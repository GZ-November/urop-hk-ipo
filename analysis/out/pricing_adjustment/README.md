# Price adjustment and retail information: 2026

Cutoff: 30 September 2026. Prepared: 4 October 2026.

| File | Purpose |
| --- | --- |
| issuer_sample.csv | All 113 issuers, price evidence classes and derived measures |
| source_audit.csv | 339 endpoint/quantity checks against stored extractions, with source provenance |
| group_statistics.csv | Price evidence and final-range-position descriptions |
| range_regressions.csv / range_coefficients.csv | All 28 focused common-sample estimates and full coefficients |
| range_sensitivity.csv | Quarter, large-winner and single-issuer exclusions |
| midpoint_identity.csv | Shared-price accounting check |
| margin_timing_audit.csv / margin_sample.csv | Publication timing decisions and selected 25-IPO sample |
| margin_regressions.csv / margin_coverage.csv | Demand associations and selected coverage |
| rolling_predictions.csv / rolling_summary.csv | Temporal training membership, predictions and errors |
| run_manifest.json | Input hashes, versions, limitations and report export provenance |

[Study specification](../../specifications/pricing_adjustment.md) ·
[English report](../../../docs/reports/HK_IPO_2026_PRICING_AND_RETAIL_INFORMATION.md).

Reproduce with `python run.py analysis --study pricing_adjustment` from the root.
Source consistency is not full source certification. Missing lower price bounds
are not zero revisions. Application measures are gross expectations, not account
returns. This is an exploratory study, with no causal or untouched-test claim.
