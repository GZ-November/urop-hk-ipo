# 2715.HK 扩展 18 列抽取包

公司：2715.HK ESTUN AUTOMATION CO., LTD - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB2715.json`。
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
- 股本结构（**已确认，不要改**）：L=967798453 M=96780000 N=871018453 O=871018453 P=0 Q=96780000 R=87102000 S=9678000
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = 39600000.0
- 行业分类（港交所官方）：701030 機器人系統及解決方案
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
{"code":"2715.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  2715.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 2715.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
（锚点无命中，需要自己 search）

### col_BB
  - p26: RMB1,892.7 million as of December 31, 2024, primarily driven by (i) the recognition of a loss / for the year of RMB817.7 million and other comprehensive income of RMB57.6 million, (ii) / dividends approved in respect of the previous year of RMB52.0 million, and (iii) appropriation / of dividends to non-controlling shareholders of subsidiaries of RMB21.6 million, partially / offset by equity-settle
  - p48: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Takeovers Code” / the Code on Takeovers and Mergers and Share Buybacks
  - p36: Ltd. (南京工藝裝備製造股份有限公司) (“Nanjing Technical Equipment”) held by our Group / in exchange for approximately 1.89% equity interest in Nanjing Chemical Fibre (the / “Proposed Transaction”), which forms part of the asset restructuring of Nanjing Chemical / Fibre. Nanjing Chemical Fibre and its ultimate beneficial owner (being State-owned Assets / Supervision and Administration Commission of Nanjing Munic

### col_BC
  - p26: RMB1,892.7 million as of December 31, 2024, primarily driven by (i) the recognition of a loss / for the year of RMB817.7 million and other comprehensive income of RMB57.6 million, (ii) / dividends approved in respect of the previous year of RMB52.0 million, and (iii) appropriation / of dividends to non-controlling shareholders of subsidiaries of RMB21.6 million, partially / offset by equity-settle
  - p48: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Takeovers Code” / the Code on Takeovers and Mergers and Share Buybacks

### col_BD
  - p26: RMB1,892.7 million as of December 31, 2024, primarily driven by (i) the recognition of a loss / for the year of RMB817.7 million and other comprehensive income of RMB57.6 million, (ii) / dividends approved in respect of the previous year of RMB52.0 million, and (iii) appropriation / of dividends to non-controlling shareholders of subsidiaries of RMB21.6 million, partially / offset by equity-settle
  - p30: Immediately upon completion of the Global Offering (assuming the Over-allotment / Option is not exercised and options granted under the 2025 Share Option Scheme are not / exercised), the Controlling Shareholders Group will be entitled to exercise approximately / 37.94% voting rights in our Company. Therefore, the Controlling Shareholders Group will / continue to be our Controlling Shareholders Gro
  - p48: the State Council of the PRC (中華人民共和國國務院) / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / “Takeovers Code” / the Code on Takeovers and Mergers and Share Buybacks

### col_BE
  - p28: Quick ratio is calculated based on total current assets less inventories divided by total current liabilities / as of the dates indicated. / (4) / Debt-to-equity ratio is calculated as indebtedness divided by total equity as of the same date. / Indebtedness represents bank loans and other borrowings, as well as lease liabilities. The increases in / our debt-to-equity ratio throughout the Track Rec
  - p73: and Use of Proceeds” for details. We expect these investments will result in additional annual / depreciation charges, which may have a material adverse effect on our financial position and / results of operations. / Our interest-bearing indebtedness exposes us to interest rate risk and our level of / indebtedness may prevent us from meeting relevant obligations under our indebtedness, / which may
  - p26: by our suppliers, which were partially offset by (i) an increase in trade and other receivables / of RMB254.9 million, primarily driven by higher trade volumes with certain automotive / customers who had relatively long payment cycles, and (ii) a decrease in bank loans and other / borrowings of RMB117.6 million. / Our net current assets decreased from RMB668.1 million as of December 31, 2023, to /

### col_BF
  - p23: broader geographical penetration. This strategy allows us to scale effectively without bearing / the substantial costs typically associated with building and managing a large direct sales force. / According to Frost & Sullivan, this approach aligns with industry practices commonly adopted / by companies focused on the R&D and commercialization of robotic technologies. While we / maintain a strong 
  - p135: automation. Industrial robotic solutions are able to execute repetitive, high-precision / tasks uninterruptedly, boosting efficiency, shortening production cycles, and ensuring / consistent quality. This directly addresses rising labor costs, recruitment issues, and / manual errors, enabling high-quality mass production while optimizing labor structures. / This sustained demand fuels the expansion
  - p152: name services in the PRC. Communication administrative bureaus at provincial levels shall / conduct supervision and administration of the domain name services within their respective / administrative jurisdictions. Domain name registration services shall, in principle, be subject / to the principle of “first apply, first register”. A domain name registrar shall, in the process of / providing domai

### col_BG
  - p34: Legal Advisors are of the view that we can pay dividend despite accumulated losses except / when the accumulative amount of our statutory reserve is not sufficient to cover accumulated / losses, in which case the current year’s profits shall first be used to make up for the losses. / FUTURE PLANS AND USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approx
  - p34: Legal Advisors are of the view that we can pay dividend despite accumulated losses except / when the accumulative amount of our statutory reserve is not sufficient to cover accumulated / losses, in which case the current year’s profits shall first be used to make up for the losses. / FUTURE PLANS AND USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approx

### col_BI
  - p2: Number of Offer Shares under / the Global Offering / : / 96,780,000 H Shares (subject to the / Over-allotment Option) / Number of Hong Kong Offer Shares / :

### col_BP
  - p183: For the information of the minority shareholders, see notes under “— Our Shareholding and Corporate / Structure.” / (2) / Carl Cloos was established on June 30, 1977. Since 1919, the Cloos group has driven innovation in mechanical / technology, pioneering advancements from manual welding equipment to robotic automation systems within / welding technology and automation. On April 27, 2020, Cloos Ho
  - p1: G L O B A L / OFFERING / Stock Code : 2715 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / 南京埃斯頓自動化股份有限公司 / ESTUN AUTOMATION CO., LTD / Sole Sponsor, Sponsor-Overall Coordinator, Joint Global Coordinator,

### col_BR
  - p128: Jiangning, Nanjing / Jiangsu Province / PRC / Principal Place of Business in Hong Kong / 4/F, Jardine House / 1 Connaught Place / Central
  - p128: Registered Office / No. 1888 Jiyin Avenue / Jiangning, Nanjing / Jiangsu Province

### col_BT
  - p43: “IAS” / International Accounting Standards / “IFRS” / IFRS Accounting Standards issued by the International / Accounting Standards Board / “International Sanctions Legal / Advisers”
  - p43: Underwriting / Arrangements and Expenses” / “IAS” / International Accounting Standards / “IFRS” / IFRS Accounting Standards issued by the International / Accounting Standards Board
  - p31: September 30, 2025 and the unaudited consolidated results based on the management accounts / of the Group for the two months ended November 30, 2025, and an estimate of the consolidated / results of our Group for the remaining one month ended December 31, 2025. The Profit / Estimate has been prepared on the basis of the accounting policies consistent in all material / respects with those currently

### col_CC
  - p5: If there is any change to the expected timetable of the Hong Kong Public Offering, / we will issue an announcement on the respective websites of the Company at / www.estun.com and the Stock Exchange at www.hkexnews.hk. / The Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on
  - p5: If there is any change to the expected timetable of the Hong Kong Public Offering, / we will issue an announcement on the respective websites of the Company at / www.estun.com and the Stock Exchange at www.hkexnews.hk. / The Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on / Friday, February 27, 2026 / Latest time to complete electronic applicat

### col_CD
  - p5: If there is any change to the expected timetable of the Hong Kong Public Offering, / we will issue an announcement on the respective websites of the Company at / www.estun.com and the Stock Exchange at www.hkexnews.hk. / The Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on

### col_CE
  - p31: compliance records of the Company on the Shenzhen Stock Exchange. / APPLICATION FOR LISTING ON THE STOCK EXCHANGE / We have applied to the Listing Committee of the Stock Exchange for the granting of the / listing of, and permission to deal in our H Shares to be issued pursuant to the Global Offering / on the basis that, among other things, we satisfy the market capitalization/revenue test under / 
  - p4: for any other number of Hong Kong Offer Shares will be considered and such an / application is liable to be rejected. / If you are applying through the White Form eIPO service, you may refer to the / table below for the amount payable for the number of H Shares you have selected. You / must pay the respective maximum amount payable on application in full upon / application for Hong Kong Offer Shar

### col_CF
  - p24: (2,874,742) / (2,364,083) / (2,732,855) / Gross profit                 / 1,276,218 / 1,455,095 / 1,134,030
  - p24: (2,874,742) / (2,364,083) / (2,732,855) / Gross profit                 / 1,276,218 / 1,455,095 / 1,134,030

### col_CG
  - p25: which these subsidiaries’ customers operate primarily include construction machinery, heavy / industry, traditional automotive industry and packaging industry. In 2024, these industries were / affected by a combination of cyclical factors, such as a slowdown in global economic growth / that constrained capital expenditure, softer activity in the real estate sector, and reduced / demand in the trad
  - p25: which these subsidiaries’ customers operate primarily include construction machinery, heavy / industry, traditional automotive industry and packaging industry. In 2024, these industries were / affected by a combination of cyclical factors, such as a slowdown in global economic growth / that constrained capital expenditure, softer activity in the real estate sector, and reduced / demand in the trad
  - p381: products of RMB1,699.0 million. / Our net cash used in investing activities in 2024 was RMB192.5 million, primarily / attributable to (i) payments for the purchase of wealth management products amounting to / RMB1,773.2 million; and (ii) payments for purchase of property, plant and equipment, / intangible assets, and right-of-use assets of RMB281.9 million, partially offset by proceeds / from the 

### col_CH
  - p607: Company shall primarily adopt a cash dividend distribution policy, which stipulates: provided / that the Company maintains sustainable operations and long-term development and achieves / profitability in the current year with a positive accumulated undistributed profit balance, the / auditing firm shall issue an unqualified audit report for the Company’s financial statements of / that year (interi
  - p270: with revenue expected to reach USD51.8 billion by 2029, at a CAGR of 15.4% from / 2024 to 2029. We had ranked first among domestic manufacturers in China’s / industrial robotic solutions market for years, in terms of industrial robot shipment / volume, according to Frost & Sullivan. This leading position, in our opinion, / provides us with a unique advantage in capturing the growth potential of th
  - p31: of the Group for the two months ended November 30, 2025, and an estimate of the consolidated / results of our Group for the remaining one month ended December 31, 2025. The Profit / Estimate has been prepared on the basis of the accounting policies consistent in all material / respects with those currently adopted by our Group as summarized in the Accountants’ Report / as set out in Appendix I to 

### col_CI
  - p34: 10.0% of the net proceeds, or approximately HK$148.6 million, will be used for working / capital and general corporate purposes. / For details, see “Future Plans and Use of Proceeds.” / LISTING EXPENSES / Assuming that the Over-allotment Option is not exercised and an Offer Price of HK$16.18 / per Offer Share (being the mid-point of the indicative Price Range stated in this prospectus), / the aggr
  - p34: 10.0% of the net proceeds, or approximately HK$148.6 million, will be used for working / capital and general corporate purposes. / For details, see “Future Plans and Use of Proceeds.” / LISTING EXPENSES / Assuming that the Over-allotment Option is not exercised and an Offer Price of HK$16.18 / per Offer Share (being the mid-point of the indicative Price Range stated in this prospectus), / the aggr


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 2715.HK`
有 ERROR 必须回原文修正。
