import pytest

from src.budget import select_within_budget
from src.corpus import Chunk


def make(*lengths):
    return [Chunk(f"c{i}", "u", 0, n, "x" * n) for i, n in enumerate(lengths)]


def ids(chunks):
    return [c.chunk_id for c in chunks]


def test_keeps_chunks_that_fit():
    assert ids(select_within_budget(make(100, 100, 100), 250)) == ["c0", "c1"]


def test_exact_boundary_is_allowed():
    assert ids(select_within_budget(make(100, 100), 200)) == ["c0", "c1"]


def test_stops_at_first_chunk_that_does_not_fit():
    # c2 (50 chars) would fit, but c1 does not: we must not skip ahead to c2
    assert ids(select_within_budget(make(100, 300, 50), 200)) == ["c0"]


def test_first_chunk_is_kept_even_if_over_budget():
    assert ids(select_within_budget(make(500, 10), 100)) == ["c0"]


def test_empty_input():
    assert select_within_budget([], 100) == []


@pytest.mark.parametrize("bad", [0, -5])
def test_invalid_budget(bad):
    with pytest.raises(ValueError):
        select_within_budget(make(10), bad)
