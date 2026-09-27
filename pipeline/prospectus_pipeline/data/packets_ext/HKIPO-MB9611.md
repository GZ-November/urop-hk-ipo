# 9611.HK 扩展 18 列抽取包

公司：9611.HK Shanghai Longcheer Technology Co., Ltd.- H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB9611.json`。
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
- 股本结构（**已确认，不要改**）：L=522590644 M=52259100 N=470331544 O=470331544 P=0 Q=52259100 R=47033100 S=5226000
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = 685978666.6666666
- 行业分类（港交所官方）：701010 消費性電訊設備及零件
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
{"code":"9611.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  9611.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 9611.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
（锚点无命中，需要自己 search）

### col_BB
  - p31: We do not believe any of the above fees or expenses are material or are unusually high for our / Group. The listing expenses above are the latest practicable estimate for reference only, and the / actual amount may differ from this estimate. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Du, Mr. Ge, Shanghai Xinhe, Kunshan Longcheer, / Chengmai Qihe and Kunshan Qiyun, by v
  - p47: municipalities under direct administration of the central government and provincial-level / autonomous regions. / In this prospectus the terms “associate(s),” “close associate(s),” “connected person(s),” / “core connected person(s),” “connected transaction(s),” “substantial shareholder(s)” and / “treasury share(s)” shall have the meanings given to such terms in the Listing Rules, unless the / cont
  - p105: GTJA Investment will hold the Offer Shares on a non-discretionary basis to hedge the Guanlan / OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed to / the Guotai Haitong Ultimate Client (Guanlan), subject to customary fees and commissions. No / single ultimate beneficial owner of Qingdao Guanlan holds 30% or more interests in the Guotai / Haitong Ultimate Clie

### col_BC
  - p31: We do not believe any of the above fees or expenses are material or are unusually high for our / Group. The listing expenses above are the latest practicable estimate for reference only, and the / actual amount may differ from this estimate. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Du, Mr. Ge, Shanghai Xinhe, Kunshan Longcheer, / Chengmai Qihe and Kunshan Qiyun, by v
  - p47: municipalities under direct administration of the central government and provincial-level / autonomous regions. / In this prospectus the terms “associate(s),” “close associate(s),” “connected person(s),” / “core connected person(s),” “connected transaction(s),” “substantial shareholder(s)” and / “treasury share(s)” shall have the meanings given to such terms in the Listing Rules, unless the / cont

### col_BD
  - p31: We do not believe any of the above fees or expenses are material or are unusually high for our / Group. The listing expenses above are the latest practicable estimate for reference only, and the / actual amount may differ from this estimate. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Du, Mr. Ge, Shanghai Xinhe, Kunshan Longcheer, / Chengmai Qihe and Kunshan Qiyun, by v
  - p31: OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Du, Mr. Ge, Shanghai Xinhe, Kunshan Longcheer, / Chengmai Qihe and Kunshan Qiyun, by virtue of the acting-in-concert arrangement, were / collectively entitled to exercise or control the exercise of the voting rights attaching to / approximately 38.69% of our total issued Shares (excluding the Non-voting Shares). / Immediately fo
  - p47: municipalities under direct administration of the central government and provincial-level / autonomous regions. / In this prospectus the terms “associate(s),” “close associate(s),” “connected person(s),” / “core connected person(s),” “connected transaction(s),” “substantial shareholder(s)” and / “treasury share(s)” shall have the meanings given to such terms in the Listing Rules, unless the / cont

### col_BE
  - p64: equity securities or securities convertible into equity securities, the ownership of our existing / Shareholders may be diluted. The holders of new securities may also have rights, preferences / or privileges which are senior to those of existing holders of ordinary shares. In addition, any / indebtedness we incur may subject us to covenants that restrict our operations and our ability / to effect
  - p25: represented our equity investments in listed companies and investments in wealth management / products, and (iii) an increase in cash and cash equivalents of RMB1,054.6 million; partially / offset by (i) an increase in trade and bills payables of RMB3,656.8 million as a result of an / increase in our procurement of raw materials, and (ii) an increase in interest-bearing bank / borrowings of RMB1,0
  - p25: products, and (iii) an increase in cash and cash equivalents of RMB1,054.6 million; partially / offset by (i) an increase in trade and bills payables of RMB3,656.8 million as a result of an / increase in our procurement of raw materials, and (ii) an increase in interest-bearing bank / borrowings of RMB1,053.8 million. / Our net current assets decreased from RMB2,436.3 million as of December 31, 20

### col_BF
  - p130: products efficiently transition from AI technology prototypes to mass-produced products, / ushering in new development opportunities. Core AI smart devices include AI smartphones, AI / PCs, AIoT devices, AI robots, etc. Smart device ODM providers’ efficient, cost-effective, / hardware-software integrated platform solutions are accelerating the commercialization of / these product categories. / Glo
  - p127: definition, industrial design, hardware and software development to manufacturing and / delivery, they can also serve as EMS suppliers to brand owners. Meanwhile, leading market / participants are building co-developed ODM and EMS models and flexible manufacturing / systems to meet brands’ end-to-end needs from prototype development to mass production. / Comparison Analysis of ODM & EMS Providers 
  - p112: provided by Frost & Sullivan. Unless otherwise indicated, the information has not been / verified by us independently. This statistical information may not be consistent with other / statistical information from other sources within or outside the PRC. While reasonable caution / has been made in the process of reproducing the data and statistics extracted from such official / government publicatio

### col_BG
  - p29: USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$1,520.7 million, after deducting underwriting commissions, fees and estimated expenses / payable by us in connection with the Global Offering, and based on the maximum Offer Price
  - p29: million, will be used to support our global strategic investments or acquisitions; and (v) / approximately 10%, or HK$152.1 million, will be used for working capital and other general / corporate purposes. / See the section headed ‘‘Future Plans and Use of Proceeds’’ in this prospectus for further / information relating to our future plans and use of proceeds from the Global Offering. / PROFIT EST

### col_BI
  - p2: Number of Offer Shares in the / Global Offering / : / 52,259,100 H Shares (subject to the / Over-allotment Option) / Number of Hong Kong Offer Shares / :

### col_BP
  - p460: Company Limited, and International Audit and Evaluation Co., LTD, respectively, both of which are certified / public accounting firms registered in Vietnam. / (11) / This company was incorporated on 26 June 2023. The statutory financial statements of this company for the / year ended 31 December 2024 prepared in accordance with the provisions of the Companies Act 1967 (the Act) / and Financial Rep
  - p1: Stock Code : 9611 / GLOBAL OFFERING / (A joint stock company incorporated in the People’s Republic of China with limited liability) / 上海龍旗科技股份有限公司 / Shanghai Longcheer Technology Co., Ltd. / Joint Sponsors, Overall Coordinators, Joint Global Coordinators,

### col_BR
  - p124: Xuhui District / Shanghai / PRC / Principal Place of Business in Hong Kong / 46/F, Hopewell Centre / 183 Queen’s Road East / Wan Chai
  - p124: Registered Office in Chinese Mainland / and Headquarters / Floor 1, Building 1 / 401 Caobao Road

### col_BT
  - p18: I to this prospectus. The summary financial data set forth below should be read together with, / and is qualified in its entirety by reference to, our financial statements in this prospectus, / including the related notes. Our consolidated financial information was prepared in accordance / with the IFRS Accounting Standards. / SUMMARY / – 8 –
  - p18: I to this prospectus. The summary financial data set forth below should be read together with, / and is qualified in its entirety by reference to, our financial statements in this prospectus, / including the related notes. Our consolidated financial information was prepared in accordance / with the IFRS Accounting Standards. / SUMMARY / – 8 –
  - p320: historical financial information has been prepared under the historical cost convention, except / for investments measured at fair value through profit or loss (“FVTPL”), and derivative / financial instruments which have been measured at fair value. / MATERIAL ACCOUNTING POLICIES AND ESTIMATES / Revenue Recognition / Revenue from Contracts with Customers / Revenue from contracts with customers is 

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on the websites / of the Stock Exchange at www.hkexnews.hk and our Company at www.longcheer.com. / Date(1)
  - p5: Offering, we will issue an announcement in Hong Kong to be published on the websites / of the Stock Exchange at www.hkexnews.hk and our Company at www.longcheer.com. / Date(1) / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on / Wednesday, January 14, 2026 / Latest time to complete electronic applications / under the White Form eIPO serv

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on the websites / of the Stock Exchange at www.hkexnews.hk and our Company at www.longcheer.com. / Date(1)

### col_CE
  - p110: APPLICATION FOR LISTING OF THE H SHARES ON THE HONG KONG STOCK / EXCHANGE / We have applied to the Hong Kong Stock Exchange for the granting of listing of, and / permission to deal in, our H Shares to be issued pursuant to the Global Offering (including any / H Shares which may be issued pursuant to the exercise of the Over-allotment Option). Dealings / in the H Shares on the Hong Kong Stock Excha
  - p314: the Shareholders’ general meeting of our Company held on June 9, 2025 and is subject to the / following major conditions: / (a) / Size of the offer. The proposed number of H Shares to be offered shall not exceed / 15% of the total issued share capital enlarged by the H Shares to be issued pursuant / to the Global Offering (before the exercise of the Over-allotment Option). The / number of H Shares

### col_CF
  - p19: (94.2) (32,887,922) / (94.2) (28,725,221) / (91.7) / Gross profit       / 2,365,121 / 8.1 / 2,590,156
  - p19: (94.2) (32,887,922) / (94.2) (28,725,221) / (91.7) / Gross profit       / 2,365,121 / 8.1 / 2,590,156

### col_CG
  - p67: fund our operations, expose us to interest rate risk and prevent us from meeting our / obligations under our indebtedness. / During the Track Record Period, we, to a certain extent, used bank borrowings to finance / our capital expenditures and business operations. We expect that we may continue to do so in / the future and our liquidity risk may increase. As of December 31, 2022, 2023 and 2024 an
  - p67: fund our operations, expose us to interest rate risk and prevent us from meeting our / obligations under our indebtedness. / During the Track Record Period, we, to a certain extent, used bank borrowings to finance / our capital expenditures and business operations. We expect that we may continue to do so in / the future and our liquidity risk may increase. As of December 31, 2022, 2023 and 2024 an

### col_CH
  - p440: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the / accountants’ report, a true and fair view of the financial position of the Group and the Company / as at 31 December 2022, 2023 and 2024 and 30 September 2025 and of the financial / perfor
  - p18: see “Business — Relationship with Our Largest Customer.” / SUMMARY OF HISTORICAL FINANCIAL INFORMATION / The following tables set forth summary financial data from our financial information / during the Track Record Period, extracted from the Accountants’ Report as set out in Appendix / I to this prospectus. The summary financial data set forth below should be read together with, / and is qualifie

### col_CI
  - p20: should not consider it in isolation from, or as substitute for analysis of, our results of operations / or financial condition as reported under IFRS. / We define adjusted net profit (non-IFRS measure) as profit for the year adding back / share-based payments and listing expenses. Share-based payments are non-cash in nature and / do not result in cash outflows. We define adjusted EBITDA (non-IFRS 
  - p20: should not consider it in isolation from, or as substitute for analysis of, our results of operations / or financial condition as reported under IFRS. / We define adjusted net profit (non-IFRS measure) as profit for the year adding back / share-based payments and listing expenses. Share-based payments are non-cash in nature and / do not result in cash outflows. We define adjusted EBITDA (non-IFRS 


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 9611.HK`
有 ERROR 必须回原文修正。
