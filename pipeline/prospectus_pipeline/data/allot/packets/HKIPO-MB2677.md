# 配发结果公告抽取任务：2677.HK Distinct Healthcare Holdings Limited

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**05/02/2026 18:11**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0205/2026020501800.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2677.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) 
and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not, and is not intended to, constitute or form a part of any offer or solicitation to purchase or 
subscribe for securities in the United States or in any other jurisdiction. The Offer Shares have not been and will not 
be registered under the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities 
Act”) or securities law of any state or other jurisdiction of the United States and may not be offered, sold, pledged or 
otherwise transferred within the United States, except in transactions exempt from, or not subject to, the registration 
requirements of the U.S. Securities Act and in compliance with any applicable state securities laws. There will be no 
public offer of the Offer Shares in the United States. The Offer Shares are being offered and sold solely outside the 
United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act and applicable laws of 
each jurisdiction where those offers and sales occur.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus 
dated January 29, 2026 (the “Prospectus”) issued by Distinct Healthcare Holdings Limited (卓正醫療控股有限公
司)(the “Company”) for detailed information about the Global Offering described below before deciding whether or 
not to invest in the Shares thereby being offered. The Company has not been and will not be registered under the U.S. 
Investment Company Act of 1940, as amended.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
In connection with the Global Offering, Haitong International Securities Company Limited as stabilization manager 
(the “Stabilization Manager”) (or its affiliates or any person acting for it) on behalf of the Underwriters, to the extent 
permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, may make purchases, over-
allocate or effect transactions in the market or otherwise take such stabilizing action(s) with a view to stabilizing 
or supporting the market price of the Shares at a level higher than that which might otherwise prevail for a limited 
period after the Listing Date. However, there is no obligation on the Stabilization Manager (or its affiliates or any 
person acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will be conducted 
at the absolute discretion of the Stabilization Manager (or its affiliates or any person acting for it) and in what the 
Stabilization Manager reasonably regards as the best interest of the Company, (b) may be discontinued at any time and 
(c) is required to be brought to an end within 30 days after the last day for lodging applications under the Hong Kong 
Public Offering.
Potential investors should note that no stabilizing action can be taken to support the price of the Shares for longer than 
the stabilization period, which will begin on the Listing Date and is expected to expire on March 5, 2026, being the 
30th day after the last day for lodging applications under the Hong Kong Public Offering. After this date, when no 
further stabilizing action may be taken, demand for the Shares, and therefore the price of the Shares, could fall.
The obligations of the Hong Kong Underwriters under the Hong Kong Underwriting Agreement to subscribe for, 
and to procure subscribers for, the Hong Kong Offer Shares, are subject to termination by the Joint Sponsor-Overall 
Coordinators (for themselves and on behalf of the Underwriters) if certain events shall occur prior to 8:00 a.m. on the 
Listing Date. Such grounds are set out in the section headed “Underwriting” in the Prospectus. It is important that you 
refer to that section for further details.

<<<PAGE 2>>>
2
Distinct Healthcare Holdings Limited
卓正醫療控股有限公司
(Incorporated in the Cayman Islands with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the 
Global Offering
:
4,750,000 Shares (subject to the Over-
allotment Option)
Number of Hong Kong Offer Shares
:
475,000 Shares
Number of International Offer Shares
:
4,275,000 Shares (subject to the Over-
allotment Option)
Final Offer Price
:
HK$59.90 per Offer Share, plus brokerage 
fee of 1.0%, SFC transaction levy of 
0.0027%, Stock Exchange trading fee of 
0.00565% and AFRC transaction levy of 
0.00015%
Nominal value
:
USD0.001 per Share
Stock code
:
2677
Joint Sponsors, Joint Sponsor-Overall Coordinators, Joint Overall Coordinators,
Joint Global Coordinators, Joint Bookrunners, Joint Lead Managers
Joint Overall Coordinators, Joint Global Coordinators, Joint Bookrunners, 
Joint Lead Managers
Joint Global Coordinators, Joint Bookrunners, Joint Lead Managers
Joint Bookrunners, Joint Lead Managers

<<<PAGE 3>>>
3
DISTINCT HEALTHCARE HOLDINGS LIMITED/卓正醫療控股有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated January 29, 2026 (the “Prospectus”) issued by 
Distinct Healthcare Holdings Limited (卓正醫療控股有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the Shares could 
move substantially even with a small number of Shares traded and should exercise extreme 
caution when dealing in the Shares.
SUMMARY
Company information
Stock code
2677
Stock short name
DISTINCT HEALTH
Dealings commencement date
February 6, 2026*
* see note at the end of the announcement
Price Information
Final Offer Price
HK$59.90
Offer Price Range
HK$57.70 – HK$66.60
Offer Shares and Share Capital
Number of Offer Shares
4,750,000
Final Number of Offer Shares in Hong Kong Public Offering
475,000
Final Number of Offer Shares in International Offering
(subject to the Over-allotment Option)
4,275,000
Number of issued shares upon Listing
64,384,350
Over-allocation
No. of Offer Shares over-allocated
712,500
 – International Offering
712,500
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.

<<<PAGE 4>>>
4
Proceeds
Gross proceeds (Note)
HK$284.53 million
Less: Estimated listing expenses payable based 
  on the Final Offer Price
HK$(75.67) million
Net proceeds
HK$208.86 million
Note: Gross proceeds refer to the amount to which the issuer is entitled to receive. For details of the use of 
proceeds, please refer to the Prospectus dated January 29, 2026.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
147,844
No. of successful applications
9,500
Subscription level
2,730.73 times
Reallocation
No
No. of Offer Shares initially available under the Public Offer
475,000
Final no. of Offer Shares under the Public Offer
475,000
% of Offer Shares under the Public Offer to the Global Offering
10%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by identification number or www.hkeipo.hk/IPOResult for the full list 
of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
211
Subscription Level
5.79 times
No. of Offer Shares initially available under the International Offering
4,275,000
Final no. of Offer Shares under the International Offering 
4,275,000
% of Offer Shares under the International Offering to 
the Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, controlling shareholders, 
substantial shareholders, existing shareholders of the Company or any of its subsidiaries or their 
respective close associates; and (ii) none of the placees and the public who have purchased the 
Offer Shares are accustomed to taking instructions from the Company, any of the Directors, chief 
executive of the Company, controlling shareholders, substantial shareholders, existing shareholders 
of the Company or any of its subsidiaries or their respective close associates in relation to the 
acquisition, disposal, voting or other disposition of Shares registered in his/her/its name or 
otherwise held by him/her/it.

<<<PAGE 6>>>
6
The placees in the International offer include the following:
Cornerstone Investors
Investor(1)
Number of Offer 
Shares allocated
% of total number 
of Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing 
shareholders 
or their close 
associates
Health Vision Hong Kong Limited
727,200
15.31%
1.13%
No
KingMed Diagnostics (Hong 
 Kong) Limited (金域檢驗(香港)
 有限公司)
386,600
8.14%
0.60%
No
Mininglamp Technology
257,750
5.43%
0.40%
No
Galaxy Dynasty Limited
128,850
2.71%
0.20%
No
Total
1,500,400
31.59%
2.33%
Notes:
(1) 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in 
the Prospectus.

<<<PAGE 7>>>
7
Allottee with Waivers/Consents Obtained
Investor
Number of 
Offer Shares 
allocated
% of total 
number of 
Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Relationship
Allottee with consent under paragraph 1C(1) of Appendix F1 to the Listing Rules (the “Placing 
Guidelines”) in relation to allocation to a connected client (1)
Guotai Junan 
Investments (Hong 
Kong) Limited
257,700
5.43%
0.40%
A connected client of 
Haitong International 
Securities Company 
Limited
Notes:
(1) 
For details of the consent under paragraph 1C(1) of the Placing Guidelines in relation to allocation to a 
connected client, please refer to the section headed “Other Information” in this announcement.
Allottee who is customer(s) or client(s)/supplier(s) of the Group
Investor
Number of 
Offer Shares 
allocated
% of total 
number of 
Offer Shares
 (assuming the
Over-allotment
Option is not
exercised)
of total
issued share
capital after the
Global Offering
(assuming the
Over-allotment
Option is not
exercised)
Relationship
KingMed Diagnostics 
(Hong Kong) 
Limited
386,600
8.14%
0.60%
A wholly owned 
subsidiary of a supplier 
of the Group

<<<PAGE 8>>>
8
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of shares held 
in the Company subject 
to lock-up undertakings 
upon Listing
% of shareholding in 
the Company subject to 
lock-up undertakings 
upon Listing (assuming 
the Over-allotment 
Option is not exercised)
Last day subject to the 
lock-up undertakings(1)
Cheuk Sing Ho(2)
11,283,000
17.52%
August 5, 2028(3)
Distinct Partners I Limited(2)
2,640,250
4.10%
August 5, 2027(4)
Mr. CAO Shaoshan(2)
1,000,000
1.55%
February 5, 2027(5)
Nineteen Seventy-Seven(2)
867,000
1.35%
February 5, 2027(5)
Proxy Shares held by H Capital 
 IV, L.P.(2)
1,597,048
2.48%
February 5, 2027(6)
Proxy Shares held by Image 
 Frame Investment (HK) 
 Limited(2)
2,079,683
3.23%
February 5, 2027(6)
Proxy Shares held by 
 MPC II L.P.(2)
319,096
0.50%
February 5, 2027(6)
Proxy Shares held by MPC II-A 
 L.P.(2)
35,455
0.06%
February 5, 2027(6)
Subtotal
19,821,532
30.79%
Notes:
(1) 
The expiry date of the lock-up period shown in the table above is pursuant to the deeds of lock-up 
undertaking entered into by each of the Controlling Shareholders in favor of the Company. The lock-up 
requirement under the deeds of lock-up undertaking is longer than the lock-up period in the undertakings 
given by the Controlling Shareholders pursuant to the Hong Kong Underwriting Agreement. The Controlling 
Shareholders will cease to be prohibited from disposing of or transferring Shares after the indicated date.
(2) 
Mr. Wang, Cheuk Sing Ho, the Concert Parties and Distinct Partners I Limited, through (i) the Acting-
in-Concert Agreement, (ii) the Cheuk Sing Ho Agreement, (iii) the trust deed of Distinct Trust I, and (iv) 
the Voting Proxy Agreements, will exercise the voting rights attached to 19,821,532 Shares in aggregate 
immediately following completion of the Global Offering. See the sections headed “History, Reorganization 
and Corporate Structure” and “Relationship with Our Controlling Shareholders” in the Prospectus for details.
(3) 
Pursuant to a deed of lock-up undertaking entered into by Cheuk Sing Ho in favor of the Company, 
11,283,000 Shares held by Cheuk Sing Ho will be subject to a 30-month lock-up period since the Listing 
Date.
(4) 
Pursuant to a deed of lock-up undertaking entered into by Distinct Partners I Limited in favor of the 
Company, 2,640,250 Shares held by Distinct Partners I Limited will be subject to a 18-month lock-up period 
since the Listing Date.
(5) 
Pursuant to deeds of lock-up undertaking entered into by Mr. CAO Shaoshan and Nineteen Seventy-Seven in 
favor of the Company, 1,000,000 Shares held by Mr. CAO Shaoshan and 867,000 Shares held by Nineteen 
Seventy-Seven will be subject to a 12-month lock-up period since the Listing Date.
(6) 
Pursuant to the Voting Proxy Agreements and deeds of lock-up undertaking entered into by each of the 
Proxy Shareholders in favor of the Company, an aggregate of 4,031,282 Proxy Shares held by the Proxy 
Shareholders will be subject to a 12-month lock-up period since the Listing Date. See the section headed 
“History, Reorganization and Corporate Structure – Voting Agreements” in the Prospectus for details.

<<<PAGE 9>>>
9
Pre-IPO Investors (as defined in the “History, Reorganization and Corporate Structure” 
section of the Prospectus)
Name
Number of shares 
held in the Company 
subject to lock-up 
undertakings
upon Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings(1)
MPC II, L.P.(2)
375,543
0.58%
August 5, 2026
MPC II-A, L.P.(3)
41,727
0.06%
August 5, 2026
Waterwood DHC Project Ltd
7,500,000
11.65%
August 5, 2026
Humansa Tech (HK) Limited
1,144,200
1.78%
August 5, 2026
Beijing Tiantu Xingbei Investment 
Center (Limited Partnership) (北京
天圖興北投資中心(有限合夥))
1,021,460
1.59%
August 5, 2026
Chengdu Tiantu Tiantou Dongfeng 
Equity Investment Fund Center 
(Limited Partnership) (成都天圖天
投東風股權投資基金中心(有限合
夥))
437,770
0.68%
August 5, 2026
CICC Kangrui Phase I (Ningbo) 
Equity Investment Fund Partnership 
(Limited Partnership) (中金康瑞壹
期(寧波)股權投資基金合夥企業
(有限合夥))
1,979,610
3.07%
August 5, 2026
Waterwood Tactics Limited
989,810
1.54%
August 5, 2026
Qianhai Ark (BVI) Investment Co., 
Limited
441,527
0.69%
August 5, 2026
Image Frame Investment (HK) 
Limited(4)
9,486,369
14.73%
August 5, 2026
H Capital IV, L.P.(5)
7,284,852
11.31%
August 5, 2026
H SF Investment LLC
35,100
0.05%
August 5, 2026

<<<PAGE 10>>>
10
Name
Number of shares 
held in the Company 
subject to lock-up 
undertakings
upon Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings(1)
Chengdu Tianfu Qianshi Equity 
Investment Partnership Enterprise 
(Limited Partnership) (成都天府淺
石股權投資合夥企業(有限合夥))
351,600
0.55%
August 5, 2026
Chinalin Chuangxin Investment Co. 
Ltd. (華林創新投資有限公司)
351,600
0.55%
August 5, 2026
Violet Gem Limited
1,019,700
1.58%
August 5, 2026
Subtotal
32,460,868
50.42%
Notes:
(1) 
The expiry date of the lock-up period shown in the table above is pursuant to the deeds of lock-up 
undertaking entered into by each of the Pre-IPO Investors named herein in favor of the Company. (A) 
1,750,000 Shares held by Tiantu Xingbei Investment Center (Limited Partnership) (北京天圖興北投資中心
(有限合夥)), (B) 750,000 Shares held by Chengdu Tiantu Dongfeng Equity Investment Fund Center (Limited 
Partnership) (成都天圖天投東風股權投資基金中心(有限合夥)), (C) 1,080,000 Shares held by MPC II, L.P. 
and 120,000 Shares held by MPC II-A, L.P., and (D) the total of 492,200 Shares held by Deripi Limited, 
Buchkana Holdings Limited and Flarensi Holdings Limited aggregately, are not subject to any lock-up upon 
the Listing.
(2) 
Excluding the 319,096 Proxy Shares held by MPC II, L.P., which are subject to a 12-month lock-up 
period since the Listing Date as disclosed under the section headed “Lock-up Undertakings – Controlling 
Shareholders” in this announcement. See the section headed “History, Reorganization and Corporate Structure 
– Voting Agreements” in the Prospectus for details.
(3) 
Excluding the 35,455 Proxy Shares held by MPC II-A, L.P., which are subject to a 12-month lock-up 
period since the Listing Date as disclosed under the section headed “Lock-up Undertakings – Controlling 
Shareholders” in this announcement. See the section headed “History, Reorganization and Corporate Structure 
– Voting Agreements” in the Prospectus for details.
(4) 
Excluding the 2,079,683 Proxy Shares held by Image Frame Investment (HK) Limited, which are subject to a 
12-month lock-up period since the Listing Date as disclosed under the section headed “Lock-up Undertakings 
– Controlling Shareholders” in this announcement. See the section headed “History, Reorganization and 
Corporate Structure – Voting Agreements” in the Prospectus for details.
(5) 
Excluding the 1,597,048 Proxy Shares held by H Capital IV, L.P., which are subject to a 12-month lock-up 
period since the Listing Date as disclosed under the section headed “Lock-up Undertakings – Controlling 
Shareholders” in this announcement. See the section headed “History, Reorganization and Corporate Structure 
– Voting Agreements” in the Prospectus for details.

<<<PAGE 11>>>
11
Existing Shareholders (other than the Controlling Shareholders and the Pre-IPO Investors as 
defined in the “History, Reorganization and Corporate Structure” section of the Prospectus)
Name
Number of shares 
held in the Company 
subject to lock-up 
undertakings
upon Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings(1)
Shine Step International Limited
800,000
1.24%
August 5, 2026
Distinct Partners II Limited
2,359,750
3.67%
August 5, 2027
Subtotal
3,159,750
4.91%
Note:
(1) 
The expiry date of the lock-up period shown in the table above is pursuant to the deeds of lock-up 
undertaking entered into by each of the existing Shareholders named herein in favor of the Company.
Cornerstone Investors
Name
Number of shares 
held in the Company 
subject to lock-up 
undertakings
upon Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings(1)
Health Vision Hong Kong Limited
727,200
1.13%
August 5, 2026
KingMed Diagnostics (Hong Kong) 
 Limited (金域檢驗(香港)有限公司)
386,600
0.60%
August 5, 2026
Mininglamp Technology
257,750
0.40%
August 5, 2026
Galaxy Dynasty Limited
128,850
0.20%
August 5, 2026
Subtotal
1,500,400
2.33%
Note:
(1) 
In accordance with the relevant Listing Rule/guidance materials, the required lock-up ends on August 5, 
2026. The Cornerstone Investors will cease to be prohibited from disposing of or transferring Shares after 
the indicated date. For details, please refer to the section headed “Cornerstone Investors – Restrictions on the 
Cornerstone Investors” of the Prospectus.

<<<PAGE 12>>>
12
PLACEE CONCENTRATION ANALYSIS
Placees
Number 
of Shares 
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
Option is fully 
exercised and 
new Shares 
are issued)
Allotment 
as % of total 
Offer Shares 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment 
as % of total 
Offer Shares 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Shares 
are issued)
Number of 
Shares held 
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
Option is fully 
exercised and 
new Shares 
are issued)
Top 1
1,041,450
24.36%
20.88%
21.93%
19.07%
1,041,450
1.62%
1.60%
Top 5
3,066,250
71.73%
61.48%
64.55%
56.13%
3,066,250
4.76%
4.71%
Top 10
4,128,700
96.58%
82.78%
86.92%
75.58%
4,128,700
6.41%
6.34%
Top 25
4,779,550
111.80%
95.83%
100.62%
87.50%
4,779,550
7.42%
7.34%
Note
* 
Ranking of placees is based on the number of Shares allotted to the placees.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
Number 
of Shares 
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
Option is fully 
exercised and 
new Shares 
are issued)
Allotment 
as % of total 
Offer Shares 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment 
as % of total 
Offer Shares 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Shares 
are issued)
Number of 
Shares held 
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
Option is fully 
exercised and 
new Shares 
are issued)
Top 1
0
0.00%
0.00%
0.00%
0.00%
15,790,250
24.52%
24.26%
Top 5
0
0.00%
0.00%
0.00%
0.00%
48,687,242
75.62%
74.79%
Top 10
1,041,450
24.36%
20.88%
21.93%
19.07%
58,203,773
90.40%
89.41%
Top 25
4,265,500
99.78%
85.52%
89.80%
78.09%
63,864,750
99.19%
98.11%
Note
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 13>>>
13
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 147,844 valid 
applications made by the public will be conditionally allocated on the basis set out below:
Pool A
Number
of Shares
applied for
Number
of valid
applications
Basis of allocation/ballot
Approximate
percentage
allotted of the
total number of
Shares applied
for
50
59,805
599 out of 59,805 applicants to receive 50 shares
1.00%
100
32,178
454 out of 32,178 applicants to receive 50 shares
0.71%
150
4,772
83 out of 4,772 applicants to receive 50 shares
0.58%
200
2,600
52 out of 2,600 applicants to receive 50 shares
0.50%
250
2,317
52 out of 2,317 applicants to receive 50 shares
0.45%
300
1,991
49 out of 1,991 applicants to receive 50 shares
0.41%
350
965
26 out of 965 applicants to receive 50 shares
0.38%
400
1,425
40 out of 1,425 applicants to receive 50 shares
0.35%
450
884
27 out of 884 applicants to receive 50 shares
0.34%
500
5,215
164 out of 5,215 applicants to receive 50 shares
0.31%
600
1,283
44 out of 1,283 applicants to receive 50 shares
0.29%
700
2,538
94 out of 2,538 applicants to receive 50 shares
0.26%
800
1,061
42 out of 1,061 applicants to receive 50 shares
0.25%
900
687
29 out of 687 applicants to receive 50 shares
0.23%
1,000
3,611
160 out of 3,611 applicants to receive 50 shares
0.22%
1,500
2,126
115 out of 2,126 applicants to receive 50 shares
0.18%
2,000
1,151
72 out of 1,151 applicants to receive 50 shares
0.16%
2,500
1,053
74 out of 1,053 applicants to receive 50 shares
0.14%
3,000
858
66 out of 858 applicants to receive 50 shares
0.13%
3,500
539
45 out of 539 applicants to receive 50 shares
0.12%
4,000
503
45 out of 503 applicants to receive 50 shares
0.11%
4,500
432
41 out of 432 applicants to receive 50 shares
0.11%
5,000
1,308
128 out of 1,308 applicants to receive 50 shares
0.10%
6,000
671
72 out of 671 applicants to receive 50 shares
0.09%
7,000
564
66 out of 564 applicants to receive 50 shares
0.08%
8,000
597
74 out of 597 applicants to receive 50 shares
0.08%
9,000
501
66 out of 501 applicants to receive 50 shares
0.07%
10,000
3,098
428 out of 3,098 applicants to receive 50 shares
0.07%
20,000
1,735
338 out of 1,735 applicants to receive 50 shares
0.05%
30,000
1,192
284 out of 1,192 applicants to receive 50 shares
0.04%
40,000
770
211 out of 770 applicants to receive 50 shares
0.03%
50,000
743
228 out of 743 applicants to receive 50 shares
0.03%
60,000
546
183 out of 546 applicants to receive 50 shares
0.03%
70,000
826
299 out of 826 applicants to receive 50 shares
0.03%
Total  
140,545 Total number of Pool A successful applicants: 4,750

<<<PAGE 14>>>
14
Pool B
Approximate
percentage
allotted of the
Number  
Number 
total number of
of Shares 
of valid 
Shares applied
applied for 
applications Basis of allocation/ballot
for
80,000
2,427
1,554 out of 2,427 applicants to receive 50 shares
0.04%
90,000
522
336 out of 522 applicants to receive 50 shares
0.04%
100,000
1,415
914 out of 1,415 applicants to receive 50 shares
0.03%
150,000
1,178
773 out of 1,178 applicants to receive 50 shares
0.02%
237,500
1,757
1,173 out of 1,757 applicants to receive 50 shares
0.01%
Total
7,299
Total number of Pool B successful applicants: 4,750
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s Shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or 
indirectly, provided by the Company, its controlling shareholder(s), directors or syndicate members 
to any placees or the public (as the case may be) and the consideration payable by them for each 
Offer Share of the Company subscribed for or purchased by them is the same as the Offer Price 
determined by the Company, in addition to any brokerage, AFRC transaction levy, SFC transaction 
levy and trading fee payable.
OTHER INFORMATION
Placing to a connected client with prior consent under paragraph 1C(1) of the Placing 
Guidelines
The Company has applied to the Stock Exchange, and the Stock Exchange has granted, a consent 
under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate certain Offer 
Shares in the International Offering to a connected client as placees. The allocation of Offer Shares 
to such connected client is in compliance with all the conditions under the consent granted by the 
Stock Exchange.
Details of the placement to connected client are set out below.

<<<PAGE 15>>>
15
No.
Connected 
distributor
Connected client
Relationship
Whether the 
connected client 
will hold 
the beneficial 
interests of the 
Offer Shares 
on a non – 
discretionary 
basis or 
discretionary 
basis for 
independent 
third parties
Number of 
Offer Shares to 
be allocated to 
the connected 
client
Approximate 
percentage of 
Offer Shares 
allocated to the 
connected client 
(assuming the 
Over-Allotment 
Option is not 
exercised)
Approximate 
percentage of 
total issued 
share capital 
after the 
Global Offering 
(assuming the 
Over-Allotment 
Option is not 
exercised)
1.
Haitong 
International 
Securities 
Company 
Limited (“HTI 
Securities”)
Guotai Junan 
Investments 
(Hong Kong) 
Limited 
(“GTJAI”)(1)
GTJAI is a 
member of the 
same group of 
HTI Securities
Non-discretionary 
 basis
257,700
5.43%
0.40%
Note:
(1) 
GTJAI proposes to subscribe for and hold the Offer Shares as a placee under the International Offering on 
behalf of its ultimate client on a non-discretionary basis.
GTJAI shall hold the Offer Shares for hedging purpose as the single underlying asset of a back-to-back total 
return swap transaction (the “GTHT Back-to-back TRS”) to be entered into between GTJAI and Guotai 
Haitong Securities Co., Ltd. (國泰海通證券股份有限公司) (the “GTHT Onshore Parent”) in connection 
with a total return swap order (the “GTHT Client TRS”) to be entered into by GTHT Onshore Parent and an 
ultimate client (the “GTHT Onshore Ultimate Client”). Such GTHT Client TRS is to be fully funded by the 
GTHT Onshore Ultimate Client. GTJAI will hold the Offer Shares on a non-discretionary basis for the purpose 
of hedging the economic exposure under the GTHT Back-to-back TRS and GTHT Client TRS only. During the 
tenor of the GTHT Client TRS, all economic returns of the Offer Shares will be passed to the GTHT Onshore 
Ultimate Client and all economic losses shall be borne by the GTHT Onshore Ultimate Client, subject to the 
terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS, and GTJAI will not take part in 
any economic return or bear any economic loss in relation to the price of the Offer Shares. The GTHT Onshore 
Ultimate Client may request to redeem the Shares at their own discretion, upon which GTJAI shall dispose of 
the Offer Shares and settle the GTHT Back-to-back TRS and GTHT Client TRS in cash in accordance with the 
terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS documents. Due to its internal 
policy, GTJAI will not exercise the voting right attaching to the Offer Shares during the tenor of the GTHT 
Back-to-back TRS and GTHT Client TRS.

<<<PAGE 16>>>
16
The GTHT Onshore Ultimate Client is Binghao Value Selected Private Securities Investment Fund (秉昊價值
精選私募證券投資基金). It has no ultimate beneficial owner holding 30% or more of its interest. To the best 
knowledge of GTJAI after making all reasonable enquiries, each of the GTHT Onshore Ultimate Client and its 
beneficial owners is an independent third party of GTJAI, HTI Securities and the companies which are members 
of the same group of HTI Securities.
GTJAI is not a collective investment scheme which is not authorized by the SFC nor is expected to hold the 
Offer Shares on behalf of such scheme.
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the 
“Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy 
or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer or 
solicitation to purchase or subscribe for securities in the United States. The securities mentioned 
herein have not been, and will not be, registered under the United States Securities Act of 1933, 
as amended (the “U.S. Securities Act”). The securities may not be offered or sold in the United 
States except pursuant to an exemption from the registration requirements of the U.S. Securities 
Act and in compliance with any applicable state securities laws, or outside the United States 
unless in compliance with Regulation S under the U.S. Securities Act. There will be no public 
offer of securities in the United States.
The Offer Shares are being offered and sold outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated January 29, 2026 issued by Distinct 
Healthcare Holdings Limited for detailed information about the Global Offering described below 
before deciding whether or not to invest in the Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Joint Sponsors and the Joint 
Sponsor-Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) 
shall be entitled to terminate their obligations under the Hong Kong Underwriting Agreement 
with immediate effect upon the occurrence of any of the events set out in the paragraph headed 
“Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – 
Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on 
the Listing Date (which is currently expected to be on February 6, 2026).

<<<PAGE 17>>>
17
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering, 19,301,787 Shares, representing 
approximately 29.98% of the issued share capital of our Company (before any exercise of the 
Over-allotment Option) will count towards the public float. Therefore, the number of Shares 
held in public hands is higher than the prescribed percentage of Shares required to be held in 
public hands of 25% under Rule 8.08(1) of the Listing Rules, satisfying the minimum percentage 
requirement in compliance with Rule 8.08(1) of the Listing Rules.
Each of the Cornerstone Investors, the Controlling Shareholders and certain other existing 
Shareholders (including Pre-IPO Investors) has agreed to a lock-up period of no less than six 
months following the Listing Date. For details, please refer to the section headed “Lock-up 
Undertakings” of this announcement. As such, Shares held by them upon the Listing shall not be 
counted towards the free float of the Shares of the Company at the time of Listing. Based on the 
final Offer Price of HK$59.90 per Share, the Company satisfies the free float requirement under 
Rule 8.08A of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering: (i) the 
Shares will be held by at least 300 Shareholders at the time of Listing, in compliance with Rule 
8.08(2) of the Listing Rules; (ii) the three largest public Shareholders will not hold more than 50% 
of the Shares held in public hands at the time of Listing, in compliance with Rules 8.08(3) and 8.24 
of the Listing Rules; (iii) no placee will, individually, be placed more than 10% of the enlarged 
issued share capital of the Company immediately after the Global Offering; and (iv) there will not 
be any new substantial Shareholder (as defined in the Listing Rules) immediately after the Global 
Offering.
COMMENCEMENT OF DEALINGS
The Share certificates will only become valid evidence of title at 8:00 a.m. (Hong Kong time) 
on Friday, February 6, 2026, provided that (i) the Global Offering has become unconditional in 
all respects, and (ii) the right of termination described in the section headed “Underwriting — 
Underwriting Arrangements and Expenses — Hong Kong Underwriting Agreement — Grounds for 
Termination” in the Prospectus has not been exercised. Investors who trade the Shares prior to the 
receipt of Share certificates or the Share certificates becoming valid evidence of title do so entirely 
at their own risk.

<<<PAGE 18>>>
18
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong Kong 
time) on Friday, February 6, 2026, it is expected that dealings in the Shares on the Stock Exchange 
will commence at 9:00 a.m. on Friday, February 6, 2026. The Shares will be traded in board lots of 
50 Shares each and the stock code of the Shares will be 2677.
By order of the Board
Distinct Healthcare Holdings Limited
卓正醫療控股有限公司
WANG Zhiyuan
Chairman and Executive Director
Hong Kong, February 5, 2026
As of the date of this announcement, the Board comprises Mr. WANG Zhiyuan and Mr. SHI Yi 
as executive Directors, Mr. CAO Shaoshan, Mr. ZHANG Xiangdong, Mr. WEI Guoxing, Ms. 
CHEN Xiaohong and Mr. HAO Rui as non-executive Directors, and Ms. CHEN Rui, Mr. WANG 
Yonggang, Mr. WANG Gaofei and Dr. GAO Pingyang as proposed independent non-executive 
Directors.
