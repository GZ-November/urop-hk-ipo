#!/usr/bin/env python3
"""
Step 2A: Build Official Exchange-Verified Southbound Stock Connect (港股通) & HKEX CCASS Panel
=============================================================================================
Harvests and caches two primary regulatory datasets (zero manual imputation):
  1. All official Shanghai Stock Exchange / China Investment Information Services (中投信)
     Stock Connect adjustment notices (`关于沪港通下港股通标的调整的通知`, 2025-01-01 to 2026-11-12)
     via https://www.sse.com.cn/services/hkexsc/disclo/announ/.
  2. Official HKEX CCASS Mutual Market Southbound Shareholding snapshots (combined SH+SZ China Clear
     holdings and % of HKEX-listed shares) via https://www3.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk
     around the March 2026 and September 2026 HSCI semi-annual rebalancings and as of 2026-11-12.

Outputs:
  - analysis/out/overview_extensions/official_sse_ggt_notices_2025_2026.csv
  - analysis/out/overview_extensions/official_ccass_southbound_snapshots_2025_2026.csv
  - analysis/out/overview_extensions/clean_n226_official_stock_connect_panel.csv
"""
from __future__ import annotations

import html as htmllib
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path("/Users/georgezhu/Desktop/UROP HK IPO")
OUT_MAIN = ROOT / "analysis" / "out" / "overview_1994_2026"
OUT_EXT = ROOT / "analysis" / "out" / "overview_extensions"
SSE_CACHE = OUT_EXT / "sse_ggt_cache"
CCASS_CACHE = OUT_EXT / "ccass_mm_cache"
MKT_CACHE = OUT_MAIN / "market_cache"

SSE_CACHE.mkdir(parents=True, exist_ok=True)
CCASS_CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


def fetch_text(url: str, cache_file: Path | None = None, timeout: int = 15) -> str:
    if cache_file and cache_file.exists() and cache_file.stat().st_size > 200:
        return cache_file.read_text(encoding="utf-8", errors="ignore")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        txt = resp.read().decode("utf-8", errors="ignore")
    if cache_file and txt:
        cache_file.write_text(txt, encoding="utf-8")
    return txt


def clean_html_text(raw_html: str) -> str:
    no_js = re.sub(r"<script.*?</script>", " ", raw_html, flags=re.S | re.I)
    no_js = re.sub(r"<style.*?</style>", " ", no_js, flags=re.S | re.I)
    txt = htmllib.unescape(re.sub(r"<[^>]+>", " ", no_js))
    return " ".join(txt.split())


def harvest_sse_ggt_notices(hsi_dates: list[str]) -> pd.DataFrame:
    print(">>> [1/3] Harvesting official SSE Stock Connect notices (2025-01-01 to 2026-11-12)...")
    notice_links: dict[str, tuple[str, str]] = {}
    for pg in range(1, 22):
        fname = "index.shtml" if pg == 1 else f"s_list_{pg}.shtml"
        url = f"https://www.sse.com.cn/services/hkexsc/disclo/announ/{fname}"
        cf = SSE_CACHE / f"list_{fname}"
        try:
            page_html = fetch_text(url, cache_file=cf, timeout=15)
        except Exception as e:
            print(f"  Stop listing pages at {fname}: {e}")
            break
        # Match href and title in any attribute order
        anchors = re.findall(
            r'<a[^>]+href="(/services/hkexsc/disclo/announ/c/c_(\d{8})_\d+\.shtml)"[^>]*>(.*?)</a>',
            page_html,
            flags=re.S | re.I,
        )
        # Also match title attribute if body whitespace/different
        anchors2 = re.findall(
            r'href="(/services/hkexsc/disclo/announ/c/c_(\d{8})_\d+\.shtml)"[^>]*title="([^"]+)"',
            page_html,
            flags=re.I,
        )
        found_dates = []
        for href, ymd, body in anchors + anchors2:
            title = " ".join(re.sub(r"<[^>]+>", " ", htmllib.unescape(body)).split())
            found_dates.append(ymd)
            if "20241201" <= ymd <= "20261112":
                if "港股通标的" in title and "ETF" not in title:
                    notice_links[href] = (ymd, title)
        if found_dates and min(found_dates) < "20241201":
            break
        time.sleep(0.08)

    print(f"  Found {len(notice_links)} official stock adjustment notices (2024-12 to 2026-11-12).")

    records: list[dict[str, Any]] = []
    for href, (ymd, title) in sorted(notice_links.items()):
        notice_date = f"{ymd[:4]}-{ymd[4:6]}-{ymd[6:8]}"
        url = f"https://www.sse.com.cn{href}"
        cf = SSE_CACHE / Path(href).name
        try:
            raw = fetch_text(url, cache_file=cf, timeout=15)
        except Exception:
            continue
        body = clean_html_text(raw)
        doc_m = re.search(r"(中投信〔\d{4}〕\d+号)", body)
        doc_no = doc_m.group(1) if doc_m else f"SSE_{ymd}"

        # Reason classification
        if "恒生综合" in body:
            channel_reason = "HSCI_Regular_Adjustment"
        elif "稳定期结束" in body or "价格稳定期" in body:
            channel_reason = "AH_Post_Stabilization"
        elif "快速纳入" in body or "第10个交易日" in body or "指数调整" in body:
            channel_reason = "Fast_Entry_or_Index"
        elif "分拆" in body or "合并" in body or "并行买卖" in body:
            channel_reason = "Corporate_Action"
        else:
            channel_reason = "Other_Adjustment"

        # Effective date
        eff_m = re.search(r"自(\d{4})年(\d{1,2})月(\d{1,2})日", body)
        if eff_m:
            eff_date = f"{int(eff_m.group(1)):04d}-{int(eff_m.group(2)):02d}-{int(eff_m.group(3)):02d}"
        else:
            # Next HKEX trading day strictly after notice_date
            nxt = [d for d in hsi_dates if d > notice_date]
            eff_date = nxt[0] if nxt else notice_date

        # Extract stock adjustment rows directly from <tr> blocks if possible
        rows_tr = re.findall(r"<tr[^>]*>(.*?)</tr>", raw, flags=re.S | re.I)
        parsed_any = False
        for tr in rows_tr:
            tds = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, flags=re.S | re.I)
            cells = [" ".join(re.sub(r"<[^>]+>", " ", htmllib.unescape(td)).split()) for td in tds]
            if not cells:
                continue
            row_txt = " | ".join(cells)
            cm = re.search(r"\b(\d{5})\b", cells[0])
            if cm and ("调入" in row_txt or "调出" in row_txt):
                code5 = cm.group(1)
                action = "IN" if "调入" in row_txt else "OUT"
                hk_code = f"{int(code5):04d}.HK"
                records.append({
                    "notice_date": notice_date,
                    "effective_date": eff_date,
                    "doc_no": doc_no,
                    "channel_reason": channel_reason,
                    "stock_code": hk_code,
                    "code5": code5,
                    "action": action,
                    "en_name": cells[1] if len(cells) > 1 else "",
                    "cn_name": cells[2] if len(cells) > 2 else "",
                    "notice_url": url,
                })
                parsed_any = True

        # Fallback regex on flat body text if table HTML differed
        if not parsed_any:
            for cm in re.finditer(r"\b(\d{5})\b\s+([^\u4e00-\u9fff]{1,40}?)\s+(\S+)\s+(调入|调出)", body):
                code5 = cm.group(1)
                action = "IN" if cm.group(4) == "调入" else "OUT"
                records.append({
                    "notice_date": notice_date,
                    "effective_date": eff_date,
                    "doc_no": doc_no,
                    "channel_reason": channel_reason,
                    "stock_code": f"{int(code5):04d}.HK",
                    "code5": code5,
                    "action": action,
                    "en_name": cm.group(2).strip(),
                    "cn_name": cm.group(3).strip(),
                    "notice_url": url,
                })
        time.sleep(0.04)

    df_not = pd.DataFrame(records)
    if len(df_not):
        df_not = df_not.drop_duplicates(subset=["doc_no", "stock_code", "action"]).sort_values(
            ["effective_date", "stock_code"]
        ).reset_index(drop=True)
    out_p = OUT_EXT / "official_sse_ggt_notices_2025_2026.csv"
    df_not.to_csv(out_p, index=False)
    print(f"  Saved {len(df_not)} stock-level official SSE Stock Connect records -> {out_p.name}")
    return df_not


def parse_ccass_html(html: str) -> list[dict[str, Any]]:
    """Parse HKEX CCASS Mutual Market rows strictly within each <tr> to avoid cross-row bleed."""
    out = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", html, flags=re.S | re.I):
        c_m = re.search(r'col-stock-code.*?<div class="mobile-list-body"[^>]*>(.*?)</div>', tr, flags=re.S | re.I)
        n_m = re.search(r'col-stock-name.*?<div class="mobile-list-body"[^>]*>(.*?)</div>', tr, flags=re.S | re.I)
        s_m = re.search(r'col-shareholding(?:\s|").*?<div class="mobile-list-body"[^>]*>(.*?)</div>', tr, flags=re.S | re.I)
        p_m = re.search(r'col-shareholding-percent.*?<div class="mobile-list-body"[^>]*>(.*?)</div>', tr, flags=re.S | re.I)
        if not (c_m and n_m and s_m):
            continue
        digits = "".join(ch for ch in re.sub(r"<[^>]+>", "", c_m.group(1)) if ch.isdigit())
        if not digits:
            continue
        hk_code = f"{int(digits):04d}.HK"
        nm_txt = " ".join(htmllib.unescape(re.sub(r"<[^>]+>", " ", n_m.group(1))).split())
        sh_txt = re.sub(r"<[^>]+>", "", s_m.group(1)).replace(",", "").strip()
        try:
            sh_f = float(sh_txt) if sh_txt else np.nan
        except ValueError:
            sh_f = np.nan
        pct_f = np.nan
        if p_m:
            pct_txt = re.sub(r"<[^>]+>", "", p_m.group(1)).replace("%", "").replace(",", "").strip()
            if pct_txt:
                try:
                    val = float(pct_txt)
                    if 0.0 <= val <= 100.0:
                        pct_f = val
                except ValueError:
                    pct_f = np.nan
        out.append({
            "stock_code": hk_code,
            "ccass_name": nm_txt,
            "ccass_sb_shares": sh_f,
            "ccass_sb_pct": pct_f,
        })
    return out


def harvest_ccass_mutualmarket(target_dates: list[str]) -> pd.DataFrame:
    print(f">>> [2/3] Querying HKEX CCASS Mutual Market Southbound snapshots ({len(target_dates)} dates)...")
    base_url = "https://www3.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk"
    tokens_fetched = False
    vs = vsg = ev = today_v = ""

    all_rows: list[dict[str, Any]] = []
    for d_slash in target_dates:
        d_iso = d_slash.replace("/", "-")
        cache_csv = CCASS_CACHE / f"ccass_sb_{d_iso}.csv"
        cache_html = CCASS_CACHE / f"ccass_sb_{d_iso}.html"
        if cache_csv.exists() and cache_csv.stat().st_size > 100:
            sub_df = pd.read_csv(cache_csv)
            all_rows.extend(sub_df.to_dict("records"))
            print(f"  [cache] {d_iso}: {len(sub_df)} securities")
            continue

        if cache_html.exists() and cache_html.stat().st_size > 5000:
            html = cache_html.read_text(encoding="utf-8", errors="ignore")
            src_tag = "html-cache"
        else:
            if not tokens_fetched:
                init_html = urllib.request.urlopen(
                    urllib.request.Request(base_url, headers={"User-Agent": UA}), timeout=15
                ).read().decode("utf-8", errors="ignore")
                vs = re.search(r'id="__VIEWSTATE" value="([^"]+)"', init_html).group(1)
                vsg = re.search(r'id="__VIEWSTATEGENERATOR" value="([^"]+)"', init_html).group(1)
                ev_m = re.search(r'id="__EVENTVALIDATION" value="([^"]+)"', init_html)
                ev = ev_m.group(1) if ev_m else ""
                today_v = re.search(r'id="today" value="([^"]+)"', init_html).group(1)
                tokens_fetched = True

            form = {
                "__VIEWSTATE": vs,
                "__VIEWSTATEGENERATOR": vsg,
                "today": today_v,
                "sortBy": "stockcode",
                "sortDirection": "asc",
                "txtShareholdingDate": d_slash,
                "btnSearch": "Search",
            }
            if ev:
                form["__EVENTVALIDATION"] = ev
            req = urllib.request.Request(
                base_url,
                data=urllib.parse.urlencode(form).encode("utf-8"),
                headers={"User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded"},
            )
            html = urllib.request.urlopen(req, timeout=18).read().decode("utf-8", errors="ignore")
            if html:
                cache_html.write_text(html, encoding="utf-8")
            src_tag = "live"
            time.sleep(0.15)

        parsed = parse_ccass_html(html)
        for item in parsed:
            item["snapshot_date"] = d_iso
        sub_df = pd.DataFrame(parsed)
        if len(sub_df):
            sub_df.to_csv(cache_csv, index=False)
            all_rows.extend(parsed)
        print(f"  [{src_tag}]  {d_iso}: {len(parsed)} securities")

    df_cc = pd.DataFrame(all_rows)
    out_p = OUT_EXT / "official_ccass_southbound_snapshots_2025_2026.csv"
    df_cc.to_csv(out_p, index=False)
    print(f"  Saved {len(df_cc)} CCASS Southbound rows across {len(target_dates)} dates -> {out_p.name}")
    return df_cc


def build_n226_official_panel(df_not: pd.DataFrame, df_cc: pd.DataFrame) -> pd.DataFrame:
    print(">>> [3/3] Merging Official Stock Connect & CCASS verification with N=226 panel...")
    master = pd.read_csv(ROOT / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv", low_memory=False)
    m226 = pd.read_csv(OUT_MAIN / "clean_micro_panel_2025_2026_N226.csv")
    df = m226.merge(
        master[[
            "Stock Code",
            "Share base used for both public shareholding ratios",
            "H shares after IPO (base; no options)",
            "Stabilization period end date",
            "First trading day closing price (HK$)",
        ]].drop_duplicates("Stock Code"),
        left_on="stock_code",
        right_on="Stock Code",
        how="left",
    )

    reviews = [
        (pd.Timestamp("2025-06-30"), pd.Timestamp("2025-09-08"), "2025-09-08"),
        (pd.Timestamp("2025-12-31"), pd.Timestamp("2026-03-09"), "2026-03-09"),
        (pd.Timestamp("2026-06-30"), pd.Timestamp("2026-09-07"), "2026-09-07"),
    ]

    # Map earliest official IN notice per stock code
    not_in = df_not[df_not["action"] == "IN"].copy()
    first_in_map: dict[str, dict[str, Any]] = {}
    for sc, grp in not_in.groupby("stock_code"):
        g0 = grp.sort_values("effective_date").iloc[0]
        first_in_map[sc] = g0.to_dict()

    # Map CCASS Mutual Market percentages and shares
    cc_first_date: dict[str, str] = {}
    cc_20261112: dict[str, tuple[float, float]] = {}
    cc_by_date: dict[tuple[str, str], tuple[float, float]] = {}
    for _, r in df_cc.iterrows():
        sc = r["stock_code"]
        sd = r["snapshot_date"]
        pct = float(r["ccass_sb_pct"]) if pd.notna(r["ccass_sb_pct"]) else np.nan
        sh = float(r["ccass_sb_shares"]) if pd.notna(r["ccass_sb_shares"]) else np.nan
        cc_by_date[(sc, sd)] = (pct, sh)
        if sd == "2026-11-12":
            cc_20261112[sc] = (pct, sh)
        if sc not in cc_first_date or sd < cc_first_date[sc]:
            cc_first_date[sc] = sd

    # Map exact snapshot pair around each review
    review_cc_snaps = {
        "2026-03-09": ("2026-03-06", "2026-03-13", "2026-03-23"),
        "2026-09-07": ("2026-09-04", "2026-09-11", "2026-09-21"),
    }
    semiannual_eff_dates = [
        pd.Timestamp("2025-03-10"),
        pd.Timestamp("2025-09-08"),
        pd.Timestamp("2026-03-09"),
        pd.Timestamp("2026-09-07"),
    ]

    def resolve_cc_pct(sc: str, sd: str, hkex_shs: float, ld: pd.Timestamp) -> float:
        if ld > pd.Timestamp(sd):
            return np.nan
        val = cc_by_date.get((sc, sd))
        if val is None:
            return 0.0
        pct, sh = val
        if pd.notna(pct) and 0.0 <= pct <= 100.0:
            return pct
        if pd.notna(sh) and sh >= 0.0 and pd.notna(hkex_shs) and hkex_shs > 0.0:
            return min(100.0, float(sh / hkex_shs * 100.0))
        return np.nan

    rows = []
    for _, r in df.iterrows():
        sc = r["stock_code"]
        num = int(sc.split(".")[0])
        ld_str = str(r["listing_date"])[:10]
        ld = pd.Timestamp(ld_str)
        cpath = MKT_CACHE / f"{num:04d}.HK_{ld_str}.json"
        if not cpath.exists():
            cands = sorted(MKT_CACHE.glob(f"{num:04d}.HK_*.json"))
            cpath = cands[0] if cands else None
        bars = json.loads(cpath.read_text()) if (cpath and cpath.exists()) else []
        bdf = pd.DataFrame(bars, columns=["date", "open", "close", "high", "low", "vol", "turn"]) if bars else pd.DataFrame()
        if len(bdf):
            bdf["date_dt"] = pd.to_datetime(bdf["date"])
            # Rescale hfq series to true nominal listing-day close to prevent recycled-ticker split distortion
            d1_true = pd.to_numeric(r["First trading day closing price (HK$)"], errors="coerce")
            b0_close = float(bdf.iloc[0]["close"])
            scale = float(d1_true / b0_close) if (pd.notna(d1_true) and d1_true > 0 and b0_close > 0) else 1.0
            bdf["true_close"] = bdf["close"] * scale

        tot_shs = pd.to_numeric(r["Share base used for both public shareholding ratios"], errors="coerce")
        h_shs = pd.to_numeric(r["H shares after IPO (base; no options)"], errors="coerce")
        hkex_shs = h_shs if (int(r["is_prc_h_share"]) == 1 and pd.notna(h_shs) and h_shs > 0) else tot_shs

        # Official notice & CCASS & refined WVR flag
        ni = first_in_map.get(sc)
        is_wvr_eff = int(
            (int(r["is_wvr"]) == 1)
            or str(r["company_name"]).strip().endswith("- W")
            or ("-W" in str(ni.get("en_name", "")) if ni else False)
        )
        in_ccass_final = int(sc in cc_20261112)
        ever_inc = int(bool(ni or in_ccass_final))
        official_eff_date = ni["effective_date"] if ni else (cc_first_date.get(sc) if in_ccass_final else None)
        official_doc_no = ni["doc_no"] if ni else ("CCASS_MM_ONLY" if in_ccass_final else None)

        if not ever_inc:
            official_reason = "Not_Included"
        elif int(r["is_ah_dual_listed"]) == 1:
            official_reason = "AH_Post_Stabilization"
        elif is_wvr_eff == 1 and official_eff_date and (pd.Timestamp(official_eff_date) - ld).days >= 180:
            official_reason = "WVR_6M20D_Entry"
        elif official_eff_date and any(abs((pd.Timestamp(official_eff_date) - se).days) <= 5 for se in semiannual_eff_dates):
            official_reason = "HSCI_SemiAnnual_Review"
        else:
            official_reason = "Fast_Entry_or_Index"

        # Assign first eligible semi-annual HSCI review for Non-A+H IPOs
        first_rev_cut = first_rev_eff = None
        hsci_mcap_me_avg = hsci_mcap_daily_avg = np.nan
        official_admitted_at_rev = np.nan
        cc_pre = cc_post4 = cc_post10 = np.nan

        if int(r["is_ah_dual_listed"]) == 0 and len(bdf) and pd.notna(hkex_shs) and hkex_shs > 0:
            for rev_cut, eff_dt, eff_str in reviews:
                if ld <= rev_cut:
                    first_rev_cut = str(rev_cut.date())
                    first_rev_eff = eff_str
                    pre_bdf = bdf[bdf["date_dt"] <= rev_cut].copy()
                    if len(pre_bdf):
                        hsci_mcap_daily_avg = float((hkex_shs * pre_bdf["true_close"].mean()) / 1e9)
                        pre_bdf["ym"] = pre_bdf["date_dt"].dt.to_period("M")
                        me_closes = pre_bdf.groupby("ym")["true_close"].last()
                        hsci_mcap_me_avg = float((hkex_shs * me_closes.mean()) / 1e9)

                    in_sse_rev = bool(
                        ni and (eff_dt - pd.Timedelta(days=2) <= pd.Timestamp(ni["effective_date"]) <= eff_dt + pd.Timedelta(days=5))
                    )
                    in_sse_already = bool(ni and pd.Timestamp(ni["effective_date"]) <= eff_dt + pd.Timedelta(days=5))
                    if eff_str in review_cc_snaps:
                        d_pre, d_p4, d_p10 = review_cc_snaps[eff_str]
                        # Evaluate semi-annual CCASS Pre/+4d/+10d windows only when the issuer's official Connect event
                        # aligns with this semi-annual effective date (or never entered); non-semiannual Fast-Entry / WVR
                        # cohorts enter months earlier and would otherwise leak post-entry holdings into "Pre".
                        same_event_date = (
                            official_reason in ("HSCI_SemiAnnual_Review", "Not_Included")
                            or (
                                official_eff_date is not None
                                and abs((pd.Timestamp(official_eff_date) - eff_dt).days) <= 5
                            )
                        )
                        if same_event_date:
                            cc_pre = resolve_cc_pct(sc, d_pre, hkex_shs, ld)
                            cc_post4 = resolve_cc_pct(sc, d_p4, hkex_shs, ld)
                            cc_post10 = resolve_cc_pct(sc, d_p10, hkex_shs, ld)
                        in_cc_post = (sc, d_p4) in cc_by_date or (sc, d_p10) in cc_by_date
                        in_cc_pre = (sc, d_pre) in cc_by_date
                        official_admitted_at_rev = int((in_sse_rev or (in_cc_post and not in_cc_pre)) or in_sse_already)
                    else:
                        in_202511 = (sc, "2025-11-14") in cc_by_date and not (ni and pd.Timestamp(ni["effective_date"]) > pd.Timestamp("2025-09-12"))
                        official_admitted_at_rev = int(in_sse_already or in_202511)
                    break

        cc_nov12 = resolve_cc_pct(sc, "2026-11-12", hkex_shs, ld)

        rows.append({
            "stock_code": sc,
            "company_name": r["company_name"],
            "cohort_quarter": r["cohort_quarter"],
            "listing_date": ld_str,
            "is_ah_dual_listed": int(r["is_ah_dual_listed"]),
            "is_prc_h_share": int(r["is_prc_h_share"]),
            "is_wvr": is_wvr_eff,
            "hkex_listed_shares": hkex_shs,
            "official_ggt_ever_included": ever_inc,
            "official_ggt_eff_date": official_eff_date,
            "official_ggt_doc_no": official_doc_no,
            "official_entry_channel": official_reason,
            "first_hsci_cutoff": first_rev_cut,
            "first_hsci_eff_date": first_rev_eff,
            "hsci_month_end_avg_mv_bn": round(hsci_mcap_me_avg, 4) if pd.notna(hsci_mcap_me_avg) else np.nan,
            "hsci_daily_avg_mv_bn": round(hsci_mcap_daily_avg, 4) if pd.notna(hsci_mcap_daily_avg) else np.nan,
            "official_admitted_at_review": official_admitted_at_rev,
            "ccass_sb_pct_pre_eff": round(cc_pre, 4) if pd.notna(cc_pre) else np.nan,
            "ccass_sb_pct_post4d": round(cc_post4, 4) if pd.notna(cc_post4) else np.nan,
            "ccass_sb_pct_post10d": round(cc_post10, 4) if pd.notna(cc_post10) else np.nan,
            "ccass_sb_pct_20261112": round(cc_nov12, 4) if pd.notna(cc_nov12) else np.nan,
        })

    out_df = pd.DataFrame(rows)
    out_p = OUT_EXT / "clean_n226_official_stock_connect_panel.csv"
    out_df.to_csv(out_p, index=False)

    non_ah = out_df[out_df["first_hsci_eff_date"].notna()]
    above = non_ah[non_ah["hsci_month_end_avg_mv_bn"] >= 5.0]
    below = non_ah[non_ah["hsci_month_end_avg_mv_bn"] < 5.0]
    print(f"  Saved {out_p.name} (N={len(out_df)})")
    print(f"  Overall N=226 Official Southbound Included Ever: {out_df['official_ggt_ever_included'].sum()}/{len(out_df)} "
          f"(A+H: {out_df[out_df['is_ah_dual_listed']==1]['official_ggt_ever_included'].sum()}/{(out_df['is_ah_dual_listed']==1).sum()}, "
          f"Non-A+H: {out_df[out_df['is_ah_dual_listed']==0]['official_ggt_ever_included'].sum()}/{(out_df['is_ah_dual_listed']==0).sum()})")
    print(f"  First-Stage Compliance at HSCI Reviews (N={len(non_ah)}):")
    print(f"    MV >= HK$5.0B (N={len(above)}): {above['official_admitted_at_review'].mean()*100:.1f}% officially admitted")
    print(f"    MV <  HK$5.0B (N={len(below)}): {below['official_admitted_at_review'].mean()*100:.1f}% officially admitted")
    return out_df


def main() -> None:
    hsi_map = json.loads((MKT_CACHE / "hkHSI_1994_2026.json").read_text())
    hsi_dates = sorted(hsi_map.keys())
    df_not = harvest_sse_ggt_notices(hsi_dates)
    snap_dates = [
        "2025/11/14",
        "2026/02/20", "2026/03/06", "2026/03/09", "2026/03/13", "2026/03/23",
        "2026/06/30", "2026/08/21", "2026/09/04", "2026/09/07", "2026/09/11", "2026/09/21",
        "2026/11/12",
    ]
    df_cc = harvest_ccass_mutualmarket(snap_dates)
    build_n226_official_panel(df_not, df_cc)


if __name__ == "__main__":
    main()
