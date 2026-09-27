# 2701.HK 扩展 18 列抽取包

公司：2701.HK Nsing Technologies Inc. - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB2701.json`。
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
- 股本结构（**已确认，不要改**）：L=678126700 M=95000000 N=583126700 O=583126700 P=0 Q=95000000 R=85500000 S=9500000
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = -100994666.66666667
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
{"code":"2701.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  2701.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 2701.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p109: Based on the independent due diligence conducted by the Sole Sponsor, nothing has come to / the Sole Sponsor’s attention that would cause it to disagree with the Directors’ confirmation with / regard to the compliance records of the Company on the Shenzhen Stock Exchange. / We have no pre-IPO investors for the purpose of the Global Offering. / OUR SINGLE LARGEST SHAREHOLDER / Mr. Sun is our Chairm

### col_BB
  - p107: by way of capitalization of capital reserve. Immediately following the issue of bonus shares and / capital reserves capitalization, our issued share capital was increased to RMB272,000,000 divided / into 272,000,000 A Shares with nominal value of RMB1.0 each, which was fully paid. / 2013 Exit of China Huada as a then controlling shareholder / In November 2013, China Huada, the then controlling sha
  - p36: “substantial shareholder(s)” / has the meaning ascribed to it under the Listing Rules / “Takeovers Code” / the Code on Takeovers and Mergers issued by the SFC, as
  - p271: under the SFO in Hong Kong by the SFC. HGCI is principally engaged in asset management and / investment advisory business focusing on investments in the technology and artificial intelligence / sectors. Chen Di, an Independent Third Party, is the beneficial owner who holds the largest portion / of the ultimate beneficial ownership of HGCI. Save for Chen Di, there is no single shareholder / holding

### col_BC
  - p107: by way of capitalization of capital reserve. Immediately following the issue of bonus shares and / capital reserves capitalization, our issued share capital was increased to RMB272,000,000 divided / into 272,000,000 A Shares with nominal value of RMB1.0 each, which was fully paid. / 2013 Exit of China Huada as a then controlling shareholder / In November 2013, China Huada, the then controlling sha
  - p36: “substantial shareholder(s)” / has the meaning ascribed to it under the Listing Rules / “Takeovers Code” / the Code on Takeovers and Mergers issued by the SFC, as

### col_BD
  - p107: by way of capitalization of capital reserve. Immediately following the issue of bonus shares and / capital reserves capitalization, our issued share capital was increased to RMB272,000,000 divided / into 272,000,000 A Shares with nominal value of RMB1.0 each, which was fully paid. / 2013 Exit of China Huada as a then controlling shareholder / In November 2013, China Huada, the then controlling sha
  - p72: We have applied to the Stock Exchange for, and the Stock Exchange has granted, a waiver / from strict compliance with the requirements under Rule 10.04 and consent under Paragraph 1C(2) / of Appendix F1 to the Listing Rules to permit H Shares in the International Offering to be placed / to certain existing minority Shareholders who (i) hold less than 5% of the voting rights of our / Company prior 
  - p36: “substantial shareholder(s)” / has the meaning ascribed to it under the Listing Rules / “Takeovers Code” / the Code on Takeovers and Mergers issued by the SFC, as

### col_BE
  - p225: INDEBTEDNESS / Our indebtedness primarily consist of (i) repurchase obligation for restricted shares relating / to Share Incentive Scheme of the Company, (ii) repurchase obligation for non-controlling interests / owed to a non-controlling shareholder of Inner Mongolia Sinuo, (iii) borrowings, and (iv) lease
  - p269: above proposed use of proceeds. / To the extent that the net proceeds of the Global Offering are not immediately used for the / purposes described above, and to the extent permitted by the relevant laws and regulations, we / intend to deposit the proceeds in short-term interest-bearing accounts at licensed commercial banks / and/or other authorized financial institutions (as defined under SFO or a
  - p147: 2031 / 2031 / We intend to fund the above R&D initiatives by using net proceeds of the Global Offering as / well as cash generated from operations, bank loans and other borrowings, as necessary. / We believe that we will be able to capture the market demand because our design and R&D / are carried out as a project group effort in close collaboration between our different teams. The Our / sales and

### col_BF
  - p122: emerging fields such as AI, robotics, new energy, and the low-altitude economy, achieving / continuous growth in both business structure and revenue scale. Beyond the Chairman, our core / management team consists of senior executives with many years of experience in the integrated / circuit and new energy materials industries. They possess extensive commercialization experience / and strong market
  - p96: Comprehensive product portfolio enhances customer retention: Platform-based / providers typically provide full product series ranging from entry-level to high- / performance MCUs. They can meet customer needs across development stages — from / prototyping to mass production and from simple control to edge intelligence — thereby / increasing customer retention and enabling horizontal growth. / • / 
  - p159: See “Financial Information — Discussion of Certain Items of Statements of Financial Position — / Inventories.” In order to maintain our competitiveness, adapt our products to evolving demand / trends and to avoid our inventories becoming obsolete, we have taken measures to optimize our / inventory level, including minimizing inventory backlog in the process of inventory management. / In addition, 

### col_BG
  - p24: overseas financing platform to enhance our international profile, enhance our market recognition, / attract equity investment through a recognized international stock exchange, and ultimately to / maximize Shareholder value and support our capital structure optimization. See “Future Plans and / Use of Proceeds” and “Business” for further details. / Since January 1, 2023 and up to the Latest Practi
  - p224: million partially offset by proceeds from borrowings raised of RMB818.5 million. / In 2024, our net cash used in financing activities was RMB96.6 million, primarily due to (i) / the repurchase of the Company’s shares of RMB71.5 million, (ii) interest paid of RMB70.8 million, / (iii) repayment of bank borrowings of RMB834.3 million; partially offset by the proceeds from / borrowings raised of RMB89
  - p25: and regulatory restrictions, and other factors which our Directors consider relevant. Distribution of / dividends will be decided by our Board at their discretion and will be subject to Shareholders’ / approval. See “Financial Information — Dividends.” / FUTURE PLANS AND USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$943.9 million, as

### col_BI
  - p2: Number of Offer Shares under / the Global Offering / : / 95,000,000 H Shares / Number of Hong Kong Offer Shares / : / 9,500,000 H Shares (subject to

### col_BP
  - p106: operating subsidiaries within the two years immediately preceding the date of this prospectus. / MAJOR SHAREHOLDING CHANGES OF OUR COMPANY / Establishment and early development of our Company / Our Company was established on March 20, 2000, with an initial registered capital of RMB30 / million and was owned as to 60% by ZTE Corporation (中興通訊股份有限公司) and 40% by SDIC / Electronics Co., Ltd. (國投電子公司) 
  - p1: Stock Code : 2701 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / GLOBAL OFFERING / 國民技術股份有限公司 / NSING TECHNOLOGIES INC.

### col_BR
  - p86: Nanshan District, Shenzhen / Guangdong Province / PRC / Principal place of business in Hong Kong / Room 1918, 19/F / Lee Garden One / 33 Hysan Avenue
  - p86: Registered office / 1/F, Nsing Tower / No. 109 Baoshen Road / Songpingshan Community

### col_BT
  - p16: should be read in conjunction with, our audited financial statements, including the accompanying / notes, set forth in the Accountants’ Report attached as Appendix I to this prospectus, as well as the / information set forth in “Financial Information.” Our financial information was prepared in / accordance with IFRS Accounting Standards. / Description of Major Components of Our Results of Operatio
  - p373: Certified Public Accountants LLP (中興財光華會計師事務所(特殊普通合夥)) while the statutory financial statements of Hubei Sinuo for the years ended 31 December 2023 and 2024 / were audited by Wuhan Wanli Certified Public Accountants Limited (武漢市萬里會計師事務有限公司), respectively. / (c) / The statutory financial statements of Nsing HK for the years ended 31 December 2022, 2023 and 2024 were prepared in accordance with HKFR
  - p16: should be read in conjunction with, our audited financial statements, including the accompanying / notes, set forth in the Accountants’ Report attached as Appendix I to this prospectus, as well as the / information set forth in “Financial Information.” Our financial information was prepared in / accordance with IFRS Accounting Standards. / Description of Major Components of Our Results of Operatio

### col_CC
  - p5: If there is any change to the expected timetable of the Hong Kong Public Offering, we / will issue an announcement to be published on the website of the Hong Kong Stock Exchange / at www.hkexnews.hk and our website at www.nsingtech.com. / Hong Kong Public Offering commences
  - p5: If there is any change to the expected timetable of the Hong Kong Public Offering, we / will issue an announcement to be published on the website of the Hong Kong Stock Exchange / at www.hkexnews.hk and our website at www.nsingtech.com. / Hong Kong Public Offering commences / . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9:00 a.m. on / Friday, March 13, 2026 / Latest time to comple

### col_CD
  - p5: If there is any change to the expected timetable of the Hong Kong Public Offering, we / will issue an announcement to be published on the website of the Hong Kong Stock Exchange / at www.hkexnews.hk and our website at www.nsingtech.com. / Hong Kong Public Offering commences

### col_CE
  - p79: APPLICATION FOR LISTING OF THE H SHARES ON THE HONG KONG STOCK / EXCHANGE / We have applied to the Hong Kong Stock Exchange for the granting of listing of, and / permission to deal in, our H Shares to be issued pursuant to the Global Offering. / We / have / applied
  - p235: shareholders’ general meeting of our Company held on June 16, 2025 and is subject to the following / conditions: / (i) / Size of the offer. The proposed number of H Shares to be offered shall not exceed 20% / of the total issued share capital enlarged by the H Shares to be issued pursuant to the / Global Offering. / (ii)

### col_CF
  - p16: (0.6) / (4,910) / (0.5) / Gross profit       / 426,020 / 35.6 / 18,011
  - p16: (0.6) / (4,910) / (0.5) / Gross profit       / 426,020 / 35.6 / 18,011

### col_CG
  - p61: we will not record net current liabilities in the future. If we record net current liabilities, our / working capital for business operations may be constrained. If we fail to generate sufficient revenue / from our operations or if we fail to maintain sufficient cash and financing resources, we may not / have sufficient cash flows to fund our business operations and capital expenditure, and our bu
  - p61: we will not record net current liabilities in the future. If we record net current liabilities, our / working capital for business operations may be constrained. If we fail to generate sufficient revenue / from our operations or if we fail to maintain sufficient cash and financing resources, we may not / have sufficient cash flows to fund our business operations and capital expenditure, and our bu
  - p390: Cash and cash equivalents / Our cash and cash equivalents were mainly denominated in Renminbi. Our cash and cash equivalents decreased from / RMB361.7 million as of December 31, 2024 to RMB197.5 million as of December 31, 2025, primarily due to our cash used / in purchase of property, plant and equipment and intangible assets in 2025. / Trade and Bill Receivables at Amortized Cost and FVTOCI / Our

### col_CH
  - p304: We believe that the evidence we have obtained is sufficient and appropriate to provide a basis / for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the accountants’ / report, a true and fair view of the Group’s financial position as at 31 December 2022, 2023 and 2024 / and 30 September 2025, of the Company’s financial position as at 31 Dece
  - p16: SUMMARY OF KEY FINANCIAL INFORMATION / The summary historical financial information set forth below have been derived from, and / should be read in conjunction with, our audited financial statements, including the accompanying / notes, set forth in the Accountants’ Report attached as Appendix I to this prospectus, as well as the / information set forth in “Financial Information.” Our financial inf

### col_CI
  - p26: approximately 10.0% of the net proceeds, or HK$94.4 million, will be used for working / capital and other general corporate purposes. / See “Future Plans and Use of Proceeds.” / LISTING EXPENSES / The total estimated listing expenses in relation to the Global Offering are RMB72.4 million / (HK$82.0 million), which constitute approximately 8.0% of the gross proceeds. The listing / expenses we incur
  - p26: approximately 10.0% of the net proceeds, or HK$94.4 million, will be used for working / capital and other general corporate purposes. / See “Future Plans and Use of Proceeds.” / LISTING EXPENSES / The total estimated listing expenses in relation to the Global Offering are RMB72.4 million / (HK$82.0 million), which constitute approximately 8.0% of the gross proceeds. The listing / expenses we incur


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 2701.HK`
有 ERROR 必须回原文修正。
