import pytest

from src.metrics import bootstrap_ci, recall_at_k, reciprocal_rank


def test_recall_all_found():
    assert recall_at_k(["a", "b", "c"], {"a", "b"}, k=3) == 1.0


def test_recall_partial():
    assert recall_at_k(["a", "x", "b"], {"a", "b"}, k=2) == 0.5


def test_recall_none_found():
    assert recall_at_k(["x", "y"], {"a"}, k=2) == 0.0


def test_recall_unanswerable_question():
    assert recall_at_k(["x", "y"], set(), k=2) == 0.0


def test_rr_first_position():
    assert reciprocal_rank(["a", "b"], {"a"}) == 1.0


def test_rr_third_position():
    assert reciprocal_rank(["x", "y", "a"], {"a"}) == pytest.approx(1 / 3)


def test_rr_not_found():
    assert reciprocal_rank(["x", "y"], {"a"}) == 0.0


@pytest.mark.skip(reason="Week 5-6: remove this line when you implement bootstrap_ci")
def test_bootstrap_ci_contains_mean():
    mean, lo, hi = bootstrap_ci([0.1, 0.5, 0.9, 0.4, 0.6], n_boot=2000)
    assert lo <= mean <= hi
