import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from cross_check import run_cross_check


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
