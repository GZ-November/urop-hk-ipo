# 配发结果公告抽取任务：3277.HK Gpixel Changchun Microelectronics Inc. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**16/04/2026 22:56**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0416/2026041602158.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3277.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for 
the contents of this announcement, make no representation as to its accuracy or completeness and expressly 
disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated April 9, 2026 (the “Prospectus”) of Gpixel Changchun 
Microelectronics Inc. (長春長光辰芯微電子股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for any securities. This announcement is not a prospectus. Potential investors should 
read the Prospectus for detailed information about the Global Offering described below before deciding 
whether or not to invest in the Offer Shares. Any investment decision in relation to the Offer Shares should be 
taken solely in reliance on the information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not, and is not intended to, constitute or form a part of any offer to sell or 
solicitation to purchase or subscribe for any securities in the United States or in any other jurisdiction. The 
Offer Shares have not been, and will not be, registered under the U.S. Securities Act of 1933, as amended 
from time to time (the “U.S. Securities Act”) or any securities law of any state or other jurisdiction of the 
United States and may not be offered, sold, pledged, or otherwise transferred within the United States, except 
pursuant to an exemption from, or in a transaction not subject to, the registration requirements of the U.S. 
Securities Act and in compliance with any applicable state securities laws. There will be no public offer of 
the Offer Shares in the United States. The Offer Shares are being offered and sold solely outside the United 
States in offshore transactions in reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, CLSA Limited as stabilizing manager (the “Stabilizing Manager”), 
its affiliates or any person acting for it, on behalf of the Underwriters, may effect transactions with a view 
to stabilizing or supporting the market price of the Shares at a level higher than that which might otherwise 
prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing Manager, 
its affiliates or any person acting for it to conduct any such stabilizing action, which, if commenced, will 
be done at the sole and absolute discretion of the Stabilizing Manager, its affiliates or any person acting 
for it and may be discontinued at any time. Any such stabilization activity is required to be brought to an 
end on Thursday, May 14, 2026, being the 30th day after the last date for lodging of applications under the 
Hong Kong Public Offering. Such stabilization action, if taken may be effected in all jurisdictions where it is 
permissible to do so, in each case in compliance with all applicable laws, rules and regulatory requirements, 
including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as 
amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that stabilizing action cannot be taken to support the price of the H 
Shares for longer than the stabilisation period which begins on the Listing Date, and is expected to expire on 
Thursday, May 14, 2026, the 30th day after the last day for the lodging of applications under the Hong Kong 
Public Offering. After this date, no further stabilizing action may be taken, demand for the H Shares, and 
therefore the price of the H Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions 
set out in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong 
Kong and/or not resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint 
Sponsors and the Overall-Coordinators (for themselves and on behalf of the Hong Kong Underwriters) 
in their sole and absolute discretion may, by notice in writing to the Company, terminate the Hong 
Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in 
“Underwriting — Underwriting Arrangements and Expenses — the Hong Kong Public Offering — Grounds 
for Termination” in the Prospectus at any time at or prior to 8:00 a.m. on the Listing Date.

<<<PAGE 2>>>
– 2 –
Gpixel Changchun Microelectronics Inc.
長春長光辰芯微電子股份有限公司
(a joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the 
Global Offering
:
65,294,200 H Shares (subject to the 
Over-allotment Option)
Number of Hong Kong Offer Shares
:
6,529,500 H Shares
Number of International Offer Shares
:
58,764,700 H Shares (subject to the 
Over-allotment Option)
Offer Price
:
HK$39.88 per H Share plus brokerage 
of 1.0%, SFC transaction levy of 
0.0027%, AFRC transaction levy 
of 0.00015% and Hong Kong Stock 
Exchange trading fee of 0.00565% 
(payable in full on application in Hong 
Kong dollars and subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
3277
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,  
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
– 3 –
Gpixel Changchun Microelectronics Inc.
長春長光辰芯微電子股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated April 9, 2026 (the “Prospectus”) 
issued by Gpixel Changchun Microelectronics Inc. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, H Shareholders and prospective investors should be aware that the 
price of the H Shares could move substantially even with a small number of H Shares 
traded and should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company Information
Stock code
3277
Stock short name
GPIXEL
Dealings commencement date
April 17, 2026*
*  see note at the end of the announcement
Price Information
Offer Price
HK$39.88
Offer Shares and Share Capital
Number of Offer Shares (before exercise of Over-
allotment Option)
65,294,200
Final Number of Offer Shares in Hong Kong Public 
Offering
6,529,500
Final Number of Offer Shares in International Offering 
(before exercise of the Over-allotment Option)
58,764,700
Number of issued shares upon Listing (before exercise of 
Over-allotment Option)
435,294,200

<<<PAGE 4>>>
– 4 –
Over-allocation
Number of Offer Shares over-allocated
9,794,100
— International Offering
9,794,100
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases 
in the secondary market at prices that do not exceed the Offer Price or through deferred delivery or a 
combination of these means. In the event the Over-allotment Option is exercised, an announcement will 
be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$2,603.9 million
Less: Estimated listing expenses payable based on 
Offer Price
HK$(100.4) million
Net proceeds
HK$2,503.6 million
Note:	 Gross proceeds refers to the amount to which the Company is entitled to receive assuming the 
Over-allotment Option is not exercised. For details of the use of proceeds, please refer to the 
section headed “Future Plans and Use of Proceeds” of the Prospectus.
The Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment 
Option (if any) for the purposes as set out in the section headed “Future Plans and Use of 
Proceeds” of the Prospectus on a pro rata basis.

<<<PAGE 5>>>
– 5 –
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
Number of valid applications
266,501
Number of successful applications
45,516
Subscription level
1,138.21 times
Claw-back triggered
No
Number of Offer Shares initially available under the Hong 
Kong Public Offering
6,529,500
Final number of Offer Shares under the Hong Kong Public 
Offering
6,529,500
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering
10.00%
Note:	 For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can 
refer to http://www.hkeipo.hk/iporesult to perform a search by name or identification number or 
http://www.hkeipo.hk/iporesult for the full list of allottees.

<<<PAGE 6>>>
– 6 –
INTERNATIONAL OFFERING
Number of placees
172
Subscription Level
22.69 times
Number of Offer Shares initially available under the 
International Offering
58,764,700
Final number of Offer Shares under the International 
Offering (before exercise of the Over-allotment Option)
58,764,700
% of Offer Shares under the International Offering to the 
Global Offering
90.00%
The Directors confirm that, to the best of their knowledge, information and belief, 
save for a waiver from strict compliance with Rule 10.04 of the Listing Rules, consents 
under paragraphs 1C(1) and 1C(2) of Appendix F1 to the Listing Rules (the “Placing 
Guidelines”) and Chapter 4.15 of the Guide for New Listing Applicants (“Listing Guide”) 
granted by the Stock Exchange to permit the Company to, among other things, place 
certain H Shares in the International Offering to close associates of existing Shareholders, 
Cornerstone Investors and/or their close associates, and connected clients, (i) none of 
the Offer Shares subscribed by the placees and the public have been financed directly or 
indirectly by the Company, any of the Directors, chief executive of the Company, controlling 
shareholders, substantial shareholders, existing shareholders of the Company or any of 
its subsidiaries or their respective close associates; and (ii) none of the placees and the 
public who have purchased the Offer Shares are accustomed to taking instructions from the 
Company, any of the Directors, chief executive of the Company, controlling shareholders, 
substantial shareholders, existing shareholders of the Company or any of its subsidiaries 
or their respective close associates in relation to the acquisition, disposal, voting or other 
disposition of Shares registered in his/her/its name or otherwise held by him/her/it.

<<<PAGE 7>>>
– 7 –
The placees in the International Offering include the following:
Cornerstone Investors
Investor Note 1
Number of 
Offer
Shares 
allocated
% of Offer 
Shares Note 2
% of total H 
Shares after 
the Global 
Offering Note 2
% of total 
issued share 
capital after 
the Global 
Offering Note 2
Existing 
shareholders 
or their close 
associates
CPE Peepal Investment Limited 
(“CPE Peepal”) Note 3
2,945,900
4.51%
1.01%
0.68%
No
HHLR Advisors, Ltd. 
(“HHLRA”) Note 3
2,945,900
4.51%
1.01%
0.68%
No
UBS Asset Management 
(Singapore) Ltd. (“UBS AM 
Singapore”) Note 3
2,945,900
4.51%
1.01%
0.68%
No
Arc Avenue Asset Management 
Pte. Ltd. (“Arc Avenue”) Note 3
1,963,900
3.01%
0.67%
0.45%
No
Boyu Capital Management 
(Singapore) Pte. Ltd.  
(“Boyu”) Note 3&4
1,963,900
3.01%
0.67%
0.45%
No
Fullgoal Asset Management (HK) 
Limited (“Fullgoal HK”) Notes 3&5
655,900
1.00%
0.23%
0.15%
No
Fullgoal Fund Management Co., 
Ltd. (“Fullgoal Fund”) Notes 3&5
1,308,000
2.00%
0.45%
0.30%
No
GF International Investment 
Management Limited (“GF Fund 
HK”) Note 3
785,500
1.20%
0.27%
0.18%
No
GF Fund Management Co., Ltd. 
(“GF Fund Management”) Note 3
1,178,300
1.80%
0.40%
0.27%
No
Shanghai Greenwoods Asset 
Management Co., Ltd. (“Shanghai 
Greenwoods”) and Huatai Capital 
Investment Limited (“HTCI”) 
(in connection with Greenwoods 
OTC Swaps) Notes 3&7
1,112,000
1.70%
0.38%
0.26%
No

<<<PAGE 8>>>
– 8 –
Investor Note 1
Number of 
Offer
Shares 
allocated
% of Offer 
Shares Note 2
% of total H 
Shares after 
the Global 
Offering Note 2
% of total 
issued share 
capital after 
the Global 
Offering Note 2
Existing 
shareholders 
or their close 
associates
Greenwoods Asset Management 
Hong Kong Limited (“HK 
Greenwoods”) Note 3
851,900
1.30%
0.29%
0.20%
No
Mirae Asset Securities (HK) 
Limited (“Mirae HK”) Note 3
1,963,900
3.01%
0.67%
0.45%
No
Perseverance Asset Management 
International (Singapore) Pte. 
Ltd. (“Perseverance Asset 
Management”) Note 3
1,963,900
3.01%
0.67%
0.45%
No
Yield Royal Investment Holding 
(Singapore) PTE. LTD. (“Yield 
Royal Investment”) Note 3
1,472,900
2.26%
0.51%
0.34%
No
3W Fund Management Limited 
(“3W Fund”) Note 3
981,900
1.50%
0.34%
0.23%
No
Eastern Bell Capital VIII 
Investment Limited (“Eastern 
Bell Capital VIII”) Note 3
981,900
1.50%
0.34%
0.23%
No
ICBC Wealth Management Co., 
Ltd. (“ICBC Wealth”) Notes 3 & 8
981,900
1.50%
0.34%
0.23%
No
Protium Capital Limited Note 3
981,900
1.50%
0.34%
0.23%
No
SCC Foresight Ventures Ltd. Note 3
314,200
0.48%
0.11%
0.07%
No
Voyage42 Master Fund Note 3
667,700
1.02%
0.23%
0.15%
No
WT Asset Management Limited 
(“WT Asset Management”) Note 3
981,900
1.50%
0.34%
0.23%
No
E Fund Management (Hong Kong) 
Co., Ltd. (“E Fund HK”) Note 3
490,900
0.75%
0.17%
0.11%
No
E Fund Management Co., Ltd.  
(“E Fund Management”) Note 3
98,100
0.15%
0.03%
0.02%
No
China Asset Management Co., 
Ltd. (“China AMC”) Notes 3&6
392,700
0.60%
0.13%
0.09%
No

<<<PAGE 9>>>
– 9 –
Investor Note 1
Number of 
Offer
Shares 
allocated
% of Offer 
Shares Note 2
% of total H 
Shares after 
the Global 
Offering Note 2
% of total 
issued share 
capital after 
the Global 
Offering Note 2
Existing 
shareholders 
or their close 
associates
Cithara Global Multi-Strategy 
SPC — Disruptive Innovation 
Investment Fund SP (“Cithara 
Fund”) Note 3
392,700
0.60%
0.13%
0.09%
No
Panjing Harbourview Investment 
Fund (“Panjing Fund”) Note 3
392,700
0.60%
0.13%
0.09%
No
Value Partners Hong Kong 
Limited Note 3
343,600
0.53%
0.12%
0.08%
No
Value Partners Limited Note 3
49,000
0.08%
0.02%
0.01%
No
China Orient International Asset 
Management Limited — China 
Orient Multi-Strategy Master Fund 
(“China Orient Multi-Strategy 
Master Fund”) Note 3
340,000
0.52%
0.12%
0.08%
No
China Merchants Securities 
Investment Management (Hong 
Kong) Company Limited 
(“CMSIM”) Note 3
196,300
0.30%
0.07%
0.05%
No
Total
32,645,200
50.0%
11.21%
7.50%
Notes:
1.	
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone 
Investors” of the Prospectus.
2.	
Assuming the Over-allotment Option is not exercised.
3.	
Only taking into account the Offer Shares allocated to the relevant investors as cornerstone investors 
under the Global Offering. In addition to the Offer Shares subscribed for as Cornerstone Investors, 
each of such investors and/or their respective close associates was allocated further Offer Shares 
as a placee in the International Offering. Please refer to the section headed “Allotment Results 
Details — International Offering Allotees with Waivers/Consents Obtained” in this announcement 
for details. Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-
up as indicated below. For details, please refer to the section headed “Lock-up Undertakings — 
Cornerstone Investors” in this announcement.

<<<PAGE 10>>>
– 10 –
4.	
Supercluster Universe Limited, the entity entering into a cornerstone investment agreement with 
the Company, the Joint Sponsors and the Overall Coordinators to subscribe for the Offer Shares, 
is a controlled subsidiary of Boyu Capital Opportunities Master Fund. Boyu Capital Opportunities 
Master Fund is an investment fund managed by Boyu.
5.	
Each of Fullgoal HK and Fullgoal Fund has entered into a cornerstone investment agreement 
with the Company, the Joint Sponsors and the Overall Coordinators to subscribe for the Offer 
Shares. Fullgoal HK is a wholly owned subsidiary of Fullgoal Fund, which is owned by Guotai 
Haitong Securities Co., Ltd. (stock code: 2611.HK/601211.SH) (“Guotai Haitong”) as to 27.775%. 
Guotai Junan Securities (Hong Kong) Limited (“GTJAS”), one of the Overall Coordinators and 
Underwriters of the Global Offering, is a subsidiary of Guotai Haitong. Haitong International 
Securities Company Limited (“HTIS”), a non-syndicate sub-broker in connection with the Global 
Offering, is also a subsidiary of Guotai Haitong. As advised by Fullgoal HK and Fullgoal Fund, 
each of Fullgoal HK and Fullgoal Fund is considered as a member of the same group of companies 
as GTJAS and HTIS and therefore is a “connected client” of GTJAS and HTIS for the purpose of 
paragraph 1B of the Placing Guidelines. For the consent under paragraph 1C(1) of the Placing 
Guidelines granted by the Stock Exchange for the subscription of Offer Shares by a connected client 
of GTJAS, please refer to the section headed “Waivers from Strict Compliance with the Listing 
Rules - Consent in respect of the Proposed Subscription of Offer Shares by Connected Clients” of 
the Prospectus. The Company has also applied to the Stock Exchange, and the Stock Exchange has 
granted consent under paragraph 1C(1) of the Placing Guidelines in respect of the subscription of 
Offer Shares by a connected client of HTIS.
6.	
China Asset Management (Hong Kong) Limited (“China AMC (HK)”), a wholly-owned subsidiary 
of China AMC, has entered into a cornerstone investment agreement with the Company, the Joint 
Sponsors, and the Overall Coordinators to subscribe for the Offer Shares. CLSA Limited, one of 
the Overall Coordinators and Underwriters of the Global Offering, is an indirect wholly-owned 
subsidiary of CITIC Securities Company Limited. China AMC (HK) is a member of the same group 
of companies as CLSA Limited and therefore is a “connected client” of CLSA Limited for the 
purpose of paragraph 1B of the Placing Guidelines. For the consent under paragraph 1C(1) of the 
Placing Guidelines granted by the Stock Exchange, please refer to the section headed “Waivers from 
Strict Compliance with the Listing Rules - Consent in respect of the Proposed Subscription of Offer 
Shares by Connected Clients” of the Prospectus.
7.	
HTCI, an indirectly wholly-owned subsidiary of Huatai Securities Co., Ltd. (“Huatai Securities”), 
has entered into a cornerstone investment agreement with the Company, the Joint Sponsors, and the 
Overall Coordinators to subscribe for the Offer Shares in connection with the Greenwoods OTC 
Swaps. Huatai Financial Holdings (Hong Kong) Limited (“HTFH”), a non-syndicate sub-broker 
in connection with the Global Offering, is also a subsidiary of Huatai Securities. HTCI is a member 
of the same group of companies as HTFH, and therefore is a “connected client” of HTFH for 
the purpose of paragraph 1B of the Placing Guidelines. The Company has applied to the Stock 
Exchange, and the Stock Exchange has granted consent under paragraph 1C(1) of the Placing 
Guidelines.
8.	
For the purpose of participation in the International Offering as a cornerstone, ICBC Wealth, has 
engaged GF Securities Asset Management (Guangdong) Co., Ltd. (廣發證券資產管理(廣東)有
限公司) (“GF Securities”), to subscribe for and hold such Offer Shares on a non-discretionary 
basis on behalf of ICBC Wealth. GF Securities is an independent third party of ICBC Wealth. GF 
Securities is also a close associate of two Cornerstone Investors, namely, GF Fund Management 
and GF Fund HK, as they are all subsidiaries of GF Securities Co., Ltd.

<<<PAGE 11>>>
– 11 –
Allotees with Waivers/Consents Obtained
Investor
Number of 
Offer Shares 
allocated
% of Offer 
SharesNote 1
% of total H 
Shares after 
the Global 
OfferingNote 1
% of total 
issued share 
capital after 
the Global 
OfferingNote 1
Relationship
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) 
of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation to subscription for H 
Shares by existing Shareholders and/or their close associates Note 2
HTI FINANCIAL 
SOLUTIONS 
LIMITED (“HTIF”)
98,100
0.15%
0.03%
0.02%
To subscribe for and hold the Offer 
Shares under the International 
Offering on behalf of Zhongke 
Chuangxing Technology Investment 
Co., Ltd. (中科創星科技投資有
限公司), a close associate of an 
existing Shareholder, i.e. Zhongke 
Chuangxing.
HTCI
1,374,700
2.11%
0.47%
0.32%
To subscribe for and hold the Offer 
Shares under the International 
Offering on behalf of Ji’ao Qianheng 
No.3 Private Equity Investment Fund 
(吉翱謙亨三號私募證券投資基
金), whose fund manager is a close 
associate of an existing Shareholder, 
i.e. Jilin Yuanheng.

<<<PAGE 12>>>
– 12 –
Investor
Number of 
Offer Shares 
allocated
% of Offer 
SharesNote 1
% of total H 
Shares after 
the Global 
OfferingNote 1
% of total 
issued share 
capital after 
the Global 
OfferingNote 1
Relationship
Allotees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocation of further H Shares to Cornerstone Investors and/or their close associates Note 3
Fullgoal HK
510,600
0.78%
0.18%
0.12%
A Cornerstone Investor
Fullgoal Fund
864,100
1.32%
0.30%
0.20%
A Cornerstone Investor
China AMC (HK)
274,900
0.42%
0.09%
0.06%
A Cornerstone Investor
CITIC Securities 
International Capital 
Management Limited 
(“CSI”)
115,400
0.18%
0.04%
0.03%
To subscribe and hold the Offer 
Shares for a close associate of 
Perseverance Asset Management, a 
Cornerstone Investor Note 5
Perseverance Asset 
Management
670,100
1.03%
0.23%
0.15%
A Cornerstone Investor
HTCI
371,500
0.57%
0.13%
0.09%
To subscribe and hold the Offer 
Shares for Shanghai Greenwoods, a 
Cornerstone Investor Note 6
HK Greenwoods
414,000
0.63%
0.14%
0.10%
A Cornerstone Investor
3W Fund
196,300
0.30%
0.07%
0.05%
A Cornerstone Investor
Boyu 
785,500
1.20%
0.27%
0.18%
Close associate of a Cornerstone 
Investor Note 7
China Orient 
International Asset 
Management Limited 
— China Orient 
Enhanced Income 
Fund
196,300
0.30%
0.07%
0.05%
Close associate of a Cornerstone 
Investor Note 8
Cithara Fund
98,100
0.15%
0.03%
0.02%
A Cornerstone Investor
HHLRA
2,945,900
4.51%
1.01%
0.68%
A Cornerstone Investor
ICBC Wealth
196,300
0.30%
0.07%
0.05%
A Cornerstone Investor Note 9
Protium Capital 
Limited
196,300
0.30%
0.07%
0.05%
A Cornerstone Investor

<<<PAGE 13>>>
– 13 –
Investor
Number of 
Offer Shares 
allocated
% of Offer 
SharesNote 1
% of total H 
Shares after 
the Global 
OfferingNote 1
% of total 
issued share 
capital after 
the Global 
OfferingNote 1
Relationship
SCC Foresight 
Ventures Ltd.
196,300
0.30%
0.07%
0.05%
A Cornerstone Investor
Voyage42 Master 
Fund
196,400
0.30%
0.07%
0.05%
A Cornerstone Investor
WT Asset 
Management
196,300
0.30%
0.07%
0.05%
A Cornerstone Investor
Richapple Resources 
Limited
442,300
0.68%
0.15%
0.10%
Close associate of a Cornerstone 
Investor Note 10
Arc Avenue
785,500
1.20%
0.27%
0.18%
A Cornerstone Investor
GF Fund HK
1,108,100
1.70%
0.38%
0.25%
A Cornerstone Investor
GF Fund Management
266,600
0.41%
0.09%
0.06%
A Cornerstone Investor
CSI
49,000
0.08%
0.02%
0.01%
To subscribe and hold the Offer 
Shares for a close associate of GF 
Fund HK and GF Fund Management, 
the Cornerstone Investors Note 11
GF Securities 
Asset Management 
(Guangdong) Co., 
Ltd. (廣發證券資產
管理(廣東)有限公司) 
(“GF Securities”)
5,000
0.01%
0.00%
0.00%
Close associate of a Cornerstone 
Investor Note11
Panjing Fund
98,100
0.15%
0.03%
0.02%
A Cornerstone Investor
E Fund Management
68,700
0.11%
0.02%
0.02%
A Cornerstone Investor
E Fund HK
343,700
0.53%
0.12%
0.08%
A Cornerstone Investor
CPE Peepal
2,356,700
3.61%
0.81%
0.54%
A Cornerstone Investor
Eastern Bell Capital 
VIII
392,700
0.60%
0.13%
0.09%
A Cornerstone Investor
Value Partners 
Limited
98,100
0.15%
0.03%
0.02%
A Cornerstone Investor
UBS AM Singapore
1,472,900
2.26%
0.51%
0.34%
A Cornerstone Investor

<<<PAGE 14>>>
– 14 –
Investor
Number of 
Offer Shares 
allocated
% of Offer 
SharesNote 1
% of total H 
Shares after 
the Global 
OfferingNote 1
% of total 
issued share 
capital after 
the Global 
OfferingNote 1
Relationship
Mirae HK
785,500
1.20%
0.27%
0.18%
A Cornerstone Investor
Bosera Asset 
Management 
(International) Co., 
Limited (“Bosera 
AM”)
196,300
0.30%
0.07%
0.05%
Close associate of a Cornerstone 
Investor Note 12
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients Note 4
Part A — Connected Clients holding securities on a Discretionary Basis on behalf of Independent Third Parties
China AMC
274,900
0.42%
0.09%
0.06%
A connected client of CLSA Limited 
(“CLSA”)
CITIC Securities 
Asset Management 
Company Limited 
(“CITIC Asset 
Management”)
1,000
0.00%
0.00%
0.00%
A connected client of CLSA
CITIC Securities 
Asset Management 
(HK) Limited 
(“CITIC Asset 
Management HK”)
1,000
0.00%
0.00%
0.00%
A connected client of CLSA
Fullgoal HK
1,166,500 
Note 13
1.78% 
Note 13
0.41%  
Note 13
0.27%  
Note 13
Guotai Junan Securities (Hong 
Kong) Limited (“GTJAS”) and 
Haitong International Securities 
Company Limited (“HTIS”)
Fullgoal Fund
2,172,100 
Note 13
3.32% 
Note 13
0.75% 
Note 13
0.50% 
Note 13
A connected client of GTJAS and 
HTIS

<<<PAGE 15>>>
– 15 –
Investor
Number of 
Offer Shares 
allocated
% of Offer 
SharesNote 1
% of total H 
Shares after 
the Global 
OfferingNote 1
% of total 
issued share 
capital after 
the Global 
OfferingNote 1
Relationship
China Southern Asset 
Management Co., Ltd. 
(“China Southern”)
294,500
0.45%
0.10%
0.07%
A connected client of HTFH
Bosera AM
196,300
0.30%
0.07%
0.05%
A connected client of CMB 
International Securities Limited 
(“CMBI”)
Part B — Connected Clients holding securities on a Non-Discretionary Basis on behalf of Independent Third Parties
CSI
566,800
0.87%
0.19%
0.13%
A connected client of CLSA
HTIF
1,215,100
1.86%
0.42%
0.28%
A connected client of GTJAS and 
HTIS
HTCI
2,858,200 
Note 14
4.38% 
Note 14
0.98% 
Note 14
0.66% 
Note 14
A connected client of HTFH
Notes:
1.	
Assuming the Over-allotment Option is not exercised.
2.	
The Stock Exchange has granted a waiver from strict compliance with the requirements under Rule 
10.04 of the Listing Rules and consent under paragraph 1C(2) of the Placing Guidelines to permit 
Offer Shares be placed the above placees who are close associates of certain existing Shareholders. 
Please refer to the section headed “Others/Additional Information — Placing to close associates of 
existing Shareholders with a waiver from the strict compliance with Rule 10.04 of the Listing Rules 
and a prior consent under paragraph 1C(2) of the Placing Guidelines” in this announcement.
3.	
The number of Offer Shares allocated to the relevant investors listed in this subsection only 
represents the number of Offer Shares allocated to the investors as placees in the International 
Offering. For allocations of Offer Shares to the relevant investors as Cornerstone Investors, please 
refer to the section headed “Allotment Results Details — International Offering — Cornerstone 
Investors” in this announcement. For details of the consent under Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations of further Shares to Cornerstone investors and/or their 
close associates, please refer to the section headed “Others/Additional Information — Allocations 
of Offer Shares to Cornerstone Investors and/or their close associates with consent under Chapter 
4.15 of the Guide for New Listing Applicants” in this announcement.

<<<PAGE 16>>>
– 16 –
4.	
For details of the consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations 
to connected clients, please refer to the section headed “Others/Additional Information — Placing 
to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines” in this 
announcement.
5.	
CSI proposes to subscribe for and hold the Offer Shares as a placee under the International 
Offering on behalf of certain ultimate clients, including certain funds where Shanghai Gaoyi 
Asset Management Partnership (Limited Partnership) (上海高毅資產管理合夥企業(有限合夥)) 
(“Shanghai Gaoyi”) acts as the fund manager for such funds. Shanghai Gaoyi is a close associate 
of a Cornerstone Investor, namely, Perseverance Asset Management.
6.	
HTCI proposes to subscribe for and hold the Offer Shares as a placee under the International 
Offering on behalf of certain ultimate clients, including certain funds where Shanghai Greenwoods 
acts as the fund manager for such funds. Shanghai Greenwoods also in its capacity is the fund 
manager of certain investment funds as a Cornerstone Investor through the TRS mechanism.
7.	
Boyu acts as a fund manager of Boyu Capital Opportunities Master Fund, which is a controlling 
entity of Supercluster Universe Limited, a Cornerstone Investor. Boyu is a close associate of 
Supercluster Universe Limited.
8.	
China Orient International Asset Management Limited as the fund manager of the Cornerstone 
Investor, namely China Orient Multi-Strategy Master Fund, acts as the fund manager of the placee.
9.	
For the purpose of participation in the International Offering as a placee, ICBC Wealth, a 
Cornerstone Investor, has engaged various asset managers that are qualified domestic international 
investors as approved by the relevant PRC authority, to subscribe for and hold such Offer Shares on 
a non-discretionary basis on behalf of ICBC Wealth. Each of such asset managers is an independent 
third party of ICBC Wealth.
Among these asset managers which are qualified domestic international investors subscribing for 
Offer Shares for ICBC Wealth, GF Securities is a close associate of two Cornerstone Investors, 
namely, GF Fund Management and GF Fund HK, as they are all subsidiaries of GF Securities 
Co., Ltd. The Company has applied to the Stock Exchange, and the Stock Exchange has granted 
consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocation of further H Shares to Cornerstone Investors and/or their close associates.
10.	
Richapple Resources Limited is wholly owned by Chang Hongna (常紅娜). Yield Royal Investment, 
a Cornerstone Investor, is wholly owned by Gallantlion Resources PTE. LTD., which is also in turn 
wholly owned by Chang Hongna (常紅娜).
11.	
CSI proposes to subscribe for and hold the Offer Shares as a placee under the International Offering 
on behalf of certain ultimate clients, including a fund where GF Securities acts as the fund manager 
for such funds. Further, GF Securities, in an agency capacity, subscribed for Offer Shares on behalf 
of Shenwan Hongyuan Securities Co., Ltd., an independent third party. GF Securities is a close 
associate of Cornerstone Investors, namely, GF Fund HK and GF Fund Management (the “GF 
Cornerstone Investors”), as GF Securities and the GF Cornerstone Investors are all subsidiaries of 
GF Securities Co., Ltd.

<<<PAGE 17>>>
– 17 –
12.	
CMSIM is a wholly-owned subsidiary of China Merchants Securities International Company Limited 
(“CMSI”). CMSI is a wholly-owned subsidiary of China Merchants Securities Co., Ltd.(“CMS”). 
Bosera AM is owned by Bosera Asset Management Co., Limited (“Bosera”) and China Merchants 
Fund Management Co., Ltd. (“China Merchants Fund”) as to 55% and 45%, respectively. CMS 
is a controlling shareholder of Bosera holding 49% equity interests. CMS is also a controlling 
shareholder of China Merchants Fund holding 45% equity interests. Bosera AM is considered as a 
close associate of CMSIM.
13.	
Including all Offer Shares allocated to Fullgoal HK and Fullgoal Fund, being the connected clients 
of CTJAS and HTIS, as placees and cornerstone investors.
14.	
Including all Offer Shares allocated to HTCI, being the connected client of HTFH, as a placee and 
a cornerstone investor.

<<<PAGE 18>>>
– 18 –
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
Unlisted 
Shares held in 
the Company 
subject to 
lock-up 
undertakings
upon Listing
Number of H 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding 
in the 
Company 
subject to 
lock-up upon 
Listing Note 1
Last day subject 
to the lock-up 
undertakings Note 2
WANG Xinyang (“Dr. Wang”) Note 3
35,425,950
65,791,050
23.25%
April 16, 2029
ZHANG Yanxia (“Dr. Zhang”) Notes 3&4
2,467,500
4,582,500
1.62%
April 16, 2029
Zhuhai Yunchen Qixin Investment 
Partnership (Limited Partnership) 
(“Zhuhai Yunchen”) Note 5
18,480,000
34,320,000
12.13%
April 16, 2027
Zhuhai Xuchen Qixin Investment 
Partnership (Limited Partnership) 
(“Zhuhai Xuchen”) Note 6
7,770,000
14,430,000
5.10%
April 16, 2027
Total
64,143,450
119,123,550
42.10%
Notes:
1.	
Assuming the Over-allotment Option is not exercised.
2.	
Unless otherwise stated, the expiry date of the lock-up period shown in the table above is pursuant 
to the PRC Company Law. The required lock-up for the Controlling Shareholders ends on April 16, 
2027, being one year following the Listing Date.
3.	
The expiry date of the lock-up period for Dr. Wang and Dr. Zhang is pursuant to a separate 
undertaking from the same to have their Shares locked up for a period of 36 months following the 
Listing Date. The required lock-up for Dr. Wang and Dr. Zhang ends on April 16, 2029.
4.	
Dr. Zhang is the spouse of Dr. Wang.
5.	
As of the Latest Practicable Date, Zhuhai Yunchen was held as to (i) approximately 0.01% by 
Hangzhou Qixin Management Consulting Co., Ltd., as its general partner, an entity solely owned 
and controlled by Dr. Wang, (ii) approximately 62.22% by Dr. Wang as its limited partner, and 
(iii) approximately 37.77% by the remaining limited partners, each of them holding less than 30% 
interest in Zhuhai Yunchen.
6.	
As of the Latest Practicable Date, Zhuhai Xuchen was held as to (i) 0.0045% by Hangzhou Qixin 
Management Consulting Co., Ltd., as its general partner, an entity solely owned and controlled 
by Dr. Wang, (ii) 95.94% by Dr. Wang as its limited partner, and (iii) 4.05% by a remaining single 
limited partner.

<<<PAGE 19>>>
– 19 –
Cornerstone Investor
Name
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up 
undertakings
upon Listing
% of
total issued
H Shares in
the Company
subject to
lock-up
undertakings
upon Listing 
Note 1
% of 
shareholding 
in the 
Company 
subject to 
lock-up upon 
Listing Note 1
Last day subject 
to the lock-up 
undertakings Note 2
CPE Peepal
2,945,900
1.01%
0.68%
October 16, 2026
HHLRA
2,945,900
1.01%
0.68%
October 16, 2026
UBS AM Singapore
2,945,900
1.01%
0.68%
October 16, 2026
Arc Avenue
1,963,900
0.67%
0.45%
October 16, 2026
Boyu
1,963,900
0.67%
0.45%
October 16, 2026
Fullgoal HK
655,900
0.23%
0.15%
October 16, 2026
Fullgoal Fund
1,308,000
0.45%
0.30%
October 16, 2026
GF Fund HK
785,500
0.27%
0.18%
October 16, 2026
GF Fund Management
1,178,300
0.40%
0.27%
October 16, 2026
Shanghai Greenwoods and HTCI (in 
connection with Greenwoods OTC 
Swaps)
1,112,000
0.38%
0.26%
October 16, 2026
HK Greenwoods
851,900
0.29%
0.20%
October 16, 2026
Mirae HK
1,963,900
0.67%
0.45%
October 16, 2026
Perseverance Asset Management
1,963,900
0.67%
0.45%
October 16, 2026
Yield Royal Investment
1,472,900
0.51%
0.34%
October 16, 2026
3W Fund
981,900
0.34%
0.23%
October 16, 2026
Eastern Bell Capital VIII
981,900
0.34%
0.23%
October 16, 2026
ICBC Wealth
981,900
0.34%
0.23%
October 16, 2026
Protium Capital Limited
981,900
0.34%
0.23%
October 16, 2026
SCC Foresight Ventures Ltd.
314,200
0.11%
0.07%
October 16, 2026

<<<PAGE 20>>>
– 20 –
Name
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up 
undertakings
upon Listing
% of
total issued
H Shares in
the Company
subject to
lock-up
undertakings
upon Listing 
Note 1
% of 
shareholding 
in the 
Company 
subject to 
lock-up upon 
Listing Note 1
Last day subject 
to the lock-up 
undertakings Note 2
Voyage42 Master Fund
667,700
0.23%
0.15%
October 16, 2026
WT Asset Management
981,900
0.34%
0.23%
October 16, 2026
E Fund HK
490,900
0.17%
0.11%
October 16, 2026
E Fund Management
98,100
0.03%
0.02%
October 16, 2026
China AMC
392,700
0.13%
0.09%
October 16, 2026
Cithara Fund
392,700
0.13%
0.09%
October 16, 2026
Panjing Fund
392,700
0.13%
0.09%
October 16, 2026
Value Partners Hong Kong Limited
343,600
0.12%
0.08%
October 16, 2026
Value Partners Limited
49,000
0.02%
0.01%
October 16, 2026
China Orient Multi-Strategy Master 
Fund
340,000
0.12%
0.08%
October 16, 2026
CMSIM
196,300
0.07%
0.05%
October 16, 2026
Total
32,645,200
11.21%
7.50%
Notes:
1.	
Assuming the Over-allotment Option is not exercised.
2.	
In accordance with each of the respective Cornerstone Investment Agreements, the required lock-up 
period of six months from the Listing Date ends on October 16, 2026. The Cornerstone Investors 
will cease to be prohibited from disposing of or transferring H Shares after the indicated date. For 
further details, please see “Cornerstone Investors — Restrictions on the Cornerstone Investors” in 
the Prospectus.

<<<PAGE 21>>>
– 21 –
Other Existing Shareholders (including the Pre-IPO Investors in the “History, 
Development and Corporate Structure” section of the Prospectus)
Name
Number of 
Unlisted 
Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding 
in the 
Company 
subject to 
lock-up upon 
Listing Note 1
Last day subject 
to the lock-up 
undertakings Note 2
Changchun UP Optotech Co., Ltd.
33,099,850
61,471,150
21.73%
April 16, 2027
LUSTER LightTech Co., Ltd.
13,240,150
24,588,850
8.69%
April 16, 2027
MA Cheng
3,405,500
6,324,500
2.24%
April 16, 2027
LIU Yang
786,625
1,460,875
0.52%
April 16, 2027
LI Yang
786,625
1,460,875
0.52%
April 16, 2027
Zhuhai Qixin Investment Center, L.P
5,550,000
0
1.27%
April 16, 2027
Beijing Gaoling Yurun Equity 
Investment Fund, L.P.
5,550,000
0
1.27%
April 16, 2027
Xianjin Zhizao Industry Investment 
Fund II (Limited Partnership)
1,554,000
2,886,000
1.02%
April 16, 2027
Shanghai Guoce Xiangchi Venture 
Capital Partnership (Limited 
Partnership)
4,070,000
0
0.94%
April 16, 2027
Xiamen Yuanfeng Xinguang Enterprise 
Management Partnership (Limited 
Partnership)
2,590,000
1,110,000
0.85%
April 16, 2027
Huashun (Guangzhou) Enterprise 
Management Partnership (Limited 
Partnership)
3,700,000
0
0.85%
April 16, 2027
Shenzhen Jiusi Investment Management 
Co., Ltd.
0
2,220,000
0.51%
April 16, 2027
QIN Hao
0
1,480,000
0.34%
April 16, 2027

<<<PAGE 22>>>
– 22 –
Name
Number of 
Unlisted 
Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding 
in the 
Company 
subject to 
lock-up upon 
Listing Note 1
Last day subject 
to the lock-up 
undertakings Note 2
Juyuan Xincheng (Jiaxing) Venture 
Capital Partnership (Limited 
Partnership)
1,850,000
0
0.43%
April 16, 2027
Wuhu Tuochen Private Equity 
Investment Center (Limited 
Partnership)
1,480,000
0
0.34%
April 16, 2027
Suzhou Fangguang Phase III 
Venture Capital Partnership (Limited 
Partnership)
463,029
859,911
0.30%
April 16, 2027
Changzhou Fangguang Phase III 
Equity Investment Partnership (Limited 
Partnership)
184,471
342,589
0.12%
April 16, 2027
Yibin Chendao New Energy Industry 
Equity Investment Partnership (Limited 
Partnership)
0
999,000
0.23%
April 16, 2027
Jiangsu Shengyu Huatian Venture 
Capital Partnership (Limited 
Partnership)
740,000
0
0.17%
April 16, 2027
Beijing Phase II Zhongke Chuangxing 
Hard Technology Venture Capital 
Partnership (Limited Partnership)
740,000
0
0.17%
April 16, 2027
Pingyang Yuanxin No. 6 Venture 
Capital Partnership (Limited 
Partnership)
0
370,000
0.09%
April 16, 2027
Jilin Zhongke Xiandao Investment 
Partnership (Limited Partnership)
0
370,000
0.09%
April 16, 2027
Jilin Zhongke Technology Achievement 
Transfer Venture Capital Partnership 
Enterprise (Limited Partnership)
0
185,000
0.04%
April 16, 2027

<<<PAGE 23>>>
– 23 –
Name
Number of 
Unlisted 
Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding 
in the 
Company 
subject to 
lock-up upon 
Listing Note 1
Last day subject 
to the lock-up 
undertakings Note 2
Wuhan Donghu Guolong Shibei No. 
2 Equity Investment Fund Partnership 
(Limited Partnership)
0
370,000
0.09%
April 16, 2027
Ningbo Yuxi Venture Capital 
Partnership (Limited Partnership)
222,000
0
0.05%
April 16, 2027
Ningbo Meishan Bonded Port Area 
Thriving Venture Capital Partnership 
(Limited Partnership)
0
111,000
0.03%
April 16, 2027
Jilin Yuanheng Equity Investment 
Partnership (Limited Partnership)
0
111,000
0.03%
April 16, 2027
Total
80,012,250
106,720,750
42.90%
Notes:
1.	
Assuming the Over-allotment Option is not exercised.
2.	
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company 
Law. The required lock-up ends on April 16, 2027, being one year following the Listing Date.

<<<PAGE 24>>>
– 24 –
PLACEE CONCENTRATION ANALYSIS
Placees
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming 
no exercise 
of the Over-
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
exercised 
and new H 
Shares are 
issued)
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
(assuming 
the Over-
allotment 
Option is 
exercised 
and new H 
Shares are 
issued)
Number of 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing 
(assuming 
no exercise 
of the Over-
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
exercised 
and new H 
Shares are 
issued)
Top 1
5,891,800
10.03%
8.59%
9.02%
7.85%
5,891,800
1.35%
1.32%
Top 5
22,339,300
38.01%
32.58%
34.21%
29.75%
22,339,300
5.13%
5.02%
Top 10
36,086,300
61.41%
52.64%
55.27%
48.06%
36,086,300
8.29%
8.11%
Top 25
55,186,500
93.91%
80.50%
84.52%
73.50%
55,186,500
12.68%
12.40%
Notes
*  Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders
*
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
(assuming 
the Over-
allotment 
Option is 
exercised and 
new H Shares 
are issued)
Number of H 
Shares held 
upon Listing
% of total 
issued H 
Shares capital 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total 
issued H 
Shares capital 
upon Listing 
(assuming 
the Over-
allotment 
Option is 
exercised and 
new H Shares 
are issued)
Number of 
Shares held 
upon Listing
Top 1
0
0.00%
0.00%
0.00%
0.00%
119,123,550
40.92%
39.58%
183,267,000
Top 5
5,891,800
10.03%
8.59%
9.02%
7.85%
217,399,850
74.67%
72.24%
331,288,800
Top 10
22,339,300
38.01%
32.58%
34.21%
29.75%
236,733,350
81.31%
78.67%
352,176,300
Top 25
45,022,400
76.61%
65.67%
68.95%
59.96%
266,038,200
91.38%
88.40%
383,054,400
Notes
*  Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 25>>>
– 25 –
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
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
Option is 
exercised and 
new H Shares 
are issued)
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
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is 
exercised and 
new H Shares 
are issued)
Top 1
0
0.00%
0.00%
0.00%
0.00%
119,123,550
183,267,000
42.10%
41.18%
Top 5
5,891,800
10.03%
8.59%
9.02%
7.85%
217,399,850
331,288,800
76.11%
74.43%
Top 10
15,613,200
26.57%
22.77%
23.91%
20.79%
230,007,250
356,550,200
81.91%
80.11%
Top 25
39,523,600
67.26%
57.65%
60.53%
52.64%
258,647,300
398,973,500
91.66%
89.64%
Notes
*	
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder 
upon Listing.

<<<PAGE 26>>>
– 26 –
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, 266,501 valid 
applications made by the public will be conditionally allocated on the basis set out below:
Pool A: 
NUMBER OF 
H SHARES 
APPLIED
FOR
NUMBER 
OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NUMBER OF 
H SHARES 
APPLIED FOR
100
95,625
957 out of 95,625 applicants to receive 100 H Shares
1.00%
200
23,363
370 out of 23,363 applicants to receive 100 H Shares
0.79%
300
8,064
167 out of 8,064 applicants to receive 100 H Shares
0.69%
400
4,992
125 out of 4,992 applicants to receive 100 H Shares
0.63%
500
6,880
200 out of 6,880 applicants to receive 100 H Shares
0.58%
600
2,880
95 out of 2,880 applicants to receive 100 H Shares
0.55%
700
2,424
88 out of 2,424 applicants to receive 100 H Shares
0.52%
800
2,113
84 out of 2,113 applicants to receive 100 H Shares
0.50%
900
1,380
59 out of 1,380 applicants to receive 100 H Shares
0.48%
1,000
19,951
914 out of 19,951 applicants to receive 100 H Shares
0.46%
1,500
5,280
317 out of 5,280 applicants to receive 100 H Shares
0.40%
2,000
8,778
636 out of 8,778 applicants to receive 100 H Shares
0.36%
2,500
3,905
328 out of 3,905 applicants to receive 100 H Shares
0.34%
3,000
3,217
305 out of 3,217 applicants to receive 100 H Shares
0.32%
3,500
2,189
230 out of 2,189 applicants to receive 100 H Shares
0.30%
4,000
2,283
262 out of 2,283 applicants to receive 100 H Shares
0.29%
4,500
1,830
227 out of 1,830 applicants to receive 100 H Shares
0.28%
5,000
4,279
568 out of 4,279 applicants to receive 100 H Shares
0.27%
6,000
2,611
391 out of 2,611 applicants to receive 100 H Shares
0.25%
7,000
2,153
357 out of 2,153 applicants to receive 100 H Shares
0.24%

<<<PAGE 27>>>
– 27 –
NUMBER OF 
H SHARES 
APPLIED
FOR
NUMBER 
OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NUMBER OF 
H SHARES 
APPLIED FOR
8,000
2,121
384 out of 2,121 applicants to receive 100 H Shares
0.23%
9,000
1,715
336 out of 1,715 applicants to receive 100 H Shares
0.22%
10,000
10,177
2,134 out of 10,177 applicants to receive 100 H Shares
0.21%
20,000
6,848
2,270 out of 6,848 applicants to receive 100 H Shares
0.17%
30,000
4,650
2,015 out of 4,650 applicants to receive 100 H Shares
0.14%
40,000
3,547
1,859 out of 3,547 applicants to receive 100 H Shares
0.13%
50,000
3,537
2,148 out of 3,537 applicants to receive 100 H Shares
0.12%
60,000
2,375
1,627 out of 2,375 applicants to receive 100 H Shares
0.11%
70,000
1,943
1,474 out of 1,943 applicants to receive 100 H Shares
0.11%
80,000
1,711
1,418 out of 1,711 applicants to receive 100 H Shares
0.10%
90,000
1,211
1,085 out of 1,211 applicants to receive 100 H Shares
0.10%
100,000
9,601
9,218 out of 9,601 applicants to receive 100 H Shares
0.10%
Total 
253,633 
Total number of Pool A successful applicants: 32,648

<<<PAGE 28>>>
– 28 –
Pool B
NO. OF SHARES 
APPLIED
FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
200,000
7,763
200 H Shares
0.10%
300,000
1,606
200 H Shares plus 739 out of 1,606 applicants to receive 
an additional 100 H Shares
0.08%
400,000
1,030
200 H Shares plus 771 out of 1,030 applicants to receive 
an additional 100 H Shares
0.07%
500,000
646
200 H Shares plus 535 out of 646 applicants to receive an 
additional 100 H Shares
0.06%
600,000
392
300 H Shares
0.05%
700,000
234
300 H Shares plus 85 out of 234 applicants to receive an 
additional 100 H Shares
0.05%
800,000
183
300 H Shares plus 81 out of 183 applicants to receive an 
additional 100 H Shares
0.04%
900,000
130
300 H Shares plus 114 out of 130 applicants to receive an 
additional 100 H Shares
0.04%
1,000,000
462
400 H Shares plus 185 out of 462 applicants to receive an 
additional 100 H Shares
0.04%
2,000,000
177
600 H Shares
0.03%
3,264,700
245
900 H Shares plus 115 out of 245 applicants to receive an 
additional 100 H Shares
0.03%
Total 
12,868 
Total number of Pool B successful applicants: 12,868
As of the date of this announcement, the relevant subscription monies previously deposited 
in the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers for any inquiries.

<<<PAGE 29>>>
– 29 –
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in 
respect of which consent has been obtained, the Company has complied with the Listing 
Rules and guidance materials in relation to the placing, allotment and listing of the H Shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or 
indirectly, provided by the Company, its controlling shareholder(s), directors or syndicate 
members to any placees or the public (as the case may be) and the consideration payable 
by them directly or indirectly for each Offer Share subscribed for or purchased by them 
is the same as the Offer Price in addition to any brokerage, AFRC transaction levy, SFC 
transaction levy and trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Placing to close associates of existing Shareholders with a waiver from the strict 
compliance with Rule 10.04 of the Listing Rules and a prior consent under paragraph 
1C(2) of the Placing Guidelines
The Company has applied to the Stock Exchange, and the Stock Exchange has granted, the 
waivers from the strict compliance with Rule 10.04 of the Listing Rules and consents under 
paragraph 1C(2) of the Placing Guidelines to permit the Company to allocate such Offer 
Shares in the International Offering to close associates (the “Placees”) of Existing Minority 
Shareholders (as defined below) on the following grounds which are consistent with the 
conditions as set out in the Chapter 4.15 of the Guide for New Listing Applicant:
(a)	
The Joint Sponsors confirm that:
(i)	
each of Beijing Phase II Zhongke Chuangxing Hard Technology Venture Capital 
Partnership (Limited Partnership) (北京二期中科創星硬科技創業投資合夥
企業(有限合夥)), and Jilin Yuanheng Equity Investment Partnership (Limited 
Partnership) (吉林省元亨股權投資合夥企業(有限合夥)) (the “Existing 
Minority Shareholders”) is interested in less than 5% of the Company’s voting 
rights before the Listing;
(ii)	 none of the Existing Minority Shareholders or their close associates is a core 
connected person of the Company or its close associate;
(iii)	 none of the Existing Minority Shareholders or their close associates has the 
power to appoint any Directors to the Board or any other special rights upon the 
Listing;

<<<PAGE 30>>>
– 30 –
(iv)	 as none of the Existing Minority Shareholders or their close associates is a core 
connected person of the Company or its close associate, allocation to the Placees 
will not affect the Company’s ability to satisfy the public float requirement under 
Rule 8.08(1)(as amended and replaced by 19A.13A(1) for PRC issuers with no 
other listed shares) of the Listing Rules; and
(v)	 to the best of their knowledge and belief, no preferential treatment has been, nor 
will be, given to the Existing Minority Shareholders or their close associates by 
virtue of their relationship with the Company in any allocation in the placing 
tranche;
(b)	 the Company confirms that no preferential treatment has been, nor will be, given to the 
Existing Minority Shareholders or their close associates by virtue of their relationship 
with the Company in any allocation of the placing tranche;
(c)	
the Overall Coordinators confirm that, to the best of their knowledge and belief, 
no preferential treatment has been, nor will be, given to the Existing Minority 
Shareholders or their close associates by virtue of their relationship with the Company 
in any allocation in the placing tranche; and
(d)	 details of the allocation of H Shares to the Existing Minority Shareholders and their 
close associates will be disclosed in this allotment results announcement
The allocation of Offer Shares to such existing Shareholders and/or close associates of 
existing Shareholders is in compliance with all the conditions under the waivers/consents 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to existing Shareholders, please refer to the 
section headed “Allotment Results Details — International Offering — Allottees with 
Waivers/Consents Obtained” in this announcement.
Allocations of Offer Shares to Cornerstone Investors and/or their close associates with 
consent under Chapter 4.15 of the Guide for New Listing Applicants

<<<PAGE 31>>>
– 31 –
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 
4.15 of the Guide for New Listing Applicants to permit the Company to allocate further 
Offer Shares in the International Offering to Cornerstone Investors and/or their close 
associates as placees, subject to the following conditions:
(a)	
the final offering size of the Global Offering (excluding any additional Shares which 
may be issued upon exercise of the Over-allotment Option) will be of a total value of 
at least HK$1 billion as required by paragraph 18(i) of Chapter 4.15 of the Guide for 
New Listing Applicants;
(b)	 each Director, chief executive and Controlling Shareholder of the Company has 
confirmed that no securities have been allocated to them or their respective close 
associates under the Size-based Exemption as required by paragraph 18(iii) of Chapter 
4.15 of the Guide for New Listing Applicants;
(c)	
the Company will comply with the public float requirement under Rule 8.08(1) of the 
Listing Rules (as amended and replaced by 19A.13A(1) for PRC issuers with no other 
listed shares); and
(d)	 details of the allocation to Cornerstone Investors and/or their close associates will be 
disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the 
consent granted by the Stock Exchange. For details of the allocations of Offer Shares 
to the Cornerstone Investors and/or their close associates, please refer to the section 
headed “Allotment Results Details — Allottees with Waivers/Consents Obtained” in this 
announcement.

<<<PAGE 32>>>
– 32 –
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate 
such Offer Shares in the International Offering to the connected clients. The allocation of 
Offer Shares to such connected clients is in compliance with all the conditions under the 
consent granted by the Stock Exchange. Details of the placement to connected clients are set 
out below:
No.
Connected 
Distributor
Connected Client
Relationship between the 
Connected Distributor and 
the Connected Client
Whether the Connected 
Client is a collective 
investment scheme which 
is not authorised by the 
SFC or is expected to 
hold the Offer Shares on 
behalf of such scheme
Number of 
Offer Shares 
intended to be 
allocated to 
the Connected 
Client
Approximate 
percentage of 
Offer Shares 
allocated to 
the Connected 
Client under 
the Global 
Offering(1)
Approximate 
percentage of 
the total share 
capital of the 
Company upon 
completion 
of the Global 
Offering
(1)
Part A — Connected Clients holding securities on a Discretionary Basis on behalf of Independent Third Parties
1.
CLSA
China AMC (HK) 
(11)
China AMC (HK) is a 
member of the same group of 
companies as CLSA
(2)
No
274,900
0.42%
0.06%
2.
CITIC Asset Management
CITIC Asset Management is a 
member of the same group of 
companies as CLSA
(2)
Yes, CITIC Asset 
Management is expected 
to hold the Offer Shares 
on behalf of such scheme. 
Please refer to note (12) 
for background and 
details of such schemes.
1,000
0.00%
0.00%
3.
CITIC Asset Management HK
CITIC Asset Management HK 
is a member of the same group 
of companies as CLSA
(2)
No
1,000
0.00%
0.00%
4.
GTJAS and HTIS
(4)
Fullgoal HK
(11)
Fullgoal HK is a member of 
the same group of companies 
as GTJAS and HTIS
(10)
No
1,166,500
16
1.78%
16
0.27%
16
5.
Fullgoal Fund
(11)
Fullgoal Fund is a member of 
the same group of companies 
as GTJAS and HTIS
(10)
No
2,172,100
16
3.32%
16
0.50%
16

<<<PAGE 33>>>
– 33 –
No.
Connected 
Distributor
Connected Client
Relationship between the 
Connected Distributor and 
the Connected Client
Whether the Connected 
Client is a collective 
investment scheme which 
is not authorised by the 
SFC or is expected to 
hold the Offer Shares on 
behalf of such scheme
Number of 
Offer Shares 
intended to be 
allocated to 
the Connected 
Client
Approximate 
percentage of 
Offer Shares 
allocated to 
the Connected 
Client under 
the Global 
Offering(1)
Approximate 
percentage of 
the total share 
capital of the 
Company upon 
completion 
of the Global 
Offering
(1)
6.
HTFH
(5)
China Southern
China Southern is a member of 
the same group of companies 
as HTFH
(13)
No
294,500
0.45%
0.07%
7.
CMBI
(14)
Bosera AM
Bosera AM is a member of the 
same group of companies as 
CMBI
(15)
No
196,300
0.30%
0.05%
No.
Connected 
Distributor
Connected Client
Relationship between the 
Connected Distributor and 
the Connected Client
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
Identities of the 
ultimate beneficial 
owners (the 
“UBO”) of the 
Offer Shares
Number of 
Offer Shares 
intended to be 
allocated to 
the Connected 
Client
Approximate 
percentage of 
Offer Shares 
allocated to 
the Connected 
Client under 
the Global 
Offering
(1)
Approximate 
percentage of 
the total share 
capital of the 
Company 
upon 
completion 
of the Global 
Offering
(1)
Part B — Connected Clients holding securities on a Non-Discretionary Basis on behalf of Independent Third Parties
8.
CLSA
CSI
(7)
CSI is a member of the 
same group of companies as 
CLSA
(2)
No
Please refer to Note 
(7) below.
566,800
0.87%
0.13%
9.
GTJAS and 
HTIS
HTIF
(8)
HTIF is a member 
of the same group of 
companies as GTJAS 
and HTIS
(3)
No
Please refer to 
Note (8) below.
1,215,100
1.86%
0.13%
10.
HTFH
HTCI
(9)
HTCI is a member 
of the same group of 
companies as HTFH
(6)
No
Please refer to 
Note (9) below.
2,858,200
17
4.38%
17
0.66%
17
Notes:
1.	
Before any exercise of the Over-allotment Option.

<<<PAGE 34>>>
– 34 –
2.	
CLSA, China AMC (HK), CITIC Asset Management, CITIC Asset Management HK and CSI 
are subsidiaries of CITIC Securities Company Limited. Each of China AMC (HK), CITIC Asset 
Management, CITIC Asset Management HK and CSI is a member of the same group of companies as 
CLSA, and accordingly, is considered as a “connected client” of CLSA pursuant to paragraph 1B of 
Appendix F1 to the Listing Rules.
3.	
GTJAS, HTIS and HTIF are subsidiaries of Guotai Haitong. HTIF is a member of the same group of 
companies as GTJAS and HTIS, and accordingly, is considered as a “connected client” of GTJAS and 
HTIS pursuant to paragraph 1B of Appendix F1 to the Listing Rules.
4.	
HTIS is a non-syndicate sub-broker in connection with the Global Offering.
5.	
HTFH is a non-syndicate sub-broker in connection with the Global Offering.
6.	
HTFH and HTCI are indirectly wholly-owned subsidiaries of Huatai Securities Co., Ltd. HTCI is a 
member of the same group of companies as HTFH, and accordingly, is considered as a “connected 
client” of HTFH.
7.	
CSI proposes to subscribe for and hold the Offer Shares as a placee under the International Offering 
on behalf of certain ultimate clients (the “CSI Ultimate Clients”), on a non-discretionary basis, 
pursuant to which: CSI will act as the single counterparty of a back-to-back total return swap 
transaction (the “CSI Back-to-back TRS”) to be entered into by it in connection with a total return 
swap order (the “CSI Client TRS”) placed and fully funded by the CSI Ultimate Clients, by which CSI 
will pass the full economic exposure of the Offer Shares placed to CSI to the CSI Ultimate Clients.
As confirmed by CSI and CLSA, CSI will hold the legal title and beneficial interest in the Offer Shares, 
but will contractually agree to pass on the full economic exposure and return of the Offer Shares to the 
CSI Ultimate Clients, on a non-discretionary basis. The CSI Ultimate Clients may exercise their early 
termination rights to terminate the CSI Client TRS at any time from the trade date of the CSI Client 
TRS which should be on or after the date on which the Offer Shares are listed on the Stock Exchange. 
Upon the final maturity or termination of the CSI Client TRS by the CSI Ultimate Clients, CSI will 
dispose of the Offer Shares on the secondary market and the CSI Ultimate Clients will receive a final 
termination amount of the CSI Back-to-back TRS which will have taken into account all the economic 
returns or economic loss in relation to the Offer Shares and the fixed amount of transaction fees of 
the CSI Back-to-back TRS and the CSI Client TRS. Due to its internal policy, CSI will not exercise the 
voting right of the Offer Shares during the terms of the CSI Back-to-back TRS.

<<<PAGE 35>>>
– 35 –
The UBO information of CSI Ultimate Clients for purpose of this place subscription is set out below:
No.
Investment Manager (if applicable)
UBOs holding 30% or more 
interest in Investment Manager 
(if applicable)
Name of CSI Ultimate Clients
UBOs holding 30% or more 
interest in CSI Ultimate Clients
1.
N/A
N/A
Canaan China Flagship Fund
Liang Hao
2.
Hover4pi Capital Management
He Hui
Hover4pi Fund I OFC
None
3.
N/A
N/A
Zhang Zili
Zhang Zili
4.
Shanghai Weining Private Equity Fund Management 
Co., Ltd. (上海衛寧私募基金管理有限公司)
Fu Chengcheng (付誠成), Lin 
Ran (林然)
Weining Focus Private Equity Investment Fund (衛寧
聚焦私募證券投資基金)
Lin Heming (林鶴鳴), Wang 
Zhangyi (王張懿)
5.
Hainan Evolution Private Equity Fund Management 
Co., Ltd. (海南進化論私募基金管理有限公司)
Wang Yiping (王一平)
Evolutionary Darwin Shangshan No. 3 Private Equity 
Investment Fund (進化論達爾文上善三號私募證券
投資基金)
None
6.
Shenzhen Dahua Xin’an Asset Management 
Enterprise (Limited Partnership) (深圳市大華信安資
產管理企業（有限合夥）)
Qi Yanchong (齊延沖)
Dahua Yongcheng No. 1 Private Equity Investment 
Fund (大華永誠一號私募證券投資基金)
Jiang yan (姜艷)
7.
Zhuhai Hunjin Private Equity Fund Management 
Partnership (Limited Partnership) (珠海渾瑾私募基
金管理合夥企業（有限合夥）)
Li Yue (李岳)
Hunjin Yuezhi Private Equity Investment Fund (渾瑾
嶽秩私募證券投資基金)
None
8.
Tibet Yuanlesheng Asset Management Co., Ltd. (西
藏源樂晟資產管理有限公司)
Zeng Xiaojie (曾曉潔)
Yuanlesheng Qiangye Private Equity Investment 
Fund (源樂晟強業私募證券投資基金)
Hu Caiyang (胡彩陽)
9.
Tibet Yuanlesheng Asset Management Co., Ltd. (西
藏源樂晟資產管理有限公司)
Zeng Xiaojie (曾曉潔)
Yuanlesheng Qiangshi Private Equity Investment 
Fund (源樂晟強勢私募證券投資基金)
None
10.
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥企業
（有限合夥）)
None
Gaoyi Liwei Selected Weishi Fund (高毅利偉精選唯
實基金)
None
11.
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥企業
（有限合夥）)
None
Gaoyi Renhao Long-Term Value Langrun Private 
Equity Investment Fund (高毅任昊長期價值朗潤私
募證券投資基金)
None
12.
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥企業
（有限合夥）)
None
Gaoyi Liwei Xinshi Private Equity Fund (高毅利偉
信實私募基金)
None
13.
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥企業
（有限合夥）)
None
Gaoyi Renhao Selected Zhifu Private Equity 
Investment Fund (高毅任昊優選致福私募證券投資
基金)
None
14.
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥企業
（有限合夥）)
None
Gaoyi Renhao Selected Chengze Private Equity 
Investment Fund (高毅任昊精選承澤私募證券投資
基金)
None
15.
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥企業
（有限合夥）)
None
Gaoyi Renhao Zhenxuan Chunhe Private Equity 
Investment Fund (高毅任昊臻選春和私募證券投資
基金)
None

<<<PAGE 36>>>
– 36 –
No.
Investment Manager (if applicable)
UBOs holding 30% or more 
interest in Investment Manager 
(if applicable)
Name of CSI Ultimate Clients
UBOs holding 30% or more 
interest in CSI Ultimate Clients
16.
Beijing Boyan Private Equity Fund Management Co., 
Ltd. (北京博衍私募基金管理有限公司)
Zhang Menglong (張夢龍)
Boyan Shanxing Value Selection Private Equity 
Investment Fund (博衍山行價值精選私募證券投資
基金)
None
17.
GF Securities Asset Management (Guangdong) Co., 
Ltd. (廣發證券資產管理（廣東）有限公司)
GF Securities Co Ltd.
GF Asset Management Shenxinli No. 71 Single Asset 
Management Plan (廣發資管申鑫利71號單一資產
管理計劃)
He Wei (賀偉)
Shanghai Gaoyi Asset Management Partnership (Limited Partnership) (上海高毅資產管理合夥企業（
有限合夥）) is a close associate of a Cornerstone Investor, namely, Perseverance Asset Management 
International (Singapore) Pte. Ltd.. We have applied consent under Chapter 4.15 of the Guide in 
relation to allocations of further H Shares to Cornerstone Investors.
To the best of CSI’s knowledge having made all reasonable inquiries, each of the CSI Onshore Clients 
is an independent third party of (i) the Company, the connected person or the associates thereof, and 
(ii) CSI and CLSA and the companies which are members of the same group of each of them.
8.	
HTIF shall hold the Offer Shares on a non-discretionary basis for hedging purposes as the single 
underlying asset of a delta one back-to-back total return swap transaction (the “GTJA Back-to-back 
TRS1”) to be entered into between HTIF and Guotai Junan Investments (Hong Kong) Limited (“GTJA 
INV”), and GTJA INV shall for hedging purposes enter into a cross-border delta one back-to-back 
total return swap transaction (the “GTJA Back-to-back TRS2”) with Guotai Haitong Securities, in 
connection with a total return swap order (the “GTHT Client TRS”) to be entered into by GTHTS 
and the GTHTS onshore clients (the “GTHT Onshore Clients”). Such GTHT Client TRS is to be 
fully funded by the GTHT Onshore Clients. The full economic exposure of the Offer Shares will be 
passed from HTIF to GTJA INV under the GTJA Back-to-back TRS1, from GTJA INV to GTHTS under 
the GTJA Back-to-back TRS2, and ultimately from GTHTS to the GTHT Onshore Clients under the 
GTHT Client TRS, pursuant to which HTIF will hold the economic interest of the Offer Shares on 
behalf of GTJA INV, GTHTS and ultimately the GTHT Onshore Clients. The GTHT Onshore Clients 
may exercise an early termination right to early terminate the GTHT Client TRS at any time from the 
trade date of the GTHT Client TRS, which should be on or after the date on which the Offer Shares 
are listed on the Stock Exchange. Accordingly, (i) GTHTS may exercise an early termination right to 
early terminate the GTJA Back-to-back TRS2 at any time from the trade date of the GTJA Back-to-back 
TRS2, and (ii) GTJA INV may exercise an early termination right to early terminate the GTJA 
Back-to-back TRS1 at any time from the trade date of the GTJA Back-to-back TRS1, which in each 
case should be on or after the date on which the Offer Shares are listed on the Stock Exchange. Upon 
the final maturity or early termination of (i) the GTHT Client TRS by the GTHT Onshore Clients, (ii) 
the GTJA Back-to-back TRS2 by GTHTS, and (iii) the GTJA Back-to-back TRS1 by GTJA INV, HTIF 
will dispose the Offer Shares on the secondary market and the GTHT Onshore Clients ultimately will 
receive a final termination amount of the GTHT Client TRS, which should have taken into account all 
the economic returns or economic loss in relation to the Offer Shares, the fixed amount in relation to 
the GTJA Back-to-back TRS1, the GTJA Back-to-back TRS2 and the GTHT Client TRS. HTIF will hold 
the legal title and the voting right of the Offer Shares by itself and pass through the economic exposure 
to GTJA INV, GTHTS and ultimately the GTHT Onshore Clients. Due to its internal policy, HTIF will 
not exercise the voting right of the Offer Shares during the tenor of the GTJA Back-to-back TRS1 and 
GTJA Back-to-back TRS2.

<<<PAGE 37>>>
– 37 –
The UBO information of GTHT Onshore Clients for purpose of this place subscription is set out below:
No.
GTHT Onshore Clients
UBOs holding 30% or more interest
1.
Zhongke Chuangxing Technology Investment Co., 
Ltd. (中科創星科技投資有限公司)
Mi Lei (米磊)
2.
Zhonghe (Tianjin) Investment management Co., 
Ltd. — Zhonghe Capital Cultivation 810 Private 
Securities Investment Fund (錦繡中和（天津）
投資管理有限公司 — 中和資本耕耘810號私募
證券投資基金)
N/A
3.
Hainan Jichuang Private Equity Fund Partnership 
(Limited Partnership) (海南集創私募基金合夥企
業(有限合夥))
Li Fengfeng (李鋒鋒)
4.
Hangzhou Zhongda Junyue Investment Co. 
Ltd. — Jun Yue Ding Zeng 2 Private Securities 
Investment Fund (杭州中大君悅投資有限公司 
— 君悅定增2號私募證券投資基金)
Wuchan Zhongda Group Co., Ltd. (物產中大
集團股份有限公司)
5.
Shanghai Tongyi Investment Management Co., 
Ltd. — Tongyi Taoli No.1 Private Securities 
Investment Fund (上海通怡投資管理有限公司 
— 通怡桃李1號私募證券投資基金)
Wang Jing (王靜)
6.
Shanghai Tongyi Investment Management Co., 
Ltd. — Tongyi Taoli No.10 Private Securities 
Investment Fund (上海通怡投資管理有限公司 
— 通怡桃李10號私募證券投資基金)
N/A
7.
Shanghai Sharewin Equity Investment Center 
(Limited Partnership) — Sharewin Changxing 
Private Securities Investment Fund (上海盛宇股
權投資中心(有限合夥) — 盛宇長興私募證券投
資基金)
N/A
8.
Winners Capital-Shidaigongying1 Private Equity 
(海南時代共贏私募基金管理合夥企業(有限合
夥))
Huang Renqiang(黄任强)
Zhongke Chuangxing Technology Investment Co., Ltd. (中科創星科技投資有限公司) is the close 
associate of an existing Shareholder, i.e. Zhongke Chuangxing, in its capacity as a wholly owned 
entity of Beijing Zhongke Chuangxing, the general partner of Zhongke Chuangxing. For details, please 
see section headed “History, Development and Corporate Structure — Investment from the Pre-IPO 
Investors — Information of the Pre-IPO Investors — 15. Beijing Phase II Zhongke Chuangxing Hard 
Technology Venture Capital Partnership (Limited Partnership) (北京二期中科創星硬科技創業投
資合夥企業(有限合夥))”. We have applied for waiver from strict compliance with Rule 10.04 of the 
Listing Rules and consent under paragraph 1C(2) of the Placing Guidelines in relation to subscription 
for H Shares by existing minority Shareholders and/or their close associates.

<<<PAGE 38>>>
– 38 –
Save as submitted above, to the best of HTIF’s knowledge having made all reasonable inquiries, each 
of the GTHT Onshore Clients is an independent third party of (i) the Company, the connected person 
or the associates thereof, and (ii) GTJAS, HTIS, HTIF, GTJA INV and GTHTS and the companies 
which are members of the same group of each of them.
9.	
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial 
public offerings (“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products 
issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading 
activities. In connection with such products, the licensed domestic securities firms, through their Hong 
Kong affiliates, may participate in Hong Kong IPOs either as placees or cornerstone investors (the 
“Cross-border Derivatives Trading Regime”).
Huatai Securities Co., Ltd. (“Huatai Securities”), the shares of which are listed on both the Shanghai 
Stock Exchange (stock code: 601688) and the Stock Exchange (stock code: 6886), is one of the 
domestic securities firms licensed to undertake cross-border derivatives trading activities. Huatai 
Securities entered into an ISDA agreement (the “ISDA Agreement”) with its indirectly wholly-owned 
subsidiary, HTCI, to set out the principal terms of any future total return swap between Huatai 
Securities and HTCI.
Pursuant to the ISDA Agreement, HTCI, which intends to participate in the Global Offering as a 
placee, will hold the beneficial interest of the Offer Shares on a non-discretionary basis as the single 
underlying holder under a back-to-back total return swap (the “Back-to-back TRS”) to be entered 
by HTCI in connection with a Client TRS (as defined below) placed by and fully funded (i.e. with 
no financing provided by HTCI) by the Huatai Ultimate Clients (as defined below), by which, HTCI 
will, subject to customary fees and commissions, pass the full economic exposure of the Offer Shares 
ultimately to the Huatai Ultimate Clients, which in effect, HTCI will hold the beneficial interest of the 
Offer Shares on behalf of the Huatai Ultimate Clients.
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the “Huatai 
Ultimate Clients”) cannot directly subscribe for the Offer Shares but may invest in derivative products 
issued by domestic securities firms licenced to undertake cross-border derivatives trading activities, 
such as Huatai Securities, with the Offer Shares as the underlying assets.

<<<PAGE 39>>>
– 39 –
Instead of directly subscribing for the Offer Shares, the Huatai Ultimate Clients, through its respective 
investment managers, will place a total return swap order (the “Client TRS”) with Huatai Securities 
in connection with the Company’s IPO and Huatai Securities will place a Back-to-back TRS order 
to HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the Back-to-back 
TRS, HTCI participates in the Company’s IPO and subscribes the Offer Shares through placing order 
with HTFH during the International Offering. The Huatai Ultimate Clients for purpose of this place 
subscription include the investment funds, details of which is set out below:
No.
Investment Manager (if applicable)
UBOs holding 30% or more 
interest in Investment Manager 
(if applicable)
Name of Huatai Ultimate Clients
UBOs holding 30% or more 
interest in Huatai Ultimate 
Clients
1.
Guangdong Ji’ao Private Equity Fund Management 
Co., Ltd. (廣東吉翱私募基金管理有限責任公司)
State-owned Assets Supervision 
& Administration Committee of 
Jilin People’s Government (吉
林省人民政府國有資產監督
管理委員會)
Ji’ao Qianheng No. 3 Private Equity Investment Fund 
(吉翱謙亨三號私募證券投資基金)
Zhao Dongyu
2.
Shanghai Greenwoods
Jiang Jinzhi
Jinglin Value Fund (景林價值基金)
N/A
3.
Shanghai Greenwoods
Jiang Jinzhi
Jinglin Zhiyuan Private Equity Fund (景林致遠私募
基金)
N/A
4.
Shanghai Greenwoods
Jiang Jinzhi
Jinglin Global Fund (景林全球基金)
N/A
5.
Shanghai Greenwoods
Jiang Jinzhi
Jinglin Jingtai Global Private Securities Investment 
Fund (景林景泰全球私募證券投資基金)
N/A
6.
Shanghai Greenwoods
Jiang Jinzhi
Jinglin Chunxiao Preferred Private Securities 
Investment Fund (景林春曉優選私募證券投資基金)
N/A
7.
Shanghai Greenwoods
Jiang Jinzhi
Jinglin Preferred Private Equity Fund (景林優選私募
基金)
N/A
8.
Shanghai Greenwoods
Jiang Jinzhi
Jinglin Innovation Growth Fund (景林創新成長基金)
N/A
9.
Shanghai Greenwoods
Jiang Jinzhi
Jinglin Jingtai Preferred Private Securities Investment 
Fund (景林景泰優選私募證券投資基金)
N/A
10.
Shanghai Greenwoods
Jiang Jinzhi
Jinglin Harvest No. 2 Fund (景林豐收2號基金)
N/A
11.
Shanghai Greenwoods
Jiang Jinzhi
Jinglin Harvest No. 3 Private Equity Fund (景林豐收
3號私募基金)
N/A
12.
Shanghai Greenwoods
Jiang Jinzhi
Jinglin Harvest No. 6 Private Securities Investment 
Fund (景林豐收6號私募證券投資基金)
N/A
13.
Shanghai Greenwoods
Jiang Jinzhi
Jinglin Jingtai Harvest Private Securities Investment 
Fund (景林景泰豐收私募證券投資基金)
N/A

<<<PAGE 40>>>
– 40 –
Other than subscription as set forth in the table above, the subscription for the Offer Shares will be 
also made by Shanghai Greenwoods Asset Management Co., Ltd. (上海景林資產管理有限公司) 
in its capacity as the fund manager of certain investment funds (Jinglin Preferred Private Equity 
Fund (景林優選私募基金), Jinglin Jingtai Preferred Private Securities Investment Fund 
(景林景泰優選私募證券投資基金), Jinglin Harvest No. 2 Fund (景林豐收2號基金), Jinglin Harvest 
No. 6 Private Securities Investment Fund (景林豐收6 號私募證券投資基金), Jinglin Jingtai Harvest 
Private Securities Investment Fund (景林景泰豐收私募證券投資基金)) as a Cornerstone Investor 
through TRS mechanism. We have applied consent under Chapter 4.15 of the Guide in relation to 
allocations of further H Shares to Cornerstone Investors.
Guangdong Ji’ao Private Equity Fund Management Co., Ltd. (廣東吉翱私募基金管理有限責任公
司) is ultimately controlled by State-owned Assets Supervision & Administration Committee of Jilin 
People’s Government (吉林省人民政府國有資產監督管理委員會) (“Jilin SASAC”). Jilin SASAC is 
the ultimate controller of Jilin Yuanheng, an existing Shareholder of the Company. As such, Guangdong 
Ji’ao is a close associate of an existing Shareholder. We has applied for waiver from strict compliance 
with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the Placing Guidelines in 
relation to subscription for H Shares by existing minority Shareholders and/or their close associates.
Save as submitted above, to the best of HTFH and HTCI’s knowledge and after making all reasonable 
enquiries, each of the Huatai Ultimate Clients is an independent third party of (i) the Company, 
the connected person or the associates thereof, and (ii) HTCI, HTFH and the companies which are 
members of the same group of HTFH.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in 
connection with the Client TRS order placed by the Huatai Ultimate Clients. Pursuant to the terms of 
the contracts of the Back-to-back TRS and the Client TRS, during the tenor of the Back-to-back TRS
and the Client TRS, subject to customary fees and commissions, all economic returns of the Offer 
Shares will be ultimately passed to the Huatai Ultimate Clients through the Back-to-back TRS and the 
Client TRS and all economic loss shall be ultimately borne by the Huatai Ultimate Clients. HTCI will 
not take any economic return or bear any economic loss in relation to the Offer Shares.
Investment in the Back-to-back TRS and the Client TRS is similar to the investment in a qualified 
domestic institutional investor fund (“QDII”) in the way that the Huatai Ultimate Clients would reap 
all the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through 
the exchange rate exposure on both the notional value of the investment and the profit and loss of the 
investment. In contrast, the profit and loss of the Back-to-back TRS and the Client TRS factor into 
account the fluctuation in RMB exchange rate upon termination of the Client TRS by converting the 
profit and loss using the current exchange rate at the time of termination. As such, the Huatai Ultimate 
Clients would bear the exchange rate exposure of the profit and loss on settlement date.

<<<PAGE 41>>>
– 41 –
The Huatai Ultimate Clients may exercise an early termination right to terminate the Client TRS 
at any time from the issue date of the Client TRS which should be on or after the date on which the 
Offer Shares are listed on the Stock Exchange at their own discretion. Upon the termination upon 
maturity or early termination of the Client TRS by the Huatai Ultimate Clients, HTCI will dispose the 
Offer Shares on the secondary market and the Huatai Ultimate Clients will receive a final settlement 
amount in cash in accordance with the terms and conditions of the Back-to-back TRS and the Client 
TRS which should have taken into account all the economic returns or economic loss in relation to 
the Offer Shares. If upon the maturity of the Client TRS, the Huatai Ultimate Clients intend to extend 
the investment period, subject to further agreement between Huatai Securities and the relevant Huatai 
Ultimate Clients, the term of the Client TRS could be extended by way of a new issuance or a tenor 
extension. Accordingly, Huatai Securities will extend the term of the Back-to-back TRS by way of a new 
issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and 
pass through the economic exposure to the Huatai Ultimate Clients, each being an onshore client who 
places a Client TRS order with Huatai Securities in connection with the IPO of the Company. HTCI 
will not exercise the voting right of the Offer Shares during the tenor of the Back-to-back TRS.
During the life of the Client TRS and Back-to-back TRS, HTCI may continue to hold the Offer Shares 
in its custodian account, or to hold some or all of the Offer Shares in a prime brokerage account for 
stock borrowing purposes, where HTCI will lend out its holding of underlying Offer Shares in the form 
of stock borrowing loans consistent with market practice to lower its finance costs, provided that HTCI 
has the ability to call back the Offer Shares on loan at any time in order to satisfy its obligations under 
the Back-to-back TRS to ensure the economic interests are ultimately passed to the Huatai Ultimate 
Clients.
10.	
Fullgoal HK is a wholly o	wned subsidiary of Fullgoal Fund, which is owned by Guotai Haitong as to 
27.775%. GTJAS and HTIS, are subsidiaries of Guotai Haitong. Each Fullgoal HK and Fullgoal Fund 
is considered as a member of the same group of companies as GTJAS and HTIS and therefore is a 
“connected client” of GTJAS and HTIS for the purpose of paragraph 1B of Appendix F1 to the Listing 
Rules.
11.	
China AMC (HK), Fullgoal HK and Fullgoal Fund are Cornerstone Investors. We have applied 
consent under Chapter 4.15 of the Guide in relation to allocations of further H Shares to Cornerstone 
Investors.
12.	
CITIC Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager 
managing the funds on behalf of their investors (the “CITIC Asset Management Ultimate Clients”), 
each of which is, to the best knowledge of CITIC Asset Management, an independent third party of 
the Company, its subsidiaries, its substantial shareholders, CITIC Asset Management, CLSA and the 
companies which are members of the same group of CLSA. No ultimate beneficial owner holds 30% or 
more interest in the funds.

<<<PAGE 42>>>
– 42 –
The details of the CITIC Asset Management Ultimate Clients are as follow.
No.
Fund Name
Fund Manager
UBO of Fund Manager
Limited Partner/
Shareholding 
holding 30% or 
more in the CITIC 
Asset Management 
Ultimate Clients
1.
CITIC SECURITIES COMPANY 
LIMITEDXINHANG ZHIYUAN NO.1 (中信證券
信航致遠 1號集合資產管理計劃)
CITIC Asset 
Management
CITIC Securities 
Company Limited
N/A
2.
CITIC SECURITIES COMPANY 
LIMITEDXINHANG ZHIYUAN NO.3 (中信證券
信航致遠 3號集合資產管理計劃)
CITIC Asset 
Management
CITIC Securities 
Company Limited
N/A
3.
CITIC Securities AM-Guibinfengyuan No.118 
QDII (中信證券資管貴賓豐元118號 QDII集合資
產管理計劃)
CITIC Asset 
Management
CITIC Securities 
Company Limited
N/A
To the best of knowledge of CITIC Asset Management and after making all reasonable enquiries, 
CITIC Asset Management Ultimate Client, together with each of their ultimate beneficial owners, is 
an independent third party of the Company, its subsidiaries, its substantial shareholders, CITIC Asset 
Management, CLSA and the companies which are members of the same group of CLSA.\
13.	
Huatai Securities is the controlling shareholder of China Southern. HTFH is an indirectly wholly-
owned subsidiary of Huatai Securities. China Southern is a member of the same group of companies 
as HTFH, and accordingly, is considered as a “connected client” of HTFH.
14.	
CMBI is a non-syndicate sub-broker in connection with the Global Offering.
15.	
CMBI is an indirectly subsidiary of China Merchants Bank. China Merchants Bank is an indirect 
controlling shareholder of the Bosera AM. Bosera AM is a member of the same group of companies as 
CMBI, and accordingly, is considered as a “connected client” of CMBI.
16.	
Including all Offer Shares allocated to Fullgoal HK and Fullgoal Fund, being the connected clients of 
CTJAS and HTIS, as placees and cornerstone investors.
17.	
Including all Offer Shares allocated to HTCI, being the connected client of HTFH, as a placee and a 
cornerstone investor.

<<<PAGE 43>>>
– 43 –
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong 
Limited (the “Stock Exchange”) and Hong Kong Securities Clearing Company Limited 
(“HKSCC”) take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part 
of the contents of this announcement.
This announcement is for information purposes only and does not constitute an invitation 
or offer to acquire, purchase or subscribe for any securities. This announcement is not a 
prospectus. Potential investors should read the Prospectus for detailed information about 
the Global Offering described below before deciding whether or not to invest in the Offer 
Shares. Any investment decision in relation to the Offer Shares should be taken solely in 
reliance on the information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, 
in or into the United States (including its territories and possessions, any state of the 
United States and the District of Columbia). This announcement does not, and is not 
intended to, constitute or form a part of any offer to sell or solicitation to purchase or 
subscribe for any securities in the United States or in any other jurisdiction. The Offer 
Shares have not been, and will not be, registered under the U.S. Securities Act of 1933, 
as amended from time to time (the “U.S. Securities Act”) or any securities law of any 
state or other jurisdiction of the United States and may not be offered, sold, pledged, or 
otherwise transferred within the United States, except pursuant to an exemption from, or 
in a transaction not subject to, the registration requirements of the U.S. Securities Act and 
in compliance with any applicable state securities laws. There will be no public offer of 
the Offer Shares in the United States. The Offer Shares are being offered and sold solely 
outside the United States in offshore transactions in reliance on Regulation S under the U.S. 
Securities Act.
Potential investors of the Offer Shares should note that the Joint Sponsors and Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) in their sole 
and absolute discretion may, by notice in writing to our Company, terminate the Hong 
Kong Underwriting Agreement with immediate effect upon the occurrence of any of the 
events set out in the paragraph headed “Underwriting — Underwriting Arrangements 
and Expenses — The Hong Kong Public Offering — Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is 
currently expected to be on April 17, 2026).

<<<PAGE 44>>>
– 44 –
PUBLIC FLOAT
Pursuant to Rule 19A.13A of the Listing Rules, assuming that the Over-allotment Option is 
not exercised, based on the Offer Price of HK$39.88 per Offer Share, the expected market 
capitalization upon the Listing is HK$17,360 million, and the minimum prescribed public 
float percentage applicable to the Shares is 15%. Immediately following completion of 
the Global Offering (assuming the Over-allotment Option is not exercised), an aggregate 
of 79,630,450 H Shares, representing approximately 18.29% of the issued share capital of 
the Company will count towards the public float. Therefore, the number of H Shares held 
in public hands is higher than the prescribed percentage of H Shares required to be held in 
public hands of 15% under Rule 19A.13A(1) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following 
the Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall 
not be counted towards the free float of the H Shares of the Company at the time of Listing. 
Based on the Offer Price of HK$39.88 per H Share, the Company satisfies the free float 
requirement under Rule 19A.13C of the Listing Rules.
The Directors confirm that immediately after the completion of the Global Offering 
(assuming the Over-allotment Option is not exercised), (i) no placee will, individually, be 
placed more than 10% of the enlarged issued share capital of the Company; (ii) there will 
not be any new substantial shareholder (as defined in the Listing Rules) of the Company; 
(iii) the three largest public shareholders of the Company do not hold more than 50% of the 
H Shares in public hands at the time of the Listing in compliance with Rules 8.08(3) and 
8.24 of the Listing Rules; and (iv) there will be at least 300 H Shareholders at the time of the 
Listing in compliance with Rule 8.08(2) of the Listing Rules.

<<<PAGE 45>>>
– 45 –
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, 
April 17, 2026 (Hong Kong time), provided that the Global Offering has become 
unconditional in all respects at or before that time, and the right of termination described 
in “Underwriting — Underwriting Arrangements and Expenses — The Hong Kong Public 
Offering — Grounds for Termination” has not been exercised. Investors who trade the H 
Shares on the basis of publicly available allocation details prior to the receipt of H Share 
certificates or prior to the H Share certificates becoming valid evidence of title do so entirely 
at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Friday, 
April 17, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Friday, April 17, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 100 Shares each, and the stock code of the Shares will 
be 3277.
By order of the Board
GPIXEL CHANGCHUN MICROELECTRONICS INC.
Dr. WANG Xinyang
Chairman, General Manager, Chief Executive Officer, 
Executive Director
Hong Kong, April 16, 2026
As of the date of this announcement, the Board comprises: (i) Dr. WANG Xinyang, Dr. ZHANG Yanxia 
and Ms. WU Qinyun as executive Directors; (ii) Ms. YANG Yi, Dr. CHU Hairong and Dr. XIONG Jingying 
as non-executive Directors; and (iii) Dr. WANG Xinlu, Dr. XIE Ning and Dr. GAO Teng as independent 
non-executive Directors.
