"""Look at what a retriever returns for ONE question (error analysis starts here).

    python -m src.inspect_question Q005 --method bm25 --chunk-size 800 --budget 8000
    python -m src.inspect_question Q005 --method dense --chunk-size 800

Legend in the ranking: '*' = the chunk is inside the context budget, 'HIT' = it overlaps gold evidence.
The test split is locked, exactly as in run_retrieval_eval.
"""

import argparse
from pathlib import Path

from src.analysis_utils import lexical_overlap
from src.budget import select_within_budget
from src.corpus import build_chunks, load_units
from src.evidence import chunk_overlaps
from src.evidence_metrics import first_hit_rank
from src.retrievers import METHODS, build_retrievers
from src.run_retrieval_eval import OVERLAP_RATIO, POOL, load_questions


def format_ranking(ranked, spans, context_ids, top=8, width=90) -> str:
    lines = []
    for rank, c in enumerate(ranked[:top], start=1):
        hit = "HIT " if any(chunk_overlaps(c, s) for s in spans) else "    "
        in_ctx = "*" if c.chunk_id in context_ids else " "
        snippet = c.text[:width].replace("\n", " ")
        lines.append(f"{rank:>3}{in_ctx} {hit}{c.unit_id:<16} [{c.start}:{c.end}] {snippet}")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("qid")
    ap.add_argument("--method", default="bm25", choices=METHODS)
    ap.add_argument("--chunk-size", default="800", help="characters, or 'article'")
    ap.add_argument("--budget", type=int, default=8000)
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--final", action="store_true", help="required to look at a test-split question")
    ap.add_argument("--questions", default="eval/questions.csv")
    args = ap.parse_args()

    chunk_size = None if args.chunk_size == "article" else int(args.chunk_size)
    if chunk_size is None and args.method != "bm25":
        raise SystemExit("whole-article chunks are BM25-only")

    units = load_units(*sorted(Path("data/processed").glob("*.jsonl")))
    by_unit = {u["unit_id"]: u for u in units}
    matches = [q for q in load_questions(args.questions, by_unit, {"dev", "test"}) if q["id"] == args.qid]
    if not matches:
        raise SystemExit(f"no question with id {args.qid}")
    q = matches[0]
    if q["split"] == "test" and not args.final:
        raise SystemExit("This question is in the locked test split. Use --final only when configs are frozen.")

    embed_fn = None
    if args.method != "bm25":
        from src.dense import load_sentence_transformer

        embed_fn = load_sentence_transformer()

    chunks = build_chunks(units, chunk_size, 0 if chunk_size is None else int(chunk_size * OVERLAP_RATIO))
    by_id = {c.chunk_id: c for c in chunks}
    retriever = build_retrievers(chunks, [args.method], embed_fn, POOL)[args.method]
    ranked = [by_id[cid] for cid in retriever.search(q["question"], k=POOL)]
    context = select_within_budget(ranked, args.budget)

    print(f"{q['id']} [{q['split']}, {q['type']}]  {q['question']}")
    print(f"gold answer: {q['gold_answer']}")
    print(f"lexical overlap with evidence: {lexical_overlap(q['question'], q['evidence_text']):.2f}")
    for s in q["spans"]:
        print(f"gold evidence: {s.unit_id} [{s.start}:{s.end}] {by_unit[s.unit_id]['text'][s.start : s.end][:100]}")
    print(f"\n{args.method}, chunk size {args.chunk_size}, budget {args.budget}: {len(context)} chunks in context, "
          f"first hit at rank {first_hit_rank(ranked, q['spans'])} (of {POOL})\n")  # fmt: skip
    print(format_ranking(ranked, q["spans"], {c.chunk_id for c in context}, args.top))


if __name__ == "__main__":
    main()
