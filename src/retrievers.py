"""Build the retrievers for one chunking, so the runner and the inspector share one code path."""

from src.bm25_baseline import BM25Retriever
from src.corpus import Chunk
from src.dense import BGE_QUERY_PREFIX, DenseRetriever
from src.hybrid import HybridRetriever

METHODS = ["bm25", "dense", "hybrid"]


def build_retrievers(chunks: list[Chunk], methods, embed_fn=None, pool: int = 50) -> dict:
    """Return {method: retriever} for the requested methods.

    Methods that need an embedder (dense, hybrid) are skipped when `embed_fn` is None.
    Hybrid is BM25 + dense fused with RRF, and reuses the two retrievers built here
    (so the corpus is embedded only once).
    """
    ids = [c.chunk_id for c in chunks]
    texts = [c.text for c in chunks]
    want_dense = embed_fn is not None and ("dense" in methods or "hybrid" in methods)

    bm25 = BM25Retriever(ids, texts) if ("bm25" in methods or (want_dense and "hybrid" in methods)) else None
    dense = DenseRetriever(ids, texts, embed_fn, query_prefix=BGE_QUERY_PREFIX) if want_dense else None

    out = {}
    if "bm25" in methods and bm25 is not None:
        out["bm25"] = bm25
    if "dense" in methods and dense is not None:
        out["dense"] = dense
    if "hybrid" in methods and bm25 is not None and dense is not None:
        out["hybrid"] = HybridRetriever([bm25, dense], pool=pool)
    return out
