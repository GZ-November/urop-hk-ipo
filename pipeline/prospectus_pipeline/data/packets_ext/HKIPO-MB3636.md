# 3636.HK 扩展 18 列抽取包

公司：3636.HK Yunnan Jinxun Resources Co., Ltd. - H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB3636.json`。
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
- 股本结构（**已确认，不要改**）：L=147062243 M=36765600 N=110296643 O=110296643 P=0 Q=36765600 R=33089000 S=3676600
- 财务期间（**已确认**）：year-1 期末 = 30/06/2025；币种 = RMB；year-1 净利 = 269964000
- 行业分类（港交所官方）：052020 銅
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
{"code":"3636.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  3636.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 3636.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
（锚点无命中，需要自己 search）

### col_BB
  - p20: material respects and save as disclosed in the “Business” section and in the “Risk Factors” / section, we had obtained all requisite licenses, approvals and permits from relevant authorities / in China during the Track Record Period and up to the Latest Practicable Date. / OUR CONTROLLING SHAREHOLDERS / Immediately upon completion of the Global Offering and without taking into account any / Shares
  - p43: “substantial shareholder(s)” / has the meaning ascribed to it under the Listing Rules; / “Tibet Huiyi” / Tibet Huiyi Information Technology Co., Ltd. (西藏匯益
  - p364: incorporated in the Cayman Islands with limited liability in September 2020. The principal / investment objective of Stoneylake Global is to maximize long-term capital growth through / active investment in the financial markets, and it maintains a well-distributed shareholder base / with no ultimate beneficial owner holding 30% or more of the ownership interest in Stoneylake / Global. Stoneylake G

### col_BC
  - p20: material respects and save as disclosed in the “Business” section and in the “Risk Factors” / section, we had obtained all requisite licenses, approvals and permits from relevant authorities / in China during the Track Record Period and up to the Latest Practicable Date. / OUR CONTROLLING SHAREHOLDERS / Immediately upon completion of the Global Offering and without taking into account any / Shares
  - p43: “substantial shareholder(s)” / has the meaning ascribed to it under the Listing Rules; / “Tibet Huiyi” / Tibet Huiyi Information Technology Co., Ltd. (西藏匯益

### col_BD
  - p20: material respects and save as disclosed in the “Business” section and in the “Risk Factors” / section, we had obtained all requisite licenses, approvals and permits from relevant authorities / in China during the Track Record Period and up to the Latest Practicable Date. / OUR CONTROLLING SHAREHOLDERS / Immediately upon completion of the Global Offering and without taking into account any / Shares
  - p20: hold / approximately 74.94% of the total share capital of our Company. Heli Investment is our share / incentive platform which is controlled by Mr. Yuan, acting as its general partner, by managing / its daily affairs and exercising its voting rights on behalf of Heli Investment as our Shareholder / pursuant to the partnership agreement of Heli Investment. Mr. Yuan will, directly or through / Heli 
  - p43: “substantial shareholder(s)” / has the meaning ascribed to it under the Listing Rules; / “Tibet Huiyi” / Tibet Huiyi Information Technology Co., Ltd. (西藏匯益

### col_BE
  - p345: INDEBTEDNESS AND CONTINGENT LIABILITIES / Indebtedness / During the Track Record Period, our indebtedness consisted of (i) lease liabilities; and (ii) / bank and other borrowings. The following table sets forth a breakdown of our indebtedness as
  - p30: capabilities, attract local talents and contribute local employment. / • / approximately 10% of the net proceeds, or HK$104.3 million, will be used to / repay certain of our interest-bearing bank borrowings with an aggregate / principal amount of approximately HK$105.8 million, which were used as / working / capital.
  - p26: million as of December 31, 2022. The increase of the net current liabilities as of December 31, / 2023 as compared with that as of December 31, 2022 was primarily attributable to the increase / in our current liabilities of RMB203.3 million, primarily due to (i) an increase in short term / bank and other borrowings of RMB114.0 million for financing the construction of the Anhui / cobalt processing

### col_BF
  - p158: The mining industry in Peru is mainly governed by the Single Ordered Text of the General / Mining Law approved by Supreme Decree N° 014-92-EM (hereinafter, the “TUO of the / LGM”), which establishes the legal framework applicable to the mining activities of / prospecting, exploration, exploitation, general work, beneficiation, commercialization and / mining transportation. / In this regard, it is 
  - p63: intended economic results. Our expenditure may not be fully recovered. / We intend to invest in projects at our existing operations to increase our production / efficiency, as well as to expand and develop our processing capacities. We are also currently / in the process of making significant capital expenditures in connection with the expansion of / our operations. Capital expenditure projects we

### col_BG
  - p30: FUTURE PLANS AND USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$1,042.6 million, assuming an Offer Price of HK$30.0 per Offer Share, after deducting the / underwriting commissions and estimated expenses paid or payable by us in connection with the
  - p30: FUTURE PLANS AND USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$1,042.6 million, assuming an Offer Price of HK$30.0 per Offer Share, after deducting the / underwriting commissions and estimated expenses paid or payable by us in connection with the

### col_BI
  - p2: Number of Offer Shares under the / Global Offering / : / 36,765,600 H Shares (subject to the / Over-allotment Option) / Number of Hong Kong Offer Shares / 3,676,600 H Shares (subject to

### col_BP
  - p1: OFFERING / Sole Sponsor, Sponsor-Overall Coordinator, Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager / Stock Code : 3636 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / 雲南金潯資源股份有限公司 / Yunnan Jinxun Resources Co., Ltd. / Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager

### col_BR
  - p101: Kunming / Yunnan Province / PRC / Principal place of business in Hong Kong / 40th Floor, Dah Sing Financial Centre / No. 248 Queen’s Road East / Wanchai
  - p101: Registered office / 3/F, Block B / No. 1389 Changyuan North Road / Gaoxin District

### col_BT
  - p21: prospectus. The summary consolidated financial information set forth below should be read / together with, and is qualified in its entirety by reference to, the Accountants’ Report set out / in Appendix I to this prospectus, including the related notes. Our consolidated financial / information was prepared in accordance with IFRS Accounting Standards. / Summary of Consolidated Statements of Profit
  - p21: prospectus. The summary consolidated financial information set forth below should be read / together with, and is qualified in its entirety by reference to, the Accountants’ Report set out / in Appendix I to this prospectus, including the related notes. Our consolidated financial / information was prepared in accordance with IFRS Accounting Standards. / Summary of Consolidated Statements of Profit
  - p251: Specifically, we have established a unified governance framework and policy system, / including a standardized internal control system for financial reporting and information / disclosure, as well as a bookkeeping management policy, and required all subsidiaries to adhere / to the same accounting policies, bookkeeping standards, and reporting procedures. Subsidiaries / are required to submit stand

### col_CC
  - p5: If there is any change in the following expected timetable, our Company will issue / an / announcement / to
  - p5: Exchange / at / www.hkexnews.hk and the website of our Company at www.jinxunec.com. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on Wednesday, / December 31, 2025 / Latest time for completing electronic applications under / the White Form eIPO service through the designated

### col_CD
  - p5: If there is any change in the following expected timetable, our Company will issue / an / announcement / to

### col_CE
  - p93: APPLICATION FOR LISTING ON THE HONG KONG STOCK EXCHANGE / We have applied to the Listing Committee for the Listing of, and permission to deal in, / the H Shares to be issued pursuant to the Global Offering, including the H Shares which may / be issued pursuant to the exercise of the Over-allotment Option. Save for our non-H Shares / quoted on the NEEQ, no part of the H Share or loan capital of the
  - p398: custodian. / If you are applying through the White Form eIPO / service, you may refer to the table below for the / amount payable for the number of H Shares you / have / selected. / You

### col_CF
  - p15: 100.0 / 963,785 / 100.0 / The following table sets forth our gross profit and gross profit margin by business lines / for the years/periods indicated: / Year ended December 31, / Six months ended June 30,
  - p15: 100.0 / 963,785 / 100.0 / The following table sets forth our gross profit and gross profit margin by business lines / for the years/periods indicated: / Year ended December 31, / Six months ended June 30,

### col_CG
  - p52: by local authorities, as well imported goods and services, may rise significantly in association / with increased inflationary pressures, thereby impacting our ability to maintain competitive / production costs in overseas jurisdictions. In addition, inflation can cause (i) increased interest / rates, affecting our financing costs and capital expenditure plans; (ii) elevated compliance / costs and
  - p52: by local authorities, as well imported goods and services, may rise significantly in association / with increased inflationary pressures, thereby impacting our ability to maintain competitive / production costs in overseas jurisdictions. In addition, inflation can cause (i) increased interest / rates, affecting our financing costs and capital expenditure plans; (ii) elevated compliance / costs and

### col_CH
  - p413: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purpose of the / accountants’ report, a true and fair view of the Company’s and the Group’s financial position / as at 31 December 2022, 2023 and 2024 and 30 June 2025, and of the Group’s financial / perfor
  - p21: during the Track Record Period. / SUMMARY OF HISTORICAL FINANCIAL INFORMATION / The following tables set forth a summary of our consolidated financial information for the / Track Record Period, are derived from the Accountants’ Report set out in Appendix I to this / prospectus. The summary consolidated financial information set forth below should be read / together with, and is qualified in its en

### col_CI
  - p29: LISTING EXPENSES / Our listing expenses mainly include underwriting commissions, professional fees paid to / legal advisors, the Reporting Accountants and other professional parties for their services / rendered in relation to the Listing and the Global Offering.
  - p29: LISTING EXPENSES / Our listing expenses mainly include underwriting commissions, professional fees paid to / legal advisors, the Reporting Accountants and other professional parties for their services / rendered in relation to the Listing and the Global Offering.


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 3636.HK`
有 ERROR 必须回原文修正。
