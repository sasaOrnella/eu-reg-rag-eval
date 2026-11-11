from src.audit_questions import audit, numbers_in, parse_notes

UNITS = {
    "gdpr:art:1": {"text": "The controller shall pay 20 000 000 EUR within 72 hours of the breach.", "unit_id": "gdpr:art:1"},
    "gdpr:art:2": {"text": "A processor shall keep records of all processing activities carried out.", "unit_id": "gdpr:art:2"},
    "gdpr:art:3": {"text": "Data subjects may object to processing for direct marketing purposes.", "unit_id": "gdpr:art:3"},
    "ai_act:art:1": {"text": "Providers of general-purpose models shall publish a summary of training content.", "unit_id": "ai_act:art:1"},
}


def row(qid="Q030", q="How soon must a company act after losing customer records?", qtype="single_hop", ev="gdpr:art:1::within 72 hours",
        ans="Within 72 hours.", split="dev", notes="GDPR | test | author:ai"):
    return {"id": qid, "split": split, "type": qtype, "question": q, "gold_answer": ans, "gold_evidence": ev, "notes": notes}


def rules(findings, severity=None):
    return {(f.rule, f.severity) for f in findings if severity is None or f.severity == severity}


def test_clean_row_has_no_errors():
    f, _ = audit([row()], UNITS)
    assert not rules(f, "ERROR")


def test_structural_reference_is_an_error_unless_tagged():
    f, _ = audit([row(q="What does Article 33 require after a breach happens to a company?")], UNITS)
    assert ("R-Q1", "ERROR") in rules(f)
    f, _ = audit([row(q="What does Article 33 require after a breach happens to a company?", notes="GDPR | x | author:ai | explicit_ref")], UNITS)
    assert ("R-Q1", "WARN") in rules(f)


def test_roman_numeral_reference():
    f, _ = audit([row(q="Which systems listed in Annex III count as risky for a deployer to use?")], UNITS)
    assert ("R-Q1", "ERROR") in rules(f)


def test_question_must_end_with_single_question_mark():
    f, _ = audit([row(q="Tell me how soon a company must act after a breach.")], UNITS)
    assert ("R-Q2", "ERROR") in rules(f)


def test_copied_wording_is_flagged():
    f, _ = audit([row(q="Does the controller pay 20 000 000 EUR within 72 hours of the breach?", ev="gdpr:art:1::The controller shall pay 20 000 000 EUR within 72 hours of the breach.")], UNITS)
    assert ("R-Q3", "ERROR") in rules(f)


def test_unanswerable_rules_for_new_questions():
    bad = row(q="What is the exact number of days a company may keep video recordings?", qtype="unanswerable", ev="", ans="Nothing.", notes="GDPR | x | author:ai")
    f, _ = audit([bad], UNITS)
    r = rules(f, "ERROR")
    assert ("R-U2", "ERROR") in r and ("R-A5", "ERROR") in r and ("R-F5/R-U1", "ERROR") in r


def test_unanswerable_rules_are_only_warnings_for_old_questions():
    old = row(qid="Q009", q="What is the exact number of days a company may keep video recordings?", qtype="unanswerable", ev="", ans="Nothing.", notes="GDPR | old")
    f, _ = audit([old], UNITS)
    assert ("R-U2", "WARN") in rules(f) and ("R-U2", "ERROR") not in rules(f)


def test_numeric_answer_must_match_evidence():
    f, _ = audit([row(qtype="numeric_or_table", ans="It is 30 days.")], UNITS)
    assert ("R-E8", "WARN") in rules(f)
    f, _ = audit([row(qtype="numeric_or_table", ans="Within 72 hours.")], UNITS)
    assert ("R-E8", "WARN") not in rules(f)


def test_reuse_of_existing_unit_is_an_error():
    old = [row(qid="Q001", ev="gdpr:art:1::within 72 hours", notes="GDPR | old")]
    new = [row(qid="Q030", ev="gdpr:art:1::20 000 000 EUR")]
    f, _ = audit(new, UNITS, existing=old)
    assert ("R-B5", "ERROR") in rules(f)


def test_near_duplicate_questions():
    a = row(qid="Q030", q="How soon must a company notify the regulator about lost customer records?", ev="gdpr:art:1::within 72 hours")
    b = row(qid="Q031", q="How soon must a company notify the regulator about lost customer records quickly?", ev="gdpr:art:3::Data subjects may object")
    f, _ = audit([a, b], UNITS)
    assert any(x.rule == "R-Q7" for x in f)


def test_multi_hop_pieces_in_different_regulations_is_error():
    r = row(qtype="multi_hop", ev="gdpr:art:1::within 72 hours || ai_act:art:1::publish a summary")
    f, _ = audit([r], UNITS)
    assert ("R-E4", "ERROR") in rules(f)


def test_quota_check_reports_mismatch():
    f, summary = audit([row()], UNITS, check_quotas=True)
    assert any(x.rule == "R-B1-B3" for x in f) and summary["type"]["single_hop"] == 1


def test_helpers():
    assert numbers_in("fines up to 20 000 000 EUR or 4 %") == {"20000000", "4"}
    assert numbers_in("EUR 20 million or 4%") == {"20000000", "4"}  # 'million' is expanded so it matches '20 000 000'
    assert parse_notes("AI_ACT | text | author:ai | hard_negative:ai_act:art:5") == ("ai_act", {"text", "author:ai", "hard_negative:ai_act:art:5"})
