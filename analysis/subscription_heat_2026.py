"""Main Line A: Subscription Demand vs First-Day Performance and Break Rate in 2026 Hong Kong IPOs.

Investigates:
  1. The empirical relationship between retail subscription demand (subscription multiple and applicant count)
     and first-day returns and offer break rates.
  2. Subgroup stability across calendar quarters (Q1, Q2, Q3), listing routes (A+H vs Non-A+H), and deal size terciles.
  3. Econometric regressions of log(1 + IR) on subscription demand with stepwise controls for deal size,
     A+H anchor, firm age, cornerstone allocation, and listing window sentiment.
  4. Post-listing performance: Day-5 and Day-20 buy-and-hold returns from Day-1 close across demand terciles on
     a balanced observation window.

All 113 Main Board ordinary IPOs listed between 2026-01-02 and 2026-09-30.
Outputs: analysis/out/subscription_heat/
"""
from __future__ import annotations


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

from research_inputs import C, ROOT, load_panel, prepare_regression, select_2026
from shared.estimation import bh_family, stars
from shared.inference import wild_cluster_p
from shared.reporting import to_markdown
from shared.reporting import (
    AXIS, BLUE, INK, INK2, ORANGE, new_fig, pct_axis, style_axes,
)

OUT = ROOT / "analysis" / "out" / "subscription_heat"
SEED = 20260930


def load_data() -> pd.DataFrame:
    """Load the 2026 sample and construct demand, size, and performance variables."""
    panel = select_2026(load_panel())
    df = panel.copy()
    df["base_proceeds_hkd_mn"] = df["base_proceeds"] / 1e6
    df["sub_x"] = df[C["sub"]]
    df["log_sub"] = np.log(df["sub_x"].where(df["sub_x"] > 0))
    df["applicants"] = df["Public applicants"]
    df["log_app"] = np.log(df["applicants"].where(df["applicants"] > 0))
    df["is_break"] = (df["ir"] < 0).astype(int)
    df["is_flat"] = (df["ir"] == 0).astype(int)
    df["is_gain"] = (df["ir"] > 0).astype(int)
    df["public_share_pct"] = 100 * (df["Final public offer shares"] / df[C["base_shares"]])

    # Terciles
    df["demand_tercile"] = pd.qcut(df["sub_x"], 3, labels=["Low demand", "Mid demand", "High demand"])
    df["app_tercile"] = pd.qcut(df["applicants"], 3, labels=["Few applicants", "Mid applicants", "Many applicants"])
    df["size_tercile"] = pd.qcut(df["base_proceeds_hkd_mn"], 3, labels=["Small deal", "Mid deal", "Large deal"])
    return df


def demand_tercile_table(df: pd.DataFrame) -> pd.DataFrame:
    """Descriptive statistics across subscription demand terciles and the full sample."""
    groups = []

    # Full sample
    groups.append({
        "Group": "Full Sample (2026)",
        "N": len(df),
        "Mean IR (%)": f"{100 * df['ir'].mean():.2f}%",
        "Median IR (%)": f"{100 * df['ir'].median():.2f}%",
        "P25 IR (%)": f"{100 * df['ir'].quantile(0.25):.2f}%",
        "P75 IR (%)": f"{100 * df['ir'].quantile(0.75):.2f}%",
        "Break Rate (%)": f"{100 * df['is_break'].mean():.1f}%",
        "Median Sub (x)": f"{df['sub_x'].median():.1f}x",
        "Median Applicants": f"{df['applicants'].median():,.0f}",
        "Median Proceeds (HK$M)": f"{df['base_proceeds_hkd_mn'].median():.1f}",
        "Mean Public Offer (%)": f"{df['public_share_pct'].mean():.1f}%",
    })

    for name, part in df.groupby("demand_tercile", observed=True):
        groups.append({
            "Group": f"{name} (Sub: {part['sub_x'].min():.1f}x - {part['sub_x'].max():.1f}x)",
            "N": len(part),
            "Mean IR (%)": f"{100 * part['ir'].mean():.2f}%",
            "Median IR (%)": f"{100 * part['ir'].median():.2f}%",
            "P25 IR (%)": f"{100 * part['ir'].quantile(0.25):.2f}%",
            "P75 IR (%)": f"{100 * part['ir'].quantile(0.75):.2f}%",
            "Break Rate (%)": f"{100 * part['is_break'].mean():.1f}%",
            "Median Sub (x)": f"{part['sub_x'].median():.1f}x",
            "Median Applicants": f"{part['applicants'].median():,.0f}",
            "Median Proceeds (HK$M)": f"{part['base_proceeds_hkd_mn'].median():.1f}",
            "Mean Public Offer (%)": f"{part['public_share_pct'].mean():.1f}%",
        })
    return pd.DataFrame(groups)


def subgroup_breakdown_table(df: pd.DataFrame) -> pd.DataFrame:
    """Subgroup breakdown comparing demand terciles across quarters, A+H status, and size terciles."""
    rows = []

    # 1. By Quarter
    for q in ["2026Q1", "2026Q2", "2026Q3"]:
        sub = df[df["cohort"] == q]
        for name, part in sub.groupby("demand_tercile", observed=True):
            rows.append({
                "Category": "Quarter",
                "Subgroup": q,
                "Demand Group": str(name),
                "N": len(part),
                "Mean IR (%)": f"{100 * part['ir'].mean():.2f}%",
                "Median IR (%)": f"{100 * part['ir'].median():.2f}%",
                "Break Rate (%)": f"{100 * part['is_break'].mean():.1f}%",
                "Median Sub (x)": f"{part['sub_x'].median():.1f}x",
                "Median Proceeds (HK$M)": f"{part['base_proceeds_hkd_mn'].median():.1f}",
                "Mean Public Offer (%)": f"{part['public_share_pct'].mean():.1f}%",
                "Median Public Offer (%)": f"{part['public_share_pct'].median():.1f}%",
            })

    # 2. By A+H status
    for ah_val, label in [(1.0, "A+H Issuers"), (0.0, "Non-A+H Issuers")]:
        sub = df[df["ah_true"] == ah_val]
        for name, part in sub.groupby("demand_tercile", observed=True):
            rows.append({
                "Category": "Listing Route",
                "Subgroup": label,
                "Demand Group": str(name),
                "N": len(part),
                "Mean IR (%)": f"{100 * part['ir'].mean():.2f}%",
                "Median IR (%)": f"{100 * part['ir'].median():.2f}%",
                "Break Rate (%)": f"{100 * part['is_break'].mean():.1f}%",
                "Median Sub (x)": f"{part['sub_x'].median():.1f}x",
                "Median Proceeds (HK$M)": f"{part['base_proceeds_hkd_mn'].median():.1f}",
                "Mean Public Offer (%)": f"{part['public_share_pct'].mean():.1f}%",
                "Median Public Offer (%)": f"{part['public_share_pct'].median():.1f}%",
            })

    # 3. By Deal Size Tercile
    for size_label in ["Small deal", "Mid deal", "Large deal"]:
        sub = df[df["size_tercile"] == size_label]
        for name, part in sub.groupby("demand_tercile", observed=True):
            rows.append({
                "Category": "Offer Size",
                "Subgroup": size_label,
                "Demand Group": str(name),
                "N": len(part),
                "Mean IR (%)": f"{100 * part['ir'].mean():.2f}%",
                "Median IR (%)": f"{100 * part['ir'].median():.2f}%",
                "Break Rate (%)": f"{100 * part['is_break'].mean():.1f}%",
                "Median Sub (x)": f"{part['sub_x'].median():.1f}x",
                "Median Proceeds (HK$M)": f"{part['base_proceeds_hkd_mn'].median():.1f}",
                "Mean Public Offer (%)": f"{part['public_share_pct'].mean():.1f}%",
                "Median Public Offer (%)": f"{part['public_share_pct'].median():.1f}%",
            })

    return pd.DataFrame(rows)


def run_regressions(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    """Run stepwise OLS regressions of log(1 + IR) on subscription demand with robust/bootstrap inference."""
    reg = prepare_regression(df)

    specs = [
        ("M1: Raw Subscription Multiple", ["lsub"], "lsub"),
        ("M2: + Offer Proceeds (Deal Size)", ["lsub", "lproc"], "lsub"),
        ("M3: + A+H Anchor, Firm Age, Cornerstone", ["lsub", "lproc", "ah", "lage", "corner"], "lsub"),
        ("M4: + Hot Window (April-June / Q2)", ["lsub", "lproc", "ah", "lage", "corner", "hot"], "lsub"),
        ("M5: Raw Applicant Count", ["lapp"], "lapp"),
        ("M6: Applicant Count + Full Controls", ["lapp", "lproc", "ah", "lage", "corner", "hot"], "lapp"),
    ]

    # Add log applicants to regression frame
    reg["lapp"] = np.log(df.set_index("Stock Code").loc[reg["code"], "Public applicants"].values)

    reg = reg.replace([np.inf, -np.inf], np.nan).dropna(subset=["y", "month", "lsub", "lapp", "lproc", "ah", "lage", "corner", "hot"])
    results = []
    family = []

    for label, xs, focus in specs:
        z = reg[[ "y", "month", *xs ]].replace([np.inf, -np.inf], np.nan).dropna()
        X = sm.add_constant(z[xs].astype(float), has_constant="add")
        fit_hc3 = sm.OLS(z["y"].astype(float), X).fit(cov_type="HC3")

        clusters = z["month"].to_numpy()
        p_wild = np.nan
        if 2 <= len(np.unique(clusters)) <= 16:
            j = list(X.columns).index(focus)
            p_wild = wild_cluster_p(z["y"].to_numpy(float), X.to_numpy(), clusters, j)

        b = fit_hc3.params[focus]
        se = fit_hc3.bse[focus]
        p_hc3 = fit_hc3.pvalues[focus]
        r2 = fit_hc3.rsquared
        n = len(z)

        results.append({
            "Specification": label,
            "Focus Regressor": focus,
            "Coefficient (HC3 SE)": f"{b:.4f}{stars(p_hc3)} ({se:.4f})",
            "HC3 p-value": f"{p_hc3:.4f}",
            "Wild Cluster p": f"{p_wild:.4f}" if pd.notna(p_wild) else "—",
            "R-squared": f"{r2:.3f}",
            "N": n, "G": len(np.unique(clusters)), "coefficient": b, "hc3_se": se,
            "ci_lower": fit_hc3.conf_int().loc[focus, 0], "ci_upper": fit_hc3.conf_int().loc[focus, 1],
        })
        family.append(("Main Line A Regressions", f"{label} - {focus}", p_hc3))

    return pd.DataFrame(results), family


def aftermarket_performance_table(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze Day-5 and Day-20 aftermarket returns across demand terciles on a balanced window."""
    # Balanced sample where both Day 5 and Day 20 are available
    balanced = df.dropna(subset=["Day-5 BHR from Day-1 close (%)", "Day-20 BHR from Day-1 close (%)"]).copy()

    rows = []
    rows.append({
        "Group": "Full Balanced Sample",
        "N": len(balanced),
        "Mean Day-1 IR (%)": f"{100 * balanced['ir'].mean():.2f}%",
        "Median Day-1 IR (%)": f"{100 * balanced['ir'].median():.2f}%",
        "Mean Day-5 BHR (%)": f"{100 * balanced['Day-5 BHR from Day-1 close (%)'].mean():.2f}%",
        "Median Day-5 BHR (%)": f"{100 * balanced['Day-5 BHR from Day-1 close (%)'].median():.2f}%",
        "Positive Day-5 (%)": f"{100 * (balanced['Day-5 BHR from Day-1 close (%)'] > 0).mean():.1f}%",
        "Mean Day-20 BHR (%)": f"{100 * balanced['Day-20 BHR from Day-1 close (%)'].mean():.2f}%",
        "Median Day-20 BHR (%)": f"{100 * balanced['Day-20 BHR from Day-1 close (%)'].median():.2f}%",
        "Positive Day-20 (%)": f"{100 * (balanced['Day-20 BHR from Day-1 close (%)'] > 0).mean():.1f}%",
    })

    for name, part in balanced.groupby("demand_tercile", observed=True):
        rows.append({
            "Group": str(name),
            "N": len(part),
            "Mean Day-1 IR (%)": f"{100 * part['ir'].mean():.2f}%",
            "Median Day-1 IR (%)": f"{100 * part['ir'].median():.2f}%",
            "Mean Day-5 BHR (%)": f"{100 * part['Day-5 BHR from Day-1 close (%)'].mean():.2f}%",
            "Median Day-5 BHR (%)": f"{100 * part['Day-5 BHR from Day-1 close (%)'].median():.2f}%",
            "Positive Day-5 (%)": f"{100 * (part['Day-5 BHR from Day-1 close (%)'] > 0).mean():.1f}%",
            "Mean Day-20 BHR (%)": f"{100 * part['Day-20 BHR from Day-1 close (%)'].mean():.2f}%",
            "Median Day-20 BHR (%)": f"{100 * part['Day-20 BHR from Day-1 close (%)'].median():.2f}%",
            "Positive Day-20 (%)": f"{100 * (part['Day-20 BHR from Day-1 close (%)'] > 0).mean():.1f}%",
        })

    return pd.DataFrame(rows)


def plot_figures(df: pd.DataFrame) -> None:
    """Generate professional publication figures for Main Line A."""
    # Figure A1: Scatter of Log Subscription vs First-Day Return
    fig, (ax1, ax2) = new_fig(1, 2, figsize=(11, 4.8))
    for ax in (ax1, ax2):
        style_axes(ax)

    # ax1: Subscription Multiple vs First-day Return
    non_break = df[df["is_break"] == 0]
    is_break = df[df["is_break"] == 1]

    ax1.scatter(non_break["sub_x"], non_break["ir"], color=BLUE, alpha=0.75, s=32, label="Trading Gain (IR >= 0)", edgecolors="none")
    ax1.scatter(is_break["sub_x"], is_break["ir"], color=ORANGE, alpha=0.85, s=36, marker="^", label="Offer Break (IR < 0)", edgecolors="none")
    ax1.set_xscale("log")
    ax1.axhline(0, color=AXIS, lw=1.2, ls="--")
    ax1.set_xlabel("Public Subscription Multiple (times, log scale)", fontsize=9, color=INK2)
    ax1.set_ylabel("First-Day Initial Return (IR)", fontsize=9, color=INK2)
    ax1.legend(frameon=False, fontsize=8, loc="upper left")
    pct_axis(ax1, "y")

    # Add trend line on log scale
    x_vals = np.logspace(np.log10(df["sub_x"].min()), np.log10(df["sub_x"].max()), 100)
    log_x = np.log(df["sub_x"])
    fit = np.polyfit(log_x, df["ir"], 1)
    ax1.plot(x_vals, fit[0] * np.log(x_vals) + fit[1], color=INK, lw=1.5, ls="-", alpha=0.7)

    # ax2: Applicant Count vs First-day Return
    ax2.scatter(non_break["applicants"], non_break["ir"], color=BLUE, alpha=0.75, s=32, label="Trading Gain (IR >= 0)", edgecolors="none")
    ax2.scatter(is_break["applicants"], is_break["ir"], color=ORANGE, alpha=0.85, s=36, marker="^", label="Offer Break (IR < 0)", edgecolors="none")
    ax2.set_xscale("log")
    ax2.axhline(0, color=AXIS, lw=1.2, ls="--")
    ax2.set_xlabel("Public Applicants (persons, log scale)", fontsize=9, color=INK2)
    ax2.set_ylabel("First-Day Initial Return (IR)", fontsize=9, color=INK2)
    pct_axis(ax2, "y")

    log_app = np.log(df["applicants"])
    fit_app = np.polyfit(log_app, df["ir"], 1)
    app_vals = np.logspace(np.log10(df["applicants"].min()), np.log10(df["applicants"].max()), 100)
    ax2.plot(app_vals, fit_app[0] * np.log(app_vals) + fit_app[1], color=INK, lw=1.5, ls="-", alpha=0.7)

    fig.suptitle("Main Line A: Retail Subscription Heat vs First-Day Return (N = 113)", fontsize=11, color=INK, fontweight="bold", y=0.98)
    fig.tight_layout()
    fig.savefig(OUT / "fig_a1_subscription_scatter.png", dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)

    # Figure A2: Demand Terciles vs First-Day Return and Break Rate
    fig, (ax1, ax2) = new_fig(1, 2, figsize=(10, 4.5))
    for ax in (ax1, ax2):
        style_axes(ax)

    terciles = ["Low demand", "Mid demand", "High demand"]
    mean_irs = [100 * df[df["demand_tercile"] == t]["ir"].mean() for t in terciles]
    med_irs = [100 * df[df["demand_tercile"] == t]["ir"].median() for t in terciles]
    break_rates = [100 * df[df["demand_tercile"] == t]["is_break"].mean() for t in terciles]

    x = np.arange(len(terciles))
    width = 0.35

    # ax1: Return bars
    ax1.bar(x - width/2, mean_irs, width, label="Mean IR (%)", color=BLUE, alpha=0.85)
    ax1.bar(x + width/2, med_irs, width, label="Median IR (%)", color="#5c93c4", alpha=0.85)
    ax1.set_xticks(x)
    ax1.set_xticklabels(terciles, fontsize=9)
    ax1.set_ylabel("First-Day Return (%)", fontsize=9, color=INK2)
    ax1.legend(frameon=False, fontsize=8)
    ax1.axhline(0, color=AXIS, lw=1)
    for i, v in enumerate(mean_irs):
        ax1.text(i - width/2, v + 2, f"{v:.1f}%", ha="center", fontsize=8, color=INK)
    for i, v in enumerate(med_irs):
        ax1.text(i + width/2, v + 2, f"{v:.1f}%", ha="center", fontsize=8, color=INK)

    # ax2: Break Rate
    bars = ax2.bar(x, break_rates, width=0.45, color=ORANGE, alpha=0.85)
    ax2.set_xticks(x)
    ax2.set_xticklabels(terciles, fontsize=9)
    ax2.set_ylabel("Day-1 Offer Break Rate (%)", fontsize=9, color=INK2)
    ax2.set_ylim(0, 50)
    for i, v in enumerate(break_rates):
        ax2.text(i, v + 1.5, f"{v:.1f}%", ha="center", fontsize=8, color=INK, fontweight="bold")

    fig.suptitle("First-Day Performance and Offer Break Rates by Subscription Demand Tercile", fontsize=11, color=INK, fontweight="bold", y=0.98)
    fig.tight_layout()
    fig.savefig(OUT / "fig_a2_demand_performance.png", dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = load_data()

    # 1. Demand terciles summary
    tab_terciles = demand_tercile_table(df)
    tab_terciles.to_csv(OUT / "demand_summary.csv", index=False)

    # 2. Subgroup comparisons
    tab_subgroups = subgroup_breakdown_table(df)
    tab_subgroups.to_csv(OUT / "demand_subgroups.csv", index=False)

    # 3. Regressions
    tab_reg, family = run_regressions(df)
    tab_reg.to_csv(OUT / "demand_regressions.csv", index=False)

    # 4. Aftermarket performance
    tab_aftermarket = aftermarket_performance_table(df)
    tab_aftermarket.to_csv(OUT / "aftermarket_performance.csv", index=False)

    # 5. Figures
    plot_figures(df)

    # Multiplicity adjustment
    bh_table = bh_family(family)
    bh_table.to_csv(OUT / "multiplicity_bh.csv", index=False)

    rho_sub, p_sub = stats.spearmanr(df["sub_x"], df["ir"])
    rho_app, p_app = stats.spearmanr(df["applicants"], df["ir"])
    pd.DataFrame([{"variable": "subscription", "rho": rho_sub, "p": p_sub},
                  {"variable": "applicants", "rho": rho_app, "p": p_app}]).to_csv(OUT / "spearman.csv", index=False)
    report = "# Subscription demand: exploratory associations\n\nFinal demand is observed after pricing; these groups are retrospective. HC3 and exact Rademacher bootstrap use nine listing-month clusters.\n\n"
    for name in ["demand_summary.csv", "demand_subgroups.csv", "demand_regressions.csv", "aftermarket_performance.csv"]:
        report += "## " + name + "\n\n" + pd.read_csv(OUT / name).pipe(to_markdown) + "\n\n"
    (OUT / "subscription_heat.md").write_text(report.rstrip()+"\n")
    print("Subscription baseline written:", OUT)


if __name__ == "__main__":
    main()
