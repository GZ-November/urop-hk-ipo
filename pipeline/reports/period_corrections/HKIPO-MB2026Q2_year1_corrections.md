# 2026Q2 Main Board: year-1 re-anchored to the audited Track Record

Same standard as `HKIPO-MB2026Q3_year1_corrections.md`: year-1 is the latest period of the audited
Accountants' Report / "Track Record Period" definition; unaudited figures outside it are never year-1;
only sales, profit before tax and profit for the period are annualised (BC = months/12, originals in CN/CO/CP).

The 45 prospectuses were downloaded from HKEXnews for this check (user approval, 2026-10-14) so that every
issuer could be resolved against its own Track Record definition; previously only section slices were local.

## What changed

| Group | Issuers | Before → after |
|---|---|---|
| Unaudited Q1 2026 used as year-1; Track Record = FY2023–FY2025 | 1688, 2553, 3661, 6067, 9630 | year-1 3M Mar-26 (×4) → FY2025 (not annualised) |
| Correct 8M stub (FY ends 31 March), derived columns were stale | 2290 | BC 1 → 8/12, CI–CP re-derived |

The other 39 issuers already matched their Track Record (all full years ending 31 Dec 2025); their rows are unchanged.

For the 5 re-anchored issuers the 27 period-dependent payload fields were re-extracted from the prospectus
(other fields untouched), validated (period-anchor gate included), recorded `extracted`, and independently
reviewed against the original pages; reports bound to each payload sha256 are in
`prospectus_pipeline/out/period_reviews/2026Q2/`. Only reviewed payloads were written back, then
`disclosure_notes` (all 45 on the Track Record basis), `audit` (3150/3150), `cross_check` (5 pre-existing
allocation warnings, unchanged), `export` and `master --derive` were rerun. 2026Q2 `validate`: 45/45, 0 errors,
gate PASS.

Notes from the reviews: 2553's col_AX is the FY2025 "development expenditure" addition (1,088k); its previous
payload had most year-1 fields NaN. col_CG keeps each issuer's previously reviewed capex basis.

## Pending

None in 2026Q2.

## Every changed cell (before → after)

### 2553.HK (36 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 2560572000 | 2680513000 |
| AA | total assets in year-2 | 2504777000 | 2560572000 |
| AB | total assets in year-1 | NaN | 2504777000 |
| AC | total equity in year-3 | 933532000 | 1179100000 |
| AD | total equity in year-2 | 608618000 | 933532000 |
| AE | total equity in year-1 | NaN | 608618000 |
| AF | total liability in year-3 | 1627040000 | 1501413000 |
| AG | total liability in year-2 | 1896159000 | 1627040000 |
| AH | total liability in year-1 | NaN | 1896159000 |
| AI | Net sales in year-3 | 563611000 | 592551000 |
| AJ | Net sales in year-2 | 521698000 | 563611000 |
| AK | Net sales in year-1 | 637600000 | 521698000 |
| AL | Profit before tax in year-3 | -245065000 | -109393000 |
| AM | Profit before tax in year-2 | -324871000 | -245065000 |
| AN | Profit before tax in year-1 | NaN | -324871000 |
| AO | Profit for the year in year-3 | -245568000 | -110147000 |
| AP | Profit for the year in year-2 | -324914000 | -245568000 |
| AQ | Profit for the year in year-1 | NaN | -324914000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2026-03-31 | 2025-12-31 |
| AX | Operating cash flow in year-1 (before annualizat | NaN | 86969000 |
| AY | Cash and cash equivalents at year-1 end | NaN | 68741000 |
| AZ | R&D expensed in year-1 (before annualization) | NaN | 42455000 |
| BA | Development costs capitalized in year-1 (additio | 0 | 1088000 |
| BB | Top 5 customers (% of year-1 revenue) | NaN | 0.838 |
| BR | Interest-bearing debt at year-1 end | NaN | 1080796000 |
| CG | Financial statement unit multiplier |  | 1000 |
| CI | Year-3 financial period start | 2023-04-01 | 2023-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2023-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2024-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2024-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2025-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 637600000 | 521698000 |
| CO | Year-1 profit before tax (original) |  | -324871000 |
| CP | Year-1 profit for period (original) |  | -324914000 |
| CT | Gross profit in year-1 | -7600000 | -127652000 |
| CU | Capital expenditure in year-1 | NaN | 219832000 |

### 2290.HK (9 cells)

| col | header | before | after |
|---|---|---|---|
| BC | Comments (nearest sales& profit adjustment facto | 1 | 0.666667 |
| CI | Year-3 financial period start | 2022-12-01 | 2023-04-01 |
| CJ | Year-3 financial period end | 2023-11-30 | 2024-03-31 |
| CK | Year-2 financial period start | 2023-12-01 | 2024-04-01 |
| CL | Year-2 financial period end | 2024-11-30 | 2025-03-31 |
| CM | Year-1 financial period start | 2024-12-01 | 2025-04-01 |
| CN | Year-1 net sales (original, pre-annualization) | 3052702500 | 2035135000 |
| CO | Year-1 profit before tax (original) | 268146000 | 178764000 |
| CP | Year-1 profit for period (original) | 222574500 | 148383000 |

### 6067.HK (35 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 23145535000 | 17945462000 |
| AA | total assets in year-2 | 24793110000 | 23145535000 |
| AB | total assets in year-1 | 25938288000 | 24793110000 |
| AC | total equity in year-3 | 9971122000 | 9958777000 |
| AD | total equity in year-2 | 10140752000 | 9971122000 |
| AE | total equity in year-1 | 10025981000 | 10140752000 |
| AF | total liability in year-3 | 13174413000 | 7986685000 |
| AG | total liability in year-2 | 14652358000 | 13174413000 |
| AH | total liability in year-1 | 15912307000 | 14652358000 |
| AI | Net sales in year-3 | 3506153000 | 2981863000 |
| AJ | Net sales in year-2 | 4076845000 | 3506153000 |
| AK | Net sales in year-1 | 4285348000 | 4076845000 |
| AL | Profit before tax in year-3 | 407019000 | 717048000 |
| AM | Profit before tax in year-2 | 120463000 | 407019000 |
| AN | Profit before tax in year-1 | 71404000 | 120463000 |
| AO | Profit for the year in year-3 | 370708000 | 593695000 |
| AP | Profit for the year in year-2 | 143110000 | 370708000 |
| AQ | Profit for the year in year-1 | 82568000 | 143110000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2026-03-31 | 2025-12-31 |
| AX | Operating cash flow in year-1 (before annualizat | 68026000 | 752512000 |
| AY | Cash and cash equivalents at year-1 end | 2259139000 | 1187671000 |
| AZ | R&D expensed in year-1 (before annualization) | 69261000 | 278380000 |
| BB | Top 5 customers (% of year-1 revenue) | 0.5001 | 0.608 |
| BR | Interest-bearing debt at year-1 end | 13810684000 | 12415603000 |
| CG | Financial statement unit multiplier |  | 1000 |
| CI | Year-3 financial period start | 2023-04-01 | 2023-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2023-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2024-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2024-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2025-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 4285348000 | 4076845000 |
| CO | Year-1 profit before tax (original) | 71404000 | 120463000 |
| CP | Year-1 profit for period (original) | 82568000 | 143110000 |
| CT | Gross profit in year-1 | 269554000 | 883205000 |
| CU | Capital expenditure in year-1 | 348200000 | 3737322000 |

### 1688.HK (34 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 45193486000 | 37367171000 |
| AA | total assets in year-2 | 57900450000 | 45193486000 |
| AB | total assets in year-1 | NaN | 57900450000 |
| AC | total equity in year-3 | 19848981000 | 18280693000 |
| AD | total equity in year-2 | 24357948000 | 19848981000 |
| AE | total equity in year-1 | NaN | 24357948000 |
| AF | total liability in year-3 | 25344505000 | 19086478000 |
| AG | total liability in year-2 | 33542502000 | 25344505000 |
| AH | total liability in year-1 | NaN | 33542502000 |
| AI | Net sales in year-3 | 44259533000 | 34154017000 |
| AJ | Net sales in year-2 | 51428944000 | 44259533000 |
| AK | Net sales in year-1 | 50571864000 | 51428944000 |
| AL | Profit before tax in year-3 | 2196375000 | 2488042000 |
| AM | Profit before tax in year-2 | 2733377000 | 2196375000 |
| AN | Profit before tax in year-1 | 1720436000 | 2733377000 |
| AO | Profit for the year in year-3 | 1760733000 | 2013899000 |
| AP | Profit for the year in year-2 | 2326825000 | 1760733000 |
| AQ | Profit for the year in year-1 | 1603224000 | 2326825000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2026-03-31 | 2025-12-31 |
| AX | Operating cash flow in year-1 (before annualizat | NaN | 4432802000 |
| AY | Cash and cash equivalents at year-1 end | NaN | 5447511000 |
| AZ | R&D expensed in year-1 (before annualization) | 688637000 | 2381587000 |
| BB | Top 5 customers (% of year-1 revenue) | NaN | 0.575 |
| CG | Financial statement unit multiplier |  | 1000 |
| CI | Year-3 financial period start | 2023-04-01 | 2023-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2023-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2024-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2024-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2025-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 50571864000 | 51428944000 |
| CO | Year-1 profit before tax (original) | 1720436000 | 2733377000 |
| CP | Year-1 profit for period (original) | 1603224000 | 2326825000 |
| CT | Gross profit in year-1 | 1852431000 | 7818407000 |
| CU | Capital expenditure in year-1 | NaN | 4833121000 |

### 3661.HK (34 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 5771119000 | 4706852000 |
| AA | total assets in year-2 | 6954150000 | 5771119000 |
| AB | total assets in year-1 | 7187023000 | 6954150000 |
| AC | total equity in year-3 | 4599260000 | 3843824000 |
| AD | total equity in year-2 | 5327106000 | 4599260000 |
| AE | total equity in year-1 | 5501334000 | 5327106000 |
| AF | total liability in year-3 | 1171859000 | 863028000 |
| AG | total liability in year-2 | 1627044000 | 1171859000 |
| AH | total liability in year-1 | 1685689000 | 1627044000 |
| AI | Net sales in year-3 | 3346983000 | 2615716000 |
| AJ | Net sales in year-2 | 3898055000 | 3346983000 |
| AK | Net sales in year-1 | 4392524000 | 3898055000 |
| AL | Profit before tax in year-3 | 484783000 | 254139000 |
| AM | Profit before tax in year-2 | 549890000 | 484783000 |
| AN | Profit before tax in year-1 | 497784000 | 549890000 |
| AO | Profit for the year in year-3 | 491162000 | 269937000 |
| AP | Profit for the year in year-2 | 534375000 | 491162000 |
| AQ | Profit for the year in year-1 | 491072000 | 534375000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2026-03-31 | 2025-12-31 |
| AX | Operating cash flow in year-1 (before annualizat | 45441000 | 434379000 |
| AY | Cash and cash equivalents at year-1 end | 1183697000 | 1181028000 |
| AZ | R&D expensed in year-1 (before annualization) | 293594000 | 1045195000 |
| BB | Top 5 customers (% of year-1 revenue) | NaN | 0.331 |
| BR | Interest-bearing debt at year-1 end | 565123000 | 417420000 |
| CI | Year-3 financial period start | 2023-04-01 | 2023-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2023-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2024-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2024-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2025-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 4392524000 | 3898055000 |
| CO | Year-1 profit before tax (original) | 497784000 | 549890000 |
| CP | Year-1 profit for period (original) | 491072000 | 534375000 |
| CT | Gross profit in year-1 | 497802000 | 1802462000 |
| CU | Capital expenditure in year-1 | 96542000 | 232643000 |

### 9630.HK (35 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 2788843000 | 2480472000 |
| AA | total assets in year-2 | 3116656000 | 2788843000 |
| AB | total assets in year-1 | 3412358000 | 3116656000 |
| AC | total equity in year-3 | 2062602000 | 2031690000 |
| AD | total equity in year-2 | 2308372000 | 2062602000 |
| AE | total equity in year-1 | 2418880000 | 2308372000 |
| AF | total liability in year-3 | 726241000 | 448782000 |
| AG | total liability in year-2 | 808284000 | 726241000 |
| AH | total liability in year-1 | 993478000 | 808284000 |
| AI | Net sales in year-3 | 953943000 | 828855000 |
| AJ | Net sales in year-2 | 1408121000 | 953943000 |
| AK | Net sales in year-1 | 2058888000 | 1408121000 |
| AL | Profit before tax in year-3 | 171068000 | 195031000 |
| AM | Profit before tax in year-2 | 329717000 | 171068000 |
| AN | Profit before tax in year-1 | 491840000 | 329717000 |
| AO | Profit for the year in year-3 | 160695000 | 179305000 |
| AP | Profit for the year in year-2 | 289932000 | 160695000 |
| AQ | Profit for the year in year-1 | 433572000 | 289932000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2026-03-31 | 2025-12-31 |
| AX | Operating cash flow in year-1 (before annualizat | 164561000 | 91864000 |
| AY | Cash and cash equivalents at year-1 end | 529150000 | 442714000 |
| AZ | R&D expensed in year-1 (before annualization) | 36023000 | 131234000 |
| BB | Top 5 customers (% of year-1 revenue) | NaN | 0.416 |
| BR | Interest-bearing debt at year-1 end | 5849000 | 10526000 |
| CG | Financial statement unit multiplier | 1000000 | 1000 |
| CI | Year-3 financial period start | 2023-04-01 | 2023-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2023-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2024-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2024-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2025-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 2058888000 | 1408121000 |
| CO | Year-1 profit before tax (original) | 491840000 | 329717000 |
| CP | Year-1 profit for period (original) | 433572000 | 289932000 |
| CT | Gross profit in year-1 | 207206000 | 550958000 |
| CU | Capital expenditure in year-1 | 29041000 | 85299000 |

