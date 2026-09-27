# 配发结果公告抽取任务：6809.HK Montage Technology Co., Ltd. - H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**06/02/2026 22:30**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0206/2026020601350.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6809.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus 
dated January 30, 2026 (the “Prospectus”) issued by Montage Technology Co., Ltd. (瀾起科技股份有限公司) (the 
“Company”) for detailed information about the Global Offering described below before deciding whether or not to 
invest in the H Shares thereby being offered. Any investment decision in relation to the Offer Shares should be taken 
solely in reliance on the information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
In connection with the Global Offering, Morgan Stanley Asia Limited, as stabilizing manager (the “Stabilizing 
Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, the extent permitted by the 
applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect transactions with 
a view to stabilizing or supporting the market price of the H Shares at such price, in such amounts and in such manners 
as the Stabilizing Manager, its affiliates or any person acting for it may determine and at a level higher than that which 
might otherwise prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing 
Manager (or its affiliates or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, 
if taken, (a) will be conducted at the absolute discretion of the Stabilization Manager (or its affiliates or any person 
acting for it) and in what the Stabilizing Manager reasonably regards as the best interest of our Company, (b) may 
be discontinued at any time and (c) is required to be brought to an end within 30 days of the last day for lodging 
applications under the Hong Kong Public Offering (which is Friday, March 6, 2026). Such stabilizing action, if taken, 
may be effected in all jurisdictions where it is permissible to do so, in each case in compliance with all applicable 
laws, rules and regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 571 W 
of the Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws 
of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Friday, March 6, 2026). 
After this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of 
the H Shares, could fall.
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on behalf of 
the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
Monday, February 9, 2026).

<<<PAGE 2>>>
2
Montage Technology Co., Ltd.
瀾起科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
65,890,000 H Shares (subject to the 
 Over-allotment Option)
Number of Hong Kong Offer Shares
:
6,589,000 H Shares
Number of International Offer Shares
:
59,301,000 H Shares (subject to the 
 Over-allotment Option)
Final Offer Price
:
HK$106.89 per H Share, plus brokerage 
 of 1.0%, SFC transaction levy of 
 0.0027%, AFRC transaction levy of 
 0.00015% and Stock Exchange trading 
 fee of 0.00565%
Nominal value
:
RMB1.00 per H Share
Stock Code
:
6809
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators, Joint Global
Coordinators, Joint Bookrunners and Joint Lead Managers
(in alphabetical order)
Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
1 
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) and 
Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this announcement, 
make no representation as to its accuracy or completeness and expressly disclaim any liability whatsoever for any loss 
howsoever arising from or in reliance upon the whole or any part of the contents of this announcement. 
 
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States (including its 
territories and possessions, any state of the United States and the District of Columbia). This announcement does not constitute 
or form a part of any offer or solicitation to purchase or subscribe for securities in the United States or in any other jurisdictions. 
The Offer Shares have not been and will not be registered under the United States Securities Act of 1933, as amended from time 
to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the United States and may not be offered, 
sold, pledged or otherwise transferred within the United States, except in transactions exempt from, or not subject to, the 
registration requirements of the U.S. Securities Act and in compliance with any applicable state securities laws. There will be 
no public offer of the Offer Shares in the United States. The Offer Shares are being offered and sold solely (1) to qualified 
institutional buyers as defined in Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under the 
U.S. Securities Act; and (2) outside the United States in offshore transactions in reliance on Regulation S under the U.S. 
Securities Act and applicable laws of each jurisdiction where those offers and sales occur. 
 
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated January 
30, 2026 (the “Prospectus”) issued by Montage Technology Co., Ltd. (瀾起科技股份有限公司) (the “Company”) for 
detailed information about the Global Offering described below before deciding whether or not to invest in the H Shares 
thereby being offered. Any investment decision in relation to the Offer Shares should be taken solely in reliance on the 
information in the Prospectus. 
 
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus. 
 
In connection with the Global Offering, Morgan Stanley Asia Limited, as stabilizing manager (the “Stabilizing 
Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, the extent permitted by the 
applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect transactions with a view 
to stabilizing or supporting the market price of the H Shares at such price, in such amounts and in such manners as 
the Stabilizing Manager, its affiliates or any person acting for it may determine and at a level higher than that which 
might otherwise prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing 
Manager (or its affiliates or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, if 
taken, (a) will be conducted at the absolute discretion of the Stabilization Manager (or its affiliates or any person acting 
for it) and in what the Stabilizing Manager reasonably regards as the best interest of our Company, (b) may be discontinued 
at any time and (c) is required to be brought to an end within 30 days of the last day for lodging applications under 
the Hong Kong Public Offering (which is Friday, March 6, 2026). Such stabilizing action, if taken, may be effected in all 
jurisdictions where it is permissible to do so, in each case in compliance with all applicable laws, rules and regulatory 
requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 571 W of the Laws of Hong Kong), 
as amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong). 
 
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Friday, March 6, 2026). After 
this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of the H 
Shares, could fall. 
 
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on behalf of 
the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus 
at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Monday, 
February 9, 2026). 

<<<PAGE 4>>>
1 
 
 
MONTAGE TECHNOLOGY CO., LTD. 
瀾起科技股份有限公司 
ANNOUNCEMENT OF FINAL OFFER PRICE AND 
ALLOTMENT RESULTS 
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same meanings as 
those defined in the prospectus dated January 30, 2026 (the “Prospectus”) issued by Montage Technology Co., 
Ltd. (the “Company”). 
 
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could move 
substantially even with a small number of H Shares traded and should exercise extreme caution when 
dealing in the H Shares. 
SUMMARY 
 
Company Information 
Stock Code 
6809 
Stock short name 
MONTAGE TECH  
Dealings commencement date 
February 9, 2026* 
* see note at the end of the announcement 
 
Price Information 
Final Offer Price 
HK$106.89 
 
Offer Shares and Share Capital 
Number of Offer Shares 
65,890,000 
Number of Offer Shares in Hong Kong Public Offering 
6,589,000  
Number of Offer Shares in International Offering 
59,301,000  
Number of issued Shares upon Listing (before exercise of the 
Over-allotment Option) 
1,212,316,521 
 
 
Over-allocation 
No. of Offer Shares over-allocated 
9,883,500 
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases in 
the secondary market at prices that do not exceed the Offer Price or through deferred delivery or a 
combination of these means. In the event the Over-allotment Option is exercised, an announcement will be 
made on the Stock Exchange’s website. 

<<<PAGE 5>>>
2 
 
 
 
Proceeds 
Gross proceeds(before the exercise of the Over-allotment Option) 
(Note) 
HK$7,043.0 million 
Less: Estimated listing expenses payable based on Final 
Offer Price 
HK$138.4 million 
Net proceeds 
HK$6,904.6 million 
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. 
The Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis. 
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING 
 
No. of valid applications 
260,646 
No. of successful applications 
56,356 
Subscription level 
707.3 times 
Claw-back triggered 
N/A 
No. of Offer Shares initially available under the Hong Kong Public 
Offering 
6,589,000 
Final no. of Offer Shares under the Hong Kong Public Offering 
6,589,000 
% of Offer Shares under the Hong Kong Public Offering to the Global 
Offering (before the exercise of the Over-allotment Option) 
10% 
 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.eipo.com.hk/eIPOAllotment 
to 
perform 
a 
search 
by 
identification 
document 
number 
or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees. 
INTERNATIONAL OFFERING 
 
No. of placees 
412 
Subscription Level 
37.67 times 
No. of Offer Shares initially available under the International Offering 
59,301,000 
Final no. of Offer Shares under the International Offering (before the 
exercise of the Over-allotment Option) 
59,301,000 
% of Offer Shares under the International Offering to the Global 
Offering (before the exercise of the Over-allotment Option) 
90% 

<<<PAGE 6>>>
3 
 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a waiver from 
strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) of Appendix F1 to 
the Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange to permit the Company to allocate 
certain Offer Shares in the International Offering to certain permitted existing shareholder ("Permitted Existing 
Shareholder") and/or their close associates; and (b) a consent under Chapter 4.15 of the Guide for New Listing 
Applicants to permit the Company to, among other things, allocate further H Shares in the International Offering 
to the Cornerstone Investors, existing shareholder and/or their close associate (i) none of the Offer Shares 
subscribed by the placees and the public have been financed directly or indirectly by the Company, any of the 
Directors, chief executive, substantial Shareholders, existing Shareholders of the Company or any of its 
subsidiaries or their respective close associates; and (ii) none of the placees and the public who have purchased 
the Offer Shares are accustomed to taking instructions from the Company, any of the Directors, chief executive, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective close 
associates in relation to the acquisition, disposal, voting or other disposition of H Shares registered in his/her/its 
name or otherwise held by him/her/it.  
The placees in the International Offering include the following: 
Cornerstone Investors 
 
 
 
 
 
 
 
Investor 
 
 
 
 
 
 
No. of Offer 
Shares allocated 
 
% of total issued H 
Shares after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised) (1)(2) 
% of total issued share 
capital in the Company 
after the Global Offering 
(assuming the Over-
allotment Option is not 
exercised and no 
additional Shares are 
issued pursuant to the 
Employee Incentive 
Plans)(1)(2) 
 
 
 
 
Existing 
shareholders or 
their close 
associates 
J.P. Morgan Investment 
Management Inc. 
(“JPMIMI”) 
4,814,800 
7.31% 
0.40% 
Yes 
UBS Asset Management 
(Singapore) Ltd. (“UBS 
AM”) 
4,814,800 
7.31% 
0.40% 
No 
 Yunfeng Investments Limited (“Yunfeng Capital”) 
New Alternative 
Limited (“New 
Alternative”)  
3,282,800 
4.98% 
0.27% 
No 
New Golden Future 
Limited (“New 
Golden Future”) 
1,532,000 
2.33% 
0.13% 
No 
Alisoft China Holding 
Limited (“Alisoft 
China”) 
4,012,400 
6.09% 
0.33% 
No 
Aspex Master Fund 
(“Aspex”) 
3,064,000 
4.65% 
0.25% 
No 
Janchor Partners Pan-
Asian Master Fund 
(“Janchor Fund”) 
3,064,000 
4.65% 
0.25% 
No 
abrdn Asia 
Limited (“abrdn Asia”) 
1,386,100 
2.10% 
0.11% 
Yes 

<<<PAGE 7>>>
4 
 
 
 
 
 
 
 
 
 
Investor 
 
 
 
 
 
 
No. of Offer 
Shares allocated 
 
% of total issued H 
Shares after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised) (1)(2) 
% of total issued share 
capital in the Company 
after the Global Offering 
(assuming the Over-
allotment Option is not 
exercised and no 
additional Shares are 
issued pursuant to the 
Employee Incentive 
Plans)(1)(2) 
 
 
 
 
Existing 
shareholders or 
their close 
associates 
Baring Asset 
Management (Asia) 
Limited (“Barings”) 
1,094,200 
1.66% 
0.09% 
Yes 
Mirae Asset Securities 
Co., Ltd. (“Mirae 
Asset”) 
1,094,200 
1.66% 
0.09% 
No 
AGIC Partners Holding 
(Cayman) II Limited 
(“AGIC”) 
729,500 
1.11% 
0.06% 
No 
Hel Ved Master Fund 
(“Hel Ved”) 
729,500 
1.11% 
0.06% 
No 
Huaqin Telecom Hong 
Kong Limited (“Huaqin 
Telecom”) 
729,500 
1.11% 
0.06% 
No 
Huadeng Summit 
Fortitude Ventures Ltd 
(“Huadeng 
Technology”) 
583,600 
0.89% 
0.05% 
No 
PSBC Wealth 
Management Co., Ltd. 
(“PSBC Wealth”) 
583,600 
0.89% 
0.05% 
No 
Taikang Life Insurance 
Co., Ltd (“Taikang 
Life”) 
583,600 
0.89% 
0.05% 
Yes 
MY Asian Opportunities 
Master Fund, L.P. (“MY 
Asian”) 
364,700 
0.55% 
0.03% 
No 
Qube Master Fund Ltd 
(“Qube”) 
364,700 
0.55% 
0.03% 
No 
Total 
32,828,000 
49.82% 
2.71% 
 
Notes: 
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering (assuming the Over-allotment Option is not exercised). 
(2) 
In addition to the Offer Shares subscribed for as Cornerstone Investors, JPMIMI, Barings, abrdn Asia, Aspex, 
Mirae Asset, UBS AM, Janchor Fund, Yunfeng Capital, Alisoft and AGIC, and/or their close associates, were 
allocated further Offer Shares as placees in the International Offering. Please refer to the section headed 
“Allotment Results Details – International Offering – Allotees with Waivers/Consents Obtained” in this 
announcement for details. Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-
up as indicated below. For details, please refer to the section headed “Lock-up Undertakings – Cornerstone 
Investors” in this announcement.  
 
 

<<<PAGE 8>>>
5 
 
 
Allotees with Waivers/Consents Obtained 
Investor 
No. of Offer 
Shares allocated 
% of total issued H 
Shares after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised) Note 3 
% of total issued share 
capital in the Company 
after the Global Offering 
(assuming the Over-
allotment Option is not 
exercised and no 
additional Shares are 
issued pursuant to the 
Employee Incentive 
Plans) 
Note 4 
Relationship 
Allotees with consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further 
H Shares to existing Shareholders and Cornerstone Investors and/or their close associates Note 1  
Alisoft China 
1,823,800 
2.77% 
0.15% 
Same entity as the 
Cornerstone Investor 
JP Morgan Asset 
Management (Asia 
Pacific) Limited 
("JPMAM")  
941,000  
1.43% 
0.08%  
Close associate of a 
Cornerstone Investor, 
JPMIMI and same entity 
as an existing 
Shareholder  
UBS AM 
941,000 
1.43% 
0.08% 
Same entity as the 
Cornerstone Investor 
ICBC UBS Asset 
Management Co., Ltd. 
(工银瑞信基金管理有
限公司, "ICBC UBS") 
3,800 
0.00577% 
0.00031% 
Close associate 
of UBS AM, a 
Cornerstone 
Investor 
ICBC UBS Asset 
Management 
(International) 
Company Limited (工
银瑞信资产管理（国
际）有限公司, "ICBC 
UBS International") 
600 
0.00091% 
0.00005% 
Close associate 
of UBS AM, a 
Cornerstone 
Investor 
Strong Media Limited 
("Strong Media") 
941,000 
1.43% 
0.08% 
Close associate of the 
Cornerstone Investor, 
Yunfeng Capital 
abrdn Asia 
547,200 
0.83% 
0.05% 
Same entity as the 
Cornerstone Investor 
and an existing 
Shareholder 
Barings 
510,700 
0.78% 
0.04% 
Same entity as the 
Cornerstone Investor 
and an existing 
Shareholder 
Mirae Asset 
255,300 
0.39% 
0.02% 
Same entity as the 
Cornerstone Investor 
Mirae Asset Global 
Investments (HK) 
Limited 
182,400 
0.28% 
0.02% 
Close associate of a 
Cornerstone Investor, 
Mirae Asset 
Mirae Asset Securities 
(HK) Limited 
73,000 
0.11% 
0.01% 
Close associate of a 
Cornerstone Investor, 
Mirae Asset 
AGIC 
364,800 
0.55% 
0.03% 
Same entity as the 
Cornerstone Investor 

<<<PAGE 9>>>
6 
 
 
Investor 
No. of Offer 
Shares allocated 
% of total issued H 
Shares after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised) Note 3 
% of total issued share 
capital in the Company 
after the Global Offering 
(assuming the Over-
allotment Option is not 
exercised and no 
additional Shares are 
issued pursuant to the 
Employee Incentive 
Plans) 
Note 4 
Relationship 
Aspex 
146,000 
0.22% 
0.01% 
Same entity as the 
Cornerstone Investor 
Janchor Partners 
Limited  
146,000 
0.22% 
0.01% 
Close associate of the 
Cornerstone Investor, 
Janchor Fund 
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients Note 2 
CICC Financial Trading 
Limited ("CICC FT") 
49,700 
0.07543% 
0.00410% 
Connected client as a 
placee 
Huatai Capital 
Investment Limited 
("HTCI") 
446,000 
0.67689% 
0.03679% 
Connected client as a 
placee 
CITIC Securities 
International Capital 
Management Limited 
("CSICM") 
300 
0.00046% 
0.00002% 
Connected client as a 
placee 
Morgan Stanley 
Investment 
Management Company 
("MSIM") 
800 
0.00121% 
0.00007% 
Connected client as a 
placee 
ICBC UBS Asset 
Management Co., Ltd. (
工银瑞信基金管理有
限公司, "ICBC UBS") 
3,800 
0.00577% 
0.00031% 
Connected client as a 
placee 
ICBC UBS Asset 
Management 
(International) 
Company Limited  (工
银瑞信资产管理（国
际）有限公司, "ICBC 
UBS International") 
600 
0.00091% 
0.00005% 
Connected client as a 
placee 
UBS Asset 
Management 
(Singapore) 
Ltd. ("UBS AM") 
941,000 
1.42814% 
0.07762% 
Connected client as a 
placee 
Goldman Sachs Asset 
Management 
(Singapore) Pte. Ltd. 
acting in its capacity as 
investment manager 
("GSAM") 
182,400 
0.27683% 
0.01505% 
Connected client as a 
placee 
Bosera Asset 
Management 
(International) 
Co., Ltd 
7,200 
0.01093% 
0.00059% 
Connected client as a 
placee 

<<<PAGE 10>>>
7 
 
 
Investor 
No. of Offer 
Shares allocated 
% of total issued H 
Shares after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised) Note 3 
% of total issued share 
capital in the Company 
after the Global Offering 
(assuming the Over-
allotment Option is not 
exercised and no 
additional Shares are 
issued pursuant to the 
Employee Incentive 
Plans) 
Note 4 
Relationship 
("Bosera AM") 
CITIC Securities Asset 
Management (HK) 
Limited 
("CITICS AM HK") 
124,000 
0.18819% 
0.01023% 
Connected client as a 
placee 
China Asset 
Management (Hong 
Kong) Limited 
("China AMC HK") 
36,500 
0.05540% 
0.00301% 
Connected client as a 
placee 
Guotai Junan 
Investments (Hong 
Kong) Limited 
("GTJA Investment") 
1,204,500 
1.82805% 
0.09936% 
Connected client as a 
placee 
Fullgoal Fund 
Management Co., Ltd. 
("Fullgoal Fund") 
45,000 
0.06830% 
0.00371% 
Connected client as a 
placee 
Fullgoal Asset 
Management (HK) 
Limited 
("Fullgoal HK") 
28,000 
0.0425% 
0.00231% 
Connected client as a 
placee 
China Southern Asset 
Management Co., Ltd 
("China Southern") 
36,500 
0.0554% 
0.0030% 
Connected client as a 
placee 
Notes:  
1. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details – International Offering – Cornerstone Investors” in this announcement. For details of the 
consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further H 
Shares to the existing Shareholders and/or their close associates and Cornerstone Investors, please refer to the 
section headed “Others/Additional Information – Allotees with consent under Chapter 4.15 of the Guide for 
New Listing Applicants in relation to allocations of further H Shares to Cornerstone Investors” in this 
announcement.  
 
2. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for 
New Listing Applicants in relation to allocations to connected clients, please refer to the section headed “Others 
/ Additional Information – Placing to connected clients with a prior consent under paragraph 1C(1) of the 
Placing Guidelines” in this announcement.  
 
3. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be 
issued under the Global Offering (assuming the Over-allotment Option is not exercised).  
 
4. 
Not taking into account any A Shares held by the relevant investors.  
 

<<<PAGE 11>>>
 
 
LOCK-UP UNDERTAKINGS 
Cornerstone Investors 
 
Name 
Number of H Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing 
% of total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing (assuming the 
Over-allotment 
Option is not 
exercised)Note 1 
% of total issued 
share capital in the 
Company subject to 
lock-up undertakings 
upon Listing 
(assuming the Over-
allotment 
Option is not 
exercised and no 
additional Shares are 
issued pursuant to the 
Employee Incentive 
Plans) 
Last day subject to 
the lock-up 
undertakingsNote 2 
JPMIMI 
4,814,800 
7.31% 
0.40% 
August 8, 2026 
UBS AM 
4,814,800 
7.31% 
0.40% 
August 8, 2026 
Yunfeng Capital 
New Alternative  
3,282,800 
4.98% 
0.27% 
August 8, 2026 
New Golden 
Future 
1,532,000 
2.33% 
0.13% 
August 8, 2026 
Alisoft China 
4,012,400 
6.09% 
0.33% 
August 8, 2026 
Aspex 
3,064,000 
4.65% 
0.25% 
August 8, 2026 
Janchor Fund 
3,064,000 
4.65% 
0.25% 
August 8, 2026 
abrdn Asia 
1,386,100 
2.10% 
0.11% 
August 8, 2026 
Barings 
1,094,200 
1.66% 
0.09% 
August 8, 2026 
Mirae Asset 
1,094,200 
1.66% 
0.09% 
August 8, 2026 

<<<PAGE 12>>>
 
 
AGIC 
729,500 
1.11% 
0.06% 
August 8, 2026 
Hel Ved 
729,500 
1.11% 
0.06% 
August 8, 2026 
Huaqin Telecom 
729,500 
1.11% 
0.06% 
August 8, 2026 
Huadeng Technology 
583,600 
0.89% 
0.05% 
August 8, 2026 
PSBC Wealth 
583,600 
0.89% 
0.05% 
August 8, 2026 
Taikang Life 
583,600 
0.89% 
0.05% 
August 8, 2026 
MY Asian 
364,700 
0.55% 
0.03% 
August 8, 2026 
Qube 
364,700 
0.55% 
0.03% 
August 8, 2026 
Total 
32,828,000 
49.82% 
2.71% 
 

<<<PAGE 13>>>
 
 
Notes: 
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering. 
2. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on 
August 8, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or 
transferring H Shares subscribed pursuant to the relevant cornerstone investment agreements after 
the indicated date. 

<<<PAGE 14>>>
11 
 
 
PLACEE CONCENTRATION ANALYSIS  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Placees* 
Number of H 
Shares allotted 
Allotment as 
% of 
International 
Offering 
(assuming no 
exercise of the 
Over- 
allotment 
Option) 
Allotment as 
% of 
International 
Offering 
(assuming the 
Over-
allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
Allotment as 
% of total 
Offer Shares 
(assuming no 
exercise of the 
Over-
allotment 
Option) 
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over-
allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
Number of H 
Shares held 
upon Listing 
% of total 
issued H share 
capital upon 
Listing 
(assuming no 
exercise of the 
Over-
allotment 
Option) 
% of total 
issued H share 
capital upon 
Listing 
(assuming the 
Over-
allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
% of total 
issued share 
capital upon 
Listing 
(assuming no 
exercise of the 
Over-
allotment 
Option and no 
additional 
Shares are 
issued 
pursuant to 
the Employee 
Incentive 
Plans) 
% of total 
issued share 
capital upon 
Listing 
(assuming the 
Over-
allotment 
Option is fully 
exercised and 
new H Shares 
are issued and 
no additional 
Shares are 
issued 
pursuant to 
the Employee 
Incentive 
Plans) 
Top 1 
5,836,200  
9.84% 
8.44% 
8.86% 
7.70% 
5,836,200  
8.86% 
7.70% 
0.48% 
0.48% 
Top 5 
26,313,600  
44.37% 
38.03% 
39.94% 
34.73% 
26,313,600  
39.94% 
34.73% 
2.17% 
2.15% 
Top 10 
36,125,700  
60.92% 
52.22% 
54.83% 
47.68% 
36,125,700  
54.83% 
47.68% 
2.98% 
2.96% 
Top 25 
49,951,500 
84.23% 
72.20% 
75.81% 
65.92% 
49,951,500 
75.81% 
65.92% 
4.12% 
4.09% 
 
Note: 
 
* 
Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 15>>>
12 
 
 
H SHAREHOLDER CONCENTRATION ANALYSIS 
 
 
 
 
 
 
 
 
 
 
 
 
H 
Sharehol 
ders* 
Number of H 
Shares allotted 
Allotment as 
% of 
International 
Offering 
(assuming no 
exercise of the 
Over- 
allotment 
Option) 
Allotment as 
% of 
International 
Offering 
(assuming the 
Over-
allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
Allotment as 
% of total 
Offer Shares 
(assuming no 
exercise of the 
Over-
allotment 
Option) 
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over-
allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
Number of H 
Shares held 
upon Listing 
% of total 
issued H share 
capital upon 
Listing 
(assuming no 
exercise of the 
Over-
allotment 
Option) 
% of total 
issued H share 
capital upon 
Listing 
(assuming the 
Over-
allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
% of total 
issued share 
capital upon 
Listing 
(assuming no 
exercise of the 
Over-
allotment 
Option and no 
additional 
Shares are 
issued 
pursuant to 
the Employee 
Incentive 
Plans) 
% of total 
issued share 
capital upon 
Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued and 
no additional 
Shares are 
issued pursuant
to the Share 
Incentive 
Plans) 
Top 1 
5,836,200  
9.84% 
8.44% 
8.86% 
7.70% 
5,836,200  
8.86% 
7.70% 
0.48% 
0.48% 
Top 5 
26,313,600  
44.37% 
38.03% 
39.94% 
34.73% 
26,313,600  
39.94% 
34.73% 
2.17% 
2.15% 
Top 10 
36,125,700  
60.92% 
52.22% 
54.83% 
47.68% 
36,125,700  
54.83% 
47.68% 
2.98% 
2.96% 
Top 25 
49,951,500  
84.23% 
72.20% 
75.81% 
65.92% 
49,951,500 
75.81% 
65.92% 
4.12% 
4.09% 
 
Note: 
 
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing. 

<<<PAGE 16>>>
13 
 
 
SHAREHOLDER CONCENTRATION ANALYSIS 
 
 
 
 
 
 
 
 
 
Shareholders 
* 
Number of H 
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
Allotment as % 
of International 
Offering 
(assuming the 
Over- allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
Allotment as 
% of total 
Offer Shares 
(assuming no 
exercise of the 
Over-
allotment 
Option) 
Allotment as % 
of total Offer 
Shares 
(assuming the 
Over- allotment 
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
upon Listing# 
% of total issued 
share capital upon 
Listing 
(assuming no 
exercise of the 
Over-allotment 
Option and no 
additional Shares 
are issued pursuant 
to the Employee 
Incentive Plans) 
% of total issued 
share capital upon 
Listing (assuming 
the Over-allotment 
Option is fully 
exercised and new 
H Shares are issued 
and no additional 
Shares are issued 
pursuant to the 
Employee 
Incentive Plans) 
Top 1 
-    
0.00% 
0.00% 
0.00% 
0.00% 
-    
82,918,511  
6.84% 
6.78% 
Top 5 
5,755,800  
9.71% 
8.32% 
8.74% 
7.60% 
5,755,800  
209,895,205  17.31% 
17.17% 
Top 10 
6,339,400  
10.69% 
9.16% 
9.62% 
8.37% 
6,339,400  
274,107,032  22.61% 
22.43% 
Top 25 
24,410,000  41.16% 
35.28% 
37.05% 
32.21% 
24,410,000  369,642,702  30.49% 
30.24% 
 
Note: 
 
* 
Ranking of Shareholders is based on the aggregate of, where applicable, the number of H Shares held by the Shareholders upon Listing and the A Shares held by the Shareholders 
(excluding Hong Kong Securities Clearing Company Limited and the Company's repurchase account) as of January 31, 2026, which is the latest shareholding of A Shares available 
to the Company.  
 
# 
Among the top 25 placees, certain placees are also existing Shareholders. To the best knowledge, information and belief of the Company after due enquiry, no allocation has been 
made to the Permitted Existing Shareholder holding more than 1% of the issued share capital of the Company immediately prior to the completion of the Global Offering. As the top 
25 placees who are also existing shareholders each held less than 1% of the issued share capital of the Company immediately prior to the completion of the Global Offering, the 
number of A Shares held by them are not counted into the number of Shares held upon Listing. 

<<<PAGE 17>>>
14 
 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 260,646 valid 
applications made by the public will be conditionally allocated on the basis set out below: 
APPROXIMATE 
PERCENTAGE ALLOTTED 
NO. OF SHARES 
NO. OF VALID 
OF THE TOTAL NO. OF 
APPLIED FOR 
APPLICATIONS 
BASIS OF ALLOTMENT / BALLOT 
SHARES APPLIED FOR 
POOL A 
100 
93,889 
4,694 out of 93,889 to receive 100 Shares 
5.00% 
200 
12,432 
746 out of 12,432 to receive 100 Shares 
3.00% 
300 
11,392 
854 out of 11,392 to receive 100 Shares 
2.50% 
400 
15,774 
1,199 out of 15,774 to receive 100 Shares 
1.90% 
500 
6,552 
531 out of 6,552 to receive 100 Shares 
1.62% 
600 
3,074 
277 out of 3,074 to receive 100 Shares 
1.50% 
700 
2,307 
226 out of 2,307 to receive 100 Shares 
1.40% 
800 
2,554 
266 out of 2,554 to receive 100 Shares 
1.30% 
900 
4,985 
538 out of 4,985 to receive 100 Shares 
1.20% 
1,000 
11,980 
1,318 out of 11,980 to receive 100 Shares 
1.10% 
1,500 
6,041 
906 out of 6,041 to receive 100 Shares 
1.00% 
2,000 
5,715 
1,029 out of 5,715 to receive 100 Shares 
0.90% 
2,500 
3,347 
669 out of 3,347 to receive 100 Shares 
0.80% 
3,000 
3,515 
717 out of 3,515 to receive 100 Shares 
0.68% 
3,500 
2,348 
493 out of 2,348 to receive 100 Shares 
0.60% 
4,000 
2,753 
607 out of 2,753 to receive 100 Shares 
0.55% 
4,500 
2,039 
450 out of 2,039 to receive 100 Shares 
0.49% 
5,000 
4,512 
1,015 out of 4,512 to receive 100 Shares 
0.45% 
6,000 
3,403 
858 out of 3,403 to receive 100 Shares 
0.42% 
7,000 
2,443 
650 out of 2,443 to receive 100 Shares 
0.38% 
8,000 
2,266 
634 out of 2,266 to receive 100 Shares 
0.35% 
9,000 
2,075 
598 out of 2,075 to receive 100 Shares 
0.32% 
10,000 
11,337 
3,401 out of 11,337 to receive 100 Shares 
0.30% 
20,000 
7,177 
3,589 out of 7,177 to receive 100 Shares 
0.25% 
30,000 
4,248 
2,931 out of 4,248 to receive 100 Shares 
0.23% 
40,000 
4,686 
3,749 out of 4,686 to receive 100 Shares 
0.20% 
232,844 
Total number of Pool A successful applicants: 32,945 
 
 

<<<PAGE 18>>>
15 
 
 
  
 
 
POOL B 
50,000 
9,619 
6,493 out of 9,619 to receive 100 Shares 
0.14% 
60,000 
3,234 
2,426 out of 3,234 to receive 100 Shares 
0.13% 
70,000 
2,033 
1,709 out of 2,033 to receive 100 Shares 
0.12% 
80,000 
1,489 
1,370 out of 1,489 to receive 100 Shares 
0.12% 
90,000 
1,225 
1,211 out of 1,225 to receive 100 Shares 
0.11% 
100,000 
5,020 
100 Shares 
0.10% 
200,000 
2,462 
100 Shares plus 1,967 out of  2,462 to receive 
additional 100 Shares 
0.09% 
300,000 
964 
200 Shares 
0.07% 
400,000 
532 
200 Shares plus 273 out of  532 to receive additional 
100 Shares 
0.06% 
500,000 
281 
300 Shares 
0.06% 
600,000 
157 
300 Shares plus 75 out of  157 to receive additional 
100 Shares 
0.06% 
700,000 
117 
400 Shares 
0.06% 
800,000 
86 
400 Shares plus 41 out of  86 to receive additional 100 
Shares 
0.06% 
900,000 
96 
500 Shares 
0.06% 
1,000,000 
194 
500 Shares plus 87 out of  194 to receive additional 
100 Shares 
0.05% 
1,500,000 
103 
800 Shares 
0.05% 
2,000,000 
64 
1,000 Shares 
0.05% 
2,500,000 
37 
1,200 Shares 
0.05% 
3,294,500 
89 
1,500 Shares 
0.05% 
27,802 
Total number of Pool B successful applicants: 23,411 

<<<PAGE 19>>>
16 
 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the designated 
nominee accounts have been remitted back to the accounts of all HKSCC participants. Investors should 
contact their relevant brokers for any inquiries. 

<<<PAGE 20>>>
17 
 
 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of which 
consent has been obtained, the Company has complied with the Listing Rules and guidance materials in 
relation to the placing, allotment and listing of the Company’s H Shares. 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the 
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by them 
was the same as the final Offer Price in addition to any brokerage, AFRC transaction levy, SFC transaction 
levy and Stock Exchange trading fee payable. 
OTHERS / ADDITIONAL INFORMATION 
Allocations of Offer Shares to the existing Shareholders and/or their close associates and 
Cornerstone Investors with a consent under Chapter 4.15 of the Guide for New Listing Applicants 
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 of the 
Guide for New Listing Applicants to permit the Company to allocate further Offer Shares in the 
International Offering to certain Cornerstone Investors, existing shareholder and their close associate, as 
placees, subject to the following conditions (“Allocation to Size-based Exemption Participants”): 
(a) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a total value 
of at least HK$1 billion; 
(b) 
the Offer Shares allocated to all existing Shareholders and their close associates (whether as 
cornerstone investors and/or as placees) as permitted under the Size-based Exemption (as defined 
in the Guide for New Listing Applicants) do not exceed 30% of the total number of the H Shares 
offered under the Global Offering; 
(c) 
the Allocation to Size-based Exemption Participants will not affect the Company’s ability to satisfy 
its public float requirement as prescribed by the Stock Exchange under the waiver from strict 
compliance with the requirements of Rule 8.08(1) and 19A.13A of the Listing Rules; 
(d) 
each Director and chief executive of the Company confirms that no securities have been allocated 
to them or their respective close associates under the Size-based Exemption; and 
(e) 
details of the allocation to existing Shareholders and/or their close associates and Cornerstone 
Investors under the Size-based Exemption will be disclosed in this announcement. 
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted by 
the Stock Exchange. 
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates and 
Cornerstone Investors, please refer to the section headed “Allotment Results Details – International 
Offering – Allotees with Waivers/Consents Obtained” in this announcement. 
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines 

<<<PAGE 21>>>
18 
 
 
Under the International Offering, certain Offer Shares were placed to connected clients of their connected 
distributors pursuant to the Placing Guidelines. Details of the placement to connected clients are set out 
below. The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, consents 
under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such Offer Shares in 
the International Offering to the connected clients. The allocation of Offer Shares to such connected clients 
is in compliance with all the conditions under the consent granted by the Stock Exchange. 

<<<PAGE 22>>>
 
 
Part A - Connected Clients holding the beneficial interest of the Offer Shares on a non-discretionary basis on behalf of independent third parties 
No. 
Connected 
Distributor 
Connected 
Client 
Relationship 
with the 
Connected 
Distributor 
Identities of 
the ultimate 
beneficial 
owners of 
the Offer 
Shares or, 
where 
applicable, 
details of the 
structured 
products 
under which 
the 
subscription 
by the 
Connected 
Client was 
made (e.g. 
OTC total 
return 
swaps) 
Whether 
the 
Connected 
Client is a 
collective 
investment 
scheme 
which is not 
authorised 
by the SFC 
or is 
expected to 
hold the 
Offer 
Shares on 
behalf of 
such 
scheme 
Number of Offer Shares 
allocated to the connected 
client 
Approximate 
Percentage of 
total number of 
Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised and no 
additional Shares 
are issued 
pursuant to the 
Share Incentive 
Plans) 
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
exercised and no 
additional Shares 
are issued 
pursuant to the 
Share Incentive 
Plans) 
1. 
China 
International 
Capital 
Corporation 
Hong Kong 
Securities 
Limited 
(CICCHKS)  
CICC FT (Note 
1) 
CICC FT is a 
member of the 
same group of 
CICCHKS.  
Please refer to 
Note (1).  
N  
Gaoyi Funds: 43,800 
0.06647% 
0.00361% 
Longrising Investors: 3,300 
0.00501% 
0.00027% 
Pinpoint Funds: 2,000 
0.00304% 
0.00016% 
Zhejiang Rongsheng: 300 
0.00046% 
0.00002% 
Qinchen Funds: 300 
0.00046% 
0.00002% 
2. 
Huatai 
Financial 
Holdings 
(Hong Kong) 
Limited 
(HTFH) 
HTCI 
(Note 2) 
HTCI is a 
member of the 
same group of 
HTFH. 
Please refer to 
Note (2).  
N 
Shanghai Qufeng: 361,100 
0.54803% 
0.02979% 
N 
Weining Funds: 300  
0.00046% 
0.00002% 
Shengquan Funds: 300 
0.00046% 
0.00002% 
Daohe Chengguang: 4,400 
0.00668% 
0.00036% 
Shanghai Greenwoods: 79,900 
0.12126% 
0.00659% 
Beijing Yuanfeng Private Equity 
Fund Management Partnership 
(Limited Partnership): 48,700 
0.07391%  
0.00402% 

<<<PAGE 23>>>
 
 
No. 
Connected 
Distributor 
Connected 
Client 
Relationship 
with the 
Connected 
Distributor 
Identities of 
the ultimate 
beneficial 
owners of 
the Offer 
Shares or, 
where 
applicable, 
details of the 
structured 
products 
under which 
the 
subscription 
by the 
Connected 
Client was 
made (e.g. 
OTC total 
return 
swaps) 
Whether 
the 
Connected 
Client is a 
collective 
investment 
scheme 
which is not 
authorised 
by the SFC 
or is 
expected to 
hold the 
Offer 
Shares on 
behalf of 
such 
scheme 
Number of Offer Shares 
allocated to the connected 
client 
Approximate 
Percentage of 
total number of 
Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised and no 
additional Shares 
are issued 
pursuant to the 
Share Incentive 
Plans) 
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
exercised and no 
additional Shares 
are issued 
pursuant to the 
Share Incentive 
Plans) 
3. 
CITIC 
Securities 
Brokerage 
(HK) 
Limited 
(CSB) 
CSICM 
(Note 3) 
CSICM is a 
member of the 
same group of 
CLSA. 
Please refer to 
Note (3). 
N 
300 
0.00046% 
0.00002% 
 
 

<<<PAGE 24>>>
 
 
Part B - Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties 
 
No. 
Connected 
Distributor 
Connected Client 
Relationship with 
the Connected 
Distributor 
Whether the 
Connected Client 
is a collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Number of Offer Shares 
allocated to the 
connected client 
Approximate 
Percentage of total 
number of Offer 
Shares (assuming 
the Over-allotment 
Option is not 
exercised and no 
additional Shares 
are issued 
pursuant to the 
Share Incentive 
Plans) 
Approximate percentage 
of total Shares in issue 
immediately following the 
completion of Global 
Offering (assuming the 
Over-allotment Option is 
not exercised and no 
additional Shares are 
issued pursuant to the 
Share Incentive Plans) 
1.  
Morgan Stanley 
Asia Limited 
(MSAL) 
MSIM 
(Note 4) 
MSIM and MSAL 
are members of the 
same group. 
N 
800 
0.00121% 
0.00007% 
2.  
UBS AG Hong 
Kong Branch 
(UBS AG HK) 
ICBC UBS 
(Note 5) 
 
UBS AG HK and 
ICBC UBS are 
members of the 
same group. 
N 
3,800 
0.00577% 
0.00031% 

<<<PAGE 25>>>
 
 
No. 
Connected 
Distributor 
Connected Client 
Relationship with 
the Connected 
Distributor 
Whether the 
Connected Client 
is a collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Number of Offer Shares 
allocated to the 
connected client 
Approximate 
Percentage of total 
number of Offer 
Shares (assuming 
the Over-allotment 
Option is not 
exercised and no 
additional Shares 
are issued 
pursuant to the 
Share Incentive 
Plans) 
Approximate percentage 
of total Shares in issue 
immediately following the 
completion of Global 
Offering (assuming the 
Over-allotment Option is 
not exercised and no 
additional Shares are 
issued pursuant to the 
Share Incentive Plans) 
3.  
UBS AG Hong 
Kong Branch 
(UBS AG HK) 
ICBC UBS International 
(Note 5) 
 
UBS AG HK and 
ICBC UBS 
International are 
members of the 
same group. 
N 
600 
0.00091% 
0.00005% 
4.  
UBS AG Hong 
Kong Branch 
(UBS AG HK) 
and UBS AG 
Singapore 
Branch (UBS 
AG SG) 
UBS AM 
(Note 6) 
UBS AG HK, 
UBS AG SG and 
UBS AM are 
members of the 
same group. 
N 
941,000 
1.42814% 
0.07762% 
5.  
Goldman Sachs 
(Asia) L.L.C. 
(GS) 
GSAM 
(Note 7) 
 
GSAM is a 
member of the 
same group of GS. 
N 
182,400 
0.27683% 
0.01505% 
6.  
CMB 
International 
Securities 
Limited 
(CMBI), China 
Merchants 
Bosera AM 
(Note 8) 
Bosera AM is a 
member of the 
same group of 
CMBI, CMS HK 
and CMBWL. 
N 
7,200 
0.01093% 
0.00059% 

<<<PAGE 26>>>
 
 
No. 
Connected 
Distributor 
Connected Client 
Relationship with 
the Connected 
Distributor 
Whether the 
Connected Client 
is a collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Number of Offer Shares 
allocated to the 
connected client 
Approximate 
Percentage of total 
number of Offer 
Shares (assuming 
the Over-allotment 
Option is not 
exercised and no 
additional Shares 
are issued 
pursuant to the 
Share Incentive 
Plans) 
Approximate percentage 
of total Shares in issue 
immediately following the 
completion of Global 
Offering (assuming the 
Over-allotment Option is 
not exercised and no 
additional Shares are 
issued pursuant to the 
Share Incentive Plans) 
Securities (HK) 
Co., Ltd 
(CMSHK) and 
CMB Wing 
Lung Bank 
Limited 
(CMBWL) 
7.  
CLSA Limited 
(CLSA) 
CITICS AM HK 
(Note 9) 
CITICS AM HK is 
a member of the 
same group of 
CLSA. 
N 
124,000 
0.18819% 
0.01023% 
8.  
CLSA 
China AMC HK 
(Note 10) 
China AMC HK is 
a member of the 
same group of 
CLSA. 
N 
36,500 
0.05540% 
0.00301% 
9.  
Guotai Junan 
Securities (Hong 
Kong) limited 
(GTJA 
Securities) 
GTJAI 
(Note 11) 
GTJAI is a 
member of the 
same group of 
GTJA Securities. 
N 
Shenzhen Bairuichen: 
1,094,200 
1.66065% 
0.09026% 
Shanghai Tongyi: 800 
0.00121% 
0.00007% 
Shanghai Minghong: 
36,500 
0.05540% 
0.00301% 

<<<PAGE 27>>>
 
 
No. 
Connected 
Distributor 
Connected Client 
Relationship with 
the Connected 
Distributor 
Whether the 
Connected Client 
is a collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Number of Offer Shares 
allocated to the 
connected client 
Approximate 
Percentage of total 
number of Offer 
Shares (assuming 
the Over-allotment 
Option is not 
exercised and no 
additional Shares 
are issued 
pursuant to the 
Share Incentive 
Plans) 
Approximate percentage 
of total Shares in issue 
immediately following the 
completion of Global 
Offering (assuming the 
Over-allotment Option is 
not exercised and no 
additional Shares are 
issued pursuant to the 
Share Incentive Plans) 
Shanghai Jiedi: 73,000 
0.11079% 
0.00602% 
10.  
Guotai Junan 
Securities (Hong 
Kong) limited 
(GTJA 
Securities) 
Fullgoal Fund 
(Note 12) 
Fullgoal HK, a 
wholly owned 
subsidiary of Full 
goal Fund, which 
is owned by 
Guotai Haitong 
Securities Co., 
Ltd. (SEHK: 2611) 
(“Guotai 
Haitong”) as to 
27.775%. 
GTJA is a 
subsidiary of 
Guotai Haitong. 
Therefore, each of 
Fullgoal Fund and 
Fullgaol HK is a 
member of the 
same group of 
GTJA Securities 
N 
45,000 
0.06830% 
0.00371% 
11.  
Guotai Junan 
Securities (Hong 
Kong) limited 
(GTJA 
Securities) 
Fullgoal HK 
(Note 13) 
 
N 
28,000 
0.0425% 
0.00231% 

<<<PAGE 28>>>
 
 
No. 
Connected 
Distributor 
Connected Client 
Relationship with 
the Connected 
Distributor 
Whether the 
Connected Client 
is a collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Number of Offer Shares 
allocated to the 
connected client 
Approximate 
Percentage of total 
number of Offer 
Shares (assuming 
the Over-allotment 
Option is not 
exercised and no 
additional Shares 
are issued 
pursuant to the 
Share Incentive 
Plans) 
Approximate percentage 
of total Shares in issue 
immediately following the 
completion of Global 
Offering (assuming the 
Over-allotment Option is 
not exercised and no 
additional Shares are 
issued pursuant to the 
Share Incentive Plans) 
12.  
Huatai Financial 
Holdings (Hong 
Kong) Limited  
(HTFH)  
China Southern 
(Note 14)  
China Southern is 
a member of the 
same group of 
HTFH.  
 
N  
36,500  
0.0554%  
0.0030%  
 
 

<<<PAGE 29>>>
 
 
       Notes: 
 
 
(1) CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one OTC swap transactions (the “OTC Swaps”) 
with each other and the ultimate clients (the “CICC FT Ultimate Clients”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis 
to hedge the OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed to the CICC FT Ultimate Clients, subject to customary 
fees and commissions. The OTC Swaps will be fully funded by the CICC FT Ultimate Clients. During the terms of the OTC Swaps, all economic returns of 
the Offer Shares subscribed by CICC FT will be passed to the CICC FT Ultimate Clients and all economic loss shall be borne by the CICC FT Ultimate Clients 
through the OTC Swaps, and CICC FT will not take part in any economic return or bear any economic loss in relation to the Offer Shares. The OTC Swaps are 
linked to the Offer Shares and the CICC FT Ultimate Clients may request CICC FT to redeem it at their own discretions, upon which CICC FT shall dispose 
of the Offer Shares and settle OTC Swaps in cash in accordance with the terms and conditions of the OTC Swap. Despite that CICC FT will hold the legal title 
of the Offer Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares during the terms of the OTC Swaps according to its 
internal policy. The CICC FT Ultimate Clients for purpose of this placee subscription include:  
 
i. 
高毅利伟精选唯实基金, 金太阳高毅国鹭1 号崇远基金, 高毅任昊长期价值朗润私募证券投资基金, 高毅国鹭信远私募证券投资基金, 高毅任
昊优选致福私募证券投资基金, 高毅庆瑞6 号瑞行基金, 高毅任昊臻选春和私募证券投资基金, 高毅庆瑞臻选沣源私募证券投资基金, 高毅任
昊精选承泽私募证券投资基金 (collectively, the "Gaoyi Funds"), which are managed by Perseverance Asset Management L.L.P. (上海高毅資產管
理合夥企業(有限合夥)) (“Gaoyi Asset Management”). No ultimate beneficial owner holds 30% or more interest in Gaoyi Funds or Gaoyi Asset 
Management; 
ii. 
源乐晟强树私募证券投资基金, 源乐晟晟世8 号私募证券投资基金 (collectively, "Longrising Investors"), which are managed by Tibet 
Yuanlesheng Asset Management Co., Ltd. (西藏源乐晟资产管理有限公司) ("Longrising"). The single ultimate beneficial owner holding 30% or more 
interest in all of YLongrising Investors and Longrising is Zeng Xiaojie (曾晓洁); 
iii. 
保银进取1 号基金, 保银多空稳健1 号基金, 保银多空稳健2 号基金 (collectively, "Pinpoint Funds"), which are managed by Shanghai Pinpoint 
Private Equity Fund Management Co., Ltd. (上海保银私募基金管理有限公司) ("Pinpoint Funds Investment"). No ultimate beneficial owner holds 
30% or more interest in Pinpoint Funds; The only ultimate beneficial owner holding 30% or more interest of Pinpoint Funds Investment is Li Mo (李
墨); 
iv. 
Zhejiang Rongsheng Holding Group Co., Ltd. (浙江荣盛控股集团有限公司)("Zhejiang Rongsheng"), whose single ultimate beneficial owner holding 
30% or more interest is Li Shuirong(李水荣); 
v. 
勤辰森裕1 号私募证券投资基金, 勤辰金选创赢1 号私募证券投资基金, 勤辰森裕3 号私募证券投资基金, 勤辰金选森裕1 号私募证券投资基
金, 勤辰嘉选森裕1 号私募证券投资基金 (collectively, "Qinchen Funds"), which are managed by Shanghai Qinchen Private Fund Management 
Partnership (Limited Partnership) (上海勤辰私募基金管理合伙企业（有限合伙）) (“Qinchen Fund Management”). No ultimate beneficial owner 
holds 30% or more interest in Qinchen Funds. The only ultimate beneficial owner holding 30% or more interest of Qinchen Fund Management is Yang 
Sen (杨森); 
 

<<<PAGE 30>>>
 
 
To the best of CICC FT’s knowledge having made all reasonable inquiries, each of the CICC FT Ultimate Clients is an independent third party of  all the 
underwriters and the companies which are members of the same group of companies as CICCHKS. 
 
The Overall Coordinators confirm that the Offer Shares to be placed to CICC FT are to be held on behalf of independent third parties. 
 
(2) PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public offerings ("IPOs") in Hong Kong. However, PRC 
investors are permitted to invest in products issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. In 
connection with such products, the licensed domestic securities firms, through their Hong Kong affiliates, may participate in Hong Kong IPOs either as placees 
or cornerstone investors (the "Cross-border Derivatives Trading Regime"). 
 
Huatai Securities Co., Ltd. ("Huatai Securities"), the shares of which are listed on both the Shanghai Stock Exchange (stock code: 601688) and the Stock 
Exchange (stock code: 6886), is one of the domestic securities firms licensed to undertake cross-border derivatives trading activities. Huatai Securities entered 
into an ISDA agreement (the "ISDA Agreement") with its indirectly wholly-owned subsidiary, HTCI, to set out the principal terms of any future total return 
swap between Huatai Securities and HTCI. 
 
Pursuant to the ISDA Agreement, HTCI, which intends to participate in the Global Offering as a placee, will hold the beneficial interest of the Offer Shares on 
a non-discretionary basis under a back-to-back total return swap (the "Back-to-back TRS") to be entered by HTCI in connection with a Client TRS (as defined 
below) placed by and fully funded (i.e. with no financing provided by HTCI) by the Huatai Ultimate Clients (as defined below), by which, HTCI will, subject 
to customary fees and commissions, pass the full economic exposure of the Offer Shares ultimately to the Huatai Ultimate Clients (as defined below), which in 
effect, HTCI will hold the beneficial interest of the Offer Shares on behalf of the Huatai Ultimate Clients (as defined below). HTFH and HTCI are indirectly 
wholly-owned subsidiaries of Huatai Securities. Accordingly, HTCI is considered as a "connected client" of HTFH pursuant to paragraph 1B(7) of the Placing 
Guidelines. 
 
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the "Huatai Ultimate Clients") cannot directly subscribe for the Offer Shares 
but may invest in derivative products issued by domestic securities firms licenced to undertake cross-border derivatives trading activities, such as Huatai 
Securities, with the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, the Huatai Ultimate Clients , through their 
respective investment managers (as applicable), will place a total return swap order (the "Client TRS") with Huatai Securities in connection with the Company's 
IPO and Huatai Securities will place a Back-to-back TRS order to HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the Back-
to-back TRS, HTCI participates in the Company's IPO and subscribes the Offer Shares through placing order with HTFH during the International Offering. 
The Huatai Ultimate Clients for purpose of this place subscription include: 
i. 
卫宁启航1 号私募证券投资基金 and 卫宁聚焦私募证券投资基金 (collectively, the "Weining Funds"), which are managed by Shanghai Weining 
Investment Management Co ,Ltd. (上海卫宁私募基金管理有限公司) (“Shanghai Weining”). Fu Chengcheng(付诚成) and Lin Ran (林然) each 
holds 30% or more interest in Shanghai Weining and Liu Yutao(刘育涛) holds 30% or more interest in Weining Funds;  
ii. 
Shanghai Qufeng International Trade Co.,Ltd. (上海渠丰国际贸易有限公司)("Shanghai Qufeng"), whose ultimate beneficial owners each holding 
30% or more interest including Yang Lu (杨璐) and Yang Zhenhua (杨震华);  

<<<PAGE 31>>>
 
 
iii. 
盛泉恒元多策略量化对冲1 号基金, 盛泉恒元量化套利专项48 号私募证券投资基金, 盛泉恒元多策略远见19 号私募证券投资基金, 盛泉恒
元灵活配置专项2 号私募证券投资基金, 盛泉恒元量化套利专项5 号私募证券投资基金, 盛泉恒元量化套利1 号专项私募证券投资基金, 盛
泉恒元量化套利专项46 号私募证券投资基金, 盛泉恒元量化套利专项29 号私募证券投资基金, 盛泉恒元量化套利专项84 号私募证券投资
基金, 盛泉恒元量化套利专项35 号私募证券投资基金 (collectively, the "Shengquan Funds"), which are managed by Nanjing Shengquan Hengyuan 
Investment Co., Ltd. (南京盛泉恒元投资有限公司). Zhao Zhongdong (赵忠东) holds 30% or more interest in Nanjing Shengquan Hengyuan 
Investment Co., Ltd. No one holds 30% or more interest in Shengquan Funds; 
iv. 
Daohe Chengguang Private Securities Investment Fund (道合承光私募证券投资基金)("Daohe Chengguang"), whose only ultimate beneficial owner 
holding 30% or more interest is Zhong Shanshan; 
v. 
Funds managed by Shanghai Greenwoods Asset Management Co., Ltd. (上海景林資產管理有限公司)("Shanghai Greenwoods"), whose ultimate 
beneficial owner is Jiang Jinzhi(蔣錦志); and 
vi. 
源峰泓聿私募证券投资基金, 源峰稳健私募证券投资基金, and 源峰价值私募证券投资基金, which are managed by Beijing Yuanfeng Private 
Equity Fund Management Partnership (Limited Partnership) (北京源峰私募基金管理合伙企业（有限合伙）). Yong Zhou (周勇) holds 30% or 
more interests in 源峰泓聿私募证券投资基金. 
 
To the best of knowledge of HTCI and after making all reasonable enquiries, each of the Huatai Ultimate Clients  is an independent third party of all the 
underwriters and the companies which are members of the same group of companies as HTFH. 
 
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in connection with the Client TRS order placed by the Huatai 
Ultimate Clients. Pursuant to the terms of the contracts of the Back-to-back TRS and the Client TRS, during the tenor of the Back-to-back TRS and the Client 
TRS, subject to customary fees and commissions, all economic returns of the Offer Shares will be ultimately passed to the Huatai Ultimate Clients  through the 
Back-to-back TRS and the Client TRS and all economic loss shall be ultimately borne by the Huatai Ultimate Clients . HTCI will not take any economic return 
or bear any economic loss in relation to the Offer Shares. 
 
Investment in the Back-to-back TRS and the Client TRS is similar to the investment in a qualified domestic institutional investor fund ("QDII") in the way that 
the Huatai Ultimate Clients  would reap all the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through the exchange 
rate exposure on both the notional value of the investment and the profit and loss of the investment. In contrast, the profit and loss of the Back-to-back TRS 
and the Client TRS factor into account the fluctuation in RMB exchange rate upon termination of the Client TRS by converting the profit and loss using the 
current exchange rate at the time of termination. As such, the Huatai Ultimate Clients  would bear the exchange rate exposure of the profit and loss on settlement 
date. 
 
The Huatai Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time from the issue date of the Client TRS which should 
be on or after the date on which the Offer Shares are listed on the Stock Exchange at their own discretion. Upon the termination upon maturity or early 
termination of the Client TRS by the Huatai Ultimate Clients , HTCI will dispose the Offer Shares on the secondary market and the Huatai Ultimate Clients  
will receive a final settlement amount in cash in accordance with the terms and conditions of the Back-to-back TRS and the Client TRS which should have 

<<<PAGE 32>>>
 
 
taken into account all the economic returns or economic loss in relation to the Offer Shares. If upon the maturity of the Client TRS, the Huatai Ultimate Clients 
intend to extend the investment period, subject to further agreement between Huatai Securities and the relevant Huatai Ultimate Clients, the term of the Client 
TRS could be extended by way of a new issuance or a tenor extension. Accordingly, Huatai Securities will extend the term of the Back-to-back TRS by way of 
a new issuance or a tenor extension. 
 
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through the economic exposure to the Huatai Ultimate 
Clients , each being an onshore client who places a Client TRS order with Huatai Securities in connection with the IPO of the Company. HTCI will not exercise 
the voting right of the Offer Shares during the tenor of the Back-to-back TRS. 
 
During the life of the Client TRS and Back-to-back TRS, HTCI may continue to hold the Offer Shares in its custodian account, or to hold some or all of the 
Offer Shares in a prime brokerage account for stock borrowing purposes, where HTCI will lend out its holding of underlying Offer Shares in the form of stock 
borrowing loans consistent with market practice to lower its finance costs, provided that HTCI has the ability to call back the Offer Shares on loan at any time 
in order to satisfy its obligations under the Back-to-back TRS to ensure the economic interests are ultimately passed to the Huatai Ultimate Clients . 
 
(3) CSICM will act as the single counterparty of a back-to-back total return swap transaction (the “CSICM Back-to-back TRS”) to be entered into by CSICM in 
connection with total return swap orders (the “CSICM Client TRS”) placed by its ultimate clients ("CSICM Ultimate Clients"), by which CSICM will hold 
the legal title and beneficial interest in the Offer Share, but will contractually agree to pass on the full economic exposure and return of the Offer Shares placed 
to the CSICM Ultimate Clients, on a non-discretionary basis. CSICM proposes to subscribe for and hold the Offer Shares as a placee under the International 
Offering on behalf of each of the CSICM Ultimate Clients, each being an independent third party, to the best of their knowledge and after making all reasonable 
enquiries, on a non-discretionary basis. The CSICM Ultimate Clients for purpose of this placee subscription include: 盤京賀想1 號私募證券投資基金 and 
盤京興和1 號私募證券投資基金 (collectively, the "Panjing Funds"), all managed by Shanghai Panjing Investment Management Center (Limited 
Partnership)(上海盤京投資管理中心（有限合夥）)("Panjing Investment Management"). No ultimate beneficial owner holds 30% or more interest in 
Panjing Funds. The only ultimate beneficial owner holding 30% or more interest of Panjing Investment Management is Zhuang Tao(庄涛). 
 
CSICM has confirmed that, to the best of their knowledge and after making all reasonable enquiries, each of the CSICM Ultimate Client and its ultimate 
beneficial owner is an independent third party of CSICM, CLSA and the companies which are members of the same group of companies as CLSA. 
 
(4) MSAL is a distributor of the Global Offering. MSIM will hold the Offer Shares in its capacity on behalf of its underlying clients, which are independent third 
parties. There is no ultimate beneficial owner holding 30% interest or more in such underlying client. 
 
(5) ICBC UBS and ICBC UBS International will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their 
investors (the “ICBC UBS Ultimate Clients”), each of which is an independent third party. None of the ICBC UBS Ultimate Clients holds more than 30% 
ultimate beneficial interest in the relevant funds. ICBC UBS and ICBC UBS International have confirmed that, to the best of their knowledge, each of the ICBC 
UBS Ultimate Clients is an independent third party of ICBC UBS, ICBC UBS International, UBS AG HK and the companies which are members of the same 
group of companies as UBS AG HK.  

<<<PAGE 33>>>
 
 
 
 
(6) UBS AG Hong Kong Branch (“UBS AG HK”) is an Overall Coordinator, Joint Global Coordinator, Joint Bookrunner, Joint Lead Manager and Capital Market 
Intermediary in connection with the Global Offering. UBS Securities Hong Kong Limited is one of the Joint Sponsors in connection with the Global Offering. 
UBS AG HK, the global wealth management division of UBS AG Singapore Branch (“UBS AG SG”) and the global wealth management division of UBS AG 
Hong Kong Branch (“UBS HK WM”) are each a connected distributor. Subject to the written consent of the Stock Exchange, UBS Asset Management 
(Singapore) Ltd. (“UBS AM”) proposes to participate as placee to subscribe for the Offer Shares for and on behalf of its underlying client under the International 
Offering. UBS AM is a wholly owned subsidiary of UBS Asset Management, an investment management company, which is wholly ultimately owned by UBS 
Group AG, which is a company organized under Swiss law as a corporation that has issued shares of common stock to investors. UBS Group AG’s shares are 
listed on the SIX Swiss Exchange (stock code: UBSG) and the New York Stock Exchange (stock code: UBS). UBS AM is a member of the same group of 
companies as UBS HK, UBS SG WM and UBS HK WM are members of the same group of companies. As a result, UBS AM is a connected client of UBS HK, 
UBS SG WM and UBS HK WM for the purpose of paragraph 1B(7) of the Placing Guidelines. UBS AM will hold the Offer Shares in its capacity as 
discretionary investment manager managing assets on behalf of its underlying client. The subscription will be fully funded by the personal assets of the 
underlying client. 
 
(7) GSAM will hold the Offer Shares in its capacity as the discretionary fund manager on behalf of its underlying clients, which are independent third parties. 
There is no ultimate beneficial owner holding 30% interest or more in such underlying client.  
 
(8) Each of CMBI and CMS HK is distributor of the Global Offering. Bosera AM intends to subscribe and hold the Offer Shares in its capacity as the discretionary 
fund manager on behalf of its sub-funds, which are all independent third parties. Each of the sub-funds and their respective ultimate beneficial owner holding 
30% or more interest is an independent third party of all the underwriters, and the companies which are members of the same group of companies as each of 
CMBI and CMS HK. 
 
(9) CITICS AM HK will hold the Offer Shares in accounts as the investment manager managing assets on behalf of its underlying client Wander Rise Assets Pte. 
Ltd. (the "CITICS AM HK Client").  To the best knowledge of CITICS AM HK, the ultimate beneficial owner of CITICS AM HK Client is SUN Shigen.  
 
CITICS AM HK has confirmed that, to the best of their knowledge and after making all reasonable enquiries, each of the CITICS AM HK Client and its ultimate 
beneficial owners holding 30% or more therein listed above is an independent third party of all the underwriters and the companies which are members of the 
same group of companies as CLSA.  
 
(10) 
China AMC HK will hold the Offer Shares as the discretionary fund manager managing on behalf of its underlying clients, each of which is an 
independent third party. The underlying clients are as follows: 
 
i. 
CHINAAMC SELECT GREATER CHINA TECHNOLOGY FUND ("CHINAAMC FUND"). The ultimate beneficial owners holding 30% or more 
interest of it is Futu Securities International (Hong Kong) Limited; 
ii. 
CHINAAMC FUND - CHINAAMC CHINA OPPORTUNITIES FUND, who confirms no others investor hold 30% or more interest in the same fund; 

<<<PAGE 34>>>
 
 
iii. 
CHINAAMC CHINA FOCUS FUND The ultimate beneficial owners holding 30% or more interest of it is Manulife (International) Limited;  
iv. 
CHINAAMC CHINA GROWTH FUND (SICAV).The ultimate beneficial owners holding 30% or more interest of it is Yuanta Securities (HK) 
Company LTD; 
v. 
HKCINDAM who is 100% hold by China Cinda (HK) Asset Management CO., LTD. 
 
To the best knowledge of China AMC HK after making all reasonable enquiries, (i) each of the China AMC HK Ultimate Clients is an independent third party 
of the Company, the Company’s subsidiaries and substantial shareholders, CLSA, China AMC HK and the companies which are members of the same group 
of companies as CLSA; and (ii) China AMC HK is not a collective investment scheme which is not authorized by the SFC. 
 
(11) 
it is proposed that Guotai Junan Investments (Hong Kong) Limited (“GTJAI”) participates as placee to subscribe for the Offer Shares under the 
International Offering (the “GTJAI Subscription”). GTJAI is a member of the same group of companies as Guotai Junan Securities (Hong Kong) Limited 
("GTJAS") and is considered as a connected client of GTJAS pursuant to paragraph 1B(7) of the Placing Guidelines. In relation to the GTJAI Subscription, 
GTJA Investment shall hold the Offer Shares for hedging purpose as the single underlying asset of several sets of back-to-back total return swap transaction 
(the “GTHT Back-to-back TRS”) to be entered into between GTJAI and Guotai Haitong Securities Co., Ltd. (the “GTHT Onshore Parent”) in connection 
with several total return swap orders (the “GTHT Client TRS”) to be entered into by GTHT Onshore Parent and several ultimate clients (the “GTHT Onshore 
Ultimate Client”), respectively. Such GTHT Client TRS is to be fully funded by the GTHT Onshore Ultimate Client. GTJAI will hold the Offer Shares on a 
non-discretionary basis for the purpose of hedging the economic exposure under the GTHT Back-to-back TRS and GTHT Client TRS only. During the tenor 
of the GTHT Client TRS, all economic returns of the Offer Shares will be passed to the GTHT Onshore Ultimate Clients and all economic losses shall be borne 
by the GTHT Onshore Ultimate Client, subject to the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS, and GTJAI will not take 
part in any economic return or bear any economic loss in relation to the price of the Offer Shares. The GTHT Onshore Ultimate Client may request to redeem 
the Offer Shares at their own discretion, upon which GTJAI shall dispose of the Offer Shares and settle the GTHT Back-to-back TRS and GTHT Client TRS 
in cash in accordance with the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS documents. Due to its internal policy, GTJAI will 
not exercise the voting right attaching to the Offer Shares during the tenor of the GTHT Back-to-back TRS and GTHT Client TRS. 
 
To the best knowledge, information and belief of GTJA Investments after due enquiry, the GTJA Onshore Ultimate Clients and their respective ultimate 
beneficial owners holding 30% or more interest include:  
i. 
Shenzhen Bairuichen Culture Development Co., Ltd.（深圳市百瑞辰文化发展有限公司）("Shenzhen Bairuichen")，whose single ultimate 
beneficial owner holding 30% or more interest is Zhang Wei (张伟); 
ii. 
Shanghai Tongyi Investment Management Co., Ltd. (上海通怡投资管理有限公司)("Shanghai Tongyi"). No single ultimate beneficial owner holding 
30% or more interest in Shanghai Tongyi; 
iii. 
Shanghai Minghong Investment Management Co.,Ltd-Minghong No. 1 Multi-strategy Hedging Fund ("上海明汯投资管理有限公司-明汯多策略对
冲1号基金") ("Shanghai Minghong"). No single ultimate beneficial owner holding 30% or more interest in Shanghai Minghong; 
iv. 
Jedi Asset Management, LLC-Jedi Yuanyang No.6 Private Securities Investment Fund (上海金澹资产管理有限公司-金澹远洋6号私募证券投资基
金) ("Shanghai Jiedi"), which is managed by Jedi Asset Management, LLC (上海金澹资产管理有限公司)("Jiedi AM"). The single ultimate 
beneficial owner holding 30% or more interest in all of Shanghai Jiedi is Ding Hai(丁海); 
 

<<<PAGE 35>>>
 
 
 
(12) 
Fullgoal Fund will hold the Offer Shares in its capacity as the discretionary fund manager on behalf of its investors, each of which is an independent 
third party of the Company, its subsidiaries, its substantial Shareholders, Fullgoal Fund Management Co., Ltd., GTJA, HTI and the companies which are 
members of the same group of GTJA and HTI.  
 
(13) 
Fullgoal HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their underlying investors, 
each of which is an independent third party of the Company, its subsidiaries, its substantial shareholders. 
 
(14) 
China Southern, a qualified domestic institutional investor as approved by the relevant PRC authority to conduct asset management business, will hold 
the Offer Shares as the independent agent and discretionary manager of certain QDII funds. China Southern has confirmed that, to the best of their knowledge, 
each of such underlying clients are independent third parties of all the underwriters and the companies which are members of the same group of companies as 
HTFH.  
 
 
 
 

<<<PAGE 36>>>
33 
 
 
 
DISCLAIMERS 
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong Kong 
Securities Clearing Company Limited take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability whatsoever for any 
loss howsoever arising from or in reliance upon the whole or any part of the contents of this announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for 
securities in the United States. The securities mentioned herein have not been, and will not be, registered under 
the United States Securities Act of 1933, as amended (the “U.S. Securities Act"). The securities may not be 
offered or sold in the United States except pursuant to an exemption from the registration requirements of the 
U.S. Securities Act and in compliance with any applicable state securities laws, or outside the United States 
unless in compliance with Regulation S under the U.S. Securities Act. There will be no public offer of securities 
in the United States. 
The Offer Shares are being offered and sold solely (1) to qualified institutional buyers as defined in Rule 144A 
under the U.S. Securities Act pursuant to an exemption from registration under the U.S. Securities Act and (2) 
outside the United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act.  
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. This announcement is not a prospectus. Potential investors should read 
the Prospectus dated January 30, 2026 issued by Montage Technology Co, Ltd. for detailed information 
about the Global Offering described below before deciding whether or not to invest in the H Shares thereby 
being offered. 
*Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators 
(for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations 
under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the 
events set out in the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong 
Kong Public Offering –Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong 
time) on the Listing Date (which is currently expected to be on February 9, 2026). 

<<<PAGE 37>>>
 
 
PUBLIC FLOAT AND FREE FLOAT 
Immediately after the completion of the Global Offering (before any exercise of the 
Overallotment Option), a total number of 4,361,066 A Shares, representing approximately 
0.36% of our Company’s total issued Shares, held by Dr. Howard C. Yang, Mr. Stephen Tai and 
Ms. Fang Zhoujie will not be considered as part of the public float since they will be considered 
as our Company’s core connected persons (as defined under the Listing Rules). 
Rule 8.08(1) (as amended and replaced by Rule 19A.13A) of the Listing Rules provides that, 
where a new applicant is a PRC issuer with other listed shares at the time of listing, this will 
normally mean that the portion of H shares for which listing is sought that are held by the public, 
at the time of listing, must (a) represent at least 10% of the issuer’s total number of issued shares 
in the class to which H shares belong (excluding treasury shares); or (b) have an expected market 
value of not less than HK$3,000,000,000. It is expected that upon Listing (assuming the Over-
allotment Option is not exercised and no additional Shares are issued pursuant to the Employee 
Incentive Plans), based on the Offer Price of HK$106.89 per H Share, the market value of the 
H Shares that are held by the public is approximately HK$7,042.98 million, which is higher than 
the prescribed market value of the H Shares required to be held by the public of HK$3 billion 
under Rule 19A.13A(2) of the Listing Rules, thereby satisfying Rule 8.08(1) (as amended and 
replaced by Rule 19A.13A) of the Listing Rules. 
 
Rule 8.08A (as amended and replaced by Rule 19A.13C) of the Listing Rules provides that, 
where a new applicant is a PRC issuer with other listed shares at the time of listing, this will 
normally mean that the portion of H shares for which listing is sought that are held by the public 
and not subject to any disposal restrictions (whether under contract, the Listing Rules, applicable 
laws or otherwise), at the time of listing, must: (a) represent at least 5% of the total number of 
issued shares in the class to which H shares belong at the time of listing (excluding treasury 
shares), with an expected market value at the time of listing of not less than HK$50,000,000; or 
(b) have an expected market value at the time of listing of not less than HK$600,000,000. The 
Company will satisfy the free float requirement under Rule 8.08A (as amended and replaced by 
Rule 19A.13C) of the Listing Rules. 
COMMENCEMENT OF DEALINGS 
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Monday, 
February 9, 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus has not been exercised. Investors who trade the H Shares on the basis of publicly 
available allocation details prior to the receipt of H Share certificates or prior to the H Share 
certificates becoming valid evidence of title do so entirely at their own risk. 
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Monday, 
February 9, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Monday, February 9, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 100 H Shares each, and the stock code of the H Shares will 
be 6809. 

<<<PAGE 38>>>
 
 
By order of the Board 
Montage Technology Co., Ltd. 
Howard C. Yang 
Chairman of the Board, executive Director, and 
Chief Executive Officer 
Hong Kong, February 6, 2026 
Directors of the Company named in the application to which this announcement relates are: (i) 
Dr. Howard C. Yang and Mr. Stephen Kuong-Io Tai as executive directors; (ii) Dr. Wang Rui and 
Ms. Fang Zhoujie as non-executive directors and (iii) Dr. Li Ruoshan, Professor Ko Ping Keung 
(appointment effective from the Listing Date), Dr. Yuhua Cheng and Dr. Shan Hailing as 
independent non-executive directors. 
 
