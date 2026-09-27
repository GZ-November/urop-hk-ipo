# 1989.HK 扩展 18 列抽取包

公司：1989.HK Delton Technology (Guangzhou) Inc. - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB1989.json`。
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
- 股本结构（**已确认，不要改**）：L=472446482 M=46000000 N=426446482 O=426446482 P=0 Q=46000000 R=41400000 S=4600000
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = 965092000.0
- 行业分类（港交所官方）：101025 電氣及電子零件
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
{"code":"1989.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  1989.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 1989.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
（锚点无命中，需要自己 search）

### col_BB
  - p24: Directors confirm that, since our A Share Listing and up to the Latest Practicable Date, there / had been no instance of any material non-compliance with the applicable rules of the / Shenzhen Stock Exchange and other applicable PRC securities laws and regulations. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Xiao and Ms. Liu, through Zhenyun Investment, / Guangsheng Inv
  - p35: per cent / In this Prospectus, the terms “associate(s),” “close associate(s),” “connected / person(s),” “connected transaction(s),” “core connected person(s),” “controlling / shareholder(s),” “subsidiary(ies)” and “substantial shareholder(s)” shall have the meanings / given to such terms in the Listing Rules, unless the context otherwise requires. / For ease of reference, the names of the PRC esta
  - p262: defined under the SFO, including corporations, institutions and high net worth individual / investors. CPE holds 100 management shares in the CPE Funds and controls their entire / voting rights. Mr. Ni Fei, director of CPE, indirectly holds 30% shares interest in CPE. Save / for Mr. Ni Fei, no single ultimate beneficial owner holds 30% or more interest in CPE. In / addition, no single ultimate ben

### col_BC
  - p24: Directors confirm that, since our A Share Listing and up to the Latest Practicable Date, there / had been no instance of any material non-compliance with the applicable rules of the / Shenzhen Stock Exchange and other applicable PRC securities laws and regulations. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Xiao and Ms. Liu, through Zhenyun Investment, / Guangsheng Inv
  - p35: per cent / In this Prospectus, the terms “associate(s),” “close associate(s),” “connected / person(s),” “connected transaction(s),” “core connected person(s),” “controlling / shareholder(s),” “subsidiary(ies)” and “substantial shareholder(s)” shall have the meanings / given to such terms in the Listing Rules, unless the context otherwise requires. / For ease of reference, the names of the PRC esta

### col_BD
  - p24: Directors confirm that, since our A Share Listing and up to the Latest Practicable Date, there / had been no instance of any material non-compliance with the applicable rules of the / Shenzhen Stock Exchange and other applicable PRC securities laws and regulations. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, Mr. Xiao and Ms. Liu, through Zhenyun Investment, / Guangsheng Inv
  - p75: waiver from strict compliance with the requirements under Rule 10.04 of, and consent under / Paragraph 1C(2) of Appendix F1 to, the Listing Rules to permit H Shares in the International / Offering to be placed to certain existing minority Shareholders who (i) hold less than 5% of / our Company’s voting rights prior to the completion of the Global Offering; and (ii) are not / and will not become (u
  - p35: per cent / In this Prospectus, the terms “associate(s),” “close associate(s),” “connected / person(s),” “connected transaction(s),” “core connected person(s),” “controlling / shareholder(s),” “subsidiary(ies)” and “substantial shareholder(s)” shall have the meanings / given to such terms in the Listing Rules, unless the context otherwise requires. / For ease of reference, the names of the PRC esta

### col_BE
  - p22: Our Directors confirm that, as of the date of this Prospectus, there has been no material / adverse change in our financial or trading position, indebtedness, mortgages, contingent / liabilities, guarantees or prospects since September 30, 2025, the end of the period reported on / the Accountants’ Report in Appendix I to this Prospectus. / Recent U.S.-China Tension on Tariffs
  - p23: Quick ratio was calculated by dividing the difference of current assets and inventories by total current / liabilities as of the dates indicated. / (3) / Gearing ratio was calculated based on total indebtedness (including lease liabilities, interest-bearing / bank and other borrowings) divided by total equity and multiplied by 100%. / (4) / Liability-to-asset ratio was calculated by dividing total
  - p23: liabilities as of the dates indicated. / (3) / Gearing ratio was calculated based on total indebtedness (including lease liabilities, interest-bearing / bank and other borrowings) divided by total equity and multiplied by 100%. / (4) / Liability-to-asset ratio was calculated by dividing total liabilities by total assets. / (5)

### col_BF
  - p46: Our products are intricate in nature and may contain errors, defects, bugs that are / difficult to detect and correct, particularly when first introduced or when new versions or / enhancements are released. Some errors or defects in our products may only be discovered / after they have been tested, commercialized and deployed by our end customers. Under these / circumstances, we may incur addition
  - p96: manufacturers are rapidly capturing high-end markets. The emergence of domestic computing / power chips has spurred the localization of supporting PCB supply chains. Through material / formula improvements, optimized processing techniques, and smart production lines, / domestic companies enhance mass production capabilities for high-layer-count server PCBs, / breaking foreign monopolies in ultra-h
  - p105: on November 1, 2021. The PIPL stipulates the scope of personal information and the ways of / processing personal information, establishes rules for processing personal information and for / providing personal information to overseas recipients, and clarifies the individual’s rights and / the processor’s obligations in the process of personal information processing. The CAC / promulgated the Securi

### col_BG
  - p21: Subsequent to the Track Record Period and up to the Latest Practicable Date, we are also / expanding the production capacity of our Guangzhou base, in particular for the production / capacity for HDI PCBs. The expanded production lines are expected to commence production / in the fourth quarter of 2026. See also “Future Plans and Use of Proceeds.” / Based on our unaudited financial information for
  - p21: Subsequent to the Track Record Period and up to the Latest Practicable Date, we are also / expanding the production capacity of our Guangzhou base, in particular for the production / capacity for HDI PCBs. The expanded production lines are expected to commence production / in the fourth quarter of 2026. See also “Future Plans and Use of Proceeds.” / Based on our unaudited financial information for

### col_BI
  - p2: Number of Offer Shares under / the Global Offering / : / 46,000,000 H Shares / Number of Hong Kong Offer Shares / : / 4,600,000 H Shares (subject to

### col_BP
  - p1: DELTON TECHNOLOGY (GUANGZHOU) INC. / 廣州廣合科技股份有限公司 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / Stock Code: 1989 / Overall Coordinators, Joint Global Coordinators, / Joint Bookrunners and Joint Lead Managers

### col_BR
  - p87: Registered Office / No.22 / Baoying South Road / Bonded Zone, Guangzhou

### col_BT
  - p16: Non-IFRS Measures / To supplement our consolidated financial statements that are presented in accordance / with IFRS Accounting Standards, we also use EBITDA (a non-IFRS measure) as an additional / financial measure, which is not required by, or presented in accordance with, IFRS / Accounting Standards. We define EBITDA (a non-IFRS measure) as profit for the year/period / adjusted by adding back (
  - p324: 2022. / (e) / The statutory financial statements of this entity for the years ended December 31, 2022, 2023 and 2024 / prepared under HKFRS Accounting Standards were audited by JOE PANG & CO, certified public / accountants registered in Hong Kong. / (f) / No audited financial statements have been prepared for these entities for the years ended December 31,
  - p16: Non-IFRS Measures / To supplement our consolidated financial statements that are presented in accordance / with IFRS Accounting Standards, we also use EBITDA (a non-IFRS measure) as an additional / financial measure, which is not required by, or presented in accordance with, IFRS / Accounting Standards. We define EBITDA (a non-IFRS measure) as profit for the year/period / adjusted by adding back (

### col_CC
  - p5: our website at www.delton.com.cn by(5) / . . . . . . . . . . . . . . . . . . . . . . . . . . 11:00 p.m. on / Thursday, March 19, 2026 / EXPECTED TIMETABLE(1) / – i –
  - p5: timetable of the Hong Kong Public Offering, an announcement will be made and published / on the website of the Stock Exchange at www.hkexnews.hk and our website at / www.delton.com.cn of the revised timetable. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9:00 a.m. on / Thursday, March 12, 2026 / Latest time for completing electronic applications

### col_CD
  - p5: our website at www.delton.com.cn by(5) / . . . . . . . . . . . . . . . . . . . . . . . . . . 11:00 p.m. on / Thursday, March 19, 2026 / EXPECTED TIMETABLE(1) / – i –

### col_CE
  - p82: securities regulatory authorities or an exemption therefrom. / APPLICATION FOR LISTING ON THE STOCK EXCHANGE / We have applied to the Listing Committee for the listing of, and permission to deal in, / the H Shares to be issued pursuant to the Global Offering. Dealings in the H Shares on the / Stock Exchange are expected to commence on Friday, March 20, 2026. Other than our A / Shares, which are cu
  - p4: number of Hong Kong Offer Shares will be considered and such an application is liable to be / rejected. / If you are applying through the HK eIPO White Form service, you may refer to the / table below for the amount payable for the number of H Shares you have selected. You must / pay the respective maximum amount payable on application in full upon application for Hong / Kong Offer Shares. / If yo

### col_CF
  - p15: (66.7) / (2,498,591) / (65.2) / Gross profit . . . . . . . . . . . / 628,668 / 26.1 / 891,842
  - p15: (66.7) / (2,498,591) / (65.2) / Gross profit . . . . . . . . . . . / 628,668 / 26.1 / 891,842

### col_CG
  - p20: 3,073,846 / 3,633,951 / As of December 31, 2022, we recorded net current liabilities of RMB103.3 million, / which was primarily attributable to capital expenditures related to the construction of our / production facilities in Dongguan and the purchase of equipment for our production facilities / in Huangshi, which led to an increase in trade and bills payables as at the end of 2022. We / reversed
  - p20: 3,073,846 / 3,633,951 / As of December 31, 2022, we recorded net current liabilities of RMB103.3 million, / which was primarily attributable to capital expenditures related to the construction of our / production facilities in Dongguan and the purchase of equipment for our production facilities / in Huangshi, which led to an increase in trade and bills payables as at the end of 2022. We / reversed

### col_CH
  - p311: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the / accountants’ report, a true and fair view of the financial position of the Group and the / Company as at 31 December 2022, 2023 and 2024 and 30 September 2025 and of the financial / perfor
  - p15: personnel with specialized skills, including senior R&D personnel and skilled engineers. / SUMMARY OF HISTORICAL AND FINANCIAL INFORMATION / The summary of consolidated financial information should be read together with the / consolidated financial information to the Accountants’ Report set out in Appendix I to this / Prospectus, including the accompanying notes and the information set out in “Fin

### col_CI
  - p25: LISTING EXPENSES / Listing expenses represent professional fees, underwriting commissions and other fees / (such as the discretionary incentive fee) incurred in connection with the Global Offering. We / estimate that our listing expenses will be approximately RMB115.8 million (or HK$131.1
  - p25: LISTING EXPENSES / Listing expenses represent professional fees, underwriting commissions and other fees / (such as the discretionary incentive fee) incurred in connection with the Global Offering. We / estimate that our listing expenses will be approximately RMB115.8 million (or HK$131.1


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 1989.HK`
有 ERROR 必须回原文修正。
