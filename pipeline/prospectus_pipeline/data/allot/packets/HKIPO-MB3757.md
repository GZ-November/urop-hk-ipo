# 配发结果公告抽取任务：3757.HK RoboTechnik Intelligent Technology Co., Ltd.  - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**28/09/2026 22:22**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0928/2026092801977.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3757.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
– 1 –
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock 
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the 
contents of this announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the 
contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for 
securities in the United States or in any other jurisdictions. The Offer Shares have not been and will not be 
registered under the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities 
Act”) or securities law of any state or other jurisdiction of the United States and may not be offered, sold, 
pledged or otherwise transferred within the United States, except in transactions exempt from, or not subject to, 
the registration requirements of the U.S. Securities Act and in compliance with any applicable state securities 
laws. There will be no public offer of the Offer Shares in the United States. The Offer Shares are being offered 
and sold solely (1) to qualified institutional buyers as defined in Rule 144A under the U.S. Securities Act 
pursuant to an exemption from registration under the U.S. Securities Act; and (2) outside the United States in 
offshore transactions in reliance on Regulation S under the U.S. Securities Act and applicable laws of each 
jurisdiction where those offers and sales occur.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. This announcement is not a prospectus. Potential investors should read the 
prospectus dated September 21, 2026 (the “Prospectus”) issued by RoboTechnik Intelligent Technology Co., 
Ltd. (羅博特科智能科技股份有限公司) (the “Company”) for detailed information about the Global Offering 
described below before deciding whether or not to invest in the H Shares thereby being offered. Any investment 
decision in relation to the Offer Shares should be taken solely in reliance on the information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as 
those defined in the Prospectus.
In connection with the Global Offering, Huatai Financial Holdings (Hong Kong) Limited, as stabilizing manager 
(the “Stabilizing Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, to the 
extent permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-
allocate or effect transactions with a view to stabilizing or supporting the market price of the H Shares at such 
price, in such amounts and in such manners as the Stabilizing Manager, its affiliates or any person acting for it 
may determine and at a level higher than that which might otherwise prevail for a limited period after the Listing 
Date. However, there is no obligation on the Stabilizing Manager (or its affiliates or any person acting for it) 
to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will be conducted at the absolute 
discretion of the Stabilizing Manager (or its affiliates or any person acting for it) and in what the Stabilizing 
Manager reasonably regards as the best interest of our Company, (b) may be discontinued at any time and (c) 
is required to be brought to an end within 30 days of the last day for lodging applications under the Hong Kong 
Public Offering (which is Saturday, October 24, 2026). Such stabilizing action, if taken, may be effected in all 
jurisdictions where it is permissible to do so, in each case in compliance with all applicable laws, rules and 
regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 571 W of the 
Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws 
of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares 
for longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 
30th day after the last day for lodging applications under the Hong Kong Public Offering (which is Saturday, 
October 24, 2026). After this date, when no further stabilizing action may be taken, demand for the H Shares, 
and therefore the price of the H Shares, could fall.
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinators (for themselves and 
on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section 
headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds 
for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is 
currently expected to be on Tuesday, September 29, 2026).

<<<PAGE 2>>>
– 2 –
RoboTechnik Intelligent Technology Co., Ltd.
羅博特科智能科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the 
Global Offering
:
11,876,000 H Shares (subject to the Over-
allotment Option)
Number of Hong Kong Offer Shares
:
1,187,600 H Shares
Number of International Offer Shares
:
10,688,400 H Shares (subject to the Over-
allotment Option)
Final Offer Price
:
HK$436.00 per H Share, plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
Stock Exchange trading fee of 0.00565% 
and AFRC transaction levy of 0.00015% 
(payable in full on application in Hong 
Kong dollars and subject to refund)
Nominal Value
:
RMB1.00 per H Share
Stock Code
:
03757
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators,
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
– 3 –
RoboTechnik Intelligent Technology Co., Ltd.
羅博特科智能科技股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have 
the same meanings as those defined in the prospectus dated September 21, 2026 (the 
“Prospectus”) issued by RoboTechnik Intelligent Technology Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, H Shareholders and prospective investors should be aware that the price 
of the H Shares could move substantially even with a small number of H Shares traded 
and should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
03757
Stock short name
ROBOTECHNIK
Dealings commencement date
September 29, 2026#
# 
see note at the end of the announcement
Price Information
Final Offer Price
HK$436.00
Maximum Offer Price
HK$436.00
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the Over-
allotment Option)
11,876,000
Final Number of Offer Shares in Hong Kong Public Offering
1,187,600
Final Number of Offer Shares in International Offering 
(before exercise of the Over-allotment Option)
10,688,400
Number of issued Shares upon Listing (before exercise of the 
Over-allotment Option)
179,484,111

<<<PAGE 4>>>
– 4 –
Offer Size Adjustment Option (Upsize option)
Number of additional shares issued under the option
0*
– Hong Kong Public Offering
–
– International Offering
–
* 
The Offer Size Adjustment Option has not been exercised.
Over-allocation
No. of Offer Shares over-allocated
1,781,400
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$5,177.9 million
Less: Estimated listing expenses payable based on the Final 
Offer Price
HK$216.6 million
Net proceeds
HK$4,961.3 million
Note: Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the use 
of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
The Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis.

<<<PAGE 5>>>
– 5 –
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
13,075
No. of successful applications
6,925
Subscription level
8.65 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong 
Public Offering
1,187,600
No. of Offer Shares reallocated from the International 
Offering (reallocation)
0
Final no. of Offer Shares under the Hong Kong Public 
Offering
1,187,600
% of Offer Shares under the Hong Kong Public Offering 
to the Global Offering (before the exercise of the 
Over-allotment Option)
10%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can 
refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
120
Subscription Level
5.97 times
No. of Offer Shares initially available under the 
International Offering
10,688,400
Final no. of Offer Shares under the International Offering
10,688,400
% of Offer Shares under the International Offering to the 
Global Offering (before the exercise of the Over-allotment 
Option)
90%

<<<PAGE 6>>>
– 6 –
The Directors confirm that, to the best of their knowledge, information and belief, save 
for (a) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent 
under paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) 
granted by the Stock Exchange to permit the Company to allocate certain Offer Shares in 
the International Offering to certain permitted existing shareholders and/or their close 
associates; and (b) a consent under Chapter 4.15 of the Guide for New Listing Applicants to 
permit the Company to, among other things, allocate further H Shares in the International 
Offering to the Cornerstone Investors, existing shareholders and/or their close associates, (i) 
none of the Offer Shares subscribed by the placees and the public offer subscribers have been 
financed directly or indirectly by the Company, any of the Directors, chief executive of the 
Company, Single Largest Shareholder Group, substantial Shareholders, existing Shareholders 
of the Company or any of its subsidiaries or their respective close associates; (ii) none of 
the placees and the public offer subscribers who have subscribed for or purchased the Offer 
Shares are accustomed to taking instructions from the Company, any of the Directors, chief 
executive of the Company, Single Largest Shareholder Group, substantial Shareholders, 
existing Shareholders of the Company or any of its subsidiaries or their respective close 
associates in relation to the acquisition, disposal, voting or other disposition of H Shares 
registered in his/her/its name or otherwise held by him/her/it; (iii) there is no side agreement 
or arrangement between the Company, any of the Directors, chief executive of the Company, 
Single Largest Shareholder Group, substantial Shareholders, existing Shareholders of the 
Company or any of its subsidiaries or their respective close associates, on one hand, and 
the public offer subscribers or the placees who have subscribed for or purchased the Offer 
Shares, on the other hand; (iv) there is no side agreement or arrangement between the 
Company, any of the Directors, chief executive of the Company, Single Largest Shareholder 
Group, substantial Shareholders, existing Shareholders of the Company or any of its 
subsidiaries or their respective close associates, on one hand, and any other parties, on the 
other hand, in connection with the subscription, purchase, disposal, turnover or valuation of 
the H Shares (which, for the avoidance of doubt, does not include agreements entered into 
with the Stabilizing Manager); and (v) no rebate has been, directly or indirectly, provided 
by the Company, any of the Directors, chief executive of the Company, Single Largest 
Shareholder Group, substantial Shareholders, existing Shareholders of the Company or any 
of its subsidiaries or their respective close associates, or syndicate members, or any other 
brokers involved in the Global Offering, to any investors in the Hong Kong Public Offering or 
placees in the International Offering.

<<<PAGE 7>>>
– 7 –
The placees in the International Offering include the following:
Cornerstone Investor
Investor(1)
No. of Offer 
Shares 
allocated(2)
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)(3)
% of total issued 
share capital in 
the Company 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing 
Shareholders 
or their close 
associates
Temasek
809,350
6.82%
0.45%
No(4)
Sunpeak Asset
719,450
6.06%
0.40%
No
IvyRock
539,550
4.54%
0.30%
No
E Fund Management
173,550
1.46%
0.10%
Yes
E Fund HK(5)
6,250
0.05%
0.003%
Yes
CIG
179,850
1.51%
0.10%
No
Winner Global Fund
269,750
2.27%
0.15%
No
Wind Sabre
179,850
1.51%
0.10%
No
Vestide Lumir
179,850
1.51%
0.10%
No
Arrowpoint
134,850
1.14%
0.08%
No
Sino Opulence Fund
71,900
0.61%
0.04%
No
Roofer Asset Management
55,750
0.47%
0.03%
No
Bloom Capital
53,950
0.45%
0.03%
No
Mr. Lai Pak Lam
539,550
4.54%
0.30%
No
Mr. Xia Shengli
126,100
1.06%
0.07%
Yes
Mr. Zhu Guodong
89,900
0.76%
0.05%
No
Mr. Zheng Xiaofeng
50,450
0.42%
0.03%
Yes
Total
4,179,950
35.20%
2.33%

<<<PAGE 8>>>
– 8 –
Investor(1)
No. of Offer 
Shares 
allocated(2)
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)(3)
% of total issued 
share capital in 
the Company 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing 
Shareholders 
or their close 
associates
Notes:
1. 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone 
Investors” of the Prospectus.
2. 
Only taking into account the Offer Shares allocated to the relevant investors as Cornerstone Investors 
under the Global Offering. In addition to the Offer Shares subscribed for as Cornerstone Investors, 
certain Cornerstone Investors and/or their respective close associates were allocated further Offer 
Shares as placees in the International Offering. Please refer to the section headed “Allotment Results 
Details — International Offering — Allottees with Waivers/Consents Obtained” in this announcement 
for details. Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-up as 
indicated below. For details, please refer to the section headed “Lock-up Undertakings — Cornerstone 
Investors” in this announcement.
3. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering (assuming the Over-allotment Option is not exercised).
4. 
Temasek was an existing Shareholder of the Company and held less than 1% of the Company’s total 
issued share capital as of September 11, 2026, being the Latest Practicable Date as defined in the 
Prospectus. As of September 18, 2026, Temasek no longer held any A Share of the Company.
5. 
E Fund HK is a wholly-owned subsidiary of E Fund Management.

<<<PAGE 9>>>
– 9 –
Allottees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares 
allocated
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)(3)
% of total issued 
share capital in 
the Company 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)(4)
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 
1C(2) of the Placing Guidelines in relation to subscription for H Shares by Existing Minority Shareholders 
holding 1% or more of the issued share capital of the Company immediately prior to the completion of the 
Global Offering and/or their close associates(5)
Nil
Nil
Nil
Nil
Nil
Allottees with consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of 
further H Shares to existing Shareholders and Cornerstone Investors and/or their close associates(1)
Temasek
809,350
6.82%
0.45%
A Cornerstone Investor(6)
E Fund Management
173,550
1.46%
0.10%
A Cornerstone Investor 
and a close associate of an 
existing Shareholder
E Fund HK(10)
6,250
0.05%
0.003%
A Cornerstone Investor 
and a close associate of an 
existing Shareholder
Mr. Xia Shengli(7)
73,200
0.62%
0.04%
A Cornerstone Investor 
and a close associate of an 
existing Shareholder
Sunpeak Asset
215,800
1.82%
0.12%
A Cornerstone Investor
CIG
179,850
1.51%
0.10%
A Cornerstone Investor
Jin Peilin
13,050
0.11%
0.01%
A close associate of 
Winner Global Fund, a 
Cornerstone Investor(8)
Wind Sabre
179,850
1.51%
0.10%
A Cornerstone Investor
Arrowpoint
134,850
1.14%
0.08%
A Cornerstone Investor

<<<PAGE 10>>>
– 10 –
Investor
No. of Offer 
Shares 
allocated
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)(3)
% of total issued 
share capital in 
the Company 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)(4)
Relationship
RIME Capital Limited
49,450
0.42%
0.03%
A close associate of 
Sino Opulence Fund, a 
Cornerstone Investor(9)
Roofer Asset Management
54,800
0.46%
0.03%
A Cornerstone Investor
Bloom Capital
35,950
0.30%
0.02%
A Cornerstone Investor
Mr. Lai Pak Lam
539,550
4.54%
0.30%
A Cornerstone Investor
Mr. Zhu Guodong
179,850
1.51%
0.10%
A Cornerstone Investor
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients and/or Cornerstone Investors(2)
GF Securities Asset 
Management (Guangdong) 
Co., Ltd. (“GF Securities 
AM”)
53,900
0.45%
0.03%
Connected client as a 
placee
Huatai Capital Investment 
Limited (“HTCI”)
27,100
0.23%
0.02%
Connected client as a 
placee
Fullgoal Fund 
Management Co., Ltd. 
(“Fullgoal Fund”)
143,000
1.20%
0.08%
Connected client as a 
placee
HuaAn Fund Management 
Co., Ltd (“HuaAn Fund”)
250
0.002%
0.0001%
Connected client as a 
placee
E Fund Management
173,550
1.46%
0.10%
Connected client as a 
Cornerstone Investor
173,550
1.46%
0.10%
Connected client as a 
placee
E Fund HK(10)
6,250
0.05%
0.003%
Connected client as a 
Cornerstone Investor
6,250
0.05%
0.003%
Connected client as a 
placee

<<<PAGE 11>>>
– 11 –
Investor
No. of Offer 
Shares 
allocated
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)(3)
% of total issued 
share capital in 
the Company 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)(4)
Relationship
China Southern Asset 
Management Co., Ltd. 
(“China Southern”)
143,000
1.20%
0.08%
Connected client as a 
placee
Bosera Asset Management 
(International) Co., 
Limited (“Bosera AM”)
250
0.002%
0.0001%
Connected client as a 
placee
Victory Privilege Fund 
OFC – Winner Global 
Fund (“Winner Global 
Fund”)
269,750
2.27%
0.15%
Connected client as a 
Cornerstone Investor
Notes:
1. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents 
the number of Offer Shares allocated to the investors as placees in the International Offering. For 
allocations of Offer Shares to the relevant investors as Cornerstone Investors, please refer to the 
section headed “Allotment Results Details — International Offering — Cornerstone Investors” in this 
announcement. For details of the consent under Chapter 4.15 of the Guide for New Listing Applicants 
in relation to allocations of further H Shares to the existing Shareholders, Cornerstone Investors and/or 
their close associates, please refer to the section headed “Others/Additional Information — Allocations 
of Offer Shares to the existing Shareholders, Cornerstone Investors and/or their close associates with a 
consent under Chapter 4.15 of the Guide for New Listing Applicants” in this announcement.
2. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations to connected clients, please refer to the 
section headed “Others/Additional Information — Placing to connected clients with a prior consent 
under paragraph 1C(1) of the Placing Guidelines” in this announcement.
3. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering (assuming the Over-allotment Option is not exercised).
4. 
Not taking into account any A Shares held by the relevant investors.

<<<PAGE 12>>>
– 12 –
Investor
No. of Offer 
Shares 
allocated
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)(3)
% of total issued 
share capital in 
the Company 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)(4)
Relationship
5. 
Among the Cornerstone Investors, Temasek, Mr. Xia Shengli, Mr. Zheng Xiaofeng, E Fund were either 
existing minority Shareholders or their respective close associates, none of which held 1% or more 
of the total issued share capital of the Company as of the Latest Practicable Date as defined in the 
Prospectus. The Stock Exchange has granted a waiver from strict compliance with the requirements 
under Rule 10.04 of the Listing Rules and consent under Paragraph 1C(2) of the Placing Guidelines to 
permit H Shares in the International Offering to be placed to such Existing Minority Shareholders (as 
defined below) and/or their close associates. Please refer to the section headed “Waivers from Strict 
Compliance with the Listing Rules — Allocation of H Shares to Existing Minority Shareholders and 
Their Close Associates” of the Prospectus for details.
The Stock Exchange has granted the waiver on the condition that, among others, details of the 
allocation to the Existing Minority Shareholders (as defined below) and/or their close associates 
holding more than 1% of the issued share capital of the Company immediately prior to the completion 
of the Global Offering will be disclosed in the Prospectus and/or allotment results announcement.
6. 
Temasek was an existing Shareholder of the Company and held less than 1% of the Company’s total 
issued share capital as of September 11, 2026, being the Latest Practicable Date as defined in the 
Prospectus. As of September 18, 2026, Temasek no longer held any A Share of the Company.
7. 
Mr. Xia Shengli will subscribe for the Offer Shares through its asset manager (QDII) Shanghai 
International Trust Corp., Ltd. (上海國際信託有限公司).
8. 
Winner Global Fund is a sub-fund of Victory Privilege Fund OFC. Jin Peilin holds more than 30% 
interest of Winner Global Fund and Victory Privilege Fund OFC.
9. 
RIME Capital Limited is the sub-manager of and therefore a close associate of Sino Opulence Fund, a 
Cornerstone Investor.
10. 
E Fund HK is a wholly-owned subsidiary of E Fund Management.

<<<PAGE 13>>>
– 13 –
LOCK-UP UNDERTAKINGS
Single Largest Shareholder Group
Name
Number of 
shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings(1)
Mr. Dai Jun(2)
6,593,408
3.67%
March 28, 2027
Yuanjiesheng(2)
39,657,240
22.10%
March 28, 2027
Ningbo Kejun(2)
6,483,740
3.61%
March 28, 2027
Total
52,734,388
29.38%
Notes:
1. 
The expiry date of the lock-up period shown in the table above is pursuant to applicable relevant 
lock-up undertakings as disclosed in the Prospectus.
2. 
For illustrative purposes only, this subsection lists only those members of the Single Largest 
Shareholder Group who hold Shares directly in the Company. Mr. Dai Jun is a direct beneficial owner 
of 6,593,408 Shares of the Company and controls voting rights of 39,657,240 Shares of the Company 
through Yuanjiesheng and 6,483,740 Shares of the Company through Ningbo Kejun. Both Yuanjiesheng 
and Ningbo Kejun are ultimately controlled by Mr. Dai Jun.
Therefore, upon Listing, Mr. Dai Jun, Yuanjiesheng and Ningbo Kejun will constitute the Single Largest 
Shareholder Group and each of them is subject to the same lock-up as disclosed above. For further 
details, please refer to “Relationship with our Single Largest Shareholder Group” in the Prospectus.

<<<PAGE 14>>>
– 14 –
Cornerstone Investors
Name
Number of 
shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)(1)
% of total issued 
share capital in 
the Company 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject to the 
lock-up undertakings(2)
Temasek
809,350
6.82%
0.45%
March 28, 2027
Sunpeak Asset
719,450
6.06%
0.40%
March 28, 2027
IvyRock
539,550
4.54%
0.30%
March 28, 2027
E Fund Management
173,550
1.46%
0.10%
March 28, 2027
E Fund HK(3)
6,250
0.05%
0.003%
March 28, 2027
CIG
179,850
1.51%
0.10%
March 28, 2027
Winner Global Fund
269,750
2.27%
0.15%
March 28, 2027
Wind Sabre
179,850
1.51%
0.10%
March 28, 2027
Vestide Lumir
179,850
1.51%
0.10%
March 28, 2027
Arrowpoint
134,850
1.14%
0.08%
March 28, 2027
Sino Opulence Fund
71,900
0.61%
0.04%
March 28, 2027
Roofer Asset Management
55,750
0.47%
0.03%
March 28, 2027
Bloom Capital
53,950
0.45%
0.03%
March 28, 2027
Mr. Lai Pak Lam
539,550
4.54%
0.30%
March 28, 2027
Mr. Xia Shengli
126,100
1.06%
0.07%
March 28, 2027
Mr. Zhu Guodong
89,900
0.76%
0.05%
March 28, 2027
Mr. Zheng Xiaofeng
50,450
0.42%
0.03%
March 28, 2027
Total
4,179,950
35.20%
2.33%
Notes:
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering.
2. 
Pursuant to the relevant cornerstone investment agreements, each of the Cornerstone Investors has 
agreed that it will not, whether directly or indirectly, at any time during the period of six months from 
(and inclusive of) the Listing Date, dispose of, in any way, any of the Offer Shares or any interest in 
any company or entity holding such Offer Shares that they have purchased pursuant to the relevant 
Cornerstone Investment Agreement, save for certain limited circumstances. For details, please refer 
to the section headed “Cornerstone Investors — Restrictions on the Cornerstone Investors” of the 
Prospectus. The Cornerstone Investors will cease to be prohibited from disposing of or transferring 
Shares subscribed for pursuant to the relevant cornerstone investment agreements after the indicated 
date.
3. 
E Fund HK is a wholly-owned subsidiary of E Fund Management.

<<<PAGE 15>>>
– 15 –
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
 Option is fully
 exercised)
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
 exercised)
Number of
 H Shares held
 upon Listing
% of
 total issued
 H share
 capital upon
 Listing
 (assuming no
 exercise of the
 Over-allotment
 Option)
% of
 total issued
 H share
 capital upon
 Listing
 (assuming the
 Over-allotment
 Option is fully
 exercised)
% of
 total issued
 share capital
 upon Listing
 (assuming no
 exercise of the
 Over-allotment
 Option)
% of
 total issued
 share capital
 upon Listing
 (assuming the
 Over-allotment
 Option is fully
 exercised)
Top 1
1,618,700
15.14%
12.98%
13.63%
11.85%
1,618,700
13.63%
11.85%
0.90%
0.89%
Top 5
5,071,050
47.44%
40.67%
42.70%
37.13%
5,071,050
42.70%
37.13%
2.83%
2.80%
Top 10
6,972,400
65.23%
55.91%
58.71%
51.05%
6,972,400
58.71%
51.05%
3.88%
3.85%
Top 25
10,327,800
96.63%
82.82%
86.96%
75.62%
10,327,800
86.96%
75.62%
5.75%
5.70%
* 
Ranking of placees is based on the number of Offer Shares allotted to the placees.
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
 exercised)
Number of
 H Shares held
 upon Listing
% of
 total issued
 H share
 capital upon
 Listing
 (assuming no
 exercise of the
 Over-allotment
 Option)
% of
 total issued
 H share
 capital upon
 Listing
 (assuming the
 Over-allotment
 Option is fully
 exercised)
% of
 total issued
 share capital
 upon Listing
 (assuming no
 exercise of the
 Over-allotment
 Option)
% of
 total issued
 share capital
 upon Listing
 (assuming the
 Over-allotment 
Option is fully
 exercised)
Top 1
1,618,700
15.14%
12.98%
13.63%
11.85%
1,618,700
13.63%
11.85%
0.90%
0.89%
Top 5
5,071,050
47.44%
40.67%
42.70%
37.13%
5,071,050
42.70%
37.13%
2.83%
2.80%
Top 10
6,972,400
65.23%
55.91%
58.71%
51.05%
6,972,400
58.71%
51.05%
3.88%
3.85%
Top 25
10,327,800
96.63%
82.82%
86.96%
75.62%
10,327,800
86.96%
75.62%
5.75%
5.70%
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholder upon Listing.

<<<PAGE 16>>>
– 16 –
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
 exercised)
Number of
 H Shares held
 upon Listing
Number of
 Shares held
 upon Listing
% of
 total issued
 share capital
 upon Listing
 (assuming no
 exercise of the
 Over-allotment
 Option)
% of
 total issued
 share capital
 upon Listing
 (assuming the
 Over-allotment
 Option is fully
 exercised)
Top 1
–
0.00%
0.00%
0.00%
0.00%
–
52,734,388
29.38%
29.09%
Top 5
359,600
3.36%
2.88%
3.03%
2.63%
359,600
63,498,497
35.38%
35.03%
Top 10
3,992,650
37.35%
32.02%
33.62%
29.23%
3,992,650
69,722,754
38.85%
38.46%
Top 25
5,808,950
54.35%
46.58%
48.91%
42.53%
5,808,950
79,961,429
44.55%
44.11%
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon 
Listing.

<<<PAGE 17>>>
– 17 –
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 13,075 valid 
applications made by the public will be conditionally allocated on the basis set out below:
NO. OF 
H SHARES
APPLIED FOR
NO. OF
VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE 
ALLOTTED
OF THE TOTAL 
NO. OF H SHARES 
APPLIED FOR
POOL A
50
7,265
2,543 out of 7,265 applicants to receive 50 H Shares
35.00%
100
1,794
738 out of 1,794 applicants to receive 50 H Shares
20.57%
150
358
206 out of 358 applicants to receive 50 H Shares
19.18%
200
393
267 out of 393 applicants to receive 50 H Shares
16.98%
250
396
317 out of 396 applicants to receive 50 H Shares
16.01%
300
142
128 out of 142 applicants to receive 50 H Shares
15.02%
350
69
68 out of 69 applicants to receive 50 H Shares
14.08%
400
79
50 H Shares
12.50%
450
68
50 H Shares plus 8 out of 68 applicants to receive additional 50 H Shares
12.42%
500
723
50 H Shares plus 159 out of 723 applicants to receive additional 50 H Shares
12.20%
600
144
50 H Shares plus 64 out of 144 applicants to receive additional 50 H Shares
12.04%
700
103
50 H Shares plus 65 out of 103 applicants to receive additional 50 H Shares
11.65%
800
89
50 H Shares plus 72 out of 89 applicants to receive additional 50 H Shares
11.31%
900
62
50 H Shares plus 61 out of 62 applicants to receive additional 50 H Shares
11.02%
1,000
336
100 H Shares
10.00%
1,500
168
100 H Shares plus 166 out of 168 applicants to receive additional 50 H 
Shares
9.96%
2,000
132
150 H Shares
7.50%
2,500
120
150 H Shares plus 60 out of 120 applicants to receive additional 50 H Shares
7.00%
3,000
71
200 H Shares
6.67%
3,500
39
200 H Shares plus 21 out of 39 applicants to receive additional 50 H Shares
6.48%
4,000
40
250 H Shares
6.25%
4,500
21
250 H Shares plus 13 out of 21 applicants to receive additional 50 H Shares
6.24%
5,000
98
300 H Shares
6.00%
6,000
28
350 H Shares
5.83%
7,000
37
400 H Shares
5.71%
8,000
20
450 H Shares
5.63%
9,000
20
500 H Shares
5.56%
10,000
153
550 H Shares
5.50%
 
Total
12,968
Total number of Pool A successful applicants: 6,818
 

<<<PAGE 18>>>
– 18 –
NO. OF 
H SHARES
APPLIED FOR
NO. OF
VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE 
ALLOTTED
OF THE TOTAL 
NO. OF H SHARES 
APPLIED FOR
POOL B
20,000
66
3,000 H Shares
15.00%
30,000
7
4,300 H Shares
14.33%
40,000
9
5,650 H Shares
14.13%
50,000
17
6,950 H Shares
13.90%
100,000
4
13,800 H Shares
13.80%
150,000
3
20,500 H Shares
13.67%
593,800
1
80,000 H Shares
13.47%
 
Total
107
Total number of Pool B successful applicants: 107
 
As of the date of this announcement, the relevant subscription monies previously deposited 
in the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in 
respect of which consent has been obtained, the Company has complied with the Listing Rules 
and guidance materials in relation to the placing, allotment and listing of the Company’s H 
Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by 
the placees or the public (as the case may be) directly or indirectly for each Offer Share 
subscribed for or purchased by them was the same as the final Offer Price in addition to any 
brokerage, AFRC transaction levy, SFC transaction levy and Stock Exchange trading fee 
payable.

<<<PAGE 19>>>
– 19 –
OTHERS/ADDITIONAL INFORMATION
Allocation of H Shares to Existing Minority Shareholders and/or their close associates
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted to 
the Company, a waiver from strict compliance with the requirements under Rule 10.04 and 
consent under Paragraph 1C(2) of Appendix F1 to the Listing Rules to permit H Shares in the 
International Offering to be placed to certain existing minority Shareholders who (i) hold less 
than 5% of our Company’s voting rights prior to the completion of the Global Offering; and 
(ii) are not and will not become (upon the completion of the Global Offering) core connected 
persons (as defined in the Listing Rules) of our Company or the close associates of any 
such core connected person (together, the “Existing Minority Shareholders,” and each an 
“Existing Minority Shareholder”) on the following conditions:
(i) 
each Existing Minority Shareholder to whom our Company may allocate the H Shares in 
the International Offering holds less than 5% of our Company’s voting rights prior to the 
completion of the Global Offering;
(ii) each Existing Minority Shareholder is not, and will not be, a core connected person of 
our Company or any close associate of any such core connected person immediately 
prior to or following the Global Offering;
(iii) none of the Existing Minority Shareholders has the right to appoint any Directors and/or 
any other special rights;
(iv) allocation to the Existing Minority Shareholders and/or their close associates will not 
affect our Company’s ability to satisfy the public float requirement as prescribed under 
Rule 8.08 of the Listing Rules (as amended and replaced by Rule 19A.13A(2) of the 
Listing Rules) or otherwise approved by the Stock Exchange;
(v) 
our Company shall confirm to the Stock Exchange in writing that:
(a) 
in the case of participation as cornerstone investors, no preferential treatment 
has been, nor will be, given to the Existing Minority Shareholders or their close 
associates by virtue of their relationship with our Company, other than the 
preferential treatment of assured entitlement under a cornerstone investment 
following the principles set out in Chapter 4.15 of the Guide for New Listing 
Applicants, and the Existing Minority Shareholders or their close associates’ 
cornerstone investment agreements do not contain any material terms which are 
more favorable to the Existing Minority Shareholders or their close associates than 
those in other cornerstone investment agreements; or
(b) 
in the case of participation as placees, no preferential treatment has been, nor will 
be, given to the Existing Minority Shareholders or their close associates, by virtue 
of their relationship with our Company in any allocation in the placing tranche;

<<<PAGE 20>>>
– 20 –
(vi) in the case of participation as placees, the Sponsor-Overall Coordinators will confirm 
to the Stock Exchange that, to the best of their knowledge and belief, no preferential 
treatment has been, nor will be, given to the Existing Minority Shareholders or their 
close associates by virtue of their relationship with our Company in any allocation in the 
placing tranche; and
(vii) the Joint Sponsors shall confirm to the Stock Exchange that to the best of their 
knowledge and belief, they have no reason to believe that any of the Existing Minority 
Shareholders received any preferential treatment by virtue of their relationship with our 
Company, and details of the allocation to the Existing Minority Shareholders holding 1% 
or more of the issued share capital of our Company immediately prior to the completion 
of the Global Offering will be disclosed in the prospectus and/or the allotment results 
announcement, as the case may be.
Please refer to the section headed “Waivers from Strict Compliance with the Listing Rules – 
Allocation of H Shares to Existing Minority Shareholders and Their Close Associates” in the 
Prospectus for further details of the waiver and consent.
Each of the Joint Sponsors and the Company has provided the required confirmations as 
elaborated in the Prospectus. In particular, as the Company’s A Shares are listed on the 
Shenzhen Stock Exchange since January 2019, the Company has a highly extensive base 
of existing Shareholders and disclosure of details of allocations to all Existing Minority 
Shareholders and/or their respective close associates will not be meaningful to investors, the 
proposed disclosure threshold, i.e. condition (e) of the waiver and consent which provides that 
details of the allocation to the Existing Minority Shareholders and/or their respective close 
associates holding more than 1% of the issued share capital of the Company immediately 
prior to the completion of the Global Offering will be disclosed in this announcement, is 
appropriate.
All allocations of Offer Shares to the Existing Minority Shareholders are in compliance with 
all the conditions under the waiver and consent granted by the Stock Exchange.
Allocations of Offer Shares to the existing Shareholders, Cornerstone Investors and/or 
their close associates with a consent under Chapter 4.15 of the Guide for New Listing 
Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 
4.15 of the Guide for New Listing Applicants to permit the Company to allocate further Offer 
Shares in the International Offering to certain Cornerstone Investors, existing shareholders 
and/or their close associates, as placees, subject to the following conditions (“Allocation to 
Size-based Exemption Participants”):
(a) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a 
total value of at least HK$1 billion;
(b) 
the Offer Shares allocated to all existing Shareholders and their close associates (whether 
as cornerstone investors and/or as placees) as permitted under the Size-based Exemption 
(as defined in the Guide for New Listing Applicants) do not exceed 30% of the total 
number of the H Shares offered under the Global Offering;

<<<PAGE 21>>>
– 21 –
(c) 
each Director and chief executive of the Company has confirmed that no H Shares will 
be allocated to them or their respective close associates under the Size-based Exemption;
(d) 
the Allocation to the Size-based Exemption Participants is not expected to affect the 
Company’s ability to satisfy its public float requirement; and
(e) 
details of the Allocation to the Size-based Exemption Participants under the Size-based 
Exemption will be disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to existing Shareholders, Cornerstone Investors 
and/or their close associates, please refer to the section headed “Allotment Results Details — 
International Offering — Allottees with Waivers/Consents Obtained” in this announcement.
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of 
their connected distributors pursuant to the Placing Guidelines. The Company has applied 
to the Stock Exchange for, and the Stock Exchange has granted, consents under paragraph 
1C(1) of the Placing Guidelines to permit the Company to allocate such Offer Shares in 
the International Offering to the connected clients. The allocation of Offer Shares to such 
connected clients is in compliance with all the conditions under the consent granted by the 
Stock Exchange. Details of the placement to connected clients are set out below:

<<<PAGE 22>>>
– 22 –
Part A – Connected Clients holding the beneficial interest of the Offer Shares on a 
non-discretionary basis on behalf of independent third parties
No.
Connected 
Distributor
Connected Client
Relationship with the 
Connected Distributor
Whether the 
Connected Client 
is a collective 
investment 
scheme which is 
not authorised 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of
 such scheme
Number of
 Offer Shares
 allocated
 to the
 connected
 client
% of
 total issued
 H Shares
 after the
 Global
 Offering
 (assuming the
 Over-allotment
 Option is not
 exercised)
% of
 total issued
 share capital
 in the
 Company
 after the
 Global
 Offering
 (assuming the
 Over-allotment
 Option is not
 exercised)
1.
GF Securities 
(Hong Kong) 
Brokerage 
Limited (“GF 
Securities 
(Hong Kong) 
Brokerage”)
GF Securities Asset 
Management 
(Guangdong) 
Co., Ltd. (“GF 
Securities AM”)
GF Securities AM is a 
member of the same 
group of companies as GF 
Securities (Hong Kong) 
Brokerage
No
53,900
0.45%
0.03%
2.
Huatai Financial 
Holdings (Hong 
Kong) Limited 
(“HTFH”)
Huatai Capital 
Investment Limited 
(“HTCI”)
HTCI is a member of the 
same group of companies 
as HTFH
No
27,100
0.23%
0.02%
Notes:
1. 
The ultimate client of GF Securities AM (the “GF Securities AM Ultimate Client”) has engaged GF 
Securities AM, an asset manager that is qualified domestic institutional investor as approved by the 
relevant PRC authority, in the name of the asset management plans as disclosed below, to subscribe for 
and hold the Offer Shares as a placee under the International Offering on behalf of the GF Securities AM 
Ultimate Client on a non-discretionary basis. GF Securities AM, in the name of the asset management 
plans as disclosed below, will hold the legal title of the Offer Shares, and the economic risks and return of 
the Offer Shares will pass through to the GF Securities AM Ultimate Client.
Details of the GF Securities AM Ultimate Client are set out as below:
Name of the GF Securities AM Ultimate Clients
Name of the asset management plan
ICBC Wealth Management Co., Ltd., whose ultimate beneficial 
owner is Industrial and Commercial Bank of China Limited 
(HKEx: 01398)
ICBC – GF Asset Management Hong Kong 
Strategy No. 3 Single Asset Management Plan
As confirmed by GF Securities AM, (i) the Offer Shares to be placed to GF Securities AM are to be held 
on a non-discretionary basis on behalf of independent third parties, and (ii) each of the GF Securities AM 
Ultimate Client and its ultimate beneficial owner is an independent third party of GF Securities AM, GF 
Securities (Hong Kong) Brokerage and the companies which are members of the same group of companies 
as GF Securities (Hong Kong) Brokerage.

<<<PAGE 23>>>
– 23 –
2. 
HTFH is an Overall Coordinator in connection with the Global Offering. Pursuant to an ISDA Agreement 
(the “ISDA Agreement”), HTCI, which intends to participate in the Global Offering as a placee, will hold 
the beneficial interest of the Shares on a non-discretionary basis as the single underlying holder under 
a back-to-back total return swap (the “Back-to-back TRS”) to be entered by HTCI in connection with a 
Client TRS (as defined below) placed by and fully funded (i.e. with no financing provided by HTCI) by 
Open Wealth Management Limited, an offshore investor and the underlying client (the “Huatai Ultimate 
Client”), by which, HTCI will, subject to customary fees and commissions, pass the full economic exposure 
of the Shares to the Huatai Ultimate Client, which in effect, HTCI will hold the beneficial interest of the 
Shares on behalf of the Huatai Ultimate Client. Accordingly, HTCI is considered as a “connected client” 
of HTFH pursuant to paragraph 13(7) of the Placing Guidelines.
The Huatai Ultimate Client will place a total return swap order (the “Client TRS”) with HTCI in 
connection with the Company’s IPO. In order to hedge its exposure under the Client TRS, HTCI 
participates in the Company’s IPO and subscribes the Shares through placing order with HTFH during 
the International Offering.
The ultimate beneficial owner holding 30% or more interest in the Huatai Ultimate Client is YOU Yiyang. 
To the best knowledge of HTCI and after making all reasonable enquiries, the Huatai Ultimate Client is 
an independent third party of (i) the Company, the connected person or the associates thereof, and (ii) 
HTCI, HTFH and the companies which are members of the same group of HTCI.
The purpose of HTCI to subscribe for the Shares is for hedging the Client TRS order placed by the Huatai 
Ultimate Client. Pursuant to the terms of the Client TRS, during the tenor of the Client TRS, subject to 
customary fees and commissions, all economic returns of the Shares will be passed to the Huatai Ultimate 
Client through the Client TRS and all economic loss shall be borne by the Huatai Ultimate Client. HTCI 
will not take any economic return or bear any economic loss in relation to the Shares.
The Huatai Ultimate Client may exercise an early termination right to terminate the Client TRS at any time 
from the issue date of the Client TRS which should be on or after the date on which the Shares are listed 
on the Stock Exchange at its own discretion. Upon the termination upon maturity or early termination of 
the Client TRS by the Huatai Ultimate Client, HTCI will dispose the Shares on the secondary market and 
the Huatai Ultimate Client will receive a final settlement amount of the Client TRS in cash in accordance 
with the terms and conditions of the Client TRS which should have taken into account all the economic 
returns or economic loss in relation to the Shares. If upon the maturity of the Client TRS, the Huatai 
Ultimate Client intends to extend the investment period, subject to further agreement between HTCI and 
the relevant Huatai Ultimate Client, the term of the Client TRS could be extended by way of a new issuance 
or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Shares by itself, and pass 
through the economic exposure to the Huatai Ultimate Client, being a client who places a Client TRS 
order with HTCI in connection with the IPO of the Company. HTCI will not exercise the voting right of 
the Shares during the tenor of the Client TRS.
During the life of the Client TRS, HTCI may continue to hold the Shares in its custodian account, or to 
hold some or all of the Shares in a prime brokerage account for stock borrowing purposes, where HTCI 
will lend out its holding of underlying Shares in the form of stock borrowing loans consistent with market 
practice to lower its finance costs, provided that HTCI has the ability to call back the Shares on loan 
at any time in order to satisfy its obligations under the Client TRS to ensure the economic interests are 
ultimately passed to the Huatai Ultimate Client.

<<<PAGE 24>>>
– 24 –
Part B – Connected Clients holding the beneficial interest of the Offer Shares on a 
discretionary basis on behalf of independent third parties
No.
Connected 
Distributor
Connected Client
Relationship with the 
Connected Distributor
Whether the 
Connected Client 
is a collective 
investment 
scheme which is 
not authorised 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of
 such scheme
Number of
 Offer Shares
 allocated to
 the connected
 client
% of
 total issued
 H Shares
 after the
 Global
 Offering
 (assuming the
 Over-allotment
 Option is not
 exercised)
% of
 total issued
 share capital
 in the
 Company
 after the
 Global
 Offering
 (assuming the
 Over-allotment
 Option is not
 exercised)
1.
Guotai Junan 
Securities 
(Hong Kong) 
Limited 
(“GTJA 
Securities”) 
and Haitong 
International 
Securities 
Company 
Limited 
(“Haitong 
Securities”)
Fullgoal Fund 
Management Co., 
Ltd. (“Fullgoal 
Fund”)
Fullgoal Fund is a member 
of the same group of 
companies as GTJA 
Securities and Haitong 
Securities
Yes
143,000
1.20%
0.08%
2.
GTJA Securities 
and Haitong 
Securities
HuaAn Fund 
Management Co., 
Ltd (“HuaAn 
Fund”)
HuaAn Fund is a member 
of the same group of 
companies as GTJA 
Securities and Haitong 
Securities
Yes
250
0.002%
0.0001%
3.
GF Securities 
(Hong Kong) 
Brokerage
E Fund Management
E Fund Management is 
a member of the same 
group of companies as GF 
Securities (Hong Kong) 
Brokerage
No
347,100
2.92%
0.19%
4.
GF Securities 
(Hong Kong) 
Brokerage
E Fund HK
E Fund HK is a member 
of the same group of 
companies as GF Securities 
(Hong Kong) Brokerage
Yes
12,500
0.11%
0.01%

<<<PAGE 25>>>
– 25 –
No.
Connected 
Distributor
Connected Client
Relationship with the 
Connected Distributor
Whether the 
Connected Client 
is a collective 
investment 
scheme which is 
not authorised 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of
 such scheme
Number of
 Offer Shares
 allocated to
 the connected
 client
% of
 total issued
 H Shares
 after the
 Global
 Offering
 (assuming the
 Over-allotment
 Option is not
 exercised)
% of
 total issued
 share capital
 in the
 Company
 after the
 Global
 Offering
 (assuming the
 Over-allotment
 Option is not
 exercised)
5.
HTFH
China Southern 
Asset Management 
Co., Ltd. (“China 
Southern”)
China Southern is a member 
of the same group of 
companies as HTFH
No
143,000
1.20%
0.08%
6.
CMB 
International 
Securities 
Limited 
(“CMBI”) 
and China 
Merchants 
Securities (HK) 
Co., Limited 
(“CMS”)
Bosera Asset 
Management 
(International) Co., 
Limited (“Bosera 
AM”)
Bosera AM is a member 
of the same group of 
companies as CMBI and 
CMS
Yes
250
0.002%
0.0001%
7.
Victory Securities 
Company 
Limited 
(“VSCL”)
Victory Privilege 
Fund OFC – 
Winner Global 
Fund (“Winner 
Global Fund”)
Winner Global Fund is a sub-
fund of Victory Privilege 
Fund OFC, which is 
managed by VSCL
Yes
269,750
2.27%
0.15%
Notes:
1. 
Fullgoal Fund will hold the Offer Shares in its capacity as the discretionary fund manager for and 
on behalf of the underlying clients, each of which is, to the best knowledge and belief and after due 
enquiry of Fullgoal Fund, an independent third party of the Company, its subsidiaries, Fullgoal Fund, 
GTJA Securities, Haitong Securities and the companies which are members of the same group of GTJA 
Securities and Haitong Securities.

<<<PAGE 26>>>
– 26 –
Fullgoal Fund is investing on behalf of certain collective investment schemes which are not authorised by 
the SFC, details of which are as follows:
Name of the fund/sub-fund
Whether 
the scheme 
is publicly 
marketed
Identities of the general 
partners and the 20 largest 
limited partners of the
scheme where applicable
Identity of the 
scheme administrator
Whether any investor 
holds 30% or more 
interests in the 
fund/sub-fund (Y/N)
The relationships among the 
scheme, the ultimate beneficial 
owners of the limited partners, 
the controlling shareholders of 
the applicant, and the applicant
ICBC Fullgoal China Small & 
Mid Cap (HK listed) Equity 
Fund
Yes
Not applicable as it is not in 
partnership structure
Fullgoal Fund
N
The scheme and ultimate beneficial 
owners are independent third 
parties of GTJA Securities, Haitong 
Securities, the Company and the 
Single Largest Shareholder Group 
of the Company.
CMB-FULLGOAL BLUE CHIP 
SELECTED EQUITY FUND 
(QDII)
Yes
Not applicable as it is not in 
partnership structure
Fullgoal Fund
N
The scheme and ultimate beneficial 
owners are independent third 
parties of GTJA Securities, Haitong 
Securities, the Company and the 
Single Largest Shareholder Group 
of the Company.
ICBC Fullgoal global technology 
& internet fund
Yes
Not applicable as it is not in 
partnership structure
Fullgoal Fund
N
The scheme and ultimate beneficial 
owners are independent third 
parties of GTJA Securities, Haitong 
Securities, the Company and the 
Single Largest Shareholder Group 
of the Company.
2. 
HuaAn Fund will hold the Offer Shares in its capacity as the discretionary fund manager for and on behalf 
of the underlying client, which is, to the best knowledge and belief and after due enquiry of HuaAn Fund, 
an independent third party of the Company, its subsidiaries, HuaAn Fund, GTJA Securities, Haitong 
Securities and the companies which are members of the same group of GTJA Securities and Haitong 
Securities.
HuaAn Fund is investing on behalf of a collective investment scheme which is not authorised by the SFC, 
details of which are as follows:
Name of the fund/sub-fund
Whether 
the scheme 
is publicly 
marketed
Identities of the general 
partners and the 20 largest 
limited partners of the 
scheme where applicable
Identity of the 
scheme administrator
Whether any investor 
holds 30% or more 
interests in the 
fund/sub-fund (Y/N)
The relationships among the 
scheme, the ultimate beneficial 
owners of the limited partners, 
the controlling shareholders of 
the applicant, and the applicant
HONG KONG SELECTED 
FUND
Yes
Not applicable as it is not in 
partnership structure
HuaAn Fund
N
The scheme and ultimate beneficial 
owners are independent third 
parties of GTJA Securities, Haitong 
Securities, the Company and the 
Single Largest Shareholder Group 
of the Company.

<<<PAGE 27>>>
– 27 –
3. 
E Fund Management will hold the Offer Shares in its capacity as the discretionary fund manager 
managing the funds on behalf of its investors, each of which is, to the best knowledge of E Fund 
Management, an independent third party of E Fund Management, GF Securities (Hong Kong) Brokerage 
and the companies which are members of the same group of GF Securities (Hong Kong) Brokerage.
The details of the underlying clients are as follows:
Name of ultimate clients
Ultimate beneficial owner(s) with 30% or more 
interests in the ultimate clients(if any)
E Fund Global Asset Allocation Hybrid Fund
None
E Fund Global Quality Enterprise Hybrid Fund
None
E Fund Global Growth Hybrid Fund
None
4. 
E Fund HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the 
funds on behalf of its investors, each of which is, to the best knowledge of E Fund HK, an independent 
third party of E Fund HK, GF Securities (Hong Kong) Brokerage and the companies which are members 
of the same group of GF Securities (Hong Kong) Brokerage.
In addition, E Fund HK is expected to hold the Offer Shares on behalf of the following collective 
investment schemes which are not authorised by the SFC:
Name of the fund/sub-fund
Whether 
the scheme 
is publicly 
marketed
Identities of the general 
partners and the 20 largest 
limited partners of the 
scheme where applicable
Identity of the 
scheme administrator
Whether any investor 
holds 30% or more 
interests in the 
fund/sub-fund (Y/N)
The relationships among the 
scheme, the ultimate beneficial 
owners of the limited partners, 
the controlling shareholders of 
the applicant, and the applicant
E Fund (HK) Neo Horizon 
Fund SP
No
Not applicable as the scheme 
is not a limited partnership 
structure
E Fund HK
Save as Mr. YANG 
Runji (楊潤基), an 
Independent Third 
Party, no other investor 
holds 30% or more 
interest
The scheme and ultimate beneficial 
owners are independent third 
parties of GF (Hong Kong) 
Securities Brokerage, the Company 
and the Single Largest Shareholder 
Group of the Company.
E Fund (HK) Neo Opportunity 
SP II
No
Not applicable as the scheme 
is not a limited partnership 
structure
E Fund HK
N
The scheme and ultimate beneficial 
owners are independent third 
parties of GF Securities (Hong 
Kong) Brokerage, the Company 
and the Single Largest Shareholder 
Group of the Company.
5. 
China Southern, a qualified domestic institutional investor as approved by the relevant PRC authority to 
conduct asset management business, will hold the Offer Shares as the independent agent and discretionary 
manager of certain QDII funds (the “China Southern Ultimate Clients”). China Southern has confirmed 
that, to the best of their knowledge, each of such China Southern Ultimate Clients is an independent third 
party of the Company, its subsidiaries, China Southern, HTFH and the companies which are members of 
the same group of companies as HTFH and China Southern.
The China Southern Ultimate Clients for purpose of this placing subscription include China Southern 
Hong Kong Growth Dynamic Allocation Hybrid Fund (南方香港成長靈活配置混合), China Southern 
Hong Kong Digital Economy Hybrid Initiating Fund (QDII) (南方港股數字經濟混合發起(QDII)), China 
Southern Hong Kong Select Equity Fund (南方香港LOF), China Southern China New Economy 9-Month 
Holding Period Hybrid Fund (QDII) (南方中國新興經濟9個月持有期混合(QDII)) and China Southern 
Global Dynamic Allocation Fund (南方全球精選配置股票(QDII-FOF)), for each of which no ultimate 
beneficial owner holds 30% or more interest.

<<<PAGE 28>>>
– 28 –
6. 
Bosera AM will hold the Offer Shares in its capacity as the discretionary investment manager for and 
on behalf of the underlying client, which is, to the best knowledge and belief and after due enquiry of 
Bosera AM, an independent third party of the Company, its subsidiaries, Bosera AM, CMBI, CMS and the 
companies which are members of the same group of CMBI and CMS.
The details of the underlying client are as follows:
Name of the fund/sub-fund
Whether 
the scheme 
is publicly 
marketed
Identities of the general 
partners and the 20 largest 
limited partners of the 
scheme where applicable
Identity of the 
scheme administrator
Whether any investor 
holds 30% or more 
interests in the 
fund/sub-fund (Y/N)
The relationships among the 
scheme, the ultimate beneficial 
owners of the limited partners, 
the controlling shareholders of 
the applicant, and the applicant
Fortuna Capital Management 
Limited IPO Mandate
N
Not applicable as the scheme 
is not a limited partnership 
structure
Bosera AM
Y; Yang Dehui (楊德會)
The scheme and ultimate beneficial 
owners are independent third 
parties of CMS and CMBI, the 
Company and the Single Largest 
Shareholder Group of the Company.
7. 
Winner Global Fund will hold the Offer Shares for and on behalf of the underlying clients, each of which is, 
to the best knowledge and belief and after due enquiry of Winner Global Fund, an independent third party 
of the Company, its subsidiaries, VSCL and the companies which are members of the same group of VSCL.
The details of Winner Global Fund are as follows:
Name of the fund/sub-fund
Whether 
the scheme 
is publicly 
marketed
Identities of the general 
partners and the 20 largest 
limited partners of the 
scheme where applicable
Identity of the 
scheme administrator
Whether any investor 
holds 30% or more 
interests in the 
fund/sub-fund (Y/N)
The relationships among the 
scheme, the ultimate beneficial 
owners of the limited partners, 
the controlling shareholders of 
the applicant, and the applicant
Winner Global Fund
N
Not applicable as the scheme 
is not a limited partnership 
structure
VSCL
Y; Jin Peilin 
(金沛霖) and Yang 
Yongxing (楊永興)
The scheme and ultimate beneficial 
owners are independent third 
parties of VSCL, the Company and 
the Single Largest Shareholder 
Group of the Company.

<<<PAGE 29>>>
– 29 –
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
and Hong Kong Securities Clearing Company Limited take no responsibility for the 
contents of this announcement, make no representation as to its accuracy or completeness 
and expressly disclaim any liability whatsoever for any loss howsoever arising from or in 
reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in 
or into the United States (including its territories and possessions, any state of the United 
States and the District of Columbia). This announcement does not constitute or form a part 
of any offer or solicitation to purchase or subscribe for securities in the United States. The 
securities mentioned herein have not been, and will not be, registered under the United 
States Securities Act of 1933, as amended (the “U.S. Securities Act”). The securities 
may not be offered or sold in the United States except pursuant to an exemption from the 
registration requirements of the U.S. Securities Act and in compliance with any applicable 
state securities laws, or outside the United States unless in compliance with Regulation 
S under the U.S. Securities Act. There will be no public offer of securities in the United 
States.
The Offer Shares are being offered and sold solely (1) to qualified institutional buyers 
as defined in Rule 144A under the U.S. Securities Act pursuant to an exemption from 
registration under the U.S. Securities Act and (2) outside the United States in offshore 
transactions in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation 
or offer to acquire, purchase or subscribe for securities. This announcement is not a 
prospectus. Potential investors should read the Prospectus dated September 21, 2026 issued 
by RoboTechnik Intelligent Technology Co., Ltd. for detailed information about the Global 
Offering described below before deciding whether or not to invest in the H Shares thereby 
being offered.
# 
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence 
of any of the events set out in the section headed “Underwriting — Underwriting Arrangements 
and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any 
time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
September 29, 2026).

<<<PAGE 30>>>
– 30 –
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering (assuming the Over-allotment Option 
is not exercised), based on the Offer Price of HK$436.00 per H Share, the market value of the 
H Shares that are held by the public is approximately HK$5,177.9 million, which is higher 
than the prescribed market value of the H Shares required to be held by the public of HK$3 
billion under Rule 19A.13A(2) of the Listing Rules, thereby satisfying Rule 8.08(1) (as 
amended and replaced by Rule 19A.13A) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not 
be counted towards the free float of the H Shares of the Company at the time of Listing. Based 
on the Offer Price of HK$436.00 per Share, the Company satisfies the free float requirement 
under Rule 8.08A (as amended and replaced by Rule 19A.13C) of the Listing Rules.
The Directors confirm that immediately after the completion of the Global Offering (assuming 
the Over-allotment Option is not exercised), (i) no placee will, individually, be placed more 
than 10% of the enlarged issued share capital of the Company; (ii) there will not be any 
new substantial shareholder (as defined in the Listing Rules) of the Company; (iii) the three 
largest public shareholders of the Company do not hold more than 50% of the H Shares in 
public hands at the time of the Listing in compliance with Rules 8.08(3) and 8.24 of the 
Listing Rules; and (iv) there will be at least 300 H Shareholders at the time of the Listing in 
compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, 
September 29, 2026 (Hong Kong time), provided that the Global Offering has become 
unconditional and the right of termination described in the section headed “Underwriting — 
Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus has not been exercised. Investors who trade the H Shares on 
the basis of publicly available allocation details prior to the receipt of H Share certificates or 
prior to the H Share certificates becoming valid evidence of title do so entirely at their own 
risk.

<<<PAGE 31>>>
– 31 –
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Tuesday, 
September 29, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the 
Stock Exchange will commence at 9:00 a.m. on Tuesday, September 29, 2026 (Hong Kong 
time). The H Shares will be traded in board lots of 50 H Shares each, and the stock code of the 
H Shares will be 03757.
By order of the Board
RoboTechnik Intelligent Technology Co., Ltd.
Mr. Dai Jun
Chairman of the Board, Executive Director
Hong Kong, September 28, 2026
As at the date of this announcement, Directors of the Company are: (i) Mr. Dai Jun, 
Mr. Torsten Vahrenkamp, Ms. Li Liangyu and Mr. Zhu Huaqiao as executive Directors, and 
(ii) Mr. Yan Houmin, Mr. Chen Lihu and Mr. Zhu Zhaobin as independent non-executive 
Directors.
