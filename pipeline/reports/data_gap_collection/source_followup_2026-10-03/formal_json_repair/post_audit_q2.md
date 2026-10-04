# HK IPO Excel vs JSON 逐格对账与数据质量审计报告

> **生成时间**：2026-10-03 20:29:37
> **目标工作簿**：`cohorts/HKIPO-MB2026Q2.xlsx` (Sheet: `NLR`)
> **审计范围**：5 家公司 × (0 招股书字段 + 18 配发字段 = 18 字段，共 90 个单元格) + 103 个外部工具字段

## 一、核心审计结论汇总

| 数据类别 | 字段数 | 审计总格数 | 一致匹配格数 | Excel 缺失 | JSON 缺失 | 数值/格式差异 | 匹配率 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **配发公告字段** | 18 | 90 | 90 | 0 | 0 | 0 | **100.00%** |
| **合计 (18 字段)** | 18 | 90 | 90 | 0 | 0 | 0 | **100.00%** |

### 关键发现点：
1. **总单元格数**：90 个，匹配格数：90（匹配率：100.00%）；
2. **差异统计**：Excel 缺失 0 项，JSON 缺失 0 项，数值不匹配 0 项；
   其中匹配格内有 6 格两边均缺失，不是已核实的证据，不能计入证据覆盖率；
3. **外部/工具衍生字段**：共 103 列；全量填报 64 列，部分填报 18 列，未填报或仅有缺失占位 21 列。此统计与上方 88 字段逐格对账是不同范围。

## 二、差异明细清单 (Discrepancies)

✅ **未发现任何字段差异，所有单元格均完全一致！**

## 三、103 个外部/工具衍生字段填报审计

| 列 | 字段说明 | 对应生成工具 | 填报数 / 总数 | 填报率 | 抽样值 |
|---|---|---|---:|---:|---|
| `V` | Filing price revision (%) | `src/academic_derivations.py (Pricing revision)` | 5/5 | 100.0% | `-0.103806` |
| `W` | Filing range width (%) | `src/academic_derivations.py (Filing range width)` | 5/5 | 100.0% | `0.207612` |
| `X` | Pricing position in filing ran | `src/academic_derivations.py (Pricing position in range)` | 5/5 | 100.0% | `At low` |
| `BC` | Comments (nearest sales& profi | `Manual / Prospectus disclosure notes (Annualization factor)` | 5/5 | 100.0% | `1` |
| `BU` | Listing board | `tools/external/flags.py (Listing board)` | 5/5 | 100.0% | `Main Board` |
| `BW` | A+H issuer flag | `tools/external/flags.py (A+H flag)` | 5/5 | 100.0% | `0` |
| `BX` | WVR flag | `tools/external/flags.py (WVR flag)` | 5/5 | 100.0% | `0` |
| `BY` | Chapter 18A flag | `tools/external/flags.py (Chapter 18A flag)` | 5/5 | 100.0% | `0` |
| `BZ` | Chapter 18C flag | `tools/external/flags.py (Chapter 18C flag)` | 5/5 | 100.0% | `0` |
| `CA` | Industry classification code | `tools/external/hsic_codes.py (Industry classification code)` | 5/5 | 100.0% | `237050` |
| `CB` | Industry classification system | `tools/external/hsic_codes.py (Industry classification system)` | 5/5 | 100.0% | `HSICS (Hang Seng Industry` |
| `CD` | Firm age at IPO (years) | `src/academic_derivations.py (Firm age at IPO)` | 5/5 | 100.0% | `0.67` |
| `CE` | Place of incorporation | `tools/external/flags.py (Place of incorporation)` | 2/5 | 40.0% | `Cayman Islands` |
| `CG` | Financial statement unit multi | `Manual / Disclosure notes (Financial statement unit multiplier)` | 4/5 | 80.0% | `1000` |
| `CI` | Year-3 financial period start | `Manual / Disclosure notes (Financial period: Year-3 start)` | 5/5 | 100.0% | `2022-12-01` |
| `CJ` | Year-3 financial period end | `Manual / Disclosure notes (Financial period: Year-3 end)` | 5/5 | 100.0% | `2023-11-30` |
| `CK` | Year-2 financial period start | `Manual / Disclosure notes (Financial period: Year-2 start)` | 5/5 | 100.0% | `2023-12-01` |
| `CL` | Year-2 financial period end | `Manual / Disclosure notes (Financial period: Year-2 end)` | 5/5 | 100.0% | `2024-11-30` |
| `CM` | Year-1 financial period start | `Manual / Disclosure notes (Financial period: Year-1 start)` | 5/5 | 100.0% | `2024-12-01` |
| `CN` | Year-1 net sales (original, pr | `Manual / Disclosure notes (Financial: Year-1 net sales original)` | 5/5 | 100.0% | `3052702500` |
| `CO` | Year-1 profit before tax (orig | `Manual / Disclosure notes (Financial: Year-1 profit before tax original)` | 5/5 | 100.0% | `268146000` |
| `CP` | Year-1 profit for period (orig | `Manual / Disclosure notes (Financial: Year-1 profit for period original)` | 5/5 | 100.0% | `222574500` |
| `CZ` | Earliest cornerstone unlock da | `tools/external/flags.py / src/cornerstone.py (Earliest cornerstone unlock date)` | 3/5 | 60.0% | `2026-12-24` |
| `DK` | Greenshoe exercise rate (%) | `src/academic_derivations.py (Greenshoe exercise rate)` | 5/5 | 100.0% | `0` |
| `DS` | HSI return over 20 trading day | `tools/external/market.py (HSI 20-day return)` | 5/5 | 100.0% | `-0.02304355` |
| `DT` | HK ordinary IPO count in 90 ca | `tools/external/ipo_count.py (90-day HK ordinary IPO count)` | 5/5 | 100.0% | `35` |
| `DU` | 1-month HIBOR before prospectu | `tools/external/hkma_import.py (1-month HIBOR)` | 5/5 | 100.0% | `0.026` |
| `DV` | Banking system aggregate balan | `tools/external/hkma_import.py (Aggregate Balance)` | 5/5 | 100.0% | `53997000000` |
| `DW` | First trading day closing pric | `tools/external/market.py (First day close)` | 5/5 | 100.0% | `2.81` |
| `DX` | First-day return / Underpricin | `src/academic_derivations.py (First-day return / Underpricing)` | 5/5 | 100.0% | `-0.457529` |
| `DY` | Money left on the table (HK$) | `src/academic_derivations.py (Money left on the table)` | 5/5 | 100.0% | `-296250000` |
| `DZ` | First trading day opening pric | `tools/external/market.py (First day open)` | 5/5 | 100.0% | `4.32` |
| `EA` | First trading day high (HK$) | `tools/external/market.py (First day high)` | 5/5 | 100.0% | `4.6` |
| `EB` | First trading day low (HK$) | `tools/external/market.py (First day low)` | 5/5 | 100.0% | `2.8` |
| `EC` | First trading day volume (shar | `tools/external/market.py (First day volume)` | 5/5 | 100.0% | `85471206` |
| `ED` | First-day flipping ratio (%) | `src/academic_derivations.py (First-day flipping ratio)` | 5/5 | 100.0% | `0.68377` |
| `EE` | First trading day turnover (HK | `tools/external/market.py (First day turnover)` | 5/5 | 100.0% | `346179400` |
| `EF` | Offer mechanism | `tools/external/rules.py (Offer mechanism)` | 3/5 | 60.0% | `Mechanism B` |
| `EG` | Applicable IPO rules / transit | `tools/external/rules.py (Applicable IPO rules)` | 5/5 | 100.0% | `FINI (from 22/11/2023); 2` |
| `EI` | Current listing status | `tools/external/aftermarket.py (Current listing status)` | 5/5 | 100.0% | `Active` |
| `EJ` | 1-month post-IPO close price ( | `tools/external/aftermarket.py (1-month close price)` | 5/5 | 100.0% | `3.6` |
| `EK` | 1-month BHR from Day-1 close ( | `tools/external/aftermarket.py (1-month BHR)` | 5/5 | 100.0% | `0.281139` |
| `EL` | 1-month total return from offe | `tools/external/aftermarket.py (1-month total return)` | 5/5 | 100.0% | `-0.305019` |
| `EM` | 1-month HSI return (%) | `tools/external/aftermarket.py (1-month HSI return)` | 5/5 | 100.0% | `-0.053907` |
| `EN` | 1-month HSTECH return (%) | `tools/external/aftermarket.py (1-month HSTECH return)` | 5/5 | 100.0% | `-0.071017` |
| `EO` | 1-month wealth relative vs HSI | `tools/external/aftermarket.py (1-month WR vs HSI)` | 5/5 | 100.0% | `1.3541` |
| `EP` | 1-month wealth relative vs HST | `tools/external/aftermarket.py (1-month WR vs HSTECH)` | 5/5 | 100.0% | `1.3791` |
| `EQ` | 1-month average daily turnover | `tools/external/aftermarket.py (1-month average daily turnover)` | 5/5 | 100.0% | `36461920` |
| `ER` | 6-month post-IPO close price ( | `tools/external/aftermarket.py (6-month close price)` | 0/5 | 0.0% | `—` |
| `ES` | 6-month BHR from Day-1 close ( | `tools/external/aftermarket.py (6-month BHR)` | 0/5 | 0.0% | `—` |
| `ET` | 6-month total return from offe | `tools/external/aftermarket.py (6-month total return)` | 0/5 | 0.0% | `—` |
| `EU` | 6-month HSI return (%) | `tools/external/aftermarket.py (6-month HSI return)` | 0/5 | 0.0% | `—` |
| `EV` | 6-month HSTECH return (%) | `tools/external/aftermarket.py (6-month HSTECH return)` | 0/5 | 0.0% | `—` |
| `EW` | 6-month wealth relative vs HSI | `tools/external/aftermarket.py (6-month WR vs HSI)` | 0/5 | 0.0% | `—` |
| `EX` | 6-month wealth relative vs HST | `tools/external/aftermarket.py (6-month WR vs HSTECH)` | 0/5 | 0.0% | `—` |
| `EY` | 6-month average daily turnover | `tools/external/aftermarket.py (6-month average daily turnover)` | 0/5 | 0.0% | `—` |
| `EZ` | Liquidity decay ratio (6M vs D | `tools/external/aftermarket.py (Liquidity decay ratio)` | 0/5 | 0.0% | `—` |
| `FA` | 1-year post-IPO return (%) [Re | `tools/external/aftermarket.py (1-year return [Reserved])` | 0/5 | 0.0% | `—` |
| `FB` | 1-year wealth relative vs HSI  | `tools/external/aftermarket.py (1-year WR vs HSI [Reserved])` | 0/5 | 0.0% | `—` |
| `FC` | 3-year post-IPO return (%) [Re | `tools/external/aftermarket.py (3-year return [Reserved])` | 0/5 | 0.0% | `—` |
| `FD` | 3-year wealth relative vs HSI  | `tools/external/aftermarket.py (3-year WR vs HSI [Reserved])` | 0/5 | 0.0% | `—` |
| `FE` | 18A/18C regulatory milestone s | `tools/external/aftermarket.py (18A/18C regulatory status)` | 5/5 | 100.0% | `Standard` |
| `FF` | Stabilizing manager | `src/write_back_expansion.py (Stabilizing manager)` | 3/5 | 60.0% | `CCB International Capital` |
| `FG` | Stabilization period end date | `src/write_back_expansion.py (Stabilization period end date)` | 1/5 | 20.0% | `2026-07-25` |
| `FH` | Stabilization purchases occurr | `src/write_back_expansion.py (Stabilization purchases occurred)` | 0/5 | 0.0% | `—` |
| `FI` | Over-allocation shares | `src/write_back_expansion.py (Over-allocation shares)` | 1/5 | 20.0% | `2016200` |
| `FJ` | Over-allocation (% of base off | `src/write_back_expansion.py (Over-allocation pct)` | 2/5 | 40.0% | `0.3788` |
| `FK` | Over-allotment option exercise | `src/write_back_expansion.py (Over-allotment exercise date)` | 3/5 | 60.0% | `2026-07-18` |
| `FL` | Shares issued under over-allot | `src/write_back_expansion.py (Shares issued under option)` | 3/5 | 60.0% | `0` |
| `FM` | Over-allotment exercise percen | `src/write_back_expansion.py (Over-allotment exercise percentage)` | 3/5 | 60.0% | `0` |
| `FN` | Post-stabilization cliff retur | `src/write_back_expansion.py (Cliff return m5 p5)` | 1/5 | 20.0% | `-0.057632` |
| `FO` | Post-stabilization 20-day retu | `src/write_back_expansion.py (Post-stabilization return p20)` | 1/5 | 20.0% | `-0.148748` |
| `FP` | Post-stabilization volume deca | `src/write_back_expansion.py (Post-stabilization volume decay)` | 1/5 | 20.0% | `0.105418` |
| `FQ` | Day-5 BHR from Day-1 close (%) | `src/write_back_expansion.py (Day-5 BHR)` | 5/5 | 100.0% | `-0.021352` |
| `FR` | Day-5 wealth relative vs HSI | `src/write_back_expansion.py (Day-5 WR vs HSI)` | 5/5 | 100.0% | `1.0074` |
| `FS` | Day-20 BHR from Day-1 close (% | `src/write_back_expansion.py (Day-20 BHR)` | 5/5 | 100.0% | `0.281139` |
| `FT` | Day-20 wealth relative vs HSI | `src/write_back_expansion.py (Day-20 WR vs HSI)` | 5/5 | 100.0% | `1.3541` |
| `FU` | 3-month BHR from Day-1 close ( | `src/write_back_expansion.py (3-month BHR)` | 5/5 | 100.0% | `0.441281` |
| `FV` | 3-month wealth relative vs HSI | `src/write_back_expansion.py (3-month WR vs HSI)` | 2/5 | 40.0% | `1.4157` |
| `FW` | 3-month wealth relative vs HST | `src/write_back_expansion.py (3-month WR vs HSTECH)` | 2/5 | 40.0% | `1.5561` |
| `FX` | 3-month average daily turnover | `src/write_back_expansion.py (3-month avg daily turnover)` | 5/5 | 100.0% | `18026963.08` |
| `FY` | Amihud illiquidity (6M mean) | `src/write_back_expansion.py (Amihud illiquidity 6M mean)` | 0/5 | 0.0% | `—` |
| `FZ` | Zero-volume days count (first  | `src/write_back_expansion.py (Zero-volume days count 6M)` | 0/5 | 0.0% | `—` |
| `GA` | Return volatility (first 6M da | `src/write_back_expansion.py (Return volatility 6M)` | 0/5 | 0.0% | `—` |
| `GB` | Maximum drawdown (first 6M, %) | `src/write_back_expansion.py (Maximum drawdown 6M)` | 0/5 | 0.0% | `—` |
| `GC` | Controlling shareholder 6-mont | `src/write_back_expansion.py (Controlling shareholder 6M disposal expiry)` | 3/5 | 60.0% | `2026-12-06` |
| `GD` | Controlling shareholder 12-mon | `src/write_back_expansion.py (Controlling shareholder 12M control expiry)` | 5/5 | 100.0% | `2027-06-06` |
| `GE` | Cornerstone unlock CAR [-5, +5 | `src/write_back_expansion.py (Cornerstone unlock CAR m5 p5)` | 0/5 | 0.0% | `—` |
| `GF` | Cornerstone unlock CAR [-20, + | `src/write_back_expansion.py (Cornerstone unlock CAR m20 p20)` | 0/5 | 0.0% | `—` |
| `GG` | Cornerstone unlock volume shoc | `src/write_back_expansion.py (Cornerstone unlock volume shock ratio)` | 0/5 | 0.0% | `—` |
| `GH` | Lead sponsor name | `src/write_back_expansion.py (Lead sponsor name)` | 5/5 | 100.0% | `CICC` |
| `GI` | Joint sponsor count | `src/write_back_expansion.py (Joint sponsor count)` | 5/5 | 100.0% | `2` |
| `GJ` | Sponsor commercial bank affili | `src/write_back_expansion.py (Sponsor bank affiliate flag)` | 5/5 | 100.0% | `0` |
| `GK` | Underwriting base commission r | `src/write_back_expansion.py (Underwriting base commission rate)` | 5/5 | 100.0% | `0.025` |
| `GL` | Underwriting discretionary inc | `src/write_back_expansion.py (Underwriting incentive fee rate)` | 5/5 | 100.0% | `0.01` |
| `GM` | Total underwriting fee rate (% | `src/write_back_expansion.py (Total underwriting fee rate)` | 5/5 | 100.0% | `0.035` |
| `GN` | Cornerstone investor count | `src/write_back_expansion.py (Cornerstone investor count)` | 2/5 | 40.0% | `0` |
| `GO` | Cornerstone state-owned presen | `src/write_back_expansion.py (Cornerstone state-owned flag)` | 5/5 | 100.0% | `0` |
| `GP` | Crossover fund presence flag | `src/write_back_expansion.py (Crossover fund flag)` | 5/5 | 100.0% | `0` |
| `GQ` | Pre-IPO institutional investor | `src/write_back_expansion.py (Pre-IPO investor count)` | 5/5 | 100.0% | `6` |
| `GR` | Pre-IPO state-owned backing fl | `src/write_back_expansion.py (Pre-IPO state-owned flag)` | 5/5 | 100.0% | `0` |
| `GS` | FINI digital settlement regime | `src/write_back_expansion.py (FINI digital settlement regime)` | 5/5 | 100.0% | `POST_FINI` |
| `GT` | 2025 pricing reform regime | `src/write_back_expansion.py (2025 pricing reform regime)` | 5/5 | 100.0% | `POST_2025_REFORM` |

## 四、5 家公司流水线门禁状态 (Pipeline State)

| 股票代码 | 招股书 extracted | 招股书 validated | 招股书 reviewed | 配发 extracted | 配发 validated | 配发 reviewed | 当前写入状态 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| `1392.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ❌ NO | ⏳ legacy-untracked |
| `2290.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ❌ NO | ⏳ legacy-untracked |
| `2335.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ❌ NO | ⏳ legacy-untracked |
| `3952.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ❌ NO | ⏳ legacy-untracked |
| `6106.HK` | ✅ PASS | ✅ PASS | ✅ PASS | ❌ NO | ✅ PASS | ❌ NO | ⏳ legacy-untracked |
