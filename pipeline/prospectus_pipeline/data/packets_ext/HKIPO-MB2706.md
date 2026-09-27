# 2706.HK 扩展 18 列抽取包

公司：2706.HK Beijing Haizhi Technology Group Co., Ltd. - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB2706.json`。
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
- 股本结构（**已确认，不要改**）：L=400430680 M=28030200 N=372400480 O=372400480 P=0 Q=28030200 R=25227000 S=2803200
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = -281092000
- 行业分类（港交所官方）：702015 數碼解決方案服務
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
{"code":"2706.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  2706.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 2706.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p57: “PRC Legal Advisor” / Zhong Lun Law Firm, legal advisor to our Company as to / PRC Law / “Pre-IPO Investments” / the investments in our Company undertaken by the / Pre-IPO Investors pursuant to the relevant investment / agreements and/or capital increase agreements, details of
  - p32: We adjust changes in the fair value of financial liabilities at fair value through profit or loss because it / was non-cash in nature. Our changes in the fair value of financial liabilities at fair value through profit / or loss was related to the derivative financial liabilities arising from anti-dilution rights granted to / Pre-IPO Investors. These anti-dilution rights will be terminated upon Li
  - p57: “PRC Legal Advisor” / Zhong Lun Law Firm, legal advisor to our Company as to / PRC Law / “Pre-IPO Investments” / the investments in our Company undertaken by the / Pre-IPO Investors pursuant to the relevant investment / agreements and/or capital increase agreements, details of

### col_BB
  - p158: economy in the past three years; (iv) the domestic company is currently under investigations / for suspicion of criminal offenses or major violations of laws and regulations which have not / definitive conclusion; or (v) there are material ownership disputes over equity held by the / domestic company’s controlling shareholder(s) or by other shareholder(s) that are controlled by / the controlling s
  - p47: — / Further / Information About Our Directors, Chief Executive and / Substantial Shareholders — 5. Equity Incentive Scheme” / in this prospectus / “Extreme Conditions” / the occurrence of “extreme conditions” as announced by
  - p200: Set out below is a description of our major Pre-IPO Investors which held 1% or more of / our total issued Shares as of the Latest Practicable Date. Save as disclosed below, to the best / knowledge of our Directors, each of our Pre-IPO Investors and where applicable, their / respective general partner(s), limited partner(s) and ultimate beneficial owner(s) is an / Independent Third Party. / 1. / Ju

### col_BC
  - p158: economy in the past three years; (iv) the domestic company is currently under investigations / for suspicion of criminal offenses or major violations of laws and regulations which have not / definitive conclusion; or (v) there are material ownership disputes over equity held by the / domestic company’s controlling shareholder(s) or by other shareholder(s) that are controlled by / the controlling s
  - p47: — / Further / Information About Our Directors, Chief Executive and / Substantial Shareholders — 5. Equity Incentive Scheme” / in this prospectus / “Extreme Conditions” / the occurrence of “extreme conditions” as announced by

### col_BD
  - p158: economy in the past three years; (iv) the domestic company is currently under investigations / for suspicion of criminal offenses or major violations of laws and regulations which have not / definitive conclusion; or (v) there are material ownership disputes over equity held by the / domestic company’s controlling shareholder(s) or by other shareholder(s) that are controlled by / the controlling s
  - p341: Company since March 2, 2021, and agreed further that if the Concert Parties have / disagreements on the major issues of our Company, the Concert Parties will cast votes on such / major issues and shall act in accordance with the direction of the Concert Party with a higher / total number of voting rights (including direct and indirect shareholdings, as well as the / number of shares that would be 
  - p47: — / Further / Information About Our Directors, Chief Executive and / Substantial Shareholders — 5. Equity Incentive Scheme” / in this prospectus / “Extreme Conditions” / the occurrence of “extreme conditions” as announced by

### col_BE
  - p39: Current ratio equals current assets divided by current liabilities as of the same date. Our current ratio / decreased from 1.1 times in 2022 to 0.4 times in 2023, and further decreased to 0.3 times in 2024, / primarily due to the increase in redemption liabilities during the Track Record Period, see “— / Indebtedness — Redemption Liabilities”. Our current ratio remained stable at 0.3 times as of D
  - p432: basis. / To the extent that the net proceeds of the Global Offering are not immediately used for / the above purposes or if we are unable to effect any part of our future development plans as / intended, we will deposit such funds into short-term interest-bearing accounts at licensed / commercial banks and/or other authorized financial institutions (as defined under the / Securities and Futures Or
  - p410: Our Directors confirm that, there was no material covenant on any of our outstanding debt / as of the Latest Practicable Date, and there was no breach of any covenants during the Track / Record Period and up to the Latest Practicable Date. Our Directors further confirm that we did / not experience any default in payment of bank loans and other borrowings, breach of / covenants, difficulty in obtai

### col_BF
  - p24: closely to deliver high-quality products and services for customers, innovate sustainably and / continually expand the technology boundaries. / Our R&D and technical team consists of dedicated talents with profound industry / expertise, focusing on developing and commercializing the solutions that help maintain our / technological advantages and market competitiveness. Each of our core R&D and tec
  - p76: Any flaws or misuse of AI technologies, whether actual or perceived, intended or / inadvertent, committed by us or by other third parties, could have a material adverse / effect on our reputation, business, financial condition, results of operations and prospects. / AI technologies are in the process of development and continue to evolve. Similar to / many disruptive innovations, AI technologies p

### col_BG
  - p42: USE OF PROCEEDS / After deducting the underwriting commissions and other estimated offering expenses / payable by us in connection with the Global Offering, and assuming an Offer Price of / HK$26.80 per Share (being the mid-point of the indicative Offer Price range of HK$25.60 and
  - p42: • / approximately 10.0%, or HK$64.8 million, will be used for working capital and / general corporate purposes. / See “Future Plans and Use of Proceeds” for details. / LOSS ESTIMATE FOR THE YEAR ENDED DECEMBER 31, 2025 / The following loss estimate has been prepared based on the audited consolidated results / of our Group for the nine months ended September 30, 2025 and the unaudited consolidated

### col_BI
  - p2: Number of Offer Shares under the / Global Offering / : / 28,030,200 H Shares / Number of Hong Kong Offer Shares / : / 2,803,200 H Shares (subject to

### col_BP
  - p46: “Company” or “our Company” / Beijing Haizhi Technology Group Co., Ltd. (北京海致科 / 技集團股份有限公司), a joint stock limited company / established in the PRC, which was initially established on / August 23, 2013 as a limited liability company and / formerly known as Beijing Haizhi Wangju Information / Technology Co., Ltd.* (北京海智網聚信息技術有限公
  - p1: OFFERING / Joint Sponsors, Overall Coordinators, Joint Global Coordinators, / Joint Bookrunners and Joint Lead Managers / (A joint stock company incorporated in the People’s Republic of China with limited liability) / Stock Code : 2706 / 北京海致科技集團股份有限公司 / Beijing Haizhi Technology Group Co., Ltd.

### col_BR
  - p125: Development Area / Beijing / PRC / Principal place of business in PRC / Room 1501, 15th Floor / Building 8, No. 8, Kegu First Street / Beijing Economic-Technological
  - p125: Registered office and headquarter / Room 1501, 15th Floor / Building 8, No. 8, Kegu First Street / Beijing Economic-Technological
  - p315: practice. During the Track Record Period, we did not make any material insurance claims in / relation to our business. / PROPERTIES / Our head office is located in Beijing, and we lease properties in the PRC. As of the Latest / Practicable Date, none of the properties held or leased by us had a carrying value of 15% or / more of our consolidated total assets. According to section 6(2) of the Compa

### col_BT
  - p31: Non-IFRS Measure / To supplement our consolidated financial statements which are presented in accordance / with IFRS Accounting Standards, we also use adjusted net loss or profit (non-IFRS measure) / as additional financial measures, which are not required by or presented in accordance with / IFRS Accounting Standards. We believe that these non-IFRS measures facilitate comparisons / of operating p
  - p31: Non-IFRS Measure / To supplement our consolidated financial statements which are presented in accordance / with IFRS Accounting Standards, we also use adjusted net loss or profit (non-IFRS measure) / as additional financial measures, which are not required by or presented in accordance with / IFRS Accounting Standards. We believe that these non-IFRS measures facilitate comparisons / of operating p
  - p42: of our Group for the nine months ended September 30, 2025 and the unaudited consolidated / results based on the management accounts of our Group for the three months ended December / 31, 2025. The Loss Estimate has been prepared on a basis consistent in all material respects / with the accounting policies normally adopted by our Group as set out in the Accountants’ / Report as set out in Appendix 

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on the / Company’s website at www.haizhi.com and the website of the Stock Exchange at / www.hkexnews.hk.
  - p5: Offering, we will issue an announcement in Hong Kong to be published on the / Company’s website at www.haizhi.com and the website of the Stock Exchange at / www.hkexnews.hk. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on / Thursday, / February 5, 2026 / Latest time for completing electronic applications

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on the / Company’s website at www.haizhi.com and the website of the Stock Exchange at / www.hkexnews.hk.

### col_CE
  - p39: “— Description of Major Components of Our Results of Operations — Non-IFRS Measure”. / APPLICATION FOR LISTING ON THE STOCK EXCHANGE / We have applied to the Hong Kong Stock Exchange for the granting of listing of, and / permission to deal in, (i) our H Shares to be issued pursuant to the Global Offering and (ii) the / H Shares to be converted from our existing Unlisted Shares on the basis that, a
  - p4: channel must be for a minimum of 200 Hong Kong Offer Shares and in one of the / numbers set out in the table. / If you are applying through the White Form eIPO service, you may refer to the / table below for the amount payable for the number of H Shares you have selected. You / must pay the respective maximum amount payable on application in full upon / application for Hong Kong Offer Shares. / If

### col_CF
  - p30: 249,074 / Cost of sales              / (216,128) (243,313) (320,736) (151,670) (150,179) / Gross profit               / 96,864 / 132,260 / 182,393
  - p30: 249,074 / Cost of sales              / (216,128) (243,313) (320,736) (151,670) (150,179) / Gross profit               / 96,864 / 132,260 / 182,393

### col_CG
  - p70: • / our business operations and prospects; / • / our capital expenditure plans; / • / weather, natural disasters and climate change; / •
  - p70: • / our business operations and prospects; / • / our capital expenditure plans; / • / weather, natural disasters and climate change; / •

### col_CH
  - p474: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purpose of the / accountants’ report, a true and fair view of the Company’s and the Group’s financial position / as at 31 December 2022, 2023 and 2024 and 30 September 2025 and of the Group’s financial / pe
  - p29: The tables below present our summary consolidated financial data derived from our / consolidated statements of profit or loss and other comprehensive income and consolidated / statements of cash flows for the years or periods ended December 31, 2022, 2023, 2024 and / the nine months ended September 30, 2024 and 2025 included in the Accountants’ Report in / Appendix I to this prospectus. The follow

### col_CI
  - p31: 76,092 / 74,090 / 102,642 / – Listing expenses(4)        / – / – / –
  - p31: 76,092 / 74,090 / 102,642 / – Listing expenses(4)        / – / – / –


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 2706.HK`
有 ERROR 必须回原文修正。
