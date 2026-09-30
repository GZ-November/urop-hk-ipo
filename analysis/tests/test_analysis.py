"""Regression tests for cohort selection, missing evidence and inference."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_cluster

ANALYSIS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ANALYSIS))
import module_a_stylized_facts as module_a
import module_b_underpricing_regression as module_b


def panel_rows():
    rows = pd.DataFrame({column: [0.0, 0.0] for column in module_a.C.values()})
    rows["Stock Code"] = ["00001.HK", "00002.HK"]
    rows["cohort"] = ["2026Q1", "2026Q2"]
    rows[module_a.C["list_date"]] = ["2026-01-08", "2026-04-08"]
    rows[module_a.C["route_text"]] = ["Main Board", "Main Board"]
    rows[module_a.C["age"]] = [10.0, 20.0]
    rows[module_a.C["offer"]] = [10.0, 20.0]
    rows[module_a.C["base_shares"]] = [100_000_000, 100_000_000]
    rows[module_a.C["sub"]] = [2.0, 3.0]
    rows[module_a.C["ir"]] = [0.1, 0.2]
    rows["sponsor_reputation_tier"] = [1, 2]
    rows["HSI return over 20 trading days before prospectus (%)"] = [0.01, 0.02]
    rows["HK ordinary IPO count in 90 calendar days before prospectus"] = [20, 30]
    return rows


def load_rows(rows):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "panel.csv"
        rows.to_csv(path, index=False)
        return module_a.load_panel(path)


class PanelSelectionTests(unittest.TestCase):
    def test_actual_listing_year_selects_only_2026(self):
        rows = panel_rows()
        rows.loc[1, "cohort"] = "2025Q2"
        rows.loc[1, module_a.C["list_date"]] = "2025-04-08"
        selected = module_a.select_2026(load_rows(rows))
        self.assertEqual(selected["Stock Code"].tolist(), ["00001.HK"])

    def test_date_cohort_disagreements_fail_in_both_directions(self):
        for cohort, date in [("2026Q1", "2025-01-08"), ("2025Q1", "2026-01-08"),
                             ("2026Q1", None)]:
            with self.subTest(cohort=cohort, date=date):
                rows = panel_rows().iloc[:1].copy()
                rows.loc[0, "cohort"] = cohort
                rows.loc[0, module_a.C["list_date"]] = date
                with self.assertRaisesRegex(ValueError, "cohort labels"):
                    module_a.select_2026(load_rows(rows))

    def test_duplicate_issuers_and_empty_sample_fail(self):
        rows = panel_rows()
        rows["Stock Code"] = "00001.HK"
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            module_a.select_2026(load_rows(rows))
        rows["cohort"] = "2025Q1"
        rows[module_a.C["list_date"]] = "2025-01-08"
        with self.assertRaisesRegex(ValueError, "No observed 2026"):
            module_a.select_2026(load_rows(rows))

    def test_unknown_route_evidence_is_preserved_even_when_entire_column_missing(self):
        rows = panel_rows()
        for key in ("c18a", "c18c", "ah", "route_text"):
            rows[module_a.C[key]] = np.nan
        panel = load_rows(rows)
        self.assertTrue(panel["ah_true"].isna().all())
        self.assertEqual(panel["route"].tolist(), ["Unknown", "Unknown"])
        self.assertTrue(module_b.prepare(panel)["ah"].isna().all())

    def test_numeric_missing_markers_and_infinity_are_not_observations(self):
        rows = panel_rows()
        rows[module_a.C["age"]] = ["-", "12.5"]
        rows[module_a.C["ir"]] = [np.inf, 0.2]
        panel = load_rows(rows)
        self.assertTrue(pd.isna(panel.loc[0, module_a.C["age"]]))
        self.assertEqual(panel.loc[1, module_a.C["age"]], 12.5)
        self.assertTrue(pd.isna(panel.loc[0, "ir"]))


class RegressionPreparationTests(unittest.TestCase):
    def test_hot_control_uses_listing_date_and_is_in_every_parsimonious_model(self):
        panel = load_rows(panel_rows())
        panel["cohort"] = "2026Q3"  # Control must not depend on this label.
        self.assertEqual(module_b.prepare(panel)["hot"].tolist(), [0.0, 1.0])
        for name, regressors in module_b.MODELS.items():
            with self.subTest(model=name):
                self.assertIn("hot", regressors)
                self.assertLessEqual(len(regressors), 10)
                self.assertTrue({"bio", "spec", "csstate"}.isdisjoint(regressors))

    def test_invalid_log_domains_become_missing(self):
        panel = load_rows(panel_rows())
        panel["ir"] = [-1.0, -1.1]
        panel[module_a.C["age"]] = [0.0, -2.0]
        panel["base_proceeds"] = [0.0, -1.0]
        panel[module_a.C["sub"]] = [0.0, -1.0]
        prepared = module_b.prepare(panel)
        self.assertTrue(prepared[["y", "lage", "lproc", "lsub"]].isna().all().all())

    def test_design_drops_nonfinite_rows_and_keeps_codes_aligned(self):
        frame = pd.DataFrame({"y": [1, 2, np.inf, 4, 5, 6],
                              "x": [0, 1, 2, -np.inf, 4, 5],
                              "code": list("abcdef")})
        y, design, codes = module_b.design(frame, ["x"])
        self.assertEqual(codes.tolist(), ["a", "b", "e", "f"])
        self.assertEqual(y.index.tolist(), design.index.tolist())
        self.assertTrue(np.isfinite(design.to_numpy()).all())
        self.assertEqual(design.columns.tolist(), ["const", "x"])

    def test_design_rejects_unidentified_or_saturated_models(self):
        singular = pd.DataFrame({"y": [1, 2, 3, 4], "x": [0] * 4, "code": list("abcd")})
        with self.assertRaisesRegex(ValueError, "rank deficient"):
            module_b.design(singular, ["x"])
        saturated = pd.DataFrame({"y": [1, 2], "x": [0, 1], "code": ["a", "b"]})
        with self.assertRaisesRegex(ValueError, "more complete observations"):
            module_b.design(saturated, ["x"])

    def test_common_sample_reports_overlapping_missing_and_invalid_reasons(self):
        frame = pd.DataFrame({name: np.ones(4) for name in module_b.MODELS["M4"]})
        frame["y"] = [np.nan, 0.1, 0.2, 0.3]
        frame["code"] = list("abcd")
        frame["month"] = ["2026-01", "2026-02", None, "2026-04"]
        frame.loc[0, "hsi"] = np.nan  # Same excluded issuer has two reasons.
        frame.loc[1, "lsub"] = np.inf
        report = module_b.table_sample_selection(frame)
        self.assertEqual(report.loc["Outcome: log(1 + IR)", "Missing/invalid"], 1)
        self.assertEqual(report.loc[module_b.V["hsi"].label, "Missing/invalid"], 1)
        self.assertEqual(report.loc[module_b.V["lsub"].label, "Missing/invalid"], 1)
        self.assertEqual(report.loc["Listing month", "Missing/invalid"], 1)
        common = report.loc["Common complete-case sample (M1-M4)"]
        self.assertEqual(common["Missing/invalid"], 3)
        self.assertEqual(common["Available"], 1)
        self.assertEqual(module_b.estimation_sample(frame)["code"].tolist(), ["d"])


class BootstrapAndClusterTests(unittest.TestCase):
    def test_cr1_covariance_matches_statsmodels_on_synthetic_clustered_sample(self):
        rng = np.random.default_rng(123)
        groups = np.repeat(np.arange(4), 20)
        design = sm.add_constant(rng.normal(size=(80, 2)))
        y = design @ np.array([1.0, 0.5, -0.2]) + rng.normal(size=4)[groups] + rng.normal(size=80)
        fitted = sm.OLS(y, design).fit()
        actual = module_b.cr1_cov(design, fitted.resid, groups)
        np.testing.assert_allclose(actual, cov_cluster(fitted, groups, use_correction=True),
                                   rtol=1e-10, atol=1e-12)

    def test_cluster_covariance_requires_multiple_clusters(self):
        design = sm.add_constant(np.arange(5, dtype=float))
        with self.assertRaisesRegex(ValueError, "at least two clusters"):
            module_b.cr1_cov(design, np.ones(5), np.zeros(5))

    def test_bootstrap_skips_singular_draws_and_reports_count(self):
        frame = pd.DataFrame({"y": [1, 2, 3, 5], "x": [0, 0, 1, 1], "code": list("abcd")})

        class Resampler:
            calls = 0

            def integers(self, low, high, size):
                self.calls += 1
                return np.zeros(size, dtype=int) if self.calls == 1 else np.arange(size)

        with patch.object(module_b, "N_BOOT", 2), patch.object(module_b.np.random, "default_rng", return_value=Resampler()):
            intervals = module_b.bootstrap_ci(frame, ["x"])
        self.assertEqual(intervals.attrs["rejected_draws"], 1)
        np.testing.assert_allclose(intervals.loc["x"], [2.5, 2.5])

    def test_bootstrap_fails_when_no_identified_draws_can_be_collected(self):
        frame = pd.DataFrame({"y": [1, 2, 3, 5], "x": [0, 0, 1, 1], "code": list("abcd")})

        class Resampler:
            def integers(self, low, high, size):
                return np.zeros(size, dtype=int)

        with patch.object(module_b, "N_BOOT", 2), patch.object(module_b.np.random, "default_rng", return_value=Resampler()):
            with self.assertRaisesRegex(ValueError, "Too few full-rank"):
                module_b.bootstrap_ci(frame, ["x"])


if __name__ == "__main__":
    unittest.main()
