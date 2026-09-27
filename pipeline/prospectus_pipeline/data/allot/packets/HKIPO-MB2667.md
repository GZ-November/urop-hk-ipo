# 配发结果公告抽取任务：2667.HK Beijing Tong Ren Tang Healthcare Investment Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**06/07/2026 22:14**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0706/2026070602117.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2667.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the prospectus dated June 26, 2026 (the “Prospectus”) issued by Beijing Tong Ren Tang Healthcare 
Investment Co., Ltd. (北京同仁堂醫養投資股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an offer or an invitation to induce an 
offer by any person to acquire, purchase or subscribe for any securities of the Company. This announcement is not a 
prospectus. Potential investors should read the Prospectus for detailed information about the Company and the Global 
Offering described below before deciding whether or not to invest in the H Shares. Any investment decision in relation 
to the Offer Shares should be taken solely in reliance on the information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not, and is not intended to, constitute or form a part of any offer to sell or solicitation to purchase 
or subscribe for any securities in the United States or in any other jurisdiction. The Offer Shares have not been, and 
will not be, registered under the U.S. Securities Act of 1933, as amended (the “U.S. Securities Act”) or securities law 
of any state or other jurisdiction of the United States and may not be offered, sold, pledged or otherwise transferred 
within the United States, except pursuant to an available exemption from, or in a transaction not subject to, the 
registration requirements of the U.S. Securities Act and in compliance with any applicable state securities laws. There 
will be no public offer of the Offer Shares in the United States. The Offer Shares are being offered and sold solely 
outside the United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited 
as stabilizing manager (the “Stabilizing Manager”), its affiliates or any person acting for it, on behalf of the 
Underwriters, may over-allocate or effect transactions with a view to stabilizing or supporting the market price of 
the Shares at a level higher than that which might otherwise prevail in an open market for a limited period after the 
Listing Date. However, there is no obligation on the Stabilizing Manager, its affiliates or any person acting for it, 
to conduct any such stabilizing action, which, if commenced, will be conducted at the sole and absolute discretion 
of the Stabilizing Manager, its affiliates or any person acting for it, and may be discontinued at any time. Any such 
stabilizing activity is required to be brought to an end on the 30th day after the last date for lodging applications under 
the Hong Kong Public Offering (which is Saturday, August 1, 2026). Such stabilization action, if commenced, may be 
effected in all jurisdictions where it is permissible to do so, in each case in compliance with all applicable laws, rules 
and regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws 
of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter. 571 of the Laws of Hong 
Kong).
Potential investors should be aware that stabilizing actions cannot be taken to support the price of the Shares for longer 
than the stabilization period which will begin on the Listing Date and is expected to expire on the 30th day after the 
last day for lodging applications under the Hong Kong Public Offering (which is Saturday, August 1, 2026). After this 
date, no further stabilizing action may be taken, and demand for the H Shares and therefore the price of the H Shares 
could fall.
Potential investors of the Offer Shares should note that the Sponsor and Sole Sponsor-Overall Coordinator (for itself 
and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong Underwriting Agreement 
with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting – 
Underwriting Arrangements – Hong Kong Public Offering – Grounds for Termination” in the Prospectus at any time 
prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Tuesday, July 7, 2026).
In connection with the Global Offering, the Company is expected to grant the Over-allotment Option to the 
International Underwriters, exercisable by the Sole Overall Coordinator (for itself and on behalf of the International 
Underwriters). Pursuant to the Over-allotment Option, the International Underwriters will have the right, exercisable 
by the Sole Overall Coordinator (for itself and on behalf of the International Underwriters) at any time from the Listing 
Date until 30 days after the last day for lodging applications under the Hong Kong Public Offering (which is Saturday, 
August 1, 2026), to require the Company to issue and allot up to an additional 16,223,000 H Shares, representing 15% 
of the total number of Offer Shares, at the Offer Price, to cover over-allocations in the International Offering, if any.

<<<PAGE 2>>>
2
Beijing Tong Ren Tang Healthcare Investment Co., Ltd.
北京同仁堂醫養投資股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the 
Global Offering
:
108,153,500 H Shares (subject to the  
 Over-allotment Option)
Number of Hong Kong Offer Shares
:
10,815,500 H Shares
Number of International Offer Shares
:
97,338,000 H Shares (subject to the  
 Over-allotment Option)
Final Offer Price
:
HK$5.50 per H Share, plus brokerage 
 of 1.0%, SFC transaction levy 
 of 0.0027%, AFRC transaction levy 
 of 0.00015%, and Hong Kong 
 Stock Exchange trading fee of 0.00565%
Nominal value
:
RMB1.00 per H Share
Stock code
:
2667
Sponsor, Sole Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint 
Lead Manager
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers
Joint Lead Managers

<<<PAGE 3>>>
3
Beijing Tong Ren Tang Healthcare Investment Co., Ltd.
北京同仁堂醫養投資股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated June 26, 2026 (the “Prospectus”) issued by Beijing Tong Ren Tang Healthcare 
Investment Co., Ltd. (北京同仁堂醫養投資股份有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
2667
Stock short name
TONGRENTANGCARE
Dealings commencement date
July 7, 2026*
* See note at the end of the announcement
Price Information
Final Offer Price
HK$5.50
Offer Price Range
HK$5.48 – HK$6.21

<<<PAGE 4>>>
4
Offer Shares and Share Capital
Number of Offer Shares (assuming the Over-allotment 
Option is not exercised)
108,153,500
Number of Offer Shares in Hong Kong Public Offering
10,815,500
Number of Offer Shares in International Offering
97,338,000
Number of issued Shares upon Listing (assuming the 
Over-allotment Option is not exercised)
465,362,049
Over-allocation
No. of Offer Shares over-allocated (Note)
5,407,500
Note: Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases in the 
secondary market at prices that do not exceed the Offer Price or through deferred delivery or a combination 
of these means. In the event the Over-allotment Option is exercised, an announcement will be made on the 
Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$594.8 million
Less:  Estimated listing expenses payable based on  
Final Offer Price
HK$62.4 million
Net proceeds
HK$532.4 million
Note: Gross proceeds refer to the amount to which the issuer is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” in the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis.

<<<PAGE 5>>>
5
ALLOTMENT RESULTS DETAILS
PUBLIC OFFER
No. of valid applications
66,390
No. of successful applications
11,293
Subscription level
251.74 times
Reallocation
N/A
No. of Offer Shares initially available under the Hong Kong 
Public Offering
10,815,500
No. of Offer Shares reallocated from the International 
Offering
0
Final no. of Offer Shares under the Hong Kong Public 
Offering
10,815,500
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering
10%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can 
refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees.

<<<PAGE 6>>>
6
INTERNATIONAL OFFERING
No. of placees
75
Subscription Level
2.84 times
No. of Offer Shares initially available under the 
International Offering
97,338,000
No. of Offer Shares reallocated to the Hong Kong Public 
Offering
0
Final no. of Offer Shares under the International Offering
97,338,000
% of Offer Shares under the International Offering to the 
Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, Controlling Shareholders, 
substantial shareholders, existing shareholders of the Company or any of its subsidiaries or their 
respective close associates; and (ii) none of the placees and the public who have purchased the 
Offer Shares are accustomed to taking instructions from the Company, any of the Directors, 
chief executive of the Company, Controlling Shareholders, substantial shareholders, existing 
shareholders of the Company or any of its subsidiaries or their respective close associates in 
relation to the acquisition, disposal, voting or other disposition of H Shares registered in his/her/its 
name or otherwise held by him/her/it.

<<<PAGE 7>>>
7
The placees in the International Offering include the following:
Cornerstone Investors
Investor (Note 1)
No. of Offer 
Shares 
allocated
% of Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total 
issued H 
Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total 
issued 
Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing 
shareholders 
or their close 
associates
Airport Technology Capital
39,818,000
36.82%
18.24%
8.56%
No
Aurora SF
9,010,500
8.33%
4.13%
1.94%
No
CICCFT (in connection 
with OTC Swaps)
5,000,000
4.62%
2.29%
1.07%
No
Total
53,828,500
49.77%
24.66%
11.57%
–
Note:
1. 
For details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in the 
Prospectus.
Allottee with consent obtained
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares
% of total 
issued H 
Shares after 
the Global 
Offering
% of total 
issued 
Shares after 
the Global 
Offering
Relationship
Allottee with consent under paragraph 1C(1) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) and 
Chapter 4.15 of the Guide for New Listing Applicants in relation to allocation to a connected client Note 1
CICCFT (in connection 
with OTC Swaps)
5,000,000
4.62%
2.29%
1.07%
Connected 
client
Note:
1. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocation to a connected client, please refer to the section headed 
“Others/Additional Information – Placing to allocation to a connected client with a prior consent under 
paragraph 1C(1) of the Placing Guidelines” in this announcement.

<<<PAGE 8>>>
8
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
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
exercised)
% of total issued 
Shares after the 
Global Offering 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings Note 1
TRT
300,000,025 Shares 
(including 
52,930,500 H Shares)
24.25%
64.47%
July 6, 2027
TRT Medical Fund 
Management
1,303,079 H Shares
0.60%
0.28%
July 6, 2027
TRT Senior Care Fund
17,605,573 H Shares
8.07%
3.78%
July 6, 2027
Tongkang Fund
7,824,557 H Shares
3.58%
1.68%
July 6, 2027
Tongqing Fund
8,446,607 H Shares
3.87%
1.82%
July 6, 2027
Total
335,179,841 Shares 
(including 
88,110,316 H Shares)
40.36%
72.03%
–
Notes:
1. 
The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws and 
relevant lock-up undertakings as disclosed in the Prospectus.
2. 
For illustrative purposes, this subsection lists only those members of the Controlling Shareholders who hold 
Shares directly in the Company. Pursuant to Rules 10.07(1) of the Listing Rules, each of the Controlling 
Shareholders (namely TRT, TRT Kangyang, TRT Heritage Fund Management, TRT Medical Fund 
Management, TRT Senior Care Fund, Tongkang Fund and Tongqing Fund) has undertaken to the Company 
and the Stock Exchange that, except pursuant to the Global Offering, it shall, and procure that the relevant 
registered holders of the Shares in which it is beneficially interested, shall, comply with the applicable 
lock-up requirements. For further details, please refer to the section headed “Underwriting – Underwriting 
Arrangements – Hong Kong Public Offering – Undertakings Pursuant to the Listing Rules” in the Prospectus.

<<<PAGE 9>>>
9
Existing Shareholders (other than Controlling Shareholders) and Pre-IPO Investors
Name
Number of shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
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
exercised)
% of total 
issued Shares 
after the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings Note 1
Mr. Zhu
7,612,833 H Shares
3.49%
1.64%
July 6, 2027
Ms. Pan
6,228,682 H Shares
2.85%
1.34%
July 6, 2027
Bozhou Yipinde
3,810,077 H Shares
1.75%
0.82%
July 6, 2027
Jining Yinling
2,592,494 H Shares
1.19%
0.56%
July 6, 2027
Bingrong Investment
1,784,622 H Shares
0.82%
0.38%
July 6, 2027
Subtotal
22,028,708  H Shares
10.09%
4.73%
–
Note:
1. 
The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws and 
relevant lock-up undertakings as disclosed in the Prospectus.

<<<PAGE 10>>>
10
Cornerstone Investors
Name
Number of shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
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
exercised)
% of total 
issued Shares 
after the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings Note 1
Airport Technology Capital
39,818,000
18.24%
8.56%
February 6, 2027
Aurora SF
9,010,500
4.13%
1.94%
February 6, 2027
CICCFT (in connection 
with OTC Swaps)
5,000,000
2.29%
1.07%
February 6, 2027
Total
53,828,500
24.66%
11.57%
–
Note:
1. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on February 
6, 2027. The Cornerstone Investors will cease to be prohibited from disposing of or transferring H Shares 
subscribed for pursuant to the relevant cornerstone investment agreements after the indicated date.
As disclosed in the Prospectus, Aurora SF, one of the Cornerstone Investors, will hold the Offer Shares in 
connection with a cross border transaction placed by and fully funded by its ultimate client, Haikou Lanxin 
Zhitong Investment Center (Limited Partnership) (海口瀾鑫志同投資中心合夥企業(有限合夥)) (“Haikou 
Lanxin”), pursuant to which the full economic return and loss of the Offer Shares placed to Aurora SF will 
be ultimately borne by Haikou Lanxin according to the terms and conditions of the transactions, subject to 
customary fees and commissions.
Haikou Lanxin is a limited partnership established in the PRC, primarily engaging in investment management 
and asset management activities with a focus on healthcare and consumption industries. Haikou Lanxin is 
owned as to (i) 0.44% by its general partner, Ms. Guo Chunyan (郭春燕), an Independent Third Party; and (ii) 
99.56% by seven limited partners, none of which holds 30% or more of the partnership interest. The previous 
general partner of Haikou Lanxin was Mr. Zhang Liang (張亮), who also serves as the general partner of 
Beijing Renhuichuan Enterprise Management Development Center (Limited Partnership) (北京仁匯川企業管
理發展中心(有限合夥)) (“Beijing Renhuichuan”), a limited partner holding 35.71% partnership interest in 
Tongqing Fund.
There are four overlapping limited partners between Haikou Lanxin and Beijing Renhuichuan, namely, 
Mr. Zhan Yongqing (詹永清), Mr. Yang Junyuan (楊軍元), Mr. Lin Hai (林海) and Ms. Chen Jingyu (陳
京渝), who hold 21.33%, 21.33%, 21.33% and 2.22% partnership interests in Haikou Lanxin, respectively 
(collectively holding 66.22% partnership interest in Haikou Lanxin), and 24.69%, 19.75%, 25.93% and 2.47% 
partnership interests in Beijing Renhuichuan, respectively (collectively holding 72.84% partnership interest 
in Beijing Renhuichuan). Accordingly, through Beijing Renhuichuan’s aforementioned 35.71% interest in 
Tongqing Fund, the same four limited partners indirectly hold a 26.0% partnership interest in Tongqing Fund. 
The four overlapping limited partners are independent from each other, and there are no acting-in-concert 
arrangements among them.

<<<PAGE 11>>>
11
PLACEE CONCENTRATION ANALYSIS
Placees Note 1
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
exercised and 
new H Shares 
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
new H Shares 
are issued)
Number of 
H Shares held 
upon Listing
% of total 
issued Shares 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total 
issued Shares 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Top 1
39,818,000
40.91%
38.75%
36.82%
35.06%
39,818,000
8.56%
8.46%
Top 5
74,824,000
76.87%
72.82%
69.18%
65.89%
74,824,000
16.08%
15.89%
Top 10
97,461,000
100.13%
94.86%
90.11%
85.82%
97,461,000
20.94%
20.70%
Top 25
101,994,000
104.78%
99.27%
94.30%
89.81%
101,994,000
21.92%
21.67%
Note:
1. 
Ranking of placees is based on the number of Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders Note 1
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
exercised and 
new H Shares 
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
new H Shares 
are issued)
Number of 
H Shares 
held upon 
Listing
% of total 
issued H Shares 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total 
issued H Shares 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Number of 
Shares 
held upon 
Listing
Top 1
0
0.00%
0.00%
0.00%
0.00%
88,110,316
18.93%
18.72%
335,179,841
Top 5
66,524,000
68.34%
64.75%
61.51%
58.58%
154,634,316
33.23%
32.85%
401,703,841
Top 10
88,033,000
90.44%
85.68%
81.40%
77.52%
189,984,831
40.83%
40.36%
437,054,356
Top 25
101,574,000
104.35%
98.86%
93.92%
89.44%
211,713,024
45.49%
44.97%
458,782,549
Note:
1. 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 12>>>
12
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders Note 1
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
exercised and 
new H Shares 
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
new H Shares 
are issued)
Number of 
H Shares 
held upon 
Listing
Number of 
Shares held 
upon Listing
% of total 
issued Shares 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total 
issued Shares 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Top 1
0
0.00%
0.00%
0.00%
0.00%
88,110,316
335,179,841
72.03%
71.20%
Top 5
66,524,000
68.34%
64.75%
61.51%
58.58%
154,634,316
401,703,841
86.32%
85.33%
Top 10
88,033,000
90.44%
85.68%
81.40%
77.52%
189,984,831
437,054,356
93.92%
92.84%
Top 25
101,574,000
104.35%
98.86%
93.92%
89.44%
211,713,024
458,782,549
98.59%
97.45%
Note:
1. 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon 
Listing.
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 66,390 valid 
applications made by the public will be conditionally allocated on the basis set out below:
BASIS OF ALLOTMENT FOR PRESS ANNOUNCEMENT
NO. OF SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/ BALLOT 
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
POOL A
500
31,095
2,488 out of 31,095 to receive 500 Shares
8.00%
1,000
4,943
455 out of 4,943 to receive 500 Shares
4.60%
1,500
11,161
1,242 out of 11,161 to receive 500 Shares
3.71%
2,000
1,637
210 out of 1,637 to receive 500 Shares
3.21%
2,500
1,193
179 out of 1,193 to receive 500 Shares
3.00%
3,000
716
112 out of 716 to receive 500 Shares
2.61%
3,500
378
64 out of 378 to receive 500 Shares
2.42%
4,000
340
60 out of 340 to receive 500 Shares
2.21%
4,500
261
49 out of 261 to receive 500 Shares
2.09%
5,000
3,022
574 out of 3,022 to receive 500 Shares
1.90%
6,000
351
72 out of 351 to receive 500 Shares
1.71%
7,000
1,669
374 out of 1,669 to receive 500 Shares
1.60%

<<<PAGE 13>>>
13
NO. OF SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/ BALLOT 
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
POOL A
8,000
366
85 out of 366 to receive 500 Shares
1.45%
9,000
206
48 out of 206 to receive 500 Shares
1.29%
10,000
1,074
269 out of 1,074 to receive 500 Shares
1.25%
15,000
1,297
389 out of 1,297 to receive 500 Shares
1.00%
20,000
503
161 out of 503 to receive 500 Shares
0.80%
25,000
403
141 out of 403 to receive 500 Shares
0.70%
30,000
301
112 out of 301 to receive 500 Shares
0.62%
35,000
195
82 out of 195 to receive 500 Shares
0.60%
40,000
183
81 out of 183 to receive 500 Shares
0.55%
45,000
117
53 out of 117 to receive 500 Shares
0.50%
50,000
628
312 out of 628 to receive 500 Shares
0.50%
60,000
193
103 out of 193 to receive 500 Shares
0.44%
70,000
161
91 out of 161 to receive 500 Shares
0.40%
80,000
213
127 out of 213 to receive 500 Shares
0.37%
90,000
123
77 out of 123 to receive 500 Shares
0.35%
100,000
885
578 out of 885 to receive 500 Shares
0.33%
200,000
507
436 out of 507 to receive 500 Shares
0.21%
300,000
298
500 Shares
0.17%
400,000
220
500 Shares plus 62 out of 220 to receive additional 500 Shares
0.16%
500,000
200
500 Shares plus 116 out of 200 to receive additional 500 Shares
0.16%
600,000
126
500 Shares plus 101 out of 126 to receive additional 500 Shares
0.15%
700,000
95
1,000 Shares
0.14%
800,000
238
1,000 Shares plus 3 out of 238 to receive additional 500 Shares
0.13%
65,298
Total number of Pool A successful applicants: 10,201
POOL B
900,000
484
4,000 Shares
0.44%
1,000,000
333
4,000 Shares plus 230 out of 333 to receive additional 500 Shares
0.43%
2,000,000
110
6,000 Shares
0.30%
3,000,000
84
6,500 Shares plus 17 out of 84 to receive additional 500 Shares
0.22%
5,407,500
81
10,000 Shares
0.18%
1,092
Total number of Pool B successful applicants: 1,092

<<<PAGE 14>>>
14
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that consent has been obtained, the 
Company has complied with the Listing Rules and guidance materials in relation to the placing, 
allotment and listing of the Company’s shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Placing to a connected client with prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to a connected client of its 
connected distributor pursuant to the Placing Guidelines.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such 
Offer Shares in the International Offering to the connected client. The allocation of Offer Shares 
to such connected client is in compliance with all the conditions under the consent granted by the 
Stock Exchange. Details of the placement to connected client are set out below:

<<<PAGE 15>>>
15
No.
Connected Distributor
Connected Client
Relationship
Whether the 
connected 
clients will hold 
the beneficial 
interests of the 
Offer Shares on a 
non-discretionary 
basis or 
discretionary 
basis for 
independent third 
parties
Number 
of Offer 
Shares to 
be allocated 
to the 
Connected 
Client
Approximate 
percentage of 
total number 
of Offer 
Shares under 
the Global 
Offering
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
percentage of 
total issued 
Shares after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
1.
China International 
Capital Corporation 
Hong Kong Securities 
Limited (“CICC 
HKS”)
CICCFT
CICCFT is a member 
of the same group 
of companies as 
CICCHKS.
Non-discretionary 
basis
5,000,000
4.62%
1.07%
Note:
(1) 
CICCFT and China International Capital Corporation Limited have entered into a series of cross border over-
the-counter swap transactions (collectively, the “CICCFT OTC Swaps”) with each other, and with Guangdong 
Hengqin Guangxin Meihao Private Fund Management Co., Ltd. (廣東橫琴廣鑫美好私募基金管理有限公
司) (“Guangxinmeihao Fund”) acting in its capacity as fund manager for and on behalf of Meihao Planck 
No. 1 Private Securities Investment Fund (美好普朗克一號私募證券投資基金) (the “Planck No. 1 Fund” 
or “CICCFT Ultimate Client”), pursuant to which CICCFT will hold the Offer Shares on a nondiscretionary 
basis to hedge the CICCFT OTC Swaps while the economic risks and returns of the underlying Offer Shares are 
passed to the CICCFT Ultimate Client, subject to customary fees and commissions. The CICCFT OTC Swaps 
will be fully funded by the CICCFT Ultimate Client.
To the best of CICCFT’s knowledge having made all reasonable inquiries, Guangxinmeihao Fund and its 
ultimate beneficial owner are independent third parties of CICCFT, CICCHKS and the companies which are 
members of the same group of CICCHKS.
To the best of CICCFT’s knowledge having made all reasonable inquiries, the CICCFT Ultimate Client is an 
independent third party of CICCFT, CICCHKS and the companies which are members of the same group of 
CICCHKS.
The Planck No. 1 Fund is established as a contractual fund without a separate legal personality. Guangxinmeihao 
Fund, which is ultimately controlled by Mr. Luo Liang (羅亮), is the fund manager of Planck No. 1 Fund, 
China Merchants Securities Co., Ltd. (招商證券股份有限公司) is the fund trustee, and Ms. Li Bo (李博) and 
Mr. Xu Chen (徐琛) are the beneficiaries, all of which are independent third parties of the Group and the 
Controlling Shareholders. The Group became acquainted with Ms. Li Bo and Mr. Xu Chen through introduction 
by suppliers of the Group, Beijing Wantailike Pharmaceutical Co., Ltd. (北京萬泰利克藥業有限公司) (“Beijing 
Wantailike”) and Zhenxing Baicao (Beijing) Pharmaceutical Co., Ltd. (振興百草(北京)藥業有限責任公司) 
(“Zhenxing Baicao”), respectively, not through introduction by CICC. Beijing Wantailike and Zhenxing Baicao 
were not the five largest suppliers of the Group during the Track Record Period. For the years ended December 
31, 2023, 2024 and 2025, the Group’s purchase amount from Beijing Wantailike accounted for 0.2%, 0.3% and 
1.1% of its total purchase for the same periods, respectively. For the years ended December 31, 2023, 2024 
and 2025, the Group’s purchase amount from Zhenxing Baicao accounted for 1.3%, 1.8% and 2.2% of its total 
purchases for the same periods, respectively, and the revenue contribution of Zhenxing Baicao accounted for 
less than 1% of its total revenue for the same periods, respectively.

<<<PAGE 16>>>
16
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the 
“Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy 
or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and the 
District of Columbia). This announcement does not, and is not intended to, constitute or form a 
part of any offer to sell or solicitation to purchase or subscribe for any securities in the United 
States or in any other jurisdiction. The Offer Shares have not been, and will not be, registered 
under the U.S. Securities Act of 1933, as amended (the “U.S. Securities Act”) or securities law 
of any state or other jurisdiction of the United States and may not be offered, sold, pledged or 
otherwise transferred within the United States, except pursuant to an available exemption from, 
or in a transaction not subject to, the registration requirements of the U.S. Securities Act and in 
compliance with any applicable state securities laws. There will be no public offer of the Offer 
Shares in the United States.
The Offer Shares are being offered and sold solely outside the United States in offshore 
transactions in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an offer or an 
invitation to induce an offer by any person to acquire, purchase or subscribe for any securities 
of the Company. This announcement is not a prospectus. Potential investors should read the 
Prospectus dated June 26, 2026 issued by the Company for detailed information about the 
Company and the Global Offering described below before deciding whether or not to invest in 
the Shares. Any investment decision in relation to the Offer Shares should be taken solely in 
reliance on the information provided in the Prospectus.
*Potential investors of the Offer Shares should note that the Sponsor and Sole Sponsor-Overall 
Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall be entitled to 
terminate the Hong Kong Underwriting Agreement with immediate effect upon the occurrence 
of any of the events set out in the section headed “Underwriting – Underwriting Arrangements 
– Hong Kong Public Offering – Grounds for Termination” in the Prospectus at any time prior to 
8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Tuesday, 
July 7, 2026).

<<<PAGE 17>>>
17
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering before any exercise of the Over-allotment 
Option, 116,340,693 H Shares, the total number of the H Shares held by the public represents 
approximately 25.00% of the total issued share capital of the Company, which is at least 25% as 
required under Rule 19A.13A of the Listing Rules, will be counted towards the public float upon 
the Listing. Therefore, the Company will be able to meet the minimum public float requirement 
under Rule 19A.13A(1) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of seven months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the Shares of the Company at the time of Listing. Based on the 
final Offer Price of HK$5.50 per H Share, the Company confirms the free float requirement under 
Rule 19A.13C(1)(a) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering (before any 
exercise of the Over-allotment Option): (i) no placee will, individually, be placed more than 10% 
of the enlarged issued share capital of the Company immediately after the Global Offering; (ii) 
there will not be any new substantial Shareholder under the Listing Rules immediately after the 
Global Offering; (iii) the three largest public shareholders of the Company do not hold more than 
50% of the Shares in public hands at the time of the Listing in compliance with Rules 8.08(3) and 
8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at the time of the Listing 
in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, July 7, 2026 
(Hong Kong time), provided that the Global Offering has become unconditional and the right of 
termination described in the section headed “Underwriting – Underwriting Arrangements – Hong 
Kong Public Offering – Grounds for Termination” in the Prospectus has not been exercised. 
Investors who trade H Shares prior to the receipt of H Share certificates or the H Share certificates 
becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Tuesday, July 
7, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange will 
commence at 9:00 a.m. on Tuesday, July 7, 2026 (Hong Kong time). The H Shares will be traded 
in board lots of 500 H Shares each. The stock code of the H Shares will be 2667.
By order of the Board
Beijing Tong Ren Tang Healthcare Investment Co., Ltd.
Mr. Rao Zuhai
Chairman of the Board and Executive Director
Hong Kong, July 6, 2026
As at the date of this announcement, the Board comprises: (i) Mr. Rao Zuhai, Mr. Lu Yan and 
Ms. Gui Shan as executive directors; (ii) Mr. Zhu Feng, Mr. Sun Kai and Ms. Xing Qian as non-
executive directors; and (iii) Mr. Yim, Chi Hung Henry, Mr. Zhang Xiang and Mr. Gao Yanbin as 
independent non-executive directors.
