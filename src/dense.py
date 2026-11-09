"""Dense (embedding) retrieval. Reference implementation, same shape as BM25Retriever.

The embedding function is injected, so the class can be tested without downloading a model.

Real use:
    embed = load_sentence_transformer("BAAI/bge-small-en-v1.5")
    r = DenseRetriever(ids, texts, embed, query_prefix=BGE_QUERY_PREFIX)

Notes
  * Small embedding models cap the input length (often 512 tokens, roughly 2000 characters).
    Longer chunks are silently truncated, which would make big-chunk results look worse than they are.
    Check `model.max_seq_length` and keep chunk sizes within it.
  * bge models expect an instruction prefix on QUERIES (not on documents).
"""

import numpy as np

BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


def load_sentence_transformer(model_name: str = "BAAI/bge-small-en-v1.5"):
    """Return embed(list[str]) -> np.ndarray (unit-length vectors). Needs `pip install sentence-transformers`."""
    from sentence_transformers import SentenceTransformer  # imported lazily: it is a heavy dependency

    model = SentenceTransformer(model_name)

    def embed(texts: list[str]) -> np.ndarray:
        return model.encode(texts, batch_size=64, normalize_embeddings=True, show_progress_bar=False)

    embed.max_seq_length = model.max_seq_length
    return embed


def _normalize(m: np.ndarray) -> np.ndarray:
    m = np.asarray(m, dtype=float)
    norms = np.linalg.norm(m, axis=-1, keepdims=True)
    return m / np.where(norms == 0, 1.0, norms)


class DenseRetriever:
    def __init__(self, chunk_ids: list[str], chunks: list[str], embed_fn, query_prefix: str = ""):
        assert len(chunk_ids) == len(chunks)
        self.chunk_ids = chunk_ids
        self.embed_fn = embed_fn
        self.query_prefix = query_prefix
        self.matrix = _normalize(embed_fn(chunks))

    def search(self, query: str, k: int = 5) -> list[str]:
        q = _normalize(self.embed_fn([self.query_prefix + query]))[0]
        scores = self.matrix @ q  # cosine similarity, since both sides are unit length
        order = np.argsort(-scores, kind="stable")[:k]
        return [self.chunk_ids[i] for i in order]
