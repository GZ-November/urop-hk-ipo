#!/usr/bin/env python3
"""
Step 1: Extend Secondary-Market Daily Caches & Matured Aftermarket/Lockup Panels Through 2026-11-12
==================================================================================================
1. Keeps primary-market listing sample fixed at 1994-01-01 through 2026-09-30 (N=2,866 / N=226 / N=113).
2. Tops up `hkHSI_1994_2026.json`, 2023-2026 `market_cache/*.json` (Tencent hfq), and `ah_reference/`
   (A-share bars, H-share bars, Frankfurter CNY/HKD FX) strictly through `2026-11-12` (excluding 2026-11-13).
3. Updates newly matured aftermarket horizons (1M/3M/6M/1Y BHR, BHAR, WR) in `HKIPO-MB-MASTER_clean.csv`,
   `hkipo_2025Q1_2026Q3_complete_226.csv`, and `clean_33y_hkipo_panel_1994_2026.csv`.
4. Computes matured Day +180 Cornerstone Lockup CAR[-20,+20], CAR[-5,+5], and Volume Shock Ratio
   using the exact LockupPanelEngine window formulas in `HKIPO-MB-MASTER_clean.csv` and builds the
   paired Day +180 vs Day +365 lockup dataset `clean_2025_2026_paired_6m_12m_lockup_panel.csv`.
"""
from __future__ import annotations

import bisect
import calendar
import datetime as dt
import json
import shutil
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path("/Users/georgezhu/Desktop/UROP HK IPO")
OUT_MAIN = ROOT / "analysis" / "out" / "overview_1994_2026"
OUT_EXT = ROOT / "analysis" / "out" / "overview_extensions"
CACHE_DIR = OUT_MAIN / "market_cache"
AH_DIR = ROOT / "pipeline" / "prospectus_pipeline" / "data" / "market" / "ah_reference"
MASTER_PATH = ROOT / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv"
C226_PATH = OUT_MAIN / "hkipo_2025Q1_2026Q3_complete_226.csv"
C33_PATH = OUT_MAIN / "clean_33y_hkipo_panel_1994_2026.csv"

AS_OF_STR = "2026-11-12"
AS_OF_DATE = dt.date(2026, 11, 12)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

OUT_EXT.mkdir(parents=True, exist_ok=True)


def add_calendar_months(value: dt.date, months: int) -> dt.date:
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return dt.date(year, month, day)


def fetch_json(url: str, timeout: int = 12) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def topup_hsi() -> dict[str, float]:
    hsi_path = CACHE_DIR / "hkHSI_1994_2026.json"
    hsi_map: dict[str, float] = json.loads(hsi_path.read_text(encoding="utf-8"))
    url = "https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?param=hkHSI,day,2026-09-20,2026-11-12,80,qfq"
    payload = fetch_json(url, timeout=15)
    d = (payload.get("data") or {}).get("hkHSI") or {}
    rows = d.get("qfqday") or d.get("day") or []
    added = 0
    for r in rows:
        day_s = str(r[0])[:10]
        if day_s <= AS_OF_STR:
            val = float(r[2])
            if day_s not in hsi_map:
                added += 1
            hsi_map[day_s] = val
    # Remove any future bars beyond AS_OF_STR if ever present
    hsi_map = {k: v for k, v in sorted(hsi_map.items()) if k <= AS_OF_STR}
    hsi_path.write_text(json.dumps(hsi_map, sort_keys=True), encoding="utf-8")
    print(f"[1/5] hkHSI topped up through {max(hsi_map.keys())} (+{added} new trading days, total={len(hsi_map)}).")
    return hsi_map


def parse_tencent_hk_rows(rows: list[list[Any]]) -> dict[str, list[Any]]:
    out: dict[str, list[Any]] = {}
    for r in rows:
        day_s = str(r[0])[:10]
        if day_s > AS_OF_STR:
            continue
        turn = None
        if len(r) > 8 and r[8] not in (None, "", "{}", {}):
            try:
                turn = float(r[8]) * 10000.0
            except Exception:
                turn = None
        out[day_s] = [
            day_s,
            float(r[1]),
            float(r[2]),
            float(r[3]),
            float(r[4]),
            float(r[5]),
            turn,
        ]
    return out


def topup_one_stock(cpath: Path, code: str, ld_str: str) -> tuple[str, str]:
    digits = "".join(ch for ch in code if ch.isdigit())
    sym = f"hk{int(digits):05d}"
    cached: list[list[Any]] = json.loads(cpath.read_text(encoding="utf-8")) if cpath.exists() else []
    cached = [b for b in cached if b[0] <= AS_OF_STR]
    if not cached:
        return code, "empty_cache"
    last_cached_date = cached[-1][0]
    if last_cached_date >= AS_OF_STR:
        return code, "already_current"

    url = f"https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?param={sym},day,2026-09-15,{AS_OF_STR},80,hfq"
    try:
        payload = fetch_json(url, timeout=12)
    except Exception as e:
        return code, f"err:{e}"
    d = payload.get("data")
    if not isinstance(d, dict) or sym not in d:
        return code, "no_symbol_data"
    rows = d[sym].get("hfqday") or d[sym].get("day") or []
    new_map = parse_tencent_hk_rows(rows)
    if not new_map:
        return code, "no_new_rows"

    cached_map = {b[0]: b for b in cached}
    overlap = sorted(set(cached_map) & set(new_map))
    if overlap:
        ov_d = overlap[-1]
        c_old = cached_map[ov_d][2]
        c_new = new_map[ov_d][2]
        if c_old > 0 and abs(c_new / c_old - 1.0) > 0.01:
            # Post-2026-09-30 dividend/split shifted hfq level on overlap; keep bars[0] scale via ratio-chain
            ratio = c_old / c_new
            for d_s, bar in new_map.items():
                if d_s > last_cached_date:
                    cached_map[d_s] = [
                        d_s,
                        round(bar[1] * ratio, 4),
                        round(bar[2] * ratio, 4),
                        round(bar[3] * ratio, 4),
                        round(bar[4] * ratio, 4),
                        bar[5],
                        bar[6],
                    ]
            res = [cached_map[k] for k in sorted(cached_map)]
            cpath.write_text(json.dumps(res), encoding="utf-8")
            return code, f"ratio_chained({ratio:.4f})"

    for d_s, bar in new_map.items():
        if d_s > last_cached_date:
            cached_map[d_s] = bar
    res = [cached_map[k] for k in sorted(cached_map)]
    cpath.write_text(json.dumps(res), encoding="utf-8")
    return code, "updated"


def topup_market_cache_2023_2026() -> None:
    df33 = pd.read_csv(C33_PATH, low_memory=False)
    sub = df33[df33["cohort_year"] >= 2023][["stock_code", "listing_date"]].drop_duplicates()
    # Also ensure every N226 code is checked
    c226 = pd.read_csv(C226_PATH)
    pairs: dict[str, tuple[Path, str]] = {}
    for _, r in sub.iterrows():
        sc = str(r["stock_code"]).strip()
        ld = str(r["listing_date"])[:10]
        num = int(sc.split(".")[0])
        cp = CACHE_DIR / f"{num:04d}.HK_{ld}.json"
        if cp.exists():
            pairs[f"{num:04d}.HK_{ld}"] = (cp, ld)
    for _, r in c226.iterrows():
        sc = str(r["Stock Code"]).strip()
        ld = str(r["Date of Listing"])[:10]
        num = int(sc.split(".")[0])
        cp = CACHE_DIR / f"{num:04d}.HK_{ld}.json"
        if cp.exists():
            pairs[f"{num:04d}.HK_{ld}"] = (cp, ld)

    counts: dict[str, int] = {}
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(topup_one_stock, cp, k.split("_")[0], ld): k for k, (cp, ld) in pairs.items()}
        for f in as_completed(futs):
            _, st = f.result()
            key_st = st.split("(")[0] if "(" in st else st
            counts[key_st] = counts.get(key_st, 0) + 1
    print(f"[2/5] Market cache topup (cohort>=2023, N={len(pairs)} files): {counts}")


def topup_ah_reference() -> None:
    if not AH_DIR.exists():
        return
    # 1. FX via Frankfurter
    fx_path = AH_DIR / "fx_cnyhkd.json"
    fx_list = json.loads(fx_path.read_text(encoding="utf-8"))
    fx_map = {x["date"]: float(x["close"]) for x in fx_list if x["date"] <= AS_OF_STR}
    try:
        fx_url = f"https://api.frankfurter.app/2026-09-25..{AS_OF_STR}?from=CNY&to=HKD"
        fx_j = fetch_json(fx_url, timeout=10)
        for d_s, rates in (fx_j.get("rates") or {}).items():
            if d_s <= AS_OF_STR and "HKD" in rates:
                fx_map[d_s] = float(rates["HKD"])
        fx_out = [{"date": k, "close": fx_map[k]} for k in sorted(fx_map)]
        fx_path.write_text(json.dumps(fx_out, indent=1), encoding="utf-8")
    except Exception as e:
        print("  FX topup warning:", e)

    # 2. A-bars & H-bars
    def _topup_bar_dir(bdir: Path, is_hk: bool) -> int:
        updated = 0
        for p in sorted(bdir.glob("*.json")):
            sym = p.stem
            rows = json.loads(p.read_text(encoding="utf-8"))
            rows = [r for r in rows if r["date"] <= AS_OF_STR]
            if not rows:
                continue
            last_d = rows[-1]["date"]
            if last_d >= AS_OF_STR:
                continue
            endpoint = "hkfqkline" if is_hk else "fqkline"
            url = f"https://web.ifzq.gtimg.cn/appstock/app/{endpoint}/get?param={sym},day,2026-09-15,{AS_OF_STR},80,qfq"
            try:
                pay = fetch_json(url, timeout=10)
                d = (pay.get("data") or {}).get(sym) or {}
                krows = d.get("qfqday") or d.get("day") or []
                old_map = {r["date"]: r for r in rows}
                ov = sorted(set(old_map) & {str(kr[0])[:10] for kr in krows})
                ratio = 1.0
                if ov:
                    od = ov[-1]
                    kr_ov = next(kr for kr in krows if str(kr[0])[:10] == od)
                    if float(kr_ov[2]) > 0 and abs(float(kr_ov[2]) / old_map[od]["close"] - 1.0) > 0.01:
                        ratio = old_map[od]["close"] / float(kr_ov[2])
                for kr in krows:
                    ds = str(kr[0])[:10]
                    if ds > last_d and ds <= AS_OF_STR:
                        old_map[ds] = {
                            "date": ds,
                            "open": round(float(kr[1]) * ratio, 4),
                            "close": round(float(kr[2]) * ratio, 4),
                            "high": round(float(kr[3]) * ratio, 4),
                            "low": round(float(kr[4]) * ratio, 4),
                            "volume": float(kr[5]),
                        }
                out_list = [old_map[k] for k in sorted(old_map)]
                p.write_text(json.dumps(out_list, indent=1), encoding="utf-8")
                updated += 1
            except Exception:
                pass
        return updated

    na = _topup_bar_dir(AH_DIR / "a_bars", False)
    nh = _topup_bar_dir(AH_DIR / "h_bars", True)
    print(f"[3/5] ah_reference updated through {AS_OF_STR}: a_bars={na}, h_bars={nh}, fx_max={max(fx_map.keys())}.")


def load_stock_bars(code: str, ld_str: str) -> list[list[Any]]:
    num = int(str(code).split(".")[0].strip())
    cp = CACHE_DIR / f"{num:04d}.HK_{ld_str}.json"
    if not cp.exists():
        cands = sorted(CACHE_DIR.glob(f"{num:04d}.HK_*.json"))
        cp = cands[0] if cands else None
    if not cp or not cp.exists():
        return []
    bars = json.loads(cp.read_text(encoding="utf-8"))
    return [b for b in bars if b[0] >= ld_str and b[0] <= AS_OF_STR]


def compute_lockup_event_from_bars(
    bars: list[list[Any]],
    hsi_map: dict[str, float],
    hsi_dates: list[str],
    event_date: dt.date,
) -> tuple[float | None, float | None, float | None, float | None, str]:
    """
    Exact replication of LockupPanelEngine.window_metrics_detail on market_cache bars:
    - event_idx: first trading bar on/after event_date (within 10 calendar days of exchange trading)
    - CAR[-20,+20]: sum of (r_stock - r_HSI) over [u-20 .. u+20]
    - CAR[-5,+5]: sum of (r_stock - r_HSI) over [u-5 .. u+5]
    - vol_shock: mean(turn[u..u+20]) / mean(turn[u-20..u-1])
    """
    if not bars or event_date > AS_OF_DATE:
        return None, None, None, None, "IMMATURE_EVENT_DATE"
    ev_str = event_date.isoformat()
    u_idx = next((i for i, b in enumerate(bars) if b[0] >= ev_str), None)
    if u_idx is None:
        return None, None, None, None, "MISSING_POST_UNLOCK_BARS"

    # Check calendar gap from event_date to bars[u_idx]
    if bisect.bisect_left(hsi_dates, bars[u_idx][0]) - bisect.bisect_left(hsi_dates, ev_str) > 2:
        return None, None, None, None, "SUSPENDED_AT_UNLOCK"

    def _car(lo: int, hi: int) -> float | None:
        if lo < 1 or hi >= len(bars):
            return None
        tot = 0.0
        for i in range(lo, hi + 1):
            p_curr, p_prev = bars[i][2], bars[i - 1][2]
            if not (p_curr and p_prev and p_curr > 0 and p_prev > 0):
                return None
            h_curr = hsi_map.get(bars[i][0])
            h_prev = hsi_map.get(bars[i - 1][0])
            if not (h_curr and h_prev and h_curr > 0 and h_prev > 0):
                # fallback on nearest prior HSI date if exact date gap
                idx_c = bisect.bisect_right(hsi_dates, bars[i][0]) - 1
                idx_p = bisect.bisect_right(hsi_dates, bars[i - 1][0]) - 1
                if idx_c < 0 or idx_p < 0:
                    return None
                h_curr, h_prev = hsi_map[hsi_dates[idx_c]], hsi_map[hsi_dates[idx_p]]
            r_s = p_curr / p_prev - 1.0
            r_m = h_curr / h_prev - 1.0
            tot += (r_s - r_m)
        return round(tot, 6)

    car20 = _car(u_idx - 20, u_idx + 20)
    car5 = _car(u_idx - 5, u_idx + 5)

    vol_shock = None
    if u_idx >= 20 and u_idx + 20 < len(bars):
        pre_t = [b[6] if b[6] is not None else b[5] * b[2] for b in bars[u_idx - 20 : u_idx]]
        post_t = [b[6] if b[6] is not None else b[5] * b[2] for b in bars[u_idx : u_idx + 21]]
        if all(t is not None and np.isfinite(t) and t >= 0 for t in pre_t + post_t):
            m_pre = float(np.mean(pre_t))
            m_post = float(np.mean(post_t))
            if m_pre > 0:
                vol_shock = round(m_post / m_pre, 4)

    # Pre-unlock run-up from Day 1 close to u_idx - 21 close
    pre_runup = None
    if u_idx >= 22 and bars[0][2] > 0:
        pre_runup = round(bars[u_idx - 21][2] / bars[0][2] - 1.0, 6)

    status = "MATURED" if car20 is not None else ("MATURED_CAR5_ONLY" if car5 is not None else "IMMATURE_WINDOW")
    return car20, car5, vol_shock, pre_runup, status


def update_master_and_panels(hsi_map: dict[str, float]) -> None:
    hsi_dates = sorted(hsi_map.keys())

    def get_hsi_on_or_after(d_str: str) -> float | None:
        idx = bisect.bisect_left(hsi_dates, d_str)
        if idx < len(hsi_dates):
            return hsi_map[hsi_dates[idx]]
        return None

    def get_hsi_on_or_before(d_str: str) -> float | None:
        idx = bisect.bisect_right(hsi_dates, d_str) - 1
        return hsi_map[hsi_dates[idx]] if idx >= 0 else None

    # Snapshots
    bak_master = OUT_MAIN / "HKIPO-MB-MASTER_clean.pre_20261112.bak.csv"
    if not bak_master.exists():
        shutil.copy2(MASTER_PATH, bak_master)
    bak_c226 = OUT_MAIN / "hkipo_2025Q1_2026Q3_complete_226.pre_20261112.bak.csv"
    if not bak_c226.exists():
        shutil.copy2(C226_PATH, bak_c226)
    bak_c33 = OUT_MAIN / "clean_33y_hkipo_panel_1994_2026.pre_20261112.bak.csv"
    if not bak_c33.exists():
        shutil.copy2(C33_PATH, bak_c33)

    master = pd.read_csv(MASTER_PATH)
    c226 = pd.read_csv(C226_PATH)

    # Stats tracking
    filled_bhr = {"1m": 0, "3m": 0, "6m": 0, "1y": 0}
    old_c20_count = int(master["Cornerstone unlock CAR [-20, +20] (%)"].notna().sum())

    paired_rows = []
    for idx, row in master.iterrows():
        sc = str(row["Stock Code"]).strip()
        ld_raw = str(row["Date of Listing (dd/mm/yy)"]).strip()
        ld_dt = pd.to_datetime(ld_raw, errors="coerce")
        if pd.isna(ld_dt):
            continue
        ld = ld_dt.date()
        ld_str = ld.isoformat()
        bars = load_stock_bars(sc, ld_str)
        if not bars:
            continue

        d1_close = bars[0][2]
        hsi_d0 = get_hsi_on_or_after(bars[0][0])

        # A. Fill ONLY missing 1M / 3M / 6M BHR and WR in Master using aftermarket.py exact rule
        # 1M: 20th trading bar (index 19)
        if pd.isna(row.get("1-month BHR from Day-1 close (%)")) and len(bars) >= 20 and d1_close > 0:
            b1m = bars[19]
            bhr1m = b1m[2] / d1_close - 1.0
            master.at[idx, "1-month BHR from Day-1 close (%)"] = round(bhr1m, 6)
            filled_bhr["1m"] += 1

        # 3M: listing_date + 3 calendar months
        t3m = add_calendar_months(ld, 3).isoformat()
        b3m = next((b for b in bars if b[0] >= t3m), None)
        if b3m is not None and d1_close > 0:
            bhr3m = b3m[2] / d1_close - 1.0
            h3m = get_hsi_on_or_after(b3m[0])
            wr3m = (1.0 + bhr3m) / (h3m / hsi_d0) if (h3m and hsi_d0 and hsi_d0 > 0) else np.nan
            if pd.isna(row.get("3-month BHR from Day-1 close (%)")):
                master.at[idx, "3-month BHR from Day-1 close (%)"] = round(bhr3m, 6)
                filled_bhr["3m"] += 1
            if pd.isna(row.get("3-month wealth relative vs HSI")) and pd.notna(wr3m):
                master.at[idx, "3-month wealth relative vs HSI"] = round(wr3m, 4)

        # 6M: listing_date + 6 calendar months
        t6m = add_calendar_months(ld, 6).isoformat()
        b6m = next((b for b in bars if b[0] >= t6m), None)
        if b6m is not None and d1_close > 0:
            bhr6m = b6m[2] / d1_close - 1.0
            h6m = get_hsi_on_or_after(b6m[0])
            wr6m = (1.0 + bhr6m) / (h6m / hsi_d0) if (h6m and hsi_d0 and hsi_d0 > 0) else np.nan
            if pd.isna(row.get("6-month BHR from Day-1 close (%)")):
                master.at[idx, "6-month BHR from Day-1 close (%)"] = round(bhr6m, 6)
                filled_bhr["6m"] += 1
            if pd.isna(row.get("6-month wealth relative vs HSI")) and pd.notna(wr6m):
                master.at[idx, "6-month wealth relative vs HSI"] = round(wr6m, 4)

        # B. Lockup expiration CARs: fill newly matured rows (preserve existing N=58 when present)
        u6_raw = row.get("Earliest cornerstone unlock date (dd/mm/yy)")
        u6_dt = pd.to_datetime(u6_raw, errors="coerce")
        if pd.notna(u6_dt):
            c20_6, c5_6, vs_6, runup_6, st_6 = compute_lockup_event_from_bars(bars, hsi_map, hsi_dates, u6_dt.date())
            if pd.isna(row.get("Cornerstone unlock CAR [-5, +5] (%)")) and c5_6 is not None:
                master.at[idx, "Cornerstone unlock CAR [-5, +5] (%)"] = c5_6
            if pd.isna(row.get("Cornerstone unlock CAR [-20, +20] (%)")) and c20_6 is not None:
                master.at[idx, "Cornerstone unlock CAR [-20, +20] (%)"] = c20_6
            if pd.isna(row.get("Cornerstone unlock volume shock ratio")) and vs_6 is not None:
                master.at[idx, "Cornerstone unlock volume shock ratio"] = vs_6

        # C. Build full N=226 Paired Day +180 (6M) & Day +365 (12M) statutory unlock panel
        # Day +180 uses verified cornerstone unlock date when present, else statutory 6M anniversary
        u6_eff = u6_dt.date() if pd.notna(u6_dt) else add_calendar_months(ld, 6)
        u12_raw = row.get("Controlling shareholder 12-month cessation of control expiry date")
        u12_dt = pd.to_datetime(u12_raw, errors="coerce")
        u12_eff = u12_dt.date() if pd.notna(u12_dt) else add_calendar_months(ld, 12)

        c20_6m, c5_6m, vs_6m, run6, st_6m = compute_lockup_event_from_bars(bars, hsi_map, hsi_dates, u6_eff)
        c20_12m, c5_12m, vs_12m, run12, st_12m = compute_lockup_event_from_bars(bars, hsi_map, hsi_dates, u12_eff)

        # Preserve pre-existing CAR if available for exact N=58 alignment, else use recomputed
        c20_6m_master = master.at[idx, "Cornerstone unlock CAR [-20, +20] (%)"]
        c5_6m_master = master.at[idx, "Cornerstone unlock CAR [-5, +5] (%)"]
        vs_6m_master = master.at[idx, "Cornerstone unlock volume shock ratio"]

        paired_rows.append({
            "stock_code": sc,
            "cohort": row["cohort"],
            "listing_date": ld_str,
            "has_cornerstone_unlock_date": int(pd.notna(u6_dt)),
            "unlock_6m_date": u6_eff.isoformat(),
            "unlock_12m_date": u12_eff.isoformat(),
            "car20_6m_bars": c20_6m,
            "car5_6m_bars": c5_6m,
            "vol_shock_6m_bars": vs_6m,
            "car20_6m_master": float(c20_6m_master) if pd.notna(c20_6m_master) else np.nan,
            "car5_6m_master": float(c5_6m_master) if pd.notna(c5_6m_master) else np.nan,
            "vol_shock_6m_master": float(vs_6m_master) if pd.notna(vs_6m_master) else np.nan,
            "pre_unlock_runup_6m": run6,
            "status_6m": st_6m,
            "car20_12m_bars": c20_12m,
            "car5_12m_bars": c5_12m,
            "vol_shock_12m_bars": vs_12m,
            "pre_unlock_runup_12m": run12,
            "status_12m": st_12m,
        })

    master.to_csv(MASTER_PATH, index=False)
    new_c20_count = int(master["Cornerstone unlock CAR [-20, +20] (%)"].notna().sum())
    print("[4/5] HKIPO-MB-MASTER_clean.csv updated:")
    print(f"      Filled missing BHRs: {filled_bhr}")
    print(f"      1M BHR non-null={master['1-month BHR from Day-1 close (%)'].notna().sum()}, "
          f"3M BHR={master['3-month BHR from Day-1 close (%)'].notna().sum()}, "
          f"6M BHR={master['6-month BHR from Day-1 close (%)'].notna().sum()}")
    print(f"      Cornerstone unlock CAR[-20,+20] expanded: {old_c20_count} -> {new_c20_count}")

    df_paired = pd.DataFrame(paired_rows)
    paired_path = OUT_EXT / "clean_2025_2026_paired_6m_12m_lockup_panel.csv"
    df_paired.to_csv(paired_path, index=False)
    print(f"      Paired lockup panel: 6M bars non-null={df_paired['car20_6m_bars'].notna().sum()}, "
          f"6M master non-null={df_paired['car20_6m_master'].notna().sum()}, "
          f"12M bars non-null={df_paired['car20_12m_bars'].notna().sum()}")

    # Sync hkipo_2025Q1_2026Q3_complete_226.csv from updated Master
    m_idx = master.set_index("Stock Code")
    for idx, r in c226.iterrows():
        sc = r["Stock Code"]
        if sc in m_idx.index:
            mr = m_idx.loc[sc]
            for c_226, c_m in [
                ("bhr_1m_pct", "1-month BHR from Day-1 close (%)"),
                ("bhr_3m_pct", "3-month BHR from Day-1 close (%)"),
                ("bhr_6m_pct", "6-month BHR from Day-1 close (%)"),
                ("wr_3m", "3-month wealth relative vs HSI"),
                ("wr_6m", "6-month wealth relative vs HSI"),
            ]:
                if pd.notna(mr[c_m]):
                    c226.at[idx, c_226] = mr[c_m]
    c226.to_csv(C226_PATH, index=False)
    print(f"      Synced complete_226: 1M={c226['bhr_1m_pct'].notna().sum()}, "
          f"3M={c226['bhr_3m_pct'].notna().sum()}, 6M={c226['bhr_6m_pct'].notna().sum()}")

    # Update clean_33y_hkipo_panel_1994_2026.csv for cohort_year >= 2023 newly matured 1M/3M/6M/1Y
    df33 = pd.read_csv(C33_PATH, low_memory=False)
    updated_33 = 0
    for idx, r in df33[df33["cohort_year"] >= 2023].iterrows():
        if pd.isna(r.get("ir_close_pct")):
            continue
        sc = str(r["stock_code"]).strip()
        ld_s = str(r["listing_date"])[:10]
        bars = load_stock_bars(sc, ld_s)
        if not bars:
            continue
        d1_close = bars[0][2]
        hsi_d1 = get_hsi_on_or_before(bars[0][0])
        changed = False
        for lbl, tidx in [("1m", 21), ("3m", 63), ("6m", 126), ("1y", 252)]:
            col_b = f"after_bhr_{lbl}_pct"
            col_a = f"after_bhar_{lbl}_pct"
            col_w = f"after_wr_{lbl}"
            if pd.isna(r.get(col_b)) and len(bars) > tidx and d1_close > 0:
                bt = bars[tidx]
                bhr = (bt[2] - d1_close) / d1_close
                if -0.99 <= bhr <= 30.0:
                    df33.at[idx, col_b] = round(bhr * 100.0, 4)
                    ht = get_hsi_on_or_before(bt[0])
                    if hsi_d1 and ht and hsi_d1 > 0:
                        bhr_m = (ht - hsi_d1) / hsi_d1
                        df33.at[idx, col_a] = round((bhr - bhr_m) * 100.0, 4)
                        if (1.0 + bhr_m) > 0:
                            df33.at[idx, col_w] = round((1.0 + bhr) / (1.0 + bhr_m), 4)
                    changed = True
        if changed:
            updated_33 += 1
    df33.to_csv(C33_PATH, index=False)
    print(f"[5/5] clean_33y_hkipo_panel_1994_2026.csv updated for {updated_33} cohort>=2023 IPOs "
          f"(2025 1Y BHAR non-null={df33[df33['cohort_year']==2025]['after_bhar_1y_pct'].notna().sum()}/{(df33['cohort_year']==2025).sum()}, "
          f"2025-26 6M BHR non-null={df33[df33['cohort_year']>=2025]['after_bhr_6m_pct'].notna().sum()}).")


def main() -> None:
    t0 = time.time()
    hsi_map = topup_hsi()
    topup_market_cache_2023_2026()
    topup_ah_reference()
    update_master_and_panels(hsi_map)
    print(f"All market caches & lockup horizons refreshed through {AS_OF_STR} in {time.time() - t0:.1f}s.")


if __name__ == "__main__":
    main()
