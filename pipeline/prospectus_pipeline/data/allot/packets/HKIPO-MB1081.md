# 配发结果公告抽取任务：1081.HK Dajin Heavy Industry Co., Ltd. - H Shares

- 公告：Announcement of Allotment Results
- 刊发时间（港交所元数据）：**04/06/2026 22:22**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0604/2026060402919.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1081.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated May 28, 2026 (the “Prospectus”) of Dajin Heavy Industry Co., Ltd. (大金重工股份有
限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for any securities. This announcement is not a prospectus. Potential investors should read the Prospectus 
for detailed information about the Global Offering before deciding whether or not to invest in the Offer Shares. Any 
investment decision in relation to the Offer Shares should be taken solely in reliance on the information provided in 
the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities in 
the United States or in any other jurisdictions. The Offer Shares have not been, and will not be, registered under the 
United States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or securities law of 
any state or other jurisdiction of the United States. The Offer Shares may not be offered, sold, pledged or otherwise 
transferred within the United States, except pursuant to an available exemption from, or in a transaction not subject to, 
the registration requirements of the U.S. Securities Act. There will be no public offer of the Offer Shares in the United 
States. The Offer Shares are being offered and sold solely outside the United States in offshore transactions in reliance 
on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, Huatai Financial Holdings (Hong Kong) Limited, as stabilizing manager 
(the “Stabilizing Manager”) (or any person acting for it), on behalf of the Underwriters, may over-allocate or effect 
transactions with a view to stabilizing or supporting the market price of the H Shares at a level higher than that which 
might otherwise prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing 
Manager (or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) 
will be conducted at the absolute discretion of the Stabilizing Manager (or any person acting for it) and in what the 
Stabilizing Manager reasonably regards as the best interest of the Company, (b) may be discontinued at any time and 
(c) is required to be brought to an end within 30 days after the last day for lodging applications under the Hong Kong 
Public Offering (which is Thursday, July 2, 2026). Such stabilizing action, if taken, may be effected in all jurisdictions 
where it is permissible to do so, in each case in compliance with all applicable laws, rules and regulatory requirements, 
including the Securities and Futures (Price Stabilizing) Rules (Chapter 571 W of the Laws of Hong Kong), as 
amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Thursday, July 2, 2026). 
After this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of 
the H Shares, could fall.
Potential investors of the Offer Shares should note that the Joint Sponsor-Overall Coordinators (for themselves and on 
behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong Underwriting Agreement with 
immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus at any time 
prior to 8:00 a.m. on the day that trading in the H Shares commences on the Stock Exchange.

<<<PAGE 2>>>
2
Dajin Heavy Industry Co., Ltd.
大金重工股份有限公司
(a joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares in 
the Global Offering
:
100,010,600 H Shares (taking into 
 account the full exercise of 
 the Offer Size Adjustment Option and
 subject to the Over-allotment Option)
Number of Hong Kong Offer Shares
:
8,696,600 H Shares
Number of International Offer Shares
:
91,314,000 H Shares (taking into account 
 the full exercise of the Offer Size 
 Adjustment Option and subject to the 
 Over-allotment Option)
Final Offer Price
:
HK$66.40 per H Share, plus brokerage 
 of 1.0%, SFC transaction levy of 
 0.0027%, AFRC transaction levy of 
 0.00015% and Stock Exchange trading 
 fee of 0.00565%
Nominal Value
:
RMB1.00 per H Share 
Stock Code
:
1081
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers
Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager

<<<PAGE 3>>>
3
Dajin Heavy Industry Co., Ltd.
大金重工股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated May 28, 2026 (the “Prospectus”) issued Dajin 
Heavy Industry Co., Ltd. (the “Company”).
SUMMARY
Company Information
Stock code
1081
Stock short name
DAJIN
Dealings commencement date
June 5, 2026*
* 
see note at the end of this announcement
Price Information
Final Offer Price
HK$66.40
Maximum Offer Price
HK$66.40
Offer Shares and Share Capital
Number of Offer Shares (taking into 
account the full exercise of the Offer Size 
Adjustment Option and before exercise of 
the Over-allotment Option)
100,010,600
Number of Offer Shares in Hong Kong 
Public Offering
8,696,600
Number of Offer Shares in International 
Offering (taking into account the full 
exercise of the Offer Size Adjustment Option 
and before exercise of the Over-allotment 
Option)
91,314,000
Number of issued Shares upon Listing 
(before exercise of the Over-allotment 
Option)
737,759,949

<<<PAGE 4>>>
4
Offer Size Adjustment Option (Upsize option)
Number of additional shares issued under 
the Offer Size Adjustment Option
13,044,800
– International Offering
13,044,800
The Offer Size Adjustment Option was exercised in full, pursuant to which the Company is 
issuing and allotting 13,044,800 additional Offer Shares, representing approximately 15.0% of 
the Offer Shares initially being offered under the Global Offering, at the Offer Price.
The additional Offer Shares issued pursuant to the Offer Size Adjustment Option will be 
allocated to the International Offering.
Over-allocation
Number of Offer Shares over-allocated
15,001,500
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$6,640.70 million
Less: Estimated listing expenses payable 
   based on Final Offer Price
HK$(175.22) million
Net proceeds
HK$6,465.48 million
Note: Gross proceeds refer to the amount which the Company is entitled to receive. For details of the use of proceeds, 
please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The Company will 
adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if any) for the purposes 
as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus on a pro rata basis.

<<<PAGE 5>>>
5
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
122,627
No. of successful applications
28,788
Subscription level
134.39 times
Claw-back triggered
N/A
No. of Offer Shares initially available under 
the Hong Kong Public Offering
8,696,600
No. of Offer Shares reallocated from the 
International Offering
0
Final no. of Offer Shares under the Hong 
Kong Public Offering
8,696,600
% of Offer Shares under the Hong Kong 
Public Offering to the Global Offering
8.70%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by identification number or www.hkeipo.hk/IPOResult for the 
full list of allottees.
INTERNATIONAL OFFERING
No. of placees
125
Subscription level (before taking into 
account the Offer Size Adjustment Option)
10.68 times
No. of Offer Shares initially available under 
the International Offering
78,269,200
No. of Offer Shares reallocated to the Hong 
Kong Public Offering
0
Final no. of Offer Shares under the 
International Offering (after taking into 
account the full exercise of the Offer Size 
Adjustment Option)
91,314,000
% of Offer Shares under the International 
Offering to the Global Offering (after taking 
into account the full exercise of the Offer 
Size Adjustment Option)
91.30%

<<<PAGE 6>>>
6
The Directors confirm that, to the best of their knowledge, information and belief, save for 
(a) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by 
the Stock Exchange to permit the Company to allocate certain Offer Shares in the International 
Offering to certain Existing Minority Shareholders and/or their close associates, (b) a consent 
under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants to permit the Company to allocate certain Offer Shares in the International Offering 
to connected clients, and (c) a consent under paragraph 18 of Chapter 4.15 of the Guide for 
New Listing Applicants to permit the Company to, among other things, allocate further Offer 
Shares in the International Offering to an existing Shareholder and/or its close associates and 
a Cornerstone Investor and/or its close associates, (i) none of the Offer Shares subscribed by 
the placees and the public have been financed directly or indirectly by the Company, any of the 
Directors, chief executive of the Company, Controlling Shareholders, substantial Shareholders, 
existing Shareholders of the Company or any of its subsidiaries or their respective close associates; 
and (ii) none of the placees and the public who have purchased the Offer Shares are accustomed 
to taking instructions from the Company, any of the Directors, chief executive of the Company, 
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company or any 
of its subsidiaries or their respective close associates in relation to the acquisition, disposal, voting 
or other disposition of H Shares registered in his/her/its name or otherwise held by him/her/it.
The places in the International Offering include the following:
Cornerstone Investors
Cornerstone Investors
No. of Offer 
Shares allocated
Approximate % 
of total issued H 
Shares after the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (1) (2)
Approximate % 
of total issued 
Shares after the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (2)
Existing 
shareholders 
or their close 
associates
GIC Private Limited (“GIC”)(3)
9,434,400
9.43%
1.28%
Yes
HHLRA and HIM
HHLR Advisors, Ltd. (“HHLRA”)(3)
2,948,200
2.95%
0.40%
No
Hillhouse Investment Management, 
Ltd. (“HIM”)
2,948,200
2.95%
0.40%
No
Subtotal
5,896,400
5.90%
0.80%
CPE Juniper Investment Limited 
(“CPE Juniper”)(3)
4,716,000
4.72%
0.64%
No
UBS Asset Management 
(Singapore) Ltd. (“UBS AM 
Singapore”)(3)
3,537,900
3.54%
0.48%
No

<<<PAGE 7>>>
7
Cornerstone Investors
No. of Offer 
Shares allocated
Approximate % 
of total issued H 
Shares after the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (1) (2)
Approximate % 
of total issued 
Shares after the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (2)
Existing 
shareholders 
or their close 
associates
Taikang Life Insurance Co., Ltd 
(“Taikang Life”)(3)
3,537,900
3.54%
0.48%
Yes
Eastspring
Eastspring Investments 
(Singapore) Limited 
(“Eastspring Singapore”)(3)
1,179,300
1.18%
0.16%
Yes
Eastspring Investments 
(Hong Kong) Limited 
(“Eastspring HK”)(3)
707,500
0.71%
0.10%
Yes
Subtotal
1,886,800
1.89%
0.26%
Pinpoint Asset Management 
Limited (“Pinpoint”)
3,537,900
3.54%
0.48%
Yes
ICBC Wealth Management Co., 
Ltd. (“ICBC Wealth”)
2,358,600
2.36%
0.32%
No
Marshall Wace Asia Limited 
(“MWAL”)
2,358,600
2.36%
0.32%
Yes
Integrated Core Strategies (Asia) 
Pte. Ltd. (“Millennium ICSA”)
2,358,600
2.36%
0.32%
Yes
PSBC Wealth Management Co., 
Ltd. (中郵理財有限責任公司) 
(“PSBC Wealth”)(3)
1,415,100
1.41%
0.19%
No
Fullgoal
Fullgoal Asset Management (HK) 
Limited (“Fullgoal HK”)(3)
448,100
0.45%
0.06%
Yes
Fullgoal Fund Management Co., 
Ltd. (“Fullgoal Fund”)(3)
731,100
0.73%
0.10%
Yes
Subtotal
1,179,200
1.18%
0.16%
Total
42,217,400
42.21%
5.72%

<<<PAGE 8>>>
8
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be 
issued under the Global Offering.
(2) 
Assuming the Over-allotment Option is not exercised.
(3) 
In addition to the Offer Shares subscribed for as Cornerstone Investors, GIC, HHLRA, CPE Juniper, UBS AM 
Singapore, Taikang Life, Eastspring Singapore, Eastspring HK, PSBC Wealth, Fullgoal HK, Fullgoal Fund and/
or their respective close associates were allocated further Offer Shares as placees in the International Offering. 
The number of Offer Shares as set out above only taking into account the Offer Shares allocated to them as 
Cornerstone Investors under the Global Offering. Please refer to the section headed “Allotment Results Details 
— International Offering — Allottees with Waivers/Consents Obtained” in this announcement for details. Only 
the Offer Shares subscribed for as Cornerstone Investors are subject to lock-up as indicated below. For details, 
please refer to the section headed “Lock-up Undertakings — Cornerstone Investors” in this announcement.
Allottees with Waivers/Consents Obtained
Investors
No. of Offer 
Shares allocated
Approximate % 
of total issued H 
Shares after the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (1) (2)
Approximate % 
of total issued 
Shares after the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (2)
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 
1C(2) of the Placing Guidelines in relation to subscription for H Shares by Existing Minority Shareholders holding 
1% or more of the issued share capital of the Company immediately prior to the completion of the Global Offering 
and/or their close associates (3)
Nil
Nil
Nil
Nil
Nil
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicant in relation to allocations to connected clients (4)
China Southern Asset Management 
Co., Ltd. (“Southern AM")
530,600
0.53%
0.07%
Connected client 
as a placee
Bosera Asset Management 
(International) Co., Limited 
(“Bosera”)
58,900
0.06%
0.01%
Connected client 
as a placee
China Merchants Fund Management 
Co., Ltd. (“CMFM”)
23,500
0.02%
0.003%
Connected client 
as a placee
CICC Financial Trading Limited 
(“CICC FT”)
2,000
0.002%
0.0003%
Connected client 
as a placee

<<<PAGE 9>>>
9
Investors
No. of Offer 
Shares allocated
Approximate % 
of total issued H 
Shares after the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (1) (2)
Approximate % 
of total issued 
Shares after the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (2)
Relationship
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocations of further H Shares to Cornerstone Investors (5)(6)
GIC
4,717,200
4.72%
0.64%
Same entity as 
the Cornerstone 
Investor
Eastspring Singapore
1,179,300
1.18%
0.16%
Same entity as 
the Cornerstone 
Investor
Eastspring HK
707,500
0.71%
0.10%
Same entity as 
the Cornerstone 
Investor
Taikang Life
707,500
0.71%
0.10%
Same entity as 
the Cornerstone 
Investor
Fullgoal Fund
29,400
0.03%
0.004%
Same entity as 
the Cornerstone 
Investor
Fullgoal HK
88,400
0.09%
0.01%
Same entity as 
the Cornerstone 
Investor
HHLRA
5,896,500
5.90%
0.80%
Same entity as 
the Cornerstone 
Investor
CPE Juniper 
4,599,300
4.60%
0.62%
Same entity as 
the Cornerstone 
Investor

<<<PAGE 10>>>
10
Investors
No. of Offer 
Shares allocated
Approximate % 
of total issued H 
Shares after the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (1) (2)
Approximate % 
of total issued 
Shares after the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (2)
Relationship
China Galaxy International 
Investment Company Limited 
(中國銀河國際投資有限公司)
(“CGII”)
1,533,000
1.53%
0.21%
To subscribe and 
hold the Offer 
Shares for close 
associates of 
a Cornerstone 
Investor (7)
UBS AM Singapore
5,306,800
5.31%
0.72%
Same entity as 
the Cornerstone 
Investor
PSBC Wealth
235,700
0.24%
0.03%
Same entity as 
the Cornerstone 
Investor
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be 
issued under the Global Offering.
(2) 
Assuming the Over-allotment Option is not exercised.
(3) 
Among the Cornerstone Investors, GIC, Taikang Life, Eastspring Singapore, Eastspring HK, Pinpoint, MWAL, 
Millennium ICSA, Fullgoal HK and Fullgoal Fund are Existing Minority Shareholders or their close associate, 
none of which holds more than 1% of the total issued share capital of the Company immediately prior to the 
completion of the Global Offering. The Stock Exchange has granted a waiver from strict compliance with 
the requirements under Rule 10.04 of the Listing Rules and paragraph 1(C)(2) of the Placing Guidelines to 
permit the Company to allocate certain Offer Shares in the International Offering to certain Existing Minority 
Shareholders and/or their close associates. Please refer to the section headed “Waiver – Allocation of H Shares 
to Existing Minority Shareholders and Their Close Associates” of the Prospectus and the section headed “Others/
Additional Information – Allocation of H Shares to Existing Minority Shareholders and their close associates” 
in this announcement for details.
The Stock Exchange has granted the waiver on the condition that, among other things, details of allocation 
to the Existing Minority Shareholders holding more than 1% of the total issued share capital of the Company 
immediately prior to the completion of the Global Offering and/or their close associates will be disclosed in the 
Prospectus and/or allotment results announcement.
(4) 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for 
New Listing Applicant in relation to allocations to connected clients, please refer to the section headed “Others/
Additional Information – Placing to connected clients with consent under paragraph 1C(1) of the Placing 
Guidelines” in this announcement.

<<<PAGE 11>>>
11
(5) 
For details of the consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in 
relation to allocations of further H Shares to Cornerstone Investors, please refer to the section headed “Others/
Additional Information – Allocations of Offer Shares to the Cornerstone Investors with consent under paragraph 
18 of Chapter 4.15 of the Guide for New Listing Applicants” in this announcement.
(6) 
The number of Offer Shares allocated to the relevant investors only represents the number of Offer Shares 
allocated to the investors as placees in the International Offering. For allocation of Offer Shares to the relevant 
investors as Cornerstone Investors, please refer to the section headed “Allotment Results Details – International 
Offer – Cornerstone Investors” in this announcement.
(7) 
CGII will hold the Offer Shares on a non-discretionary basis under a series of swaps transactions with, its 
ultimate client, namely, Yuanfeng Hongyu Private Securities Investment Fund (源峰泓聿私募證券投資基金) 
and Yuanfeng Yuanjing Growth Private Securities Investment Fund (源峰遠景成長私募證券投資基金), both 
being close associate of CPE Juniper, one of the Cornerstone Investors
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
Approximate 
% of total 
issued H Shares 
subject to lock-
up undertakings 
upon Listing 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (1) (2)
Approximate 
% of total 
issued Shares 
subject to lock-
up undertakings 
upon Listing 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (2)
Last day subject to the 
lock-up undertakings (3)
Mr. Jin
7,745,625 
A Shares
–
1.05%
December 4, 2026 (First 
Six-Month Period) (4)
June 4, 2027 (Second Six-
Month Period) (5)
Jinyin Energy
248,300,500 
A Shares
–
33.66%
December 4, 2026 (First 
Six-Month Period) (4)
June 4, 2027 (Second Six-
Month Period) (5)
Total
256,046,125
 A Shares
–
34.71%
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be 
issued under the Global Offering.
(2) 
Assuming the Over-allotment Option is not exercised.
(3) 
In accordance with the applicable Listing Rules, the required lock-up for the First Six-Month Period will end on 
December 4, 2026 and for the Second Six-Month Period will end on June 4, 2027.
(4) 
Each member of the Controlling Shareholders may dispose or transfer Shares after the indicated date subject to 
that any member of the Controlling Shareholders will not cease to be a controlling shareholder (as defined in the 
Listing Rules) of the Company.
(5) 
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after the 
indicated date.

<<<PAGE 12>>>
12
Cornerstone Investors
Name
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
Approximate 
% of total 
issued H Shares 
subject to lock-
up undertakings 
upon Listing (after 
taking into account 
the full exercise 
of the Offer 
Size Adjustment 
Option) (1) (2)
Approximate % of 
total issued Shares 
subject to lock-
up undertakings 
upon Listing (after 
taking into account 
the full exercise 
of the Offer 
Size Adjustment 
Option) (2)
Last day subject 
to the lock-up 
undertakings (3)
GIC
9,434,400
9.43%
1.28%
December 4, 2026
HHLRA
2,948,200
2.95%
0.40%
December 4, 2026
HIM
2,948,200
2.95%
0.40%
December 4, 2026
CPE Juniper
4,716,000
4.72%
0.64%
December 4, 2026
UBS AM Singapore
3,537,900
3.54%
0.48%
December 4, 2026
Taikang Life
3,537,900
3.54%
0.48%
December 4, 2026
Eastspring Singapore
1,179,300
1.18%
0.16%
December 4, 2026
Eastspring HK
707,500
0.71%
0.10%
December 4, 2026
Pinpoint
3,537,900
3.54%
0.48%
December 4, 2026
ICBC Wealth
2,358,600
2.36%
0.32%
December 4, 2026
MWAL
2,358,600
2.36%
0.32%
December 4, 2026
Millennium ICSA
2,358,600
2.36%
0.32%
December 4, 2026
PSBC Wealth
1,415,100
1.41%
0.19%
December 4, 2026
Fullgoal HK
448,100
0.45%
0.06%
December 4, 2026
Fullgoal Fund
731,100
0.73%
0.10%
December 4, 2026
Total
42,217,400
42.21%
5.72%
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be 
issued under the Global Offering.
(2) 
Assuming the Over-allotment Option is not exercised.
(3) 
In accordance with the respective cornerstone investment agreements, the required lock-up periods will end on 
December 4, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or transferring the 
Shares subscribed for pursuant to their respective cornerstone investment agreements after the indicated date.

<<<PAGE 13>>>
13
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
exercise of 
the
Over-
allotment
Option)
Allotment
as % of
International
Offering
(assuming the
Over-
allotment
Option is
exercised and
new H Shares
are issued)
Allotment
as % of
total Offer
Shares
(assuming no
exercise of 
the
Over-
allotment
Option)
Allotment
as % of
total Offer
Shares
(assuming the
Over-
allotment
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
exercise of 
the
Over-
allotment
Option)
% of total
issued share
capital upon
Listing
(assuming the
Over-
allotment
Option is
exercised and
new H Shares
are issued)
Top 1
14,151,600
15.50%
13.31%
14.15%
12.30%
14,151,600
1.92%
1.88%
Top 5
49,882,900
54.63%
46.92%
49.88%
43.37%
49,882,900
6.76%
6.63%
Top 10
68,279,600
74.77%
64.22%
68.27%
59.37%
68,279,600
9.25%
9.07%
Top 25
96,286,800
105.45%
90.57%
96.28%
83.72%
96,286,800
13.05%
12.79%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDER CONCENTRATION ANALYSIS
H 
Shareholders*
Number of
H Shares
allotted
Allotment
as % of
International
Offering
(assuming no
exercise of 
the
Over-
allotment
Option)
Allotment
as % of
International
Offering
(assuming 
the
Over-
allotment
Option is
exercised 
and
new H 
Shares
are issued)
Allotment
as % of
total Offer
Shares
(assuming no
exercise of 
the
Over-
allotment
Option)
Allotment
as % of
total Offer
Shares
(assuming 
the
Over-
allotment
Option is
exercised 
and
new H 
Shares
are issued)
Number of
H Shares 
held
upon Listing
% of total
issued share
capital upon
Listing
(assuming no
exercise of 
the
Over-
allotment
Option)
% of total
issued share
capital upon
Listing
(assuming 
the
Over-
allotment
Option is
exercised 
and
new H 
Shares
are issued)
Number of 
Shares 
held upon 
Listing
Top 1
14,151,600
15.50%
13.31%
14.15%
12.30%
14,151,600
1.92%
1.88%
16,020,853
Top 5
49,882,900
54.63%
46.92%
49.88%
43.37%
49,882,900
6.76%
6.63%
57,141,166
Top 10
68,279,600
74.77%
64.22%
68.27%
59.37%
68,279,600
9.25%
9.07%
75,559,966
Top 25
96,286,800
105.45%
90.57%
96.28%
83.72%
96,286,800
13.05%
12.79%
109,879,497
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 14>>>
14
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number of
H Shares
allotted
Allotment
as % of
International
Offering
(assuming no
exercise of 
the
Over-
allotment
Option)
Allotment
as % of
International
Offering
(assuming 
the
Over-
allotment
Option is
exercised 
and
new H 
Shares
are issued)
Allotment
as % of
total Offer
Shares
(assuming no
exercise of 
the
Over-
allotment
Option)
Allotment
as % of
total Offer
Shares
(assuming 
the
Over-
allotment
Option is
exercised 
and
new H 
Shares
are issued)
Number of
H Shares 
held
upon Listing
Number of
Shares held
upon Listing
% of total
issued share
capital upon
Listing
(assuming no
exercise of 
the
Over-
allotment
Option)
% of total
issued share
capital upon
Listing
(assuming 
the
Over-
allotment
Option is
exercised 
and
new H 
Shares
are issued)
Top 1
0
0.00%
0.00%
0.00%
0.00%
0
256,046,125
34.71%
34.01%
Top 5
36,792,800
40.29%
34.61%
36.79%
31.99%
36,792,800
333,011,363
45.14%
44.24%
Top 10
57,784,000
63.28%
54.35%
57.78%
50.24%
57,784,000
364,161,627
49.36%
48.38%
Top 25
85,969,000
94.15%
80.86%
85.96%
74.75%
85,969,000
418,621,623
56.74%
55.61%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon 
Listing.
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, 122,627 valid applications 
made by the public will be conditionally allocated on the basis set out below:

<<<PAGE 15>>>
15
NO. OF H 
SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL NO. 
OF H SHARES 
APPLIED FOR
POOL A
100
56,672
1,701 out of 56,672 applicants to receive 100 H Shares
3.00%
200
8,402
451 out of 8,402 applicants to receive 100 H Shares
2.68%
300
4,380
330 out of 4,380 applicants to receive 100 H Shares
2.51%
400
2,710
260 out of 2,710 applicants to receive 100 H Shares
2.40%
500
3,477
402 out of 3,477 applicants to receive 100 H Shares
2.31%
600
2,115
285 out of 2,115 applicants to receive 100 H Shares
2.25%
700
6,016
922 out of 6,016 applicants to receive 100 H Shares
2.19%
800
1,521
261 out of 1,521 applicants to receive 100 H Shares
2.14%
900
1,696
321 out of 1,696 applicants to receive 100 H Shares
2.10%
1,000
7,841
1,619 out of 7,841 applicants to receive 100 H Shares
2.06%
1,500
2,692
781 out of 2,692 applicants to receive 100 H Shares
1.93%
2,000
2,006
741 out of 2,006 applicants to receive 100 H Shares
1.85%
2,500
1,332
593 out of 1,332 applicants to receive 100 H Shares
1.78%
3,000
1,404
736 out of 1,404 applicants to receive 100 H Shares
1.75%
3,500
753
458 out of 753 applicants to receive 100 H Shares
1.74%
4,000
895
619 out of 895 applicants to receive 100 H Shares
1.73%
4,500
807
624 out of 807 applicants to receive 100 H Shares
1.72%
5,000
1,445
1,221 out of 1,445 applicants to receive 100 H Shares
1.69%
6,000
975
100 H Shares
1.67%
7,000
946
100 H Shares plus 35 out of 946 applicants to receive an 
additional 100 H Shares
1.48%
8,000
825
100 H Shares plus 139 out of 825 applicants to receive 
an additional 100 H Shares
1.46%
9,000
731
100 H Shares plus 210 out of 731 applicants to receive 
an additional 100 H Shares
1.43%
10,000
3,942
100 H Shares plus 1,545 out of 3,942 applicants to 
receive an additional 100 H Shares
1.39%
20,000
1,686
200 H Shares plus 897 out of 1,686 applicants to receive 
an additional 100 H Shares
1.27%
30,000
1,034
300 H Shares plus 566 out of 1,034 applicants to receive 
an additional 100 H Shares
1.18%

<<<PAGE 16>>>
16
NO. OF H 
SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL NO. 
OF H SHARES 
APPLIED FOR
40,000
716
400 H Shares plus 373 out of 716 applicants to receive 
an additional 100 H Shares
1.13%
50,000
632
500 H Shares plus 285 out of 632 applicants to receive 
an additional 100 H Shares
1.09%
60,000
405
600 H Shares plus 146 out of 405 applicants to receive 
an additional 100 H Shares
1.06%
70,000
640
700 H Shares plus 135 out of 640 applicants to receive 
an additional 100 H Shares
1.03%
Total
118,696
Total number of Pool A successful applicants: 24,857
POOL B
80,000
1,348
800 H Shares
1.00%
90,000
332
800 H Shares plus 158 out of 332 applicants to receive 
an additional 100 H Shares
0.94%
100,000
1,238
800 H Shares plus 1,142 out of 1,238 applicants to 
receive an additional 100 H Shares
0.89%
200,000
420
1,100 H Shares plus 252 out of 420 applicants to receive 
an additional 100 H Shares
0.58%
300,000
186
1,400 H Shares plus 30 out of 186 applicants to receive 
an additional 100 H Shares
0.47%
400,000
102
1,700 H Shares
0.43%
500,000
71
2,000 H Shares
0.40%
600,000
32
2,300 H Shares
0.38%
700,000
23
2,600 H Shares
0.37%
800,000
21
2,900 H Shares
0.36%
900,000
18
3,200 H Shares
0.36%
1,000,000
69
3,500 H Shares
0.35%
2,000,000
23
4,000 H Shares
0.20%
3,000,000
15
4,500 H Shares
0.15%
4,348,300
33
5,000 H Shares
0.11%
Total
3,931
Total number of Pool B successful applicants: 3,931
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 17>>>
17
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or 
indirectly, provided by the Company, the Controlling Shareholders, Directors or syndicate 
members to any placees or the public (as the case may be) and the consideration payable by them 
for each Share of the Company subscribed for or purchased by them is the same as the final Offer 
Price in addition to any brokerage, AFRC transaction levy, SFC transaction levy and trading fee 
payable.
OTHERS/ADDITIONAL INFORMATION
Offer Size Adjustment Option
The Offer Size Adjustment Option has been exercised in full, pursuant to which the Company 
is issuing and allotting 13,044,800 additional Offer Shares, representing approximately 15.0% 
of the Offer Shares initially being offered under the Global Offering, at the Offer Price. All of 
the additional Offer Shares that would be allotted and issued by the Company pursuant to the 
Offer Size Adjustment Option will be allocated to the International Offering. Accordingly, the 
total number of Offer Shares finally available under the Global Offering (taking into account the 
full exercise of the Offer Size Adjustment Option and before any exercise of the Over-allotment 
Option) will be 100,010,600 Shares.
Allocation of H Shares to Existing Minority Shareholders and their close associates
The Company applied to the Stock Exchange for, and the Stock Exchange has granted, a waiver 
from strict compliance with the requirements under Rule 10.04 and consent under Paragraph 
1C(2) of the Placing Guidelines to permit the Company to allocate certain Offer Shares in the 
International Offering to certain Existing Minority Shareholders and/or their close associates. Such 
allocations of Offer Shares are in compliance with all the conditions under the waiver/consent 
granted by the Stock Exchange.
Please refer to the section headed “Waivers – Allocation of H Shares to Existing Minority 
Shareholders and their Closing Associates” in the Prospectus for further details of the waiver and 
consent.
For details of the allocations of Offer Shares to the Existing Minority Shareholders and/or their 
close associates, please refer to the section headed “Allotment Results Details – International 
Offering – Allottees with Waiver/Consents Obtained” in this announcement.
Placing to connected clients with consent under paragraph 1C(1) of the Placing Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines. Details of the placement to connected 
clients are set out below. The Company has applied to the Stock Exchange for, and the Stock 
Exchange has granted, a consent under paragraph 1C(1) of the Placing Guidelines to permit the 
Company to allocate such Offer Shares in the International Offering to the connected clients. The 
allocation of Offer Shares to such connected clients is in compliance with all the conditions under 
the consent granted by the Stock Exchange.

<<<PAGE 18>>>
18
Part A – Connected Clients holding the beneficial interest of the Offer Shares on a 
non-discretionary basis on behalf of independent third parties
No.
Connected Distributor
Connected 
Client
Relationship with the 
Connected Distributor
Whether the 
Connected
Client is a 
collective 
Investment 
scheme 
which is not 
authorised by 
the SFC or is 
expected to 
hold the Offer 
Shares on 
behalf of
such scheme
Number of
Offer Shares to
be allocated to
the connected
client
Appropriate
percentage of 
total
number of 
Offer
Shares (taking 
into account 
the full
exercise of the 
Offer Size 
Adjustment
Option) (1)(2)
Approximate
percentage of 
total
issued share 
capital
in the 
Company
upon Listing 
(taking
into account 
the full 
exercise of the 
Offer Size
Adjustment 
Option) (2)
1.
China International
Capital Corporation
Hong Kong Securities
Limited (“CICC”)
CICC FT (3)
CICC FT is a member 
of the same group of 
companies as CICC.
No
2,000
0.002%
0.0003%
Part B – Connected Clients holding the beneficial interest of the Offer Shares on a 
discretionary basis on behalf of independent third parties
No.
Connected Distributor
Connected 
Client
Relationship with the 
Connected Distributor
Whether the 
Connected
Client is a 
collective 
Investment 
scheme 
which is not 
authorised by 
the SFC or is 
expected to 
hold the Offer 
Shares on 
behalf of
such scheme
Number of
Offer Shares to
be allocated to
the connected
client
Appropriate
percentage of 
total
number of 
Offer
Shares (taking 
into account 
the full
exercise of the 
Offer Size 
Adjustment
Option) (1)(2)
Approximate
percentage of 
total
issued share 
capital
in the 
Company
upon Listing 
(taking
into account 
the full 
exercise of the 
Offer Size
Adjustment 
Option) (2)
2.
Huatai Financial
Holdings (Hong Kong)
Limited (“Huatai”)
Southern 
AM (4)
Southern AM is a member 
of the same group of 
companies as Huatai
No
530,600
0.53%
0.07%

<<<PAGE 19>>>
19
No.
Connected Distributor
Connected 
Client
Relationship with the 
Connected Distributor
Whether the 
Connected
Client is a 
collective 
Investment 
scheme 
which is not 
authorised by 
the SFC or is 
expected to 
hold the Offer 
Shares on 
behalf of
such scheme
Number of
Offer Shares to
be allocated to
the connected
client
Appropriate
percentage of 
total
number of 
Offer
Shares (taking 
into account 
the full
exercise of the 
Offer Size 
Adjustment
Option) (1)(2)
Approximate
percentage of 
total
issued share 
capital
in the 
Company
upon Listing 
(taking
into account 
the full 
exercise of the 
Offer Size
Adjustment 
Option) (2)
3.
China Merchants
Securities (HK) Co.,
Limited (“CMS”)
Bosera (5)
Bosera is a member of the 
same group of companies 
as CMS
Yes
58,900
0.06%
0.01%
4.
CMS
CMFM (6)
CMFM is a member of the 
same group of companies 
as CMS
No
23,500
0.02%
0.003%
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be 
issued under the Global Offering.
(2) 
Assuming the Over-allotment Option is not exercised.
(3) 
CICC FT will hold the Offer Shares in its capacity as the non-discretionary fund manager on behalf of its 
following client. Such client is, to the best knowledge and belief of CICC FT, an independent third party of the 
Company, its subsidiaries, its substantial shareholders, CICC and the companies which are members of the same 
group of CICC.
Name of whom the Offer Shares will be allocated
Whether any 
investor holds 30% 
or more interest in 
the fund
Ultimate Beneficial 
Owner with 30% or 
more interests and 
Shareholding (%)
Shanghai Minghong Investment Management Co.,Ltd. as the 
manager on behalf of Minghong No. 1 Multi-strategy Hedging 
Fund
No
N/A
(4) 
Southern AM will hold the Offer Shares in its capacity as the discretionary manager on behalf of its following 
clients. Each of such clients is, to the best knowledge and belief of Southern AM, an independent third party of 
the Company, its subsidiaries, its substantial shareholders, Huatai and the companies which are members of the 
same group of Huatai.

<<<PAGE 20>>>
20
Name of whom the Offer Shares will be allocated
Whether any investor 
holds 30% or more 
interest in the fund
Ultimate Beneficial 
Owner with 30% or 
more interests and 
Shareholding (%)
China Southern International Select Allocation Fund
No
N/A
China Southern Hong Kong Preference Equity Fund
No
N/A
China Southern Hong Kong Growth Dynamic Allocation Hybrid 
Fund
No
N/A
China Southern China Emerging Economics Nine Months Holding 
Period Hybrid Fund
No
N/A
(5) 
Bosera will hold the Offer Shares in its capacity as the discretionary fund manager managing the sub-funds 
on behalf of its following clients. Each of such clients, and its respective ultimate beneficial owner(s) with 
30% interest, is, to the best knowledge and belief of Bosera, an independent third party of the Company, its 
subsidiaries, its substantial shareholders, CMS and the companies which are members of the same group of 
CMS.
Name of whom the Offer Shares will be allocated
Whether any investor 
holds 30% or more 
interest in the fund
Ultimate Beneficial Owner 
with 30% or more interests 
and Shareholding (%)
Navigator Technology Limited IPO Mandate
Yes
Zheng Fuhua (鄭複花): 100%
Fortuna Capital Management Limited IPO Mandate
Yes
Yang Dehui (楊德會): 100%
(6) 
CMFM will hold the Offer Shares in its capacity as the discretionary manager on behalf of its following client. 
Such client is, to the best knowledge and belief of CMFM, an independent third party of the Company, its 
subsidiaries, its substantial shareholders, CMS and the companies which are members of the same group of 
CMS.
Name of whom to which the Offer Shares will be allocated
Whether any 
investor holds 30% 
or more interest in 
the fund
Ultimate Beneficial 
Owner with 30% or 
more interests and 
Shareholding (%)
CMF PUSHENG GLOBAL ALLOCATION FUND – 007729
No
N/A
Allocations of Offer Shares to the Cornerstone Investors with consent under paragraph 18 of 
Chapter 4.15 of the Guide for New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 
of the Guide for New Listing Applicants to permit the Company to allocate further Offer Shares 
in the International Offering to certain Cornerstone Investors as placees, subject to the following 
conditions (the “Allocation to Double-Dipping Shareholder Participants”):
(a) the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;
(b) 
the Offer Shares allocated to all existing Shareholders and their close associates (whether 
as cornerstone investors and/or as placees) as permitted under this exemption do not exceed 
30% of the total number of Offer Shares;

<<<PAGE 21>>>
21
(c) 
each Director, chief executive and Controlling Shareholder of the Company has confirmed 
that no Offer Shares have been allocated to them or their respective close associates under 
this exemption;
(d) 
the Allocation to Double-Dipping Shareholder Participants will not affect the Company’s 
ability to satisfy its public float requirement as prescribed by the Stock Exchange under the 
waiver from strict compliance with the requirements of Rules 8.08(1)(b) and 19A.13A of the 
Listing Rules; and
(e) 
details of the allocation to the Cornerstone Investors under this exemption will be disclosed 
in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the further allocations of Offer Shares to Cornerstone Investors, please refer to 
the section headed “Allotment Results Details – International Offering – Allottees with Waivers/
Consents Obtained” in this announcement.
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for any securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated May 28, 2026 for detailed information about 
the Global Offering before deciding whether or not to invest in the Offer Shares. Any investment 
decision in relation to the Offer Shares should be taken solely in reliance on the information 
provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer or 
solicitation to purchase or subscribe for securities in the United States or in any other jurisdictions. 
The Offer Shares have not been, and will not be, registered under the United States Securities Act 
of 1933 as amended from time to time (the “U.S. Securities Act”) or securities law of any state 
or other jurisdiction of the United States. The Offer Shares may not be offered, sold, pledged or 
otherwise transferred within the United States, except pursuant to an available exemption from, or 
in a transaction not subject to, the registration requirements of the U.S. Securities Act. There will 
be no public offer of the Offer Shares in the United States. The Offer Shares are being offered and 
sold solely outside the United States in offshore transactions in reliance on Regulation S under the 
U.S. Securities Act.

<<<PAGE 22>>>
22
* Potential investors of the Offer Shares should note that the Joint Sponsor-Overall Coordinators 
(for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the 
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the 
events set out in the section headed “Underwriting – Underwriting Arrangements and Expenses – 
Hong Kong Public Offering – Grounds for Termination” in the Prospectus at any time prior to 8:00 
a.m. on the day that trading in the H Shares commences on the Stock Exchange.
PUBLIC FLOAT AND FREE FLOAT
Rule 19A.13A(2) of the Listing Rules provides that, where a new applicant is a PRC issuer with 
other listed shares at the time of Listing, this will normally mean that the portion of H shares for 
which Listing is sought that are held by the public, at the time of Listing, must (a) represent at least 
10% of the issuer’s total number of issued shares in the class to which H shares belong (excluding 
treasury shares); or (b) have an expected market value of not less than HK$3,000,000,000. The 
A Shares of the Company are listed on the Shenzhen Stock Exchange. So far as the Directors 
are aware, all H Shares to be issued pursuant to the Global Offering, representing approximately 
13.56% of the total issued share capital immediately upon Listing (excluding the treasury shares), 
are expected to be held by the public, which is higher than the prescribed percentage of H Shares 
required to be held in public hands of 10% under Rule 19A.13A(2)(a) of the Listing Rules, thereby 
satisfying Rule 19A.13A(2) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the H Shares of the Company at the time of Listing. Based on the 
final Offer Price of HK$66.40 per H Share, the Company satisfies the free float requirement under 
Rule 19A.13C(2) of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public shareholders of 
the Company do not hold more than 50% of the H shares in public hands at the time of the Listing 
in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 
Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. (Hong Kong time) 
on Friday, June 5, 2026, provided that the Global Offering has become unconditional and the right 
of termination described in the section headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Grounds for termination” in the Prospectus has not been 
exercised. Investors who trade H Shares prior to the receipt of H Share certificates or the H Share 
certificates becoming valid evidence of title do so entirely at their own risk.

<<<PAGE 23>>>
23
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong Kong 
time) on Friday, June 5, 2026, it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Friday, June 5, 2026. The H Shares will be traded in board lots of 
100 Shares each. The stock code of the Shares is 1081.
By Order of the Board
Dajin Heavy Industry Co., Ltd.
Mr. JIN Xin
Executive Director and Chairman of the Board
Hong Kong, June 4, 2026
As of the date of this announcement, the board of directors of the Company comprises: (i) Mr. JIN 
Xin, Mr. SUN Xiaole, Ms. LIU Aihua, Mr. LI Xin and Mr. JIANG Haitao as executive directors; 
and (ii) Mr. CAI Meng, Mr. QU Guangjie, Ms. ZHANG Wei and Ms. LU Qiannan as independent 
non-executive directors.
