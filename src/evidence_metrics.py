"""Evidence-level retrieval metric. CORE FUNCTION, written by you.

Why this differs from metrics.recall_at_k:
  Chunk ids change whenever chunk size changes, so gold labels are spans (src/evidence.py),
  and we ask: how many gold evidence spans are covered by the top-k retrieved chunks?
  (If we instead counted 'fraction of relevant chunks', small chunk sizes would be punished
  just because one long evidence span is cut into many chunks.)
"""

from src.corpus import Chunk
from src.evidence import Span, chunk_overlaps  # noqa: F401  (chunk_overlaps is what you need)


def evidence_recall_at_k(retrieved: list[Chunk], gold_spans: list[Span], k: int
) -> float:
    if  k <= 0:
        raise ValueError
    if len(gold_spans) == 0 :
        return 0.0
    
    matched = 0
    for s in gold_spans:
        if any(chunk_overlaps(c, s) for c in retrieved[:k]):
            matched += 1
        
    return matched / len(gold_spans)


def first_hit_rank(retrieved: list[Chunk], gold_spans: list[Span]) -> int | None:
    """Rank (starting at 1) of the first retrieved chunk that overlaps ANY gold span, else None.

    This is the ingredient for MRR: reciprocal rank = 1/rank, or 0.0 when None.
    Provided for you.
    """
    for rank, c in enumerate(retrieved, start=1):
        if any(chunk_overlaps(c, s) for s in gold_spans):
            return rank
    return None
