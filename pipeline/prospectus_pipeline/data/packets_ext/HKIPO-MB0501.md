# 0501.HK 扩展 18 列抽取包

公司：0501.HK OmniVision Integrated Circuits Group, Inc. - H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB0501.json`。
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
- 股本结构（**已确认，不要改**）：L=1255474412 M=45800000 N=1209674412 O=1209674412 P=0 Q=45800000 R=41220000 S=4580000
- 财务期间（**已确认**）：year-1 期末 = 30/06/25；币种 = RMB；year-1 净利 = 4040786000
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
{"code":"0501.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  0501.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 0501.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
（锚点无命中，需要自己 search）

### col_BB
  - p27: capital for the development and expansion of our global business, further strengthen our business / profile and market position in the industry, and better attract overseas investors and talents. / See “Business—Our Strategies” and “Future Plans and Use of Proceeds” for more details. / OUR CONTROLLING SHAREHOLDERS / Mr. YU Renrong is the founder of our Group, the chairman of the Board of Directors
  - p40: “Strategy and Development / Committee” / the strategy and development committee of the Board / “substantial shareholder(s)” / has the meaning ascribed to it in the Listing Rules / “Superpix Technology” / Superpix Technology (Hong Kong) Limited (思比科（香
  - p89: As of the Latest Practicable Date, each of Mr. YU Renrong and Shaoxing Weihao Management has / pledged 171,790,000 A Shares, representing approximately 14.20% of the total issued share capital of / our Company, and 15,856,000 A Shares, representing approximately 1.31% of the total issued share / capital of our Company, respectively. Mr. YU Renrong is the ultimate beneficial owner of the general / 

### col_BC
  - p27: capital for the development and expansion of our global business, further strengthen our business / profile and market position in the industry, and better attract overseas investors and talents. / See “Business—Our Strategies” and “Future Plans and Use of Proceeds” for more details. / OUR CONTROLLING SHAREHOLDERS / Mr. YU Renrong is the founder of our Group, the chairman of the Board of Directors
  - p40: “Strategy and Development / Committee” / the strategy and development committee of the Board / “substantial shareholder(s)” / has the meaning ascribed to it in the Listing Rules / “Superpix Technology” / Superpix Technology (Hong Kong) Limited (思比科（香

### col_BD
  - p27: capital for the development and expansion of our global business, further strengthen our business / profile and market position in the industry, and better attract overseas investors and talents. / See “Business—Our Strategies” and “Future Plans and Use of Proceeds” for more details. / OUR CONTROLLING SHAREHOLDERS / Mr. YU Renrong is the founder of our Group, the chairman of the Board of Directors
  - p107: will participate only as either cornerstone investors or placees (but not both) in the International / Offering (together, the “Existing Minority Shareholders”) on the conditions that each of them: / (a) / together with their close associates, holds less than 5% of the voting rights in our / Company prior to the completion of the Global Offering; / (b) / is not and will not become a core connected
  - p40: “Strategy and Development / Committee” / the strategy and development committee of the Board / “substantial shareholder(s)” / has the meaning ascribed to it in the Listing Rules / “Superpix Technology” / Superpix Technology (Hong Kong) Limited (思比科（香

### col_BE
  - p78: reduction in our customers’ sales, default by our customers, a prolonged delay in the payment of trade / receivables or the extension of payment terms for our customers could adversely affect our cash flow, / liquidity, business, financial condition and results of operations. / Failure to comply with the terms of our indebtedness or enforcement of our obligations under any / guarantee or other sim
  - p360: entities. / Cash flow and fair value interest rate risk / Our income and operating cash flows are substantially independent from changes in market / interest rates and we have no significant interest-bearing assets except for cash and cash equivalents / and restricted cash, details of which have been disclosed in Note 28 of the Accountants’ Report in / Appendix I to this document, respectively. / 
  - p20: Our net current assets increased from RMB14.3 billion as of June 30, 2025 to RMB16.8 billion / of October 31, 2025, mainly due to (i) an increase in cash and cash equivalents of RMB1.7 billion and / (ii) an increase in inventories of RMB280.0 million, partially offset by (i) an increase in current / borrowings / of / RMB526.4 / million

### col_BF
  - p197: recognition and reputation. According to Frost & Sullivan, we are the third largest CIS providers, with / a market share of 13.7%, the world’s third largest smartphone CIS provider with a market share of / 10.5% and the largest automotive CIS provider with a market share of 32.9%, by revenue in 2024. We / are also a leader in the world to commercialize BSI technology for the CIS industry. / With a
  - p13: primarily on promoting the advantages of a single chip image sensor and supporting our customers at / industry trade shows around the world. We work extensively with our customer’s management and / engineers to help optimize our solution. After granting a design win, our customer will then decide / when to start mass production for the specific product based on various factors including the / comp
  - p417: 3 / The amendments shall be applied prospectively to sale or contribution of assets occurring in annual periods beginning on or after a date / to be determined. / The Group is in the process of making an assessment of the impact of these new and amended / standards upon initial application. The adoption of IFRS 18 will not affect the recognition or / measurement of items in the consolidated financ

### col_BG
  - p27: Our Company seeks to be listed on the Hong Kong Stock Exchange in order to provide further / capital for the development and expansion of our global business, further strengthen our business / profile and market position in the industry, and better attract overseas investors and talents. / See “Business—Our Strategies” and “Future Plans and Use of Proceeds” for more details. / OUR CONTROLLING SHAR
  - p22: ended June 30, 2025, supported by the growth in both semiconductor design and sales and / semiconductor distribution business lines and our continuous cost management efforts. / Our gearing ratio as of December 31, 2023 significantly decreased as compared to December 31, / 2022, reflecting the substantial improvement of our cash flow and repayment of borrowings in 2023. As / of December 31, 2024 a
  - p27: Our Company seeks to be listed on the Hong Kong Stock Exchange in order to provide further / capital for the development and expansion of our global business, further strengthen our business / profile and market position in the industry, and better attract overseas investors and talents. / See “Business—Our Strategies” and “Future Plans and Use of Proceeds” for more details. / OUR CONTROLLING SHAR

### col_BI
  - p2: GLOBAL OFFERING / Number of Offer Shares under the Global Offering / : / 45,800,000 H Shares (subject to the Over-allotment / Option) / Number of Hong Kong Offer Shares / :

### col_BP
  - p31: the audit committee of the Board / “Beijing Jinghongzhi” / Beijing Jinghongzhi Technology Co., Ltd. (北京京鴻志科技 / 有限公司), a company established on September 10, 2001 / in the PRC, one of our Major Subsidiaries / “Beijing OmniVision” / Beijing OmniVision Technologies Company Limited (北京
  - p1: Joint Lead Manager / GLOBAL / OFFERING / (A joint stock company incorporated in the People’s Republic of China with limited liability) / Stock code: 佾侃佾使 / OmniVision Integrated Circuits Group, Inc. / 豪威集成電路(集團)股份有限公司

### col_BR
  - p122: Pilot Free Trade Zone / Shanghai / PRC / Principal Place of Business in / Hong Kong / Room 1912, 19/F, Lee Garden One / 33 Hysan Avenue
  - p122: CORPORATE INFORMATION / Registered Office / 7/F, Building C, Block 1 / No. 3000 Longdong Avenue / Pilot Free Trade Zone

### col_BT
  - p297: for the six months ended June 30, 2025. / BASIS OF PREPARATION / The principal accounting policies applied in the preparation of our historical financial / information are in accordance with all applicable IFRS Accounting Standards, which collective term / includes all applicable individual IFRS, International Accounting Standards and Interpretations issued / by International Accounting Standards 
  - p35: 2020 in the PRC, one of our Major Subsidiaries / “IFRS” / International Financial Reporting Standards, as issued by / the International Accounting Standards Board / “Independent Third Party(ies)” / person(s) or company(ies) who/which, to the best of our / Directors’ knowledge, information and belief, is/are not our
  - p67: provision for impairment and an impairment loss are recognized for the amount by which the asset’s / carrying amount exceeds its recoverable amount. The recoverable amount is the higher of an asset’s / fair value less costs to sell and the present value of the asset’s estimated future cash flows. See / “Financial Information—Material Accounting Policies and Critical Accounting Estimates and / Judg

### col_CC
  - p5: EXPECTED TIMETABLE(1) / If there is any change in the following expected timetable of the Hong Kong Public / Offering, our Company will issue an announcement to be published on the website of the Stock / Exchange at www.hkexnews.hk and the website of our Company at www.omnivision-
  - p5: Exchange at www.hkexnews.hk and the website of our Company at www.omnivision- / group.com. / Date(1) / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . / 9:00 a.m. on / Wednesday, December 31, 2025 / Latest time to complete electronic applications under the HK eIPO

### col_CD
  - p5: EXPECTED TIMETABLE(1) / If there is any change in the following expected timetable of the Hong Kong Public / Offering, our Company will issue an announcement to be published on the website of the Stock / Exchange at www.hkexnews.hk and the website of our Company at www.omnivision-

### col_CE
  - p112: APPLICATION FOR LISTING OF THE H SHARES ON THE HONG KONG STOCK / EXCHANGE / We have applied to the Hong Kong Stock Exchange for the granting of listing of, and / permission to deal in, our H Shares to be issued pursuant to the Global Offering (including any / H Shares which may be issued pursuant to the exercise of the Over-allotment Option). Dealings in the / H Shares on the Hong Kong Stock Excha
  - p3: Hong Kong Offer Shares as set out in the table below. No application for any other number of Hong / Kong Offer Shares will be considered and such an application is liable to be rejected. / If you are applying through the HK eIPO White Form service, you may refer to the table / below for the amount payable for the number of H Shares you have selected. You must pay the / respective maximum amount pa

### col_CF
  - p14: (71.8) / (9,818.1) / (70.4) / Gross profit . . . . . . . . . . . . . . . . . . . . . . . . / 4,741.2 / 23.7 / 4,183.5
  - p14: (71.8) / (9,818.1) / (70.4) / Gross profit . . . . . . . . . . . . . . . . . . . . . . . . / 4,741.2 / 23.7 / 4,183.5

### col_CG
  - p9: partnerships, and (iii) the ability to quickly adapt to market demands while achieving higher production / efficiency. In markets where technology evolves rapidly and semiconductor innovation drives / continuous advancement, our fabless model enables us to respond swiftly to shifting market demands / without incurring substantial capital expenditures. This flexibility allows us to upgrade our tech
  - p9: partnerships, and (iii) the ability to quickly adapt to market demands while achieving higher production / efficiency. In markets where technology evolves rapidly and semiconductor innovation drives / continuous advancement, our fabless model enables us to respond swiftly to shifting market demands / without incurring substantial capital expenditures. This flexibility allows us to upgrade our tech
  - p437: assurance that the grant will be received and the Group will comply with all attached conditions. / Government grants relating to costs are deferred and recognized in the profit or loss over the / period necessary to match them with the costs that they are intended to compensate. / Government grants relating to the purchase of property, plant and equipment are included in / non-current liabilities

### col_CH
  - p404: We believe that the evidence we have obtained is sufficient and appropriate to provide a basis / for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the accountants’ / report, a true and fair view of the financial position of the Company as at December 31, 2022, 2023 / and 2024 and June 30, 2025 and the consolidated financial position of the
  - p14: was also a supplier/customer. / SUMMARY OF HISTORICAL FINANCIAL INFORMATION / The following tables set forth summary financial data from our financial information during the / Track Record Period, extracted from the Accountants’ Report set out in Appendix I to this document. / The summary financial data set forth below should be read together with, and is qualified in its entirety / by reference t

### col_CI
  - p29: paid a total amount of RMB264.5 million on August 1, 2025 out of our distributable profits. We further / declared the 2025 interim dividend on October 28, 2025 and paid a total amount of RMB482.2 million / on November 24, 2025 out of our distributable profits. / LISTING EXPENSES / Assuming the Over-allotment Option is not exercised, the maximum Offer Price of HK$104.80 / per Offer Share and the fu
  - p29: paid a total amount of RMB264.5 million on August 1, 2025 out of our distributable profits. We further / declared the 2025 interim dividend on October 28, 2025 and paid a total amount of RMB482.2 million / on November 24, 2025 out of our distributable profits. / LISTING EXPENSES / Assuming the Over-allotment Option is not exercised, the maximum Offer Price of HK$104.80 / per Offer Share and the fu
  - p375: H Shares, representing not more than 15% of the number of Offer Shares initially available under the / Global Offering, at the Offer Price, to cover over-allocations in the International Offering, if any. See / “Structure of the Global Offering — Over-allotment Option.” / UNDERWRITING COMMISSIONS AND LISTING EXPENSES / The Underwriters and the Capital Market Intermediaries will receive an underwri


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 0501.HK`
有 ERROR 必须回原文修正。
