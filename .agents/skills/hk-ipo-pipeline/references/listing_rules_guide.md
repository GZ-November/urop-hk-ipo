# HKEX Main Board Listing Rules & Cross-Check Reference Guide

This manual documents the quantitative listing criteria, statutory limits, and accounting consistency rules enforced by `run.py cross_check` against Hong Kong Exchanges and Clearing Limited (HKEX) Main Board Listing Rules.

---

## 1. Chapter 18C: Specialist Technology Companies

### Regulatory Background & 2024 Temporary Relief Reform
- **Original Benchmark (Effective March 2023)**:
  - Commercialized companies: Expected market capitalization not less than **HK$ 6.0 billion**.
  - Pre-Commercialized companies: Expected market capitalization not less than **HK$ 10.0 billion**.
- **Current Reform (Effective September 1, 2024, for 3 years)**:
  - **Commercialized Companies Minimum Market Cap**: Temporarily lowered to **HK$ 4.0 billion**.
  - **Pre-Commercialized Companies Minimum Market Cap**: Temporarily lowered to **HK$ 8.0 billion**.

### Sample Verification Examples (2026 Q1 Main Board)
- `6636.HK`: Expected market cap **HK$ 4.52 billion** (Commercialized Specialist Technology, satisfies >= HK$ 4.0B).
- `3625.HK`: Expected market cap **HK$ 5.60 billion** (Commercialized Specialist Technology, satisfies >= HK$ 4.0B).
- `6082.HK`: Expected market cap **HK$ 11.33 billion** (Satisfies >= HK$ 4.0B).

---

## 2. FINI Offering Mechanism & Public Clawback Triggers

HKEX price discovery and allotment framework under the FINI digital settlement platform:

### Mechanism A (Traditional Statutory Clawback Schedule)
If the issuer adopts standard tiered clawback:
- Subscription multiple `< 15x`: public tranche remains at the initial **5%**;
- Subscription multiple `>= 15x and < 50x`: public tranche increases to **15%**;
- Subscription multiple `>= 50x and < 100x`: public tranche increases to **25%**;
- Subscription multiple `>= 100x`: public tranche increases to **35%**.

### Chapter 18C Modification
For Specialist Technology Companies, Main Board Rule 18C.09 modifies the
general Practice Note 18 ladder:
- Subscription multiple `< 10x`: public tranche remains at **5%**;
- Subscription multiple `>= 10x and < 50x`: public tranche increases to **10%**;
- Subscription multiple `>= 50x`: public tranche increases to **20%**.

All ladder percentages use the shares initially offered under the Global
Offering as the denominator. Shares added through an Offer Size Adjustment
Option do not change that denominator.

### Mechanism B (Issuer-Determined Flexible Clawback)
- Issuers adopting Mechanism B pre-select a public subscription allocation of **10%–60%** with no clawback mechanism.
- Verification rule: compare the final allocation with the percentage disclosed in the statutory prospectus and flag any case-specific waiver separately.

---

## 3. Over-Allotment Option (Green Shoe) Statutory Ceiling

Pursuant to HKEX Main Board Listing Rules (Rule 10.08 and practice notes):
- The aggregate number of shares issued under an over-allotment option (Green Shoe) **must not exceed 15.00% of the initial base offer shares**.
- Pipeline cross-check formula: `col_CS * 0.15 >= actual_greenshoe_shares`.

---

## 4. Cornerstone Investor Statutory Lockup Period

Under HKEX Guidance Letter GL51-13 and prevailing market rules:
- Shares allocated to cornerstone investors are subject to a mandatory lockup period of **no less than 6 months (180 days)** from the official listing date.
- Pipeline cross-check formula: `Earliest Unlock Date (col_CL) - Listing Date (col_E) >= 180 days`.

---

## 5. First-Day Trading Price Bounds (OHLC Continuity)

Secondary market first-day transaction prices must satisfy mathematical continuity:
- `First Day Low <= First Day Open <= First Day High`;
- `First Day Low <= First Day Close <= First Day High`;
- `First Day Volume > 0` and `First Day Turnover > 0`.
