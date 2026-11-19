#!/usr/bin/env python3
"""
Generate publication-grade vector PDF & 300-DPI PNG figures for the
Comprehensive Research Master Monograph:
  `docs/overview_paper/HK_IPO_Financial_History_Master.md`

Figures produced:
  - master_fig4_1_policy_valve.{png,pdf}
  - master_fig8_2_liquidity_and_ah_wedge.{png,pdf}
  - master_fig9_1_dollar_flow_map.{png,pdf}
  - master_fig9_2_fees_and_hkex_revenue.{png,pdf}
  - master_fig11_1_investor_origin_connect.{png,pdf}
"""

from __future__ import annotations

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, PathPatch
from matplotlib.path import Path as MplPath
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
OV_DIR = REPO_ROOT / "analysis" / "out" / "overview_1994_2026"
EXT_DIR = REPO_ROOT / "analysis" / "out" / "overview_extensions"
FIG_DIR = REPO_ROOT / "docs" / "overview_paper" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Academic typography matching journal_fig1..9
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Palatino", "DejaVu Serif"],
    "font.size": 9.5,
    "axes.titlesize": 10.8,
    "axes.titleweight": "bold",
    "axes.labelsize": 9.5,
    "xtick.labelsize": 8.6,
    "ytick.labelsize": 8.6,
    "legend.fontsize": 8.2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.32,
})

NAVY = "#1B4F8C"
CRIMSON = "#B83B4A"
OCHRE = "#D99B26"
TEAL = "#2A7B6F"
SLATE = "#4A5568"
LIGHT_CORAL = "#E69A9E"
LIGHT_BLUE = "#89AED6"


def save_both(fig: plt.Figure, stem: str) -> None:
    png_p = FIG_DIR / f"{stem}.png"
    pdf_p = FIG_DIR / f"{stem}.pdf"
    fig.savefig(png_p, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(pdf_p, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {stem}.png ({png_p.stat().st_size // 1024} KB) & .pdf")


def build_fig4_1() -> None:
    """Plain-English Policy Valve chart (removes Jordà LP / Newey-West labels)."""
    pol_reg = pd.read_csv(OV_DIR / "table_policy_valve_regimes.csv")
    pol_lp = pd.read_csv(OV_DIR / "table_policy_valve_local_projections.csv")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.3))
    reg_short = [
        "Normal\n1994–2021.06",
        "Onshore A-Share\nIPO Freezes",
        "CAC / HFCAA\n2021.07–23.03",
        "Filing Onset\n2023.04–24.03",
        "Apr 2024\nFive Measures",
    ]
    x_r = np.arange(len(pol_reg))
    h_vals = pd.to_numeric(pol_reg["Mean_HShare_IPOs_pm"], errors="coerce")
    nh_vals = pd.to_numeric(pol_reg["Mean_NonH_IPOs_pm"], errors="coerce")

    ax1.bar(x_r, h_vals, color=CRIMSON, alpha=0.88, width=0.58, label="PRC H-Share IPOs / Month")
    ax1.bar(x_r, nh_vals, bottom=h_vals, color=NAVY, alpha=0.82, width=0.58, label="Offshore Non-H-Share IPOs / Month")
    for xi, tot in zip(x_r, h_vals + nh_vals):
        ax1.text(xi, tot + 0.18, f"{tot:.2f}", ha="center", va="bottom", fontsize=8.2, fontweight="bold", color="#1F2937")
    ax1.set_xticks(x_r)
    ax1.set_xticklabels(reg_short, fontsize=8.1)
    ax1.set_ylim(0, 11.0)
    ax1.set_ylabel("Mean Monthly HKEX Ordinary IPOs")
    ax1.set_title("(a) Monthly Issuance Across Mainland Policy Regimes")
    ax1.legend(loc="upper left", frameon=True, framealpha=0.92)

    horizons = pd.to_numeric(pol_lp["horizon_months"], errors="coerce")
    coefs = pd.to_numeric(pol_lp["beta_hshare_pct"], errors="coerce")
    ses = pd.to_numeric(pol_lp["se_hshare_pct"], errors="coerce")
    ax2.plot(horizons, coefs, color=NAVY, marker="o", linewidth=2.1, label="H-Share Deal Share Shift (pp)")
    ax2.fill_between(horizons, coefs - 1.96 * ses, coefs + 1.96 * ses, color=NAVY, alpha=0.17, label="95% Confidence Interval")
    ax2.axhline(0, color="black", linewidth=0.8)
    y_lo, y_hi = ax2.get_ylim()
    ax2.set_ylim(y_lo - 0.12 * (y_hi - y_lo), y_hi + 0.10 * (y_hi - y_lo))
    ax2.set_xlabel("Months Following Cross-Border Policy Pivot")
    ax2.set_ylabel("Change in HKEX H-Share Deal Share (pp)")
    ax2.set_title("(b) Dynamic Persistence of Southward H-Share Routing")
    ax2.legend(loc="lower right", frameon=True, framealpha=0.92)

    fig.tight_layout()
    save_both(fig, "master_fig4_1_policy_valve")


def build_fig8_2() -> None:
    """Blueprint Fig 8.2: Post-IPO Liquidity Decay & Persistent A-H Valuation Wedge."""
    zom = pd.read_csv(EXT_DIR / "ext_table19a_zombie_ipos_and_amihud_summary.csv")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.8, 4.45))

    # Panel (a): 33-Year Main Board Eras (rows 4..7) + Modern Scale Terciles (rows 8..10)
    mb_rows = zom.iloc[[4, 5, 6, 7]].copy()
    labels_a = ["Era II\n(N=378)", "Era III\n(N=821)", "Era IV\n(N=575)", "Era V\n(N=334)"]
    decay_pct = mb_rows["Zombie_95Pct_Decay_Share_Pct"].to_numpy(dtype=float)
    zero_pct = mb_rows["Any_Zero_Volume_Day_Pct"].to_numpy(dtype=float)
    med_to = mb_rows["Med_6M_Daily_Turnover_HKDm"].to_numpy(dtype=float)

    x = np.arange(len(labels_a))
    w = 0.34
    b1 = ax1.bar(x - w / 2, decay_pct, width=w, color=CRIMSON, alpha=0.88, label="Lost >95% of Day-1 Volume by Month 6 (%)")
    b2 = ax1.bar(x + w / 2, zero_pct, width=w, color=OCHRE, alpha=0.86, label=">=1 Zero-Volume Trading Day in Months 2–6 (%)")
    for rect in b1:
        h = rect.get_height()
        ax1.text(rect.get_x() + rect.get_width() / 2, h + 1.3, f"{h:.1f}%", ha="center", va="bottom", fontsize=7.9, fontweight="bold", color=CRIMSON)
    for rect in b2:
        h = rect.get_height()
        ax1.text(rect.get_x() + rect.get_width() / 2, h + 1.3, f"{h:.1f}%", ha="center", va="bottom", fontsize=7.9, color="#7C5810")

    ax1_r = ax1.twinx()
    ax1_r.spines["top"].set_visible(False)
    ax1_r.grid(False)
    ax1_r.plot(x, med_to, color=NAVY, marker="s", linewidth=2.0, linestyle="--", label="Median Daily Turnover (HK$M, Right)")
    for xi, tv in zip(x, med_to):
        dx = -0.18 if xi == 3 else 0.0
        dy = 1.15
        ax1_r.text(xi + dx, tv + dy, f"HK${tv:.1f}M/d", ha="center", fontsize=7.8, fontweight="bold", color=NAVY,
                   bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.78))
    ax1_r.set_ylim(0, 21.5)
    ax1_r.set_ylabel("Median Month 2–6 Daily Turnover (HK$ Million)", color=NAVY)
    ax1_r.tick_params(axis="y", colors=NAVY)

    ax1.set_xticks(x)
    ax1.set_xticklabels(labels_a)
    ax1.set_ylim(0, 104)
    ax1.set_ylabel("Share of Main Board IPOs (%)")
    ax1.set_title("(a) Post-IPO Liquidity Decay Across Main Board Eras")
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax1_r.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper right", fontsize=7.5, frameon=True, framealpha=0.92)

    # Panel (b): Persistent H-to-A Valuation Discount Across Lifecycle Stages (N = 53/57 A+H IPOs)
    stages = [
        "IPO Offer\nPrice\n(N = 57)",
        "IPO Offer\n(Paired)\n(N = 53)",
        "Day-1\nMarket Close\n(N = 53)",
        "Pre-Connect\nWindow\n(N = 53)",
        "Post-Connect\n[T_stab+1..D60]\n(N = 53)",
    ]
    disc_vals = [-36.40, -35.72, -29.38, -28.20, -26.51]
    bar_cols = [SLATE, SLATE, NAVY, NAVY, TEAL]
    x_b = np.arange(len(stages))
    bars = ax2.bar(x_b, disc_vals, width=0.54, color=bar_cols, alpha=0.88)
    ax2.axhline(0, color="black", linewidth=0.85)
    for xi, v in zip(x_b, disc_vals):
        ax2.text(xi, v - 1.9, f"{v:.2f}%", ha="center", va="top", fontsize=8.2, fontweight="bold", color="#111827")

    # Annotate primary repricing vs post-Connect non-convergence
    ax2.annotate(
        "Day-1 Secondary Repricing:\n+6.34 pp narrowing (p = 0.0001)",
        xy=(2, -29.38),
        xytext=(1.15, -13.5),
        arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.2),
        fontsize=8.0,
        fontweight="bold",
        color=NAVY,
        bbox=dict(boxstyle="round,pad=0.3", fc="#F0F5FA", ec=NAVY, lw=0.8),
    )
    ax2.annotate(
        "Post-Connect (100% Auto-Entry):\nTurnover +32.5 log-pts (25.8% CCASS),\nyet gap moves only +1.69 pp (p = 0.18)\nunder non-fungibility & 20% div. tax",
        xy=(4, -26.51),
        xytext=(2.35, -6.8),
        arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2),
        fontsize=7.7,
        color="#134E4A",
        bbox=dict(boxstyle="round,pad=0.32", fc="#F0FDFA", ec=TEAL, lw=0.8),
    )

    ax2.set_xticks(x_b)
    ax2.set_xticklabels(stages, fontsize=7.9)
    ax2.set_ylim(-43.5, 2.5)
    ax2.set_ylabel("Mean H-Share vs. A-Share Price Discount (%)")
    ax2.set_title("(b) A+H Valuation Wedge Before & After Stock Connect")

    fig.tight_layout()
    save_both(fig, "master_fig8_2_liquidity_and_ah_wedge")


def _draw_ribbon(ax: plt.Axes, x0: float, y0_bot: float, y0_top: float, x1: float, y1_bot: float, y1_top: float, color: str, alpha: float = 0.28) -> None:
    """Draw a smooth cubic Bezier Sankey ribbon between two vertical intervals."""
    xm = 0.5 * (x0 + x1)
    verts = [
        (x0, y0_top),
        (xm, y0_top),
        (xm, y1_top),
        (x1, y1_top),
        (x1, y1_bot),
        (xm, y1_bot),
        (xm, y0_bot),
        (x0, y0_bot),
        (x0, y0_top),
    ]
    codes = [
        MplPath.MOVETO,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.LINETO,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CLOSEPOLY,
    ]
    patch = PathPatch(MplPath(verts, codes), facecolor=color, edgecolor="none", alpha=alpha, zorder=1)
    ax.add_patch(patch)


def _draw_node(ax: plt.Axes, x: float, y: float, w: float, h: float, title: str, body: str, fc: str, ec: str, title_color: str = "white") -> None:
    """Draw a clean two-tone institutional flow box."""
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.008,rounding_size=0.014",
        facecolor="#FFFFFF", edgecolor=ec, linewidth=1.35, zorder=3
    )
    ax.add_patch(box)
    hdr_h = min(0.055, h * 0.34)
    hdr = FancyBboxPatch(
        (x, y + h - hdr_h), w, hdr_h,
        boxstyle="round,pad=0.004,rounding_size=0.010",
        facecolor=fc, edgecolor=ec, linewidth=0.9, zorder=4
    )
    ax.add_patch(hdr)
    ax.text(x + w / 2, y + h - hdr_h / 2, title, ha="center", va="center", fontsize=8.3, fontweight="bold", color=title_color, zorder=5)
    ax.text(x + w / 2, y + (h - hdr_h) / 2, body, ha="center", va="center", fontsize=7.65, color="#1F2937", linespacing=1.28, zorder=5)


def build_fig9_1() -> None:
    """True Flow & Residency Map: 'A Dollar Raised in Hong Kong: Where Does It Go?'"""
    fig, ax = plt.subplots(figsize=(12.6, 5.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Stage headers
    headers = [
        (0.11, "STAGE 1: SUBSCRIPTION INFLOW"),
        (0.37, "STAGE 2: TRANCHE & FEE SPLIT"),
        (0.64, "STAGE 3: CAPITAL DEPLOYMENT"),
        (0.89, "STAGE 4: HOST-CITY VALUE ENGINE"),
    ]
    for xh, lbl in headers:
        ax.text(xh, 0.965, lbl, ha="center", va="center", fontsize=8.4, fontweight="bold", color=NAVY,
                bbox=dict(boxstyle="round,pad=0.25", fc="#EEF2F6", ec="#CBD5E1", lw=0.8))

    # Coordinates for nodes
    # Col 1: Gross IPO Subscriptions
    c1_x, c1_w = 0.015, 0.19
    _draw_node(
        ax, c1_x, 0.24, c1_w, 0.64,
        "Gross IPO Proceeds (100%)",
        "HK$5,659.4B (N = 2,866 IPOs)\n1994–2026Q3 Ordinary Census\n\n"
        "• Global Active & SWFs\n"
        "• Mainland QDII / Cornerstones\n"
        "• HK Institutions & Retail\n"
        "(Settled in Convertible HKD)",
        NAVY, NAVY
    )

    # Col 2: Top = Primary New Shares (94.19%), Mid = Issuance Expenses (~4.03%), Bot = Secondary Vendor (5.81%)
    c2_x, c2_w = 0.27, 0.205
    _draw_node(
        ax, c2_x, 0.56, c2_w, 0.34,
        "Primary Corporate Shares (94.2%)",
        "94.19% of Share-Split Value\n(99.8% in Era V 2023–2026Q3)\n"
        "83.5% of MB Deals Pure Primary\n"
        "Enters Corporate Treasury",
        NAVY, NAVY
    )
    _draw_node(
        ax, c2_x, 0.28, c2_w, 0.23,
        "Direct Listing Costs (4.03% Wtd.)",
        "Median 7.98% | <HK$500M: 18.22%\n"
        "• 50.9% Non-UW Law, Audit, Valuers,\n  Print, Registrar & Regulatory\n"
        "• 49.1% UW Syndicates (HK/PRC/Global)",
        TEAL, TEAL
    )
    _draw_node(
        ax, c2_x, 0.06, c2_w, 0.17,
        "Secondary Vendor Sales (5.8%)",
        "Founders / Pre-IPO PE Exits &\n2001–2017 NSSF 10% State-\nPension Transfers (Global Residency)",
        SLATE, SLATE
    )

    # Col 3: Top = Cross-Border Real Deployment (Non-HK GDP), Bot = Onshore Transaction Value Added (HK GDP)
    c3_x, c3_w = 0.54, 0.205
    _draw_node(
        ax, c3_x, 0.53, c3_w, 0.37,
        "Cross-Border Corporate Assets",
        "Net Proceeds (~90%–96% of Gross)\n"
        "• Mainland Plants, R&D & Bank CAR\n"
        "• Overseas Capex (e.g., CATL Hungary)\n"
        "• Debt Repayment: 1.14% Mean\n"
        "[Balance-Sheet Transfer ≠ HK GDP]",
        CRIMSON, CRIMSON
    )
    _draw_node(
        ax, c3_x, 0.18, c3_w, 0.29,
        "Hong Kong Deal-Time Value Added",
        "Resident HK Professional Output\n"
        "• HK/PRC Legal & Sponsor Teams\n"
        "• Big-4 Reporting Accountants\n"
        "• Surveyors, Registrars & Printers\n"
        "[HK GDP Only If Resident-Produced]",
        TEAL, TEAL
    )

    # Col 4: Durable Multi-Decade Host-City Recurring Engine
    c4_x, c4_w = 0.805, 0.185
    _draw_node(
        ax, c4_x, 0.48, c4_w, 0.42,
        "Recurring Market Ecosystem",
        "Triggered by Listed Equity Stock:\n"
        "• HKEX Trading, Clearing, CCASS\n  & Data: HK$19.95B in FY25\n  (11.2x Listing Fees of HK$1.79B)\n"
        "• Post-IPO Follow-On Equity:\n  >IPO Proceeds in 16 / 24 Years",
        NAVY, NAVY
    )
    _draw_node(
        ax, c4_x, 0.12, c4_w, 0.30,
        "Public Revenue & Capabilities",
        "• HKSAR Stock Stamp Duty:\n  ~HK$44B (H1 FY25/26; Cyclical)\n"
        "• Annual Audits & M&A Advisory\n"
        "• Reusable Talent Inside HK's\n  265,000 Finance Workforce\n  (Sector Context: 26.2% of GDP)",
        OCHRE, "#9A6B12"
    )

    # Draw proportional ribbons connecting columns
    # Col 1 -> Col 2
    _draw_ribbon(ax, c1_x + c1_w, 0.40, 0.86, c2_x, 0.58, 0.88, NAVY, alpha=0.25)      # Primary shares
    _draw_ribbon(ax, c1_x + c1_w, 0.31, 0.40, c2_x, 0.30, 0.49, TEAL, alpha=0.28)      # Direct fees
    _draw_ribbon(ax, c1_x + c1_w, 0.25, 0.31, c2_x, 0.08, 0.21, SLATE, alpha=0.24)     # Secondary vendor

    # Col 2 -> Col 3
    _draw_ribbon(ax, c2_x + c2_w, 0.59, 0.87, c3_x, 0.56, 0.87, CRIMSON, alpha=0.23)   # Net proceeds -> Mainland/Overseas
    _draw_ribbon(ax, c2_x + c2_w, 0.31, 0.48, c3_x, 0.21, 0.44, TEAL, alpha=0.28)      # 50.9% onshore + HK UW share -> HK GDP

    # Col 3 -> Col 4 (Listed stock stays on HKEX -> Recurring engine & Fiscal/Capabilities)
    _draw_ribbon(ax, c3_x + c3_w, 0.62, 0.82, c4_x, 0.54, 0.84, NAVY, alpha=0.22)      # Listed equity -> Recurring HKEX & Follow-on
    _draw_ribbon(ax, c3_x + c3_w, 0.22, 0.42, c4_x, 0.16, 0.39, OCHRE, alpha=0.26)     # Onshore ecosystem -> Fiscal & Talent

    ax.text(
        0.50, 0.012,
        r"Accounting Boundary (C&SD National Accounts): Gross IPO proceeds (HK\$5,659.4B) and investor price appreciation (+HK\$3,705.5B) are balance-sheet/wealth flows, never summed into Hong Kong GDP.",
        ha="center", va="bottom", fontsize=7.8, style="italic", color="#374151"
    )

    fig.tight_layout()
    save_both(fig, "master_fig9_1_dollar_flow_map")


def build_fig9_2() -> None:
    """Two-panel quantitative chart: (a) Direct Fee Retention by Size (N=216) & (b) 20-Year HKEX Recurring vs Listing Revenue."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.8, 4.45))

    # Panel (a): Table P1.2 (N = 216 audited corpus)
    tiers = ["< HK$500M\n(N = 42)", "HK$500M–1B\n(N = 52)", "HK$1B–3B\n(N = 73)", "> HK$3B\n(N = 49)", "All Matched\n(N = 216)"]
    non_uw = np.array([79.3, 67.7, 54.3, 34.7, 50.9])
    base_uw = np.array([18.1, 27.2, 39.1, 49.3, 39.2])
    inc_uw = 100.0 - non_uw - base_uw
    gross_pct = ["18.22%\nof Gross", "10.98%\nof Gross", "6.68%\nof Gross", "2.28%\nof Gross", "4.03% Wtd.\n(HK$24.1B)"]

    x1 = np.arange(len(tiers))
    w1 = 0.54
    ax1.bar(x1, non_uw, width=w1, color=NAVY, label="Non-UW Legal, Big-4 Audit, Valuer & Reg. (50.9%)")
    ax1.bar(x1, base_uw, bottom=non_uw, width=w1, color=CRIMSON, alpha=0.86, label="Base Underwriting Commissions (39.2%)")
    ax1.bar(x1, inc_uw, bottom=non_uw + base_uw, width=w1, color=OCHRE, alpha=0.90, label="Discretionary Incentive Cap (9.9%)")

    for xi, nuw, gp in zip(x1, non_uw, gross_pct):
        ax1.text(xi, nuw / 2, f"{nuw:.1f}%", ha="center", va="center", fontsize=8.3, fontweight="bold", color="white")
        ax1.text(xi, 102.5, gp, ha="center", va="bottom", fontsize=7.8, fontweight="bold", color="#1F2937")

    ax1.set_xticks(x1)
    ax1.set_xticklabels(tiers, fontsize=8.1)
    ax1.set_ylim(0, 136)
    ax1.set_ylabel("Share of Disclosed Listing Expenses (%)")
    ax1.set_title("(a) Non-Underwriting Fee Share by Deal Size (N = 216)")
    ax1.legend(loc="upper right", fontsize=7.6, frameon=True, framealpha=0.94)

    # Panel (b): HKEX 20-Year Revenue Evolution (Table P1.3: FY2005 - FY2025)
    yrs = ["FY2005", "FY2010", "FY2015", "FY2020", "FY2022", "FY2024", "FY2025"]
    listing_fees = np.array([0.443, 0.945, 0.703, 1.899, 1.915, 1.484, 1.789])  # HK$ Billion
    total_rev = np.array([2.694, 7.566, 13.372, 19.190, 18.456, 22.430, 29.161])  # HK$ Billion (HKEX ARs)
    non_listing_rev = total_rev - listing_fees
    list_share = listing_fees / total_rev * 100.0

    x2 = np.arange(len(yrs))
    w2 = 0.54
    ax2.bar(x2, listing_fees, width=w2, color=CRIMSON, label="Stock Exchange Listing Fees (HK$B)")
    ax2.bar(x2, non_listing_rev, bottom=listing_fees, width=w2, color=TEAL, alpha=0.85,
            label="Recurring Trading, Clearing, Custody, Data & Inv. (HK$B)")

    for xi, tot, lf, ls in zip(x2, total_rev, listing_fees, list_share):
        ax2.text(xi, tot + 0.55, f"{tot:.1f}B\n({ls:.1f}% List.)", ha="center", va="bottom", fontsize=7.4, fontweight="bold", color="#1F2937")

    ax2.annotate(
        r"FY2025 Post-Trade & Trading Alone:" + "\n" + r"HK\$19.95B = 11.2x Listing Fees (HK\$1.79B)",
        xy=(6, 20.0),
        xytext=(1.55, 25.4),
        arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.2),
        fontsize=8.0,
        fontweight="bold",
        color=NAVY,
        bbox=dict(boxstyle="round,pad=0.3", fc="#F0F5FA", ec=NAVY, lw=0.8),
    )

    ax2.set_xticks(x2)
    ax2.set_xticklabels(yrs, fontsize=8.2)
    ax2.set_ylim(0, 34.5)
    ax2.set_ylabel("HKEX Group Revenue & Other Income (HK$ Billion)")
    ax2.set_title("(b) Listing Fees vs. Trading, Clearing and Data Income")
    ax2.legend(loc="upper left", fontsize=7.6, frameon=True, framealpha=0.94)

    fig.tight_layout()
    save_both(fig, "master_fig9_2_fees_and_hkex_revenue")


def build_fig11_1() -> None:
    """Fixed Investor Origin Chart: No cross-definition bar splicing + clean label placement."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.9, 4.45))

    # Panel (a): HKEX CMTS Overseas Turnover Breakdown (cleanly separating Mainland/SB Connect from Rest of Asia in 2020)
    periods = ["2000/01", "2009/10", "2016", "2020\n(Final CMTS)"]
    x1 = np.arange(len(periods))
    w = 0.25

    # UK (2000-16) and Europe incl. UK (2020: 24% total Europe; ~14-17% UK + Cont. EU)
    uk_base = np.array([33.0, 29.0, 23.0, 15.5])       # UK component (est. ~15.5% in 2020 based on 2018 17.2% / 27.3% EU ratio)
    cont_eu_2020 = np.array([0.0, 0.0, 0.0, 8.5])      # Continental Europe reported jointly in 2020 = 24.0% Europe total
    us_share = np.array([29.0, 24.0, 20.0, 23.0])
    # Mainland China: 3% (00/01), 11% (09/10), 22% (2016); in 2020 SB Connect alone = 8.6% / 41.2% = 20.9% of overseas!
    mainland_direct = np.array([3.0, 11.0, 22.0, 20.9])
    other_asia_2020 = np.array([0.0, 0.0, 0.0, 27.1])  # Remaining Asia (incl. QFII/offshore Asia & SG/JP) = 48.0% Total Asia

    ax1.bar(x1 - w, uk_base, width=w, color=NAVY, label="United Kingdom (% Overseas)")
    ax1.bar(x1 - w, cont_eu_2020, bottom=uk_base, width=w, color=LIGHT_BLUE, hatch="//", edgecolor=NAVY, linewidth=0.5,
            label="Continental Europe (2020 Total EU: 24%)")
    ax1.bar(x1, us_share, width=w, color=OCHRE, label="United States (% Overseas)")
    ax1.bar(x1 + w, mainland_direct, width=w, color=CRIMSON, label="Mainland China (2020: SB Connect 20.9%)")
    ax1.bar(x1 + w, other_asia_2020, bottom=mainland_direct, width=w, color=LIGHT_CORAL, hatch="..", edgecolor=CRIMSON, linewidth=0.5,
            label="Rest of Asia (2020 Total Asia: 48%)")

    for xi in range(3):
        ax1.text(xi - w, uk_base[xi] + 0.9, f"{uk_base[xi]:.0f}%", ha="center", va="bottom", fontsize=7.9, color=NAVY, fontweight="bold")
        ax1.text(xi, us_share[xi] + 0.9, f"{us_share[xi]:.0f}%", ha="center", va="bottom", fontsize=7.9, color="#8C6210", fontweight="bold")
        ax1.text(xi + w, mainland_direct[xi] + 0.9, f"{mainland_direct[xi]:.0f}%", ha="center", va="bottom", fontsize=7.9, color=CRIMSON, fontweight="bold")

    # Clean 2020 labels
    ax1.text(3 - w, 24.0 + 0.9, "24%\n(EU)", ha="center", va="bottom", fontsize=7.6, color=NAVY, fontweight="bold")
    ax1.text(3, 23.0 + 0.9, "23%", ha="center", va="bottom", fontsize=7.9, color="#8C6210", fontweight="bold")
    ax1.text(3 + w, 10.4, "20.9%\nSB", ha="center", va="center", fontsize=7.2, color="white", fontweight="bold")
    ax1.text(3 + w, 48.0 + 0.9, "48% Asia", ha="center", va="bottom", fontsize=7.8, color=CRIMSON, fontweight="bold")

    ax1.set_xticks(x1)
    ax1.set_xticklabels(periods)
    ax1.set_ylim(0, 62)
    ax1.set_ylabel("Share of Overseas Investor Cash Turnover (%)")
    ax1.set_title("(a) Overseas Cash Turnover by Origin (CMTS, 2000–2020)")
    ax1.legend(loc="upper left", fontsize=7.3, frameon=True, framealpha=0.94)

    # Panel (b): Southbound Connect Scaling vs Primary Syndicate & SFC AWMAS Benchmarks (zero label overlap)
    yrs_b = ["2016", "2018", "2020", "2022", "2024", "2025"]
    x2 = np.arange(len(yrs_b))
    sb_adt = np.array([4.1, 12.7, 24.4, 31.7, 48.2, 121.1])
    sb_mkt_pct = np.array([6.0, 13.0, 16.0, 23.0, 20.9, 23.0])

    ax2.bar(x2 - 0.17, sb_adt, width=0.33, color=NAVY, alpha=0.86, label="Southbound Connect ADT (HK$B, Left)")
    for xi, adt in zip(x2, sb_adt):
        ax2.text(xi - 0.17, adt + 2.5, f"{adt:.1f}B", ha="center", va="bottom", fontsize=7.5, fontweight="bold", color=NAVY)
    ax2.set_ylim(0, 152)
    ax2.set_ylabel("Southbound Average Daily Turnover (HK$ Billion)", color=NAVY)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(yrs_b)

    ax2_r = ax2.twinx()
    ax2_r.spines["top"].set_visible(False)
    ax2_r.grid(False)
    ax2_r.plot(x2 + 0.17, sb_mkt_pct, color=CRIMSON, marker="s", linewidth=2.1, zorder=5, label="Southbound Share of HK Turnover (%, Right)")
    ax2_r.axhline(90.8, color="#4C1D95", linestyle=":", linewidth=1.6, label="Era V Deals With a PRC Sponsor (90.8%, Right)")
    ax2_r.axhline(63.0, color=TEAL, linestyle="--", linewidth=1.6, label="SFC AWMAS Non-HK Investor AUM (63.0%, Right)")

    # Place % callouts cleanly away from the left-shifted ADT bar labels
    pct_dx = [+0.20, +0.20, +0.22, +0.22, +0.17, +0.17]
    pct_dy = [+5.0, +5.2, -5.8, +5.8, -5.8, -5.8]
    for xi, sp, dx, dy in zip(x2, sb_mkt_pct, pct_dx, pct_dy):
        ax2_r.text(
            xi + dx, sp + dy, f"{sp:.1f}%" if sp == 20.9 else f"{sp:.0f}%",
            ha="center", va="center", fontsize=7.6, fontweight="bold", color=CRIMSON,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.88)
        )

    ax2_r.set_ylim(0, 112)
    ax2_r.set_ylabel("Share of Market Turnover / Sponsors / AUM (%)", color="#1F2937")
    ax2.set_title("(b) Southbound Connect vs. Primary & AUM Benchmarks")

    h1, l1 = ax2.get_legend_handles_labels()
    h2, l2 = ax2_r.get_legend_handles_labels()
    ax2.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=7.3, frameon=True, framealpha=0.94)

    fig.tight_layout()
    save_both(fig, "master_fig11_1_investor_origin_connect")


if __name__ == "__main__":
    build_fig4_1()
    build_fig8_2()
    build_fig9_1()
    build_fig9_2()
    build_fig11_1()
