# 0600.HK 扩展 18 列抽取包

公司：0600.HK Axera Semiconductor Co., Ltd. - H shares

## 任务
从招股书抽取下面 **18 个字段**，写成严格 JSON 到 `/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News/prospectus_pipeline/out_ext/extracted/HKIPO-MB0600.json`。
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
- 股本结构（**已确认，不要改**）：L=587760481 M=104915200 N=482845281 O=482845281 P=0 Q=104915200 R=94423600 S=10491600
- 财务期间（**已确认**）：year-1 期末 = 30/09/25；币种 = RMB；year-1 净利 = -1140933333.3333333
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
{"code":"0600.HK","fields":{"col_BA":{"value":1,"page":33,"quote":"<=200字符连续原文","confidence":"high"}}}
```
- `fields` 必须**恰好**包含下面 18 个 key，不多不少。
- 每个 entry 只能有 value / page / quote / confidence。
- `page` 整数；缺失写 null。`quote` ≤200 字符且必须是该页**连续**原文。
- 数值缺失写字符串 `"NaN"`；文本/日期缺失写字符串 `"NA"`。
- 日期一律 `dd/mm/yy`（如 `22/12/25`）。
- **不要**动其它 42 列——它们已完成。

## 允许的工具（只有这两个，禁止 ls/find/读源码/读别家 JSON/调 skill）
```bash
python3 prospectus_pipeline/tools_search.py pages  0600.HK 33,314,416
python3 prospectus_pipeline/tools_search.py search 0600.HK "正则" --context 3 --max 5
```


## 预计算候选原文（bundle 输出，¥0；可直接引用其中的页码）

### col_BA
  - p20: RMB3,065.4 million as of December 31, 2023, primarily due to an increase of RMB1,716.4 million in our / current liabilities, which was mainly attributable to the increase of RMB871.3 million in financial / instruments issued to investors, representing the shares with preferred rights issued to Pre-IPO Investors in / connection with the Pre-IPO Investments, which will be derecognized and transferre
  - p20: Our net current liabilities increased from RMB1,275.4 million as of December 31, 2022 to / RMB3,065.4 million as of December 31, 2023, primarily due to an increase of RMB1,716.4 million in our / current liabilities, which was mainly attributable to the increase of RMB871.3 million in financial / instruments issued to investors, representing the shares with preferred rights issued to Pre-IPO Invest
  - p20: RMB3,065.4 million as of December 31, 2023, primarily due to an increase of RMB1,716.4 million in our / current liabilities, which was mainly attributable to the increase of RMB871.3 million in financial / instruments issued to investors, representing the shares with preferred rights issued to Pre-IPO Investors in / connection with the Pre-IPO Investments, which will be derecognized and transferre

### col_BB
  - p27: of our Company. Additionally, assuming the Over-allotment Option is not exercised, Dr. QIU, Shanghai / Jinling, Jiaxing Zhixin, Jiaxing Aixin, Shanghai Bonasi and Xinsheng Bicheng Platforms will collectively / be entitled to exercise voting rights attaching to 18.70% of the total issued Shares of our Company. / Accordingly, our Company will no longer have any controlling shareholder. Instead, Dr. 
  - p38: subsidiary of Hong Kong Exchanges and Clearing Limited / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / – 29 –
  - p333: as the investment manager on a discretionary basis. FML is domiciled in Hong Kong and is licensed by the / SFC for the regulated activity of asset management (Type 9 license). FML is wholly owned by its founder / and chief investment officer, Mr. Barun Agarwal, an Independent Third Party. Save for Mr. Barun Agarwal, / no other ultimate beneficial owner of each of FMF and FML holds 10% or more of b

### col_BC
  - p27: of our Company. Additionally, assuming the Over-allotment Option is not exercised, Dr. QIU, Shanghai / Jinling, Jiaxing Zhixin, Jiaxing Aixin, Shanghai Bonasi and Xinsheng Bicheng Platforms will collectively / be entitled to exercise voting rights attaching to 18.70% of the total issued Shares of our Company. / Accordingly, our Company will no longer have any controlling shareholder. Instead, Dr. 
  - p38: subsidiary of Hong Kong Exchanges and Clearing Limited / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / – 29 –

### col_BD
  - p27: of our Company. Additionally, assuming the Over-allotment Option is not exercised, Dr. QIU, Shanghai / Jinling, Jiaxing Zhixin, Jiaxing Aixin, Shanghai Bonasi and Xinsheng Bicheng Platforms will collectively / be entitled to exercise voting rights attaching to 18.70% of the total issued Shares of our Company. / Accordingly, our Company will no longer have any controlling shareholder. Instead, Dr. 
  - p27: changes in the Board composition, Dr. QIU will no longer be able to control the majority of the Board seats / of our Company. Additionally, assuming the Over-allotment Option is not exercised, Dr. QIU, Shanghai / Jinling, Jiaxing Zhixin, Jiaxing Aixin, Shanghai Bonasi and Xinsheng Bicheng Platforms will collectively / be entitled to exercise voting rights attaching to 18.70% of the total issued Sh
  - p38: subsidiary of Hong Kong Exchanges and Clearing Limited / “subsidiary(ies)” / has the meaning ascribed thereto under the Listing Rules / “substantial shareholder(s)” / has the meaning ascribed thereto under the Listing Rules / – 29 –

### col_BE
  - p312: capital and other cash requirements with existing cash and cash equivalents, income generated from our / commercialized products, the net proceeds from Global Offering and, when necessary, bank and other / borrowings. / As of November 30, 2025, the most recent practicable date for determining our indebtedness, we had cash / and cash equivalents of RMB715.2 million. As of the same date, we had comm
  - p320: Interest Rate Risk / Interest rate risk is the risk that the fair value or future cash flows of a financial instrument will / fluctuate because of changes in market interest rates. Our interest rate risk arises primarily from time / deposits, cash at bank and interest-bearing borrowings. Our interest-bearing financial instruments at fixed / interest rates at the end of each year during the Track R
  - p25: working capital requirements. Prior to securing external financing, our finance department carefully evaluate the / purpose and necessity, then selects the most suitable solutions to fulfill cash needs. / During the Track Record Period, we financed our operations and other capital requirements primarily / through sales of our products, capital contributions from equity holders and bank borrowings.

### col_BF
  - p10: requirements of AI inference and the critical “perception” applications that drive real-world value. / We adopt the fabless model and focus solely on chip design and sales. Our proprietary technology / platform embodies an integrated and universal architecture, enabling efficient reuse of IP cores across / multiple applications. This scalable approach allows us to rapidly develop, commercialize, a
  - p25: SUMMARY / will minimize resource allocation to less impactful initiatives, ensuring efficient use of R&D budgets. We / also expect to realize higher cost efficiencies in the R&D process, particularly in tape-out, testing, and / packaging, driven by the increasing economies of scale from mass production. Additionally, we are taking / measures to optimize our cost structure and enhance our brand awa
  - p90: government publications and other sources, including information or data provided by China Insights / Consultancy. Unless otherwise indicated, the information has not been verified by us independently. This / statistical information may not be consistent with other statistical information from other sources within or / outside the PRC. While reasonable caution has been made in the process of repro

### col_BG
  - p28: statutory common reserve fund as described above. In light of our accumulated losses as disclosed in this / prospectus, it is unlikely that we will be eligible to pay a dividend out of our profits in the foreseeable / future. / FUTURE PLANS AND USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$2,790.1 million, after deducting underwritin
  - p318: During the Track Record Period and up to the Latest Practicable Date, there were no material / covenants on any of our outstanding debts which could significantly limit our ability to undertake additional / debt or equity financing, nor was there any breach of covenants. Our Directors further confirm that we did / not experience difficulty in obtaining borrowings, default in repayment of borrowing
  - p28: statutory common reserve fund as described above. In light of our accumulated losses as disclosed in this / prospectus, it is unlikely that we will be eligible to pay a dividend out of our profits in the foreseeable / future. / FUTURE PLANS AND USE OF PROCEEDS / We estimate that we will receive net proceeds from the Global Offering of approximately / HK$2,790.1 million, after deducting underwritin

### col_BI
  - p2: GLOBAL OFFERING / Number of Offer Shares in the Global Offering / : / 104,915,200 H Shares (subject to the Over- / allotment Option) / Number of Hong Kong Offer Shares / :

### col_BP
  - p178: We are a provider in China’s edge and visual on-device AI inference chip market. According to CIC, / we ranked as the fifth largest provider of visual on-device AI inference chips globally and the third largest / provider in China in the realm of edge AI inference in terms of shipment volume in 2024. Despite being / established only six years ago, we have already secured a market-leading position 
  - p1: GLOBAL OFFERING / (A joint stock company incorporated in the People’s Republic of China with limited liability) / Stock Code: 600 / Joint Sponsors, Overall Coordinators, Joint Global Coordinators, / Joint Bookrunners and Joint Lead Managers

### col_BR
  - p97: CORPORATE INFORMATION / Head Office, Registered Office and / Principal Place of Business in the PRC / Room 59, 17th Floor, Kechuang Building / No. 777 Zhongguan West Road / Zhuangshi Subdistrict, Zhenhai District
  - p97: CORPORATE INFORMATION / Head Office, Registered Office and / Principal Place of Business in the PRC / Room 59, 17th Floor, Kechuang Building / No. 777 Zhongguan West Road
  - p97: CORPORATE INFORMATION / Head Office, Registered Office and / Principal Place of Business in the PRC / Room 59, 17th Floor, Kechuang Building / No. 777 Zhongguan West Road

### col_BT
  - p275: You should read the following discussion and analysis in conjunction with our consolidated / financial statements, included in the Accountants’ Report in Appendix I to this prospectus, together / with the respective accompanying notes. Our consolidated financial information has been prepared / in accordance with IFRS Accounting Standards, which may differ in material aspects from / generally accep
  - p34: “Huatu” / Zhejiang Huatu and its subsidiaries / “IASB” / International Accounting Standards Board / – 25 –
  - p276: Further details of the material accounting policy information are set out in note 2 to the Accountants’ / Report as set out in Appendix I to this prospectus. The historical financial information also complies with / the relevant disclosure requirements of the Rules Governing the Listing of Securities on The Stock / Exchange of Hong Kong Limited. The accounting policies set out in the Accountants’ 

### col_CC
  - p5: EXPECTED TIMETABLE / If there is any change to the expected timetable of the Hong Kong Public Offering, we will issue / an announcement to be published on the website of the Hong Kong Stock Exchange at / www.hkexnews.hk and our website at www.axera-tech.com.
  - p5: If there is any change to the expected timetable of the Hong Kong Public Offering, we will issue / an announcement to be published on the website of the Hong Kong Stock Exchange at / www.hkexnews.hk and our website at www.axera-tech.com. / Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . / 9:00 a.m. on Friday, / January 30, 2026 / Latest time to c

### col_CD
  - p5: EXPECTED TIMETABLE / If there is any change to the expected timetable of the Hong Kong Public Offering, we will issue / an announcement to be published on the website of the Hong Kong Stock Exchange at / www.hkexnews.hk and our website at www.axera-tech.com.

### col_CE
  - p252: filing materials, and the CSRC will update the public filing information accordingly. / Listing Approval by the Stock Exchange / We have applied to the Listing Committee for the granting of listing of, and permission to deal in, our / H Shares to be issued pursuant to the Global Offering and the H Shares to be converted from 482,845,281 / Unlisted Shares on the Stock Exchange, which is subject to 
  - p165: public float. / Upon Listing, our Company will satisfy the public float requirement under Rule 19A.13A(1) of the / Listing Rules, which states that, in the event the expected market value of the Company’s H Shares upon / Listing is over HK$6 billion but does not exceed HK$30 billion, the minimum number of H shares held by / the public at the time of Listing as a percentage of the total issued Shar

### col_CF
  - p16: (79.0) (200,693) / (78.9) (212,070) / (78.8) / Gross profit / 12,994 / 25.9 / 59,244
  - p16: (79.0) (200,693) / (78.9) (212,070) / (78.8) / Gross profit / 12,994 / 25.9 / 59,244

### col_CG
  - p66: value change of financial instruments issued to investors is expected to be recognized afterwards, we cannot / assure you that we will not record net liabilities or net current liabilities in the future. If we are unable to / maintain adequate working capital or obtain sufficient financings, we may not have sufficient cash flows to / fund our business, operations and capital expenditure and our bu
  - p66: value change of financial instruments issued to investors is expected to be recognized afterwards, we cannot / assure you that we will not record net liabilities or net current liabilities in the future. If we are unable to / maintain adequate working capital or obtain sufficient financings, we may not have sufficient cash flows to / fund our business, operations and capital expenditure and our bu
  - p315: Investing Activities / For the nine months ended September 30, 2025, our net cash used in investing activities was / RMB485.0 million, primarily attributable to (i) payment for purchase of financial assets measured at FVPL / of RMB1,306.5 million, and (ii) payment for purchase of property, plant and equipment and intangible / assets of RMB143.7 million, partially offset by (i) proceeds from dispos

### col_CH
  - p378: Financial Information. / We believe that the evidence we have obtained is sufficient and appropriate to provide a basis for our opinion. / Opinion / In our opinion, the Historical Financial Information gives, for the purpose of the accountants’ report, a true and fair view of the / Company’s and the Group’s financial position as at December 31, 2022, 2023 and 2024 and September 30, 2025, and of th
  - p16: SUMMARY OF HISTORICAL FINANCIAL INFORMATION / The summary of the key financial information set forth below have been derived from and should be / read in conjunction with our consolidated financial statements, including the accompanying notes, set forth / in the Accountants’ Report as set out in Appendix I to this prospectus, as well as the information set forth in / the section headed “Financial 

### col_CI
  - p17: changes of the redemption rights granted by us, which is non-cash in nature and will be reclassified to equity after / the termination of the investors’ redemption rights upon Listing, (ii) equity settled share-based payment, which / was non-cash in nature and represented the employee benefit expenses incurred in connection with our award to / management and key employees, and (iii) Listing expens
  - p17: changes of the redemption rights granted by us, which is non-cash in nature and will be reclassified to equity after / the termination of the investors’ redemption rights upon Listing, (ii) equity settled share-based payment, which / was non-cash in nature and represented the employee benefit expenses incurred in connection with our award to / management and key employees, and (iii) Listing expens


## 自检
写完后运行：
`python3 prospectus_pipeline/run.py validate_ext --only 0600.HK`
有 ERROR 必须回原文修正。
