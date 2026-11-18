"""Self-test for ipo_metrics.py and regtable.py on synthetic data.

    python selftest.py            # pandas, numpy, scipy, statsmodels required
    python selftest.py --latex    # also compile the table if pdflatex exists

pyfixest / linearmodels checks run only when those packages are installed.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ipo_metrics import (bhar_panel, bootstrap_skew_adjusted_test,  # noqa: E402
                         calendar_time_portfolio, initial_returns, money_left_on_table,
                         price_revision, skew_adjusted_t, wealth_relative, winsorize)
from regtable import regression_table  # noqa: E402

rng = np.random.default_rng(7)


def check(cond: bool, msg: str) -> None:
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        raise SystemExit(1)


# winsorize: NaNs preserved, outliers clipped even when NaNs are present
s = pd.Series(np.r_[rng.normal(size=95), [50.0] * 3, [np.nan] * 12])
w = winsorize(s, 0.05, 0.05)
check(w.isna().sum() == 12, "winsorize keeps NaN as NaN")
check(w.max() < 50, "winsorize clips outliers despite NaNs")
g = pd.Series(np.repeat([2024, 2025], len(s) // 2))
wg = winsorize(s, 0.05, 0.05, by=g)
check(wg.index.equals(s.index) and wg.isna().sum() == 12, "group winsorize aligned")

# initial returns and market adjustment
ir = initial_returns(pd.Series([10.0, 5.0, 0.0]), pd.Series([12.0, 4.0, 3.0]),
                     pd.Series([100.0, 100.0, 100.0]), pd.Series([110.0, 100.0, 100.0]))
check(abs(ir.loc[0, "ir"] - 0.2) < 1e-12, "IR = P1/P0 - 1")
check(abs(ir.loc[0, "mair"] - (1.2 / 1.1 - 1)) < 1e-12, "MAIR ratio form")
check(abs(ir.loc[0, "mair_diff"] - 0.1) < 1e-12, "MAIR difference form")
check(np.isnan(ir.loc[2, "ir"]), "non-positive offer price -> NaN")

# price revision, fixed-price offers
pr = price_revision(pd.Series([3.0, 2.0, 1.8]), pd.Series([2.0, 2.0, 2.0]),
                    pd.Series([3.0, 2.0, 3.0]))
check(abs(pr.loc[0, "range_pos"] - 1.0) < 1e-12, "range position top = 1")
check(np.isnan(pr.loc[1, "range_pos"]) and bool(pr.loc[1, "is_fixed_price"]),
      "fixed-price offer has no range position")
check(pr.loc[2, "range_pos"] < 0 and bool(pr.loc[2, "below_range"]),
      "downward-adjusted price below range")
check(abs(money_left_on_table(pd.Series([10.0]), pd.Series([12.0]),
                              pd.Series([1e6]))[0] - 2e6) < 1e-6, "money left on table")

# BHAR
rows = []
for i in range(3):
    for t in range(1, 13):
        r = 0.01
        if i == 1 and t > 6:
            r = np.nan  # delisted after month 6
        rows.append({"ipo_id": i, "event_t": t, "ret": r if i != 2 else 0.0,
                     "bench_ret": 0.01})
bh = bhar_panel(pd.DataFrame(rows), horizon=12)
check(abs(bh.loc[0, "bhar"]) < 1e-12, "firm == benchmark -> BHAR 0")
check(abs(bh.loc[1, "bhar"]) < 1e-12 and not bh.loc[1, "complete"],
      "delisted firm earns benchmark afterwards")
check(abs(bh.loc[2, "bhar"] - (1 - 1.01 ** 12)) < 1e-12, "BHAR arithmetic")
bt = bhar_panel(pd.DataFrame(rows), horizon=12, after_delisting="truncate")
check(abs(bt.loc[1, "bench_bhr"] - (1.01 ** 6 - 1)) < 1e-12, "truncate compounds matched months")
check(abs(wealth_relative(bh["bhr"], bh["bench_bhr"]) - (1 + bh["bhr"].mean()) /
          (1 + bh["bench_bhr"].mean())) < 1e-12, "wealth relative")

# skewness-adjusted t
sym = rng.normal(0.02, 0.1, 400)
t_ord = sym.mean() / sym.std(ddof=1) * np.sqrt(sym.size)
check(abs(skew_adjusted_t(sym) - t_ord) < 0.15, "t_sa ~ ordinary t for symmetric data")
skewed = rng.lognormal(0, 1, 300) - np.exp(0.5)  # mean zero, right skewed
res = bootstrap_skew_adjusted_test(skewed, reps=500)
check(np.isfinite(res["t_sa"]) and 0 <= res["p_boot"] <= 1, "bootstrap skew-adjusted test runs")

# calendar-time portfolio: true alpha 0.01 per month
months = pd.period_range("2015-01", "2024-12", freq="M")
fac = pd.DataFrame({"mkt_rf": rng.normal(0.005, 0.04, len(months)), "rf": 0.001}, index=months)
recs = []
for i in range(300):
    lm = months[rng.integers(0, len(months) - 40)]
    for k in range(1, 37):
        m = lm + k
        if m > months[-1]:
            break
        recs.append({"ipo_id": i, "month": m, "listing_month": lm,
                     "ret": 0.001 + 0.01 + 1.2 * fac.loc[m, "mkt_rf"] + rng.normal(0, 0.08),
                     "me_lag": rng.lognormal(20, 1)})
ct = calendar_time_portfolio(pd.DataFrame(recs), fac, factor_cols=["mkt_rf"])
check(abs(ct["alpha"] - 0.01) < 0.004, f"calendar-time alpha recovered ({ct['alpha']:.4f})")
ctv = calendar_time_portfolio(pd.DataFrame(recs), fac, weight="vw", factor_cols=["mkt_rf"])
check(np.isfinite(ctv["alpha"]), "value-weighted calendar-time alpha runs")

# regression table from statsmodels
import statsmodels.formula.api as smf  # noqa: E402

n = 150
df = pd.DataFrame({"cs": rng.uniform(0, 0.6, n), "lnp": rng.normal(20, 1, n),
                   "month": rng.integers(1, 13, n), "ind": rng.integers(0, 8, n)})
df["log_ir"] = 0.3 * df.cs - 0.05 * df.lnp + rng.normal(0, 0.2, n) + 1
m1 = smf.ols("log_ir ~ cs + lnp", df).fit(cov_type="HC3")
m2 = smf.ols("log_ir ~ cs + lnp + C(ind)", df).fit(cov_type="cluster",
                                                   cov_kwds={"groups": df["month"]})
tex = regression_table([m1, m2], labels={"cs": "Cornerstone share", "lnp": "Ln(proceeds)"},
                       keep=["cs", "lnp"], depvar="Log initial return",
                       extra_rows={"Industry FE": ["No", "Yes"],
                                   "SE": ["HC3", "Cluster (month)"]},
                       notes=r"$^{*}p<0.10$, $^{**}p<0.05$, $^{***}p<0.01$.")
check(r"\toprule" in tex and "Cornerstone share" in tex and "C(ind)" not in tex,
      "booktabs table built and filtered")

try:
    from linearmodels.iv import IV2SLS
    df["z"] = df.cs + rng.normal(0, 0.1, n)
    iv = IV2SLS.from_formula("log_ir ~ 1 + lnp + [cs ~ z]", df).fit(cov_type="robust")
    tex_iv = regression_table([iv], keep=["cs"])
    check("cs" in tex_iv, "linearmodels result accepted")
except ImportError:
    print("SKIP linearmodels not installed")

try:
    import pyfixest as pf
    fit = pf.feols("log_ir ~ cs + lnp | ind", data=df, vcov={"CRV1": "month"})
    wb = fit.wildboottest(param="cs", reps=999, seed=1)
    check(0 <= float(wb["Pr(>|t|)"]) <= 1, "pyfixest feols + wild cluster bootstrap")
    check(r"\toprule" in pf.etable([fit], type="tex"), "pyfixest etable tex")
except ImportError:
    print("SKIP pyfixest not installed")

if "--latex" in sys.argv and shutil.which("pdflatex"):
    doc = ("\\documentclass{article}\\usepackage{booktabs}\\begin{document}\n"
           + tex + "\n\\end{document}\n")
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "t.tex"), "w") as f:
            f.write(doc)
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "t.tex"], cwd=d,
                           capture_output=True, text=True)
        check(r.returncode == 0, "table compiles with pdflatex")

print("All checks passed.")
