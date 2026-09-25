# 香港主板 2026 Q1 IPO 学术研究数据变量代码本 (Data Codebook)

- **样本规模 (N)**：38 家香港联交所主板新上市公司
- **变量总数 (K)**：202 维完整跨学科指标
- **数据层级划分**：浅绿官方基础 (11 列) + 浅蓝招股书披露 (77 列) + 深蓝配发及外部衍生 (114 列)
- **生成时间**：2026-09-25 16:57:48 | **数据基准**：`HKIPO-MB2026Q1.xlsx` (Sheet: NLR)

---

## 一、变量层级与来源体系导览

| 数据层级 | 覆盖范围 | 列数 | 核心特征与学术用途 |
|---|---|---|---|
| **浅绿 (HKEX 官方来源)** | 列 A–K | 11 列 | 港交所新上市报告官方确证指标：上市编号、代码、保荐人、会计师、公开发售及国际发售募资额、最终定价。 |
| **浅蓝 (招股书全量来源)** | 招股书法定披露与Pre-IPO结构 | 77 列 | 发行人招股书披露：资本结构、发售价区间、Pre-IPO VC/PE 投资背景与治理席位、近三年财务与业务指标。 |
| **深蓝 (配发及外部数据)** | 配发公告与外部市场数据 | 114 列 | 发行结果与市场宏观：基石投资者最终获配及禁售期、回拨机制、超购倍数、自由流通量、首日二级市场表现、恒指收益率、HIBOR、总结余、监管分类。 |

---

## 二、202 维全量变量字典详细清单 (Codebook)

| 列 | 变量英文名 (Variable Header) | 中文口径释义 | 数据层级 | 数据类型 | 时点约定 | 样本状态 (填报率) | 描述性统计 / 分布特征 |
|---|---|---|---|---|---|---|---|
| **A** | `HKEx file# of the year` | 港交所年度申请编号 | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 19.79 / 中位数 19.50 / 区间 [1.00, 39.00] |
| **B** | `Stock Code` | 股份代号（四位港股代码，如 6082.HK） | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 38 种取值 ('6082.HK': 1, '2513.HK': 1, '9903.HK': 1) |
| **C** | `Company Name at time of listing` | 公司上市时法定英文名称 | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 38 种取值 ('Shanghai Biren Technology Co., Ltd.- H shares': 1, 'Knowledge Atlas Technology Joint Stock Company Limited - H shares': 1, 'Shanghai Iluvatar CoreX Semiconductor Co., Ltd. - H shares': 1) |
| **D** | `Date of Prospectus (dd/mm/yy)` | 招股书刊发日期 | 浅绿 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-12-22 ~ 2026-03-23 |
| **E** | `Date of Listing (dd/mm/yy)` | 正式挂牌上市交易日期 | 浅绿 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2026-01-02 ~ 2026-03-31 |
| **F** | `Sponsor(s)` | 独家/联席保荐人名单 | 浅绿 | `string` | Prospectus syndicate structure | 100% 完备 | 共 31 种取值 ('China International Capital Corporation Hong Kong Securities Limited': 4, 'Huatai Financial Holdings (Hong Kong) Limited': 4, 'CITIC Securities (Hong Kong) Limited': 2) |
| **G** | `Reporting Accountants` | 申报会计师事务所 | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 8 种取值 ('Ernst & Young': 17, 'KPMG': 9, 'Deloitte Touche Tohmatsu': 5) |
| **H** | `Valuer(s)` | 独立物业或资产估值师 | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 6 种取值 ('N/A': 30, 'Jones Lang LaSalle Corporate Appraisal and Advisory Limited': 4, 'AVISTA Valuation Advisory Limited': 1) |
| **I** | `Funds Raised HK (a)` | 香港公开发售募资额 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 300,178,580.53 / 中位数 162,953,902.50 / 区间 [22,374,000.00, 1,068,412,800.00] |
| **J** | `Funds Raised Int.(b)` | 国际配售募资额 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 2,602,887,898.47 / 中位数 1,504,365,064.00 / 区间 [201,322,000.00, 11,030,288,100.00] |
| **K** | `IPO Subscription Price (HK$)` | 最终发售定价 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 65.43 / 中位数 42.42 / 区间 [10.80, 248.00] |
| **L** | `Total (without option)` | Total (without option) | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 642,887,734.82 / 中位数 400,215,340.00 / 区间 [64,384,350.00, 5,736,722,666.00] |
| **M** | `Global Offering (without option)` | Global Offering (without option) | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 52,841,780.79 / 中位数 32,500,000.00 / 区间 [4,750,000.00, 273,951,400.00] |
| **N** | `Number of offer shares under the capitalization Issue` | 全球发售完成前的已发行股份总数。本数据集口径：一律填 L − M（Total 减去全球发售股数），即使招股书未披露「资本化发行」也必须照填，不得留 NaN。用于满足恒等式 L = N + Q。2026Q1 成品工作簿 38 家公司全部取 L − M，Q2 必须同口径。数值只取权威 SHARE CAPITAL 汇总表与封面，禁止取「历史沿革／资本化发行沿革」段落。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 590,045,954.03 / 中位数 366,200,240.00 / 区间 [57,000,000.00, 5,462,771,266.00] |
| **O** | `Number of offer shares under Capitalization Rest` | 与 col_N 同口径：一律填 L − M（全球发售完成前的已发行股份总数），即使招股书未披露「资本化转换」也必须照填，不得留 NaN。用于满足恒等式 L = O + M。2026Q1 成品 38 家全部为 L − M。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 590,045,954.03 / 中位数 366,200,240.00 / 区间 [57,000,000.00, 5,462,771,266.00] |
| **P** | `Sale Shares` | 老股出售（Sale Shares）数量。若为全部新股的 Offer for Subscription（无 Selling Shareholder），填数字 0，不得留 NaN，用于满足恒等式 M = Q + P。判据：封面／股本汇总表无 Sale Shares 行，且全文无 Selling Shareholder 披露。2026Q1 成品 38 家全部为 0。若确有老股出售，按招股书披露填写。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **Q** | `New shares` | New shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 52,841,780.79 / 中位数 32,500,000.00 / 区间 [4,750,000.00, 273,951,400.00] |
| **R** | `Placing Shares` | Placing Shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 48,104,611.58 / 中位数 29,250,000.00 / 区间 [4,275,000.00, 246,556,200.00] |
| **S** | `Public Offer shares` | Public Offer shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 4,737,169.21 / 中位数 2,945,800.00 / 区间 [475,000.00, 27,395,200.00] |
| **T** | `Maximum Offer Price` | Maximum Offer Price | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 67.00 / 中位数 44.52 / 区间 [10.80, 248.00] |
| **U** | `Minimum Offer Price` | Minimum Offer Price | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (26/38 (68.42%)) | 均值 59.21 / 中位数 40.00 / 区间 [11.00, 229.60] |
| **V** | `Filing price revision (%)` | 发售定价偏离询价区间中点幅度（Hanley 1993 动态信息提取，固定价格发售为 0.00%） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 -0.01 / 中位数 0.00 / 区间 [-0.12, 0.10] |
| **W** | `Filing range width (%)` | 询价区间相对宽度（Beatty & Ritter 1986 事前估值不确定性，固定价格发售为 0.00%） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.06 / 中位数 0.00 / 区间 [0.00, 0.24] |
| **X** | `Pricing position in filing range` | 定价落点分类体系（Fixed price / Above range / At high / Midpoint / Within range / At low / Below range） | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 4 种取值 ('Fixed price': 22, 'At high': 6, 'Within range': 6) |
| **Y** | `currency in financial information` | currency in financial information | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 2 种取值 ('RMB': 37, 'USD': 1) |
| **Z** | `total assets in year-3 (3 years before IPO)` | total assets in year-3 (3 years before IPO) | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 11,032,532,105.26 / 中位数 2,626,291,000.00 / 区间 [221,090,000.00, 195,404,600,000.00] |
| **AA** | `total assets in year-2` | total assets in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 11,822,724,552.63 / 中位数 3,024,553,000.00 / 区间 [212,474,000.00, 187,648,700,000.00] |
| **AB** | `total assets in year-1` | total assets in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 12,236,328,763.16 / 中位数 3,563,213,500.00 / 区间 [244,069,000.00, 180,755,900,000.00] |
| **AC** | `total equity in year-3` | total equity in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 4,474,098,078.95 / 中位数 1,063,515,500.00 / 区间 [-5,969,861,000.00, 74,036,700,000.00] |
| **AD** | `total equity in year-2` | total equity in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 4,741,253,552.63 / 中位数 938,585,500.00 / 区间 [-7,424,205,000.00, 77,536,200,000.00] |
| **AE** | `total equity in year-1` | total equity in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 4,943,336,605.26 / 中位数 1,080,543,500.00 / 区间 [-8,997,718,000.00, 80,439,800,000.00] |
| **AF** | `total liability in year-3` | total liability in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 6,558,407,710.53 / 中位数 1,273,394,500.00 / 区间 [87,320,000.00, 121,367,900,000.00] |
| **AG** | `total liability in year-2` | total liability in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 7,081,471,000.00 / 中位数 1,847,077,000.00 / 区间 [38,292,000.00, 110,112,500,000.00] |
| **AH** | `total liability in year-1` | total liability in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 7,292,992,157.89 / 中位数 2,335,801,500.00 / 区间 [48,007,000.00, 100,316,100,000.00] |
| **AI** | `Net sales in year-3` | Net sales in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 6,606,596,500.00 / 中位数 742,227,000.00 / 区间 [44,000.00, 110,860,700,000.00] |
| **AJ** | `Net sales in year-2` | Net sales in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 9,055,951,105.26 / 中位数 966,447,000.00 / 区间 [30,523,000.00, 137,946,900,000.00] |
| **AK** | `Net sales in year-1` | Net sales in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 10,405,474,354.39 / 中位数 921,752,250.00 / 区间 [71,249,333.33, 149,053,333,333.33] |
| **AL** | `Profit before tax in year-3` | Profit before tax in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 -21,667,184.21 / 中位数 54,984,000.00 / 区间 [-4,170,100,000.00, 2,579,270,000.00] |
| **AM** | `Profit before tax in year-2` | Profit before tax in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 697,060,657.89 / 中位数 83,905,000.00 / 区间 [-2,958,007,000.00, 18,896,400,000.00] |
| **AN** | `Profit before tax in year-1` | Profit before tax in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 876,225,394.74 / 中位数 93,193,666.67 / 区间 [-4,715,704,000.00, 20,128,533,333.33] |
| **AO** | `Profit for the year in year-3` | Profit for the year in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 -57,277,842.11 / 中位数 46,566,000.00 / 区间 [-4,167,900,000.00, 2,039,772,000.00] |
| **AP** | `Profit for the year in year-2` | Profit for the year in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 653,713,605.26 / 中位数 79,604,500.00 / 区间 [-2,958,007,000.00, 18,925,000,000.00] |
| **AQ** | `Profit for the year in year-1` | Profit for the year in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 778,204,066.67 / 中位数 67,385,000.00 / 区间 [-4,715,704,000.00, 20,149,466,666.67] |
| **AR** | `Underwriting Commission (% of fund raised HK (a)` | Underwriting Commission (% of fund raised HK (a) | 浅蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.02 / 中位数 0.02 / 区间 [0.00, 0.04] |
| **AS** | `Underwriting Commission (% of fund raised Int.(b)` | Underwriting Commission (% of fund raised Int.(b) | 浅蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.02 / 中位数 0.02 / 区间 [0.00, 0.04] |
| **AT** | `Over-allotment Option (%)` | Over-allotment Option (%) | 浅蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 0.10 / 中位数 0.15 / 区间 [0.00, 0.15] |
| **AU** | `Principal business / industry` | Principal business / industry | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 38 种取值 ('GPGPU chips and GPGPU-based intelligent computing solutions for AI': 1, 'Leading AI company in China dedicated to developing general-purpose large models / MaaS platform': 1, 'GPGPU products and AI computing solutions (chips, accelerators, servers and clusters)': 1) |
| **AV** | `Listing route / applicable chapter` | Listing route / applicable chapter | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 14 种取值 ('Main Board; Chapter 19A PRC issuer with other listed shares (A+H)': 11, 'Main Board (Chapter 19A PRC issuer)': 8, 'Chapter 18C Specialist Technology Company (Commercial Company)': 4) |
| **AW** | `Year-1 financial period end (dd/mm/yy)` | Year-1 financial period end (dd/mm/yy) | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2025-06-30 ~ 2025-10-31 |
| **AX** | `Operating cash flow in year-1 (before annualization)` | Operating cash flow in year-1 (before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 1,098,096,368.42 / 中位数 72,245,500.00 / 区间 [-1,327,150,000.00, 28,579,500,000.00] |
| **AY** | `Cash and cash equivalents at year-1 end` | Cash and cash equivalents at year-1 end | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 2,078,274,263.16 / 中位数 360,591,000.00 / 区间 [19,684,000.00, 17,268,700,000.00] |
| **AZ** | `R&D expensed in year-1 (before annualization)` | R&D expensed in year-1 (before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (35/38 (92.11%)) | 均值 373,710,400.00 / 中位数 129,142,000.00 / 区间 [513,000.00, 1,951,106,000.00] |
| **BA** | `Development costs capitalized in year-1 (additions, before annualization)` | Development costs capitalized in year-1 (additions, before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 14,527,684.21 / 中位数 0.00 / 区间 [0.00, 359,743,000.00] |
| **BB** | `Top 5 customers (% of year-1 revenue)` | Top 5 customers (% of year-1 revenue) | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 0.43 / 中位数 0.42 / 区间 [0.01, 0.99] |
| **BC** | `Comments / Annualization factor` | 最近一期财务数据对应的年化因子与口径说明 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 0.69 / 中位数 0.75 / 区间 [0.50, 0.83] |
| **BD** | `Pre-IPO VC/PE backing (1=yes; 0=no)` | 是否引入 Pre-IPO VC/PE 投资者：1=有，0=无。看 HISTORY AND DEVELOPMENT — Pre-IPO Investments 与 SUBSTANTIAL SHAREHOLDERS 名单；只要有专业投资机构（VC/PE/产业基金）在上市前入股即 1。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.74 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BE** | `Pre-IPO VC backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。早期/成长期专业风险投资基金为 1；未找到证据不等于 0，无法确认时填 NaN。分类依据须在本字段 quote 中体现。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.61 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BF** | `Pre-IPO PE backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。中晚期私募股权基金或并购基金为 1；未找到证据不等于 0，无法确认时填 NaN。分类依据须在本字段 quote 中体现。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.29 / 中位数 0.00 / 区间 [0.00, 1.00] |
| **BG** | `Pre-IPO CVC backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。发行人产业股东须有战略投资/企业风投关系依据才归 CVC；普通产业股东不能自动算 CVC。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.42 / 中位数 0.00 / 区间 [0.00, 1.00] |
| **BH** | `Pre-IPO State/Gov backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。有明确国资、政府或产业引导基金背景的机构为 1；国资身份不自动代表 VC/PE。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.32 / 中位数 0.00 / 区间 [0.00, 1.00] |
| **BI** | `Top-tier VC/PE backing (1=yes; 0=no)` | 仅在本公司招股书确认一线知名 VC/PE 机构持有重要股权或领投时填 1；不得仅凭机构知名度推断其参与本公司投资。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.58 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BJ** | `Key Pre-IPO investors` | 仅列本公司招股书披露的上市前投资者，采用一致的英文全称/拼音并以分号分隔；同一投资者只记一次，不从其他 cohort 补名单。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (28/38 (73.68%)) | 共 28 种取值 ('Qiming Venture Partners; Country Garden VC; Sky9 Capital; Songhe Capital; Zhuhai Gree; Walden International; Shanghai SOE Reform Fund': 1, 'Qiming Venture Partners; HongShan; Legend Capital; Meituan; Alibaba; Tencent; Xiaomi; Prosperity7; Beijing AI Fund': 1, 'Princeville Global; HongShan; Shanghai Lianhe Investment; Cathay Capital; Greater Bay Area Fund': 1) |
| **BK** | `Pre-IPO institutional shareholding (%)` | 上市前 VC/PE/CVC/国资机构合计持股比例，取紧邻上市前的股权口径，不能混入 IPO 新股或基石配售；统一填 0–1 小数（如 12.5%=0.125）。只有招股书披露或可用披露数字复算时填写，否则 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.25 / 中位数 0.21 / 区间 [0.00, 0.69] |
| **BL** | `Pre-IPO investor board seat (1=yes; 0=no)` | 只有能从招股书明确关联到 Pre-IPO 投资机构的非执行董事或正式观察员席位才填 1；没有证据不等于 0，无法确认时填 NaN。 | 浅蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 19 家 (50.0%), 0 (否): 19 家 |
| **BM** | `Earliest Pre-IPO investment round` | 从本公司招股书披露的 Pre-IPO 投资轮次中取最早一轮，保留披露的标准轮次名称；只有明确说明没有外部上市前投资时填 None，否则无法确认时 NA。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 8 种取值 ('Series A': 12, 'None': 10, 'Series Angel': 5) |
| **BN** | `Pre-IPO holding duration (years)` | 从最早 Pre-IPO 投资协议日期至本公司招股书日期计算年数，保留两位小数；起始日期无法确认则 NaN。每家公司必须使用自己的招股书日期，不沿用其他季度日期。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 5.38 / 中位数 6.14 / 区间 [0.00, 12.50] |
| **BO** | `Ultimate controller type` | 最终控制人类型（如：自然人 / 家族 / 国资委 / 地方政府 / 外资 / 无实际控制人）。取 SUBSTANTIAL SHAREHOLDERS 与 Controlling Shareholders 段的实际控制人身份表述。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 12 种取值 ('自然人': 25, '无实际控制人': 3, '自然人（Dr. Liu 为最终控制人，与一致行动人共同构成控股股东集团）': 1) |
| **BP** | `Controller economic interest at listing (%)` | 控制人上市时**经济权益**（持股比例），填小数。取 CONTROLLING/SUBSTANTIAL SHAREHOLDERS 表的持股百分比。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.36 / 中位数 0.31 / 区间 [0.02, 0.75] |
| **BQ** | `Controller voting rights at listing (%)` | 控制人上市时**投票权**比例，填小数。有 WVR（同股不同权）时与持股不同，取投票权那一列；无 WVR 通常与 BC 相同。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.38 / 中位数 0.34 / 区间 [0.02, 0.75] |
| **BR** | `Interest-bearing debt at year-1 end` | year-1 期末**总有息负债**（用与 col_V 相同的披露货币基本单位）。包含短期借款、长期借款、租赁负债及带息应付票据债券等带息债务总额，取 INDEBTEDNESS 表格的 Total 余额；不含应付账款等无息负债。必须换算为货币基本单位（乘表格千元/百万元乘数）。期末余额，不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 3,159,907,289.47 / 中位数 337,828,500.00 / 区间 [5,851,000.00, 71,212,600,000.00] |
| **BS** | `Technology commercialization stage` | 技术商业化阶段（如：研发阶段 / 小批量试产 / 商业化初期 / 规模商业化 / 已量产）。按 BUSINESS 与业务摘要里的产品状态表述填，不要按行业推测。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 30 种取值 ('规模商业化（已量产）': 5, '已量产（规模商业化，mass production）': 3, '已量产（Mass production）': 2) |
| **BT** | `Debt repayment (% of planned net IPO proceeds)` | 计划净募资中用于**偿债**的比例，填小数。取 USE OF PROCEEDS 里用于偿还借款/债务的金额 ÷ 计划净募资额；没有该用途填 0。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.01 / 中位数 0.00 / 区间 [0.00, 0.15] |
| **BU** | `Listing board` | 上市板块（Main Board 主板） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Main Board': 38) |
| **BV** | `Share class` | 股份类别（如 H Shares / A Shares / Class A Ordinary Shares / Class B Ordinary Shares）。按招股书股本表的类别名称填。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 3 种取值 ('H Shares': 35, 'Ordinary Shares': 2, 'Class A Ordinary Shares': 1) |
| **BW** | `A+H issuer flag` | A+H 两地上市发行人标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 12 家 (31.6%), 0 (否): 26 家 |
| **BX** | `WVR flag` | 不同投票权/同股不同权架构标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 1 家 (2.6%), 0 (否): 37 家 |
| **BY** | `Chapter 18A flag` | 第 18A 章未盈利生物科技公司标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 3 家 (7.9%), 0 (否): 35 家 |
| **BZ** | `Chapter 18C flag` | 第 18C 章特专科技公司标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 6 家 (15.8%), 0 (否): 32 家 |
| **CA** | `Industry classification code` | 恒生行业分类 HSICS 6 位业务细分代码 | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 453,492.89 / 中位数 651,020.00 / 区间 [52,020.00, 703,020.00] |
| **CB** | `Industry classification system and version` | 行业分类系统与版本号 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('HSICS (Hang Seng Industry Classification System) 2026': 38) |
| **CC** | `Incorporation date` | 公司**法定注册成立日期**（dd/mm/yy）。必须优先取自 Statutory and General Information (Appendix V '1. Incorporation')、History & Development 或 Accountants' Report (附注 1)。严禁从 Definitions (释义) 章节取值（释义章节常有起草笔误或仅为前期筹备日）。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 1994-06-30 ~ 2024-07-17 |
| **CD** | `Firm age at IPO (years)` | 公司成立至上市年限（Lowry et al. 2017 Table 3.4 基础控制变量） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 15.76 / 中位数 15.48 / 区间 [1.57, 31.60] |
| **CE** | `Place of incorporation` | 公司注册成立法域（如 Cayman Islands, PRC 等） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 2 种取值 ('PRC': 35, 'Cayman Islands': 3) |
| **CF** | `Principal place of business` | 主要营业地点（城市/国家），如 PRC、Hong Kong、Shenzhen, PRC。取公司资料或注册办事处段。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 25 种取值 ('Shenzhen, PRC': 7, 'Shanghai, PRC': 6, 'Beijing, PRC': 3) |
| **CG** | `Financial statement unit multiplier` | 财务报表基础货币乘数（千元/万元/百万元） | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 27,289.47 / 中位数 1,000.00 / 区间 [1,000.00, 1,000,000.00] |
| **CH** | `Accounting standard` | 财务报表采用的会计准则（如 IFRS Accounting Standards / HKFRS / ASBE / US GAAP）。取会计师报告开头声明。 | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 3 种取值 ('IFRS Accounting Standards': 35, 'HKFRS Accounting Standards': 2, 'China Accounting Standards for Business Enterprises (CASBE)': 1) |
| **CI** | `Year-3 financial period start` | 往绩记录第三年前期起始日 | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2023-01-01 ~ 2023-01-01 |
| **CJ** | `Year-3 financial period end` | 往绩记录第三年前期截止日 | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2023-12-31 ~ 2023-12-31 |
| **CK** | `Year-2 financial period start` | 往绩记录第二年前期起始日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2024-01-01 ~ 2024-01-01 |
| **CL** | `Year-2 financial period end` | 往绩记录第二年前期截止日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2024-12-31 ~ 2024-12-31 |
| **CM** | `Year-1 financial period start` | 往绩记录最近一期起始日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2025-01-01 ~ 2025-01-01 |
| **CN** | `Year-1 net sales (original, pre-annualization)` | 最近一期营业收入原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 7,593,341,500.00 / 中位数 623,652,000.00 / 区间 [53,437,000.00, 111,790,000,000.00] |
| **CO** | `Year-1 profit before tax (original)` | 最近一期税前利润原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 683,109,052.63 / 中位数 56,568,500.00 / 区间 [-2,357,852,000.00, 15,096,400,000.00] |
| **CP** | `Year-1 profit for period (original)` | 最近一期净利润原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 612,175,315.79 / 中位数 40,618,000.00 / 区间 [-2,357,852,000.00, 15,112,100,000.00] |
| **CQ** | `Subscription opening date` | 香港公开发售**开始认购日期**（dd/mm/yy）。取 EXPECTED TIMETABLE。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-12-22 ~ 2026-03-23 |
| **CR** | `Subscription closing date` | 香港公开发售**截止认购日期**（dd/mm/yy）。取 EXPECTED TIMETABLE。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-12-29 ~ 2026-03-26 |
| **CS** | `H shares after IPO (base; no options)` | 上市后**在港交所挂牌的股份数**（base，不含超额配售）。统一口径：① 内地 H 股发行人全部转换时 = 总股本；② 部分转换时 = 由未上市股转换的 H 股 + 新发 H 股（剩余未上市股不挂牌，不计入）；③ A+H 发行人 = 仅新发 H 股（A 股在沪深市场挂牌，不计入）；④ 开曼/境外发行人没有 H 股类别，其全部股份均在港交所挂牌，故 = 上市后已发行股份总数。即：本列恒等于「港交所挂牌的股份数」，四类结构可比。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 191,738,254.11 / 中位数 102,908,514.50 / 区间 [24,566,464.00, 1,120,964,824.00] |
| **CT** | `Gross profit in year-1` | year-1 **毛利**（用与 col_V 相同的披露货币基本单位）。取损益表的 Gross profit。强制期间锚定：必须与 col_AT 严格同期间！若 col_AT 为中期报告期（如截至 2025 年 6 月 30 日或 9 月 30 日止期间），必须严格提取该中期报告期对应列的原值，绝对严禁错采前一完整财年（FY2024）的数值。必须换算为货币基本单位（乘表格千元/百万元乘数）。不年化——手册明确仅 year-1 销售/税前利润/净利润年化，毛利不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 1,540,744,947.37 / 中位数 164,852,000.00 / 区间 [12,476,000.00, 20,934,500,000.00] |
| **CU** | `Capital expenditure in year-1` | year-1 **资本开支**（用与 col_V 相同的披露货币基本单位）。取现金流量表“购建物业、厂房及设备”或 CAPITAL EXPENDITURE 段。强制期间锚定：必须与 col_AT 严格同期间！若 col_AT 为中期报告期（如截至 2025 年 6 月 30 日或 9 月 30 日止期间），必须严格提取该中期报告期实际资本开支原值，绝对严禁错采前一完整财年（FY2024）数值。必须换算为货币基本单位（乘表格千元/百万元乘数）。不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 396,206,789.47 / 中位数 70,963,000.00 / 区间 [479,000.00, 7,286,600,000.00] |
| **CV** | `Audit opinion (year-1)` | year-1 **审计意见类型**（如 无保留意见 / Unqualified opinion / Qualified opinion）。取会计师报告的审计意见段。 | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 9 种取值 ('无保留意见 (Unqualified opinion)': 12, '无保留意见（Unqualified opinion）': 9, '无保留意见': 6) |
| **CW** | `Listing expenses (HK$)` | **总上市费用**（HK$ 基本单位，含承销佣金与其他开支）。取 UNDERWRITING COMMISSIONS AND LISTING EXPENSES 段的合计。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 106,426,842.11 / 中位数 82,200,000.00 / 区间 [32,900,000.00, 224,400,000.00] |
| **CX** | `Cornerstone investor names` | Cornerstone investor names | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (34/38 (89.47%)) | 共 34 种取值 ('3W Fund; Qiming Venture Partners (QM125, QM120); AMF; WT Asset Management; Hao Great China Focus Fund; Ping An Life Insurance; Huadeng Technology; Lion Global; CICC FT (Shanghai Greenwoods OTC Swaps); MY Asian; Eastspring; UBS AM Singapore; Taikang Life; Aspirational China Growth; Charoen Pokphand; Digital China; GTJA HK (Jinxiu 608/Zhonghe OTC Swaps); China Southern; Fullgoal (Fullgoal Fund, Fullgoal HK); Yeebo; EIP; Tessy Holding Limited; New Opportunities SPC': 1, 'JSC International Investment Fund SPC (acting for and on behalf of Qizhi SP); JinYi Capital Multi-Strategy Fund SPC Ltd. (acting for and on behalf of Structured Credit SP Fund); Perseverance Asset Management; Shanghai Gaoyi and CICC Financial Trading Limited (in connection with Gaoyi OTC Swaps); WT Asset Management; Taikang Life; GF Fund; 3W Fund; RIME; Optimas Capital Limited; Luster LightTech International Limited': 1, 'ZTE HK; XN Mountain; Wind Sabre; UBS AM Singapore; Teamsun HK; Qin Wan; OCM; Ocean Fine Industrial; Huatai OTC Swaps — Hengxin Fund Management; Fourth Paradigm; Engine International; Duckling Fund; DeepRoot Alpha; China Universal (HK); China Orient EIF; China Orient MSMF; China AMC (HK); CFIG; Alphahill Capital': 1) |
| **CY** | `Final cornerstone allocation (% of base offer)` | Final cornerstone allocation (% of base offer) | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 0.34 / 中位数 0.42 / 区间 [0.00, 0.69] |
| **CZ** | `Earliest cornerstone unlock date (dd/mm/yy)` | 基石投资者最早解禁日期 | 深蓝 | `date` | Post-IPO lockup expiration events | Adequate (34/38 (89.47%)) | 区间: 2026-07-02 ~ 2026-09-30 |
| **DA** | `Subscription Ratio (times)` | Subscription Ratio (times) | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 1,438.49 / 中位数 1,072.05 / 区间 [5.88, 5,297.23] |
| **DB** | `Public applicants` | Public applicants | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 141,740.97 / 中位数 143,279.50 / 区间 [14,551.00, 471,116.00] |
| **DC** | `Public valid applied shares` | Public valid applied shares | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 4,374,133,620.26 / 中位数 2,210,741,000.00 / 区间 [42,511,100.00, 29,073,659,800.00] |
| **DD** | `Public subscription original wording` | Public subscription original wording | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 38 种取值 ('Subscription level 2,347.53 times': 1, 'Subscription level 1,159.46 times': 1, 'Subscription level 414.24 times': 1) |
| **DE** | `Pricing date` | Pricing date | 深蓝 | `date` | Ex-ante prospectus disclosure | Adequate (28/38 (73.68%)) | 区间: 2025-12-30 ~ 2026-03-27 |
| **DF** | `Allotment announcement date` | Allotment announcement date | 深蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-12-31 ~ 2026-03-30 |
| **DG** | `Final global offering shares (before over-allotment)` | Final global offering shares (before over-allotment) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 54,891,919.74 / 中位数 34,188,000.00 / 区间 [4,750,000.00, 284,846,600.00] |
| **DH** | `Final public offer shares` | Final public offer shares | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 6,388,089.74 / 中位数 3,588,300.00 / 区间 [475,000.00, 49,538,600.00] |
| **DI** | `Final placing shares` | Final placing shares | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 48,503,830.00 / 中位数 29,398,600.00 / 区间 [4,275,000.00, 246,556,200.00] |
| **DJ** | `Over-allotment shares actually issued` | Over-allotment shares actually issued | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 4,138,011.58 / 中位数 0.00 / 区间 [0.00, 42,726,800.00] |
| **DK** | `Greenshoe exercise rate (%)` | 绿鞋实际行使比例（Ellis et al. 2000 超额配售执行度与价格支持） | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.38 / 中位数 0.00 / 区间 [0.00, 1.00] |
| **DL** | `Actual clawback / reallocation description` | Actual clawback / reallocation description | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 35 种取值 ('Claw-back triggered: No': 3, 'Reallocation: No. No. of Offer Shares reallocated from the International Offering: 0': 2, 'No. of Offer Shares reallocated from the International Offer (claw-back) 37,153,800; final no. of Offer Shares under the Public Offer (after reallocation) 49,538,600.': 1) |
| **DM** | `Net IPO proceeds to issuer (HK$)` | Net IPO proceeds to issuer (HK$) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 2,552,667,631.58 / 中位数 1,539,465,000.00 / 区间 [175,520,000.00, 10,470,400,000.00] |
| **DN** | `Public shareholding at listing (%)` | Public shareholding at listing (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.32 / 中位数 0.27 / 区间 [0.04, 0.80] |
| **DO** | `Share base used for both public shareholding ratios` | Share base used for both public shareholding ratios | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 642,803,596.55 / 中位数 400,215,340.00 / 区间 [64,384,350.00, 5,736,722,666.00] |
| **DP** | `Unrestricted public shareholding at listing (%)` | Unrestricted public shareholding at listing (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.08 / 中位数 0.07 / 区间 [0.02, 0.23] |
| **DQ** | `Free float denominator description` | Free float denominator description | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 37 种取值 ('Free float denominator = total issued shares upon listing (col_CZ); numerator = offer shares minus cornerstone allocation': 2, 'Free float denominator = total issued share capital of the Company upon Listing (2,396,131,700 Shares, taking into account the full exercise of the Offer Size Adjustment Option and before any exercise of the Over-allotment Option); H Shares held by the Cornerstone Investors (six-month lock-up) are excluded from free float.': 1, 'Free float denominator = total issued shares upon Listing (440,230,190 shares); Shares held by the Cornerstone Investors are excluded from the free float because they are subject to a six-month lock-up following the Listing Date.': 1) |
| **DR** | `Free float denominator shares` | Free float denominator shares | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 636,898,214.71 / 中位数 400,215,340.00 / 区间 [18,190,000.00, 5,736,722,666.00] |
| **DS** | `HSI return over 20 trading days before prospectus (%)` | 招股日前 20 个交易日恒生指数累计收益率 (%) | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 0.00 / 中位数 -0.00 / 区间 [-0.06, 0.09] |
| **DT** | `HK ordinary IPO count in 90 calendar days before prospectus` | 招股日前 90 个自然日香港普通主板 IPO 上市数量 | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 45.16 / 中位数 47.00 / 区间 [37.00, 54.00] |
| **DU** | `1-month HIBOR before prospectus (%)` | 招股日前一交易日香港银行同业拆借 1 个月 HIBOR 利率 (%) | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.03 / 中位数 0.03 / 区间 [0.02, 0.03] |
| **DV** | `Banking system aggregate balance before prospectus (HK$)` | 招股日前一交易日香港银行体系总结余 (HK$) | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 53,870,973,684.21 / 中位数 53,854,000,000.00 / 区间 [53,770,000,000.00, 54,049,000,000.00] |
| **DW** | `First trading day closing price (HK$)` | 首日上市二级市场收盘价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 87.45 / 中位数 51.62 / 区间 [6.20, 400.00] |
| **DX** | `First-day return / Underpricing (%)` | 上市首日抑价率 / 初始收益率（Rock 1986 / Ritter 1984 核心被解释变量） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 0.32 / 中位数 0.13 / 区间 [-0.49, 2.42] |
| **DY** | `Money left on the table (HK$)` | 留在桌面上的财富 / 抑价转移财富总额（Loughran & Ritter 2002 前景理论指标） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 675,383,250.99 / 中位数 296,492,902.40 / 区间 [-2,452,167,303.00, 5,255,568,000.00] |
| **DZ** | `First trading day opening price (HK$)` | 首日上市二级市场开盘价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 86.76 / 中位数 57.22 / 区间 [7.50, 445.00] |
| **EA** | `First trading day high (HK$)` | 首日上市二级市场盘中最高价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 96.72 / 中位数 58.22 / 区间 [7.90, 445.00] |
| **EB** | `First trading day low (HK$)` | 首日上市二级市场盘中最低价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 78.77 / 中位数 46.36 / 区间 [6.00, 399.20] |
| **EC** | `First trading day volume (shares)` | 首日上市二级市场全天成交量（股） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 19,368,847.08 / 中位数 12,966,926.50 / 区间 [2,240,320.00, 150,709,945.00] |
| **ED** | `First-day flipping ratio (%)` | 首日短线翻转抛售率 / 成交量占全球发售比例（Aggarwal 2003 机构抛售假说） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 0.39 / 中位数 0.35 / 区间 [0.12, 0.92] |
| **EE** | `First trading day turnover (HK$)` | 首日上市二级市场全天成交金额 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 1,166,665,934.21 / 中位数 728,528,050.00 / 区间 [111,474,300.00, 5,521,275,600.00] |
| **EF** | `Offer mechanism` | 发售与回拨机制（Mechanism A 传统 / Mechanism B 灵活） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 2 种取值 ('Mechanism B': 32, 'Mechanism A': 6) |
| **EG** | `Applicable IPO rules / transition basis` | 适用之上市规则过渡基准（FINI 改革规则） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 2 种取值 ('FINI (from 22/11/2023); 2025-08-04 pricing reform (Mechanism A/B; six-month cornerstone lock-up retained); this IPO: Mechanism B': 32, 'FINI (from 22/11/2023); 2025-08-04 pricing reform (Mechanism A/B; six-month cornerstone lock-up retained); this IPO: Mechanism A': 6) |
| **EH** | `Company Chinese Name` | Company Chinese Name | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (37/38 (97.37%)) | 共 37 种取值 ('上海壁仞科技股份有限公司': 1, '北京智谱华章科技股份有限公司': 1, '上海天数智芯半导体股份有限公司': 1) |
| **EI** | `Current listing status` | 当前挂牌存续状态 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 2 种取值 ('Active': 37, 'Suspended': 1) |
| **EJ** | `1-month post-IPO close price (HK$)` | 第20个交易日收盘价（窗口成熟后填报） | 深蓝 | `numeric` | Post-IPO T+20 trading days | Adequate (37/38 (97.37%)) | 均值 101.17 / 中位数 59.55 / 区间 [8.05, 486.00] |
| **EK** | `1-month BHR from Day-1 close (%)` | 由首日收盘至第20个交易日的买入持有收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | Adequate (37/38 (97.37%)) | 均值 0.11 / 中位数 0.02 / 区间 [-0.63, 2.11] |
| **EL** | `1-month total return from offer price (%)` | 由发售价至第20个交易日的累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | Adequate (37/38 (97.37%)) | 均值 0.48 / 中位数 0.22 / 区间 [-0.63, 2.15] |
| **EM** | `1-month HSI return (%)` | 同期恒生指数累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | Adequate (37/38 (97.37%)) | 均值 0.01 / 中位数 0.02 / 区间 [-0.07, 0.07] |
| **EN** | `1-month HSTECH return (%)` | 同期恒生科技指数累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | Adequate (37/38 (97.37%)) | 均值 -0.03 / 中位数 -0.05 / 区间 [-0.13, 0.05] |
| **EO** | `1-month wealth relative vs HSI` | 一个月相对恒指财富比 | 深蓝 | `numeric` | Post-IPO T+20 trading days | Adequate (37/38 (97.37%)) | 均值 1.10 / 中位数 1.02 / 区间 [0.36, 3.01] |
| **EP** | `1-month wealth relative vs HSTECH` | 一个月相对恒生科技指数财富比 | 深蓝 | `numeric` | Post-IPO T+20 trading days | Adequate (37/38 (97.37%)) | 均值 1.14 / 中位数 1.05 / 区间 [0.39, 3.09] |
| **EQ** | `1-month average daily turnover (HK$)` | 上市后首20个交易日日均成交额 | 深蓝 | `numeric` | Post-IPO T+20 trading days | Adequate (37/38 (97.37%)) | 均值 217,400,066.86 / 中位数 114,006,531.00 / 区间 [13,271,480.00, 1,047,544,366.00] |
| **ER** | `6-month post-IPO close price (HK$)` | 六个月目标日后首个交易日收盘价（窗口成熟后填报） | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Adequate (27/38 (71.05%)) | 均值 164.99 / 中位数 39.98 / 区间 [4.30, 1,825.00] |
| **ES** | `6-month BHR from Day-1 close (%)` | 由首日收盘至六个月目标交易日的买入持有收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Adequate (27/38 (71.05%)) | 均值 0.36 / 中位数 -0.29 / 区间 [-0.68, 12.88] |
| **ET** | `6-month total return from offer price (%)` | 由发售价至六个月目标交易日的累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Adequate (27/38 (71.05%)) | 均值 0.70 / 中位数 -0.14 / 区间 [-0.65, 14.71] |
| **EU** | `6-month HSI return (%)` | 同期恒生指数累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Adequate (27/38 (71.05%)) | 均值 -0.06 / 中位数 -0.05 / 区间 [-0.12, -0.01] |
| **EV** | `6-month HSTECH return (%)` | 同期恒生科技指数累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Adequate (27/38 (71.05%)) | 均值 -0.14 / 中位数 -0.12 / 区间 [-0.22, -0.09] |
| **EW** | `6-month wealth relative vs HSI` | 六个月相对恒指财富比 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Adequate (27/38 (71.05%)) | 均值 1.45 / 中位数 0.76 / 区间 [0.33, 15.00] |
| **EX** | `6-month wealth relative vs HSTECH` | 六个月相对恒生科技指数财富比 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Adequate (27/38 (71.05%)) | 均值 1.60 / 中位数 0.85 / 区间 [0.35, 16.66] |
| **EY** | `6-month average daily turnover (HK$)` | 六个月目标日前20个交易日日均成交额 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Adequate (27/38 (71.05%)) | 均值 579,847,504.09 / 中位数 72,406,991.00 / 区间 [108,175.00, 5,832,790,800.00] |
| **EZ** | `Liquidity decay ratio (6M vs Day-1 turnover)` | 六个月窗口日均成交额相对首日成交额比率 | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (27/38 (71.05%)) | 均值 0.27 / 中位数 0.06 / 区间 [0.00, 2.62] |
| **FA** | `1-year post-IPO return (%) [Reserved]` | 一年期收益率预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/38 (0.0%)) | 全部缺失 |
| **FB** | `1-year wealth relative vs HSI [Reserved]` | 一年期相对恒指财富比预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/38 (0.0%)) | 全部缺失 |
| **FC** | `3-year post-IPO return (%) [Reserved]` | 三年期收益率预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/38 (0.0%)) | 全部缺失 |
| **FD** | `3-year wealth relative vs HSI [Reserved]` | 三年期相对恒指财富比预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/38 (0.0%)) | 全部缺失 |
| **FE** | `18A/18C regulatory milestone status` | 18A/18C 监管路径与商业化里程碑状态 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 3 种取值 ('Standard': 29, '18C (Specialist Tech)': 6, '18A (Biotech / B-tag)': 3) |
| **FF** | `Stabilizing manager` | 官方指定价格稳定经理人名称 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 7 种取值 ('China International Capital Corporation / Sponsor-OC': 24, 'China International Capital Corporation Hong Kong Securities Limited': 4, 'Morgan Stanley Asia Limited': 3) |
| **FG** | `Stabilization period end date` | 法定30天稳价期结束日期 | 深蓝 | `string` | Post-IPO 30-day stabilization window | 100% 完备 | 共 26 种取值 ('2026-03-05': 3, '2026-04-08': 3, '2026-04-29': 3) |
| **FH** | `Stabilization purchases occurred` | 稳价期内是否发生二级市场托单购买 (1=是, 0=否) | 深蓝 | `boolean` | Post-IPO 30-day stabilization window | 100% 完备 | 1 (是): 10 家 (26.3%), 0 (否): 28 家 |
| **FI** | `Over-allocation shares` | 国际配售超额配售股份数量（股） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 4,770,760.53 / 中位数 0.00 / 区间 [0.00, 42,726,800.00] |
| **FJ** | `Over-allocation (% of base offer)` | 超额配售股数占基础发售股份比例 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 0.15 / 中位数 0.15 / 区间 [0.05, 0.15] |
| **FK** | `Over-allotment option exercise date` | 超额配售权实际行使公告日期 | 深蓝 | `string` | Post-IPO 30-day stabilization window | 100% 完备 | 共 27 种取值 ('2026-03-05': 3, '2026-03-09': 3, '2026-03-30': 3) |
| **FL** | `Shares issued under over-allotment option` | 超额配售权最终发行股份数量（股） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 4,564,719.47 / 中位数 0.00 / 区间 [0.00, 42,726,800.00] |
| **FM** | `Over-allotment exercise percentage (%)` | 超额配售权行使比例 (行使股数/超额配售上限, %) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 0.43 / 中位数 0.04 / 区间 [0.00, 1.00] |
| **FN** | `Post-stabilization cliff return [-5, +5] (%)` | 稳价期结束日前后[-5, +5]交易日累计收益率（断崖效应测试） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Adequate (37/38 (97.37%)) | 均值 0.06 / 中位数 0.01 / 区间 [-0.25, 0.62] |
| **FO** | `Post-stabilization 20-day return [0, +20] (%)` | 稳价期结束后20个交易日累计收益率 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Adequate (37/38 (97.37%)) | 均值 0.07 / 中位数 -0.02 / 区间 [-0.42, 1.53] |
| **FP** | `Post-stabilization volume decay ratio (%)` | 稳价结束后20日均成交额相对稳价期内之比 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Adequate (37/38 (97.37%)) | 均值 0.53 / 中位数 0.35 / 区间 [0.10, 2.26] |
| **FQ** | `Day-5 BHR from Day-1 close (%)` | 挂牌首周 (T+5交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 0.08 / 中位数 0.02 / 区间 [-0.20, 0.69] |
| **FR** | `Day-5 wealth relative vs HSI` | 挂牌首周对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 1.06 / 中位数 1.02 / 区间 [0.80, 1.71] |
| **FS** | `Day-20 BHR from Day-1 close (%)` | 首月 (T+20交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | Adequate (37/38 (97.37%)) | 均值 0.13 / 中位数 0.05 / 区间 [-0.33, 2.11] |
| **FT** | `Day-20 wealth relative vs HSI` | 首月对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | Adequate (37/38 (97.37%)) | 均值 1.12 / 中位数 1.03 / 区间 [0.67, 3.01] |
| **FU** | `3-month BHR from Day-1 close (%)` | 首季 (T+63交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | Adequate (37/38 (97.37%)) | 均值 0.35 / 中位数 -0.03 / 区间 [-0.58, 6.21] |
| **FV** | `3-month wealth relative vs HSI` | 首季对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | Adequate (37/38 (97.37%)) | 均值 1.40 / 中位数 0.97 / 区间 [0.42, 7.29] |
| **FW** | `3-month wealth relative vs HSTECH` | 首季对标恒科财富相对比 (WR_HSTECH) | 深蓝 | `numeric` | Aftermarket event horizon window | Adequate (37/38 (97.37%)) | 均值 1.50 / 中位数 1.10 / 区间 [0.44, 8.44] |
| **FX** | `3-month average daily turnover (HK$)` | 首季度日均成交金额 (港元) | 深蓝 | `numeric` | Aftermarket event horizon window | Adequate (37/38 (97.37%)) | 均值 207,985,100.56 / 中位数 66,984,136.03 / 区间 [5,369,220.63, 1,590,398,283.17] |
| **FY** | `Amihud illiquidity (6M mean)` | 上市前6个月日均 Amihud (2002) 非流动性指标 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.03 / 中位数 0.00 / 区间 [0.00, 0.44] |
| **FZ** | `Zero-volume days count (first 6M)` | 上市前6个月零成交量交易日天数 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.03 / 中位数 0.00 / 区间 [0.00, 1.00] |
| **GA** | `Return volatility (first 6M daily std dev, %)` | 上市前6个月日度收益率标准差 (波动率, %) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.08 / 中位数 0.06 / 区间 [0.03, 0.25] |
| **GB** | `Maximum drawdown (first 6M, %)` | 上市前6个月二级市场最大回撤幅度 (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.56 / 中位数 0.54 / 区间 [0.36, 0.87] |
| **GC** | `Controlling shareholder 6-month disposal lockup expiry date` | 控股股东首阶段6个月绝对禁售期满日 | 深蓝 | `string` | Post-IPO lockup expiration events | 100% 完备 | 共 20 种取值 ('2026-09-30': 6, '2026-07-08': 3, '2026-07-09': 3) |
| **GD** | `Controlling shareholder 12-month cessation of control expiry date` | 控股股东次阶段12个月控制权锁定到期日 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 21 种取值 ('2027-03-30': 4, '2027-01-08': 3, '2027-01-09': 3) |
| **GE** | `Cornerstone unlock CAR [-5, +5] (%)` | 基石投资者解禁日前后[-5, +5]交易日累计超额收益 (CAR vs HSI) | 深蓝 | `numeric` | Post-IPO lockup expiration events | Adequate (27/38 (71.05%)) | 均值 -0.04 / 中位数 -0.02 / 区间 [-0.48, 0.32] |
| **GF** | `Cornerstone unlock CAR [-20, +20] (%)` | 基石投资者解禁日前后[-20, +20]交易日累计超额收益 (CAR vs HSI) | 深蓝 | `numeric` | Post-IPO lockup expiration events | Adequate (27/38 (71.05%)) | 均值 -0.04 / 中位数 -0.08 / 区间 [-0.67, 0.52] |
| **GG** | `Cornerstone unlock volume shock ratio` | 基石解禁后20日均换手额相对解禁前20日换手额之比 | 深蓝 | `numeric` | Post-IPO lockup expiration events | Adequate (27/38 (71.05%)) | 均值 1.44 / 中位数 1.07 / 区间 [0.38, 8.54] |
| **GH** | `Lead sponsor name` | 独家/联席牵头保荐人英文全称 | 深蓝 | `string` | Prospectus syndicate structure | 100% 完备 | 共 7 种取值 ('China International Capital Corporation / Sponsor-OC': 24, 'China International Capital Corporation Hong Kong Securities Limited': 4, 'Morgan Stanley Asia Limited': 3) |
| **GI** | `Joint sponsor count` | 保荐人总家数 (独家=1, 联席=2+) | 深蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **GJ** | `Sponsor commercial bank affiliate flag` | 保荐人是否属于商业银行系金融机构 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus syndicate structure | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 38 家 |
| **GK** | `Underwriting base commission rate (%)` | 承销基础佣金费率 (%) | 深蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **GL** | `Underwriting discretionary incentive fee rate (%)` | 承销酌情奖励费率估算 (%) | 深蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.01 / 中位数 0.01 / 区间 [0.01, 0.01] |
| **GM** | `Total underwriting fee rate (%)` | 承销总费率估算 (基础+奖励, %) | 深蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.01 / 中位数 0.01 / 区间 [0.01, 0.01] |
| **GN** | `Cornerstone investor count` | 基石投资者机构总家数 | 深蓝 | `numeric` | Prospectus / allotment institutional network | 100% 完备 | 均值 9.42 / 中位数 9.00 / 区间 [0.00, 25.00] |
| **GO** | `Cornerstone state-owned presence flag` | 基石投资者中是否包含国资/地方政府基金 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | 100% 完备 | 1 (是): 28 家 (73.7%), 0 (否): 10 家 |
| **GP** | `Crossover fund presence flag` | 是否包含兼具 Pre-IPO 与基石双重身份的跨界基金 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | 100% 完备 | 1 (是): 2 家 (5.3%), 0 (否): 36 家 |
| **GQ** | `Pre-IPO institutional investor count` | 主要 Pre-IPO 投资机构总数 | 深蓝 | `numeric` | Prospectus / allotment institutional network | 100% 完备 | 均值 2.66 / 中位数 3.00 / 区间 [0.00, 9.00] |
| **GR** | `Pre-IPO state-owned backing flag` | Pre-IPO 股东中是否包含国资机构 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | 100% 完备 | 1 (是): 27 家 (71.1%), 0 (否): 11 家 |
| **GS** | `FINI digital settlement regime` | 结算监管体制 (POST_FINI / PRE_FINI) | 深蓝 | `string` | Listing date regulatory regime | 100% 完备 | 共 1 种取值 ('POST_FINI': 38) |
| **GT** | `2025 pricing reform regime` | 发售与定价机制改革体制 (POST_2025_REFORM / PRE_2025_REFORM) | 深蓝 | `string` | Listing date regulatory regime | 100% 完备 | 共 1 种取值 ('POST_2025_REFORM': 38) |

---

## 三、计量软件导入指引 (Stata / Python)

配套清洗数据文件：`out/HKIPO-MB2026Q1_clean.csv`（编码：UTF-8 with BOM）。

### 1. Stata
```stata
* 导入纯净版 CSV 数据
import delimited "out/HKIPO-MB2026Q1_clean.csv", clear bindquote(strict) varnames(1)
describe
summarize
```

### 2. Python (pandas)
```python
import pandas as pd
df = pd.read_csv("out/HKIPO-MB2026Q1_clean.csv")
print(df.info())
print(df.describe())
```

---
*本数据代码本由 HK IPO Prospectus Pipeline 自动化分析引擎生成。*
