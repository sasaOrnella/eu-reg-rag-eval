"""A working BM25 retrieval baseline (reference implementation, provided for you).

Read it line by line. Later you will write the dense and hybrid versions yourself,
following this structure.
"""

import re

from rank_bm25 import BM25Okapi


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class BM25Retriever:
    def __init__(self, chunk_ids: list[str], chunks: list[str]):
        assert len(chunk_ids) == len(chunks)
        self.chunk_ids = chunk_ids
        self.index = BM25Okapi([tokenize(c) for c in chunks])

    def search(self, query: str, k: int = 5) -> list[str]:
        scores = self.index.get_scores(tokenize(query))
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [self.chunk_ids[i] for i in ranked]
