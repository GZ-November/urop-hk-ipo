# Verification and Audit Memo: U.S. IPO Benchmarks & Mainland Policy Valve Panel (1994–2026)

**Data Engineer**: External Benchmark & Mainland Policy Timeline Specialist  
**Project**: 1994–2026 Hong Kong IPO Overview Research Monograph  
**Date**: November 11, 2026  
**Primary Deliverables**:
1. [`clean_us_ritter_annual_1994_2025.csv`](file:///Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026/clean_us_ritter_annual_1994_2025.csv) ($N = 32$ annual rows)
2. [`clean_monthly_policy_valve_1994_2026.csv`](file:///Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026/clean_monthly_policy_valve_1994_2026.csv) ($N = 393$ monthly rows)

---

## 1. Executive Summary & Corrections to Prior Hardcoded Benchmarks

In prior draft scripts (`build_us_hk_parallel_table.py`), several benchmark figures for 2017–2025 were either preliminary estimates, unverified citations, or conflated equal-weighted with proceeds-weighted returns. We have audited the series against Professor Jay R. Ritter's official University of Florida tables (*Initial Public Offerings: Updated Statistics*, November 5, 2026 / July 13, 2026 update, Tables 1, 1a, 8, 10, 11) and Lowry, Michaely, and Volkova (2017, Table 3.1).

### Key Errors Fixed:
1. **2020 First-Day Return Conflation**:
   - *Prior Script*: Entered `US_EW_IR_Pct = 47.9%`.
   - *Audit Finding*: **47.9% was Ritter's proceeds-weighted return**! The correct **equal-weighted initial return was 41.6%** (median = 26.2%). Conflating EW with PW exaggerated standard U.S. average underpricing by 6.3 percentage points.
2. **2021 Volume and Proceeds Precision**:
   - *Prior Script*: Entered `Proceeds = $119.10B`, `IR = 32.0%`.
   - *Audit Finding*: Official Ritter Table 1 specifies **$119.36B in gross proceeds** and **32.1% equal-weighted return** ($N = 311$).
3. **2022 Gross Proceeds**:
   - *Prior Script*: Entered `$6.90B`.
   - *Audit Finding*: Official Ritter Table 1 records **$6.99B** ($N = 38$, EW IR = 48.9%, PW IR = 14.2%).
4. **2023 Preliminary vs Finalized Statistics**:
   - *Prior Script*: Entered `54 IPOs, 12.5% IR, $16.40B proceeds`.
   - *Audit Finding*: The $16.40B was a raw preliminary estimate before CRSP exclusions. Ritter's official Table 1 records **54 operating-company IPOs, 11.9% equal-weighted return, -0.5% median return, and $11.92B in gross proceeds**!
5. **2024 Preliminary vs Finalized Statistics**:
   - *Prior Script*: Entered `71 IPOs, 15.6% IR, $25.30B proceeds`.
   - *Audit Finding*: Ritter's official Table 1 records **73 operating-company IPOs, 15.3% equal-weighted return, 7.2% median return, and $20.90B in gross proceeds**.
6. **2025 Finalized Series Addition**:
   - *Prior Script*: Marked `np.nan` ("Pending Ritter update").
   - *Audit Finding*: Complete official 2025 data are now available: **90 operating-company IPOs, 29.3% equal-weighted return, 33.6% proceeds-weighted return, 13.7% median return, $13.11B money left on the table, and $38.97B in gross proceeds**.
7. **U.S. 7% Gross Spread Persistence**:
   - Audited against Chen & Ritter (2000, *Journal of Finance*), Abrahamson, Jenkinson & Jones (2011, *RFS*), and Ritter (Updated Statistics Table 10, December 31, 2025):
   - Over 2001–2025, for moderate-size U.S. operating company IPOs ($30M–$160M in 2025 dollars), **93.3% (1,064 out of 1,141 IPOs) had gross spreads of exactly 7.00%**.
   - By contrast, for large deals (>$160M), 54.4% were <7% and 45.1% were =7%.

---

## 2. Definitive Chronology of CSRC A-Share IPO Freezes (1994–2026)

Between 1994 and 2026, the China Securities Regulatory Commission (CSRC) implemented **9 official complete IPO moratoria** (Freezes 1 to 9), followed by the post-2023 **counter-cyclical phased tightening ("8·27" regime)**:

| # | Regime Name | Start Date | End Date | Calendar Months | Key Trigger & Context |
|---|---|---|---|---|---|
| **1** | `1994-07_1994-12_Bailout_Freeze` | 1994-07-21 | 1994-12-07 | 1994-07 to 1994-12 | Shanghai Index crashed to 333 points; State Council issued "Three Major Bailout Measures". |
| **2** | `1995-01_1995-06_Bond_Futures_Freeze` | 1995-01-19 | 1995-06-09 | 1995-01 to 1995-06 | Market stagnation & the "327 Treasury Bond Futures" scandal (327国债期货事件). |
| **3** | `1995-07_1996-01_Bear_Market_Freeze` | 1995-07-05 | 1996-01-03 | 1995-07 to 1996-01 | Severe liquidity drainage and persistent secondary market slump. |
| **4** | `2001-07_2001-11_State_Share_Freeze` | 2001-07-31 | 2001-11-02 | 2001-07 to 2001-11 | State-owned share reduction at market prices (国有股减持) triggered a violent market crash from 2,245 points. |
| **5** | `2004-08_2005-01_Inquiry_Reform_Freeze` | 2004-08-26 | 2005-01-23 | 2004-08 to 2005-01 | CSRC halted approvals during the transition to the institutional bookbuilding/inquiry system (首次公开发行股票询价制度). |
| **6** | `2005-05_2006-06_Split_Share_Reform_Freeze` | 2005-05-25 | 2006-06-02 | 2005-05 to 2006-06 | Full-scale Split-Share Structure Reform (股权分置改革). Longest complete moratorium in A-share history (~1 year, 264 trading days). |
| **7** | `2008-09_2009-06_GFC_Freeze` | 2008-09-25 | 2009-06-29 | 2008-09 to 2009-06 | Global Financial Crisis crash from 6,124 points; reopened with Guilin Sanjin (桂林三金) on 2009-06-29. |
| **8** | `2012-11_2013-12_Financial_Audit_Freeze` | 2012-11-16 | 2013-12-30 | 2012-11 to 2013-12 | CSRC nationwide financial fraud inspection storm (史上最严财务大检查) and underwriting regime reform (14-month freeze). |
| **9** | `2015-07_2015-11_Stock_Crash_Freeze` | 2015-07-04 | 2015-11-06 | 2015-07 to 2015-11 | 2015 A-share stock market crash emergency bailout package suspending 28 pending offerings; announced resumption on Nov 6, 2015. |
| **10** | `2023-08_2026-09_Counter_Cyclical_Tightening` | 2023-08-27 | 2026-09-30 | 2023-08 to 2026-09 | CSRC "8·27" phased pace tightening ("阶段性收紧IPO节奏") and State Council New "Nine National Measures" (新国九条) raising listing thresholds. |

---

## 3. Major Cross-Border Offshore Listing Policy Shocks

Four statutory and administrative milestones transformed the regulatory valve between the Mainland and Hong Kong:

1. **2020-12-18 (HFCAA Enacted)**:
   - *Statute*: U.S. Holding Foreign Companies Accountable Act signed into law.
   - *Mechanism*: Mandated PCAOB audit inspection access within 3 years or face trading prohibitions on U.S. exchanges, triggering the large-scale homecoming wave of U.S.-listed Chinese ADRs to HKEX (dual-primary and secondary listings).
2. **2021-07-10 (CAC Cybersecurity Review Draft)**:
   - *Regulation*: Cyberspace Administration of China (国家互联网信息办公室) published draft *Cybersecurity Review Measures* (网络安全审查办法修订草案征求意见稿).
   - *Mechanism*: Article 6 required platforms holding personal information of >1 million users to undergo mandatory national cybersecurity clearance before listing abroad, effectively closing the direct U.S. IPO window for Mainland tech platforms.
3. **2023-03-31 (CSRC Overseas Listing Filing Regime Effective)**:
   - *Regulation*: CSRC *Trial Administrative Measures of Overseas Securities Offering and Listing by Domestic Companies* (境内企业境外发行证券和上市管理试行办法).
   - *Mechanism*: Formalized unified filing requirements for both direct (H-share) and indirect (Red-Chip / VIE) offshore offerings, replacing traditional administrative approvals with a codified compliance pipeline.
4. **2024-04-19 (CSRC Five Measures on HK Capital Market Cooperation)**:
   - *Regulation*: CSRC announced 5 measures to deepen cooperation with Hong Kong (中国证监会发布5项资本市场对港合作措施).
   - *Mechanism*: Measure 5 explicitly states: "Support leading mainland industry enterprises to list in Hong Kong" (支持内地行业龙头企业赴香港上市), providing official political and regulatory backing for Mainland champions to tap HKEX liquidity amid domestic A-share tightening.

---

## 4. Summary Statistics of the 393-Month Panel (`1994-01` to `2026-09`)

- **Total Calendar Months**: **393 months** (1994-01 through 2026-09).
- **Months with >= 1 IPO**: **380 months** (96.7%).
- **Zero-IPO Months**: **13 months** (3.3%) — coinciding with acute macroeconomic shocks:
  - 1998-08 (Asian Financial Crisis peak / HKMA currency defense)
  - 1998-11, 1999-01, 1999-02 (post-AFC winter)
  - 2006-08, 2006-11
  - 2008-01, 2008-09 (Lehman Brothers collapse)
  - 2011-08 (U.S. sovereign debt downgrade / European debt crisis)
  - 2012-09
  - 2023-02, 2023-08 (CSRC 8·27 tightening onset)
  - 2024-02 (Chinese New Year lull)
- **HKEX Ordinary IPOs ($N = 2,865$)**:
  - Main Board: **2,476 IPOs**
  - GEM: **389 IPOs**
  - PRC Joint Stock Company H-Shares (`is_prc_joint_stock == 1`): **659 IPOs** (23.0% of total count, raising HK$ 2,769.3 billion or 49.0% of total capital)
  - Statutory CNE ISIN H-Shares (`is_cne_isin == 1`): **581 IPOs**
  - Non-H-Share Issuers (Local HK, Red-Chip, VIE, International): **2,206 IPOs** (raising HK$ 2,887.5 billion or 51.0% of total capital)
  - Aggregate Gross Proceeds: **HK$ 5,656.8 billion** (~US$ 725.2 billion)
- **CSRC A-Share Freeze Exposure**:
  - Strict Complete Moratoria (Freezes 1 to 9): **73 months** (18.6% of panel) had at least 1 day of complete A-share halt; **55 months** were under a 100% full-month freeze.
  - Total Policy Restrictions (including 2023-08+ tightening): **111 months** (28.2% of panel).
- **Macro Market Benchmarks**:
  - HSI monthly return range: **-28.28%** (1997-10 Asian Financial Crisis) to **+30.50%** (1998-10 post-defense rebound).
  - HSI 20-day realized volatility range: **8.62%** (2017-09 low-vol regime) to **109.91%** (1997-10 AFC turbulence).
