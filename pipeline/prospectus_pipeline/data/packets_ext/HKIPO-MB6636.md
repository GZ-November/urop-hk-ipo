# 6636.HK 扩展 18 列抽取包

公司：6636.HK Shandong Extreme Vision Technology Co., Ltd. - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB6636.json`。
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
- 股本结构（**已确认，不要改**）：L=112914783 M=12480000 N=100434783 O=100434783 P=0 Q=12480000 R=11856000 S=624000
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = -48394666.666666664
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
{"code":"6636.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  6636.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 6636.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p17: 8,708 / (27,141) / (36,296) / For details of the Pre-IPO investments and the accounting treatment of the redemption rights, see / “History, Development and Corporate Structure — Details of the Pre-IPO Investments — Special rights / granted to the Pre-IPO Investors” and note 29 to the Accountants’ Report set out in Appendix I to this / Prospectus.
  - p17: (36,296) / For details of the Pre-IPO investments and the accounting treatment of the redemption rights, see / “History, Development and Corporate Structure — Details of the Pre-IPO Investments — Special rights / granted to the Pre-IPO Investors” and note 29 to the Accountants’ Report set out in Appendix I to this / Prospectus. / SUMMARY / – 8 –
  - p17: 8,708 / (27,141) / (36,296) / For details of the Pre-IPO investments and the accounting treatment of the redemption rights, see / “History, Development and Corporate Structure — Details of the Pre-IPO Investments — Special rights / granted to the Pre-IPO Investors” and note 29 to the Accountants’ Report set out in Appendix I to this / Prospectus.

### col_BB
  - p22: completion of the Global Offering, Mr. Chan, Ms. Luo and Hengqin Jili are expected to be entitled to / exercise an aggregate of approximately 26.54% of the voting rights in our Company. Mr. Chan, Ms. / Luo and Hengqin Jili, will remain the Single Largest Group of Shareholders upon the Listing and our / Company will not have any controlling shareholders as defined under the Listing Rules. For furth
  - p32: “subsidiary(ies)” / has the meaning ascribed thereto in section 15 of the Companies / Ordinance / “substantial shareholders” / has the meaning ascribed to it in the Listing Rules / “Takeovers Code” / The Code on Takeovers and Mergers issued by the SFC, as amended,
  - p103: the / ultimate / beneficial owner of which is Mr. Cheung Che Kit Richard, our independent non-executive Director, the / ultimate beneficial owners of the Pre-IPO Investors are Independent Third Parties. / HISTORY, DEVELOPMENT AND CORPORATE STRUCTURE / – 94 –

### col_BC
  - p22: completion of the Global Offering, Mr. Chan, Ms. Luo and Hengqin Jili are expected to be entitled to / exercise an aggregate of approximately 26.54% of the voting rights in our Company. Mr. Chan, Ms. / Luo and Hengqin Jili, will remain the Single Largest Group of Shareholders upon the Listing and our / Company will not have any controlling shareholders as defined under the Listing Rules. For furth
  - p32: “subsidiary(ies)” / has the meaning ascribed thereto in section 15 of the Companies / Ordinance / “substantial shareholders” / has the meaning ascribed to it in the Listing Rules / “Takeovers Code” / The Code on Takeovers and Mergers issued by the SFC, as amended,

### col_BD
  - p22: completion of the Global Offering, Mr. Chan, Ms. Luo and Hengqin Jili are expected to be entitled to / exercise an aggregate of approximately 26.54% of the voting rights in our Company. Mr. Chan, Ms. / Luo and Hengqin Jili, will remain the Single Largest Group of Shareholders upon the Listing and our / Company will not have any controlling shareholders as defined under the Listing Rules. For furth
  - p22: OUR SINGLE LARGEST GROUP OF SHAREHOLDERS / As of the Latest Practicable Date, pursuant to the Acting-in-Concert Agreement, Mr. Chan, Ms. / Luo and Hengqin Jili, collectively being the Single Largest Group of Shareholders, were able to / exercise an aggregate of approximately 29.85% of the voting rights in our Company. Immediately upon / completion of the Global Offering, Mr. Chan, Ms. Luo and Heng
  - p32: “subsidiary(ies)” / has the meaning ascribed thereto in section 15 of the Companies / Ordinance / “substantial shareholders” / has the meaning ascribed to it in the Listing Rules / “Takeovers Code” / The Code on Takeovers and Mergers issued by the SFC, as amended,

### col_BE
  - p20: the Global Offering, for approximately 221.7 months. We will continue to closely monitor our cash / flows used in and generated from operating activities and maintain our financial viability through a / variety of means, including, among others, banking facilities and external financings. Please refer to / “Financial Information — Indebtedness” in this Prospectus. We will continue to monitor our c
  - p242: 33,171 / 88,444 / 99,388 / Interest-bearing bank borrowings . . . . . . / 4,800 / 21,780 / 53,138
  - p92: foreign-invested enterprises, enabling them to settle foreign exchange capital based on operational / needs, subject to document verification. The circular emphasizes authentic and self-use principles / within the enterprise’s scope, barring use for payments beyond business scope, securities investment / (unless specified), Renminbi entrust loans, inter-enterprise borrowings, or real estate expens

### col_BF
  - p12: Please see “Financial Information — Key Components of Our Consolidated Statements of Profit / or Loss” for breakdowns of our revenue, gross profit, and gross profit margin by: (i) industry, (ii) / customer type, (iii) geographical location, and (iv) solution type for the periods presented. / COMMERCIALIZATION / We adopt a project-based business model for our solutions. / As of September 30, 2025, 
  - p323: Effective for annual/reporting periods beginning on or after 1 January 2027 / 3 / No mandatory effective date yet determined but available for adoption / The Group is in the process of making a detailed assessment of the impact of these new and / revised IFRS Accounting Standards upon initial application. So far, the Group considers that these new / and revised IFRS Accounting Standards, except fo

### col_BG
  - p24: RMB18.7 million for our listing expenses is expected to be expensed through the statement of profit or / loss and an estimated amount of RMB23.3 million is expected to be recognized directly as a deduction / from equity upon the Listing. / USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$434.4 million after deducting the underwriting fe
  - p264: • / Familiar with technologies like transformer, / RLHF tuning, LangChain / FUTURE PLANS AND USE OF PROCEEDS / – 255 –

### col_BI
  - p2: Number of Offer Shares under the / Global Offering / : / 12,480,000 H Shares / Number of Hong Kong Offer Shares / : / 624,000 H Shares (subject to reallocation)

### col_BP
  - p94: OVERVIEW / The predecessor of our Company, Shenzhen Extreme Vision Technology Co., Ltd.* (深圳極視角科 / 技有限公司), was established on June 15, 2015, as a limited liability company in the PRC. On April 26, / 2023, our Company was converted into a joint-stock limited company and was renamed Shandong / Extreme Vision Technology Co., Ltd.* (山東極視角科技股份有限公司). Our founders, Mr. Chan and / Ms. Luo, became acquaint
  - p1: Shandong Extreme Vision Technology Co., Ltd.* / 山東極視角科技股份有限公司 / (a joint stock company incorporated in the People’s Republic of China with limited liability) / Stock Code : 6636 / Sole Sponsor, Overall Coordinator, Sole Global Coordinator, Joint Bookrunner and Joint Lead Manager / GLOBAL OFFERING

### col_BR
  - p71: Registered Office, Head Office and Principal / Place of Business in the PRC / Principal Place of Business in / Hong Kong / Room 1201 / Jingkong Building
  - p71: Registered Office, Head Office and Principal / Place of Business in the PRC / Principal Place of Business in / Hong Kong
  - p71: Registered Office, Head Office and Principal / Place of Business in the PRC / Principal Place of Business in / Hong Kong

### col_BT
  - p18: To supplement our consolidated financial statements which are presented in accordance with IFRS / Accounting Standards, we also use non-IFRS measures, namely, adjusted (loss)/profit (non-IFRS / measures), as additional financial metrics, which are not required by, or presented in accordance with, / IFRS Accounting Standards. / Our Directors are of the view that (1) share-based payments are non-cas
  - p408: The Preliminary Financial Information does not include all of the information required for a / complete set of financial statements prepared in accordance with the IFRS Accounting Standards. / 3. / ISSUED BUT NOT YET EFFECTIVE HKFRS ACCOUNTING STANDARDS / The Group has not applied the following new and revised IFRS Accounting Standards, that have / been issued but are not yet effective, in the His
  - p18: NON-IFRS MEASURES / To supplement our consolidated financial statements which are presented in accordance with IFRS / Accounting Standards, we also use non-IFRS measures, namely, adjusted (loss)/profit (non-IFRS / measures), as additional financial metrics, which are not required by, or presented in accordance with, / IFRS Accounting Standards. / Our Directors are of the view that (1) share-based 

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public Offering, / we will issue an announcement to be published on the website of the Stock Exchange at / www.hkexnews.hk and our Company’s website at www.extremevision.com.cn. / Date(1)
  - p5: we will issue an announcement to be published on the website of the Stock Exchange at / www.hkexnews.hk and our Company’s website at www.extremevision.com.cn. / Date(1) / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9:00 a.m. on Friday, / March 20, 2026 / Latest time for completing electronic applications / under HK eIPO White Form service throu

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public Offering, / we will issue an announcement to be published on the website of the Stock Exchange at / www.hkexnews.hk and our Company’s website at www.extremevision.com.cn. / Date(1)

### col_CE
  - p218: H Shares to be converted from Unlisted Shares(1) . . . . . . . . . . . . / 99,872,436 / 88.45% / H Shares to be issued pursuant to the Global Offering . . . . . . . . / 12,480,000 / 11.05% / Total . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  - p3: Your application through the HK eIPO White Form service or the HKSCC EIPO channel must / be for a minimum of 50 Hong Kong Offer Shares and in one of the numbers set out in the table. If you / are applying through the HK eIPO White Form service, you may refer to the table below for the / amount payable for the number of H Shares you have selected. You must pay the respective amount / IMPORTANT

### col_CF
  - p12: The following table sets forth a breakdown of our gross profit and gross profit margin by business / segments for the periods indicated: / For the Year Ended December 31, / For the Nine Months Ended September 30,
  - p12: The following table sets forth a breakdown of our gross profit and gross profit margin by business / segments for the periods indicated: / For the Year Ended December 31, / For the Nine Months Ended September 30,

### col_CG
  - p37: plans; our ability to successfully implement our business plans and strategies; our financial / condition and performance, debt levels and capital needs; our dividend policy; / • / our capital expenditure plans; various business opportunities that we may pursue; the actions / and developments of our competitors; changes or volatility in interest rates, foreign / exchange rates, equity prices or ot
  - p37: plans; our ability to successfully implement our business plans and strategies; our financial / condition and performance, debt levels and capital needs; our dividend policy; / • / our capital expenditure plans; various business opportunities that we may pursue; the actions / and developments of our competitors; changes or volatility in interest rates, foreign / exchange rates, equity prices or ot

### col_CH
  - p308: Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the accountants’ / report, a true and fair view of the financial position of the Group and the Company as at 31 December / 2022, 2023, 2024 and 30 September 2025 and of the financial performance and cash flows of the Group / for each of the Relevant Periods in accordance with the basis of preparation set out 
  - p16: SUMMARY OF HISTORICAL FINANCIAL INFORMATION / The summary of the key financial information set forth below has been derived from and should / be read in conjunction with our consolidated financial statements, including the accompanying notes, / set forth in the Accountants’ Report in Appendix I to this Prospectus, as well as the information set / forth in the section headed “Financial Information.

### col_CI
  - p18: 11,786 / 8,803 / 9,288 / Listing expenses . . . . . . . / — / — / —
  - p18: 11,786 / 8,803 / 9,288 / Listing expenses . . . . . . . / — / — / —


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 6636.HK`
有 ERROR 必须回原文修正。
