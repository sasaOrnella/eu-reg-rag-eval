"""Mechanical fixtures only. All text and evidence are synthetic placeholders."""
import json
from pathlib import Path

import pytest

from src.check_locked_test_quotas import PROTOCOL, audit_absence, quotas, validate


@pytest.fixture
def scaffolding():
    spec = json.loads(Path(PROTOCOL).read_text())
    units = {}
    def stub(qid, split, doc="gdpr"):
        return dict(id=f"Q{qid:03d}", split=split, type="unanswerable",
                    question=f"placeholder{qid}", gold_answer="Not specified for fixture.",
                    gold_evidence="", notes=f"{'GDPR' if doc=='gdpr' else 'AI_ACT'} | author:ai | human_review:pending")
    baseline = [stub(i,"dev" if i<=40 else "test") for i in range(1,81)]
    new_dev = [stub(i,"dev") for i in range(81,121)]
    additions = []
    serial = 1000
    for doc,reg in spec["regulations"].items():
        near = [f"{doc}:art:{i}" for i in (997,998,999)]
        units.update({uid:{"text":"placeholder"} for uid in near})
        absence = 0
        for batch in reg["batches"]:
            qid = batch["first_id"]
            for (_,_,kind,evidence,band),n in quotas(doc,batch["quota"]).items():
                for _ in range(n):
                    row = stub(qid,"test",doc)
                    tokens = [f"fixture{qid}token{i}" for i in range(8)]
                    row.update(type=kind,question=" ".join(tokens)+"?",gold_answer="Fixture answer.")
                    if band == "na":
                        row["gold_answer"] = "Not specified in this fixture because the field is absent."
                        row["notes"] += (f" | absence_kind:{'abcd'[absence%4]} | hard_negative:{near[0]}"
                                         f" | search:variants=first, second, third; inspected={', '.join(near)}; missing=fixture detail")
                        absence += 1
                    else:
                        sources = ["art","rec"] if evidence=="mixed" else (
                            ["art","art"] if kind=="multi_hop" else ["rec" if evidence=="recital_only" else "art"])
                        quotes = []
                        for source in sources:
                            serial += 1
                            uid = f"{doc}:{source}:{serial}"
                            quote = " ".join(tokens[:4]) if band=="high" else "unrelated placeholder"
                            extra = "condition placeholder"
                            units[uid] = {"text":f"{quote}\n{extra}"}
                            quotes.append(f"{uid}::{quote}")
                            if kind=="conflicting_or_conditional":
                                quotes.append(f"{uid}::{extra}")
                        row["gold_evidence"] = " || ".join(quotes)
                    additions.append(row)
                    qid += 1
    return spec,baseline,new_dev,additions,units


def test_partial_batch_and_preceding_batch_validation(scaffolding):
    spec,old,dev,new,units = scaffolding
    _, errors = validate(spec,old,dev,new[:1],units,("gdpr",),batch_id="gdpr-01")
    assert not errors
    _, errors = validate(spec,old,dev,new[18:19],units,("gdpr",),batch_id="gdpr-02",previous=new[:18])
    assert not errors
    _, errors = validate(spec,old,dev,new[18:19],units,("gdpr",),batch_id="gdpr-02")
    assert any("preceding" in e for e in errors)


def test_exact_cohort_90_and_joint_180(scaffolding):
    spec,old,dev,new,units = scaffolding
    for rows,docs in ((new[:90],("gdpr",)),(new,("gdpr","ai_act"))):
        table, errors = validate(spec,old,dev,rows,units,docs)
        assert not errors
        assert sum(row["expected"] for row in table) == len(rows)
    _, errors = validate(spec,old,dev,new[:-1],units,("gdpr","ai_act"))
    assert any("Quota mismatch" in error for error in errors)


def test_partial_catches_duplicates_reused_units_and_absence_tags(scaffolding):
    spec,old,dev,new,units = scaffolding
    old[-1] = dict(new[0],id=old[-1]["id"])
    _, errors = validate(spec,old,dev,new[:1],units,("gdpr",),batch_id="gdpr-01")
    assert any("duplicate question" in e for e in errors) and any("reserved units" in e for e in errors)
    sample = next(row.copy() for row in new if row["type"]=="unanswerable")
    sample["question"] = "What exact resource does the textual specification establish?"
    kind, errors = audit_absence(sample,["absence_kind:e","hard_negative:missing"],"gdpr",units,spec["unanswerable"])
    assert kind is None and all(any(label in e for e in errors) for label in ("absence_kind","hard_negative","search record","signal"))


def test_full_cohort_catches_kind_d_cap_and_missing_kind(scaffolding):
    spec,old,dev,new,units = scaffolding
    for row in new[:90]:
        if row["type"]=="unanswerable":
            row["notes"] = row["notes"].replace("absence_kind:a","absence_kind:d").replace("absence_kind:b","absence_kind:d")
    _, errors = validate(spec,old,dev,new[:90],units,("gdpr",))
    assert any("at most four" in e for e in errors) and any("all four" in e for e in errors)
