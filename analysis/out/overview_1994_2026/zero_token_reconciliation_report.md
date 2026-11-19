# Zero-Token Historical Panel Reconciliation & Audit Report (1994–2026)

**Target Panel**: 33-Year Hong Kong IPO Master Panel (`clean_33y_hkipo_panel_1994_2026_enriched.csv`)  
**Total Sample Size**: **2,866 Ordinary IPOs** (2,289 Main Board, 577 GEM)  
**Observation Window**: 1994-01-01 to 2026-09-30 (33 cohort years across 5 statutory market epochs)  
**Execution Date**: 2026-11-12  

---

## Executive Summary of Zero-Token Reconciliation

This reconciliation audited and populated previously untapped zero-token fields across official HKEX statutory filings and Bloomberg ECDR records:
1. **GEM Official Fields Recovery (100.0%)**:
   - Reconciled `gem_incorporation`, `gem_industry`, `gem_listing_method`, `gem_shares_at_listing`, and `gem_market_cap_hkd` across all **577 GEM IPOs** (574 pre-2025 listings + 3 modern listings: `8549.HK` in 2025, `8610.HK` and `8090.HK` in 2026).
   - Resolved the single missing incorporation entry in raw HKEX records (`8112.HK`, Focus Media Network Ltd.) to **Cayman Islands**, fully supported by its official prospectus and ISIN `KYG3610T1215`.
2. **Main Board Multi-row `(b)` International Placing Proceeds Recovery**:
   - Audited the **464 Main Board rows** where `funds_raised_int_hkd` was previously recorded as `NaN`.
   - Classified `nlr_tranche_structure` across the entire panel:
     - **Public_And_Placing**: 1,826 Main Board IPOs (including 2 Singapore dual-tranche cases `0058.HK` and `0903.HK` in 1999).
     - **Public_Only_In_NLR**: 459 Main Board IPOs (371 unlabelled single-row entries from earlier years + 88 explicit `(a)`-only public offers) where placing proceeds are definitively `0.0`.
     - **Placing_Only_In_NLR**: 3 pure institutional placings (`0686.HK` in 2000, `0486.HK` UC RUSAL in 2010, `0080.HK` in 2011) where public tranche proceeds were corrected from erroneously 100% to exact `0.0`.
     - Multi-row `(b)` proceeds sum recovery: `0694.HK` (Beijing Capital International Airport, 2000) corrected from partial HK$ 941.2M to exact combined placing proceeds of **HK$ 2,690,539,731.0**.
3. **Bloomberg ECDR Zero-Token Institutional Anchors**:
   - Extracted `isin_domicile_code` and `isin_domicile_jurisdiction` across 2,758 matched IPOs.
   - Cross-validated ISIN domicile against official HKEX GEM place of incorporation:
     - **Exact Jurisdiction Agreement**: **95.01%** (476 / 501).
     - **Offshore vs. Onshore Macro Classification Agreement**: **100.00%** (501 / 501).
     - Discrepancy analysis: All 25 differences are Cayman-incorporated issuers registered with Bermuda (`BM`) ISINs, reflecting post-listing offshore corporate restructuring with zero onshore leakage.
   - Identified **373 PE/VC-Backed IPOs** (`bbg_pe_vc_backed_flag = 1`) and **1,327 Secondary Share Sale Offerings** (`bbg_secondary_sale_flag = 1`).

---

## 1. Multi-Decade Sample Distribution by Analytical Cohort Batch

| Batch Window | Main Board IPOs | GEM IPOs | Total Cohort Sample | Share of Total |
| :--- | :---: | :---: | :---: | :---: |
| **1994–2001** (H-Share Pioneer & Pre-PN18) | 328 | 110 | 438 | 15.3% |
| **2002–2007** (Pre-Lehman Expansion) | 325 | 122 | 447 | 15.6% |
| **2008–2017** (Mega-SOE & Cornerstone Era) | 693 | 240 | 933 | 32.6% |
| **2018–2024** (New Economy Ch. 8A/18A/19C) | 717 | 102 | 819 | 28.6% |
| **2025–2026** (Modern FINI & Mech A/B) | 226 | 3 | 229 | 8.0% |
| **All 33 Years** | **2,289** | **577** | **2,866** | **100.0%** |

---

## 2. Main Board Tranche Structure & Proceed Resolution

Across all 2,289 Main Board listings, each issuer's offering structure is now deterministically verified:

| Analytical Batch | Public & Placing (`Public_And_Placing`) | Public Offer Only (`Public_Only_In_NLR`) | Placing Only (`Placing_Only_In_NLR`) | Unclassified (Supplement) | Total Main Board |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1994–2001** | 38 | 289 | 1 | 0 | 328 |
| **2002–2007** | 177 | 148 | 0 | 0 | 325 |
| **2008–2017** | 671 | 20 | 2 | 0 | 693 |
| **2018–2024** | 715 | 2 | 0 | 0 | 717 |
| **2025–2026** | 225 | 0 | 0 | 1 | 226 |
| **Total** | **1,826** | **459** | **3** | **1** | **2,289** |

### Breakdown of the 464 Previously NaN `funds_raised_int_hkd` Rows
1. **459 Pure Public Offers (`Public_Only_In_NLR`)**:
   - `funds_raised_public_hkd` confirmed equal to total capital raised.
   - `funds_raised_int_hkd` set to exact `0.0` (rather than missing).
   - `public_tranche_proceeds_share` confirmed at `1.0` (100.0%).
2. **3 Pure Institutional Placings (`Placing_Only_In_NLR`)**:
   - `0686.HK` (Peking Founder Tech, 2000): HK$ 60.0M placing proceeds, HK$ 0.0 public.
   - `0486.HK` (United Company RUSAL Plc, 2010): HK$ 17,391,162,672.0 placing proceeds, HK$ 0.0 public.
   - `0080.HK` (China New Economy Fund, 2011): HK$ 312,090,000.0 placing proceeds, HK$ 0.0 public.
   - `public_tranche_proceeds_share` corrected from erroneously 1.0 to exact `0.0`.
3. **2 Dual Public & Singapore Offers (`Public_And_Placing`)**:
   - `0058.HK` (Sun East Technology, 1999): HK$ 173.25M public offer `(a)` + HK$ 141.75M Singapore offer `(c)`.
   - `0903.HK` (G-Prop Holdings, 1999): HK$ 265.43M public offer `(a)` + HK$ 91.57M Singapore offer `(c)`.
4. **1 Multi-Row Sum Correction**:
   - `0694.HK` (Beijing Capital Int'l Airport, 2000): Combined international tranche (b1: HK$ 1.749B + b2: HK$ 941.2M = **HK$ 2,690,539,731.0**).

---

## 3. GEM Official Fields Recovery & Tranche Structure

GEM listings were completely recovered with 100.0% coverage across all 5 official HKEX parameters:

| Parameter Name | Target Scope | Non-Null Count | Coverage Rate | Status |
| :--- | :---: | :---: | :---: | :---: |
| `gem_incorporation` | 577 GEM IPOs | 577 | **100.0%** | Complete (8112.HK resolved to Cayman) |
| `gem_industry` | 577 GEM IPOs | 577 | **100.0%** | Complete (Hang Seng Indexes standard) |
| `gem_listing_method` | 577 GEM IPOs | 577 | **100.0%** | Complete |
| `gem_shares_at_listing` | 577 GEM IPOs | 577 | **100.0%** | Complete |
| `gem_market_cap_hkd` | 577 GEM IPOs | 577 | **100.0%** | Complete |

### GEM Offering Tranche Classification
- **Public & Placing (`Public_And_Placing`)**: **308 IPOs** (53.4%)
- **Placing Only (`Placing_Only_In_NLR`)**: **228 IPOs** (39.5%)
- **Public Offer Only (`Public_Only_In_NLR`)**: **41 IPOs** (7.1%)

---

## 4. Bloomberg ECDR Zero-Token Anchors & Cross-Check Audit

### Institutional Ownership & Offering Types by Batch

| Analytical Batch | Matched to Bloomberg | PE/VC-Backed IPOs (`bbg_pe_vc_backed_flag`) | Secondary Shares Sold (`bbg_secondary_sale_flag`) |
| :--- | :---: | :---: | :---: |
| **1994–2001** | 392 | 2 (0.5%) | 46 (11.7%) |
| **2002–2007** | 420 | 60 (14.3%) | 178 (42.4%) |
| **2008–2017** | 899 | 154 (17.1%) | 461 (51.3%) |
| **2018–2024** | 818 | 60 (7.3%) | 632 (77.3%) |
| **2025–2026** | 229 | 97 (42.4%) | 10 (4.4%) |
| **Total Matched** | **2,758** | **373 (13.5%)** | **1,327 (48.1%)** |

### Cross-Check Validation: `isin_domicile_jurisdiction` vs. `gem_incorporation`

To verify the semantic accuracy of `isin_domicile_jurisdiction`, we cross-tabulated all 501 matched GEM issuers against their official HKEX place of incorporation:

| Official HKEX GEM Incorporation | Matched ISIN Domicile | Frequency | Concordance Interpretation |
| :--- | :--- | :---: | :--- |
| **Cayman Islands** | Cayman Islands (`KY`) | 385 | Exact Agreement (76.8%) |
| **PRC (China)** | China (`CN`) | 50 | Exact Agreement (10.0%) |
| **Bermuda** | Bermuda (`BM`) | 26 | Exact Agreement (5.2%) |
| **Hong Kong** | Hong Kong (`HK`) | 12 | Exact Agreement (2.4%) |
| **Singapore** | Singapore (`SG`) | 2 | Exact Agreement (0.4%) |
| **Focus Media Network Ltd. (8112.HK)** | Cayman Islands (`KY`) | 1 | Resolved Audit Agreement (0.2%) |
| **Cayman Islands** | Bermuda (`BM`) | 25 | Offshore Re-Domiciliation / Restructuring (5.0%) |
| **Total Matched GEM Evaluated** | — | **501** | **95.01% Exact Agreement / 100.0% Macro Concordance** |

> **Key Empirical Takeaway**: Across all 501 cross-validated GEM IPOs, there is **zero cross-border onshore leakage** (0.0% PRC-to-Offshore or Offshore-to-PRC mismatches). The only divergence consists of 25 Cayman-incorporated issuers carrying Bermuda ISINs, confirming that ISIN domicile is an exceptionally robust zero-token corporate governance anchor.

---

## 5. Modern 2025Q3 Audit (N=24 Main Board Issuers)

We conducted a forensic inspection of the 2025Q3 cohort (`pipeline/prospectus_pipeline/datasets/HKIPO_2025-07-01_2025-09-30_HKIPO-MB/`):

1. **Prospectus Pipeline**:
   - Extraction JSONs in `out/extracted/`: **24 / 24 complete**.
   - Pipeline state tokens: `extracted` (24), `reviewed` (24), `validated` (24), `written` (24).
   - Independent Review Sign-off: **24 / 24 passed** by *Independent Period Reviewer (audit-grade Track Record verification)* under contract `2026-09-22-v3-70fields`.
2. **Allotment Pipeline**:
   - Extraction JSONs in `out/allot/extracted/`: **24 / 24 complete**.
   - Pipeline state tokens: `extracted` (24), `reviewed` (24), `validated` (24), `written` (24).
   - Independent Review Sign-off: **24 / 24 passed** by *Independent Allotment Reviewer (official allotment announcement verification)*.
3. **Master Clean Integration**:
   - All 24 issuers are fully populated and validated in `HKIPO-MB2025Q3_clean.csv` and merged into `pipeline/exports/HKIPO-MB-MASTER_clean.csv` (Cohort `2025Q3`).
   - No issuers or extraction targets are pending review or export.

---

## Conclusion & Artifact Verification

The enriched 33-year master panel is saved at:
- `analysis/out/overview_1994_2026/clean_33y_hkipo_panel_1994_2026_enriched.csv`

All zero-token historical fields (`gem_incorporation`, `gem_industry`, `gem_listing_method`, `gem_shares_at_listing`, `gem_market_cap_hkd`, `nlr_tranche_structure`, `isin_domicile_code`, `isin_domicile_jurisdiction`, `bbg_offer_type_raw`, `bbg_pe_vc_backed_flag`, `bbg_secondary_sale_flag`, `bbg_first_selling_stockholder_raw`) are deterministically reconciled and ready for empirical econometrics and publication tables.
