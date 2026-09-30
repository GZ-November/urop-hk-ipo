# Master 面板漂移报告 (2025Q1 ~ 2026Q3)

- **生成时间**：2026-09-30 18:03:45 | **cohort 数**：5 | **样本合计**：148 家 | **变量数**：202
- **复现命令**：`python3 run.py master`
- **Master 数据**：`HKIPO-MB-MASTER_clean.csv`（cohort 列已前置，本地产物不入库）
- **派生比率列**：leverage_y1, roa_y1, sales_growth_y1, log_proceeds_hkd, public_offer_fraction, sponsor_reputation_tier（免汇率，`--derive` 生成）

## 1. 表头跨 cohort 对齐：✅ 通过

全部 5 个 cohort 的 202 列表头完全一致（顺序敏感）。

## 2. 注册表校验（HKIPO_Variable_Registry.yaml）：✅ 一致

CSV 表头与注册表逐列一致（列名 + 顺序）。

## 3. 样本与重复检查

| cohort | 样本数 | cohort 内重复代码 |
|---|---|---|
| 2025Q1 | 15 | 无 |
| 2025Q2 | 27 | 无 |
| 2026Q1 | 38 | 无 |
| 2026Q2 | 45 | 无 |
| 2026Q3 | 23 | 无 |

✅ 无跨 cohort 重复股票代码。

## 4. 上市日期与 cohort 季度一致性（警告级）

全部样本的上市日期落在所属 cohort 的自然季度内。

## 5. 填报率监控（任一 cohort < 100% 的列）

| 变量 | 2025Q1 | 2025Q2 | 2026Q1 | 2026Q2 | 2026Q3 |
|---|---|---|---|---|---|
| `Valuer(s)` | 13.3% | 7.4% | 21.1% | 13.3% | 8.7% |
| `Minimum Offer Price` | 100.0% | 96.3% | 68.4% | 82.2% | 60.9% |
| `total assets in year-3 (3 years before IPO)` | 100.0% | 85.2% | 100.0% | 84.4% | 100.0% |
| `total assets in year-1` | 93.3% | 96.3% | 100.0% | 95.6% | 100.0% |
| `total equity in year-3` | 100.0% | 88.9% | 100.0% | 84.4% | 100.0% |
| `total equity in year-1` | 93.3% | 96.3% | 100.0% | 95.6% | 100.0% |
| `total liability in year-3` | 100.0% | 85.2% | 100.0% | 84.4% | 100.0% |
| `total liability in year-1` | 93.3% | 96.3% | 100.0% | 95.6% | 100.0% |
| `Net sales in year-3` | 86.7% | 88.9% | 100.0% | 84.4% | 100.0% |
| `Net sales in year-2` | 86.7% | 100.0% | 100.0% | 97.8% | 100.0% |
| `Net sales in year-1` | 86.7% | 96.3% | 100.0% | 97.8% | 100.0% |
| `Profit before tax in year-3` | 100.0% | 85.2% | 100.0% | 84.4% | 100.0% |
| `Profit before tax in year-1` | 93.3% | 96.3% | 100.0% | 97.8% | 100.0% |
| `Profit for the year in year-3` | 100.0% | 85.2% | 100.0% | 84.4% | 100.0% |
| `Profit for the year in year-1` | 93.3% | 96.3% | 100.0% | 97.8% | 100.0% |
| `Underwriting Commission (% of fund raised HK (a)` | 100.0% | 92.6% | 100.0% | 97.8% | 100.0% |
| `Underwriting Commission (% of fund raised Int.(b)` | 100.0% | 92.6% | 100.0% | 97.8% | 100.0% |
| `Over-allotment Option (%)` | 100.0% | 88.9% | 100.0% | 88.9% | 100.0% |
| `Operating cash flow in year-1 (before annualization)` | 93.3% | 96.3% | 100.0% | 95.6% | 100.0% |
| `Cash and cash equivalents at year-1 end` | 93.3% | 100.0% | 100.0% | 95.6% | 100.0% |
| `R&D expensed in year-1 (before annualization)` | 73.3% | 81.5% | 92.1% | 93.3% | 95.7% |
| `Development costs capitalized in year-1 (additions, before annualization)` | 80.0% | 85.2% | 100.0% | 93.3% | 100.0% |
| `Top 5 customers (% of year-1 revenue)` | 80.0% | 85.2% | 100.0% | 84.4% | 69.6% |
| `Pre-IPO VC/PE backing (1=yes; 0=no)` | 100.0% | 77.8% | 100.0% | 100.0% | 82.6% |
| `Pre-IPO VC backing (1=yes; 0=no)` | 100.0% | 70.4% | 100.0% | 100.0% | 78.3% |
| `Pre-IPO PE backing (1=yes; 0=no)` | 100.0% | 77.8% | 100.0% | 100.0% | 82.6% |
| `Pre-IPO CVC backing (1=yes; 0=no)` | 93.3% | 59.3% | 100.0% | 77.8% | 78.3% |
| `Pre-IPO State/Gov backing (1=yes; 0=no)` | 100.0% | 63.0% | 100.0% | 86.7% | 78.3% |
| `Top-tier VC/PE backing (1=yes; 0=no)` | 86.7% | 40.7% | 100.0% | 71.1% | 60.9% |
| `Key Pre-IPO investors` | 66.7% | 74.1% | 73.7% | 84.4% | 78.3% |
| `Pre-IPO institutional shareholding (%)` | 66.7% | 55.6% | 100.0% | 82.2% | 65.2% |
| `Pre-IPO investor board seat (1=yes; 0=no)` | 100.0% | 100.0% | 100.0% | 100.0% | 60.9% |
| `Earliest Pre-IPO investment round` | 53.3% | 74.1% | 73.7% | 84.4% | 73.9% |
| `Pre-IPO holding duration (years)` | 53.3% | 55.6% | 100.0% | 80.0% | 69.6% |
| `Controller economic interest at listing (%)` | 93.3% | 100.0% | 100.0% | 97.8% | 100.0% |
| `Controller voting rights at listing (%)` | 93.3% | 100.0% | 100.0% | 97.8% | 100.0% |
| `Interest-bearing debt at year-1 end` | 86.7% | 100.0% | 100.0% | 97.8% | 100.0% |
| `Technology commercialization stage` | 53.3% | 51.9% | 100.0% | 84.4% | 91.3% |
| `Debt repayment (% of planned net IPO proceeds)` | 100.0% | 92.6% | 100.0% | 95.6% | 100.0% |
| `Place of incorporation` | 100.0% | 88.9% | 100.0% | 22.2% | 100.0% |
| `Financial statement unit multiplier` | 53.3% | 92.6% | 100.0% | 91.1% | 39.1% |
| `Year-1 net sales (original, pre-annualization)` | 86.7% | 96.3% | 100.0% | 97.8% | 100.0% |
| `Year-1 profit before tax (original)` | 93.3% | 96.3% | 100.0% | 97.8% | 100.0% |
| `Year-1 profit for period (original)` | 93.3% | 96.3% | 100.0% | 97.8% | 100.0% |
| `H shares after IPO (base; no options)` | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `Gross profit in year-1` | 86.7% | 92.6% | 100.0% | 95.6% | 100.0% |
| `Capital expenditure in year-1` | 93.3% | 100.0% | 100.0% | 95.6% | 100.0% |
| `Audit opinion (year-1)` | 93.3% | 100.0% | 100.0% | 95.6% | 100.0% |
| `Listing expenses (HK$)` | 100.0% | 100.0% | 100.0% | 100.0% | 95.7% |
| `Cornerstone investor names` | 73.3% | 92.6% | 89.5% | 82.2% | 73.9% |
| `Earliest cornerstone unlock date (dd/mm/yy)` | 73.3% | 92.6% | 89.5% | 82.2% | 73.9% |
| `Pricing date` | 93.3% | 59.3% | 73.7% | 42.2% | 52.2% |
| `Over-allotment shares actually issued` | 100.0% | 100.0% | 100.0% | 100.0% | 78.3% |
| `Actual clawback / reallocation description` | 100.0% | 100.0% | 100.0% | 97.8% | 100.0% |
| `Public shareholding at listing (%)` | 86.7% | 96.3% | 100.0% | 97.8% | 100.0% |
| `Unrestricted public shareholding at listing (%)` | 100.0% | 100.0% | 100.0% | 97.8% | 100.0% |
| `Free float denominator description` | 100.0% | 100.0% | 100.0% | 97.8% | 100.0% |
| `Free float denominator shares` | 100.0% | 100.0% | 100.0% | 97.8% | 100.0% |
| `Offer mechanism` | 100.0% | 100.0% | 100.0% | 93.3% | 100.0% |
| `Company Chinese Name` | 100.0% | 88.9% | 97.4% | 97.8% | 95.7% |
| `1-month post-IPO close price (HK$)` | 100.0% | 100.0% | 97.4% | 100.0% | 87.0% |
| `1-month BHR from Day-1 close (%)` | 100.0% | 100.0% | 97.4% | 100.0% | 87.0% |
| `1-month total return from offer price (%)` | 100.0% | 100.0% | 97.4% | 100.0% | 87.0% |
| `1-month HSI return (%)` | 100.0% | 100.0% | 97.4% | 100.0% | 87.0% |
| `1-month HSTECH return (%)` | 100.0% | 100.0% | 97.4% | 100.0% | 87.0% |
| `1-month wealth relative vs HSI` | 100.0% | 100.0% | 97.4% | 100.0% | 87.0% |
| `1-month wealth relative vs HSTECH` | 100.0% | 100.0% | 97.4% | 100.0% | 87.0% |
| `1-month average daily turnover (HK$)` | 100.0% | 100.0% | 97.4% | 100.0% | 87.0% |
| `6-month post-IPO close price (HK$)` | 100.0% | 100.0% | 81.6% | 0.0% | 0.0% |
| `6-month BHR from Day-1 close (%)` | 100.0% | 100.0% | 81.6% | 0.0% | 0.0% |
| `6-month total return from offer price (%)` | 100.0% | 100.0% | 81.6% | 0.0% | 0.0% |
| `6-month HSI return (%)` | 100.0% | 100.0% | 81.6% | 0.0% | 0.0% |
| `6-month HSTECH return (%)` | 100.0% | 100.0% | 81.6% | 0.0% | 0.0% |
| `6-month wealth relative vs HSI` | 100.0% | 100.0% | 81.6% | 0.0% | 0.0% |
| `6-month wealth relative vs HSTECH` | 100.0% | 100.0% | 81.6% | 0.0% | 0.0% |
| `6-month average daily turnover (HK$)` | 100.0% | 100.0% | 81.6% | 0.0% | 0.0% |
| `Liquidity decay ratio (6M vs Day-1 turnover)` | 100.0% | 100.0% | 81.6% | 0.0% | 0.0% |
| `1-year post-IPO return (%) [Reserved]` | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `1-year wealth relative vs HSI [Reserved]` | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `3-year post-IPO return (%) [Reserved]` | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `3-year wealth relative vs HSI [Reserved]` | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `Stabilizing manager` | 100.0% | 100.0% | 50.0% | 48.9% | 47.8% |
| `Stabilization period end date` | 100.0% | 100.0% | 39.5% | 22.2% | 26.1% |
| `Stabilization purchases occurred` | 100.0% | 100.0% | 18.4% | 22.2% | 4.3% |
| `Over-allocation shares` | 100.0% | 100.0% | 39.5% | 24.4% | 30.4% |
| `Over-allocation (% of base offer)` | 100.0% | 100.0% | 36.8% | 20.0% | 34.8% |
| `Over-allotment option exercise date` | 100.0% | 100.0% | 92.1% | 84.4% | 78.3% |
| `Shares issued under over-allotment option` | 100.0% | 100.0% | 57.9% | 68.9% | 73.9% |
| `Over-allotment exercise percentage (%)` | 100.0% | 100.0% | 60.5% | 71.1% | 78.3% |
| `Post-stabilization cliff return [-5, +5] (%)` | 100.0% | 100.0% | 39.5% | 22.2% | 26.1% |
| `Post-stabilization 20-day return [0, +20] (%)` | 100.0% | 100.0% | 39.5% | 22.2% | 26.1% |
| `Post-stabilization volume decay ratio (%)` | 100.0% | 100.0% | 39.5% | 22.2% | 26.1% |
| `Day-20 BHR from Day-1 close (%)` | 100.0% | 100.0% | 97.4% | 100.0% | 87.0% |
| `Day-20 wealth relative vs HSI` | 100.0% | 100.0% | 97.4% | 100.0% | 78.3% |
| `3-month BHR from Day-1 close (%)` | 100.0% | 100.0% | 97.4% | 100.0% | 0.0% |
| `3-month wealth relative vs HSI` | 100.0% | 100.0% | 97.4% | 62.2% | 0.0% |
| `3-month wealth relative vs HSTECH` | 100.0% | 100.0% | 97.4% | 62.2% | 0.0% |
| `3-month average daily turnover (HK$)` | 100.0% | 100.0% | 97.4% | 100.0% | 0.0% |
| `Amihud illiquidity (6M mean)` | 100.0% | 100.0% | 71.1% | 0.0% | 0.0% |
| `Zero-volume days count (first 6M)` | 100.0% | 100.0% | 71.1% | 0.0% | 0.0% |
| `Return volatility (first 6M daily std dev, %)` | 100.0% | 100.0% | 71.1% | 0.0% | 0.0% |
| `Maximum drawdown (first 6M, %)` | 100.0% | 100.0% | 71.1% | 0.0% | 0.0% |
| `Cornerstone unlock CAR [-5, +5] (%)` | 73.3% | 92.6% | 68.4% | 0.0% | 0.0% |
| `Cornerstone unlock CAR [-20, +20] (%)` | 73.3% | 92.6% | 60.5% | 0.0% | 0.0% |
| `Cornerstone unlock volume shock ratio` | 73.3% | 92.6% | 60.5% | 0.0% | 0.0% |
| `Underwriting discretionary incentive fee rate (%)` | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% |
| `Total underwriting fee rate (%)` | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% |
| `Cornerstone investor count` | 100.0% | 100.0% | 100.0% | 17.8% | 100.0% |

### 5.1 填报率环比（最近两个 cohort，|Δ| ≥ 10pp）

| 变量 | 上一 cohort | 最新 cohort | 变化 |
|---|---|---|---|
| `Minimum Offer Price` | 82.2% | 60.9% | -21.3pp |
| `total assets in year-3 (3 years before IPO)` | 84.4% | 100.0% | +15.6pp |
| `total equity in year-3` | 84.4% | 100.0% | +15.6pp |
| `total liability in year-3` | 84.4% | 100.0% | +15.6pp |
| `Net sales in year-3` | 84.4% | 100.0% | +15.6pp |
| `Profit before tax in year-3` | 84.4% | 100.0% | +15.6pp |
| `Profit for the year in year-3` | 84.4% | 100.0% | +15.6pp |
| `Over-allotment Option (%)` | 88.9% | 100.0% | +11.1pp |
| `Top 5 customers (% of year-1 revenue)` | 84.4% | 69.6% | -14.8pp |
| `Pre-IPO VC/PE backing (1=yes; 0=no)` | 100.0% | 82.6% | -17.4pp |
| `Pre-IPO VC backing (1=yes; 0=no)` | 100.0% | 78.3% | -21.7pp |
| `Pre-IPO PE backing (1=yes; 0=no)` | 100.0% | 82.6% | -17.4pp |
| `Top-tier VC/PE backing (1=yes; 0=no)` | 71.1% | 60.9% | -10.2pp |
| `Pre-IPO institutional shareholding (%)` | 82.2% | 65.2% | -17.0pp |
| `Pre-IPO investor board seat (1=yes; 0=no)` | 100.0% | 60.9% | -39.1pp |
| `Earliest Pre-IPO investment round` | 84.4% | 73.9% | -10.5pp |
| `Pre-IPO holding duration (years)` | 80.0% | 69.6% | -10.4pp |
| `Place of incorporation` | 22.2% | 100.0% | +77.8pp |
| `Financial statement unit multiplier` | 91.1% | 39.1% | -52.0pp |
| `Pricing date` | 42.2% | 52.2% | +10.0pp |
| `Over-allotment shares actually issued` | 100.0% | 78.3% | -21.7pp |
| `1-month post-IPO close price (HK$)` | 100.0% | 87.0% | -13.0pp |
| `1-month BHR from Day-1 close (%)` | 100.0% | 87.0% | -13.0pp |
| `1-month total return from offer price (%)` | 100.0% | 87.0% | -13.0pp |
| `1-month HSI return (%)` | 100.0% | 87.0% | -13.0pp |
| `1-month HSTECH return (%)` | 100.0% | 87.0% | -13.0pp |
| `1-month wealth relative vs HSI` | 100.0% | 87.0% | -13.0pp |
| `1-month wealth relative vs HSTECH` | 100.0% | 87.0% | -13.0pp |
| `1-month average daily turnover (HK$)` | 100.0% | 87.0% | -13.0pp |
| `Stabilization purchases occurred` | 22.2% | 4.3% | -17.9pp |
| `Over-allocation (% of base offer)` | 20.0% | 34.8% | +14.8pp |
| `Day-20 BHR from Day-1 close (%)` | 100.0% | 87.0% | -13.0pp |
| `Day-20 wealth relative vs HSI` | 100.0% | 78.3% | -21.7pp |
| `3-month BHR from Day-1 close (%)` | 100.0% | 0.0% | -100.0pp |
| `3-month wealth relative vs HSI` | 62.2% | 0.0% | -62.2pp |
| `3-month wealth relative vs HSTECH` | 62.2% | 0.0% | -62.2pp |
| `3-month average daily turnover (HK$)` | 100.0% | 0.0% | -100.0pp |
| `Cornerstone investor count` | 17.8% | 100.0% | +82.2pp |

### 5.2 布尔列空值警告（约定：0/1 不得留空）

| 布尔列 | 2025Q1 | 2025Q2 | 2026Q1 | 2026Q2 | 2026Q3 |
|---|---|---|---|---|---|
| `Pre-IPO investor board seat (1=yes; 0=no)` | 100.0% | 100.0% | 100.0% | 100.0% | 60.9% |
| `Stabilization purchases occurred` | 100.0% | 100.0% | 18.4% | 22.2% | 4.3% |

处置：确认「确无」后补 0（或按手册填 NA），重跑 export 与 master。

## 6. 股数恒等式校验（警告级，容差 ±1 股）

✅ 全部可评估样本满足恒等式 L = N + Q、L = O + M、M = Q + P。
