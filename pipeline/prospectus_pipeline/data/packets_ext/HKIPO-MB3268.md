# 3268.HK 扩展 18 列抽取包

公司：3268.HK MeiG Smart Technology Co., Ltd. - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB3268.json`。
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
- 股本结构（**已确认，不要改**）：L=296756700 M=35000000 N=261756700 O=261756700 P=0 Q=35000000 R=31500000 S=3500000
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = 150893333.33333334
- 行业分类（港交所官方）：701010 消費性電訊設備及零件
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
{"code":"3268.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  3268.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 3268.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
（锚点无命中，需要自己 search）

### col_BB
  - p29: to fines, enforcement actions or other penalties that could, individually or in the aggregate, have a / material adverse effect on our business, financial condition and results of operations. For further / details, please see “Business — Legal Proceedings and Compliance”. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, our Company was held as to (i) 39.13% by Mr. WANG / Ping; a
  - p46: person(s),” / “controlling / shareholder(s),” / “subsidiary(ies)” and “substantial shareholder(s)” shall have the meanings given to such terms in / the Listing Rules, unless the context otherwise requires. / For ease of reference, the names of the PRC established companies or entities, laws or / regulations have been included in this prospectus in both the Chinese and English languages and
  - p185: As of the Latest Practicable Date, Fenghuangshan Investment was wholly owned by Shenzhen Fenghuang / Joint-Stock Cooperative Company (深圳市鳳凰股份合作公司), a joint-stock enterprise jointly funded and operated / by rural collective economic organizations or their members. To the best knowledge of the Company, each of / Fenghuangshan Investment and its ultimate beneficial owners was an Independent Third Par

### col_BC
  - p29: to fines, enforcement actions or other penalties that could, individually or in the aggregate, have a / material adverse effect on our business, financial condition and results of operations. For further / details, please see “Business — Legal Proceedings and Compliance”. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, our Company was held as to (i) 39.13% by Mr. WANG / Ping; a
  - p46: person(s),” / “controlling / shareholder(s),” / “subsidiary(ies)” and “substantial shareholder(s)” shall have the meanings given to such terms in / the Listing Rules, unless the context otherwise requires. / For ease of reference, the names of the PRC established companies or entities, laws or / regulations have been included in this prospectus in both the Chinese and English languages and

### col_BD
  - p29: to fines, enforcement actions or other penalties that could, individually or in the aggregate, have a / material adverse effect on our business, financial condition and results of operations. For further / details, please see “Business — Legal Proceedings and Compliance”. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, our Company was held as to (i) 39.13% by Mr. WANG / Ping; a
  - p94: The interests of our Controlling Shareholders may not be aligned with the interests of other / Shareholders. / Immediately upon the completion of the Global Offering, our Controlling Shareholders will / control approximately 43.36% of the voting rights at our general meetings. Our Controlling / Shareholders will, through their voting power at the Shareholders’ meetings and their delegates on / the
  - p46: person(s),” / “controlling / shareholder(s),” / “subsidiary(ies)” and “substantial shareholder(s)” shall have the meanings given to such terms in / the Listing Rules, unless the context otherwise requires. / For ease of reference, the names of the PRC established companies or entities, laws or / regulations have been included in this prospectus in both the Chinese and English languages and

### col_BE
  - p352: million as of December 31, 2024, primarily because of lease payments. Our non-current lease / liabilities increased by 173.1% from RMB1.4 million as of December 31, 2024 to RMB3.9 million / as of September 30, 2025, primarily because we entered into new lease agreements. / INDEBTEDNESS / The table below sets out the details of our indebtedness as of the dates indicated: / As of December 31, / As o
  - p26: a / decrease / in / interest-bearing / bank / borrowings / of
  - p26: in / interest-bearing / bank / borrowings / of / RMB305.7 million, partially offset by an increase in trade and bills payables of RMB154.5 / million.

### col_BF
  - p14: the / threshold / for / high-computing-power smart modules, enabling stable deployment and effective commercialization in mainstream / scenarios such as AI model deployment in intelligent cockpits and on-device generative image models for extended / reality devices. / (2)
  - p182: We established our research and development center in Shanghai and commenced / our product design and development in the field of 4G wireless communications. / 2013 / Our 4G wireless data terminals became one of the first to achieve mass production. / 2014 / We increased our investment in the research and development for 4G technology, / and subsequently established R&D centers in Xi’an and Wuhan.
  - p93: fluctuation of the market prices of other companies with business operations located mainly in / Chinese mainland that have listed their securities in Hong Kong may affect the volatility in the / price of and trading volumes for our H Shares. A number of Chinese mainland-based companies / have listed their securities, and some are in the process of preparing for listing their securities, in / Hong

### col_BG
  - p31: distribution of dividends in the future after taking into account our results of operations, financial / condition, operating requirements, capital requirements, shareholders’ interests and any other / conditions that our Board may deem relevant. / FUTURE PLANS AND USE OF PROCEEDS / Future Plans / Please see “Business — Our Strategies” for a detailed description of our future plans. / Use of Proce
  - p89: certain current account transactions such as profit distributions, interest payments and trade-related / expenses can be conducted in foreign currency without prior approval from the SAFE, as long as / certain procedural requirements are met. However, capital account transactions such as capital / transfers, direct investments, securities investments and repayment of borrowings are subject to / fo
  - p31: distribution of dividends in the future after taking into account our results of operations, financial / condition, operating requirements, capital requirements, shareholders’ interests and any other / conditions that our Board may deem relevant. / FUTURE PLANS AND USE OF PROCEEDS / Future Plans / Please see “Business — Our Strategies” for a detailed description of our future plans. / Use of Proce

### col_BI
  - p2: Number of Offer Shares under the / Global Offering / : / 35,000,000 H Shares (subject to the Offer Size / Adjustment Option) / Number of Hong Kong Offer Shares / :

### col_BP
  - p184: Capital of Our Subsidiaries” in Appendix VI to this prospectus. / MAJOR SHAREHOLDING CHANGES OF OUR COMPANY / Early Development and Conversion into a Joint Stock Company / Our Company was established on April 5, 2007, under the laws of the PRC as a limited / liability company with an initial registered capital of RMB1 million, which was contributed as to / 99% by Mr. WANG Guojun (王囯軍), the father 
  - p1: (A joint stock company incorporated in the People’s Republic of China with limited liability) / Stock Code : 3268 / Sole Sponsor, Sponsor-Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager / Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager

### col_BR
  - p126: Registered Office / 2/F, No. 5 Lingxia Road / Fenghuang Community / Fuyong Street

### col_BT
  - p305: BASIS OF PRESENTATION / The historical financial information has been prepared in accordance with International / Accounting Standards and International Financial Reporting Standards (“IFRSs”), together the / IFRS Accounting Standards, which comprise all standards and interpretations approved by the / International Accounting / Standards / Board.
  - p40: Underwriters / “IFRS” / International Financial Reporting Standards, as issued by / the International Accounting Standards Board / “Independent Third Party(ies)” / person(s) or company(ies) who/which, to the best of our / Directors’ knowledge, information and belief, is/are not a
  - p35: audited consolidated results of our Group for the nine months ended September 30, 2025; and (ii) / the unaudited consolidated results of our Group for the remaining three months ended December / 31, 2025 based on the management accounts of our Group. / The Profit Estimate has been prepared on the basis of the accounting policies consistent in all / material respects with those currently adopted by

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, our Company will issue an announcement to be published on the website of the Stock / Exchange at www.hkexnews.hk and the website of our Company at www.meigsmart.com. / Date(1)
  - p5: Offering, our Company will issue an announcement to be published on the website of the Stock / Exchange at www.hkexnews.hk and the website of our Company at www.meigsmart.com. / Date(1) / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9:00 a.m. on / Friday, February 27, 2026 / Latest time to complete electronic applications / under White F

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, our Company will issue an announcement to be published on the website of the Stock / Exchange at www.hkexnews.hk and the website of our Company at www.meigsmart.com. / Date(1)

### col_CE
  - p188: Our A Shares are listed on the Shenzhen Stock Exchange. So far as our Directors are aware, / immediately following the completion of the Global Offering (assuming that (i) no additional / Shares are issued pursuant to our Equity Incentive Plans and (ii) the Offer Size Adjustment Option / is not exercised), all 35,000,000 H Shares to be issued pursuant to the Global Offering, / approximately 11.79%
  - p365: on the Stock Exchange at the general meeting of our Company held on June 5, 2025. Such / approval is subject to the following conditions: / (i) / Size of the offer. The proposed number of H Shares to be offered shall not exceed 30% / of the total issued share capital enlarged by the H Shares to be issued pursuant to the / Global Offering; / (ii)

### col_CF
  - p16: 2025, primarily due to an increase in the average selling price of our data transmission modules as / a result of an increase in the sales of our 5G data transmission modules and solutions with a high / selling price as a result of our expanded customer base. / Our gross profit margin decreased from 15.8% in the nine months ended September 30, 2024 / to 12.6% in the nine months ended September 30,
  - p16: 2025, primarily due to an increase in the average selling price of our data transmission modules as / a result of an increase in the sales of our 5G data transmission modules and solutions with a high / selling price as a result of our expanded customer base. / Our gross profit margin decreased from 15.8% in the nine months ended September 30, 2024 / to 12.6% in the nine months ended September 30,

### col_CG
  - p79: We recorded net cash flows used in operating activities of RMB31.3 million in 2023 and / RMB129.9 million in 2024. Please see “Financial Information — Liquidity and Capital Resources / — Cash Flow Analysis — Operating Activities”. Net operating cash outflow could impair our / ability to make necessary capital expenditures and constrain our operational flexibility as well as / adversely affect our 
  - p79: We recorded net cash flows used in operating activities of RMB31.3 million in 2023 and / RMB129.9 million in 2024. Please see “Financial Information — Liquidity and Capital Resources / — Cash Flow Analysis — Operating Activities”. Net operating cash outflow could impair our / ability to make necessary capital expenditures and constrain our operational flexibility as well as / adversely affect our 

### col_CH
  - p599: We believe that the evidence we have obtained is sufficient and appropriate to provide a basis / for our opinion. / Opinion / In our opinion: / (a) / the Unaudited Pro Forma Financial Information has been properly compiled on the basis / stated;
  - p26: 31, 2024, primarily due to our profit for the year of RMB134.4 million. Our total equity increased / from RMB1,567.1 million as of December 31, 2024 to RMB1,681.3 million as of September 30, / 2025, primarily due to our profit for the period of RMB113.2 million. Please see “Consolidated / Statements of Changes in Equity” in the Accountants’ Report in Appendix I to this prospectus. / SUMMARY / – 15

### col_CI
  - p23: understanding and evaluating our consolidated results of operations in the same manner as they / help our management. We define adjusted net profit (non-IFRS measure) as profit for the / year/period adjusted for (i) share-based payment expenses, which are non-cash in nature; and (ii) / listing expenses, which relate to the Global Offering. However, our presentation of adjusted net / profit (non-IF
  - p23: understanding and evaluating our consolidated results of operations in the same manner as they / help our management. We define adjusted net profit (non-IFRS measure) as profit for the / year/period adjusted for (i) share-based payment expenses, which are non-cash in nature; and (ii) / listing expenses, which relate to the Global Offering. However, our presentation of adjusted net / profit (non-IF
  - p409: UNDERWRITING COMMISSIONS AND LISTING EXPENSES / The Underwriters and the Capital Market Intermediaries will receive an underwriting / commission equal to 2.65% of the aggregate Offer Price payable for the Offer Shares, out of which / they will pay any sub-underwriting commissions and other fees (the “Fixed Fees”). Our Company


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 3268.HK`
有 ERROR 必须回原文修正。
