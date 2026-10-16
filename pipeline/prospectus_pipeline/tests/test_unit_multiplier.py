"""Financial-statement unit inference for the disclosure-note column (CG/BS)."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src"), str(ROOT / "tools")]

from derive_disclosure_notes import infer_multiplier  # noqa: E402


def rec(key, value, quote):
    return {"fields": {key: {"value": value, "quote": quote}}}


class UnitMultiplierTests(unittest.TestCase):
    # 2675.HK: 6M2025 revenue 149,383 (RMB in thousands), annualised to 298,766,000.
    STUB = rec("col_AH", 298_766_000, "Revenue 48,042 159,994 30,245 149,383")

    def test_annualised_stub_no_longer_mimics_ten_thousands(self):
        # 298,766,000 / 30,245 = 9,878: within the old 2% tolerance of 10,000.
        self.assertIsNone(infer_multiplier(self.STUB, "col_AH"))

    def test_de_annualised_value_finds_the_reporting_unit(self):
        self.assertEqual(infer_multiplier(self.STUB, "col_AH", 298_766_000 * 0.5), 1000)

    def test_figures_reported_in_units_and_millions(self):
        self.assertEqual(infer_multiplier(
            rec("col_AH", 635_456_675, "Revenue 4(a) 360,106,324 463,738,031 635,456,675"), "col_AH"), 1)
        self.assertEqual(infer_multiplier(
            rec("col_Y", 38_923_000_000, "Total assets 32,906 35,222 36,094 38,923"), "col_Y"), 1000000)


if __name__ == "__main__":
    unittest.main()
