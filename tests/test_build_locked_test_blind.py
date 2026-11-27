"""The coordinator's ledger is projected to a two-column blind availability table."""
import pytest

from src.build_locked_test_blind import LEDGER_HEADER, balance_csv, read_balances


@pytest.fixture
def ledger(tmp_path):
    source = tmp_path / "usage.csv"
    permanent = [f"gdpr:art:{n}" for n in range(1, 127)]
    source.write_text(
        ",".join(LEDGER_HEADER) + "\n"
        + "".join(f"{uid},1,0,0\n" for uid in permanent)
        + "gdpr:rec:1,0,2,0\ngdpr:rec:2,0,1,1\nai_act:rec:1,0,1,1\n"
    )
    return source, {*permanent, "gdpr:rec:1", "gdpr:rec:2", "gdpr:rec:3", "ai_act:rec:1"}


def test_blind_balances_include_unused_units_and_hide_history(ledger):
    source, units = ledger
    balances = read_balances(source, units)
    assert balances["gdpr:art:1"] == balances["gdpr:rec:1"] == 0
    assert balances["gdpr:rec:2"] == 1
    assert balances["gdpr:rec:3"] == 2
    text = balance_csv(balances).decode()
    assert text.splitlines()[0] == "unit_id,positive_uses_remaining"
    assert text.splitlines()[-3:] == ["gdpr:rec:1,0", "gdpr:rec:2,1", "gdpr:rec:3,2"]
    assert "ai_act:" not in text


@pytest.mark.parametrize("replacement", ["gdpr:rec:2,0,1,0", "gdpr:rec:2,0,3,0", "gdpr:rec:1,0,1,1"])
def test_blind_balances_reject_inconsistent_or_duplicate_rows(ledger, replacement):
    source, units = ledger
    source.write_text(source.read_text().replace("gdpr:rec:2,0,1,1", replacement))
    with pytest.raises(ValueError, match="evidence"):
        read_balances(source, units)
