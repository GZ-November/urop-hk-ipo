"""Tests for the academic-extension helpers."""
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd

ANALYSIS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ANALYSIS))
import academic_extensions_2026 as ac


def frame(n=60, ex=0.0, turnover=100.0):
    idx = pd.bdate_range("2026-01-05", periods=n)
    return pd.DataFrame({"r": ex, "ex_hsi": ex, "ex_hstech": ex, "turnover": turnover}, index=idx)


class EventWindowTests(unittest.TestCase):
    def test_window_car_sums_excess_returns_and_requires_full_window(self):
        f = frame(40)
        f.loc[f.index[20], "ex_hsi"] = 0.05
        self.assertAlmostEqual(ac.window_car(f, 20, -1, 1), 0.05)
        self.assertTrue(np.isnan(ac.window_car(f, 38, -1, 5)))   # runs off the end
        self.assertTrue(np.isnan(ac.window_car(f, 3, -5, 5)))    # starts before the first return
        f.loc[f.index[21], "ex_hsi"] = np.nan
        self.assertTrue(np.isnan(ac.window_car(f, 20, -1, 1)))   # a missing return is never zero-filled

    def test_turnover_shock_is_log_ratio_and_missing_when_baseline_incomplete(self):
        f = frame(60, turnover=100.0)
        f.iloc[40:46, f.columns.get_loc("turnover")] = 200.0
        self.assertAlmostEqual(ac.turnover_shock(f, 40), np.log(2))
        self.assertTrue(np.isnan(ac.turnover_shock(f, 10)))      # fewer than 25 pre-event bars

    def test_event_index_uses_first_bar_on_or_after_the_date(self):
        f = frame(10)
        self.assertEqual(ac.event_index(f, pd.Timestamp("2026-01-10")), 5)  # Saturday -> Monday bar
        self.assertIsNone(ac.event_index(f, pd.Timestamp("2027-01-01")))

    def test_placebo_days_stay_near_but_outside_the_event(self):
        f = frame(120)
        seen = []
        ac.placebo_grid(f, 60, lambda fr, k: seen.append(k) or 0.0)
        self.assertTrue(all(ac.PLACEBO_EXCLUDE < abs(k - 60) <= ac.PLACEBO_NEAR for k in seen))
        self.assertTrue(min(seen) >= 6 and max(seen) <= len(f) - 6)


class InferenceTests(unittest.TestCase):
    def test_cross_t_matches_scipy_and_is_scale_free(self):
        rng = np.random.default_rng(0)
        v = rng.normal(0.02, 0.1, 40)
        from scipy import stats
        self.assertAlmostEqual(ac.cross_t(v), stats.ttest_1samp(v, 0).statistic)
        self.assertAlmostEqual(ac.cross_t(v * 5), ac.cross_t(v))

    def test_placebo_p_flags_a_true_shift_and_not_a_null_draw(self):
        rng = np.random.default_rng(1)
        grid = {f"s{i}": rng.normal(0, 0.05, 40) for i in range(30)}
        shifted = {c: 0.08 for c in grid}
        _, p_shift = ac.placebo_p(grid, shifted, ac.cross_t, n_draw=500, seed=2)
        self.assertLess(p_shift, 0.02)
        null = {c: float(rng.normal(0, 0.05)) for c in grid}
        _, p_null = ac.placebo_p(grid, null, ac.cross_t, n_draw=500, seed=2)
        self.assertGreater(p_null, 0.05)


class MoneyLeftTests(unittest.TestCase):
    def test_gain_split_adds_to_mlot_and_shares_add_to_one(self):
        d = pd.DataFrame({"base_shares": [1000.0, 2000.0], "retail_shares": [100.0, 200.0], "corner_shares": [300.0, 800.0],
                          "offer": [10.0, 20.0], "close1": [12.0, 18.0]})
        s = ac.money_left_split(d)
        mlot = 1000 * 2 + 2000 * -2
        self.assertAlmostEqual(sum(s["gain"].values()), mlot)
        self.assertAlmostEqual(sum(s["shares"].values()), 1.0)
        self.assertEqual(s["negative_other"], 0)

    def test_impossible_allocation_is_quarantined_never_capped_at_one(self):
        d = pd.DataFrame({"retail_shares": [500.0, 50.0, 0.0], "applied": [100.0, 100.0, 100.0], "ir": [0.5, 0.5, 0.5],
                          "close1": [15.0] * 3, "offer": [10.0] * 3, "applicants": [10.0] * 3})
        out = ac.retail_profile(d)
        self.assertTrue(np.isnan(out["alloc"].iloc[0]))        # 500/100 = 5 is impossible: missing, not 1.0
        self.assertTrue(np.isnan(out["gain_10k"].iloc[0]))
        self.assertTrue(out["alloc_quarantined"].iloc[0])
        self.assertAlmostEqual(out["alloc"].iloc[1], 0.5)
        self.assertAlmostEqual(out["gain_10k"].iloc[1], 2500.0)
        self.assertTrue(out["alloc_quarantined"].iloc[2])      # zero allocation is not a valid rate either


if __name__ == "__main__":
    unittest.main()
