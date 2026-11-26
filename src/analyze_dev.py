"""Paired Dev Pilot inference. See eval/dev_pilot_p1/README.md for the analysis decisions."""
import argparse
from itertools import combinations
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.metrics import bootstrap_ci
from src.pilot_inference import (
    PRIMARY_BOOTSTRAPS, continuous_overlap_dev, dev_annotations, exact_sign_flip, extreme_count, primary_dev,
)
from src.retrievers import METHODS
from src.run_retrieval_eval import BUDGETS, CHUNK_SIZES

SIZES = tuple(s for s in CHUNK_SIZES if s is not None)
KEYS = ["qid", "method", "chunk_size", "budget_chars"]
THRESHOLDS = (.20, .25, .30, .40)


def load_pilot(path, metric):
    """Require the same questions in each of the strict-budget factorial cells."""
    frame = pd.read_csv(path, dtype={"chunk_size": str, "qid": str})
    required = {*KEYS, "split", "type", "lexical_overlap", metric}
    if not required <= set(frame):
        raise ValueError(f"Missing columns: {sorted(required - set(frame))}")
    if frame.empty or not frame["split"].eq("dev").all():
        raise ValueError("Only nonempty Dev results are accepted")
    strict = frame[frame.chunk_size != "article"].copy()
    if "budget_policy" in strict and not strict.budget_policy.eq("strict").all():
        raise ValueError("Expected strict-budget rows for fixed-size settings")
    strict["chunk_size"] = pd.to_numeric(strict.chunk_size)
    if strict.empty or strict[KEYS].isna().any().any() or strict.duplicated(KEYS).any():
        raise ValueError("Empty, incomplete, or duplicate question/configuration keys")
    cells = {(m, s, b) for m in METHODS for s in SIZES for b in BUDGETS}
    if not all(
        set(zip(q.method, q.chunk_size, q.budget_chars)) == cells
        for _, q in strict.groupby("qid")
    ):
        raise ValueError("Each question needs exactly the full strict-budget grid")
    if not strict["lexical_overlap"].between(0, 1).all() or not strict[metric].between(0, 1).all():
        raise ValueError("Scores and lexical overlap must be finite and in [0, 1]")
    attrs = strict.groupby("qid")[["type", "lexical_overlap"]].nunique(dropna=False)
    if (attrs != 1).any().any() or strict["type"].isna().any() or strict["type"].eq("unanswerable").any():
        raise ValueError("Each question needs one answerable type and one overlap score")
    return strict


def holm(p_values):
    """Holm step-down adjusted p-values in original order, with monotonicity."""
    p = np.asarray(p_values, dtype=float)
    order = np.argsort(p, kind="stable")
    adjusted = np.empty(len(p))
    adjusted[order] = np.minimum(1, np.maximum.accumulate((len(p) - np.arange(len(p))) * p[order]))
    return adjusted


def bootstrap_test(values, null, alternative, n_boot, seed):
    """Centered paired nonparametric bootstrap test of a mean at the null boundary."""
    v = np.asarray(values)
    observed = v.mean() - null
    # Bootstrap whole question differences. Center to impose the tested null mean.
    rng = np.random.default_rng(seed)
    centered = v[rng.integers(len(v), size=(n_boot, len(v)))].mean(axis=1) - v.mean()
    return (extreme_count(centered, observed, alternative) + 1) / (n_boot + 1)


def analyze(frame, metric, inspected, n_boot=10000, seed=0):
    means, tests = [], []
    for cohort, selected in (
        ("all_dev", frame),
        ("exclude_inspected", frame[~frame.qid.isin(inspected)]),
    ):
        attrs = selected.drop_duplicates("qid").set_index("qid")
        context = {"metric": metric, "cohort": cohort}

        def compare(differences, *, family, contrast, budget, group="all",
                    size="", threshold="", null=0.0, alternative="two-sided", **detail):
            values = differences.sort_index().tolist()
            row = dict(context, family=family, contrast=contrast, budget_chars=budget,
                       subgroup=group, chunk_size=size, overlap_threshold=threshold,
                       null_effect=null, alternative=alternative, n=len(values),
                       n_boot=n_boot, seed=seed, p_raw=np.nan, p_bootstrap_floor=1 / (n_boot + 1),
                       p_signflip_exact=np.nan, **detail)
            if len(values) >= 2:
                effect, low, high = bootstrap_ci(values, n_boot=n_boot, seed=seed)
                row.update(effect=effect, ci_low=low, ci_high=high,
                           p_raw=bootstrap_test(values, null, alternative, n_boot, seed),
                           status="estimated")
            else:
                row.update(effect=values[0] if values else np.nan, status="insufficient_pairs")
            if 2 <= len(values) <= 20:
                row["p_signflip_exact"] = exact_sign_flip(values, null, alternative)
            row["bootstrap_at_floor"] = row["p_raw"] == row["p_bootstrap_floor"]
            tests.append(row)

        for budget in BUDGETS:
            block = selected[selected.budget_chars.eq(budget)]
            grid = block.pivot(index="qid", columns=["method", "chunk_size"], values=metric)
            grid = grid.reindex(columns=[(m, s) for m in METHODS for s in SIZES])
            for method in METHODS:
                scores = grid[method]
                for size in SIZES:
                    vals = scores[size].tolist()
                    mean, low, high = bootstrap_ci(vals, n_boot=n_boot, seed=seed) if vals else (np.nan,) * 3
                    means.append(dict(context, budget_chars=budget, method=method, chunk_size=size,
                                      n=len(vals), mean=mean, ci_low=low, ci_high=high))
                mid = (scores[800] + scores[1200]) / 2
                for label, delta in (
                    ("C: mid minus extremes", mid - (scores[400] + scores[2000]) / 2),
                    ("mid minus 400", mid - scores[400]),
                    ("mid minus 2000", mid - scores[2000]),
                ):
                    compare(delta, family="H1_shape", contrast=label, budget=budget,
                            method_a=method, alternative="greater")

            method_pairs = list(combinations(METHODS, 2))
            for size in (*SIZES, "equal_weight_over_sizes"):
                scores = (grid.T.groupby(level=0).mean().T if isinstance(size, str)
                          else grid.xs(size, axis=1, level=1))

                def method_delta(a, b, ids, family, group, **options):
                    x, y = scores[a].loc[ids], scores[b].loc[ids]
                    compare(x - y, family=family, contrast=f"{a} - {b}", budget=budget, size=size,
                            group=group, method_a=a, method_b=b, mean_a=x.mean(), mean_b=y.mean(), **options)

                for a, b in method_pairs:
                    method_delta(a, b, scores.index, "H2_overall", "all")
                for question_type in sorted(frame["type"].unique()):
                    group_ids = scores.index.intersection(attrs.index[attrs.type.eq(question_type)])
                    for a, b in method_pairs:
                        method_delta(a, b, group_ids, "H2_by_type", question_type)
                multi = scores.index.intersection(attrs.index[attrs.type.eq("multi_hop")])
                for method in ("dense", "hybrid"):
                    method_delta(method, "bm25", multi, "H2b_multi_hop", "multi_hop", alternative="greater")
                for threshold in THRESHOLDS:
                    high = attrs.lexical_overlap.ge(threshold)
                    high_ids = scores.index.intersection(attrs.index[high])
                    low_ids = scores.index.intersection(attrs.index[~high])
                    method_delta("bm25", "dense", high_ids, "H2a_high_margin", "high",
                                 threshold=threshold, null=-.05, alternative="greater")
                    for method in ("dense", "hybrid"):
                        method_delta(method, "bm25", low_ids, "H2b_low", "low",
                                     threshold=threshold, alternative="greater")
    table = pd.DataFrame(tests)
    table["p_holm"] = np.nan
    table["family_size"] = 0
    for _, group in table.groupby(["metric", "cohort", "family", "overlap_threshold"]):
        # Insufficient comparisons stay visible and count toward the planned family size.
        adjusted = holm(group.p_raw.fillna(1).to_numpy())
        table.loc[group.index, "p_holm"] = np.where(group.p_raw.notna(), adjusted, np.nan)
        table.loc[group.index, "family_size"] = len(group)
    return pd.DataFrame(means), table


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=Path("results/retrieval_dev.csv"))
    parser.add_argument("--coverage", type=Path, help="Optional Dev replay CSV from src.replay_dev")
    parser.add_argument("--metadata", type=Path, default=Path("eval/dev_pilot_metadata.json"))
    parser.add_argument("--questions", type=Path, default=Path("eval/questions.csv"),
                        help="Frozen annotations for the Dev protocol preview")
    parser.add_argument("--out-dir", type=Path, default=Path("results/dev_analysis"))
    parser.add_argument("--n-boot", type=int, default=10000, help="Bootstrap iterations for exploratory comparisons")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    if args.n_boot < 1 or args.seed < 0:
        parser.error("--n-boot must be positive and --seed nonnegative")
    inspected = json.loads(args.metadata.read_text())["inspection_records"]
    frame = load_pilot(args.results, "recall")
    if not set(inspected) <= set(frame.qid):
        parser.error("Dev results are missing one or more inspected question IDs")
    inputs = [(frame, "recall")]
    if args.coverage:
        replay = load_pilot(args.coverage, "recall_coverage50")
        original = frame.set_index(KEYS).sort_index()
        paired = replay.set_index(KEYS).sort_index()
        if not original.index.equals(paired.index) or not original[["type", "lexical_overlap"]].equals(
            paired[["type", "lexical_overlap"]]
        ):
            parser.error("Replay and pilot must cover identical question/settings and annotations")
        if not paired["recall"].between(0, 1).all() or (paired["recall_coverage50"] > paired["recall"]).any():
            parser.error("Replay coverage is inconsistent with its any-overlap recall")
        inputs.extend([(replay, "recall_replayed"), (replay, "recall_coverage50")])
    overlaps, clusters = dev_annotations(args.questions, set(frame.qid))
    preview = primary_dev(frame, overlaps, clusters, PRIMARY_BOOTSTRAPS, 0, holm)
    continuous = continuous_overlap_dev(frame, overlaps, clusters)
    all_means, all_tests = [], []
    for data, label in inputs:
        if label == "recall_replayed":
            data = data.assign(recall_replayed=data.recall)
        means, tests = analyze(data, label, inspected, args.n_boot, args.seed)
        all_means.append(means)
        all_tests.append(tests)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    pd.concat(all_means, ignore_index=True).to_csv(args.out_dir / "means.csv", index=False)
    pd.concat(all_tests, ignore_index=True).to_csv(args.out_dir / "contrasts.csv", index=False)
    preview.to_csv(args.out_dir / "primary_protocol_dev.csv", index=False)
    pd.DataFrame([continuous]).to_csv(args.out_dir / "continuous_overlap_dev.csv", index=False)


if __name__ == "__main__":
    main()
