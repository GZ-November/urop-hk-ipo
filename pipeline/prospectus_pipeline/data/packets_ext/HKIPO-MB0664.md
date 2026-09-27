# 0664.HK 扩展 18 列抽取包

公司：0664.HK Hangzhou Tongshifu Cultural and Creative (Group) Co., Ltd. - H Shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB0664.json`。
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
- 股本结构（**已确认，不要改**）：L=64406800 M=7406800 N=57000000 O=57000000 P=0 Q=7406800 R=6666100 S=740700
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = 55404000
- 行业分类（港交所官方）：232030 玩具及消閒用品
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
{"code":"0664.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  0664.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 0664.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p18: approximately 23.24% of the aggregate voting power of our enlarged share capital. For details, see / the section headed “Relationship with the Single Largest Shareholder” in this prospectus. / PRE-IPO INVESTORS / We have engaged in Pre-IPO Investments with our Pre-IPO Investors. Our Pre-IPO / Investments consist of several rounds of investments from the Pre-IPO Investors by way of transfer / of eq
  - p18: Over-allotment Option is not exercised), our Single Largest Shareholder will be able to exercise / approximately 23.24% of the aggregate voting power of our enlarged share capital. For details, see / the section headed “Relationship with the Single Largest Shareholder” in this prospectus. / PRE-IPO INVESTORS / We have engaged in Pre-IPO Investments with our Pre-IPO Investors. Our Pre-IPO / Investm
  - p18: approximately 23.24% of the aggregate voting power of our enlarged share capital. For details, see / the section headed “Relationship with the Single Largest Shareholder” in this prospectus. / PRE-IPO INVESTORS / We have engaged in Pre-IPO Investments with our Pre-IPO Investors. Our Pre-IPO / Investments consist of several rounds of investments from the Pre-IPO Investors by way of transfer / of eq

### col_BB
  - p95: regulations and relevant state rules; (ii) where the intended securities offering and listing may / endanger national security as reviewed and determined by competent authorities under the State / Council of the PRC in accordance with applicable laws; (iii) where the domestic company intending / to make the securities offering and listing, or its controlling shareholders and the actual controller,
  - p30: “subsidiary(ies)” / has the meaning ascribed to it in section 15 of the / Companies Ordinance / “substantial shareholder(s)” / has the meaning ascribed to it under the Listing Rules / “Tai Tong (太銅)” / A sub-brand of our Company dedicated to copper cultural

### col_BC
  - p95: regulations and relevant state rules; (ii) where the intended securities offering and listing may / endanger national security as reviewed and determined by competent authorities under the State / Council of the PRC in accordance with applicable laws; (iii) where the domestic company intending / to make the securities offering and listing, or its controlling shareholders and the actual controller,
  - p30: “subsidiary(ies)” / has the meaning ascribed to it in section 15 of the / Companies Ordinance / “substantial shareholder(s)” / has the meaning ascribed to it under the Listing Rules / “Tai Tong (太銅)” / A sub-brand of our Company dedicated to copper cultural

### col_BD
  - p95: regulations and relevant state rules; (ii) where the intended securities offering and listing may / endanger national security as reviewed and determined by competent authorities under the State / Council of the PRC in accordance with applicable laws; (iii) where the domestic company intending / to make the securities offering and listing, or its controlling shareholders and the actual controller,
  - p18: For more details, please refer to “Financial Information – Key Financial Ratios” in this / prospectus. / OUR SINGLE LARGEST SHAREHOLDER / As of the Latest Practicable Date, Mr. Yu held approximately 26.27% of the voting rights / in our Company. Immediately after completion of the Global Offering (assuming that the / Over-allotment Option is not exercised), our Single Largest Shareholder will be ab
  - p30: “subsidiary(ies)” / has the meaning ascribed to it in section 15 of the / Companies Ordinance / “substantial shareholder(s)” / has the meaning ascribed to it under the Listing Rules / “Tai Tong (太銅)” / A sub-brand of our Company dedicated to copper cultural

### col_BE
  - p239: 2023, 4.01% in 2024 and 3.75% in the nine months ended September 30, 2025. / The significant increase in current lease liabilities in 2024 was due to the lease payments / under newly added store leases. / INDEBTEDNESS / As of January 31, 2026, being the most recent practicable date for this indebtedness / statement, save as disclosed in this paragraph headed “Indebtedness” in this section, we did 
  - p226: to support our prototyping and sampling work. / Finance Costs / Finance costs declined from RMB0.9 million in 2022 to RMB5,000 in 2023, mainly as a / result of repaying interest-bearing bank borrowings. / Income Tax Expenses / Income tax expenses decreased by 50.8%, from RMB5.5 million in 2022 to RMB2.7 / million in 2023, primarily due to a lower level of profit before tax.
  - p186: Largest Shareholder and his respective close associates for financing after the Listing as we expect / that our working capital will be funded by the cash, cash equivalent on hand as well as the proceeds / from the Global Offering. Our Directors confirm that the only guarantee of RMB128,500,000 / provided by Mr. Yu for borrowings by our Company during the year ended December 31, 2022 was / fully r

### col_BF
  - p41: However, the commercial success of our products depends on the continuing strength and / protection of our intellectual property rights. If we fail to obtain patent or copyright registrations, / maintain the validity of our rights, or protect these rights from infringement or misuse, our ability / to commercialize new product concepts or preserve brand distinctiveness may be impaired. / Moreover, 
  - p90: (《中華人民共和國個人信息保護法》) which became effective on November 1, 2021. The PRC / Personal Information Protection Law stipulates the scope of personal information, sets out the rules / for processing personal information and the rules for cross-border transfer of personal information, / as well as clarifies the individual’s rights and the processor’s obligations in the process of personal / information pro

### col_BG
  - p19: fees and expenses of approximately HK$17.6 million. The listing expenses above are the current / estimate for reference only and the final amount to be recognized to our consolidated income / statement is subject to audit and the then changes in variables and assumptions. / FUTURE PLANS AND USE OF PROCEEDS / Assuming an Offer Price of HK$64.0 per Share (being the mid-point of the indicative Offer 
  - p19: fees and expenses of approximately HK$17.6 million. The listing expenses above are the current / estimate for reference only and the final amount to be recognized to our consolidated income / statement is subject to audit and the then changes in variables and assumptions. / FUTURE PLANS AND USE OF PROCEEDS / Assuming an Offer Price of HK$64.0 per Share (being the mid-point of the indicative Offer 

### col_BI
  - p2: Number of Offer Shares under / the Global Offering / : / 7,406,800 H Shares (subject to the / Over-allotment Option) / Number of Hong Kong Offer Shares / :

### col_BP
  - p98: ESTABLISHMENT AND DEVELOPMENT OF THE COMPANY / A. / Establishment of our Company / Our Company was established on March 26, 2013 with an initial registered capital of / RMB3 million. The shareholding structure of our Company at the time of our establishment were / as follows: / No.
  - p1: Stock Code : 0664 / (A joint stock company incorporated in the People’s Republic of China with limited liability) / GLOBAL OFFERING / Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager / Sole Sponsor, Sole Sponsor-Overall Coordinator, Joint Global Coordinator,

### col_BR
  - p293: As at September 30, 2025, Mr. Yu Guang (“Mr. Yu”), the founder, chairman and general manager of the Company / and its subsidiaries (the “Group”), holds 26.27% of the total share capital of the Company. His shareholding remained / unchanged throughout the Track Record Period. Mr. Yu is also the single largest shareholder of the Company. / The addresses of the registered office and principal place o
  - p71: Registered Office and Head Office / in the PRC / No. 777 Yading Road, Yangxi Subdistrict, / Jiande City,
  - p71: Registered Office and Head Office / in the PRC / No. 777 Yading Road, Yangxi Subdistrict, / Jiande City,

### col_BT
  - p207: You should read the following discussion and analysis with our consolidated financial / information, including the notes thereto, included in the Accountants’ Report as set out in / Appendix I to this prospectus. Our consolidated financial information has been prepared in / accordance with IFRS Accounting Standards, which may differ in material aspects from / generally accepted accounting principl
  - p25: we design, market, and sell our plastic figure and toy / products / “IAS” / International Accounting Standards / “IFRS” / the International Financial Reporting Standards, which as / collective
  - p159: We did not receive any third-party payments in the year ended December 31, 2024 or up to the / Latest Practicable Date. These instances were isolated, limited in scale, and not indicative of any / systemic or recurring practice within our distributor network. During the Relevant Period, we duly / recorded all such payments in accordance with our internal accounting policies and the applicable / ta

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on our Company’s / website at www.tongshifu.com and the website of the Hong Kong Stock Exchange at / www.hkexnews.hk.
  - p5: Offering, we will issue an announcement in Hong Kong to be published on our Company’s / website at www.tongshifu.com and the website of the Hong Kong Stock Exchange at / www.hkexnews.hk. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on Monday, / March 23, 2026 / Latest time to complete electronic applications under White Form / eIPO service thro

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, we will issue an announcement in Hong Kong to be published on our Company’s / website at www.tongshifu.com and the website of the Hong Kong Stock Exchange at / www.hkexnews.hk.

### col_CE
  - p18: “History, Development and Corporate Structure – Pre-IPO Investments.” / APPLICATION FOR LISTING ON THE STOCK EXCHANGE / We have applied to the Listing Committee for the granting of the listing of, and permission / to deal in (i) our H Shares to be issued pursuant to the Global Offering (including any H Shares / which may be issued pursuant to the exercise of the Over-allotment Option), and (ii) th
  - p264: it, on behalf of the International Underwriters, may over-allocate or effect short sales or any other / stabilizing transactions with a view to stabilizing or maintaining the market price of the Offer / Shares at a level higher than that which might otherwise prevail in the open market. Short sales / involve the sale by the Stabilizing Manager of a greater number of H Shares than the International

### col_CF
  - p11: 100.0 / 447,672 / 100.0 / The following table sets forth the breakdown of our gross profit and gross profit margin by / product categories during the Track Record Period. For further details of the trend discussion, / please refer to the section headed “Financial Information – Description of Selected Components of / Statements of Profit or Loss – Revenue – Sales Channel” in this prospectus.
  - p11: 100.0 / 447,672 / 100.0 / The following table sets forth the breakdown of our gross profit and gross profit margin by / product categories during the Track Record Period. For further details of the trend discussion, / please refer to the section headed “Financial Information – Description of Selected Components of / Statements of Profit or Loss – Revenue – Sales Channel” in this prospectus.

### col_CG
  - p229: including rental deposits and refunds totaling approximately RMB0.3 million, were also recognized / under investing activities. / For the year ended December 31, 2022, net cash used in investing activities amounted to / RMB19.2 million. This primarily comprised (i) capital expenditure of RMB22.1 million for / property, plant and equipment, and (ii) RMB3.3 million for intangible assets mainly relat
  - p229: including rental deposits and refunds totaling approximately RMB0.3 million, were also recognized / under investing activities. / For the year ended December 31, 2022, net cash used in investing activities amounted to / RMB19.2 million. This primarily comprised (i) capital expenditure of RMB22.1 million for / property, plant and equipment, and (ii) RMB3.3 million for intangible assets mainly relat
  - p346: Advances to suppliers                         / 4,942 / 5,954 / Prepayments for purchase of property, plant and equipment   / – / 310 / Prepaid expenses                           

### col_CH
  - p284: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the / accountants’ report, a true and fair view of the Group’s and the Company’s financial position as at / December 31, 2022, 2023 and 2024, and September 30, 2025 and of the Group’s financial 
  - p15: The following tables present our summary historical financial information for the periods / or as of the dates indicated. The summary historical financial information set forth below should be / read together with, and is qualified in its entirety by reference to, the historical financial / information included in the Accountants’ Report in Appendix I to this prospectus, including the / accompanyi

### col_CI
  - p15: 0.3 / (1,205) / 0.3 / Listing expenses        / – / – / –
  - p15: 0.3 / (1,205) / 0.3 / Listing expenses        / – / – / –


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 0664.HK`
有 ERROR 必须回原文修正。
