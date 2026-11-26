"""Compare tie policies on Dev with one set of base-model scores per query."""
import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from src.analysis_utils import lexical_overlap
from src.budget import select_within_budget
from src.corpus import build_chunks, load_units
from src.dense import load_sentence_transformer
from src.evidence_metrics import first_hit_rank
from src.hybrid import rrf, rrf_scores
from src.replay_dev import covered_fraction, recall, write_rows
from src.retrievers import build_retrievers
from src.run_retrieval_eval import BUDGETS, CHUNK_SIZES, OVERLAP_RATIO, POOL, load_questions
from src.tie_breaks import rank_scores

RRF_K = 60


def tie_audit(scores, baseline, reversed_order, neutral, cutoffs=(5, 10, 50)):
    groups = defaultdict(set)
    counts = Counter(scores.values())
    for cid, score in scores.items():
        groups[score].add(cid.split(":", 1)[0])
    for k in cutoffs:
        old, reverse, new = baseline[:k], reversed_order[:k], neutral[:k]
        yield dict(k=k, slots=len(old),
                   tied_slots=sum(counts[scores[cid]] > 1 for cid in old),
                   cross_regulation_tied_slots=sum(len(groups[scores[cid]]) > 1 for cid in old),
                   cutoff_tie=len(baseline) > k and scores[baseline[k-1]] == scores[baseline[k]],
                   reverse_swaps=len(set(old).difference(reverse)),
                   neutral_swaps=len(set(old).difference(new)),
                   ai_act_legacy=sum(cid.startswith("ai_act:") for cid in old),
                   ai_act_reverse=sum(cid.startswith("ai_act:") for cid in reverse),
                   ai_act_neutral=sum(cid.startswith("ai_act:") for cid in new))


def replay(units, questions, embed):
    results, audits = [], []
    for size in CHUNK_SIZES:
        size_label = "article" if size is None else size
        chunks = build_chunks(units, size, 0 if size is None else int(size * OVERLAP_RATIO))
        by_id = {c.chunk_id: c for c in chunks}
        ids = list(by_id)
        methods = ["bm25"] if size is None else ["bm25", "dense", "hybrid"]
        models = build_retrievers(chunks, methods, embed if size is not None else None, POOL)
        for q in questions:
            base_old, base_new = {}, {}
            for method in methods:
                if method == "hybrid":
                    continue
                values = models[method].scores(q["question"])
                old = rank_scores(ids, values, len(ids))
                reverse = rank_scores(ids, values, POOL, reverse_input=True)
                neutral = rank_scores(ids, values, POOL, models[method].tie_order)
                scores = dict(zip(ids, values))
                audits.extend(dict(qid=q["id"], split="dev", chunk_size=size_label, method=method, **row)
                              for row in tie_audit(scores, old, reverse, neutral))
                base_old[method], base_new[method] = old[:POOL], neutral

            rankings = {"legacy": base_old.copy(), "neutral": base_new.copy()}
            if size is not None:
                order = models["hybrid"].tie_order
                fused = rrf_scores(list(base_old.values()), RRF_K)
                ranked = rrf(list(base_old.values()), RRF_K)
                reverse = sorted(sorted(fused, reverse=True), key=fused.__getitem__, reverse=True)
                neutral = rrf(list(base_old.values()), RRF_K, tie_order=order)
                audits.extend(dict(qid=q["id"], split="dev", chunk_size=size_label, method="hybrid", **row)
                              for row in tie_audit(fused, ranked, reverse, neutral))
                rankings["legacy"]["hybrid"] = ranked[:POOL]
                rankings["rrf_only"] = {"hybrid": neutral[:POOL]}
                rankings["neutral"]["hybrid"] = rrf(list(base_new.values()), RRF_K, tie_order=order)[:POOL]

            for policy, methods_ranked in rankings.items():
                for method, ranking in methods_ranked.items():
                    ranked_chunks = [by_id[cid] for cid in ranking]
                    spans = q["spans"]
                    hit = first_hit_rank(ranked_chunks, spans)
                    for budget in BUDGETS:
                        selected = select_within_budget(ranked_chunks, budget, allow_oversized_first=size is None)
                        results.append(dict(
                            policy=policy, method=method, chunk_size=size_label, budget_chars=budget,
                            qid=q["id"], split=q["split"], type=q["type"], n_gold_spans=len(spans),
                            lexical_overlap=round(lexical_overlap(q["question"], q["evidence_text"]), 3),
                            recall=recall(selected, spans), rr=1 / hit if hit else 0.,
                            recall_coverage50=sum(covered_fraction(s, selected) >= .5 for s in spans) / len(spans),
                            n_chunks=len(selected), ctx_chars=sum(len(c.text) for c in selected),
                            ranked_ids=json.dumps(ranking, separators=(",", ":")),
                        ))
    return results, audits


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    if not args.model.is_dir():
        parser.error("--model must be an existing local snapshot")
    corpus = sorted(Path("data/processed").glob("*.jsonl"))
    units = load_units(*corpus)
    questions_path = Path("eval/questions.csv")
    questions = [q for q in load_questions(questions_path, {u["unit_id"]: u for u in units}, {"dev"})
                 if q["type"] != "unanswerable"]
    if not questions or any(not q["spans"] for q in questions):
        parser.error("Answerable Dev questions with resolved spans are required")
    for path in [questions_path, *corpus, args.model / "model.safetensors"]:
        print(f"{path.name} SHA-256 {hashlib.sha256(path.read_bytes()).hexdigest()}", flush=True)
    results, audits = replay(units, questions, load_sentence_transformer(str(args.model.resolve())))
    for policy in ("legacy", "rrf_only", "neutral"):
        write_rows(args.out_dir / f"dev_{policy}.csv", [row for row in results if row["policy"] == policy])
    write_rows(args.out_dir / "tie_audit.csv", audits)
    print(f"Wrote {len(results)} Dev results and {len(audits)} tie audit rows")


if __name__ == "__main__":
    main()
