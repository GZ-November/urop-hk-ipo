# 配发结果公告抽取任务：6880.HK MOMENTA GLOBAL LIMITED - W

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**07/07/2026 22:21**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0707/2026070701963.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6880.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) and Hong 
Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement. 
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those defined in 
the prospectus dated Monday, June 29, 2026 (the “Prospectus”) issued by MOMENTA GLOBAL LIMITED (the “Company”). 
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase or 
subscribe for securities. Potential investors should read the Prospectus for detailed information about the Company and the 
Global Offering described below before deciding whether or not to invest in the Offer Shares. 
This announcement is not for release, publication or distribution, directly or indirectly, in or into the United States (including its 
territories and possessions, any state of the United States and the District of Columbia). This announcement does not constitute 
or form a part of any offer or solicitation to purchase or subscribe for securities in the United States or in any other jurisdiction. 
The Offer Shares have not been and will not be registered under the United States Securities Act of 1933, as amended from time 
to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the United States and may not be offered, 
sold, pledged or transferred within the United States, except in transactions exempt from, or not subject to, the registration 
requirements of the U.S. Securities Act. There will be no public offer of the Offer Shares in the United States. The Offer Shares 
are being offered and sold (1) solely to qualified institutional buyers as defined in Rule 144A under the U.S. Securities Act 
pursuant to an exemption from registration under the U.S. Securities Act and (2) outside the United States in offshore transactions 
in reliance on Regulation S under the U.S. Securities Act. 
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited, as the stabilizing 
manager (the “Stabilizing Manager”), or any person acting for it, on behalf of the Underwriters, may over-allocate or effect 
transactions with a view to stabilizing or supporting the market price of the Class A Ordinary Shares at a level higher than that 
which might otherwise prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing 
Manager, or any person acting for it, to conduct any such stabilizing action, which, if taken, will be conducted at the absolute 
discretion of the Stabilizing Manager and may be discontinued at any time. Any such stabilizing activity is required to be brought 
to an end on Sunday, August 2, 2026, being the 30th day after the last day for lodging applications under the Hong Kong Public 
Offering. Such stabilization action, if taken, may be effected in all jurisdictions where it is permissible to do so, in each case in 
compliance with all applicable laws, rules and regulatory requirements, including the Securities and Futures (Price Stabilizing) 
Rules (Cap. 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance (Cap. 571 of the 
Laws of Hong Kong).
Potential investors should be aware that stabilizing action cannot be taken to support the price of the Class A Ordinary Shares for 
longer than the stabilization period which begins on the Listing Date and is expected to expire on Sunday, August 2, 2026, being 
the 30th day after the last day for the lodging of applications under the Hong Kong Public Offering. After this date, no further 
stabilizing action may be taken, and demand for the Class A Ordinary Shares and the price of the Class A Ordinary Shares could 
fall. 
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out in the 
Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not resident in Hong 
Kong. Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators (for themselves 
and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting — 
Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any 
time prior to 8:00 a.m. (Hong Kong time) on the Listing Date.
The Company is controlled through weighted voting rights. Prospective investors should be aware of the potential risks of 
investing in a company with a WVR structure, in particular that the WVR Beneficiaries, whose interests may not necessarily 
be aligned with those of our Shareholders as a whole, will be in a position to exert significant influence over the outcome of 
Shareholders’ resolutions, irrespective of how other Shareholders vote. For further information about the risks associated with 
the WVR structure, see “Risk Factors — Risks Related to the WVR Structure” in the Prospectus. Prospective investors should 
make the decision to invest in the Company only after due and careful consideration.

<<<PAGE 2>>>
2
MOMENTA GLOBAL LIMITED
(A company controlled through weighted voting rights and incorporated in the Cayman Islands with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
19,938,300 Offer Shares (subject to the 
Over-allotment Option)
Number of Hong Kong Offer Shares
:
1,993,840 Offer Shares 
Number of International Offer Shares
:
17,944,460 Offer Shares (subject to the 
Over-allotment Option)
Final Offer Price
:
HK$295.60 per Offer Share plus brokerage 
of 1%, SFC transaction levy of 0.0027%, 
Stock Exchange trading fee of 0.00565% 
and AFRC transaction levy of 0.00015% 
(payable in full on application in Hong 
Kong dollars, subject to refund)
Nominal Value
:
US$0.00025 per Offer Share
Stock Code
:
6880
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
MOMENTA GLOBAL LIMITED
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated June 29, 2026 (the “Prospectus”) issued by 
MOMENTA GLOBAL LIMITED (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the Class A 
Ordinary Shares could move substantially even with a small number of the Class A 
Ordinary Shares traded and should exercise extreme caution when dealing in the Class A 
Ordinary Shares.
SUMMARY
Company information
Stock code 
6880
Stock short name 
MOMENTA-W
Dealings commencement date
July 8, 2026*
*  see note at the end of the announcement
Price Information
Final Offer Price
HK$295.60
Fixed Offer Price
HK$295.60
Offer Shares and Share Capital
Number of Offer Shares
19,938,300 
Number of Offer Shares in Hong Kong Public Offering
1,993,840 
Number of Offer Shares in International Offering  
(before exercise of the Over-allotment Option)
17,944,460 
Number of issued Shares upon Listing (before exercise of 
the Over-allotment Option)
235,538,011 
Over-allocation
No. of Offer Shares over-allocated
2,990,740
International Offering
2,990,740
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery, stock borrowing or a combination of these means. In the event the Over-
allotment Option is exercised, an announcement will be made on the Stock Exchange’s website. 

<<<PAGE 4>>>
4
Proceeds
Gross proceeds
(Note) 
HK$5,893.8 million
  Less: Estimated listing expenses payable based on Offer Price 
HK$237.9 million
Net proceeds 
HK$5,655.9 million
Note:	
Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of proceeds, 
please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. In the event that the Over-
allotment Option is exercised, the Company will adjust the allocation of the net proceeds on a pro rata basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications 
209,045
No. of successful applications 
58,585
Subscription level
413.63 times
Claw-back triggered 
N/A
No. of Offer Shares initially available under the Hong Kong Public 
Offering
1,993,840
No. of Offer Shares reallocated from the International Offering 
N/A
Final number of Offer Shares under the Hong Kong Public 
Offering
1,993,840
% of final number of Offer Shares under the Hong Kong Public 
Offering to the Global Offering
10%
Note:	 For details of the final allocation of Offer Shares to the Hong Kong Public Offering, investors can refer to 
https://www.hkeipo.hk/iporesult to perform a search by identification number or https://www.hkeipo.hk/iporesult for the 
full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
239
Subscription level
20.31 times
No. of Offer Shares initially available under the International 
Offering 
17,944,460 
No. of Offer Shares reallocated to the Hong Kong Public Offering 
N/A
Final number of Offer Shares under the International Offering
17,944,460 
% of final number of Offer Shares under the International Offer to 
the Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) 
a waiver from strict compliance with Rule 10.04 of the Listing Rules and/or a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the 
Stock Exchange to permit Offer Shares in the International Offering to be placed to certain existing 
Shareholders and/or their close associates; and (b) a consent under paragraph 18 of Chapter 4.15 
of the Guide for New Listing Applicants to permit the Company to, among other things, allocate 
further Offer Shares in the International Offering to existing Shareholders and/or Cornerstone 
Investors and/or their close associates, (i) none of the Offer Shares subscribed by the placees 
and the public have been financed directly or indirectly by the Company, any of the Directors, 
chief executive of the Company, the Controlling Shareholders, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates; and 
(ii) none of the placees and the public who have purchased the Offer Shares are accustomed to 
taking instructions from the Company, any of the Directors, chief executive of the Company, the 
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company or any 
of its subsidiaries or their respective close associates in relation to the acquisition, disposal, voting 
or other disposition of the Class A Ordinary Shares registered in his/her/its name or otherwise held 
by him/her/it. 

<<<PAGE 6>>>
6
The placees in the International Offering include the following:
Cornerstone Investors
Investor
Note 1
No. of Offer 
Shares 
allocated
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total issued 
Class A Ordinary 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
Note 1 Note 2
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Note 1 Note 2
Existing 
shareholders 
or their close 
associates
Note 4
GIC 
2,650,760 
13.29%
1.29%
1.13%
No
Fidelity International
2,650,760 
13.29%
1.29%
1.13%
No
BlackRock
662,680 
3.32%
0.32%
0.28%
No
Mercedes-Benz AG
662,680 
3.32%
0.32%
0.28%
Yes (existing 
Shareholder)
Oaktree
530,140 
2.66%
0.26%
0.23%
No
Golden Link
397,600 
1.99%
0.19%
0.17%
Yes (existing 
Shareholder)
Franklin Templeton
265,060 
1.33%
0.13%
0.11%
No
Boyu
265,060 
1.33%
0.13%
0.11%
No
Gaoyi Entities
Note 3
265,060 
1.33%
0.13%
0.11%
No
CPIC
265,060 
1.33%
0.13%
0.11%
No
GF Fund 
265,060 
1.33%
0.13%
0.11%
No
ChinaAMC (HK)
265,060 
1.33%
0.13%
0.11%
No
Suzhou Mosu
656,060 
3.29%
0.32%
0.28%
No
GigaDevice 
159,040 
0.80%
0.08%
0.07%
No
TOTAL
9,960,080
49.95%
4.83%
4.23%

<<<PAGE 7>>>
7
Investor
Note 1
No. of Offer 
Shares 
allocated
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total issued 
Class A Ordinary 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
Note 1 Note 2
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Note 1 Note 2
Existing 
shareholders 
or their close 
associates
Note 4
1.	
In addition to the Offer Shares subscribed for as Cornerstone Investors, GIC, Fidelity International, a close associate 
of BlackRock, Golden Link, a close associate of Franklin Templeton, close associates of Boyu, Perseverance Asset 
Management (as defined below), CPIC, GF Fund, a close associate of ChinaAMC (HK) and ChinaAMC (HK) were 
allocated further Offer Shares as placees in the International Offering. Please refer to the section headed “Allotment 
Results Details — International Offering — Allotees with Waivers/Consents Obtained” in this announcement for details. 
Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-up as indicated below. For details, 
please refer to the section headed “Lock-up Undertakings — Cornerstone Investors” in this announcement.
2.	
Only taking into account the Offer Shares allocated to the relevant investors as Cornerstone Investors under the Global 
Offering.
3.	
Gaoyi Entities include Perseverance Asset Management and CICC FT (in connection with Gaoyi OTC Swaps). The 
allocation of Offer Shares to CICC FT as a Cornerstone Investor is with consent under paragraph 1C(1) of the Placing 
Guidelines in relation to allocations to connected clients. For further details, please refer to the section headed 
“Cornerstone Investors” and “Waivers and Exemption — Consent in respect of Proposed Subscription of Shares by 
a Cornerstone Investor who is a Connected Client” of the Prospectus, and the section headed “Others/Additional 
Information — Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines” in 
this announcement.
4.	
For further details of the Cornerstone Investors, please refer to the sections headed “Cornerstone Investors” and 
“Waivers and Exemption — Subscription for Shares by Existing Shareholders and/or their Close Associates” and “— 
Consent in respect of Proposed Subscription of Shares by a Cornerstone Investor who is a Connected Client” of the 
Prospectus. 

<<<PAGE 8>>>
8
Allotees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total issued 
Class A Ordinary 
Shares
(assuming the 
Over-allotment 
Option is not 
exercised) 
Note 1
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Note 1
Relationship
Allotees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation 
to allocations of further Offer Shares to existing Shareholders and/or Cornerstone Investors and/or their close 
associates
Note 3
Cornerstone Investor
Mercedes-Benz AG
662,680
3.32%
0.32%
0.28%
A Cornerstone 
Investor and 
an existing 
Shareholder.
Placees
 Note 2
GIC
1,060,000
5.32%
0.51%
0.45%
A Cornerstone 
Investor.
Fidelity International
1,060,000
5.32%
0.51%
0.45%
A Cornerstone 
Investor.
BlackRock Asset Management North 
Asia Limited
397,600
1.99%
0.19%
0.17% A close associate 
of BlackRock, 
a Cornerstone 
Investor.
Golden Link
389,600
1.95%
0.19%
0.17%
A Cornerstone 
Investor and 
an existing 
Shareholder.
FRANKLIN TEMPLETON 
INVESTMENTS (ASIA) LIMITED 
159,000
0.80%
0.08%
0.07% A close associate 
of Franklin 
Templeton, a 
Cornerstone 
Investor.

<<<PAGE 9>>>
9
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total issued 
Class A Ordinary 
Shares
(assuming the 
Over-allotment 
Option is not 
exercised) 
Note 1
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Note 1
Relationship
Close associates of Boyu
Boyu Capital Management 
(Singapore) Pte. Ltd.
95,400
0.48%
0.05%
0.04% A close associate 
of Boyu, a 
Cornerstone 
Investor.
Boyu Capital Investment 
Management Co Ltd
63,600
0.32%
0.03%
0.03% A close associate 
of Boyu, a 
Cornerstone 
Investor.
Subtotal
159,000
0.80%
0.08%
0.07%
—
Perseverance Asset Management
53,000
0.27%
0.03%
0.02%
A Cornerstone 
Investor.
CPIC IMHK
10,620
0.05%
0.005%
0.005%
A Cornerstone 
Investor.
Pacific Asset Management
42,380
0.21%
0.02%
0.02%
A Cornerstone 
Investor.
GF Fund 
53,000
0.27%
0.03%
0.02%
A Cornerstone 
Investor.
ChinaAMC (HK) and its close associate
ChinaAMC (HK)
47,700
0.24%
0.02%
0.02%
A Cornerstone 
Investor.
China Asset Management Co., Ltd.
5,300
0.03%
0.0026%
0.0023% A close associate 
of ChinaAMC 
(HK), a 
Cornerstone 
Investor.
Subtotal
53,000
0.27%
0.03%
0.02%
—

<<<PAGE 10>>>
10
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total issued 
Class A Ordinary 
Shares
(assuming the 
Over-allotment 
Option is not 
exercised) 
Note 1
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Note 1
Relationship
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) 
of the Placing Guidelines in relation to subscription for Offer Shares by existing Shareholders and/or their close 
associates
Note 4
Cornerstone Investor
Golden Link
397,600
1.99%
0.19%
0.17%
A Cornerstone 
Investor and 
an existing 
Shareholder.
Placees
 Note 2
Close associates of Cognitive Dynamics Limited and OG Blaze Dynamics Limited
CDH EMERGING MARKETS 
FUND II, L.P.
26,500
0.13%
0.01%
0.01% A close associate 
of each of 
Cognitive 
Dynamics 
Limited and OG 
Blaze Dynamics 
Limited, existing 
Shareholders.
CDH Prime Growth, L.P.
106,000
0.53%
0.05%
0.05% A close associate 
of each of 
Cognitive 
Dynamics 
Limited and OG 
Blaze Dynamics 
Limited, existing 
Shareholders.
Subtotal
132,500
0.66%
0.06%
0.06%
—

<<<PAGE 11>>>
11
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total issued 
Class A Ordinary 
Shares
(assuming the 
Over-allotment 
Option is not 
exercised) 
Note 1
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Note 1
Relationship
Granite Asia IX VCC (acting for and 
in respect of GX Access)
13,200
0.07%
0.01%
0.01%
An existing 
Shareholder and 
a close associate 
of each of GGV 
Capital VI L.P., 
GGV Capital VI 
Entrepreneurs 
Fund L.P. 
and GGV 
Capital VI Plus 
L.P., existing 
Shareholders.
Infore Capital Management (Hong 
Kong) Limited
26,500
0.13%
0.01%
0.01% A close associate 
of Wise Impact 
Asia Limited, 
an existing 
Shareholder.
AEZ Capital Master Fund
2,600
0.01%
0.0013%
0.0011%
An existing 
Shareholder.
Eastern Bell Capital VIII Investment 
Limited
2,600
0.01%
0.0013%
0.0011% A close associate 
of Eastern Bell 
International 
XXVIII Limited, 
an existing 
Shareholder.
SMB Holding Corporation
397,600
1.99%
0.19%
0.17%
An existing 
Shareholder.

<<<PAGE 12>>>
12
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total issued 
Class A Ordinary 
Shares
(assuming the 
Over-allotment 
Option is not 
exercised) 
Note 1
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Note 1
Relationship
Close associates of Eagle Fixed Income Alternative Investments Limited
Oman Investment Authority
25,000
0.13%
0.01%
0.01% A close associate 
of Eagle 
Fixed Income 
Alternative 
Investments 
Limited, 
an existing 
Shareholder.
Jabal China AMC Loong Equity Fund
1,500
0.01%
0.0007%
0.0006% A close associate 
of Eagle 
Fixed Income 
Alternative 
Investments 
Limited, 
an existing 
Shareholder.
Subtotal
26,500
0.13%
0.01%
0.01%
—
Taibai Investments Pte. Ltd
265,000
1.33%
0.13%
0.11% A close associate 
of Anderson 
Investments Pte. 
Ltd., an existing 
Shareholder.

<<<PAGE 13>>>
13
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total issued 
Class A Ordinary 
Shares
(assuming the 
Over-allotment 
Option is not 
exercised) 
Note 1
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Note 1
Relationship
Close associates of Blue Lake Capital Opportunity Fund I (HongKong) Limited and Blue Lake Fund, L.P.
Blue Lake Capital Opportunity Fund 
I, L.P.
2,600
0.01%
0.0013%
0.0011% A close associate 
of each of Blue 
Lake Capital 
Opportunity 
Fund I 
(HongKong) 
Limited and 
Blue Lake Fund, 
L.P., existing 
Shareholders.
Mr. HU Lei
6,560
0.03%
0.0032%
0.0028% A close associate 
of each of Blue 
Lake Capital 
Opportunity 
Fund I 
(HongKong) 
Limited and 
Blue Lake Fund, 
L.P., existing 
Shareholders.
Subtotal
9,160
0.05%
0.0044%
0.0039%
—

<<<PAGE 14>>>
14
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total issued 
Class A Ordinary 
Shares
(assuming the 
Over-allotment 
Option is not 
exercised) 
Note 1
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Note 1
Relationship
Huatai Capital Investment Limited
8,000
0.04%
0.0039%
0.0034% A close associate 
of HTPE 
Explore L.P., 
an existing 
Shareholder.
Giga Industries Limited
2,600
0.01%
0.0013%
0.0011% A close associate 
of each of 
Mega Prime 
Development 
Limited and 
GBA Equity 
Fund I LPF, 
existing 
Shareholders.
Allotees with consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to connected clients
Note 5
Cornerstone Investor
CICC FT (in connection with Gaoyi 
OTC Swaps)
143,140
0.72%
0.07%
0.06%
A Cornerstone 
Investor and a 
connected client.
Placees
 Note 2
DWS Investments Hong Kong 
Limited
7,860
0.04%
0.004%
0.003%
Connected 
client.
DWS Investment GmbH
177,140
0.89%
0.09%
0.08%
Connected 
client.
JP Morgan Asset Management (Asia 
Pacific) Limited 
265,000
1.33%
0.13%
0.11%
Connected 
client.
Bosera Asset Management 
(International) Co., Ltd 
1,300
0.01%
0.0006%
0.0006%
Connected 
client.
Fullgoal Fund Management Co., Ltd.
1,300
0.01%
0.0006%
0.0006%
Connected 
client.

<<<PAGE 15>>>
15
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total issued 
Class A Ordinary 
Shares
(assuming the 
Over-allotment 
Option is not 
exercised) 
Note 1
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Note 1
Relationship
Notes:
1.	
Only taking into account the Offer Shares allocated to the relevant investors under the Global Offering.
2.	
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the number of Offer Shares allocated to the 
investors as placees in the bookbuilding placing tranche in the International Offering. For allocations of Offer Shares to the relevant investors as 
Cornerstone Investors, please refer to the section headed “Allotment Results Details — International Offering — Cornerstone Investors” in this 
announcement.
3.	
For details of the consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of Offer Shares to 
certain existing Shareholder and Cornerstone Investors and/or their respective close associates, please refer to the section headed “Waivers and 
Exemption — Subscription for Shares by Existing Shareholders and/or their Close Associates” of the Prospectus and the section headed “Others/
Additional Information — Allocations of Offer Shares to the existing Shareholders and Cornerstone Investors and/or their close associates with 
consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants” in this announcement. 
4.	
For details of the waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the Placing Guidelines 
in relation to subscription for Offer Shares by existing Shareholders and/or their close associates, please refer to the section headed “Waivers and 
Exemption — Subscription for Shares by Existing Shareholders and/or their Close Associates” of the Prospectus, and the section headed “Others/
Additional Information — Placing to existing Shareholders and/or their close associates with a waiver from the strict compliance with Rule 10.04 of 
the Listing Rules and a prior consent under paragraph 1C(2) of the Placing Guidelines” in this announcement.
5.	
For details of the consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to connected clients, please refer to the section 
headed “Waivers and Exemption — Consent in respect of Proposed Subscription of Shares by a Cornerstone Investor who is a Connected Client” of 
the Prospectus, and the section headed “Others/Additional Information — Placing to connected clients with a prior consent under paragraph 1C(1) of 
the Placing Guidelines” in this announcement.

<<<PAGE 16>>>
16
LOCK-UP UNDERTAKINGS 
Controlling Shareholders
Name
Note 1
Number of Shares held in the 
Company subject to lock-up 
undertakings upon Listing
% of total issued 
Shares after the 
Global Offering upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Note 2
Last day subject to the lock-up 
undertakings
Note 3
Bigsail Holdings Limited 
16,896,621 
Class B Ordinary Shares
7.17%
January 7, 2027 
(First Six-month Period) 
July 7, 2027 
(Second Six-month Period)
Green City Global Limited 
(綠都環球有限公司)
4,458,830 
Class B Ordinary Shares
1.89%
January 7, 2027 
(First Six-month Period) 
July 7, 2027 
(Second Six-month Period)
Vibrant Colour Limited 
(盛色有限公司) 
4,458,830 
Class B Ordinary Shares
1.89%
January 7, 2027 
(First Six-month Period) 
July 7, 2027 
(Second Six-month Period)
Pine Sky International Limited 
3,520,129 
Class B Ordinary Shares
1.49%
January 7, 2027 
(First Six-month Period) 
July 7, 2027 
(Second Six-month Period)
Creative Circuit Limited 
1,408,052 
Class A Ordinary Shares
0.60%
January 7, 2027 
(First Six-month Period) 
July 7, 2027 
(Second Six-month Period)
Vantage Plus Ventures Limited 
(益加創投有限公司)
1,408,052 
Class A Ordinary Shares
0.60%
January 7, 2027 
(First Six-month Period)
 July 7, 2027 
(Second Six-month Period)
Tide Bay Limited 
1,408,052 
Class A Ordinary Shares
0.60%
January 7, 2027 
(First Six-month Period) 
July 7, 2027
(Second Six-month Period)
Tycoon Insight Limited
1,408,052 
Class A Ordinary Shares
0.60%
January 7, 2027 
(First Six-month Period) 
July 7, 2027 
(Second Six-month Period)

<<<PAGE 17>>>
17
Name
Note 1
Number of Shares held in the 
Company subject to lock-up 
undertakings upon Listing
% of total issued 
Shares after the 
Global Offering upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Note 2
Last day subject to the lock-up 
undertakings
Note 3
TOTAL
5,632,208 
Class A Ordinary Shares 
29,334,410 
Class B Ordinary Shares
14.85%
Notes: 
1.	
The above Controlling Shareholders are wholly owned by Mr. CAO Xudong, Dr. XIA Yan, Dr. SUN Gang, Ms. SUN Huan, JIA Sibo, LI Jun, ZHU 
Wangjiang and WANG Jinwei, respectively, who are also subject to the aforementioned lock-up undertakings.
2.	
Discrepancies in the above table between the sum of the percentage of Offer Shares allocated to each investor and the percentage of the total Offer 
Shares allocated to such investors are due to rounding.
3.	
In accordance with the relevant Listing Rules/guidance materials, the required lock-up for the first six-month period ends on January 7, 2027 (the 
“First Six-month Period”) and for the second six-month period ends on July 7, 2027 (the “Second Six-month Period”). The Controlling Shareholders 
may dispose of or transfer Shares after the First Six-month Period subject to that the Controlling Shareholders will not cease to be a Controlling 
Shareholder. The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after the Second Six-month Period.
Existing Shareholders
Name
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
% of total 
issued Class A 
Ordinary Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
Shares after the 
Global Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings
Note 1
All existing Shareholders as 
of the date of the Prospectus 
186,265,301 Class A
 Ordinary Shares 
29,334,410 Class B 
Ordinary Shares
90.33%
91.53%
January 7, 2027
Note:
1.	
Each of the existing Shareholders as of the date of the Prospectus has entered into a deed of lock-up undertakings in favour of the Company, the 
Joint Sponsors and the Overall Coordinators, pursuant to which certain lock-up restrictions have been imposed on its Locked-up Securities from 
(and be inclusive of) the Listing Date and ending on the date that is six months from the Listing Date (i.e., January 7, 2027). For details, please 
refer to the section headed “Underwriting — Lock-up Arrangements — (E) Undertakings by all of our Shareholders as of the date of this Prospectus 
pursuant to Lock-up Undertakings” of the Prospectus.

<<<PAGE 18>>>
18
Cornerstone Investors
Name
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
% of total 
issued Class A 
Ordinary Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
Shares after the 
Global Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings
Note 1
GIC 
2,650,760 Class A 
Ordinary Shares
1.29%
1.13%
January 7, 2027 
Fidelity International
2,650,760 Class A 
Ordinary Shares
1.29%
1.13%
January 7, 2027 
BlackRock
662,680 Class A 
Ordinary Shares
0.32%
0.28%
January 7, 2027 
Mercedes-Benz AG
662,680 Class A 
Ordinary Shares
0.32%
0.28%
January 7, 2027 
Oaktree
530,140 Class A 
Ordinary Shares
0.26%
0.23%
January 7, 2027 
Golden Link
397,600 Class A 
Ordinary Shares
0.19%
0.17%
January 7, 2027 
Franklin Templeton
265,060 Class A 
Ordinary Shares
0.13%
0.11%
January 7, 2027 
Boyu
265,060 Class A 
Ordinary Shares
0.13%
0.11%
January 7, 2027 
Gaoyi Entities
265,060 Class A 
Ordinary Shares
0.13%
0.11%
January 7, 2027 
CPIC
265,060 Class A 
Ordinary Shares
0.13%
0.11%
January 7, 2027 
GF Fund 
265,060 Class A 
Ordinary Shares
0.13%
0.11%
January 7, 2027 
ChinaAMC (HK)
265,060 Class A 
Ordinary Shares
0.13%
0.11%
January 7, 2027 

<<<PAGE 19>>>
19
Name
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
% of total 
issued Class A 
Ordinary Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
Shares after the 
Global Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings
Note 1
Suzhou Mosu
656,060 Class A 
Ordinary Shares
0.32%
0.28%
January 7, 2027 
GigaDevice 
159,040 Class A 
Ordinary Shares
0.08%
0.07%
January 7, 2027 
TOTAL
9,960,080 Class A 
Ordinary Shares
4.83%
4.23%
Note:
1.	
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on January 7, 2027. The Cornerstone Investors will 
cease to be prohibited from disposing of or transferring the Class A Ordinary Shares subscribed for pursuant to the relevant cornerstone investment 
agreements after the indicated date.

<<<PAGE 20>>>
20
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
Class A 
Ordinary 
Shares allotted
Allotment 
as % of the 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment 
as % of the 
International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Class A 
Ordinary Shares 
are issued)
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
exercised and 
new Class A 
Ordinary Shares 
are issued)
Number 
of Class A 
Ordinary 
Shares held 
upon Listing
Number 
of Shares 
held upon 
Listing**
% of total 
issued Class A 
Ordinary Shares 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total 
issued Class A 
Ordinary Shares 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Class A 
Ordinary Shares 
are issued)
% of total 
issued Shares 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)**
% of total 
issued Shares 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Class A 
Ordinary Shares 
are issued)**
Top 1
3,710,760
20.68%
17.72%
18.61%
16.18%
3,710,760
3,710,760
1.80%
1.77%
1.58%
1.56%
Top 5
9,931,680
55.35%
47.44%
49.81%
43.31%
24,180,528
24,180,528
11.73%
11.56%
10.27%
10.14%
Top 10
12,549,140
69.93%
59.94%
62.94%
54.73%
26,797,988
26,797,988
13.00%
12.81%
11.38%
11.23%
Top 25
17,014,540
94.82%
81.27%
85.34%
74.21%
41,889,884
41,889,884
20.31%
20.02%
17.78%
17.56%
Notes:
*	
Ranking of placees is based on the number of Offer Shares allotted to the placees.
**	
Total issued share capital upon Listing includes Class B Ordinary Shares (i.e. Shares with weighted voting rights which will not be converted into Class A Ordinary Shares upon 
Listing). For details on the weighted voting rights structure of the Company, please refer to the section headed “Share Capital” of the Prospectus.

<<<PAGE 21>>>
21
SHAREHOLDERS OF CLASS A ORDINARY SHARES CONCENTRATION ANALYSIS
Class A Shareholders*
Number of 
Class A 
Ordinary 
Shares allotted
Allotment 
as % of the 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
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
exercised and 
new Class A 
Ordinary Shares 
are issued)
Number 
of Class A 
Ordinary 
Shares held 
upon Listing
Number of 
Shares held 
upon Listing**
% of total 
issued Class A 
Ordinary 
Shares upon 
Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total 
issued Class A 
Ordinary Shares 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Class A 
Ordinary Shares 
are issued)
% of total 
issued Shares 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)**
% of total 
issued Shares 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Class A 
Ordinary Shares 
are issued)**
Top 1
0
0.00%
0.00%
0.00%
20,374,980
20,374,980
9.88%
9.74%
8.65%
8.54%
Top 5
927,680
5.17%
4.65%
4.05%
75,612,191
75,612,191
36.67%
36.14%
32.10%
31.70%
Top 10
936,840
5.22%
4.70%
4.09%
108,463,069
137,797,479
52.60%
51.85%
58.50%
57.77%
Top 25
8,504,060
47.39%
42.65%
37.09%
151,871,402
181,205,812
73.65%
72.60%
76.93%
75.97%
Notes:
*	
Ranking of Shareholders of Class A Ordinary Shares is based on the number of Class A Ordinary Shares held by the Shareholders of Class A Ordinary Shares upon Listing.
**	
Total issued share capital upon Listing includes Class B Ordinary Shares (i.e. Shares with weighted voting rights which will not be converted into Class A Ordinary Shares upon 
Listing). For details on the weighted voting rights structure of the Company, please refer to the section headed “Share Capital” of the Prospectus.

<<<PAGE 22>>>
22
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders*
Number of 
Class A 
Ordinary 
Shares 
allotted
Allotment 
as % of the 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment 
as % of the 
International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Class 
A Ordinary 
Shares are 
issued)
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
exercised and 
new Class 
A Ordinary 
Shares are 
issued)
Number 
of Class A 
Ordinary 
Shares held 
upon Listing
Number 
of Class B 
Ordinary 
Shares held 
upon Listing
Number 
of Shares 
held upon 
Listing**
% of total 
issued Class 
A Ordinary 
Shares upon 
Listing 
(assuming 
no exercise 
of the Over-
allotment 
Option)
% of total 
issued Class 
A Ordinary 
Shares upon 
Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Class 
A Ordinary 
Shares are 
issued)
% of total 
issued Shares 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)**
% of total 
issued Shares 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Class 
A Ordinary 
Shares are 
issued)**
Top 1***
0
0.00%
0.00%
0.00%
0.00%
5,632,208
29,334,410
34,966,618
2.73%
2.69%
14.85%
14.66%
Top 5
927,680
5.17%
4.43%
4.65%
4.05%
71,532,824
29,334,410
100,867,234
34.69%
34.19%
42.82%
42.29%
Top 10
936,840
5.22%
4.47%
4.70%
4.09%
108,463,069
29,334,410
137,797,479
52.60%
51.85%
58.50%
57.77%
Top 25
8,504,060
47.39%
40.62%
42.65%
37.09%
151,871,402
29,334,410
181,205,812
73.65%
72.60%
76.93%
75.97%
Notes:
*	
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon Listing.
**	
Total issued Shares upon Listing includes Class B Ordinary Shares (i.e. Shares with weighted voting rights which will not be converted into Class A Ordinary Shares upon 
Listing). For details on the weighted voting rights structure of the Company, please refer to the section headed “Share Capital” of the Prospectus.
***	 Pursuant to a concert party agreement entered into by, among others, Mr. Cao, Dr. Xia, Dr. Sun, Ms. Sun, JIA Sibo, LI Jun, ZHU Wangjiang and WANG Jinwei, Dr. Xia, Dr. 
Sun, Ms. Sun, JIA Sibo, LI Jun, ZHU Wangjiang and WANG Jinwei and their controlled entities agreed to act in concert with Mr. Cao and his controlled entity in exercising 
Shareholders’ rights pertaining to our Company in accordance with Mr. Cao’s instructions, for so long as they, directly or indirectly through their controlled entities, hold 
equity interests in our Company. For further details relating to the concert party arrangement, see the section headed “History, Development and Corporate Structure — 
Concert Party Arrangement and Voting Entrustment Arrangements” of the Prospectus.

<<<PAGE 23>>>
23
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by the 
public will be conditionally allocated on the basis set out below: 
POOL A
NO. OF OFFER 
SHARES APPLIED
 FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF OFFER 
SHARES 
APPLIED FOR
20
86,896
4,345 out of 86,896 applicants to receive 20 shares
5.00%
40
9,962
598 out of 9,962 applicants to receive 20 shares
3.00%
60
3,920
330 out of 3,920 applicants to receive 20 shares
2.81%
80
2,629
272 out of 2,629 applicants to receive 20 shares
2.59%
100
3,922
456 out of 3,922 applicants to receive 20 shares
2.33%
120
1,888
238 out of 1,888 applicants to receive 20 shares
2.10%
140
1,710
236 out of 1,710 applicants to receive 20 shares
1.97%
160
11,079
1,640 out of 11,079 applicants to receive 20 shares
1.85%
180
1,625
249 out of 1,625 applicants to receive 20 shares
1.70%
200
8,338
1,385 out of 8,338 applicants to receive 20 shares
1.66%
300
8,157
1,591 out of 8,157 applicants to receive 20 shares
1.30%
400
3,422
753 out of 3,422 applicants to receive 20 shares
1.10%
500
2,349
588 out of 2,349 applicants to receive 20 shares
1.00%
600
2,455
663 out of 2,455 applicants to receive 20 shares
0.90%
700
1,745
538 out of 1,745 applicants to receive 20 shares
0.88%
800
1,923
616 out of 1,923 applicants to receive 20 shares
0.80%
900
1,190
413 out of 1,190 applicants to receive 20 shares
0.77%
1,000
8,590
3,007 out of 8,590 applicants to receive 20 shares
0.70%
2,000
7,380
3,690 out of 7,380 applicants to receive 20 shares
0.50%
3,000
4,141
2,485 out of 4,141 applicants to receive 20 shares
0.40%
4,000
3,844
2,922 out of 3,844 applicants to receive 20 shares
0.38%
5,000
2,486
2,176 out of 2,486 applicants to receive 20 shares
0.35%
6,000
2,072
20 shares
0.33%
7,000
1,754
20 shares plus 211 out of 1,754 applicants to 
  receive an additional 20 shares
0.32%
8,000
1,190
20 shares plus 286 out of 1,190 applicants to 
  receive an additional 20 shares
0.31%
9,000
882
20 shares plus 309 out of 882 applicants to 
  receive an additional 20 shares
0.30%
10,000
9,621
20 shares plus 4,330 out of 9,621 applicants to 
  receive an additional 20 shares
0.29%
 
Total
195,170
Total number of Pool A successful 
  applicants: 44,710
 

<<<PAGE 24>>>
24
POOL B
NO. OF OFFER 
SHARES APPLIED 
FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF OFFER 
SHARES 
APPLIED FOR
20,000
8,930
40 shares plus 7,144 out of 8,930 applicants to 
  receive an additional 20 shares
0.28%
30,000
1,478
60 shares plus 597 out of 1,478 applicants to 
  receive an additional 20 shares
0.23%
40,000
943
60 shares plus 857 out of 943 applicants to 
  receive an additional 20 shares
0.20%
50,000
501
80 shares plus 177 out of 501 applicants to 
  receive an additional 20 shares
0.17%
60,000
365
80 shares plus 275 out of 365 applicants to 
  receive an additional 20 shares
0.16%
70,000
276
100 shares plus 33 out of 276 applicants to 
  receive an additional 20 shares
0.15%
80,000
182
100 shares plus 84 out of 182 applicants to 
  receive an additional 20 shares
0.14%
90,000
135
100 shares plus 105 out of 135 applicants to 
  receive an additional 20 shares
0.13%
100,000
568
120 shares plus 43 out of 568 applicants to 
  receive an additional 20 shares
0.12%
200,000
225
160 shares plus 108 out of 225 applicants to 
  receive an additional 20 shares
0.08%
300,000
85
200 shares plus 27 out of 85 applicants to 
  receive an additional 20 shares
0.07%
400,000
48
220 shares plus 41 out of 48 applicants to 
  receive an additional 20 shares
0.06%
500,000
39
260 shares plus 8 out of 39 applicants to 
  receive an additional 20 shares
0.05%
600,000
16
280 shares plus 7 out of 16 applicants to 
  receive an additional 20 shares
0.05%
700,000
17
300 shares plus 9 out of 17 applicants to 
  receive an additional 20 shares
0.04%
800,000
11
320 shares plus 6 out of 11 applicants to 
  receive an additional 20 shares
0.04%
900,000
5
340 shares plus 3 out of 5 applicants to 
  receive an additional 20 shares
0.04%
996,920
51
360 shares plus 19 out of 51 applicants to 
  receive an additional 20 shares
0.04%
 
Total
13,875 
Total number of Pool B successful 
  applicants: 13,875
 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
 

<<<PAGE 25>>>
25
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Class A Ordinary Shares. 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them is the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Allocations of Offer Shares to the existing Shareholders and/or Cornerstone Investors and/or 
their close associates with consent under paragraph 18 of Chapter 4.15 of the Guide for New 
Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph 18 
of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to allocate further 
Offer Shares in the International Offering to certain existing Shareholders, Cornerstone Investors 
and/or their close associates as placees (the “Size-based Exemption Participants”), subject to the 
following conditions (the “Size-based Exemption”):
(a)	 the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;
(b)	 the Offer Shares allocated to the Size-based Exemption Participants who are existing 
shareholders and/or their close associates (whether as Cornerstone Investors and/or as placees) 
as permitted under this exemption do not exceed 30% of the total number of Offer Shares 
offered under the Global Offering;
(c)	 each Director, chief executive and Controlling Shareholder of the Company confirms that no 
securities have been allocated to them or their respective close associates under the Size-based 
Exemption; 
(d)	 the allocation to Size-based Exemption Participants will not affect the Company’s ability to 
satisfy its public float requirement under Rule 8.08(1) of the Listing Rules; and
(e)	 details of the allocation to Size-based Exemption Participants under the Size-based Exemption 
will be disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted 
by the Stock Exchange.
For details of the allocations of Offer Shares to Cornerstone Investors, please refer to the section 
headed “Allotment Results Details — International Offering — Allotees with Waivers/Consents 
Obtained” in this announcement. 

<<<PAGE 26>>>
26
Placing to existing Shareholders and/or their close associates with a waiver from the strict 
compliance with Rule 10.04 of the Listing Rules and a prior consent under paragraph 1C(2) of 
the Placing Guidelines
The Company has applied to the Stock Exchange, and the Stock Exchange has granted, a waiver 
from the strict compliance with Rule 10.04 of the Listing Rules and a  consent under paragraph 
1C(2) of the Placing Guidelines to permit the Company to allocate such Offer Shares in the 
International Offering to the existing Shareholders and/or their close associates listed above. 
The allocation of Offer Shares to such existing Shareholders and/or their close associates is in 
compliance with all the conditions under paragraph 14 of Chapter 4.15 of the Guide for New Listing 
Applicants.
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates, 
please refer to the section headed “Allotment Results Details — International Offering — Allotees 
with Waivers/Consents Obtained” in this announcement.

<<<PAGE 27>>>
27
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their connected distributors pursuant to the 
Placing Guidelines. 
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing 
Guidelines to permit the Company to allocate such Offer Shares in the International Offering to the connected clients. The allocation of 
Offer Shares to such connected clients is in compliance with all the conditions under the consent granted by the Stock Exchange. Details of 
the placement to connected clients are set out below:
 
No.
Connected Distributor
Connected Client
Relationship
Whether the 
Connected 
Client is a 
collective 
investment 
scheme 
which is not 
authorized by 
the SFC or is 
expected to 
hold the Offer 
Shares on 
behalf of such 
scheme
Identities of the 
ultimate beneficial 
owners of the 
Offer Shares or, 
where applicable, 
details of the 
structured products 
under which the 
subscription by the 
Connected Client 
was made (e.g. OTC 
total return swaps)
Number of 
Offer Shares to 
be allocated to 
the Connected 
Client
Approximate 
% of total 
number of 
Offer Shares 
under the 
Global 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Approximate 
% of total 
issued Class 
A Ordinary 
Shares under 
the Global 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Approximate 
% of total 
issued Shares 
immediately 
following the 
completion 
of the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Part A — Connected Client holding Offer Shares on a non-discretionary basis on behalf of independent third parties
1.
China International 
Capital Corporation 
Hong Kong 
Securities Limited 
(“CICCHKS”)
CICC Financial 
Trading Limited 
(“CICC FT”)
CICC FT is a member of the 
same group of companies as 
CICCHKS
No
Please refer to 
Note 1
143,140
0.72%
0.07%
0.06%

<<<PAGE 28>>>
28
No.
Connected Distributor
Connected Client
Relationship
Whether the 
Connected 
Client is a 
collective 
investment 
scheme 
which is not 
authorized by 
the SFC or is 
expected to 
hold the Offer 
Shares on 
behalf of such 
scheme
Identities of the 
ultimate beneficial 
owners of the 
Offer Shares or, 
where applicable, 
details of the 
structured products 
under which the 
subscription by the 
Connected Client 
was made (e.g. OTC 
total return swaps)
Number of 
Offer Shares to 
be allocated to 
the Connected 
Client
Approximate 
% of total 
number of 
Offer Shares 
under the 
Global 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Approximate 
% of total 
issued Class 
A Ordinary 
Shares under 
the Global 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Approximate 
% of total 
issued Shares 
immediately 
following the 
completion 
of the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Part B — Connected Clients holding Offer Shares on a discretionary basis on behalf of independent third parties
2.
Deutsche Bank AG, 
Hong Kong Branch 
(“DBHK”)
DWS Investments 
Hong Kong Limited 
(“DWS HK”)
DBHK and DWS HK are 
members of the same group.
No
Please refer to 
Note 2
7,860
0.04%
0.004%
0.003%
3.
DBHK
DWS Investment 
GmbH (“DWS 
Investment”)
DBHK and DWS Investment are 
members of the same group.
No
Please refer to 
Note 3
177,140
0.89%
0.09%
0.08%
4.
J.P. Morgan Securities 
(Asia Pacific) Limited 
(“JPM APAC”) and 
JPMorgan Chase 
Bank, N.A. (“JPM 
Chase”)
JP Morgan Asset 
Management (Asia 
Pacific) Limited 
(“JPM AM”)
JPM APAC, JPM Chase and JPM 
AM are members of the same 
group. 
No
Please refer to 
Note 4
265,000
1.33%
0.13%
0.11%

<<<PAGE 29>>>
29
No.
Connected Distributor
Connected Client
Relationship
Whether the 
Connected 
Client is a 
collective 
investment 
scheme 
which is not 
authorized by 
the SFC or is 
expected to 
hold the Offer 
Shares on 
behalf of such 
scheme
Identities of the 
ultimate beneficial 
owners of the 
Offer Shares or, 
where applicable, 
details of the 
structured products 
under which the 
subscription by the 
Connected Client 
was made (e.g. OTC 
total return swaps)
Number of 
Offer Shares to 
be allocated to 
the Connected 
Client
Approximate 
% of total 
number of 
Offer Shares 
under the 
Global 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Approximate 
% of total 
issued Class 
A Ordinary 
Shares under 
the Global 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Approximate 
% of total 
issued Shares 
immediately 
following the 
completion 
of the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
5.
CMB International 
Securities Limited and 
CMB International 
Global Markets 
Limited (collectively, 
“CMBI”) and China 
Merchants Securities 
(HK) Co., Ltd (“CMS 
HK”)
Bosera Asset 
Management 
(International) Co., 
Ltd (“Bosera AM”)
Bosera AM is a member of the 
same group of CMBI and CMS 
HK.
Yes.
Please refer to 
Note 5
Please refer to 
Note 5
1,300
0.01%
0.0006%
0.0006%
6.
Guotai Junan 
Securities (Hong 
Kong) Limited 
(“GTJA Securities”) 
Fullgoal Fund 
Management Co., 
Ltd. (“Fullgoal 
Fund”)
Fullgoal Fund, GTJA Securities 
and Haitong Securities are 
members of the same group.
Yes
Please refer to 
Note 6
1,300
0.01%
0.0006%
0.0006%
Haitong International 
Securities Company 
Limited (“Haitong 
Securities”)

<<<PAGE 30>>>
30
Notes:
1.	
CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one OTC swap transactions (the “OTC Swaps”) with each other and 
the ultimate clients (the “CICC FT Ultimate Clients”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the OTC Swaps while the 
economic risks and returns of the underlying Offer Shares are passed to the CICC FT Ultimate Clients, subject to customary fees and commissions. The OTC Swaps will be fully 
funded by the CICC FT Ultimate Clients. During the terms of the OTC Swaps, all economic returns of the Offer Shares subscribed by CICC FT will be passed to the CICC FT 
Ultimate Clients and all economic loss shall be borne by the CICC FT Ultimate Clients through the OTC Swaps, and CICC FT will not take part in any economic return or bear 
any economic loss in relation to the Offer Shares. The OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate Clients may request CICC FT to redeem it at their 
own discretion, upon which CICC FT shall dispose of the Offer Shares and settle OTC Swaps in cash in accordance with the terms and conditions of the OTC Swap. Despite 
that CICC FT will hold the legal title of the Offer Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares during the terms of the OTC Swaps 
according to its internal policy. 
To the best knowledge, information and belief of CICC FT after due enquiry, the CICC FT Ultimate Clients are Gaoyi Xiaofeng No.1 Ruiyuan Securities Investment Fund (高
毅曉峰1號睿遠證券投資基金) and Gaoyi Xiaofeng No.2 Zhixin Fund (高毅曉峰2號致信基金), and there is no investor holding 30% or more interests in CICC FT Ultimate 
Clients. To the best of CICC FT’s knowledge having made all reasonable inquiries, each of the CICC FT Ultimate Clients is an independent third party of CICC FT, CICCHKS 
and the companies which are members of the same group of companies as CICCHKS.
2.	
DWS HK will hold the Offer Shares in its capacity as the discretionary fund manager managing DWS Invest Chinese Equities on behalf of its investors, each of which is an 
independent third party.
No ultimate beneficial owner holds 30% or more interest in DWS Invest Chinese Equities.
3.	
DWS Investment will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their investors, each of which is an independent 
third party.
The funds are as follows:
•	
DWS Invest Artificial Intelligence
•	
DWS Invest ESG Global Emerging Markets Equities
No ultimate beneficial owner holds 30% or more interest in the funds.
4.	
JPM AM will hold the Offer Shares in its capacity as the discretionary fund manager managing assets on behalf of its underlying clients. Each of the underlying clients of JPM 
AM is an independent third party of JPM AM, JPM APAC and JPM Chase.

<<<PAGE 31>>>
31
5.	
Each of CMBI and CMS HK is a distributor of the Global Offering. Bosera AM intends to subscribe and hold the Offer Shares in its capacity as the discretionary fund manager 
on behalf of its sub-funds, which are all independent third parties. To the best knowledge of Bosera AM after due enquiry, each of the sub-funds and their respective ultimate 
beneficial owner holding 30% or more interest is an independent third party of Bosera AM and each of CMBI and CMS HK, and the companies which are members of the same 
group of companies as each of CMBI and CMS HK.
Name of the sub-funds to which the Offer Shares will be allocated
Whether any investor holds 
30% or more interests in the 
sub-fund (Y/N)
UBO name
Percentage shareholding 
Navigator Technology Limited IPO Mandate 
Y
Fuhua Zheng
100
*	
The account “Navigator Technology Limited IPO Mandate” is not a SFC authorized fund. It is a segregated mandate that primarily invests in equities.
6.	
Fullgoal Fund will hold the Offer Shares in its capacity as the discretionary fund manager managing the fund on behalf of their investors (the “Fullgoal Fund Ultimate Client”), 
each of which is, to the best knowledge of Fullgoal Fund, (i) an independent third party of the Company, its subsidiaries, its substantial shareholders, Fullgoal Fund, GTJA 
Securities, Haitong Securities and the companies which are members of the same group of companies as GTJA Securities, Haitong Securities and Fullgoal Fund; and (ii) a 
collective investment scheme which is not authorized by the SFC. No ultimate beneficial owner holds 30% or more interest in the fund.
The details of the Fullgoal Fund Ultimate Client is as follows:
Fund Name
Whether the Scheme is 
Publicly Marketed
Fund Manager
UBO of Fund 
Manager
UBO of the Fullgoal Fund 
Ultimate Client
ICBC Fullgoal China Small & Mid Cap 
(HK listed) Equity Fund
Yes
Fullgoal Fund
N/A
No single ultimate beneficial 
owner holds 30% or more 
interest
ICBC Fullgoal China Small & Mid Cap (HK listed) Equity Fund is the public offering of fund and invests in equity.

<<<PAGE 32>>>
32
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
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
investors should read the Prospectus dated June 29, 2026 issued by MOMENTA GLOBAL 
LIMITED for detailed information about the Global Offering described above before deciding 
whether or not to invest in the Offer Shares thereby being offered.
Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting 
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on  the Listing 
Date (which is currently expected to be on July 8, 2026).

<<<PAGE 33>>>
33
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering and before any exercise of the Over-
allotment Option, the total number of the Class A Ordinary Shares held by the public represents 
approximately 97.27% of the total number of issued Class A Ordinary Shares of the Company, 
which is higher than the prescribed percentage of Class A Ordinary Shares required to be held in 
public hands of 10% under Rule 8.08(1) of the Listing Rules calculated based on the Offer Price, 
thereby satisfying the public float requirement under Rule 8.08(1) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, Class A Ordinary Shares held by the Cornerstone Investors upon the Listing 
shall not be counted towards the free float of the Class A Ordinary Shares of the Company at the 
time of Listing. Based on the Offer Price, the Company satisfies the free float requirement under 
Rule 8.08A of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering and 
before any exercise of the Over-allotment Option, (i) no placee will, individually, be placed 
more than 10% of the enlarged issued share capital of the Company immediately after the Global 
Offering; (ii) there will not be any new substantial Shareholder immediately after the Global 
Offering; (iii) the three largest public shareholders of the Company do not hold more than 50% of 
the Class A Ordinary Shares in public hands at the time of the Listing in compliance with Rules 
8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at the time of 
the Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The Share certificates will only become valid evidence of title at 8:00 a.m. on July 8, 2026 
(Hong Kong time), provided that the Global Offering has become unconditional and the right of 
termination described in the section headed “Underwriting — Underwriting Arrangements and 
Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus has not 
been exercised. Investors who trade the Class A Ordinary Shares on the basis of publicly available 
allocation details prior to the receipt of Share certificates or prior to the Share certificates becoming 
valid evidence of title do so entirely at their own risk.

<<<PAGE 34>>>
34
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on July 8, 2026 
(Hong Kong time), it is expected that dealings in the Class A Ordinary Shares on the Stock 
Exchange will commence at 9:00 a.m. on July 8, 2026 (Hong Kong time). The Class A Ordinary 
Shares will be traded in board lots of 20 Class A Ordinary Shares each, and the stock code of the 
Class A Ordinary Shares will be 6880.
By order of the Board
MOMENTA GLOBAL LIMITED
Mr. CAO Xudong
Chairperson of the Board,  
Executive Director and  
Chief Executive Officer
Hong Kong, July 7, 2026
As of the date of this announcement, the Board comprises: (1) Mr. CAO Xudong, Dr. XIA Yan, Dr. SUN Gang, Ms. SUN Huan 
and Ms. AN Ren as executive Directors; (2) Mr. ZHANG Jianjun, Mr. WANG Glide Xiao Ou and Mr. Fabian Johannes THOMAS 
as non-executive Directors; and Mr. FENG Heping, Ms. WEI Yu, Mr. LI Dong and Mr. SHAO Yu as proposed independent non-
executive Directors.
