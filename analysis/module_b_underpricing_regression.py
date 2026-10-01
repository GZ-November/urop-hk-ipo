"""Module B — what explains underpricing in 2026 HK Main Board IPOs?

Dependent variable: ln(1 + initial return) = ln(day-1 close / offer price).
The raw return is bounded below; its logarithm is far less skewed than the
raw return, and a coefficient reads as a proportional change in the price ratio.

Four nested OLS models with HC3 standard errors (at most 10 regressors).
Every model controls for the April-June hot window, as required by the research plan.
18A/18C groups remain descriptive in Module A; state-owned cornerstones belong in
the separate cornerstone study, keeping this small-sample model parsimonious.

    M1  Ex-ante uncertainty        Rock (1986), Beatty & Ritter (1986)
    M2  + Certification            Megginson & Weiss (1991), Carter & Manaster (1990),
                                   Lee & Wahal (2004), Hoberg (2007)
    M3  + Market conditions        Lowry & Schwert (2002), Lowry (2003)      <- baseline
    M4  + Retail demand (ln subscription ratio)   Rock (1986), Welch (1992)  <- descriptive

The subscription ratio is measured at the same time as pricing, so M4 is a channel
check (does demand absorb the other effects?), not a causal estimate.

Status of the specification: theory-driven and fixed in this file before estimation,
but *exploratory*. The correlation matrix of the candidates was inspected first, and
the data are 2026 only, so nothing here is confirmatory. Freeze the specification and
re-estimate it, unchanged, on 2026Q4 listings as an out-of-sample check.

Robustness of the baseline (M3): raw return as the dependent variable, winsorized
dependent variable, dropping the three largest returns, median (quantile) regression,
quarter fixed effects in place of the market variables, and a pairs bootstrap.

Inference: IPOs listed in the same month share market shocks, and the two market
variables vary only by date, so HC3 errors are likely too small. Table 6 therefore adds
cluster-robust errors by listing month and a restricted wild cluster bootstrap-t with
exact enumeration of all 2^G sign patterns (G = 9 months; Cameron, Gelbach & Miller 2008).

Outputs (analysis/out/module_b/):
    table3_hypotheses.md          Variables, definitions, theory and predicted signs
    table4_regressions.md / .tex  M1-M4
    table5_robustness.md / .tex   Baseline under alternative estimators
    table6_inference.md           HC3 vs month-clustered vs wild cluster bootstrap p-values
    fig4_coefficients.png         Baseline effects, OLS vs median regression

Usage:
    python3 analysis/module_b_underpricing_regression.py
"""

from __future__ import annotations

from dataclasses import dataclass

import itertools

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.diagnostic import het_breuschpagan

from research_inputs import C as C, ROOT as ROOT, load_panel as load_panel, select_2026 as select_2026  # noqa: F401 — legacy C export
from module_a_stylized_facts import (
    BLUE, GRID, INK, INK2, MUTED, ORANGE, SURFACE, new_fig, style_axes, to_latex, to_markdown,
)

OUT = ROOT / "analysis" / "out" / "module_b"
N_BOOT = 2000
SEED = 20260929


# ------------------------------------------------------------ specification

@dataclass(frozen=True)
class Var:
    name: str
    label: str
    block: str
    sign: str        # predicted sign: "+", "-" or "+/-"
    theory: str
    definition: str


VARS = [
    Var("lage", "ln firm age", "uncertainty", "-",
        "Beatty & Ritter (1986): older firms have more track record",
        "ln(years from incorporation to listing)"),
    Var("lproc", "ln offer size", "uncertainty", "-",
        "Ritter (1984); Beatty & Ritter (1986): size proxies for information available",
        "ln(offer price x base offer shares, HK$bn), before over-allotment"),
    Var("ah", "A+H issuer", "uncertainty", "-",
        "Rock (1986): a public A-share price removes much of the information asymmetry",
        "1 if the issuer already trades on the A-share market"),
    Var("vc", "VC/PE-backed", "certification", "+/-",
        "Megginson & Weiss (1991) certification (-) vs Gompers (1996), Lee & Wahal (2004) (+)",
        "1 if any pre-IPO VC or PE investor"),
    Var("tier1", "Top-tier sponsor", "certification", "+/-",
        "Carter & Manaster (1990) (-) vs Hoberg (2007): top banks underprice more (+)",
        "1 if the best sponsor is tier 1 of the 2025 HK underwriter ranking"),
    Var("corner", "Cornerstone allocation", "certification", "+/-",
        "Anchor certification (-) vs smaller float and demand signal (+); see Module C",
        "Final cornerstone allocation, share of base offer"),
    Var("hsi", "HSI return, prior 20 days", "market", "+",
        "Lowry & Schwert (2002): market momentum passes into initial returns",
        "HSI return over the 20 trading days before the prospectus"),
    Var("n90", "IPO count, prior 90 days", "market", "+/-",
        "Sentiment and volume (+) vs underwriter capacity and supply crowding (-)",
        "HK ordinary IPOs in the 90 days before the prospectus"),
    Var("hot", "April-June hot window", "time", "+",
        "2026 research plan: control for the observed April-June hot window",
        "1 if listing occurs in April-June 2026; exploratory time control"),
    Var("lsub", "ln subscription ratio", "demand", "+",
        "Rock (1986), Welch (1992): retail demand; endogenous, descriptive only",
        "ln(public offer subscription multiple)"),
]
V = {v.name: v for v in VARS}
BLOCK_VARS = {b: [v.name for v in VARS if v.block == b] for b in ("uncertainty", "certification", "market", "demand")}

MODELS = {
    "M1": BLOCK_VARS["uncertainty"] + ["hot"],
    "M2": BLOCK_VARS["uncertainty"] + BLOCK_VARS["certification"] + ["hot"],
    "M3": BLOCK_VARS["uncertainty"] + BLOCK_VARS["certification"] + BLOCK_VARS["market"] + ["hot"],
}
MODELS["M4"] = MODELS["M3"] + BLOCK_VARS["demand"]
BASELINE = "M3"
BLOCK_LABEL = {"uncertainty": "Uncertainty", "certification": "Certification", "market": "Market conditions", "time": "Time control"}


# Compatibility name for existing notebooks; no second implementation.
from research_inputs import prepare_regression as prepare


# ------------------------------------------------------------------- data


def design(d: pd.DataFrame, xs: list[str], y: str = "y") -> tuple[pd.Series, pd.DataFrame, pd.Series]:
    """Listwise-complete (y, X with constant) and the matching stock codes."""
    z = d[[y] + xs + ["code"]].replace([np.inf, -np.inf], np.nan).dropna()
    X = sm.add_constant(z[xs].astype(float), has_constant="add")
    if len(z) <= X.shape[1]:
        raise ValueError("Regression needs more complete observations than coefficients")
    if np.linalg.matrix_rank(X) < X.shape[1]:
        raise ValueError("Regression design is rank deficient; remove constant or collinear regressors")
    return z[y], X, z["code"]


def estimation_sample(d: pd.DataFrame) -> pd.DataFrame:
    """Use one finite complete-case sample for all nested models and inference."""
    columns = list(dict.fromkeys(["y", "code", "month", *MODELS["M4"]]))
    return d.replace([np.inf, -np.inf], np.nan).dropna(subset=columns).copy()


def table_sample_selection(d: pd.DataFrame) -> pd.DataFrame:
    """Report overlapping exclusion reasons before common-sample selection."""
    clean = d.replace([np.inf, -np.inf], np.nan)
    rows = {}
    for name in ["y", "code", "month", *MODELS["M4"]]:
        label = {"y": "Outcome: log(1 + IR)", "code": "Stock code", "month": "Listing month"}.get(name, V[name].label if name in V else name)
        rows[label] = {"Missing/invalid": int(clean[name].isna().sum()), "Available": int(clean[name].notna().sum())}
    rows["Common complete-case sample (M1-M4)"] = {
        "Missing/invalid": len(d) - len(estimation_sample(d)), "Available": len(estimation_sample(d))}
    return pd.DataFrame(rows).T


# ------------------------------------------------------------- estimation

def fit_ols(d: pd.DataFrame, xs: list[str], y: str = "y"):
    yy, X, _ = design(d, xs, y)
    return sm.OLS(yy, X).fit(cov_type="HC3")


def fit_median(d: pd.DataFrame, xs: list[str], y: str = "y"):
    yy, X, _ = design(d, xs, y)
    return sm.QuantReg(yy, X).fit(q=0.5, max_iter=5000)


def winsorize(s: pd.Series, lo: float, hi: float) -> pd.Series:
    a, b = s.quantile([lo, hi])
    return s.clip(a, b)


def bootstrap_ci(d: pd.DataFrame, xs: list[str]) -> pd.DataFrame:
    """Pairs bootstrap, percentile 95% intervals for OLS coefficients."""
    yy, X, _ = design(d, xs)
    Y, A = yy.to_numpy(), X.to_numpy()
    rng = np.random.default_rng(SEED)
    draws = []
    attempts = 0
    while len(draws) < N_BOOT and attempts < 10 * N_BOOT:
        attempts += 1
        i = rng.integers(0, len(Y), len(Y))
        if np.linalg.matrix_rank(A[i]) < A.shape[1]:
            continue
        beta, *_ = np.linalg.lstsq(A[i], Y[i], rcond=None)
        draws.append(beta)
    if len(draws) != N_BOOT:
        raise ValueError("Too few full-rank bootstrap resamples; simplify the model")
    lo, hi = np.percentile(np.array(draws), [2.5, 97.5], axis=0)
    intervals = pd.DataFrame({"lo": lo, "hi": hi}, index=X.columns)
    intervals.attrs["rejected_draws"] = attempts - N_BOOT
    return intervals


def stars(p: float) -> str:
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def cell(b: float, se: float, p: float) -> str:
    return f"{b:.3f}{stars(p)} ({se:.3f})"


def block_wald_p(res, names: list[str]) -> float:
    if not all(n in res.params.index for n in names):
        return np.nan
    return float(res.wald_test(", ".join(f"{n} = 0" for n in names), use_f=True, scalar=True).pvalue)


# ---------------------------------------------- clustered inference (numpy)

def cr1_cov(X: np.ndarray, u: np.ndarray, g: np.ndarray) -> np.ndarray:
    """Cluster-robust covariance with the CR1 small-sample correction (as in Stata / statsmodels)."""
    n, k = X.shape
    ids = np.unique(g)
    if len(ids) < 2 or n <= k or np.linalg.matrix_rank(X) < k:
        raise ValueError("Cluster covariance needs full rank, residual degrees of freedom and at least two clusters")
    bread = np.linalg.inv(X.T @ X)
    meat = np.zeros((k, k))
    for c in ids:
        s = X[g == c].T @ u[g == c]
        meat += np.outer(s, s)
    return (len(ids) / (len(ids) - 1)) * ((n - 1) / (n - k)) * bread @ meat @ bread


def cluster_t(Y: np.ndarray, X: np.ndarray, g: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    beta = np.linalg.solve(X.T @ X, X.T @ Y)
    u = Y - X @ beta
    return beta, beta / np.sqrt(np.diag(cr1_cov(X, u, g)))


def wild_cluster_p(Y: np.ndarray, X: np.ndarray, g: np.ndarray, j: int) -> float:
    """Restricted wild cluster bootstrap-t p-value for H0: beta_j = 0.

    Rademacher weights, one per cluster, enumerated exactly (2^G draws)."""
    _, t_obs = cluster_t(Y, X, g)
    keep = [c for c in range(X.shape[1]) if c != j]
    Xr = X[:, keep]
    br = np.linalg.solve(Xr.T @ Xr, Xr.T @ Y)
    fit_r, u_r = Xr @ br, Y - Xr @ br
    ids = np.unique(g)
    if len(ids) > 16:
        raise ValueError("Exact wild bootstrap supports at most 16 clusters; use a simulated method for larger samples")
    idx = np.searchsorted(ids, g)
    t_star = []
    for w in itertools.product((-1.0, 1.0), repeat=len(ids)):
        y_star = fit_r + np.array(w)[idx] * u_r
        t_star.append(cluster_t(y_star, X, g)[1][j])
    return float(np.mean(np.abs(t_star) >= abs(t_obs[j]) - 1e-12))


# ----------------------------------------------------------------- tables

def table_hypotheses() -> pd.DataFrame:
    rows = {
        v.label: {"Block": v.block, "Definition": v.definition, "Predicted sign": v.sign, "Theory": v.theory}
        for v in VARS
    }
    return pd.DataFrame(rows).T


def table_regressions(d: pd.DataFrame) -> tuple[pd.DataFrame, list[str], dict]:
    d = estimation_sample(d)
    fits = {m: fit_ols(d, xs) for m, xs in MODELS.items()}
    order = ["const"] + [v.name for v in VARS]
    label = {"const": "Intercept", **{v.name: v.label for v in VARS}}
    out = {}
    for m, r in fits.items():
        col = {}
        for n in order:
            col[label[n]] = cell(r.params[n], r.bse[n], r.pvalues[n]) if n in r.params.index else ""
        col["N"] = f"{int(r.nobs)}"
        col["R-squared"] = f"{r.rsquared:.3f}"
        col["Adj. R-squared"] = f"{r.rsquared_adj:.3f}"
        for b, names in BLOCK_VARS.items():
            if b in BLOCK_LABEL:
                p = block_wald_p(r, names)
                col[f"Joint F-test, {BLOCK_LABEL[b].lower()} (p)"] = "" if np.isnan(p) else f"{p:.3f}"
        yy, X, _ = design(d, MODELS[m])
        col["Breusch-Pagan (p)"] = f"{het_breuschpagan(fits[m].resid, X)[1]:.3f}"
        out[m] = col
    tab = pd.DataFrame(out)

    base = fits[BASELINE]
    _, _, codes = design(d, MODELS[BASELINE])
    cooks = pd.Series(base.get_influence().cooks_distance[0], index=codes.to_numpy()).sort_values(ascending=False)
    top = ", ".join(f"{c} ({v:.2f})" for c, v in cooks.head(3).items())
    dy = [fits[m].rsquared_adj for m in MODELS]
    notes = [
        "Dependent variable: ln(1 + first-day return). HC3 standard errors in parentheses; * p<0.10, ** p<0.05, *** p<0.01.",
        "Read a dummy coefficient b as a proportional change in the day-1 price ratio: exp(b) - 1.",
        f"Adjusted R-squared across M1-M4: {' -> '.join(f'{x:.3f}' for x in dy)}.",
        f"Most influential observations in {BASELINE} (Cook's distance): {top}.",
        "M4 adds a demand variable measured at pricing; treat it as a channel check, not a causal estimate.",
        "All four models use the same finite complete-case sample, including the demand variable and listing month; see sample_selection.md for overlapping missing/invalid counts.",
        "With roughly 100 observations and up to 10 regressors, non-significance is weak evidence of no effect; "
        "the model has little power against moderate effects.",
    ]
    return tab, notes, fits


def table_inference(d: pd.DataFrame, base_fit) -> tuple[pd.DataFrame, list[str]]:
    xs = MODELS[BASELINE]
    yy, X, _ = design(d, xs)
    g = d.loc[X.index, "month"].to_numpy()
    if pd.isna(g).any():
        raise ValueError("Listing month is required for every observation in the baseline clustering sample")
    Y, A = yy.to_numpy(), X.to_numpy()
    beta, t = cluster_t(Y, A, g)
    G = len(np.unique(g))
    p_cr1 = 2 * stats.t.sf(np.abs(t), df=G - 1)
    rows = {}
    for j, n in enumerate(X.columns):
        if n == "const":
            continue
        rows[V[n].label] = {
            "Coefficient": f"{beta[j]:.3f}",
            "HC3 p": f"{base_fit.pvalues[n]:.3f}",
            f"Cluster-robust p, t({G - 1})": f"{p_cr1[j]:.3f}",
            f"Wild cluster bootstrap p ({2 ** G} draws)": f"{wild_cluster_p(Y, A, g, j):.3f}",
        }
    sizes = pd.Series(g).value_counts().sort_index()
    notes = [
        f"Clusters: {G} listing months ({', '.join(f'{m[-2:]}: {n}' for m, n in sizes.items())} IPOs). "
        "With so few clusters, conventional cluster-robust p-values are unreliable; the wild cluster bootstrap is the "
        "recommended small-G test (Cameron, Gelbach & Miller 2008).",
        "Wild cluster bootstrap: restricted residuals, Rademacher weights per cluster, all 2^G sign patterns enumerated "
        "(exact, no simulation noise); a p-value cannot go below 2 / 2^G = "
        f"{2 / 2 ** G:.3f}.",
        "Cluster-robust and HC3 coefficients are identical (same OLS fit); only the standard errors differ.",
    ]
    return pd.DataFrame(rows).T, notes


def table_robustness(d: pd.DataFrame, base_fit) -> tuple[pd.DataFrame, list[str], dict]:
    xs = MODELS[BASELINE]
    _, X, _ = design(d, xs)
    d2 = d.loc[X.index].copy()
    d2["y_w"] = winsorize(d2["y"], 0.01, 0.99)
    d2["y_raw"] = d2["ir"]
    drop3 = d2.drop(d2["ir"].nlargest(3).index)
    xs_fe = [x for x in xs if x not in BLOCK_VARS["market"] and x != "hot"] + ["q2", "q3"]

    specs = {
        "Baseline (M3)": (base_fit, "ols"),
        "Raw return": (fit_ols(d2, xs, "y_raw"), "ols"),
        "Winsorized 1/99": (fit_ols(d2, xs, "y_w"), "ols"),
        "Drop top-3 returns": (fit_ols(drop3, xs), "ols"),
        "Median regression": (fit_median(d2, xs), "med"),
        "Quarter FE": (fit_ols(d2, xs_fe), "ols"),
    }
    boot = bootstrap_ci(d, xs)
    order = ["const"] + xs + ["q2", "q3"]
    label = {"const": "Intercept", "q2": "2026Q2 dummy", "q3": "2026Q3 dummy", **{v.name: v.label for v in VARS}}
    cols = {}
    for name, (r, _) in specs.items():
        col = {}
        for n in order:
            col[label[n]] = cell(r.params[n], r.bse[n], r.pvalues[n]) if n in r.params.index else ""
        col["N"] = f"{int(r.nobs)}"
        col["R-squared"] = f"{r.prsquared:.3f} (pseudo)" if hasattr(r, "prsquared") else f"{r.rsquared:.3f}"
        cols[name] = col
    col = {label[n]: f"[{boot.loc[n, 'lo']:.3f}, {boot.loc[n, 'hi']:.3f}]" for n in ["const"] + xs}
    col["N"] = f"{int(base_fit.nobs)}"
    col["R-squared"] = ""
    cols[f"Bootstrap 95% CI ({N_BOOT})"] = col
    tab = pd.DataFrame(cols).fillna("")
    tab = tab.loc[[r for r in tab.index if tab.loc[r].astype(str).str.strip().ne("").any()]]

    n_specs = len(specs)
    sig = {  # (specifications significant at 5%, specifications that include the variable); bootstrap counts as one
        v: (
            sum(r.pvalues[v] < 0.05 for r, _ in specs.values() if v in r.params.index)
            + int(boot.loc[v, "lo"] > 0 or boot.loc[v, "hi"] < 0),
            sum(v in r.params.index for r, _ in specs.values()) + 1,
        )
        for v in xs
    }
    tab.loc["Specifications significant at 5%"] = [""] * len(tab.columns)
    tab.loc["Specifications significant at 5%", "Baseline (M3)"] = "; ".join(
        f"{V[v].label} {k}/{m}" for v, (k, m) in sig.items() if k > 0) or "none"
    robust = [V[v].label for v, (k, m) in sig.items() if k == m]
    notes = [
        "Dependent variable is ln(1 + first-day return) except 'Raw return' (return in decimal units; coefficients are not comparable in size).",
        "Median regression reports asymptotic standard errors; it estimates the effect on the typical IPO, not the mean.",
        "Quarter FE replaces the market variables and hot-window control with quarter dummies; other robustness checks use the baseline complete-case sample.",
        f"Bootstrap: {N_BOOT} full-rank pairs resamples of the baseline sample, seed {SEED}; {boot.attrs['rejected_draws']} rank-deficient draws rejected.",
        f"Significant at 5% in every specification that includes them (incl. the bootstrap interval): {', '.join(robust) or 'none'}. "
        "These p-values ignore clustering by listing month; see Table 6 for the wild cluster bootstrap.",
    ]
    return tab, notes, specs


# ---------------------------------------------------------------- figure

def fig_coefficients(d: pd.DataFrame, base_fit, med_fit) -> None:
    xs = MODELS[BASELINE]
    _, X, _ = design(d, xs)
    delta = {n: (1.0 if set(X[n].dropna().unique()) <= {0.0, 1.0} else X[n].std()) for n in xs}
    y = np.arange(len(xs))[::-1]
    ci_b = base_fit.conf_int()
    ci_m = med_fit.conf_int()

    fig, ax = new_fig(figsize=(8.4, 5.6))
    style_axes(ax)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    for i, n in zip(y, xs):
        k = delta[n]
        for off, res, ci, col, mk in ((0.14, base_fit, ci_b, BLUE, "o"), (-0.14, med_fit, ci_m, ORANGE, "s")):
            b, lo, hi = res.params[n] * k, ci.loc[n, 0] * k, ci.loc[n, 1] * k
            ax.plot([lo, hi], [i + off] * 2, color=col, lw=1.6, solid_capstyle="round")
            ax.plot(b, i + off, marker=mk, color=col, ms=6, mec=SURFACE, mew=1.2)
    ax.axvline(0, color=INK2, lw=1)
    ax.set_yticks(y, [V[n].label + ("" if delta[n] == 1.0 else " (per 1 SD)") for n in xs])
    prev = None
    for i, n in zip(y, xs):
        if V[n].block != prev:
            ax.axhline(i + 0.5, color=GRID, lw=1)
            ax.text(ax.get_xlim()[0] + 0.005, i + 0.44, BLOCK_LABEL[V[n].block].upper(), color=MUTED, fontsize=7,
                    ha="left", va="bottom")
            prev = V[n].block
    ax.set_xlabel("Effect on ln(1 + first-day return), 95% intervals\ndummies: switched on; continuous: +1 SD",
                  color=INK2, fontsize=8.5)
    ax.plot([], [], color=BLUE, marker="o", lw=1.6, label="OLS, HC3")
    ax.plot([], [], color=ORANGE, marker="s", lw=1.6, label="Median regression")
    ax.legend(frameon=False, fontsize=8, loc="upper right", labelcolor=INK2)
    ax.set_title(f"What explains 2026 underpricing? Baseline model (N = {int(base_fit.nobs)})",
                 loc="left", fontsize=11, color=INK, fontweight="bold")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.text(0.01, 0.008, "Intervals ignore clustering by listing month; see Table 6 for wild-bootstrap p-values.",
             fontsize=7.5, color=MUTED)
    fig.savefig(OUT / "fig4_coefficients.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)


# ------------------------------------------------------------------- main

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    y26 = select_2026(load_panel())
    raw = prepare(y26)
    selection = table_sample_selection(raw)
    d = estimation_sample(raw)

    t3 = table_hypotheses()
    t4, n4, fits = table_regressions(d)
    t5, n5, specs = table_robustness(d, fits[BASELINE])
    t6, n6 = table_inference(d, fits[BASELINE])
    bullet = lambda ns: "\n".join(f"- {n}" for n in ns)

    (OUT / "sample_selection.md").write_text(
        f"# Module B sample selection — 2026 listings only\n\nInput: {len(raw)} issuers; common complete-case sample: {len(d)}.\n\n"
        + to_markdown(selection, "Input")
        + "\n\nCounts overlap. Nonpositive age, proceeds or subscription ratio, IR <= -1, invalid flags/tier and non-finite values are missing inputs; unknown flags are never recoded as zero.\n",
        encoding="utf-8")

    (OUT / "table3_hypotheses.md").write_text(
        "# Table 3 — Variables, theory and predicted signs\n\n" + to_markdown(t3, "Variable") + "\n", encoding="utf-8")
    (OUT / "table4_regressions.md").write_text(
        f"# Table 4 — Determinants of underpricing, 2026 HK IPOs (N = {int(fits[BASELINE].nobs)})\n\n"
        + to_markdown(t4, "") + "\n\n" + bullet(n4) + "\n", encoding="utf-8")
    (OUT / "table4_regressions.tex").write_text(to_latex(t4, "Table 4. Determinants of underpricing") + "\n", encoding="utf-8")
    (OUT / "table5_robustness.md").write_text(
        "# Table 5 — Robustness of the baseline model (M3)\n\n" + to_markdown(t5, "") + "\n\n" + bullet(n5) + "\n",
        encoding="utf-8")
    (OUT / "table5_robustness.tex").write_text(to_latex(t5, "Table 5. Robustness of the baseline model") + "\n", encoding="utf-8")

    (OUT / "table6_inference.md").write_text(
        "# Table 6 — Inference with time clustering, baseline model (M3)\n\n" + to_markdown(t6, "Variable") + "\n\n"
        + bullet(n6) + "\n", encoding="utf-8")

    fig_coefficients(d, fits[BASELINE], specs["Median regression"][0])
    print(f"Module B written to {OUT.relative_to(ROOT)}/ (baseline N = {int(fits[BASELINE].nobs)})")


if __name__ == "__main__":
    main()
