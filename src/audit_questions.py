"""Heuristic audit of the evaluation questions, mapped to the rule ids in eval/question_rules.md.

    python -m src.audit_questions                                  # audit eval/questions.csv
    python -m src.audit_questions drafts.csv --existing eval/questions.csv
    python -m src.audit_questions eval/questions.csv --check-quotas   # final 80-question set

ERROR lines must be fixed, WARN lines fixed or justified in notes, INFO lines are for the human reader.
Scripts cannot judge sufficiency, ambiguity or whether a question is really unanswerable: those need a reader
(see section 9 of the rules). This file only screens.
"""

import argparse
import csv
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from src.analysis_utils import content_tokens, lexical_overlap
from src.check_questions import check_rows
from src.corpus import load_units
from src.evidence import resolve_evidence

FIRST_AI_ID = 21  # ids from Q021 on are AI-drafted and held to the stricter checks
STRUCTURAL = re.compile(r"\b(?:articles?|art\.?|recitals?|annex(?:es)?|chapters?|sections?|paragraphs?|points?)\s*\(?\s*\d+", re.I)
ROMAN_REF = re.compile(r"\b(?:annex|chapter|article)\s+[ivxlc]+\b", re.I)
TELLTALE = re.compile(r"\b(exact|exactly|specific|specifically|precise|precisely|single|universal|universally)\b|maximum number of days", re.I)
QUOTAS = {
    "type": {"single_hop": 22, "multi_hop": 19, "unanswerable": 13, "conflicting_or_conditional": 13, "numeric_or_table": 13},
    "split": {"dev": 40, "test": 40},
    "doc": {"gdpr": 40, "ai_act": 40},
}


@dataclass
class Finding:
    severity: str  # ERROR | WARN | INFO
    rule: str
    qid: str
    message: str


def id_number(qid: str) -> int:
    m = re.match(r"Q(\d+)$", qid)
    return int(m.group(1)) if m else 0


def parse_notes(notes: str) -> tuple[str | None, set[str]]:
    """Return (doc tag or None, set of tags). Notes look like 'GDPR | free text | author:ai | hard_negative:gdpr:art:5'."""
    parts = [p.strip() for p in notes.split("|")]
    doc = {"GDPR": "gdpr", "AI_ACT": "ai_act"}.get(parts[0]) if parts else None
    return doc, set(parts[1:])


def numbers_in(text: str) -> set[str]:
    text = re.sub(r"(?<=\d)[ ,](?=\d{3}\b)", "", text)  # '20 000 000' and '20,000,000' -> '20000000'
    scale = {"million": 10**6, "billion": 10**9}
    text = re.sub(r"(\d+(?:\.\d+)?)\s*(million|billion)\b", lambda m: str(int(float(m.group(1)) * scale[m.group(2).lower()])), text, flags=re.I)
    return set(re.findall(r"\d+(?:\.\d+)?", text))


def jaccard(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if a | b else 0.0


def audit(rows: list[dict], units_by_id: dict, existing: list[dict] | None = None, check_quotas: bool = False):
    """Return (findings, summary). `rows` are the questions to audit; `existing` are older questions to compare with."""
    F: list[Finding] = []
    existing = existing or []
    existing_ids = {r["id"] for r in existing}

    def add(sev, rule, qid, msg):
        F.append(Finding(sev, rule, qid, msg))

    # format, quotes, types, split leakage: reuse the structural checker
    for p in check_rows(rows, units_by_id):
        add("ERROR", "R-F/R-S2", "-", p)

    spans, doc_of = {}, {}
    for r in rows:
        qid, new = r["id"], id_number(r["id"]) >= FIRST_AI_ID
        try:
            spans[qid] = resolve_evidence(r["gold_evidence"], units_by_id) if r["gold_evidence"].strip() else []
        except ValueError:
            spans[qid] = []  # already reported by check_rows
        note_doc, tags = parse_notes(r["notes"])
        span_docs = {s.unit_id.split(":")[0] for s in spans[qid]}
        doc_of[qid] = next(iter(span_docs)) if len(span_docs) == 1 else note_doc
        sev = "ERROR" if new else "WARN"

        if note_doc is None:
            add("ERROR", "R-F5", qid, "notes must start with 'GDPR | ' or 'AI_ACT | '")
        if new and not any(t.startswith("author:") for t in tags):
            add("ERROR", "R-F5", qid, "missing author tag (author:ai)")
        if new and r["type"] == "unanswerable" and not any(t.startswith("hard_negative:") for t in tags):
            add("ERROR", "R-F5/R-U1", qid, "unanswerable question needs a hard_negative:<unit_id> tag")

        q, words = r["question"].strip(), r["question"].split()
        if STRUCTURAL.search(q) or ROMAN_REF.search(q):
            add("WARN" if "explicit_ref" in tags else "ERROR", "R-Q1", qid, "question contains a provision number")
        if not q.endswith("?") or q.count("?") > 1:
            add("ERROR", "R-Q2", qid, "must be one sentence ending with a single '?'")
        if not 8 <= len(words) <= 40:
            add("WARN", "R-Q2", qid, f"{len(words)} words (allowed 8-40)")
        if r["type"] == "unanswerable":
            m = TELLTALE.search(q)
            if m:
                add(sev, "R-U2", qid, f"tell-tale word '{m.group()}' in an unanswerable question")
            if not r["gold_answer"].startswith("Not specified"):
                add(sev, "R-A5", qid, "unanswerable answer should start with 'Not specified'")
        if len(r["gold_answer"].split()) > 60:
            add("WARN", "R-A2", qid, f"gold_answer has {len(r['gold_answer'].split())} words (max 60)")

        sp = spans[qid]
        if not sp:
            continue
        ev_text = " ".join(units_by_id[s.unit_id]["text"][s.start : s.end] for s in sp)
        ov = lexical_overlap(q, ev_text)
        if ov > 0.8:
            add("ERROR", "R-Q3", qid, f"lexical overlap {ov:.2f} > 0.8: wording copied from the evidence")
        elif ov > 0.6:
            add("WARN", "R-Q3", qid, f"lexical overlap {ov:.2f} (0.6-0.8): paraphrase more")
        for s in sp:
            n = s.end - s.start
            if n > 600:
                add("ERROR", "R-E2", qid, f"quote of {n} characters in {s.unit_id} (max 600)")
            elif n > 400 or n < 25:
                add("WARN", "R-E2", qid, f"quote of {n} characters in {s.unit_id} (target 40-300)")
        if len({s.unit_id.split(":")[0] for s in sp}) > 1:
            add("ERROR", "R-E4", qid, "evidence pieces come from different regulations")
        if r["type"] == "multi_hop" and len(sp) >= 2:
            units_used = {s.unit_id for s in sp}
            if len(units_used) == 1 and max(s.start for s in sp) - min(s.end for s in sp) < 400:
                add("WARN", "R-E4", qid, "multi_hop pieces are in one unit less than 400 characters apart")
        if r["type"] == "conflicting_or_conditional" and len(sp) < 2:
            add("WARN", "R-E7", qid, "conditional question should quote the rule and the exception separately")
        if r["type"] == "numeric_or_table":
            missing = numbers_in(r["gold_answer"]) - numbers_in(ev_text)
            if missing:
                add("WARN", "R-E8", qid, f"numbers in gold_answer not found in the evidence: {sorted(missing)}")

    # unanswerable: first-pass screen only (final decision needs a reader)
    unit_tokens = None
    for r in rows:
        if r["type"] != "unanswerable":
            continue
        unit_tokens = unit_tokens or {uid: content_tokens(u["text"]) for uid, u in units_by_id.items()}
        qt = content_tokens(r["question"])
        if not qt:
            continue
        best = sorted(((len(qt & t) / len(qt), uid) for uid, t in unit_tokens.items()), reverse=True)[:3]
        add("INFO", "R-U1", r["id"], "nearest units by word overlap: " + ", ".join(f"{u} ({s:.2f})" for s, u in best))
        if best[0][0] >= 0.7:
            add("WARN", "R-U1", r["id"], f"{best[0][1]} shares {best[0][0]:.0%} of the question's content words: may be answerable")

    # reuse of units from the existing questions, and near-duplicates
    new_rows = [r for r in rows if r["id"] not in existing_ids]
    old_units = {}
    for r in existing:
        try:
            for s in (resolve_evidence(r["gold_evidence"], units_by_id) if r["gold_evidence"].strip() else []):
                old_units.setdefault(s.unit_id, r["id"])
        except ValueError:
            pass
    for r in new_rows:
        for s in spans.get(r["id"], []):
            if s.unit_id in old_units:
                add("ERROR", "R-B5", r["id"], f"{s.unit_id} is already the evidence of {old_units[s.unit_id]}")
    pool = [(r["id"], content_tokens(r["question"])) for r in rows + [e for e in existing if e["id"] not in {x["id"] for x in rows}]]
    for i, (a, ta) in enumerate(pool):
        for b, tb in pool[i + 1 :]:
            if jaccard(ta, tb) >= 0.6 and (a in {r["id"] for r in new_rows} or b in {r["id"] for r in new_rows}):
                add("WARN", "R-Q7", a, f"near-duplicate of {b} (word Jaccard {jaccard(ta, tb):.2f})")

    # set-level checks on the new rows (or on everything when no existing file is given)
    target = new_rows if existing else rows
    first_words = Counter(r["question"].split()[0].lower() for r in target if r["question"].split())
    if target and first_words.most_common(1)[0][1] / len(target) > 0.30:
        w, c = first_words.most_common(1)[0]
        add("WARN", "R-Q8", "-", f"{c} of {len(target)} questions start with '{w}' (max 30%)")
    answerable = [r for r in target if spans.get(r["id"])]
    if len(answerable) >= 20:
        low = sum(lexical_overlap(r["question"], " ".join(units_by_id[s.unit_id]["text"][s.start : s.end] for s in spans[r["id"]])) < 0.3 for r in answerable)
        if low / len(answerable) < 0.40:
            add("WARN", "R-Q3", "-", f"only {low}/{len(answerable)} questions have overlap below 0.3 (need 40%)")
        uses = Counter(s.unit_id for r in answerable for s in spans[r["id"]])
        if len(uses) < 20:
            add("WARN", "R-B4", "-", f"only {len(uses)} distinct evidence units (need 20)")
        for uid, n in uses.items():
            if n > 2:
                add("WARN", "R-B4", "-", f"{uid} is evidence of {n} spans (max 2)")
        rec_share = sum(any(":rec:" in s.unit_id for s in spans[r["id"]]) for r in answerable) / len(answerable)
        if rec_share < 0.20:
            add("WARN", "R-B4", "-", f"recital evidence share {rec_share:.0%} (need at least 20%)")
        late = 0
        for uid in uses:
            doc, kind, num = uid.split(":")
            if kind == "art" and int(num) >= (50 if doc == "gdpr" else 56):
                late += 1
        if late < 6:
            add("WARN", "R-B4", "-", f"only {late} evidence units from the second half of the document (need 6)")

    summary = {
        "type": Counter(r["type"] for r in rows),
        "split": Counter(r["split"] for r in rows),
        "doc": Counter(doc_of.get(r["id"]) for r in rows),
    }
    if check_quotas:
        for key, quota in QUOTAS.items():
            for k, want in quota.items():
                if summary[key].get(k, 0) != want:
                    add("ERROR", "R-B1-B3", "-", f"{key}={k}: have {summary[key].get(k, 0)}, quota {want}")
    return F, summary


def read_rows(path: str) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_path", nargs="?", default="eval/questions.csv")
    ap.add_argument("--existing", help="older question file to compare against (reuse of units, near-duplicates)")
    ap.add_argument("--check-quotas", action="store_true", help="enforce the final 80-question quotas")
    ap.add_argument("--hide-info", action="store_true")
    args = ap.parse_args()

    units = load_units(*sorted(Path("data/processed").glob("*.jsonl")))
    units_by_id = {u["unit_id"]: u for u in units}
    rows = read_rows(args.csv_path)
    existing = read_rows(args.existing) if args.existing else None
    findings, summary = audit(rows, units_by_id, existing, args.check_quotas)

    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    for f in sorted(findings, key=lambda f: (order[f.severity], f.qid, f.rule)):
        if f.severity == "INFO" and args.hide_info:
            continue
        print(f"{f.severity:<5} {f.rule:<10} {f.qid:<5} {f.message}")
    print(f"\n{len(rows)} questions | types {dict(summary['type'])} | splits {dict(summary['split'])} | docs {dict(summary['doc'])}")
    counts = Counter(f.severity for f in findings)
    print(f"{counts['ERROR']} error(s), {counts['WARN']} warning(s)")
    return 1 if counts["ERROR"] else 0


if __name__ == "__main__":
    sys.exit(main())
