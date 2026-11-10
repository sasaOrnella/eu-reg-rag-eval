"""Retrieval experiment: method x chunk size x context budget.   Run from the repo root:

    python -m src.run_retrieval_eval --split dev                      # bm25, dense, hybrid
    python -m src.run_retrieval_eval --split dev --methods bm25       # no model needed

For every configuration it chunks the corpus, retrieves for every answerable question, keeps the best
chunks that fit in the character budget, and records evidence recall for each question.

Rules built into this script
  * The test split is locked: it needs --final, to be used once, when configurations are frozen.
  * Unanswerable questions are skipped: they have no gold evidence, so recall is undefined.
  * Whole-article chunks are BM25-only: they are far longer than the embedder's input limit.
  * Results are written per question (results/*.csv) so that bootstrap confidence intervals can be
    computed later; the printed tables only show means.
"""

import argparse
import csv
from pathlib import Path

import pandas as pd

from src.analysis_utils import lexical_overlap
from src.budget import select_within_budget
from src.corpus import build_chunks, load_units
from src.dense import truncation_rate
from src.evidence import resolve_evidence
from src.evidence_metrics import evidence_recall_at_k, first_hit_rank
from src.retrievers import METHODS, build_retrievers

CHUNK_SIZES = [400, 800, 1200, 2000, None]  # characters; None = whole article/recital as one chunk
BUDGETS = [4000, 8000]  # characters, roughly 1000 and 2000 tokens
OVERLAP_RATIO = 0.1  # overlap is 10% of chunk size, kept constant so it does not confound chunk size
POOL = 50  # how many ranked candidates the retriever hands to the budget step


def load_questions(path: str, units_by_id: dict, splits: set[str]) -> list[dict]:
    """Read the CSV, keep the wanted splits, and attach resolved gold spans and evidence text."""
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    questions = []
    for r in rows:
        if r["split"] not in splits:
            continue
        spans = resolve_evidence(r["gold_evidence"], units_by_id) if r["gold_evidence"].strip() else []
        evidence_text = " ".join(units_by_id[s.unit_id]["text"][s.start : s.end] for s in spans)
        questions.append({**r, "spans": spans, "evidence_text": evidence_text})
    return questions


def score_questions(retriever, method, by_id, questions, chunk_size, budget_chars, pool=POOL, selector=select_within_budget):
    """One retriever, one budget -> one result row per answerable question."""
    rows = []
    for q in questions:
        if q["type"] == "unanswerable":
            continue
        ranked = [by_id[cid] for cid in retriever.search(q["question"], k=pool)]
        context = selector(ranked, budget_chars)
        rank = first_hit_rank(ranked, q["spans"])
        rows.append(
            {
                "method": method,
                "chunk_size": "article" if chunk_size is None else chunk_size,
                "budget_chars": budget_chars,
                "qid": q["id"],
                "split": q["split"],
                "type": q["type"],
                "n_gold_spans": len(q["spans"]),
                "lexical_overlap": round(lexical_overlap(q["question"], q["evidence_text"]), 3),
                "recall": evidence_recall_at_k(context, q["spans"], k=max(len(context), 1)),
                "rr": 1 / rank if rank else 0.0,
                "n_chunks": len(context),
                "ctx_chars": sum(len(c.text) for c in context),
            }
        )
    return rows


def run_chunking(
    units, questions, chunk_size, budgets, methods=("bm25",), embed_fn=None,
    overlap_ratio=OVERLAP_RATIO, pool=POOL, selector=select_within_budget,
) -> list[dict]:  # fmt: skip
    """Chunk once, build the retrievers once, then score every requested method and budget."""
    overlap = 0 if chunk_size is None else int(chunk_size * overlap_ratio)
    chunks = build_chunks(units, chunk_size, overlap)
    by_id = {c.chunk_id: c for c in chunks}

    # whole-article chunks are far longer than the embedder's input limit, so they stay BM25-only
    usable_embed = embed_fn if chunk_size is not None else None
    retrievers = build_retrievers(chunks, methods, usable_embed, pool)
    if usable_embed is not None:
        rate = truncation_rate([c.text for c in chunks], usable_embed)
        if rate is not None:
            note = "  <-- dense results for this size are affected" if rate > 0.01 else ""
            print(f"  chunk_size={chunk_size}: {rate:.1%} of chunks exceed the embedder input limit{note}")

    rows = []
    for method in methods:
        if method not in retrievers:
            print(f"  chunk_size={'article' if chunk_size is None else chunk_size}: skipping {method}")
            continue
        for budget in budgets:
            rows += score_questions(retrievers[method], method, by_id, questions, chunk_size, budget, pool, selector)
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="dev", choices=["dev", "test"])
    ap.add_argument("--final", action="store_true", help="required to touch the test split")
    ap.add_argument("--methods", nargs="+", default=METHODS, choices=METHODS)
    ap.add_argument("--questions", default="eval/questions.csv")
    ap.add_argument("--out", default=None, help="default: results/retrieval_<split>.csv")
    ap.add_argument("--by-type", action="store_true", help="also print recall broken down by question type")
    args = ap.parse_args()

    if args.split == "test" and not args.final:
        raise SystemExit("The test split is reserved for final numbers. Use --final only when configs are frozen.")

    embed_fn = None
    if set(args.methods) & {"dense", "hybrid"}:
        try:
            from src.dense import load_sentence_transformer

            embed_fn = load_sentence_transformer()
        except ImportError:
            raise SystemExit("dense/hybrid need the embedding library: pip install -r requirements-dense.txt")
        print(f"embedding model: {embed_fn.model_name} (input limit {embed_fn.max_seq_length} tokens)")

    units = load_units(*sorted(Path("data/processed").glob("*.jsonl")))
    units_by_id = {u["unit_id"]: u for u in units}
    questions = load_questions(args.questions, units_by_id, {args.split})
    n_answerable = sum(q["type"] != "unanswerable" for q in questions)

    rows = []
    for chunk_size in CHUNK_SIZES:
        rows += run_chunking(units, questions, chunk_size, BUDGETS, args.methods, embed_fn)

    out = Path(args.out or f"results/retrieval_{args.split}.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(out, index=False)

    print(f"\n{args.split}: {n_answerable} answerable questions, {len(df)} result rows -> {out}")
    if n_answerable < 100:
        print(f"WARNING: n={n_answerable} is a pilot. Differences are within noise; do not draw conclusions yet.")
    for budget in BUDGETS:
        sub = df[df["budget_chars"] == budget]
        print(f"\nMean evidence recall, budget = {budget} characters (rows: chunk size, columns: method):")
        print(sub.pivot_table(index="chunk_size", columns="method", values="recall", aggfunc="mean", sort=False).round(3).to_string())
    if args.by_type:
        big = df[df["budget_chars"] == max(BUDGETS)]
        print(f"\nMean recall by question type, budget = {max(BUDGETS)}:")
        print(big.pivot_table(index=["method", "chunk_size"], columns="type", values="recall", aggfunc="mean", sort=False).round(2).to_string())


if __name__ == "__main__":
    main()
