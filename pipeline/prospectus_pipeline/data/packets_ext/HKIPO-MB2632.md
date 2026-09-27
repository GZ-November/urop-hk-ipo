# 2632.HK 扩展 18 列抽取包

公司：2632.HK Jiangsu New Vision Automotive Electronics Co., Ltd. - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB2632.json`。
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
- 股本结构（**已确认，不要改**）：L=123395266 M=16226500 N=107168766 O=107168766 P=0 Q=16226500 R=14603850 S=1622650
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = -458246666.6666667
- 行业分类（港交所官方）：231020 汽車零件
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
{"code":"2632.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  2632.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 2632.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p26: million, RMB994.3 million, RMB1,360.9 million and RMB1,667.9 million as of December 31, / 2022, 2023 and 2024 and September 30, 2025, respectively. Our redemption liabilities on / equity shares primarily represent the preferred shares we issued in our Pre-IPO financing. See / “History, Development and Corporate Structure — Pre-IPO Investments.” Our preferred shares / will be re-designated from lia
  - p37: a / limited / partnership established in PRC on July 13, 2021, one of / our Pre-IPO Investors, the details of which are set out in / “History, Development and Corporate Structure” / “Articles of Association” or / “Articles”
  - p26: million, RMB994.3 million, RMB1,360.9 million and RMB1,667.9 million as of December 31, / 2022, 2023 and 2024 and September 30, 2025, respectively. Our redemption liabilities on / equity shares primarily represent the preferred shares we issued in our Pre-IPO financing. See / “History, Development and Corporate Structure — Pre-IPO Investments.” Our preferred shares / will be re-designated from lia

### col_BB
  - p26: Our net liabilities increased from RMB897.4 million as of December 31, 2024 to / RMB1,236.0 million as of September 30, 2025, primarily due to the loss for the period of / RMB343.7 million, partially offset by (i) the share-based payment of RMB3.0 million, and (ii) / the capital injection from non-controlling shareholders of RMB2.2 million. / As of December 31, 2022, 2023 and 2024 and September 30
  - p54: “%” / per cent / In this Prospectus, the terms “associate,” “close associate,” “connected person,” “core / connected person,” “connected transaction” and “substantial shareholder” shall have the / meanings given to such terms in the Hong Kong Listing Rules, unless the context otherwise / requires. / DEFINITIONS
  - p538: The Listing does not take place prior to 31 December 2027; or / (b) / Any change in the Company’s de facto control occurs, or instability arises in the Company’s equity or / controlling shareholders’ ownership due to marriage, inheritance (or their ultimate beneficial owners, if / such shareholders are legal entities), thereby creating material obstacles or risks to the Company’s IPO; / or / (c)

### col_BC
  - p26: Our net liabilities increased from RMB897.4 million as of December 31, 2024 to / RMB1,236.0 million as of September 30, 2025, primarily due to the loss for the period of / RMB343.7 million, partially offset by (i) the share-based payment of RMB3.0 million, and (ii) / the capital injection from non-controlling shareholders of RMB2.2 million. / As of December 31, 2022, 2023 and 2024 and September 30
  - p54: “%” / per cent / In this Prospectus, the terms “associate,” “close associate,” “connected person,” “core / connected person,” “connected transaction” and “substantial shareholder” shall have the / meanings given to such terms in the Hong Kong Listing Rules, unless the context otherwise / requires. / DEFINITIONS

### col_BD
  - p26: Our net liabilities increased from RMB897.4 million as of December 31, 2024 to / RMB1,236.0 million as of September 30, 2025, primarily due to the loss for the period of / RMB343.7 million, partially offset by (i) the share-based payment of RMB3.0 million, and (ii) / the capital injection from non-controlling shareholders of RMB2.2 million. / As of December 31, 2022, 2023 and 2024 and September 30
  - p117: and consent under Paragraph 1C(2) of Appendix F1 to the Listing Rules for subscriptions of / Close Associates of Offer Shares as Cornerstone Investors on the conditions that: / (a) / Shunyi State Investment holds less than 5% of the total voting rights in our / Company before Listing; / (b) / Shunyi State Investment is not, and will not be, a core connected person of our
  - p54: “%” / per cent / In this Prospectus, the terms “associate,” “close associate,” “connected person,” “core / connected person,” “connected transaction” and “substantial shareholder” shall have the / meanings given to such terms in the Hong Kong Listing Rules, unless the context otherwise / requires. / DEFINITIONS

### col_BE
  - p421: INDEBTEDNESS / As of December 31, 2022, 2023 and 2024, September 30, 2025 and January 31, 2026, our / indebtedness consisted of lease liabilities, interest-bearing bank and other borrowings and / redemption liabilities on equity shares. As of January 31, 2026, we had a total indebtedness of
  - p25: Our net current liabilities increased by 30.5% from RMB740.1 million as of December / 31, 2023 to RMB966.0 million as of December 31, 2024, primarily due to (i) an increase in / redemption liabilities on equity shares of RMB366.6 million, which represents the preferred / shares issued in our Pre-IPO financing, (ii) an increase in interest-bearing bank and other / borrowings of RMB49.1 million, pri
  - p25: 31, 2023 to RMB966.0 million as of December 31, 2024, primarily due to (i) an increase in / redemption liabilities on equity shares of RMB366.6 million, which represents the preferred / shares issued in our Pre-IPO financing, (ii) an increase in interest-bearing bank and other / borrowings of RMB49.1 million, primarily to support our day-to-day operations and / anticipated business growth, and (ii

### col_BF
  - p34: expansion, and (b) an increase in our testing and design expenses as a result of our increased / R&D activities. These R&D activities are intended to benefit our long-term growth and we / expected our R&D expenses to gradually stabilize as key R&D programs progress toward / commercialization. We also expect that our successful R&D initiatives will help to improve our / profitability over time by e
  - p16: further innovate building upon our existing R&D achievements. Our development / tools enable automated adjustments, which effectively reduces coordination costs in / development and production processes, allows rapid development and adaptation / and maximizes solution development and mass production delivery efficiency. / Currently, we can achieve delivery cycles as short as 10 months, far below t
  - p101: which came into effect on March 31, 2023, requiring that, in the process of overseas issuance / and listing of securities by domestic entities, the domestic entities, and securities companies / and securities service institutions that provide relevant securities service shall strictly / implement the provisions of relevant laws and regulations and the requirements of these

### col_BG
  - p29: USE OF PROCEEDS / Please see “Future Plans and Use of Proceeds” for a detailed discussion of our future / plans. / We estimate that the net proceeds which we will receive, assuming an Offer Price of
  - p29: USE OF PROCEEDS / Please see “Future Plans and Use of Proceeds” for a detailed discussion of our future / plans. / We estimate that the net proceeds which we will receive, assuming an Offer Price of / HK$45.00 per H Share (being the mid-point of the indicative Offer Price range of HK$42.00

### col_BI
  - p2: Number of Offer Shares under the / Global Offering / : / 16,226,500 H Shares / Number of Hong Kong Offer Shares / : / 1,622,650 H Shares (subject to

### col_BP
  - p1: GLOBAL OFFERING / (A joint stock company incorporated in the People’s Republic of China with limited liability) / 江蘇澤景汽車電子股份有限公司 / JIANGSU NEW VISION AUTOMOTIVE ELECTRONICS CO., LTD. / Stock Code : 2632

### col_BR
  - p129: 3 Tianyue Road, Automobile Industry Park / Yizheng, Yangzhou, Jiangsu Province / PRC / Principal Place of Business in Hong Kong / Room 1918, 19/F / Lee Garden One / 33 Hysan Avenue
  - p122: All H Shares issued pursuant to applications made in the Hong Kong Public Offering and / the International Offering will be registered on the Company’s H Share register of members to / be maintained by our H Share Registrar, Tricor Investor Services Limited, in Hong Kong. We / will maintain the Company’s principal register of members at our current registered office in / the PRC. / Dealings in our

### col_BT
  - p494: No audited financial statements have been prepared for these entities since their dates of incorporation. / 2.1 / BASIS OF PREPARATION / The Historical Financial Information has been prepared in accordance with IFRS Accounting Standards, which / comprise all standards and Interpretations approved by the International Accounting Standards Board (“IASB”). All / IFRS Accounting Standards effective fo
  - p43: amendments / and / interpretations / promulgated by the International Accounting Standards / Board and the International Accounting Standards and / interpretation issued by the International Accounting / Standards Committee
  - p325: continually review the implementation of our risk management and internal control policies / and procedures to enhance their effectiveness and sufficiency. / Financial Reporting Risk Management / We have in place a set of accounting policies in connection with our financial reporting / risk management, such as financial reporting management policies, budget management / policies and financial stat

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong on the websites of the Stock / Exchange at www.hkexnews.hk and our Company at www.zjautomotive.com. / Hong Kong Public Offering commences . . . . . . . . . . . . .9:00 a.m. Monday, March 16, 2026
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong on the websites of the Stock / Exchange at www.hkexnews.hk and our Company at www.zjautomotive.com. / Hong Kong Public Offering commences . . . . . . . . . . . . .9:00 a.m. Monday, March 16, 2026 / Latest time for completing electronic applications / under the H

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong on the websites of the Stock / Exchange at www.hkexnews.hk and our Company at www.zjautomotive.com. / Hong Kong Public Offering commences . . . . . . . . . . . . .9:00 a.m. Monday, March 16, 2026

### col_CE
  - p120: prospectus. / APPLICATION FOR LISTING ON THE HONG KONG STOCK EXCHANGE / We have applied to the Listing Committee for the granting of listing of, and permission / to deal in, (i) our H Shares to be issued pursuant to the Global Offering, and (ii) the H Shares / to be converted from our existing Domestic Unlisted Shares. Dealings in the H Shares on the / Hong Kong Stock Exchange are expected to comm
  - p4: channel must be made for a minimum of 50 Hong Kong Offer Shares and in multiples of that / number of Hong Kong Offer Shares as set out in the table below. / If you are applying through the HK eIPO White Form service, you may refer to the table / below for the amount payable for the number of H Shares you have selected. You must pay the / respective maximum amount payable on application in full upo

### col_CF
  - p20: (72.7) / (365,027) / (76.1) / Gross profit         / 48,383 / 22.6 / 140,430
  - p20: (72.7) / (365,027) / (76.1) / Gross profit         / 48,383 / 22.6 / 140,430

### col_CG
  - p61: • / our business operations and prospects; / • / our capital expenditure plans; / • / weather, natural disasters and climate change; / •
  - p61: • / our business operations and prospects; / • / our capital expenditure plans; / • / weather, natural disasters and climate change; / •

### col_CH
  - p478: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the / accountants’ report, a true and fair view of the financial position of the Group and the Company / as at 31 December 2022, 2023 and 2024 and 30 September 2025 and of the financial / perfor
  - p19: SUMMARY OF HISTORICAL FINANCIAL INFORMATION / The following tables present our summary historical financial information for the periods / or as of the dates indicated. This summary has been derived from our historical financial / information set forth in the Accountants’ Report in Appendix I to this prospectus. The summary / historical financial data set forth below should be read together with, a

### col_CI
  - p23: for analysis of our results of operations or financial condition as reported under IFRSs. / We define adjusted (loss)/profit for the year/period (non-IFRS measure) as loss for the / year/period adjusted by adding back (i) fair value losses on redemption liabilities on equity / shares, (ii) share-based payment expenses and (iii) listing expenses. The following table / reconciles our adjusted (loss)
  - p23: for analysis of our results of operations or financial condition as reported under IFRSs. / We define adjusted (loss)/profit for the year/period (non-IFRS measure) as loss for the / year/period adjusted by adding back (i) fair value losses on redemption liabilities on equity / shares, (ii) share-based payment expenses and (iii) listing expenses. The following table / reconciles our adjusted (loss)


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 2632.HK`
有 ERROR 必须回原文修正。
