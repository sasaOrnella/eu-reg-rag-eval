"""Hybrid retrieval by Reciprocal Rank Fusion (RRF). Needs no training and no score calibration.

Each retriever returns a ranked list of chunk ids. A chunk's fused score is the sum over lists of
1 / (rrf_k + rank), so being near the top of ANY list helps, and being near the top of several helps most.
"""


def rrf_scores(rankings: list[list[str]], rrf_k: int = 60) -> dict[str, float]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, cid in enumerate(ranking, start=1):
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (rrf_k + rank)
    return scores


def rrf(rankings: list[list[str]], rrf_k: int = 60, *, tie_order=None) -> list[str]:
    scores = rrf_scores(rankings, rrf_k)
    return sorted(scores, key=lambda c: (-scores[c], c if tie_order is None else tie_order[c]))


class HybridRetriever:
    def __init__(self, retrievers: list, pool: int = 50, rrf_k: int = 60, *, tie_order=None):
        self.retrievers = retrievers
        self.pool = pool  # how many candidates each retriever contributes before fusion
        self.rrf_k = rrf_k
        self.tie_order = tie_order

    def search(self, query: str, k: int = 5) -> list[str]:
        rankings = [r.search(query, self.pool) for r in self.retrievers]
        return rrf(rankings, self.rrf_k, tie_order=self.tie_order)[:k]
