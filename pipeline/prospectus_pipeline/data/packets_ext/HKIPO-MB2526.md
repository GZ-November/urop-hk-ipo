# 2526.HK 扩展 18 列抽取包

公司：2526.HK Hangzhou Diagens Biotechnology Co., Ltd. - B - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB2526.json`。
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
- 股本结构（**已确认，不要改**）：L=88879200 M=7999200 N=80880000 O=80880000 P=0 Q=7999200 R=7199250 S=799950
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = -48865333.333333336
- 行业分类（港交所官方）：282010 醫療設備及用品
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
{"code":"2526.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  2526.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 2526.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p27: total issued shares, and hence they will continue to be a group of Controlling Shareholders. For / details, please see section headed “Relationship With Our Controlling Shareholders” in this / prospectus. / PRE-IPO INVESTMENTS / Our Company received ten rounds of investments from the Pre-IPO Investors through / subscriptions for increased registered capital of our Company in a total amount of appr
  - p27: details, please see section headed “Relationship With Our Controlling Shareholders” in this / prospectus. / PRE-IPO INVESTMENTS / Our Company received ten rounds of investments from the Pre-IPO Investors through / subscriptions for increased registered capital of our Company in a total amount of approximately / RMB397 million. The valuation of our Company upon completion of the last round of the /
  - p27: total issued shares, and hence they will continue to be a group of Controlling Shareholders. For / details, please see section headed “Relationship With Our Controlling Shareholders” in this / prospectus. / PRE-IPO INVESTMENTS / Our Company received ten rounds of investments from the Pre-IPO Investors through / subscriptions for increased registered capital of our Company in a total amount of appr

### col_BB
  - p26: million, will be allocated to pursue strategic collaboration and investment opportunities in upstream / and downstream players in the healthcare value chain. See “Future Plans and Use of Proceeds” for / further details. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Dr. Song was able to exercise voting rights attached to / 42,102,157 Shares, representing approximately 52.06% o
  - p35: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Takeovers Code” / the Code on Takeovers and Mergers and Share Buy-backs
  - p136: following the completion of the Global Offering, respectively. The background information of our / existing Pre-IPO Investors is set out below. To the best knowledge of our Directors, save as / disclosed, each of our Pre-IPO Investors and where applicable, their respective general partner(s), / limited partner(s) and ultimate beneficial owner(s) is an Independent Third Party. / Diagens Nuoda, Deqi

### col_BC
  - p26: million, will be allocated to pursue strategic collaboration and investment opportunities in upstream / and downstream players in the healthcare value chain. See “Future Plans and Use of Proceeds” for / further details. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Dr. Song was able to exercise voting rights attached to / 42,102,157 Shares, representing approximately 52.06% o
  - p35: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Takeovers Code” / the Code on Takeovers and Mergers and Share Buy-backs

### col_BD
  - p26: million, will be allocated to pursue strategic collaboration and investment opportunities in upstream / and downstream players in the healthcare value chain. See “Future Plans and Use of Proceeds” for / further details. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Dr. Song was able to exercise voting rights attached to / 42,102,157 Shares, representing approximately 52.06% o
  - p26: and downstream players in the healthcare value chain. See “Future Plans and Use of Proceeds” for / further details. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Dr. Song was able to exercise voting rights attached to / 42,102,157 Shares, representing approximately 52.06% of the voting rights in our Company through / (i) his personal capacity as to 24,293,507 Shares, represen
  - p35: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Takeovers Code” / the Code on Takeovers and Mergers and Share Buy-backs

### col_BE
  - p60: materially affected. Going forward, from time to time, we may evaluate various investment / opportunities, including investment in other associates or joint ventures in relation to associates. / Any future investment in associates may entail numerous risks, such as increased cash requirements / and additional indebtedness or contingent or unforeseen liabilities. / RISK FACTORS / – 51 –
  - p23: deferred listing expenses as of September 30, 2025 in relation to the Global Offering. Our net / current assets decreased from RMB106.9 million as of December 31, 2023 to RMB90.5 million as / of December 31, 2024, primarily due to (i) the decrease in our inventories as a result of our effort / to optimize our management of inventory level; and (ii) the interest-bearing bank loans we incurred / to 
  - p270: 30, 2025, as we repaid part our interest-bearing bank loans. As of January 31, 2026, we had / RMB141.9 million of committed unutilized banking facilities. / Our Directors confirm that we have not defaulted in the repayment of the bank loans and other / borrowings during the Track Record Period. Our Directors have confirmed that, as of the Latest / Practicable Date, there was no material covenant o

### col_BF
  - p10: imaging products and services. We have self-developed a diversified portfolio that can effectively / enhance diagnostic efficiency and service quality, which comprises: (i) six medical imaging / software products, including our Core Product, AI AutoVision®, which is at the registration stage, / one commercialized product, AutoVision®, as well as four pre-clinical stage product candidates; (ii) / t
  - p20: units, which are sufficient to meet the current market demands. Since the end of the Track Record / Period, we have reduced the number of our production lines from nine to four due to the termination / of lease of the Jian Space Production Base, with all five reduced production lines focusing on the / manufacturing of medical consumables and medical reagents. We are currently in the process of / e

### col_BG
  - p26: We believe that the level of such fees and expenses are in line with market level and are not / unusually high. The aforementioned listing expenses are the latest practicable estimates by us and / are provided for reference only and the actual amounts may differ. / USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$762.9 million, after de
  - p26: capabilities and market penetration in China; (v) approximately 5.0%, or HK$38.2 million, will be / allocated to expand our presence in global markets; and (vi) approximately 8.0%, or HK$61.0 / million, will be allocated to pursue strategic collaboration and investment opportunities in upstream / and downstream players in the healthcare value chain. See “Future Plans and Use of Proceeds” for / fur

### col_BI
  - p241: Total                                    / 88,879,200 / 100.00 / SHARE CLASSES / Upon completion of the Global Offering and conversion of 80,880,000 Unlisted Shares into / H Shares, our Shares will consist of Unlisted Shares and H Shares. Both Unlisted Shares and H / Shares are ordinary shares in the share capital of our Company. Apart from certain qualified
  - p2: Number of Offer Shares under / the Global Offering / : / 7,999,200 H Shares / Number of Hong Kong Offer Shares / : / 799,950 H Shares (subject to

### col_BP
  - p20: other medical institutions, to ensure that the products enter the target market efficiently. See / “Business — Commercialization and Sales — Product sales” in this prospectus. / MANUFACTURING / As of the Latest Practicable Date, we have established one production facility located in / Hangzhou, Zhejiang Province, namely the Smart Health Valley Production Base, with 18 / manufacturing personnel and
  - p1: GLOBAL OFFERING / Stock Code : 02526 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / 杭州德適生物科技股份有限公司 / Hangzhou Diagens Biotechnology Co., Ltd. / Sole Sponsor, Sponsor-overall Coordinator, Overall Coordinator,

### col_BR
  - p91: Registered Office, Headquarters and / Principal Place of Business in the PRC / Room 101, Building 1 / No. 609 Hongfeng Road / Donghu Sub-district, Linping District
  - p91: Registered Office, Headquarters and / Principal Place of Business in the PRC / Room 101, Building 1 / No. 609 Hongfeng Road

### col_BT
  - p21: Appendix I to this prospectus. The summary financial data set forth below should be read together / with, and is qualified in its entirety by reference to, the consolidated financial statements in this / prospectus, including the related notes. Our consolidated financial information was prepared in / accordance with HKFRS Accounting Standards. / Summary of Consolidated Statements of Profit or Loss
  - p21: Appendix I to this prospectus. The summary financial data set forth below should be read together / with, and is qualified in its entirety by reference to, the consolidated financial statements in this / prospectus, including the related notes. Our consolidated financial information was prepared in / accordance with HKFRS Accounting Standards. / Summary of Consolidated Statements of Profit or Loss
  - p245: MATERIAL ACCOUNTING POLICIES AND SIGNIFICANT ACCOUNTING JUDGMENTS / AND ESTIMATES / We have identified certain accounting policies that are significant to the preparation of our / consolidated financial statements. Some of our accounting policies involve subjective assumptions

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on our Company’s / website at www.diagens.com and the website of the Hong Kong Stock Exchange at / www.hkexnews.hk.
  - p5: Offering, we will issue an announcement in Hong Kong to be published on our Company’s / website at www.diagens.com and the website of the Hong Kong Stock Exchange at / www.hkexnews.hk. / Hong Kong Public Offering commences / . . . . . . . . . . . . . .9:00 a.m. on Friday, March 20, 2026 / Latest time to complete electronic applications under / White Form eIPO service through the designated

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on our Company’s / website at www.diagens.com and the website of the Hong Kong Stock Exchange at / www.hkexnews.hk.

### col_CE
  - p82: APPLICATION FOR LISTING OF THE H SHARES ON THE HONG KONG STOCK / EXCHANGE / We have applied to the Hong Kong Stock Exchange for the granting of listing of, and / permission to deal in, our H Shares to be issued pursuant to the Global Offering and the H Shares / to be converted from Unlisted Shares. / No part of our Shares or loan capital is listed on or dealt in on any other stock exchange, and / 
  - p70: future. / In addition, our Unlisted Shares may be converted into H Shares subject to regulatory / approvals and compliance with relevant regulatory requirements. Any conversion of our Unlisted / Shares will increase the number of H Shares available on the market and may affect the trading / price of our H Shares. / The interests of our Controlling Shareholders may not be aligned with the interest 

### col_CF
  - p21: (57.1) / (26,947) / (24.1) / Gross profit             / 37,495 / 71.0 / 46,061
  - p21: (57.1) / (26,947) / (24.1) / Gross profit             / 37,495 / 71.0 / 46,061

### col_CG
  - p25: to cast reasonable doubt on the Directors’ view as set out above. For detailed analysis of on / fluctuations of our cash flow items, see “Financial Information”. / Our cash burn rate refers to our average monthly (i) net cash used in operating activities, (ii) / capital expenditures and (iii) lease payments. Assuming an average cash burn rate going forward of / 1.1 times the level in 2024, we esti
  - p25: to cast reasonable doubt on the Directors’ view as set out above. For detailed analysis of on / fluctuations of our cash flow items, see “Financial Information”. / Our cash burn rate refers to our average monthly (i) net cash used in operating activities, (ii) / capital expenditures and (iii) lease payments. Assuming an average cash burn rate going forward of / 1.1 times the level in 2024, we esti

### col_CH
  - p311: We believe that the evidence we have obtained is sufficient and appropriate to provide a basis / for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the accountants’ / report, a true and fair view of the financial position of the Group and the Company as at 31 / December 2023 and 2024 and 30 September 2025 and of the financial performance an
  - p21: associates had any interest in any of our five largest customers. / SUMMARY OF HISTORICAL FINANCIAL INFORMATION / The following tables set forth summary financial data from our consolidated financial / information for the Track Record Period, extracted from the Accountants’ Report set out in / Appendix I to this prospectus. The summary financial data set forth below should be read together / with,

### col_CI
  - p23: prepayments, other receivables and other assets as a result of (i) an increase in prepayments / primarily due to our procurement of computing power services for R&D needs of our iMedImage® / foundation model to further improve the operational efficiency of AI AutoVision®, and (ii) the / deferred listing expenses as of September 30, 2025 in relation to the Global Offering. Our net / current assets 
  - p23: prepayments, other receivables and other assets as a result of (i) an increase in prepayments / primarily due to our procurement of computing power services for R&D needs of our iMedImage® / foundation model to further improve the operational efficiency of AI AutoVision®, and (ii) the / deferred listing expenses as of September 30, 2025 in relation to the Global Offering. Our net / current assets 


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 2526.HK`
有 ERROR 必须回原文修正。
