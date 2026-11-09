import numpy as np

from src.dense import DenseRetriever
from src.hybrid import HybridRetriever, rrf


def fake_embed(texts):
    """Toy embedder: 3 dimensions counting the words 'breach', 'erasure', 'risk'."""
    keys = ["breach", "erasure", "risk"]
    return np.array([[t.lower().count(k) for k in keys] for t in texts], dtype=float)


def test_dense_ranks_by_cosine():
    r = DenseRetriever(
        ["a", "b", "c"], ["breach breach", "erasure", "risk"], fake_embed
    )
    assert r.search("breach", k=2)[0] == "a"
    assert r.search("erasure", k=1) == ["b"]


def test_dense_k_larger_than_corpus():
    r = DenseRetriever(["a", "b"], ["breach", "erasure"], fake_embed)
    assert len(r.search("breach", k=10)) == 2


def test_dense_query_prefix_is_applied():
    seen = []

    def spy(texts):
        seen.extend(texts)
        return fake_embed(texts)

    r = DenseRetriever(["a"], ["breach"], spy, query_prefix="Q: ")
    r.search("breach")
    assert seen[-1] == "Q: breach" and seen[0] == "breach"


def test_rrf_rewards_agreement():
    assert rrf([["a", "b", "c"], ["b", "a", "d"]])[:2] == [
        "a",
        "b",
    ]  # exact tie, broken by id
    fused = rrf([["x", "a"], ["y", "a"]])
    assert (
        fused[0] == "a"
    )  # 'a' is second in both lists and beats the single first places


def test_rrf_is_deterministic_on_ties():
    assert rrf([["b"], ["a"]]) == ["a", "b"]


class Fixed:
    def __init__(self, ranking):
        self.ranking = ranking

    def search(self, query, k=5):
        return self.ranking[:k]


def test_hybrid_combines_two_retrievers():
    h = HybridRetriever([Fixed(["a", "b", "c"]), Fixed(["d", "b", "e"])], pool=3)
    assert h.search("q", k=1) == [
        "b"
    ]  # b is 2nd in both lists, beating the single first places
    assert len(h.search("q", k=10)) == 5
