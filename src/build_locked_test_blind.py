"""Export a GDPR blind-generation packet using the approved evidence ledger."""
import argparse
from collections import Counter
import csv
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from src.analysis_utils import STOPWORDS
from src.check_locked_test_quotas import PROTOCOL, expected_ids, quotas
from src.corpus import load_units

LEDGER = Path("eval/dev_pilot_p1/locked_test_evidence_usage_v3_1.csv")
RULES = Path("eval/question_rules.md")
GDPR = Path("data/processed/gdpr.jsonl")
AI_ACT = Path("data/processed/ai_act.jsonl")
GDPR_HTML = Path("data/raw/gdpr.html")
LEDGER_HEADER = ["unit_id", "permanent_exclusion", "new_test_question_count", "remaining_uses"]


def read_balances(path, corpus_ids):
    """Validate internal ledger consistency, then fill unused corpus units with two uses."""
    balances = {}
    permanent_count = 0
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        if reader.fieldnames != LEDGER_HEADER:
            raise ValueError("Unexpected evidence ledger header")
        for row in reader:
            uid, permanent, count, remaining = (row[key] for key in LEDGER_HEADER)
            if None in row or uid in balances or uid not in corpus_ids:
                raise ValueError(f"Invalid or duplicate evidence unit: {uid}")
            if permanent == "1" and count == "0" and remaining == "0":
                permanent_count += 1
            elif permanent != "0" or (count, remaining) not in {("1", "1"), ("2", "0")}:
                raise ValueError(f"Inconsistent evidence ledger counts for {uid}")
            balances[uid] = int(remaining)
    if permanent_count != 126:
        raise ValueError(f"Expected 126 permanent exclusions, got {permanent_count}")
    return {uid: balances.get(uid, 2) for uid in sorted(corpus_ids)}


def balance_csv(balances):
    stream = StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(["unit_id", "positive_uses_remaining"])
    writer.writerows((uid, n) for uid, n in balances.items() if uid.startswith("gdpr:"))
    return stream.getvalue().encode()


def generation_spec(protocol, batch, counts):
    ids = sorted(expected_ids(batch))
    bands = Counter()
    for (*_, band), n in counts.items():
        bands[band] += n
    cells = "\n".join(
        f"| {kind} | {evidence} | {band} | {n} |"
        for (_, _, kind, evidence, band), n in counts.items()
        if n
    )
    stopwords = " ".join(sorted(STOPWORDS))
    return f"""# Locked Test blind generation · {batch['id']} · {protocol['protocol_version']}

Generate only **{ids[0]}–{ids[-1]}**, exactly **{len(ids)} English GDPR questions** with CSV
split `test`, after the project owner starts the batch. Target **High {bands['high']} /
Low {bands['low']} / Unanswerable {bands['na']}**. Match each joint count below.
All omitted cells are zero. These counts govern this batch.

| Question type | Positive evidence | Overlap band | Count |
| --- | --- | --- | ---: |
{cells}

## Sources and evidence

- Use `question_rules.md` and the frozen `locked_test_quotas_v3.json`.
- Copy each gold quote exactly from `data/processed/gdpr.jsonl`; the quote must occur
  exactly once in its named unit. Use `data/raw/gdpr.html` to check the surrounding
  legal context. Use the GDPR text and `data/processed/ai_act.jsonl` to check genuine
  absence; positive evidence for this batch comes only from GDPR.
- `evidence_availability.csv` gives the positive-use balance for every GDPR unit.
  A balance of 0 forbids positive use, 1 allows at most one question, and 2 allows at
  most two questions. Count each question once per unit, including when several
  quotes come from that unit. A unit at balance 1 can be proposed for a distinct
  legal conclusion. The coordinator will privately check independence from existing
  items. Availability alone does not establish that a topic is distinct.
- Article-only multi-hop requires at least two **different Articles**. Mixed requires
  at least one necessary Article and one necessary Recital. Remove each evidence
  piece in turn and confirm that the full answer is lost. For a conditional item,
  separately cite the rule and the material condition or exception. For a numeric
  item, verify the value, unit, legal event and any qualification; use a Recital
  only if the operative text does not supply that fact.

High means unrounded lexical overlap ≥0.30, Low is <0.30, and unanswerable is N/A.
Tokenize the question and joined quote text (omit unit IDs) with `[a-z0-9]+` after
lowercasing. Keep unique tokens longer than one character and remove these stopwords.
Divide the number of shared tokens by the number of retained question tokens; if
that denominator is zero use zero.

```text
{stopwords}
```

## Unanswerable and output files

Leave gold evidence empty. Start the answer with `Not specified` and give the reason.
Use a single `absence_kind:a/b/c/d` tag with the actual letter, an existing GDPR
`hard_negative:<unit_id>`, and the following search tag. Include at least three
distinct variants and three inspected GDPR units, including the hard negative.
Across the full GDPR cohort all four kinds must be represented, with at most four
kind:d items. The coordinator checks those cumulative limits.

```text
search:variants=<comma-separated terms>; inspected=<comma-separated unit IDs>; missing=<absent fact and why the inspected units do not supply it>
```

- Return a UTF-8 CSV with exactly
  `id,split,type,question,gold_answer,gold_evidence,notes`. Use `unit_id::verbatim quote`
  for each span and separate spans with ` || `. Start notes with `GDPR | ` and retain
  separate `author:ai` and `human_review:pending` tags.
- Return generation metadata with provider, available model version, generation
  timestamp with timezone, available seed and settings, assigned IDs, exact prompt
  text or a versioned prompt reference with SHA-256, and input/output SHA-256 hashes.
  State any unavailable fields accurately. Report any unfilled cell for review
  instead of stretching legal claims or retaining unnecessary evidence.
"""


def build(batch_id, output):
    if output.suffix.lower() != ".zip":
        raise ValueError("Output must be a new ZIP path")
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    batch = next(b for b in protocol["regulations"]["gdpr"]["batches"] if b["id"] == batch_id)
    units = {u["unit_id"] for u in load_units(GDPR, AI_ACT)}
    availability = balance_csv(read_balances(LEDGER, units))
    rules = RULES.read_text(encoding="utf-8").split("## 3. Question text (R-Q)\n", 1)[1]
    excerpt = rules.split("## 7. Split rules (R-S)", 1)[0]
    counts = quotas("gdpr", batch["quota"])
    files = {
        str(p): p.read_bytes() for p in (GDPR, GDPR_HTML, AI_ACT)
    }
    files.update({
        PROTOCOL.name: PROTOCOL.read_bytes(),
        "evidence_availability.csv": availability,
        "blind_generation_spec.md": generation_spec(protocol, batch, counts).encode(),
        "question_rules.md": (
            "# Frozen question-writing rules · v3.1\n\n"
            "The batch specification governs exact quotas, distinct multi-hop source units, "
            "and cumulative absence limits. The GDPR is the only source of positive evidence.\n\n"
            "## 3. Question text (R-Q)\n" + excerpt
        ).encode(),
    })
    files["SHA256SUMS.txt"] = "".join(
        f"{sha256(content).hexdigest()}  {name}\n" for name, content in sorted(files.items())
    ).encode()
    with ZipFile(output, "x") as archive:
        for name, content in sorted(files.items()):
            archive.writestr(ZipInfo(name), content, compress_type=ZIP_DEFLATED)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", choices=("gdpr-04", "gdpr-05"), required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        build(args.batch, args.out)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
