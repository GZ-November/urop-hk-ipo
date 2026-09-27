# 2714.HK 扩展 18 列抽取包

公司：2714.HK Muyuan Foods Co., Ltd. - H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB2714.json`。
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
- 股本结构（**已确认，不要改**）：L=5736722666 M=273951400 N=5462771266 O=5462771266 P=0 Q=273951400 R=246556200 S=27395200
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = 20149466666.666668
- 行业分类（港交所官方）：252010 禽畜肉類
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
{"code":"2714.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  2714.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 2714.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
（锚点无命中，需要自己 search）

### col_BB
  - p37: competitive industry and may face increased competition. New competitors who enter the / market could have an adverse impact on our businesses and prospects; and (vi) we incurred net / losses in the past. / THE CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, our Controlling Shareholders Group, comprising Mr. / Qin Yinglin, Ms. Qian Ying and Muyuan Group, collectively held approximate
  - p50: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Track Record Period” / the financial years ended December 31, 2022, 2023 and
  - p343: approximately 1,700 employees located across Canada, the United States, Europe and Asia. / RBC Global Asset Management (U.S.) Inc., a wholly owned subsidiary of Royal Bank of / Canada, is the sole beneficial owner of 100% of the outstanding shares of the RBC China / Equity Fund (40 Act). To the best of its knowledge, no single ultimate beneficial owner is / holding 30% or more interests in (i) RBC

### col_BC
  - p37: competitive industry and may face increased competition. New competitors who enter the / market could have an adverse impact on our businesses and prospects; and (vi) we incurred net / losses in the past. / THE CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, our Controlling Shareholders Group, comprising Mr. / Qin Yinglin, Ms. Qian Ying and Muyuan Group, collectively held approximate
  - p50: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Track Record Period” / the financial years ended December 31, 2022, 2023 and
  - p304: For our Directors’ interest in our Shares within the meaning of Part XV of the SFO, see / “Appendix VI. Statutory and General Information — 3. Further Information about Our / Directors and Substantial Shareholders — C. Disclosure of Interests — (b) Disclosure of / Interests of Directors and Chief Executive” in Appendix VI to this prospectus.

### col_BD
  - p37: competitive industry and may face increased competition. New competitors who enter the / market could have an adverse impact on our businesses and prospects; and (vi) we incurred net / losses in the past. / THE CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, our Controlling Shareholders Group, comprising Mr. / Qin Yinglin, Ms. Qian Ying and Muyuan Group, collectively held approximate
  - p37: THE CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, our Controlling Shareholders Group, comprising Mr. / Qin Yinglin, Ms. Qian Ying and Muyuan Group, collectively held approximately 54.91% of our / total share capital and controlled 55.62% of the voting rights in our Company. Immediately / following the completion of the Global Offering (assuming that the Over-allotment Option is / n
  - p50: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Track Record Period” / the financial years ended December 31, 2022, 2023 and

### col_BE
  - p78: We may require additional funding to finance our operations, which may not be available / on terms acceptable to us or at all. Our level of indebtedness and the terms of our / indebtedness could adversely affect our business and liquidity position. / We currently fund our operations principally with proceeds from our business operations / and bank and other borrowings. As of November 30, 2025, we 
  - p425: readily realizable marketable securities and adequate committed lines of facilities from major / financial institutions to meet its liquidity requirements in the short and longer term. / Interest Rate Risk / Interest-bearing financial instruments at fixed rates and at variable rates expose us to fair / value interest rate risk and cash flow interest risk, respectively. We determine the appropriate
  - p32: drawn to supplement our working capital when the hog prices was in downswing in 2023 as / part of our liquidity management efforts. We obtained short-term loans from time to time / during the Track Record Period, primarily to meet our working capital needs. Financial / institutions generally require sufficient collateral for medium- to long-term borrowings. / However, our assets, such as hogs and 

### col_BF
  - p13: challenges in the hog farming industry, including soybean meal reliance and / nitrogen emission. / – / In 2024, we commercialized ammonia reduction and deodorization solutions for / livestock farming, which were promoted by the PRC Ministry of Ecology and / Environment. / Through our proprietary innovations, we have solidified our leadership within the
  - p133: • / Technology Barrier. The hog farming industry is globally recognized as technology- / intensive. Advanced breeding technologies and breeding tools are important for hog / farming companies to ensure mass production of hogs with consistency, adaptability, and / high productivity. In parallel, they must upgrade in-house systems to standardize the / breeding / process
  - p151: preservatives, additives and other chemicals used in the process of packaging, preservation, / storage and transportation of agricultural products shall be in conformity with the relevant / mandatory national standards and other provisions on the quality and safety of agricultural / products.

### col_BG
  - p36: USE OF PROCEEDS / Assuming an Maximum Offer Price of HK$39.0 per Offer Share, we estimate that we will / receive net proceeds of approximately HK$10,459.7 million from the Global Offering after / deducting the underwriting commissions, fees and other estimated expenses in connection with
  - p36: • / Approximately 10.0% of the net proceeds or approximately HK$1,046.0 million will / be used for working capital and general corporate purposes. / See “Future Plans and Use of Proceeds.” / RISK FACTORS / Our operations and the Global Offering involve certain risks and uncertainties, including / (i) risks relating to our business and industry, (ii) risks relating to the local laws and regulations

### col_BI
  - p2: Number of Offer Shares under the / Global Offering / : / 273,951,400 H Shares (subject to / the Over-allotment Option) / Number of Hong Kong Offer Shares / :

### col_BP
  - p328: Neixiang RCB is a joint-stock limited liability company established on November 30, / 2017 and is a licensed banking institution authorized to conduct operations approved by the / China Banking Regulatory Commission. We have established a long and stable relationship / with Neixiang RCB and it would be conducive for us to maintain the continuity of financial
  - p1: 牧原食品股份有限公司 / MUYUAN FOODS CO., LTD. / Stock Code : 2714 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / GLOBAL OFFERING

### col_BR
  - p120: Neixiang County, Nanyang / Henan Province / PRC / Principal Place of Business in the PRC / Longsheng Industrial Park / Wolong District, Nanyang / Henan Province
  - p120: Registered Office in the PRC / Shuitian Village, Guanzhang Town / Neixiang County, Nanyang / Henan Province
  - p503: INFORMATION / 牧原食品股份有限公司(Muyuan Foods Co., Ltd.) (the “Company”) was established in Nanyang City, Henan / Province, the People’s Republic of China (the “PRC”) on 13 July 2000 as a limited liability company under the PRC / Company Law, with its head office located at Nanyang City, Henan Province. The Company was previously known / as 河南省內鄉縣牧原養殖有限公司(Henan Province Neixiang County Muyuan Breeding Co.

### col_BT
  - p41: the Cyberspace Administration of China (中華人民共和 / 國國家互聯網信息辦公室) / “CASBE” / China Accounting Standards for Business Enterprises / “CCASS” / the Central Clearing and Settlement System established / and operated by HKSCC
  - p40: ended December 31, 2025 based on the audited consolidated results of our Group for the nine months / ended September 30, 2025, the unaudited consolidated results based on the management accounts of our / Group for the three months ended December 31, 2025. The profit estimate has been prepared on a basis / consistent in all material respects with the accounting policies currently adopted by our Gro

### col_CC
  - p5: If there is any change in the following expected timetable(1) of the Hong Kong / Public Offering, we will issue an announcement in Hong Kong to be published on the / Company’s website at www.muyuanfoods.com and the website of the Stock Exchange at / www.hkexnews.hk.
  - p5: Public Offering, we will issue an announcement in Hong Kong to be published on the / Company’s website at www.muyuanfoods.com and the website of the Stock Exchange at / www.hkexnews.hk. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on Thursday, / January 29, 2026 / Latest time to complete electronic applications / under the HK eIPO White Form service

### col_CD
  - p5: If there is any change in the following expected timetable(1) of the Hong Kong / Public Offering, we will issue an announcement in Hong Kong to be published on the / Company’s website at www.muyuanfoods.com and the website of the Stock Exchange at / www.hkexnews.hk.

### col_CE
  - p39: adjustments referred to in the section headed “Unaudited Pro Forma Financial Information” in Appendix / II to this prospectus and on the basis that 5,667,135,906 Shares (being 5,462,771,029 Shares in issue / as of September 30, 2025, deducting 69,586,523 treasury shares held by the Company as of September / 30, 2025 and adding 273,951,400 H Shares to be issued pursuant to the Global Offering) were
  - p335: following major terms: / (i) / Size of the offer / The number of H Shares to be offered under the Global Offering shall not exceed 8% of / the total share capital of our Company as enlarged by the H Shares to be issued pursuant to the / Global Offering (before the exercise of the Over-allotment Option). The number of H Shares / to be issued pursuant to the exercise of the Over-allotment Option sha

### col_CF
  - p27: Operating costs           (102,987.1)(107,414.8)(111,666.5) / (80,065.4) / (90,855.5) / Gross profit             / 21,839.1 / 3,445.9 / 26,280.4
  - p27: Operating costs           (102,987.1)(107,414.8)(111,666.5) / (80,065.4) / (90,855.5) / Gross profit             / 21,839.1 / 3,445.9 / 26,280.4

### col_CG
  - p14: ended September 30, 2024 and 2025, we recorded net cash inflow from operating activities of / RMB23,010.6 million, RMB9,892.8 million, RMB37,543.1 million, RMB29,177.9 million and / RMB28,579.5 million, respectively. From 2022 to 2024, our accumulated net cash inflow from / operating activities was 1.6 times of our accumulated capital expenditure (which represents / payment for acquisition of fix 
  - p14: ended September 30, 2024 and 2025, we recorded net cash inflow from operating activities of / RMB23,010.6 million, RMB9,892.8 million, RMB37,543.1 million, RMB29,177.9 million and / RMB28,579.5 million, respectively. From 2022 to 2024, our accumulated net cash inflow from / operating activities was 1.6 times of our accumulated capital expenditure (which represents / payment for acquisition of fix 

### col_CH
  - p147: system, supervises and guides hog slaughtering plants (houses) to implement various / prevention and control measures, supervises and guides hog slaughtering plants (houses) to / strictly fulfill their main responsibilities for animal epidemic prevention and hog product / quality and safety, resolutely prevents dead hogs and uninspected or unqualified hogs from / entering the slaughterhouse (farm)
  - p480: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purpose of the / accountants’ report, a true and fair view of the Group’s and the Company’s financial position / as at 31 December 2022, 2023 and 2024 and 30 September 2025 and of the Group’s and the / Comp
  - p27: of slaughter volume in 2024. See “Industry Overview.” / SUMMARY OF HISTORICAL FINANCIAL INFORMATION / The following tables set forth summary financial data from historical financial / information during the Track Record Period, extracted from the Accountants’ Report as set out / in Appendix I to this prospectus. The summary financial data set forth below should be read / together with, and is qual

### col_CI
  - p38: dividends, will be subject to our Articles of Association and the relevant PRC laws. We / currently do not have any fixed dividend pay-out ratio. No dividend shall be declared or / payable except out of our profits and reserves lawfully available for distribution. / LISTING EXPENSES / Listing expenses represent professional fees, underwriting commissions and other fees / incurred in connection wit
  - p38: dividends, will be subject to our Articles of Association and the relevant PRC laws. We / currently do not have any fixed dividend pay-out ratio. No dividend shall be declared or / payable except out of our profits and reserves lawfully available for distribution. / LISTING EXPENSES / Listing expenses represent professional fees, underwriting commissions and other fees / incurred in connection wit


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 2714.HK`
有 ERROR 必须回原文修正。
