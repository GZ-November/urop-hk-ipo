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


def _numeric(s: pd.Series) -> pd.Series:
    """Coerce invalid/nonfinite values to missing without changing the index."""
    v = pd.to_numeric(s, errors="coerce").astype(float)
    return v.where(np.isfinite(v))


def _aligned(*series: pd.Series) -> None:
    if any(not s.index.is_unique for s in series):
        raise ValueError("Series indexes must be unique")
    if any(not s.index.equals(series[0].index) for s in series[1:]):
        raise ValueError("Series indexes must match exactly; align inputs explicitly")


def _positive_int(value, name: str, minimum: int = 1) -> None:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


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
    _aligned(s)
    if not (np.isfinite(lower) and np.isfinite(upper) and lower >= 0 and upper >= 0 and lower + upper < 1):
        raise ValueError("tail fractions must be nonnegative and sum to less than one")
    if by is not None:
        _aligned(s, by)
        if by.isna().any():
            raise ValueError("group labels must be known")
    s = _numeric(s)

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
    _aligned(offer_price, first_close)
    if (mkt_at_pricing is None) != (mkt_at_first_close is None):
        raise ValueError("provide both market index Series or neither")
    p0 = _numeric(offer_price)
    p1 = _numeric(first_close)
    p0 = p0.where(p0 > 0)
    p1 = p1.where(p1 > 0)
    out = pd.DataFrame({"ir": p1 / p0 - 1.0, "log_ir": np.log(p1 / p0)})
    if mkt_at_pricing is not None and mkt_at_first_close is not None:
        _aligned(offer_price, mkt_at_pricing, mkt_at_first_close)
        m0 = _numeric(mkt_at_pricing)
        m1 = _numeric(mkt_at_first_close)
        rm = m1.where(m1 > 0) / m0.where(m0 > 0) - 1.0
        out["rm_window"] = rm
        out["mair"] = (1.0 + out["ir"]) / (1.0 + rm) - 1.0
        out["mair_diff"] = out["ir"] - rm
    return out.replace([np.inf, -np.inf], np.nan)


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
    _aligned(offer_price, range_low, range_high)
    p0, lo, hi = (_numeric(x).where(_numeric(x) > 0)
                  for x in (offer_price, range_low, range_high))
    invalid_range = lo.notna() & hi.notna() & hi.lt(lo)
    if invalid_range.any():
        raise ValueError("range_high must be >= range_low")
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
    _aligned(offer_price, first_close, base_shares)
    p0, p1, n = map(_numeric, (offer_price, first_close, base_shares))
    result = (p1.where(p1 > 0) - p0.where(p0 > 0)) * n.where(n >= 0)
    return result.where(np.isfinite(result))


# ---------------------------------------------------------------------------
# Long-run performance: event-time
# ---------------------------------------------------------------------------

def bhar_panel(panel: pd.DataFrame, horizon: int, id_col: str = "ipo_id",
               t_col: str = "event_t", r_col: str = "ret", b_col: str = "bench_ret",
               after_delisting: str = "benchmark", min_periods: int = 1,
               available_through: Optional[dict] = None,
               delisting_periods: Optional[dict] = None) -> pd.DataFrame:
    """Fixed-horizon BHR/BHAR with explicit missingness and delisting semantics.

    Supply one row per IPO and event period 1..horizon, including missing rows.
    Period 1 begins after the first-day close. Returns are decimals >= -1.
    ``available_through`` maps IPO IDs to elapsed periods at the data cutoff;
    values below horizon mark immature IPOs (no numeric horizon result).
    Without it, a complete grid is required, but maturity must be checked upstream.
    ``delisting_periods`` maps IDs to verified delisting periods. The return at
    that period MUST include the delisting payoff. Only then may missing later
    returns be replaced by benchmark returns. No missing value implies delisting.
    'truncate' stops BOTH legs at a verified delisting period; this is a shorter
    holding period, labelled truncated/complete=False, never a horizon return.
    For benchmark reinvestment, the terminal wealth difference scales with the
    benchmark; simple-difference BHAR is not frozen at delisting.

    Returns all input IDs, typed empty output, and status/valid/complete flags.
    Complete means valid full-horizon strategy, including documented reinvestment.
    n_obs counts actual valid firm returns, not substituted benchmark returns.
    """
    _positive_int(horizon, "horizon")
    _positive_int(min_periods, "min_periods")
    if min_periods > horizon:
        raise ValueError("min_periods cannot exceed horizon")
    if after_delisting not in {"benchmark", "truncate"}:
        raise ValueError("after_delisting must be 'benchmark' or 'truncate'")
    cols = [id_col, t_col, r_col, b_col]
    d = panel[cols].copy()
    if d[id_col].isna().any():
        raise ValueError("IPO IDs cannot be missing")
    periods = pd.to_numeric(d[t_col], errors="coerce")
    if (periods.isna() | ~np.isfinite(periods) | (periods < 1) | (periods % 1 != 0)).any():
        raise ValueError("event periods must be positive integers")
    d[t_col] = periods.astype(int)
    if d.duplicated([id_col, t_col]).any():
        raise ValueError("duplicate (id, event_t) rows in panel")
    ids = set(d[id_col])
    for mapping, name in [(available_through, "available_through"),
                          (delisting_periods, "delisting_periods")]:
        if mapping is not None:
            if set(mapping) - ids:
                raise ValueError(f"{name} contains unknown IPO IDs")
            for value in mapping.values():
                _positive_int(value, name, minimum=0 if name == "available_through" else 1)
    if available_through is not None and set(available_through) != ids:
        raise ValueError("available_through must cover every IPO ID")
    for c in [r_col, b_col]:
        original = pd.to_numeric(d[c], errors="coerce")
        if (original.dropna() < -1).any():
            raise ValueError("simple returns cannot be below -1")
        d[c] = _numeric(d[c])
    schema = {"bhr": float, "bench_bhr": float, "bhar": float,
              "n_obs": int, "effective_horizon": int, "valid": bool,
              "complete": bool, "status": str}
    rows = []
    keys = []
    for key, g in d.groupby(id_col, sort=False):
        g = g.set_index(t_col).sort_index()
        within = g.loc[g.index <= horizon]
        row = dict(bhr=np.nan, bench_bhr=np.nan, bhar=np.nan,
                   n_obs=int(within[r_col].notna().sum()), effective_horizon=0,
                   valid=False, complete=False, status="incomplete_grid")
        keys.append(key)
        rows.append(row)
        elapsed = available_through.get(key) if available_through is not None else None
        if elapsed is not None and elapsed < horizon:
            row["status"] = "immature"
            continue
        dl = (delisting_periods or {}).get(key)
        if dl is not None and elapsed is not None and dl > elapsed:
            raise ValueError("delisting cannot be after the observation cutoff")
        relevant_dl = dl is not None and dl <= horizon
        stop = dl if relevant_dl and after_delisting == "truncate" else horizon
        if not pd.Index(range(1, stop + 1)).isin(g.index).all():
            continue
        part = g.reindex(range(1, stop + 1))
        ret = part[r_col].copy()
        bench = part[b_col]
        if bench.isna().any():
            row["status"] = "missing_benchmark"
            continue
        if relevant_dl:
            if g.loc[g.index > dl, r_col].notna().any():
                raise ValueError("firm returns after verified delisting must be missing")
            if ret.loc[:dl].isna().any():
                row["status"] = "missing_firm_return"
                continue
            if after_delisting == "benchmark":
                ret.loc[ret.index > dl] = bench.loc[bench.index > dl]
        if ret.isna().any():
            row["status"] = "missing_firm_return"
            continue
        if row["n_obs"] < min_periods:
            row["status"] = "insufficient_observations"
            continue
        firm_wealth = float(np.prod(1 + ret.to_numpy()))
        bench_wealth = float(np.prod(1 + bench.to_numpy()))
        if not np.isfinite(firm_wealth) or not np.isfinite(bench_wealth):
            row["status"] = "nonfinite_wealth"
            continue
        row.update(bhr=firm_wealth - 1, bench_bhr=bench_wealth - 1,
                   bhar=firm_wealth - bench_wealth, effective_horizon=stop,
                   valid=True, complete=stop == horizon,
                   status="truncated" if stop < horizon else
                          ("delisted_reinvested" if relevant_dl else "complete"))
    result = pd.DataFrame(rows, columns=schema, index=pd.Index(keys, name=id_col))
    return result.astype(schema)


def wealth_relative(bhr: pd.Series, bench_bhr: pd.Series) -> float:
    """Ritter (1991) wealth relative: (1 + mean BHR_ipo) / (1 + mean BHR_bench).

    Uses the matched sample (rows with both values). < 1 means underperformance.
    """
    _aligned(bhr, bench_bhr)
    m = pd.concat([_numeric(bhr), _numeric(bench_bhr)], axis=1).dropna()
    if m.empty or (m < -1).any().any() or 1 + m.iloc[:, 1].mean() <= 0:
        return float("nan")
    return float((1.0 + m.iloc[:, 0].mean()) / (1.0 + m.iloc[:, 1].mean()))


def skew_adjusted_t(x: Iterable[float]) -> float:
    """Skewness-adjusted t-statistic (Johnson 1978; Lyon, Barber & Tsai 1999, eq. 5).

    t_sa = sqrt(n) * (S + gamma * S**2 / 3 + gamma / (6 n)),
    S = mean / sd,  gamma = sum((x - mean)**3) / (n * sd**3).
    Long-run BHARs are strongly right-skewed, which biases the ordinary t-test
    toward rejecting in the lower tail.
    """
    a = _numeric(pd.Series(list(x), dtype=float)).dropna().to_numpy()
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
    _positive_int(reps, "reps")
    if not np.isfinite(resample_frac) or not 0 < resample_frac <= 1:
        raise ValueError("resample_frac must be in (0, 1]")
    a = _numeric(pd.Series(list(x), dtype=float)).dropna().to_numpy()
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
    if stats.size == 0:
        return {"t_sa": t_obs, "p_boot": float("nan"), "n": n,
                "n_b": nb, "reps": 0, "requested_reps": reps}
    # Plus-one correction avoids a zero Monte Carlo tail probability.
    p_lo = (1 + np.sum(stats <= t_obs)) / (stats.size + 1)
    p_hi = (1 + np.sum(stats >= t_obs)) / (stats.size + 1)
    return {"t_sa": t_obs, "p_boot": float(min(1.0, 2 * min(p_lo, p_hi))),
            "crit_2.5%": float(np.quantile(stats, 0.025)),
            "crit_97.5%": float(np.quantile(stats, 0.975)),
            "n": n, "n_b": nb, "reps": int(stats.size), "requested_reps": reps}


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
    locally constructed HK factors). Inference uses Newey-West HAC errors on
    consecutive calendar months; gaps are rejected. Duplicate IPO-months or
    factor months, rank/df failure and nonpositive VW weights are checked.
    Returns result, monthly portfolio/exclusion audit and actual holdings/weights.
    All return and factor series must share currency and decimal scaling.
    """
    import statsmodels.api as sm

    _positive_int(window_months, "window_months")
    _positive_int(min_firms, "min_firms")
    _positive_int(nw_lags, "nw_lags", minimum=0)
    if weight not in {"ew", "vw"}:
        raise ValueError("weight must be 'ew' or 'vw'")
    if not factor_cols or len(set(factor_cols)) != len(factor_cols) or rf_col in factor_cols:
        raise ValueError("factor_cols must be distinct and exclude rf_col")
    if "const" in factor_cols or "rp" in factor_cols or rf_col in {"const", "rp"}:
        raise ValueError("const and rp are reserved column names")
    d = monthly.copy()
    if d.empty:
        raise ValueError("no IPO-month observations")
    if d[[id_col, month_col, listing_month_col]].isna().any().any():
        raise ValueError("IPO IDs and dates cannot be missing")
    if d.duplicated([id_col, month_col]).any():
        raise ValueError("duplicate (IPO ID, month) observations")
    for col in [month_col, listing_month_col]:
        if not isinstance(d[col].dtype, pd.PeriodDtype) or d[col].dtype.freq != pd.offsets.MonthEnd():
            raise ValueError(f"{col} must contain monthly pandas Periods")
    if d.groupby(id_col)[listing_month_col].nunique().gt(1).any():
        raise ValueError("each IPO must have one listing month")
    if not isinstance(factors.index, pd.PeriodIndex) or factors.index.freq != pd.offsets.MonthEnd():
        raise ValueError("factors must have a monthly PeriodIndex")
    if not factors.index.is_unique or factors.index.hasnans or not factors.columns.is_unique:
        raise ValueError("factor months and columns must be unique and nonmissing")
    factor_data = factors[[rf_col, *factor_cols]].apply(_numeric)
    # Full calendar ordering matters: HAC must not compress missing months.
    age = d[month_col].astype("int64") - d[listing_month_col].astype("int64")
    d = d[(age >= 1) & (age <= window_months)].copy()
    d[r_col] = _numeric(d[r_col])
    if d[r_col].dropna().lt(-1).any():
        raise ValueError("simple returns cannot be below -1")
    all_months = pd.period_range(monthly[month_col].min(), monthly[month_col].max(), freq="M")
    d = d[d[r_col].notna()].copy()
    if weight == "vw":
        if me_col is None:
            raise ValueError("vw weighting needs lagged market equity (me_col)")
        d[me_col] = _numeric(d[me_col])
        d = d[d[me_col] > 0].copy()
        d["portfolio_weight"] = d[me_col] / d.groupby(month_col)[me_col].transform("sum")
    else:
        d["portfolio_weight"] = 1 / d.groupby(month_col)[id_col].transform("size")
    port = (d[r_col] * d["portfolio_weight"]).groupby(d[month_col]).sum()
    n_firms = d.groupby(month_col)[id_col].nunique()
    audit = pd.DataFrame({"rp": port, "n_firms": n_firms}).reindex(all_months)
    audit["n_firms"] = audit["n_firms"].fillna(0).astype(int)
    audit = audit.join(factor_data)
    enough = audit["n_firms"] >= min_firms
    finite_factors = audit[[rf_col, *factor_cols]].notna().all(axis=1)
    audit["reason"] = np.where(~enough, "too_few_firms",
                                np.where(~finite_factors, "missing_factor", "included"))
    reg = audit.loc[audit["reason"].eq("included")].sort_index()
    if len(reg) <= len(factor_cols) + 1:
        raise ValueError("insufficient months for positive residual degrees of freedom")
    if np.any(np.diff(reg.index.asi8) != 1):
        raise ValueError("HAC requires consecutive calendar months; resolve gaps or explicitly select a contiguous window")
    if nw_lags >= len(reg):
        raise ValueError("nw_lags must be less than the number of regression months")
    y = reg["rp"] - reg[rf_col]
    X = sm.add_constant(reg[list(factor_cols)], has_constant="add")
    if np.linalg.matrix_rank(X.to_numpy()) != X.shape[1]:
        raise ValueError("factor design is rank deficient")
    fit = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": nw_lags})
    return {"alpha": float(fit.params["const"]), "t_alpha": float(fit.tvalues["const"]),
            "p_alpha": float(fit.pvalues["const"]), "months": int(fit.nobs),
            "avg_firms": float(reg["n_firms"].mean()), "result": fit,
            "portfolio": audit, "holdings": d, "regression_months": reg.index}
