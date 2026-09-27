# 2692.HK 扩展 18 列抽取包

公司：2692.HK Shenzhen Zhaowei Machinery & Electronics Co., Ltd. - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB2692.json`。
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
- 股本结构（**已确认，不要改**）：L=267482700 M=26748300 N=240734400 O=240734400 P=0 Q=26748300 R=24073400 S=2674900
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = 242813333.33333334
- 行业分类（港交所官方）：101020 工業零件及器材
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
{"code":"2692.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  2692.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 2692.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
（锚点无命中，需要自己 search）

### col_BB
  - p20: limited control. To the extent there are any significant seasonal fluctuations different from our prior / experience, we must arrange for relevant supplies and manufacturing capacity in an effective manner, to / ensure we can dynamically meet the market demand. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, our Company was controlled by a group of Controlling / Shareholders, c
  - p33: “%” / Percent / In this prospectus, the terms “associate,” “close associate,” “connected person,” “core connected / person,” “connected transaction,” “controlling shareholder” and “substantial shareholder” shall have the / meanings given to such terms in the Listing Rules, unless the context otherwise requires. / Certain amounts and percentage figures included in this prospectus have been subject 
  - p278: Asset / Management”) acts as the investment advisor or investment manager on a discretionary basis of no more / than six investment funds and/or separated managed accounts (collectively the “Perseverance Funds”). No / single ultimate beneficial owner holds 30% or more interest in each of the Perseverance Funds. Each of / the Perseverance Funds is an Independent Third Party. Perseverance Asset Mana

### col_BC
  - p20: limited control. To the extent there are any significant seasonal fluctuations different from our prior / experience, we must arrange for relevant supplies and manufacturing capacity in an effective manner, to / ensure we can dynamically meet the market demand. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, our Company was controlled by a group of Controlling / Shareholders, c
  - p33: “%” / Percent / In this prospectus, the terms “associate,” “close associate,” “connected person,” “core connected / person,” “connected transaction,” “controlling shareholder” and “substantial shareholder” shall have the / meanings given to such terms in the Listing Rules, unless the context otherwise requires. / Certain amounts and percentage figures included in this prospectus have been subject 
  - p215: none of our Directors and members of the senior management is related to other Directors and / members of the senior management; / (4) / each of our Directors did not have any interest in our Shares within the meaning of Part XV / of the SFO; / (5) / to the best knowledge, information and belief of our Directors having made all reasonable

### col_BD
  - p20: limited control. To the extent there are any significant seasonal fluctuations different from our prior / experience, we must arrange for relevant supplies and manufacturing capacity in an effective manner, to / ensure we can dynamically meet the market demand. / OUR CONTROLLING SHAREHOLDERS / As of the Latest Practicable Date, our Company was controlled by a group of Controlling / Shareholders, c
  - p20: Shareholders, comprising (i) Mr. Li, our executive Director and chairman of the Board, together with / Zhaowei Investment, an entity controlled by him, and (ii) Ms. Xie, our executive Director, vice / chairwoman of the Board and the spouse of Mr. Li, through Qingmo Partnership where she acted as the / general partner, collectively being able to exercise an aggregate 62.40% voting rights in our Com
  - p33: “%” / Percent / In this prospectus, the terms “associate,” “close associate,” “connected person,” “core connected / person,” “connected transaction,” “controlling shareholder” and “substantial shareholder” shall have the / meanings given to such terms in the Listing Rules, unless the context otherwise requires. / Certain amounts and percentage figures included in this prospectus have been subject 

### col_BE
  - p67: an unexpected business interruption resulting from operational breakdowns, natural disasters, / or major changes in our key personnel or senior management; / • / adverse market reaction to any indebtedness that we may incur or securities that we may issue / in the future; / • / announcements of competitive developments, acquisitions or strategic alliances in our
  - p18: current asset items, mainly including (1) our cash and cash equivalents, trade and notes receivables and / inventories, generally in line with our sales growth and business expansion over the same period; and (2) / financial assets at FVTPL as we increased our investments in certain wealth management products, / partially offset by an increase in the current portion of interest-bearing bank borrow
  - p18: current asset items, mainly including (1) our cash and cash equivalents, trade and notes receivables and / inventories, generally in line with our sales growth and business expansion over the same period; and (2) / financial assets at FVTPL as we increased our investments in certain wealth management products, / partially offset by an increase in the current portion of interest-bearing bank borrow

### col_BF
  - p11: gearbox, and standardized product range for versatile applications. Moreover, we have developed / highly-integrated micro drive modules that power our dexterous hand product, capable of precisely / replicating human grip and fine-motion control. As the first company in China to introduce a / commercialized high-degree-of-freedom dexterous hand product, we have established collaborative / partnersh
  - p11: drive control within compact product dimensions. We developed China’s smallest 3.4mm micro / transmission system; we are the world’s first company to mass-produce micro transmission systems under / 6mm with high quality and efficiency; we have also achieved a technological breakthrough in our 4mm / brushless coreless motor and now possess the capability for mass production. / Our tri-integrated
  - p346: Effective for annual/reporting periods beginning on or after 1 January 2027 / 3 / No mandatory effective date yet determined but available for adoption / The Group is in the process of making an assessment of the impact of these revised IFRS Accounting Standards upon initial / application. So far, the Group considers that these new and revised IFRS Accounting Standards, except for IFRS 18, may res

### col_BG
  - p23: USE OF PROCEEDS / We estimate that the net proceeds from the Global Offering will be approximately HK$1,892.3 / million (after deducting the estimated underwriting commissions and other fees and expenses payable by / us in connection with the Global Offering), assuming an Offer Price of HK$73.68 per H Share, being the
  - p267: paid of RMB8.7 million, partially offset by new bank borrowings of RMB320.9 million. / Net cash flows from financing activities was RMB77.3 million in 2024, primarily due to new bank / borrowings of RMB192.9 million and proceeds from issue of restricted shares of RMB27.0 million, / partially offset by dividends paid of RMB93.5 million and repayment of bank borrowings of RMB35.0 / million. / Net ca
  - p23: • / approximately 10.0%, or HK$189.2 million, will be used for working capital and general / corporate purposes. / See “Future Plans and Use of Proceeds—Use of Proceeds.” / PROFIT ESTIMATE FOR THE YEAR ENDED DECEMBER 31, 2025 / We have prepared the following profit estimate for the year ended December 31, 2025. / Estimated consolidated profit attributable to

### col_BI
  - p2: Number of Offer Shares under the / Global Offering / : / 26,748,300 H Shares / Number of Hong Kong Offer Shares / : / 2,674,900 H Shares (subject to reallocation)

### col_BP
  - p26: “Dongguan Zhaowei” / Dongguan Zhaowei Machinery & Electronics Co., Ltd. (東莞市兆 / 威機電有限公司), a PRC company established on October 31, / 2018, one of our subsidiaries / “EAR” / United States Export Administration Regulations, 15 C.F.R. Parts
  - p1: Stock Code : 2692 / (a joint stock company incorporated in the People’s Republic of China with limited liability) / 深圳市兆威機電股份有限公司 / Shenzhen Zhaowei Machinery & Electronics Co., Ltd. / GLOBAL OFFERING

### col_BR
  - p94: Yanluo Subdistrict / Bao’an District, Shenzhen City / PRC / Headquarters and Principal Place of Business / in the PRC / Room 101, Office Building / No. 62 Yanhu Road, Yanchuan Community
  - p94: Registered Office in the PRC / Room 101, Office Building / No. 62 Yanhu Road, Yanchuan Community / Yanluo Subdistrict
  - p85: All of the H Shares issued pursuant to applications made in the Hong Kong Public Offering will be / registered on our H Share register of members to be maintained in Hong Kong by our H Share Registrar, / Tricor Investor Services Limited, at 17/F, Far East Finance Centre, 16 Harcourt Road, Hong Kong. Our / principal register of members will be maintained by us at our head office in the PRC. / Deali

### col_BT
  - p16: Non-IFRS Measure / To supplement our consolidated financial statements which are presented in accordance with IFRS / Accounting Standards, we also use adjusted net profit (non-IFRS measure) as additional financial measure, / which is not required by, or presented in accordance with, IFRS Accounting Standards. We believe that / such non-IFRS measure facilitate comparisons of operating performance f
  - p16: 14.5 / Non-IFRS Measure / To supplement our consolidated financial statements which are presented in accordance with IFRS / Accounting Standards, we also use adjusted net profit (non-IFRS measure) as additional financial measure, / which is not required by, or presented in accordance with, IFRS Accounting Standards. We believe that / such non-IFRS measure facilitate comparisons of operating perfor
  - p23: year ended December 31, 2025 based on the audited consolidated results of our Group for the nine months ended / September 30, 2025 and the unaudited consolidated results based on the management accounts of our Group for the / three months ended December 31, 2025. The profit estimate has been prepared on a basis consistent in all material / respects with our accounting policies, as presently adopte

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public Offering, / our Company will issue an announcement to be published on the website of the Stock Exchange at / www.hkexnews.hk and the website of our Company at http://www.szzhaowei.net. / Date(1)
  - p5: our Company will issue an announcement to be published on the website of the Stock Exchange at / www.hkexnews.hk and the website of our Company at http://www.szzhaowei.net. / Date(1) / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on / Friday, February 27, 2026 / Latest time to complete electronic applications under the / HK 

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public Offering, / our Company will issue an announcement to be published on the website of the Stock Exchange at / www.hkexnews.hk and the website of our Company at http://www.szzhaowei.net. / Date(1)

### col_CE
  - p132: by the public, at the time of the Listing, must (a) represent at least 10% of the Company’s total number / of issued Shares (excluding treasury shares): or (b) have an expected market value of not less than HK$3 / billion. / The total number of the H Shares to be issued pursuant to the Global Offering represents / approximately 10% of the enlarged issued share capital of the Company (assuming that
  - p4: Your application through the HK eIPO White Form service or the HKSCC EIPO channel / must be for a minimum of 100 Hong Kong Offer Shares and in one of the numbers set out in the / table. If you are applying through the HK eIPO White Form service, you may refer to the table / below for the amount payable for the number of H Shares you have selected. You must pay the / respective maximum amount payab

### col_CF
  - p16: (68.9) / (845,252) / (67.3) / Gross profit       / 335,110 / 29.1 / 349,091
  - p16: (68.9) / (845,252) / (67.3) / Gross profit       / 335,110 / 29.1 / 349,091

### col_CG
  - p37: • / our financial condition and performance; / • / our capital expenditure plans; / • / changes to the regulatory environment, policies, operating conditions of and general outlook in / the industries and markets in which we operate;
  - p37: • / our financial condition and performance; / • / our capital expenditure plans; / • / changes to the regulatory environment, policies, operating conditions of and general outlook in / the industries and markets in which we operate;

### col_CH
  - p328: We believe that the evidence we have obtained is sufficient and appropriate to provide a basis for / our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the accountants’ / report, a true and fair view of the financial position of the Group and the Company as at 31 December / 2022, 2023, 2024 and 30 September 2025 and of the financial performance
  - p16: decide to invest in our Shares. / SUMMARY OF FINANCIAL INFORMATION / The following tables present the summary of financial information for the Track Record Period and / should be read in conjunction with our financial information included in the Accountants’ Report in / Appendix I to this prospectus, including the notes thereto. / Summary of Consolidated Statements of Profit or Loss / The followin

### col_CI
  - p22: has been completed on September 30, 2025 but takes no account of any Shares which may be issued or repurchased / by our Company for the vesting of restricted A Shares and the exercise of share options under the 2024 Share Incentive / Scheme. / LISTING EXPENSES / We did not record listing expenses during the Track Record Period. We expect to incur a total of / approximately RMB69.7 million (HK$78.5
  - p22: has been completed on September 30, 2025 but takes no account of any Shares which may be issued or repurchased / by our Company for the vesting of restricted A Shares and the exercise of share options under the 2024 Share Incentive / Scheme. / LISTING EXPENSES / We did not record listing expenses during the Track Record Period. We expect to incur a total of / approximately RMB69.7 million (HK$78.5


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 2692.HK`
有 ERROR 必须回原文修正。
