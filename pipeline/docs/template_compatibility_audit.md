# HKIPO-MB 模板 × Pipeline 兼容性审计报告

- 模板文件: `Copy of HKIPO-MB-template-final.xlsx` (sha256: 32330d91…)
- 工作表: `NLR` | 表头行: 1 | 列数: 202 | 模板数据行: 0 (纯空白)

## 一、列解析验证 (最关键)

| Schema | 字段数 | resolve_columns 唯一命中 | 问题 |
|---|---|---|---|
| fields.json (招股书) | 70 | **70/70** | 无 |
| allot_fields.json (配发) | 18 | **18/18** | 无 |

> 注: schema 内记录的 `col` 字母为旧版布局、系统性偏移，但 `resolve_columns()` 按规范化**表头**匹配，
> 不依赖列字母，故实际可用。另: 全部 202 列表头均有实心填充色，通过 `fill_type == "solid"` 门禁。

## 二、202 列来源分布

| 来源 | 列数 |
|---|---|
| 招股书抽取 (fields.json) | 70 |
| 配发公告 (allot_fields.json) | 18 |
| HKEX 新上市报告 NLR (sample_builder.py) | 11 |
| 人工/披露附注 | 10 |
| 预留字段 (1年/3年，数据未到期) | 4 |
| src/academic_derivations.py (Pricing revision) | 1 |
| src/academic_derivations.py (Filing range width) | 1 |
| src/academic_derivations.py (Pricing position in range) | 1 |
| tools/external/flags.py (Listing board) | 1 |
| tools/external/flags.py (A+H flag) | 1 |
| tools/external/flags.py (WVR flag) | 1 |
| tools/external/flags.py (Chapter 18A flag) | 1 |
| tools/external/flags.py (Chapter 18C flag) | 1 |
| tools/external/hsic_codes.py (Industry classification code) | 1 |
| tools/external/hsic_codes.py (Industry classification system) | 1 |
| src/academic_derivations.py (Firm age at IPO) | 1 |
| tools/external/flags.py (Place of incorporation) | 1 |
| tools/external/flags.py / src/cornerstone.py (Earliest cornerstone unlock date) | 1 |
| src/academic_derivations.py (Greenshoe exercise rate) | 1 |
| tools/external/market.py (HSI 20-day return) | 1 |
| tools/external/ipo_count.py (90-day HK ordinary IPO count) | 1 |
| tools/external/hkma_import.py (1-month HIBOR) | 1 |
| tools/external/hkma_import.py (Aggregate Balance) | 1 |
| tools/external/market.py (First day close) | 1 |
| src/academic_derivations.py (First-day return / Underpricing) | 1 |
| src/academic_derivations.py (Money left on the table) | 1 |
| tools/external/market.py (First day open) | 1 |
| tools/external/market.py (First day high) | 1 |
| tools/external/market.py (First day low) | 1 |
| tools/external/market.py (First day volume) | 1 |
| src/academic_derivations.py (First-day flipping ratio) | 1 |
| tools/external/market.py (First day turnover) | 1 |
| tools/external/rules.py (Offer mechanism) | 1 |
| tools/external/rules.py (Applicable IPO rules) | 1 |
| tools/external/aftermarket.py (Current listing status) | 1 |
| tools/external/aftermarket.py (1-month close price) | 1 |
| tools/external/aftermarket.py (1-month BHR) | 1 |
| tools/external/aftermarket.py (1-month total return) | 1 |
| tools/external/aftermarket.py (1-month HSI return) | 1 |
| tools/external/aftermarket.py (1-month HSTECH return) | 1 |
| tools/external/aftermarket.py (1-month WR vs HSI) | 1 |
| tools/external/aftermarket.py (1-month WR vs HSTECH) | 1 |
| tools/external/aftermarket.py (1-month average daily turnover) | 1 |
| tools/external/aftermarket.py (6-month close price) | 1 |
| tools/external/aftermarket.py (6-month BHR) | 1 |
| tools/external/aftermarket.py (6-month total return) | 1 |
| tools/external/aftermarket.py (6-month HSI return) | 1 |
| tools/external/aftermarket.py (6-month HSTECH return) | 1 |
| tools/external/aftermarket.py (6-month WR vs HSI) | 1 |
| tools/external/aftermarket.py (6-month WR vs HSTECH) | 1 |
| tools/external/aftermarket.py (6-month average daily turnover) | 1 |
| tools/external/aftermarket.py (Liquidity decay ratio) | 1 |
| tools/external/aftermarket.py (18A/18C regulatory status) | 1 |
| src/write_back_expansion.py (Stabilizing manager) | 1 |
| src/write_back_expansion.py (Stabilization period end date) | 1 |
| src/write_back_expansion.py (Stabilization purchases occurred) | 1 |
| src/write_back_expansion.py (Over-allocation shares) | 1 |
| src/write_back_expansion.py (Over-allocation pct) | 1 |
| src/write_back_expansion.py (Over-allotment exercise date) | 1 |
| src/write_back_expansion.py (Shares issued under option) | 1 |
| src/write_back_expansion.py (Over-allotment exercise percentage) | 1 |
| src/write_back_expansion.py (Cliff return m5 p5) | 1 |
| src/write_back_expansion.py (Post-stabilization return p20) | 1 |
| src/write_back_expansion.py (Post-stabilization volume decay) | 1 |
| src/write_back_expansion.py (Day-5 BHR) | 1 |
| src/write_back_expansion.py (Day-5 WR vs HSI) | 1 |
| src/write_back_expansion.py (Day-20 BHR) | 1 |
| src/write_back_expansion.py (Day-20 WR vs HSI) | 1 |
| src/write_back_expansion.py (3-month BHR) | 1 |
| src/write_back_expansion.py (3-month WR vs HSI) | 1 |
| src/write_back_expansion.py (3-month WR vs HSTECH) | 1 |
| src/write_back_expansion.py (3-month avg daily turnover) | 1 |
| src/write_back_expansion.py (Amihud illiquidity 6M mean) | 1 |
| src/write_back_expansion.py (Zero-volume days count 6M) | 1 |
| src/write_back_expansion.py (Return volatility 6M) | 1 |
| src/write_back_expansion.py (Maximum drawdown 6M) | 1 |
| src/write_back_expansion.py (Controlling shareholder 6M disposal expiry) | 1 |
| src/write_back_expansion.py (Controlling shareholder 12M control expiry) | 1 |
| src/write_back_expansion.py (Cornerstone unlock CAR m5 p5) | 1 |
| src/write_back_expansion.py (Cornerstone unlock CAR m20 p20) | 1 |
| src/write_back_expansion.py (Cornerstone unlock volume shock ratio) | 1 |
| src/write_back_expansion.py (Lead sponsor name) | 1 |
| src/write_back_expansion.py (Joint sponsor count) | 1 |
| src/write_back_expansion.py (Sponsor bank affiliate flag) | 1 |
| src/write_back_expansion.py (Underwriting base commission rate) | 1 |
| src/write_back_expansion.py (Underwriting incentive fee rate) | 1 |
| src/write_back_expansion.py (Total underwriting fee rate) | 1 |
| src/write_back_expansion.py (Cornerstone investor count) | 1 |
| src/write_back_expansion.py (Cornerstone state-owned flag) | 1 |
| src/write_back_expansion.py (Crossover fund flag) | 1 |
| src/write_back_expansion.py (Pre-IPO investor count) | 1 |
| src/write_back_expansion.py (Pre-IPO state-owned flag) | 1 |
| src/write_back_expansion.py (FINI digital settlement regime) | 1 |
| src/write_back_expansion.py (2025 pricing reform regime) | 1 |
| **合计** | **202** |

## 三、逐列明细

| 列 | 表头 | 来源模块 | 填充方式 |
|---|---|---|---|
| A | HKEx file# of the year | HKEX 新上市报告 NLR (sample_builder.py) | 确定性解析 (0 token) |
| B | Stock Code | HKEX 新上市报告 NLR (sample_builder.py) | 确定性解析 (0 token) |
| C | Company Name at time of listing (exclude Chapter 20 cases) | HKEX 新上市报告 NLR (sample_builder.py) | 确定性解析 (0 token) |
| D | Date of Prospectus (dd/mm/yy) | HKEX 新上市报告 NLR (sample_builder.py) | 确定性解析 (0 token) |
| E | Date of Listing (dd/mm/yy) | HKEX 新上市报告 NLR (sample_builder.py) | 确定性解析 (0 token) |
| F | Sponsor(s) | HKEX 新上市报告 NLR (sample_builder.py) | 确定性解析 (0 token) |
| G | Reporting Accountants | HKEX 新上市报告 NLR (sample_builder.py) | 确定性解析 (0 token) |
| H | Valuer(s) | HKEX 新上市报告 NLR (sample_builder.py) | 确定性解析 (0 token) |
| I | Funds Raised HK (a) | HKEX 新上市报告 NLR (sample_builder.py) | 确定性解析 (0 token) |
| J | Funds Raised Int.(b) | HKEX 新上市报告 NLR (sample_builder.py) | 确定性解析 (0 token) |
| K |  IPO Subscription Price (HK$) | HKEX 新上市报告 NLR (sample_builder.py) | 确定性解析 (0 token) |
| L | Total (without option) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| M | Global Offering (without option) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| N | Number of offer shares under the capitalization Issue | 招股书抽取 (fields.json) | LLM 语义抽取 |
| O | Number of offer shares under Capitalization Rest | 招股书抽取 (fields.json) | LLM 语义抽取 |
| P | Sale Shares | 招股书抽取 (fields.json) | LLM 语义抽取 |
| Q | New shares  | 招股书抽取 (fields.json) | LLM 语义抽取 |
| R | Placing Shares | 招股书抽取 (fields.json) | LLM 语义抽取 |
| S | Public Offer shares | 招股书抽取 (fields.json) | LLM 语义抽取 |
| T | Maximum Offer Price | 招股书抽取 (fields.json) | LLM 语义抽取 |
| U | Minimum Offer Price | 招股书抽取 (fields.json) | LLM 语义抽取 |
| V | Filing price revision (%) | src/academic_derivations.py (Pricing revision) | 确定性计算 (0 token) |
| W | Filing range width (%) | src/academic_derivations.py (Filing range width) | 确定性计算 (0 token) |
| X | Pricing position in filing range | src/academic_derivations.py (Pricing position in range) | 确定性计算 (0 token) |
| Y | currency in financial information | 招股书抽取 (fields.json) | LLM 语义抽取 |
| Z | total assets in year-3 (3 years before IPO) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AA | total assets in year-2 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AB | total assets in year-1 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AC | total equity in year-3 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AD | total equity in year-2 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AE | total equity in year-1 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AF | total liability in year-3 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AG | total liability in year-2 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AH | total liability in year-1 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AI | Net sales in year-3 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AJ | Net sales in year-2 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AK | Net sales in year-1 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AL | Profit before tax in year-3 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AM | Profit before tax in year-2 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AN | Profit before tax in year-1 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AO | Profit for the year in year-3 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AP | Profit for the year in year-2 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AQ | Profit for the year in year-1 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AR | Underwriting Commission (% of fund raised HK (a) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AS | Underwriting Commission (% of fund raised Int.(b) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AT | Over-allotment Option (%) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AU | Principal business / industry | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AV | Listing route / applicable chapter | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AW | Year-1 financial period end (dd/mm/yy) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AX | Operating cash flow in year-1 (before annualization) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AY | Cash and cash equivalents at year-1 end | 招股书抽取 (fields.json) | LLM 语义抽取 |
| AZ | R&D expensed in year-1 (before annualization) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BA | Development costs capitalized in year-1 (additions, before ann | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BB | Top 5 customers (% of year-1 revenue) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BC | Comments (nearest sales& profit adjustment factor - original d | 人工/披露附注 | 人工录入 |
| BD | Pre-IPO VC/PE backing (1=yes; 0=no) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BE | Pre-IPO VC backing (1=yes; 0=no) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BF | Pre-IPO PE backing (1=yes; 0=no) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BG | Pre-IPO CVC backing (1=yes; 0=no) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BH | Pre-IPO State/Gov backing (1=yes; 0=no) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BI | Top-tier VC/PE backing (1=yes; 0=no) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BJ | Key Pre-IPO investors | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BK | Pre-IPO institutional shareholding (%) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BL | Pre-IPO investor board seat (1=yes; 0=no) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BM | Earliest Pre-IPO investment round | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BN | Pre-IPO holding duration (years) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BO | Ultimate controller type | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BP | Controller economic interest at listing (%) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BQ | Controller voting rights at listing (%) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BR | Interest-bearing debt at year-1 end | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BS | Technology commercialization stage | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BT | Debt repayment (% of planned net IPO proceeds) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BU | Listing board | tools/external/flags.py (Listing board) | 外部抓取 |
| BV | Share class | 招股书抽取 (fields.json) | LLM 语义抽取 |
| BW | A+H issuer flag | tools/external/flags.py (A+H flag) | 外部抓取 |
| BX | WVR flag | tools/external/flags.py (WVR flag) | 外部抓取 |
| BY | Chapter 18A flag | tools/external/flags.py (Chapter 18A flag) | 外部抓取 |
| BZ | Chapter 18C flag | tools/external/flags.py (Chapter 18C flag) | 外部抓取 |
| CA | Industry classification code | tools/external/hsic_codes.py (Industry classification code) | 外部抓取 |
| CB | Industry classification system and version | tools/external/hsic_codes.py (Industry classification system) | 外部抓取 |
| CC | Incorporation date | 招股书抽取 (fields.json) | LLM 语义抽取 |
| CD | Firm age at IPO (years) | src/academic_derivations.py (Firm age at IPO) | 确定性计算 (0 token) |
| CE | Place of incorporation | tools/external/flags.py (Place of incorporation) | 外部抓取 |
| CF | Principal place of business | 招股书抽取 (fields.json) | LLM 语义抽取 |
| CG | Financial statement unit multiplier | 人工/披露附注 | 人工录入 |
| CH | Accounting standard | 招股书抽取 (fields.json) | LLM 语义抽取 |
| CI | Year-3 financial period start | 人工/披露附注 | 人工录入 |
| CJ | Year-3 financial period end | 人工/披露附注 | 人工录入 |
| CK | Year-2 financial period start | 人工/披露附注 | 人工录入 |
| CL | Year-2 financial period end | 人工/披露附注 | 人工录入 |
| CM | Year-1 financial period start | 人工/披露附注 | 人工录入 |
| CN | Year-1 net sales (original, pre-annualization) | 人工/披露附注 | 人工录入 |
| CO | Year-1 profit before tax (original) | 人工/披露附注 | 人工录入 |
| CP | Year-1 profit for period (original) | 人工/披露附注 | 人工录入 |
| CQ | Subscription opening date | 招股书抽取 (fields.json) | LLM 语义抽取 |
| CR | Subscription closing date | 招股书抽取 (fields.json) | LLM 语义抽取 |
| CS | H shares after IPO (base; no options) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| CT | Gross profit in year-1 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| CU | Capital expenditure in year-1 | 招股书抽取 (fields.json) | LLM 语义抽取 |
| CV | Audit opinion (year-1) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| CW | Listing expenses (HK$) | 招股书抽取 (fields.json) | LLM 语义抽取 |
| CX | Cornerstone investor names | 招股书抽取 (fields.json) | LLM 语义抽取 |
| CY | Final cornerstone allocation (% of base offer) | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| CZ | Earliest cornerstone unlock date (dd/mm/yy) | tools/external/flags.py / src/cornerstone.py (Earliest cornerstone unlock date) | 确定性计算 (0 token) |
| DA | Subscription Ratio (times) | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DB | Public applicants | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DC | Public valid applied shares | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DD | Public subscription original wording | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DE | Pricing date | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DF | Allotment announcement date | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DG | Final global offering shares (before over-allotment) | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DH | Final public offer shares | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DI | Final placing shares | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DJ | Over-allotment shares actually issued | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DK | Greenshoe exercise rate (%) | src/academic_derivations.py (Greenshoe exercise rate) | 确定性计算 (0 token) |
| DL | Actual clawback / reallocation description | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DM | Net IPO proceeds to issuer (HK$) | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DN | Public shareholding at listing (%) | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DO | Share base used for both public shareholding ratios | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DP | Unrestricted public shareholding at listing (%) | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DQ | Free float denominator description | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DR | Free float denominator shares | 配发公告 (allot_fields.json) | LLM 语义抽取 |
| DS | HSI return over 20 trading days before prospectus (%) | tools/external/market.py (HSI 20-day return) | 外部抓取 |
| DT | HK ordinary IPO count in 90 calendar days before prospectus | tools/external/ipo_count.py (90-day HK ordinary IPO count) | 外部抓取 |
| DU | 1-month HIBOR before prospectus (%) | tools/external/hkma_import.py (1-month HIBOR) | 外部抓取 |
| DV | Banking system aggregate balance before prospectus (HK$) | tools/external/hkma_import.py (Aggregate Balance) | 外部抓取 |
| DW | First trading day closing price (HK$) | tools/external/market.py (First day close) | 外部抓取 |
| DX | First-day return / Underpricing (%) | src/academic_derivations.py (First-day return / Underpricing) | 确定性计算 (0 token) |
| DY | Money left on the table (HK$) | src/academic_derivations.py (Money left on the table) | 确定性计算 (0 token) |
| DZ | First trading day opening price (HK$) | tools/external/market.py (First day open) | 外部抓取 |
| EA | First trading day high (HK$) | tools/external/market.py (First day high) | 外部抓取 |
| EB | First trading day low (HK$) | tools/external/market.py (First day low) | 外部抓取 |
| EC | First trading day volume (shares) | tools/external/market.py (First day volume) | 外部抓取 |
| ED | First-day flipping ratio (%) | src/academic_derivations.py (First-day flipping ratio) | 确定性计算 (0 token) |
| EE | First trading day turnover (HK$) | tools/external/market.py (First day turnover) | 外部抓取 |
| EF | Offer mechanism | tools/external/rules.py (Offer mechanism) | 外部抓取 |
| EG | Applicable IPO rules / transition basis | tools/external/rules.py (Applicable IPO rules) | 外部抓取 |
| EH | Company Chinese Name | 招股书抽取 (fields.json) | LLM 语义抽取 |
| EI | Current listing status | tools/external/aftermarket.py (Current listing status) | 外部抓取 |
| EJ | 1-month post-IPO close price (HK$) | tools/external/aftermarket.py (1-month close price) | 外部抓取 |
| EK | 1-month BHR from Day-1 close (%) | tools/external/aftermarket.py (1-month BHR) | 外部抓取 |
| EL | 1-month total return from offer price (%) | tools/external/aftermarket.py (1-month total return) | 外部抓取 |
| EM | 1-month HSI return (%) | tools/external/aftermarket.py (1-month HSI return) | 外部抓取 |
| EN | 1-month HSTECH return (%) | tools/external/aftermarket.py (1-month HSTECH return) | 外部抓取 |
| EO | 1-month wealth relative vs HSI | tools/external/aftermarket.py (1-month WR vs HSI) | 外部抓取 |
| EP | 1-month wealth relative vs HSTECH | tools/external/aftermarket.py (1-month WR vs HSTECH) | 外部抓取 |
| EQ | 1-month average daily turnover (HK$) | tools/external/aftermarket.py (1-month average daily turnover) | 外部抓取 |
| ER | 6-month post-IPO close price (HK$) | tools/external/aftermarket.py (6-month close price) | 外部抓取 |
| ES | 6-month BHR from Day-1 close (%) | tools/external/aftermarket.py (6-month BHR) | 外部抓取 |
| ET | 6-month total return from offer price (%) | tools/external/aftermarket.py (6-month total return) | 外部抓取 |
| EU | 6-month HSI return (%) | tools/external/aftermarket.py (6-month HSI return) | 外部抓取 |
| EV | 6-month HSTECH return (%) | tools/external/aftermarket.py (6-month HSTECH return) | 外部抓取 |
| EW | 6-month wealth relative vs HSI | tools/external/aftermarket.py (6-month WR vs HSI) | 外部抓取 |
| EX | 6-month wealth relative vs HSTECH | tools/external/aftermarket.py (6-month WR vs HSTECH) | 外部抓取 |
| EY | 6-month average daily turnover (HK$) | tools/external/aftermarket.py (6-month average daily turnover) | 外部抓取 |
| EZ | Liquidity decay ratio (6M vs Day-1 turnover) | tools/external/aftermarket.py (Liquidity decay ratio) | 外部抓取 |
| FA | 1-year post-IPO return (%) [Reserved] | 预留字段 (1年/3年，数据未到期) | 暂不可计算 |
| FB | 1-year wealth relative vs HSI [Reserved] | 预留字段 (1年/3年，数据未到期) | 暂不可计算 |
| FC | 3-year post-IPO return (%) [Reserved] | 预留字段 (1年/3年，数据未到期) | 暂不可计算 |
| FD | 3-year wealth relative vs HSI [Reserved] | 预留字段 (1年/3年，数据未到期) | 暂不可计算 |
| FE | 18A/18C regulatory milestone status | tools/external/aftermarket.py (18A/18C regulatory status) | 外部抓取 |
| FF | Stabilizing manager | src/write_back_expansion.py (Stabilizing manager) | 确定性计算 (0 token) |
| FG | Stabilization period end date | src/write_back_expansion.py (Stabilization period end date) | 确定性计算 (0 token) |
| FH | Stabilization purchases occurred | src/write_back_expansion.py (Stabilization purchases occurred) | 确定性计算 (0 token) |
| FI | Over-allocation shares | src/write_back_expansion.py (Over-allocation shares) | 确定性计算 (0 token) |
| FJ | Over-allocation (% of base offer) | src/write_back_expansion.py (Over-allocation pct) | 确定性计算 (0 token) |
| FK | Over-allotment option exercise date | src/write_back_expansion.py (Over-allotment exercise date) | 确定性计算 (0 token) |
| FL | Shares issued under over-allotment option | src/write_back_expansion.py (Shares issued under option) | 确定性计算 (0 token) |
| FM | Over-allotment exercise percentage (%) | src/write_back_expansion.py (Over-allotment exercise percentage) | 确定性计算 (0 token) |
| FN | Post-stabilization cliff return [-5, +5] (%) | src/write_back_expansion.py (Cliff return m5 p5) | 确定性计算 (0 token) |
| FO | Post-stabilization 20-day return [0, +20] (%) | src/write_back_expansion.py (Post-stabilization return p20) | 确定性计算 (0 token) |
| FP | Post-stabilization volume decay ratio (%) | src/write_back_expansion.py (Post-stabilization volume decay) | 确定性计算 (0 token) |
| FQ | Day-5 BHR from Day-1 close (%) | src/write_back_expansion.py (Day-5 BHR) | 确定性计算 (0 token) |
| FR | Day-5 wealth relative vs HSI | src/write_back_expansion.py (Day-5 WR vs HSI) | 确定性计算 (0 token) |
| FS | Day-20 BHR from Day-1 close (%) | src/write_back_expansion.py (Day-20 BHR) | 确定性计算 (0 token) |
| FT | Day-20 wealth relative vs HSI | src/write_back_expansion.py (Day-20 WR vs HSI) | 确定性计算 (0 token) |
| FU | 3-month BHR from Day-1 close (%) | src/write_back_expansion.py (3-month BHR) | 确定性计算 (0 token) |
| FV | 3-month wealth relative vs HSI | src/write_back_expansion.py (3-month WR vs HSI) | 确定性计算 (0 token) |
| FW | 3-month wealth relative vs HSTECH | src/write_back_expansion.py (3-month WR vs HSTECH) | 确定性计算 (0 token) |
| FX | 3-month average daily turnover (HK$) | src/write_back_expansion.py (3-month avg daily turnover) | 确定性计算 (0 token) |
| FY | Amihud illiquidity (6M mean) | src/write_back_expansion.py (Amihud illiquidity 6M mean) | 确定性计算 (0 token) |
| FZ | Zero-volume days count (first 6M) | src/write_back_expansion.py (Zero-volume days count 6M) | 确定性计算 (0 token) |
| GA | Return volatility (first 6M daily std dev, %) | src/write_back_expansion.py (Return volatility 6M) | 确定性计算 (0 token) |
| GB | Maximum drawdown (first 6M, %) | src/write_back_expansion.py (Maximum drawdown 6M) | 确定性计算 (0 token) |
| GC | Controlling shareholder 6-month disposal lockup expiry date | src/write_back_expansion.py (Controlling shareholder 6M disposal expiry) | 确定性计算 (0 token) |
| GD | Controlling shareholder 12-month cessation of control expiry d | src/write_back_expansion.py (Controlling shareholder 12M control expiry) | 确定性计算 (0 token) |
| GE | Cornerstone unlock CAR [-5, +5] (%) | src/write_back_expansion.py (Cornerstone unlock CAR m5 p5) | 确定性计算 (0 token) |
| GF | Cornerstone unlock CAR [-20, +20] (%) | src/write_back_expansion.py (Cornerstone unlock CAR m20 p20) | 确定性计算 (0 token) |
| GG | Cornerstone unlock volume shock ratio | src/write_back_expansion.py (Cornerstone unlock volume shock ratio) | 确定性计算 (0 token) |
| GH | Lead sponsor name | src/write_back_expansion.py (Lead sponsor name) | 确定性计算 (0 token) |
| GI | Joint sponsor count | src/write_back_expansion.py (Joint sponsor count) | 确定性计算 (0 token) |
| GJ | Sponsor commercial bank affiliate flag | src/write_back_expansion.py (Sponsor bank affiliate flag) | 确定性计算 (0 token) |
| GK | Underwriting base commission rate (%) | src/write_back_expansion.py (Underwriting base commission rate) | 确定性计算 (0 token) |
| GL | Underwriting discretionary incentive fee rate (%) | src/write_back_expansion.py (Underwriting incentive fee rate) | 确定性计算 (0 token) |
| GM | Total underwriting fee rate (%) | src/write_back_expansion.py (Total underwriting fee rate) | 确定性计算 (0 token) |
| GN | Cornerstone investor count | src/write_back_expansion.py (Cornerstone investor count) | 确定性计算 (0 token) |
| GO | Cornerstone state-owned presence flag | src/write_back_expansion.py (Cornerstone state-owned flag) | 确定性计算 (0 token) |
| GP | Crossover fund presence flag | src/write_back_expansion.py (Crossover fund flag) | 确定性计算 (0 token) |
| GQ | Pre-IPO institutional investor count | src/write_back_expansion.py (Pre-IPO investor count) | 确定性计算 (0 token) |
| GR | Pre-IPO state-owned backing flag | src/write_back_expansion.py (Pre-IPO state-owned flag) | 确定性计算 (0 token) |
| GS | FINI digital settlement regime | src/write_back_expansion.py (FINI digital settlement regime) | 确定性计算 (0 token) |
| GT | 2025 pricing reform regime | src/write_back_expansion.py (2025 pricing reform regime) | 确定性计算 (0 token) |