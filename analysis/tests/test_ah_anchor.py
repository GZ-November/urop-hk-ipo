"""Tests for sample composition and pre-event benchmark estimation."""
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ah_anchor_2026 as ah


class AnchorAnalysisTests(unittest.TestCase):
    def test_balanced_path_excludes_late_issuers_and_does_not_fill_holidays(self):
        panel = pd.DataFrame({"code": ["old", "old", "old", "late", "late"],
                              "event_day": [0, 1, 60, 0, 1], "gap": [-.4, -.3, -.2, -.9, -.8]})
        path = ah.balanced_path(panel)
        self.assertAlmostEqual(path.loc[0, "mean"], -.4)
        self.assertEqual(path.loc[60, "count"], 1)
        self.assertNotIn(2, path.index)

    def test_market_model_recovers_beta_without_using_event_or_gap_returns(self):
        rng = np.random.default_rng(13)
        index = pd.bdate_range("2025-01-01", periods=180)
        market = rng.normal(0, .01, len(index))
        returns = .001 + 1.5 * market
        returns[130:] += .2  # excluded gap, event and post-event observations
        frame = pd.DataFrame({"r": returns, "market": market}, index=index)
        residual, meta = ah.market_residuals(frame, index[150])
        self.assertEqual(meta["n_estimation"], 100)
        self.assertAlmostEqual(meta["beta"], 1.5)
        self.assertAlmostEqual(meta["alpha"], .001)
        self.assertAlmostEqual(residual.iloc[150], .2)
        _, short = ah.market_residuals(frame, index[40])
        self.assertTrue(np.isnan(short["beta"]))
