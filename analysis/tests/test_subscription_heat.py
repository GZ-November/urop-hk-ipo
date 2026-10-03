"""Tests for Main Line A: Subscription heat and first-day performance."""
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import subscription_heat_2026 as sub_heat


class SubscriptionHeatTests(unittest.TestCase):
    def test_load_data_returns_113_issuers_and_terciles(self):
        df = sub_heat.load_data()
        self.assertEqual(len(df), 113)
        self.assertFalse(df["Stock Code"].duplicated().any())
        self.assertEqual(df["demand_tercile"].value_counts().sum(), 113)
        self.assertTrue(set(df["demand_tercile"].dropna().unique()).issubset(
            {"Low demand", "Mid demand", "High demand"}))

    def test_demand_tercile_table_structure(self):
        df = sub_heat.load_data()
        tab = sub_heat.demand_tercile_table(df)
        self.assertEqual(len(tab), 4)  # Full sample + 3 terciles
        self.assertIn("Group", tab.columns)
        self.assertIn("Break Rate (%)", tab.columns)
        self.assertIn("Median IR (%)", tab.columns)

    def test_regressions_produce_expected_columns(self):
        df = sub_heat.load_data()
        tab, family = sub_heat.run_regressions(df)
        self.assertEqual(len(tab), 6)
        self.assertIn("Coefficient (HC3 SE)", tab.columns)
        self.assertIn("Wild Cluster p", tab.columns)
        self.assertIn("N", tab.columns)
        for _, row in tab.iterrows():
            self.assertEqual(row["N"], 113)

    def test_aftermarket_balanced_sample_size(self):
        df = sub_heat.load_data()
        tab = sub_heat.aftermarket_performance_table(df)
        self.assertIn("Full Balanced Sample", tab["Group"].values)
        full_row = tab[tab["Group"] == "Full Balanced Sample"].iloc[0]
        self.assertEqual(full_row["N"], 102)

    def test_subgroups_table_includes_public_offer_share(self):
        df = sub_heat.load_data()
        tab = sub_heat.subgroup_breakdown_table(df)
        self.assertIn("Mean Public Offer (%)", tab.columns)
        self.assertIn("Median Public Offer (%)", tab.columns)
        self.assertFalse(tab["Mean Public Offer (%)"].isna().any())



if __name__ == "__main__":
    unittest.main()
