# HK IPO Excel vs JSON 逐格对账与数据质量审计报告

> **生成时间**：2026-09-28 16:43:34  
> **目标工作簿**：`cohorts/HKIPO-MB2026Q1.xlsx` (Sheet: `NLR`)  
> **审计范围**：38 家公司 × (70 招股书字段 + 18 配发字段 = 88 字段，共 3,344 个单元格) + 103 个外部工具字段  

## 一、核心审计结论汇总

| 数据类别 | 字段数 | 审计总格数 | 一致匹配格数 | Excel 缺失 | JSON 缺失 | 数值/格式差异 | 匹配率 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **招股书字段** | 70 | 2660 | 2660 | 0 | 0 | 0 | **100.00%** |
| **配发公告字段** | 18 | 684 | 684 | 0 | 0 | 0 | **100.00%** |
| **合计 (88 字段)** | 88 | 3344 | 3344 | 0 | 0 | 0 | **100.00%** |

### 关键发现点：
1. **总单元格数**：3344 个，匹配格数：3344（匹配率：100.00%）；
2. **差异统计**：Excel 缺失 0 项，JSON 缺失 0 项，数值不匹配 0 项；
3. **外部/工具衍生字段**：共 103 列；全量填报 69 列，部分填报 30 列，未填报或仅有缺失占位 4 列。此统计与上方 88 字段逐格对账是不同范围。

## 二、差异明细清单 (Discrepancies)

✅ **未发现任何字段差异，所有单元格均完全一致！**

## 三、103 个外部/工具衍生字段填报审计

| 列 | 字段说明 | 对应生成工具 | 填报数 / 总数 | 填报率 | 抽样值 |
|---|---|---|---:|---:|---|
| `V` | Filing price revision (%) | `src/academic_derivations.py (Pricing revision)` | 38/38 | 100.0% | `0.071038` |
| `W` | Filing range width (%) | `src/academic_derivations.py (Filing range width)` | 38/38 | 100.0% | `0.142077` |
| `X` | Pricing position in filing ran | `src/academic_derivations.py (Pricing position in range)` | 38/38 | 100.0% | `At high` |
| `BC` | Comments (nearest sales& profi | `Manual / Prospectus disclosure notes (Annualization factor)` | 38/38 | 100.0% | `0.5` |
| `BU` | Listing board | `tools/external/flags.py (Listing board)` | 38/38 | 100.0% | `Main Board` |
| `BW` | A+H issuer flag | `tools/external/flags.py (A+H flag)` | 38/38 | 100.0% | `0` |
| `BX` | WVR flag | `tools/external/flags.py (WVR flag)` | 38/38 | 100.0% | `0` |
| `BY` | Chapter 18A flag | `tools/external/flags.py (Chapter 18A flag)` | 38/38 | 100.0% | `0` |
| `BZ` | Chapter 18C flag | `tools/external/flags.py (Chapter 18C flag)` | 38/38 | 100.0% | `1` |
| `CA` | Industry classification code | `tools/external/hsic_codes.py (Industry classification code)` | 38/38 | 100.0% | `703010` |
| `CB` | Industry classification system | `tools/external/hsic_codes.py (Industry classification system)` | 38/38 | 100.0% | `HSICS (Hang Seng Industry` |
| `CD` | Firm age at IPO (years) | `src/academic_derivations.py (Firm age at IPO)` | 38/38 | 100.0% | `6.32` |
| `CE` | Place of incorporation | `tools/external/flags.py (Place of incorporation)` | 38/38 | 100.0% | `PRC` |
| `CG` | Financial statement unit multi | `Manual / Disclosure notes (Financial statement unit multiplier)` | 38/38 | 100.0% | `1000` |
| `CI` | Year-3 financial period start | `Manual / Disclosure notes (Financial period: Year-3 start)` | 38/38 | 100.0% | `2023-01-01` |
| `CJ` | Year-3 financial period end | `Manual / Disclosure notes (Financial period: Year-3 end)` | 38/38 | 100.0% | `2023-12-31` |
| `CK` | Year-2 financial period start | `Manual / Disclosure notes (Financial period: Year-2 start)` | 38/38 | 100.0% | `2024-01-01` |
| `CL` | Year-2 financial period end | `Manual / Disclosure notes (Financial period: Year-2 end)` | 38/38 | 100.0% | `2024-12-31` |
| `CM` | Year-1 financial period start | `Manual / Disclosure notes (Financial period: Year-1 start)` | 38/38 | 100.0% | `2025-01-01` |
| `CN` | Year-1 net sales (original, pr | `Manual / Disclosure notes (Financial: Year-1 net sales original)` | 38/38 | 100.0% | `58903000` |
| `CO` | Year-1 profit before tax (orig | `Manual / Disclosure notes (Financial: Year-1 profit before tax original)` | 38/38 | 100.0% | `-1600526000` |
| `CP` | Year-1 profit for period (orig | `Manual / Disclosure notes (Financial: Year-1 profit for period original)` | 38/38 | 100.0% | `-1600526000` |
| `CZ` | Earliest cornerstone unlock da | `tools/external/flags.py / src/cornerstone.py (Earliest cornerstone unlock date)` | 34/38 | 89.5% | `2026-07-02` |
| `DK` | Greenshoe exercise rate (%) | `src/academic_derivations.py (Greenshoe exercise rate)` | 38/38 | 100.0% | `1` |
| `DS` | HSI return over 20 trading day | `tools/external/market.py (HSI 20-day return)` | 38/38 | 100.0% | `0.01865617` |
| `DT` | HK ordinary IPO count in 90 ca | `tools/external/ipo_count.py (90-day HK ordinary IPO count)` | 38/38 | 100.0% | `39` |
| `DU` | 1-month HIBOR before prospectu | `tools/external/hkma_import.py (1-month HIBOR)` | 38/38 | 100.0% | `0.0316798` |
| `DV` | Banking system aggregate balan | `tools/external/hkma_import.py (Aggregate Balance)` | 38/38 | 100.0% | `53926000000` |
| `DW` | First trading day closing pric | `tools/external/market.py (First day close)` | 38/38 | 100.0% | `34.46` |
| `DX` | First-day return / Underpricin | `src/academic_derivations.py (First-day return / Underpricing)` | 38/38 | 100.0% | `0.758163` |
| `DY` | Money left on the table (HK$) | `src/academic_derivations.py (Money left on the table)` | 38/38 | 100.0% | `4232820476` |
| `DZ` | First trading day opening pric | `tools/external/market.py (First day open)` | 38/38 | 100.0% | `35.7` |
| `EA` | First trading day high (HK$) | `tools/external/market.py (First day high)` | 38/38 | 100.0% | `42.88` |
| `EB` | First trading day low (HK$) | `tools/external/market.py (First day low)` | 38/38 | 100.0% | `33.5` |
| `EC` | First trading day volume (shar | `tools/external/market.py (First day volume)` | 38/38 | 100.0% | `150709945` |
| `ED` | First-day flipping ratio (%) | `src/academic_derivations.py (First-day flipping ratio)` | 38/38 | 100.0% | `0.529092` |
| `EE` | First trading day turnover (HK | `tools/external/market.py (First day turnover)` | 38/38 | 100.0% | `5521275600` |
| `EF` | Offer mechanism | `tools/external/rules.py (Offer mechanism)` | 38/38 | 100.0% | `Mechanism A` |
| `EG` | Applicable IPO rules / transit | `tools/external/rules.py (Applicable IPO rules)` | 38/38 | 100.0% | `FINI (from 22/11/2023); 2` |
| `EI` | Current listing status | `tools/external/aftermarket.py (Current listing status)` | 38/38 | 100.0% | `Active` |
| `EJ` | 1-month post-IPO close price ( | `tools/external/aftermarket.py (1-month close price)` | 37/38 | 97.4% | `35.2` |
| `EK` | 1-month BHR from Day-1 close ( | `tools/external/aftermarket.py (1-month BHR)` | 37/38 | 97.4% | `0.021474` |
| `EL` | 1-month total return from offe | `tools/external/aftermarket.py (1-month total return)` | 37/38 | 97.4% | `0.795918` |
| `EM` | 1-month HSI return (%) | `tools/external/aftermarket.py (1-month HSI return)` | 37/38 | 97.4% | `0.061872` |
| `EN` | 1-month HSTECH return (%) | `tools/external/aftermarket.py (1-month HSTECH return)` | 37/38 | 97.4% | `0.018245` |
| `EO` | 1-month wealth relative vs HSI | `tools/external/aftermarket.py (1-month WR vs HSI)` | 37/38 | 97.4% | `0.962` |
| `EP` | 1-month wealth relative vs HST | `tools/external/aftermarket.py (1-month WR vs HSTECH)` | 37/38 | 97.4% | `1.0032` |
| `EQ` | 1-month average daily turnover | `tools/external/aftermarket.py (1-month average daily turnover)` | 37/38 | 97.4% | `683071810` |
| `ER` | 6-month post-IPO close price ( | `tools/external/aftermarket.py (6-month close price)` | 31/38 | 81.6% | `48.32` |
| `ES` | 6-month BHR from Day-1 close ( | `tools/external/aftermarket.py (6-month BHR)` | 31/38 | 81.6% | `0.402205` |
| `ET` | 6-month total return from offe | `tools/external/aftermarket.py (6-month total return)` | 31/38 | 81.6% | `1.465306` |
| `EU` | 6-month HSI return (%) | `tools/external/aftermarket.py (6-month HSI return)` | 31/38 | 81.6% | `-0.124663` |
| `EV` | 6-month HSTECH return (%) | `tools/external/aftermarket.py (6-month HSTECH return)` | 31/38 | 81.6% | `-0.223511` |
| `EW` | 6-month wealth relative vs HSI | `tools/external/aftermarket.py (6-month WR vs HSI)` | 31/38 | 81.6% | `1.6019` |
| `EX` | 6-month wealth relative vs HST | `tools/external/aftermarket.py (6-month WR vs HSTECH)` | 31/38 | 81.6% | `1.8058` |
| `EY` | 6-month average daily turnover | `tools/external/aftermarket.py (6-month average daily turnover)` | 31/38 | 81.6% | `871107890` |
| `EZ` | Liquidity decay ratio (6M vs D | `tools/external/aftermarket.py (Liquidity decay ratio)` | 31/38 | 81.6% | `0.157773` |
| `FA` | 1-year post-IPO return (%) [Re | `tools/external/aftermarket.py (1-year return [Reserved])` | 0/38 | 0.0% | `—` |
| `FB` | 1-year wealth relative vs HSI  | `tools/external/aftermarket.py (1-year WR vs HSI [Reserved])` | 0/38 | 0.0% | `—` |
| `FC` | 3-year post-IPO return (%) [Re | `tools/external/aftermarket.py (3-year return [Reserved])` | 0/38 | 0.0% | `—` |
| `FD` | 3-year wealth relative vs HSI  | `tools/external/aftermarket.py (3-year WR vs HSI [Reserved])` | 0/38 | 0.0% | `—` |
| `FE` | 18A/18C regulatory milestone s | `tools/external/aftermarket.py (18A/18C regulatory status)` | 38/38 | 100.0% | `18C (Specialist Tech)` |
| `FF` | Stabilizing manager | `src/write_back_expansion.py (Stabilizing manager)` | 38/38 | 100.0% | `China International Capit` |
| `FG` | Stabilization period end date | `src/write_back_expansion.py (Stabilization period end date)` | 38/38 | 100.0% | `2026-01-28` |
| `FH` | Stabilization purchases occurr | `src/write_back_expansion.py (Stabilization purchases occurred)` | 38/38 | 100.0% | `0` |
| `FI` | Over-allocation shares | `src/write_back_expansion.py (Over-allocation shares)` | 38/38 | 100.0% | `42726800` |
| `FJ` | Over-allocation (% of base off | `src/write_back_expansion.py (Over-allocation pct)` | 38/38 | 100.0% | `0.15` |
| `FK` | Over-allotment option exercise | `src/write_back_expansion.py (Over-allotment exercise date)` | 38/38 | 100.0% | `2026-01-28` |
| `FL` | Shares issued under over-allot | `src/write_back_expansion.py (Shares issued under option)` | 38/38 | 100.0% | `42726800` |
| `FM` | Over-allotment exercise percen | `src/write_back_expansion.py (Over-allotment exercise percentage)` | 38/38 | 100.0% | `1` |
| `FN` | Post-stabilization cliff retur | `src/write_back_expansion.py (Cliff return m5 p5)` | 37/38 | 97.4% | `-0.083147` |
| `FO` | Post-stabilization 20-day retu | `src/write_back_expansion.py (Post-stabilization return p20)` | 37/38 | 97.4% | `-0.053846` |
| `FP` | Post-stabilization volume deca | `src/write_back_expansion.py (Post-stabilization volume decay)` | 37/38 | 97.4% | `0.324883` |
| `FQ` | Day-5 BHR from Day-1 close (%) | `src/write_back_expansion.py (Day-5 BHR)` | 38/38 | 100.0% | `-0.024376` |
| `FR` | Day-5 wealth relative vs HSI | `src/write_back_expansion.py (Day-5 WR vs HSI)` | 38/38 | 100.0% | `0.9827` |
| `FS` | Day-20 BHR from Day-1 close (% | `src/write_back_expansion.py (Day-20 BHR)` | 37/38 | 97.4% | `0.021474` |
| `FT` | Day-20 wealth relative vs HSI | `src/write_back_expansion.py (Day-20 WR vs HSI)` | 37/38 | 97.4% | `0.962` |
| `FU` | 3-month BHR from Day-1 close ( | `src/write_back_expansion.py (3-month BHR)` | 37/38 | 97.4% | `-0.052234` |
| `FV` | 3-month wealth relative vs HSI | `src/write_back_expansion.py (3-month WR vs HSI)` | 37/38 | 97.4% | `0.9641` |
| `FW` | 3-month wealth relative vs HST | `src/write_back_expansion.py (3-month WR vs HSTECH)` | 37/38 | 97.4% | `1.1043` |
| `FX` | 3-month average daily turnover | `src/write_back_expansion.py (3-month avg daily turnover)` | 37/38 | 97.4% | `350517749.21` |
| `FY` | Amihud illiquidity (6M mean) | `src/write_back_expansion.py (Amihud illiquidity 6M mean)` | 38/38 | 100.0% | `0.0001398412698412698` |
| `FZ` | Zero-volume days count (first  | `src/write_back_expansion.py (Zero-volume days count 6M)` | 38/38 | 100.0% | `0` |
| `GA` | Return volatility (first 6M da | `src/write_back_expansion.py (Return volatility 6M)` | 38/38 | 100.0% | `0.09299886542479831` |
| `GB` | Maximum drawdown (first 6M, %) | `src/write_back_expansion.py (Maximum drawdown 6M)` | 38/38 | 100.0% | `0.36424` |
| `GC` | Controlling shareholder 6-mont | `src/write_back_expansion.py (Controlling shareholder 6M disposal expiry)` | 38/38 | 100.0% | `2026-07-02` |
| `GD` | Controlling shareholder 12-mon | `src/write_back_expansion.py (Controlling shareholder 12M control expiry)` | 38/38 | 100.0% | `2027-01-02` |
| `GE` | Cornerstone unlock CAR [-5, +5 | `src/write_back_expansion.py (Cornerstone unlock CAR m5 p5)` | 27/38 | 71.1% | `-0.177192` |
| `GF` | Cornerstone unlock CAR [-20, + | `src/write_back_expansion.py (Cornerstone unlock CAR m20 p20)` | 27/38 | 71.1% | `-0.670933` |
| `GG` | Cornerstone unlock volume shoc | `src/write_back_expansion.py (Cornerstone unlock volume shock ratio)` | 27/38 | 71.1% | `1.4033` |
| `GH` | Lead sponsor name | `src/write_back_expansion.py (Lead sponsor name)` | 38/38 | 100.0% | `China International Capit` |
| `GI` | Joint sponsor count | `src/write_back_expansion.py (Joint sponsor count)` | 38/38 | 100.0% | `0` |
| `GJ` | Sponsor commercial bank affili | `src/write_back_expansion.py (Sponsor bank affiliate flag)` | 38/38 | 100.0% | `0` |
| `GK` | Underwriting base commission r | `src/write_back_expansion.py (Underwriting base commission rate)` | 38/38 | 100.0% | `0.00015` |
| `GL` | Underwriting discretionary inc | `src/write_back_expansion.py (Underwriting incentive fee rate)` | 38/38 | 100.0% | `0.01` |
| `GM` | Total underwriting fee rate (% | `src/write_back_expansion.py (Total underwriting fee rate)` | 38/38 | 100.0% | `0.01015` |
| `GN` | Cornerstone investor count | `src/write_back_expansion.py (Cornerstone investor count)` | 38/38 | 100.0% | `25` |
| `GO` | Cornerstone state-owned presen | `src/write_back_expansion.py (Cornerstone state-owned flag)` | 38/38 | 100.0% | `1` |
| `GP` | Crossover fund presence flag | `src/write_back_expansion.py (Crossover fund flag)` | 38/38 | 100.0% | `1` |
| `GQ` | Pre-IPO institutional investor | `src/write_back_expansion.py (Pre-IPO investor count)` | 38/38 | 100.0% | `8` |
| `GR` | Pre-IPO state-owned backing fl | `src/write_back_expansion.py (Pre-IPO state-owned flag)` | 38/38 | 100.0% | `1` |
| `GS` | FINI digital settlement regime | `src/write_back_expansion.py (FINI digital settlement regime)` | 38/38 | 100.0% | `POST_FINI` |
| `GT` | 2025 pricing reform regime | `src/write_back_expansion.py (2025 pricing reform regime)` | 38/38 | 100.0% | `POST_2025_REFORM` |

## 四、38 家公司流水线门禁状态 (Pipeline State)

| 股票代码 | 招股书 extracted | 招股书 validated | 招股书 reviewed | 配发 extracted | 配发 validated | 配发 reviewed | 当前写入状态 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| `0100.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `0470.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `0501.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `0600.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `0664.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `1021.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `1641.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `1768.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `1989.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2513.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2526.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2632.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2649.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2675.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2677.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2692.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2701.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2706.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2714.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2715.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2720.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2726.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2729.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2768.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `3200.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `3268.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `3355.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `3625.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `3636.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `3986.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `6082.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `6636.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `6809.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `6938.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `9611.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `9903.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `9980.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `9981.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
