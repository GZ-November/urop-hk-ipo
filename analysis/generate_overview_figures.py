#!/usr/bin/env python3
"""
Generate Publication-Grade Figures (Figures 1-8) for the 1994-2026 HK IPO Overview Monograph.
Outputs both vector PDF and 300-DPI PNG to docs/overview_paper/figures/.
Reads strictly from verified CSV datasets in analysis/out/overview_1994_2026/.
"""
import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DATA = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026"
FIG_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/docs/overview_paper/figures"
os.makedirs(FIG_DIR, exist_ok=True)

# Set JFE / RFS academic publication styling
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "Georgia"],
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 8.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.22,
    "grid.linestyle": "--",
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

NAVY = "#1B365D"
CRIMSON = "#A61C1C"
FOREST = "#2E6F40"
SLATE = "#5C6B73"
OCHRE = "#C87D20"
LIGHT_NAVY = "#4A777A"


def save_fig(fig, stem):
    pdf_path = os.path.join(FIG_DIR, f"{stem}.pdf")
    png_path = os.path.join(FIG_DIR, f"{stem}.png")
    fig.savefig(pdf_path)
    fig.savefig(png_path, dpi=300)
    plt.close(fig)
    print(f"Saved: {stem}.pdf & {stem}.png")


# Load core datasets
df33 = pd.read_csv(os.path.join(OUT_DATA, "hkipo_33y_master_panel_1994_2026_tier1_complete.csv"), low_memory=False)
t5 = pd.read_csv(os.path.join(OUT_DATA, "table5_us_hk_parallel_clean_1994_2026.csv"))
lp = pd.read_csv(os.path.join(OUT_DATA, "table_policy_valve_local_projections.csv"))
pv_reg = pd.read_csv(os.path.join(OUT_DATA, "table_policy_valve_regimes.csv"))
t15 = pd.read_csv(os.path.join(OUT_DATA, "table15_33y_longrun_bhar_complete.csv"))
rock = pd.read_csv(os.path.join(OUT_DATA, "clean_rock_ballot_113_net_returns.csv"))


# ==============================================================================
# FIGURE 1: 33-Year Parallel IPO Volume & Initial Returns (HK vs. U.S. Ritter)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10.5, 7.2), sharex=True)
years = t5["Year"].values

# Panel A: Annual IPO Counts
ax1.bar(years - 0.18, t5["HK_MB_N"], width=0.36, color=NAVY, label="HKEX Main Board IPOs", zorder=3)
ax1.bar(years - 0.18, t5["HK_GEM_N"].fillna(0), bottom=t5["HK_MB_N"], width=0.36, color=OCHRE, alpha=0.85, label="HKEX GEM IPOs", zorder=3)
ax1_r = ax1.twinx()
ax1_r.spines["top"].set_visible(False)
ax1_r.plot(years, t5["US_Ritter_N"], color=CRIMSON, marker="o", markersize=4, linewidth=1.8, linestyle="-", label="U.S. Operating IPOs (Ritter, Right Axis)", zorder=4)
ax1.set_ylabel("HKEX Annual IPO Count")
ax1_r.set_ylabel("U.S. Operating IPO Count (Ritter)", color=CRIMSON)
ax1_r.tick_params(axis="y", labelcolor=CRIMSON)
ax1.set_title("Panel A: Secular Divergence in Annual IPO Volume — Hong Kong Expansion (+77%) vs. U.S. Listing Contraction (-75%)")

ax1.set_ylim(0, 240)
# Combine legends
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax1_r.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc="upper center", ncol=2, frameon=True, facecolor="white", framealpha=0.92)

# Annotate key structural breaks
for yr, lbl in [(1999.8, "GEM\nLaunch"), (2018.3, "Ch. 8A/18A\nReform"), (2023.2, "CSRC Unified\nFiling")]:
    ax1.axvline(yr, color=SLATE, linestyle=":", linewidth=1.1, alpha=0.85)
    ax1.text(yr + 0.15, 202, lbl, fontsize=7.8, color=SLATE, va="top")

# Panel B: Equal-Weighted Initial Returns
ax2.plot(years, t5["HK_MB_EW_IR_Pct"], color=NAVY, marker="s", markersize=4, linewidth=1.9, label="HKEX Main Board EW Initial Return (%)")
ax2.plot(years, t5["US_EW_IR_Pct"], color=CRIMSON, marker="^", markersize=4, linewidth=1.6, linestyle="--", label="U.S. Operating IPOs EW Initial Return (%)")
ax2.axhline(10.29, color=NAVY, linestyle=":", alpha=0.6, linewidth=1.0, label="HK MB 1994–2025 Mean (10.3%)")
ax2.axhline(20.49, color=CRIMSON, linestyle=":", alpha=0.6, linewidth=1.0, label="U.S. 1994–2025 Mean (20.5%)")
ax2.set_ylabel("Equal-Weighted Day-1 Return (%)")
ax2.set_xlabel("Listing Year (2026 through Q3)")
ax2.set_title("Panel B: Equal-Weighted First-Day Initial Returns — Hong Kong Main Board vs. United States (1994–2026)")
ax2.set_xticks(np.arange(1994, 2027, 2))
ax2.legend(loc="upper right", ncol=2, frameon=True, facecolor="white", framealpha=0.9)

fig.tight_layout()
save_fig(fig, "fig1_us_hk_parallel_33y")


# ==============================================================================
# FIGURE 2: Three Methodological Pitfalls in HK IPO Return Measurement
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.8, 4.4))

# Panel A: Pitfall 1 — Reverse-Split Inflation across Main Board Epochs
mb = df33[df33["board"] == "Main Board"].copy()
ep_order = ["Epoch II (1994–2004)", "Epoch III (2005–2017)", "Epoch IV (2018–2022)", "Epoch V (2023–2026)"]
# Normalize epoch labels if hyphen differs
mb["ep_norm"] = mb["epoch"].astype(str).str.replace("-", "–")
naive_means, clean_means, ep_short = [], [], ["1994–2004\n(Epoch II)", "2005–2017\n(Epoch III)", "2018–2022\n(Epoch IV)", "2023–2026\n(Epoch V)"]
for ep_prefix in ["Epoch II ", "Epoch III", "Epoch IV", "Epoch V"]:
    sub = mb[mb["epoch"].astype(str).str.startswith(ep_prefix)].dropna(subset=["hkex_ir_close_pct", "ir_close_pct"])
    naive_means.append(sub["hkex_ir_close_pct"].mean())
    clean_means.append(sub["ir_close_pct"].mean())

x = np.arange(len(ep_short))
w = 0.35
b1 = ax1.bar(x - w/2, naive_means, width=w, color=CRIMSON, alpha=0.85, label="Naive Backward-Adjusted API Return (%)")
b2 = ax1.bar(x + w/2, clean_means, width=w, color=NAVY, label="Split-Clean Contemporaneous Return (%)")
for idx in range(len(x)):
    diff = naive_means[idx] - clean_means[idx]
    if diff > 2.0:
        ax1.annotate(f"+{diff:.1f} pp\nbias", xy=(x[idx] - w/2, naive_means[idx]),
                     xytext=(x[idx] - w/2, naive_means[idx] + 2.2), ha="center", fontsize=8, color=CRIMSON, fontweight="bold")
ax1.set_xticks(x)
ax1.set_xticklabels(ep_short)
ax1.set_ylim(0, max(naive_means) * 1.24)
ax1.set_ylabel("Mean Day-1 Initial Return (%)")
ax1.set_title("Panel A: Pitfall 1 — Micro-Cap Reverse-Split Bias")
ax1.legend(loc="upper left", frameon=True, facecolor="white")

# Panel B: Pitfall 3 — Active Survivors vs. Delisted/Acquired Issuers
surv = df33[df33["flag_delisted_or_acquired"] == 0]
delist = df33[df33["flag_delisted_or_acquired"] == 1]
metrics_lbl = ["Day-1 Initial Return\n(Offer to 1st Close)", "1-Year Aftermarket BHAR\n(From Day-1 Close vs. HSI)"]
surv_vals = [surv["ir_close_pct"].dropna().mean(), surv["after_bhar_1y_pct"].dropna().mean()]
delist_vals = [delist["ir_close_pct"].dropna().mean(), delist["after_bhar_1y_pct"].dropna().mean()]

x2 = np.arange(2)
ax2.bar(x2 - w/2, surv_vals, width=w, color=NAVY, label=f"Active Numeric Tickers (N={len(surv):,})")
ax2.bar(x2 + w/2, delist_vals, width=w, color=OCHRE, label=f"Delisted / Acquired Tickers (N={len(delist):,})")
ax2.axhline(0, color="black", linewidth=0.8)
for i in range(2):
    wedge = surv_vals[i] - delist_vals[i]
    y_top = max(surv_vals[i], delist_vals[i]) + 2.5
    ax2.text(x2[i], y_top, f"Survivorship Wedge:\n+{wedge:.2f} pp", ha="center", fontsize=8.2, fontweight="bold", color=NAVY)
ax2.set_xticks(x2)
ax2.set_xticklabels(metrics_lbl)
ax2.set_ylim(-20, 52)
ax2.set_ylabel("Equal-Weighted Mean Return (%)")
ax2.set_title("Panel B: Pitfall 3 — Delisting Survivorship Wedge")
ax2.legend(loc="upper right", frameon=True, facecolor="white")

fig.tight_layout()
save_fig(fig, "fig2_three_return_pitfalls")


# ==============================================================================
# FIGURE 3: Mainland Policy Shocks & the "A-Share Freeze Valve" (T = 393 Months)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.5))

# Panel A: Jorda (2005) Local Projections IRF
h = lp["horizon_months"].values
beta = lp["beta_hshare_pct"].values
se = lp["se_hshare_pct"].values
ax1.plot(h, beta, color=NAVY, marker="o", linewidth=2.2, label="IRF Point Estimate (H-Share % of HKEX Deals)")
ax1.fill_between(h, beta - 1.96 * se, beta + 1.96 * se, color=NAVY, alpha=0.18, label="95% Newey-West HAC Confidence Band")
ax1.axhline(0, color="black", linewidth=0.9, linestyle="--")
ax1.set_xticks(h)
ax1.set_xticklabels([f"t+{int(v)}m" for v in h])
ax1.set_xlabel("Months Following Onshore CSRC Issuance Restriction Shock")
ax1.set_ylabel("Change in H-Share Share of HKEX IPOs (pp)")
ax1.set_title("Panel A: Jordà (2005) Dynamic Local Projection IRF")
ax1.legend(loc="lower right", frameon=True, facecolor="white")

# Panel B: Regime Shift Across 5 Policy Eras
era_labels = [
    "Normal Onshore\n(1994–2021.06)",
    "CSRC Freezes 1–9\n(1994–2015)",
    "CAC / US HFCAA\n(2021.07–2023.03)",
    "Unified Filing\n(2023.04–2023.08)",
    "Filing + 8·27 Tight.\n(2023.09–2026.09)"
]
y_pos = np.arange(len(pv_reg))
ax2.barh(y_pos + 0.17, pv_reg["HShare_Deal_Share_Pct"], height=0.34, color=NAVY, label="H-Share % of HKEX Deal Count")
ax2.barh(y_pos - 0.17, pv_reg["HShare_Proceeds_Share_Pct"], height=0.34, color=FOREST, alpha=0.85, label="H-Share % of HKEX Proceeds")
for idx, (v1, v2) in enumerate(zip(pv_reg["HShare_Deal_Share_Pct"], pv_reg["HShare_Proceeds_Share_Pct"])):
    ax2.text(v1 + 1.0, idx + 0.17, f"{v1:.1f}%", va="center", fontsize=8, color=NAVY, fontweight="bold")
    ax2.text(v2 + 1.0, idx - 0.17, f"{v2:.1f}%", va="center", fontsize=8, color=FOREST)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(era_labels, fontsize=8.5)
ax2.invert_yaxis()
ax2.set_xlim(0, 82)
ax2.set_xlabel("PRC Direct H-Share Share (%)")
ax2.set_title("Panel B: Structural Shift Under Post-2023 Unified Filing")
ax2.legend(loc="upper right", frameon=True, facecolor="white")

fig.tight_layout()
save_fig(fig, "fig3_policy_valve_jorda_lp")


# ==============================================================================
# FIGURE 4: Absence of the U.S. "7% Solution" & 33-Year Gross Spread Curve
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.5))

df33["proceeds_hkd_m"] = np.where(
    df33["funds_raised_total_hkd"].notna() & (df33["funds_raised_total_hkd"] > 0),
    df33["funds_raised_total_hkd"] / 1e6,
    df33["bbg_offer_size_m"]
)
sp_valid = df33.dropna(subset=["gross_spread_clean_pct", "proceeds_hkd_m"]).copy()
sp_valid = sp_valid[(sp_valid["gross_spread_clean_pct"] > 0) & (sp_valid["gross_spread_clean_pct"] <= 25) & (sp_valid["proceeds_hkd_m"] > 0)]

# Panel A: Moderate-size IPOs ($30M-$160M = HK$234M-1,248M, 2001-2025 Main Board)
mod_hk = sp_valid[
    (sp_valid["board"] == "Main Board") &
    (sp_valid["cohort_year"].between(2001, 2025)) &
    (sp_valid["proceeds_hkd_m"].between(234.0, 1248.0))
]
bins = np.arange(0.75, 9.25, 0.5)
ax1.hist(mod_hk["gross_spread_clean_pct"], bins=bins, weights=np.ones(len(mod_hk)) / len(mod_hk) * 100,
         color=NAVY, edgecolor="white", alpha=0.88, label=f"HK Main Board Moderate Deals\n(USD 30M–160M, N={len(mod_hk)})")
ax1.axvline(2.5, color=FOREST, linestyle="--", linewidth=1.6, label="HK Historical Brokerage Norm (2.50%: 22.4%)")
ax1.axvline(7.0, color=CRIMSON, linestyle="-.", linewidth=1.8, label="U.S. '7% Solution' Benchmark (HK: 0.6% vs. U.S.: 93.3%)")
ax1.set_xlabel("Gross Underwriting Spread (%)")
ax1.set_ylabel("Percentage of Moderate-Size Deals (%)")
ax1.set_title("Panel A: Absence of the U.S. 7% Clustering in Hong Kong")
ax1.legend(loc="upper right", fontsize=8, frameon=True, facecolor="white")

# Panel B: Binned Scale Curve (Main Board vs. GEM Pre/Post 2018)
mb_sp = sp_valid[sp_valid["board"] == "Main Board"].copy()
mb_sp["size_bin"] = pd.qcut(np.log10(mb_sp["proceeds_hkd_m"]), q=12, duplicates="drop")
b_stats = mb_sp.groupby("size_bin", observed=True).agg(
    med_proc=("proceeds_hkd_m", "median"),
    mean_sp=("gross_spread_clean_pct", "mean"),
    se_sp=("gross_spread_clean_pct", lambda s: s.std() / np.sqrt(len(s)))
)
ax2.errorbar(b_stats["med_proc"], b_stats["mean_sp"], yerr=1.96 * b_stats["se_sp"],
             fmt="o-", color=NAVY, linewidth=1.8, markersize=5, capsize=3, label="Main Board Scale Curve (12 Quantile Bins)")

gem_pre = sp_valid[(sp_valid["board"] == "GEM") & (sp_valid["cohort_year"] <= 2017)]
gem_post = sp_valid[(sp_valid["board"] == "GEM") & (sp_valid["cohort_year"] >= 2018)]
ax2.scatter([gem_pre["proceeds_hkd_m"].median()], [gem_pre["gross_spread_clean_pct"].mean()],
            color=OCHRE, marker="s", s=75, zorder=5, label=f"GEM Pre-2018 Crackdown Mean ({gem_pre['gross_spread_clean_pct'].mean():.2f}%, N={len(gem_pre)})")
ax2.scatter([gem_post["proceeds_hkd_m"].median()], [gem_post["gross_spread_clean_pct"].mean()],
            color=CRIMSON, marker="D", s=75, zorder=5, label=f"GEM Post-2018 Reform Mean ({gem_post['gross_spread_clean_pct'].mean():.2f}%, N={len(gem_post)})")
ax2.annotate("Post-2018 GEM\nSpread Doubling", xy=(gem_post["proceeds_hkd_m"].median(), gem_post["gross_spread_clean_pct"].mean()),
             xytext=(gem_post["proceeds_hkd_m"].median() * 2.2, gem_post["gross_spread_clean_pct"].mean() - 0.3),
             arrowprops=dict(arrowstyle="->", color=CRIMSON, lw=1.2), fontsize=8.2, fontweight="bold", color=CRIMSON)
ax2.set_xscale("log")
ax2.set_xlabel("Gross Proceeds (HK$ Millions, Log Scale)")
ax2.set_ylabel("Mean Gross Spread (%)")
ax2.set_title("Panel B: Underwriting Economies of Scale & GEM Fee Shift")
ax2.legend(loc="upper right", fontsize=7.8, frameon=True, facecolor="white")

fig.tight_layout()
save_fig(fig, "fig4_gross_spread_absence_of_7pct")


# ==============================================================================
# FIGURE 5: GEM Placing-Only Manipulation Bubble & Two-Stage Crackdown DiD
# ==============================================================================
gem_win = df33[df33["cohort_year"].between(2011, 2022)].dropna(subset=["ir_close_pct"]).copy()
gem_win["log_ir"] = np.log1p(np.maximum(gem_win["ir_close_pct"] / 100.0, -0.95))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.5), sharex=True)
yrs_did = np.arange(2011, 2023)

for brd, col, mk in [("GEM", CRIMSON, "o"), ("Main Board", NAVY, "s")]:
    sub = gem_win[gem_win["board"] == brd]
    ann = sub.groupby("cohort_year").agg(
        mean_log=("log_ir", "mean"),
        se_log=("log_ir", lambda s: s.std() / np.sqrt(len(s)) if len(s) > 1 else 0.0),
        med_ir=("ir_close_pct", "median"),
        n=("log_ir", "size")
    ).reindex(yrs_did)
    ax1.errorbar(yrs_did, ann["mean_log"], yerr=1.96 * ann["se_log"], fmt=f"{mk}-", color=col,
                 linewidth=1.9, markersize=5, capsize=2.5, label=f"{brd} Mean log(1 + IR)")
    ax2.plot(yrs_did, ann["med_ir"], f"{mk}-", color=col, linewidth=1.9, markersize=5, label=f"{brd} Median Day-1 IR (%)")

for ax in (ax1, ax2):
    ax.axvline(2017.05, color=CRIMSON, linestyle="--", linewidth=1.4, label="Jan 20, 2017 SFC/HKEX Joint Statement")
    ax.axvline(2018.12, color=FOREST, linestyle=":", linewidth=1.4, label="Feb 15, 2018 Mandatory 10% Public Offer")
    ax.set_xticks(yrs_did)
    ax.set_xticklabels(yrs_did, rotation=45)
    ax.set_xlabel("Listing Year")

ax1.set_ylabel("Mean Log Initial Return log(1 + IR)")
ax1.set_title("Panel A: Event-Study Log Initial Return (Unbundled 2017 Break)")
ax1.legend(loc="upper right", fontsize=7.8, frameon=True, facecolor="white")

ax2.set_ylabel("Median (Q50) Day-1 Initial Return (%)")
ax2.set_title("Panel B: Median (Q50) Initial Return (Non-Outlier Proof)")
ax2.legend(loc="upper right", fontsize=7.8, frameon=True, facecolor="white")

fig.tight_layout()
save_fig(fig, "fig5_gem_placing_bubble_did")


# ==============================================================================
# FIGURE 6: Practice Note 18 Clawback RD at the 15x Threshold (1998-2025.07)
# ==============================================================================
pn18 = df33[
    (df33["board"] == "Main Board") &
    (pd.to_datetime(df33["listing_date"]) >= "1998-06-01") &
    (pd.to_datetime(df33["listing_date"]) < "2025-08-04")
].dropna(subset=["retail_sub_ratio_clean", "ir_close_pct"]).copy()
pn18 = pn18[pn18["retail_sub_ratio_clean"] > 0].copy()
pn18["log_ir"] = np.log1p(np.maximum(pn18["ir_close_pct"] / 100.0, -0.95))
pn18["rv"] = np.log(pn18["retail_sub_ratio_clean"]) - np.log(15.0)

rd_sub = pn18[pn18["rv"].abs() <= 1.15].copy()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.4))

# Panel A: Binned scatter + Local linear fit on each side of 0
bins_rd = np.linspace(-1.15, 1.15, 17)
rd_sub["bin"] = pd.cut(rd_sub["rv"], bins=bins_rd)
b_rd = rd_sub.groupby("bin", observed=True).agg(x=("rv", "mean"), y=("log_ir", "mean"), n=("log_ir", "size")).dropna()
ax1.scatter(b_rd["x"], b_rd["y"], s=b_rd["n"] * 2.2, color=SLATE, alpha=0.8, edgecolor="black", linewidth=0.6, label="Binned Means (Size prop. to N)")

left = rd_sub[rd_sub["rv"] < 0]
right = rd_sub[rd_sub["rv"] >= 0]
for side_df, col, lbl in [(left, NAVY, "Below 15x (10% Public Tranche)"), (right, CRIMSON, "At/Above 15x (30% Clawback Tranche)")]:
    coef = np.polyfit(side_df["rv"], side_df["log_ir"], 1)
    xs = np.linspace(side_df["rv"].min(), side_df["rv"].max(), 50)
    ax1.plot(xs, np.polyval(coef, xs), color=col, linewidth=2.2, label=lbl)

rd_bw65 = pn18[pn18["rv"].abs() <= 0.65].copy()
rd_bw65["above"] = (rd_bw65["retail_sub_ratio_clean"] >= 15.0).astype(int)
rd_fit65 = smf.ols("log_ir ~ above * rv", data=rd_bw65).fit(cov_type="HC3")
rd_jmp = float(rd_fit65.params["above"])
rd_pct = (np.exp(rd_jmp) - 1.0) * 100.0
rd_t = float(rd_fit65.tvalues["above"])
rd_p = float(rd_fit65.pvalues["above"])

ax1.axvline(0.0, color="black", linestyle="--", linewidth=1.2)
ax1.set_ylim(-0.11, 0.28)
ax1.annotate(f"RD Jump at 15x (|rv|<=0.65):\n{rd_jmp:+.3f} log pts ({rd_pct:+.1f}%)\n(t = {rd_t:.2f}, p = {rd_p:.4f})",
             xy=(0.0, 0.055), xytext=(0.18, 0.165),
             arrowprops=dict(arrowstyle="->", color=CRIMSON, lw=1.3),
             fontsize=8.2, fontweight="bold", color=CRIMSON,
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=CRIMSON, alpha=0.92))
ax1.set_xlabel("Centered Log Subscription Ratio: log(Sub Ratio) - log(15)")
ax1.set_ylabel("Mean Log Initial Return log(1 + IR)")
ax1.set_title("Panel A: Local Linear RD at PN18 15x Clawback Threshold")
ax1.legend(loc="upper left", fontsize=7.8, frameon=True, facecolor="white")

# Panel B: Density Histogram around 15x
sub_hist = pn18[pn18["retail_sub_ratio_clean"].between(3, 30)]
n_b12 = int(((pn18["retail_sub_ratio_clean"] >= 12.0) & (pn18["retail_sub_ratio_clean"] < 15.0)).sum())
n_a15 = int(((pn18["retail_sub_ratio_clean"] >= 15.0) & (pn18["retail_sub_ratio_clean"] <= 18.0)).sum())
p_dens = float(stats.binomtest(n_b12, n_b12 + n_a15, 0.5).pvalue)
ax2.hist(sub_hist["retail_sub_ratio_clean"], bins=np.arange(3, 31, 1.5), color=NAVY, alpha=0.82, edgecolor="white")
ax2.axvline(15.0, color=CRIMSON, linestyle="--", linewidth=1.8, label=f"15x Clawback Cutoff\n([12x,15x): {n_b12} vs [15x,18x]: {n_a15}, p={p_dens:.2f})")
ax2.set_xlabel("Retail Subscription Ratio (Times)")
ax2.set_ylabel("Number of Main Board IPOs")
ax2.set_title("Panel B: Density Test Around 15x Threshold (No Manipulation)")
ax2.legend(loc="upper right", fontsize=8.2, frameon=True, facecolor="white")

fig.tight_layout()
save_fig(fig, "fig6_pn18_clawback_rd_15x")


# ==============================================================================
# FIGURE 7: Rock (1986) Rationing Curve & Net-of-Cost Retail Equilibrium (N=113)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.5))

# Panel A: Allocation Rate vs Initial Return Quantile Bins
rock["ir_bin"] = pd.qcut(rock["initial_return_pct"], q=5, duplicates="drop")
r_bin = rock.groupby("ir_bin", observed=True).agg(
    mean_ir=("initial_return_pct", "mean"),
    a1=("alloc_rate_1lot_pct", "mean"),
    a10=("alloc_rate_10lot_pct", "mean"),
    ab=("alloc_rate_poolB_min_pct", "mean")
)
x_q = np.arange(len(r_bin))
q_lbls = [f"Q{i+1}\n({v:+.1f}%)" for i, v in enumerate(r_bin["mean_ir"])]
ax1.plot(x_q, r_bin["a1"], "o-", color=NAVY, linewidth=2.0, markersize=6, label="1-Lot Cash Applicant (Pool A Small)")
ax1.plot(x_q, r_bin["a10"], "s--", color=FOREST, linewidth=1.8, markersize=5, label="10-Lot Cash Applicant (Pool A Medium)")
ax1.plot(x_q, r_bin["ab"], "^:", color=CRIMSON, linewidth=1.8, markersize=6, label="Pool B Min Whale (>HK$5M Subscription)")
ax1.set_xticks(x_q)
ax1.set_xticklabels(q_lbls)
ax1.set_xlabel("Day-1 Initial Return Quintile (Mean Return in Parentheses)")
ax1.set_ylabel("Mean Share Allocation Rate (%)")
ax1.set_title("Panel A: Winner's Curse Adverse Selection Across Ballot Tiers")
ax1.legend(loc="upper right", frameon=True, facecolor="white")

# Panel B: Mean Net-of-Fee & Net-of-HIBOR Per-Deal Excess Return with 95% CIs
tiers = [
    ("1-Lot Cash\n(FINI HKID Capped)", rock["excess_1lot_ret_over_hibor_pct"].dropna(), NAVY),
    ("10-Lot Cash\n(Pool A Medium)", rock["excess_10lot_ret_over_hibor_pct"].dropna(), FOREST),
    ("Pool B Whale\n(Flat HK$100 Fee)", rock["net_poolB_ret_flat_margin_pct"].dropna(), OCHRE),
    ("Pool B Whale\n(Full HIBOR Loan)", rock["net_poolB_ret_full_hibor_margin_pct"].dropna(), CRIMSON),
]
tx = np.arange(len(tiers))
means = [s.mean() for _, s, _ in tiers]
cis = [1.96 * s.std() / np.sqrt(len(s)) for _, s, _ in tiers]
cols_t = [c for _, _, c in tiers]

ax2.bar(tx, means, yerr=cis, width=0.52, color=cols_t, alpha=0.88, capsize=4, edgecolor="black", linewidth=0.6)
ax2.axhline(0, color="black", linewidth=1.0, linestyle="--")
for i, (m_val, ci_val) in enumerate(zip(means, cis)):
    offset = ci_val + 0.14 if m_val >= 0 else -(ci_val + 0.28)
    ax2.text(i, m_val + offset, f"{m_val:+.2f}%", ha="center", fontsize=8.5, fontweight="bold", color=cols_t[i])
ax2.set_xticks(tx)
ax2.set_xticklabels([lbl for lbl, _, _ in tiers], fontsize=8.3)
ax2.set_ylim(-0.65, 3.45)
ax2.set_ylabel("Net Excess Return per Deal on Committed Capital (%)")
ax2.set_title("Panel B: Net-of-Cost Rock (1986) Equilibrium (N = 113 IPOs)")

fig.tight_layout()
save_fig(fig, "fig7_rock_rationing_and_net_returns")


# ==============================================================================
# FIGURE 8: 33-Year Long-Run Aftermarket BHAR (1-Year Horizon, Main Board vs GEM)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 4.5), sharey=False)

for ax, brd, title_tag in [
    (ax1, "Main Board", "Panel A: Main Board 1-Year Aftermarket BHAR (%)"),
    (ax2, "GEM", "Panel B: GEM 1-Year Aftermarket BHAR (%)")
]:
    sub = t15[(t15["Board"] == brd) & (t15["N_1Y"] >= 5)].copy()
    lbls = [
        e.replace("Epoch I (1994-1999)", "1994–1999")
         .replace("Epoch II (2000-2007)", "2000–2007")
         .replace("Epoch III (2008-2017)", "2008–2017")
         .replace("Epoch IV (2018-2022)", "2018–2022")
         .replace("Epoch V (2023-2026Q3)", "2023–2026")
         .replace("All 1994-2026", "All\n1994–2026")
        for e in sub["Epoch"]
    ]
    xb = np.arange(len(sub))
    wb = 0.26
    ax.bar(xb - wb, sub["EW_1Y_BHAR_Pct"], width=wb, color=NAVY, label="Equal-Weighted (EW)")
    ax.bar(xb, sub["VW_1Y_BHAR_Pct"], width=wb, color=FOREST, label="Proceeds-Weighted (VW)")
    ax.bar(xb + wb, sub["Med_1Y_BHAR_Pct"], width=wb, color=CRIMSON, alpha=0.85, label="Median (Q50)")
    ax.axhline(0, color="black", linewidth=0.9)
    ax.set_xticks(xb)
    ax.set_xticklabels(lbls, fontsize=8.3)
    ax.set_ylabel("1-Year BHAR from Day-1 Close vs. HSI (%)")
    ax.set_title(title_tag)
    ax.legend(loc="best", fontsize=8, frameon=True, facecolor="white")

fig.tight_layout()
save_fig(fig, "fig8_longrun_bhar_5epochs")
print("All 8 core figures generated successfully!")
