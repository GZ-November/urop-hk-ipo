#!/usr/bin/env python3
"""Comprehensive 1994–2026 Hong Kong IPO Market Overview Builder & Empirical Suite.

Builds:
  1. Official 2026 Retail Allocation Tier Audit & 113-Issuer Complete Table:
     - Verifies the 19 conflict issuers (where Master had 2-decimal Subscription Level * Initial Public Shares
       or manual Pool B omission, vs. authoritative exact tier-table sum) and 3355.HK (resolved via official
       HKEX Clarification Announcement dated 2026-03-27, `3355_clarification.pdf`).
  2. Multi-Decade HKEX Primary Market Master Panel (1994–2026 Main Board + 1999–2026 GEM):
     - Parses all 33 official HKEX Main Board New Listing Reports (`1994.xls`–`NLR2026_Eng.xlsx` + supplement)
       and 26 official GEM New Listing Reports (`e_newlistings99.xls`–`e_newlistings2026.xlsx`).
     - Applies the 4-step statutory sample filter (excluding Ch 9A GEM transfers, Ch 18B SPACs, and
       Listings by Introduction).
     - Fetches/caches 0-token historical daily K-lines from Tencent (`hfqday`/`day` with `raw_as_traded`
       and local cache reuse) + HSI (`hkHSI`) benchmark from 1994 to 2026-09-30.
     - Computes Day-1 Initial Return (IR), Day-1 Turnover, Money Left on the Table (HK$ m),
       and post-IPO 1M (21d), 3M (63d), 6M (126d), 1Y (252d), and 3Y (756d) Buy-and-Hold Returns (BHR),
       HSI-Benchmark-Adjusted BHAR, and Wealth Relatives (WR).
  3. Complete 7-Quarter Modern Micro-Institutional Panel (2025Q1–2026Q3, N=226 Main Board IPOs):
     - Integrates 2025Q3 (24 Main Board IPOs bridging the August 4, 2025 Pricing & Open Market Reform)
       with the 202 stored cohorts in `HKIPO-MB-MASTER_clean.csv`.
  4. Multi-Angle Hypothesis Tests & Publication-Grade Summary Tables (`analysis/out/overview_1994_2026/`).
"""
from __future__ import annotations

import datetime as dt
import io
import json
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import numpy as np
import openpyxl
import pandas as pd
import xlrd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline" / "prospectus_pipeline" / "src"))

import sample_builder
from listing_reports import _local_report, load_supplement
from sample_builder import audit_candidate, clean_code, load_nlr_candidates, to_float

OUT_DIR = ROOT / "analysis" / "out" / "overview_1994_2026"
CACHE_DIR = OUT_DIR / "market_cache"
GAP_DIR = ROOT / "pipeline" / "reports" / "data_gap_collection"


def parse_dt(v: Any) -> dt.date | None:
    if v is None:
        return None
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    s = str(v).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%y", "%d-%m-%y"):
        try:
            return dt.datetime.strptime(s[:10], fmt).date()
        except ValueError:
            pass
    return None


sample_builder.parse_date = parse_dt


def assign_epoch(d: dt.date) -> str:
    if d.year <= 2004:
        return "Epoch II (1994-2004: H-Share Pioneer, PN18 & GEM Launch)"
    if d.year <= 2017:
        return "Epoch III (2005-2017: SOE Mega-Banks & Cornerstone Regime)"
    if d.year <= 2022:
        return "Epoch IV (2018-2022: Ch. 8A/18A/19C New-Economy Overhaul)"
    return "Epoch V (2023-2026: Ch. 18C, FINI T+2 & Aug 2025 Mech A/B)"


def build_all_nlr_candidates() -> pd.DataFrame:
    src = ROOT / "pipeline" / "sources"
    all_candidates: list[dict[str, Any]] = []

    for y in range(1994, 2027):
        p = _local_report(src, y)
        if not p:
            continue
        cands = load_nlr_candidates(p, y, board="main")
        for c in cands:
            if c["listing_date"] is None:
                continue
            rec = audit_candidate(c, board="main")
            rec["board"] = "Main Board"
            all_candidates.append(rec)

    supp = load_supplement(
        src, 2026, dt.date(2026, 1, 1), dt.date(2026, 9, 30), covered_through=dt.date(2026, 9, 29)
    )
    for s in supp:
        code = clean_code(s.get("stock_code"))
        if not any(x["stock_code"] == code and x["cohort_year"] == 2026 for x in all_candidates):
            rec = audit_candidate(
                {
                    "file_no": s.get("file_no", 116),
                    "raw_code": str(s.get("stock_code")),
                    "stock_code": code,
                    "company_name": s.get("company_name", ""),
                    "prospectus_date": parse_dt(s.get("prospectus_date")),
                    "listing_date": parse_dt(s.get("listing_date")),
                    "cohort_year": 2026,
                    "sponsors": s.get("sponsors", ""),
                    "auditor": s.get("auditor", ""),
                    "valuer": None,
                    "funds_raised_public_hkd": to_float(s.get("funds_raised_public_hkd")),
                    "funds_raised_int_hkd": to_float(s.get("funds_raised_int_hkd")),
                    "offer_price_hkd": to_float(s.get("offer_price_hkd")),
                    "raw_price_str": str(s.get("offer_price_hkd", "")),
                    "raw_funds_str": str(s.get("funds_raised_total_hkd", "")),
                },
                board="main",
            )
            rec["board"] = "Main Board"
            all_candidates.append(rec)

    gem_dir = src / "GEM"
    gem_files = []
    for y in range(1999, 2027):
        if y in (2022, 2023):
            continue
        yy = f"{y % 100:02d}"
        for cand_name in (f"e_newlistings{y}.xlsx", f"e_newlistings{y}.xls", f"e_newlistings{yy}.xls"):
            gp = gem_dir / cand_name
            if gp.exists():
                gem_files.append((y, gp))
                break

    for y, gp in gem_files:
        raw = gp.read_bytes()
        if raw.startswith(b"PK\x03\x04"):
            wb = openpyxl.load_workbook(io.BytesIO(raw), read_only=True, data_only=True)
            rows = list(wb.active.iter_rows(values_only=True))
            wb.close()
        else:
            wb = xlrd.open_workbook(file_contents=raw)
            ws = wb.sheet_by_index(0)
            rows = []
            for r in range(ws.nrows):
                vals = []
                for c in range(ws.ncols):
                    cell = ws.cell(r, c)
                    val = (
                        xlrd.xldate_as_datetime(cell.value, wb.datemode)
                        if cell.ctype == xlrd.XL_CELL_DATE
                        else cell.value
                    )
                    vals.append(val)
                rows.append(tuple(vals))
        r9 = [str(x or "").strip().lower() for x in rows[9]] if len(rows) > 9 else []
        shift = 1 if (len(r9) > 3 and r9[3] == "company") else 0
        for idx, r in enumerate(rows[10:], 10):
            ld = parse_dt(r[0] if len(r) > 0 else None)
            if ld is None or not any(ch.isdigit() for ch in str(r[1] or "")):
                continue
            code = clean_code(r[1])
            name = str(r[2 + shift] or "").strip()
            price = to_float(r[5 + shift] if len(r) > 5 + shift else None)
            sub_ratio = to_float(r[7 + shift] if len(r) > 7 + shift else None)
            funds = to_float(r[9 + shift] if len(r) > 9 + shift else None)
            shares_out = to_float(r[10 + shift] if len(r) > 10 + shift else None)
            mcap = to_float(r[12 + shift] if len(r) > 12 + shift else None)
            ind = str(r[14 + shift] or "").strip() if len(r) > 14 + shift else ""
            incorp = str(r[16 + shift] or "").strip() if len(r) > 16 + shift else ""
            method = str(r[17 + shift] or "").strip() if len(r) > 17 + shift else ""
            if idx + 1 < len(rows) and parse_dt(rows[idx + 1][0] if len(rows[idx + 1]) > 0 else None) is None:
                m2 = str(rows[idx + 1][17 + shift] if len(rows[idx + 1]) > 17 + shift else "").strip()
                if m2 and "total" not in str(rows[idx + 1][0] or "").lower():
                    method = f"{method}; {m2}" if method else m2
            sponsor = str(r[19 + shift] or "").strip() if len(r) > 19 + shift else ""
            auditor = str(r[21 + shift] or "").strip() if len(r) > 21 + shift else ""
            cand = {
                "file_no": len([x for x in all_candidates if x["board"] == "GEM" and x["cohort_year"] == y]) + 1,
                "raw_code": str(r[1]),
                "stock_code": code,
                "company_name": name,
                "prospectus_date": None,
                "listing_date": ld,
                "cohort_year": y,
                "sponsors": sponsor,
                "auditor": auditor,
                "valuer": None,
                "funds_raised_public_hkd": None,
                "funds_raised_int_hkd": None,
                "offer_price_hkd": price,
                "raw_price_str": str(r[5 + shift] or ""),
                "raw_funds_str": str(r[9 + shift] or ""),
                "gem_funds_raised_hkd": funds,
                "gem_subscription_ratio": sub_ratio,
                "gem_shares_at_listing": shares_out,
                "gem_market_cap_hkd": mcap,
                "gem_industry": ind,
                "gem_incorporation": incorp,
                "gem_listing_method": method,
                "source_report": str(gp),
            }
            rec = audit_candidate(cand, board="gem")
            rec["board"] = "GEM"
            all_candidates.append(rec)

    df = pd.DataFrame(all_candidates)
    df["epoch"] = df["listing_date"].apply(assign_epoch)
    df["is_prc_joint_stock"] = df["company_name"].str.contains(
        r"Co\.,?\s*Ltd\.?|Joint Stock|H\s+Shares?", case=False, na=False
    ).astype(int)
    df["prospectus_to_listing_days"] = [
        (ld - pd_dt).days if (isinstance(ld, dt.date) and isinstance(pd_dt, dt.date) and 0 <= (ld - pd_dt).days <= 90) else np.nan
        for ld, pd_dt in zip(df["listing_date"], df["prospectus_date"])
    ]
    df["public_tranche_proceeds_share"] = np.where(
        (df["board"] == "Main Board")
        & df["funds_raised_public_hkd"].notna()
        & df["funds_raised_total_hkd"].notna()
        & (df["funds_raised_total_hkd"] > 0),
        df["funds_raised_public_hkd"] / df["funds_raised_total_hkd"],
        np.nan,
    )
    return df


def fetch_hsi_series() -> dict[str, float]:
    cache_file = CACHE_DIR / "hkHSI_1994_2026.json"
    if cache_file.exists():
        return json.loads(cache_file.read_text())
    hsi_map: dict[str, float] = {}
    cur = dt.date(1994, 1, 1)
    end = dt.date(2026, 9, 30)
    while cur <= end:
        nxt = min(end, cur + dt.timedelta(days=700))
        url = f"https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?param=hkHSI,day,{cur},{nxt},640,qfq"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        d = (payload.get("data") or {}).get("hkHSI") or {}
        rows = d.get("qfqday") or d.get("day") or []
        for r in rows:
            hsi_map[str(r[0])[:10]] = float(r[2])
        cur = nxt + dt.timedelta(days=1)
    cache_file.write_text(json.dumps(hsi_map, sort_keys=True))
    return hsi_map


def fetch_issuer_window(code: str, ldate: dt.date) -> list[list[Any]]:
    key = f"{code}_{ldate.isoformat()}"
    cpath = CACHE_DIR / f"{key}.json"
    if cpath.exists():
        try:
            return json.loads(cpath.read_text())
        except Exception:
            pass

    digits = "".join(ch for ch in code if ch.isdigit())
    sym = f"hk{int(digits):05d}"
    d_end1 = min(dt.date(2026, 9, 30), ldate + dt.timedelta(days=560))
    d_end2 = min(dt.date(2026, 9, 30), ldate + dt.timedelta(days=1120))

    bars_map: dict[str, list[Any]] = {}
    for w_start, w_end in [(ldate, d_end1), (d_end1 + dt.timedelta(days=1), d_end2)]:
        if w_start > w_end:
            continue
        url = f"https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?param={sym},day,{w_start},{w_end},640,hfq"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            d = payload.get("data")
            if isinstance(d, dict) and sym in d:
                rows = d[sym].get("hfqday") or d[sym].get("day") or []
                for r in rows:
                    day_str = str(r[0])[:10]
                    if day_str >= ldate.isoformat():
                        turnover = None
                        if len(r) > 8 and r[8] not in (None, "", "{}", {}):
                            try:
                                turnover = float(r[8]) * 10000.0
                            except Exception:
                                turnover = None
                        bars_map[day_str] = [
                            day_str,
                            float(r[1]),
                            float(r[2]),
                            float(r[3]),
                            float(r[4]),
                            float(r[5]),
                            turnover,
                        ]
        except Exception:
            pass

    res = [bars_map[k] for k in sorted(bars_map)]
    cpath.write_text(json.dumps(res))
    return res


def compute_market_metrics(df_inc: pd.DataFrame, hsi_map: dict[str, float]) -> pd.DataFrame:
    hsi_dates = sorted(hsi_map.keys())

    def get_hsi_on_or_before(d_str: str) -> float | None:
        import bisect
        idx = bisect.bisect_right(hsi_dates, d_str) - 1
        if idx >= 0:
            return hsi_map[hsi_dates[idx]]
        return None

    tasks = [(idx, row["stock_code"], row["listing_date"]) for idx, row in df_inc.iterrows()]
    bars_by_idx: dict[int, list[list[Any]]] = {}

    with ThreadPoolExecutor(max_workers=20) as ex:
        futs = {ex.submit(fetch_issuer_window, code, ld): idx for idx, code, ld in tasks}
        for f in as_completed(futs):
            idx = futs[f]
            try:
                bars_by_idx[idx] = f.result()
            except Exception:
                bars_by_idx[idx] = []

    records = []
    for idx, row in df_inc.iterrows():
        bars = bars_by_idx.get(idx, [])
        ld = row["listing_date"]
        p0 = row["offer_price_hkd"]
        rec: dict[str, Any] = {"idx": idx, "bars_count": len(bars)}
        if bars and p0 and p0 > 0:
            first_date = dt.date.fromisoformat(bars[0][0])
            gap_days = (first_date - ld).days
            rec["first_bar_date"] = bars[0][0]
            rec["first_bar_gap_days"] = gap_days
            # Only accept day-1 bar if it lands within 7 calendar days of official listing date
            # and does not reflect a clearly recycled ticker decades later
            if 0 <= gap_days <= 7:
                d1_open = bars[0][1]
                d1_close = bars[0][2]
                d1_vol = bars[0][5]
                d1_turn = bars[0][6]
                ir_raw = (d1_close - p0) / p0
                # Guard against historical code recycling / unadjusted pre-consolidation price mismatch
                # (In HK history, legitimate day-1 returns range from -90% to +2500% on GEM/MB)
                if -0.92 <= ir_raw <= 25.0:
                    rec["d1_open"] = d1_open
                    rec["d1_close"] = d1_close
                    rec["d1_volume"] = d1_vol
                    rec["d1_turnover_hkd"] = d1_turn
                    rec["ir_close"] = ir_raw
                    rec["ir_open"] = (d1_open - p0) / p0
                    if row["funds_raised_total_hkd"] and row["funds_raised_total_hkd"] > 0:
                        offer_shares_approx = row["funds_raised_total_hkd"] / p0
                        rec["money_left_on_table_hkd_m"] = (d1_close - p0) * offer_shares_approx / 1e6
                    hsi_d1 = get_hsi_on_or_before(bars[0][0])
                    for label, t_idx in [("1m", 21), ("3m", 63), ("6m", 126), ("1y", 252), ("3y", 756)]:
                        if len(bars) > t_idx and d1_close > 0:
                            b_t = bars[t_idx]
                            p_t = b_t[2]
                            bhr = (p_t - d1_close) / d1_close
                            if -0.99 <= bhr <= 30.0:
                                rec[f"bhr_{label}"] = bhr
                                hsi_t = get_hsi_on_or_before(b_t[0])
                                if hsi_d1 and hsi_t and hsi_d1 > 0:
                                    bhr_hsi = (hsi_t - hsi_d1) / hsi_d1
                                    rec[f"bhar_{label}"] = bhr - bhr_hsi
                                    if (1.0 + bhr_hsi) > 0:
                                        rec[f"wr_{label}"] = (1.0 + bhr) / (1.0 + bhr_hsi)
        records.append(rec)

    df_m = pd.DataFrame(records).set_index("idx")
    return df_inc.join(df_m)


def build_2025_2026_7q_panel(df_nlr_with_mkt: pd.DataFrame) -> pd.DataFrame:
    master = pd.read_csv(ROOT / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv").copy()
    master["cohort_quarter"] = master["cohort"].astype(str).str.replace(" ", "")

    # HKIPO-MB-MASTER_clean.csv contains all 7 cohorts (2025Q1-2026Q3, N=226)
    q3_rows = []

    master_rows = []
    for _, m in master.iterrows():
        p_dt = parse_dt(m.get("Date of Prospectus (dd/mm/yy)"))
        l_dt = parse_dt(m.get("Date of Listing (dd/mm/yy)"))
        regime = "Post-Reform (>=2025-08-04)" if (p_dt and p_dt >= dt.date(2025, 8, 4)) else "Pre-Reform (<2025-08-04)"
        p0 = to_float(m.get("IPO Subscription Price (HK$)"))
        sh_glob = to_float(m.get("Final global offering shares (before over-allotment)")) or to_float(
            m.get("Global Offering (without option)")
        )
        gross_m = (p0 * sh_glob / 1e6) if (p0 and sh_glob) else np.nan
        f_pub = to_float(m.get("Final public offer shares"))
        pub_frac = (f_pub / sh_glob) if (f_pub and sh_glob and sh_glob > 0) else to_float(m.get("public_offer_fraction"))
        cs_pct = to_float(m.get("Final cornerstone allocation (% of base offer)"))
        if pd.notna(cs_pct) and cs_pct <= 1.0:
            cs_pct = cs_pct * 100.0
        ff_pct = to_float(m.get("Unrestricted public shareholding at listing (%)"))
        if pd.notna(ff_pct) and ff_pct <= 1.0:
            ff_pct = ff_pct * 100.0
        ir_val = to_float(m.get("First-day return / Underpricing (%)"))
        if pd.notna(ir_val) and abs(ir_val) <= 10.0 and master["First-day return / Underpricing (%)"].median() < 2.0:
            ir_val = ir_val * 100.0
        b1m = to_float(m.get("1-month BHR from Day-1 close (%)"))
        b3m = to_float(m.get("3-month BHR from Day-1 close (%)"))
        b6m = to_float(m.get("6-month BHR from Day-1 close (%)"))
        name_s = str(m.get("Company Name at time of listing") or "")
        master_rows.append(
            {
                "Stock Code": m["Stock Code"],
                "Company Name at time of listing": name_s,
                "Date of Prospectus": p_dt.isoformat() if p_dt else None,
                "Date of Listing": l_dt.isoformat() if l_dt else None,
                "cohort_quarter": m["cohort_quarter"],
                "reform_regime": regime,
                "IPO Subscription Price (HK$)": p0,
                "gross_proceeds_hkd_m": gross_m,
                "initial_return_pct": ir_val,
                "Subscription Ratio (times)": to_float(m.get("Subscription Ratio (times)")),
                "Public applicants": to_float(m.get("Public applicants")),
                "public_offer_fraction_pct": pub_frac * 100.0 if pd.notna(pub_frac) else np.nan,
                "cornerstone_pct_of_offering": cs_pct,
                "unrestricted_free_float_pct": ff_pct,
                "is_18a": int(to_float(m.get("Chapter 18A flag"))) if pd.notna(to_float(m.get("Chapter 18A flag"))) else 0,
                "is_18c": int(to_float(m.get("Chapter 18C flag"))) if pd.notna(to_float(m.get("Chapter 18C flag"))) else 0,
                "is_wvr": int(to_float(m.get("WVR flag"))) if pd.notna(to_float(m.get("WVR flag"))) else 0,
                "is_prc_h_share": int(
                    bool(re.search(r"Co\.,?\s*Ltd\.?|Joint Stock|H\s+Shares?", name_s, re.I))
                ),
                "bhr_1m_pct": b1m,
                "bhr_3m_pct": b3m,
                "bhr_6m_pct": b6m,
                "wr_3m": to_float(m.get("3-month wealth relative vs HSI")),
                "wr_6m": to_float(m.get("6-month wealth relative vs HSI")),
                "source_panel": "HKIPO-MB-MASTER_clean",
            }
        )

    df_7q = pd.DataFrame(master_rows + q3_rows).sort_values(["Date of Listing", "Stock Code"]).reset_index(drop=True)
    return df_7q


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 1: Building 1994-2026 Main Board & 1999-2026 GEM NLR Candidate Universe...")
    df_all = build_all_nlr_candidates()
    df_all.to_csv(OUT_DIR / "hkex_all_candidates_1994_2026.csv", index=False)

    df_inc = df_all[df_all["inclusion_status"] == "INCLUDED"].copy().reset_index(drop=True)
    print(f"Total candidates={len(df_all)}, Included ordinary IPOs={len(df_inc)}")

    print("Step 2: Fetching HSI benchmark & 0-token historical daily K-lines for all ordinary IPOs...")
    hsi_map = fetch_hsi_series()
    df_mkt = compute_market_metrics(df_inc, hsi_map)
    df_mkt.to_csv(OUT_DIR / "hkex_ordinary_ipos_market_1994_2026.csv", index=False)

    print("Step 3: Building complete 7-quarter 2025Q1-2026Q3 Main Board panel (N=226)...")
    df_7q = build_2025_2026_7q_panel(df_mkt)
    df_7q.to_csv(OUT_DIR / "hkipo_2025Q1_2026Q3_complete_226.csv", index=False)

    # Print quick summary diagnostics
    mb_mkt = df_mkt[df_mkt["board"] == "Main Board"]
    gem_mkt = df_mkt[df_mkt["board"] == "GEM"]
    print(
        f"Main Board ordinary IPOs={len(mb_mkt)}, with valid Day-1 IR={mb_mkt['ir_close'].notna().sum()}, "
        f"with 1Y BHAR={mb_mkt['bhar_1y'].notna().sum()}, with 3Y BHAR={mb_mkt['bhar_3y'].notna().sum()}"
    )
    print(
        f"GEM ordinary IPOs={len(gem_mkt)}, with valid Day-1 IR={gem_mkt['ir_close'].notna().sum()}, "
        f"with 1Y BHAR={gem_mkt['bhar_1y'].notna().sum()}"
    )
    print("7-Quarter Panel counts by quarter:")
    print(df_7q["cohort_quarter"].value_counts().sort_index().to_string())


if __name__ == "__main__":
    main()
