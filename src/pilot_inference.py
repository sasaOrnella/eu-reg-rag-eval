"""Statistical helpers for the prospective protocol exercised on Dev."""
import csv
from pathlib import Path

import numpy as np
import pandas as pd

from src.analysis_utils import lexical_overlap
from src.metrics import bootstrap_ci

PRIMARY_BUDGET = 8000
PRIMARY_BOOTSTRAPS = 200_000
HIGH_CUTOFF = .30


def extreme_count(draws, observed, alternative):
    if alternative == "greater":
        return np.count_nonzero(draws >= observed - 1e-12)
    if alternative == "less":
        return np.count_nonzero(draws <= observed + 1e-12)
    if alternative == "two-sided":
        return np.count_nonzero(np.abs(draws) >= abs(observed) - 1e-12)
    raise ValueError(f"Unknown alternative: {alternative}")


def exact_sign_flip(values, null, alternative):
    """Enumerate sign assignments under symmetry of paired differences at the null."""
    shifted = np.asarray(values, dtype=float) - null
    if not 1 <= len(shifted) <= 20:
        raise ValueError("Exact sign flip requires 1–20 pairs")
    sums = np.zeros(1)
    # Zero differences would duplicate every sum and leave its probability unchanged.
    for magnitude in np.abs(shifted[shifted != 0]):
        sums = np.concatenate((sums - magnitude, sums + magnitude))
    return extreme_count(sums, shifted.sum(), alternative) / len(sums)


def dev_annotations(path: Path, qids):
    """Read only selected answerable Dev annotations and link shared evidence units."""
    overlaps, owners = {}, {}
    parent = {qid: qid for qid in qids}

    def root(qid):
        while parent[qid] != qid:
            qid = parent[qid]
        return qid

    with path.open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            qid = row["id"]
            if row["split"] != "dev" or qid not in parent:
                continue
            if row["type"] == "unanswerable" or qid in overlaps:
                raise ValueError(f"Expected one answerable Dev annotation for {qid}")
            quotes = []
            for piece in row["gold_evidence"].split("||"):
                unit, sep, quote = piece.partition("::")
                if not sep or not unit.strip() or not quote.strip():
                    raise ValueError(f"Malformed evidence for {qid}")
                owner = owners.setdefault(unit.strip(), qid)
                parent[root(qid)] = root(owner)
                quotes.append(quote.strip())
            overlaps[qid] = lexical_overlap(row["question"], " ".join(quotes))
    if overlaps.keys() != parent.keys():
        raise ValueError("Dev scores must have matching annotations")
    return pd.Series(overlaps, dtype=float), {qid: root(qid) for qid in parent}


def cluster_statistics(values, clusters, null, alternative, n_boot, seed):
    """Resample connected evidence clusters, retaining question-weighted means."""
    labels = pd.Series([clusters[qid] for qid in values.index], index=values.index, dtype=str)
    groups = values.groupby(labels)
    sizes, sums = groups.size().to_numpy(), groups.sum().to_numpy()
    result = {"n_clusters": len(sizes), "max_cluster_size": max(sizes, default=0),
              "cluster_ci_low": np.nan, "cluster_ci_high": np.nan, "p_raw": np.nan}
    if len(sizes) >= 2:
        rng = np.random.default_rng(seed)
        means = np.empty(n_boot)
        for start in range(0, n_boot, 10_000):
            stop = min(start + 10_000, n_boot)
            draws = rng.integers(len(sizes), size=(stop - start, len(sizes)))
            means[start:stop] = sums[draws].sum(axis=1) / sizes[draws].sum(axis=1)
        low, high = np.quantile(means, [.025, .975])
        count = extreme_count(means - values.mean(), values.mean() - null, alternative)
        result.update(cluster_ci_low=low, cluster_ci_high=high, p_raw=(count + 1) / (n_boot + 1))
    return result


def primary_dev(frame, overlaps, clusters, n_boot, seed, holm):
    """Exercise prospective hypotheses on original any-overlap, all-Dev results."""
    grid = frame[frame.budget_chars.eq(PRIMARY_BUDGET)].pivot(
        index="qid", columns=["method", "chunk_size"], values="recall"
    )
    scores = grid.T.groupby(level=0).mean().T
    high = overlaps.reindex(grid.index).ge(HIGH_CUTOFF)
    rows = []

    def component(hypothesis, name, values, null=0., alternative="greater"):
        n = len(values)
        if n >= 2:
            effect, low, upper = bootstrap_ci(values.tolist(), n_boot=n_boot, seed=seed)
        else:
            effect, low, upper = values.mean(), np.nan, np.nan
        row = dict(hypothesis=hypothesis, component=name, n=n, effect=effect,
                   pair_ci_low=low, pair_ci_high=upper, null=null, alternative=alternative)
        row.update(cluster_statistics(values, clusters, null, alternative, n_boot, seed))
        row["p_signflip_exact"] = exact_sign_flip(values, null, alternative) if 2 <= n <= 20 else np.nan
        return row

    def claim(family, hypothesis, components):
        probabilities = [row["p_raw"] for row in components]
        combined = max(probabilities) if all(np.isfinite(probabilities)) else np.nan
        for row in components:
            rows.append(dict(family=family, claim_p=combined, **row))

    for method in ("bm25", "dense", "hybrid"):
        curve = grid[method]
        middle = (curve[800] + curve[1200]) / 2
        name = f"H1_{method}"
        claim("primary", name, [
            component(name, "middle_minus_400", middle - curve[400]),
            component(name, "middle_minus_2000", middle - curve[2000]),
        ])
    delta = (scores.bm25 - scores.dense)[high]
    for margin, family in ((.05, "primary"), (.10, "secondary_margin")):
        for direction, alternative in (("noninferiority", "greater"), ("inferiority", "less")):
            name = f"H2a_{margin:.2f}_{direction}"
            claim(family, name, [component(name, "bm25_minus_dense_high", delta, -margin, alternative)])
    for method in ("dense", "hybrid"):
        name = f"H2b_{method}_low"
        claim("primary", name, [component(name, f"{method}_minus_bm25_low", (scores[method] - scores.bm25)[~high])])
    claim("primary", "H2c_overall", [
        component("H2c_overall", f"hybrid_minus_{method}", scores.hybrid - scores[method], -.10)
        for method in ("bm25", "dense")
    ])
    table = pd.DataFrame(rows)
    table["claim_p_holm"] = np.nan
    for _, group in table.groupby("family"):
        claims = group.drop_duplicates("hypothesis").set_index("hypothesis").claim_p
        adjusted = pd.Series(holm(claims.fillna(1).to_numpy()), index=claims.index).where(claims.notna())
        table.loc[group.index, "claim_p_holm"] = group.hypothesis.map(adjusted)
    table["decision"] = np.select(
        [table.claim_p_holm.isna(), table.claim_p_holm.le(.05)],
        ["insufficient_clusters", "passes_pilot_threshold"], default="inconclusive",
    )
    table["stage"] = "dev_protocol_preview"
    table["budget_chars"] = PRIMARY_BUDGET
    table["n_boot"] = n_boot
    table["seed"] = seed
    table["p_bootstrap_floor"] = 1 / (n_boot + 1)
    table["bootstrap_at_floor"] = table.p_raw.eq(table.p_bootstrap_floor)
    return table



def continuous_overlap_dev(frame, overlaps, clusters, n_boot=PRIMARY_BOOTSTRAPS, seed=0):
    """Exploratory OLS slope of BM25 − Dense per +0.10 overlap, with cluster resampling."""
    selected = frame[frame.budget_chars.eq(PRIMARY_BUDGET)]
    scores = selected.groupby(["qid", "method"]).recall.mean().unstack()
    delta = scores.bm25 - scores.dense
    x = overlaps.loc[delta.index] * 10
    labels = [clusters[qid] for qid in delta.index]
    moments = pd.DataFrame(dict(n=1, x=x, y=delta, xx=x*x, xy=x*delta)).groupby(labels).sum().to_numpy()

    def slopes(totals):
        n, x_sum, y_sum, xx, xy = totals.T
        denominator = n * xx - x_sum * x_sum
        return np.divide(n * xy - x_sum * y_sum, denominator,
                         out=np.full_like(denominator, np.nan), where=denominator > 1e-12)

    effect = slopes(moments.sum(axis=0, keepdims=True))[0]
    estimates = np.empty(0)
    if len(moments) >= 2 and np.isfinite(effect):
        rng = np.random.default_rng(seed)
        estimates = np.empty(n_boot)
        for start in range(0, n_boot, 5_000):
            stop = min(start + 5_000, n_boot)
            draws = rng.integers(len(moments), size=(stop - start, len(moments)))
            estimates[start:stop] = slopes(moments[draws].sum(axis=1))
        estimates = estimates[np.isfinite(estimates)]
    low, high = np.quantile(estimates, [.025, .975]) if len(estimates) else (np.nan, np.nan)
    return dict(analysis="exploratory_H2a_continuous", budget_chars=PRIMARY_BUDGET,
                contrast="BM25 minus Dense per +0.10 overlap", n=len(delta),
                n_clusters=len(moments), effect=effect, ci_low=low, ci_high=high,
                bootstrap_draws=n_boot, defined_draws=len(estimates), seed=seed)
