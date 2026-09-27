# 3200.HK 扩展 18 列抽取包

公司：3200.HK Shenzhen Han’s CNC Technology Co., Ltd. - H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB3200.json`。
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
- 股本结构（**已确认，不要改**）：L=475960952 M=50451800 N=425509152 O=425509152 P=0 Q=50451800 R=45406600 S=5045200
- 财务期间（**已确认**）：year-1 期末 = 31/10/25；币种 = RMB；year-1 净利 = 622702800
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
{"code":"3200.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  3200.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 3200.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
（锚点无命中，需要自己 search）

### col_BB
  - p35: OUR CONTROLLING SHAREHOLDERS GROUP / As of the Latest Practicable Date, Mr. Gao was interested in approximately 84.39% of the / total issued share capital of our Company through (i) Han’s Laser as to approximately 83.63% and / (ii) Dazu Holdings as to approximately 0.76%. Han’s Laser is a company listed on the Shenzhen
  - p47: “%” / per cent / In this Prospectus, the terms “associate,” “close associate,” “connected person,” “core / connected person,” “connected transaction” and “substantial shareholder” shall have the / meanings given to such terms in the Hong Kong Listing Rules, unless the context otherwise / requires. / Certain amounts and percentage figures included in this Prospectus have been subject to
  - p43: Ministry of Commerce of the PRC (中華人民共和國商務 / 部) / “Mr. Gao” / Mr. GAO Yunfeng (高雲峰), the ultimate beneficial owner / of / Dazu / Holdings

### col_BC
  - p35: OUR CONTROLLING SHAREHOLDERS GROUP / As of the Latest Practicable Date, Mr. Gao was interested in approximately 84.39% of the / total issued share capital of our Company through (i) Han’s Laser as to approximately 83.63% and / (ii) Dazu Holdings as to approximately 0.76%. Han’s Laser is a company listed on the Shenzhen
  - p47: “%” / per cent / In this Prospectus, the terms “associate,” “close associate,” “connected person,” “core / connected person,” “connected transaction” and “substantial shareholder” shall have the / meanings given to such terms in the Hong Kong Listing Rules, unless the context otherwise / requires. / Certain amounts and percentage figures included in this Prospectus have been subject to

### col_BD
  - p35: OUR CONTROLLING SHAREHOLDERS GROUP / As of the Latest Practicable Date, Mr. Gao was interested in approximately 84.39% of the / total issued share capital of our Company through (i) Han’s Laser as to approximately 83.63% and / (ii) Dazu Holdings as to approximately 0.76%. Han’s Laser is a company listed on the Shenzhen
  - p86: assets, election of directors and other significant corporate actions. Immediately following the / completion of the Global Offering (assuming the Over-allotment Option is not exercised), the / Controlling Shareholders Group will be together entitled to control the exercise of approximately / 71.45% of the voting rights and thus remain as the Controlling Shareholders Group of our / Company. The in
  - p47: “%” / per cent / In this Prospectus, the terms “associate,” “close associate,” “connected person,” “core / connected person,” “connected transaction” and “substantial shareholder” shall have the / meanings given to such terms in the Hong Kong Listing Rules, unless the context otherwise / requires. / Certain amounts and percentage figures included in this Prospectus have been subject to

### col_BE
  - p64: We may incur additional indebtedness, and increased cost of indebtedness in the future could / affect our business, results of operations and liquidity. / During the Track Record Period, we had certain borrowings to finance our business / operations and capital expenditures. We expect to continue to do so in the future and our liquidity
  - p24: receivables, inventories and prepayments, other receivables and other assets primarily driven by / our increased sales in the ten months ended October 31, 2025, partially offset by (i) an increase in / trade and bills payables and other payables and accruals driven by an increase in procurement to / respond to increased sales and by our expanded business scale; (ii) an increase in interest-bearing
  - p24: our increased sales in the ten months ended October 31, 2025, partially offset by (i) an increase in / trade and bills payables and other payables and accruals driven by an increase in procurement to / respond to increased sales and by our expanded business scale; (ii) an increase in interest-bearing / borrowings which served as flexible sources for our enhanced raw material procurement in / respo

### col_BF
  - p54: could result in our products becoming obsolete, leading to a potential loss of market share and / adversely affecting our business operations. However, there can be no assurance that our R&D / projects will yield the expected outcome or be completed within the anticipated time frame and / budget. If we fail to commercialize our R&D efforts, we may incur significant sunk costs. Even if / the newly 
  - p16: • / We plan to anchor our strategy in emerging sectors such as AI and intelligent NEVs, / collaborating closely with end-customers through joint R&D laboratories and full-chain / support from process validation to mass production; / • / We plan to expand our global business presence; / •
  - p207: As of the Latest Practicable Date, we had completed the acquisition of land; for certain / buildings, we had obtained the property ownership certificate, and for the remaining buildings, the / construction of main structures, and works on outdoor greening and fire protection, while interior / renovation and equipment installation were still in progress. We were also in the process of / obtaining t

### col_BG
  - p31: FUTURE PLANS AND USE OF PROCEEDS / Assuming that the Over-allotment Option is not exercised, after deducting the underwriting / commissions and other estimated offering expenses payable by us in connection with the Global / Offering, and assuming the maximum Offer Price of HK$95.80 per Share, we estimate that we will
  - p399: Net Cash Flows From/(Used) in Financing Activities / In the ten months ended October 31, 2025, our net cash flows generated from financing / activities were RMB473.8 million, primarily attributable to proceeds of borrowings from banks of / RMB1,610.8 million, partially offset by repayment of borrowings from banks of RMB1,024.7 / million. / In 2024, our net cash flows generated from financing activ
  - p31: FUTURE PLANS AND USE OF PROCEEDS / Assuming that the Over-allotment Option is not exercised, after deducting the underwriting / commissions and other estimated offering expenses payable by us in connection with the Global / Offering, and assuming the maximum Offer Price of HK$95.80 per Share, we estimate that we will

### col_BI
  - p2: Number of Offer Shares under the / Global Offering / : / 50,451,800 H Shares (subject to the Over-allotment / Option) / Number of Hong Kong Offer Shares / :

### col_BP
  - p165: MAJOR SHAREHOLDING CHANGES OF OUR COMPANY / Early Development of our Company and Conversion into a Joint Stock Limited Company / Our Company, then known as Shenzhen Han’s CNC Technology Limited (深圳市大族數控科 / 技有限公司), was established on April 22, 2002 in Shenzhen, PRC by Han’s Laser, a member of / the Controlling Shareholders Group, HAN Jinlong (韓金龍) and LUO Huicai (羅會才), both being / early investors 
  - p1: 深圳市大族數控科技股份有限公司 / SHENZHEN HAN’S CNC TECHNOLOGY CO., LTD. / (A joint stock company incorporated in the People’s Republic of China with limited liability) / Stock Code : 3200 / GLOBAL / OFFERING

### col_BR
  - p118: Bao’an District / Shenzhen, Guangdong Province / PRC / Principal Place of Business in / Hong Kong / Room 1916, 19/F, Lee Garden One / 33 Hysan Avenue, Causeway Bay
  - p118: Registered Office / No. 101 of Building 3, 1-2/F, 4/F and 7/F of / Building 3, and 1/F and 4/F of Building 4 / Han’s Laser Intelligence Manufacturing Center

### col_BT
  - p22: Non-IFRS Measure / To supplement our consolidated financial statements, which are presented in accordance with / IFRS Accounting Standards, we also use adjusted net profit (non-IFRS measure) as an additional / financial measure, which is not required by, or presented in accordance with IFRS Accounting / Standards. We believe this non-IFRS measure facilitates comparisons of operating performance / 
  - p482: requirements under the relevant rules and regulations in the jurisdictions of incorporation. / (ix) / The statutory financial statements of these entities for the years ended December 31, 2022, 2023 and 2024 prepared / under HKFRS Accounting Standards were audited by New Choice C.P.A. & Co. registered in Hong Kong. / (x) / The entity was a wholly-owned subsidiary of the Group as at December 31, 20
  - p22: Non-IFRS Measure / To supplement our consolidated financial statements, which are presented in accordance with / IFRS Accounting Standards, we also use adjusted net profit (non-IFRS measure) as an additional / financial measure, which is not required by, or presented in accordance with IFRS Accounting / Standards. We believe this non-IFRS measure facilitates comparisons of operating performance / 

### col_CC
  - p4: If there is any change in the following expected timetable of the Hong Kong Public Offering, / we will issue an announcement on the website of the Company at www.hanscnc.com and the / website of the Stock Exchange at www.hkexnews.hk. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9:00 a.m. on
  - p4: If there is any change in the following expected timetable of the Hong Kong Public Offering, / we will issue an announcement on the website of the Company at www.hanscnc.com and the / website of the Stock Exchange at www.hkexnews.hk. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9:00 a.m. on / Thursday, January 29, 2026 / Latest time fo

### col_CD
  - p4: If there is any change in the following expected timetable of the Hong Kong Public Offering, / we will issue an announcement on the website of the Company at www.hanscnc.com and the / website of the Stock Exchange at www.hkexnews.hk. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9:00 a.m. on

### col_CE
  - p108: APPLICATION FOR LISTING OF THE H SHARES ON THE HONG KONG STOCK / EXCHANGE / We have applied to the Hong Kong Stock Exchange for the granting of listing of, and / permission to deal in, our H Shares to be issued pursuant to the Global Offering (including any H / Shares which may be issued pursuant to the exercise of the Over-allotment Option). Dealings in / INFORMATION ABOUT THIS PROSPECTUS AND THE
  - p3: Hong Kong Offer Shares as set out in the table below. No application for any other number of / Hong Kong Offer Shares will be considered and such an application is liable to be rejected. / If you are applying through the HK eIPO White Form service, you may refer to the table / below for the amount payable for the number of H Shares you have selected. You must pay the / respective maximum amount pa

### col_CF
  - p21: (72.8) (1,935,634) / (73.8) (2,971,290) / (68.9) / Gross profit / . . . . . . . . . . . / 947,818 / 34.0
  - p21: (72.8) (1,935,634) / (73.8) (2,971,290) / (68.9) / Gross profit / . . . . . . . . . . . / 947,818 / 34.0

### col_CG
  - p56: effectively, and maintain our pricing and other competitive advantages. Our ability and efforts to / enhance our production capabilities are subject to significant risks and uncertainties, including: / • / our ability to obtain funding for the additional capital expenditures, working capital and / other corporate requirements to be used to enhance our production capabilities. We may / be unable to
  - p56: effectively, and maintain our pricing and other competitive advantages. Our ability and efforts to / enhance our production capabilities are subject to significant risks and uncertainties, including: / • / our ability to obtain funding for the additional capital expenditures, working capital and / other corporate requirements to be used to enhance our production capabilities. We may / be unable to

### col_CH
  - p144: under the State Council, inspect and accept the environmental protection facilities for supporting / construction and prepare an acceptance report. The environmental protection facilities supporting / the construction of these projects can only be put into production or use after they are qualified; If / it has not been accepted or unqualified, it shall not be put into production or use. If an ent
  - p633: We believe that the evidence we have obtained is sufficient and appropriate to provide a basis / for our opinion. / Opinion / In our opinion: / (a) / the Unaudited Pro Forma Financial Information has been properly compiled on the basis / stated;
  - p21: The following tables present our summary of consolidated financial data derived from our / consolidated statements of profit or loss, consolidated statements of financial position and / consolidated statements of cash flows for the years ended December 31, 2022, 2023, 2024 and the / ten months ended October 31, 2024 and 2025, included in the Accountants’ Report in Appendix I / to this Prospectus. 

### col_CI
  - p22: differently from similar terms used by other companies, and may not be comparable to other / similarly titled measures used by other companies. / We define adjusted net profit (non-IFRS measure) as profit for the year/period adjusted by / adding back/subtracting share-based payment compensation and adding back listing expenses. The / following table reconciles our adjusted net profit (non-IFRS mea
  - p22: differently from similar terms used by other companies, and may not be comparable to other / similarly titled measures used by other companies. / We define adjusted net profit (non-IFRS measure) as profit for the year/period adjusted by / adding back/subtracting share-based payment compensation and adding back listing expenses. The / following table reconciles our adjusted net profit (non-IFRS mea


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 3200.HK`
有 ERROR 必须回原文修正。
