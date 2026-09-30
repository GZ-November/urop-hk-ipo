"""A+H issuers: the H-share offer discount to the A-share price, and what follows.

Uses the A-share reference prices collected by `tools/external/ah_reference.py` (raw A-share closes, CNY/HKD, CSI 300)
for the 34 A+H issuers listed in 2026. Four questions:

  1. How large is the discount at the offer and at the day-1 close, and does a deeper discount go with a higher
     first-day return? The two gaps use different A-share prices (closing-date vs listing-day close), so they are not
     linked by an exact identity; the A-share price can move between the two dates.
  2. Determinants of the offer discount (A-share momentum, size, listing window).
  3. Convergence: the daily H/A price gap over the first 60 trading days, and H-share returns measured against the
     issuer's own A share instead of the index.
  4. A-share reaction: CSI 300-adjusted A-share returns around the H-share subscription close and listing day, with the same
     placebo calibration as the lockup study.

Only 2026 listings; N = 34, so every result is exploratory.

Outputs (analysis/out/ah_anchor/): ah_anchor.md, fig9_ah_anchor.png.

Usage:
    python3 analysis/ah_anchor_2026.py
"""

from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

import academic_extensions_2026 as ac
import extended_analysis_2026 as ext
from module_a_stylized_facts import AXIS, BLUE, INK, INK2, MUTED, ORANGE, ROOT, load_panel, new_fig, pct_axis, select_2026, style_axes, to_markdown

OUT = ROOT / "analysis" / "out" / "ah_anchor"
REFERENCE = ROOT / "pipeline" / "exports" / "HKIPO-2026-AH-reference.csv"
CACHE = ROOT / "pipeline" / "prospectus_pipeline" / "data" / "market" / "ah_reference"
HORIZONS = (5, 20, 40, 60)


# ------------------------------------------------------------------ data

def load_series(path) -> pd.Series:
    bars = json.loads(path.read_text(encoding="utf-8"))
    return pd.Series({pd.Timestamp(b["date"]): float(b["close"]) for b in bars}).sort_index()


def build_frame(y26: pd.DataFrame) -> pd.DataFrame:
    """One row per A+H issuer: extended-analysis variables plus the collected anchors."""
    d = ac.build_frame(y26)
    ref = pd.read_csv(REFERENCE)
    ref = ref.rename(columns={"h_code": "code"})
    out = d[d["ah"] == 1].merge(ref[["code", "a_symbol", "offer_vs_a_close", "offer_vs_a_pricing", "h_day1_close_vs_a", "a_date_close", "plausible"]], on="code", how="left", validate="one_to_one")
    out["disc"] = out["offer_vs_a_close"]
    out["disc10"] = out["disc"] * 10          # per 10 percentage points of offer premium (+) or discount (-)
    out["a_mom20"] = np.nan
    for i, row in out.iterrows():
        if pd.isna(row["a_symbol"]) or pd.isna(row["a_date_close"]):
            continue
        bars = load_series(CACHE / "a_bars" / f"{row['a_symbol']}.json")
        end = pd.Timestamp(row["a_date_close"])
        window = bars[bars.index <= end].iloc[-21:]
        if len(window) == 21:
            out.loc[i, "a_mom20"] = window.iloc[-1] / window.iloc[0] - 1
    return out


def premium_panel(d: pd.DataFrame, fx: pd.Series) -> pd.DataFrame:
    """Daily H-share price relative to the converted A-share price, event day 0 = H listing day."""
    rows = []
    for _, r in d.iterrows():
        if pd.isna(r["a_symbol"]):
            continue
        h = load_series(CACHE / "h_bars" / f"hk{r['code'].split('.')[0].zfill(5)}.json")
        h = h[h.index >= pd.Timestamp(r["ld"])]
        a = load_series(CACHE / "a_bars" / f"{r['a_symbol']}.json")
        frame = pd.DataFrame({"h": h}).join(a.rename("a"), how="inner")   # dates on which both markets traded
        frame["fx"] = fx.reindex(frame.index, method="ffill", tolerance=pd.Timedelta(days=7))
        frame["a_hkd"] = frame["a"] * frame["fx"]
        frame["gap"] = frame["h"] / frame["a_hkd"] - 1
        frame["event_day"] = [int((h.index <= t).sum()) - 1 for t in frame.index]   # position on the H-share calendar
        frame["code"], frame["hot"], frame["month"] = r["code"], r["hot"], str(pd.Timestamp(r["ld"]).to_period("M"))
        rows.append(frame.reset_index(names="date"))
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=["code", "event_day", "gap"])


def balanced_path(panel: pd.DataFrame, horizon: int = 60) -> pd.DataFrame:
    """Hold issuer composition fixed across a path; do not fill cross-market holidays."""
    valid = panel.dropna(subset=["gap"])
    codes = set(valid.loc[valid["event_day"] == 0, "code"]) & set(valid.loc[valid["event_day"] == horizon, "code"])
    return valid[valid["code"].isin(codes) & valid["event_day"].between(0, horizon)].groupby("event_day")["gap"].agg(["mean", "median", "count"])


def gap_change(panel: pd.DataFrame, k: int) -> pd.DataFrame:
    """Change in the H/A gap from listing day to event day k, and H return minus own-A-share return over the same span."""
    p0 = panel[panel["event_day"] == 0].set_index("code")
    pk = panel[panel["event_day"] == k].set_index("code")
    common = p0.index.intersection(pk.index)
    out = pd.DataFrame({
        "gap0": p0.loc[common, "gap"], "gapk": pk.loc[common, "gap"],
        "rel_a": (pk.loc[common, "h"] / p0.loc[common, "h"]) - (pk.loc[common, "a_hkd"] / p0.loc[common, "a_hkd"]),
        "hot": p0.loc[common, "hot"], "month": p0.loc[common, "month"]})
    out["dgap"] = out["gapk"] - out["gap0"]
    return out.dropna()


# ------------------------------------------------------------------ A-share reaction

def market_residuals(frame: pd.DataFrame, event) -> tuple[pd.Series, dict]:
    """Estimate alpha/beta on A trading bars [-120,-21], with at least 60 matched returns."""
    position = frame.index.searchsorted(pd.Timestamp(event))
    training = frame.iloc[max(0, position - 120):max(0, position - 20)].dropna(subset=["r", "market"])
    meta = {"n_estimation": len(training), "alpha": np.nan, "beta": np.nan}
    if len(training) < 60:
        return pd.Series(np.nan, index=frame.index), meta
    x = np.column_stack([np.ones(len(training)), training["market"]])
    if np.linalg.matrix_rank(x) < 2:
        return pd.Series(np.nan, index=frame.index), meta
    alpha, beta = np.linalg.lstsq(x, training["r"], rcond=None)[0]
    meta.update(alpha=alpha, beta=beta)
    return frame["r"] - alpha - beta * frame["market"], meta


def a_share_frames(d: pd.DataFrame, events: pd.Series | None = None) -> dict[str, pd.DataFrame]:
    """Per-issuer frames whose `ex_hsi` column is the A-share return minus the CSI 300 return (name reused by the event study)."""
    csi = load_series(CACHE / "csi300.json")
    frames = {}
    estimates = []
    for _, r in d.iterrows():
        if pd.isna(r["a_symbol"]):
            continue
        a = load_series(CACHE / "a_bars" / f"{r['a_symbol']}.json")
        frame = pd.DataFrame({"r": a.pct_change(fill_method=None), "turnover": np.nan})
        frame["market"] = csi.reindex(a.index).pct_change(fill_method=None)
        frame["ex_hsi"] = frame["r"] - frame["market"]
        if events is not None:
            event = events.get(r["code"])
            if pd.isna(event):
                continue
            frame["ex_hsi"], meta = market_residuals(frame, event)
            estimates.append({"code": r["code"], "event": event, **meta})
        frame["ex_hstech"] = frame["ex_hsi"]
        frames[r["code"]] = frame
    if events is not None:
        name = events.name or "event"
        pd.DataFrame(estimates).to_csv(OUT / f"market_model_{name}_estimates.csv", index=False)
    return frames


# ------------------------------------------------------------------ report

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    y26 = select_2026(load_panel())
    d = build_frame(y26)
    fx = load_series(CACHE / "fx_cnyhkd.json")
    family: list[tuple[str, str, float]] = []

    # 1. discounts
    rows = []
    for name, part in [("All A+H", d), ("April-June", d[d["hot"] == 1]), ("Other months", d[d["hot"] == 0])]:
        rows.append([name, str(len(part)), f"{100 * part['disc'].mean():.1f}%", f"{100 * part['disc'].median():.1f}%",
                     f"{100 * part['h_day1_close_vs_a'].mean():.1f}%", f"{100 * part['ir'].mean():.1f}%", f"{100 * part['ir'].median():.1f}%"])
    disc = pd.DataFrame(rows, columns=["Sample", "N", "Offer vs A (mean)", "Offer vs A (median)", "Day-1 close vs A (mean)", "Mean IR", "Median IR"])
    t_close = stats.ttest_rel(d["h_day1_close_vs_a"], d["disc"], nan_policy="omit")
    hot_diff = ext.ols_focus(d.assign(y=d["disc"]), "y", ["hot"], "hot")
    family.append(("Discount", "Offer discount differs between April-June and other listings (HC3)", hot_diff["p"]))
    family.append(("Discount", "Day-1 close discount is smaller than offer discount (paired t)", float(t_close.pvalue)))

    # 2. IR on offer discount
    specs = [("Offer discount only", ["disc10"]), ("+ April-June window", ["disc10", "hot"]), ("+ window + ln size", ["disc10", "hot", "lproc"])]
    reg_rows = []
    for label, xs in specs:
        r = ext.ols_focus(d, "y", xs, "disc10")
        reg_rows.append([label, f"{r['b']:.3f}{ext.stars(r['p'])} ({r['se']:.3f})", f"{r['p']:.3f}", "—" if np.isnan(r["p_wild"]) else f"{r['p_wild']:.3f}", str(r["n"])])
        if label.startswith("+ April"):
            family.append(("Discount", "Offer discount -> log(1 + IR), window-adjusted (HC3)", r["p"]))
    ok = d[d["plausible"] == 1]
    r_ok = ext.ols_focus(ok, "y", ["disc10", "hot"], "disc10")
    reg_rows.append(["+ window, drop implausible anchors", f"{r_ok['b']:.3f}{ext.stars(r_ok['p'])} ({r_ok['se']:.3f})", f"{r_ok['p']:.3f}", "—" if np.isnan(r_ok["p_wild"]) else f"{r_ok['p_wild']:.3f}", str(r_ok["n"])])
    reg = pd.DataFrame(reg_rows, columns=["Specification", "Coefficient per +10 pp of offer premium (HC3 s.e.)", "HC3 p", "Wild cluster p", "N"])
    rho = stats.spearmanr(d["disc"], d["ir"])
    family.append(("Discount", "Offer discount vs IR, Spearman", float(rho.pvalue)))

    # 3. determinants of the discount
    det_rows = []
    for label, x in [("A-share 20-day return before the offer", "a_mom20"), ("April-June window", "hot"), ("ln offer size", "lproc")]:
        r = ext.ols_focus(d, "disc", ["a_mom20", "hot", "lproc"], x)
        det_rows.append([label, f"{100 * r['b']:.2f}{ext.stars(r['p'])} ({100 * r['se']:.2f})", f"{r['p']:.3f}", "—" if np.isnan(r["p_wild"]) else f"{r['p_wild']:.3f}", str(r["n"])])
        if x == "a_mom20":
            family.append(("Discount", "A-share momentum -> offer discount (HC3)", r["p"]))
    det = pd.DataFrame(det_rows, columns=["Regressor", "Coefficient, pp of discount per unit (HC3 s.e.)", "HC3 p", "Wild cluster p", "N"])

    # 4. convergence
    panel = premium_panel(d, fx)
    panel.to_csv(OUT / "premium_panel.csv", index=False)
    balanced_path(panel).to_csv(OUT / "balanced_path_60.csv")
    pd.DataFrame([{ "horizon": k, "matched_issuers": len(gap_change(panel, k)), "sample_issuers": len(d)} for k in (0, *HORIZONS)]).to_csv(OUT / "horizon_coverage.csv", index=False)
    conv_rows = []
    for k in HORIZONS:
        z = gap_change(panel, k)
        if len(z) < 8:
            continue
        t = stats.ttest_1samp(z["dgap"], 0)
        w = stats.wilcoxon(z["dgap"])
        conv_rows.append([str(k), str(len(z)), f"{100 * z['gap0'].mean():.1f}%", f"{100 * z['gapk'].mean():.1f}%", f"{100 * z['dgap'].mean():.1f} pp",
                          f"{t.pvalue:.3f}", f"{w.pvalue:.3f}", f"{100 * z['rel_a'].mean():.1f}%", f"{100 * z['rel_a'].median():.1f}%"])
        if k in (20, 60):
            family.append(("Convergence", f"H/A gap changes from day 0 to day {k} (Wilcoxon)", float(w.pvalue)))
    conv = pd.DataFrame(conv_rows, columns=["Trading days after listing", "N", "Mean gap, day 0", "Mean gap, day k", "Mean change",
                                            "t p", "Wilcoxon p", "H minus own A return, mean", "H minus own A return, median"])

    # 5. A-share reaction
    frames = a_share_frames(d)
    events = d.set_index("code")
    sub_close = pd.Series(pd.to_datetime(y26.set_index("Stock Code")["Subscription closing date"]).reindex(events.index))
    listing = events["ld"]
    listing.name = "listing"
    sub_close.name = "subscription_close"
    react_close = ac.study_event(frames, sub_close)
    react_list = ac.study_event(frames, listing)
    beta_close = ac.study_event(a_share_frames(d, sub_close), sub_close)
    beta_list = ac.study_event(a_share_frames(d, listing), listing)
    beta_close = beta_close[~beta_close["Window"].str.startswith("Turnover")]
    beta_list = beta_list[~beta_list["Window"].str.startswith("Turnover")]
    for label, tab in (("subscription close", beta_close), ("H listing day", beta_list)):
        row = tab[tab["Window"] == "[-1,+1]"]
        if len(row):
            family.append(("A-share reaction", f"Market-model CAR [-1,+1] around {label} (placebo)", float(row["Placebo p"].iloc[0])))
    for label, tab in (("subscription close", react_close), ("H listing day", react_list)):
        row = tab[tab["Window"] == "[-1,+1]"]
        if len(row):
            family.append(("A-share reaction", f"A-share CAR [-1,+1] around {label} (placebo)", float(row["Placebo p"].iloc[0])))
    react_close = react_close[~react_close["Window"].str.startswith("Turnover")]
    react_list = react_list[~react_list["Window"].str.startswith("Turnover")]

    fam = ext.bh_family(family)
    text = f"""# A+H issuers: offer discount to the A-share price (N = {len(d)} issuers listed in 2026)

Data: `tools/external/ah_reference.py` (raw A-share closes from Tencent, CNY/HKD from Yahoo, CSI 300). A-share reference = close on the last A-share trading day
on or before the H-share subscription closing date; the price is converted to HKD with that day's exchange rate. Anchors are matched to issuers by A/H short name
(one manual override, 2768.HK); {int((d['plausible'] == 0).sum())} issuer(s) fall outside a plausible +/-60% band and are flagged (`plausible = 0`); robustness drops them.
The day-1 gap uses the A-share close on the H listing day, so it also reflects A-share moves between the two dates.

## 1. The discount

{to_markdown(disc.set_index('Sample'), 'Sample')}

- Offer vs A is negative for {int((d['disc'] < 0).sum())} of {len(d)} issuers: H shares are priced below the A-share close on average, and the discount is
  {'smaller' if abs(d['h_day1_close_vs_a'].mean()) < abs(d['disc'].mean()) else 'not smaller'} at the day-1 close (paired t p = {t_close.pvalue:.3f}). This comparison also includes A-share and FX moves between anchor dates.
- April-June listings vs others: difference in the offer discount = {100 * hot_diff['b']:.1f} pp (HC3 p = {hot_diff['p']:.3f}).

## 2. Does the offer discount go with the first-day return?

Rank correlation of offer premium with IR: rho = {rho.statistic:.2f} (p = {rho.pvalue:.3f}). Outcome log(1 + IR):

{to_markdown(reg.set_index('Specification'), 'Specification')}

- A negative coefficient means a deeper discount goes with a higher first-day return; this association alone does not identify convergence.
- N = {len(d)} and {d['month'].nunique()} listing months; treat as directional.

## 3. What explains the size of the discount

{to_markdown(det.set_index('Regressor'), 'Regressor')}

A-share momentum is the 20-trading-day A-share return up to the anchor date. The coefficient is in percentage points of offer premium per unit (100 pp) of A-share return.

## 4. Convergence with the A share after listing

H/A gap = H close / (A close x CNY/HKD) - 1 on days when both markets traded; day 0 is the H listing day. "H minus own A return" is the H-share buy-and-hold return
from the day-0 close minus the A-share's return (in HKD) over the same dates: an abnormal return against the issuer's own A share.

{to_markdown(conv.set_index('Trading days after listing'), 'Trading days after listing')}

`horizon_coverage.csv` records matched issuers at every reported horizon. `balanced_path_60.csv` and the figure hold the cohort fixed to issuers
with valid day-0 and day-60 pairs. On cross-market holidays the daily count can still fall; prices are not carried forward.
The daily premium panel uses raw H and A prices from Tencent. Adjusted H caches cannot be divided by raw A prices after a share split.
Nonsignificant gap changes are inconclusive, rather than evidence that convergence is absent.

## 5. The A-share reaction to the H-share issue (A-share return minus CSI 300)

Same placebo calibration as the lockup study (placebo days within {ac.PLACEBO_NEAR} bars of the event, cross-sectional t against the placebo t-distribution).
The CSI 300 benchmark does not match each stock's beta or sector (the issuers are mostly technology manufacturers), which is why placebo days from the same stock
are the relevant comparison rather than zero.

Around the subscription closing date:

{to_markdown(ac.format_events(react_close), 'Window') if len(react_close) else 'Too few events.'}

Around the H listing day:

{to_markdown(ac.format_events(react_list), 'Window') if len(react_list) else 'Too few events.'}

Sensitivity to pre-event alpha/beta: OLS on A trading bars [-120,-21], minimum 60 matched returns. Parameters are estimated separately
for subscription-close and listing events and held fixed in the event/placebo windows. This does not provide sector matching or causal identification.

Around subscription close (market model):

{to_markdown(ac.format_events(beta_close), 'Window') if len(beta_close) else 'Too few events.'}

Around H listing (market model):

{to_markdown(ac.format_events(beta_list), 'Window') if len(beta_list) else 'Too few events.'}

## 6. Multiplicity

{to_markdown(fam.assign(p=fam['p'].map('{:.4f}'.format), **{'q (BH)': fam['q (BH)'].map('{:.4f}'.format)}).set_index('Rank')[['Section', 'Test', 'p', 'q (BH)']], 'Rank')}

Limits: 34 issuers; the offer anchor uses the closing-date A-share price (pricing dates are missing for several issuers; the pre-pricing anchor is in the CSV where available);
CNY/HKD is a daily close rather than the rate at the pricing time; raw A-share prices are not adjusted for dividends inside the window.
"""
    (OUT / "ah_anchor.md").write_text(text, encoding="utf-8")
    fig_anchor(d, panel)
    print(f"A+H anchor analysis written to {OUT.relative_to(ROOT)}/ (N = {len(d)})")


def fig_anchor(d: pd.DataFrame, panel: pd.DataFrame) -> None:
    fig, (left, right) = new_fig(1, 2, figsize=(10, 4))
    for ax in (left, right):
        style_axes(ax)
    for hot, color, label in [(0.0, BLUE, "Other months"), (1.0, ORANGE, "April-June")]:
        part = d[d["hot"] == hot]
        left.scatter(part["disc"], part["ir"], s=26, color=color, alpha=0.8, linewidths=0, label=label)
    left.axhline(0, color=AXIS, lw=1)
    left.axvline(0, color=AXIS, lw=1)
    left.legend(frameon=False, fontsize=8, labelcolor=INK2)
    left.set_xlabel("H offer price vs A-share close (in HKD)", fontsize=8, color=INK2)
    left.set_ylabel("H first-day return", fontsize=8, color=INK2)
    pct_axis(left)
    pct_axis(left, "x")
    path = balanced_path(panel)
    right.plot(path.index, path["mean"], color=BLUE, lw=2)
    right.plot(path.index, path["median"], color=BLUE, lw=1.5, ls="--")
    right.axhline(0, color=AXIS, lw=1)
    right.set_xlabel("Trading days after H listing (both markets open)", fontsize=8, color=INK2)
    right.set_ylabel("H price vs A price", fontsize=8, color=INK2)
    right.text(0.02, 0.93, "fixed day-0/day-60 cohort; mean / median", transform=right.transAxes, fontsize=8, color=MUTED)
    pct_axis(right)
    fig.suptitle("A+H issuers: discount to the A share at the offer, and its path after listing", x=0.01, ha="left", fontsize=10, color=INK, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "fig9_ah_anchor.png", dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    main()
