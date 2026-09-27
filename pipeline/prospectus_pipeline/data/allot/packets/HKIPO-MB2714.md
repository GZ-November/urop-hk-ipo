# 配发结果公告抽取任务：2714.HK Muyuan Foods Co., Ltd. - H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**05/02/2026 22:18**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0205/2026020502402.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2714.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
```

- `fields` 必须包含下面**每一个** key，不能少、不能多、不能重复。
- 每个字段 entry 只能有 `value` / `page` / `quote` / `confidence` 四个键。
- `page` 是**本包中的整数页码**；缺失写 `null`。`quote` 是原文短摘录（≤200 字符）；缺失写 `""`。
- 数值字段缺失写字符串 `"NaN"`；文本/日期缺失写 `"NA"`。
- 非缺失字段必须有真实页码与原文摘录，否则校验不通过。

## 手册口径

1. 金额用**基本单位**（HK$125.6 million → 125600000）；百分比用**小数**（68.86% → 0.6886）。
2. 认购倍数填**倍数**（2,347.53 times → 2347.53）。
3. 确认零填数字 `0`（例如超额配售权未行使 → `col_CV` = 0）。
4. 「最终」与「初始」必须分清：`col_CS` 是**行使发售规模调整权之后**的全球发售股数，且**不含**超额配售。
5. `col_CK` 的分母是 **base offer（不含超额配售）**；公告基石表里若已给「假设超额配售权未行使」的
   百分比列，可直接采用该列合计。
6. `col_CX` 是发行人的**净募资额**（扣除开支），**不含**售股股东所得。
7. 不确定就填 `NaN`/`NA` 并在 quote 说明，**不要猜**。

## 基石与发售机制要点（已按港交所 2025-08-04 改革公告核实）

- **基石禁售期仍为 6 个月**：港交所在该次改革的「Proposals not adopted」中明确
  *retain the existing six-month cornerstone lock-up requirement*，
  即**分阶段/3 个月解禁的方案未被采纳**。不要假设 3 个月解禁。
- **超额配售（绿鞋）与发售规模调整是两个不同的东西**：
  绿鞋是 Over-allotment Option；发售规模调整是 Offer Size Adjustment Option。
  `col_CS` 的 base offer **包含已行使的规模调整、排除绿鞋**。
- **承诺投资金额 ≠ 最终获配**：基石最终股数只认公告基石表的逐行配发数。
- 绿鞋是否实际行使要看行使公告；**不能**从本公告里「假设未行使」的口径反推。
- 本公告可能是双语对照重复排版（英文段之后是中文段），同一数字出现两次属正常。
- 每项证据必须给出**本包内**的页码与原文摘录。

### 发售机制（用于理解公告中的分配，不用来填 §DN/DO）

- **Mechanism A**：按公开发售超额认购倍数**分档回拨**到公开认购部分——
  初始 5%；≥15x 且 <50x → 15%；≥50x 且 <100x → 25%；≥100x → 35%（上限 35%）。
- **Mechanism B**：公开发售初始分配**至少 10%、最多 60%**，**无回拨机制**。
- 另：首次公开发售中至少 **40%** 须分配予建簿配售部分。

---

## 字段清单



### 基石最终获配

- `col_CK` = Final cornerstone allocation (% of base offer)（type=number unit=decimal missing=NaN）
  - 提示：最终基石股数 ÷ base offer（不含超额配售）。优先用公告基石表的 Total 行；若表内已给『假设超额配售权未行使』的百分比，可直接采用。

### 认购需求

- `col_CM` = Subscription Ratio (times)（type=number unit=times missing=NaN）
  - 提示：香港公开发售认购倍数。公告常见表述：over-subscribed by N times / Subscription level N times。填倍数（如 2347.53）。
- `col_CN` = Public applicants（type=integer unit=count missing=NaN）
  - 提示：有效申请数目（valid applications）。填人的个数，不是股数。
- `col_CO` = Public valid applied shares（type=integer unit=shares missing=NaN）
  - 提示：有效申请所涉及的股数（total number of Offer Shares applied for）。**正文常不直接给总数**：请去 `BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING` 表，把 Pool A 与 Pool B 各档的『NO. OF SHARES APPLIED FOR』逐档加总（表内『NO. OF VALID APPLICATIONS』列是人数，别加错），并可用『初始公开发售股数 × 认购倍数』做交叉验证。
- `col_CP` = Public subscription original wording（type=text unit=text missing=NA）
  - 提示：认购情况的原文表述，便于核对口径（『认购 N 倍』与『超额认购 N 倍』相差 1 倍）。

### 定价与公告日

- `col_CQ` = Pricing date（type=date unit=date missing=NA）
  - 提示：最终发售价确定日；公告正文通常写明于某日厘定。
- `col_CR` = Allotment announcement date（type=date unit=date missing=NA）
  - 提示：本公告的刊发日期，取自港交所文件元数据 DATE_TIME（确定性），不要用正文里的其他日期。quote 请引用包首『刊发时间（港交所元数据）』那一行，不要引正文的签署日期。page 填 1（该信息在包首而非正文某页）。

### 最终发售与回拨

- `col_CS` = Final global offering shares (before over-allotment)（type=integer unit=shares missing=NaN）
  - 提示：最终全球发售股数（行使发售规模调整权后、未计入超额配售的部分）。
- `col_CT` = Final public offer shares（type=integer unit=shares missing=NaN）
  - 提示：最终香港公开发售股数（已计入回拨）。
- `col_CU` = Final placing shares（type=integer unit=shares missing=NaN）
  - 提示：最终国际配售股数（不含超额配售）。
- `col_CV` = Over-allotment shares actually issued（type=integer unit=shares missing=NaN）
  - 提示：超额配售权实际行使并配发的股数；未行使填 0。另有 FULL EXERCISE OF THE OVER-ALLOTMENT OPTION 公告可交叉确认。
- `col_CW` = Actual clawback / reallocation description（type=text unit=text missing=NA）
  - 提示：实际回拨/重新分配情况的原文描述（例如由国际配售回拨至公开发售的股数）。

### 净募资

- `col_CX` = Net IPO proceeds to issuer (HK$)（type=number unit=HKD missing=NaN）
  - 提示：发行人的净募资额（扣除承销费等开支），不含售股股东所得。公告若给区间，取对应最终发售价的数值。

### 上市时持股与自由流通

- `col_CY` = Public shareholding at listing (%)（type=number unit=decimal missing=NaN）
  - 提示：上市时公众持股比例（小数）。
- `col_CZ` = Share base used for both public shareholding ratios（type=integer unit=shares missing=NaN）
  - 提示：计算公众持股比例所用的分母股数。公告里通常写作 Number of issued Shares upon Listing (before exercise of the Over-allotment Option)；也可能需要从公众持股百分比反算。**不要因为公告用了市值口径就不填**——先找这一行的股数。
- `col_DA` = Unrestricted public shareholding at listing (%)（type=number unit=decimal missing=NaN）
  - 提示：不受禁售限制的公众持股比例（小数）。公告若直接给 free float 百分比就直接用；若只给自由流通股数，则 = 自由流通股数 ÷ col_CZ。**自由流通股数 = 本次全球发售股份(col_CS) − 基石获配股份(= col_CK × col_CS)**。**不要用 col_CY − col_CK**：那会漏掉其他受禁售的上市前股东（如 PRC 法律下 12 个月禁售的内资股）。
- `col_DB` = Free float denominator description（type=text unit=text missing=NA）
  - 提示：自由流通量（FREE FLOAT）分母的口径说明与所涉股份类别/剔除项。
- `col_DC` = Free float denominator shares（type=integer unit=shares missing=NaN）
  - 提示：自由流通比例所用的**分母股数**（通常与 col_CZ 相同，即上市时已发行股份总数）。注意：本字段是**分母**，不是自由流通股数本身。

---

## 公告全文


<<<PAGE 1>>>
1
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”, 
or the “Hong Kong Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy or completeness and 
expressly disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated January 29, 2026 (the “Prospectus”) of Muyuan Foods Co., Ltd. (牧原食品股份有
限公司) (the “Company”). This announcement is made by the order of the board (the “Board”) of directors (the 
“Directors”) of the Company. The Board collectively and individually accept responsibility for the accuracy of this 
announcement.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for any securities. This announcement is not a prospectus. Potential investors should read the Prospectus 
for detailed information about the Global Offering described below before deciding whether or not to invest in 
the Offer Shares. Any investment decision in relation to the Offer Shares should be taken solely in reliance on the 
information provided in the Prospectus.
This announcement is not for release, publication or distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia or any other 
jurisdiction where such distribution is prohibited by laws). This announcement does not constitute or form a part of 
any offer or solicitation to purchase or subscribe for securities in the United States or in any other jurisdictions. The 
securities mentioned herein have not been, and will not be, registered under the United States Securities Act of 1933 
as amended from time to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the 
United States. The securities may not be offered, sold, pledged or otherwise transferred within the United States, 
except pursuant to an available exemption from, or in a transaction not subject to, the registration requirements of the 
U.S. Securities Act and in accordance with any applicable state securities laws in the United States. The Offer Shares 
may only be offered and sold (a) in the United States to QIBs in reliance on Rule 144A or another available exemption 
from registration requirements under the U.S. Securities Act, and (b) outside the United States in offshore transactions 
in reliance on Regulation S. There will be no public offer of securities in the United States.
In connection with the Global Offering, Morgan Stanley Asia Limited as stabilizing manager (the “Stabilizing 
Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, to the extent permitted by the 
applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect transactions with 
a view to stabilizing or supporting the market price of the H Shares at such price, in such amounts and in such manners 
as the Stabilizing Manager, its affiliates or any person acting for it may determine and at a level higher than that which 
might otherwise prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing 
Manager (or its affiliates or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, 
if taken, (a) will be conducted at the absolute discretion of the Stabilizing Manager (or its affiliates or any person 
acting for it) and in what the Stabilizing Manager reasonably regards as the best interest of the Company, (b) may 
be discontinued at any time and (c) is required to be brought to an end within 30 days of the last day for lodging 
applications under the Hong Kong Public Offering (which is Thursday, March 5, 2026). Such Stabilizing action, 
if taken, may be effected in all jurisdictions where it is permissible to do so, in each case in compliance with all 
applicable laws, rules and regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules 
(Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter 
571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Thursday, March 5, 2026). 
After this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of 
the H Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to terms and conditions set out in 
the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not 
resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong 
Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section 
headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. on the Listing Date.

<<<PAGE 2>>>
2
MUYUAN FOODS CO., LTD.
牧原食品股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under the 
Global Offering
:
273,951,400 H Shares (subject to the 
 Over-allotment Option)
Number of Hong Kong Offer Shares
:
27,395,200 H Shares 
Number of International Offer Shares
:
246,556,200 H Shares (subject to 
 the Over-allotment Option)
Final Offer Price
:
HK$39.00 per H Share, plus brokerage 
 of 1.0%, SFC transaction levy of
 0.0027%, Hong Kong Stock Exchange
 trading fee of 0.00565% and AFRC
 transaction levy of 0.00015% (payable
 in full on application in Hong Kong
 dollars and subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
2714
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
MUYUAN FOODS CO., LTD.
牧原食品股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated January 29, 2026 (the “Prospectus”) issued by 
Muyuan Foods Co., Ltd. (牧原食品股份有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of H 
Shareholders, H Shareholders and prospective investors should be aware that the price of 
the H Shares could move substantially even with a small number of H Shares traded and 
should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
2714
Stock short name
MUYUAN
Dealings commencement date
February 6, 2026*
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$39.00
Maximum Offer Price
HK$39.00
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the Over-allotment 
Option)
273,951,400
Number of Offer Shares in Hong Kong Public Offering
27,395,200
Number of Offer Shares in International Offering (before 
exercise of the Over-allotment Option)
246,556,200
Number of issued Shares upon Listing (before exercise of the 
Over-allotment Option)(1)
5,736,722,666
Note:
(1) 
The number of issued Shares upon Listing includes 69,586,523 repurchased A Shares which are held by 
the Company as treasury Shares and excludes A Shares issuable upon the conversion of the outstanding 
Convertible Bonds.

<<<PAGE 4>>>
4
Over-allocation
Number of Offer Shares over-allocated
41,092,700
International Offering 
41,092,700
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds
HK$10,684.1 million
Less: Estimated listing expenses payable based on Final 
Offer Price
HK$213.7 million
Net proceeds
HK$10,470.4 million
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The Company 
will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if any) for the 
purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus on a pro rata basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
Number of valid applications
21,268
Number of successful applications
21,268
Subscription level
5.88 times
Claw-back triggered
N/A
Number of Offer Shares initially available under the Hong Kong 
Public Offering
27,395,200
Number of Offer Shares reallocated from the International Offering 
0
Final number of Offer Shares under the Hong Kong Public Offering
27,395,200
% of final number of Offer Shares under the Hong Kong Public Offering 
to the Global Offering
10%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can refer to 
https://www.hkeipo.hk/iporesult to perform a search by identification number or https://www.hkeipo.hk/iporesult for 
the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
Number of placees
160
Subscription level
8.62 times
Number of Offer Shares initially available under the International 
Offering
246,556,200
Number of Offer Shares reallocated to the Hong Kong Public Offering 
0
Final number of Offer Shares under the International Offering
246,556,200
% of final number of Offer Shares under the International Offering 
to the Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a 
waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit the Company to allocate certain Offer Shares in the International Offering 
to certain Existing Minority Shareholders and/or their close associates, and (b) a consent under 
paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company 
to, among other things, allocate further H Shares in the International Offering to certain existing 
Shareholders and/or their close associates and Cornerstone Investors and/or their close associates, 
(i) none of the Offer Shares subscribed by the placees and the public have been financed directly 
or indirectly by the Company, any of its Directors, chief executive, Controlling Shareholders, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or 
their respective close associates; and (ii) none of the placees and the public who have purchased 
the Offer Shares are accustomed to taking instructions from the Company, any of its Directors, 
chief executive, substantial Shareholders, Controlling Shareholders, existing Shareholders of the 
Company or any of its subsidiaries or their respective close associates in relation to the acquisition, 
disposal, voting or other disposition of H Shares registered in his/her/its name or otherwise held by 
him/her/it.

<<<PAGE 6>>>
6
The placees in the International Offering include the following: 
Cornerstone Investors
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering (1) (2)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering (2) (3)
Existing 
Shareholders 
or their close 
associates
Charoen Pokphand Foods Public 
Company Limited (“CPF”)
39,992,200
14.60%
0.70%
No
Wilmar
– Wii Pte Ltd
9,998,000
3.65%
0.17%
No
– HPRY Holdings Limited 
 (“HPRY”)
3,999,200
1.46%
0.07%
No
Subtotal
13,997,200
5.11%
0.24%
Sinochem Hong Kong (Group) 
Company Limited (“Sinochem 
HK”)
12,997,400
4.74%
0.23%
No
Hong Kong Henan Agri 
International Co., Limited 
(“Hong Kong Henan Agri 
International”)
9,998,000
3.65%
0.17%
No
FIL Investment Management 
(Hong Kong) Limited (“FIL 
Investment”)
15,996,800
5.84%
0.28%
Yes
RBC Global Asset Management 
(Asia) Limited (“RBC GAM”)
5,998,800
2.19%
0.10%
No
Gaoyi Entities
– Perseverance Asset 
 Management International 
 (Singapore) Pte. Ltd. 
 (“Perseverance Asset 
 Management”)
6,518,700
2.38%
0.11%
Yes
– Shanghai Gaoyi Asset 
 Management Partnership 
 (Limited Partnership) 
 (“Shanghai Gaoyi”) and 
 Huatai Capital Investment 
 Limited (“HTCI”) (in 
 connection with Gaoyi 
 OTC Swaps)
5,478,900
2.00%
0.10%
Yes

<<<PAGE 7>>>
7
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering (1) (2)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering (2) (3)
Existing 
Shareholders 
or their close 
associates
Subtotal
11,997,600
4.38%
0.21%
Ping An of China Asset 
Management (Hong Kong) 
Company Limited (“Ping An 
Asset HK”)
5,998,800
2.19%
0.10%
Yes
Dajia Life Insurance Co., Ltd. 
(“Dajia Life”)
5,998,800
2.19%
0.10%
Yes
UBS Asset Management 
(Singapore) Ltd. (“UBS AM 
Singapore”) 
3,999,200
1.46%
0.07%
Yes
Midea Development Holding 
(BVI) Limited (“Midea 
Development Holding BVI”)
5,998,800
2.19%
0.10%
Yes
Integrated Core Strategies 
(Asia) Pte. Ltd. (“Millennium 
ICSA”)
1,999,600
0.73%
0.03%
Yes
Jane Street Asia Trading 
Limited (“JSAT”)
1,999,600
0.73%
0.03%
No
Total
136,972,800
50.00%
2.39%
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
(2) 
Assuming the Over-allotment Option is not exercised.
(3) 
The total issued share capital after the Global Offering includes 69,586,523 A Shares being held as treasury 
Shares as of the date of this announcement and excludes A Shares issuable upon the conversion of the 
outstanding Convertible Bonds.
(4) 
In addition to the Offer Shares subscribed for as Cornerstone Investors, Sinochem HK, FIL Investment, RBC 
GAM, Perseverance Asset Management, Shanghai Gaoyi and HTCI (in connection with Gaoyi OTC Swaps), 
Ping An Asset HK, Dajia Life, UBS AM Singapore, Midea Development Holding BVI, Millennium ICSA 
and JSAT, and/or their close associates, were allocated further Offer Shares as placees in the International 
Offering. Please refer to the section headed “Allotment Results Details — International Offering — Allottees 
with Waivers/Consents Obtained” in this announcement for details. Only the Offer Shares subscribed for as 
Cornerstone Investors are subject to lock-up as indicated below. For details, please refer to the section headed 
“Lock-up Undertakings — Cornerstone Investors” in this announcement.
(5) 
For details of the waiver from strict compliance with Rule 10.04 of the Listing Rules and prior consent 
under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by existing minority 
Shareholders and/or close associates of existing Shareholders, please refer to the section headed “Others/
Additional Information — Allocation of H Shares to Existing Minority Shareholders and/or their close 
associates” in this announcement.

<<<PAGE 8>>>
8
Allottees with waivers/consents obtained
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering (1) (2)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering (2) (3)
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and 
consent under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H 
Shares by Existing Minority Shareholders holding 1% or more of the issued share capital 
of the Company immediately prior to the completion of the Global Offering and/or their 
close associates(4)
Nil
Nil
Nil
Nil
Nil
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations of further H Shares to existing Shareholders and 
Cornerstone Investors and/or their close associates(5)
Sinochem HK
6,998,600
2.55%
0.13%
Same entity as the 
Cornerstone Investor
FIL Investment
7,998,000
2.92%
0.15%
Same entity as the 
Cornerstone Investor 
and an existing 
Shareholder
RBC GAM
3,000,000
1.10%
0.05%
Same entity as the 
Cornerstone Investor
Gaoyi Entities
– Perseverance Asset 
 Management
409,400
0.15%
0.007%
Same entity as the 
Cornerstone Investor 
and an existing 
Shareholder
– Shanghai Gaoyi 
 and HTCI (in 
 connection with 
 Gaoyi OTC Swaps)
190,300
0.07%
0.003%
Same entity as the 
Cornerstone Investor 
and a close associate 
of certain existing 
Shareholders
Subtotal
599,700
0.22%
0.01%
Ping An Asset HK
3,600,000
1.31%
0.07%
Same entity as the 
Cornerstone Investor 
and a close associate 
of certain existing 
Shareholders
Dajia Life
3,999,000
1.46%
0.07%
Same entity as the 
Cornerstone Investor 
and a close associate 
of an existing 
Shareholder

<<<PAGE 9>>>
9
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering (1) (2)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering (2) (3)
Relationship
UBS AM Singapore
3,000,000
1.10%
0.05%
Same entity as the 
Cornerstone Investor 
and a close associate 
of an existing 
Shareholder
Lu Deyan
3,000,000
1.10%
0.05%
A close associate of a 
Cornerstone Investor, 
Midea Development 
Holding BVI
Millennium Entities
– Millennium ICSA
2,000,000
0.73%
0.04%
Same entity as the 
Cornerstone Investor 
and an existing 
Shareholder
– Centerline 
 Investment 
 Management 
 Limited
8,000
0.0029%
0.0001%
A close associate of a 
Cornerstone Investor, 
Millennium ICSA
Subtotal
2,008,000
0.7329%
0.0401%
Jane Street Financial 
Limited
2,000,000
0.73%
0.04%
A close associate of a 
Cornerstone Investor, 
JSAT
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 
of the Guide for New Listing Applicants in relation to allocations to connected clients(6)
HTCI (7)
5,478,900
2.00%
0.10%
Connected client as a 
Cornerstone Investor
190,300
0.07%
0.003%
Connected client as a 
placee
CITIC Securities 
International Capital 
Management Limited 
(“CSI”)
4,471,700
1.63%
0.08%
Connected client as a 
placee
CITIC Securities 
Asset Management 
Company Limited 
(“CITIC Asset 
Management”)
40,000
0.01%
0.001%
Connected client as a 
placee

<<<PAGE 10>>>
10
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering (1) (2)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering (2) (3)
Relationship
GF International 
Investment 
Management Limited 
(“GF International”)
599,700
0.22%
0.01%
Connected client as a 
placee
E Fund Management 
Co., Ltd. (“E Fund”)
569,300
0.21%
0.01%
Connected client as a 
placee
E Fund Management 
(Hong Kong) Co., Ltd. 
(“E Fund HK”)
30,400
0.01%
0.001%
Connected client as a 
placee
Value Partners 
Limited and Value 
Partners Hong Kong 
Limited (collectively, 
“Value Partners”)
1,598,000
0.58%
0.03%
Connected client as a 
placee
Bosera Asset 
Management 
(International) Co., 
Limited (“Bosera 
Asset Management”)
399,000
0.15%
0.01%
Connected client as a 
placee

<<<PAGE 11>>>
11
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering (1) (2)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering (2) (3)
Relationship
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
(2) 
Assuming the Over-allotment Option is not exercised.
(3) 
The total issued share capital after the Global Offering includes 69,586,523 A Shares being held as treasury 
Shares as of the date of this announcement and excludes A Shares issuable upon the conversion of the 
outstanding Convertible Bonds.
(4) 
Among the Cornerstone Investors, FIL Investment, Perseverance Asset Management, Shanghai Gaoyi and 
HTCI (in connection with Gaoyi OTC Swaps), Ping An Life Insurance, Dajia Life, UBS AM Singapore, 
Midea Development Holding BVI and Millennium are Existing Minority Shareholders or their close 
associates (in the case of Millennium, its existing interest in the Company is held through OTC swaps), 
none of which holds 1% or more of the issued share capital of the Company (including the treasury Shares) 
immediately prior to the completion of the Global Offering. The Stock Exchange has granted a waiver from 
strict compliance with the requirements under Rule 10.04 of the Listing Rules and consent under Paragraph 
1C(2) of the Placing Guidelines to permit H Shares in the International Offering to be placed to such 
Existing Minority Shareholders and/or their close associates. Please refer to the section headed “Waivers and 
Exemptions — Allocation of H Shares to Existing Minority Shareholders and/or Their Close Associates” of 
the Prospectus for details.
The Stock Exchange has granted the waiver on the condition that, among others, details of the allocation to 
the Existing Minority Shareholders and/or their close associates holding more than 1% of the issued share 
capital of the Company (including the treasury Shares) immediately prior to the completion of the Global 
Offering will be disclosed in the Prospectus and/or allotment results announcement.
(5) 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details — International Offering — Cornerstone Investors” in this announcement. For details of the 
consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations 
of further H Shares to the Cornerstone Investors, please refer to the section headed “Others/Additional 
Information — Allocations of Offer Shares to the Cornerstone Investors and/or their close associates with a 
consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants” in this announcement.
(6) 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients, please refer to the sections headed 
“Others/Additional Information — Placing to connected clients with a consent under paragraph 1C(1) of the 
Placing Guidelines” and “Others/Additional Information — Allocations of Offer Shares to the Cornerstone 
Investors and/or their close associates with a consent under paragraph 18 of Chapter 4.15 of the Guide for 
New Listing Applicants” in this announcement.

<<<PAGE 12>>>
12
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering (1) (2)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering (2) (3)
Relationship
(7) 
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public 
offerings (“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products issued by 
appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. In 
connection with such products, the licensed domestic securities firms, through their Hong Kong affiliates, 
may participate in Hong Kong IPOs either as placees or cornerstone investors (the “Cross-border 
Derivatives Trading Regime”).
Huatai Securities Co., Ltd. (“HTSC”), the A shares of which are listed on the Shanghai Stock Exchange 
(stock code: 601688), the H shares of which are listed on the Stock Exchange (stock code: 6886), and the 
global depositary receipts of which are listed on the London Stock Exchange (LON: HTSC), is one of the 
domestic securities firms licensed to undertake cross-border derivatives trading activities. HTSC entered into 
an ISDA agreement (the “ISDA Agreement”) with its indirectly wholly-owned subsidiary, HTCI, to set out 
the principal terms of any future total return swap between HTSC and HTCI.
HTFH is the Connected Distributor. Pursuant to the ISDA Agreement, HTCI, which intends to participate 
in the International Offering as a placee, will hold the beneficial interest of the Offer Shares on a non-
discretionary basis as the single underlying holder under a back-to-back total return swap (the “HT Back-
to-back TRS”) to be entered by HTCI in connection with Huatai TRS (as defined below) placed by and 
fully funded (i.e. with no financing provided by HTCI) by the Huatai Ultimate Clients (as defined below), 
by which, HTCI will, subject to customary fees and commissions, pass the full economic exposure of the 
Offer Shares ultimately to the Huatai Ultimate Clients, which in effect, HTCI will hold the beneficial interest 
of the Offer Shares on behalf of the Huatai Ultimate Clients. HTFH and HTCI are indirectly wholly-owned 
subsidiaries of HTSC. Accordingly, HTCI is considered as a “connected clients” of Huatai pursuant to 
paragraph 1B(7) of the Placing Guidelines.
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investor (the “Huatai Ultimate 
Clients”) cannot directly subscribe for the Offer Shares but may invest in derivative products issued by 
domestic securities firms licenced to undertake cross-border derivatives trading activities, such as HTSC, 
with the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, the Huatai 
Ultimate Clients will, through its investment manager, place a total return swap order (the “Huatai TRS”) 
with HTSC in connection with the Company’s IPO and HTSC will place a HT Back-to-back TRS order to 
HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the HT Back-to-back TRS, 
HTCI participates in the Company’s IPO and subscribes for the Offer Shares through placing order with 
HTFH during the International Offering.
The Huatai Ultimate Clients for purpose of this placing subscription are certain investment funds managed by 
Shanghai Gaoyi Asset Management Partnership (Limited Partnership) (上海高毅資產管理合夥企業(有限合
夥)) on a discretionary basis, as follows:
Name of the Huatai Ultimate Clients
Ultimate beneficial 
owner(s) holding 30% or 
more interest (if any)
Gaoyi Renhao Youxuan Zhifu Private Equity Investment Fund (高毅任昊優選
致福私募證券投資基金)
N/A
Gaoyi Renhao Long-Term Value Langrun Private Equity Investment Fund (高
毅任昊長期價值朗潤私募證券投資基金)
N/A
Gaoyi Renhao Long-Term Value Langrun Private Equity Investment Fund (高
毅任昊臻選春和私募證券投資基金)
N/A
Gaoyi Renhao Selected Chengze Private Equity Investment Fund (高毅任昊精
選承澤私募證券投資基金)
N/A
Gaoyi-Xiaofeng No. 1 Ruiyuan Securities Investment Fund (高毅－曉峰 1 號
睿遠證券投資基金)
N/A
Gaoyi Xiaofeng No. 2 Letter Foundation (高毅曉峰 2 號致信基金)
N/A
To the best of knowledge of HTCI and after making all reasonable enquiries, the Huatai Ultimate Clients are 
independent third parties of HTCI, and the companies which are members of the same group of HTCI.

<<<PAGE 13>>>
13
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering (1) (2)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering (2) (3)
Relationship
The purpose of HTCI to subscribe for the Offer Shares is for hedging the HT Back-to-back TRS in 
connection with the Huatai TRS order placed by the Huatai Ultimate Clients. Pursuant to the terms of the 
contracts of the HT Back-to-back TRS and the Huatai TRS, during the tenor of the HT Back-to-back TRS and 
the Huatai TRS, subject to customary fees and commissions, all economic returns of the Offer Shares will be 
ultimately passed to the Huatai Ultimate Clients through the HT Back-to-back TRS and the Huatai TRS and 
all economic loss shall be ultimately borne by the Huatai Ultimate Clients. HTCI will not take any economic 
return or bear any economic loss in relation to the Offer Shares, save as customary fees and commissions.
Investment in the HT Back-to-back TRS and the Huatai TRS is similar to the investment in a qualified 
domestic institutional investor fund (“QDII”) in the way that the Huatai Ultimate Clients would reap all 
the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through the 
exchange rate exposure on both the notional value of the investment and the profit and loss of the investment. 
In contrast, the profit and loss of the HT Back-to-back TRS and the Huatai TRS factor into account the 
fluctuation in RMB exchange rate upon termination of the Huatai TRS by converting the profit and loss using 
the current exchange rate at the time of termination. As such, the Huatai Ultimate Clients would bear the 
exchange rate exposure of the profit and loss on settlement date.
The Huatai Ultimate Clients may exercise an early termination right to terminate the Huatai TRS at any 
time from the issue date of the Huatai TRS which should be on or after the date on which the Offer Shares 
are listed on the Stock Exchange at their own discretions. Upon the termination upon maturity or early 
termination of the Huatai TRS by the Huatai Ultimate Clients, HTCI will dispose the Offer Shares on the 
secondary market and the Huatai Ultimate Clients will receive a final settlement amount in cash in accordance 
with the terms and conditions of the HT Back-to-back TRS and the Huatai TRS which should have taken into 
account all the economic returns or economic loss in relation to the Offer Shares. If upon the maturity of the 
Huatai TRS, the Huatai Ultimate Clients intend to extend the investment period, subject to further agreement 
between HTSC and the relevant Huatai Ultimate Clients, the term of the Huatai TRS could be extended by 
way of a new issuance or a tenor extension. Accordingly, HTSC will extend the term of the HT Back-to-back 
TRS by way of a new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass 
through the economic exposure to the Huatai Ultimate Clients, being an onshore clients who places Huatai 
TRS orders with HTSC in connection with the IPO of the Company. HTCI will not exercise the voting rights 
of the Offer Shares during the tenor of the HT Back-to-back TRS.
During the life of the Huatai TRS and HT Back-to-back TRS, HTCI may continue to hold the Offer Shares 
in its custodian account, or to hold some or all of the Offer Shares in a prime brokerage account for stock 
borrowing purposes, where HTCI will lend out its holding of underlying Offer Shares in the form of stock 
borrowing loans consistent with market practice to lower its finance costs, provided that HTCI has the ability 
to call back the Offer Shares on loan at any time in order to satisfy its obligations under the HT Back-to-back 
TRS to ensure the economic interests are ultimately passed to the Huatai Ultimate Clients.

<<<PAGE 14>>>
14
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name(6)
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
total issued 
H Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon 
Listing (1)(2)
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon 
Listing (2)
Last day subject 
to the lock-up 
undertakings (3)
Mr. Qin Yinglin
2,086,287,906
–
36.37%
August 5, 2026 
(First Six-Month 
Period)(4) 
February 5, 2027 
(Second Six-Month 
Period)(5)
Muyuan Industrial 
Group Co., Ltd. 
(“Muyuan Group”)
848,762,153
–
14.80%
August 5, 2026 
(First Six-Month 
Period)(4) 
February 5, 2027 
(Second Six-Month 
Period)(5)
Ms. Qian Ying
64,445,240
–
1.12%
August 5, 2026 
(First Six-Month 
Period)(4) 
February 5, 2027 
(Second Six-Month 
Period)(5)

<<<PAGE 15>>>
15
Name(6)
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
total issued 
H Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon 
Listing (1)(2)
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon 
Listing (2)
Last day subject 
to the lock-up 
undertakings (3)
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
(2) 
Assuming the Over-allotment Option is not exercised.
(3) 
In accordance with the applicable Listing Rules, the required lock-up for the first six month period will end 
on August 5, 2026 and for the second six-month period will end on February 5, 2027.
(4) 
Each member of the Controlling Shareholders may dispose of or transfer Shares (which includes the 
Convertible Bonds held by Muyuan Group and the underlying Shares that may be converted from such 
Convertible Bonds in the event of the exercise of its conversion rights, as applicable) after the indicated date 
subject to that the any member of Controlling Shareholders will not cease to be a controlling shareholder (as 
defined in the Listing Rules).
(5) 
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after the 
indicated date.
(6) 
For illustrative purposes only, this subsection lists only those members of the Controlling Shareholders who 
hold Shares directly in the Company. Pursuant to Rule 10.07 of the Listing Rules, each of the Controlling 
Shareholders (namely, Mr. Qin Yinglin, Ms. Qian Ying and Muyuan Group) has undertaken to the Company 
and the Stock Exchange that, except in connection with the Global Offering (including the Over-allotment 
Option), he/she/it shall, and shall procure that the relevant registered holders of the Shares in which he/she/
it is beneficially interested shall, comply with the applicable lock-up requirements. For further details, please 
refer to the section headed “Underwriting — Underwriting Arrangements and Expenses — Undertakings to 
the Hong Kong Stock Exchange pursuant to the Listing Rules” in the Prospectus.

<<<PAGE 16>>>
16
Cornerstone Investors
Name
Number of 
Shares held 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
total issued 
H Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon 
Listing (1)(2)
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon 
Listing (2)
Last day subject 
to the lock-up 
undertakings (3)
CPF
39,992,200
14.60%
0.70%
August 5, 2026
Wilmar
– Wii Pte Ltd
9,998,000
3.65%
0.17%
August 5, 2026
– HPRY
3,999,200
1.46%
0.07%
August 5, 2026
Subtotal
13,997,200
5.11%
0.24%
Sinochem HK
12,997,400
4.74%
0.23%
August 5, 2026
Hong Kong Henan Agri 
International
9,998,000
3.65%
0.17%
August 5, 2026
FIL Investment
15,996,800
5.84%
0.28%
August 5, 2026
RBC GAM
5,998,800
2.19%
0.10%
August 5, 2026
Gaoyi Entities
– Perseverance Asset 
Management
6,518,700
2.38%
0.11%
August 5, 2026
– Shanghai Gaoyi and 
HTCI (in connection 
with Gaoyi OTC Swaps)
5,478,900
2.00%
0.10%
August 5, 2026
Subtotal
11,997,600
4.38%
0.21%
Ping An Asset HK
5,998,800
2.19%
0.10%
August 5, 2026
Dajia Life
5,998,800
2.19%
0.10%
August 5, 2026
UBS AM Singapore
3,999,200
1.46%
0.07%
August 5, 2026
Midea Development 
Holding BVI
5,998,800
2.19%
0.10%
August 5, 2026
Millennium ICSA
1,999,600
0.73%
0.03%
August 5, 2026
JSAT
1,999,600
0.73%
0.03%
August 5, 2026
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
(2) 
Assuming the Over-allotment Option is not exercised.
(3) 
In accordance with the respective cornerstone investment agreements, the required lock-up periods will end 
on August 5, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or transferring 
the Shares subscribed for pursuant to their respective cornerstone investment agreements after the indicated 
date.

<<<PAGE 17>>>
17
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of
H Shares
allotted
Allotment
as % of
International
Offering
(assuming no
exercise of the
Over-allotment
Option)
Allotment
as % of
International
Offering
(assuming the
Over-allotment
Option is
exercised and
new H Shares
are issued)
Allotment
as % of
total Offer
Shares
(assuming no
exercise of the
Over-allotment
Option)
Allotment
as % of
total Offer
Shares
(assuming the
Over-allotment
Option is
exercised and
new H Shares
are issued)
Number of
H Shares held 
upon Listing
% of total
issued share
capital upon
Listing
(assuming no
exercise of the
Over-allotment
Option)
% of total
issued share
capital upon
Listing
(assuming the
Over-allotment
Option is
exercised and
new H Shares
are issued)
Top 1
39,992,200
16.22%
13.90%
14.60%
12.69%
39,992,200
0.70%
0.69%
Top 5
110,577,500
44.85%
38.44%
40.36%
35.10%
110,577,500
1.93%
1.91%
Top 10
157,215,300
63.76%
54.66%
57.39%
49.90%
157,215,300
2.74%
2.72%
Top 25
243,712,300
98.85%
84.73%
88.96%
77.36%
243,712,300
4.25%
4.22%
Note
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H 
Shareholders*
Number of
H Shares
allotted
Allotment
as % of
International
Offering
(assuming
no exercise
of the
Over-allotment
Option)
Allotment
as % of
International
Offering
(assuming the
Over-allotment
Option is
exercised
and new
H Shares
are issued)
Allotment
as % of
total Offer
Shares
(assuming
no exercise
of the
Over-allotment
Option)
Allotment
as % of
total Offer
Shares
(assuming the
Over-allotment
Option is
exercised
and new
H Shares
are issued)
Number of
H Shares
held upon
Listing
% of
total issued
H Shares
capital upon
Listing
(assuming
no exercise
of the
Over-allotment
Option)
% of
total issued
H Shares
capital upon
Listing
(assuming the
Over-allotment
Option is
exercised
and new
H Shares
are issued)
Number of
Shares
held upon
Listing
Top 1
39,992,200
16.22%
13.90%
14.60%
12.69%
39,992,200
14.60%
12.69%
39,992,200
Top 5
110,577,500
44.85%
38.44%
40.36%
35.10%
110,577,500
40.36%
35.10%
121,656,682
Top 10
157,215,300
63.76%
54.66%
57.39%
49.90%
157,215,300
57.39%
49.90%
201,098,429
Top 25
243,712,300
98.85%
84.73%
88.96%
77.36%
243,712,300
88.96%
77.36%
289,463,587
Note
* 
Ranking of H Shareholders is based on the number of H Shares held by the Shareholder upon Listing.

<<<PAGE 18>>>
18
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number of
H Shares
allotted
Allotment
as % of
International
Offering
(assuming
no exercise
of the
Over-allotment
Option)
Allotment
as % of
International
Offering
(assuming the
Over-allotment
Option is
exercised
and new
H Shares
are issued)
Allotment
as % of
total Offer
Shares
(assuming
no exercise
of the
Over-allotment
Option)
Allotment
as % of
total Offer
Shares
(assuming the
Over-allotment
Option is
exercised
and new
H Shares
are issued)
Number of
H Shares
held upon
Listing
Number of
Shares held
upon Listing
% of total
issued share
capital upon
Listing
(assuming
no exercise
of the
Over-allotment
Option)
% of
total issued
share capital
upon Listing
(assuming the
Over-allotment
Option is
exercised
and new
H Shares
are issued)
Top 1
0
0.00%
0.00%
0.00%
0.00%
0
2,999,495,299
52.29%
51.91%
Top 5
0
0.00%
0.00%
0.00%
0.00%
0
3,360,922,089
58.59%
58.17%
Top 10
72,985,800
29.60%
25.37%
26.64%
23.17%
72,985,800
3,577,056,629
62.35%
61.91%
Top 25
208,435,300
84.54%
72.46%
76.08%
66.16%
208,435,300
3,733,316,339
65.08%
64.61%
Notes
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 19>>>
19
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, 21,268 valid applications 
made by the public will be conditionally allocated on the basis set out below:
Pool A
Number of 
H Shares 
applied for
Number of valid
applications
Basis of allocation/ballot
Approximate
percentage
allotted of the
total number of
H Shares 
applied for
100
11,029
100 H Shares
100.00%
200
3,001
100 H Shares plus 2,281 out of 3,001 applicants to receive an additional 100 H Shares
88.00%
300
1,131
200 H Shares plus 509 out of 1,131 applicants to receive an additional 100 H Shares
81.67%
400
458
300 H Shares plus 45 out of 458 applicants to receive an additional 100 H Shares
77.46%
500
868
300 H Shares plus 621 out of 868 applicants to receive an additional 100 H Shares
74.31%
600
287
400 H Shares plus 89 out of 287 applicants to receive an additional 100 H Shares
71.84%
700
142
400 H Shares plus 126 out of 142 applicants to receive an additional 100 H Shares
69.82%
800
195
500 H Shares plus 88 out of 195 applicants to receive an additional 100 H Shares
68.14%
900
105
600 H Shares
66.67%
1,000
1,667
600 H Shares plus 896 out of 1,667 applicants to receive an additional 100 H Shares
65.37%
1,500
270
900 H Shares plus 27 out of 270 applicants to receive an additional 100 H Shares
60.67%
2,000
348
1,100 H Shares plus 176 out of 348 applicants to receive an additional 100 H Shares
57.53%
2,500
170
1,300 H Shares plus 136 out of 170 applicants to receive an additional 100 H Shares
55.20%
3,000
253
1,600 H Shares plus 3 out of 253 applicants to receive an additional 100 H Shares
53.37%
3,500
73
1,800 H Shares plus 12 out of 73 applicants to receive an additional 100 H Shares
51.90%
4,000
79
2,000 H Shares plus 20 out of 79 applicants to receive an additional 100 H Shares
50.63%
4,500
36
2,200 H Shares plus 11 out of 36 applicants to receive an additional 100 H Shares
49.57%
5,000
176
2,400 H Shares plus 50 out of 176 applicants to receive an additional 100 H Shares
48.57%
6,000
89
2,800 H Shares plus 16 out of 89 applicants to receive an additional 100 H Shares
46.97%
7,000
48
3,100 H Shares plus 46 out of 48 applicants to receive an additional 100 H Shares
45.65%
8,000
45
3,500 H Shares plus 29 out of 45 applicants to receive an additional 100 H Shares
44.56%
9,000
39
3,900 H Shares plus 9 out of 39 applicants to receive an additional 100 H Shares
43.59%
10,000
294
4,200 H Shares plus 215 out of 294 applicants to receive an additional 100 H Shares
42.73%
20,000
112
7,500 H Shares plus 22 out of 112 applicants to receive an additional 100 H Shares
37.60%
30,000
65
10,400 H Shares plus 43 out of 65 applicants to receive an additional 100 H Shares
34.89%
40,000
39
13,200 H Shares plus 13 out of 39 applicants to receive an additional 100 H Shares
33.08%
50,000
48
15,800 H Shares plus 36 out of 48 applicants to receive an additional 100 H Shares
31.75%
60,000
20
18,400 H Shares plus 4 out of 20 applicants to receive an additional 100 H Shares
30.70%
70,000
15
20,800 H Shares plus 13 out of 15 applicants to receive an additional 100 H Shares
29.84%
80,000
6
23,300 H Shares
29.13%
90,000
7
25,600 H Shares plus 3 out of 7 applicants to receive an additional 100 H Shares
28.49%
100,000
72
27,900 H Shares plus 24 out of 72 applicants to receive an additional 100 H Shares
27.93%
Total
21,187
Total number of Pool A successful applicants: 21,187

<<<PAGE 20>>>
20
Pool B
Number
of H Shares
applied for
Number
of valid
applications
Basis of allocation/ballot
Approximate
percentage
allotted of the
total number of
H Shares 
applied for
200,000
31
30,000 H Shares
15.00%
300,000
20
43,100 H Shares
14.37%
400,000
3
55,800 H Shares
13.95%
500,000
4
68,200 H Shares
13.64%
600,000
3
80,300 H Shares
13.38%
700,000
2
92,200 H Shares
13.17%
800,000
2
103,900 H Shares
12.99%
1,000,000
6
127,000 H Shares
12.70%
2,000,000
2
236,000 H Shares
11.80%
3,000,000
1
339,400 H Shares
11.31%
13,697,600
7
1,322,700 H Shares
9.66%
Total
81
Total number of Pool B successful applicants: 81
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 21>>>
21
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Allocation of H Shares to Existing Minority Shareholders and/or their close associates
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted to the 
Company, a waiver from strict compliance with the requirements under Rule 10.04 and consent 
under Paragraph 1C(2) of Appendix F1 to the Listing Rules to permit H Shares in the International 
Offering to be placed to certain existing minority Shareholders who (i) hold less than 5% of the 
total voting rights in the Company prior to the completion of the Global Offering and (ii) are 
not and will not become (upon the completion of the Global Offering) core connected persons of 
the Company or the close associates of any such core connected person (together, the “Existing 
Minority Shareholders”) and/or their close associates, subject to the conditions as follows:
(a) 
each Existing Minority Shareholder to whom the Company may allocate the H Shares in the 
International Offering holds less than 5% of the total voting rights in the Company before 
Listing;
(b) 
each Existing Minority Shareholder is not, and will not be, a core connected person of the 
Company or any close associate of any such core connected person immediately prior to or 
following the Global Offering;
(c) 
none of the Existing Minority Shareholders has the right to appoint a Director and/or have 
any other special rights;
(d) 
allocation to the Existing Minority Shareholders or their close associates will not affect the 
Company’s ability to satisfy the public float requirement as prescribed by the Stock Exchange 
under Rule 19A.13A(2) of the Listing Rules or otherwise approved by the Stock Exchange;
(e) 
the Joint Sponsors confirm the matters set out in (a) to (d) above and confirm to the Stock 
Exchange in writing that, to the best of their knowledge and belief, they have no reason to 
believe that any of the Existing Minority Shareholders or their close associates received 
any preferential treatment, or is in a position to exert influence on the Company to obtain 
actual or perceived preferential treatment in the allocation either as a cornerstone investor 
or as a placee by virtue of their relationship with the Company other than the preferential 
treatment of assured entitlement under a cornerstone investment following the principles set 
out in Chapter 4.15 of the Guide for New Listing Applicants, and details of the allocation 
to the Existing Minority Shareholders holding 1% or more of the issued share capital of the 
Company immediately prior to the completion of the Global Offering will be disclosed in the 
Prospectus and/or this announcement, as the case may be;

<<<PAGE 22>>>
22
(f) 
the Company confirms to the Stock Exchange in writing that:
a. 
in the case of participation as cornerstone investors, no preferential treatment has been, 
nor will be, given to the Existing Minority Shareholders or their close associates by 
virtue of their relationship with the Company, other than the preferential treatment of 
assured entitlement under a cornerstone investment following the principles set out in 
Chapter 4.15 of the Guide for New Listing Applicants, nor is the Existing Minority 
Shareholder in a position to exert influence on the Company to obtain actual or 
perceived preferential treatment, and the Existing Minority Shareholders or their close 
associates’ cornerstone investment agreements do not contain any material terms which 
are more favorable to the Existing Minority Shareholders or their close associates than 
those in other cornerstone investment agreements; or
b. 
in the case of participation as placees, no preferential treatment has been, nor will be, 
given to the Existing Minority Shareholders or their close associates, nor is the Existing 
Minority Shareholder in a position to exert influence on the Company to obtain actual 
or perceived preferential treatment, by virtue of their relationship with the Company in 
any allocation in the placing tranche;
(g) 
in the case of participation as placees, the Overall Coordinators will confirm to the Stock 
Exchange that, to the best of their knowledge and belief, no preferential treatment has been, 
nor will be, given to the Existing Minority Shareholders or their close associates by virtue of 
their relationship with the Company in any allocation in the placing tranche.
Please refer to the section headed “Waivers and Exemptions — Allocation of H Shares to Existing 
Minority Shareholders and/or Their Close Associates” in the Prospectus for further details of the 
waiver and consent.
Each of the Joint Sponsors and the Company has provided the required confirmations as elaborated 
in the Prospectus. In particular, as the Company’s A Shares are listed on the Shenzhen Stock 
Exchange since January 2014, the Company has a highly extensive base of existing Shareholders 
and disclosure of details of allocations to all Existing Minority Shareholders and/or their respective 
close associates will not be meaningful to investors, the proposed disclosure threshold, i.e. 
condition (e) of the waiver and consent which provides that details of the allocation to the Existing 
Minority Shareholders and/or their respective close associates holding more than 1% of the issued 
share capital of the Company immediately prior to the completion of the Global Offering will be 
disclosed in this announcement, is appropriate.
All allocations of Offer Shares to the Existing Minority Shareholders are in compliance with all 
the conditions under the waiver and consent granted by the Stock Exchange.
Allocations of Offer Shares to the existing Shareholders and Cornerstone Investors and/or 
their close associates with a consent under paragraph 18 of Chapter 4.15 of the Guide for 
New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph 
18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to allocate 
further Offer Shares in the International Offering to certain existing Shareholders and Cornerstone 
Investors and/or their close associates as placees, subject to the following conditions (“Allocation 
to Size-based Exemption Participants”):

<<<PAGE 23>>>
23
(a) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;
(b) 
the Offer Shares allocated to all existing Shareholders (whether as cornerstone investors and 
as placees) as permitted under this exemption do not exceed 30% of the total number of the 
H Shares offered under the Global Offering;
(c) 
the Allocation to Size-based Exemption Participants will not affect the Company’s ability 
to satisfy its public float requirement as prescribed by the Stock Exchange under the waiver 
from strict compliance with the requirements of Rule 19A.13A(2) of the Listing Rules;
(d) 
each of the Directors, chief executive of the Company and the Controlling Shareholders 
confirms that no securities have been allocated to them or their respective close associates 
under this exemption; and
(e) 
details of the allocation to Cornerstone Investors under this exemption has been disclosed in 
this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of further allocations of Offer Shares to Cornerstone Investors, please refer to the 
section headed “Allotment Results Details — International Offering — Allottees with Waivers/
Consents Obtained” in this announcement.
Placing to connected clients with a consent under paragraph 1C(1) of the Placing Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, consent 
under paragraph 1C(1) of the Placing Guidelines to permit HTCI to participate in the Global 
Offering as connected client to participate in the Global Offering as a Cornerstone Investor. For 
details of the consent granted, please refer to the section headed “Allotment Results Details — 
International Offering — Cornerstone Investors” in this announcement.
In addition, under the International Offering, certain Offer Shares were placed to connected clients 
of their connected distributors pursuant to the Placing Guidelines as placees. Please refer to the 
section headed “Allotment Results Details — International Offering — Allottees with Waivers/
Consents Obtained” in this announcement for details. The Company has applied to the Stock 
Exchange for, and the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing 
Guidelines to permit the Company to allocate such Offer Shares in the International Offering to 
the connected clients as placees. The allocation of Offer Shares to such connected clients is in 
compliance with all the conditions under the consent granted by the Stock Exchange. Details of the 
placement to connected clients as placees are set out below.

<<<PAGE 24>>>
24
No.
Connected 
Client (11)
Connected 
Distributor(s)
Relationship between 
the Connected Client 
and the Connected 
Distributor(s)
Discretionary 
or non- 
discretionary
Investment 
amount (US$)
Number of H 
Shares to be 
allocated
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering(1)
Approximate 
percentage 
of the total 
issued share 
capital 
immediately 
following 
completion 
of the Global 
Offering(1) (2)
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering(3)
Approximate 
percentage 
of the total 
issued share 
capital 
immediately 
following 
completion 
of the Global 
Offering(2) (3)
1.
HTCI (4)
Huatai Financial 
Holdings (Hong 
Kong) Limited 
(“HTFH”)
HTCI is a member 
of the same group of 
companies as HTFH
Non-
discretionary
28,351,452
5,669,200
2.07%
0.10%
1.80%
0.10%
2.
CSI(5)
CLSA Limited 
(“CLSA”)
CSI is a member of 
the same group of 
companies as CLSA
Non-
discretionary
22,362,849
4,471,700
1.63%
0.08%
1.42%
0.08%
3.
CITIC Asset 
Management(6)
CLSA
CITIC Asset 
Management is a 
member of the same 
group of companies as 
CLSA
Discretionary
200,038
40,000
0.01%
0.001%
0.01%
0.001%

<<<PAGE 25>>>
25
No.
Connected 
Client (11)
Connected 
Distributor(s)
Relationship between 
the Connected Client 
and the Connected 
Distributor(s)
Discretionary 
or non- 
discretionary
Investment 
amount (US$)
Number of H 
Shares to be 
allocated
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering(1)
Approximate 
percentage 
of the total 
issued share 
capital 
immediately 
following 
completion 
of the Global 
Offering(1) (2)
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering(3)
Approximate 
percentage 
of the total 
issued share 
capital 
immediately 
following 
completion 
of the Global 
Offering(2) (3)
4.
GF International(7)
GF Securities (Hong 
Kong) Brokerage
GF International is a 
member of the same 
group of companies as 
GF Securities (Hong 
Kong) Brokerage
Discretionary
2,999,077
599,700
0.22%
0.01%
0.19%
0.01%
5.
E Fund(8)
GF Securities (Hong 
Kong) Brokerage
E Fund is a member 
of the same group 
of companies as GF 
Securities (Hong Kong) 
Brokerage
Discretionary
2,847,048
569,300
0.21%
0.01%
0.18%
0.01%
6.
E Fund HK(8)
GF Securities (Hong 
Kong) Brokerage
E Fund HK is a member 
of the same group 
of companies as GF 
Securities (Hong Kong) 
Brokerage
Discretionary
152,029
30,400
0.01%
0.001%
0.01%
0.001%
7.
Value Partners(9)
GF Securities (Hong 
Kong) Brokerage
Value Partners are the 
members of the same 
group of companies as 
GF Securities (Hong 
Kong) Brokerage
Discretionary
7,991,537
1,598,000
0.58%
0.03%
0.51%
0.03%

<<<PAGE 26>>>
26
No.
Connected 
Client (11)
Connected 
Distributor(s)
Relationship between 
the Connected Client 
and the Connected 
Distributor(s)
Discretionary 
or non- 
discretionary
Investment 
amount (US$)
Number of H 
Shares to be 
allocated
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering(1)
Approximate 
percentage 
of the total 
issued share 
capital 
immediately 
following 
completion 
of the Global 
Offering(1) (2)
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering(3)
Approximate 
percentage 
of the total 
issued share 
capital 
immediately 
following 
completion 
of the Global 
Offering(2) (3)
8.
Bosera Asset 
Management(10)
China Merchants 
Securities (HK) 
Co., Limited 
(“CMS”) and CMB 
International Capital 
Limited (“CMBI”)
Bosera Asset 
Management is a 
member of the same 
group of companies as 
CMS and CMBI
Discretionary
1,995,384
399,000
0.15%
0.01%
0.13%
0.01%
Notes:
(1) 
Assuming the Over-allotment Option is not exercised.
(2) 
Including 69,586,523 A Shares held by the Company in treasury as of the Latest Practicable Date and excluding A Shares issuable upon the conversion of the 
outstanding Convertible Bonds.
(3) 
Assuming the Over-allotment Option is fully exercised.
(4) 
In addition to the Offer Shares subscribed for as a placee, HTCI was allocated 5,478,900 Offer Shares as a Cornerstone Investor in the International Offering. 
HTFT is a distributor in connection of the Global Offering. 

<<<PAGE 27>>>
27
HTFT is a distributor in connection of the Global Offering. Both HTCI and HTFH are indirect wholly-owned subsidiaries of Huatai Securities. Accordingly, 
HTCI is a connected client. The Company has also applied for, and the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing 
Guidelines to permit HTCI to participate in the Global Offering as a Cornerstone Investor. Please also refer to the section headed “Allotment Results Details 
— International Offering — Allottees with Waivers/Consents Obtained” in this announcement.
(5) 
CSI will hold the Offer Shares as a placee under the International Offering on behalf of CSI Ultimate Clients, on a non-discretionary basis, pursuant to 
which: (i) CSI will act as the single counterparty of a back-to-back total return swap transaction (the “CSI Back-to-back TRS”) to be entered into by it in 
connection with a total return swap order (the “CSI Client TRS”) placed and fully funded by Beevest financial trading limited, Canaan China Flagship Fund 
and the investment managers (Beevest Capital Management Limited, Hover4pi Capital Management, Wealth Management Co., Ltd., Guangdong Yundao 
Private Securities Fund Management Co., Ltd. and Shanghai Greenwoods Asset Management Co., Ltd.) who act for and on behalf of certain ultimate clients 
(collectively with Beevest financial trading limited and Canaan China Flagship Fund, the “CSI Ultimate Clients”), by which CSI will pass the full economic 
exposure of the Offer Shares placed to CSI to the CSI Ultimate Clients; (ii) as confirmed by CSI and CLSA, CSI will hold the legal title and beneficial interest 
in the Offer Shares, but will contractually agree to pass on the full economic exposure and return of the Offer Shares to the CSI Ultimate Clients, on a non-
discretionary basis. The CSI Ultimate Clients may exercise their early termination rights to terminate the CSI Client TRS at any time from the trade date of the 
CSI Client TRS which should be on or after the date on which the Offer Shares are listed on the Stock Exchange.The details of the CSI Ultimate Client are as 
follow:
Name of CSI Ultimate Clients
Fund Manager
UBO of Fund Manager
Limited Partner/
Shareholding holding 30% 
or more in the CSI Ultimate 
Client
Beevest Capital Management Limited – Global Multi Alpha Fund
Beevest Capital Management Limited
Zeng Shuzhen
ZENG Shuzhen
Beevest Financial Trading Limited
Not applicable
Not applicable
KANG Lan
Canaan China Flagship Fund
Not applicable
Not applicable
LIANG Hao
Hover4pi Capital Management – Hover4pi Fund I OFC
Hover4pi Capital Management
He Hui
None
招銀理財招睿量化穩健封閉 9 號固收增強理財計劃(China Merchants Bank Wealth 
Management Zhaorui Quantitative Stable Closed No.9 Fixed-income Enhanced Wealth 
Management Plan)
招銀理財有限責任公司(Wealth Management Co., Ltd.)
None
None
招銀理財招睿量化穩健封閉 10 號固收增強理財計劃(China Merchants Bank Wealth 
Management Zhaorui Quantitative Stable Closed No.10 Fixed-income Enhanced Wealth 
Management Plan)
招銀理財有限責任公司(Wealth Management Co., Ltd.)
None
None
筠道複利私募證券投資基金(Yundao Compound Interest Private Equity Securities 
Investment Fund)
廣東筠道私募證券基金管理有限公司(Guangdong Yundao 
Private Securities Fund Management Co., Ltd.)
None
溫少模(Wen Shaomo)

<<<PAGE 28>>>
28
Name of CSI Ultimate Clients
Fund Manager
UBO of Fund Manager
Limited Partner/
Shareholding holding 30% 
or more in the CSI Ultimate 
Client
景林全球基金(Greenwoods Global Fund)
上海景林資產管理有限公司(Shanghai Greenwoods Asset 
Management Co., Ltd.)
蔣錦志(JIANG Jinzhi)
None
景林致遠私募基金(Greenwoods Zhiyuan Private Equity Fund)
上海景林資產管理有限公司(Shanghai Greenwoods Asset 
Management Co., Ltd.)
蔣錦志(JIANG Jinzhi)
None
景林豐收 2 號基金(Greenwoods Harvest No. 2 Fund)
上海景林資產管理有限公司(Shanghai Greenwoods Asset 
Management Co., Ltd.)
蔣錦志(JIANG Jinzhi)
None
景林豐收 3 號私募基金(Greenwoods Harvest No. 3 Private Equity Fund)
上海景林資產管理有限公司(Shanghai Greenwoods Asset 
Management Co., Ltd.)
蔣錦志(JIANG Jinzhi)
None
景林上元私募證券投資基金(Greenwoods Shangyuan Private Securities Investment 
Fund)
上海景林資產管理有限公司(Shanghai Greenwoods Asset 
Management Co., Ltd.)
蔣錦志(JIANG Jinzhi)
林燕蕾(Lin Yanlei)
景林豐收 6 號私募證券投資基金(Greenwoods Harvest No. 6 Private Securities 
Investment Fund)
上海景林資產管理有限公司(Shanghai Greenwoods Asset 
Management Co., Ltd.)
蔣錦志(JIANG Jinzhi)
None
景林豐收 7 號私募證券投資基金(Greenwoods Harvest No. 7 Private Securities 
Investment Fund)
上海景林資產管理有限公司(Shanghai Greenwoods Asset 
Management Co., Ltd.)
蔣錦志(JIANG Jinzhi)
None
景林景泰豐收私募證券投資基金(Greenwoods Harvest No. 7 Private Securities 
Investment Fund)
上海景林資產管理有限公司(Shanghai Greenwoods Asset 
Management Co., Ltd.)
蔣錦志(JIANG Jinzhi)
None
景林景泰全球私募證券投資基金(Greenwoods Jingtai Harvest Private Equity 
Investment Fund)
上海景林資產管理有限公司(Shanghai Greenwoods Asset 
Management Co., Ltd.)
蔣錦志(JIANG Jinzhi)
None

<<<PAGE 29>>>
29
To the best of knowledge of CSI and after making all reasonable enquiries, the CSI Ultimate Clients, together with its ultimate beneficial owners, is an 
independent third party of the Company, its subsidiaries, its Controlling Shareholders, its substantial shareholders, CSI, CLSA and the companies which are 
members of the same group of CLSA.
Upon the final maturity or termination of the CSI Client TRS by the CSI Ultimate Clients, CSI will dispose of the Offer Shares on the secondary market and 
the CSI Ultimate Clients will receive a final termination amount of the CSI Back-to-back TRS which will have taken into account all the economic returns or 
economic loss in relation to the Offer Shares and the fixed amount of transaction fees of the CSI Back-to-back TRS and the CSI Client TRS. Due to its internal 
policy, CSI will not exercise the voting right of the Offer Shares during the terms of the CSI Back-to-back TRS.
(6) 
CITIC Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their investors 
(“CITIC Asset Management Ultimate Client”), each of which is an independent third party of the Company, its subsidiaries, its Controlling Shareholders, 
its substantial shareholders, CITIC Asset Management, CLSA and the companies which are members of the same group of CLSA. No ultimate beneficial 
owner holds 30% or more interest in the funds. The China Asset Management Ultimate Client include CITIC SECURITIES COMPANY LIMITED-XINHANG 
ZHIYUAN NO.1, CITIC SECURITIES COMPANY LIMITED-XINHANG ZHIYUAN NO.3 and CITIC Securities AM-Guibinfengyuan No.118 QDII.
To the best of knowledge of CITIC Asset Management and after making all reasonable enquiries, CITIC Asset Management Ultimate Client, together with 
its ultimate beneficial owners, is an independent third party of the Company, its subsidiaries, its Controlling Shareholders, its substantial shareholders, CITIC 
Asset Management, CLSA and the companies which are members of the same group of CLSA.
(7) 
GF International will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their investors, each of which is 
an independent third party of the Company, its subsidiaries, its Controlling Shareholders, its substantial shareholders, GF International, GF Securities (Hong 
Kong) Brokerage and the companies which are members of the same group of GF Securities Co., Ltd. (廣發証券股份有限公司) (Stock Code: 1776) (“GF 
Securities”). No ultimate beneficial owner holds 30% or more interest in the funds.

<<<PAGE 30>>>
30
To the best of knowledge of GF International and after making all reasonable enquiries, GF International Ultimate Client, together with its ultimate beneficial 
owners, is an independent third party of the Company, its subsidiaries, its Controlling Shareholders, its substantial shareholders, GF Securities (Hong Kong) 
Brokerage and the companies which are members of the same group of CLSA.
(8) 
E Fund and E Fund HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the sub funds on behalf of the underlying clients 
(the “E Fund Ultimate Clients”). GF Securities (Hong Kong) Brokerage is an indirect wholly-owned subsidiary of GF Securities, which in turn holds 22.65% 
of the issued share capital of E Fund. E Fund HK is a wholly-owned subsidiary of E Fund. Therefore, each of E Fund and E Fund HK constitutes a member of 
the same group with GF. Securities (Hong Kong) Brokerage. Accordingly, each of E Fund and E Fund HK is considered as a connected client of GF Securities 
(Hong Kong) Brokerage pursuant to paragraph 1B(7) of the Placing Guidelines. Notwithstanding GF Securities (Hong Kong) Brokerage’ shareholding in E 
Fund and E Fund HK (through E Fund) and that E Fund, E Fund HK and GF Securities (Hong Kong) Brokerage are members of the same group of companies, 
(i) GF Securities (Hong Kong) Brokerage does not have control over E Fund and E Fund HK by virtue of its shareholding or control over the board of directors 
of E Fund and E Fund HK; and (ii) both E Fund and E Fund HK operate and make investment decisions independently from GF Securities (Hong Kong) 
Brokerage.
E Fund and E Fund HK are to invest on discretionary basis on behalf of the E Fund Ultimate Clients which are independent third parties and no proprietary 
money is used for the subscribing. To the best knowledge of E Fund and E Fund HK and after making all reasonable enquiries, (i) each of the E Fund Ultimate 
Clients is an independent third party of the GF Securities (Hong Kong) Brokerage, E Fund, E Fund HK, the companies which are members of the same group 
of companies as GF Securities (Hong Kong) Brokerage; and (ii) neither E Fund or E Fund HK is a collective investment scheme which is not authorised by the 
SFC nor is expected to hold the Offer Shares on behalf of such scheme. Each of E Fund and E Fund HK also confirms that it will not hold any Offer Shares 
placed to them on a proprietary basis for themselves or for any group member of GF Securities (Hong Kong) Brokerage. The Offer Shares placed to each of E 
Fund and E Fund HK will be held by them through the Sub Funds on behalf of independent third parties.
(9) 
Value Partners will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their investors, each of which is 
an independent third party of the Company, its subsidiaries, its Controlling Shareholders, its substantial shareholders, Value Partners, GF Securities and the 
companies which are members of the same group of GF Securities.
To the best of knowledge of Value Partners, the Value Partners Ultimate Client, together with its ultimate beneficial owners, is an independent third party of 
the Company, its subsidiaries, its Controlling Shareholders, its substantial shareholders, Value Partners, GF Securities and the companies which are members 
of the same group of GF Securities.
(10) 
Bosera Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager managing the sub-funds on behalf of its underlying 
client, each of which is an independent third party of the Company, its subsidiaries, its substantial shareholders, CMS and CMBI and the companies which are 
members of the same group of CMS and CMBI to the best knowledge and belief of Bosera Asset Management.
(11) 
Each of the connected clients is not a collective investment scheme which is not authorized by the SFC, nor is it holding the Offer Shares on behalf of such 
schemes.

<<<PAGE 31>>>
31
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or 
any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer or 
solicitation to purchase or subscribe for securities in the United States. The securities mentioned 
herein have not been, and will not be, registered under the U.S. Securities Act. The securities 
may not be offered or sold in the United States except pursuant to an available exemption from, 
or in a transaction not subject to, the registration requirements of the U.S. Securities Act and in 
accordance with any applicable state securities laws in the United States. The Offer Shares may 
only be offered and sold (a) in the United States to QIBs in reliance on Rule 144A or another 
available exemption from registration requirements under the U.S. Securities Act, and (b) outside 
the United States in offshore transactions in reliance on Regulation S. There will be no public 
offer of securities in the United States.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated January 29, 2026 issued by the Company for 
detailed information about the Global Offering described above before deciding whether or not 
to invest in the Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the paragraph headed “Underwriting 
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing 
Date (which is currently expected to be on February 6, 2026).

<<<PAGE 32>>>
32
Public Float and Free Float
Immediately after the completion of the Global Offering (before any exercise of the Over-
allotment Option), the total market value of the H Shares to be held by the public is expected to be 
approximately HK$10,684.1 million, calculated based on the final Offer Price of HK$39.00, which 
is higher than the prescribed expected market value of H Shares required to be held in public 
hands of not less than HK$3,000 million under Rule 19A.13A(2)(b) of the Listing Rules, thereby 
satisfying Rule 19A.13A(2) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following and 
including the Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing 
shall not be counted towards the free float of the H Shares of the Company at the time of Listing. 
Based on the Offer Price of HK$39.00 per H Share, the Company confirmed that it complies with 
the free float requirement under Rule 19A.13C(2)(b) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering (before any 
exercise of the Over-allotment Option): (i) the Shares will be held by at least 300 Shareholders 
at the time of Listing, in compliance with Rule 8.08(2) of the Listing Rules; (ii) the three largest 
public Shareholders will not hold more than 50% of the H Shares held in public hands at the 
time of Listing, in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; (iii) no placee 
will, individually, be placed more than 10% of the enlarged issued share capital of the Company 
immediately after the Global Offering; and (iv) there will not be any new substantial Shareholder 
(as defined in the Listing Rules) immediately after the Global Offering.

<<<PAGE 33>>>
33
Commencement of Dealings
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, February 
6, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting — Underwriting Arrangements 
and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade the H Shares on the basis of publicly available allocation 
details prior to the receipt of H Share certificates or prior to the H Share certificates becoming 
valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Friday, 
February 6, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Friday, February 6, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 100 H Shares each, and the stock code of the H Shares will 
be 2714.
By order of the Board
Muyuan Foods Co., Ltd.
Mr. Qin Yinglin
Chairman of the Board and President
Hong Kong, February 5, 2026
As at the date of this announcement, the Board comprises (i) Mr. QIN Yinglin, Mr. CAO Zhinian 
and Ms. YANG Ruihua as executive Directors; (ii) Ms. QIAN Ying and Mr. SU Danglin as non-
executive Directors; and (iii) Mr. CHOW Ming Sang, Mr. YAN Lei and Mr. FENG Genfu as 
independent non-executive Directors.
