"""Retrieval metrics.

CORE FUNCTIONS, written by you. See tests/test_metrics.py.

Terminology:
  retrieved_ids : list of chunk ids returned by the retriever, best first
  relevant_ids  : set of chunk ids that the gold evidence says should be found
"""


def recall_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float:

    if k <= 0:
        raise ValueError("k must be a positive integer!")

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
    for position, chunk_id in enumerate(retrieved_ids, start=1):
        if chunk_id in relevant_ids:
            rr = 1 / position
            break

    return rr


import numpy as np
import random

def bootstrap_ci(
values: list[float], n_boot: int = 10000, alpha: float = 0.05, seed: int = 0
):
    if len(values) == 0:
        raise ValueError('values must not be empty!!')

    if n_boot == 0:
        raise ValueError('n_boot must be positive!!')

    if not 0 < alpha < 1:
        raise ValueError('alpha must be between 0 and 1!!')

    
    rng = random.Random(seed)
    boot_m = []

    for i in range(n_boot):
        sampling = rng.choices(values, k = len(values))
        avg = sum(sampling) / len(sampling)
        boot_m.append(avg)

    mean = sum(values) / len(values)

    lower = np.quantile(boot_m, alpha / 2)
    upper = np.quantile(boot_m, 1 - alpha / 2)

    return mean, lower, upper
