# 配发结果公告抽取任务：1768.HK BUSY MING GROUP CO., LTD.- H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**27/01/2026 22:20**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0127/2026012701713.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1768.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated January 20, 2026 (the “Prospectus”) issued by Busy Ming Group Co., Ltd. (湖南鳴鳴
很忙商業連鎖股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. Potential investors should read the Prospectus for detailed information about the Company 
and the Global Offering described below before deciding whether or not to invest in the Offer Shares.
This announcement is not for release, publication or distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities 
in the United States or in any other jurisdiction. The Offer Shares have not been and will not be registered under the 
United States Securities Act of 1933, as amended from time to time (the “U.S. Securities Act”) or securities law of 
any state or other jurisdiction of the United States and may not be offered, sold, pledged or transferred within the 
United States, except in transactions exempt from, or not subject to, the registration requirements of the U.S. Securities 
Act. There will be no public offer of the Offer Shares in the United States. The Offer Shares are being offered and 
sold (1) solely to qualified institutional buyers as defined in Rule 144A under the U.S. Securities Act pursuant to an 
exemption from registration under the U.S. Securities Act and (2) outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, Goldman Sachs (Asia) L.L.C. as stabilizing manager (the “Stabilizing 
Manager”), or any person acting for it, on behalf of the Underwriters, may over-allocate or effect transactions with 
a view to stabilizing or supporting the market price of the H Shares at a level higher than that which might otherwise 
prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing Manager (or any 
person acting for it) to conduct any such stabilizing action, which, if commenced, will be done at the sole and absolute 
discretion of the Stabilizing Manager, or any person acting for it, and may be discontinued at any time. Any such 
stabilizing action is required to be brought to an end on the 30th day after the last day for the lodging of applications 
under the Hong Kong Public Offering. Such stabilizing action, if taken, may be effected in all jurisdictions where it is 
permissible to do so, in each case in compliance with all applicable laws, rules and regulatory requirements, including 
the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made 
under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that stabilizing action cannot be taken to support the price of the H Shares for 
longer than the stabilization period which begins on the Listing Date and is expected to expire on the 30th day after 
the last day for the lodging of applications under the Hong Kong Public Offering. After this date, no further stabilizing 
action may be taken, and demand for the H Shares and the price of the H Shares could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out 
in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/
or not resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint Sponsors and the 
Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the 
events set out in the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public 
Offering – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing 
Date.

<<<PAGE 2>>>
2
BUSY MING GROUP CO., LTD.
湖南鳴鳴很忙商業連鎖股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under
the Global Offering
:
15,511,200 H Shares (taking into account 
 the full exercise of the Offer Size 
 Adjustment Option and subject to the 
 Over-allotment Option)
Number of Hong Kong Offer Shares
:
1,410,200 H Shares
Number of International Offer Shares
:
14,101,000 H Shares (taking into account 
 the full exercise of the Offer Size 
 Adjustment Option and subject to the 
 Over-allotment Option)
Final Offer Price
:
HK$236.60 per H Share plus brokerage 
 of 1%, SFC transaction levy of 0.0027%, 
 Hong Kong Stock Exchange trading fee 
 of 0.00565% and AFRC transaction levy 
 of 0.00015% (payable in full on 
 application in Hong Kong dollars, 
 subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
01768
Joint Sponsors, Joint Sponsor-Overall Coordinators, 
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
BUSY MING GROUP CO., LTD.
湖南鳴鳴很忙商業連鎖股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company Information
Stock code
01768
Stock short name
BUSYMING
Dealings commencement date
January 28, 2026*
*see note at the end of this announcement
Price Information
Final Offer Price
HK$236.60
Offer Price Range
HK$229.60 - HK$236.60
Offer Price Adjustment exercised
No
Offer Shares and Share Capital*
Number of Offer Shares (taking into account the full exercise 
of the Offer Size Adjustment Option)
15,511,200
Number of Offer Shares in Hong Kong Public Offering
1,410,200
Number of Offer Shares in International Offering (taking into 
account the full exercise of the Offer Size Adjustment Option)
14,101,000
Number of issued Shares upon Listing
215,511,200
*without taking into account any exercise of the Over-allotment Option

<<<PAGE 4>>>
4
The number of Offer Shares above is determined after taking into account the additional Offer 
Shares issued under the following Offer Size Adjustment Option.
Offer Size Adjustment Option (Upsize option) 
Number of additional Offer Shares issued under the option
1,410,100
- 
Hong Kong Public Offering
N/A
- 
International Offering
1,410,100
The Offer Size Adjustment Option has been exercised in full, pursuant to which the Company 
is issuing and allotting 1,410,100 additional Offer Shares, representing approximately 10% of 
the total number of Offer Shares initially available under the Global Offering, at the final Offer 
Price.
Over-allocation
No. of Offer Shares over-allocated
2,326,600
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$3,670 million
 Less: Estimated listing expenses payable based on Final 
 Offer Price
HK$142 million
Net proceeds
HK$3,528 million
Note: Gross proceeds refers to the amount to which the Company is entitled receive. For details of the use of 
proceeds, please refer to section headed “Future Plans and Use of Proceeds” of the Prospectus. In the event that 
the Over-allotment Option is exercised, the Company will adjust the allocation of the net proceeds on a pro rata 
basis. During the Track Record Period, the listing expenses charged to consolidated statement of profit or loss and 
comprehensive income were RMB23.7 million.

<<<PAGE 5>>>
5
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
229,245
No. of successful applications
14,102
Subscription level
1,899.49 times
Claw-back triggered
No
No. of Offer Shares initially available under the Hong Kong Public 
Offering
1,410,200
No. of Offer Shares reallocated from the International Offering
N/A
Final no. of Offer Shares under the Hong Kong Public Offering
1,410,200
% of Offer Shares under the Hong Kong Public Offering to the Global 
Offering
9.1%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.eipo.com.hk/eIPOAllotment to perform a search by identification number or www.eipo.com.hk/eIPOAllotment 
for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
306
Subscription Level
44.44 times
No. of Offer Shares initially available under the International Offering
12,690,900
No. of Offer Shares reallocated to the Hong Kong Public Offering
N/A
Final no. of Offer Shares under the International Offering (taking into 
account the full exercise of the Offer Size Adjustment Option)
14,101,000
% of Offer Shares under the International Offering to the Global 
Offering
90.9%

<<<PAGE 6>>>
6
The Directors confirm that, to the best of their knowledge, information and belief, save for 
(a) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by 
the Stock Exchange to permit the Company to allocate certain Offer Shares in the International 
Offering to any existing Shareholder or close associate of existing Shareholders, (b) a consent 
under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants to permit the Company to allocate certain Offer Shares in the International Offering 
to connected clients and (c) a consent under paragraph 18 of Chapter 4.15 of the Guide for New 
Listing Applicants to permit the Company to, among other things, allocate further H Shares in the 
International Offering to certain Cornerstone Investors and/or their close associates, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly by 
the Company, any of the Directors, supervisors of the Company, chief executive of the Company, 
controlling Shareholders, substantial Shareholders, existing Shareholders or any of its subsidiaries 
or their respective close associates; and (ii) none of the placees and the public who have purchased 
the Offer Shares are accustomed to taking instructions from the Company, any of the Directors, 
supervisors of the Company, chief executive of the Company, controlling Shareholders, substantial 
Shareholders, existing Shareholders or any of its subsidiaries or their respective close associates in 
relation to the acquisition, disposal, voting or other disposition of H Shares registered in his/her/its 
name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of Offer 
Shares
allocated
Approximate 
% of total 
number of 
Offer
Shares(1)
Approximate 
% of the 
total issued 
H Shares 
immediately 
following 
completion 
of the Global 
Offering(1)(2)(3)
Approximate 
% of the 
total issued 
share capital 
immediately 
following 
completion 
of the Global 
Offering(1)(2)
Existing 
Shareholders 
or their close 
associates
Tencent
1,482,400
9.56%
0.69%
0.69%
No
Temasek
1,482,400
9.56%
0.69%
0.69%
No
BlackRock
1,153,000
7.43%
0.54%
0.54%
No
FIL Investment
988,200
6.37%
0.46%
0.46%
No
Bosera 
International
329,400
2.12%
0.15%
0.15%
No
E Fund
329,400
2.12%
0.15%
0.15%
No
Springs Capital 
(Hong Kong)
329,400
2.12%
0.15%
0.15%
No
Taikang Life
329,400
2.12%
0.15%
0.15%
No
Subtotal
6,423,600
41.41%
3.01%
2.98%

<<<PAGE 7>>>
7
Notes:
(1) 
Taking into account the full exercise of the Offer Size Adjustment Option and before any exercise of the Over-
allotment Option.
(2) 
Only taking into account the H Shares allocated to the relevant investors as cornerstone investors under the 
Global Offering. In addition to the Offer Shares subscribed for as Cornerstone Investors, each of Tencent, 
Temasek and its close associate, a close associate of BlackRock and FIL Investment was allocated further Offer 
Shares as placees in the International Offering. Please refer to the section headed “Allotment Results Details 
– International Offering – Allotees with Waivers/Consents Obtained” in this announcement for details. Only 
the Offer Shares subscribed for as Cornerstone Investors are subject to lock-up as indicated below. For details, 
please refer to the section headed “Lock-up Undertakings – Cornerstone Investors” in this announcement.
(3) 
Discrepancies in the above table between the sum of the percentage of Offer Shares allocated to each investor 
and the percentage of the total Offer Shares allocated to such investors are due to rounding.
Allotees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares allocated
Approximate % 
of Offer Shares(1)
Approximate 
% of the total 
issued H Shares 
immediately 
following 
completion 
of the Global 
Offering(1)(8)
Approximate 
% of the 
total issued 
share capital 
immediately 
following 
completion 
of the Global 
Offering(1)(8)
Relationship
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 
1C(2) of the Placing Guidelines in relation to subscription for H Shares by existing Shareholder or close associate of 
existing Shareholders(2)
HongShan Growth 
VII Holdco, Ltd.(3)
329,500
2.12%
0.15%
0.15%
A close associate of an 
existing Shareholder
HCEP Management 
Limited(3)
400
Less than 0.01%
Less than 0.01%
Less than 0.01%
A close associate of an 
existing Shareholder
5Y Capital GP 
Limited(4)
164,800
1.06%
0.08%
0.08%
A close associate of an 
existing Shareholder
Jindong Hong Kong
65,900
0.42%
0.03%
0.03%
An existing 
Shareholder

<<<PAGE 8>>>
8
Investor
No. of Offer 
Shares allocated
Approximate % 
of Offer Shares(1)
Approximate 
% of the total 
issued H Shares 
immediately 
following 
completion 
of the Global 
Offering(1)(8)
Approximate 
% of the 
total issued 
share capital 
immediately 
following 
completion 
of the Global 
Offering(1)(8)
Relationship
Allotees with a consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to connected 
clients(2)
Huatai Capital 
Investment Limited 
(“HTCI”)
1,410,000
9.09%
0.66%
0.65%
A connected client 
of Huatai Financial 
Holdings (Hong Kong) 
Limited (“HTFH”)
China Southern 
Asset Management 
Co., Ltd. (南方基金
管理股份有限公司) 
(“China Southern”)
1,600
0.01%
Less than 0.01%
Less than 0.01%
A connected client of 
HTFH
CSOP Asset 
Management Limited 
(“CSOP AM”)
400
Less than 0.01%
Less than 0.01%
Less than 0.01%
A connected client of 
HTFH
Harvest Global 
Investments Limited 
(“Harvest Global”)
164,800
1.06%
0.08%
0.08%
A connected client of 
Deutsche Bank AG, 
Hong Kong Branch 
(“Deutsche Bank”)
Haitong International 
Asset Management 
(HK) Limited 
(“Haitong AM”)
100
Less than 0.01%
Less than 0.01%
Less than 0.01%
A connected client of 
Haitong International 
Securities Company 
Limited (“Haitong”)
Fullgoal Fund 
Management Co., 
Ltd. (“Fullgoal 
AM”)
89,200
0.58%
0.04%
0.04%
A connected client of 
Haitong

<<<PAGE 9>>>
9
Investor
No. of Offer 
Shares allocated
Approximate % 
of Offer Shares(1)
Approximate 
% of the total 
issued H Shares 
immediately 
following 
completion 
of the Global 
Offering(1)(8)
Approximate 
% of the 
total issued 
share capital 
immediately 
following 
completion 
of the Global 
Offering(1)(8)
Relationship
Fullgoal Asset 
Management (HK) 
Limited (“Fullgoal 
HK”, together 
with Fullgoal AM, 
“Fullgoal Funds”)
75,600
0.49%
0.04%
0.04%
A connected client of 
Haitong
China Universal 
Asset Management 
(Hong Kong) 
Company Limited 
(“China Universal 
(HK)”)
49,700
0.32%
0.02%
0.02%
A connected client 
of Orient Securities 
(Hong Kong) Limited 
(“Orient Securities”)
China Universal 
Asset Management 
Company Limited 
(匯添富基金管
理股份有限公司) 
(“CUAM”, together 
with China Universal 
(HK), the “CUAM 
Entities”)
116,700
0.75%
0.05%
0.05%
A connected client of 
Orient Securities
China Asset 
Management Co., 
Ltd. (“China AMC”)
6,600
0.04%
Less than 0.01%
Less than 0.01%
A connected client 
of CITIC Securities 
Brokerage (HK) 
Limited (“CSB”)
China Asset 
Management (Hong 
Kong) Limited 
(“China AMC HK”)
1,600
0.01%
Less than 0.01%
Less than 0.01%
A connected client of 
CSB

<<<PAGE 10>>>
10
Investor
No. of Offer 
Shares allocated
Approximate % 
of Offer Shares(1)
Approximate 
% of the total 
issued H Shares 
immediately 
following 
completion 
of the Global 
Offering(1)(8)
Approximate 
% of the 
total issued 
share capital 
immediately 
following 
completion 
of the Global 
Offering(1)(8)
Relationship
Allotees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocations of further H Shares to certain Cornerstone Investors and/or their close associates(2)(5)
Tencent
164,800
1.06%
0.08%
0.08%
A Cornerstone 
Investor
Taibai Investments 
Pte. Ltd. 
(“Temasek”)
164,800
1.06%
0.08%
0.08%
A Cornerstone 
Investor
Arc Avenue Asset 
Management Pte. 
Ltd.
181,000
1.17%
0.08%
0.08%
A close associate of a 
Cornerstone Investor(6)
BlackRock Asset 
Management North 
Asia Limited
98,800
0.64%
0.05%
0.05%
A close associate of a 
Cornerstone Investor(7)
FIL Investment
98,800
0.64%
0.05%
0.05%
A Cornerstone 
Investor

<<<PAGE 11>>>
11
Notes:
(1) 
Taking into account the full exercise of the Offer Size Adjustment Option and before any exercise of the Over-
allotment Option.
(2) 
For details of (i) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent 
under paragraph 1C(2) of the Placing Guidelines in relation to subscription for Offer Shares by an existing 
Shareholder or close associate of existing Shareholders, (ii) a consent under paragraph 1C(1) of the Placing 
Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations to connected 
clients, and (iii) a consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in 
relation to allocations of Offer Shares to Cornerstone Investors and/or their close associates, please refer to the 
section headed “Others/Additional Information” in this announcement.
(3) 
Each of HongShan Growth VII Holdco, Ltd. and HCEP Management Limited is a close associate of HongShan 
Growth VII Holdco A, Ltd., which is an existing Shareholder.
(4) 
5Y Capital GP Limited is a close associate of 5Y Growth Holding I HK Limited, which is an existing 
Shareholder.
(5) 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details – International Offering – Cornerstone Investors” in this announcement.
(6) 
Arc Avenue Asset Management Pte. Ltd. is a close associate of Temasek, which is a Cornerstone Investor.
(7) 
BlackRock Asset Management North Asia Limited is a close associate of BlackRock, which is a Cornerstone 
Investor.
(8) 
Only taking into account the H Shares allocated to the relevant investors under the Global Offering.

<<<PAGE 12>>>
12
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Approximate 
% of the 
total issued H 
Shares subject 
to lock-up 
undertakings 
upon Listing(1)
Approximate 
% of the total 
issued share 
capital subject 
to lock-up 
undertakings 
upon Listing(1)
Last day subject 
to the lock-up 
undertakings
Mr. Yan(2)(3)(5)
123,661,229
57.72%(4)
57.38%
January 27, 2027(6)
Mr. Zhao(2)(3)(5)
123,661,229
57.72% (4)
57.38%
January 27, 2027(6)
Changsha Xunmang(2)(3)
8,190,235
3.83%
3.80%
January 27, 2027(6)
Changsha Jianmang(2)(3)
1,568,498
0.73%
0.73%
January 27, 2027(6)
Changsha Lingmang(2)(3)
1,076,977
0.50%
0.50%
January 27, 2027(6)
Changsha Zhongmang(2)(3)
8,670,009
4.06%
4.02%
January 27, 2027(6)
Changsha Shizaimang(2)(3)
384,361(4)
-(4)
0.18%
January 27, 2027(6)
Shanghai Bird Nest(2)(5)
45,378,489
21.25%
21.06%
January 27, 2027(6)
Yichun Yikouniao(2)(3)
6,888,341
3.23%
3.20%
January 27, 2027(6)
Notes:
(1) 
Taking into account the full exercise of the Offer Size Adjustment Option and before any exercise of the Over-
allotment Option.
(2) 
Mr. Yan and Mr. Zhao have been acting in concert with respect to the exercising of voting rights in the general 
meetings of the Company since the completion of the Super Ming Acquisition in November 2023. As such, Mr. 
Yan and Mr. Zhao are deemed to be jointly interested in the Shares held by their controlled entities, namely 
Changsha Xunmang, Changsha Jianmang, Changsha Lingmang, Changsha Zhongmang, Changsha Shizaimang, 
Shanghai Bird Nest and Yichun Yikouniao.
(3) 
Mr. Yan is the general partner of Changsha Zhongmang, Changsha Xunmang, Changsha Shizaimang, Changsha 
Jianmang, Changsha Lingmang and Yichun Yikouniao. As such, Mr. Yan is deemed to be interested in the 
Shares of the Company held by each of Changsha Zhongmang, Changsha Xunmang, Changsha Shizaimang, 
Changsha Jianmang, Changsha Lingmang and Yichun Yikouniao.
(4) 
The 384,361 Shares held by Changsha Shizaimang are Domestic Unlisted Shares in issue which will not be 
converted into H Shares upon Listing.
(5) 
As of the Latest Practicable Date, Mr. Zhao is interested in approximately 65.37% equity interests in Shanghai 
Bird Nest. As such, Mr. Zhao is deemed to be interested in the H Shares held by Shanghai Bird Nest.
(6) 
The expiry day of the lock-up period shown in the table above is pursuant to the PRC Company Law. In 
accordance with the relevant Listing Rule and guidance materials, the required lock-up for the First Six-Month 
Period ends on July 27, 2026 and the Second Six-Month Period ends on January 27, 2027.

<<<PAGE 13>>>
13
Pre-IPO Investors (Other than the Controlling Shareholders as defined in the Prospectus)
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Approximate 
% of the 
total issued H 
Shares subject 
to lock-up 
undertakings 
upon  
Listing(1)(5)
Approximate 
% of the total 
issued share 
capital subject 
to lock-up 
undertakings 
upon  
Listing(1)(5)
Last day subject 
to the lock-up 
undertakings
HongShan Hanchen
3,877,397
1.82%
1.80%
January 27, 2027(4)
Gaorong LKZN
5,392,784
2.52%
2.50%
January 27, 2027(4)
Discounter Seed HK
2,507,601
1.17%
1.16%
January 27, 2027(4)
HongShan Yaheng
4,546,154
2.13%
2.11%
January 27, 2027(4)
5Y
3,083,372
1.44%
1.43%
January 27, 2027(4)
BA HM
3,613,511
1.69%
1.68%
January 27, 2027(4)
Shanghai Yihai
1,224,053
0.57%
0.57%
January 27, 2027(4)
Xiamen Black Ant
3,162,393
1.48%
1.47%
January 27, 2027(4)
Haoxiangni Health
Food(2)
3,593,185
1.68%
1.67%
January 27, 2027(4)
Haoxiangni Youran(2)
3,593,185
1.68%
1.67%
January 27, 2027(4)
Jiandan Qiaochu(2)
5,389,782
2.52%
2.50%
January 27, 2027(4)
Hunan Xiaomang(3)
2,288,079
1.07%
1.06%
January 27, 2027(4)
HongShan Growth
5,724,214
2.68%
2.66%
January 27, 2027(4)
Jindong Hong Kong(3)
4,000,000
1.87%
1.86%
January 27, 2027(4)
Subtotal
51,995,710
24.34%
24.13%
Notes:
(1) 
Taking into account the full exercise of the Offer Size Adjustment Option and before any exercise of the Over-
allotment Option.
(2) 
Each of Haoxiangni Youran and Jiandan Qiaochu is wholly owned by Haoxiangni Health Food. As such, 
Haoxiangni Health Food is deemed to be interested in the H Shares of the Company held by Haoxiangni 
Youran and Jiandan Qiaochu.
(3) 
Hunan Xiaomang is wholly owned by Jindong Hong Kong.
(4) 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law.
(5) 
Discrepancies in the above table between the sum of the percentage of Shares held by each investor and the 
percentage of the total Shares held by such investors are due to rounding.

<<<PAGE 14>>>
14
Directors (Other than the Controlling Shareholder as defined in the Prospectus)
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Approximate 
% of the 
total issued H 
Shares subject 
to lock-up 
undertakings 
upon Listing(1)
Approximate 
% of the total 
issued share 
capital subject 
to lock-up 
undertakings 
upon Listing(1)
Last day subject 
to the lock-up 
undertakings
Mr. Wang Yutong
1,536,088(2)
-(2)
0.71%
January 27, 2027(4)
Mr. Wang Ping’an(3)
4,740,096
2.22%
2.20%
January 27, 2027(4)
Mr. Li Wei
6,455,931
3.02%
3.00%
January 27, 2027(4)
Subtotal
12,732,115
5.24%
5.91%
Notes:
(1) 
Taking into account the full exercise of the Offer Size Adjustment Option and before any exercise of the Over-
allotment Option.
(2) 
Mr. Wang Yutong held an aggregate of 1,920,449 Shares, which comprises of (i) 1,536,088 Shares that were 
beneficially owned by him and (ii) 384,361 Shares that he held through Changsha Shizaimang as its limited 
partner holding 79.90% of the partnership interests. The 1,920,449 Shares held by Mr. Wang Yutong are 
Domestic Unlisted Shares in issue which will not be converted into H Shares upon Listing. Please refer to the 
section headed “Lock-up Undertakings – Controlling Shareholders” in this announcement for details.
(3) 
These interests were held through Shanghai Anyicheng, which was in turn held as to approximately 51% by 
Mr. Wang Ping’an.
(4) 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law.
Other Existing Shareholders
Name
Number 
of Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
Approximate 
% of the 
total issued 
H Shares 
subject to 
lock-up 
undertakings 
upon 
Listing(1)(3)
Approximate 
% of the 
total issued 
share capital 
subject to 
lock-up 
undertakings 
upon 
Listing(1)
Last day subject 
to the lock-up 
undertakings
Mr. Liu Wei
5,667,580
2.65%
2.63%
January 27, 2027(2)
Mr. Zhu Lang
5,943,366
2.78%
2.76%
January 27, 2027(2)
Subtotal
11,610,946
5.44%
5.39%

<<<PAGE 15>>>
15
Notes:
(1) 
Taking into account the full exercise of the Offer Size Adjustment Option and before any exercise of the 
Over-allotment Option.
(2) 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law.
(3) 
Discrepancies in the above table between the sum of the percentage of Shares held by each investor and the 
percentage of the total Shares held by such investors are due to rounding.
Cornerstone Investors
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing(1)
Approximate 
% of the 
total issued H 
Shares subject 
to lock-up 
undertakings 
upon  
Listing(2)(3)
Approximate 
% of the total 
issued share 
capital subject 
to lock-up 
undertakings 
upon Listing(2)
Last day subject 
to the lock-up 
undertakings
Tencent
1,482,400
0.69%
0.69%
July 27, 2026(2)
Temasek
1,482,400
0.69%
0.69%
July 27, 2026(2)
BlackRock
1,153,000
0.54%
0.54%
July 27, 2026(2)
FIL Investment
988,200
0.46%
0.46%
July 27, 2026(2)
Bosera International
329,400
0.15%
0.15%
July 27, 2026(2)
E Fund
329,400
0.15%
0.15%
July 27, 2026(2)
Springs Capital (Hong 
Kong)
329,400
0.15%
0.15%
July 27, 2026(2)
Taikang Life
329,400
0.15%
0.15%
July 27, 2026(2)
Subtotal
6,423,600
3.01%
2.98%
Notes:
(1) 
Taking into account the full exercise of the Offer Size Adjustment Option and before any exercise of the 
Over-allotment Option.
(2) 
Each Cornerstone Investor shall not dispose of any of the Offer Shares acquired in the Global Offering at 
any time during the period of six months from (and inclusive of) the Listing Date pursuant to their respective 
Cornerstone Investment Agreement, save for certain limited circumstances, such as transfers to any of its 
wholly-owned subsidiaries who will be bound by the same obligations of the relevant Cornerstone Investor, 
including the lock-up period restriction. For details, please refer to the section headed “Cornerstone Investors 
– Restrictions on the Cornerstone Investors” of the Prospectus.
(3) 
Discrepancies in the above table between the sum of the percentage of Shares held by each investor and the 
percentage of the total Shares held by such investors are due to rounding.

<<<PAGE 16>>>
16
PLACEE CONCENTRATION ANALYSIS
Placees
Number of H 
Shares allotted
Allotment 
as % of 
International 
Offering 
(taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-allotment 
Option)
Allotment 
as % of 
International 
Offering 
(taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is 
exercised in 
full)
Allotment as 
% of total 
Offer Shares 
(taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is 
exercised in 
full)
Number of
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing 
(taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is 
exercised in 
full)
Top 1
1,647,200
11.68%
10.03%
10.62%
9.23%
1,647,200
0.76%
0.76%
Top 5
6,661,800
47.24%
40.55%
42.95%
37.35%
6,661,800
3.09%
3.06%
Top 10
9,577,400
67.92%
58.30%
61.75%
53.69%
15,301,614
7.10%
7.02%
Top 25
13,341,300
94.61%
81.21%
86.01%
74.79%
19,065,514
8.85%
8.75%
Notes
* 
Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 17>>>
17
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(taking into 
account the 
full exercise 
of the 
Offer Size 
Adjustment 
Option and 
assuming no 
exercise of 
the Over-
allotment 
Option)
Allotment 
as % of 
International 
Offering 
(taking into 
account the 
full exercise 
of the 
Offer Size 
Adjustment 
Option and 
assuming 
the Over-
allotment 
Option is 
exercised in 
full)
Allotment as 
% of total 
Offer Shares 
(taking into 
account the 
full exercise 
of the 
Offer Size 
Adjustment 
Option and 
assuming no 
exercise of 
the Over-
allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(taking into 
account the 
full exercise 
of the 
Offer Size 
Adjustment 
Option and 
assuming 
the Over-
allotment 
Option is 
exercised in 
full)
Number of H 
Shares held 
upon Listing
% of total 
issued H 
Shares capital 
upon Listing 
(taking into 
account the 
full exercise 
of the 
Offer Size 
Adjustment 
Option and 
assuming no 
exercise of 
the Over-
allotment 
Option)
% of total 
issued H 
Shares capital 
upon Listing 
(taking into 
account the 
full exercise 
of the 
Offer Size 
Adjustment 
Option and 
assuming 
the Over-
allotment 
Option is 
exercised in 
full)
Number of 
Shares held 
upon Listing
Top 1
0
0.00%
0.00%
0.00%
0.00%
123,276,868
57.72%
57.09%
123,661,229
Top 5
329,500
2.34%
2.01%
2.12%
1.85%
147,397,459
69.01%
68.27%
147,781,820
Top 10
395,400
2.80%
2.41%
2.55%
2.22%
171,532,175
80.31%
79.44%
171,916,536
Top 25
8,177,300
57.99%
49.78%
52.72%
45.84%
206,256,851
96.57%
95.53%
206,641,212
Notes
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 18>>>
18
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(taking into 
account the 
full exercise 
of the 
Offer Size 
Adjustment 
Option and 
assuming no 
exercise of 
the Over-
allotment 
Option)
Allotment 
as % of 
International 
Offering 
(taking into 
account the 
full exercise 
of the 
Offer Size 
Adjustment 
Option and 
assuming 
the Over-
allotment 
Option is 
exercised in 
full)
Allotment as 
% of total 
Offer Shares 
(taking into 
account the 
full exercise 
of the 
Offer Size 
Adjustment 
Option and 
assuming no 
exercise of 
the Over-
allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(taking into 
account the 
full exercise 
of the 
Offer Size 
Adjustment 
Option and 
assuming 
the Over-
allotment 
Option is 
exercised in 
full)
Number of H 
Shares held 
upon Listing
Number of 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing 
(taking into 
account the 
full exercise 
of the 
Offer Size 
Adjustment 
Option and 
assuming no 
exercise of 
the Over-
allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(taking into 
account the 
full exercise 
of the 
Offer Size 
Adjustment 
Option and 
assuming 
the Over-
allotment 
Option is 
exercised in 
full)
Top 1
0
0.00%
0.00%
0.00%
0.00%
123,276,868
123,661,229
57.38%
56.77%
Top 5
329,500
2.34%
2.01%
2.12%
1.85%
147,397,459
147,781,820
68.57%
67.84%
Top 10
395,400
2.80%
2.41%
2.55%
2.22%
171,532,175
171,916,536
79.77%
78.92%
Top 25
7,222,000
51.22%
43.96%
46.56%
40.49%
205,301,551
207,222,000
96.15%
95.13%
Notes
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 19>>>
19
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 229,245 valid 
applications made by the public will be conditionally allocated on the basis set out below:
POOL A
NO. OF SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL NO. OF 
SHARES APPLIED 
FOR
100
61,617
1,849 out of 61,617 to receive 100 H Shares
3.00%
200
25,446
895 out of 25,446 to receive 100 H Shares
1.76%
300
8,190
289 out of 8,190 to receive 100 H Shares
1.18%
400
9,550
337 out of 9,550 to receive 100 H Shares
0.88%
500
6,307
223 out of 6,307 to receive 100 H Shares
0.71%
600
3,198
114 out of 3,198 to receive 100 H Shares
0.59%
700
2,738
98 out of 2,738 to receive 100 H Shares
0.51%
800
3,047
110 out of 3,047 to receive 100 H Shares
0.45%
900
2,187
79 out of 2,187 to receive 100 H Shares
0.40%
1,000
12,527
453 out of 12,527 to receive 100 H Shares
0.36%
1,500
6,397
232 out of 6,397 to receive 100 H Shares
0.24%
2,000
5,902
215 out of 5,902 to receive 100 H Shares
0.18%
2,500
4,344
159 out of 4,344 to receive 100 H Shares
0.15%
3,000
3,634
134 out of 3,634 to receive 100 H Shares
0.12%
3,500
2,774
103 out of 2,774 to receive 100 H Shares
0.11%
4,000
3,140
120 out of 3,140 to receive 100 H Shares
0.10%
4,500
2,428
93 out of 2,428 to receive 100 H Shares
0.09%
5,000
4,110
158 out of 4,110 to receive 100 H Shares
0.08%
6,000
3,176
124 out of 3,176 to receive 100 H Shares
0.07%
7,000
2,619
103 out of 2,619 to receive 100 H Shares
0.06%
8,000
2,485
98 out of 2,485 to receive 100 H Shares
0.05%
9,000
2,022
80 out of 2,022 to receive 100 H Shares
0.04%
10,000
12,939
514 out of 12,939 to receive 100 H Shares
0.04%
20,000
11,677
471 out of 11,677 to receive 100 H Shares
0.02%
Total
202,454
Total number of Pool A successful applicants: 7,051

<<<PAGE 20>>>
20
POOL B
NO. OF SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED  
OF THE TOTAL  
NO. OF SHARES  
APPLIED FOR
30,000
9,749
2,545 out of 9,749 to receive 100 H Shares
0.09%
40,000
3,518
919 out of 3,518 to receive 100 H Shares
0.07%
50,000
7,067
1,847 out of 7,067 to receive 100 H Shares
0.05%
100,000
2,972
777 out of 2,972 to receive 100 H Shares
0.03%
150,000
1,214
318 out of 1,214 to receive 100 H Shares
0.02%
200,000
694
182 out of 694 to receive 100 H Shares
0.01%
250,000
338
89 out of 338 to receive 100 H Shares
0.01%
300,000
281
74 out of 281 to receive 100 H Shares
0.01%
350,000
173
46 out of 173 to receive 100 H Shares
0.01%
400,000
117
32 out of 117 to receive 100 H Shares
0.01%
450,000
81
23 out of 81 to receive 100 H Shares
0.01%
500,000
76
22 out of 76 to receive 100 H Shares
0.01%
550,000
42
13 out of 42 to receive 100 H Shares
0.01%
600,000
52
17 out of 52 to receive 100 H Shares
0.01%
650,000
30
10 out of 30 to receive 100 H Shares
0.01%
705,100
387
137 out of 387 to receive 100 H Shares
0.01%
Total
26,791
Total number of Pool B successful applicants: 7,051
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect 
of which consents have been obtained, the Company has complied with the Listing Rules and 
guidance materials in relation to the placing, allotment and listing of the Company’s Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.

<<<PAGE 21>>>
21
OTHERS/ADDITIONAL INFORMATION
Offer Size Adjustment Option
The Offer Size Adjustment Option has been fully exercised by the Overall Coordinators, pursuant 
to which the Company is issuing and allotting 1,410,100 additional Offer Shares, representing 
approximately 10% of the total number of Offer Shares initially available under the Global 
Offering, at the final Offer Price. All of the additional Offer Shares that would be allotted and 
issued by the Company pursuant to the full exercise of the Offer Size Adjustment Option will 
be allocated to the International Offering. Accordingly, the total number of Offer Shares finally 
available under the Global Offering (taking into account the full exercise of the Offer Size 
Adjustment Option and before any exercise of the Over-allotment Option) that would be allotted 
and issued by the Company is 15,511,200 Offer Shares and the total issued share capital of the 
Company upon Listing (taking into account the full exercise of the Offer Size Adjustment Option 
and before any exercise of the Over-allotment Option) will be 215,511,200 Shares.
Placing to existing Shareholder or close associate of existing Shareholders with a waiver 
from the strict compliance with Rule 10.04 of the Listing Rules and a prior consent under 
paragraph 1C(2) of the Placing Guidelines
The Company has applied to the Stock Exchange, and the Stock Exchange has granted, a waiver 
from the strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of the Placing Guidelines to permit the Company to allocate such Offer Shares in the 
International Offering to any existing Shareholder or close associate of existing Shareholders as 
listed above. The allocation of Offer Shares to such existing Shareholder or close associate of 
existing Shareholders is in compliance with all the conditions under the waiver/consent granted by 
the Stock Exchange.
For details of the allocations of Offer Shares to the existing Shareholders, please refer to the 
section headed “Allotment Results Details – International Offering – Allotees with Waivers/
Consents Obtained” in this announcement.

<<<PAGE 22>>>
22
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their connected distributors pursuant to the 
Placing Guidelines.
The Company has applied to the Stock Exchange, and the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing 
Guidelines to permit the Company to allocate such Offer Shares in the International Offering to the connected clients listed below. The 
allocation of Offer Shares to such connected clients is in compliance with all the conditions under the consent granted by the Stock 
Exchange. Details of the placement to connected clients are set out below:
Connected 
Distributor
Connected 
Client
Relationship
Whether the 
connected 
clients will hold 
the beneficial 
interests of the 
Offer Shares 
on a non-
discretionary 
basis or 
discretionary 
basis for 
independent 
third parties
No. of Offer 
Shares 
allocated
Approximate 
% of Offer 
Shares(1)
Approximate 
% of the 
total issued 
H Shares 
immediately 
following 
completion of 
the
Global 
Offering(1)
Approximate 
% of the 
total issued 
shares capital 
immediately 
following 
completion 
of the Global 
Offering(1)
HTFH
HTCI
HTCI is a 
member of the 
same group of 
companies as 
HTFH(2)(3)
Non-
discretionary 
basis
1,410,000
9.09%
0.66%
0.65%
HTFH
China Southern
China Southern 
is a member of 
the same group 
of HTFH(4)
Discretionary 
basis
1,600
0.01%
Less than 0.01% Less than 0.01%

<<<PAGE 23>>>
23
Connected 
Distributor
Connected 
Client
Relationship
Whether the 
connected 
clients will hold 
the beneficial 
interests of the 
Offer Shares 
on a non-
discretionary 
basis or 
discretionary 
basis for 
independent 
third parties
No. of Offer 
Shares 
allocated
Approximate 
% of Offer 
Shares(1)
Approximate 
% of the 
total issued 
H Shares 
immediately 
following 
completion of 
the
Global 
Offering(1)
Approximate 
% of the 
total issued 
shares capital 
immediately 
following 
completion 
of the Global 
Offering(1)
HTFH
CSOP AM
See Note (5)
Discretionary 
basis
400
Less than 0.01% Less than 0.01% Less than 0.01%
Deutsche Bank
Harvest Global
Harvest 
Global is a 
wholly owned 
subsidiary 
of Harvest 
Financial Group 
Limited, which 
in turn is wholly 
owned by 
Harvest Fund 
Management 
Co., Ltd. (6)
Discretionary 
basis
164,800
1.06%
0.08%
0.08%
Haitong
Haitong AM
Haitong AM is 
a member of the 
same group of 
Haitong(7)
Discretionary 
basis
100
Less than 0.01% Less than 0.01% Less than 0.01%
Haitong
Fullgoal AM
See Note (8)
Discretionary 
basis
89,200
0.58%
0.04%
0.04%

<<<PAGE 24>>>
24
Connected 
Distributor
Connected 
Client
Relationship
Whether the 
connected 
clients will hold 
the beneficial 
interests of the 
Offer Shares 
on a non-
discretionary 
basis or 
discretionary 
basis for 
independent 
third parties
No. of Offer 
Shares 
allocated
Approximate 
% of Offer 
Shares(1)
Approximate 
% of the 
total issued 
H Shares 
immediately 
following 
completion of 
the
Global 
Offering(1)
Approximate 
% of the 
total issued 
shares capital 
immediately 
following 
completion 
of the Global 
Offering(1)
Haitong
Fullgoal Funds
See Note (8)
Discretionary 
basis
75,600
0.49%
0.04%
0.04%
Orient 
Securities
China Universal 
(HK)
See Note (9)
Discretionary 
basis
49,700
0.32%
0.02%
0.02%
Orient 
Securities
CUAM Entities
See Note (9)
Discretionary 
basis
116,700
0.75%
0.05%
0.05%
CSB
China AMC
See Note (10)
Discretionary 
basis
6,600
0.04%
Less than 0.01% Less than 0.01%
CSB
China AMC HK
See Note (11)
Discretionary 
basis
1,600
0.01%
Less than 0.01% Less than 0.01%
Notes:
(1) 
Taking into account the full exercise of the Offer Size Adjustment Option and before any exercise of the Over-allotment Option.
(2) 
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public offerings (“IPOs”) in Hong Kong. However, PRC 
investors are permitted to invest in products issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. In 
connection with such products, the licensed domestic securities firms, through their Hong Kong affiliates, may participate in Hong Kong IPOs either as placees 
or cornerstone investors (the “Cross-border Derivatives Trading Regime”).

<<<PAGE 25>>>
25
Huatai Securities Co., Ltd. (“Huatai Securities”), the shares of which are listed on both the Shanghai Stock Exchange (stock code: 601688) and the Stock 
Exchange (stock code: 6886), is one of the domestic securities firms licensed to undertake cross-border derivatives trading activities. Huatai Securities entered 
into an ISDA agreement (the “ISDA Agreement”) with its indirectly wholly-owned subsidiary, HTCI, to set out the principal terms of any future total return 
swap between Huatai Securities and HTCI.
HTFH is one of the Joint Sponsors and the Overall Coordinators and Underwriters in connection with the Global Offering. Pursuant to an ISDA agreement 
entered into between Huatai Securities and HTCI, HTCI, which intends to participate in the Global Offering as a placee, will hold the beneficial interest of the 
Offer Shares on a non-discretionary basis as the single underlying holding under a back-to-back total return swap (“Huatai Back-to-back TRS”) to be entered 
by HTCI in connection with a Client TRS (as defined below) placed by and fully funded (i.e., with no financing provided by HTCI) by Huatai Onshore Ultimate 
Clients (as defined below), by which, HTCI will, subject to customary fees and commissions, pass the full economic exposure of the Offer Shares ultimately 
to the Huatai Onshore Ultimate Clients, which in effect, HTCI will hold the beneficial interest of the Offer Shares on behalf of the Huatai Onshore Ultimate 
Clients.
HTCI and HTFH are both indirectly wholly-owned subsidiaries of Huatai Securities. Accordingly, HTCI is considered as a “connected client” of HTFH pursuant 
to paragraph 1B(7) of the Placing Guidelines.
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the “Huatai Onshore Ultimate Clients”) cannot directly subscribe for the 
Offer Shares but may invest in derivative products issued by domestic securities firms licenced to undertake cross-border derivatives trading activities, such 
as Huatai Securities, with the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, the Huatai Onshore Ultimate Clients, 
through their investment managers, will place a total return swap order (the “Client TRS”) with Huatai Securities in connection with the Global Offering and 
Huatai Securities will place a Huatai Back-to-back TRS order to HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the Huatai 
Backto-back TRS, HTCI participates in the Global Offering and subscribes the Offer Shares through placing order with HTFH during the International Offering.
To the best of HTCI’s knowledge and after making all reasonable enquiries, each of the Huatai Onshore Ultimate Clients is an independent third party of (i) the 
Company, the connected person and/or their respective associates thereof, and (ii) HTCI, HTFH and the companies which are members of the same group of 
HTCI.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Huatai Back-to-back TRS in connection with the Client TRS order placed by the 
Huatai Onshore Ultimate Clients. Pursuant to the terms of the contracts of the Huatai Back-to-back TRS and the Client TRS, during the tenor of the Huatai 
Back-to-back TRS and the Client TRS, subject to customary fees and commissions, all economic returns of the Offer Shares will be ultimately passed to the 
Huatai Onshore Ultimate Clients through the Huatai Back-to-back TRS and the Client TRS and all economic loss shall be ultimately borne by the Huatai 
Onshore Ultimate Clients. HTCI will not take any economic return or bear any economic loss in relation to the Offer Shares.
Investment in the Huatai Back-to-back TRS and the Client TRS is similar to the investment in a qualified domestic institutional investor fund (“QDII”) in the 
way that the Huatai Onshore Ultimate Clients would reap all the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through 
the exchange rate exposure on both the notional value of the investment and the profit and loss of the investment. In contrast, the profit and loss of the Huatai 
Back-to-back TRS and the Client TRS factor into account the fluctuation in RMB exchange rate upon termination of the Client TRS by converting the profit 
and loss using the current exchange rate at the time of termination. As such, the Huatai Onshore Ultimate Clients would bear the exchange rate exposure of the 
profit and loss on settlement date.

<<<PAGE 26>>>
26
The Huatai Onshore Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time from the issue date of the Client TRS 
which should be on or after the date on which the Offer Shares are listed on the Stock Exchange at their own discretions. Upon the termination upon maturity 
or early termination of the Client TRS by the Huatai Onshore Ultimate Clients, HTCI will dispose the Offer Shares on the secondary market and the Huatai 
Onshore Ultimate Clients will receive a final settlement amount in cash in accordance with the terms and conditions of the Huatai Back-to-back TRS and the 
Client TRS which should have taken into account all the economic returns or economic loss in relation to the Offer Shares. If upon the maturity of the Client 
TRS, the Huatai Onshore Ultimate Clients intend to extend the investment period, subject to further agreement between Huatai Securities and the relevant 
Huatai Onshore Ultimate Clients, the term of the Client TRS could be extended by way of a new issuance or a tenor extension. Accordingly, Huatai Securities 
will extend the term of the Huatai Back-to-back TRS by way of a new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through the economic exposure to the Huatai 
Onshore Ultimate Clients, each being an onshore client who places a Client TRS order with Huatai Securities in connection with the Global Offering. HTCI will 
not exercise the voting right of the Offer Shares during the tenor of the Huatai Back-to-back TRS.
During the life of the Client TRS and Huatai Back-to-back TRS, HTCI may continue to hold the Offer Shares in its custodian account, or to hold some or all 
of the Offer Shares in a prime brokerage account for stock borrowing purposes, HTCI will lend out its holding of underlying Offer Shares in the form of stock 
borrowing loans consistent with market practice to lower its finance costs, provided that HTCI has the ability to call back the Offer Shares on loan at any time 
in order to satisfy its obligations under the Huatai Back-to-back TRS to ensure the economic interests are ultimately passed to the Huatai Onshore Ultimate 
Clients.
Huatai Onshore Ultimate Clients
Ultimate Beneficial 
Owners (“UBO”)
Remarks
Zhuhai Hunkin Private Fund Management Partnership (Limited Partnership) - Jinyueyang Private 
Securities Investment Fund* (珠海渾瑾私募基金管理合夥企業(有限合夥)-瑾岳陽私募證券投資基金)
N/A
N/A
Yucheng Private Fund Management (Hainan) Partnership (Limited Partnership) - Yucheng Xiangjiang 
Qiming Private Securities Investment Fund* (宇誠私募基金管理(海南)合夥企業(有限合夥)-宇誠香江啟
明私募證券投資基金)
Hong Yan (洪燕)
Zhang Weihua (張衛
華)
UBO with over 30% 
interest
Beijing Hengde Times Private Fund Management Co., Ltd. - Hengde Yuanzheng Tianli No. 3 Private 
Securities Investment Fund* (北京恒德時代私募基金管理有限公司－恒德遠征添利 3 號私募證券投資
基金)
N/A
N/A
Shanghai Baoyin Private Fund Management Co., Ltd.* (上海保銀私募基金管理有限公司)
N/A
N/A
Shanghai Qinchen Private Fund Management Partnership (Limited Partnership) - Qinchen Jiaxuan Senyu 
No. 1 Private Securities Investment Fund* (上海勤辰私募基金管理合夥企業(有限合夥)-勤辰嘉選森裕 
1 號私募證券投資基金)
N/A
N/A

<<<PAGE 27>>>
27
Huatai Onshore Ultimate Clients
Ultimate Beneficial 
Owners (“UBO”)
Remarks
Shanghai Qinchen Private Fund Management Partnership (Limited Partnership) - Qinchen Jinsuan Senyu 
No. 1 Private Securities Investment Fund* (上海勤辰私募基金管理合夥企業(有限合夥)-勤辰金選森裕 
1 號私募證券投資基金)
N/A
N/A
Shanghai Qinchen Private Fund Management Partnership (Limited Partnership) - Qinchen Senyu No. 1 
Private Securities Investment Fund* (上海勤辰私募基金管理合夥企業(有限合夥)-勤辰森裕 1 號私募證
券投資基金)
N/A
N/A
Shanghai Qinchen Private Fund Management Partnership (Limited Partnership) - Qinchen Senyu No. 2 
Private Securities Investment Fund* (上海勤辰私募基金管理合夥企業(有限合夥)-勤辰森裕 2 號私募證
券投資基金)
N/A
N/A
Shanghai Qinchen Private Fund Management Partnership (Limited Partnership) - Qinchen Senyu No. 3 
Private Securities Investment Fund* (上海勤辰私募基金管理合夥企業(有限合夥)-勤辰森裕 3 號私募證
券投資基金)
N/A
N/A
Shanghai Qinchen Private Fund Management Partnership (Limited Partnership) - Qinchen Chuangying 
Growth No. 1 Private Securities Investment Fund* (上海勤辰私募基金管理合夥企業(有限合夥)-勤辰創
贏成長 1 號私募證券投資基金)
N/A
N/A
Shanghai Qinchen Private Fund Management Partnership (Limited Partnership) - Qinchen Chuangying 
Growth No. 2 Private Securities Investment Fund* (上海勤辰私募基金管理合夥企業(有限合夥)-勤辰創
贏成長 2 號私募證券投資基金)
N/A
N/A
Shanghai Qinchen Private Fund Management Partnership (Limited Partnership) - Qinchen Jiaxuan 
Chuangying Growth No. 1 Private Securities Investment Fund* (上海勤辰私募基金管理合夥企業(有限
合夥)-勤辰嘉選創贏成長 1 號私募證券投資基金)
N/A
N/A
Shanghai Qinchen Private Fund Management Partnership (Limited Partnership) - Qinchen Jinsuan 
Chuangying Growth No. 1 Private Securities Investment Fund* (上海勤辰私募基金管理合夥企業(有限
合夥)-勤辰金選創贏成長 1 號私募證券投資基金)
N/A
N/A
Pingyang Ruihe Investment Management Co., Ltd. - Ruihe Xinjian Private Securities Investment Fund* 
(平陽瑞和投資管理有限公司－瑞和信見私募證券投資基金)
N/A
N/A
Shanghai Mingmeng Investment Management Co., Ltd. - Mingmeng Multi-Strategy Hedge No. 1 Fund* 
(上海明汯投資管理有限公司－明汯多策略對沖 1 號基金)
N/A
N/A

<<<PAGE 28>>>
28
Huatai Onshore Ultimate Clients
Ultimate Beneficial 
Owners (“UBO”)
Remarks
Shanghai Weining Private Fund Management Co., Ltd. - Weining Qihang No. 1 Private Securities 
Investment Fund* (上海衛寧私募基金管理有限公司－衛甯啟航 1 號私募證券投資基金)
Liu Yutao (劉育濤)
UBO with over 30% 
interest
Shanghai Weining Private Fund Management Co., Ltd. - Weining Focus Private Securities Investment 
Fund* (上海衛寧私募基金管理有限公司－衛寧聚焦私募證券投資基金)
Lin Ran (林然)
UBO with over 30% 
interest
Shanghai Hesheng Asset Management Co., Ltd. - Hesheng Qijia Hybrid No. 1 Private Securities 
Investment Fund* (上海合晟資產管理股份有限公司－合晟齊嘉混合 1 號私募證券投資基金)
N/A
N/A
Shanghai Ruijun Asset Management Co., Ltd. - Ruijun No. 6 Private Securities Investment Fund* (上海
睿郡資產管理有限公司－睿郡 6 號私募證券投資基金)
N/A
N/A
Shanghai Ruijun Asset Management Co., Ltd. - Ruijun No. 7 Private Securities Investment Fund* (上海
睿郡資產管理有限公司－睿郡 7 號私募證券投資基金)
N/A
N/A
Shanghai Ruijun Asset Management Co., Ltd. - Ruijun No. 11 Private Securities Investment Fund* (上海
睿郡資產管理有限公司－睿郡 11 號私募證券投資基金)
N/A
N/A
Shanghai Ruijun Asset Management Co., Ltd. - Ruijun No. 18 Private Securities Investment Fund* (上海
睿郡資產管理有限公司－睿郡 18 號私募證券投資基金)
N/A
N/A
Shanghai Ruijun Asset Management Co., Ltd. - Ruijun Exclusive No. 29 Private Securities Investment 
Fund* (上海睿郡資產管理有限公司－睿郡專享 29 號私募證券投資基金)
N/A
N/A
Shanghai Ruijun Asset Management Co., Ltd. - Ruijun Shanghai-Hong Kong-Shenzhen Private Securities 
Investment Fund* (上海睿郡資產管理有限公司－睿郡滬港深私募證券投資基金)
N/A
N/A
Shanghai Ruijun Asset Management Co., Ltd. - Ruijun Huixiang No. 1 Private Securities Investment 
Fund* (上海睿郡資產管理有限公司－睿郡慧享 1 號私募證券投資基金)
N/A
N/A

<<<PAGE 29>>>
29
Huatai Onshore Ultimate Clients
Ultimate Beneficial 
Owners (“UBO”)
Remarks
Shanghai Ruijun Asset Management Co., Ltd. - Ruijun Zhiyuan No. 1 Private Securities Investment 
Fund* (上海睿郡資產管理有限公司－睿郡致遠 1 號私募證券投資基金)
N/A
N/A
Shanghai Ruijun Asset Management Co., Ltd. - Ruijun Ruixiang Private Securities Investment Fund* (上
海睿郡資產管理有限公司－睿郡睿享私募證券投資基金)
N/A
N/A
Shanghai Ruijun Asset Management Co., Ltd. - Ruijun Zhongxiang No. 6 Private Securities Investment 
Fund* (上海睿郡資產管理有限公司－睿郡眾享 6 號私募證券投資基金)
N/A
N/A
Shanghai Ruijun Asset Management Co., Ltd. - Ruijun Jinsuan Flexible Strategy No. 1 Private Securities 
Investment Fund* (上海睿郡資產管理有限公司－睿郡金選靈活策略 1 號私募證券投資基金)
N/A
N/A
Shanghai Ruijun Asset Management Co., Ltd. - Ruijun Yuexiang Private Securities Investment Fund* (上
海睿郡資產管理有限公司－睿郡悅享私募證券投資基金)
N/A
N/A
Shanghai Ruijun Asset Management Co., Ltd. - Ruijun Jiejie Gao 22 Private Securities Investment Fund* 
(上海睿郡資產管理有限公司－睿郡節節高 22 號私募證券投資基金)
N/A
N/A
Shanghai Ruijun Asset Management Co., Ltd. - Ruijun Xinxiang Private Securities Investment Fund* (上
海睿郡資產管理有限公司－睿郡昕享私募證券投資基金)
N/A
N/A
Shenzhen Wangzheng Asset Management Co., Ltd. - Wangzheng Win-Win 17 Private Securities 
Investment Fund* (深圳望正資產管理有限公司－望正共贏 17 號私募證券投資基金)
Qu Qin (瞿琴)
UBO with over 30% 
interest
Yuanxin (Zhuhai) Private Fund Management Co., Ltd. - Yuanxin China Value Return Select Private 
Securities Investment Fund* (遠信(珠海)私募基金管理有限公司－遠信中國價值回報精選私募證券投
資基金)
Xie Zhendong (謝振東)
UBO with over 30% 
interest
Yuanxin (Zhuhai) Private Fund Management Co., Ltd. - CITIC Capital China Value Return Private 
Securities Investment Fund* (遠信(珠海)私募基金管理有限公司－中信資本中國價值回報私募證券投
資基金)
Xu Jiangnan (許江南)
UBO with over 30% 
interest

<<<PAGE 30>>>
30
Huatai Onshore Ultimate Clients
Ultimate Beneficial 
Owners (“UBO”)
Remarks
Yuanxin (Zhuhai) Private Fund Management Co., Ltd. - CITIC Capital China Quality Enterprises 
Contrarian Strategy Private Securities Investment Fund* (遠信(珠海)私募基金管理有限公司－中信資本
中國優質企業逆向策略私募證券投資基金)
N/A
N/A
Jinxiu Zhonghe (Tianjin) Investment Management Co., Ltd. - Zhonghe Capital Cultivation No. 8 Private 
Securities Investment Fund* (錦繡中和(天津)投資管理有限公司－中和資本耕耘 8 號私募證券投資基
金)
Zhang Jingting (張敬
庭)
UBO with over 30% 
interest
Beijing Dongfang Engine Investment Management Co., Ltd. - Engine Capital China Opportunity High-
Yield Bond Private Fund No. 1* (北京東方引擎投資管理有限公司－引擎資本中國機會高收益債券私
募基金 1 號)
N/A
N/A
Beijing Dongfang Engine Investment Management Co., Ltd. - Dongfang Engine Evergreen No. 2 Private 
Securities Investment Fund* (北京東方引擎投資管理有限公司－東方引擎基業長青 2 號私募證券投資
基金)
Ji Zongming (季宗明)
UBO with over 30% 
interest
Shanghai Yongjin Investment Management Co., Ltd. - Yongjin Yongxin Multi-Strategy No. 11 Private 
Securities Investment Fund* (上海湧津投資管理有限公司－湧津湧鑫多策略 11 號私募證券投資基金)
Xie Xiaoyong (謝小勇)
UBO with over 30% 
interest
Hainan Bingzuo Guanfu Private Fund Management Partnership (Limited Partnership) acting as manager 
for Bingzuo Guanfu Baopu No. 1 Private Securities Investment Fund* (海南並作觀複私募基金管理合夥
企業(有限公司)作為管理人代並作觀複抱樸 1 號私募證券投資基金)
N/A
N/A
Shanghai Jinglin Asset Management Co., Ltd.* (上海景林資產管理有限公司)
N/A
N/A
Shanghai Gaoyi Asset Management Partnership (Limited Partnership)* (上海高毅資產管理合夥企業(有
限合夥))
N/A
N/A

<<<PAGE 31>>>
31
(3) 
The offshore investors (the “Huatai Offshore Ultimate Clients”), through its investment manager, will place the Client TRS with HTCI in connection with the 
Global Offering. In order to hedge its exposure under the Client TRS, HTCI participates in the Global Offering and subscribes the H Shares through placing 
order with HTFH during the International Offering.
To the best of our knowledge and after making all reasonable enquiries, the Huatai Offshore Ultimate Clients are an independent third party of (i) the Company, 
the connected person or the associates thereof, and (ii) HTCI, HTFH and the companies which are members of the same group of HTCI.
The purpose of HTCI to subscribe for the H Shares is for hedging the Client TRS order placed by the Huatai Offshore Ultimate Clients. Pursuant to the terms 
of the Client TRS, during the tenor of the Client TRS, subject to customary fees and commissions, all economic returns of the H Shares will be passed to the 
Huatai Offshore Ultimate Clients through the Client TRS and all economic loss shall be borne by the Huatai Offshore Ultimate Clients. HTCI will not take any 
economic return or bear any economic loss in relation to the H Shares.
The Huatai Offshore Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time from the issue date of the Client TRS 
which should be on or after the date on which the H Shares are listed on the Stock Exchange at their own discretion. Upon the termination upon maturity or 
early termination of the Client TRS by the Huatai Offshore Ultimate Clients, HTCI will dispose the H Shares on the secondary market and the Huatai Offshore 
Ultimate Clients will receive a final settlement amount of the Client TRS in cash in accordance with the terms and conditions of the Client TRS which should 
have taken into account all the economic returns or economic loss in relation to the H Shares. If upon the maturity of the Client TRS, the Huatai Offshore 
Ultimate Clients intends to extend the investment period, subject to further agreement between HTCI and the relevant Huatai Offshore Ultimate Client, the term 
of the Client TRS could be extended by way of a new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the H Shares by itself, and pass through the economic exposure to the Huatai Offshore 
Ultimate Clients, being a client who places a Client TRS order with HTCI in connection with the Global Offering. HTCI will not exercise the voting right of the 
H Shares during the tenor of the Client TRS.
During the life of the Client TRS, HTCI may continue to hold the H Shares in its custodian account, or to hold some or all of the H Shares in a prime brokerage 
account for stock borrowing purposes, where HTCI will lend out its holding of underlying H Shares in the form of stock borrowing loans consistent with market 
practice to lower its finance costs, provided that HTCI has the ability to call back the H Shares on loan at any time in order to satisfy its obligations under the 
Client TRS to ensure the economic interests are ultimately passed to the Huatai Offshore Ultimate Clients.
Huatai Offshore Ultimate Clients
UBO
Remarks
Baichuan Investment SPC – Baichuan Growth Fund SP
Sun Jian
UBO with over 30% interest
(4) 
China Southern, a qualified domestic institutional investor as approved by the relevant PRC authority to conduct asset management business, will hold the Offer 
Shares as the independent agent and discretionary manager of certain QDII funds.

<<<PAGE 32>>>
32
(5) 
CSOP AM is the discretionary investment manager of China New Balance Opportunity Fund (the “CSOP AM Ultimate Client”) whose investors are, to the 
best of CSOP AM’s knowledge, independent third parties of the CSOP AM, HTFH and the companies which are members of the same group of HTFH. The 
only ultimate beneficial owner holding 30% or more interest of the CSOP AM Ultimate Client is CMB Wing Lung (Nominee) Ltd. CSOP AM makes investment 
decisions for the CSOP AM Ultimate Client. HTFH indirectly holds 21.609% shares of CSOP AM. CSOP AM is therefore considered as a connected client of 
HTFH pursuant to paragraph 1B(7) of the Placing Guidelines.
(6) 
Harvest Fund Management Co., Ltd. is 30% owned by DWS Investments Singapore Limited, a wholly-owned subsidiary of Deutsche Bank.
(7) 
Haitong AM will hold the Offer Shares in its capacity as the discretionary investment manager managing assets on behalf of its underlying clients, each of 
which is an independent third party of Haitong AM, Haitong and the companies which are members of the same group of Haitong.
(8) 
Fullgoal AM and Fullgoal HK are members of the same group of companies as Haitong. Each of Fullgoal AM and Fullgoal HK will subscribe for and hold 
Offer Shares under the International Offering in accounts in its capacity as the discretionary fund manager managing assets on behalf of its ultimate clients (the 
“Fullgoals Underlying Clients”).
The Fullgoal Underlying Clients include (i) ICBC Fullgoal China Small & Mid Cap (HK listed) Equity Fund, (ii) ICBC Fullgoal Global Technology & Internet 
Fund, (iii) Cmb-Fullgoal Blue Chip Selected Equity Fund (QDII), (iv) Fullgoal Dividend Selected Hybrid Fund, (v) Fullgoal China Opportunities Fund, (vi) 
Fullgoal China Growth Select Fund and (vii) The University of Hong Kong — Hong Kong and China Equity Fund. As confirmed by Fullgoal Funds, none 
of Fullgoal Underlying Clients holds an interest of 30% or more. To the best knowledge of Fullgoal Fund after due enquiry, each of the Fullgoal Underlying 
Clients is an independent third party of the Company, its subsidiaries, Fullgoal Funds, Haitong and the companies which are members of the same group of 
Haitong.
(9) 
China Universal (HK) is a wholly owned subsidiary of CUAM, which is owned by Orient Securities Co., Ltd., the group company of Orient Securities as to 
35.412%. As such, each of the CUAM Entities is a member of the same group of companies as Orient Securities.
The subscription will be made by each of the CUAM Entities in its capacity as the investment manager on a discretionary basis for and on behalf of its 
underlying clients. Each of the CUAM Entities has confirmed that, to the best of their knowledge and after making all reasonable enquiries, each of its 
underlying clients and its ultimate beneficial owners (if applicable) listed above is an independent third party of the CUAM Entities, and the companies which 
are members of the same group of companies as Orient Securities.
(10) 
China AMC is a member of the same group of CSB. China AMC proposes to subscribe for and hold Offer Shares under the International Offering in accounts 
in its capacity as the discretionary fund manager managing assets on behalf of its ultimate clients (the “China AMC Underlying Clients”). The China AMC 
Underlying Clients are the beneficial owners of Huaxia New Era Renminbi (華夏新時代人民幣), Huaxia Global Select Renminbi (華夏全球精選人民幣), 
Mackenzie ChinaAMC All China Equity Fund and JSS Equity – All China Fund. None of China AMC Underlying Clients hold an interest of 30% or more. To 
the best knowledge of China AMC after due enquiry, each of the China AMC Underlying Clients is an independent third party of the Company, its subsidiaries, 
China AMC, CSB and the companies which are members of the same group of CSB.

<<<PAGE 33>>>
33
(11) 
China AMC HK is a member of the same group of CSB. China AMC HK proposes to subscribe for and hold Offer Shares under the International Offering in 
accounts in its capacity as the discretionary fund manager managing assets on behalf of its ultimate clients (the “China AMC HK Underlying Clients”). The 
China AMC HK Underlying Clients are the beneficial owners of China AMC China Focus Fund, China AMC Select Greater China Technology Fund, China 
AMC Fund – China AMC China Opportunities Fund, China AMC China Growth Fund (SICAV) and C215. Except for Manulife (International) Limited, Futu 
Securities International (Hong Kong) Limited, Yuanta Securities (HK) Company Ltd and Hong Kong Monetary Authority, none of China AMC HK Underlying 
Clients hold an interest of 30% or more. To the best knowledge of China AMC HK after due enquiry, each of the China AMC HK Underlying Clients is an 
independent third party of the Company, its subsidiaries, China AMC HK, CSB and the companies which are members of the same group of CSB.
* 
For identification purposes only

<<<PAGE 34>>>
34
Allocations of Offer Shares to Cornerstone Investors and/or their close associates with a 
consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 
of the Guide for New Listing Applicants to permit the Company to allocate further Offer Shares 
in the International Offering to certain Cornerstone Investors as placees, subject to the following 
conditions:
(a) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;
(b) 
the Offer Shares allocated to all existing Shareholders and their close associates (whether 
as cornerstone investors and/or as placees) and cornerstone investors as permitted under the 
Size-based Exemption (as defined in the Guide for New Listing Applicants) do not exceed 
30% of the total number of the H Shares offered under the Global Offering;
(c) 
each Director, supervisor, chief executive of the Company and Controlling Shareholders 
confirms that no securities have been allocated to them or their respective close associates 
under the Size-based Exemption; and
(d) 
details of the allocation to the Cornerstone Investors under the Size-based Exemption will be 
disclosed in this announcement. Such allocations of Offer Shares are in compliance with all 
the conditions under the consent granted by the Stock Exchange.
For details of the further allocations of Offer Shares to Cornerstone Investors, please refer to 
the section headed “Allotment Results Details – International Offering – Allotees with Waivers/
Consents Obtained” in this announcement.

<<<PAGE 35>>>
35
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
The Offer Shares are being offered and sold (1) solely to qualified institutional buyers as defined 
in Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under 
the U.S. Securities Act and (2) outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated January 20, 2026 issued by Busy Ming Group Co., 
Ltd. (湖南鳴鳴很忙商業連鎖股份有限公司) for detailed information about the Global Offering 
described above before deciding whether or not to invest in the H Shares thereby being offered.
Potential investors of the Offer Shares should note that the Joint Sponsors and Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the paragraph headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Hong Kong 
Underwriting Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 
a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on January 28, 
2026).

<<<PAGE 36>>>
36
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering (after taking into account the full 
exercise of the Offer Size Adjustment Option and before any exercise of the Over-allotment 
Option), the total number of H Shares held by the public represents approximately 33.95% of the 
total issued share capital of the Company, which is higher than the minimum prescribed percentage 
of H Shares required to be held in public hands of 10% under Rule 8.08(1) of the Listing Rules 
calculated based on the final Offer Price of HK$236.60 per Offer Share, thereby satisfying the 
public float requirement under Rule 8.08(1) of the Listing Rules.
Based on the final Offer Price of HK$236.60 per Offer Share, the Company satisfies the free float 
requirement under Rule 8.08A of the Listing Rules.
The Directors also confirm that immediately following the completion of the Global Offering (after 
taking into account the full exercise of the Offer Size Adjustment Option and before any exercise 
of the Over-allotment Option), (i) no placee will, individually, be placed more than 10% of the 
enlarged issued share capital of the Company immediately after the Global Offering; (ii) there will 
not be any new substantial Shareholder upon Listing (after taking into account the full exercise of 
the Offer Size Adjustment Option and before any exercise of the Over-allotment Option); and (iii) 
there will be at least 300 Shareholders at the time of the Listing in compliance with Rule 8.08(2) 
of the Listing Rules.
COMMENCEMENT OF DEALINGS
Share certificates for the Offer Shares will only become valid evidence of title at 8:00 a.m. on 
Wednesday, January 28, 2026 (Hong Kong time), provided that (i) the Global Offering has become 
unconditional in all respects, and (ii) the right of termination as described in the paragraph headed 
“Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – 
Hong Kong Underwriting Agreement – Grounds for Termination” in the Prospectus has not been 
exercised. Investors who trade H Shares on the basis of publicly available allocation details before 
the receipt of H Share certificates or before the H Share certificates become valid evidence of title 
do so entirely at their own risk.
Assuming that the Hong Kong Public Offering becomes unconditional at or before 8:00 a.m. in 
Hong Kong on Wednesday, January 28, 2026, it is expected that dealings in the H Shares on the 
Stock Exchange will commence at 9:00 a.m. on Wednesday, January 28, 2026. The H Shares will 
be traded in board lots of 100 H Shares each and the stock code of the H Shares will be 1768.
By order of the Board
Busy Ming Group Co., Ltd.
Mr. Yan Zhou
Chairman of the Board, Executive Director and General Manager
Hong Kong, January 27, 2026
As at the date of this announcement, the Board of Directors of the Company comprises Mr. 
Yan Zhou, Mr. Zhao Ding, Mr. Wang Yutong, Mr. Wang Ping’an and Mr. Li Wei as executive 
Directors; Dr. Su Kai as non-executive Director and Ms. Peng Hui, Mr. Qiu Huang and Ms. Wu 
Qianhui as independent non-executive Directors.
