"""Tests for the experiment plumbing. They use a stand-in selector and a fake embedder, so they run
without your select_within_budget and without downloading a model; they check the glue."""

import zlib

import numpy as np

from src.analysis_utils import lexical_overlap
from src.corpus import Chunk, build_chunks
from src.dense import truncation_rate
from src.evidence import resolve_evidence
from src.inspect_question import format_ranking
from src.retrievers import build_retrievers
from src.run_retrieval_eval import run_chunking

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


def fake_embed(texts):
    """Deterministic bag-of-words embedder (32 dims) so tests need no model."""
    out = np.zeros((len(texts), 32))
    for i, t in enumerate(texts):
        for w in t.lower().split():
            out[i, zlib.crc32(w.encode()) % 32] += 1
    return out


def question(qid, text, evidence, qtype="single_hop"):
    spans = resolve_evidence(evidence, BY_ID) if evidence else []
    ev = " ".join(BY_ID[s.unit_id]["text"][s.start : s.end] for s in spans)
    return {"id": qid, "split": "dev", "type": qtype, "question": text, "spans": spans, "evidence_text": ev}


def first_n(ranked, budget):  # stand-in selector: keep the first two chunks
    return ranked[:2]


def test_run_chunking_bm25_scores_a_hit_and_skips_unanswerable():
    qs = [
        question("q1", "breach notification deadline", "d:art:1::within 72 hours"),
        question("q2", "something absent", "", qtype="unanswerable"),
    ]
    rows = run_chunking(UNITS, qs, None, [1000], methods=["bm25"], selector=first_n)
    assert [r["qid"] for r in rows] == ["q1"]
    assert rows[0]["recall"] == 1.0 and rows[0]["rr"] == 1.0
    assert rows[0]["method"] == "bm25" and rows[0]["chunk_size"] == "article" and rows[0]["n_chunks"] == 2


def test_run_chunking_all_methods_and_budgets():
    qs = [question("q1", "erasure of personal data", "d:art:2::right to erasure")]
    rows = run_chunking(UNITS, qs, 40, [500, 1000], methods=["bm25", "dense", "hybrid"], embed_fn=fake_embed, selector=first_n)
    assert {(r["method"], r["budget_chars"]) for r in rows} == {(m, b) for m in ("bm25", "dense", "hybrid") for b in (500, 1000)}
    assert all(r["chunk_size"] == 40 and r["ctx_chars"] > 0 for r in rows)


def test_whole_article_chunks_are_bm25_only():
    qs = [question("q1", "erasure", "d:art:2::right to erasure")]
    rows = run_chunking(UNITS, qs, None, [1000], methods=["bm25", "dense", "hybrid"], embed_fn=fake_embed, selector=first_n)
    assert {r["method"] for r in rows} == {"bm25"}


def test_build_retrievers_without_embedder_gives_bm25_only():
    chunks = build_chunks(UNITS, None)
    assert list(build_retrievers(chunks, ["bm25", "dense", "hybrid"], None)) == ["bm25"]
    assert set(build_retrievers(chunks, ["bm25", "dense", "hybrid"], fake_embed)) == {"bm25", "dense", "hybrid"}


def test_truncation_rate():
    def embed(texts):
        return np.zeros((len(texts), 2))

    assert truncation_rate(["a"], embed) is None  # cannot be measured -> None, never an error
    embed.max_seq_length = 3
    embed.count_tokens = lambda texts: [len(t.split()) for t in texts]
    assert truncation_rate(["a b", "a b c d", "x y z w v"], embed) == 2 / 3

    def broken(texts):
        raise RuntimeError

    embed.count_tokens = broken
    assert truncation_rate(["a"], embed) is None


def test_format_ranking_marks_hits_and_context():
    spans = resolve_evidence("d:art:1::within 72 hours", BY_ID)
    ranked = [Chunk("d:art:2#0", "d:art:2", 0, 20, "other text"), Chunk("d:art:1#0", "d:art:1", 0, 99, "the right chunk")]
    out = format_ranking(ranked, spans, {"d:art:1#0"}).splitlines()
    assert "HIT" not in out[0] and "HIT" in out[1]
    assert "*" in out[1] and "*" not in out[0]


def test_lexical_overlap():
    assert lexical_overlap("breach notification", "notification of a breach") == 1.0
    assert lexical_overlap("breach notification", "unrelated words here") == 0.0
    assert lexical_overlap("the of and", "anything") == 0.0  # only stopwords
    assert 0 < lexical_overlap("breach deadline", "the breach occurred") < 1
