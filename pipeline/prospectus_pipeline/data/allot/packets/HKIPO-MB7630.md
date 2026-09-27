# 配发结果公告抽取任务：7630.HK IMPACT Therapeutics, Inc - B - H Shares

- 公告：Announcement of Final Offer Price and Allotment Results
- 刊发时间（港交所元数据）：**12/05/2026 21:52**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0512/2026051201406.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"7630.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities in 
the United States or in any other jurisdictions in which such offer or solicitation would be unlawful. The securities 
mentioned herein have not been, and will not be, registered under the United States Securities Act of 1933 as amended 
from time to time (the “U.S. Securities Act”) or any state securities law of the United States. The securities may not 
be offered, sold, pledged or transferred within the United States, except in transactions exempt from, or not subject 
to, the registration requirements of the U.S. Securities Act and in compliance with any applicable state securities 
laws. There will be no public offer of the Offer Shares in the United States. The Offer Shares are being offered and 
sold solely (1) to qualified institutional buyers as defined in Rule 144A under the U.S. Securities Act pursuant to an 
exemption from registration under the U.S. Securities Act; and (2) outside the United States in offshore transactions 
in reliance on Regulation S under the U.S. Securities Act and applicable laws of each jurisdiction where those offers 
and sales occur. This announcement is for information purposes only and does not constitute an invitation or offer to 
acquire, purchase or subscribe for securities.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus 
dated May 5, 2026 (the “Prospectus”) issued by IMPACT Therapeutics, Inc (南京英派藥業股份有限公司) (the 
“Company”) for detailed information about the Global Offering described below before deciding whether or not to 
invest in the H Shares thereby being offered. Any investment decision in relation to the Offer Shares should be taken 
solely in reliance on the information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
In connection with the Global Offering, Goldman Sachs (Asia) L.L.C., as the stabilization manager (the “Stabilization 
Manager”), or any person acting for it and on behalf of the Underwriters, may over-allocate or effect transactions with 
a view to stabilizing or supporting the market price of the Shares at a level higher than that which might otherwise 
prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilization Manager (or any 
person acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will be conducted at 
the absolute discretion of the Stabilization Manager (or any person acting for it) and in what the Stabilization Manager 
reasonably regards as the best interest of the Company, (b) may be discontinued at any time and (c) is required to be 
brought to an end within 30 days of the last day for lodging applications under the Hong Kong Public Offering. Such 
stabilization action, if commenced, may be effected in all jurisdictions where it is permissible to do so, in each case 
in compliance with all applicable laws, rules and regulatory requirements, including the Securities and Futures (Price 
Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures 
Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that stabilizing action cannot be taken to support the price of the Shares for longer 
than the stabilization period which begins on the Listing Date, and is expected to expire on Sunday, June 7, 2026, the 
30th day after the last day for the lodging of applications under the Hong Kong Public Offering. After this date, no 
further stabilizing action may be taken, demand for the Shares, and therefore the price of the Shares, could fall.
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on behalf of 
the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting
– Underwriting Arrangements – Hong Kong Public Offering – Grounds for Termination” in the Prospectus at any time 
prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Wednesday, May 13, 
2026).

<<<PAGE 2>>>
2
IMPACT Therapeutics, Inc
南京英派藥業股份有限公司
(A joint stock company established in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the Global 
Offering
:
41,977,000 H Shares (subject to the  
Over-allotment Option)
Number of Hong Kong Offer Shares
:
4,197,800 H Shares
Number of International Offer Shares
:
37,779,200 H Shares (subject to the  
Over-allotment Option)
Final Offer Price
:
HK$20.10 per H Share, plus brokerage 
of 1.0%, AFRC transaction levy of 
0.00015%, SFC transaction levy of 
0.0027% and Stock Exchange trading fee 
of 0.00565%
Nominal value
:
RMB1.00 per H Share
Stock code
:
7630
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Joint Global Coordinator,
Joint Bookrunner and Joint Lead Manager
Joint Bookrunner and Joint Lead Manager

<<<PAGE 3>>>
3
IMPACT Therapeutics, Inc
南京英派藥業股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE
 AND ALLOTMENT RESULTS
Warning: In view of high concentration of shareholding in a small number of H Shareholders, H 
Shareholders and prospective investors should be aware that the price of the H Shares could move 
substantially even with a small number of H Shares traded and should exercise extreme caution 
when dealing in the H Shares.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated May 5, 2026 (the “Prospectus”) issued by 
IMPACT Therapeutics, Inc (南京英派藥業股份有限公司) (the “Company”).
SUMMARY
Company information
Stock code
7630
Stock short name
IMPACT THERAP-B
Dealings commencement date
May 13, 2026*
* see note at the end of the announcement
Price Information
Final Offer Price
HK$20.10
Offer Price Range
HK$19.75 – HK$21.75
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the Over-allotment Option)
41,977,000
H Shares
Final Number of Offer Shares in Hong Kong Public Offering
4,197,800
H Shares
Final Number of Offer Shares in International Offering (before 
exercise of the Over-allotment Option)
37,779,200
H Shares
Number of issued Shares upon Listing (before exercise of the Over-
allotment Option)
276,165,130
Shares
Over-allocation
Number of Offer Shares over-allocated
6,296,400
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.

<<<PAGE 4>>>
4
Proceeds
Gross proceeds(Note)
HK$843.7 million
 Less: Estimated listing expenses payable based on 
     Offer Price
HK$84.2 million
Net proceeds
HK$759.5 million
Note: Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
221,788
No. of successful applications
18,774
Subscription level
2,282.4 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong Public 
Offering
4,197,800 H Shares
No. of Offer Shares reallocated from the International Offering 
(claw-back)
N/A
Final no. of Offer Shares under the Hong Kong Public Offering
4,197,800 H Shares
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering
10.00%
Note: For details of the final allocation of the H Shares to the Hong Kong Public Offering, investors 
can refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
137
Subscription level
24.58 times
No. of Offer Shares initially available under the International 
Offering
37,779,200 H Shares
No. of Offer Shares reallocated to the Hong Kong Public Offering 
(claw-back)
N/A
Final no. of Offer Shares under the International Offering
37,779,200 H Shares
% of Offer Shares under the International Offering to the Global 
Offering
90%

<<<PAGE 5>>>
5
The Directors confirm that, to the best of their knowledge, information and belief, save for 
consents under paragraphs 1C(1) and 1C(2) of Appendix F1 to the Listing Rules (the “Placing 
Guidelines”) and waivers from strict compliance with the requirements under Rules 9.09(b)(if 
applicable) and 10.04 of the Listing Rules pursuant to Chapters 2.3 and 4.15 of the Guide for 
New Listing Applicants (“Listing Guide”) granted by the Stock Exchange to permit the Company 
to, among other things, place certain H Shares in the International Offering to certain existing 
Shareholders and/or their close associates and certain connected clients, (i) none of the Offer 
Shares subscribed by the placees and the public have been financed directly or indirectly by the 
Company, any of the Directors, chief executive of the Company, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates; and (ii) 
none of the placees and the public who have purchased the Offer Shares are accustomed to taking 
instructions from the Company, any of the Directors, chief executive of the Company, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates in relation to the acquisition, disposal, voting or other disposition of H Shares 
registered in his/her/its name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
Investor Note 1
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
% of total 
issued share 
capital after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing
shareholders
or their close
associatesNote 2
Nanjing Biotech and Pharmaceutical Valley 
Construction and Development Co., Ltd. 
(“BPV”) and Huatai Capital Investment Limited 
(“HTCI”) (in connection with Huatai Back-to-
back TRS and the Huatai Client TRS)
4,775,600
11.38%
1.73%
No
Huang River Investment Limited (“Huang 
River”) Note 3
3,117,800
7.43%
1.13%
Yes
Prosper High Holding Limited (“Prosper 
High”) Note 3
776,000
1.85%
0.28%
Yes
LAV Star Limited (“LAV Star”) Note 4
974,200
2.32%
0.35%
Yes
LAV Star Opportunities Limited (“LAV 
Opportunities”) Note 4
974,200
2.32%
0.35%
Yes
Global Superior Choice Fund 1 SP (“GSC Fund 
1”) Note 5
565,000
1.35%
0.20%
No
Vision Fund 1 SP (“Vision Fund 1”) Note 5
993,800
2.37%
0.36%
No

<<<PAGE 6>>>
6
Investor Note 1
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
% of total 
issued share 
capital after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing
shareholders
or their close
associatesNote 2
Horizon Fund 1 SP (“Horizon 
Fund 1”) Note 5
194,800
0.46%
0.07%
No
Horizon Next SP (“Horizon Next Fund”) Note 5
194,800
0.46%
0.07%
No
First Quarter Moon OFC – Phecda Fund
974,200
2.32%
0.35%
No
Worldwide Healthcare Partners LLC 
(“WWHCP”) Note 6
389,600
0.93%
0.14%
Yes
Total
13,930,000
33.19%
5.03%
Notes:
(1) 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in the Prospectus.
(2) 
Among the Cornerstone Investors, WWHCP is an existing Shareholder, each of LAV Star, LAV Opportunities is a close associate of an existing 
Shareholder and a core connected person of the Company, and each of Huang River and Prosper High is a close associate of an existing 
Shareholder. The Stock Exchange has granted consents under paragraph 1C (2) of Appendix F1 of Placing Guidelines and Chapter 4.15 of the 
Listing Guide and a waiver from strict compliance from the requirements under Rule 9.09(b) and Rule 10.04 of the Listing Rules to permit each 
of WWHCP, LAV Star, LAV Opportunities, Huang River and Prosper High to participate in the International Offering as a cornerstone investor. 
Please refer to the section headed “Waivers and Exemptions – Consent and Waiver in respect of Allocation of H Shares to Certain Existing 
Shareholders and/or Their Close Associates” of the Prospectus for details.
(3) 
Tencent Holdings Limited (騰訊控股有限公司), through Guangxi Tencent Venture Investment Co., Ltd. (廣西騰訊創業投資有限公司), owns 
approximately 6.66% of the total number of issued Shares of the Company before the Global Offering. Such shareholding is expected to be 
approximately 7.06% immediately following the completion of the Global Offering (and before any exercise of the Over-allotment Option), after 
taking into account the Shares to be subscribed by Huang River and Prosper High under the Cornerstone Investment.
(4) 
As disclosed in the Prospectus, each of LAV Innovation Hong Kong Co., Limited, LAV Enterprise Hong Kong Limited, LAV Impetus Limited, 
and LAV Integra Limited (together, “LAV USD”) owns approximately 15.62% of the total number of issued Shares of the Company before the 
Global Offering. Such shareholding is expected to be approximately 13.95% immediately following the completion of the Global Offering (and 
before any exercise of the Over-allotment Option), after taking into account the Shares to be subscribed by LAV Star and LAV Opportunities 
under the Cornerstone Investment.
(5) 
As disclosed in the Prospectus, GSC Fund 1, Vision Fund 1, Horizon Fund 1, and Horizon Next Fund are all sub-funds of Foresight Global 
Superior Choice SPC. Immediately following the completion of the Global Offering (and before any exercise of the Over-allotment Option), 
Foresight owns approximately 0.71% of the total number of issued Shares of the Company.
(6) 
WWHCP owns approximately 0.14% of the total number of issued Shares of the Company before the Global Offering. Such shareholding is 
expected to increase to approximately 0.26% immediately following the completion of the Global Offering (and before any exercise of the Over-
allotment Option), after taking into account the Shares to be subscribed by it under the Cornerstone Investment. Exome Asset Management LLC, 
through WWHCP and Emerging Markets Healthcare Partners LLC, in aggregate owns approximately 0.39% of the total number of issued Shares 
of the Company before the Global Offering, and approximately 0.47% immediately following the completion of the Global Offering (and before 
any exercise of the Over-allotment Option).

<<<PAGE 7>>>
7
Allottees with Waivers/Consents Obtained
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
% of total 
issued share 
capital after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Relationship
Allottees with consent under paragraph 1C(2) of the Placing Guidelines and waiver from strict 
compliance with the requirements under Rule 9.09(b) (where applicable) and Rule 10.04 of the Listing 
Rules pursuant to Chapters 2.3 and 4.15 of the Listing Guide in relation to subscription for Offer 
Shares by existing Shareholder and/or their close associatesNote 1
WWHCP
389,600
0.93%
0.14%
An Existing 
Shareholder
LAV Star
974,200
2.32%
0.35%
A close 
associate of 
an existing 
Shareholder
LAV Opportunities
974,200
2.32%
0.35%
A close 
associate of 
an existing 
Shareholder
Huang River
3,117,800
7.43%
1.13%
A close 
associate of 
an existing 
Shareholder
Prosper High
776,000
1.85%
0.28%
A close 
associate of 
an existing 
Shareholder
CPIC Investment Management HK 
Limited (“CPIC IMHK”) Note 2
272,800
0.65%
0.10%
A close 
associate of 
an existing 
Shareholder
PACIFIC ASSET MANAGEMENT CO., 
LTD. (“Pacific Asset”) Note 2
1,091,200
2.60%
0.40%
A close 
associate of 
an existing 
Shareholder

<<<PAGE 8>>>
8
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
% of total 
issued share 
capital after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Relationship
Wealth Shine Asia Pacific Limited 
(“Wealth Shine”) Note 3
311,800
0.74%
0.11%
A close 
associate of 
an existing 
Shareholder
STAR FOCUS GROUP LIMITED (“Star 
Focus”) Note 4
30,600
0.07%
0.01%
A close 
associate of 
an existing 
Shareholder
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the 
Listing Guide in relation to allocations to connected clients Note 5
CICC Financial Trading Limited (“CICC 
FT”)
5,800
0.0138%
0.0021%
A connected 
client
China Asset Management (Hong Kong) 
Limited (“China AMC”)
4,200
0.0100%
0.0015%
A connected 
client
Notes:
1. 
The Stock Exchange has granted a consent under paragraph 1C(2) of the Placing Guidelines and a waiver 
from strict compliance with the requirements under Rule 9.09(b) (where applicable) and 10.04 of the Listing 
Rules pursuant to Chapters 2.3 and 4.15 of the Listing Guide to permit Offer Shares be placed the above 
placees who are existing Shareholders and/or their close associates. Please refer to the section headed 
“Others/Additional Information – Allocation of H Shares to Certain Existing Shareholders and/or Their Close 
Associates” in this announcement.
2. 
Shanghai Kangjun Business Management Consulting Partnership (Limited Partnership) (上海康鋆企業管理
諮詢合夥企業(有限合夥)(“Shanghai Kangjun”) owns approximately 2.58% of the total number of issued 
Shares of the Company before the Global Offering. Such shareholding is expected to be approximately 2.68% 
immediately following the completion of the Global Offering (and before any exercise of the Over-allotment 
Option), after taking into account the Shares to be subscribed by CPIC IMHK and Pacific Asset under the 
International Offering.
3. 
Gongqingcheng Ruiji Fund III Investment Partnership (Limited Partnership) (共青城瑞吉三期投資合夥企
業(有限合夥)) (“Ruiji Fund III”) owns approximately 1.01% of the total number of issued Shares of the 
Company before the Global Offering. Such shareholding is expected to be approximately 0.97% immediately 
following the completion of the Global Offering (and before any exercise of the Over-allotment Option), after 
taking into account the Shares to be subscribed by Wealth Shine under the International Offering.

<<<PAGE 9>>>
9
4. 
Eagle Mind Investments Limited (“Eagle Mind”) owns approximately 0.98% of the total number of issued 
Shares of the Company before the Global Offering. Such shareholding is expected to be approximately 0.84% 
immediately following the completion of the Global Offering (and before any exercise of the Over-allotment 
Option), after taking into account the Shares to be subscribed by Star Focus under the International Offering.
5. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Listing 
Guide in relation to allocations to a connected client, please refer to the section headed “Others/Additional 
Information – Placing to a connected client with prior consent under paragraph 1C(1) of the Placing 
Guidelines” in this announcement.
LOCK-UP UNDERTAKINGS
Cornerstone Investors
Investor Note 1
Number of H Shares 
held in the Company 
subject to lock-up 
undertakings 
upon Listing
% of shareholding
 in the Company 
subject to lock-up 
undertakings 
upon Listing 
(assuming the
Over-allotment
Option is not
exercised)
Last day subject to 
the lock-up 
undertaking Note 1
BPV and HTCI (in connection with  
Huatai Back-to-back TRS and the Huatai Client TRS)
4,775,600
1.73%
November 12, 2026
Huang River
3,117,800
1.13%
November 12, 2026
Prosper High
776,000
0.28%
November 12, 2026
LAV Star
974,200
0.35%
November 12, 2026
LAV Opportunities
974,200
0.35%
November 12, 2026
GSC Fund 1
565,000
0.20%
November 12, 2026
Vision Fund 1
993,800
0.36%
November 12, 2026
Horizon Fund 1
194,800
0.07%
November 12, 2026
Horizon Next Fund
194,800
0.07%
November 12, 2026
First Quarter Moon OFC – Phecda Fund
974,200
0.35%
November 12, 2026
WWHCP
389,600
0.14%
November 12, 2026
Subtotal
13,930,000
5.03%
Note:
1. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on November 
12, 2026, being six months following the Listing Date. The Cornerstone Investors will cease to be prohibited 
from disposing of or transferring H Shares subscribed for pursuant to the relevant cornerstone investment 
agreements after the indicated date.

<<<PAGE 10>>>
10
Other Existing Shareholders (including the Pre-IPO Investors as defined in the “History, 
Development and Corporate Structure” section of the Prospectus)
Name
Number of H Shares 
held in the
Company subject to 
lock-up undertakings 
upon Listing
% of
shareholding in the 
Company subject to 
lock-up 
undertakings upon 
Listing (assuming the 
Over-allotment Option 
is not exercised)
Last day subject 
to the lock-up 
undertakings Note 1
Sui Xiong Cai (蔡遂雄)
8,422,233
3.05%
May 12, 2027
Ye Edward Tian (田野)
8,422,233
3.05%
May 12, 2027
Bao Jun
2,767,497
1.00%
May 12, 2027
Yu Qingzhen (于慶貞)
39,722
0.01%
May 12, 2027
Decheng IMPACT Limited
23,559,685
8.53%
May 12, 2027
LAV Enterprise Hong Kong Limited 
(“LAV Enterprise”) Note 2
14,220,861
5.15%
May 12, 2027
LAV Innovation (Hong Kong) Co., Limited (“LAV Innovation”) Note 2
8,789,975
3.18%
May 12, 2027
LAV Integra Limited (“LAV Integra”) Note 2
6,846,397
2.48%
May 12, 2027
LAV Impetus Limited  
(“LAV Impetus”) Note 2
6,725,827
2.44%
May 12, 2027
Shanghai Lihan Biotechnology Partnership (Limited Partnership) (上海
禮瀚生物科技合夥企業(有限合夥))
14,640,236
5.30%
May 12, 2027
Suzhou Lirui Equity Investment Center (Limited Partnership) (蘇州禮瑞
股權投資中心(有限合夥))
8,368,406
3.03%
May 12, 2027
Suzhou Likang Equity Investment Centre (Limited Partnership) (蘇州禮
康股權投資中心(有限合夥))
5,139,637
1.86%
May 12, 2027
Shanghai Lihao Biotech, L.P. (上海禮灝生物科技合夥企業(有限合夥))
2,290,116
0.83%
May 12, 2027
Suzhou Lirun Equity Investment Centre (LP) (蘇州禮潤股權投資中心(有
限合夥))
2,125,370
0.77%
May 12, 2027
Guangxi Tencent Venture Investment Co., Ltd. (廣西騰訊創業投資有限
公司) (“Tencent”) Note 2
15,593,533
5.65%
May 12, 2027
BOUNDLESS CREEK, LLC
10,875,618
3.94%
May 12, 2027
Wanquandao Biomedical Technology Partnership (Limited Partnership) 
(杭州萬全島生物醫藥科技合夥企業(有限合夥))
4,274,984
1.55%
May 12, 2027
Hangzhou Qianxishan Biopharmaceutical Technology Partnership 
(Limited Partnership) (杭州千溪山生物醫藥科技合夥企業(有限合夥))
2,986,905
1.08%
May 12, 2027
Wuhan Biolake China Summit Fund Partnership (Limited Partnership) 
(武漢光谷生物城華嶺基金合夥企業(有限合夥))
4,362,991
1.58%
May 12, 2027

<<<PAGE 11>>>
11
Name
Number of H Shares 
held in the
Company subject to 
lock-up undertakings 
upon Listing
% of
shareholding in the 
Company subject to 
lock-up 
undertakings upon 
Listing (assuming the 
Over-allotment Option 
is not exercised)
Last day subject 
to the lock-up 
undertakings Note 1
Shanghai China Summit Zhixin Investment Partnership (Limited 
Partnership) (上海華嶺智新投資合夥企業(有限合夥))
3,558,211
1.29%
May 12, 2027
China Summit Capital Limited Partnership
2,290,117
0.83%
May 12, 2027
Homeric Summit Capital Limited Partnership
2,290,117
0.83%
May 12, 2027
Suzhou Gaotejia Xinyin Huixin Equity Investment Partnership (Limited 
Partnership) (蘇州高特佳信銀匯鑫股權投資合夥企業(有限合夥))
8,615,202
3.12%
May 12, 2027
Shanghai Yunan Enterprise Management Partnership (Limited 
Partnership) (上海譽楠企業管理合夥企業(有限合夥))
4,580,233
1.66%
May 12, 2027
Guangzhou Yuexiu Bioindustry Venture Capital Limited Partnership 
(Limited Partnership) (廣州越秀生物產業創業投資基金合夥企業(有限
合夥))
3,588,778
1.30%
May 12, 2027
Yangzhou Guojin Yingpai Biomedical Venture Capital Partnership 
(Limited Partnership) (揚州國金英派生物醫藥創業投資合夥企業(有限
合夥))
7,944,585
2.88%
May 12, 2027
Shanghai Junshi Biosciences Co., Ltd. (上海君實生物醫藥科技股份有限
公司)
7,907,133
2.86%
May 12, 2027
Beijing New Power Equity Investment Fund (Limited Partnership) (北京
新動力股權投資基金(有限合夥))
6,030,642
2.18%
May 12, 2027
Shanghai Kangjun Business Management Consulting Partnership 
(Limited Partnership)(上海康鋆企業管理諮詢合夥企業(有限合夥))
6,030,649
2.18%
May 12, 2027
Hainan Yuema Zhengchun Venture Investment Center (Limited 
Partnership)  
(海南躍馬爭春創業投資中心(有限合夥))
4,307,601
1.56%
May 12, 2027
Xiamen C&D Emerging Industries Equity Investment No. 7 Partnership 
(Limited Partnership) (廈門建發新興產業股權投資柒號合夥企業(有限
合夥))
4,013,156
1.45%
May 12, 2027
Everspring GQ Investment Fund L.P.
3,664,188
1.33%
May 12, 2027

<<<PAGE 12>>>
12
Name
Number of H Shares 
held in the
Company subject to 
lock-up undertakings 
upon Listing
% of
shareholding in the 
Company subject to 
lock-up 
undertakings upon 
Listing (assuming the 
Over-allotment Option 
is not exercised)
Last day subject 
to the lock-up 
undertakings Note 1
WuXi AppTec Investment Fund I L.P. (無錫藥明康德一期投資企業(有
限合夥))
3,029,306
1.10%
May 12, 2027
Gongqingcheng Ruiji Fund III Investment Partnership (Limited 
Partnership) (共青城瑞吉三期投資合夥企業(有限合夥))
2,372,140
0.86%
May 12, 2027
Dingxin Capital Biotech Ventures Limited
2,290,116
0.83%
May 12, 2027
Eagle Mind Investments Limited
2,290,116
0.83%
May 12, 2027
Suzhou Industrial Park Sungent Bio-Venture Capital Investment 
Enterprise (Limited Partnership) (蘇州工業園區新建元生物創業投資企
業(有限合夥))
2,134,448
0.77%
May 12, 2027
Hangzhou Haibang Medicine Valley Congzheng Venture Capital 
Investment Partnership (Limited Partnership) (杭州海邦藥谷從正創業投
資合夥企業(有限合夥))
2,134,448
0.77%
May 12, 2027
Ausun (Hong Kong) Industrial Co., Limited (奧翔(香港)實業有限公司)
1,581,427
0.57%
May 12, 2027
AlphaTech Projects Limited
1,313,865
0.48%
May 12, 2027
Lakeshore LSV Limited
853,380
0.31%
May 12, 2027
Emerging Markets Healthcare Partners LLC
595,430
0.22%
May 12, 2027
WWHCP Note 2
320,616
0.12%
May 12, 2027
Subtotal
234,188,130
84.80%
Note:
1. 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Laws. The 
required lock-up for existing Shareholders ends on May 12, 2027, being 12 months following the Listing 
Date.
2. 
The numbers of Shares held by LAV Enterprise, LAV Innovation, LAV Integra, LAV Impetus, Tencent, 
and WWHCP in the table above do not take into account the Shares to be subscribed by them and/or their 
respective close associates in the Global Offering. The Company has applied to the Stock Exchange for, and 
the Stock Exchange has granted to the Company, a consent under paragraph 1C (2) of Appendix F1 and a 
waiver from strict compliance with the requirements under Rule 9.09(b) (where applicable) and Rule 10.04 
of the Listing Rules to permit the Company to allocate such Offer Shares in the International Offering to 
themselves and/or their respective close associates. For details, please refer to the sections headed “Allottees 
with Waivers/Consents Obtained” and “Others/Additional Information” in this announcement.

<<<PAGE 13>>>
13
PLACEE CONCENTRATION ANALYSIS
Placees
* Numbers 
of H Shares 
allotted
Allotment as 
% of 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option
Allotment as 
% of 
International 
Offering 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued)
Allotment as 
% of total 
Offer Shares 
(assuming 
no exercise 
of the 
Overallotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming the 
Overallotment 
Option is 
exercised and 
new H Shares 
are issued)
Number of 
H Shares held 
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
Option is 
exercised and 
new H Shares 
are issued)
Top 1
4,775,600
12.64%
10.84%
11.38%
9.89%
4,775,600 
1.73% 
1.69%
Top 5
19,576,400
51.82%
44.42%
46.64%
40.55%
35,169,933
12.74%
12.45%
Top 10
29,298,200
77.55% 
66.47% 
69.80% 
60.69% 
81,474,793
29.50% 
28.84%
Top 25
42,363,400
112.13%
96.12% 
100.92%
87.76%
101,486,688
36.75%
35.93%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders
* Numbers 
of H Shares 
allotted
Allotment as 
% of 
International 
Offering 
(assuming no 
exercise 
of the Over-
allotment 
Option)
Allotment as 
% of 
International 
Offering 
(assuming 
the Over-
allotment 
Option is 
exercised 
and new 
H Shares 
are issued)
Allotment as 
% of 
total Offer 
Shares 
(assuming 
no exercise 
of the 
Overallotment 
Option)
Allotment as 
% of 
total Offer 
Shares 
(assuming the 
Overallotment 
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
(assuming no 
exercise 
of the Over-
allotment 
Option)
% of 
total issued 
H Shares 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is 
exercised 
and new 
H Shares 
are issued)
Number 
of Shares 
held upon 
Listing
Top 1
1,948,400
5.16%
4.42%
4.64%
4.04%
38,531,460
13.95%
13.64%
38,531,460
Top 5
5,842,200
15.46%
13.25%
13.92%
12.10%
132,279,750
47.90%
46.83%
132,279,750
Top 10
5,842,200
15.46%
13.25%
13.92%
12.10%
178,409,865
64.60%
63.16%
178,409,865
Top 25
23,231,200
61.49%
52.71%
55.34%
48.12%
246,155,878
89.13%
87.15%
246,155,878
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 14>>>
14
SHAREHOLDERS CONCENTRATION ANALYSIS
All Shareholders
* Numbers 
of H Shares 
allotted
Allotment as 
% of 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as 
% of 
International 
Offering 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued)
Allotment as 
% of total 
Offer Shares 
(assuming 
no exercise 
of the 
Overallotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming the 
Overallotment 
Option is 
exercised and 
new H Shares 
are issued)
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
Option is 
exercised and 
new H Shares 
are issued)
Top 1
1,948,400
5.16%
4.42%
4.64%
4.04%
38,531,460
13.95%
13.64%
Top 5
5,842,200
15.46%
13.25%
13.92%
12.10%
132,279,750
47.90%
46.83%
Top 10
5,842,200
15.46%
13.25%
13.92%
12.10%
178,409,865
64.60%
63.16%
Top 25
23,231,200
61.49%
52.71%
55.34%
48.12%
246,155,878
89.13%
87.15%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
NO. OF 
SHARES
APPLIED FOR
NO. OF 
VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE 
ALLOTTED
OF THE TOTAL 
NO. OF SHARES 
APPLIED FOR
POOL A
200
67,375
1,010 out of 67,375 to receive 200 Shares
1.50%
400
31,423
487 out of 31,423 to receive 200 Shares
0.77%
600
7,145
114 out of 7,145 to receive 200 Shares
0.53%
800
4,135
68 out of 4,135 to receive 200 Shares
0.41%
1,000
5,633
96 out of 5,633 to receive 200 Shares
0.34%
1,200
2,889
51 out of 2,889 to receive 200 Shares
0.29%
1,400
2,481
45 out of 2,481 to receive 200 Shares
0.26%
1,600
2,331
43 out of 2,331 to receive 200 Shares
0.23%
1,800
2,223
43 out of 2,223 to receive 200 Shares
0.21%
2,000
21,604
422 out of 21,604 to receive 200 Shares
0.20%
3,000
5,244
115 out of 5,244 to receive 200 Shares
0.15%
4,000
6,287
153 out of 6,287 to receive 200 Shares
0.12%
5,000
2,883
77 out of 2,883 to receive 200 Shares
0.11%
6,000
1,867
55 out of 1,867 to receive 200 Shares
0.10%
7,000
1,308
41 out of 1,308 to receive 200 Shares
0.09%

<<<PAGE 15>>>
15
NO. OF 
SHARES
APPLIED FOR
NO. OF 
VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE 
ALLOTTED
OF THE TOTAL 
NO. OF SHARES 
APPLIED FOR
8,000
1,141
39 out of 1,141 to receive 200 Shares
0.09%
9,000
1,085
40 out of 1,085 to receive 200 Shares
0.08%
10,000
7,202
282 out of 7,202 to receive 200 Shares
0.08%
20,000
6,048
380 out of 6,048 to receive 200 Shares
0.06%
30,000
4,890
424 out of 4,890 to receive 200 Shares
0.06%
40,000
4,190
463 out of 4,190 to receive 200 Shares
0.06%
50,000
2,441
328 out of 2,441 to receive 200 Shares
0.05%
60,000
1,914
302 out of 1,914 to receive 200 Shares
0.05%
70,000
1,434
260 out of 1,434 to receive 200 Shares
0.05%
80,000
1,524
313 out of 1,524 to receive 200 Shares
0.05%
90,000
1,259
289 out of 1,259 to receive 200 Shares
0.05%
100,000
8,062
2,041 out of 8,062 to receive 200 Shares
0.05%
200,000
5,128
2,514 out of 5,128 to receive 200 Shares
0.05%
211,146
Total number of Pool A successful applicants: 10,495
POOL B
300,000
5,016
3,182 out of 5,016 to receive 200 Shares
0.04%
400,000
1,603
1,199 out of 1,603 to receive 200 Shares
0.04%
500,000
903
778 out of 903 to receive 200 Shares
0.03%
600,000
503
200 Shares
0.03%
700,000
397
200 Shares plus 33 out of 397 to receive additional  
 200 Shares
0.03%
800,000
250
200 Shares plus 50 out of 250 to receive additional  
 200 Shares
0.03%
900,000
184
200 Shares plus 57 out of 184 to receive additional  
 200 Shares
0.03%
1,000,000
444
200 Shares plus 191 out of 444 to receive additional  
 200 Shares
0.03%
1,250,000
227
200 Shares plus 162 out of 227 to receive additional  
 200 Shares
0.03%
1,500,000
148
400 Shares
0.03%
1,750,000
127
400 Shares plus 35 out of 127 to receive additional 
 200 Shares
0.03%
2,098,800
840
400 Shares plus 572 out of 840 to receive additional 
 200 Shares
0.03%
10,642
Total number of Pool B successful applicants: 8,279
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 16>>>
16
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and Stock Exchange trading fee payable.

<<<PAGE 17>>>
17
OTHERS/ADDITIONAL INFORMATION
Allocation of H Shares to Certain Existing Shareholders and/or Their Close Associates
As Cornerstone Investors
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted to the 
Company, a consent under paragraph 1C (2) of Appendix F1 and a waiver from strict compliance 
with the requirements under Rule 9.09(b) (where applicable) and Rule 10.04 of the Listing Rules 
to permit H Shares in the International Offering to be placed to the Existing Shareholders and their 
Close Associates to participate in the Global Offering as a cornerstone investor on the following 
basis as set out in Paragraph 18 of Chapter 2.3 and Chapter 4.15 of the Guide, subject to the 
conditions as follows:
(a) 
the Company will comply with the public float requirement under Rule 19A.13A of the 
Listing Rules and the free float requirement under Rule 19A.13C of the Listing Rules;
(b) 
no preference in allocation has been, nor will be, given to WWHCP, LAV Star, LAV 
Opportunities, Huang River, and Prosper High or its respective close associate(s) by virtue 
of their relationship with the Company other than the preferential treatment of assured 
entitlement at the Offer Price under a cornerstone investment and the terms of the cornerstone 
investment agreement with WWHCP, LAV Star, LAV Opportunities, Huang River, and 
Prosper High or its respective close associate(s) are substantially the same as the other 
cornerstone investment agreements following the principles set out in Chapters 2.3 and 4.15 
of the Guide;
(c) 
the Shares to be subscribed by and allocated to WWHCP, LAV Star, LAV Opportunities, 
Huang River, and Prosper High under the Global Offering will be at the same Offer Price and 
on substantially the same terms, or no more favorable than, the terms of the other cornerstone 
investors (including being subject to a lock-up period of six months from the Listing Date) 
and WWHCP, LAV Star, LAV Opportunities, Huang River, and Prosper High shall pay and 
settle in full the consideration for the relevant Offer Shares before dealings commence on the 
Listing Date;
(d) 
each of the Company, the Joint Sponsors and the Overall Coordinators has provided the Stock 
Exchange with written confirmations in accordance with Chapters 2.3 and 4.15 of the Guide; 
and
(e) 
the relevant information in respect of the allocation to WWHCP, LAV Star, LAV 
Opportunities, Huang River, and Prosper High as Cornerstone Investors has been disclosed in 
the allotment results announcement.
All allocations of Offer Shares to the Existing Shareholders and/or their close associates are in 
compliance with all the conditions under the waiver and consent granted by the Stock Exchange.
Please refer to the section headed “Waivers and Exemptions – Consent and Waiver in respect of 
Allocation of H Shares to Certain Existing Shareholders and/or Their Close Associates” in the 
Prospectus for further details of the waiver and consent.

<<<PAGE 18>>>
18
As Placees
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted to the 
Company, a consent under paragraph 1C (2) of Appendix F1 and a waiver from strict compliance 
with the requirements under Rule 10.04 of the Listing Rules to permit H Shares in the International 
Offering to be placed to the Existing Shareholders and their Close Associates to participate in the 
Global Offering on the following basis as set out in Paragraph 18 of Chapter 2.3 and Chapter 4.15 
of the Guide, subject to the conditions as follows:
(a) 
since none of the Permitted Participants, together with the involved existing Shareholder, 
is, and will be, a core connected person of the Company, the allocation to the Permitted 
Participants will not affect the Company’s ability to satisfy the public float requirement under 
Rule 19A.13A of the Listing Rules and the free float requirement under Rule 19A.13C of the 
Listing Rules;
(b) 
to the best knowledge and belief of the Company and based on the confirmation required to 
be submitted to the Stock Exchange, the Company will confirm to the Stock Exchange that 
no preferential treatment has been, nor will be, given to any Permitted Participant by virtue 
of its relationship with the Company in any allocation in the International Offering, and that 
such allocation will not prejudice or unfairly treat any public investors in their investment 
decision-making process;
(c) 
the Overall Coordinators will confirm to the Stock Exchange that, to the best of their 
knowledge and belief, no preferential treatment has been, nor will be, given to any 
Permitted Participant by virtue of its relationship with the Company in any allocation in the 
International Offering and that such allocation will not prejudice or unfairly treat any public 
investors in their investment decision-making process;
(d) 
each of the Company, the Joint Sponsors and the Overall Coordinators has provided the Stock 
Exchange with written confirmations in accordance with Chapters 2.3 and 4.15 of the Guide; 
and
(e) 
the relevant information in respect of the allocation to the Permitted Participants has been 
disclosed in the allotment results announcement.
For details of the allocations of Offer Shares to the existing Shareholder and/or their close 
associates, please refer to the section headed “Allotment Results Details – International Offering – 
Allottees with Waivers/Consents Obtained” in this announcement.

<<<PAGE 19>>>
19
Placing to a connected client with prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to a connected client of a 
connected distributor pursuant to the Placing Guidelines. Details of the placement to this connected 
client are set out below.
Connected Client
Connected 
Distributor
Relationship 
with the 
Connected 
Distributor
Whether the 
Connected Client 
will hold the 
beneficial interests 
of the Offer 
Shares on a non-
discretionary basis 
or discretionary 
basis for 
independent third 
parties
Number of 
Offer Shares 
to be allocated
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering
(1)
Approximate 
percentage of 
the total issued 
share capital 
immediately 
following 
completion 
of the Global 
Offering
(1)
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering
(2)
Approximate 
percentage of 
the total issued 
share capital 
immediately 
following 
completion 
of the Global 
Offering
(2)
CICC Financial 
Trading Limited 
(“CICC FT”)
(3)
CICC HK
CICC FT is a 
member of the 
same group of 
companies as 
CICC HK.
Non-discretionary
5,800
0.0138%
0.0021%
0.0120%
0.0021%
China Asset 
Management (Hong 
Kong) Limited 
(“China AMC”)
(4)
CSB
China AMC is a 
member of the 
same group of 
companies as 
CSB.
Discretionary
4,200
0.0100%
0.0015%
0.0087%
0.0015%

<<<PAGE 20>>>
20
Notes:
1. 
Assuming the Over-allotment Option is not exercised.
2. 
Assuming the Over-allotment Option is fully exercised.
3. 
CICC FT, which intends to participate in the International Offering as a placee, and China International 
Capital Corporation Limited will enter into a series of cross border delta-one OTC swap transactions (the 
“OTC Swaps”) with each other and the ultimate clients (the “CICC FT Ultimate Clients”), pursuant to 
which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the OTC Swaps while the 
economic risks and returns of the underlying Offer Shares are passed to the CICC FT Ultimate Clients subject 
to customary fees and commissions. The OTC Swaps will be fully funded by the CICC FT Ultimate Clients. 
During the terms of the OTC Swaps, all economic returns of the Offer Shares subscribed by CICC FT will 
be passed to the CICC FT Ultimate Clients and all economic loss shall be borne by the CICC FT Ultimate 
Clients through the OTC Swaps, and CICC FT will not take part in any economic return or bear any economic 
loss in relation to the Offer Shares. The OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate 
Clients may request CICC FT to redeem it at their own discretion, upon which CICC FT shall dispose of the 
Offer Shares and settle OTC Swaps in cash in accordance with the terms and conditions of the OTC Swap. 
Despite that CICC FT will hold the legal title of the Offer Shares by itself, it will not exercise the voting 
rights attaching to the relevant Offer Shares during the terms of the OTC Swaps according to its internal 
policy. Each of the CICC FT Ultimate Clients for purpose of this placee subscription is an independent third 
party of CICC FT, CICCHKS and the companies which are members of the same group of companies as each 
of the Underwriters.
The details of the CICC FT Ultimate Client are as follows:
Name of CICC FT Ultimate Clients(1)
Fund manager(s)(2)
Ultimate Beneficial 
Owner (“UBO”) of 
Fund Manager
Limited Partner/Shareholding 
holding 30% or more in the CICC FT 
Ultimate Client
Yuanzheng Tianli No.3 Private Securities 
Investment Fund (遠征添利3號私募證券 
投資基金)
Beijing Hengde Era Fund 
Management Co. Ltd. (北京恒德
時代私募基金管理有限公司)
N/A
Not applicable as there is no limited 
partner holding 30% or more
Yuanzheng Jinxin No.4 Private Securities 
Investment Fund(遠征金信 4 號私募證券 
投資基金私募證券投資基金
Beijing Hengde Era Fund 
Management Co. Ltd. (北京恒德
時代私募基金管理有限公司)
N/A
Not applicable as there is no limited 
partner holding 30% or more
Hengde Jinze E49 Private Securities Investment 
Fund (恒德金澤 E49 號私募證券投資基金)
Beijing Hengde Era Fund 
Management Co. Ltd. (北京恒德
時代私募基金管理有限公司)
N/A
Tsinghua University Education 
Foundation3
Longrising Qiangshu Private Securities 
Investment Fund (源樂晟強樹私募證券投資
基金)
Tibet Longrising Capital 
Management Co., Ltd.(西藏源樂
晟資產管理有限公司)
ZENG Xiaojie
ZENG Xiaojie (shareholding interests: 
98.36%)
Longrising Qiangye Private Securities 
Investment Fund (源樂晟強業私募證券投資
基金)
Tibet Longrising Capital 
Management Co., Ltd.(西藏源樂
晟資產管理有限公司)
ZENG Xiaojie
ZENG Xiaojie (shareholding interests: 
42.31%)
To the best knowledge, information and belief of CICC FT after due enquiry, (i) the CICC FT Ultimate 
Clients are independent third parties of CICC FT, CICC HK and the companies which are members of the 
same group of CICC HK; (ii) the ultimate beneficial owners holding 30% or more interest of the CICC FT 
Ultimate Clients as set out below, each of which is an independent third party of the CICC FT, CICC HK and 
the companies which are members of the same group of CICC HK; and (iii) the CICC FT Ultimate Clients 
are independent third parties of the Company, the subsidiaries, and substantial shareholders of the Company.
(1) 
English Names are for identification purpose only.
(2) 
English Names are for identification purpose only.
(3) 
As Tsinghua University Education Foundation (清華大學教育基金會) is a non-profit organization (NGO), it does not have any equity 
holders or ultimate beneficial owners. Its primary funding comes from social donations.

<<<PAGE 21>>>
21
4. 
CSB is a sub-distributor of the Global Offering. China AMC will hold the Offer Shares in its capacity 
as the discretionary fund manager managing assets on behalf of its underlying clients, each of which 
is an independent third party (“China AMC Ultimate Clients”). CSB is a wholly owned subsidiary of 
CITIC Securities Company Limited (a company listed on the Stock Exchange, stock code: 6030 “CITIC 
Securities”), China AMC is controlled as to 62.2% by CITIC Securities. Therefore, China AMC is a member 
of the same group of companies as CSB Connected Distributors.
The details of the China AMC Ultimate Clients are as follow:
Name of China AMC 
Ultimate Clients
Fund manager(s)
UBO of Fund 
Manager
Limited Partner/Shareholding holding 
30% or more in the China AMC 
Ultimate Clients
CHINAAMC SELECT GREATER 
 CHINA TECHNOLOGY FUND
China Asset Management  
(Hong Kong) Limited
CITIC Securities
Futu Securities International (Hong 
Kong) Limited (wholly-owned by Futu 
Holdings Limited, FUTU.O/NASDAQ) 
-client account
CHINAAMC FUND
China Asset Management  
(Hong Kong) Limited
CITIC Securities
Not applicable as there is no limited 
partner holding 30% or more
CHINAAMC CHINA  
 FOCUS FUND
China Asset Management  
(Hong Kong) Limited
CITIC Securities
Manulife (International) Limited (wholly-
owned by Manulife Financial Corp, 
MFC.TO/0045.HK)
CHINAAMC CHINA  
 GROWTH FUND
China Asset Management  
(Hong Kong) Limited
CITIC Securities
Yuanta Securities (HK) Company LTD) 
(wholly-owned by Yuanta Financial 
Holding, 2885.TW)-client account
HKCINDAM
China Asset Management  
(Hong Kong) Limited
CITIC Securities
China Cinda (HK) Asset Management CO., 
LTD (wholly-owned by China Cinda 
Asset Management Co., LTD, 1359.HK)
To the best knowledge of China AMC and after making all reasonable enquiries, China AMC Ultimate Client, 
together with its ultimate beneficial owners, is an independent third party of the Company, its subsidiaries, its 
substantial shareholders, China AMC, CSB, CITIC Securities and the companies which are members of the 
same group of companies as each of the Overall Coordinators and Underwriters, respectively.
5. 
Each of the Connected Clients is not a collective investment scheme which is not authorized by the SFC, nor 
is expected to hold the Offer Shares on behalf of such scheme.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such 
Offer Shares in the International Offering to the connected client listed above. The allocation of 
Offer Shares to such connected client is in compliance with all the conditions under the consent 
granted by the Stock Exchange.

<<<PAGE 22>>>
22
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the 
“Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy 
or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer 
to sell or solicitation to purchase or subscribe for securities in the United States or in any other 
jurisdictions in which such offer or solicitation would be unlawful. The securities mentioned 
herein have not been, and will not be, registered under the United States Securities Act of 1933 
as amended from time to time (the “U.S. Securities Act”) or any state securities law of the 
United States. The securities may not be offered, sold, pledged or transferred within the United 
States ,except in transactions exempt from, or not subject to, the registration requirements of the 
U.S. Securities Act and in compliance with any applicable state securities laws. There will be no 
public offer of the Offer Shares in the United States. 
The Offer Shares are being offered and sold solely (1) to qualified institutional buyers as defined 
in Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under 
the U.S. Securities Act; and (2) outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act and applicable laws of each jurisdiction where those 
offers and sales occur.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated May 5, 2026 issued by IMPACT Therapeutics, Inc (南
京英派藥業股份有限公司) for detailed information about the Global Offering described below 
before deciding whether or not to invest in the H Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the 
occurrence of any of the events set out in the paragraph headed “Underwriting – Underwriting 
Arrangements – Hong Kong Public Offering – Grounds for Termination” in the Prospectus at 
any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected 
to be on May 13, 2026).

<<<PAGE 23>>>
23
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering (before any exercise of the 
Over-Allotment Option), the expected market capitalization of the Company’s H Shares would be 
approximately HK$5,551 million, calculated based on the final Offer Price of HK$20.10. Under 
Rule 19A.13A(1), the minimum public float of the Company shall be 25% based on the final Offer 
Price of HK$20.10. The total number of listed H Shares held by the public (being 157,586,496 H 
Shares) represents approximately 57.06% of the total issued Shares of the Company upon Listing, 
taking into account the actual number of Offer Shares allocated to cornerstone investors that are 
core connected Shareholders. For details of the Shares held by certain of our Shareholders which 
shall not be counted towards the public float, see “History, Development and Corporate Structure 
– Capitalization” in the Prospectus for details. Therefore, the Company will be able to meet the 
minimum public float requirement under Rule 19A.13A.
Immediately following the completion of the Global Offering (before any exercise of the 
Over-allotment Option) and based on the final Offer Price of HK$20.10 per Offer Share, the 
expected market value of the H Shares held by the public and not subject to disposal restrictions 
will be approximately HK$563.7 million, representing approximately 10.16% of the total issued 
Shares of the Company upon Listing. As such, the Company will be able to satisfy the free float 
requirement under Rule 19A.13C(1)(a) of the Listing Rules.
The Directors confirm that immediately following the completion of the Global Offering (before 
any exercise of the Over-allotment Option), (i) no placee will, individually, be placed more than 
10% of the enlarged issued share capital of the Company immediately after the Global Offering; 
(ii) there will not be any new substantial Shareholder immediately after the Global Offering; (iii) 
the three largest public shareholders of the Company do not hold more than 50% of the H Shares 
in public hands at the time of the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing 
Rules; and (iv) there will be at least 300 Shareholders at the time of the Listing in compliance with 
Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, May 
13, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting – Underwriting Arrangements – 
Hong Kong Public Offering – Grounds for Termination” in the Prospectus has not been exercised. 
Investors who trade the H Shares on the basis of publicly available allocation details prior to the 
receipt of H Share certificates or prior to the H Share certificates becoming valid evidence of title 
do so entirely at their own risk.

<<<PAGE 24>>>
24
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Wednesday, 
May 13, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Wednesday, May 13, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 200 H Shares each, and the stock code of the H Shares will 
be 7630.
By order of the Board
IMPACT Therapeutics, Inc
Dr. Sui Xiong CAI
Executive Director and Chief Executive Officer
Hong Kong, May 12, 2026
As at the date of this announcement, the Board comprises (i) Dr. Sui Xiong CAI, Dr. Ye Edward 
TIAN and Ms. Ning MA as executive directors; (ii) Dr. Cong XU, Dr. Qiang XU and Mr. Tao LIU 
as non-executive directors; and (iii) Dr. Edward Ming GUO, Mr. Chi Hung SIU and Dr. Liming 
SHAO as proposed independent non-executive directors.
