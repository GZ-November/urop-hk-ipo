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

from cross_check import mechanism_a_public_ratio, run_cross_check
from run import load_cfg


def production_cfg() -> dict:
    """Return a config pinned to the canonical 2026 Q1 production workbook.

    A working checkout's ``config.yaml`` is repointed whenever a new cohort is
    being collected (for example ``HKIPO-MB2026Q2.xlsx``), so these tests must
    pin the dataset they assert on rather than inheriting the local checkout's
    target workbook.
    """
    cfg = load_cfg()
    cfg["workbook_path"] = WORKBOOK_PATH
    return cfg


class CrossCheckTests(unittest.TestCase):
    def test_post_2025_mechanism_a_ladder(self):
        self.assertEqual(mechanism_a_public_ratio(14.99), 0.05)
        self.assertEqual(mechanism_a_public_ratio(15), 0.15)
        self.assertEqual(mechanism_a_public_ratio(50), 0.25)
        self.assertEqual(mechanism_a_public_ratio(100), 0.35)
        self.assertEqual(mechanism_a_public_ratio(9.99, is_18c=True), 0.05)
        self.assertEqual(mechanism_a_public_ratio(10, is_18c=True), 0.10)
        self.assertEqual(mechanism_a_public_ratio(50, is_18c=True), 0.20)

    def test_missing_semantic_header_does_not_fall_back_to_old_position(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            broken = Path(tmp_dir) / "moved_columns.xlsx"
            wb = openpyxl.load_workbook(FIXTURE_WORKBOOK)
            ws = wb["NLR"]
            for cell in ws[1]:
                if cell.value == "Offer mechanism":
                    cell.value = "Unknown allocation field"
                    break
            wb.save(broken)
            wb.close()

            cfg = load_cfg()
            cfg["workbook_path"] = broken
            with self.assertRaisesRegex(KeyError, "refusing positional fallback"):
                run_cross_check(cfg, out_dir=tmp_dir)

    def test_run_cross_check_with_mock_fixture(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            cfg = load_cfg()
            cfg["workbook_path"] = FIXTURE_WORKBOOK
            result = run_cross_check(cfg, out_dir=tmp_dir)
            self.assertEqual(result["total_companies"], 2)
            self.assertEqual(result["clean_companies"], 2)
            self.assertEqual(result["total_anomalies"], 0)
            self.assertTrue(all(r["status"] == "PASS" for r in result["results"]))
            self.assertTrue((Path(tmp_dir) / "cross_check_report.json").exists())
            self.assertTrue((Path(tmp_dir) / "cross_check_report.md").exists())

    @unittest.skipUnless(WORKBOOK_PATH.exists(), "Requires local production dataset HKIPO-MB2026Q1.xlsx")
    def test_run_cross_check_all_companies(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_cross_check(production_cfg(), out_dir=tmp_dir)
            self.assertEqual(result["total_companies"], 38)
            self.assertEqual(result["clean_companies"], 38)
            self.assertEqual(result["total_anomalies"], 0)
            self.assertTrue(all(r["status"] == "PASS" for r in result["results"]))

    @unittest.skipUnless(WORKBOOK_PATH.exists(), "Requires local production dataset HKIPO-MB2026Q1.xlsx")
    def test_run_cross_check_single_company(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_cross_check(production_cfg(), only=["6082.HK"], out_dir=tmp_dir)
            self.assertEqual(result["total_companies"], 1)
            self.assertEqual(result["clean_companies"], 1)
            self.assertEqual(result["results"][0]["code"], "6082.HK")
            self.assertEqual(result["results"][0]["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
