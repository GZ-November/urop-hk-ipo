#!/usr/bin/env python3
"""
fetch_and_build_hkex_hml_and_peers.py
=====================================
Caches official and financial-statement metadata needed for:
1. HKEX strictly-seasoned (>36M post-IPO) Carhart 4-factor (`HML_seasoned`)
   across 2000-2026Q3 and 2008-2026Q3, cross-checked against Kenneth French
   Asia-Pacific ex-Japan 3F+MOM factors (1994-2026Q3).
2. Industry x Size matched-firm daily CAR benchmarks for the 2025-2026 lockup
   natural experiment (using official HKEX ListOfSecurities + Eastmoney
   BELONG_INDUSTRY / INDUSTRY_TYPE + Tencent hfq daily bars through 2026-11-12).
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import io
import json
from pathlib import Path
import time
import urllib.request
import zipfile

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
OV_DIR = REPO_ROOT / "analysis" / "out" / "overview_1994_2026"
EXT_DIR = REPO_ROOT / "analysis" / "out" / "overview_extensions"
PEER_DAILY_DIR = OV_DIR / "matched_peer_daily_cache"
PEER_DAILY_DIR.mkdir(parents=True, exist_ok=True)
EXT_DIR.mkdir(parents=True, exist_ok=True)

AS_OF_STR = "2026-11-12"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}


def fetch_json_retry(url: str, timeout: int = 12, retries: int = 3) -> dict:
    for att in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if att == retries - 1:
                raise
            time.sleep(0.5 * (att + 1))
    return {}


def cache_kenfrench_apxj() -> pd.DataFrame:
    out_path = EXT_DIR / "kenfrench_apxj_factors_1994_2026.csv"
    if out_path.exists():
        print(f"[1/4] Ken French APxJP already cached: {out_path}")
        return pd.read_csv(out_path)

    def _parse_kf_zip(fname: str, expected_cols: list[str]) -> pd.DataFrame:
        url = f"https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/{fname}"
        raw = urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=15).read()
        z = zipfile.ZipFile(io.BytesIO(raw))
        txt = z.open(z.namelist()[0]).read().decode("latin1")
        rows = []
        in_monthly = False
        for line in txt.splitlines():
            s = line.strip()
            if not s:
                if in_monthly and len(rows) > 100:
                    break
                continue
            parts = [p.strip() for p in s.split(",")]
            if len(parts) >= 2 and parts[0].isdigit() and len(parts[0]) == 6:
                in_monthly = True
                ym = f"{parts[0][:4]}-{parts[0][4:6]}"
                vals = [float(x) if x != "-99.99" else np.nan for x in parts[1 : 1 + len(expected_cols)]]
                rows.append([ym] + vals)
        return pd.DataFrame(rows, columns=["year_month"] + expected_cols)

    df3 = _parse_kf_zip("Asia_Pacific_ex_Japan_3_Factors_CSV.zip", ["kf_mkt_rf", "kf_smb", "kf_hml", "kf_rf"])
    dfm = _parse_kf_zip("Asia_Pacific_ex_Japan_MOM_Factor_CSV.zip", ["kf_wml"])
    kf = df3.merge(dfm, on="year_month", how="inner")
    kf = kf[(kf["year_month"] >= "1993-12") & (kf["year_month"] <= "2026-10")].reset_index(drop=True)
    kf.to_csv(out_path, index=False)
    print(f"[1/4] Cached Ken French APxJP factors: {len(kf)} months ({kf['year_month'].min()}..{kf['year_month'].max()})")
    return kf


def cache_hkex_list_of_securities() -> pd.DataFrame:
    out_path = EXT_DIR / "hkex_list_of_securities_20261112.csv"
    if out_path.exists():
        print(f"[2/4] HKEX ListOfSecurities already cached: {out_path}")
        return pd.read_csv(out_path, dtype={"code5": str})
    url = "https://www.hkex.com.hk/eng/services/trading/securities/securitieslists/ListOfSecurities.xlsx"
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=20).read()
    df_xl = pd.read_excel(io.BytesIO(raw), skiprows=2)
    eq = df_xl[df_xl["Category"].astype(str).str.contains("Equity", case=False, na=False)].copy()
    eq["code5"] = pd.to_numeric(eq["Stock Code"], errors="coerce").dropna().astype(int).map(lambda x: f"{x:05d}")
    eq = eq.dropna(subset=["code5"]).copy()
    eq.to_csv(out_path, index=False)
    print(f"[2/4] Cached HKEX active equities: {len(eq)} rows")
    return eq


def cache_eastmoney_orgprofile() -> pd.DataFrame:
    out_path = EXT_DIR / "hkex_eastmoney_orgprofile_20261112.csv"
    if out_path.exists():
        print(f"[3/4] Eastmoney HK OrgProfile already cached: {out_path}")
        return pd.read_csv(out_path, dtype={"SECURITY_CODE": str})

    cols = "SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,ORG_EN_ABBR,BELONG_INDUSTRY,INDUSTRY_TYPE,LISTING_DATE,BELONG_MARKET,REG_PLACE,ORG_TYPE"
    first = fetch_json_retry(
        f"https://datacenter.eastmoney.com/securities/api/data/v1/get?reportName=RPT_HKF10_INFO_ORGPROFILE&columns={cols}&pageSize=500&pageNumber=1"
    )
    pages = int(first["result"]["pages"])
    all_rows = list(first["result"]["data"])

    def _get_page(p: int) -> list[dict]:
        u = f"https://datacenter.eastmoney.com/securities/api/data/v1/get?reportName=RPT_HKF10_INFO_ORGPROFILE&columns={cols}&pageSize=500&pageNumber={p}"
        return fetch_json_retry(u)["result"]["data"]

    with ThreadPoolExecutor(max_workers=8) as ex:
        for res in ex.map(_get_page, range(2, pages + 1)):
            all_rows.extend(res)

    df_op = pd.DataFrame(all_rows).drop_duplicates("SECUCODE")
    df_op["SECURITY_CODE"] = df_op["SECURITY_CODE"].astype(str).str.zfill(5)
    df_op.to_csv(out_path, index=False)
    print(f"[3/4] Cached Eastmoney HK OrgProfile: {len(df_op)} rows across {pages} pages")
    return df_op


def cache_eastmoney_annual_financials() -> pd.DataFrame:
    out_path = EXT_DIR / "hkex_eastmoney_annual_equity_1999_2026.csv"
    if out_path.exists():
        print(f"[4/4] Eastmoney HK Annual Financials already cached: {out_path}")
        return pd.read_csv(out_path, dtype={"SECURITY_CODE": str})

    cols = "SECUCODE,SECURITY_CODE,REPORT_DATE,DATE_TYPE_CODE,TOTAL_PARENT_EQUITY,BPS,TOTAL_MARKET_CAP,PB_TTM,CURRENCY,IS_CNY_CODE"
    base_u = (
        "https://datacenter.eastmoney.com/securities/api/data/v1/get?"
        f"reportName=RPT_HKF10_FN_MAININDICATOR&columns={cols}&pageSize=500&filter=(DATE_TYPE_CODE%3D%27001%27)"
    )
    first = fetch_json_retry(base_u + "&pageNumber=1", timeout=15)
    pages = int(first["result"]["pages"])
    all_rows = list(first["result"]["data"])
    print(f"    Fetching {pages} pages of annual HKEX financials (~{first['result']['count']:,} firm-years)...")

    def _get_fin_page(p: int) -> list[dict]:
        r = fetch_json_retry(base_u + f"&pageNumber={p}", timeout=15, retries=4)
        return (r.get("result") or {}).get("data", [])

    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(_get_fin_page, p): p for p in range(2, pages + 1)}
        done = 1
        for f in as_completed(futs):
            all_rows.extend(f.result())
            done += 1
            if done % 50 == 0:
                print(f"      fetched {done}/{pages} pages...")

    df_fin = pd.DataFrame(all_rows)
    df_fin["SECURITY_CODE"] = df_fin["SECURITY_CODE"].astype(str).str.zfill(5)
    df_fin["report_ym"] = df_fin["REPORT_DATE"].astype(str).str.slice(0, 7)
    df_fin.to_csv(out_path, index=False)
    print(f"[4/4] Cached Eastmoney HK Annual Financials: {len(df_fin):,} rows")
    return df_fin


def fetch_daily_hfq_peer(sym: str) -> tuple[str, int]:
    """Fetch & cache daily hfq bars (2024-11-01 to 2026-11-12) for a matched seasoned peer."""
    cfile = PEER_DAILY_DIR / f"{sym}.json"
    if cfile.exists():
        try:
            d = json.loads(cfile.read_text(encoding="utf-8"))
            if len(d) > 50 and d[-1][0] >= "2026-11-01":
                return sym, len(d)
        except Exception:
            pass
    url = f"https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?param={sym},day,2024-11-01,{AS_OF_STR},600,hfq"
    for att in range(3):
        try:
            raw = fetch_json_retry(url, timeout=12, retries=2)
            sub = (raw.get("data") or {}).get(sym) or {}
            rows = sub.get("hfqday") or sub.get("day") or []
            clean_rows = []
            for r in rows:
                ds = str(r[0])[:10]
                if ds <= AS_OF_STR:
                    clean_rows.append([ds, float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5])])
            cfile.write_text(json.dumps(clean_rows), encoding="utf-8")
            return sym, len(clean_rows)
        except Exception:
            time.sleep(0.3 * (att + 1))
    return sym, 0


def build_matched_peers_and_cache_bars(hkex_eq: pd.DataFrame, org_prof: pd.DataFrame) -> pd.DataFrame:
    """Select k=5 strictly-seasoned (>36M) industry x size matched peers per N=226 IPO and fetch daily hfq bars."""
    master = pd.read_csv(OV_DIR / "hkipo_33y_master_panel_1994_2026_tier1_complete.csv", low_memory=False)
    paired = pd.read_csv(EXT_DIR / "clean_2025_2026_paired_6m_12m_lockup_panel.csv")
    mb_master = pd.read_csv(REPO_ROOT / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv", low_memory=False)

    # Identify all 2022-2026 IPOs so they are strictly EXCLUDED from the seasoned peer pool
    recent_codes = set()
    for _, r in master[master["cohort_year"] >= 2022].iterrows():
        dig = "".join(ch for ch in str(r["stock_code"]) if ch.isdigit())
        if dig:
            recent_codes.add(f"{int(dig):05d}")

    # Active HKEX Main Board equities
    active_mb = hkex_eq[hkex_eq["Sub-Category"].astype(str).str.contains("Main Board", case=False, na=False)].copy()
    active_mb = active_mb.drop_duplicates("code5")

    # Merge OrgProfile industry & listing date
    prof_sub = org_prof[org_prof["BELONG_MARKET"].astype(str).str.contains("主板", na=False) | org_prof["BELONG_MARKET"].isna()].copy()
    prof_sub = prof_sub.drop_duplicates("SECURITY_CODE")
    pool = active_mb.merge(
        prof_sub[["SECURITY_CODE", "BELONG_INDUSTRY", "INDUSTRY_TYPE", "LISTING_DATE"]],
        left_on="code5", right_on="SECURITY_CODE", how="left",
    )
    pool["list_dt_str"] = pool["LISTING_DATE"].astype(str).str.slice(0, 10)
    pool = pool[
        (~pool["code5"].isin(recent_codes))
        & (pool["list_dt_str"] <= "2021-12-31")
        & pool["BELONG_INDUSTRY"].notna()
        & (pool["BELONG_INDUSTRY"].astype(str) != "--")
    ].copy()

    # Get 2025-01 / latest seasoned market cap from seasoned_monthly_hfq_cache
    seas_dir = OV_DIR / "seasoned_monthly_hfq_cache"
    mcap_map: dict[str, float] = {}
    for c5 in pool["code5"]:
        sp = seas_dir / f"hk{c5}.json"
        if sp.exists():
            try:
                sd = json.loads(sp.read_text())
                cur_mc = sd.get("cur_mcap_hkd")
                bars = sd.get("bars", [])
                if cur_mc and cur_mc > 0 and bars:
                    p_last = float(bars[-1][1])
                    p_2412 = next((float(b[1]) for b in bars if b[0] >= "2024-12"), p_last)
                    if p_last > 0 and p_2412 > 0:
                        mcap_map[c5] = float(cur_mc) * (p_2412 / p_last)
            except Exception:
                pass
    pool["peer_mcap_hkd"] = pool["code5"].map(mcap_map)
    pool = pool.dropna(subset=["peer_mcap_hkd"]).copy()
    pool = pool[pool["peer_mcap_hkd"] > 0].copy()
    pool["log_mcap"] = np.log(pool["peer_mcap_hkd"])
    pool["broad_sector"] = pool["INDUSTRY_TYPE"].astype(str).str.split("-").str[0].str.strip()
    print(f"    Strictly seasoned (>36M) Main Board peer pool with verified industry & mcap: {len(pool)} firms")

    # Prepare N=226 treated IPOs with Eastmoney BELONG_INDUSTRY + fallback HSICS-2 + listing market cap
    mb_master["code5"] = mb_master["Stock Code"].astype(str).str.extract(r"(\d+)")[0].astype(int).map(lambda x: f"{x:05d}")
    paired["code5"] = paired["stock_code"].astype(str).str.extract(r"(\d+)")[0].astype(int).map(lambda x: f"{x:05d}")

    # Listing-day market cap from master panel
    master_clean = master[master["flag_recycled_or_transferred_ticker"].fillna(0) == 0].copy()
    master_clean["code5"] = master_clean["stock_code"].astype(str).str.extract(r"(\d+)")[0].dropna().astype(int).map(lambda x: f"{x:05d}")
    sh = pd.to_numeric(master_clean["ext_total_shares_listed"], errors="coerce")
    p0 = pd.to_numeric(master_clean["offer_price_hkd"], errors="coerce")
    pr = pd.to_numeric(master_clean["funds_raised_total_hkd"], errors="coerce")
    master_clean["ipo_mcap_hkd"] = np.where(sh.notna() & (sh > 0) & p0.notna(), sh * p0, pr * 4.0)
    mcap_ipo_map = master_clean.dropna(subset=["ipo_mcap_hkd"]).drop_duplicates("code5").set_index("code5")["ipo_mcap_hkd"].to_dict()

    trt = paired[["stock_code", "code5", "listing_date"]].drop_duplicates("code5").merge(
        prof_sub[["SECURITY_CODE", "BELONG_INDUSTRY", "INDUSTRY_TYPE"]],
        left_on="code5", right_on="SECURITY_CODE", how="left",
    )
    trt = trt.merge(mb_master[["code5", "Industry classification code"]], on="code5", how="left")
    trt["ipo_mcap_hkd"] = trt["code5"].map(mcap_ipo_map)
    trt["log_mcap"] = np.log(trt["ipo_mcap_hkd"].clip(lower=1e7))
    trt["broad_sector"] = trt["INDUSTRY_TYPE"].astype(str).str.split("-").str[0].str.strip()

    # Map fallback HSICS 2-digit prefix to Eastmoney broad sector if needed
    hsic2_to_broad = {
        "00": "原材料", "05": "能源", "10": "工业", "23": "可选消费", "25": "日常消费",
        "28": "医疗保健", "35": "电讯服务", "40": "公用事业", "50": "金融", "53": "综合企业",
        "60": "房地产", "70": "信息技术",
    }

    match_rows = []
    unique_peers: set[str] = set()
    for _, r in trt.iterrows():
        ind = r["BELONG_INDUSTRY"]
        broad = r["broad_sector"]
        hsic2 = str(r["Industry classification code"])[:2].zfill(2) if pd.notna(r["Industry classification code"]) else ""
        if pd.isna(broad) or broad == "nan":
            broad = hsic2_to_broad.get(hsic2, "工业")

        cand_fine = pool[pool["BELONG_INDUSTRY"] == ind].copy() if pd.notna(ind) else pool.iloc[0:0].copy()
        match_tier = "Exact_Industry"
        if len(cand_fine) >= 5:
            cand = cand_fine
        else:
            cand_broad = pool[pool["broad_sector"] == broad].copy()
            if len(cand_broad) >= 5:
                cand = cand_broad
                match_tier = "Broad_Sector"
            else:
                cand = pool.copy()
                match_tier = "Size_Only"

        cand["dist"] = np.abs(cand["log_mcap"] - r["log_mcap"])
        top5 = cand.sort_values("dist").head(5)
        peer_codes = top5["code5"].tolist()
        for pc in peer_codes:
            unique_peers.add(f"hk{pc}")
        match_rows.append({
            "stock_code": r["stock_code"],
            "code5": r["code5"],
            "belong_industry": ind,
            "broad_sector": broad,
            "match_tier": match_tier,
            "ipo_mcap_hkd": r["ipo_mcap_hkd"],
            "peer_codes_json": json.dumps(peer_codes),
            "mean_peer_log_mcap_diff": float(top5["dist"].mean()),
        })

    match_df = pd.DataFrame(match_rows)
    match_df.to_csv(EXT_DIR / "lockup_n226_industry_size_matched_peers.csv", index=False)
    print(f"    Matched {len(match_df)} IPOs across {len(unique_peers)} unique seasoned peers "
          f"(Exact_Industry={(match_df['match_tier']=='Exact_Industry').sum()}, "
          f"Broad_Sector={(match_df['match_tier']=='Broad_Sector').sum()}, "
          f"Size_Only={(match_df['match_tier']=='Size_Only').sum()})")

    # Fetch daily hfq bars for unique peers
    print(f"    Caching 2024-11..2026-11 daily hfq bars for {len(unique_peers)} seasoned peers...")
    ok_n = 0
    with ThreadPoolExecutor(max_workers=20) as ex:
        for _, nbars in ex.map(fetch_daily_hfq_peer, sorted(unique_peers)):
            if nbars > 50:
                ok_n += 1
    print(f"    Cached daily hfq bars for {ok_n}/{len(unique_peers)} unique seasoned peers.")
    return match_df


def main() -> None:
    print("=" * 80)
    print("CACHING KEN FRENCH APxJP, HKEX SECURITIES, ORG PROFILE & ANNUAL BOOK EQUITY")
    print("=" * 80)
    cache_kenfrench_apxj()
    hkex_eq = cache_hkex_list_of_securities()
    org_prof = cache_eastmoney_orgprofile()
    cache_eastmoney_annual_financials()
    build_matched_peers_and_cache_bars(hkex_eq, org_prof)
    print("ALL EXTERNAL CACHES BUILT SUCCESSFULLY.")


if __name__ == "__main__":
    main()
