# Topic 1 — Step 2: date provenance and matched-anchor sensitivity

Prepared 4 October 2026. Cutoff: 30 September 2026. Working research note,
not a final report. No workbooks, extraction JSON or LaTeX report were changed.

## Evidence work completed

The existing 43 range-priced IPOs remain the research population for this step.
The current allotment download manifest contains publication times for 29 of
those IPOs. Earlier collection packets preserve the other 14 publication times
and official announcement URLs. Announcement metadata coverage is therefore
restored to 43/43 in the research ledger. The recovered entries retain their
packet paths and hashes. This is provenance recovery, not a fresh independent
verification of every HKEX timestamp.

The document search now covers the full text of all 29 locally available
prospectuses, all 43 allotment text files, and available greenshoe texts. It
produces 373 pricing-related candidate snippets, all from prospectuses. These
are candidates for semantic review, not verified actual dates. Fourteen local
prospectuses remain unavailable at the expected paths. One available prospectus
has a text-decoding warning, recorded in the ledger.

**No actual price-determination date is newly verified.** The full-text search
alone does not prove that dates are absent from all disclosures. No date is
imputed from the timetable, a deadline or announcement publication.

## Three distinctions checked directly

1. MiniMax (0100.HK): prospectus PDF page 2 describes 7 January 2026 as the
   expected pricing date. It does not establish the actual date of agreement.
2. Tongshifu (0664.HK): prospectus PDF page 2 states an expected date on or
   before 27 March 2026. A latest permissible date is not an execution record.
3. Manycore (0068.HK): the stored greenshoe text dates a stock-borrowing
   agreement to 15 April 2026. That is a different contract; it does not verify
   price determination, even though its date matches the pricing proxy.

Manycore's [official allotment announcement](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0416/2026041601684.pdf),
PDF page 3, reports the final offer price of HK$7.62 and range HK$6.72–HK$7.62.
This confirms the final-price outcome by publication; it does not say when the
price was agreed. The earlier collection packet records publication at
20:59 HKT on 16 April 2026.

A search-index prospectus link for Manycore returned HTTP 404 on retrieval.
Its search excerpt is not used to certify an actual date or amend source data.

## Market adjustment: distinguish date effects from sample effects

We retain the same revision variable, intercept, and Q2/Q3 controls within each
sample. The outcome is log offer-to-close return, adjusted by subtracting log
HSI return over the named window. HSI levels use the latest available trading
close on or before each date. Raw close return is always shown as a reference.

The publication-day window is an **information-release benchmark**. It is not
an actual-pricing or investor-holding window. Expected pricing dates remain
proxies. The uniform subscription-close window retains its original definition.

| Sample | Anchor | N | Mean return | Revision coefficient | HC3 t p |
| --- | --- | ---: | ---: | ---: | ---: |
| All range offers | Unadjusted close | 43 | 68.29% | 1.598 | 0.251 |
| All range offers | Subscription close | 43 | 68.85% | 1.554 | 0.267 |
| All range offers | Final-price publication day | 43 | 68.41% | 1.604 | 0.249 |
| Same proxy-available firms | Unadjusted close | 36 | 65.85% | 3.419 | 0.008 |
| Same proxy-available firms | Subscription close | 36 | 66.13% | 3.398 | 0.009 |
| Same proxy-available firms | Expected pricing proxy | 36 | 66.05% | 3.386 | 0.009 |
| Same proxy-available firms | Final-price publication day | 36 | 66.18% | 3.412 | 0.009 |

Coefficient units: log-return units per one unit of fractional revision. For
+10 percentage points of revision, the fitted log-return change is 0.1 times
the coefficient. This is not an increase of the same number of percentage
points in simple return. HC3 p-values are exploratory, without a new multiple-
test adjustment or restricted-sample wild-cluster validation. They do not
replace the main study's inference.

Within the same 36 firms, adjusted mean returns span only 66.05%–66.18%, and
coefficients span 3.386–3.412. The unadjusted coefficient is already 3.419.
Thus the apparent stronger association is mainly a **sample-restriction issue**,
not evidence that a better date anchor revealed the mechanism. Removing seven
firms changes the unadjusted coefficient from 1.598 to 3.419. Those seven firms
cannot be silently excluded from the headline claim.

The 43-firm result remains positive but uncertain across the two complete
market windows. Actual pricing-window sensitivity has not been tested because
actual dates are not certified.

## Implication and next research step

Keep the 43-firm close-return result as the principal pricing association.
Treat the 36-firm proxy comparison as a selected-sample sensitivity check.
Do not claim that market adjustment establishes partial adjustment or that a
publication date identifies the timing of bookbuilding news.

Next, diagnose why the seven missing-proxy firms change the revision coefficient:
inspect their revision, opening and close returns, leverage, and individual
influence on the common model. Use all 43 firms for the price-stage analysis.
Actual-date retrieval remains a separate evidence task, not a reason to select
a stronger result. This research topic is not yet ready for its final report.

## Reproduction and audit files

Run `python analysis/pricing_date_audit_2026.py` from the repository root.

- `step02_date_provenance.csv`: all 43 publication timestamps, their sources,
  date status and local document coverage; actual dates remain missing.
- `step02_date_candidates.csv`: 373 full-document candidates awaiting semantic review.
- `step02_market_anchor_panel.csv`: per-issuer index dates, points and returns.
- `step02_matched_anchor_comparison.csv`: all seven reported comparisons.
- `step02_missing_proxy_issuers.csv`: the seven excluded firms for diagnosis.
- `step02_manifest.json`: source hashes and scope limits.
