# 配发结果公告抽取任务：3388.HK Shenzhen Creality 3D Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**28/05/2026 22:38**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0528/2026052802543.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3388.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
  - 提示：最终基石股数 ÷ base offer（不含超额配售）。优先用公告基石表的 Total 行；若表内已给『假设超额配售权未行使』的百分比，可直接采用。**若公告与招股书均无基石投资者（无基石表、全文无 Cornerstone Investor），必须填 0 —— 这是「确定的零」，不得留 NaN。**

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
  - 提示：【流水线自动回填，不要自己推断】本字段由 greenshoe 阶段依据上市后港交所的《行使超额配售权》公告确定：有行使公告则填其实际配发股数（部分行使也有数字），无行使公告且 30 天窗口已过则填 0。**严禁**从配发结果公告里「假设未行使」的口径反推，那会把实际行使的公司填成 0。此处填 NaN 即可，后续会被确定性回填覆盖。
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
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities 
in the United States or in any other jurisdictions. The Offer Shares have not been and will not be registered under 
the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities Act”) or securities law 
of any state or other jurisdiction of the United States and may not be offered, sold, pledged or otherwise transferred 
within the United States, except in transactions exempt from, or not subject to, the registration requirements of the U.S. 
Securities Act and in compliance with any applicable state securities laws. There will be no public offer of the Offer 
Shares in the United States. The Offer Shares are being offered and sold (1) to qualified institutional buyers as defined 
in Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under the U.S. Securities Act; 
and (2) outside the United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act and 
applicable laws of each jurisdiction where those offers and sales occur.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
May 20, 2026 (the “Prospectus”) issued by Shenzhen Creality 3D Technology Co., Ltd. (深圳市創想三維科技股份有
限公司) (the “Company”) for detailed information about the Global Offering described below before deciding whether 
or not to invest in the H Shares thereby being offered. Any investment decision in relation to the Offer Shares should 
be taken solely in reliance on the information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited, 
as stabilizing manager (the “Stabilizing Manager”) (or its affiliates or any person acting for it), on behalf of the 
Underwriters, to the extent permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, 
may over-allocate or effect transactions with a view to stabilizing or supporting the market price of the H Shares at 
such price, in such amounts and in such manners as the Stabilizing Manager, its affiliates or any person acting for it 
may determine and at a level higher than that which might otherwise prevail for a limited period after the Listing Date. 
However, there is no obligation on the Stabilizing Manager (or its affiliates or any person acting for it) to conduct 
any such stabilizing action. Such stabilizing action, if taken, (a) will be conducted at the absolute discretion of the 
Stabilizing Manager (or its affiliates or any person acting for it) and in what the Stabilizing Manager reasonably 
regards as the best interest of our Company, (b) may be discontinued at any time and (c) is required to be brought to an 
end within 30 days of the last day for lodging applications under the Hong Kong Public Offering (which is Thursday, 
June 25, 2026). Such stabilizing action, if taken, may be effected in all jurisdictions where it is permissible to do so, 
in each case in compliance with all applicable laws, rules and regulatory requirements, including the Securities and 
Futures (Price Stabilizing) Rules (Chapter 571 W of the Laws of Hong Kong), as amended, made under the Securities 
and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Thursday, June 25, 2026). 
After this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of 
the H Shares, could fall.
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinator (for itself and on behalf 
of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” 
in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to 
be on Friday, May 29, 2026).

<<<PAGE 2>>>
2
Shenzhen Creality 3D Technology Co., Ltd.
深圳市創想三維科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
73,427,550 H Shares (subject to the 
 Over-allotment Option)
Number of Hong Kong Offer Shares
:
7,342,800 H Shares
Number of International Offer Shares
:
66,084,750 H Shares (subject to the 
 Over-allotment Option)
Offer Price
:
HK$18.80 per H Share, plus brokerage of 
 1.0%, SFC transaction levy of 0.0027%, 
 AFRC transaction levy of 0.00015% and 
 Stock Exchange trading fee of 0.00565% 
 (payable in full on application in Hong 
 Kong dollars and subject to refund)
Nominal Value
:
RMB1.00 per H Share
Stock Code
:
3388
Sole Sponsor, Sponsor-Overall Coordinator, Joint Global Coordinator,
Joint Bookrunner and Joint Lead Manager
Overall Coordinator, Joint Global Coordinator and Joint Bookrunner
Joint Bookrunner and
Joint Lead Manager
Joint Bookrunners

<<<PAGE 3>>>
3
Shenzhen Creality 3D Technology Co., Ltd.
深圳市創想三維科技股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated May 20, 2026 (the “Prospectus”) issued by 
Shenzhen Creality 3D Technology Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
H Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
3388
Stock short name
CREALITY
Dealings commencement date
May 29, 2026#
# 
see note at the end of the announcement
Price Information
Offer Price
HK$18.80
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the 
Over-allotment Option)
73,427,550
Final Number of Offer Shares in Hong Kong Public Offering
7,342,800
Final Number of Offer Shares in International Offering 
(before exercise of the Over-allotment Option)
66,084,750
Number of issued Shares upon Listing (before exercise of the 
Over-allotment Option)
466,840,101
Over-allocation
No. of Offer Shares over-allocated
11,014,050
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.

<<<PAGE 4>>>
4
Proceeds
Gross proceeds (Note)
HK$1,380.44 million
Less: Estimated listing expenses payable based on the Offer 
Price
HK$(108.12) million
Net proceeds
HK$1,272.32 million
Note: Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
The Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if any) 
for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus on a pro rata 
basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
251,375
No. of successful applications
44,336
Subscription level
3,829.42 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong 
Public Offering
7,342,800
No. of Offer Shares reallocated from the International Offering
0
Final no. of Offer Shares under the Hong Kong Public Offering
7,342,800
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering (before the exercise of the Over-allotment 
Option)
10%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can refer to www.
hkeipo.hk/IPOResult to perform a search by identification number or www.hkeipo.hk/IPOResult for the full list of 
allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
183
Subscription Level
26.80 times
No. of Offer Shares initially available under the International 
Offering
66,084,750
Final no. of Offer Shares under the International Offering
66,084,750
% of Offer Shares under the International Offering to the Global 
Offering (before the exercise of the Over-allotment Option)
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for a 
consent under Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to, 
among other things, allocate further H Shares in the International Offering to the Cornerstone 
Investors and/or their close associate (i) none of the Offer Shares subscribed by the placees and 
the public have been financed directly or indirectly by the Company, any of the directors, chief 
executive, supervisors, substantial Shareholders, existing Shareholders of the Company or any of 
its subsidiaries or their respective close associates; and (ii) none of the placees and the public who 
have purchased the Offer Shares are accustomed to taking instructions from the Company, any of 
the directors, chief executive, supervisors, substantial Shareholders, existing Shareholders of the 
Company or any of its subsidiaries or their respective close associates in relation to the acquisition, 
disposal, voting or other disposition of H Shares registered in his/her/its name or otherwise held by 
him/her/it.

<<<PAGE 6>>>
6
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of Offer 
Shares allocated
% of total number 
of Offer Shares 
(assuming the Over-
allotment Option is 
not exercised)  
Note 1/Note 2
% of total issued 
share capital in the 
Company after the 
Global Offering 
(assuming the  
Over-allotment 
Option is not 
exercised)  
Note 1/Note 2/Note 3
Existing 
Shareholders 
or their close 
associates
Taikang Life Insurance Co., Ltd (“Taikang Life”)
8,327,250
11.34%
1.78%
No
CITIC Industrial International Investment Limited 
(“CITIC Industrial International”)
6,245,400
8.51%
1.34%
No
CPE Greater China Enterprises Growth Fund (“CPE 
Greater China”)
4,163,550
5.67%
0.89%
No
Martis Fund, L.P. (“Martis Fund”)
3,330,900
4.54%
0.71%
No
Hong Kong BoYue International Investment Fund Co., 
Limited (“BoYue Fund”)
2,081,700
2.84%
0.45%
No
Greater Bay Area Homeland Investments Limited 
(“GBAHIL”)
2,081,700
2.84%
0.45%
No
Apex Insight Investment L.P. (“Apex”)
2,081,700
2.84%
0.45%
No
Oasis Investments II Master Fund Ltd. (“Oasis Fund”)
1,665,450
2.27%
0.36%
No
Jump Trading Pacific Pte. Ltd. (“Jump Trading”)
1,665,450
2.27%
0.36%
No
Polymer Asia Fund LP (“Polymer”)
832,650
1.13%
0.18%
No
Dingxin (Securities) Limited (“Dingxin Securities”)
832,650
1.13%
0.18%
No
Colloway Group Limited (“Colloway”)
832,650
1.13%
0.18%
No
Seven Grand Managers, LLC (“Seven Grand”)
832,650
1.13%
0.18%
No
Integrated Core Strategies (Asia) Pte. Ltd. (“ICSA”)
832,650
1.13%
0.18%
No
Optimas Capital Limited (“Optimas Capital”)
832,650
1.13%
0.18%
No
Total
36,639,000
49.90%
7.85%
Notes:
1. 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” of 
the Prospectus.
2. 
Only taking into account the Offer Shares allocated to the relevant investors as Cornerstone Investors under the 
Global Offering. In addition to the Offer Shares subscribed for as Cornerstone Investors, Taikang Life, CITIC 
Industrial International, Martis Fund, BoYue Fund, GBAHIL, Apex, Oasis Fund, Jump Trading, Polymer, 
Dingxin Securities, Colloway, Seven Grand, ICSA and Optimas Capital and/or their respective close associates 
was allocated further Offer Shares as placees in the International Offering. Please refer to the section headed 
“Allotment Results Details – International Offering – Allottees with Waivers/Consents Obtained” in this 
announcement for details. Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-
up as indicated below. For details, please refer to the section headed “Lock-up Undertakings – Cornerstone 
Investors” in this announcement.
3. 
The number of H Shares immediately after the Global Offering is the same as the number of total issued shares 
of the Company after the Global Offering.

<<<PAGE 7>>>
7
Allottee with Waiver/Consent Obtained
Investor
No. of Offer 
Shares 
allocated
% of total 
number of 
Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
share capital in the 
Company after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 3
Relationship
Allottees with consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further H Shares to 
Cornerstone Investors and/or their close associates Note 1
Taikang Life
2,498,100
3.40%
0.54%
A Cornerstone Investor
CITIC Industrial International, CITIC 
Securities Asset Management Company 
Limited, CITIC Securities International 
Capital Management Limited, CITIC 
Securities Asset Management (HK) 
Limited, and China Asset Management 
(Hong Kong) Limited
1,921,950
2.62%
0.41%
A Cornerstone Investor and 
close associates of CITIC 
Industrial International, a 
Cornerstone Investor
Martis Fund
999,150
1.36%
0.21%
A Cornerstone Investor
BoYue Fund
570,000
0.78%
0.12%
A Cornerstone Investor
GBAHIL (Mega Prime Development 
Limited, Poly Platinum Enterprises 
Limited and GIGA Industries Limited)
624,450
0.85%
0.13%
A Cornerstone Investor
Apex
5,229,900
7.12%
1.12%
A Cornerstone Investor
Oasis Fund
499,500
0.68%
0.11%
A Cornerstone Investor
Jump Trading
499,500
0.68%
0.11%
A Cornerstone Investor
Polymer Capital Management (HK) 
Limited and Pacific Alliance Investment 
Management (HK) Limited
262,200
0.36%
0.06%
Close associates of Polymer, a 
Cornerstone Investor
Dingxin Securities
83,250
0.11%
0.02%
A Cornerstone Investor
Colloway
249,750
0.34%
0.05%
A Cornerstone Investor
Optimas Capital, and Optimas Capital 
Management Pte. Ltd.
499,500
0.68%
0.11%
A Cornerstone Investor and the 
investment manager of ICSA, a 
Cornerstone Investor, through 
separately managed account 
structure
Seven Grand
249,750
0.34%
0.05%
A Cornerstone Investor

<<<PAGE 8>>>
8
Investor
No. of Offer 
Shares 
allocated
% of total 
number of 
Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
share capital in the 
Company after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 3
Relationship
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants 
in relation to allocations to connected clients Note 2
CICC Financial Trading Limited 
(“CICC FT”)
15,900
0.02%
0.003%
Connected client
Huatai Capital Investment Limited 
(“HTCI”)
1,950
0.003%
0.0004%
Connected client
Harvest Global Investments Limited 
(“Harvest”)
12,450
0.02%
0.003%
Connected client
HSBC Global Asset Management 
(Hong Kong) Limited (“HSBC GAM”)
124,800
0.17%
0.03%
Connected client
China Southern Asset Management Co., 
Ltd. (“China Southern”)
41,550
0.06%
0.009%
Connected client
Funde Ivy OFC-Funde Pioneers Equity 
Sub-Fund (“Funde Pioneers”)
1,950
0.003%
0.0004%
Connected client
Notes:
1. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details – International Offering – Cornerstone Investors” in this announcement. For details of the 
consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further H 
Shares to the Cornerstone Investors and/or their close associates, please refer to the section headed “Others/
Additional Information – Allottees with consent under Chapter 4.15 of the Guide for New Listing Applicants 
in relation to allocations of further H Shares to Cornerstone Investors and/or their close associates” in this 
announcement.
2. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for 
New Listing Applicants in relation to allocations to connected clients, please refer to the section headed “Others/
Additional Information – Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines” in this announcement.
3. 
The number of H Shares immediately after the Global Offering is the same as the number of total issued shares 
of the Company after the Global Offering.

<<<PAGE 9>>>
9
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of H 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
% of total issued share 
capital in the Company 
subject to lock-up 
undertakings upon 
Listing (assuming the 
Over-allotment Option 
is not exercised)
Last day subject 
to the lock-up 
undertakingsNote1
Chen Chun (“Mr. Chen”) Note 2
51,600,000
11.05%
May 28, 2027
Shenzhen Creality Chuangwei Technology 
Co., Ltd. (“Creality Chuangwei”) Note 2
25,800,000
5.53%
May 28, 2027
Shenzhen Creality Huida Technology 
Enterprise (Limited Partnership) (“Creality 
Huida”) Note 2
6,450,000
1.38%
May 28, 2027
Ao Danjun (“Mr. Ao”) Note 2
51,600,000
11.05%
May 28, 2027
Shenzhen Longge’er Investment Technology 
Co., Ltd. (“Longge’er Investment”) Note 2
25,800,000
5.53%
May 28, 2027
Liu Huilin (“Mr. Liu”) Note 2
51,600,000
11.05%
May 28, 2027
Shenzhen Creality Industrial Development 
Co., Ltd. (“Creality Industrial”) Note 2
25,800,000
5.53%
May 28, 2027
Tang Jingke (“Mr. Tang”) Note 2
51,600,000
11.05%
May 28, 2027
Shenzhen Creality Chuangtou Shiye Co., Ltd. 
(“Creality Chuangtou”) Note 2
25,800,000
5.53%
May 28, 2027
Shenzhen Creality Changsheng Technology 
Enterprise (Limited Partnership) (“Creality 
Changsheng”) Note 2
6,450,000
1.38%
May 28, 2027
Total
322,500,000
69.08%
Notes:
1. 
The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws and relevant 
lock-up undertakings as disclosed in the Prospectus.
2. 
Upon Listing, Mr. Chen, Mr. Ao, Mr. Liu and Mr. Tang, Creality Chuangwei, Creality Huida, Longge’er 
Investment, Creality Industrial, Creality Chuangtou and Creality Changsheng will constitute a group of 
Controlling Shareholders. For further details, please refer to “Relationship with our Controlling Shareholders” in 
the Prospectus. This subsection illustrates their direct shareholding in the Company, and each of them is subject 
to the same lock-up as disclosed above.

<<<PAGE 10>>>
10
Cornerstone Investors
Name
Number of H Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
% total issued 
share capital in the 
Company subject to 
lock-up undertakings 
upon Listing 
(assuming 
the Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings Note 1
Taikang Life
8,327,250
1.78%
November 28, 2026
CITIC Industrial 
International
6,245,400
1.34%
November 28, 2026
CPE Greater China
4,163,550
0.89%
November 28, 2026
Martis Fund
3,330,900
0.71%
November 28, 2026
BoYue Fund
2,081,700
0.45%
November 28, 2026
GBAHIL
2,081,700
0.45%
November 28, 2026
Apex
2,081,700
0.45%
November 28, 2026
Oasis Fund
1,665,450
0.36%
November 28, 2026
Jump Trading
1,665,450
0.36%
November 28, 2026
Polymer
832,650
0.18%
November 28, 2026
Dingxin Securities
832,650
0.18%
November 28, 2026
Colloway
832,650
0.18%
November 28, 2026
Seven Grand
832,650
0.18%
November 28, 2026
ICSA
832,650
0.18%
November 28, 2026
Optimas Capital
832,650
0.18%
November 28, 2026
Total
36,639,000
7.85%
Note:
1. 
In accordance with the relevant cornerstone investment agreements, the required lock-up period ends on 
November 28, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or transferring 
Shares subscribed for pursuant to the relevant cornerstone investment agreements after the indicated date.

<<<PAGE 11>>>
11
Other Existing Shareholders (including the Pre-IPO Investors as defined in the “History, 
Development and Corporate Structure” section of the Prospectus)
Name
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
share capital in 
the Company 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakingsNote1
Shenzhen Creality 3D Enterprise 
(Limited Partnership) (深圳市創想三維
企業(有限合夥))
6,450,000
1.38%
May 28, 2027
Shenzhen Creality Yunding Technology 
Enterprise (Limited Partnership) (深圳市
創想雲頂科技企業(有限合夥))
6,450,000
1.38%
May 28, 2027
Qianhai Equity Investment Fund (Limited 
Partnership) (前海股權投資基金(有限合
夥))
15,949,070
3.42%
May 28, 2027
Zhongyuan Qianhai Equity Investment 
Fund (Limited Partnership) (中原前海股
權投資基金(有限合夥)) 
3,417,658
0.73%
May 28, 2027
Smart Internet Telecom Ark (Shenzhen) 
Venture Capital Fund Partnership Limited 
Partnership (智慧互聯電信方舟(深圳)創
業投資基金合夥企業(有限合夥)) 
3,505,290
0.75%
May 28, 2027
Shenzhen Capital Group Co., Ltd. (深圳
市創新投資集團有限公司)
7,361,109
1.58%
May 28, 2027
Shenzhen Nanshan Hongtu Equity 
Investment Fund Partnership Limited 
Partnership (深圳市南山紅土股權投資基
金合夥企業(有限合夥))
9,639,548
2.06%
May 28, 2027

<<<PAGE 12>>>
12
Name
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
share capital in 
the Company 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakingsNote1
Guangxi Tencent Venture Capital Co., 
Ltd. (廣西騰訊創業投資有限公司)
8,500,328
1.82%
May 28, 2027
Shenzhen Pingshan Kaisheng Integrated 
Circuit Venture Investment Partnership 
(Limited Partnership) (深圳坪山凱晟集
成電路創業投資合夥企業(有限合夥)
5,696,096
1.22%
May 28, 2027
Wuhan Renzhe Buyou Equity Investment 
Partnership LP (武漢仁者不憂股權投資
合夥企業(有限合夥)) 
3,417,658
0.73%
May 28, 2027
Shenzhen Guoxin South No. 4 Investment 
Partnership Enterprise Limited 
Partnership (深圳國新南方四號投資合夥
企業(有限合夥))
525,794
0.11%
May 28, 2027
Total
70,912,551
15.19%
Notes:
1. 
Pursuant to the applicable PRC laws, all existing Shareholders are not permitted to dispose of any of the Shares 
held by them within 12 months following the Listing Date.
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
H Shares 
allotted
Allotment as % 
of International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as % 
of International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised)
Allotment as 
% of total 
Offer Shares 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over-allotment 
Option is fully 
exercised)
Number of H 
Shares held 
upon Listing
% of total issued 
share capital 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)**
% of total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised)**
Top 1
10,825,350
16.38%
14.04%
14.74%
12.82%
10,825,350
2.32%
2.27%
Top 5
34,797,900
52.66%
45.13%
47.39%
41.21%
34,797,900
7.45%
7.28%
Top 10
50,572,350
76.53%
65.59%
68.87%
59.89%
50,572,350
10.83%
10.58%
Top 25
71,767,350
108.60%
93.08%
97.74%
84.99%
71,767,350
15.37%
15.02%
* 
Ranking of placees is based on the number of Offer Shares allotted to the placees.
** 
The number of H Shares immediately after the Global Offering is the same as the number of total issued shares 
of the Company after the Global Offering.

<<<PAGE 13>>>
13
H SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders*
Number 
of H 
Shares 
allotted
Allotment as 
% of 
International 
Offering 
(assuming no 
exercise of the
 Over-
allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
Allotment as 
% of total 
Offer Shares 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over-
allotment 
Option is 
fully 
exercised)
Number of 
H Shares 
held upon 
Listing
% of total 
issued 
share 
capital 
upon Listing 
(assuming 
no exercise 
of the Over-
allotment 
Option)**
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised)**
Top 1
0
0.00%
0.00%
0.00%
0.00%
322,500,000
69.08%
67.49%
Top 5
10,825,350
16.38%
14.04%
14.74%
12.82%
381,698,353
81.76%
79.88%
Top 10
26,304,300
39.80%
34.12%
35.82%
31.15%
415,773,399
89.06%
87.01%
Top 25
64,353,900
97.38%
83.47%
87.64%
76.21%
457,240,657
97.94%
95.69%
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholder upon Listing.
** 
The number of H Shares immediately after the Global Offering is the same as the number of total issued shares 
of the Company after the Global Offering.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number 
of H 
Shares 
allotted
Allotment 
as % of 
International 
Offering
 (assuming 
no exercise 
of the Over 
allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised)
Allotment 
as % of 
total Offer 
Shares 
(assuming 
no exercise 
of the 
Over-
allotment 
Option)
Allotment 
as % of 
total Offer 
Shares 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised)
Number 
of H
Shares 
held 
upon 
Listing
Number 
of Shares 
held 
upon 
Listing
% of total 
issued share 
capital upon 
Listing 
(assuming no 
exercise of 
the Over-
allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised)
Top 1
0
0.00%
0.00%
0.00%
0.00%
322,500,000
322,500,000
69.08%
67.49%
Top 5
10,825,350
16.38%
14.04%
14.74%
12.82%
381,698,353
381,698,353
81.76%
79.88%
Top 10
26,304,300
39.80%
34.12%
35.82%
31.15%
415,773,399
415,773,399
89.06%
87.01%
Top 25
64,353,900
97.38%
83.47%
87.64%
76.21%
457,240,657
457,240,657
97.94%
95.69%
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 14>>>
14
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 251,375 valid 
applications made by the public will be conditionally allocated on the basis set out below:
BASIS OF ALLOTMENT UNDER THE HONG KONG PUBLIC OFFERING
Pool A
Number of 
H Shares 
applied for
Number 
of valid 
applications
Basis of allocation/ballot
Approximate 
percentage 
allotted of the 
total number 
of H Shares 
applied for
150
38,516
1,156 out of 38,516 applicants to receive 150 H Shares
3.00%
300
12,146
463 out of 12,146 applicants to receive 150 H Shares
1.91%
450
24,358
1,068 out of 24,358 applicants to receive 150 H Shares
1.46%
600
6,408
311 out of 6,408 applicants to receive 150 H Shares
1.21%
750
5,163
270 out of 5,163 applicants to receive 150 H Shares
1.05%
900
3,385
189 out of 3,385 applicants to receive 150 H Shares
0.93%
1,050
3,838
226 out of 3,838 applicants to receive 150 H Shares
0.84%
1,200
2,925
180 out of 2,925 applicants to receive 150 H Shares
0.77%
1,350
2,114
136 out of 2,114 applicants to receive 150 H Shares
0.71%
1,500
26,899
1,786 out of 26,899 applicants to receive 150 H Shares
0.66%
3,000
7,941
670 out of 7,941 applicants to receive 150 H Shares
0.42%
4,500
8,961
869 out of 8,961 applicants to receive 150 H Shares
0.32%
6,000
4,075
437 out of 4,075 applicants to receive 150 H Shares
0.27%
7,500
2,977
345 out of 2,977 applicants to receive 150 H Shares
0.23%
9,000
2,690
332 out of 2,690 applicants to receive 150 H Shares
0.21%
10,500
2,710
352 out of 2,710 applicants to receive 150 H Shares
0.19%
12,000
1,931
263 out of 1,931 applicants to receive 150 H Shares
0.17%
13,500
1,609
228 out of 1,609 applicants to receive 150 H Shares
0.16%
15,000
11,928
1,752 out of 11,928 applicants to receive 150 H Shares
0.15%
30,000
7,771
1,450 out of 7,771 applicants to receive 150 H Shares
0.09%
45,000
5,993
1,286 out of 5,993 applicants to receive 150 H Shares
0.07%
60,000
4,413
1,046 out of 4,413 applicants to receive 150 H Shares
0.06%
75,000
3,542
906 out of 3,542 applicants to receive 150 H Shares
0.05%
90,000
2,477
675 out of 2,477 applicants to receive 150 H Shares
0.05%
105,000
2,781
799 out of 2,781 applicants to receive 150 H Shares
0.04%
120,000
2,430
731 out of 2,430 applicants to receive 150 H Shares
0.04%
135,000
1,946
610 out of 1,946 applicants to receive 150 H Shares
0.03%
150,000
18,284
5,940 out of 18,284 applicants to receive 150 H Shares
0.03%
Total
220,211
Total number of Pool A successful applicants: 24,476

<<<PAGE 15>>>
15
Pool B
Number of 
H Shares 
applied for
Number 
of valid 
applications
Basis of allocation/ballot
Approximate 
percentage 
allotted of the 
total number 
of H Shares 
applied for
300,000
13,174
5,270 out of 13,174 applicants to receive 150 H Shares
0.02%
450,000
4,830
2,686 out of 4,830 applicants to receive 150 H Shares
0.02%
600,000
3,013
2,117 out of 3,013 applicants to receive 150 H Shares
0.02%
750,000
2,073
1,746 out of 2,073 applicants to receive 150 H Shares
0.02%
900,000
1,427
1,394 out of 1,427 applicants to receive 150 H Shares
0.02%
1,050,000
1,129
150 H Shares plus 121 out of 1,129 applicants to receive an 
additional 150 H Shares
0.02%
1,200,000
944
150 H Shares plus 221 out of 944 applicants to receive an 
additional 150 H Shares
0.02%
1,350,000
604
150 H Shares plus 216 out of 604 applicants to receive an 
additional 150 H Shares
0.02%
1,500,000
2,460
150 H Shares plus 1,178 out of 2,460 applicants to receive 
an additional 150 H Shares
0.01%
3,000,000
500
300 H Shares plus 299 out of 500 applicants to receive an 
additional 150 H Shares
0.01%
3,671,400
1,010
450 H Shares plus 61 out of 1,010 applicants to receive an 
additional 150 H Shares
0.01%
Total 
 31,164
Total number of Pool B successful applicants: 19,860
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.

<<<PAGE 16>>>
16
OTHERS/ADDITIONAL INFORMATION
Allocations of Offer Shares to the Cornerstone Investors and/or their close associates with a 
consent under Chapter 4.15 of the Guide for New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 
of the Guide for New Listing Applicants (the “Size-based Exemption”) to permit the Company 
to allocate further Offer Shares in the International Offering to certain Cornerstone Investors and 
their close associates, as placees, subject to the following conditions (“Allocation to Size-based 
Exemption Participants”):
(a) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;
(b) 
H Shares allocated to all existing shareholders and their close associates (whether as 
cornerstone investors and/or as placees) as permitted under this exemption do not exceed 
30% of the total number of H Shares offered under the Global Offering;
(c) 
each of the Directors, chief executives and members of the group of Controlling Shareholders 
of the Company confirms that no securities have been allocated to them or their respective 
close associates under the Size-based Exemption;
(d) 
the Allocation to Size-based Exemption Participants is not expected to affect the Company’s 
ability to satisfy its public float requirement; and
(e) 
details of the Allocation to Size-based Exemption Participants under the Size-based 
Exemption will be disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to Cornerstone Investors and/or their close associates, 
please refer to the section headed “Allotment Results Details – International Offering – Allottees 
with Waivers/Consents Obtained” in this announcement.
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines. Details of the placement to connected 
clients are set out below. The Company has applied to the Stock Exchange for, and the Stock 
Exchange has granted, consents under paragraph 1C(1) of the Placing Guidelines to permit the 
Company to allocate such Offer Shares in the International Offering to the connected clients. The 
allocation of Offer Shares to such connected clients is in compliance with all the conditions under 
the consent granted by the Stock Exchange.

<<<PAGE 17>>>
17
Part A – Connected Clients holding the beneficial interest of the Offer Shares on a non-
discretionary basis on behalf of independent third parties
No.
Connected Distributor
Connected 
Client
Relationship with 
the Connected 
Distributor
Identities of the ultimate 
beneficial owners of the Offer 
Shares or, where applicable, 
details of the structured 
products under which the 
subscription by the Connected 
Client was made (e.g. OTC 
total return swaps) 
Whether the 
Connected Client 
is a collective 
investment scheme 
which is not 
authorised by the 
SFC or is expected 
to hold the Offer 
Shares on behalf of 
such scheme
Number of Offer 
Shares allocated 
to the connected 
client
Approximate 
percentage of total 
number of Offer 
Shares (assuming 
the Over-allotment 
Option is not 
exercised)
Approximate 
percentage of 
total Shares in 
issue immediately 
following the 
completion of 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
1.
China International 
Capital Corporation Hong 
Kong Securities Limited 
(“CICC”)
CICC FT
Same group entities
Please refer to note 1
No
15,900
0.02%
0.003%
2.
Huatai Financial Holdings 
(Hong Kong) Limited 
(“Huatai”)
HTCI
Same group entities
Please refer to note 2
No
1,950
0.003%
0.0004%
Notes:
1. 
CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one 
OTC swap transactions (the “OTC Swaps”) with each other and the ultimate clients (the “CICC FT Ultimate 
Clients”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the 
OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed to the CICC FT 
Ultimate Clients, subject to customary fees and commissions. The OTC Swaps will be fully funded by the CICC 
FT Ultimate Clients. During the terms of the OTC Swaps, all economic returns of the Offer Shares subscribed 
by CICC FT will be passed to the CICC FT Ultimate Clients and all economic loss shall be borne by the CICC 
FT Ultimate Clients through the OTC Swaps, and CICC FT will not take part in any economic return or bear 
any economic loss in relation to the Offer Shares. The OTC Swaps are linked to the Offer Shares and the CICC 
FT Ultimate Clients may request CICC FT to redeem it at their own discretions, upon which CICC FT shall 
dispose of the Offer Shares and settle OTC Swaps in cash in accordance with the terms and conditions of the 
OTC Swap. Despite that CICC FT will hold the legal title of the Offer Shares by itself, it will not exercise 
the voting rights attaching to the relevant Offer Shares during the terms of the OTC Swaps according to its 
internal policy. The CICC FT Ultimate Clients for purpose of this placee subscription include (i) Yuanlesheng 
Qiangye Private Securities Investment Fund (源樂晟強業私募證券投資基金), whose fund manager is Tibet 
Yuanlesheng Asset Management Company Ltd.(“Tibet Longrising”, 西藏源樂晟資產管理有限公司) and 
ultimate beneficial owners holding 30% or more interest are Zeng Xiaojie and Hu Caiyang, (ii) Yuanlesheng 
Qiangshu Private Securities Investment Fund (源樂晟強樹私募證券投資基金), whose fund manager is Tibet 
Longrising and ultimate beneficial owner holding 30% or more interest is Zeng Xiaojie, (iii) Yuanlesheng 
Qiangshi Private Securities Investment Fund (源樂晟強勢私募證券投資基金), whose fund manager is Tibet 
Longrising and ultimate beneficial owner holding 30% or more interest is Zeng Xiaojie, (iv) Baoyin Long/Short 
Steady No. 1 Private Securities Investment Fund (保銀多空穩健1號私募證券投資基金), whose fund manager 
is Pinpoint Investment Management Limited (“Pinpoint Investment”, 上海保銀私募基金管理有限公司) and 
ultimate beneficial owner holding 30% or more interest is Wang Qiang, and (v) Baoyin Long/Short Steady No. 
2 Private Securities Investment Fund (保銀多空穩健 2 號私募證券投資基金), whose fund manager is Pinpoint 
Investment and ultimate beneficial owner holding 30% or more interest is Wang Qiang.
To the best of CICC FT’s knowledge having made all reasonable enquiries, each of the CICC FT Ultimate 
Clients is an independent third party of CICC FT, CICC and the companies which are members of the same 
group of companies as each of the Underwriters.

<<<PAGE 18>>>
18
2. 
Pursuant to an ISDA Agreement (the “ISDA Agreement”), HTCI, which intends to participate in the Global 
Offering as a placee, will hold the beneficial interest of the Shares on a non-discretionary basis as the single 
underlying holder under a back-to-back total return swap (the “Back-to-back TRS”) to be entered by HTCI in 
connection with a Client TRS (as defined below) placed by and fully funded (i.e. with no financing provided 
by HTCI) by the Huatai Ultimate Client (as defined below), by which, HTCI will, subject to customary fees 
and commissions, pass the full economic exposure of the Shares to the Huatai Ultimate Client, which in effect, 
HTCI will hold the beneficial interest of the Shares on behalf of the Huatai Ultimate Client.
Huatai is a sub-broker under the International Offering. HTCI is a member of the same group as Huatai, and 
accordingly HTCI is considered as a “connected client” of Huatai pursuant to paragraph 1B of the Placing 
Guidelines.
The offshore investor (the “Huatai Ultimate Client”), through its investment manager, will place a total 
return swap order (the “Client TRS”) with HTCI in connection with the Company’s IPO. In order to hedge its 
exposure under the Client TRS, HTCI participates in the Company’s IPO and subscribes the Shares through 
placing order with Huatai during the International Offering.
The purpose of HTCI to subscribe for the Shares is for hedging the Client TRS order placed by the Huatai 
Ultimate Client. Pursuant to the terms of the Client TRS, during the tenor of the Client TRS, subject to 
customary fees and commissions, all economic returns of the Shares will be passed to the Huatai Ultimate Client 
through the Client TRS and all economic loss shall be borne by the Huatai Ultimate Client. HTCI will not take 
any economic return or bear any economic loss in relation to the Shares.
The Huatai Ultimate Client may exercise an early termination right to terminate the Client TRS at any time from 
the issue date of the Client TRS which should be on or after the date on which the Shares are listed on the Stock 
Exchange at its own discretion. Upon the termination upon maturity or early termination of the Client TRS 
by the Huatai Ultimate Client, HTCI will dispose the Shares on the secondary market and the Huatai Ultimate 
Client will receive a final settlement amount of the Client TRS in cash in accordance with the terms and 
conditions of the Client TRS which should have taken into account all the economic returns or economic loss in 
relation to the Shares. If upon the maturity of the Client TRS, the Huatai Ultimate Client intends to extend the 
investment period, subject to further agreement between HTCI and the relevant Huatai Ultimate Client, the term 
of the Client TRS could be extended by way of a new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Shares by itself, and pass through 
the economic exposure to the Huatai Ultimate Client, being a client who places a Client TRS order with HTCI 
in connection with the IPO of the Company. HTCI will not exercise the voting right of the Shares during the 
tenor of the Client TRS.
During the life of the Client TRS, HTCI may continue to hold the Shares in its custodian account, or to hold 
some or all of the Shares in a prime brokerage account for stock borrowing purposes, where HTCI will lend 
out its holding of underlying Shares in the form of stock borrowing loans consistent with market practice to 
lower its finance costs, provided that HTCI has the ability to call back the Shares on loan at any time in order to 
satisfy its obligations under the Client TRS to ensure the economic interests are ultimately passed to the Huatai 
Ultimate Client.
The Huatai Ultimate Client and its respective ultimate beneficial owner holding 30% or more interest include:
Huatai Ultimate Client 
UBO with 30% or more interests
MANTOU HOLDING LIMITED 
Meng Wang
HTCI has confirmed that, to the best of their knowledge having made all reasonable enquiries, the Huatai 
Ultimate Client is an independent third party of HTCI, Huatai and the companies which are members of the 
same group of companies as each of the Underwriters.

<<<PAGE 19>>>
19
Part B – Connected Clients holding the beneficial interest of the Offer Shares on a 
discretionary basis on behalf of independent third parties
No.
Connected Distributor
Connected 
Clients
Relationship with the Connected 
Distributor
Whether the 
Connected Client is a 
collective investment 
scheme which is not 
authorised by the 
SFC or is expected 
to hold the Offer 
Shares on behalf of 
such scheme 
Number of Offer 
Shares allocated to 
the connected client
Approximate 
percentage of total 
number of Offer 
Shares (assuming 
the Over-allotment 
Option is not 
exercised)
Approximate 
percentage of total 
Shares in issue 
immediately following 
the completion of 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised)
1.
Deutsche Bank AG, 
Hong Kong Branch 
(“DBHK”)
Harvest
Harvest is a wholly-owned 
subsidiary of Harvest Financial 
Group Limited, which in turn is 
wholly owned by Harvest Fund 
Management Co., Ltd. Harvest 
Fund Management Co., Ltd. is 
30% owned by DWS Investments 
Singapore Limited. DWS 
Investments Singapore Limited 
is a wholly-owned subsidiary 
of DWS Group GmbH & Co. 
KGaA. DWS Group GmbH & 
Co. KGaA is partially owned by 
DB Beteiligungs-Holdings GmbH 
(79.49%), Nippon Life Insurance 
(5%) and outside shareholders 
(15.51 %) as at December 31, 
2025. DB Beteiligungs-Holdings 
GmbH is wholly owned by 
Deutsche Bank AG.
No 
12,450
0.02%
0.003%
2.
The Hongkong and 
Shanghai Banking 
Corporation Limited 
(“HSBC”) 
HSBC GAM
HSBC and HSBC GAM are 
members of the same group 
No 
124,800
0.17%
0.03%
3.
Huatai
China 
Southern
China Southern and Huatai are 
members of the same group 
No 
41,550
0.06%
0.009%
4.
Funde Securities 
Limited (“Funde 
Securities”) 
Funde 
Pioneers
The investment manager of 
Funde Pioneers is Funde Asset 
Management (Hong Kong) 
Company Limited, which is a 
subsidiary of Funde Holdings 
(Group) Co., Ltd. Funde Securities 
is also a subsidiary of Funde 
Holdings (Group) Co., Ltd. 
Therefore, Funde Pioneers is a 
member of the same group with 
Funde Securities.
No 
1,950
0.003%
0.0004%

<<<PAGE 20>>>
20
Notes:
1. 
Harvest will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on 
behalf of their investors, each of which is, to the best knowledge of Harvest, an independent third party of the 
Company, its subsidiaries, its substantial shareholders, Harvest, DBHK and the companies which are members 
of the same group of companies as Harvest and DBHK.
The funds are as follows:
• 
HARVEST ESG CHINA A RESEARCH SELECT FUND
• 
ASIA FRONTIER EQUITY FUND
• 
Harvest BOCHK Diverse Income Fund
• 
Harvest Total Return Fund
• 
HGI IPO MANDATE NO.1
No ultimate beneficial owner holds 30% or more interest in the funds.
2. 
HSBC is a sub-broker under the International Offering. HSBC GAM will hold the Offer Shares in its capacity 
as the discretionary fund manager managing assets on behalf of its underlying clients. HSBC GAM is a member 
of the same group of companies as HSBC. As a result, HSBC GAM is a connected client of HSBC. To the best 
knowledge of HSBC GAM after due enquiry, each of its underlying clients is an independent third party of the 
Company, its subsidiaries, HSBC, HSBC GAM and the companies which are members of the same group of 
HSBC and HSBC GAM.
3. 
Huatai is a sub-broker under the International Offering. China Southern, a qualified domestic institutional 
investor as approved by the relevant PRC authority to conduct asset management business, will hold the Offer 
Shares as the independent agent and discretionary manager of certain QDII funds (the “China Southern 
Ultimate Clients”). China Southern has confirmed that, to the best of their knowledge, each of such China 
Southern Underlying Clients are independent third parties of the Company, its subsidiaries, China Southern, 
Huatai and the companies which are members of the same group of companies as Huatai and China Southern.
The China Southern Ultimate Clients for purpose of this placing subscription include China Southern Hong 
Kong Growth Dynamic Allocation Hybrid Fund (南方香港成長靈活配置混合), China Southern Hong Kong 
Digital Economy Hybrid Initiating Fund (QDII) (南方港股數字經濟混合發起(QDII)), China Southern Hong 
Kong Select Equity Fund (南方香港 LOF), China Southern China New Economy 9-Month Holding Period 
Hybrid Fund (QDII) (南方中國新興經濟9個月持有期混合(QDII)) and China Southern Global Dynamic 
Allocation Fund (南方全球精選配置股票(QDII-FOF)), for each of which no ultimate beneficial owner holds 
30% or more interest.
4. 
Funde Securities is a sub-broker under the International Offering. Funde Pioneers will hold the Offer Shares on 
behalf of Huang Jinghua and Kong Weina (“Funde Pioneers Ultimate Clients”) on a discretionary basis. To 
the best knowledge, information and belief of Funde Pioneers after making all reasonable enquiries, each of the 
Funde Pioneers Ultimate Clients is an independent third party of the Company, its subsidiaries, its substantial 
shareholders, Funde Pioneers, Funde Securities and the companies which are members of the same group of 
companies as Funde Pioneers and Funde Securities.

<<<PAGE 21>>>
21
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
herein have not been, and will not be, registered under the United States Securities Act of 1933, 
as amended (the “U.S. Securities Act”). The securities may not be offered or sold in the United 
States except pursuant to an exemption from the registration requirements of the U.S. Securities 
Act and in compliance with any applicable state securities laws, or outside the United States 
unless in compliance with Regulation S under the U.S. Securities Act. There will be no public 
offer of securities in the United States.
The Offer Shares are being offered and sold (1) to qualified institutional buyers as defined in 
Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under the 
U.S. Securities Act and (2) outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated May 20, 2026 issued by Shenzhen Creality 
3D Technology Co., Ltd. for detailed information about the Global Offering described below 
before deciding whether or not to invest in the H Shares thereby being offered.
* 
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinator (for itself and on 
behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section 
headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is 
currently expected to be on May 29, 2026).

<<<PAGE 22>>>
22
PUBLIC FLOAT AND FREE FLOAT
Pursuant to Rule 19A.13A of the Listing Rules, assuming that the Over-allotment Option is 
not exercised, based on the Offer Price of HK$18.80 per Offer Share, the expected market 
capitalization upon the Listing is HK$8,776.6 million, and the minimum prescribed public float 
percentage applicable to the Shares is the higher of (i) the percentage that would result in the 
expected market value of H shares held by the public to be HK$1,500,000,000 at the time of 
listing and (ii) 15%. Immediately following completion of the Global Offering (assuming the 
Over-allotment Option is not exercised), an aggregate of 131,440,101 H Shares, representing 
approximately 28.2% of the issued share capital of the Company and having an expected market 
value (based on the Offer Price of HK$18.80 per Offer Share) at the time of Listing of HK$2.47 
billion, will count towards the public float. Therefore, the number of H Shares held in public hands 
is higher than the prescribed percentage of H Shares required to be held in public hands under Rule 
19A.13A(1) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. The H Shares held by all existing Pre-IPO investors to be converted from Unlisted 
Shares are subject to a lock-up period of 12 months following the Listing Date under the applicable 
PRC laws. As such, H Shares held by the Cornerstone Investors and all existing Pre-IPO investors 
upon the Listing shall not be counted towards the free float of the H Shares of the Company at 
the time of Listing. Based on the Offer Price of HK$18.80 per H Share, 36,788,550 H Shares 
with an expected market value of approximately HK$691.6 million, which is higher than HK$600 
million as required under Rule 19A.13C of the Listing Rules, will not be subject to any disposal 
restrictions (whether under contract, the Listing Rules, applicable laws or otherwise) at the time of 
Listing. Therefore, the Company satisfies the free float requirement under Rule 19A.13C(1)(b) of 
the Listing Rules.
The Directors confirm that, immediately after the completion of the Global Offering (assuming 
the Over-allotment Option is not exercised), (i) no placee will, individually, be placed more than 
10% of the enlarged issued share capital of the Company; (ii) there will not be any new substantial 
shareholder (as defined in the Listing Rules) of the Company; (iii) the three largest public 
shareholders of the Company do not hold more than 50% of the H Shares in public hands at the 
time of the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there 
will be at least 300 H Shareholders at the time of the Listing in compliance with Rule 8.08(2) of 
the Listing Rules.

<<<PAGE 23>>>
23
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, May 29, 
2026 (Hong Kong time), provided that the Global Offering has become unconditional and the right 
of termination described in the section headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has not been 
exercised. Investors who trade the H Shares on the basis of publicly available allocation details 
prior to the receipt of H Share certificates or prior to the H Share certificates becoming valid 
evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Friday, May 
29, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Friday, May 29, 2026 (Hong Kong time). The H Shares will be 
traded in board lots of 150 H Shares each, and the stock code of the H Shares will be 3388.
By order of the Board
Shenzhen Creality 3D Technology Co., Ltd.
Mr. Ao Danjun
Executive Director and Vice Chairman of the Board
Hong Kong, May 28, 2026
Directors of the Company to which this announcement relates are: (i) Mr. Chen Chun, Mr. Ao 
Danjun, Mr. Liu Huilin, Mr. Tang Jingke, and Mr. Fang Zongdi as executive directors; (ii) Mr. 
Huang Hongman as non-executive director; and (iii) Ms. Gao Li, Ms. Wang Yating, and Mr. Liang 
Huaquan as independent non-executive directors.
