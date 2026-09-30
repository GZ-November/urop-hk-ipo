# 香港主板 2026 Q2 IPO 学术研究数据变量代码本 (Data Codebook)

- **样本规模 (N)**：45 家香港联交所主板新上市公司
- **变量总数 (K)**：202 维完整跨学科指标
- **数据层级划分**：浅绿官方基础 (11 列) + 浅蓝招股书披露 (77 列) + 深蓝配发及外部衍生 (114 列)
- **生成时间**：2026-09-30 18:03:37 | **数据基准**：`HKIPO-MB2026Q2.xlsx` (Sheet: NLR)

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
| **A** | `HKEx file# of the year` | 港交所年度申请编号 | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 62.93 / 中位数 63.00 / 区间 [40.00, 85.00] |
| **B** | `Stock Code` | 股份代号（四位港股代码，如 6082.HK） | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 45 种取值 ('6656.HK': 1, '0068.HK': 1, '3277.HK': 1) |
| **C** | `Company Name at time of listing` | 公司上市时法定英文名称 | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 45 种取值 ('Sigenergy Technology Co., Ltd. - H Shares': 1, 'Manycore Tech Inc.': 1, 'Gpixel Changchun Microelectronics Inc. - H Shares': 1) |
| **D** | `Date of Prospectus (dd/mm/yy)` | 招股书刊发日期 | 浅绿 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2026-04-08 ~ 2026-06-22 |
| **E** | `Date of Listing (dd/mm/yy)` | 正式挂牌上市交易日期 | 浅绿 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2026-04-16 ~ 2026-06-30 |
| **F** | `Sponsor(s)` | 独家/联席保荐人名单 | 浅绿 | `string` | Prospectus syndicate structure | 100% 完备 | 共 40 种取值 ('China International Capital Corporation Hong Kong Securities Limited': 4, 'CITIC Securities (Hong Kong) Limited': 2, 'China Securities (International) Corporate Finance Company Limited': 2) |
| **G** | `Reporting Accountants` | 申报会计师事务所 | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 8 种取值 ('Ernst & Young': 22, 'KPMG': 5, 'PricewaterhouseCoopers': 5) |
| **H** | `Valuer(s)` | 独立物业或资产估值师 | 浅绿 | `string` | Ex-ante prospectus disclosure | Sparse (6/45 (13.33%)) | 共 4 种取值 ('Jones Lang LaSalle Corporate Appraisal and Advisory Limited': 2, 'AVISTA Valuation Advisory Limited': 2, 'Asia-Pacific Consulting and Appraisal Limited': 1) |
| **I** | `Funds Raised HK (a)` | 香港公开发售募资额 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 221,232,113.80 / 中位数 128,268,560.00 / 区间 [39,994,542.00, 1,749,307,824.00] |
| **J** | `Funds Raised Int.(b)` | 国际配售募资额 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 2,046,300,914.53 / 中位数 982,386,450.00 / 区间 [359,946,132.00, 21,385,239,876.00] |
| **K** | `IPO Subscription Price (HK$)` | 最终发售定价 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 62.18 / 中位数 39.33 / 区间 [5.18, 324.20] |
| **L** | `Total (without option)` | Total (without option) | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 881,407,168.49 / 中位数 320,620,632.00 / 区间 [35,647,003.00, 14,731,366,060.00] |
| **M** | `Global Offering (without option)` | Global Offering (without option) | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 81,897,516.11 / 中位数 36,234,500.00 / 区间 [3,564,700.00, 896,686,000.00] |
| **N** | `Number of offer shares under the capitalization Issue` | 全球发售完成前的已发行股份总数。本数据集口径：一律填 L − M（Total 减去全球发售股数），即使招股书未披露「资本化发行」也必须照填，不得留 NaN。用于满足恒等式 L = N + Q。2026Q1 成品工作簿 38 家公司全部取 L − M，Q2 必须同口径。数值只取权威 SHARE CAPITAL 汇总表与封面，禁止取「历史沿革／资本化发行沿革」段落。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 819,436,007.93 / 中位数 273,685,950.00 / 区间 [32,082,303.00, 14,731,366,060.00] |
| **O** | `Number of offer shares under Capitalization Rest` | 与 col_N 同口径：一律填 L − M（全球发售完成前的已发行股份总数），即使招股书未披露「资本化转换」也必须照填，不得留 NaN。用于满足恒等式 L = O + M。2026Q1 成品 38 家全部为 L − M。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 799,509,652.38 / 中位数 273,685,950.00 / 区间 [32,082,303.00, 13,834,680,060.00] |
| **P** | `Sale Shares` | 老股出售（Sale Shares）数量。若为全部新股的 Offer for Subscription（无 Selling Shareholder），填数字 0，不得留 NaN，用于满足恒等式 M = Q + P。判据：封面／股本汇总表无 Sale Shares 行，且全文无 Selling Shareholder 披露。2026Q1 成品 38 家全部为 0。若确有老股出售，按招股书披露填写。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 19,926,355.56 / 中位数 0.00 / 区间 [0.00, 896,686,000.00] |
| **Q** | `New shares` | New shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 61,971,160.56 / 中位数 33,344,400.00 / 区间 [0.00, 811,811,880.00] |
| **R** | `Placing Shares` | Placing Shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 74,033,100.22 / 中位数 32,611,000.00 / 区间 [3,208,220.00, 807,017,000.00] |
| **S** | `Public Offer shares` | Public Offer shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 7,864,415.89 / 中位数 3,623,500.00 / 区间 [356,480.00, 89,669,000.00] |
| **T** | `Maximum Offer Price` | Maximum Offer Price | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 62.86 / 中位数 39.33 / 区间 [6.38, 324.20] |
| **U** | `Minimum Offer Price` | Minimum Offer Price | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (37/45 (82.22%)) | 均值 59.78 / 中位数 32.80 / 区间 [5.18, 324.20] |
| **V** | `Filing price revision (%)` | 发售定价偏离询价区间中点幅度（Hanley 1993 动态信息提取，固定价格发售为 0.00%） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 -0.00 / 中位数 0.00 / 区间 [-0.13, 0.12] |
| **W** | `Filing range width (%)` | 询价区间相对宽度（Beatty & Ritter 1986 事前估值不确定性，固定价格发售为 0.00%） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.05 / 中位数 0.00 / 区间 [0.00, 0.33] |
| **X** | `Pricing position in filing range` | 定价落点分类体系（Fixed price / Above range / At high / Midpoint / Within range / At low / Below range） | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 4 种取值 ('Fixed price': 31, 'At high': 5, 'At low': 5) |
| **Y** | `currency in financial information` | currency in financial information | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 3 种取值 ('RMB': 43, 'HKD': 1, 'USD': 1) |
| **Z** | `total assets in year-3 (3 years before IPO)` | total assets in year-3 (3 years before IPO) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (38/45 (84.44%)) | 均值 5,055,213,500.00 / 中位数 1,155,286,500.00 / 区间 [96,054,000.00, 51,509,636,000.00] |
| **AA** | `total assets in year-2` | total assets in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 5,493,623,600.00 / 中位数 1,048,535,000.00 / 区间 [132,886,000.00, 76,296,823,000.00] |
| **AB** | `total assets in year-1` | total assets in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (43/45 (95.56%)) | 均值 5,604,405,418.60 / 中位数 1,104,017,000.00 / 区间 [227,036,000.00, 96,205,628,000.00] |
| **AC** | `total equity in year-3` | total equity in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (38/45 (84.44%)) | 均值 2,139,044,684.21 / 中位数 461,408,000.00 / 区间 [-3,328,016,000.00, 20,843,047,000.00] |
| **AD** | `total equity in year-2` | total equity in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 1,985,681,622.22 / 中位数 407,550,000.00 / 区间 [-3,858,035,000.00, 24,357,948,000.00] |
| **AE** | `total equity in year-1` | total equity in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (43/45 (95.56%)) | 均值 1,941,831,465.12 / 中位数 503,243,000.00 / 区间 [-4,247,852,000.00, 26,345,328,000.00] |
| **AF** | `total liability in year-3` | total liability in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (38/45 (84.44%)) | 均值 2,916,168,815.79 / 中位数 889,662,000.00 / 区间 [76,510,000.00, 30,666,589,000.00] |
| **AG** | `total liability in year-2` | total liability in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 3,507,941,977.78 / 中位数 1,030,934,000.00 / 区间 [29,925,000.00, 53,372,763,000.00] |
| **AH** | `total liability in year-1` | total liability in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (43/45 (95.56%)) | 均值 3,662,573,953.49 / 中位数 934,833,000.00 / 区间 [41,258,000.00, 69,860,300,000.00] |
| **AI** | `Net sales in year-3` | Net sales in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (38/45 (84.44%)) | 均值 4,498,516,710.53 / 中位数 591,038,000.00 / 区间 [0.00, 85,338,484,000.00] |
| **AJ** | `Net sales in year-2` | Net sales in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (44/45 (97.78%)) | 均值 4,830,032,886.36 / 中位数 534,713,000.00 / 区间 [0.00, 109,877,987,000.00] |
| **AK** | `Net sales in year-1` | Net sales in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (44/45 (97.78%)) | 均值 6,809,356,329.55 / 中位数 708,146,000.00 / 区间 [0.00, 171,436,927,000.00] |
| **AL** | `Profit before tax in year-3` | Profit before tax in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (38/45 (84.44%)) | 均值 132,354,815.79 / 中位数 26,731,500.00 / 区间 [-646,097,000.00, 2,835,217,000.00] |
| **AM** | `Profit before tax in year-2` | Profit before tax in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 110,584,600.00 / 中位数 -14,934,000.00 / 区间 [-1,047,471,000.00, 3,037,064,000.00] |
| **AN** | `Profit before tax in year-1` | Profit before tax in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (44/45 (97.78%)) | 均值 289,416,250.00 / 中位数 -36,065,000.00 / 区间 [-1,342,376,000.00, 5,021,716,000.00] |
| **AO** | `Profit for the year in year-3` | Profit for the year in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (38/45 (84.44%)) | 均值 106,191,815.79 / 中位数 24,322,000.00 / 区间 [-646,097,000.00, 2,657,010,000.00] |
| **AP** | `Profit for the year in year-2` | Profit for the year in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 87,490,977.78 / 中位数 -12,700,000.00 / 区间 [-1,046,564,000.00, 2,916,351,000.00] |
| **AQ** | `Profit for the year in year-1` | Profit for the year in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (44/45 (97.78%)) | 均值 242,463,875.00 / 中位数 -37,081,500.00 / 区间 [-1,342,376,000.00, 4,311,988,000.00] |
| **AR** | `Underwriting Commission (% of fund raised HK (a)` | Underwriting Commission (% of fund raised HK (a) | 浅蓝 | `numeric` | Prospectus syndicate structure | Adequate (44/45 (97.78%)) | 均值 0.03 / 中位数 0.03 / 区间 [0.00, 0.05] |
| **AS** | `Underwriting Commission (% of fund raised Int.(b)` | Underwriting Commission (% of fund raised Int.(b) | 浅蓝 | `numeric` | Prospectus syndicate structure | Adequate (44/45 (97.78%)) | 均值 0.03 / 中位数 0.03 / 区间 [0.00, 0.05] |
| **AT** | `Over-allotment Option (%)` | Over-allotment Option (%) | 浅蓝 | `numeric` | Post-IPO 30-day stabilization window | Adequate (40/45 (88.89%)) | 均值 0.14 / 中位数 0.15 / 区间 [0.00, 0.15] |
| **AU** | `Principal business / industry` | Principal business / industry | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 45 种取值 ('Renewable energy - distributed energy storage system (DESS) solutions': 1, 'Cloud-native spatial design software (spatial design software industry)': 1, 'CMOS image sensor design and sales (semiconductor industry)': 1) |
| **AV** | `Listing route / applicable chapter` | Listing route / applicable chapter | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 35 种取值 ('Main Board': 4, 'Chapter 18A of the Listing Rules (Main Board)': 3, 'Main Board - Rule 8.05(3) market capitalisation/revenue test': 2) |
| **AW** | `Year-1 financial period end (dd/mm/yy)` | Year-1 financial period end (dd/mm/yy) | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2025-11-30 ~ 2026-03-31 |
| **AX** | `Operating cash flow in year-1 (before annualization)` | Operating cash flow in year-1 (before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (43/45 (95.56%)) | 均值 124,706,325.58 / 中位数 -63,977,000.00 / 区间 [-361,099,000.00, 4,620,074,000.00] |
| **AY** | `Cash and cash equivalents at year-1 end` | Cash and cash equivalents at year-1 end | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (43/45 (95.56%)) | 均值 757,628,162.79 / 中位数 209,058,000.00 / 区间 [3,720,000.00, 10,270,248,000.00] |
| **AZ** | `R&D expensed in year-1 (before annualization)` | R&D expensed in year-1 (before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (42/45 (93.33%)) | 均值 339,353,738.10 / 中位数 115,649,500.00 / 区间 [-266,036,000.00, 6,363,453,000.00] |
| **BA** | `Development costs capitalized in year-1 (additions, before annualization)` | Development costs capitalized in year-1 (additions, before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (42/45 (93.33%)) | 均值 1,889,428.57 / 中位数 0.00 / 区间 [0.00, 54,477,000.00] |
| **BB** | `Top 5 customers (% of year-1 revenue)` | Top 5 customers (% of year-1 revenue) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (38/45 (84.44%)) | 均值 0.55 / 中位数 0.50 / 区间 [0.00, 1.00] |
| **BC** | `Comments / Annualization factor` | 最近一期财务数据对应的年化因子与口径说明 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 1.00 / 中位数 1.00 / 区间 [1.00, 1.00] |
| **BD** | `Pre-IPO VC/PE backing (1=yes; 0=no)` | 是否引入 Pre-IPO VC/PE 投资者：1=有，0=无。看 HISTORY AND DEVELOPMENT — Pre-IPO Investments 与 SUBSTANTIAL SHAREHOLDERS 名单；只要有专业投资机构（VC/PE/产业基金）在上市前入股即 1。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.84 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BE** | `Pre-IPO VC backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。早期/成长期专业风险投资基金为 1；未找到证据不等于 0，无法确认时填 NaN。分类依据须在本字段 quote 中体现。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.84 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BF** | `Pre-IPO PE backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。中晚期私募股权基金或并购基金为 1；未找到证据不等于 0，无法确认时填 NaN。分类依据须在本字段 quote 中体现。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.84 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BG** | `Pre-IPO CVC backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。发行人产业股东须有战略投资/企业风投关系依据才归 CVC；普通产业股东不能自动算 CVC。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (35/45 (77.78%)) | 均值 0.74 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BH** | `Pre-IPO State/Gov backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。有明确国资、政府或产业引导基金背景的机构为 1；国资身份不自动代表 VC/PE。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (39/45 (86.67%)) | 均值 0.82 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BI** | `Top-tier VC/PE backing (1=yes; 0=no)` | 仅在本公司招股书确认一线知名 VC/PE 机构持有重要股权或领投时填 1；不得仅凭机构知名度推断其参与本公司投资。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (32/45 (71.11%)) | 均值 0.78 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BJ** | `Key Pre-IPO investors` | 仅列本公司招股书披露的上市前投资者，采用一致的英文全称/拼音并以分号分隔；同一投资者只记一次，不从其他 cohort 补名单。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (38/45 (84.44%)) | 共 38 种取值 ('Shanghai Yusong; Jiefeng Technology; Zhuhai Meiheng; Guangzhou Huaxin; Andaman International; Jiaxing Yuzai; Suzhou V Fund; Jinan V Fund; Gongqingcheng Yunteng; Jiaxing Dingyun; Xiamen Xiaoyu; Hangzhou Yiyun; Xingxu Yaoneng; Xingxu New Energy; TTGG Ventures': 1, 'GGV Capital V L.P.; GGV Capital V Entrepreneurs Fund L.P.; Shanghai Yuanyan Enterprise Management Consulting Partnership (Limited Partnership); Shunwei Growth III Limited; Astrend Opportunity III Alpha Limited; IDG Technology Venture Investment IV, L.P.; IDG Technology Venture Investment V, L.P.; New Gultar Limited; HH SUM-I Holdings Limited; MPC III L.P.; MPC III-A L.P.; Coatue PE Asia 36 LLC; Coatue PE Asia 73 LLC; HES VENTURES I, INC.; HEARST VENTURES, INC.; QINGTING INVESTMENTS PTE. LTD.; Linear Venture, Ltd.; Mountain Glacier Investments Ltd.; Planetree Partners I, L.P.; EXC Investment LLC; Planetree EXC Investment LLC; Aquanauts 3820 III L.P.': 1, 'Zhuhai Qixin; Gaoling Yurun; Xianjin Zhizao; Guoce Xiangchi; Xiamen Yuanfeng; Huashun Guangzhou; Shenzhen Jiusi; Juyuan Xincheng; QIN Hao; Wuhu Tuochen; Suzhou Fangguang; Yibin Chendao; Shengyu Huatian; Zhongke Chuangxing; Changzhou Fangguang; Pingyang Yuanxin; Donghu Guolong; Zhongke Xiandao; Ningbo Yuxi; Zhongke Ketou; Thriving Capital; Jilin Yuanheng': 1) |
| **BK** | `Pre-IPO institutional shareholding (%)` | 上市前 VC/PE/CVC/国资机构合计持股比例，取紧邻上市前的股权口径，不能混入 IPO 新股或基石配售；统一填 0–1 小数（如 12.5%=0.125）。只有招股书披露或可用披露数字复算时填写，否则 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (37/45 (82.22%)) | 均值 0.33 / 中位数 0.32 / 区间 [0.00, 0.84] |
| **BL** | `Pre-IPO investor board seat (1=yes; 0=no)` | 只有能从招股书明确关联到 Pre-IPO 投资机构的非执行董事或正式观察员席位才填 1；没有证据不等于 0，无法确认时填 NaN。 | 浅蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 24 家 (53.3%), 0 (否): 21 家 |
| **BM** | `Earliest Pre-IPO investment round` | 从本公司招股书披露的 Pre-IPO 投资轮次中取最早一轮，保留披露的标准轮次名称；只有明确说明没有外部上市前投资时填 None，否则无法确认时 NA。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (38/45 (84.44%)) | 共 26 种取值 ('Series A Financing': 7, 'Series A': 6, 'Series Angel Financing': 2) |
| **BN** | `Pre-IPO holding duration (years)` | 从最早 Pre-IPO 投资协议日期至本公司招股书日期计算年数，保留两位小数；起始日期无法确认则 NaN。每家公司必须使用自己的招股书日期，不沿用其他季度日期。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (36/45 (80.0%)) | 均值 9.17 / 中位数 8.29 / 区间 [1.13, 17.77] |
| **BO** | `Ultimate controller type` | 最终控制人类型（如：自然人 / 家族 / 国资委 / 地方政府 / 外资 / 无实际控制人）。取 SUBSTANTIAL SHAREHOLDERS 与 Controlling Shareholders 段的实际控制人身份表述。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 41 种取值 ('Individual (natural person)': 3, 'Natural person': 2, 'Individual': 2) |
| **BP** | `Controller economic interest at listing (%)` | 控制人上市时**经济权益**（持股比例），填小数。取 CONTROLLING/SUBSTANTIAL SHAREHOLDERS 表的持股百分比。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (44/45 (97.78%)) | 均值 0.38 / 中位数 0.35 / 区间 [0.11, 0.75] |
| **BQ** | `Controller voting rights at listing (%)` | 控制人上市时**投票权**比例，填小数。有 WVR（同股不同权）时与持股不同，取投票权那一列；无 WVR 通常与 BC 相同。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (44/45 (97.78%)) | 均值 0.39 / 中位数 0.35 / 区间 [0.11, 0.80] |
| **BR** | `Interest-bearing debt at year-1 end` | year-1 期末**总有息负债**（用与 col_V 相同的披露货币基本单位）。包含短期借款、长期借款、租赁负债及带息应付票据债券等带息债务总额，取 INDEBTEDNESS 表格的 Total 余额；不含应付账款等无息负债。必须换算为货币基本单位（乘表格千元/百万元乘数）。期末余额，不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (44/45 (97.78%)) | 均值 1,905,240,795.45 / 中位数 318,002,000.00 / 区间 [894,000.00, 20,018,095,000.00] |
| **BS** | `Technology commercialization stage` | 技术商业化阶段（如：研发阶段 / 小批量试产 / 商业化初期 / 规模商业化 / 已量产）。按 BUSINESS 与业务摘要里的产品状态表述填，不要按行业推测。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (38/45 (84.44%)) | 共 32 种取值 ('Mass production and commercialization': 3, 'Pre-Commercial Company': 2, 'Commercialized': 2) |
| **BT** | `Debt repayment (% of planned net IPO proceeds)` | 计划净募资中用于**偿债**的比例，填小数。取 USE OF PROCEEDS 里用于偿还借款/债务的金额 ÷ 计划净募资额；没有该用途填 0。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (43/45 (95.56%)) | 均值 0.01 / 中位数 0.00 / 区间 [0.00, 0.20] |
| **BU** | `Listing board` | 上市板块（Main Board 主板） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Main Board': 45) |
| **BV** | `Share class` | 股份类别（如 H Shares / A Shares / Class A Ordinary Shares / Class B Ordinary Shares）。按招股书股本表的类别名称填。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 5 种取值 ('H Shares': 39, 'Ordinary Shares': 2, 'Ordinary shares': 2) |
| **BW** | `A+H issuer flag` | A+H 两地上市发行人标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 9 家 (20.0%), 0 (否): 36 家 |
| **BX** | `WVR flag` | 不同投票权/同股不同权架构标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 1 家 (2.2%), 0 (否): 44 家 |
| **BY** | `Chapter 18A flag` | 第 18A 章未盈利生物科技公司标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 8 家 (17.8%), 0 (否): 37 家 |
| **BZ** | `Chapter 18C flag` | 第 18C 章特专科技公司标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 7 家 (15.6%), 0 (否): 38 家 |
| **CA** | `Industry classification code` | 恒生行业分类 HSICS 6 位业务细分代码 | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 382,154.67 / 中位数 281,020.00 / 区间 [51,010.00, 703,020.00] |
| **CB** | `Industry classification system and version` | 行业分类系统与版本号 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('HSICS (Hang Seng Industry Classification System) 2026': 45) |
| **CC** | `Incorporation date` | 公司**法定注册成立日期**（dd/mm/yy）。必须优先取自 Statutory and General Information (Appendix V '1. Incorporation')、History & Development 或 Accountants' Report (附注 1)。严禁从 Definitions (释义) 章节取值（释义章节常有起草笔误或仅为前期筹备日）。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2002-07-05 ~ 2025-10-03 |
| **CD** | `Firm age at IPO (years)` | 公司成立至上市年限（Lowry et al. 2017 Table 3.4 基础控制变量） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 13.53 / 中位数 13.22 / 区间 [0.67, 23.99] |
| **CE** | `Place of incorporation` | 公司注册成立法域（如 Cayman Islands, PRC 等） | 深蓝 | `string` | Ex-ante prospectus disclosure | Sparse (10/45 (22.22%)) | 共 2 种取值 ('PRC': 9, 'Cayman Islands': 1) |
| **CF** | `Principal place of business` | 主要营业地点（城市/国家），如 PRC、Hong Kong、Shenzhen, PRC。取公司资料或注册办事处段。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 42 种取值 ('Shanghai, PRC': 3, 'Room 1920, 19/F, Lee Garden One, 33 Hysan Avenue, Causeway Bay, Hong Kong': 2, 'Building 12-2, 678 Yunqiao Road, Pilot Free Trade Zone, Shanghai, PRC': 1) |
| **CG** | `Financial statement unit multiplier` | 财务报表基础货币乘数（千元/万元/百万元） | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (41/45 (91.11%)) | 均值 25,365.85 / 中位数 1,000.00 / 区间 [1,000.00, 1,000,000.00] |
| **CH** | `Accounting standard` | 财务报表采用的会计准则（如 IFRS Accounting Standards / HKFRS / ASBE / US GAAP）。取会计师报告开头声明。 | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 7 种取值 ('IFRS Accounting Standards': 22, 'IFRS': 11, 'HKFRS': 4) |
| **CI** | `Year-3 financial period start` | 往绩记录第三年前期起始日 | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2022-12-01 ~ 2023-04-01 |
| **CJ** | `Year-3 financial period end` | 往绩记录第三年前期截止日 | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2023-11-30 ~ 2024-03-31 |
| **CK** | `Year-2 financial period start` | 往绩记录第二年前期起始日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2023-12-01 ~ 2024-04-01 |
| **CL** | `Year-2 financial period end` | 往绩记录第二年前期截止日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2024-11-30 ~ 2025-03-31 |
| **CM** | `Year-1 financial period start` | 往绩记录最近一期起始日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2024-12-01 ~ 2025-04-01 |
| **CN** | `Year-1 net sales (original, pre-annualization)` | 最近一期营业收入原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | Adequate (44/45 (97.78%)) | 均值 6,809,356,329.55 / 中位数 708,146,000.00 / 区间 [0.00, 171,436,927,000.00] |
| **CO** | `Year-1 profit before tax (original)` | 最近一期税前利润原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | Adequate (44/45 (97.78%)) | 均值 289,416,250.00 / 中位数 -36,065,000.00 / 区间 [-1,342,376,000.00, 5,021,716,000.00] |
| **CP** | `Year-1 profit for period (original)` | 最近一期净利润原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | Adequate (44/45 (97.78%)) | 均值 242,463,875.00 / 中位数 -37,081,500.00 / 区间 [-1,342,376,000.00, 4,311,988,000.00] |
| **CQ** | `Subscription opening date` | 香港公开发售**开始认购日期**（dd/mm/yy）。取 EXPECTED TIMETABLE。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2026-04-08 ~ 2026-06-22 |
| **CR** | `Subscription closing date` | 香港公开发售**截止认购日期**（dd/mm/yy）。取 EXPECTED TIMETABLE。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2026-04-13 ~ 2026-06-25 |
| **CS** | `H shares after IPO (base; no options)` | 上市后**在港交所挂牌的股份数**（base，不含超额配售）。统一口径：① 内地 H 股发行人全部转换时 = 总股本；② 部分转换时 = 由未上市股转换的 H 股 + 新发 H 股（剩余未上市股不挂牌，不计入）；③ A+H 发行人 = 仅新发 H 股（A 股在沪深市场挂牌，不计入）；④ 开曼/境外发行人没有 H 股类别，其全部股份均在港交所挂牌，故 = 上市后已发行股份总数。即：本列恒等于「港交所挂牌的股份数」，四类结构可比。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 272,359,305.27 / 中位数 149,523,500.00 / 区间 [12,838,650.00, 1,700,106,840.00] |
| **CT** | `Gross profit in year-1` | year-1 **毛利**（用与 col_V 相同的披露货币基本单位）。取损益表的 Gross profit。强制期间锚定：必须与 col_AT 严格同期间！若 col_AT 为中期报告期（如截至 2025 年 6 月 30 日或 9 月 30 日止期间），必须严格提取该中期报告期对应列的原值，绝对严禁错采前一完整财年（FY2024）的数值。必须换算为货币基本单位（乘表格千元/百万元乘数）。不年化——手册明确仅 year-1 销售/税前利润/净利润年化，毛利不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (43/45 (95.56%)) | 均值 928,677,139.53 / 中位数 204,358,000.00 / 区间 [-7,600,000.00, 13,230,496,000.00] |
| **CU** | `Capital expenditure in year-1` | year-1 **资本开支**（用与 col_V 相同的披露货币基本单位）。取现金流量表“购建物业、厂房及设备”或 CAPITAL EXPENDITURE 段。强制期间锚定：必须与 col_AT 严格同期间！若 col_AT 为中期报告期（如截至 2025 年 6 月 30 日或 9 月 30 日止期间），必须严格提取该中期报告期实际资本开支原值，绝对严禁错采前一完整财年（FY2024）数值。必须换算为货币基本单位（乘表格千元/百万元乘数）。不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (43/45 (95.56%)) | 均值 279,958,418.60 / 中位数 29,541,000.00 / 区间 [368,000.00, 6,388,985,000.00] |
| **CV** | `Audit opinion (year-1)` | year-1 **审计意见类型**（如 无保留意见 / Unqualified opinion / Qualified opinion）。取会计师报告的审计意见段。 | 浅蓝 | `string` | Track record period financial disclosure | Adequate (43/45 (95.56%)) | 共 8 种取值 ('Unqualified opinion (true and fair view)': 18, 'Unqualified (true and fair view)': 9, 'Unqualified': 6) |
| **CW** | `Listing expenses (HK$)` | **总上市费用**（HK$ 基本单位，含承销佣金与其他开支）。取 UNDERWRITING COMMISSIONS AND LISTING EXPENSES 段的合计。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 94,820,000.00 / 中位数 86,900,000.00 / 区间 [14,900,000.00, 264,000,000.00] |
| **CX** | `Cornerstone investor names` | Cornerstone investor names | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (37/45 (82.22%)) | 共 37 种取值 ('Aranda Investments Pte. Ltd.; Shanghai Lujiazui (Group) Co., Ltd. (GUOTAI JUNAN INVESTMENTS (HONG KONG) LIMITED OTC Swap); Goldman Sachs Asset Management (Hong Kong) Limited; HHLR Advisors, Ltd.; Hillhouse Investment Management, Ltd.; UBS Asset Management (Singapore) Ltd.; AXA Investment Managers UK Limited; CPE Energy Investment Limited; Lazurite Hime L.P.; Baring Asset Management (Asia) Limited; Charoen Pokphand Robot Limited; CPIC Investment Management (H.K.) Company Limited; Fullgoal Asset Management (HK) Limited; Fullgoal Fund Management Co., Ltd.; Greenwoods Asset Management Hong Kong Limited; Huadeng Technology Space Ventures Ltd; ICBC Wealth Management Co., Ltd.; Perseverance Asset Management International (Singapore) Pte. Ltd.; Scene Cloud Global Limited; Tropical Terrain Limited; 3W Fund Management Limited': 1, 'Taikang Life Insurance Co., Ltd; Sunshine Life Insurance Corporation Limited; GF Fund Management Co., Ltd.; GF International Investment Management Limited; REDWOOD ELITE LIMITED; Mirae Asset Securities Co., Ltd.; RIME Capital Limited; Hesai Hong Kong Limited; Guohui (HK) Holdings Co., Limited; CR Construction Group Holdings Limited': 1, 'CPE Peepal; HHLRA; UBS AM Singapore; Arc Avenue; Boyu; Fullgoal; GF Fund; Greenwoods; Mirae HK; Perseverance Asset Management; Yield Royal Investment; 3W Fund; Eastern Bell Capital VIII; ICBC Wealth; Protium Capital Limited; Source Code Capital; WT Asset Management; E Fund; China AMC; Cithara Fund; Panjing Fund; Value Partners; China Orient Multi-Strategy Master Fund; CMSIM': 1) |
| **CY** | `Final cornerstone allocation (% of base offer)` | Final cornerstone allocation (% of base offer) | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 0.33 / 中位数 0.37 / 区间 [0.00, 0.65] |
| **CZ** | `Earliest cornerstone unlock date (dd/mm/yy)` | 基石投资者最早解禁日期 | 深蓝 | `date` | Post-IPO lockup expiration events | Adequate (37/45 (82.22%)) | 区间: 2026-10-16 ~ 2026-12-30 |
| **DA** | `Subscription Ratio (times)` | Subscription Ratio (times) | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 3,198.68 / 中位数 2,003.16 / 区间 [4.42, 14,855.40] |
| **DB** | `Public applicants` | Public applicants | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 203,846.38 / 中位数 202,730.00 / 区间 [22,329.00, 383,309.00] |
| **DC** | `Public valid applied shares` | Public valid applied shares | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 10,785,534,139.42 / 中位数 4,969,471,300.00 / 区间 [39,645,800.00, 84,572,151,000.00] |
| **DD** | `Public subscription original wording` | Public subscription original wording | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 45 种取值 ('Subscription level 1,102.05 times': 1, 'Subscription level 1,590.56 times': 1, 'Subscription level 1,138.21 times': 1) |
| **DE** | `Pricing date` | Pricing date | 深蓝 | `date` | Ex-ante prospectus disclosure | Sparse (19/45 (42.22%)) | 区间: 2026-04-15 ~ 2026-06-26 |
| **DF** | `Allotment announcement date` | Allotment announcement date | 深蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2026-04-15 ~ 2026-06-29 |
| **DG** | `Final global offering shares (before over-allotment)` | Final global offering shares (before over-allotment) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 82,478,010.56 / 中位数 36,234,500.00 / 区间 [3,564,700.00, 896,686,000.00] |
| **DH** | `Final public offer shares` | Final public offer shares | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 8,885,061.00 / 中位数 4,197,800.00 / 区间 [356,480.00, 89,669,000.00] |
| **DI** | `Final placing shares` | Final placing shares | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 73,592,949.56 / 中位数 32,611,000.00 / 区间 [3,208,220.00, 807,017,000.00] |
| **DJ** | `Over-allotment shares actually issued` | Over-allotment shares actually issued | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 3,541,094.00 / 中位数 0.00 / 区间 [0.00, 30,184,000.00] |
| **DK** | `Greenshoe exercise rate (%)` | 绿鞋实际行使比例（Ellis et al. 2000 超额配售执行度与价格支持） | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.39 / 中位数 0.00 / 区间 [0.00, 1.00] |
| **DL** | `Actual clawback / reallocation description` | Actual clawback / reallocation description | 深蓝 | `string` | Ex-ante prospectus disclosure | Adequate (44/45 (97.78%)) | 共 44 种取值 ('No clawback triggered (Claw-back triggered: N/A); the final number of Offer Shares under the Hong Kong Public Offering (1,357,400) equals the initial number and represents 10.0% of the Global Offering.': 1, 'Reallocation: No. No. of Offer Shares reallocated from the International Offering: 0. Final no. of Offer Shares under the Hong Kong Public Offering: 16,062,000, being 10% of the Global Offering before exercise of the Over-allotment Option.': 1, 'No clawback triggered (Claw-back triggered: No); the final number of Offer Shares under the Hong Kong Public Offering (6,529,500) equals the initial number and represents 10.00% of the Global Offering, with no reallocation from the International Offering.': 1) |
| **DM** | `Net IPO proceeds to issuer (HK$)` | Net IPO proceeds to issuer (HK$) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 1,981,655,565.71 / 中位数 1,018,700,000.00 / 区间 [338,800,000.00, 19,889,400,000.00] |
| **DN** | `Public shareholding at listing (%)` | Public shareholding at listing (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (44/45 (97.78%)) | 均值 0.40 / 中位数 0.41 / 区间 [0.05, 0.83] |
| **DO** | `Share base used for both public shareholding ratios` | Share base used for both public shareholding ratios | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 878,940,738.33 / 中位数 308,377,319.00 / 区间 [35,647,003.00, 14,731,366,060.00] |
| **DP** | `Unrestricted public shareholding at listing (%)` | Unrestricted public shareholding at listing (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (44/45 (97.78%)) | 均值 0.08 / 中位数 0.08 / 区间 [0.03, 0.25] |
| **DQ** | `Free float denominator description` | Free float denominator description | 深蓝 | `string` | Ex-ante prospectus disclosure | Adequate (44/45 (97.78%)) | 共 22 种取值 ('Free float denominator = total issued shares upon listing (col_CZ); numerator = offer shares minus cornerstone allocation': 23, 'Free float denominator = total issued shares upon Listing (before exercise of the Over-allotment Option) = 246,796,930; numerator = Offer Shares minus cornerstone allocation.': 1, 'Free float excludes H Shares held by Cornerstone Investors upon Listing (six-month lock-up); denominator = total issued shares upon Listing (before exercise of the Over-allotment Option) = 435,294,200.': 1) |
| **DR** | `Free float denominator shares` | Free float denominator shares | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (44/45 (97.78%)) | 均值 896,405,361.93 / 中位数 314,498,975.50 / 区间 [35,647,003.00, 14,731,366,060.00] |
| **DS** | `HSI return over 20 trading days before prospectus (%)` | 招股日前 20 个交易日恒生指数累计收益率 (%) | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 -0.02 / 中位数 -0.02 / 区间 [-0.08, 0.06] |
| **DT** | `HK ordinary IPO count in 90 calendar days before prospectus` | 招股日前 90 个自然日香港普通主板 IPO 上市数量 | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 33.73 / 中位数 35.00 / 区间 [28.00, 38.00] |
| **DU** | `1-month HIBOR before prospectus (%)` | 招股日前一交易日香港银行同业拆借 1 个月 HIBOR 利率 (%) | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.03 / 中位数 0.03 / 区间 [0.02, 0.03] |
| **DV** | `Banking system aggregate balance before prospectus (HK$)` | 招股日前一交易日香港银行体系总结余 (HK$) | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 53,944,755,555.56 / 中位数 53,886,000,000.00 / 区间 [53,828,000,000.00, 54,867,000,000.00] |
| **DW** | `First trading day closing price (HK$)` | 首日上市二级市场收盘价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 124.25 / 中位数 61.20 / 区间 [2.81, 886.00] |
| **DX** | `First-day return / Underpricing (%)` | 上市首日抑价率 / 初始收益率（Rock 1986 / Ritter 1984 核心被解释变量） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 0.92 / 中位数 0.80 / 区间 [-0.57, 3.84] |
| **DY** | `Money left on the table (HK$)` | 留在桌面上的财富 / 抑价转移财富总额（Loughran & Ritter 2002 前景理论指标） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 1,270,703,547.71 / 中位数 913,419,520.00 / 区间 [-1,560,233,640.00, 10,075,752,000.00] |
| **DZ** | `First trading day opening price (HK$)` | 首日上市二级市场开盘价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 118.88 / 中位数 61.55 / 区间 [4.32, 880.00] |
| **EA** | `First trading day high (HK$)` | 首日上市二级市场盘中最高价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 138.05 / 中位数 66.35 / 区间 [4.60, 996.00] |
| **EB** | `First trading day low (HK$)` | 首日上市二级市场盘中最低价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 107.82 / 中位数 57.30 / 区间 [2.80, 807.00] |
| **EC** | `First trading day volume (shares)` | 首日上市二级市场全天成交量（股） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 24,957,480.87 / 中位数 12,671,555.00 / 区间 [911,040.00, 192,052,421.00] |
| **ED** | `First-day flipping ratio (%)` | 首日短线翻转抛售率 / 成交量占全球发售比例（Aggarwal 2003 机构抛售假说） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 0.42 / 中位数 0.38 / 区间 [0.03, 0.93] |
| **EE** | `First trading day turnover (HK$)` | 首日上市二级市场全天成交金额 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 1,375,207,839.56 / 中位数 694,075,300.00 / 区间 [230,830,000.00, 10,784,221,200.00] |
| **EF** | `Offer mechanism` | 适用发售与回拨制度（2025-08-04 前 PN18/18C.09；之后 Mechanism A/B） | 深蓝 | `string` | Ex-ante prospectus disclosure | Adequate (42/45 (93.33%)) | 共 2 种取值 ('Mechanism B': 29, 'Mechanism A': 13) |
| **EG** | `Applicable IPO rules / transition basis` | 适用之上市规则过渡基准（FINI 改革规则） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 3 种取值 ('FINI (from 22/11/2023); 2025-08-04 pricing reform (Mechanism A/B; six-month cornerstone lock-up retained); this IPO: Mechanism B': 29, 'FINI (from 22/11/2023); 2025-08-04 pricing reform (Mechanism A/B; six-month cornerstone lock-up retained); this IPO: Mechanism A': 13, 'FINI (from 22/11/2023); 2025-08-04 pricing reform (Mechanism A/B; six-month cornerstone lock-up retained)': 3) |
| **EH** | `Company Chinese Name` | Company Chinese Name | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (44/45 (97.78%)) | 共 44 种取值 ('思格新能源（上海）股份有限公司': 1, '群核科技': 1, '长春长光辰芯微电子股份有限公司': 1) |
| **EI** | `Current listing status` | 当前挂牌存续状态 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Active': 45) |
| **EJ** | `1-month post-IPO close price (HK$)` | 第20个交易日收盘价（窗口成熟后填报） | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 113.53 / 中位数 59.00 / 区间 [3.60, 682.50] |
| **EK** | `1-month BHR from Day-1 close (%)` | 由首日收盘至第20个交易日的买入持有收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 -0.05 / 中位数 -0.15 / 区间 [-0.51, 1.09] |
| **EL** | `1-month total return from offer price (%)` | 由发售价至第20个交易日的累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.79 / 中位数 0.37 / 区间 [-0.45, 5.16] |
| **EM** | `1-month HSI return (%)` | 同期恒生指数累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.01 / 中位数 -0.01 / 区间 [-0.10, 0.11] |
| **EN** | `1-month HSTECH return (%)` | 同期恒生科技指数累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.00 / 中位数 0.02 / 区间 [-0.13, 0.09] |
| **EO** | `1-month wealth relative vs HSI` | 一个月相对恒指财富比 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.95 / 中位数 0.86 / 区间 [0.45, 2.32] |
| **EP** | `1-month wealth relative vs HSTECH` | 一个月相对恒生科技指数财富比 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.95 / 中位数 0.86 / 区间 [0.46, 2.37] |
| **EQ** | `1-month average daily turnover (HK$)` | 上市后首20个交易日日均成交额 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 196,129,988.29 / 中位数 66,568,305.00 / 区间 [22,264,910.00, 2,066,770,985.00] |
| **ER** | `6-month post-IPO close price (HK$)` | 六个月目标日后首个交易日收盘价（窗口成熟后填报） | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **ES** | `6-month BHR from Day-1 close (%)` | 由首日收盘至六个月目标交易日的买入持有收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **ET** | `6-month total return from offer price (%)` | 由发售价至六个月目标交易日的累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **EU** | `6-month HSI return (%)` | 同期恒生指数累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **EV** | `6-month HSTECH return (%)` | 同期恒生科技指数累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **EW** | `6-month wealth relative vs HSI` | 六个月相对恒指财富比 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **EX** | `6-month wealth relative vs HSTECH` | 六个月相对恒生科技指数财富比 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **EY** | `6-month average daily turnover (HK$)` | 六个月目标日前20个交易日日均成交额 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **EZ** | `Liquidity decay ratio (6M vs Day-1 turnover)` | 六个月窗口日均成交额相对首日成交额比率 | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FA** | `1-year post-IPO return (%) [Reserved]` | 一年期收益率预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FB** | `1-year wealth relative vs HSI [Reserved]` | 一年期相对恒指财富比预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FC** | `3-year post-IPO return (%) [Reserved]` | 三年期收益率预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FD** | `3-year wealth relative vs HSI [Reserved]` | 三年期相对恒指财富比预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FE** | `18A/18C regulatory milestone status` | 18A/18C 监管路径与商业化里程碑状态 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 3 种取值 ('Standard': 30, '18A (Biotech / B-tag)': 8, '18C (Specialist Tech)': 7) |
| **FF** | `Stabilizing manager` | 官方指定价格稳定经理人名称 | 深蓝 | `string` | Ex-ante prospectus disclosure | Sparse (22/45 (48.89%)) | 共 10 种取值 ('China International Capital Corporation Hong Kong Securities Limited': 8, 'CLSA Limited': 6, 'Haitong International Securities Company Limited': 1) |
| **FG** | `Stabilization period end date` | 法定30天稳价期结束日期 | 深蓝 | `string` | Post-IPO 30-day stabilization window | Sparse (10/45 (22.22%)) | 共 8 种取值 ('2026-07-23': 3, '2026-05-13': 1, '2026-05-20': 1) |
| **FH** | `Stabilization purchases occurred` | 稳价期内是否发生二级市场托单购买 (1=是, 0=否) | 深蓝 | `boolean` | Post-IPO 30-day stabilization window | Sparse (10/45 (22.22%)) | 1 (是): 1 家 (10.0%), 0 (否): 9 家 |
| **FI** | `Over-allocation shares` | 国际配售超额配售股份数量（股） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Sparse (11/45 (24.44%)) | 均值 9,057,968.18 / 中位数 8,513,300.00 / 区间 [1,335,000.00, 30,184,000.00] |
| **FJ** | `Over-allocation (% of base offer)` | 超额配售股数占基础发售股份比例 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Sparse (9/45 (20.0%)) | 均值 0.19 / 中位数 0.15 / 区间 [0.05, 0.54] |
| **FK** | `Over-allotment option exercise date` | 超额配售权实际行使公告日期 | 深蓝 | `string` | Post-IPO 30-day stabilization window | Adequate (38/45 (84.44%)) | 共 28 种取值 ('2026-06-30': 3, '2026-07-23': 3, '2026-05-20': 2) |
| **FL** | `Shares issued under over-allotment option` | 超额配售权最终发行股份数量（股） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Adequate (31/45 (68.89%)) | 均值 5,451,155.81 / 中位数 2,036,000.00 / 区间 [0.00, 30,184,000.00] |
| **FM** | `Over-allotment exercise percentage (%)` | 超额配售权行使比例 (行使股数/超额配售上限, %) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Adequate (32/45 (71.11%)) | 均值 0.64 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **FN** | `Post-stabilization cliff return [-5, +5] (%)` | 稳价期结束日前后[-5, +5]交易日累计收益率（断崖效应测试） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Sparse (10/45 (22.22%)) | 均值 -0.12 / 中位数 -0.06 / 区间 [-0.36, 0.11] |
| **FO** | `Post-stabilization 20-day return [0, +20] (%)` | 稳价期结束后20个交易日累计收益率 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Sparse (10/45 (22.22%)) | 均值 0.01 / 中位数 0.00 / 区间 [-0.44, 0.45] |
| **FP** | `Post-stabilization volume decay ratio (%)` | 稳价结束后20日均成交额相对稳价期内之比 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Sparse (10/45 (22.22%)) | 均值 0.33 / 中位数 0.26 / 区间 [0.11, 0.79] |
| **FQ** | `Day-5 BHR from Day-1 close (%)` | 挂牌首周 (T+5交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 -0.01 / 中位数 -0.04 / 区间 [-0.50, 0.75] |
| **FR** | `Day-5 wealth relative vs HSI` | 挂牌首周对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 0.99 / 中位数 0.96 / 区间 [0.49, 1.71] |
| **FS** | `Day-20 BHR from Day-1 close (%)` | 首月 (T+20交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 -0.05 / 中位数 -0.15 / 区间 [-0.51, 1.09] |
| **FT** | `Day-20 wealth relative vs HSI` | 首月对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 0.95 / 中位数 0.86 / 区间 [0.45, 2.32] |
| **FU** | `3-month BHR from Day-1 close (%)` | 首季 (T+63交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 -0.17 / 中位数 -0.30 / 区间 [-0.71, 2.46] |
| **FV** | `3-month wealth relative vs HSI` | 首季对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | Adequate (28/45 (62.22%)) | 均值 0.89 / 中位数 0.77 / 区间 [0.30, 3.43] |
| **FW** | `3-month wealth relative vs HSTECH` | 首季对标恒科财富相对比 (WR_HSTECH) | 深蓝 | `numeric` | Aftermarket event horizon window | Adequate (28/45 (62.22%)) | 均值 0.94 / 中位数 0.77 / 区间 [0.31, 3.67] |
| **FX** | `3-month average daily turnover (HK$)` | 首季度日均成交金额 (港元) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 118,300,670.87 / 中位数 37,480,786.36 / 区间 [15,389,478.79, 1,861,466,041.94] |
| **FY** | `Amihud illiquidity (6M mean)` | 上市前6个月日均 Amihud (2002) 非流动性指标 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FZ** | `Zero-volume days count (first 6M)` | 上市前6个月零成交量交易日天数 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GA** | `Return volatility (first 6M daily std dev, %)` | 上市前6个月日度收益率标准差 (波动率, %) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GB** | `Maximum drawdown (first 6M, %)` | 上市前6个月二级市场最大回撤幅度 (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GC** | `Controlling shareholder 6-month disposal lockup expiry date` | 控股股东首阶段6个月绝对禁售期满日 | 深蓝 | `string` | Post-IPO lockup expiration events | 100% 完备 | 共 25 种取值 ('2026-12-26': 6, '2026-12-30': 4, '2026-11-27': 3) |
| **GD** | `Controlling shareholder 12-month cessation of control expiry date` | 控股股东次阶段12个月控制权锁定到期日 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 25 种取值 ('2027-06-26': 6, '2027-06-30': 4, '2027-05-27': 3) |
| **GE** | `Cornerstone unlock CAR [-5, +5] (%)` | 基石投资者解禁日前后[-5, +5]交易日累计超额收益 (CAR vs HSI) | 深蓝 | `numeric` | Post-IPO lockup expiration events | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GF** | `Cornerstone unlock CAR [-20, +20] (%)` | 基石投资者解禁日前后[-20, +20]交易日累计超额收益 (CAR vs HSI) | 深蓝 | `numeric` | Post-IPO lockup expiration events | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GG** | `Cornerstone unlock volume shock ratio` | 基石解禁后20日均换手额相对解禁前20日换手额之比 | 深蓝 | `numeric` | Post-IPO lockup expiration events | Reserved / Unmatured (0/45 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GH** | `Lead sponsor name` | 独家/联席牵头保荐人英文全称 | 深蓝 | `string` | Prospectus syndicate structure | 100% 完备 | 共 1 种取值 ('CICC': 45) |
| **GI** | `Joint sponsor count` | 保荐人总家数 (独家=1, 联席=2+) | 深蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 2.00 / 中位数 2.00 / 区间 [2.00, 2.00] |
| **GJ** | `Sponsor commercial bank affiliate flag` | 保荐人是否属于商业银行系金融机构 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus syndicate structure | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 45 家 |
| **GK** | `Underwriting base commission rate (%)` | 承销基础佣金费率 (%) | 深蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.03 / 中位数 0.03 / 区间 [0.03, 0.03] |
| **GL** | `Underwriting discretionary incentive fee rate (%)` | 承销酌情奖励费率估算 (%) | 深蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.01 / 中位数 0.01 / 区间 [0.01, 0.01] |
| **GM** | `Total underwriting fee rate (%)` | 承销总费率估算 (基础+奖励, %) | 深蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.04 / 中位数 0.04 / 区间 [0.04, 0.04] |
| **GN** | `Cornerstone investor count` | 基石投资者机构总家数 | 深蓝 | `numeric` | Prospectus / allotment institutional network | Sparse (8/45 (17.78%)) | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **GO** | `Cornerstone state-owned presence flag` | 基石投资者中是否包含国资/地方政府基金 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 45 家 |
| **GP** | `Crossover fund presence flag` | 是否包含兼具 Pre-IPO 与基石双重身份的跨界基金 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 45 家 |
| **GQ** | `Pre-IPO institutional investor count` | 主要 Pre-IPO 投资机构总数 | 深蓝 | `numeric` | Prospectus / allotment institutional network | 100% 完备 | 均值 6.00 / 中位数 6.00 / 区间 [6.00, 6.00] |
| **GR** | `Pre-IPO state-owned backing flag` | Pre-IPO 股东中是否包含国资机构 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 45 家 |
| **GS** | `FINI digital settlement regime` | 结算监管体制 (POST_FINI / PRE_FINI) | 深蓝 | `string` | Listing date regulatory regime | 100% 完备 | 共 1 种取值 ('POST_FINI': 45) |
| **GT** | `2025 pricing reform regime` | 发售与定价机制改革体制 (POST_2025_REFORM / PRE_2025_REFORM) | 深蓝 | `string` | Listing date regulatory regime | 100% 完备 | 共 1 种取值 ('POST_2025_REFORM': 45) |

---

## 三、计量软件导入指引 (Stata / Python)

配套清洗数据文件：`out/HKIPO-MB2026Q2_clean.csv`（编码：UTF-8 with BOM）。

### 1. Stata
```stata
* 导入纯净版 CSV 数据
import delimited "out/HKIPO-MB2026Q2_clean.csv", clear bindquote(strict) varnames(1)
describe
summarize
```

### 2. Python (pandas)
```python
import pandas as pd
df = pd.read_csv("out/HKIPO-MB2026Q2_clean.csv")
print(df.info())
print(df.describe())
```

---
*本数据代码本由 HK IPO Prospectus Pipeline 自动化分析引擎生成。*
