#!/usr/bin/env python3
"""Compare lifetime offered-tranche gains with the same dollars held in the Hang Seng Index.

Inputs are the verified terminal sample used for Table 8.2. The IPO leg is price-only
(Bloomberg "Offer To Date", split-adjusted). The benchmark is reported two ways because
IPO dividends are not observed: price-only HSI is like-for-like; HSI plus reinvested
dividends is deliberately demanding. Output: ext_table14c_wealth_vs_hsi_benchmark.csv.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent / "out"
EXT = ROOT / "overview_extensions"
ASOF = pd.Timestamp("2026-11-12")


def close_of(value) -> float:
    """Return the close from a cached HSI bar stored as a number, list or mapping."""
    if isinstance(value, dict):
        return value["close"]
    if isinstance(value, (list, tuple)):
        return value[1] if len(value) == 2 else value[2]
    return value


def main() -> None:
    d = pd.read_csv(EXT / "clean_33y_macro_144a_hibor_panel.csv", low_memory=False)
    rows = json.loads((ROOT / "overview_1994_2026/market_cache/hkHSI_1994_2026.json").read_text())
    px = pd.Series({pd.Timestamp(k): close_of(v) for k, v in rows.items()}).astype(float).sort_index()
    px = px[px.index <= ASOF]
    ctp = pd.read_csv(EXT / "clean_monthly_ctp_seasoned_factors_1994_2026.csv")
    div = ctp.set_index("year_month")["hsi_div_monthly_pct"].astype(float) / 100
    months = pd.period_range("1994-01", "2026-11", freq="M").strftime("%Y-%m")
    div = div.reindex(months).ffill()
    div_index = (1 + div).cumprod()

    recycled = d["flag_recycled_or_transferred_ticker"].fillna(0) != 0
    rev = ~recycled & d["flag_reverse_split_distortion"].fillna(False).astype(bool)
    unv = ~recycled & ~rev & d["flag_lifetime_split_unverified"].fillna(False).astype(bool)
    ret = pd.to_numeric(d["lifetime_offer_to_date_pct"], errors="coerce") / 100
    proceeds = pd.to_numeric(d["funds_raised_total_hkd"], errors="coerce") / 1e9
    ok = ~recycled & ~rev & ~unv & ret.notna()
    noquote = ~recycled & ~rev & ~unv & ret.isna()

    g = pd.DataFrame({"name": d["company_name"], "board": d["board"], "P": proceeds, "r": ret,
                      "date": pd.to_datetime(d["listing_date"], format="mixed")})[ok].dropna(subset=["P"])
    start = px.reindex(g["date"], method="ffill").to_numpy()
    g["b_px"] = px.iloc[-1] / start - 1
    ym = g["date"].dt.strftime("%Y-%m")
    g["b_tr"] = (1 + g["b_px"]) * (div_index.iloc[-1] / ym.map(div_index)) - 1
    g["gain"] = g.P * g.r

    def row(label: str, t: pd.DataFrame) -> dict:
        out = {"Sample": label, "N": len(t), "Proceeds_HKD_Bn": t.P.sum(), "IPO_Price_Gain_HKD_Bn": t.gain.sum()}
        for key, col in [("HSI_Price", "b_px"), ("HSI_TR", "b_tr")]:
            bench = (t.P * t[col]).sum()
            beat = t.r > t[col]
            out |= {f"{key}_Gain_HKD_Bn": bench, f"Excess_vs_{key}_HKD_Bn": t.gain.sum() - bench,
                    f"Wealth_Ratio_vs_{key}": (t.P * (1 + t.r)).sum() / (t.P * (1 + t[col])).sum(),
                    f"Pct_IPOs_Beating_{key}": beat.mean() * 100,
                    f"Pct_Proceeds_Beating_{key}": t.P[beat].sum() / t.P.sum() * 100}
        return out

    y = g["date"].dt.year
    out = [row("All verified IPOs", g), row("Main Board", g[g.board == "Main Board"]), row("GEM", g[g.board == "GEM"]),
           row("All excluding Tencent", g[~g.name.str.contains("Tencent")])]
    for label, lo, hi in [("Era I", 1994, 1999), ("Era II", 2000, 2007), ("Era III", 2008, 2017),
                          ("Era IV", 2018, 2022), ("Era V", 2023, 2026)]:
        out.append(row(label, g[y.between(lo, hi)]))
    res = pd.DataFrame(out).round(2)
    res["NoQuote_Delisted_Proceeds_HKD_Bn"] = round(float(proceeds[noquote].sum()), 2)
    res["Other_Excluded_Proceeds_HKD_Bn"] = round(float(proceeds[recycled | rev | unv].sum()), 2)
    res.to_csv(EXT / "ext_table14c_wealth_vs_hsi_benchmark.csv", index=False)
    print(res.T.to_string())


if __name__ == "__main__":
    main()
