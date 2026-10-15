# HK IPO Excel vs JSON 逐格对账与数据质量审计报告

> **生成时间**：2026-10-15 10:59:08  
> **目标工作簿**：`cohorts/HKIPO-MB2025Q4.xlsx` (Sheet: `NLR`)  
> **审计范围**：47 家公司 × (70 招股书字段 + 18 配发字段 = 88 字段，共 4,136 个单元格) + 103 个外部工具字段  

## 一、核心审计结论汇总

| 数据类别 | 字段数 | 审计总格数 | 一致匹配格数 | Excel 缺失 | JSON 缺失 | 数值/格式差异 | 匹配率 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **招股书字段** | 70 | 3290 | 3290 | 0 | 0 | 0 | **100.00%** |
| **配发公告字段** | 18 | 846 | 846 | 0 | 0 | 0 | **100.00%** |
| **合计 (88 字段)** | 88 | 4136 | 4136 | 0 | 0 | 0 | **100.00%** |

### 关键发现点：
1. **总单元格数**：4136 个，匹配格数：4136（匹配率：100.00%）；
2. **差异统计**：Excel 缺失 0 项，JSON 缺失 0 项，数值不匹配 0 项；
   其中匹配格内有 265 格两边均缺失，不是已核实的证据，不能计入证据覆盖率；
3. **外部/工具衍生字段**：共 103 列；全量填报 71 列，部分填报 9 列，未填报或仅有缺失占位 23 列。此统计与上方 88 字段逐格对账是不同范围。

## 二、差异明细清单 (Discrepancies)

✅ **未发现任何字段差异，所有单元格均完全一致！**

## 三、103 个外部/工具衍生字段填报审计

| 列 | 字段说明 | 对应生成工具 | 填报数 / 总数 | 填报率 | 抽样值 |
|---|---|---|---:|---:|---|
| `V` | Filing price revision (%) | `src/academic_derivations.py (Pricing revision)` | 47/47 | 100.0% | `0` |
| `W` | Filing range width (%) | `src/academic_derivations.py (Filing range width)` | 47/47 | 100.0% | `0` |
| `X` | Pricing position in filing ran | `src/academic_derivations.py (Pricing position in range)` | 47/47 | 100.0% | `Fixed price` |
| `BC` | Comments (nearest sales& profi | `Manual / Prospectus disclosure notes (Annualization factor)` | 47/47 | 100.0% | `0.25` |
| `BU` | Listing board | `tools/external/flags.py (Listing board)` | 47/47 | 100.0% | `Main Board` |
| `BW` | A+H issuer flag | `tools/external/flags.py (A+H flag)` | 47/47 | 100.0% | `0` |
| `BX` | WVR flag | `tools/external/flags.py (WVR flag)` | 47/47 | 100.0% | `0` |
| `BY` | Chapter 18A flag | `tools/external/flags.py (Chapter 18A flag)` | 47/47 | 100.0% | `0` |
| `BZ` | Chapter 18C flag | `tools/external/flags.py (Chapter 18C flag)` | 47/47 | 100.0% | `0` |
| `CA` | Industry classification code | `tools/external/hsic_codes.py (Industry classification code)` | 47/47 | 100.0% | `281010` |
| `CB` | Industry classification system | `tools/external/hsic_codes.py (Industry classification system)` | 47/47 | 100.0% | `HSICS (Hang Seng Industry` |
| `CD` | Firm age at IPO (years) | `src/academic_derivations.py (Firm age at IPO)` | 46/47 | 97.9% | `12.7` |
| `CE` | Place of incorporation | `tools/external/flags.py (Place of incorporation)` | 46/47 | 97.9% | `PRC` |
| `CG` | Financial statement unit multi | `Manual / Disclosure notes (Financial statement unit multiplier)` | 14/47 | 29.8% | `1000` |
| `CI` | Year-3 financial period start | `Manual / Disclosure notes (Financial period: Year-3 start)` | 47/47 | 100.0% | `2023-01-01` |
| `CJ` | Year-3 financial period end | `Manual / Disclosure notes (Financial period: Year-3 end)` | 47/47 | 100.0% | `2023-12-31` |
| `CK` | Year-2 financial period start | `Manual / Disclosure notes (Financial period: Year-2 start)` | 47/47 | 100.0% | `2024-01-01` |
| `CL` | Year-2 financial period end | `Manual / Disclosure notes (Financial period: Year-2 end)` | 47/47 | 100.0% | `2024-12-31` |
| `CM` | Year-1 financial period start | `Manual / Disclosure notes (Financial period: Year-1 start)` | 47/47 | 100.0% | `2025-01-01` |
| `CN` | Year-1 net sales (original, pr | `Manual / Disclosure notes (Financial: Year-1 net sales original)` | 47/47 | 100.0% | `135942000` |
| `CO` | Year-1 profit before tax (orig | `Manual / Disclosure notes (Financial: Year-1 profit before tax original)` | 47/47 | 100.0% | `11427000` |
| `CP` | Year-1 profit for period (orig | `Manual / Disclosure notes (Financial: Year-1 profit for period original)` | 47/47 | 100.0% | `12815000` |
| `CZ` | Earliest cornerstone unlock da | `tools/external/flags.py / src/cornerstone.py (Earliest cornerstone unlock date)` | 32/47 | 68.1% | `2026-04-15` |
| `DK` | Greenshoe exercise rate (%) | `src/academic_derivations.py (Greenshoe exercise rate)` | 47/47 | 100.0% | `0` |
| `DS` | HSI return over 20 trading day | `tools/external/market.py (HSI 20-day return)` | 47/47 | 100.0% | `0.05943721` |
| `DT` | HK ordinary IPO count in 90 ca | `tools/external/ipo_count.py (90-day HK ordinary IPO count)` | 47/47 | 100.0% | `24` |
| `DU` | 1-month HIBOR before prospectu | `tools/external/hkma_import.py (1-month HIBOR)` | 47/47 | 100.0% | `0.0362202` |
| `DV` | Banking system aggregate balan | `tools/external/hkma_import.py (Aggregate Balance)` | 47/47 | 100.0% | `54208000000` |
| `DW` | First trading day closing pric | `tools/external/market.py (First day close)` | 47/47 | 100.0% | `38.5` |
| `DX` | First-day return / Underpricin | `src/academic_derivations.py (First-day return / Underpricing)` | 47/47 | 100.0% | `1.610169` |
| `DY` | Money left on the table (HK$) | `src/academic_derivations.py (Money left on the table)` | 47/47 | 100.0% | `978452500` |
| `DZ` | First trading day opening pric | `tools/external/market.py (First day open)` | 47/47 | 100.0% | `47` |
| `EA` | First trading day high (HK$) | `tools/external/market.py (First day high)` | 47/47 | 100.0% | `48.8` |
| `EB` | First trading day low (HK$) | `tools/external/market.py (First day low)` | 47/47 | 100.0% | `37.46` |
| `EC` | First trading day volume (shar | `tools/external/market.py (First day volume)` | 47/47 | 100.0% | `13550698` |
| `ED` | First-day flipping ratio (%) | `src/academic_derivations.py (First-day flipping ratio)` | 47/47 | 100.0% | `0.328916` |
| `EE` | First trading day turnover (HK | `tools/external/market.py (First day turnover)` | 0/47 | 0.0% | `—` |
| `EF` | Offer mechanism | `tools/external/rules.py (Offer mechanism)` | 43/47 | 91.5% | `Mechanism B` |
| `EG` | Applicable IPO rules / transit | `tools/external/rules.py (Applicable IPO rules)` | 47/47 | 100.0% | `FINI (from 22/11/2023); 2` |
| `EI` | Current listing status | `tools/external/aftermarket.py (Current listing status)` | 47/47 | 100.0% | `Active` |
| `EJ` | 1-month post-IPO close price ( | `tools/external/aftermarket.py (1-month close price)` | 47/47 | 100.0% | `29.34` |
| `EK` | 1-month BHR from Day-1 close ( | `tools/external/aftermarket.py (1-month BHR)` | 47/47 | 100.0% | `-0.237922` |
| `EL` | 1-month total return from offe | `tools/external/aftermarket.py (1-month total return)` | 47/47 | 100.0% | `0.989153` |
| `EM` | 1-month HSI return (%) | `tools/external/aftermarket.py (1-month HSI return)` | 47/47 | 100.0% | `-0.033323` |
| `EN` | 1-month HSTECH return (%) | `tools/external/aftermarket.py (1-month HSTECH return)` | 47/47 | 100.0% | `-0.111808` |
| `EO` | 1-month wealth relative vs HSI | `tools/external/aftermarket.py (1-month WR vs HSI)` | 47/47 | 100.0% | `0.7883` |
| `EP` | 1-month wealth relative vs HST | `tools/external/aftermarket.py (1-month WR vs HSTECH)` | 47/47 | 100.0% | `0.858` |
| `EQ` | 1-month average daily turnover | `tools/external/aftermarket.py (1-month average daily turnover)` | 47/47 | 100.0% | `48591755` |
| `ER` | 6-month post-IPO close price ( | `tools/external/aftermarket.py (6-month close price)` | 47/47 | 100.0% | `23.08` |
| `ES` | 6-month BHR from Day-1 close ( | `tools/external/aftermarket.py (6-month BHR)` | 47/47 | 100.0% | `-0.400519` |
| `ET` | 6-month total return from offe | `tools/external/aftermarket.py (6-month total return)` | 47/47 | 100.0% | `0.564746` |
| `EU` | 6-month HSI return (%) | `tools/external/aftermarket.py (6-month HSI return)` | 47/47 | 100.0% | `-0.034903` |
| `EV` | 6-month HSTECH return (%) | `tools/external/aftermarket.py (6-month HSTECH return)` | 47/47 | 100.0% | `-0.244227` |
| `EW` | 6-month wealth relative vs HSI | `tools/external/aftermarket.py (6-month WR vs HSI)` | 47/47 | 100.0% | `0.6212` |
| `EX` | 6-month wealth relative vs HST | `tools/external/aftermarket.py (6-month WR vs HSTECH)` | 47/47 | 100.0% | `0.7932` |
| `EY` | 6-month average daily turnover | `tools/external/aftermarket.py (6-month average daily turnover)` | 47/47 | 100.0% | `42844470` |
| `EZ` | Liquidity decay ratio (6M vs D | `tools/external/aftermarket.py (Liquidity decay ratio)` | 47/47 | 100.0% | `0.07013` |
| `FA` | 1-year post-IPO return (%) [Re | `tools/external/aftermarket.py (1-year return [Reserved])` | 0/47 | 0.0% | `—` |
| `FB` | 1-year wealth relative vs HSI  | `tools/external/aftermarket.py (1-year WR vs HSI [Reserved])` | 0/47 | 0.0% | `—` |
| `FC` | 3-year post-IPO return (%) [Re | `tools/external/aftermarket.py (3-year return [Reserved])` | 0/47 | 0.0% | `—` |
| `FD` | 3-year wealth relative vs HSI  | `tools/external/aftermarket.py (3-year WR vs HSI [Reserved])` | 0/47 | 0.0% | `—` |
| `FE` | 18A/18C regulatory milestone s | `tools/external/aftermarket.py (18A/18C regulatory status)` | 47/47 | 100.0% | `Standard` |
| `FF` | Stabilizing manager | `src/write_back_expansion.py (Stabilizing manager)` | 0/47 | 0.0% | `—` |
| `FG` | Stabilization period end date | `src/write_back_expansion.py (Stabilization period end date)` | 0/47 | 0.0% | `—` |
| `FH` | Stabilization purchases occurr | `src/write_back_expansion.py (Stabilization purchases occurred)` | 0/47 | 0.0% | `—` |
| `FI` | Over-allocation shares | `src/write_back_expansion.py (Over-allocation shares)` | 0/47 | 0.0% | `—` |
| `FJ` | Over-allocation (% of base off | `src/write_back_expansion.py (Over-allocation pct)` | 0/47 | 0.0% | `—` |
| `FK` | Over-allotment option exercise | `src/write_back_expansion.py (Over-allotment exercise date)` | 0/47 | 0.0% | `—` |
| `FL` | Shares issued under over-allot | `src/write_back_expansion.py (Shares issued under option)` | 0/47 | 0.0% | `—` |
| `FM` | Over-allotment exercise percen | `src/write_back_expansion.py (Over-allotment exercise percentage)` | 0/47 | 0.0% | `—` |
| `FN` | Post-stabilization cliff retur | `src/write_back_expansion.py (Cliff return m5 p5)` | 0/47 | 0.0% | `—` |
| `FO` | Post-stabilization 20-day retu | `src/write_back_expansion.py (Post-stabilization return p20)` | 0/47 | 0.0% | `—` |
| `FP` | Post-stabilization volume deca | `src/write_back_expansion.py (Post-stabilization volume decay)` | 0/47 | 0.0% | `—` |
| `FQ` | Day-5 BHR from Day-1 close (%) | `src/write_back_expansion.py (Day-5 BHR)` | 47/47 | 100.0% | `-0.281558` |
| `FR` | Day-5 wealth relative vs HSI | `src/write_back_expansion.py (Day-5 WR vs HSI)` | 47/47 | 100.0% | `0.7576` |
| `FS` | Day-20 BHR from Day-1 close (% | `src/write_back_expansion.py (Day-20 BHR)` | 47/47 | 100.0% | `-0.237922` |
| `FT` | Day-20 wealth relative vs HSI | `src/write_back_expansion.py (Day-20 WR vs HSI)` | 47/47 | 100.0% | `0.7883` |
| `FU` | 3-month BHR from Day-1 close ( | `src/write_back_expansion.py (3-month BHR)` | 47/47 | 100.0% | `-0.158442` |
| `FV` | 3-month wealth relative vs HSI | `src/write_back_expansion.py (3-month WR vs HSI)` | 47/47 | 100.0% | `0.8634` |
| `FW` | 3-month wealth relative vs HST | `src/write_back_expansion.py (3-month WR vs HSTECH)` | 47/47 | 100.0% | `0.9654` |
| `FX` | 3-month average daily turnover | `src/write_back_expansion.py (3-month avg daily turnover)` | 47/47 | 100.0% | `21991390.48` |
| `FY` | Amihud illiquidity (6M mean) | `src/write_back_expansion.py (Amihud illiquidity 6M mean)` | 47/47 | 100.0% | `0.002482314049586777` |
| `FZ` | Zero-volume days count (first  | `src/write_back_expansion.py (Zero-volume days count 6M)` | 47/47 | 100.0% | `0` |
| `GA` | Return volatility (first 6M da | `src/write_back_expansion.py (Return volatility 6M)` | 47/47 | 100.0% | `0.1524316750458491` |
| `GB` | Maximum drawdown (first 6M, %) | `src/write_back_expansion.py (Maximum drawdown 6M)` | 47/47 | 100.0% | `0.545902` |
| `GC` | Controlling shareholder 6-mont | `src/write_back_expansion.py (Controlling shareholder 6M disposal expiry)` | 0/47 | 0.0% | `—` |
| `GD` | Controlling shareholder 12-mon | `src/write_back_expansion.py (Controlling shareholder 12M control expiry)` | 0/47 | 0.0% | `—` |
| `GE` | Cornerstone unlock CAR [-5, +5 | `src/write_back_expansion.py (Cornerstone unlock CAR m5 p5)` | 0/47 | 0.0% | `—` |
| `GF` | Cornerstone unlock CAR [-20, + | `src/write_back_expansion.py (Cornerstone unlock CAR m20 p20)` | 0/47 | 0.0% | `—` |
| `GG` | Cornerstone unlock volume shoc | `src/write_back_expansion.py (Cornerstone unlock volume shock ratio)` | 0/47 | 0.0% | `—` |
| `GH` | Lead sponsor name | `src/write_back_expansion.py (Lead sponsor name)` | 47/47 | 100.0% | `CITIC Securities (Hong Ko` |
| `GI` | Joint sponsor count | `src/write_back_expansion.py (Joint sponsor count)` | 47/47 | 100.0% | `2` |
| `GJ` | Sponsor commercial bank affili | `src/write_back_expansion.py (Sponsor bank affiliate flag)` | 47/47 | 100.0% | `1` |
| `GK` | Underwriting base commission r | `src/write_back_expansion.py (Underwriting base commission rate)` | 47/47 | 100.0% | `0.03` |
| `GL` | Underwriting discretionary inc | `src/write_back_expansion.py (Underwriting incentive fee rate)` | 0/47 | 0.0% | `—` |
| `GM` | Total underwriting fee rate (% | `src/write_back_expansion.py (Total underwriting fee rate)` | 0/47 | 0.0% | `—` |
| `GN` | Cornerstone investor count | `src/write_back_expansion.py (Cornerstone investor count)` | 47/47 | 100.0% | `0` |
| `GO` | Cornerstone state-owned presen | `src/write_back_expansion.py (Cornerstone state-owned flag)` | 46/47 | 97.9% | `0` |
| `GP` | Crossover fund presence flag | `src/write_back_expansion.py (Crossover fund flag)` | 46/47 | 97.9% | `0` |
| `GQ` | Pre-IPO institutional investor | `src/write_back_expansion.py (Pre-IPO investor count)` | 46/47 | 97.9% | `55` |
| `GR` | Pre-IPO state-owned backing fl | `src/write_back_expansion.py (Pre-IPO state-owned flag)` | 46/47 | 97.9% | `1` |
| `GS` | FINI digital settlement regime | `src/write_back_expansion.py (FINI digital settlement regime)` | 47/47 | 100.0% | `POST_FINI` |
| `GT` | 2025 pricing reform regime | `src/write_back_expansion.py (2025 pricing reform regime)` | 47/47 | 100.0% | `POST_2025_REFORM` |

## 四、47 家公司流水线门禁状态 (Pipeline State)

| 股票代码 | 招股书 extracted | 招股书 validated | 招股书 reviewed | 配发 extracted | 配发 validated | 配发 reviewed | 当前写入状态 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| `0638.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `0699.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `0800.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `1384.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2026.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2396.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2408.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2539.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2546.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2575.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2579.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2581.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2630.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2635.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2637.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2650.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2652.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2655.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2657.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2658.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2659.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2661.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2670.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2671.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2676.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2685.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2687.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2691.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2693.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2695.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2698.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2718.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `2788.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `3317.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `3378.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `3696.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `3881.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `3887.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `6031.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `6166.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `6600.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `6651.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `6687.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `6980.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `7618.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `9609.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
| `9927.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
