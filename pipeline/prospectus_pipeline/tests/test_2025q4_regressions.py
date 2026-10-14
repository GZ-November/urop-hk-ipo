"""Regressions found by the 2025Q4 Main Board + GEM collection run."""
import datetime as dt
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src"), str(ROOT / "tools"), str(ROOT / "tools" / "external")]

import periods  # noqa: E402
from cohort import load_cfg  # noqa: E402
from greenshoe import PATTERNS  # noqa: E402
from hkex import parse_doc_date  # noqa: E402
from validate import check_firm, traceability_warnings  # noqa: E402


def page(text, number=1):
    return {"page": number, "text": text}


class PeriodResolverTests(unittest.TestCase):
    def test_four_month_stub_is_year_one(self):
        tr = periods.resolve([page('"Track Record Period" the years ended December 31, 2022, 2023 and 2024 '
                                   "and the four months ended April 30, 2025")])
        self.assertEqual(tr.status, "ok")
        self.assertEqual((tr.year1.start, tr.year1.end, tr.year1.months),
                         (dt.date(2025, 1, 1), dt.date(2025, 4, 30), 4))
        self.assertEqual(tr.year2.end, dt.date(2024, 12, 31))
        self.assertEqual(tr.year3.end, dt.date(2023, 12, 31))

    def test_digit_and_hyphen_stub_forms(self):
        for phrase, months in (("5 months ended 31 May 2025", 5), ("seven-month period ended 31 July 2025", 7),
                               ("three months ended March 31,\n2024 2025", 3)):
            with self.subTest(phrase=phrase):
                tr = periods.resolve([page("CONSOLIDATED STATEMENTS OF PROFIT OR LOSS years ended "
                                           f"31 December 2022, 2023 and 2024 {phrase}")])
                self.assertEqual(tr.status, "ok", tr.reason)
                self.assertEqual(tr.year1.months, months)

    def test_march_fiscal_year_with_june_stub(self):
        tr = periods.resolve([page('"Track Record Period" the years ended 31 March 2023, 2024 and 2025 '
                                   "and the three months ended 30 June 2025")])
        self.assertEqual(tr.year1, periods.Period(dt.date(2025, 4, 1), dt.date(2025, 6, 30), 3))
        self.assertEqual(tr.year2, periods.Period(dt.date(2024, 4, 1), dt.date(2025, 3, 31), 12))

    def test_june_fiscal_year_is_not_a_stub(self):
        tr = periods.resolve([page('"Track Record Period" the years ended 30 June 2023, 2024 and 2025')])
        self.assertEqual(tr.year1, periods.Period(dt.date(2024, 7, 1), dt.date(2025, 6, 30), 12))

    def test_non_contiguous_stub_is_unresolved(self):
        tr = periods.resolve([page('"Track Record Period" the years ended 31 December 2023 and 2024 '
                                   "and the six months ended 31 July 2025")])
        self.assertEqual(tr.status, "unresolved")

    def test_payload_months_from_annualised_values(self):
        fields = {"col_AH": {"value": 53437000 * 12 / 9, "quote": "Revenue 3,460 30,523 19,454 53,437"},
                  "col_AN": {"value": -1000 * 4 * 1000, "quote": "Loss for the period (1,000)"}}
        self.assertIsNone(periods.payload_months({"col_AH": {"value": 5, "quote": "none"}}))
        self.assertEqual(periods.payload_months({"col_AH": fields["col_AH"]}), 9)


class ValidateGateTests(unittest.TestCase):
    STUB = periods.resolve([page('"Track Record Period" the years ended December 31, 2022, 2023 and 2024 '
                                 "and the four months ended April 30, 2025")])

    def test_period_anchor_rejects_last_full_year(self):
        rec = {"code": "2652.HK", "fields": {"col_AT": {"value": "31/12/24", "quote": "x"}}}
        issues = check_firm(rec, {"fields": []}, track_record=self.STUB)
        self.assertTrue(any(i["check"] == "期间锚定" for i in issues), issues)

    def test_period_anchor_accepts_stub_and_documented_override(self):
        ok = {"code": "2652.HK", "fields": {"col_AT": {"value": "30/04/25", "quote": "x"}}}
        self.assertEqual([i for i in check_firm(ok, {"fields": []}, track_record=self.STUB)
                          if i["check"] == "期间锚定"], [])
        override = {"code": "2652.HK", "fields": {"col_AT": {
            "value": "31/12/24", "quote": "x", "note": "period-override: p.12 stub is unaudited pro forma"}}}
        self.assertEqual([i for i in check_firm(override, {"fields": []}, track_record=self.STUB)
                          if i["check"] == "期间锚定"], [])

    def test_wrong_annualisation_is_rejected(self):
        rec = {"code": "2652.HK", "fields": {
            "col_AT": {"value": "30/04/25", "quote": "x"},
            "col_AH": {"value": 100_000 * 1000 * 2, "quote": "Revenue 100,000"}}}   # ×2 = 6M, should be ×3
        issues = check_firm(rec, {"fields": []}, track_record=self.STUB)
        self.assertTrue(any(i["check"] == "年化系数" for i in issues), issues)

    def test_scale_guard_accepts_scaled_small_capex(self):
        base = {"col_V": {"value": "RMB"}, "col_Y": {"value": 900_000_000},
                "col_AT": {"value": "31/12/24", "quote": "x"}}
        scaled = {"code": "2685.HK", "fields": {**base, "col_CG": {
            "value": 13_000, "quote": "Purchase of property, plant and equipment (13)"}}}
        unscaled = {"code": "2685.HK", "fields": {**base, "col_CG": {
            "value": 13, "quote": "Purchase of property, plant and equipment (13)"}}}
        self.assertFalse([i for i in check_firm(scaled, {"fields": []}) if "资本开支" in i["check"]])
        self.assertTrue([i for i in check_firm(unscaled, {"fields": []}) if "资本开支" in i["check"]])

    def test_back_solved_value_is_flagged_for_review(self):
        schema = {"fields": [{"key": "col_W", "unit": "basic_currency_units"}]}
        rec = {"code": "2581.HK", "fields": {"col_W": {
            "value": 1_234_567_000, "page": 5, "quote": "Total assets 1,100,000 1,200,000"}}}
        self.assertEqual(len(traceability_warnings(rec, schema)), 1)
        rec["fields"]["col_W"]["value"] = 1_200_000_000
        self.assertEqual(traceability_warnings(rec, schema), [])


class DeriveDisclosureNotesTests(unittest.TestCase):
    def test_three_month_stub_is_not_treated_as_full_fiscal_year(self):
        import derive_disclosure_notes as dn
        fields = {"col_AT": {"value": "31/03/26"},
                  "col_AH": {"value": 231_564_000 * 4, "quote": "Revenue 4 231,564 167,803"}}
        with tempfile.TemporaryDirectory() as tmp:
            result, basis = dn.year1_periods("0537.HK", fields, Path(tmp))
        self.assertEqual(basis, "payload_annualisation")
        self.assertEqual(result["year1"], periods.Period(dt.date(2026, 1, 1), dt.date(2026, 3, 31), 3))
        self.assertEqual(result["year2"].end, dt.date(2025, 12, 31))

    def test_conflicting_text_and_payload_are_skipped(self):
        import derive_disclosure_notes as dn
        fields = {"col_AT": {"value": "31/12/24"}, "col_AH": {"value": 100_000_000, "quote": "Revenue 100,000"}}
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "HKIPO-MB2652.jsonl").write_text(json.dumps(page(
                '"Track Record Period" the years ended December 31, 2022, 2023 and 2024 '
                "and the four months ended April 30, 2025")) + "\n", encoding="utf-8")
            result, reason = dn.year1_periods("2652.HK", fields, Path(tmp))
        self.assertIsNone(result)
        self.assertIn("期间锚定", reason)


class CollectionRegressionTests(unittest.TestCase):
    def test_cohort_period_exported_to_children_is_not_a_new_override(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
            base["dataset"].update({"id": "HKIPO_2025-10-01_2025-12-31_MB",
                                    "period_start": "2025-10-01", "period_end": "2025-12-31"})
            base["paths"] = {key: str(Path(tmp) / key) for key in base["paths"]}
            config = Path(tmp) / "cohort.yaml"
            config.write_text(yaml.safe_dump(base), encoding="utf-8")
            with patch.dict(os.environ, {"HKIPO_PERIOD_START": "2025-10-01",
                                         "HKIPO_PERIOD_END": "2025-12-31"}):
                cfg = load_cfg(config_path=config)
        self.assertEqual(cfg["paths"]["out"], Path(tmp) / "out")
        self.assertEqual(cfg["dataset"]["id"], "HKIPO_2025-10-01_2025-12-31_MB")

    def test_hkex_document_time_is_day_first(self):
        self.assertEqual(parse_doc_date("30/09/2025 06:18"), dt.date(2025, 9, 30))
        self.assertEqual(parse_doc_date("2025-09-30"), dt.date(2025, 9, 30))
        self.assertIsNone(parse_doc_date("None"))

    def test_greenshoe_share_class_prefix(self):
        text = "over-allotment option ... in respect of an aggregate of 1,082,800 Class A Shares"
        self.assertTrue(any(p.search(text) and p.search(text).group(1) == "1,082,800" for p in PATTERNS))

    def test_hsic_chinese_name_fallback_and_conflict(self):
        from hsic_codes import resolve_code
        tax = {"602020": {"name": "樓宇建造"}, "702030": {"name": "應用軟件"}}
        self.assertEqual(resolve_code({"hsic_sub": "Brand New Name", "hsic_sub_zh": "樓宇建造"}, tax),
                         ("602020", "official_chinese_name"))
        self.assertEqual(resolve_code({"hsic_sub": "Application Software"}, tax)[0], "702030")
        self.assertIsNone(resolve_code({"hsic_sub": "Application Software", "hsic_sub_zh": "樓宇建造"}, tax)[0])
        self.assertIsNone(resolve_code({"hsic_sub": "Unknown"}, tax)[0])


if __name__ == "__main__":
    unittest.main()
