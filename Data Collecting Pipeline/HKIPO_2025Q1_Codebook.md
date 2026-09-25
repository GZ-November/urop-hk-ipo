# 香港主板 2025 Q1 IPO 学术研究数据变量代码本 (Data Codebook)

- **样本规模 (N)**：15 家香港联交所主板新上市公司
- **变量总数 (K)**：202 维完整跨学科指标
- **数据层级划分**：浅绿官方基础 (11 列) + 浅蓝招股书披露 (77 列) + 深蓝配发及外部衍生 (114 列)
- **生成时间**：2026-09-25 21:46:59 | **数据基准**：`HKIPO-MB.xlsx` (Sheet: NLR)

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
| **A** | `HKEx file# of the year` | 港交所年度申请编号 | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 8.73 / 中位数 8.00 / 区间 [1.00, 17.00] |
| **B** | `Stock Code` | 股份代号（四位港股代码，如 6082.HK） | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 15 种取值 ('6681.HK': 1, '2560.HK': 1, '2613.HK': 1) |
| **C** | `Company Name at time of listing` | 公司上市时法定英文名称 | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 15 种取值 ('BrainAurora Medical Technology Limited - B': 1, 'Anhui Conch Material Technology Co., Ltd. - H shares': 1, 'ContiOcean Environment Tech Group Co., Ltd. - H shares': 1) |
| **D** | `Date of Prospectus (dd/mm/yy)` | 招股书刊发日期 | 浅绿 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2024-12-30 ~ 2025-03-21 |
| **E** | `Date of Listing (dd/mm/yy)` | 正式挂牌上市交易日期 | 浅绿 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-01-08 ~ 2025-03-31 |
| **F** | `Sponsor(s)` | 独家/联席保荐人名单 | 浅绿 | `string` | Prospectus syndicate structure | 100% 完备 | 共 14 种取值 ('Huatai Financial Holdings (Hong Kong) Limited': 2, 'China International Capital Corporation Hong Kong Securities Limited/ SPDB International Capital Limited': 1, 'China Securities (International) Corporate Finance Company Limited': 1) |
| **G** | `Reporting Accountants` | 申报会计师事务所 | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 5 种取值 ('Ernst & Young': 5, 'KPMG': 4, 'Deloitte Touche Tohmatsu': 2) |
| **H** | `Valuer(s)` | 独立物业或资产估值师 | 浅绿 | `string` | Ex-ante prospectus disclosure | Sparse (2/15 (13.33%)) | 共 2 种取值 ('Jones Lang LaSalle Corporate Appraisal and Advisory Limited': 1, 'BonVision International Appraisals Limited': 1) |
| **I** | `Funds Raised HK (a)` | 香港公开发售募资额 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 306,672,849.00 / 中位数 80,000,000.00 / 区间 [22,230,000.00, 1,727,325,000.00] |
| **J** | `Funds Raised Int.(b)` | 国际配售募资额 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 936,906,441.93 / 中位数 469,972,800.00 / 区间 [63,750,000.00, 2,962,622,712.00] |
| **K** | `IPO Subscription Price (HK$)` | 最终发售定价 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 29.37 / 中位数 9.94 / 区间 [0.51, 202.50] |
| **L** | `Total (without option)` | Total (without option) | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 1,005,739,874.13 / 中位数 588,235,300.00 / 区间 [24,120,300.00, 4,588,400,000.00] |
| **M** | `Global Offering (without option)` | Global Offering (without option) | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 156,997,393.33 / 中位数 144,974,000.00 / 区间 [9,900,000.00, 688,400,000.00] |
| **N** | `Number of offer shares under the capitalization Issue` | 全球发售完成前的已发行股份总数。本数据集口径：一律填 L − M（Total 减去全球发售股数），即使招股书未披露「资本化发行」也必须照填，不得留 NaN。用于满足恒等式 L = N + Q。2026Q1 成品工作簿 38 家公司全部取 L − M，Q2 必须同口径。数值只取权威 SHARE CAPITAL 汇总表与封面，禁止取「历史沿革／资本化发行沿革」段落。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 848,742,480.80 / 中位数 500,000,000.00 / 区间 [0.00, 3,900,000,000.00] |
| **O** | `Number of offer shares under Capitalization Rest` | 与 col_N 同口径：一律填 L − M（全球发售完成前的已发行股份总数），即使招股书未披露「资本化转换」也必须照填，不得留 NaN。用于满足恒等式 L = O + M。2026Q1 成品 38 家全部为 L − M。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 848,742,480.80 / 中位数 500,000,000.00 / 区间 [0.00, 3,900,000,000.00] |
| **P** | `Sale Shares` | 老股出售（Sale Shares）数量。若为全部新股的 Offer for Subscription（无 Selling Shareholder），填数字 0，不得留 NaN，用于满足恒等式 M = Q + P。判据：封面／股本汇总表无 Sale Shares 行，且全文无 Selling Shareholder 披露。2026Q1 成品 38 家全部为 0。若确有老股出售，按招股书披露填写。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **Q** | `New shares` | New shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 156,997,393.33 / 中位数 144,974,000.00 / 区间 [9,900,000.00, 688,400,000.00] |
| **R** | `Placing Shares` | Placing Shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 141,297,480.00 / 中位数 130,476,000.00 / 区间 [8,910,000.00, 619,560,000.00] |
| **S** | `Public Offer shares` | Public Offer shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 15,699,913.33 / 中位数 14,498,000.00 / 区间 [990,000.00, 68,840,000.00] |
| **T** | `Maximum Offer Price` | Maximum Offer Price | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 31.25 / 中位数 9.94 / 区间 [0.60, 202.50] |
| **U** | `Minimum Offer Price` | Minimum Offer Price | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 28.88 / 中位数 8.68 / 区间 [0.50, 202.50] |
| **V** | `Filing price revision (%)` | 发售定价偏离询价区间中点幅度（Hanley 1993 动态信息提取，固定价格发售为 0.00%） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 -0.06 / 中位数 -0.07 / 区间 [-0.15, 0.07] |
| **W** | `Filing range width (%)` | 询价区间相对宽度（Beatty & Ritter 1986 事前估值不确定性，固定价格发售为 0.00%） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.16 / 中位数 0.14 / 区间 [0.00, 0.40] |
| **X** | `Pricing position in filing range` | 定价落点分类体系（Fixed price / Above range / At high / Midpoint / Within range / At low / Below range） | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 4 种取值 ('At low': 7, 'Within range': 4, 'Fixed price': 2) |
| **Y** | `currency in financial information` | currency in financial information | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 2 种取值 ('RMB': 14, 'USD': 1) |
| **Z** | `total assets in year-3 (3 years before IPO)` | total assets in year-3 (3 years before IPO) | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 7,778,577,866.67 / 中位数 1,177,000,000.00 / 区间 [224,320,000.00, 80,413,277,000.00] |
| **AA** | `total assets in year-2` | total assets in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 8,944,329,200.00 / 中位数 1,012,656,000.00 / 区间 [300,223,000.00, 93,444,044,000.00] |
| **AB** | `total assets in year-1` | total assets in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (14/15 (93.33%)) | 均值 10,592,662,571.43 / 中位数 1,003,975,000.00 / 区间 [318,927,000.00, 100,192,656,000.00] |
| **AC** | `total equity in year-3` | total equity in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 1,418,698,133.33 / 中位数 265,022,000.00 / 区间 [-1,377,115,000.00, 8,667,952,000.00] |
| **AD** | `total equity in year-2` | total equity in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 1,760,493,133.33 / 中位数 410,076,000.00 / 区间 [-1,608,294,000.00, 9,286,500,000.00] |
| **AE** | `total equity in year-1` | total equity in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (14/15 (93.33%)) | 均值 2,471,404,642.86 / 中位数 497,376,500.00 / 区间 [-411,266,000.00, 10,595,465,000.00] |
| **AF** | `total liability in year-3` | total liability in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 6,359,879,733.33 / 中位数 779,489,000.00 / 区间 [50,942,000.00, 71,745,325,000.00] |
| **AG** | `total liability in year-2` | total liability in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 7,183,836,066.67 / 中位数 727,035,000.00 / 区间 [52,921,000.00, 84,157,544,000.00] |
| **AH** | `total liability in year-1` | total liability in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (14/15 (93.33%)) | 均值 8,121,257,928.57 / 中位数 583,320,000.00 / 区间 [44,640,000.00, 90,578,459,000.00] |
| **AI** | `Net sales in year-3` | Net sales in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (13/15 (86.67%)) | 均值 1,996,984,307.69 / 中位数 325,574,000.00 / 区间 [11,291,000.00, 10,350,986,000.00] |
| **AJ** | `Net sales in year-2` | Net sales in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (13/15 (86.67%)) | 均值 2,556,662,153.85 / 中位数 498,780,000.00 / 区间 [67,200,000.00, 13,575,577,000.00] |
| **AK** | `Net sales in year-1` | Net sales in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (13/15 (86.67%)) | 均值 3,476,227,846.15 / 中位数 720,303,000.00 / 区间 [103,774,000.00, 20,302,465,000.00] |
| **AL** | `Profit before tax in year-3` | Profit before tax in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 217,027,133.33 / 中位数 41,658,000.00 / 区间 [-502,461,000.00, 2,558,874,000.00] |
| **AM** | `Profit before tax in year-2` | Profit before tax in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 332,150,133.33 / 中位数 68,487,000.00 / 区间 [-359,116,000.00, 2,658,043,000.00] |
| **AN** | `Profit before tax in year-1` | Profit before tax in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (14/15 (93.33%)) | 均值 658,832,547.64 / 中位数 124,230,000.00 / 区间 [-228,778,000.00, 4,154,002,000.00] |
| **AO** | `Profit for the year in year-3` | Profit for the year in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 132,556,466.67 / 中位数 35,080,000.00 / 区间 [-502,461,000.00, 1,911,942,000.00] |
| **AP** | `Profit for the year in year-2` | Profit for the year in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 235,241,933.33 / 中位数 51,065,000.00 / 区间 [-359,116,000.00, 2,013,091,000.00] |
| **AQ** | `Profit for the year in year-1` | Profit for the year in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (14/15 (93.33%)) | 均值 488,432,476.21 / 中位数 105,481,000.00 / 区间 [-228,778,000.00, 3,186,605,000.00] |
| **AR** | `Underwriting Commission (% of fund raised HK (a)` | Underwriting Commission (% of fund raised HK (a) | 浅蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.03 / 中位数 0.03 / 区间 [0.01, 0.06] |
| **AS** | `Underwriting Commission (% of fund raised Int.(b)` | Underwriting Commission (% of fund raised Int.(b) | 浅蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.03 / 中位数 0.03 / 区间 [0.01, 0.06] |
| **AT** | `Over-allotment Option (%)` | Over-allotment Option (%) | 浅蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 0.14 / 中位数 0.15 / 区间 [0.00, 0.15] |
| **AU** | `Principal business / industry` | Principal business / industry | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 15 种取值 ('Cognitive impairment digital therapeutics (DTx) integral software solutions / medical devices': 1, 'Cement and concrete admixtures and their in-process intermediaries (fine chemical materials)': 1, 'marine exhaust gas cleaning systems, marine energy-saving devices, marine clean-energy supply systems and maritime services': 1) |
| **AV** | `Listing route / applicable chapter` | Listing route / applicable chapter | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 8 种取值 ('Main Board': 8, 'Main Board Chapter 18A of the Listing Rules': 1, 'Main Board of The Stock Exchange of Hong Kong Limited (H Shares)': 1) |
| **AW** | `Year-1 financial period end (dd/mm/yy)` | Year-1 financial period end (dd/mm/yy) | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2023-12-31 ~ 2024-09-30 |
| **AX** | `Operating cash flow in year-1 (before annualization)` | Operating cash flow in year-1 (before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (14/15 (93.33%)) | 均值 921,646,928.57 / 中位数 108,019,500.00 / 区间 [-102,406,000.00, 4,964,236,000.00] |
| **AY** | `Cash and cash equivalents at year-1 end` | Cash and cash equivalents at year-1 end | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (14/15 (93.33%)) | 均值 1,346,449,142.86 / 中位数 239,436,500.00 / 区间 [14,345,000.00, 7,177,645,000.00] |
| **AZ** | `R&D expensed in year-1 (before annualization)` | R&D expensed in year-1 (before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (11/15 (73.33%)) | 均值 54,821,181.82 / 中位数 47,893,000.00 / 区间 [0.00, 198,736,000.00] |
| **BA** | `Development costs capitalized in year-1 (additions, before annualization)` | Development costs capitalized in year-1 (additions, before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (12/15 (80.0%)) | 均值 654,666.67 / 中位数 0.00 / 区间 [0.00, 5,056,000.00] |
| **BB** | `Top 5 customers (% of year-1 revenue)` | Top 5 customers (% of year-1 revenue) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (12/15 (80.0%)) | 均值 0.54 / 中位数 0.56 / 区间 [0.01, 1.00] |
| **BC** | `Comments / Annualization factor` | 最近一期财务数据对应的年化因子与口径说明 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 1.00 / 中位数 1.00 / 区间 [1.00, 1.00] |
| **BD** | `Pre-IPO VC/PE backing (1=yes; 0=no)` | 是否引入 Pre-IPO VC/PE 投资者：1=有，0=无。看 HISTORY AND DEVELOPMENT — Pre-IPO Investments 与 SUBSTANTIAL SHAREHOLDERS 名单；只要有专业投资机构（VC/PE/产业基金）在上市前入股即 1。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.53 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BE** | `Pre-IPO VC backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。早期/成长期专业风险投资基金为 1；未找到证据不等于 0，无法确认时填 NaN。分类依据须在本字段 quote 中体现。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.40 / 中位数 0.00 / 区间 [0.00, 1.00] |
| **BF** | `Pre-IPO PE backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。中晚期私募股权基金或并购基金为 1；未找到证据不等于 0，无法确认时填 NaN。分类依据须在本字段 quote 中体现。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.53 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BG** | `Pre-IPO CVC backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。发行人产业股东须有战略投资/企业风投关系依据才归 CVC；普通产业股东不能自动算 CVC。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (14/15 (93.33%)) | 均值 0.07 / 中位数 0.00 / 区间 [0.00, 1.00] |
| **BH** | `Pre-IPO State/Gov backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。有明确国资、政府或产业引导基金背景的机构为 1；国资身份不自动代表 VC/PE。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.40 / 中位数 0.00 / 区间 [0.00, 1.00] |
| **BI** | `Top-tier VC/PE backing (1=yes; 0=no)` | 仅在本公司招股书确认一线知名 VC/PE 机构持有重要股权或领投时填 1；不得仅凭机构知名度推断其参与本公司投资。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (13/15 (86.67%)) | 均值 0.31 / 中位数 0.00 / 区间 [0.00, 1.00] |
| **BJ** | `Key Pre-IPO investors` | 仅列本公司招股书披露的上市前投资者，采用一致的英文全称/拼音并以分号分隔；同一投资者只记一次，不从其他 cohort 补名单。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (10/15 (66.67%)) | 共 10 种取值 ('Northern Light Venture Capital funds (NLSF/NLVF/NLPF via IMMENSE VANTAGE), Zhongwei Growth, Shanghai Pegasus, Tianjin Kangsheng, Tianjin Tianjian, Tianjin Chengye, Anji Shundian, Hainan Synthesis, CICC Healthcare Fund, Mr. Tan': 1, 'CCB Financial Asset Investment; Anhui Huiyuan LP; Wuhu Longmen LP; Wuhu Industrial Fund (Kegai Ceyuan LP and Anhui Zhongan LP exited in 2023)': 1, 'Legend Capital (via Idea Great and LC Fund), Yunfeng Capital (Yunfeng Blocks/Tuoyuan), Gaorong (Gaorong BLK Holding), Gaintex, BlueCo (Mr. Charlie Cao), JYCP/JYMB Holding, SinoMedia (Asia Pacific), NAW, Way Elegance, Mr. Qi Daqing': 1) |
| **BK** | `Pre-IPO institutional shareholding (%)` | 上市前 VC/PE/CVC/国资机构合计持股比例，取紧邻上市前的股权口径，不能混入 IPO 新股或基石配售；统一填 0–1 小数（如 12.5%=0.125）。只有招股书披露或可用披露数字复算时填写，否则 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (10/15 (66.67%)) | 均值 0.13 / 中位数 0.09 / 区间 [0.00, 0.51] |
| **BL** | `Pre-IPO investor board seat (1=yes; 0=no)` | 只有能从招股书明确关联到 Pre-IPO 投资机构的非执行董事或正式观察员席位才填 1；没有证据不等于 0，无法确认时填 NaN。 | 浅蓝 | `boolean` | Ex-ante prospectus disclosure | Adequate (14/15 (93.33%)) | 1 (是): 5 家 (35.7%), 0 (否): 9 家 |
| **BM** | `Earliest Pre-IPO investment round` | 从本公司招股书披露的 Pre-IPO 投资轮次中取最早一轮，保留披露的标准轮次名称；只有明确说明没有外部上市前投资时填 None，否则无法确认时 NA。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (9/15 (60.0%)) | 共 9 种取值 ('Series Angel': 1, 'Pre-IPO Investment (January 2023)': 1, 'Series Angel Investment (2018)': 1) |
| **BN** | `Pre-IPO holding duration (years)` | 从最早 Pre-IPO 投资协议日期至本公司招股书日期计算年数，保留两位小数；起始日期无法确认则 NaN。每家公司必须使用自己的招股书日期，不沿用其他季度日期。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (8/15 (53.33%)) | 均值 5.60 / 中位数 5.35 / 区间 [1.98, 9.80] |
| **BO** | `Ultimate controller type` | 最终控制人类型（如：自然人 / 家族 / 国资委 / 地方政府 / 外资 / 无实际控制人）。取 SUBSTANTIAL SHAREHOLDERS 与 Controlling Shareholders 段的实际控制人身份表述。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 13 种取值 ('individual': 2, '自然人': 2, 'Individuals (Mr. Tan Zheng and Dr. Wang Xiaoyi)': 1) |
| **BP** | `Controller economic interest at listing (%)` | 控制人上市时**经济权益**（持股比例），填小数。取 CONTROLLING/SUBSTANTIAL SHAREHOLDERS 表的持股百分比。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (14/15 (93.33%)) | 均值 0.52 / 中位数 0.55 / 区间 [0.13, 0.75] |
| **BQ** | `Controller voting rights at listing (%)` | 控制人上市时**投票权**比例，填小数。有 WVR（同股不同权）时与持股不同，取投票权那一列；无 WVR 通常与 BC 相同。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (14/15 (93.33%)) | 均值 0.53 / 中位数 0.55 / 区间 [0.13, 0.75] |
| **BR** | `Interest-bearing debt at year-1 end` | year-1 期末**总有息负债**（用与 col_V 相同的披露货币基本单位）。包含短期借款、长期借款、租赁负债及带息应付票据债券等带息债务总额，取 INDEBTEDNESS 表格的 Total 余额；不含应付账款等无息负债。必须换算为货币基本单位（乘表格千元/百万元乘数）。期末余额，不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (13/15 (86.67%)) | 均值 628,284,846.15 / 中位数 103,994,000.00 / 区间 [907,000.00, 3,350,203,000.00] |
| **BS** | `Technology commercialization stage` | 技术商业化阶段（如：研发阶段 / 小批量试产 / 商业化初期 / 规模商业化 / 已量产）。按 BUSINESS 与业务摘要里的产品状态表述填，不要按行业推测。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (8/15 (53.33%)) | 共 7 种取值 ('Commercialized at scale (mass production and sale)': 2, 'Commercial stage': 1, 'Commercialised (products sold at scale)': 1) |
| **BT** | `Debt repayment (% of planned net IPO proceeds)` | 计划净募资中用于**偿债**的比例，填小数。取 USE OF PROCEEDS 里用于偿还借款/债务的金额 ÷ 计划净募资额；没有该用途填 0。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.01 / 中位数 0.00 / 区间 [0.00, 0.15] |
| **BU** | `Listing board` | 上市板块（Main Board 主板） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Main Board': 15) |
| **BV** | `Share class` | 股份类别（如 H Shares / A Shares / Class A Ordinary Shares / Class B Ordinary Shares）。按招股书股本表的类别名称填。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 8 种取值 ('Ordinary Shares': 4, 'H Shares': 3, 'H shares': 3) |
| **BW** | `A+H issuer flag` | A+H 两地上市发行人标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 15 家 |
| **BX** | `WVR flag` | 不同投票权/同股不同权架构标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 15 家 |
| **BY** | `Chapter 18A flag` | 第 18A 章未盈利生物科技公司标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 2 家 (13.3%), 0 (否): 13 家 |
| **BZ** | `Chapter 18C flag` | 第 18C 章特专科技公司标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 15 家 |
| **CA** | `Industry classification code` | 恒生行业分类 HSICS 6 位业务细分代码 | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 251,755.33 / 中位数 251,030.00 / 区间 [51,010.00, 702,030.00] |
| **CB** | `Industry classification system and version` | 行业分类系统与版本号 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('HSICS (Hang Seng Industry Classification System) 2026': 15) |
| **CC** | `Incorporation date` | 公司**法定注册成立日期**（dd/mm/yy）。必须优先取自 Statutory and General Information (Appendix V '1. Incorporation')、History & Development 或 Accountants' Report (附注 1)。严禁从 Definitions (释义) 章节取值（释义章节常有起草笔误或仅为前期筹备日）。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 1998-06-22 ~ 2023-11-22 |
| **CD** | `Firm age at IPO (years)` | 公司成立至上市年限（Lowry et al. 2017 Table 3.4 基础控制变量） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 8.87 / 中位数 6.38 / 区间 [1.34, 26.72] |
| **CE** | `Place of incorporation` | 公司注册成立法域（如 Cayman Islands, PRC 等） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 2 种取值 ('Cayman Islands': 8, 'PRC': 7) |
| **CF** | `Principal place of business` | 主要营业地点（城市/国家），如 PRC、Hong Kong、Shenzhen, PRC。取公司资料或注册办事处段。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 15 种取值 ('PRC (Beijing)': 1, 'Wuhu City, Anhui Province, China': 1, 'Shanghai, the PRC': 1) |
| **CG** | `Financial statement unit multiplier` | 财务报表基础货币乘数（千元/万元/百万元） | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (8/15 (53.33%)) | 均值 1,000.00 / 中位数 1,000.00 / 区间 [1,000.00, 1,000.00] |
| **CH** | `Accounting standard` | 财务报表采用的会计准则（如 IFRS Accounting Standards / HKFRS / ASBE / US GAAP）。取会计师报告开头声明。 | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 6 种取值 ('IFRS': 6, 'IFRS Accounting Standards': 3, 'IFRSs': 2) |
| **CI** | `Year-3 financial period start` | 往绩记录第三年前期起始日 | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2021-01-01 ~ 2021-10-01 |
| **CJ** | `Year-3 financial period end` | 往绩记录第三年前期截止日 | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2021-12-31 ~ 2022-09-30 |
| **CK** | `Year-2 financial period start` | 往绩记录第二年前期起始日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2022-01-01 ~ 2022-10-01 |
| **CL** | `Year-2 financial period end` | 往绩记录第二年前期截止日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2022-12-31 ~ 2023-09-30 |
| **CM** | `Year-1 financial period start` | 往绩记录最近一期起始日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2023-01-01 ~ 2023-10-01 |
| **CN** | `Year-1 net sales (original, pre-annualization)` | 最近一期营业收入原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | Adequate (13/15 (86.67%)) | 均值 3,476,227,846.15 / 中位数 720,303,000.00 / 区间 [103,774,000.00, 20,302,465,000.00] |
| **CO** | `Year-1 profit before tax (original)` | 最近一期税前利润原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | Adequate (14/15 (93.33%)) | 均值 658,832,547.64 / 中位数 124,230,000.00 / 区间 [-228,778,000.00, 4,154,002,000.00] |
| **CP** | `Year-1 profit for period (original)` | 最近一期净利润原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | Adequate (14/15 (93.33%)) | 均值 488,432,476.21 / 中位数 105,481,000.00 / 区间 [-228,778,000.00, 3,186,605,000.00] |
| **CQ** | `Subscription opening date` | 香港公开发售**开始认购日期**（dd/mm/yy）。取 EXPECTED TIMETABLE。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2024-12-30 ~ 2025-03-21 |
| **CR** | `Subscription closing date` | 香港公开发售**截止认购日期**（dd/mm/yy）。取 EXPECTED TIMETABLE。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-01-03 ~ 2025-03-26 |
| **CS** | `H shares after IPO (base; no options)` | 上市后**在港交所挂牌的股份数**（base，不含超额配售）。统一口径：① 内地 H 股发行人全部转换时 = 总股本；② 部分转换时 = 由未上市股转换的 H 股 + 新发 H 股（剩余未上市股不挂牌，不计入）；③ A+H 发行人 = 仅新发 H 股（A 股在沪深市场挂牌，不计入）；④ 开曼/境外发行人没有 H 股类别，其全部股份均在港交所挂牌，故 = 上市后已发行股份总数。即：本列恒等于「港交所挂牌的股份数」，四类结构可比。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (12/15 (80.0%)) | 均值 539,877,457.67 / 中位数 209,949,455.00 / 区间 [10,000,000.00, 2,332,525,060.00] |
| **CT** | `Gross profit in year-1` | year-1 **毛利**（用与 col_V 相同的披露货币基本单位）。取损益表的 Gross profit。强制期间锚定：必须与 col_AT 严格同期间！若 col_AT 为中期报告期（如截至 2025 年 6 月 30 日或 9 月 30 日止期间），必须严格提取该中期报告期对应列的原值，绝对严禁错采前一完整财年（FY2024）的数值。必须换算为货币基本单位（乘表格千元/百万元乘数）。不年化——手册明确仅 year-1 销售/税前利润/净利润年化，毛利不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (13/15 (86.67%)) | 均值 1,036,412,307.69 / 中位数 209,100,000.00 / 区间 [24,520,000.00, 5,998,967,000.00] |
| **CU** | `Capital expenditure in year-1` | year-1 **资本开支**（用与 col_V 相同的披露货币基本单位）。取现金流量表“购建物业、厂房及设备”或 CAPITAL EXPENDITURE 段。强制期间锚定：必须与 col_AT 严格同期间！若 col_AT 为中期报告期（如截至 2025 年 6 月 30 日或 9 月 30 日止期间），必须严格提取该中期报告期实际资本开支原值，绝对严禁错采前一完整财年（FY2024）数值。必须换算为货币基本单位（乘表格千元/百万元乘数）。不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (14/15 (93.33%)) | 均值 251,249,714.29 / 中位数 40,238,500.00 / 区间 [117,000.00, 1,690,766,000.00] |
| **CV** | `Audit opinion (year-1)` | year-1 **审计意见类型**（如 无保留意见 / Unqualified opinion / Qualified opinion）。取会计师报告的审计意见段。 | 浅蓝 | `string` | Track record period financial disclosure | Adequate (14/15 (93.33%)) | 共 6 种取值 ('Unqualified': 5, 'Unqualified opinion': 3, 'Unaudited': 2) |
| **CW** | `Listing expenses (HK$)` | **总上市费用**（HK$ 基本单位，含承销佣金与其他开支）。取 UNDERWRITING COMMISSIONS AND LISTING EXPENSES 段的合计。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 87,573,582.20 / 中位数 81,200,000.00 / 区间 [39,000,000.00, 163,700,000.00] |
| **CX** | `Cornerstone investor names` | Cornerstone investor names | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (11/15 (73.33%)) | 共 11 种取值 ('Tasly (Hong Kong) Pharmaceutical Investment Limited; Tasly (International) Healthcare Investment&Development Company Limited; Huang Guangwei; Suzhou Ceyuan Fuhai Enterprise Management Partnership (Limited Partnership)': 1, '国轩高科股份有限公司(Gotion High-tech); 安徽盛昌化工有限公司(Anhui Shengchang); 芜湖阿泰克生物科技有限公司(Wuhu Artec); SCGC Capital Holding Company Limited; 广东纵行科技有限公司(Guangdong Zongxing); 深圳高灯计算机科技有限公司(Shenzhen Gaodeng)': 1, 'Harvest International Premium Value (Secondary Market) Fund SPC on behalf of Harvest Oriental SP': 1) |
| **CY** | `Final cornerstone allocation (% of base offer)` | Final cornerstone allocation (% of base offer) | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 0.30 / 中位数 0.29 / 区间 [0.00, 0.70] |
| **CZ** | `Earliest cornerstone unlock date (dd/mm/yy)` | 基石投资者最早解禁日期 | 深蓝 | `date` | Post-IPO lockup expiration events | Adequate (11/15 (73.33%)) | 区间: 2025-07-08 ~ 2025-09-30 |
| **DA** | `Subscription Ratio (times)` | Subscription Ratio (times) | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 794.42 / 中位数 46.96 / 区间 [0.21, 5,999.96] |
| **DB** | `Public applicants` | Public applicants | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 37,911.67 / 中位数 12,389.00 / 区间 [2,336.00, 264,992.00] |
| **DC** | `Public valid applied shares` | Public valid applied shares | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 2,241,011,040.00 / 中位数 206,386,000.00 / 区间 [8,855,400.00, 14,473,713,600.00] |
| **DD** | `Public subscription original wording` | Public subscription original wording | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 15 种取值 ('Subscription level 11.39 times': 1, 'Subscription level 25.83 times': 1, 'Subscription level 55.33 times (Hong Kong Public Offering); International Offering subscription level 0.95 times': 1) |
| **DE** | `Pricing date` | Pricing date | 深蓝 | `date` | Ex-ante prospectus disclosure | Adequate (14/15 (93.33%)) | 区间: 2025-01-07 ~ 2025-03-27 |
| **DF** | `Allotment announcement date` | Allotment announcement date | 深蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-01-07 ~ 2025-03-28 |
| **DG** | `Final global offering shares (before over-allotment)` | Final global offering shares (before over-allotment) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 158,923,700.00 / 中位数 144,974,000.00 / 区间 [10,000,000.00, 688,400,000.00] |
| **DH** | `Final public offer shares` | Final public offer shares | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 31,540,113.33 / 中位数 14,538,000.00 / 区间 [1,894,200.00, 125,000,000.00] |
| **DI** | `Final placing shares` | Final placing shares | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 127,383,586.67 / 中位数 101,481,000.00 / 区间 [6,831,000.00, 673,862,000.00] |
| **DJ** | `Over-allotment shares actually issued` | Over-allotment shares actually issued | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 4,042,433.33 / 中位数 0.00 / 区间 [0.00, 30,847,800.00] |
| **DK** | `Greenshoe exercise rate (%)` | 绿鞋实际行使比例（Ellis et al. 2000 超额配售执行度与价格支持） | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.26 / 中位数 0.00 / 区间 [0.00, 1.00] |
| **DL** | `Actual clawback / reallocation description` | Actual clawback / reallocation description | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 15 种取值 ('Claw-back triggered: No; final no. of Offer Shares under the Hong Kong Public Offering remained at the initial 18,112,000 (no clawback from the International Offering)': 1, 'No. of Offer Shares reallocated from the International Placing (claw-back) 28,995,000': 1, '894,200 Offer Shares reallocated from the International Offering to the Hong Kong Public Offering; final Hong Kong Public Offering increased from 1,000,000 to 1,894,200 H Shares (~18.94% of the Global Offering)': 1) |
| **DM** | `Net IPO proceeds to issuer (HK$)` | Net IPO proceeds to issuer (HK$) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 1,061,957,333.33 / 中位数 501,320,000.00 / 区间 [86,000,000.00, 3,291,000,000.00] |
| **DN** | `Public shareholding at listing (%)` | Public shareholding at listing (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (13/15 (86.67%)) | 均值 0.24 / 中位数 0.25 / 区间 [0.10, 0.49] |
| **DO** | `Share base used for both public shareholding ratios` | Share base used for both public shareholding ratios | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 1,022,156,310.47 / 中位数 588,235,300.00 / 区间 [40,000,000.00, 4,588,400,000.00] |
| **DP** | `Unrestricted public shareholding at listing (%)` | Unrestricted public shareholding at listing (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.13 / 中位数 0.09 / 区间 [0.02, 0.25] |
| **DQ** | `Free float denominator description` | Free float denominator description | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 15 种取值 ('Total issued share capital of the Company immediately following the completion of the Global Offering (Number of issued Shares upon Listing, before exercise of the Over-allotment Option; the Over-allotment Option was not exercised)': 1, '% of total issued share capital upon Listing (579,894,000 shares, before exercise of the Over-allotment Option)': 1, 'Total issued share capital of the Company upon Listing = 40,000,000 shares (30,000,000 domestic shares + 10,000,000 H Shares), assuming options under the Pre-IPO Share Option Scheme are not exercised': 1) |
| **DR** | `Free float denominator shares` | Free float denominator shares | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 1,022,156,310.47 / 中位数 588,235,300.00 / 区间 [40,000,000.00, 4,588,400,000.00] |
| **DS** | `HSI return over 20 trading days before prospectus (%)` | 招股日前 20 个交易日恒生指数累计收益率 (%) | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 0.06 / 中位数 0.03 / 区间 [0.01, 0.17] |
| **DT** | `HK ordinary IPO count in 90 calendar days before prospectus` | 招股日前 90 个自然日香港普通主板 IPO 上市数量 | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 21.73 / 中位数 22.00 / 区间 [16.00, 25.00] |
| **DU** | `1-month HIBOR before prospectus (%)` | 招股日前一交易日香港银行同业拆借 1 个月 HIBOR 利率 (%) | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.04 / 中位数 0.05 / 区间 [0.04, 0.05] |
| **DV** | `Banking system aggregate balance before prospectus (HK$)` | 招股日前一交易日香港银行体系总结余 (HK$) | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 45,245,866,666.67 / 中位数 45,746,000,000.00 / 区间 [44,595,000,000.00, 45,752,000,000.00] |
| **DW** | `First trading day closing price (HK$)` | 首日上市二级市场收盘价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 36.40 / 中位数 8.12 / 区间 [0.61, 290.00] |
| **DX** | `First-day return / Underpricing (%)` | 上市首日抑价率 / 初始收益率（Rock 1986 / Ritter 1984 核心被解释变量） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 -0.01 / 中位数 0.00 / 区间 [-0.60, 0.43] |
| **DY** | `Money left on the table (HK$)` | 留在桌面上的财富 / 抑价转移财富总额（Loughran & Ritter 2002 前景理论指标） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 75,868,202.17 / 中位数 0.00 / 区间 [-331,974,552.00, 1,492,741,250.00] |
| **DZ** | `First trading day opening price (HK$)` | 首日上市二级市场开盘价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 36.39 / 中位数 8.82 / 区间 [0.49, 262.00] |
| **EA** | `First trading day high (HK$)` | 首日上市二级市场盘中最高价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 39.14 / 中位数 9.22 / 区间 [0.71, 298.00] |
| **EB** | `First trading day low (HK$)` | 首日上市二级市场盘中最低价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 33.72 / 中位数 7.75 / 区间 [0.48, 256.00] |
| **EC** | `First trading day volume (shares)` | 首日上市二级市场全天成交量（股） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 51,921,865.47 / 中位数 25,689,500.00 / 区间 [2,054,100.00, 272,546,000.00] |
| **ED** | `First-day flipping ratio (%)` | 首日短线翻转抛售率 / 成交量占全球发售比例（Aggarwal 2003 机构抛售假说） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 0.43 / 中位数 0.30 / 区间 [0.04, 1.09] |
| **EE** | `First trading day turnover (HK$)` | 首日上市二级市场全天成交金额 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 690,793,458.67 / 中位数 101,952,200.00 / 区间 [9,176,480.00, 4,333,988,600.00] |
| **EF** | `Offer mechanism` | 适用发售与回拨制度（2025-08-04 前 PN18/18C.09；之后 Mechanism A/B） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('PN18 statutory clawback': 15) |
| **EG** | `Applicable IPO rules / transition basis` | 适用之上市规则过渡基准（FINI 改革规则） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('FINI (from 22/11/2023)': 15) |
| **EH** | `Company Chinese Name` | Company Chinese Name | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 15 种取值 ('脑动极光医疗科技有限公司': 1, '安徽海螺材料科技股份有限公司': 1, '上海汇舸环保科技集团股份有限公司': 1) |
| **EI** | `Current listing status` | 当前挂牌存续状态 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Active': 15) |
| **EJ** | `1-month post-IPO close price (HK$)` | 第20个交易日收盘价（窗口成熟后填报） | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 45.21 / 中位数 13.86 / 区间 [0.61, 432.00] |
| **EK** | `1-month BHR from Day-1 close (%)` | 由首日收盘至第20个交易日的买入持有收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.11 / 中位数 0.00 / 区间 [-0.36, 0.71] |
| **EL** | `1-month total return from offer price (%)` | 由发售价至第20个交易日的累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.11 / 中位数 0.11 / 区间 [-0.66, 1.13] |
| **EM** | `1-month HSI return (%)` | 同期恒生指数累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.05 / 中位数 0.10 / 区间 [-0.17, 0.17] |
| **EN** | `1-month HSTECH return (%)` | 同期恒生科技指数累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.09 / 中位数 0.20 / 区间 [-0.25, 0.27] |
| **EO** | `1-month wealth relative vs HSI` | 一个月相对恒指财富比 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 1.07 / 中位数 0.97 / 区间 [0.71, 1.57] |
| **EP** | `1-month wealth relative vs HSTECH` | 一个月相对恒生科技指数财富比 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 1.05 / 中位数 0.89 / 区间 [0.69, 1.59] |
| **EQ** | `1-month average daily turnover (HK$)` | 上市后首20个交易日日均成交额 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 90,690,910.57 / 中位数 11,750,145.00 / 区间 [5,230,722.50, 657,746,425.00] |
| **ER** | `6-month post-IPO close price (HK$)` | 六个月目标日后首个交易日收盘价（窗口成熟后填报） | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 49.79 / 中位数 12.98 / 区间 [0.62, 409.00] |
| **ES** | `6-month BHR from Day-1 close (%)` | 由首日收盘至六个月目标交易日的买入持有收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.46 / 中位数 0.22 / 区间 [-0.37, 1.72] |
| **ET** | `6-month total return from offer price (%)` | 由发售价至六个月目标交易日的累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.44 / 中位数 0.41 / 区间 [-0.51, 1.41] |
| **EU** | `6-month HSI return (%)` | 同期恒生指数累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.20 / 中位数 0.24 / 区间 [0.10, 0.28] |
| **EV** | `6-month HSTECH return (%)` | 同期恒生科技指数累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.17 / 中位数 0.21 / 区间 [0.00, 0.25] |
| **EW** | `6-month wealth relative vs HSI` | 六个月相对恒指财富比 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 1.24 / 中位数 0.98 / 区间 [0.57, 2.38] |
| **EX** | `6-month wealth relative vs HSTECH` | 六个月相对恒生科技指数财富比 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 1.28 / 中位数 1.00 / 区间 [0.57, 2.64] |
| **EY** | `6-month average daily turnover (HK$)` | 六个月目标日前20个交易日日均成交额 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 72,000,129.40 / 中位数 1,409,940.00 / 区间 [49,525.50, 369,387,891.00] |
| **EZ** | `Liquidity decay ratio (6M vs Day-1 turnover)` | 六个月窗口日均成交额相对首日成交额比率 | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.08 / 中位数 0.02 / 区间 [0.00, 0.53] |
| **FA** | `1-year post-IPO return (%) [Reserved]` | 一年期收益率预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FB** | `1-year wealth relative vs HSI [Reserved]` | 一年期相对恒指财富比预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FC** | `3-year post-IPO return (%) [Reserved]` | 三年期收益率预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FD** | `3-year wealth relative vs HSI [Reserved]` | 三年期相对恒指财富比预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FE** | `18A/18C regulatory milestone status` | 18A/18C 监管路径与商业化里程碑状态 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 2 种取值 ('Standard': 13, '18A (Biotech / B-tag)': 2) |
| **FF** | `Stabilizing manager` | 官方指定价格稳定经理人名称 | 深蓝 | `string` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FG** | `Stabilization period end date` | 法定30天稳价期结束日期 | 深蓝 | `string` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FH** | `Stabilization purchases occurred` | 稳价期内是否发生二级市场托单购买 (1=是, 0=否) | 深蓝 | `boolean` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FI** | `Over-allocation shares` | 国际配售超额配售股份数量（股） | 深蓝 | `string` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FJ** | `Over-allocation (% of base offer)` | 超额配售股数占基础发售股份比例 (%) | 深蓝 | `string` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FK** | `Over-allotment option exercise date` | 超额配售权实际行使公告日期 | 深蓝 | `string` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FL** | `Shares issued under over-allotment option` | 超额配售权最终发行股份数量（股） | 深蓝 | `string` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FM** | `Over-allotment exercise percentage (%)` | 超额配售权行使比例 (行使股数/超额配售上限, %) | 深蓝 | `string` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FN** | `Post-stabilization cliff return [-5, +5] (%)` | 稳价期结束日前后[-5, +5]交易日累计收益率（断崖效应测试） | 深蓝 | `string` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FO** | `Post-stabilization 20-day return [0, +20] (%)` | 稳价期结束后20个交易日累计收益率 (%) | 深蓝 | `string` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FP** | `Post-stabilization volume decay ratio (%)` | 稳价结束后20日均成交额相对稳价期内之比 (%) | 深蓝 | `string` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FQ** | `Day-5 BHR from Day-1 close (%)` | 挂牌首周 (T+5交易日) 二级买入持有收益率 (%) | 深蓝 | `string` | Aftermarket event horizon window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FR** | `Day-5 wealth relative vs HSI` | 挂牌首周对标恒指财富相对比 (WR_HSI) | 深蓝 | `string` | Aftermarket event horizon window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FS** | `Day-20 BHR from Day-1 close (%)` | 首月 (T+20交易日) 二级买入持有收益率 (%) | 深蓝 | `string` | Aftermarket event horizon window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FT** | `Day-20 wealth relative vs HSI` | 首月对标恒指财富相对比 (WR_HSI) | 深蓝 | `string` | Aftermarket event horizon window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FU** | `3-month BHR from Day-1 close (%)` | 首季 (T+63交易日) 二级买入持有收益率 (%) | 深蓝 | `string` | Aftermarket event horizon window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FV** | `3-month wealth relative vs HSI` | 首季对标恒指财富相对比 (WR_HSI) | 深蓝 | `string` | Aftermarket event horizon window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FW** | `3-month wealth relative vs HSTECH` | 首季对标恒科财富相对比 (WR_HSTECH) | 深蓝 | `string` | Aftermarket event horizon window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FX** | `3-month average daily turnover (HK$)` | 首季度日均成交金额 (港元) | 深蓝 | `string` | Aftermarket event horizon window | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FY** | `Amihud illiquidity (6M mean)` | 上市前6个月日均 Amihud (2002) 非流动性指标 | 深蓝 | `string` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **FZ** | `Zero-volume days count (first 6M)` | 上市前6个月零成交量交易日天数 | 深蓝 | `string` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GA** | `Return volatility (first 6M daily std dev, %)` | 上市前6个月日度收益率标准差 (波动率, %) | 深蓝 | `string` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GB** | `Maximum drawdown (first 6M, %)` | 上市前6个月二级市场最大回撤幅度 (%) | 深蓝 | `string` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GC** | `Controlling shareholder 6-month disposal lockup expiry date` | 控股股东首阶段6个月绝对禁售期满日 | 深蓝 | `string` | Post-IPO lockup expiration events | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GD** | `Controlling shareholder 12-month cessation of control expiry date` | 控股股东次阶段12个月控制权锁定到期日 | 深蓝 | `string` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GE** | `Cornerstone unlock CAR [-5, +5] (%)` | 基石投资者解禁日前后[-5, +5]交易日累计超额收益 (CAR vs HSI) | 深蓝 | `string` | Post-IPO lockup expiration events | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GF** | `Cornerstone unlock CAR [-20, +20] (%)` | 基石投资者解禁日前后[-20, +20]交易日累计超额收益 (CAR vs HSI) | 深蓝 | `string` | Post-IPO lockup expiration events | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GG** | `Cornerstone unlock volume shock ratio` | 基石解禁后20日均换手额相对解禁前20日换手额之比 | 深蓝 | `string` | Post-IPO lockup expiration events | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GH** | `Lead sponsor name` | 独家/联席牵头保荐人英文全称 | 深蓝 | `string` | Prospectus syndicate structure | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GI** | `Joint sponsor count` | 保荐人总家数 (独家=1, 联席=2+) | 深蓝 | `string` | Prospectus syndicate structure | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GJ** | `Sponsor commercial bank affiliate flag` | 保荐人是否属于商业银行系金融机构 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus syndicate structure | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GK** | `Underwriting base commission rate (%)` | 承销基础佣金费率 (%) | 深蓝 | `string` | Prospectus syndicate structure | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GL** | `Underwriting discretionary incentive fee rate (%)` | 承销酌情奖励费率估算 (%) | 深蓝 | `string` | Prospectus syndicate structure | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GM** | `Total underwriting fee rate (%)` | 承销总费率估算 (基础+奖励, %) | 深蓝 | `string` | Prospectus syndicate structure | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GN** | `Cornerstone investor count` | 基石投资者机构总家数 | 深蓝 | `string` | Prospectus / allotment institutional network | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GO** | `Cornerstone state-owned presence flag` | 基石投资者中是否包含国资/地方政府基金 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GP** | `Crossover fund presence flag` | 是否包含兼具 Pre-IPO 与基石双重身份的跨界基金 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GQ** | `Pre-IPO institutional investor count` | 主要 Pre-IPO 投资机构总数 | 深蓝 | `string` | Prospectus / allotment institutional network | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GR** | `Pre-IPO state-owned backing flag` | Pre-IPO 股东中是否包含国资机构 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GS** | `FINI digital settlement regime` | 结算监管体制 (POST_FINI / PRE_FINI) | 深蓝 | `string` | Listing date regulatory regime | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |
| **GT** | `2025 pricing reform regime` | 发售与定价机制改革体制 (POST_2025_REFORM / PRE_2025_REFORM) | 深蓝 | `string` | Listing date regulatory regime | Reserved / Unmatured (0/15 (0.0%)) | 全部缺失 |

---

## 三、计量软件导入指引 (Stata / Python)

配套清洗数据文件：`out/HKIPO-MB2025Q1_clean.csv`（编码：UTF-8 with BOM）。

### 1. Stata
```stata
* 导入纯净版 CSV 数据
import delimited "out/HKIPO-MB2025Q1_clean.csv", clear bindquote(strict) varnames(1)
describe
summarize
```

### 2. Python (pandas)
```python
import pandas as pd
df = pd.read_csv("out/HKIPO-MB2025Q1_clean.csv")
print(df.info())
print(df.describe())
```

---
*本数据代码本由 HK IPO Prospectus Pipeline 自动化分析引擎生成。*
