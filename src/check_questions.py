"""Validate eval/questions.csv against the extracted corpus.  Run:  python -m src.check_questions

Catches the annotation mistakes that silently ruin an evaluation: quotes that do not exist,
wrong question types, unanswerable questions that have evidence, missing dev/test split, duplicate ids.
"""

import csv
import sys
from collections import Counter
from pathlib import Path

from src.corpus import load_units
from src.evidence import resolve_evidence

TYPES = {
    "single_hop",
    "multi_hop",
    "unanswerable",
    "conflicting_or_conditional",
    "numeric_or_table",
}
SPLITS = {"dev", "test"}
COLUMNS = ["id", "split", "type", "question", "gold_answer", "gold_evidence", "notes"]


def check_rows(rows: list[dict], units_by_id: dict[str, dict]) -> list[str]:
    problems, seen = [], set()
    for line_no, r in enumerate(rows, start=2):  # line 1 is the header
        where = f"line {line_no} ({r.get('id', '?')})"
        if r["id"] in seen:
            problems.append(f"{where}: duplicate id")
        seen.add(r["id"])
        if r["type"] not in TYPES:
            problems.append(f"{where}: type must be one of {sorted(TYPES)}")
        if r["split"] not in SPLITS:
            problems.append(f"{where}: split must be dev or test")
        if not r["question"].strip():
            problems.append(f"{where}: empty question")
        evidence = r["gold_evidence"].strip()
        if r["type"] == "unanswerable":
            if evidence:
                problems.append(
                    f"{where}: unanswerable questions must have empty gold_evidence"
                )
            continue
        if not evidence:
            problems.append(f"{where}: missing gold_evidence")
            continue
        try:
            spans = resolve_evidence(evidence, units_by_id)
        except ValueError as e:
            problems.append(f"{where}: {e}")
            continue
        if r["type"] == "multi_hop" and len(spans) < 2:
            problems.append(f"{where}: multi_hop needs at least 2 evidence pieces")
    return problems


def main(csv_path: str = "eval/questions.csv") -> int:
    units = load_units(*sorted(Path("data/processed").glob("*.jsonl")))
    units_by_id = {u["unit_id"]: u for u in units}
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            print(f"missing columns: {missing}")
            return 1
        rows = list(reader)

    problems = check_rows(rows, units_by_id)
    print(
        f"{len(rows)} questions | types: {dict(Counter(r['type'] for r in rows))} | splits: {dict(Counter(r['split'] for r in rows))}"
    )
    for p in problems:
        print("PROBLEM:", p)
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
