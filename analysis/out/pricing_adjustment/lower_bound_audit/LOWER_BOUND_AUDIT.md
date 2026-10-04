# Offer-price lower-bound audit: 2026 Hong Kong IPOs

Audit date: 4 October 2026. Scope: the 31 issuers labelled `undisclosed_lower_bound` in the frozen 113-issuer pricing research input. This is an evidence note, not a completed topic report.

## Finding

Thirty issuers explicitly use maximum-only offer-price disclosure. One issuer, Medcaptain Medical Technology (2041.HK), states a single offer price of HK$15.42. No numerical lower endpoint of a two-sided offer-price range was recovered. No issuer remains unresolved in this 31-issuer audit.

The earlier blanket description of all 31 issuers as having an undisclosed lower bound was too broad. It combined maximum-only disclosure with one single-price offer. A blank extraction field alone could not support that description.

| Finding | Issuers | Treatment in the midpoint-revision study |
|---|---:|---|
| Confirmed maximum-only disclosure | 30 | Exclude from the range-midpoint revision measure; keep in other studies with usable variables. |
| Confirmed single stated price: 2041.HK | 1 | Classify separately; no two-sided range midpoint. |
| Numerical lower endpoint recovered | 0 | No addition to the two-sided-range sample. |
| Unresolved source or meaning | 0 | None in this audit. |

## Evidence and scope

[Issuer evidence ledger](issuer_evidence.csv) contains all 31 codes, short source excerpts, official HKEX URLs, PDF page numbers, printed page numbers where available, document lengths and SHA-256 hashes. [Audit manifest](audit_manifest.json) records the input and audit script hashes and the count checks.

All 31 complete prospectuses were searched. Review focused on the front-page offer-price terms and the waiver or pricing sections. Historical A-share price ranges, possible adverse effects of setting a lower offer price, and minimum application payments are not IPO offer-price lower endpoints. A waiver application was not treated as evidence that the waiver had been granted: the conclusion concerns the stated price-disclosure method.

Twenty-three complete documents were already in the pipeline cache. Eight were retrieved from official HKEX URLs. For SG Micro (3661.HK), the indexed English document was only a three-page extract; it was not treated as a full prospectus. The full 519-page official Chinese prospectus was reviewed instead. Its PDF page 83 (printed page 75) states maximum-only disclosure. The ledger preserves the short original Chinese excerpt and an explicitly labelled English interpretation.

Medcaptain's prospectus states a single price on PDF page 2. The pricing section corroborates it on PDF page 293 (printed page 285). The terms allow a reduction through a later announcement. This is not evidence of a missing numerical lower bound. A single quoted price also does not establish that the final price remained unchanged; that requires a separate comparison with dated subsequent disclosures.

## Effect on research

After this classification review, the 113 issuers comprise 43 with two-sided ranges, 39 with equal recorded endpoints, one additional single-price offer, and 30 with confirmed maximum-only disclosure. The 39 equal-endpoint records were not re-audited here.

The two-sided-range regression sample therefore remains **43**. The audit does not enlarge it to 74 or 113. It improves the reason for exclusion. Opening, closing, application-return and market-adjusted-return analyses can still use these issuers when their required inputs exist. They should not receive an invented lower bound or a zero midpoint revision.

For maximum-only offers, a separate ceiling-based measure, final offer price divided by the prospectus maximum minus one, can describe pricing below the ceiling. It is not interchangeable with revision from a range midpoint. Compare it in a separate specification, and distinguish changes in definitions from changes in issuer samples.

The 30 maximum-only issuers can also be used to examine the relation between price-disclosure format, listing route, demand and first-day returns. Such comparisons are descriptive unless the design accounts for issuer selection and other differences. This audit alone does not identify a causal effect of the disclosure format.

## Source-data status and reproduction

No extraction JSON, workbook, master panel, frozen regression output or LaTeX report was changed. The ledger is the research classification overlay. In the existing 2041 extraction, `col_T` already contains HK$15.42 and its price excerpt; `col_U` is blank. Treat the case as a single quoted price in subsequent research classification. Formal field conventions and any source writeback require their own semantic review.

Run from the repository root:

```sh
python3 analysis/pricing_lower_bound_audit_2026.py --supplemental-dir /path/to/retrieved/official/pdfs
```

The supplemental directory needs the eight PDFs identified in the script: files named by stock code, with the full Chinese SG Micro document named `3661_full_zh.pdf`. URLs and hashes in the ledger identify the reviewed versions. Downloads were held in a temporary research cache to avoid adding duplicate large PDFs to the repository.
