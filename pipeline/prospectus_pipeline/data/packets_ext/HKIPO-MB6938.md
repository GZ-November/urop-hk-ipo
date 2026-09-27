# 6938.HK 扩展 18 列抽取包

公司：6938.HK Suzhou Ribo Life Science Co., Ltd. - B - H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB6938.json`。
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
- 股本结构（**已确认，不要改**）：L=161690510 M=27487400 N=134203110 O=134203110 P=0 Q=27487400 R=24738600 S=2748800
- 财务期间（**已确认**）：year-1 期末 = 30/06/2025；币种 = RMB；year-1 净利 = -195530000
- 行业分类（港交所官方）：281020 生物技術
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
{"code":"6938.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  6938.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 6938.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p30: issued under the Pre-IPO Share Option Scheme). Based on the above, upon Listing, the Concert / Parties will be our Single Largest Group of Shareholders. For details, see “Relationship with / Our Single Largest Group of Shareholders.” / PRE-IPO INVESTMENTS / Since the establishment of our Group, we have attracted certain Pre-IPO Investors to raise / funds for fueling the development of our business
  - p30: Parties will be our Single Largest Group of Shareholders. For details, see “Relationship with / Our Single Largest Group of Shareholders.” / PRE-IPO INVESTMENTS / Since the establishment of our Group, we have attracted certain Pre-IPO Investors to raise / funds for fueling the development of our business. Our Pre-IPO Investors include certain / Sophisticated Investors, such as Future Industry Inve
  - p30: issued under the Pre-IPO Share Option Scheme). Based on the above, upon Listing, the Concert / Parties will be our Single Largest Group of Shareholders. For details, see “Relationship with / Our Single Largest Group of Shareholders.” / PRE-IPO INVESTMENTS / Since the establishment of our Group, we have attracted certain Pre-IPO Investors to raise / funds for fueling the development of our business

### col_BB
  - p25: in 2024, partially offset by issue of shares of RMB45.8 million primarily in connection with / our series E2 financing. Our financial position transitioned from net liabilities to net assets / between December 31, 2024 and June 30, 2025, primarily due to capital contribution from / non-controlling shareholders of RMB236.4 million primarily in relation to Ribocure AB’s / equity financing, partially
  - p48: strategy committee of the Board / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / DEFINITIONS / – 38 –
  - p256: Commission of the State Council of the PRC (國務院國有資產 / 監督管理委員會). To the best of the Company’s knowledge, / information and belief, having made all reasonable enquiries, / China Resources Enterprise and its ultimate beneficial owner / are Independent Third Parties. / Note: Due to internal arrangements of China Resources Company Limited, on May 13, 2020, CR Life Science / transferred all equity inter

### col_BC
  - p25: in 2024, partially offset by issue of shares of RMB45.8 million primarily in connection with / our series E2 financing. Our financial position transitioned from net liabilities to net assets / between December 31, 2024 and June 30, 2025, primarily due to capital contribution from / non-controlling shareholders of RMB236.4 million primarily in relation to Ribocure AB’s / equity financing, partially
  - p48: strategy committee of the Board / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / DEFINITIONS / – 38 –

### col_BD
  - p25: in 2024, partially offset by issue of shares of RMB45.8 million primarily in connection with / our series E2 financing. Our financial position transitioned from net liabilities to net assets / between December 31, 2024 and June 30, 2025, primarily due to capital contribution from / non-controlling shareholders of RMB236.4 million primarily in relation to Ribocure AB’s / equity financing, partially
  - p30: Party under the Concert Party Arrangement, even though Kunshan Ruixing did not enter into / any acting-in-concert undertaking or agreement with the other Concert Parties. For details, see / “History and Corporate Structure — Acting-in-Concert”. / As such, the Concert Parties were collectively entitled to exercise voting rights attaching / to approximately 29.91% of the total issued Shares of our C
  - p48: strategy committee of the Board / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / DEFINITIONS / – 38 –

### col_BE
  - p110: • / increased operating expenses and cash requirements; / • / the assumption of additional indebtedness or contingent liabilities; / • / the issuance of our equity securities; / •
  - p24: – / 67,124 / 67,124 / Interest-bearing bank and other borrowings   / 217,284 / 226,612 / 336,116
  - p24: – / 67,124 / 67,124 / Interest-bearing bank and other borrowings   / 217,284 / 226,612 / 336,116

### col_BF
  - p12: N/A / Notes: / * / Key jurisdictions in which the drug candidates are being developed and/or planned to be commercialized. Preclinical assets are not yet assigned specific jurisdictions and are / instead marked “N/A” given their early development stage. / 1. / In December 2023, we granted Qilu Pharmaceutical Co., Ltd. (“Qilu Pharmaceutical”) exclusive rights to develop, manufacture, and commercial
  - p137: provided by Frost & Sullivan. Unless otherwise indicated, the information has not been / verified by us independently. This statistical information may not be consistent with other / statistical information from other sources within or outside the PRC. While reasonable caution / has been made in the process of reproducing the data and statistics extracted from such official / government publicatio

### col_BG
  - p32: tangible assets attributable to owners of our Company per Share is HK$9.32 after adjustments of the Pre-IPO / investments from series E3 financing and on the basis that 161,690,510 Shares are in issue assuming the Global / Offering had been completed on June 30, 2025. / USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$1,473.6 million, a
  - p388: compliance adviser to provide advice to our Directors and management team until / the end of the first fiscal year after the Listing regarding matters relating to the / Listing Rules. Our compliance adviser is expected to ensure our use of funding / complies with the section headed “Future Plans and Use of Proceeds” in this / prospectus after the Listing, as well as to provide support and advice r

### col_BI
  - p2: Number of Offer Shares in / the Global Offering / : / 27,487,400 H Shares (subject to the Offer / Size Adjustment Option and the / Over-allotment Option) / Number of Hong Kong Offer Shares

### col_BP
  - p19: To date, our manufacturing activities are primarily limited to supporting our drug / development process. We also engaged industry-recognized CDMOs to supplement our / in-house capacity so as to enhance efficiency and reduce operational costs. / We have established one cGMP-compliant manufacturing facility in Kunshan, Jiangsu / province, China, and adhere to the requirements under the cGMP standar
  - p2: IMPORTANT: If you are in any doubt about any of the contents of this prospectus, you should obtain independent professional advice. / Suzhou Ribo Life Science Co., Ltd. / 蘇州瑞博生物技術股份有限公司 / (a joint stock company incorporated in the People’s Republic of China with limited liability) / GLOBAL OFFERING / Number of Offer Shares in / the Global Offering

### col_BR
  - p148: Head Office, Registered Office and / Principal Place of Business in the PRC / No. 168 Yuanfeng Road / Yushan Town / Kunshan City
  - p148: Head Office, Registered Office and / Principal Place of Business in the PRC / No. 168 Yuanfeng Road / Yushan Town
  - p148: Head Office, Registered Office and / Principal Place of Business in the PRC / No. 168 Yuanfeng Road / Yushan Town

### col_BT
  - p554: ACCOUNTING POLICIES / 2.1 / Basis of Preparation / The Historical Financial Information has been prepared in accordance with IFRS Accounting Standards, which / comprise all standards and interpretations approved by the International Accounting Standards Board (“IASB”). All / IFRS Accounting Standards effective for the accounting period commencing from 1 January 2024, together with the / relevant t
  - p41: headed “Underwriting — Hong Kong Public Offering — / Hong Kong Underwriting Agreement” in this prospectus / “IASB” / International Accounting Standards Board / “IFRS” / the International Financial Reporting Standards as issued / by the IASB, which comprise the IFRS Accounting
  - p436: on historical experience and various other factors, including expectations of future events, that / are believed to be reasonable under the circumstances, from which our actual results may / differ. / Set out below are material accounting policies, judgements and estimates which we / believe are most important for understanding our results of operations and financial condition. / See notes 2.3 and

### col_CC
  - p5: at www.ribolia.com(5) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .no later than / 11:00 p.m. on / Thursday, January 8, 2026 / EXPECTED TIMETABLE(1) / – iv –
  - p5: timetable of the Hong Kong Public Offering, an announcement will be made and / published on the website of the Stock Exchange at www.hkexnews.hk and our website at / www.ribolia.com of the revised timetable. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on / Wednesday, December 31, 2025 / Latest time for completing electronic applicati

### col_CD
  - p5: at www.ribolia.com(5) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .no later than / 11:00 p.m. on / Thursday, January 8, 2026 / EXPECTED TIMETABLE(1) / – iv –

### col_CE
  - p134: of our Directors, Supervisors or existing Shareholders or a nominee of any of the foregoing. / APPLICATION FOR LISTING OF THE H SHARES ON THE STOCK EXCHANGE / We have applied to the Stock Exchange for the listing of, and permission to deal in, the / H Shares to be issued pursuant to the Global Offering (including (i) any H Shares which may / be issued pursuant to the exercise of the Offer Size Adj
  - p263: Upon Listing, our Company will satisfy the public float requirement under Rule / 19A.13A(1) of the Listing Rules, which states that, in the event the expected market value of / the Company’s H Shares upon Listing is over HK$6 billion but does not exceed HK$30 billion, / the minimum number of H shares held by the public at the time of Listing as a percentage of / the total issued Shares of the Comp

### col_CF
  - p22: (11,903) / (2,110) / (6,591) / Gross Profit               / 20 / 130,724 / 64,195
  - p22: (11,903) / (2,110) / (6,591) / Gross Profit               / 20 / 130,724 / 64,195

### col_CG
  - p27: During the Track Record Period, we funded our operations primarily through equity and / debt financing, as well as revenue from our licensing and collaboration arrangements. We / expect to continue to require significant funding for our R&D activities and daily operations / going forward. We plan to fund our business operation and capital expenditure with our / existing cash and bank balances, inc
  - p27: During the Track Record Period, we funded our operations primarily through equity and / debt financing, as well as revenue from our licensing and collaboration arrangements. We / expect to continue to require significant funding for our R&D activities and daily operations / going forward. We plan to fund our business operation and capital expenditure with our / existing cash and bank balances, inc
  - p454: product. / Other Non-current Assets / During the Track Record Period, our other non-current assets consisted of prepayment for / purchase of property, plant and equipment and non-current portion of recoverable withholding / tax. Our other non-current assets increased from RMB723.0 thousand as of December 31, 2023 / to RMB12.2 million as of December 31, 2024 primarily because we had recoverable / w

### col_CH
  - p538: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the / accountants’ report, a true and fair view of the financial position of the Group and the Company / as at 31 December 2023 and 2024 and 30 June 2025 and of the financial performance and cas
  - p21: SUMMARY OF KEY FINANCIAL INFORMATION / The summary of the key financial information set forth below have been derived from and / should be read in conjunction with our consolidated financial statements, including the / accompanying notes, set forth in the Accountants’ Report in Appendix I to this prospectus, as / well as the information set forth in the section headed “Financial Information.” / SU

### col_CI
  - p33: technology platforms; and (vi) approximately 8.1%, or HK$119.5 million, will be used for / working capital and other general corporate purposes. For further details, see “Future Plans and / Use of Proceeds.” / LISTING EXPENSES / Listing expenses to be borne by us are estimated to be approximately HK$119.9 million / (based on an Offer Price of HK$57.97 per Share), representing approximately 7.5% of
  - p33: technology platforms; and (vi) approximately 8.1%, or HK$119.5 million, will be used for / working capital and other general corporate purposes. For further details, see “Future Plans and / Use of Proceeds.” / LISTING EXPENSES / Listing expenses to be borne by us are estimated to be approximately HK$119.9 million / (based on an Offer Price of HK$57.97 per Share), representing approximately 7.5% of


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 6938.HK`
有 ERROR 必须回原文修正。
