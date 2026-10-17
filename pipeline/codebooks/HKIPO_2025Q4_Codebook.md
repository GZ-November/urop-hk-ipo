# 香港主板 2025 Q4 IPO 学术研究数据变量代码本 (Data Codebook)

- **样本规模 (N)**：47 家香港联交所 Main Board 新上市公司
- **变量总数 (K)**：202 维完整跨学科指标
- **数据层级划分**：浅绿官方基础 (11 列) + 浅蓝招股书披露 (77 列) + 深蓝配发及外部衍生 (114 列)
- **生成时间**：2026-10-17 09:53:38 | **数据基准**：`HKIPO-MB2025Q4.xlsx` (Sheet: NLR)

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
| **A** | `HKEx file# of the year` | 港交所年度申请编号 | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 94.13 / 中位数 94.00 / 区间 [70.00, 118.00] |
| **B** | `Stock Code` | 股份代号（四位港股代码，如 6082.HK） | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 47 种取值 ('2652.HK': 1, '2650.HK': 1, '2575.HK': 1) |
| **C** | `Company Name at time of listing` | 公司上市时法定英文名称 | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 47 种取值 ('CF PharmTech, Inc. - H shares': 1, 'Shanghai Zhida Technology Development Co., Ltd. - H shares': 1, 'Xuanzhu Biopharmaceutical Co., Ltd. - B - H shares': 1) |
| **D** | `Date of Prospectus (dd/mm/yy)` | 招股书刊发日期 | 浅绿 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-09-26 ~ 2025-12-18 |
| **E** | `Date of Listing (dd/mm/yy)` | 正式挂牌上市交易日期 | 浅绿 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-10-08 ~ 2025-12-30 |
| **F** | `Sponsor(s)` | 独家/联席保荐人名单 | 浅绿 | `string` | Prospectus syndicate structure | 100% 完备 | 共 39 种取值 ('CITIC Securities (Hong Kong) Limited': 5, 'China International Capital Corporation Hong Kong Securities Limited': 3, 'Shenwan Hongyuan Capital (H.K.) Limited': 2) |
| **G** | `Reporting Accountants` | 申报会计师事务所 | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 8 种取值 ('Ernst & Young': 14, 'KPMG': 12, 'Deloitte Touche Tohmatsu': 11) |
| **H** | `Valuer(s)` | 独立物业或资产估值师 | 浅绿 | `string` | Ex-ante prospectus disclosure | Sparse (7/47 (14.89%)) | 共 4 种取值 ('AVISTA Valuation Advisory Limited': 3, 'Cushman & Wakefield Limited': 2, 'Asia-Pacific Consulting and Appraisal Limited': 1) |
| **I** | `Funds Raised HK (a)` | 香港公开发售募资额 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 204,728,674.84 / 中位数 108,000,000.00 / 区间 [12,996,000.00, 1,428,339,850.00] |
| **J** | `Funds Raised Int.(b)` | 国际配售募资额 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 1,892,507,675.97 / 中位数 894,240,000.00 / 区间 [116,964,000.00, 14,112,779,340.00] |
| **K** | `IPO Subscription Price (HK$)` | 最终发售定价 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 46.24 / 中位数 27.10 / 区间 [3.60, 263.00] |
| **L** | `Total (without option)` | Total (without option) | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 709,866,649.43 / 中位数 326,632,000.00 / 区间 [37,866,600.00, 9,054,814,637.00] |
| **M** | `Global Offering (without option)` | Global Offering (without option) | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 74,080,290.00 / 中位数 30,831,400.00 / 区间 [3,786,600.00, 580,424,600.00] |
| **N** | `Number of offer shares under the capitalization Issue` | 全球发售完成前的已发行股份总数。本数据集口径：一律填 L − M（Total 减去全球发售股数），即使招股书未披露「资本化发行」也必须照填，不得留 NaN。用于满足恒等式 L = N + Q。2026Q1 成品工作簿 38 家公司全部取 L − M，Q2 必须同口径。数值只取权威 SHARE CAPITAL 汇总表与封面，禁止取「历史沿革／资本化发行沿革」段落。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 635,786,359.43 / 中位数 300,000,000.00 / 区间 [34,080,000.00, 8,474,390,037.00] |
| **O** | `Number of offer shares under Capitalization Rest` | 与 col_N 同口径：一律填 L − M（全球发售完成前的已发行股份总数），即使招股书未披露「资本化转换」也必须照填，不得留 NaN。用于满足恒等式 L = O + M。2026Q1 成品 38 家全部为 L − M。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 635,786,359.43 / 中位数 300,000,000.00 / 区间 [34,080,000.00, 8,474,390,037.00] |
| **P** | `Sale Shares` | 老股出售（Sale Shares）数量。若为全部新股的 Offer for Subscription（无 Selling Shareholder），填数字 0，不得留 NaN，用于满足恒等式 M = Q + P。判据：封面／股本汇总表无 Sale Shares 行，且全文无 Selling Shareholder 披露。2026Q1 成品 38 家全部为 0。若确有老股出售，按招股书披露填写。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **Q** | `New shares` | New shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 74,080,290.00 / 中位数 30,831,400.00 / 区间 [3,786,600.00, 580,424,600.00] |
| **R** | `Placing Shares` | Placing Shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 66,833,003.40 / 中位数 27,748,200.00 / 区间 [3,407,900.00, 522,382,000.00] |
| **S** | `Public Offer shares` | Public Offer shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 7,247,286.60 / 中位数 3,083,200.00 / 区间 [270,400.00, 58,042,600.00] |
| **T** | `Maximum Offer Price` | Maximum Offer Price | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 49.30 / 中位数 30.50 / 区间 [4.10, 263.00] |
| **U** | `Minimum Offer Price` | Minimum Offer Price | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (41/47 (87.23%)) | 均值 39.08 / 中位数 26.38 / 区间 [3.47, 263.00] |
| **V** | `Filing price revision (%)` | 发售定价偏离询价区间中点幅度（Hanley 1993 动态信息提取，固定价格发售为 0.00%） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 -0.00 / 中位数 0.00 / 区间 [-0.14, 0.19] |
| **W** | `Filing range width (%)` | 询价区间相对宽度（Beatty & Ritter 1986 事前估值不确定性，固定价格发售为 0.00%） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.09 / 中位数 0.06 / 区间 [0.00, 0.39] |
| **X** | `Pricing position in filing range` | 定价落点分类体系（Fixed price / Above range / At high / Midpoint / Within range / At low / Below range） | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 5 种取值 ('Fixed price': 22, 'At high': 11, 'At low': 8) |
| **Y** | `currency in financial information` | currency in financial information | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 4 种取值 ('RMB': 43, 'USD': 2, 'US$': 1) |
| **Z** | `total assets in year-3 (3 years before IPO)` | total assets in year-3 (3 years before IPO) | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 9,559,699,957.45 / 中位数 973,880,000.00 / 区间 [202,795,000.00, 151,203,358,000.00] |
| **AA** | `total assets in year-2` | total assets in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 11,336,096,617.02 / 中位数 1,196,619,000.00 / 区间 [144,002,000.00, 152,145,076,000.00] |
| **AB** | `total assets in year-1` | total assets in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 11,953,500,680.85 / 中位数 1,247,980,000.00 / 区间 [127,956,000.00, 153,897,737,000.00] |
| **AC** | `total equity in year-3` | total equity in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 2,913,277,489.36 / 中位数 398,267,000.00 / 区间 [-6,426,455,000.00, 69,162,033,000.00] |
| **AD** | `total equity in year-2` | total equity in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 3,328,089,829.79 / 中位数 498,869,000.00 / 区间 [-6,399,964,000.00, 73,001,599,000.00] |
| **AE** | `total equity in year-1` | total equity in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 3,732,902,893.62 / 中位数 631,536,000.00 / 区间 [-6,566,365,000.00, 76,101,875,000.00] |
| **AF** | `total liability in year-3` | total liability in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 6,646,422,468.09 / 中位数 852,953,000.00 / 区间 [51,944,000.00, 82,041,325,000.00] |
| **AG** | `total liability in year-2` | total liability in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 8,008,006,787.23 / 中位数 807,925,000.00 / 区间 [40,077,000.00, 82,458,401,000.00] |
| **AH** | `total liability in year-1` | total liability in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 8,220,597,787.23 / 中位数 922,675,000.00 / 区间 [43,420,000.00, 85,902,076,000.00] |
| **AI** | `Net sales in year-3` | Net sales in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 5,566,771,106.38 / 中位数 529,669,000.00 / 区间 [0.00, 74,018,936,000.00] |
| **AJ** | `Net sales in year-2` | Net sales in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 8,316,365,234.04 / 中位数 631,978,000.00 / 区间 [0.00, 145,113,623,000.00] |
| **AK** | `Net sales in year-1` | Net sales in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 8,416,714,617.02 / 中位数 792,588,000.00 / 区间 [0.00, 124,717,650,000.00] |
| **AL** | `Profit before tax in year-3` | Profit before tax in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 83,226,255.32 / 中位数 57,138,000.00 / 区间 [-4,080,859,000.00, 5,316,554,000.00] |
| **AM** | `Profit before tax in year-2` | Profit before tax in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 246,804,425.53 / 中位数 58,916,000.00 / 区间 [-2,510,940,000.00, 6,907,770,000.00] |
| **AN** | `Profit before tax in year-1` | Profit before tax in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 502,527,202.83 / 中位数 48,252,000.00 / 区间 [-1,579,280,000.00, 12,143,751,000.00] |
| **AO** | `Profit for the year in year-3` | Profit for the year in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 39,752,723.40 / 中位数 43,617,000.00 / 区间 [-4,156,716,000.00, 4,606,110,000.00] |
| **AP** | `Profit for the year in year-2` | Profit for the year in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 199,350,829.79 / 中位数 49,119,000.00 / 区间 [-2,516,808,000.00, 6,092,538,000.00] |
| **AQ** | `Profit for the year in year-1` | Profit for the year in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 401,916,687.94 / 中位数 51,260,000.00 / 区间 [-1,583,034,000.00, 10,426,887,000.00] |
| **AR** | `Underwriting Commission (% of fund raised HK (a)` | Underwriting Commission (% of fund raised HK (a) | 浅蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.03 / 中位数 0.03 / 区间 [0.01, 0.05] |
| **AS** | `Underwriting Commission (% of fund raised Int.(b)` | Underwriting Commission (% of fund raised Int.(b) | 浅蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.03 / 中位数 0.03 / 区间 [0.01, 0.05] |
| **AT** | `Over-allotment Option (%)` | Over-allotment Option (%) | 浅蓝 | `numeric` | Post-IPO 30-day stabilization window | Adequate (42/47 (89.36%)) | 均值 0.13 / 中位数 0.15 / 区间 [0.00, 0.15] |
| **AU** | `Principal business / industry` | Principal business / industry | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 47 种取值 ('R&D, manufacturing and commercialization of inhalation technologies and inhalation drugs for respiratory diseases': 1, 'EV home charging solutions: smart home EV chargers and accessories, installation and after-sales services, and a digital home energy management platform': 1, 'R&D, manufacturing and commercialization of innovative drugs (biopharmaceutical)': 1) |
| **AV** | `Listing route / applicable chapter` | Listing route / applicable chapter | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 42 种取值 ('Main Board, Rule 8.05(3) market capitalisation/revenue test': 3, 'Main Board': 2, 'Main Board of the Stock Exchange': 2) |
| **AW** | `Year-1 financial period end (dd/mm/yy)` | Year-1 financial period end (dd/mm/yy) | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2024-12-31 ~ 2025-09-30 |
| **AX** | `Operating cash flow in year-1 (before annualization)` | Operating cash flow in year-1 (before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 453,918,042.55 / 中位数 -6,851,000.00 / 区间 [-663,396,000.00, 14,034,486,000.00] |
| **AY** | `Cash and cash equivalents at year-1 end` | Cash and cash equivalents at year-1 end | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 1,364,845,638.30 / 中位数 197,065,000.00 / 区间 [8,558,000.00, 21,664,886,000.00] |
| **AZ** | `R&D expensed in year-1 (before annualization)` | R&D expensed in year-1 (before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (41/47 (87.23%)) | 均值 230,858,195.12 / 中位数 58,679,000.00 / 区间 [257,000.00, 2,929,532,000.00] |
| **BA** | `Development costs capitalized in year-1 (additions, before annualization)` | Development costs capitalized in year-1 (additions, before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (31/47 (65.96%)) | 均值 92,404,677.42 / 中位数 0.00 / 区间 [0.00, 2,260,956,000.00] |
| **BB** | `Top 5 customers (% of year-1 revenue)` | Top 5 customers (% of year-1 revenue) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (45/47 (95.74%)) | 均值 0.43 / 中位数 0.42 / 区间 [0.01, 0.99] |
| **BC** | `Comments / Annualization factor` | 最近一期财务数据对应的年化因子与口径说明 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 0.49 / 中位数 0.50 / 区间 [0.25, 1.00] |
| **BD** | `Pre-IPO VC/PE backing (1=yes; 0=no)` | 是否引入 Pre-IPO VC/PE 投资者：1=有，0=无。看 HISTORY AND DEVELOPMENT — Pre-IPO Investments 与 SUBSTANTIAL SHAREHOLDERS 名单；只要有专业投资机构（VC/PE/产业基金）在上市前入股即 1。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (39/47 (82.98%)) | 均值 1.00 / 中位数 1.00 / 区间 [1.00, 1.00] |
| **BE** | `Pre-IPO VC backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。早期/成长期专业风险投资基金为 1；未找到证据不等于 0，无法确认时填 NaN。分类依据须在本字段 quote 中体现。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (34/47 (72.34%)) | 均值 1.00 / 中位数 1.00 / 区间 [1.00, 1.00] |
| **BF** | `Pre-IPO PE backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。中晚期私募股权基金或并购基金为 1；未找到证据不等于 0，无法确认时填 NaN。分类依据须在本字段 quote 中体现。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (34/47 (72.34%)) | 均值 1.00 / 中位数 1.00 / 区间 [1.00, 1.00] |
| **BG** | `Pre-IPO CVC backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。发行人产业股东须有战略投资/企业风投关系依据才归 CVC；普通产业股东不能自动算 CVC。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Sparse (22/47 (46.81%)) | 均值 1.00 / 中位数 1.00 / 区间 [1.00, 1.00] |
| **BH** | `Pre-IPO State/Gov backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。有明确国资、政府或产业引导基金背景的机构为 1；国资身份不自动代表 VC/PE。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (26/47 (55.32%)) | 均值 1.00 / 中位数 1.00 / 区间 [1.00, 1.00] |
| **BI** | `Top-tier VC/PE backing (1=yes; 0=no)` | 仅在本公司招股书确认一线知名 VC/PE 机构持有重要股权或领投时填 1；不得仅凭机构知名度推断其参与本公司投资。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Sparse (12/47 (25.53%)) | 均值 1.00 / 中位数 1.00 / 区间 [1.00, 1.00] |
| **BJ** | `Key Pre-IPO investors` | 仅列本公司招股书披露的上市前投资者，采用一致的英文全称/拼音并以分号分隔；同一投资者只记一次，不从其他 cohort 补名单。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (40/47 (85.11%)) | 共 40 种取值 ('FIIF; China-Singapore Ventures; Jiequan Oriza; Shanghai Sihongda; SL Pharmaceutical; Jiangsu CMB; Nanjing CMB; Lianyi Investment; Shenzhen GTJA; Jiangsu GTJA; CICC Generation Fund; Meimin Investment; GP Healthcare Capital Phase I; Longmen Changfeng; CICC Biomedical Fund; Yuanming Capital; Unique Classic Limited; Longmen No. 1; Longmen Yusen; CCBI Investment; Yantai Duoying; Qingdao Finnova; Shanghai Hanren; Changzhou Longcheng; Ningbo Yuanchuan; Guangzhou Yongping; Changzhou Yongjun; Cornerstone Fund; Jinpu Merger Fund; Shanghai Jianli; Mengxi Venture; Tianjin Yuanyi; Langma No. 18; Langma No. 17; Boyuan Venture; Yangtze River Delta Fund; Changzhou Feijun; Guangzhou Feijun; Qianhai Kangda; Wosheng Huijia; Taichu Investment; Yangzhou Tenglan; Changzhou Tengren; Wuxi Lejin; Xinfei Dingke; Xinding Kenge; Suzhou Yueliang; Shengyuan Investment; Ms. CHEN Xiangyun; Xinxing Venture; Zhiyuan Investment; Suzhou Wosheng; Shenzhen Gongying; Mr. MI Jinyong; Mr. GENG Shaofeng': 1, 'Anhui Zhongding; Zhenghai Juhong; Beida Guangju; Jingzhou Zhida; Shanghai China Power Investment; Ningbo Longhuahui; Anhui Jintong; Suzhou Xinjing; Ningbo Zhizun; Jiangsu Jiequan; BYD; Chuangqi Kaiying; Hubei Qingyan; Jiaxing Xiuzhou; Zhejiang Dongxin; Xuancheng Jintong; Anqing Jintong; Zhuhai Zhidingli; Shiji Guanghua; Xuancheng Fund': 1, 'Metropolitan Industrial Investment Fund; Future Industry Investment Fund II; Shijiazhuang Keshuo Investment Centre (Limited Partnership); Beijing Tonghe Yinxing Innovative Asset Management Centre (Limited Partnership); Beijing SL Pharmaceutical Co., Ltd.; Shanghai Yunxin Venture Capital Partnership (Limited Partnership)': 1) |
| **BK** | `Pre-IPO institutional shareholding (%)` | 上市前 VC/PE/CVC/国资机构合计持股比例，取紧邻上市前的股权口径，不能混入 IPO 新股或基石配售；统一填 0–1 小数（如 12.5%=0.125）。只有招股书披露或可用披露数字复算时填写，否则 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (29/47 (61.7%)) | 均值 0.32 / 中位数 0.26 / 区间 [0.02, 0.83] |
| **BL** | `Pre-IPO investor board seat (1=yes; 0=no)` | 只有能从招股书明确关联到 Pre-IPO 投资机构的非执行董事或正式观察员席位才填 1；没有证据不等于 0，无法确认时填 NaN。 | 浅蓝 | `boolean` | Ex-ante prospectus disclosure | Sparse (20/47 (42.55%)) | 1 (是): 19 家 (95.0%), 0 (否): 1 家 |
| **BM** | `Earliest Pre-IPO investment round` | 从本公司招股书披露的 Pre-IPO 投资轮次中取最早一轮，保留披露的标准轮次名称；只有明确说明没有外部上市前投资时填 None，否则无法确认时 NA。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (39/47 (82.98%)) | 共 29 种取值 ('Series A': 8, 'Series A Financing': 2, 'Series Angel Financing': 2) |
| **BN** | `Pre-IPO holding duration (years)` | 从最早 Pre-IPO 投资协议日期至本公司招股书日期计算年数，保留两位小数；起始日期无法确认则 NaN。每家公司必须使用自己的招股书日期，不沿用其他季度日期。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (34/47 (72.34%)) | 均值 8.69 / 中位数 7.95 / 区间 [0.70, 18.06] |
| **BO** | `Ultimate controller type` | 最终控制人类型（如：自然人 / 家族 / 国资委 / 地方政府 / 外资 / 无实际控制人）。取 SUBSTANTIAL SHAREHOLDERS 与 Controlling Shareholders 段的实际控制人身份表述。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 37 种取值 ('自然人': 7, 'Natural person': 5, '自然人 (natural persons acting in concert)': 1) |
| **BP** | `Controller economic interest at listing (%)` | 控制人上市时**经济权益**（持股比例），填小数。取 CONTROLLING/SUBSTANTIAL SHAREHOLDERS 表的持股百分比。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.41 / 中位数 0.39 / 区间 [0.08, 0.75] |
| **BQ** | `Controller voting rights at listing (%)` | 控制人上市时**投票权**比例，填小数。有 WVR（同股不同权）时与持股不同，取投票权那一列；无 WVR 通常与 BC 相同。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.46 / 中位数 0.46 / 区间 [0.10, 0.75] |
| **BR** | `Interest-bearing debt at year-1 end` | year-1 期末**总有息负债**（用与 col_V 相同的披露货币基本单位）。包含短期借款、长期借款、租赁负债及带息应付票据债券等带息债务总额，取 INDEBTEDNESS 表格的 Total 余额；不含应付账款等无息负债。必须换算为货币基本单位（乘表格千元/百万元乘数）。期末余额，不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 2,947,889,978.72 / 中位数 377,561,000.00 / 区间 [1,067,000.00, 29,430,478,000.00] |
| **BS** | `Technology commercialization stage` | 技术商业化阶段（如：研发阶段 / 小批量试产 / 商业化初期 / 规模商业化 / 已量产）。按 BUSINESS 与业务摘要里的产品状态表述填，不要按行业推测。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (42/47 (89.36%)) | 共 40 种取值 ('规模商业化': 3, '规模商业化/商业化初期 (CF017 approved May 2021 and included in VBP; six NMPA/FDA approvals; over 20 candidates)': 1, 'Mass production / commercially scaled': 1) |
| **BT** | `Debt repayment (% of planned net IPO proceeds)` | 计划净募资中用于**偿债**的比例，填小数。取 USE OF PROCEEDS 里用于偿还借款/债务的金额 ÷ 计划净募资额；没有该用途填 0。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.10] |
| **BU** | `Listing board` | 上市板块（Main Board 主板） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Main Board': 47) |
| **BV** | `Share class` | 股份类别（如 H Shares / A Shares / Class A Ordinary Shares / Class B Ordinary Shares）。按招股书股本表的类别名称填。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 7 种取值 ('H Shares': 35, 'Ordinary Shares': 6, 'Class A Ordinary Shares; Class B Ordinary Shares': 2) |
| **BW** | `A+H issuer flag` | A+H 两地上市发行人标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 8 家 (17.0%), 0 (否): 39 家 |
| **BX** | `WVR flag` | 不同投票权/同股不同权架构标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 2 家 (4.3%), 0 (否): 45 家 |
| **BY** | `Chapter 18A flag` | 第 18A 章未盈利生物科技公司标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 5 家 (10.6%), 0 (否): 42 家 |
| **BZ** | `Chapter 18C flag` | 第 18C 章特专科技公司标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 4 家 (8.5%), 0 (否): 43 家 |
| **CA** | `Industry classification code` | 恒生行业分类 HSICS 6 位业务细分代码 | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 371,003.62 / 中位数 281,010.00 / 区间 [52,030.00, 703,020.00] |
| **CB** | `Industry classification system and version` | 行业分类系统与版本号 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('HSICS (Hang Seng Industry Classification System) 2026': 47) |
| **CC** | `Incorporation date` | 公司**法定注册成立日期**（dd/mm/yy）。必须优先取自 Statutory and General Information (Appendix V '1. Incorporation')、History & Development 或 Accountants' Report (附注 1)。严禁从 Definitions (释义) 章节取值（释义章节常有起草笔误或仅为前期筹备日）。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | Adequate (46/47 (97.87%)) | 区间: 1992-08-07 ~ 2023-07-04 |
| **CD** | `Firm age at IPO (years)` | 公司成立至上市年限（Lowry et al. 2017 Table 3.4 基础控制变量） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (46/47 (97.87%)) | 均值 13.02 / 中位数 11.76 / 区间 [2.39, 33.25] |
| **CE** | `Place of incorporation` | 公司注册成立法域（如 Cayman Islands, PRC 等） | 深蓝 | `string` | Ex-ante prospectus disclosure | Adequate (46/47 (97.87%)) | 共 2 种取值 ('PRC': 35, 'Cayman Islands': 11) |
| **CF** | `Principal place of business` | 主要营业地点（城市/国家），如 PRC、Hong Kong、Shenzhen, PRC。取公司资料或注册办事处段。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 33 种取值 ('Shanghai, PRC': 7, 'Beijing, PRC': 7, 'Shenzhen, Guangdong Province, PRC': 2) |
| **CG** | `Financial statement unit multiplier` | 财务报表基础货币乘数（千元/万元/百万元） | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Sparse (14/47 (29.79%)) | 均值 1,000.00 / 中位数 1,000.00 / 区间 [1,000.00, 1,000.00] |
| **CH** | `Accounting standard` | 财务报表采用的会计准则（如 IFRS Accounting Standards / HKFRS / ASBE / US GAAP）。取会计师报告开头声明。 | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 9 种取值 ('IFRS Accounting Standards': 36, 'HKFRS Accounting Standards': 3, 'HKFRSs (Hong Kong Financial Reporting Standards)': 2) |
| **CI** | `Year-3 financial period start` | 往绩记录第三年前期起始日 | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2022-01-01 ~ 2023-01-01 |
| **CJ** | `Year-3 financial period end` | 往绩记录第三年前期截止日 | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2022-12-31 ~ 2023-12-31 |
| **CK** | `Year-2 financial period start` | 往绩记录第二年前期起始日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2023-01-01 ~ 2024-01-01 |
| **CL** | `Year-2 financial period end` | 往绩记录第二年前期截止日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2023-12-31 ~ 2024-12-31 |
| **CM** | `Year-1 financial period start` | 往绩记录最近一期起始日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2024-01-01 ~ 2025-01-01 |
| **CN** | `Year-1 net sales (original, pre-annualization)` | 最近一期营业收入原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 3,630,674,851.06 / 中位数 287,362,000.00 / 区间 [0.00, 62,358,825,000.00] |
| **CO** | `Year-1 profit before tax (original)` | 最近一期税前利润原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 192,134,618.79 / 中位数 20,529,000.00 / 区间 [-789,640,000.00, 4,047,917,000.00] |
| **CP** | `Year-1 profit for period (original)` | 最近一期净利润原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 152,192,106.38 / 中位数 18,032,000.00 / 区间 [-791,517,000.00, 3,475,629,000.00] |
| **CQ** | `Subscription opening date` | 香港公开发售**开始认购日期**（dd/mm/yy）。取 EXPECTED TIMETABLE。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-09-26 ~ 2025-12-18 |
| **CR** | `Subscription closing date` | 香港公开发售**截止认购日期**（dd/mm/yy）。取 EXPECTED TIMETABLE。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-10-02 ~ 2025-12-23 |
| **CS** | `H shares after IPO (base; no options)` | 上市后**在港交所挂牌的股份数**（base，不含超额配售）。统一口径：① 内地 H 股发行人全部转换时 = 总股本；② 部分转换时 = 由未上市股转换的 H 股 + 新发 H 股（剩余未上市股不挂牌，不计入）；③ A+H 发行人 = 仅新发 H 股（A 股在沪深市场挂牌，不计入）；④ 开曼/境外发行人没有 H 股类别，其全部股份均在港交所挂牌，故 = 上市后已发行股份总数。即：本列恒等于「港交所挂牌的股份数」，四类结构可比。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 363,192,111.15 / 中位数 136,218,830.00 / 区间 [19,068,400.00, 2,765,176,002.00] |
| **CT** | `Gross profit in year-1` | year-1 **毛利**（用与 col_V 相同的披露货币基本单位）。取损益表的 Gross profit。强制期间锚定：必须与 col_AT 严格同期间！若 col_AT 为中期报告期（如截至 2025 年 6 月 30 日或 9 月 30 日止期间），必须严格提取该中期报告期对应列的原值，绝对严禁错采前一完整财年（FY2024）的数值。必须换算为货币基本单位（乘表格千元/百万元乘数）。不年化——手册明确仅 year-1 销售/税前利润/净利润年化，毛利不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (44/47 (93.62%)) | 均值 929,661,204.55 / 中位数 138,576,000.00 / 区间 [0.00, 16,530,758,000.00] |
| **CU** | `Capital expenditure in year-1` | year-1 **资本开支**（用与 col_V 相同的披露货币基本单位）。取现金流量表“购建物业、厂房及设备”或 CAPITAL EXPENDITURE 段。强制期间锚定：必须与 col_AT 严格同期间！若 col_AT 为中期报告期（如截至 2025 年 6 月 30 日或 9 月 30 日止期间），必须严格提取该中期报告期实际资本开支原值，绝对严禁错采前一完整财年（FY2024）数值。必须换算为货币基本单位（乘表格千元/百万元乘数）。不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 190,515,021.28 / 中位数 15,800,000.00 / 区间 [13,000.00, 3,164,700,000.00] |
| **CV** | `Audit opinion (year-1)` | year-1 **审计意见类型**（如 无保留意见 / Unqualified opinion / Qualified opinion）。取会计师报告的审计意见段。 | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 7 种取值 ('Unqualified opinion': 33, 'Unqualified opinion (true and fair view)': 8, 'Unqualified opinion (无保留意见)': 2) |
| **CW** | `Listing expenses (HK$)` | **总上市费用**（HK$ 基本单位，含承销佣金与其他开支）。取 UNDERWRITING COMMISSIONS AND LISTING EXPENSES 段的合计。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 105,188,255.32 / 中位数 88,500,000.00 / 区间 [26,400,000.00, 358,500,000.00] |
| **CX** | `Cornerstone investor names` | Cornerstone investor names | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (32/47 (68.09%)) | 共 32 种取值 ('Beijing Denov Ruilang Phase XV Equity Investment Fund Center (Limited Partnership)': 1, 'Harvest International Premium Value (Secondary Market) Fund SPC acting on behalf of and for the account of Harvest Oriental SP': 1, 'Blue Lake Capital Opportunity Fund; CUAM Entities; DAMSIMF; Fourier Global Master Fund; GRANITE ASIA VIII INVESTMENTS PTE. LTD.; Greenwoods HK; GTCS Holdings; HongShan Growth; Jain Global Master Fund; Perseverance Asset Management; Stoneylake Global Alpha Fund; WT Asset Management; 3W Fund': 1) |
| **CY** | `Final cornerstone allocation (% of base offer)` | Final cornerstone allocation (% of base offer) | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 0.24 / 中位数 0.24 / 区间 [0.00, 0.50] |
| **CZ** | `Earliest cornerstone unlock date (dd/mm/yy)` | 基石投资者最早解禁日期 | 深蓝 | `date` | Post-IPO lockup expiration events | Adequate (32/47 (68.09%)) | 区间: 2026-04-15 ~ 2026-06-30 |
| **DA** | `Subscription Ratio (times)` | Subscription Ratio (times) | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 2,341.15 / 中位数 1,235.81 / 区间 [1.91, 9,366.28] |
| **DB** | `Public applicants` | Public applicants | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 149,605.98 / 中位数 146,647.00 / 区间 [7,479.00, 386,815.00] |
| **DC** | `Public valid applied shares` | Public valid applied shares | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 7,600,876,263.70 / 中位数 3,214,610,880.00 / 区间 [6,096,750.00, 64,006,413,000.00] |
| **DD** | `Public subscription original wording` | Public subscription original wording | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 47 种取值 ('Subscription level 6,697.80 times': 1, 'Subscription level 5,440.80 times': 1, 'Subscription level 4,908.33 times': 1) |
| **DE** | `Pricing date` | Pricing date | 深蓝 | `date` | Ex-ante prospectus disclosure | Adequate (31/47 (65.96%)) | 区间: 2025-10-08 ~ 2025-12-24 |
| **DF** | `Allotment announcement date` | Allotment announcement date | 深蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-10-06 ~ 2025-12-29 |
| **DG** | `Final global offering shares (before over-allotment)` | Final global offering shares (before over-allotment) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 75,688,566.60 / 中位数 35,456,000.00 / 区间 [3,786,600.00, 631,598,800.00] |
| **DH** | `Final public offer shares` | Final public offer shares | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 7,860,497.23 / 中位数 3,610,000.00 / 区间 [378,700.00, 58,042,600.00] |
| **DI** | `Final placing shares` | Final placing shares | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 67,828,069.36 / 中位数 31,910,400.00 / 区间 [3,407,900.00, 573,556,200.00] |
| **DJ** | `Over-allotment shares actually issued` | Over-allotment shares actually issued | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 4,997,737.23 / 中位数 0.00 / 区间 [0.00, 89,015,600.00] |
| **DK** | `Greenshoe exercise rate (%)` | 绿鞋实际行使比例（Ellis et al. 2000 超额配售执行度与价格支持） | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.27 / 中位数 0.00 / 区间 [0.00, 1.00] |
| **DL** | `Actual clawback / reallocation description` | Actual clawback / reallocation description | 深蓝 | `string` | Ex-ante prospectus disclosure | Adequate (46/47 (97.87%)) | 共 46 种取值 ('Claw-back triggered N/A ; No. of Offer Shares reallocated from the International Offering (claw-back) N/A': 1, 'No claw-back triggered (Claw-back triggered: N/A); the final Hong Kong Public Offer shares remained 597,900, i.e. 10.00% of the Global Offering': 1, 'Number of Offer Shares reallocated from International Offering to Hong Kong Public Offering 0': 1) |
| **DM** | `Net IPO proceeds to issuer (HK$)` | Net IPO proceeds to issuer (HK$) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 1,880,457,245.87 / 中位数 902,200,000.00 / 区间 [12,370,000.00, 14,016,410,000.00] |
| **DN** | `Public shareholding at listing (%)` | Public shareholding at listing (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.37 / 中位数 0.31 / 区间 [0.06, 0.99] |
| **DO** | `Share base used for both public shareholding ratios` | Share base used for both public shareholding ratios | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 711,696,619.00 / 中位数 326,632,000.00 / 区间 [37,866,600.00, 9,105,988,837.00] |
| **DP** | `Unrestricted public shareholding at listing (%)` | Unrestricted public shareholding at listing (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (46/47 (97.87%)) | 均值 0.09 / 中位数 0.10 / 区间 [0.03, 0.25] |
| **DQ** | `Free float denominator description` | Free float denominator description | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 31 种取值 ('Free float denominator = total issued shares upon listing (col_CZ); numerator = offer shares minus cornerstone allocation': 17, 'Free float denominator = total issued Shares upon Listing (411,978,387, per 'Number of issued Shares upon Listing'); numerator = Global Offering shares less cornerstone allocation = 41,198,000 - 0 = 41,198,000': 1, 'Total issued Shares upon Listing (59,788,807 Shares) less locked-up shares: Controlling Shareholders 25,669,015 H Shares (42.93%) and Pre-IPO Investors 28,140,892 H Shares (47.07%); free float is the 5,978,900 H Shares of the Global Offering': 1) |
| **DR** | `Free float denominator shares` | Free float denominator shares | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 711,696,619.00 / 中位数 326,632,000.00 / 区间 [37,866,600.00, 9,105,988,837.00] |
| **DS** | `HSI return over 20 trading days before prospectus (%)` | 招股日前 20 个交易日恒生指数累计收益率 (%) | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 -0.01 / 中位数 -0.01 / 区间 [-0.06, 0.08] |
| **DT** | `HK ordinary IPO count in 90 calendar days before prospectus` | 招股日前 90 个自然日香港普通主板 IPO 上市数量 | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 29.45 / 中位数 31.00 / 区间 [16.00, 38.00] |
| **DU** | `1-month HIBOR before prospectus (%)` | 招股日前一交易日香港银行同业拆借 1 个月 HIBOR 利率 (%) | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.03 / 中位数 0.03 / 区间 [0.02, 0.04] |
| **DV** | `Banking system aggregate balance before prospectus (HK$)` | 招股日前一交易日香港银行体系总结余 (HK$) | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 54,071,872,340.43 / 中位数 54,090,000,000.00 / 区间 [53,877,000,000.00, 54,683,000,000.00] |
| **DW** | `First trading day closing price (HK$)` | 首日上市二级市场收盘价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 65.63 / 中位数 38.50 / 区间 [2.33, 371.00] |
| **DX** | `First-day return / Underpricing (%)` | 上市首日抑价率 / 初始收益率（Rock 1986 / Ritter 1984 核心被解释变量） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 0.42 / 中位数 0.09 / 区间 [-0.49, 3.64] |
| **DY** | `Money left on the table (HK$)` | 留在桌面上的财富 / 抑价转移财富总额（Loughran & Ritter 2002 前景理论指标） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 297,721,755.48 / 中位数 100,977,433.50 / 区间 [-622,412,100.00, 1,800,000,000.00] |
| **DZ** | `First trading day opening price (HK$)` | 首日上市二级市场开盘价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 65.23 / 中位数 38.00 / 区间 [3.26, 319.80] |
| **EA** | `First trading day high (HK$)` | 首日上市二级市场盘中最高价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 71.59 / 中位数 40.58 / 区间 [3.40, 371.00] |
| **EB** | `First trading day low (HK$)` | 首日上市二级市场盘中最低价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 59.75 / 中位数 35.10 / 区间 [2.33, 310.00] |
| **EC** | `First trading day volume (shares)` | 首日上市二级市场全天成交量（股） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 21,718,123.15 / 中位数 8,732,200.00 / 区间 [811,640.00, 170,339,680.00] |
| **ED** | `First-day flipping ratio (%)` | 首日短线翻转抛售率 / 成交量占全球发售比例（Aggarwal 2003 机构抛售假说） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 0.32 / 中位数 0.25 / 区间 [0.07, 1.18] |
| **EE** | `First trading day turnover (HK$)` | 首日上市二级市场全天成交金额 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **EF** | `Offer mechanism` | 适用发售与回拨制度（2025-08-04 前 PN18/18C.09；之后 Mechanism A/B） | 深蓝 | `string` | Ex-ante prospectus disclosure | Adequate (43/47 (91.49%)) | 共 2 种取值 ('Mechanism B': 39, 'Mechanism A': 4) |
| **EG** | `Applicable IPO rules / transition basis` | 适用之上市规则过渡基准（FINI 改革规则） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 3 种取值 ('FINI (from 22/11/2023); 2025-08-04 pricing reform (Mechanism A/B; six-month cornerstone lock-up retained); this IPO: Mechanism B': 39, 'FINI (from 22/11/2023); 2025-08-04 pricing reform (Mechanism A/B; six-month cornerstone lock-up retained); this IPO: Mechanism A': 4, 'FINI (from 22/11/2023); 2025-08-04 pricing reform (Mechanism A/B; six-month cornerstone lock-up retained)': 4) |
| **EH** | `Company Chinese Name` | Company Chinese Name | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (46/47 (97.87%)) | 共 46 种取值 ('长风药业股份有限公司': 1, '上海挚达科技发展股份有限公司': 1, '轩竹生物科技股份有限公司': 1) |
| **EI** | `Current listing status` | 当前挂牌存续状态 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Active': 47) |
| **EJ** | `1-month post-IPO close price (HK$)` | 第20个交易日收盘价（窗口成熟后填报） | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 51.40 / 中位数 29.34 / 区间 [2.10, 201.80] |
| **EK** | `1-month BHR from Day-1 close (%)` | 由首日收盘至第20个交易日的买入持有收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.09 / 中位数 -0.01 / 区间 [-0.59, 1.42] |
| **EL** | `1-month total return from offer price (%)` | 由发售价至第20个交易日的累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.60 / 中位数 0.10 / 区间 [-0.71, 4.48] |
| **EM** | `1-month HSI return (%)` | 同期恒生指数累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.02 / 中位数 0.02 / 区间 [-0.03, 0.07] |
| **EN** | `1-month HSTECH return (%)` | 同期恒生科技指数累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 -0.00 / 中位数 0.01 / 区间 [-0.11, 0.08] |
| **EO** | `1-month wealth relative vs HSI` | 一个月相对恒指财富比 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 1.07 / 中位数 0.97 / 区间 [0.39, 2.33] |
| **EP** | `1-month wealth relative vs HSTECH` | 一个月相对恒生科技指数财富比 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 1.09 / 中位数 0.98 / 区间 [0.39, 2.48] |
| **EQ** | `1-month average daily turnover (HK$)` | 上市后首20个交易日日均成交额 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 76,753,766.55 / 中位数 47,957,715.00 / 区间 [4,889,720.00, 344,052,246.00] |
| **ER** | `6-month post-IPO close price (HK$)` | 六个月目标日后首个交易日收盘价（窗口成熟后填报） | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 42.80 / 中位数 22.22 / 区间 [1.70, 223.20] |
| **ES** | `6-month BHR from Day-1 close (%)` | 由首日收盘至六个月目标交易日的买入持有收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 -0.09 / 中位数 -0.18 / 区间 [-0.83, 1.51] |
| **ET** | `6-month total return from offer price (%)` | 由发售价至六个月目标交易日的累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.22 / 中位数 -0.16 / 区间 [-0.88, 2.25] |
| **EU** | `6-month HSI return (%)` | 同期恒生指数累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 -0.04 / 中位数 -0.03 / 区间 [-0.12, 0.02] |
| **EV** | `6-month HSTECH return (%)` | 同期恒生科技指数累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 -0.17 / 中位数 -0.16 / 区间 [-0.24, -0.09] |
| **EW** | `6-month wealth relative vs HSI` | 六个月相对恒指财富比 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.96 / 中位数 0.87 / 区间 [0.18, 2.84] |
| **EX** | `6-month wealth relative vs HSTECH` | 六个月相对恒生科技指数财富比 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 1.10 / 中位数 0.98 / 区间 [0.21, 3.13] |
| **EY** | `6-month average daily turnover (HK$)` | 六个月目标日前20个交易日日均成交额 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 134,009,939.73 / 中位数 36,872,915.00 / 区间 [39,713.50, 1,193,823,560.00] |
| **EZ** | `Liquidity decay ratio (6M vs Day-1 turnover)` | 六个月窗口日均成交额相对首日成交额比率 | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.35 / 中位数 0.07 / 区间 [0.00, 5.86] |
| **FA** | `1-year post-IPO return (%) [Reserved]` | 一年期收益率预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FB** | `1-year wealth relative vs HSI [Reserved]` | 一年期相对恒指财富比预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FC** | `3-year post-IPO return (%) [Reserved]` | 三年期收益率预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FD** | `3-year wealth relative vs HSI [Reserved]` | 三年期相对恒指财富比预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FE** | `18A/18C regulatory milestone status` | 18A/18C 监管路径与商业化里程碑状态 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 3 种取值 ('Standard': 38, '18A (Biotech / B-tag)': 5, '18C (Specialist Tech)': 4) |
| **FF** | `Stabilizing manager` | 官方指定价格稳定经理人名称 | 深蓝 | `string` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FG** | `Stabilization period end date` | 法定30天稳价期结束日期 | 深蓝 | `string` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FH** | `Stabilization purchases occurred` | 稳价期内是否发生二级市场托单购买 (1=是, 0=否) | 深蓝 | `boolean` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FI** | `Over-allocation shares` | 国际配售超额配售股份数量（股） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FJ** | `Over-allocation (% of base offer)` | 超额配售股数占基础发售股份比例 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FK** | `Over-allotment option exercise date` | 超额配售权实际行使公告日期 | 深蓝 | `string` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FL** | `Shares issued under over-allotment option` | 超额配售权最终发行股份数量（股） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FM** | `Over-allotment exercise percentage (%)` | 超额配售权行使比例 (行使股数/超额配售上限, %) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FN** | `Post-stabilization cliff return [-5, +5] (%)` | 稳价期结束日前后[-5, +5]交易日累计收益率（断崖效应测试） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FO** | `Post-stabilization 20-day return [0, +20] (%)` | 稳价期结束后20个交易日累计收益率 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FP** | `Post-stabilization volume decay ratio (%)` | 稳价结束后20日均成交额相对稳价期内之比 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FQ** | `Day-5 BHR from Day-1 close (%)` | 挂牌首周 (T+5交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 0.02 / 中位数 0.00 / 区间 [-0.36, 0.73] |
| **FR** | `Day-5 wealth relative vs HSI` | 挂牌首周对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 1.01 / 中位数 0.99 / 区间 [0.63, 1.72] |
| **FS** | `Day-20 BHR from Day-1 close (%)` | 首月 (T+20交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 0.09 / 中位数 -0.01 / 区间 [-0.59, 1.42] |
| **FT** | `Day-20 wealth relative vs HSI` | 首月对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 1.07 / 中位数 0.97 / 区间 [0.39, 2.33] |
| **FU** | `3-month BHR from Day-1 close (%)` | 首季 (T+63交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 0.16 / 中位数 0.01 / 区间 [-0.73, 3.21] |
| **FV** | `3-month wealth relative vs HSI` | 首季对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 1.16 / 中位数 0.97 / 区间 [0.28, 4.40] |
| **FW** | `3-month wealth relative vs HSTECH` | 首季对标恒科财富相对比 (WR_HSTECH) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 1.29 / 中位数 1.07 / 区间 [0.31, 5.01] |
| **FX** | `3-month average daily turnover (HK$)` | 首季度日均成交金额 (港元) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 57,623,132.02 / 中位数 32,526,034.38 / 区间 [2,019,421.67, 341,452,819.67] |
| **FY** | `Amihud illiquidity (6M mean)` | 上市前6个月日均 Amihud (2002) 非流动性指标 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.03 / 中位数 0.00 / 区间 [0.00, 0.86] |
| **FZ** | `Zero-volume days count (first 6M)` | 上市前6个月零成交量交易日天数 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.17 / 中位数 0.00 / 区间 [0.00, 7.00] |
| **GA** | `Return volatility (first 6M daily std dev, %)` | 上市前6个月日度收益率标准差 (波动率, %) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.07 / 中位数 0.06 / 区间 [0.03, 0.17] |
| **GB** | `Maximum drawdown (first 6M, %)` | 上市前6个月二级市场最大回撤幅度 (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.55 / 中位数 0.58 / 区间 [0.23, 0.93] |
| **GC** | `Controlling shareholder 6-month disposal lockup expiry date` | 控股股东首阶段6个月绝对禁售期满日 | 深蓝 | `string` | Post-IPO lockup expiration events | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GD** | `Controlling shareholder 12-month cessation of control expiry date` | 控股股东次阶段12个月控制权锁定到期日 | 深蓝 | `string` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GE** | `Cornerstone unlock CAR [-5, +5] (%)` | 基石投资者解禁日前后[-5, +5]交易日累计超额收益 (CAR vs HSI) | 深蓝 | `numeric` | Post-IPO lockup expiration events | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GF** | `Cornerstone unlock CAR [-20, +20] (%)` | 基石投资者解禁日前后[-20, +20]交易日累计超额收益 (CAR vs HSI) | 深蓝 | `numeric` | Post-IPO lockup expiration events | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GG** | `Cornerstone unlock volume shock ratio` | 基石解禁后20日均换手额相对解禁前20日换手额之比 | 深蓝 | `numeric` | Post-IPO lockup expiration events | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GH** | `Lead sponsor name` | 独家/联席牵头保荐人英文全称 | 深蓝 | `string` | Prospectus syndicate structure | 100% 完备 | 共 18 种取值 ('China International Capital Corporation Hong Kong Securities Limited': 14, 'CITIC Securities (Hong Kong) Limited': 10, 'Huatai Financial Holdings (Hong Kong) Limited': 3) |
| **GI** | `Joint sponsor count` | 保荐人总家数 (独家=1, 联席=2+) | 深蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 1.89 / 中位数 2.00 / 区间 [1.00, 5.00] |
| **GJ** | `Sponsor commercial bank affiliate flag` | 保荐人是否属于商业银行系金融机构 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus syndicate structure | 100% 完备 | 1 (是): 12 家 (25.5%), 0 (否): 35 家 |
| **GK** | `Underwriting base commission rate (%)` | 承销基础佣金费率 (%) | 深蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.03 / 中位数 0.03 / 区间 [0.01, 0.05] |
| **GL** | `Underwriting discretionary incentive fee rate (%)` | 招股书披露的酌情奖励费率上限（非实际支付，%） | 深蓝 | `numeric` | Prospectus syndicate structure | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GM** | `Total underwriting fee rate (%)` | 披露的承销总费率上限（基础+奖励上限，非实际支付，%） | 深蓝 | `numeric` | Prospectus syndicate structure | Reserved / Unmatured (0/47 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GN** | `Cornerstone investor count` | 基石投资者机构总家数 | 深蓝 | `numeric` | Prospectus / allotment institutional network | 100% 完备 | 均值 6.36 / 中位数 4.00 / 区间 [0.00, 28.00] |
| **GO** | `Cornerstone state-owned presence flag` | 基石投资者中是否包含国资/地方政府基金 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | Adequate (46/47 (97.87%)) | 1 (是): 30 家 (65.2%), 0 (否): 16 家 |
| **GP** | `Crossover fund presence flag` | 是否包含兼具 Pre-IPO 与基石双重身份的跨界基金 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | Adequate (46/47 (97.87%)) | 1 (是): 0 家 (0.0%), 0 (否): 46 家 |
| **GQ** | `Pre-IPO institutional investor count` | 主要 Pre-IPO 投资机构总数 | 深蓝 | `numeric` | Prospectus / allotment institutional network | Adequate (46/47 (97.87%)) | 均值 17.15 / 中位数 16.00 / 区间 [0.00, 75.00] |
| **GR** | `Pre-IPO state-owned backing flag` | Pre-IPO 股东中是否包含国资机构 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | Adequate (46/47 (97.87%)) | 1 (是): 34 家 (73.9%), 0 (否): 12 家 |
| **GS** | `FINI digital settlement regime` | 结算监管体制 (POST_FINI / PRE_FINI) | 深蓝 | `string` | Listing date regulatory regime | 100% 完备 | 共 1 种取值 ('POST_FINI': 47) |
| **GT** | `2025 pricing reform regime` | 发售与定价机制改革体制 (POST_2025_REFORM / PRE_2025_REFORM) | 深蓝 | `string` | Listing date regulatory regime | 100% 完备 | 共 1 种取值 ('POST_2025_REFORM': 47) |

---

## 三、计量软件导入指引 (Stata / Python)

配套清洗数据文件：`out/HKIPO-MB2025Q4_clean.csv`（编码：UTF-8 with BOM）。

### 1. Stata
```stata
* 导入纯净版 CSV 数据
import delimited "out/HKIPO-MB2025Q4_clean.csv", clear bindquote(strict) varnames(1)
describe
summarize
```

### 2. Python (pandas)
```python
import pandas as pd
df = pd.read_csv("out/HKIPO-MB2025Q4_clean.csv")
print(df.info())
print(df.describe())
```

---
*本数据代码本由 HK IPO Prospectus Pipeline 自动化分析引擎生成。*
