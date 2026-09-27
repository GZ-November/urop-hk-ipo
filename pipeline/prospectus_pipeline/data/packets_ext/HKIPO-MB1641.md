# 1641.HK 扩展 18 列抽取包

公司：1641.HK Hongxing Coldchain (Hunan) Co., Ltd.- H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB1641.json`。
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
- 股本结构（**已确认，不要改**）：L=98263000 M=23263000 N=75000000 O=75000000 P=0 Q=23263000 R=20936500 S=2326500
- 财务期间（**已确认**）：year-1 期末 = 30/06/2025；币种 = RMB；year-1 净利 = 79366000
- 行业分类（港交所官方）：601030 地產投資
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
{"code":"1641.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  1641.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 1641.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
（锚点无命中，需要自己 search）

### col_BB
  - p21: OUR CONTROLLING SHAREHOLDERS AND SHAREHOLDING STRUCTURE / During the Track Record Period and as of the Latest Practicable Date, our Company was / controlled by Hongxing Shiye, which is our direct Controlling Shareholder controls 58.25% of the total / issued share capital of our Company and is wholly controlled by Hongxing Center. Hongxing Shiye also
  - p31: “%” / Percent / In this prospectus, the terms “associate,” “close associate,” “connected person,” “core connected / person,” “connected transaction,” “controlling shareholder” and “substantial shareholder” shall have the / meanings given to such terms in the Listing Rules, unless the context otherwise requires. / Certain amounts and percentage figures included in this prospectus have been subject 

### col_BC
  - p21: OUR CONTROLLING SHAREHOLDERS AND SHAREHOLDING STRUCTURE / During the Track Record Period and as of the Latest Practicable Date, our Company was / controlled by Hongxing Shiye, which is our direct Controlling Shareholder controls 58.25% of the total / issued share capital of our Company and is wholly controlled by Hongxing Center. Hongxing Shiye also
  - p31: “%” / Percent / In this prospectus, the terms “associate,” “close associate,” “connected person,” “core connected / person,” “connected transaction,” “controlling shareholder” and “substantial shareholder” shall have the / meanings given to such terms in the Listing Rules, unless the context otherwise requires. / Certain amounts and percentage figures included in this prospectus have been subject 

### col_BD
  - p21: OUR CONTROLLING SHAREHOLDERS AND SHAREHOLDING STRUCTURE / During the Track Record Period and as of the Latest Practicable Date, our Company was / controlled by Hongxing Shiye, which is our direct Controlling Shareholder controls 58.25% of the total / issued share capital of our Company and is wholly controlled by Hongxing Center. Hongxing Shiye also
  - p84: meeting of shareholders. / Under the Company Law, shareholders present at a shareholders’ general meeting have one vote / for each share they hold except the shareholders of classified shares. The company’s shares held by the / company are not entitled to any voting rights. / Under the Company Law, resolutions of the general meeting shall be passed by more than half of / the voting rights held by 
  - p31: “%” / Percent / In this prospectus, the terms “associate,” “close associate,” “connected person,” “core connected / person,” “connected transaction,” “controlling shareholder” and “substantial shareholder” shall have the / meanings given to such terms in the Listing Rules, unless the context otherwise requires. / Certain amounts and percentage figures included in this prospectus have been subject 

### col_BE
  - p52: an unexpected business interruption resulting from operational breakdowns, natural disasters, / or major changes in our key personnel or senior management; / • / adverse market reaction to any indebtedness that we may incur or securities that we may / issue in the future; / • / announcements of competitive developments, acquisitions or strategic alliances in our
  - p197: During the Track Record Period, we recorded finance costs of RMB3.0 million, nil, RMB1.2 / million, nil and RMB2.1 million in 2022, 2023, 2024 and the six months ended June 30, 2024 and / 2025, respectively, which primarily represented the interest accrued for our bank borrowings. For / details, see “—Indebtedness—Interest-bearing Bank Borrowings.” / Income Tax Expense / We are registered and cond
  - p156: accounts with our Controlling Shareholders and their associates. We believe that we are capable of / obtaining financing from third parties without relying on any guarantee or security provided by our / Controlling Shareholder or its associates. During the Track Record Period, we primarily finance our / business operation through cash generated from our business activities and bank borrowings. As 

### col_BF
  - p105: Provincial / Agricultural / Product / Commercialization Leading Enterprise” (湖南省農業產業化省級龍頭企業). / * / Our phase I to IV projects are to provide storage and loading services and the trading space leasing services to our / customers.
  - p13: a result, the storage capacity purchased by customers of our southern base also increased from 129,077 / tonnes as of December 31, 2023 to 186,916 tonnes as of December 31, 2024. The storage capacity / utilization rate decreased from 99.0% as of December 31, 2023 to 90.5% as of December 31, 2024, as / we were in the process of ramping up our storage capacity. The average monthly frozen food storag

### col_BG
  - p22: to be submitted to our shareholders’ meeting for approval. If we make a profit in the previous fiscal / year and our accumulative distributable profits are positive, provided that our capital requirements for / ordinary business operations are met, we shall distribute cash dividends. / FUTURE PLANS AND USE OF PROCEEDS / We estimate that the net proceeds of the Global Offering, after deducting the 
  - p215: For the year ended December 31, 2022, our net cash used in financing activities was RMB117.1 / million, primarily due to repayment of bank borrowings of RMB176.1 million and dividends paid of / RMB30.0 million, partially offset by proceeds from bank borrowings of RMB92.1 million. / INDEBTEDNESS / Our indebtedness primarily consisted of bank borrowings. The following table sets forth a
  - p22: to be submitted to our shareholders’ meeting for approval. If we make a profit in the previous fiscal / year and our accumulative distributable profits are positive, provided that our capital requirements for / ordinary business operations are met, we shall distribute cash dividends. / FUTURE PLANS AND USE OF PROCEEDS / We estimate that the net proceeds of the Global Offering, after deducting the 

### col_BI
  - p2: Number of Offer Shares under / the Global Offering / : / 23,263,000 H Shares / Number of Hong Kong Offer Shares / : / 2,326,500 H Shares (subject to reallocation)

### col_BP
  - p1: Joint Sponsors, Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers / Stock Code: 01641 / (a joint stock company incorporated in the People’s Republic of China with limited liability) / Hongxing Coldchain (Hunan) Co., Ltd. / 紅星冷鏈(湖南)股份有限公司

### col_BR
  - p70: No. 21, Section 1 Huanbao East Road / Yuhua District, Changsha City / Hunan Province, the PRC / Principal Place of Business in / Hong Kong / Room 1917, 19/F / Lee Garden One
  - p70: Registered Office in the PRC / No. 21, Section 1 Huanbao East Road / Yuhua District, Changsha City / Hunan Province, the PRC
  - p61: All of the H Shares issued pursuant to applications made in the Hong Kong Public Offering will / be registered on our H Share register of members to be maintained in Hong Kong by our H Share / Registrar, Tricor Investor Services Limited, at 17/F, Far East Finance Centre, 16 Harcourt Road, Hong / Kong. Our principal register of members will be maintained by us at our head office in the PRC. / Deali

### col_BT
  - p267: BASIS OF PREPARATION / The Historical Financial Information has been prepared in accordance with IFRS Accounting / Standards, which comprise all standards and interpretations approved by the International Accounting / Standards Board (“IASB”). All IFRS Accounting Standards effective for the accounting period / commencing from 1 January 2025, together with the relevant transitional provisions, have
  - p101: The principal laws, rules and regulations governing dividend distributions by foreign-invested / enterprises in the PRC are the Company Law, and the Foreign Investment Law and its Implementing / Regulations. Under these requirements, foreign-invested enterprises may pay dividends only out of their / accumulated profit, if any, as determined in accordance with PRC accounting standards and regulatio
  - p185: financial information has been prepared under the historical cost convention. / The preparation of the historical financial information in conformity with the IFRS requires the / use of certain critical accounting estimates. It also requires management to exercise its judgment in the / process of applying our accounting policies. The areas involving a higher degree of judgment or / complexity, or 

### col_CC
  - p5: If there is any change in the following expected timetable, we will issue an announcement in / Hong Kong on the respective websites of the Company at http://www.hnhxld.com and the Stock / Exchange at www.hkexnews.hk. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9:00 a.m. on
  - p5: If there is any change in the following expected timetable, we will issue an announcement in / Hong Kong on the respective websites of the Company at http://www.hnhxld.com and the Stock / Exchange at www.hkexnews.hk. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9:00 a.m. on / Wednesday, December 31, 2025 / Latest time for completin

### col_CD
  - p5: If there is any change in the following expected timetable, we will issue an announcement in / Hong Kong on the respective websites of the Company at http://www.hnhxld.com and the Stock / Exchange at www.hkexnews.hk. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9:00 a.m. on

### col_CE
  - p180: H Shares to be converted from Unlisted Shares . . . . . . . . . . . . . / 1,303,464 / 1,303,464 / H Shares to be issued pursuant to the Global Offering . . . . . . . . / 23,263,000 / 23,263,000 / Total
  - p4: Your application through the HK eIPO White Form service or the HKSCC EIPO channel must be / for a minimum of 500 Hong Kong Offer Shares and in one of the numbers set out in the table. If you / are applying through the HK eIPO White Form service, you may refer to the table below for the / amount payable for the number of H Shares you have selected. You must pay the respective amount / payable on ap

### col_CF
  - p10: Our financial performance demonstrates stable growth and strong profitability. We generated / revenue of RMB236.7 million, RMB201.8 million, RMB233.6 million, RMB112.3 million and / RMB118.0 million in 2022, 2023, 2024 and the six months ended June 30, 2024 and 2025, respectively, / with a gross profit margin of 50.1%, 57.7%, 52.8%, 54.2% and 53.3% during the same periods, / respectively. Our net 
  - p10: Our financial performance demonstrates stable growth and strong profitability. We generated / revenue of RMB236.7 million, RMB201.8 million, RMB233.6 million, RMB112.3 million and / RMB118.0 million in 2022, 2023, 2024 and the six months ended June 30, 2024 and 2025, respectively, / with a gross profit margin of 50.1%, 57.7%, 52.8%, 54.2% and 53.3% during the same periods, / respectively. Our net 

### col_CG
  - p21: any failure to compete effectively could adversely affect our customer base, profitability and market / share; (3) reduction of our customers’ expenditure in third-party frozen food storage services; (4) our / failure to meet evolving customer demands and expectations, as well as our ability to attract and retain / customers; (5) our substantial capital expenditures, which may not generate returns
  - p21: any failure to compete effectively could adversely affect our customer base, profitability and market / share; (3) reduction of our customers’ expenditure in third-party frozen food storage services; (4) our / failure to meet evolving customer demands and expectations, as well as our ability to attract and retain / customers; (5) our substantial capital expenditures, which may not generate returns
  - p19: net current assets of RMB95.6 million as of December 31, 2022. The change was primarily due to an / increase in the current portion of other payables and accruals from RMB57.2 million as of December / 31, 2022 to RMB209.8 million as of December 31, 2023, mainly as a result of the increase in payable / for purchase of property, plant and equipment for our Phase V Expansion Project. Our net current 

### col_CH
  - p258: Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the accountants’ / report, a true and fair view of the financial position of the Group and the Company as at 31 December / 2022, 2023 and 2024 and 30 June 2025 and of the financial performance and cash flows of the Group / for each of the Relevant Periods in accordance with the basis of preparation set out in
  - p15: environment. / SUMMARY HISTORICAL FINANCIAL INFORMATION / The following tables set forth summary of our financial information for the Track Record Period, / and should be read together with the consolidated financial statements in the Accountants’ Report set / out in Appendix I to this prospectus, including the accompanying notes and the information set forth in / “Financial Information.” Our cons

### col_CI
  - p21: “Risk Factors” section in its entirety before you decide to invest in our Shares. / WAIVERS AND EXEMPTIONS / See “Waivers from Strict Compliance with the Listing Rules” for details. / LISTING EXPENSES / We did not record any listing expenses in connection with the Global Offering for 2022, 2023 and / 2024, and we recorded listing expenses of RMB0.5 million for the six months ended June 30, 2025. W
  - p21: “Risk Factors” section in its entirety before you decide to invest in our Shares. / WAIVERS AND EXEMPTIONS / See “Waivers from Strict Compliance with the Listing Rules” for details. / LISTING EXPENSES / We did not record any listing expenses in connection with the Global Offering for 2022, 2023 and / 2024, and we recorded listing expenses of RMB0.5 million for the six months ended June 30, 2025. W


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 1641.HK`
有 ERROR 必须回原文修正。
