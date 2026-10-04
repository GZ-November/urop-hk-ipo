# Topic 1 — Step 1: define revision and audit date evidence

Research status: in progress. Prepared 4 October 2026. Cutoff: 30 September 2026.
This is a working note, not a final report. Topics 2 and 3 are not combined here.

## Question for this step

Does a final offer price above the filed midpoint establish that the price was
raised during bookbuilding? Can the stored pricing date be used as an actual
price-determination date?

## Findings

The existing 113-IPO sample contains 43 offers with usable two-sided ranges.
Among those 43, 21 final prices are above the filed midpoint and 22 are below it.
None is exactly at the midpoint. Revision is final price / filed midpoint - 1.
It compares two price references. Without a dated earlier price proposal or
amendment, it does not establish a price increase during the subscription period.

| Final price vs midpoint | N | Mean revision | Mean offer-to-close | Mean offer-to-open | Median offer-to-close |
| --- | ---: | ---: | ---: | ---: | ---: |
| Above midpoint | 21 | 5.70% | 79.39% | 69.50% | 37.53% |
| Below midpoint | 22 | -7.15% | 57.69% | 58.94% | 28.80% |

These are descriptive groups, with no matching or causal identification. Large
first-day gains occur in both groups. That observation alone cannot explain why
prices changed, or show that the bookbuilding process failed to incorporate news.

Two direct prospectus checks show that a date currently recorded as a pricing
proxy is explicitly an expected date:

- **0100.HK, prospectus PDF page 2:** the Price Determination Date is expected
  to be on or around Wednesday, 7 January 2026. The timetable on PDF page 5 also
  labels it as expected. This does not verify when the price was actually agreed.
- **0664.HK, prospectus PDF page 2:** the Price Determination Date is expected
  to be on or before Friday, 27 March 2026. This is a planned timing statement,
  not a record of execution.

## Search coverage and limits

The step searches all 43 local allotment text files for explicit pricing-date
or pricing-agreement candidates. The specified keyword search finds no matches.
A no-hit result does not establish that a date is absent: alternative wording,
other announcements, text extraction problems and attachments may contain it.

Only 29 of the 43 prospectus PDFs are present at the expected local paths. The
script checks the first 15 PDF pages of those 29 for timetable candidates.
The other 14 are labelled unavailable locally, rather than treated as documents
that were checked. Full-document semantic review has not been completed.

The stored final-price/allotment download manifest supplies publication times
for 29 offers. Those publication times are not price-determination times. A
final-price announcement can establish that the price was known by publication,
but it does not prove that the price was agreed on the same date. The existing
panel has 36 recorded pricing proxies and seven missing proxies.

**No actual pricing date is newly certified in this step.** Original workbooks,
formal extraction JSON and the currently open LaTeX report remain unchanged.

## Implication for the next step

Use “final-price revision relative to the filed midpoint” for the current
measure. Reserve “price increase during bookbuilding” for a dated, documented
change. Keep expected dates, announcement dates and verified actual dates in
separate fields.

The next evidence step is issuer-level retrieval of actual price-agreement or
price-determination statements, starting with missing local prospectuses and
missing announcement metadata. Record source URL, PDF page, exact wording and
whether the date is expected, actual, a deadline or a publication date. Where
actual dates remain undisclosed, keep them missing; do not impute a date from
the prospectus timetable or announcement publication.

After that audit, compare actual-date market-adjusted returns with the existing
subscription-close benchmark on the same firms. Keep the close return as the
main outcome and use opening/intraday returns to locate the adjustment stages.
A report should follow completion of this topic's evidence and analysis steps.

## Files and reproduction

- `step01_pricing_date_evidence.csv`: source candidates, coverage, proxies,
  publication times, hashes and manual review status; all actual-date cells remain missing.
- `step01_revision_groups.csv`: reproducible group means and medians.
- Run `python analysis/pricing_date_evidence_2026.py` from the repository root.

These records are exploratory evidence notes, not formal pipeline writeback or
an independent review approval.
