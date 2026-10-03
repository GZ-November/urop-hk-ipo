"""Tests for Main Line B: Retail allotment rates, expected allocation and profit."""
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import retail_allocation_profit_2026 as rap


class RetailAllocationProfitTests(unittest.TestCase):
    def test_load_strategies_data_population_and_completeness(self):
        panel, df_1lot, df_10lot, df_budgets = rap.load_strategies_data()
        self.assertEqual(len(panel), 113)
        self.assertEqual(len(df_1lot), 113)
        self.assertEqual(len(df_10lot), 113)
        self.assertEqual(len(df_budgets), 113 * 3)

        # 1-lot exact match is 112, 1 exception is 2649.HK
        self.assertEqual(df_1lot["is_exact_lot"].sum(), 112)
        exception_code = df_1lot[df_1lot["is_exact_lot"] == 0]["code"].iloc[0]
        self.assertEqual(exception_code, "2649.HK")

    def test_allocation_rate_bounds(self):
        _, df_1lot, df_10lot, _ = rap.load_strategies_data()
        for df, name in [(df_1lot, "1-lot"), (df_10lot, "10-lot")]:
            with self.subTest(strategy=name):
                self.assertTrue((df["alloc_rate"] >= 0).all())
                self.assertTrue((df["alloc_rate"] <= 1.0001).all())
                self.assertTrue((df["applied_capital"] > 0).all())

    def test_fixed_budget_affordability_and_unused_cash(self):
        _, _, _, df_budgets = rap.load_strategies_data()
        for budget in [10000, 50000, 100000]:
            sub = df_budgets[df_budgets["budget"] == budget]
            self.assertEqual(len(sub), 113)
            # Applied cost must never exceed budget
            self.assertTrue((sub["applied_cost"] <= budget).all())
            self.assertTrue((sub["unused_cash"] >= 0).all())
            self.assertTrue(np.allclose(sub["applied_cost"] + sub["unused_cash"], budget))

    def test_cost_and_financing_scenarios_computation(self):
        _, df_1lot, df_10lot, _ = rap.load_strategies_data()
        tab = rap.cost_and_financing_table(df_1lot, df_10lot)
        self.assertTrue(len(tab) > 0)
        self.assertIn("Mean Net Profit (HK$)", tab.columns)
        self.assertIn("Loss Share (%)", tab.columns)

    def test_10lot_ballot_success_rate_vs_allocation_rate(self):
        _, df_1lot, df_10lot, _ = rap.load_strategies_data()
        # 10-lot ballot success rate (chance of receiving >=1 lot) must exceed 1-lot ballot success rate
        self.assertGreater(df_10lot["success_rate"].mean(), df_1lot["success_rate"].mean())
        # 10-lot allocation rate (shares / applied) must be lower than 1-lot allocation rate
        self.assertLess(df_10lot["alloc_rate"].mean(), df_1lot["alloc_rate"].mean())

    def test_macro_vs_micro_allocation_progressive_ratio(self):
        _, df_1lot, df_10lot, _ = rap.load_strategies_data()
        tab = rap.macro_vs_micro_table(df_1lot, df_10lot)
        self.assertEqual(len(tab), 4)
        full_row = tab[tab["Group"].str.startswith("Full Sample")].iloc[0]
        ratio_1 = float(full_row["1-Lot / Macro Ratio (Median)"].replace("x", ""))
        self.assertTrue(np.isfinite(ratio_1))

    def test_binary_lottery_realization_bounds(self):
        _, df_1lot, _, _ = rap.load_strategies_data()
        tab = rap.binary_lottery_table(df_1lot)
        self.assertTrue(len(tab) > 0)
        high_88 = tab[(tab["Group"] == "High demand") & (tab["Broker Fee"] == "HK$ 88")].iloc[0]
        zero_share_pct = float(high_88["Mean Zero-Share Probability (%)"].replace("%", ""))
        loss_pct = float(high_88["Mean Applicant Loss Probability (%)"].replace("%", ""))
        self.assertTrue(0 <= zero_share_pct <= 100)
        self.assertTrue(zero_share_pct <= loss_pct <= 100)

    def test_fixed_budget_allocation_rates(self):
        _, _, _, df_budgets = rap.load_strategies_data()
        affordable = df_budgets[df_budgets["can_afford"] == 1]
        self.assertTrue((affordable["alloc_rate"] > 0).all())
        self.assertTrue((affordable["alloc_rate"] <= 1.0).all())


if __name__ == "__main__":
    unittest.main()
