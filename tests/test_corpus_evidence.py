import pytest

from src.check_questions import check_rows
from src.corpus import Chunk, build_chunks, make_unit_id
from src.evidence import Span, chunk_overlaps, resolve_evidence


def simple_chunker(text, size, overlap):
    """A correct stand-in for chunk_text, so these tests do not depend on your implementation."""
    step = size - overlap
    return (
        [text[i : i + size] for i in range(0, max(len(text) - overlap, 1), step)]
        if text
        else []
    )


UNITS = [
    {
        "doc": "gdpr",
        "kind": "article",
        "article": "33",
        "title": "",
        "text": "abcdefghijklmnopqrstuvwxyz",
        "unit_id": "gdpr:art:33",
    },
    {
        "doc": "gdpr",
        "kind": "recital",
        "number": "7",
        "title": "",
        "text": "short",
        "unit_id": "gdpr:rec:7",
    },
]
BY_ID = {u["unit_id"]: u for u in UNITS}


def test_make_unit_id():
    assert (
        make_unit_id({"doc": "ai_act", "kind": "article", "article": "5"})
        == "ai_act:art:5"
    )
    assert (
        make_unit_id({"doc": "gdpr", "kind": "recital", "number": "26"})
        == "gdpr:rec:26"
    )


def test_build_chunks_offsets_and_ids():
    chunks = build_chunks(UNITS, chunk_size=10, overlap=3, chunker=simple_chunker)
    first = [c for c in chunks if c.unit_id == "gdpr:art:33"]
    assert first[0].chunk_id == "gdpr:art:33#0" and (first[0].start, first[0].end) == (
        0,
        10,
    )
    assert (first[1].start, first[1].end) == (7, 17)
    assert all(UNITS[0]["text"][c.start : c.end] == c.text for c in first)


def test_build_chunks_whole_unit_baseline():
    chunks = build_chunks(UNITS, chunk_size=None)
    assert [c.chunk_id for c in chunks] == ["gdpr:art:33#0", "gdpr:rec:7#0"]
    assert chunks[0].text == UNITS[0]["text"]


def test_build_chunks_detects_bad_chunker():
    def stripping_chunker(text, size, overlap):
        return [c.strip("a") for c in simple_chunker(text, size, overlap)]

    with pytest.raises(AssertionError):
        build_chunks(UNITS, chunk_size=10, overlap=3, chunker=stripping_chunker)


def test_resolve_evidence_single_and_multiple():
    spans = resolve_evidence("gdpr:art:33::defgh || gdpr:rec:7::hor", BY_ID)
    assert spans == [Span("gdpr:art:33", 3, 8), Span("gdpr:rec:7", 1, 4)]


@pytest.mark.parametrize(
    "bad",
    ["no separator", "gdpr:art:99::abc", "gdpr:art:33::NOTTHERE", "gdpr:art:33::"],
)
def test_resolve_evidence_errors(bad):
    with pytest.raises(ValueError):
        resolve_evidence(bad, BY_ID)


def test_resolve_evidence_ambiguous_quote():
    units = {"u": {"text": "abab", "unit_id": "u"}}
    with pytest.raises(ValueError):
        resolve_evidence("u::ab", units)


def test_chunk_overlaps():
    span = Span("gdpr:art:33", 8, 12)
    assert chunk_overlaps(
        Chunk("c", "gdpr:art:33", 0, 9, ""), span
    )  # shares character 8
    assert not chunk_overlaps(
        Chunk("c", "gdpr:art:33", 0, 8, ""), span
    )  # ends exactly at the span start
    assert not chunk_overlaps(
        Chunk("c", "gdpr:art:33", 12, 20, ""), span
    )  # starts exactly at the span end
    assert not chunk_overlaps(Chunk("c", "gdpr:rec:7", 0, 20, ""), span)  # other unit


def test_check_rows_catches_problems():
    good = {
        "id": "q1",
        "split": "dev",
        "type": "single_hop",
        "question": "?",
        "gold_answer": "a",
        "gold_evidence": "gdpr:art:33::defgh",
        "notes": "",
    }
    assert check_rows([good], BY_ID) == []
    bad_type = dict(good, id="q2", type="whatever")
    unans_with_evidence = dict(good, id="q3", type="unanswerable")
    multi_one_piece = dict(good, id="q4", type="multi_hop")
    dup = dict(good)
    problems = check_rows(
        [good, bad_type, unans_with_evidence, multi_one_piece, dup], BY_ID
    )
    assert len(problems) == 4
