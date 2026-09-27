# 1768.HK 扩展 18 列抽取包

公司：1768.HK BUSY MING GROUP CO., LTD.- H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB1768.json`。
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
- 股本结构（**已确认，不要改**）：L=214101100 M=14101100 N=200000000 O=200000000 P=0 Q=14101100 R=12690900 S=1410200
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = 2078376000
- 行业分类（港交所官方）：251010 包裝食品
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
{"code":"1768.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  1768.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 1768.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p23: 488,879 / 1,558,782 / For details on the accounting treatment of redemption rights and liquidation preference / rights of pre-IPO investments, see “— Pre-IPO Investments” below and note 29 to the / Accountants’ Report set out in Appendix I to this prospectus. / Non-IFRS Measure / To supplement our consolidated financial statements, which are presented in accordance
  - p32: group of our Controlling Shareholders. / PRE-IPO INVESTMENTS / We have completed series rounds of Pre-IPO Investments. For further details of the / identity and background of the Pre-IPO Investors and the principal terms of the Pre-IPO / Investments, / please / see
  - p23: 488,879 / 1,558,782 / For details on the accounting treatment of redemption rights and liquidation preference / rights of pre-IPO investments, see “— Pre-IPO Investments” below and note 29 to the / Accountants’ Report set out in Appendix I to this prospectus. / Non-IFRS Measure / To supplement our consolidated financial statements, which are presented in accordance

### col_BB
  - p32: 2025, being the end date of our latest consolidated financial statements, and there has been no / event since September 30, 2025 that would materially affect the information shown in the / Accountants’ Report set out in Appendix I to this prospectus. / OUR CONTROLLING SHAREHOLDERS / Immediately following the completion of the Global Offering (assuming the Offer Size / Adjustment Option and the Ove
  - p50: “subsidiary(ies)” / has the meaning ascribed to it in section 15 of the / Companies Ordinance / “substantial shareholder(s)” / has the meaning ascribed to it in the Listing Rules / “Super Ming Group” / Super Ming Food Technology and its subsidiaries
  - p341: liability company incorporated in Hong Kong, and is primarily engaged in asset management. / It is licensed to carry out Type 1 (Dealing in securities), Type 4 (Advising on securities) and / Type 9 (Asset management) regulated activities under the Securities and Futures Ordinance. / Mr. Zhao Jun is the founder and the ultimate beneficial owner of Springs Capital (Hong Kong), / and Springs Capital 

### col_BC
  - p32: 2025, being the end date of our latest consolidated financial statements, and there has been no / event since September 30, 2025 that would materially affect the information shown in the / Accountants’ Report set out in Appendix I to this prospectus. / OUR CONTROLLING SHAREHOLDERS / Immediately following the completion of the Global Offering (assuming the Offer Size / Adjustment Option and the Ove
  - p50: “subsidiary(ies)” / has the meaning ascribed to it in section 15 of the / Companies Ordinance / “substantial shareholder(s)” / has the meaning ascribed to it in the Listing Rules / “Super Ming Group” / Super Ming Food Technology and its subsidiaries

### col_BD
  - p32: 2025, being the end date of our latest consolidated financial statements, and there has been no / event since September 30, 2025 that would materially affect the information shown in the / Accountants’ Report set out in Appendix I to this prospectus. / OUR CONTROLLING SHAREHOLDERS / Immediately following the completion of the Global Offering (assuming the Offer Size / Adjustment Option and the Ove
  - p32: Changsha Xunmang, Changsha Jianmang, Changsha Lingmang, Changsha Zhongmang, / Changsha Shizaimang, Shanghai Bird Nest and Yichun Yikouniao, through the act in concert / arrangement between Mr. Yan and Mr. Zhao, will be entitled to control the exercise of / approximately 57.76% of the voting rights at the general meetings of our Company. Therefore, / Mr. Yan, Mr. Zhao, Changsha Xunmang, Changsha Ji
  - p50: “subsidiary(ies)” / has the meaning ascribed to it in section 15 of the / Companies Ordinance / “substantial shareholder(s)” / has the meaning ascribed to it in the Listing Rules / “Super Ming Group” / Super Ming Food Technology and its subsidiaries

### col_BE
  - p316: In 2022, our net cash flows from financing activities were RMB200.7 million, mainly / attributable to capital injection of RMB220.7 million, mainly offset by a principal portion of / lease payments of RMB15.7 million. / INDEBTEDNESS / As of December 31, 2022, 2023, 2024, September 30, 2025 and November 30, 2025, our / indebtedness included lease liabilities and interest-bearing bank borrowings. Th
  - p28: prepayments, other receivables and other assets of RMB1,843.6 million, (ii) an increase in / inventories of RMB1,041.9 million, and (iii) an increase in cash and cash equivalents of / RMB215.1 million, partially offset by (i) an increase in trade payables of RMB892.9 million, / (ii) an increase in interest-bearing bank borrowings of RMB491.0 million, (iii) an increase in / other payables and accru
  - p28: prepayments, other receivables and other assets of RMB1,843.6 million, (ii) an increase in / inventories of RMB1,041.9 million, and (iii) an increase in cash and cash equivalents of / RMB215.1 million, partially offset by (i) an increase in trade payables of RMB892.9 million, / (ii) an increase in interest-bearing bank borrowings of RMB491.0 million, (iii) an increase in / other payables and accru

### col_BF
  - p88: and fluctuation of the market prices of other companies with business operations located / primarily in Mainland China that have listed their securities in Hong Kong may affect the / volatility in the price of and trading volumes for our H Shares. A number of Mainland / China-based companies have listed their securities, and some are in the process of preparing / for listing their securities, in H

### col_BG
  - p30: (4) / Gearing ratio equals total liabilities divided by total assets as of the end of the year/period and / multiplied by 100%. / USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$3,124 million based on the Offer Price of HK$233.10 per Offer Share (being the mid-point / of the stated range of the Offer Price between HK$229.60 and HK$236.
  - p318: the Track Record Period. Following the Global Offering, we will continue to incur capital / expenditures to grow our business. We plan to fund our planned capital expenditures mainly / with cash flows generated from our operations, bank borrowings, and the net proceeds received / from the Global Offering. See “Future Plans and Use of Proceeds.” We may adjust our capital / expenditures for any give

### col_BI
  - p2: Number of Offer Shares under / the Global Offering / : / 14,101,100 H Shares (subject to / the Offer Size Adjustment Option / and the Over-allotment Option) / Number of Hong Kong Offer Shares

### col_BP
  - p1: 湖南鳴鳴很忙商業連鎖股份有限公司 / BUSY MING GROUP CO., LTD. / Stock Code : 1768 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / GLOBAL OFFERING / Joint Sponsors, Joint Sponsor-Overall Coordinators, / Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers

### col_BR
  - p113: Yunda Central Plaza, 567 Changsha Avenue / Yuhua District, Changsha / Hunan Province, PRC / Principal Place of Business / in Hong Kong / 31/F, Tower Two / Times Square
  - p113: Registered Office / 33001-33006, Phase II Business Complex Building / Yunda Central Plaza, 567 Changsha Avenue / Yuhua District, Changsha
  - p113: Yunda Central Plaza, 567 Changsha Avenue / Yuhua District, Changsha / Hunan Province, PRC / Head Office and Principal Place / of Business in the PRC / 33001-33006, Phase II Business Complex Building / Yunda Central Plaza, 567 Changsha Avenue

### col_BT
  - p22: entirety by reference to, the historical financial information included in the Accountants’ / Report in Appendix I to this prospectus, including the accompanying notes, and the information / set forth in “Financial Information.” Our historical financial information was prepared in / accordance with IFRS Accounting Standards. / SUMMARY / – 12 –
  - p22: entirety by reference to, the historical financial information included in the Accountants’ / Report in Appendix I to this prospectus, including the accompanying notes, and the information / set forth in “Financial Information.” Our historical financial information was prepared in / accordance with IFRS Accounting Standards. / SUMMARY / – 12 –
  - p244: During the Track Record Period, we have duly booked all payments received under / Third-party Payment Arrangements according to our internal accounting policies and tax- / related laws and regulations. In 2022, 2023 and 2024, the aggregate amount of third-party / payments we received was RMB586.1 million, RMB541.0 million and RMB925.9 million, / respectively, representing 13.7%, 5.3% and 2.4% of o

### col_CC
  - p5: If there is any change in the following expected timetable, we will issue an / announcement / to / be
  - p5: at / http://www.busyming.com/ and the Hong Kong Stock Exchange at www.hkexnews.hk. / Date(1) / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on Tuesday, / January 20, 2026 / Latest time for completing electronic applications under / White Form eIPO service through the designated

### col_CD
  - p5: If there is any change in the following expected timetable, we will issue an / announcement / to / be

### col_CE
  - p4: of Hong Kong Offer Shares as set out in the table below. No application for any other number / of Hong Kong Offer Shares will be considered and such an application is liable to be rejected. / If you are applying through the White Form eIPO service, you may refer to the table / below for the amount payable for the number of H Shares you have selected. You must pay the / respective amount payable on

### col_CF
  - p23: (36,344,463) / (24,565,683) / (41,861,454) / Gross profit              / 319,351 / 772,339 / 2,999,048
  - p23: (36,344,463) / (24,565,683) / (41,861,454) / Gross profit              / 319,351 / 772,339 / 2,999,048

### col_CG
  - p57: • / our business operations and prospects; / • / our capital expenditure plans; / • / weather, natural disasters and climate change; / •
  - p57: • / our business operations and prospects; / • / our capital expenditure plans; / • / weather, natural disasters and climate change; / •
  - p318: CAPITAL COMMITMENTS / In 2022, 2023, 2024 and the nine months ended September 30, 2025, our capital / commitments were nil, RMB19.4 million, RMB167.3 million and RMB107.2 million, / respectively, which comprised purchase of property, plant and equipment that has been / contracted but not yet paid for. / FINANCIAL INFORMATION / – 308 –

### col_CH
  - p396: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the / accountants’ report, a true and fair view of the financial position of the Group and the Company / as at 31 December 2022, 2023 and 2024 and 30 September 2025 and of the financial / perfor
  - p22: SUMMARY OF HISTORICAL FINANCIAL INFORMATION / The following tables present our historical financial information for the years/periods or / as of the dates indicated. This summary has been derived from our historical financial / information set forth in the Accountants’ Report in Appendix I to this prospectus. The summary / historical financial data set forth below should be read together with, and

### col_CI
  - p24: measure may be defined differently from similar terms used by other companies, and may not / be comparable to other similarly titled measures used by other companies. / We define adjusted net profit (non-IFRS measures) as profit for the year/period adjusted / by adding back share-based payment expenses and listing expenses. The following table / reconciles our adjusted net profit (non-IFRS measure
  - p24: measure may be defined differently from similar terms used by other companies, and may not / be comparable to other similarly titled measures used by other companies. / We define adjusted net profit (non-IFRS measures) as profit for the year/period adjusted / by adding back share-based payment expenses and listing expenses. The following table / reconciles our adjusted net profit (non-IFRS measure


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 1768.HK`
有 ERROR 必须回原文修正。
