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
- Subscription multiple `< 15x`: No clawback triggered (public tranche remains at initial proportion, typically 10%);
- Subscription multiple `15x ~ 50x`: Public tranche increases to **30%**;
- Subscription multiple `50x ~ 100x`: Public tranche increases to **40%**;
- Subscription multiple `>= 100x`: Public tranche increases to **50%**.

### Mechanism B (Issuer-Determined Flexible Clawback)
- Issuers adopting Mechanism B disclose customized clawback schedules and fixed ceilings in the prospectus (e.g., initial 5%–10% expanding to a maximum cap of **20%**, as seen in `2513.HK`, `0100.HK`).
- Verification rule: The final public allocation proportion must never exceed the maximum ceiling disclosed in the statutory prospectus.

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
