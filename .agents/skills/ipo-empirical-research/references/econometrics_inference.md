# Estimation, identification and inference for IPO cross-sections

## Contents
1. Data structure: IPOs are a cross-section
2. Tool choice in Python
3. Fixed effects: what they absorb and what they cost
4. Standard errors decision table
5. Endogeneity toolkit
6. Robustness menu
7. Multiple testing and specification search
8. Code patterns

---

## 1. Data structure

A sample of IPOs is one observation per issuer: a cross-section, with listing
dates spread over time. It is not a panel. Industry and listing-period effects
enter as dummies (fixed effects) in a cross-sectional regression; clustering
accounts for shocks shared by IPOs listed in the same month or industry.
Forcing the data into `PanelOLS` with an (industry, year) index works
mechanically but mislabels the design, makes "entity" mean industry, and
obscures which dimension the clustering uses. Use a cross-sectional estimator
with explicit absorbed effects instead.

Post-IPO *firm-year* data (e.g. profitability after listing, governance
changes) are panels: there firm FE and firm clustering are standard.

## 2. Tool choice in Python

| Need | Package | Notes |
|---|---|---|
| OLS with absorbed FE, CRV1/CRV3, two-way clustering, wild cluster bootstrap, Romano–Wolf, LaTeX tables | `pyfixest` (fixest syntax) | `pf.feols("y ~ x | ind + month", data, vcov={"CRV1": "month"})`; `.wildboottest(param=, reps=, seed=)`; `pf.etable(..., type="tex")`; `pf.rwolf`. Tested with 0.60. |
| HC3, quantile regression, Heckman-by-hand, probit/logit | `statsmodels` | `smf.ols(...).fit(cov_type="HC3")`; `smf.quantreg`. |
| IV/2SLS/LIML/GMM with first-stage diagnostics | `linearmodels.iv` | `IV2SLS.from_formula("y ~ 1 + w + [x ~ z]", df)`; `.first_stage`, `.wu_hausman()`, `.sargan`. |
| Firm-year panels | `linearmodels.panel.PanelOLS` or `pyfixest` | Index (firm, year). |
| Matching / weighting | `scikit-learn` for propensity; entropy balancing by hand or `ebal` ports | Report balance tables. |

Pin versions in `requirements.txt` / lock file and record them in the paper's
replication notes; defaults (small-sample corrections, dof) change across releases.

## 3. Fixed effects

- **Listing-period FE** (year, quarter or month) absorb hot/cold market
  conditions (Ritter 1984; Lowry & Schwert 2002). In a single-year study, month
  FE with ~12 levels and ~80 IPOs consume a lot of degrees of freedom and can
  absorb the variation of interest (e.g. a regulatory change). Alternatives:
  quarter FE, or continuous market controls (index return and volatility over
  the bookbuilding window, number of IPOs in the prior 30 days).
- **Industry FE** absorb sector valuation levels. Use a coarse classification
  (e.g. ~10–12 Hang Seng Industry Classification sectors, or Fama–French 12)
  rather than fine codes that create singletons. Report how many singletons
  were dropped (`pyfixest` drops them by default; `fixef_rm="singleton"`).
- Absorb only what the question needs. Show a sequence: no FE → industry FE →
  industry + period FE, so readers see coefficient stability.
- A regressor that does not vary within FE cells (e.g. a reform dummy with
  month FE) is not identified. Check for collinearity drops in the output.

## 4. Standard errors

| Situation | Default | Also report |
|---|---|---|
| Cross-section, small N (< ~250), no obvious grouping | HC3 (Long & Ervin 2000) | HC1 |
| Shocks shared by listing month / week | Cluster by listing month (CRV1) | Wild cluster restricted bootstrap p-values if G < ~40–50 |
| Few clusters (G < ~40), or very unequal cluster sizes | Wild cluster restricted (WCR) bootstrap, Rademacher weights; Webb 6-point weights if G < ~12; CV3 (jackknife) SEs | Number of clusters G and largest cluster share |
| Two plausible dimensions (industry and month) | Two-way clustering only when both have many clusters (Petersen 2009; Cameron, Gelbach & Miller 2011) | One-way results for each dimension |
| BHAR on a constant | Cluster by listing month or use calendar-time portfolios | t_sa, bootstrap |

Rules behind the table: clustered SEs rely on G → ∞; with few or unbalanced
clusters they over-reject, sometimes severely (Cameron & Miller 2015;
MacKinnon, Nielsen & Webb 2023). Always state G. The Python wild bootstrap
(`pyfixest` via `wildboottest`) imposes the null by default (`impose_null=True`),
which is the recommended WCR variant. With fewer than ~12 clusters, Rademacher
weights yield only 2^G distinct draws; use Webb weights
(`weights_type="webb"`) and report that inference is fragile.

## 5. Endogeneity toolkit

Typical endogenous choices in IPO research: underwriter/sponsor quality, VC/PE
backing, cornerstone participation and size, listing route, offer timing,
price-range setting, and retail demand. Design options:

**Instrumental variables.** Must be relevant and excludable, and the exclusion
restriction needs an economic argument, not only a statistical test. Examples
from the literature and their risks:
- Leave-one-out supply measures (e.g. cornerstone commitments by the same
  investor group or bookrunner in prior months, excluding the focal IPO). Risk:
  common market conditions affect both supply and underpricing; control for
  period effects.
- Geographic or network proximity (e.g. VC–issuer distance). Risk: proximity
  correlates with firm quality.
- Rule-induced variation (tranche thresholds, eligibility cutoffs).
Diagnostics: report the first stage; use the effective F of Montiel Olea &
Pflueger (2013) rather than the Stock–Yogo rule of thumb when errors are
heteroskedastic/clustered; report Anderson–Rubin confidence intervals, which are
robust to weak instruments. Lee, McCrary, Moreira & Porter (2022) show a
conventional 5% t-test needs F > 104.7 to have correct size, or use their tF
adjustment. Over-identification tests (Sargan/Hansen) cannot validate
exclusion when all instruments share one flaw.

**Selection models.** Heckman (1979) two-step for outcomes observed only for
completed IPOs (withdrawals) or for the self-selected choice of a route;
requires an exclusion variable in the selection equation, otherwise
identification rests on functional form. Endogenous switching regressions
(Fang 2005 for underwriter reputation) estimate counterfactual outcomes for
both choices.

**Matching and weighting.** Propensity score matching or entropy balancing
(Hainmueller 2012) for binary treatments (cornerstone presence, VC backing).
They address only selection on observables: say so. Report standardized mean
differences before and after (< 0.1 is the common threshold). King & Nielsen
(2019) caution against PSM specifically; prefer entropy balancing, coarsened
exact matching or regression adjustment with overlap checks.

**Coefficient stability.** Oster (2019) δ: how strong selection on
unobservables must be, relative to observables, to explain away the effect.
Cheap and informative when no instrument exists.

**Regulatory events.** Rule changes create natural experiments, but a
single-date reform confounds with contemporaneous market conditions.
- Before/after (interrupted time series / regression discontinuity in time):
  control for market returns, volatility, IPO volume; use narrow windows; run
  placebo dates.
- Difference-in-differences needs an unaffected comparison group (e.g. an
  exempt listing route, or a comparable exchange). Show pre-trends. With a
  single treated period and few clusters, use wild bootstrap or randomization
  inference.
- Threshold rules (e.g. clawback triggers at fixed oversubscription multiples)
  invite regression discontinuity/bunching designs. Test for manipulation of the
  running variable (McCrary 2008; Cattaneo, Jansson & Ma 2020 `rddensity`)
  and remember that retail demand is chosen *knowing* the thresholds.

## 6. Robustness menu

Choose the ones that address a specific threat and say which threat:
- Alternative LHS: raw IR, log IR, MAIR, winsorized IR, open-to-close.
- Median/quantile regression (τ = 0.25, 0.5, 0.75): heavy right tail.
- Drop the most influential observations (top IRs, Cook's distance) and report.
- Alternative samples: exclude 18A/18C, A+H, WVR, secondary listings;
  sub-periods (pre/post FINI, pre/post Aug-2025 reform).
- Alternative definitions of key regressors (cornerstone share vs presence;
  reputation over 1 vs 3 prior years).
- Placebo outcomes/dates; randomization inference for event dummies.
- Pairs (case) bootstrap for small-sample CIs; count failed/singular draws.

## 7. Multiple testing and specification search

IPO datasets have hundreds of candidate variables and few observations. Pre-
specify the main specification and hypotheses (write them down before looking
at results), keep the regressor count well below N/10, and report the full set
of specifications tried. For families of hypotheses use Romano–Wolf stepdown
p-values (`pf.rwolf`) or Bonferroni/Holm; Harvey, Liu & Zhu (2016) argue new
return predictors need t > 3.0. Label exploratory results as exploratory.

## 8. Code patterns

```python
import numpy as np
import pandas as pd
import pyfixest as pf
import statsmodels.formula.api as smf
from linearmodels.iv import IV2SLS

from ipo_metrics import winsorize   # NaN-safe, see scripts/

df = df.copy()
for c in ["ln_proceeds", "ln_age", "leverage", "range_width"]:
    df[c] = winsorize(df[c], 0.01, 0.01)

# Fix one estimation sample for all nested models (complete cases on the
# largest specification) so coefficients are comparable across columns.
cols = ["log_ir", "cornerstone_pct", "ln_proceeds", "ln_age", "leverage",
        "range_width", "mkt_ret_bookbuild", "ind", "list_month"]
est = df.dropna(subset=cols)

m1 = pf.feols("log_ir ~ cornerstone_pct + ln_proceeds + ln_age + leverage",
              data=est, vcov="HC3")
m2 = pf.feols("log_ir ~ cornerstone_pct + ln_proceeds + ln_age + leverage"
              " + range_width + mkt_ret_bookbuild | ind",
              data=est, vcov={"CRV1": "list_month"})
m3 = pf.feols("log_ir ~ cornerstone_pct + ln_proceeds + ln_age + leverage"
              " + range_width | ind + list_month",
              data=est, vcov={"CRV1": "list_month"})
wcr = m2.wildboottest(param="cornerstone_pct", reps=9999, seed=2026)

# Quantile regression for the heavy right tail
q50 = smf.quantreg("log_ir ~ cornerstone_pct + ln_proceeds + ln_age + leverage",
                   est).fit(q=0.5)

# IV with diagnostics (instrument must be argued economically)
iv = IV2SLS.from_formula("log_ir ~ 1 + ln_proceeds + ln_age + leverage"
                         " + [cornerstone_pct ~ cs_supply_loo]", est
                         ).fit(cov_type="clustered", clusters=est["list_month"])
print(iv.first_stage)

tex = pf.etable([m1, m2, m3], type="tex",
                labels={"log_ir": "Log initial return",
                        "cornerstone_pct": "Cornerstone share"},
                felabels={"ind": "Industry FE", "list_month": "Listing-month FE"},
                notes="Standard errors in parentheses.")
```

Pitfalls this pattern avoids: `scipy.stats.mstats.winsorize` on data with NaN
(NaN sorts as the maximum, so real outliers survive); nested models on
different samples; clustering on a dimension with a handful of groups without
bootstrap; reporting stars from conventional p-values while the text relies on
bootstrap inference.
