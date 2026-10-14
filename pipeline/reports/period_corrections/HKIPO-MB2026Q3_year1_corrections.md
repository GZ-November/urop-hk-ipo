# 2026Q3 Main Board: year-1 re-anchored to the audited Track Record

Standard (teacher's manual §2.3; `src/periods.py`; AGENTS.md): year-1 is the latest period of the
audited Accountants' Report / "Track Record Period" definition, full year or stub. year-2 and year-3 are
the two complete financial years before it. Only sales, profit before tax and profit for the period
(sheet AK/AN/AQ = schema col_AH/AK/AN) are annualised (×12/months); BC = months/12 and the originals
are in CN/CO/CP. Balances are at the year-1 end; other year-1 flows are original-period values.
Unaudited figures outside the Accountants' Report are never year-1.

## What changed

| Group | Issuers | Before → after |
|---|---|---|
| Unaudited Q1 2026 used as year-1; Track Record = FY2023–FY2025 | 0537, 0668, 1377, 2249, 2475, 6745, 6951 | year-1 3M Mar-26 (×4) → FY2025 (not annualised) |
| Track Record stub missed | 3228, 3757 | FY2025 → 4M Apr-26 (×3) |
| | 6727, 6802 | FY2025 → 3M Mar-26 (×4) |
| | 6731, 9607, 9856 | FY2025 → 6M Jun-26 (×2) |
| Stub already correct; derived columns were stale (BC = 1 bug) | 0625, 2041, 2261, 3223, 3231, 3308, 9615, 9976 | BC, CI–CP re-derived only |

For the 14 re-anchored issuers the 27 period-dependent payload fields (col_W–AN, AT–AY, BE, CF, CG) were
re-extracted from the prospectus; every other field (shares, offering, VC/PE, cornerstone, allotment) is
unchanged. Each payload passed `validate` (period-anchor gate included), was recorded `extracted`, and was
independently reviewed by a fresh-context reviewer against the original PDF pages; the report, bound to
the payload sha256, is in `prospectus_pipeline/out/period_reviews/2026Q3/`. Only reviewed payloads were
written back (`write --target prospectus --only`), then `disclosure_notes`, `audit` (2100/2100 cells
match), `cross_check`, `export` and `master --derive` were rerun. 2026Q3 `validate`: 30/30 issuers,
0 errors, gate PASS.

Judgement calls (all accepted by the reviewers; listed in each review report):
- Total assets/liabilities summed from current + non-current subtotals where no total line exists: 6951, 3757, 6727.
- col_BE (interest-bearing debt) = INDEBTEDNESS table Total, except 6731 and 9856, whose Total is dominated by
  redemption liabilities owed to pre-IPO investors; BE there = bank borrowings + lease liabilities
  (literal Totals: 6731 1,790,271k; 9856 2,409,394k). 2249's previous BE (19,492,700) was borrowings only
  and off by ×1000; now the full Total 21,508,961k.
- col_CG keeps each issuer's previously reviewed capex basis (PPE line, combined PPE+intangibles line, or the
  issuer's capital-expenditure table/paragraph).

## Pending

None in 2026Q3: every issuer's col_AT, factor and year-2/3 now agree with its audited Track Record.

## Every changed cell (before → after)

### 0668.HK (35 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 16603708000 | 12776703000 |
| AA | total assets in year-2 | 20066893000 | 16603708000 |
| AB | total assets in year-1 | 20228400000 | 20066893000 |
| AC | total equity in year-3 | 9144520000 | 8161299000 |
| AD | total equity in year-2 | 10711670000 | 9144520000 |
| AE | total equity in year-1 | 11344197000 | 10711670000 |
| AF | total liability in year-3 | 7459188000 | 4615404000 |
| AG | total liability in year-2 | 9355223000 | 7459188000 |
| AH | total liability in year-1 | 8884200000 | 9355223000 |
| AI | Net sales in year-3 | 24710080000 | 17507203000 |
| AJ | Net sales in year-2 | 30514403000 | 24710080000 |
| AK | Net sales in year-1 | 30430584000 | 30514403000 |
| AL | Profit before tax in year-3 | 2348349000 | 1812512000 |
| AM | Profit before tax in year-2 | 2922474000 | 2348349000 |
| AN | Profit before tax in year-1 | 2234896000 | 2922474000 |
| AO | Profit for the year in year-3 | 2211124000 | 1693939000 |
| AP | Profit for the year in year-2 | 2617194000 | 2211124000 |
| AQ | Profit for the year in year-1 | 1883688000 | 2617194000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2026-03-31 | 2025-12-31 |
| AX | Operating cash flow in year-1 (before annualizat | -450632000 | 480807000 |
| AY | Cash and cash equivalents at year-1 end | 2670127000 | 3067742000 |
| AZ | R&D expensed in year-1 (before annualization) | 805291000 | 2892785000 |
| BB | Top 5 customers (% of year-1 revenue) | NaN | 0.086 |
| BR | Interest-bearing debt at year-1 end | 3108231000 | 2918825000 |
| CG | Financial statement unit multiplier |  | 1000 |
| CI | Year-3 financial period start | 2023-04-01 | 2023-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2023-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2024-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2024-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2025-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 30430584000 | 30514403000 |
| CO | Year-1 profit before tax (original) | 2234896000 | 2922474000 |
| CP | Year-1 profit for period (original) | 1883688000 | 2617194000 |
| CT | Gross profit in year-1 | 3253208000 | 13386431000 |
| CU | Capital expenditure in year-1 | 25360000 | 365120000 |

### 0537.HK (35 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 3852922000 | 3265683000 |
| AA | total assets in year-2 | 3584586000 | 3852922000 |
| AB | total assets in year-1 | 3550966000 | 3584586000 |
| AC | total equity in year-3 | 3167740000 | 2889230000 |
| AD | total equity in year-2 | 3160818000 | 3167740000 |
| AE | total equity in year-1 | 3179584000 | 3160818000 |
| AF | total liability in year-3 | 685182000 | 376453000 |
| AG | total liability in year-2 | 423768000 | 685182000 |
| AH | total liability in year-1 | 371382000 | 423768000 |
| AI | Net sales in year-3 | 775826000 | 670538000 |
| AJ | Net sales in year-2 | 900234000 | 775826000 |
| AK | Net sales in year-1 | 926256000 | 900234000 |
| AL | Profit before tax in year-3 | 76818000 | 113838000 |
| AM | Profit before tax in year-2 | 91053000 | 76818000 |
| AN | Profit before tax in year-1 | 108724000 | 91053000 |
| AO | Profit for the year in year-3 | 92303000 | 107953000 |
| AP | Profit for the year in year-2 | 86083000 | 92303000 |
| AQ | Profit for the year in year-1 | 92600000 | 86083000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2026-03-31 | 2025-12-31 |
| AX | Operating cash flow in year-1 (before annualizat | -5271000 | 85311000 |
| AY | Cash and cash equivalents at year-1 end | 300303000 | 330566000 |
| AZ | R&D expensed in year-1 (before annualization) | 56119000 | 225895000 |
| BB | Top 5 customers (% of year-1 revenue) | NaN | 0.306 |
| BR | Interest-bearing debt at year-1 end | 58378000 | 89872000 |
| CG | Financial statement unit multiplier |  | 1000 |
| CI | Year-3 financial period start | 2023-04-01 | 2023-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2023-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2024-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2024-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2025-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 926256000 | 900234000 |
| CO | Year-1 profit before tax (original) | 108724000 | 91053000 |
| CP | Year-1 profit for period (original) | 92600000 | 86083000 |
| CT | Gross profit in year-1 | 128551000 | 475717000 |
| CU | Capital expenditure in year-1 | 1318000 | 55585000 |

### 1377.HK (35 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 3520596000 | 3179443000 |
| AA | total assets in year-2 | 4538074000 | 3520596000 |
| AB | total assets in year-1 | 5328243000 | 4538074000 |
| AC | total equity in year-3 | 2479467000 | 2319541000 |
| AD | total equity in year-2 | 2648954000 | 2479467000 |
| AE | total equity in year-1 | 2901986000 | 2648954000 |
| AF | total liability in year-3 | 1041129000 | 859902000 |
| AG | total liability in year-2 | 1889120000 | 1041129000 |
| AH | total liability in year-1 | 2426257000 | 1889120000 |
| AI | Net sales in year-3 | 1552635000 | 1295121000 |
| AJ | Net sales in year-2 | 2084177000 | 1552635000 |
| AK | Net sales in year-1 | 3024268000 | 2084177000 |
| AL | Profit before tax in year-3 | 257779000 | 248270000 |
| AM | Profit before tax in year-2 | 491750000 | 257779000 |
| AN | Profit before tax in year-1 | 1207584000 | 491750000 |
| AO | Profit for the year in year-3 | 227306000 | 219485000 |
| AP | Profit for the year in year-2 | 431641000 | 227306000 |
| AQ | Profit for the year in year-1 | 1040772000 | 431641000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2026-03-31 | 2025-12-31 |
| AX | Operating cash flow in year-1 (before annualizat | -47761000 | 290852000 |
| AY | Cash and cash equivalents at year-1 end | 451362000 | 271331000 |
| AZ | R&D expensed in year-1 (before annualization) | 40645000 | 135894000 |
| BB | Top 5 customers (% of year-1 revenue) | NaN | 0.308 |
| BR | Interest-bearing debt at year-1 end | 1167459000 | 624974000 |
| CG | Financial statement unit multiplier |  | 1000 |
| CI | Year-3 financial period start | 2023-04-01 | 2023-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2023-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2024-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2024-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2025-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 3024268000 | 2084177000 |
| CO | Year-1 profit before tax (original) | 1207584000 | 491750000 |
| CP | Year-1 profit for period (original) | 1040772000 | 431641000 |
| CT | Gross profit in year-1 | 375696000 | 843032000 |
| CU | Capital expenditure in year-1 | 271565000 | 495904000 |

### 2475.HK (35 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 223827586000 | 161992100000 |
| AA | total assets in year-2 | 306537675000 | 223827586000 |
| AB | total assets in year-1 | 325616587000 | 306537675000 |
| AC | total equity in year-3 | 84687125000 | 70284865000 |
| AD | total equity in year-2 | 104020233000 | 84687125000 |
| AE | total equity in year-1 | 108978157000 | 104020233000 |
| AF | total liability in year-3 | 139140461000 | 91707235000 |
| AG | total liability in year-2 | 202517442000 | 139140461000 |
| AH | total liability in year-1 | 216638430000 | 202517442000 |
| AI | Net sales in year-3 | 268794738000 | 231905460000 |
| AJ | Net sales in year-2 | 332344443000 | 268794738000 |
| AK | Net sales in year-1 | 335553968000 | 332344443000 |
| AL | Profit before tax in year-3 | 16108739000 | 12885042000 |
| AM | Profit before tax in year-2 | 19549858000 | 16108739000 |
| AN | Profit before tax in year-1 | 17163816000 | 19549858000 |
| AO | Profit for the year in year-3 | 14579044000 | 12243213000 |
| AP | Profit for the year in year-2 | 18170237000 | 14579044000 |
| AQ | Profit for the year in year-1 | 15870540000 | 18170237000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2026-03-31 | 2025-12-31 |
| AX | Operating cash flow in year-1 (before annualizat | -7068301000 | 17325330000 |
| AY | Cash and cash equivalents at year-1 end | 67320137000 | 59340613000 |
| AZ | R&D expensed in year-1 (before annualization) | 3021085000 | 11428041000 |
| BA | Development costs capitalized in year-1 (additio | 0 | 90951000 |
| BB | Top 5 customers (% of year-1 revenue) | NaN | 0.65 |
| CG | Financial statement unit multiplier |  | 1000 |
| CI | Year-3 financial period start | 2023-04-01 | 2023-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2023-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2024-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2024-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2025-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 335553968000 | 332344443000 |
| CO | Year-1 profit before tax (original) | 17163816000 | 19549858000 |
| CP | Year-1 profit for period (original) | 15870540000 | 18170237000 |
| CT | Gross profit in year-1 | 9558528000 | 38443840000 |
| CU | Capital expenditure in year-1 | 5538975000 | 17904338000 |

### 6951.HK (35 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 23915804000 | 21826964000 |
| AA | total assets in year-2 | 26506089000 | 23915804000 |
| AB | total assets in year-1 | 27033473000 | 26506089000 |
| AC | total equity in year-3 | 19871768000 | 18239100000 |
| AD | total equity in year-2 | 21663042000 | 19871768000 |
| AE | total equity in year-1 | 22400977000 | 21663042000 |
| AF | total liability in year-3 | 4044036000 | 3587864000 |
| AG | total liability in year-2 | 4843047000 | 4044036000 |
| AH | total liability in year-1 | 4632496000 | 4843047000 |
| AI | Net sales in year-3 | 7266133000 | 5681529000 |
| AJ | Net sales in year-2 | 8868527000 | 7266133000 |
| AK | Net sales in year-1 | 10605356000 | 8868527000 |
| AL | Profit before tax in year-3 | 2518943000 | 1782848000 |
| AM | Profit before tax in year-2 | 3008176000 | 2518943000 |
| AN | Profit before tax in year-1 | 3630968000 | 3008176000 |
| AO | Profit for the year in year-3 | 2190233000 | 1583151000 |
| AP | Profit for the year in year-2 | 2616980000 | 2190233000 |
| AQ | Profit for the year in year-1 | 3163220000 | 2616980000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2026-03-31 | 2025-12-31 |
| AX | Operating cash flow in year-1 (before annualizat | 156685000 | 2877609000 |
| AY | Cash and cash equivalents at year-1 end | 3564395000 | 2285396000 |
| AZ | R&D expensed in year-1 (before annualization) | 155810000 | 653437000 |
| BB | Top 5 customers (% of year-1 revenue) | NaN | 0.152 |
| BR | Interest-bearing debt at year-1 end | 812367000 | 586438000 |
| CG | Financial statement unit multiplier |  | 1000 |
| CI | Year-3 financial period start | 2023-04-01 | 2023-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2023-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2024-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2024-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2025-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 10605356000 | 8868527000 |
| CO | Year-1 profit before tax (original) | 3630968000 | 3008176000 |
| CP | Year-1 profit for period (original) | 3163220000 | 2616980000 |
| CT | Gross profit in year-1 | 1095552000 | 3542782000 |
| CU | Capital expenditure in year-1 | 187760000 | 578546000 |

### 2249.HK (36 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 50398582000 | 48156278000 |
| AA | total assets in year-2 | 53297969000 | 50398582000 |
| AB | total assets in year-1 | 54705900000 | 53297969000 |
| AC | total equity in year-3 | 26088968000 | 22138164000 |
| AD | total equity in year-2 | 28087689000 | 26088968000 |
| AE | total equity in year-1 | 29759200000 | 28087689000 |
| AF | total liability in year-3 | 24309614000 | 26018114000 |
| AG | total liability in year-2 | 25210280000 | 24309614000 |
| AH | total liability in year-1 | 24946700000 | 25210280000 |
| AI | Net sales in year-3 | 9119580000 | 7182744000 |
| AJ | Net sales in year-2 | 10388302000 | 9119580000 |
| AK | Net sales in year-1 | 11224520000 | 10388302000 |
| AL | Profit before tax in year-3 | 482460000 | 119341000 |
| AM | Profit before tax in year-2 | 466694000 | 482460000 |
| AN | Profit before tax in year-1 | 114288000 | 466694000 |
| AO | Profit for the year in year-3 | 482197000 | 119165000 |
| AP | Profit for the year in year-2 | 466498000 | 482197000 |
| AQ | Profit for the year in year-1 | 114064000 | 466498000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2026-03-31 | 2025-12-31 |
| AX | Operating cash flow in year-1 (before annualizat | 963808000 | 3842920000 |
| AY | Cash and cash equivalents at year-1 end | 2874143000 | 2276620000 |
| AZ | R&D expensed in year-1 (before annualization) | 302589000 | 1453400000 |
| BA | Development costs capitalized in year-1 (additio | 57252000 | 0 |
| BB | Top 5 customers (% of year-1 revenue) | NaN | 0.579 |
| BR | Interest-bearing debt at year-1 end | 19492700 | 21508961000 |
| CG | Financial statement unit multiplier |  | 1000 |
| CI | Year-3 financial period start | 2023-04-01 | 2023-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2023-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2024-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2024-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2025-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 11224520000 | 10388302000 |
| CO | Year-1 profit before tax (original) | 114288000 | 466694000 |
| CP | Year-1 profit for period (original) | 114064000 | 466498000 |
| CT | Gross profit in year-1 | 573538000 | 2358065000 |
| CU | Capital expenditure in year-1 | 1426645000 | 9303151000 |

### 6745.HK (35 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 22956459000 | 21134389000 |
| AA | total assets in year-2 | 24259291000 | 22956459000 |
| AB | total assets in year-1 | 24397323000 | 24259291000 |
| AC | total equity in year-3 | 11382714000 | 11524020000 |
| AD | total equity in year-2 | 12152769000 | 11382714000 |
| AE | total equity in year-1 | 12329303000 | 12152769000 |
| AF | total liability in year-3 | 11573745000 | 9610369000 |
| AG | total liability in year-2 | 12106522000 | 11573745000 |
| AH | total liability in year-1 | 12068020000 | 12106522000 |
| AI | Net sales in year-3 | 10228062000 | 7305904000 |
| AJ | Net sales in year-2 | 14836442000 | 10228062000 |
| AK | Net sales in year-1 | 15690168000 | 14836442000 |
| AL | Profit before tax in year-3 | 121427000 | 484154000 |
| AM | Profit before tax in year-2 | 355662000 | 121427000 |
| AN | Profit before tax in year-1 | 999444000 | 355662000 |
| AO | Profit for the year in year-3 | 217255000 | 398904000 |
| AP | Profit for the year in year-2 | 235492000 | 217255000 |
| AQ | Profit for the year in year-1 | 691232000 | 235492000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2026-03-31 | 2025-12-31 |
| AX | Operating cash flow in year-1 (before annualizat | 191310000 | 2865408000 |
| AY | Cash and cash equivalents at year-1 end | 1497412000 | 1701588000 |
| AZ | R&D expensed in year-1 (before annualization) | 12599000 | 173193000 |
| BB | Top 5 customers (% of year-1 revenue) | NaN | 0.213 |
| BR | Interest-bearing debt at year-1 end | 9439927000 | 9317372000 |
| CG | Financial statement unit multiplier |  | 1000 |
| CI | Year-3 financial period start | 2023-04-01 | 2023-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2023-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2024-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2024-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2025-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 15690168000 | 14836442000 |
| CO | Year-1 profit before tax (original) | 999444000 | 355662000 |
| CP | Year-1 profit for period (original) | 691232000 | 235492000 |
| CT | Gross profit in year-1 | 506781000 | 1455575000 |
| CU | Capital expenditure in year-1 | 110459000 | 828964000 |

### 3308.HK (9 cells)

| col | header | before | after |
|---|---|---|---|
| BC | Comments (nearest sales& profit adjustment facto | 1 | 0.25 |
| CI | Year-3 financial period start | 2023-04-01 | 2024-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2024-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2025-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2025-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2026-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 77985592000 | 19496398000 |
| CO | Year-1 profit before tax (original) | 30143208000 | 7535802000 |
| CP | Year-1 profit for period (original) | 25267168000 | 6316792000 |

### 2261.HK (9 cells)

| col | header | before | after |
|---|---|---|---|
| BC | Comments (nearest sales& profit adjustment facto | 1 | 0.25 |
| CI | Year-3 financial period start | 2023-04-01 | 2024-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2024-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2025-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2025-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2026-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 603264000 | 150816000 |
| CO | Year-1 profit before tax (original) | -219528000 | -54882000 |
| CP | Year-1 profit for period (original) | -219528000 | -54882000 |

### 3223.HK (9 cells)

| col | header | before | after |
|---|---|---|---|
| BC | Comments (nearest sales& profit adjustment facto | 1 | 0.25 |
| CI | Year-3 financial period start | 2023-04-01 | 2024-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2024-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2025-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2025-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2026-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 6239068000 | 1559767000 |
| CO | Year-1 profit before tax (original) | 1454048000 | 363512000 |
| CP | Year-1 profit for period (original) | 1281392000 | 320348000 |

### 0625.HK (9 cells)

| col | header | before | after |
|---|---|---|---|
| BC | Comments (nearest sales& profit adjustment facto | 1 | 0.25 |
| CI | Year-3 financial period start | 2023-04-01 | 2024-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2024-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2025-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2025-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2026-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 36208000000 | 9052000000 |
| CO | Year-1 profit before tax (original) | -80000000 | -20000000 |
| CP | Year-1 profit for period (original) | -396000000 | -99000000 |

### 9615.HK (9 cells)

| col | header | before | after |
|---|---|---|---|
| BC | Comments (nearest sales& profit adjustment facto | 1 | 0.25 |
| CI | Year-3 financial period start | 2023-04-01 | 2024-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2024-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2025-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2025-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2026-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 427660000 | 106915000 |
| CO | Year-1 profit before tax (original) | -225504000 | -56376000 |
| CP | Year-1 profit for period (original) | -227308000 | -56827000 |

### 2041.HK (9 cells)

| col | header | before | after |
|---|---|---|---|
| BC | Comments (nearest sales& profit adjustment facto | 1 | 0.25 |
| CI | Year-3 financial period start | 2023-04-01 | 2024-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2024-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2025-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2025-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2026-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 1689288000 | 422322000 |
| CO | Year-1 profit before tax (original) | 13324000 | 3331000 |
| CP | Year-1 profit for period (original) | -10108000 | -2527000 |

### 9976.HK (9 cells)

| col | header | before | after |
|---|---|---|---|
| BC | Comments (nearest sales& profit adjustment facto | 1 | 0.333333 |
| CI | Year-3 financial period start | 2023-05-01 | 2024-01-01 |
| CJ | Year-3 financial period end | 2024-04-30 | 2024-12-31 |
| CK | Year-2 financial period start | 2024-05-01 | 2025-01-01 |
| CL | Year-2 financial period end | 2025-04-30 | 2025-12-31 |
| CM | Year-1 financial period start | 2025-05-01 | 2026-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 44119863000 | 14706621000 |
| CO | Year-1 profit before tax (original) | 23175585000 | 7725195000 |
| CP | Year-1 profit for period (original) | 19281489000 | 6427163000 |

### 3231.HK (9 cells)

| col | header | before | after |
|---|---|---|---|
| BC | Comments (nearest sales& profit adjustment facto | 1 | 0.25 |
| CI | Year-3 financial period start | 2023-04-01 | 2024-01-01 |
| CJ | Year-3 financial period end | 2024-03-31 | 2024-12-31 |
| CK | Year-2 financial period start | 2024-04-01 | 2025-01-01 |
| CL | Year-2 financial period end | 2025-03-31 | 2025-12-31 |
| CM | Year-1 financial period start | 2025-04-01 | 2026-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 306052000 | 76513000 |
| CO | Year-1 profit before tax (original) | -124932000 | -31233000 |
| CP | Year-1 profit for period (original) | -124864000 | -31216000 |

### 6727.HK (36 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 1792864000 | 1396259000 |
| AA | total assets in year-2 | 1396259000 | 1178048000 |
| AB | total assets in year-1 | 1178048000 | 1084165000 |
| AC | total equity in year-3 | 1439834000 | 1094441000 |
| AD | total equity in year-2 | 1094441000 | 862512000 |
| AE | total equity in year-1 | 862512000 | 806513000 |
| AF | total liability in year-3 | 353030000 | 301818000 |
| AG | total liability in year-2 | 301818000 | 315536000 |
| AH | total liability in year-1 | 315536000 | 277652000 |
| AI | Net sales in year-3 | 490533000 | 370755000 |
| AJ | Net sales in year-2 | 370755000 | 447069000 |
| AK | Net sales in year-1 | 447069000 | 324968000 |
| AL | Profit before tax in year-3 | -289168000 | -344281000 |
| AM | Profit before tax in year-2 | -344281000 | -245156000 |
| AN | Profit before tax in year-1 | -245156000 | -223996000 |
| AO | Profit for the year in year-3 | -289168000 | -344281000 |
| AP | Profit for the year in year-2 | -344281000 | -245170000 |
| AQ | Profit for the year in year-1 | -245170000 | -223996000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2025-12-31 | 2026-03-31 |
| AX | Operating cash flow in year-1 (before annualizat | -109650000 | -59320000 |
| AY | Cash and cash equivalents at year-1 end | 353951000 | 242910000 |
| AZ | R&D expensed in year-1 (before annualization) | 204061000 | 46160000 |
| BA | Development costs capitalized in year-1 (additio | 46472000 | 9588000 |
| BB | Top 5 customers (% of year-1 revenue) | 0.222 | 0.348 |
| BC | Comments (nearest sales& profit adjustment facto | 1 | 0.25 |
| BR | Interest-bearing debt at year-1 end | 30036000 | 21764000 |
| CI | Year-3 financial period start | 2023-01-01 | 2024-01-01 |
| CJ | Year-3 financial period end | 2023-12-31 | 2024-12-31 |
| CK | Year-2 financial period start | 2024-01-01 | 2025-01-01 |
| CL | Year-2 financial period end | 2024-12-31 | 2025-12-31 |
| CM | Year-1 financial period start | 2025-01-01 | 2026-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 447069000 | 81242000 |
| CO | Year-1 profit before tax (original) | -245156000 | -55999000 |
| CP | Year-1 profit for period (original) | -245170000 | -55999000 |
| CT | Gross profit in year-1 | 236010000 | 33635000 |
| CU | Capital expenditure in year-1 | 47400000 | 7700000 |

### 9856.HK (36 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 5480854000 | 7759869000 |
| AA | total assets in year-2 | 7759869000 | 7743144000 |
| AB | total assets in year-1 | 7743144000 | 11009094000 |
| AC | total equity in year-3 | 1933574000 | 1928276000 |
| AD | total equity in year-2 | 1928276000 | 3757722000 |
| AE | total equity in year-1 | 3757722000 | 4387859000 |
| AF | total liability in year-3 | 3547280000 | 5831593000 |
| AG | total liability in year-2 | 5831593000 | 3985422000 |
| AH | total liability in year-1 | 3985422000 | 6621235000 |
| AI | Net sales in year-3 | 4238989000 | 5086600000 |
| AJ | Net sales in year-2 | 5086600000 | 8354680000 |
| AK | Net sales in year-1 | 8354680000 | 10785296000 |
| AL | Profit before tax in year-3 | 242499000 | 98399000 |
| AM | Profit before tax in year-2 | 98399000 | 921584000 |
| AN | Profit before tax in year-1 | 921584000 | 1587864000 |
| AO | Profit for the year in year-3 | 215521000 | 89490000 |
| AP | Profit for the year in year-2 | 89490000 | 872640000 |
| AQ | Profit for the year in year-1 | 872640000 | 1321982000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2025-12-31 | 2026-06-30 |
| AX | Operating cash flow in year-1 (before annualizat | 1388382000 | -1256318000 |
| AY | Cash and cash equivalents at year-1 end | 1273617000 | 1584152000 |
| AZ | R&D expensed in year-1 (before annualization) | 663730000 | 319973000 |
| BA | Development costs capitalized in year-1 (additio | NaN | 0 |
| BB | Top 5 customers (% of year-1 revenue) | 0.702 | 0.718 |
| BC | Comments (nearest sales& profit adjustment facto | 1 | 0.5 |
| BR | Interest-bearing debt at year-1 end | 87221000 | 1871082000 |
| CI | Year-3 financial period start | 2023-01-01 | 2024-01-01 |
| CJ | Year-3 financial period end | 2023-12-31 | 2024-12-31 |
| CK | Year-2 financial period start | 2024-01-01 | 2025-01-01 |
| CL | Year-2 financial period end | 2024-12-31 | 2025-12-31 |
| CM | Year-1 financial period start | 2025-01-01 | 2026-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 8354680000 | 5392648000 |
| CO | Year-1 profit before tax (original) | 921584000 | 793932000 |
| CP | Year-1 profit for period (original) | 872640000 | 660991000 |
| CT | Gross profit in year-1 | 1672231000 | 1306050000 |
| CU | Capital expenditure in year-1 | 353359000 | 562574000 |

### 3228.HK (36 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 17230732000 | 19243777000 |
| AA | total assets in year-2 | 19243777000 | 23726909000 |
| AB | total assets in year-1 | 23726909000 | 26473789000 |
| AC | total equity in year-3 | 8970220000 | 11497706000 |
| AD | total equity in year-2 | 11497706000 | 13269792000 |
| AE | total equity in year-1 | 13269792000 | 13077545000 |
| AF | total liability in year-3 | 8260512000 | 7746071000 |
| AG | total liability in year-2 | 7746071000 | 10457117000 |
| AH | total liability in year-1 | 10457117000 | 13396244000 |
| AI | Net sales in year-3 | 10757302000 | 12659373000 |
| AJ | Net sales in year-2 | 12659373000 | 15308052000 |
| AK | Net sales in year-1 | 15308052000 | 16024176000 |
| AL | Profit before tax in year-3 | 1047530000 | 1320439000 |
| AM | Profit before tax in year-2 | 1320439000 | 1464383000 |
| AN | Profit before tax in year-1 | 1464383000 | 1013688000 |
| AO | Profit for the year in year-3 | 911029000 | 1160208000 |
| AP | Profit for the year in year-2 | 1160208000 | 1244018000 |
| AQ | Profit for the year in year-1 | 1244018000 | 950757000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2025-12-31 | 2026-04-30 |
| AX | Operating cash flow in year-1 (before annualizat | 1931225000 | 493389000 |
| AY | Cash and cash equivalents at year-1 end | 1941199000 | 2910922000 |
| AZ | R&D expensed in year-1 (before annualization) | 929932000 | 280739000 |
| BA | Development costs capitalized in year-1 (additio | NaN | 0 |
| BB | Top 5 customers (% of year-1 revenue) | 0.236 | 0.261 |
| BC | Comments (nearest sales& profit adjustment facto | 1 | 0.333333 |
| BR | Interest-bearing debt at year-1 end | 2484620000 | 4824612000 |
| CI | Year-3 financial period start | 2023-01-01 | 2024-01-01 |
| CJ | Year-3 financial period end | 2023-12-31 | 2024-12-31 |
| CK | Year-2 financial period start | 2024-01-01 | 2025-01-01 |
| CL | Year-2 financial period end | 2024-12-31 | 2025-12-31 |
| CM | Year-1 financial period start | 2025-01-01 | 2026-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 15308052000 | 5341392000 |
| CO | Year-1 profit before tax (original) | 1464383000 | 337896000 |
| CP | Year-1 profit for period (original) | 1244018000 | 316919000 |
| CT | Gross profit in year-1 | 3304889000 | 1001200000 |
| CU | Capital expenditure in year-1 | 2762785000 | 2071706000 |

### 3757.HK (36 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 2567380000 | 2365282000 |
| AA | total assets in year-2 | 2365282000 | 4311760000 |
| AB | total assets in year-1 | 4311760000 | 4410517000 |
| AC | total equity in year-3 | 980267000 | 1004936000 |
| AD | total equity in year-2 | 1004936000 | 2337424000 |
| AE | total equity in year-1 | 2337424000 | 2254705000 |
| AF | total liability in year-3 | 1587113000 | 1360346000 |
| AG | total liability in year-2 | 1360346000 | 1974336000 |
| AH | total liability in year-1 | 1974336000 | 2155812000 |
| AI | Net sales in year-3 | 1569649000 | 1104248000 |
| AJ | Net sales in year-2 | 1104248000 | 948838000 |
| AK | Net sales in year-1 | 948838000 | 595665000 |
| AL | Profit before tax in year-3 | 85322000 | 60431000 |
| AM | Profit before tax in year-2 | 60431000 | -50421000 |
| AN | Profit before tax in year-1 | -50421000 | -238773000 |
| AO | Profit for the year in year-3 | 79469000 | 63176000 |
| AP | Profit for the year in year-2 | 63176000 | -44956000 |
| AQ | Profit for the year in year-1 | -44956000 | -224028000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2025-12-31 | 2026-04-30 |
| AX | Operating cash flow in year-1 (before annualizat | 207794000 | 93866000 |
| AY | Cash and cash equivalents at year-1 end | 263662000 | 334749000 |
| AZ | R&D expensed in year-1 (before annualization) | 106267000 | 54428000 |
| BA | Development costs capitalized in year-1 (additio | NaN | 0 |
| BB | Top 5 customers (% of year-1 revenue) | 0.632 | 0.642 |
| BC | Comments (nearest sales& profit adjustment facto | 1 | 0.333333 |
| BR | Interest-bearing debt at year-1 end | 1325484000 | 1376881000 |
| CI | Year-3 financial period start | 2023-01-01 | 2024-01-01 |
| CJ | Year-3 financial period end | 2023-12-31 | 2024-12-31 |
| CK | Year-2 financial period start | 2024-01-01 | 2025-01-01 |
| CL | Year-2 financial period end | 2024-12-31 | 2025-12-31 |
| CM | Year-1 financial period start | 2025-01-01 | 2026-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 948838000 | 198555000 |
| CO | Year-1 profit before tax (original) | -50421000 | -79591000 |
| CP | Year-1 profit for period (original) | -44956000 | -74676000 |
| CT | Gross profit in year-1 | 327527000 | 63806000 |
| CU | Capital expenditure in year-1 | 43100000 | 68195000 |

### 6731.HK (36 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 39542000 | 101183000 |
| AA | total assets in year-2 | 101183000 | 545731000 |
| AB | total assets in year-1 | 545731000 | 655840000 |
| AC | total equity in year-3 | -120366000 | -198609000 |
| AD | total equity in year-2 | -198609000 | -1019357000 |
| AE | total equity in year-1 | -1019357000 | -1347370000 |
| AF | total liability in year-3 | 159908000 | 299792000 |
| AG | total liability in year-2 | 299792000 | 1565088000 |
| AH | total liability in year-1 | 1565088000 | 2003210000 |
| AI | Net sales in year-3 | 17538000 | 79802000 |
| AJ | Net sales in year-2 | 79802000 | 281715000 |
| AK | Net sales in year-1 | 281715000 | 400590000 |
| AL | Profit before tax in year-3 | -75585000 | -93735000 |
| AM | Profit before tax in year-2 | -93735000 | -880977000 |
| AN | Profit before tax in year-1 | -880977000 | -781464000 |
| AO | Profit for the year in year-3 | -75585000 | -93735000 |
| AP | Profit for the year in year-2 | -93735000 | -880977000 |
| AQ | Profit for the year in year-1 | -880977000 | -781464000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2025-12-31 | 2026-06-30 |
| AX | Operating cash flow in year-1 (before annualizat | -69563000 | -64795000 |
| AY | Cash and cash equivalents at year-1 end | 353871000 | 293522000 |
| AZ | R&D expensed in year-1 (before annualization) | 55437000 | 53587000 |
| BA | Development costs capitalized in year-1 (additio | NaN | 0 |
| BB | Top 5 customers (% of year-1 revenue) | 0.857 | 0.813 |
| BC | Comments (nearest sales& profit adjustment facto | 1 | 0.5 |
| BR | Interest-bearing debt at year-1 end | 44778000 | 51349000 |
| CI | Year-3 financial period start | 2023-01-01 | 2024-01-01 |
| CJ | Year-3 financial period end | 2023-12-31 | 2024-12-31 |
| CK | Year-2 financial period start | 2024-01-01 | 2025-01-01 |
| CL | Year-2 financial period end | 2024-12-31 | 2025-12-31 |
| CM | Year-1 financial period start | 2025-01-01 | 2026-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 281715000 | 200295000 |
| CO | Year-1 profit before tax (original) | -880977000 | -390732000 |
| CP | Year-1 profit for period (original) | -880977000 | -390732000 |
| CT | Gross profit in year-1 | 60585000 | 41407000 |
| CU | Capital expenditure in year-1 | 16400000 | 12969000 |

### 9607.HK (36 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 7333905000 | 8409127000 |
| AA | total assets in year-2 | 8409127000 | 9218735000 |
| AB | total assets in year-1 | 9218735000 | 9531055000 |
| AC | total equity in year-3 | 3504896000 | 3459330000 |
| AD | total equity in year-2 | 3459330000 | 4258691000 |
| AE | total equity in year-1 | 4258691000 | 4316949000 |
| AF | total liability in year-3 | 3829009000 | 4949797000 |
| AG | total liability in year-2 | 4949797000 | 4960044000 |
| AH | total liability in year-1 | 4960044000 | 5214106000 |
| AI | Net sales in year-3 | 2937334000 | 3263380000 |
| AJ | Net sales in year-2 | 3263380000 | 3420577000 |
| AK | Net sales in year-1 | 3420577000 | 4266128000 |
| AL | Profit before tax in year-3 | 426985000 | 550166000 |
| AM | Profit before tax in year-2 | 550166000 | 600950000 |
| AN | Profit before tax in year-1 | 600950000 | 807952000 |
| AO | Profit for the year in year-3 | 404118000 | 534185000 |
| AP | Profit for the year in year-2 | 534185000 | 577261000 |
| AQ | Profit for the year in year-1 | 577261000 | 778192000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2025-12-31 | 2026-06-30 |
| AX | Operating cash flow in year-1 (before annualizat | 262272000 | 36546000 |
| AY | Cash and cash equivalents at year-1 end | 476150000 | 435686000 |
| AZ | R&D expensed in year-1 (before annualization) | 232512000 | 118384000 |
| BA | Development costs capitalized in year-1 (additio | NaN | 0 |
| BB | Top 5 customers (% of year-1 revenue) | 0.298 | 0.291 |
| BC | Comments (nearest sales& profit adjustment facto | 1 | 0.5 |
| BR | Interest-bearing debt at year-1 end | 3790340000 | 4118228000 |
| CI | Year-3 financial period start | 2023-01-01 | 2024-01-01 |
| CJ | Year-3 financial period end | 2023-12-31 | 2024-12-31 |
| CK | Year-2 financial period start | 2024-01-01 | 2025-01-01 |
| CL | Year-2 financial period end | 2024-12-31 | 2025-12-31 |
| CM | Year-1 financial period start | 2025-01-01 | 2026-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 3420577000 | 2133064000 |
| CO | Year-1 profit before tax (original) | 600950000 | 403976000 |
| CP | Year-1 profit for period (original) | 577261000 | 389096000 |
| CT | Gross profit in year-1 | 813592000 | 487429000 |
| CU | Capital expenditure in year-1 | 313375000 | 257691000 |

### 6802.HK (36 cells)

| col | header | before | after |
|---|---|---|---|
| Z | total assets in year-3 (3 years before IPO) | 336334000 | 407914000 |
| AA | total assets in year-2 | 407914000 | 483591000 |
| AB | total assets in year-1 | 483591000 | 557073000 |
| AC | total equity in year-3 | 249615000 | 277626000 |
| AD | total equity in year-2 | 277626000 | 327402000 |
| AE | total equity in year-1 | 327402000 | 336828000 |
| AF | total liability in year-3 | 86719000 | 130288000 |
| AG | total liability in year-2 | 130288000 | 156189000 |
| AH | total liability in year-1 | 156189000 | 220245000 |
| AI | Net sales in year-3 | 332107000 | 433324000 |
| AJ | Net sales in year-2 | 433324000 | 613523000 |
| AK | Net sales in year-1 | 613523000 | 783676000 |
| AL | Profit before tax in year-3 | -883000 | -31360000 |
| AM | Profit before tax in year-2 | -31360000 | 2201000 |
| AN | Profit before tax in year-1 | 2201000 | 31028000 |
| AO | Profit for the year in year-3 | -883000 | -31375000 |
| AP | Profit for the year in year-2 | -31375000 | 2201000 |
| AQ | Profit for the year in year-1 | 2201000 | 31028000 |
| AW | Year-1 financial period end (dd/mm/yy) | 2025-12-31 | 2026-03-31 |
| AX | Operating cash flow in year-1 (before annualizat | -9038000 | -5319000 |
| AY | Cash and cash equivalents at year-1 end | 12123000 | 26314000 |
| AZ | R&D expensed in year-1 (before annualization) | 59367000 | 14813000 |
| BA | Development costs capitalized in year-1 (additio | NaN | 0 |
| BB | Top 5 customers (% of year-1 revenue) | 0.804 | 0.856 |
| BC | Comments (nearest sales& profit adjustment facto | 1 | 0.25 |
| BR | Interest-bearing debt at year-1 end | 28900000 | 27820000 |
| CI | Year-3 financial period start | 2023-01-01 | 2024-01-01 |
| CJ | Year-3 financial period end | 2023-12-31 | 2024-12-31 |
| CK | Year-2 financial period start | 2024-01-01 | 2025-01-01 |
| CL | Year-2 financial period end | 2024-12-31 | 2025-12-31 |
| CM | Year-1 financial period start | 2025-01-01 | 2026-01-01 |
| CN | Year-1 net sales (original, pre-annualization) | 613523000 | 195919000 |
| CO | Year-1 profit before tax (original) | 2201000 | 7757000 |
| CP | Year-1 profit for period (original) | 2201000 | 7757000 |
| CT | Gross profit in year-1 | 100989000 | 37580000 |
| CU | Capital expenditure in year-1 | 16511000 | 3312000 |

