"""Main Line B: Does High First-Day Return Equal Retail Investor Profit?

Empirical investigation into retail allocation success rates, expected allotment,
and real first-day wealth effects under institutional rationing, fixed-budget constraints,
progressive allotment schedules, and transaction/financing frictions across 2026 Hong Kong IPOs.

Sample: 113 Hong Kong Main Board ordinary IPOs listed between 2026-01-02 and 2026-09-30.
Data Sources:
  - Clean allocation tiers: pipeline/reports/data_gap_collection/allocation_tiers_clean.csv (4,582 tiers, 100% reconciled)
  - Board lot units: pipeline/reports/data_gap_collection/board_lots.csv (113 issuers)
  - Master panel: select_2026(load_panel())

Outputs: analysis/out/retail_profit/
"""
from __future__ import annotations


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

from research_inputs import C, ROOT, load_panel, select_2026
from shared.estimation import bh_family, stars
from shared.inference import wild_cluster_p
from shared.reporting import to_markdown
from shared.allocation_review import reviewed_tiers
from shared.reporting import (
    AXIS, BLUE, INK, INK2, MUTED, ORANGE, new_fig, style_axes,
)

OUT = ROOT / "analysis" / "out" / "retail_profit"
TIERS_PATH = ROOT / "pipeline/reports/data_gap_collection/allocation_tiers_clean.csv"
LOTS_PATH = ROOT / "pipeline/reports/data_gap_collection/board_lots.csv"
SEED = 20260930


def load_strategies_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Extract 1-lot, 10-lot, and fixed budget strategies from verified tier-level disclosures."""
    panel = select_2026(load_panel()).copy()
    panel = panel.set_index("Stock Code")
    panel["sub_x"] = panel[C["sub"]]
    panel["demand_group"] = pd.qcut(panel["sub_x"], 3, labels=["Low demand", "Mid demand", "High demand"])

    tiers = reviewed_tiers(ROOT)
    lots = pd.read_csv(LOTS_PATH).set_index("code")
    coverage = pd.read_csv(TIERS_PATH.parent / "allocation_coverage.csv").set_index("code")

    one_lot_records = []
    ten_lot_records = []
    budget_records = {10000: [], 50000: [], 100000: []}

    for code, row in panel.iterrows():
        lot_size = lots.loc[code, "board_lot_units"]
        unit = lots.loc[code, "board_lot_unit"]
        p0 = row[C["offer"]]
        p1 = row["First trading day closing price (HK$)"]
        ir = row["ir"]
        cohort = row["cohort"]
        demand_group = row["demand_group"]
        sub_x = row["sub_x"]
        applicants = row["Public applicants"]
        proceeds = row["base_proceeds"] / 1e6
        ah_flag = row["ah_true"]
        month = str(row["month"])

        # Macro allocation rate (headline aggregate: Final public shares / Valid applied shares)
        macro_alloc_rate = ((row["Final public offer shares"] - coverage.loc[code, "overseas_employee_reserved_shares"]) / row["Public valid applied shares"]) if row["Public valid applied shares"] > 0 else np.nan

        t = tiers[tiers["code"] == code].copy()

        if t.empty or t["applied_shares"].duplicated().any():
            raise ValueError(f"{code}: missing or ambiguous tier strategy")
        if t["applied_shares"].mul(t["applicants"]).sum() != row["Public valid applied shares"]:
            raise ValueError(f"{code}: current master differs from reviewed applied totals")
        if t.applicants.sum() != row["Public applicants"] or t.allocated_shares.sum() != row["Final public offer shares"] - coverage.loc[code, "overseas_employee_reserved_shares"]:
            raise ValueError(f"{code}: current master differs from reviewed allocation totals")
        if lot_size != t.board_lot_units.iloc[0] or unit != t.board_lot_unit.iloc[0]:
            raise ValueError(f"{code}: lot metadata differs from reviewed tiers")
        # 1. Strategy: 1 Board Lot (or minimum tier)
        exact1 = t[t["applied_shares"] == lot_size]
        is_exact_1lot = len(exact1) > 0
        r1 = exact1.iloc[0] if is_exact_1lot else t.sort_values("applied_shares").iloc[0]

        guaranteed_1 = r1["guaranteed_shares"]
        ballot_prob_1 = (r1["ballot_winners"] / r1["applicants"]) if r1["applicants"] > 0 else 0.0
        success_rate_1 = 1.0 if guaranteed_1 > 0 else ballot_prob_1
        exp_shares_1 = r1["expected_shares"]
        applied_shares_1 = r1["applied_shares"]
        capital_1 = applied_shares_1 * p0
        exp_profit_1 = exp_shares_1 * (p1 - p0)
        app_ret_1 = exp_profit_1 / capital_1 if capital_1 > 0 else 0.0
        alloc_rate_1 = exp_shares_1 / applied_shares_1 if applied_shares_1 > 0 else 0.0

        one_lot_records.append({
            "code": code, "cohort": cohort, "month": month, "demand_group": demand_group,
            "sub_x": sub_x, "applicants": applicants, "proceeds": proceeds, "ah_flag": ah_flag,
            "p0": p0, "p1": p1, "ir": ir, "lot_size": lot_size, "unit": unit,
            "applied_shares": applied_shares_1, "is_exact_lot": int(is_exact_1lot),
            "ballot_extra_shares": r1["ballot_extra_shares"], "strategy_kind": "strict_one_lot" if is_exact_1lot else "minimum_application",
            "guaranteed_shares": guaranteed_1, "ballot_prob": ballot_prob_1, "success_rate": success_rate_1,
            "exp_shares": exp_shares_1, "applied_capital": capital_1, "exp_profit_hkd": exp_profit_1,
            "app_return": app_ret_1, "alloc_rate": alloc_rate_1, "macro_alloc_rate": macro_alloc_rate,
            "is_break": int(ir < 0),
        })

        # 2. Strategy: 10 Board Lots
        r10 = t[t["applied_shares"] == 10 * lot_size].iloc[0]
        guaranteed_10 = r10["guaranteed_shares"]
        ballot_prob_10 = (r10["ballot_winners"] / r10["applicants"]) if r10["applicants"] > 0 else 0.0
        success_rate_10 = 1.0 if guaranteed_10 > 0 else ballot_prob_10
        exp_shares_10 = r10["expected_shares"]
        applied_shares_10 = r10["applied_shares"]
        capital_10 = applied_shares_10 * p0
        exp_profit_10 = exp_shares_10 * (p1 - p0)
        app_ret_10 = exp_profit_10 / capital_10 if capital_10 > 0 else 0.0
        alloc_rate_10 = exp_shares_10 / applied_shares_10 if applied_shares_10 > 0 else 0.0

        ten_lot_records.append({
            "code": code, "cohort": cohort, "month": month, "demand_group": demand_group,
            "sub_x": sub_x, "applicants": applicants, "proceeds": proceeds, "ah_flag": ah_flag,
            "p0": p0, "p1": p1, "ir": ir, "lot_size": lot_size,
            "applied_shares": applied_shares_10, "guaranteed_shares": guaranteed_10,
            "ballot_extra_shares": r10["ballot_extra_shares"], "ballot_prob": ballot_prob_10, "success_rate": success_rate_10, "exp_shares": exp_shares_10,
            "applied_capital": capital_10, "exp_profit_hkd": exp_profit_10,
            "app_return": app_ret_10, "alloc_rate": alloc_rate_10, "macro_alloc_rate": macro_alloc_rate,
            "is_break": int(ir < 0),
        })

        # 3. Strategy: Fixed Budgets
        t["cost"] = t["applied_shares"] * p0
        for b in [10000, 50000, 100000]:
            feasible = t[t["cost"] <= b]
            if len(feasible) == 0:
                budget_records[b].append({
                    "code": code, "cohort": cohort, "month": month, "demand_group": demand_group,
                    "budget": b, "can_afford": 0, "applied_shares": 0, "applied_cost": 0.0,
                    "unused_cash": float(b), "exp_shares": 0.0, "exp_profit_hkd": 0.0,
                    "budget_return": 0.0, "applied_return": 0.0, "alloc_rate": 0.0, "ir": ir,
                })
            else:
                best = feasible.sort_values("applied_shares").iloc[-1]
                b_exp_shares = best["expected_shares"]
                b_profit = b_exp_shares * (p1 - p0)
                b_cost = best["cost"]
                b_alloc_rate = b_exp_shares / best["applied_shares"] if best["applied_shares"] > 0 else 0.0
                budget_records[b].append({
                    "code": code, "cohort": cohort, "month": month, "demand_group": demand_group,
                    "budget": b, "can_afford": 1, "applied_shares": best["applied_shares"],
                    "applied_cost": b_cost, "unused_cash": b - b_cost, "exp_shares": b_exp_shares,
                    "exp_profit_hkd": b_profit, "budget_return": b_profit / b,
                    "applied_return": b_profit / b_cost if b_cost > 0 else 0.0,
                    "alloc_rate": b_alloc_rate, "ir": ir,
                })

    df_1lot = pd.DataFrame(one_lot_records)
    df_10lot = pd.DataFrame(ten_lot_records)
    df_budgets = {b: pd.DataFrame(budget_records[b]) for b in budget_records}
    all_budgets = pd.concat(df_budgets.values(), ignore_index=True)
    return panel, df_1lot, df_10lot, all_budgets


def strategy_comparison_table(df_1lot: pd.DataFrame, df_10lot: pd.DataFrame, df_budgets: pd.DataFrame) -> pd.DataFrame:
    """Compare all retail strategies across capital, allocation, and return metrics."""
    rows = []

    # 1-lot strategy
    rows.append({
        "Retail Strategy": "1 Lot / Minimum Application",
        "Eligible Deals": f"{len(df_1lot)} / {len(df_1lot)} (100%)",
        "Mean Applied Capital (HK$)": f"HK$ {df_1lot['applied_capital'].mean():,.0f}",
        "Median Applied Capital (HK$)": f"HK$ {df_1lot['applied_capital'].median():,.0f}",
        "Mean Ballot Success Rate (%)": f"{100 * df_1lot['success_rate'].mean():.2f}%",
        "Median Ballot Success Rate (%)": f"{100 * df_1lot['success_rate'].median():.2f}%",
        "Mean Allocation Rate (%)": f"{100 * df_1lot['alloc_rate'].mean():.2f}%",
        "Median Allocation Rate (%)": f"{100 * df_1lot['alloc_rate'].median():.2f}%",
        "Mean Expected Shares": f"{df_1lot['exp_shares'].mean():.2f}",
        "Median Expected Shares": f"{df_1lot['exp_shares'].median():.2f}",
        "Mean Expected Profit (HK$)": f"HK$ {df_1lot['exp_profit_hkd'].mean():.2f}",
        "Median Expected Profit (HK$)": f"HK$ {df_1lot['exp_profit_hkd'].median():.2f}",
        "Mean Capital Return (%)": f"{100 * df_1lot['app_return'].mean():.2f}%",
        "Median Capital Return (%)": f"{100 * df_1lot['app_return'].median():.2f}%",
        "Offer Break Share (%)": f"{100 * df_1lot['is_break'].mean():.1f}%",
    })

    # 10-lot strategy
    rows.append({
        "Retail Strategy": "10 Board Lots Application",
        "Eligible Deals": f"{len(df_10lot)} / {len(df_10lot)} (100%)",
        "Mean Applied Capital (HK$)": f"HK$ {df_10lot['applied_capital'].mean():,.0f}",
        "Median Applied Capital (HK$)": f"HK$ {df_10lot['applied_capital'].median():,.0f}",
        "Mean Ballot Success Rate (%)": f"{100 * df_10lot['success_rate'].mean():.2f}%",
        "Median Ballot Success Rate (%)": f"{100 * df_10lot['success_rate'].median():.2f}%",
        "Mean Allocation Rate (%)": f"{100 * df_10lot['alloc_rate'].mean():.2f}%",
        "Median Allocation Rate (%)": f"{100 * df_10lot['alloc_rate'].median():.2f}%",
        "Mean Expected Shares": f"{df_10lot['exp_shares'].mean():.2f}",
        "Median Expected Shares": f"{df_10lot['exp_shares'].median():.2f}",
        "Mean Expected Profit (HK$)": f"HK$ {df_10lot['exp_profit_hkd'].mean():.2f}",
        "Median Expected Profit (HK$)": f"HK$ {df_10lot['exp_profit_hkd'].median():.2f}",
        "Mean Capital Return (%)": f"{100 * df_10lot['app_return'].mean():.2f}%",
        "Median Capital Return (%)": f"{100 * df_10lot['app_return'].median():.2f}%",
        "Offer Break Share (%)": f"{100 * df_10lot['is_break'].mean():.1f}%",
    })

    # Budgets
    for b in [10000, 50000, 100000]:
        sub_b = df_budgets[df_budgets["budget"] == b]
        afford = sub_b[sub_b["can_afford"] == 1]
        rows.append({
            "Retail Strategy": f"Fixed Budget HK$ {b:,}",
            "Eligible Deals": f"{afford['can_afford'].sum()} / {len(sub_b)} ({100*afford['can_afford'].sum()/len(sub_b):.1f}%)",
            "Mean Applied Capital (HK$)": f"HK$ {afford['applied_cost'].mean():,.0f}",
            "Median Applied Capital (HK$)": f"HK$ {afford['applied_cost'].median():,.0f}",
            "Mean Ballot Success Rate (%)": "—",
            "Median Ballot Success Rate (%)": "—",
            "Mean Allocation Rate (%)": f"{100 * afford['alloc_rate'].mean():.2f}%",
            "Median Allocation Rate (%)": f"{100 * afford['alloc_rate'].median():.2f}%",
            "Mean Expected Shares": f"{afford['exp_shares'].mean():.2f}",
            "Median Expected Shares": f"{afford['exp_shares'].median():.2f}",
            "Mean Expected Profit (HK$)": f"HK$ {afford['exp_profit_hkd'].mean():.2f}",
            "Median Expected Profit (HK$)": f"HK$ {afford['exp_profit_hkd'].median():.2f}",
            "Mean Capital Return (%)": f"{100 * sub_b['budget_return'].mean():.2f}%",
            "Median Capital Return (%)": f"{100 * sub_b['budget_return'].median():.2f}%",
            "Offer Break Share (%)": f"{100 * (afford['ir'] < 0).mean():.1f}%",
        })

    return pd.DataFrame(rows)


def demand_contrast_table(df_1lot: pd.DataFrame, df_10lot: pd.DataFrame) -> pd.DataFrame:
    """Demonstrate the Winner's Curse across subscription demand terciles."""
    rows = []

    for tercile in ["Low demand", "Mid demand", "High demand"]:
        p1 = df_1lot[df_1lot["demand_group"] == tercile]
        p10 = df_10lot[df_10lot["demand_group"] == tercile]

        rows.append({
            "Demand Group": str(tercile),
            "N": len(p1),
            "Median Sub (x)": f"{p1['sub_x'].median():.1f}x",
            "Mean Nominal IR (%)": f"{100 * p1['ir'].mean():.2f}%",
            "Median Nominal IR (%)": f"{100 * p1['ir'].median():.2f}%",
            "Offer Break Rate (%)": f"{100 * p1['is_break'].mean():.1f}%",
            "1-Lot Ballot Success Rate (%)": f"{100 * p1['success_rate'].mean():.2f}%",
            "1-Lot Allocation Rate (%)": f"{100 * p1['alloc_rate'].mean():.2f}%",
            "1-Lot Mean Expected Shares": f"{p1['exp_shares'].mean():.2f}",
            "1-Lot Mean Gross Profit (HK$)": f"HK$ {p1['exp_profit_hkd'].mean():.2f}",
            "1-Lot Median Gross Profit (HK$)": f"HK$ {p1['exp_profit_hkd'].median():.2f}",
            "1-Lot Mean Capital Return (%)": f"{100 * p1['app_return'].mean():.2f}%",
            "10-Lot Ballot Success Rate (%)": f"{100 * p10['success_rate'].mean():.2f}%",
            "10-Lot Allocation Rate (%)": f"{100 * p10['alloc_rate'].mean():.2f}%",
            "10-Lot Mean Expected Shares": f"{p10['exp_shares'].mean():.2f}",
            "10-Lot Mean Gross Profit (HK$)": f"HK$ {p10['exp_profit_hkd'].mean():.2f}",
            "10-Lot Mean Capital Return (%)": f"{100 * p10['app_return'].mean():.2f}%",
        })

    return pd.DataFrame(rows)


def macro_vs_micro_table(df_1lot: pd.DataFrame, df_10lot: pd.DataFrame) -> pd.DataFrame:
    """Compare headline aggregate (macro) allocation rates against tier-level micro rates."""
    rows = []

    # Full Sample
    ratio_1 = df_1lot["alloc_rate"] / df_1lot["macro_alloc_rate"].replace(0, np.nan)
    ratio_10 = df_10lot["alloc_rate"] / df_10lot["macro_alloc_rate"].replace(0, np.nan)

    rows.append({
        "Group": "Full Sample (2026)",
        "N": len(df_1lot),
        "Mean Macro Allocation Rate (%)": f"{100 * df_1lot['macro_alloc_rate'].mean():.2f}%",
        "Median Macro Allocation Rate (%)": f"{100 * df_1lot['macro_alloc_rate'].median():.2f}%",
        "Mean 1-Lot Allocation Rate (%)": f"{100 * df_1lot['alloc_rate'].mean():.2f}%",
        "Median 1-Lot Allocation Rate (%)": f"{100 * df_1lot['alloc_rate'].median():.2f}%",
        "1-Lot / Macro Ratio (Median)": f"{ratio_1.median():.1f}x",
        "Mean 10-Lot Allocation Rate (%)": f"{100 * df_10lot['alloc_rate'].mean():.2f}%",
        "Median 10-Lot Allocation Rate (%)": f"{100 * df_10lot['alloc_rate'].median():.2f}%",
        "10-Lot / Macro Ratio (Median)": f"{ratio_10.median():.1f}x",
    })

    for tercile in ["Low demand", "Mid demand", "High demand"]:
        p1 = df_1lot[df_1lot["demand_group"] == tercile]
        p10 = df_10lot[df_10lot["demand_group"] == tercile]
        r1 = p1["alloc_rate"] / p1["macro_alloc_rate"].replace(0, np.nan)
        r10 = p10["alloc_rate"] / p10["macro_alloc_rate"].replace(0, np.nan)
        rows.append({
            "Group": str(tercile),
            "N": len(p1),
            "Mean Macro Allocation Rate (%)": f"{100 * p1['macro_alloc_rate'].mean():.2f}%",
            "Median Macro Allocation Rate (%)": f"{100 * p1['macro_alloc_rate'].median():.2f}%",
            "Mean 1-Lot Allocation Rate (%)": f"{100 * p1['alloc_rate'].mean():.2f}%",
            "Median 1-Lot Allocation Rate (%)": f"{100 * p1['alloc_rate'].median():.2f}%",
            "1-Lot / Macro Ratio (Median)": f"{r1.median():.1f}x",
            "Mean 10-Lot Allocation Rate (%)": f"{100 * p10['alloc_rate'].mean():.2f}%",
            "Median 10-Lot Allocation Rate (%)": f"{100 * p10['alloc_rate'].median():.2f}%",
            "10-Lot / Macro Ratio (Median)": f"{r10.median():.1f}x",
        })

    return pd.DataFrame(rows)


def binary_lottery_table(df_1lot: pd.DataFrame) -> pd.DataFrame:
    """Analyze applicant-level discrete binary realization: winning shares vs getting zero shares."""
    rows = []

    groups = [("Full Sample (2026)", df_1lot)]
    for tercile in ["Low demand", "Mid demand", "High demand"]:
        groups.append((str(tercile), df_1lot[df_1lot["demand_group"] == tercile]))

    for grp_name, sub in groups:
        p = sub["success_rate"]
        ballot = sub["ballot_prob"]
        delta = sub["p1"] - sub["p0"]
        low = sub["guaranteed_shares"] * delta
        high = (sub["guaranteed_shares"] + sub["ballot_extra_shares"]) * delta
        for fee in [0, 28, 88, 100]:
            loss_prob = (1 - ballot) * (low < fee) + ballot * (high < fee)
            win_profit_prob = (1 - ballot) * (low > fee) + ballot * (high > fee)
            rows.append({
                "Group": grp_name,
                "Broker Fee": f"HK$ {fee}",
                "Mean Ballot Success Rate (%)": f"{100 * p.mean():.2f}%",
                "Mean Zero-Share Probability (%)": f"{100 * (1.0 - p).mean():.2f}%",
                "Mean Applicant Loss Probability (%)": f"{100 * loss_prob.mean():.2f}%",
                "Median Applicant Loss Probability (%)": f"{100 * loss_prob.median():.2f}%",
                "Mean Win & Profit Probability (%)": f"{100 * win_profit_prob.mean():.2f}%",
            })

    return pd.DataFrame(rows)


def cost_and_financing_table(df_1lot: pd.DataFrame, df_10lot: pd.DataFrame) -> pd.DataFrame:
    """Analyze fee erosion and margin financing interest across institutional scenarios."""
    scenarios = []

    # 1. Unleveraged Cash Applications: 1-Lot and 10-Lot under fees
    for strategy_name, s_profit, s_cap in [("1 Board Lot", df_1lot["exp_profit_hkd"], df_1lot["applied_capital"]),
                                          ("10 Board Lots", df_10lot["exp_profit_hkd"], df_10lot["applied_capital"])]:
        for fee in [0, 28, 88, 100]:
            net_gain = s_profit - fee
            net_ret = net_gain / s_cap
            scenarios.append({
                "Strategy": strategy_name,
                "Leverage": "Cash (100% Equity)",
                "Margin Rate": "0%",
                "Fee (HK$)": f"HK$ {fee}",
                "Mean Net Profit (HK$)": f"HK$ {net_gain.mean():.2f}",
                "Median Net Profit (HK$)": f"HK$ {net_gain.median():.2f}",
                "Loss Share (%)": f"{100 * net_gain.lt(0).mean():.1f}%",
                "Mean Net Return on Equity (%)": f"{100 * net_ret.mean():.2f}%",
                "Median Net Return on Equity (%)": f"{100 * net_ret.median():.2f}%",
            })

    # 2. Leveraged 10-Lot Applications: 90% margin financing (10% cash equity)
    for rate in [0.03, 0.06, 0.10]:
        for fee in [0, 28, 88, 100]:
            capital = df_10lot["applied_capital"]
            borrowed = 0.90 * capital
            equity = 0.10 * capital
            interest = borrowed * rate * 2 / 365  # 2 days settlement lockup
            net_gain = df_10lot["exp_profit_hkd"] - fee - interest
            net_ret = net_gain / equity
            scenarios.append({
                "Strategy": "10 Board Lots",
                "Leverage": "90% Margin (10x)",
                "Margin Rate": f"{rate*100:.0f}% p.a.",
                "Fee (HK$)": f"HK$ {fee}",
                "Mean Net Profit (HK$)": f"HK$ {net_gain.mean():.2f}",
                "Median Net Profit (HK$)": f"HK$ {net_gain.median():.2f}",
                "Loss Share (%)": f"{100 * net_gain.lt(0).mean():.1f}%",
                "Mean Net Return on Equity (%)": f"{100 * net_ret.mean():.2f}%",
                "Median Net Return on Equity (%)": f"{100 * net_ret.median():.2f}%",
            })

    return pd.DataFrame(scenarios)


def run_retail_regressions(df_1lot: pd.DataFrame, df_10lot: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    """Econometric regressions of Retail Expected Profit and Capital Return on demand and characteristics."""
    d = df_1lot.copy()
    d["log_sub"] = np.log(d["sub_x"].where(d["sub_x"] > 0))
    d["log_app"] = np.log(d["applicants"].where(d["applicants"] > 0))
    d["log_proc"] = np.log(d["proceeds"].where(d["proceeds"] > 0))
    d["hot"] = d["month"].isin(["2026-04", "2026-05", "2026-06"]).astype(float)

    specs = [
        ("Model 1: 1-Lot Return on log(Sub)", "app_return", ["log_sub"], "log_sub"),
        ("Model 2: 1-Lot Return + Size, A+H, Hot", "app_return", ["log_sub", "log_proc", "ah_flag", "hot"], "log_sub"),
        ("Model 3: 1-Lot Dollar Profit on log(Sub)", "exp_profit_hkd", ["log_sub"], "log_sub"),
        ("Model 4: 1-Lot Dollar Profit + Size, A+H, Hot", "exp_profit_hkd", ["log_sub", "log_proc", "ah_flag", "hot"], "log_sub"),
        ("Model 5: 10-Lot Return on log(Sub)", "app_return_10", ["log_sub"], "log_sub"),
        ("Model 6: 10-Lot Dollar Profit + Controls", "exp_profit_hkd_10", ["log_sub", "log_proc", "ah_flag", "hot"], "log_sub"),
    ]

    other = df_10lot.set_index("code")
    d["app_return_10"] = d.code.map(other.app_return)
    d["exp_profit_hkd_10"] = d.code.map(other.exp_profit_hkd)
    d = d.replace([np.inf, -np.inf], np.nan).dropna(subset=["app_return", "exp_profit_hkd", "app_return_10", "exp_profit_hkd_10", "month", "log_sub", "log_proc", "ah_flag", "hot"])

    results = []
    family = []

    for label, y_var, xs, focus in specs:
        z = d[[y_var, "month", *xs]].replace([np.inf, -np.inf], np.nan).dropna()
        X = sm.add_constant(z[xs].astype(float), has_constant="add")
        fit_hc3 = sm.OLS(z[y_var].astype(float), X).fit(cov_type="HC3")

        clusters = z["month"].to_numpy()
        p_wild = np.nan
        if 2 <= len(np.unique(clusters)) <= 16:
            j = list(X.columns).index(focus)
            p_wild = wild_cluster_p(z[y_var].to_numpy(float), X.to_numpy(), clusters, j)

        b = fit_hc3.params[focus]
        se = fit_hc3.bse[focus]
        p_hc3 = fit_hc3.pvalues[focus]
        r2 = fit_hc3.rsquared
        n = len(z)

        results.append({
            "Specification": label,
            "Dependent Variable": y_var,
            "Focus Regressor": focus,
            "Coefficient (HC3 SE)": f"{b:.4f}{stars(p_hc3)} ({se:.4f})",
            "HC3 p-value": f"{p_hc3:.4f}",
            "Wild Cluster p": f"{p_wild:.4f}" if pd.notna(p_wild) else "—",
            "R-squared": f"{r2:.3f}",
            "N": n, "G": len(np.unique(clusters)), "coefficient": b, "hc3_se": se,
            "ci_lower": fit_hc3.conf_int().loc[focus, 0], "ci_upper": fit_hc3.conf_int().loc[focus, 1],
        })
        family.append(("Main Line B Regressions", f"{label} - {focus}", p_hc3))

    return pd.DataFrame(results), family


def plot_retail_figures(df_1lot: pd.DataFrame, df_10lot: pd.DataFrame, df_scenarios: pd.DataFrame) -> None:
    """Generate publication-standard figures illustrating the Winner's Curse and fee erosion."""
    # Figure B1: Winner's Curse (Nominal IR vs Application Return)
    fig, (ax1, ax2) = new_fig(1, 2, figsize=(11, 4.8))
    for ax in (ax1, ax2):
        style_axes(ax)

    # ax1: Nominal IR vs 1-Lot Return
    ax1.scatter(100 * df_1lot["ir"], 100 * df_1lot["app_return"], color=BLUE, alpha=0.8, s=32, edgecolors="none")
    ax1.plot([-60, 400], [-60, 400], color=MUTED, lw=1.2, ls=":", label="Unrationed Identity (Return = IR)")
    ax1.axhline(0, color=AXIS, lw=1)
    ax1.axvline(0, color=AXIS, lw=1)
    ax1.set_xlabel("Headline Nominal First-Day Return (%)", fontsize=9, color=INK2)
    ax1.set_ylabel("1-Lot Application Capital Return (%)", fontsize=9, color=INK2)
    ax1.set_ylim(100 * df_1lot.app_return.min() - 2, 100 * df_1lot.app_return.max() + 2)
    ax1.set_xlim(-60, 400)
    ax1.legend(frameon=False, fontsize=8, loc="lower right")
    ax1.text(0.05, 0.90, "Allocation changes the return\non application capital",
             transform=ax1.transAxes, fontsize=8, color=ORANGE, fontweight="bold")

    # ax2: 1-Lot Ballot Success Rate vs Subscription Multiple
    ax2.scatter(df_1lot["sub_x"], 100 * df_1lot["success_rate"], color=ORANGE, alpha=0.8, s=32, edgecolors="none")
    ax2.set_xscale("log")
    ax2.set_xlabel("Subscription Multiple (times, log scale)", fontsize=9, color=INK2)
    ax2.set_ylabel("1-Lot Ballot Success Rate (%)", fontsize=9, color=INK2)
    ax2.text(0.05, 0.90, "Allocation probabilities vary\nacross disclosed application tiers",
             transform=ax2.transAxes, fontsize=8, color=INK2)

    fig.suptitle("Main Line B: Allocation and Application Returns in Hong Kong IPOs (N = 113)", fontsize=11, color=INK, fontweight="bold", y=0.98)
    fig.tight_layout()
    fig.savefig(OUT / "fig_b1_winners_curse.png", dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)

    # Figure B2: Fee Erosion and Net Loss Share
    fig, (ax1, ax2) = new_fig(1, 2, figsize=(10.5, 4.5))
    for ax in (ax1, ax2):
        style_axes(ax)

    fees = [0, 28, 88, 100]
    fee_labels = ["HK$ 0\n(Free)", "HK$ 28\n(Discount)", "HK$ 88\n(Standard)", "HK$ 100\n(Bank)"]

    c1 = df_scenarios[(df_scenarios["Strategy"] == "1 Board Lot") & (df_scenarios["Leverage"] == "Cash (100% Equity)")]
    c10 = df_scenarios[(df_scenarios["Strategy"] == "10 Board Lots") & (df_scenarios["Leverage"] == "Cash (100% Equity)")]

    med_profit_1 = [float(x.replace("HK$", "").strip()) for x in c1["Median Net Profit (HK$)"]]
    med_profit_10 = [float(x.replace("HK$", "").strip()) for x in c10["Median Net Profit (HK$)"]]
    loss_share_1 = [float(x.replace("%", "").strip()) for x in c1["Loss Share (%)"]]
    loss_share_10 = [float(x.replace("%", "").strip()) for x in c10["Loss Share (%)"]]

    x = np.arange(len(fees))
    width = 0.35

    # ax1: Median Net Profit
    ax1.bar(x - width/2, med_profit_1, width, label="1 Board Lot", color=BLUE, alpha=0.85)
    ax1.bar(x + width/2, med_profit_10, width, label="10 Board Lots", color="#406b87", alpha=0.85)
    ax1.set_xticks(x)
    ax1.set_xticklabels(fee_labels, fontsize=8)
    ax1.set_ylabel("Median Expected Net Profit (HK$)", fontsize=9, color=INK2)
    ax1.axhline(0, color=AXIS, lw=1)
    ax1.legend(frameon=False, fontsize=8)
    for i, v in enumerate(med_profit_1):
        ax1.text(i - width/2, v + (3 if v >= 0 else -8), f"{v:.0f}", ha="center", fontsize=8, color=INK)
    for i, v in enumerate(med_profit_10):
        ax1.text(i + width/2, v + (3 if v >= 0 else -8), f"{v:.0f}", ha="center", fontsize=8, color=INK)

    # ax2: Loss Share (%)
    ax2.plot(x, loss_share_1, marker="o", lw=2, color=ORANGE, label="1 Board Lot Loss Share (%)")
    ax2.plot(x, loss_share_10, marker="s", lw=2, color=BLUE, label="10 Board Lots Loss Share (%)")
    ax2.set_xticks(x)
    ax2.set_xticklabels(fee_labels, fontsize=8)
    ax2.set_ylabel("IPOs with negative expected net (%)", fontsize=9, color=INK2)
    ax2.set_ylim(15, 80)
    ax2.legend(frameon=False, fontsize=8)
    for i, v in enumerate(loss_share_1):
        ax2.text(i, v + 2, f"{v:.1f}%", ha="center", fontsize=8, color=ORANGE, fontweight="bold")
    for i, v in enumerate(loss_share_10):
        ax2.text(i, v - 3.5, f"{v:.1f}%", ha="center", fontsize=8, color=BLUE, fontweight="bold")

    fig.suptitle("Friction Erosion: Expected Net Profit and Negative-Expectation Share Across Fee Scenarios", fontsize=11, color=INK, fontweight="bold", y=0.98)
    fig.tight_layout()
    fig.savefig(OUT / "fig_b3_fee_erosion.png", dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    panel, df_1lot, df_10lot, df_budgets = load_strategies_data()

    # 1. Strategy Comparison Table
    tab_strategies = strategy_comparison_table(df_1lot, df_10lot, df_budgets)
    tab_strategies.to_csv(OUT / "retail_strategies_summary.csv", index=False)

    # 2. Demand Terciles Contrast (Winner's Curse)
    tab_demand = demand_contrast_table(df_1lot, df_10lot)
    tab_demand.to_csv(OUT / "retail_demand_comparison.csv", index=False)

    # 3. Macro vs Micro Allocation Rate Contrast
    tab_macro = macro_vs_micro_table(df_1lot, df_10lot)
    tab_macro.to_csv(OUT / "macro_vs_micro_allocation.csv", index=False)

    # 4. Discrete Binary Lottery Realization Table
    tab_binary = binary_lottery_table(df_1lot)
    tab_binary.to_csv(OUT / "retail_binary_lottery_realization.csv", index=False)

    # 5. Cost & Margin Financing Sensitivity
    tab_scenarios = cost_and_financing_table(df_1lot, df_10lot)
    tab_scenarios.to_csv(OUT / "retail_cost_scenarios.csv", index=False)

    # 6. Regressions
    tab_reg, family = run_retail_regressions(df_1lot, df_10lot)
    tab_reg.to_csv(OUT / "retail_regressions.csv", index=False)

    # Multiplicity adjustment
    bh_table = bh_family(family)
    bh_table.to_csv(OUT / "multiplicity_bh.csv", index=False)

    # Save individual strategies microdata
    df_1lot.to_csv(OUT / "retail_1lot_sample.csv", index=False)
    df_10lot.to_csv(OUT / "retail_10lot_sample.csv", index=False)
    df_budgets.to_csv(OUT / "retail_budget_sample.csv", index=False)

    # Figures
    plot_retail_figures(df_1lot, df_10lot, tab_scenarios)

    report_text = "# Retail application expectations (2026)\n\n"
    report_text += "112 strict one-lot applications and one minimum-tier exception (2649: 500 units versus 200-unit trading lot). All prices are observed first-day closes.\n\n"
    report_text += "Macro rate = ordinary-public allocated units / ordinary-public applied units; employee reserved allotments excluded. It is not 1/subscription multiple.\n\n"
    report_text += "Fees 28/88/100 and interest/day assumptions are sensitivity scenarios, not actual historical account charges. Loss Share is the share of IPOs with negative expected net profit; applicant loss probabilities are separate. No annualization or causal information-type claim.\n\n"
    for title, table in [("Strategies", tab_strategies), ("Demand groups", tab_demand), ("Macro versus micro", tab_macro), ("Applicant outcomes", tab_binary), ("Fee scenarios", tab_scenarios), ("Associations", tab_reg)]:
        report_text += "## " + title + "\n\n" + table.pipe(to_markdown) + "\n\n"
    (OUT / "retail_profit.md").write_text(report_text.rstrip()+"\n")
    print("Retail baseline written:", OUT)


if __name__ == "__main__":
    main()
