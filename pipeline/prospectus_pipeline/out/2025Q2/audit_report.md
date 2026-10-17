# HK IPO Excel vs JSON 逐格对账与数据质量审计报告

> **生成时间**：2026-10-17 09:53:27  
> **目标工作簿**：`cohorts/HKIPO-MB2025Q2.xlsx` (Sheet: `NLR`)  
> **审计范围**：27 家公司 × (70 招股书字段 + 18 配发字段 = 88 字段，共 2,376 个单元格) + 103 个外部工具字段  

## 一、核心审计结论汇总

| 数据类别 | 字段数 | 审计总格数 | 一致匹配格数 | Excel 缺失 | JSON 缺失 | 数值/格式差异 | 匹配率 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **招股书字段** | 70 | 1890 | 1890 | 0 | 0 | 0 | **100.00%** |
| **配发公告字段** | 18 | 486 | 486 | 0 | 0 | 0 | **100.00%** |
| **合计 (88 字段)** | 88 | 2376 | 2376 | 0 | 0 | 0 | **100.00%** |

### 关键发现点：
1. **总单元格数**：2376 个，匹配格数：2376（匹配率：100.00%）；
2. **差异统计**：Excel 缺失 0 项，JSON 缺失 0 项，数值不匹配 0 项；
   其中匹配格内有 173 格两边均缺失，不是已核实的证据，不能计入证据覆盖率；
3. **外部/工具衍生字段**：共 103 列；全量填报 94 列，部分填报 5 列，未填报或仅有缺失占位 4 列。此统计与上方 88 字段逐格对账是不同范围。

## 二、差异明细清单 (Discrepancies)

✅ **未发现任何字段差异，所有单元格均完全一致！**

## 三、103 个外部/工具衍生字段填报审计

| 列 | 字段说明 | 对应生成工具 | 填报数 / 总数 | 填报率 | 抽样值 |
|---|---|---|---:|---:|---|
| `V` | Filing price revision (%) | `src/academic_derivations.py (Pricing revision)` | 27/27 | 100.0% | `0` |
| `W` | Filing range width (%) | `src/academic_derivations.py (Filing range width)` | 27/27 | 100.0% | `0` |
| `X` | Pricing position in filing ran | `src/academic_derivations.py (Pricing position in range)` | 27/27 | 100.0% | `Fixed price` |
| `BC` | Comments (nearest sales& profi | `Manual / Prospectus disclosure notes (Annualization factor)` | 27/27 | 100.0% | `1` |
| `BU` | Listing board | `tools/external/flags.py (Listing board)` | 27/27 | 100.0% | `Main Board` |
| `BW` | A+H issuer flag | `tools/external/flags.py (A+H flag)` | 27/27 | 100.0% | `0` |
| `BX` | WVR flag | `tools/external/flags.py (WVR flag)` | 27/27 | 100.0% | `0` |
| `BY` | Chapter 18A flag | `tools/external/flags.py (Chapter 18A flag)` | 27/27 | 100.0% | `0` |
| `BZ` | Chapter 18C flag | `tools/external/flags.py (Chapter 18C flag)` | 27/27 | 100.0% | `0` |
| `CA` | Industry classification code | `tools/external/hsic_codes.py (Industry classification code)` | 27/27 | 100.0% | `101070` |
| `CB` | Industry classification system | `tools/external/hsic_codes.py (Industry classification system)` | 27/27 | 100.0% | `HSICS (Hang Seng Industry` |
| `CD` | Firm age at IPO (years) | `src/academic_derivations.py (Firm age at IPO)` | 27/27 | 100.0% | `6.13` |
| `CE` | Place of incorporation | `tools/external/flags.py (Place of incorporation)` | 24/27 | 88.9% | `PRC` |
| `CG` | Financial statement unit multi | `Manual / Disclosure notes (Financial statement unit multiplier)` | 27/27 | 100.0% | `1000` |
| `CI` | Year-3 financial period start | `Manual / Disclosure notes (Financial period: Year-3 start)` | 27/27 | 100.0% | `2022-01-01` |
| `CJ` | Year-3 financial period end | `Manual / Disclosure notes (Financial period: Year-3 end)` | 27/27 | 100.0% | `2022-12-31` |
| `CK` | Year-2 financial period start | `Manual / Disclosure notes (Financial period: Year-2 start)` | 27/27 | 100.0% | `2023-01-01` |
| `CL` | Year-2 financial period end | `Manual / Disclosure notes (Financial period: Year-2 end)` | 27/27 | 100.0% | `2023-12-31` |
| `CM` | Year-1 financial period start | `Manual / Disclosure notes (Financial period: Year-1 start)` | 27/27 | 100.0% | `2024-01-01` |
| `CN` | Year-1 net sales (original, pr | `Manual / Disclosure notes (Financial: Year-1 net sales original)` | 27/27 | 100.0% | `5130317000` |
| `CO` | Year-1 profit before tax (orig | `Manual / Disclosure notes (Financial: Year-1 profit before tax original)` | 27/27 | 100.0% | `79043000` |
| `CP` | Year-1 profit for period (orig | `Manual / Disclosure notes (Financial: Year-1 profit for period original)` | 27/27 | 100.0% | `91014000` |
| `CZ` | Earliest cornerstone unlock da | `tools/external/flags.py / src/cornerstone.py (Earliest cornerstone unlock date)` | 25/27 | 92.6% | `2025-10-14` |
| `DK` | Greenshoe exercise rate (%) | `src/academic_derivations.py (Greenshoe exercise rate)` | 27/27 | 100.0% | `0` |
| `DS` | HSI return over 20 trading day | `tools/external/market.py (HSI 20-day return)` | 27/27 | 100.0% | `-0.01660077` |
| `DT` | HK ordinary IPO count in 90 ca | `tools/external/ipo_count.py (90-day HK ordinary IPO count)` | 27/27 | 100.0% | `15` |
| `DU` | 1-month HIBOR before prospectu | `tools/external/hkma_import.py (1-month HIBOR)` | 27/27 | 100.0% | `0.034872` |
| `DV` | Banking system aggregate balan | `tools/external/hkma_import.py (Aggregate Balance)` | 27/27 | 100.0% | `44694000000` |
| `DW` | First trading day closing pric | `tools/external/market.py (First day close)` | 27/27 | 100.0% | `8.39` |
| `DX` | First-day return / Underpricin | `src/academic_derivations.py (First-day return / Underpricing)` | 27/27 | 100.0% | `0.01451` |
| `DY` | Money left on the table (HK$) | `src/academic_derivations.py (Money left on the table)` | 27/27 | 100.0% | `14582844` |
| `DZ` | First trading day opening pric | `tools/external/market.py (First day open)` | 27/27 | 100.0% | `8.46` |
| `EA` | First trading day high (HK$) | `tools/external/market.py (First day high)` | 27/27 | 100.0% | `8.46` |
| `EB` | First trading day low (HK$) | `tools/external/market.py (First day low)` | 27/27 | 100.0% | `8.33` |
| `EC` | First trading day volume (shar | `tools/external/market.py (First day volume)` | 27/27 | 100.0% | `3230400` |
| `ED` | First-day flipping ratio (%) | `src/academic_derivations.py (First-day flipping ratio)` | 27/27 | 100.0% | `0.026582` |
| `EE` | First trading day turnover (HK | `tools/external/market.py (First day turnover)` | 27/27 | 100.0% | `27167900` |
| `EF` | Offer mechanism | `tools/external/rules.py (Offer mechanism)` | 27/27 | 100.0% | `PN18 statutory clawback` |
| `EG` | Applicable IPO rules / transit | `tools/external/rules.py (Applicable IPO rules)` | 27/27 | 100.0% | `FINI (from 22/11/2023)` |
| `EI` | Current listing status | `tools/external/aftermarket.py (Current listing status)` | 27/27 | 100.0% | `Active` |
| `EJ` | 1-month post-IPO close price ( | `tools/external/aftermarket.py (1-month close price)` | 27/27 | 100.0% | `9.61` |
| `EK` | 1-month BHR from Day-1 close ( | `tools/external/aftermarket.py (1-month BHR)` | 27/27 | 100.0% | `0.145411` |
| `EL` | 1-month total return from offe | `tools/external/aftermarket.py (1-month total return)` | 27/27 | 100.0% | `0.162031` |
| `EM` | 1-month HSI return (%) | `tools/external/aftermarket.py (1-month HSI return)` | 27/27 | 100.0% | `0.095052` |
| `EN` | 1-month HSTECH return (%) | `tools/external/aftermarket.py (1-month HSTECH return)` | 27/27 | 100.0% | `0.056374` |
| `EO` | 1-month wealth relative vs HSI | `tools/external/aftermarket.py (1-month WR vs HSI)` | 27/27 | 100.0% | `1.046` |
| `EP` | 1-month wealth relative vs HST | `tools/external/aftermarket.py (1-month WR vs HSTECH)` | 27/27 | 100.0% | `1.0843` |
| `EQ` | 1-month average daily turnover | `tools/external/aftermarket.py (1-month average daily turnover)` | 27/27 | 100.0% | `12683475` |
| `ER` | 6-month post-IPO close price ( | `tools/external/aftermarket.py (6-month close price)` | 27/27 | 100.0% | `11.86` |
| `ES` | 6-month BHR from Day-1 close ( | `tools/external/aftermarket.py (6-month BHR)` | 27/27 | 100.0% | `0.413588` |
| `ET` | 6-month total return from offe | `tools/external/aftermarket.py (6-month total return)` | 27/27 | 100.0% | `0.434099` |
| `EU` | 6-month HSI return (%) | `tools/external/aftermarket.py (6-month HSI return)` | 27/27 | 100.0% | `0.187882` |
| `EV` | 6-month HSTECH return (%) | `tools/external/aftermarket.py (6-month HSTECH return)` | 27/27 | 100.0% | `0.18108` |
| `EW` | 6-month wealth relative vs HSI | `tools/external/aftermarket.py (6-month WR vs HSI)` | 27/27 | 100.0% | `1.19` |
| `EX` | 6-month wealth relative vs HST | `tools/external/aftermarket.py (6-month WR vs HSTECH)` | 27/27 | 100.0% | `1.1969` |
| `EY` | 6-month average daily turnover | `tools/external/aftermarket.py (6-month average daily turnover)` | 27/27 | 100.0% | `108347715` |
| `EZ` | Liquidity decay ratio (6M vs D | `tools/external/aftermarket.py (Liquidity decay ratio)` | 27/27 | 100.0% | `3.988078` |
| `FA` | 1-year post-IPO return (%) [Re | `tools/external/aftermarket.py (1-year return [Reserved])` | 0/27 | 0.0% | `—` |
| `FB` | 1-year wealth relative vs HSI  | `tools/external/aftermarket.py (1-year WR vs HSI [Reserved])` | 0/27 | 0.0% | `—` |
| `FC` | 3-year post-IPO return (%) [Re | `tools/external/aftermarket.py (3-year return [Reserved])` | 0/27 | 0.0% | `—` |
| `FD` | 3-year wealth relative vs HSI  | `tools/external/aftermarket.py (3-year WR vs HSI [Reserved])` | 0/27 | 0.0% | `—` |
| `FE` | 18A/18C regulatory milestone s | `tools/external/aftermarket.py (18A/18C regulatory status)` | 27/27 | 100.0% | `Standard` |
| `FF` | Stabilizing manager | `src/write_back_expansion.py (Stabilizing manager)` | 27/27 | 100.0% | `China International Capit` |
| `FG` | Stabilization period end date | `src/write_back_expansion.py (Stabilization period end date)` | 27/27 | 100.0% | `2025-05-14` |
| `FH` | Stabilization purchases occurr | `src/write_back_expansion.py (Stabilization purchases occurred)` | 27/27 | 100.0% | `0` |
| `FI` | Over-allocation shares | `src/write_back_expansion.py (Over-allocation shares)` | 27/27 | 100.0% | `0` |
| `FJ` | Over-allocation (% of base off | `src/write_back_expansion.py (Over-allocation pct)` | 27/27 | 100.0% | `0.15` |
| `FK` | Over-allotment option exercise | `src/write_back_expansion.py (Over-allotment exercise date)` | 27/27 | 100.0% | `2025-05-14` |
| `FL` | Shares issued under over-allot | `src/write_back_expansion.py (Shares issued under option)` | 27/27 | 100.0% | `0` |
| `FM` | Over-allotment exercise percen | `src/write_back_expansion.py (Over-allotment exercise percentage)` | 27/27 | 100.0% | `0` |
| `FN` | Post-stabilization cliff retur | `src/write_back_expansion.py (Cliff return m5 p5)` | 27/27 | 100.0% | `0.075792` |
| `FO` | Post-stabilization 20-day retu | `src/write_back_expansion.py (Post-stabilization return p20)` | 27/27 | 100.0% | `0.149028` |
| `FP` | Post-stabilization volume deca | `src/write_back_expansion.py (Post-stabilization volume decay)` | 27/27 | 100.0% | `0.983436` |
| `FQ` | Day-5 BHR from Day-1 close (%) | `src/write_back_expansion.py (Day-5 BHR)` | 27/27 | 100.0% | `-0.014303` |
| `FR` | Day-5 wealth relative vs HSI | `src/write_back_expansion.py (Day-5 WR vs HSI)` | 27/27 | 100.0% | `0.9791` |
| `FS` | Day-20 BHR from Day-1 close (% | `src/write_back_expansion.py (Day-20 BHR)` | 27/27 | 100.0% | `0.145411` |
| `FT` | Day-20 wealth relative vs HSI | `src/write_back_expansion.py (Day-20 WR vs HSI)` | 27/27 | 100.0% | `1.046` |
| `FU` | 3-month BHR from Day-1 close ( | `src/write_back_expansion.py (3-month BHR)` | 27/27 | 100.0% | `0.239571` |
| `FV` | 3-month wealth relative vs HSI | `src/write_back_expansion.py (3-month WR vs HSI)` | 27/27 | 100.0% | `1.0828` |
| `FW` | 3-month wealth relative vs HST | `src/write_back_expansion.py (3-month WR vs HSTECH)` | 27/27 | 100.0% | `1.1473` |
| `FX` | 3-month average daily turnover | `src/write_back_expansion.py (3-month avg daily turnover)` | 27/27 | 100.0% | `10863488.89` |
| `FY` | Amihud illiquidity (6M mean) | `src/write_back_expansion.py (Amihud illiquidity 6M mean)` | 27/27 | 100.0% | `0.001177285714285714` |
| `FZ` | Zero-volume days count (first  | `src/write_back_expansion.py (Zero-volume days count 6M)` | 27/27 | 100.0% | `0` |
| `GA` | Return volatility (first 6M da | `src/write_back_expansion.py (Return volatility 6M)` | 27/27 | 100.0% | `0.02702259469376962` |
| `GB` | Maximum drawdown (first 6M, %) | `src/write_back_expansion.py (Maximum drawdown 6M)` | 27/27 | 100.0% | `0.179508` |
| `GC` | Controlling shareholder 6-mont | `src/write_back_expansion.py (Controlling shareholder 6M disposal expiry)` | 27/27 | 100.0% | `2025-10-14` |
| `GD` | Controlling shareholder 12-mon | `src/write_back_expansion.py (Controlling shareholder 12M control expiry)` | 27/27 | 100.0% | `2026-04-14` |
| `GE` | Cornerstone unlock CAR [-5, +5 | `src/write_back_expansion.py (Cornerstone unlock CAR m5 p5)` | 25/27 | 92.6% | `-0.104706` |
| `GF` | Cornerstone unlock CAR [-20, + | `src/write_back_expansion.py (Cornerstone unlock CAR m20 p20)` | 25/27 | 92.6% | `-0.221232` |
| `GG` | Cornerstone unlock volume shoc | `src/write_back_expansion.py (Cornerstone unlock volume shock ratio)` | 25/27 | 92.6% | `0.4612` |
| `GH` | Lead sponsor name | `src/write_back_expansion.py (Lead sponsor name)` | 27/27 | 100.0% | `China International Capit` |
| `GI` | Joint sponsor count | `src/write_back_expansion.py (Joint sponsor count)` | 27/27 | 100.0% | `0` |
| `GJ` | Sponsor commercial bank affili | `src/write_back_expansion.py (Sponsor bank affiliate flag)` | 27/27 | 100.0% | `0` |
| `GK` | Underwriting base commission r | `src/write_back_expansion.py (Underwriting base commission rate)` | 27/27 | 100.0% | `0.025` |
| `GL` | Underwriting discretionary inc | `src/write_back_expansion.py (Underwriting incentive fee rate)` | 27/27 | 100.0% | `0.01` |
| `GM` | Total underwriting fee rate (% | `src/write_back_expansion.py (Total underwriting fee rate)` | 27/27 | 100.0% | `0.035` |
| `GN` | Cornerstone investor count | `src/write_back_expansion.py (Cornerstone investor count)` | 27/27 | 100.0% | `4` |
| `GO` | Cornerstone state-owned presen | `src/write_back_expansion.py (Cornerstone state-owned flag)` | 27/27 | 100.0% | `0` |
| `GP` | Crossover fund presence flag | `src/write_back_expansion.py (Crossover fund flag)` | 27/27 | 100.0% | `0` |
| `GQ` | Pre-IPO institutional investor | `src/write_back_expansion.py (Pre-IPO investor count)` | 27/27 | 100.0% | `6` |
| `GR` | Pre-IPO state-owned backing fl | `src/write_back_expansion.py (Pre-IPO state-owned flag)` | 27/27 | 100.0% | `0` |
| `GS` | FINI digital settlement regime | `src/write_back_expansion.py (FINI digital settlement regime)` | 27/27 | 100.0% | `POST_FINI` |
| `GT` | 2025 pricing reform regime | `src/write_back_expansion.py (2025 pricing reform regime)` | 27/27 | 100.0% | `PRE_2025_REFORM` |

## 四、27 家公司流水线门禁状态 (Pipeline State)

| 股票代码 | 招股书 extracted | 招股书 validated | 招股书 reviewed | 配发 extracted | 配发 validated | 配发 reviewed | 当前写入状态 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| `1276.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `1333.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2050.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2508.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2565.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2573.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2589.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2603.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2605.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2609.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2617.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2619.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2621.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2629.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2643.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2865.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `3288.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `3677.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `3750.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `3880.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `6168.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `6603.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `6831.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `6883.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `9606.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `9678.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `9881.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
