# 3625.HK 扩展 18 列抽取包

公司：3625.HK Shanghai FourSemi Semiconductor Co., Ltd. - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB3625.json`。
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
- 股本结构（**已确认，不要改**）：L=112000000 M=12000000 N=100000000 O=100000000 P=0 Q=12000000 R=11400000 S=600000
- 财务期间（**已确认**）：year-1 期末 = 31/10/2025；币种 = RMB；year-1 净利 = -62131200
- 行业分类（港交所官方）：703010 半導體
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
{"code":"3625.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  3625.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 3625.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p20: For details on the accounting treatment of redemption rights of pre-IPO investments, see “— / Share Capital and Total Equity” below and note 26 to the Accountants’ Report set out in Appendix I to / this prospectus. See note 28 to the Accountants’ Report in Appendix I to this prospectus for further / details of the financial impacts.
  - p24: To fund our strategic growth and broaden our shareholder base, we have conducted several rounds / of Pre-IPO Investments since the incorporation of our Company. See “History and Corporate Structure / — Pre-IPO Investments” for details of the principal terms of our Pre-IPO Investments and the identity / and background of our Pre-IPO Investors. / SUMMARY / – 15 –
  - p20: For details on the accounting treatment of redemption rights of pre-IPO investments, see “— / Share Capital and Total Equity” below and note 26 to the Accountants’ Report set out in Appendix I to / this prospectus. See note 28 to the Accountants’ Report in Appendix I to this prospectus for further / details of the financial impacts.

### col_BB
  - p8: 104 / BUSINESS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . / 128 / RELATIONSHIP WITH OUR CONTROLLING SHAREHOLDERS . . . . . . . . . . . . . . . . . / 201 / FINANCIAL INFORMATION. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . / 204
  - p37: subsidiary of Hong Kong Exchanges and Clearing Limited / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Takeovers Code” / the Code on Takeovers and Mergers issued by the SFC, as

### col_BC
  - p8: 104 / BUSINESS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . / 128 / RELATIONSHIP WITH OUR CONTROLLING SHAREHOLDERS . . . . . . . . . . . . . . . . . / 201 / FINANCIAL INFORMATION. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . / 204
  - p37: subsidiary of Hong Kong Exchanges and Clearing Limited / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Takeovers Code” / the Code on Takeovers and Mergers issued by the SFC, as

### col_BD
  - p8: 104 / BUSINESS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . / 128 / RELATIONSHIP WITH OUR CONTROLLING SHAREHOLDERS . . . . . . . . . . . . . . . . . / 201 / FINANCIAL INFORMATION. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . / 204
  - p323: Control is achieved when the Group is exposed, or has rights, to variable returns from its involvement / with the investee and has the ability to affect those returns through its power over the investee (i.e., / existing rights that give the Group the current ability to direct the relevant activities of the investee). / Generally, there is a presumption that a majority of voting rights results in 
  - p37: subsidiary of Hong Kong Exchanges and Clearing Limited / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Takeovers Code” / the Code on Takeovers and Mergers issued by the SFC, as

### col_BE
  - p249: INDEBTEDNESS / Our indebtedness during the Track Record Period primarily consisted of interest-bearing bank / borrowings, lease liabilities and redemption liabilities. The following table sets forth a breakdown of / our indebtedness as of the dates indicated.
  - p22: See “Financial Information — Discussion of Certain Balance Sheet Items” for detailed discussion / of our consolidated statements of financial position items during the Track Record Period. / Net current assets decreased from RMB141.7 million as of December 31, 2024 to RMB126.0 / million as of October 31, 2025. This decrease was primarily driven by an increase in interest-bearing / bank borrowings 
  - p22: current assets. Our net current assets increased from RMB136.2 million as of December 31, 2023 to / RMB141.7 million as of December 31, 2024, primarily due to a rise in inventory, trade receivables, and / prepayments, which outweighed the increase in trade payables. This growth consequently led to a rise / in current liabilities, notably trade payables and short-term bank borrowings, to fund worki

### col_BF
  - p15: as it reflected early-stage launch costs. As sales scaled and operational efficiencies were realized in / 2024, the gross profit margin normalized at a higher, more sustainable level, underscoring the success / of integrating haptic drivers into our broader product portfolio and sales strategy. / COMMERCIALIZATION / We primarily engaged in the design and development of semiconductor chips. Our Dir
  - p14: and drive audio signals with output power exceeding 10W. Our product design for mid/high-power / audio chips prioritizes heat dissipation and electromagnetic interference mitigation to ensure sustained / performance in compact, power-dense environments. We launched China’s first mid-power amplifier / audio chip, FS2119, in 2021. The FS2119 series has since achieved mass production and has been / w
  - p61: 2023, 2024 and October 31, 2025, we engaged third-party agencies for paying social insurance or / housing provident funds to 18, six, five and seven employees, respectively. During the Track Record / Period, such third-party agencies made a total of RMB2.9 million of social insurance and housing / provident fund contributions on behalf of us. We are in the process of rectifying the non-compliance 

### col_BG
  - p24: of approximately HK$480.3 million after deducting the underwriting fees and expenses payable by us / in the Global Offering, assuming no Over-allotment Option is exercised and assuming an Offer Price of / HK$40.00 per Offer Share, being the low-point of the indicative Offer Price range in this prospectus, if / we also take into account our intended use of proceeds for future expansion plans, inclu
  - p26: (3) / The unaudited pro forma adjusted consolidated net tangible assets attributable to owners of the Company are arrived on the / basis that 112,000,000 shares were in issue assuming that the Global Offering had been completed on October 31, 2025. / FUTURE PLANS AND USE OF PROCEEDS / We estimate that the net proceeds of the Global Offering, after deducting the estimated / underwriting commissions

### col_BI
  - p2: Global Offering / Number of Offer Shares under the Global Offering / : / 12,000,000 H Shares (subject to the Over-allotment / Option) / Number of Hong Kong Offer Shares / :

### col_BP
  - p1: Shanghai FourSemi Semiconductor Co., Ltd. / 上海傅里葉半導體股份有限公司 / (A joint stock company incorporated in the People's Republic of China with limited liability) / Stock Code : 3625 / GLOBAL OFFERING / Joint Sponsors, Joint Sponsor-Overall Coordinators, Joint Global Coordinators,

### col_BR
  - p90: Lin-gang Special Area / China (Shanghai) Free Trade Pilot Zone / PRC / Principal Place of Business in Hong / Kong / 46/F, Hopewell Centre / 183 Queen’s Road East
  - p90: Registered Office and Headquarters / Room 303, Building 4 / Second Street, Gangcheng Square / No. 88 Yunjuan Road, Lane 11

### col_BT
  - p20: We believe that the adjusted loss (non-IFRS measure) would provide useful information to / investors and others in understanding and evaluating our consolidated results of operations in the same / manner as they help our management. However, our non-IFRS measure does not have a standardized / meaning prescribed by IFRS Accounting Standards, and our presentation of adjusted loss (non-IFRS / measure
  - p19: and should be read together with the consolidated financial statements in the Accountants’ Report set / out in Appendix I to this prospectus, including the accompanying notes and the information set forth in / “Financial Information.” Our consolidated financial information was prepared in accordance with IFRS / Accounting Standards. / Summary of Consolidated Statements of Profit or Loss / The foll
  - p217: Track Record Period. / The historical financial information has been prepared under the historical cost convention, except / for certain financial instruments which have been measured at fair value. / MATERIAL ACCOUNTING POLICIES, ESTIMATES AND JUDGMENTS / We have identified certain accounting policies that are significant to the preparation of our / consolidated financial statements. Some of our 

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public Offering, / we will issue an announcement in Hong Kong to be published on the websites of the Stock Exchange / at www.hkexnews.hk and our website at www.foursemi.com. / Time and date(1)
  - p5: we will issue an announcement in Hong Kong to be published on the websites of the Stock Exchange / at www.hkexnews.hk and our website at www.foursemi.com. / Time and date(1) / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9:00 a.m. on / Monday, March 23, 2026 / Latest time to complete electronic applications under / White Form eIPO se

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public Offering, / we will issue an announcement in Hong Kong to be published on the websites of the Stock Exchange / at www.hkexnews.hk and our website at www.foursemi.com. / Time and date(1)

### col_CE
  - p273: effective within 12 months from the date of approval. / Listing Approval by the Stock Exchange / We have applied to the Listing Committee of the Stock Exchange for the granting of listing of, / and permission to deal in, our H Shares to be issued pursuant to the Global Offering (including any H / Shares which may be issued pursuant to the exercise of the Over-allotment Option) and the H Shares to 
  - p4: made for a minimum of 100 Hong Kong Offer Shares and in multiples of that number of Hong Kong / Offer Shares as set out in the table below. / If you are applying through the White Form eIPO service, you may refer to the table below for / the amount payable for the number of H Shares you have selected. You must pay the respective amount / payable on application in full upon application for Hong Kon

### col_CF
  - p12: due to significantly increased customer demand for certain higher-priced models of the FS21 series. The / ASP decreased to RMB2.28 per unit in 2024 as demand for other models with lower unit prices / increased. / The following table sets forth a breakdown of our gross profit and gross profit/(loss) margin by / product type for the periods indicated. / Year ended December 31, / Ten months ended Oct
  - p12: due to significantly increased customer demand for certain higher-priced models of the FS21 series. The / ASP decreased to RMB2.28 per unit in 2024 as demand for other models with lower unit prices / increased. / The following table sets forth a breakdown of our gross profit and gross profit/(loss) margin by / product type for the periods indicated. / Year ended December 31, / Ten months ended Oct

### col_CG
  - p48: • / our financial condition and performance; / • / our capital expenditure plans; / • / our dividend policy; / •
  - p48: • / our financial condition and performance; / • / our capital expenditure plans; / • / our dividend policy; / •
  - p252: CAPITAL EXPENDITURES AND COMMITMENTS / Capital Expenditures / Our capital expenditures during the Track Record Period primarily consisted of expenditures on / purchase of property, plant and equipment and purchase of intangible asset. The following table sets / forth our capital expenditure for the periods indicated. / Year ended December 31, / Ten months ended October 31,

### col_CH
  - p312: We believe that the evidence we have obtained is sufficient and appropriate to provide a basis for / our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the accountants’ / report, a true and fair view of the financial position of the Group and the Company as at 31 December / 2022, 2023, 2024 and 31 October 2025 and of the financial performance a
  - p19: operations and financial condition could be adversely affected.” for details. / SUMMARY OF HISTORICAL FINANCIAL INFORMATION / The following tables set forth summary of our financial information for the Track Record Period, / and should be read together with the consolidated financial statements in the Accountants’ Report set / out in Appendix I to this prospectus, including the accompanying notes 

### col_CI
  - p20: connection with our award to key employees. Such expenses in any specific period are not / expected to result in future cash payments. / • / Listing expenses represent the costs incurred in connection with our initial public offering / on the Hong Kong Stock Exchange. Such expenses in any specific period are not expected to / result in future cash payments after completion of the listing process. 
  - p20: connection with our award to key employees. Such expenses in any specific period are not / expected to result in future cash payments. / • / Listing expenses represent the costs incurred in connection with our initial public offering / on the Hong Kong Stock Exchange. Such expenses in any specific period are not expected to / result in future cash payments after completion of the listing process. 


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 3625.HK`
有 ERROR 必须回原文修正。
