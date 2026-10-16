"""A pre-IPO flag or stake of 0 needs a disclosed basis; NaN is the honest unknown."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from validate import check_firm, pre_ipo_evidence_issues  # noqa: E402


def fields(round_="NA", investors="NA", **values):
    out = {"col_earliest_round": {"value": round_}, "col_pre_ipo_investors": {"value": investors}}
    for key, value in values.items():
        out[key] = value if isinstance(value, dict) else {"value": value}
    return out


class PreIpoEvidenceTests(unittest.TestCase):
    def test_zero_without_any_basis_is_rejected(self):
        issues = pre_ipo_evidence_issues(fields(col_vc_backed=0, col_vc_pe_stake=0.0))
        self.assertEqual(len(issues), 2)
        self.assertTrue(all("无依据" in x for x in issues))

    def test_nan_is_the_accepted_unknown(self):
        self.assertEqual(pre_ipo_evidence_issues(fields(col_vc_backed="NaN", col_vc_pe_stake="NaN")), [])

    def test_explicit_no_pre_ipo_statement_allows_zero(self):
        self.assertEqual(pre_ipo_evidence_issues(fields(round_="None", investors="None", col_BA=0)), [])

    def test_named_investors_allow_a_classified_zero(self):
        self.assertEqual(pre_ipo_evidence_issues(
            fields(round_="Pre-IPO Investment", investors="Future Trade Network Limited",
                   col_vc_backed=0, col_holding_duration=1.28)), [])

    def test_zero_basis_note_allows_zero(self):
        stake = {"value": 0, "note": "zero-basis: pre-offering shares 100% held by BBSB Overseas (p264)"}
        self.assertEqual(pre_ipo_evidence_issues(fields(col_vc_pe_stake=stake)), [])

    def test_one_needs_a_named_investor_and_duration_a_named_round(self):
        issues = pre_ipo_evidence_issues(fields(col_gov_backed=1, col_holding_duration=0.0))
        self.assertEqual(len(issues), 2)
        self.assertIn("col_gov_backed=1", issues[0])
        self.assertIn("col_holding_duration", issues[1])

    def test_check_firm_reports_the_rule_as_an_error(self):
        rec = {"code": "0001.HK", "fields": fields(col_pe_backed=0)}
        checks = [x for x in check_firm(rec, {"fields": []}) if x["check"] == "上市前投资证据"]
        self.assertEqual(len(checks), 1)
        self.assertEqual(checks[0]["severity"], "error")


if __name__ == "__main__":
    unittest.main()
