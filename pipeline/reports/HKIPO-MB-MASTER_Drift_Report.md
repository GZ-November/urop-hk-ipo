# Master 面板漂移报告 (2025Q1 ~ 2026Q3)

- **生成时间**：2026-10-03 15:42:09 | **cohort 数**：5 | **样本合计**：155 家 | **变量数**：202
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
| 2026Q3 | 30 | 无 |

✅ 无跨 cohort 重复股票代码。

## 4. 上市日期与 cohort 季度一致性（警告级）

全部样本的上市日期落在所属 cohort 的自然季度内。

## 5. 填报率监控（任一 cohort < 100% 的列）

| 变量 | 2025Q1 | 2025Q2 | 2026Q1 | 2026Q2 | 2026Q3 |
|---|---|---|---|---|---|
| `HKEx file# of the year` | 100.0% | 100.0% | 100.0% | 100.0% | 96.7% |
| `Sponsor(s)` | 100.0% | 100.0% | 100.0% | 100.0% | 96.7% |
| `Reporting Accountants` | 100.0% | 100.0% | 100.0% | 100.0% | 96.7% |
| `Valuer(s)` | 13.3% | 7.4% | 21.1% | 13.3% | 6.7% |
| `Funds Raised HK (a)` | 100.0% | 100.0% | 100.0% | 100.0% | 96.7% |
| `Funds Raised Int.(b)` | 100.0% | 100.0% | 100.0% | 100.0% | 96.7% |
| `Number of offer shares under the capitalization Issue` | 100.0% | 100.0% | 100.0% | 100.0% | 83.3% |
| `Number of offer shares under Capitalization Rest` | 100.0% | 100.0% | 100.0% | 100.0% | 83.3% |
| `Minimum Offer Price` | 100.0% | 96.3% | 68.4% | 82.2% | 63.3% |
| `total assets in year-3 (3 years before IPO)` | 100.0% | 85.2% | 100.0% | 84.4% | 100.0% |
| `total assets in year-1` | 93.3% | 96.3% | 100.0% | 95.6% | 100.0% |
| `total equity in year-3` | 100.0% | 88.9% | 100.0% | 84.4% | 100.0% |
| `total equity in year-1` | 93.3% | 96.3% | 100.0% | 95.6% | 100.0% |
| `total liability in year-3` | 100.0% | 85.2% | 100.0% | 84.4% | 100.0% |
| `total liability in year-1` | 93.3% | 96.3% | 100.0% | 95.6% | 100.0% |
| `Net sales in year-3` | 86.7% | 88.9% | 100.0% | 86.7% | 100.0% |
| `Net sales in year-2` | 86.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `Net sales in year-1` | 86.7% | 96.3% | 100.0% | 100.0% | 100.0% |
| `Profit before tax in year-3` | 100.0% | 85.2% | 100.0% | 84.4% | 100.0% |
| `Profit before tax in year-1` | 93.3% | 96.3% | 100.0% | 97.8% | 100.0% |
| `Profit for the year in year-3` | 100.0% | 85.2% | 100.0% | 84.4% | 100.0% |
| `Profit for the year in year-1` | 93.3% | 96.3% | 100.0% | 97.8% | 100.0% |
| `Underwriting Commission (% of fund raised HK (a)` | 100.0% | 92.6% | 100.0% | 97.8% | 100.0% |
| `Underwriting Commission (% of fund raised Int.(b)` | 100.0% | 92.6% | 100.0% | 97.8% | 100.0% |
| `Over-allotment Option (%)` | 100.0% | 88.9% | 100.0% | 88.9% | 96.7% |
| `Operating cash flow in year-1 (before annualization)` | 93.3% | 96.3% | 100.0% | 95.6% | 100.0% |
| `Cash and cash equivalents at year-1 end` | 93.3% | 100.0% | 100.0% | 95.6% | 100.0% |
| `R&D expensed in year-1 (before annualization)` | 73.3% | 81.5% | 92.1% | 93.3% | 96.7% |
| `Development costs capitalized in year-1 (additions, before annualization)` | 80.0% | 85.2% | 100.0% | 93.3% | 80.0% |
| `Top 5 customers (% of year-1 revenue)` | 80.0% | 85.2% | 100.0% | 84.4% | 76.7% |
| `Pre-IPO VC/PE backing (1=yes; 0=no)` | 100.0% | 77.8% | 100.0% | 100.0% | 76.7% |
| `Pre-IPO VC backing (1=yes; 0=no)` | 100.0% | 70.4% | 100.0% | 100.0% | 70.0% |
| `Pre-IPO PE backing (1=yes; 0=no)` | 100.0% | 77.8% | 100.0% | 100.0% | 76.7% |
| `Pre-IPO CVC backing (1=yes; 0=no)` | 93.3% | 59.3% | 100.0% | 77.8% | 70.0% |
| `Pre-IPO State/Gov backing (1=yes; 0=no)` | 100.0% | 63.0% | 100.0% | 86.7% | 73.3% |
| `Top-tier VC/PE backing (1=yes; 0=no)` | 86.7% | 40.7% | 100.0% | 68.9% | 46.7% |
| `Key Pre-IPO investors` | 66.7% | 74.1% | 73.7% | 84.4% | 73.3% |
| `Pre-IPO institutional shareholding (%)` | 66.7% | 55.6% | 100.0% | 82.2% | 63.3% |
| `Pre-IPO investor board seat (1=yes; 0=no)` | 100.0% | 100.0% | 100.0% | 88.9% | 56.7% |
| `Earliest Pre-IPO investment round` | 53.3% | 74.1% | 73.7% | 84.4% | 70.0% |
| `Pre-IPO holding duration (years)` | 53.3% | 55.6% | 100.0% | 80.0% | 66.7% |
| `Controller economic interest at listing (%)` | 93.3% | 100.0% | 100.0% | 95.6% | 96.7% |
| `Controller voting rights at listing (%)` | 93.3% | 100.0% | 100.0% | 95.6% | 100.0% |
| `Interest-bearing debt at year-1 end` | 86.7% | 100.0% | 100.0% | 97.8% | 100.0% |
| `Technology commercialization stage` | 53.3% | 51.9% | 100.0% | 84.4% | 90.0% |
| `Debt repayment (% of planned net IPO proceeds)` | 100.0% | 92.6% | 100.0% | 97.8% | 100.0% |
| `Place of incorporation` | 100.0% | 88.9% | 100.0% | 22.2% | 96.7% |
| `Financial statement unit multiplier` | 53.3% | 92.6% | 100.0% | 91.1% | 53.3% |
| `Year-1 net sales (original, pre-annualization)` | 86.7% | 96.3% | 100.0% | 100.0% | 100.0% |
| `Year-1 profit before tax (original)` | 93.3% | 96.3% | 100.0% | 97.8% | 100.0% |
| `Year-1 profit for period (original)` | 93.3% | 96.3% | 100.0% | 97.8% | 100.0% |
| `H shares after IPO (base; no options)` | 80.0% | 100.0% | 100.0% | 100.0% | 96.7% |
| `Gross profit in year-1` | 86.7% | 92.6% | 100.0% | 95.6% | 100.0% |
| `Capital expenditure in year-1` | 93.3% | 100.0% | 100.0% | 95.6% | 100.0% |
| `Audit opinion (year-1)` | 93.3% | 100.0% | 100.0% | 95.6% | 96.7% |
| `Listing expenses (HK$)` | 100.0% | 100.0% | 100.0% | 100.0% | 93.3% |
| `Cornerstone investor names` | 73.3% | 92.6% | 89.5% | 82.2% | 80.0% |
| `Earliest cornerstone unlock date (dd/mm/yy)` | 73.3% | 92.6% | 89.5% | 82.2% | 80.0% |
| `Pricing date` | 93.3% | 59.3% | 73.7% | 42.2% | 40.0% |
| `Over-allotment shares actually issued` | 100.0% | 100.0% | 100.0% | 100.0% | 63.3% |
| `Actual clawback / reallocation description` | 100.0% | 100.0% | 100.0% | 97.8% | 100.0% |
| `Public shareholding at listing (%)` | 86.7% | 96.3% | 100.0% | 97.8% | 100.0% |
| `Unrestricted public shareholding at listing (%)` | 100.0% | 100.0% | 100.0% | 97.8% | 100.0% |
| `Free float denominator description` | 100.0% | 100.0% | 100.0% | 97.8% | 100.0% |
| `Free float denominator shares` | 100.0% | 100.0% | 100.0% | 97.8% | 100.0% |
| `First trading day turnover (HK$)` | 100.0% | 100.0% | 100.0% | 100.0% | 76.7% |
| `Offer mechanism` | 100.0% | 100.0% | 100.0% | 93.3% | 100.0% |
| `Company Chinese Name` | 100.0% | 88.9% | 97.4% | 97.8% | 96.7% |
| `1-month post-IPO close price (HK$)` | 100.0% | 100.0% | 97.4% | 100.0% | 66.7% |
| `1-month BHR from Day-1 close (%)` | 100.0% | 100.0% | 97.4% | 100.0% | 66.7% |
| `1-month total return from offer price (%)` | 100.0% | 100.0% | 97.4% | 100.0% | 66.7% |
| `1-month HSI return (%)` | 100.0% | 100.0% | 97.4% | 100.0% | 66.7% |
| `1-month HSTECH return (%)` | 100.0% | 100.0% | 97.4% | 100.0% | 66.7% |
| `1-month wealth relative vs HSI` | 100.0% | 100.0% | 97.4% | 100.0% | 66.7% |
| `1-month wealth relative vs HSTECH` | 100.0% | 100.0% | 97.4% | 100.0% | 66.7% |
| `1-month average daily turnover (HK$)` | 100.0% | 100.0% | 97.4% | 100.0% | 66.7% |
| `6-month post-IPO close price (HK$)` | 100.0% | 100.0% | 97.4% | 0.0% | 0.0% |
| `6-month BHR from Day-1 close (%)` | 100.0% | 100.0% | 97.4% | 0.0% | 0.0% |
| `6-month total return from offer price (%)` | 100.0% | 100.0% | 97.4% | 0.0% | 0.0% |
| `6-month HSI return (%)` | 100.0% | 100.0% | 97.4% | 0.0% | 0.0% |
| `6-month HSTECH return (%)` | 100.0% | 100.0% | 97.4% | 0.0% | 0.0% |
| `6-month wealth relative vs HSI` | 100.0% | 100.0% | 97.4% | 0.0% | 0.0% |
| `6-month wealth relative vs HSTECH` | 100.0% | 100.0% | 97.4% | 0.0% | 0.0% |
| `6-month average daily turnover (HK$)` | 100.0% | 100.0% | 97.4% | 0.0% | 0.0% |
| `Liquidity decay ratio (6M vs Day-1 turnover)` | 100.0% | 100.0% | 97.4% | 0.0% | 0.0% |
| `1-year post-IPO return (%) [Reserved]` | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `1-year wealth relative vs HSI [Reserved]` | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `3-year post-IPO return (%) [Reserved]` | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `3-year wealth relative vs HSI [Reserved]` | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `Stabilizing manager` | 100.0% | 100.0% | 50.0% | 48.9% | 36.7% |
| `Stabilization period end date` | 100.0% | 100.0% | 39.5% | 22.2% | 20.0% |
| `Stabilization purchases occurred` | 100.0% | 100.0% | 18.4% | 22.2% | 3.3% |
| `Over-allocation shares` | 100.0% | 100.0% | 39.5% | 24.4% | 23.3% |
| `Over-allocation (% of base offer)` | 100.0% | 100.0% | 36.8% | 20.0% | 26.7% |
| `Over-allotment option exercise date` | 100.0% | 100.0% | 92.1% | 84.4% | 60.0% |
| `Shares issued under over-allotment option` | 100.0% | 100.0% | 57.9% | 68.9% | 56.7% |
| `Over-allotment exercise percentage (%)` | 100.0% | 100.0% | 60.5% | 71.1% | 60.0% |
| `Post-stabilization cliff return [-5, +5] (%)` | 100.0% | 100.0% | 39.5% | 22.2% | 20.0% |
| `Post-stabilization 20-day return [0, +20] (%)` | 100.0% | 100.0% | 39.5% | 22.2% | 20.0% |
| `Post-stabilization volume decay ratio (%)` | 100.0% | 100.0% | 39.5% | 22.2% | 20.0% |
| `Day-5 BHR from Day-1 close (%)` | 100.0% | 100.0% | 100.0% | 100.0% | 76.7% |
| `Day-5 wealth relative vs HSI` | 100.0% | 100.0% | 100.0% | 100.0% | 76.7% |
| `Day-20 BHR from Day-1 close (%)` | 100.0% | 100.0% | 97.4% | 100.0% | 66.7% |
| `Day-20 wealth relative vs HSI` | 100.0% | 100.0% | 97.4% | 100.0% | 60.0% |
| `3-month BHR from Day-1 close (%)` | 100.0% | 100.0% | 97.4% | 100.0% | 0.0% |
| `3-month wealth relative vs HSI` | 100.0% | 100.0% | 97.4% | 62.2% | 0.0% |
| `3-month wealth relative vs HSTECH` | 100.0% | 100.0% | 97.4% | 62.2% | 0.0% |
| `3-month average daily turnover (HK$)` | 100.0% | 100.0% | 97.4% | 100.0% | 0.0% |
| `Amihud illiquidity (6M mean)` | 100.0% | 100.0% | 71.1% | 0.0% | 0.0% |
| `Zero-volume days count (first 6M)` | 100.0% | 100.0% | 71.1% | 0.0% | 0.0% |
| `Return volatility (first 6M daily std dev, %)` | 100.0% | 100.0% | 71.1% | 0.0% | 0.0% |
| `Maximum drawdown (first 6M, %)` | 100.0% | 100.0% | 71.1% | 0.0% | 0.0% |
| `Controlling shareholder 6-month disposal lockup expiry date` | 100.0% | 100.0% | 71.1% | 71.1% | 56.7% |
| `Controlling shareholder 12-month cessation of control expiry date` | 100.0% | 100.0% | 73.7% | 75.6% | 63.3% |
| `Cornerstone unlock CAR [-5, +5] (%)` | 73.3% | 92.6% | 65.8% | 0.0% | 0.0% |
| `Cornerstone unlock CAR [-20, +20] (%)` | 73.3% | 92.6% | 57.9% | 0.0% | 0.0% |
| `Cornerstone unlock volume shock ratio` | 73.3% | 92.6% | 57.9% | 0.0% | 0.0% |
| `Lead sponsor name` | 100.0% | 100.0% | 100.0% | 100.0% | 76.7% |
| `Joint sponsor count` | 100.0% | 100.0% | 100.0% | 100.0% | 76.7% |
| `Sponsor commercial bank affiliate flag` | 100.0% | 100.0% | 100.0% | 100.0% | 76.7% |
| `Underwriting base commission rate (%)` | 100.0% | 100.0% | 100.0% | 100.0% | 76.7% |
| `Underwriting discretionary incentive fee rate (%)` | 100.0% | 100.0% | 0.0% | 100.0% | 76.7% |
| `Total underwriting fee rate (%)` | 100.0% | 100.0% | 0.0% | 100.0% | 76.7% |
| `Cornerstone investor count` | 100.0% | 100.0% | 100.0% | 17.8% | 76.7% |
| `Cornerstone state-owned presence flag` | 100.0% | 100.0% | 100.0% | 100.0% | 76.7% |
| `Crossover fund presence flag` | 100.0% | 100.0% | 100.0% | 100.0% | 76.7% |
| `Pre-IPO institutional investor count` | 100.0% | 100.0% | 100.0% | 100.0% | 76.7% |
| `Pre-IPO state-owned backing flag` | 100.0% | 100.0% | 100.0% | 100.0% | 76.7% |

### 5.1 填报率环比（最近两个 cohort，|Δ| ≥ 10pp）

| 变量 | 上一 cohort | 最新 cohort | 变化 |
|---|---|---|---|
| `Number of offer shares under the capitalization Issue` | 100.0% | 83.3% | -16.7pp |
| `Number of offer shares under Capitalization Rest` | 100.0% | 83.3% | -16.7pp |
| `Minimum Offer Price` | 82.2% | 63.3% | -18.9pp |
| `total assets in year-3 (3 years before IPO)` | 84.4% | 100.0% | +15.6pp |
| `total equity in year-3` | 84.4% | 100.0% | +15.6pp |
| `total liability in year-3` | 84.4% | 100.0% | +15.6pp |
| `Net sales in year-3` | 86.7% | 100.0% | +13.3pp |
| `Profit before tax in year-3` | 84.4% | 100.0% | +15.6pp |
| `Profit for the year in year-3` | 84.4% | 100.0% | +15.6pp |
| `Development costs capitalized in year-1 (additions, before annualization)` | 93.3% | 80.0% | -13.3pp |
| `Pre-IPO VC/PE backing (1=yes; 0=no)` | 100.0% | 76.7% | -23.3pp |
| `Pre-IPO VC backing (1=yes; 0=no)` | 100.0% | 70.0% | -30.0pp |
| `Pre-IPO PE backing (1=yes; 0=no)` | 100.0% | 76.7% | -23.3pp |
| `Pre-IPO State/Gov backing (1=yes; 0=no)` | 86.7% | 73.3% | -13.4pp |
| `Top-tier VC/PE backing (1=yes; 0=no)` | 68.9% | 46.7% | -22.2pp |
| `Key Pre-IPO investors` | 84.4% | 73.3% | -11.1pp |
| `Pre-IPO institutional shareholding (%)` | 82.2% | 63.3% | -18.9pp |
| `Pre-IPO investor board seat (1=yes; 0=no)` | 88.9% | 56.7% | -32.2pp |
| `Earliest Pre-IPO investment round` | 84.4% | 70.0% | -14.4pp |
| `Pre-IPO holding duration (years)` | 80.0% | 66.7% | -13.3pp |
| `Place of incorporation` | 22.2% | 96.7% | +74.5pp |
| `Financial statement unit multiplier` | 91.1% | 53.3% | -37.8pp |
| `Over-allotment shares actually issued` | 100.0% | 63.3% | -36.7pp |
| `First trading day turnover (HK$)` | 100.0% | 76.7% | -23.3pp |
| `1-month post-IPO close price (HK$)` | 100.0% | 66.7% | -33.3pp |
| `1-month BHR from Day-1 close (%)` | 100.0% | 66.7% | -33.3pp |
| `1-month total return from offer price (%)` | 100.0% | 66.7% | -33.3pp |
| `1-month HSI return (%)` | 100.0% | 66.7% | -33.3pp |
| `1-month HSTECH return (%)` | 100.0% | 66.7% | -33.3pp |
| `1-month wealth relative vs HSI` | 100.0% | 66.7% | -33.3pp |
| `1-month wealth relative vs HSTECH` | 100.0% | 66.7% | -33.3pp |
| `1-month average daily turnover (HK$)` | 100.0% | 66.7% | -33.3pp |
| `Stabilizing manager` | 48.9% | 36.7% | -12.2pp |
| `Stabilization purchases occurred` | 22.2% | 3.3% | -18.9pp |
| `Over-allotment option exercise date` | 84.4% | 60.0% | -24.4pp |
| `Shares issued under over-allotment option` | 68.9% | 56.7% | -12.2pp |
| `Over-allotment exercise percentage (%)` | 71.1% | 60.0% | -11.1pp |
| `Day-5 BHR from Day-1 close (%)` | 100.0% | 76.7% | -23.3pp |
| `Day-5 wealth relative vs HSI` | 100.0% | 76.7% | -23.3pp |
| `Day-20 BHR from Day-1 close (%)` | 100.0% | 66.7% | -33.3pp |
| `Day-20 wealth relative vs HSI` | 100.0% | 60.0% | -40.0pp |
| `3-month BHR from Day-1 close (%)` | 100.0% | 0.0% | -100.0pp |
| `3-month wealth relative vs HSI` | 62.2% | 0.0% | -62.2pp |
| `3-month wealth relative vs HSTECH` | 62.2% | 0.0% | -62.2pp |
| `3-month average daily turnover (HK$)` | 100.0% | 0.0% | -100.0pp |
| `Controlling shareholder 6-month disposal lockup expiry date` | 71.1% | 56.7% | -14.4pp |
| `Controlling shareholder 12-month cessation of control expiry date` | 75.6% | 63.3% | -12.3pp |
| `Lead sponsor name` | 100.0% | 76.7% | -23.3pp |
| `Joint sponsor count` | 100.0% | 76.7% | -23.3pp |
| `Sponsor commercial bank affiliate flag` | 100.0% | 76.7% | -23.3pp |
| `Underwriting base commission rate (%)` | 100.0% | 76.7% | -23.3pp |
| `Underwriting discretionary incentive fee rate (%)` | 100.0% | 76.7% | -23.3pp |
| `Total underwriting fee rate (%)` | 100.0% | 76.7% | -23.3pp |
| `Cornerstone investor count` | 17.8% | 76.7% | +58.9pp |
| `Cornerstone state-owned presence flag` | 100.0% | 76.7% | -23.3pp |
| `Crossover fund presence flag` | 100.0% | 76.7% | -23.3pp |
| `Pre-IPO institutional investor count` | 100.0% | 76.7% | -23.3pp |
| `Pre-IPO state-owned backing flag` | 100.0% | 76.7% | -23.3pp |

### 5.2 布尔列覆盖警告（已确认值为 0/1，未知保留缺失）

| 布尔列 | 2025Q1 | 2025Q2 | 2026Q1 | 2026Q2 | 2026Q3 |
|---|---|---|---|---|---|
| `Pre-IPO investor board seat (1=yes; 0=no)` | 100.0% | 100.0% | 100.0% | 88.9% | 56.7% |
| `Stabilization purchases occurred` | 100.0% | 100.0% | 18.4% | 22.2% | 3.3% |
| `Sponsor commercial bank affiliate flag` | 100.0% | 100.0% | 100.0% | 100.0% | 76.7% |
| `Cornerstone state-owned presence flag` | 100.0% | 100.0% | 100.0% | 100.0% | 76.7% |
| `Crossover fund presence flag` | 100.0% | 100.0% | 100.0% | 100.0% | 76.7% |
| `Pre-IPO state-owned backing flag` | 100.0% | 100.0% | 100.0% | 100.0% | 76.7% |

处置：依字段证据规则确认有无；未知保留缺失，不得为覆盖率补 0。更新已确认值后重跑 export 与 master。

## 6. 股数恒等式校验（警告级，容差 ±1 股）

- L = N + Q：违规 0 行
- L = O + M：违规 1 行
- M = Q + P：违规 0 行

- `2026Q2` 第 38 行 6228.HK：Total (without option)=14,731,366,060 vs Number of offer shares under Capitalization Rest + Global Offering (without option)=13,924,348,660
