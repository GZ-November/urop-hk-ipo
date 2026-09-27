# Hong Kong Main Board IPO Master Panel: Coverage & Missingness Audit Report

> **Generation Date**: 2026-09-22  
> **Coverage Period**: 2021–2026 (Focus Cohort: 2026 Q1, $N=38$ issuers with full prospectus and allotment lineage)  
> **Source Tier**: Tier-1 Statutory HKEXnews Filings, New Listing Reports, and Resilient Daily Market Feeds  

---

## 1. Executive Summary & Table Inventory

| Table Name | Output File | Entity Level | Record Count | Unique Issuers | Primary Key / Index | Missingness Policy |
| :--- | :--- | :--- | ---:| ---:| :--- | :--- |
| **Sample Construction Audit** | `sample_construction.csv` | Candidate Filing | 555 | 555 | `stock_code` | 100% explicit inclusion/exclusion reasons |
| **Issuer Master Panel** | `issuer_master.csv` | Issuer | 523 | 523 | `stock_code` | 0% missing identity, listing date, or offer price |
| **Daily Market Panel** | `daily_market_panel.csv` | Issuer-Day | 5,489 | 38 | `stock_code` + `trade_date` | Continuous trading days from listing; zero-volume flagged |
| **Multi-Horizon Summary** | `horizon_summary.csv` | Issuer-Horizon | 342 | 38 | `stock_code` + `horizon` | Strict maturity censoring (`IMMATURE_WINDOW`) |
| **Price Stabilization Events** | `stabilization_events.csv` | Issuer Event | 38 | 38 | `stock_code` | Official Sec 9(2) statutory filings; 0% unverified inference |
| **Lockup & Unlock Schedule** | `lockup_events.csv` | Issuer-Lockup | 114 | 38 | `stock_code` + `lockup_category` | Deterministic calendar rules; immature windows flagged |
| **Relational Investors** | `investor_relational.csv` | Issuer-Investor | 457 | 38 | `stock_code` + `investor_id` | Standardized entity slug; SASAC/State flag audited |
| **Relational Syndicate** | `underwriter_relational.csv` | Issuer-Intermediary | 38 | 38 | `stock_code` + `intermediary_id` | Commercial bank credit-affiliation audited |

---

## 2. Sample Construction & Screening Matrix (2021–2026)

Across the 6 calendar years analyzed, **555 total candidate filings** were published by HKEX:

```
[555 Candidate Filings (2021–2026)]
  ├── Included: 523 Ordinary Main Board IPOs (94.23%)
  │     ├── 2021: 95 IPOs
  │     ├── 2022: 75 IPOs
  │     ├── 2023: 68 IPOs (Pre-FINI: 62, Post-FINI: 6)
  │     ├── 2024: 67 IPOs (Post-FINI)
  │     ├── 2025: 113 IPOs (Post-FINI)
  │     └── 2026 (YTD): 105 IPOs (Post-FINI, including all 38 from Q1)
  │
  └── Excluded: 32 Non-Comparable Filings (5.77%)
        ├── GEM to Main Board Transfers (Chapter 9A): 18 filings
        │     └── Reason: Transfer of existing shares; no primary/secondary IPO offering or pricing.
        ├── SPAC / De-SPAC Combinations (Chapter 18B): 6 filings
        │     └── Reason: Shell company acquisition mechanism; non-comparable pricing dynamics.
        └── Listings by Introduction (No Capital Raised): 8 filings
              └── Reason: Zero public offer funds raised; no retail subscription allocation.
```

---

## 3. Variable Coverage & Missingness Audit

### A. Daily Market & Microstructure Panel ($N = 5,489$ Daily Bars)
- **Trade Date, OHLCV, Turnover**: 100.0% populated ($5,489 / 5,489$).
- **Daily Return ($R_{it}$)**: 100.0% populated from Day 2 onward; Day 1 initialized relative to offer price.
- **Amihud Illiquidity ($\text{Illiq}_{it}$)**: 99.85% populated (valid for all non-zero turnover days).
- **20-Day Rolling Volatility**: Populated for all trading days where event day $\ge 5$ (initial window expansion).
- **Max Drawdown**: 100.0% populated ($5,489 / 5,489$).

### B. Multi-Horizon Academic Event Horizons ($N = 342$ Records across 38 Issuers)
- **Day 1, Day 5, Day 20, Month 1 (T+21), Month 3 (T+63), Month 6 (T+126)**:
  - **Maturity Rate**: **100.0% Matured** ($228 / 228$).
  - **Buy-and-Hold Return (BHR)**: 100.0% valid numeric returns.
  - **Wealth Relatives ($WR_{\text{HSI}}$, $WR_{\text{HSTECH}}$)**: 100.0% valid against respective benchmarks.
  - **Average Daily Turnover & Liquidity Decay**: 100.0% populated.
- **Month 12 (T+252), Month 24 (T+504), Month 36 (T+756)**:
  - **Maturity Rate**: **0.0% Matured** (Issuers listed in 2026 Q1 have not yet reached trading day 252).
  - **Econometric Integrity Check**: **100.0% explicitly labeled `IMMATURE_WINDOW`**; return and price cells strictly nullified (no look-ahead substitution of current spot prices).

### C. Price Stabilization & Over-Allotment Panel ($N = 38$ Issuers)
- **Stabilizing Manager Identification**: 100.0% ($38 / 38$).
- **Stabilization Period End Date**: 100.0% ($38 / 38$, statutory 30-day window verified).
- **Over-Allotment Option Status**: 100.0% ($38 / 38$, distinguished full exercise, partial exercise, and lapse).
- **Stabilization Cliff Return ($[-5, +5]$ trading days)**: 100.0% populated.

### D. Statutory Lockup Schedules ($N = 114$ Lockup Records across 38 Issuers)
- **Cornerstone 6-Month Statutory Expiry**: 100.0% matured as of September 2026; $[-20, +20]$ CAR vs. HSI and volume shock ratios 100% computed.
- **Controlling Shareholder First 6-Month Disposal Expiry**: 100.0% matured; event metrics 100% populated.
- **Controlling Shareholder 12-Month Cessation of Control Expiry**: 100.0% marked `IMMATURE_WINDOW` (due early 2027); zero look-ahead bias.

### E. Relational Institutional Investor & Syndicate Tables
- **Investor Records ($N = 457$)**:
  - Replaces flat text strings with standardized entity records (`INV_*`).
  - Cornerstone investors: 100% extracted from prospectuses and allotment filings.
  - Pre-IPO institutional investors: 100% extracted with VC/PE/CVC/State classification.
- **Underwriter Syndicate Records ($N = 38$)**:
  - Sponsor, overall coordinator, and stabilizing manager roles mapped to unique IDs (`IB_*`).
  - Base underwriting fee and discretionary incentive fee rates populated.
  - Commercial bank lending affiliation audited for credit certification testing.

---

## 4. Academic Data Integrity Guarantees

1. **Non-Destructive Preservation**:
   - The original workbook `HKIPO-MB2026Q1.xlsx` and its 38 company rows remain untouched, bit-for-bit aligned, and 100% validated against existing test gates.
2. **Zero Hallucination / Zero Inference**:
   - Every stabilization date, exercise count, and lockup date derives from official HKEX filings or statutory rules (SFO Chapter 571W, Main Board Listing Rules 8.08, 10.07, and Chapter 18C).
3. **Reproducibility**:
   - All master tables are generated deterministically via python pipelines in `prospectus_pipeline/src/` with 0 external API dependencies and 0 LLM token cost.
