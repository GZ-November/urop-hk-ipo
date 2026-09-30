# Hong Kong IPO institutions for empirical work

Last verified: 30 Sep 2026 against HKEX Guide for New Listing Applicants
ch. 4.14 (Offering-related Mechanisms) and law-firm summaries of the Aug-2025
consultation conclusions. Rules change: before relying on a threshold for a
design, re-check the current HKEX rulebook and the issuer's prospectus, which
also discloses any waiver granted.

## Contents
1. Offer structure and timeline
2. Regime dates that split samples
3. Public tranche allocation: old PN18 vs Mechanism A/B
4. Cornerstones, placing and public float
5. Pricing, stabilization, lockups
6. Listing routes and issuer types
7. Data sources
8. Research designs these institutions enable
9. Hong Kong-focused literature starting points

---

## 1. Offer structure and timeline

A global offering has a **Hong Kong public offer** (retail, 公开发售) and an
**international placing** (institutions, 国际配售), plus **cornerstone
investors** (基石投资者) who commit before the prospectus at the final offer
price. Sequence: prospectus and price range → public subscription (about 3.5
business days) and bookbuilding → price determination → allotment results →
grey-market trading (暗盘, broker platforms, evening before listing) → listing.
Retail can subscribe with broker margin financing (孖展), which is reported
publicly day by day and is a pre-pricing demand signal.

Unlike the US, retail demand is revealed through a public tranche with
disclosed oversubscription and price is set after the public offer closes. The
lag between pricing and trading means subscribers bear market risk (Chowdhry &
Sherman 1996 relate this timing to underpricing in HK/UK-style offerings).

## 2. Regime dates that split samples

| Date | Change | Empirical implication |
|---|---|---|
| 22 Nov 2023 | FINI settlement platform: pricing-to-trading shortened from T+5 to T+2 business days; new pre-funding model for public offer | Shorter market-risk window; pre/post comparison of MAIR windows and subscription behaviour. |
| 4 Aug 2025 | Consultation conclusions (published 1 Aug 2025) effective for listing documents published on or after this date: ≥ 40% of offer shares to the bookbuilding placing tranche; Mechanism A/B for the public tranche; tiered initial public float; new free-float requirement; cornerstone 6-month lockup retained; upward pricing flexibility **not** adopted | Structural break in allocation, retail share and cornerstone room. Define the regime by prospectus date, not listing date. |
| Pending/2025–26 | Ongoing public float consultation (Aug 2025; conclusions Dec 2025) | Affects post-listing float studies; check effective dates. |
| Mar 2023 | Chapter 18C (specialist technology) regime | New route; exempt from Mechanism A/B; ≥ 50% of offer shares to independent price-setting investors. |
| 2018 | Chapter 8A (WVR) and 18A (pre-revenue biotech); Chapter 19C secondary listings | Route indicators; pre-revenue issuers. |

## 3. Public tranche allocation

**Pre-reform PN18 (prospectuses before 4 Aug 2025).** Initial public
allocation 10% of offer shares; clawback raises it to 30% when the public
tranche is ≥ 15× and < 50× subscribed, 40% at ≥ 50× and < 100×, 50% at ≥ 100×.
Large offerings often obtained waivers with lower triggers (a "Typical PN18
Waiver" in Guide 4.14: 5% initial, then 7.5% / 10% / 20%). Reallocation from an
under-subscribed placing to an over-subscribed public tranche is capped
("Allocation Cap"); see Guide 4.14 for the conditions.

**Mechanism A (from 4 Aug 2025).** Initial public allocation 5%; at ≥ 15× and
< 50×: 15%; ≥ 50× and < 100×: 25%; ≥ 100×: 35%.

**Mechanism B.** Minimum initial allocation 10% with no clawback; the maximum is
60% because ≥ 40% must go to the bookbuilding placing tranche.

Neither mechanism applies to 18C issuers. HKEX can grant waivers for very
large offers, so code the mechanism and the actual allocation from each
prospectus and allotment announcement; never infer them from the rules alone.

Coding implications:
- Oversubscription multiple is measured against the *initial* public
  allocation; the post-clawback share is an outcome of it.
- Retail allocation jumps discontinuously at 15×/50×/100×. Around those
  thresholds, allotment ratios and one-lot success rates change sharply.
- Pre/post reform comparisons of "retail share" mix a rule change with demand.

## 4. Cornerstones, placing and public float

- Cornerstone shares are subject to a 6-month lockup from listing; cornerstones
  buy at the offer price and are named in the prospectus with commitment size.
- After Aug 2025 the ≥ 40% bookbuilding-placing floor (excluding cornerstones)
  caps cornerstone room at about 55% (Mechanism A, 5% public) or 50%
  (Mechanism B, 10% public) of offer shares before clawback.
- Initial public float is tiered by expected market value at listing: ≤ HK$6bn:
  25%; HK$6–30bn: higher of 15% or the % giving HK$1.5bn in public hands;
  > HK$30bn: higher of 10% or the % giving HK$4.5bn. A+H issuers: H shares in
  public hands ≥ 10% of the H-share class or HK$3bn. Free float (public and not
  locked up) ≥ 10% (market value ≥ HK$50m) or HK$600m; 5% for A+H issuers.
- The old guideline of at least 3 placees per HK$1m of placing (minimum 100)
  was removed in Aug 2025.
- Allotment announcements disclose placee concentration (top 1/5/25 placees)
  and cornerstone holdings; these support studies of allocation concentration.

## 5. Pricing, stabilization, lockups

- **Price range.** Pricing Flexibility Mechanism: final price can be up to 10%
  below the indicative price or range bottom if disclosed; with a range, the
  top may not exceed the bottom by more than 30%. Pricing lower than 10% below
  requires cancellation and relaunch.
- **Offer size adjustment option** (upsize, typically up to 15%) and
  **over-allotment option** (greenshoe, up to 15%) are separate; record each.
- **Stabilization** under the SFC Securities and Futures (Price Stabilizing)
  Rules; the stabilizing period ends 30 days after the last day for lodging
  applications under the public offer. The stabilizing manager's post-period
  announcement discloses actions and greenshoe exercise.
- **Lockups.** Controlling shareholders: no disposal in the first 6 months and
  must remain controlling shareholders for the next 6 months (Main Board Rule
  10.07); cornerstones 6 months; pre-IPO investors per contract (often 6–12
  months, disclosed in prospectus).

## 6. Listing routes and issuer types

Main Board ordinary IPO; Chapter 8A WVR; Chapter 18A pre-revenue biotech;
Chapter 18C specialist technology (commercial / pre-commercial); Chapter 19C
secondary listing and dual-primary listings (often US-listed Chinese firms);
H-share issuers (PRC-incorporated) with or without A shares (A+H). Transfers
from GEM, SPAC/de-SPAC and listings by introduction raise no public-offer
capital and are usually excluded from underpricing samples. Define the
research population and log every exclusion with a reason.

## 7. Data sources

- **HKEXnews** (www.hkexnews.hk): prospectuses, formal notices, allotment
  results, stabilization announcements, lockup-related announcements.
- **HKEX Main Board new listing reports** (annual/monthly): population lists.
- Market data: HKEX historical prices; vendors (Wind, iFinD, CSMAR HK,
  LSEG/Refinitiv Datastream, Bloomberg, S&P Capital IQ). Check adjustment for
  corporate actions and suspension handling per vendor.
- Grey-market prices: broker platforms (not exchange data); document source.
- Margin financing: broker-aggregated daily figures reported in financial media;
  document the aggregator and snapshot time.
- Factors: Kenneth French Data Library, Asia Pacific ex Japan (USD).
- Global comparisons: Jay Ritter's IPO data site (US statistics, international
  underpricing tables).

## 8. Research designs enabled by these institutions

- **Clawback thresholds** (15×/50×/100×) → regression discontinuity or bunching
  in oversubscription; test manipulation of the running variable; retail
  subscribers know the thresholds, so demand near them is strategic.
- **Aug-2025 reform** → before/after with market controls; 18C issuers
  (exempt from Mechanism A/B) as a small comparison group; Mechanism A vs B
  choice as an issuer decision (itself endogenous: model it).
- **FINI** → shorter market-risk window; test whether MAIR and the IR–market
  return link change.
- **Grey market** → decompose IR into pre-listing and listing-day components;
  test whether grey-market prices are unbiased predictors of first-day close.
- **Margin financing** → pre-pricing retail demand; test partial adjustment of
  price to *observable* retail demand.
- **Cornerstone lockup expiry at 6 months** → CAR and volume around day +180.
- **A+H issuers** → H-share offer discount relative to A-share price as a
  directly observable valuation benchmark.

## 9. Literature starting points (verify details before citing)

- McGuinness (1992), underpricing of Hong Kong IPOs, 1980–90, *Journal of
  Business Finance & Accounting*.
- Chowdhry & Sherman (1996), international differences in oversubscription and
  underpricing, *Journal of Corporate Finance*.
- "The role of 'cornerstone' investors and the Chinese state in the relative
  underpricing of state- and privately controlled IPO firms", *Applied
  Financial Economics* 22(18), 2012.
- "Committed anchor investment and IPO survival – the roles of cornerstone and
  strategic investors", *Journal of Corporate Finance* 41 (2016), 139–155.
- Suen (2026), cornerstone investors, pricing uncertainty and sentiment in
  new-economy HK listings, *Asia-Pacific Journal of Financial Studies*.
- HKEX consultation paper (Dec 2024) and conclusions (Aug 2025) on IPO price
  discovery and open market requirements: primary source for the reform's
  stated motivation and market statistics.
