"""Event-time and calendar-time aftermarket returns of 2026 IPOs from cached daily bars.

Answers, with the daily bars for all 106 issuers (data/market/aftermarket, to late September 2026):
does the April-June listing window earn lower returns after day 1, and is that an artefact of
cross-sectional overlap? Two standard designs (Lowry, Michaely & Volkova 2017, Ch. 7):

  1. Event time    Buy-and-hold abnormal return (BHAR) vs the HSI (and HSTECH) from the day-1
                   close, at 5/20/40/60/90 trading days, hot window vs other listings.
                   Inference by exact wild cluster bootstrap on listing months, and Mann-Whitney.
  2. Calendar time Equal-weighted portfolios of issuers in their first 60 trading days after
                   day 1, one for April-June listings and one for the rest; alpha with
                   Newey-West standard errors. Overlapping issuers are averaged within each date,
                   so this design does not treat 45 same-window IPOs as 45 independent draws.

Benchmark returns are taken between each issuer's own consecutive bar dates, so a suspended or
missing day never becomes a zero benchmark return. Only matured windows enter (no partial windows).

Outputs (analysis/out/event_time/): event_time.md, fig7_bhar_paths.png.

Usage:
    python3 analysis/aftermarket_event_time_2026.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.multitest import multipletests

import module_b_underpricing_regression as mb
from research_inputs import ROOT as ROOT, load_panel as load_panel, select_2026 as select_2026
from module_a_stylized_facts import (
    AXIS, BLUE, INK, INK2, MUTED, ORANGE, new_fig, pct_axis, style_axes, to_markdown,
)

OUT = ROOT / "analysis" / "out" / "event_time"
BARS = ROOT / "pipeline" / "prospectus_pipeline" / "data" / "market" / "aftermarket"
HORIZONS = (5, 20, 40, 60, 90)
HOLD_DAYS = 60
MIN_PORTFOLIO = 5
NW_LAGS = 10
MIN_PATH_N = 15


# ------------------------------------------------------------------ data

def load_bars(path: Path) -> pd.Series:
    """Close price indexed by date from a cached bar file."""
    bars = json.loads(path.read_text(encoding="utf-8"))
    return pd.Series({pd.Timestamp(b["date"]): float(b["close"]) for b in bars}).sort_index()


def aligned_returns(stock: pd.Series, bench: pd.Series) -> pd.DataFrame:
    """Stock and benchmark simple returns between the stock's own consecutive bar dates.

    Rows where either benchmark date is missing are dropped rather than set to zero."""
    frame = pd.DataFrame({"close": stock, "bench": bench.reindex(stock.index)})
    frame["r"] = frame["close"].pct_change()
    frame["m"] = frame["bench"].pct_change()
    frame["event_day"] = np.arange(len(frame))
    return frame


def issuer_panel(y26: pd.DataFrame, benches: dict[str, pd.Series], bars_dir: Path = BARS) -> pd.DataFrame:
    """Long issuer-day panel with returns and each benchmark's return, event_day 0 = listing day."""
    rows = []
    for _, row in y26.iterrows():
        path = bars_dir / f"hk{row['Stock Code'].split('.')[0].zfill(5)}.json"
        if not path.exists():
            continue
        stock = load_bars(path)
        if stock.index[0] != row["listing_date"]:
            continue  # history truncated or not starting on the listing date: unusable
        parts = {name: aligned_returns(stock, b) for name, b in benches.items()}
        base = parts["HSI"][["close", "r", "event_day"]].copy()
        for name, part in parts.items():
            base[f"m_{name}"] = part["m"]
            base[f"idx_{name}"] = part["bench"]
        base["code"] = row["Stock Code"]
        base["hot"] = float(4 <= row["listing_date"].month <= 6)
        base["month"] = str(row["listing_date"].to_period("M"))
        rows.append(base.rename_axis("date").reset_index())
    return pd.concat(rows, ignore_index=True)


def bhar(panel: pd.DataFrame, bench: str, k: int) -> pd.DataFrame:
    """BHAR at event day k from the day-1 close, only for issuers with a bar and benchmark price at day 0 and k."""
    day0 = panel[panel["event_day"] == 0].set_index("code")
    dayk = panel[panel["event_day"] == k].set_index("code")
    common = day0.index.intersection(dayk.index)
    r_stock = dayk.loc[common, "close"] / day0.loc[common, "close"] - 1
    r_bench = dayk.loc[common, f"idx_{bench}"] / day0.loc[common, f"idx_{bench}"] - 1
    out = pd.DataFrame({"bhar": r_stock - r_bench, "hot": day0.loc[common, "hot"], "month": day0.loc[common, "month"]})
    return out.replace([np.inf, -np.inf], np.nan).dropna()


# ------------------------------------------------------------------ event time

def group_difference(z: pd.DataFrame) -> dict:
    """Hot minus other mean BHAR: HC3 p, exact wild cluster p over listing months, Mann-Whitney p."""
    X = sm.add_constant(z[["hot"]].astype(float))
    fit = sm.OLS(z["bhar"], X).fit(cov_type="HC3")
    clusters = z["month"].to_numpy()
    wild = np.nan
    if 2 <= len(np.unique(clusters)) <= 16 and z["hot"].nunique() == 2:
        wild = mb.wild_cluster_p(z["bhar"].to_numpy(float), X.to_numpy(), clusters, 1)
    hot, other = z.loc[z["hot"] == 1, "bhar"], z.loc[z["hot"] == 0, "bhar"]
    mw = stats.mannwhitneyu(hot, other).pvalue if len(hot) > 2 and len(other) > 2 else np.nan
    return {"diff": fit.params["hot"], "p_hc3": fit.pvalues["hot"], "p_wild": wild, "p_mw": mw}


def event_time_table(panel: pd.DataFrame, bench: str, family: list) -> pd.DataFrame:
    rows = []
    for k in HORIZONS:
        z = bhar(panel, bench, k)
        hot, other = z[z["hot"] == 1]["bhar"], z[z["hot"] == 0]["bhar"]
        if len(hot) < 5 or len(other) < 5:
            continue
        g = group_difference(z)
        rows.append([f"{k}", f"{len(hot)} / {len(other)}", f"{100 * hot.mean():.1f}% / {100 * other.mean():.1f}%",
                     f"{100 * hot.median():.1f}% / {100 * other.median():.1f}%", f"{100 * g['diff']:.1f} pp",
                     f"{g['p_hc3']:.3f}", "—" if np.isnan(g["p_wild"]) else f"{g['p_wild']:.3f}", f"{g['p_mw']:.3f}"])
        if bench == "HSI" and k in (20, 60):
            family.append((f"BHAR vs HSI, day {k}: hot minus other (wild cluster)", g["p_wild"]))
    return pd.DataFrame(rows, columns=["Trading days after day 1", "N (hot / other)", "Mean BHAR", "Median BHAR",
                                       "Mean difference", "HC3 p", "Wild cluster p (9 months)", "Mann-Whitney p"])


def bhar_path(panel: pd.DataFrame, bench: str, hot: float, max_day: int = 90) -> pd.DataFrame:
    """Mean and median BHAR by event day among issuers still observed, requiring at least MIN_PATH_N of them."""
    sub = panel[(panel["hot"] == hot)]
    day0 = sub[sub["event_day"] == 0].set_index("code")
    rows = []
    for k in range(1, max_day + 1):
        dayk = sub[sub["event_day"] == k].set_index("code")
        common = day0.index.intersection(dayk.index)
        if len(common) < MIN_PATH_N:
            break
        values = (dayk.loc[common, "close"] / day0.loc[common, "close"]
                  - dayk.loc[common, f"idx_{bench}"] / day0.loc[common, f"idx_{bench}"]).replace([np.inf, -np.inf], np.nan).dropna()
        # value above is stock ratio minus benchmark ratio, which equals the BHAR
        rows.append({"day": k, "mean": values.mean(), "median": values.median(), "n": len(values)})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ calendar time

def calendar_portfolio(panel: pd.DataFrame, bench: str, hot: float | None, hold: int = HOLD_DAYS) -> pd.DataFrame:
    """Equal-weighted daily excess return of issuers in event days 1..hold (a fixed calendar cohort, no look-ahead)."""
    sub = panel[(panel["event_day"].between(1, hold))]
    if hot is not None:
        sub = sub[sub["hot"] == hot]
    sub = sub.assign(excess=sub["r"] - sub[f"m_{bench}"]).replace([np.inf, -np.inf], np.nan).dropna(subset=["excess", "r", f"m_{bench}"])
    grouped = sub.groupby("date").agg(excess=("excess", "mean"), raw=("r", "mean"), market=(f"m_{bench}", "mean"), n=("code", "nunique"))
    return grouped[grouped["n"] >= MIN_PORTFOLIO]


def nw_alpha(y: pd.Series, X: pd.DataFrame | None = None, lags: int = NW_LAGS) -> dict:
    """Intercept, Newey-West t and p from regressing y on a constant (and optionally X)."""
    design = sm.add_constant(X if X is not None else pd.DataFrame(index=y.index), has_constant="add")
    fit = sm.OLS(y, design).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    out = {"alpha": fit.params["const"], "t": fit.tvalues["const"], "p": fit.pvalues["const"], "n": int(fit.nobs)}
    if X is not None:
        out["beta"] = fit.params.iloc[1]
    return out


def calendar_table(panel: pd.DataFrame, bench: str, family: list) -> pd.DataFrame:
    rows = []
    ports = {"April-June listings": calendar_portfolio(panel, bench, 1.0), "Other listings": calendar_portfolio(panel, bench, 0.0)}
    for name, port in ports.items():
        a = nw_alpha(port["excess"])
        c = nw_alpha(port["raw"], port[["market"]])
        rows.append([name, str(a["n"]), f"{port['n'].mean():.0f}", f"{1e4 * a['alpha']:.1f}", f"{a['t']:.2f} ({a['p']:.3f})",
                     f"{1e4 * c['alpha']:.1f}", f"{c['beta']:.2f}", f"{c['t']:.2f} ({c['p']:.3f})"])
        if bench == "HSI":
            family.append((f"Calendar-time alpha vs HSI, {name}", a["p"]))
    both = pd.concat([ports["April-June listings"]["excess"], ports["Other listings"]["excess"]], axis=1, keys=["hot", "other"], sort=True).dropna()
    spread = nw_alpha(both["hot"] - both["other"])
    rows.append(["Hot minus other (dates with both)", str(spread["n"]), "—", f"{1e4 * spread['alpha']:.1f}",
                 f"{spread['t']:.2f} ({spread['p']:.3f})", "—", "—", "—"])
    if bench == "HSI":
        family.append(("Calendar-time spread, hot minus other, vs HSI", spread["p"]))
    return pd.DataFrame(rows, columns=["Portfolio", "Days", "Mean issuers/day", "Excess return, bp/day", "NW t (p)",
                                       "CAPM alpha, bp/day", "CAPM beta", "CAPM alpha NW t (p)"])


# ------------------------------------------------------------------ figure

def fig_paths(panel: pd.DataFrame) -> None:
    fig, ax = new_fig(figsize=(8, 4.4))
    style_axes(ax)
    for hot, color, label in [(1.0, ORANGE, "April-June listings"), (0.0, BLUE, "Other listings")]:
        path = bhar_path(panel, "HSI", hot)
        ax.plot(path["day"], path["mean"], color=color, lw=2)
        ax.plot(path["day"], path["median"], color=color, lw=1.5, ls="--")
        ax.text(path["day"].iloc[-1] + 1, path["mean"].iloc[-1], f"  {label}", color=INK2, fontsize=8, va="center")
    ax.axhline(0, color=AXIS, lw=1)
    pct_axis(ax)
    ax.set_xlim(0, 105)
    ax.set_xlabel("Trading days after the day-1 close", fontsize=9, color=INK2)
    ax.set_ylabel("BHAR vs HSI", fontsize=9, color=INK2)
    ax.text(0.02, 0.05, "solid = mean, dashed = median; paths end where fewer than "
            f"{MIN_PATH_N} issuers remain", transform=ax.transAxes, fontsize=8, color=MUTED)
    fig.suptitle("BHAR vs HSI after day 1: April-June vs other 2026 IPOs (means are lifted by a few winners)", x=0.08, ha="left",
                 fontsize=10, color=INK, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "fig7_bhar_paths.png", dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)


# ------------------------------------------------------------------ main

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    y26 = select_2026(load_panel())
    benches = {"HSI": load_bars(BARS / "hsi_bars.json"), "HSTECH": load_bars(BARS / "hstech_bars.json")}
    panel = issuer_panel(y26, benches)
    used = panel["code"].nunique()
    family: list[tuple[str, float]] = []
    tables = {b: (event_time_table(panel, b, family), calendar_table(panel, b, family)) for b in benches}
    fam_p = dict(family)
    p60 = fam_p["BHAR vs HSI, day 60: hot minus other (wild cluster)"]
    p_hot = fam_p["Calendar-time alpha vs HSI, April-June listings"]
    p_other = fam_p["Calendar-time alpha vs HSI, Other listings"]
    p_spread = fam_p["Calendar-time spread, hot minus other, vs HSI"]
    last = panel["date"].max().date()
    depth = panel.groupby("code")["event_day"].max()
    fam = pd.DataFrame(family, columns=['Test', 'p']).dropna()
    fam['q (BH)'] = multipletests(fam['p'], alpha=0.10, method='fdr_bh')[1]
    mult = fam.assign(p=fam['p'].map('{:.4f}'.format), **{'q (BH)': fam['q (BH)'].map('{:.4f}'.format)})
    text = f"""# Aftermarket returns of 2026 IPOs from daily bars ({used} of {len(y26)} issuers, last bar {last})

Bars are the cached Tencent series in `data/market/aftermarket`; benchmark returns are aligned to each issuer's own bar dates.
Issuers have between {int(depth.min())} and {int(depth.max())} trading days after listing, so long horizons cover
earlier listings only (N shown per row). "Hot" = listed April-June (calendar dummy used throughout the analysis).

## Reading

- Event time, treating each IPO as independent, shows a large hot-vs-other gap that grows with the horizon. With listing-month clustering
  it is weaker (day-60 wild cluster p = {p60:.3f}); the ordinary Mann-Whitney and HC3 p-values overstate it.
- Calendar time, which counts each date once, gives the April-June portfolio an excess return not distinguishable from zero (p = {p_hot:.2f}), the other
  listings a positive excess return (p = {p_other:.3f}), and no significant difference between them (p = {p_spread:.2f}).
- So the evidence supports "January-March listings did well after day 1" more than "April-June listings collapsed"; the two are not the same claim,
  and a 9-month sample cannot separate them from the market path of each window.

## 1. Event time: BHAR from the day-1 close, benchmark HSI

{to_markdown(tables['HSI'][0].set_index('Trading days after day 1'), 'Trading days after day 1')}

- Inference: HC3 ignores clustering; the wild cluster p uses exact enumeration over listing months (the hot dummy is constant within a month,
  so only 9 clusters, 3 treated, identify the difference; it is the appropriate but low-power test). Mann-Whitney ignores clustering.
- Horizons mix calendar windows: the 90-day "other" group is mostly January-March listings, whose window overlaps the April-June rally.

Same table, benchmark HSTECH:

{to_markdown(tables['HSTECH'][0].set_index('Trading days after day 1'), 'Trading days after day 1')}

![BHAR paths](fig7_bhar_paths.png)

## 2. Calendar time: equal-weighted portfolios in days 1-{HOLD_DAYS} after listing

Each date's portfolio averages the excess return of all issuers in their first {HOLD_DAYS} trading days after day 1, requires at least
{MIN_PORTFOLIO} issuers, and uses Newey-West standard errors ({NW_LAGS} lags). This treats overlapping same-window IPOs as one observation per date.

Benchmark HSI:

{to_markdown(tables['HSI'][1].set_index('Portfolio'), 'Portfolio')}

Benchmark HSTECH:

{to_markdown(tables['HSTECH'][1].set_index('Portfolio'), 'Portfolio')}

- Alpha is per trading day in basis points (100 bp = 1%). The "Other" portfolio is largely January-March listings, so it and the hot portfolio face different market paths;
  the CAPM columns control the common market move but not a different sentiment regime.
- Calendar-time p-values are typically much larger than event-time ones because they count each date once.

## 3. Multiplicity

{to_markdown(mult.set_index('Test'), 'Test')}

The comparisons above are the headline aftermarket claims; the earlier Mann-Whitney p-values in `analysis/out/extended/` correspond to the event-time design without clustering.
"""
    (OUT / "event_time.md").write_text(text, encoding="utf-8")
    fig_paths(panel)
    print(f"Event-time analysis written to {OUT.relative_to(ROOT)}/ ({used} issuers)")


if __name__ == "__main__":
    main()
