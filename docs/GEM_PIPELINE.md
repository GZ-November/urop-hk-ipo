# GEM pipeline and template design

The GEM pipeline follows the existing IPO research framework while using its own official reports, source layout, template, evidence schema and output directories. Main Board-only concepts are physically deleted from both the GEM research view and its canonical data sheet.

## Workbook and data structure

- `HKIPO-GEM-template-students.xlsx` retains the original 46 fields and historical records. Only nonpopulated formatting beyond column AT is removed.
- `HKIPO-GEM-template-final.xlsx` is the clean blank collection template. It contains no historical companies.
- `GEM` is the first user-facing sheet. Its first 46 fields match the original template, followed by applicable shared research fields and GEM extensions.
- `NLR` contains the common evidence/market fields required by the existing deterministic tools. It has 195 fields, with seven Main Board-only concepts removed.
- `GEM_details` contains 15 independently extracted GEM-specific fields, identity keys and official-report/prospectus-date provenance.

The user-facing GEM sheet is refreshed from the authoritative source sheets at writeback/export and in delivery copies. It is a generated view: collect or correct evidence through the source gates. Direct edits to the view are overwritten on refresh. The 69-field GEM prospectus schema excludes technology commercialization stage; allotment retains its 18-field contract and GEM-specific extensions have a separate 15-field contract.

## Deleted Main Board-only fields

- 2025 pricing reform regime
- Chapter 18A flag
- Chapter 18C flag
- Technology commercialization stage
- WVR flag
- Controlling shareholder 6-month disposal lockup expiry date
- Controlling shareholder 12-month cessation of control expiry date

The Main Board template and datasets retain these fields. GEM does not infer them as zeros. Future return windows and legitimate issuer-dependent concepts remain available when applicable.

## Original 46-field mapping

| Original GEM column | Original field | Canonical source / interpretation |
|---|---|---|
| A | Listing Date | Date of Listing (dd/mm/yy) |
| B | Stock Code | Stock Code |
| C | Company | Company Name at time of listing (exclude Chapter 20 cases) |
| D | Offer Price (HK$) |  IPO Subscription Price (HK$) |
| E | Subscription ratio (times) | Subscription Ratio (times) |
| F | Funds raised (HK$) | Official GEM gross funds raised, retained as a total; no invented public/placing split. |
| G | No. of outstanding shares at listing | Official GEM outstanding shares at listing; may refer to the listed class. Preserve separately from total company share capital. |
| H | MC at listing (HK$) | Official GEM market capitalisation, retained with its reported share-class denominator. |
| I | Business activity | Principal business / industry |
| J | Place of incorporation | Place of incorporation |
| K | Listing method | Listing route / applicable chapter |
| L | Sponsors | Sponsor(s) |
| M | Reporting accountant | Reporting Accountants |
| N | Total (without option) | Total (without option) |
| O | Global Offering (without option) | Global Offering (without option) |
| P | Number of offer shares under the capitalization Issue | Number of offer shares under the capitalization Issue |
| Q | Number of offer shares under Capitalization Rest | Number of offer shares under Capitalization Rest |
| R | Sale Shares | Sale Shares |
| S | New shares  | New shares  |
| T | Placing Shares | Placing Shares |
| U | Public Offer shares | Public Offer shares |
| V | Maximum Offer Price | Maximum Offer Price |
| W | Minimum Offer Price | Minimum Offer Price |
| X | currency in financial information | currency in financial information |
| Y | total assets in year-3 | total assets in year-3 (3 years before IPO) |
| Z | total assets in year-2 | total assets in year-2 |
| AA | total assets in year-1 | total assets in year-1 |
| AB | total equity in year-3 | total equity in year-3 |
| AC | total equity in year-2 | total equity in year-2 |
| AD | total equity in year-1 | total equity in year-1 |
| AE | total liability in year-3 | total liability in year-3 |
| AF | total liability in year-2 | total liability in year-2 |
| AG | total liability in year-1 | total liability in year-1 |
| AH | Net sales in year-3 | Net sales in year-3 |
| AI | Net sales in year-2 | Net sales in year-2 |
| AJ | Net sales in year-1 | Net sales in year-1 |
| AK | Profit before tax in year-3 | Profit before tax in year-3 |
| AL | Profit before tax in year-2 | Profit before tax in year-2 |
| AM | Profit before tax in year-1 | Profit before tax in year-1 |
| AN | Profit for the year in year-3 | Profit for the year in year-3 |
| AO | Profit for the year in year-2 | Profit for the year in year-2 |
| AP | Profit for the year in year-1 | Profit for the year in year-1 |
| AQ | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) |
| AR | Underwriting Commission (%) | A single disclosed common/nonzero commission rate when tranche rates agree or only one is present. Unequal nonzero tranche rates remain NA; both separate tranche rates are retained in added columns. |
| AS | Over-allotment Option | Over-allotment Option (%) |
| AT | Company Chinese Name | Company Chinese Name |

## GEM-specific additions

| Field | Type and source interpretation |
|---|---|
| GEM eligibility rule / disclosed route | text: Issuer-stated dated GEM admission route; record rule and applicable waiver. |
| GEM disclosed trading record (years) | number: Number of financial years covered by the disclosed eligibility trading record. |
| GEM eligibility aggregate operating cash flow | number: Disclosed aggregate cash flow used for eligibility, in base financial-reporting currency units; retain applicable adjustments. |
| GEM eligibility cash flow currency | text: Currency of the aggregate operating cash-flow measure. |
| GEM eligibility cash flow period start | date: Beginning of the eligibility cash-flow measurement period. |
| GEM eligibility cash flow period end | date: End of the eligibility cash-flow measurement period. |
| GEM eligibility R&D / operating expenditure ratio | number: Disclosed ratio under an applicable alternative route; not inferred for standard cash-flow route. |
| GEM disclosed minimum market cap (HK$) | number: Applicable minimum stated by issuer, with dated rule/route/waiver evidence; not a hardcoded universal threshold. |
| GEM disclosed minimum public float (%) | number: Disclosed issuer-specific minimum public float, stored as a decimal fraction. |
| GEM public float waiver / exemption | text: Disclosed waiver terms; NA where unsupported. A missing waiver is not proof of none. |
| GEM disclosed controller lockup (months) | number: Initial no-disposal period in months, retain later retain-control restriction in quote/review note. |
| GEM compliance adviser | text: Full name of appointed compliance adviser. |
| GEM compliance adviser appointment end | date: End date only when explicitly disclosed, otherwise NA. |
| GEM offering structure | text: Public offer / placing / combined offering, from the listing document. |
| GEM board lot (shares) | integer: Disclosed trading board-lot shares; distinguish shares and any other quoted units. |

## Applicability decisions

GEM can have a shorter disclosed financial record than a Main Board issuer. Use only the actual accounts and periods. Keep unsupported third-year cells missing. A public offer, cornerstone investment, greenshoe, price stabilization, A+H structure or VC/PE backing is issuer-dependent, so those concepts are not removed solely because they are uncommon on GEM. A placing-only offering needs disclosed absence/zero of a public tranche; missing evidence alone is not a zero.

The shared 90-day IPO count is renamed to the GEM-specific count and uses GEM reports. Main Board counts are not silently relabeled as GEM counts.

The GEM collector does not infer Main Board Mechanism A/B or Chapter 18A/18C admission checks. It skips Main Board offering-rule inference and the automatic six-month cornerstone-unlock calculation. GEM unlocks need actual contractual evidence. The Main Board advanced `expansion` writer is explicitly unavailable for GEM until its event adapter is implemented; it returns an explanatory error rather than inferring Main Board lockup dates. Common market horizons and academic fields remain supported.

## Official sources and date coverage

- [HKEX GEM new-listing information and annual reports](https://www2.hkexnews.hk/New-Listings/New-Listing-Information/GEM?sc_lang=en).
- [HKEX GEM rules and dated amendments](https://en-rules.hkex.com.hk/entiresection/91).
- [2025 price discovery/open-market conclusions](https://www.hkex.com.hk/News/Regulatory-Announcements/2025/2508012news?sc_lang=en).
- [Ongoing public-float changes announced in December 2025](https://www.hkex.com.hk/News/Regulatory-Announcements/2025/251217news?sc_lang=en).

The annual GEM report is not the Main Board NLR layout. The parser reads listing date A, code B, company C, offer price F, subscription ratio H, total gross funds J, reported outstanding shares K, reported market cap M, industry O, incorporation Q, listing method R, sponsors T and accountant V. Continuation rows do not create duplicate issuers. The report has no prospectus-date column; document discovery supplies HKEX publication date with a separate provenance record.

Reported subscription ratio and industry remain source candidates; they are not copied into reviewed disclosure fields merely to pass an audit. Report date coverage is explicit. An archived sparse historical GEM annual report can print its last IPO date rather than 31 December. A current-year report ending before the requested interval does not establish complete coverage. A report filename, observation count or passing code check is not a substitute for original-source evidence.

## Collection and delivery

Use `collect --board gem --period-start YYYY-MM-DD --period-end YYYY-MM-DD` and the generated cohort config. Follow portable handoff work orders for prospectus, allotment and GEM extensions. All three targets need independent current review before collect writeback. The base configuration `gem_base.yaml` is a generation recipe; `config_gem_2026q1.yaml` is the initial official-source-only canonical cohort, explicitly awaiting extraction/review.

GEM exports live in `pipeline/exports/GEM/` and `pipeline/codebooks/GEM/`. They do not enter `HKIPO-MB-MASTER_clean.csv` or the existing Main Board 2026 studies. A bundle contains both the common clean CSV and the GEM research view/extensions; use stock code and listing date to join cohorts and board labels to prevent accidental sample mixing.

See [complete English instructions](AGENT_INSTRUCTIONS.md) for installation, copyable prompts, exit codes, review, resume, maturity and ZIP delivery.
