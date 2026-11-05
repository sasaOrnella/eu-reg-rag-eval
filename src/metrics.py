"""Retrieval metrics.

CORE FUNCTIONS, written by you. See tests/test_metrics.py.

Terminology:
  retrieved_ids : list of chunk ids returned by the retriever, best first
  relevant_ids  : set of chunk ids that the gold evidence says should be found
"""


def recall_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float:
  
    if len(relevant_ids) == 0:
        return 0.0
    else:
        top_k = retrieved_ids[:k]
        top_k = set(top_k)
        matched = relevant_ids & top_k

        recall = len(matched) / len(relevant_ids)
    return recall


def reciprocal_rank(retrieved_ids: list[str], relevant_ids: set[str]) -> float:
    rr = 0.0
    for position, chunk_id in enumerate(retrieved_ids, start = 1):
        
        if chunk_id in relevant_ids:
            rr = 1/position
            break
    
    return rr


def bootstrap_ci(values: list[float], n_boot: int = 10000, alpha: float = 0.05, seed: int = 0):
    """Return (mean, lower, upper) of a percentile bootstrap confidence interval.

    Used later in the project: every reported number needs an interval.
    """
    # TODO(you): implement in week 5-6
    raise NotImplementedError
