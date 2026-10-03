# HK IPO Excel vs JSON 逐格对账与数据质量审计报告

> **生成时间**：2026-10-03 20:29:38
> **目标工作簿**：`cohorts/HKIPO-MB2026Q3.xlsx` (Sheet: `NLR`)
> **审计范围**：14 家公司 × (0 招股书字段 + 18 配发字段 = 18 字段，共 252 个单元格) + 103 个外部工具字段

## 一、核心审计结论汇总

| 数据类别 | 字段数 | 审计总格数 | 一致匹配格数 | Excel 缺失 | JSON 缺失 | 数值/格式差异 | 匹配率 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **配发公告字段** | 18 | 252 | 252 | 0 | 0 | 0 | **100.00%** |
| **合计 (18 字段)** | 18 | 252 | 252 | 0 | 0 | 0 | **100.00%** |

### 关键发现点：
1. **总单元格数**：252 个，匹配格数：252（匹配率：100.00%）；
2. **差异统计**：Excel 缺失 0 项，JSON 缺失 0 项，数值不匹配 0 项；
   其中匹配格内有 5 格两边均缺失，不是已核实的证据，不能计入证据覆盖率；
3. **外部/工具衍生字段**：共 103 列；全量填报 54 列，部分填报 25 列，未填报或仅有缺失占位 24 列。此统计与上方 88 字段逐格对账是不同范围。

## 二、差异明细清单 (Discrepancies)

✅ **未发现任何字段差异，所有单元格均完全一致！**

## 三、103 个外部/工具衍生字段填报审计

| 列 | 字段说明 | 对应生成工具 | 填报数 / 总数 | 填报率 | 抽样值 |
|---|---|---|---:|---:|---|
| `V` | Filing price revision (%) | `src/academic_derivations.py (Pricing revision)` | 14/14 | 100.0% | `-0.059025` |
| `W` | Filing range width (%) | `src/academic_derivations.py (Filing range width)` | 14/14 | 100.0% | `0.124893` |
| `X` | Pricing position in filing ran | `src/academic_derivations.py (Pricing position in range)` | 14/14 | 100.0% | `Within range` |
| `BC` | Comments (nearest sales& profi | `Manual / Prospectus disclosure notes (Annualization factor)` | 14/14 | 100.0% | `1` |
| `BU` | Listing board | `tools/external/flags.py (Listing board)` | 14/14 | 100.0% | `Main Board` |
| `BW` | A+H issuer flag | `tools/external/flags.py (A+H flag)` | 14/14 | 100.0% | `0` |
| `BX` | WVR flag | `tools/external/flags.py (WVR flag)` | 14/14 | 100.0% | `0` |
| `BY` | Chapter 18A flag | `tools/external/flags.py (Chapter 18A flag)` | 14/14 | 100.0% | `0` |
| `BZ` | Chapter 18C flag | `tools/external/flags.py (Chapter 18C flag)` | 14/14 | 100.0% | `0` |
| `CA` | Industry classification code | `tools/external/hsic_codes.py (Industry classification code)` | 14/14 | 100.0% | `282020` |
| `CB` | Industry classification system | `tools/external/hsic_codes.py (Industry classification system)` | 14/14 | 100.0% | `HSICS (Hang Seng Industry` |
| `CD` | Firm age at IPO (years) | `src/academic_derivations.py (Firm age at IPO)` | 14/14 | 100.0% | `11.31` |
| `CE` | Place of incorporation | `tools/external/flags.py (Place of incorporation)` | 14/14 | 100.0% | `PRC` |
| `CG` | Financial statement unit multi | `Manual / Disclosure notes (Financial statement unit multiplier)` | 8/14 | 57.1% | `1000` |
| `CI` | Year-3 financial period start | `Manual / Disclosure notes (Financial period: Year-3 start)` | 14/14 | 100.0% | `2023-01-01` |
| `CJ` | Year-3 financial period end | `Manual / Disclosure notes (Financial period: Year-3 end)` | 14/14 | 100.0% | `2023-12-31` |
| `CK` | Year-2 financial period start | `Manual / Disclosure notes (Financial period: Year-2 start)` | 14/14 | 100.0% | `2024-01-01` |
| `CL` | Year-2 financial period end | `Manual / Disclosure notes (Financial period: Year-2 end)` | 14/14 | 100.0% | `2024-12-31` |
| `CM` | Year-1 financial period start | `Manual / Disclosure notes (Financial period: Year-1 start)` | 14/14 | 100.0% | `2025-01-01` |
| `CN` | Year-1 net sales (original, pr | `Manual / Disclosure notes (Financial: Year-1 net sales original)` | 14/14 | 100.0% | `1171315000` |
| `CO` | Year-1 profit before tax (orig | `Manual / Disclosure notes (Financial: Year-1 profit before tax original)` | 14/14 | 100.0% | `48249000` |
| `CP` | Year-1 profit for period (orig | `Manual / Disclosure notes (Financial: Year-1 profit for period original)` | 14/14 | 100.0% | `33750000` |
| `CZ` | Earliest cornerstone unlock da | `tools/external/flags.py / src/cornerstone.py (Earliest cornerstone unlock date)` | 10/14 | 71.4% | `2027-01-07` |
| `DK` | Greenshoe exercise rate (%) | `src/academic_derivations.py (Greenshoe exercise rate)` | 14/14 | 100.0% | `0` |
| `DS` | HSI return over 20 trading day | `tools/external/market.py (HSI 20-day return)` | 14/14 | 100.0% | `-0.08888584` |
| `DT` | HK ordinary IPO count in 90 ca | `tools/external/ipo_count.py (90-day HK ordinary IPO count)` | 14/14 | 100.0% | `38` |
| `DU` | 1-month HIBOR before prospectu | `tools/external/hkma_import.py (1-month HIBOR)` | 14/14 | 100.0% | `0.0296113` |
| `DV` | Banking system aggregate balan | `tools/external/hkma_import.py (Aggregate Balance)` | 14/14 | 100.0% | `54001000000` |
| `DW` | First trading day closing pric | `tools/external/market.py (First day close)` | 14/14 | 100.0% | `3.35` |
| `DX` | First-day return / Underpricin | `src/academic_derivations.py (First-day return / Underpricing)` | 14/14 | 100.0% | `-0.390909` |
| `DY` | Money left on the table (HK$) | `src/academic_derivations.py (Money left on the table)` | 14/14 | 100.0% | `-232530025` |
| `DZ` | First trading day opening pric | `tools/external/market.py (First day open)` | 14/14 | 100.0% | `4.76` |
| `EA` | First trading day high (HK$) | `tools/external/market.py (First day high)` | 14/14 | 100.0% | `4.79` |
| `EB` | First trading day low (HK$) | `tools/external/market.py (First day low)` | 14/14 | 100.0% | `3.01` |
| `EC` | First trading day volume (shar | `tools/external/market.py (First day volume)` | 14/14 | 100.0% | `43259960` |
| `ED` | First-day flipping ratio (%) | `src/academic_derivations.py (First-day flipping ratio)` | 14/14 | 100.0% | `0.399987` |
| `EE` | First trading day turnover (HK | `tools/external/market.py (First day turnover)` | 14/14 | 100.0% | `163015600` |
| `EF` | Offer mechanism | `tools/external/rules.py (Offer mechanism)` | 14/14 | 100.0% | `Mechanism B` |
| `EG` | Applicable IPO rules / transit | `tools/external/rules.py (Applicable IPO rules)` | 14/14 | 100.0% | `FINI (from 22/11/2023); 2` |
| `EI` | Current listing status | `tools/external/aftermarket.py (Current listing status)` | 14/14 | 100.0% | `Active` |
| `EJ` | 1-month post-IPO close price ( | `tools/external/aftermarket.py (1-month close price)` | 13/14 | 92.9% | `3` |
| `EK` | 1-month BHR from Day-1 close ( | `tools/external/aftermarket.py (1-month BHR)` | 13/14 | 92.9% | `-0.104478` |
| `EL` | 1-month total return from offe | `tools/external/aftermarket.py (1-month total return)` | 13/14 | 92.9% | `-0.454545` |
| `EM` | 1-month HSI return (%) | `tools/external/aftermarket.py (1-month HSI return)` | 13/14 | 92.9% | `0.106929` |
| `EN` | 1-month HSTECH return (%) | `tools/external/aftermarket.py (1-month HSTECH return)` | 13/14 | 92.9% | `0.081777` |
| `EO` | 1-month wealth relative vs HSI | `tools/external/aftermarket.py (1-month WR vs HSI)` | 13/14 | 92.9% | `0.809` |
| `EP` | 1-month wealth relative vs HST | `tools/external/aftermarket.py (1-month WR vs HSTECH)` | 13/14 | 92.9% | `0.8278` |
| `EQ` | 1-month average daily turnover | `tools/external/aftermarket.py (1-month average daily turnover)` | 13/14 | 92.9% | `12855415` |
| `ER` | 6-month post-IPO close price ( | `tools/external/aftermarket.py (6-month close price)` | 0/14 | 0.0% | `—` |
| `ES` | 6-month BHR from Day-1 close ( | `tools/external/aftermarket.py (6-month BHR)` | 0/14 | 0.0% | `—` |
| `ET` | 6-month total return from offe | `tools/external/aftermarket.py (6-month total return)` | 0/14 | 0.0% | `—` |
| `EU` | 6-month HSI return (%) | `tools/external/aftermarket.py (6-month HSI return)` | 0/14 | 0.0% | `—` |
| `EV` | 6-month HSTECH return (%) | `tools/external/aftermarket.py (6-month HSTECH return)` | 0/14 | 0.0% | `—` |
| `EW` | 6-month wealth relative vs HSI | `tools/external/aftermarket.py (6-month WR vs HSI)` | 0/14 | 0.0% | `—` |
| `EX` | 6-month wealth relative vs HST | `tools/external/aftermarket.py (6-month WR vs HSTECH)` | 0/14 | 0.0% | `—` |
| `EY` | 6-month average daily turnover | `tools/external/aftermarket.py (6-month average daily turnover)` | 0/14 | 0.0% | `—` |
| `EZ` | Liquidity decay ratio (6M vs D | `tools/external/aftermarket.py (Liquidity decay ratio)` | 0/14 | 0.0% | `—` |
| `FA` | 1-year post-IPO return (%) [Re | `tools/external/aftermarket.py (1-year return [Reserved])` | 0/14 | 0.0% | `—` |
| `FB` | 1-year wealth relative vs HSI  | `tools/external/aftermarket.py (1-year WR vs HSI [Reserved])` | 0/14 | 0.0% | `—` |
| `FC` | 3-year post-IPO return (%) [Re | `tools/external/aftermarket.py (3-year return [Reserved])` | 0/14 | 0.0% | `—` |
| `FD` | 3-year wealth relative vs HSI  | `tools/external/aftermarket.py (3-year WR vs HSI [Reserved])` | 0/14 | 0.0% | `—` |
| `FE` | 18A/18C regulatory milestone s | `tools/external/aftermarket.py (18A/18C regulatory status)` | 14/14 | 100.0% | `Standard` |
| `FF` | Stabilizing manager | `src/write_back_expansion.py (Stabilizing manager)` | 7/14 | 50.0% | `China International Capit` |
| `FG` | Stabilization period end date | `src/write_back_expansion.py (Stabilization period end date)` | 4/14 | 28.6% | `2026-08-02` |
| `FH` | Stabilization purchases occurr | `src/write_back_expansion.py (Stabilization purchases occurred)` | 1/14 | 7.1% | `0` |
| `FI` | Over-allocation shares | `src/write_back_expansion.py (Over-allocation shares)` | 5/14 | 35.7% | `3919800` |
| `FJ` | Over-allocation (% of base off | `src/write_back_expansion.py (Over-allocation pct)` | 5/14 | 35.7% | `0.15` |
| `FK` | Over-allotment option exercise | `src/write_back_expansion.py (Over-allotment exercise date)` | 12/14 | 85.7% | `2026-07-07` |
| `FL` | Shares issued under over-allot | `src/write_back_expansion.py (Shares issued under option)` | 10/14 | 71.4% | `0` |
| `FM` | Over-allotment exercise percen | `src/write_back_expansion.py (Over-allotment exercise percentage)` | 11/14 | 78.6% | `0` |
| `FN` | Post-stabilization cliff retur | `src/write_back_expansion.py (Cliff return m5 p5)` | 4/14 | 28.6% | `-0.129545` |
| `FO` | Post-stabilization 20-day retu | `src/write_back_expansion.py (Post-stabilization return p20)` | 4/14 | 28.6% | `-0.103142` |
| `FP` | Post-stabilization volume deca | `src/write_back_expansion.py (Post-stabilization volume decay)` | 4/14 | 28.6% | `0.127787` |
| `FQ` | Day-5 BHR from Day-1 close (%) | `src/write_back_expansion.py (Day-5 BHR)` | 14/14 | 100.0% | `-0.202985` |
| `FR` | Day-5 wealth relative vs HSI | `src/write_back_expansion.py (Day-5 WR vs HSI)` | 14/14 | 100.0% | `0.7734` |
| `FS` | Day-20 BHR from Day-1 close (% | `src/write_back_expansion.py (Day-20 BHR)` | 13/14 | 92.9% | `-0.104478` |
| `FT` | Day-20 wealth relative vs HSI | `src/write_back_expansion.py (Day-20 WR vs HSI)` | 13/14 | 92.9% | `0.809` |
| `FU` | 3-month BHR from Day-1 close ( | `src/write_back_expansion.py (3-month BHR)` | 0/14 | 0.0% | `—` |
| `FV` | 3-month wealth relative vs HSI | `src/write_back_expansion.py (3-month WR vs HSI)` | 0/14 | 0.0% | `—` |
| `FW` | 3-month wealth relative vs HST | `src/write_back_expansion.py (3-month WR vs HSTECH)` | 0/14 | 0.0% | `—` |
| `FX` | 3-month average daily turnover | `src/write_back_expansion.py (3-month avg daily turnover)` | 0/14 | 0.0% | `—` |
| `FY` | Amihud illiquidity (6M mean) | `src/write_back_expansion.py (Amihud illiquidity 6M mean)` | 0/14 | 0.0% | `—` |
| `FZ` | Zero-volume days count (first  | `src/write_back_expansion.py (Zero-volume days count 6M)` | 0/14 | 0.0% | `—` |
| `GA` | Return volatility (first 6M da | `src/write_back_expansion.py (Return volatility 6M)` | 0/14 | 0.0% | `—` |
| `GB` | Maximum drawdown (first 6M, %) | `src/write_back_expansion.py (Maximum drawdown 6M)` | 0/14 | 0.0% | `—` |
| `GC` | Controlling shareholder 6-mont | `src/write_back_expansion.py (Controlling shareholder 6M disposal expiry)` | 11/14 | 78.6% | `2027-01-08` |
| `GD` | Controlling shareholder 12-mon | `src/write_back_expansion.py (Controlling shareholder 12M control expiry)` | 13/14 | 92.9% | `2027-07-07` |
| `GE` | Cornerstone unlock CAR [-5, +5 | `src/write_back_expansion.py (Cornerstone unlock CAR m5 p5)` | 0/14 | 0.0% | `—` |
| `GF` | Cornerstone unlock CAR [-20, + | `src/write_back_expansion.py (Cornerstone unlock CAR m20 p20)` | 0/14 | 0.0% | `—` |
| `GG` | Cornerstone unlock volume shoc | `src/write_back_expansion.py (Cornerstone unlock volume shock ratio)` | 0/14 | 0.0% | `—` |
| `GH` | Lead sponsor name | `src/write_back_expansion.py (Lead sponsor name)` | 14/14 | 100.0% | `CICC` |
| `GI` | Joint sponsor count | `src/write_back_expansion.py (Joint sponsor count)` | 14/14 | 100.0% | `2` |
| `GJ` | Sponsor commercial bank affili | `src/write_back_expansion.py (Sponsor bank affiliate flag)` | 14/14 | 100.0% | `0` |
| `GK` | Underwriting base commission r | `src/write_back_expansion.py (Underwriting base commission rate)` | 14/14 | 100.0% | `0.025` |
| `GL` | Underwriting discretionary inc | `src/write_back_expansion.py (Underwriting incentive fee rate)` | 14/14 | 100.0% | `0.01` |
| `GM` | Total underwriting fee rate (% | `src/write_back_expansion.py (Total underwriting fee rate)` | 14/14 | 100.0% | `0.035` |
| `GN` | Cornerstone investor count | `src/write_back_expansion.py (Cornerstone investor count)` | 14/14 | 100.0% | `4` |
| `GO` | Cornerstone state-owned presen | `src/write_back_expansion.py (Cornerstone state-owned flag)` | 14/14 | 100.0% | `0` |
| `GP` | Crossover fund presence flag | `src/write_back_expansion.py (Crossover fund flag)` | 14/14 | 100.0% | `0` |
| `GQ` | Pre-IPO institutional investor | `src/write_back_expansion.py (Pre-IPO investor count)` | 14/14 | 100.0% | `6` |
| `GR` | Pre-IPO state-owned backing fl | `src/write_back_expansion.py (Pre-IPO state-owned flag)` | 14/14 | 100.0% | `0` |
| `GS` | FINI digital settlement regime | `src/write_back_expansion.py (FINI digital settlement regime)` | 14/14 | 100.0% | `POST_FINI` |
| `GT` | 2025 pricing reform regime | `src/write_back_expansion.py (2025 pricing reform regime)` | 14/14 | 100.0% | `POST_2025_REFORM` |

## 四、14 家公司流水线门禁状态 (Pipeline State)

| 股票代码 | 招股书 extracted | 招股书 validated | 招股书 reviewed | 配发 extracted | 配发 validated | 配发 reviewed | 当前写入状态 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| `1377.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `1770.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2249.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2475.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2667.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `2797.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `3752.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `6745.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `6880.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `6951.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `7656.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `7687.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `9971.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
| `9976.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ written |
