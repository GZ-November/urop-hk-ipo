"""Is the 2026Q2 first-day-return premium a calendar quarter or a shorter window?

q2_breakdown_2026.py shows the Q2 premium is broad across issuers and sectors.
This script splits the year by listing month and tests whether a quarter dummy,
a single Apr-Jun "hot window" dummy, or free month dummies describe the data best.

Outputs (analysis/out/monthly_breakdown/monthly_breakdown.md):
    1. By listing month: N, IR distribution, pricing mix, demand, pre-prospectus market
    2. Longest gaps between consecutive listings
    3. Time-structure models for log(1 + IR): quarters vs hot window vs months
    4. Tests inside and at the edges of the hot window

Usage:
    python3 analysis/monthly_breakdown_2026.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

import module_a_stylized_facts as ma
from q2_breakdown_2026 import prepare

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "out" / "monthly_breakdown"

HSI = "HSI return over 20 trading days before prospectus (%)"
COUNT = "HK ordinary IPO count in 90 calendar days before prospectus"
HOT_MONTHS = {"2026-04", "2026-05", "2026-06"}


def monthly_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = {}
    for m, g in df.groupby("month_id"):
        ir = g["ir"]
        rows[m] = {
            "N": len(g),
            "Mean IR": f"{100 * ir.mean():.0f}%",
            "Median IR": f"{100 * ir.median():.0f}%",
            "IR < 0": f"{100 * (ir < 0).mean():.0f}%",
            "IR > 100%": f"{100 * (ir > 1).mean():.0f}%",
            "Fixed price": f"{100 * (g[ma.C['pricing']] == 'Fixed price').mean():.0f}%",
            "Median public subscription (x)": f"{g[ma.C['sub']].median():,.0f}",
            "HSI 20d before prospectus": f"{100 * g[HSI].mean():.1f}%",
            "IPOs in prior 90 days": f"{g[COUNT].mean():.0f}",
        }
    return pd.DataFrame(rows).T


def gap_table(df: pd.DataFrame, k: int = 4) -> pd.DataFrame:
    d = df["listing_date"].sort_values().reset_index(drop=True)
    gaps = d.diff().dt.days
    rows = [(d[i - 1].date(), d[i].date(), int(gaps[i])) for i in gaps.nlargest(k).index]
    return pd.DataFrame(rows, columns=["Last listing before", "Next listing", "Days"]).sort_values("Last listing before").set_index("Last listing before")


def time_models(df: pd.DataFrame) -> pd.DataFrame:
    df = df.assign(hot=df["month_id"].isin(HOT_MONTHS).astype(int))
    ctrl = "C(route, Treatment('Conventional')) + C(sector)"
    groups = pd.factorize(df["month_id"])[0]
    specs = {
        "Quarter dummies": "C(cohort)",
        "Hot window (Apr-Jun) dummy": "hot",
        "Month dummies": "C(month_id)",
    }
    rows = {}
    for name, rhs in specs.items():
        for label, extra in (("", ""), (" + route + sector", f" + {ctrl}")):
            m = smf.ols(f"lir ~ {rhs}{extra}", data=df).fit()
            rows[name + label] = {
                "Parameters": int(m.df_model) + 1,
                "R-squared": f"{m.rsquared:.3f}",
                "Adj. R-squared": f"{m.rsquared_adj:.3f}",
                "AIC": f"{m.aic:.1f}",
            }
    hot = smf.ols(f"lir ~ hot + {ctrl}", data=df).fit(cov_type="cluster", cov_kwds={"groups": groups})
    hot_hc = smf.ols(f"lir ~ hot + {ctrl}", data=df).fit(cov_type="HC3")
    tab = pd.DataFrame(rows).T
    note = (
        f"Hot-window coefficient (with route + sector): {hot.params['hot']:.2f}; "
        f"s.e. {hot.bse['hot']:.2f} clustered by month, {hot_hc.bse['hot']:.2f} heteroskedasticity-robust (HC3)."
    )
    return tab, note


def restriction_tests(df: pd.DataFrame) -> list[str]:
    df = df.assign(hot=df["month_id"].isin(HOT_MONTHS).astype(int))
    ctrl = "C(route, Treatment('Conventional')) + C(sector)"
    month = smf.ols(f"lir ~ C(month_id) + {ctrl}", data=df).fit()
    out = []
    for label, rhs in (("hot-window dummy", "hot"), ("quarter dummies", "C(cohort)")):
        small = smf.ols(f"lir ~ {rhs} + {ctrl}", data=df).fit()
        f, p, _ = month.compare_f_test(small)
        out.append(f"Restricting month dummies to the {label}: F = {f:.2f}, p = {p:.3f}.")
    ir = df.set_index("month_id")["ir"]
    apr_jun = [ir[m].values for m in sorted(HOT_MONTHS)]
    out.append(f"IR equal across Apr, May, Jun: Kruskal-Wallis p = {stats.kruskal(*apr_jun).pvalue:.3f}.")
    out.append(f"IR equal across Jan, Feb, Mar: Kruskal-Wallis p = "
               f"{stats.kruskal(*[ir[m].values for m in ('2026-01', '2026-02', '2026-03')]).pvalue:.3f}.")
    out.append(f"Mar vs Apr: Mann-Whitney p = {stats.mannwhitneyu(ir['2026-03'], ir['2026-04']).pvalue:.3f}; "
               f"Jun vs Jul: Mann-Whitney p = {stats.mannwhitneyu(ir['2026-06'], ir['2026-07']).pvalue:.3f}.")
    hot, rest = df.loc[df.hot == 1, "ir"], df.loc[df.hot == 0, "ir"]
    out.append(f"Hot window vs rest: mean IR {100 * hot.mean():.0f}% (n = {len(hot)}) vs {100 * rest.mean():.0f}% "
               f"(n = {len(rest)}); Mann-Whitney p = {stats.mannwhitneyu(hot, rest).pvalue:.2g}.")
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = prepare()
    models, model_note = time_models(df)
    md = ma.to_markdown
    bullet = lambda ns: "\n".join(f"- {n}" for n in ns)
    text = "\n\n".join([
        "# 2026 first-day returns by listing month (N = 106)",
        "## 1. By listing month", md(monthly_table(df), "Month"),
        "## 2. Longest gaps between consecutive listings", md(gap_table(df), "Last listing before"),
        "## 3. Time-structure models for log(1 + IR)", md(models, "Model"), "- " + model_note,
        "## 4. Tests", bullet(restriction_tests(df)),
        "- Months with 2 or 5 deals (Aug, Sep) are too thin to read individually.",
    ]) + "\n"
    (OUT / "monthly_breakdown.md").write_text(text, encoding="utf-8")
    print(f"Monthly breakdown written to {OUT.relative_to(ROOT)}/ (N = {len(df)})")


if __name__ == "__main__":
    main()
