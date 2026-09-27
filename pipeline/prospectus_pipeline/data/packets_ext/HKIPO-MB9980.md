# 9980.HK 扩展 18 列抽取包

公司：9980.HK Eastroc Beverage (Group) Co., Ltd. - H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB9980.json`。
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
- 股本结构（**已确认，不要改**）：L=560902900 M=40889900 N=520013000 O=520013000 P=0 Q=40889900 R=36800900 S=4089000
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = 5013082666.666667
- 行业分类（港交所官方）：251030 非酒精飲料
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
{"code":"9980.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  9980.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 9980.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
（锚点无命中，需要自己 search）

### col_BB
  - p25: beverage industry in terms of sales volume increased from 57.8% in 2022 to 61.6% in 2024, / reflecting the further consolidation of the industry. We believe that we are well-positioned to / compete effectively given our competitive strengths and strategies. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Lin directly held as beneficial owner 49.74% of our / total issued sha
  - p43: “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Takeovers Code” or “Hong Kong / Takeovers Code”
  - p331: Fund Series — China Opportunity Equity (USD); (iv) UBS (Lux) Equity SICAV — All China / (USD); (v) UBS (Lux) Investment SICAV — China A Opportunity (USD); (vi) UBS (CAY) China / A Opportunity; and (vii) certain other segregated accounts and mandates. To the best of UBS AM / Singapore’s knowledge, no single ultimate beneficial owner holds 30% or more interest in those / funds. UBS AM Singapore is a

### col_BC
  - p25: beverage industry in terms of sales volume increased from 57.8% in 2022 to 61.6% in 2024, / reflecting the further consolidation of the industry. We believe that we are well-positioned to / compete effectively given our competitive strengths and strategies. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Lin directly held as beneficial owner 49.74% of our / total issued sha
  - p43: “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Takeovers Code” or “Hong Kong / Takeovers Code”

### col_BD
  - p25: beverage industry in terms of sales volume increased from 57.8% in 2022 to 61.6% in 2024, / reflecting the further consolidation of the industry. We believe that we are well-positioned to / compete effectively given our competitive strengths and strategies. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Lin directly held as beneficial owner 49.74% of our / total issued sha
  - p84: certain / existing / minority / Shareholders who (i) hold less than 5% of the voting rights in our Company prior to the / completion of the Global Offering and (ii) are not and will not become (upon the completion of / the Global Offering) core connected persons of our Company or the close associates of any such / core connected person (together, the “Permitted Existing Shareholder”), on the follo
  - p43: “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Takeovers Code” or “Hong Kong / Takeovers Code”

### col_BE
  - p30: No Material Adverse Change / Our Directors have confirmed that, up to the date of this Prospectus, there has been no / material adverse change in our financial, operational or trading position, indebtedness, contingent / liabilities or prospects since September 30, 2025, being the end date of our latest audited financial / statements, and there has been no event since September 30, 2025 that would
  - p316: Calculated by current assets as of the end of the year/period less inventories as of the end of the same year/period / divided by current liabilities as of the end of the same year/period. / (7) / Calculated by total debt (including lease liabilities and interest-bearing debt borrowings) as of the end of the / year/period divided by total equity as of the end of the same year/period and multiplied
  - p23: We recorded net current liabilities of RMB2,139.4 million as of December 31, 2024, / compared to net current assets of RMB721.2 million as of December 31, 2023. The change was / primarily due to (i) the increase in the current portion of borrowings of RMB3,535.4 million, (ii) / the increase in contract liabilities of RMB2,153.3 million, mainly attributable to the increase in / advance payment rece

### col_BF
  - p270: The historical financial information of our Group has been prepared in accordance with IFRS. / The preparation of the historical financial information in conformity with IFRS requires the use of / certain material accounting policy information. It also requires management to make judgements, / estimates and assumptions in the process of applying our Group’s accounting policies. Judgements / made b

### col_BG
  - p28: Relating to the Global Offering — Our historical dividends may not be indicative of our future / dividend policy, and there can be no assurance that we will declare and distribute dividend in the / future” in this Prospectus for details. / USE OF PROCEEDS / Based on an Offer Price of HK$248.00, we estimate that we will receive net proceeds of / approximately HK$9,994.3 million from the Global Offe
  - p312: assets at FVTPL of RMB3,608.3 million. / Net Cash Generated from/Used in Financing Activities / Net cash used in financing activities in the nine months ended September 30, 2025 was / RMB2,275.5 million, which primarily consisted of (i) repayment of borrowings of RMB6,862.6 / million, and (ii) dividends paid of RMB2,600.0 million; partially offset by additions of borrowings / of RMB7,283.1 million
  - p58: prospects could be adversely affected. / We continually evaluate the potentials of new business initiatives or new markets. For / example, we plan to expand into overseas markets with a priority on the Southeast Asian market. / See “Future Plans and Use of Proceeds” for details. The overseas markets in which we plan to / enter / in / the

### col_BI
  - p2: GLOBAL OFFERING / Number of Offer Shares under the Global Offering / : / 40,889,900 H Shares (subject to the Over-allotment / Option) / Number of Hong Kong Offer Shares / :

### col_BP
  - p1: Eastroc Beverage (Group) Co., Ltd. / 東鵬飲料（集團）股份有限公司 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / Stock Code : 09980 / Joint Sponsors, Overall Coordinators, Joint Global Coordinators, / Joint Bookrunners and Joint Lead Managers

### col_BR
  - p107: Shenzhen / Guangdong Province / PRC / Principal Place of Business / in Hong Kong / 40th Floor, Dah Sing Financial Centre / 248 Queen’s Road East
  - p107: Registered Office / 1/F, Building 3 / Zhongguan Honghualing Industry Western District / 142 Zhuguang North Road

### col_BT
  - p430: accountants’ report. / The consolidated financial statements of the Group for the Track Record Period, on which the / Historical Financial Information is based, have been prepared in accordance with the accounting / policies which conform with IFRS Accounting Standards issued by the International Accounting / Standards Board (the “IASB”) and were audited by us in accordance with International Stan
  - p37: others, the Company and the Overall Coordinators (for / themselves and on behalf of the Hong Kong Underwriters) / “IASB” / International Accounting Standards Board / “IFRS” / the International Financial Reporting Standards, which as / collective
  - p26: Company for the year ended December 31, 2025 based on (i) the audited consolidated results of our Group for the / nine months ended September 30, 2025; and (ii) the unaudited consolidated results of our Group for the three / months ended December 31, 2025 based on the management accounts of our Group. The profit estimate has been / prepared on a basis consistent in all material respects with the a

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, our Company will issue an announcement to be published on the website of the Stock / Exchange at www.hkexnews.hk and the website of our Company www.szeastroc.com. / Date(1)
  - p5: Offering, our Company will issue an announcement to be published on the website of the Stock / Exchange at www.hkexnews.hk and the website of our Company www.szeastroc.com. / Date(1) / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9:00 a.m. on / Monday, January 26, 2026 / Latest time to complete electronic applications / under White Form 

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, our Company will issue an announcement to be published on the website of the Stock / Exchange at www.hkexnews.hk and the website of our Company www.szeastroc.com. / Date(1)

### col_CE
  - p155: Price of HK$248.00 per H Share, the minimum prescribed public float percentage under Rule / 19A.13A(2)(b) of the Listing Rules would be approximately 2.16%, being the percentage derived / by dividing HK$3,000,000,000 by the total market value of the Company’s total issued shares at / the time of Listing. The total number of the H Shares to be issued pursuant to the Global Offering / represents app
  - p87: maximum number of H Shares that any individual Eligible Employee may indirectly apply for / under the Employee Preferential Offering will be limited to 43,000 H Shares, representing / approximately / 6.41%

### col_CF
  - p17: The following table sets forth a breakdown of the gross profit and gross profit margin of our / beverage products for the periods indicated: / For the year ended December 31, / For the nine months ended September 30,
  - p17: The following table sets forth a breakdown of the gross profit and gross profit margin of our / beverage products for the periods indicated: / For the year ended December 31, / For the nine months ended September 30,

### col_CG
  - p27: in the future after taking into account our results of operations, financial condition, cash / requirements and availability and other factors as it may deem relevant at such time. The Dividend / Policy sets out our guiding principles for shareholder return over the next three years, including (i) / giving due regard to sustainable business development, capital expenditure plans and liquidity / po
  - p27: in the future after taking into account our results of operations, financial condition, cash / requirements and availability and other factors as it may deem relevant at such time. The Dividend / Policy sets out our guiding principles for shareholder return over the next three years, including (i) / giving due regard to sustainable business development, capital expenditure plans and liquidity / po

### col_CH
  - p596: 3. / An All-Directional Automatic / Rejection Device for / Unqualified Packaging (一 / 種全方位自動剔除包裝不 / 合格裝置) . . . . . . . . . . / Utility
  - p542: Opinion / In our opinion: / (a) / the unaudited pro forma financial information has been properly compiled on the basis / stated;
  - p20: attributable to owners of our Company for the periods to which such dividends related, reflecting / our commitment to returning value to investors. / The following tables set forth summary financial data from our financial information during / the Track Record Period, extracted from the Accountants’ Report in Appendix I to this Prospectus. / The summary financial data set forth below should be rea

### col_CI
  - p21: (0.6) / (76,782) / (0.5) / Listing expenses . . . . . . . . . . . / — / — / —
  - p21: (0.6) / (76,782) / (0.5) / Listing expenses . . . . . . . . . . . / — / — / —
  - p389: UNDERWRITING COMMISSIONS AND LISTING EXPENSES / The Underwriters and the Capital Market Intermediaries will receive an underwriting / commission equal to 0.6% of the aggregate Offer Price payable for the Offer Shares (including the / Offer Shares to be issued pursuant to the Over-allotment Option, if any) (the “Fixed Fees”). Our


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 9980.HK`
有 ERROR 必须回原文修正。
