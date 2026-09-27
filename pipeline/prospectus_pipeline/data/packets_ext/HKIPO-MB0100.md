# 0100.HK 扩展 18 列抽取包

公司：0100.HK MiniMax Group Inc. - W - P

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB0100.json`。
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
- 股本结构（**已确认，不要改**）：L=305447288 M=25389220 N=280058068 O=280058068 P=0 Q=25389220 R=24119740 S=1269480
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = USD；year-1 净利 = -682684000.0
- 行业分类（港交所官方）：702030 應用軟件
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
{"code":"0100.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  0100.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 0100.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p28: Awakening, MiniMax Limited, Alpha EXP, Scaling EXP Limited, and MiniMax Matrix / together will constitute as a group of Controlling Shareholders of our Company after the / Listing. / PRE-IPO INVESTMENTS / We have undertaken several rounds of Pre-IPO Investments. For details of the background / of our key Pre-IPO Investors and the principal terms of the Pre-IPO Investments, see “History, / Reorgani
  - p28: Listing. / PRE-IPO INVESTMENTS / We have undertaken several rounds of Pre-IPO Investments. For details of the background / of our key Pre-IPO Investors and the principal terms of the Pre-IPO Investments, see “History, / Reorganization and Corporate Structure — Pre-IPO Investments.” / LOCK-UP REQUIREMENTS UNDER RULE 18C.14 OF THE LISTING RULES / Dr. Yan, Ms. Yun and their close associates as well a
  - p28: Awakening, MiniMax Limited, Alpha EXP, Scaling EXP Limited, and MiniMax Matrix / together will constitute as a group of Controlling Shareholders of our Company after the / Listing. / PRE-IPO INVESTMENTS / We have undertaken several rounds of Pre-IPO Investments. For details of the background / of our key Pre-IPO Investors and the principal terms of the Pre-IPO Investments, see “History, / Reorgani

### col_BB
  - p28: OUR CONTROLLING SHAREHOLDERS / Immediately following the completion of the Global Offering (assuming the Offer Size / Adjustment Option and the Over-allotment Option are not exercised), an aggregate of / 5,000,000 Class A Ordinary Shares and 74,102,534 Class B Ordinary Shares, representing
  - p57: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Track Record Period” / the
  - p222: below), miHoYo SIIs (as defined below), IDG SIIs (as defined below) and Image Frame / (as defined below), and two of which, namely IDG SIIs and miHoYo SIIs, are our / Pathfinder SIIs. Save for being a shareholder of our Company and as disclosed otherwise, / each of our Sophisticated Independent Investors and their ultimate beneficial owners is / independent from and not connected with any Director

### col_BC
  - p28: OUR CONTROLLING SHAREHOLDERS / Immediately following the completion of the Global Offering (assuming the Offer Size / Adjustment Option and the Over-allotment Option are not exercised), an aggregate of / 5,000,000 Class A Ordinary Shares and 74,102,534 Class B Ordinary Shares, representing
  - p57: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Track Record Period” / the

### col_BD
  - p28: OUR CONTROLLING SHAREHOLDERS / Immediately following the completion of the Global Offering (assuming the Offer Size / Adjustment Option and the Over-allotment Option are not exercised), an aggregate of / 5,000,000 Class A Ordinary Shares and 74,102,534 Class B Ordinary Shares, representing
  - p1: Stock Code : 0100 / (A company controlled through weighted voting rights and / incorporated in the Cayman Islands with limited liability) / MiniMax Group Inc. / GLOBAL
  - p57: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Track Record Period” / the

### col_BE
  - p467: INDEBTEDNESS / The following table sets forth our indebtedness as of the dates indicated. / As of December 31, / As of
  - p32: 805,648 / 1,051,772 / CURRENT LIABILITIES / Interest-bearing bank / borrowings            / – / –
  - p32: 1,051,772 / CURRENT LIABILITIES / Interest-bearing bank / borrowings            / – / – / 19,455

### col_BF
  - p12: We believe scalability is pivotal to our long-term goals. To build one of the most scalable / AI businesses globally, we focus on three core competencies — original research, a sustainable / business model, and organizational efficiency. These pillars support both continuous model / advancement and product commercialization at scale. Together, the three core competencies / enable an elevated level
  - p43: We are in the process of reviewing these regulations to ensure the continued compliance / of our Talkie application. Based on (i) an assessment of the current features and functionalities / of Talkie and (ii) research conducted on existing state legislation and regulations governing / chatbots, as advised by our U.S. data legal advisor, (a) the current features and design of Talkie

### col_BG
  - p40: Future Plans and Use of Proceeds / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$3,818.3 million, after deducting underwriting commissions, fees and estimated expenses / payable by us in connection with the Global Offering, assuming the Offer Size Adjustment
  - p40: Future Plans and Use of Proceeds / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$3,818.3 million, after deducting underwriting commissions, fees and estimated expenses / payable by us in connection with the Global Offering, assuming the Offer Size Adjustment

### col_BI
  - p511: Over-allotment Option is exercised in full. / The stock borrowing arrangement described above will be effected in compliance with all / applicable laws, rules and regulatory requirements. No payment will be made to MiniMax / Matrix by the Stabilizing Manager (or any person acting for it) in relation to such Shares / borrowing arrangement. / PRICING AND ALLOCATION / Determining the Pricing of the O
  - p6: unsuccessful applications under the Hong Kong / Public Offering to be dispatched on or before(8)(9) / . . . . . . . . . . . Friday, January 9, 2026 / Dealings in the Class A Ordinary Shares on the Hong Kong Stock / Exchange expected to commence at 9:00 a.m. on . . . . . . . . . . . . .Friday, January 9, 2026 / EXPECTED TIMETABLE(1) / – v –

### col_BP
  - p214: MAJOR SHAREHOLDING CHANGES OF OUR COMPANY / (1) / Incorporation of our Company / Our Company was incorporated on June 30, 2021 in the Cayman Islands as an exempted / company with limited liability with an authorized share capital of US$50,000 divided into / 50,000 shares with a par value of US$1. At the time of the incorporation of our Company, we / were beneficially owned by Dr. Yan as to 98.5% a
  - p1: Stock Code : 0100 / (A company controlled through weighted voting rights and / incorporated in the Cayman Islands with limited liability) / MiniMax Group Inc. / GLOBAL / OFFERING

### col_BR
  - p41: report, certain investments in covered foreign persons, which are defined as “covered / transactions,” and include acquisitions of equity interests (including contingent equity / interests), certain debt financing, joint ventures, and certain investments as a limited partner / in a non-U.S. person pooled investment fund. Since our principal place of business is in China / and we engage in the deve
  - p151: Registered Office / Maples Corporate Services Limited / PO Box 309, Ugland House / Grand Cayman, KY1-1104
  - p151: PO Box 309, Ugland House / Grand Cayman, KY1-1104 / Cayman Islands / Head Office and Principal Place of / Business in the PRC / 11th Floor, Building B / Xinyan Mansion

### col_BT
  - p50: under the Classification Catalogue Telecommunications / Services (《電信業務分類目錄》) / “IFRSs” / the IFRS Accounting Standards, which include standards, / amendments / and / interpretations
  - p555: acquisition of 100% equity interest. / (f) / MiniMax HONGKONG Limited is registered as a limited liability company under Hong Kong law. The / statutory financial statements for the year ended 2024 under the HKFRSs for Private Entities were / audited by Raymond Li&Co., certified public accountants registered in Hong Kong. / 2. / ACCOUNTING POLICIES
  - p50: under the Classification Catalogue Telecommunications / Services (《電信業務分類目錄》) / “IFRSs” / the IFRS Accounting Standards, which include standards, / amendments / and / interpretations

### col_CC
  - p5: If there is any change in the following expected timetable, we will issue an / announcement / to / be
  - p5: at / https://www.minimaxi.com and the Stock Exchange at www.hkexnews.hk. / Date(1) / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on / Wednesday, December 31, 2025 / Latest time for completing electronic applications under / HK eIPO White Form service through the designated website

### col_CD
  - p5: If there is any change in the following expected timetable, we will issue an / announcement / to / be

### col_CE
（锚点无命中，需要自己 search）

### col_CF
  - p36: product suite, increased adoption by individual users, developers, and enterprise customers, / and diversified monetization channels across subscriptions, in-app top-up, enterprise API / usage, and online marketing services. / As we scaled up operations, we significantly improved our gross profit margin, from / negative 24.7% in 2023 to 12.2% in 2024, and further to 23.3% in the nine months ended 
  - p36: product suite, increased adoption by individual users, developers, and enterprise customers, / and diversified monetization channels across subscriptions, in-app top-up, enterprise API / usage, and online marketing services. / As we scaled up operations, we significantly improved our gross profit margin, from / negative 24.7% in 2023 to 12.2% in 2024, and further to 23.3% in the nine months ended 

### col_CG
  - p35: promotion to acquire and engage users, and general and administrative expenses. These factors / collectively resulted in net operating cash outflows throughout the Track Record Period. / Our cash burn refers to the aggregate amount of (i) net cash used in operating activities, / (ii) capital expenditures, and (iii) lease payment. Our historical cash burn was US$11.5 million, / US$65.9 million, US$
  - p35: promotion to acquire and engage users, and general and administrative expenses. These factors / collectively resulted in net operating cash outflows throughout the Track Record Period. / Our cash burn refers to the aggregate amount of (i) net cash used in operating activities, / (ii) capital expenditures, and (iii) lease payment. Our historical cash burn was US$11.5 million, / US$65.9 million, US$

### col_CH
  - p539: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the / accountants’ report, a true and fair view of the financial position of the Group and the Company / as at 31 December 2022, 2023 and 2024 and 30 September 2025, and of the financial / perfo
  - p28: required under Rule 18C.24 of the Listing Rules. / SUMMARY OF HISTORICAL FINANCIAL INFORMATION / The following tables set forth summary financial data from our consolidated financial / information for the Track Record Period, extracted from the Accountants’ Report set out in / Appendix I. You should read this summary in conjunction with our consolidated financial / information included in the Acco

### col_CI
  - p30: value losses on financial liabilities, comprising fair value changes of convertible redeemable / preferred shares which will be re-designated from liabilities to equity as a result of the / automatic conversion into ordinary shares upon Listing, and convertible bonds, which have / subsequently been repaid in full as of the Latest Practicable Date, and (iii) listing expenses. / The following table 
  - p30: value losses on financial liabilities, comprising fair value changes of convertible redeemable / preferred shares which will be re-designated from liabilities to equity as a result of the / automatic conversion into ordinary shares upon Listing, and convertible bonds, which have / subsequently been repaid in full as of the Latest Practicable Date, and (iii) listing expenses. / The following table 


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 0100.HK`
有 ERROR 必须回原文修正。
