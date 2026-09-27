# 6082.HK 扩展 18 列抽取包

公司：6082.HK Shanghai Biren Technology Co., Ltd.- H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB6082.json`。
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
- 股本结构（**已确认，不要改**）：L=2358977900 M=247692800 N=2111285100 O=2111285100 P=0 Q=247692800 R=235308000 S=12384800
- 财务期间（**已确认**）：year-1 期末 = 30/06/25；币种 = RMB；year-1 净利 = -3201052000
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
{"code":"6082.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  6082.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 6082.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p33: of the Global Offering (assuming that the Offer Size Adjustment Option and the Over-allotment / Option are not exercised), our Single Largest Group of Shareholders will control approximately / 15.87% of our total issued share capital. / Pre-IPO Investments / We completed several rounds of Pre-IPO Investments since our inception with an / aggregate amount of over RMB9 billion raised. We have five S
  - p33: Venture Capital and Huibi No. 2), Sky9 Capital, Zhuhai Gree and Shenzhen Songhe, which are / also our Pathfinder SIIs. See “History, Development and Corporate Structure – Pre-IPO / Investments” for the details of the Pre-IPO Investments, our Sophisticated Independent / Shareholders and Pre-IPO Investors. / DIVIDEND / We do not have any fixed dividend policy nor pre-determined dividend payout ratio
  - p33: of the Global Offering (assuming that the Offer Size Adjustment Option and the Over-allotment / Option are not exercised), our Single Largest Group of Shareholders will control approximately / 15.87% of our total issued share capital. / Pre-IPO Investments / We completed several rounds of Pre-IPO Investments since our inception with an / aggregate amount of over RMB9 billion raised. We have five S

### col_BB
  - p161: and relevant state rules; (ii) where the intended securities offering and listing may endanger / national security as reviewed and determined by competent authorities under the State Council / in accordance with law; (iii) where the domestic company intending to make the securities / offering and listing, or its controlling shareholder(s) and the actual controller, have committed / crimes such as 
  - p46: our / Directors, / Senior / Management and Substantial Shareholders – 5. Pre-IPO / Employee Incentive Scheme” / “Pre-IPO Investment(s)” / the investment(s) in our Company undertaken by the
  - p187: Independent Investors is independent from and not connected with any Director, chief / executive or substantial shareholder of our Company, its subsidiaries or any of their respective / associates (within the meaning of the Listing Rules). Save as disclosed otherwise, each of the / general partners, ultimate beneficial owners, and limited partners and shareholders holding / 30% or more of the part

### col_BC
  - p161: and relevant state rules; (ii) where the intended securities offering and listing may endanger / national security as reviewed and determined by competent authorities under the State Council / in accordance with law; (iii) where the domestic company intending to make the securities / offering and listing, or its controlling shareholder(s) and the actual controller, have committed / crimes such as 
  - p46: our / Directors, / Senior / Management and Substantial Shareholders – 5. Pre-IPO / Employee Incentive Scheme” / “Pre-IPO Investment(s)” / the investment(s) in our Company undertaken by the

### col_BD
  - p161: and relevant state rules; (ii) where the intended securities offering and listing may endanger / national security as reviewed and determined by competent authorities under the State Council / in accordance with law; (iii) where the domestic company intending to make the securities / offering and listing, or its controlling shareholder(s) and the actual controller, have committed / crimes such as 
  - p142: Mechanism in advance and shall not proceed the foreign investments until the Office of / Working Mechanism decides whether to initiate the security review. “Actual control” exists / where the foreign investor (i) holds no less than 50% equity interests in the target enterprise; / (ii) holds voting rights that can materially impact on the resolutions of the board of directors / or shareholders meet
  - p46: our / Directors, / Senior / Management and Substantial Shareholders – 5. Pre-IPO / Employee Incentive Scheme” / “Pre-IPO Investment(s)” / the investment(s) in our Company undertaken by the

### col_BE
  - p36: offshore transactions in reliance on Regulation S under the U.S. Securities Act. / No Material Change / Our Directors confirm that, as of the date of this Prospectus, there has been no material / adverse change in our financial or trading position, indebtedness, mortgage, contingent / liabilities, guarantees or prospects since June 30, 2025, the end of the period reported on the / Accountant’s Rep
  - p417: We did not have any outstanding balance of bank borrowings as of December 31, 2022, / 2023 and 2024. As of June 30, 2025 and October 31, 2025, we had outstanding bank / borrowings in the amount of RMB200.1 million and RMB200.5 million, respectively, / representing short-term interest-bearing credit loans. / Our Directors confirm that, during the Track Record Period and up to the date of this / Pro
  - p84: or net current liabilities could constrain our operational flexibility and adversely affect our / ability to expand our business. If we do not generate sufficient cash flow from our operations / to meet our present and future liquidity needs, we may need to rely on additional external / borrowings for funding. If adequate funds are not available, whether on satisfactory terms or / at all, we may b

### col_BF
  - p12: advanced interconnection specifications, according to CIC. Our SoC design / methodology and workflow ensure successful VLSI (Very Large Scale Integrated / Circuit) execution and first-time-right tape-out, which help us achieve mass / production and commercialization with our first generation products. / SUMMARY / – 2 –
  - p171: RMB330 million / We successfully taped-out BR110 / 2023 / We achieved mass production of BR106 and started to generate revenue / from our intelligent computing solutions / We joined the FlagOpen large model technology open source system of / the Beijing Academy of Artificial Intelligence
  - p95: and fluctuation of the market prices of other companies with business operations located / mainly in Chinese Mainland that have listed their securities in Hong Kong may affect the / volatility in the price of and trading volumes for our H Shares. A number of Chinese / Mainland-based companies have listed their securities, and some are in the process of / preparing for listing their securities, in 

### col_BG
  - p32: FUTURE PLANS AND USE OF PROCEEDS / We estimate the net proceeds of the Global Offering which we will receive, assuming an / Offer Price of HK$18.30 per Offer Share (being the mid-point of the Offer Price range stated / in the Prospectus), will be approximately HK$4,350.6 million, after deduction of underwriting
  - p32: FUTURE PLANS AND USE OF PROCEEDS / We estimate the net proceeds of the Global Offering which we will receive, assuming an / Offer Price of HK$18.30 per Offer Share (being the mid-point of the Offer Price range stated / in the Prospectus), will be approximately HK$4,350.6 million, after deduction of underwriting

### col_BI
  - p2: Number of Offer Shares under / the Global Offering / : / 247,692,800 H Shares (subject to the / Offer Size Adjustment Option and the / Over-allotment Option) / Number of Hong Kong Offer Shares

### col_BP
  - p1: GLOBAL / OFFERING / (A joint stock company incorporated in the People's Republic of China with limited liability) / Stock Code : 6082 / 上海壁仞科技股份有限公司 / Shanghai Biren Technology Co., Ltd.

### col_BR
  - p121: No. 2388 Chenhang Road / Minhang District, Shanghai / PRC / Principal Place of Business in / Hong Kong / Room 1919, 19/F, Lee Garden One / 33 Hysan Avenue
  - p121: Registered Office / Room 1302, 13/F, Building 16 / No. 2388 Chenhang Road / Minhang District, Shanghai

### col_BT
  - p361: the / historical / financial / information in conformity with IFRS Accounting Standards requires the use of certain critical / accounting estimates. It also requires management to make judgements, estimates and / assumptions in the process of applying our accounting policies. Judgements made by / management in the application of IFRS Accounting Standards that have significant effect on
  - p361: future revenue when realized. / BASIS OF PRESENTATION / The historical financial information of our Group has been prepared in accordance with / International Financial Reporting Standards issued by the International Accounting Standards / Board / (“IFRS Accounting / Standards”).
  - p316: relation to the potential non-compliance with our code of conduct, work ethics, and violations / of our internal policies or illegal acts at all levels of our Group. / Financial Reporting Risk Management / We have adopted comprehensive accounting policies in connection with our financial / reporting risk management, such as financial management, budget management and financial / statement preparat

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on the Company’s / website / at
  - p5: Exchange / at / www.hkexnews.hk. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on Monday, / December 22, 2025 / Latest time to complete electronic applications under HK eIPO / White Form service through the designated website at

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on the Company’s / website / at

### col_CE
  - p30: to enhance operational efficiency and support sustainable long-term growth. / APPLICATION FOR LISTING OF THE H SHARES ON THE STOCK EXCHANGE / We have applied to the Stock Exchange for the granting of the listing of, and permission / to deal in, the H Shares to be issued pursuant to the Global Offering (including (i) any H Shares / that may be issued under the Offer Size Adjustment Option and the O
  - p451: The dilution effect of the Offer Size Adjustment Option (assuming the Over-allotment / Option is not exercised) is set out below: / Number of H Shares issued / under the Global Offering / before the exercise of the / Offer Size Adjustment Option

### col_CF
  - p20: (157,606) / (11,395) / (40,134) / Gross profit / 499 / 47,403 / 179,197
  - p20: (157,606) / (11,395) / (40,134) / Gross profit / 499 / 47,403 / 179,197

### col_CG
  - p13: the demand for computing power. Key sectors, including AI data centers, AI solutions and / Internet, are at the forefront of the race, significantly increasing their investment in computing / power and related infrastructure. Moreover, leading companies within these industries account / for the majority of capital expenditures on computing power. Hence, we implement the strategy / that targets key
  - p13: the demand for computing power. Key sectors, including AI data centers, AI solutions and / Internet, are at the forefront of the race, significantly increasing their investment in computing / power and related infrastructure. Moreover, leading companies within these industries account / for the majority of capital expenditures on computing power. Hence, we implement the strategy / that targets key
  - p589: grant will be received and the Group will comply with all attached conditions. / Government grants relating to costs and expenses are deferred and recognised in the profit or loss over the / period necessary to match them with the costs and expenses that they are intended to compensate. / Government grants relating to the purchase of property, plant and equipment are included in non-current / liab

### col_CH
  - p477: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the / accountant’s report, a true and fair view of the financial position of the Company as at 31 / December 2022, 2023 and 2024 and 30 June 2025 and the consolidated financial position of / the
  - p476: Company’s reporting accountant, PricewaterhouseCoopers, Certified Public Accountants, / Hong Kong, for the purpose of incorporation in this prospectus. It is prepared and addressed / to the directors of the Company and to the Joint Sponsors pursuant to the requirements of / HKSIR 200, Accountants’ Reports on Historical Financial Information in Investment Circulars / issued by the Hong Kong Institu

### col_CI
  - p21: measures differently, limiting their usefulness as comparative measures to our data. / We define our adjusted loss for the year/period (non-IFRS measure) by adding back (i) / changes in the carrying value of redemption liabilities, (ii) share-based compensation / expenses, and (iii) listing expenses, to loss for the year/period. We exclude these items because / they are not expected to result in f
  - p21: measures differently, limiting their usefulness as comparative measures to our data. / We define our adjusted loss for the year/period (non-IFRS measure) by adding back (i) / changes in the carrying value of redemption liabilities, (ii) share-based compensation / expenses, and (iii) listing expenses, to loss for the year/period. We exclude these items because / they are not expected to result in f


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 6082.HK`
有 ERROR 必须回原文修正。
