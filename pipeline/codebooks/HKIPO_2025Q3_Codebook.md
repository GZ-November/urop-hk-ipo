# 香港主板 2025 Q3 IPO 学术研究数据变量代码本 (Data Codebook)

- **样本规模 (N)**：24 家香港联交所 Main Board 新上市公司
- **变量总数 (K)**：202 维完整跨学科指标
- **数据层级划分**：浅绿官方基础 (11 列) + 浅蓝招股书披露 (77 列) + 深蓝配发及外部衍生 (114 列)
- **生成时间**：2026-11-12 23:23:44 | **数据基准**：`HKIPO-MB.xlsx` (Sheet: NLR)

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
| **A** | `HKEx file# of the year` | 港交所年度申请编号 | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 57.12 / 中位数 57.50 / 区间 [45.00, 69.00] |
| **B** | `Stock Code` | 股份代号（四位港股代码，如 6082.HK） | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 24 种取值 ('2592.HK': 1, '2648.HK': 1, '1828.HK': 1) |
| **C** | `Company Name at time of listing` | 公司上市时法定英文名称 | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 24 种取值 ('Cloudbreak Pharma Inc. - B': 1, 'Anjoy Foods Group Co., Ltd. - H shares': 1, 'FWD Group Holdings Limited': 1) |
| **D** | `Date of Prospectus (dd/mm/yy)` | 招股书刊发日期 | 浅绿 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-06-24 ~ 2025-09-22 |
| **E** | `Date of Listing (dd/mm/yy)` | 正式挂牌上市交易日期 | 浅绿 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-07-03 ~ 2025-09-30 |
| **F** | `Sponsor(s)` | 独家/联席保荐人名单 | 浅绿 | `string` | Prospectus syndicate structure | 100% 完备 | 共 21 种取值 ('China International Capital Corporation Hong Kong Securities Limited': 2, 'CITIC Securities (Hong Kong) Limited': 2, 'Morgan Stanley Asia Limited/ CITIC Securities (Hong Kong) Limited': 2) |
| **G** | `Reporting Accountants` | 申报会计师事务所 | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 5 种取值 ('Ernst & Young': 12, 'Deloitte Touche Tohmatsu': 6, 'PricewaterhouseCoopers': 3) |
| **H** | `Valuer(s)` | 独立物业或资产估值师 | 浅绿 | `string` | Ex-ante prospectus disclosure | Sparse (2/24 (8.33%)) | 共 2 种取值 ('Asia-Pacific Consulting and Appraisal Limited': 1, 'Jones Lang LaSalle Corporate Appraisal and Advisory Limited': 1) |
| **I** | `Funds Raised HK (a)` | 香港公开发售募资额 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 566,934,447.77 / 中位数 140,296,475.00 / 区间 [31,376,000.00, 2,498,426,569.00] |
| **J** | `Funds Raised Int.(b)` | 国际配售募资额 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 2,719,097,581.85 / 中位数 1,109,664,866.00 / 区间 [178,246,000.00, 26,233,453,918.00] |
| **K** | `IPO Subscription Price (HK$)` | 最终发售定价 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 43.72 / 中位数 25.00 / 区间 [10.10, 212.80] |
| **L** | `Total (without option)` | Total (without option) | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 947,998,846.25 / 中位数 369,391,615.00 / 区间 [31,667,841.00, 5,767,228,633.00] |
| **M** | `Global Offering (without option)` | Global Offering (without option) | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 83,001,125.00 / 中位数 38,275,550.00 / 区间 [7,920,000.00, 348,990,700.00] |
| **N** | `Number of offer shares under the capitalization Issue` | 全球发售完成前的已发行股份总数。本数据集口径：一律填 L − M（Total 减去全球发售股数），即使招股书未披露「资本化发行」也必须照填，不得留 NaN。用于满足恒等式 L = N + Q。2026Q1 成品工作簿 38 家公司全部取 L − M，Q2 必须同口径。数值只取权威 SHARE CAPITAL 汇总表与封面，禁止取「历史沿革／资本化发行沿革」段落。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (17/24 (70.83%)) | 均值 489,883,784.06 / 中位数 267,740,630.00 / 区间 [23,747,841.00, 2,275,000,000.00] |
| **O** | `Number of offer shares under Capitalization Rest` | 与 col_N 同口径：一律填 L − M（全球发售完成前的已发行股份总数），即使招股书未披露「资本化转换」也必须照填，不得留 NaN。用于满足恒等式 L = O + M。2026Q1 成品 38 家全部为 L − M。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (19/24 (79.17%)) | 均值 748,322,047.95 / 中位数 293,294,232.00 / 区间 [23,747,841.00, 5,469,831,633.00] |
| **P** | `Sale Shares` | 老股出售（Sale Shares）数量。若为全部新股的 Offer for Subscription（无 Selling Shareholder），填数字 0，不得留 NaN，用于满足恒等式 M = Q + P。判据：封面／股本汇总表无 Sale Shares 行，且全文无 Selling Shareholder 披露。2026Q1 成品 38 家全部为 0。若确有老股出售，按招股书披露填写。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **Q** | `New shares` | New shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 83,001,125.00 / 中位数 38,275,550.00 / 区间 [7,920,000.00, 348,990,700.00] |
| **R** | `Placing Shares` | Placing Shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 75,122,706.25 / 中位数 34,447,900.00 / 区间 [7,128,000.00, 314,091,600.00] |
| **S** | `Public Offer shares` | Public Offer shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 7,878,418.75 / 中位数 3,510,275.00 / 区间 [792,000.00, 34,899,100.00] |
| **T** | `Maximum Offer Price` | Maximum Offer Price | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 44.96 / 中位数 25.50 / 区间 [10.10, 228.00] |
| **U** | `Minimum Offer Price` | Minimum Offer Price | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (21/24 (87.5%)) | 均值 30.27 / 中位数 20.00 / 区间 [10.10, 102.23] |
| **V** | `Filing price revision (%)` | 发售定价偏离询价区间中点幅度（Hanley 1993 动态信息提取，固定价格发售为 0.00%） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 -0.00 / 中位数 0.00 / 区间 [-0.11, 0.07] |
| **W** | `Filing range width (%)` | 询价区间相对宽度（Beatty & Ritter 1986 事前估值不确定性，固定价格发售为 0.00%） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.05 / 中位数 0.00 / 区间 [0.00, 0.22] |
| **X** | `Pricing position in filing range` | 定价落点分类体系（Fixed price / Above range / At high / Midpoint / Within range / At low / Below range） | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 3 种取值 ('Fixed price': 14, 'At high': 6, 'At low': 4) |
| **Y** | `currency in financial information` | currency in financial information | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 3 种取值 ('RMB': 20, 'USD': 3, 'HKD': 1) |
| **Z** | `total assets in year-3 (3 years before IPO)` | total assets in year-3 (3 years before IPO) | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 15,965,475,791.67 / 中位数 2,137,192,500.00 / 区间 [82,087,000.00, 179,434,000,000.00] |
| **AA** | `total assets in year-2` | total assets in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 17,885,588,833.33 / 中位数 2,179,268,000.00 / 区间 [64,831,000.00, 213,996,000,000.00] |
| **AB** | `total assets in year-1` | total assets in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 18,199,592,708.33 / 中位数 2,473,974,500.00 / 区间 [40,009,000.00, 210,478,000,000.00] |
| **AC** | `total equity in year-3` | total equity in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 4,004,623,458.33 / 中位数 667,725,500.00 / 区间 [-4,327,815,000.00, 44,381,243,000.00] |
| **AD** | `total equity in year-2` | total equity in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 4,601,397,791.67 / 中位数 793,107,000.00 / 区间 [-5,443,066,000.00, 46,521,627,000.00] |
| **AE** | `total equity in year-1` | total equity in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 4,743,625,916.67 / 中位数 772,614,500.00 / 区间 [-6,248,799,000.00, 48,845,910,000.00] |
| **AF** | `total liability in year-3` | total liability in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 11,960,851,916.67 / 中位数 1,719,959,000.00 / 区间 [103,180,000.00, 164,853,000,000.00] |
| **AG** | `total liability in year-2` | total liability in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 13,284,191,041.67 / 中位数 1,960,829,000.00 / 区间 [102,570,000.00, 188,072,000,000.00] |
| **AH** | `total liability in year-1` | total liability in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 13,455,966,791.67 / 中位数 1,885,415,000.00 / 区间 [96,316,000.00, 184,683,000,000.00] |
| **AI** | `Net sales in year-3` | Net sales in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 11,072,919,708.33 / 中位数 830,923,000.00 / 区间 [0.00, 163,205,000,000.00] |
| **AJ** | `Net sales in year-2` | Net sales in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 16,325,483,083.33 / 中位数 1,082,252,500.00 / 区间 [0.00, 269,897,000,000.00] |
| **AK** | `Net sales in year-1` | Net sales in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 17,494,403,891.67 / 中位数 1,184,615,000.00 / 区间 [0.00, 272,892,000,000.00] |
| **AL** | `Profit before tax in year-3` | Profit before tax in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 714,853,500.00 / 中位数 -7,913,000.00 / 区间 [-1,564,054,000.00, 13,305,000,000.00] |
| **AM** | `Profit before tax in year-2` | Profit before tax in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 959,071,625.00 / 中位数 60,200,500.00 / 区间 [-1,122,519,000.00, 16,612,000,000.00] |
| **AN** | `Profit before tax in year-1` | Profit before tax in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 1,411,592,225.00 / 中位数 61,109,500.00 / 区间 [-827,281,000.00, 23,068,000,000.00] |
| **AO** | `Profit for the year in year-3` | Profit for the year in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 528,681,416.67 / 中位数 -9,248,000.00 / 区间 [-1,567,108,000.00, 10,444,000,000.00] |
| **AP** | `Profit for the year in year-2` | Profit for the year in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 796,056,916.67 / 中位数 50,823,500.00 / 区间 [-1,126,683,000.00, 14,334,000,000.00] |
| **AQ** | `Profit for the year in year-1` | Profit for the year in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 1,137,214,316.67 / 中位数 42,357,000.00 / 区间 [-831,501,000.00, 18,904,000,000.00] |
| **AR** | `Underwriting Commission (% of fund raised HK (a)` | Underwriting Commission (% of fund raised HK (a) | 浅蓝 | `numeric` | Prospectus syndicate structure | Adequate (19/24 (79.17%)) | 均值 0.03 / 中位数 0.03 / 区间 [0.01, 0.04] |
| **AS** | `Underwriting Commission (% of fund raised Int.(b)` | Underwriting Commission (% of fund raised Int.(b) | 浅蓝 | `numeric` | Prospectus syndicate structure | Adequate (19/24 (79.17%)) | 均值 0.03 / 中位数 0.03 / 区间 [0.01, 0.04] |
| **AT** | `Over-allotment Option (%)` | Over-allotment Option (%) | 浅蓝 | `numeric` | Post-IPO 30-day stabilization window | Adequate (20/24 (83.33%)) | 均值 0.14 / 中位数 0.15 / 区间 [0.00, 0.15] |
| **AU** | `Principal business / industry` | Principal business / industry | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 23 种取值 ('Biotechnology': 2, 'Research and developments of therapeutic biologics': 1, 'Production and sales of quick-frozen food products': 1) |
| **AV** | `Listing route / applicable chapter` | Listing route / applicable chapter | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 14 种取值 ('Main Board': 6, 'Chapter 18A': 4, 'Chapter 19A (A+H dual listing)': 2) |
| **AW** | `Year-1 financial period end (dd/mm/yy)` | Year-1 financial period end (dd/mm/yy) | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2024-12-31 ~ 2025-06-30 |
| **AX** | `Operating cash flow in year-1 (before annualization)` | Operating cash flow in year-1 (before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 806,120,833.33 / 中位数 56,077,500.00 / 区间 [-256,990,000.00, 10,888,841,000.00] |
| **AY** | `Cash and cash equivalents at year-1 end` | Cash and cash equivalents at year-1 end | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 2,712,488,458.33 / 中位数 411,071,000.00 / 区间 [5,911,000.00, 37,498,000,000.00] |
| **AZ** | `R&D expensed in year-1 (before annualization)` | R&D expensed in year-1 (before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (22/24 (91.67%)) | 均值 292,112,909.09 / 中位数 56,500,000.00 / 区间 [0.00, 2,784,813,000.00] |
| **BA** | `Development costs capitalized in year-1 (additions, before annualization)` | Development costs capitalized in year-1 (additions, before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (21/24 (87.5%)) | 均值 23,238,095.24 / 中位数 0.00 / 区间 [0.00, 488,000,000.00] |
| **BB** | `Top 5 customers (% of year-1 revenue)` | Top 5 customers (% of year-1 revenue) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (23/24 (95.83%)) | 均值 0.54 / 中位数 0.47 / 区间 [0.00, 1.00] |
| **BC** | `Comments / Annualization factor` | 最近一期财务数据对应的年化因子与口径说明 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (23/24 (95.83%)) | 均值 0.55 / 中位数 0.42 / 区间 [0.25, 1.00] |
| **BD** | `Pre-IPO VC/PE backing (1=yes; 0=no)` | 是否引入 Pre-IPO VC/PE 投资者：1=有，0=无。看 HISTORY AND DEVELOPMENT — Pre-IPO Investments 与 SUBSTANTIAL SHAREHOLDERS 名单；只要有专业投资机构（VC/PE/产业基金）在上市前入股即 1。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (23/24 (95.83%)) | 均值 0.83 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BE** | `Pre-IPO VC backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。早期/成长期专业风险投资基金为 1；未找到证据不等于 0，无法确认时填 NaN。分类依据须在本字段 quote 中体现。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (22/24 (91.67%)) | 均值 0.68 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BF** | `Pre-IPO PE backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。中晚期私募股权基金或并购基金为 1；未找到证据不等于 0，无法确认时填 NaN。分类依据须在本字段 quote 中体现。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (22/24 (91.67%)) | 均值 0.77 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BG** | `Pre-IPO CVC backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。发行人产业股东须有战略投资/企业风投关系依据才归 CVC；普通产业股东不能自动算 CVC。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (20/24 (83.33%)) | 均值 0.60 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BH** | `Pre-IPO State/Gov backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。有明确国资、政府或产业引导基金背景的机构为 1；国资身份不自动代表 VC/PE。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (19/24 (79.17%)) | 均值 0.68 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BI** | `Top-tier VC/PE backing (1=yes; 0=no)` | 仅在本公司招股书确认一线知名 VC/PE 机构持有重要股权或领投时填 1；不得仅凭机构知名度推断其参与本公司投资。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (20/24 (83.33%)) | 均值 0.60 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BJ** | `Key Pre-IPO investors` | 仅列本公司招股书披露的上市前投资者，采用一致的英文全称/拼音并以分号分隔；同一投资者只记一次，不从其他 cohort 补名单。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (23/24 (95.83%)) | 共 20 种取值 ('None': 4, 'Skketch Shine; Design Time; Gaotejia; Grand Diamond; Dyee Evergreen': 1, 'Shenzhen Xiushui Investment Co., Ltd.; Shenzhen Tongsheng Chuangye Investment Enterprise (Limited Partnership)': 1) |
| **BK** | `Pre-IPO institutional shareholding (%)` | 上市前 VC/PE/CVC/国资机构合计持股比例，取紧邻上市前的股权口径，不能混入 IPO 新股或基石配售；统一填 0–1 小数（如 12.5%=0.125）。只有招股书披露或可用披露数字复算时填写，否则 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (18/24 (75.0%)) | 均值 0.31 / 中位数 0.25 / 区间 [0.00, 0.80] |
| **BL** | `Pre-IPO investor board seat (1=yes; 0=no)` | 只有能从招股书明确关联到 Pre-IPO 投资机构的非执行董事或正式观察员席位才填 1；没有证据不等于 0，无法确认时填 NaN。 | 浅蓝 | `boolean` | Ex-ante prospectus disclosure | Adequate (21/24 (87.5%)) | 1 (是): 11 家 (52.4%), 0 (否): 10 家 |
| **BM** | `Earliest Pre-IPO investment round` | 从本公司招股书披露的 Pre-IPO 投资轮次中取最早一轮，保留披露的标准轮次名称；只有明确说明没有外部上市前投资时填 None，否则无法确认时 NA。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (23/24 (95.83%)) | 共 18 种取值 ('None': 4, 'Series A Financing': 2, 'Pre-IPO': 2) |
| **BN** | `Pre-IPO holding duration (years)` | 从最早 Pre-IPO 投资协议日期至本公司招股书日期计算年数，保留两位小数；起始日期无法确认则 NaN。每家公司必须使用自己的招股书日期，不沿用其他季度日期。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (16/24 (66.67%)) | 均值 9.52 / 中位数 9.48 / 区间 [2.67, 17.73] |
| **BO** | `Ultimate controller type` | 最终控制人类型（如：自然人 / 家族 / 国资委 / 地方政府 / 外资 / 无实际控制人）。取 SUBSTANTIAL SHAREHOLDERS 与 Controlling Shareholders 段的实际控制人身份表述。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 14 种取值 ('自然人': 7, 'Individual': 5, '自然人 (Dr. Jinsong Ni 与 Ms. Yiqing Leng 夫妇)': 1) |
| **BP** | `Controller economic interest at listing (%)` | 控制人上市时**经济权益**（持股比例），填小数。取 CONTROLLING/SUBSTANTIAL SHAREHOLDERS 表的持股百分比。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.40 / 中位数 0.33 / 区间 [0.08, 0.87] |
| **BQ** | `Controller voting rights at listing (%)` | 控制人上市时**投票权**比例，填小数。有 WVR（同股不同权）时与持股不同，取投票权那一列；无 WVR 通常与 BC 相同。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.46 / 中位数 0.38 / 区间 [0.16, 0.87] |
| **BR** | `Interest-bearing debt at year-1 end` | year-1 期末**总有息负债**（用与 col_V 相同的披露货币基本单位）。包含短期借款、长期借款、租赁负债及带息应付票据债券等带息债务总额，取 INDEBTEDNESS 表格的 Total 余额；不含应付账款等无息负债。必须换算为货币基本单位（乘表格千元/百万元乘数）。期末余额，不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 2,261,395,666.67 / 中位数 378,808,500.00 / 区间 [0.00, 23,916,000,000.00] |
| **BS** | `Technology commercialization stage` | 技术商业化阶段（如：研发阶段 / 小批量试产 / 商业化初期 / 规模商业化 / 已量产）。按 BUSINESS 与业务摘要里的产品状态表述填，不要按行业推测。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (22/24 (91.67%)) | 共 12 种取值 ('Commercialized': 6, 'Commercialized / mass production stage': 5, 'Clinical-stage': 2) |
| **BT** | `Debt repayment (% of planned net IPO proceeds)` | 计划净募资中用于**偿债**的比例，填小数。取 USE OF PROCEEDS 里用于偿还借款/债务的金额 ÷ 计划净募资额；没有该用途填 0。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (22/24 (91.67%)) | 均值 0.02 / 中位数 0.00 / 区间 [0.00, 0.25] |
| **BU** | `Listing board` | 上市板块（Main Board 主板） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Main Board': 24) |
| **BV** | `Share class` | 股份类别（如 H Shares / A Shares / Class A Ordinary Shares / Class B Ordinary Shares）。按招股书股本表的类别名称填。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 13 种取值 ('Ordinary shares': 4, 'H Shares': 4, 'Ordinary Shares': 3) |
| **BW** | `A+H issuer flag` | A+H 两地上市发行人标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 4 家 (16.7%), 0 (否): 20 家 |
| **BX** | `WVR flag` | 不同投票权/同股不同权架构标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 2 家 (8.3%), 0 (否): 22 家 |
| **BY** | `Chapter 18A flag` | 第 18A 章未盈利生物科技公司标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 4 家 (16.7%), 0 (否): 20 家 |
| **BZ** | `Chapter 18C flag` | 第 18C 章特专科技公司标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 24 家 |
| **CA** | `Industry classification code` | 恒生行业分类 HSICS 6 位业务细分代码 | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 355,357.50 / 中位数 281,020.00 / 区间 [51,010.00, 703,020.00] |
| **CB** | `Industry classification system and version` | 行业分类系统与版本号 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('HSICS (Hang Seng Industry Classification System) 2026': 24) |
| **CC** | `Incorporation date` | 公司**法定注册成立日期**（dd/mm/yy）。必须优先取自 Statutory and General Information (Appendix V '1. Incorporation')、History & Development 或 Accountants' Report (附注 1)。严禁从 Definitions (释义) 章节取值（释义章节常有起草笔误或仅为前期筹备日）。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | Adequate (22/24 (91.67%)) | 区间: 1997-01-08 ~ 2024-10-23 |
| **CD** | `Firm age at IPO (years)` | 公司成立至上市年限（Lowry et al. 2017 Table 3.4 基础控制变量） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (22/24 (91.67%)) | 均值 12.22 / 中位数 12.26 / 区间 [0.86, 28.71] |
| **CE** | `Place of incorporation` | 公司注册成立法域（如 Cayman Islands, PRC 等） | 深蓝 | `string` | Ex-ante prospectus disclosure | Adequate (23/24 (95.83%)) | 共 3 种取值 ('PRC': 16, 'Cayman Islands': 5, 'Hong Kong': 2) |
| **CF** | `Principal place of business` | 主要营业地点（城市/国家），如 PRC、Hong Kong、Shenzhen, PRC。取公司资料或注册办事处段。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (23/24 (95.83%)) | 共 20 种取值 ('PRC': 2, 'Hong Kong': 2, 'Shenzhen, Guangdong Province, PRC': 2) |
| **CG** | `Financial statement unit multiplier` | 财务报表基础货币乘数（千元/万元/百万元） | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (23/24 (95.83%)) | 均值 87,869.57 / 中位数 1,000.00 / 区间 [1,000.00, 1,000,000.00] |
| **CH** | `Accounting standard` | 财务报表采用的会计准则（如 IFRS Accounting Standards / HKFRS / ASBE / US GAAP）。取会计师报告开头声明。 | 浅蓝 | `string` | Track record period financial disclosure | Adequate (23/24 (95.83%)) | 共 5 种取值 ('IFRS': 12, 'IFRS Accounting Standards': 4, 'HKFRS Accounting Standards': 3) |
| **CI** | `Year-3 financial period start` | 往绩记录第三年前期起始日 | 浅蓝 | `date` | Track record period financial disclosure | Adequate (23/24 (95.83%)) | 区间: 2022-01-01 ~ 2023-01-01 |
| **CJ** | `Year-3 financial period end` | 往绩记录第三年前期截止日 | 浅蓝 | `date` | Track record period financial disclosure | Adequate (23/24 (95.83%)) | 区间: 2022-12-31 ~ 2023-12-31 |
| **CK** | `Year-2 financial period start` | 往绩记录第二年前期起始日 | 深蓝 | `date` | Track record period financial disclosure | Adequate (23/24 (95.83%)) | 区间: 2023-01-01 ~ 2024-01-01 |
| **CL** | `Year-2 financial period end` | 往绩记录第二年前期截止日 | 深蓝 | `date` | Track record period financial disclosure | Adequate (23/24 (95.83%)) | 区间: 2023-12-31 ~ 2024-12-31 |
| **CM** | `Year-1 financial period start` | 往绩记录最近一期起始日 | 深蓝 | `date` | Track record period financial disclosure | Adequate (23/24 (95.83%)) | 区间: 2024-01-01 ~ 2025-01-01 |
| **CN** | `Year-1 net sales (original, pre-annualization)` | 最近一期营业收入原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | Adequate (23/24 (95.83%)) | 均值 7,560,225,086.96 / 中位数 525,302,000.00 / 区间 [0.00, 69,896,776,000.00] |
| **CO** | `Year-1 profit before tax (original)` | 最近一期税前利润原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | Adequate (23/24 (95.83%)) | 均值 553,731,739.13 / 中位数 25,356,000.00 / 区间 [-827,281,000.00, 5,767,000,000.00] |
| **CP** | `Year-1 profit for period (original)` | 最近一期净利润原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | Adequate (23/24 (95.83%)) | 均值 457,815,086.96 / 中位数 21,528,000.00 / 区间 [-831,501,000.00, 4,726,000,000.00] |
| **CQ** | `Subscription opening date` | 香港公开发售**开始认购日期**（dd/mm/yy）。取 EXPECTED TIMETABLE。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-06-24 ~ 2025-09-22 |
| **CR** | `Subscription closing date` | 香港公开发售**截止认购日期**（dd/mm/yy）。取 EXPECTED TIMETABLE。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-06-27 ~ 2025-09-25 |
| **CS** | `H shares after IPO (base; no options)` | 上市后**在港交所挂牌的股份数**（base，不含超额配售）。统一口径：① 内地 H 股发行人全部转换时 = 总股本；② 部分转换时 = 由未上市股转换的 H 股 + 新发 H 股（剩余未上市股不挂牌，不计入）；③ A+H 发行人 = 仅新发 H 股（A 股在沪深市场挂牌，不计入）；④ 开曼/境外发行人没有 H 股类别，其全部股份均在港交所挂牌，故 = 上市后已发行股份总数。即：本列恒等于「港交所挂牌的股份数」，四类结构可比。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (20/24 (83.33%)) | 均值 465,118,976.80 / 中位数 142,496,995.50 / 区间 [7,920,000.00, 2,623,990,700.00] |
| **CT** | `Gross profit in year-1` | year-1 **毛利**（用与 col_V 相同的披露货币基本单位）。取损益表的 Gross profit。强制期间锚定：必须与 col_AT 严格同期间！若 col_AT 为中期报告期（如截至 2025 年 6 月 30 日或 9 月 30 日止期间），必须严格提取该中期报告期对应列的原值，绝对严禁错采前一完整财年（FY2024）的数值。必须换算为货币基本单位（乘表格千元/百万元乘数）。不年化——手册明确仅 year-1 销售/税前利润/净利润年化，毛利不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (23/24 (95.83%)) | 均值 1,208,718,956.52 / 中位数 152,340,000.00 / 区间 [-3,625,000.00, 10,183,493,000.00] |
| **CU** | `Capital expenditure in year-1` | year-1 **资本开支**（用与 col_V 相同的披露货币基本单位）。取现金流量表“购建物业、厂房及设备”或 CAPITAL EXPENDITURE 段。强制期间锚定：必须与 col_AT 严格同期间！若 col_AT 为中期报告期（如截至 2025 年 6 月 30 日或 9 月 30 日止期间），必须严格提取该中期报告期实际资本开支原值，绝对严禁错采前一完整财年（FY2024）数值。必须换算为货币基本单位（乘表格千元/百万元乘数）。不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 458,843,458.33 / 中位数 32,784,000.00 / 区间 [155,000.00, 6,356,054,000.00] |
| **CV** | `Audit opinion (year-1)` | year-1 **审计意见类型**（如 无保留意见 / Unqualified opinion / Qualified opinion）。取会计师报告的审计意见段。 | 浅蓝 | `string` | Track record period financial disclosure | Adequate (22/24 (91.67%)) | 共 5 种取值 ('Unqualified': 12, 'Unqualified opinion': 5, 'Unqualified opinion (true and fair view)': 2) |
| **CW** | `Listing expenses (HK$)` | **总上市费用**（HK$ 基本单位，含承销佣金与其他开支）。取 UNDERWRITING COMMISSIONS AND LISTING EXPENSES 段的合计。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (21/24 (87.5%)) | 均值 144,589,047.62 / 中位数 99,700,000.00 / 区间 [39,400,000.00, 517,600,000.00] |
| **CX** | `Cornerstone investor names` | Cornerstone investor names | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (21/24 (87.5%)) | 共 21 种取值 ('Wealth Strategy Holding Limited; The Reynold Lemkins Group (Asia) Limited': 1, 'Shanghai Greenwoods Asset Management Co., Ltd.; Huatai Capital Investment Limited; Greenwoods Asset Management Hong Kong Limited; HT Investment Limited; Torus Fund SP; FCP Domains Co., Ltd.; NonaVerse (Hong Kong) Limited': 1, 'MC Management 10 RSC Ltd; T&D United Capital Co., Ltd.': 1) |
| **CY** | `Final cornerstone allocation (% of base offer)` | Final cornerstone allocation (% of base offer) | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 0.28 / 中位数 0.29 / 区间 [0.00, 0.56] |
| **CZ** | `Earliest cornerstone unlock date (dd/mm/yy)` | 基石投资者最早解禁日期 | 深蓝 | `date` | Post-IPO lockup expiration events | Adequate (21/24 (87.5%)) | 区间: 2026-01-03 ~ 2026-03-30 |
| **DA** | `Subscription Ratio (times)` | Subscription Ratio (times) | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 1,716.16 / 中位数 543.50 / 区间 [12.79, 7,558.40] |
| **DB** | `Public applicants` | Public applicants | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 154,513.33 / 中位数 157,650.50 / 区间 [9,119.00, 350,775.00] |
| **DC** | `Public valid applied shares` | Public valid applied shares | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/24 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **DD** | `Public subscription original wording` | Public subscription original wording | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 24 种取值 ('Subscription level 78.78 times': 1, 'Subscription level 44.2 times': 1, 'Subscription level 37.13 times': 1) |
| **DE** | `Pricing date` | Pricing date | 深蓝 | `date` | Ex-ante prospectus disclosure | Adequate (13/24 (54.17%)) | 区间: 2025-07-02 ~ 2025-09-25 |
| **DF** | `Allotment announcement date` | Allotment announcement date | 深蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-07-02 ~ 2025-09-29 |
| **DG** | `Final global offering shares (before over-allotment)` | Final global offering shares (before over-allotment) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 86,066,533.33 / 中位数 38,428,600.00 / 区间 [7,920,000.00, 348,990,700.00] |
| **DH** | `Final public offer shares` | Final public offer shares | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 19,798,922.92 / 中位数 7,954,900.00 / 区间 [792,000.00, 118,015,600.00] |
| **DI** | `Final placing shares` | Final placing shares | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 66,267,610.42 / 中位数 30,657,725.00 / 区间 [7,128,000.00, 314,091,600.00] |
| **DJ** | `Over-allotment shares actually issued` | Over-allotment shares actually issued | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 8,872,125.00 / 中位数 1,966,300.00 / 区间 [0.00, 52,348,600.00] |
| **DK** | `Greenshoe exercise rate (%)` | 绿鞋实际行使比例（Ellis et al. 2000 超额配售执行度与价格支持） | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.47 / 中位数 0.18 / 区间 [0.00, 1.00] |
| **DL** | `Actual clawback / reallocation description` | Actual clawback / reallocation description | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 24 种取值 ('由国际发售回拨6,057,000股至香港公开发售；最终公开发售12,115,500股，占全球发售20%': 1, '由国际发售回拨7,999,000股至香港公开发售；最终公开发售11,998,500股，占全球发售30%': 1, '由国际发售回拨18,268,400股至香港公开发售；最终公开发售27,402,700股，占全球发售30%': 1) |
| **DM** | `Net IPO proceeds to issuer (HK$)` | Net IPO proceeds to issuer (HK$) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 2,802,465,416.67 / 中位数 1,133,500,000.00 / 区间 [178,170,000.00, 24,469,900,000.00] |
| **DN** | `Public shareholding at listing (%)` | Public shareholding at listing (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.30 / 中位数 0.25 / 区间 [0.05, 1.00] |
| **DO** | `Share base used for both public shareholding ratios` | Share base used for both public shareholding ratios | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 951,064,254.58 / 中位数 375,211,615.00 / 区间 [31,667,841.00, 5,767,228,633.00] |
| **DP** | `Unrestricted public shareholding at listing (%)` | Unrestricted public shareholding at listing (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.10 / 中位数 0.10 / 区间 [0.03, 0.22] |
| **DQ** | `Free float denominator description` | Free float denominator description | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Free float denominator = total issued shares upon listing (col_CZ); numerator = offer shares minus cornerstone allocation': 24) |
| **DR** | `Free float denominator shares` | Free float denominator shares | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 951,064,254.58 / 中位数 375,211,615.00 / 区间 [31,667,841.00, 5,767,228,633.00] |
| **DS** | `HSI return over 20 trading days before prospectus (%)` | 招股日前 20 个交易日恒生指数累计收益率 (%) | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 0.03 / 中位数 0.04 / 区间 [-0.00, 0.06] |
| **DT** | `HK ordinary IPO count in 90 calendar days before prospectus` | 招股日前 90 个自然日香港普通主板 IPO 上市数量 | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 27.58 / 中位数 28.50 / 区间 [21.00, 34.00] |
| **DU** | `1-month HIBOR before prospectus (%)` | 招股日前一交易日香港银行同业拆借 1 个月 HIBOR 利率 (%) | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.02 / 中位数 0.01 / 区间 [0.01, 0.03] |
| **DV** | `Banking system aggregate balance before prospectus (HK$)` | 招股日前一交易日香港银行体系总结余 (HK$) | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 96,355,041,666.67 / 中位数 59,061,500,000.00 / 区间 [53,716,000,000.00, 173,518,000,000.00] |
| **DW** | `First trading day closing price (HK$)` | 首日上市二级市场收盘价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 60.90 / 中位数 40.25 / 区间 [6.20, 234.00] |
| **DX** | `First-day return / Underpricing (%)` | 上市首日抑价率 / 初始收益率（Rock 1986 / Ritter 1984 核心被解释变量） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 0.56 / 中位数 0.15 / 区间 [-0.39, 2.58] |
| **DY** | `Money left on the table (HK$)` | 留在桌面上的财富 / 抑价转移财富总额（Loughran & Ritter 2002 前景理论指标） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 1,181,178,404.79 / 中位数 354,860,705.00 / 区间 [-236,269,800.00, 17,104,034,207.00] |
| **DZ** | `First trading day opening price (HK$)` | 首日上市二级市场开盘价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 59.70 / 中位数 41.00 / 区间 [9.50, 229.20] |
| **EA** | `First trading day high (HK$)` | 首日上市二级市场盘中最高价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 66.14 / 中位数 43.50 / 区间 [9.74, 244.00] |
| **EB** | `First trading day low (HK$)` | 首日上市二级市场盘中最低价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 55.90 / 中位数 39.52 / 区间 [5.60, 229.20] |
| **EC** | `First trading day volume (shares)` | 首日上市二级市场全天成交量（股） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 32,743,898.54 / 中位数 18,534,135.00 / 区间 [1,642,440.00, 140,581,771.00] |
| **ED** | `First-day flipping ratio (%)` | 首日短线翻转抛售率 / 成交量占全球发售比例（Aggarwal 2003 机构抛售假说） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 0.42 / 中位数 0.35 / 区间 [0.07, 1.04] |
| **EE** | `First trading day turnover (HK$)` | 首日上市二级市场全天成交金额 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 1,391,925,777.08 / 中位数 898,190,640.00 / 区间 [30,358,000.00, 11,211,450,560.00] |
| **EF** | `Offer mechanism` | 适用发售与回拨制度（2025-08-04 前 PN18/18C.09；之后 Mechanism A/B） | 深蓝 | `string` | Ex-ante prospectus disclosure | Adequate (18/24 (75.0%)) | 共 3 种取值 ('PN18 statutory clawback': 10, 'Mechanism B': 6, 'Mechanism A': 2) |
| **EG** | `Applicable IPO rules / transition basis` | 适用之上市规则过渡基准（FINI 改革规则） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 4 种取值 ('FINI (from 22/11/2023)': 10, 'FINI (from 22/11/2023); 2025-08-04 pricing reform (Mechanism A/B; six-month cornerstone lock-up retained)': 6, 'FINI (from 22/11/2023); 2025-08-04 pricing reform (Mechanism A/B; six-month cornerstone lock-up retained); this IPO: Mechanism B': 6) |
| **EH** | `Company Chinese Name` | Company Chinese Name | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 24 种取值 ('拨康视云制药有限公司': 1, '安井食品集团股份有限公司': 1, '富卫集团有限公司': 1) |
| **EI** | `Current listing status` | 当前挂牌存续状态 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 2 种取值 ('No recent trading (verify status)': 14, 'Active': 10) |
| **EJ** | `1-month post-IPO close price (HK$)` | 第20个交易日收盘价（窗口成熟后填报） | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 55.99 / 中位数 40.09 / 区间 [5.57, 180.60] |
| **EK** | `1-month BHR from Day-1 close (%)` | 由首日收盘至第20个交易日的买入持有收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.04 / 中位数 0.01 / 区间 [-0.30, 0.51] |
| **EL** | `1-month total return from offer price (%)` | 由发售价至第20个交易日的累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.68 / 中位数 0.28 / 区间 [-0.45, 4.42] |
| **EM** | `1-month HSI return (%)` | 同期恒生指数累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.02 / 中位数 0.03 / 区间 [-0.04, 0.06] |
| **EN** | `1-month HSTECH return (%)` | 同期恒生科技指数累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.03 / 中位数 0.05 / 区间 [-0.06, 0.12] |
| **EO** | `1-month wealth relative vs HSI` | 一个月相对恒指财富比 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 1.02 / 中位数 0.98 / 区间 [0.68, 1.55] |
| **EP** | `1-month wealth relative vs HSTECH` | 一个月相对恒生科技指数财富比 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 1.02 / 中位数 0.97 / 区间 [0.67, 1.62] |
| **EQ** | `1-month average daily turnover (HK$)` | 上市后首20个交易日日均成交额 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 212,220,573.44 / 中位数 96,731,344.25 / 区间 [5,090,065.00, 2,206,158,578.00] |
| **ER** | `6-month post-IPO close price (HK$)` | 六个月目标日后首个交易日收盘价（窗口成熟后填报） | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 56.52 / 中位数 33.34 / 区间 [3.65, 175.00] |
| **ES** | `6-month BHR from Day-1 close (%)` | 由首日收盘至六个月目标交易日的买入持有收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.24 / 中位数 -0.09 / 区间 [-0.52, 4.35] |
| **ET** | `6-month total return from offer price (%)` | 由发售价至六个月目标交易日的累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 1.26 / 中位数 0.13 / 区间 [-0.64, 11.70] |
| **EU** | `6-month HSI return (%)` | 同期恒生指数累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.03 / 中位数 0.05 / 区间 [-0.08, 0.11] |
| **EV** | `6-month HSTECH return (%)` | 同期恒生科技指数累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 -0.07 / 中位数 -0.09 / 区间 [-0.27, 0.10] |
| **EW** | `6-month wealth relative vs HSI` | 六个月相对恒指财富比 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 1.22 / 中位数 0.87 / 区间 [0.45, 5.57] |
| **EX** | `6-month wealth relative vs HSTECH` | 六个月相对恒生科技指数财富比 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 1.39 / 中位数 0.94 / 区间 [0.45, 6.64] |
| **EY** | `6-month average daily turnover (HK$)` | 六个月目标日前20个交易日日均成交额 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 124,645,312.15 / 中位数 29,941,807.75 / 区间 [69,795.50, 1,294,062,871.00] |
| **EZ** | `Liquidity decay ratio (6M vs Day-1 turnover)` | 六个月窗口日均成交额相对首日成交额比率 | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.09 / 中位数 0.05 / 区间 [0.00, 0.63] |
| **FA** | `1-year post-IPO return (%) [Reserved]` | 一年期收益率预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/24 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FB** | `1-year wealth relative vs HSI [Reserved]` | 一年期相对恒指财富比预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/24 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FC** | `3-year post-IPO return (%) [Reserved]` | 三年期收益率预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/24 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FD** | `3-year wealth relative vs HSI [Reserved]` | 三年期相对恒指财富比预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/24 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FE** | `18A/18C regulatory milestone status` | 18A/18C 监管路径与商业化里程碑状态 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 2 种取值 ('Standard': 20, '18A (Biotech / B-tag)': 4) |
| **FF** | `Stabilizing manager` | 官方指定价格稳定经理人名称 | 深蓝 | `string` | Ex-ante prospectus disclosure | Adequate (15/24 (62.5%)) | 共 6 种取值 ('China International Capital Corporation Hong Kong Securities Limited': 6, 'Morgan Stanley Asia Limited': 3, 'CLSA Limited': 3) |
| **FG** | `Stabilization period end date` | 法定30天稳价期结束日期 | 深蓝 | `string` | Post-IPO 30-day stabilization window | Sparse (8/24 (33.33%)) | 共 7 种取值 ('2025-08-03': 2, '2025-08-01': 1, '2025-09-14': 1) |
| **FH** | `Stabilization purchases occurred` | 稳价期内是否发生二级市场托单购买 (1=是, 0=否) | 深蓝 | `boolean` | Post-IPO 30-day stabilization window | Sparse (3/24 (12.5%)) | 1 (是): 0 家 (0.0%), 0 (否): 3 家 |
| **FI** | `Over-allocation shares` | 国际配售超额配售股份数量（股） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Sparse (8/24 (33.33%)) | 均值 19,046,412.50 / 中位数 13,543,650.00 / 区间 [1,180,000.00, 44,609,500.00] |
| **FJ** | `Over-allocation (% of base offer)` | 超额配售股数占基础发售股份比例 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Sparse (11/24 (45.83%)) | 均值 0.15 / 中位数 0.15 / 区间 [0.05, 0.30] |
| **FK** | `Over-allotment option exercise date` | 超额配售权实际行使公告日期 | 深蓝 | `string` | Post-IPO 30-day stabilization window | 100% 完备 | 共 19 种取值 ('2025-06-30': 5, '2025-09-19': 2, '2025-06-24': 1) |
| **FL** | `Shares issued under over-allotment option` | 超额配售权最终发行股份数量（股） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Adequate (19/24 (79.17%)) | 均值 11,603,789.47 / 中位数 5,001,400.00 / 区间 [0.00, 52,348,600.00] |
| **FM** | `Over-allotment exercise percentage (%)` | 超额配售权行使比例 (行使股数/超额配售上限, %) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Adequate (20/24 (83.33%)) | 均值 0.66 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **FN** | `Post-stabilization cliff return [-5, +5] (%)` | 稳价期结束日前后[-5, +5]交易日累计收益率（断崖效应测试） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Sparse (8/24 (33.33%)) | 均值 0.00 / 中位数 0.02 / 区间 [-0.19, 0.32] |
| **FO** | `Post-stabilization 20-day return [0, +20] (%)` | 稳价期结束后20个交易日累计收益率 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Sparse (8/24 (33.33%)) | 均值 0.10 / 中位数 0.09 / 区间 [-0.15, 0.44] |
| **FP** | `Post-stabilization volume decay ratio (%)` | 稳价结束后20日均成交额相对稳价期内之比 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Sparse (8/24 (33.33%)) | 均值 0.46 / 中位数 0.33 / 区间 [0.09, 1.21] |
| **FQ** | `Day-5 BHR from Day-1 close (%)` | 挂牌首周 (T+5交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 0.06 / 中位数 -0.00 / 区间 [-0.17, 0.58] |
| **FR** | `Day-5 wealth relative vs HSI` | 挂牌首周对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 1.05 / 中位数 0.99 / 区间 [0.81, 1.58] |
| **FS** | `Day-20 BHR from Day-1 close (%)` | 首月 (T+20交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 0.04 / 中位数 0.01 / 区间 [-0.30, 0.51] |
| **FT** | `Day-20 wealth relative vs HSI` | 首月对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 1.02 / 中位数 0.98 / 区间 [0.68, 1.55] |
| **FU** | `3-month BHR from Day-1 close (%)` | 首季 (T+63交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 0.11 / 中位数 0.10 / 区间 [-0.41, 0.84] |
| **FV** | `3-month wealth relative vs HSI` | 首季对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 1.07 / 中位数 1.03 / 区间 [0.53, 1.94] |
| **FW** | `3-month wealth relative vs HSTECH` | 首季对标恒科财富相对比 (WR_HSTECH) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 1.08 / 中位数 1.11 / 区间 [0.48, 2.13] |
| **FX** | `3-month average daily turnover (HK$)` | 首季度日均成交金额 (港元) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 120,488,774.90 / 中位数 51,993,365.65 / 区间 [2,825,911.85, 1,147,372,224.92] |
| **FY** | `Amihud illiquidity (6M mean)` | 上市前6个月日均 Amihud (2002) 非流动性指标 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.02 / 中位数 0.00 / 区间 [0.00, 0.36] |
| **FZ** | `Zero-volume days count (first 6M)` | 上市前6个月零成交量交易日天数 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.33 / 中位数 0.00 / 区间 [0.00, 7.00] |
| **GA** | `Return volatility (first 6M daily std dev, %)` | 上市前6个月日度收益率标准差 (波动率, %) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.08 / 中位数 0.06 / 区间 [0.02, 0.24] |
| **GB** | `Maximum drawdown (first 6M, %)` | 上市前6个月二级市场最大回撤幅度 (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.44 / 中位数 0.42 / 区间 [0.16, 0.65] |
| **GC** | `Controlling shareholder 6-month disposal lockup expiry date` | 控股股东首阶段6个月绝对禁售期满日 | 深蓝 | `string` | Post-IPO lockup expiration events | Reserved / Unmatured (0/24 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GD** | `Controlling shareholder 12-month cessation of control expiry date` | 控股股东次阶段12个月控制权锁定到期日 | 深蓝 | `string` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/24 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GE** | `Cornerstone unlock CAR [-5, +5] (%)` | 基石投资者解禁日前后[-5, +5]交易日累计超额收益 (CAR vs HSI) | 深蓝 | `numeric` | Post-IPO lockup expiration events | Reserved / Unmatured (0/24 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GF** | `Cornerstone unlock CAR [-20, +20] (%)` | 基石投资者解禁日前后[-20, +20]交易日累计超额收益 (CAR vs HSI) | 深蓝 | `numeric` | Post-IPO lockup expiration events | Reserved / Unmatured (0/24 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GG** | `Cornerstone unlock volume shock ratio` | 基石解禁后20日均换手额相对解禁前20日换手额之比 | 深蓝 | `numeric` | Post-IPO lockup expiration events | Reserved / Unmatured (0/24 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GH** | `Lead sponsor name` | 独家/联席牵头保荐人英文全称 | 深蓝 | `string` | Prospectus syndicate structure | 100% 完备 | 共 10 种取值 ('China International Capital Corporation Hong Kong Securities Limited': 8, 'CITIC Securities (Hong Kong) Limited': 5, 'Morgan Stanley Asia Limited': 4) |
| **GI** | `Joint sponsor count` | 保荐人总家数 (独家=1, 联席=2+) | 深蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 1.88 / 中位数 2.00 / 区间 [1.00, 5.00] |
| **GJ** | `Sponsor commercial bank affiliate flag` | 保荐人是否属于商业银行系金融机构 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus syndicate structure | 100% 完备 | 1 (是): 6 家 (25.0%), 0 (否): 18 家 |
| **GK** | `Underwriting base commission rate (%)` | 承销基础佣金费率 (%) | 深蓝 | `numeric` | Prospectus syndicate structure | Adequate (19/24 (79.17%)) | 均值 0.03 / 中位数 0.03 / 区间 [0.01, 0.04] |
| **GL** | `Underwriting discretionary incentive fee rate (%)` | 招股书披露的酌情奖励费率上限（非实际支付，%） | 深蓝 | `numeric` | Prospectus syndicate structure | Reserved / Unmatured (0/24 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GM** | `Total underwriting fee rate (%)` | 披露的承销总费率上限（基础+奖励上限，非实际支付，%） | 深蓝 | `numeric` | Prospectus syndicate structure | Reserved / Unmatured (0/24 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GN** | `Cornerstone investor count` | 基石投资者机构总家数 | 深蓝 | `numeric` | Prospectus / allotment institutional network | 100% 完备 | 均值 7.21 / 中位数 4.00 / 区间 [0.00, 29.00] |
| **GO** | `Cornerstone state-owned presence flag` | 基石投资者中是否包含国资/地方政府基金 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | 100% 完备 | 1 (是): 16 家 (66.7%), 0 (否): 8 家 |
| **GP** | `Crossover fund presence flag` | 是否包含兼具 Pre-IPO 与基石双重身份的跨界基金 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 24 家 |
| **GQ** | `Pre-IPO institutional investor count` | 主要 Pre-IPO 投资机构总数 | 深蓝 | `numeric` | Prospectus / allotment institutional network | 100% 完备 | 均值 7.58 / 中位数 5.50 / 区间 [0.00, 37.00] |
| **GR** | `Pre-IPO state-owned backing flag` | Pre-IPO 股东中是否包含国资机构 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | 100% 完备 | 1 (是): 16 家 (66.7%), 0 (否): 8 家 |
| **GS** | `FINI digital settlement regime` | 结算监管体制 (POST_FINI / PRE_FINI) | 深蓝 | `string` | Listing date regulatory regime | 100% 完备 | 共 1 种取值 ('POST_FINI': 24) |
| **GT** | `2025 pricing reform regime` | 发售与定价机制改革体制 (POST_2025_REFORM / PRE_2025_REFORM) | 深蓝 | `string` | Listing date regulatory regime | 100% 完备 | 共 2 种取值 ('POST_2025_REFORM': 15, 'PRE_2025_REFORM': 9) |

---

## 三、计量软件导入指引 (Stata / Python)

配套清洗数据文件：`out/HKIPO-MB2025Q3_clean.csv`（编码：UTF-8 with BOM）。

### 1. Stata
```stata
* 导入纯净版 CSV 数据
import delimited "out/HKIPO-MB2025Q3_clean.csv", clear bindquote(strict) varnames(1)
describe
summarize
```

### 2. Python (pandas)
```python
import pandas as pd
df = pd.read_csv("out/HKIPO-MB2025Q3_clean.csv")
print(df.info())
print(df.describe())
```

---
*本数据代码本由 HK IPO Prospectus Pipeline 自动化分析引擎生成。*
