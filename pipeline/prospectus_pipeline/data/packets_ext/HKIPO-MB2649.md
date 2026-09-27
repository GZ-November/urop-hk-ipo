# 2649.HK 扩展 18 列抽取包

公司：2649.HK ALSCO Pooling Service Co., Ltd. - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB2649.json`。
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
- 股本结构（**已确认，不要改**）：L=90336000 M=20336000 N=70000000 O=70000000 P=0 Q=20336000 R=18302000 S=2034000
- 财务期间（**已确认**）：year-1 期末 = 31/08/2025；币种 = RMB；year-1 净利 = 40338000
- 行业分类（港交所官方）：103020 印刷及包裝
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
{"code":"2649.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  2649.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 2649.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p20: allotment Option is not exercised), Mr. Sun and Suzhou Anhua will collectively hold / approximately 43.63% of our total issued Shares. Accordingly, Mr. Sun and Suzhou Anhua will / remain as our Controlling Shareholders immediately after Listing. / Pre-IPO Investments / We conducted the Pre-IPO Investments with the Pre-IPO Investors, namely, Suzhou / Emerging Industry, Yuandian Zhengze, Suqian Inte
  - p20: approximately 43.63% of our total issued Shares. Accordingly, Mr. Sun and Suzhou Anhua will / remain as our Controlling Shareholders immediately after Listing. / Pre-IPO Investments / We conducted the Pre-IPO Investments with the Pre-IPO Investors, namely, Suzhou / Emerging Industry, Yuandian Zhengze, Suqian International Development, Suzhou Union, / Changzhou Shuguang, Shanghai Qianjin, Hangzhou 
  - p20: allotment Option is not exercised), Mr. Sun and Suzhou Anhua will collectively hold / approximately 43.63% of our total issued Shares. Accordingly, Mr. Sun and Suzhou Anhua will / remain as our Controlling Shareholders immediately after Listing. / Pre-IPO Investments / We conducted the Pre-IPO Investments with the Pre-IPO Investors, namely, Suzhou / Emerging Industry, Yuandian Zhengze, Suqian Inte

### col_BB
  - p19: We are subject to laws and regulations regarding regulatory matters that may have / increased or will increase both our costs and the risk of non-compliance. / OUR SHAREHOLDING STRUCTURE / Our Controlling Shareholders / As of the Latest Practicable Date, Mr. Sun and Suzhou Anhua held 36,093,750 and / 3,318,924 Shares, representing approximately 51.56% and 4.74% of our total issued Shares, / respec
  - p47: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / as the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / as the meaning ascribed thereto under the Listing Rules / “Supervisor(s)” / member(s) of our Supervisory Committee
  - p164: Park Finance and Audit Bureau (蘇州工業園區財政審計局). / Independence of the Pre-IPO Investors / To the best knowledge of our Directors, save for Dr. Fang Dianjun, our non-executive / Director, each of the Pre-IPO Investors and their ultimate beneficial owners is an Independent / Third Party. / Sole Sponsor’s Confirmation / On the basis that (i) the consideration for the Pre-IPO Investments was settled more

### col_BC
  - p19: We are subject to laws and regulations regarding regulatory matters that may have / increased or will increase both our costs and the risk of non-compliance. / OUR SHAREHOLDING STRUCTURE / Our Controlling Shareholders / As of the Latest Practicable Date, Mr. Sun and Suzhou Anhua held 36,093,750 and / 3,318,924 Shares, representing approximately 51.56% and 4.74% of our total issued Shares, / respec
  - p47: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / as the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / as the meaning ascribed thereto under the Listing Rules / “Supervisor(s)” / member(s) of our Supervisory Committee

### col_BD
  - p19: We are subject to laws and regulations regarding regulatory matters that may have / increased or will increase both our costs and the risk of non-compliance. / OUR SHAREHOLDING STRUCTURE / Our Controlling Shareholders / As of the Latest Practicable Date, Mr. Sun and Suzhou Anhua held 36,093,750 and / 3,318,924 Shares, representing approximately 51.56% and 4.74% of our total issued Shares, / respec
  - p19: As of the Latest Practicable Date, Mr. Sun and Suzhou Anhua held 36,093,750 and / 3,318,924 Shares, representing approximately 51.56% and 4.74% of our total issued Shares, / respectively. As Mr. Sun directly owns 90% equity interests in Suzhou Anhua and can control / the voting rights attached to the Shares held by Suzhou Anhua, Mr. Sun and Suzhou Anhua are / considered to be a group of Controllin
  - p47: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / as the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / as the meaning ascribed thereto under the Listing Rules / “Supervisor(s)” / member(s) of our Supervisory Committee

### col_BE
  - p34: Our Directors confirm that, subsequent to the Track Record Period and up to the date of / the prospectus, there had been no material adverse change in our business operations, the / business environment in which we operate, as well as our financial or trading position, / indebtedness, mortgage, contingent liabilities, guarantees or prospects. / PROFIT ESTIMATE FOR THE YEAR ENDED DECEMBER 31, 2025 
  - p27: cash and cash equivalents of RMB32.3 million. / Our net current assets decreased from RMB120.6 million as of December 31, 2024 to / RMB119.8 million as of August 31, 2025, primarily due to (i) a decrease in our trade and bills / receivables of RMB57.9 million; and (ii) an increase in interest-bearing bank and other / borrowings of RMB76.7 million, partially offset by (i) a decrease in our trade an
  - p27: Our net current assets decreased from RMB120.6 million as of December 31, 2024 to / RMB119.8 million as of August 31, 2025, primarily due to (i) a decrease in our trade and bills / receivables of RMB57.9 million; and (ii) an increase in interest-bearing bank and other / borrowings of RMB76.7 million, partially offset by (i) a decrease in our trade and bills / payables of RMB46.8 million; (ii) an i

### col_BF
  - p55: subsidies, economic incentives and policies, such as the Notice on Improving the Policies of / Government Subsidies for Promotion and Application of New Energy Vehicles (《關於完善新 / 能源汽車推廣應用財政補貼政策的通知》) that was issued in 2020 to provide monetary / rewards to eligible city clusters for the commercialization of key technologies used in the fuel / cell vehicles, and any updates on the government policie
  - p235: Service Scope. We sell the customer a specified number of sets of the product. The / mold-making process begins upon contract signing and receipt of the deposit. We / will send sample products to the customer, and upon their written confirmation (via / email or written reply) that there are no issues, we will commence mass production / and deliver the products according to the agreed delivery meth
  - p79: performance and fluctuation of the market prices of other companies with business operations / located mainly in the PRC that have listed their securities in Hong Kong may affect the / volatility in the price of and trading volumes for our H Shares. A number of PRC-based / companies have listed their securities, and some are in the process of preparing for listing their / securities, in Hong Kong.

### col_BG
  - p32: FUTURE PLANS AND USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$204.8 million, after deducting underwriting commissions, fees and estimated expenses / payable by us in connection with the Global Offering, and assuming the Over-allotment Option
  - p32: FUTURE PLANS AND USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$204.8 million, after deducting underwriting commissions, fees and estimated expenses / payable by us in connection with the Global Offering, and assuming the Over-allotment Option

### col_BI
  - p2: Number of Offer Shares under the Global / Offering / : / 20,336,000 H Shares (subject to the Over- / allotment Option) / Number of Hong Kong Offer Shares / :

### col_BP
  - p1: Stock Code : 2649 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / GLOBAL OFFERING / Sole Sponsor, Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager / 蘇州優樂賽共享服務股份有限公司

### col_BR
  - p103: Suzhou Industrial Park / Suzhou, Jiangsu / PRC / Principal Place of Business in Hong Kong / 46/F, Hopewell Centre / 183 Queen’s Road East / Wanchai
  - p103: Registered Office in the PRC / Room 3A, Jiacheng Building / No. 128 Zhongxin Avenue West / Suzhou Industrial Park

### col_BT
  - p446: framework of the Company’s jurisdiction and the governing law of the supplementary agreements, the directors / considered that it is appropriate to present the pre-IPO Investments as equity throughout the Relevant Periods. For / details of the financial impacts, see note 28 to this report. / The Historical Financial Information has been prepared in accordance with IFRS Accounting Standards, which 
  - p447: IFRS 19 /                    / Subsidiaries without Public Accountability: Disclosures2 / Amendments to IFRS 9 and HKFRS 7  / Amendments to the Classification and Measurement of / Financial Instruments1 / Amendments to IFRS 9 and HKFRS 7 
  - p42: amendments / and / interpretations / promulgated by the International Accounting Standards / Board and the International Accounting Standards and / interpretation issued by the International Accounting / Standards Committee

### col_CC
  - p5: If there is any change in the following expected timetable of the Global Offering, we / will issue an announcement in Hong Kong to be published on the Stock Exchange’s / website at www.hkexnews.hk and our Company’s website at www.anwood.com.cn. / Date(1)
  - p5: will issue an announcement in Hong Kong to be published on the Stock Exchange’s / website at www.hkexnews.hk and our Company’s website at www.anwood.com.cn. / Date(1) / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on / Friday, February 27, 2026 / Latest time to complete electronic applications under / White Form eIPO service through

### col_CD
  - p5: If there is any change in the following expected timetable of the Global Offering, we / will issue an announcement in Hong Kong to be published on the Stock Exchange’s / website at www.hkexnews.hk and our Company’s website at www.anwood.com.cn. / Date(1)

### col_CE
  - p93: APPLICATION FOR LISTING OF THE H SHARES ON THE HONG KONG STOCK / EXCHANGE / We have applied to the Hong Kong Stock Exchange for the granting of listing of, and / permission to deal in, our H Shares to be issued pursuant to the Global Offering (including any / H Shares which may be issued pursuant to the exercise of the Over-allotment Option) and the / H Shares to be converted from Unlisted Shares.
  - p409: on whether sufficient number of H Shares will be made available under delayed delivery / arrangements. There will be no stabilization actions and no exercise of the Over-allotment / Option should no investors be willing to enter into such delayed delivery arrangements. / The Company will ensure that an announcement in compliance with the Securities and

### col_CF
  - p20: (653,479) / (398,432) / (422,138) / GROSS PROFIT           / 127,448 / 169,872 / 184,141
  - p20: (653,479) / (398,432) / (422,138) / GROSS PROFIT           / 127,448 / 169,872 / 184,141

### col_CG
  - p12: logistical / complexities. For customer-owned container management, we are responsible / for the operation and management of clients’ own containers, helping them / improve asset utilization and reduce capital expenditures related to container / management. / • / Container Sales: Our container sales business targets customers with logistical
  - p12: logistical / complexities. For customer-owned container management, we are responsible / for the operation and management of clients’ own containers, helping them / improve asset utilization and reduce capital expenditures related to container / management. / • / Container Sales: Our container sales business targets customers with logistical

### col_CH
  - p432: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the / accountants’ report, a true and fair view of the financial position of the Group and the Company / as at 31 December 2022, 2023 and 2024 and 31 August 2025 and of the financial performance
  - p20: Pre-IPO Investors and the principal terms of the Pre-IPO Investments. / SUMMARY KEY FINANCIAL INFORMATION / The following table summarizes the financial information of our Group during the Track / Record Period, which is extracted from the Accountants’ Report set out in Appendix I to this / prospectus. / Summary of Consolidated Statements of Profit or Loss / Year ended 31 December

### col_CI
  - p22: adjusted by adding back equity-settled share option expense and listing expenses. Equity- / settled share option expense is non-cash in nature. Listing expenses are expenses relating to the / Global Offering. The following table sets out a reconciliation of profit for the year/period to / EBITDA (non-IFRS measure) and adjusted EBITDA (non-IFRS measure) for the years/periods
  - p22: adjusted by adding back equity-settled share option expense and listing expenses. Equity- / settled share option expense is non-cash in nature. Listing expenses are expenses relating to the / Global Offering. The following table sets out a reconciliation of profit for the year/period to / EBITDA (non-IFRS measure) and adjusted EBITDA (non-IFRS measure) for the years/periods


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 2649.HK`
有 ERROR 必须回原文修正。
