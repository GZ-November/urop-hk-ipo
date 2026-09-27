# 2768.HK 扩展 18 列抽取包

公司：2768.HK Qingdao Gon Technology Co., Ltd. - H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB2768.json`。
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
- 股本结构（**已确认，不要改**）：L=301250000 M=30000000 N=271250000 O=271250000 P=0 Q=30000000 R=27000000 S=3000000
- 财务期间（**已确认**）：year-1 期末 = 31/10/25；币种 = RMB；year-1 净利 = 865179600
- 行业分类（港交所官方）：053040 特殊化工用品
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
{"code":"2768.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  2768.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 2768.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
（锚点无命中，需要自己 search）

### col_BB
  - p21: million and RMB7,588.6 million, as at 31 December 2022, 2023 and 2024 and 31 October / 2025, respectively. Our net assets increased to RMB5,900.9 million as at 31 December 2022, / primarily attributable to (i) total comprehensive income of RMB724.4 million for the year; (ii) / contribution from a non-controlling shareholder of subsidiary leading to increase in capital / reserve and non-controlling
  - p42: per cent / In this prospectus, the terms “associate”, “close associate”, “connected person”, / “connected transaction”, “core connected person”, “controlling shareholder”, “subsidiary” / and “substantial shareholder” shall have the meanings given to such terms in the Listing / Rules, unless the context otherwise requires. / If there is any inconsistency between the Chinese names of PRC laws and re
  - p270: (advising on securities) and Type 9 (asset management) activities since September 2023. It / conducts dealing in securities, investment advisory, and asset management activities in Hong / Kong in compliance with regulatory requirements. First Seafront Asset Management Limited / is ultimately owned by First Seafront Holding Limited, and no ultimate beneficial owner holds / 30% or more interest in F

### col_BC
  - p21: million and RMB7,588.6 million, as at 31 December 2022, 2023 and 2024 and 31 October / 2025, respectively. Our net assets increased to RMB5,900.9 million as at 31 December 2022, / primarily attributable to (i) total comprehensive income of RMB724.4 million for the year; (ii) / contribution from a non-controlling shareholder of subsidiary leading to increase in capital / reserve and non-controlling
  - p42: per cent / In this prospectus, the terms “associate”, “close associate”, “connected person”, / “connected transaction”, “core connected person”, “controlling shareholder”, “subsidiary” / and “substantial shareholder” shall have the meanings given to such terms in the Listing / Rules, unless the context otherwise requires. / If there is any inconsistency between the Chinese names of PRC laws and re

### col_BD
  - p21: million and RMB7,588.6 million, as at 31 December 2022, 2023 and 2024 and 31 October / 2025, respectively. Our net assets increased to RMB5,900.9 million as at 31 December 2022, / primarily attributable to (i) total comprehensive income of RMB724.4 million for the year; (ii) / contribution from a non-controlling shareholder of subsidiary leading to increase in capital / reserve and non-controlling
  - p61: beneficially owned 126,000,000 A Shares, representing 46.45% of the total issued share capital / of our Company, and, together with the 18,000,000 A Shares and 9,000,000 A Shares / respectively held by Ms. Xu (Mr. Wang’s wife) and Xinghao Investment, controlled 56.41% of / the voting rights as of the Latest Practicable Date. Mr. Wang has pledged the A Shares he / owned to certain PRC financial ins
  - p42: per cent / In this prospectus, the terms “associate”, “close associate”, “connected person”, / “connected transaction”, “core connected person”, “controlling shareholder”, “subsidiary” / and “substantial shareholder” shall have the meanings given to such terms in the Listing / Rules, unless the context otherwise requires. / If there is any inconsistency between the Chinese names of PRC laws and re

### col_BE
  - p264: Mr. Wang has confirmed that, if any circumstances arise which results in a margin call or / top-up mechanism being triggered under any of the Share Pledges, Mr. Wang shall take all / necessary actions, such as provision of additional collateral/and repayment of the relevant / indebtedness, to prevent the enforcement of the pledged A Shares. Mr. Wang will only pledge / additional Shares to the exte
  - p23: Return on total assets is calculated by profit for the annualised profit for the period divided by total assets as / at the end of the respective year multiplied by 100%. / 5. / Gearing ratio is calculated based on the total interest-bearing debt divided by total equity as at the end of / respective year/period multiplied by 100%. / For details, please see “Financial Information – Key Financial Ra
  - p20: 14,485 / 23,407 / Bank and other / borrowings         / 1,725,921 / 1,895,339 / 2,217,366

### col_BF
  - p172: domestic empty capsule manufacturers and large pharmaceutical enterprises. Our product / quality has been widely recognized by downstream customers. Our high-value-added product, / plasma substitute gelatin, has been included in the national Guide for Excellent and Innovative / Consumer Goods (《升級和創新消費品指南》) and has been commercialized. Moreover, / downstream product, namely, succinylated gelatin i
  - p110: substitutes. / Domestic / technological / breakthroughs have enabled localized mass production, breaking international / monopolies and achieving full import substitution. The Company’s high-end / medical-grade gelatin, including plasma substitute gelatin, has gradually achieved / import substitution in these applications.
  - p136: of social security collection. In principle, the basic pension insurance for enterprise employees / and other insurance types for enterprise employees shall be collected temporarily according to / the existing collection system to stabilize the payment method. It also emphasizes that the / historical unpaid arrears of the enterprise shall be properly treated. In the process of / reformation of the

### col_BG
  - p27: USE OF PROCEEDS / After deducting the underwriting commissions and other estimated offering expenses / payable by us in connection with the Global Offering, and assuming an Offer Price of / HK$38.00 per H Share (being the mid-point of the indicative Offer Price range stated in this
  - p27: approximately 5.0% of the net proceeds, or approximately HK$53.0 million (or / RMB47.6 million), is expected to be used for working capital and general corporate / purposes. / For further details, please see the section headed “Future Plans and Use of Proceeds”. / DIVIDENDS AND DIVIDEND POLICY / We have adopted a dividend policy. According to our dividend policy which is in line with / the Article

### col_BI
  - p2: Number of Offer Shares under / the Global Offering / : / 30,000,000 H Shares / Number of Hong Kong Offer Shares / : / 3,000,000 H Shares (subject to

### col_BP
  - p149: Year / Event / 2000     / Our Company was established on 22 December 2000 / 2006     / Our Qingda Industrial Park Headquarters Base has been completed and put / into operation (青島市城陽區青大工業園)
  - p1: 青島國恩科技股份有限公司 / QINGDAO GON TECHNOLOGY CO., LTD. / Stock Code : 2768 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / GLOBAL OFFERING / Joint Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers / Joint Bookrunners and Joint Lead Managers

### col_BR
  - p90: Qingdao City / Shandong Province / PRC / Principal place of business in the PRC / No. 2 Road, Qingda Industrial Park / Jihongtan Street / Chengyang District
  - p90: Registered office in the PRC / No. 2 Road, Qingda Industrial Park / Jihongtan Street / Chengyang District

### col_BT
  - p277: The Historical Financial Information has been prepared in accordance with IFRS / Accounting Standards, which collective term includes all applicable individual IFRS / Accounting Standards and Interpretations approved by the International Accounting Standards / Board (“IASB”). All IFRS Accounting Standards are effective for the accounting period / beginning on 1 January 2024, together with the rele
  - p36: Sponsor, the Joint Overall Coordinators, the Joint Global / Coordinators and the Hong Kong Underwriters / “IASB” / International Accounting Standards Board / “IFRS(s)” / International / Accounting
  - p53: in FY2024 and 10MFY2025 was primarily due to that the operating performance of Dongbao / Bio-Tech falling short of expectations and the unfavorable market conditions of health / industry. For details of factors which may trigger impairment of intangible assets and goodwill, / please refer to “Financial Information — Material accounting policies, critical accounting / judgements and estimation”. As

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on the Stock / Exchange’s website at www.hkexnews.hk and our website at www.qdgon.com. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on Tuesday,
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on the Stock / Exchange’s website at www.hkexnews.hk and our website at www.qdgon.com. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on Tuesday, / 27 January 2026 / Latest time to complete applicatio

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on the Stock / Exchange’s website at www.hkexnews.hk and our website at www.qdgon.com. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on Tuesday,

### col_CE
  - p275: 1. / Size of the offer / The proposed number of H Shares to be offered shall not exceed 15% of the total issued / share capital as enlarged by the H Shares to be issued pursuant to the Global Offering before / the exercise of any over-allotment option. The number of H Shares to be issued pursuant to the / full exercise of any over-allotment option shall not exceed 15% of the total number of H Shar
  - p163: (11) / Treasury shares of the Company have been included in the total issued share capital of the Company for the purpose of calculation of the shareholding percentages. For the / purpose of the public float analysis, the percentage of H Shares to be issued excluding the treasury shares shall be 10.17%. This is calculated on the basis that the total number / of issued shares excluding the 6,250,00

### col_CF
  - p16: 15,863,106 / 17,443,865 / Cost of sales               (11,826,476) (15,838,017) (17,595,339) (14,580,724) (15,632,844) / Gross Profit                / 1,579,964 / 1,600,762 / 1,592,172
  - p16: 15,863,106 / 17,443,865 / Cost of sales               (11,826,476) (15,838,017) (17,595,339) (14,580,724) (15,632,844) / Gross Profit                / 1,579,964 / 1,600,762 / 1,592,172

### col_CG
  - p341: Period and up to the Latest Practicable Date. Our Directors also confirm that there has been no / material change in our indebtedness since 30 November 2025 and up to the date of this / prospectus. / CAPITAL EXPENDITURE AND COMMITMENTS / Capital Expenditures / Our capital expenditures primarily consist of expenditures for property, plant and / equipment, right-of-use assets, intangible assets and 
  - p341: Period and up to the Latest Practicable Date. Our Directors also confirm that there has been no / material change in our indebtedness since 30 November 2025 and up to the date of this / prospectus. / CAPITAL EXPENDITURE AND COMMITMENTS / Capital Expenditures / Our capital expenditures primarily consist of expenditures for property, plant and / equipment, right-of-use assets, intangible assets and 

### col_CH
  - p128: the construction entity shall, in accordance with the provisions of relevant laws and / regulations, conduct acceptance of the supporting noise pollution prevention and control / facilities, prepare an acceptance report, and open to the public. Without acceptance or / unqualified acceptance, the construction project shall not be put into production or use. / REGULATORY OVERVIEW / – 117 –
  - p400: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion the Historical Financial Information gives, for the purposes of the / accountant’s report, a true and fair view of the Company’s and the Group’s financial position / as at 31 December 2022, 2023, 2024 and 31 October 2025 and of the Group’s financial / perform
  - p399: Reporting accountant’s responsibility / Our responsibility is to express an opinion on the Historical Financial Information and to / report our opinion to you. We conducted our work in accordance with Hong Kong Standard on / Investment Circular Reporting Engagements 200 “Accountants’ Report on Historical Financial / Information in Investment Circulars” issued by the Hong Kong Institute of Certifie

### col_CI
  - p29: LISTING EXPENSES / Based on an Offer Price of HK$38.00 per Offer Share (which is the mid-point of the Offer / Price range) and assuming the full payment of the discretionary incentive fee, if any, we expect / to incur approximately HKD82.3 million of listing expenses (including (i) underwriting-related
  - p29: LISTING EXPENSES / Based on an Offer Price of HK$38.00 per Offer Share (which is the mid-point of the Offer / Price range) and assuming the full payment of the discretionary incentive fee, if any, we expect / to incur approximately HKD82.3 million of listing expenses (including (i) underwriting-related


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 2768.HK`
有 ERROR 必须回原文修正。
