"""Tests for the experiment plumbing. They use a stand-in selector so they pass before you write
select_within_budget; they check the glue, not your function."""

from src.analysis_utils import lexical_overlap
from src.evidence import resolve_evidence
from src.run_retrieval_eval import run_config

UNITS = [
    {
        "doc": "d", "kind": "article", "article": "1", "title": "", "unit_id": "d:art:1",
        "text": "The controller shall notify the supervisory authority of a personal data breach within 72 hours.",
    },
    {
        "doc": "d", "kind": "article", "article": "2", "title": "", "unit_id": "d:art:2",
        "text": "Every data subject has the right to erasure of personal data without undue delay.",
    },
]  # fmt: skip
BY_ID = {u["unit_id"]: u for u in UNITS}


def question(qid, text, evidence, qtype="single_hop"):
    spans = resolve_evidence(evidence, BY_ID) if evidence else []
    ev = " ".join(BY_ID[s.unit_id]["text"][s.start : s.end] for s in spans)
    return {"id": qid, "split": "dev", "type": qtype, "question": text, "spans": spans, "evidence_text": ev}


def first_n(ranked, budget):  # stand-in selector: keep the first two chunks
    return ranked[:2]


def test_run_config_scores_a_hit_and_skips_unanswerable():
    qs = [
        question("q1", "breach notification deadline", "d:art:1::within 72 hours"),
        question("q2", "something absent", "", qtype="unanswerable"),
    ]
    rows = run_config(UNITS, qs, chunk_size=None, budget_chars=1000, selector=first_n)
    assert [r["qid"] for r in rows] == ["q1"]  # unanswerable skipped
    assert rows[0]["recall"] == 1.0 and rows[0]["rr"] == 1.0
    assert rows[0]["chunk_size"] == "article" and rows[0]["n_chunks"] == 2


def test_run_config_records_context_size():
    qs = [question("q1", "erasure", "d:art:2::right to erasure")]
    rows = run_config(UNITS, qs, chunk_size=40, budget_chars=1000, selector=first_n)
    assert rows[0]["ctx_chars"] > 0 and rows[0]["chunk_size"] == 40


def test_lexical_overlap():
    assert lexical_overlap("breach notification", "notification of a breach") == 1.0
    assert lexical_overlap("breach notification", "unrelated words here") == 0.0
    assert lexical_overlap("the of and", "anything") == 0.0  # only stopwords
    assert 0 < lexical_overlap("breach deadline", "the breach occurred") < 1
