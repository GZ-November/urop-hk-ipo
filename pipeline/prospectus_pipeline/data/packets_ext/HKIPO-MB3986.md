# 3986.HK 扩展 18 列抽取包

公司：3986.HK GigaDevice Semiconductor Inc. - H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB3986.json`。
主包（42 列）已完成并已入表，这里只补扩展列。

## 字段清单
| key | 列 | 表头 | 类型 | 缺失 | 提示 |
|---|---|---|---|---|---|
| col_BA | BA | Pre-IPO VC/PE backing (1=yes; 0=no) | integer | NaN | 是否引入 Pre-IPO VC/PE 投资者：1=有，0=无。看 HISTORY AND DEVELOPMENT — Pre-IPO Investments 与 SUBSTANTIAL SHAREHOLDERS 名单；只要有专业投资机构（VC/PE/产业基金）在上市前入股即 1。 |
| col_BB | BB | Ultimate controller type | text | NA | 最终控制人类型（如：自然人 / 家族 / 国资委 / 地方政府 / 外资 / 无实际控制人）。取 SUBSTANTIAL SHAREHOLDERS 与 Controlling Shareholders 段的实际控制人身份表述。 |
| col_BC | BC | Controller economic interest at listing (%) | number | NaN | 控制人上市时**经济权益**（持股比例），填小数。取 CONTROLLING/SUBSTANTIAL SHAREHOLDERS 表的持股百分比。 |
| col_BD | BD | Controller voting rights at listing (%) | number | NaN | 控制人上市时**投票权**比例，填小数。有 WVR（同股不同权）时与持股不同，取投票权那一列；无 WVR 通常与 BC 相同。 |
| col_BE | BE | Interest-bearing debt at year-1 end | number | NaN | year-1 期末**有息负债**（借款、债券、租赁负债等带息项目）。取 INDEBTEDNESS 段或借款附注的期末余额；不含应付账款等无息负债。 期末余额，不年化（手册：仅 year-1 销售/税前利润/净利润年化） |
| col_BF | BF | Technology commercialization stage | text | NA | 技术商业化阶段（如：研发阶段 / 小批量试产 / 商业化初期 / 规模商业化 / 已量产）。按 BUSINESS 与业务摘要里的产品状态表述填，不要按行业推测。 |
| col_BG | BG | Debt repayment (% of planned net IPO proceeds) | number | NaN | 计划净募资中用于**偿债**的比例，填小数。取 USE OF PROCEEDS 里用于偿还借款/债务的金额 ÷ 计划净募资额；没有该用途填 0。 |
| col_BI | BI | Share class | text | NA | 股份类别（如 H Shares / A Shares / Class A Ordinary Shares / Class B Ordinary Shares）。按招股书股本表的类别名称填。 |
| col_BP | BP | Incorporation date | date | NA | 公司**注册成立日期**（dd/mm/yy）。取 HISTORY AND DEVELOPMENT 或公司资料段“incorporated/established on <date>”。 |
| col_BR | BR | Principal place of business | text | NA | 主要营业地点（城市/国家），如 PRC、Hong Kong、Shenzhen, PRC。取公司资料或注册办事处段。 |
| col_BT | BT | Accounting standard | text | NA | 财务报表采用的会计准则（如 IFRS Accounting Standards / HKFRS / ASBE / US GAAP）。取会计师报告开头声明。 |
| col_CC | CC | Subscription opening date | date | NA | 香港公开发售**开始认购日期**（dd/mm/yy）。取 EXPECTED TIMETABLE。 |
| col_CD | CD | Subscription closing date | date | NA | 香港公开发售**截止认购日期**（dd/mm/yy）。取 EXPECTED TIMETABLE。 |
| col_CE | CE | H shares after IPO (base; no options) | integer | NaN | 上市后 H 股股数（base，不含超额配售）。取股本表里 H 股合计或“H Shares to be issued pursuant to the Global Offering”。 股本余额，不年化 |
| col_CF | CF | Gross profit in year-1 | number | NaN | year-1 **毛利**（用与 col_V 相同的披露货币基本单位）。取损益表的 Gross profit。 **不年化**——手册明确仅 year-1 销售/税前利润/净利润年化，毛利不在其列；直接填 year-1 期间披露值 |
| col_CG | CG | Capital expenditure in year-1 | number | NaN | year-1 **资本开支**。取现金流量表“购建物业、厂房及设备”或 CAPITAL EXPENDITURE 段。 **不年化**——属原始期间流量，与 AU/AW/AX 同口径；直接填 year-1 期间披露值 |
| col_CH | CH | Audit opinion (year-1) | text | NA | year-1 **审计意见类型**（如 无保留意见 / Unqualified opinion / Qualified opinion）。取会计师报告的审计意见段。 |
| col_CI | CI | Listing expenses (HK$) | number | NaN | **总上市费用**（HK$ 基本单位，含承销佣金与其他开支）。取 UNDERWRITING COMMISSIONS AND LISTING EXPENSES 段的合计。 |

## 已确认的结论（直接用，不要推翻）
- 股本结构（**已确认，不要改**）：L=696765151 M=28915800 N=667849351 O=667849351 P=0 Q=28915800 R=26024200 S=2891600
- 财务期间（**已确认**）：year-1 期末 = 30/06/25；币种 = RMB；year-1 净利 = 1175670000
- 行业分类（港交所官方）：703010 半導體
- 基石投资者：有

## 手册规则
- 金额换算成**基本货币单位**（披露币种见上面的 col_V）；百分比填**小数**。
- `col_BE` 只算**有息负债**（借款/债券/租赁负债），不含应付账款。
- `col_BG` = 用于偿债的金额 ÷ 计划净募资额；没有该用途填 `0`。
- `col_BF` 按招股书原文的产品阶段表述，**不要**按行业推测。
- `col_BA` 只要上市前有专业投资机构（VC/PE/产业基金）入股即 `1`，否则 `0`。
- `col_CD`/`col_CC` 取 EXPECTED TIMETABLE 的认购起止日。
- `col_CI` 是**总上市费用**（含承销佣金与其他开支），用 HK$ 基本单位。
- 不确定就填 NaN/NA 并在 quote 说明，**不要猜**。

## 输出契约（机器校验，违反即失败）
顶层**只能**有 `code` 和 `fields`：
```json
{"code":"3986.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  3986.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 3986.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
（锚点无命中，需要自己 search）

### col_BB
  - p159: as reviewed and determined by relevant competent authorities under the State / Council in accordance with law; / (3) / the domestic enterprise, its controlling shareholders or the actual controller, have / committed criminal offences such as corruption, bribery, misappropriation of / property, embezzlement, or undermining the order of the socialist market economy / during the recent three years;
  - p41: the Board / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / DEFINITIONS / – 31 –
  - p98: business prospects of Hefei Kuxin. Such investment is subject to the fullfilment of conditions precedent / set out in the investment agreement and might not be materialized. To the best knowledge, information / and belief of the Directors and having made all reasonable enquiry, each of Hefei Kuxin, the relevant / counterparties and the ultimate beneficial owners of Hefei Kuxin and the relevant cou

### col_BC
  - p159: as reviewed and determined by relevant competent authorities under the State / Council in accordance with law; / (3) / the domestic enterprise, its controlling shareholders or the actual controller, have / committed criminal offences such as corruption, bribery, misappropriation of / property, embezzlement, or undermining the order of the socialist market economy / during the recent three years;
  - p41: the Board / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / DEFINITIONS / – 31 –

### col_BD
  - p159: as reviewed and determined by relevant competent authorities under the State / Council in accordance with law; / (3) / the domestic enterprise, its controlling shareholders or the actual controller, have / committed criminal offences such as corruption, bribery, misappropriation of / property, embezzlement, or undermining the order of the socialist market economy / during the recent three years;
  - p158: However, where one of the following is the case relevant to an operator consolidation, / declaration to the State Council anti-monopoly law enforcement authorities is not required: (1) / one of the parties to a consolidation holds fifty percent or more assets or shares that grant / voting rights in each of the other Operators; or (2) in each of the parties to a consolidation, fifty / percent or mo
  - p41: the Board / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / DEFINITIONS / – 31 –

### col_BE
  - p309: primarily consists of (i) dividends paid of RMB707.5 million, (ii) purchase of forfeited / restricted shares of RMB34.5 million, and (iii) capital element of lease rentals paid of / RMB31.4 million. / INDEBTEDNESS / The table below sets forth the indebtedness as of the dates indicated. / As of December 31, / As of
  - p303: Trade Payables / Our trade payables are primarily for contract manufacturing and raw materials, masks, / software and IT services. Our trade payables are non-interest-bearing and are normally settled / on 15 days to two months terms. / As of December 31, / As of
  - p310: Record Period and up to the Latest Practicable Date. Our Directors confirm that there has not / been any material change in our indebtedness since the October 31, 2025 up to the date of this / prospectus. Our Directors confirm that we did not have any material defaults on trade and / non-trade payables and borrowings, breaches of covenants, or experience any material / difficulty in obtaining bank

### col_BF
  - p54: • / cyclicality in the downstream industries; / • / the inability to dedicate necessary resources to promote and commercialize end / products; / • / the failure to meet the evolving industry requirements or achieve market acceptance;
  - p137: • / Supply-Chain Barriers / Chip design enterprises need to have the ability to coordinate and manage key processes / such as wafer foundry and packaging/testing to ensure smooth mass production and stable / delivery of products. Leading enterprises have formed deep cooperation mechanisms with / multiple upstream and downstream entities through long-term accumulation, possessing higher / collabora
  - p82: prices of other companies with business operations located mainly in Chinese Mainland that / have listed their securities in Hong Kong may affect the volatility in the price of and trading / volumes for our H Shares. A number of Chinese Mainland-based companies have listed their / securities, and some are in the process of preparing for listing their securities, in Hong Kong. / The share price of 

### col_BG
  - p24: Our R&D efforts are not guaranteed to yield the results we anticipate; / • / We rely on third parties for IC fabrication, testing and packaging; / FUTURE PLANS AND USE OF PROCEEDS / Assuming an Offer Price of HK$147.00 per H Share (being the midpoint of the range of / the Offer Price stated in this prospectus), we estimate that we will receive net proceeds of / approximately HK$4,180.7 million fro
  - p24: Our R&D efforts are not guaranteed to yield the results we anticipate; / • / We rely on third parties for IC fabrication, testing and packaging; / FUTURE PLANS AND USE OF PROCEEDS / Assuming an Offer Price of HK$147.00 per H Share (being the midpoint of the range of / the Offer Price stated in this prospectus), we estimate that we will receive net proceeds of / approximately HK$4,180.7 million fro

### col_BI
  - p2: Number of Offer Shares under the / Global Offering / : / 28,915,800 H Shares (subject to the / Offer Size Adjustment Option and the / Over-allotment Option) / Number of Hong Kong Offer Shares

### col_BP
  - p1: Stock Code : 3986 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / 兆易創新科技集團股份有限公司 / GigaDevice Semiconductor Inc. / GLOBAL

### col_BR
  - p111: Registered Office / Room 101, 1/F to 5/F, Building 8 / No. 9 Fenghao East Road / Haidian District

### col_BT
  - p17: should be read together with, and is qualified in its entirety by reference to, the consolidated / financial statements as set out in the Accountants’ Report in Appendix I to this prospectus, / including the related notes. Our consolidated financial information was prepared in accordance / with IFRS Accounting Standards. / Results of Operations / Year Ended December 31, / Six Months Ended June 30,
  - p17: should be read together with, and is qualified in its entirety by reference to, the consolidated / financial statements as set out in the Accountants’ Report in Appendix I to this prospectus, / including the related notes. Our consolidated financial information was prepared in accordance / with IFRS Accounting Standards. / Results of Operations / Year Ended December 31, / Six Months Ended June 30,
  - p261: historical cost basis except for financial assets and liabilities measured at FVPL and equity / securities designated at FVOCI are stated at their fair value. / See notes 1 and 2 to “Appendix I — Accountants’ Report.” / MATERIAL ACCOUNTING POLICIES AND ESTIMATES / Note 2 to “Appendix I — Accountants’ Report” to this prospectus sets forth certain / material accounting policy information, which are 

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong / Public Offering, we will issue an announcement in Hong Kong to be published on the / Company’s website at www.gigadevice.com and the website of the Stock Exchange at / www.hkexnews.hk.
  - p5: Public Offering, we will issue an announcement in Hong Kong to be published on the / Company’s website at www.gigadevice.com and the website of the Stock Exchange at / www.hkexnews.hk. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on / Wednesday, December 31, 2025 / Latest time for completing electronic applications / under the HK eIPO W

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong / Public Offering, we will issue an announcement in Hong Kong to be published on the / Company’s website at www.gigadevice.com and the website of the Stock Exchange at / www.hkexnews.hk.

### col_CE
  - p26: “Appendix II – Unaudited Pro Forma Financial Information” in this prospectus and on the basis that / 692,028,799 Shares (being 664,059,190 Shares in issue as of June 30, 2025, deducting repurchased ordinary / shares held by us and unvested restricted shares under the 2021 Restricted Share Incentive Plan as at June 30, / 2025 of 946,191 Shares and adding 28,915,800 H Shares to be issued pursuant to
  - p4: channel must be for a minimum of 100 Hong Kong Offer Shares and in one of the / numbers set out in the table. / If you are applying through the HK eIPO White Form service, you may refer to / the table below for the amount payable for the number of H Shares you have selected. / You must pay the respective maximum amount payable on application in full upon / application for Hong Kong Offer Shares. /

### col_CF
  - p17: (64.3)% (2,308,838) / (64.0)% (2,617,583) / (63.1)% / Gross profit        / 3,697,216 / 45.5% / 1,746,308
  - p17: (64.3)% (2,308,838) / (64.0)% (2,617,583) / (63.1)% / Gross profit        / 3,697,216 / 45.5% / 1,746,308

### col_CG
  - p27: market condition. As such, we did not experience material disruption of supplies caused by the / COVID-19 pandemic. Moreover, as an IC design house, our business and financial results are / closely linked to the cyclical nature of the semiconductor industry, which is influenced by / factors such as macroeconomic trends, capital expenditures, technology shifts, inventory / adjustments, and changes 
  - p27: market condition. As such, we did not experience material disruption of supplies caused by the / COVID-19 pandemic. Moreover, as an IC design house, our business and financial results are / closely linked to the cyclical nature of the semiconductor industry, which is influenced by / factors such as macroeconomic trends, capital expenditures, technology shifts, inventory / adjustments, and changes 
  - p308: Investing Activities / In the six months ended June 30, 2025, we had net cash used in investing activities of / RMB1,762.8 million, which primarily consists of (i) purchase of time deposits of RMB1,330.3 / million, (ii) payments for the purchase of property, plant and equipment and intangible assets / of RMB412.5 million and (iii) investment in associates of RMB140.0 million, partially offset / by

### col_CH
  - p402: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purpose of the / accountants’ report, a true and fair view of the Group’s and the Company’s financial position / as at 31 December 2022, 2023 and 2024 and 30 June 2025 and of the Group’s financial / perform
  - p17: The following tables sets forth summary financial data from our consolidated financial / information during the Track Record Period. The summary financial data set forth below / should be read together with, and is qualified in its entirety by reference to, the consolidated / financial statements as set out in the Accountants’ Report in Appendix I to this prospectus, / including the related notes.

### col_CI
  - p18: as an analytical tool, and you should not consider them in isolation from, or as substitute for / analysis of, our consolidated financial statements or financial condition as reported under IFRS / Accounting Standards. We define adjusted net profit (a non-IFRS measure) as profit for the / year/period adjusted for share-based payments (a non-cash item) and listing expenses. We / define adjusted net
  - p18: as an analytical tool, and you should not consider them in isolation from, or as substitute for / analysis of, our consolidated financial statements or financial condition as reported under IFRS / Accounting Standards. We define adjusted net profit (a non-IFRS measure) as profit for the / year/period adjusted for share-based payments (a non-cash item) and listing expenses. We / define adjusted net


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 3986.HK`
有 ERROR 必须回原文修正。
