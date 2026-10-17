# HK IPO Excel vs JSON 逐格对账与数据质量审计报告

> **生成时间**：2026-10-17 09:53:26  
> **目标工作簿**：`cohorts/HKIPO-MB2025Q1.xlsx` (Sheet: `NLR`)  
> **审计范围**：15 家公司 × (70 招股书字段 + 18 配发字段 = 88 字段，共 1,320 个单元格) + 103 个外部工具字段  

## 一、核心审计结论汇总

| 数据类别 | 字段数 | 审计总格数 | 一致匹配格数 | Excel 缺失 | JSON 缺失 | 数值/格式差异 | 匹配率 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **招股书字段** | 70 | 1050 | 1050 | 0 | 0 | 0 | **100.00%** |
| **配发公告字段** | 18 | 270 | 270 | 0 | 0 | 0 | **100.00%** |
| **合计 (88 字段)** | 88 | 1320 | 1320 | 0 | 0 | 0 | **100.00%** |

### 关键发现点：
1. **总单元格数**：1320 个，匹配格数：1320（匹配率：100.00%）；
2. **差异统计**：Excel 缺失 0 项，JSON 缺失 0 项，数值不匹配 0 项；
   其中匹配格内有 72 格两边均缺失，不是已核实的证据，不能计入证据覆盖率；
3. **外部/工具衍生字段**：共 103 列；全量填报 93 列，部分填报 6 列，未填报或仅有缺失占位 4 列。此统计与上方 88 字段逐格对账是不同范围。

## 二、差异明细清单 (Discrepancies)

✅ **未发现任何字段差异，所有单元格均完全一致！**

## 三、103 个外部/工具衍生字段填报审计

| 列 | 字段说明 | 对应生成工具 | 填报数 / 总数 | 填报率 | 抽样值 |
|---|---|---|---:|---:|---|
| `V` | Filing price revision (%) | `src/academic_derivations.py (Pricing revision)` | 15/15 | 100.0% | `0` |
| `W` | Filing range width (%) | `src/academic_derivations.py (Filing range width)` | 15/15 | 100.0% | `0` |
| `X` | Pricing position in filing ran | `src/academic_derivations.py (Pricing position in range)` | 15/15 | 100.0% | `Fixed price` |
| `BC` | Comments (nearest sales& profi | `Manual / Prospectus disclosure notes (Annualization factor)` | 15/15 | 100.0% | `0.5` |
| `BU` | Listing board | `tools/external/flags.py (Listing board)` | 15/15 | 100.0% | `Main Board` |
| `BW` | A+H issuer flag | `tools/external/flags.py (A+H flag)` | 15/15 | 100.0% | `0` |
| `BX` | WVR flag | `tools/external/flags.py (WVR flag)` | 15/15 | 100.0% | `0` |
| `BY` | Chapter 18A flag | `tools/external/flags.py (Chapter 18A flag)` | 15/15 | 100.0% | `1` |
| `BZ` | Chapter 18C flag | `tools/external/flags.py (Chapter 18C flag)` | 15/15 | 100.0% | `0` |
| `CA` | Industry classification code | `tools/external/hsic_codes.py (Industry classification code)` | 15/15 | 100.0% | `282020` |
| `CB` | Industry classification system | `tools/external/hsic_codes.py (Industry classification system)` | 15/15 | 100.0% | `HSICS (Hang Seng Industry` |
| `CD` | Firm age at IPO (years) | `src/academic_derivations.py (Firm age at IPO)` | 15/15 | 100.0% | `1.71` |
| `CE` | Place of incorporation | `tools/external/flags.py (Place of incorporation)` | 15/15 | 100.0% | `Cayman Islands` |
| `CG` | Financial statement unit multi | `Manual / Disclosure notes (Financial statement unit multiplier)` | 9/15 | 60.0% | `1000` |
| `CI` | Year-3 financial period start | `Manual / Disclosure notes (Financial period: Year-3 start)` | 15/15 | 100.0% | `2022-01-01` |
| `CJ` | Year-3 financial period end | `Manual / Disclosure notes (Financial period: Year-3 end)` | 15/15 | 100.0% | `2022-12-31` |
| `CK` | Year-2 financial period start | `Manual / Disclosure notes (Financial period: Year-2 start)` | 15/15 | 100.0% | `2023-01-01` |
| `CL` | Year-2 financial period end | `Manual / Disclosure notes (Financial period: Year-2 end)` | 15/15 | 100.0% | `2023-12-31` |
| `CM` | Year-1 financial period start | `Manual / Disclosure notes (Financial period: Year-1 start)` | 15/15 | 100.0% | `2024-01-01` |
| `CN` | Year-1 net sales (original, pr | `Manual / Disclosure notes (Financial: Year-1 net sales original)` | 13/15 | 86.7% | `51887000` |
| `CO` | Year-1 profit before tax (orig | `Manual / Disclosure notes (Financial: Year-1 profit before tax original)` | 15/15 | 100.0% | `-114389000` |
| `CP` | Year-1 profit for period (orig | `Manual / Disclosure notes (Financial: Year-1 profit for period original)` | 15/15 | 100.0% | `-114389000` |
| `CZ` | Earliest cornerstone unlock da | `tools/external/flags.py / src/cornerstone.py (Earliest cornerstone unlock date)` | 11/15 | 73.3% | `2025-07-08` |
| `DK` | Greenshoe exercise rate (%) | `src/academic_derivations.py (Greenshoe exercise rate)` | 15/15 | 100.0% | `0` |
| `DS` | HSI return over 20 trading day | `tools/external/market.py (HSI 20-day return)` | 15/15 | 100.0% | `0.0248598` |
| `DT` | HK ordinary IPO count in 90 ca | `tools/external/ipo_count.py (90-day HK ordinary IPO count)` | 15/15 | 100.0% | `22` |
| `DU` | 1-month HIBOR before prospectu | `tools/external/hkma_import.py (1-month HIBOR)` | 15/15 | 100.0% | `0.0458435` |
| `DV` | Banking system aggregate balan | `tools/external/hkma_import.py (Aggregate Balance)` | 15/15 | 100.0% | `45746000000` |
| `DW` | First trading day closing pric | `tools/external/market.py (First day close)` | 15/15 | 100.0% | `3.33` |
| `DX` | First-day return / Underpricin | `src/academic_derivations.py (First-day return / Underpricing)` | 15/15 | 100.0% | `0.034161` |
| `DY` | Money left on the table (HK$) | `src/academic_derivations.py (Money left on the table)` | 15/15 | 100.0% | `19922320` |
| `DZ` | First trading day opening pric | `tools/external/market.py (First day open)` | 15/15 | 100.0% | `3.22` |
| `EA` | First trading day high (HK$) | `tools/external/market.py (First day high)` | 15/15 | 100.0% | `3.49` |
| `EB` | First trading day low (HK$) | `tools/external/market.py (First day low)` | 15/15 | 100.0% | `3.13` |
| `EC` | First trading day volume (shar | `tools/external/market.py (First day volume)` | 15/15 | 100.0% | `18896100` |
| `ED` | First-day flipping ratio (%) | `src/academic_derivations.py (First-day flipping ratio)` | 15/15 | 100.0% | `0.104334` |
| `EE` | First trading day turnover (HK | `tools/external/market.py (First day turnover)` | 15/15 | 100.0% | `61637900` |
| `EF` | Offer mechanism | `tools/external/rules.py (Offer mechanism)` | 15/15 | 100.0% | `PN18 statutory clawback` |
| `EG` | Applicable IPO rules / transit | `tools/external/rules.py (Applicable IPO rules)` | 15/15 | 100.0% | `FINI (from 22/11/2023)` |
| `EI` | Current listing status | `tools/external/aftermarket.py (Current listing status)` | 15/15 | 100.0% | `Active` |
| `EJ` | 1-month post-IPO close price ( | `tools/external/aftermarket.py (1-month close price)` | 15/15 | 100.0% | `5.63` |
| `EK` | 1-month BHR from Day-1 close ( | `tools/external/aftermarket.py (1-month BHR)` | 15/15 | 100.0% | `0.690691` |
| `EL` | 1-month total return from offe | `tools/external/aftermarket.py (1-month total return)` | 15/15 | 100.0% | `0.748447` |
| `EM` | 1-month HSI return (%) | `tools/external/aftermarket.py (1-month HSI return)` | 15/15 | 100.0% | `0.096147` |
| `EN` | 1-month HSTECH return (%) | `tools/external/aftermarket.py (1-month HSTECH return)` | 15/15 | 100.0% | `0.195698` |
| `EO` | 1-month wealth relative vs HSI | `tools/external/aftermarket.py (1-month WR vs HSI)` | 15/15 | 100.0% | `1.5424` |
| `EP` | 1-month wealth relative vs HST | `tools/external/aftermarket.py (1-month WR vs HSTECH)` | 15/15 | 100.0% | `1.414` |
| `EQ` | 1-month average daily turnover | `tools/external/aftermarket.py (1-month average daily turnover)` | 15/15 | 100.0% | `11750145` |
| `ER` | 6-month post-IPO close price ( | `tools/external/aftermarket.py (6-month close price)` | 15/15 | 100.0% | `5.71` |
| `ES` | 6-month BHR from Day-1 close ( | `tools/external/aftermarket.py (6-month BHR)` | 15/15 | 100.0% | `0.714715` |
| `ET` | 6-month total return from offe | `tools/external/aftermarket.py (6-month total return)` | 15/15 | 100.0% | `0.773292` |
| `EU` | 6-month HSI return (%) | `tools/external/aftermarket.py (6-month HSI return)` | 15/15 | 100.0% | `0.252504` |
| `EV` | 6-month HSTECH return (%) | `tools/external/aftermarket.py (6-month HSTECH return)` | 15/15 | 100.0% | `0.236465` |
| `EW` | 6-month wealth relative vs HSI | `tools/external/aftermarket.py (6-month WR vs HSI)` | 15/15 | 100.0% | `1.369` |
| `EX` | 6-month wealth relative vs HST | `tools/external/aftermarket.py (6-month WR vs HSTECH)` | 15/15 | 100.0% | `1.3868` |
| `EY` | 6-month average daily turnover | `tools/external/aftermarket.py (6-month average daily turnover)` | 15/15 | 100.0% | `5200620` |
| `EZ` | Liquidity decay ratio (6M vs D | `tools/external/aftermarket.py (Liquidity decay ratio)` | 15/15 | 100.0% | `0.084374` |
| `FA` | 1-year post-IPO return (%) [Re | `tools/external/aftermarket.py (1-year return [Reserved])` | 0/15 | 0.0% | `—` |
| `FB` | 1-year wealth relative vs HSI  | `tools/external/aftermarket.py (1-year WR vs HSI [Reserved])` | 0/15 | 0.0% | `—` |
| `FC` | 3-year post-IPO return (%) [Re | `tools/external/aftermarket.py (3-year return [Reserved])` | 0/15 | 0.0% | `—` |
| `FD` | 3-year wealth relative vs HSI  | `tools/external/aftermarket.py (3-year WR vs HSI [Reserved])` | 0/15 | 0.0% | `—` |
| `FE` | 18A/18C regulatory milestone s | `tools/external/aftermarket.py (18A/18C regulatory status)` | 15/15 | 100.0% | `18A (Biotech / B-tag)` |
| `FF` | Stabilizing manager | `src/write_back_expansion.py (Stabilizing manager)` | 15/15 | 100.0% | `China International Capit` |
| `FG` | Stabilization period end date | `src/write_back_expansion.py (Stabilization period end date)` | 15/15 | 100.0% | `2025-02-07` |
| `FH` | Stabilization purchases occurr | `src/write_back_expansion.py (Stabilization purchases occurred)` | 15/15 | 100.0% | `0` |
| `FI` | Over-allocation shares | `src/write_back_expansion.py (Over-allocation shares)` | 15/15 | 100.0% | `0` |
| `FJ` | Over-allocation (% of base off | `src/write_back_expansion.py (Over-allocation pct)` | 15/15 | 100.0% | `0.15` |
| `FK` | Over-allotment option exercise | `src/write_back_expansion.py (Over-allotment exercise date)` | 15/15 | 100.0% | `2025-02-07` |
| `FL` | Shares issued under over-allot | `src/write_back_expansion.py (Shares issued under option)` | 15/15 | 100.0% | `0` |
| `FM` | Over-allotment exercise percen | `src/write_back_expansion.py (Over-allotment exercise percentage)` | 15/15 | 100.0% | `0` |
| `FN` | Post-stabilization cliff retur | `src/write_back_expansion.py (Cliff return m5 p5)` | 15/15 | 100.0% | `0.336364` |
| `FO` | Post-stabilization 20-day retu | `src/write_back_expansion.py (Post-stabilization return p20)` | 15/15 | 100.0% | `0.049734` |
| `FP` | Post-stabilization volume deca | `src/write_back_expansion.py (Post-stabilization volume decay)` | 15/15 | 100.0% | `0.458637` |
| `FQ` | Day-5 BHR from Day-1 close (%) | `src/write_back_expansion.py (Day-5 BHR)` | 15/15 | 100.0% | `0.078078` |
| `FR` | Day-5 wealth relative vs HSI | `src/write_back_expansion.py (Day-5 WR vs HSI)` | 15/15 | 100.0% | `1.0814` |
| `FS` | Day-20 BHR from Day-1 close (% | `src/write_back_expansion.py (Day-20 BHR)` | 15/15 | 100.0% | `0.690691` |
| `FT` | Day-20 wealth relative vs HSI | `src/write_back_expansion.py (Day-20 WR vs HSI)` | 15/15 | 100.0% | `1.5424` |
| `FU` | 3-month BHR from Day-1 close ( | `src/write_back_expansion.py (3-month BHR)` | 15/15 | 100.0% | `0.867868` |
| `FV` | 3-month wealth relative vs HSI | `src/write_back_expansion.py (3-month WR vs HSI)` | 15/15 | 100.0% | `1.7413` |
| `FW` | 3-month wealth relative vs HST | `src/write_back_expansion.py (3-month WR vs HSTECH)` | 15/15 | 100.0% | `1.6714` |
| `FX` | 3-month average daily turnover | `src/write_back_expansion.py (3-month avg daily turnover)` | 15/15 | 100.0% | `8572966.67` |
| `FY` | Amihud illiquidity (6M mean) | `src/write_back_expansion.py (Amihud illiquidity 6M mean)` | 15/15 | 100.0% | `0.004369428571428572` |
| `FZ` | Zero-volume days count (first  | `src/write_back_expansion.py (Zero-volume days count 6M)` | 15/15 | 100.0% | `0` |
| `GA` | Return volatility (first 6M da | `src/write_back_expansion.py (Return volatility 6M)` | 15/15 | 100.0% | `0.04788001531553043` |
| `GB` | Maximum drawdown (first 6M, %) | `src/write_back_expansion.py (Maximum drawdown 6M)` | 15/15 | 100.0% | `0.285531` |
| `GC` | Controlling shareholder 6-mont | `src/write_back_expansion.py (Controlling shareholder 6M disposal expiry)` | 15/15 | 100.0% | `2025-07-08` |
| `GD` | Controlling shareholder 12-mon | `src/write_back_expansion.py (Controlling shareholder 12M control expiry)` | 15/15 | 100.0% | `2026-01-08` |
| `GE` | Cornerstone unlock CAR [-5, +5 | `src/write_back_expansion.py (Cornerstone unlock CAR m5 p5)` | 11/15 | 73.3% | `-0.162206` |
| `GF` | Cornerstone unlock CAR [-20, + | `src/write_back_expansion.py (Cornerstone unlock CAR m20 p20)` | 11/15 | 73.3% | `-0.290976` |
| `GG` | Cornerstone unlock volume shoc | `src/write_back_expansion.py (Cornerstone unlock volume shock ratio)` | 11/15 | 73.3% | `0.6264` |
| `GH` | Lead sponsor name | `src/write_back_expansion.py (Lead sponsor name)` | 15/15 | 100.0% | `CICC` |
| `GI` | Joint sponsor count | `src/write_back_expansion.py (Joint sponsor count)` | 15/15 | 100.0% | `2` |
| `GJ` | Sponsor commercial bank affili | `src/write_back_expansion.py (Sponsor bank affiliate flag)` | 15/15 | 100.0% | `0` |
| `GK` | Underwriting base commission r | `src/write_back_expansion.py (Underwriting base commission rate)` | 15/15 | 100.0% | `0.025` |
| `GL` | Underwriting discretionary inc | `src/write_back_expansion.py (Underwriting incentive fee rate)` | 15/15 | 100.0% | `0.01` |
| `GM` | Total underwriting fee rate (% | `src/write_back_expansion.py (Total underwriting fee rate)` | 15/15 | 100.0% | `0.035` |
| `GN` | Cornerstone investor count | `src/write_back_expansion.py (Cornerstone investor count)` | 15/15 | 100.0% | `4` |
| `GO` | Cornerstone state-owned presen | `src/write_back_expansion.py (Cornerstone state-owned flag)` | 15/15 | 100.0% | `0` |
| `GP` | Crossover fund presence flag | `src/write_back_expansion.py (Crossover fund flag)` | 15/15 | 100.0% | `0` |
| `GQ` | Pre-IPO institutional investor | `src/write_back_expansion.py (Pre-IPO investor count)` | 15/15 | 100.0% | `6` |
| `GR` | Pre-IPO state-owned backing fl | `src/write_back_expansion.py (Pre-IPO state-owned flag)` | 15/15 | 100.0% | `0` |
| `GS` | FINI digital settlement regime | `src/write_back_expansion.py (FINI digital settlement regime)` | 15/15 | 100.0% | `POST_FINI` |
| `GT` | 2025 pricing reform regime | `src/write_back_expansion.py (2025 pricing reform regime)` | 15/15 | 100.0% | `PRE_2025_REFORM` |

## 四、15 家公司流水线门禁状态 (Pipeline State)

| 股票代码 | 招股书 extracted | 招股书 validated | 招股书 reviewed | 配发 extracted | 配发 validated | 配发 reviewed | 当前写入状态 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| `0325.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `0805.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `1364.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2097.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2530.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2560.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2561.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2569.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2571.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2596.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2610.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2613.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `2625.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `6681.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
| `6693.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ✅ PASS | ⏳ legacy-untracked |
