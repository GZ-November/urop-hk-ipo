# 1021.HK 扩展 18 列抽取包

公司：1021.HK Guangdong Huayan Robotics Co., Ltd. - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB1021.json`。
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
- 股本结构（**已确认，不要改**）：L=531479980 M=80785000 N=450694980 O=450694980 P=0 Q=80785000 R=76745600 S=4039400
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = -20784000.0
- 行业分类（港交所官方）：701030 機器人系統及解決方案
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
{"code":"1021.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  1021.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 1021.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p17: Over-allotment Option are not exercised). Therefore, Mr. Wang, Mr. Zhang, Zhirentuan, Zhirentuan / Tech, Zhirenxing, Xianzhikong, Zhirenying, Zhirenxue, Zhirenle, Zhirenju and Zhirenyun will / remain as the group of Controlling Shareholders upon Listing. / PRE-IPO INVESTMENT / From September 2017 to May 2025, we have completed several rounds of Pre-IPO / Investments. As of the Latest Practicable D
  - p17: remain as the group of Controlling Shareholders upon Listing. / PRE-IPO INVESTMENT / From September 2017 to May 2025, we have completed several rounds of Pre-IPO / Investments. As of the Latest Practicable Date, the Pre-IPO Investors hold approximately 60.56% / of our total issued share capital. Immediately following the completion of the Global Offering, the / Pre-IPO Investors will hold 51.35% o
  - p17: application; or (iii) 18 months following the submission of the Listing application. Considering that / the Company has no obligation to repurchase the Shares held by the Pre-IPO Investors, no / redemption liability was recorded during the Track Record Period. See “History, Development and / Corporate Structure — Pre-IPO Investments.” for further details of the Pre-IPO Investments. / Our Company a

### col_BB
  - p16: scope of such protection may not be sufficiently broad; and (v) we may become involved in lawsuits / to protect or enforce our intellectual property, which could be expensive, time-consuming and / unsuccessful. See “Risk Factors.” / CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Wang and Mr. Zhang beneficially owned 3.15% and / 0.45% of the total issued share capital of our Comp
  - p35: of / our / Pre-IPO / Investors and substantial shareholders / “HK eIPO White Form” / the application for Hong Kong Offer Shares to be issued in / the applicant’s own name by submitting applications online
  - p235: owners are independent of the other Cornerstone Investors, our Group, our connected persons and / their respective associates, and is not an existing Shareholder or a close associate of our Group; and / as confirmed by each of the Cornerstone Investors, each of the Cornerstone Investors and their / respective ultimate beneficial owners are independent from each other and make independent / investm

### col_BC
  - p16: scope of such protection may not be sufficiently broad; and (v) we may become involved in lawsuits / to protect or enforce our intellectual property, which could be expensive, time-consuming and / unsuccessful. See “Risk Factors.” / CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Wang and Mr. Zhang beneficially owned 3.15% and / 0.45% of the total issued share capital of our Comp
  - p35: of / our / Pre-IPO / Investors and substantial shareholders / “HK eIPO White Form” / the application for Hong Kong Offer Shares to be issued in / the applicant’s own name by submitting applications online

### col_BD
  - p16: scope of such protection may not be sufficiently broad; and (v) we may become involved in lawsuits / to protect or enforce our intellectual property, which could be expensive, time-consuming and / unsuccessful. See “Risk Factors.” / CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Wang and Mr. Zhang beneficially owned 3.15% and / 0.45% of the total issued share capital of our Comp
  - p16: CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Wang and Mr. Zhang beneficially owned 3.15% and / 0.45% of the total issued share capital of our Company, respectively. In addition, Mr. Wang / ultimately controlled 35.84% voting rights, which are attached to the 25.10%, 4.20%, 1.73%, / 0.81%, 1.91%, 1.11%, 0.55% and 0.42% of the total issued share capital of our Company held by / 
  - p35: of / our / Pre-IPO / Investors and substantial shareholders / “HK eIPO White Form” / the application for Hong Kong Offer Shares to be issued in / the applicant’s own name by submitting applications online

### col_BE
  - p279: (5) / Non-income taxes and other charges include value-added taxes and other charges recorded under / administrative expenses. / INDEBTEDNESS / As of December 31, 2022, 2023, 2024, September 30, 2025 and January 31, 2026, our / indebtedness included lease liabilities and interest-bearing bank borrowings. As of January 31, / 2026, we did not have any committed unutilized banking facilities. The fol
  - p265: 36,640 / 37,577 / 46,346 / Interest-bearing bank loans / 10,000 / – / –
  - p270: Prepayments, Deposits and Other Receivables / Our prepayments, deposits and other receivables primarily consisted of (i) value-added tax / recoverable, (ii) prepayments for our procurements and (iii) amounts due from Neura Robotics, / mainly representing the balance of borrowings to be repaid by the then-associate of our Company. / See “— Related Party Transactions.” The following table sets out a

### col_BF
  - p13: deployed in third-party applications ranging from industrial automation to advanced humanoid robots. / We are the only cobot provider in China among top cobot companies that offers our core motion / components for external sales. / Commercialization / We have adopted a transaction-based model for the sales of our products. Since the launch of / our first cobot in 2017, we have achieved rapid comme
  - p91: covering loading and unloading, assembly, polishing, grinding, dispensing and gluing operations; / (ii) welding, such as spot welding, arc welding and laser welding; (iii) handling and palletizing, / including material handling and palletizing and depalletizing operations; (iv) screw fastening, / primarily used in mass production scenarios such as electronic products and home appliances; and / (v)
  - p347: Effective for annual periods beginning on or after 1 January 2026 / 3 / Effective for annual/reporting periods beginning on or after 1 January 2027 / The Group is in the process of making a detailed assessment of the impact of these new and revised IFRS / Accounting Standards upon initial application. So far, the Group considers that these new and revised IFRS / Accounting Standards, except for IF

### col_BG
  - p28: commission of RMB48.4 million, and (ii) non-underwriting related expenses of RMB33.5 million, / which consist of fees and expenses of legal advisors and the Reporting Accountant of RMB20.0 / million and other fees and expenses of RMB13.5 million. / FUTURE PLANS AND USE OF PROCEEDS / Assuming that the Offer Size Adjustment Option and the Over-allotment Option are not / exercised, after deducting th
  - p28: commission of RMB48.4 million, and (ii) non-underwriting related expenses of RMB33.5 million, / which consist of fees and expenses of legal advisors and the Reporting Accountant of RMB20.0 / million and other fees and expenses of RMB13.5 million. / FUTURE PLANS AND USE OF PROCEEDS / Assuming that the Offer Size Adjustment Option and the Over-allotment Option are not / exercised, after deducting th

### col_BI
  - p2: Number of Offer Shares under the / Global Offering / : / 80,785,000 H Shares (subject to the / Offer Size Adjustment Option and the / Over-allotment Option) / Number of Hong Kong Offer Shares

### col_BP
  - p238: International Investment Management Limited (廣發國際資產管理有限公司) (“GF Fund HK”, / together with GF Fund Management, “GF Fund”) have, respectively, entered into Cornerstone / Investment Agreement with our Company. / GF Fund Management was established on August 5, 2003. As of December 31, 2025, GF Fund / Management’s assets under management exceeded 2 trillion yuan with comprehensive product / lines, and 
  - p1: Joint Bookrunners and Joint Lead Managers / Joint Bookrunners and Joint Lead Managers / Stock Code : 1021 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / 廣東華沿機器人股份有限公司 / Guangdong Huayan Robotics Co., Ltd.

### col_BR
  - p85: Head Office and Principal Place of Business / in the PRC / Room 1101, Building 9 / Haichuang Dazu Robot Intelligent
  - p345: 1. / CORPORATE INFORMATION / The Company is a joint stock company with limited liability incorporated in Shenzhen, People’s Republic of / China (the “PRC”). The registered office address of the Company is 1101, Building 9, Haichuang Dazu Robot / Intelligent Manufacturing Center, No. 3 Erzhi Industrial Avenue, Xihai Village, Beijiao Town, Shunde District, / Foshan City, Guangdong Province, the PRC.
  - p69: management presence in Hong Kong, which normally means that at least two executive directors / must be ordinarily resident in Hong Kong. Given that (i) our core business operations are / principally located, managed and conducted in the PRC and will continue to be based in the PRC; / (ii) our Company’s head office is situated in the PRC, our executive Directors and senior / management team princip

### col_BT
  - p244: The historical financial information has been prepared in accordance with IFRS Accounting / Standards, which comprise all standards and interpretations as issued by the International / Accounting Standards Board (the “IASB”). / All IFRS Accounting Standards effective for the accounting period commencing from January / 1, 2025, together with the relevant transitional provisions, have been early ado
  - p37: issued / by / the / International Accounting Standards Committee (IASC) / “Independent Third Party(ies)” / any entity(ies) or person(s) who is not a connected person of / our Company within the meaning of the Hong Kong Listing
  - p246: MATERIAL ACCOUNTING POLICY INFORMATION / We have identified certain accounting policies that are significant to the preparation of our / financial statements. Material accounting policies that are significant for understanding our / financial condition and results of operations are set forth in detail in Note 2.3 of the Accountants’ / Report in Appendix I lo this Prospectus. Some of our accounting

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on the websites of the / Stock Exchange at www.hkexnews.hk and our Company at www.huayan-robotics.com. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on Friday,
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on the websites of the / Stock Exchange at www.hkexnews.hk and our Company at www.huayan-robotics.com. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on Friday, / March 20, 2026 / Latest time for 

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on the websites of the / Stock Exchange at www.hkexnews.hk and our Company at www.huayan-robotics.com. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on Friday,

### col_CE
  - p27: liabilities as of the same date. / APPLICATION FOR LISTING ON THE STOCK EXCHANGE / We have applied to the Listing Committee for the granting of listing of, and permission to deal / in, our H Shares to be issued pursuant to the Global Offering (including any H Shares which may / be issued pursuant to the exercise of the Offer Size Adjustment Option and the Over-allotment / Option) and the H Shares 
  - p4: Your application must be for a minimum of 200 Hong Kong Offer Shares and in one / of the numbers set out in the table. You are required to pay the amount next to the / number you select. If you are applying through the HK eIPO White Form service, you / may refer to the table below for the amount payable for the number of H Shares you have / selected. You must pay the respective amount payable on a

### col_CF
  - p18: (204,008) / (136,988) / (175,328) / Gross profit                 / 15,006 / 50,230 / 106,433
  - p18: (204,008) / (136,988) / (175,328) / Gross profit                 / 15,006 / 50,230 / 106,433

### col_CG
  - p31: • / no Group entity has a voting or equity interest, board seat, or certain powers with respect / to any covered foreign person, where more than 50 percent of our annual revenue, net / income, capital expenditure or operating expenses (both individually and aggregated / across such entities) is attributable to covered foreign persons; and no entity within our / Group participates in any joint vent
  - p31: • / no Group entity has a voting or equity interest, board seat, or certain powers with respect / to any covered foreign person, where more than 50 percent of our annual revenue, net / income, capital expenditure or operating expenses (both individually and aggregated / across such entities) is attributable to covered foreign persons; and no entity within our / Group participates in any joint vent
  - p284: expenses, selling and distribution expenses, administrative expenses and other operating costs for / at least 12 months from the date of this Prospectus. / Our cash burn rate refers to the average monthly (i) net cash (used in)/from operating / activities, (ii) purchase of property, plant and equipment, and (iii) purchase of intangible assets. Our / historical cash burn rate was RMB13.7 million an

### col_CH
  - p328: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / OPINION / In our opinion, the Historical Financial Information gives, for the purposes of the / accountants’ report, a true and fair view of the financial position of the Group and the Company / as at 31 December 2022, 2023 and 2024 and 30 September 2025 and of the financial / perfor
  - p18: (0.09) / (0.08) / (0.09) / See Note 31 to the Accountants’ Report set out in Appendix I to this prospectus. / SUMMARY OF HISTORICAL AND FINANCIAL INFORMATION / The following tables set forth summary financial data from our consolidated financial / information for the Track Record Period, derived from the Accountants’ Report in Appendix I to this

### col_CI
  - p19: services from employees as consideration for our equity instruments. Share-based payment expenses are not / expected to result in future cash payments. / (2) / Listing expenses represent professional fees, underwriting commission, and other fees incurred in connection / with the Global Offering and the Listing. / Revenue / Revenue by Nature and Product Series/Line
  - p19: services from employees as consideration for our equity instruments. Share-based payment expenses are not / expected to result in future cash payments. / (2) / Listing expenses represent professional fees, underwriting commission, and other fees incurred in connection / with the Global Offering and the Listing. / Revenue / Revenue by Nature and Product Series/Line


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 1021.HK`
有 ERROR 必须回原文修正。
