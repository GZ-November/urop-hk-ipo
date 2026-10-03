# 2026 Data-Gap Collection and Evidence Ledger

Latest scoped [source follow-up](../../../docs/reports/RETAIL_EVIDENCE_ASSESSMENT_2026-10-03.md): 2649's official correction confirms a 500-share lot; 3355's official clarification confirms all ten Pool B guarantees; 763 PDF operand pairs support the 19 current workbook/master totals. Fourteen old rounded-ratio formulas reproduce, two have additional arithmetic discrepancies (6880/6951), one case is only compatible with rounding, and two error mechanisms are unrecorded. The [19 formal extraction totals are now repaired](source_followup_2026-10-03/formal_json_repair/README.md), with independent source review scoped to `col_CO`. Original JSON snapshots and frozen inputs/reviews are preserved; whole-payload gate approval has not been renewed. Earlier qualifications below describe the pre-follow-up baseline.

Population: 113 ordinary Main Board IPOs. Observation cutoff: 30 September 2026. This ledger records the existing data baseline and the subsequent read-time safeguards; it is not a new independent source review.

## Available artifacts

| Item | Coverage and status | Artifact |
|---|---|---|
| Trading-lot units | 113 issuers; 112 share-based and one HDR (6228) | [Board lots](board_lots.csv) |
| Allocation tiers | 4,582 rows across 113 issuers; all three stored totals currently reconcile | [Clean tiers](allocation_tiers_clean.csv), [reconciliation](allocation_tiers_reconciled.csv), [existing review](allocation_review.json) |
| Four added A+H references | 6727, 3228, 3757 and 9607; reference coverage 38/38 | [Added references](ah_four_added.csv), [complete references](../../exports/HKIPO-2026-AH-reference.csv) |
| 6872 prior-period revenue | FY2025 RMB0 formally recorded after the existing whole-payload repair/review | [Repair](6872_repair/README.md), [review](6872_repair/final_review.json) |
| 2553 prior-period profit | Latest selected period is 2026Q1; revenue/gross profit found, but same-period net profit not found. FY2025 loss cannot substitute | [Financial evidence](financial_vc_review.md) |
| Seven VC/PE flags | 0668, 2475, 6951, 6745, 3228, 3757 and 9607 remain unknown | [Issuer ledger](financial_vc_ledger.csv) |

## Tier definitions

`applied_shares` is the application quantity and `applicants` the number of valid applications in that tier. Quantity field names also apply to HDR records; read `board_lot_unit` and do not add HDR quantities to ordinary share quantities.

Expected allocation = guaranteed quantity + ballot winners/applicants * additional quantity. An additional-ballot probability is not the chance of receiving any allocation when a guarantee is positive. Trading-lot sizes come from their separate disclosure, not from the minimum application tier. In particular, the current 2649 record has a 200-security trading lot and a 500-security minimum application; this is a source follow-up and is excluded from the strict one-lot sample.

3636 and 0901 use disclosed success/failure count distributions, merged by application tier with original distributions retained. Unknown pool titles remain blank. Actual cross-page rules retain continuation-page metadata.

1377 ordinary-public allocation is 1,202,900 plus 60,300 employee-reserved securities; 2476 is 7,852,800 plus 482,000. Employees are separate from ordinary-public tiers. Current tier-based macro rates exclude these reserved quantities.

## Existing baseline corrections and qualifications

The preceding collection stage changed `Public valid applied shares` for 19 Q2/Q3 issuers using tier integer sums. Its ledger attributes 17 differences to rounding-based reconstruction and two (2290, 1392) to earlier entry errors. Current totals match, but this later reporting round did not independently re-establish those diagnoses or perform formal writeback.

For 3355, the stored guarantee vector [100,100,100,200,200,200,200,200,200,300] was inferred from rounded allocation percentages and pool totals, together with the reported number of successful Pool B applicants. The parser also changes a printed `008%` token to `0.08%`. Arithmetic reconciliation is a necessary check, not proof that inferred wording appeared in the source. The [original/derived appendix](../../../analysis/out/retail_distribution/3355_original_and_derived.json) separates the text from the inference, and the report includes an exclusion sensitivity.

The frozen candidate and coverage hashes currently match the existing review. No new semantic approval has been created during the subsequent research implementation.

## Remaining source questions

- 6727 retains `plausible=0` for its reference discount, pending an independent price source and corporate-action check. Four actual pricing dates are still missing; daily FX is not necessarily known at the pricing time.
- 2649's trading-lot/application-tier mismatch requires source follow-up.
- Seven VC/PE flags remain unknown. Director biographies, employee platforms, cornerstone participation and target sellers are not interchangeable with pre-IPO VC ownership.
- The 6872 whole-payload repair has an existing final review; its earlier rejected snapshot remains historical evidence. Necessary missing fields were retained.

## Re-extraction and review safeguards

`python analysis/allocation_tiers_2026.py` now creates candidates and coverage only. It does not write a clean table, assign a passing semantic review, or change workbooks. Changed candidate or coverage bytes invalidate the old approval for analysis use.

The analysis reader checks the independent review's verdict/scope, candidate and coverage hashes, source-text hashes, and clean/candidate field correspondence. This prevents stale approval from being carried into future reruns. The [English empirical report](../../../docs/reports/EMPIRICAL_RESEARCH_REPORT_2026.md) and [implementation notes](../../../docs/reports/RETAIL_RESEARCH_IMPLEMENTATION_2026-10-03.md) document the current study.

Source URLs are cataloged in [the source index](allocation_source_index.csv). Existing review JSON and original data remain unchanged by this English documentation update.
