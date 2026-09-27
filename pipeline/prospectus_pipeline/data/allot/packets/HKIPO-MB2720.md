# 配发结果公告抽取任务：2720.HK Ridge Outdoor International Limited

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**09/02/2026 21:10**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0209/2026020901096.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2720.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the prospectus dated January 31, 2026 (the “Prospectus”) issued by Ridge Outdoor International Limited 
(樂欣戶外國際有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an offer or an invitation to induce an 
offer by any person to acquire, purchase or subscribe for any securities of the Company. This announcement is not a 
prospectus. Potential investors should read the Prospectus for detailed information about the Company and the Global 
Offering described below before deciding whether or not to invest in the Shares. Any investment decision in relation 
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
Potential investors of the Offer Shares should note that the Sole Sponsor and Sponsor-Overall Coordinator (for itself 
and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong Underwriting Agreement 
with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting — 
Underwriting Arrangements — Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time 
prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Tuesday, February 10, 
2026).

<<<PAGE 2>>>
2
Ridge Outdoor International Limited
樂欣戶外國際有限公司
(Incorporated in the Cayman Islands with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
28,205,000 Shares
Number of Hong Kong Offer Shares
:
2,820,500 Shares
Number of International Offer Shares
:
25,384,500 Shares
Final Offer Price
:
HK$12.25 per Share, plus brokerage of 
 1.0%, SFC transaction levy of 0.0027%, 
 AFRC transaction levy of 0.00015%, and 
 Hong Kong Stock Exchange trading fee 
 of 0.00565%
Nominal value
:
US$0.0005 per Share
Stock code
:
2720
Sole Sponsor, Sponsor-Overall Coordinator, Sole Overall Coordinator
and Sole Global Coordinator
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
Ridge Outdoor International Limited
樂欣戶外國際有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated January 31, 2026 (the “Prospectus”) issued by 
Ridge Outdoor International Limited (樂欣戶外國際有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the Shares could 
move substantially even with a small number of Shares traded and should exercise extreme 
caution when dealing in the Shares.
SUMMARY
Company information
Stock code
2720
Stock short name
RIDGE OUTDOOR
Dealings commencement date
February 10, 2026
Price Information
Final Offer Price
HK$12.25
Offer Shares and Share Capital
Number of Offer Shares
28,205,000
Number of Offer Shares in Hong Kong Public Offering
2,820,500
Number of offer shares in International Offering
25,384,500
Number of issued shares upon Listing
128,205,000
Proceeds
Gross proceeds (Note)
HK$345.5 million
Less: Estimated listing expenses payable based on final 
Offer Price
HK$60.4 million
Net proceeds
HK$285.2 million
Note: Gross proceeds refers to the amount to which the issuer is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” in the Prospectus.

<<<PAGE 4>>>
4
ALLOTMENT RESULTS DETAILS
PUBLIC OFFER
No. of valid applications
111,036
No. of successful applications
5,641
Subscription level
3,654.23 times
Reallocation
N/A
No. of Offer Shares initially available under the Hong Kong 
Public Offering
2,820,500
No. of Offer Shares reallocated from the International Offering
N/A
Final no. of Offer Shares under the Hong Kong Public Offering
2,820,500
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering
10%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can refer to 
https://www.hkeipo.hk/iporesult to perform a search by identification number or https://www.hkeipo.hk/iporesult 
for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
74
Subscription Level
2.94 times
No. of Offer Shares initially available under the International 
Offering
25,384,500
No. of Offer Shares reallocated to the Hong Kong Public Offering
N/A
Final No. of Offer Shares under the International Offering
25,384,500
% of Offer Shares under the International Offering to the Global 
Offering
90%

<<<PAGE 5>>>
5
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, Controlling Shareholders, 
substantial shareholders, existing shareholders of the Company or any of its subsidiaries or their 
respective close associates; and (ii) none of the placees and the public who have purchased the 
Offer Shares are accustomed to taking instructions from the Company, any of the Directors, 
chief executive of the Company, Controlling Shareholders, substantial shareholders, existing 
shareholders of the Company or any of its subsidiaries or their respective close associates in 
relation to the acquisition, disposal, voting or other disposition of Shares registered in his/her/its 
name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares
% of total 
issued share 
capital after the 
Global 
Offering
Existing 
shareholders 
or their close 
associates
Orbit Venture Capital 
Management Co., Limited 
(“Orbit VC”)
6,530,500
23.15%
5.09%
No
Huangshan Dejun 
Enterprise Management 
Co., Ltd. (黃山德鈞企業管
理有限公司) (“Huangshan 
Dejun”)
4,081,500
14.47%
3.18%
No
Total
10,612,000
37.62%
8.28% Note 1
Notes:
1. 
This figure has been rounded up to 2 decimal places.

<<<PAGE 6>>>
6
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number 
of shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding 
in  the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings Note 1
Mr. Yang
94,770,000
73.92%
August 9, 2026 
(First Six-month 
Period) Note 3
February 9, 2027 
(Second Six-month 
Period) Note 4
GreatCast Note 2
88,062,400
68.69%
August 9, 2026 
(First Six-month 
Period) Note 3
February 9, 2027 
(Second Six-month 
Period) Note 4
Taihong
6,707,600
5.23%
August 9, 2026 
(First Six-month 
Period) Note 3
February 9, 2027 
(Second Six-month 
Period) Note 4
Outrider Partnership Note 2
6,707,600
5.23%
August 9, 2026 
(First Six-month 
Period) Note 3
February 9, 2027 
(Second Six-month 
Period) Note 4

<<<PAGE 7>>>
7
Notes:
1. 
In accordance with the relevant Listing Rule/guidance materials, the required lock-up for the first six-month 
period ends on August 9, 2026 and for the second six-month period ends on February 9, 2027.
2. 
As of the Latest Practicable Date, Mr. Yang was (i) indirectly interested in approximately 88.06% of the 
total issued share capital of the Company through GreatCast, a company wholly owned by him; and (ii) 
deemed to be interested in approximately 6.71% of the total issued share capital of the Company held by 
Outrider Partnership, by virtue of his role as the sole shareholder of Taihong, the general partner of Outrider 
Partnership. By virtue of the SFO, Mr. Yang is deemed to be interested in all the Shares held by GreatCast 
and Outrider Partnership. For details, please refer to the section headed “Relationship with Controlling 
Shareholders” and “Substantial Shareholders” in the Prospectus.
3. 
The Controlling Shareholders may dispose of or transfer Shares after the indicated date subject to that the 
Controlling Shareholders will not cease to be a Controlling Shareholder.
4. 
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after the 
indicated date.
Cornerstone Investors
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued Shares 
after the 
Global Offering 
subject to 
lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings Note 1
Orbit VC
6,530,500
5.09%
February 9, 2027
Huangshan Dejun
4,081,500
3.18%
February 9, 2027
Subtotal
10,612,000
8.28% Note 2
Notes:
1. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on February 
9, 2027. The Cornerstone Investors will cease to be prohibited from disposing of or transferring Shares 
subscribed for pursuant to the relevant cornerstone investment agreements after the indicated date.
2. 
This figure has been rounded up to 2 decimal places.

<<<PAGE 8>>>
8
PLACEE CONCENTRATION ANALYSIS
Placees Note 1
Number 
of Shares 
allotted
Allotment 
as % of 
International 
Offering
Allotment as 
% of total 
Offer Shares
Number of 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing
Top 1
6,530,500
25.73%
23.15%
6,530,500
5.09%
Top 5
16,896,000
66.56%
59.90%
16,896,000
13.18%
Top 10
22,364,000
88.10%
79.29%
22,364,000
17.44%
Top 25
25,343,000
99.84%
89.85%
25,343,000
19.77%
Note:
1. 
Ranking of placees is based on the number of Shares allotted to the places.
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders Note 1
Number 
of Shares 
allotted
Allotment as
% of 
International 
Offering
Allotment as
% of total 
Offer Shares
Number of 
Shares Held 
upon Listing
% of the 
total issued 
share capital 
upon Listing
Top 1
–
N/A
N/A
94,770,000
73.92%
Top 5
13,469,000
53.06%
47.75%
113,239,000
88.33%
Top 10
20,731,000
81.67%
73.50%
120,501,000
93.99%
Top 25
25,318,000
99.74%
89.76%
125,318,000
97.75%
Note:
1. 
Ranking of Shareholders is based on the number of Shares held by the Shareholders upon Listing.

<<<PAGE 9>>>
9
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, 111,036 valid applications 
made by the public will be conditionally allocated on the basis set out below:
Number 
of Shares 
applied for
Number 
of valid 
applications
Pool A
Approximate 
percentage 
allotted of the 
total number 
of Shares 
applied for
Basis of allocation/ballot
500
56,367
564 out of 56,367 applicants to receive 500 shares
1.00%
1,000
5,942
80 out of 5,942 applicants to receive 500 shares
0.67%
1,500
3,415
55 out of 3,415 applicants to receive 500 shares
0.54%
2,000
1,906
35 out of 1,906 applicants to receive 500 shares
0.46%
2,500
1,895
38 out of 1,895 applicants to receive 500 shares
0.40%
3,000
1,182
26 out of 1,182 applicants to receive 500 shares
0.37%
3,500
853
20 out of 853 applicants to receive 500 shares
0.33%
4,000
3,168
76 out of 3,168 applicants to receive 500 shares
0.30%
4,500
714
18 out of 714 applicants to receive 500 shares
0.28%
5,000
2,832
75 out of 2,832 applicants to receive 500 shares
0.26%
6,000
896
26 out of 896 applicants to receive 500 shares
0.24%
7,000
799
25 out of 799 applicants to receive 500 shares
0.22%
8,000
1,347
44 out of 1,347 applicants to receive 500 shares
0.20%
9,000
603
21 out of 603 applicants to receive 500 shares
0.19%
10,000
2,116
75 out of 2,116 applicants to receive 500 shares
0.18%
15,000
1,498
63 out of 1,498 applicants to receive 500 shares
0.14%
20,000
1,050
50 out of 1,050 applicants to receive 500 shares
0.12%
25,000
796
42 out of 796 applicants to receive 500 shares
0.11%
30,000
679
38 out of 679 applicants to receive 500 shares
0.09%
35,000
567
34 out of 567 applicants to receive 500 shares
0.09%
40,000
554
35 out of 554 applicants to receive 500 shares
0.08%
45,000
502
34 out of 502 applicants to receive 500 shares
0.08%
50,000
1,117
78 out of 1,117 applicants to receive 500 shares
0.07%
60,000
678
51 out of 678 applicants to receive 500 shares
0.06%
70,000
737
59 out of 737 applicants to receive 500 shares
0.06%
80,000
730
62 out of 730 applicants to receive 500 shares
0.05%
90,000
465
42 out of 465 applicants to receive 500 shares
0.05%
100,000
2,783
258 out of 2,783 applicants to receive 500 shares
0.05%
200,000
1,890
234 out of 1,890 applicants to receive 500 shares
0.03%
300,000
1,456
214 out of 1,456 applicants to receive 500 shares
0.02%
400,000
2,109
349 out of 2,109 applicants to receive 500 shares
0.02%
Total
101,646
Total number of Pool A successful applicants: 2,821

<<<PAGE 10>>>
10
Number 
of Shares 
applied for
Number 
of valid 
applications
Pool B
Approximate 
percentage 
allotted of the 
total number 
of Shares 
applied for
Basis of allocation/ballot
500,000
3,575
715 out of 3,575 applicants to receive 500 shares
0.02%
600,000
915
213 out of 915 applicants to receive 500 shares
0.02%
700,000
676
178 out of 676 applicants to receive 500 shares
0.02%
800,000
666
196 out of 666 applicants to receive 500 shares
0.02%
900,000
375
122 out of 375 applicants to receive 500 shares
0.02%
1,000,000
546
193 out of 546 applicants to receive 500 shares
0.02%
1,200,000
493
202 out of 493 applicants to receive 500 shares
0.02%
1,410,000
2,144
1,001 out of 2,144 applicants to receive 500 shares
0.02%
Total
9,390
Total number of Pool B successful applicants: 2,820
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and trading fee payable.

<<<PAGE 11>>>
11
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
Prospectus dated January 31, 2026 issued by the Company for detailed information about the 
Company and the Global Offering described below before deciding whether or not to invest in 
the Shares. Any investment decision in relation to the Offer Shares should be taken solely in 
reliance on the information provided in the Prospectus.
* Potential investors of the Offer Shares should note that the Sole Sponsor and Sponsor-
Overall Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall be entitled to 
terminate the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of 
any of the events set out in the section headed “Underwriting — Underwriting Arrangements — 
Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to 
8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Tuesday, 
February 10, 2026).

<<<PAGE 12>>>
12
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering, 33,435,000 Shares, the total number of 
the Shares held by the public represents approximately 26.08% of the total issued share capital 
of the Company, which is higher than the prescribed percentage of Shares required to be held in 
public hands of 25% which is the minimum prescribed public float percentage applicable to our 
Shares under Rule 8.08 of the Listing Rules, thereby satisfying Rule 8.08(1) of the Listing Rules at 
the time of the Listing.
Each of the Cornerstone Investors has agreed to a lock-up period of twelve months following the 
Listing Date. As such, Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the Shares of the Company at the time of Listing. Based on the 
final Offer Price of HK$12.25 per Share, the Company satisfies the free float requirement under 
Rule 8.08A of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering: (i) no placee 
will, individually, be placed more than 10% of the enlarged issued share capital of the Company 
immediately after the Global Offering; (ii) there will not be any new substantial Shareholder under 
the Listing Rules immediately after the Global Offering; (iii) the three largest public shareholders 
of the Company do not hold more than 50% of the Shares in public hands at the time of the Listing 
in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 
Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
Share certificates will only become valid evidence of title at 8:00 a.m. (Hong Kong time) on 
Tuesday, February 10, 2026, provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting — Underwriting 
Arrangements — Hong Kong Public Offering — Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade Shares prior to the receipt of Share certificates or the 
Share certificates becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong Kong time) 
on Tuesday, February 10, 2026, it is expected that dealings in the Shares on the Stock Exchange 
will commence at 9:00 a.m. on Tuesday, February 10, 2026. The Shares will be traded in board 
lots of 500 Shares each. The stock code of the Shares will be 2720.
By order of the Board
Ridge Outdoor International Limited
Lei Yang
Executive Director
Hong Kong, February 9, 2026
As at the date of this announcement, the Board comprises: (i) Ms. Lei Yang and Mr. Wu Guihua 
as executive Directors; (ii) Mr. Yang Baoqing and Ms. Wen Meixia as non-executive Directors; 
and (iii) Mr. Ding Feng, Mr. Han Hongling and Mr. Shu Yuanchao as independent non-executive 
Directors.
