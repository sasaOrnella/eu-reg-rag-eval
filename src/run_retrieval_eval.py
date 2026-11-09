"""BM25 retrieval experiment: chunk size x context budget.   Run from the repo root:

    python -m src.run_retrieval_eval --split dev

For every configuration it chunks the corpus, retrieves for every answerable question, keeps the best
chunks that fit in the character budget, and records evidence recall for each question.

Rules built into this script
  * The test split is locked: it needs --final, to be used once, when configurations are frozen.
  * Unanswerable questions are skipped: they have no gold evidence, so recall is undefined.
  * Results are written per question (results/*.csv) so that bootstrap confidence intervals can be
    computed later; the printed table only shows means.
"""

import argparse
import csv
from pathlib import Path

import pandas as pd

from src.analysis_utils import lexical_overlap
from src.bm25_baseline import BM25Retriever
from src.budget import select_within_budget
from src.corpus import build_chunks, load_units
from src.evidence import resolve_evidence
from src.evidence_metrics import evidence_recall_at_k, first_hit_rank

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


def run_config(
    units: list[dict],
    questions: list[dict],
    chunk_size: int | None,
    budget_chars: int,
    overlap_ratio: float = OVERLAP_RATIO,
    pool: int = POOL,
    selector=select_within_budget,
) -> list[dict]:
    """One configuration -> one result row per answerable question."""
    overlap = 0 if chunk_size is None else int(chunk_size * overlap_ratio)
    chunks = build_chunks(units, chunk_size, overlap)
    by_id = {c.chunk_id: c for c in chunks}
    retriever = BM25Retriever([c.chunk_id for c in chunks], [c.text for c in chunks])

    rows = []
    for q in questions:
        if q["type"] == "unanswerable":
            continue
        ranked = [by_id[cid] for cid in retriever.search(q["question"], k=pool)]
        context = selector(ranked, budget_chars)
        rank = first_hit_rank(ranked, q["spans"])
        rows.append(
            {
                "method": "bm25",
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


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="dev", choices=["dev", "test"])
    ap.add_argument("--final", action="store_true", help="required to touch the test split")
    ap.add_argument("--questions", default="eval/questions.csv")
    ap.add_argument("--out", default=None, help="default: results/bm25_<split>.csv")
    args = ap.parse_args()

    if args.split == "test" and not args.final:
        raise SystemExit("The test split is reserved for final numbers. Use --final only when configs are frozen.")

    units = load_units(*sorted(Path("data/processed").glob("*.jsonl")))
    units_by_id = {u["unit_id"]: u for u in units}
    questions = load_questions(args.questions, units_by_id, {args.split})
    n_answerable = sum(q["type"] != "unanswerable" for q in questions)

    rows = []
    for chunk_size in CHUNK_SIZES:
        for budget in BUDGETS:
            rows += run_config(units, questions, chunk_size, budget)

    out = Path(args.out or f"results/bm25_{args.split}.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(out, index=False)

    print(f"{args.split}: {n_answerable} answerable questions x {len(CHUNK_SIZES) * len(BUDGETS)} configurations -> {out}")
    if n_answerable < 100:
        print(f"WARNING: n={n_answerable} is a pilot. Differences are within noise; do not draw conclusions yet.")
    keys = ["budget_chars", "chunk_size"]
    print("\nMean over questions:")
    print(df.groupby(keys, sort=False)[["recall", "rr", "n_chunks", "ctx_chars"]].mean().round(3).to_string())
    print("\nMean recall by question type:")
    print(df.pivot_table(index=keys, columns="type", values="recall", aggfunc="mean", sort=False).round(2).to_string())


if __name__ == "__main__":
    main()
