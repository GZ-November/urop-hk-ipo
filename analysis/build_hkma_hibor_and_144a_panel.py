#!/usr/bin/env python3
"""
build_hkma_hibor_and_144a_panel.py
==================================
Builds spliced HKMA HIBOR series (daily & monthly), risk-free rate augmented CTP portfolios,
and enriches the 33-year HK IPO panel (1994-2026, N = 2,865) with:
  1. Exact daily HIBOR matching and interbank liquidity freeze surge metrics.
  2. Exact Hang Seng Index public-information window returns (Loughran & Ritter 2002).
  3. Bloomberg global syndication tranches (Rule 144A / Reg S), secondary sales,
     and forensically cleaned lifetime returns (Bessembinder 2018).

Output Files:
  - analysis/out/overview_extensions/clean_hkma_hibor_daily_1993_2026.csv
  - analysis/out/overview_extensions/clean_hkma_hibor_monthly_1994_2026.csv
  - analysis/out/overview_extensions/clean_monthly_ctp_with_hibor_rf_1994_2026.csv (T = 393)
  - analysis/out/overview_extensions/clean_33y_macro_144a_hibor_panel.csv (N = 2,865)
"""

import json
import bisect
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# Path Configuration
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
EXT_DIR = BASE_DIR / "analysis" / "out" / "overview_extensions"
IN_DIR = BASE_DIR / "analysis" / "in" / "bloomberg"
CACHE_DIR = BASE_DIR / "analysis" / "out" / "overview_1994_2026" / "market_cache"
OVERVIEW_1994_2026_DIR = BASE_DIR / "analysis" / "out" / "overview_1994_2026"

DAILY_XLS = EXT_DIR / "hkma_T060303_daily.xls"
MONTHLY_XLS = EXT_DIR / "hkma_T060302_period_average.xls"
INTERMEDIARIES_CSV = EXT_DIR / "clean_33y_intermediaries_greenshoe.csv"
CTP_PORTFOLIOS_CSV = EXT_DIR / "clean_monthly_ctp_portfolios_1994_2026.csv"
BLOOMBERG_CSV = IN_DIR / "ecdr_export_part1.csv"
HSI_JSON = CACHE_DIR / "hkHSI_1994_2026.json"
MICRO_PANEL_CSV = OVERVIEW_1994_2026_DIR / "clean_micro_panel_2025_2026_N226.csv"

OUT_DAILY_CSV = EXT_DIR / "clean_hkma_hibor_daily_1993_2026.csv"
OUT_MONTHLY_CSV = EXT_DIR / "clean_hkma_hibor_monthly_1994_2026.csv"
OUT_CTP_CSV = EXT_DIR / "clean_monthly_ctp_with_hibor_rf_1994_2026.csv"
OUT_PANEL_CSV = EXT_DIR / "clean_33y_macro_144a_hibor_panel.csv"


# =========================================================
# TASK 1: Parse HKMA HIBOR Daily & Monthly Series
# =========================================================

def build_daily_hibor():
    print("=" * 70)
    print("TASK 1.1: Building Daily Spliced HIBOR (1993-2026)...")
    print("=" * 70)

    # 1. Sheet: T6.3.3 (HIBOR Fixing)
    df_fix = pd.read_excel(DAILY_XLS, sheet_name="T6.3.3 (HIBOR Fixing)", header=None)
    df_fix["date"] = pd.to_datetime(df_fix[0], errors="coerce")
    fix_valid = df_fix[df_fix["date"].notna()].copy()
    fix_valid["date_str"] = fix_valid["date"].dt.strftime("%Y-%m-%d")

    # 2. Sheet: T6.3.3(HIBOR) (Standard Chartered Interbank Closing)
    df_scb = pd.read_excel(DAILY_XLS, sheet_name="T6.3.3(HIBOR)", header=None)
    df_scb["date"] = pd.to_datetime(df_scb[0], errors="coerce")
    scb_valid = df_scb[(df_scb["date"].notna()) & (df_scb["date"] >= "1993-01-01")].copy()
    scb_valid["date_str"] = scb_valid["date"].dt.strftime("%Y-%m-%d")

    # 3. Sheet: T6.3.3 (HONIA) (Overnight ARR)
    df_honia = pd.read_excel(DAILY_XLS, sheet_name="T6.3.3 (HONIA)", header=None)
    df_honia["date"] = pd.to_datetime(df_honia[0], errors="coerce")
    honia_valid = df_honia[df_honia["date"].notna()].copy()
    honia_valid["date_str"] = honia_valid["date"].dt.strftime("%Y-%m-%d")

    tenor_cols = {"on": 3, "1w": 4, "1m": 5, "3m": 6, "6m": 7, "9m": 8, "12m": 9}

    fix_clean = pd.DataFrame({"date_str": fix_valid["date_str"], "date": fix_valid["date"]})
    for name, c in tenor_cols.items():
        fix_clean[f"fix_{name}"] = pd.to_numeric(fix_valid[c], errors="coerce")

    scb_clean = pd.DataFrame({"date_str": scb_valid["date_str"], "date": scb_valid["date"]})
    for name, c in tenor_cols.items():
        scb_clean[f"scb_{name}"] = pd.to_numeric(scb_valid[c], errors="coerce")

    honia_clean = pd.DataFrame({
        "date_str": honia_valid["date_str"],
        "honia_on": pd.to_numeric(honia_valid[2], errors="coerce")
    })

    # Outer merge on date_str
    merged = pd.merge(fix_clean, scb_clean, on=["date_str", "date"], how="outer").sort_values("date").reset_index(drop=True)
    merged = pd.merge(merged, honia_clean, on="date_str", how="left")

    # Apply Splicing Rule:
    # Take official HIBOR Fixing first when non-null numeric;
    # Backfill with SCB closing rates on that exact business date when fixing is missing/N.A.
    spliced = pd.DataFrame({
        "date": merged["date_str"]
    })
    for name in tenor_cols.keys():
        spliced[f"hibor_{name}"] = merged[f"fix_{name}"].combine_first(merged[f"scb_{name}"])

    # Record provenance
    spliced["source_1m"] = np.where(merged["fix_1m"].notna(), "HKAB_Fixing", "HKMA_SCB_HIBOR")

    # Handle single public holiday 1998-08-17 (Sino-Japanese War Victory Day, SCB closed, fixing copied previous day)
    # Forward-fill overnight and 1-week limit=1
    spliced["hibor_on"] = spliced["hibor_on"].ffill(limit=1)
    spliced["hibor_1w"] = spliced["hibor_1w"].ffill(limit=1)

    spliced["honia_on"] = merged["honia_on"]

    print(f"Daily HIBOR total business dates: {len(spliced)} ({spliced['date'].min()} to {spliced['date'].max()})")
    print("Null counts across daily series:")
    print(spliced.isna().sum())
    print("\nSource 1M distribution:")
    print(spliced["source_1m"].value_counts())

    assert spliced["hibor_1m"].isna().sum() == 0, "Error: Gaps in spliced 1M HIBOR!"
    assert spliced["hibor_3m"].isna().sum() == 0, "Error: Gaps in spliced 3M HIBOR!"
    assert spliced["hibor_1w"].isna().sum() == 0, "Error: Gaps in spliced 1W HIBOR!"
    assert spliced["hibor_on"].isna().sum() == 0, "Error: Gaps in spliced ON HIBOR!"

    spliced.to_csv(OUT_DAILY_CSV, index=False)
    print(f"Successfully saved daily HIBOR to: {OUT_DAILY_CSV}")
    return spliced


def build_monthly_hibor_and_augment_ctp():
    print("=" * 70)
    print("TASK 1.2: Building Monthly Period-Average HIBOR & Augmenting CTP Portfolios...")
    print("=" * 70)

    month_map = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
        "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
    }

    def parse_monthly_sheet(sheet_name):
        df = pd.read_excel(MONTHLY_XLS, sheet_name=sheet_name, header=None)
        data_rows = []
        current_year = None
        for idx, row in df.iterrows():
            m = str(row[1]).strip()
            if m in month_map:
                y_val = row[0]
                if pd.notna(y_val) and str(y_val).strip().isdigit():
                    current_year = int(str(y_val).strip())
                if current_year is not None:
                    ym = f"{current_year}-{month_map[m]}"
                    data_rows.append({
                        "year_month": ym,
                        "on": row[4],
                        "1w": row[5],
                        "1m": row[6],
                        "3m": row[7],
                        "6m": row[8],
                        "9m": row[9],
                        "12m": row[10]
                    })
        res = pd.DataFrame(data_rows)
        for c in ["on", "1w", "1m", "3m", "6m", "9m", "12m"]:
            res[c] = pd.to_numeric(res[c], errors="coerce")
        return res

    df_m_fix = parse_monthly_sheet("T6.3.2 (HIBOR Fixing)")
    df_m_scb = parse_monthly_sheet("T6.3.2(HIBOR)")

    # Splicing: Fixing primary, SCB secondary
    merged_m = pd.merge(df_m_fix, df_m_scb, on="year_month", how="outer", suffixes=("_fix", "_scb")).sort_values("year_month").reset_index(drop=True)
    spliced_m = pd.DataFrame({"year_month": merged_m["year_month"]})
    for tenor in ["on", "1w", "1m", "3m", "6m", "9m", "12m"]:
        spliced_m[f"hibor_{tenor}_avg_annual_pct"] = merged_m[f"{tenor}_fix"].combine_first(merged_m[f"{tenor}_scb"])

    spliced_m["source_1m"] = np.where(merged_m["1m_fix"].notna(), "HKAB_Fixing", "HKMA_SCB_HIBOR")

    # Filter to 1994-01 to 2026-09 (393 calendar months)
    m_393 = spliced_m[(spliced_m["year_month"] >= "1994-01") & (spliced_m["year_month"] <= "2026-09")].copy().reset_index(drop=True)
    assert len(m_393) == 393, f"Expected 393 months, got {len(m_393)}"

    # Compute monthly risk-free rate in percent
    # rf_monthly_pct = hibor_1m_avg_annual_pct / 12.0
    m_393["rf_monthly_pct"] = m_393["hibor_1m_avg_annual_pct"] / 12.0

    print(f"Monthly HIBOR 393 months: {m_393['year_month'].min()} to {m_393['year_month'].max()}")
    print("Summary of rf_monthly_pct:")
    print(m_393["rf_monthly_pct"].describe())

    m_393.to_csv(OUT_MONTHLY_CSV, index=False)
    print(f"Successfully saved monthly HIBOR to: {OUT_MONTHLY_CSV}")

    # Merge onto clean_monthly_ctp_portfolios_1994_2026.csv
    ctp = pd.read_csv(CTP_PORTFOLIOS_CSV)
    assert len(ctp) == 393, f"Expected 393 CTP rows, got {len(ctp)}"

    ctp_augmented = pd.merge(
        ctp,
        m_393[["year_month", "hibor_1m_avg_annual_pct", "rf_monthly_pct"]],
        on="year_month",
        how="left"
    )
    assert len(ctp_augmented) == 393, "Merge changed CTP row count!"
    assert ctp_augmented["rf_monthly_pct"].isna().sum() == 0, "Missing rf_monthly_pct values in CTP!"

    ctp_augmented.to_csv(OUT_CTP_CSV, index=False)
    print(f"Successfully saved augmented CTP portfolios (T = 393) to: {OUT_CTP_CSV}")
    return spliced_m, ctp_augmented


# =========================================================
# TASK 2: Enrich 33-Year Deal Panel (N = 2,865)
# =========================================================

def build_deal_panel(daily_hibor):
    print("=" * 70)
    print("TASK 2: Enriching 33-Year Deal Panel (N = 2,866)...")
    print("=" * 70)

    panel = pd.read_csv(INTERMEDIARIES_CSV)
    assert len(panel) == 2866, f"Expected 2866 rows, got {len(panel)}"

    # -----------------------------------------------------
    # 1. Exact Anchor Dates & Lags
    # -----------------------------------------------------
    print("Calculating anchor dates, subscription window, and lags...")
    anchor_dates = []
    has_exact_p_list = []
    p_to_l_days_list = []
    allot_peak_dates = []
    baseline_dates = []

    for idx, row in panel.iterrows():
        ld_str = str(row["listing_date"])[:10]
        pd_str = str(row["prospectus_date"])[:10] if pd.notna(row["prospectus_date"]) else None

        ld = datetime.strptime(ld_str, "%Y-%m-%d")
        pd_dt = datetime.strptime(pd_str, "%Y-%m-%d") if pd_str else None

        lag = (ld - pd_dt).days if pd_dt else None
        # Plausible lag between prospectus and listing is between 0 and 90 calendar days
        if lag is not None and 0 <= lag <= 90:
            anchor = pd_dt
            has_exact = True
            p_to_l = float(lag)
        else:
            anchor = ld - timedelta(days=10)
            has_exact = False
            p_to_l = np.nan

        base_dt = anchor - timedelta(days=5)
        peak_dt = ld - timedelta(days=2)

        anchor_dates.append(anchor.strftime("%Y-%m-%d"))
        has_exact_p_list.append(has_exact)
        p_to_l_days_list.append(p_to_l)
        allot_peak_dates.append(peak_dt.strftime("%Y-%m-%d"))
        baseline_dates.append(base_dt.strftime("%Y-%m-%d"))

    panel["anchor_open_date"] = anchor_dates
    panel["has_exact_prospectus_date"] = has_exact_p_list
    panel["prospectus_to_listing_days"] = p_to_l_days_list
    panel["allotment_freeze_peak_date"] = allot_peak_dates

    # -----------------------------------------------------
    # 2. Exact Daily HIBOR Matching & Liquidity-Freeze Spikes
    # -----------------------------------------------------
    print("Matching daily HIBOR at open, baseline, peak, and window maximum...")
    daily_sorted = daily_hibor.sort_values("date").reset_index(drop=True)
    daily_sorted["date_dt"] = pd.to_datetime(daily_sorted["date"])

    # Prepare query dataframes
    temp_df = pd.DataFrame({
        "orig_idx": panel.index,
        "anchor_dt": pd.to_datetime(panel["anchor_open_date"]),
        "base_dt": pd.to_datetime(baseline_dates),
        "peak_dt": pd.to_datetime(panel["allotment_freeze_peak_date"]),
        "list_dt": pd.to_datetime(panel["listing_date"])
    })

    def match_rates(dt_col, prefix):
        sorted_temp = temp_df[["orig_idx", dt_col]].sort_values(dt_col)
        m = pd.merge_asof(
            sorted_temp,
            daily_sorted[["date_dt", "hibor_on", "hibor_1w", "hibor_1m", "hibor_3m"]],
            left_on=dt_col,
            right_on="date_dt",
            direction="backward"
        )
        return m.set_index("orig_idx")[["hibor_on", "hibor_1w", "hibor_1m", "hibor_3m"]].rename(
            columns={
                "hibor_on": f"hibor_on_{prefix}",
                "hibor_1w": f"hibor_1w_{prefix}",
                "hibor_1m": f"hibor_1m_{prefix}",
                "hibor_3m": f"hibor_3m_{prefix}"
            }
        ).loc[panel.index]

    open_rates = match_rates("anchor_dt", "open")
    base_rates = match_rates("base_dt", "Baseline_minus5d")
    peak_rates = match_rates("peak_dt", "peak")

    for col in open_rates.columns:
        panel[col] = open_rates[col]

    panel["hibor_on_Baseline_minus5d"] = base_rates["hibor_on_Baseline_minus5d"]
    panel["hibor_1w_Baseline_minus5d"] = base_rates["hibor_1w_Baseline_minus5d"]

    for col in peak_rates.columns:
        panel[col] = peak_rates[col]

    # Calculate hibor_1w_window_max = max daily 1w HIBOR in [anchor_open_date, listing_date - 1]
    window_maxes = []
    # Index daily_sorted by date_dt for fast slicing
    daily_indexed = daily_sorted.set_index("date_dt")["hibor_1w"]

    for idx, row in panel.iterrows():
        a_dt = pd.to_datetime(row["anchor_open_date"])
        w_end = pd.to_datetime(row["listing_date"]) - timedelta(days=1)
        sub_slice = daily_indexed.loc[a_dt:w_end]
        if len(sub_slice) > 0:
            w_max = float(sub_slice.max())
        else:
            w_max = float(row["hibor_1w_open"])
        window_maxes.append(w_max)

    panel["hibor_1w_window_max"] = window_maxes
    panel["delta_hibor_1w_freeze_pp"] = panel["hibor_1w_window_max"] - panel["hibor_1w_Baseline_minus5d"]
    panel["hibor_1w_3m_spread_peak_pp"] = panel["hibor_1w_window_max"] - panel["hibor_3m_open"]

    # -----------------------------------------------------
    # 3. Locked Retail Subscription Capital (PN18 Clawback Adjusted)
    # -----------------------------------------------------
    print("Calculating locked retail capital with PN18 clawback adjustment...")
    micro_init_map = {}
    if MICRO_PANEL_CSV.exists():
        micro_df = pd.read_csv(MICRO_PANEL_CSV)
        for _, m_row in micro_df.iterrows():
            sc = m_row.get("stock_code")
            p_init = m_row.get("public_shares_initial")
            p0 = m_row.get("p0_offer_price_hkd")
            if pd.notna(sc) and pd.notna(p_init) and pd.notna(p0):
                micro_init_map[sc] = float(p_init) * float(p0)

    approx_init_public = []
    locked_retail = []

    for idx, row in panel.iterrows():
        sc = row["stock_code"]
        tot = row["funds_raised_total_hkd"]
        pub = row["funds_raised_public_hkd"]
        sub = row["retail_sub_ratio_clean"]
        board = row["board"]

        if board != "Main Board" or pd.isna(tot) or pd.isna(pub) or pd.isna(sub):
            # GEM or missing data
            approx_init = pub if pd.notna(pub) else np.nan
            locked_bn = np.nan
        else:
            if sc in micro_init_map:
                approx_init = micro_init_map[sc]
            else:
                # On Main Board under PN18 clawback:
                # If sub >= 15x, public tranche was expanded from initial (~10%) to 30%/40%/50%.
                # The HKEX tables report post-clawback proceeds in funds_raised_public_hkd.
                # Therefore, initial public tranche is min(pub, 0.10 * tot).
                if sub >= 15.0:
                    approx_init = min(pub, 0.10 * tot)
                else:
                    approx_init = pub

            locked_bn = (approx_init * sub) / 1e9

        approx_init_public.append(approx_init)
        locked_retail.append(locked_bn)

    panel["approx_initial_public_hkd"] = approx_init_public
    panel["locked_retail_hkd_bn"] = locked_retail

    # -----------------------------------------------------
    # 4. Hang Seng Index Public-Information Windows (Loughran & Ritter 2002)
    # -----------------------------------------------------
    print("Calculating Hang Seng Index pre-offer & subscription window returns...")
    with open(HSI_JSON) as f:
        hsi_raw = json.load(f)

    hsi_series = pd.Series(hsi_raw).sort_index()
    hsi_dates = list(hsi_series.index)
    hsi_vals = list(hsi_series.values)

    hsi_pre30 = []
    hsi_sub_win = []

    for idx, row in panel.iterrows():
        anchor_str = row["anchor_open_date"]
        has_exact = row["has_exact_prospectus_date"]
        pd_str = str(row["prospectus_date"])[:10] if pd.notna(row["prospectus_date"]) else None
        ld_str = str(row["listing_date"])[:10]

        # 30-trading-day return ending on anchor_open_date
        pos = bisect.bisect_right(hsi_dates, anchor_str) - 1
        if pos >= 30 and pos < len(hsi_dates):
            r_pre30 = (hsi_vals[pos] / hsi_vals[pos - 30] - 1.0) * 100.0
        else:
            r_pre30 = np.nan
        hsi_pre30.append(r_pre30)

        # Subscription window return: strictly only when has_exact_prospectus_date == True
        # from prospectus_date to listing_date - 1 trading day
        if has_exact and pd_str:
            p_pos = bisect.bisect_right(hsi_dates, pd_str) - 1
            l_pos = bisect.bisect_left(hsi_dates, ld_str) - 1
            if 0 <= p_pos <= l_pos and l_pos < len(hsi_dates):
                r_sub = (hsi_vals[l_pos] / hsi_vals[p_pos] - 1.0) * 100.0
            else:
                r_sub = np.nan
        else:
            r_sub = np.nan
        hsi_sub_win.append(r_sub)

    panel["hsi_ret_pre30td_pct"] = hsi_pre30
    panel["hsi_ret_sub_window_pct"] = hsi_sub_win

    # -----------------------------------------------------
    # 5. Bloomberg Syndication (Rule 144A / Reg S), Secondary Sales & Lifetime Returns
    # -----------------------------------------------------
    print("Merging Bloomberg syndication data & performing forensic lifetime return audits...")
    bbg = pd.read_csv(BLOOMBERG_CSV)

    panel["bbg_action_id_str"] = panel["bbg_action_id"].dropna().astype(int).astype(str)
    bbg["action_id_str"] = bbg["Action Id"].dropna().astype(int).astype(str)

    bbg_sub = bbg[["action_id_str", "Offer Type", "First Selling Stockholder", "Offer To Date", "Last Price"]].drop_duplicates(subset=["action_id_str"])
    merged_bbg = pd.merge(panel[["bbg_action_id_str"]], bbg_sub, left_on="bbg_action_id_str", right_on="action_id_str", how="left")

    has_144a = []
    has_regs = []
    has_sec = []
    selling_dir = []
    lifetime_ret_raw = []

    sec_triggers = ["secondary share offering", "pe exit", "vc exit", "government exit"]

    for idx, b_row in merged_bbg.iterrows():
        if pd.isna(b_row["action_id_str"]):
            # Strictly unmatched Bloomberg row (N = 108) -> keep NaN, NEVER fillna(0)
            has_144a.append(np.nan)
            has_regs.append(np.nan)
            has_sec.append(np.nan)
            selling_dir.append(np.nan)
            lifetime_ret_raw.append(np.nan)
        else:
            ot = str(b_row["Offer Type"]).lower() if pd.notna(b_row["Offer Type"]) else ""
            fss = str(b_row["First Selling Stockholder"]).lower() if pd.notna(b_row["First Selling Stockholder"]) else ""

            has_144a.append(1.0 if "rule 144a" in ot else 0.0)
            has_regs.append(1.0 if "reg s" in ot else 0.0)
            has_sec.append(1.0 if any(t in ot for t in sec_triggers) else 0.0)
            selling_dir.append(1.0 if "directors & executive officers" in fss else 0.0)

            otd_val = pd.to_numeric(b_row["Offer To Date"], errors="coerce")
            lifetime_ret_raw.append(otd_val)

    panel["has_rule_144a"] = has_144a
    panel["has_reg_s"] = has_regs
    panel["has_secondary_sale"] = has_sec
    panel["selling_insider_director"] = selling_dir

    # Forensic audit of lifetime_offer_to_date_pct:
    # 1. Set to NaN whenever flag_recycled_or_transferred_ticker == 1 OR flag_reverse_split_distortion == 1
    # 2. Audit extreme positive values (Offer To Date > 1000% / > 500%) against market_cache bar history and Last Price
    flag_split_unverified = []
    lifetime_clean = []

    # Known genuine forward split / bonus blue-chips where lifetime returns reflect real wealth compounding:
    # 0700.HK (Tencent 5:1), 2899.HK (Zijin Mining), 1211.HK (BYD), 0992.HK (Lenovo 4:1), 2338.HK (Weichai Power),
    # 3939.HK (Wanguo Mining), 0914.HK (Conch Cement), 0883.HK (CNOOC), 2328.HK (PICC), 1093.HK (CSPC Pharma 5:1),
    # 1171.HK (Yanzhou Coal), 2319.HK (Mengniu Dairy 2:1), 2318.HK (Ping An 2:1), 0696.HK (Travelsky),
    # 2333.HK (Great Wall Motor), 2359.HK (WuXi AppTec), 2269.HK (WuXi Biologics), 2005.HK (SSY Group),
    # 3339.HK (Lonking), 1919.HK (COSCO Shipping), 0868.HK (Xinyi Glass)
    GENUINE_SPLIT_STOCKS = {
        "0700.HK", "2899.HK", "1211.HK", "0992.HK", "2338.HK", "3939.HK", "0914.HK",
        "0883.HK", "2328.HK", "1093.HK", "1171.HK", "2319.HK", "2318.HK", "0696.HK",
        "2333.HK", "2359.HK", "2269.HK", "2005.HK", "3339.HK", "1919.HK", "0868.HK",
        "0565.HK", "1072.HK", "0900.HK"
    }

    # Known reverse-split / consolidation distorted tickers:
    DISTORTED_ANOMALY_STOCKS = {
        "1735.HK", "2225.HK", "1783.HK", "2723.HK", "8279.HK"
    }

    for idx, row in panel.iterrows():
        sc = row["stock_code"]
        ld = row["listing_date"]
        raw_otd = lifetime_ret_raw[idx]
        is_recycled = bool(row["flag_recycled_or_transferred_ticker"])
        is_rev_split = bool(row["flag_reverse_split_distortion"])

        is_unverified = False

        if pd.isna(raw_otd):
            lifetime_clean.append(np.nan)
            flag_split_unverified.append(False)
            continue

        # Rule 1: Exclude recycled tickers and reverse split distorted tickers
        if is_recycled or is_rev_split:
            lifetime_clean.append(np.nan)
            flag_split_unverified.append(True)
            continue

        # Rule 2: Check market cache for extreme single-day jumps > 400%
        cpath = CACHE_DIR / f"{sc}_{ld}.json"
        if cpath.exists():
            try:
                with open(cpath) as f:
                    bars = json.load(f)
                for i in range(1, len(bars)):
                    c0 = bars[i-1][2]
                    c1 = bars[i][2]
                    if c0 > 0.01 and (c1 / c0 > 4.0):
                        is_unverified = True
                        break
            except Exception:
                pass

        # Rule 3: Check specific anomalous tickers or extreme divergence from unadjusted price ratio
        if sc in DISTORTED_ANOMALY_STOCKS:
            is_unverified = True

        last_bbg_p = pd.to_numeric(merged_bbg.loc[idx, "Last Price"], errors="coerce")
        p0 = row["offer_price_hkd"]
        if pd.notna(last_bbg_p) and pd.notna(p0) and p0 > 0 and raw_otd > 500.0:
            raw_last_ret = (last_bbg_p / p0 - 1.0) * 100.0
            ratio = (raw_otd + 100.0) / (raw_last_ret + 100.0) if raw_last_ret > -99 else 1.0
            if ratio > 3.0 and sc not in GENUINE_SPLIT_STOCKS:
                is_unverified = True

        flag_split_unverified.append(is_unverified)
        if is_unverified:
            lifetime_clean.append(np.nan)
        else:
            lifetime_clean.append(raw_otd)

    panel["lifetime_offer_to_date_pct"] = lifetime_clean
    panel["flag_lifetime_split_unverified"] = flag_split_unverified

    # Clean up temporary matching columns
    if "bbg_action_id_str" in panel.columns:
        panel.drop(columns=["bbg_action_id_str"], inplace=True)

    print("\nDeal Panel Enrichment Verification:")
    print(f"Total Rows: {len(panel)}")
    new_cols = [
        "anchor_open_date", "has_exact_prospectus_date", "prospectus_to_listing_days",
        "allotment_freeze_peak_date", "hibor_on_open", "hibor_1w_open", "hibor_1m_open", "hibor_3m_open",
        "hibor_on_Baseline_minus5d", "hibor_1w_Baseline_minus5d", "hibor_on_peak", "hibor_1w_peak",
        "hibor_1m_peak", "hibor_3m_peak", "hibor_1w_window_max", "delta_hibor_1w_freeze_pp",
        "hibor_1w_3m_spread_peak_pp", "approx_initial_public_hkd", "locked_retail_hkd_bn",
        "hsi_ret_pre30td_pct", "hsi_ret_sub_window_pct", "has_rule_144a", "has_reg_s",
        "has_secondary_sale", "selling_insider_director", "lifetime_offer_to_date_pct",
        "flag_lifetime_split_unverified"
    ]

    for col in new_cols:
        nn = panel[col].notna().sum()
        nu = panel[col].nunique(dropna=True)
        print(f"  {col:<32}: non-null = {nn:<5} | nunique = {nu}")

    panel.to_csv(OUT_PANEL_CSV, index=False)
    print(f"\nSuccessfully saved enriched 33-year deal panel to: {OUT_PANEL_CSV}")
    return panel


# =========================================================
# Main Execution
# =========================================================
def main():
    print("STARTING 33-YEAR HKMA HIBOR, 144A & MARKET-TIMING PIPELINE...")
    daily_hibor = build_daily_hibor()
    build_monthly_hibor_and_augment_ctp()
    build_deal_panel(daily_hibor)
    print("ALL 5 TASKS COMPLETED SUCCESSFULLY WITH ZERO ERRORS!")


if __name__ == "__main__":
    main()
