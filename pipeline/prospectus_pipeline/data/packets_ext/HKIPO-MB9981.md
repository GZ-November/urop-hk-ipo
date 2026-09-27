# 9981.HK 扩展 18 列抽取包

公司：9981.HK Shenzhen Woer Heat-Shrinkable Material Co., Ltd. - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB9981.json`。
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
- 股本结构（**已确认，不要改**）：L=1399887362 M=139988800 N=1259898562 O=1259898562 P=0 Q=139988800 R=125989800 S=13999000
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = 1177737333.3333333
- 行业分类（港交所官方）：101020 工業零件及器材
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
{"code":"9981.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  9981.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 9981.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
（锚点无命中，需要自己 search）

### col_BB
  - p51: transaction value or US$377,700 (as such amount may be adjusted for inflation), and — for willful violations — / criminal penalties of fines of up to US$1 million and imprisonment of up to 20 years. Because the OISP regulates / U.S. persons and, in some cases, U.S. persons controlling or directing nonU.S. person-investors, and not the / entities they are investing in, none of the Company, the Cont
  - p16: As such, as of the Latest Practicable Date, each of Mr. Zhou and Ms. Yi Huarong is interested in / 189,563,801 A Shares, representing approximately 15.05% of the total issued Shares of our Company (including / 10,283,600 treasury A Shares), and Mr. Zhou, Ms. Yi and the Tongyi Funds constitute a group of single largest / shareholder of the Company. For details, see “Substantial Shareholders”. / THE
  - p220: knowledge after having made all reasonable inquiries, each of the HTCI Ultimate Clients (Greenwoods) is an / independent third party of (i) the Company, the connected persons or associates thereof, and (ii) HTCI, and the / companies which are members of the same group of Huatai Financial Holdings (Hong Kong) Limited / (“Huatai”), and no single ultimate beneficial owner holds 30% or more interests 

### col_BC
  - p51: transaction value or US$377,700 (as such amount may be adjusted for inflation), and — for willful violations — / criminal penalties of fines of up to US$1 million and imprisonment of up to 20 years. Because the OISP regulates / U.S. persons and, in some cases, U.S. persons controlling or directing nonU.S. person-investors, and not the / entities they are investing in, none of the Company, the Cont
  - p16: As such, as of the Latest Practicable Date, each of Mr. Zhou and Ms. Yi Huarong is interested in / 189,563,801 A Shares, representing approximately 15.05% of the total issued Shares of our Company (including / 10,283,600 treasury A Shares), and Mr. Zhou, Ms. Yi and the Tongyi Funds constitute a group of single largest / shareholder of the Company. For details, see “Substantial Shareholders”. / THE

### col_BD
  - p51: transaction value or US$377,700 (as such amount may be adjusted for inflation), and — for willful violations — / criminal penalties of fines of up to US$1 million and imprisonment of up to 20 years. Because the OISP regulates / U.S. persons and, in some cases, U.S. persons controlling or directing nonU.S. person-investors, and not the / entities they are investing in, none of the Company, the Cont
  - p76: We have applied for, and the Stock Exchange has granted, a waiver from strict compliance with Rule 10.04 / of, and a consent under paragraph 1C(2) of Appendix F1 to the Listing Rules to permit H Shares in the / International Offering to be placed to certain existing minority Shareholders who (i) hold less than 5% of the / voting rights in our Company prior to the completion of the Global Offering 
  - p16: As such, as of the Latest Practicable Date, each of Mr. Zhou and Ms. Yi Huarong is interested in / 189,563,801 A Shares, representing approximately 15.05% of the total issued Shares of our Company (including / 10,283,600 treasury A Shares), and Mr. Zhou, Ms. Yi and the Tongyi Funds constitute a group of single largest / shareholder of the Company. For details, see “Substantial Shareholders”. / THE

### col_BE
  - p63: parties, and the amount of cash flow from our operations. If our resources are insufficient to satisfy our cash / requirements, we may seek additional financing through selling additional equity or debt securities or obtaining a / credit facility. The sale of additional equity securities could result in additional dilution to our Shareholders. The / incurrence of indebtedness would result in incre
  - p181: 4.5% / 2010 / 75 days; / interest-bearing / note or wire / transfer / 2
  - p15: RMB2,056.4 million as of December 31, 2022, 2023 and 2024 and September 30, 2025, respectively. The / increase in our net current assets during the Track Record Period were mainly attributed to increase in trade and / other receivable in line with growth in our revenue and increase in bank balances and cash, as well as decrease in / bank and other borrowings, the effect of which are partially offs

### col_BF
  - p131: We are one of the largest manufacturers of heat-shrinkable materials and telecoms cable products in the / world, enjoying rapid growth in line with strong expansion of high-speed data communication and electrical / power transmission industries in recent years. We had a successful track record of taking the lead in launching / premium products, exhibiting outstanding technology commercialization b
  - p119: 示範企業) / 2024 / We completed the development of 224G single-channel high-speed copper cables, which served / as the basis for initiating mass production. / We also launched mass production of 800G multi-channel high-speed copper cables. / We completed the development of 1600G multi-channel high-speed copper cables. / – 111 –
  - p53: RISK FACTORS / We have a certain number of dispatched workers. Any labor shortages, labor disputes or occurrence of / accidents and/or product quality issues arising in the process of labor outsourcing and labor dispatching / could result in a material and adverse effect on our business, financial condition and results of operations. / We have a certain number of dispatched workers. We may experie

### col_BG
  - p17: timing or the sequence of the potential spin-offs. We cannot assure you that any spin-off will ultimately be / consummated, whether within the three-year period after the Listing or otherwise, and any such spin-off will be / subject to, among other things, market conditions and Shareholders’ approval at the time. / USE OF PROCEEDS / We estimate the net proceeds of the Global Offering which we will
  - p266: disposal of property, plant and equipment and other assets of RMB31.3 million. / Net Cash Flows (Used in)/From Financing Activities / Net cash flows used in financing activities were RMB209.2 million in the nine months ended in / September 30, 2025, primarily consisting of (i) repayment of borrowings of RMB765.3 million, and (ii) payment / for acquisition of additional interests in subsidiaries of
  - p17: • / 10%, or approximately HK$273.4 million will be used for the working capital and general corporate / purposes. / For more details, see “Future Plans and Use of Proceeds” in this prospectus. / LISTING EXPENSES / Listing expenses to be borne by us are estimated to be approximately RMB70.6 million (HK$78.8 million) / (including

### col_BI
  - p215: 1,399,887,362 / 100.00 / Note: (1) These A Shares include 10,283,600 A Shares which are held by our Company as treasury A Shares. / SHARE CLASSES / Upon the completion of the Global Offering, the Shares will consist of A Shares and H Shares. The A / Shares and H Shares are all ordinary Shares in the share capital of the Company. Apart from certain qualified / domestic institutional investors in Ch
  - p2: (A joint stock company incorporated in the People’s Republic of China with limited liability) / Global Offering / Number of Offer Shares under the Global Offering : / 139,988,800 H Shares / Number of Hong Kong Offer Shares : / 13,999,000 H Shares (subject to reallocation) / Number of International Offer Shares :

### col_BP
  - p323: (c) / No statutory financial statements for the years ended December 31, 2022, 2023 and 2024 were issued. / (d) / The entity was established on April 1, 2022. No statutory financial statements for the period ended December 31, 2022 and for the / years ended December 31, 2023 and 2024 were available as there was no requirements to issue audited accounts by the local / authorities. The Group directl
  - p1: Stock Code: 9981 / (A joint stock company incorporated in the People's Republic of China with limited liability) / * / 岑㏔䄬婘撨劭免罆♷僗꡿⪝⺚ / 4)&/;)&/80&3)&"54)3*/,"#-&."5&3*"-$0

### col_BR
  - p86: Shenzhen / Guangdong / PRC / Principal Place of Business in Hong Kong / Room 504, 5/F, / Cheong Tai Commercial Building / 60–66 Wing Lok Street
  - p86: CORPORATE INFORMATION / Registered Office, Headquarters and Principal Place / of Business in the PRC / No. 53, Qingsong Road / Pingshan District

### col_BT
  - p9: We believe these achievements stem from our continuous investment in product innovation. As of / September 30, 2025, we held 547 invention patents. Leveraging our well-recognized product quality and leading / market position, we have achieved strong growth during the Track Record Period. Based on financial reports / prepared in accordance with IFRS Accounting Standards, our revenue grow from RMB5,
  - p9: We believe these achievements stem from our continuous investment in product innovation. As of / September 30, 2025, we held 547 invention patents. Leveraging our well-recognized product quality and leading / market position, we have achieved strong growth during the Track Record Period. Based on financial reports / prepared in accordance with IFRS Accounting Standards, our revenue grow from RMB5,
  - p176: addition, in line with our distributor management policies, we conduct regular review on performance, market / feedback and interview results from end customers of distributors. We also dispatch employees to visit / distributors’ office premises on regular or ad hoc basis to verify information provided by our distributors, in line / with our financial and accounting policies. In line with our poli

### col_CC
  - p4: EXPECTED TIMETABLE(1) / If there is any change to the expected timetable of the Hong Kong Public Offering, we will issue an / announcement on the respective websites of the Company at www.woer.com and the Stock Exchange at / www.hkexnews.hk.
  - p4: If there is any change to the expected timetable of the Hong Kong Public Offering, we will issue an / announcement on the respective websites of the Company at www.woer.com and the Stock Exchange at / www.hkexnews.hk. / The Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . / 9:00 a.m. on / Thursday, February 5, 2026 / Latest time to complete electronic appli

### col_CD
  - p4: EXPECTED TIMETABLE(1) / If there is any change to the expected timetable of the Hong Kong Public Offering, we will issue an / announcement on the respective websites of the Company at www.woer.com and the Stock Exchange at / www.hkexnews.hk.

### col_CE
  - p80: and sold, and will not be offered and sold, directly or indirectly, in the PRC or the United States. / APPLICATION FOR LISTING OF THE H SHARES ON THE HONG KONG STOCK EXCHANGE / We have applied to the Hong Kong Stock Exchange for the granting of listing of, and permission to deal in, / our H Shares to be issued pursuant to the Global Offering. / Except as otherwise disclosed in this prospectus and 
  - p3: Hong Kong Offer Shares and in multiples of that number of Hong Kong Offer Shares as set out in the table below. No application / for any other number of Hong Kong Offer Shares will be considered and such an application is liable to be rejected. / If you are applying through the White Form eIPO service, you may refer to the table below for the amount payable for the / number of H Shares you have se

### col_CF
  - p13: 4,815,515 100.0 / 6,076,678 100.0 / Cost of sales . . . . . . . . . (3,724,687) (69.8) (3,930,200) (68.7) (4,809,739) (69.5) (3,320,800) (69.0) (4,198,941) (69.1) / Gross profit . . . . . . . . . / 1,611,962 / 30.2 / 1,788,641
  - p13: 4,815,515 100.0 / 6,076,678 100.0 / Cost of sales . . . . . . . . . (3,724,687) (69.8) (3,930,200) (68.7) (4,809,739) (69.5) (3,320,800) (69.0) (4,198,941) (69.1) / Gross profit . . . . . . . . . / 1,611,962 / 30.2 / 1,788,641

### col_CG
  - p42: RISK FACTORS / Our expenditure may not be fully recovered if the major capital expenditure projects under our expansion / program are not completed within the expected time frame and budget, or at all, and may not achieve the / intended economic results even if completed. / Our operations depend on the continuous maintenance, upgrades and expansion of production capacity to
  - p42: RISK FACTORS / Our expenditure may not be fully recovered if the major capital expenditure projects under our expansion / program are not completed within the expected time frame and budget, or at all, and may not achieve the / intended economic results even if completed. / Our operations depend on the continuous maintenance, upgrades and expansion of production capacity to
  - p319: FVTPL . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . / 80,093 / 200,345 2,062,406 1,230,897 1,152,913 / Purchase of property, plant and equipment . . . . . / (376,277) / (302,716) / (516,571)

### col_CH
  - p307: We believe that the evidence we have obtained is sufficient and appropriate to provide a basis for our / opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the accountants’ report, a true / and fair view of the consolidated financial position of the Group as at December 31, 2022, 2023 and 2024 and / September 30, 2025 and of the financial position 
  - p12: SUMMARY OF HISTORICAL FINANCIAL INFORMATION / This summary of key financial information set forth below has been derived from, and should be read in / conjunction with, our consolidated audited financial statements, including the accompanying notes, set forth in / the Accountants’ Report set out in Appendix I to this prospectus, as well as the information set forth in the / section headed “Financi

### col_CI
  - p17: 10%, or approximately HK$273.4 million will be used for the working capital and general corporate / purposes. / For more details, see “Future Plans and Use of Proceeds” in this prospectus. / LISTING EXPENSES / Listing expenses to be borne by us are estimated to be approximately RMB70.6 million (HK$78.8 million) / (including / underwriting
  - p17: 10%, or approximately HK$273.4 million will be used for the working capital and general corporate / purposes. / For more details, see “Future Plans and Use of Proceeds” in this prospectus. / LISTING EXPENSES / Listing expenses to be borne by us are estimated to be approximately RMB70.6 million (HK$78.8 million) / (including / underwriting


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 9981.HK`
有 ERROR 必须回原文修正。
