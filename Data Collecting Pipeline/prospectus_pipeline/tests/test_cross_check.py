import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]
WS = ROOT.parent
WORKBOOK_PATH = WS / "HKIPO-MB2026Q1.xlsx"
FIXTURE_WORKBOOK = ROOT / "tests" / "fixtures" / "mock_workbook.xlsx"

from cross_check import run_cross_check
from run import load_cfg


class CrossCheckTests(unittest.TestCase):
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
            result = run_cross_check(out_dir=tmp_dir)
            self.assertEqual(result["total_companies"], 38)
            self.assertEqual(result["clean_companies"], 38)
            self.assertEqual(result["total_anomalies"], 0)
            self.assertTrue(all(r["status"] == "PASS" for r in result["results"]))

    @unittest.skipUnless(WORKBOOK_PATH.exists(), "Requires local production dataset HKIPO-MB2026Q1.xlsx")
    def test_run_cross_check_single_company(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_cross_check(only=["6082.HK"], out_dir=tmp_dir)
            self.assertEqual(result["total_companies"], 1)
            self.assertEqual(result["clean_companies"], 1)
            self.assertEqual(result["results"][0]["code"], "6082.HK")
            self.assertEqual(result["results"][0]["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
