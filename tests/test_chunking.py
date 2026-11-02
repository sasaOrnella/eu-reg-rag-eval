import pytest

from src.chunking import chunk_text


def test_empty_text():
    assert chunk_text("") == []


def test_short_text_single_chunk():
    assert chunk_text("hello", chunk_size=10, overlap=2) == ["hello"]


def test_chunks_have_max_size():
    chunks = chunk_text("a" * 1000, chunk_size=300, overlap=50)
    assert all(len(c) <= 300 for c in chunks)


def test_overlap_between_consecutive_chunks():
    text = "abcdefghijklmnopqrstuvwxyz"
    chunks = chunk_text(text, chunk_size=10, overlap=3)
    assert chunks[0][-3:] == chunks[1][:3]


def test_last_part_not_skipped():
    text = "abcdefghijklmnopqrstuvwxyz"
    chunks = chunk_text(text, chunk_size=10, overlap=3)
    assert chunks[-1].endswith("z")


def test_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_text("abc", chunk_size=10, overlap=10)
