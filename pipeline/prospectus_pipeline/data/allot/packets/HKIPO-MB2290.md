# 配发结果公告抽取任务：2290.HK Lung Fung Group Holdings Limited

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**04/06/2026 19:43**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0604/2026060402521.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2290.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
(the “Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) 
take no responsibility for the contents of this announcement, make no representation as to 
its accuracy or completeness and expressly disclaim any liability whatsoever for any loss 
howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated 28 May 2026 (the “Prospectus”) of 
Lung Fung Group Holdings Limited (龍豐集團控股有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation 
or offer to acquire, purchase or subscribe for any securities. This announcement is not a 
prospectus. Potential investors should read the Prospectus for detailed information about the 
Company and the Global Offering described below before deciding whether or not to invest 
in the Offer Shares. Any investment decision in relation to the Offer Shares should be taken 
solely in reliance on the information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or 
into the United States (including its territories and possessions, any state of the United States 
and the District of Columbia). This announcement does not constitute or form a part of any 
offer or solicitation to purchase or subscribe for securities in the United States or in any other 
jurisdictions. The Offer Shares have not been, and will not be, registered under the United 
States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or 
securities law of any state or other jurisdiction of the United States. The Offer Shares may not 
be offered, sold, pledged or otherwise transferred within the United States, except pursuant to 
an available exemption from, or in a transaction not subject to, the registration requirements 
of the U.S. Securities Act. There will be no public offer of the Offer Shares in the United 
States. The Offer Shares are being offered and sold solely outside the United States in offshore 
transactions in reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, DBS Asia Capital Limited acts as the Sole Sponsor, 
Sponsor-Overall Coordinator and Overall Coordinator.
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinator (for 
itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong 
Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events 
set out in the section headed “Underwriting — Underwriting Arrangements and Expenses — 
Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior 
to 8:00 a.m. on the day that trading in the Shares commences on the Stock Exchange (which is 
currently expected to be on Friday, 5 June, 2026).

<<<PAGE 2>>>
– 2 –
Lung Fung Group Holdings Limited
龍豐集團控股有限公司
(Incorporated in the Cayman Islands with limited liability)
GLOBAL OFFERING
Number of Offer Shares under
the Global Offering
:
125,000,000 Shares
Number of Hong Kong Offer Shares
:
12,500,000 Shares
Number of International Offer Shares
:
112,500,000 Shares
Final Offer Price
:
HK$5.18 per Offer Share plus brokerage of
1.0%, SFC transaction levy of 0.0027%,
Stock Exchange trading fee of 0.00565%,
and AFRC transaction levy of 0.00015%
(payable in full on application in Hong
Kong dollars, subject to refund)
Nominal value
:
HK$0.0001 per Share
Stock code
:
2290
Sole Sponsor, Overall Coordinator, Sole Global Coordinator,
Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers
(in alphabetical order)

<<<PAGE 3>>>
– 3 –
LUNG FUNG GROUP HOLDINGS LIMITED (龍豐集團控股有限公司)
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated 28 May 2026 (the “Prospectus”) 
issued by Lung Fung Group Holdings Limited (龍豐集團控股有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, Shareholders and prospective investors should be aware that the price 
of the Shares could move substantially even with a small number of Shares traded and 
should exercise extreme caution when dealing in the Shares.
SUMMARY
Company information
Stock code
2290
Stock short name
LUNG FUNG GROUP
Dealings commencement date
5 June 2026*
*  see note at the end of the announcement
Price Information
Final Offer Price
HK$5.18
Offer Price Range
HK$5.18 to HK$6.38
Offer Shares and Share Capital
Number of Offer Shares
125,000,000
Final Number of Offer Shares in Hong Kong Public 
Offering
12,500,000
Final Number of Offer Shares in International 
Offering
112,500,000
Number of issued Shares upon Listing
500,000,000 
Over-allocation
No. of Offer Shares over-allocated
0
Proceeds
Gross proceeds (1)
HK$647.5 million
Less: Estimated listing expenses payable based on 
the final Offer Price
HK$47.9 million
Net proceeds(2)
HK$599.6 million
Notes:
1.	
Gross proceeds refer to the amount to which the Company is entitled to receive.
2.	
For details of the use of proceeds, please refer to the section headed “Future Plans and Use of 
Proceeds” in the Prospectus.

<<<PAGE 4>>>
– 4 –
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
133,189
No. of successful applications
16,359
Subscription level
664.92 times
No. of Offer Shares initially available under the Hong Kong 
Public Offering
12,500,000
No. of Offer Shares reallocated from the International Offering 
(reallocation)
0
Final no. of Offer Shares under the Hong Kong Public Offering 
(after reallocation)
12,500,000
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering
10%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can refer to 
https://www.hkeipo.hk/iporesult to perform a search by name or identification number or https://www.hkeipo.hk/
iporesult for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
78
Subscription Level
3.18 times
No. of Offer Shares initially available under the International 
Offering
112,500,000
No. of Offer Shares reallocated to the Hong Kong Public 
Offering (reallocation)
0
Final no. of Offer Shares under the International Offering (after 
reallocation)
112,500,000
% of Offer Shares under the International Offering to the 
Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, (i) none 
of the Offer Shares subscribed by the placees and the public have been financed directly or 
indirectly by the Company, any of the Directors, chief executives, controlling shareholders, 
substantial shareholders, existing shareholders of the Company or any of its subsidiaries 
or their respective close associates; and (ii) none of the placees and the public who have 
purchased the Offer Shares are accustomed to taking instructions from the Company, any of 
the Directors, chief executives, controlling shareholders, substantial shareholders, existing 
shareholders of the Company or any of its subsidiaries or their respective close associates in 
relation to the acquisition, disposal, voting or other disposition of Shares registered in his/
her/its name or otherwise held by him/her/it.

<<<PAGE 5>>>
– 5 –
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
% of shareholding in 
the Company subject to 
lock-up undertakings 
upon Listing
Last day subject to the lock-
up undertakings(1)
TTK Holding Limited(2)
375,000,000 Shares
75.00%
4 December 2026 
(First Six-Month Period)(3)
4 June 2027 
(Second Six-Month Period)(4)
Subtotal
375,000,000 Shares
75.00%
Notes:
1.	
In accordance with the relevant Listing Rule/guidance materials, the required lock-up for the first six-
month period ends on 4 December 2026 and for the second six-month period, on 4 June 2027. For further 
details, please refer to “Underwriting — Underwriting Arrangements and Expenses — Undertakings to 
the Stock Exchange Pursuant to the Listing Rules — Undertakings by our Controlling Shareholders” in 
the Prospectus.
2.	
TTK Holding Limited (“TTK Holding”) is an investment holding company owned by Mr. Tse Siu 
Hoi (“Mr. Tse”), Ms. Chan Yuen Fong Shirley (“Mrs. Tse”) and Ms. Tse Chui Ying (“Ms. Tse”) as 
to 97.29%, 2.70% and 0.01%, respectively. TTK Holding, Mr. Tse, Mrs. Tse and Ms. Tse will be the 
controlling shareholders of the Company and will continue to hold a controlling interest in the Company 
upon completion of the Global Offering. For further details, please refer to “Relationship with Our 
Controlling Shareholders” in the Prospectus.
3.	
The Controlling Shareholder may dispose of or transfer Shares after the indicated date subject to that the 
Controlling Shareholder will not cease to be a controlling shareholder (as defined in the Listing Rules) 
of the Company.
4.	
The Controlling Shareholder will cease to be prohibited from disposing of or transferring Shares after 
the indicated date.

<<<PAGE 6>>>
– 6 –
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
Shares allotted
Allotment as % of 
the International 
Offering
Allotment 
as % of total 
Offer Shares 
Number of 
Shares held 
upon Listing
% of total issued 
share capital 
upon Listing
Top 1
9,200,000
8.18%
7.36%
9,200,000
1.84%
Top 5
38,025,000
33.80%
30.42%
38,025,000
7.61%
Top 10
62,345,000
55.42%
49.88%
62,345,000
12.47%
Top 25
97,706,500
86.85%
78.17%
97,706,500
19.54%
Notes:
*	
Ranking of placees is based on the number of Shares allotted to the placees.
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders*
Number of 
Shares allotted
Allotment as % of 
the International 
Offering 
Allotment 
as % of total 
Offer Shares
Number of 
Shares held 
upon Listing
% of total issued 
share capital 
upon Listing 
Top 1
0
0.00%
0.00%
375,000,000
75.00%
Top 5
32,025,000
28.47%
25.62%
407,025,000
81.41%
Top 10
58,545,000
52.04%
46.84%
433,545,000
86.71%
Top 25
96,606,500
85.87%
77.29%
471,606,500
94.32%
Notes:
*	
Ranking of Shareholders is based on the number of Shares held by the Shareholders upon Listing.

<<<PAGE 7>>>
– 7 –
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made 
by the public will be conditionally allocated on the basis set out below:
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
POOL A
500
46,124
2,307 out of 46,124 applicants to receive 500 Shares
5.00%
1,000
9,299
576 out of 9,299 applicants to receive 500 Shares
3.10%
1,500
25,001
1,753 out of 25,001 applicants to receive 500 Shares
2.34%
2,000
3,063
235 out of 3,063 applicants to receive 500 Shares
1.92%
2,500
2,111
174 out of 2,111 applicants to receive 500 Shares
1.65%
3,000
1,604
140 out of 1,604 applicants to receive 500 Shares
1.45%
3,500
940
86 out of 940 applicants to receive 500 Shares
1.31%
4,000
1,002
95 out of 1,002 applicants to receive 500 Shares
1.19%
4,500
806
80 out of 806 applicants to receive 500 Shares
1.10%
5,000
4,594
467 out of 4,594 applicants to receive 500 Shares
1.02%
6,000
1,330
143 out of 1,330 applicants to receive 500 Shares
0.90%
7,000
9,591
1,080 out of 9,591 applicants to receive 500 Shares
0.80%
8,000
1,014
119 out of 1,014 applicants to receive 500 Shares
0.73%
9,000
672
82 out of 672 applicants to receive 500 Shares
0.68%
10,000
2,937
369 out of 2,937 applicants to receive 500 Shares
0.63%
15,000
2,287
326 out of 2,287 applicants to receive 500 Shares
0.48%
20,000
1,160
181 out of 1,160 applicants to receive 500 Shares
0.39%
25,000
898
150 out of 898 applicants to receive 500 Shares
0.33%
30,000
858
152 out of 858 applicants to receive 500 Shares
0.30%
35,000
551
102 out of 551 applicants to receive 500 Shares
0.26%
40,000
535
103 out of 535 applicants to receive 500 Shares
0.24%
45,000
432
87 out of 432 applicants to receive 500 Shares
0.22%
50,000
1,223
252 out of 1,223 applicants to receive 500 Shares
0.21%
60,000
745
163 out of 745 applicants to receive 500 Shares
0.18%
70,000
750
172 out of 750 applicants to receive 500 Shares
0.16%
80,000
755
180 out of 755 applicants to receive 500 Shares
0.15%
90,000
604
150 out of 604 applicants to receive 500 Shares
0.14%
100,000
3,414
871 out of 3,414 applicants to receive 500 Shares
0.13%

<<<PAGE 8>>>
– 8 –
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
200,000
1,545
488 out of 1,545 applicants to receive 500 Shares
0.08%
300,000
1,070
383 out of 1,070 applicants to receive 500 Shares
0.06%
400,000
708
277 out of 708 applicants to receive 500 Shares
0.05%
500,000
582
244 out of 582 applicants to receive 500 Shares
0.04%
600,000
424
188 out of 424 applicants to receive 500 Shares
0.04%
700,000
701
325 out of 701 applicants to receive 500 Shares
0.03%
 
Total
129,330
Total number of Pool A successful applicants: 12,500
 
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
POOL B
800,000
1,432
1,000 Shares plus 940 out of 1,432 applicants to receive
  an additional 500 Shares
0.17%
900,000
538
1,000 Shares plus 386 out of 538 applicants to receive
  an additional 500 Shares
0.15%
1,000,000
1,109
1,000 Shares plus 888 out of 1,109 applicants to receive
  an additional 500 Shares
0.14%
2,000,000
370
2,000 Shares
0.10%
3,000,000
137
2,500 Shares
0.08%
4,000,000
94
3,000 Shares
0.08%
5,000,000
33
3,500 Shares
0.07%
6,250,000
146
4,000 Shares
0.06%
 
Total
3,859
Total number of Pool B successful applicants: 3,859
 
As of the date of this announcement, the relevant subscription monies previously deposited 
in the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers for any inquiries.

<<<PAGE 9>>>
– 9 –
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s Shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or 
indirectly, provided by the Company, the Controlling Shareholders, the Directors or syndicate 
members to any placees or the public (as the case may be) and the consideration paid by 
the placees or the public (as the case may be) directly or indirectly for each Offer Share 
subscribed for or purchased by them was the same as the final Offer Price in addition to any 
brokerage, AFRC transaction levy, SFC transaction levy and Stock Exchange trading fee 
payable.

<<<PAGE 10>>>
– 10 –
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
(the “Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) 
take no responsibility for the contents of this announcement, make no representation as to 
its accuracy or completeness and expressly disclaim any liability whatsoever for any loss 
howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in 
or into the United States (including its territories and possessions, any state of the United 
States and the District of Columbia). This announcement does not constitute or form a 
part of any offer or solicitation to purchase or subscribe for securities in the United States 
or in any other jurisdictions. The Offer Shares have not been, and will not be, registered 
under the United States Securities Act of 1933 as amended from time to time (the “U.S. 
Securities Act”) or securities law of any state or other jurisdiction of the United States. The 
Offer Shares may not be offered, sold, pledged or otherwise transferred within the United 
States, except pursuant to an available exemption from, or in a transaction not subject to, 
the registration requirements of the U.S. Securities Act. There will be no public offer of 
the Offer Shares in the United States. The Offer Shares are being offered and sold solely 
outside the United States in offshore transactions in reliance on Regulation S under the U.S. 
Securities Act.
This announcement is for information purposes only and does not constitute an invitation 
or offer to acquire, purchase or subscribe for any securities. This announcement is not a 
prospectus. Potential investors should read the Prospectus for detailed information about 
the Company and the Global Offering described below before deciding whether or not to 
invest in the Offer Shares. Any investment decision in relation to the Offer Shares should be 
taken solely in reliance on the information provided in the Prospectus.
*	
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinator (for itself and 
on behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds 
for Termination” in the Prospectus at any time prior to 8:00 a.m. on the day that trading in the Shares 
commences on the Stock Exchange (which is currently expected to be on Friday, 5 June, 2026).

<<<PAGE 11>>>
– 11 –
PUBLIC FLOAT AND FREE FLOAT
Based on (i) the final Offer Price of HK$5.18 per Offer Share and (ii) 500,000,000 Shares 
in issue immediately upon completion of the Global Offering, it is expected that the market 
capitalization of our Shares at the time of Listing will be HK$2,590,000,000. Under Rule 
8.08(1) of the Listing Rules, in the event the expected market value of the class of securities 
new to listing upon Listing does not exceed HK$6,000,000,000, at least 25% of the total 
issued Shares must be held by the public upon Listing. Immediately following the completion 
of the Global Offering, the total number of the Shares held by the public represents 25% of the 
total issued Shares. Therefore, the Company will be able to satisfy the public float requirement 
under Rule 8.08(1) of the Listing Rules immediately upon Listing.
Based on the final Offer Price of HK$5.18 per Offer Share, the Company will be able to 
satisfy the free float requirement under Rule 8.08A of the Listing Rules immediately upon 
Listing.
The Directors confirm that, immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public Shareholders 
of the Company do not hold more than 50% of the Shares in public hands at the time of the 
Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will 
be at least 300 Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the 
Listing Rules.
COMMENCEMENT OF DEALINGS
The Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, 5 June, 
2026, provided that the Global Offering has become unconditional and the right of termination 
described in the section headed “Underwriting — Underwriting Arrangements and Expenses 
— Hong Kong Public Offering — Grounds for Termination” in the Prospectus has not been 
exercised. Investors who trade the Shares on the basis of publicly available allocation details 
prior to the receipt of Share certificates or prior to the Share certificates becoming valid 
evidence of title do so entirely at their own risk.

<<<PAGE 12>>>
– 12 –
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. in Hong 
Kong on Friday, 5 June, 2026, it is expected that dealings in the Shares on the Stock Exchange 
will commence at 9:00 a.m. on Friday, 5 June, 2026. The Shares will be traded in board lots of 
500 Shares each and the stock code of our Shares will be 2290.
By Order of the Board
Lung Fung Group Holdings Limited
Tse Siu Hoi
Executive Director and Chairman of the Board
Hong Kong, 4 June 2026
As at the date of this announcement, Directors of the Company are: (i) Mr. Tse Siu Hoi and 
Ms. Tse Chui Ying as executive Directors; and (ii) Mr. Chu Woon Ming, Mr. Yau Sheung Yu 
and Ms. Woo Pui Yan Joyce as independent non-executive Directors.
