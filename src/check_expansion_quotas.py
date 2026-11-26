"""Check prospective quotas from question annotations alone, before retrieval."""
import argparse
import csv
from collections import Counter
from pathlib import Path

from src.analysis_utils import lexical_overlap

DOC_TAGS = {"GDPR": "gdpr", "AI_ACT": "ai_act"}
# Per answerable type: ((article only, recital only, mixed), minimum High in each).
TARGETS = {
    "dev": {
        "single_hop": ((4, 1, 0), (2, 0, 0)),
        "multi_hop": ((3, 0, 2), (1, 0, 1)),
        "conflicting_or_conditional": ((3, 1, 0), (1, 0, 0)),
        "numeric_or_table": ((3, 1, 0), (1, 1, 0)),
    },
    "test": {
        "single_hop": ((9, 2, 0), (4, 1, 0)),
        "multi_hop": ((8, 0, 3), (3, 0, 1)),
        "conflicting_or_conditional": ((4, 2, 0), (2, 1, 0)),
        "numeric_or_table": ((4, 2, 0), (1, 1, 0)),
    },
}
EVIDENCE_TYPES = ("article_only", "recital_only", "mixed")
UNANSWERABLE = {"dev": 2, "test": 6}


def classify(row):
    tag = row["notes"].split("|", 1)[0].strip()
    doc, split, question_type = DOC_TAGS[tag], row["split"], row["type"]
    if question_type == "unanswerable":
        if row["gold_evidence"].strip():
            raise ValueError(f"{row['id']}: unanswerable question has gold evidence")
        return doc, split, question_type, "none", "na"
    kinds, quotes = set(), []
    for piece in row["gold_evidence"].split("||"):
        source, sep, quote = piece.partition("::")
        unit = source.strip().split(":")
        if not sep or not quote.strip() or len(unit) != 3 or unit[0] != doc or unit[1] not in {"rec", "art"}:
            raise ValueError(f"{row['id']}: expected evidence from {doc} with article or recital IDs")
        kinds.add(unit[1])
        quotes.append(quote.strip())
    evidence = "mixed" if len(kinds) == 2 else "article_only" if "art" in kinds else "recital_only"
    overlap = "high" if lexical_overlap(row["question"], " ".join(quotes)) >= .30 else "low"
    return doc, split, question_type, evidence, overlap


def validate(old_rows, new_rows):
    rows = old_rows + new_rows
    if len({r["id"] for r in rows}) != len(rows):
        raise ValueError("Question IDs must be unique across cohorts")
    old = Counter(map(classify, old_rows))
    new = Counter(map(classify, new_rows))
    errors = []
    audit = []
    merged = old + new
    for key in old.keys() | new.keys():
        doc, split, kind, _, _ = key
        if split not in TARGETS or kind not in (TARGETS[split].keys() | {"unanswerable"}):
            errors.append(f"Unexpected stratum: {doc}/{split}/{kind}")
    for doc in DOC_TAGS.values():
        for split, targets in TARGETS.items():
            prefix = (doc, split)
            for kind, (totals, floors) in targets.items():
                low_total = 0
                for evidence, total, high_floor in zip(EVIDENCE_TYPES, totals, floors):
                    high = new[(*prefix, kind, evidence, "high")]
                    low = new[(*prefix, kind, evidence, "low")]
                    low_total += low
                    audit.append(dict(doc=doc, split=split, type=kind, evidence=evidence, high=high,
                                      low=low, total=high+low, target=total, high_floor=high_floor))
                    if high + low != total or high < high_floor:
                        errors.append(f"{prefix}/{kind}/{evidence}: total {high+low}/{total}, High {high} (min {high_floor})")
                if low_total == 0:
                    errors.append(f"{prefix}/{kind}: at least one Low is required")
            observed = new[(*prefix, "unanswerable", "none", "na")]
            target = UNANSWERABLE[split]
            audit.append(dict(doc=doc, split=split, type="unanswerable", evidence="none",
                              high="", low="", total=observed, target=target, high_floor=""))
            if observed != target:
                errors.append(f"{prefix}: unanswerable {observed}/{target}")
            total = sum(v for key, v in merged.items() if key[:2] == prefix)
            high = sum(v for key, v in merged.items() if key[:2] == prefix and key[-1] == "high")
            expected = 40 if split == "dev" else 60
            audit.append(dict(doc=doc, split=split, type="merged_all", evidence="all",
                              high=high, low=sum(v for key, v in merged.items()
                                                 if key[:2] == prefix and key[-1] == "low"),
                              total=total, target=expected, high_floor=(35 * expected + 99) // 100))
            if total != expected or 100 * high < 35 * total:
                errors.append(f"{prefix}: merged total {total}/{expected}, High {high}/{total} (min 35%)")
    return audit, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old", type=Path, default=Path("eval/questions.csv"))
    parser.add_argument("--new", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.resolve() in {args.old.resolve(), args.new.resolve()}:
        parser.error("--out must not overwrite either input")
    try:
        with args.old.open(encoding="utf-8-sig") as old, args.new.open(encoding="utf-8-sig") as new:
            rows, errors = validate(list(csv.DictReader(old)), list(csv.DictReader(new)))
    except (KeyError, ValueError) as error:
        parser.error(str(error))
    with args.out.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
