# HK IPO Excel vs JSON 逐格对账与数据质量审计报告

> **生成时间**：2026-10-16 01:45:58  
> **目标工作簿**：`cohorts/HKIPO-GEM2026Q1.xlsx` (Sheet: `NLR`)  
> **审计范围**：1 家公司 × (69 招股书字段 + 18 配发字段 = 87 字段，共 87 个单元格) + 97 个外部工具字段  

## 一、核心审计结论汇总

| 数据类别 | 字段数 | 审计总格数 | 一致匹配格数 | Excel 缺失 | JSON 缺失 | 数值/格式差异 | 匹配率 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **招股书字段** | 69 | 69 | 69 | 0 | 0 | 0 | **100.00%** |
| **配发公告字段** | 18 | 18 | 18 | 0 | 0 | 0 | **100.00%** |
| **合计 (87 字段)** | 87 | 87 | 87 | 0 | 0 | 0 | **100.00%** |

### 关键发现点：
1. **总单元格数**：87 个，匹配格数：87（匹配率：100.00%）；
2. **差异统计**：Excel 缺失 0 项，JSON 缺失 0 项，数值不匹配 0 项；
   其中匹配格内有 4 格两边均缺失，不是已核实的证据，不能计入证据覆盖率；
3. **外部/工具衍生字段**：共 97 列；全量填报 50 列，部分填报 0 列，未填报或仅有缺失占位 47 列。此统计与上方 88 字段逐格对账是不同范围。

## 二、差异明细清单 (Discrepancies)

✅ **未发现任何字段差异，所有单元格均完全一致！**

## 三、97 个外部/工具衍生字段填报审计

| 列 | 字段说明 | 对应生成工具 | 填报数 / 总数 | 填报率 | 抽样值 |
|---|---|---|---:|---:|---|
| `V` | Filing price revision (%) | `src/academic_derivations.py (Pricing revision)` | 1/1 | 100.0% | `-0.076923` |
| `W` | Filing range width (%) | `src/academic_derivations.py (Filing range width)` | 1/1 | 100.0% | `0.153846` |
| `X` | Pricing position in filing ran | `src/academic_derivations.py (Pricing position in range)` | 1/1 | 100.0% | `At low` |
| `BC` | Comments (nearest sales& profi | `Manual / Prospectus disclosure notes (Annualization factor)` | 1/1 | 100.0% | `0.5` |
| `BT` | Listing board | `tools/external/flags.py (Listing board)` | 1/1 | 100.0% | `GEM` |
| `BV` | A+H issuer flag | `tools/external/flags.py (A+H flag)` | 1/1 | 100.0% | `0` |
| `BW` | Industry classification code | `tools/external/hsic_codes.py (Industry classification code)` | 1/1 | 100.0% | `602030` |
| `BX` | Industry classification system | `tools/external/hsic_codes.py (Industry classification system)` | 1/1 | 100.0% | `HSICS (Hang Seng Industry` |
| `BZ` | Firm age at IPO (years) | `src/academic_derivations.py (Firm age at IPO)` | 1/1 | 100.0% | `0.62` |
| `CA` | Place of incorporation | `tools/external/flags.py (Place of incorporation)` | 1/1 | 100.0% | `Cayman Islands` |
| `CC` | Financial statement unit multi | `Manual / Disclosure notes (Financial statement unit multiplier)` | 0/1 | 0.0% | `—` |
| `CE` | Year-3 financial period start | `Manual / Disclosure notes (Financial period: Year-3 start)` | 1/1 | 100.0% | `2023-01-01` |
| `CF` | Year-3 financial period end | `Manual / Disclosure notes (Financial period: Year-3 end)` | 1/1 | 100.0% | `2023-12-31` |
| `CG` | Year-2 financial period start | `Manual / Disclosure notes (Financial period: Year-2 start)` | 1/1 | 100.0% | `2024-01-01` |
| `CH` | Year-2 financial period end | `Manual / Disclosure notes (Financial period: Year-2 end)` | 1/1 | 100.0% | `2024-12-31` |
| `CI` | Year-1 financial period start | `Manual / Disclosure notes (Financial period: Year-1 start)` | 1/1 | 100.0% | `2025-01-01` |
| `CJ` | Year-1 net sales (original, pr | `Manual / Disclosure notes (Financial: Year-1 net sales original)` | 1/1 | 100.0% | `73986000` |
| `CK` | Year-1 profit before tax (orig | `Manual / Disclosure notes (Financial: Year-1 profit before tax original)` | 1/1 | 100.0% | `5943000` |
| `CL` | Year-1 profit for period (orig | `Manual / Disclosure notes (Financial: Year-1 profit for period original)` | 1/1 | 100.0% | `3201000` |
| `CV` | Earliest cornerstone unlock da | `tools/external/flags.py / src/cornerstone.py (Earliest cornerstone unlock date)` | 0/1 | 0.0% | `—` |
| `DG` | Greenshoe exercise rate (%) | `src/academic_derivations.py (Greenshoe exercise rate)` | 1/1 | 100.0% | `0` |
| `DO` | HSI return over 20 trading day | `tools/external/market.py (HSI 20-day return)` | 1/1 | 100.0% | `-0.00016594` |
| `DP` | GEM ordinary IPO count in 90 c | `Other external / manual` | 1/1 | 100.0% | `1` |
| `DQ` | 1-month HIBOR before prospectu | `tools/external/hkma_import.py (1-month HIBOR)` | 1/1 | 100.0% | `0.0321107` |
| `DR` | Banking system aggregate balan | `tools/external/hkma_import.py (Aggregate Balance)` | 1/1 | 100.0% | `53950000000` |
| `DS` | First trading day closing pric | `tools/external/market.py (First day close)` | 1/1 | 100.0% | `0.67` |
| `DT` | First-day return / Underpricin | `src/academic_derivations.py (First-day return / Underpricing)` | 1/1 | 100.0% | `0.116667` |
| `DU` | Money left on the table (HK$) | `src/academic_derivations.py (Money left on the table)` | 1/1 | 100.0% | `8750000` |
| `DV` | First trading day opening pric | `tools/external/market.py (First day open)` | 1/1 | 100.0% | `3` |
| `DW` | First trading day high (HK$) | `tools/external/market.py (First day high)` | 1/1 | 100.0% | `3.11` |
| `DX` | First trading day low (HK$) | `tools/external/market.py (First day low)` | 1/1 | 100.0% | `0.59` |
| `DY` | First trading day volume (shar | `tools/external/market.py (First day volume)` | 1/1 | 100.0% | `120963660` |
| `DZ` | First-day flipping ratio (%) | `src/academic_derivations.py (First-day flipping ratio)` | 1/1 | 100.0% | `0.967709` |
| `EA` | First trading day turnover (HK | `tools/external/market.py (First day turnover)` | 0/1 | 0.0% | `—` |
| `EB` | Offer mechanism | `tools/external/rules.py (Offer mechanism)` | 0/1 | 0.0% | `—` |
| `EC` | Applicable IPO rules / transit | `tools/external/rules.py (Applicable IPO rules)` | 0/1 | 0.0% | `—` |
| `EE` | Current listing status | `tools/external/aftermarket.py (Current listing status)` | 1/1 | 100.0% | `Active` |
| `EF` | 1-month post-IPO close price ( | `tools/external/aftermarket.py (1-month close price)` | 1/1 | 100.0% | `0.66` |
| `EG` | 1-month BHR from Day-1 close ( | `tools/external/aftermarket.py (1-month BHR)` | 1/1 | 100.0% | `0` |
| `EH` | 1-month total return from offe | `tools/external/aftermarket.py (1-month total return)` | 1/1 | 100.0% | `0.116667` |
| `EI` | 1-month HSI return (%) | `tools/external/aftermarket.py (1-month HSI return)` | 1/1 | 100.0% | `0.006655` |
| `EJ` | 1-month HSTECH return (%) | `tools/external/aftermarket.py (1-month HSTECH return)` | 1/1 | 100.0% | `-0.077037` |
| `EK` | 1-month wealth relative vs HSI | `tools/external/aftermarket.py (1-month WR vs HSI)` | 1/1 | 100.0% | `0.9934` |
| `EL` | 1-month wealth relative vs HST | `tools/external/aftermarket.py (1-month WR vs HSTECH)` | 1/1 | 100.0% | `1.0835` |
| `EM` | 1-month average daily turnover | `tools/external/aftermarket.py (1-month average daily turnover)` | 1/1 | 100.0% | `11622003.5` |
| `EN` | 6-month post-IPO close price ( | `tools/external/aftermarket.py (6-month close price)` | 1/1 | 100.0% | `0.56` |
| `EO` | 6-month BHR from Day-1 close ( | `tools/external/aftermarket.py (6-month BHR)` | 1/1 | 100.0% | `-0.151515` |
| `EP` | 6-month total return from offe | `tools/external/aftermarket.py (6-month total return)` | 1/1 | 100.0% | `-0.052525` |
| `EQ` | 6-month HSI return (%) | `tools/external/aftermarket.py (6-month HSI return)` | 1/1 | 100.0% | `-0.098134` |
| `ER` | 6-month HSTECH return (%) | `tools/external/aftermarket.py (6-month HSTECH return)` | 1/1 | 100.0% | `-0.203305` |
| `ES` | 6-month wealth relative vs HSI | `tools/external/aftermarket.py (6-month WR vs HSI)` | 1/1 | 100.0% | `0.9408` |
| `ET` | 6-month wealth relative vs HST | `tools/external/aftermarket.py (6-month WR vs HSTECH)` | 1/1 | 100.0% | `1.065` |
| `EU` | 6-month average daily turnover | `tools/external/aftermarket.py (6-month average daily turnover)` | 1/1 | 100.0% | `69385` |
| `EV` | Liquidity decay ratio (6M vs D | `tools/external/aftermarket.py (Liquidity decay ratio)` | 1/1 | 100.0% | `0.000385` |
| `EW` | 1-year post-IPO return (%) [Re | `tools/external/aftermarket.py (1-year return [Reserved])` | 0/1 | 0.0% | `—` |
| `EX` | 1-year wealth relative vs HSI  | `tools/external/aftermarket.py (1-year WR vs HSI [Reserved])` | 0/1 | 0.0% | `—` |
| `EY` | 3-year post-IPO return (%) [Re | `tools/external/aftermarket.py (3-year return [Reserved])` | 0/1 | 0.0% | `—` |
| `EZ` | 3-year wealth relative vs HSI  | `tools/external/aftermarket.py (3-year WR vs HSI [Reserved])` | 0/1 | 0.0% | `—` |
| `FA` | 18A/18C regulatory milestone s | `tools/external/aftermarket.py (18A/18C regulatory status)` | 1/1 | 100.0% | `Standard` |
| `FB` | Stabilizing manager | `src/write_back_expansion.py (Stabilizing manager)` | 0/1 | 0.0% | `—` |
| `FC` | Stabilization period end date | `src/write_back_expansion.py (Stabilization period end date)` | 0/1 | 0.0% | `—` |
| `FD` | Stabilization purchases occurr | `src/write_back_expansion.py (Stabilization purchases occurred)` | 0/1 | 0.0% | `—` |
| `FE` | Over-allocation shares | `src/write_back_expansion.py (Over-allocation shares)` | 0/1 | 0.0% | `—` |
| `FF` | Over-allocation (% of base off | `src/write_back_expansion.py (Over-allocation pct)` | 0/1 | 0.0% | `—` |
| `FG` | Over-allotment option exercise | `src/write_back_expansion.py (Over-allotment exercise date)` | 0/1 | 0.0% | `—` |
| `FH` | Shares issued under over-allot | `src/write_back_expansion.py (Shares issued under option)` | 0/1 | 0.0% | `—` |
| `FI` | Over-allotment exercise percen | `src/write_back_expansion.py (Over-allotment exercise percentage)` | 0/1 | 0.0% | `—` |
| `FJ` | Post-stabilization cliff retur | `src/write_back_expansion.py (Cliff return m5 p5)` | 0/1 | 0.0% | `—` |
| `FK` | Post-stabilization 20-day retu | `src/write_back_expansion.py (Post-stabilization return p20)` | 0/1 | 0.0% | `—` |
| `FL` | Post-stabilization volume deca | `src/write_back_expansion.py (Post-stabilization volume decay)` | 0/1 | 0.0% | `—` |
| `FM` | Day-5 BHR from Day-1 close (%) | `src/write_back_expansion.py (Day-5 BHR)` | 0/1 | 0.0% | `—` |
| `FN` | Day-5 wealth relative vs HSI | `src/write_back_expansion.py (Day-5 WR vs HSI)` | 0/1 | 0.0% | `—` |
| `FO` | Day-20 BHR from Day-1 close (% | `src/write_back_expansion.py (Day-20 BHR)` | 0/1 | 0.0% | `—` |
| `FP` | Day-20 wealth relative vs HSI | `src/write_back_expansion.py (Day-20 WR vs HSI)` | 0/1 | 0.0% | `—` |
| `FQ` | 3-month BHR from Day-1 close ( | `src/write_back_expansion.py (3-month BHR)` | 0/1 | 0.0% | `—` |
| `FR` | 3-month wealth relative vs HSI | `src/write_back_expansion.py (3-month WR vs HSI)` | 0/1 | 0.0% | `—` |
| `FS` | 3-month wealth relative vs HST | `src/write_back_expansion.py (3-month WR vs HSTECH)` | 0/1 | 0.0% | `—` |
| `FT` | 3-month average daily turnover | `src/write_back_expansion.py (3-month avg daily turnover)` | 0/1 | 0.0% | `—` |
| `FU` | Amihud illiquidity (6M mean) | `src/write_back_expansion.py (Amihud illiquidity 6M mean)` | 0/1 | 0.0% | `—` |
| `FV` | Zero-volume days count (first  | `src/write_back_expansion.py (Zero-volume days count 6M)` | 0/1 | 0.0% | `—` |
| `FW` | Return volatility (first 6M da | `src/write_back_expansion.py (Return volatility 6M)` | 0/1 | 0.0% | `—` |
| `FX` | Maximum drawdown (first 6M, %) | `src/write_back_expansion.py (Maximum drawdown 6M)` | 0/1 | 0.0% | `—` |
| `FY` | Cornerstone unlock CAR [-5, +5 | `src/write_back_expansion.py (Cornerstone unlock CAR m5 p5)` | 0/1 | 0.0% | `—` |
| `FZ` | Cornerstone unlock CAR [-20, + | `src/write_back_expansion.py (Cornerstone unlock CAR m20 p20)` | 0/1 | 0.0% | `—` |
| `GA` | Cornerstone unlock volume shoc | `src/write_back_expansion.py (Cornerstone unlock volume shock ratio)` | 0/1 | 0.0% | `—` |
| `GB` | Lead sponsor name | `src/write_back_expansion.py (Lead sponsor name)` | 0/1 | 0.0% | `—` |
| `GC` | Joint sponsor count | `src/write_back_expansion.py (Joint sponsor count)` | 0/1 | 0.0% | `—` |
| `GD` | Sponsor commercial bank affili | `src/write_back_expansion.py (Sponsor bank affiliate flag)` | 0/1 | 0.0% | `—` |
| `GE` | Underwriting base commission r | `src/write_back_expansion.py (Underwriting base commission rate)` | 0/1 | 0.0% | `—` |
| `GF` | Underwriting discretionary inc | `src/write_back_expansion.py (Underwriting incentive fee rate)` | 0/1 | 0.0% | `—` |
| `GG` | Total underwriting fee rate (% | `src/write_back_expansion.py (Total underwriting fee rate)` | 0/1 | 0.0% | `—` |
| `GH` | Cornerstone investor count | `src/write_back_expansion.py (Cornerstone investor count)` | 0/1 | 0.0% | `—` |
| `GI` | Cornerstone state-owned presen | `src/write_back_expansion.py (Cornerstone state-owned flag)` | 0/1 | 0.0% | `—` |
| `GJ` | Crossover fund presence flag | `src/write_back_expansion.py (Crossover fund flag)` | 0/1 | 0.0% | `—` |
| `GK` | Pre-IPO institutional investor | `src/write_back_expansion.py (Pre-IPO investor count)` | 0/1 | 0.0% | `—` |
| `GL` | Pre-IPO state-owned backing fl | `src/write_back_expansion.py (Pre-IPO state-owned flag)` | 0/1 | 0.0% | `—` |
| `GM` | FINI digital settlement regime | `src/write_back_expansion.py (FINI digital settlement regime)` | 0/1 | 0.0% | `—` |

## 四、1 家公司流水线门禁状态 (Pipeline State)

| 股票代码 | 招股书 extracted | 招股书 validated | 招股书 reviewed | 配发 extracted | 配发 validated | 配发 reviewed | 当前写入状态 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| `8610.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
