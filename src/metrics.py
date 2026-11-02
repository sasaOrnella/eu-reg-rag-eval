"""Retrieval metrics.

CORE FUNCTIONS, written by you. See tests/test_metrics.py.

Terminology:
  retrieved_ids : list of chunk ids returned by the retriever, best first
  relevant_ids  : set of chunk ids that the gold evidence says should be found
"""


def recall_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float:
    """Fraction of relevant ids that appear in the top-k retrieved ids.

    If relevant_ids is empty (an 'unanswerable' question) return 0.0.
    """
    # TODO(you): implement
    raise NotImplementedError


def reciprocal_rank(retrieved_ids: list[str], relevant_ids: set[str]) -> float:
    """1 / rank of the first relevant id (rank starts at 1). 0.0 if none is retrieved."""
    # TODO(you): implement
    raise NotImplementedError


def bootstrap_ci(values: list[float], n_boot: int = 10000, alpha: float = 0.05, seed: int = 0):
    """Return (mean, lower, upper) of a percentile bootstrap confidence interval.

    Used later in the project: every reported number needs an interval.
    """
    # TODO(you): implement in week 5-6
    raise NotImplementedError
