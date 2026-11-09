from src.bm25_baseline import BM25Retriever


def test_bm25_finds_matching_chunk():
    r = BM25Retriever(
        ["c1", "c2", "c3"],
        [
            "controller must notify breach within 72 hours",
            "right to erasure of personal data",
            "AI system risk classes",
        ],
    )
    assert r.search("notify breach", k=1) == ["c1"]
