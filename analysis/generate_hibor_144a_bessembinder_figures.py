"""
generate_hibor_144a_bessembinder_figures.py

Generates publication-grade Figures 13 & 14 in docs/overview_paper/figures/:
- Fig 13: Monetary Transmission, FINI Settlement Reform & Downside Offer-Price Stickiness
  Panel A: Short-End Interbank Yield-Curve Squeeze (Peak 1W - 3M HIBOR Spread) Across
           Retail Subscription Capital Tiers: Pre-FINI Escrow Lockup vs. Post-FINI T+2
  Panel B: Asymmetric Public-Information Pass-Through During Hong Kong's Concurrent
           Retail Subscription Window (Post-Prospectus HSI Return vs. Day-1 Return & Break Rate)
- Fig 14: Global Capital Market Decoupling (Rule 144A) & Bessembinder Lifetime Wealth Skewness
  Panel A: Global Distribution Decoupling on HK$1B+ Main Board IPOs (Rule 144A Share &
           Wall Street Bulge-Bracket Bookrunners) and Vanishing Secondary Share Sales (2000-2026)
  Panel B: Bessembinder (2018) Cumulative Gross Wealth Concentration & Return Distribution
           Across N = 2,117 Split-Verified HKEX IPOs (1994-2026)

Vector PDF + 300 DPI PNG outputs.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Helvetica", "Arial"]
plt.rcParams["axes.unicode_minus"] = False

BASE_DIR = Path(__file__).resolve().parent.parent
EXT_DIR = BASE_DIR / "analysis" / "out" / "overview_extensions"
FIG_DIR = BASE_DIR / "docs" / "overview_paper" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

PANEL_CSV = EXT_DIR / "clean_33y_macro_144a_hibor_panel.csv"
TAB11_CSV = EXT_DIR / "ext_table11_hibor_liquidity_freeze_fini.csv"
TAB13_CSV = EXT_DIR / "ext_table13_rule144a_decoupling_and_secondary.csv"


def plot_fig13(df: pd.DataFrame, tab11: pd.DataFrame) -> None:
    print("Generating Figure 13: FINI Interbank Squeeze Elimination & Downside Price Stickiness...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.8, 5.8), dpi=300)

    # ------------------------------------------------------------------
    # Panel A: Pre-FINI vs. Post-FINI Peak (1W - 3M HIBOR) Spread (bps)
    # ------------------------------------------------------------------
    tiers = [
        "Cold/Mod (< HK$10B Subscribed)",
        "Warm (HK$10B - HK$100B)",
        "Hot Mega-Freeze (>= HK$100B)",
    ]
    tier_short = [
        "Cold / Mod.\n(< HK$10B)",
        "Warm\n(HK$10B–100B)",
        "Hot Mega-Freeze\n(>= HK$100B)",
    ]

    pre = tab11[tab11["Settlement_Regime"].str.startswith("Pre-FINI")].set_index("Subscription_Capital_Tier").loc[tiers]
    post = tab11[tab11["Settlement_Regime"].str.startswith("Post-FINI")].set_index("Subscription_Capital_Tier").loc[tiers]

    x = np.arange(len(tiers))
    w = 0.34

    n_pre_fini = int(pre["N_Deals"].sum())
    n_post_fini = int(post["N_Deals"].sum())

    b1 = ax1.bar(
        x - w / 2,
        pre["Mean_1W_Minus_3M_Spread_bps"],
        width=w,
        color="#B22222",
        alpha=0.88,
        edgecolor="#222222",
        lw=0.7,
        label=f"Pre-FINI Escrow Lockup (1999–2023.11, N={n_pre_fini:,})",
    )
    b2 = ax1.bar(
        x + w / 2,
        post["Mean_1W_Minus_3M_Spread_bps"],
        width=w,
        color="#1F77B4",
        alpha=0.88,
        edgecolor="#222222",
        lw=0.7,
        label=f"Post-FINI Credit Cap T+2 (2023.11–2026, N={n_post_fini:,})",
    )

    ax1.axhline(0, color="#111111", lw=1.0, ls="--")

    for bars, sub_df in [(b1, pre), (b2, post)]:
        for bar, (_, r) in zip(bars, sub_df.iterrows()):
            val = bar.get_height()
            y_txt = val + 1.1 if val >= 0 else val - 2.3
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                y_txt,
                f"{val:+.1f} bps\n(n={int(r['N_Deals'])})",
                ha="center",
                va="bottom" if val >= 0 else "top",
                fontsize=7.9,
                fontweight="bold",
                color="#111111",
            )

    ax1.annotate(
        "Continuous OLS Slope on log(1 + Locked HK$B):\n"
        "• Pre-FINI: +4.14 bps (t = +5.45, p < 0.0001)\n"
        "• Interaction × Post-FINI: −4.81 bps (t = −2.52)\n"
        "• Post-FINI Net Slope: −0.67 bps (flat)",
        xy=(2 - w / 2, 6.0),
        xytext=(0.62, 13.5),
        fontsize=8.0,
        color="#222222",
        bbox=dict(boxstyle="round,pad=0.35", fc="#FFFDF7", ec="#CCCCCC", alpha=0.95),
        arrowprops=dict(arrowstyle="->", color="#B22222", lw=0.9),
    )

    ax1.set_xticks(x)
    ax1.set_xticklabels(tier_short, fontsize=9.3, fontweight="bold")
    ax1.set_ylim(-29.5, 29.5)
    ax1.set_ylabel("Peak Freeze Window (1W − 3M HIBOR) Spread (bps)", fontsize=9.8)
    ax1.set_title("Panel A: FINI Eliminated IPO-Induced Interbank Yield-Curve Squeezes", fontsize=10.8, fontweight="bold", pad=10)
    ax1.grid(True, ls=":", alpha=0.5, axis="y")
    ax1.legend(frameon=True, facecolor="white", edgecolor="#DDDDDD", fontsize=8.0, loc="upper left")

    # ------------------------------------------------------------------
    # Panel B: Downside Offer-Price Stickiness During Subscription Freeze
    # ------------------------------------------------------------------
    clean = df[
        (df["board"] == "Main Board")
        & (df["flag_recycled_or_transferred_ticker"] == 0)
        & (df["flag_reverse_split_distortion"] == 0)
        & (df["has_exact_prospectus_date"] == True)
    ].copy()
    clean["ir_wins"] = pd.to_numeric(clean["ir_close_pct"], errors="coerce").clip(lower=-90, upper=300)
    clean = clean.dropna(subset=["ir_wins", "hsi_ret_sub_window_pct"]).copy()
    clean["day1_break_pct"] = (clean["ir_wins"] < 0).astype(float) * 100.0

    # Bin post-prospectus HSI returns into 8 quantile-balanced / interpretable buckets
    bins = [-40, -6.0, -3.5, -1.5, 0.0, 1.5, 3.5, 6.0, 40]
    clean["hsi_bin"] = pd.cut(clean["hsi_ret_sub_window_pct"], bins=bins)
    grp = clean.groupby("hsi_bin", observed=False).agg(
        x_mean=("hsi_ret_sub_window_pct", "mean"),
        ir_mean=("ir_wins", "mean"),
        ir_se=("ir_wins", lambda s: s.std(ddof=1) / np.sqrt(len(s))),
        brk_mean=("day1_break_pct", "mean"),
        n=("ir_wins", "count"),
    ).dropna()

    ax2_twin = ax2.twinx()

    # Plot binned mean IR with +/- 1 SE error bars
    eb = ax2.errorbar(
        grp["x_mean"],
        grp["ir_mean"],
        yerr=grp["ir_se"],
        fmt="o",
        color="#1F77B4",
        ecolor="#6BAED6",
        elinewidth=1.4,
        capsize=3.5,
        ms=6.2,
        label="Binned Mean Day-1 Return ± 1 SE (Left)",
        zorder=4,
    )

    # Overlay piecewise fitted spline anchored at x = 0 mean intercept
    y0 = float(clean.loc[clean["hsi_ret_sub_window_pct"].abs() <= 1.0, "ir_wins"].mean())
    x_neg = np.linspace(-9.0, 0.0, 50)
    x_pos = np.linspace(0.0, 9.0, 50)
    l_neg = ax2.plot(x_neg, y0 + 1.4917 * x_neg, color="#B22222", lw=2.5, label="Downside Stickiness Slope: +1.49 (t = +3.73)")
    l_pos = ax2.plot(x_pos, y0 - 0.0794 * x_pos, color="#2E8B57", lw=2.5, ls="--", label="Upside Hard-Cap Slope: −0.08 (t = −0.21)")

    l_brk = ax2_twin.plot(
        grp["x_mean"],
        grp["brk_mean"],
        color="#7B3294",
        lw=2.0,
        ls="-.",
        marker="s",
        ms=4.8,
        label="Day-1 Break Rate IR < 0% (Right)",
    )

    ax2.axvline(0, color="#444444", lw=1.0, ls=":")
    ax2.axhline(0, color="#888888", lw=0.8, ls=":")

    ax2.annotate(
        f"Wald Asymmetry Test:\np = 0.0150 (N = {len(clean):,})\n34.5% Fixed-Price + Rule 11.13\nOpt-Out Deter Downward Revision",
        xy=(-5.5, y0 + 1.4917 * (-5.5)),
        xytext=(-9.2, 23.5),
        fontsize=7.9,
        color="#222222",
        bbox=dict(boxstyle="round,pad=0.3", fc="#FFFDF7", ec="#CCCCCC", alpha=0.94),
        arrowprops=dict(arrowstyle="->", color="#B22222", lw=0.85),
    )

    ax2.set_xlim(-9.8, 9.8)
    ax2.set_ylim(-6, 33)
    ax2_twin.set_ylim(10, 68)
    ax2.set_xlabel("Post-Prospectus Subscription-Window HSI Return (%)", fontsize=9.8)
    ax2.set_ylabel("Mean Day-1 Initial Return (%)", fontsize=9.8, color="#1F77B4")
    ax2_twin.set_ylabel("Day-1 Break Rate (% Closing Below Offer)", fontsize=9.8, color="#7B3294")
    ax2_twin.tick_params(axis="y", labelcolor="#7B3294")
    ax2.set_title("Panel B: Asymmetric Public-Info Pass-Through (Downside Price Stickiness)", fontsize=10.8, fontweight="bold", pad=10)
    ax2.grid(True, ls=":", alpha=0.5)

    handles = [eb, l_neg[0], l_pos[0], l_brk[0]]
    labels = [h.get_label() for h in handles]
    ax2.legend(handles, labels, frameon=True, facecolor="white", edgecolor="#DDDDDD", fontsize=7.9, loc="lower left")

    plt.tight_layout()
    pdf_path = FIG_DIR / "fig13_hibor_liquidity_freeze_and_hardcap_asymmetry.pdf"
    png_path = FIG_DIR / "fig13_hibor_liquidity_freeze_and_hardcap_asymmetry.png"
    plt.savefig(pdf_path, bbox_inches="tight")
    plt.savefig(png_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved {pdf_path} and {png_path}")


def plot_fig14(df: pd.DataFrame, tab13: pd.DataFrame) -> None:
    print("Generating Figure 14: Global Rule 144A Decoupling & Bessembinder Lifetime Wealth...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.8, 5.8), dpi=300)

    # ------------------------------------------------------------------
    # Panel A: Post-2000 Global Rule 144A Rise & 2023-26 Retreat + Vanishing Secondary Sales
    # ------------------------------------------------------------------
    t13 = tab13.iloc[1:].copy().reset_index(drop=True)  # 2000-2026Q3 windows (post electronic prospectus era)
    win_labels = [
        "2000–07\n(WTO / SOE)",
        "2008–17\n(Global Peak)",
        "2018–20\n(Ch.18A/19C)",
        "2021–22\n(Tech Peak)",
        "2023–26Q3\n(Decoupling)",
    ]
    x = np.arange(len(t13))

    ax1.plot(
        x,
        t13["Rule_144A_Over_HKD1Bn_Pct"],
        color="#B22222",
        lw=2.6,
        marker="o",
        ms=6.5,
        label="U.S. Rule 144A Tranche on HK$1B+ IPOs (%)",
    )
    ax1.plot(
        x,
        t13["Bulge_Bracket_Bookrunner_Pct"],
        color="#2E8B57",
        lw=2.2,
        ls="--",
        marker="s",
        ms=5.5,
        label="U.S. / EU Bulge-Bracket Bookrunner Share (%)",
    )
    ax1.bar(
        x,
        t13["Secondary_Sale_Share_Pct"],
        width=0.42,
        color="#4C78A8",
        alpha=0.35,
        edgecolor="#2B5B84",
        lw=0.8,
        label="IPOs with Secondary Share Sales (Sale Shares %)",
    )

    for xi, r144, sec in zip(x, t13["Rule_144A_Over_HKD1Bn_Pct"], t13["Secondary_Sale_Share_Pct"]):
        if xi == 1:
            ax1.text(xi + 0.14, r144 - 3.6, f"{r144:.1f}%", ha="left", va="top", fontsize=8.3, fontweight="bold", color="#B22222")
        elif xi == 4:
            ax1.text(xi + 0.06, r144 - 4.8, f"{r144:.1f}%", ha="center", va="top", fontsize=8.3, fontweight="bold", color="#B22222")
        else:
            ax1.text(xi, r144 + 2.6, f"{r144:.1f}%", ha="center", va="bottom", fontsize=8.3, fontweight="bold", color="#B22222")
        ax1.text(xi, sec + 1.2, f"{sec:.1f}%", ha="center", va="bottom", fontsize=7.8, color="#1F4E78")

    ax1.annotate(
        "−24.5 pp Rule 144A Retreat\n(Mediated by Wall St. BB Exodus:\nBB β = +57.1 pp, t = +15.66)",
        xy=(3.96, 42.0),
        xytext=(2.32, 74.5),
        fontsize=8.0,
        color="#222222",
        bbox=dict(boxstyle="round,pad=0.3", fc="#FFFDF7", ec="#CCCCCC", alpha=0.95),
        arrowprops=dict(arrowstyle="->", color="#B22222", lw=0.9),
    )

    ax1.set_xticks(x)
    ax1.set_xticklabels(win_labels, fontsize=8.9, fontweight="bold")
    ax1.set_ylim(0, 92)
    ax1.set_ylabel("Share of Main Board Offerings (%)", fontsize=9.8)
    ax1.set_title("Panel A: U.S. Rule 144A Decoupling & Vanishing Secondary Sales", fontsize=10.8, fontweight="bold", pad=10)
    ax1.grid(True, ls=":", alpha=0.5, axis="y")
    ax1.legend(frameon=True, facecolor="white", edgecolor="#DDDDDD", fontsize=8.2, loc="upper left")

    # ------------------------------------------------------------------
    # Panel B: Bessembinder (2018) Cumulative Net Wealth Curve (N = 2,117)
    # ------------------------------------------------------------------
    bess = df[
        df["lifetime_offer_to_date_pct"].notna()
        & (~df["flag_lifetime_split_unverified"].astype(bool))
        & (df["flag_recycled_or_transferred_ticker"] == 0)
        & (df["flag_reverse_split_distortion"] == 0)
    ].copy()
    bess["proceeds_hkd_bn"] = pd.to_numeric(bess["funds_raised_total_hkd"], errors="coerce") / 1e9
    bess["wealth_bn"] = bess["proceeds_hkd_bn"] * (bess["lifetime_offer_to_date_pct"] / 100.0)
    bess = bess.dropna(subset=["wealth_bn"]).sort_values("wealth_bn", ascending=False).reset_index(drop=True)

    n_tot = len(bess)
    pct_firms = np.arange(1, n_tot + 1) / n_tot * 100.0
    cum_net_wealth = bess["wealth_bn"].cumsum()
    total_net = float(cum_net_wealth.iloc[-1])
    peak_gross = float(cum_net_wealth.max())
    pos_cutoff_pct = float((bess["wealth_bn"] > 0).mean() * 100.0)

    ax2.plot(pct_firms, cum_net_wealth, color="#1F77B4", lw=2.6, label="Cumulative Offered-Tranche Net Wealth (HK$ Bn)")
    ax2.fill_between(pct_firms, 0, cum_net_wealth, color="#1F77B4", alpha=0.12)
    ax2.axhline(total_net, color="#2E8B57", lw=1.2, ls="--", label=f"Final Net Wealth Creation: +HK${total_net:,.0f}B")
    ax2.axvline(pos_cutoff_pct, color="#B22222", lw=1.1, ls=":", label=f"Zero-Return Threshold ({pos_cutoff_pct:.1f}% Positive; {100.0 - pos_cutoff_pct:.1f}% Lose)")

    # Highlight Top 1% and Peak Gross Creation
    idx_1pct = max(0, int(round(0.01 * n_tot)) - 1)
    w_1pct = float(cum_net_wealth.iloc[idx_1pct])
    share_1pct = (w_1pct / peak_gross) * 100.0
    med_all_lt = float(bess["lifetime_offer_to_date_pct"].median())
    med_gem_lt = float(bess.loc[bess["board"] == "GEM", "lifetime_offer_to_date_pct"].median())
    ax2.scatter([1.0, pos_cutoff_pct], [w_1pct, peak_gross], color="#B22222", s=42, zorder=5)

    ax2.annotate(
        f"Top 1% ({idx_1pct + 1} IPOs: Tencent, Zijin, BYD...)\nGenerate +HK${w_1pct:,.0f}B\n({share_1pct:.1f}% of Gross Wealth Creation)",
        xy=(1.0, w_1pct),
        xytext=(11.5, 2250),
        fontsize=8.0,
        color="#222222",
        bbox=dict(boxstyle="round,pad=0.3", fc="#FFFDF7", ec="#CCCCCC", alpha=0.95),
        arrowprops=dict(arrowstyle="->", color="#B22222", lw=0.9),
    )

    ax2.annotate(
        f"Peak Gross Gain: +HK${peak_gross:,.0f}B at Top {pos_cutoff_pct:.1f}%;\nBottom {100.0 - pos_cutoff_pct:.1f}% Destroy −HK${peak_gross - total_net:,.0f}B\n(Median IPO = {med_all_lt:+.1f}%; GEM = {med_gem_lt:+.1f}%)",
        xy=(pos_cutoff_pct, peak_gross),
        xytext=(34.0, 4250),
        fontsize=7.9,
        color="#222222",
        bbox=dict(boxstyle="round,pad=0.3", fc="#FFFDF7", ec="#CCCCCC", alpha=0.95),
        arrowprops=dict(arrowstyle="->", color="#444444", lw=0.85),
    )

    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, peak_gross * 1.16)
    ax2.set_xlabel(f"Cumulative Percentage of Split-Verified HKEX IPOs Ranked by Wealth Gain (N = {n_tot:,})", fontsize=9.5)
    ax2.set_ylabel("Cumulative Offered-Tranche Wealth Gain (HK$ Billion)", fontsize=9.8)
    ax2.set_title("Panel B: Bessembinder (2018) Lifetime Wealth Concentration (1994–2026)", fontsize=10.8, fontweight="bold", pad=10)
    ax2.grid(True, ls=":", alpha=0.5)
    ax2.legend(frameon=True, facecolor="white", edgecolor="#DDDDDD", fontsize=8.0, loc="lower right")

    plt.tight_layout()
    pdf_path = FIG_DIR / "fig14_rule144a_decoupling_and_bessembinder_wealth.pdf"
    png_path = FIG_DIR / "fig14_rule144a_decoupling_and_bessembinder_wealth.png"
    plt.savefig(pdf_path, bbox_inches="tight")
    plt.savefig(png_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved {pdf_path} and {png_path}")


def main() -> None:
    df = pd.read_csv(PANEL_CSV, low_memory=False)
    tab11 = pd.read_csv(TAB11_CSV)
    tab13 = pd.read_csv(TAB13_CSV)
    plot_fig13(df, tab11)
    plot_fig14(df, tab13)
    print("Figures 13 and 14 successfully generated!")


if __name__ == "__main__":
    main()
