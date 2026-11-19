#!/usr/bin/env python3
"""Reconcile Haiku + allotment parser cornerstone allocations for the 725 confirmed historical (1994-2024)
cornerstone IPOs, archive the pre-repair master panel, and write repaired ext_cornerstone_pct /
ext_cornerstone_shares back to the 33Y master panel."""
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PANEL_PATH = ROOT / "analysis/out/overview_1994_2026/hkipo_33y_master_panel_1994_2026_tier1_complete.csv"
BACKUP_DIR = ROOT / "analysis/out/overview_1994_2026/archive_pre_cornerstone_pct_repair"
OUT_DIR = ROOT / "analysis/out/subscription_cornerstone_repair"
PARSED_CSV = OUT_DIR / "parsed_cornerstone_pct.csv"
CACHE_JSONL = OUT_DIR / "haiku_cornerstone_cache.jsonl"
RECONCILED_CSV = OUT_DIR / "cornerstone_pct_reconciled.csv"

# Verified manual/forensic resolutions from original allotment/prospectus pages where
# table headers, FINI boilerplate, international-tranche %, or Offer Size Adjustment Options differed.
VERIFIED_OVERRIDES: dict[str, tuple[float | None, float | None, str, str]] = {
    # (cs_pct_reconciled, cs_shares_reconciled, source_tag, note)
    "2009_0906.HK": (16.50, 33000000.0, "verified_manual_table", "33M / 200M base offer = 16.50% (Haiku read 4.13% issued share cap column)"),
    "2012_1314.HK": (20.50, 68344000.0, "verified_manual_table", "Two cornerstone investors x 34,172,000 = 68.344M / 333.334M base offer = 20.50% (10.25% each)"),
    "2012_1829.HK": (32.95, 236586000.0, "verified_manual_shares", "236,586,000 / 718,000,000 Global Offer = 32.95% (54.9% in announcement was % of International tranche)"),
    "2013_1963.HK": (17.10, 123591000.0, "verified_manual_shares", "123,591,000 / 722,947,000 Global Offer = 17.10% (19.41% was % of International tranche)"),
    "2015_8361.HK": (26.76, 66902000.0, "verified_manual_shares", "66,902,000 / 250,000,000 Global Offer = 26.76% (23.3% was post-greenshoe / subset)"),
    "2017_8469.HK": (24.00, 44400000.0, "verified_manual_shares", "44,400,000 / 185,000,000 Global Offer = 24.00% (26.66% was % of International Placing)"),
    "2017_8142.HK": (10.64, 26590000.0, "verified_haiku_shares", "26,590,000 / 250,000,000 Global Offer = 10.64%"),
    "2017_8199.HK": (39.60, 99000000.0, "verified_haiku_shares", "99,000,000 / 250,000,000 Global Offer = 39.60%"),
    "2019_1876.HK": (23.00, 290344400.0, "verified_manual_shares", "290,344,400 / 1,262,350,000 initial Global Offer = 23.00% (20.0% was after +15% OSAO)"),
    "2021_6626.HK": (10.76, 159126000.0, "verified_manual_explicit", "Explicitly stated 10.76% of initial Global Offer Shares (panel R+S excluded preferential tranche)"),
    "2023_9690.HK": (68.99, 28021300.0, "verified_manual_shares", "28,021,300 / 40,617,100 initial Global Offer = 68.99% (66.0% after partial OSAO)"),
    "2024_1318.HK": (33.30, 23504400.0, "verified_manual_shares", "23,504,400 / 70,588,200 initial Global Offer = 33.30% (29.98% after OSAO)"),
    "2024_2598.HK": (55.52, 35693000.0, "verified_manual_pdf", "Allotment PDF p5 Cornerstone table Total = 35,693,000 (55.52% of Offer Shares)"),
    "2024_9639.HK": (19.18, 47935000.0, "verified_manual_pdf", "Allotment announcement Cornerstone table Total = 47,935,000 (19.18% of Offer Shares)"),
    # Deals where panel base_shares had missing zeros / double count / greenshoe inflation -> explicit Global Offer % governs
    "2007_0285.HK": (2.64, 14508500.0, "verified_haiku_explicit", "14.5085M / 550M actual base offer = 2.64% (panel R+S misparsed)"),
    "2007_0390.HK": (16.54, 550172000.0, "verified_haiku_explicit", "550.172M / 3,326M stated base offer = 16.54% (panel R+S included +15% greenshoe)"),
    "2007_1813.HK": (27.92, 174506674.0, "verified_haiku_explicit", "174.507M / 625M initial base offer = 27.92% (panel R+S 718.75M included +15% greenshoe)"),
    "2007_2007.HK": (27.10, None, "verified_haiku_explicit", "Announcement Summary p4 explicitly states 27.1% of Offer Shares"),
    "2007_3868.HK": (32.00, 96000000.0, "verified_haiku_explicit", "96M / 300M stated Offer Shares = 32.0%"),
    "2007_3883.HK": (19.20, None, "verified_haiku_explicit", "Announcement Summary p4 explicitly states 19.2% of Offer Shares"),
    "2010_0486.HK": (34.61, 635106000.0, "verified_haiku_explicit", "635.106M / 1,835.293M stated Offer Shares = 34.61%"),
    "2011_0579.HK": (63.34, 653808000.0, "verified_haiku_explicit", "653.808M / 1,032.2M stated base Offer Shares = 63.34% (panel R+S 1,135.42M was post-greenshoe)"),
    "2011_1296.HK": (69.24, 756450000.0, "verified_haiku_explicit", "Announcement explicitly states 69.24% of Offer Shares (panel col_R inflated)"),
    "2013_1680.HK": (12.40, 115593000.0, "verified_haiku_explicit", "Announcement explicitly states 12.4% of Offer Shares (panel col_R inflated)"),
    "2013_6818.HK": (58.16, 3397848000.0, "verified_haiku_explicit", "Announcement table explicitly states 58.16% of Offer Shares (panel R+S inflated)"),
    "2013_6881.HK": (48.04, 527195000.0, "verified_haiku_explicit", "527.195M / 1,097.365M stated base Offer Shares = 48.04% (panel R+S 1,606.6M inflated)"),
    "2014_1816.HK": (42.10, 3713105000.0, "verified_haiku_explicit", "Announcement explicitly states 42.1% of Offer Shares (panel R+S 10.149B included +15% greenshoe)"),
    "2015_1430.HK": (37.28, 74568000.0, "verified_haiku_explicit", "74.568M / 200M base offer = 37.28% (panel col_R=18 typo)"),
    "2016_2016.HK": (57.69, 1903823000.0, "verified_haiku_explicit", "Announcement table explicitly states 57.69% of Offer Shares (before greenshoe)"),
    "2018_1760.HK": (18.20, 45554000.0, "verified_haiku_explicit", "Announcement explicitly states 18.2% of Offer Shares (panel R+S included +15% greenshoe)"),
    "2018_1916.HK": (51.60, 603586000.0, "verified_haiku_explicit", "Announcement explicitly states 51.6% of Offer Shares (panel R+S included +15% greenshoe)"),
    "2018_1996.HK": (47.40, 378964000.0, "verified_haiku_explicit", "Announcement explicitly states 47.4% of Offer Shares (panel R+S included +15% greenshoe)"),
    "2019_2500.HK": (39.26, 30829500.0, "verified_haiku_explicit", "Announcement explicitly states 39.26% of Offer Shares (panel R+S included +15% greenshoe)"),
    "2020_9668.HK": (29.15, 839592500.0, "verified_haiku_explicit", "Announcement explicitly states 29.15% of Offer Shares (panel R+S included +15% greenshoe)"),
    "2021_6606.HK": (47.08, 36062500.0, "verified_haiku_explicit", "36.0625M / 76.598M base offer = 47.08% (panel col_R=6 typo)"),
    # Genuinely unquantifiable / FINI Note-2-only non-cornerstone listings (keep NaN in pct)
    "2020_9993.HK": (None, None, "unverified_no_disclosure", "PHIP redacted and final allotment has 0 cornerstone mentions"),
    "2023_2483.HK": (None, None, "unverified_fini_boilerplate", "Only FINI lock-up Note 2 boilerplate; no cornerstone investor table"),
    "2024_6086.HK": (None, None, "unverified_fini_boilerplate", "Only FINI lock-up Note 2 boilerplate; no cornerstone investor table"),
}


def reconcile_row(p: pd.Series, h: dict | None, panel_row: pd.Series) -> dict:
    key = p["key"]
    p_base = float(p["base_shares"]) if pd.notna(p["base_shares"]) else np.nan
    old_pct = float(p["old_pct"]) if pd.notna(p["old_pct"]) else np.nan

    pct_out: float | None = None
    sh_out: float | None = None
    denom_out: float | None = p_base if pd.notna(p_base) else None
    src = ""
    note = ""

    if key in VERIFIED_OVERRIDES:
        pct_out, sh_out, src, note = VERIFIED_OVERRIDES[key]
        if sh_out and pct_out and not denom_out:
            denom_out = round(sh_out / (pct_out / 100.0))
    elif h is not None and h.get("status") == "ok":
        h_sh = h.get("cs_shares")
        h_exp = h.get("explicit_offer_pct")
        h_base = h.get("stated_base_offer_shares")
        note = str(h.get("note") or "")
        if h_sh is not None and h_sh > 0:
            sh_out = float(h_sh)
            if h_base and h_base > 0 and h_exp is not None and abs((sh_out / h_base * 100.0) - h_exp) <= 1.0:
                pct_out = sh_out / float(h_base) * 100.0
                denom_out = float(h_base)
                src = "haiku_shares_stated_base"
            elif pd.notna(p_base) and p_base > 0:
                calc = sh_out / p_base * 100.0
                if 0 < calc <= 100.0:
                    pct_out = calc
                    src = "haiku_shares_panel_base"
                elif h_exp is not None and 0 < h_exp <= 100.0:
                    pct_out = float(h_exp)
                    src = "haiku_explicit_pct_fallback"
        elif h_exp is not None and 0 < float(h_exp) <= 100.0:
            pct_out = float(h_exp)
            src = "haiku_explicit_pct_only"
    else:
        # High-confidence parser paths (100% spot-check agreement): parsed_verified or prose_total
        st = p["status"]
        p_sh = float(p["cs_shares"]) if pd.notna(p["cs_shares"]) else None
        p_calc = float(p["calc_pct_base"]) if pd.notna(p["calc_pct_base"]) else None
        p_exp = float(p["explicit_offer_pct"]) if pd.notna(p["explicit_offer_pct"]) else None
        if p_calc is not None and 0 < p_calc <= 100.0:
            pct_out = p_calc
            sh_out = p_sh
            src = f"parser_{st}_{p['how']}"
        elif p_exp is not None and 0 < p_exp <= 100.0:
            pct_out = p_exp
            src = f"parser_{st}_explicit"

    if pct_out is not None:
        pct_out = round(float(pct_out), 2)
        if not (0 < pct_out <= 100.0):
            pct_out = None
            src = f"{src}_rejected_range"

    return {
        "key": key,
        "batch": p["batch"],
        "cohort_year": int(p["cohort_year"]),
        "old_cornerstone_pct": old_pct,
        "new_cornerstone_pct": pct_out,
        "cs_shares": sh_out,
        "base_offer_shares": denom_out,
        "source": src or "unresolved",
        "diff_vs_old_pp": round(pct_out - old_pct, 2) if (pct_out is not None and pd.notna(old_pct)) else np.nan,
        "note": note[:200],
    }


def main():
    parsed = pd.read_csv(PARSED_CSV)
    cache = {}
    if CACHE_JSONL.exists():
        for ln in CACHE_JSONL.open():
            if ln.strip():
                d = json.loads(ln)
                cache[d["key"]] = d

    panel = pd.read_csv(PANEL_PATH, low_memory=False)
    panel["key"] = panel["file"].str.replace(".json", "", regex=False)
    panel_idx = panel.set_index("key")

    recs = [reconcile_row(r, cache.get(r["key"]), panel_idx.loc[r["key"]]) for _, r in parsed.iterrows()]
    rec_df = pd.DataFrame(recs)
    rec_df.to_csv(RECONCILED_CSV, index=False)

    print("=== Cornerstone % Reconciliation Summary (N = 725 confirmed historical CS IPOs) ===")
    print("Non-null new_cornerstone_pct:", rec_df["new_cornerstone_pct"].notna().sum(), "/", len(rec_df))
    print("Non-null old_cornerstone_pct:", rec_df["old_cornerstone_pct"].notna().sum(), "/", len(rec_df))
    print("\nBy source:")
    print(rec_df["source"].value_counts(dropna=False).to_string())
    print("\nBy batch (coverage):")
    cov = rec_df.groupby("batch").agg(
        total=("key", "count"),
        old_n=("old_cornerstone_pct", lambda s: s.notna().sum()),
        old_med=("old_cornerstone_pct", "median"),
        new_n=("new_cornerstone_pct", lambda s: s.notna().sum()),
        new_med=("new_cornerstone_pct", "median"),
    )
    print(cov.round(2).to_string())

    comp = rec_df[rec_df["old_cornerstone_pct"].notna() & rec_df["new_cornerstone_pct"].notna()]
    print(f"\nComparable old vs new: {len(comp)} | |diff| <= 1.5pp: {(comp['diff_vs_old_pp'].abs() <= 1.5).sum()} | |diff| > 1.5pp: {(comp['diff_vs_old_pp'].abs() > 1.5).sum()}")

    # Backup pre-repair master panel once (or timestamped)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"hkipo_33y_master_panel_1994_2026_tier1_complete_pre_cs_pct_{ts}.csv"
    shutil.copy2(PANEL_PATH, backup_file)
    print(f"\nBacked up pre-repair panel -> {backup_file}")

    # Apply back to master panel (leave 2025-2026 and non-CS rows untouched)
    pct_map = rec_df.set_index("key")["new_cornerstone_pct"].to_dict()
    mask_hist_cs1 = (panel["batch"] != "2025-2026") & (panel["ext_has_cornerstone"] == 1)
    assert int(mask_hist_cs1.sum()) == len(rec_df), f"Expected {len(rec_df)} rows, got {mask_hist_cs1.sum()}"
    new_vals = panel.loc[mask_hist_cs1, "key"].map(pct_map).astype(float)
    panel.loc[mask_hist_cs1, "ext_cornerstone_pct"] = new_vals
    panel.loc[mask_hist_cs1, "ext_cornerstone_shares"] = new_vals
    panel.drop(columns=["key"]).to_csv(PANEL_PATH, index=False)
    print(f"Updated ext_cornerstone_pct & ext_cornerstone_shares on {mask_hist_cs1.sum()} historical CS=1 rows in {PANEL_PATH}")


if __name__ == "__main__":
    main()
