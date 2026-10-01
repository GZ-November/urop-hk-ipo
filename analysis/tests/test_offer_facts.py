"""Contracts for fixed-cutoff descriptive facts and financial timing."""
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import offer_facts_2026 as facts


class OfferFactsTests(unittest.TestCase):
    def test_ratio_excludes_unknown_and_nonpositive_denominators(self):
        result = facts.ratio(pd.Series([0., 1., np.nan, 2., 1.]), pd.Series([2., 0., 2., -1., np.inf]))
        self.assertEqual(result.iloc[0], 0)
        self.assertTrue(result.iloc[1:].isna().all())

    def test_missing_flag_is_not_negative_classification(self):
        result = facts.flag(pd.Series([-1., 0., np.nan]), lambda s: s < 0)
        self.assertEqual(result.iloc[:2].tolist(), [1., 0.])
        self.assertTrue(pd.isna(result.iloc[2]))

    def test_snapshot_and_financial_timing(self):
        d, metrics = facts.build_frame()
        self.assertEqual(len(d), 113)
        self.assertEqual(d["Stock Code"].nunique(), 113)
        self.assertTrue((d.listing_date <= facts.CUTOFF).all())
        self.assertTrue((d.listing_date.dt.year == 2026).all())
        pd.testing.assert_series_equal(
            d.net_margin, 100 * facts.ratio(d["Year-1 profit for period (original)"],
                                           d["Year-1 net sales (original, pre-annualization)"]), check_names=False)
        self.assertTrue(d.loc[d.fixed == 1, "revision"].isna().all())
        self.assertFalse(any("return" in k or "ir" == k or "bhar" in k for k in metrics))


if __name__ == "__main__":
    unittest.main()
