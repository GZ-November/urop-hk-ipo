# Hong Kong Main Board IPO Dataset: New Data Priority Matrix & Econometric Architecture

## Executive Summary

To elevate the Hong Kong Main Board IPO dataset from a single-quarter cross-section ($N=38$, 2026 Q1) into a world-class empirical corporate finance and market-microstructure panel, this matrix systematically evaluates the 10 data expansion priorities defined in the empirical research agenda.

Each proposed field is scored across six rigorous dimensions:
1. **Research Value**: Contribution to answering fundamental questions in IPO pricing, intermediary behavior, corporate governance, and long-run asset pricing.
2. **Identification Value**: Ability to exploit regulatory discontinuities, policy reforms, and quasi-experimental variation (e.g., FINI digitisation on Nov 22, 2023; Chapter 18C threshold revisions; Price Stabilizing Rules).
3. **Source Reliability**: Cryptographic verification against statutory exchange filings (Tier-1 official HKEX prospectuses and announcements) vs. unverified media/broker estimates.
4. **Expected Coverage**: Feasibility of achieving near-complete ($\ge 95\%$) coverage across issuers without systematic attrition bias.
5. **Collection Cost**: Engineering and extraction complexity (deterministic automation vs. manual auditing).
6. **Maintenance Cost**: Forward-looking pipeline maintainability as new companies list each week.

---

## 1. Multi-Dimensional Priority Matrix (Ranked 1 to 10)

| Rank | Priority Area | Core Variables | Primary Research Ideas Supported | Source & Tier | Expected Coverage | Ident. Value | Research Value | Implementation Difficulty | Recommended Phase |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **1** | **Sample Expansion (2021–2026)** | Multi-year IPO master panel, inclusion/exclusion audit, FINI regime flag | Idea 01, 02, 08, 20 | HKEX New Listing Reports (`NLR2021`–`2026_Eng.xlsx`) [Tier-1] | **100%** ($N \approx 524$ clean IPOs) | **Maximum** | **Exceptional** | **Low to Moderate** | **Phase A** |
| **2** | **Daily Market & Liquidity Panel** | Daily OHLCV, turnover, Amihud illiquidity, zero-volume days, BHR, WR vs HSI/HSTECH across Day 1, 5, 20, 1M, 3M, 6M, 12M, 24M, 36M | Idea 03, 08, 11, 20 | Tencent Securities K-Line / Yahoo Finance API [Tier-1/2] | **98–100%** (Active trading series) | **High** | **Very High** | **Moderate** | **Phase A/B** |
| **3** | **Stabilization & Over-Allotment** | Stabilization manager, purchase dates, price range, stock borrowing, greenshoe exercise vs lapse, expiry date | Idea 05, 11 | HKEXnews Sec 9(2) Price Stabilizing Announcements [Tier-1] | **100%** (All greenshoe offerings) | **Very High** | **Very High** | **Moderate** | **Phase A/B** |
| **4** | **Lockup & Unlock Schedules** | Cornerstone 6M expiry, controlling shareholder 6M/12M, Pre-IPO/WVR lockups, [-20,+20] and [0,+60] abnormal return/volume | Idea 03, 09 | Listing Rules 8.08/10.07, Prospectus Lockup Deeds [Tier-1] | **100%** (Statutory & contractual rules) | **Maximum** | **Very High** | **Moderate** | **Phase A/B** |
| **5** | **Structured Investor Relational Table** | Standardized Parent ID, investor category (Cornerstone, Pre-IPO VC, PE, CVC, State, Crossover), shares, valuation, board seat | Idea 03, 04, 14 | Prospectus History & Cornerstone Chapters, Allotment Results [Tier-1] | **90–95%** (Disclosed institutional investors) | **High** | **High** | **Moderate** | **Phase C** |
| **6** | **Underwriting Syndicate Structure** | Intermediary ID, roles (Sponsor, OC, GC, Bookrunner, Underwriter), gross spread %, discretionary incentive fee %, bank credit tie | Idea 05, 10, 17, 18 | Prospectus Underwriting Chapter, Allotment Announcements [Tier-1] | **95–100%** | **High** | **High** | **Moderate** | **Phase C** |
| **7** | **A+H Price-Anchor Panel** | A-share ticker, pre-prospectus/pre-pricing/pre-listing A-share price, turnover, volatility, H/A offer price discount, FX conversion | Idea 01, 06 | SSE / SZSE Daily K-Line via Tencent/Yahoo [Tier-1] | **100%** ($N \approx 40$ A+H dual listings) | **Very High** (for A+H) | **Moderate to High** | **Low to Moderate** | **Phase B** |
| **8** | **Offering & Retail Allocation** | Mechanism A vs B, FINI clawback triggers, Pool A/B applications, One-Person-One-Lot allocation probability | Idea 02, 08, 13 | Official HKEX Allotment Results Announcements [Tier-1] | **100%** | **High** | **Moderate to High** | **Low to Moderate** | **Phase A** |
| **9** | **Governance & Insider Ownership** | Board size, independent director %, female %, founder CEO, CEO-chair duality, WVR voting rights wedge | Idea 07, 15 | Prospectus Directors & Substantial Shareholders Chapters [Tier-1] | **95%** | **Moderate** | **Moderate** | **Moderate** | **Phase D** |
| **10** | **Post-IPO Operating Performance** | Semi-annual/annual revenue, gross profit, EBITDA, net profit, OCF, CapEx, R&D, cash, debt, proceeds usage progress | Idea 04, 20 | HKEX Listed Company Annual & Interim Reports [Tier-1] | **Matured cohorts** (2021–2024: 100%; 2025: 50%; 2026: 0%) | **Moderate** | **Moderate to High** | **High** | **Phase D** |

---

## 2. Deep-Dive: The Ten Most Valuable Additions

### 1. Multi-Year Main Board IPO Panel ($N \approx 524$, 2021–2026)
- **Scientific Rationale**: A 38-issuer cross-section cannot distinguish between time-series macroeconomic shocks (e.g., Fed interest rate hikes, China stimulus) and regulatory effects. Expanding the sample across 2021–2026 creates a multi-year panel spanning:
  - Pre-FINI (T+5 settlement, paper forms, margin lockup) vs. Post-FINI (T+2 digital settlement from Nov 22, 2023).
  - Introduction of Chapter 18C (March 2023) and the August 2024 market cap threshold reduction (Commercialized firms: HK\$ 8B $\to$ HK\$ 4B; Uncommercialized: HK\$ 10B $\to$ HK\$ 8B).
  - Hot market cycles (2021 tech boom) vs. cold issue markets (2022–2023 liquidity contraction) vs. 2025–2026 recovery.
- **Empirical Filtering**: Excludes GEM transfers (no new capital raising), De-SPAC/SPACs, and listings by introduction.

### 2. Daily Trading & Liquidity Panel with Strict Maturity Censoring
- **Scientific Rationale**: Resolves the "long-run underperformance puzzle" (Lowry et al. 2017 Ch 7) by computing Buy-and-Hold Returns (BHR) and Wealth Relatives (WR) against both broad market (Hang Seng Index) and growth/tech benchmarks (Hang Seng TECH Index).
- **Microstructure Variables**: Daily Amihud illiquidity ($\frac{|R_{it}|}{\text{Turnover}_{it}} \times 10^6$), zero-volume days, and rolling return volatility reveal whether trading dries up following the first-day flipping frenzy (Aggarwal 2003).
- **Econometric Rule**: Strict maturity gating ensures no future look-ahead imputation; unexpired horizons remain explicitly missing with standardized status codes (`IMMATURE_WINDOW`).

### 3. Price Stabilization & Over-Allotment Execution Panel
- **Scientific Rationale**: Tests whether underwriting price support masks true market sentiment and precipitates a "post-stabilization price cliff" once the 30-day statutory window expires (Securities and Futures Chapter 571W).
- **Variables**: Exact stabilization period dates, stabilizing manager identity, whether stabilization purchases occurred, purchase price range, and over-allotment exercise percentage.

### 4. Statutory Lockup Schedules & Event-Window Impacts
- **Scientific Rationale**: Identifies the "chip avalanche effect" (Idea 09). The Hong Kong regulatory regime imposes distinct staggered lockups:
  - Cornerstone investors: 6 months from listing.
  - Controlling shareholders: 6 months absolute lockup + 6 months disposal restriction preventing loss of control (Listing Rule 10.07).
  - Chapter 18C Key Pre-IPO Investors: 12 months (Senior) / 24 months (Controlling).
- **Event Windows**: $[-20, +20]$, $[-5, +5]$, and $[0, +60]$ trading-day windows capture price drift, volume surges, and liquidity evaporation around unlock dates.

### 5. Relational Investor Master Table
- **Scientific Rationale**: Replaces unstructured name strings with an entity-level database linking investors to standardized parent groups, classifying them into PE, VC, Corporate VC (CVC), State-Owned Capital, and Crossover Funds.
- **Key Hypotheses**: Tests Gompers (1996) VC grandstanding vs. Megginson-Weiss (1991) certification, and tests whether crossover funds that act both as Pre-IPO backers and Cornerstone placees mitigate or exacerbate agency conflicts (Idea 14).

### 6. Relational Syndicate & Discretionary Incentive Fee Structure
- **Scientific Rationale**: Disentangles the fixed underwriting commission from discretionary incentive fees (Rule 3A.02). Evaluates whether syndicate expansion leads to free-riding (Corwin and Schultz 2005) or whether commercial-bank sponsors certify borrower creditworthiness (Idea 10).

### 7. A+H Cross-Market Valuation Anchor Panel
- **Scientific Rationale**: Dual-listed issuers possess an observable, exogenous mainland price anchor immediately prior to Hong Kong listing. This provides clean identification for testing whether underpricing reflects true information extraction (Rock 1986, Benveniste-Spindt 1989) or intentional wealth transfer / "money left on the table" (Loughran-Ritter 2002).

### 8. FINI Offering Mechanism A vs. B & Retail Allocation Microstructure
- **Scientific Rationale**: Compares FINI Allocation Mechanism A (statutory 50% retail clawback) vs. Mechanism B (custom clawback ceiling). Measures retail rationing and lottery probability (one-person-one-lot allocation rate).

### 9. Life-Cycle Corporate Governance & WVR Wedge
- **Scientific Rationale**: Analyzes the wedge between voting rights and economic cash flow rights in Weighted Voting Rights (WVR / Chapter 8A) issuers, board independence, female director diversity, and founder CEO-chair duality (Lowry et al. 2017 Ch 9).

### 10. Post-Listing Multi-Year Operating Trajectory
- **Scientific Rationale**: Compares post-IPO financial performance (revenues, R&D intensity, EBITDA margins, cash burn rate) against prospectus use-of-proceeds milestones to test whether pre-IPO earnings were inflated or whether firms successfully commercialize.

---

## 3. Recommended Phase A Scope

### Immediate Implementation Targets:
1. **Multi-Year Issuer Sample (2021–2026)**:
   - Ingest official HKEX NLR reports (`NLR2021` through `NLR2026_Eng.xlsx`).
   - Standardize all candidate records ($N \approx 550+$).
   - Apply verifiable exclusion filters: GEM transfers (e.g. 9893.HK, 9876.HK, 6051.HK, 3774.HK), De-SPAC transactions (e.g. 6676.HK, 2665.HK), and non-capital introductions (e.g. 6887.HK, 7489.HK).
   - Establish the Clean Master Issuer Table ($N \approx 524$ ordinary IPOs), ensuring the existing 38 issuers in 2026 Q1 remain 100% untouched and aligned.
2. **Event-Level Daily Trading Panel**:
   - Collect daily OHLCV and turnover from listing date to present for all active issuers.
   - Compute BHR, Total Return, Amihud Illiquidity, Zero-Volume Days, and Wealth Relatives across matured horizons (Day 1, 5, 20, 1M, 3M, 6M, 12M).
   - Enforce strict maturity guards on unreached horizons.
3. **Stabilization & Lockup Tables**:
   - Parse statutory stabilization and over-allotment announcements for all issuers.
   - Formulate deterministic lockup calendar schedules.
4. **Validation, Auditing, and Codebook**:
   - Update schemas, generate test suites, and provide reproducible CSV and codebook exports.
