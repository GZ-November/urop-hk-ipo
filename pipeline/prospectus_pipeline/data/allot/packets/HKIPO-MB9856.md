# 配发结果公告抽取任务：9856.HK Ligent Technologies, Inc.

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**21/09/2026 21:13**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0921/2026092101567.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"9856.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
within the United States, except in transactions exempt from, or not subject to, the registration requirements of the 
U.S. Securities Act and in compliance with any applicable state securities laws. There will be no public offer of the 
Offer Shares in the United States. The Offer Shares are being offered and sold solely (1) to qualified institutional 
buyers as defined in Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under the U.S. 
Securities Act; and (2) outside the United States in offshore transactions in reliance on Regulation S under the U.S. 
Securities Act and applicable laws of each jurisdiction where those offers and sales occur.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
September 14, 2026 (the “Prospectus”) issued by Ligent Technologies, Inc. (納真科技公司) (the “Company”) for 
detailed information about the Global Offering described below before deciding whether or not to invest in the Shares 
thereby being offered. Any investment decision in relation to the Offer Shares should be taken solely in reliance on the 
information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
In connection with the Global Offering, CLSA Limited, as stabilizing manager (the “Stabilizing Manager”) (or its 
affiliates or any person acting for it), on behalf of the Underwriters, to the extent permitted by the applicable laws and 
regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect transactions with a view to stabilizing 
or supporting the market price of the Shares at such price, in such amounts and in such manners as the Stabilizing 
Manager, its affiliates or any person acting for it may determine and at a level higher than that which might otherwise 
prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing Manager (or its 
affiliates or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will 
be conducted at the absolute discretion of the Stabilizing Manager (or its affiliates or any person acting for it) and in 
what the Stabilizing Manager reasonably regards as the best interest of our Company, (b) may be discontinued at any 
time and (c) is required to be brought to an end within 30 days of the last day for lodging applications under the Hong 
Kong Public Offering (which is Saturday, October 17, 2026). Such stabilizing action, if taken, may be effected in all 
jurisdictions where it is permissible to do so, in each case in compliance with all applicable laws, rules and regulatory 
requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 571 W of the Laws of Hong 
Kong), as amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the Shares for longer 
than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day after the 
last day for lodging applications under the Hong Kong Public Offering (which is Saturday, October 17, 2026). After 
this date, when no further stabilizing action may be taken, demand for the Shares, and therefore the price of the Shares, 
could fall.
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on behalf of 
the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
Tuesday, September 22, 2026).

<<<PAGE 2>>>
2
Ligent Technologies, Inc.
納真科技公司
(Registered by way of continuation in the Cayman Islands with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the 
Global Offering
:
172,014,700 Shares (subject to the 
 Over-allotment Option)
Number of Hong Kong Offer Shares
:
17,201,500 Shares
Number of International Offer Shares
:
154,813,200 Shares (subject to 
 the Over-allotment Option)
Offer Price
:
HK$32.96 per Share, plus brokerage of 
 1.0%, SFC transaction levy of 0.0027%, 
 AFRC transaction levy of 0.00015% and 
 Stock Exchange trading fee of 0.00565%
Nominal Value
:
US$0.02 per Share
Stock Code
:
9856
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators,
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
LIGENT TECHNOLOGIES, INC.
納真科技公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated September 14, 2026 (the “Prospectus”) issued 
by Ligent Technologies, Inc. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the Shares could 
move substantially even with a small number of Shares traded and should exercise extreme 
caution when dealing in the Shares.
SUMMARY
Company information
Stock code
9856
Stock short name
LIGENT
Dealings commencement date
September 22, 2026#
# 
see note at the end of the announcement
Price Information
Offer Price
HK$32.96
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the Over-allotment 
Option)
172,014,700
Final Number of Offer Shares in Hong Kong Public Offering
17,201,500
Final Number of Offer Shares in International Offering (before 
exercise of the Over-allotment Option)
154,813,200
Number of issued Shares upon Listing (before exercise of the Over-
allotment Option)
982,941,500

<<<PAGE 4>>>
4
Over-allocation
No. of Offer Shares over-allocated
25,802,200
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$5,669.6 million
Less: Estimated listing expenses payable based on the Offer Price
HK$224.3 million
Net proceeds
HK$5,445.3 million
Note: Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
The Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
37,594
No. of successful applications
13,561
Subscription level
35.16 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong Public 
Offering
17,201,500
No. of Offer Shares reallocated from the International Offering
0
Final no. of Offer Shares under the Hong Kong Public Offering
17,201,500
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering (before the exercise of the Over-allotment Option)
10%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can 
refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
192
Subscription Level
4.67 times
No. of Offer Shares initially available under the International 
Offering
154,813,200
Final no. of Offer Shares under the International Offering
154,813,200
% of Offer Shares under the International Offering to the Global 
Offering (before the exercise of the Over-allotment Option)
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a 
waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit the Company to allocate certain Offer Shares in the International Offering to 
a close associate of the Minority Existing Shareholder; and (b) a consent under paragraph 18 of 
Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to, among other 
things, allocate further Shares in the International Offering to certain existing Shareholders and/
or their close associates and the Cornerstone Investors and/or their close associate (i) none of 
the Offer Shares subscribed by the placees and the public offer subscribers have been financed 
directly or indirectly by the Company, any of the Directors, chief executive of the Company, 
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company or 
any of its subsidiaries or their respective close associates; (ii) none of the placees and the public 
offer subscribers who have subscribed for or purchased the Offer Shares are accustomed to taking 
instructions from the Company, any of the Directors, chief executive of the Company, Controlling 
Shareholders, substantial Shareholders, existing Shareholders of the Company or any of its 
subsidiaries or their respective close associates in relation to the acquisition, disposal, voting or 
other disposition of Shares registered in his/her/its name or otherwise held by him/her/it; (iii) there 
is no side agreement or arrangement between the Company, any of the Directors, chief executive 
of the Company, the Controlling Shareholders, substantial Shareholders, existing Shareholders of 
the Company or any of its subsidiaries or their respective close associates, on one hand, and the 
public offer subscribers or the placees who have subscribed for or purchased the Offer Shares, on 
the other hand; (iv) there is no side agreement or arrangement between the Company, any of the 
Directors, chief executive of the Company, the Controlling Shareholders, substantial Shareholders, 
existing Shareholders of the Company or any of its subsidiaries or their respective close associates, 
on one hand, and any other parties, on the other hand, in connection with the subscription, 
purchase, disposal or valuation of the Shares (which, for the avoidance of doubt, does not include 
agreements entered into with the price stabilising managers); and (v) no rebate has been, directly 
or indirectly, provided by the Company, any of the Directors, chief executive of the Company, the 
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company or any 
of its subsidiaries or their respective close associates, or syndicate members, or any other brokers 
involved in the Global Offering, to any investors in the Hong Kong Public Offering or placees in 
the International Offering.

<<<PAGE 6>>>
6
The placees in the International Offering include the following:
Cornerstone Investors
Investor(1)
No. of Offer 
Shares 
allocated(2)
% of total 
number 
of Offer 
Shares(3)
% of total 
issued share 
capital in the 
Company 
after the 
Global 
Offering(3)(4)
Existing 
Shareholders 
or their close 
associates
Primavera Investment Fund
7,136,300
4.15%
0.73%
Yes(5)
GBAHIL
– Mega Prime
3,568,100
2.07%
0.36%
No
– Poly Platinum
3,568,100
2.07%
0.36%
No
Subtotal
7,136,200
4.14%
0.72%
CFTC Paragon SP
7,136,300
4.15%
0.73%
No
HK BVF I LPF
7,136,300
4.15%
0.73%
No
Orient Asset Management
3,568,100
2.07%
0.36%
No
Mount Altai
3,568,100
2.07%
0.36%
No
Peak View Capital
3,568,100
2.07%
0.36%
No
Sinofortune International
3,568,100
2.07%
0.36%
No
Ambre Lau Trade Limited
3,568,100
2.07%
0.36%
No
SCV Delta
2,378,700
1.38%
0.24%
No
Mirae Asset Securities HK
2,378,700
1.38%
0.24%
No
PAG Capital Structure
Opportunity Fund LP
2,378,700
1.38%
0.24%
No
Turquoise Hime (ORIX)
2,378,700
1.38%
0.24%
No
GF Fund(6)
– GF Fund Management
2,259,800
1.31%
0.23%
No
– GF Fund HK
118,900
0.07%
0.01%
No
Subtotal
2,378,700
1.38%
0.24%
E Fund(6)
– E Fund HK
2,259,800
1.31%
0.23%
No
– E Fund Management
118,900
0.07%
0.01%
No
Subtotal
2,378,700
1.38%
0.24%

<<<PAGE 7>>>
7
Investor(1)
No. of Offer 
Shares 
allocated(2)
% of total 
number 
of Offer 
Shares(3)
% of total 
issued share 
capital in the 
Company 
after the 
Global 
Offering(3)(4)
Existing 
Shareholders 
or their close 
associates
CSC OTC Swap
2,378,700
1.38%
0.24%
Yes(5)
First Seafront Asset 
Management Limited
2,378,700
1.38%
0.24%
No
GaoTeng Global Asset 
Management Limited
2,378,700
1.38%
0.24%
No
GigaDevice
2,378,700
1.38%
0.24%
No
Amlogic Hong Kong
2,378,700
1.38%
0.24%
No
Atlas Venture Limited
2,378,700
1.38%
0.24%
No
Alphahill Capital
2,378,700
1.38%
0.24%
No
ODI Trust
2,378,700
1.38%
0.24%
No
Barings
1,189,300
0.69%
0.12%
No
Total
80,876,700
47.02%
8.23%
Notes:
1. 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” of 
the Prospectus.
2. 
Only taking into account the Offer Shares allocated to the relevant investors as Cornerstone Investors 
under the Global Offering. In addition to the Offer Shares subscribed for as Cornerstone Investors, certain 
Cornerstone Investors and/or their respective close associates were allocated further Offer Shares as placees 
in the International Offering. Please refer to the section headed “Allotment Results Details – International 
Offering – Allotees with Waivers/Consents Obtained” in this announcement for details. Only the Offer Shares 
subscribed for as Cornerstone Investors are subject to lock-up as indicated below. For details, please refer to 
the section headed “Lock-up Undertakings – Cornerstone Investors” in this announcement.
3. 
Assuming the Over-allotment Option is not exercised.
4. 
The number of Shares immediately after the Global Offering is the same as the number of total issued Shares 
after the Global Offering.
5. 
For further details, please refer to the section headed “Cornerstone Investors” and “Waivers – Allocation of 
Offer Shares to Close Associates of Existing Shareholders as Cornerstone Investors” in the Prospectus. 
6. 
The allocation of Offer Shares to GF Fund Management, GF Fund HK, E Fund Management and E Fund 
HK is with consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to connected 
clients. For further details, please refer to the section headed “Cornerstone Investors” and “Waivers – Consent 
in respect of Proposed Subscription of Shares by certain Cornerstone Investor who are Connected Clients” of 
the Prospectus.

<<<PAGE 8>>>
8
Allottees with Waiver/Consent Obtained
Investor
No. of Offer 
Shares 
allocated
% of total 
number 
of Offer 
Shares(2)
% of total 
issued share 
capital in the 
Company 
after the 
Global 
Offering(2)(3)
Relationship
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations of further Offer Shares to (i) close associates of existing 
Shareholders and (ii) Cornerstone Investors and/or their close associates(1)
Primavera Investment 
Fund
4,040,000
2.35%
0.41%
A cornerstone 
investor and a 
close associate 
of an existing 
Shareholder
CSC OTC Swap
237,800
0.14%
0.02%
A cornerstone 
investor and a close 
associate of the 
Minority Existing 
Shareholder
GBAHIL
– Mega Prime
1,783,000
1.04%
0.18%
A cornerstone 
investor 
– Poly Platinum
1,783,000
1.04%
0.18%
A cornerstone 
investor
Subtotal
3,566,000
2.07%
0.36%
CFTC PARAMOUNT SP
2,381,400
1.38%
0.24%
A close associate 
of a cornerstone 
investor(4)
HK BVF I LPF
4,750,600
2.76%
0.48%
A cornerstone 
investor
Orient Asset Management
Orient Asset 
Management 
713,300
0.41%
0.07%
A cornerstone 
investor
China Universal Asset 
Management (Hong 
Kong) Company Limited 
(“China UAM”)
1,400,000
0.81%
0.14%
A close associate 
of a cornerstone 
investor(5)
Subtotal
2,113,300
1.23%
0.21%
Mount Altai
1,189,300
0.69%
0.12%
A cornerstone 
investor

<<<PAGE 9>>>
9
Investor
No. of Offer 
Shares 
allocated
% of total 
number 
of Offer 
Shares(2)
% of total 
issued share 
capital in the 
Company 
after the 
Global 
Offering(2)(3)
Relationship
Sinofortune International
1,902,900
1.11%
0.19%
A cornerstone 
investor
Ambre Lau Trade 
Limited
1,165,300
0.68%
0.12%
A cornerstone 
investor
SCV Delta
1,145,300
0.67%
0.12%
A cornerstone 
investor
Mirae Asset Securities 
HK
1,902,900
1.11%
0.19%
A cornerstone 
investor
Turquoise Hime (ORIX)
713,500
0.41%
0.07%
A cornerstone 
investor
GF Fund
GF Fund HK
713,500
0.41%
0.07%
A cornerstone 
investor
GF Securities 
Asset Management 
(Guangdong ) Co., Ltd. 
(“GF Securities AM”)
118,900
0.07%
0.01%
A close associate 
of a cornerstone 
investor(6)
GF Asset Management 
(Hong Kong) Limited 
(“GFAM HK”)
2,378,000
1.38%
0.24%
A close associate 
of a cornerstone 
investor(6)
Subtotal
3,210,400
1.87%
0.33%
E Fund
– E Fund HK
677,800
0.39%
0.07%
A cornerstone 
investor
– E Fund Management
35,700
0.02%
0.004%
A cornerstone 
investor
Subtotal
713,500
0.41%
0.07%
First Seafront Asset 
Management Limited
1,189,100
0.69%
0.12%
A cornerstone 
investor
GigaDevice
1,189,300
0.69%
0.12%
A cornerstone 
investor

<<<PAGE 10>>>
10
Investor
No. of Offer 
Shares 
allocated
% of total 
number 
of Offer 
Shares(2)
% of total 
issued share 
capital in the 
Company 
after the 
Global 
Offering(2)(3)
Relationship
Alphahill Capital
1,189,300
0.69%
0.12%
A cornerstone 
investor
ODI Trust
713,500
0.41%
0.07%
A cornerstone 
investor
Barings
1,189,300
0.69%
0.12%
A cornerstone 
investor
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 
of the Guide for New Listing Applicants in relation to allocations to connected clients(7)
CITIC Securities 
International Capital 
Management Limited 
(“CSI”)
712,600
0.41%
0.07%
Connected client as 
a placee
GF Securities AM
118,900
0.07%
0.01%
Connected client as 
a placee
CITIC Securities Asset 
Management Company 
Limited (“CITIC AM”)
59,500
0.03%
0.01%
Connected client as 
a placee
CITIC Securities Asset 
Management (HK) 
Limited (“CITIC AM 
HK”)
30,400
0.02%
0.003%
Connected client as 
a placee
Value Partners Limited 
(“Value Partners”)
951,000
0.55%
0.10%
Connected client as 
a placee
GFAM HK
2,378,000
1.38%
0.24%
Connected client as 
a placee
GF Fund HK
713,500
0.41%
0.07%
Connected client as 
a placee

<<<PAGE 11>>>
11
Investor
No. of Offer 
Shares 
allocated
% of total 
number 
of Offer 
Shares(2)
% of total 
issued share 
capital in the 
Company 
after the 
Global 
Offering(2)(3)
Relationship
E Fund Management
35,700
0.02%
0.004%
Connected client as 
a placee
E Fund HK
677,800
0.39%
0.07%
Connected client as 
a placee
Bosera Asset 
Management 
(International) Co., 
Limited (“Bosera AM”)
450,000
0.26%
0.05%
Connected client as 
a placee
China Merchants Fund 
Management Co., Ltd. 
(“China Merchants 
Fund”)
118,100
0.07%
0.01%
Connected client as 
a placee
HSBC Global Asset 
Management (Hong 
Kong) Limited (“HSBC 
GAM”)
5,940,000
3.45%
0.60%
Connected client as 
a placee

<<<PAGE 12>>>
12
Investor
No. of Offer 
Shares 
allocated
% of total 
number 
of Offer 
Shares(2)
% of total 
issued share 
capital in the 
Company 
after the 
Global 
Offering(2)(3)
Relationship
Notes:
1. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details – International Offering – Cornerstone Investors” in this announcement. For details of the 
consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations 
of further Shares to (i) close associates of existing Shareholders and (ii) Cornerstone Investors and/or their 
close associates, please refer to the section headed “Others/Additional Information – Allocation of Offer 
Shares to (i) close associates of existing Shareholders and (ii) Cornerstone Investors and/or their close 
associates with a consent under Chapter 4.15 of the Guide for New Listing Applicants” in this announcement.
2. 
Assuming the Over-allotment Option is not exercised.
3. 
The number of Shares immediately after the Global Offering is the same as the number of total issued shares 
of the Company after the Global Offering.
4. 
CFTC Paragon SP (a Cornerstone Investor) and CFTC Paramount SP are separate segregated portfolios of 
CFTC Summit Fund SPC and are managed by the same investment manager, being CFTC Asset Management 
(Hong Kong) Limited. As a result, CFTC Paramount SP is a close associate of CFTC Paragon SP.
5. 
Each of Orient Asset Management (a cornerstone Investor) and China UAM is ultimately controlled by Orient 
Securities Company Limited, and therefore China UAM is a close associate of Orient Asset Management.
6. 
Each of GF Securities AM., GFAM HK and GF Fund HK (a Cornerstone Investor) is ultimately controlled by 
GF Securities Co., Ltd., and therefore each of GF Securities AM and GFAM HK is a close associate of GF 
Fund HK.
7. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details – International Offering – Cornerstone Investors” in this announcement. For details of the 
consent under paragraph 1C(1) of the Placing Guidelines and paragraph 18 of Chapter 4.15 of the Guide for 
New Listing Applicants in relation to allocations to connected clients, please refer to the sections headed 
“Others/Additional Information – Placing to connected clients with a prior consent under paragraph 1C(1) of 
the Placing Guidelines” in this announcement.

<<<PAGE 13>>>
13
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
% of total issued 
share capital in 
the Company 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-
allotment Option 
is not exercised)
Last day subject 
to the lock-up 
undertakings(1)
Hisense Group Holdings  
Co., Ltd.
(海信集團控股股份 
有限公司)
360,373,650
36.66%
September 21, 2027
Hisense CKL (HK)  
Co., Limited
(海信世紀金隆(香港) 
有限公司)
33,851,300
3.44%
September 21, 2027
Note:
1. 
The expiry date of the lock-up period shown in the table above is pursuant to applicable relevant lock-up 
undertakings as disclosed in the Prospectus.
Cornerstone Investors
Name
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
% total issued 
share capital in 
the Company 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-
allotment Option 
is not exercised)
Last day subject 
to the lock-up 
undertakings(1)
Primavera Investment
Fund
7,136,300
0.73%
March 21, 2027
Mega Prime
3,568,100
0.36%
March 21, 2027
Poly Platinum
3,568,100
0.36%
March 21, 2027
CFTC Paragon SP
7,136,300
0.73%
March 21, 2027
HK BVF I LPF
7,136,300
0.73%
March 21, 2027

<<<PAGE 14>>>
14
Name
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
% total issued 
share capital in 
the Company 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-
allotment Option 
is not exercised)
Last day subject 
to the lock-up 
undertakings(1)
Orient Asset Management
3,568,100
0.36%
March 21, 2027
Mount Altai
3,568,100
0.36%
March 21, 2027
Peak View Capital
3,568,100
0.36%
March 21, 2027
Sinofortune International
3,568,100
0.36%
March 21, 2027
Ambre Lau Trade Limited
3,568,100
0.36%
March 21, 2027
SCV Delta
2,378,700
0.24%
March 21, 2027
Mirae Asset Securities HK
2,378,700
0.24%
March 21, 2027
PAG Capital Structure
Opportunity Fund LP
2,378,700
0.24%
March 21, 2027
Turquoise Hime (ORIX)
2,378,700
0.24%
March 21, 2027
GF Fund Management
2,259,800
0.23%
March 21, 2027
GF Fund HK
118,900
0.01%
March 21, 2027
E Fund HK
2,259,800
0.23%
March 21, 2027
E Fund Management
118,900
0.01%
March 21, 2027
CSC OTC Swap
2,378,700
0.24%
March 21, 2027
First Seafront Asset 
Management Limited
2,378,700
0.24%
March 21, 2027
GaoTeng Global Asset 
Management Limited
2,378,700
0.24%
March 21, 2027
GigaDevice
2,378,700
0.24%
March 21, 2027

<<<PAGE 15>>>
15
Name
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
% total issued 
share capital in 
the Company 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-
allotment Option 
is not exercised)
Last day subject 
to the lock-up 
undertakings(1)
Amlogic Hong Kong
2,378,700
0.24%
March 21, 2027
Atlas Venture Limited
2,378,700
0.24%
March 21, 2027
Alphahill Capital
2,378,700
0.24%
March 21, 2027
ODI Trust
2,378,700
0.24%
March 21, 2027
Barings
1,189,300
0.12%
March 21, 2027
Note:
1. 
Pursuant to the relevant cornerstone investment agreements, each of the Cornerstone Investors shall not, at 
any time during the period of six months from (and inclusive of) the Listing Date, dispose of, in any way, 
any of the Offer Shares or any interest in any company or entity holding such Offer Shares that they have 
purchased pursuant to the relevant Cornerstone Investment Agreement, save for certain limited circumstances. 
For details, please refer to the section headed “Cornerstone Investors – Restrictions on the Cornerstone 
Investors” of the Prospectus.
Other Existing Shareholders
Name
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
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
undertakings(1)
Qingdao Bolangde  
Broadband Co., Ltd.
(青島博朗德寬頻股份 
有限公司) (“Bolangde”)
26,645,950
2.71%
September 21, 2027
AI Talents Holdings, LLC 
(“Talents Holdings”)
6,725,950
0.68%
September 21, 2027
TransLight Limited 
(“TransLight”)
188,300,750
19.16%
September 21, 2027(2)
Global Optical Holdings Limited
(全球光通控股有限公司) 
(“Global Optical”)
133,630,750
13.60%
September 21, 2027(2)

<<<PAGE 16>>>
16
Name
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
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
undertakings(1)
Archcom Delaware Holding LLC 
(“Archcom LLC”)
36,574,150
3.72%
September 21, 2027(2)
Xiamen Guojuxiang Equity 
Investment Partnership Enterprise 
(Limited Partnership)
(廈門國炬翔股權投資合夥
企業(有限合夥)) (“Xiamen 
Guojuxiang”)
10,610,500
1.08%
September 21, 2027(2)
Xiamen Advanced Manufacturing 
Equity Investment Fund 
Partnership Enterprise (Limited 
Partnership)
(廈門先進製造業股權投資基金
合夥企業(有限合夥)) (“Xiamen 
Advanced Manufacturing 
Fund”)
10,452,550
1.06%
September 21, 2027(2)
Xiamen TorchRunxin Technology 
Equity Investment Partnership 
Enterprise (Limited Partnership)
(廈門火炬潤信科技股權投
資基金合夥企業(有限合夥)) 
(“Xiamen TorchRunxin”, 
collectively with Xiamen 
Guojuxiang and Xiamen 
Advanced Manufacturing Fund, 
the “Xiamen Entities”)
3,761,250
0.38%
September 21, 2027(2)
Notes:
1. 
The expiry date of the lock-up period shown in the table above is pursuant to the relevant lock-up 
undertakings as set out in the Prospectus.
2. 
For each of TransLight, Global Optical, Archcom LLC and Xiamen Entities, the number of Shares subject to 
lock-up undertaking shall represent (i) 100% of the Shares for the first six months after the Listing Date; (ii) 
85% of the Shares for the seventh month after the Listing Date; (iii) 50% of the Shares for the eighth month 
and the ninth month after the Listing Date; and (iv) 20% of the Shares for the tenth month after the Listing 
Date until the end of the lock-up period.

<<<PAGE 17>>>
17
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
Shares 
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
Option)**
% of total 
issued share 
capital upon 
Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised)**
Top 1
11,886,900
7.68%
6.58%
6.91%
6.01%
11,886,900
1.21%
1.18%
Top 5
52,915,400
34.18%
29.30%
30.76%
26.75%
186,546,150
18.98%
18.49%
Top 10
79,498,600
51.35%
44.02%
46.22%
40.19%
213,129,350
21.68%
21.13%
Top 25
126,669,800
81.82%
70.13%
73.64%
64.03%
264,061,800
26.86%
26.18%
* 
Ranking of placees is based on the number of Offer Shares allotted to the placees.
** 
The number of Shares immediately after the Global Offering is the same as the number of total issued shares of 
the Company after the Global Offering.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number of 
Shares 
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
Option)**
% of total 
issued share 
capital upon 
Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised)**
Top 1
–
0.00%
0.00%
0.00%
0.00%
394,224,950
40.11%
39.08%
Top 5
11,176,300.00
7.22%
6.19%
6.50%
5.65%
790,552,850
80.43%
78.37%
Top 10
52,915,400.00
34.18%
29.30%
30.76%
26.75%
853,355,000
86.82%
84.60%
Top 25
110,970,700.00
71.68%
61.44%
64.51%
56.10%
921,897,500
93.79%
91.39%
* 
Ranking of Shareholders is based on the number of Shares held by the Shareholder upon Listing.
** 
The number of Shares immediately after the Global Offering is the same as the number of total issued shares of 
the Company after the Global Offering.

<<<PAGE 18>>>
18
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 37,594 valid 
applications made by the public will be conditionally allocated on the basis set out below:
BASIS OF ALLOTMENT UNDER THE HONG 
KONG PUBLIC OFFERING
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
100
12,344
495 out of 12,344 to receive 100 Shares
4.01%
200
2,719
218 out of 2,719 to receive 100 Shares
4.01%
300
3,948
475 out of 3,948 to receive 100 Shares
4.01%
400
1,003
161 out of 1,003 to receive 100 Shares
4.01%
500
1,417
284 out of 1,417 to receive 100 Shares
4.01%
600
702
169 out of 702 to receive 100 Shares
4.01%
700
453
127 out of 453 to receive 100 Shares
4.01%
800
449
144 out of 449 to receive 100 Shares
4.01%
900
404
145 out of 404 to receive 100 Shares
3.99%
1,000
3,971
1,574 out of 3,971 to receive 100 Shares
3.96%
2,000
1,991
1,576 out of 1,991 to receive 100 Shares
3.96%
3,000
1,176
100 Shares plus 221 out of 1,176 to receive additional 100 Shares
3.96%
4,000
506
100 Shares plus 296 out of 506 to receive additional 100 Shares
3.96%
5,000
538
100 Shares plus 528 out of 538 to receive additional 100 Shares
3.96%
6,000
343
200 Shares plus 129 out of 343 to receive additional 100 Shares
3.96%
7,000
196
200 Shares plus 151 out of 196 to receive additional 100 Shares
3.96%
8,000
207
300 Shares plus 35 out of 207 to receive additional 100 Shares
3.96%
9,000
200
300 Shares plus 112 out of 200 to receive additional 100 Shares
3.96%
10,000
1,306
300 Shares plus 1,252 out of 1,306 to receive additional 100 Shares 3.96%
20,000
661
700 Shares plus 602 out of 661 to receive additional 100 Shares
3.96%
30,000
403
1,100 Shares plus 349 out of 403 to receive additional 100 Shares
3.96%
40,000
270
1,500 Shares plus 222 out of 270 to receive additional 100 Shares
3.96%
50,000
227
1,900 Shares plus 187 out of 227 to receive additional 100 Shares
3.96%
60,000
164
2,300 Shares plus 120 out of 164 to receive additional 100 Shares
3.96%
70,000
134
2,700 Shares plus 92 out of 134 to receive additional 100 Shares
3.96%
80,000
124
3,100 Shares plus 80 out of 124 to receive additional 100 Shares
3.96%
90,000
111
3,500 Shares plus 67 out of 111 to receive additional 100 Shares
3.96%
100,000
890
3,900 Shares plus 508 out of 890 to receive additional 100 Shares
3.96%
Total
36,857
Total number of Pool A successful applicants: 12,824

<<<PAGE 19>>>
19
Pool B
Number of 
Shares 
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
200,000
398
4,400 Shares plus 155 out of 398 to receive additional 100 Shares
2.22%
300,000
101
6,600 Shares plus 59 out of 101 to receive additional 100 Shares
2.22%
400,000
41
8,800 Shares plus 32 out of 41 to receive additional 100 Shares
2.22%
500,000
106
11,000 Shares plus 103 out of 106 to receive additional 100 Shares
2.22%
1,000,000
38
22,100 Shares plus 36 out of 38 to receive additional 100 Shares
2.22%
1,500,000
22
33,200 Shares plus 20 out of 22 to receive additional 100 Shares
2.22%
2,000,000
6
44,300 Shares plus 5 out of 6 to receive additional 100 Shares
2.22%
3,000,000
9
66,500 Shares plus 8 out of 9 to receive additional 100 Shares
2.22%
4,000,000
7
88,700 Shares plus 6 out of 7 to receive additional 100 Shares
2.22%
5,000,000
2
111,000 Shares
2.22%
8,600,700
7
190,900 Shares
2.22%
Total
737
Total number of Pool B successful applicants: 737
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Allocations of Offer Shares to (i) close associates of existing Shareholders and (ii) Cornerstone 
Investors and/or their close associates with a consent under Chapter 4.15 of the Guide for 
New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph 18 
of Chapter 4.15 of the Guide for New Listing Applicants (the “Size-based Exemption”) to permit 
the Company to allocate further Offer Shares in the International Offering to close associates of 
certain existing Shareholders and Cornerstone Investors and/or their close associates, as placees, 
subject to the following conditions (“Allocation to Size-based Exemption Participants”):
(a) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;

<<<PAGE 20>>>
20
(b) 
it is expected that the Offer Shares allocated to all existing Shareholders and their close 
associates (whether as Cornerstone Investors and/or as placees) as permitted under the Size-
based Exemption do not exceed 30% of the total number of Shares offered under the Global 
Offering;
(c) 
each of the Directors, chief executive of the Company and the Controlling Shareholders has 
confirmed that no securities have been allocated to them or their respective close associates 
under the Size-based Exemption;
(d) 
the Allocation to Size-based Exemption Participants is not expected to affect the Company’s 
ability to satisfy its public float requirement; and
(e) 
details of the Allocation to Size-based Exemption Participants under the Size-based 
Exemption will be disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to existing Shareholders and Cornerstone Investors 
and/or their close associates, please refer to the section headed “Allotment Results Details – 
International Offering – Allottees with Waivers/Consents Obtained” in this announcement.
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines. Details of the placement to connected 
clients are set out below. The Company has applied to the Stock Exchange for, and the Stock 
Exchange has granted, consents under paragraph 1C(1) of the Placing Guidelines to permit the 
Company to allocate such Offer Shares in the International Offering to the connected clients. The 
allocation of Offer Shares to such connected clients is in compliance with all the conditions under 
the consent granted by the Stock Exchange. Details of the placement to connected clients are set 
out below:

<<<PAGE 21>>>
21
Part A – Connected Clients holding the beneficial interest of the Offer Shares on a non-discretionary basis on behalf of independent 
third parties
No.
Connected Distributor
Connected Client
Relationship with the 
Connected Distributor
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
Number of 
Offer Shares 
allocated to the 
connected client
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
CLSA Limited (“CLSA”) 
and CNCB (Hong Kong) 
Capital Limited (“CNCB”)
CITIC Securities 
International Capital 
Management Limited 
(“CSI”)
CSI is a member of the 
same group of companies  
as CLSA and CNCB
No
712,600
0.41%
0.07%
2.
GF Securities (Hong Kong) 
Brokerage Limited (“GF 
Securities (Hong Kong) 
Brokerage”)
GF Securities Asset 
Management (Guangdong) 
Co., Ltd. (“GF Securities 
AM”)
GF Securities AM is 
a member of the same 
group of companies as GF 
Securities (Hong Kong) 
Brokerage
No
118,900
0.07%
0.01%

<<<PAGE 22>>>
22
Notes:
1. 
CSI will hold the Offer Shares as a placee under the International Offering on behalf of its ultimate clients (the “CSI Ultimate Clients”), on a non-discretionary 
basis, pursuant to which: (i) CSI will act as the single counterparty of the CSI Back-to-back TRS (the “CSI Back-to-back TRS”) to be entered into by it in 
connection with a total return swap order (the “CSI Client TRS”) placed and fully funded by the CSI Ultimate Clients, by which CSI will pass the full economic 
exposure of the Offer Shares placed to CSI to the CSI Ultimate Clients; (ii) as confirmed by CSI and CLSA, CSI will hold the legal title and beneficial interest 
in the Offer Shares, but will contractually agree to pass on the full economic exposure and return of the Offer Shares to the CSI Ultimate Clients, on a non-
discretionary basis. The CSI Ultimate Clients may exercise their early termination rights to terminate the CSI Client TRS at any time from the trade date of the 
CSI Client TRS which should be on or after the date on which the Offer Shares are listed on the Stock Exchange; (iii) upon the final maturity or termination of 
the CSI Client TRS by the CSI Ultimate Clients, CSI will dispose of the Offer Shares on the secondary market and the CSI Ultimate Clients will receive a final 
termination amount of the CSI Back-to-back TRS which will have taken into account all the economic returns or economic loss in relation to the Offer Shares 
and the fixed amount of transaction fees of the CSI Back-to-back TRS and the CSI Client TRS. Due to its internal policy, CSI will not exercise the voting right 
of the Offer Shares during the terms of the CSI Back-to-back TRS; and (iv) CSI is not a collective investment scheme which is not authorized by the SFC, nor is 
expected to hold the Offer Shares on behalf of such scheme.
The details of the CSI Ultimate Clients are as follows:
Name of the CSI Ultimate Clients
Asset manager
UBO of asset manager
UBO of CSI Ultimate Client
HY Capital Company Limited
N/A
N/A
Xia Hui (ID R317264(2))
Lu Ang (ID M863625(2))
LFountain Asset Management SPC 
 – Gestone SP
HONG KONG LFOUNTAIN 
CAPITAL CO., LIMITED
LI YEMIAO (Passport EE3344765) 
SUN JIANLIN (Passport EL5204692)
GE JIAXI (EJ5133483)
To the best of knowledge of CSI and having made all reasonable inquiries, each of the CSI Ultimate Clients and its UBOs is an independent third party of the 
Company, its subsidiaries, its substantial shareholders, CSI, CLSA, CNCB and the companies which are members of the same group of companies as CLSA and 
CNCB.
2. 
Each of the ultimate clients of GF Securities AM (the “GF Securities AM Ultimate Clients”) have engaged GF Securities AM, an asset manager that is qualified 
domestic institutional investor as approved by the relevant PRC authority, in the name of the asset management plans as disclosed below, to subscribe for and 
hold the Offer Shares as a placee under the International Offering on behalf of the GF Securities AM Ultimate Client on a non-discretionary basis. GF Securities 
AM, in the name of the asset management plans as disclosed below, will hold the legal title of the Offer Shares, and the economic risks and return of the Offer 
Shares will pass through to the GF Securities AM Ultimate Clients.
Details of the GF Securities AM Ultimate Clients are set out as below:
Name of the GF Securities AM Ultimate Clients
Name of the asset management plan
Zhonghe Capital Cultivation 920 Private Securities Investment Fund 
 (中和資本耕耘 920 號私募證券投資基金), 
 whose ultimate beneficial owner is Zhang Jingting (張敬庭)
GF Asset Management Hong Kong Equity Diversified Strategy 
 No. 7 Single Asset Management Plan
Zhonghe Capital Cultivation 810 Private Securities Investment Fund 
 (中和資本耕耘 810 號私募證券投資基金), 
 whose ultimate beneficial owner is Zhang Jingting (張敬庭)
GF Asset Management Hong Kong Equity Diversified Strategy 
 No. 12 Single Asset Management Plan
Liu Peilan (劉培蘭)
GF Asset Management Excellence Diversified Allocation 
 No. 58 Single Asset Management Plan
No UBO holding 30% or more interest
GF Asset Management Ruixin Hong Kong Equity Research Select 
 No. 1 Collective Asset Management Plan

<<<PAGE 23>>>
23
Part B – Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third 
parties
No.
Connected Distributor
Connected Client
Relationship with the 
Connected Distributor
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
Number of 
Offer Shares 
allocated to the 
connected client
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
CLSA and CNCB
CITIC Securities Asset 
Management Company 
Limited (“CITIC AM”)
CITIC AM is a member 
of the same group of 
companies as CLSA and 
CNCB
Yes
59,500
0.03%
0.01%
2.
CLSA and CNCB
CITIC Securities Asset 
Management (HK) Limited 
(“CITIC AM HK”)
CITIC AM HK is a member 
of the same group of 
companies as CLSA and 
CNCB
No
30,400
0.02%
0.003%
3.
GF Securities (Hong Kong) 
Brokerage
Value Partners Limited 
(“Value Partners”)
Value Partners is a member 
of the same group of 
companies as GF Securities 
(Hong Kong) Brokerage
No
951,000
0.55%
0.10%

<<<PAGE 24>>>
24
No.
Connected Distributor
Connected Client
Relationship with the 
Connected Distributor
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
Number of 
Offer Shares 
allocated to the 
connected client
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
4.
GF Securities (Hong Kong) 
Brokerage
GF Asset Management 
(Hong Kong) Limited 
(“GFAM HK”)
GFAM HK is a member 
of the same group of 
companies as GF Securities 
(Hong Kong) Brokerage
No
2,378,000
1.38%
0.24%
5.
GF Securities (Hong Kong) 
Brokerage
GF International Investment 
Management Limited (“GF 
Fund HK”)
GF Fund HK is a member 
of the same group of 
companies as GF Securities 
(Hong Kong) Brokerage
Please refer to Note 
5 for details.
713,500
0.41%
0.07%
6.
GF Securities (Hong Kong) 
Brokerage
E Fund Management 
Co., Ltd. (“E Fund 
Management”)
E Fund Management is 
a member of the same 
group of companies as GF 
Securities (Hong Kong) 
Brokerage
No
35,700
0.02%
0.004%

<<<PAGE 25>>>
25
No.
Connected Distributor
Connected Client
Relationship with the 
Connected Distributor
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
Number of 
Offer Shares 
allocated to the 
connected client
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
7.
GF Securities (Hong Kong) 
Brokerage
E Fund Management (Hong 
Kong) Co., Ltd. (“E Fund 
HK”)
E Fund HK is a member 
of the same group of 
companies as GF Securities 
(Hong Kong) Brokerage
Yes
677,800
0.39%
0.07%
8.
CMB International 
Securities Limited 
(“CMBI”) and China 
Merchants Securities (HK) 
Co., Limited (“CMS”)
Bosera Asset Management 
(International) Co., Limited 
(“Bosera AM”)
Bosera AM is a member 
of the same group of 
companies as CMBI and 
CMS
Yes
450,000
0.26%
0.05%
9.
CMBI and CMS
China Merchants Fund 
Management Co., Ltd. 
(“China Merchants Fund”)
China Merchants Fund is a 
member of the same group 
of companies as CMBI and 
CMS
No
118,100
0.07%
0.01%
10.
The Hongkong and 
Shanghai Banking 
Corporation Limited 
(“HSBC”)
HSBC Global Asset 
Management (Hong Kong) 
Limited (“HSBC GAM”)
HSBC GAM is a member 
of the same group of 
companies as HSBC
Please refer to Note 
11 for details.
5,940,000
3.45%
0.60%
Notes:
1. 
CITIC AM will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their investors (the “CITIC Asset 
Management Ultimate Clients”), each of which is an independent third party.

<<<PAGE 26>>>
26
The details of the CITIC Asset Management Ultimate Clients are as follows:
Fund name
Values of assets 
under management 
(AUM)
Whether the 
scheme is 
publicly 
marketed
Fund manager
UBO holding 
30% or more 
interest in the fund
UBO of fund 
manager
Number of the 
CITIC Asset 
Management 
Ultimate Clients
CITIC SECURITIES COMPANY 
 LIMITED-XINHANG ZHIYUAN 
 NO.1 (中信證券信航致遠 1 號
 集合資產管理計劃)
RMB 20,240,402.13
Not publicly marketed
CITIC AM
No
CITIC Securities 
 Company Limited
20
CITIC SECURITIES COMPANY 
 LIMITED-XINHANG ZHIYUAN 
 NO.3 (中信證券信航致遠 3 號
 集合資產管理計劃)
RMB 47,342,081.73
Not publicly marketed
CITIC AM
No
CITIC Securities 
 Company Limited
35
2. 
CITIC AM HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their investors, each of which is an 
independent third party.
The funds are as follows:
(1) 
CITIC Securities Asset Management (HK) Limited – Meta Chance2, invested 100% by Meta Chance Limited, of which UBO holding 30% or more interest 
is natural person Song Ke (CHN Passport E57964565).
(2) 
ICBC (ASIA) LTD-CITIC SECURITIES AM LTD-BSCOMC LTD, invested 100% by BSCOMC Limited, of which UBO holding 30% or more interest is 
State-owned Assets Supervision and Administration Commission of People’s Government of Beijing Municipality.

<<<PAGE 27>>>
27
3. 
Value Partners is a member of the same group of companies as GF Securities (Hong Kong) Brokerage. GF Securities (Hong Kong) Brokerage is an indirect 
wholly-owned subsidiary of GF Securities Co. Ltd. (Stock Code: 1776) (“GF Securities”). Value Partners is a wholly-owned subsidiary of Value Partners Group 
Limited (Stock Code: 806) (“VPGL”). GF Securities is interested in 20.04% shareholding in VPGL which renders Value Partners an associate of GF Securities. 
Accordingly, Value Partners is a member of the same group of companies as GF Securities (Hong Kong) Brokerage and is considered as a connected client of GF 
Securities (Hong Kong) Brokerage under paragraph 1B(7) of the Placing Guidelines.
Value Partners will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of its investors (the “VP Ultimate 
Clients”). Value Partners is to invest on a discretionary basis on behalf of the VP Ultimate Clients which are independent third parties and no proprietary money 
is used for the subscription of Offer Shares. To the best knowledge of Value Partners, each of the VP Ultimate Clients is an independent third party of the 
Company, its subsidiaries, its substantial shareholders, Value Partners, GF Securities (Hong Kong) Brokerage and the companies which are members of the same 
group of companies as GF Securities (Hong Kong) Brokerage.
The details of the VP Ultimate Clients are as follows:
Name of the funds to which the Offer Shares 
will be allocated
Whether any investor holds 30% or 
more interest in the fund
UBO holding 30% or more interest
Value Partners Intelligent Funds – Chinese 
 Mainland Focus Fund
Yes
AIA International Limited
4. 
GFAM HK will hold the Offer Shares in its capacity as the discretionary investment manager for and on behalf of the underlying clients, each of which is, to the 
best knowledge and belief and after due enquiry of GFAM HK, an independent third party of the Company, its subsidiaries, GFAM HK, GF Securities (Hong 
Kong) Brokerage and the companies which are members of the same group of GF Securities (Hong Kong) Brokerage.

<<<PAGE 28>>>
28
The details of the underlying clients are as follows:
Name of the ultimate client to which the Offer 
Shares will be allocated
Whether any investor holds 30% or 
more interest in the ultimate client
UBO holding 30% or more interest
Golden Armour Investment Limited
Yes
Hengming Fan

<<<PAGE 29>>>
29
5. 
GF Fund HK will hold the Offer Shares in its capacity as the discretionary investment manager for and on behalf of the underlying clients, each of which is, to 
the best knowledge and belief and after due enquiry of GF Fund HK, an independent third party of the Company, its subsidiaries, GF Fund HK, GF Securities 
(Hong Kong) Brokerage and the companies which are members of the same group of GF Securities (Hong Kong) Brokerage. No ultimate beneficial owner holds 
30% or more interest in the funds.
GF Fund HK is investing on behalf of certain collective investment schemes which are not authorized by the SFC, details of which are as follows:
Name of the 
fund/sub-fund
Whether the scheme is 
publicly marketed
Identities of the general partners 
and the 20 largest limited 
partners of the scheme where 
applicable
Identity of the scheme 
administrator
The relationships among the scheme, 
the ultimate beneficial owners of 
the limited partners, the controlling 
shareholders of the applicant, and 
the applicant
Golden Fortune Opportunity 
Fund
No
Not applicable as it is not in 
partnership structure
GF Fund HK
The scheme and ultimate beneficial 
owners are independent third parties 
of GF Securities (Hong Kong) 
Brokerage, the Company and the 
Controlling Shareholders of the 
Company.
FrontLine Investment  
Master SPC-GF  
Luminous Fund SP
No
Not applicable as it is not in 
partnership structure
GF Fund HK
The scheme and ultimate beneficial 
owners are independent third parties 
of GF Securities (Hong Kong) 
Brokerage, the Company and the 
Controlling Shareholders of the 
Company.
FrontLine Investment  
Master SPC-GF  
Vision Fund SP
No
Not applicable as it is not in 
partnership structure
GF Fund HK
The scheme and ultimate beneficial 
owners are independent third parties 
of GF Securities (Hong Kong) 
Brokerage, the Company and the 
Controlling Shareholders of the 
Company.
In addition to the funds disclosed above, GF Fund HK is also expected to hold the Offer Shares on behalf of one SFC authorized fund, namely GFI Global Select 
Equity Fund.

<<<PAGE 30>>>
30
6. 
E Fund Management will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of its investors, each of which 
is, to the best knowledge of E Fund Management, an independent third party of E Fund Management, GF Securities (Hong Kong) Brokerage and the companies 
which are members of the same group of GF Securities (Hong Kong) Brokerage.
7. 
E Fund HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of its investors, each of which is, to the 
best knowledge of E Fund HK, an independent third party of E Fund HK, GF Securities (Hong Kong) Brokerage and the companies which are members of the 
same group of GF Securities (Hong Kong) Brokerage.
In addition, E Fund HK is expected to hold the Offer Shares on behalf of the following collective investment schemes which are not authorised by the SFC:
Name of the collective 
investment schemes
Whether the scheme is 
publicly marketed
Identities of the general partners 
and the 20 largest limited 
partners of the scheme where 
applicable
Identity of the Scheme 
Administrator
The relationships among the scheme, 
the ultimate beneficial owners of 
the limited partners, the controlling 
shareholders of the applicant, and 
the applicant
E Fund (HK) Neo Horizon 
Fund SP
No
Not applicable as the scheme  
is not a limited partnership 
structure
E Fund HK
The scheme and ultimate beneficial 
owners are independent third parties 
of GF Securities (Hong Kong) 
Brokerage, the Company and the 
Controlling Shareholders of the 
Company.
E Fund (HK) Neo 
Opportunity SP II
No
Not applicable as the scheme is not 
a limited partnership structure
E Fund HK
The scheme and ultimate beneficial 
owners are independent third parties 
of GF Securities (Hong Kong) 
Brokerage, the Company and the 
Controlling Shareholders of the 
Company.

<<<PAGE 31>>>
31
8. 
Bosera AM will hold the Offer Shares in its capacity as the discretionary investment manager for and on behalf of the underlying clients, each of which is, to the 
best knowledge and belief and after due enquiry of Bosera AM, an independent third party of the Company, its subsidiaries, Bosera AM, CMBI, CMS and the 
companies which are members of the same group of CMBI and CMS.
The details of the underlying clients are as follows:
Name of the fund/sub-fund
Whether the scheme is 
publicly marketed (Y/N)
Identities of the general partners 
and the 20 largest limited partners 
of the scheme where applicable
Identity of the scheme 
administrator
The relationships among the scheme, 
the ultimate beneficial owners of 
the limited partners, the controlling 
shareholders of the applicant, and the 
applicant
Bosera China New 
Opportunities Fund SP
N
N/A
Bosera AM
The scheme and ultimate beneficial 
owners are independent third parties 
of CMBI, the Company and the 
Controlling Shareholders of the 
Company.
Bosera Growth Premium 
Global Equity Strategy 
Fund SP
N
N/A
Bosera AM
The scheme and ultimate beneficial 
owners are independent third parties 
of CMBI, the Company and the 
Controlling Shareholders of the 
Company.
KB CHINA MAINLAND  
FD BOSERA
N
N/A
Bosera AM
The scheme and ultimate beneficial 
owners are independent third parties 
of CMBI, the Company and the 
Controlling Shareholders of the 
Company.
Bosera Growth Premium 
Global Equity Strategy 
Fund SP2
N
N/A
Bosera AM
The scheme and ultimate beneficial 
owners are independent third parties 
of CMBI, the Company and the 
Controlling Shareholders of the 
Company.

<<<PAGE 32>>>
32
Name of the fund/sub-fund
Whether the scheme is 
publicly marketed (Y/N)
Identities of the general partners 
and the 20 largest limited partners 
of the scheme where applicable
Identity of the scheme 
administrator
The relationships among the scheme, 
the ultimate beneficial owners of 
the limited partners, the controlling 
shareholders of the applicant, and the 
applicant
Bosera Growth Premium 
Global Equity Strategy 
Fund SP3
N
N/A
Bosera AM
The scheme and ultimate beneficial 
owners are independent third parties 
of CMBI, the Company and the 
Controlling Shareholders of the 
Company.
Bosera Growth Premium 
Global Equity Strategy 
Fund SP4
N
N/A
Bosera AM
The scheme and ultimate beneficial 
owners are independent third parties 
of CMBI, the Company and the 
Controlling Shareholders of the 
Company.
9. 
China Merchants Fund will hold the Offer Shares in its capacity as the discretionary fund manager managing the Pusheng Global Allocation Fund (a mutual fund) 
on behalf of their investors, of which all underlying investors of China Merchants Fund are independent third parties of the Company, its subsidiaries, China 
Merchants Fund, CMBI, CMS and the companies which are members of the same group of CMBI or CMS. No ultimate beneficial owner holds 30% or more 
interest therein. China Merchants Bank Co., Ltd. (listed on the Shanghai Stock Exchange (SHA: 600036) and the Hong Kong Stock Exchange (HKEX: 3968)) 
and China Merchants Securities Co., Ltd. (listed on the Shanghai Stock Exchange (SHA: 600999) and the Hong Kong Stock Exchange (HKEX: 6099)) are the 
ultimate beneficial owners holding 30% or more interest in China Merchants Fund.
10. 
HSBC GAM will hold the Offer Shares in its capacity as the discretionary fund manager managing assets on behalf of the underlying funds. To the best 
knowledge of HSBC GAM after due enquiry, each of the underlying funds is an independent third party of the Company and its subsidiaries as confirmed by the 
Company, and each of the underlying funds is an independent third party of HSBC, HSBC GAM and the companies which are members of the same group of 
HSBC and HSBC GAM.

<<<PAGE 33>>>
33
HSBC GAM is investing on behalf of certain collective investment schemes which are not authorised by the SFC, details of which are as follows:
Name of the fund/sub-fund
Whether the scheme is 
publicly marketed (Y/N)
Identities of the general partners 
and the 20 largest limited partners 
of the scheme where applicable
Identity of the scheme 
administrator
The relationships among the scheme, 
the ultimate beneficial owners of 
the limited partners, the controlling 
shareholders of the applicant, and the 
applicant
HSBC China – Mother Fund
N
N/A
HSBC Asset Management 
(Japan) Limited
The scheme and ultimate beneficial 
owners are independent third parties 
of HSBC, the Company and the 
Controlling Shareholders of the 
Company.
HSBC Pooled Investment 
Fund – HSBC Pooled 
Chinese Equity Fund
N
N/A
HSBC GAM
The scheme and ultimate beneficial 
owners are independent third parties 
of HSBC, the Company and the 
Controlling Shareholders of the 
Company.
HSBC Pooled Investment 
Fund – HSBC Pooled Hong 
Kong Equity Fund
N
N/A
HSBC GAM
The scheme and ultimate beneficial 
owners are independent third parties 
of HSBC, the Company and the 
Controlling Shareholders of the 
Company.
In addition to the funds disclosed above, HSBC GAM is also expected to hold the Offer Shares on behalf of certain SFC authorised funds, comprising HSBC 
Global Investment Funds Chinese Equity, HSBC Global Investment Funds Hong Kong Equity, HSBC China Growth Fund, HSBC China Momentum Fund and 
HSBC Collective Investment Trust – HSBC China Multi-Asset Income Fund.

<<<PAGE 34>>>
34
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
The Offer Shares are being offered and sold solely (1) to qualified institutional buyers as defined 
in Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under 
the U.S. Securities Act and (2) outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated September 14, 2026 issued by Ligent Technologies, 
Inc. for detailed information about the Global Offering described below before deciding whether 
or not to invest in the Shares thereby being offered.
* 
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on 
behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the 
section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – 
Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing 
Date (which is currently expected to be on September 22, 2026).

<<<PAGE 35>>>
35
PUBLIC FLOAT AND FREE FLOAT
Pursuant to Rule 8.08(1) of the Listing Rules, assuming that the Over-allotment Option is not 
exercised, based on the Offer Price of HK$32.96 per Offer Share, the expected market value upon 
the Listing is HK$32.4 billion, and the minimum prescribed public float percentage applicable to 
the Shares is the higher of (i) the percentage that would result in the expected market value of such 
securities held by the public to be HK$4.5 billion at the time of listing and (ii) 10%. Immediately 
following completion of the Global Offering (assuming the Over-allotment Option is not 
exercised), an aggregate of 222,236,850 Shares, representing approximately 22.61% of the issued 
share capital of the Company will be counted towards the public float. Therefore, the number of 
Shares held in public hands is higher than the prescribed percentage of Shares required to be held 
in public hands under Rule 8.08(1) of the Listing Rules.
Shares held by all Shareholders immediately prior to the Listing Date and the Cornerstone 
Investors will be subject to certain lock-up restrictions immediately upon Listing and therefore will 
not be counted towards the free float for the purpose of Rule 8.08A of the Listing Rules. Based 
on the Offer Price of HK$32.96 per Offer Share, 87,098,000 Shares with an expected market 
value of approximately HK$2,871 million, which is higher than HK$600 million as required under 
8.08A of the Listing Rules, will not be subject to any disposal restrictions (whether under contract, 
the Listing Rules, applicable laws or otherwise) at the time of Listing. Therefore, the Company 
satisfies the free float requirement under Rule 8.08A of the Listing Rules.
The Directors confirm that save as disclosed in this announcement, immediately after the 
completion of the Global Offering (assuming the Over-allotment Option is not exercised), (i) no 
placee will, individually, be placed more than 10% of the enlarged issued share capital of the 
Company; (ii) there will not be any new substantial shareholder (as defined in the Listing Rules) 
of the Company; (iii) the three largest public shareholders of the Company do not hold more than 
50% of the Shares in public hands at the time of the Listing in compliance with Rules 8.08(3) and 
8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at the time of the Listing 
in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, September 
22, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting – Underwriting Arrangements 
and Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has not 
been exercised. Investors who trade the Shares on the basis of publicly available allocation details 
prior to the receipt of Share certificates or prior to the Share certificates becoming valid evidence 
of title do so entirely at their own risk.

<<<PAGE 36>>>
36
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Tuesday, 
September 22, 2026 (Hong Kong time), it is expected that dealings in the Shares on the Stock 
Exchange will commence at 9:00 a.m. on Tuesday, September 22, 2026 (Hong Kong time). The 
Shares will be traded in board lots of 100 Shares each, and the stock code of the Shares will be 
9856.
By order of the Board
Ligent Technologies, Inc.
Yu Zhitao
Chairman of the Board and Non-executive Director
Hong Kong, September 21, 2026
Directors of the Company to which this announcement relates are: (i) Mr. Yu Zhitao as Chairman 
of the Board and non-executive director; (ii) Dr. Hong Jin and Ms. Wang Hui as executive 
directors; (iii) Dr. Jia Shaoqian, Dr. Huang Weiping and Mr. Zhang Jing as non-executive 
directors; and (iv) Dr. Zhou Changjun, Dr. Sun Ying and Dr. Tong Franklin Fuk Kay as 
independent non-executive directors.
