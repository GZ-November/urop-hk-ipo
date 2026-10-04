# Topic 1: pricing adjustment and first-day returns

Current-sample empirical assessment completed on 4 October 2026. Cutoff:
30 September 2026. Total population: 113 ordinary Main Board IPOs. Main price-
revision sample: 43 two-sided-range offers, across nine listing-month clusters.

[English report](../../../../docs/reports/HK_IPO_2026_PRICING_AND_RETAIL_INFORMATION.md),
[LaTeX source](../../../../docs/reports/HK_IPO_2026_PRICING_AND_RETAIL_INFORMATION.tex)
and [PDF](../../../../docs/reports/exported_pdfs/HK_IPO_2026_PRICING_AND_RETAIL_INFORMATION.pdf).
The legacy source filename is retained to keep the user's editor open. Its
contents cover Topic 1 only. Topics 2 and 3 are separate research projects.

## Results and limits

The positive revision-close association is stable in sign, uncertain in size,
and not supported by the maintained Holm-adjusted inference. Intraday evidence
is sensitive to the inference method. Date-anchor sensitivity is small relative
to missing-proxy sample selection. Maximum-only offers are mostly A+H, have only
four below-ceiling observations, and do not supply missing midpoint revisions.
The data do not identify a causal information-incorporation mechanism or prove
that prices were increased during bookbuilding.

## Reproduction

From the repository root, with the project environment:

```sh
.venv/bin/python analysis/pricing_topic1_completion_2026.py
.venv/bin/python analysis/pricing_topic1_report.py
.venv/bin/python -m pytest analysis/tests/test_pricing_topic1_completion.py -q
```

The completion script reads the frozen parent `issuer_sample.csv`, the
[lower-bound evidence ledger](../lower_bound_audit/issuer_evidence.csv), the
Step 2 date-provenance table, the parent baseline regression table and the
cached HSI bars. The report also reads the Step 4 robust-estimator output.
Reproduction of the final estimates and report requires no live network call.
The separate earlier step scripts can reproduce their respective diagnostics;
source searches require the official documents or the recorded caches.

The disclosure audit can be rerun with the audited official PDFs, using its
recorded URLs and hashes. PDF originals are not duplicated in this result folder.
Source JSON, workbooks and master exports are not written by this study.

## Output map

| File | Research purpose |
|---|---|
| `audited_issuer_panel.csv` | 113 firms; disclosure overlay; source measures preserved |
| `disclosure_groups.csv`, `range_descriptives.csv` | Sample composition and distributions |
| `stage_inference.csv` | All four declared control designs and four price-stage outcomes; HC3, CV3 and exact WCR |
| `primary_family_inference.csv` | Maintained seven-outcome family; both CV3 and WCR Holm results |
| `cluster_information.csv` | Month size, leverage and residual-regressor information share |
| `leave_one_month_out.csv` | Deterministic month exclusions across every primary design and stage |
| `range_geometry.csv` | Revision versus range position, conditional on width; eight-test Holm family |
| `asymmetry.csv` | Positive/negative revision slopes and difference; 12-test Holm family |
| `public_market_associations.csv` | Named market-window associations, not verified pre-agreement information |
| `anchor_sensitivity_panel.csv` | Candidate daily-index sets and per-firm outcome bounds |
| `anchor_slope_bounds.csv` | Sharp conditional coefficient bounds, independently verified by linear programming |
| `route_disclosure_overlap.csv` | Observed route overlap and within-route descriptions |
| `maximum_only_panel.csv`, `ceiling_groups.csv` | All 30 maximum-only firms, including every below-ceiling case |
| `revision_stage_groups.csv` | Above/below-midpoint price-stage descriptions |
| `key_counterexample_evidence.csv` | Fresh full-prospectus checks for 2672 and 3231 |
| `run_manifest.json` | Versions, input hashes, validation, report and PDF hashes |

CV3 is centered on the full-sample estimate. It is verified against an independent
block-residual sandwich. Three focused tests verify known statistical invariants
and rank-loss handling. Stage accounting, fixed sample membership, historical
coefficient agreement, geometry and linear-programming bounds pass. There is no
investment simulation and no random resampling. Exact WCR enumerates all 512
Rademacher signs; this does not make finite-sample inference exact in size.
