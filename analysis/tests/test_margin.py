"""Tests for the margin-financing data validation."""
from pathlib import Path
import sys
import unittest

import pandas as pd

ANALYSIS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ANALYSIS))
import margin_financing_2026 as mf

SAMPLE = pd.DataFrame({"Stock Code": ["1.HK"], "Subscription opening date": ["2026-01-05"], "Subscription closing date": ["2026-01-09"]})


def rows(*items):
    return pd.DataFrame(items, columns=mf.REQUIRED)


class ValidationTests(unittest.TestCase):
    def test_valid_file_passes_and_summarizes(self):
        m = mf.validate(rows(("1.HK", "2026-01-05", 1e8, 10.0, "x"), ("1.HK", "2026-01-08", 3e8, 30.0, "x")), SAMPLE)
        out = mf.per_issuer(m)
        self.assertEqual(out.loc["1.HK", "final_multiple"], 30.0)
        self.assertEqual(out.loc["1.HK", "days"], 2)

    def test_rows_outside_subscription_period_unknown_issuers_and_falling_totals_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside the issuer's subscription"):
            mf.validate(rows(("1.HK", "2026-01-20", 1e8, 10.0, "x")), SAMPLE)
        with self.assertRaisesRegex(ValueError, "outside the 2026 sample"):
            mf.validate(rows(("9.HK", "2026-01-06", 1e8, 10.0, "x")), SAMPLE)
        with self.assertRaisesRegex(ValueError, "decrease"):
            mf.validate(rows(("1.HK", "2026-01-05", 3e8, 30.0, "x"), ("1.HK", "2026-01-08", 1e8, 10.0, "x")), SAMPLE)
        with self.assertRaisesRegex(ValueError, "lacks columns"):
            mf.validate(pd.DataFrame({"stock_code": ["1.HK"]}), SAMPLE)


if __name__ == "__main__":
    unittest.main()
