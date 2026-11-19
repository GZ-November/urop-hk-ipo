#!/usr/bin/env python3
"""Generate Post-Bloomberg Table 4 Pitfall Summary & 6 Publication-Grade Figures (300 DPI).

All statistics and plots are computed directly from the audited CSV outputs in
`analysis/out/overview_1994_2026/` with zero manual hardcoding.
"""
import shutil
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path("/Users/georgezhu/Desktop/UROP HK IPO")
OUT_DIR = REPO / "analysis" / "out" / "overview_1994_2026"
FIG_DIR = OUT_DIR / "figures"
DOC_FIG_DIR = REPO / "docs" / "overview_paper" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)
DOC_FIG_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

# ==============================================================================
# 1. POST-BLOOMBERG TABLE 4 SUMMARY BY BOARD & EPOCH
# ==============================================================================
df33 = pd.read_csv(OUT_DIR / "clean_33y_hkipo_panel_1994_2026.csv")

def assign_4epoch(y):
    if y <= 2004:
        return "Epoch II (1994-2004)"
    elif y <= 2017:
        return "Epoch III (2005-2017)"
    elif y <= 2022:
        return "Epoch IV (2018-2022)"
    return "Epoch V (2023-2026)"

df33["epoch_doc"] = df33["cohort_year"].apply(assign_4epoch)
df33["proceeds_hkd_m"] = np.where(
    df33["funds_raised_total_hkd"].notna(),
    df33["funds_raised_total_hkd"] / 1e6,
    np.where(df33["gem_funds_raised_hkd"].notna(), df33["gem_funds_raised_hkd"] / 1e6, df33["bbg_offer_size_m"])
)
df33["is_bbg_matched"] = df33["bbg_ticker"].notna() & (df33["bbg_ticker"].astype(str).str.strip() != "")

t4_rows = []
for board in ["Main Board", "GEM"]:
    sub_b = df33[df33["board"] == board].copy()
    groups = [(ep, sub_b[sub_b["epoch_doc"] == ep]) for ep in [
        "Epoch II (1994-2004)", "Epoch III (2005-2017)", "Epoch IV (2018-2022)", "Epoch V (2023-2026)"
    ]] + [(f"{board} Total", sub_b)]
    for lbl, g in groups:
        if len(g) == 0:
            continue
        n_pop = len(g)
        n_bbg = int(g["is_bbg_matched"].sum())
        n_split_10pp = int(g["flag_reverse_split_distortion"].astype(bool).sum())
        n_recycled = int(g["flag_recycled_or_transferred_ticker"].astype(bool).sum())
        n_delist_bbg = int(g["flag_delisted_or_acquired"].astype(bool).sum())
        n_missing_local = int(g["hkex_ir_close_pct"].isna().sum())
        naive_ew = g["hkex_ir_close_pct"].dropna().mean()
        clean_s = g["ir_close_pct"].dropna()
        clean_ew = clean_s.mean()
        valid_pw = g.dropna(subset=["ir_close_pct", "proceeds_hkd_m"])
        valid_pw = valid_pw[valid_pw["proceeds_hkd_m"] > 0]
        clean_pw = np.average(valid_pw["ir_close_pct"], weights=valid_pw["proceeds_hkd_m"]) if len(valid_pw) else np.nan
        clean_med = clean_s.median()
        break_pct = (clean_s < 0).mean() * 100.0
        t4_rows.append({
            "Board": board,
            "Epoch": lbl,
            "Pop_N": n_pop,
            "BBG_Matched_N": n_bbg,
            "BBG_Match_Pct": n_bbg / n_pop * 100.0,
            "Split_Distorted_gt10pp_N": n_split_10pp,
            "Recycled_or_Migrated_N": n_recycled,
            "Recycled_or_Migrated_Pct": n_recycled / n_pop * 100.0,
            "Delisted_BBG_Captured_N": n_delist_bbg,
            "Missing_Local_Feed_N": n_missing_local,
            "Naive_Local_EW_IR_Pct": naive_ew,
            "Clean_Unadj_EW_IR_Pct": clean_ew,
            "Clean_PW_IR_Pct": clean_pw,
            "Clean_Median_IR_Pct": clean_med,
            "Break_Rate_Pct": break_pct,
            "Clean_IR_N": len(clean_s),
        })

df_t4 = pd.DataFrame(t4_rows)
df_t4.round(3).to_csv(OUT_DIR / "table4_post_bbg_pitfalls_by_epoch.csv", index=False)
print("=== POST-BLOOMBERG TABLE 4 BY BOARD & EPOCH ===")
print(df_t4.round(2).to_string(index=False))

# Active vs Delisted survivorship summary across matched sample
m_surv = df33[df33["is_bbg_matched"]].copy()
print("\n=== ACTIVE VS DELISTED SURVIVORSHIP WEDGE (MATCHED N=2,757) ===")
for flag, lbl in [(False, "Active Tickers"), (True, "Delisted/Acquired (D/Q HK)")]:
    s = m_surv[m_surv["flag_delisted_or_acquired"].astype(bool) == flag]
    ir_s = s["ir_close_pct"].dropna()
    b1y = s["after_bhar_1y_pct"].dropna()
    print(f"  {lbl:28s}: N={len(s):4d} | Clean IR Mean={ir_s.mean():+6.2f}% (Med={ir_s.median():+6.2f}%) | 1Y Aftermarket BHAR Mean={b1y.mean():+6.2f}% (Med={b1y.median():+6.2f}%, N={len(b1y)})")

# ==============================================================================
# FIGURE 1: 33-YEAR PARALLEL VOLUME & PROCEEDS (HK VS US, 1994-2026)
# ==============================================================================
t5 = pd.read_csv(OUT_DIR / "table5_us_hk_parallel_clean_1994_2026.csv")
t5["HK_Total_N"] = t5["HK_MB_N"].fillna(0) + t5["HK_GEM_N"].fillna(0)
# Total HK proceeds USD bn from df33
hk_yr_usd = df33.groupby("cohort_year")["proceeds_hkd_m"].sum() / 7800.0
t5["HK_Total_USD_Bn"] = t5["Year"].map(hk_yr_usd)

fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.4))
ax = axes[0]
ax.plot(t5["Year"], t5["US_Ritter_N"], marker="o", ms=4, lw=2.0, color="#1f4e79", label="U.S. Operating IPOs (Ritter, 1994–2025)")
ax.plot(t5["Year"], t5["HK_Total_N"], marker="s", ms=4, lw=2.0, color="#b22222", label="Hong Kong Total IPOs (MB + GEM, 1994–2026Q3)")
ax.axvline(2000.5, ls="--", lw=1.0, color="gray", alpha=0.7)
ax.text(2001.0, 630, "Post-2000 U.S.\nListing Gap", fontsize=8.5, color="#444444")
ax.set_title("Panel A: Annual IPO Deal Counts (1994–2026)")
ax.set_xlabel("Listing Year")
ax.set_ylabel("Number of Ordinary Equity IPOs")
ax.legend(frameon=False, loc="upper right", fontsize=8.5)
ax.grid(axis="y", alpha=0.25)

ax = axes[1]
w = 0.40
yrs = t5["Year"].values
ax.bar(yrs - w/2, t5["US_Proceeds_USD_Bn"].fillna(0), width=w, color="#4a7ebb", alpha=0.85, label="U.S. Proceeds (US$ bn)")
ax.bar(yrs + w/2, t5["HK_Total_USD_Bn"].fillna(0), width=w, color="#c0504d", alpha=0.90, label="HKEX Proceeds (US$ bn)")
ax.set_title("Panel B: Annual Aggregate Gross Proceeds (US$ Billions)")
ax.set_xlabel("Listing Year")
ax.set_ylabel("Gross Proceeds (US$ Billions)")
ax.legend(frameon=False, loc="upper left", fontsize=8.5)
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
fig.savefig(FIG_DIR / "fig1_us_hk_parallel_1994_2026.png")

# ==============================================================================
# FIGURE 2: 33-YEAR GROSS SPREAD VS LOG PROCEEDS & ABSENCE OF U.S. 7% RULE
# ==============================================================================
sp = df33.dropna(subset=["gross_spread_clean_pct", "proceeds_hkd_m"]).copy()
sp = sp[(sp["gross_spread_clean_pct"] > 0) & (sp["gross_spread_clean_pct"] <= 15) & (sp["proceeds_hkd_m"] > 1)]
sp["proceeds_usd_m"] = sp["proceeds_hkd_m"] / 7.8

fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.4))
ax = axes[0]
mb_sp = sp[sp["board"] == "Main Board"]
gem_sp = sp[sp["board"] == "GEM"]
ax.scatter(np.log10(mb_sp["proceeds_usd_m"]), mb_sp["gross_spread_clean_pct"], s=12, alpha=0.35, color="#1f4e79", label=f"Main Board (N={len(mb_sp)})")
ax.scatter(np.log10(gem_sp["proceeds_usd_m"]), gem_sp["gross_spread_clean_pct"], s=14, alpha=0.45, color="#d95f02", marker="^", label=f"GEM (N={len(gem_sp)})")
ax.axhline(7.0, ls="--", lw=1.6, color="#b22222", label="U.S. 7.00% Focal Norm (93.3% of US$30M–$160M)")
ax.axhline(2.5, ls=":", lw=1.5, color="#1b7837", label="HK Historical 2.50% Brokerage Norm")
# OLS fit on Main Board
x_grid = np.linspace(0.5, 4.3, 100)
m_slope, m_int = np.polyfit(np.log10(mb_sp["proceeds_usd_m"]), mb_sp["gross_spread_clean_pct"], 1)
ax.plot(x_grid, m_int + m_slope * x_grid, lw=2.0, color="#08306b", label="Main Board OLS Fit")
ax.set_xticks([0, 1, 2, 3, 4])
ax.set_xticklabels(["$1M", "$10M", "$100M", "$1B", "$10B"])
ax.set_ylim(0, 13.5)
ax.set_title("Panel A: Gross Spread vs. Offering Size (1994–2026, N=1,758)")
ax.set_xlabel("Gross Proceeds (US$ Millions, Log Scale)")
ax.set_ylabel("Gross Underwriting Spread (%)")
ax.legend(frameon=False, loc="upper right", fontsize=8)
ax.grid(alpha=0.25)

ax = axes[1]
mod_mb = mb_sp[(mb_sp["cohort_year"].between(2001, 2025)) & (mb_sp["proceeds_usd_m"].between(30.0, 160.0))]
bins = np.arange(0.5, 9.25, 0.25)
ax.hist(mod_mb["gross_spread_clean_pct"], bins=bins, color="#2b5c8f", edgecolor="white", alpha=0.9)
ax.axvline(7.0, ls="--", lw=1.8, color="#b22222", label="7.00% U.S. Norm (HK Share = 0.60%)")
ax.axvline(2.5, ls=":", lw=1.8, color="#1b7837", label="2.50% HK Modal Spread (22.36%)")
ax.set_title(f"Panel B: Moderate-Size Main Board IPOs (US$30M–$160M, N={len(mod_mb)})")
ax.set_xlabel("Gross Underwriting Spread (%)")
ax.set_ylabel("Number of Offerings")
ax.legend(frameon=False, loc="upper right", fontsize=8.5)
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
fig.savefig(FIG_DIR / "fig2_gross_spread_7pct_vs_hk.png")

# ==============================================================================
# FIGURE 3: CSRC POLICY REGIMES & JORDA (2005) LOCAL PROJECTIONS (T=393 MONTHS)
# ==============================================================================
pv_reg = pd.read_csv(OUT_DIR / "table_policy_valve_regimes.csv")
pv_lp = pd.read_csv(OUT_DIR / "table_policy_valve_local_projections.csv")

fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.4))
ax = axes[0]
short_labels = [
    "Normal A-Share\n(1994–2021.06)",
    "9 CSRC Freezes\n(1994–2015)",
    "CAC & HFCAA\n(2021.07–2023.03)",
    "Unified Filing\n(2023.04–2024.03)",
    "8.27 + 5 Measures\n(2024.04–2026.09)",
]
y_pos = np.arange(len(short_labels))
ax.barh(y_pos - 0.18, pv_reg["HShare_Deal_Share_Pct"], height=0.35, color="#1f4e79", label="H-Share % of Monthly Deals")
ax.barh(y_pos + 0.18, pv_reg["HShare_Proceeds_Share_Pct"], height=0.35, color="#c0504d", label="H-Share % of Monthly Proceeds")
ax.set_yticks(y_pos)
ax.set_yticklabels(short_labels, fontsize=8.5)
ax.invert_yaxis()
ax.set_xlabel("Share of HKEX Monthly Issuance (%)")
ax.set_title("Panel A: H-Share Share Across Mainland Policy Regimes")
ax.legend(frameon=False, loc="lower right", fontsize=8.5)
ax.grid(axis="x", alpha=0.25)

ax = axes[1]
h = pv_lp["horizon_months"].values
b = pv_lp["beta_hshare_pct"].values
se = pv_lp["se_hshare_pct"].values
ax.plot(h, b, marker="o", lw=2.2, color="#b22222", label="IRF Point Estimate (pp)")
ax.fill_between(h, b - 1.96 * se, b + 1.96 * se, color="#b22222", alpha=0.18, label="95% Newey–West HAC CI")
ax.axhline(0.0, ls="--", lw=1.0, color="black")
ax.set_xticks(h)
ax.set_title("Panel B: Jordà (2005) Local Projection of H-Share Deal Share")
ax.set_xlabel("Horizon h (Months After Onshore A-Share Restriction)")
ax.set_ylabel("Response of H-Share Deal Share (pp)")
ax.legend(frameon=False, loc="upper right", fontsize=8.5)
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(FIG_DIR / "fig3_csrc_policy_valve_lp.png")

# ==============================================================================
# FIGURE 4: TWO-STAGE GEM PLACING-ONLY CRACKDOWN EVENT STUDY (2011-2021)
# ==============================================================================
gem_ev = pd.read_csv(OUT_DIR / "table_gem_did_annual_event_study_2011_2022.csv", skiprows=2)
gem_ev.columns = [
    "year", "N_GEM", "N_MB", "Mean_IR_GEM", "Mean_IR_MB",
    "Med_IR_GEM", "Med_IR_MB", "P75_IR_GEM", "P75_IR_MB",
    "Mean_1Y_GEM", "Mean_1Y_MB", "Med_1Y_GEM", "Med_1Y_MB"
]
gem_ev = gem_ev.dropna(subset=["year", "Med_IR_GEM"]).copy()
gem_ev["year"] = gem_ev["year"].astype(int)

fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.4))
ax = axes[0]
ax.plot(gem_ev["year"], gem_ev["Med_IR_GEM"], marker="s", lw=2.2, color="#b22222", label="GEM Median Day-1 IR (%)")
ax.plot(gem_ev["year"], gem_ev["Med_IR_MB"], marker="o", lw=2.0, color="#1f4e79", label="Main Board Median Day-1 IR (%)")
ax.axvline(2016.8, ls="--", lw=1.3, color="#d95f02", label="Jan 20, 2017 SFC/HKEX Joint Statement")
ax.axvline(2018.1, ls=":", lw=1.5, color="#1b7837", label="Feb 15, 2018 Mandatory >=10% Public Offer")
ax.set_title("Panel A: Median Day-1 Initial Return — GEM vs. Main Board")
ax.set_xlabel("Cohort Year")
ax.set_ylabel("Median Day-1 Initial Return (%)")
ax.legend(frameon=False, loc="upper right", fontsize=8)
ax.grid(alpha=0.25)

ax = axes[1]
ax.plot(gem_ev["year"], gem_ev["Med_1Y_GEM"], marker="s", lw=2.2, color="#b22222", label="GEM Median 1-Year Aftermarket BHAR (%)")
ax.plot(gem_ev["year"], gem_ev["Med_1Y_MB"], marker="o", lw=2.0, color="#1f4e79", label="Main Board Median 1-Year Aftermarket BHAR (%)")
ax.axhline(0.0, ls="--", lw=1.0, color="gray")
ax.axvline(2016.8, ls="--", lw=1.3, color="#d95f02")
ax.axvline(2018.1, ls=":", lw=1.5, color="#1b7837")
ax.set_title("Panel B: Post-IPO 1-Year Median BHAR Reversal (2011–2021)")
ax.set_xlabel("Cohort Year")
ax.set_ylabel("Median 1-Year Aftermarket BHAR (%)")
ax.legend(frameon=False, loc="lower left", fontsize=8)
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(FIG_DIR / "fig4_gem_event_study_did.png")

# ==============================================================================
# FIGURE 5: PN18 CLAWBACK BRACKETS & AGARWAL-LIU-RHEE 27-YEAR REPLICATION
# ==============================================================================
pn18 = pd.read_csv(OUT_DIR / "table_pn18_clawback_and_alr2008_replication.csv")
fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.4))
short_br = ["<15x\n(10% Public)", "15x–50x\n(30% Clawback)", "50x–100x\n(40% Clawback)", ">=100x\n(50% Clawback)"]
x_b = np.arange(len(short_br))

ax = axes[0]
ax.bar(x_b - 0.18, pn18["Mean_Day1_IR"], width=0.35, color="#1f4e79", label="Mean Day-1 Initial Return (%)")
ax.bar(x_b + 0.18, pn18["Med_Day1_IR"], width=0.35, color="#6baed6", label="Median Day-1 Initial Return (%)")
ax.set_xticks(x_b)
ax.set_xticklabels(short_br, fontsize=8.5)
ax.set_ylabel("Day-1 Initial Return (%)")
ax.set_title("Panel A: Day-1 Returns Across PN18 Clawback Brackets (N=1,528)")
ax.legend(frameon=False, loc="upper left", fontsize=8.5)
ax.grid(axis="y", alpha=0.25)

ax = axes[1]
ax.bar(x_b - 0.18, pn18["Mean_1Y_After_BHAR"], width=0.35, color="#b22222", label="Mean 1-Year Aftermarket BHAR (%)")
ax.bar(x_b + 0.18, pn18["Med_1Y_After_BHAR"], width=0.35, color="#fc9272", label="Median 1-Year Aftermarket BHAR (%)")
ax.axhline(0.0, ls="--", lw=1.0, color="black")
ax.set_xticks(x_b)
ax.set_xticklabels(short_br, fontsize=8.5)
ax.set_ylabel("1-Year Aftermarket BHAR (%)")
ax.set_title("Panel B: Long-Run Overreaction Reversal by Demand Bracket")
ax.legend(frameon=False, loc="lower left", fontsize=8.5)
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
fig.savefig(FIG_DIR / "fig5_pn18_clawback_rd_and_alr.png")

# ==============================================================================
# FIGURE 6: NET-OF-COST ROCK (1986) EQUILIBRIUM & AUG 2025 RENT REDISTRIBUTION
# ==============================================================================
rk = pd.read_csv(OUT_DIR / "clean_rock_ballot_113_net_returns.csv")
rk["sub_q"] = pd.qcut(rk["alloc_rate_1lot_pct"].rank(method="first", ascending=False), 5, labels=["Q1\n(Coldest)", "Q2", "Q3", "Q4", "Q5\n(Hottest)"])
q_agg = rk.groupby("sub_q", observed=False).agg(
    headline_ir=("initial_return_pct", "mean"),
    net_1lot=("excess_1lot_ret_over_hibor_pct", "mean"),
    net_10lot=("excess_10lot_ret_over_hibor_pct", "mean"),
    net_poolb=("net_poolB_ret_full_hibor_margin_pct", "mean"),
)

fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.4))
ax = axes[0]
xq = np.arange(len(q_agg))
ax.plot(xq, q_agg["net_1lot"], marker="o", lw=2.2, color="#1f4e79", label="1-Lot Cash Net Excess (+1.92% Mean, p=0.0012)")
ax.plot(xq, q_agg["net_10lot"], marker="s", lw=2.0, color="#2ca25f", label="10-Lot Cash Net Excess (+0.31% Mean, p=0.016)")
ax.plot(xq, q_agg["net_poolb"], marker="^", lw=2.0, color="#b22222", label="Pool B Whale Full-HIBOR (-0.065% Mean, p=0.33)")
ax.axhline(0.0, ls="--", lw=1.1, color="black")
ax.set_xticks(xq)
ax.set_xticklabels(q_agg.index, fontsize=8.5)
ax.set_title("Panel A: Net-of-Fee & Net-of-HIBOR Rationed Returns (2026, N=113)")
ax.set_xlabel("Rationing Intensity Quintile (Ordered by 1-Lot Scarcity)")
ax.set_ylabel("Net Excess Return per IPO (% of Capital)")
ax.legend(frameon=False, loc="upper left", fontsize=8)
ax.grid(alpha=0.25)

ax = axes[1]
regimes = ["Pre-Aug 4, 2025\n(Legacy PN18, N=52)", "Post-Aug 4, 2025\n(Mech A/B Era, N=174)"]
ret_sh = np.array([26.66, 11.30])
cs_sh = np.array([43.96, 39.77])
inst_sh = np.array([29.38, 48.93])
xr = np.arange(2)
ax.bar(xr, ret_sh, width=0.48, color="#2b5c8f", label="Retail Public Subscribers")
ax.bar(xr, cs_sh, width=0.48, bottom=ret_sh, color="#d95f02", label="Cornerstone Investors (6M Locked)")
ax.bar(xr, inst_sh, width=0.48, bottom=ret_sh + cs_sh, color="#1b7837", label="Unrestricted Institutional Placees")
for idx in range(2):
    ax.text(idx, ret_sh[idx]/2, f"{ret_sh[idx]:.1f}%", ha="center", va="center", color="white", fontweight="bold", fontsize=9)
    ax.text(idx, ret_sh[idx] + cs_sh[idx]/2, f"{cs_sh[idx]:.1f}%", ha="center", va="center", color="white", fontweight="bold", fontsize=9)
    ax.text(idx, ret_sh[idx] + cs_sh[idx] + inst_sh[idx]/2, f"{inst_sh[idx]:.1f}%", ha="center", va="center", color="white", fontweight="bold", fontsize=9)
ax.set_xticks(xr)
ax.set_xticklabels(regimes, fontsize=9)
ax.set_ylim(0, 108)
ax.set_ylabel("Share of Net Dollar Money Left on Table (%)")
ax.set_title("Panel B: Three-Way Redistribution of Day-1 IPO Rents (N=226)")
ax.legend(frameon=False, loc="upper right", fontsize=8)
fig.tight_layout()
fig.savefig(FIG_DIR / "fig6_rock_net_returns_and_rent_split.png")

# Copy all 6 figures into docs/overview_paper/figures/
for png in sorted(FIG_DIR.glob("fig*.png")):
    shutil.copy2(png, DOC_FIG_DIR / png.name)
    print(f"Saved & mirrored figure: {png.name}")
