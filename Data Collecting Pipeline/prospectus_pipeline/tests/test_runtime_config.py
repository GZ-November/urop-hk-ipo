import sys
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
from run import load_cfg, read_companies
from market_panel import load_issuers


class RuntimeConfigTests(unittest.TestCase):
    def test_promptable_period_overrides_filter_issuers_and_isolate_outputs(self):
        cfg = load_cfg(period_start_override="2026-01-01", period_end_override="2026-01-31")
        companies = read_companies(cfg)
        self.assertTrue(companies)
        self.assertLess(len(companies), 38)
        self.assertEqual(cfg["dataset"]["cohort"], "2026 Q1")
        self.assertIn("datasets/HKIPO_2026-01-01_2026-01-31", str(cfg["paths"]["out"]))
        for company in companies:
            relevant_date = company["listing_date"] or company["prospectus_date"]
            self.assertGreaterEqual(relevant_date, date(2026, 1, 1))
            self.assertLessEqual(relevant_date, date(2026, 1, 31))

    def test_alternate_workbook_uses_all_rows_without_manual_date_config(self):
        workbook = ROOT / "tests" / "fixtures" / "mock_workbook.xlsx"
        cfg = load_cfg(workbook_override=str(workbook))
        companies = read_companies(cfg)
        self.assertEqual(len(companies), 2)
        dates = [d for company in companies for d in (company["listing_date"], company["prospectus_date"]) if d]
        self.assertEqual(cfg["dataset"]["period_start"], min(dates).isoformat())
        self.assertEqual(cfg["dataset"]["period_end"], max(dates).isoformat())
        self.assertIn("datasets/mock_workbook", str(cfg["paths"]["out"]))

    def test_reversed_period_is_rejected(self):
        with self.assertRaises(ValueError):
            load_cfg(period_start_override="2026-02-01", period_end_override="2026-01-01")

    def test_absolute_path_to_default_workbook_keeps_default_storage(self):
        workbook = ROOT.parent / "HKIPO-MB2026Q1.xlsx"
        cfg = load_cfg(workbook_override=str(workbook))
        self.assertEqual(cfg["dataset"]["id"], "HKIPO-MB2026Q1")
        self.assertEqual(cfg["paths"]["out"], ROOT / "out")

    def test_different_ranges_in_same_quarter_get_separate_state(self):
        january = load_cfg(period_start_override="2026-01-01", period_end_override="2026-01-31")
        february = load_cfg(period_start_override="2026-02-01", period_end_override="2026-02-28")
        self.assertNotEqual(january["dataset"]["id"], february["dataset"]["id"])
        self.assertNotEqual(january["state_dir"], february["state_dir"])

    def test_open_ended_period_infers_missing_endpoint_from_selected_workbook(self):
        workbook = ROOT / "tests" / "fixtures" / "mock_workbook.xlsx"
        after_jan_1 = load_cfg(workbook_override=str(workbook), period_start_override="2026-01-01")
        before_jan_5 = load_cfg(workbook_override=str(workbook), period_end_override="2026-01-05")

        self.assertEqual(after_jan_1["dataset"]["period_end"], "2026-01-08")
        self.assertEqual(before_jan_5["dataset"]["period_start"], "2026-01-02")
        self.assertEqual([c["code"] for c in read_companies(after_jan_1)], ["6082.HK", "2513.HK"])
        self.assertEqual([c["code"] for c in read_companies(before_jan_5)], ["6082.HK"])
        self.assertIn("2026-01-01_2026-01-08_mock_workbook", str(after_jan_1["paths"]["out"]))

    def test_market_issuers_use_configured_workbook_column_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            workbook_path = Path(tmp) / "alternate-layout.xlsx"
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "NLR"
            # Deliberately use different columns from the canonical template.
            sheet.append(["Name", "Offer", "List date", "Code", "File no", "Prospectus date"])
            sheet.append(["Example Issuer", 12.5, datetime(2026, 1, 10), "1234", 9, datetime(2026, 1, 3)])
            workbook.save(workbook_path)
            workbook.close()

            cfg = load_cfg(period_start_override="2026-01-01", period_end_override="2026-01-31")
            cfg["workbook"] = str(workbook_path)
            cfg["workbook_path"] = workbook_path
            cfg["_workbook_path"] = workbook_path
            cfg["id_columns"] = {
                "name": "A",
                "offer_price": "B",
                "listing_date": "C",
                "stock_code": "D",
                "file_no": "E",
                "prospectus_date": "F",
            }

            issuers = load_issuers(cfg=cfg)
            self.assertEqual(len(issuers), 1)
            self.assertEqual(issuers[0]["stock_code"], "1234.HK")
            self.assertEqual(issuers[0]["company_name"], "Example Issuer")
            self.assertEqual(issuers[0]["offer_price_hkd"], 12.5)


if __name__ == "__main__":
    unittest.main()
