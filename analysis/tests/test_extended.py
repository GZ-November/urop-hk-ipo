"""Tests for the extended 2026 analysis helpers."""
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd

ANALYSIS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ANALYSIS))
import extended_analysis_2026 as ext
import research_inputs as inputs


class ScanTests(unittest.TestCase):
    def test_planted_level_shift_is_found_and_null_is_not_rejected(self):
        rng = np.random.default_rng(1)
        dates = pd.date_range("2026-01-01", periods=80, freq="D").to_numpy()
        y = rng.normal(0, 1, 80)
        y[30:55] += 3.0
        hit = ext.scan_test(y, dates, min_n=10, n_perm=300, seed=2)
        self.assertLess(hit["p"], 0.02)
        self.assertLessEqual(abs(hit["up"][0] - 30), 3)
        self.assertLessEqual(abs(hit["up"][1] - 55), 3)
        null = ext.scan_test(rng.normal(0, 1, 80), dates, min_n=10, n_perm=300, seed=2)
        self.assertGreater(null["p"], 0.05)

    def test_window_edges_respect_date_changes_and_minimum_size(self):
        dates = np.array(["2026-01-01"] * 5 + ["2026-01-02"] * 5 + ["2026-01-03"] * 10, dtype="datetime64[ns]")
        a, b = ext.window_grid(dates, 5)
        self.assertTrue(set(a) <= {0, 5, 10} and set(b) <= {5, 10, 20})
        self.assertTrue(((b - a >= 5) & (len(dates) - (b - a) >= 5)).all())


class VariableTests(unittest.TestCase):
    def test_prior_ir_never_uses_the_deal_itself_or_later_listings(self):
        listing = pd.Series(pd.to_datetime(["2026-01-05", "2026-01-10", "2026-01-15", "2026-01-20", "2026-02-01"]))
        ir = pd.Series([9.0, 0.1, 0.2, 0.3, 100.0])
        cutoff = pd.Series(pd.to_datetime(["2026-01-20", "2026-01-25", "2026-01-12", "2026-03-15"] + ["2026-01-25"]))
        out = inputs.prior_mean_ir(listing, ir, cutoff, days=30, min_deals=3)
        self.assertAlmostEqual(out.iloc[0], np.mean([9.0, 0.1, 0.2]))        # the 01-20 listing itself is excluded
        self.assertAlmostEqual(out.iloc[1], np.mean([9.0, 0.1, 0.2, 0.3]))   # the 02-01 listing is in the future
        self.assertTrue(np.isnan(out.iloc[2]))                                # fewer than three earlier deals
        self.assertTrue(np.isnan(out.iloc[3]))                                # everything older than 30 days

    def test_subscription_overlap_counts_others_only(self):
        start = pd.Series(pd.to_datetime(["2026-01-01", "2026-01-03", "2026-02-01"]))
        end = pd.Series(pd.to_datetime(["2026-01-05", "2026-01-08", "2026-02-05"]))
        self.assertEqual(inputs.subscription_overlap(start, end).tolist(), [1, 1, 0])


class InferenceTests(unittest.TestCase):
    def test_benjamini_hochberg_matches_hand_calculation(self):
        out = ext.bh_family([("s", "a", 0.01), ("s", "b", 0.04), ("s", "c", 0.03), ("s", "d", 0.5)])
        q = dict(zip(out["Test"], out["q (BH)"]))
        self.assertAlmostEqual(q["a"], 0.04)
        self.assertAlmostEqual(q["c"], 0.0533333, places=5)
        self.assertAlmostEqual(q["b"], 0.0533333, places=5)
        self.assertAlmostEqual(q["d"], 0.5)

    def test_out_of_sample_r2_is_zero_for_null_and_negative_for_noise(self):
        rng = np.random.default_rng(3)
        y = rng.normal(size=60)
        groups = np.repeat(np.arange(6), 10)
        self.assertEqual(ext.cv_r2(y, None, groups), 0.0)
        noise = rng.normal(size=(60, 8))
        self.assertLess(ext.cv_r2(y, noise, groups), 0.0)
        signal = np.c_[np.repeat(np.arange(6) % 2, 10)]
        self.assertGreater(ext.cv_r2(y + 3 * signal[:, 0], signal, groups), 0.3)

    def test_icc_detects_group_effect(self):
        rng = np.random.default_rng(4)
        groups = np.repeat(np.arange(8), 12)
        y = rng.normal(size=96) + np.repeat(rng.normal(0, 2, 8), 12)
        icc, _, p = ext.anova_icc(y, groups, n_perm=300, seed=5)
        self.assertGreater(icc, 0.3)
        self.assertLess(p, 0.02)


if __name__ == "__main__":
    unittest.main()
