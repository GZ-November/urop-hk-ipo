"""Shared focused regressions, multiple-test adjustment and group diagnostics.

Callers supply outcomes, covariates, focus variables and explicit study samples.
This module does not load data, render figures or import report entry points.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
from shared.inference import wild_cluster_p

def stars(p: float) -> str:
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""



def ols_focus(d: pd.DataFrame, y: str, xs: list[str], focus: str, wild: bool = True) -> dict:
    """OLS on the listwise-complete sample: coefficient, HC3 p and (optionally) wild-cluster-bootstrap p."""
    z = d[[y, "month", *xs]].replace([np.inf, -np.inf], np.nan).dropna()
    X = sm.add_constant(z[xs].astype(float), has_constant="add")
    fit = sm.OLS(z[y].astype(float), X).fit(cov_type="HC3")
    clusters = z["month"].to_numpy()
    p_wild = np.nan
    if wild and 2 <= len(np.unique(clusters)) <= 16:
        p_wild = wild_cluster_p(z[y].to_numpy(float), X.to_numpy(), clusters, list(X.columns).index(focus))
    return {"n": len(z), "b": fit.params[focus], "se": fit.bse[focus], "p": fit.pvalues[focus],
            "p_wild": p_wild, "r2": fit.rsquared}



def fmt_focus(r: dict, digits: int = 3) -> list[str]:
    wild = "—" if np.isnan(r["p_wild"]) else f"{r['p_wild']:.3f}"
    return [f"{r['b']:.{digits}f}{stars(r['p'])} ({r['se']:.{digits}f})", f"{r['p']:.3f}", wild, str(r["n"])]



def bh_family(rows: list[tuple[str, str, float]], q: float = 0.10) -> pd.DataFrame:
    """Benjamini-Hochberg step-up adjustment over (section, test, p) rows."""
    frame = pd.DataFrame(rows, columns=["Section", "Test", "p"]).dropna(subset=["p"]).reset_index(drop=True)
    frame["q (BH)"] = multipletests(frame["p"], alpha=q, method="fdr_bh")[1]
    frame["Rank"] = frame["p"].rank(method="first").astype(int)
    return frame.sort_values("p").reset_index(drop=True)



def anova_icc(y: np.ndarray, groups: np.ndarray, n_perm: int = 5000, seed: int = 20260930) -> tuple[float, float, float]:
    """One-way ANOVA intraclass correlation, F and permutation p across listing months."""
    labels, inverse = np.unique(groups, return_inverse=True)

    def f_stat(vals):
        sizes = np.bincount(inverse)
        means = np.bincount(inverse, vals) / sizes
        ssb = (sizes * (means - vals.mean()) ** 2).sum()
        ssw = ((vals - means[inverse]) ** 2).sum()
        return (ssb / (len(labels) - 1)) / (ssw / (len(vals) - len(labels))), ssb, ssw
    f_obs, _, _ = f_stat(y)
    sizes = np.bincount(inverse)
    k0 = (len(y) - (sizes ** 2).sum() / len(y)) / (len(labels) - 1)
    icc = (f_obs - 1) / (f_obs + k0 - 1)
    rng = np.random.default_rng(seed)
    perm = np.array([f_stat(rng.permutation(y))[0] for _ in range(n_perm)])
    return float(icc), float(f_obs), float((1 + (perm >= f_obs).sum()) / (n_perm + 1))

