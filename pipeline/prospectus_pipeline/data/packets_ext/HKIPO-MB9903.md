# 9903.HK 扩展 18 列抽取包

公司：9903.HK Shanghai Iluvatar CoreX Semiconductor Co., Ltd. - H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB9903.json`。
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
- 股本结构（**已确认，不要改**）：L=254317736 M=25431800 N=228885936 O=228885936 P=0 Q=25431800 R=22888600 S=2543200
- 财务期间（**已确认**）：year-1 期末 = 30/06/25；币种 = RMB；year-1 净利 = -1218632000
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
{"code":"9903.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  9903.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 9903.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p25: OUR PRE-IPO INVESTORS / We have concluded several rounds of Pre-IPO Investments with a broad and diversified / base of Pre-IPO Investors. For further details of the identity and background of the Pre-IPO / Investors, and the principal terms of the Pre-IPO Investments, see ‘‘History, Development and / Corporate Structure — Pre-IPO Investments.’’
  - p25: OUR PRE-IPO INVESTORS / We have concluded several rounds of Pre-IPO Investments with a broad and diversified / base of Pre-IPO Investors. For further details of the identity and background of the Pre-IPO / Investors, and the principal terms of the Pre-IPO Investments, see ‘‘History, Development and
  - p25: OUR PRE-IPO INVESTORS / We have concluded several rounds of Pre-IPO Investments with a broad and diversified / base of Pre-IPO Investors. For further details of the identity and background of the Pre-IPO / Investors, and the principal terms of the Pre-IPO Investments, see ‘‘History, Development and / Corporate Structure — Pre-IPO Investments.’’

### col_BB
  - p138: issuance and listing is prohibited by laws, administrative regulations or the relevant provisions / of the state; where the overseas issuance and listing is recognized by the relevant competent / department of the State Council in accordance with the law may jeopardize national security; / where domestic enterprises or their controlling shareholders or de facto controllers are involved / in crimin
  - p37: ‘‘%’’ / per cent / In this prospectus, the terms ‘‘associate,’’ ‘‘close associate,’’ ‘‘connected person,’’ ‘‘core / connected person,’’ ‘‘connected transaction,’’ ‘‘substantial shareholder,’’ and ‘‘subsidiary’’ shall / have the meanings ascribed to such terms under the Listing Rules, unless the context otherwise / requires. / Certain amounts and percentage figures included in this prospectus have 
  - p163: Set forth below is a description of all of our Pre-IPO Investors. To the best knowledge of / the Company, save for the Centurium Capital Entities (as defined below), which will hold in / excess of 10% of the issued Shares and constitute core connected persons of our Company upon / Listing, each of the Pre-IPO Investors, together with their respective ultimate beneficial owners, / is an Independent

### col_BC
  - p138: issuance and listing is prohibited by laws, administrative regulations or the relevant provisions / of the state; where the overseas issuance and listing is recognized by the relevant competent / department of the State Council in accordance with the law may jeopardize national security; / where domestic enterprises or their controlling shareholders or de facto controllers are involved / in crimin
  - p37: ‘‘%’’ / per cent / In this prospectus, the terms ‘‘associate,’’ ‘‘close associate,’’ ‘‘connected person,’’ ‘‘core / connected person,’’ ‘‘connected transaction,’’ ‘‘substantial shareholder,’’ and ‘‘subsidiary’’ shall / have the meanings ascribed to such terms under the Listing Rules, unless the context otherwise / requires. / Certain amounts and percentage figures included in this prospectus have 
  - p598: The general partner of each of the Employee Shareholding Platforms and the indirect / shareholding platforms of the Direct Employee Shareholding Platforms is Shanghai Shuqi. The / above arrangement of the equity incentive schemes could offer incentives to the participants / through granting them indirect interest in our Shares while allowing our core management team / to retain control on the voti

### col_BD
  - p138: issuance and listing is prohibited by laws, administrative regulations or the relevant provisions / of the state; where the overseas issuance and listing is recognized by the relevant competent / department of the State Council in accordance with the law may jeopardize national security; / where domestic enterprises or their controlling shareholders or de facto controllers are involved / in crimin
  - p24: single member holds a veto right or casting vote. / Shanghai Shuqi is the general partner of each of Shanghai Xishi, Shanghai Yishi, Shanghai / Sushi, Shanghai Nashi, Shanghai Yueshi, Shanghai Yuanshi and Shanghai Qiongyu (the / ‘‘Shareholding Platforms’’). Shanghai Shuqi is responsible for exercising the voting rights of the / Shareholding Platforms in our Company and is required to act in accord
  - p37: ‘‘%’’ / per cent / In this prospectus, the terms ‘‘associate,’’ ‘‘close associate,’’ ‘‘connected person,’’ ‘‘core / connected person,’’ ‘‘connected transaction,’’ ‘‘substantial shareholder,’’ and ‘‘subsidiary’’ shall / have the meanings ascribed to such terms under the Listing Rules, unless the context otherwise / requires. / Certain amounts and percentage figures included in this prospectus have 

### col_BE
  - p333: operations. We expect to fund our future working capital and other cash requirements with / existing cash and cash equivalents, income generated from our products and solutions, the net / proceeds from Global Offering and, when necessary, bank and other borrowings. / As of October 31, 2025, the most recent practicable date for determining our indebtedness, / we had cash and cash equivalents of RMB
  - p20: RMB2,296.0 million as of June 30, 2025, primarily due to the increase of RMB1,399.6 million in / cash and cash equivalents and the increase of RMB259.0 million in prepayments, other / receivables and other assets. Such an increase was partially offset by an increase of RMB17.7 / million in interest-bearing bank and other borrowings. / Our net current assets decreased from RMB600.7 million as of De
  - p20: RMB2,296.0 million as of June 30, 2025, primarily due to the increase of RMB1,399.6 million in / cash and cash equivalents and the increase of RMB259.0 million in prepayments, other / receivables and other assets. Such an increase was partially offset by an increase of RMB17.7 / million in interest-bearing bank and other borrowings. / Our net current assets decreased from RMB600.7 million as of De

### col_BF
  - p13: solution / iteration, / mature / commercialization / capabilities / and / continuously
  - p15: Research and development forms the foundation of our sustained growth and competitive / strength in the industry. We are committed to continuous innovation, guided by the principle of / integrated design and independent development encompassing both hardware and software. We / maintain a strategic ‘‘three-generation’’ R&D philosophy: one generation in mass production, / one in design, and one in p
  - p417: The Group is in the process of making an assessment of the impact of these new and revised HKFRS Accounting / Standards upon initial application. HKFRS 18 introduces new requirements for presentation within the statement of / profit or loss and other comprehensive income, including specified totals and subtotals. Entities are required to classify / all income and expenses within the statement of p

### col_BG
  - p26: (4.82) / For more details, please refer to note 30(b) to the Accountant’s Report in Appendix I to / this prospectus / FUTURE PLANS AND USE OF PROCEEDS / We estimate the net proceeds of the Global Offering which we will receive, based on the / Offer Price of HK$144.60 per Offer Share, will be approximately HK$3,478.6 million, after / deduction of underwriting fees and commissions and estimated expe
  - p340: material covenants on any of our outstanding debts which could significantly limit our ability to / undertake additional debt or equity financing, nor was there any breach of covenants. Our / Directors further confirm that we did not experience difficulty in obtaining borrowings, default / in repayment of borrowings or lessors during the Track Record Period and up to the Latest / Practicable Date.
  - p26: (4.82) / For more details, please refer to note 30(b) to the Accountant’s Report in Appendix I to / this prospectus / FUTURE PLANS AND USE OF PROCEEDS / We estimate the net proceeds of the Global Offering which we will receive, based on the / Offer Price of HK$144.60 per Offer Share, will be approximately HK$3,478.6 million, after / deduction of underwriting fees and commissions and estimated expe

### col_BI
  - p2: Total number of Offer Shares under the / Global Offering / : / 25,431,800 H Shares / Number of Hong Kong Offer Shares / : / 2,543,200 H Shares (subject to reallocation)

### col_BP
  - p355: The Huatai Ultimate Client is a domestic private securities investment fund managed by / Hengxin Fund Management in its capacity as fund manager. Hengxin Fund Management is a / private fund management company registered with the Asset Management Association of / China. Hengxin Fund Management was filed and established on September 9, 2016, with a fund / size of over RMB500 million. Its principal b
  - p1: 上海天數智芯半導體股份有限公司 / Sole Sponsor, Sponsor-overall Coordinator / Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers / (A joint stock company incorporated in the People’s Republic of China with limited liability) / Stock Code：9903 / GLOBAL OFFERING

### col_BR
  - p96: No. 2168 Chenhang Road / Minhang District / Shanghai, China / Principal Place of Business in Hong / Kong / 40/F, Dah Sing Financial Centre / No. 248 Queen’s Road East
  - p96: Headquarters and Registered Office in / the PRC / Room 101, Building 3 / No. 2168 Chenhang Road

### col_BT
  - p17: Non-HKFRS Measure / We define adjusted net loss (non-HKFRS measure) as net loss for the year/period adjusted / by adding back share-based payment expenses. / To supplement our consolidated financial statements, we also use adjusted net loss
  - p31: Hong Kong Financial Reporting Standards / ‘‘HKFRS Accounting / Standards’’ / HKFRS Accounting Standards, which include all Hong Kong / Financial Reporting Standards, Hong Kong Accounting Standards / (HKASs) and Interpretations as issued by the Hong Kong Institute / of Certified Public Accountants
  - p70: various assumptions of unobservable inputs, which may fluctuate according to the changes in / the unobservable inputs. The fair value of a financial instrument is the amount that would be / received if an asset is sold or paid to transfer a liability in an orderly transaction between market / participants at the measurement date. In line with our accounting policies, we establish a fair / value hi

### col_CC
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, our Company will issue an announcement to be published on the website of the Stock / Exchange at www.hkexnews.hk and the website of our Company at www.iluvatar.com. / Date(1)
  - p5: Offering, our Company will issue an announcement to be published on the website of the Stock / Exchange at www.hkexnews.hk and the website of our Company at www.iluvatar.com. / Date(1) / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . .9: 00 a.m. on / Tuesday, December 30, 2025 / Latest time to complete electronic applications / under White Form eIPO ser

### col_CD
  - p5: If there is any change in the following expected timetable of the Hong Kong Public / Offering, our Company will issue an announcement to be published on the website of the Stock / Exchange at www.hkexnews.hk and the website of our Company at www.iluvatar.com. / Date(1)

### col_CE
  - p360: (1) / Subject to rounding down to the nearest whole board lot of 100 Offer Shares. Calculated based on the / exchange rate set out in the section headed ‘‘Information about this Prospectus and the Global Offering — / Exchange Rate Conversion’’. The exact number of H Shares to be subscribed by the Cornerstone Investors / will be subject to the exchange rate as prescribed in the relevant cornerstone

### col_CF
  - p16: (54.9) / (161,830) / (49.9) / Gross profit / 112,412 / 59.4 / 143,151
  - p16: (54.9) / (161,830) / (49.9) / Gross profit / 112,412 / 59.4 / 143,151

### col_CG
  - p43: . / our financial condition and performance; / . / our capital expenditure plans; / . / our dividend policy; / .
  - p43: . / our financial condition and performance; / . / our capital expenditure plans; / . / our dividend policy; / .
  - p494: RMB’000 / RMB’000 / Contracted, but not provided for: / Purchase of property, plant and equipment / and intangible assets / 3,989 / 1,590

### col_CH
  - p399: We believe that the evidence we have obtained is sufficient and appropriate to provide a / basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purposes of the / accountants’ report, a true and fair view of the financial position of the Group and the / Company as at 31 December 2022, 2023 and 2024 and 30 June 2025 and of the financial / performance
  - p28: RECENT DEVELOPMENT AND NO MATERIAL ADVERSE CHANGE / Our Directors confirm that there has been no material adverse change in our business, / financial condition and results of operations since June 30, 2025, being the latest balance sheet / date of our consolidated financial statements in the Accountants’ Report set out in Appendix I / to this prospectus, and up to the date of this prospectus. We h

### col_CI
  - p17: 54.2 / 295,859 / 91.2 / Listing expenses(2) / — / — / —
  - p17: 54.2 / 295,859 / 91.2 / Listing expenses(2) / — / — / —
  - p370: UNDERWRITING COMMISSIONS AND LISTING EXPENSES / The Underwriters and the Capital Market Intermediaries will receive an underwriting / commission equal to 3.0% of the aggregate Offer Price payable for the Offer Shares, out of / which they will pay any sub-underwriting commissions and other fees (the ‘‘Fixed Fees’’). Our


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 9903.HK`
有 ERROR 必须回原文修正。
