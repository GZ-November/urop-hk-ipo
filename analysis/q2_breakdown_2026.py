"""Where does the 2026Q2 first-day-return premium come from?

ir_decomposition_2026.py shows that listing quarter is the largest single factor
and that market variables measured before the prospectus do not absorb the 2026Q2
premium. This script asks whether the premium is (a) a handful of individual
deals, (b) a sector mix effect, or (c) broad across sectors.

Sectors follow the Hang Seng Industry Classification (HSICS) code already in the
panel, grouped by code prefix; the group names are read off the issuers'
principal-business descriptions.

Outputs (analysis/out/q2_breakdown/q2_breakdown.md):
    1. Sector mix by quarter
    2. Mean / median IR by sector and quarter
    3. Concentration: how much of the Q2 mean is the top deals
    4. Q2 premium after sector controls and after dropping top deals
    5. Q2 issuers ranked by IR

Usage:
    python3 analysis/q2_breakdown_2026.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from shared.reporting import to_markdown
import research_inputs as inputs

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "out" / "q2_breakdown"

SECTORS = {
    "051": "Materials & mining", "052": "Materials & mining", "053": "Materials & mining",
    "101": "Industrials & equipment", "103": "Industrials & equipment",
    "231": "Consumer discretionary", "232": "Consumer discretionary",
    "235": "Consumer discretionary", "237": "Consumer discretionary",
    "251": "Consumer staples", "252": "Consumer staples",
    "281": "Biotech & pharma",
    "282": "Medical devices & services",
    "502": "Other", "601": "Other",
    "701": "IT hardware & robotics", "702": "Software & AI", "703": "Semiconductors",
}
SECTOR_ORDER = [
    "Semiconductors", "Software & AI", "IT hardware & robotics", "Biotech & pharma",
    "Medical devices & services", "Industrials & equipment", "Consumer discretionary",
    "Consumer staples", "Materials & mining", "Other",
]
QUARTERS = ["2026Q1", "2026Q2", "2026Q3"]
IND = "Industry classification code"


def prepare() -> pd.DataFrame:
    df = inputs.select_2026(inputs.load_panel()).copy()
    df["lir"] = np.log1p(df["ir"])
    code = df[IND].astype(int).astype(str).str.zfill(6)
    df["sector"] = code.str[:3].map(SECTORS)
    assert df["sector"].notna().all(), "unmapped HSICS prefix"
    df["month_id"] = df["month"].astype(str)
    df["name"] = (
        df["Company Name at time of listing"]
        .str.replace(r"\s*-\s*[A-Z]\s*-\s*H Shares|\s*-\s*H Shares|,? ?(Co\.|Limited|Ltd\.?|Inc\.?|Tbk)\b.*", "", regex=True)
        .str.strip()
        .str.slice(0, 32)
    )
    return df


def cell(g: pd.Series) -> str:
    return f"{len(g)} / {100 * g.mean():.0f}% / {100 * g.median():.0f}%" if len(g) else "0"


def mix_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = {s: [f"{(df.loc[df.cohort == q, 'sector'] == s).sum()}" for q in QUARTERS] for s in SECTOR_ORDER}
    tab = pd.DataFrame(rows, index=QUARTERS).T
    tab.loc["Total"] = [str((df.cohort == q).sum()) for q in QUARTERS]
    return tab


def sector_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = {}
    for s in SECTOR_ORDER:
        g = df[df.sector == s]
        rows[s] = [cell(g.loc[g.cohort == q, "ir"]) for q in QUARTERS] + [cell(g["ir"])]
    tab = pd.DataFrame(rows, index=QUARTERS + ["All"]).T
    tab.loc["All"] = [cell(df.loc[df.cohort == q, "ir"]) for q in QUARTERS] + [cell(df["ir"])]
    return tab


def concentration(df: pd.DataFrame) -> pd.DataFrame:
    rows = {}
    for q in QUARTERS:
        ir = df.loc[df.cohort == q, "ir"].sort_values(ascending=False)
        rows[q] = {
            "N": len(ir),
            "Mean IR": f"{100 * ir.mean():.0f}%",
            "Median IR": f"{100 * ir.median():.0f}%",
            "Mean without top 3": f"{100 * ir.iloc[3:].mean():.0f}%",
            "Mean without top 5": f"{100 * ir.iloc[5:].mean():.0f}%",
            "Share of deals with IR > 100%": f"{100 * (ir > 1).mean():.0f}%",
            "Share of deals with IR > 50%": f"{100 * (ir > 0.5).mean():.0f}%",
        }
    return pd.DataFrame(rows)


def premium_table(df: pd.DataFrame) -> pd.DataFrame:
    """Coefficient on Listed-2026Q2 (vs 2026Q1) and 2026Q3 under alternative specifications."""
    route = "C(route, Treatment('Conventional'))"
    quarter = "C(cohort, Treatment('2026Q1'))"
    sector = "C(sector)"
    q2 = f"{quarter}[T.2026Q2]"
    q3 = f"{quarter}[T.2026Q3]"

    def fit(data: pd.DataFrame, rhs: str):
        return smf.ols(f"lir ~ {rhs}", data=data).fit(
            cov_type="cluster", cov_kwds={"groups": pd.factorize(data["month_id"])[0]}
        )

    top5 = df.loc[df.cohort == "2026Q2"].nlargest(5, "ir").index
    specs = {
        "Quarter only": (df, quarter),
        "+ route": (df, f"{quarter} + {route}"),
        "+ sector": (df, f"{quarter} + {sector}"),
        "+ route + sector": (df, f"{quarter} + {route} + {sector}"),
        "+ route + sector, drop Q2 top 5": (df.drop(top5), f"{quarter} + {route} + {sector}"),
        "+ route + sector, drop top 5 of every quarter": (
            df.drop(df.groupby("cohort")["ir"].nlargest(5).index.get_level_values(1)),
            f"{quarter} + {route} + {sector}",
        ),
    }
    rows = {}
    for name, (data, rhs) in specs.items():
        m = fit(data, rhs)
        star = lambda p: "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""
        rows[name] = {
            "N": int(m.nobs),
            "Q2 vs Q1": f"{m.params[q2]:.2f}{star(m.pvalues[q2])} ({m.bse[q2]:.2f})",
            "Q3 vs Q1": f"{m.params[q3]:.2f}{star(m.pvalues[q3])} ({m.bse[q3]:.2f})",
            "R-squared": f"{m.rsquared:.2f}",
        }
    return pd.DataFrame(rows).T


def q2_ranked(df: pd.DataFrame) -> pd.DataFrame:
    g = df[df.cohort == "2026Q2"].sort_values("ir", ascending=False)
    tab = pd.DataFrame({
        "Issuer": g["name"],
        "Sector": g["sector"],
        "Route": g["route"],
        "Pricing": g[inputs.C["pricing"]],
        "Public subscription (x)": g[inputs.C["sub"]].map("{:,.0f}".format),
        "IR": (100 * g["ir"]).map("{:.0f}%".format),
    })
    tab.index = range(1, len(tab) + 1)
    return tab


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = prepare()
    md = to_markdown
    text = "\n\n".join([
        "# Where does the 2026Q2 first-day-return premium come from? (2026, N = 106)",
        "## 1. Sector mix by listing quarter (number of IPOs)", md(mix_table(df), "Sector"),
        "## 2. By sector and quarter (cell = N / mean IR / median IR)", md(sector_table(df), "Sector"),
        "## 3. Concentration within each quarter", md(concentration(df), ""),
        "## 4. Quarter effects on log(1 + IR) under alternative specifications",
        "Coefficients vs 2026Q1 with month-clustered standard errors in parentheses. "
        "* p<0.10, ** p<0.05, *** p<0.01.",
        md(premium_table(df), "Specification"),
        "## 5. 2026Q2 issuers ranked by first-day return", md(q2_ranked(df), "Rank"),
        "- Sector groups come from the HSICS code prefix; names are read from principal-business descriptions.",
        "- Cells with only a few deals are not reliable: read sector rows together with the N.",
    ]) + "\n"
    (OUT / "q2_breakdown.md").write_text(text, encoding="utf-8")
    print(f"Q2 breakdown written to {OUT.relative_to(ROOT)}/ (N = {len(df)})")


if __name__ == "__main__":
    main()
