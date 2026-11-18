#!/usr/bin/env python3
"""
Generate Extension Figures 9 & 10 (Vector PDF + 300-DPI PNG) in docs/overview_paper/figures/:
- Figure 9: Convex Demand Spillover Curve (PN18 Supply Buffer vs Dual-Cap Saturation) & 33-Year Stabilization Discontinuity at P0
- Figure 10: Ritter (1987) Total Direct Going-Public Cost Decomposition (UW Spread vs Legal/Audit/Sponsor Overhead) & VC/State Backing
"""
import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

IN_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026"
EXT_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_extensions"
FIG_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/docs/overview_paper/figures"
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "Georgia"],
    "font.size": 10,
    "axes.titlesize": 10.8,
    "axes.titleweight": "bold",
    "axes.labelsize": 9.8,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.8,
    "legend.fontsize": 8.0,
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


def save_fig(fig, stem):
    fig.savefig(os.path.join(FIG_DIR, f"{stem}.pdf"))
    fig.savefig(os.path.join(FIG_DIR, f"{stem}.png"), dpi=300)
    plt.close(fig)
    print(f"Saved: {stem}.pdf & {stem}.png")


df33 = pd.read_csv(os.path.join(IN_DIR, "hkipo_33y_master_panel_1994_2026_tier1_complete.csv"), low_memory=False)
spill = pd.read_csv(os.path.join(EXT_DIR, "ext_table2_convex_demand_spillover.csv"))
cost_tab = pd.read_csv(os.path.join(EXT_DIR, "ext_table7_ritter1987_direct_cost_decomposition.csv"))
vc_tab = pd.read_csv(os.path.join(EXT_DIR, "ext_table5_vc_state_and_fundamentals_by_route.csv"))

# ==============================================================================
# FIGURE 9: Convex Demand Spillover & 33-Year Zero-Return Stabilization Peg
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.4, 4.6))

# Panel A: 7-Tier Convex Spillover & 1Y Reversal
x = np.arange(len(spill))
short_tiers = ["<1x", "1–5x", "5–15x\n(No Claw)", "15–50x\n(30% Claw)", "50–100x\n(40% Claw)", "100–500x\n(50% Max)", ">=500x\n(Saturated)"]
ax1.plot(x, spill["Mean_Open_Jump_Pct"], "o-", color=NAVY, linewidth=2.1, markersize=5.5, label="Day-1 Opening Jump (%)")
ax1.plot(x, spill["Mean_Intraday_Ret_Pct"], "s:", color=SLATE, linewidth=1.6, markersize=4.5, label="Day-1 Intraday Drift (%)")
ax1.plot(x, spill["Mean_1Y_BHAR_Pct"], "^--", color=CRIMSON, linewidth=2.0, markersize=5.5, label="1-Year Aftermarket BHAR (%)")
ax1.axhline(0, color="black", linewidth=0.8)
ax1.axvspan(2.5, 4.5, color=FOREST, alpha=0.09, label="PN18 Clawback Supply Buffer (15x–100x)")
ax1.set_xticks(x)
ax1.set_xticklabels(short_tiers, fontsize=8)
ax1.set_xlabel(f"Retail Subscription Ratio Tier (Main Board, N = {int(spill['N'].sum()):,})")
ax1.set_ylabel("Equal-Weighted Mean Return (%)")
ax1.set_title("Panel A: Hard-Cap Spillover, Clawback Buffer & 1Y Reversal")
ax1.legend(loc="upper left", frameon=True, facecolor="white")

# Panel B: Day-1 Return Histogram Around 0.00% + Zero-Greenshoe Overlay
sub_ir = df33[df33["ir_close_pct"].between(-12.0, 16.0)].copy()
n_exact_zero = int(df33["ir_close_pct"].between(-0.05, 0.05).sum())
bins_z = np.arange(-12.0, 16.5, 1.0)
ax2.hist(sub_ir["ir_close_pct"], bins=bins_z, color=NAVY, alpha=0.82, edgecolor="white", label="Deal Count (1% Return Bins)")
ax2.axvline(0.0, color=CRIMSON, linestyle="--", linewidth=1.6, label=f"Offer Price P0 ({n_exact_zero} Exact 0% Closes; p = 1.2e-29)")

# Compute zero-shoe share across coarse bins on twin axis
gs_sub = sub_ir[sub_ir["greenshoe_facility_m"] > 0].copy()
gs_sub["zero_shoe"] = (gs_sub["greenshoe_shares_exercised_m"] == 0).astype(float) * 100.0
coarse_bins = [-12, -6, -2, -0.05, 1.0, 4.0, 8.0, 16.0]
gs_sub["cbin"] = pd.cut(gs_sub["ir_close_pct"], bins=coarse_bins)
gs_curve = gs_sub.groupby("cbin", observed=True).agg(mid=("ir_close_pct", "mean"), zs=("zero_shoe", "mean")).dropna()

ax2_r = ax2.twinx()
ax2_r.spines["top"].set_visible(False)
ax2_r.plot(gs_curve["mid"], gs_curve["zs"], "D-", color=OCHRE, linewidth=2.0, markersize=5.5, label="% Deals with Zero Greenshoe Exercised (Right)")
ax2_r.set_ylabel("Zero Greenshoe Exercise Rate (%)", color=OCHRE)
ax2_r.tick_params(axis="y", labelcolor=OCHRE)
ax2_r.set_ylim(0, 100)

ax2.set_xlabel("Day-1 Initial Return Around Offer Price (%)")
ax2.set_ylabel(f"Number of IPOs (N = {len(sub_ir):,} in [-12%, +16%])")
ax2.set_title("Panel B: Price Stabilization Spike at P0 & Greenshoe Non-Exercise")

h1, l1 = ax2.get_legend_handles_labels()
h2, l2 = ax2_r.get_legend_handles_labels()
ax2.legend(h1 + h2, l1 + l2, loc="upper right", fontsize=7.6, frameon=True, facecolor="white")

fig.tight_layout()
save_fig(fig, "fig9_hardcap_convex_spillover_and_stabilization")


# ==============================================================================
# FIGURE 10: Ritter (1987) Direct Going-Public Cost Decomposition & VC/State Backing
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.4, 4.6))

# Panel A: Stacked Bar of UW Spread vs Non-UW Fixed Overhead
c_q = cost_tab.iloc[:4].copy()
n_cost_tot = int(cost_tab.loc[cost_tab["Deal_Size_Quartile"].str.contains("All"), "N"].iloc[0]) if (cost_tab["Deal_Size_Quartile"].str.contains("All")).any() else int(c_q["N"].sum())
xq = np.arange(len(c_q))
q_labels_short = ["Q1 Smallest", "Q2 Lower-Mid", "Q3 Upper-Mid", "Q4 Largest"]
q_names = [
    f"{ql}\n(Med HK${med/1000:.2f}B)" if med >= 1000 else f"{ql}\n(Med HK${med:.0f}M)"
    for ql, med in zip(q_labels_short, c_q["Med_Proceeds_HKDm"])
]
ax1.bar(xq, c_q["Mean_UW_Spread_Pct"], width=0.52, color=NAVY, label="Explicit Underwriting Commission (%)")
ax1.bar(xq, c_q["Mean_NonUW_Legal_Audit_Sponsor_Pct"], bottom=c_q["Mean_UW_Spread_Pct"], width=0.52,
        color=OCHRE, alpha=0.88, label="Non-UW Legal, Audit & Joint-Sponsor Overhead (%)")
for i, tot in enumerate(c_q["Mean_Total_Direct_Cost_Pct"]):
    ax1.text(i, tot + 0.45, f"Total: {tot:.1f}%", ha="center", fontsize=8.5, fontweight="bold", color=NAVY)
ax1.set_xticks(xq)
ax1.set_xticklabels(q_names, fontsize=8.2)
ax1.set_ylim(0, 21.5)
ax1.set_ylabel("Share of Gross IPO Proceeds (%)")
ax1.set_title(f"Panel A: Ritter (1987) Total Direct Cost Decomposition (N = {n_cost_tot})")
ax1.legend(loc="upper right", frameon=True, facecolor="white")

# Panel B: VC/PE vs Municipal/State Guidance Fund & SOE Cornerstone by Listing Route
v_sub = vc_tab.iloc[:4].copy()
xr = np.arange(len(v_sub))
route_short = {
    "1. Ch. 18A Pre-Revenue Biotech": "Ch. 18A Biotech",
    "2. Ch. 18C Specialist Hard-Tech": "Ch. 18C Hard-Tech",
    "3. A+H Dual-Listed (Conventional)": "A+H Dual",
    "4. Standard Main Board (Rule 8.05 / 8A)": "Standard MB",
}
r_names = [f"{route_short.get(r['Listing_Route'], r['Listing_Route'])}\n(N={int(r['N'])})" for _, r in v_sub.iterrows()]
w = 0.24
ax2.bar(xr - w, v_sub["VC_PE_Backed_Pct"], width=w, color=NAVY, label="Private VC/PE Backed (%)")
ax2.bar(xr, v_sub["State_Guidance_PreIPO_Pct"], width=w, color=CRIMSON, alpha=0.88, label="PRC State/Guidance Pre-IPO (%)")
ax2.bar(xr + w, v_sub["SOE_Cornerstone_Pct"], width=w, color=FOREST, alpha=0.88, label="SOE IPO Cornerstone (%)")
ax2.set_xticks(xr)
ax2.set_xticklabels(r_names, fontsize=8.3)
ax2.set_ylim(0, 116)
ax2.set_ylabel("Percentage of Issuers (%)")
ax2.set_title("Panel B: Private VC vs. State Guidance & SOE Backing (2025–2026)")
ax2.legend(loc="upper right", fontsize=7.8, frameon=True, facecolor="white")

fig.tight_layout()
save_fig(fig, "fig10_ritter1987_total_direct_costs_and_vc_state")
print("Extension Figures 9 & 10 generated successfully!")
