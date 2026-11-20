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


def test_rrf_matches_hand_calculation_and_chunk_id_tie_break():
    from src.hybrid import rrf_scores
    from src.replay_dev import tie_statistics

    ai, gdpr, common = "ai_act:art:1#0", "gdpr:art:1#0", "gdpr:rec:2#0"
    rankings = [[ai, common, gdpr], [gdpr, common, ai]]
    expected = {ai: 1 / 61 + 1 / 63, gdpr: 1 / 61 + 1 / 63, common: 2 / 62}
    assert rrf_scores(rankings) == expected
    assert rrf(rankings) == [ai, gdpr, common]
    top_two = next(tie_statistics(rankings, 60, (2,)))
    assert top_two["tied_slots"] == 2
    assert not top_two["cutoff_tie"]
    top_one = next(tie_statistics(rankings, 60, (1,)))
    assert top_one["cutoff_tie"] and top_one["changed_members"] == 1
    assert top_one["ai_act_slots"] == 1 and top_one["ai_act_slots_reverse"] == 0
