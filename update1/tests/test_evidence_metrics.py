from src.corpus import Chunk
from src.evidence import Span
from src.evidence_metrics import evidence_recall_at_k, first_hit_rank

S1 = Span("u1", 10, 20)
S2 = Span("u2", 0, 5)


def chunk(unit, start, end):
    return Chunk(f"{unit}#{start}", unit, start, end, "")


def test_both_spans_covered():
    top = [chunk("u1", 0, 15), chunk("u2", 0, 30)]
    assert evidence_recall_at_k(top, [S1, S2], k=2) == 1.0


def test_one_span_covered():
    assert evidence_recall_at_k([chunk("u1", 0, 15), chunk("u3", 0, 9)], [S1, S2], k=2) == 0.5


def test_k_cuts_the_list():
    top = [chunk("u3", 0, 9), chunk("u1", 0, 15)]
    assert evidence_recall_at_k(top, [S1], k=1) == 0.0
    assert evidence_recall_at_k(top, [S1], k=2) == 1.0


def test_two_chunks_covering_one_span_count_once():
    top = [chunk("u1", 0, 15), chunk("u1", 14, 30)]
    assert evidence_recall_at_k(top, [S1], k=2) == 1.0


def test_no_gold_spans_returns_zero():
    assert evidence_recall_at_k([chunk("u1", 0, 15)], [], k=1) == 0.0


def test_first_hit_rank():
    top = [chunk("u3", 0, 9), chunk("u2", 0, 30)]
    assert first_hit_rank(top, [S1, S2]) == 2
    assert first_hit_rank(top, [S1]) is None
