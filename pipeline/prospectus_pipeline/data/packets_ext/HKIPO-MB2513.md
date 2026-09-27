# 2513.HK 扩展 18 列抽取包

公司：2513.HK Knowledge Atlas Technology Joint Stock Company Limited - H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB2513.json`。
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
- 股本结构（**已确认，不要改**）：L=440230190 M=37419500 N=402810690 O=402810690 P=0 Q=37419500 R=35548500 S=1871000
- 财务期间（**已确认**）：year-1 期末 = 30/06/25；币种 = RMB；year-1 净利 = -4715704000
- 行业分类（港交所官方）：702030 應用軟件
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
{"code":"2513.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  2513.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 2513.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p21: under Rule 18C.03 of the Listing Rules as a Commercial Company (as defined in the Listing Rules) with / reference to our expected market capitalization at the time of Listing, which, based on the Offer Price of / HK$116.20 per Offer Share, exceeds HK$6 billion. / PRE-IPO INVESTMENTS / We completed eight rounds of Pre-IPO Investments and had raised funds of over RMB8,360 million. / See “History, De
  - p21: PRE-IPO INVESTMENTS / We completed eight rounds of Pre-IPO Investments and had raised funds of over RMB8,360 million. / See “History, Development and Corporate Structure—Pre-IPO Investments” for further details of the Pre- / IPO Investments and the Pre-IPO Investors. / RISK FACTORS / Our operations and the Global Offering involve certain risks and uncertainties, including (i) risks / related to ou
  - p21: under Rule 18C.03 of the Listing Rules as a Commercial Company (as defined in the Listing Rules) with / reference to our expected market capitalization at the time of Listing, which, based on the Offer Price of / HK$116.20 per Offer Share, exceeds HK$6 billion. / PRE-IPO INVESTMENTS / We completed eight rounds of Pre-IPO Investments and had raised funds of over RMB8,360 million. / See “History, De

### col_BB
  - p21: 53.6%, 47.3% and 50.2% of our total purchases, respectively. In each year/period during 2022, 2023, 2024 / and the six months ended June 30, 2025, purchases from our largest supplier accounted for 33.1%, 16.4%, / 15.6% and 13.4% of our total purchases, respectively. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, the Controlling Shareholders, Beijing Lianpai, Dr. Liu, Dr. Tang,
  - p41: Limited; / “subsidiary(ies)” / has the meaning ascribed to it under the Listing Rules; / “substantial shareholder(s)” / has the meaning ascribed to it under the Listing Rules; / “Supervisor” / the supervisor of our Company;
  - p80: each of the Company, the Overall Coordinators, CICCHKS and CICC FT has provided the Stock / Exchange with written confirmations in accordance with Chapter 4.15 of the Guide; and / (f) / details of the cornerstone investment, the identities of ultimate beneficial owners of the securities and / details of the structured products under has been disclosed in this prospectus, and details of the final /

### col_BC
  - p21: 53.6%, 47.3% and 50.2% of our total purchases, respectively. In each year/period during 2022, 2023, 2024 / and the six months ended June 30, 2025, purchases from our largest supplier accounted for 33.1%, 16.4%, / 15.6% and 13.4% of our total purchases, respectively. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, the Controlling Shareholders, Beijing Lianpai, Dr. Liu, Dr. Tang,
  - p41: Limited; / “subsidiary(ies)” / has the meaning ascribed to it under the Listing Rules; / “substantial shareholder(s)” / has the meaning ascribed to it under the Listing Rules; / “Supervisor” / the supervisor of our Company;

### col_BD
  - p21: 53.6%, 47.3% and 50.2% of our total purchases, respectively. In each year/period during 2022, 2023, 2024 / and the six months ended June 30, 2025, purchases from our largest supplier accounted for 33.1%, 16.4%, / 15.6% and 13.4% of our total purchases, respectively. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, the Controlling Shareholders, Beijing Lianpai, Dr. Liu, Dr. Tang,
  - p304: request to early terminate the Gaoyi OTC Swaps at their own discretions, upon which CICC FT may / dispose of the Offer Shares and settle the Gaoyi OTC Swaps in cash in accordance with the terms and / conditions of the Gaoyi OTC Swaps. Despite that CICC FT will hold the legal title of the Offer Shares by / itself, it will not exercise the voting rights attaching to the relevant Offer Shares during 
  - p41: Limited; / “subsidiary(ies)” / has the meaning ascribed to it under the Listing Rules; / “substantial shareholder(s)” / has the meaning ascribed to it under the Listing Rules; / “Supervisor” / the supervisor of our Company;

### col_BE
  - p292: FINANCIAL INFORMATION / INDEBTEDNESS / Our indebtedness during the Track Record Period primarily consisted of bank loans and lease / liabilities. The following table sets forth a breakdown of our indebtedness as of the dates indicated. / As of December 31,
  - p29: (2) / Quick ratio is calculated by dividing current assets less inventories by current liabilities as of the date indicated. / (3) / Gearing ratio is calculated by dividing total interest-bearing bank and other borrowings and lease liabilities divided by total equity / as of the end of the period multiplied by 100%. / – 20 –
  - p29: (2) / Quick ratio is calculated by dividing current assets less inventories by current liabilities as of the date indicated. / (3) / Gearing ratio is calculated by dividing total interest-bearing bank and other borrowings and lease liabilities divided by total equity / as of the end of the period multiplied by 100%. / – 20 –

### col_BF
  - p10: China. We have solidly delivered advanced technology across the full spectrum of AI research and steadily / scaled up its commercial application to achieve fast growth in revenue. In 2021, we launched GLM / framework, China’s first proprietary pre-trained large model framework, and debuted our Model-as-a- / Service (MaaS) product development and commercialization platform, through which we provide
  - p60: Any flaws or misuse of AI technologies, whether actual or perceived, intended or inadvertent, / committed by us or by other third parties, could have a material adverse effect on our reputation, / business, results of operations, financial condition and prospects. / AI technologies are in the process of rapid development and continue to evolve. Similar to many / innovations, AI technologies presen

### col_BG
  - p30: 440,230,190 Shares were in issue (being 402,810,690 Shares in issue and outstanding as of June 30, 2025 taking into account the / Share Subdivision and 37,419,500 H Shares to be issued pursuant to Global Offering) and does not take into account of any shares / which may be issued upon the exercise of the Over-allotment Option or the share incentive plans. / FUTURE PLANS AND USE OF PROCEEDS / Assum
  - p30: 440,230,190 Shares were in issue (being 402,810,690 Shares in issue and outstanding as of June 30, 2025 taking into account the / Share Subdivision and 37,419,500 H Shares to be issued pursuant to Global Offering) and does not take into account of any shares / which may be issued upon the exercise of the Over-allotment Option or the share incentive plans. / FUTURE PLANS AND USE OF PROCEEDS / Assum

### col_BI
  - p251: 9.65% / 445,843,090 / 100.00% / SHARE CLASSES AND RANKING / Upon the completion of the Global Offering and the Conversion of Unlisted Shares into H Shares, our / Shares will consist of Unlisted Shares and H Shares. Unlisted Shares and H Shares are all ordinary Shares / in the share capital of our Company and are regarded as the same class of Shares under the Articles of
  - p2: (A joint stock company established in the People’s Republic of China with limited liability) / GLOBAL OFFERING / Number of Offer Shares under the Global Offering / 37,419,500 H Shares (subject to the Over-allotment / Option) / Number of Hong Kong Offer Shares / 1,871,000 H Shares (subject to reallocation)

### col_BP
  - p305: Investment Management Limited（廣發國際資產管理有限公司) (“GF Fund HK”, together with GF Fund / Management, “GF Fund”) have, respectively, entered into Cornerstone Investment Agreement with our / Company. / GF Fund Management was established on August 5, 2003. GF Fund Management and its subsidiaries / are licensed to conduct business as Qualified Investment Manager of Public Fund, Entrusted Domestic / Investme
  - p78: “Cornerstone Investors,” as Luster LightTech International is wholly owned by Luster, it is a close associate / of Luster. / Structured Credit SP Fund / JinYi Capital Multi-Strategy Fund SPC Ltd. is a segregated portfolio company incorporated in the / Cayman Islands. The funding of JinYi Capital Multi-Strategy Fund SPC Ltd.—Structured Credit SP Fund, / which is participating in the Global Offering

### col_BR
  - p89: Haidian District / Beijing / PRC / Principal place of business in Hong Kong / 40/F, Dah Sing Financial Centre / 248 Queen’s Road East, Wanchai / Hong Kong
  - p89: CORPORATE INFORMATION / Headquarters and registered office in the PRC / 10th Floor, Building 9 / Yard 1, Zhongguancun East Road / Haidian District
  - p83: H SHARE REGISTER OF MEMBERS AND STAMP DUTY / All of the H Shares issued pursuant to applications made in the Global Offering will be registered on / our H Share register of members to be maintained in Hong Kong by our H Share Registrar, Tricor Investor / Services Limited. Our principal register of members will be maintained by us at our head office in the PRC. / Dealings in the H Shares registered

### col_BT
  - p22: Period, extracted from the Accountants’ Report as set out in Appendix I to this document. The key financial / information set forth below should be read together with, and is qualified in its entirety by reference to, our / financial statements in this document, including the related notes. Our consolidated financial information / was prepared in accordance with the IFRS Accounting Standards. / – 
  - p22: Period, extracted from the Accountants’ Report as set out in Appendix I to this document. The key financial / information set forth below should be read together with, and is qualified in its entirety by reference to, our / financial statements in this document, including the related notes. Our consolidated financial information / was prepared in accordance with the IFRS Accounting Standards. / – 
  - p13: contracts, we generally recognize revenue ratably over the contract term; for usage-based contracts, we / recognize revenue based on the customer’s utilization of the resources when the services are rendered to the / customers. For details of our revenue recognition policies, see “Financial Information—Material / Accounting Policies and Estimates—Material Accounting Policy Information—Revenue Reco

### col_CC
  - p5: EXPECTED TIMETABLE(1) / If there is any change in the following expected timetable of the Hong Kong Public Offering, we / will issue an announcement to be published on the websites of the Stock Exchange at / www.hkexnews.hk and our Company at www.zhipuai.cn.
  - p5: If there is any change in the following expected timetable of the Hong Kong Public Offering, we / will issue an announcement to be published on the websites of the Stock Exchange at / www.hkexnews.hk and our Company at www.zhipuai.cn. / Hong Kong Public Offering commences . . . . . . . . . . / 9:00 a.m. / Tuesday, December 30, 2025 / Latest time for completing applications under the HK

### col_CD
  - p5: EXPECTED TIMETABLE(1) / If there is any change in the following expected timetable of the Hong Kong Public Offering, we / will issue an announcement to be published on the websites of the Stock Exchange at / www.hkexnews.hk and our Company at www.zhipuai.cn.

### col_CE
  - p82: or existing Shareholders or a nominee of any of the foregoing. / APPLICATION FOR LISTING OF H SHARES ON THE STOCK EXCHANGE / We have applied to the Stock Exchange for the granting of the listing of, and permission to deal in, our / H Shares to be issued pursuant to the Global Offering (including any H Shares which may be issued / pursuant to the exercise of the Over-allotment Option) and the H Sha
  - p3: be made for a minimum of 100 Hong Kong Offer Shares and in multiples of that number of Hong / Kong Offer Shares as set out in the table below. / If you are applying through the HK eIPO White Form service, you may refer to the table below / for the amount payable for the number of H Shares you have selected. You must pay the respective / amount payable on application in full upon application for Ho

### col_CF
  - p11: Number of institutional customers(2) / Revenue in 2022, 2023, 2024 and the / six months ended June 30, 2025 / Gross profit margin / in 2022, 2023, 2024 and the / six months ended June 30, 2025 / Revenue CAGR from 2022 to 2024
  - p11: Number of institutional customers(2) / Revenue in 2022, 2023, 2024 and the / six months ended June 30, 2025 / Gross profit margin / in 2022, 2023, 2024 and the / six months ended June 30, 2025 / Revenue CAGR from 2022 to 2024

### col_CG
  - p48: • / our strategies, plans, objectives and goals and our ability to successfully implement them; / • / estimates of our costs, expenses, future revenues, capital expenditures and our needs for / additional financing; / • / our ability to attract and retain senior management and key employees;
  - p48: • / our strategies, plans, objectives and goals and our ability to successfully implement them; / • / estimates of our costs, expenses, future revenues, capital expenditures and our needs for / additional financing; / • / our ability to attract and retain senior management and key employees;

### col_CH
  - p345: We believe that the evidence we have obtained is sufficient and appropriate to provide a basis for our / opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purpose of the accountants’ report, / a true and fair view of the Group’s and the Company’s financial position as at 31 December 2022, 2023 and / 2024 and 30 June 2025, and of the Group’s financial performa
  - p22: We have a limited track record in the commercialization of our business. / SUMMARY OF KEY FINANCIAL INFORMATION / The following tables set forth the summary of key financial information during the Track Record / Period, extracted from the Accountants’ Report as set out in Appendix I to this document. The key financial / information set forth below should be read together with, and is qualified in 

### col_CI
  - p24: of, our consolidated financial statements or financial condition as reported under IFRS Accounting Standards. / We define adjusted loss for the year/period (a non-IFRS measure) as loss for the year/period adjusted for adding / back equity-settled share-based compensation expenses, changes in the carrying amount of financial instruments / issued to investors, and listing expenses. / Year Ended / De
  - p24: of, our consolidated financial statements or financial condition as reported under IFRS Accounting Standards. / We define adjusted loss for the year/period (a non-IFRS measure) as loss for the year/period adjusted for adding / back equity-settled share-based compensation expenses, changes in the carrying amount of financial instruments / issued to investors, and listing expenses. / Year Ended / De


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 2513.HK`
有 ERROR 必须回原文修正。
