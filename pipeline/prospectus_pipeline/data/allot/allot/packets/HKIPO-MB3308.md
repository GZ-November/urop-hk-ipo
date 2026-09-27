# 配发结果公告抽取任务：3308.HK ZHONGJI INNOLIGHT CO., LTD. - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**29/07/2026 22:16**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0729/2026072901629.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3308.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
ZHONGJI INNOLIGHT CO., LTD.
中際旭創股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE 
AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated July 22, 2026 (the “Prospectus”) issued by 
Zhongji InnoLight Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
H Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
3308
Stock short name
ZJ INNOLIGHT
Dealings commencement date
July 30, 2026*
* see note at the end of the announcement
Price Information
Final Offer Price
HK$980.00
Maximum Offer Price
HK$1,010.00
Offer Price Adjustment exercised
N/A
Offer Shares and Share Capital
Number of Offer Shares (subject to the Over-allotment 
Option)
54,500,000
Number of Offer Shares in Hong Kong Public Offering
5,450,000
Number of Offer Shares in International Offering (subject 
to the Over-allotment Option)
49,050,000
Number of issued Shares upon Listing (before any exercise 
of the Over-allotment Option)
1,169,734,641

<<<PAGE 2>>>
2
Over-allocation
No. of Offer Shares over-allocated
8,175,000
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$53,410 million
 Less: Estimated listing expenses payable based on Final 
  Offer Price
HK$(519) million
Net proceeds
HK$52,891 million
Note: Gross proceeds refer to the amount to which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” in the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” in the Prospectus 
on a pro rata basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
62,731
No. of successful applications
51,199
Subscription level
16.84 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong 
Public Offering
5,450,000
Final no. of Offer Shares under the Hong Kong Public 
Offering
5,450,000
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering
10%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can refer to 
www.eipo.com.hk/eIPOAllotment to perform a search by identification number or www.eipo.com.hk/eIPOAllotment 
for the full list of allottees.

<<<PAGE 3>>>
3
INTERNATIONAL OFFERING
No. of placees
549
Subscription Level
9.73 times
No. of Offer Shares initially available under the International 
Offering
49,050,000
Final no. of Offer Shares under the International Offering
49,050,000
% of Offer Shares under the International Offering to the 
Global Offering
90.0%
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a 
waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit H Shares in the International Offering to be placed to certain Existing Minority 
Shareholders and/or their close associates and (b) a consent under Chapter 4.15 of the Guide for 
New Listing Applicants to permit the Company to, among other things, allocate further H Shares in 
the International Offering to certain Cornerstone Investors and/or their close associates, (i) none of 
the Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, substantial Shareholders, 
existing Shareholders of the Company or any of its subsidiaries or their respective close associates; 
and (ii) none of the placees and the public who have purchased the Offer Shares are accustomed 
to taking instructions from the Company, any of the Directors, chief executive of the Company, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or their 
respective close associates in relation to the acquisition, disposal, voting or other disposition of H 
Shares registered in his/her/its name or otherwise held by him/her/it.

<<<PAGE 4>>>
4
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of
Offer Shares
allocated Note 1
Approximate % 
of Offer Shares 
after the Global
Offering (assuming 
the Over-allotment 
Option is not 
exercised) Note 1
Approximate % 
of total issued 
share capital 
after the Global
Offering (assuming 
the Over-allotment 
Option is not 
exercised) Note 1
Existing 
Shareholders 
or their close 
associates
Taibai
1,895,650
3.48%
0.16%
Yes
True Light
473,900
0.87%
0.04%
Yes
HHLRA
2,369,550
4.35%
0.20%
No
JPMIMI
1,212,400
2.22%
0.10%
Yes
JPMAMAPL
762,200
1.40%
0.07%
Yes
BlackRock
1,974,600
3.62%
0.17%
Yes
YF Capital
1,184,750
2.17%
0.10%
No
Aspex
1,184,750
2.17%
0.10%
No
ADIA
789,850
1.45%
0.07%
Yes
Wellington
789,850
1.45%
0.07%
Yes
Perseverance Asset 
Management
789,850
1.45%
0.07%
Yes
Indus Funds
789,850
1.45%
0.07%
No
Mirae Investors
789,850
1.45%
0.07%
Yes
NGS Super Fund
789,850
1.45%
0.07%
No
Bain Capital
789,850
1.45%
0.07%
No
CPE
789,850
1.45%
0.07%
No
Boyu Capital
789,850
1.45%
0.07%
Yes
IDG Capital
710,850
1.30%
0.06%
No
Ninety One Asia
78,950
0.14%
0.01%
Yes
WT Asset Management
789,850
1.45%
0.07%
Yes
CloudAlpha Capital
789,850
1.45%
0.07%
No
Tairen
789,850
1.45%
0.07%
No
Hao Funds
789,850
1.45%
0.07%
No

<<<PAGE 5>>>
5
Investor
No. of
Offer Shares
allocated Note 1
Approximate % 
of Offer Shares 
after the Global
Offering (assuming 
the Over-allotment 
Option is not 
exercised) Note 1
Approximate % 
of total issued 
share capital 
after the Global
Offering (assuming 
the Over-allotment 
Option is not 
exercised) Note 1
Existing 
Shareholders 
or their close 
associates
Janchor Funds
789,850
1.45%
0.07%
No
Alibaba
394,900
0.72%
0.03%
No
Tencent
394,900
0.72%
0.03%
No
CPP Investments
394,900
0.72%
0.03%
Yes
Oaktree
394,900
0.72%
0.03%
No
CP Black Dragon
394,900
0.72%
0.03%
No
CTFE
394,900
0.72%
0.03%
No
Athos Capital
394,900
0.72%
0.03%
No
TAL Funds
394,900
0.72%
0.03%
No
Burkehill
394,900
0.72%
0.03%
No
General Atlantic
394,900
0.72%
0.03%
No
Huadeng Technology
394,900
0.72%
0.03%
No
Total
27,249,400
50.00%
2.33%
Notes:
1. 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in 
the Prospectus.
2. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering (assuming the Over-allotment Option is not exercised).
3. 
In addition to the Offer Shares subscribed for as Cornerstone Investors, certain Cornerstone Investors and/or 
their close associates were allocated further Offer Shares as placees in the International Offering. Please refer 
to the section headed “Allotment Results Details – International Offering – Allottees with Waivers/Consents 
Obtained” in this announcement for details. Only the Offer Shares subscribed for as Cornerstone Investors 
are subject to lock-up restrictions as indicated below. For details, please refer to the section headed “Lock-up 
Undertakings – Cornerstone Investors” in this announcement.

<<<PAGE 6>>>
6
Allottees with Waivers/Consents Obtained
Investor
No. of 
Offer Shares 
allocated Note 1
% of total issued 
H Shares after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) Note 5
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of 
the Placing Guidelines in relation to subscription for H Shares by Existing Minority Shareholders holding more than 1% 
of the issued share capital of the Company immediately prior to the completion of the Global Offering and/or their close 
associates Note 2
Fullgoal Asset 
Management (HK) 
Limited (“Fullgoal HK”) 
100,350
0.18%
0.01%
An existing Shareholder and/
or its close associates
Fullgoal Fund 
Management Co., Ltd. 
(“Fullgoal Fund”) 
122,650
0.23%
0.01%
An existing Shareholder and/
or its close associates
GF International 
Investment Management 
Limited (“GF 
International”)
96,200
0.18%
0.01%
An Existing Shareholder and/
or its close associates
Allottee with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocation of Offer Shares to certain Cornerstone Investors Note 3
ADIA
200,000
0.37%
0.02%
A Cornerstone Investor and 
an existing Shareholder 
and/or its close associates 
Note 2
MAS KR
27,200
0.05%
0.002%
A Cornerstone InvestorNote 2
MAS HK
35,000
0.06%
0.003%
A Cornerstone InvestorNote 2
MAGI HK
15,500
0.03%
0.001%
A Cornerstone InvestorNote 2
Boyu
55,150.00
0.10%
0.01%
A close associate of 
Cornerstone Investor and 
an existing Shareholder 
and/or its close associates 
Note 2
Boyu Capital Investment 
Management Co., 
Ltd ("Boyu Capital 
Investment")
22,550.00
0.04%
0.002%
A close associate of 
Cornerstone Investor and 
an existing Shareholder 
and/or its close associates 
Note 2
WT Asset Management 
77,700
0.14%
0.01%
A Cornerstone InvestorNote 2

<<<PAGE 7>>>
7
Investor
No. of 
Offer Shares 
allocated Note 1
% of total issued 
H Shares after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) Note 5
Relationship
JPMAMAPL
564,000
1.03%
0.05%
A Cornerstone Investor and a 
close associate of another  
Cornerstone InvestorNote 2
Wellington
564,000
1.03%
0.05%
A Cornerstone InvestorNote 2
BlackRock
564,000
1.03%
0.05%
A Cornerstone InvestorNote 2
Perseverance
77,700
0.14%
0.01%
A Cornerstone InvestorNote 2
CPP Investments
39,000
0.07%
0.003%
A Cornerstone InvestorNote 2
Aspex
564,000
1.03%
0.05%
A Cornerstone Investor Note 2
Janchor
77,700
0.14%
0.01%
A Cornerstone Investor Note 2
Burkehill
39,000
0.07%
0.003%
A Cornerstone Investor Note 2
General Atlantic
39,000
0.07%
0.003%
A Cornerstone Investor Note 2
New Golden Future 
Limited ("New Golden")
38,900
0.07%
0.003%
A close associate of its 
Cornerstone InvestorNote 2
Strong Media Limited
800
0.001%
0.0001%
A close associate of its 
Cornerstone InvestorNote 2
CPE 
77,700
0.14%
0.01%
A Cornerstone InvestorNote 2
Hao Advisors 
77,700
0.14%
0.01%
A Cornerstone InvestorNote 2
Alibaba Investment 
236,000
0.43%
0.02%
A Cornerstone InvestorNote 2
Huadeng Technology 
39,000
0.07%
0.003%
A Cornerstone InvestorNote 2
Trivest
39,000
0.07%
0.003%
A Cornerstone InvestorNote 2
HHLRA
472,550
0.87%
0.04%
A Cornerstone InvestorNote 2
CP Black Dragon
236,000
0.43%
0.02%
A Cornerstone InvestorNote 2
Tairen
77,700
0.14%
0.01%
A Cornerstone InvestorNote 2
Indus Fund
39,000
0.07%
0.003%
A Cornerstone InvestorNote 2
CloudAlpha Capital
77,700
0.14%
0.01%
A Cornerstone InvestorNote 2

<<<PAGE 8>>>
8
Investor
No. of 
Offer Shares 
allocated Note 1
% of total issued 
H Shares after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) Note 5
Relationship
CTFE
39,000
0.07%
0.003%
A Cornerstone InvestorNote 2
Athos Capital
39,000
0.07%
0.003%
A Cornerstone InvestorNote 2
E Fund Management 
Co., Ltd. (“E Fund 
Management”) and E 
Fund Management (Hong 
Kong) Co., Limited (“E 
Fund Hong Kong”)
223,000
0.41%
0.02%
An existing Shareholder and/
or its close associates
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations to connected client Note 4
Shanghai Guotai 
Haitong Securities Asset 
Management Co., Ltd. 
(“Shanghai GTHT”)
16,000
0.03%
0.001%
Connected client as placee
China International 
Capital Corporation 
Limited (“CICC”)
1,600
0.003%
0.0001%
Connected client as placee
China Southern Asset 
Management Co., Ltd. 
(“China Southern”) 
67,000
0.12%
0.01%
Connected client as placee
UBS Asset Management 
(Singapore) Ltd. (“UBS 
AM Singapore”) 
132,000
0.24%
0.01%
Connected client as placee
HSBC Global Asset 
Management (Hong Kong) 
Limited (“HSBC AM 
HK”) 
390,000 
0.72%
0.03%
Connected client as placee
ABCI Asset Management 
Limited (“ABCI AM”)
3,900
0.01%
0.0003%
Connected client as placee

<<<PAGE 9>>>
9
Investor
No. of 
Offer Shares 
allocated Note 1
% of total issued 
H Shares after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) Note 5
Relationship
GF International
96,200
0.18%
0.01%
Connected client as placee
Value Partners Hong 
Kong Limited (“VPHK”) 
and Value Partners 
Limited (“VPL”) 
(collectively as “Value 
Partners”)
39,000
0.07%
0.003%
Connected client as placee
E Fund Management
174,000
0.32%
0.01%
Connected client as placee
E Fund Hong Kong
49,000
0.09%
0.004%
Connected client as placee
GF Securities Asset 
Management (Guangdong) 
Co., Ltd. (“GF Securities 
AM”)
61,000
0.11%
0.01%
Connected client as placee
Bosera Asset Management 
(International) Co., 
Limited (“Bosera AM”)
67,000
0.12%
0.01%
Connected client as placee
China Asset Management 
(Hong Kong) Limited 
(“China AMC HK”)
20,000
0.04%
0.002%
Connected client as placee
China Asset Management 
Co., Ltd. (“China AMC”)
135,000
0.25%
0.01%
Connected client as placee
China Universal Asset 
Management Company 
Limited (“CUAM”)
2,950
0.01%
0.0003%
Connected client as placee
China Universal Asset 
Management (Hong 
Kong) Company Limited 
(“CUAM HK”)
92,050
0.17%
0.01%
Connected client as placee
Fullgoal HK
100,350
0.18%
0.01%
Connected client as placee

<<<PAGE 10>>>
10
Investor
No. of 
Offer Shares 
allocated Note 1
% of total issued 
H Shares after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) Note 5
Relationship
Fullgoal Fund
122,650
0.23%
0.01%
Connected client as placee
Notes:
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the Global Offering. 
The figures assume that the Over-allotment Option is not exercised.
2. 
The Stock Exchange has granted a waiver from strict compliance with the requirements under Rule 10.04 of the Listing Rules and consent 
under Paragraph 1C(2) of the Placing Guidelines to permit H Shares in the International Offering to be placed to certain Existing Minority 
Shareholders. Please refer to the section headed “Waivers – Allocation of H Shares to Existing Minority Shareholders and/or Their Close 
Associates” in the Prospectus for details.
To the best knowledge, information and belief of the Company after due enquiry, details of the allocations to the Existing Minority Shareholder 
holding more than 1% of the issued share capital of the Company immediately prior to the completion of the Global Offering have been disclosed 
in this announcement.
3. 
The number of Offer Shares allocated to such investors only represents the number of Offer Shares allocated to the investors as placees in the 
International Offering. For allocations of Offer Shares to the investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details – International Offering – Cornerstone Investors” in this announcement. For details of the consent under Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations of further H Shares to the Cornerstone Investors, please refer to the section headed 
“Allottees with Waivers/Consents Obtained – Allottee with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants 
in relation to allocation of Offer Shares to certain Cornerstone Investors” in this announcement.
4. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation 
to allocations to connected clients, please refer to the section headed “Others/Additional Information – Placing to connected clients with a prior 
consent under paragraph 1C(1) of the Placing Guidelines” in this announcement.
5. 
Not taking into account any A Shares held by the relevant investors. The figures are based on assumption that the Over-allotment Option is not 
exercised.

<<<PAGE 11>>>
11
LOCK-UP UNDERTAKINGS
Cornerstone Investors
Name
Number of H 
Shares held
in the Company 
subject
to lock-up
undertakings 
upon
Listing
Approximate % 
of total issued H 
Shares after the 
Global Offering 
subject to
lock-up 
undertakings
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1
Approximate 
% of
shareholding
in the
Company
subject to
lock-up
undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1
Last day subject 
to the lock-up 
undertakings Note 2
Taibai
1,895,650
3.48%
0.16%
January 29, 2027
True Light
473,900
0.87%
0.04%
January 29, 2027
HHLRA
2,369,550
4.35%
0.20%
January 29, 2027
JPMIMI
1,212,400
2.22%
0.10%
January 29, 2027
JPMAMAPL
762,200
1.40%
0.07%
January 29, 2027
BlackRock
1,974,600
3.62%
0.17%
January 29, 2027
YF Capital
1,184,750
2.17%
0.10%
January 29, 2027
Aspex
1,184,750
2.17%
0.10%
January 29, 2027
ADIA
789,850
1.45%
0.07%
January 29, 2027
Wellington
789,850
1.45%
0.07%
January 29, 2027
Perseverance Asset Management
789,850
1.45%
0.07%
January 29, 2027
Indus Funds
789,850
1.45%
0.07%
January 29, 2027
Mirae Investors
789,850
1.45%
0.07%
January 29, 2027
NGS Super Fund
789,850
1.45%
0.07%
January 29, 2027
Bain Capital
789,850
1.45%
0.07%
January 29, 2027
CPE
789,850
1.45%
0.07%
January 29, 2027
Boyu Capital
789,850
1.45%
0.07%
January 29, 2027
IDG Capital
710,850
1.30%
0.06%
January 29, 2027
Ninety One Asia
78,950
0.14%
0.01%
January 29, 2027
WT Asset Management
789,850
1.45%
0.07%
January 29, 2027
CloudAlpha Capital
789,850
1.45%
0.07%
January 29, 2027

<<<PAGE 12>>>
12
Name
Number of H 
Shares held
in the Company 
subject
to lock-up
undertakings 
upon
Listing
Approximate % 
of total issued H 
Shares after the 
Global Offering 
subject to
lock-up 
undertakings
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1
Approximate 
% of
shareholding
in the
Company
subject to
lock-up
undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1
Last day subject 
to the lock-up 
undertakings Note 2
Tairen
789,850
1.45%
0.07%
January 29, 2027
Hao Funds
789,850
1.45%
0.07%
January 29, 2027
Janchor Funds
789,850
1.45%
0.07%
January 29, 2027
Alibaba
394,900
0.72%
0.03%
January 29, 2027
Tencent
394,900
0.72%
0.03%
January 29, 2027
CPP Investments
394,900
0.72%
0.03%
January 29, 2027
Oaktree
394,900
0.72%
0.03%
January 29, 2027
CP Black Dragon
394,900
0.72%
0.03%
January 29, 2027
CTFE
394,900
0.72%
0.03%
January 29, 2027
Athos Capital
394,900
0.72%
0.03%
January 29, 2027
TAL Funds
394,900
0.72%
0.03%
January 29, 2027
Burkehill
394,900
0.72%
0.03%
January 29, 2027
General Atlantic
394,900
0.72%
0.03%
January 29, 2027
Huadeng Technology
394,900
0.72%
0.03%
January 29, 2027
Total
27,249,400
50.00%
2.33%
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
(2) 
In accordance with the relevant Cornerstone Investment Agreements, the required lock-up period commences 
from (and inclusive of) the Listing Date and ending on (and inclusive of) the date falling six (6) months 
after the Listing Date (being January 29, 2027). The Cornerstone Investors will cease to be prohibited from 
disposing of or transferring H Shares subscribed pursuant to the relevant Cornerstone Investment Agreements 
after the indicated date.

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
(assuming 
the Over-
allotment
Option is not
exercised)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised and 
new H 
Shares 
are issued)
Allotment 
as % of 
total Offer 
Shares 
(assuming 
the Over-
Allotment
Option is not
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
H Shares 
are issued)
Number of 
H Shares 
held upon 
Listing
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment
Option is not
exercised)
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
H Shares 
are issued)
Top 1
2,842,100
5.79%
4.97%
5.21%
4.53%
2,842,100
0.24%
0.24%
Top 5
13,236,300
26.99%
23.13%
24.29%
21.12%
13,236,300
1.13%
1.12%
Top 10
20,922,750
42.66%
36.56%
38.39%
33.38%
20,922,750
1.79%
1.78%
Top 25
33,450,100
68.20%
58.45%
61.38%
53.37%
33,450,100
2.86%
2.84%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment
Option is not
exercised)
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
H Shares 
are issued)
Allotment 
as % of 
total Offer 
Shares 
(assuming 
the Over-
allotment
Option is not
exercised)
Allotment 
as % of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised 
and new 
H Shares 
are issued)
Number of 
H Shares 
held upon 
Listing
% of total 
issued 
H share 
capital upon 
Listing 
(assuming 
the Over-
allotment
Option is not
exercised)
% of total 
issued 
H share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised and 
new 
H Shares 
are issued)
Top 1
2,842,100
5.79%
4.97%
5.21%
4.53%
2,842,100
5.21%
4.53%
Top 5
13,236,300
26.99%
23.13%
24.29%
21.12%
13,236,300
24.29%
21.12%
Top 10
20,922,750
42.66%
36.56%
38.39%
33.38%
20,922,750
38.39%
33.38%
Top 25
33,450,100
68.20%
58.45%
61.38%
53.37%
33,450,100
61.38%
53.37%
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
(assuming 
the Over-
allotment
Option is not
exercised)
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
H Shares 
are issued)
Allotment 
as % of 
total Offer 
Shares 
(assuming 
the Over-
allotment
Option is not
exercised)
Allotment 
as % of 
total Offer 
Shares 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised 
and new 
H Shares 
are issued)
Number of 
H Shares 
held upon 
Listing
Number 
of Shares 
held upon 
Listing#
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment
Option is not
exercised)
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
H Shares 
are issued)
Top 1
–
–
–
–
–
–
121,440,135
10.38%
10.31%
Top 5
–
–
–
–
–
–
326,020,786
27.87%
27.68%
Top 10
144,200
0.29%
0.25%
0.26%
0.23%
144,200
373,631,896
31.94%
31.72%
Top 25
3,672,650
7.49%
6.42%
6.74%
5.86%
3,672,650
440,619,836
37.67%
37.41%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon 
Listing.
# 
Among the top 25 placees, certain placees are also existing Shareholders. To the best knowledge, information 
and belief of the Company after due enquiry, details of the allocations to the Existing Minority Shareholder 
holding more than 1% of the issued share capital of the Company immediately prior to the completion of the 
Global Offering have been disclosed in this announcement. Please refer to the section headed “Allottees with 
Waivers/Consents Obtained – Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules 
and consent under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by Existing 
Minority Shareholders holding more than 1% of the issued share capital of the Company immediately prior 
to the completion of the Global Offering and/or their close associates” in this announcement. For the top 25 
placees who are also existing shareholders holding less than 0.05% of the issued share capital of the Company 
immediately prior to the completion of the Global Offering, the number of A Shares held by them is not counted 
into the number of Shares held upon Listing.

<<<PAGE 15>>>
15
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, 62,731 valid applications 
made by the public will be conditionally allocated on the basis set out below:
Number of 
H Shares 
applied for
Number of 
valid 
applications
Basis of allocation/
ballot
Approximate % 
allotted of the total 
no. of H Shares 
applied for
POOL A
50
23,612
16,528 out of 23,612 to receive 50 Shares
70.00%
100
6,988
4,892 out of 6,988 to receive 50 Shares
35.00%
150
3,598
2,699 out of 3,598 to receive 50 Shares
25.00%
200
3,047
2,438 out of 3,047 to receive 50 Shares
20.00%
250
2,139
1,925 out of 2,139 to receive 50 Shares
18.00%
300
1,720
1,548 out of 1,720 to receive 50 Shares
15.00%
350
1,099
1,000 out of 1,099 to receive 50 Shares
13.00%
400
1,149
1,057 out of 1,149 to receive 50 Shares
11.50%
450
899
850 out of 899 to receive 50 Shares
10.51%
500
3,088
2,934 out of 3,088 to receive 50 Shares
9.50%
600
1,231
1,182 out of 1,231 to receive 50 Shares
8.00%
700
779
764 out of 779 to receive 50 Shares
7.01%
800
943
50 Shares
6.25%
900
659
50 Shares plus 65 out of 659 to receive 
additional 50 Shares
6.10%
1,000
3,641
50 Shares plus 364 out of 3,641 to receive 
additional 50 Shares
5.50%
2,000
1,967
100 Shares
5.00%
3,000
1,205
100 Shares plus 1,064 out of 1,205 to 
receive additional 50 Shares
4.80%
4,000
1,201
150 Shares
3.75%
58,965
Total number of Pool A successful applicants: 47,433

<<<PAGE 16>>>
16
Number of 
H Shares 
applied for
Number of 
valid 
applications
Basis of allocation/
ballot
Approximate % 
allotted of the total 
no. of H Shares 
applied for
POOL B
5,000
1,311
300 Shares
6.00%
6,000
546
350 Shares
5.83%
7,000
283
400 Shares
5.71%
8,000
217
450 Shares
5.63%
9,000
146
500 Shares
5.56%
10,000
632
550 Shares
5.50%
20,000
231
1,000 Shares
5.00%
30,000
105
1,450 Shares
4.83%
40,000
78
1,750 Shares
4.38%
50,000
49
2,000 Shares
4.00%
60,000
25
2,250 Shares
3.75%
70,000
22
2,500 Shares
3.57%
80,000
13
2,800 Shares
3.50%
90,000
10
3,100 Shares
3.44%
100,000
60
3,300 Shares
3.30%
200,000
17
6,000 Shares
3.00%
300,000
9
8,000 Shares
2.67%
400,000
3
10,100 Shares
2.53%
500,000
2
12,600 Shares
2.52%
1,000,000
1
25,000 Shares
2.50%
1,500,000
1
35,250 Shares
2.35%
2,000,000
5
45,000 Shares
2.25%
3,766
Total number of Pool B successful applicants: 3,766
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 17>>>
17
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.
OTHER/ADDITIONAL INFORMATION
Allocation of H Shares to Existing Minority Shareholders and their close associates
The Company has applied for, and the Hong Kong Stock Exchange has granted, a waiver from 
strict compliance with the requirements under Rule 10.04 and consent under Paragraph 1C(2) of 
Appendix F1 to the Listing Rules to permit H Shares in the International Offering to be placed 
to certain existing minority Shareholders who (i) hold less than 5% of the total voting rights in 
our Company prior to the completion of the Global Offering and (ii) are not and will not become 
(upon the completion of the Global Offering) core connected persons of our Company or the close 
associates of any such core connected person (together, the “Existing Minority Shareholders”) 
and/or their close associates, subject to the conditions as follows:
(i) 
each of them to whom the Company may allocate the H Shares in the International Offering 
holds less than 5% of the total voting rights in the Company before Listing;
(ii) each of them is not, and will not be, a core connected person of the Company or any close 
associate of any such core connected person immediately prior to or following the Global 
Offering;
(iii) each of them does not have the right to appoint a Director and/or have any other special 
rights;
(iv) allocation to the Existing Minority Shareholders or their close associates will not affect the 
Company’s ability to satisfy the public float requirement as prescribed by the Hong Kong 
Stock Exchange under Rule 19A.13A of the Listing Rules; and
(v) 
no preferential treatment is given to the Existing Minority Shareholders or their close 
associates, nor are they in a position to exert influence on the Company to obtain actual or 
perceived preferential treatment in the allocation as a cornerstone investor (other than the 
assured entitlement for a cornerstone investor) and details of the allocation to the Existing 
Minority Shareholders holding more than 1% of the issued share capital of the Company 
immediately prior to the completion of the Global Offering will be disclosed in this 
announcement.

<<<PAGE 18>>>
18
Please refer to the section headed “Waivers – Allocation of H Shares to Existing Minority 
Shareholders and/or Their Close Associates” in the Prospectus for further details of the waiver and 
consent.
Each of the Joint Sponsors and the Company has provided the required confirmations as elaborated 
in the Prospectus. In particular, as the Company’s A Shares are listed on the ChiNext Market of 
the Shenzhen Stock Exchange since 2012, the Company has a highly extensive base of existing 
Shareholders and disclosure of details of allocations to all Existing Minority Shareholders will not 
be meaningful to investors, the proposed disclosure threshold, i.e. condition (v) of the waiver and 
consent which provides that details of the allocation to the Existing Minority Shareholders holding 
more than 1% of the issued share capital of the Company immediately prior to the completion of 
the Global Offering will be disclosed in this announcement, is appropriate.
All allocations of Offer Shares to the Existing Minority Shareholders are in compliance with all 
the conditions under the waiver and consent granted by the Stock Exchange.
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines. Please refer to the section headed 
“Allotment Results Details — International Offering — Allottees with Waivers/Consents Obtained” 
in this announcement for details.
The Company has applied to the Hong Kong Stock Exchange for, and the Hong Kong Stock 
Exchange has granted, a consent under paragraph 1C(1) of the Placing Guidelines to permit the 
Company to allocate such Offer Shares in the International Offering to the connected clients as 
placees. The allocation of Offer Shares to such connected clients is in compliance with all the 
conditions under the consent granted by the Stock Exchange.

<<<PAGE 19>>>
19
Details of the placement to connected clients are set out below:
No.
Connected 
Distributor
Connected Client
Relationship with 
the Connected 
Distributor
Whether the 
connected
client will hold 
the beneficial 
interests of the
Offer Shares 
on a non-
discretionary
basis or
discretionary 
basis for
independent 
third parties
Whether the 
Connected 
Client is a 
collective 
investment 
scheme 
which is not 
authorised 
by the 
SFC or is 
expected 
to hold the 
Offer Shares 
on behalf of 
such scheme
Number of 
Offer Shares 
allocated 
to the 
Connected 
Client
Approximate 
percentage 
of total 
number of 
Offer Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
percentage 
of total 
Shares 
in issue 
immediately 
following the 
completion 
of Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
1.
Guotai Junan 
Securities (Hong 
Kong) Limited 
(“GTJA Securities”)
Shanghai GTHT 
acting as a qualified 
domestic institutional 
investor for ICBC 
Wealth Management 
Co., Ltd. (“ICBC 
Wealth”)) (Note 1)
Shanghai GTHT is a 
member of the same 
group of companies 
as GTJA Securities 
and Haitong 
International.
Non-
discretionary
No
16,000
0.03%
0.001%
2.
Haitong International 
Securities Company 
Limited (“Haitong 
International”)
3.
China International 
Capital Corporation 
Hong Kong 
Securities Limited 
(“CICCHKS”)
CICC (stock code: 
601995.SH, 3908.
HK) acting as a 
qualified domestic 
institutional investor 
for ICBC Wealth 
(Note 2)
CICCHKS is a 
member of the same 
group of companies 
as CICC.
Non-
discretionary
No
1,600
0.003%
0.0001%
4.
Huatai Financial 
Holdings (Hong 
Kong) Limited 
(“HTFH”)
China Southern 
(Note 3)
China Southern is a 
member of the same 
group of companies 
as HTFH.
Discretionary
No
67,000
0.12%
0.01%
5.
UBS AG Singapore 
Branch (“UBS AG 
Singapore” ) and 
UBS AG Hong Kong 
Branch (“UBS AG 
Hong Kong”)
UBS AM Singapore 
(Note 4)
UBS AM Singapore is 
a member of the same 
group of companies 
as UBS AG Singapore 
and UBS AG Hong 
Kong.
Discretionary
No
132,000
0.24%
0.01%
6.
The Hongkong and 
Shanghai Banking 
Corporation Limited 
(“HSBC Bank”)
HSBC AM HK 
(Note 5)
HSBC AM HK is a 
member of the same 
group of companies 
as HSBC Bank.
Discretionary
No
390,000
0.72%
0.03%

<<<PAGE 20>>>
20
No.
Connected 
Distributor
Connected Client
Relationship with 
the Connected 
Distributor
Whether the 
connected
client will hold 
the beneficial 
interests of the
Offer Shares 
on a non-
discretionary
basis or
discretionary 
basis for
independent 
third parties
Whether the 
Connected 
Client is a 
collective 
investment 
scheme 
which is not 
authorised 
by the 
SFC or is 
expected 
to hold the 
Offer Shares 
on behalf of 
such scheme
Number of 
Offer Shares 
allocated 
to the 
Connected 
Client
Approximate 
percentage 
of total 
number of 
Offer Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
percentage 
of total 
Shares 
in issue 
immediately 
following the 
completion 
of Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
7.
ABCI Capital Limited 
(“ABCI Capital”) 
and ABCI Securities 
Company Limited 
(“ABCI Securities”)
ABCI AM (Note 6)
ABCI Capital and 
ABCI Securities are 
group companies 
within the same 
group.
Discretionary
No
3,900
0.01%
0.0003%
8.
CITIC Securities 
Brokerage (HK) 
Limited (“CSB”)
China AMC HK 
(Note 7)
China AMC HK is a 
member of the same 
group of companies 
as CSB.
Discretionary
No
20,000
0.04%
0.002%
9.
China AMC
 (Note 8)
China AMC is a 
member of the same 
group of companies 
as CSB.
Discretionary
No
135,000
0.25%
0.01%
10.
Orient Securities 
(Hong Kong) Limited 
(“Orient”)
CUAM (Note 9)
CUAM is a member 
of the same group of 
companies as Orient.
Discretionary
No
2,950
0.01%
0.0003%
11.
CUAM HK
 (Note 10)
CUAM HK is a 
member of the same 
group of companies 
as Orient.
Discretionary
Yes. Please 
refer to Note 
10.
92,050
0.17%
0.01%

<<<PAGE 21>>>
21
No.
Connected 
Distributor
Connected Client
Relationship with 
the Connected 
Distributor
Whether the 
connected
client will hold 
the beneficial 
interests of the
Offer Shares 
on a non-
discretionary
basis or
discretionary 
basis for
independent 
third parties
Whether the 
Connected 
Client is a 
collective 
investment 
scheme 
which is not 
authorised 
by the 
SFC or is 
expected 
to hold the 
Offer Shares 
on behalf of 
such scheme
Number of 
Offer Shares 
allocated 
to the 
Connected 
Client
Approximate 
percentage 
of total 
number of 
Offer Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
percentage 
of total 
Shares 
in issue 
immediately 
following the 
completion 
of Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
12.
GF Securities (Hong 
Kong) Brokerage 
Limited (“GF 
Securities (Hong 
Kong) Brokerage”)
GF International 
(Note 11)
GF International is a 
member of the same 
group of companies 
as GF Securities 
(Hong Kong) 
Brokerage.
Discretionary
No
96,200
0.18%
0.01%
13.
VPHK and VPL 
(Note 12)
Value Partners is a 
member of the same 
group of companies 
as GF Securities 
(Hong Kong) 
Brokerage.
Discretionary
Yes. Please 
refer to Note 
12.
39,000
0.07%
0.003%
14.
E Fund Management 
(Note 13)
E Fund Management 
is a member of 
the same group of 
companies as GF 
Securities (Hong 
Kong) Brokerage.
Discretionary
No
174,000
0.32%
0.02%
15.
E Fund Hong Kong 
(Note 13)
E Fund Hong Kong is 
a member of the same 
group of companies 
as GF Securities 
(Hong Kong) 
Brokerage.
Discretionary
No
49,000
0.09%
0.004%
16.
GF Securities AM 
(Note 14)
GF Securities AM is 
a member of the same 
group of companies 
as GF Securities 
(Hong Kong) 
Brokerage.
Discretionary
No
61,000
0.11%
0.01%

<<<PAGE 22>>>
22
No.
Connected 
Distributor
Connected Client
Relationship with 
the Connected 
Distributor
Whether the 
connected
client will hold 
the beneficial 
interests of the
Offer Shares 
on a non-
discretionary
basis or
discretionary 
basis for
independent 
third parties
Whether the 
Connected 
Client is a 
collective 
investment 
scheme 
which is not 
authorised 
by the 
SFC or is 
expected 
to hold the 
Offer Shares 
on behalf of 
such scheme
Number of 
Offer Shares 
allocated 
to the 
Connected 
Client
Approximate 
percentage 
of total 
number of 
Offer Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
percentage 
of total 
Shares 
in issue 
immediately 
following the 
completion 
of Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
17.
China Merchants 
Securities (HK) Co., 
Limited (“CMS”)
Bosera AM 
(Note 15)
Bosera AM is a 
member of the same 
group of companies 
as CMS.
Discretionary
No
67,000
0.12%
0.01%
18.
GTJA Securities and 
Haitong International 
Fullgoal HK 
(Note 16)
Fullgoal HK is 
considered as a 
member of the same 
group of companies 
as GTJA Securities 
and Haitong 
International.
Discretionary
Yes
100,350
0.18%
0.01%
19.
Fullgoal Fund 
(Note 16)
Fullgoal Fund is 
considered as a 
member of the same 
group of companies 
as GTJA Securities 
and Haitong 
International.
Discretionary
Yes
122,650
0.23%
0.01%
Notes:
(1) 
ICBC Wealth has engaged Shanghai GTHT, a qualified domestic institutional investor as approved by the 
relevant PRC authority, to subscribe for and hold such Offer Shares on a non-discretionary basis on behalf of 
ICBC Wealth, in the name of Guotai Haitong Junxiang Wentuo QDII No.1 Collective Asset Management Plan 
Product (國泰海通君享穩拓 QDII1 號集合資產管理計劃). Shanghai GTHT is a member of the same group 
of companies as GTJA Securities and Haitong International. ICBC Wealth is wholly owned by Industrial and 
Commercial Bank of China Limited (stock code: 1398.HK, 601398.SH).
As confirmed by Shanghai GTHT, (i) the Offer Shares to be placed to Shanghai GTHT are to be held on a 
non-discretionary basis on behalf of an independent third party; and (ii) each of ICBC Wealth and its ultimate 
beneficial owner(s) is independent third party of the Company, its subsidiaries, its Single Largest Group 
of Shareholders, its substantial shareholders, Shanghai GTHT, GTJA Securities, Haitong International and 
the companies which are members of the same group of companies as each of the Overall Coordinators and 
Underwriters, respectively.

<<<PAGE 23>>>
23
(2) 
ICBC Wealth has engaged CICC, a qualified domestic institutional investor as approved by the relevant PRC 
authority, to subscribe for and hold such Offer Shares on a non-discretionary basis on behalf of ICBC Wealth, 
in the name of ICBC Wealth Wisdom Joy Minimum Holding Period 180 Days Fixed Income Open-End Net 
Value Wealth Management Product (工銀理財智悅最短持有 180 天固定收益類開放式淨值型理財產品). ICBC 
Wealth is wholly owned by Industrial and Commercial Bank of China Limited (stock code: 1398.HK, 601398.
SH). CICCHKS is a wholly owned subsidiary of CICC, and therefore a member of the same group of companies 
as CICC.
As confirmed by CICC, (i) the Offer Shares to be placed to CICC are to be held on a non-discretionary basis 
on behalf of an independent third party; and (ii) each of ICBC Wealth and its ultimate beneficial owner(s) 
is an independent third party of the Company, its subsidiaries, its Single Largest Group of Shareholders, 
its substantial shareholders, CICC, CICCHKS and the companies which are members of the same group of 
companies as each of the Overall Coordinators and Underwriters, respectively.
(3) 
China Southern is held by Huatai Securities Co., Ltd. as to 41.16%, which wholly owns HTFH. China Southern 
will hold the Offer Shares in its capacity as the discretionary fund manager for and on behalf of its underlying 
clients, each of which is an independent third party of the Company, its subsidiaries, China Southern, HTFH and 
the companies which are members of the same group of companies as HTFH.
(4) 
UBS AM Singapore will hold the Offer Shares in its capacity as the delegate of the investment manager on a 
discretionary basis. It is an independent third party of the Company, its subsidiaries, UBS AG Singapore, UBS 
AG Hong Kong and the companies which are members of the same group of companies as UBS AG Singapore 
and UBS AG Hong Kong.
(5) 
HSBC AM HK is a wholly owned subsidiary of HSBC Holdings Plc, a company listed on the Stock Exchange 
(stock code: 0005) and several other overseas stock exchanges and one of the group of legal entities that form 
HSBC Global Asset Management.
HSBC Bank is one of the Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead 
Managers in connection with the Global Offering. HSBC AM HK will hold the Offer Shares in its capacity as 
the discretionary fund manager managing assets on behalf of its underlying clients (“HSBC AM HK Ultimate 
Clients”). There is no ultimate beneficial owner holding 30% interest or more in such underlying client.
The HSBC AM HK Ultimate Clients for purpose of this placing subscription include HGIF CHINESE EQUITY 
(HH), HSBC CHINA GROWTH FD (HH), HSBC CHINA MOMENTUM (HH), HSBC CHINA MULT-A EQ-
OFF, HSBC POOLED CHINESE (HH), HGIF HONG KONG EQUITY (HH), HSBC POOLED HK EQ (HH), 
AVAW ASIEN FUND D (HH), CITY U HK-ASIA XJ EQ (HH), HGIF ASIA EX JAPAN EQ (HH), HGIF 
MGD SOL-AFG (HH), HSBC MST ASIEN (HH), HSBC RAIF AES ANGEL (HH), HSBC RAIF AES (HH), 
HSBC APXJ EQ VOL FOC (HH), HSBC POOLED AP EXJ EQ (AC), HGIF ASIA EXJ EQ SMAL (HH), 
HSHK ASIAN SMALL CAP (EQ), APNIESA-ADIV (HH), HGIF APXJ EQ HIGHDIV (HH), HGIF MGD 
SOL-AFI (HH), SAA (HH), +SG INSP Asia G ILP, HSBC Digital Leaders, HGIF GEM Equity, HGIF BRIC 
Equity, HGIF BRIC MARKETS, for each of which no ultimate beneficial owner holds 30% or more interest. 
HSBC AM HK has confirmed that, to the best of their knowledge and after making all reasonable enquires, each 
relevant fund managed by them is an independent third party of the Company and its subsidiaries.
(6) 
ABCI AM is a member of the same group of companies as ABCI Capital and ABCI Securities. ABCI AM 
is therefore a connected client of ABCI Capital and ABCI Securities. The investment of ABCI AM is on a 
discretionary basis, and each of the underlying clients and their respective ultimate beneficial owners holding 
30% or more interest is an independent third party of ABCI Asset Management Limited.

<<<PAGE 24>>>
24
(7) 
China AMC HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the sub 
funds on behalf of its investors (the “China AMC HK Ultimate Clients”). CSB is an indirectly wholly owned 
subsidiary of CITIC Securities. China AMC HK is wholly owned by China AMC, who is in turn controlled as to 
62.2% by CITIC Securities. Therefore, China AMC HK is a member of the same group of companies as CSB.
China AMC HK is to invest on a discretionary basis on behalf of the China AMC HK Ultimate Clients which 
are independent third parties and no proprietary money is used for the subscription of Offer Shares. The details 
of the China AMC HK Ultimate Clients are as follows:
Name of the funds to which the Offer 
Shares will be allocated
Whether any investor 
holds 30% or more 
interest in the fund
Ultimate Beneficial Owner with 
30% or more interests and 
Shareholding (%)
CHINAAMC CHINA FOCUS FUND
Yes
Manulife (International) Limited
ChinaAMC Absolute Return Fund SP
Yes
Li Fung Ming
To the best knowledge of China AMC HK, each of the China AMC HK Ultimate Clients is an independent third 
party of the Company, its subsidiaries, its Single Largest Group of Shareholders, its substantial shareholders, 
China AMC HK, CSB, the companies which are members of the same group of companies as each of the 
Overall Coordinators and Underwriters, respectively.
(8) 
China AMC will hold the Offer Shares in its capacity as the discretionary fund manager managing the sub funds 
on behalf of its investors (the “China AMC Ultimate Clients”). CSB is an indirectly wholly owned subsidiary 
of CITIC Securities. China AMC is controlled as to 62.2% by CITIC Securities. Therefore, China AMC is a 
member of the same group of companies as CSB.
China AMC is to invest on a discretionary basis on behalf of the China AMC Ultimate Clients which are 
independent third parties and no proprietary money is used for the subscription of Offer Shares. The details of 
the China AMC Ultimate Clients are as follows:
Name of the funds to which the Offer 
Shares will be allocated
Whether any investor 
holds 30% or more 
interest in the fund
Ultimate Beneficial Owner with 
30% or more interests and 
Shareholding (%)
ChinaAMC Greater China Enterprises 
Selected Dynamic Allocation Hybrid Fund 
(QDII)
No
N/A
ChinaAMC Global Technology Pioneer 
Hybrid Fund (QDII)
No
N/A
ChinaAMC Mobile Internet Dynamic 
Allocation Hybrid Fund (QDII)
No
N/A
ChinaAMC New Era Flexible Allocation 
Hybrid Fund (QDII)
No
N/A
To the best knowledge of China AMC, each of the China AMC Ultimate Clients is an independent third 
party of the Company, its subsidiaries, its Single Largest Group of Shareholders, its substantial shareholders, 
China AMC, CSB, the companies which are members of the same group of companies as each of the Overall 
Coordinators and Underwriters, respectively.

<<<PAGE 25>>>
25
(9) 
CUAM will hold the Offer Shares in its capacity as the discretionary fund manager managing the sub funds on 
behalf of its investors (the “CUAM Ultimate Clients”). CUAM is owned as to 35.41% by Orient Securities Co., 
Ltd (stock code: 3958.HK, 600958.SH) and is therefore a member of the same group of companies as Orient.
CUAM is to invest on a discretionary basis on behalf of the CUAM Ultimate Clients which are independent 
third parties and no proprietary money is used for the subscription of Offer Shares. The details of the CUAM 
Ultimate Clients are as follows:
Name of the funds to which the Offer 
Shares will be allocated
Whether any investor 
holds 30% or more 
interest in the fund
Ultimate Beneficial Owner with 
30% or more interests and 
Shareholding (%)
CUAM Global Consumer Industries Hybrid 
Fund
No
N/A
To the best knowledge of CUAM, each of the CUAM Ultimate Clients is an independent third party of the 
Company, its subsidiaries, its Single Largest Group of Shareholders, its substantial shareholders, CUAM, 
Orient, the companies which are members of the same group of companies as each of the Overall Coordinators 
and Underwriters, respectively.
(10) 
CUAM HK will hold the Offer Shares in its capacity as the discretionary investment manager managing the sub 
funds and discretionary accounts on behalf of its investors (the “CUAM HK Ultimate Clients”). CUAM HK is 
wholly owned by CUAM and is therefore a member of the same group of companies as Orient.
CUAM HK is to invest on a discretionary basis on behalf of the CUAM HK Ultimate Clients which are 
independent third parties and no proprietary money is used for the subscription of Offer Shares. The details of 
the CUAM HK Ultimate Clients are as follows:
Name of the funds to which the Offer 
Shares will be allocated
Whether any investor 
holds 30% or more 
interest in the fund
Ultimate Beneficial Owner with 
30% or more interests and 
Shareholding (%)
LC Logistics, Inc
Yes
Xu Xin
Li Yan 
China Universal Special Situation Fund 
SPC - CUAM Flexible Strategy Fund SP
Yes
CITIC Securities Brokerage (HK) 
Limited - Client Account
Excellent Tide Securities Limited (for and 
on behalf of Excellent Tide Eurasia OFC - 
Excellent Tide Eurasia No.1 Fund）
Yes
Hua Zhongjie 
Zhang Ping 
Poly Legend International Limited
Yes
Yang Peilin
Welkin Links Asset Management Limited 
(for and on behalf of ZhiDe HengShun 
No.1 Limited Partnership Fund）
Yes
Liao Jianfeng 
Liao Yanning 
CUAM China-Hong Kong Strategy Fund
No
N/A
Among CUAM HK Ultimate Clients, China Universal Special Situation Fund SPC - CUAM Flexible Strategy 
Fund SP, is a collective investment scheme which is not authorised by the SFC.
To the best knowledge of CUAM HK, each of the CUAM HK Ultimate Clients is an independent third party 
of the Company, its subsidiaries, its Single Largest Group of Shareholders, its substantial shareholders, 
CUAM HK, Orient, the companies which are members of the same group of companies as each of the Overall 
Coordinators and Underwriters, respectively.

<<<PAGE 26>>>
26
(11) 
GF International will hold Offer Shares in its capacity as the discretionary fund manager managing the funds on 
behalf of its investors (the “GF International Ultimate Clients”). GF International is an indirect non-wholly 
owned subsidiary of GF Securities Co. Ltd. (Stock Code: 1776) (“GF Securities”), and GF Securities (Hong 
Kong) Brokerage is an indirect wholly-owned subsidiary of GF Securities, therefore GF International is a 
member of the same group of companies as GF Securities (Hong Kong) Brokerage. GF International is therefore 
considered as a connected client of GF Securities (Hong Kong) Brokerage pursuant to paragraph 1B(7) of 
Appendix F1 to the Listing Rules.
GF International is to invest on a discretionary basis on behalf of the GF International Ultimate Clients which 
are independent third parties and no proprietary money is used for the subscription of Offer Shares. The details 
of the GF International Ultimate Clients are as follows:
Name of the funds to which the Offer
Shares will be allocated
Whether any investor 
holds 30% or more 
interest in the fund
Ultimate Beneficial Owner with 
30% or more interests and 
Shareholding (%)
GFI Global Select Equity Fund
No
N/A
GF Luminous Fund
No
N/A
GF Vision Fund
No
N/A
GF Bonanza Fund
No
N/A
GF Curation Equity Fund
No
N/A
GF International is to invest on a discretionary basis on behalf of the GF International Ultimate Clients which 
are independent third parties and no proprietary money is used for the subscription of Offer Shares. To the best 
knowledge of GF International, each of GF International Ultimate Clients is an independent third party of the 
Company, its subsidiaries, its substantial shareholders, GF International, GF Securities (Hong Kong) Brokerage 
and the companies which are members of the same group of companies as GF Securities (Hong Kong) 
Brokerage. No ultimate beneficial owner holds 30% or more interest in the funds.
(12) 
Each of VPHK and VPL will hold the Offer Shares in its capacity as the discretionary fund manager managing 
the sub funds on behalf of its investors (the “VP Ultimate Clients”). Value Partners is a member of the same 
group of companies as GF Securities (Hong Kong) Brokerage. GF Securities (Hong Kong) Brokerage is an 
indirect wholly-owned subsidiary of GF Securities. Each of Value Partners Hong Kong Limited and Value 
Partners Limited is a wholly-owned subsidiary of Value Partners Group Limited (Stock Code: 806) (“VPGL”). 
By virtue of GF Securities is interested in 20.04% shareholding in VPGL which renders Value Partners an 
associate of GF Securities. Accordingly, Value Partners is a member of the same group of companies as GF 
Securities (Hong Kong) Brokerage and is considered as a connected client of GF Securities (Hong Kong) 
Brokerage under paragraph 1B(7) of the Placing Guidelines.

<<<PAGE 27>>>
27
VPHK and VPL are to invest on a discretionary basis on behalf of the VP Ultimate Clients which are 
independent third parties and no proprietary money is used for the subscription of Offer Shares. The details of 
the VP Ultimate Clients are as follows:
Name of the funds to which the Offer Shares 
will be allocated
Fund Manager
Whether any 
investor holds 30% 
or more interest 
in the fund
Ultimate Beneficial Owner with 
30% or more interests and 
Shareholding (%)
Value Partners China Greenchip Fund Limited
VPL
Yes
AIA International Limited
Value Partners Intelligent Funds – China 
Convergence Fund
VPL
No
N/A
Value Partners Intelligent Funds – Chinese 
Mainland Focus Fund
VPL
Yes
AIA International Limited
Value Partners Intelligent Funds – JA-VP China 
New Century Fund
VPL
Yes
Aizawa Securities Co., Ltd.
Value Partners Asia Fund, LLC
VPL
Yes
No UBO shareholding with 30% 
or more interest
Value Partners Classic Fund
VPHK
No
N/A
Value Partners High-Dividend Stocks Fund
VPHK
No
N/A
Value Partners Fund Series – Value Partners 
Asian Income Fund
VPHK
Yes
Bank of China (Hong Kong) 
Nominees Limited
Value Partners Multi-Asset Fund
VPHK
Yes
AIA International Limited
Value Partners Funds SPC – Value Partners China 
A-Share Innovation Fund SP
VPHK
Yes
Custody Bank of Japan, Ltd.
Among the VP Ultimate Clients, (i) Value Partners Intelligent Funds - JA-VP China New Century Fund; (ii)
Value Partners Asia Fund, LLC; and (iii) Value Partners Funds SPC – Value Partners China A-Share Innovation 
Fund SP are collective investment schemes which are not authorised by the SFC.
To the best knowledge of VPHK and VPL, each of the VP Ultimate Clients is an independent third party of the 
Company, its subsidiaries, its Single Largest Group of Shareholders, its substantial shareholders, VPHK, VPL, 
GF Securities (Hong Kong) Brokerage and the companies which are members of the same group of companies 
as each of the Overall Coordinators and Underwriters, respectively.

<<<PAGE 28>>>
28
(13) 
Each of E Fund Management and E Fund Hong Kong will hold the Offer Shares in its capacity as the 
discretionary fund manager managing the sub funds on behalf of its investors (the “E Fund Ultimate Clients”). 
GF Securities (Hong Kong) Brokerage is an indirect wholly-owned subsidiary of GF Securities, which in turn 
holds 22.65% of the issued share capital of E Fund Management, therefore E Fund Management is a member of 
the same group of companies as GF Securities (Hong Kong) Brokerage. E Fund Hong Kong is a wholly-owned 
subsidiary of E Fund Management, therefore E Fund Hong Kong is a member of the same group of companies 
as GF Securities (Hong Kong) Brokerage. Each of E Fund Management and E Fund Hong Kong is therefore 
considered as a connected client of GF Securities (Hong Kong) Brokerage pursuant to paragraph 1B(7) of 
Appendix F1 to the Listing Rules.
E Fund Management and E Fund Hong Kong are to invest on a discretionary basis on behalf of the E Fund 
Ultimate Clients which are independent third parties and no proprietary money is used for the subscription of 
Offer Shares. The details of the E Fund Ultimate Clients are as follows:
Name of the funds to which the Offer
Shares will be allocated
Fund Manager
Whether any 
investor holds 30% 
or more interest 
in the fund
Ultimate Beneficial Owner 
with 30% or more interests 
and Shareholding (%)
E Fund Global Asset Allocation Hybrid Fund
E Fund Management
No
N/A
E Fund Global Quality Enterprise Hybrid Fund
E Fund Management
No
N/A
E Fund HSCEI ETF
E Fund Management
No
N/A
E Fund CSI Overseas China Internet 50 Index 
ETF
E Fund Management
No
N/A
E Fund HSTECH ETF
E Fund Management
Yes
E Fund HSTECH ETF FEEDER 
FUND
E Fund S&P Global Luxury Enhanced Index Fund
E Fund Management
No
N/A
E Fund Global Growth Hybrid Fund
E Fund Management
No
N/A
E Fund Global Healthcare Sector Sponsored 
Hybrid Fund
E Fund Management
No
N/A
E Fund Hong Kong Hang Seng Composite 
SmallCap Index Fund
E Fund Management
No
N/A
E FUND HANG SENG INDEX ETF
E Fund Management
No
N/A
E Fund (HK) Global Quality Growth Fund
E Fund Hong Kong
No
N/A
E Fund (HK) China Equity Dividend Fund
E Fund Hong Kong
No
N/A
E Fund (HK) Global Conviction Fund
E Fund Hong Kong
No
N/A
E Fund (HK) Greater China Conviction Fund
E Fund Hong Kong
No
N/A
E Fund (HK) Global Allocation Fund SP I
E Fund Hong Kong
Yes
China Cinda Asset Management 
Co Ltd (PRC)
E FUND (HK) NEO OPPORTUNITY SP I
E Fund Hong Kong
No
N/A
E Fund (HK) Neo Opportunity SP II
E Fund Hong Kong
No
N/A
To the best knowledge of E Fund Management and E Fund Hong Kong, each of the E Fund Ultimate Clients 
is an independent third party of the Company, its subsidiaries, its Single Largest Group of Shareholders, its 
substantial shareholders, E Fund Management, E Fund Hong Kong, GF Securities (Hong Kong) Brokerage and 
the companies which are members of the same group of companies as each of the Overall Coordinators and 
Underwriters, respectively.

<<<PAGE 29>>>
29
(14) 
GF Securities AM will hold Offer Shares in its capacity as the discretionary fund manager managing 
the funds on behalf of its investors (the “GF Securities AM Ultimate Clients”). GF Securities AM is a 
direct wholly-owned subsidiary of GF Securities and GF Securities (Hong Kong) Brokerage is an indirect 
wholly-owned subsidiary of GF Securities, therefore GF Securities AM is a member of the same group of 
companies as GF Securities (Hong Kong) Brokerage. GF Securities AM is therefore considered as a connected 
client of GF Securities (Hong Kong) Brokerage pursuant to paragraph 1B(7) of Appendix F1 to the Listing 
Rules.
GF Securities AM is to invest on a discretionary basis on behalf of the GF Securities AM Ultimate Clients 
which are independent third parties and no proprietary money is used for the subscription of Offer Shares. The 
details of the GF Securities AM Ultimate Clients are as follows:
Name of the funds to which the Offer
Shares will be allocated
Whether any investor holds 
30% or more interest in 
the fund
Ultimate Beneficial Owner with 
30% or more interests and 
Shareholding (%)
GFAM ZYJXCL NO.2 ASSET 
MANAGEMENT AC
Yes
Postal Savings Bank of China 
Co., Ltd. (stock code: 1658.HK) 
(“PSBC”)
ICBC (ASIA) LTD-PAB-GFAM ZHONGYOU 
NO.1 ASSET MANAGEMENT
Yes
PSBC
ICBC (ASIA) LTD-PAB-GFAM ZHONGYOU 
NO.2 ASSET MANAGEMENT
Yes
PSBC
GFAM ZHONGYOU NO.9 ASSET 
MANAGEMENT ACCOUNT (QDII)
Yes
PSBC
GFAM-RXGGJX HK STOCK NO.1 ASSET 
MANAGEMENT AC
No
N/A
ICBC (ASIA) LTD-ICBC LTD-GFAM GYJXCL 
NO.1 ASSET MANAGEMENT AC
Yes
Industrial and Commercial Bank of 
China Limited (stock code: 1398.HK, 
601398.SH) (“ICBC”)
ICBC (ASIA) LTD-ICBC LTD-GFAM 
GYGGCL NO.2 AMA
Yes
ICBC
CIB-GFAM-ZYDYPZ NO.58 ASSET 
MANAGEMENT AC
Yes
Liu Peilan
To the best knowledge of GF Securities AM, each of the GF Securities AM Ultimate Clients is an independent 
third party of the Company, its subsidiaries, its Single Largest Group of Shareholders, its substantial 
shareholders, GF Securities AM, GF Securities (Hong Kong) Brokerage and the companies which are members 
of the same group of companies as each of the Overall Coordinators and Underwriters, respectively.

<<<PAGE 30>>>
30
(15) 
Bosera AM will hold Offer Shares in its capacity as the discretionary fund manager managing the funds on 
behalf of its investors (the “Bosera AM Ultimate Clients”). Bosera AM is owned as to approximately 45% 
by China Merchants Fund Management Co., Ltd., which is in turn owned as to approximately 45% by China 
Merchants Securities Co., Ltd. (stock code: 6099.HK). CMS is a wholly owned subsidiary of China Merchants 
Securities Co., Ltd. Therefore, Bosera AM is a member of the same group of companies as CMS and is 
considered a connected client of CMS pursuant to paragraph 1B(7) of Appendix F1 to the Listing Rules.
Bosera AM is to invest on a discretionary basis on behalf of the Bosera AM Ultimate Clients which are 
independent third parties and no proprietary money is used for the subscription of Offer Shares. The details of 
the Bosera AM Ultimate Clients are as follows:
Name of the funds to which the Offer
Shares will be allocated
Whether any investor holds 
30% or more interest in 
the fund
Ultimate Beneficial Owner with 
30% or more interests and 
Shareholding (%)
Bosera Hong Kong Equity Plus Fund (SFC 
Authorised Fund)
No
N/A
Bosera Global Select Equity Fund SP
Yes
Zhang Lei
Bosera China New Opportunities Fund SP
No
N/A
Bosera Growth Premium Global Equity Strategy 
Fund SP
Yes
Guo Feng
Bosera Growth Premium Global Equity Strategy 
Fund SP2
Yes
Guangdong Dongfang Precision 
Science & Technology Co., Ltd 
(“Dongfang Precision Science”, 
a company listed on the Shenzhen 
Stock Exchange, stock code: 002611)
Bosera Greater China Enhanced Return Bond 
Fund (SFC Authorised Fund)
No
N/A
Bosera Growth Premium Global Equity Strategy 
Fund SP3
Yes
Huang Liya
Bosera Growth Premium Global Equity Strategy 
Fund SP4
Yes
Dongfang Precision Science
To the best knowledge of Bosera AM, each of the Bosera AM Ultimate Clients is an independent third party 
of the Company, its subsidiaries, its Single Largest Group of Shareholders, its substantial shareholders, Bosera 
AM, CMS and the companies which are members of the same group of companies as each of the Overall 
Coordinators and Underwriters, respectively.

<<<PAGE 31>>>
31
(16) 
Fullgoal HK is a wholly owned subsidiary of Fullgoal Fund. Guotai Haitong Securities Co., Ltd. (stock codes: 
2611.HK and 601211.SH) (“Guotai Haitong”) is a shareholder of Fullgoal Fund, holding a 27.775% equity 
interest therein. GTJA Securities and Haitong International are both subsidiaries of Guotai Haitong. Each of 
Fullgoal HK and Fullgoal Fund will hold the Offer Shares in its capacity as the discretionary fund manager 
managing assets for and on behalf of its underlying investors, each of which is an independent third party of 
the Company, its subsidiaries, Fullgoal HK, Fullgoal Fund, GTJA Securities, Haitong International and the 
companies which are members of the same group of GTJA Securities and Haitong International. Details of the 
collective investment schemes which are not authorized by the SFC are as follows:
Fund Name
Whether 
the Scheme 
is Publicly 
Marketed
Fund Manager
UBO of Fund 
Manager
UBO of the Fullgoal 
Fund Ultimate 
Clients
ICBC Fullgoal global technology 
& internet fund
Yes
Fullgoal Fund
N/A
No single ultimate 
beneficial owner holds 
30% or more interest
ICBC Fullgoal China Small & 
Mid Cap (HK listed) Equity Fund
Yes
Fullgoal Fund
N/A
No single ultimate 
beneficial owner holds 
30% or more interest
CMB-FULLGOAL BLUE 
CHIP SELECTED EQUITY 
FUND (QDII)
Yes
Fullgoal Fund
N/A
No single ultimate 
beneficial owner 
holds 30% or more 
interest

<<<PAGE 32>>>
32
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or 
any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or 
into the United States (including its territories and possessions, any state of the United States 
and the District of Columbia). This announcement does not constitute or form a part of any 
offer or solicitation to purchase or subscribe for securities in the United States or in any other 
jurisdictions. The securities mentioned herein have not been, and will not be, registered under 
the United States Securities Act of 1933 as amended from time to time (the “U.S. Securities 
Act”) or securities law of any state or other jurisdiction of the United States. The securities may 
not be offered, sold, pledged or otherwise transferred within the United States except pursuant 
to an exemption from the registration requirements of the U. S. Securities Act and in compliance 
with any applicable state securities laws, or (1) solely to qualified institutional buyers as defined 
in Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under 
the U.S. Securities Act and (2) outside the United States unless in compliance with Regulation S 
under the U.S. Securities Act. There will be no public offer of securities in the United States.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated July 22, 2026 issued by Zhongji InnoLight 
Co., Ltd. for detailed information about the Global Offering described below before deciding 
whether or not to invest in the H Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinators 
(for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate 
their obligations under the Hong Kong Underwriting Agreement with immediate effect upon 
the occurrence of any of the events set out in the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. on the Listing Date (which is currently expected to be 
on Thursday, July 30, 2026 (Hong Kong time)).

<<<PAGE 33>>>
33
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering (before any exercise of the 
Over-allotment Option, and assuming no new Shares are issued under the Restricted Shares 
Incentive Schemes), the total market value of the H Shares expected to be held by the public 
is expected to be approximately HK$53.4 billion, calculated based on the final Offer Price of 
HK$980.00 per H Share, which is higher than the prescribed expected market value of H Shares 
required to be held in public hands of not less than HK$3.0 billion under Rule 19A.13A(2)(b) of 
the Listing Rules, thereby satisfying Rule 19A.13A(2) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the H Shares of the Company at the time of Listing. Based on 
the final Offer Price of HK$980.00 per H Share, the Company satisfies the free float requirement 
under Rule 19A.13C of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering (before any 
exercise of the Over-allotment Option): (i) no placee will, individually, be placed more than 10% 
of the enlarged issued share capital of the Company immediately after the Global Offering; (ii) 
there will not be any new substantial Shareholder immediately after the Global Offering; (iii) the 
three largest public Shareholders do not hold more than 50% of the H shares in public hands at the 
time of the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there 
will be at least 300 Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the 
Listing Rules.
PROPOSAL ON POTENTIAL A SHARE REPURCHASE PLAN
Reference is made to the A Share announcement of the Company dated July 29, 2026 in relation to 
the proposal on a potential A Share repurchase plan (the “Proposal”) received from Dr. Liu Sheng, 
the Chairman of the Board, an executive Director and the President of the Company, on July 28, 
2026. The Proposal remains subject to the consideration and approval of the Board. Therefore, the 
Proposal may or may not proceed, and the timing and amount of any A Share repurchase under the 
Proposal (if implemented) has yet to be determined. No repurchase of A Shares is currently being 
conducted or has been implemented pursuant to the Proposal. The source of funds for the A Share 
repurchase under the Proposal (if implemented) will be the Company’s internal resources and/or 
self-raised funds, and not the proceeds from the Global Offering. The A Share repurchase under the 
Proposal, if implemented, will be conducted in compliance with all applicable laws and regulations 
(including the Listing Rules).

<<<PAGE 34>>>
34
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Thursday, July 
30, 2026 (Hong Kong time), provided that (i) the Global Offering has become unconditional 
in all respects, and (ii) the right of termination described in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for 
Termination” in the Prospectus has not been exercised. Investors who trade H Shares on the basis 
of publicly available allocation details prior to the receipt of H Share certificates or prior to the H 
Share certificates becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Thursday, July 
30, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Thursday, July 30, 2026 (Hong Kong time). The H Shares will be 
traded in board lots of 50 H Shares each and the stock code of the H Shares will be 3308.
By order of the Board
Zhongji InnoLight Co., Ltd.
中際旭創股份有限公司
Dr. Liu Sheng
Chairman of the Board, Executive Director and 
President of the Company
Hong Kong, July 29, 2026
As at the date of this announcement, the Board comprises (i) Dr. Liu Sheng, Mr. Wang Xiaodong 
and Ms. Wang Xiaoli as executive Directors; (ii) Ms. Chen Caiyun as non-executive Director; and 
(iii) Ms. Zhan Shuping, Dr. Cheng Bo, Dr. Qu Wenzhou and Mr. Huang Guobin as independent 
non-executive Directors.
