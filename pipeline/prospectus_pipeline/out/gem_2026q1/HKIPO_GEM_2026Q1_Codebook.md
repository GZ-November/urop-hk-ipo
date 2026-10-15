# 香港主板 2026 Q1 IPO 学术研究数据变量代码本 (Data Codebook)

- **样本规模 (N)**：1 家香港联交所 GEM 新上市公司
- **变量总数 (K)**：195 维完整跨学科指标
- **数据层级划分**：浅绿官方基础 (11 列) + 浅蓝招股书披露 (76 列) + 深蓝配发及外部衍生 (108 列)
- **生成时间**：2026-10-16 01:45:58 | **数据基准**：`HKIPO-GEM2026Q1.xlsx` (Sheet: NLR)

---

## 一、变量层级与来源体系导览

| 数据层级 | 覆盖范围 | 列数 | 核心特征与学术用途 |
|---|---|---|---|
| **浅绿 (HKEX 官方来源)** | 列 A–K | 11 列 | 港交所新上市报告官方确证指标：上市编号、代码、保荐人、会计师、公开发售及国际发售募资额、最终定价。 |
| **浅蓝 (招股书全量来源)** | 招股书法定披露与Pre-IPO结构 | 76 列 | 发行人招股书披露：资本结构、发售价区间、Pre-IPO VC/PE 投资背景与治理席位、近三年财务与业务指标。 |
| **深蓝 (配发及外部数据)** | 配发公告与外部市场数据 | 108 列 | 发行结果与市场宏观：基石投资者最终获配及禁售期、回拨机制、超购倍数、自由流通量、首日二级市场表现、恒指收益率、HIBOR、总结余、监管分类。 |

---

## 二、195 维全量变量字典详细清单 (Codebook)

| 列 | 变量英文名 (Variable Header) | 中文口径释义 | 数据层级 | 数据类型 | 时点约定 | 样本状态 (填报率) | 描述性统计 / 分布特征 |
|---|---|---|---|---|---|---|---|
| **A** | `HKEx file# of the year` | 港交所年度申请编号 | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 1.00 / 中位数 1.00 / 区间 [1.00, 1.00] |
| **B** | `Stock Code` | 股份代号（四位港股代码，如 6082.HK） | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('8610.HK': 1) |
| **C** | `Company Name at time of listing` | 公司上市时法定英文名称 | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('BBSB International Limited': 1) |
| **D** | `Date of Prospectus (dd/mm/yy)` | 招股书刊发日期 | 浅绿 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-12-31 ~ 2025-12-31 |
| **E** | `Date of Listing (dd/mm/yy)` | 正式挂牌上市交易日期 | 浅绿 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2026-01-13 ~ 2026-01-13 |
| **F** | `Sponsor(s)` | 独家/联席保荐人名单 | 浅绿 | `string` | Prospectus syndicate structure | 100% 完备 | 共 1 种取值 ('Lego Corporate Finance Limited': 1) |
| **G** | `Reporting Accountants` | 申报会计师事务所 | 浅绿 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('BDO Limited': 1) |
| **H** | `Valuer(s)` | 独立物业或资产估值师 | 浅绿 | `string` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **I** | `Funds Raised HK (a)` | 香港公开发售募资额 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **J** | `Funds Raised Int.(b)` | 国际配售募资额 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **K** | `IPO Subscription Price (HK$)` | 最终发售定价 (HK$) | 浅绿 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.60 / 中位数 0.60 / 区间 [0.60, 0.60] |
| **L** | `Total (without option)` | Total (without option) | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 500,000,000.00 / 中位数 500,000,000.00 / 区间 [500,000,000.00, 500,000,000.00] |
| **M** | `Global Offering (without option)` | Global Offering (without option) | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 125,000,000.00 / 中位数 125,000,000.00 / 区间 [125,000,000.00, 125,000,000.00] |
| **N** | `Number of offer shares under the capitalization Issue` | 全球发售完成前的已发行股份总数。本数据集口径：一律填 L − M（Total 减去全球发售股数），即使招股书未披露「资本化发行」也必须照填，不得留 NaN。用于满足恒等式 L = N + Q。2026Q1 成品工作簿 38 家公司全部取 L − M，Q2 必须同口径。数值只取权威 SHARE CAPITAL 汇总表与封面，禁止取「历史沿革／资本化发行沿革」段落。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 375,000,000.00 / 中位数 375,000,000.00 / 区间 [375,000,000.00, 375,000,000.00] |
| **O** | `Number of offer shares under Capitalization Rest` | 与 col_N 同口径：一律填 L − M（全球发售完成前的已发行股份总数），即使招股书未披露「资本化转换」也必须照填，不得留 NaN。用于满足恒等式 L = O + M。2026Q1 成品 38 家全部为 L − M。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 375,000,000.00 / 中位数 375,000,000.00 / 区间 [375,000,000.00, 375,000,000.00] |
| **P** | `Sale Shares` | 老股出售（Sale Shares）数量。若为全部新股的 Offer for Subscription（无 Selling Shareholder），填数字 0，不得留 NaN，用于满足恒等式 M = Q + P。判据：封面／股本汇总表无 Sale Shares 行，且全文无 Selling Shareholder 披露。2026Q1 成品 38 家全部为 0。若确有老股出售，按招股书披露填写。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **Q** | `New shares` | New shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 125,000,000.00 / 中位数 125,000,000.00 / 区间 [125,000,000.00, 125,000,000.00] |
| **R** | `Placing Shares` | Placing Shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 112,500,000.00 / 中位数 112,500,000.00 / 区间 [112,500,000.00, 112,500,000.00] |
| **S** | `Public Offer shares` | Public Offer shares | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 12,500,000.00 / 中位数 12,500,000.00 / 区间 [12,500,000.00, 12,500,000.00] |
| **T** | `Maximum Offer Price` | Maximum Offer Price | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.70 / 中位数 0.70 / 区间 [0.70, 0.70] |
| **U** | `Minimum Offer Price` | Minimum Offer Price | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.60 / 中位数 0.60 / 区间 [0.60, 0.60] |
| **V** | `Filing price revision (%)` | 发售定价偏离询价区间中点幅度（Hanley 1993 动态信息提取，固定价格发售为 0.00%） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 -0.08 / 中位数 -0.08 / 区间 [-0.08, -0.08] |
| **W** | `Filing range width (%)` | 询价区间相对宽度（Beatty & Ritter 1986 事前估值不确定性，固定价格发售为 0.00%） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.15 / 中位数 0.15 / 区间 [0.15, 0.15] |
| **X** | `Pricing position in filing range` | 定价落点分类体系（Fixed price / Above range / At high / Midpoint / Within range / At low / Below range） | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('At low': 1) |
| **Y** | `currency in financial information` | currency in financial information | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 1 种取值 ('MYR': 1) |
| **Z** | `total assets in year-3 (3 years before IPO)` | total assets in year-3 (3 years before IPO) | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 113,572,000.00 / 中位数 113,572,000.00 / 区间 [113,572,000.00, 113,572,000.00] |
| **AA** | `total assets in year-2` | total assets in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 109,044,000.00 / 中位数 109,044,000.00 / 区间 [109,044,000.00, 109,044,000.00] |
| **AB** | `total assets in year-1` | total assets in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 114,046,000.00 / 中位数 114,046,000.00 / 区间 [114,046,000.00, 114,046,000.00] |
| **AC** | `total equity in year-3` | total equity in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 63,611,000.00 / 中位数 63,611,000.00 / 区间 [63,611,000.00, 63,611,000.00] |
| **AD** | `total equity in year-2` | total equity in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 53,800,000.00 / 中位数 53,800,000.00 / 区间 [53,800,000.00, 53,800,000.00] |
| **AE** | `total equity in year-1` | total equity in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 57,001,000.00 / 中位数 57,001,000.00 / 区间 [57,001,000.00, 57,001,000.00] |
| **AF** | `total liability in year-3` | total liability in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 49,961,000.00 / 中位数 49,961,000.00 / 区间 [49,961,000.00, 49,961,000.00] |
| **AG** | `total liability in year-2` | total liability in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 55,244,000.00 / 中位数 55,244,000.00 / 区间 [55,244,000.00, 55,244,000.00] |
| **AH** | `total liability in year-1` | total liability in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 57,045,000.00 / 中位数 57,045,000.00 / 区间 [57,045,000.00, 57,045,000.00] |
| **AI** | `Net sales in year-3` | Net sales in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 76,757,000.00 / 中位数 76,757,000.00 / 区间 [76,757,000.00, 76,757,000.00] |
| **AJ** | `Net sales in year-2` | Net sales in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 133,002,000.00 / 中位数 133,002,000.00 / 区间 [133,002,000.00, 133,002,000.00] |
| **AK** | `Net sales in year-1` | Net sales in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 147,972,000.00 / 中位数 147,972,000.00 / 区间 [147,972,000.00, 147,972,000.00] |
| **AL** | `Profit before tax in year-3` | Profit before tax in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 -13,098,000.00 / 中位数 -13,098,000.00 / 区间 [-13,098,000.00, -13,098,000.00] |
| **AM** | `Profit before tax in year-2` | Profit before tax in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 33,273,000.00 / 中位数 33,273,000.00 / 区间 [33,273,000.00, 33,273,000.00] |
| **AN** | `Profit before tax in year-1` | Profit before tax in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 11,886,000.00 / 中位数 11,886,000.00 / 区间 [11,886,000.00, 11,886,000.00] |
| **AO** | `Profit for the year in year-3` | Profit for the year in year-3 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 -14,460,000.00 / 中位数 -14,460,000.00 / 区间 [-14,460,000.00, -14,460,000.00] |
| **AP** | `Profit for the year in year-2` | Profit for the year in year-2 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 26,189,000.00 / 中位数 26,189,000.00 / 区间 [26,189,000.00, 26,189,000.00] |
| **AQ** | `Profit for the year in year-1` | Profit for the year in year-1 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 6,402,000.00 / 中位数 6,402,000.00 / 区间 [6,402,000.00, 6,402,000.00] |
| **AR** | `Underwriting Commission (% of fund raised HK (a)` | Underwriting Commission (% of fund raised HK (a) | 浅蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.05 / 中位数 0.05 / 区间 [0.05, 0.05] |
| **AS** | `Underwriting Commission (% of fund raised Int.(b)` | Underwriting Commission (% of fund raised Int.(b) | 浅蓝 | `numeric` | Prospectus syndicate structure | 100% 完备 | 均值 0.05 / 中位数 0.05 / 区间 [0.05, 0.05] |
| **AT** | `Over-allotment Option (%)` | Over-allotment Option (%) | 浅蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 0.15 / 中位数 0.15 / 区间 [0.15, 0.15] |
| **AU** | `Principal business / industry` | Principal business / industry | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Civil engineering contractor in Malaysia specialising in bridge engineering services as a subcontractor for large-scale transportation infrastructure engineering projects': 1) |
| **AV** | `Listing route / applicable chapter` | Listing route / applicable chapter | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Listing on GEM of the Stock Exchange by way of Share Offer (Public Offer and Placing)': 1) |
| **AW** | `Year-1 financial period end (dd/mm/yy)` | Year-1 financial period end (dd/mm/yy) | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2025-06-30 ~ 2025-06-30 |
| **AX** | `Operating cash flow in year-1 (before annualization)` | Operating cash flow in year-1 (before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 -3,480,000.00 / 中位数 -3,480,000.00 / 区间 [-3,480,000.00, -3,480,000.00] |
| **AY** | `Cash and cash equivalents at year-1 end` | Cash and cash equivalents at year-1 end | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 9,086,000.00 / 中位数 9,086,000.00 / 区间 [9,086,000.00, 9,086,000.00] |
| **AZ** | `R&D expensed in year-1 (before annualization)` | R&D expensed in year-1 (before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **BA** | `Development costs capitalized in year-1 (additions, before annualization)` | Development costs capitalized in year-1 (additions, before annualization) | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **BB** | `Top 5 customers (% of year-1 revenue)` | Top 5 customers (% of year-1 revenue) | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 1.00 / 中位数 1.00 / 区间 [1.00, 1.00] |
| **BC** | `Comments / Annualization factor` | 最近一期财务数据对应的年化因子与口径说明 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 0.50 / 中位数 0.50 / 区间 [0.50, 0.50] |
| **BD** | `Pre-IPO VC/PE backing (1=yes; 0=no)` | 是否引入 Pre-IPO VC/PE 投资者：1=有，0=无。看 HISTORY AND DEVELOPMENT — Pre-IPO Investments 与 SUBSTANTIAL SHAREHOLDERS 名单；只要有专业投资机构（VC/PE/产业基金）在上市前入股即 1。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **BE** | `Pre-IPO VC backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。早期/成长期专业风险投资基金为 1；未找到证据不等于 0，无法确认时填 NaN。分类依据须在本字段 quote 中体现。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **BF** | `Pre-IPO PE backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。中晚期私募股权基金或并购基金为 1；未找到证据不等于 0，无法确认时填 NaN。分类依据须在本字段 quote 中体现。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **BG** | `Pre-IPO CVC backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。发行人产业股东须有战略投资/企业风投关系依据才归 CVC；普通产业股东不能自动算 CVC。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **BH** | `Pre-IPO State/Gov backing (1=yes; 0=no)` | 只根据本公司招股书披露的上市前投资判定。有明确国资、政府或产业引导基金背景的机构为 1；国资身份不自动代表 VC/PE。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **BI** | `Top-tier VC/PE backing (1=yes; 0=no)` | 仅在本公司招股书确认一线知名 VC/PE 机构持有重要股权或领投时填 1；不得仅凭机构知名度推断其参与本公司投资。无法确认时填 NaN。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **BJ** | `Key Pre-IPO investors` | 仅列本公司招股书披露的上市前投资者，采用一致的英文全称/拼音并以分号分隔；同一投资者只记一次，不从其他 cohort 补名单。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('None': 1) |
| **BK** | `Pre-IPO institutional shareholding (%)` | 上市前 VC/PE/CVC/国资机构合计持股比例，取紧邻上市前的股权口径，不能混入 IPO 新股或基石配售；统一填 0–1 小数（如 12.5%=0.125）。只有招股书披露或可用披露数字复算时填写，否则 NaN。 | 浅蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 1 家 |
| **BL** | `Pre-IPO investor board seat (1=yes; 0=no)` | 只有能从招股书明确关联到 Pre-IPO 投资机构的非执行董事或正式观察员席位才填 1；没有证据不等于 0，无法确认时填 NaN。 | 浅蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 1 家 |
| **BM** | `Earliest Pre-IPO investment round` | 从本公司招股书披露的 Pre-IPO 投资轮次中取最早一轮，保留披露的标准轮次名称；只有明确说明没有外部上市前投资时填 None，否则无法确认时 NA。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('None': 1) |
| **BN** | `Pre-IPO holding duration (years)` | 从最早 Pre-IPO 投资协议日期至本公司招股书日期计算年数，保留两位小数；起始日期无法确认则 NaN。每家公司必须使用自己的招股书日期，不沿用其他季度日期。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **BO** | `Ultimate controller type` | 最终控制人类型（如：自然人 / 家族 / 国资委 / 地方政府 / 外资 / 无实际控制人）。取 SUBSTANTIAL SHAREHOLDERS 与 Controlling Shareholders 段的实际控制人身份表述。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Family (Datuk Tan and spouse Datin Pan, via BBSB Overseas)': 1) |
| **BP** | `Controller economic interest at listing (%)` | 控制人上市时**经济权益**（持股比例），填小数。取 CONTROLLING/SUBSTANTIAL SHAREHOLDERS 表的持股百分比。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.75 / 中位数 0.75 / 区间 [0.75, 0.75] |
| **BQ** | `Controller voting rights at listing (%)` | 控制人上市时**投票权**比例，填小数。有 WVR（同股不同权）时与持股不同，取投票权那一列；无 WVR 通常与 BC 相同。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.75 / 中位数 0.75 / 区间 [0.75, 0.75] |
| **BR** | `Interest-bearing debt at year-1 end` | year-1 期末**总有息负债**（用与 col_V 相同的披露货币基本单位）。包含短期借款、长期借款、租赁负债及带息应付票据债券等带息债务总额，取 INDEBTEDNESS 表格的 Total 余额；不含应付账款等无息负债。必须换算为货币基本单位（乘表格千元/百万元乘数）。期末余额，不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 6,042,000.00 / 中位数 6,042,000.00 / 区间 [6,042,000.00, 6,042,000.00] |
| **BS** | `Debt repayment (% of planned net IPO proceeds)` | 计划净募资中用于**偿债**的比例，填小数。取 USE OF PROCEEDS 里用于偿还借款/债务的金额 ÷ 计划净募资额；没有该用途填 0。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **BT** | `Listing board` | 上市板块（Main Board 主板） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('GEM': 1) |
| **BU** | `Share class` | 股份类别（如 H Shares / A Shares / Class A Ordinary Shares / Class B Ordinary Shares）。按招股书股本表的类别名称填。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Ordinary Shares': 1) |
| **BV** | `A+H issuer flag` | A+H 两地上市发行人标识（1=是，0=否） | 深蓝 | `boolean` | Ex-ante prospectus disclosure | 100% 完备 | 1 (是): 0 家 (0.0%), 0 (否): 1 家 |
| **BW** | `Industry classification code` | 恒生行业分类 HSICS 6 位业务细分代码 | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 602,030.00 / 中位数 602,030.00 / 区间 [602,030.00, 602,030.00] |
| **BX** | `Industry classification system and version` | 行业分类系统与版本号 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('HSICS (Hang Seng Industry Classification System) 2026': 1) |
| **BY** | `Incorporation date` | 公司**法定注册成立日期**（dd/mm/yy）。必须优先取自 Statutory and General Information (Appendix V '1. Incorporation')、History & Development 或 Accountants' Report (附注 1)。严禁从 Definitions (释义) 章节取值（释义章节常有起草笔误或仅为前期筹备日）。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-05-30 ~ 2025-05-30 |
| **BZ** | `Firm age at IPO (years)` | 公司成立至上市年限（Lowry et al. 2017 Table 3.4 基础控制变量） | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.62 / 中位数 0.62 / 区间 [0.62, 0.62] |
| **CA** | `Place of incorporation` | 公司注册成立法域（如 Cayman Islands, PRC 等） | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Cayman Islands': 1) |
| **CB** | `Principal place of business` | 主要营业地点（城市/国家），如 PRC、Hong Kong、Shenzhen, PRC。取公司资料或注册办事处段。 | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Petaling Jaya, Malaysia': 1) |
| **CC** | `Financial statement unit multiplier` | 财务报表基础货币乘数（千元/万元/百万元） | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **CD** | `Accounting standard` | 财务报表采用的会计准则（如 IFRS Accounting Standards / HKFRS / ASBE / US GAAP）。取会计师报告开头声明。 | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 1 种取值 ('IFRS Accounting Standards': 1) |
| **CE** | `Year-3 financial period start` | 往绩记录第三年前期起始日 | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2023-01-01 ~ 2023-01-01 |
| **CF** | `Year-3 financial period end` | 往绩记录第三年前期截止日 | 浅蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2023-12-31 ~ 2023-12-31 |
| **CG** | `Year-2 financial period start` | 往绩记录第二年前期起始日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2024-01-01 ~ 2024-01-01 |
| **CH** | `Year-2 financial period end` | 往绩记录第二年前期截止日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2024-12-31 ~ 2024-12-31 |
| **CI** | `Year-1 financial period start` | 往绩记录最近一期起始日 | 深蓝 | `date` | Track record period financial disclosure | 100% 完备 | 区间: 2025-01-01 ~ 2025-01-01 |
| **CJ** | `Year-1 net sales (original, pre-annualization)` | 最近一期营业收入原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 73,986,000.00 / 中位数 73,986,000.00 / 区间 [73,986,000.00, 73,986,000.00] |
| **CK** | `Year-1 profit before tax (original)` | 最近一期税前利润原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 5,943,000.00 / 中位数 5,943,000.00 / 区间 [5,943,000.00, 5,943,000.00] |
| **CL** | `Year-1 profit for period (original)` | 最近一期净利润原值（年化前） | 深蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 3,201,000.00 / 中位数 3,201,000.00 / 区间 [3,201,000.00, 3,201,000.00] |
| **CM** | `Subscription opening date` | 香港公开发售**开始认购日期**（dd/mm/yy）。取 EXPECTED TIMETABLE。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2025-12-31 ~ 2025-12-31 |
| **CN** | `Subscription closing date` | 香港公开发售**截止认购日期**（dd/mm/yy）。取 EXPECTED TIMETABLE。 | 浅蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2026-01-08 ~ 2026-01-08 |
| **CO** | `H shares after IPO (base; no options)` | 上市后**在港交所挂牌的股份数**（base，不含超额配售）。统一口径：① 内地 H 股发行人全部转换时 = 总股本；② 部分转换时 = 由未上市股转换的 H 股 + 新发 H 股（剩余未上市股不挂牌，不计入）；③ A+H 发行人 = 仅新发 H 股（A 股在沪深市场挂牌，不计入）；④ 开曼/境外发行人没有 H 股类别，其全部股份均在港交所挂牌，故 = 上市后已发行股份总数。即：本列恒等于「港交所挂牌的股份数」，四类结构可比。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 500,000,000.00 / 中位数 500,000,000.00 / 区间 [500,000,000.00, 500,000,000.00] |
| **CP** | `Gross profit in year-1` | year-1 **毛利**（用与 col_V 相同的披露货币基本单位）。取损益表的 Gross profit。强制期间锚定：必须与 col_AT 严格同期间！若 col_AT 为中期报告期（如截至 2025 年 6 月 30 日或 9 月 30 日止期间），必须严格提取该中期报告期对应列的原值，绝对严禁错采前一完整财年（FY2024）的数值。必须换算为货币基本单位（乘表格千元/百万元乘数）。不年化——手册明确仅 year-1 销售/税前利润/净利润年化，毛利不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 15,806,000.00 / 中位数 15,806,000.00 / 区间 [15,806,000.00, 15,806,000.00] |
| **CQ** | `Capital expenditure in year-1` | year-1 **资本开支**（用与 col_V 相同的披露货币基本单位）。取现金流量表“购建物业、厂房及设备”或 CAPITAL EXPENDITURE 段。强制期间锚定：必须与 col_AT 严格同期间！若 col_AT 为中期报告期（如截至 2025 年 6 月 30 日或 9 月 30 日止期间），必须严格提取该中期报告期实际资本开支原值，绝对严禁错采前一完整财年（FY2024）数值。必须换算为货币基本单位（乘表格千元/百万元乘数）。不年化。 | 浅蓝 | `numeric` | Track record period financial disclosure | 100% 完备 | 均值 113,000.00 / 中位数 113,000.00 / 区间 [113,000.00, 113,000.00] |
| **CR** | `Audit opinion (year-1)` | year-1 **审计意见类型**（如 无保留意见 / Unqualified opinion / Qualified opinion）。取会计师报告的审计意见段。 | 浅蓝 | `string` | Track record period financial disclosure | 100% 完备 | 共 1 种取值 ('Unqualified opinion': 1) |
| **CS** | `Listing expenses (HK$)` | **总上市费用**（HK$ 基本单位，含承销佣金与其他开支）。取 UNDERWRITING COMMISSIONS AND LISTING EXPENSES 段的合计。 | 浅蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 25,300,000.00 / 中位数 25,300,000.00 / 区间 [25,300,000.00, 25,300,000.00] |
| **CT** | `Cornerstone investor names` | Cornerstone investor names | 浅蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Mr. Choy Joo Seong; Mr. Tan Nam Joo': 1) |
| **CU** | `Final cornerstone allocation (% of base offer)` | Final cornerstone allocation (% of base offer) | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 0.19 / 中位数 0.19 / 区间 [0.19, 0.19] |
| **CV** | `Earliest cornerstone unlock date (dd/mm/yy)` | 基石投资者最早解禁日期 | 深蓝 | `date` | Post-IPO lockup expiration events | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **CW** | `Subscription Ratio (times)` | Subscription Ratio (times) | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 10,745.13 / 中位数 10,745.13 / 区间 [10,745.13, 10,745.13] |
| **CX** | `Public applicants` | Public applicants | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 145,089.00 / 中位数 145,089.00 / 区间 [145,089.00, 145,089.00] |
| **CY** | `Public valid applied shares` | Public valid applied shares | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 134,314,148,000.00 / 中位数 134,314,148,000.00 / 区间 [134,314,148,000.00, 134,314,148,000.00] |
| **CZ** | `Public subscription original wording` | Public subscription original wording | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Subscription level 10,745.13 times': 1) |
| **DA** | `Pricing date` | Pricing date | 深蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2026-01-09 ~ 2026-01-09 |
| **DB** | `Allotment announcement date` | Allotment announcement date | 深蓝 | `date` | Ex-ante prospectus disclosure | 100% 完备 | 区间: 2026-01-12 ~ 2026-01-12 |
| **DC** | `Final global offering shares (before over-allotment)` | Final global offering shares (before over-allotment) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 125,000,000.00 / 中位数 125,000,000.00 / 区间 [125,000,000.00, 125,000,000.00] |
| **DD** | `Final public offer shares` | Final public offer shares | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 12,500,000.00 / 中位数 12,500,000.00 / 区间 [12,500,000.00, 12,500,000.00] |
| **DE** | `Final placing shares` | Final placing shares | 深蓝 | `numeric` | Allotment results announcement | 100% 完备 | 均值 112,500,000.00 / 中位数 112,500,000.00 / 区间 [112,500,000.00, 112,500,000.00] |
| **DF** | `Over-allotment shares actually issued` | Over-allotment shares actually issued | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **DG** | `Greenshoe exercise rate (%)` | 绿鞋实际行使比例（Ellis et al. 2000 超额配售执行度与价格支持） | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **DH** | `Actual clawback / reallocation description` | Actual clawback / reallocation description | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('No clawback: Claw-back triggered No; re-allocation procedure not applied; final Public Offer 12,500,000 and Placing 112,500,000 Shares': 1) |
| **DI** | `Net IPO proceeds to issuer (HK$)` | Net IPO proceeds to issuer (HK$) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 50,000,000.00 / 中位数 50,000,000.00 / 区间 [50,000,000.00, 50,000,000.00] |
| **DJ** | `Public shareholding at listing (%)` | Public shareholding at listing (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.25 / 中位数 0.25 / 区间 [0.25, 0.25] |
| **DK** | `Share base used for both public shareholding ratios` | Share base used for both public shareholding ratios | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 500,000,000.00 / 中位数 500,000,000.00 / 区间 [500,000,000.00, 500,000,000.00] |
| **DL** | `Unrestricted public shareholding at listing (%)` | Unrestricted public shareholding at listing (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.20 / 中位数 0.20 / 区间 [0.20, 0.20] |
| **DM** | `Free float denominator description` | Free float denominator description | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Free float denominator = total issued shares upon listing (col_CZ); numerator = offer shares minus cornerstone allocation': 1) |
| **DN** | `Free float denominator shares` | Free float denominator shares | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 500,000,000.00 / 中位数 500,000,000.00 / 区间 [500,000,000.00, 500,000,000.00] |
| **DO** | `HSI return over 20 trading days before prospectus (%)` | 招股日前 20 个交易日恒生指数累计收益率 (%) | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 -0.00 / 中位数 -0.00 / 区间 [-0.00, -0.00] |
| **DP** | `GEM ordinary IPO count in 90 calendar days before prospectus` | 招股书日前90个自然日内GEM普通IPO上市家数（不含主板） | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 1.00 / 中位数 1.00 / 区间 [1.00, 1.00] |
| **DQ** | `1-month HIBOR before prospectus (%)` | 招股日前一交易日香港银行同业拆借 1 个月 HIBOR 利率 (%) | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.03 / 中位数 0.03 / 区间 [0.03, 0.03] |
| **DR** | `Banking system aggregate balance before prospectus (HK$)` | 招股日前一交易日香港银行体系总结余 (HK$) | 深蓝 | `numeric` | Ex-ante pre-prospectus window | 100% 完备 | 均值 53,950,000,000.00 / 中位数 53,950,000,000.00 / 区间 [53,950,000,000.00, 53,950,000,000.00] |
| **DS** | `First trading day closing price (HK$)` | 首日上市二级市场收盘价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 0.67 / 中位数 0.67 / 区间 [0.67, 0.67] |
| **DT** | `First-day return / Underpricing (%)` | 上市首日抑价率 / 初始收益率（Rock 1986 / Ritter 1984 核心被解释变量） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 0.12 / 中位数 0.12 / 区间 [0.12, 0.12] |
| **DU** | `Money left on the table (HK$)` | 留在桌面上的财富 / 抑价转移财富总额（Loughran & Ritter 2002 前景理论指标） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 8,750,000.00 / 中位数 8,750,000.00 / 区间 [8,750,000.00, 8,750,000.00] |
| **DV** | `First trading day opening price (HK$)` | 首日上市二级市场开盘价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 3.00 / 中位数 3.00 / 区间 [3.00, 3.00] |
| **DW** | `First trading day high (HK$)` | 首日上市二级市场盘中最高价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 3.11 / 中位数 3.11 / 区间 [3.11, 3.11] |
| **DX** | `First trading day low (HK$)` | 首日上市二级市场盘中最低价 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 0.59 / 中位数 0.59 / 区间 [0.59, 0.59] |
| **DY** | `First trading day volume (shares)` | 首日上市二级市场全天成交量（股） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 120,963,660.00 / 中位数 120,963,660.00 / 区间 [120,963,660.00, 120,963,660.00] |
| **DZ** | `First-day flipping ratio (%)` | 首日短线翻转抛售率 / 成交量占全球发售比例（Aggarwal 2003 机构抛售假说） | 深蓝 | `numeric` | Listing Day 1 secondary market | 100% 完备 | 均值 0.97 / 中位数 0.97 / 区间 [0.97, 0.97] |
| **EA** | `First trading day turnover (HK$)` | 首日上市二级市场全天成交金额 (HK$) | 深蓝 | `numeric` | Listing Day 1 secondary market | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **EB** | `Offer mechanism` | 适用发售与回拨制度（2025-08-04 前 PN18/18C.09；之后 Mechanism A/B） | 深蓝 | `string` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **EC** | `Applicable IPO rules / transition basis` | 适用之上市规则过渡基准（FINI 改革规则） | 深蓝 | `string` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **ED** | `Company Chinese Name` | Company Chinese Name | 浅蓝 | `string` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **EE** | `Current listing status` | 当前挂牌存续状态 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Active': 1) |
| **EF** | `1-month post-IPO close price (HK$)` | 第20个交易日收盘价（窗口成熟后填报） | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.66 / 中位数 0.66 / 区间 [0.66, 0.66] |
| **EG** | `1-month BHR from Day-1 close (%)` | 由首日收盘至第20个交易日的买入持有收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **EH** | `1-month total return from offer price (%)` | 由发售价至第20个交易日的累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.12 / 中位数 0.12 / 区间 [0.12, 0.12] |
| **EI** | `1-month HSI return (%)` | 同期恒生指数累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.01 / 中位数 0.01 / 区间 [0.01, 0.01] |
| **EJ** | `1-month HSTECH return (%)` | 同期恒生科技指数累计收益率 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 -0.08 / 中位数 -0.08 / 区间 [-0.08, -0.08] |
| **EK** | `1-month wealth relative vs HSI` | 一个月相对恒指财富比 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 0.99 / 中位数 0.99 / 区间 [0.99, 0.99] |
| **EL** | `1-month wealth relative vs HSTECH` | 一个月相对恒生科技指数财富比 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 1.08 / 中位数 1.08 / 区间 [1.08, 1.08] |
| **EM** | `1-month average daily turnover (HK$)` | 上市后首20个交易日日均成交额 | 深蓝 | `numeric` | Post-IPO T+20 trading days | 100% 完备 | 均值 11,622,003.50 / 中位数 11,622,003.50 / 区间 [11,622,003.50, 11,622,003.50] |
| **EN** | `6-month post-IPO close price (HK$)` | 六个月目标日后首个交易日收盘价（窗口成熟后填报） | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.56 / 中位数 0.56 / 区间 [0.56, 0.56] |
| **EO** | `6-month BHR from Day-1 close (%)` | 由首日收盘至六个月目标交易日的买入持有收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 -0.15 / 中位数 -0.15 / 区间 [-0.15, -0.15] |
| **EP** | `6-month total return from offer price (%)` | 由发售价至六个月目标交易日的累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 -0.05 / 中位数 -0.05 / 区间 [-0.05, -0.05] |
| **EQ** | `6-month HSI return (%)` | 同期恒生指数累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 -0.10 / 中位数 -0.10 / 区间 [-0.10, -0.10] |
| **ER** | `6-month HSTECH return (%)` | 同期恒生科技指数累计收益率 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 -0.20 / 中位数 -0.20 / 区间 [-0.20, -0.20] |
| **ES** | `6-month wealth relative vs HSI` | 六个月相对恒指财富比 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 0.94 / 中位数 0.94 / 区间 [0.94, 0.94] |
| **ET** | `6-month wealth relative vs HSTECH` | 六个月相对恒生科技指数财富比 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 1.06 / 中位数 1.06 / 区间 [1.06, 1.06] |
| **EU** | `6-month average daily turnover (HK$)` | 六个月目标日前20个交易日日均成交额 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | 100% 完备 | 均值 69,385.00 / 中位数 69,385.00 / 区间 [69,385.00, 69,385.00] |
| **EV** | `Liquidity decay ratio (6M vs Day-1 turnover)` | 六个月窗口日均成交额相对首日成交额比率 | 深蓝 | `numeric` | Ex-ante prospectus disclosure | 100% 完备 | 均值 0.00 / 中位数 0.00 / 区间 [0.00, 0.00] |
| **EW** | `1-year post-IPO return (%) [Reserved]` | 一年期收益率预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **EX** | `1-year wealth relative vs HSI [Reserved]` | 一年期相对恒指财富比预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **EY** | `3-year post-IPO return (%) [Reserved]` | 三年期收益率预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **EZ** | `3-year wealth relative vs HSI [Reserved]` | 三年期相对恒指财富比预留字段 | 深蓝 | `string` | Long-run post-IPO (Reserved / Unmatured) | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FA** | `18A/18C regulatory milestone status` | 18A/18C 监管路径与商业化里程碑状态 | 深蓝 | `string` | Ex-ante prospectus disclosure | 100% 完备 | 共 1 种取值 ('Standard': 1) |
| **FB** | `Stabilizing manager` | 官方指定价格稳定经理人名称 | 深蓝 | `string` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FC** | `Stabilization period end date` | 法定30天稳价期结束日期 | 深蓝 | `string` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FD** | `Stabilization purchases occurred` | 稳价期内是否发生二级市场托单购买 (1=是, 0=否) | 深蓝 | `boolean` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FE** | `Over-allocation shares` | 国际配售超额配售股份数量（股） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FF** | `Over-allocation (% of base offer)` | 超额配售股数占基础发售股份比例 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FG** | `Over-allotment option exercise date` | 超额配售权实际行使公告日期 | 深蓝 | `string` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FH** | `Shares issued under over-allotment option` | 超额配售权最终发行股份数量（股） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FI** | `Over-allotment exercise percentage (%)` | 超额配售权行使比例 (行使股数/超额配售上限, %) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FJ** | `Post-stabilization cliff return [-5, +5] (%)` | 稳价期结束日前后[-5, +5]交易日累计收益率（断崖效应测试） | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FK** | `Post-stabilization 20-day return [0, +20] (%)` | 稳价期结束后20个交易日累计收益率 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FL** | `Post-stabilization volume decay ratio (%)` | 稳价结束后20日均成交额相对稳价期内之比 (%) | 深蓝 | `numeric` | Post-IPO 30-day stabilization window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FM** | `Day-5 BHR from Day-1 close (%)` | 挂牌首周 (T+5交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FN** | `Day-5 wealth relative vs HSI` | 挂牌首周对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FO** | `Day-20 BHR from Day-1 close (%)` | 首月 (T+20交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FP** | `Day-20 wealth relative vs HSI` | 首月对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FQ** | `3-month BHR from Day-1 close (%)` | 首季 (T+63交易日) 二级买入持有收益率 (%) | 深蓝 | `numeric` | Aftermarket event horizon window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FR** | `3-month wealth relative vs HSI` | 首季对标恒指财富相对比 (WR_HSI) | 深蓝 | `numeric` | Aftermarket event horizon window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FS** | `3-month wealth relative vs HSTECH` | 首季对标恒科财富相对比 (WR_HSTECH) | 深蓝 | `numeric` | Aftermarket event horizon window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FT** | `3-month average daily turnover (HK$)` | 首季度日均成交金额 (港元) | 深蓝 | `numeric` | Aftermarket event horizon window | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FU** | `Amihud illiquidity (6M mean)` | 上市前6个月日均 Amihud (2002) 非流动性指标 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FV** | `Zero-volume days count (first 6M)` | 上市前6个月零成交量交易日天数 | 深蓝 | `numeric` | Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure) | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FW** | `Return volatility (first 6M daily std dev, %)` | 上市前6个月日度收益率标准差 (波动率, %) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FX** | `Maximum drawdown (first 6M, %)` | 上市前6个月二级市场最大回撤幅度 (%) | 深蓝 | `numeric` | Ex-ante prospectus disclosure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FY** | `Cornerstone unlock CAR [-5, +5] (%)` | 基石投资者解禁日前后[-5, +5]交易日累计超额收益 (CAR vs HSI) | 深蓝 | `numeric` | Post-IPO lockup expiration events | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **FZ** | `Cornerstone unlock CAR [-20, +20] (%)` | 基石投资者解禁日前后[-20, +20]交易日累计超额收益 (CAR vs HSI) | 深蓝 | `numeric` | Post-IPO lockup expiration events | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GA** | `Cornerstone unlock volume shock ratio` | 基石解禁后20日均换手额相对解禁前20日换手额之比 | 深蓝 | `numeric` | Post-IPO lockup expiration events | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GB** | `Lead sponsor name` | 独家/联席牵头保荐人英文全称 | 深蓝 | `string` | Prospectus syndicate structure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GC** | `Joint sponsor count` | 保荐人总家数 (独家=1, 联席=2+) | 深蓝 | `numeric` | Prospectus syndicate structure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GD** | `Sponsor commercial bank affiliate flag` | 保荐人是否属于商业银行系金融机构 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus syndicate structure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GE** | `Underwriting base commission rate (%)` | 承销基础佣金费率 (%) | 深蓝 | `numeric` | Prospectus syndicate structure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GF** | `Underwriting discretionary incentive fee rate (%)` | 招股书披露的酌情奖励费率上限（非实际支付，%） | 深蓝 | `numeric` | Prospectus syndicate structure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GG** | `Total underwriting fee rate (%)` | 披露的承销总费率上限（基础+奖励上限，非实际支付，%） | 深蓝 | `numeric` | Prospectus syndicate structure | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GH** | `Cornerstone investor count` | 基石投资者机构总家数 | 深蓝 | `numeric` | Prospectus / allotment institutional network | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GI** | `Cornerstone state-owned presence flag` | 基石投资者中是否包含国资/地方政府基金 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GJ** | `Crossover fund presence flag` | 是否包含兼具 Pre-IPO 与基石双重身份的跨界基金 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GK** | `Pre-IPO institutional investor count` | 主要 Pre-IPO 投资机构总数 | 深蓝 | `numeric` | Prospectus / allotment institutional network | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GL** | `Pre-IPO state-owned backing flag` | Pre-IPO 股东中是否包含国资机构 (1=是, 0=否) | 深蓝 | `boolean` | Prospectus / allotment institutional network | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |
| **GM** | `FINI digital settlement regime` | 结算监管体制 (POST_FINI / PRE_FINI) | 深蓝 | `string` | Listing date regulatory regime | Reserved / Unmatured (0/1 (0.0%)) | 全部缺失（Reserved / Unmatured；类型取自注册表声明） |

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
