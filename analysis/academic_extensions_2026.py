"""Academic extensions on the 2026 HK IPO sample.

Five questions the earlier modules do not answer, each with a standard reference design:

  1. Money left on the table   Who captures it (cornerstone, other placees, retail)? How large is it
                               relative to underwriting fees (Loughran & Ritter 2002)? What does a retail
                               application actually earn?
  2. Underwriting fees         Commission-rate mass points and scale economies (Chen & Ritter 2000).
  3. Lockup and stabilization  Market-adjusted abnormal returns and turnover around the six-month lockup
                               expiry and the end of the stabilization period, calibrated with placebo
                               event dates drawn from the same issuers (Field & Hanka 2001; Ljungqvist et al. 2006).
  4. Partial adjustment        First-day return vs the offer-price revision inside the filing range (Hanley 1993).
  5. Sponsor effects           Do lead sponsors explain first-day returns beyond the listing window?

Only 2026 listings are used. All results are exploratory.

Outputs (analysis/out/academic/): money_left.md, fees.md, events.md, partial_adjustment.md,
sponsor.md, multiplicity.md, fig8_lockup_stabilization_car.png.

Usage:
    python3 analysis/academic_extensions_2026.py
"""

from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

import aftermarket_event_time_2026 as et
from shared import estimation as ext
from research_inputs import C as C, ROOT as ROOT, load_panel as load_panel, select_2026 as select_2026  # noqa: F401 — legacy C export
from shared.reporting import (
    AXIS, BLUE, INK, INK2, MUTED, new_fig, pct_axis, style_axes, to_markdown,
)

# Compatibility names for existing notebooks.
from research_inputs import FINAL_GLOBAL_SHARES as FG, prepare_academic as build_frame  # noqa: F401

OUT = ROOT / "analysis" / "out" / "academic"
SEED = 20260930
N_PLACEBO = 5000
WINDOWS = {"[-1,+1]": (-1, 1), "[0,+5]": (0, 5), "[-5,+5]": (-5, 5), "[-5,-1]": (-5, -1)}
PLACEBO_NEAR = 30             # placebo days come from within this many bars of the true event (similar volatility regime)
PLACEBO_EXCLUDE = 10          # ... but at least this far from it, so windows do not overlap


# ------------------------------------------------------------------ 1. money left on the table

def money_left_split(d: pd.DataFrame) -> dict:
    """Gains per HK$ share between offer and day-1 close, split by who holds the shares.

    Cornerstone = final cornerstone share of the base offer; retail = final public tranche after clawback;
    other placees = the remainder. MLOT is the day-1 gain on the base offer."""
    gain = d["close1"] - d["offer"]
    other = d["base_shares"] - d["retail_shares"] - d["corner_shares"]
    parts = {"Cornerstone investors": d["corner_shares"] * gain, "Other placees": other * gain, "Retail (public offer)": d["retail_shares"] * gain}
    shares = {"Cornerstone investors": d["corner_shares"], "Other placees": other, "Retail (public offer)": d["retail_shares"]}
    return {"gain": {k: v.sum() for k, v in parts.items()}, "shares": {k: v.sum() / d["base_shares"].sum() for k, v in shares.items()},
            "negative_other": int((other < 0).sum())}


def retail_profile(d: pd.DataFrame) -> pd.DataFrame:
    """Per-deal retail outcomes: allocation ratio, expected gain per HK$10,000 applied, gain per applicant.

    An allocation ratio outside (0, 1] is a unit/definition anomaly, not a measurement to clamp:
    it is quarantined (missing) and flagged in `alloc_quarantined` for review."""
    z = d.copy()
    raw = z["retail_shares"] / z["applied"]
    z["alloc_quarantined"] = raw.notna() & ~((raw > 0) & (raw <= 1))
    z["alloc"] = raw.where(~z["alloc_quarantined"])
    z["gain_10k"] = z["alloc"] * z["ir"] * 10_000
    z["gain_applicant"] = z["retail_shares"] * (z["close1"] - z["offer"]) / z["applicants"]
    return z


def money_left_section(d: pd.DataFrame, family: list) -> str:
    rows, splits = [], {}
    for name, part in [("All 2026", d), ("April-June listings", d[d["hot"] == 1]), ("Other listings", d[d["hot"] == 0])]:
        s = money_left_split(part)
        splits[name] = s
        total = part["mlot"].sum()
        fees = part["fee"].sum()
        rows.append([name, str(len(part)), f"{total / 1e9:.1f}", f"{fees / 1e9:.1f}", f"{total / fees:.1f}x",
                     f"{part.loc[part['mlot'] > 0, 'mlot'].sum() / 1e9:.1f}", f"{part.loc[part['mlot'] < 0, 'mlot'].sum() / 1e9:.1f}"])
    head = pd.DataFrame(rows, columns=["Sample", "N", "Net MLOT (HK$bn)", "Underwriting fees (HK$bn)", "MLOT / fees",
                                       "Gains on deals with IR > 0 (HK$bn)", "Losses on deals with IR < 0 (HK$bn)"])
    who = pd.DataFrame({
        name: {**{f"{k}: share of shares": f"{100 * s['shares'][k]:.1f}%" for k in s["shares"]},
               **{f"{k}: share of net MLOT": f"{100 * s['gain'][k] / sum(s['gain'].values()):.1f}%" for k in s["gain"]}}
        for name, s in splits.items()})
    rp = retail_profile(d)
    prof = rp.groupby("hot").agg(N=("ir", "size"), alloc_med=("alloc", "median"), gain_med=("gain_10k", "median"), gain_mean=("gain_10k", "mean"),
                                 neg=("gain_10k", lambda s: (s.dropna() < 0).mean()), app_mean=("gain_applicant", "mean"), app_med=("gain_applicant", "median"))
    prof.index = ["Other listings", "April-June listings"]
    prof_tab = pd.DataFrame({
        "N": prof["N"].astype(int),
        "Median allocation ratio": (100 * prof["alloc_med"]).map("{:.2f}%".format),
        "Expected gain per HK$10,000 applied, median": prof["gain_med"].map("HK${:.1f}".format),
        "Expected gain per HK$10,000 applied, mean": prof["gain_mean"].map("HK${:.1f}".format),
        "Deals with an expected loss": (100 * prof["neg"]).map("{:.0f}%".format),
        "Retail gain per applicant, median (HK$)": prof["app_med"].map("{:,.0f}".format),
        "Retail gain per applicant, mean (HK$)": prof["app_mean"].map("{:,.0f}".format)})
    total_all = sum(splits['All 2026']['gain'].values())
    corner_share_gain = splits["All 2026"]["gain"]["Cornerstone investors"] / sum(splits["All 2026"]["gain"].values())
    corner_share_sh = splits["All 2026"]["shares"]["Cornerstone investors"]
    retail_share_gain = splits["All 2026"]["gain"]["Retail (public offer)"] / sum(splits["All 2026"]["gain"].values())
    retail_share_sh = splits["All 2026"]["shares"]["Retail (public offer)"]
    fee_covered = float((d["mlot"] > d["fee"]).mean())
    med = d["mlot"] / d["fee"]
    corr = stats.spearmanr(d["ir"], d["fee"] / d["gross"], nan_policy="omit")
    partial = ext.ols_focus(d, "fee_rate_hk", ["y", "lproc", "hot", "ah"], "y")
    family.append(("Money left", "Commission rate vs log(1 + IR), controlling size, window, A+H (HC3)", partial["p"]))
    return f"""# Money left on the table, 2026 (N = {len(d)})

MLOT = (day-1 close - offer price) x base offer shares. Fees = the disclosed underwriting commission on HK and international proceeds
(discretionary incentive fees are not in the data and would add up to 1%).

{to_markdown(head.set_index('Sample'), 'Sample')}

- In aggregate the money left is {total_all / d['fee'].sum():.1f} times the fees paid; on {100 * fee_covered:.0f}% of deals the day-1 gain exceeds the underwriting fee.
  Median deal-level ratio is {med.median():.1f}x. Net figures hide {abs(float(head.iloc[0, 6])):.1f}bn of losses on deals that closed below the offer price.

## Who holds the gain

{to_markdown(who, '')}

- Cornerstone investors hold {100 * corner_share_sh:.1f}% of the base offer and capture {100 * corner_share_gain:.1f}% of net money left; retail holds {100 * retail_share_sh:.1f}% of the shares and captures {100 * retail_share_gain:.1f}%.
  Shares held and gains match closely because IR is a per-share return: the allocation, not the pricing, decides who benefits, and the public tranche is small.
- Fee rate (fees / proceeds) and IR: Spearman = {corr.statistic:.2f} (p = {corr.pvalue:.2f}). Small deals carry both higher fee rates and higher IR, so the raw correlation mostly
  reflects size: with ln size, the window and A+H held fixed, the commission-rate coefficient on log(1 + IR) is {100 * partial['b']:.3f} pp (HC3 p = {partial['p']:.2f}).

## What a retail application earns

Expected gain per HK$10,000 = allocation ratio (final public shares / valid applied shares, capped at 1) x IR x 10,000, assuming proportional allocation
(actual allocation is by lottery, so this is an expectation, not a typical outcome).

{to_markdown(prof_tab, '')}

- The typical application earns a few Hong Kong dollars per HK$10,000; the mean is driven by rare large allocations and losses on broken issues.
  Gain per applicant averages the retail gain over everyone who applied, winners and non-winners.
"""


# ------------------------------------------------------------------ 2. fees

def fee_section(d: pd.DataFrame, family: list) -> str:
    xs = ["lproc", "hot", "ah", "vc", "tier1", "corner", "fixed"]
    z = d.dropna(subset=["fee_rate_hk"] + xs).copy()
    counts = z["fee_rate_hk"].round(4).value_counts().head(8)
    top_share = counts.iloc[0] / len(z)
    labels = {"lproc": "ln offer size", "hot": "April-June window", "ah": "A+H issuer", "vc": "VC/PE-backed", "tier1": "Top-tier sponsor",
              "corner": "Cornerstone allocation", "fixed": "Fixed-price offer"}
    rows = []
    for x in xs:
        r = ext.ols_focus(z, "fee_rate_hk", xs, x)
        rows.append([labels[x], f"{100 * r['b']:.3f}{ext.stars(r['p'])} ({100 * r['se']:.3f})", f"{r['p']:.3f}",
                     "—" if np.isnan(r["p_wild"]) else f"{r['p_wild']:.3f}"])
        if x == "lproc":
            family.append(("Fees", "Scale economies: commission rate vs ln offer size (HC3)", r["p"]))
    tab = pd.DataFrame(rows, columns=["Regressor", "Coefficient, pp of proceeds (HC3 s.e.)", "HC3 p", "Wild cluster p"])
    fit = sm.OLS(z["fee_rate_hk"], sm.add_constant(z[xs].astype(float))).fit(cov_type="HC3")
    dist = pd.DataFrame({"Commission rate": [f"{100 * k:.2f}%" for k in counts.index], "Deals": counts.values,
                         "Share": [f"{100 * v / len(z):.0f}%" for v in counts.values]})
    return f"""# Underwriting commission rates, 2026 (N = {len(z)})

Outcome: disclosed underwriting commission on the HK offer, as a share of proceeds. The derived columns `Underwriting base commission rate`
and `Total underwriting fee rate` in the master are not used: the total equals 3.5% for 68 issuers and 1.00x% for the other 38 regardless of the disclosed
commission, so it does not follow from it (see docs/ACADEMIC_EXTENSIONS_2026.md).

## Distribution

{to_markdown(dist.set_index('Commission rate'), 'Commission rate')}

The most common single rate covers {100 * top_share:.0f}% of deals; unlike the U.S. 7% gross spread, no rate dominates.

## Determinants (OLS, one regression, {len(z)} deals, R-squared {fit.rsquared:.2f})

{to_markdown(tab.set_index('Regressor'), 'Regressor')}

- A negative size coefficient is the usual scale economy: a doubling of the offer (ln 2 = 0.69) changes the commission rate by {100 * fit.params['lproc'] * np.log(2):.2f} percentage points.
- Wild cluster p uses listing months (exact enumeration); with few clusters treat both p-values as indicative.
"""


# ------------------------------------------------------------------ 3. events

def load_event_frame(y26: pd.DataFrame, as_of: str | None = None) -> tuple[dict[str, pd.DataFrame], dict[str, pd.Series]]:
    """Per-issuer frames of excess returns (vs HSI and HSTECH) and turnover from the cached bars."""
    cutoff = (pd.Timestamp(as_of) if as_of else pd.Timestamp.now(tz="Asia/Hong_Kong").tz_localize(None)).normalize()
    hsi, hstech = et.load_bars(et.BARS / "hsi_bars.json"), et.load_bars(et.BARS / "hstech_bars.json")
    hsi, hstech = hsi.loc[:cutoff], hstech.loc[:cutoff]
    frames = {}
    for _, row in y26.iterrows():
        path = et.BARS / f"hk{row['Stock Code'].split('.')[0].zfill(5)}.json"
        if not path.exists():
            continue
        bars = [b for b in json.loads(path.read_text(encoding="utf-8")) if pd.Timestamp(b["date"]) <= cutoff]
        if not bars:
            continue
        close = pd.Series({pd.Timestamp(b["date"]): float(b["close"]) for b in bars}).sort_index()
        turnover = pd.Series({pd.Timestamp(b["date"]): b.get("turnover") for b in bars}, dtype=float).sort_index()
        if close.index[0] != row["listing_date"]:
            continue
        frame = pd.DataFrame({"r": close.pct_change(fill_method=None), "turnover": turnover})
        for name, bench in (("hsi", hsi), ("hstech", hstech)):
            frame[f"ex_{name}"] = frame["r"] - bench.reindex(close.index).pct_change(fill_method=None)
        frames[row["Stock Code"]] = frame
    return frames, {}


def window_car(frame: pd.DataFrame, event_idx: int, a: int, b: int, col: str = "ex_hsi") -> float:
    """Sum of excess returns over event days [a, b]; NaN if the window is incomplete or has missing returns."""
    lo, hi = event_idx + a, event_idx + b
    if lo < 1 or hi >= len(frame):
        return np.nan
    w = frame[col].iloc[lo:hi + 1]
    return float(w.sum()) if w.notna().all() else np.nan


def turnover_shock(frame: pd.DataFrame, event_idx: int) -> float:
    """log(mean turnover on event days [0, +5] / mean turnover on days [-25, -6]); NaN if either window is incomplete."""
    if event_idx - 25 < 0 or event_idx + 5 >= len(frame):
        return np.nan
    post = frame["turnover"].iloc[event_idx:event_idx + 6]
    pre = frame["turnover"].iloc[event_idx - 25:event_idx - 5]
    if post.isna().any() or pre.isna().any() or pre.mean() <= 0 or post.mean() <= 0:
        return np.nan
    return float(np.log(post.mean() / pre.mean()))


def event_index(frame: pd.DataFrame, date: pd.Timestamp) -> int | None:
    """Position of the first bar on or after the event date, if any bar exists then."""
    hits = np.flatnonzero(frame.index >= date)
    return int(hits[0]) if len(hits) else None


def cross_t(v: np.ndarray) -> float:
    """Cross-sectional t of the mean (standardizes by each sample's own dispersion, so event-induced variance does not inflate it)."""
    return float(v.mean() / (v.std(ddof=1) / np.sqrt(len(v)))) if len(v) > 1 and v.std(ddof=1) > 0 else 0.0


def placebo_p(stat_by_issuer: dict[str, np.ndarray], observed: dict[str, float], agg, n_draw: int = N_PLACEBO, seed: int = SEED) -> tuple[float, float]:
    """Observed cross-issuer statistic and two-sided placebo p.

    stat_by_issuer[code] holds the statistic for every admissible placebo event day of that issuer; each draw picks one per issuer."""
    codes = [c for c in observed if c in stat_by_issuer and len(stat_by_issuer[c])]
    obs = agg(np.array([observed[c] for c in codes]))
    rng = np.random.default_rng(seed)
    draws = np.array([agg(np.array([rng.choice(stat_by_issuer[c]) for c in codes])) for _ in range(n_draw)])
    return float(obs), float((1 + (np.abs(draws - np.median(draws)) >= abs(obs - np.median(draws))).sum()) / (n_draw + 1))


def placebo_grid(frame: pd.DataFrame, true_idx: int, fn) -> np.ndarray:
    """Statistic at every placebo event day within PLACEBO_NEAR bars, and more than PLACEBO_EXCLUDE bars, from the true event day.

    Newly listed stocks are far more volatile in their first weeks, so placebo days must sit near the true event day in event time;
    drawing them from the whole history would make the null distribution too narrow for early events such as stabilization end."""
    days = [k for k in range(max(6, true_idx - PLACEBO_NEAR), min(len(frame) - 6, true_idx + PLACEBO_NEAR) + 1) if abs(k - true_idx) > PLACEBO_EXCLUDE]
    vals = np.array([fn(frame, k) for k in days], dtype=float)
    return vals[~np.isnan(vals)]


def study_event(frames: dict, events: pd.Series, col: str = "ex_hsi") -> pd.DataFrame:
    """Rows per window: N, mean/median CAR, t, Wilcoxon p, placebo p; plus a turnover row."""
    idx = {c: event_index(frames[c], d) for c, d in events.dropna().items() if c in frames}
    idx = {c: i for c, i in idx.items() if i is not None}
    rows = []
    for name, (a, b) in WINDOWS.items():
        observed = {c: window_car(frames[c], i, a, b, col) for c, i in idx.items()}
        observed = {c: v for c, v in observed.items() if not np.isnan(v)}
        if len(observed) < 8:
            continue
        grid = {c: placebo_grid(frames[c], idx[c], lambda f, k, a=a, b=b: window_car(f, k, a, b, col)) for c in observed}
        _, p_placebo = placebo_p(grid, observed, cross_t)
        v = np.array(list(observed.values()))
        rows.append({"Window": name, "N": len(v), "Mean CAR": float(v.mean()), "Median CAR": float(np.median(v)),
                     "t": stats.ttest_1samp(v, 0).statistic, "Wilcoxon p": stats.wilcoxon(v).pvalue, "Placebo p": p_placebo,
                     "share < 0": float((v < 0).mean())})
    shock = {c: turnover_shock(frames[c], i) for c, i in idx.items()}
    shock = {c: v for c, v in shock.items() if not np.isnan(v)}
    if len(shock) >= 8:
        grid = {c: placebo_grid(frames[c], idx[c], turnover_shock) for c in shock}
        _, p_placebo = placebo_p(grid, shock, cross_t)
        v = np.array(list(shock.values()))
        rows.append({"Window": "Turnover [0,+5] vs [-25,-6], median log ratio", "N": len(v), "Mean CAR": float(v.mean()), "Median CAR": float(np.median(v)),
                     "t": stats.ttest_1samp(v, 0).statistic, "Wilcoxon p": stats.wilcoxon(v).pvalue, "Placebo p": p_placebo,
                     "share < 0": float((v < 0).mean())})
    return pd.DataFrame(rows)


def format_events(tab: pd.DataFrame) -> pd.DataFrame:
    out = tab.copy()
    is_turn = out["Window"].str.startswith("Turnover")
    for col in ("Mean CAR", "Median CAR"):
        out[col] = [f"{v:.2f}" if t else f"{100 * v:.1f}%" for v, t in zip(out[col], is_turn)]
    out["t"] = out["t"].map("{:.2f}".format)
    out["Wilcoxon p"] = out["Wilcoxon p"].map("{:.3f}".format)
    out["Placebo p"] = out["Placebo p"].map("{:.3f}".format)
    out["share < 0"] = (100 * out["share < 0"]).map("{:.0f}%".format)
    return out.set_index("Window")


def events_section(frames: dict, d: pd.DataFrame, family: list) -> tuple[str, dict]:
    events = d.set_index("code")
    lock = study_event(frames, events["lockup_date"])
    stab = study_event(frames, events["stab_end"])
    lock_tech = study_event(frames, events["lockup_date"], col="ex_hstech")
    stab_bought = study_event(frames, events.loc[events["stab"] == 1, "stab_end"])
    stab_not = study_event(frames, events.loc[events["stab"] == 0, "stab_end"])
    for label, tab in (("Six-month lockup expiry", lock), ("Stabilization end", stab)):
        row = tab[tab["Window"] == "[-5,+5]"]
        if len(row):
            family.append(("Events", f"{label}: CAR [-5,+5] vs HSI (placebo)", float(row["Placebo p"].iloc[0])))
    turn = lock[lock["Window"].str.startswith("Turnover")]
    if len(turn):
        family.append(("Events", "Six-month lockup expiry: turnover shock vs placebo days", float(turn["Placebo p"].iloc[0])))
    n_lock = int(lock["N"].max()) if len(lock) else 0
    return f"""# Lockup expiry and stabilization end, 2026 (HSI-adjusted, from cached daily bars)

Event day 0 is the first trading day on or after the event date; CAR is the sum of daily stock returns minus HSI returns over the window.
The **placebo p** re-draws one non-event day per issuer from the same issuer's own history, between {PLACEBO_EXCLUDE + 1} and {PLACEBO_NEAR} trading days from the true
event (so the volatility regime is similar), {N_PLACEBO} times. It calibrates drift and cross-issuer dependence that a plain t-test ignores.
The placebo compares the cross-sectional t-statistic of each draw with the observed one, so a window whose returns are unusually dispersed (event-induced variance) is not mistaken for a shifted mean.
Turnover rows compare mean turnover on days [0,+5] to days [-25,-6] (log ratio; 0 = no change).

## 1. Six-month lockup expiry (cornerstone unlock date, else controlling-shareholder date)

Only issuers listed early enough to have reached the expiry with a full window are included ({n_lock} at most, all listed January-March; 88 issuers share the same
cornerstone and controlling-shareholder date, so they are one event, not two).

{to_markdown(format_events(lock), 'Window')}

Robustness, HSTECH-adjusted:

{to_markdown(format_events(lock_tech), 'Window')}

## 2. End of the stabilization period

{to_markdown(format_events(stab), 'Window')}

Split by whether stabilizing purchases occurred (their number is small):

Purchases occurred:

{to_markdown(format_events(stab_bought), 'Window') if len(stab_bought) else 'Too few issuers with a full window.'}

No purchases:

{to_markdown(format_events(stab_not), 'Window') if len(stab_not) else 'Too few issuers with a full window.'}

- A negative pre-window on the lockup event ([-5,-1]) is the usual anticipation of selling pressure; the sign and size of [-5,+5] against the placebo distribution
  is the test. With about {n_lock} events from one listing quarter the power is limited.
- The placebo statistics are centred below zero: returns drift down and turnover decays as a new listing ages, so an ordinary window in the same weeks would
  show a negative average. That is why the placebo p can be much smaller than the plain t-test or Wilcoxon p (for example the stabilization-end [-5,+5] window has
  t about 1.9 but placebo p about 0.004): the window is unusual relative to the issuer's own neighbouring days, though a plain test against zero is only marginal.
- Stabilization end falls about 20 trading days after listing, exactly the Day-20 observation used elsewhere in this project, so this window also overlaps
  the post-listing decline that the hot-window comparison shows; the pre-window [-5,-1] is positive as well, which fits price support that lasts until the end.
- Lockup events include only January-March listings (N = 26 to 31), so they say nothing about April-June or later issuers.
""", {"lock": lock, "stab": stab}


def fig_events(frames: dict, d: pd.DataFrame) -> None:
    events = d.set_index("code")
    fig, axes = new_fig(1, 2, figsize=(10, 3.8), sharey=True)
    for ax, (col, title) in zip(axes, [("lockup_date", "Six-month lockup expiry"), ("stab_end", "Stabilization end")]):
        style_axes(ax)
        curves = []
        for code, date in events[col].dropna().items():
            if code not in frames:
                continue
            i = event_index(frames[code], date)
            if i is None or i - 10 < 1 or i + 10 >= len(frames[code]):
                continue
            ex = frames[code]["ex_hsi"].iloc[i - 10:i + 11]
            if ex.notna().all():
                curves.append(ex.to_numpy())
        if not curves:
            continue
        arr = np.array(curves)
        mean = arr.mean(axis=0).cumsum()
        lo = np.quantile(arr.cumsum(axis=1), 0.25, axis=0)
        hi = np.quantile(arr.cumsum(axis=1), 0.75, axis=0)
        x = np.arange(-10, 11)
        ax.fill_between(x, lo, hi, color=BLUE, alpha=0.15, linewidth=0)
        ax.plot(x, mean, color=BLUE, lw=2)
        ax.axhline(0, color=AXIS, lw=1)
        ax.axvline(0, color=MUTED, lw=1, ls="--")
        ax.set_title(f"{title} (n = {len(curves)})", fontsize=9, color=INK, loc="left", fontweight="bold")
        ax.set_xticks(range(-10, 11, 5))
        ax.set_xlabel("Trading days from event", fontsize=8, color=INK2)
        pct_axis(ax)
    axes[0].set_ylabel("Cumulative excess return vs HSI", fontsize=8, color=INK2)
    fig.suptitle("Cumulative market-adjusted return around two supply events (line = mean, band = interquartile range)", x=0.01, ha="left",
                 fontsize=10, color=INK, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "fig8_lockup_stabilization_car.png", dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)


# ------------------------------------------------------------------ 4. partial adjustment

def partial_adjustment_section(d: pd.DataFrame, family: list) -> str:
    z = d[(d["range_max"] > d["range_min"]) & d["revision"].notna()].copy()
    rho = stats.spearmanr(z["revision"], z["ir"])
    specs = [("Revision only", ["revision"]), ("+ April-June window", ["revision", "hot"]), ("+ window + A+H + ln size", ["revision", "hot", "ah", "lproc"])]
    rows = []
    for label, xs in specs:
        r = ext.ols_focus(z, "y", xs, "revision")
        rows.append([label, f"{r['b']:.2f}{ext.stars(r['p'])} ({r['se']:.2f})", f"{r['p']:.3f}", "—" if np.isnan(r["p_wild"]) else f"{r['p_wild']:.3f}", str(r["n"])])
        if label.startswith("+ April"):
            family.append(("Partial adjustment", "Offer-price revision -> IR, window-adjusted (HC3)", r["p"]))
    tab = pd.DataFrame(rows, columns=["Specification", "Revision coefficient (HC3 s.e.)", "HC3 p", "Wild cluster p", "N"])
    return f"""# Partial adjustment inside the filing range, 2026 (range deals only, N = {len(z)})

Revision = (offer price - midpoint of the filing range) / midpoint. Hanley (1993) predicts a positive relation between revision and first-day return:
information that raises demand lifts the price only partly. The 65 fixed-price deals have no range and are excluded, so this is a subsample of the deals
that are priced by bookbuilding, and the sample is small.

Rank correlation of revision with IR: rho = {rho.statistic:.2f} (p = {rho.pvalue:.3f}).

Outcome log(1 + IR):

{to_markdown(tab.set_index('Specification'), 'Specification')}

- Revision is negative when the offer is priced below the midpoint and positive when above; the coefficient is per unit (100 pp) of revision.
- {len(z)} observations and 9 listing months limit inference; treat as a directional check of the partial-adjustment idea, not an estimate to quote.
"""


# ------------------------------------------------------------------ 5. sponsor

def sponsor_section(d: pd.DataFrame, family: list) -> str:
    z = d.dropna(subset=["y", "sponsor", "hot", "ah", "lproc"]).copy()
    counts = z["sponsor"].value_counts()
    keep = counts[counts >= 3].index
    g = z[z["sponsor"].isin(keep)].copy()
    resid = sm.OLS(g["y"], sm.add_constant(g[["hot", "ah", "lproc"]].astype(float))).fit().resid
    icc_raw, f_raw, p_raw = ext.anova_icc(g["y"].to_numpy(), g["sponsor"].to_numpy())
    icc_res, f_res, p_res = ext.anova_icc(resid.to_numpy(), g["sponsor"].to_numpy())
    family.append(("Sponsor", "First-named sponsor effect on IR, after window, A+H and size (ANOVA permutation)", p_res))
    tab = g.groupby("sponsor").agg(N=("ir", "size"), mean_ir=("ir", "mean"), median_ir=("ir", "median"), hot=("hot", "mean")).sort_values("N", ascending=False)
    view = pd.DataFrame({"Deals": tab["N"], "Mean IR": (100 * tab["mean_ir"]).map("{:.0f}%".format), "Median IR": (100 * tab["median_ir"]).map("{:.0f}%".format),
                         "Share listed Apr-Jun": (100 * tab["hot"]).map("{:.0f}%".format)})
    return f"""# Sponsor effects, 2026

The first-named sponsor in the `Sponsor(s)` column is used as the lead-sponsor proxy: the `Lead sponsor name` column reads "CICC" for 92 of 106
issuers even when CICC is not among the sponsors, so it is unusable. Sponsors with at least 3 deals are compared ({len(keep)} sponsors, {len(g)} deals).

{to_markdown(view, 'First-named sponsor')}

| Statistic | Raw log(1 + IR) | After window, A+H and size |
|---|---|---|
| Intraclass correlation across sponsors | {icc_raw:.3f} | {icc_res:.3f} |
| ANOVA F (permutation p) | {f_raw:.2f} ({p_raw:.3f}) | {f_res:.2f} ({p_res:.3f}) |

- Sponsor differences in mean IR largely reflect when each sponsor's deals listed; the residual test asks whether anything remains once the listing window, A+H
  and size are removed. With few deals per sponsor and sponsors that often co-sponsor, a null result is weak evidence of no sponsor effect.
"""


# ------------------------------------------------------------------ main

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    y26 = select_2026(load_panel())
    d = build_frame(y26)
    frames, _ = load_event_frame(y26)
    family: list[tuple[str, str, float]] = []

    money = money_left_section(d, family)
    fees = fee_section(d, family)
    events, _ = events_section(frames, d, family)
    partial = partial_adjustment_section(d, family)
    sponsor = sponsor_section(d, family)
    mult = ext.bh_family(family)
    mult_text = ("# Multiplicity across the tests in this module\n\nBenjamini-Hochberg step-up at FDR 10%.\n\n"
                 + to_markdown(mult.assign(p=mult["p"].map("{:.4f}".format), **{"q (BH)": mult["q (BH)"].map("{:.4f}".format)})
                               .set_index("Rank")[["Section", "Test", "p", "q (BH)"]], "Rank")
                 + "\n\nThe family counts only tests reported here, not the exploration that chose them.\n")
    for name, text in [("money_left.md", money), ("fees.md", fees), ("events.md", events), ("partial_adjustment.md", partial),
                       ("sponsor.md", sponsor), ("multiplicity.md", mult_text)]:
        (OUT / name).write_text(text, encoding="utf-8")
    fig_events(frames, d)
    print(f"Academic extensions written to {OUT.relative_to(ROOT)}/ (N = {len(d)})")


if __name__ == "__main__":
    main()
