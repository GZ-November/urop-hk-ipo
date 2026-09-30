# IPO variable definitions and timing

Reference implementations: `scripts/ipo_metrics.py`. Returns are decimals.

## Contents
1. Timing and information sets
2. Initial return (underpricing)
3. Pricing and revision variables
4. Demand and allocation variables
5. Offer and firm characteristics
6. Intermediaries and investors
7. Aftermarket and lockup variables
8. Transformations and winsorization

---

## 1. Timing and information sets

Label every variable with *when it becomes known* relative to four dates:

| Date | Hong Kong document | What is fixed |
|---|---|---|
| Filing (A1) | Application proof / PHIP | Business, financials, risk factors |
| Launch | Prospectus (招股书) | Price range or fixed price, offer size, cornerstones, tranche split |
| Pricing | Price determination / pricing announcement | Final offer price P0 |
| Allotment | Allotment results announcement (配发结果公告) | Subscription multiples, clawback, final allocation, placee concentration |
| Listing | First trading day | P1, opening price; grey market (暗盘) trades the evening before |

Why it matters: a regressor known only *after* pricing (final oversubscription,
clawback outcome, grey-market return) cannot explain how the issuer and
underwriter set P0. It can describe the joint outcome, but its coefficient is
not a "determinant of underpricing". Retail demand responds to expected
underpricing, so oversubscription is jointly determined with the initial return.
Treat such variables as outcomes, as mediators, or instrument them; say which.

## 2. Initial return (underpricing, 首日抑价)

| Name | Formula | Notes |
|---|---|---|
| IR | P1 / P0 − 1 | P1 = first-day close. Ritter's standard definition. |
| log IR | ln(P1 / P0) | Preferred regression LHS when IR is right-skewed; report IR too. |
| MAIR (ratio) | (1 + IR)/(1 + Rm) − 1 | Aggarwal, Leal & Hernandez (1993). |
| MAIR (diff) | IR − Rm | Common and nearly identical when Rm is small. |
| Open return | P_open / P0 − 1 | Separates pre-open auction from intraday trading. |
| Grey-market return | P_grey / P0 − 1 | HK broker grey market (Futu, Phillip etc.) the evening before listing. |
| Decomposition | (1+IR) = (1+R_grey)(1+R_grey→close) | Splits pre-listing from listing-day price discovery. |
| Money left on table | (P1 − P0) × base offer shares | Excludes over-allotment (Ritter). Aggregate $ measure. |
| Proceeds-weighted IR | Σ MLT / Σ proceeds | Aggregate cost of underpricing; differs sharply from EW mean. |

**Market-adjustment window.** Rm runs from the index close on the pricing date
(or the subscription close; state which) to the index close on the first
trading day, because subscribers bear market risk over that interval. A
listing-day-only index return understates the adjustment. Hong Kong: pricing to
listing is about two business days since FINI went live (22 Nov 2023) and about
five before, so the choice matters more for pre-FINI samples. Benchmarks: Hang
Seng Composite Index (broad) is usually a better match for small and mid-cap
IPOs than the HSI (large-cap); for sector studies consider the Hang Seng
sector index; for A+H issuers also record the A-share price.

## 3. Pricing and revision variables

| Name | Formula | Notes |
|---|---|---|
| Price revision | (P0 − P_mid)/P_mid | Hanley (1993) partial adjustment: positive revisions predict higher IR. |
| Range position | (P0 − P_low)/(P_high − P_low) | Undefined for fixed-price offers; do not impute 0.5. Can be < 0 in HK (downward flexibility). |
| Range width | (P_high − P_low)/P_mid | Proxy for ex-ante valuation uncertainty. |
| Below/above range | indicator | HK Pricing Flexibility Mechanism permits pricing ≤ 10% below the range bottom if disclosed (HKEX Guide 4.14); upward flexibility was proposed in 2024 but *not* adopted. |
| Offer-price discount (A+H) | P0_H × FX / P_A − 1 | Use the A-share close on the pricing date; state FX source and date. |

Loughran & Ritter (2002) show public information (market returns during the
bookbuilding period) also predicts revisions and IR, contrary to strict
Benveniste–Spindt. Include the pre-pricing market return as a control when
testing partial adjustment.

## 4. Demand and allocation variables

| Name | Construction | Notes |
|---|---|---|
| Public oversubscription | valid applications / shares initially offered in public tranche | Use ln(1 + x); x can be < 1 (undersubscribed). Post-pricing information (see §1). |
| Placing oversubscription | as disclosed in allotment results | Often reported as a range or qualitatively; code missing, not 0. |
| Clawback outcome | final public-tranche % of offer shares | Mechanical function of oversubscription under PN18 / Mechanism A. |
| Margin financing (孖展) | broker margin subscription amount / public tranche size | Observable *before* pricing: a cleaner pre-pricing retail-demand proxy than final oversubscription. |
| Cornerstone share | cornerstone shares / total offer shares (base) | State base vs incl. over-allotment; state denominator. |
| Cornerstone presence | indicator | Endogenous: quality issuers attract cornerstones. |
| Placee concentration | top-1/top-5/top-25 placee shares ÷ placing shares | Disclosed in HK allotment results. |

## 5. Offer and firm characteristics

| Name | Construction | Notes |
|---|---|---|
| Ln(proceeds) | ln(P0 × base offer shares), constant-currency | Deflate multi-year samples (e.g. to a base-year HKD). |
| Primary share | new shares / total offer shares | Secondary sales signal insiders cashing out. |
| Overhang | pre-IPO shares retained / shares offered | Bradley & Jordan (2002). |
| Dilution | new shares / pre-IPO shares | |
| Firm age | ln(1 + years since founding at IPO) | Use founding (incorporation of operating entity), not holding-company date; document choice. |
| Size | ln(total assets) or ln(market cap at P0) | Pre-IPO fiscal year-end; state currency conversion date. |
| Profitability | indicator for positive net income; ROA | Many HK 18A/18C issuers are pre-revenue; the indicator matters more than the ratio. |
| Leverage | total liabilities / total assets | Pre-IPO balance sheet. |
| Listing route | Main Board ordinary, 18A (biotech), 18C (specialist tech), WVR, secondary/dual primary, A+H | Mutually exclusive route vs overlapping flags: define. |

## 6. Intermediaries and investors

| Name | Construction | Notes |
|---|---|---|
| Underwriter/sponsor reputation | Market-share rank (Megginson & Weiss 1991) computed over a *prior* window, or Carter–Manaster (1990) tombstone ranks (US only; Loughran & Ritter 2004 update) | In HK use sponsor / overall coordinator market share by proceeds over the previous 1–3 years. Avoid contemporaneous shares that include the IPO itself. |
| VC/PE backing | indicator; also pre-IPO investor share | Megginson & Weiss (1991) certification vs Gompers (1996) grandstanding. Distinguish "unknown" from "no". |
| Syndicate size | number of bookrunners / overall coordinators | HK IPOs often have very large syndicates. |
| State-owned cornerstone | indicator | Separate from total cornerstone share. |

## 7. Aftermarket and lockup variables

| Name | Construction | Notes |
|---|---|---|
| Aftermarket BHR | compounded from first-day close (t = 1 starts day 2) | Excludes the initial return; state this. |
| Total return from offer | compounded from P0 | Includes IR. Different object. |
| Stabilization / greenshoe | over-allotment option (≤ 15%), exercise % | HK stabilizing period ends 30 days after the last day for lodging applications (SFC Price Stabilizing Rules). |
| Lockup expiry windows | CAR around day +180 (cornerstones, 6 months), controlling shareholders 6 + 6 months | Field & Hanka (2001); Brav & Gompers (2003). |
| Turnover | day-1 volume / shares offered | Liquidity and flipping proxy. |

Mark each horizon's maturity: an IPO whose 6-month window has not elapsed has
a *missing* 6M return, not a zero and not a truncated one.

## 8. Transformations and winsorization

- Winsorize continuous regressors at 1/99 (or 0.5/99.5 in small samples) with
  `ipo_metrics.winsorize`, which is NaN-safe; within listing year for pooled
  multi-year samples. Do not winsorize binaries, ranks or shares bounded in [0,1].
- The dependent variable: prefer log IR (a transformation, not data removal) as
  the main LHS and show raw IR, winsorized IR and median/quantile regression as
  robustness. Winsorizing the LHS changes the estimand; say so.
- Scale: report returns in decimals in code; convert to % only in tables.
- Log of zero: use ln(1 + x) only for counts/multiples where 0 is meaningful.
- Currency: convert RMB/USD figures to HKD at a dated rate before ratios mix
  items; never mix units inside one regressor.
- Missing ≠ zero: unknown VC backing, undisclosed placing demand and immature
  horizons stay missing; report N per variable.
