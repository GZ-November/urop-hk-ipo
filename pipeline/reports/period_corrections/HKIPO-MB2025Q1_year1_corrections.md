# 2025Q1 Main Board: year-1 re-anchored to the audited Track Record

Same standard as `HKIPO-MB2026Q2_year1_corrections.md` and `HKIPO-MB2026Q3_year1_corrections.md`:
year-1 is the latest period of the audited Accountants' Report / "Track Record Period" definition;
unaudited figures outside it are never year-1; only sales, profit before tax and profit for the period
are annualised (BC = months/12, originals in CN/CO/CP).

## What changed

| Group | Issuers | Before → after |
|---|---|---|
| 6M2024 audited stub period omitted in initial extraction; re-anchored to 30/06/2024 (×2.0) | 2613.HK, 0325.HK, 0805.HK, 2571.HK | year-1 FY2023 (not annualised) → 6M2024 stub (×2.0 annualised for AH/AK/AN) |
| 9M2024 audited stub period omitted in initial extraction; re-anchored to 30/09/2024 (×1.3333) | 1364.HK, 2097.HK, 2610.HK, 2569.HK, 2625.HK | year-1 FY2023 (not annualised) → 9M2024 stub (×1.3333 annualised for AH/AK/AN) |
| Audited stub already in payload, derived disclosure notes columns updated | 6681.HK, 2560.HK, 2530.HK, 2596.HK, 6693.HK, 2561.HK | Derived columns BC (months/12) and CI–CP re-derived by `disclosure_notes` |

For the 9 re-anchored issuers, the 27 period-dependent payload fields were re-extracted from the prospectus
(other fields untouched), validated (period-anchor gate included), recorded `extracted`, and independently
reviewed against original disclosure pages; reports bound to each payload sha256 are in
`pipeline/prospectus_pipeline/out/period_reviews/2025Q1/`. Reviewed payloads were written back to the workbook,
followed by `disclosure_notes` (all 15 on the Track Record basis), `audit` (1050/1050 perfect match), `cross_check`
(15/15 clean), `export` and `master --derive`. 2025Q1 `validate`: 15/15 target, 0 errors, gate PASS.

## Pending

None in 2025Q1.

## Every changed cell (before → after)

### 0325.HK - Bloks Group Limited (24 cells)

| col | header | before | after |
|---|---|---|---|
| AB | total assets in year-1 | NaN | 1125533000 |
| AE | total equity in year-1 | NaN | -1492462000 |
| AH | total liability in year-1 | NaN | 2617995000 |
| AK | Net sales in year-1 | 2172400000 | 2092406000 |
| AN | Profit before tax in year-1 | NaN | -405512000 |
| AQ | Profit for the year in year-1 | NaN | -509782000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2024-09-30 | 2024-06-30 |
| AX | Operating cash flow in year-1 (before annualization) | NaN | 508032000 |
| AY | Cash and cash equivalents at year-1 end | NaN | 554092000 |
| AZ | R&D expensed in year-1 (before annualization) | NaN | 76016000 |
| BB | Top 5 customers (% of year-1 revenue) | NaN | 0.121 |
| BC | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) | 1 | 0.5 |
| BR | Interest-bearing debt at year-1 end | NaN | 46266000 |
| CG | Financial statement unit multiplier | NaN | 1000 |
| CI | Year-3 financial period start | 2021-10-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2022-09-30 | 2022-12-31 |
| CK | Year-2 financial period start | 2022-10-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2023-09-30 | 2023-12-31 |
| CM | Year-1 financial period start | 2023-10-01 | 2024-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 2172400000 | 1046203000 |
| CO | Year-1 profit before tax (original) | NaN | -202756000 |
| CP | Year-1 profit for period (original) | NaN | -254891000 |
| CT | Gross profit in year-1 | 866800000 | 553736000 |
| CU | Capital expenditure in year-1 | NaN | 22068000 |

### 0805.HK - New Gonow Recreational Vehicles Inc. (35 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 224320000 | 300223000 |
| AA | total assets in year-2 | 300223000 | 398798000 |
| AB | total assets in year-1 | 398798000 | 525104000 |
| AC | total equity in year-3 | 26970000 | 56954000 |
| AD | total equity in year-2 | 56954000 | 27186000 |
| AE | total equity in year-1 | 27186000 | 35283000 |
| AF | total liability in year-3 | 197350000 | 243269000 |
| AG | total liability in year-2 | 243269000 | 371612000 |
| AH | total liability in year-1 | 371612000 | 489821000 |
| AI | Net sales in year-3 | 299672000 | 498780000 |
| AJ | Net sales in year-2 | 498780000 | 720303000 |
| AK | Net sales in year-1 | 720303000 | 843946000 |
| AL | Profit before tax in year-3 | 34325000 | 44261000 |
| AM | Profit before tax in year-2 | 44261000 | 107676000 |
| AN | Profit before tax in year-1 | 107676000 | 108010000 |
| AO | Profit for the year in year-3 | 25080000 | 32956000 |
| AP | Profit for the year in year-2 | 32956000 | 78768000 |
| AQ | Profit for the year in year-1 | 78768000 | 80860000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2023-12-31 | 2024-06-30 |
| AX | Operating cash flow in year-1 (before annualization) | 119770000 | 35554000 |
| AY | Cash and cash equivalents at year-1 end | 14345000 | 43882000 |
| AZ | R&D expensed in year-1 (before annualization) | 7968000 | 5625000 |
| BB | Top 5 customers (% of year-1 revenue) | 0.552 | 0.462 |
| BC | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) | 1 | 0.5 |
| BR | Interest-bearing debt at year-1 end | 103994000 | 191405000 |
| CI | Year-3 financial period start | 2021-01-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2021-12-31 | 2022-12-31 |
| CK | Year-2 financial period start | 2022-01-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2022-12-31 | 2023-12-31 |
| CM | Year-1 financial period start | 2023-01-01 | 2024-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 720303000 | 421973000 |
| CO | Year-1 profit before tax (original) | 107676000 | 54005000 |
| CP | Year-1 profit for period (original) | 78768000 | 40430000 |
| CT | Gross profit in year-1 | 181051000 | 134903000 |
| CU | Capital expenditure in year-1 | 7185000 | 3049000 |

### 1364.HK - Guming Holdings Limited (35 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 2043500000 | 3031676000 |
| AA | total assets in year-2 | 3031676000 | 5152929000 |
| AB | total assets in year-1 | 5152929000 | 6350749000 |
| AC | total equity in year-3 | -1205811000 | -816594000 |
| AD | total equity in year-2 | -816594000 | 615506000 |
| AE | total equity in year-1 | 615506000 | 1727640000 |
| AF | total liability in year-3 | 3249311000 | 3848270000 |
| AG | total liability in year-2 | 3848270000 | 4537423000 |
| AH | total liability in year-1 | 4537423000 | 4623109000 |
| AI | Net sales in year-3 | 4383901000 | 5559222000 |
| AJ | Net sales in year-2 | 5559222000 | 7675665000 |
| AK | Net sales in year-1 | 7675665000 | 8588384000 |
| AL | Profit before tax in year-3 | 247093000 | 650357000 |
| AM | Profit before tax in year-2 | 650357000 | 1445087000 |
| AN | Profit before tax in year-1 | 1445087000 | 1774349333 |
| AO | Profit for the year in year-3 | 23992000 | 372025000 |
| AP | Profit for the year in year-2 | 372025000 | 1096354000 |
| AQ | Profit for the year in year-1 | 1096354000 | 1493024000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2023-12-31 | 2024-09-30 |
| AX | Operating cash flow in year-1 (before annualization) | 1573306000 | 1128514000 |
| AY | Cash and cash equivalents at year-1 end | 2357961000 | 1677868000 |
| AZ | R&D expensed in year-1 (before annualization) | 198736000 | 165826000 |
| BB | Top 5 customers (% of year-1 revenue) | 0.032 | 0.026 |
| BC | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) | 1 | 0.75 |
| BR | Interest-bearing debt at year-1 end | 3350203000 | 3348672000 |
| CI | Year-3 financial period start | 2021-01-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2021-12-31 | 2022-12-31 |
| CK | Year-2 financial period start | 2022-01-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2022-12-31 | 2023-12-31 |
| CM | Year-1 financial period start | 2023-01-01 | 2024-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 7675665000 | 6441288000 |
| CO | Year-1 profit before tax (original) | 1445087000 | 1330762000 |
| CP | Year-1 profit for period (original) | 1096354000 | 1119768000 |
| CT | Gross profit in year-1 | 2403331000 | 1964382000 |
| CU | Capital expenditure in year-1 | 398800000 | 332647000 |

### 2097.HK - MIXUE Group - H shares (35 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 7316383000 | 9945356000 |
| AA | total assets in year-2 | 9945356000 | 14593566000 |
| AB | total assets in year-1 | 14593566000 | 18620333000 |
| AC | total equity in year-3 | 5542710000 | 7479267000 |
| AD | total equity in year-2 | 7479267000 | 10595465000 |
| AE | total equity in year-1 | 10595465000 | 14096206000 |
| AF | total liability in year-3 | 1773673000 | 2466089000 |
| AG | total liability in year-2 | 2466089000 | 3998101000 |
| AH | total liability in year-1 | 3998101000 | 4524127000 |
| AI | Net sales in year-3 | 10350986000 | 13575577000 |
| AJ | Net sales in year-2 | 13575577000 | 20302465000 |
| AK | Net sales in year-1 | 20302465000 | 24879561333 |
| AL | Profit before tax in year-3 | 2558874000 | 2658043000 |
| AM | Profit before tax in year-2 | 2658043000 | 4154002000 |
| AN | Profit before tax in year-1 | 4154002000 | 6091393333 |
| AO | Profit for the year in year-3 | 1911942000 | 2013091000 |
| AP | Profit for the year in year-2 | 2013091000 | 3186605000 |
| AQ | Profit for the year in year-1 | 3186605000 | 4654629333 |
| AW | Year-1 financial period end (dd/mm/yy) | 2023-12-31 | 2024-09-30 |
| AX | Operating cash flow in year-1 (before annualization) | 3793872000 | 5100754000 |
| AY | Cash and cash equivalents at year-1 end | 5621904000 | 5980396000 |
| AZ | R&D expensed in year-1 (before annualization) | 85000000 | 64805000 |
| BB | Top 5 customers (% of year-1 revenue) | 0.011 | 0.01 |
| BC | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) | 1 | 0.75 |
| BR | Interest-bearing debt at year-1 end | 259748000 | 92957000 |
| CI | Year-3 financial period start | 2021-01-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2021-12-31 | 2022-12-31 |
| CK | Year-2 financial period start | 2022-01-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2022-12-31 | 2023-12-31 |
| CM | Year-1 financial period start | 2023-01-01 | 2024-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 20302465000 | 18659671000 |
| CO | Year-1 profit before tax (original) | 4154002000 | 4568545000 |
| CP | Year-1 profit for period (original) | 3186605000 | 3490972000 |
| CT | Gross profit in year-1 | 5998967000 | 6040422000 |
| CU | Capital expenditure in year-1 | 1690766000 | 1200444000 |

### 2530.HK - Numans Health Food Holdings Company Limited (9 cells)

| col | header | before | after |
|---|---|---|---|
| BC | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) | 1 | 0.5 |
| CI | Year-3 financial period start | 2021-07-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2022-06-30 | 2022-12-31 |
| CK | Year-2 financial period start | 2022-07-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2023-06-30 | 2023-12-31 |
| CM | Year-1 financial period start | 2023-07-01 | 2024-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 292172000 | 146086000 |
| CO | Year-1 profit before tax (original) | 103398000 | 51699000 |
| CP | Year-1 profit for period (original) | 90562000 | 45281000 |

### 2560.HK - Anhui Conch Material Technology Co., Ltd. - H shares (9 cells)

| col | header | before | after |
|---|---|---|---|
| BC | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) | 1 | 0.5 |
| CI | Year-3 financial period start | 2021-07-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2022-06-30 | 2022-12-31 |
| CK | Year-2 financial period start | 2022-07-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2023-06-30 | 2023-12-31 |
| CM | Year-1 financial period start | 2023-07-01 | 2024-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 2206800000 | 1103400000 |
| CO | Year-1 profit before tax (original) | 141622000 | 70811000 |
| CP | Year-1 profit for period (original) | 120400000 | 60200000 |

### 2561.HK - VISEN Pharmaceuticals -B (8 cells)

| col | header | before | after |
|---|---|---|---|
| BC | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) | 1 | 0.75 |
| CI | Year-3 financial period start | 2021-10-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2022-09-30 | 2022-12-31 |
| CK | Year-2 financial period start | 2022-10-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2023-09-30 | 2023-12-31 |
| CM | Year-1 financial period start | 2023-10-01 | 2024-01-01 |
| CO | Year-1 profit before tax (original) | -172660000 | -129495000 |
| CP | Year-1 profit for period (original) | -172660000 | -129495000 |

### 2569.HK - Soft International Group Ltd (35 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 435222000 | 523892000 |
| AA | total assets in year-2 | 523892000 | 519438000 |
| AB | total assets in year-1 | 519438000 | 526891000 |
| AC | total equity in year-3 | -16265000 | 25051000 |
| AD | total equity in year-2 | 25051000 | 82991000 |
| AE | total equity in year-1 | 82991000 | 330337000 |
| AF | total liability in year-3 | 451487000 | 498841000 |
| AG | total liability in year-2 | 498841000 | 436447000 |
| AH | total liability in year-1 | 436447000 | 196554000 |
| AI | Net sales in year-3 | 263226000 | 408066000 |
| AJ | Net sales in year-2 | 408066000 | 654560000 |
| AK | Net sales in year-1 | 654560000 | 693729333 |
| AL | Profit before tax in year-3 | 12467000 | 50904000 |
| AM | Profit before tax in year-2 | 50904000 | 66612000 |
| AN | Profit before tax in year-1 | 66612000 | 67980000 |
| AO | Profit for the year in year-3 | 10002000 | 41859000 |
| AP | Profit for the year in year-2 | 41859000 | 57689000 |
| AQ | Profit for the year in year-1 | 57689000 | 53949333 |
| AW | Year-1 financial period end (dd/mm/yy) | 2023-12-31 | 2024-09-30 |
| AX | Operating cash flow in year-1 (before annualization) | 155964000 | 26216000 |
| AY | Cash and cash equivalents at year-1 end | 63000000 | 22867000 |
| AZ | R&D expensed in year-1 (before annualization) | 20638000 | 14899000 |
| BB | Top 5 customers (% of year-1 revenue) | 0.641 | 0.48 |
| BC | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) | 1 | 0.75 |
| BR | Interest-bearing debt at year-1 end | 13734000 | 41907000 |
| CI | Year-3 financial period start | 2021-01-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2021-12-31 | 2022-12-31 |
| CK | Year-2 financial period start | 2022-01-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2022-12-31 | 2023-12-31 |
| CM | Year-1 financial period start | 2023-01-01 | 2024-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 654560000 | 520297000 |
| CO | Year-1 profit before tax (original) | 66612000 | 50985000 |
| CP | Year-1 profit for period (original) | 57689000 | 40462000 |
| CT | Gross profit in year-1 | 197267000 | 162064000 |
| CU | Capital expenditure in year-1 | 39746000 | 19556000 |

### 2571.HK - Beijing Saimo Technology Co., Ltd. - H shares (36 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 315964000 | 544759000 |
| AA | total assets in year-2 | 544759000 | 600814000 |
| AB | total assets in year-1 | 600814000 | 565129000 |
| AC | total equity in year-3 | 265022000 | 446843000 |
| AD | total equity in year-2 | 446843000 | 501412000 |
| AE | total equity in year-1 | 501412000 | 497417000 |
| AF | total liability in year-3 | 50942000 | 97916000 |
| AG | total liability in year-2 | 97916000 | 99402000 |
| AH | total liability in year-1 | 99402000 | 67712000 |
| AI | Net sales in year-3 | 106906000 | 145385000 |
| AJ | Net sales in year-2 | 145385000 | 175703000 |
| AK | Net sales in year-1 | 175703000 | 111120000 |
| AL | Profit before tax in year-3 | 39131000 | 48686000 |
| AM | Profit before tax in year-2 | 48686000 | 50755000 |
| AN | Profit before tax in year-1 | 50755000 | -13492000 |
| AO | Profit for the year in year-3 | 37571000 | 48686000 |
| AP | Profit for the year in year-2 | 48686000 | 53431000 |
| AQ | Profit for the year in year-1 | 53431000 | -9198000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2023-12-31 | 2024-06-30 |
| AX | Operating cash flow in year-1 (before annualization) | 50466000 | 554000 |
| AY | Cash and cash equivalents at year-1 end | 118431000 | 34090000 |
| AZ | R&D expensed in year-1 (before annualization) | 71331000 | 41106000 |
| BA | Development costs capitalized in year-1 (additions, before annualization) | 5056000 | 0 |
| BB | Top 5 customers (% of year-1 revenue) | 0.558 | 0.761 |
| BC | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) | 1 | 0.5 |
| BR | Interest-bearing debt at year-1 end | 40520000 | 27284000 |
| CI | Year-3 financial period start | 2021-01-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2021-12-31 | 2022-12-31 |
| CK | Year-2 financial period start | 2022-01-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2022-12-31 | 2023-12-31 |
| CM | Year-1 financial period start | 2023-01-01 | 2024-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 175703000 | 55560000 |
| CO | Year-1 profit before tax (original) | 50755000 | -6746000 |
| CP | Year-1 profit for period (original) | 53431000 | -4599000 |
| CT | Gross profit in year-1 | 124564000 | 39064000 |
| CU | Capital expenditure in year-1 | 69365000 | 12322000 |

### 2596.HK - Yibin City Commercial Bank Co., Ltd - H Shares (8 cells)

| col | header | before | after |
|---|---|---|---|
| BC | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) | 1 | 0.5 |
| CI | Year-3 financial period start | 2021-07-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2022-06-30 | 2022-12-31 |
| CK | Year-2 financial period start | 2022-07-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2023-06-30 | 2023-12-31 |
| CM | Year-1 financial period start | 2023-07-01 | 2024-01-01 |
| CO | Year-1 profit before tax (original) | 693964000 | 346982000 |
| CP | Year-1 profit for period (original) | 523664000 | 261832000 |

### 2610.HK - Nanshan Aluminium International Holdings Limited (33 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 1202411000 | 1282117000 |
| AA | total assets in year-2 | 1282117000 | 1437962000 |
| AB | total assets in year-1 | 1437962000 | 1689536000 |
| AC | total equity in year-3 | 1005493000 | 995509000 |
| AD | total equity in year-2 | 995509000 | 1269640000 |
| AE | total equity in year-1 | 1269640000 | 1212002000 |
| AF | total liability in year-3 | 196918000 | 286608000 |
| AG | total liability in year-2 | 286608000 | 168322000 |
| AH | total liability in year-1 | 168322000 | 477534000 |
| AI | Net sales in year-3 | 172842000 | 466777000 |
| AJ | Net sales in year-2 | 466777000 | 677785000 |
| AK | Net sales in year-1 | 677785000 | 910717333 |
| AL | Profit before tax in year-3 | 41658000 | 103132000 |
| AM | Profit before tax in year-2 | 103132000 | 187089000 |
| AN | Profit before tax in year-1 | 187089000 | 393400000 |
| AO | Profit for the year in year-3 | 39710000 | 96092000 |
| AP | Profit for the year in year-2 | 96092000 | 173525000 |
| AQ | Profit for the year in year-1 | 173525000 | 355101333 |
| AW | Year-1 financial period end (dd/mm/yy) | 2023-12-31 | 2024-09-30 |
| AX | Operating cash flow in year-1 (before annualization) | 96269000 | 422248000 |
| AY | Cash and cash equivalents at year-1 end | 251561000 | 439201000 |
| BC | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) | 1 | 0.75 |
| BR | Interest-bearing debt at year-1 end | 907000 | 7907000 |
| CI | Year-3 financial period start | 2021-01-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2021-12-31 | 2022-12-31 |
| CK | Year-2 financial period start | 2022-01-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2022-12-31 | 2023-12-31 |
| CM | Year-1 financial period start | 2023-01-01 | 2024-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 677785000 | 683038000 |
| CO | Year-1 profit before tax (original) | 187089000 | 295050000 |
| CP | Year-1 profit for period (original) | 173525000 | 266326000 |
| CT | Gross profit in year-1 | 197668000 | 316058000 |
| CU | Capital expenditure in year-1 | 72800000 | 150932000 |

### 2613.HK - ContiOcean Environment Tech Group Co., Ltd. - H shares (35 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 358405000 | 376716000 |
| AA | total assets in year-2 | 376716000 | 522500000 |
| AB | total assets in year-1 | 522500000 | 410723000 |
| AC | total equity in year-3 | 113600000 | 135903000 |
| AD | total equity in year-2 | 135903000 | 254791000 |
| AE | total equity in year-1 | 254791000 | 239409000 |
| AF | total liability in year-3 | 244805000 | 240813000 |
| AG | total liability in year-2 | 240813000 | 267709000 |
| AH | total liability in year-1 | 267709000 | 171314000 |
| AI | Net sales in year-3 | 140521000 | 267233000 |
| AJ | Net sales in year-2 | 267233000 | 510255000 |
| AK | Net sales in year-1 | 510255000 | 672932000 |
| AL | Profit before tax in year-3 | 14764000 | 42895000 |
| AM | Profit before tax in year-2 | 42895000 | 140784000 |
| AN | Profit before tax in year-1 | 140784000 | 191636000 |
| AO | Profit for the year in year-3 | 12769000 | 36777000 |
| AP | Profit for the year in year-2 | 36777000 | 120534000 |
| AQ | Profit for the year in year-1 | 120534000 | 164164000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2023-12-31 | 2024-06-30 |
| AX | Operating cash flow in year-1 (before annualization) | 151107000 | -14908000 |
| AY | Cash and cash equivalents at year-1 end | 177414000 | 155634000 |
| AZ | R&D expensed in year-1 (before annualization) | 18929000 | 10148000 |
| BB | Top 5 customers (% of year-1 revenue) | 0.843 | 0.894 |
| BC | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) | 1 | 0.5 |
| BR | Interest-bearing debt at year-1 end | 22788000 | 29125000 |
| CI | Year-3 financial period start | 2021-01-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2021-12-31 | 2022-12-31 |
| CK | Year-2 financial period start | 2022-01-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2022-12-31 | 2023-12-31 |
| CM | Year-1 financial period start | 2023-01-01 | 2024-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 510255000 | 336466000 |
| CO | Year-1 profit before tax (original) | 140784000 | 95818000 |
| CP | Year-1 profit for period (original) | 120534000 | 82082000 |
| CT | Gross profit in year-1 | 241737000 | 142782000 |
| CU | Capital expenditure in year-1 | 3467000 | 1470000 |

### 2625.HK - Jiangsu Horizon Chain Supermarket Company Limited - H shares (34 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 1177000000 | 1331539000 |
| AA | total assets in year-2 | 1331539000 | 1407136000 |
| AB | total assets in year-1 | 1407136000 | 1399974000 |
| AC | total equity in year-3 | 397511000 | 446780000 |
| AD | total equity in year-2 | 446780000 | 493341000 |
| AE | total equity in year-1 | 493341000 | 518475000 |
| AF | total liability in year-3 | 779489000 | 884759000 |
| AG | total liability in year-2 | 884759000 | 913795000 |
| AH | total liability in year-1 | 913795000 | 881499000 |
| AI | Net sales in year-3 | 1432193000 | 1328685000 |
| AJ | Net sales in year-2 | 1328685000 | 1401972000 |
| AK | Net sales in year-1 | 1401972000 | 1341080000 |
| AL | Profit before tax in year-3 | 47696000 | 68487000 |
| AM | Profit before tax in year-2 | 68487000 | 70058000 |
| AN | Profit before tax in year-1 | 70058000 | 46802667 |
| AO | Profit for the year in year-3 | 35080000 | 51065000 |
| AP | Profit for the year in year-2 | 51065000 | 51602000 |
| AQ | Profit for the year in year-1 | 51602000 | 32104000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2023-12-31 | 2024-09-30 |
| AX | Operating cash flow in year-1 (before annualization) | 69219000 | -10625000 |
| AY | Cash and cash equivalents at year-1 end | 236226000 | 147792000 |
| BB | Top 5 customers (% of year-1 revenue) | 0.318 | 0.285 |
| BC | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) | 1 | 0.75 |
| BR | Interest-bearing debt at year-1 end | 575445000 | 579772000 |
| CI | Year-3 financial period start | 2021-01-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2021-12-31 | 2022-12-31 |
| CK | Year-2 financial period start | 2022-01-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2022-12-31 | 2023-12-31 |
| CM | Year-1 financial period start | 2023-01-01 | 2024-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 1401972000 | 1005810000 |
| CO | Year-1 profit before tax (original) | 70058000 | 35102000 |
| CP | Year-1 profit for period (original) | 51602000 | 24078000 |
| CT | Gross profit in year-1 | 301376000 | 208434000 |
| CU | Capital expenditure in year-1 | 40731000 | 29058000 |

### 6681.HK - BrainAurora Medical Technology Limited - B (9 cells)

| col | header | before | after |
|---|---|---|---|
| BC | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) | 1 | 0.5 |
| CI | Year-3 financial period start | 2021-07-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2022-06-30 | 2022-12-31 |
| CK | Year-2 financial period start | 2022-07-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2023-06-30 | 2023-12-31 |
| CM | Year-1 financial period start | 2023-07-01 | 2024-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 103774000 | 51887000 |
| CO | Year-1 profit before tax (original) | -228778000 | -114389000 |
| CP | Year-1 profit for period (original) | -228778000 | -114389000 |

### 6693.HK - Chifeng Jilong Gold Mining Co., Ltd. - H shares (9 cells)

| col | header | before | after |
|---|---|---|---|
| BC | Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5) | 1 | 0.75 |
| CI | Year-3 financial period start | 2021-10-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2022-09-30 | 2022-12-31 |
| CK | Year-2 financial period start | 2022-10-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2023-09-30 | 2023-12-31 |
| CM | Year-1 financial period start | 2023-10-01 | 2024-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 8297108000 | 6222831000 |
| CO | Year-1 profit before tax (original) | 2464046667 | 1848035000 |
| CP | Year-1 profit for period (original) | 1686358667 | 1264769000 |

