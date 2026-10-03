"""Publication-format fixtures check economic allocation quantities and quarantine."""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import allocation_tiers_2026 as tiers


def run_fixture(tmp_path, monkeypatch, code, pages, applicants, applied, allocated):
    monkeypatch.setattr(tiers, "ROOT", tmp_path)
    monkeypatch.setattr(tiers, "DATA", tmp_path / "source")
    monkeypatch.setattr(tiers, "OUT", tmp_path / "out")
    tiers.DATA.mkdir()
    (tiers.DATA / f"HKIPO-MB{code[:4]}.jsonl").write_text(
        "\n".join(json.dumps({"page": i + 1, "text": text}) for i, text in enumerate(pages)))
    panel = pd.DataFrame([{"Stock Code": code, "Company Name at time of listing": "fixture",
                           "Public applicants": applicants, "Public valid applied shares": applied,
                           "Final public offer shares": allocated}])
    monkeypatch.setattr(tiers, "load_panel", lambda: panel)
    monkeypatch.setattr(tiers, "select_2026", lambda d: d)
    tiers.main()
    assert not (tiers.OUT / "allocation_tiers_clean.csv").exists()
    return pd.read_csv(tiers.OUT / "allocation_tiers_candidates.csv"), pd.read_csv(tiers.OUT / "allocation_coverage.csv")


def test_guarantee_and_cross_page_ballot(tmp_path, monkeypatch):
    table, coverage = run_fixture(tmp_path, monkeypatch, "1111.HK", [
        "Pool A\n600\n10\n100 H Shares plus 2 out of 10 applicants to\n20.00%\n",
        "receive an additional 100 H Shares\nH Shares will be traded in board lots of 100 H Shares each."],
        10, 6000, 1200)
    row = table.iloc[0]
    assert row.guaranteed_shares == 100
    assert row.ballot_extra_shares == 100
    assert row.expected_shares == 120
    assert row.continuation_page == 2
    assert coverage.iloc[0].status == "totals_reconciled_pending_semantic_review"


def test_disclosed_outcome_counts_include_unsuccessful_applicants(tmp_path, monkeypatch):
    table, coverage = run_fixture(tmp_path, monkeypatch, "3636.HK", [
        "200\n90\n0 H Shares\n10.00%\n200\n10\n200 H Shares\n"
        "H Shares will be traded in board lots of 200 H Shares each."], 100, 20000, 2000)
    assert len(table) == 1
    assert table.iloc[0].applicants == 100
    assert table.iloc[0].guaranteed_shares == 0
    assert table.iloc[0].ballot_winners == 10
    assert table.iloc[0].expected_shares == 20
    assert coverage.iloc[0].applicants_extracted == 100


def test_conflicting_public_totals_are_quarantined(tmp_path, monkeypatch):
    _, coverage = run_fixture(tmp_path, monkeypatch, "1111.HK", [
        "Pool A\n100\n10\n2 out of 10 to receive 100 Shares\n20.00%\n"
        "Shares will be traded in board lots of 100 Shares each."], 10, 1000, 300)
    assert coverage.iloc[0].status == "quarantined_reconciliation"
