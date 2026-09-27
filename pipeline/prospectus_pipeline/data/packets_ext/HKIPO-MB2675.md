# 2675.HK 扩展 18 列抽取包

公司：2675.HK Shenzhen Edge Medical Co., Ltd.- B - H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB2675.json`。
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
- 股本结构（**已确认，不要改**）：L=387722200 M=27722200 N=360000000 O=360000000 P=0 Q=27722200 R=24949900 S=2772300
- 财务期间（**已确认**）：year-1 期末 = 30/06/25；币种 = RMB；year-1 净利 = -178174000
- 行业分类（港交所官方）：282010 醫療設備及用品
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
{"code":"2675.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  2675.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 2675.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p40: For further details of our Controlling Shareholders, see “Relationship with our / Controlling Shareholders.” / OUR PRE-IPO INVESTORS / Since November 2017, we have secured six rounds of Pre-IPO Investments with an / aggregate amount of approximately RMB2,050 million. Pursuant to the applicable PRC law, / within the 12 months following the Listing Date, our Pre-IPO Investors could not dispose of / 
  - p40: Controlling Shareholders. / For further details of our Controlling Shareholders, see “Relationship with our / Controlling Shareholders.” / OUR PRE-IPO INVESTORS / Since November 2017, we have secured six rounds of Pre-IPO Investments with an / aggregate amount of approximately RMB2,050 million. Pursuant to the applicable PRC law, / within the 12 months following the Listing Date, our Pre-IPO Inves
  - p40: For further details of our Controlling Shareholders, see “Relationship with our / Controlling Shareholders.” / OUR PRE-IPO INVESTORS / Since November 2017, we have secured six rounds of Pre-IPO Investments with an / aggregate amount of approximately RMB2,050 million. Pursuant to the applicable PRC law, / within the 12 months following the Listing Date, our Pre-IPO Investors could not dispose of / 

### col_BB
  - p40: OUR CONTROLLING SHAREHOLDERS / Our Company was founded by Dr. Wang and Dr. Gao back in 2017 and has been jointly / controlled by Dr. Wang and Dr. Gao (by virtue of their relationship of being spouses) by / themselves and/or through certain entities since then. Immediately prior to the Global Offering,
  - p47: General / Information—Further / Information about our Directors, Supervisors, Senior / Management and Substantial Shareholders—5. Employee / Incentive Scheme” / “Exchange Participant” / a person (a) who, in accordance with the Rules of the
  - p281: partnership duly established under the laws of the PRC. Sanzheng Zhengyun is managed by its / general partner Hainan Sanzheng Shouzheng Health Management Co., Ltd. (海南叁正守正健 / 康管理有限公司) (“Hainan Sanzheng”), which in turn is controlled by Mr. Sheng Li (盛利), / our non-executive Director, as its ultimate beneficial owner. Sanzheng Zhengyun has one / limited partner, Nanjing Sanzheng. Nanjing Sanzheng i

### col_BC
  - p40: OUR CONTROLLING SHAREHOLDERS / Our Company was founded by Dr. Wang and Dr. Gao back in 2017 and has been jointly / controlled by Dr. Wang and Dr. Gao (by virtue of their relationship of being spouses) by / themselves and/or through certain entities since then. Immediately prior to the Global Offering,
  - p47: General / Information—Further / Information about our Directors, Supervisors, Senior / Management and Substantial Shareholders—5. Employee / Incentive Scheme” / “Exchange Participant” / a person (a) who, in accordance with the Rules of the

### col_BD
  - p40: OUR CONTROLLING SHAREHOLDERS / Our Company was founded by Dr. Wang and Dr. Gao back in 2017 and has been jointly / controlled by Dr. Wang and Dr. Gao (by virtue of their relationship of being spouses) by / themselves and/or through certain entities since then. Immediately prior to the Global Offering,
  - p275: Zhongxu Ruifeng / Zhongxu Ruifeng was established as a limited partnership established in the PRC on / December 29, 2021. Dr. Wang, as the sole general partner of Zhongxu Ruifeng, is responsible / for the management of Zhongxu Ruifeng and exercises the voting rights held by Zhongxu / Ruifeng in its external investments at his full and absolute discretion. As of the Latest / Practicable Date, Zhong
  - p47: General / Information—Further / Information about our Directors, Supervisors, Senior / Management and Substantial Shareholders—5. Employee / Incentive Scheme” / “Exchange Participant” / a person (a) who, in accordance with the Rules of the

### col_BE
  - p105: financings, and collaborations or licensing arrangements. To the extent that we raise additional / capital through the sale of equity or convertible debt securities, your ownership interest will / be diluted, and the terms may include liquidation or other preferences that adversely affect / your rights as a holder of our H Shares. The incurrence of additional indebtedness or the / issuance of cert
  - p518: operations, bank loans and other borrowings. To the extent that the net proceeds from the / Global Offering are not immediately used for the purposes described above and to the extent / permitted by the relevant laws and regulations, we may hold such funds in short-term / interest-bearing accounts at licensed commercial banks and/or authorized financial institutions / (as defined under the SFO or 
  - p493: We expect to incur capital expenditures in 2025 primarily for expansion of manufacturing / capacities and purchase of new equipment. For details, see “Future Plans and Use of Proceeds.” / We expect to finance such capital expenditures through a combination of existing cash and cash / equivalents, net proceeds from the Global Offering and bank and other borrowings. We may / adjust our capital expen

### col_BF
  - p12: MP1000, also known as MP1000 Plus, and MP2000 series, the second generation of our / MP1000, respectively. We have been expanding our overseas registration and sales since 2025. / In March 2025, we obtained the CE Marking of MP1000 in the EU. We started to / commercialize Edge Multi-Port Endoscopic Surgical Robot in China in December 2022. We / sold 20 units of Edge Multi-Port Endoscopic Surgical 
  - p239: control. / Such / manufacturer and seller must also comply with various other items stipulated by the ministerial / ordinances of the MHLW in the process of conducting the licensed business. / In order to conduct the business of manufacturing medical devices, the manufacturer is / also required to make a renewable, five-year manufacturing registration with the Minister for / each manufacturing sit

### col_BG
  - p41: reserve fund until such fund has reached more than 50% of our registered capital. As a result, / we may not have sufficient or any distributable profits to make dividend distributions to our / Shareholders, even if we become profitable. / USE OF PROCEEDS / We estimate that we will receive net proceeds of approximately HK$1,116.6 million from / the Global Offering after deducting underwriting commi
  - p42: • / approximately 10.0% of the net proceeds, or HK$111.7 million, will be used for / working capital and general corporate purposes. / For further details, see “Future Plans and Use of Proceeds.” / RISK FACTORS / We are a surgical robot company seeking to list on the Main Board of the Stock Exchange / under Chapter 18A of the Listing Rules. We believe there are certain risks and uncertainties

### col_BI
  - p2: Number of Offer Shares under / the Global Offering / : / 27,722,200 H Shares (subject to / the Over-allotment Option) / Number of Hong Kong Offer Shares / :

### col_BP
  - p1: Stock Code : 2675 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / 深圳市精鋒醫療科技股份有限公司 / Shenzhen Edge Medical Co., Ltd. / GLOBAL OFFERING

### col_BR
  - p161: Baolong Street / Longgang District / Shenzhen, PRC / Principal Place of Business in Hong Kong / Room 1918, 19/F / Lee Garden One / 33 Hysan Avenue
  - p161: Registered Office / Room 1901, Building 2B / Smart Park Phase II / Baolong Street

### col_BT
  - p50: Public / Offering—Hong Kong Underwriting Agreement” / “IFRS” / IFRS Accounting Standards issued by the International / Accounting Standards Board / “Independent Third Party(ies)” / any entity(ies) or person(s) who is not a connected person
  - p32: the accompanying notes, set forth in the Accountants’ Report set out in Appendix I to this / Prospectus, as well as the information set forth in the section headed “Financial Information” / of this Prospectus. Our financial information was prepared in accordance with IFRS / Accounting Standards. / SUMMARY / – 23 –
  - p459: except financial assets measured at fair value through profit or loss are stated at fair value. / The preparation of financial statements in conformity with IFRS Accounting Standards / requires the use of certain critical accounting estimates. It also requires management to / exercise its judgement in the process of applying our accounting policies. All effective / standards, amendments to standar

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on the Company’s / website / at
  - p5: Exchange / at / www.hkexnews.hk. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on Tuesday, / December 30, 2025 / Latest time for completing electronic applications / under the HK eIPO White Form service through

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on the Company’s / website / at

### col_CE
  - p140: of the H Shares will be 2675. / APPLICATION FOR LISTING ON THE HONG KONG STOCK EXCHANGE / We have applied to the Listing Committee for the listing of, and permission to deal in, the / H Shares to be issued pursuant to the Global Offering (including any H Shares which may be / issued pursuant to the exercise of the Over-allotment Option) and the H Shares to be converted / from the Unlisted Shares. 
  - p4: Your application must be for a minimum of 100 Hong Kong Offer Shares and in one / of the numbers set out in the table below. If you are applying through the HK eIPO / White Form service, you may refer to the table below for the amount payable for the / number of H Shares you have selected. You must pay the respective amount payable on / application in full upon application for Hong Kong Offer Shar

### col_CF
  - p33: (61,917) / (11,088) / (55,533) / Gross profit               / 28,466 / 98,077 / 19,157
  - p33: (61,917) / (11,088) / (55,533) / Gross profit               / 28,466 / 98,077 / 19,157

### col_CG
  - p38: administrative expenses, selling and marketing expenses, finance costs and other expenses for / at least the next 12 months from the date of this Prospectus. / Our cash burn rate refers to the average monthly (i) net cash used in operating activities, / (ii) capital expenditures and (iii) lease payments. We had cash and cash equivalents and the / financial assets measured at FVPL with high liquidi
  - p38: administrative expenses, selling and marketing expenses, finance costs and other expenses for / at least the next 12 months from the date of this Prospectus. / Our cash burn rate refers to the average monthly (i) net cash used in operating activities, / (ii) capital expenditures and (iii) lease payments. We had cash and cash equivalents and the / financial assets measured at FVPL with high liquidi
  - p489: For the year ended December 31, 2023, our net cash generated from investing activities / was RMB383.7 million, mainly attributable to proceeds from financial assets of RMB530.4 / million, which was partially offset by payment for purchase of financial assets of RMB85.0 / million and purchase of property, plant and equipment of RMB61.3 million. / Net Cash Used in Financing Activities / During the T

### col_CH
  - p226: According to the Civil Code of the People’s Republic of China (中華人民共和國民法典), / which was promulgated by the National People’s Congress on May 28, 2020 and came into / effect on January 1, 2021, patients who suffer from damage due to defects in drugs, disinfectant / products and medical devices, or the infusion of unqualified blood may claim compensation / from the marketing license holder, the manu
  - p32: COMPLIANCE AND LEGAL PROCEEDINGS / During the Track Record Period and up to the Latest Practicable Date, we are not a party / to, and we are not aware of any threat of, any legal, arbitral or administrative proceeding, / which, in our opinion, is likely to have a material and adverse effect on our business, financial / conditions or results of operation. During the Track Record Period and up to th
  - p32: SUMMARY OF KEY FINANCIAL INFORMATION / This summary historical data of financial information set forth below has been derived / from, and should be read in conjunction with, our consolidated financial statements, including / the accompanying notes, set forth in the Accountants’ Report set out in Appendix I to this / Prospectus, as well as the information set forth in the section headed “Financial 

### col_CI
  - p43: rights obtained is not sufficiently broad, third parties may compete directly against / us. / LISTING EXPENSE / The total Listing expenses (including underwriting commissions) payable by our / Company are estimated to be approximately HK$82.1 million (or approximately RMB74.4 / million) or 6.8% of the gross proceeds of the Global Offering, assuming the Over-allotment / Option is not exercised and 
  - p43: rights obtained is not sufficiently broad, third parties may compete directly against / us. / LISTING EXPENSE / The total Listing expenses (including underwriting commissions) payable by our / Company are estimated to be approximately HK$82.1 million (or approximately RMB74.4 / million) or 6.8% of the gross proceeds of the Global Offering, assuming the Over-allotment / Option is not exercised and 


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 2675.HK`
有 ERROR 必须回原文修正。
