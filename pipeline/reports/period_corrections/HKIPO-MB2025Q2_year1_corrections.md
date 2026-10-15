# 2025Q2 Main Board: year-1 re-anchored to the audited Track Record

Same standard as `HKIPO-MB2026Q2_year1_corrections.md` and `HKIPO-MB2026Q3_year1_corrections.md`:
year-1 is the latest period of the audited Accountants' Report / "Track Record Period" definition;
unaudited figures outside it are never year-1; only sales, profit before tax and profit for the period
are annualised (BC = months/12, originals in CN/CO/CP).

## What changed

| Group | Issuers | Before → after |
|---|---|---|
| Unaudited quarterly dates outside Track Record used as year-1; Track Record ended 31/12/2024 | 3750.HK (CATL), 2619.HK (X.J. Electrics) | Unaudited 31/03/25 or 30/04/25 → Audited FY2024 ended 31/12/2024 (full year, not annualised) |
| Short track record due to incorporation (8 Dec 2022); period override recorded | 6603.HK (IFBH Limited) | Added `period-override` note to `col_AT`; FY2024 ended 31/12/2024 validated |

The other 24 issuers in 2025Q2 already matched their Track Record (FY2024 ending 31 Dec 2024 or FY2025 ending 31 Mar 2025); their cells are unchanged.

For 3750.HK and 2619.HK, the 27 period-dependent payload fields were re-extracted from the audited Accountants' Report
(other fields untouched), validated, recorded `extracted`, and independently reviewed against original disclosure pages;
reports bound to each payload sha256 are in `pipeline/prospectus_pipeline/out/period_reviews/2025Q2/`. Reviewed payloads
were written back to the workbook, followed by `disclosure_notes` (all 27 on the Track Record basis), `audit` (1890/1890 perfect match),
`cross_check` (5 pre-existing allocation warnings, unchanged), `export` and `master --derive`. 2025Q2 `validate`: 27/27 target, 0 errors, gate PASS.

## Pending

None in 2025Q2.

## Every changed cell (before → after)

### 2619.HK - X.J. Electrics (Hu Bei) Co., Ltd - H Shares (35 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 1550292000 | 1220774000 |
| AA | total assets in year-2 | 1706979000 | 1550292000 |
| AB | total assets in year-1 | NaN | 1706979000 |
| AC | total equity in year-3 | 784935000 | 663167000 |
| AD | total equity in year-2 | 926211000 | 784935000 |
| AE | total equity in year-1 | NaN | 926211000 |
| AF | total liability in year-3 | 765357000 | 557607000 |
| AG | total liability in year-2 | 780768000 | 765357000 |
| AH | total liability in year-1 | NaN | 780768000 |
| AI | Net sales in year-3 | 1188321000 | 1096965000 |
| AJ | Net sales in year-2 | 1501510000 | 1188321000 |
| AK | Net sales in year-1 | NaN | 1501510000 |
| AL | Profit before tax in year-3 | 146693000 | 91921000 |
| AM | Profit before tax in year-2 | 161315000 | 146693000 |
| AN | Profit before tax in year-1 | NaN | 161315000 |
| AO | Profit for the year in year-3 | 121462000 | 80261000 |
| AP | Profit for the year in year-2 | 140425000 | 121462000 |
| AQ | Profit for the year in year-1 | NaN | 140425000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2025-04-30 | 2024-12-31 |
| AX | Operating cash flow in year-1 (before annualization) | NaN | 71288000 |
| AY | Cash and cash equivalents at year-1 end | 490300000 | 474154000 |
| AZ | R&D expensed in year-1 (before annualization) | NaN | 36426000 |
| BA | Development costs capitalized in year-1 (additions, before annualization) | NaN | 0 |
| BB | Top 5 customers (% of year-1 revenue) | NaN | 0.779 |
| BR | Interest-bearing debt at year-1 end | 466500000 | 323091000 |
| CG | Financial statement unit multiplier | NaN | 1000 |
| CI | Year-3 financial period start | 2022-05-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2023-04-30 | 2022-12-31 |
| CK | Year-2 financial period start | 2023-05-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2024-04-30 | 2023-12-31 |
| CM | Year-1 financial period start | 2024-05-01 | 2024-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | NaN | 1501510000 |
| CO | Year-1 profit before tax (original) | NaN | 161315000 |
| CP | Year-1 profit for period (original) | NaN | 140425000 |
| CU | Capital expenditure in year-1 | 114706000 | 165333000 |

### 3750.HK - Contemporary Amperex Technology Co., Limited - H shares (35 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 717168041000 | 600952353000 |
| AA | total assets in year-2 | 786658123000 | 717168041000 |
| AB | total assets in year-1 | 820097269000 | 786658123000 |
| AC | total equity in year-3 | 219883150000 | 176909161000 |
| AD | total equity in year-2 | 273456173000 | 219883150000 |
| AE | total equity in year-1 | 289139355000 | 273456173000 |
| AF | total liability in year-3 | 497284891000 | 424043192000 |
| AG | total liability in year-2 | 513201950000 | 497284891000 |
| AH | total liability in year-1 | 530957914000 | 513201950000 |
| AI | Net sales in year-3 | 400917045000 | 328593988000 |
| AJ | Net sales in year-2 | 362012554000 | 400917045000 |
| AK | Net sales in year-1 | 338818356000 | 362012554000 |
| AL | Profit before tax in year-3 | 54495054000 | 36672857000 |
| AM | Profit before tax in year-2 | 64470204000 | 54495054000 |
| AN | Profit before tax in year-1 | 69500124000 | 64470204000 |
| AO | Profit for the year in year-3 | 47342035000 | 33457144000 |
| AP | Profit for the year in year-2 | 55294959000 | 47342035000 |
| AQ | Profit for the year in year-1 | 59445536000 | 55294959000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2025-03-31 | 2024-12-31 |
| AX | Operating cash flow in year-1 (before annualization) | 32868257000 | 96990344000 |
| AY | Cash and cash equivalents at year-1 end | 286300836000 | 270159734000 |
| AZ | R&D expensed in year-1 (before annualization) | 4814003000 | 18606756000 |
| BA | Development costs capitalized in year-1 (additions, before annualization) | NaN | 0 |
| BR | Interest-bearing debt at year-1 end | 137584403000 | 137830010000 |
| CG | Financial statement unit multiplier | NaN | 1000 |
| CI | Year-3 financial period start | 2022-04-01 | 2022-01-01 |
| CJ | Year-3 financial period end | 2023-03-31 | 2022-12-31 |
| CK | Year-2 financial period start | 2023-04-01 | 2023-01-01 |
| CL | Year-2 financial period end | 2024-03-31 | 2023-12-31 |
| CM | Year-1 financial period start | 2024-04-01 | 2024-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 338818356000 | 362012554000 |
| CO | Year-1 profit before tax (original) | 69500124000 | 64470204000 |
| CP | Year-1 profit for period (original) | 59445536000 | 55294959000 |
| CT | Gross profit in year-1 | 20674478000 | 88493595000 |
| CU | Capital expenditure in year-1 | 10342606000 | 31179943000 |

