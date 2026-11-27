"""Audit partial or complete Locked Test annotations without running retrieval."""
import argparse
from collections import Counter
import csv
from itertools import combinations
import json
from pathlib import Path
import re

from src.analysis_utils import content_tokens
from src.audit_questions import TELLTALE, jaccard
from src.check_expansion_quotas import classify
from src.check_questions import COLUMNS, check_rows
from src.corpus import load_units
from src.evidence import resolve_evidence

PROTOCOL = Path("eval/dev_pilot_p1/locked_test_quotas_v3.json")
CANDIDATES = Path("eval/candidates")
SOURCES = (
    Path("eval/questions.csv"),
    CANDIDATES / "gdpr_dev_q081_q100_v2/outputs/gdpr_dev_candidates_v2.csv",
    CANDIDATES / "ai_act_dev_q101_q120_v2/outputs/ai_act_dev_candidates_v2.csv",
)


def read_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        if reader.fieldnames != COLUMNS:
            raise ValueError(f"Unexpected header: {path}")
        rows = list(reader)
    if any(None in row or any(v is None or "\n" in v or "\r" in v for v in row.values()) for row in rows):
        raise ValueError(f"Malformed CSV rows: {path}")
    return rows


def quotas(doc, cells):
    return Counter({
        (doc, "test", kind, evidence, band): n for kind, types in cells.items()
        for evidence, bands in types.items() for band, n in bands.items()
    })


def quota_table(expected, rows):
    observed = Counter(map(classify, rows))
    return [
        dict(regulation=doc, split=split, type=kind, evidence_type=evidence,
             overlap=overlap, expected=expected[key], actual=observed[key])
        for key in sorted(expected.keys() | observed.keys())
        for doc, split, kind, evidence, overlap in (key,)
    ]


def expected_ids(limits):
    return {f"Q{i:03d}" for i in range(limits["first_id"], limits["last_id"] + 1)}


def tagged(tags, key):
    return [value.strip() for name, _, value in (tag.partition(":") for tag in tags) if name == key]


def audit_absence(row, tags, doc, units, settings):
    """Validate the logged search and label shape. Absence itself needs legal review."""
    qid = row["id"]
    errors = []
    kinds = tagged(tags, "absence_kind")
    kind = kinds[0] if len(kinds) == 1 and kinds[0] in settings["absence_kinds"] else None
    if kind is None:
        errors.append(f"{qid}: expected exactly one absence_kind:a/b/c/d")
    hard = tagged(tags, "hard_negative")
    if len(hard) != 1 or hard[0] not in units or not hard[0].startswith(doc + ":"):
        errors.append(f"{qid}: expected exactly one valid same-regulation hard_negative unit")
    logs = tagged(tags, "search")
    pattern = r"variants=(?P<variants>[^;]+);\s*inspected=(?P<units>[^;]+);\s*missing=(?P<missing>.+)"
    log = re.fullmatch(pattern, logs[0]) if len(logs) == 1 else None
    if log:
        variants = {v.strip().casefold() for v in log["variants"].split(",") if v.strip()}
        inspected = {uid.strip() for uid in log["units"].split(",") if uid.strip()}
    if (not log or len(variants) < settings["min_variants"]
            or len(inspected) < settings["min_inspected_units"]
            or not all(uid in units and uid.startswith(doc + ":") for uid in inspected)
            or not set(hard) <= inspected or not log["missing"].strip()):
        errors.append(f"{qid}: missing or invalid search record (variants, inspected units, missing fact)")
    if TELLTALE.search(row["question"]):
        errors.append(f"{qid}: remove terms that signal the unanswerable class")
    if not re.match(r"^Not specified\b[\s\S]+\S",row["gold_answer"].strip()):
        errors.append(f"{qid}: unanswerable answer must start with 'Not specified' and explain why")
    return kind, errors


def duplicate_errors(baseline, rows):
    indexed = [(r, content_tokens(r["question"])) for r in baseline]
    errors = []
    for row in rows:
        question = row["question"]
        tokens = content_tokens(question)
        normalized = " ".join(re.findall(r"\w+",question.casefold()))
        for other, other_tokens in indexed:
            if normalized == " ".join(re.findall(r"\w+",other["question"].casefold())):
                errors.append(f"{row['id']} / {other['id']}: duplicate question text")
            elif jaccard(tokens, other_tokens) >= .60:
                errors.append(f"{row['id']} / {other['id']}: lexical near-duplicate needs review")
        indexed.append((row,tokens))
    return errors


def validate(spec, old, new_dev, proposed, units, documents, *, batch_id=None, previous=None):
    previous = previous or []
    all_new = previous + proposed
    if len(old) != 80 or Counter(r["split"] for r in old) != {"dev":40,"test":40}:
        raise ValueError("Expected frozen 40 Dev and 40 Test annotations")
    if len(new_dev) != 40 or any(r["split"] != "dev" for r in new_dev):
        raise ValueError("Expected 40 accepted new Dev annotations")
    errors = check_rows(old + new_dev + all_new, units)
    if errors:
        return [], errors
    if not proposed:
        errors.append("No proposed questions")
    if any(r["split"] != spec["split"] for r in all_new):
        errors.append("New Locked Test candidates must use split=test")
    batches = {b["id"]:(doc,b) for doc,reg in spec["regulations"].items() for b in reg["batches"]}
    if batch_id:
        doc,batch = batches[batch_id]
        target = quotas(doc,batch["quota"])
        if not {r["id"] for r in proposed} <= expected_ids(batch):
            errors.append(f"Proposed IDs must fall within {batch_id}")
        preceding = set(range(spec["regulations"][doc]["first_id"],batch["first_id"]))
        actual = {int(r["id"][1:]) for r in previous if re.fullmatch(r"Q[0-9]{3}",r["id"]) and classify(r)[0]==doc}
        if actual != preceding:
            errors.append(f"{batch_id}: supply all and only preceding batches of this regulation with --previous")
        for earlier_doc, earlier in batches.values():
            earlier_rows = [r for r in previous if r["id"] in expected_ids(earlier)]
            if earlier_rows and Counter(map(classify,earlier_rows)) != quotas(earlier_doc,earlier["quota"]):
                errors.append(f"{earlier['id']}: previous batch must be complete and match its joint quota")
    else:
        target = sum((quotas(doc,spec["regulations"][doc]["quota"]) for doc in documents),Counter())
        required = set.union(*(expected_ids(spec["regulations"][d]) for d in documents))
        if {r["id"] for r in proposed} != required:
            errors.append("Proposed IDs do not match the selected regulation ranges")
        for doc in documents:
            for b in spec["regulations"][doc]["batches"]:
                rows = [r for r in proposed if r["id"] in expected_ids(b)]
                if Counter(map(classify,rows)) != quotas(doc,b["quota"]):
                    errors.append(f"{b['id']}: exact batch cell counts do not match")
    table = quota_table(target,proposed)
    for row in table:
        if row["actual"] > row["expected"] or (not batch_id and row["actual"] != row["expected"]):
            errors.append(f"Quota mismatch: {row}")

    errors.extend(duplicate_errors(old+new_dev,all_new))
    reserved = {s.unit_id for r in old+new_dev for s in resolve_evidence(r["gold_evidence"],units)}
    use = Counter()
    later = Counter()
    kinds = {doc:Counter() for doc in spec["regulations"]}
    for row in all_new:
        qid = row["id"]
        doc, _, kind, _, _ = classify(row)
        ids = expected_ids(spec["regulations"][doc])
        if qid not in ids:
            errors.append(f"{qid}: outside the {doc} ID range")
        tags = [tag.strip() for tag in row["notes"].split("|")]
        if tags.count("author:ai") != 1 or tags.count("human_review:pending") != 1 or "verified:human" in tags:
            errors.append(f"{qid}: blind candidates require author:ai and human_review:pending")
        if any(uid not in units or not uid.startswith(doc+":") for uid in tagged(tags,"alt_evidence")):
            errors.append(f"{qid}: invalid same-regulation alt_evidence unit")
        if not 8 <= len(row["question"].split()) <= 40 or row["question"].count("?") != 1 or not row["question"].strip().endswith("?"):
            errors.append(f"{qid}: question must end in one question mark and contain 8–40 words")
        if not 1 <= len(row["gold_answer"].split()) <= 60:
            errors.append(f"{qid}: gold answer must contain 1–60 words")
        spans = resolve_evidence(row["gold_evidence"],units)
        unit_set = {s.unit_id for s in spans}
        if unit_set & reserved:
            errors.append(f"{qid}: positive evidence reuses reserved units {sorted(unit_set & reserved)}")
        use.update(unit_set)
        if any(not 1 <= s.end-s.start <= 600 for s in spans):
            errors.append(f"{qid}: evidence quote exceeds 600 characters")
        if kind == "single_hop" and len(spans) != 1:
            errors.append(f"{qid}: single-hop requires one quote")
        if kind == "multi_hop" and len(unit_set) < 2:
            errors.append(f"{qid}: multi-hop requires two distinct units")
        if kind == "conflicting_or_conditional" and len(set(spans)) < 2:
            errors.append(f"{qid}: conditional requires separate rule and condition or exception quotes")
        later[doc] += any(":art:" in uid and int(uid.rsplit(":",1)[-1]) >= (50 if doc=="gdpr" else 56) for uid in unit_set)
        if kind == "unanswerable":
            absence_kind, issues = audit_absence(row,tags,doc,units,spec["unanswerable"])
            if absence_kind:
                kinds[doc][absence_kind] += 1
            errors.extend(issues)
    errors.extend(f"{uid} used by {n} new Test questions" for uid,n in sorted(use.items())
                  if n > spec["max_questions_per_evidence_unit"])
    for doc, counts in kinds.items():
        if counts["d"] > spec["unanswerable"]["max_unspecified_quantity_per_regulation"]:
            errors.append(f"{doc}: at most four unspecified-quantity items")
        if not batch_id and doc in documents:
            if set(counts) != set(spec["unanswerable"]["absence_kinds"]):
                errors.append(f"{doc}: the complete cohort must include all four absence kinds")
            if later[doc] < 6:
                errors.append(f"{doc}: at least six questions must cite later articles")
    return table, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--new", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--regulation", choices=("gdpr", "ai_act", "both"), default="both")
    mode.add_argument("--batch", help="Validate an in-progress or complete 18-question batch")
    parser.add_argument("--previous", type=Path, action="append", default=[])
    args = parser.parse_args()
    if args.previous and not args.batch:
        parser.error("--previous requires --batch")
    if args.out.resolve() in {p.resolve() for p in (*SOURCES, PROTOCOL, args.new, *args.previous)}:
        parser.error("--out must not overwrite input files")
    spec = json.loads(PROTOCOL.read_text())
    documents = tuple(spec["regulations"]) if args.regulation == "both" else (args.regulation,)
    try:
        old,gdpr_dev,ai_dev = map(read_rows,SOURCES)
        proposed = read_rows(args.new)
        previous = [r for p in args.previous for r in read_rows(p)]
        units = {u["unit_id"]:u for u in load_units(*sorted(Path("data/processed").glob("*.jsonl")))}
        table,errors = validate(spec,old,gdpr_dev+ai_dev,proposed,units,documents,
                                batch_id=args.batch,previous=previous)
    except (KeyError,ValueError) as error:
        parser.error(str(error))
    if table:
        with args.out.open("w",encoding="utf-8",newline="") as stream:
            writer = csv.DictWriter(stream,fieldnames=table[0])
            writer.writeheader()
            writer.writerows(table)
    for error in errors:
        print(error)
    if not errors:
        scope = f"partial batch {args.batch}" if args.batch else "complete quota scope"
        print(f"Annotation checks passed for {scope}. Independent semantic review required.")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
