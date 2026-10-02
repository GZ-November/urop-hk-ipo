"""Which of listing route, listing quarter and VC/PE backing carries the 2026 first-day return?

Module A shows three large gaps in first-day returns (IR): by route (18A/18C
high, A+H low), by quarter (Q2 high, Q3 low) and by VC/PE backing. The three
overlap: every 18A/18C issuer is VC/PE-backed and 18A issuers list only in
Q1-Q2. This script separates them on the observed 2026 sample.

Outcome is log(1 + IR); standard errors are clustered by listing month.

Outputs (analysis/out/ir_decomposition/):
    crosstabs.md      Route x quarter and route x backing, N and mean IR
    regressions.md    Nested OLS models and incremental R-squared

Usage:
    python3 analysis/ir_decomposition_2026.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from shared.reporting import to_markdown
import research_inputs as inputs

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "out" / "ir_decomposition"

ROUTE = "C(route, Treatment('Conventional'))"
QUARTER = "C(cohort, Treatment('2026Q1'))"
BACKING = "vc"
CONTROLS = "log_proceeds + fixed_price + cornerstone"
MARKET = "z_hsi + z_ipo_count + z_hibor + z_balance"

MARKET_COLS = {
    "z_hsi": "HSI return over 20 trading days before prospectus (%)",
    "z_ipo_count": "HK ordinary IPO count in 90 calendar days before prospectus",
    "z_hibor": "1-month HIBOR before prospectus (%)",
    "z_balance": "Banking system aggregate balance before prospectus (HK$)",
}

MODELS = {
    "(1) Route": f"lir ~ {ROUTE}",
    "(2) Quarter": f"lir ~ {QUARTER}",
    "(3) VC/PE backing": f"lir ~ {BACKING}",
    "(4) Route + quarter": f"lir ~ {ROUTE} + {QUARTER}",
    "(5) Route + quarter + backing": f"lir ~ {ROUTE} + {QUARTER} + {BACKING}",
    "(6) + controls": f"lir ~ {ROUTE} + {QUARTER} + {BACKING} + {CONTROLS}",
    "(7) Market only": f"lir ~ {MARKET}",
    "(8) Route + backing + market": f"lir ~ {ROUTE} + {BACKING} + {MARKET}",
    "(9) Route + backing + market + quarter": f"lir ~ {ROUTE} + {BACKING} + {MARKET} + {QUARTER}",
}
FIRST_TABLE = [k for k in MODELS if k[:3] in {f"({i})" for i in range(1, 7)}]
MARKET_TABLE = ["(5) Route + quarter + backing", "(7) Market only", "(8) Route + backing + market",
                "(9) Route + backing + market + quarter"]

LABELS = {
    "C(route, Treatment('Conventional'))[T.18A biotech]": "18A biotech",
    "C(route, Treatment('Conventional'))[T.18C specialist tech]": "18C specialist tech",
    "C(route, Treatment('Conventional'))[T.A+H (19A)]": "A+H (19A)",
    "C(cohort, Treatment('2026Q1'))[T.2026Q2]": "Listed 2026Q2",
    "C(cohort, Treatment('2026Q1'))[T.2026Q3]": "Listed 2026Q3",
    "vc": "VC/PE-backed",
    "log_proceeds": "ln(gross proceeds, HK$)",
    "fixed_price": "Fixed price",
    "cornerstone": "Cornerstone (share of base offer)",
    "z_hsi": "HSI 20-day return before prospectus (z)",
    "z_ipo_count": "IPO count, prior 90 days (z)",
    "z_hibor": "1-month HIBOR (z)",
    "z_balance": "Banking aggregate balance (z)",
}


def prepare() -> pd.DataFrame:
    df = inputs.select_2026(inputs.load_panel()).copy()
    df["lir"] = np.log1p(df["ir"])
    df["vc"] = df[inputs.C["vc"]]
    df["log_proceeds"] = np.log(df["gross_proceeds"])
    df["fixed_price"] = (df[inputs.C["pricing"]] == "Fixed price").astype(int)
    df["cornerstone"] = df[inputs.C["corner"]]
    df["month_id"] = df["month"].astype(str)
    for name, col in MARKET_COLS.items():
        df[name] = (df[col] - df[col].mean()) / df[col].std()
    return df.dropna(subset=["lir", "vc", "log_proceeds", "cornerstone"])


def crosstabs(df: pd.DataFrame) -> str:
    def cell(g: pd.Series) -> str:
        return f"{len(g)} / {100 * g.mean():.0f}%" if len(g) else "0 / —"

    by_q = df.pivot_table(index="route", columns="cohort", values="ir", aggfunc=list).reindex(
        ["18A biotech", "18C specialist tech", "A+H (19A)", "Conventional"]
    )
    q_tab = by_q.apply(lambda col: col.map(lambda v: cell(pd.Series(v)) if isinstance(v, list) else "0 / —"))
    q_tab["All"] = [cell(df.loc[df.route == r, "ir"]) for r in q_tab.index]
    q_tab.loc["All"] = [cell(df.loc[df.cohort == q, "ir"]) for q in q_tab.columns[:-1]] + [cell(df["ir"])]

    df = df.assign(backing=np.where(df["vc"] == 1, "VC/PE-backed", "Not backed"))
    b_tab = df.pivot_table(index="route", columns="backing", values="ir", aggfunc=list).reindex(q_tab.index[:-1])
    b_tab = b_tab.apply(lambda col: col.map(lambda v: cell(pd.Series(v)) if isinstance(v, list) else "0 / —"))

    return "\n\n".join([
        "# Cross-tabs: cell = N / mean first-day return (2026)",
        "## Route x listing quarter", to_markdown(q_tab, "Route"),
        "## Route x VC/PE backing", to_markdown(b_tab, "Route"),
        "- Empty cells show where the three factors cannot be separated: 18A/18C issuers are all backed, "
        "and there is no 18A issuer in 2026Q3.",
    ]) + "\n"


def stars(p: float) -> str:
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def coef_table(fits: dict, names: list[str]) -> pd.DataFrame:
    sub = {n: fits[n] for n in names}
    rows = {}
    for t, label in LABELS.items():
        if any(t in m.params for m in sub.values()):
            rows[label] = [
                f"{m.params[t]:.2f}{stars(m.pvalues[t])} ({m.bse[t]:.2f})" if t in m.params else "" for m in sub.values()
            ]
    rows["N"] = [str(int(m.nobs)) for m in sub.values()]
    rows["R-squared"] = [f"{m.rsquared:.2f}" for m in sub.values()]
    rows["Adj. R-squared"] = [f"{m.rsquared_adj:.2f}" for m in sub.values()]
    return pd.DataFrame(rows, index=names).T


def r2_lost(df: pd.DataFrame, full_r2: float, drops: dict[str, str]) -> pd.DataFrame:
    vals = [f"{full_r2 - smf.ols(f, data=df).fit().rsquared:.3f}" for f in drops.values()]
    return pd.DataFrame({"R-squared lost when dropped": vals}, index=list(drops))


def regressions(df: pd.DataFrame) -> str:
    fits = {
        name: smf.ols(f, data=df).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(df["month_id"])[0]})
        for name, f in MODELS.items()
    }
    inc5 = r2_lost(df, fits["(5) Route + quarter + backing"].rsquared, {
        "Route": f"lir ~ {QUARTER} + {BACKING}",
        "Quarter": f"lir ~ {ROUTE} + {BACKING}",
        "VC/PE backing": f"lir ~ {ROUTE} + {QUARTER}",
    })
    inc9 = r2_lost(df, fits["(9) Route + backing + market + quarter"].rsquared, {
        "Route": f"lir ~ {BACKING} + {MARKET} + {QUARTER}",
        "VC/PE backing": f"lir ~ {ROUTE} + {MARKET} + {QUARTER}",
        "Market variables (4)": f"lir ~ {ROUTE} + {BACKING} + {QUARTER}",
        "Quarter": f"lir ~ {ROUTE} + {BACKING} + {MARKET}",
    })
    return "\n\n".join([
        "# Nested OLS, outcome = log(1 + first-day return), 2026",
        "Coefficients with month-clustered standard errors in parentheses. Omitted groups: Conventional route, "
        "listed 2026Q1, not VC/PE-backed. Market variables are standardized (mean 0, s.d. 1) and measured "
        "before the prospectus date. * p<0.10, ** p<0.05, *** p<0.01.",
        "## A. Route, quarter and backing", to_markdown(coef_table(fits, FIRST_TABLE), ""),
        to_markdown(inc5, "Factor (model 5)"),
        "## B. Can market conditions replace the quarter?", to_markdown(coef_table(fits, MARKET_TABLE), ""),
        to_markdown(inc9, "Factor (model 9)"),
        "- Nine listing months give few clusters, so the p-values are indicative only. "
        "Backing is identified only within Conventional and A+H issuers, because all 18A/18C issuers are backed.",
        "- A coefficient b on log(1 + IR) is roughly a 100*b percent difference in (1 + IR).",
    ]) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = prepare()
    (OUT / "crosstabs.md").write_text(crosstabs(df), encoding="utf-8")
    (OUT / "regressions.md").write_text(regressions(df), encoding="utf-8")
    print(f"IR decomposition written to {OUT.relative_to(ROOT)}/ (N = {len(df)})")


if __name__ == "__main__":
    main()
