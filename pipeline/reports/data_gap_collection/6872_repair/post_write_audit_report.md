# HK IPO Excel vs JSON 逐格对账与数据质量审计报告

> **生成时间**：2026-10-02 12:40:18  
> **目标工作簿**：`cohorts/HKIPO-MB2026Q2.xlsx` (Sheet: `NLR`)  
> **审计范围**：1 家公司 × (70 招股书字段 + 0 配发字段 = 70 字段，共 70 个单元格) + 103 个外部工具字段  

## 一、核心审计结论汇总

| 数据类别 | 字段数 | 审计总格数 | 一致匹配格数 | Excel 缺失 | JSON 缺失 | 数值/格式差异 | 匹配率 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **招股书字段** | 70 | 70 | 70 | 0 | 0 | 0 | **100.00%** |
| **合计 (70 字段)** | 70 | 70 | 70 | 0 | 0 | 0 | **100.00%** |

### 关键发现点：
1. **总单元格数**：70 个，匹配格数：70（匹配率：100.00%）；
2. **差异统计**：Excel 缺失 0 项，JSON 缺失 0 项，数值不匹配 0 项；
   其中匹配格内有 6 格两边均缺失，不是已核实的证据，不能计入证据覆盖率；
3. **外部/工具衍生字段**：共 103 列；全量填报 72 列，部分填报 0 列，未填报或仅有缺失占位 31 列。此统计与上方 88 字段逐格对账是不同范围。

## 二、差异明细清单 (Discrepancies)

✅ **未发现任何字段差异，所有单元格均完全一致！**

## 三、103 个外部/工具衍生字段填报审计

| 列 | 字段说明 | 对应生成工具 | 填报数 / 总数 | 填报率 | 抽样值 |
|---|---|---|---:|---:|---|
| `V` | Filing price revision (%) | `src/academic_derivations.py (Pricing revision)` | 1/1 | 100.0% | `0` |
| `W` | Filing range width (%) | `src/academic_derivations.py (Filing range width)` | 1/1 | 100.0% | `0` |
| `X` | Pricing position in filing ran | `src/academic_derivations.py (Pricing position in range)` | 1/1 | 100.0% | `Fixed price` |
| `BC` | Comments (nearest sales& profi | `Manual / Prospectus disclosure notes (Annualization factor)` | 1/1 | 100.0% | `1` |
| `BU` | Listing board | `tools/external/flags.py (Listing board)` | 1/1 | 100.0% | `Main Board` |
| `BW` | A+H issuer flag | `tools/external/flags.py (A+H flag)` | 1/1 | 100.0% | `0` |
| `BX` | WVR flag | `tools/external/flags.py (WVR flag)` | 1/1 | 100.0% | `0` |
| `BY` | Chapter 18A flag | `tools/external/flags.py (Chapter 18A flag)` | 1/1 | 100.0% | `1` |
| `BZ` | Chapter 18C flag | `tools/external/flags.py (Chapter 18C flag)` | 1/1 | 100.0% | `0` |
| `CA` | Industry classification code | `tools/external/hsic_codes.py (Industry classification code)` | 1/1 | 100.0% | `281010` |
| `CB` | Industry classification system | `tools/external/hsic_codes.py (Industry classification system)` | 1/1 | 100.0% | `HSICS (Hang Seng Industry` |
| `CD` | Firm age at IPO (years) | `src/academic_derivations.py (Firm age at IPO)` | 1/1 | 100.0% | `13.23` |
| `CE` | Place of incorporation | `tools/external/flags.py (Place of incorporation)` | 0/1 | 0.0% | `—` |
| `CG` | Financial statement unit multi | `Manual / Disclosure notes (Financial statement unit multiplier)` | 1/1 | 100.0% | `1000` |
| `CI` | Year-3 financial period start | `Manual / Disclosure notes (Financial period: Year-3 start)` | 1/1 | 100.0% | `2023-01-01` |
| `CJ` | Year-3 financial period end | `Manual / Disclosure notes (Financial period: Year-3 end)` | 1/1 | 100.0% | `2023-12-31` |
| `CK` | Year-2 financial period start | `Manual / Disclosure notes (Financial period: Year-2 start)` | 1/1 | 100.0% | `2024-01-01` |
| `CL` | Year-2 financial period end | `Manual / Disclosure notes (Financial period: Year-2 end)` | 1/1 | 100.0% | `2024-12-31` |
| `CM` | Year-1 financial period start | `Manual / Disclosure notes (Financial period: Year-1 start)` | 1/1 | 100.0% | `2025-01-01` |
| `CN` | Year-1 net sales (original, pr | `Manual / Disclosure notes (Financial: Year-1 net sales original)` | 1/1 | 100.0% | `0` |
| `CO` | Year-1 profit before tax (orig | `Manual / Disclosure notes (Financial: Year-1 profit before tax original)` | 1/1 | 100.0% | `-153244000` |
| `CP` | Year-1 profit for period (orig | `Manual / Disclosure notes (Financial: Year-1 profit for period original)` | 1/1 | 100.0% | `-153244000` |
| `CZ` | Earliest cornerstone unlock da | `tools/external/flags.py / src/cornerstone.py (Earliest cornerstone unlock date)` | 1/1 | 100.0% | `2026-11-22` |
| `DK` | Greenshoe exercise rate (%) | `src/academic_derivations.py (Greenshoe exercise rate)` | 1/1 | 100.0% | `0` |
| `DS` | HSI return over 20 trading day | `tools/external/market.py (HSI 20-day return)` | 1/1 | 100.0% | `0.01994873` |
| `DT` | HK ordinary IPO count in 90 ca | `tools/external/ipo_count.py (90-day HK ordinary IPO count)` | 1/1 | 100.0% | `30` |
| `DU` | 1-month HIBOR before prospectu | `tools/external/hkma_import.py (1-month HIBOR)` | 1/1 | 100.0% | `0.027` |
| `DV` | Banking system aggregate balan | `tools/external/hkma_import.py (Aggregate Balance)` | 1/1 | 100.0% | `53975000000` |
| `DW` | First trading day closing pric | `tools/external/market.py (First day close)` | 1/1 | 100.0% | `211` |
| `DX` | First-day return / Underpricin | `src/academic_derivations.py (First-day return / Underpricing)` | 1/1 | 100.0% | `1.787318` |
| `DY` | Money left on the table (HK$) | `src/academic_derivations.py (Money left on the table)` | 1/1 | 100.0% | `1198216800` |
| `DZ` | First trading day opening pric | `tools/external/market.py (First day open)` | 1/1 | 100.0% | `150` |
| `EA` | First trading day high (HK$) | `tools/external/market.py (First day high)` | 1/1 | 100.0% | `222.2` |
| `EB` | First trading day low (HK$) | `tools/external/market.py (First day low)` | 1/1 | 100.0% | `145` |
| `EC` | First trading day volume (shar | `tools/external/market.py (First day volume)` | 1/1 | 100.0% | `2458654` |
| `ED` | First-day flipping ratio (%) | `src/academic_derivations.py (First-day flipping ratio)` | 1/1 | 100.0% | `0.277626` |
| `EE` | First trading day turnover (HK | `tools/external/market.py (First day turnover)` | 1/1 | 100.0% | `369693300` |
| `EF` | Offer mechanism | `tools/external/rules.py (Offer mechanism)` | 1/1 | 100.0% | `Mechanism B` |
| `EG` | Applicable IPO rules / transit | `tools/external/rules.py (Applicable IPO rules)` | 1/1 | 100.0% | `FINI (from 22/11/2023); 2` |
| `EI` | Current listing status | `tools/external/aftermarket.py (Current listing status)` | 1/1 | 100.0% | `Active` |
| `EJ` | 1-month post-IPO close price ( | `tools/external/aftermarket.py (1-month close price)` | 1/1 | 100.0% | `270` |
| `EK` | 1-month BHR from Day-1 close ( | `tools/external/aftermarket.py (1-month BHR)` | 1/1 | 100.0% | `0.279621` |
| `EL` | 1-month total return from offe | `tools/external/aftermarket.py (1-month total return)` | 1/1 | 100.0% | `2.566711` |
| `EM` | 1-month HSI return (%) | `tools/external/aftermarket.py (1-month HSI return)` | 1/1 | 100.0% | `-0.071761` |
| `EN` | 1-month HSTECH return (%) | `tools/external/aftermarket.py (1-month HSTECH return)` | 1/1 | 100.0% | `-0.065747` |
| `EO` | 1-month wealth relative vs HSI | `tools/external/aftermarket.py (1-month WR vs HSI)` | 1/1 | 100.0% | `1.3785` |
| `EP` | 1-month wealth relative vs HST | `tools/external/aftermarket.py (1-month WR vs HSTECH)` | 1/1 | 100.0% | `1.3697` |
| `EQ` | 1-month average daily turnover | `tools/external/aftermarket.py (1-month average daily turnover)` | 1/1 | 100.0% | `38852615` |
| `ER` | 6-month post-IPO close price ( | `tools/external/aftermarket.py (6-month close price)` | 0/1 | 0.0% | `—` |
| `ES` | 6-month BHR from Day-1 close ( | `tools/external/aftermarket.py (6-month BHR)` | 0/1 | 0.0% | `—` |
| `ET` | 6-month total return from offe | `tools/external/aftermarket.py (6-month total return)` | 0/1 | 0.0% | `—` |
| `EU` | 6-month HSI return (%) | `tools/external/aftermarket.py (6-month HSI return)` | 0/1 | 0.0% | `—` |
| `EV` | 6-month HSTECH return (%) | `tools/external/aftermarket.py (6-month HSTECH return)` | 0/1 | 0.0% | `—` |
| `EW` | 6-month wealth relative vs HSI | `tools/external/aftermarket.py (6-month WR vs HSI)` | 0/1 | 0.0% | `—` |
| `EX` | 6-month wealth relative vs HST | `tools/external/aftermarket.py (6-month WR vs HSTECH)` | 0/1 | 0.0% | `—` |
| `EY` | 6-month average daily turnover | `tools/external/aftermarket.py (6-month average daily turnover)` | 0/1 | 0.0% | `—` |
| `EZ` | Liquidity decay ratio (6M vs D | `tools/external/aftermarket.py (Liquidity decay ratio)` | 0/1 | 0.0% | `—` |
| `FA` | 1-year post-IPO return (%) [Re | `tools/external/aftermarket.py (1-year return [Reserved])` | 0/1 | 0.0% | `—` |
| `FB` | 1-year wealth relative vs HSI  | `tools/external/aftermarket.py (1-year WR vs HSI [Reserved])` | 0/1 | 0.0% | `—` |
| `FC` | 3-year post-IPO return (%) [Re | `tools/external/aftermarket.py (3-year return [Reserved])` | 0/1 | 0.0% | `—` |
| `FD` | 3-year wealth relative vs HSI  | `tools/external/aftermarket.py (3-year WR vs HSI [Reserved])` | 0/1 | 0.0% | `—` |
| `FE` | 18A/18C regulatory milestone s | `tools/external/aftermarket.py (18A/18C regulatory status)` | 1/1 | 100.0% | `18A (Biotech / B-tag)` |
| `FF` | Stabilizing manager | `src/write_back_expansion.py (Stabilizing manager)` | 1/1 | 100.0% | `CLSA Limited` |
| `FG` | Stabilization period end date | `src/write_back_expansion.py (Stabilization period end date)` | 0/1 | 0.0% | `—` |
| `FH` | Stabilization purchases occurr | `src/write_back_expansion.py (Stabilization purchases occurred)` | 0/1 | 0.0% | `—` |
| `FI` | Over-allocation shares | `src/write_back_expansion.py (Over-allocation shares)` | 0/1 | 0.0% | `—` |
| `FJ` | Over-allocation (% of base off | `src/write_back_expansion.py (Over-allocation pct)` | 1/1 | 100.0% | `0.0695` |
| `FK` | Over-allotment option exercise | `src/write_back_expansion.py (Over-allotment exercise date)` | 1/1 | 100.0% | `2026-05-22` |
| `FL` | Shares issued under over-allot | `src/write_back_expansion.py (Shares issued under option)` | 0/1 | 0.0% | `—` |
| `FM` | Over-allotment exercise percen | `src/write_back_expansion.py (Over-allotment exercise percentage)` | 0/1 | 0.0% | `—` |
| `FN` | Post-stabilization cliff retur | `src/write_back_expansion.py (Cliff return m5 p5)` | 0/1 | 0.0% | `—` |
| `FO` | Post-stabilization 20-day retu | `src/write_back_expansion.py (Post-stabilization return p20)` | 0/1 | 0.0% | `—` |
| `FP` | Post-stabilization volume deca | `src/write_back_expansion.py (Post-stabilization volume decay)` | 0/1 | 0.0% | `—` |
| `FQ` | Day-5 BHR from Day-1 close (%) | `src/write_back_expansion.py (Day-5 BHR)` | 1/1 | 100.0% | `-0.035071` |
| `FR` | Day-5 wealth relative vs HSI | `src/write_back_expansion.py (Day-5 WR vs HSI)` | 1/1 | 100.0% | `0.9812` |
| `FS` | Day-20 BHR from Day-1 close (% | `src/write_back_expansion.py (Day-20 BHR)` | 1/1 | 100.0% | `0.279621` |
| `FT` | Day-20 wealth relative vs HSI | `src/write_back_expansion.py (Day-20 WR vs HSI)` | 1/1 | 100.0% | `1.3785` |
| `FU` | 3-month BHR from Day-1 close ( | `src/write_back_expansion.py (3-month BHR)` | 1/1 | 100.0% | `-0.049289` |
| `FV` | 3-month wealth relative vs HSI | `src/write_back_expansion.py (3-month WR vs HSI)` | 1/1 | 100.0% | `0.954` |
| `FW` | 3-month wealth relative vs HST | `src/write_back_expansion.py (3-month WR vs HSTECH)` | 1/1 | 100.0% | `1.0077` |
| `FX` | 3-month average daily turnover | `src/write_back_expansion.py (3-month avg daily turnover)` | 1/1 | 100.0% | `20381029.69` |
| `FY` | Amihud illiquidity (6M mean) | `src/write_back_expansion.py (Amihud illiquidity 6M mean)` | 0/1 | 0.0% | `—` |
| `FZ` | Zero-volume days count (first  | `src/write_back_expansion.py (Zero-volume days count 6M)` | 0/1 | 0.0% | `—` |
| `GA` | Return volatility (first 6M da | `src/write_back_expansion.py (Return volatility 6M)` | 0/1 | 0.0% | `—` |
| `GB` | Maximum drawdown (first 6M, %) | `src/write_back_expansion.py (Maximum drawdown 6M)` | 0/1 | 0.0% | `—` |
| `GC` | Controlling shareholder 6-mont | `src/write_back_expansion.py (Controlling shareholder 6M disposal expiry)` | 0/1 | 0.0% | `—` |
| `GD` | Controlling shareholder 12-mon | `src/write_back_expansion.py (Controlling shareholder 12M control expiry)` | 1/1 | 100.0% | `2027-05-23` |
| `GE` | Cornerstone unlock CAR [-5, +5 | `src/write_back_expansion.py (Cornerstone unlock CAR m5 p5)` | 0/1 | 0.0% | `—` |
| `GF` | Cornerstone unlock CAR [-20, + | `src/write_back_expansion.py (Cornerstone unlock CAR m20 p20)` | 0/1 | 0.0% | `—` |
| `GG` | Cornerstone unlock volume shoc | `src/write_back_expansion.py (Cornerstone unlock volume shock ratio)` | 0/1 | 0.0% | `—` |
| `GH` | Lead sponsor name | `src/write_back_expansion.py (Lead sponsor name)` | 1/1 | 100.0% | `CICC` |
| `GI` | Joint sponsor count | `src/write_back_expansion.py (Joint sponsor count)` | 1/1 | 100.0% | `2` |
| `GJ` | Sponsor commercial bank affili | `src/write_back_expansion.py (Sponsor bank affiliate flag)` | 1/1 | 100.0% | `0` |
| `GK` | Underwriting base commission r | `src/write_back_expansion.py (Underwriting base commission rate)` | 1/1 | 100.0% | `0.03` |
| `GL` | Underwriting discretionary inc | `src/write_back_expansion.py (Underwriting incentive fee rate)` | 1/1 | 100.0% | `0.01` |
| `GM` | Total underwriting fee rate (% | `src/write_back_expansion.py (Total underwriting fee rate)` | 1/1 | 100.0% | `0.04` |
| `GN` | Cornerstone investor count | `src/write_back_expansion.py (Cornerstone investor count)` | 0/1 | 0.0% | `—` |
| `GO` | Cornerstone state-owned presen | `src/write_back_expansion.py (Cornerstone state-owned flag)` | 1/1 | 100.0% | `0` |
| `GP` | Crossover fund presence flag | `src/write_back_expansion.py (Crossover fund flag)` | 1/1 | 100.0% | `0` |
| `GQ` | Pre-IPO institutional investor | `src/write_back_expansion.py (Pre-IPO investor count)` | 1/1 | 100.0% | `6` |
| `GR` | Pre-IPO state-owned backing fl | `src/write_back_expansion.py (Pre-IPO state-owned flag)` | 1/1 | 100.0% | `0` |
| `GS` | FINI digital settlement regime | `src/write_back_expansion.py (FINI digital settlement regime)` | 1/1 | 100.0% | `POST_FINI` |
| `GT` | 2025 pricing reform regime | `src/write_back_expansion.py (2025 pricing reform regime)` | 1/1 | 100.0% | `POST_2025_REFORM` |

## 四、1 家公司流水线门禁状态 (Pipeline State)

| 股票代码 | 招股书 extracted | 招股书 validated | 招股书 reviewed | 配发 extracted | 配发 validated | 配发 reviewed | 当前写入状态 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| `6872.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
