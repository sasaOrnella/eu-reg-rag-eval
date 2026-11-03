"""Hybrid retrieval by Reciprocal Rank Fusion (RRF). Needs no training and no score calibration.

Each retriever returns a ranked list of chunk ids. A chunk's fused score is the sum over lists of
1 / (rrf_k + rank), so being near the top of ANY list helps, and being near the top of several helps most.
"""


def rrf(rankings: list[list[str]], rrf_k: int = 60) -> list[str]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, cid in enumerate(ranking, start=1):
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (rrf_k + rank)
    return sorted(scores, key=lambda c: (-scores[c], c))  # ties broken by id -> deterministic


class HybridRetriever:
    def __init__(self, retrievers: list, pool: int = 50, rrf_k: int = 60):
        self.retrievers = retrievers
        self.pool = pool  # how many candidates each retriever contributes before fusion
        self.rrf_k = rrf_k

    def search(self, query: str, k: int = 5) -> list[str]:
        rankings = [r.search(query, self.pool) for r in self.retrievers]
        return rrf(rankings, self.rrf_k)[:k]
