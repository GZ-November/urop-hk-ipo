# 2726.HK 扩展 18 列抽取包

公司：2726.HK Epiworld International Co., Ltd. - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB2726.json`。
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
- 股本结构（**已确认，不要改**）：L=425584810 M=21492050 N=404092760 O=404092760 P=0 Q=21492050 R=19342800 S=2149250
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = 28193333.333333332
- 行业分类（港交所官方）：703020 半導體設備與材料
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
{"code":"2726.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  2726.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 2726.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p19: of our total issued share capital and he will be our Single Largest Shareholder upon Listing. For / more details, see “Relationship with the Single Largest Shareholder.” / OUR PRE-IPO INVESTORS / We have undergone multiple rounds of Pre-IPO Investments. For further details of the identity / and background of the Pre-IPO Investors and the principal terms of the Pre-IPO Investments, see / “History, 
  - p19: Immediately following the completion of the Global Offering, Dr. Zhao will control 27.39% / of our total issued share capital and he will be our Single Largest Shareholder upon Listing. For / more details, see “Relationship with the Single Largest Shareholder.” / OUR PRE-IPO INVESTORS / We have undergone multiple rounds of Pre-IPO Investments. For further details of the identity / and background o
  - p19: of our total issued share capital and he will be our Single Largest Shareholder upon Listing. For / more details, see “Relationship with the Single Largest Shareholder.” / OUR PRE-IPO INVESTORS / We have undergone multiple rounds of Pre-IPO Investments. For further details of the identity / and background of the Pre-IPO Investors and the principal terms of the Pre-IPO Investments, see / “History, 

### col_BB
  - p126: fulfill the filing procedure and submit relevant information to the CSRC; if a domestic company / fails to complete the filing procedure or conceals any material fact or falsifies any major content / in its filing documents, it may be subject to administrative penalties, such as order to rectify, / warnings and fines, and its controlling shareholders, de facto controllers, the person directly in /
  - p45: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Supervisor(s)” / supervisor(s) of the Company
  - p133: Xike Zhongheng is a limited partnership established in the PRC on January 7, 2013, / principally engaged in the investments in high-tech industries. The general partner of Xike / Zhongheng is Mr. Su Ping (蘇平), our non-executive Director, who holds 27.53% of the partnership / interests therein as the ultimate beneficial owner. / There are 20 limited partners in Xike Zhongheng, amongst which i) Ms. 

### col_BC
  - p126: fulfill the filing procedure and submit relevant information to the CSRC; if a domestic company / fails to complete the filing procedure or conceals any material fact or falsifies any major content / in its filing documents, it may be subject to administrative penalties, such as order to rectify, / warnings and fines, and its controlling shareholders, de facto controllers, the person directly in /
  - p45: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Supervisor(s)” / supervisor(s) of the Company

### col_BD
  - p126: fulfill the filing procedure and submit relevant information to the CSRC; if a domestic company / fails to complete the filing procedure or conceals any material fact or falsifies any major content / in its filing documents, it may be subject to administrative penalties, such as order to rectify, / warnings and fines, and its controlling shareholders, de facto controllers, the person directly in /
  - p88: Existing Shareholder Conditions: / (a) / the Minority Existing Shareholders are interested in less than 5% of the Company’s / voting rights prior to the completion of the Global Offering; / (b) / each of the Minority Existing Shareholders and its close associates are not, and will not / be, core connected persons (as defined under the Listing Rules) of the Company or any
  - p45: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Supervisor(s)” / supervisor(s) of the Company

### col_BE
  - p33: in the long-term, we have implemented a range of measures to enhance our profitability. For details / on our concrete plan to expand our revenue, see “Financial Information — Financial Strategies.” / Our Directors confirm that, as of the date of the Prospectus, there has been no material adverse / change in our financial or trading position, indebtedness, mortgage, contingent liabilities, / guaran
  - p255: 806,563 / Our borrowings amounted to RMB313.2 million, RMB1,127.0 million, RMB1,112.1 million, / RMB769.5 million, and RMB806.5 million as of December 31, 2022, 2023 and 2024, September 30, / 2025, and January 31, 2026, respectively. For the interest rate profile of our interest-bearing bank / borrowings during the Track Record Period, see Note 28 to the Accountant’s Report in Appendix / I to this
  - p25: 67 / 66 / 67 / Borrowings               / 142,405 / 315,181 / 303,536

### col_BF
  - p11: Largest / World’s largest SiC epitaxial foundry1 / First / in the commercialization of 8-inch SiC / epitaxial wafer in the open market2 / Leader / of setting industry standards3
  - p11: and “Glossary of Technical Terms” in this Prospectus. / OVERVIEW / We are a global leader in the silicon carbide (SiC) epitaxy industry. We have been primarily / engaged in the research and development, mass production and sales of SiC epitaxial wafers, / components used in the manufacturing of SiC semiconductor devices. Our customers utilize our SiC / epitaxial wafers to manufacture their power d
  - p188: employees. The Company has obtained ISO45001:2018 for Occupational Health and Safety / Management System. To mitigate the risks in the workplace that may endanger the health of / employees or damage the property of the Company, we have formulated safety management of / hazardous chemicals and pollution prevention and control strategies. We are in the process of / developing additional procedures t

### col_BG
  - p32: According to our PRC Legal Adviser, the business operations we engaged in had been carried / out in compliance with applicable PRC laws and regulations in all material respects during the / Track Record Period and up to the Latest Practicable Date. / FUTURE PLANS AND USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$1,560.1 million, afte
  - p238: Finance Costs / Our finance costs decreased by RMB12.0 million, or 55.4%, from RMB21.6 million for the / nine months ended September 30, 2024 to RMB9.6 million for the same period in 2025, primarily / due to our repayment of borrowings from our equity financing activities and operational cash / inflow. / Income Tax Expense / Our income tax expense decreased from RMB37.1 million for the nine months
  - p32: According to our PRC Legal Adviser, the business operations we engaged in had been carried / out in compliance with applicable PRC laws and regulations in all material respects during the / Track Record Period and up to the Latest Practicable Date. / FUTURE PLANS AND USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$1,560.1 million, afte

### col_BI
  - p2: Number of Offer Shares under / the Global Offering / : / 21,492,050 H Shares / Number of Hong Kong Offer Shares / : / 2,149,250 H Shares (subject to

### col_BP
  - p200: business administration in June 2006 from Xiamen University (廈門大學) in the PRC. / Ms. Xie also notified the Board that she has served as director of UCAR (Xiamen) Information / Technology Co., Ltd. (神州優車(廈門)信息科技有限公司) (“UCAR”) since May 2019. UCAR was / incorporated on March 14, 2019 in Xiamen City, Fujian Province, People’s Republic of China, / primarily as an investment platform to hold shares in 
  - p1: 瀚天天成電子科技（廈門）股份有限公司 / Epiworld International Co., Ltd. / Stock Code : 2726 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / GLOBAL OFFERING / Sole Sponsor, Sponsor-Overall Coordinator, Overall Coordinator, / Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager

### col_BR
  - p99: Registered Office, Headquarters and / Principal Place of Business in the PRC / No. 198-1, East 2nd Road / Tongxiang High-tech City / Torch Hi-tech Zone
  - p99: Registered Office, Headquarters and / Principal Place of Business in the PRC / No. 198-1, East 2nd Road / Tongxiang High-tech City

### col_BT
  - p221: BASIS OF PRESENTATION AND PREPARATION / The consolidated financial statements of the Group for the Track Record Period, on which the / Historical Financial Information is based, have been prepared in accordance with the accounting / policies which conform with IFRS Accounting standards (“IFRSs”) issued by International / Accounting Standards Board (“IASB”) and were audited by BDO Limited in accord
  - p41: issued / by / the / International Accounting Standards Committee (IASC) / “IIT Law” / the Individual Income Tax Law of the PRC (《中華人民共 / 和國個人所得稅法》)
  - p221: to this Prospectus. / The preparation of the Historical Financial Information in conformity with IFRSs requires the / use of certain critical accounting estimates. It also requires management to exercise its judgment in / the process of applying the Group’s accounting policies. The areas involving a higher degree of / judgment or complexity, or areas where assumptions and estimates are significant

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong on the websites of the Stock / Exchange at www.hkexnews.hk and our Company at http://www.epiworld.com.cn/. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong on the websites of the Stock / Exchange at www.hkexnews.hk and our Company at http://www.epiworld.com.cn/. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on / Friday, March 20, 2026 / Latest time for 

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong on the websites of the Stock / Exchange at www.hkexnews.hk and our Company at http://www.epiworld.com.cn/. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on

### col_CE
  - p272: Offer Shares for subscription on the terms and conditions set out in this prospectus and the Hong / Kong Underwriting Agreement at the Offer Price. / Subject to (a) the Stock Exchange granting approval for the listing of, and permission to deal / in, the H Shares to be issued pursuant to the Global Offering (including the H Shares to be converted / from Unlisted Shares) as mentioned herein on the 
  - p138: Immediately following the completion of the Global Offering and based on the Offer Price, / the expected market capitalization of the class of shares to which the H Shares belong at the time / of Listing will be over HK$30,000,000,000 and pursuant to Rule 8.08 (as amended and replaced by / Rule 19A.13A), the minimum number of H Shares held by the public at the time of Listing as a / percentage of 

### col_CF
  - p20: (642,007) / (522,542) / (397,982) / Gross profit           / 196,937 / 445,399 / 332,309
  - p20: (642,007) / (522,542) / (397,982) / Gross profit           / 196,937 / 445,399 / 332,309

### col_CG
  - p31: estimated net proceeds from the Global Offering, our Directors believe that we have sufficient / working capital for our present requirements and for the next 12 months from the date of this / Prospectus. / We intend to finance our future working capital requirements and capital expenditures / primarily from cash expected to be generated from operating activities, bank facilities and funds / raise
  - p31: estimated net proceeds from the Global Offering, our Directors believe that we have sufficient / working capital for our present requirements and for the next 12 months from the date of this / Prospectus. / We intend to finance our future working capital requirements and capital expenditures / primarily from cash expected to be generated from operating activities, bank facilities and funds / raise
  - p254: inventories of RMB40.2 million. / Net Cash Used in Investing Activities / For the nine months ended September 30, 2025, our net cash used in investing activities was / RMB21.5 million, primarily attributable to purchase of property, plant and equipment of RMB69.8 / million; partially offset by interest received of RMB48.9 million. / In 2024, our net cash used in investing activities was RMB144.3 m

### col_CH
  - p304: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / OPINION / In our opinion, the Historical Financial Information gives, for the purposes of the / accountants’ report, a true and fair view of the Group’s financial position as at December 31, / 2022, 2023, 2024 and September 30, 2025, the Company’s financial position as at December / 
  - p34: UPDATES ON FINANCIAL INFORMATION / Save as disclosed in the section headed “Financial Information” and the Accountants’ Report / included in Appendix I to this Prospectus, our Directors confirm that, as of the date of this / Prospectus, there has been no material adverse change in our financial or trading position, / indebtedness, mortgage, contingent liabilities, guarantees or prospects of our Gr

### col_CI
  - p32: approximately 10% of the net proceeds, or HK$156.0 million, will be used as working / capital and for general corporate purposes. / For details, please see “Future Plans and Use of Proceeds.” / LISTING EXPENSES / Our listing expenses mainly include (i) underwriting-related expenses, such as underwriting / fees and commissions, and (ii) non-underwriting-related expenses, comprising professional fee
  - p32: approximately 10% of the net proceeds, or HK$156.0 million, will be used as working / capital and for general corporate purposes. / For details, please see “Future Plans and Use of Proceeds.” / LISTING EXPENSES / Our listing expenses mainly include (i) underwriting-related expenses, such as underwriting / fees and commissions, and (ii) non-underwriting-related expenses, comprising professional fee


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 2726.HK`
有 ERROR 必须回原文修正。
