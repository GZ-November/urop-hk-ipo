# Price adjustment and pre-deadline retail information

Prepared 4 October 2026. This extension is exploratory, not a preregistration.
The observation cutoff is 30 September 2026. No source workbook or extraction
record is rewritten by this study.

## Sample and measures

The frozen retail-return panel contains 113 ordinary Main Board IPOs listed in
2026. Current master offer prices and first-day closes must match that panel.
Price endpoints and initial global offering quantity are reconciled to 113 stored
prospectus extractions. Agreement verifies extraction consistency, not independent
semantic correctness. Missing lower endpoints remain missing. The classifications
are 43 two-sided ranges, 39 equal endpoints and 31 undisclosed lower endpoints.
Only the 43 range offers receive midpoint revision and range-position measures.

Revision is final price / filed midpoint - 1. All main models use the same 43
issuers and an intercept plus Q2 and Q3 indicators. Seven outcomes are log
close/offer, log open/offer, log close/open, allocation fraction, gross application
return, log HSI-adjusted close return, and raw close/offer return minus one.
Alternative designs use revision alone, launch size and A+H status, or launch size
and the prospectus-to-subscription-close HSI change. The latter is not a verified
actual price-determination window. Planned size uses the original filed global
quantity times the midpoint, or the ceiling outside the range sample.

Gross application return equals expected allocation fraction times price return.
The ceiling-principal measure is allocation fraction times (close - final price)
divided by the published maximum price. Both omit fees, levies and financing.
Neither is actual account performance or a complete cash commitment measure.

## Inference and sensitivity

HC3 standard errors use a t reference. Restricted wild cluster-t enumerates all
Rademacher sign vectors for the nine listing-month clusters. Holm adjustment
covers the seven main outcome tests. Few clusters and a small sample limit
inference; these results do not identify causal bookbuilding effects. Four
specifications and all coefficients are retained. Quarter exclusions, removal
of the three largest price-return or application-return winners, and every
single-issuer exclusion are retained. Log-stage coefficient identities are
accounting checks, not independent economic evidence.

## Demand timing and temporal exercise

Margin snapshots must be explicitly classified as published before the closing
day and have publication date strictly before subscription close. Later records
and unresolved closing-day publication times are excluded. The latest eligible
snapshot is selected per IPO. Broker-survey coverage is partial and selected.
The 25-IPO margin sample uses six month clusters, log margin multiple and planned
size; Holm covers its three controlled outcome tests. Six clusters give coarse
inference.

The temporal assessment predicts gross ceiling-principal return using only log
planned size and A+H status. Each training label must have a listing date strictly
before the target prospectus date. At least 40 prior IPOs are required. An
expanding mean is the benchmark. All 70 prediction rows retain training membership.
This previously explored sample is not an untouched holdout. Final prices, final
demand, final allocation and post-deadline grey-market prices are not predictors.

## Reproduction

Run `python run.py analysis --study pricing_adjustment`. Outputs are in
`analysis/out/pricing_adjustment/`; the report builder is
`analysis/pricing_adjustment_report.py`. Confirm native LaTeX compilation, export
the PDF to `docs/reports/exported_pdfs/`, and inspect every rendered page.
