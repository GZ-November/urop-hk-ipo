---
name: ipo-empirical-research
description: Design, run and report journal-standard empirical research on IPOs in Python (pandas, statsmodels, pyfixest, linearmodels), with deep Hong Kong / HKEX coverage. Use whenever the user asks about IPO underpricing or initial returns (首日抑价/首日收益), market-adjusted returns, price revision and partial adjustment, oversubscription and clawback (超额认购/回拨), cornerstone investors (基石投资者), grey market (暗盘), margin financing (孖展), sponsor/underwriter or VC effects, lockups, stabilization/greenshoe, long-run performance (BHAR, CAR, calendar-time alpha, wealth relatives), prospectus/allotment data (招股书/配发结果) turned into regression variables, IPO regression design (fixed effects, clustering, wild bootstrap, IV/2SLS, Heckman, matching, RD/DiD around HKEX rule changes), or LaTeX booktabs regression tables for an IPO paper — even if they do not say "empirical" or "skill".
---

# IPO Empirical Research (Python)

Produce IPO research that a referee at JF/JFE/RFS (or a thesis examiner) would
accept: correct variable timing, a defensible identification argument, honest
inference for small samples, and reproducible Python code. Hong Kong specifics
are first-class because institutional details (clawback, cornerstones, grey
market, the 2025 reform) change what a variable means.

## How to use this skill

1. Read the task and decide which parts apply: design, variable construction,
   estimation, long-run performance, reporting. Load only the matching
   reference file(s):

| Task | Read |
|---|---|
| Building variables from prospectus/allotment/price data; timing questions | `references/variable_definitions.md` |
| Regression design, FE, standard errors, IV/Heckman/matching/RD/DiD, robustness | `references/econometrics_inference.md` |
| BHAR, CAR, calendar-time portfolios, lockup-expiry windows | `references/long_run_performance.md` |
| Anything about Hong Kong rules, regime dates, data sources, HK designs | `references/hong_kong_institutions.md` |
| Motivating a hypothesis; choosing proxies that separate theories | `references/theory_to_tests.md` |
| Tables, LaTeX, figures, replication package | `references/reporting_and_replication.md` |

2. Reuse the tested code in `scripts/` rather than rewriting formulas:
   - `ipo_metrics.py`: NaN-safe `winsorize`, `initial_returns` (IR, log IR,
     MAIR), `price_revision`, `money_left_on_table`, `bhar_panel`,
     `skew_adjusted_t`, `bootstrap_skew_adjusted_test`, `wealth_relative`,
     `calendar_time_portfolio`.
   - `regtable.py`: booktabs LaTeX tables for statsmodels/linearmodels results.
   - `selftest.py`: run it once in a new environment to confirm the helpers and
     installed package versions behave as documented.
   Copy the files next to the user's analysis code (or add the folder to
   `sys.path`) and cite them in comments.

3. If working inside a repository that already has a research plan, variable
   registry or analysis scripts (for example the UROP HK IPO repo with
   `docs/RESEARCH_PLAN_2026.md` and the `hk-ipo-pipeline` skill), the
   repository's definitions and sample rules take precedence. Use this skill's
   standards to review or extend them, and flag disagreements rather than
   silently changing a study's specification.

4. For literature depth (theory derivations, US SDC/CRSP sample filters,
   governance), the `lowry-ipo-research` skill complements this one.

## Standards that matter most (and why)

**Timing defines meaning.** Classify each variable by when it becomes known:
prospectus (range, cornerstones, offer size), pricing (P0), allotment
(oversubscription, clawback), listing (P1). Post-pricing information cannot
explain how P0 was set. Final retail oversubscription is jointly determined
with the initial return because demand responds to expected underpricing;
present it as an outcome/mediator, or use a pre-pricing proxy (margin
financing) or an instrument, and say so explicitly.

**Initial return.** IR = P1/P0 − 1 (first-day close; Ritter). Use log IR as
the regression LHS when the distribution is right-skewed and report raw IR.
Market-adjust over the window investors actually bear: index close on the
pricing date to index close on the first trading day, MAIR = (1+IR)/(1+Rm) − 1
(or IR − Rm). A listing-day-only index return is the wrong window.

**Price revision.** (P0 − P_mid)/P_mid and range position
(P0 − P_low)/(P_high − P_low). Fixed-price offers have no range position:
leave it missing and add an indicator. HK offers may price up to 10% below the
range.

**Missing is not zero.** Unknown VC backing, undisclosed placing demand and
immature return horizons stay missing. Report N per variable and per horizon.
Blanket `fillna(0)` silently creates false negatives.

**Winsorize safely.** 1/99 two-sided on continuous regressors with
`ipo_metrics.winsorize`. Do not use `scipy.stats.mstats.winsorize` on data with
NaN: NaN sorts as the maximum, so the upper tail that gets clipped is the NaNs
and genuine outliers survive. Prefer transforming the LHS (log IR) over
winsorizing it, and show winsorized/raw/median-regression robustness. Never
winsorize binaries or bounded shares.

**It is a cross-section.** One row per IPO. Use `pyfixest.feols` or
`statsmodels` with absorbed industry and listing-period effects, not a panel
estimator indexed by (industry, year). Keep FE coarse in small samples (sectors
not sub-industries; quarter rather than month when N is under ~150), and show
the progression no FE → industry → industry + period.

**Inference for small samples.** Default HC3 for a plain cross-section.
Cluster by listing month when IPOs listed together share shocks; report the
number of clusters G. When G is below ~40–50 or cluster sizes are unequal,
report wild cluster restricted bootstrap p-values (`fit.wildboottest(...)`,
Webb weights when G < ~12) and/or CV3. Two-way clustering only when both
dimensions have many clusters. Stars must match the inference you rely on.

**One estimation sample.** Nested columns use the same complete-case sample,
fixed on the largest specification. Log each sample restriction with counts.

**Identification before significance.** Cornerstone participation, sponsor
quality, VC backing, listing route and timing are choices. Name the selection
channel and pick a design: IV with an economic exclusion argument and weak-IV
robust inference (effective F, Anderson–Rubin), selection/switching models,
entropy balancing with balance tables, Oster (2019) bounds, or rule-based
variation (clawback thresholds, the Aug-2025 HKEX reform, FINI). If none is
credible, call results associations and say what would change the conclusion.

**Long run.** Report BHAR (matched firm or buy-and-hold reference portfolio,
skewness-adjusted and bootstrapped t, median and % positive, wealth relative)
*and* calendar-time portfolio alpha (EW and VW). Start aftermarket returns after
the first-day close. Handle delisting and trading suspensions explicitly; count
immature horizons out, not in.

**Few observations, many variables.** Keep regressors well below N/10,
pre-specify the main model, report every specification tried, and correct
families of tests (Romano–Wolf via `pf.rwolf`, or Holm).

## Hong Kong essentials (details in the reference)

- Regime breaks: FINI settlement (22 Nov 2023, pricing-to-trading T+5 → T+2);
  HKEX price-discovery reform effective for listing documents published on or
  after 4 Aug 2025 (≥ 40% bookbuilding placing tranche; public tranche under
  Mechanism A: 5% → 15/25/35% at 15×/50×/100×, or Mechanism B: ≥ 10%, no
  clawback; tiered public float; cornerstone 6-month lockup retained). Before
  it, PN18: 10% → 30/40/50% at 15×/50×/100×. Split or control by prospectus
  date. 18C issuers are exempt from Mechanism A/B.
- Code the actual mechanism and allocation from each prospectus and allotment
  announcement: waivers are common for large deals.
- Useful HK-only variables: grey-market return, margin-financing multiple,
  placee concentration, cornerstone and SOE-cornerstone shares, A-share
  reference price for A+H issuers.

Rules evolve: when a design depends on a threshold or date, verify it against
the current HKEX Listing Rules / Guide for New Listing Applicants and cite it.

## Response template

When delivering a research design, analysis or code, structure the answer as
follows (skip sections that the request clearly does not need; keep each tight):

1. **Question and mechanism.** The economic channel (e.g. information
   asymmetry, certification, bookbuilding information revelation, sentiment),
   the competing explanation, and the predicted signs.
2. **Sample and data.** Population, filters with counts, data sources, time
   stamps of each variable relative to pricing.
3. **Specification.** The estimating equation in LaTeX, e.g.
   $\ln(1+IR_i)=\alpha+\beta\,CS_i+X_i'\gamma+\delta_{ind(i)}+\tau_{m(i)}+\varepsilon_i$,
   with every symbol defined and the coefficient of interest's interpretation.
4. **Identification and threats.** Selection, reverse causality, mechanical
   links, omitted quality; the design used against each; what remains.
5. **Inference.** SE type and why, number of clusters, bootstrap details.
6. **Python code.** Modular, commented, runnable; uses `scripts/` helpers;
   fixes one estimation sample; sets seeds; prints N and G.
7. **Tables.** Booktabs LaTeX (via `pf.etable(type="tex")` or
   `regtable.regression_table`) with FE rows, SE note, N and clusters.
8. **Robustness and next steps.** Ranked by which threat they address.

Write numbers only from actual output. If data are not available in the
session, show the code and a table shell with placeholders clearly marked as
placeholders; never invent estimates, p-values or sample sizes.

Match the user's language (Chinese or English) in prose; keep variable names and
code in English.
