# 120-Variable Econometric Schema & Architecture Overview

---

## 1. Three-Tier Data Hierarchy & Data Provenance

In accordance with academic research standards and HKEX disclosure practices, the 120 variables are organized into three primary operational tiers:

| Tier Identifier | Column Range | Field Count | Primary Provenance | Extraction Mechanism |
|---|---|---|---|---|
| **Tier 1 (Green)** | Col A–K | 11 | HKEX Official New Listing Reports | Deterministic table parser (0 Tokens) |
| **Tier 2 (Light Blue)** | Col L–AY, DP, CJ, BA–CI | 60 | Statutory Prospectus Disclosures | Slicing + agent model + SHA-256 hash-gating |
| **Tier 3 (Dark Blue)** | Col CK, CM–DC | 18 | Allotment Results Announcements | Allotment slicing + deterministic derivations |
| **Tier 3 (Dark Blue)** | Col DD–DO, DF/DG | 31 | Market Trading & Macro Data | Offline feeds, HKMA API, and rules engine |

---

## 2. Key Empirical Variables & Cross-References

### Offering Size & Valuation
- `col_T`: Maximum Offer Price
- `col_K`: Final IPO Subscription / Offer Price
- `col_L`: Total Shares in Issue (excluding option)
- `col_M`: Global Offering Shares (excluding option)
- `col_CS`: Base Offer Shares
- `col_CX`: Net Proceeds Received by Issuer

### Cornerstone Demand & Market Sentiment
- `col_CK`: Cornerstone Allocation as % of Base Offer Shares
- `col_CL`: Earliest Cornerstone Lockup Expiry Date
- `col_CM`: Public Tranche Subscription Multiple
- `col_CP`: Final Public Tranche Allocated Shares (post-clawback)
- `col_CQ`: Final Price Determination Date
- `col_DA`: Free Float Percentage (%)

### Secondary Market Performance (Underpricing)
- `col_DI`: First-Day Opening Price
- `col_DH`: First-Day Closing Price
- `col_DM`: First-Day Turnover
- First-Day Return (Underpricing): `(col_DH - col_K) / col_K`

### Macroeconomic & Market Conditions
- `col_DD`: Hang Seng Index 20-Day Return Pre-IPO (%)
- `col_DE`: Number of Ordinary Main Board IPOs in Preceding 90 Days
- `col_DF`: 1-Month HIBOR on T-1 Trading Day (%)
- `col_DG`: Aggregate Balance of the HK Banking System on T-1 (HK$)

### Regulatory Classification & Special Regimes
- `col_BL`: Chapter 18A Biotech Indicator (1/0)
- `col_BM`: Chapter 18C Specialist Technology Indicator (1/0)
- `col_BK`: Weighted Voting Rights (WVR) Flag (1/0)
- `col_BJ`: Dual A+H Listing Flag (1/0)
- `col_DN`: FINI Clawback Mechanism (`Mechanism A` / `Mechanism B`)
- `col_BN`: Hang Seng Industry Classification System (HSICS 2026) 6-digit code
