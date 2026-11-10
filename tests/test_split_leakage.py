from src.check_questions import check_rows

UNITS = {
    "d:art:1": {"text": "alpha beta gamma delta", "unit_id": "d:art:1"},
    "d:art:2": {"text": "epsilon zeta eta theta", "unit_id": "d:art:2"},
}


def row(qid, split, evidence):
    return {"id": qid, "split": split, "type": "single_hop", "question": "?", "gold_answer": "a", "gold_evidence": evidence, "notes": ""}


def test_same_unit_in_both_splits_is_reported():
    rows = [row("q1", "dev", "d:art:1::alpha beta"), row("q2", "test", "d:art:1::gamma delta")]  # different spans, same unit
    problems = check_rows(rows, UNITS)
    assert len(problems) == 1 and "d:art:1" in problems[0]


def test_different_units_in_different_splits_is_fine():
    rows = [row("q1", "dev", "d:art:1::alpha"), row("q2", "test", "d:art:2::zeta")]
    assert check_rows(rows, UNITS) == []


def test_same_unit_twice_in_one_split_is_fine():
    rows = [row("q1", "dev", "d:art:1::alpha"), row("q2", "dev", "d:art:1::delta")]
    assert check_rows(rows, UNITS) == []
