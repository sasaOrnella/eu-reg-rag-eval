from itertools import product

import pandas as pd
import pytest

from src.analyze_dev import SIZES, analyze, bootstrap_test, holm, load_pilot
from src.replay_dev import covered_fraction
from src.corpus import Chunk
from src.evidence import Span
from src.run_retrieval_eval import BUDGETS, METHODS


def sample_grid():
    questions = [("Q001", .20), ("Q002", .30), ("Q003", .30)]
    return pd.DataFrame([
        dict(qid=qid, method=method, chunk_size=size, budget_chars=budget,
             split="dev", type="multi_hop", lexical_overlap=overlap,
             recall=.75 if size in (800, 1200) else .25)
        for (qid, overlap), method, size, budget in product(questions, METHODS, SIZES, BUDGETS)
    ])


def test_holm_adjusts_all_p_values_in_original_order():
    assert holm([.04, .01, .03, 1.0]).tolist() == pytest.approx([.09, .04, .09, 1])


def test_paired_contrast_and_cutoff_equality():
    frame = sample_grid().sample(frac=1, random_state=7)
    _, table = analyze(frame, "recall", {"Q001"}, n_boot=20)
    shape = table[table.contrast.eq("C: mid minus extremes")]
    assert shape.effect.eq(.5).all()
    assert shape.family_size.eq(18).all()
    margin = table[table.family.eq("H2a_high_margin") & table.overlap_threshold.eq(.30)]
    assert margin.n.eq(2).all()
    assert margin.null_effect.eq(-.05).all()
    assert margin.effect.eq(0).all()
    empty = table[table.family.eq("H2b_low") & table.cohort.eq("exclude_inspected")
                  & table.overlap_threshold.eq(.20)]
    assert not empty.empty and empty.status.eq("insufficient_pairs").all()
    assert empty.p_holm.isna().all()


@pytest.mark.parametrize("damage", ["duplicate", "missing", "other_split"])
def test_invalid_pilot_is_rejected(tmp_path, damage):
    frame = sample_grid()
    if damage == "duplicate":
        frame = pd.concat([frame, frame.iloc[:1]])
    elif damage == "missing":
        frame = frame.iloc[1:]
    else:
        frame.loc[0, "split"] = "other"
    path = tmp_path / "pilot.csv"
    frame.to_csv(path, index=False)
    with pytest.raises(ValueError):
        load_pilot(path, "recall")


def test_centered_bootstrap_respects_margin_and_direction():
    assert bootstrap_test([0, 0, 0], -.05, "greater", 99, 0) == .01
    assert bootstrap_test([0, 0, 0], .05, "greater", 99, 0) == 1.0
    assert bootstrap_test([0, 0, 0], 0, "two-sided", 99, 0) == 1.0


def test_span_coverage_is_union_in_the_same_unit():
    gold = Span("doc", 10, 30)
    chunks = [Chunk("a", "doc", 0, 16, ""), Chunk("b", "doc", 14, 20, ""),
              Chunk("c", "other", 0, 50, ""), Chunk("d", "doc", 30, 40, "")]
    assert covered_fraction(gold, chunks) == .5
    assert covered_fraction(gold, chunks[:1]) == .3
    assert covered_fraction(gold, chunks[2:]) == 0
