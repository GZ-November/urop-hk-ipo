# 配发结果公告抽取任务：2513.HK Knowledge Atlas Technology Joint Stock Company Limited - H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**07/01/2026 21:57**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0107/2026010701798.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2513.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) and Hong 
Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those defined 
in the prospectus dated December 30, 2025 (the “Prospectus”) issued by Knowledge Atlas Technology Joint Stock Company 
Limited (北京智譜華章科技股份有限公司) (the “Company”).
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
are being offered and sold outside the United States to persons that are not, and are not acting for the account or benefit of, 
U.S. persons or United States person as defined in 31 CFR Part 850.229, the final rule that implements Executive Order 14105 
and became effective in January 2025 (“U.S. Investor”), in offshore transactions in reliance on Regulation S under the U.S. 
Securities Act.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out in the 
Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not resident in Hong 
Kong and/or U.S. Investors. Potential investors of the Offer Shares should note that the Sole Sponsor and the Sponsor-Overall 
Coordinator (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under 
the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section 
headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” 
in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited, as stabilizing 
manager (the “Stabilizing Manager”) (or any person acting for it), on behalf of the Underwriters, may over-allocate or effect 
transactions with a view to stabilizing or supporting the market price of the H Shares at a level higher than that which might 
otherwise prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing Manager (or any 
person acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will be conducted at the absolute 
discretion of the Stabilizing Manager (or any person acting for it) and in what the Stabilizing Manager reasonably regards as 
the best interest of the Company, (b) may be discontinued at any time and (c) is required to be brought to an end within 30 days 
after the last day for lodging applications under the Hong Kong Public Offering (which is Wednesday, February 4, 2026). Such 
stabilizing action, if taken, may be effected in all jurisdictions where it is permissible to do so, in each case in compliance with all 
applicable laws, rules and regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W 
of the Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong 
Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for longer than the 
stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day after the last day for lodging 
applications under the Hong Kong Public Offering (which is Wednesday, February 4, 2026). After this date, when no further 
stabilizing action may be taken, demand for the H Shares, and therefore the price of the H Shares, could fall.

<<<PAGE 2>>>
2
Knowledge Atlas Technology Joint Stock Company Limited
北京智譜華章科技股份有限公司
(A joint stock company established in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the 
Global Offering
:
37,419,500 H Shares (subject to the 
  Over-allotment Option)
Number of Hong Kong Offer Shares
:
7,483,900 H Shares (as adjusted after 
  reallocation)
Number of International Offer Shares
:
29,935,600 H Shares (as adjusted after 
  reallocation and subject to the 
  Over-allotment Option)
Offer Price
:
HK$116.20 per H Share, plus brokerage of 
  1.0%, SFC transaction levy of 0.0027%, 
  AFRC transaction levy of 0.00015% and 
  Hong Kong Stock Exchange trading fee of 
  0.00565% (payable in full on application 
  in Hong Kong dollars and subject to 
  refund)
Nominal value
:
RMB0.10 per H Share
Stock code
:
2513
Sole Sponsor, Sponsor-Overall Coordinator, Overall Coordinator, Joint Global Coordinator, 
Joint Bookrunner and Joint Lead Manager
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
KNOWLEDGE ATLAS TECHNOLOGY JOINT STOCK COMPANY LIMITED
北京智譜華章科技股份有限公司
ANNOUNCEMENT OF OFFER PRICE AND
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated December 30, 2025 (the “Prospectus”) issued by 
Knowledge Atlas Technology Joint Stock Company Limited (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code 
2513
Stock short name
KNOWLEDGE ATLAS
Dealings commencement date 
January 8, 2026*
*  see note at the end of the announcement
Price Information
Offer Price 
HK$116.20
Offer Shares and Share Capital
Number of Offer Shares before exercise of the Over-allotment 
Option
37,419,500
Final number of Offer Shares in Public Offer (after reallocation)
7,483,900
Final number of offer shares in International Offer (after 
reallocation)
29,935,600
Number of issued shares upon Listing before exercise of the Over-
allotment Option
440,230,190

<<<PAGE 4>>>
4
Over-allocation
No. of Offer Shares over-allocated 
5,612,900
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$4,348.1 million
Less: Estimated listing expenses payable based on Offer Price 
HK$ (174.7) million
Net proceeds 
HK$4,173.4 million
Note:	 Gross proceeds refers to the amount to which the issuer is entitled receive. For details of the use of proceeds, please 
refer to the Prospectus dated December 30, 2025. The Company will adjust the allocation of the net proceeds from the 
exercise of the Over-allotment Option (if any) for the purposes as set out in the section headed “Future Plans and Use 
of Proceeds” of the Prospectus on a pro rata basis.
ALLOTMENT RESULTS DETAILS
PUBLIC OFFER
No. of valid applications 
204,871
No. of successful applications 
50,907
Subscription level 
1,159.46 times
Claw-back triggered 
Yes
No. of Offer Shares initially available under the Public Offer 
1,871,000
Final no. of Offer Shares under the Public Offer (after reallocation) 7,483,900
% of Offer Shares under the Public Offer to the Global Offering
20.00%
Note:	 For details of the final allocation of shares to the Public Offer, investors can refer to www.hkeipo.hk/IPOResult to perform 
a search by name or identification number or www.hkeipo.hk/IPOResult for the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFER
No. of placees 
221
Subscription Level 
15.28 times
No. of Offer Shares initially available under the International Offer 35,548,500
Final no. of Offer Shares under the International Offer (after 
reallocation)
29,935,600
% of Offer Shares under the International Offer to the Global 
Offering
80.00%
The Directors confirm that, to the best of their knowledge, information and belief, save for waivers 
under Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of Appendix F1 to the 
Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange to permit the Company to 
allocate certain Offer Shares in the International Offering to certain existing minority shareholders 
and/or their close associates as cornerstone investors or placees, (i) none of the Offer Shares 
subscribed by the placees and the public have been financed directly or indirectly by the Company, 
any of the Directors, chief executive of the Company, controlling shareholders, substantial 
shareholders, existing shareholders of the Company or any of its subsidiaries or their respective 
close associates; and (ii) none of the placees and the public who have purchased the Offer Shares 
are accustomed to taking instructions from the Company, any of the Directors, chief executive 
of the Company, controlling shareholders, substantial shareholders, existing shareholders of the 
Company or any of its subsidiaries or their respective close associates in relation to the acquisition, 
disposal, voting or other disposition of Shares registered in his/her/its name or otherwise held by 
him/her/it.

<<<PAGE 6>>>
6
PREFERENTIAL OFFERINGS
The placees in the International Offer include the following:
Cornerstone Investors
Investor
No. of
Offer
Shares
allocated
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option 
is not 
exercised)
% of total 
issued H 
Shares after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option 
is not 
exercised)
% of total 
issued share 
capital after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option 
is not 
exercised)
Existing 
shareholders 
or their close 
associates
JSC International 
Investment Fund 
SPC (acting for and 
on behalf of Qizhi 
SP)
11,985,900 
32.03%
5.56%
2.72%
Yes
JinYi Capital Multi-
Strategy Fund SPC 
Ltd. (acting for 
and on behalf of 
Structured Credit SP 
Fund)
468,700 
1.25%
0.22%
0.11%
Yes
Perseverance Asset 
Management
1,941,800 
5.19%
0.90%
0.44%
No
Shanghai Gaoyi 
and CICC Financial 
Trading Limited 
(in connection with 
Gaoyi OTC Swaps)
602,600 
1.61%
0.28%
0.14%
No
WT Asset 
Management
3,006,500 
8.03%
1.39%
0.68%
No
Taikang Life
2,008,800 
5.37%
0.93%
0.46%
No
GF Fund
2,812,300 
7.52%
1.30%
0.64%
No
3W Fund
1,205,200 
3.22%
0.56%
0.27%
No

<<<PAGE 7>>>
7
Investor
No. of
Offer
Shares
allocated
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option 
is not 
exercised)
% of total 
issued H 
Shares after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option 
is not 
exercised)
% of total 
issued share 
capital after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option 
is not 
exercised)
Existing 
shareholders 
or their close 
associates
RIME
645,400 
1.72%
0.30%
0.15%
No
Optimas Capital 
Limited
669,600 
1.79%
0.31%
0.15%
No
Luster LightTech 
International 
Limited
334,800 
0.89%
0.16%
0.08%
Yes
Total
25,681,600 
68.63%
11.91%
5.83%
Allottees who are customer(s) or client(s)/supplier(s) of the issuer
Investor
No. of Offer 
Shares 
allocated
% of offer 
shares
(assuming 
the Over-
allotment
Option is 
not
exercised)
% of total 
issued H 
Shares after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option 
is not 
exercised)
% of total 
issued share 
capital after 
the Global 
Offering
(assuming 
the Over-
allotment
Option is 
not
exercised)
Relationship
Luster LightTech 
International 
Limited
334,800 
0.89%
0.16%
0.08%
customer of the 
issuer
Total
334,800 
0.89%
0.16%
0.08%

<<<PAGE 8>>>
8
Allottees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares 
allocated
% of offer 
shares
(assuming 
the Over-
allotment
Option 
is not 
exercised)
% of total 
issued H 
Shares after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option 
is not 
exercised)
% of total 
issued share 
capital after 
the Global 
Offering
(assuming 
the Over-
allotment
Option 
is not 
exercised)
Relationship
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent 
under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares 
by existing minority shareholders and/or its close associates as cornerstone investors and 
placeesNote 1
Cornerstone investors
JSC International 
Investment Fund 
SPC (acting for and 
on behalf of Qizhi 
SP)
11,985,900 
32.03%
5.56%
2.72%
A cornerstone 
investor and a 
close associate 
of an existing 
minority 
shareholder
JinYi Capital Multi-
Strategy Fund SPC 
Ltd. (acting for 
and on behalf of 
Structured Credit SP 
Fund)
468,700 
1.25%
0.22%
0.11%
A cornerstone 
investor and a 
close associate 
of an existing 
minority 
shareholder
Luster LightTech 
International 
Limited
334,800 
0.89%
0.16%
0.08%
A cornerstone 
investor and a 
close associate 
of an existing 
minority 
shareholder
Placee
Huatai Capital 
Investment Limited 
(in connection 
with HTCI TRS 
with Zhongke 
Chuangxing 
Technology 
Investment Co., Ltd. 
(中科創星科技投資
有限公司))
28,400
0.08%
0.01%
0.01%
A placee, a 
close associate 
of an existing 
minority 
shareholder and 
a connected 
client

<<<PAGE 9>>>
9
Investor
No. of Offer 
Shares 
allocated
% of offer 
shares
(assuming 
the Over-
allotment
Option 
is not 
exercised)
% of total 
issued H 
Shares after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option 
is not 
exercised)
% of total 
issued share 
capital after 
the Global 
Offering
(assuming 
the Over-
allotment
Option 
is not 
exercised)
Relationship
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations to connected clientsNote 2
CICC FT (in 
connection with 
Gaoyi OTC Swaps 
and the CICCFT 
OTC Swaps)
602,600
1.61%
0.28%
0.14%
Cornerstone 
investor and 
connected 
client (in 
connection 
with Gaoyi 
OTC Swaps)
92,300
0.25%
0.04%
0.02%
Connected 
client (in 
connection 
with the 
CICCFT OTC 
Swaps)
Huatai Capital 
Investment Limited 
(in connection with 
HTCI TRSs with 
Huatai Onshore 
Ultimate Clients 
and Huatai Offshore 
Ultimate Client)
147,600
0.39%
0.07%
0.03%
Connected 
client (for and 
on behalf of 
Huatai Onshore 
Ultimate 
Clients)
18,900
0.05%
0.01%
0.004%
Connected 
client (for 
and on behalf 
of Huatai 
Offshore 
Ultimate 
Client)
Guotai Junan 
Investments
(Hong Kong) 
Limited (in 
connection with 
GTJAI TRSs with 
GTHT Onshore 
Underlying Clients)
88,700
0.24%
0.04%
0.02%
Connected 
client

<<<PAGE 10>>>
10
Investor
No. of Offer 
Shares 
allocated
% of offer 
shares
(assuming 
the Over-
allotment
Option 
is not 
exercised)
% of total 
issued H 
Shares after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option 
is not 
exercised)
% of total 
issued share 
capital after 
the Global 
Offering
(assuming 
the Over-
allotment
Option 
is not 
exercised)
Relationship
Bosera Asset 
Management 
(International) Co., 
Limited
13,400
0.04%
0.01%
0.003%
Connected 
client
Fullgoal Fund 
Management Co., 
Ltd and Fullgoal 
Asset Management 
(HK) Limited 
66,900
0.18%
0.03%
0.02%
Connected 
client
Haitong 
International Asset 
Management (HK) 
Limited
6,600
0.02%
0.003%
0.001%
Connected 
client
China Asset 
Management
(Hong Kong) 
Limited 
6,600
0.02%
0.003%
0.001%
Connected 
client
China Asset 
Management Co., 
Ltd.
66,900
0.18%
0.03%
0.02%
Connected 
client
BOCOM 
International Asset 
Management 
Limited
18,900
0.05%
0.01%
0.004%
Connected 
client
Notes:
(1)	
See “Waivers from Strict Compliance with the Requirements under the Listing Rules — Waiver Under Rule 10.04 and 
Consent Under Paragraph 1C(2) of Appendix F1 to the Listing Rules in Respect of Subscriptions of Offer Shares by 
Close Associates of Existing Shareholders as Cornerstone Investors” of the Prospectus and the section headed “Others/
Additional Information — Placing to existing shareholders and/or its close associates with a prior waiver under Rule 
10.04 and consent under paragraph 1C(1) of the Placing Guidelines” in this announcement for further details.
(2)	
The H Shares placed to such allottees are held on behalf of independent third parties (as defined in Chapter 4.15 of the 
Guide for New Listing Applicants, and are in compliance with all the conditions under the consent granted by the Stock 
Exchange. For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients, please refer to the section headed “Others/
Additional Information — Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines” in this announcement.

<<<PAGE 11>>>
11
LOCK-UP UNDERTAKINGS
Key Persons (as defined under Rule 18C.14 of the Listing Rules)
Name
Capacity
Number of 
shares held in the 
Company subject 
to lock-up 
undertakings 
upon listing
Number of H 
shares held in the 
Company subject 
to lock-up 
undertakings 
upon listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock–up 
undertakings 
upon Listing
Note 1
% of 
shareholding in 
the Company 
subject to 
lock–up 
undertakings 
upon Listing
Note 1
Last day subject 
to the lock up 
undertakings
Note 2
Dr. Liu
Co-founder, 
executive Director 
and chairman of 
the Board
925,150
—
—
0.21%
January 7, 2027
Beijing Lianpai
Note 3
Shareholding Plat 
form controlled 
by Dr. Liu
34,038,390
—
—
7.73%
January 7, 2027
Huihui
Note 4
Employee 
Incentive 
Platform 
controlled by Dr. 
Liu
39,482,710
5,922,407
2.75%
8.97%
January 7, 2027
Zhideng
Note 5
Employee 
Incentive 
Platform 
controlled by Dr. 
Liu
27,196,330
4,079,450
1.89%
6.18%
January 7, 2027
Dr. Tang
Co-founder
26,835,330
—
—
6.10%
January 7, 2027
Dr. Li
Co-founder and 
non-executive 
Director
3,367,760
—
—
0.76%
January 7, 2027
Dr. Xu
Co-founder
799,040
—
—
0.18%
January 7, 2027
Dr. Zhang
Co-founder and 
executive Director
399,520
—
—
0.09%
January 7, 2027
Wang Shaolan
Note 3
Co-founder and 
deputy general 
manager
—
—
—
—
January 7, 2027
Yan Xingyu
Note 4
Key R&D 
member
—
—
—
—
January 7, 2027

<<<PAGE 12>>>
12
Name
Capacity
Number of 
shares held in the 
Company subject 
to lock-up 
undertakings 
upon listing
Number of H 
shares held in the 
Company subject 
to lock-up 
undertakings 
upon listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock–up 
undertakings 
upon Listing
Note 1
% of 
shareholding in 
the Company 
subject to 
lock–up 
undertakings 
upon Listing
Note 1
Last day subject 
to the lock up 
undertakings
Note 2
Gu Xiaotao
Note 4
Key R&D 
member
—
—
—
—
January 7, 2027
Zhang Bo
Note 3
Key R&D 
member
—
—
—
—
January 7, 2027
Du Zhengxiao
Note 4
Key R&D 
member
—
—
—
—
January 7, 2027
Subtotal
133,044,230
10,001,857
4.64%
30.22%
Notes:
(1)	
Assuming the Over-allotment Option is not exercised.
(2)	
The lock-up period commencing on the date by reference to which disclosure of its shareholding is made in the 
Prospectus and ending on the date which is 12 months from the Listing Date, i.e. January 7, 2027.
(3)	
As of the date of this announcement, Mr. Wang Shaolan (a co-founder) and Zhang Bo (張鈸) (our chief scientist) are 
limited partners of Beijing Lianpai and shall be subject to disposal restrictions pursuant to Rule 18C.14 of the Listing 
Rules.
(4)	
As of the date of this announcement, Huihui and Zhideng were established as the Employee Ownership Platforms of 
the Group, under which the eligible participants (including the executive Directors, Dr. Liu, Dr. Zhang and Ms. Zhang 
Xiaohan as well as other core R&D employees of the Group) were awarded partnership interest in the Employee 
Ownership Platforms. The core R&D employees for the purpose of Rule 18C.14 of the Listing Rules include the 
followings:
•	
Mr. Yan Xingyu, an algorithm expert;
•	
Dr. Gu Xiaotao, an algorithm expert; and
•	
Dr. Du Zhengxiao, an algorithm expert.
See “History, Development and Corporate Structure — Employee Ownership Platforms” in the Prospectus for further 
details. All the above executive Directors, senior management members and key persons of the Company shall be subject 
to disposal restrictions pursuant to Rule 18C.14 of the Listing Rules.

<<<PAGE 13>>>
13
Pathfinder SIIs
Name
Capacity
Number of 
shares held in the 
Company subject 
to lock-up 
undertakings 
upon listing
Number of H 
shares held in the 
Company subject 
to lock-up 
undertakings 
upon listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock–up 
undertakings 
upon Listing 
(assuming the
Over-allotment
Option is not 
exercised)
Note 1
% of 
shareholding
in the Company 
subject to 
lock–up 
undertakings 
upon Listing 
(assuming the
Over-allotment
Option is not
exercised)
Note 1
Last day subject 
to the lock up 
undertakings
Note 2
Legend Capital SIIs
Note 3
Pathfinder SII
27,109,120
27,109,120
12.57%
6.16%
January 7, 2027
Meituan SII
Note 4
Pathfinder SII
17,217,310
17,217,310
7.98%
3.91%
January 7, 2027
Subtotal
44,326,430
44,326,430
20.55%
10.07%
Notes:
(1)	
Assuming the Over-allotment Option is not exercised. Each of Legend Capital SIIs and Meituan SII is a pathfinder SII of 
the Company as defined under Chapter 2.5 of the Guide for New Listing Applicants. Please refer to the section headed 
“History, Development and Corporate Structure — Capitalization of our Company” in the Prospectus for further details.
(2)	
In accordance with Rule 18C.14(2) of the Listing Rules, the required lock–up period commences on the date by reference 
to which disclosure of its shareholding is made in the Prospectus and ends on the date which is six months from the 
Listing Date, i.e. July 7, 2026. In addition to the lock-up requirement under Rule 18C.14(2) of the Listing Rules, all 
existing Shareholders shall not dispose of any of the Shares held by them within the 12 months following the Listing Date, 
i.e. January 7, 2027, as required under the applicable PRC laws.
(3)	
Representing the Shares to be held by Junlian Xiangdao, Junlian Jinfan and Social Security Zhongguancun Innovation 
Fund upon completion of the Global Offering.
(4)	
Representing the Shares to be held by Tianjin Sankuai upon completion of the Global Offering.

<<<PAGE 14>>>
14
Controlling Shareholders
Name
Number of 
shares held
in the Company
subject to 
lock-up 
undertakings 
upon listing
Number of 
H shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock–up 
undertakings 
upon Listing
Note 1
% of 
shareholding
in the Company 
subject to 
lock–up 
undertakings 
upon Listing
Note 1
Last day subject 
to the lock up 
undertakings
Note 2
Dr. Liu
925,150
—
—
0.21%
January 7, 2027
Beijing Lianpai 
34,038,390
—
—
7.73%
January 7, 2027
Huihui 
39,482,710
5,922,407
2.75%
8.97%
January 7, 2027
Zhideng 
27,196,330
4,079,450
1.89%
6.18%
January 7, 2027
Dr. Tang
26,835,330
—
—
6.10%
January 7, 2027
Dr. Li
3,367,760
—
—
0.76%
January 7, 2027
Dr. Xu
799,040
—
—
0.18%
January 7, 2027
Dr. Zhang
399,520
—
—
0.09%
January 7, 2027
Subtotal
133,044,230
10,001,857
4.64%
30.22% 
Notes:
(1)	
Assuming the Over-allotment Option is not exercised.
(2)	
All existing Shareholders (including the Controlling Shareholders) shall not dispose of any of the Shares held by them within the 12 months following the Listing 
Date as required under the applicable PRC laws.

<<<PAGE 15>>>
15
Existing Shareholders
Name
Note 1
Number of 
shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
Number of 
H shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock–up 
undertakings 
upon Listing
Note 2
% of 
shareholding
 in the Company 
subject to 
lock–up 
undertakings 
upon Listing
Note 2
Last day subject 
to the lock up 
undertakings
Note 3
Dr. Liu
925,150
—
—
0.21%
January 7, 2027
Beijing Lianpai 
34,038,390
—
—
7.73%
January 7, 2027
Huihui 
39,482,710
5,922,407
2.75%
8.97%
January 7, 2027
Zhideng 
27,196,330
4,079,450
1.89%
6.18%
January 7, 2027
Dr. Tang
26,835,330
—
—
6.10%
January 7, 2027
Dr. Li
3,367,760
—
—
0.76%
January 7, 2027
Dr. Xu
799,040
—
—
0.18%
January 7, 2027
Dr. Zhang
399,520
—
—
0.09%
January 7, 2027
Junlian Xiangdao
18,667,750
18,667,750
8.65%
4.24%
January 7, 2027
Junlian Jinfan
1,752,410
1,752,410
0.81%
0.40%
January 7, 2027
Social Security 
Zhongguancun 
Innovation Fund
6,688,960
6,688,960
3.10%
1.52%
January 7, 2027
Tianjin Sankuai
17,217,310
17,217,310
7.98%
3.91%
January 7, 2027
Qiming Rongqian
5,905,240
2,952,620
1.37%
1.34%
January 7, 2027
Qiming Rongkai
4,113,690
2,056,845
0.95%
0.93%
January 7, 2027
Xinglian Zhaoji
9,519,340
6,696,856
3.10%
2.16%
January 7, 2027
Tongzhi Investments
7,067,670
2,120,300
0.98%
1.61%
January 7, 2027
Shanghai Yunya
5,393,230
5,393,230
2.50%
1.23%
January 7, 2027
Shanghai Feiya
10,691,510
10,691,510
4.96%
2.43%
January 7, 2027
Haihe Fuxin Youda Fund
15,698,000
4,709,400
2.18%
3.57%
January 7, 2027
Tsinghua Technology
15,534,390
—
—
3.53%
January 7, 2027
TrendMega
11,349,910
11,349,910
5.26%
2.58%
January 7, 2027

<<<PAGE 16>>>
16
Name
Note 1
Number of 
shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
Number of 
H shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock–up 
undertakings 
upon Listing
Note 2
% of 
shareholding
 in the Company 
subject to 
lock–up 
undertakings 
upon Listing
Note 2
Last day subject 
to the lock up 
undertakings
Note 3
Dachen Chuanghong
8,233,410
2,470,023
1.15%
1.87%
January 7, 2027
Caizhi Chuangying
584,430
175,329
0.08%
0.13%
January 7, 2027
Beijing Huakong
3,007,520
1,503,760
0.70%
0.68%
January 7, 2027
Qingdao Huakong
5,280,470
2,640,235
1.22%
1.20%
January 7, 2027
Zhongguancun Science 
City
8,262,110
2,478,633
1.15%
1.88%
January 7, 2027
ZhuhaiHuafa
8,262,110
2,478,633
1.15%
1.88%
January 7, 2027
ZhihuiLinghang
8,262,110
4,131,055
1.92%
1.88%
January 7, 2027
AI Fund
7,955,740
3,977,870
1.84%
1.81%
January 7, 2027
Tencent Investment
6,948,540
6,948,540
3.22%
1.58%
January 7, 2027
Duoxiang Network
6,782,940
6,782,940
3.14%
1.54%
January 7, 2027
CAS Star
5,912,270
1,773,681
0.82%
1.34%
January 7, 2027
Hangzhou Chengtou 
Industrial Fund
5,783,470
1,735,041
0.80%
1.31%
January 7, 2027
Beijing Shunying
5,211,410
5,211,410
2.42%
1.18%
January 7, 2027
Daxing Industrial Fund
4,957,260
1,735,041
0.80%
1.13%
January 7, 2027
Prosperity7
4,953,900
4,953,900
2.30%
1.13%
January 7, 2027
High-tech Orinno
4,957,260
1,982,904
0.92%
1.13%
January 7, 2027
Xiamen Yaheng
3,823,090
1,911,545
0.89%
0.87%
January 7, 2027
Tianjin Heyuan
3,211,750
3,211,750
1.49%
0.73%
January 7, 2027
Hangzhou Guanghe
601,330
601,330
0.28%
0.14%
January 7, 2027
TAL
3,474,270
3,474,270
1.61%
0.79%
January 7, 2027
Ningbo Mingheng
3,474,270
1,042,281
0.48%
0.79%
January 7, 2027
Hainan Hezun
3,007,520
902,256
0.42%
0.68%
January 7, 2027
Lingyue No.4
2,086,180
625,854
0.29%
0.47%
January 7, 2027

<<<PAGE 17>>>
17
Name
Note 1
Number of 
shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
Number of 
H shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock–up 
undertakings 
upon Listing
Note 2
% of 
shareholding
 in the Company 
subject to 
lock–up 
undertakings 
upon Listing
Note 2
Last day subject 
to the lock up 
undertakings
Note 3
Lingyue No.5
392,450
117,735
0.05%
0.09%
January 7, 2027
Wuxi Yunhui
2,325,450
2,325,450
1.08%
0.53%
January 7, 2027
Tianchuang Capital
2,148,150
1,074,075
0.50%
0.49%
January 7, 2027
5G Fund
2,092,900
1,046,450
0.49%
0.48%
January 7, 2027
Shangcheng Linghang
1,652,420
1,321,936
0.61%
0.38%
January 7, 2027
Xiarui Investments
1,652,420
826,210
0.38%
0.38%
January 7, 2027
Lenovo Venture Capital
1,652,420
660,968
0.31%
0.38%
January 7, 2027
Jia’an Qixin
1,652,420
660,968
0.31%
0.38%
January 7, 2027
Jiangmen Venture 
Capital
1,503,760
451,128
0.21%
0.34%
January 7, 2027
Luster
1,503,760
451,128
0.21%
0.34%
January 7, 2027
Xiaofeng Technology
1,486,720
1,486,720
0.69%
0.34%
January 7, 2027
Huahai Jinpu
1,032,760
1,032,760
0.48%
0.23%
January 7, 2027
Zhaoshang Shuke
992,240
992,240
0.46%
0.23%
January 7, 2027
Innovation Zhiyuan
941,560
282,468
0.13%
0.21%
January 7, 2027
Rongjia Xingpu
866,290
433,145
0.20%
0.20%
January 7, 2027
Lianrong Zhiyuan
860,620
860,620
0.40%
0.20%
January 7, 2027
Lingtou Future
813,820
—
—
0.18%
January 7, 2027
Shanchuang Zhizhi
429,200
429,200
0.20%
0.10%
January 7, 2027
Hengqin Shanzhi
429,200
429,200
0.20%
0.10%
January 7, 2027
Zhongxiao Ruizheng
403,030
201,515
0.09%
0.09%
January 7, 2027
Shandong Fuhong
302,100
151,050
0.07%
0.07%
January 7, 2027
Subtotal
402,810,690
178,282,205
82.65%
91.50%

<<<PAGE 18>>>
18
Name
Note 1
Number of 
shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
Number of 
H shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock–up 
undertakings 
upon Listing
Note 2
% of 
shareholding
 in the Company 
subject to 
lock–up 
undertakings 
upon Listing
Note 2
Last day subject 
to the lock up 
undertakings
Note 3
Notes:
(1)	
Please refer to the Prospectus for further details.
(2)	
Assuming the Over-allotment Option is not exercised.
(3)	
The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws.
Cornerstone Investors
Name 
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon listing
% of total 
issued H 
Shares after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of 
shareholding g 
in the Company 
subject to 
lock-up 
undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock up 
undertakings
JSC International 
Investment Fund SPC 
(acting for and on 
behalf of Qizhi SP)
11,985,900
5.56%
2.72%
July 7, 2026
JinYi Capital Multi-
Strategy Fund SPC 
Ltd. (acting for and on 
behalf of Structured 
Credit SP Fund)
468,700 
0.22%
0.11%
July 7, 2026
Perseverance Asset 
Management
1,941,800 
0.90%
0.44%
July 7, 2026
Shanghai Gaoyi 
and CICC Financial 
Trading Limited (in 
connection with Gaoyi 
OTC Swaps)
602,600 
0.28%
0.14%
July 7, 2026

<<<PAGE 19>>>
19
Name 
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon listing
% of total 
issued H 
Shares after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of 
shareholding g 
in the Company 
subject to 
lock-up 
undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock up 
undertakings
WT Asset 
Management
3,006,500 
1.39%
0.68%
July 7, 2026
Taikang Life
2,008,800 
0.93%
0.46%
July 7, 2026
GF Fund
2,812,300 
1.30%
0.64%
July 7, 2026
3W Fund
1,205,200 
0.56%
0.27%
July 7, 2026
RIME
645,400 
0.30%
0.15%
July 7, 2026
Optimas Capital 
Limited
669,600 
0.31%
0.15%
July 7, 2026
Luster LightTech 
International Limited
334,800 
0.16%
0.08%
July 7, 2026
Subtotal
25,681,600
11.91%
5.83%

<<<PAGE 20>>>
20
PLACEE CONCENTRATION ANALYSIS
Placees
Number of 
Shares allotted
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
Option is fully 
exercised and 
new Shares 
are issued)
Allotment as 
% of total 
Offer Shares 
(assuming 
no exercise 
of the Over-
allotment 
Option is 
exercised)
Allotment as 
% of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option is fully 
exercised and 
new Shares 
are issued)
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
Option is fully 
exercised and 
new Shares 
are issued)
Top 1
11,985,900
40.04%
33.72%
32.03%
27.85%
33,161,010
7.53%
7.44%
Top 5
22,357,900
74.69%
62.89%
59.75%
51.96%
43,533,010
9.89%
9.76%
Top 10
26,433,200
88.30%
74.36%
70.64%
61.43%
47,608,310
10.81%
10.68%
Top 25
31,189,000
104.19%
87.74%
83.35%
72.48%
69,402,260
15.76%
15.57%
Notes
*  Ranking of placees is based on the number of Offer Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders
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
Option 
is fully 
exercised 
and new 
Shares are 
issued)
Allotment as 
% of total 
Offer Shares 
(assuming 
no exercise 
of the Over-
allotment 
Option is 
exercised)
Allotment as 
% of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised 
and new 
Shares are 
issued)
Number of H 
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
Option 
is fully 
exercised 
and new 
Shares are 
issued)
Number of 
total Shares 
held upon 
Listing
Top 1
—
0.00%
0.00%
0.00%
0.00%
27,109,120
6.16%
6.08%
27,109,120
Top 5
11,985,900
40.04%
33.72%
32.03%
27.85%
91,938,524
20.88%
20.62%
104,922,090
Top 10
11,985,900
40.04%
33.72%
32.03%
27.85%
129,700,427
29.46%
29.09%
273,496,220
Top 25
22,357,900
74.69%
62.89%
59.75%
51.96%
179,739,931
40.83%
40.31%
362,739,160
Notes
*  Ranking of H Shareholders is based on the number of Shares held by the Shareholders upon Listing.

<<<PAGE 21>>>
21
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
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
Option 
is fully 
exercised 
and new 
Shares are 
issued)
Allotment as 
% of total 
Offer Shares 
(assuming 
no exercise 
of the Over-
allotment 
Option is 
exercised)
Allotment as 
% of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised 
and new 
Shares are 
issued)
Number of H 
Shares held 
upon Listing
Number of 
total Shares 
held upon 
Listing
Number of 
total shares 
held upon 
listing as 
% of total 
issued share 
capital upon 
Listing 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Number of 
total shares 
held upon 
listing as 
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised 
and new 
Shares are 
issued)
Top 1
—
0.00%
0.00%
0.00%
0.00%
10,001,857
133,044,230
30.22%
29.84%
Top 5
11,985,900
40.04%
33.72%
32.03%
27.85%
83,322,887
227,118,680
51.59%
50.94%
Top 10
12,454,600
41.60%
35.04%
33.28%
28.94%
120,945,102
296,273,350
67.30%
66.45%
Top 25
12,483,000
41.70%
35.12%
33.36%
29.01%
174,002,129
385,066,300
87.47%
86.37%
Notes
*  Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 22>>>
22
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by the 
public will be conditionally allocated on the basis set out below:
Pool A
 Number of 
H Shares 
applied for 
 Number 
of valid 
applications Basis of allocation/ballot
Approximate 
percentage 
allotted of the 
total number 
of H Shares 
applied for
100
92,859
4,643 out of 92,859 applicants to receive 100 H Shares
5.00%
200
12,235
897 out of 12,235 applicants to receive 100 H Shares
3.67%
300
5,502
505 out of 5,502 applicants to receive 100 H Shares
3.06%
400
13,605
1,462 out of 13,605 applicants to receive 100 H Shares
2.69%
500
4,461
543 out of 4,461 applicants to receive 100 H Shares
2.43%
600
1,699
229 out of 1,699 applicants to receive 100 H Shares
2.25%
700
1,068
157 out of 1,068 applicants to receive 100 H Shares
2.10%
800
2,695
425 out of 2,695 applicants to receive 100 H Shares
1.97%
900
1,784
300 out of 1,784 applicants to receive 100 H Shares
1.87%
1,000
10,763
1,918 out of 10,763 applicants to receive 100 H Shares
1.78%
1,500
3,513
783 out of 3,513 applicants to receive 100 H Shares
1.49%
2,000
3,709
969 out of 3,709 applicants to receive 100 H Shares
1.31%
2,500
1,896
560 out of 1,896 applicants to receive 100 H Shares
1.18%
3,000
2,337
764 out of 2,337 applicants to receive 100 H Shares
1.09%
3,500
1,331
474 out of 1,331 applicants to receive 100 H Shares
1.02%
4,000
1,816
696 out of 1,816 applicants to receive 100 H Shares
0.96%
4,500
1,141
467 out of 1,141 applicants to receive 100 H Shares
0.91%
5,000
2,813
1,218 out of 2,813 applicants to receive 100 H Shares
0.87%
6,000
1,693
811 out of 1,693 applicants to receive 100 H Shares
0.80%
7,000
1,329
693 out of 1,329 applicants to receive 100 H Shares
0.74%
8,000
1,460
820 out of 1,460 applicants to receive 100 H Shares
0.70%
9,000
1,302
750 out of 1,302 applicants to receive 100 H Shares
0.64%
10,000
7,925
4,888 out of 7,925 applicants to receive 100 H Shares
0.62%
20,000
5,297
100 H Shares
0.50%
30,000
2,898
100 H Shares plus 406 out of 2,898 applicants to receive an 
additional 100 H Shares
0.38%
40,000
2,914
100 H Shares plus 933 out of 2,914 applicants to receive an 
additional 100 H Shares
0.33%
 
 Total 
 190,045 Total number of Pool A successful applicants: 36,081
 

<<<PAGE 23>>>
23
Pool B
 Number of 
H Shares 
applied for 
 Number 
of valid 
applications Basis of allocation/ballot
Approximate 
percentage 
allotted of the 
total number 
of H Shares 
applied for
50,000
6,994
100 H Shares plus 3,497 out of 6,994 applicants to receive an 
additional 100 H Shares
0.30%
60,000
1,398
100 H Shares plus 1,010 out of 1,398 applicants to receive an 
additional 100 H Shares
0.29%
70,000
817
100 H Shares plus 764 out of 817 applicants to receive an 
additional 100 H Shares
0.28%
80,000
700
200 H Shares plus 99 out of 700 applicants to receive an 
additional 100 H Shares
0.27%
90,000
550
200 H Shares plus 188 out of 550 applicants to receive an 
additional 100 H Shares
0.26%
100,000
2,340
200 H Shares plus 1,014 out of 2,340 applicants to receive an 
additional 100 H Shares
0.24%
200,000
915
400 H Shares plus 366 out of 915 applicants to receive an 
additional 100 H Shares
0.22%
300,000
328
600 H Shares plus 99 out of 328 applicants to receive an 
additional 100 H Shares
0.21%
400,000
187
800 H Shares
0.20%
500,000
129
900 H Shares
0.18%
600,000
78
1,000 H Shares
0.17%
700,000
43
1,100 H Shares
0.16%
800,000
56
1,200 H Shares
0.15%
935,500
291
1,300 H Shares
0.14%
 
 Total 
 14,826 Total number of Pool B successful applicants: 14,826
 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and trading fee payable.

<<<PAGE 24>>>
24
The Directors and the Overall Coordinators confirm that at least 50% of the total number of 
the Offer Shares (excluding any Offer Shares to be issued pursuant to the exercise of the Over-
allotment Option, if any) have been allocated to and taken up by independent price setting investors 
in compliance with Rule 18C.08 of the Listing Rules.
The Directors further confirm that at least 10% of the issued share capital of the Company will be 
held by sophisticated independent investors at the time of Listing in compliance with Chapter 2.5 of 
the Guide for New Listing Applicants.
OTHERS/ADDITIONAL INFORMATION
Reallocation
As the Hong Kong Public Offering has been over-subscribed by more than 50 times of the total 
number of Offer Shares initially available under the Hong Kong Public Offering, the reallocation 
procedure as disclosed in the section headed “Structure of the Global Offering — The Hong Kong 
Public Offering — Reallocation and Clawback” in the Prospectus has been applied.
The number of Offer Shares initially available under the Hong Kong Public Offering is 1,871,000 
Shares, representing approximately 5% of the total number of Offer Shares initially available under 
the Global Offering (assuming the Over-allotment Option is not exercised). As a result of such 
reallocation, the final number of Offer Shares under the Hong Kong Public Offering is adjusted to 
7,483,900 Shares, representing 20% of the total number of Offer Shares initially available under the 
Global Offering (assuming the Over-allotment Option is not exercised).
Placing to existing shareholders and/or its close associates with a prior waiver under Rule 
10.04 of the Listing Rules and consent under paragraph 1C(1) of the Placing Guidelines
We have applied for a waiver under Rule 10.04 of the Listing Rules and consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules to permit the existing shareholders and/or its close 
associates to participate as cornerstone investors or placees in the Global Offering to subscribe 
for the Offer Shares to be issued by the Company under the International Offering (together, the 
“Existing Shareholder Participants”). The Stock Exchange has agreed to grant the requested 
consent subject to the conditions that:
(a)	 the Company will comply with the public float requirements of Rules 19A.13A and 18C.08 of 
the Listing Rules and the free float requirements of Rule 19A.13C of the Listing Rules;
(b)	 the Company and the Sole Sponsor confirm that no preferential treatment has been, nor 
will be, directly or indirectly, given to the Existing Shareholder Participants, as cornerstone 
investors or placees by virtue of their relationship with the Company in any allocation in 
the Global Offering, other than the preferential treatment of assured entitlement under the 
cornerstone investments at the Offer Price and the terms are substantially the same as other 
cornerstone investors; and
(c)	 details of the subscription of the Offer Shares by the Existing Shareholder Participants as 
cornerstone investors under the Global Offering are disclosed in the Prospectus, and details of 
the allocation will be disclosed in this allotment results announcement.

<<<PAGE 25>>>
25
For details of the allocations of Offer Shares to such Existing Shareholder Participants, please 
refer to the section headed “Allotment Results Details — International Offering — Allottees with 
Waivers/Consents Obtained” in this announcement.
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such 
Offer Shares in the International Offering to the connected clients. The allocation of Offer Shares 
to such connected clients is in compliance with all the conditions under the consent granted by the 
Stock Exchange. Details of the placement to connected clients are set out below:
No.
Connected 
Distributor 
Connected client 
Relationship
Identities of 
the ultimate 
beneficial 
owners of the 
Offer Shares 
or, where 
applicable, 
details of the 
structured 
products under 
which the 
subscription by 
the Connected 
Client was made 
(e.g. OTC total 
return swaps)
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
Amount of Offer 
Shares to be 
allocated to the 
Connected Client 
(based on the 
Offer Price of 
HK$116.20 per 
H Share)
Approximate 
percentage of 
total number 
of Offer Shares 
under the 
Global Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Approximate 
percentage of 
total issued share 
capital after the 
Global Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Part A — Connected Client holding the beneficial interest of the Offer Shares on a non-discretionary basis on behalf of independent third parties
1.
China Internation 
al Capital 
Corporation 
Hong Kong 
Securities 
Limited 
(“CICCHKS”)
CICC Financial 
Trading Limited 
(CICC FT)
CICC FT is a 
member of the 
same group of 
CICCHKS
Please refer to 
note (1).
N
602,600
1.61%
0.14%
Please refer to 
note (2).
N
92,300
0.25%
0.02%
2.
Huatai Financial 
Holdings (Hong 
Kong) Limited 
(“HTFH”)
Huatai Capital 
Investment 
Limited 
(“HTCI”)
HTFH and 
HTCI are fellow 
subsidiaries 
of Huatai 
Securities Co., 
Ltd. (“Huatai 
Securities”)
Please refer to 
note (3).
N
147,600
0.39%
0.03%
Please refer to 
note (4).
N
18,900
0.05%
0.004%
3.
Guotai Junan 
Securities (Hong 
Kong) Limited 
(“Guotai 
Junan”)
Guotai Junan 
Investments 
(Hong Kong) 
Limited 
(“GTJAI”)
GTJAI is a 
member of the 
same group of 
Guotai Junan
Please refer to 
note (5).
N
88,700
0.24%
0.02%

<<<PAGE 26>>>
26
No.
Connected 
Distributor 
Connected client 
Relationship
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
Amount of Offer 
Shares to be 
allocated to the 
Connected Client 
(based on the Offer 
Price of HK$116.20 
per H Share)
Approximate 
percentage of total 
number of Offer 
Shares under the 
Global Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Approximate 
percentage of total 
issued share capital 
after the Global 
Offering (assuming 
no exercise of the 
Over-allotment 
Option)
Part B — Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties
1.
China Merchants 
Securities (HK) Co. 
(“CMS”) and CMB 
International Capital 
Limited (“CMBI”)
Bosera Asset 
Management 
(International) Co., 
Limited (“Bosera 
AM”) (Note 6)
Bosera AM is a 
member of the same 
group of CMS and 
CMBI
N
13,400
0.04%
0.003%
2.
Guotai Junan 
Securities (Hong 
Kong) Limited 
(“Guotai Junan”) 
and Haitong 
International 
Securities Company 
Limited (“Haitong 
IS”)
Fullgoal Fund 
Management Co., 
Ltd and Fullgoal 
Asset Management 
(HK) Limited 
(collectively, 
“Fullgoal Funds”)
(Note 7)
Fullgoal Funds 
are members of 
the same group of 
Guotai Junan and 
Haitong IS
N
66,900
0.18%
0.02%
Haitong 
International Asset 
Management 
(HK) Limited 
and Haitong 
International 
Investment 
Managers Limited 
(collectively, 
“Haitong AMs”) 
(Note 8)
Haitong AMs are 
members of the 
same group of 
Guotai Junan and 
Haitong IS
N
6,600
0.02%
0.001%
3.
CITIC Securities 
Brokerage (HK) 
Limited (“CSB”)
China Asset 
Management (Hong 
Kong) Limited 
(“ChinaAMC HK”) 
(Note 9)
ChinaAMC HK 
and ChinaAMC 
are members of the 
same group of CSB
N
6,600
0.02%
0.001%
China Asset 
Management 
Co., Ltd. 
(“ChinaAMC”) 
(Note 10)
N
66,900
0.18%
0.02%
4.
BOCOM 
International 
Securities Limited 
(“BOCOMI 
Securities”)
BOCOM 
International Asset 
Management 
Limited 
(“BOCOMI AM”)
(Note 11)
BOCOMI AM is 
a members of the 
same group of 
BOCOMI Securities
N
18,900
0.05%
0.004%

<<<PAGE 27>>>
27
Notes:
(1)	
CICC FT has entered into cornerstone investment agreements with the Company, the Sole Sponsor and the Sponsor-OC, to 
participate as a cornerstone investor in the Global Offering to subscribe for the Offer Shares to be issued by the Company 
under the International Offering.
	
CICC FT and China International Capital Corporation Limited has entered into a series of cross border delta-one OTC 
swap transactions (collectively, the Gaoyi OTC Swaps) with each other and the ultimate clients (the “CICC FT Ultimate 
Clients (Gaoyi)”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the Gaoyi 
OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed to the CICC FT Ultimate 
Clients (Gaoyi), subject to customary fees and commissions. The Gaoyi OTC Swaps will be fully funded by the CICC FT 
Ultimate Clients (Gaoyi). During the terms of the Gaoyi OTC Swaps, all economic returns of the Offer Shares subscribed 
by CICC FT will be passed to the CICC FT Ultimate Clients (Gaoyi) and all economic loss shall be borne by the CICC FT 
Ultimate Clients (Gaoyi) through the Gaoyi OTC Swaps, and CICC FT will not take part in any economic return or bear any 
economic loss in relation to the Offer Shares.
	
To the best of CICC FT’s knowledge having made all reasonable inquiries, each of the CICC FT Ultimate Clients (Gaoyi) is 
an independent third party of CICC FT, CICCHKS and the companies which are members of the same group of CICCHKS, 
and no single ultimate beneficial owner holds 30% or more interests in each of the CICC FT Ultimate Clients (Gaoyi).
(2)	
CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one OTC swap 
transactions (collectively, the “CICC FT OTC Swaps”) with each other and the ultimate clients (the “CICC FT Underlying 
Clients”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the CICC FT OTC 
Swaps while the economic risks and returns of the underlying Offer Shares are passed to the CICC FT Underlying Clients, 
subject to customary fees and commissions.
	
The CICC FT Ultimate Clients include (i) Hengze Jinze No. E49 Private Equity Securities Investment Fund (恒德金澤E49號
私募證券投資基金). Its fund manager is Beijing Hengde Shidai Private Equity Fund Management Co., Ltd. (北京恒德時代
私募基金管理有限公司), which is ultimately controlled as to 45% by Wang Yu (王玨), 45% by Yu Yan (遇言) and 10% by 
Duan Gengchao (段更超). Except for Pan Jianyue, none of the ultimate beneficial owners of Hengze Jinze No. E49 Private 
Equity Securities Investment Fund holds an interest of 30% or more; (ii) Wangzheng Gongying No. 17 Private Securities 
Investment Fund (望正共贏17號私募證券投資基金). Its fund manager is Shenzhen Upright Asset Management Company 
Limited (深圳望正資產管理有限公司), which is controlled as to 94% by Qu Qin (瞿琴) and as to 6% by Wang Penghui 
(王鵬輝). Except for Qu Qin, none of the ultimate beneficial owners of Wangzheng Gongying No. 17 Private Securities 
Investment Fund holds an interest of 30% or more; (iii) Zuoqihe Tianxia No.9 Private Securities Investment Fund (左啟禾
天下9號私募證券投資基金). Its fund manager is Shanghai Zuoqi Private Equity Fund Management Co., Ltd. (上海左啟私
募基金管理有限公司), which is controlled as to 85.7143% by Duan Juanjuan (段娟娟) and 14.2857% by Xia Shan (夏珊). 
Except for Duan Juanjuan, none of the ultimate beneficial owners of Zuoqihe Tianxia No.9 Private Securities Investment 
Fund holds an interest of 30% or more; and (iv) Baoyin Duokong Stable No.1 (保銀多空穩健1號), Baoyin Duokong Stable 
No.2 (保銀多空穩健2號) and Baoyin Jinqu No.1 (保銀進取1號). Its fund manager is Shanghai Baoyin Private Equity Fund 
Management Co., Ltd. (上海保銀私募基金管理有限公司), which is controlled as to 84.1% by Li Mo (李墨)and as to 15.9% 
by Shanghai Baoyin Investment Consulting Co., Ltd. (上海保銀投資顧問有限公司). None of the limited partners of Baoyin 
Duokong Stable No.1, Baoyin Duokong Stable No.2 and Baoyin Jinqu No.1 hold an interest of 30% or more.
	
To the best knowledge of CICC FT after due enquiry, each of the CICC FT Underlying Clients is an independent third party 
of the Company, its subsidiaries, CICC FT and CICCHKS and the companies which are members of the same group of 
CICCHKS.
(3)	
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public offerings 
(“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products issued by appropriate domestic 
securities firms licensed to undertake cross-border derivatives trading activities. In connection with such products, the 
licensed domestic securities firms, through their Hong Kong affiliates, may participate in Hong Kong IPOs either as placees 
or cornerstone investors (the “Cross-border Derivatives Trading Regime”).
	
Huatai Securities, the shares of which are listed on both the Shanghai Stock Exchange (stock code: 601688) and the Stock 
Exchange (stock code: 6886), is one of the domestic securities firms licensed to undertake cross-border derivatives trading 
activities. Huatai Securities entered into an ISDA agreement (the “ISDA Agreement”) with its indirectly wholly-owned 

<<<PAGE 28>>>
28
subsidiary, Huatai Capital Investment Limited (“HTCI”) to set out the principal terms of any future total return swap 
between Huatai Securities and HTCI.
	
HTFH is the one of the Overall Coordinators and Underwriters in connection with the Global Offering. Pursuant to the 
ISDA Agreement, HTCI, which intends to participate in the Global Offering as a placee, will hold the beneficial interest 
of the Offer Shares on a non-discretionary basis as the single underlying holder under a back-to-back total return swap 
(the “Back-to-back TRS”) to be entered by HTCI in connection with a Client TRS (as defined below) placed by and fully 
funded (i.e. with no financing provided by HTCI) by the Huatai Onshore Ultimate Clients (as defined below), by which, 
HTCI will, subject to customary fees and commissions, pass the full economic exposure of the Offer Shares ultimately to the 
Huatai Onshore Ultimate Clients, which in effect, HTCI will hold the beneficial interest of the Offer Shares on behalf of the 
Huatai Onshore Ultimate Clients. HTFH, the Overall Coordinator and Underwriter, and HTCI are indirectly wholly-owned 
subsidiaries of Huatai Securities. Accordingly, HTCI is considered as a “connected client” of HTFH pursuant to paragraph 
13(7) of the Placing Guidelines.
	
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the “Huatai Onshore Ultimate Clients”) 
cannot directly subscribe for the Offer Shares but may invest in derivative products issued by domestic securities firms 
licenced to undertake cross-border derivatives trading activities, such as Huatai Securities, with the Offer Shares as the 
underlying assets. Instead of directly subscribing for the Offer Shares, the Huatai Onshore Ultimate Clients, through 
their respective investment managers as applicable, will place a total return swap order (the “Client TRS”) with Huatai 
Securities in connection with the Company’s IPO and Huatai Securities will place a Back-to-back TRS order to HTCI on 
the terms of the ISDA Agreement. In order to hedge its exposure under the Back-to-back TRS, HTCI participates in the 
Company’s IPO and subscribes the Offer Shares through placing order with HTFH during the International Offering.
	
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in connection with the Client 
TRS order placed by the Huatai Onshore Ultimate Clients. Pursuant to the terms of the contracts of the Back-to-back 
TRS and the Client TRS, during the tenor of the Back-to-back TRS and the Client TRS, subject to customary fees and 
commissions, all economic returns of the Offer Shares will be ultimately passed to the Huatai Onshore Ultimate Clients 
through the Back-to-back TRS and the Client TRS and all economic loss shall be ultimately borne by the Huatai Onshore 
Ultimate Clients. HTCI will not take any economic return or bear any economic loss in relation to the Offer Shares.
	
Investment in the Back-to-back TRS and the Client TRS is similar to the investment in a qualified domestic institutional 
investor fund (“QDII”) in the way that the Huatai Onshore Ultimate Clients would reap all the economic benefits of the 
underlying Offer Shares, except that a QDII fund would pass through the exchange rate exposure on both the notional value 
of the investment and the profit and loss of the investment. In contrast, the profit and loss of the Back-to-back TRS and the 
Client TRS factor into account the fluctuation in RMB exchange rate upon termination of the Client TRS by converting the 
profit and loss using the current exchange rate at the time of termination. As such, the Huatai Onshore Ultimate Clients 
would bear the exchange rate exposure of the profit and loss on settlement date.
	
The Huatai Onshore Ultimate Clients may exercise an early termination right to terminate the Client TRS at its own 
discretion. Upon the termination upon maturity or early termination of the Client TRS by the Huatai Onshore Ultimate 
Clients, HTCI will dispose the Offer Shares on the secondary market and the Huatai Onshore Ultimate Clients will receive 
a final settlement amount in cash in accordance with the terms and conditions of the Back-to-back TRS and the Client TRS 
which should have taken into account all the economic returns or economic loss in relation to the Offer Shares. If upon the 
maturity of the Client TRS, the Huatai Onshore Ultimate Clients intend to extend the investment period, subject to further 
agreement between Huatai Securities and the relevant Huatai Onshore Ultimate Clients, the term of the Client TRS could be 
extended by way of a new issuance or a tenor extension. Accordingly, Huatai Securities will extend the term of the Back-to-
back TRS by way of a new issuance or a tenor extension.
	
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through the 
economic exposure to the Huatai Onshore Ultimate Clients, each being an onshore client who places a Client TRS order 
with Huatai Securities in connection with the IPO of the Company. HTCI will not exercise the voting right of the Offer 
Shares during the tenor of the Back-to-back TRS.
	
During the life of the Client TRS and Back-to-back TRS, HTCI may continue to hold the Offer Shares in its custodian 
account, or to hold some or all of the Offer Shares in a prime brokerage account for stock borrowing purposes, where HTCI 
will lend out its holding of underlying Offer Shares in the form of stock borrowing loans consistent with market practice 
to lower its finance costs, provided that HTCI has the ability to call back the Offer Shares on loan at any time in order 
to satisfy its obligations under the Back-to-back TRS to ensure the economic interests are ultimately passed to the Huatai 
Onshore Ultimate Clients.

<<<PAGE 29>>>
29
	
HTCI will purchase and hold the Offer Shares on a non-discretionary basis in accordance with the instruction from 
and for and on behalf of its underlying clients (the “HTCI Underlying Clients”), namely (i) Beijing Yuanfeng Private 
Equity Fund Management Partnership (Limited Partnership) (北京源峰私募基金管理合夥企業 (有限合夥)) (“Beijing 
Yuanfeng”). None of ultimate beneficial owners holds an interest of 30% or more in Beijing Yuanfeng. The general 
partner of Beijing Yuanfeng is Shanghai Rongyu Enterprise Management Partnership (Limited Partnership) (上海鎔
聿企業管理合夥企業（有限合夥）) (“Shanghai Rongyu”). None of ultimate beneficial owners holds an interest 
of 30% or more in Shanghai Rongyu. The largest limited partner of Beijing Yuanfeng is Hangzhou Xinyu Youxuan 
Investment Management Partnership Enterprise (Limited Partnership) (杭州信聿優選投資管理合夥企業（有限合夥）)
(“Hangzhou Xinyu”), holding approximately 91% partnership. None of ultimate beneficial owners holds an interest 
of 30% or more in Hangzhou Xinyu; (ii) Daohe Chengguang Private Equity Securities Investment Fund (道合承光
私募證券投資基金) (“Daohe Chengguang”). The fund manager of Daohe Chengguang is Shanghai Daohe Private 
Equity Fund Management Co., Ltd. (上海道合私募基金管理有限公司), which is controlled as to 65% by Zhao Bin 
(趙斌), 21% by Li Jianan (李佳男) and 14% by Tong Bo (童波), (iii) Zhongke Chuangxing Technology Investment Co., Ltd. 
(中科創星科技投資有限公司). Except for Mi Lei (米磊), none of the ultimate beneficial owners of Zhongke Chuangxing 
Technology Investment Co., Ltd. holds an interest of 30% or more.
	
To the best of HTFH’s knowledge and after making all reasonable enquiries, each of the Huatai Onshore Ultimate Clients is 
an independent third party of (i) the Company, the connected person or the associates thereof, and (ii) HTCI, HTFH and the 
companies which are members of the same group of HTCI.
(4)	
HTFH is one of the Overall Coordinators and Underwriters in connection with the Global Offering. Pursuant to an ISDA 
Agreement, HTCI, which intends to participate in the Global Offering as a placee, will hold the beneficial interest of the 
Offer Shares on a non-discretionary basis as the single underlying holder under a back-to-back total return swap (the 
“Back-to-back TRS”) to be entered by HTCI in connection with a Client TRS (as defined below) placed by and fully funded 
(i.e. with no financing provided by HTCI) by the Huatai Offshore Ultimate Client (as defined below), by which, HTCI will, 
subject to customary fees and commissions, pass the full economic exposure of the Offer Shares to the Huatai Offshore 
Ultimate Client, which in effect, HTCI will hold the beneficial interest of the Offer Shares on behalf of the Huatai Offshore 
Ultimate Client. Accordingly, HTCI is considered as a “connected client” of HTFH pursuant to paragraph 13(7) of the 
Placing Guidelines.
	
The offshore investor (the “Huatai Offshore Ultimate Client”), through its respective investment manager, will place 
a total return swap order (the “Client TRS”) with HTCI in connection with the Company’s IPO. In order to hedge its 
exposure under the Client TRS, HTCI participates in the Company’s IPO and subscribes the Offer Shares through placing 
order with HTFH during the International Offering.
	
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Client TRS order placed by the Huatai Offshore 
Ultimate Client. Pursuant to the terms of the Client TRS, during the tenor of the Client TRS, subject to customary fees and 
commissions, all economic returns of the Offer Shares will be ultimately passed to the Huatai Offshore Ultimate Client 
through the Client TRS and all economic loss shall be ultimately borne by the Huatai Offshore Ultimate Client. HTCI will 
not take any economic return or bear any economic loss in relation to the Offer Shares.
	
The Huatai Offshore Ultimate Client may exercise an early termination right to terminate the Client TRS at any time from 
the issue date of the Client TRS which should be on or after the date on which the Offer Shares are listed on the Stock 
Exchange at their own discretion. Upon the termination upon maturity or early termination of the Client TRS by the Huatai 
Offshore Ultimate Client, HTCI will dispose the Offer Shares on the secondary market and the Huatai Offshore Ultimate 
Client will receive a final settlement amount of the Client TRS in cash in accordance with the terms and conditions of the 
Client TRS which should have taken into account all the economic returns or economic loss in relation to the Offer Shares. 
If upon the maturity of the Client TRS, the Huatai Offshore Ultimate Client intends to extend the investment period, subject 
to further agreement between HTCI and the relevant Huatai Offshore Ultimate Client, the term of the Client TRS could be 
extended by way of a new issuance or a tenor extension.
	
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through the 
economic exposure to the Huatai Offshore Ultimate Client, being the client who places a Client TRS order with HTCI in 
connection with the IPO of the Company. HTCI will not exercise the voting right of the Offer Shares during the tenor of the 
Client TRS.
	
During the life of the Client TRS, HTCI may continue to hold the Offer Shares in its custodian account, or to hold some or 
all of the Offer Shares in a prime brokerage account for stock borrowing purposes, where HTCI will lend out its holding 
of underlying Offer Shares in the form of stock borrowing loans consistent with market practice to lower its finance costs, 
provided that HTCI has the ability to call back the Offer Shares on loan at any time in order to satisfy its obligations under 
the Client TRS to ensure the economic interests are ultimately passed to the Huatai Offshore Ultimate Client.

<<<PAGE 30>>>
30
	
HTCI will purchase and hold the Offer Shares on a non-discretionary basis in accordance with the instruction from and for 
and on behalf of its underlying client (the “HTCI Underlying Client”), namely KSICN SPC SUB KSICN SP2. Except for 
Zhu Lei, none of the ultimate beneficial owners of KSICN SPC SUB KSICN SP2 holds an interest of 30% or more.
	
To the best of HTFH’s knowledge and after making all reasonable enquiries, the Huatai Offshore Ultimate Client is an 
independent third party of (i) the Company, the connected person or the associates thereof, and (ii) HTCI, HTFH and the 
companies which are members of the same group of HTCI.
(5)	
It is proposed that GTJAI participates as placee to subscribe for the Offer Shares under the International Offering (the 
“GTJAI Subscription”).
	
In relation to the GTJAI Subscription, GTJAI shall hold the Offer Shares for hedging purpose as the single underlying asset 
of several sets of back-to-back total return swap transaction (the “GTHT Back-to-back TRS”) to be entered into between 
GTJAI and Guotai Haitong Securities Co., Ltd. (the “GTHT Onshore Parent”) in connection with several total return 
swap orders (the “GTHT Client TRS”) to be entered into by GTHT Onshore Parent and several underlying clients (the 
“GTHT Onshore Underlying Clients”), respectively. Such GTHT Client TRS is to be fully funded by the GTHT Onshore 
Underlying Client. GTJAI will hold the Offer Shares on a non-discretionary basis for the purpose of hedging the economic 
exposure under the GTHT Back-to-back TRS and GTHT Client TRS only. During the tenor of the GTHT Client TRS, all 
economic returns of the Offer Shares will be passed to the GTHT Onshore Underlying Clients and all economic losses shall 
be borne by the GTHT Onshore Underlying Client, subject to the terms and conditions of the GTHT Back-to-back TRS and 
GTHT Client TRS, and GTJAI will not take part in any economic return or bear any economic loss in relation to the price 
of the Offer Shares. The GTHT Onshore Underlying Client may request to redeem the Offer Shares at their own discretion, 
upon which GTJAI shall dispose of the Offer Shares and settle the GTHT Back-to-back TRS and GTHT Client TRS in cash 
in accordance with the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS documents. Due to its 
internal policy, GTJAI will not exercise the voting right attaching to the Offer Shares during the tenor of the GTHT Back-to-
back TRS and GTHT Client TRS.
	
To the best knowledge, information and belief of GTJA Investments after due enquiry, the GTJA Onshore Ultimate Clients 
and their respective ultimate beneficial owners holding 30% or more interest include (i) Splendid Zhonghe (Tianjin) 
Investment Management Co., Ltd. (錦繡中和(天津)投資管理有限公司). Except for Wang Diansuo (王殿鎖), none of 
the ultimate beneficial owners of Splendid Zhonghe (Tianjin) Investment Management Co., Ltd. holds an interest of 30% 
or more; (ii) Qingdao Roadshow Investment Management Co., Ltd. (青島鹿秀投資管理有限公司). Except for Zhang 
Chengyong (張成勇), none of the ultimate beneficial owners of Qingdao Roadshow Investment Management Co., Ltd. holds 
an interest of 30% or more; (iii) Shanghai Qufeng International Trade Co., Ltd. (上海渠豐國際貿易有限公司). Except for 
Yang Lu (楊璐), none of the ultimate beneficial owners of Shanghai Qufeng International Trade Co., Ltd. holds an interest 
of 30% or more; (iv) Jedi Asset Management, LLC (上海金澹資產管理有限公司). Except for Ding Hai (丁海), none of 
the ultimate beneficial owners of Jedi Asset Management, LLC holds an interest of 30% or more; (v) Shanghai Panjing 
Investment Center (Limited Partnership) (上海盤京投資管理中心 (有限合夥)). None of the ultimate beneficial owners of 
Shanghai Panjing Investment Center (Limited Partnership) holds an interest of 30% or more; and (vi) Zhejiang Junhong 
Asset Management Co., Ltd. (浙江君弘資產管理有限公司). Except for Lan Jun (蘭俊), none of the ultimate beneficial 
owners of Zhejiang Junhong Asset Management Co., Ltd. holds an interest of 30% or more.
	
To the best knowledge of GTJAI after due enquiry, each of the GTHT Onshore Underlying Clients is an independent third 
party of the Company, its subsidiaries, GTJAI and Guotai Junan and the companies which are members of the same group 
of Guotai Junan.
(6)	
It is proposed that Bosera AM proposes to subscribe for and hold 13,400 Offer Shares (the “Proposed Bosera AM 
Subscription”) under the International Offering in accounts in its capacity as the discretionary fund manager managing 
assets on behalf of its ultimate clients (the “Bosera AM Underlying Clients”).
	
The Bosera AM Underlying Clients include (i) Bosera Global Select Equity Fund SP and (ii) Bosera Hong Kong Equity 
Plus Fund. The ultimate beneficial owner of Bosera Global Select Equity Fund SP is Zhang Lei, who holds 53.67% of the 
equity interest in Bosera Global Select Equity Fund SP. Bosera Hong Kong Equity Plus Fund is an SFC authorized Fund. As 
confirmed by Bosera AM, none of other Bosera AM Underlying Clients hold an interest of 30% or more therein.
	
To the best knowledge of Bosera AM after due enquiry, each of the Bosera AM Underlying Clients is an independent third 
party of the Company, its subsidiaries, Bosera AM, CMS and CMBI and the companies which are members of the same 
group of CMS and CMBI.

<<<PAGE 31>>>
31
(7)	
Fullgoal Funds will subscribe for and hold 66,900 Offer Shares (the “Proposed Fullgoal Subscription”) under the 
International Offering in accounts in its capacity as the discretionary fund manager managing assets on behalf of its 
ultimate clients (the “Fullgoal Underlying Clients”).
	
The Fullgoal Fund Underlying Clients include (i) China Merchants Bank-Fullgoal Hong Kong Equity Select Hybrid Fund 
(QDII), (ii) ICBC Fullgoal China Small & Mid Cap (HK listed) Equity Fund, (iii) ICBC Fullgoal Global Technology & 
Internet Fund, (iv) Cmb-Fullgoal Blue Chip Selected Equity Fund (QDII), (v) Fullgoal Dividend Selected Hybrid Fund, (vi) 
Fullgoal China Opportunities Fund, (vii) Fullgoal China Growth Select Fund and (viii) The University of Hong Kong — 
Hong Kong and China Equity Fund (the “Fullgoal Fund Underlying Clients”). As confirmed by Fullgoal Funds, none of 
Fullgoal Fund Underlying Clients holds an interest of 30% or more.
	
To the best knowledge of Fullgoal Fund after due enquiry, each of the Fullgoal Fund Underlying Clients is an independent 
third party of the Company, its subsidiaries, Fullgoal Funds, Guotai Junan and the companies which are members of the 
same group of Guotai Junan.
(8)	
It is proposed that Haitong AM proposes to subscribe for and hold 6,600 Offer Shares (the “Proposed Haitong AM 
Subscription”) under the International Offering in accounts in its capacity as the discretionary fund manager managing 
assets on behalf of its ultimate clients (the “Haitong AM Underlying Clients”).
	
The Haitong AM Underlying Clients include (i) Haitong Opportunity Fund II S.P. and (ii) Haitong Hong Kong SAR Fund. 
None of Haitong AM Underlying Clients hold an interest of 30% or more.
	
To the best knowledge of Haitong AMs after due enquiry, each of the Haitong AM Underlying Clients is an independent 
third party of the Company, its subsidiaries, Haitong AM, Guotai Junan and the companies which are members of the same 
group of Guotai Junan.
(9)	
It is proposed that ChinaAMC HK proposes to subscribe for and hold 6,600 Offer Shares (the “Proposed ChinaAMC HK 
Subscription”) under the International Offering in accounts in its capacity as the discretionary fund manager managing 
assets on behalf of its ultimate clients (the “ChinaAMC HK Underlying Clients”).
	
The ChinaAMC HK Underlying Clients are the beneficial owners of ChinaAMC China Focus Fund. Except for Manulife 
(International) Limited, none of ChinaAMC HK Underlying Clients hold an interest of 30% or more.
	
To the best knowledge of ChinaAMC HK after due enquiry, each of the ChinaAMC HK Underlying Clients is an independent 
third party of the Company, its subsidiaries, ChinaAMC HK, CSB and the companies which are members of the same group 
of CSB.
(10)	 It is proposed that ChinaAMC proposes to subscribe for and hold 66,900 Offer Shares (the “Proposed ChinaAMC 
Subscription”) under the International Offering in accounts in its capacity as the discretionary fund manager managing 
assets on behalf of its ultimate clients (the “ChinaAMC Underlying Clients”).
	
The ChinaAMC Underlying Clients are the beneficial owners of Huaxia New Era Renminbi (華夏新時代人民幣), Huaxia 
Global Select Renminbi (華夏全球精選人民幣), KWI China Global Vision Fund, Huaxia Hong Kong Stocks Frontier 
Economy Hybrid (QDII) (華夏港股前沿經濟混合(QDII)), Huaxia Mobile Internet Hybrid (QDII) (華夏移動互聯混合
(QDII)) and Huaxia Greater China Enterprise Selection (華夏大中華企業精選). None of ChinaAMC Underlying Clients 
hold an interest of 30% or more.
	
To the best knowledge of ChinaAMC after due enquiry, each of the ChinaAMC Underlying Clients is an independent third 
party of the Company, its subsidiaries, ChinaAMC, CSB and the companies which are members of the same group of CSB.
(11)	 It is proposed that BOCOMI AM proposes to subscribe for and hold 18,900 Offer Shares (the “Proposed BOCOMI AM 
Subscription”) under the International Offering in accounts in its capacity as the discretionary fund manager managing 
assets on behalf of its ultimate clients (the “BOCOMI AM Underlying Clients”).
	
The BOCOMI AM Underlying Clients are Wu Xiaomin, Jian Weiwen and Chen Qinghua.
	
To the best knowledge of BOCOMI AM after due enquiry, each of the BOCOMI AM Underlying Clients is an independent 
third party of the Company, its subsidiaries, BOCOMI AM, BOCOMI Securities and the companies which are members of 
the same group of BOCOMI Securities.

<<<PAGE 32>>>
32
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the 
“Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy or 
completeness and expressly disclaim any liability whatsoever for any loss howsoever arising from 
or in reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer or 
solicitation to purchase or subscribe for securities in the United States. The securities mentioned 
herein have not been, and will not be, registered under the United States Securities Act of 1933, 
as amended (the “U.S. Securities Act”) or any state securities laws in the United States and may 
not be offered, sold, pledged or transferred within the United States or to, or for the account or 
benefit of U.S. persons (as defined in Regulation S under the U.S. Securities Act) or United States 
persons (United States person as defined in 31 CFR Part 850.229, the final rule that implements 
Executive Order 14105 and became effective in January 2025), except in transactions exempt 
from, or not subject to, the registration requirements of the U.S. Securities Act. The Offer Shares 
are being offered and sold outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated December 30, 2025 issued by the Company 
for detailed information about the Global Offering described below before deciding whether or 
not to invest in the H Shares thereby being offered.
*  Potential investors of the Offer Shares should note that the Sole Sponsor and the Sponsor-OC (for itself and on behalf 
of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the paragraph headed “Underwriting 
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Hong Kong Underwriting Agreement — 
Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is 
currently expected to be on January 8, 2026).
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering (assuming no exercise of the Over-
allotment Option), the total number of the H Shares held by the public represents approximately 
46.73% of the total issued share capital of the Company, which is higher than the prescribed 
percentage of H Shares required to be held in public hands of 10.00% under Rule 19A.13A(1) of the 
Listing Rules calculated based on the Offer Price of HK$116.20 per H Share, thereby satisfying the 
public float requirement under Rule 19A.13A(1) of the Listing Rules.

<<<PAGE 33>>>
33
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the Shares of the Company at the time of Listing. Based on the 
Offer Price of HK$116.20 per H Share, the Company satisfies the free float requirement under Rule 
19A.13C(1)(b) of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering, (i) the 
three largest public Shareholders do not hold more than 50% of the H Shares in public hands at the 
time of Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; (ii) there will not be 
any new substantial Shareholder (as defined in the Listing Rules) of the Company; (iii) no placee 
will, individually, be placed more than 10% of the enlarged issued share capital of the Company 
immediately after the Global Offering; and (iv) there will be at least 300 Shareholders at the time of 
Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Thursday, January 
8, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting — Underwriting Arrangements 
and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade the H Shares on the basis of publicly available allocation 
details prior to the receipt of H Share certificates or prior to the H Share certificates becoming valid 
evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Thursday, 
January 8, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Thursday, January 8, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 100 H Shares each, and the stock code of the H Shares will be 
2513.
By order of the Board
Knowledge Atlas Technology Joint Stock Company Limited
北京智譜華章科技股份有限公司
Dr. Liu Debing
Chairman of the Board and executive Director
Hong Kong, January 7, 2026
As at the date of this announcement, the Board comprises: (i) Dr. Liu Debing, Dr. Zhang Peng, Ms. Zhang Xiaohan as 
executive directors; (ii) Dr. Li Juanzi, Mr. Li Jiaqing and Mr. Wang Meng as non-executive directors; and (iii) Dr. Yang Qiang, 
Dr. Xie Deren and Mr. Tang Ying as independent non-executive directors.
