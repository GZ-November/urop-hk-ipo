# 0470.HK 扩展 18 列抽取包

公司：0470.HK WUXI LEAD INTELLIGENT EQUIPMENT CO., LTD. - H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB0470.json`。
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
- 股本结构（**已确认，不要改**）：L=1659779034 M=93616000 N=1566163034 O=1566163034 P=0 Q=93616000 R=84254400 S=9361600
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = 1548393333.3333333
- 行业分类（港交所官方）：101020 工業零件及器材
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
{"code":"0470.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  0470.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 0470.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
（锚点无命中，需要自己 search）

### col_BB
  - p36: conducted by the Joint Sponsors, nothing has come to the Joint Sponsors’ attention that would / cause them to disagree with our Directors’ confirmation with regard to the compliance records / of the Company on the Shenzhen Stock Exchange. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, our Company was held as to (i) approximately 21.46% / by Lhasa Xindao, which was in turn held
  - p38: Mr. Wang, Ms. Ni, Lhasa Xindao, Wuxi Yuxi, Wuxi / Luojie, Wuxi Zhipu, Shanghai Zhuoao, Shanghai Yiwei, / Shanghai Haochang and Shanghai Haoling, collectively / the substantial shareholders of our Company; prior to the / Listing and as of the date of this Prospectus, Mr. Wang, / Ms. Ni, Lhasa Xindao, Wuxi Yuxi, Wuxi Luojie, Wuxi / Zhipu, Shanghai Zhuoao, Shanghai Yiwei, Shanghai
  - p355: SFO) by the SFC. It is directly held by Pinpoint Capital Management Group as to 100%, and / is ultimately held as to 84.1% by Mr. Wang Qiang, and as to 15.9% by Ms. Bao Jiarong. Apart / from Mr. Wang Qiang who holds 30% or more of Pinpoint China Fund and Pinpoint / Multi-Strategy Master Fund, no other ultimate beneficial owner holds 30% or more interest in / Pinpoint China Fund and Pinpoint Multi 

### col_BC
  - p36: conducted by the Joint Sponsors, nothing has come to the Joint Sponsors’ attention that would / cause them to disagree with our Directors’ confirmation with regard to the compliance records / of the Company on the Shenzhen Stock Exchange. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, our Company was held as to (i) approximately 21.46% / by Lhasa Xindao, which was in turn held
  - p38: Mr. Wang, Ms. Ni, Lhasa Xindao, Wuxi Yuxi, Wuxi / Luojie, Wuxi Zhipu, Shanghai Zhuoao, Shanghai Yiwei, / Shanghai Haochang and Shanghai Haoling, collectively / the substantial shareholders of our Company; prior to the / Listing and as of the date of this Prospectus, Mr. Wang, / Ms. Ni, Lhasa Xindao, Wuxi Yuxi, Wuxi Luojie, Wuxi / Zhipu, Shanghai Zhuoao, Shanghai Yiwei, Shanghai

### col_BD
  - p36: conducted by the Joint Sponsors, nothing has come to the Joint Sponsors’ attention that would / cause them to disagree with our Directors’ confirmation with regard to the compliance records / of the Company on the Shenzhen Stock Exchange. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, our Company was held as to (i) approximately 21.46% / by Lhasa Xindao, which was in turn held
  - p38: Ms. Ni, Lhasa Xindao, Wuxi Yuxi, Wuxi Luojie, Wuxi / Zhipu, Shanghai Zhuoao, Shanghai Yiwei, Shanghai / Haochang and Shanghai Haoling controlled more than / 30% of the total voting rights in our Company, and upon / Listing, Mr. Wang, Ms. Ni, Lhasa Xindao, Wuxi Yuxi, / Wuxi Luojie, Wuxi Zhipu, Shanghai Zhuoao, Shanghai / Yiwei, Shanghai Haochang and Shanghai Haoling will
  - p38: Mr. Wang, Ms. Ni, Lhasa Xindao, Wuxi Yuxi, Wuxi / Luojie, Wuxi Zhipu, Shanghai Zhuoao, Shanghai Yiwei, / Shanghai Haochang and Shanghai Haoling, collectively / the substantial shareholders of our Company; prior to the / Listing and as of the date of this Prospectus, Mr. Wang, / Ms. Ni, Lhasa Xindao, Wuxi Yuxi, Wuxi Luojie, Wuxi / Zhipu, Shanghai Zhuoao, Shanghai Yiwei, Shanghai

### col_BE
  - p83: We may incur substantial additional indebtedness and increased cost of indebtedness in / the future, could materially and adversely affect our business, results of operations and / liquidity. / During the Track Record Period, we had certain borrowings to finance our business
  - p363: basis. / For the net proceeds of the Global Offering which are not immediately used in accordance / with the purposes described above, we will only deposit such proceeds into short-term / interest-bearing accounts at licensed commercial banks and/or other authorized financial / institutions (as defined under the Securities and Futures Ordinance or the applicable laws and / regulations in other jur
  - p26: Our net current assets increased to RMB8,907.1 million as of December 31, 2024, from / RMB7,700.1 million as of December 31, 2023, primarily due to (i) a decrease of RMB1,905.2 / million in bills, trade and other payables and (ii) a decrease of RMB975.8 million in contract / liabilities, partially offset by (i) an increase of RMB1,602.1 million in borrowings and (ii) a / decrease of RMB514.8 milli

### col_BF
  - p76: products may infringe. If third parties successfully assert their intellectual property rights / against us, we might be barred from using certain aspects of our technology or barred from / developing and commercializing certain products, or we may be required to pay burdensome / royalties to license their products. If we are unsuccessful in defending against allegations that / we have infringed, 
  - p175: and drive the implementation and industrialization of cutting-edge downstream technologies. / • / In the field of solid-state batteries, we have successfully consolidated all process / stages for mass production. We delivered the world’s first automotive-grade, / all-solid-state battery turnkey solution and have been progressively delivering / standalone key equipment for solid-state battery produ
  - p218: process and purchase customary insurance. We also regularly evaluate logistics service / providers by grading them as per their qualifications and historical performance to update our / service provider list. / We are also in the process of developing an internal logistics system to establish efficient / and integrated logistics arrangements, which will further reduce transportation costs and / en

### col_BG
  - p32: expensed in our consolidated statements of profit or loss. The listing expenses above are the / latest practicable estimate for reference only, and the actual amount may differ from this / estimate. / FUTURE PLANS AND USE OF PROCEEDS / We estimate that we will receive net proceeds of approximately HK$4,166.1 million from / the Global Offering after deducting the underwriting commissions, fees and 
  - p32: expensed in our consolidated statements of profit or loss. The listing expenses above are the / latest practicable estimate for reference only, and the actual amount may differ from this / estimate. / FUTURE PLANS AND USE OF PROCEEDS / We estimate that we will receive net proceeds of approximately HK$4,166.1 million from / the Global Offering after deducting the underwriting commissions, fees and 

### col_BI
  - p2: Number of Offer Shares under the / Global Offering / : / 93,616,000 H Shares (subject to the / Offer Size Adjustment Option and the / Over-allotment Option) / Number of Hong Kong Offer Shares

### col_BP
  - p40: “Guangdong Beidao” / Guangdong Beidao Intelligent Technology Co., Ltd. (廣 / 東貝導智能科技有限公司), a PRC subsidiary of ours / established on December 17, 2020 / “Guide for New Listing / Applicants” / the Guide for New Listing Applicants, as published by
  - p1: Joint Bookrunners and Joint Lead Managers / GLOBAL / OFFERING / (A joint stock company incorporated in the People’s Republic of China with limited liability) / Stock Code: 0 4 7 0 / (in alphabetical order) / 無錫先導智能裝備股份有限公司

### col_BR
  - p119: Xinwu District, Wuxi City / Jiangsu Province / PRC / Principal Place of Business in Hong Kong / 46/F, Hopewell Centre / 183 Queen’s Road East / Wanchai
  - p119: Registered Office / No. 20 Xinxi Road / Xinwu District, Wuxi City / Jiangsu Province

### col_BT
  - p18: and is qualified in its entirety by reference to, our financial statements in this prospectus, / including the related notes. Our consolidated financial information was prepared in accordance / with the IFRS Accounting Standards. / Summary of Consolidated Statements of Profit or Loss / The following table sets out a summary of our consolidated statements of profit or loss / for the years/periods i
  - p18: and is qualified in its entirety by reference to, our financial statements in this prospectus, / including the related notes. Our consolidated financial information was prepared in accordance / with the IFRS Accounting Standards. / Summary of Consolidated Statements of Profit or Loss / The following table sets out a summary of our consolidated statements of profit or loss / for the years/periods i
  - p287: The preparation of the historical financial information in conformity with IFRS requires / the use of certain critical accounting estimates. It also requires management to exercise its / judgment in the process of applying our accounting policies. The areas involving a higher / degree of judgment or complexity, or areas where assumptions and estimates are significant to / the historical financial 

### col_CC
  - p5: If there is any change to the expected timetable of the Hong Kong Public Offering, / we will issue an announcement to be published on the website of the Hong Kong Stock / Exchange at www.hkexnews.hk and our website at https://www.leadintelligent.com. / Hong Kong Public Offering commences
  - p5: If there is any change to the expected timetable of the Hong Kong Public Offering, / we will issue an announcement to be published on the website of the Hong Kong Stock / Exchange at www.hkexnews.hk and our website at https://www.leadintelligent.com. / Hong Kong Public Offering commences / . . . . . . . . . . . . . . . . . . . . . . 9:00 a.m. on Tuesday, / February 3, 2026 / Latest time to complet

### col_CD
  - p5: If there is any change to the expected timetable of the Hong Kong Public Offering, / we will issue an announcement to be published on the website of the Hong Kong Stock / Exchange at www.hkexnews.hk and our website at https://www.leadintelligent.com. / Hong Kong Public Offering commences

### col_CE
  - p113: APPLICATION FOR LISTING OF THE H SHARES ON THE HONG KONG STOCK / EXCHANGE / We have applied to the Hong Kong Stock Exchange for the granting of listing of, and / permission to deal in, our H Shares to be issued pursuant to the Global Offering (including any / H Shares which may be issued pursuant to the exercise of the Offer Size Adjustment Option / and the Over-allotment Option). Dealings in the 
  - p284: by us at the shareholders’ general meeting of our Company held on February 14, 2025 and is / subject to the following conditions: / (i) / Size of the offer. The proposed number of H Shares to be offered shall not exceed / 10% of the total issued share capital enlarged by the H Shares to be issued pursuant / to the Global Offering (before the exercise of the Over-allotment Option). The / number of 

### col_CF
  - p18: (8,236) (70.0) / (5,866) (64.9) / (7,183) (69.1) / Gross profit            / 5,065 / 36.6 / 5,393
  - p18: (8,236) (70.0) / (5,866) (64.9) / (7,183) (69.1) / Gross profit            / 5,065 / 36.6 / 5,393

### col_CG
  - p54: • / our business operations and prospects; / • / our capital expenditure plans; / • / weather, natural disasters and climate change; / •
  - p54: • / our business operations and prospects; / • / our capital expenditure plans; / • / weather, natural disasters and climate change; / •
  - p344: Net Cash (Used in)/Generated from Investing activities / In the nine months ended September 30, 2025, we had net cash used in investing activities / of RMB1,096.7 million, primarily attributable to (i) purchases of financial assets at FVTPL of / RMB8,185.0 million and (ii) purchase of property, plant and equipment of RMB374.8 million, / partially offset by redemptions of financial assets at FVTPL 

### col_CH
  - p412: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the / accountants’ report, a true and fair view of the Group’s financial position as at December 31, / 2022, 2023 and 2024 and September 30, 2025, of the Company’s financial position as at / Dec
  - p17: respond successfully to changes in the competitive landscape.” / SUMMARY OF HISTORICAL FINANCIAL INFORMATION / The following tables set forth summary financial data from our financial information / during the Track Record Period, extracted from the Accountants’ Report as set out in Appendix / I to this prospectus. The summary financial data set forth below should be read together with, / SUMMARY /

### col_CI
  - p18: (9.5) / (883) / (8.5) / Listing expenses         / – / – / –
  - p18: (9.5) / (883) / (8.5) / Listing expenses         / – / – / –


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 0470.HK`
有 ERROR 必须回原文修正。
