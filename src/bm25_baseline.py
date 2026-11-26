"""A working BM25 retrieval baseline (reference implementation, provided for you).

Read it line by line. Later you will write the dense and hybrid versions yourself,
following this structure.
"""

import re

from rank_bm25 import BM25Okapi

from src.tie_breaks import rank_scores


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class BM25Retriever:
    def __init__(self, chunk_ids: list[str], chunks: list[str], *, tie_order=None):
        assert len(chunk_ids) == len(chunks)
        self.chunk_ids = chunk_ids
        self.tie_order = tie_order
        self.index = BM25Okapi([tokenize(c) for c in chunks])

    def scores(self, query: str):
        return self.index.get_scores(tokenize(query))

    def search(self, query: str, k: int = 5) -> list[str]:
        return rank_scores(self.chunk_ids, self.scores(query), k, self.tie_order)
