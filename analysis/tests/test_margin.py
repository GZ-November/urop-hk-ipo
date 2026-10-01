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
        m = mf.validate(rows(("1.HK", "2026-01-05", 1e8, 10.0, "https://example.com/survey"), ("1.HK", "2026-01-08", 3e8, 30.0, "https://example.com/survey")), SAMPLE)
        out = mf.per_issuer(m)
        self.assertEqual(out.loc["1.HK", "final_multiple"], 30.0)
        self.assertEqual(out.loc["1.HK", "days"], 2)

    def test_rows_outside_subscription_period_unknown_issuers_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside the issuer's subscription"):
            mf.validate(rows(("1.HK", "2026-01-20", 1e8, 10.0, "https://example.com/survey")), SAMPLE)
        with self.assertRaisesRegex(ValueError, "outside the 2026 sample"):
            mf.validate(rows(("9.HK", "2026-01-06", 1e8, 10.0, "https://example.com/survey")), SAMPLE)
        with self.assertRaisesRegex(ValueError, "lacks columns"):
            mf.validate(pd.DataFrame({"stock_code": ["1.HK"]}), SAMPLE)

    def test_declining_snapshots_are_valid_but_provenance_and_finite_values_required(self):
        m = mf.validate(rows(("1.HK", "2026-01-05", 3e8, 30, "https://example.com/survey"),
                             ("1.HK", "2026-01-08", 1e8, 10, "https://example.com/survey")), SAMPLE)
        pi = mf.per_issuer(m)
        self.assertFalse(pi.loc["1.HK", "on_close"])
        self.assertFalse(pi.loc["1.HK", "comparable_scope"])
        self.assertTrue(mf.cascade_summary(pi).empty)
        for value in (float("nan"), float("inf"), "invalid"):
            with self.assertRaisesRegex(ValueError, "nonfinite"):
                mf.validate(rows(("1.HK", "2026-01-05", value, 10, "https://example.com/survey")), SAMPLE)
        with self.assertRaisesRegex(ValueError, "source URL"):
            mf.validate(rows(("1.HK", "2026-01-05", 1e8, 10, "media survey")), SAMPLE)

    def test_duplicate_rows_and_inconsistent_denominators_fail(self):
        r = ("1.HK", "2026-01-05", 1e8, 10, "https://example.com/survey")
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            mf.validate(rows(r, r), SAMPLE)
        data = rows(r).assign(initial_public_value_hkd=2e7)
        with self.assertRaisesRegex(ValueError, "disagrees"):
            mf.validate(data, SAMPLE)

    def test_growth_requires_same_source_scope_and_positive_baseline(self):
        data = rows(("1.HK", "2026-01-05", 1e8, 10, "https://example.com/a"),
                    ("1.HK", "2026-01-09", 3e8, 30, "https://example.com/b")).assign(source_group="same_survey")
        pi = mf.per_issuer(mf.validate(data, SAMPLE))
        self.assertTrue(pi.loc["1.HK", "on_close"])
        self.assertAlmostEqual(mf.cascade_summary(pi).loc["1.HK", "cascade_ratio"], 3)
        data.loc[1, "source_group"] = "other_survey"
        self.assertTrue(mf.cascade_summary(mf.per_issuer(mf.validate(data, SAMPLE))).empty)

    def test_unit_leverage_model_withholds_hc3_inference(self):
        frame = pd.DataFrame({"y": range(9), "x": range(9), "hot": [1] + [0] * 8,
                              "month": ["2026-04"] + ["2026-07"] * 8})
        out = mf.safe_focus(frame, "y", ["x", "hot"], "x")
        self.assertEqual(out["n"], 9)
        self.assertTrue(pd.isna(out["p"]))
    def test_empty_sample_returns_diagnostic_instead_of_rank_error(self):
        frame = pd.DataFrame(columns=["y", "month", "x"])
        out = mf.safe_focus(frame, "y", ["x"], "x")
        self.assertEqual(out["n"], 0)
        self.assertEqual(out["rank"], 0)
        self.assertEqual(out["status"], "insufficient_sample_or_rank")
        self.assertTrue(pd.isna(out["p"]))



class TimingAndCoverageTests(unittest.TestCase):
    def test_pre_deadline_summary_uses_only_demonstrably_public_snapshots(self):
        data = rows(("1.HK", "2026-01-05", 1e8, 10.0, "https://example.com/a"),
                    ("1.HK", "2026-01-08", 3e8, 30.0, "https://example.com/b"),
                    ("1.HK", "2026-01-09", 9e8, 90.0, "https://example.com/c")).assign(
            available_before_deadline=["yes_published_before_closing_day", "yes_published_before_closing_day", "no_after_deadline"])
        out = mf.per_issuer(mf.validate(data, SAMPLE))
        self.assertEqual(out.loc["1.HK", "pre_deadline_n"], 2)
        self.assertEqual(out.loc["1.HK", "pre_deadline_last_multiple"], 30.0)  # the closing-day 90x was posted after the deadline
        self.assertEqual(out.loc["1.HK", "final_multiple"], 90.0)

    def test_issuer_with_only_post_deadline_observations_has_no_pre_deadline_value(self):
        data = rows(("1.HK", "2026-01-09", 9e8, 90.0, "https://example.com/c")).assign(
            available_before_deadline=["no_after_deadline"])
        out = mf.per_issuer(mf.validate(data, SAMPLE))
        self.assertEqual(out.loc["1.HK", "pre_deadline_n"], 0)
        self.assertTrue(pd.isna(out.loc["1.HK", "pre_deadline_last_multiple"]))

    def test_coverage_selection_counts_issuers_with_and_without_sources(self):
        d_full = pd.DataFrame({"code": ["1.HK", "2.HK", "3.HK", "4.HK"], "month": ["2026-01", "2026-01", "2026-02", "2026-02"],
                               "y": [.1, .2, .3, .4], "lsub": [1., 2., 3., 4.], "lproc": [5., 6., 7., 8.], "hot": [0, 0, 0, 0]})
        pi = pd.DataFrame(index=pd.Index(["1.HK", "3.HK"], name="stock_code"))
        margin = pd.DataFrame({"available_before_deadline": ["yes_published_before_closing_day"], "days_to_deadline": [2]})
        out = mf.coverage_selection(d_full, pi, margin)
        self.assertEqual(out["by_month"]["with_margin"].tolist(), [1, 1])
        self.assertEqual(int(out["comparison"].loc[0, "n_with_margin"]), 2)
        self.assertEqual(int(out["comparison"].loc[0, "n_without_margin"]), 2)


if __name__ == "__main__":
    unittest.main()
