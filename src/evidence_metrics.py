"""Evidence-level retrieval metric. CORE FUNCTION, written by you.

Why this differs from metrics.recall_at_k:
  Chunk ids change whenever chunk size changes, so gold labels are spans (src/evidence.py),
  and we ask: how many gold evidence spans are covered by the top-k retrieved chunks?
  (If we instead counted 'fraction of relevant chunks', small chunk sizes would be punished
  just because one long evidence span is cut into many chunks.)
"""

from src.corpus import Chunk
from src.evidence import Span, chunk_overlaps  # noqa: F401  (chunk_overlaps is what you need)


def evidence_recall_at_k(retrieved: list[Chunk], gold_spans: list[Span], k: int) -> float:
    """Fraction of gold spans overlapped by at least one of the first k retrieved chunks.

    - `retrieved` is ordered best first.
    - Unanswerable questions have no gold spans: return 0.0 (evaluate them separately, see annotation guide).
    """
    # TODO(you): implement; tests/test_evidence_metrics.py shows the expected behaviour
    raise NotImplementedError


def first_hit_rank(retrieved: list[Chunk], gold_spans: list[Span]) -> int | None:
    """Rank (starting at 1) of the first retrieved chunk that overlaps ANY gold span, else None.

    This is the ingredient for MRR: reciprocal rank = 1/rank, or 0.0 when None.
    Provided for you.
    """
    for rank, c in enumerate(retrieved, start=1):
        if any(chunk_overlaps(c, s) for s in gold_spans):
            return rank
    return None
