# 6809.HK 扩展 18 列抽取包

公司：6809.HK Montage Technology Co., Ltd. - H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB6809.json`。
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
- 股本结构（**已确认，不要改**）：L=1212316521 M=65890000 N=1146426521 O=1146426521 P=0 Q=65890000 R=59301000 S=6589000
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = 2101820000
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
{"code":"6809.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  6809.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 6809.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
（锚点无命中，需要自己 search）

### col_BB
  - p109: under Rules 14.58 and 14.60 of the Listing Rules on each acquisition. In this regard, / “unduly burdensome” will be assessed based on each new applicant’s specific facts / and circumstances (e.g. why the financial information of the acquisition target is not / available and whether the new applicant or its controlling shareholder has sufficient / control or influence over the seller to gain access
  - p44: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / DEFINITIONS / – 34 –
  - p109: not have any significant influence over the underlying company or business to which / Rule 4.04(2) and 4.04(4) of the Listing Rules relate, and has disclosed in its listing / document the reasons for the acquisition and a confirmation that the counterparties / and their respective ultimate beneficial owners are independent of the new applicant / and its connected persons. In this regard, “control”

### col_BC
  - p109: under Rules 14.58 and 14.60 of the Listing Rules on each acquisition. In this regard, / “unduly burdensome” will be assessed based on each new applicant’s specific facts / and circumstances (e.g. why the financial information of the acquisition target is not / available and whether the new applicant or its controlling shareholder has sufficient / control or influence over the seller to gain access
  - p44: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / DEFINITIONS / – 34 –

### col_BD
  - p109: under Rules 14.58 and 14.60 of the Listing Rules on each acquisition. In this regard, / “unduly burdensome” will be assessed based on each new applicant’s specific facts / and circumstances (e.g. why the financial information of the acquisition target is not / available and whether the new applicant or its controlling shareholder has sufficient / control or influence over the seller to gain access
  - p117: We have applied for, and the Stock Exchange has granted, a waiver from strict compliance / with Rule 10.04 of, and a consent under paragraph 1C(2) of Appendix F1 to the Listing Rules / to permit H Shares in the International Offering to be placed to certain existing minority / Shareholders who (i) hold less than 5% of the voting rights in our Company prior to the / completion of the Global Offerin
  - p44: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / DEFINITIONS / – 34 –

### col_BE
  - p32: foundation for memory pooling and sharing in next-generation computing infrastructure. / NO MATERIAL ADVERSE CHANGE / Our Directors have confirmed that as of the date of this Prospectus, there has been no / material adverse change in our financial, operational or trading position, indebtedness, / contingent liabilities or prospects between October 1, 2025 (being the date after the end date / of ou
  - p309: typically range from 30 to 60 days. We seek to maintain strict control over our outstanding / receivables. Overdue balances are reviewed regularly by senior management. We do not hold / any collateral or other credit enhancements over our trade receivable balances. The balances / of trade receivables are non-interest-bearing. / Our trade receivables decreased from RMB322.4 million as of December 3
  - p317: million, RMB16.0 million and RMB15.7 million, respectively, as of December 31, 2022, 2023 / and 2024 and September 30, 2025. / Except as discussed above, we had no outstanding indebtedness or any loan capital issued / and outstanding or agreed to be issued, bank overdrafts, term-loans, other borrowings or / similar indebtedness, liabilities under acceptances (other than normal trade bills), accept

### col_BF
  - p16: accounting for over 90% of the total market share. Among them, the Company ranked first with / a 36.8% market share, according to Frost & Sullivan. These companies have established strong / technical barriers based on years of R&D, deep understanding of industry standards, and / extensive experience in product design and commercialization. In addition, they have built / long-term and robust relati
  - p149: Their ability to support complex system-level interconnect topology further reinforces their / market competitiveness. Meanwhile, CXL interconnect technology remains an emerging field. / Although adoption and ecosystem development are gradually progressing, chips based on CXL / have yet to reach mass production, and the market is still in its early stage. / Ethernet and optical interconnect chip m
  - p92: of other companies with business operations located mainly in mainland China that have listed / their securities in Hong Kong may affect the volatility in the price of and trading volumes for / our H Shares. A number of mainland China-based companies have listed their securities, and / some are in the process of preparing for listing their securities, in Hong Kong. Some of these / companies have e

### col_BG
  - p30: Forma Financial Information” and on the basis that 1,212,316,521 Shares were in issue assuming the / Global Offering had been completed on September 30, 2025 and do not take into account any Shares / which may be sold and offered upon exercise of the Over-allotment Option. / FUTURE PLANS AND USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately /
  - p30: Forma Financial Information” and on the basis that 1,212,316,521 Shares were in issue assuming the / Global Offering had been completed on September 30, 2025 and do not take into account any Shares / which may be sold and offered upon exercise of the Over-allotment Option. / FUTURE PLANS AND USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately /

### col_BI
  - p2: Number of Offer Shares under / the Global Offering / : / 65,890,000 H Shares (subject to / the Over-allotment Option) / Number of Hong Kong Offer Shares / :

### col_BP
  - p268: profound background in the semiconductor industry and investment. There is no shareholder / holding 30% or more of the shareholding interests in Huadeng Technology. / PSBC Wealth / PSBC Wealth Management Co., Ltd. (“PSBC Wealth”) was established on December 18, / 2019, with a registered capital of RMB8.0 billion, in which Postal Savings Bank of China Co., / Ltd., a company listed on the Main Board
  - p1: Stock Code : 6809 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / GLOBAL / OFFERING / Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators,

### col_BR
  - p130: Registered Office, Headquarters and / Principal Place of Business in the PRC / 15th Floor, Building 1 / No. 181 Caobao Road / Xuhui District, Shanghai
  - p130: Registered Office, Headquarters and / Principal Place of Business in the PRC / 15th Floor, Building 1 / No. 181 Caobao Road

### col_BT
  - p111: amongst others, flash memory chips, niche dynamic random access memory, micro control / units, analog chips and sensor chips. / According to the financial statements of Company Y audited by its reporting accountant / pursuant to the requirements of IFRS Accounting Standards as set out in the listing document / of Company Y: / As of December 31, / As of
  - p38: issued / by / the / International Accounting Standards Committee (IASC) / “IIT Law” / the Individual Income Tax Law of the PRC (《中華人民 / 共和國個人所得稅法》)
  - p277: BASIS OF PRESENTATION AND PREPARATION / The consolidated financial statements of the Group for the Track Record Period, on which / the Historical Financial Information is based, have been prepared in accordance with the / accounting policies which conform with IFRS Accounting standards (“IFRSs”) issued by / International Accounting Standards Board (“IASB”). For details of the basis of preparation,

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on the Company’s / website / at
  - p5: Exchange / at / www.hkexnews.hk. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on / Friday, January 30, 2026 / Latest time to complete electronic applications / under the White Form eIPO service through

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on the Company’s / website / at

### col_CE
  - p121: APPLICATION FOR LISTING OF THE H SHARES ON THE HONG KONG STOCK / EXCHANGE / We have applied to the Hong Kong Stock Exchange for the granting of listing of, and / permission to deal in, our H Shares to be issued pursuant to the Global Offering (including any / H Shares which may be issued pursuant to the exercise of the Over-allotment Option). / INFORMATION ABOUT THIS PROSPECTUS AND THE GLOBAL OFFE
  - p113: (a) / The requested waiver would not prejudice the interests of the investing public. / i. / the total number of H shares of Company X and Company Y and shares of / Marvell Technology that we acquired after the Track Record Period only / represented approximately 0.02% of the enlarged issued share capital of each / of Company X and Company Y, respectively, and less than 0.035% of the

### col_CF
  - p13: and RMB4,057.7 million in 2022, 2023, 2024, and the nine months ended September 30, 2025, / respectively. Our newly launched interconnect chips including PCIe Retimer, MRCD/MDB and / CKD generated revenue of RMB422.5 million in 2024. Additionally, we have maintained a / robust margin profile, supported by continuous product innovation. Our overall gross profit / margin was 46.4%, 58.9%, 58.1% and 
  - p13: and RMB4,057.7 million in 2022, 2023, 2024, and the nine months ended September 30, 2025, / respectively. Our newly launched interconnect chips including PCIe Retimer, MRCD/MDB and / CKD generated revenue of RMB422.5 million in 2024. Additionally, we have maintained a / robust margin profile, supported by continuous product innovation. Our overall gross profit / margin was 46.4%, 58.9%, 58.1% and 

### col_CG
  - p29: We intend to finance our future working capital requirements and capital expenditures / primarily from cash expected to be generated from operating activities and funds raised from / financing activities, including the net proceeds we will receive from the Global Offering. / LISTING EXPENSES
  - p29: We intend to finance our future working capital requirements and capital expenditures / primarily from cash expected to be generated from operating activities and funds raised from / financing activities, including the net proceeds we will receive from the Global Offering. / LISTING EXPENSES
  - p313: Other Payables and Accruals / Our other payables and accruals consist of (i) payroll and welfare payable, (ii) dividends / payable, (iii) payables for purchase of property, plant and equipment, (iv) warranty, (v) / professional services and consulting fees, (vi) deposits and (vii) others. As of December 31, / 2022, 2023 and 2024 and September 30, 2025, all other payables were unsecured, non-intere

### col_CH
  - p369: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the / accountants’ report, a true and fair view of the financial position of the Group and the Company / as at 31 December 2022, 2023 and 2024 and 30 September 2025, and of the financial / perfo
  - p18: Customers.” / SUMMARY OF HISTORICAL FINANCIAL INFORMATION / The following tables set forth summary financial data from our consolidated financial / information for the Track Record Period, extracted from the Accountants’ Report set out in / Appendix I to this Prospectus. The summary consolidated financial data set forth below should / be read together with, and is qualified in its entirety by refe

### col_CI
  - p12: 1. / According to Frost & Sullivan / 2. / Profit for the periods adjusted by adding back (i) share-based payments, and (ii) listing expenses, which relate / to the Global Offering. / Interconnectivity plays an increasingly vital role in data transmission with the evolvement / of modern data infrastructure. As processing power accelerated at a remarkable rate, it created
  - p12: 1. / According to Frost & Sullivan / 2. / Profit for the periods adjusted by adding back (i) share-based payments, and (ii) listing expenses, which relate / to the Global Offering. / Interconnectivity plays an increasingly vital role in data transmission with the evolvement / of modern data infrastructure. As processing power accelerated at a remarkable rate, it created


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 6809.HK`
有 ERROR 必须回原文修正。
