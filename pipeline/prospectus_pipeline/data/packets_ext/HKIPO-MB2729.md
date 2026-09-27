# 2729.HK 扩展 18 列抽取包

公司：2729.HK Zhejiang Galaxis Technology Group Co., Ltd. - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB2729.json`。
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
- 股本结构（**已确认，不要改**）：L=427883729 M=36798000 N=391085729 O=391085729 P=0 Q=36798000 R=33118200 S=3679800
- 财务期间（**已确认**）：year-1 期末 = 30/09/2025；币种 = RMB；year-1 净利 = -179294666.66666666
- 行业分类（港交所官方）：701030 機器人系統及解決方案
- 基石投资者：确认无

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
{"code":"2729.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  2729.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 2729.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p23: Pre-IPO Investors / Since the establishment of our Group, we have attracted a broad and diversified base of / Pre-IPO Investors through equity financings and share transfers. For details of our Pre-IPO / Investors and the principal terms of the Pre-IPO Investments, see “History, Development and / Corporate Structure — Pre-IPO Investments.” / Share Incentive Schemes / We adopted Restricted Share In
  - p17: Equity settled share-based payment expenses are non-cash in nature. / (2) / Changes in the carrying amount of the redemption liability represents the changes in the carrying amount of / the redeemable special rights that we granted to certain Pre-IPO Investors. Such changes are non-cash in / nature. Upon completion of the Global Offering, the financial liabilities will be re-designated from liabil
  - p23: Pre-IPO Investors / Since the establishment of our Group, we have attracted a broad and diversified base of / Pre-IPO Investors through equity financings and share transfers. For details of our Pre-IPO / Investors and the principal terms of the Pre-IPO Investments, see “History, Development and / Corporate Structure — Pre-IPO Investments.” / Share Incentive Schemes / We adopted Restricted Share In

### col_BB
  - p22: Acting-in-Concert and Our Single Largest Group of Shareholders / As of the Latest Practicable Date, pursuant to a series of Concert Party Agreements, Dr. GU, / together with the Pre-Listing Concert Parties, are able to exercise approximately 40.30% of the / voting rights in the Company, and therefore constituted a group of controlling shareholders (as / defined in the Listing Rules) of the Company
  - p35: Limited / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Takeovers Code” / the Codes on Takeovers and Mergers and Share Buy-backs
  - p115: Happiness / Cornerstone / Investment / Management Co., Ltd (馬鞍山幸福基石投資管理有限公司), the ultimate beneficial owner of which / is Mr. ZHANG Wei (張維), an Independent Third Party. As of the Latest Practicable Date, all four / limited partners of Anhui Cornerstone were Independent Third Parties, of which Anhui Sanzhong / Yichuang Industrial Development Fund Co., Ltd. (安徽三重一創產業發展基金股份有限公司), a

### col_BC
  - p22: Acting-in-Concert and Our Single Largest Group of Shareholders / As of the Latest Practicable Date, pursuant to a series of Concert Party Agreements, Dr. GU, / together with the Pre-Listing Concert Parties, are able to exercise approximately 40.30% of the / voting rights in the Company, and therefore constituted a group of controlling shareholders (as / defined in the Listing Rules) of the Company
  - p35: Limited / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Takeovers Code” / the Codes on Takeovers and Mergers and Share Buy-backs

### col_BD
  - p22: Acting-in-Concert and Our Single Largest Group of Shareholders / As of the Latest Practicable Date, pursuant to a series of Concert Party Agreements, Dr. GU, / together with the Pre-Listing Concert Parties, are able to exercise approximately 40.30% of the / voting rights in the Company, and therefore constituted a group of controlling shareholders (as / defined in the Listing Rules) of the Company
  - p22: Acting-in-Concert and Our Single Largest Group of Shareholders / As of the Latest Practicable Date, pursuant to a series of Concert Party Agreements, Dr. GU, / together with the Pre-Listing Concert Parties, are able to exercise approximately 40.30% of the / voting rights in the Company, and therefore constituted a group of controlling shareholders (as / defined in the Listing Rules) of the Company
  - p35: Limited / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Takeovers Code” / the Codes on Takeovers and Mergers and Share Buy-backs

### col_BE
  - p266: of our sales network and construction of our manufacturing facilities. / We expect to fund our future working capital and other cash requirements with cash generated / from our operations, the net proceeds from the Global Offering and, when necessary, bank and other / borrowings. As of January 31, 2026, the latest practicable date for determining our indebtedness, / we had cash and cash equivalent
  - p190: properties on these parcels of land with an aggregate GFA of approximately 13,110 square meters, / which are primarily used for production, R&D, warehouse and office purposes. We have obtained / certificates to all our owned land use rights and properties. As of the Latest Practicable Date, our / land use rights in Jiaxing and Anhui were mortgaged for interest-bearing bank borrowings. / As of the 
  - p49: respectively, and we had net current liabilities of RMB1,007.0 million, RMB1,134.4 million, / RMB1,179.9 million and RMB1,317.9 million, respectively, as of the same dates. A net liabilities / position and net current liabilities position could require us to seek financing from external sources / such as debt issuance and bank borrowings, which may not be available on terms favorably or / commerci

### col_BF
  - p22: in alternative technologies may adversely affect the competitiveness of our products and systems, / and our failure to anticipate or respond effectively to technological evolution could harm our / business; (iii) the growth of our business depends on our ability to successfully integrate and / improve technologies; (iv) the commercialization of our intelligent intralogistics robots and systems / m
  - p92: LiDAR        / 400-1,000 / • / Technology route (solid-state vs mechanical) and mass production / impact prices; / • / Demand growth and competition drive cost changes.
  - p99: PRC. Communication administrative bureaus at provincial levels shall conduct supervision and / administration of the domain name services within their respective administrative jurisdictions. / Domain name registration services shall, in principle, be subject to the principle of “first apply, first / register”. A domain name registrar shall, in the process of providing domain name registration / s

### col_BG
  - p24: For further details, please refer to “APPENDIX IIA — Unaudited Pro Forma Financial / Information — A. Unaudited Pro Forma Statement of Adjusted Consolidated Net Tangible Assets” / to this document. / USE OF PROCEEDS / We estimate that the net proceeds of the Global Offering, after deducting the estimated / underwriting commissions and other fees and expenses paid and payable by us in connection wi
  - p24: is crucial for establishing our international presence and capturing opportunities in key overseas / markets; and (e) approximately 10.0% of the net proceeds, or HK$61.8 million, will be used for / working capital and other general corporate purposes to support our daily operations and overall / business growth. For further details, see “Future Plans and Use of Proceeds.” / LISTING EXPENSES / The 

### col_BI
  - p2: Number of Offer Shares in the Global / Offering / : / 36,798,000 H Shares (subject to the Over- / allotment Option) / Number of Hong Kong Offer Shares / :

### col_BP
  - p1: Stock Code : 2729 / (a joint stock company incorporated in the People’s Republic of China with limited liability) / 浙江凱樂士科技集團股份有限公司 / Zhejiang Galaxis Technology Group Co., Ltd. / GLOBAL OFFERING

### col_BR
  - p77: Head Office, Registered Office / and Principal Place of Business / in the PRC / No. 1118, Chicheng Road / Daqiao Town, Nanhu District
  - p77: Head Office, Registered Office / and Principal Place of Business / in the PRC / No. 1118, Chicheng Road
  - p77: Head Office, Registered Office / and Principal Place of Business / in the PRC / No. 1118, Chicheng Road

### col_BT
  - p31: International Accounting Standards Board / “IFRS” / the International Financial Reporting Standards as issued by / the IASB, which comprise the IFRS Accounting Standards, / International / Accounting / Standards,
  - p31: laws of the PRC on January 16, 2009, and a wholly-owned / subsidiary of our Company / “IASB” / International Accounting Standards Board / “IFRS” / the International Financial Reporting Standards as issued by / the IASB, which comprise the IFRS Accounting Standards,
  - p223: MATERIAL ACCOUNTING POLICIES AND CRITICAL JUDGMENTS AND ESTIMATES / The preparation of historical financial information in conformity with IFRS Accounting / Standards requires management to make judgements, estimates and assumptions that affect the / application of policies and reported amounts of assets, liabilities, income and expenses. The

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, our Company will issue an announcement to be published on the website of the Stock / Exchange at www.hkexnews.hk and the website of our Company at www.galaxis-tech.com. / Date(1)
  - p5: Offering, our Company will issue an announcement to be published on the website of the Stock / Exchange at www.hkexnews.hk and the website of our Company at www.galaxis-tech.com. / Date(1) / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on Monday, / March 16, 2026 / Latest time to complete electronic applications under / White Form eIPO service th

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, our Company will issue an announcement to be published on the website of the Stock / Exchange at www.hkexnews.hk and the website of our Company at www.galaxis-tech.com. / Date(1)

### col_CE
  - p220: accordingly. / Listing Approval by the Stock Exchange / We have applied to the Listing Committee for the granting of listing of, and permission to deal / in, our H Shares to be issued pursuant to the Global Offering (including any H Shares which may / be issued pursuant to the exercise of the Over-allotment Option), the H Shares to be issued under / the Pre-IPO Share Option Schemes, and the H Shar
  - p4: Kong Offer Shares as set out in the table below. No application for any other number of Hong Kong / Offer Shares will be considered and such an application is liable to be rejected. / If you are applying through the White Form eIPO service, you may refer to the table below / for the amount payable for the number of H Shares you have selected. You must pay the respective / amount payable on applica

### col_CF
  - p16: (607,855) / (283,995) / (460,225) / Gross profit             / 103,428 / 91,667 / 113,562
  - p16: (607,855) / (283,995) / (460,225) / Gross profit             / 103,428 / 91,667 / 113,562

### col_CG
  - p49: available capital resources sooner than we currently expect. If we are unable to maintain adequate / working capital or obtain sufficient financings to meet our capital needs, we may be unable to / continue our operations according to our plan, default on our payment obligations and fail to meet / our capital expenditure requirements. / Failure to manage our inventory effectively could materially 
  - p49: available capital resources sooner than we currently expect. If we are unable to maintain adequate / working capital or obtain sufficient financings to meet our capital needs, we may be unable to / continue our operations according to our plan, default on our payment obligations and fail to meet / our capital expenditure requirements. / Failure to manage our inventory effectively could materially 
  - p272: indebtedness since January 31, 2026, being the latest practicable date for determining our / indebtedness, up to the Latest Practicable Date. / CAPITAL EXPENDITURES / During the Track Record Period, our payment for purchase of property, plant and equipment / and intangible assets amounted to RMB105.8 million, RMB22.4 million, RMB13.3 million and / RMB3.0 million for the years ended December 31, 20

### col_CH
  - p310: Opinion / In our opinion, the Historical Financial Information gives, for the purpose of the accountants’ / report, a true and fair view of the Company’s and the Group’s financial position as at December 31, / 2022, 2023 and 2024 and September 30, 2025 and of the Group’s financial performance and cash / flows for the Track Record Period in accordance with the basis of preparation and presentation 
  - p16: SUMMARY OF KEY FINANCIAL INFORMATION / The summary of the key financial information set forth below have been derived from and / should be read in conjunction with our consolidated financial statements, including the / accompanying notes, set forth in the Accountants’ Report in Appendix I to this document, as well / as the information set forth in the section headed “Financial Information.” / Summ

### col_CI
  - p17: Non-IFRS Measures / We define adjusted net loss (non-IFRS measure) as net loss for the year/period adjusted by / adding back equity settled share-based payment expenses, changes in the carrying amount of the / redemption liability and listing expenses. / To supplement our consolidated financial statements, we also use adjusted net loss (non-IFRS / measure) as additional financial measure, which is
  - p17: Non-IFRS Measures / We define adjusted net loss (non-IFRS measure) as net loss for the year/period adjusted by / adding back equity settled share-based payment expenses, changes in the carrying amount of the / redemption liability and listing expenses. / To supplement our consolidated financial statements, we also use adjusted net loss (non-IFRS / measure) as additional financial measure, which is
  - p288: Offering to cover over-allocations in the International Offering, if any. For more details of the / arrangements relating to the Over-allotment Option and stabilization, see “Structure of the Global / Offering” in this prospectus. / UNDERWRITING COMMISSIONS AND LISTING EXPENSES / The Underwriters and the Capital Market Intermediaries will receive an underwriting / commission equal to 2.0% of the a


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 2729.HK`
有 ERROR 必须回原文修正。
