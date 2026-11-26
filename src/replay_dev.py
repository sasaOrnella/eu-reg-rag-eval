"""Replay answerable Dev questions for span coverage and RRF diagnostics."""
import argparse
import csv
from collections import Counter
import hashlib
import json
from pathlib import Path

from src.analysis_utils import lexical_overlap
from src.budget import select_within_budget
from src.corpus import build_chunks, load_units
from src.dense import load_sentence_transformer
from src.evidence import chunk_overlaps
from src.evidence_metrics import evidence_recall_at_k
from src.hybrid import HybridRetriever, rrf, rrf_scores
from src.retrievers import METHODS, build_retrievers
from src.run_retrieval_eval import BUDGETS, CHUNK_SIZES, OVERLAP_RATIO, POOL, load_questions


def covered_fraction(span, chunks):
    """Measure union coverage in the span's own unit, counting each character once."""
    bands = sorted(
        (max(span.start, c.start), min(span.end, c.end))
        for c in chunks if chunk_overlaps(c, span)
    )
    end, length = span.start, 0
    for start, stop in bands:
        length += max(0, stop - max(start, end))
        end = max(end, stop)
    return length / (span.end - span.start)


def recall(chunks, spans):
    return evidence_recall_at_k(chunks, spans, max(1, len(chunks)))


def first_ranks(ranked, spans):
    return [
        next((i for i, c in enumerate(ranked, 1) if chunk_overlaps(c, span)), None)
        for span in spans
    ]


def tie_statistics(rankings, rrf_k, cutoffs=(5, 10, 50)):
    """Audit exact production-score ties and reverse only the ID tie-break."""
    scores = rrf_scores(rankings, rrf_k)
    counts = Counter(scores.values())
    ranked = sorted(scores, key=lambda cid: (-scores[cid], cid))
    reversed_ties = sorted(sorted(scores, reverse=True), key=scores.__getitem__, reverse=True)
    for cutoff in cutoffs:
        top = ranked[:cutoff]
        reverse_top = reversed_ties[:cutoff]
        insiders = set(top)
        tied = [cid for cid in top if counts[scores[cid]] > 1]
        cross_regulation = {
            scores[cid] for cid in tied
            if any(scores[other] == scores[cid] and other.split(":")[0] != cid.split(":")[0]
                   for other in ranked)
        }
        yield {
            "k": cutoff, "slots": len(top), "tied_slots": len(tied),
            "cross_regulation_tied_slots": sum(scores[cid] in cross_regulation for cid in top),
            "cutoff_tie": len(ranked) > cutoff and scores[top[-1]] == scores[ranked[cutoff]],
            "changed_members": len(insiders.difference(reverse_top)),
            "ai_act_slots": sum(cid.startswith("ai_act:") for cid in top),
            "ai_act_slots_reverse": sum(cid.startswith("ai_act:") for cid in reverse_top),
        }


def replay(units, questions, embed, tie_rows=None):
    for size in (s for s in CHUNK_SIZES if s is not None):
        chunks = build_chunks(units, size, int(size * OVERLAP_RATIO))
        by_id = {chunk.chunk_id: chunk for chunk in chunks}
        models = build_retrievers(chunks, METHODS, embed, POOL, legacy_ties=True)
        for q in questions:
            query, spans = q["question"], q["spans"]
            # One search per base ranker. RRF consumes the same prefix as HybridRetriever.
            diagnostic_depth = 100 if size in (400, 800) else POOL
            base = {method: models[method].search(query, k=diagnostic_depth) for method in ("bm25", "dense")}
            rankings = {name: ids[:POOL] for name, ids in base.items()}
            hybrid: HybridRetriever = models["hybrid"]
            component_lists = list(rankings.values())
            fused = rrf(component_lists, hybrid.rrf_k)
            if tie_rows is not None:
                tie_rows.extend(
                    dict(qid=q["id"], split="dev", chunk_size=size, pool=hybrid.pool,
                         rrf_k=hybrid.rrf_k, **stats)
                    for stats in tie_statistics(component_lists, hybrid.rrf_k)
                )
            rankings["hybrid"] = fused[:POOL]
            for method, ids in rankings.items():
                ranked = [by_id[cid] for cid in ids]
                for budget in BUDGETS:
                    selected = select_within_budget(ranked, budget)
                    coverage = [covered_fraction(span, selected) for span in spans]
                    row = {
                        "method": method, "chunk_size": size, "budget_chars": budget,
                        "qid": q["id"], "split": q["split"], "type": q["type"],
                        "lexical_overlap": round(lexical_overlap(query, q["evidence_text"]), 3),
                        "recall": recall(selected, spans),
                        "recall_coverage50": sum(value >= .5 for value in coverage) / len(spans),
                        "n_chunks": len(selected), "ctx_chars": sum(len(c.text) for c in selected),
                    }
                    row.update(dict.fromkeys(
                        ("recall_pool", "recall_union", "bm25_span_ranks", "dense_span_ranks",
                         "rrf_span_ranks", "next_chunk_chars", "rrf_pool10", "rrf_pool25", "rrf_pool100"), ""
                    ))
                    if method == "hybrid" and size in (400, 800) and budget == 4000:
                        row.update(
                            recall_pool=recall(ranked, spans),
                            recall_union=recall([by_id[cid] for cid in fused], spans),
                            bm25_span_ranks=json.dumps(first_ranks([by_id[cid] for cid in base["bm25"][:POOL]], spans)),
                            dense_span_ranks=json.dumps(first_ranks([by_id[cid] for cid in base["dense"][:POOL]], spans)),
                            rrf_span_ranks=json.dumps(first_ranks([by_id[cid] for cid in fused], spans)),
                            next_chunk_chars=len(ranked[len(selected)].text) if len(selected) < len(ranked) else "",
                        )
                        for depth in (10, 25, 100):
                            alternative = rrf([ids[:depth] for ids in base.values()], hybrid.rrf_k)[:POOL]
                            selection = select_within_budget([by_id[cid] for cid in alternative], budget)
                            row[f"rrf_pool{depth}"] = recall(selection, spans)
                    yield row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Path to a pinned local SentenceTransformer snapshot")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--rrf-ties", type=Path, help="Write Dev top-K tie statistics")
    args = parser.parse_args()
    model = Path(args.model)
    if not model.is_dir():
        parser.error("--model must be an existing local snapshot directory")
    corpus = sorted(Path("data/processed").glob("*.jsonl"))
    units = load_units(*corpus)
    questions_path = Path("eval/questions.csv")
    questions = [
        q for q in load_questions(questions_path, {u["unit_id"]: u for u in units}, {"dev"})
        if q["type"] != "unanswerable"
    ]
    if not questions or any(not q["spans"] for q in questions):
        parser.error("answerable Dev questions with resolved spans are required")
    for path in [questions_path, *corpus, model / "model.safetensors"]:
        print(f"{path} SHA-256 {hashlib.sha256(path.read_bytes()).hexdigest()}", flush=True)
    if args.rrf_ties and args.rrf_ties.resolve() == args.out.resolve():
        parser.error("--rrf-ties and --out must be different files")
    ties = [] if args.rrf_ties else None
    rows = list(replay(units, questions, load_sentence_transformer(str(model.resolve())), ties))
    write_rows(args.out, rows)
    if ties:
        write_rows(args.rrf_ties, ties)
    print(f"Wrote {len(rows)} Dev-only configuration rows to {args.out}")


def write_rows(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
