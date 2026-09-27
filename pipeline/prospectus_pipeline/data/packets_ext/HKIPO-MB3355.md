# 3355.HK 扩展 18 列抽取包

公司：3355.HK FS.COM Ltd. - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB3355.json`。
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
- 股本结构（**已确认，不要改**）：L=400000000 M=40000000 N=360000000 O=360000000 P=0 Q=40000000 R=36000000 S=4000000
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = 564232000
- 行业分类（港交所官方）：702025 互聯網服務及基礎設施
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
{"code":"3355.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  3355.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 3355.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p30: Yuxuan Prudence, Yuxuan Progress and Yuxuan Growth, continue to control 55.04% voting / rights of our Company. Therefore, Mr. Xiang, Yuxuan Prudence, Yuxuan Progress and Yuxuan / Growth will remain as our Controlling Shareholders upon the Listing. / PRE-IPO INVESTMENT / As of the Latest Practicable Date, the Pre-IPO Investors hold approximately 38.84% of / our total issued share capital. Immediate
  - p30: rights of our Company. Therefore, Mr. Xiang, Yuxuan Prudence, Yuxuan Progress and Yuxuan / Growth will remain as our Controlling Shareholders upon the Listing. / PRE-IPO INVESTMENT / As of the Latest Practicable Date, the Pre-IPO Investors hold approximately 38.84% of / our total issued share capital. Immediately following the completion of the Global Offering, the / Pre-IPO Investors will hold 34
  - p30: Listing application within a prescribed time. Our Shares held by the Pre-IPO Investors are / subject to a statutory lock-up period of 12 months after the date of Listing. For details / regarding the background of the Pre-IPO Investors, see “History, Development and Corporate / Structure — Pre-IPO Investments.” / SUMMARY / – 19 –

### col_BB
  - p30: in Appendix I to this prospectus, and there is no event since September 30, 2025 which would / materially affect the information in the Accountants’ Report as set out in Appendix I to this / prospectus. / RELATIONSHIP WITH OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Xiang directly and indirectly controlled 61.16% / voting rights of the Company, among which, (i) he was dir
  - p43: “%” / per cent / In this prospectus, the terms “associate”, “close associate”, “connected person”, “core / connected person”, “connected transaction” and “substantial shareholder” shall have the / meanings given to such terms in the Hong Kong Listing Rules, unless the context otherwise / requires. / Certain amounts and percentage figures included in this prospectus have been subject to
  - p321: Placing; (iii) all necessary approvals have been obtained with respect to the Cornerstone / Placing and no specific approval from any stock exchange (if relevant) is required for the / relevant Cornerstone Placing and (iv) each of the Cornerstone Investors and their respective / ultimate beneficial owners is an Independent Third Party. / The Cornerstone Investors have agreed to fully pay for the r

### col_BC
  - p30: in Appendix I to this prospectus, and there is no event since September 30, 2025 which would / materially affect the information in the Accountants’ Report as set out in Appendix I to this / prospectus. / RELATIONSHIP WITH OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Xiang directly and indirectly controlled 61.16% / voting rights of the Company, among which, (i) he was dir
  - p43: “%” / per cent / In this prospectus, the terms “associate”, “close associate”, “connected person”, “core / connected person”, “connected transaction” and “substantial shareholder” shall have the / meanings given to such terms in the Hong Kong Listing Rules, unless the context otherwise / requires. / Certain amounts and percentage figures included in this prospectus have been subject to

### col_BD
  - p30: in Appendix I to this prospectus, and there is no event since September 30, 2025 which would / materially affect the information in the Accountants’ Report as set out in Appendix I to this / prospectus. / RELATIONSHIP WITH OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Xiang directly and indirectly controlled 61.16% / voting rights of the Company, among which, (i) he was dir
  - p30: prospectus. / RELATIONSHIP WITH OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Xiang directly and indirectly controlled 61.16% / voting rights of the Company, among which, (i) he was directly interested in 56.65% of the / total issued share capital of our Company; and (ii) he controlled voting rights attached to the / 3.19%, 0.74% and 0.58% issued share capital of our Compan
  - p43: “%” / per cent / In this prospectus, the terms “associate”, “close associate”, “connected person”, “core / connected person”, “connected transaction” and “substantial shareholder” shall have the / meanings given to such terms in the Hong Kong Listing Rules, unless the context otherwise / requires. / Certain amounts and percentage figures included in this prospectus have been subject to

### col_BE
  - p268: used for research and development activities. / Finance Costs / Our finance costs increased by 298.4% from RMB4.7 million in 2023 to RMB18.5 million / in 2024, primarily due to the addition of two borrowings in 2024. See “— Indebtedness — / Borrowings.” / Income Tax Expense / Our income tax expense remained relatively stable at RMB56.5 million in 2023 and
  - p339: viable, or the occurrence of force majeure events, we will carefully evaluate the situation and / may reallocate the net proceeds from the Global Offering. / To the extent that the net proceeds of the Global Offering are not immediately used for / the above purposes, we will only deposit those net proceeds into short-term interest-bearing / accounts at licensed commercial banks and/or other author
  - p19: current assets increased from RMB1,476.3 million as of December 31, 2024 to RMB1,587.3 / million as of September 30, 2025, primarily due to (i) an increase in financial assets at FVTPL / of RMB187.6 million; and (ii) an increase in bank balances and cash of RMB81.8 million, / partially offset by (i) an increase in borrowings of RMB112.5 million; and (ii) a decrease in / inventories of RMB87.4 mill

### col_BF
  - p48: expenses amounted to RMB99.8 million, RMB110.5 million, RMB143.7 million, RMB99.8 / million and RMB124.3 million, respectively, accounting for 5.0%, 5.0%, 5.5%, 5.1% and 5.7% / of our total revenue in the same respective periods. However, there is no assurance that our / R&D efforts will yield successful outcomes or that we will be able to commercialize new / technologies effectively. Any failure 
  - p218: delivery of high-quality products. We have also established four major testing systems, / including networking equipment, optical modules, optical transmission and integrated cabling, / covering from the sample stage to small batch trial production, as well as quality assurance / testing of finished products during mass production. We generally use performance, / functionality, compatibility, para
  - p245: I to this Prospectus for material accounting policy information. / The preparation of the historical financial information in conformity with IFRS requires / the use of certain critical accounting estimates. It also requires management to exercise its / judgment in the process of applying our accounting policies. The areas involving a higher / degree of judgment or complexity, or areas where assum

### col_BG
  - p21: Debt ratio equals net debt divided by total equity and multiplied by 100%. Net debt equals bank / borrowing plus lease liabilities plus redemption liabilities minus bank balances and cash. / See “Financial Information — Key Financial Ratios.” / FUTURE PLANS AND USE OF PROCEEDS / Assuming an Offer Price of HK$38.40 per Offer Share (being the mid-point of the stated / range of the Offer Price betwee
  - p21: Debt ratio equals net debt divided by total equity and multiplied by 100%. Net debt equals bank / borrowing plus lease liabilities plus redemption liabilities minus bank balances and cash. / See “Financial Information — Key Financial Ratios.” / FUTURE PLANS AND USE OF PROCEEDS / Assuming an Offer Price of HK$38.40 per Offer Share (being the mid-point of the stated / range of the Offer Price betwee

### col_BI
  - p2: Number of Offer Shares under the / Global Offering / : / 40,000,000 H Shares (subject to the / Over-allotment Option) / Number of Hong Kong Offer Shares / :

### col_BP
  - p328: Investors” in this prospectus. / GF Fund HK / GF Management Co., Ltd. (廣發基金管理有限公司) (“GF Fund Management”) was / established on August 5, 2003. As of December 31, 2025, the assets under management of GF / Fund Management exceeded RMB2 trillion with comprehensive product lines, and covering / active equity, bonds, currencies, overseas investment, passive investments, FOF, quantitative / hedging, etc
  - p1: Stock Code : 3355 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / Joint Sponsors, Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers / Joint Bookrunners / 深圳市飛速創新技術股份有限公司

### col_BR
  - p102: Shenzhen / Guangdong Province / PRC / Principal Place of Business in Hong Kong / Room 1910, 19/F / Lee Garden One / 33 Hysan Avenue Causeway Bay
  - p395: INFORMATION / The Company was incorporated in the PRC on April 9, 2009 as a limited liability company under the Company / Law of the PRC. On September 29, 2020, the Company was converted from a limited liability company into a joint / stock company. The respective addresses of the registered office and the principal place of business of the Company / are stated in the section headed “Corporate Inf
  - p79: sufficient management presence in Hong Kong, which normally means that at least two / executive directors must be ordinarily resident in Hong Kong. Given that (i) our core business / operations are principally located, managed and conducted out of Hong Kong; (ii) our / Company’s head office is situated in the PRC, our executive Directors and senior management / team principally reside in the PRC a

### col_BT
  - p37: Expenses — The Hong Kong Public Offering — Hong / Kong Underwriting Agreement” in this prospectus / “IFRS” / IFRS Accounting Standards, which include standards, / amendments and interpretations promulgated by the / International Accounting Standards Board and the IFRIC / Interpretations
  - p442: (ii) / The financial statements of the Company’s subsidiaries established in the PRC and other regions were prepared / in accordance with the relevant accounting principles (including Chinese Generally Accepted Accounting / Principles (“PRC GAAP”), HKFRS for Private Entities Accounting Standards, IFRS Accounting Standards, / Singapore Financial Reporting Standards (“SFRS”), Generally Accepted Acco
  - p37: Expenses — The Hong Kong Public Offering — Hong / Kong Underwriting Agreement” in this prospectus / “IFRS” / IFRS Accounting Standards, which include standards, / amendments and interpretations promulgated by the / International Accounting Standards Board and the IFRIC / Interpretations

### col_CC
  - p6: If there is any change to the expected timetable of the Hong Kong Public Offering, / we will issue an announcement on the respective websites of the Company at / https://www.fs.com and the Stock Exchange at www.hkexnews.hk. / Hong Kong Public Offering commences
  - p6: If there is any change to the expected timetable of the Hong Kong Public Offering, / we will issue an announcement on the respective websites of the Company at / https://www.fs.com and the Stock Exchange at www.hkexnews.hk. / Hong Kong Public Offering commences / . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on Friday, / March 13, 2026 / Latest time for completing electronic application

### col_CD
  - p6: If there is any change to the expected timetable of the Hong Kong Public Offering, / we will issue an announcement on the respective websites of the Company at / https://www.fs.com and the Stock Exchange at www.hkexnews.hk. / Hong Kong Public Offering commences

### col_CE
  - p91: regulatory authorities or an exemption therefrom. / APPLICATION FOR LISTING OF THE H SHARES ON THE STOCK EXCHANGE / We have applied to the Listing Committee of the Stock Exchange for the granting of the / listing of, and permission to deal in, our H Shares to be issued pursuant to the Global Offering / and the H Shares to be converted from Unlisted Shares. / No part of the H Shares is listed on or
  - p370: custodian. / If you are applying through the HK eIPO White / Form service, you may refer to the table below for / the amount payable for the number of H Shares / you have selected. You must pay the respective / maximum amount payable on application in full / upon application for Hong Kong Offer Shares.

### col_CF
  - p12: 14.6% / CAGR of revenue 2022-2024 / 50.0%; 52.6% / Gross profit margin in 2024 and the / nine months ended September 30, 2025, / respectively / ;
  - p12: 14.6% / CAGR of revenue 2022-2024 / 50.0%; 52.6% / Gross profit margin in 2024 and the / nine months ended September 30, 2025, / respectively / ;

### col_CG
  - p22: in the form of cash and may conduct interim dividends. Any proposed distribution of dividends / is subject to the discretion of our Board and the approval of our Shareholders. Our Board may / propose a distribution of dividends in the future after taking into account our financial / performance, working capital requirements, capital expenditure requirements, future expansion / plans, liquidity pos
  - p22: in the form of cash and may conduct interim dividends. Any proposed distribution of dividends / is subject to the discretion of our Board and the approval of our Shareholders. Our Board may / propose a distribution of dividends in the future after taking into account our financial / performance, working capital requirements, capital expenditure requirements, future expansion / plans, liquidity pos

### col_CH
  - p384: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the / accountants’ report, a true and fair view of the Group’s and the Company’s financial position / as at December 31, 2022, 2023 and 2024 and September 30, 2025, and of the Group’s financial 
  - p16: SUMMARY OF KEY FINANCIAL INFORMATION / The following tables summarize our consolidated financial results during the Track / Record Period and should be read in conjunction with “Financial Information” of this / prospectus and the Accountants’ Report set out in Appendix I to this prospectus, together with / the respective accompanying notes. / SUMMARY / – 5 –

### col_CI
  - p17: (18,544) / (12,823) / (19,997) / Listing expenses         / – / – / (893)
  - p17: (18,544) / (12,823) / (19,997) / Listing expenses         / – / – / (893)


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 3355.HK`
有 ERROR 必须回原文修正。
