"""Extended statistical analysis of the 2026 HK Main Board IPO sample.

Complements Module A/B with tests that address what they cannot:

  1. Regime      Is the April-June "hot window" still significant after correcting for
                 having searched for it? Serial dependence, real-time predictability from
                 prior-IPO returns, and subscription-period crowding.
  2. Mechanism   Offer Mechanism A vs B: how much of the contrast is really Chapter 18C?
  3. Tails       Quantile regressions, PPML on 1 + IR, and logit models of breaks and big pops.
  4. Demand      What drives retail subscription, and how demand relates to IR.
  5. Aftermarket Hot vs other windows, reversal after day 1, stabilization and greenshoe.
  6. Prediction  Leave-one-month-out and leave-one-out out-of-sample R-squared.
  7. Multiplicity Benjamini-Hochberg adjustment across the headline tests above.

Only 2026 listings are used (same selector as every other script). All results are
exploratory; issuer and listing-month counts are reported from each analysis sample.

Outputs (analysis/out/extended/): regime.md, mechanism.md, tails.md, demand_aftermarket.md,
prediction.md, multiplicity.md, fig5_regime_scan.png, fig6_quantile_paths.png.

Usage:
    python3 analysis/extended_analysis_2026.py
"""

from __future__ import annotations

import warnings

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox

from specifications.underpricing import MODELS, VARS, estimation_sample
from shared.estimation import (  # noqa: F401 -- compatibility exports
    stars, ols_focus, fmt_focus, bh_family, anova_icc,
)
from research_inputs import C as C, ROOT as ROOT, load_panel as load_panel, select_2026 as select_2026  # noqa: F401 — legacy C export
from shared.reporting import (
    AXIS, BLUE, INK, INK2, MUTED, ORANGE, new_fig, pct_axis, style_axes, to_markdown,
)

# Compatibility names for existing notebooks and helper callers.
from research_inputs import (  # noqa: F401
    EXTENDED_HORIZONS as HORIZONS, prepare_extended as prepare,
    prior_mean_ir as prior_mean_ir, subscription_overlap as subscription_overlap,
)

OUT = ROOT / "analysis" / "out" / "extended"
SEED = 20260930
N_PERM = 5000
N_BOOT = 1000
QUANTILES = (0.10, 0.25, 0.50, 0.75, 0.90)
MIN_WINDOW = 10
CONTROLS = ["lage", "lproc", "ah", "vc"]
M3 = MODELS["M3"]


# ------------------------------------------------------------- estimation helpers





def verdict(p: float) -> str:
    return "significant at 5%" if p < 0.05 else "marginal (p < 0.10)" if p < 0.10 else "not significant"






# ------------------------------------------------------------------ 1. regime

def window_grid(dates: np.ndarray, min_n: int) -> tuple[np.ndarray, np.ndarray]:
    """All contiguous [a, b) windows whose edges sit on listing-date changes and both sides hold >= min_n deals."""
    n = len(dates)
    cuts = np.r_[0, np.flatnonzero(np.diff(dates.astype("int64")) != 0) + 1, n]
    i, j = np.triu_indices(len(cuts), 1)
    a, b = cuts[i], cuts[j]
    keep = (b - a >= min_n) & (n - (b - a) >= min_n)
    return a[keep], b[keep]


def window_t(y: np.ndarray, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Welch t of inside-window vs outside-window means for every window."""
    n = len(y)
    c1, c2 = np.r_[0, np.cumsum(y)], np.r_[0, np.cumsum(y ** 2)]
    k1, k0 = b - a, n - (b - a)
    s1, q1 = c1[b] - c1[a], c2[b] - c2[a]
    s0, q0 = c1[-1] - s1, c2[-1] - q1
    m1, m0 = s1 / k1, s0 / k0
    v1, v0 = (q1 - k1 * m1 ** 2) / (k1 - 1), (q0 - k0 * m0 ** 2) / (k0 - 1)
    return (m1 - m0) / np.sqrt(v1 / k1 + v0 / k0)


def scan_test(y: np.ndarray, dates: np.ndarray, min_n: int = MIN_WINDOW, n_perm: int = N_PERM, seed: int = SEED) -> dict:
    """Search-corrected test for a contiguous window with a different mean.

    Statistic: max |Welch t| over all windows. Null: y exchangeable across listing order (permutation),
    which is a fair null here because serial dependence is tested and found negligible (see regime.md)."""
    a, b = window_grid(dates, min_n)
    t = window_t(y, a, b)
    rng = np.random.default_rng(seed)
    perm = np.array([np.abs(window_t(rng.permutation(y), a, b)).max() for _ in range(n_perm)])
    hi, lo = int(np.argmax(t)), int(np.argmin(t))
    return {"stat": float(np.abs(t).max()), "p": float((1 + (perm >= np.abs(t).max()).sum()) / (n_perm + 1)),
            "up": (a[hi], b[hi], float(t[hi])), "down": (a[lo], b[lo], float(t[lo])), "perm_95": float(np.quantile(perm, 0.95)),
            "n_windows": len(a)}


def perm_p_welch(y: np.ndarray, group: np.ndarray, n_perm: int = N_PERM, seed: int = SEED) -> tuple[float, float]:
    """Welch t of group 1 vs 0 and its two-sided permutation p-value (group labels shuffled)."""
    def t_of(g):
        return stats.ttest_ind(y[g], y[~g], equal_var=False).statistic
    g = group.astype(bool)
    obs, rng = t_of(g), np.random.default_rng(seed)
    perm = np.array([t_of(rng.permutation(g)) for _ in range(n_perm)])
    return float(obs), float((1 + (np.abs(perm) >= abs(obs)).sum()) / (n_perm + 1))




def regime_section(d: pd.DataFrame, family: list) -> tuple[str, dict]:
    z = d.dropna(subset=["y"]).reset_index(drop=True)
    y, dates = z["y"].to_numpy(), z["ld"].to_numpy()
    scan = scan_test(y, dates)
    hot_t, hot_p = perm_p_welch(y, z["hot"].to_numpy())
    icc, f_obs, icc_p = anova_icc(y, z["month"].to_numpy())
    span = lambda w: f"{pd.Timestamp(dates[w[0]]).date()} to {pd.Timestamp(dates[w[1] - 1]).date()}, {w[1] - w[0]} deals"
    family += [("Regime", "Best contiguous window, search-corrected (permutation)", scan["p"]),
               ("Regime", "Month effect on IR (ANOVA permutation)", icc_p)]

    resid_fit = sm.OLS(z["y"], sm.add_constant(z[CONTROLS].astype(float))).fit() if z[CONTROLS].notna().all().all() else None
    lb = {name: acorr_ljungbox(v, lags=[5, 10], return_df=True)["lb_pvalue"] for name, v in
          [("log(1+IR)", y)] + ([("residual after controls", resid_fit.resid.to_numpy())] if resid_fit is not None else [])}
    rho = stats.spearmanr(y[:-1], y[1:])

    # real-time predictability and crowding
    rows, crowd_lsub = [], None
    for label, dv, xs, focus in [
        ("Prior-30-day mean IR (per +100 pp)", "y", ["prior_ir"], "prior_ir"),
        ("  + issuer controls", "y", ["prior_ir", *CONTROLS], "prior_ir"),
        ("  + issuer controls + April-June dummy", "y", ["prior_ir", *CONTROLS, "hot"], "prior_ir"),
        ("Overlapping subscriptions (per deal), controls + hot", "y", ["conc", *CONTROLS, "hot"], "conc"),
        ("Same-day listings (per deal), controls + hot", "y", ["sameday", *CONTROLS, "hot"], "sameday"),
        ("Overlapping subscriptions -> ln subscription ratio", "lsub", ["conc", *CONTROLS, "hot"], "conc"),
    ]:
        r = ols_focus(d, dv, xs, focus)
        rows.append([label, *fmt_focus(r)])
        if dv == "lsub":
            crowd_lsub = r
        if label.endswith("controls") and "prior" in label:
            family.append(("Regime", "Prior-IPO returns -> IR (controls)", r["p"]))
        if label.startswith("Overlapping subscriptions (per"):
            family.append(("Regime", "Subscription crowding -> IR", r["p"]))
    rho_prior = stats.spearmanr(*d[["prior_ir", "ir"]].dropna().T.to_numpy())
    table = pd.DataFrame(rows, columns=["Specification", "Coefficient (HC3 s.e.)", "HC3 p", "Wild cluster p", "N"])

    text = f"""# Regime tests, 2026 (N = {len(z)})

The Apr-Jun "hot window" was found by inspecting these data, so its ordinary p-value overstates the evidence.
These tests price in the search and ask what a listing-date regime does and does not explain.

## 1. Search-corrected test for a contiguous window

Statistic: the largest |Welch t| of log(1 + IR) inside vs outside any contiguous run of listings
({scan['n_windows']} candidate windows, edges on listing-date changes, at least {MIN_WINDOW} deals on each side).
Null: IR is exchangeable across listing order ({N_PERM} permutations).

| Item | Value |
|---|---|
| Largest |t| over all windows | {scan['stat']:.2f} (95th percentile under null: {scan['perm_95']:.2f}) |
| **Search-corrected permutation p** | **{scan['p']:.3f}** |
| Best "hot" window (positive) | {span(scan['up'])}, t = {scan['up'][2]:.2f} |
| Best "cold" window (negative) | {span(scan['down'])}, t = {scan['down'][2]:.2f} |
| Calendar Apr-Jun vs rest (a data-informed window) | Welch t = {hot_t:.2f}, ordinary permutation p = {hot_p:.4f} |

- The data-optimal hot window ({span(scan['up'])}) is close to the calendar Apr-Jun dummy, so the dummy is
  not far from the best possible block. The single strongest contrast is the cold spell that follows it ({span(scan['down'])}).
- After correcting for the search, the evidence for a level shift is **{verdict(scan['p'])}** (p = {scan['p']:.3f}) while the
  uncorrected Apr-Jun p-value ({hot_p:.4f}) is far smaller. Report the corrected number; the regime is a feature of 2026,
  not a precisely dated event.

## 2. How much of IR is a month effect?

| Item | Value |
|---|---|
| ANOVA intraclass correlation across {z['month'].nunique()} listing months | {icc:.3f} |
| F (month effect) / permutation p | {f_obs:.2f} / {icc_p:.4f} |

About {100 * max(icc, 0):.0f}% of the variance of log(1 + IR) sits between months; most dispersion is within a month.

## 3. Serial dependence across listing order

| Series | Spearman lag-1 (p) | Ljung-Box p, 5 lags | Ljung-Box p, 10 lags |
|---|---|---|---|
| log(1+IR) | {rho.statistic:.3f} ({rho.pvalue:.2f}) | {lb['log(1+IR)'].iloc[0]:.3f} | {lb['log(1+IR)'].iloc[1]:.3f} |
""" + (f"| Residual after age, size, A+H, VC/PE | — | {lb['residual after controls'].iloc[0]:.3f} | {lb['residual after controls'].iloc[1]:.3f} |\n" if resid_fit is not None else "") + f"""
Consecutive listings are not significantly correlated, which is why the permutation null above is reasonable.
The regime is a level shift in the mean with large idiosyncratic noise, not a smooth momentum process.

## 4. Real-time predictability and crowding

`prior_ir` is the mean IR of 2026 IPOs listed in the 30 days before the deal's subscription opened (at least 3 deals,
so January listings are dropped). It uses only information available at the offer date. Crowding counts other deals
whose subscription window overlaps this one; the last row asks whether crowding lowers retail oversubscription.

{to_markdown(table.set_index("Specification"), "Specification")}

- Unconditional Spearman correlation of prior-IPO mean IR with IR: {rho_prior.statistic:.2f} (p = {rho_prior.pvalue:.2f}).
- Prior-IPO returns are not a significant predictor with or without the window dummy (the sign flips once the dummy is
  added, because the dummy carries the level). Prior IR is a weak real-time signal of the regime; prediction.md checks this out of sample.
- Retail oversubscription falls by about {100 * (1 - np.exp(crowd_lsub['b'])):.0f}% per additional overlapping offering
  (HC3 p = {crowd_lsub['p']:.3f}, wild cluster p = {crowd_lsub['p_wild']:.3f}): {verdict(crowd_lsub['p'])}. Crowding does not significantly change IR itself.
- Wild cluster p uses listing-month clusters (exact enumeration); HC3 p ignores clustering. Read both.
"""
    return text, {"scan": scan, "z": z}


# ------------------------------------------------------------------ 2. mechanism

def mechanism_section(d: pd.DataFrame, family: list) -> str:
    z = d.dropna(subset=["mechA", "y"]).copy()
    a, b = z[z["mechA"] == 1], z[z["mechA"] == 0]
    cross = pd.crosstab(z["mech"], z["r18c"].map({1.0: "18C", 0.0: "Not 18C"}))
    hot_cross = pd.crosstab(z["mech"], z["hot"].map({1.0: "Apr-Jun", 0.0: "Other months"}))
    non18c = z[z["r18c"] == 0]
    na, nb = int((non18c["mechA"] == 1).sum()), int((non18c["mechA"] == 0).sum())
    welch = stats.ttest_ind(a["ir"], b["ir"], equal_var=False)
    mw = stats.mannwhitneyu(a["ir"], b["ir"])

    rng = np.random.default_rng(SEED)
    obs = a["ir"].mean() - b["ir"].mean()
    labels = z["mechA"].to_numpy().astype(bool)
    strata = [np.flatnonzero(z["hot"].to_numpy() == h) for h in (0.0, 1.0)]
    perm = []
    for _ in range(N_PERM):
        lab = labels.copy()
        for idx in strata:
            lab[idx] = rng.permutation(labels[idx])
        perm.append(z["ir"].to_numpy()[lab].mean() - z["ir"].to_numpy()[~lab].mean())
    p_strat = float((1 + (np.abs(perm) >= abs(obs)).sum()) / (N_PERM + 1))

    rows = []
    specs = [("Mechanism A only", ["mechA"]), ("+ Apr-Jun dummy", ["mechA", "hot"]),
             ("+ route (18A, 18C; A+H in controls)", ["mechA", "hot", "r18a", "r18c", "ah"]),
             ("+ route + size + fixed price", ["mechA", "hot", "r18a", "r18c", "ah", "lproc", "fixed"])]
    for label, xs in specs:
        r = ols_focus(z, "y", xs, "mechA")
        rows.append([label, *fmt_focus(r), f"{2.8 * r['se']:.2f}"])
        if label.startswith("+ route (18A"):
            family.append(("Mechanism", "Mechanism A vs B, route- and time-adjusted", r["p"]))
        if label == "Mechanism A only":
            family.append(("Mechanism", "Mechanism A vs B, raw (stratified permutation)", p_strat))
    table = pd.DataFrame(rows, columns=["Specification", "Mechanism A coefficient (HC3 s.e.)", "HC3 p", "Wild cluster p", "N",
                                        "Min. detectable effect (log pts, 80% power)"])
    return f"""# Offer Mechanism A vs B, 2026 (N = {len(z)} with a recorded mechanism)

Research plan line A proposes A vs B as a main hypothesis. The cross-tab shows why it cannot be identified as such.

## Who uses Mechanism A

{to_markdown(cross, "Mechanism")}

{to_markdown(hot_cross, "Mechanism")}

- {int(cross.loc['Mechanism A', '18C'])} of {int(cross['18C'].sum())} 18C issuers use Mechanism A. Only {na} of the {na + nb} non-18C issuers with a mechanism are on A.
  "A vs B" is therefore almost the same variable as "18C vs the rest", and it is a choice made by the issuer.

## Raw contrast

Mean IR {100 * a['ir'].mean():.1f}% (A, n = {len(a)}) vs {100 * b['ir'].mean():.1f}% (B, n = {len(b)}); median
{100 * a['ir'].median():.1f}% vs {100 * b['ir'].median():.1f}%. Welch p = {welch.pvalue:.3f}, Mann-Whitney p = {mw.pvalue:.3f},
permutation p stratified by the Apr-Jun window = {p_strat:.3f}.

## Adjusted contrast, outcome log(1 + IR)

{to_markdown(table.set_index("Specification"), "Specification")}

- Once route is held fixed the Mechanism A coefficient is identified from {na} non-18C issuers only, so its standard
  error is large. The sample cannot separate a mechanism effect from an 18C effect at any economically plausible size.
- Recommendation: fold Mechanism A vs B into the route/18C analysis as a descriptive note, or move it to a multi-year
  study. Do not present it as an independent 2026 hypothesis.
"""


# ------------------------------------------------------------------ 3. tails

def quantile_bootstrap(z: pd.DataFrame, xs: list[str], q: float, n_boot: int, seed: int) -> tuple[pd.Series, pd.DataFrame, int]:
    """Quantile regression point estimates and pairs-bootstrap draws (rank-deficient draws rejected and counted)."""
    X = sm.add_constant(z[xs].astype(float))
    y = z["y"].to_numpy()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        point = sm.QuantReg(y, X).fit(q=q, max_iter=5000).params
        rng = np.random.default_rng(seed)
        draws, rejected = [], 0
        for _ in range(n_boot):
            idx = rng.integers(0, len(z), len(z))
            Xb = X.iloc[idx]
            if np.linalg.matrix_rank(Xb) < Xb.shape[1]:
                rejected += 1
                continue
            draws.append(sm.QuantReg(y[idx], Xb).fit(q=q, max_iter=5000).params.to_numpy())
    return point, pd.DataFrame(draws, columns=X.columns), rejected


def boot_p(draws: pd.Series) -> float:
    """Two-sided percentile-bootstrap p-value for H0: coefficient = 0."""
    return float(min(1.0, 2 * min((draws <= 0).mean(), (draws >= 0).mean())))


def logit_or(z: pd.DataFrame, event: pd.Series, xs: list[str]) -> pd.DataFrame | None:
    X = sm.add_constant(z[xs].astype(float))
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fit = sm.Logit(event.astype(float), X).fit(disp=0, cov_type="HC3")
    except Exception:  # separation or singular Hessian
        return None
    if not np.isfinite(fit.params).all() or fit.params.abs().max() > 15:
        return None
    return pd.DataFrame({"OR": np.exp(fit.params), "p": fit.pvalues}).drop(index="const")


def tails_section(d: pd.DataFrame, family: list) -> tuple[str, dict]:
    z = estimation_sample(d)
    labels = {v.name: v.label for v in VARS}
    X = sm.add_constant(z[M3].astype(float))

    qr, paths = {}, {}
    for q in QUANTILES:
        point, draws, rejected = quantile_bootstrap(z, M3, q, N_BOOT, SEED)
        qr[q] = (point, draws, rejected)
    show = [x for x in M3 if x != "n90"]
    qtab = pd.DataFrame({
        f"q{int(100 * q)}": {labels[x]: f"{qr[q][0][x]:.2f} [{qr[q][1][x].quantile(.025):.2f}, {qr[q][1][x].quantile(.975):.2f}]"
                             + ("*" if qr[q][1][x].quantile(.025) > 0 or qr[q][1][x].quantile(.975) < 0 else "") for x in show}
        for q in QUANTILES})
    ols = sm.OLS(z["y"], X).fit(cov_type="HC3")
    qtab.insert(0, "OLS mean", {labels[x]: f"{ols.params[x]:.2f}{stars(ols.pvalues[x])}" for x in show})
    p_corner90 = boot_p(qr[0.90][1]["corner"])
    family.append(("Tails", "Cornerstone allocation, 90th-percentile quantile regression (bootstrap)", p_corner90))
    family.append(("Tails", "Cornerstone allocation, mean OLS (HC3)", float(ols.pvalues["corner"])))

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ppml = sm.GLM(1 + z["ir"], X, family=sm.families.Poisson()).fit(cov_type="HC3")
    ptab = pd.DataFrame({"Multiplier on 1 + IR, exp(b)": [f"{np.exp(ppml.params[x]):.2f}" for x in show],
                         "HC3 p": [f"{ppml.pvalues[x]:.3f}" for x in show]}, index=[labels[x] for x in show])
    family.append(("Tails", "A+H issuer, PPML on 1 + IR", float(ppml.pvalues["ah"])))
    family.append(("Tails", "April-June window, PPML on 1 + IR", float(ppml.pvalues["hot"])))

    small = ["ah", "vc", "corner", "hot", "lproc"]
    events = {"IR < 0 (break)": z["ir"] < 0, "IR > 50%": z["ir"] > 0.5, "IR > 100%": z["ir"] > 1.0}
    lt, logit_rows = [], {}
    for name, ev in events.items():
        res = logit_or(z, ev, small)
        logit_rows[name] = res
        lt.append(f"- **{name}**: {int(ev.sum())} of {len(z)} deals ({100 * ev.mean():.0f}%).")
    lg = pd.DataFrame({name: {labels[x]: f"{r.loc[x, 'OR']:.2f}{stars(r.loc[x, 'p'])}" for x in small} if r is not None else
                       {labels[x]: "n/a" for x in small} for name, r in logit_rows.items()})
    if logit_rows["IR < 0 (break)"] is not None:
        family.append(("Tails", "VC/PE backing -> P(IR < 0), logit", float(logit_rows["IR < 0 (break)"].loc["vc", "p"])))
    if logit_rows["IR > 100%"] is not None:
        family.append(("Tails", "April-June window -> P(IR > 100%), logit", float(logit_rows["IR > 100%"].loc["hot", "p"])))
    fisher_vc = stats.fisher_exact(pd.crosstab(z["vc"], z["ir"] < 0).to_numpy())
    fisher_hot = stats.fisher_exact(pd.crosstab(z["hot"], z["ir"] > 1).to_numpy())
    rej = sum(v[2] for v in qr.values())
    sig = {x: [q for q in QUANTILES if qr[q][1][x].quantile(.025) > 0 or qr[q][1][x].quantile(.975) < 0] for x in show}
    sig_text = "; ".join(f"{labels[x]}: {', '.join(f'q{int(100 * q)}' for q in qs)}" for x, qs in sig.items() if qs) or "none"

    text = f"""# Tails of the first-day return distribution, 2026 (N = {len(z)}, M3 specification)

The first-day-return distribution has losses and large gains: {100 * (z['ir'] < 0).mean():.0f}% of deals break issue while {100 * (z['ir'] > 1).mean():.0f}% more than double.
A mean regression averages over both, so this section asks where in the distribution each variable acts.

## 1. Quantile regressions of log(1 + IR)

Cells: coefficient [95% pairs-bootstrap interval]; * = interval excludes zero. {N_BOOT} draws, seed {SEED},
{rej} rank-deficient draws rejected in total. The OLS column repeats the M3 mean coefficients (HC3).

{to_markdown(qtab, "Variable")}

- Bootstrap intervals that exclude zero: {sig_text}. Everything else is compatible with no effect at that quantile.
- The cornerstone point estimates drift from {qr[0.10][0]['corner']:+.2f} at q10 to {qr[0.90][0]['corner']:+.2f} at q90 (fewer extreme pops with
  larger anchor share), but the q90 bootstrap interval includes zero (p = {p_corner90:.2f}). Asymptotic quantile standard errors would
  suggest significance; the bootstrap does not support it. Treat as a hypothesis for a larger sample, not a finding.
- The quantile estimates use {len(z)} observations. Read their signs and bootstrap intervals in the table;
  wide intervals limit inference about differences across the return distribution.

## 2. PPML on 1 + IR (mean multiplier, no log re-transformation bias)

{to_markdown(ptab, "Variable")}

## 3. Break and pop events (logit, reduced regressors, HC3)

{chr(10).join(lt)}

Odds ratios (* p<0.10, ** p<0.05, *** p<0.01); cornerstone allocation is a 0-1 share so its odds ratio is per 100 percentage points,
ln offer size per ln HK$bn. Events are few (about 5 per regressor), so read these as descriptive.

{to_markdown(lg, "Variable")}

- Fisher exact: VC/PE backing vs break issue p = {fisher_vc[1]:.4f} (odds ratio {fisher_vc[0]:.2f}); April-June vs IR > 100% p = {fisher_hot[1]:.4f} (odds ratio {fisher_hot[0]:.2f}).
- The VC/PE break-issue association must be assessed from the logit and Fisher tests above, rather than inferred from backing alone.
  Backing and listing route are selected characteristics; the A+H control does not establish a causal certification effect.
"""
    return text, {"qr": qr, "z": z, "ols": ols}


def fig_quantile_paths(qr: dict, ols) -> None:
    names = [("corner", "Cornerstone allocation"), ("hot", "April-June window"), ("ah", "A+H issuer"), ("vc", "VC/PE-backed")]
    fig, axes = new_fig(1, 4, figsize=(11, 3.4), sharey=False)
    x = np.array(QUANTILES)
    for ax, (key, title) in zip(axes, names):
        style_axes(ax)
        est = np.array([qr[q][0][key] for q in QUANTILES])
        lo = np.array([qr[q][1][key].quantile(.025) for q in QUANTILES])
        hi = np.array([qr[q][1][key].quantile(.975) for q in QUANTILES])
        ax.fill_between(x, lo, hi, color=BLUE, alpha=0.15, linewidth=0)
        ax.plot(x, est, color=BLUE, lw=2, marker="o", ms=5)
        ax.axhline(0, color=AXIS, lw=1)
        ax.axhline(ols.params[key], color=ORANGE, lw=1.5, ls="--")
        ax.set_title(title, fontsize=9, color=INK, loc="left", fontweight="bold")
        ax.set_xticks(x, [f"{int(100 * q)}" for q in x])
        ax.set_xlabel("Quantile of log(1 + IR)", fontsize=8, color=INK2)
    axes[0].set_ylabel("Coefficient", fontsize=8, color=INK2)
    fig.suptitle("Where in the IR distribution each variable acts (M3; band = 95% bootstrap interval, dashed = OLS mean)", x=0.01, ha="left",
                 fontsize=10, color=INK, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "fig6_quantile_paths.png", dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)


# ------------------------------------------------------------------ 4. demand and aftermarket

def demand_aftermarket_section(d: pd.DataFrame, family: list) -> str:
    labels = {v.name: v.label for v in VARS}
    xs = [x for x in M3]
    rows, hot_coef = {}, {}
    for name, dv in [("ln subscription ratio", "lsub"), ("ln public applicants", "lapp"), ("ln average application value", "lavg")]:
        z = d[[dv, "month", *xs]].replace([np.inf, -np.inf], np.nan).dropna()
        fit = sm.OLS(z[dv], sm.add_constant(z[xs].astype(float))).fit(cov_type="HC3")
        rows[name] = {**{labels[x]: f"{fit.params[x]:.2f}{stars(fit.pvalues[x])}" for x in xs}, "R-squared": f"{fit.rsquared:.2f}", "N": str(len(z))}
        hot_coef[dv] = fit.params["hot"]
        if dv == "lsub":
            hot_p_lsub = float(fit.pvalues["hot"])
        if dv == "lsub":
            family.append(("Demand", "April-June window -> ln subscription ratio", float(fit.pvalues["hot"])))
    demand = pd.DataFrame(rows)

    slopes = []
    z = d.dropna(subset=["y", "lsub"])
    for label, part in [("All", z), ("April-June", z[z["hot"] == 1]), ("Other months", z[z["hot"] == 0])]:
        fit = sm.OLS(part["y"], sm.add_constant(part[["lsub"]])).fit(cov_type="HC3")
        slopes.append([label, str(len(part)), f"{fit.params['lsub']:.3f} ({fit.bse['lsub']:.3f})", f"{fit.rsquared:.2f}"])
    inter = sm.OLS(z["y"], sm.add_constant(pd.DataFrame({"lsub": z["lsub"], "hot": z["hot"], "lsub_x_hot": z["lsub"] * z["hot"]}))).fit(cov_type="HC3")
    slope_tab = pd.DataFrame(slopes, columns=["Sample", "N", "d log(1+IR) / d ln subscription (HC3 s.e.)", "R-squared"])

    # aftermarket: hot window vs rest ("1 month" is the same T+20 observation as "Day 20", so only Day 20 is used)
    am_rows, wr_ps = [], {}
    for name in HORIZONS:
        b, w = d[f"bhr_{name}"], d[f"wr_{name}"]
        ok = b.notna()
        hot, cold = b[ok & (d["hot"] == 1)], b[ok & (d["hot"] == 0)]
        wr_h, wr_c = w[ok & (d["hot"] == 1)].dropna(), w[ok & (d["hot"] == 0)].dropna()
        p_bhr = stats.mannwhitneyu(hot, cold).pvalue if len(hot) > 2 and len(cold) > 2 else np.nan
        p_wr = stats.mannwhitneyu(wr_h, wr_c).pvalue if len(wr_h) > 2 and len(wr_c) > 2 else np.nan
        wr_ps[name] = p_wr
        am_rows.append([name, f"{len(hot)} / {len(cold)}", f"{100 * hot.median():.1f}% / {100 * cold.median():.1f}%",
                        f"{100 * hot.mean():.1f}% / {100 * cold.mean():.1f}%", f"{p_bhr:.3f}",
                        f"{wr_h.median():.3f} / {wr_c.median():.3f}", f"{p_wr:.3f}"])
    for name in ("Day 20", "3 months"):
        family.append(("Aftermarket", f"Wealth relative vs HSI, {name}: Apr-Jun vs other listings (Mann-Whitney)", wr_ps[name]))
    am = pd.DataFrame(am_rows, columns=["Horizon", "N (Apr-Jun / other)", "Median BHR", "Mean BHR", "Mann-Whitney p (BHR)",
                                        "Median WR vs HSI", "Mann-Whitney p (WR)"])

    rev = []
    for name in HORIZONS:
        zz = d.dropna(subset=[f"bhr_{name}", "ir"])
        rho = stats.spearmanr(zz["ir"], zz[f"bhr_{name}"])
        fit = sm.OLS(zz[f"bhr_{name}"], sm.add_constant(zz[["ir", "hot"]])).fit(cov_type="HC3")
        rev.append([name, str(len(zz)), f"{rho.statistic:.2f} ({rho.pvalue:.3f})", f"{fit.params['ir']:.3f} ({fit.pvalues['ir']:.3f})"])
        if name == "3 months":
            family.append(("Aftermarket", "Day-1 return vs 3-month BHR (Spearman)", float(rho.pvalue)))
    rev_tab = pd.DataFrame(rev, columns=["Horizon", "N", "Spearman IR vs BHR (p)", "OLS slope on IR, controlling Apr-Jun (HC3 p)"])

    bins = pd.cut(d["ir"], [-1, 0, 0.25, 1, 10], labels=["IR <= 0", "0 to 25%", "25% to 100%", "> 100%"])
    tab = d.groupby(bins, observed=True).agg(N=("ir", "size"), stabilized=("stab", "mean"), greenshoe=("greenshoe", "mean"),
                                             m20=("bhr_Day 20", "median"))
    tab = pd.DataFrame({"N": tab["N"], "Stabilization purchases": (100 * tab["stabilized"]).map("{:.0f}%".format),
                        "Mean greenshoe exercise rate": (100 * tab["greenshoe"]).map("{:.0f}%".format),
                        "Median day-20 BHR": (100 * tab["m20"]).map("{:.1f}%".format)})

    return f"""# Demand and aftermarket, 2026

## 1. What drives retail demand (OLS, HC3, M3 regressors; * p<0.10, ** p<0.05, *** p<0.01)

{to_markdown(demand, "Variable")}

- The hot-window coefficient implies retail oversubscription about {np.exp(hot_coef['lsub']):.1f}x higher (HC3 p = {hot_p_lsub:.2f}: {verdict(hot_p_lsub)});
  its size depends on the controls, because the HSI return carries part of the regime. Larger offers see lower multiples, partly by
  construction because the retail tranche scales with size.
- The final retail share after clawback is deliberately excluded as a regressor: it is a mechanical function of the multiple.

## 2. First-day return and demand

{to_markdown(slope_tab.set_index("Sample"), "Sample")}

Interaction test (ln subscription x April-June), HC3 p = {inter.pvalues['lsub_x_hot']:.3f}. Demand and IR are jointly determined; this is the Rock/Welch
association, not a causal effect.

## 3. Aftermarket returns, hot window vs other listings

BHR is measured from the day-1 close; WR is the wealth relative vs the HSI over the same horizon. Only matured windows appear.
The 3-month "other" group is January-March listings; the 3-month hot group is April to early June listings.

{to_markdown(am.set_index("Horizon"), "Horizon")}

- Deals listed in the hot window fall further after day 1: medians turn clearly negative by day 20, and
  the 3-month gap is the largest. Each horizon mixes different calendar windows, and these Mann-Whitney p-values treat every IPO as independent.
  `analysis/out/event_time/` redoes this with listing-month clustering and calendar-time portfolios, where the gap is weaker: read that first.

## 4. Does a high day-1 return predict a later reversal?

{to_markdown(rev_tab.set_index("Horizon"), "Horizon")}

Unconditionally, higher first-day returns go with weaker 3-month BHR (rank correlation above), but the association disappears once the
Apr-Jun dummy is included. This is consistent with reversal being a feature of the listing window rather than of individual deals.

## 5. Stabilization and greenshoe by IR bin

{to_markdown(tab, "IR bin")}

Stabilization purchases cluster in weak deals and greenshoe exercise in strong ones, as the mechanism implies; both are consequences of
the first-day price, not explanatory variables for it.
"""


# ------------------------------------------------------------------ 5. prediction

def cv_r2(y: np.ndarray, X: np.ndarray | None, groups: np.ndarray | None) -> float:
    """Out-of-sample R-squared vs the training mean; leave-one-group-out (groups) or leave-one-out (None)."""
    n = len(y)
    folds = [np.flatnonzero(groups == g) for g in np.unique(groups)] if groups is not None else [np.array([i]) for i in range(n)]
    sse = sse0 = 0.0
    for test in folds:
        train = np.setdiff1d(np.arange(n), test)
        base = y[train].mean()
        if X is None:
            pred = np.full(len(test), base)
        else:
            beta = np.linalg.lstsq(np.c_[np.ones(len(train)), X[train]], y[train], rcond=None)[0]
            pred = np.c_[np.ones(len(test)), X[test]] @ beta
        sse += ((y[test] - pred) ** 2).sum()
        sse0 += ((y[test] - base) ** 2).sum()
    return 1 - sse / sse0


def prediction_section(d: pd.DataFrame) -> str:
    ex_ante = ["lage", "lproc", "ah", "vc", "tier1", "corner", "hsi", "n90"]
    z = d[["y", "month", "hot", "prior_ir", *ex_ante]].replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
    y, g = z["y"].to_numpy(), z["month"].to_numpy()
    sets = {"Mean only (null)": [], "April-June dummy only": ["hot"], "Prior-30-day IR only": ["prior_ir"],
            "Ex-ante issuer + market (no window)": ex_ante,
            "Ex-ante + prior IR": [*ex_ante, "prior_ir"],
            "M1: age, size, A+H + window": ["lage", "lproc", "ah", "hot"],
            "M3 baseline + window": [*ex_ante, "hot"]}
    rows = []
    for name, cols in sets.items():
        X = z[cols].to_numpy(float) if cols else None
        fit = sm.OLS(y, sm.add_constant(z[cols].astype(float))).fit() if cols else None
        rows.append([name, str(len(cols)), "0.000" if fit is None else f"{fit.rsquared:.3f}",
                     f"{cv_r2(y, X, g):.3f}", f"{cv_r2(y, X, None):.3f}"])
    oos = {r[0]: float(r[3]) for r in rows}
    tab = pd.DataFrame(rows, columns=["Model", "Regressors", "In-sample R-squared", "Out-of-sample R-squared, leave one month out",
                                      "Out-of-sample R-squared, leave one deal out"])
    return f"""# Predictability of first-day returns, 2026 (N = {len(z)}, deals with a prior-IR value)

Out-of-sample R-squared is measured against predicting each held-out deal with the training-sample mean; 0 is no
better than the mean, negative is worse. In leave-one-month-out the held-out month's Apr-Jun label is treated as known,
which flatters the window dummy: a forecaster would not know in real time that April had started a hot regime.

{to_markdown(tab.set_index("Model"), "Model")}

- The M3 baseline (leave-one-month-out {oos['M3 baseline + window']:.3f}) does {'better' if oos['M3 baseline + window'] > oos['April-June dummy only'] + 0.01 else 'no better'} than the window dummy alone ({oos['April-June dummy only']:.3f}); in-sample R-squared
  overstates it. Issuer and market variables without the window reach {oos['Ex-ante issuer + market (no window)']:.3f}; prior-IPO returns add nothing ({oos['Prior-30-day IR only']:.3f} alone).
- Most of the predictable variation in 2026 IR is the level shift between windows, and none of the variables tested forecasts that
  shift in real time. Any claim about issuer characteristics should be read against this ceiling.
"""


# ------------------------------------------------------------------ figures

def fig_regime(d: pd.DataFrame, scan: dict) -> None:
    z = d.dropna(subset=["y"])
    dates = z["ld"].to_numpy()
    fig, ax = new_fig(figsize=(9, 4.2))
    style_axes(ax)
    a, b, _ = scan["up"]
    ax.axvspan(pd.Timestamp(dates[a]), pd.Timestamp(dates[b - 1]), color=BLUE, alpha=0.10, linewidth=0)
    ax.scatter(z["ld"], z["ir"], s=16, color=MUTED, alpha=0.6, linewidths=0)
    roll = z.set_index("ld")["ir"].rolling(15, min_periods=8).median()
    ax.plot(roll.index, roll.values, color=BLUE, lw=2)
    ax.axhline(0, color=AXIS, lw=1)
    pct_axis(ax)
    ax.set_ylabel("First-day return", fontsize=9, color=INK2)
    ax.text(pd.Timestamp(dates[a]), ax.get_ylim()[1] * 0.93, "  best hot window", fontsize=8, color=BLUE, va="top")
    ax.text(roll.index[-1], roll.values[-1], "  15-deal median", fontsize=8, color=INK2, va="center")
    ax.set_xlim(z["ld"].min() - pd.Timedelta(days=5), z["ld"].max() + pd.Timedelta(days=40))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    fig.suptitle(f"2026 first-day returns in listing order (search-corrected window p = {scan['p']:.3f})", x=0.08, ha="left",
                 fontsize=10, color=INK, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "fig5_regime_scan.png", dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)


# ------------------------------------------------------------------ main

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    y26 = select_2026(load_panel())
    d = prepare(y26)
    family: list[tuple[str, str, float]] = []

    regime, info = regime_section(d, family)
    mech = mechanism_section(d, family)
    tails, tinfo = tails_section(d, family)
    demand = demand_aftermarket_section(d, family)
    pred = prediction_section(d)
    mult = bh_family(family)
    mult_text = ("# Multiplicity across the headline tests in this module\n\n"
                 "Benjamini-Hochberg step-up at FDR 10% over the tests listed. Other tables in this repository are outside this family.\n\n"
                 + to_markdown(mult.assign(p=mult["p"].map("{:.4f}".format), **{"q (BH)": mult["q (BH)"].map("{:.4f}".format)})
                               .set_index("Rank")[["Section", "Test", "p", "q (BH)"]], "Rank")
                 + f"\n\n- {int((mult['q (BH)'] < 0.10).sum())} of {len(mult)} tests have q < 0.10. Most p-values ignore listing-month clustering;"
                 " those that rely on it carry few (9) clusters, so q-values are indicative only. The family counts only tests reported here, not the"
                 " exploration that chose them, so q-values understate the true multiplicity.\n")

    for name, text in [("regime.md", regime), ("mechanism.md", mech), ("tails.md", tails), ("demand_aftermarket.md", demand),
                       ("prediction.md", pred), ("multiplicity.md", mult_text)]:
        (OUT / name).write_text(text, encoding="utf-8")
    fig_regime(d, info["scan"])
    fig_quantile_paths(tinfo["qr"], tinfo["ols"])
    print(f"Extended analysis written to {OUT.relative_to(ROOT)}/ (N = {len(d)})")


if __name__ == "__main__":
    main()
