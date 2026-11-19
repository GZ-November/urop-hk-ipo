"""
generate_intermediary_and_ctp_figures.py

Generates Figures 11 & 12 in docs/overview_paper/figures/:
- Fig 11: Geopolitical Power Shift in HK Investment Banking (1994-2026) & Syndicate Bloat
  Panel A: 33-Year Annual Lead Sponsor Market Share Crossover (PRC IB vs Bulge Bracket vs HK/British Legacy)
  Panel B: Syndicate Size Expansion (Mean Sponsors & Bookrunners) and Fintech Broker Penetration
- Fig 12: Calendar-Time Portfolio (CTP) Performance & Long-Run Wealth Relatives
  Panel A: Cumulative Calendar-Time Wealth of HK IPO Portfolios (MB 12M VW, MB 12M EW, GEM 12M EW vs HSI, 1994-2026)
  Panel B: 2-Factor Monthly Excess Alphas (Net of Official HKMA 1M HIBOR): Equal-Month OLS vs. Deal-Count WLS

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

PANEL_CSV = EXT_DIR / "clean_33y_intermediaries_greenshoe.csv"
CTP_CSV = EXT_DIR / "clean_monthly_ctp_with_hibor_rf_1994_2026.csv"
TABLE10_CSV = EXT_DIR / "ext_table10_calendar_time_portfolio_alphas.csv"


def plot_fig11(panel_df: pd.DataFrame):
    print("Generating Figure 11: Geopolitical Power Shift & Syndicate Bloat...")
    mb = panel_df[panel_df["board"] == "Main Board"].copy()

    annual = []
    for yr, sub in mb.groupby("cohort_year"):
        n = len(sub)
        prc = (sub["lead_sponsor_group"] == "PRC_Mainland_IB").mean() * 100
        bb = (sub["lead_sponsor_group"] == "US_EU_Bulge_Bracket").mean() * 100
        hk = (sub["lead_sponsor_group"] == "HK_British_Legacy_and_Asia").mean() * 100

        n_sp = sub["n_sponsors"].mean()
        n_br = sub["n_bookrunners"].mean()
        fintech = sub["has_fintech_retail_broker"].mean() * 100

        annual.append({
            "year": yr,
            "n": n,
            "prc_share": prc,
            "bb_share": bb,
            "hk_share": hk,
            "mean_sponsors": n_sp,
            "mean_bookrunners": n_br,
            "fintech_share": fintech,
        })
    df_yr = pd.DataFrame(annual).sort_values("year")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 5.8), dpi=300)

    # Panel A: 33-Year Sponsor Crossover (clean top headroom for legend & non-overlapping annotations)
    years = df_yr["year"].values
    ax1.plot(years, df_yr["hk_share"], label="HK / British Legacy & Asia", color="#3A6EA5", lw=2.1, ls="--", marker="o", ms=3.8)
    ax1.plot(years, df_yr["bb_share"], label="US / EU Bulge Bracket", color="#2E8B57", lw=2.1, ls="-.", marker="s", ms=3.8)
    ax1.plot(years, df_yr["prc_share"], label="PRC Mainland Investment Banks", color="#B22222", lw=2.5, marker="^", ms=4.5)

    ax1.axvline(2013, color="#555555", lw=1.0, ls=":", alpha=0.85)
    ax1.annotate(
        "2013: CITIC acquires CLSA\n& Sponsor Code Reform",
        xy=(2013, 62),
        xytext=(2004.2, 82),
        fontsize=8.2,
        color="#222222",
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#CCCCCC", alpha=0.92),
        arrowprops=dict(arrowstyle="->", color="#666666", lw=0.8),
    )

    ax1.axvline(2023, color="#555555", lw=1.0, ls=":", alpha=0.85)
    ax1.annotate(
        "2023: CSRC Filing\n& FINI T+2",
        xy=(2023, 68),
        xytext=(2015.2, 89),
        fontsize=8.2,
        color="#222222",
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#CCCCCC", alpha=0.92),
        arrowprops=dict(arrowstyle="->", color="#666666", lw=0.8),
    )

    ax1.set_title("Panel A: 33-Year Lead Sponsor Market Share Crossover (1994–2026)", fontsize=11, fontweight="bold", pad=10)
    ax1.set_xlabel("Listing Cohort Year", fontsize=10)
    ax1.set_ylabel("Share of Main Board Offerings (%)", fontsize=10)
    ax1.set_xlim(1993, 2027)
    ax1.set_ylim(-3, 118)
    ax1.set_yticks([0, 20, 40, 60, 80, 100])
    ax1.grid(True, ls=":", alpha=0.5)
    ax1.legend(
        frameon=True,
        facecolor="white",
        edgecolor="#DDDDDD",
        fontsize=8.3,
        loc="upper center",
        ncol=2,
    )

    # Panel B: Syndicate Bloat & Fintech Brokers
    ax2_twin = ax2.twinx()

    p1 = ax2.plot(years, df_yr["mean_bookrunners"], label="Mean Bookrunners per Deal (Left)", color="#1F77B4", lw=2.3, marker="o", ms=3.8)
    p2 = ax2.plot(years, df_yr["mean_sponsors"], label="Mean Sponsors per Deal (Left)", color="#FF7F0E", lw=2.0, ls="--", marker="d", ms=3.8)
    p3 = ax2_twin.plot(years, df_yr["fintech_share"], label="Fintech Broker Syndicate % (Right)", color="#7B3294", lw=2.2, ls="-.", marker="x", ms=4.8)

    ax2.set_title("Panel B: Syndicate Bloat and Fintech Broker Penetration", fontsize=11, fontweight="bold", pad=10)
    ax2.set_xlabel("Listing Cohort Year", fontsize=10)
    ax2.set_ylabel("Average Syndicate Member Count", fontsize=10)
    ax2_twin.set_ylabel("Deals with Fintech Broker (%)", fontsize=10, color="#7B3294")
    ax2_twin.tick_params(axis="y", labelcolor="#7B3294")
    ax2.set_xlim(1993, 2027)
    ax2.set_ylim(0, 11.8)
    ax2_twin.set_ylim(-2, 88)
    ax2.grid(True, ls=":", alpha=0.5)

    plots = p1 + p2 + p3
    labs = [l.get_label() for l in plots]
    ax2.legend(plots, labs, frameon=True, facecolor="white", edgecolor="#DDDDDD", fontsize=8.5, loc="upper left")

    plt.tight_layout()
    pdf_path = FIG_DIR / "fig11_geopolitical_ib_crossover_and_syndicate_bloat.pdf"
    png_path = FIG_DIR / "fig11_geopolitical_ib_crossover_and_syndicate_bloat.png"
    plt.savefig(pdf_path, bbox_inches="tight")
    plt.savefig(png_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved {pdf_path} and {png_path}")


def plot_fig12(ctp_df: pd.DataFrame, tab10: pd.DataFrame):
    print("Generating Figure 12: Calendar-Time Portfolio Returns & Alphas (HKMA HIBOR Rf, OLS vs WLS)...")

    ctp = ctp_df.copy().sort_values("year_month").reset_index(drop=True)

    mb_vw_ret = ctp["ctp_12m_mb_vw_ret"].fillna(0) / 100.0
    mb_ew_ret = ctp["ctp_12m_mb_ew_ret"].fillna(0) / 100.0
    hsi_ret = ctp["hsi_monthly_return_pct"].fillna(0) / 100.0

    cum_mb_vw = (1.0 + mb_vw_ret).cumprod()
    cum_mb_ew = (1.0 + mb_ew_ret).cumprod()
    cum_hsi = (1.0 + hsi_ret).cumprod()

    gem_start_idx = ctp["ctp_12m_gem_ew_ret"].first_valid_index()
    cum_gem_ew = pd.Series(index=ctp.index, dtype=float)
    if gem_start_idx is not None:
        cum_gem_ew.loc[gem_start_idx:] = (1.0 + ctp.loc[gem_start_idx:, "ctp_12m_gem_ew_ret"].fillna(0) / 100.0).cumprod()
        base_hsi = cum_hsi.loc[gem_start_idx]
        cum_gem_ew = cum_gem_ew * base_hsi

    dates = pd.to_datetime(ctp["year_month"])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.8, 5.9), dpi=300)

    # Panel A: Cumulative Wealth
    ax1.plot(dates, cum_mb_vw, label="MB 12M Value-Weighted IPO Portfolio", color="#1F77B4", lw=2.2)
    ax1.plot(dates, cum_mb_ew, label="MB 12M Equal-Weighted IPO Portfolio", color="#2CA02C", lw=1.9, ls="--")
    ax1.plot(dates, cum_hsi, label="Hang Seng Index (^HSI Benchmark)", color="#111111", lw=1.9, ls=":")
    if gem_start_idx is not None:
        ax1.plot(dates, cum_gem_ew, label="GEM 12M Equal-Weighted (Scaled to HSI at 1999.12)", color="#C0392B", lw=1.7, ls="-.")

    ax1.set_yscale("log")
    ax1.set_ylim(0.08, 28)
    ax1.set_title("Panel A: Cumulative Calendar-Time Wealth (Log Scale, 1994–2026)", fontsize=10.8, fontweight="bold", pad=10)
    ax1.set_xlabel("Calendar Time", fontsize=10)
    ax1.set_ylabel("Wealth Index (HK$1.00 Invested in 1994.01)", fontsize=10)
    ax1.grid(True, ls=":", alpha=0.5)
    ax1.legend(frameon=True, facecolor="white", edgecolor="#DDDDDD", fontsize=8.2, loc="upper left")

    # Panel B: Paired Horizontal Bars — Equal-Month OLS (NW HAC) vs. Deal-Count WLS (Mitchell & Stafford 2000)
    short_labels = {
        "MB 12M Equal-Weighted": "MB 12M EW",
        "MB 12M Value-Weighted": "MB 12M VW",
        "MB 36M Equal-Weighted": "MB 36M EW",
        "MB 36M Value-Weighted": "MB 36M VW",
        "GEM 12M Equal-Weighted": "GEM 12M EW",
        "GEM 12M Value-Weighted": "GEM 12M VW",
        "GEM 36M Equal-Weighted": "GEM 36M EW",
        "GEM 36M Value-Weighted": "GEM 36M VW",
    }
    t10 = tab10.copy()
    t10["short"] = t10["Portfolio"].map(short_labels)

    y_pos = np.arange(len(t10))
    bar_h = 0.36

    b_ols = ax2.barh(
        y_pos - bar_h / 2,
        t10["TwoFactor_OLS_Alpha_Pct"],
        height=bar_h,
        color="#4C78A8",
        alpha=0.90,
        edgecolor="#222222",
        lw=0.6,
        label="Equal-Month OLS (Newey–West 6-Lag HAC)",
    )
    b_wls = ax2.barh(
        y_pos + bar_h / 2,
        t10["TwoFactor_WLS_Alpha_Pct"],
        height=bar_h,
        color="#E45756",
        alpha=0.90,
        edgecolor="#222222",
        lw=0.6,
        label="Deal-Count WLS (Active IPO Weight N_t)",
    )

    ax2.axvline(0, color="#111111", lw=1.0)
    ax2.axhline(3.5, color="#888888", lw=0.9, ls="--", alpha=0.7)

    for idx, row in t10.iterrows():
        for val, tval, y_off in [
            (row["TwoFactor_OLS_Alpha_Pct"], row["TwoFactor_OLS_t_NW"], -bar_h / 2),
            (row["TwoFactor_WLS_Alpha_Pct"], row["TwoFactor_WLS_t_HC3"], +bar_h / 2),
        ]:
            stars = "**" if abs(tval) >= 2.58 else ("*" if abs(tval) >= 1.96 else "")
            pad = 0.04 if val >= 0 else -0.04
            ha = "left" if val >= 0 else "right"
            ax2.text(
                val + pad,
                idx + y_off,
                f"{val:+.2f}% (t={tval:+.2f}){stars}",
                va="center",
                ha=ha,
                fontsize=7.6,
                color="#111111",
            )

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(t10["short"], fontsize=9.2, fontweight="bold")
    ax2.set_ylim(-0.65, len(t10) + 0.55)
    ax2.invert_yaxis()
    ax2.set_xlim(-2.45, 1.18)
    ax2.set_title("Panel B: 2-Factor Excess Alphas Net of HKMA 1M HIBOR (OLS vs. WLS)", fontsize=10.8, fontweight="bold", pad=10)
    ax2.set_xlabel("Monthly Abnormal Alpha (% per month; * p<0.05, ** p<0.01)", fontsize=9.8)
    ax2.grid(True, ls=":", alpha=0.5, axis="x")
    ax2.legend(frameon=True, facecolor="white", edgecolor="#DDDDDD", fontsize=8.1, loc="lower left")

    plt.tight_layout()
    pdf_path = FIG_DIR / "fig12_calendar_time_portfolio_alphas_and_auditor.pdf"
    png_path = FIG_DIR / "fig12_calendar_time_portfolio_alphas_and_auditor.png"
    plt.savefig(pdf_path, bbox_inches="tight")
    plt.savefig(png_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved {pdf_path} and {png_path}")


def main():
    panel_df = pd.read_csv(PANEL_CSV, low_memory=False)
    ctp_df = pd.read_csv(CTP_CSV, low_memory=False)
    tab10 = pd.read_csv(TABLE10_CSV)
    plot_fig11(panel_df)
    plot_fig12(ctp_df, tab10)
    print("Figures 11 and 12 successfully updated!")


if __name__ == "__main__":
    main()
