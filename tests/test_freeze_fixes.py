from dataclasses import replace

import pandas as pd

from src.audit_dev_ties import tie_audit
from src.check_expansion_quotas import DOC_TAGS, EVIDENCE_TYPES, TARGETS, UNANSWERABLE, validate
from src.corpus import build_chunks
from src.hybrid import rrf
from src.pilot_inference import PRIMARY_BOOTSTRAPS, continuous_overlap_dev
from src.tie_breaks import content_order, rank_scores


def test_content_tie_order_independent_of_labels_and_input_order():
    units = [
        dict(unit_id="ai_act:art:1", text="sameAAAAABBBBB"),
        dict(unit_id="gdpr:art:1", text="sameCCCCCDDDDD"),
    ]
    chunks = build_chunks(units, 4)
    first_chunks = [chunk for chunk in chunks if chunk.start == 0]
    renamed = [replace(c, chunk_id=f"new-{i}", unit_id=f"unit-{i}")
               for i, c in enumerate(first_chunks)]
    ids = [c.chunk_id for c in first_chunks]
    new_ids = [c.chunk_id for c in renamed]
    key = content_order(first_chunks)
    new_key = content_order(renamed[::-1])
    assert [key[cid] for cid in ids] == [new_key[cid] for cid in new_ids]
    baseline = rank_scores(ids, [1., 1.], 2, key)
    assert rank_scores(ids[::-1], [1., 1.], 2, key) == baseline
    assert rrf([[ids[0]], [ids[1]]], tie_order=key) == baseline
    assert rank_scores(ids, [2., 1.], 2, key) == ids
    stats = next(tie_audit(dict.fromkeys(ids, 1.), ids, ids[::-1], baseline, (1,)))
    assert stats["cutoff_tie"] and stats["reverse_swaps"] == 1


def test_continuous_overlap_reports_slope_per_tenth():
    scores = pd.DataFrame([
        dict(qid=qid, budget_chars=8000, method=method, recall=value if method == "bm25" else .2)
        for qid, value in {"q1": .3, "q2": .4, "q3": .5}.items()
        for method in ("bm25", "dense")
    ])
    overlaps = pd.Series({"q1": .1, "q2": .2, "q3": .3})
    effect = continuous_overlap_dev(scores, overlaps, {"q1": "c1", "q2": "c1", "q3": "c2"}, n_boot=100)
    assert PRIMARY_BOOTSTRAPS == 200_000
    assert abs(effect["effect"] - .1) < 1e-12
    assert effect["n_clusters"] == 2
    assert 0 < effect["defined_draws"] <= 100


def test_joint_quota_detects_high_missing_in_one_evidence_cell():
    old, new = [], []
    def add(target, tag, split, kind, evidence, high):
        doc = DOC_TAGS[tag]
        quotes = {"article_only": f"{doc}:art:1::breach",
                  "recital_only": f"{doc}:rec:1::breach",
                  "mixed": f"{doc}:art:1::breach || {doc}:rec:1::notify", "none": ""}
        target.append(dict(id=str(len(old)+len(new)), notes=tag, split=split, type=kind,
                           question="breach" if high else "protection",
                           gold_evidence=quotes[evidence]))
    for tag in DOC_TAGS:
        for split, types in TARGETS.items():
            for _ in range(20):
                add(old, tag, split, "single_hop", "article_only", True)
            for kind, (totals, floors) in types.items():
                for evidence, total, floor in zip(EVIDENCE_TYPES, totals, floors):
                    for i in range(total):
                        add(new, tag, split, kind, evidence, i < floor)
            for _ in range(UNANSWERABLE[split]):
                add(new, tag, split, "unanswerable", "none", False)
    audit, errors = validate(old, new)
    assert not errors and len(audit) == 56
    new[0]["question"], new[2]["question"] = "protection", "breach"
    # Swap overlap labels across article/recital while keeping the marginal counts.
    new[4]["question"], new[1]["question"] = "breach", "protection"
    _, errors = validate(old, new)
    assert any("single_hop/article_only" in error for error in errors)
