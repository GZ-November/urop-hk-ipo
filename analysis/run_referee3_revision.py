#!/usr/bin/env python3
"""Third-round referee revision checks for the Hong Kong IPO monograph.

Reads existing cleaned panels (no network access) and writes six CSVs to
analysis/out/overview_extensions/rev3_*.csv:

1. rev3_table1_pricing_window_split.csv
   Splits offer-window Hang Seng news at the recorded pricing date. News
   before pricing can enter both the offer price P0 and the debut price P1;
   news after pricing can only enter P1. The original specification measured
   the window to the trading day before listing, so it mixed both.
2. rev3_table2_mechanism_relabel.csv
   Applies prospectus-verified Mechanism A/B labels, separates Chapter 18C
   and bespoke waiver schedules, and re-estimates the pre/post August 2025
   comparison with controls fixed at prospectus publication.
3. rev3_table3_ballot_costs.csv
   Reconciles the Pool B financing-day assumption and reports HK$ outcomes.
4. rev3_table4_terminal_sample_ledger.csv
   Counts and proceeds for every exclusion between the census and the
   terminal-value sample.
5. rev3_table5_regime_timing.csv
   Deals whose PN18 regime differs between listing-date and prospectus-date
   cutoffs.
6. rev3_table6_benchmark_construction.csv
   Documents the estimated HSI total-return construction.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

REPO = Path(__file__).resolve().parent.parent
OV_DIR = REPO / "analysis" / "out" / "overview_1994_2026"
EXT_DIR = REPO / "analysis" / "out" / "overview_extensions"
PANEL_33Y = EXT_DIR / "clean_33y_macro_144a_hibor_panel.csv"
MICRO_226 = OV_DIR / "clean_micro_panel_2025_2026_N226.csv"
ROCK_113 = OV_DIR / "clean_rock_ballot_113_net_returns.csv"
HSI_JSON = OV_DIR / "market_cache" / "hkHSI_1994_2026.json"
MB_MASTER_CSV = REPO / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv"
SECTIONS_TEXT = REPO / "pipeline" / "prospectus_pipeline" / "data" / "text"
REFORM_DATE = "2025-08-04"

# Allocation-mechanism labels verified against the prospectus text (Chapter 4.14 of the Guide
# for New Listing Applicants). The panel labelled these six as Mechanism A through a fallback
# rule (final public share > 14%), which is incompatible with permissible Mechanism B reallocation.
VERIFIED_MECHANISM = {
    "1609.HK": "Mechanism_B",
    "7630.HK": "Mechanism_B",
    "2553.HK": "Mechanism_B",
    "6067.HK": "Mechanism_B",
    "6228.HK": "Mechanism_B",
    "1191.HK": "Mechanism_B",
    # WeRide launched with a 5% public tranche and a bespoke 10%/20% schedule at 10x/50x under a waiver.
    "0800.HK": "Bespoke_Waiver",
}


def _hc3_row(fit, var: str, **meta) -> dict:
    return {
        **meta,
        "Regressor": var,
        "N": int(fit.nobs),
        "Estimate": round(float(fit.params[var]), 4),
        "SE": round(float(fit.bse[var]), 4),
        "t_stat": round(float(fit.tvalues[var]), 2),
        "p_val": round(float(fit.pvalues[var]), 4),
        "R2": round(float(fit.rsquared), 4),
    }


def _wald_row(fit, lhs: str, rhs: str, **meta) -> dict:
    w = fit.t_test(f"{lhs} = {rhs}")
    return {
        **meta,
        "Regressor": f"Wald[{lhs} = {rhs}]",
        "N": int(fit.nobs),
        "Estimate": round(float(np.ravel(w.effect)[0]), 4),
        "SE": round(float(np.ravel(w.sd)[0]), 4),
        "t_stat": round(float(np.ravel(w.tvalue)[0]), 2),
        "p_val": round(float(w.pvalue), 4),
        "R2": np.nan,
    }


# ---------------------------------------------------------------------------
# 1. Offer-window market news split at the pricing date
# ---------------------------------------------------------------------------
def run_pricing_window_split() -> None:
    print("--- 1. Offer-window market news split at the pricing date ---")
    hsi = pd.Series({pd.Timestamp(k): float(v) for k, v in json.loads(HSI_JSON.read_text()).items()}).sort_index()
    dates = hsi.index

    def close_on_or_before(ts: pd.Timestamp) -> float:
        pos = dates.searchsorted(ts, side="right") - 1
        return float(hsi.iloc[pos]) if pos >= 0 else np.nan

    def close_before(ts: pd.Timestamp) -> float:
        pos = dates.searchsorted(ts, side="left") - 1
        return float(hsi.iloc[pos]) if pos >= 0 else np.nan

    d = pd.read_csv(PANEL_33Y, low_memory=False)
    clean = d[(d["flag_recycled_or_transferred_ticker"] == 0) & (d["flag_reverse_split_distortion"] == 0)]
    mb = clean[(clean["board"] == "Main Board") & (clean["has_exact_prospectus_date"] == True)].copy()  # noqa: E712
    mb["ir_wins"] = pd.to_numeric(mb["ir_close_pct"], errors="coerce").clip(lower=-90, upper=300)
    mb["log_proceeds"] = np.log(pd.to_numeric(mb["funds_raised_total_hkd"], errors="coerce") / 1e6)
    for c in ["prospectus_date", "bbg_pricing_date", "listing_date"]:
        mb[c + "_dt"] = pd.to_datetime(mb[c], errors="coerce", format="mixed")

    # A usable pricing date lies on or after the prospectus date and strictly before listing.
    ok_price = (
        mb["bbg_pricing_date_dt"].notna()
        & (mb["bbg_pricing_date_dt"] >= mb["prospectus_date_dt"])
        & (mb["bbg_pricing_date_dt"] < mb["listing_date_dt"])
    )
    mb["valid_pricing_date"] = ok_price.astype(int)
    pre, post = [], []
    for _, r in mb.iterrows():
        if not r["valid_pricing_date"]:
            pre.append(np.nan)
            post.append(np.nan)
            continue
        p_launch = close_on_or_before(r["prospectus_date_dt"])
        p_price = close_on_or_before(r["bbg_pricing_date_dt"])
        p_last = close_before(r["listing_date_dt"])
        pre.append((p_price / p_launch - 1.0) * 100.0)
        post.append((p_last / p_price - 1.0) * 100.0)
    mb["hsi_pre_pricing_pct"] = pre
    mb["hsi_post_pricing_pct"] = post
    for base in ["hsi_ret_sub_window_pct", "hsi_ret_pre30td_pct", "hsi_pre_pricing_pct", "hsi_post_pricing_pct"]:
        x = pd.to_numeric(mb[base], errors="coerce")
        mb[base + "_pos"] = x.clip(lower=0)
        mb[base + "_neg"] = x.clip(upper=0)

    mb["range_pos"] = pd.to_numeric(mb["ext_range_pos"], errors="coerce")
    mb["is_range"] = pd.to_numeric(mb["ext_is_bookbuilding_range"], errors="coerce")
    p0 = pd.to_numeric(mb["offer_price_hkd"], errors="coerce")
    pmax = pd.to_numeric(mb["ext_price_high"], errors="coerce")
    mb["log_p0_over_pmax"] = np.where((p0 > 0) & (pmax > 0), np.log(p0 / pmax), np.nan)

    rows: list[dict] = []
    base_ctrl = "hsi_ret_pre30td_pct_pos + hsi_ret_pre30td_pct_neg + log_proceeds"
    orig = "ir_wins ~ hsi_ret_sub_window_pct_pos + hsi_ret_sub_window_pct_neg + " + base_ctrl
    split = (
        "ir_wins ~ hsi_pre_pricing_pct_pos + hsi_pre_pricing_pct_neg + "
        "hsi_post_pricing_pct_pos + hsi_post_pricing_pct_neg + " + base_ctrl
    )

    s0 = mb.dropna(subset=["ir_wins", "hsi_ret_sub_window_pct", "hsi_ret_pre30td_pct", "log_proceeds"])
    f0 = smf.ols(orig, data=s0).fit(cov_type="HC3")
    s1 = s0[s0["valid_pricing_date"] == 1].dropna(subset=["hsi_pre_pricing_pct", "hsi_post_pricing_pct"])
    f1 = smf.ols(orig, data=s1).fit(cov_type="HC3")
    f2 = smf.ols(split, data=s1).fit(cov_type="HC3")
    for lbl, fit, vars_ in [
        ("A1_Original_Window_Full", f0, ["hsi_ret_sub_window_pct_pos", "hsi_ret_sub_window_pct_neg"]),
        ("A2_Original_Window_ValidPricingDate", f1, ["hsi_ret_sub_window_pct_pos", "hsi_ret_sub_window_pct_neg"]),
        ("A3_Split_at_Pricing_Date", f2, [
            "hsi_pre_pricing_pct_pos", "hsi_pre_pricing_pct_neg",
            "hsi_post_pricing_pct_pos", "hsi_post_pricing_pct_neg",
        ]),
    ]:
        for v in vars_:
            rows.append(_hc3_row(fit, v, Panel="A_Day1_Return", Specification=lbl, Outcome="IR_pct_winsorised"))
    rows.append(_wald_row(f2, "hsi_pre_pricing_pct_pos", "hsi_pre_pricing_pct_neg",
                          Panel="A_Day1_Return", Specification="A3_Split_at_Pricing_Date", Outcome="IR_pct_winsorised"))
    rows.append(_wald_row(f2, "hsi_post_pricing_pct_pos", "hsi_post_pricing_pct_neg",
                          Panel="A_Day1_Return", Specification="A3_Split_at_Pricing_Date", Outcome="IR_pct_winsorised"))

    # Does pre-pricing news move the offer price inside the range? (bookbuilt-range deals only)
    rng = s1[s1["is_range"] == 1].copy()
    for dep in ["range_pos", "log_p0_over_pmax"]:
        sub = rng.dropna(subset=[dep])
        fit = smf.ols(
            f"{dep} ~ hsi_pre_pricing_pct_pos + hsi_pre_pricing_pct_neg + hsi_ret_pre30td_pct + log_proceeds",
            data=sub,
        ).fit(cov_type="HC3")
        for v in ["hsi_pre_pricing_pct_pos", "hsi_pre_pricing_pct_neg"]:
            rows.append(_hc3_row(fit, v, Panel="B_Offer_Price_Position", Specification="B1_Range_Deals", Outcome=dep))

    # Ex-ante room to revise: fixed-price deals have none; range deals can move down, and up only to P_max.
    fx = s1.dropna(subset=["is_range"]).copy()
    fit_r = smf.ols(
        "ir_wins ~ (hsi_pre_pricing_pct_pos + hsi_pre_pricing_pct_neg) * is_range + "
        "hsi_post_pricing_pct_pos + hsi_post_pricing_pct_neg + " + base_ctrl,
        data=fx,
    ).fit(cov_type="HC3")
    for v in ["hsi_pre_pricing_pct_pos", "hsi_pre_pricing_pct_neg",
              "hsi_pre_pricing_pct_pos:is_range", "hsi_pre_pricing_pct_neg:is_range"]:
        rows.append(_hc3_row(fit_r, v, Panel="C_Room_to_Revise", Specification="C1_Fixed_vs_Range", Outcome="IR_pct_winsorised"))

    out = pd.DataFrame(rows)
    meta = pd.DataFrame([
        {"Panel": "Z_Sample", "Specification": "Main Board exact prospectus date", "Regressor": "N", "N": len(mb)},
        {"Panel": "Z_Sample", "Specification": "Valid pricing date (prospectus <= pricing < listing)",
         "Regressor": "N", "N": int(mb["valid_pricing_date"].sum())},
        {"Panel": "Z_Sample", "Specification": "Median trading-calendar days pricing to listing",
         "Regressor": "days", "N": float((mb.loc[ok_price, "listing_date_dt"] - mb.loc[ok_price, "bbg_pricing_date_dt"]).dt.days.median())},
        {"Panel": "Z_Sample", "Specification": "Range deals / fixed-price deals in split sample",
         "Regressor": "N", "N": f"{int((fx['is_range'] == 1).sum())}/{int((fx['is_range'] == 0).sum())}"},
    ])
    out = pd.concat([out, meta], ignore_index=True)
    out.to_csv(EXT_DIR / "rev3_table1_pricing_window_split.csv", index=False)
    print(out.to_string())


# ---------------------------------------------------------------------------
# 2. Mechanism A/B relabelling and prospectus-date pre/post comparison
# ---------------------------------------------------------------------------
def _confirm_mechanism_b(code: str) -> bool:
    f = SECTIONS_TEXT / f"HKIPO-MB{code.split('.')[0]}.jsonl"
    if not f.exists():
        return False
    txt = f.read_text(errors="ignore").replace("\\n", " ")
    return "follows Mechanism B" in txt or "Mechanism B set out" in txt


def run_mechanism_relabel() -> None:
    print("\n--- 2. Mechanism A/B relabelling ---")
    n = pd.read_csv(MICRO_226)
    # The cleaned panel now carries the verified labels; rebuild the earlier labels for comparison.
    n["regime_rev"] = n["alloc_regime_actual"]
    n["regime_orig"] = np.where(n["stock_code"].isin(list(VERIFIED_MECHANISM)), "Mechanism_A", n["alloc_regime_actual"])
    rows: list[dict] = []
    for code, lab in VERIFIED_MECHANISM.items():
        m = n["stock_code"] == code
        if not m.any():
            continue
        text_ok = _confirm_mechanism_b(code) if lab == "Mechanism_B" else np.nan
        rows.append({"Panel": "A_Label_Changes", "Group": code, "Measure": f"Mechanism_A -> {lab}",
                     "Value": text_ok, "Note": "Mechanism B text found in cached prospectus" if text_ok is True else ""})
        n.loc[m, "regime_rev"] = lab

    post = n["post_aug2025_prospectus"] == 1
    for col, lbl in [("regime_orig", "Original"), ("regime_rev", "Revised")]:
        elig = post & ~n[col].isin(["Ch18C_Special"])
        nb = int((n.loc[elig, col] == "Mechanism_B").sum())
        rows.append({"Panel": "B_Adoption", "Group": lbl, "Measure": "Mechanism B / eligible non-18C post-reform",
                     "Value": f"{nb}/{int(elig.sum())}", "Note": f"{nb / elig.sum() * 100:.1f}%"})
        for g, gdf in n[post].groupby(col):
            rows.append({"Panel": "C_AH_Share_by_Regime", "Group": f"{lbl}:{g}", "Measure": "Share A+H dual-listed",
                         "Value": round(float(gdf["is_ah_dual_listed"].mean()) * 100, 1), "Note": f"N={len(gdf)}"})
    # The earlier diagnostic pooled every post-reform non-B deal as "A" (9 A + 23 Chapter 18C).
    mixed = n[post & (n["regime_orig"] != "Mechanism_B")]
    rows.append({"Panel": "C_AH_Share_by_Regime", "Group": "Earlier diagnostic: all post-reform non-B",
                 "Measure": "Share A+H dual-listed", "Value": round(float(mixed["is_ah_dual_listed"].mean()) * 100, 1),
                 "Note": f"N={len(mixed)} (mixes Mechanism A with Chapter 18C)"})

    # Pre/post comparison with controls fixed when the prospectus is published.
    mbm = pd.read_csv(MB_MASTER_CSV, low_memory=False)
    mbm["stock_code"] = mbm["Stock Code"].astype(str).str.strip()
    n = n.merge(mbm[["stock_code", "First-day flipping ratio (%)", "Industry classification code"]], on="stock_code", how="left")
    n["day1_turnover_pct"] = pd.to_numeric(n["First-day flipping ratio (%)"], errors="coerce") * 100.0
    n["log_ir"] = np.log1p(pd.to_numeric(n["initial_return_pct"], errors="coerce") / 100.0)
    n["post_reg"] = n["post_aug2025_prospectus"].astype(int)
    n["hsics"] = n["Industry classification code"].fillna("UNK")
    n["list_ym"] = pd.to_datetime(n["listing_date"]).dt.strftime("%Y-%m")
    shares_base = pd.to_numeric(n["public_shares_final"], errors="coerce") + pd.to_numeric(n["placing_shares_final"], errors="coerce")
    n["log_max_size"] = np.log(shares_base * pd.to_numeric(n["max_offer_price_hkd"], errors="coerce") / 1e6)
    n["log_proc"] = np.log(pd.to_numeric(n["gross_proceeds_hkd_m"], errors="coerce"))
    for c in ["is_ah_dual_listed", "is_18a", "is_18c"]:
        n[c] = pd.to_numeric(n[c], errors="coerce").fillna(0)

    specs = [
        ("Earlier: +log proceeds +cornerstone pct (post-deal)",
         "{dep} ~ post_reg + log_proc + cornerstone_pct_of_offering + is_ah_dual_listed + C(hsics)"),
        ("Prospectus-time controls only (+max size, A+H, 18A, 18C, sector)",
         "{dep} ~ post_reg + log_max_size + is_ah_dual_listed + is_18a + is_18c + C(hsics)"),
        ("Prospectus-time, no sector FE", "{dep} ~ post_reg + log_max_size + is_ah_dual_listed + is_18a + is_18c"),
        ("Excluding Chapter 18C, prospectus-time controls",
         "{dep} ~ post_reg + log_max_size + is_ah_dual_listed + is_18a + C(hsics)"),
    ]
    for dep in ["public_offer_fraction_pct", "day1_turnover_pct", "log_ir"]:
        for lbl, fml in specs:
            sub = n if "Excluding" not in lbl else n[n["is_18c"] == 0]
            need = [dep, "log_max_size"] + (["log_proc", "cornerstone_pct_of_offering"] if "Earlier" in lbl else [])
            sub = sub.dropna(subset=need).copy()
            fit = smf.ols(fml.format(dep=dep), data=sub).fit(cov_type="cluster", cov_kwds={"groups": sub["list_ym"]})
            rows.append({"Panel": "D_PrePost_Comparison", "Group": lbl, "Measure": dep,
                         "Value": round(float(fit.params["post_reg"]), 4),
                         "Note": f"t={fit.tvalues['post_reg']:+.2f}, p={fit.pvalues['post_reg']:.3f}, N={int(fit.nobs)}, "
                                 f"G={sub['list_ym'].nunique()}"})
    out = pd.DataFrame(rows)
    out.to_csv(EXT_DIR / "rev3_table2_mechanism_relabel.csv", index=False)
    print(out.to_string())


# ---------------------------------------------------------------------------
# 3. Ballot financing costs
# ---------------------------------------------------------------------------
def run_ballot_costs() -> None:
    print("\n--- 3. Ballot financing costs ---")
    r = pd.read_csv(ROCK_113)
    fee = 1.0085
    a_pb = pd.to_numeric(r["alloc_rate_poolB_min_pct"], errors="coerce")
    g_pb = pd.to_numeric(r["gross_cap_ret_poolB_pct"], errors="coerce")
    cap_b = pd.to_numeric(r["poolB_min_capital_hkd"], errors="coerce")
    c1 = pd.to_numeric(r["entry_1lot_cost_hkd"], errors="coerce")
    rows = []
    for days in [2, 3]:
        net = g_pb - (a_pb / 100.0) * fee - 0.90 * 3.80 * (days / 365.0)
        rows.append({"Scenario": f"Pool B, table formula, {days}-day 90% margin at 3.80% p.a.", "N": int(net.notna().sum()),
                     "Mean_Net_Pct": round(float(net.mean()), 6), "Median_Net_HKD_per_Application": np.nan, "Mean_Net_HKD_per_Application": np.nan})
    for col, lbl in [("net_poolB_ret_full_hibor_margin_pct", "Pool B, deal-specific HIBOR and holding days, HK$100 fee, sale costs"),
                     ("net_poolB_ret_flat_margin_pct", "Pool B, flat-fee margin package (10% cash deposit)")]:
        x = pd.to_numeric(r[col], errors="coerce")
        hkd = cap_b * x / 100.0
        rows.append({"Scenario": lbl, "N": int(x.notna().sum()), "Mean_Net_Pct": round(float(x.mean()), 6),
                     "Median_Net_HKD_per_Application": round(float(hkd.median()), 0), "Mean_Net_HKD_per_Application": round(float(hkd.mean()), 0)})
    x1 = pd.to_numeric(r["excess_1lot_ret_over_hibor_pct"], errors="coerce")
    h1 = c1 * x1 / 100.0
    rows.append({"Scenario": "Pool A one lot, cash, net of fees, sale costs and HIBOR", "N": int(x1.notna().sum()),
                 "Mean_Net_Pct": round(float(x1.mean()), 4), "Median_Net_HKD_per_Application": round(float(h1.median()), 0),
                 "Mean_Net_HKD_per_Application": round(float(h1.mean()), 0)})
    rows.append({"Scenario": "Holding days used in detailed scenario (mean / median)", "N": len(r),
                 "Mean_Net_Pct": round(float(r["settlement_freeze_days"].mean()), 2),
                 "Median_Net_HKD_per_Application": float(r["settlement_freeze_days"].median()), "Mean_Net_HKD_per_Application": np.nan})
    out = pd.DataFrame(rows)
    out.to_csv(EXT_DIR / "rev3_table3_ballot_costs.csv", index=False)
    print(out.to_string())


# ---------------------------------------------------------------------------
# 4. Terminal-value sample ledger, 5. regime timing, 6. benchmark construction
# ---------------------------------------------------------------------------
def run_ledger_and_timing() -> None:
    print("\n--- 4. Terminal sample ledger ---")
    d = pd.read_csv(PANEL_33Y, low_memory=False)
    proc = pd.to_numeric(d["funds_raised_total_hkd"], errors="coerce") / 1e9
    recycled = d["flag_recycled_or_transferred_ticker"].fillna(0) != 0
    rev = ~recycled & d["flag_reverse_split_distortion"].fillna(False).astype(bool)
    unv = ~recycled & ~rev & d["flag_lifetime_split_unverified"].fillna(False).astype(bool)
    ret = pd.to_numeric(d["lifetime_offer_to_date_pct"], errors="coerce")
    ok = ~recycled & ~rev & ~unv & ret.notna()
    noq = ~recycled & ~rev & ~unv & ret.isna()
    rows = []
    for lbl, m in [
        ("Census of ordinary IPOs", pd.Series(True, index=d.index)),
        ("Verified terminal price", ok),
        ("  of which with usable proceeds", ok & proc.notna()),
        ("Delisted without terminal quote", noq),
        ("Code or corporate-action anomaly (all)", recycled | rev | unv),
        ("  Recycled ticker or transfer", recycled),
        ("  Unadjusted consolidation", rev),
        ("  Unverified split factor", unv),
    ]:
        rows.append({"Category": lbl, "N": int(m.sum()), "Proceeds_HKD_Bn": round(float(proc[m].sum()), 1)})
    led = pd.DataFrame(rows)
    led.to_csv(EXT_DIR / "rev3_table4_terminal_sample_ledger.csv", index=False)
    print(led.to_string())

    print("\n--- 5. Regime timing ---")
    ld = pd.to_datetime(d["listing_date"], errors="coerce", format="mixed")
    pdt = pd.to_datetime(d["prospectus_date"], errors="coerce", format="mixed")
    m = (d["board"] == "Main Board") & (pdt < REFORM_DATE) & (ld >= REFORM_DATE)
    tim = d.loc[m, ["stock_code", "prospectus_date", "listing_date"]].copy()
    tim["pn18_allocation_sample"] = d.loc[m, "pn18_allocation_sample"]
    tim.to_csv(EXT_DIR / "rev3_table5_regime_timing.csv", index=False)
    print(tim.to_string() if len(tim) else "No deal straddles the reform date.")

    print("\n--- 6. Benchmark construction ---")
    bench = pd.DataFrame([{
        "Series": "HSI total return (HSI-TR) used in Tables 8.1 and 8.3",
        "Construction": "Hang Seng price index compounded with a hard-coded annual dividend yield per calendar year "
                        "(build_longrun_benchmarks_and_factors.HSI_DIV_YIELD_PA), spread evenly across months",
        "Status": "Estimated series; not the published Hang Seng total-return index",
    }])
    bench.to_csv(EXT_DIR / "rev3_table6_benchmark_construction.csv", index=False)


def main() -> None:
    run_pricing_window_split()
    run_mechanism_relabel()
    run_ballot_costs()
    run_ledger_and_timing()
    print("\nRev3 checks complete.")


if __name__ == "__main__":
    main()
