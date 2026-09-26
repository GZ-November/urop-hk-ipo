# 香港主板 2025 Q2 IPO 学术研究数据变量代码本 (Data Codebook)

- **样本规模 (N)**：27 家香港联交所主板新上市公司
- **变量总数 (K)**：202 维完整跨学科指标
- **数据层级划分**：浅绿官方基础 (11 列) + 浅蓝招股书披露 (77 列) + 深蓝配发及外部衍生 (114 列)
- **生成时间**：2026-09-26 11:56:19 | **数据基准**：`HKIPO-MB.xlsx` (Sheet: NLR)

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
| **A** | `HKEx file# of the year` | 港交所年度申请编号 | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 31.00 / 中位数 31.00 / 区间 [18.00, 44.00] |
| **B** | `Stock Code` | 股份代号（四位港股代码，如 6082.HK） | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 27 种取值 ('3677.HK': 1, '9606.HK': 1, '1333.HK': 1) |
| **C** | `Company Name at time of listing` | 公司上市时法定英文名称 | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 27 种取值 ('Jiangsu Zenergy Battery Technologies Group Co., Ltd.- H shares': 1, 'Duality Biotherapeutics, Inc. - B': 1, 'Breton Technology Co., Ltd.- H shares': 1) |
| **D** | `Date of Prospectus (dd/mm/yy)` | 招股书刊发日期 | 浅绿 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-04-03 ~ 2025-06-20 |
| **E** | `Date of Listing (dd/mm/yy)` | 正式挂牌上市交易日期 | 浅绿 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-04-14 ~ 2025-06-30 |
| **F** | `Sponsor(s)` | 独家/联席保荐人名单 | 浅绿 | `string` | Prospectus syndicate structure | 100% 完备 | 共 25 种取值 ('China International Capital Corporation Hong Kong Securities Limited/ CMB International Capital Limited': 2, 'China International Capital Corporation Hong Kong Securities Limited': 2, 'Morgan Stanley Asia Limited/ Jefferies Hong Kong Limited/ CITIC Securities (Hong Kong) Limited': 1) |
| **G** | `Reporting Accountants` | 申报会计师事务所 | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 8 种取值 ('Ernst & Young': 9, 'KPMG': 7, 'PricewaterhouseCoopers': 5) |
| **H** | `Valuer(s)` | 独立物业或资产估值师 | 浅绿 | `string` | Ex-ante prospectus disclosure | Sparse (2/27 (7.41%)) | 共 2 种取值 ('Peak Vision Appraisals Limited': 1, 'AVISTA Group': 1) |
| **I** | `Funds Raised HK (a)` | 香港公开发售募资额 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 541,954,063.68 / 中位数 150,415,200.00 / 区间 [24,290,000.00, 2,674,289,200.00] |
| **J** | `Funds Raised Int.(b)` | 国际配售募资额 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 2,819,064,955.96 / 中位数 493,180,428.00 / 区间 [97,554,600.00, 38,331,434,700.00] |
| **K** | `IPO Subscription Price (HK$)` | 最终发售定价 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 40.06 / 中位数 18.90 / 区间 [2.86, 263.00] |
| **L** | `Total (without option)` | Total (without option) | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 1,190,235,435.30 / 中位数 385,955,532.00 / 区间 [70,953,453.00, 6,603,522,074.00] |
| **M** | `Global Offering (without option)` | Global Offering (without option) | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 87,342,193.33 / 中位数 46,620,000.00 / 区间 [1,560,980.00, 360,330,000.00] |
| **N** | `Number of offer shares under the capitalization Issue` | 全球发售完成前的已发行股份总数。本数据集口径：一律填 L − M（Total 减去全球发售股数），即使招股书未披露「资本化发行」也必须照填，不得留 NaN。用于满足恒等式 L = N + Q。2026Q1 成品工作簿 38 家公司全部取 L − M，Q2 必须同口径。数值只取权威 SHARE CAPITAL 汇总表与封面，禁止取「历史沿革／资本化发行沿革」段落。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 1,104,763,953.07 / 中位数 366,672,032.00 / 区间 [68,104,164.00, 6,379,002,274.00] |
| **O** | `Number of offer shares under Capitalization Rest` | 与 col_N 同口径：一律填 L − M（全球发售完成前的已发行股份总数），即使招股书未披露「资本化转换」也必须照填，不得留 NaN。用于满足恒等式 L = O + M。2026Q1 成品 38 家全部为 L − M。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 1,102,893,241.96 / 中位数 366,672,032.00 / 区间 [68,104,164.00, 6,379,002,274.00] |
| **P** | `Sale Shares` | 老股出售（Sale Shares）数量。若为全部新股的 Offer for Subscription（无 Selling Shareholder），填数字 0，不得留 NaN，用于满足恒等式 M = Q + P。判据：封面／股本汇总表无 Sale Shares 行，且全文无 Selling Shareholder 披露。2026Q1 成品 38 家全部为 0。若确有老股出售，按招股书披露填写。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 1,870,711.11 / 中位数 0.00 / 区间 [0.00, 50,509,200.00] |
| **Q** | `New shares` | New shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 85,471,482.22 / 中位数 46,620,000.00 / 区间 [1,560,980.00, 360,330,000.00] |
| **R** | `Placing Shares` | Placing Shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 79,881,625.19 / 中位数 41,958,000.00 / 区间 [1,404,880.00, 335,106,900.00] |
| **S** | `Public Offer shares` | Public Offer shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 7,460,568.15 / 中位数 4,662,000.00 / 区间 [156,100.00, 33,340,000.00] |
| **T** | `Maximum Offer Price` | Maximum Offer Price | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 41.00 / 中位数 20.90 / 区间 [3.35, 263.00] |
| **U** | `Minimum Offer Price` | Minimum Offer Price | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (26/27 (96.3%)) | 均值 28.75 / 中位数 18.45 / 区间 [2.80, 165.00] |
| **V** | `Filing price revision (%)` | 发售定价偏离询价区间中点幅度（Hanley 1993 动态信息提取，固定价格发售为 0.00%） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 -0.01 / 中位数 0.00 / 区间 [-0.23, 0.11] |
| **W** | `Filing range width (%)` | 询价区间相对宽度（Beatty & Ritter 1986 事前估值不确定性，固定价格发售为 0.00%） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.10 / 中位数 0.06 / 区间 [0.00, 0.46] |
| **X** | `Pricing position in filing range` | 定价落点分类体系（Fixed price / Above range / At high / Midpoint / Within range / At low / Below range） | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 4 种取值 ('Fixed price': 11, 'At high': 8, 'At low': 5) |
| **Y** | `currency in financial information` | currency in financial information | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 3 种取值 ('RMB': 23, 'CNY': 2, 'USD': 2) |
| **Z** | `total assets in year-3 (3 years before IPO)` | total assets in year-3 (3 years before IPO) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (23/27 (85.19%)) | 均值 37,587,980,147.39 / 中位数 1,550,292,000.00 / 区间 [119,827,390.00, 717,168,041,000.00] |
| **AA** | `total assets in year-2` | total assets in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 35,686,814,883.37 / 中位数 1,548,079,000.00 / 区间 [30,511,000.00, 786,658,123,000.00] |
| **AB** | `total assets in year-1` | total assets in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (26/27 (96.3%)) | 均值 38,821,681,898.15 / 中位数 1,845,988,500.00 / 区间 [71,354,352.00, 820,097,269,000.00] |
| **AC** | `total equity in year-3` | total equity in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (24/27 (88.89%)) | 均值 12,588,276,679.71 / 中位数 501,719,500.00 / 区间 [-5,298,050,000.00, 219,883,150,000.00] |
| **AD** | `total equity in year-2` | total equity in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 13,719,958,035.56 / 中位数 458,545,000.00 / 区间 [-6,373,594,000.00, 273,456,173,000.00] |
| **AE** | `total equity in year-1` | total equity in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (26/27 (96.3%)) | 均值 15,081,472,005.96 / 中位数 603,656,997.00 / 区间 [-7,205,579,000.00, 289,139,355,000.00] |
| **AF** | `total liability in year-3` | total liability in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (23/27 (85.19%)) | 均值 24,465,674,971.87 / 中位数 1,105,221,000.00 / 区间 [181,589,353.00, 497,284,891,000.00] |
| **AG** | `total liability in year-2` | total liability in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 21,966,856,867.81 / 中位数 1,054,862,000.00 / 区间 [21,005,000.00, 513,201,950,000.00] |
| **AH** | `total liability in year-1` | total liability in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (26/27 (96.3%)) | 均值 23,740,209,891.96 / 中位数 1,337,272,000.00 / 区间 [26,047,000.00, 530,957,914,000.00] |
| **AI** | `Net sales in year-3` | Net sales in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (24/27 (88.89%)) | 均值 21,324,827,053.96 / 中位数 1,443,732,500.00 / 区间 [0.00, 400,917,045,000.00] |
| **AJ** | `Net sales in year-2` | Net sales in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 18,414,837,742.37 / 中位数 1,634,395,000.00 / 区间 [0.00, 362,012,554,000.00] |
| **AK** | `Net sales in year-1` | Net sales in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (26/27 (96.3%)) | 均值 18,478,921,551.92 / 中位数 1,664,171,500.00 / 区间 [0.00, 338,818,356,000.00] |
| **AL** | `Profit before tax in year-3` | Profit before tax in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (23/27 (85.19%)) | 均值 2,894,640,548.74 / 中位数 146,693,000.00 / 区间 [-2,130,304,000.00, 54,495,054,000.00] |
| **AM** | `Profit before tax in year-2` | Profit before tax in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 2,897,601,624.67 / 中位数 29,554,000.00 / 区间 [-1,939,996,000.00, 64,470,204,000.00] |
| **AN** | `Profit before tax in year-1` | Profit before tax in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (26/27 (96.3%)) | 均值 3,285,304,939.88 / 中位数 42,481,500.00 / 区间 [-1,206,342,000.00, 69,500,124,000.00] |
| **AO** | `Profit for the year in year-3` | Profit for the year in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (23/27 (85.19%)) | 均值 2,499,884,761.00 / 中位数 121,462,000.00 / 区间 [-2,007,100,000.00, 47,342,035,000.00] |
| **AP** | `Profit for the year in year-2` | Profit for the year in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 2,454,012,266.74 / 中位数 27,603,000.00 / 区间 [-1,981,058,000.00, 55,294,959,000.00] |
| **AQ** | `Profit for the year in year-1` | Profit for the year in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (26/27 (96.3%)) | 均值 2,782,300,376.50 / 中位数 37,331,500.00 / 区间 [-1,246,389,000.00, 59,445,536,000.00] |
| **AR** | `Underwriting Commission (% of fund raised HK (a)` | Underwriting Commission (% of fund raised HK (a) | 浅蓝 | `numeric` | Prospectus syndicate structure | Adequate (25/27 (92.59%)) | 均值 0.03 / 中位数 0.03 / 区间 [0.00, 0.14] |
| **AS** | `Underwriting Commission (% of fund raised Int.(b)` | Underwriting Commission (% of fund raised Int.(b) | 浅蓝 | `numeric` | Prospectus syndicate structure | Adequate (25/27 (92.59%)) | 均值 0.03 / 中位数 0.03 / 区间 [0.00, 0.14] |
| **AT** | `Over-allotment Option (%)` | Over-allotment Option (%) | 浅蓝 | `numeric` | Post-IPO 30-day stabilization window | Adequate (24/27 (88.89%)) | 均值 0.13 / 中位数 0.15 / 区间 [0.00, 0.15] |
| **AU** | `Principal business / industry` | Principal business / industry | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 27 种取值 ('Lithium-ion battery manufacturer (EV battery and ESS battery products)': 1, '抗体偶联药物（ADC）创新药研发（生物科技）': 1, 'China-based provider of electric-powered engineering machinery (battery-electric loaders and wide-body dump trucks with autonomous capabilities)': 1) |
| **AV** | `Listing route / applicable chapter` | Listing route / applicable chapter | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 20 种取值 ('Main Board': 8, 'Main Board - Rule 8.05(3) market capitalization/revenue test': 1, 'Chapter 18A of the Listing Rules（18A 生物科技公司）': 1) |
| **AW** | `Year-1 financial period end (dd/mm/yy)` | Year-1 financial period end (dd/mm/yy) | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2024-12-31 ~ 2025-04-30 |
| **AX** | `Operating cash flow in year-1 (before annualization)` | Operating cash flow in year-1 (before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (26/27 (96.3%)) | 均值 2,069,306,992.54 / 中位数 144,523,500.00 / 区间 [-361,142,000.00, 32,868,257,000.00] |
| **AY** | `Cash and cash equivalents at year-1 end` | Cash and cash equivalents at year-1 end | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 12,513,844,735.67 / 中位数 255,998,000.00 / 区间 [5,073,863.00, 286,300,836,000.00] |
| **AZ** | `R&D expensed in year-1 (before annualization)` | R&D expensed in year-1 (before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (22/27 (81.48%)) | 均值 754,052,179.36 / 中位数 109,928,000.00 / 区间 [12,553,000.00, 6,582,916,000.00] |
| **BA** | `Development costs capitalized in year-1 (additions, before annualization)` | Development costs capitalized in year-1 (additions, before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (23/27 (85.19%)) | 均值 75,702,739.13 / 中位数 0.00 / 区间 [0.00, 1,732,707,000.00] |
| **BB** | `Top 5 customers (% of year-1 revenue)` | Top 5 customers (% of year-1 revenue) | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (23/27 (85.19%)) | 均值 0.41 / 中位数 0.37 / 区间 [0.02, 1.00] |
| **BC** | `Comments / Annualization factor` | 最近一期财务数据对应的年化因子与口径说明 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 1.00 / 中位数 1.00 / 区间 [1.00, 1.00] |
| **BD** | `Pre-IPO VC/PE backing (1=yes; 0=no)` | 是否引入 Pre-IPO VC/PE 投资者：1=有，0=无。看 HISTORY AND DEVELOPMENT — Pre-IPO Investments 与 SUBSTANTIAL SHAREHOLDERS 名单；只要有专业投资机构（VC/PE/产业基金）在上市前入股即 1。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (21/27 (77.78%)) | 均值 0.95 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BE** | `Pre-IPO VC backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。早期/成长期专业风险投资基金为 1；未找到证据不等于 0，无法确认时填 NaN。分类依据须在本字段 quote 中体现。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (19/27 (70.37%)) | 均值 0.89 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BF** | `Pre-IPO PE backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。中晚期私募股权基金或并购基金为 1；未找到证据不等于 0，无法确认时填 NaN。分类依据须在本字段 quote 中体现。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (21/27 (77.78%)) | 均值 0.90 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BG** | `Pre-IPO CVC backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。发行人产业股东须有战略投资/企业风投关系依据才归 CVC；普通产业股东不能自动算 CVC。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (16/27 (59.26%)) | 均值 0.69 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BH** | `Pre-IPO State/Gov backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。有明确国资、政府或产业引导基金背景的机构为 1；国资身份不自动代表 VC/PE。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (17/27 (62.96%)) | 均值 0.65 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BI** | `Top-tier VC/PE backing (1=yes; 0=no)` | 仅在本公司招股书确认一线知名 VC/PE 机构持有重要股权或领投时填 1；不得仅凭机构知名度推断其参与本公司投资。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Sparse (11/27 (40.74%)) | 均值 0.73 / 中位数 1.00 / 区间 [0.00, 1.00] |
| **BJ** | `Key Pre-IPO investors` | 仅列本公司招股书披露的上市前投资者，采用一致的英文全称/拼音并以分号分隔；同一投资者只记一次，不从其他 cohort 补名单。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (20/27 (74.07%)) | 共 20 种取值 ('Oceanpine Capital; Nanjing Jiangning; CICC SAIC Investment; Southeast Xinneng; Chuanghe Xincai; C&D Investment; Juxin Xihai; Lianhe Jiaying; Jiaxing Chenyue; Xiamen ITG Group; Nanjing Heyi; Anhui Haichuang': 1, 'LAV USD; King Star Med; Shanghai Yingjia; Orchids; Golden Sword; China Singapore Suzhou Industrial Park Ventures (CSVC)': 1, 'Zhongding No.5; Xiangtan Caixin; Changjiang Automobile Valley; Huzhou Qingyun; Jinhua Boleidun; Kesheng Center; Shandong Kinetic Energy; Rockets Capital L.P.; Broad-Ocean Motor': 1) |
| **BK** | `Pre-IPO institutional shareholding (%)` | 上市前 VC/PE/CVC/国资机构合计持股比例，取紧邻上市前的股权口径，不能混入 IPO 新股或基石配售；统一填 0–1 小数（如 12.5%=0.125）。只有招股书披露或可用披露数字复算时填写，否则 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (15/27 (55.56%)) | 均值 0.26 / 中位数 0.21 / 区间 [0.00, 0.69] |
| **BL** | `Pre-IPO investor board seat (1=yes; 0=no)` | 只有能从招股书明确关联到 Pre-IPO 投资机构的非执行董事或正式观察员席位才填 1；没有证据不等于 0，无法确认时填 NaN。 | 浅蓝 | `boolean` | Ex-ante prospectus disclosure | Sparse (10/27 (37.04%)) | 1 (是): 3 家 (30.0%), 0 (否): 7 家 |
| **BM** | `Earliest Pre-IPO investment round` | 从本公司招股书披露的 Pre-IPO 投资轮次中取最早一轮，保留披露的标准轮次名称；只有明确说明没有外部上市前投资时填 None，否则无法确认时 NA。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (20/27 (74.07%)) | 共 17 种取值 ('Series A': 4, 'Series Seed Financing (April 24, 2020)': 1, 'Series A financing (October 2018)': 1) |
| **BN** | `Pre-IPO holding duration (years)` | 从最早 Pre-IPO 投资协议日期至本公司招股书日期计算年数，保留两位小数；起始日期无法确认则 NaN。每家公司必须使用自己的招股书日期，不沿用其他季度日期。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (15/27 (55.56%)) | 均值 7.40 / 中位数 7.37 / 区间 [2.20, 17.20] |
| **BO** | `Ultimate controller type` | 最终控制人类型（如：自然人 / 家族 / 国资委 / 地方政府 / 外资 / 无实际控制人）。取 SUBSTANTIAL SHAREHOLDERS 与 Controlling Shareholders 段的实际控制人身份表述。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 24 种取值 ('Individual': 4, 'Individual (Ms. Cao and Dr. Chen, acting in concert)': 1, '无单一控股股东；创始人朱忠远博士与单一最大股东 LAV USD': 1) |
| **BP** | `Controller economic interest at listing (%)` | 控制人上市时**经济权益**（持股比例），填小数。取 CONTROLLING/SUBSTANTIAL SHAREHOLDERS 表的持股百分比。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.47 / 中位数 0.41 / 区间 [0.18, 0.83] |
| **BQ** | `Controller voting rights at listing (%)` | 控制人上市时**投票权**比例，填小数。有 WVR（同股不同权）时与持股不同，取投票权那一列；无 WVR 通常与 BC 相同。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.47 / 中位数 0.46 / 区间 [0.18, 0.83] |
| **BR** | `Interest-bearing debt at year-1 end` | year-1 期末**总有息负债**（用与 col_V 相同的披露货币基本单位）。包含短期借款、长期借款、租赁负债及带息应付票据债券等带息债务总额，取 INDEBTEDNESS 表格的 Total 余额；不含应付账款等无息负债。必须换算为货币基本单位（乘表格千元/百万元乘数）。期末余额，不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 6,055,762,082.41 / 中位数 163,626,000.00 / 区间 [319,000.00, 137,584,403,000.00] |
| **BS** | `Technology commercialization stage` | 技术商业化阶段（如：研发阶段 / 小批量试产 / 商业化初期 / 规模商业化 / 已量产）。按 BUSINESS 与业务摘要里的产品状态表述填，不要按行业推测。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (14/27 (51.85%)) | 共 14 种取值 ('Commercialization stage (NCM and LFP products commercialized; LMFP, sodium-ion and semi-solid-state in pipeline)': 1, '尚无产品获批上市（临床开发阶段，未取得任何药品上市许可）': 1, 'Commercialized (products in mass production generating revenue during Track Record Period)': 1) |
| **BT** | `Debt repayment (% of planned net IPO proceeds)` | 计划净募资中用于**偿债**的比例，填小数。取 USE OF PROCEEDS 里用于偿还借款/债务的金额 ÷ 计划净募资额；没有该用途填 0。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (25/27 (92.59%)) | 均值 0.01 / 中位数 0.00 / 区间 [0.00, 0.20] |
| **BU** | `Listing board` | 上市板块（Main Board 主板） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Main Board': 27) |
| **BV** | `Share class` | 股份类别（如 H Shares / A Shares / Class A Ordinary Shares / Class B Ordinary Shares）。按招股书股本表的类别名称填。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 14 种取值 ('H Shares': 7, 'Ordinary Shares': 5, 'Ordinary shares': 4) |
| **BW** | `A+H issuer flag` | A+H 两地上市发行人标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 2 家 (7.4%), 0 (否): 25 家 |
| **BX** | `WVR flag` | 不同投票权/同股不同权架构标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 27 家 |
| **BY** | `Chapter 18A flag` | 第 18A 章未盈利生物科技公司标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 4 家 (14.8%), 0 (否): 23 家 |
| **BZ** | `Chapter 18C flag` | 第 18C 章特专科技公司标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 27 家 |
| **CA** | `Industry classification code` | 恒生行业分类 HSICS 6 位业务细分代码 | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 270,736.67 / 中位数 251,030.00 / 区间 [101,020.00, 702,030.00] |
| **CB** | `Industry classification system and version` | 行业分类系统与版本号 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('HSICS (Hang Seng Industry Classification System) 2026': 27) |
| **CC** | `Incorporation date` | 公司**法定注册成立日期**（dd/mm/yy）。必须优先取自 Statutory and General Information (Appendix V '1. Incorporation')、History & Development 或 Accountants' Report (附注 1)。严禁从 Definitions (释义) 章节取值（释义章节常有起草笔误或仅为前期筹备日）。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 1994-09-10 ~ 2024-02-27 |
| **CD** | `Firm age at IPO (years)` | 公司成立至上市年限（Lowry et al. 2017 Table 3.4 基础控制变量） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 12.03 / 中位数 11.19 / 区间 [1.34, 30.78] |
| **CE** | `Place of incorporation` | 公司注册成立法域（如 Cayman Islands, PRC 等） | 深蓝 | `string` | Ex-ante prospectus disclosure | Adequate (24/27 (88.89%)) | 共 2 种取值 ('PRC': 17, 'Cayman Islands': 7) |
| **CF** | `Principal place of business` | 主要营业地点（城市/国家），如 PRC、Hong Kong、Shenzhen, PRC。取公司资料或注册办事处段。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 27 种取值 ('No. 68 Xin'anjiang Road, Dongnan Community, Changshu, Jiangsu Province, the PRC': 1, 'Unit 301, Building 3, Zone B, Phase III, Biopharmaceutical Industrial Park, Pudong New Area, Shanghai, the PRC': 1, 'Room 208, 2/F, Block 3, No. 168 Shennan Road, Minhang District, Shanghai, PRC': 1) |
| **CG** | `Financial statement unit multiplier` | 财务报表基础货币乘数（千元/万元/百万元） | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (25/27 (92.59%)) | 均值 40,880.08 / 中位数 1,000.00 / 区间 [1.00, 1,000,000.00] |
| **CH** | `Accounting standard` | 财务报表采用的会计准则（如 IFRS Accounting Standards / HKFRS / ASBE / US GAAP）。取会计师报告开头声明。 | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 4 种取值 ('IFRS': 18, 'HKFRS': 5, 'IFRS Accounting Standards': 3) |
| **CI** | `Year-3 financial period start` | 往绩记录第三年前期起始日 | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2022-01-01 ~ 2022-05-01 |
| **CJ** | `Year-3 financial period end` | 往绩记录第三年前期截止日 | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2022-12-31 ~ 2023-04-30 |
| **CK** | `Year-2 financial period start` | 往绩记录第二年前期起始日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2023-01-01 ~ 2023-05-01 |
| **CL** | `Year-2 financial period end` | 往绩记录第二年前期截止日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2023-12-31 ~ 2024-04-30 |
| **CM** | `Year-1 financial period start` | 往绩记录最近一期起始日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2024-01-01 ~ 2024-05-01 |
| **CN** | `Year-1 net sales (original, pre-annualization)` | 最近一期营业收入原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | Adequate (26/27 (96.3%)) | 均值 18,478,921,551.92 / 中位数 1,664,171,500.00 / 区间 [0.00, 338,818,356,000.00] |
| **CO** | `Year-1 profit before tax (original)` | 最近一期税前利润原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | Adequate (26/27 (96.3%)) | 均值 3,285,304,939.88 / 中位数 42,481,500.00 / 区间 [-1,206,342,000.00, 69,500,124,000.00] |
| **CP** | `Year-1 profit for period (original)` | 最近一期净利润原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | Adequate (26/27 (96.3%)) | 均值 2,782,300,376.50 / 中位数 37,331,500.00 / 区间 [-1,246,389,000.00, 59,445,536,000.00] |
| **CQ** | `Subscription opening date` | 香港公开发售**开始认购日期**（dd/mm/yy）。取 EXPECTED TIMETABLE。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-04-03 ~ 2025-06-20 |
| **CR** | `Subscription closing date` | 香港公开发售**截止认购日期**（dd/mm/yy）。取 EXPECTED TIMETABLE。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-04-09 ~ 2025-06-25 |
| **CS** | `H shares after IPO (base; no options)` | 上市后**在港交所挂牌的股份数**（base，不含超额配售）。统一口径：① 内地 H 股发行人全部转换时 = 总股本；② 部分转换时 = 由未上市股转换的 H 股 + 新发 H 股（剩余未上市股不挂牌，不计入）；③ A+H 发行人 = 仅新发 H 股（A 股在沪深市场挂牌，不计入）；④ 开曼/境外发行人没有 H 股类别，其全部股份均在港交所挂牌，故 = 上市后已发行股份总数。即：本列恒等于「港交所挂牌的股份数」，四类结构可比。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 351,158,392.26 / 中位数 241,241,531.00 / 区间 [41,387,743.00, 1,439,372,739.00] |
| **CT** | `Gross profit in year-1` | year-1 **毛利**（用与 col_V 相同的披露货币基本单位）。取损益表的 Gross profit。强制期间锚定：必须与 col_AT 严格同期间！若 col_AT 为中期报告期（如截至 2025 年 6 月 30 日或 9 月 30 日止期间），必须严格提取该中期报告期对应列的原值，绝对严禁错采前一完整财年（FY2024）的数值。必须换算为货币基本单位（乘表格千元/百万元乘数）。不年化——手册明确仅 year-1 销售/税前利润/净利润年化，毛利不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | Adequate (25/27 (92.59%)) | 均值 2,927,078,795.08 / 中位数 364,480,000.00 / 区间 [-85,058,000.00, 24,136,428,000.00] |
| **CU** | `Capital expenditure in year-1` | year-1 **资本开支**（用与 col_V 相同的披露货币基本单位）。取现金流量表“购建物业、厂房及设备”或 CAPITAL EXPENDITURE 段。强制期间锚定：必须与 col_AT 严格同期间！若 col_AT 为中期报告期（如截至 2025 年 6 月 30 日或 9 月 30 日止期间），必须严格提取该中期报告期实际资本开支原值，绝对严禁错采前一完整财年（FY2024）数值。必须换算为货币基本单位（乘表格千元/百万元乘数）。不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 696,683,676.59 / 中位数 49,959,000.00 / 区间 [187,000.00, 10,342,606,000.00] |
| **CV** | `Audit opinion (year-1)` | year-1 **审计意见类型**（如 无保留意见 / Unqualified opinion / Qualified opinion）。取会计师报告的审计意见段。 | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 14 种取值 ('Unqualified opinion (true and fair view)': 8, 'Unqualified': 5, 'Unqualified (true and fair view)': 3) |
| **CW** | `Listing expenses (HK$)` | **总上市费用**（HK$ 基本单位，含承销佣金与其他开支）。取 UNDERWRITING COMMISSIONS AND LISTING EXPENSES 段的合计。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 102,006,938.96 / 中位数 87,396,352.00 / 区间 [36,300,000.00, 288,300,000.00] |
| **CX** | `Cornerstone investor names` | Cornerstone investor names | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (25/27 (92.59%)) | 共 25 种取值 ('Jiangsu Mixed Ownership Reform Fund; Suzhou High-end Equipment Fund; Southeast Investment Holding': 1, 'BioNTech SE; LAV Star Opportunities Limited; Lake Bleu Prime Healthcare Master Fund Limited; Lake Bleu Innovation Healthcare Master Fund Limited; TruMed Healthcare Master Fund; ABS Direct Equity Fund LLC Asia Series 11; TruMed Health Innovation Fund LP; Fullgoal Asset Management (HK) Limited; Fullgoal Fund Management Co., Ltd.; E Fund Management Co., Ltd.; E Fund Management (Hong Kong) Co., Ltd.; China Universal Asset Management Co., Ltd.; Panjing Harbourview Investment Fund; MY Asian Opportunities Master Fund, L.P.; Emerging Markets Healthcare Partners LLC; Worldwide Healthcare Partners LLC; Suzhou Suchuang Biomedical Health Venture Capital Fund Partnership (Limited Partnership)': 1, 'HongKong Xinwei Electronic Co., Limited (香港欣威電子有限公司); Changfeng Growth Equity Fund OFC (長風成長股票開放式基金型公司)': 1) |
| **CY** | `Final cornerstone allocation (% of base offer)` | Final cornerstone allocation (% of base offer) | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 0.37 / 中位数 0.41 / 区间 [0.00, 0.64] |
| **CZ** | `Earliest cornerstone unlock date (dd/mm/yy)` | 基石投资者最早解禁日期 | 深蓝 | `date` | Post-IPO lockup expiration events | Adequate (25/27 (92.59%)) | 区间: 2025-10-14 ~ 2025-12-30 |
| **DA** | `Subscription Ratio (times)` | Subscription Ratio (times) | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 643.34 / 中位数 274.44 / 区间 [3.50, 3,616.83] |
| **DB** | `Public applicants` | Public applicants | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 93,614.19 / 中位数 48,554.00 / 区间 [5,998.00, 379,668.00] |
| **DC** | `Public valid applied shares` | Public valid applied shares | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 3,045,401,097.41 / 中位数 872,162,250.00 / 区间 [14,307,380.00, 18,864,853,500.00] |
| **DD** | `Public subscription original wording` | Public subscription original wording | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 27 种取值 ('Subscription level 3.51 times': 1, 'Subscription level 115.14 times': 1, 'Subscription level 198.72 times': 1) |
| **DE** | `Pricing date` | Pricing date | 深蓝 | `date` | Ex-ante prospectus disclosure | Adequate (16/27 (59.26%)) | 区间: 2025-04-11 ~ 2025-06-26 |
| **DF** | `Allotment announcement date` | Allotment announcement date | 深蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-04-11 ~ 2025-06-27 |
| **DG** | `Final global offering shares (before over-allotment)` | Final global offering shares (before over-allotment) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 91,457,848.89 / 中位数 46,620,000.00 / 区间 [1,560,980.00, 414,379,500.00] |
| **DH** | `Final public offer shares` | Final public offer shares | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 24,806,961.85 / 中位数 12,179,200.00 / 区间 [624,400.00, 109,810,600.00] |
| **DI** | `Final placing shares` | Final placing shares | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 66,650,887.04 / 中位数 30,925,000.00 / 区间 [936,580.00, 304,568,900.00] |
| **DJ** | `Over-allotment shares actually issued` | Over-allotment shares actually issued | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 5,864,722.96 / 中位数 0.00 / 区间 [0.00, 62,156,900.00] |
| **DK** | `Greenshoe exercise rate (%)` | 绿鞋实际行使比例（Ellis et al. 2000 超额配售执行度与价格支持） | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.34 / 中位数 0.00 / 区间 [0.00, 1.00] |
| **DL** | `Actual clawback / reallocation description` | Actual clawback / reallocation description | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 27 种取值 ('Claw-back triggered No; no reallocation, final HKPO stays at 12,152,400 (approximately 10% of the Global Offering)': 1, 'Claw-back triggered: Yes; 6,028,600 Offer Shares reallocated from the International Offering to the Hong Kong Public Offering; final Hong Kong Public Offering 7,535,800 Shares (approximately 43.48% of the Global Offering)': 1, '1,300,000 Offer Shares reallocated from the International Offering to the Hong Kong Public Offering; final number of Offer Shares under the Hong Kong Public Offering adjusted to 2,600,000 (20% of the Global Offering) and International Offering reduced to 10,400,000 (80%), because the International Offer Shares were undersubscribed (0.92 times) and the Hong Kong Public Offer Shares were oversubscribed.': 1) |
| **DM** | `Net IPO proceeds to issuer (HK$)` | Net IPO proceeds to issuer (HK$) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 2,893,318,518.52 / 中位数 629,950,000.00 / 区间 [131,200,000.00, 35,331,200,000.00] |
| **DN** | `Public shareholding at listing (%)` | Public shareholding at listing (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Adequate (26/27 (96.3%)) | 均值 0.30 / 中位数 0.26 / 区间 [0.03, 0.73] |
| **DO** | `Share base used for both public shareholding ratios` | Share base used for both public shareholding ratios | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 1,194,351,090.85 / 中位数 385,955,532.00 / 区间 [70,953,453.00, 6,603,522,074.00] |
| **DP** | `Unrestricted public shareholding at listing (%)` | Unrestricted public shareholding at listing (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.08 / 中位数 0.08 / 区间 [0.01, 0.25] |
| **DQ** | `Free float denominator description` | Free float denominator description | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 27 种取值 ('分母为上市时已发行股份总数 2,508,500,103 股（假设非上市股份转换为 H 股已完成，且超额配售权未行使）': 1, '分母为上市时已发行股份总数85,436,464股（含发售规模调整权全额行使、不含超额配售权）；公告仅披露公众持股62,253,243股(72.86%)，未单列自由流通量，自由流通股数=全球发售17,332,300股−基石获配5,341,800股=11,990,500股': 1, 'Denominator = total number of issued Shares upon Listing (379,651,762 Shares, i.e. H Shares plus Unlisted Shares converted into H Shares upon Listing), the base used for the 44.23% public float statement.': 1) |
| **DR** | `Free float denominator shares` | Free float denominator shares | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 1,194,351,090.85 / 中位数 385,955,532.00 / 区间 [70,953,453.00, 6,603,522,074.00] |
| **DS** | `HSI return over 20 trading days before prospectus (%)` | 招股日前 20 个交易日恒生指数累计收益率 (%) | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 0.03 / 中位数 0.02 / 区间 [-0.08, 0.15] |
| **DT** | `HK ordinary IPO count in 90 calendar days before prospectus` | 招股日前 90 个自然日香港普通主板 IPO 上市数量 | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 15.44 / 中位数 17.00 / 区间 [9.00, 19.00] |
| **DU** | `1-month HIBOR before prospectus (%)` | 招股日前一交易日香港银行同业拆借 1 个月 HIBOR 利率 (%) | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.01 / 中位数 0.01 / 区间 [0.01, 0.04] |
| **DV** | `Banking system aggregate balance before prospectus (HK$)` | 招股日前一交易日香港银行体系总结余 (HK$) | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 149,227,740,740.74 / 中位数 173,483,000,000.00 / 区间 [44,547,000,000.00, 174,100,000,000.00] |
| **DW** | `First trading day closing price (HK$)` | 首日上市二级市场收盘价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 52.17 / 中位数 23.50 / 区间 [2.26, 296.40] |
| **DX** | `First-day return / Underpricing (%)` | 上市首日抑价率 / 初始收益率（Rock 1986 / Ritter 1984 核心被解释变量） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 0.18 / 中位数 0.21 / 区间 [-0.30, 1.17] |
| **DY** | `Money left on the table (HK$)` | 留在桌面上的财富 / 抑价转移财富总额（Loughran & Ritter 2002 前景理论指标） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 362,494,083.14 / 中位数 89,700,000.00 / 区间 [-371,670,224.40, 4,417,693,102.40] |
| **DZ** | `First trading day opening price (HK$)` | 首日上市二级市场开盘价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 49.08 / 中位数 22.20 / 区间 [2.44, 285.38] |
| **EA** | `First trading day high (HK$)` | 首日上市二级市场盘中最高价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 57.10 / 中位数 27.50 / 区间 [2.65, 319.80] |
| **EB** | `First trading day low (HK$)` | 首日上市二级市场盘中最低价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 45.82 / 中位数 22.10 / 区间 [2.11, 280.38] |
| **EC** | `First trading day volume (shares)` | 首日上市二级市场全天成交量（股） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 36,878,785.04 / 中位数 21,324,400.00 / 区间 [803,070.00, 173,642,999.00] |
| **ED** | `First-day flipping ratio (%)` | 首日短线翻转抛售率 / 成交量占全球发售比例（Aggarwal 2003 机构抛售假说） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 0.53 / 中位数 0.51 / 区间 [0.03, 1.36] |
| **EE** | `First trading day turnover (HK$)` | 首日上市二级市场全天成交金额 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 1,079,654,366.67 / 中位数 274,942,900.00 / 区间 [27,167,900.00, 8,284,435,400.00] |
| **EF** | `Offer mechanism` | 适用发售与回拨制度（2025-08-04 前 PN18/18C.09；之后 Mechanism A/B） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 2 种取值 ('PN18 statutory clawback': 25, 'Chapter 18C.09 clawback': 2) |
| **EG** | `Applicable IPO rules / transition basis` | 适用之上市规则过渡基准（FINI 改革规则） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('FINI (from 22/11/2023)': 27) |
| **EH** | `Company Chinese Name` | Company Chinese Name | 浅蓝 | `string` | Ex-ante prospectus disclosure | Adequate (24/27 (88.89%)) | 共 24 种取值 ('江苏正力新能电池技术股份有限公司': 1, '映恩生物': 1, '博雷顿科技股份公司': 1) |
| **EI** | `Current listing status` | 当前挂牌存续状态 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 2 种取值 ('Active': 24, 'No recent trading (verify status)': 3) |
| **EJ** | `1-month post-IPO close price (HK$)` | 第20个交易日收盘价（窗口成熟后填报） | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 59.89 / 中位数 27.41 / 区间 [1.96, 528.50] |
| **EK** | `1-month BHR from Day-1 close (%)` | 由首日收盘至第20个交易日的买入持有收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.02 / 中位数 -0.03 / 区间 [-0.41, 0.78] |
| **EL** | `1-month total return from offer price (%)` | 由发售价至第20个交易日的累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.22 / 中位数 0.13 / 区间 [-0.42, 1.58] |
| **EM** | `1-month HSI return (%)` | 同期恒生指数累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.04 / 中位数 0.04 / 区间 [-0.02, 0.10] |
| **EN** | `1-month HSTECH return (%)` | 同期恒生科技指数累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.03 / 中位数 0.06 / 区间 [-0.03, 0.08] |
| **EO** | `1-month wealth relative vs HSI` | 一个月相对恒指财富比 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.98 / 中位数 0.96 / 区间 [0.59, 1.68] |
| **EP** | `1-month wealth relative vs HSTECH` | 一个月相对恒生科技指数财富比 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.98 / 中位数 0.97 / 区间 [0.60, 1.67] |
| **EQ** | `1-month average daily turnover (HK$)` | 上市后首20个交易日日均成交额 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 171,277,021.00 / 中位数 43,185,150.00 / 区间 [8,554,624.50, 2,078,148,718.50] |
| **ER** | `6-month post-IPO close price (HK$)` | 六个月目标日后首个交易日收盘价（窗口成熟后填报） | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 70.41 / 中位数 24.92 / 区间 [2.04, 473.49] |
| **ES** | `6-month BHR from Day-1 close (%)` | 由首日收盘至六个月目标交易日的买入持有收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.35 / 中位数 -0.08 / 区间 [-0.63, 5.06] |
| **ET** | `6-month total return from offer price (%)` | 由发售价至六个月目标交易日的累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.65 / 中位数 0.02 / 区间 [-0.69, 9.51] |
| **EU** | `6-month HSI return (%)` | 同期恒生指数累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.10 / 中位数 0.09 / 区间 [0.05, 0.21] |
| **EV** | `6-month HSTECH return (%)` | 同期恒生科技指数累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.07 / 中位数 0.06 / 区间 [0.02, 0.22] |
| **EW** | `6-month wealth relative vs HSI` | 六个月相对恒指财富比 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 1.23 / 中位数 0.86 / 区间 [0.35, 5.46] |
| **EX** | `6-month wealth relative vs HSTECH` | 六个月相对恒生科技指数财富比 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 1.26 / 中位数 0.88 / 区间 [0.36, 5.61] |
| **EY** | `6-month average daily turnover (HK$)` | 六个月目标日前20个交易日日均成交额 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 130,154,338.57 / 中位数 27,920,060.00 / 区间 [146,460.00, 1,269,077,714.50] |
| **EZ** | `Liquidity decay ratio (6M vs Day-1 turnover)` | 六个月窗口日均成交额相对首日成交额比率 | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.26 / 中位数 0.07 / 区间 [0.00, 3.99] |
| **FA** | `1-year post-IPO return (%) [Reserved]` | 一年期收益率预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/27 (0.0%)) | 全部缺失 |
| **FB** | `1-year wealth relative vs HSI [Reserved]` | 一年期相对恒指财富比预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/27 (0.0%)) | 全部缺失 |
| **FC** | `3-year post-IPO return (%) [Reserved]` | 三年期收益率预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/27 (0.0%)) | 全部缺失 |
| **FD** | `3-year wealth relative vs HSI [Reserved]` | 三年期相对恒指财富比预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/27 (0.0%)) | 全部缺失 |
| **FE** | `18A/18C regulatory milestone status` | 18A/18C 监管路径与商业化里程碑状态 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 2 种取值 ('Standard': 23, '18A (Biotech / B-tag)': 4) |
| **FF** | `Stabilizing manager` | 官方指定价格稳定经理人名称 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('China International Capital Corporation / Sponsor-OC': 27) |
| **FG** | `Stabilization period end date` | 法定30天稳价期结束日期 | 深蓝 | `string` | Post-IPO 30-day stabilization window | 100% 完备 | 共 15 种取值 ('2025-07-10': 3, '2025-07-23': 3, '2025-07-26': 3) |
| **FH** | `Stabilization purchases occurred` | 稳价期内是否发生二级市场托单购买 (1=是, 0=否) | 深蓝 | `boolean` | Post-IPO 30-day stabilization window | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 27 家 |
| **FI** | `Over-allocation shares` | 国际配售超额配售股份数量（股） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **FJ** | `Over-allocation (% of base offer)` | 超额配售股数占基础发售股份比例 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 0.15 / 中位数 0.15 / 区间 [0.15, 0.15] |
| **FK** | `Over-allotment option exercise date` | 超额配售权实际行使公告日期 | 深蓝 | `string` | Post-IPO 30-day stabilization window | 100% 完备 | 共 15 种取值 ('2025-07-10': 3, '2025-07-23': 3, '2025-07-26': 3) |
| **FL** | `Shares issued under over-allotment option` | 超额配售权最终发行股份数量（股） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **FM** | `Over-allotment exercise percentage (%)` | 超额配售权行使比例 (行使股数/超额配售上限, %) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **FN** | `Post-stabilization cliff return [-5, +5] (%)` | 稳价期结束日前后[-5, +5]交易日累计收益率（断崖效应测试） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 0.04 / 中位数 0.01 / 区间 [-0.24, 0.32] |
| **FO** | `Post-stabilization 20-day return [0, +20] (%)` | 稳价期结束后20个交易日累计收益率 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 0.19 / 中位数 0.07 / 区间 [-0.12, 0.91] |
| **FP** | `Post-stabilization volume decay ratio (%)` | 稳价结束后20日均成交额相对稳价期内之比 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 0.52 / 中位数 0.36 / 区间 [0.06, 1.91] |
| **FQ** | `Day-5 BHR from Day-1 close (%)` | 挂牌首周 (T+5交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 -0.02 / 中位数 -0.01 / 区间 [-0.30, 0.34] |
| **FR** | `Day-5 wealth relative vs HSI` | 挂牌首周对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 0.98 / 中位数 0.98 / 区间 [0.70, 1.36] |
| **FS** | `Day-20 BHR from Day-1 close (%)` | 首月 (T+20交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 0.02 / 中位数 -0.03 / 区间 [-0.41, 0.78] |
| **FT** | `Day-20 wealth relative vs HSI` | 首月对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 0.98 / 中位数 0.96 / 区间 [0.59, 1.68] |
| **FU** | `3-month BHR from Day-1 close (%)` | 首季 (T+63交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 0.46 / 中位数 0.24 / 区间 [-0.46, 6.80] |
| **FV** | `3-month wealth relative vs HSI` | 首季对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 1.33 / 中位数 1.08 / 区间 [0.51, 6.96] |
| **FW** | `3-month wealth relative vs HSTECH` | 首季对标恒科财富相对比 (WR_HSTECH) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 1.28 / 中位数 1.15 / 区间 [0.51, 6.45] |
| **FX** | `3-month average daily turnover (HK$)` | 首季度日均成交金额 (港元) | 深蓝 | `numeric` | Aftermarket event horizon window | 100% 完备 | 均值 136,301,095.44 / 中位数 34,887,228.57 / 区间 [3,405,488.73, 1,372,611,588.89] |
| **FY** | `Amihud illiquidity (6M mean)` | 上市前6个月日均 Amihud (2002) 非流动性指标 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.01 / 中位数 0.00 / 区间 [0.00, 0.07] |
| **FZ** | `Zero-volume days count (first 6M)` | 上市前6个月零成交量交易日天数 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.04 / 中位数 0.00 / 区间 [0.00, 1.00] |
| **GA** | `Return volatility (first 6M daily std dev, %)` | 上市前6个月日度收益率标准差 (波动率, %) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.05 / 中位数 0.05 / 区间 [0.01, 0.17] |
| **GB** | `Maximum drawdown (first 6M, %)` | 上市前6个月二级市场最大回撤幅度 (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.47 / 中位数 0.42 / 区间 [0.15, 0.83] |
| **GC** | `Controlling shareholder 6-month disposal lockup expiry date` | 控股股东首阶段6个月绝对禁售期满日 | 深蓝 | `string` | Post-IPO lockup expiration events | 100% 完备 | 共 15 种取值 ('2025-12-10': 3, '2025-12-23': 3, '2025-12-26': 3) |
| **GD** | `Controlling shareholder 12-month cessation of control expiry date` | 控股股东次阶段12个月控制权锁定到期日 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 15 种取值 ('2026-06-10': 3, '2026-06-23': 3, '2026-06-26': 3) |
| **GE** | `Cornerstone unlock CAR [-5, +5] (%)` | 基石投资者解禁日前后[-5, +5]交易日累计超额收益 (CAR vs HSI) | 深蓝 | `numeric` | Post-IPO lockup expiration events | 100% 完备 | 均值 -0.04 / 中位数 -0.00 / 区间 [-0.37, 0.22] |
| **GF** | `Cornerstone unlock CAR [-20, +20] (%)` | 基石投资者解禁日前后[-20, +20]交易日累计超额收益 (CAR vs HSI) | 深蓝 | `numeric` | Post-IPO lockup expiration events | 100% 完备 | 均值 -0.14 / 中位数 -0.10 / 区间 [-0.83, 0.48] |
| **GG** | `Cornerstone unlock volume shock ratio` | 基石解禁后20日均换手额相对解禁前20日换手额之比 | 深蓝 | `numeric` | Post-IPO lockup expiration events | 100% 完备 | 均值 1.95 / 中位数 1.33 / 区间 [0.36, 12.22] |
| **GH** | `Lead sponsor name` | 独家/联席牵头保荐人英文全称 | 深蓝 | `string` | Prospectus syndicate structure | 100% 完备 | 共 1 种取值 ('China International Capital Corporation / Sponsor-OC': 27) |
| **GI** | `Joint sponsor count` | 保荐人总家数 (独家=1, 联席=2+) | 深蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **GJ** | `Sponsor commercial bank affiliate flag` | 保荐人是否属于商业银行系金融机构 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus syndicate structure | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 27 家 |
| **GK** | `Underwriting base commission rate (%)` | 承销基础佣金费率 (%) | 深蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.03 / 中位数 0.03 / 区间 [0.03, 0.03] |
| **GL** | `Underwriting discretionary incentive fee rate (%)` | 承销酌情奖励费率估算 (%) | 深蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.01 / 中位数 0.01 / 区间 [0.01, 0.01] |
| **GM** | `Total underwriting fee rate (%)` | 承销总费率估算 (基础+奖励, %) | 深蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.04 / 中位数 0.04 / 区间 [0.04, 0.04] |
| **GN** | `Cornerstone investor count` | 基石投资者机构总家数 | 深蓝 | `numeric` | Prospectus / allotment institutional network | 100% 完备 | 均值 4.00 / 中位数 4.00 / 区间 [4.00, 4.00] |
| **GO** | `Cornerstone state-owned presence flag` | 基石投资者中是否包含国资/地方政府基金 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 27 家 |
| **GP** | `Crossover fund presence flag` | 是否包含兼具 Pre-IPO 与基石双重身份的跨界基金 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 27 家 |
| **GQ** | `Pre-IPO institutional investor count` | 主要 Pre-IPO 投资机构总数 | 深蓝 | `numeric` | Prospectus / allotment institutional network | 100% 完备 | 均值 6.00 / 中位数 6.00 / 区间 [6.00, 6.00] |
| **GR** | `Pre-IPO state-owned backing flag` | Pre-IPO 股东中是否包含国资机构 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 27 家 |
| **GS** | `FINI digital settlement regime` | 结算监管体制 (POST_FINI / PRE_FINI) | 深蓝 | `string` | Listing date regulatory regime | 100% 完备 | 共 1 种取值 ('POST_FINI': 27) |
| **GT** | `2025 pricing reform regime` | 发售与定价机制改革体制 (POST_2025_REFORM / PRE_2025_REFORM) | 深蓝 | `string` | Listing date regulatory regime | 100% 完备 | 共 1 种取值 ('POST_2025_REFORM': 27) |

---

## 三、计量软件导入指引 (Stata / Python)

配套清洗数据文件：`out/HKIPO-MB2025Q2_clean.csv`（编码：UTF-8 with BOM）。

### 1. Stata
```stata
* 导入纯净版 CSV 数据
import delimited "out/HKIPO-MB2025Q2_clean.csv", clear bindquote(strict) varnames(1)
describe
summarize
```

### 2. Python (pandas)
```python
import pandas as pd
df = pd.read_csv("out/HKIPO-MB2025Q2_clean.csv")
print(df.info())
print(df.describe())
```

---
*本数据代码本由 HK IPO Prospectus Pipeline 自动化分析引擎生成。*
