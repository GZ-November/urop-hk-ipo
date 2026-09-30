"""Source-reported margin snapshots and separate retail-demand proxy regressions.

Sparse, censored media broker surveys cannot identify information cascades or
individual leverage. Earliest/latest observations are not assumed to be opening/
closing-day observations. Full-sample proxy models remain a separate layer.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

import extended_analysis_2026 as ext
from module_a_stylized_facts import (
    AXIS, BLUE, INK, INK2, ORANGE, ROOT,
    load_panel, new_fig, pct_axis, select_2026, style_axes, to_markdown,
)

OUT = ROOT / "analysis" / "out" / "margin"
DATA = ROOT / "pipeline" / "exports" / "HKIPO-2026-margin-daily.csv"
REQUIRED = ["stock_code", "date", "margin_total_hkd", "margin_multiple", "source"]


# ------------------------------------------------------------------ validation & preparation

def validate(margin: pd.DataFrame, sample: pd.DataFrame) -> pd.DataFrame:
    """Validate source-backed snapshots; declining observations are permitted."""
    missing = [c for c in REQUIRED if c not in margin.columns]
    if missing:
        raise ValueError(f"Margin file lacks columns: {missing}")
    frame = margin.copy()
    if frame[["stock_code", "date"]].isna().any().any():
        raise ValueError("Missing stock_code or date")
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    if frame["date"].isna().any():
        raise ValueError("Unparseable dates in the margin file")
    if frame.duplicated(["stock_code", "date"]).any():
        raise ValueError("Duplicate issuer/date snapshots; resolve survey scope before ingestion")
    if not frame["source"].fillna("").astype(str).str.match(r"https?://\S+$").all():
        raise ValueError("Each snapshot requires a source URL")
    unknown = set(frame["stock_code"]) - set(sample["Stock Code"])
    if unknown:
        raise ValueError(f"Issuers outside the 2026 sample: {sorted(unknown)}")
    window = sample.set_index("Stock Code")[["Subscription opening date", "Subscription closing date"]].apply(pd.to_datetime)
    if window.loc[frame["stock_code"]].isna().any().any():
        raise ValueError("Missing subscription window")
    outside = frame[(frame["date"] < frame["stock_code"].map(window["Subscription opening date"]))
                    | (frame["date"] > frame["stock_code"].map(window["Subscription closing date"]))]
    if len(outside):
        raise ValueError(f"{len(outside)} rows fall outside the issuer's subscription period")
    for col in ("margin_total_hkd", "margin_multiple"):
        values = pd.to_numeric(frame[col], errors="coerce")
        if not np.isfinite(values).all():
            raise ValueError(f"Missing or nonfinite {col}")
        if (values < 0).any():
            raise ValueError(f"Negative {col}")
        frame[col] = values
    if "initial_public_value_hkd" in frame:
        base = pd.to_numeric(frame["initial_public_value_hkd"], errors="coerce")
        if not (np.isfinite(base) & (base > 0)).all():
            raise ValueError("Invalid public tranche denominator")
        if not np.allclose(frame["margin_multiple"], frame["margin_total_hkd"] / base):
            raise ValueError("Margin multiple disagrees with fixed public tranche denominator")
        if frame.assign(base=base).groupby("stock_code")["base"].nunique().gt(1).any():
            raise ValueError("Public tranche denominator changes within issuer")
    frame["on_close"] = frame["date"].eq(frame["stock_code"].map(window["Subscription closing date"]))
    return frame.sort_values(["stock_code", "date"])


def per_issuer(margin: pd.DataFrame) -> pd.DataFrame:
    """Summarize earliest/latest observations; neither implies a complete window."""
    g = margin.sort_values(["stock_code", "date"]).groupby("stock_code")
    out = pd.DataFrame({"final_multiple": g["margin_multiple"].last(), "first_multiple": g["margin_multiple"].first(),
                        "days": g["date"].nunique(), "first_date": g["date"].first(), "last_date": g["date"].last(),
                        "first_total_b": g["margin_total_hkd"].first() / 1e9, "final_total_b": g["margin_total_hkd"].last() / 1e9,
                        "on_close": g["on_close"].last()})
    out["comparable_scope"] = g["source_group"].nunique().eq(1) if "source_group" in margin else False
    return out


def cascade_summary(pi: pd.DataFrame) -> pd.DataFrame:
    """Observed endpoint growth, requiring positive baseline and constant survey scope."""
    multi = pi[(pi["days"] > 1) & (pi["first_multiple"] > 0) & pi["comparable_scope"]].copy()
    multi["cascade_ratio"] = multi["final_multiple"] / multi["first_multiple"]
    return multi


def safe_focus(d, y, xs, focus):
    z = d[[y, "month", *xs]].replace([np.inf, -np.inf], np.nan).dropna()
    x = np.column_stack([np.ones(len(z)), z[xs].to_numpy(float)])
    if len(z) <= len(xs) + 2 or np.linalg.matrix_rank(x) < x.shape[1]:
        return {"n": len(z), **{k: np.nan for k in ("b", "se", "p", "p_wild", "r2")}}
    leverage = np.einsum("ij,ji->i", x, np.linalg.pinv(x))
    if (leverage >= 1 - 1e-9).any():
        return {"n": len(z), **{k: np.nan for k in ("b", "se", "p", "p_wild", "r2")}}
    return ext.ols_focus(z, y, xs, focus)


def prepare_full_sample(y26: pd.DataFrame) -> pd.DataFrame:
    """Prepare 2026 regression frame with Idea 13 microstructure variables."""
    extra = pd.DataFrame({
        "code": y26["Stock Code"],
        "intraday_vol": (pd.to_numeric(y26["First trading day high (HK$)"]) - pd.to_numeric(y26["First trading day low (HK$)"])) / pd.to_numeric(y26["IPO Subscription Price (HK$)"]),
        "flip": pd.to_numeric(y26["First-day flipping ratio (%)"]),
        "hibor": pd.to_numeric(y26["1-month HIBOR before prospectus (%)"]),
        "sub_ratio": pd.to_numeric(y26["Subscription Ratio (times)"]),
    })
    d = ext.prepare(y26).merge(extra, on="code", how="inner")
    d["lintraday"] = np.log(d["intraday_vol"].where(d["intraday_vol"] > 0))
    return d


# ------------------------------------------------------------------ plotting

def fig_margin(margin_frame: pd.DataFrame, d_margin: pd.DataFrame, d_full: pd.DataFrame, out_path) -> None:
    """Publication-quality 3-panel figure for margin financing and cascade dynamics."""
    fig, (ax1, ax2, ax3) = new_fig(1, 3, figsize=(14, 4.2))
    for ax in (ax1, ax2, ax3):
        style_axes(ax)

    # Panel 1: Margin Multiple Expansion (Day 1 vs Final)
    pi = per_issuer(margin_frame).sort_values("final_multiple")
    x = np.arange(len(pi))
    ax1.barh(x - 0.18, pi["first_multiple"], height=0.35, color=BLUE, alpha=0.7, label="Earliest observed")
    ax1.barh(x + 0.18, pi["final_multiple"], height=0.35, color=ORANGE, alpha=0.85, label="Latest observed")
    ax1.set_yticks(x)
    ax1.set_yticklabels(pi.index, fontsize=7)
    ax1.set_xlabel("Margin Subscription Multiple (times)", fontsize=8, color=INK2)
    ax1.set_title("Panel A: Earliest vs Latest Observations", fontsize=9, color=INK, fontweight="bold")
    ax1.legend(frameon=False, fontsize=7, loc="lower right")

    # Panel 2: Final Margin Multiple vs IR
    ax2.scatter(d_margin["final_multiple"], d_margin["ir"], color=BLUE, s=32, alpha=0.85, edgecolors="none")
    # Linear fit
    valid = d_margin.dropna(subset=["final_multiple", "ir"])
    if len(valid) > 2:
        slope, intercept, rval, pval, _ = stats.linregress(valid["final_multiple"], valid["ir"])
        x_grid = np.linspace(valid["final_multiple"].min(), valid["final_multiple"].max(), 50)
        ax2.plot(x_grid, intercept + slope * x_grid, color=ORANGE, lw=1.5, ls="--", label=f"Fit (r = {rval:.2f}, p = {pval:.3f})")
        ax2.legend(frameon=False, fontsize=7, loc="lower right")
    ax2.axhline(0, color=AXIS, lw=0.8)
    ax2.set_xlabel("Latest Observed Margin Multiple (times)", fontsize=8, color=INK2)
    ax2.set_ylabel("First-Day Return (IR)", fontsize=8, color=INK2)
    ax2.set_title(f"Panel B: Observed Margin vs IR (N = {len(d_margin)})", fontsize=9, color=INK, fontweight="bold")
    pct_axis(ax2)

    # Panel 3: Model 13.1 Subscription Ratio vs Intraday Volatility (Full Sample N = 106)
    for hot, col, lbl in [(0.0, BLUE, "Other months"), (1.0, ORANGE, "April-June")]:
        sub = d_full[d_full["hot"] == hot]
        ax3.scatter(sub["sub_ratio"], sub["intraday_vol"], color=col, s=24, alpha=0.75, edgecolors="none", label=lbl)
    ax3.set_xscale("log")
    ax3.set_xlabel("Public Subscription Ratio (log scale, times)", fontsize=8, color=INK2)
    ax3.set_ylabel("First-Day Intraday Volatility ((High-Low)/Offer)", fontsize=8, color=INK2)
    ax3.set_title(f"Panel C: Subscription vs Price Range (N = {len(d_full)})", fontsize=9, color=INK, fontweight="bold")
    ax3.legend(frameon=False, fontsize=7, loc="upper left")
    pct_axis(ax3)

    fig.suptitle("Idea 13: Margin Snapshots, Retail Demand, and First-Day Price Range", fontsize=11, color=INK, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


# ------------------------------------------------------------------ main

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    y26 = select_2026(load_panel())
    d_full = prepare_full_sample(y26)

    # Check for margin CSV
    has_margin = DATA.exists()
    margin_frame = None
    if has_margin:
        margin_frame = validate(pd.read_csv(DATA), y26)
    family = []

    report_parts = ["# Margin Snapshots & Retail Demand, 2026 (Idea 13)\n"]

    if has_margin and margin_frame is not None:
        pi = per_issuer(margin_frame)
        d_merged = d_full.merge(pi, left_on="code", right_index=True, how="inner")
        d_merged["lfinal"] = np.log(d_merged["final_multiple"].where(d_merged["final_multiple"] > 0))
        rho = stats.spearmanr(d_merged["lfinal"], d_merged["ir"], nan_policy="omit")

        # Table 1: Broker Margin OLS
        rows_margin = []
        for label, xs in [
            ("ln latest observed margin multiple", ["lfinal"]),
            ("+ April-June window", ["lfinal", "hot"]),
            ("+ window + ln size", ["lfinal", "hot", "lproc"]),
        ]:
            r = safe_focus(d_merged, "y", xs, "lfinal")
            family.append(("Observed margin", label, r["p"]))
            rows_margin.append([
                label,
                f"{r['b']:.3f}{ext.stars(r['p'])} ({r['se']:.3f})",
                f"{r['p']:.3f}",
                "—" if np.isnan(r["p_wild"]) else f"{r['p_wild']:.3f}",
                str(r["n"]),
            ])
        tab_margin = pd.DataFrame(rows_margin, columns=["Specification", "Coefficient (HC3 s.e.)", "HC3 p", "Wild cluster p", "N"])

        close_sample = d_merged[d_merged["on_close"]]
        close_fit = safe_focus(close_sample, "y", ["lfinal", "hot", "lproc"], "lfinal")
        family.append(("Observed margin", "Closing-day snapshots, window + size", close_fit["p"]))
        close_result = (f"coefficient = {close_fit['b']:.3f}, HC3 p = {close_fit['p']:.3f}" if np.isfinite(close_fit["p"])
                        else "HC3 model not estimable (insufficient sample, rank or unit-leverage constraint)")
        report_parts.append(f"Closing-day snapshot sensitivity: N = {close_fit['n']}, {close_result}. "
                            "A closing-day snapshot may still precede the broker cutoff. Non-closing observations are censored and differ in time to deadline.\n")
        # Table 2: Information Cascade Dynamics (Day 1 vs Final)
        cascades = cascade_summary(pi)
        mean_ratio = cascades["cascade_ratio"].mean()
        median_ratio = cascades["cascade_ratio"].median()
        cascades_tab = cascades.reset_index().rename(columns={
            "stock_code": "Stock Code",
            "first_multiple": "Earliest Observed Multiple",
            "final_multiple": "Latest Observed Multiple",
            "first_total_b": "Earliest Margin (B HKD)",
            "final_total_b": "Latest Margin (B HKD)",
            "cascade_ratio": "Observed Growth Ratio",
        })
        cascades_tab["Earliest Observed Multiple"] = cascades_tab["Earliest Observed Multiple"].map("{:.1f}x".format)
        cascades_tab["Latest Observed Multiple"] = cascades_tab["Latest Observed Multiple"].map("{:.1f}x".format)
        cascades_tab["Earliest Margin (B HKD)"] = cascades_tab["Earliest Margin (B HKD)"].map("{:.1f}".format)
        cascades_tab["Latest Margin (B HKD)"] = cascades_tab["Latest Margin (B HKD)"].map("{:.1f}".format)
        cascades_tab["Observed Growth Ratio"] = cascades_tab["Observed Growth Ratio"].map("{:.2f}x".format)

        report_parts.append(f"""## 1. Broker Margin Financing Panel (N = {len(d_merged)} issuers)

Source-reported broker-survey snapshots cover {len(d_merged)} of {len(d_full)} issuers ({len(margin_frame)} observations). Only {int(pi["on_close"].sum())} have a snapshot on the subscription closing date. No missing dates are interpolated. These are media-reported survey amounts, not audited market-wide totals.
- **Rank correlation** of latest observed margin multiple with first-day return (IR): $\\rho = {rho.statistic:.2f}$ ($p = {rho.pvalue:.3f}$).
- **Observed growth** in {len(cascades)} issuers with multiple dates and a constant named survey scope: mean **{mean_ratio:.2f}x**, median **{median_ratio:.2f}x**. Endpoint growth does not establish acceleration, exponential growth or herding. Broker membership within a news survey remains unspecified.

### Latest Observed Margin Multiple vs First-Day Return (IR)

{to_markdown(tab_margin.set_index('Specification'), 'Specification')}

### Growth Between Observed Endpoints

{to_markdown(cascades_tab.set_index('Stock Code'), 'Stock Code')}
""")
        # Figure 10
        fig_margin(margin_frame, d_merged, d_full, OUT / "fig10_margin_cascades.png")
        report_parts.append("![Idea 13 Margin Cascades](fig10_margin_cascades.png)\n")
    else:
        report_parts.append("## 1. Broker Margin Financing Panel\n\nNo verified broker margin file found or invalid data.\n")

    # Table 3: Model 13.1 Full-Sample Econometric Regressions (N = 106)
    rows_model13 = []
    complete = {dep: d_full.replace([np.inf, -np.inf], np.nan).dropna(subset=[dep, "lsub", "lapp", "hibor", "lproc", "hot", "month"]) for dep in ("intraday_vol", "flip")}
    # Dependent: Intraday Volatility
    for label, dep, focus, xs in [
        ("Intraday Range ~ ln Subscription Ratio", "intraday_vol", "lsub", ["lsub"]),
        ("+ ln Applicants + HIBOR + ln Size", "intraday_vol", "lsub", ["lsub", "lapp", "hibor", "lproc"]),
        ("+ Window (Hot)", "intraday_vol", "lsub", ["lsub", "lapp", "hibor", "lproc", "hot"]),
        ("Flipping Ratio ~ ln Subscription Ratio", "flip", "lsub", ["lsub"]),
        ("+ ln Applicants + HIBOR + ln Size", "flip", "lsub", ["lsub", "lapp", "hibor", "lproc"]),
        ("+ Window (Hot)", "flip", "lsub", ["lsub", "lapp", "hibor", "lproc", "hot"]),
    ]:
        r = safe_focus(complete[dep], dep, xs, focus)
        family.append(("Retail proxies", label, r["p"]))
        rows_model13.append([
            label,
            f"{r['b']:.3f}{ext.stars(r['p'])} ({r['se']:.3f})",
            f"{r['p']:.3f}",
            "—" if np.isnan(r["p_wild"]) else f"{r['p_wild']:.3f}",
            f"{r['r2']:.3f}",
            str(r["n"]),
        ])
    tab_model13 = pd.DataFrame(rows_model13, columns=["Specification", "Focus Coeff (HC3 s.e.)", "HC3 p", "Wild cluster p", "R²", "N"])

    report_parts.append(f"""## 2. Model 13.1: Full-Sample Retail Frenzy & Intraday Price Discovery (N = {len(d_full)})

Following **Idea 13 (Model 13.1)** in `docs/RESEARCH_IDEAS.md`:
$$\\text{{IntradayRange}}_i = \\alpha_0 + \\beta_1 \\ln(\\text{{SubscriptionRatio}}_i) + \\beta_2 \\ln(\\text{{PublicApplicants}}_i) + \\beta_3 \\text{{HIBOR1m}}_i + \\gamma \\mathbf{{X}}_i + \\varepsilon_i$$
$$\\text{{FirstDayFlipping}}_i = \\alpha_0 + \\beta_1 \\ln(\\text{{SubscriptionRatio}}_i) + \\beta_2 \\ln(\\text{{PublicApplicants}}_i) + \\beta_3 \\text{{HIBOR1m}}_i + \\gamma \\mathbf{{X}}_i + \\varepsilon_i$$

### Econometric Results

{to_markdown(tab_model13.set_index('Specification'), 'Specification')}

### Interpretation

Nested models use the same finite complete-case sample within each outcome. Intraday range / offer is a price amplitude, not realized volatility.
Subscription intensity, applicants and HIBOR are proxies. These regressions do not observe individual borrowing, loan repayment or investor herding;
they cannot establish that leverage causes flipping. Read the controlled estimates and cluster p-values alongside the simple correlations.

""")

    fam = ext.bh_family(family)
    report_parts.append("## Multiplicity (all reported HC3 tests)\n\n" + to_markdown(fam.set_index("Rank"), "Rank"))
    if has_margin:
        pi.reset_index().to_csv(OUT / "coverage.csv", index=False)
    (OUT / "margin.md").write_text("\n".join(report_parts), encoding="utf-8")
    print(f"Margin analysis written to {(OUT / 'margin.md').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
