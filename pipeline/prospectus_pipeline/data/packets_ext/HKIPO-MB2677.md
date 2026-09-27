# 2677.HK 扩展 18 列抽取包

公司：2677.HK Distinct Healthcare Holdings Limited

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB2677.json`。
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
- 股本结构（**已确认，不要改**）：L=64384350 M=4750000 N=59634350 O=59634350 P=0 Q=4750000 R=4275000 S=475000
- 财务期间（**已确认**）：year-1 期末 = 31/08/25；币种 = RMB；year-1 净利 = 124816500
- 行业分类（港交所官方）：282020 醫療及醫學美容服務
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
{"code":"2677.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  2677.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 2677.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p29: Pre-IPO Investments — Special Rights of the Pre-IPO Investors” and Note 27 to the / Accountant’s Report in Appendix I to this prospectus. As the convertible redeemable / preference shares will be re-designated from liabilities to equity as a result of the automatic / conversion into ordinary Shares upon Listing, we expect our net liability and net current
  - p28: We had total liabilities of RMB2,505.2 million, RMB2,880.0 million, RMB3,084.7 / million and RMB2,985.9 million as of December 31, 2022, 2023 and 2024 and August 31, / 2025, respectively. The changes in total liabilities were primarily attributable to the convertible / redeemable preference shares that we issued to Pre-IPO Investors. The convertible redeemable / preference shares will be converted
  - p29: Pre-IPO Investments — Special Rights of the Pre-IPO Investors” and Note 27 to the / Accountant’s Report in Appendix I to this prospectus. As the convertible redeemable / preference shares will be re-designated from liabilities to equity as a result of the automatic / conversion into ordinary Shares upon Listing, we expect our net liability and net current

### col_BB
  - p34: SHAREHOLDER INFORMATION / Upon completion of the Global Offering (assuming the Over-allotment Option is not / exercised), Mr. Wang, Cheuk Sing Ho, the Concert Parties and Distinct Partners I Limited are / our Controlling Shareholders who will be able to exercise an aggregate of 30.79% voting rights / in the Company through (i) the Acting-in-Concert Agreement, (ii) the Cheuk Sing Ho / Agreement, (i
  - p55: Haitong International Securities Company Limited / “subsidiary(ies)” / has the meaning ascribed to it under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed to it under the Listing Rules / DEFINITIONS / – 46 –

### col_BC
  - p34: SHAREHOLDER INFORMATION / Upon completion of the Global Offering (assuming the Over-allotment Option is not / exercised), Mr. Wang, Cheuk Sing Ho, the Concert Parties and Distinct Partners I Limited are / our Controlling Shareholders who will be able to exercise an aggregate of 30.79% voting rights / in the Company through (i) the Acting-in-Concert Agreement, (ii) the Cheuk Sing Ho / Agreement, (i
  - p55: Haitong International Securities Company Limited / “subsidiary(ies)” / has the meaning ascribed to it under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed to it under the Listing Rules / DEFINITIONS / – 46 –

### col_BD
  - p34: SHAREHOLDER INFORMATION / Upon completion of the Global Offering (assuming the Over-allotment Option is not / exercised), Mr. Wang, Cheuk Sing Ho, the Concert Parties and Distinct Partners I Limited are / our Controlling Shareholders who will be able to exercise an aggregate of 30.79% voting rights / in the Company through (i) the Acting-in-Concert Agreement, (ii) the Cheuk Sing Ho / Agreement, (i
  - p34: SHAREHOLDER INFORMATION / Upon completion of the Global Offering (assuming the Over-allotment Option is not / exercised), Mr. Wang, Cheuk Sing Ho, the Concert Parties and Distinct Partners I Limited are / our Controlling Shareholders who will be able to exercise an aggregate of 30.79% voting rights / in the Company through (i) the Acting-in-Concert Agreement, (ii) the Cheuk Sing Ho / Agreement, (i
  - p55: Haitong International Securities Company Limited / “subsidiary(ies)” / has the meaning ascribed to it under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed to it under the Listing Rules / DEFINITIONS / – 46 –

### col_BE
  - p84: cash flow from our operations. If our resources are insufficient to satisfy our cash / requirements, we may seek additional financing. To the extent that we raise additional / financing by issuance of additional equity securities, our Shareholders may experience / dilution. To the extent we engage in debt financing, the incurrence of indebtedness would result / in increased debt servicing obligati
  - p464: the event that the Over-allotment Option is exercised. / To the extent that the net proceeds are not immediately applied to the above purposes and / to the extent permitted by applicable law and regulations, we will only deposit the net proceeds / in short-term interest-bearing accounts at licensed commercial banks or authorized financial / institutions (as defined under the Securities and Futures
  - p394: statement, to the date of this prospectus. We had unutilized bank facilities of RMB30.0 million / as of November 30, 2025. / Our Directors confirm that our Group did not experience any difficulty in obtaining bank / loans and other borrowings, default in payment of bank loans and other borrowings or breach / of covenants during the Track Record Period and up to the Latest Practicable Date. There w

### col_BF
  - p87: unable to enforce these Contractual Arrangements or we experience significant delays or other / obstacles in the process of enforcing these Contractual Arrangements, we may not be able to / exert effective control over Zhuozheng Xinhe, and our ability to conduct our business may be / negatively affected. / The Relevant Shareholders may have potential conflicts of interest with us, which may

### col_BG
  - p36: granted to the Directors, as described in the section headed “Share Capital” of this prospectus. / No adjustment has been made to reflect any trading results or other transactions of the Group entered into / subsequent to August 31, 2025. / USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$219.1 million, after deducting underwriting comm
  - p37: ➢ / 10%, or approximately HK$21.9 million for working capital and other general / corporate purposes. / For details, see “Future Plans and Use of Proceeds.” / PROFIT ESTIMATE FOR THE YEAR ENDED DECEMBER 31, 2025 / We have prepared the following profit estimate for the year ended December 31, 2025. / Estimated consolidated profit

### col_BI
  - p27: We recorded net loss of RMB353.2 million in 2023 and net profit of RMB80.2 million in / 2024, primarily due to (i) a change in the fair value of convertible redeemable preference / shares from a loss of RMB289.4 million in 2023 to a gain of RMB128.8 million in 2024, / mainly attributable to a decrease in the valuation of fair values of such shares, and (ii) an / increase in revenue of RMB268.1 mil

### col_BP
  - p1: GLOBAL OFFERING / Stock Code : 2677 / (Incorporated in the Cayman Islands with limited liability) / Distinct Healthcare Holdings Limited / 卓正醫療控股有限公司 / Joint Sponsors, Joint Sponsor-Overall Coordinators, Joint Overall Coordinators,

### col_BR
  - p132: Gongye 4th Rd / Nanshan District, Shenzhen / PRC / Principal Place of Business in Hong Kong / Room 1901, 19/F, Lee Garden One / 33 Hysan Avenue / Causeway Bay
  - p132: Registered Office / Floor 4, Willow House / Cricket Square / Grand Cayman KY1-9010
  - p132: Cricket Square / Grand Cayman KY1-9010 / Cayman Islands / Head Office and Principal Place / of Business in China / Floor 4, Tower A / Wanrong Building

### col_BT
  - p536: The Historical Financial Information of the Company has been prepared in accordance with International / Financial Reporting Standards issued by the International Accounting Standards Board (the “IFRS Accounting / Standards”). / The preparation of Historical Financial Information in conformity with IFRS Accounting Standards requires / the use of certain critical accounting estimates. It also requi
  - p47: amendments / and / interpretations / promulgated by the International Accounting Standards / Board / and / International
  - p37: owners of the Company for the year ended December 31, 2025 based on the audited consolidated results / of our Group for the eight months ended August 31, 2025 and the unaudited consolidated results based / on the management accounts of our Group for the four months ended December 31, 2025. The profit / estimate has been prepared on a basis consistent in all material respects with our accounting po

### col_CC
  - p5: at www.distinctclinic.com by(5) / . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .11:00 p.m. on / Thursday, February 5, 2026 / EXPECTED TIMETABLE(1) / – iv –
  - p5: timetable of the Hong Kong Public Offering, an announcement will be made and / published on the website of the Stock Exchange at www.hkexnews.hk and our website at / www.distinctclinic.com of the revised timetable. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on / Thursday, January 29, 2026 / Latest time for completing electronic applic

### col_CD
  - p5: at www.distinctclinic.com by(5) / . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .11:00 p.m. on / Thursday, February 5, 2026 / EXPECTED TIMETABLE(1) / – iv –

### col_CE
（锚点无命中，需要自己 search）

### col_CF
  - p18: (732,575) / (462,388) / (528,396) / Gross profits               / 43,980 / 133,502 / 226,003
  - p18: (732,575) / (462,388) / (528,396) / Gross profits               / 43,980 / 133,502 / 226,003

### col_CG
  - p84: under commercially acceptable terms, or at all. / We believe that our current cash and cash equivalents, anticipated cash flow from / operations, and the proceeds from this Global Offering will be sufficient to meet our / anticipated cash needs, including our cash needs for working capital and capital expenditures, / for at least the next 12 months from the date of this prospectus. We may, however
  - p84: under commercially acceptable terms, or at all. / We believe that our current cash and cash equivalents, anticipated cash flow from / operations, and the proceeds from this Global Offering will be sufficient to meet our / anticipated cash needs, including our cash needs for working capital and capital expenditures, / for at least the next 12 months from the date of this prospectus. We may, however
  - p389: For the year ended December 31, 2023, our net cash used in investing activities was / RMB1.5 million, primarily attributable to (i) payments for financial assets at fair value through / profit or loss of RMB825.1 million, (ii) placement of term deposits with initial term of over / three months of RMB325.2 million, and (iii) purchase of property, plant and equipment of / RMB66.4 million, partially 

### col_CH
  - p72: any of which may adversely affect our results of operations and reputation. We cannot assure / you that significant claims of such nature will not be asserted against us in the future, and that / adverse verdicts will not be reached or that we will be able to recover losses from our suppliers. / In addition, termination of our supply agreements with unqualified suppliers can be / time-consuming an
  - p513: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the / accountant’s report, a true and fair view of the financial position of the Company as at / December 31, 2022, 2023 and 2024 and August 31, 2025 and the consolidated financial / position of
  - p512: Company’s reporting accountant, PricewaterhouseCoopers, Certified Public Accountants, / Hong Kong, for the purpose of incorporation in this prospectus. It is prepared and addressed / to the directors of the Company and to the Joint Sponsors pursuant to the requirements of / HKSIR 200, Accountants’ Reports on Historical Financial Information in Investment Circulars / issued by the Hong Kong Institu

### col_CI
  - p19: We define “adjusted net profit or loss (a non-IFRS measure)” as (loss)/profit for the / years/period adjusted by adding back or deducting, as the case may be, fair value (loss)/gain / of convertible redeemable preference shares, share-based compensation expenses and listing / expenses. Listing expenses are expenses incurred in relation to the Global Offering. Fair value / (loss)/gain of convertibl
  - p19: We define “adjusted net profit or loss (a non-IFRS measure)” as (loss)/profit for the / years/period adjusted by adding back or deducting, as the case may be, fair value (loss)/gain / of convertible redeemable preference shares, share-based compensation expenses and listing / expenses. Listing expenses are expenses incurred in relation to the Global Offering. Fair value / (loss)/gain of convertibl


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 2677.HK`
有 ERROR 必须回原文修正。
