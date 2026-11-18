"""Reference implementations of standard IPO research measures.

Import from a research script (copy the file or add its folder to sys.path):

    from ipo_metrics import (winsorize, initial_returns, price_revision,
                             money_left_on_table, bhar_panel, skew_adjusted_t,
                             bootstrap_skew_adjusted_test, wealth_relative,
                             calendar_time_portfolio)

Conventions
-----------
* Returns are simple decimal returns (0.05 = 5%), never percent.
* Missing inputs stay missing. No function fills NaN with 0.
* Every function is pure: it returns new objects and never mutates inputs.

Method sources are cited in each docstring; see references/long_run_performance.md
and references/variable_definitions.md of the ipo-empirical-research skill.
"""
from __future__ import annotations

from typing import Iterable, Optional, Sequence

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Cleaning
# ---------------------------------------------------------------------------

def winsorize(s: pd.Series, lower: float = 0.01, upper: float = 0.01,
              by: Optional[pd.Series] = None) -> pd.Series:
    """NaN-safe two-sided winsorization at the (lower, 1-upper) quantiles.

    Quantiles are computed on non-missing values only and NaNs are returned as
    NaN. ``scipy.stats.mstats.winsorize`` is avoided on purpose: it sorts NaN as
    the largest value, so with missing data the top "tail" is NaN and genuine
    outliers survive (scipy issues #8327, #16211).

    ``by`` (e.g. listing year) winsorizes within each group, the usual choice
    for multi-year pooled samples whose distributions shift across years.
    """
    s = pd.to_numeric(s, errors="coerce").astype(float)

    def _clip(x: pd.Series) -> pd.Series:
        valid = x.dropna()
        if valid.empty:
            return x
        lo, hi = valid.quantile([lower, 1.0 - upper])
        return x.clip(lower=lo, upper=hi)

    if by is None:
        return _clip(s)
    return s.groupby(by).transform(_clip)


# ---------------------------------------------------------------------------
# Offer-level measures
# ---------------------------------------------------------------------------

def initial_returns(offer_price: pd.Series, first_close: pd.Series,
                    mkt_at_pricing: Optional[pd.Series] = None,
                    mkt_at_first_close: Optional[pd.Series] = None) -> pd.DataFrame:
    """First-day (initial) return and its market-adjusted variants.

    IR       = P1 / P0 - 1                       (Ritter: offer price to first close)
    log_IR   = ln(P1 / P0)                       (less skewed; common regression LHS)
    MAIR     = (1 + IR) / (1 + Rm) - 1           (Aggarwal, Leal & Hernandez 1993)
    MAIR_d   = IR - Rm                           (difference form, also common)

    Rm must cover the window over which subscribers bear market risk: from the
    index close on the price-determination date (or subscription close, state
    which) to the index close on the first trading day. It is *not* the listing-
    day index return alone. In Hong Kong that window is about T+2 business days
    after FINI (22 Nov 2023) and about T+5 before.
    """
    p0 = pd.to_numeric(offer_price, errors="coerce").astype(float)
    p1 = pd.to_numeric(first_close, errors="coerce").astype(float)
    p0 = p0.where(p0 > 0)
    p1 = p1.where(p1 > 0)
    out = pd.DataFrame({"ir": p1 / p0 - 1.0, "log_ir": np.log(p1 / p0)})
    if mkt_at_pricing is not None and mkt_at_first_close is not None:
        m0 = pd.to_numeric(mkt_at_pricing, errors="coerce").astype(float)
        m1 = pd.to_numeric(mkt_at_first_close, errors="coerce").astype(float)
        rm = m1 / m0.where(m0 > 0) - 1.0
        out["rm_window"] = rm
        out["mair"] = (1.0 + out["ir"]) / (1.0 + rm) - 1.0
        out["mair_diff"] = out["ir"] - rm
    return out


def price_revision(offer_price: pd.Series, range_low: pd.Series,
                   range_high: pd.Series) -> pd.DataFrame:
    """Price revision relative to the filing range (Hanley 1993 partial adjustment).

    pr_mid     = (P0 - Pmid) / Pmid
    range_pos  = (P0 - Plow) / (Phigh - Plow); NaN for fixed-price offers
                 (Plow == Phigh), never imputed as 0.5
    below_range / above_range flags; is_fixed_price flag.

    In Hong Kong an offer may price up to 10% below the range bottom under the
    Pricing Flexibility Mechanism (HKEX Guide 4.14), so range_pos < 0 is valid.
    """
    p0 = pd.to_numeric(offer_price, errors="coerce").astype(float)
    lo = pd.to_numeric(range_low, errors="coerce").astype(float)
    hi = pd.to_numeric(range_high, errors="coerce").astype(float)
    mid = (lo + hi) / 2.0
    width = hi - lo
    fixed = width.eq(0)
    out = pd.DataFrame(index=p0.index)
    out["pr_mid"] = (p0 - mid) / mid.where(mid > 0)
    out["range_pos"] = ((p0 - lo) / width).where(width > 0)
    out["is_fixed_price"] = fixed.where(width.notna())
    out["below_range"] = (p0 < lo).where(p0.notna() & lo.notna())
    out["above_range"] = (p0 > hi).where(p0.notna() & hi.notna())
    return out


def money_left_on_table(offer_price: pd.Series, first_close: pd.Series,
                        base_shares: pd.Series) -> pd.Series:
    """(P1 - P0) x base offer shares, excluding the over-allotment option (Ritter)."""
    p0 = pd.to_numeric(offer_price, errors="coerce").astype(float)
    p1 = pd.to_numeric(first_close, errors="coerce").astype(float)
    n = pd.to_numeric(base_shares, errors="coerce").astype(float)
    return (p1 - p0) * n


# ---------------------------------------------------------------------------
# Long-run performance: event-time
# ---------------------------------------------------------------------------

def bhar_panel(panel: pd.DataFrame, horizon: int, id_col: str = "ipo_id",
               t_col: str = "event_t", r_col: str = "ret", b_col: str = "bench_ret",
               after_delisting: str = "benchmark", min_periods: int = 1) -> pd.DataFrame:
    """Buy-and-hold returns over event periods 1..horizon for each IPO.

    ``panel`` is long form: one row per IPO and event period (month or day)
    with the firm return and the benchmark return of the *same* period. Period 1
    should start after the first-day close so the initial return is excluded
    (state this; including it mixes underpricing into long-run performance).

    after_delisting:
      'benchmark' - after the firm's last return, the firm is assumed to earn the
                    benchmark, so BHAR stops accumulating (Barber & Lyon 1997,
                    Lyon, Barber & Tsai 1999). Incorporate delisting returns in
                    ``ret`` before calling.
      'truncate'  - compound only observed periods for both firm and benchmark.
    Firms observed for fewer than ``min_periods`` periods get NaN.

    Returns bhr, bench_bhr, bhar, n_obs, and complete (observed through horizon).
    """
    if after_delisting not in {"benchmark", "truncate"}:
        raise ValueError("after_delisting must be 'benchmark' or 'truncate'")
    d = panel.loc[(panel[t_col] >= 1) & (panel[t_col] <= horizon),
                  [id_col, t_col, r_col, b_col]].copy()
    if d.duplicated([id_col, t_col]).any():
        raise ValueError("duplicate (id, event_t) rows in panel")

    def _one(g: pd.DataFrame) -> pd.Series:
        g = g.sort_values(t_col)
        obs = g[r_col].notna()
        n_obs = int(obs.sum())
        if n_obs < min_periods:
            return pd.Series({"bhr": np.nan, "bench_bhr": np.nan, "bhar": np.nan,
                              "n_obs": n_obs, "complete": False})
        if after_delisting == "truncate":
            g = g[obs & g[b_col].notna()]
            firm = np.prod(1.0 + g[r_col].to_numpy())
            bench = np.prod(1.0 + g[b_col].to_numpy())
        else:
            last_t = g.loc[obs, t_col].max()
            firm_part = g[g[t_col] <= last_t]
            if firm_part[r_col].isna().any():
                # Interior gaps (e.g. trading suspensions) must be resolved upstream.
                return pd.Series({"bhr": np.nan, "bench_bhr": np.nan, "bhar": np.nan,
                                  "n_obs": n_obs, "complete": False})
            tail = g[g[t_col] > last_t]
            firm = np.prod(1.0 + firm_part[r_col].to_numpy()) * \
                np.prod(1.0 + tail[b_col].to_numpy())
            bench = np.prod(1.0 + g[b_col].to_numpy())
        return pd.Series({"bhr": firm - 1.0, "bench_bhr": bench - 1.0,
                          "bhar": firm - bench, "n_obs": n_obs,
                          "complete": n_obs == horizon})

    res = pd.DataFrame({k: _one(g) for k, g in d.groupby(id_col)}).T
    res.index.name = id_col
    return res.astype({"bhr": float, "bench_bhr": float, "bhar": float,
                       "n_obs": int, "complete": bool})


def wealth_relative(bhr: pd.Series, bench_bhr: pd.Series) -> float:
    """Ritter (1991) wealth relative: (1 + mean BHR_ipo) / (1 + mean BHR_bench).

    Uses the matched sample (rows with both values). < 1 means underperformance.
    """
    m = pd.concat([bhr, bench_bhr], axis=1).dropna()
    return float((1.0 + m.iloc[:, 0].mean()) / (1.0 + m.iloc[:, 1].mean()))


def skew_adjusted_t(x: Iterable[float]) -> float:
    """Skewness-adjusted t-statistic (Johnson 1978; Lyon, Barber & Tsai 1999, eq. 5).

    t_sa = sqrt(n) * (S + gamma * S**2 / 3 + gamma / (6 n)),
    S = mean / sd,  gamma = sum((x - mean)**3) / (n * sd**3).
    Long-run BHARs are strongly right-skewed, which biases the ordinary t-test
    toward rejecting in the lower tail.
    """
    a = np.asarray(pd.Series(list(x), dtype=float).dropna())
    n = a.size
    if n < 3:
        return float("nan")
    mean, sd = a.mean(), a.std(ddof=1)
    if sd == 0:
        return float("nan")
    s = mean / sd
    gamma = np.sum((a - mean) ** 3) / (n * sd ** 3)
    return float(np.sqrt(n) * (s + gamma * s ** 2 / 3.0 + gamma / (6.0 * n)))


def bootstrap_skew_adjusted_test(x: Iterable[float], reps: int = 1000,
                                 resample_frac: float = 0.25,
                                 seed: Optional[int] = 12345) -> dict:
    """Bootstrapped skewness-adjusted t-test (Lyon, Barber & Tsai 1999, Sec. III.B).

    Draws ``reps`` resamples of size n_b = resample_frac * n (LBT use n/4) and
    computes the statistic on each resample centred on the full-sample mean,
    which imposes the null. The two-sided p-value compares the full-sample t_sa
    to that bootstrap distribution.
    """
    a = np.asarray(pd.Series(list(x), dtype=float).dropna())
    n = a.size
    t_obs = skew_adjusted_t(a)
    if n < 8 or not np.isfinite(t_obs):
        return {"t_sa": t_obs, "p_boot": float("nan"), "n": n, "reps": 0}
    rng = np.random.default_rng(seed)
    nb = max(int(round(resample_frac * n)), 4)
    mu = a.mean()
    stats = np.empty(reps)
    for b in range(reps):
        s = rng.choice(a, size=nb, replace=True)
        sd = s.std(ddof=1)
        if sd == 0:
            stats[b] = np.nan
            continue
        S = (s.mean() - mu) / sd
        g = np.sum((s - s.mean()) ** 3) / (nb * sd ** 3)
        stats[b] = np.sqrt(nb) * (S + g * S ** 2 / 3.0 + g / (6.0 * nb))
    stats = stats[np.isfinite(stats)]
    p_lo = np.mean(stats <= t_obs)
    p_hi = np.mean(stats >= t_obs)
    return {"t_sa": t_obs, "p_boot": float(min(1.0, 2 * min(p_lo, p_hi))),
            "crit_2.5%": float(np.quantile(stats, 0.025)),
            "crit_97.5%": float(np.quantile(stats, 0.975)),
            "n": n, "n_b": nb, "reps": int(stats.size)}


# ---------------------------------------------------------------------------
# Long-run performance: calendar-time portfolios
# ---------------------------------------------------------------------------

def calendar_time_portfolio(monthly: pd.DataFrame, factors: pd.DataFrame,
                            window_months: int = 36, weight: str = "ew",
                            min_firms: int = 10, factor_cols: Sequence[str] = ("mkt_rf",),
                            rf_col: str = "rf", id_col: str = "ipo_id",
                            month_col: str = "month", r_col: str = "ret",
                            listing_month_col: str = "listing_month",
                            me_col: Optional[str] = "me_lag", nw_lags: int = 6) -> dict:
    """Jensen's alpha of a rolling IPO portfolio (Fama 1998; Mitchell & Stafford 2000).

    Each calendar month the portfolio holds every IPO whose listing month is
    within the previous ``window_months`` months (excluding the listing month
    itself). Months with fewer than ``min_firms`` holdings are dropped; thin
    portfolios make alpha noisy and heteroskedastic.

    ``monthly``: one row per IPO-month with ``month`` and ``listing_month`` as
    pandas Periods (freq 'M'), the return, and for VW the lagged market equity.
    ``factors``: indexed by monthly Period with ``rf_col`` and ``factor_cols``
    (e.g. mkt_rf, smb, hml from Ken French's Asia-Pacific ex-Japan library or
    locally constructed HK factors). Inference uses Newey-West HAC errors.
    """
    import statsmodels.api as sm

    d = monthly.copy()
    age = (d[month_col] - d[listing_month_col]).apply(lambda x: x.n)
    d = d[(age >= 1) & (age <= window_months) & d[r_col].notna()]
    if weight == "vw":
        if me_col is None:
            raise ValueError("vw weighting needs lagged market equity (me_col)")
        d = d[d[me_col] > 0]
        port = (d[r_col] * d[me_col]).groupby(d[month_col]).sum() / \
            d[me_col].groupby(d[month_col]).sum()
    elif weight == "ew":
        port = d.groupby(month_col)[r_col].mean()
    else:
        raise ValueError("weight must be 'ew' or 'vw'")
    n_firms = d.groupby(month_col)[id_col].nunique()
    port = port[n_firms.reindex(port.index) >= min_firms]
    reg = pd.concat([port.rename("rp"), factors], axis=1, join="inner").dropna()
    y = reg["rp"] - reg[rf_col]
    X = sm.add_constant(reg[list(factor_cols)])
    fit = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": nw_lags})
    return {"alpha": float(fit.params["const"]), "t_alpha": float(fit.tvalues["const"]),
            "p_alpha": float(fit.pvalues["const"]), "months": int(fit.nobs),
            "avg_firms": float(n_firms.reindex(reg.index).mean()),
            "result": fit}
