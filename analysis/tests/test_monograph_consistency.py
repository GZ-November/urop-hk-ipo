"""Programmatic regression tests for monograph econometric & institutional consistency."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
OV_DIR = REPO_ROOT / "analysis" / "out" / "overview_1994_2026"
EXT_DIR = REPO_ROOT / "analysis" / "out" / "overview_extensions"
JE_DIR = REPO_ROOT / "analysis" / "out" / "journal_edition"


class MonographConsistencyTests(unittest.TestCase):
    def test_institutional_timeline_dates_and_tiers(self) -> None:
        tl = pd.read_csv(OV_DIR / "institutional_timeline_1994_2026.csv")
        r809 = tl[tl["rule_reference"].astype(str).str.contains("8.09", regex=False)]
        self.assertFalse(r809.empty)
        self.assertTrue((r809["effective_date"] == "2018-02-15").all())
        self.assertTrue(r809["default_requirement"].astype(str).str.contains("125M", regex=False).any())

        self.assertTrue((tl["effective_date"] == "2005-10-27").any())
        self.assertTrue(tl["event_id"].astype(str).str.contains("GL5113", regex=False).any())

        aug25 = tl[tl["effective_date"] == "2025-08-04"]
        self.assertFalse(aug25.empty)
        desc = " ".join(aug25["default_requirement"].astype(str).tolist())
        for tok in ("15%", "25%", "35%", "Mechanism B"):
            self.assertIn(tok, desc)
        self.assertNotIn("10x / 30x / 50x", desc)

    def test_ccass_pre_entry_alignment_clean(self) -> None:
        sc = pd.read_csv(EXT_DIR / "ext_table20c_fuzzy_rdd_diagnostics_and_ccass_holdings.csv")
        cc = sc[sc["Panel"].astype(str).str.startswith("C. CCASS")]
        semi = cc[cc["Specification"].astype(str).str.contains("Semi-Annual", regex=False)]
        self.assertFalse(semi.empty)
        self.assertIn("Pre=0.00%", str(semi["Metric_1"].iloc[0]))
        all_m1 = " ".join(cc["Metric_1"].astype(str).tolist())
        self.assertNotIn("Pre=2.69%", all_m1)
        self.assertNotIn("Pre=1.88%", all_m1)

    def test_ah_57_complete_anchor_coverage(self) -> None:
        ah = pd.read_csv(OV_DIR / "table10b_ah_anchor_and_inversions_N57.csv")
        self.assertEqual(len(ah), 57)
        self.assertEqual(ah["offer_vs_a_close_discount"].notna().sum(), 57)
        self.assertEqual(ah["h_day1_close_vs_a_discount"].notna().sum(), 57)
        self.assertGreaterEqual(ah["offer_vs_a_pricing_discount"].notna().sum(), 46)
        codes = set(ah["stock_code"].astype(str))
        for expected in ("0638.HK", "1304.HK", "2691.HK", "3750.HK", "6031.HK"):
            self.assertIn(expected, codes)

    def test_seasoned_3f_ctp_not_overwritten(self) -> None:
        ctp = pd.read_csv(EXT_DIR / "ext_table10_calendar_time_portfolio_alphas.csv")
        for col in ("Months_Seasoned_3F", "Beta_SMB_Seasoned", "Beta_MOM_Seasoned"):
            self.assertIn(col, ctp.columns)
        self.assertTrue((EXT_DIR / "ext_table10b_legacy_2f_calendar_time_portfolio_alphas.csv").is_file())

    def test_hibor_fini_year_fe_present(self) -> None:
        hib = pd.read_csv(EXT_DIR / "ext_table11b_hibor_fini_regressions.csv")
        models = " ".join(hib["Model"].astype(str).tolist())
        self.assertIn("Year FE", models)
        self.assertIn("1W-3M Spread", models)
        self.assertEqual(int(hib["N"].iloc[0]), 1871)

    def test_pn18_three_panel_validity_and_weak_fs(self) -> None:
        txt = (OV_DIR / "table9c_pn18_firststage_and_2sls_filing_verified.csv").read_text(encoding="utf-8")
        self.assertIn("# Panel A:", txt)
        self.assertIn("# Panel B:", txt)
        self.assertIn("# Panel C:", txt)
        self.assertIn("Covariate-Adjusted RF RD", txt)
        self.assertIn("Density Binomial Test", txt)
        # Weak 50x/100x Wald slope cells should be NaN/empty
        lines = [ln for ln in txt.splitlines() if ln.startswith(("50.0,", "100.0,"))]
        self.assertEqual(len(lines), 12)
        for ln in lines:
            self.assertTrue(ln.endswith(",,,"), f"Expected empty 2SLS/Wald columns on weak FS row: {ln}")

    def test_iv_exclusion_flag_and_oster_separation(self) -> None:
        iv = pd.read_csv(EXT_DIR / "ext_table16d_tier1_iv_ar_oster_diagnostics.csv")
        self.assertIn("Exclusion_Status", iv.columns)
        self.assertIn("Oster_Delta", iv.columns)
        self.assertTrue(iv["Exclusion_Status"].astype(str).str.contains("FAILS_EXCLUSION", regex=False).any())

    def test_lockup_placebo_and_subgroups_present(self) -> None:
        lk = pd.read_csv(EXT_DIR / "ext_table15b_paired_6m_vs_12m_lockup_did.csv")
        cohorts = " ".join(lk["Cohort_and_Window"].astype(str).tolist())
        self.assertIn("Placebo Day +120", cohorts)
        self.assertIn("Placebo Day +240", cohorts)
        self.assertIn("Pure Ch.19A H-Shares", cohorts)
        self.assertIn("A+H Dual-Listed H-Shares", cohorts)

    def test_tables_and_stats_json_complete(self) -> None:
        data = json.loads((JE_DIR / "tables_and_stats.json").read_text(encoding="utf-8"))
        self.assertEqual(set(data["main_tables"].keys()), {f"Table {i}" for i in range(1, 14)})
        self.assertEqual(set(data["ia_tables"].keys()), {f"Table IA.{i}" for i in range(1, 22)})
        for k, v in {**data["main_tables"], **data["ia_tables"]}.items():
            self.assertGreater(len(v), 50, f"Table {k} unexpectedly short")


if __name__ == "__main__":
    unittest.main()
