import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]
WS = ROOT.parent
WORKBOOK_PATH = WS / "HKIPO-MB2026Q1.xlsx"

from cross_check import run_cross_check


@unittest.skipUnless(WORKBOOK_PATH.exists(), "Requires local production dataset HKIPO-MB2026Q1.xlsx")
class CrossCheckTests(unittest.TestCase):
    def test_run_cross_check_all_companies(self):
        result = run_cross_check()
        self.assertEqual(result["total_companies"], 38)
        self.assertEqual(result["clean_companies"], 38)
        self.assertEqual(result["total_anomalies"], 0)
        self.assertTrue(all(r["status"] == "PASS" for r in result["results"]))

    def test_run_cross_check_single_company(self):
        result = run_cross_check(only=["6082.HK"])
        self.assertEqual(result["total_companies"], 1)
        self.assertEqual(result["clean_companies"], 1)
        self.assertEqual(result["results"][0]["code"], "6082.HK")
        self.assertEqual(result["results"][0]["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
