# 配发结果公告抽取任务：9980.HK Eastroc Beverage (Group) Co., Ltd. - H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**02/02/2026 22:57**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0202/2026020203212.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"9980.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
– 1 –
EASTROC BEVERAGE (GROUP) CO., LTD.╱
東鵬飲料(集團)股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated January 26, 2026 (the “Prospectus”) 
issued by Eastroc Beverage (Group) Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, Shareholders and prospective investors should be aware that the price 
of the H Shares could move substantially even with a small number of H Shares 
traded and should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
09980
Stock short name
EASTROC
Dealings commencement date
February 3, 2026*
*  see note at the end of the announcement
Price Information
Final Offer Price
HK$248.00
Maximum Offer Price
HK$248.00
Offer Shares and Share Capital
Number of Offer Shares (Before exercise of the Over-
allotment Option)
40,889,900
Final Number of Offer Shares in Hong Kong Public 
Offering
4,089,000
Final Number of Offer Shares in International 
Offering (excluding Employee Reserved Shares under 
the Employee Preferential Offering)
36,130,300
Number of Employee Reserved Shares in Employee 
Preferential Offering
670,600
Number of issued shares upon Listing (before exercise 
of the Over-allotment Option)
560,902,900

<<<PAGE 2>>>
– 2 –
Over-allocation
No. of Offer Shares over-allocated
6,133,400
Such over-allocation may be covered by exercising the Over-allotment Option or 
by making purchases in the secondary market at prices that do not exceed the Offer 
Price or through deferred delivery or a combination of these means. In the event 
the Over-allotment Option is exercised, an announcement will be made on the Stock 
Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$10,140.7 million
Less: Estimated listing expenses payable based on 
Final Offer Price
HK$(146.4) million
Net proceeds
HK$9,994.3 million
Note:  Gross proceeds refers to the amount to which the Company is entitled receive. For details of the 
use of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the 
Prospectus. The Company will adjust the allocation of the net proceeds from the exercise of the 
Over-allotment Option (if any) for the purposes as set out in the section headed “Future Plans and 
Use of Proceeds” of the Prospectus on a pro rata basis. For the nine months ended September 30, 
2025, the listing expenses of RMB2.6 million has been charged to the consolidated statements of 
profit or loss and other comprehensive income of the Company.

<<<PAGE 3>>>
– 3 –
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
66,692
No. of successful applications
20,113
Subscription level
57.46 times
Reallocation
No
No. of Offer Shares initially available under the Hong 
Kong Public Offering
4,089,000
No. of Offer Shares reallocated from the International 
Offering
0
Final no. of Offer Shares under the Hong Kong Public 
Offering
4,089,000
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering
10.00%
Note:  For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can 
refer to www.eipo.com.hk/eIPOAllotment to perform a search by name or identification number or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
219
Subscription Level (excluding Employee Reserved 
Shares under the Employee Preferential Offering)
15.60 times
No. of Offer Shares initially available under the 
International Offering (excluding Employee Reserved 
Shares under the Employee Preferential Offering)
36,130,300
Final no. of Offer Shares under the International 
Offering (excluding Employee Reserved Shares under 
the Employee Preferential Offering) (before exercise of 
the Over-allotment Option)
36,131,200
% of Offer Shares under the International Offering to the 
Global Offering
90.00%

<<<PAGE 4>>>
– 4 –
The Directors confirm that, to the best of their knowledge, information and belief, save 
for (a) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent 
under paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) 
granted by the Stock Exchange to permit H Shares in the International Offering to be placed 
to certain existing minority Shareholders and/or their close associates, (b) a waiver from 
strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) 
of the Placing Guidelines granted by the Stock Exchange to permit the Company to allocate 
certain Offer Shares to the Existing Shareholder Employee Participants on a preferential 
basis under the Employee Preferential Offering, and (c) a consent under paragraph 18 of 
Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to, among 
other things, allocate further H Shares in the International Offering to certain Cornerstone 
Investors and/or their close associates, (i) none of the Offer Shares subscribed by the 
placees and the public have been financed directly or indirectly by the Company, any of the 
Directors, chief executive of the Company, substantial Shareholders, existing Shareholders 
of the Company or any of its subsidiaries or their respective close associates; and (ii) none 
of the placees and the public who have purchased the Offer Shares are accustomed to 
taking instructions from the Company, any of the Directors, chief executive of the Company, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries 
or their respective close associates in relation to the acquisition, disposal, voting or other 
disposition of H Shares registered in his/her/its name or otherwise held by him/her/it.
PREFERENTIAL OFFERING
Employee preferential offering
No. of valid applications
1*
Subscription level
0.9987 times
No. of Employee Reserved Share initially available 
under the Employee Preferential Offering
670,600 International Offer 
Shares
Final no. of Employee Reserved Share under  
the Employee Preferential Offering
669,700
Under-subscription of shares and made available to  
the International Offering
900
Under-subscription of shares and made available to  
the Hong Kong Public Offer
—
*  The number of Eligible Employee participated in the Employee Preferential Offering is 67.

<<<PAGE 5>>>
– 5 –
For details of the Employee Preferential Offering, please refer to the section headed 
“Structure of the Global Offering — Employee Preferential Offering” of the Prospectus 
and the section headed “Others/Additional Information — Allocations under the Employee 
Preferential Offering” in this announcement.
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of Offer 
Shares allocated
% of total 
issued H Shares 
after  the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing 
shareholders 
or their close 
associates
Al-Rayyan Holding LLC Note 2
4,715,900
11.53%
0.84%
No
Taibai Investments Pte. Ltd. Note 2
1,760,600
4.31%
0.31%
Yes
True Light Investments  
H Pte. Ltd. Note 2
440,100
1.08%
0.08%
Yes
BlackRock Funds Note 2
1,886,300
4.61%
0.34%
Yes
UBS Asset Management 
(Singapore) Ltd. (“UBS AM 
Singapore”) Note 2
1,571,900
3.84%
0.28%
Yes
Huang River Investment Limited
1,571,900
3.84%
0.28%
No
HSG Growth VII Holdco, Ltd. Note 2
1,257,500
3.08%
0.22%
No
JPMorgan Asset Management (Asia 
Pacific) Limited Note 2
943,100
2.31%
0.17%
No
Azure Skylines Limited Note 2
943,100
2.31%
0.17%
No
Taikang Life Insurance  
Co., Ltd Note 2
943,100
2.31%
0.17%
Yes
Pacific Century Pines Investments 
1 Limited
943,100
2.31%
0.17%
No
FMR Participating Funds Note 2
628,700
1.54%
0.11%
Yes
Velmar Company Limited Note 2
628,700
1.54%
0.11%
No
Pinpoint Asset Management 
Limited Note 2
628,700
1.54%
0.11%
Yes
Amazing Mountain Limited Note 2
628,700
1.54%
0.11%
No
Great China Motivation Fund Phase 
II L.P. Note 2
628,700
1.54%
0.11%
Yes
Total
20,120,100
49.21%
3.59%

<<<PAGE 6>>>
– 6 –
Notes:
1.	
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering.
2.	
Only taking into account the Offer Shares allocated to the relevant investors as cornerstone 
investors under the Global Offering. In addition to the Offer Shares subscribed for as Cornerstone 
Investors, each of Al-Rayyan Holding LLC, Taibai Investments Pte. Ltd., True Light Investments H 
Pte. Ltd., BlackRock Funds, UBS AM Singapore, HSG Growth VII Holdco, Ltd., JPMorgan Asset 
Management (Asia Pacific) Limited, Azure Skylines Limited, Taikang Life Insurance Co., Ltd, FMR 
Participating Funds, Velmar Company Limited, Pinpoint Asset Management Limited, Amazing 
Mountain Limited, and Great China Motivation Fund Phase II L.P. and/or their respective close 
associates was allocated further Offer Shares as placees in the International Offering. Please 
refer to the section headed “Allotment Results Details — International Offering — Allottees with 
Waivers/Consents Obtained” in this announcement for details. Only the Offer Shares subscribed for 
as Cornerstone Investors are subject to lock-up as indicated below. For details, please refer to the 
section headed “Lock-up Undertakings — Cornerstone Investors” in this announcement.
Allottees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after the 
Global Offering 
(Assuming Over-
allotment Option is 
not exercised) Note 6
% of total issued 
share capital after 
the Global Offering 
(Assuming Over-
allotment Option is 
not exercised) Note 7
Relationship*
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of 
the Placing Guidelines in relation to subscription for H Shares by existing minority Shareholders holding more than 1% 
of the issued share capital of the Company immediately prior to the completion of the Global Offering and/or their close 
associates Notes 1, 2 and 9
Taikang Life Insurance Co., Ltd
943,100
2.31%
0.17%
A cornerstone 
investor and a 
close associate 
of an existing 
Shareholder
Great China Motivation Fund Phase 
II L.P.
628,700
1.54%
0.11%
A cornerstone 
investor and a 
close associate 
of an existing 
Shareholder

<<<PAGE 7>>>
– 7 –
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after the 
Global Offering 
(Assuming Over-
allotment Option is 
not exercised) Note 6
% of total issued 
share capital after 
the Global Offering 
(Assuming Over-
allotment Option is 
not exercised) Note 7
Relationship*
Allotees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations 
of further H Shares to the existing Shareholders and/or their close associates and Cornerstone Investors Note 3
Al-Rayyan Holding LLC
1,241,800
3.04%
0.22%
Same entity as 
the Cornerstone 
Investor
Taibai Investments Pte. Ltd.
404,000
0.99%
0.07%
Same entity as 
the Cornerstone 
Investor and 
an existing 
Shareholder
True Light Investments H Pte. Ltd.
101,000
0.25%
0.02%
Same entity as 
the Cornerstone 
Investor and a 
close associate 
of an existing 
Shareholder
Blackrock Asset Management 
North Asia Limited
404,000
0.99%
0.07%
Close associate of 
the Cornerstone 
Investor who 
is an existing 
Shareholder
UBS AM Singapore
202,000
0.49%
0.04%
Same entity as 
the Cornerstone 
Investor and 
an existing 
Shareholder
HCEP Management Limited
359,000
0.88%
0.06%
Close associate of 
the Cornerstone 
Investor
JPMorgan Asset Management (Asia 
Pacific) Limited
202,000
0.49%
0.04%
Same entity as 
the Cornerstone 
Investor
J.P. Morgan Securities Plc
15,000
0.04%
0.00% Note 10
Close associate of 
the Cornerstone 
Investor

<<<PAGE 8>>>
– 8 –
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after the 
Global Offering 
(Assuming Over-
allotment Option is 
not exercised) Note 6
% of total issued 
share capital after 
the Global Offering 
(Assuming Over-
allotment Option is 
not exercised) Note 7
Relationship*
Boyu Capital Investment 
Management Co., Limited
403,000
0.99%
0.07%
Close associate of 
the Cornerstone 
Investor
Taikang Life Insurance Co., Ltd
57,400
0.14%
0.01%
Same entity as 
the Cornerstone 
Investor and a 
close associate 
of an existing 
Shareholder
Taikang Asset Management (Hong 
Kong) Company Limited
2,600
0.01%
0.00% Note 10
Close associate of 
the Cornerstone 
Investor who is 
a close associate 
of an existing 
Shareholder
Fidelity Management & Research 
(Hong Kong) Limited
202,000
0.49%
0.04%
Close associate of 
the Cornerstone 
Investor who 
is an existing 
Shareholder
Velmar Company Limited
308,000
0.75%
0.05%
Same entity as 
the Cornerstone 
Investor
Pinpoint Asset Management 
Limited
60,000
0.15%
0.01%
Same entity as 
the Cornerstone 
Investor and a 
close associate 
of an existing 
Shareholder
Orchid Public Investment 
Management Company Limited
121,000
0.30%
0.02%
Close associate of 
the Cornerstone 
Investor
AJS Family Holding Limited
832,000
2.03%
0.15%
Close associate of 
the Cornerstone 
Investor who is 
a close associate 
of an existing 
Shareholder

<<<PAGE 9>>>
– 9 –
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after the 
Global Offering 
(Assuming Over-
allotment Option is 
not exercised) Note 6
% of total issued 
share capital after 
the Global Offering 
(Assuming Over-
allotment Option is 
not exercised) Note 7
Relationship*
Song Family International Holding 
Limited
832,000
2.03%
0.15%
Close associate of 
the Cornerstone 
Investor who is 
a close associate 
of an existing 
Shareholder
Great China Motivation Fund Phase 
II L.P.
675,000
1.65%
0.12%
Same entity as 
the Cornerstone 
Investor and a 
close associate 
of an existing 
Shareholder
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the 
Placing Guidelines in relation to allocations to Existing Shareholder Employee Participants under the Employee Preferential 
Offering Note 4
Existing Shareholder Employee 
Participants
669,700
1.64%
0.12%
Eligible Employees
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations to connected clients Note 5
Huatai Capital Investment Limited 
(“HTCI”) Note 8
331,600
0.81%
0.06%
Connected client as 
placee
UBS AM Singapore
1,571,900
3.84%
0.28%
Connected client 
as a cornerstone 
investor
202,000
0.49%
0.04%
Connected client as 
placee
CICC Financial Trading Limited 
(“CICC FT”)
120,900
0.30%
0.02%
Connected client as 
placee
E Fund Management Co., Ltd.  
(“E Fund Management”)
169,000
0.41%
0.03%
Connected client as 
placee
E Fund Management (Hong Kong) 
Co., Ltd. (“E Fund HK”)
21,000
0.05%
0.00% Note 10
Connected client as 
placee
Value Partners Hong Kong Limited 
(“Value Partners”)
32,000
0.08%
0.01%
Connected client as 
placee
Fullgoal Fund Management Co., 
Ltd. (“Fullgoal Fund”)
43,600
0.11%
0.01%
Connected client as 
placee

<<<PAGE 10>>>
– 10 –
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after the 
Global Offering 
(Assuming Over-
allotment Option is 
not exercised) Note 6
% of total issued 
share capital after 
the Global Offering 
(Assuming Over-
allotment Option is 
not exercised) Note 7
Relationship*
Fullgoal Asset Management (HK) 
Limited (“Fullgoal HK”)
33,000
0.08%
0.01%
Connected client as 
placee
Guotai Junan Investments 
(Hong Kong) Limited (“GTJA 
Investments”)
2,800
0.01%
0.00% Note 10
Connected client as 
placee
Notes:
1.	
Among the Cornerstone Investors, Taibai Investments Pte. Ltd., True Light Investments H Pte. Ltd., 
BlackRock Funds, UBS AM Singapore, Taikang Life Insurance Co., Ltd, FMR Participating Funds, 
Pinpoint Asset Management Limited and Great China Motivation Fund Phase II L.P. are either existing 
minority Shareholders of the Company or their close associates. The Stock Exchange has granted a 
waiver from strict compliance with the requirements under Rule 10.04 of the Listing Rules and consent 
under Paragraph 1C(2) of the Placing Guidelines to permit H Shares in the International Offering to 
be placed to certain existing minority Shareholders and/or their close associates. Please refer to the 
section headed “Waivers and Exemptions — Allocation of H Shares to existing minority Shareholders 
and their Close Associates” of the Prospectus for details.
The Stock Exchange granted the waiver on the condition that, among others, details of the allocation 
to the existing minority Shareholders holding more than 1% of the issued share capital of the Company 
immediately prior to the completion of the Global Offering will be disclosed in the Prospectus and/or 
allotment results announcement.
2.	
For details of the waiver from strict compliance with Rule 10.04 of the Listing Rules and prior consent 
under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by existing 
minority Shareholders and/or close associates of existing Shareholders, please refer to the section 
headed “Others/Additional Information” in this announcement.
3.	
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents 
the number of Offer Shares allocated to the investors as placees in the International Offering. For 
allocations of Offer Shares to the relevant investors as Cornerstone Investors, please refer to the 
section headed “Allotment Results Details — International Offer — Cornerstone Investors” in this 
announcement. For details of the consent under paragraph 18 of Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations of further H Shares to the existing Shareholders and/or 
their close associates and Cornerstone investors, please refer to the section headed “Others/Additional 
Information — Allocations of Offer Shares to the existing Shareholders and/or their close associates 
and Cornerstone investors with a consent under paragraph 18 of Chapter 4.15 of the Guide for New 
Listing Applicants” in this announcement.

<<<PAGE 11>>>
– 11 –
4.	
For details of the waiver from strict compliance with Rule 10.04 of the Listing Rules and consent 
under Paragraph 1C(2) of the Placing Guidelines in relation to allocations to Existing Shareholder 
Employee Participants and the Employee Preferential Offering, please refer to the sections headed 
“Waivers and Exemptions — Waiver and Consent in Respect of Allocations to Existing Shareholder 
Employee Participants” and “Structure of the Global Offering — Employee Preferential Offering” of 
the Prospectus. For details of the allocations under the Employee Preferential Offering, please refer 
to the section headed “Others/Additional Information — Allocations under the Employee Preferential 
Offering” in this announcement.
5.	
For details of the consents under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations to connected clients, please refer to the 
section headed “Others/Additional Information — Placing to connected clients with a prior consent 
under paragraph 1C(1) of the Placing Guidelines” in this announcement.
6.	
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering.
7.	
Only taking into account the H Shares allocated to the relevant investors under the Global Offering.
8.	
The number of Offer Shares allocated to HTCI listed in this subsection only represents the number of 
Offer Shares allocated to HTCI as a placee (excluding the final number of Offer Shares allocated to 
HTCI held on behalf of the privately-offered investment fund subscribed by the Eligible Employees 
under the Employee Preferential Offering).
9.	
The number of Offer Shares allocated to Taikang Life Insurance Co., Ltd and Great China Motivation 
Fund Phase II L.P. listed in this subsection only represents the number of Offer Shares allocated to 
Taikang Life Insurance Co., Ltd or Great China Motivation Fund Phase II L.P.as cornerstone investors 
(excluding the Offer Shares allocated to Taikang Life Insurance Co., Ltd or Great China Motivation 
Fund Phase II L.P. and/or their close associates in the placing tranche). For details of the consent 
under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations 
of further H Shares to the existing Shareholders and/or their close associates and Cornerstone 
investors, please refer to the section headed “Others/Additional Information — Allocations of Offer 
Shares to the existing Shareholders and/or their close associates and Cornerstone investors with 
a consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants” in this 
announcement.
10.	
Denotes less than 0.01%.

<<<PAGE 12>>>
– 12 –
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
immediately upon 
Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 3
% of shareholding 
in the Company 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings Note 2
Mr. Lin Note 4
260,828,779
—
46.50%
August 2, 2026 
(First Six Month 
Period)Note 1
February 2, 2027 
(Second Six Month 
Period)Note 2
Dongpeng Yuandao Note 4
2,080,034
—
0.37%
August 2, 2026 
(First Six Month 
Period)Note 1
February 2, 2027 
(Second Six Month 
Period)Note 2
Dongpeng Zhiyuan Note 4
65,082
—
0.01%
August 2, 2026 
(First Six Month 
Period)Note 1
February 2, 2027 
(Second Six Month 
Period)Note 2
Dongpeng Zhicheng Note 4
26,029
—
0.00%Note 5 
August 2, 2026 
(First Six Month 
Period)Note 1
February 2, 2027 
(Second Six Month 
Period)Note 2

<<<PAGE 13>>>
– 13 –
Notes:
1.	
The Controlling Shareholders may dispose of or transfer Share after the indicated date subject to 
that the Controlling Shareholders will not cease to be a Controlling Shareholder.
2.	
The Controlling Shareholders will cease to be prohibited from disposing or transferring Shares after 
the indicated date.
3.	
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering.
4.	
As of the Latest Practicable Date, Mr. Lin (i) directly owns approximately 99.9984% partnership 
interests as a limited partner in Dongpeng Yuandao, which beneficially owns 2,080,034 A Shares; 
(ii) directly owns approximately 99.8901% partnership interests as a limited partner in Dongpeng 
Zhiyuan, which beneficially owns 65,082 A Shares; (iii) directly owns approximately 99.8742% 
partnership interests as a limited partner in Dongpeng Zhicheng, which beneficially owns 26,029 
A Shares. By virtue of the SFO, Mr. Lin is deemed to be interested in the Shares held by Dongpeng 
Yuandao, Dongpeng Zhiyuan and Dongpeng Zhicheng.
5.	
Denotes less than 0.01%.
Cornerstone Investors
Name
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1
% of shareholding 
in the Company 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings Note 2
Al-Rayyan Holding LLC
4,715,900
11.53%
0.84%
August 2, 2026
Taibai Investments Pte. Ltd.
1,760,600
4.31%
0.31%
August 2, 2026
True Light Investments H Pte. Ltd.
440,100
1.08%
0.08%
August 2, 2026
BlackRock Funds
1,886,300
4.61%
0.34%
August 2, 2026
UBS AM Singapore
1,571,900
3.84%
0.28%
August 2, 2026
Huang River Investment Limited
1,571,900
3.84%
0.28%
August 2, 2026
HSG Growth VII Holdco, Ltd.
1,257,500
3.08%
0.22%
August 2, 2026
JPMorgan Asset Management (Asia 
Pacific) Limited
943,100
2.31%
0.17%
August 2, 2026
Azure Skylines Limited
943,100
2.31%
0.17%
August 2, 2026
Taikang Life Insurance Co., Ltd
943,100
2.31%
0.17%
August 2, 2026

<<<PAGE 14>>>
– 14 –
Name
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1
% of shareholding 
in the Company 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings Note 2
Pacific Century Pines Investments 
1 Limited
943,100
2.31%
0.17%
August 2, 2026
FMR Participating Funds
628,700
1.54%
0.11%
August 2, 2026
Velmar Company Limited
628,700
1.54%
0.11%
August 2, 2026
Pinpoint Asset Management 
Limited
628,700
1.54%
0.11%
August 2, 2026
Amazing Mountain Limited
628,700
1.54%
0.11%
August 2, 2026
Great China Motivation Fund Phase 
II L.P.
628,700
1.54%
0.11%
August 2, 2026
Notes:
1.	
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering.
2.	
In accordance with the relevant cornerstone investment agreements, the required lock-up ends 
on August 2, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or 
transferring H Shares subscribed for pursuant to the relevant cornerstone investment agreements 
after the indicated date.

<<<PAGE 15>>>
– 15 –
PLACEE CONCENTRATION ANALYSIS
Placees
Number of H 
Shares allotted
Allotment as % 
of International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as % 
of International 
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
% of total issued 
share capital 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Top 1
5,957,700
16.19%
13.88%
14.57%
12.67%
5,957,700
1.06%
1.05%
Top 5
15,154,200
41.18%
35.30%
37.06%
32.23%
15,154,200
2.70%
2.67%
Top 10
22,200,800
60.33%
51.71%
54.29%
47.21%
22,200,800
3.96%
3.92%
Top 25
32,670,400
88.78%
76.09%
79.90%
69.48%
32,670,400
5.82%
5.76%
Note
*  Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 16>>>
– 16 –
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders
Number of H 
Shares allotted
Allotment as % 
of International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as % 
of International 
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
% of total issued 
H Shares 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total issued 
H Shares 
upon Listing 
(assuming the 
Over-allotment 
Option is  
exercised and 
new H Shares 
are issued)
Number of 
Shares held 
upon Listing
Top 1
5,957,700
16.19%
13.88%
14.57%
12.67%
5,957,700
1.06%
1.05%
5,957,700
Top 5
15,154,200
41.18%
35.30%
37.06%
32.23%
15,154,200
2.70%
2.67%
15,154,200
Top 10
22,200,800
60.33%
51.71%
54.29%
47.21%
22,200,800
3.96%
3.92%
22,200,800
Top 25
32,670,400
88.78%
76.09%
79.90%
69.48%
32,670,400
5.82%
5.76%
32,670,400
Note
*  Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 17>>>
– 17 –
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number of H 
Shares allotted
Allotment as % 
of International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as % 
of International 
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
Number of 
Shares held 
upon Listing
% of total issued 
share capital 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total issued 
share capital 
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
0
260,828,779
46.50%
46.00%
Top 5
0
0.00%
0.00%
0.00%
0.00%
0
388,562,300
69.27%
68.53%
Top 10
9,928,500
26.98%
23.12%
24.28%
21.11%
9,928,500
425,106,410
75.79%
74.97%
Top 25(1)
14,383,400
39.08%
33.50%
35.18%
30.59%
14,383,400
464,920,584
82.89%
81.99%
Note
*  Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.
(1)	
Among the top 25 placees, certain placees are also existing Shareholders. To the best knowledge, information and belief of the Company after due 
enquiry, details of the allocations to the existing minority Shareholders holding more than 1% of the issued share capital of the Company immediately 
prior to the completion of the Global Offering will be disclosed in this announcement. Please refer to the section headed “Allotees with waiver from 
strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the Placing Guidelines in relation to subscription for 
H Shares by existing minority Shareholders holding more than 1% of the issued share capital of the Company immediately prior to the completion 
of the Global Offering and/or their close associates” in this announcement. Save for Taikang Life Insurance Co., Ltd and Great China Motivation 
Fund Phase II L.P. who held more than 1% of the issued share capital of the Company immediately prior to the completion of the Global Offering, 
respectively, each of the top 25 placees who are also existing shareholders held less than 1% of the issued share capital of the Company immediately 
prior to the completion of the Global Offering, and the number of A Shares held by the existing shareholders except Taikang Life Insurance Co., Ltd 
and Great China Motivation Fund Phase II L.P. are not counted into the number of Shares held upon Listing.

<<<PAGE 18>>>
– 18 –
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications 
made by the public will be conditionally allocated on the basis set out below:
BASIS OF ALLOTMENT FOR PRESS ANNOUNCEMENT
NO. OF SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT
POOL A
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
100
37,167
5,575 out of 37,167 to receive 100 Shares
15.00%
200
4,163
833 out of 4,163 to receive 100 Shares
10.00%
300
2,771
665 out of 2,771 to receive 100 Shares
8.00%
400
1,703
443 out of 1,703 to receive 100 Shares
6.50%
500
1,576
433 out of 1,576 to receive 100 Shares
5.49%
600
791
237 out of 791 to receive 100 Shares
4.99%
700
658
207 out of 658 to receive 100 Shares
4.49%
800
655
210 out of 655 to receive 100 Shares
4.01%
900
403
134 out of 403 to receive 100 Shares
3.69%
1,000
3,497
1,189 out of 3,497 to receive 100 Shares
3.40%
1,500
1,380
513 out of 1,380 to receive 100 Shares
2.48%
2,000
1,452
581 out of 1,452 to receive 100 Shares
2.00%
2,500
770
350 out of 770 to receive 100 Shares
1.82%
3,000
887
476 out of 887 to receive 100 Shares
1.79%
3,500
435
269 out of 435 to receive 100 Shares
1.77%
4,000
701
485 out of 701 to receive 100 Shares
1.73%
4,500
252
194 out of 252 to receive 100 Shares
1.71%
5,000
748
636 out of 748 to receive 100 Shares
1.70%
6,000
488
100 Shares
1.67%
7,000
364
100 Shares plus 44 out of 364 to receive additional 100 Shares
1.60%
8,000
363
100 Shares plus 93 out of 363 to receive additional 100 Shares
1.57%
9,000
259
100 Shares plus 98 out of 259 to receive additional 100 Shares
1.53%
10,000
1,757
100 Shares plus 879 out of 1,757 to receive additional 100 Shares
1.50%
20,000
1,335
200 Shares
1.00%
 
64,575
Total number of Pool A successful applicants: 17,996
 

<<<PAGE 19>>>
– 19 –
NO. OF SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT
POOL B
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
30,000
1,158
500 Shares plus 1,027 out of 1,158 to  
receive additional 100 Shares
1.96%
40,000
258
600 Shares
1.50%
50,000
190
700 Shares
1.40%
60,000
84
800 Shares
1.33%
70,000
39
900 Shares
1.29%
80,000
83
1,000 Shares
1.25%
90,000
23
1,100 Shares
1.22%
100,000
144
1,200 Shares
1.20%
200,000
59
2,300 Shares
1.15%
300,000
18
3,400 Shares
1.13%
400,000
13
4,400 Shares
1.10%
500,000
22
5,400 Shares
1.08%
750,000
8
8,000 Shares
1.07%
1,000,000
11
10,600 Shares
1.06%
1,500,000
2
15,800 Shares
1.05%
2,044,500
5
21,300 Shares
1.04%
 
2,117
Total number of Pool B successful applicants: 2,117
 

<<<PAGE 20>>>
– 20 –
As of the date of this announcement, the relevant subscription monies previously deposited 
in the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/
or in respect of which consent has been obtained, the Company has complied with the 
Listing Rules and guidance materials in relation to the placing, allotment and listing of the 
Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by 
the placees or the public (as the case may be) directly or indirectly for each Offer Share 
subscribed for or purchased by them was the same as the final Offer Price in addition to any 
brokerage, AFRC transaction levy, SFC transaction levy and Stock Exchange trading fee 
payable.
OTHERS/ADDITIONAL INFORMATION
Allocations of Offer Shares to the existing Shareholders and/or their close associates 
and Cornerstone Investors with a consent under paragraph 18 of Chapter 4.15 of the 
Guide for New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under 
paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the 
Company to allocate further Offer Shares in the International Offering to certain Cornerstone 
Investors as placees, subject to the following conditions:
(a).	 the final offering size of the Global Offering will be of a total value of at least HK$1 
billion;
(b).	 the Offer Shares allocated to all existing Shareholders and their close associates 
(whether as cornerstone investors and/or as placees) as permitted under the Size-based 
Exemption (as defined in the Guide for New Listing Applicants) do not exceed 30% of 
the total number of the H Shares offered under the Global Offering;

<<<PAGE 21>>>
– 21 –
(c).	 each Director, chief executive and Controlling Shareholders of the Company confirms 
that no securities have been allocated to them or their respective close associates under 
the Size-based Exemption; and
(d).	 details of the allocation to existing Shareholders and/or their close associates and 
Cornerstone Investors under the Size-based Exemption will be disclosed in this 
announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to existing Shareholders and/or their close 
associates and Cornerstone Investors, please refer to the section headed “Allotment Results 
Details — International Offer — Allottees with Waivers/Consents Obtained” in this 
announcement.
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, 
a consent under paragraph 1C(1) of the Placing Guidelines to permit UBS AM Singapore 
to participate in the Global Offering as a Cornerstone Investor. For details of the allocations 
to UBS AM Singapore, please refer to the section headed “Allotment Results Details — 
International Offer — Cornerstone Investors” in this announcement.
In addition, under the International Offering, certain Offer Shares were placed to connected 
clients of their connected distributors pursuant to the Placing Guidelines as placees. Please 
refer to the section headed “Allotment Results Details — International Offering — Allottees 
with Waivers/Consents Obtained” in this announcement for details. The Company has 
applied to the Stock Exchange for, and the Stock Exchange has granted, a consent under 
paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such Offer 
Shares in the International Offering to the connected clients as placees. The allocation of 
Offer Shares to such connected clients is in compliance with all the conditions under the 
consent granted by the Stock Exchange. Details of the placement to connected clients as 
placees are set out below.

<<<PAGE 22>>>
– 22 –
No.
Connected Distributor
Connected Client
Relationship with the 
Connected Distributor
Whether the connected 
clients will hold the 
beneficial interests of 
the Offer Shares on 
a non-discretionary 
basis or discretionary 
basis for independent 
third parties
Number of Offer 
Shares to be allocated 
to the connected client
Approximate 
percentage of Offer 
Shares allocated to 
the connected client 
(assuming the Over-
allotment Option is 
not exercised)
Approximate 
percentage of total 
issued share capital 
after the Global 
Offering (assuming 
the Over-allotment 
Option is not 
exercised)
1.
Huatai Financial Holdings 
(Hong Kong) Limited 
(“HTFH”)
HTCI (1)
Each of HTCI and HTFH 
is an indirect wholly-
owned subsidiary of Huatai 
Securities Co., Ltd. (“Huatai 
Securities”).
Non-discretionary basis
331,600
0.81%
0.06%
2.
UBS AG Hong Kong Branch 
(“UBS HK”), the global 
wealth management division 
of UBS AG Singapore Branch 
(“UBS SG WM”) and the 
global wealth management 
division of UBS AG Hong 
Kong Branch (“UBS HK 
WM”)
UBS AM Singapore (2)
UBS AM Singapore is a 
member of the same group of 
companies as UBS HK, UBS 
SG WM and UBS HK WM.
Discretionary basis
202,000
0.49%
0.04%
3.
China International Capital 
Corporation Hong Kong 
Securities Limited 
(“CICCHKS”)
CICC FT (3)
CICC FT is a member of the 
same group as CICCHKS.
Non-discretionary
120,900
0.30%
0.02%

<<<PAGE 23>>>
– 23 –
No.
Connected Distributor
Connected Client
Relationship with the 
Connected Distributor
Whether the connected 
clients will hold the 
beneficial interests of 
the Offer Shares on 
a non-discretionary 
basis or discretionary 
basis for independent 
third parties
Number of Offer 
Shares to be allocated 
to the connected client
Approximate 
percentage of Offer 
Shares allocated to 
the connected client 
(assuming the Over-
allotment Option is 
not exercised)
Approximate 
percentage of total 
issued share capital 
after the Global 
Offering (assuming 
the Over-allotment 
Option is not 
exercised)
4.
GF Securities (Hong Kong) 
Brokerage Limited (“GF 
Securities”)
E Fund Management (4)
Each of E Fund Management, E 
Fund HK and Value Partners 
is a member of the same 
group with GF Securities.
Discretionary
169,000
0.41%
0.03%
5.
E Fund HK (4)
Discretionary
21,000
0.05%
0.00%(8)
6.
Value Partners (5)
Discretionary
32,000
0.08%
0.01%
7.
Guotai Junan Securities (Hong 
Kong) Limited (“GTJA”)
Fullgoal Fund (6)
Each of Fullgoal Fund and 
Fullgoal HK is a member of 
the same group of companies 
as GTJA.
Discretionary
43,600
0.11%
0.01%
8.
Fullgoal HK (6)
Discretionary
33,000
0.08%
0.01%
9.
GTJA Investments (7)
GTJA Investments is a member 
of same group of GTJA.
Non-Discretionary basis
2,800
0.01%
0.00%(8)

<<<PAGE 24>>>
– 24 –
Notes:
1.	
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial 
public offerings (“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products 
issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading 
activities. In connection with such products, the licensed domestic securities firms, through their Hong 
Kong affiliates, may participate in Hong Kong IPOs either as placees or cornerstone investors (the 
“Cross-border Derivatives Trading Regime”).
Huatai Securities, the shares of which are listed on both the Shanghai Stock Exchange (stock code: 
601688) and the Stock Exchange (stock code: 6886), is one of the domestic securities firms licensed to 
undertake cross-border derivatives trading activities. Huatai Securities entered into an International 
Swaps and Derivatives Association agreement (the “ISDA Agreement”) with its indirectly 
wholly-owned subsidiary, HTCI to set out the principal terms of any future total return swap between 
Huatai Securities and HTCI.
HTFH is a Joint Sponsor, Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint 
Lead Manager in connection with the Global Offering. Pursuant to the ISDA Agreement, HTCI, which 
intends to participate in the Global Offering as a placee, will hold the beneficial interest of the Offer 
Shares on a non-discretionary basis as the single underlying holder under a back-to-back total return 
swap (the “Back-to-back TRS”) to be entered by HTCI in connection with a Client TRS (as defined 
below) placed by and fully funded (i.e. with no financing provided by HTCI) by the Huatai Ultimate 
Clients (as defined below), by which, HTCI will, subject to customary fees and commissions, pass the 
full economic exposure of the Offer Shares ultimately to the Huatai Ultimate Clients, which in effect, 
HTCI will hold the beneficial interest of the Offer Shares on behalf of the Huatai Ultimate Clients. 
HTFH and HTCI are indirectly wholly-owned subsidiaries of Huatai Securities. Accordingly, HTCI is 
considered as a “connected client” of HTFH pursuant to paragraph 1B(7) of the Placing Guidelines.
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the “Huatai Ultimate 
Clients”) cannot directly subscribe for the Offer Shares but may invest in derivative products issued 
by domestic securities firms licenced to undertake cross-border derivatives trading activities, such as 
Huatai Securities, with the Offer Shares as the underlying assets. Instead of directly subscribing for 
the Offer Shares, the Huatai Ultimate Clients, through its investment manager, will place a total return 
swap order (the “Client TRS”) with Huatai Securities in connection with the Company’s IPO and 
Huatai Securities will place a Back-to-back TRS order to HTCI on the terms of the ISDA Agreement. In 
order to hedge its exposure under the Back-to-back TRS, HTCI participates in the Company’s IPO and 
subscribes the Offer Shares through placing order with HTFH during the International Offering.
To the best of HTCI’s knowledge and after making all reasonable enquiries, each of the Huatai 
Ultimate Clients is an independent third party of (i) the Company, the connected person or the 
associates thereof, and (ii) HTCI, HTFH and the companies which are members of the same group of 
HTCI.

<<<PAGE 25>>>
– 25 –
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
stock borrowing purposes.
HTCI will lend out its holding of underlying Offer Shares in the form of stock borrowing loans 
consistent with market practice to lower its finance costs, provided that HTCI has the ability to call 
back the Offer Shares on loan at any time in order to satisfy its obligations under the Back-to-back 
TRS to ensure the economic interests are ultimately passed to the Huatai Ultimate Clients.

<<<PAGE 26>>>
– 26 –
2.	
UBS AM Singapore will hold the beneficial interests of the Offer Shares on a discretionary basis for 
and on behalf of the underlying clients, each of whom is an independent third party of the Company, its 
subsidiaries, its Controlling Shareholders, its substantial shareholders, UBS AM Singapore, UBS HK, 
UBS HK WM, UBS SG WM and the companies which are members of the same group of UBS HK, UBS 
HK WM and UBS SG WM.
In addition to the Offer Shares subscribed for as a placee, UBS AM Singapore was allocated 
1,571,900 Offer Shares as a Cornerstone Investor in the International Offering. UBS HK is an 
Overall Coordinator. UBS AM Singapore and UBS HK are members of the same group of companies. 
Accordingly, UBS AM Singapore is a connected client. The Company has, therefore, applied for, and 
the Stock Exchange has granted, a consent under paragraph 1C(1) of Appendix F1 to the Listing 
Rules to permit UBS AM Singapore to participate in the Global Offering as a Cornerstone Investor. 
For details, please refer to the section headed “Waivers and Exemptions — Consent in respect of the 
Proposed Subscription of H Shares by Certain Cornerstone Investor who is Connected Client” in the 
Prospectus. With the appointment of UBS SG WM and UBS HK WM as additional sub-distributors in 
the Global Offering, the relationship among UBS AM Singapore, UBS HK, UBS SG WM and UBS HK 
WM also falls within the scope of the aforementioned waiver.
3.	
CICCHKS is a distributor in connection with the Global Offering. CICC FT is a wholly-owned 
subsidiary of China International Capital Corporation Limited (“CICCL”), of which its shares are 
listed on the Shanghai Stock Exchange (stock code: 601995) and the Stock Exchange (stock code: 
3908). CICCHKS is an indirectly wholly owned subsidiary of CICCL. Therefore, CICC FT and 
CICCHKS are members of the same group of companies.
CICC FT and CICCL will enter into a series of cross border delta-one OTC swap transactions 
(collectively, the “OTC Swaps”) with each other and the ultimate clients (the “CICC FT Ultimate 
Clients”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to 
hedge the OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed 
to the CICC FT Ultimate Clients, subject to customary fees and commissions. The OTC Swaps will 
be fully funded by the CICC FT Ultimate Clients. During the terms of the OTC Swaps, all economic 
returns of the Offer Shares subscribed by CICC FT will be passed to the CICC FT Ultimate Clients 
and all economic loss shall be borne by the CICC FT Ultimate Clients through the OTC Swaps, and 
CICC FT will not take part in any economic return or bear any economic loss in relation to the Offer 
Shares. Despite that CICC FT will hold the legal title of the Offer Shares by itself, it will not exercise 
the voting rights attaching to the relevant Offer Shares during the terms of the OTC Swaps according 
to its internal policy.
To the best of CICC FT’s knowledge and after making all reasonable enquiries, each of the CICC FT 
Ultimate Clients is an independent third party of the CICC FT and is not connected to the Company 
for the purpose of the Listing Rules.
4.	
Each of E Fund Management and E Fund HK will hold the beneficial interests of the Offer Shares on a 
discretionary basis for and on behalf of their underlying clients, each of whom is an independent third 
party of the Company, its subsidiaries, its Controlling Shareholders, its substantial shareholders, GF 
Securities and the companies which are members of the same group of GF Securities.

<<<PAGE 27>>>
– 27 –
5.	
GF Securities is an indirect wholly-owned subsidiary of GF Securities Co. Ltd. (Stock Code: 1776). 
Value Partners is a wholly-owned subsidiary of Value Partners Group Limited (Stock Code: 806), 
“VPGL”). By virtue of GF Securities Co. Ltd. is interested in 20.04% of the issued share capital 
of VPGL which renders Value Partners an associate of GF Securities. Value Partners is therefore a 
member of the same group of companies as GF Securities. Value Partners will hold the beneficial 
interests of the Offer Shares on a discretionary basis for and on behalf of its underlying clients, each 
of whom is an independent third party of the Company, its subsidiaries, its Controlling Shareholders, 
its substantial shareholders, GF Securities and the companies which are members of the same group of 
GF Securities.
6.	
Fullgoal HK, a wholly owned subsidiary of Fullgoal Fund, which is owned by Guotai Haitong 
Securities Co., Ltd. (SEHK: 2611) (“Guotai Haitong”) as to 27.775%. GTJA is a subsidiary of 
Guotai Haitong. Therefore, each of Fullgoal Fund and Fullgoal HK is a member of the same group of 
companies as GTJA. Each of Fullgoal Fund and Fullgoal HK will hold the beneficial interests of the 
Offer Shares on a discretionary basis for and on behalf of their underlying clients, each of whom is an 
independent third party of the Company, its subsidiaries, its Controlling Shareholders, its substantial 
shareholders, GTJA and the companies which are members of the same group of GTJA.
7.	
GTJA Investments shall hold the Offer Shares for hedging purpose as the single underlying asset of 
several sets of back-to-back total return swap transaction (the “GTHT Back-to-back TRS”) to be 
entered into between GTJA Investments and Guotai Haitong Securities Co., Ltd. (the “GTHT Onshore 
Parent”) in connection with several total return swap orders (the “GTHT Client TRS”) to be entered 
into by GTHT Onshore Parent and several ultimate clients (the “GTHT Onshore Ultimate Client”), 
respectively. Such GTHT Client TRS is to be fully funded by the GTHT Onshore Ultimate Client. GTJA 
Investments will hold the Offer Shares on a non-discretionary basis for the purpose of hedging the 
economic exposure under the GTHT Back-to-back TRS and GTHT Client TRS only, During the tenor 
of the GTHT Client TRS, all economic returns of the Offer Shares will be passed to the GTHT Onshore 
Ultimate Clients and all economic losses shall be borne by the GTHT Onshore Ultimate Client, 
subject to the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS, and GTJA 
Investments will not take part in any economic return or bear any economic loss in relation to the 
price of the Offer Shares. The GTHT Onshore Ultimate Client may request to redeem the Offer Shares 
at their own discretion, upon which GTJA Investments shall dispose of the Offer Shares and settle the 
GTHT Back-to-back TRS and GTHT Client TRS in cash in accordance with the terms and conditions 
of the GTHT Back-to-back TRS and GTHT Client TRS documents. Due to its internal policy, GTJA 
Investments will not exercise the voting right attaching to the Offer Shares during the tenor of the 
GTHT Back-to-back TRS and GTHT Client TRS.

<<<PAGE 28>>>
– 28 –
To the best knowledge, information and belief of GTJA Investments after due enquiry, the GTHT 
Onshore Ultimate Clients and their respective ultimate beneficial owners holding 30% or more interest 
include:
Funds
Ultimate 
beneficial 
owner(s) who 
hold 30% 
interest or more 
in the fund
Remark
Zhonghe (tianjin) Investment management Co. Ltd — 
Zhonghe Capital Cultivation 810 Private Securities 
Investment Fund (錦綉中和(天津)投資管理有限公司 — 
中和資本耕耘810號私募證券投資基金)
Wang Diansuo  
(王殿鎖)
UBO with over 
30% interest
Shanghai Weining Investment Mangement Co, Ltd — Weining 
Qihang No. 1 Private Securities Investment Fund  
(上海衛寧私募基金管理有限公司 — 衛寧啟航1號私募
證券投資基金)
Liu Yutao  
(劉育濤)
UBO with over 
30% interest
Shanghai Minghong Investment Management Co., Ltd — 
Minghong No. 1 Multi-strategy Hedging Fund  
(上海明汯投資管理有限公司 — 明汯多策略對沖1號基
金)
Qiu Huiming  
(裘慧明)
General Partner
To the best knowledge of GTJA Investments and after making all reasonable enquiries, (i) GTJA 
Investments has confirmed that, to the best of their knowledge, each of the GTHT Onshore Ultimate 
Clients and the ultimate beneficial owners holding 30% or more interest of the GTHT Onshore 
Ultimate Clients is an independent third party of GTJA Investments, GTJA and the companies which 
are members of the same group of companies as GTJA, and (ii) GTJA Investments is not a collective 
investment scheme which is not authorised by the SFC nor is expected to hold the Offer Shares on 
behalf of such scheme.
8.	
Denotes less than 0.01%.

<<<PAGE 29>>>
– 29 –
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate 
such Offer Shares in the International Offering to the connected clients listed above. The 
allocation of Offer Shares to such connected clients is in compliance with all the conditions 
under the consent granted by the Stock Exchange.
Allocations under the Employee Preferential Offering
Of the 36,800,900 Offer Shares initially being offered under the International Offering, 
670,600 Offer Shares, representing approximately 1.82% of the Offer Shares initially 
available for subscription under the International Offering, are available for subscription 
as Employee Reserved Shares by the Eligible Employees on a preferential basis under 
the Employee Preferential Offering according to Rule 10.01 of the Listing Rules. For 
details, please refer to the section headed “Structure of the Global Offering — Employee 
Preferential Offering” of the Prospectus.
669,700 Offer Shares have been placed to 67 Eligible Employees pursuant to the Employee 
Preferential Offering, representing approximately 1.64% of the total number of Offer Shares 
initially available under the Global Offering (before exercise of the Over-allotment Option). 
Each Eligible Employees confirms that he/she is and remains as an employee as of the date 
of the Prospectus and is not a core connected person of the Company.
Allocation of H Shares to existing minority Shareholders and their close associates
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted 
to the Company, a waiver from strict compliance with the requirements under Rule 10.04 
and consent under Paragraph 1C(2) of Appendix F1 to the Listing Rules to permit H Shares 
in the International Offering to be placed to certain existing minority Shareholders who will 
participate only as either cornerstone investors or placees (but not both) in the International 
Offering (together, the “Permitted Existing Shareholders”) on the conditions that each of 
them:
(a).	 together with their close associates, holds less than 5% of the voting rights in our 
Company prior to the completion of the Global Offering;
(b).	 is not and will not be, a core connected person of our Company or any close associate 
of any such core connected person immediately prior to or following the Global 
Offering;
(c).	 does not have the power to appoint any Director and/or have any other special rights;

<<<PAGE 30>>>
– 30 –
(d).	 allocation to the Permitted Existing Shareholders and their close associates will 
not affect our Company’s ability to satisfy the public float requirement under Rule 
19A.13A(2)(b) of the Listing Rules; and
(e).	 that no preferential treatment has been, nor will be, given to any of the Permitted 
Existing Shareholders or their close associates by virtue of their relationship with our 
Company in any allocation in the International Offering.
Please refer to the section headed “Waivers and Exemptions — Allocation of H Shares to 
existing minority Shareholders and their close associates ” in the Prospectus for further 
details of the waiver and consent.
Each of the Joint Sponsors and the Company has provided the required confirmations as 
elaborated in the Prospectus. In particular, as the Company’s A Shares are listed on the Main 
Board of Shanghai Stock Exchange since May 2021, the Company has a highly extensive 
base of existing Shareholders and disclosure of details of allocations to all existing minority 
Shareholders will not be meaningful to investors, the proposed disclosure threshold, i.e. 
condition (ii) of the waiver and consent which provides that details of the allocation to the 
existing minority Shareholders holding more than 1% of the issued share capital of the 
Company immediately prior to the completion of the Global Offering will be disclosed in 
this announcement, is appropriate.
All allocations of Offer Shares to the existing minority Shareholders are in compliance with 
all the conditions under the waiver and consent granted by the Stock Exchange.

<<<PAGE 31>>>
– 31 –
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong 
Limited (the “Stock Exchange”) and Hong Kong Securities Clearing Company Limited 
(“HKSCC”) take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part 
of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in 
or into the United States (including its territories and possessions, any state of the United 
States and the District of Columbia). This announcement does not constitute or form 
a part of any offer or solicitation to purchase or subscribe for securities in the United 
States. The securities mentioned herein have not been, and will not be, registered under 
the United States Securities Act of 1933, as amended (the “U.S. Securities Act”). The 
securities may not be offered or sold in the United States except pursuant to an exemption 
from the registration requirements of the U.S. Securities Act and in compliance with any 
applicable state securities laws, or outside the United States unless in compliance with 
Regulation S under the U.S. Securities Act. There will be no public offer of securities in 
the United States.
The Offer Shares are being offered and sold (1) solely to qualified institutional buyers 
as defined in Rule 144A under the U.S. Securities Act pursuant to an exemption from 
registration under the U.S. Securities Act and (2) outside the United States in offshore 
transactions in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation 
or offer to acquire, purchase or subscribe for securities. This announcement is not a 
prospectus. Potential investors should read the Prospectus dated January 26, 2026 issued 
by Eastroc Beverage (Group) Co., Ltd. for detailed information about the Global Offering 
described below before deciding whether or not to invest in the H Shares thereby being 
offered.
* Potential investors of the Offer Shares should note that the Joint Sponsors and the 
Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters and 
the Capital Market Intermediaries) shall be entitled to terminate their obligations under 
the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any 
of the events set out in the section headed “Underwriting — Underwriting Arrangements 
and Expenses — Hong Kong Public Offering — Hong Kong Underwriting Agreement — 
Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong 
time) on the Listing Date (which is currently expected to be on February 3, 2026).

<<<PAGE 32>>>
– 32 –
PUBLIC FLOAT
Immediately after the completion of the Global Offering (before any exercise of the 
Over-allotment Option), the total market value of the H Shares to be held by the public is 
expected to be approximately HK$10,140.70 million, calculated based on the final Offer 
Price of HK$248.00 per H Share, which is higher than the prescribed expected market 
value of H Shares required to be held in public hands of not less than HK$3,000,000,000 
under Rule 19A.13A(2)(b) of the Listing Rules, thereby satisfying Rule 19A.13A of the 
Listing Rules. Based on the final Offer Price of HK$248.00 per H Share, the minimum 
prescribed public float percentage under Rule 19A.13A(2)(b) of the Listing Rules would 
be approximately 2.16%, being the percentage derived by dividing HK$3,000,000,000 
by the total market value of the Company’s total issued shares at the time of Listing. 
The total number of the H Shares to be issued pursuant to the Global Offering represents 
approximately 7.29% of the total issued share capital of our Company (assuming the 
Over-allotment Option is not exercised and no H Shares will be allocated under the Global 
Offering to any core connected person of our Company or person which is not regarded 
as a member of the public under Rule 8.24 of the Listing Rules), which is higher than the 
minimum prescribed public float percentage under Rule 19A.13A(2)(b) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following 
the Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall 
not be counted towards the free float of the H Shares of the Company at the time of Listing. 
Based on the final Offer Price of HK$248.00 per H Share, the Company confirms the free 
float requirement under Rule 19A.13C(2)(a) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering (before 
any exercise of the Over-allotment Option): (i) no placee will, individually, be placed 
more than 10% of the enlarged issued share capital of the Company immediately after the 
Global Offering; (ii) there will not be any new substantial Shareholder under the Listing 
Rules immediately after the Global Offering; (iii) the three largest public shareholders of 
the Company do not hold more than 50% of the H shares in public hands at the time of the 
Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will 
be at least 300 Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the 
Listing Rules.

<<<PAGE 33>>>
– 33 –
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, 
February 3, 2026 (Hong Kong time), provided that the Global Offering has become 
unconditional and the right of termination described in the section headed “Underwriting — 
Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus has not been exercised. Investors who trade the H Shares on 
the basis of publicly available allocation details prior to the receipt of H Share certificates or 
prior to the H Share certificates becoming valid evidence of title do so entirely at their own 
risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on 
February 3, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the 
Stock Exchange will commence at 9:00 a.m. on February 3, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 100 H Shares each, and the stock code of the H Shares 
will be 09980.
By order of the Board
Eastroc Beverage (Group) Co., Ltd.
Mr. Lin Muqin
Chairman of the Board, Executive Director and 
Chief Executive Officer
Hong Kong, February 2, 2026
As at the date of this announcement, the Board comprises: (i) Mr. LIN Muqin, Mr. LIN Mugang, Mr. LU Yifu, 
Ms. JIANG Weiwei, Mr. ZHANG Lei and Mr. LIN Daiji as executive Directors; and (ii) Ms. ZHAO Yali, Ms. 
YOU Xiao, Mr. LI Hongbin and Mr. TAI Kwok Leung, Alexander as independent non-executive Directors.
