# Retail evidence assessment and exclusion results

3 October 2026 | Research price cutoff: 30 September 2026 | Scope: 2649, 3355 and 19 application-total corrections

## Reviewable summary

Corrected baseline: N=113, mean gross application return 2.08%, covariance contribution -3.65 pp, mean expected gross profit HK$91.77.

| Item | Verified | Still derived / unresolved | Exclusion N | Application return | Covariance (pp) |
| --- | --- | --- | --- | --- | --- |
| 2649 board lot / minimum application | Verified: both 500; original 200 corrected by issuer | None for lot size; original frozen lot metadata remains stale | 112 | 2.10% | -3.77 |
| 3355 ten Pool B guarantees | Verified: all ten match official 27 March clarification | Prior inference confirmed; Pool A 008% remains a transcription interpretation, unused in one-lot result | 112 | 2.10% | -3.71 |
| 19 valid-application quantity corrections | Verified: 763 PDF quantity/count pairs; exact sums match current master | Totals are sums; 14 old formulas reproduce, 2 have arithmetic errors, 9976 rounding compatible only, 2290/1392 cause unrecorded; 0 current formal totals stale | 94 | 2.48% | -4.06 |
| Joint exclusion of all flagged issuers | Conservative sensitivity; different sample composition | No causal interpretation of exclusion difference | 92 | 2.53% | -4.32 |

This is a scoped source reassessment and deterministic research sensitivity exercise. It creates no whole-payload pipeline gate approval, changes no workbook/master/frozen tier/review bytes, and does not certify all issuer fields. All 19 formal extraction totals have now been repaired and independently reviewed for col_CO; the old values are preserved in before snapshots. This is a scoped field review, not whole-payload writeback approval. The existing hash-bound tier gate is checked before use. A source-specific overlay changes only 2649's lot classification in the new draft; earlier generated results retain their historical definitions.

## 2649: resolved by official correction

The original 6 March allotment PDF physically prints a 200-share board lot on page 17 and starts applications at 500 shares on page 12. The prospectus specifies 500 on PDF pages 412 and 417 (printed pages 403 and 408). The issuer's [11 March clarification](https://www.hkexnews.hk/listedco/listconews/sehk/2026/0311/2026031100837_c.pdf), page 1, explicitly corrects 200 to 500. The [5 March HKSCC admission circular](https://www.hkex.com.hk/-/media/HKEX-Market/Services/Circulars-and-Notices/Participant-and-Members-Circulars/HKSCC/2026/ce_HKSCC_SKA_074_2026.pdf), page 1, independently records 500 before listing. Original and correction pages were visually inspected. Minimum application and corrected trading lot therefore both equal 500. There is no need to infer lot size from the minimum tier. The original announcement's typo explains the frozen 200-unit metadata.

The corrected 113-IPO one-lot results equal the former 113-IPO minimum-tier results in economics, but their label is now supported. The previous 112-IPO strict sample remains an exclusion sensitivity. No historical extraction approval was rewritten to authorize changed bytes.

## 3355: prior guarantee inference confirmed by direct disclosure

The original PDF page 16 omits Pool B guarantees from the ballot wording. The [27 March clarification](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0327/2026032702666.pdf), page 2, explicitly provides all ten guarantees and additional-ballot rules. Every application quantity, applicant count, guarantee, ballot numerator/denominator, extra quantity and printed percentage matches the frozen economic values. The guarantee vector is 100,100,100,200,200,200,200,200,200,300. The ten tiers have 11,492 applicants and allocate 2,000,000 shares, matching Pool B. This conclusion rests on the corrected PDF, rather than a totals-only proof. The original, prior inference and new official relation are preserved separately in [the ten-row comparison](../../pipeline/reports/data_gap_collection/source_followup_2026-10-03/3355_official_pool_b.csv).

The Pool A page-15 token `008%` was not addressed in that Pool B clarification. Its interpretation as 0.08% remains an arithmetic/transcription interpretation, not a newly obtained correction. This is the 90,000-share tier, whereas this draft uses the directly disclosed 100-share tier. The source ambiguity therefore does not enter the one-lot calculation; the issuer-wide exclusion is still shown.

## 19 corrected application totals

The quantity and applicant columns were re-read directly from the local PDF layout, using a separate reader from the frozen text parser. All 763 operand pairs match the frozen tiers one for one, with no omitted or duplicate pairs. The exact sum of quantity times applicants agrees with both current workbook values (resolved by header name) and the current master. Applicant totals also agree. Final allocation totals are reconciled using existing tier rules, with 1377's employee-reserved allocation separated; those 19 allocation rules were not independently re-reviewed in this exercise.

Sixteen old formal records explicitly document multiplication of the rounded subscription level by the initial public quantity. Fourteen reproduce the old value to within integer rounding. Two also contain arithmetic inconsistencies in their notes: 6880's stated operands multiply to 824,712,039.20, rather than 824,712,149; 6951's multiply to 2,337,132,385, rather than 2,337,131,310. These two differences must not be explained solely by rounding the disclosed subscription multiple. The new exact totals are supported by the PDF tier operands in all cases.

For 9976, 2,607,800 × 40.32 = 105,146,496, close to the old 105,146,500, but the old record does not document that procedure: rounding is a compatible explanation, not established historical provenance. For 2290 and 1392 the old totals are unsupported by the re-read tiers; the exact original error mechanism remains undocumented. Thus the earlier broad claim of '17 rounding reconstructions and two entry errors' is narrowed to **14 reproducible rounded-ratio reconstructions, two documented formulas with additional arithmetic discrepancies, one compatible explanation and two undocumented error mechanisms**.

| Code | Tiers | PDF pages | Old formal total | Verified sum / workbook / master | Change | Origin assessment |
| --- | --- | --- | --- | --- | --- | --- |
| 2290.HK | 42 | 7;8 | 6,362,250,000 | 8,311,550,000 | +1,949,300,000 | Earlier total unsupported; error mechanism unrecorded |
| 1392.HK | 40 | 13;14;15 | 84,572,151,000 | 61,158,791,500 | -23,413,359,500 | Earlier total unsupported; error mechanism unrecorded |
| 2335.HK | 38 | 11;12 | 6,859,084,176 | 6,859,076,200 | -7,976 | Rounded-ratio reconstruction documented |
| 6106.HK | 40 | 16;17 | 3,115,050,544 | 3,115,049,350 | -1,194 | Rounded-ratio reconstruction documented |
| 3952.HK | 37 | 14;15 | 3,072,834,479 | 3,072,837,300 | +2,821 | Rounded-ratio reconstruction documented |
| 2667.HK | 40 | 12;13 | 2,722,693,970 | 2,722,712,500 | +18,530 | Rounded-ratio reconstruction documented |
| 6880.HK | 45 | 23;24 | 824,712,149 | 824,707,040 | -5,109 | Formula documented; additional arithmetic mismatch |
| 7656.HK | 40 | 15;16 | 5,120,526,664 | 5,120,530,600 | +3,936 | Rounded-ratio reconstruction documented |
| 7687.HK | 40 | 24;25 | 412,415,224 | 412,411,450 | -3,774 | Rounded-ratio reconstruction documented |
| 9971.HK | 42 | 19;20 | 6,590,538,768 | 6,590,539,800 | +1,032 | Rounded-ratio reconstruction documented |
| 1377.HK | 37 | 18;19 | 403,190,216 | 403,185,300 | -4,916 | Rounded-ratio reconstruction documented |
| 1770.HK | 40 | 10;11 | 546,473,726 | 546,474,050 | +324 | Rounded-ratio reconstruction documented |
| 2475.HK | 45 | 22;23;24 | 144,952,794 | 144,959,900 | +7,106 | Rounded-ratio reconstruction documented |
| 2797.HK | 35 | 8;9 | 4,220,250,000 | 4,220,214,000 | -36,000 | Rounded-ratio reconstruction documented |
| 3752.HK | 42 | 14;15 | 360,635,056 | 360,637,200 | +2,144 | Rounded-ratio reconstruction documented |
| 6951.HK | 40 | 15;16;17 | 2,337,131,310 | 2,337,106,300 | -25,010 | Formula documented; additional arithmetic mismatch |
| 2249.HK | 40 | 15;16 | 7,441,765,142 | 7,441,779,600 | +14,458 | Rounded-ratio reconstruction documented |
| 6745.HK | 40 | 12;13 | 8,013,774,540 | 8,013,633,000 | -141,540 | Rounded-ratio reconstruction documented |
| 9976.HK | 40 | 20;21 | 105,146,500 | 105,156,600 | +10,100 | Compatible with rounding; cause unrecorded |

Every pre-repair formal `col_CO` value differs from the current workbook/master value. `col_CO` is the legacy extraction schema field; the physical workbook column is resolved by its `Public valid applied shares` header, not by Excel letter. All 19 formal extraction totals have now been repaired and independently reviewed for col_CO; the old values are preserved in before snapshots. This is a scoped field review, not whole-payload writeback approval. The [repair record](../../pipeline/reports/data_gap_collection/source_followup_2026-10-03/formal_json_repair/README.md) separates the field repair from whole-payload writeback credentials. This assessment does not fabricate whole-payload approval.

Per-issuer official URLs, source pages, notes and hashes are in [the correction ledger](../../pipeline/reports/data_gap_collection/source_followup_2026-10-03/nineteen_applied_totals.csv); the [763-row operands table](../../pipeline/reports/data_gap_collection/source_followup_2026-10-03/nineteen_pdf_operands.csv) makes every sum reproducible. These totals are source-verified derivations, not directly printed aggregate counts.

## Research disposition

| Sample | N | Mean application return | Covariance (pp) | Mean gross profit (HK$) |
| --- | --- | --- | --- | --- |
| Corrected one-lot baseline | 113 | 2.08% | -3.65 | 91.77 |
| Exclude 2649 (previous strict sample) | 112 | 2.10% | -3.77 | 92.59 |
| Exclude 3355 | 112 | 2.10% | -3.71 | 92.54 |
| Exclude 19 total corrections | 94 | 2.48% | -4.06 | 109.62 |
| Exclude all 21 flagged issuers | 92 | 2.53% | -4.32 | 111.95 |

Primary one-lot outcomes use tier-specific expected allocations and requested quantities. They do not use the aggregate valid-application total, so changing those totals has no direct arithmetic effect on one-lot profits. Excluding the 19 issuers is a conservative sample-composition sensitivity. All reported samples retain positive mean gross application returns and negative covariance contributions; monetary profits under a chosen fee can still differ. Exclusion differences do not identify an effect of data quality.

New computations are exact expectations using observed prices. No new simulation was run. The [mentor brief](RETAIL_MENTOR_BRIEF_2026-10-03.md) uses gross outcomes as its baseline and hypothetical fees only as sensitivity scenarios.
