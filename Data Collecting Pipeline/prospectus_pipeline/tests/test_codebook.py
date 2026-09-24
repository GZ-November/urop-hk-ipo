import csv
import sys
import tempfile
import unittest
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]
WS = ROOT.parent
WORKBOOK_PATH = WS / "HKIPO-MB2026Q1.xlsx"
FIXTURE_WORKBOOK = ROOT / "tests" / "fixtures" / "mock_workbook.xlsx"

from codebook import build_codebook, export_clean_csv, export_all
from run import load_cfg


def production_cfg() -> dict:
    """Return a config pinned to the canonical 2026 Q1 production workbook.

    A working checkout's ``config.yaml`` is repointed whenever a new cohort is
    being collected (for example ``HKIPO-MB2026Q2.xlsx``), so this test must pin
    the dataset it asserts on rather than inheriting the local checkout's target
    workbook.
    """
    cfg = load_cfg()
    cfg["workbook_path"] = WORKBOOK_PATH
    return cfg


class CodebookTests(unittest.TestCase):
    def test_build_codebook_with_mock_fixture(self):
        cfg = load_cfg()
        cfg["workbook_path"] = FIXTURE_WORKBOOK
        variables, summary = build_codebook(cfg)
        self.assertEqual(summary["sample_size"], 2)
        self.assertEqual(summary["variable_count"], 161)
        self.assertEqual(len(variables), 161)

        by_col = {item["col_letter"]: item for item in variables}
        self.assertEqual(by_col["BC"]["header"], "Comments / Annualization factor")
        self.assertEqual(by_col["CI"]["header"], "Year-3 financial period start")
        self.assertEqual(by_col["CL"]["header"], "Year-2 financial period end")
        self.assertEqual(by_col["CZ"]["header"], "Earliest cornerstone unlock date (dd/mm/yy)")

    def test_unknown_header_fails_instead_of_using_column_position(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            broken = Path(tmp_dir) / "unknown_header.xlsx"
            wb = openpyxl.load_workbook(FIXTURE_WORKBOOK)
            wb["NLR"].cell(1, 55).value = "Unregistered semantic field"
            wb.save(broken)
            wb.close()

            cfg = load_cfg()
            cfg["workbook_path"] = broken
            with self.assertRaisesRegex(ValueError, "未登记的工作簿表头"):
                build_codebook(cfg)

    def test_clean_csv_export_isolated(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            cfg = load_cfg()
            if not WORKBOOK_PATH.exists():
                cfg["workbook_path"] = FIXTURE_WORKBOOK
            variables, summary = build_codebook(cfg)
            out_csv = Path(tmp_dir) / "test_clean.csv"
            csv_path = export_clean_csv(variables, out_path=out_csv)
            self.assertTrue(csv_path.exists())
            self.assertEqual(csv_path, out_csv)

            with open(csv_path, mode="r", encoding="utf-8-sig") as f:
                reader = list(csv.reader(f))
                self.assertEqual(len(reader), summary["sample_size"] + 1)
                self.assertEqual(len(reader[0]), summary["variable_count"])
                self.assertEqual(reader[0][1], "Stock Code")
                stock_codes = [row[1] for row in reader[1:]]
                self.assertEqual(len(stock_codes), summary["sample_size"])
                self.assertTrue(all(code.endswith(".HK") for code in stock_codes))

    def test_export_all_artifacts_isolated(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            cfg = load_cfg()
            if not WORKBOOK_PATH.exists():
                cfg["workbook_path"] = FIXTURE_WORKBOOK
            res = export_all(cfg, out_dir=tmp_dir)
            expected_vars = 202 if WORKBOOK_PATH.exists() else 161
            self.assertEqual(res["variable_count"], expected_vars)
            self.assertTrue(Path(res["csv_path"]).exists())
            self.assertTrue(Path(res["md_path"]).exists())
            self.assertTrue(Path(res["json_path"]).exists())
            self.assertTrue(str(res["csv_path"]).startswith(tmp_dir))

            md_content = Path(res["md_path"]).read_text(encoding="utf-8")
            self.assertIn(f"{expected_vars} 维全量变量字典详细清单", md_content)
            self.assertIn(f"{res['sample_size']} 家", md_content)
            self.assertIn("浅绿", md_content)

    @unittest.skipUnless(WORKBOOK_PATH.exists(), "Requires local production dataset HKIPO-MB2026Q1.xlsx")
    def test_build_codebook_full_production_coverage(self):
        variables, summary = build_codebook(production_cfg())
        self.assertEqual(summary["sample_size"], 38)
        self.assertEqual(summary["variable_count"], 202)
        self.assertEqual(summary["tiers"]["green_hkex"], 11)
        self.assertEqual(summary["tiers"]["blue_prospectus"], 77)
        self.assertEqual(summary["tiers"]["darkblue_external"], 114)
        self.assertEqual(len(variables), 202)


if __name__ == "__main__":
    unittest.main()
