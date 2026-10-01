# 配发结果公告抽取任务：3228.HK Shenzhen Kinwong Electronic Co., Ltd. - H Shares

- 公告：Announcement of Final Offer Price and Allotment Results
- 刊发时间（港交所元数据）：**28/09/2026 22:15**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0928/2026092801965.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3228.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated September 21, 2026 (the “Prospectus”) issued by Shenzhen Kinwong Electronic Co., 
Ltd. (深圳市景旺電子股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities of the Company. This announcement is not a prospectus. Potential investors should read 
the Prospectus for detailed information about the Company and the Global Offering described below before deciding 
whether or not to invest in the Offer Shares. Any investment decision in relation to the Offer Shares should be taken 
solely in reliance on the information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for any securities 
in the United States or in any other jurisdictions. The Offer Shares have not been, and will not be, registered under the 
United States Securities Act of 1933, as amended (the “U.S. Securities Act”) or securities law of any state or other 
jurisdiction of the United States. The Offer Shares may not be offered, sold, pledged or otherwise transferred within 
the United States, except pursuant to an available exemption from, or in a transaction not subject to, the registration 
requirements of the U.S. Securities Act. There will be no public offer of the Offer Shares in the United States. The 
Offer Shares are being offered and sold solely (1) to qualified institutional buyers as defined in Rule 144A under the 
U.S. Securities Act pursuant to Rule 144A or another available exemption from registration under the U.S. Securities 
Act and (2) outside the United States in offshore transactions in reliance on Regulation S under the U.S. Securities 
Act.
In connection with the Global Offering, CITIC Securities (Hong Kong) Limited, Merrill Lynch (Asia Pacific) Limited 
and Guolian Securities International Capital Market Co., Limited act as the Joint Sponsors; CLSA Limited, Merrill 
Lynch (Asia Pacific) Limited and Guolian Securities International Capital Co., Limited act as the Sponsor-Overall 
Coordinators and the Overall Coordinators.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out 
in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/
or not resident in Hong Kong. Potential investors of the Offer Shares should note that the Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Agreements – Hong Kong Underwriting Agreement – Grounds for Termination” in the Prospectus 
at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Tuesday, 
September 29, 2026).

<<<PAGE 2>>>
2
Shenzhen Kinwong Electronic Co., Ltd.
（深圳市景旺電子股份有限公司）
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
72,944,300 H Shares
Number of Hong Kong Offer Shares
:
7,294,500 H Shares 
Number of International Offer Shares
:
65,649,800 H Shares 
Offer Price
:
HK$69.88 per H Share, plus brokerage of  
 1.0%, SFC transaction levy of 0.0027%,  
 AFRC transaction levy of 0.00015% and  
 Hong Kong Stock Exchange trading fee  
 of 0.00565% (payable in full on  
 application in Hong Kong dollars and  
 subject to refund) 
Nominal value
:
RMB1.00 per Share
Stock code
:
3228
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators, Joint Global
Coordinators, Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
SHENZHEN KINWONG ELECTRONIC CO., LTD.
深圳市景旺電子股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated September 21, 2026 (the “Prospectus”) issued 
by Shenzhen Kinwong Electronic Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
3228
Stock short name
KINWONG
Dealings commencement date
September 29, 2026*
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$69.88
Maximum Offer Price
HK$69.88
Offer Shares and Share Capital
Number of Offer Shares
72,944,300 H Shares
Final Number of Offer Shares in Hong Kong Public 
Offering
7,294,500 H Shares
Final Number of Offer Shares in International Offering
65,649,800 H Shares
Number of issued shares upon Listing
1,074,268,341 Shares
Proceeds
Gross proceeds (Note)
HK$5,097.3 million
Less:  Estimated listing expenses payable based on Final 
Offer Price
HK$(136.7) million
Net proceeds
HK$4,960.6 million
Note: Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.

<<<PAGE 4>>>
4
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
61,273
No. of successful applications
17,090
Subscription level
94.25 times
Reallocation
No
No. of Offer Shares initially available under the Hong Kong 
Public Offering
7,294,500
No. of Offer Shares reallocated from the International 
Offering
0
Final no. of Offer Shares under the Hong Kong Public 
Offering
7,294,500
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering
10.00%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by name or identification number or www.hkeipo.hk/IPOResult 
for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
143
Subscription Level
10.57 times
No. of Offer Shares initially available under the 
International Offering
65,649,800
Final no. of Offer Shares under the International Offering
65,649,800
% of Offer Shares under the International Offering to the 
Global Offering
90.00%

<<<PAGE 5>>>
5
The Directors confirm that, to the best of their knowledge, information and belief, save for 
(a) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the 
Stock Exchange to permit H Shares in the International Offering to be placed to certain existing 
minority Shareholders who (i) hold less than 5% of the voting rights in the Company prior to the 
completion of the Global Offering and (ii) are not and will not become (upon the completion of the 
Global Offering) core connected persons of the Company or the close associates of any such core 
connected person (the “Existing Minority Shareholders”), and (b) a consent under paragraph 18 
of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to, among other 
things, allocate further H Shares in the International Offering to certain existing Shareholders, 
Cornerstone Investors and/or their close associates, (i) none of the Offer Shares subscribed by the 
placees and the public offer subscribers have been financed directly or indirectly by the Company, 
any of the Directors, chief executive of the Company, Controlling Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates; (ii) none of the placees and the public offer subscribers who have subscribed for 
or purchased the Offer Shares are accustomed to taking instructions from the Company, any of the 
Directors, chief executive of the Company, Controlling Shareholders, substantial Shareholders, 
existing Shareholders of the Company or any of its subsidiaries or their respective close associates 
in relation to the acquisition, disposal, voting or other disposition of H Shares registered in his/her/
its name or otherwise held by him/her/it; (iii) there is no side agreement or arrangement between 
the Company, any of the Directors, chief executive of the Company, the Controlling Shareholders, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or their 
respective close associates, on one hand, and the public offer subscribers or the placees who have 
subscribed for or purchased the Offer Shares, on the other hand; (iv) there is no side agreement 
or arrangement between the Company, any of the Directors, chief executive of the Company, the 
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company or any 
of its subsidiaries or their respective close associates, on one hand, and any other parties, on the 
other hand, in connection with the subscription, purchase, disposal, turnover or valuation of the 
Shares (which, for the avoidance of doubt, does not include agreements entered into with the price 
stabilising managers); and (v) no rebate has been, directly or indirectly, provided by the Company, 
any of the Directors, chief executive of the Company, the Controlling Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates, or syndicate members, or any other brokers involved in the Global Offering, to 
any investors in the Hong Kong Public Offering or placees in the International Offering.

<<<PAGE 6>>>
6
The placees in the International Offering include the following:
Cornerstone Investors
Investor Note 1
No. of Offer
Shares allocated
Approximate % 
of total issued H 
Shares after 
the Global 
Offering Note 2,3
Approximate % 
of total
issued share
capital after the 
Global Offering
Existing
shareholders or
their close
associates
CPE Redwood Investment Limited 
(“CPE Redwood”)
5,611,100
7.69%
0.52%
No
VERTEXVEST HOLDING PTE. 
LTD. (“Zhongji Innolight”)
5,611,100
7.69%
0.52%
No
HONG KONG MASON 
ELECTRONICS CO., LIMITED (香
港麥遜電子有限公司) (“Hong Kong 
Mason”)
5,611,100
7.69%
0.52%
No
Cambridge Industries Group 
Telecommunication Limited (“CIG”)
3,366,600
4.62%
0.31%
No
CloudAlpha Capital Management 
Limited (奇點資產管理有限公司) 
(“CloudAlpha Capital”)
2,805,500
3.85%
0.26%
No
E Fund
(i) 
E Fund Management Co., Ltd. 
(“E Fund Management”)
(ii) 
E Fund Management (Hong 
Kong) Co., Ltd. (易方達資產管
理(香港)有限公司) (“E Fund 
HK”)
2,805,400
3.85%
0.26%
Yes
1,851,600
2.54%
0.17%
Yes
953,800
1.31%
0.09%
Yes
Bosera Asset Management 
(International) Co., Limited (“Bosera 
International”)
2,244,400
3.08%
0.21%
No
Seven Grand Managers, LLC (“Seven 
Grand”)
1,683,300
2.31%
0.16%
No
3W Fund Management Limited (“3W 
Fund”)
1,122,200
1.54%
0.10%
No

<<<PAGE 7>>>
7
Investor Note 1
No. of Offer
Shares allocated
Approximate % 
of total issued H 
Shares after 
the Global 
Offering Note 2,3
Approximate % 
of total
issued share
capital after the 
Global Offering
Existing
shareholders or
their close
associates
Tianhong Asset Management Co., Ltd. 
(天弘基金管理有限公司) (“Tianhong 
Fund”)
1,122,200
1.54%
0.10%
No
Ninety One Asia Pte. Limited 
(“Ninety One Asia”)
1,122,200
1.54%
0.10%
No
JPMorgan Asset Management (Asia 
Pacific) Limited (“JPMAMAPL”)
561,100
0.77%
0.05%
No
Baring Asset Management (Asia) 
Limited (霸菱資產管理(亞洲)有限公
司) (“Barings”)
561,100
0.77%
0.05%
No
Kingboard Investments Limited (建滔
投資有限公司) (“KHL”)
561,100
0.77%
0.05%
No
Total
34,788,400
47.69%
3.24%
Notes:
1. 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in 
the Prospectus.
2. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
3. 
In addition to the Offer Shares subscribed for as Cornerstone Investors, certain Cornerstone Investors and/
or their close associates were allocated further Offer Shares as placees in the International Offering. Please 
refer to the section headed “Allotment Results Details – Allottees with Waivers/Consents Obtained” in this 
announcement for details. Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-
up restrictions as indicated below. For details, please refer to the section headed “Lock-up Undertakings – 
Cornerstone Investors” in this announcement.

<<<PAGE 8>>>
8
Allottees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares allocated
Approximate % 
of total issued  
H Shares after 
the Global 
Offering Note 4
Approximate % 
of total issued 
share capital 
after the Global 
Offering Note 5
Relationship*
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 
1C(2) of the Placing Guidelines in relation to subscription for H Shares by existing minority Shareholders 
immediately prior to the completion of the Global Offering and/or their close associates Note 1
E Fund (comprising of E Fund 
Management and E Fund HK)
2,805,400
3.85%
0.26%
A Cornerstone
Investor and a 
close associate 
of an existing 
minority 
Shareholder
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation 
to allocations of further H Shares to existing Shareholders and Cornerstone Investors and/or their close 
associates Note 2
CIG
561,100
0.77%
0.05%
A Cornerstone 
Investor
CloudAlpha Capital
505,000
0.69%
0.05%
A Cornerstone 
Investor
E Fund Management
333,300
0.46%
0.03%
A Cornerstone 
Investor and a 
close associate 
of an existing 
minority 
Shareholder
E Fund HK
171,700
0.24%
0.02%
A Cornerstone 
Investor and a 
close associate 
of an existing 
minority 
Shareholder
Bosera International
404,000
0.55%
0.04%
A Cornerstone 
Investor
Seven Grand
303,000
0.42%
0.03%
A Cornerstone 
Investor
3W Fund
202,000
0.28%
0.02%
A Cornerstone 
Investor

<<<PAGE 9>>>
9
Investor
No. of Offer 
Shares allocated
Approximate % 
of total issued  
H Shares after 
the Global 
Offering Note 4
Approximate % 
of total issued 
share capital 
after the Global 
Offering Note 5
Relationship*
Tianhong – CEB-THFUND GLOBAL 
NEW EN V EQ SEC I
20,200
0.03%
0.002%
A close 
associate of 
Tianhong Fund, 
a Cornerstone 
Investor
Tianhong – CMB-THAM-GLO ADV 
MANUFACTURING FD
181,800
0.25%
0.02%
A close 
associate of 
Tianhong Fund, 
a Cornerstone 
Investor
Ninety One Asia
202,000
0.28%
0.02%
A Cornerstone 
Investor
JPMAMAPL
1,122,200
1.54%
0.10%
A Cornerstone 
Investor
Baring
280,500
0.38%
0.03%
A Cornerstone 
Investor
KHL
134,600
0.18%
0.01%
A Cornerstone 
Investor
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients Note 3
CITIC Securities International Capital 
Management Limited (“CSI”)
347,700
0.48%
0.03%
Connected client
as placee
CITIC Securities Asset Management 
(HK) Limited (“CITIC AM HK”)
11,200
0.02%
0.001%
Connected client
as placee
CITIC Securities Asset Management 
Company Limited (“CITIC AM”)
11,200
0.02%
0.001%
Connected client
as placee
E Fund Management
333,300
0.46%
0.03%
Connected client
as placee
E Fund HK
171,700
0.24%
0.02%
Connected client
as placee
Value Partners Limited (“VPL”)
63,100
0.09%
0.006%
Connected client 
as placee
Value Partners Hong Kong Limited 
(“VPHK”, together with VPL, “Value 
Partners”)
105,200
0.14%
0.01%
Connected client 
as placee
GF Securities Asset Management 
(Guangdong) Co., Ltd. (“GF 
Securities AM”)
381,400
0.52%
0.04%
Connected client
as placee

<<<PAGE 10>>>
10
Investor
No. of Offer 
Shares allocated
Approximate % 
of total issued  
H Shares after 
the Global 
Offering Note 4
Approximate % 
of total issued 
share capital 
after the Global 
Offering Note 5
Relationship*
GF International Investment 
Management Limited (“GF 
International”)
168,300
0.23%
0.02%
as placee
China International Capital 
Corporation Limited (“CICC”)
33,700
0.05%
0.003%
Connected client
as placee
Notes:
1. 
The Company has applied for, and the Stock Exchange has granted, a waiver from strict compliance with the requirements under 
Rule 10.04 of the Listing Rules and consent under Paragraph 1C(2) of the Placing Guidelines to permit H Shares in the International 
Offering to be placed to certain existing minority Shareholders and/or their close associates. Please refer to the section headed “Waivers 
and Exemptions – Waiver in respect of Allocation of H Shares to existing minority Shareholders and their Close Associates” of the 
Prospectus for details. The Stock Exchange granted the waiver on the condition that, among others, details of the allocation to the 
existing minority Shareholders of the Company immediately prior to the completion of the Global Offering will be disclosed in the 
Prospectus and/or allotment results announcement.
2. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the number of Offer Shares 
allocated to the investors as placees in the International Offering. For allocations of Offer Shares to the relevant investors as Cornerstone 
Investors, please refer to the section headed “Allotment Results Details – International Offering – Cornerstone Investors” in this 
announcement. For details of the consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocations of further H Shares to existing Shareholders, Cornerstone Investors and/or their close associates, please refer to the section 
headed “Others/Additional Information – Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines” in this announcement.
3. 
For details of the consents under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants 
in relation to allocations to connected clients, please refer to the section headed “Others/Additional Information – Placing to connected 
clients with a prior consent under paragraph 1C(1) of the Placing Guidelines” in this announcement.
4. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the Global 
Offering.
5. 
Only taking into account the H Shares allocated to the relevant investors under the Global Offering.

<<<PAGE 11>>>
11
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
subject to lock-up 
undertakings upon 
Listing Note 3
% of shareholding 
in the Company
subject to lock-up 
undertakings upon 
Listing
Last day subject 
to the lock-up 
undertakings Note 2
Jinghong Yongtai Note 4
280,075,322
—
26.07%
March 28, 2027 
(First Six-Month 
Period) Note 1
September 28, 2027 
(Second Six-Month 
Period) Note 2
Wise Able Investment Note 5
279,874,108
—
26.05%
March 28, 2027 
(First Six-Month 
Period) Note 1
September 28, 2027 
(Second Six-Month 
Period) Note 2
Mr. Liu Shaobai
478,805
—
0.04%
March 28, 2027 
(First Six-Month 
Period) Note 1
September 28, 2027 
(Second Six-Month 
Period) Note 2
Ms. Huang Xiaofen
417,940
—
0.04%
March 28, 2027 
(First Six-Month 
Period) Note 1
September 28, 2027 
(Second Six-Month 
Period) Note 2

<<<PAGE 12>>>
12
Notes:
1. 
The Controlling Shareholders may dispose of or transfer Share after the indicated date subject to that the 
Controlling Shareholders will not cease to be a Controlling Shareholder.
2. 
The Controlling Shareholders will cease to be prohibited from disposing or transferring Shares after the 
indicated date.
3. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
4. 
Jinghong Yongtai is 50% owned by Ms. Huang Xiaofen and 50% owned by Yizhao Investment, which is 51% 
owned by Ms. Huang Xiaofen and 49% owned by Mr. Liu Yu.
5. 
Wise Able Investment is 100% owned by Ms. Cheuk Kwan.
On January 6, 2020, Jinghong Yongtai, Wise Able Investment, Mr. Liu Shaobai, Ms. Huang Xiaofen and 
Ms. Cheuk Kwan entered into an acting in concert agreement (“Acting-in-concert Agreement”) pursuant to 
which, Mr. Liu Shaobai, Ms. Huang Xiaofen and Ms. Cheuk Kwan and their respectively controlled entities 
Jinghong Yongtai and Wise Able Investment shall act in concert to exercise their shareholder rights. On 
August 14, 2023, Mr. Liu Yu undertook to join the Acting-in-concert Agreement. Accordingly, Jinghong 
Yongtai, Wise Able Investment, Yizhao Investment (an entity in which Ms. Huang Xiaofen is the managing 
partner), Mr. Liu Shaobai, Ms. Huang Xiaofen, Ms. Cheuk Kwan and Mr. Liu Yu are the parties acting in 
concert. Therefore, Jinghong Yongtai, Wise Able Investment, Yizhao Investment, Mr. Liu Shaobai, Ms. 
Huang Xiaofen, Ms. Cheuk Kwan and Mr. Liu Yu were in aggregate entitled to exercise the voting rights 
attached to 560,846,175 Shares and approximately 56.01% of our Shares in issue and constituted our 
Controlling Shareholders Group as of the Latest Practicable Date. Our Controlling Shareholders Group will 
be collectively entitled to exercise the voting rights attached to approximately 52.21% of our Shares in issue 
immediately following the completion of the Global Offering.
Cornerstone Investors
Name
Number of H 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing Note 1
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing
Last day subject 
to the lock-up 
undertakings Note 2
CPE Redwood
5,611,100
7.69%
0.52%
March 28, 2027
Zhongji Innolight
5,611,100
7.69%
0.52%
March 28, 2027
Hong Kong Mason
5,611,100
7.69%
0.52%
March 28, 2027
CIG
3,366,600
4.62%
0.31%
March 28, 2027
CloudAlpha Capital
2,805,500
3.85%
0.26%
March 28, 2027
E Fund
(i) 
E Fund Management
(ii) 
E Fund HK
2,805,400
1,851,600
953,800
3.85%
2.54%
1.31%
0.26%
0.17%
0.09%
March 28, 2027
Bosera International
2,244,400
3.08%
0.21%
March 28, 2027

<<<PAGE 13>>>
13
Name
Number of H 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing Note 1
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing
Last day subject 
to the lock-up 
undertakings Note 2
Seven Grand
1,683,300
2.31%
0.16%
March 28, 2027
3W Fund
1,122,200
1.54%
0.10%
March 28, 2027
Tianhong Fund
1,122,200
1.54%
0.10%
March 28, 2027
Ninety One Asia
1,122,200
1.54%
0.10%
March 28, 2027
JPMAMAPL
561,100
0.77%
0.05%
March 28, 2027
Barings
561,100
0.77%
0.05%
March 28, 2027
KHL
561,100
0.77%
0.05%
March 28, 2027
Notes:
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
2. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on March 
28, 2027. The Cornerstone Investors will cease to be prohibited from disposing of or transferring H Shares 
subscribed for pursuant to the relevant cornerstone investment agreements after the indicated date.
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of
H Shares
Allotted
Allotment as
% of
International
Offering
Allotment as
% of
total Offer
Shares
Number of
H Shares held 
upon Listing
% of total
issued share
capital upon
Listing
Top 1
5,611,100
8.55%
7.69%
5,611,100 
0.52%
Top 5
24,127,600
36.75%
33.08%
24,127,600 
2.25%
Top 10
37,998,000
57.88%
52.09%
37,998,000 
3.54%
Top 25
54,669,300
83.27%
74.95%
54,669,300 
5.09%
Note
* 
Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 14>>>
14
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number
of
H Shares
allotted
Allotment as
% of
International
Offering
Allotment as
% of
total Offer
Shares
Number of H
Shares held upon 
Listing
% of total
issued share
capital upon
Listing
Top 1
5,611,100
8.55%
7.69%
5,611,100 
0.52%
Top 5
24,127,600
36.75%
33.08%
24,127,600 
2.25%
Top 10
37,998,000
57.88%
52.09%
37,998,000 
3.54%
Top 25
54,669,300
83.27%
74.95%
54,669,300 
5.09%
Note
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number of H 
Shares allotted
Allotment 
as % of 
International 
Offering
Allotment as % 
of total Offer 
Shares
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
Top 1
0
0.00%
0.00%
0
560,846,175
52.21%
Top 5
538,500
0.82%
0.74%
538,500
639,350,767
59.51%
Top 10
20,682,200
31.50%
28.35%
20,682,200
670,869,813
62.45%
Top 25
31,421,600
47.86%
43.08%
31,421,600
730,155,155
67.97%
Note
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 15>>>
15
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
Pool A
Approximate
percentage
allotted of the
Number
Number
total number of
of H Shares
of valid
H Shares applied
applied for
applications
Basis of allocation/ballot
for
100
23,208
697 out of 23,208 applicants to receive 100 H Shares
3.00%
200
3,303
182 out of 3,303 applicants to receive 100 H Shares
2.76%
300
1,947
153 out of 1,947 applicants to receive 100 H Shares
2.62%
400
1,319
134 out of 1,319 applicants to receive 100 H Shares
2.54%
500
3,306
407 out of 3,306 applicants to receive 100 H Shares
2.46%
600
641
93 out of 641 applicants to receive 100 H Shares
2.42%
700
8,559
1,413 out of 8,559 applicants to receive 100 H Shares
2.36%
800
471
88 out of 471 applicants to receive 100 H Shares
2.34%
900
257
53 out of 257 applicants to receive 100 H Shares
2.29%
1,000
3,030
684 out of 3,030 applicants to receive 100 H Shares
2.26%
1,500
960
309 out of 960 applicants to receive 100 H Shares
2.15%
2,000
995
412 out of 995 applicants to receive 100 H Shares
2.07%
2,500
482
243 out of 482 applicants to receive 100 H Shares
2.02%
3,000
695
411 out of 695 applicants to receive 100 H Shares
1.97%
3,500
291
197 out of 291 applicants to receive 100 H Shares
1.93%
4,000
386
294 out of 386 applicants to receive 100 H Shares
1.90%
4,500
255
215 out of 255 applicants to receive 100 H Shares
1.87%
5,000
833
770 out of 833 applicants to receive 100 H Shares
1.85%
6,000
445
100 H Shares plus 38 out of 445 applicants to receive an additional 100 H Shares
1.81%
7,000
399
100 H Shares plus 97 out of 399 applicants to receive an additional 100 H Shares
1.78%
8,000
388
100 H Shares plus 154 out of 388 applicants to receive an additional 100 H Shares
1.75%
9,000
232
100 H Shares plus 127 out of 232 applicants to receive an additional 100 H Shares
1.72%
10,000
1,855
100 H Shares plus 1,291 out of 1,855 applicants to receive an additional 100 H Shares
1.70%
20,000
1,294
300 H Shares plus 146 out of 1,294 applicants to receive an additional 100 H Shares
1.56%
30,000
774
400 H Shares plus 341 out of 774 applicants to receive an additional 100 H Shares
1.48%
40,000
594
500 H Shares plus 424 out of 594 applicants to receive an additional 100 H Shares
1.43%
50,000
560
600 H Shares plus 530 out of 560 applicants to receive an additional 100 H Shares
1.39%
60,000
388
800 H Shares plus 58 out of 388 applicants to receive an additional 100 H Shares
1.36%
70,000
727
900 H Shares plus 238 out of 727 applicants to receive an additional 100 H Shares
1.33%
Total
58,594
Total number of Pool A successful applicants: 14,411

<<<PAGE 16>>>
16
Pool B
Approximate
percentage
allotted of the
Number
Number
total number of
of H Shares
of valid
H Shares applied
applied for
applications
Basis of allocation/ballot
for
80,000
1,357
700 H Shares plus 272 out of 1,357 applicants to receive an additional 100 H Shares
0.90%
90,000
262
800 H Shares plus 13 out of 262 applicants to receive an additional 100 H Shares
0.89%
100,000
631
800 H Shares plus 505 out of 631 applicants to receive an additional 100 H Shares
0.88%
200,000
158
1,600 H Shares plus 127 out of 158 applicants to receive an additional 100 H Shares
0.84%
300,000
88
2,400 H Shares plus 27 out of 88 applicants to receive an additional 100 H Shares
0.81%
400,000
27
3,100 H Shares plus 17 out of 27 applicants to receive an additional 100 H Shares
0.79%
500,000
30
3,800 H Shares plus 24 out of 30 applicants to receive an additional 100 H Shares
0.78%
600,000
27
4,600 H Shares plus 6 out of 27 applicants to receive an additional 100 H Shares
0.77%
700,000
20
5,200 H Shares plus 17 out of 20 applicants to receive an additional 100 H Shares
0.76%
800,000
12
5,900 H Shares plus 9 out of 12 applicants to receive an additional 100 H Shares
0.75%
900,000
6
6,600 H Shares plus 4 out of 6 applicants to receive an additional 100 H Shares
0.74%
1,000,000
18
7,300 H Shares plus 6 out of 18 applicants to receive an additional 100 H Shares
0.73%
2,000,000
28
13,800 H Shares plus 9 out of 28 applicants to receive an additional 100 H Shares
0.69%
3,647,200
15
24,000 H Shares plus 12 out of 15 applicants to receive an additional 100 H Shares
0.66%
Total
2,679
Total number of Pool B successful applicants: 2,679
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.

<<<PAGE 17>>>
17
OTHERS/ADDITIONAL INFORMATION
Allocation of H shares to existing minority shareholders and their close associates
The Company has applied for, and the Stock Exchange has granted, a waiver from strict 
compliance with Rule 10.04 of, and a consent under paragraph 1C(2) of Appendix F1 to the 
Listing Rules to permit H Shares in the International Offering to be placed to certain existing 
minority Shareholders who (i) hold less than 5% of the voting rights in our Company prior to the 
completion of the Global Offering and (ii) are not and will not become (upon the completion of 
the Global Offering) core connected persons of our Company or the close associates of any such 
core connected person (together, the “Existing Minority Shareholder”), subject to the following 
conditions:
a) 
each Existing Minority Shareholder to whom our Company may allocate the H Shares under 
the International Offering holds less than 5% of the voting rights in our Company prior to the 
completion of the Global Offering;
b) 
each Existing Minority Shareholder is not, and will not be, a core connected person of our 
Company or any close associate of any such core connected person immediately prior to or 
following the Global Offering;
c) 
none of the Existing Minority Shareholders has the right to appoint a Director and/or have 
any other special rights in our Company;
d) 
allocation to the Existing Minority Shareholders or their close associates will not affect our 
Company’s ability to satisfy the public float requirement as prescribed under the requirements 
of Rule 8.08(1)(b) (as amended and replaced by Rule 19A.13A(2)) of the Listing Rules or 
otherwise by the Stock Exchange;
e) 
to the best knowledge and belief of our Company, and based on discussions between our 
Company and the Overall Coordinators and confirmations required to be submitted to the 
Stock Exchange by the Joint Sponsors, we will confirm to the Stock Exchange in writing 
that: a) in case of participation as cornerstone investors, no preferential treatment has been, 
nor will be, given to the Existing Minority Shareholders and/or their close associates by 
virtue of their relationship with our Company, other than the preferential treatment of assured 
entitlement under a cornerstone investment following the principles set out in Chapter 4.15 
of the Guide for New Listing Applicants, and the Existing Minority Shareholders’ or their 
close associates’ cornerstone investment agreements do not contain any material terms which 
are more favorable to the Existing Minority Shareholders or their close associates than 
those in other cornerstone investment agreements; or b) in case of participation as placees, 
no preferential treatment has been, nor will be given to the Existing Minority Shareholders 
and/or their close associates, nor is the Existing Minority Shareholder in a position to exert 
influence on our Company to obtain actual or perceived preferential treatment, by virtue of 
their relationship with our Company in any allocation in the placing tranche;

<<<PAGE 18>>>
18
f) 
in the case of participation as placees, the Overall Coordinators will confirm to the Stock 
Exchange that, to the best of their knowledge and belief, no preferential treatment has been, 
nor will be, given to any of the Existing Minority Shareholders or their close associates by 
virtue of their relationship with our Company in any allocation in the International Offering; 
and
g) 
the Joint Sponsors will confirm to the Stock Exchange in writing that based on (i) their 
discussions with our Company and the Overall Coordinators; and (ii) the confirmations 
provided to the Stock Exchange by our Company and the Overall Coordinators, and to the 
best of their knowledge and belief, they have no reason to believe that any of the Existing 
Minority Shareholders and/or their close associates received any preferential treatment, or 
is in a position to exert influence on our Company to obtain actual or perceived preferential 
treatment in the allocation process either as cornerstone investors or as placees by virtue 
of their relationship with our Company, other than the preferential treatment of assured 
entitlement under a cornerstone investment following the principles set out in Chapter 4.15 of 
the Guide for New Listing Applicants, and the details of allocation to the Existing Minority 
Shareholders and/or their close associates holding more than 1% of the issued share capital of 
our Company immediately prior to the completion of the Global Offering will be disclosed in 
the Prospectus and/or the allotment results announcement of our Company, as the case may 
be.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates, 
please refer to the section headed “Allotment Results Details – International Offer – Allottees with 
Waivers/Consents Obtained” in this announcement.
Allocations of Offer Shares to the existing Shareholders and/or their close associates and 
Cornerstone Investors with a consent under Chapter 4.15 of the Guide for New Listing 
Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 
of the Guide for New Listing Applicants to permit the Company to allocate further Offer Shares 
in the International Offering to certain Cornerstone Investors as placees, subject to the following 
conditions (“Allocation to Size-based Exemption Participants”):
a) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;
b) 
the Offer Shares allocated to all existing Shareholders and their close associates (whether as 
Cornerstone Investors and/or as placees) as permitted under the Size-based Exemption (as 
defined in the Guide for New Listing Applicants) do not exceed 30% of the total number of 
the H Shares offered under the Global Offering;

<<<PAGE 19>>>
19
c) 
the Allocation to Size-based Exemption Participants will not affect the Company’s ability to 
satisfy its public float requirement;
d) 
each Director, chief executive and Controlling Shareholder of the Company confirms that 
no securities have been allocated to them or their respective close associates under the 
Size-based Exemption; and
e) 
details of the allocation to existing Shareholders and/or their close associates and Cornerstone 
Investors under the Size-based Exemption will be disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates 
and Cornerstone Investors, please refer to the section headed “Allotment Results Details – 
International Offering – Allotees with Waivers/Consents Obtained” in this announcement.
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines as placees. Please refer to the section 
headed “Allotment Results Details – International Offering – Allottees with Waivers/Consents 
Obtained” in this announcement for details. The Company has applied to the Stock Exchange for, 
and the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing Guidelines 
to permit the Company to allocate such Offer Shares in the International Offering to the connected 
clients as placees. The allocation of Offer Shares to such connected clients is in compliance with 
all the conditions under the consent granted by the Stock Exchange. Details of the placement to 
connected clients as placees are set out below.

<<<PAGE 20>>>
20
No
Connected 
Distributor
Connected Client
Relationship with the Connected Distributor
Whether the 
Connected 
Client will hold 
the beneficial 
interests of the 
Offer Shares on a 
non-discretionary 
basis or 
discretionary 
basis for 
independent third 
parties
Whether the 
Connected Client 
is a collective 
investment 
scheme which is 
not authorised 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme
Maximum 
number of Offer 
Shares (rounded 
down to nearest 
whole board lot 
of 100 Shares) to 
be allocated to the 
Connected Client
Appropriate 
percentage of 
total number of 
Offer Shares
Approximate 
percentage of 
total Shares in 
issue immediately 
following the 
completion of 
Global Offering
1.
CLSA
CSI Note (1)
CSI is a member of the same group of companies as CLSA
Non-discretionary
N
347,700
0.48%
0.03%
2.
CITIC Asset 
Management Note (2)
CITIC Asset Management is a member of the same group of 
companies as CLSA
Discretionary
Y Note (2) 
11,200
0.02%
0.001%
3.
CITIC AM 
HK Note (3)
CITIC AM HK is a member of the same group of companies 
as CLSA
Discretionary
N
11,200
0.02%
0.001%
4.
GF Securities 
(Hong Kong) 
Brokerage
E Fund 
Management Note (4)
E Fund Management and GF Securities (Hong Kong) 
Brokerage are members of the same group of companies
Discretionary
N
333,300
0.46%
0.03%
5.
E Fund HK Note (5)
E Fund HK and GF Securities (Hong Kong) Brokerage are 
members of the same group of companies
Discretionary
Y Note (5)
171,700
0.24%
0.02%
6.
VPL Note (6)
VPL is a member of the same group of GF Securities (Hong 
Kong) Brokerage
Discretionary
N
63,100
0.09%
0.006%
VPHK Note (6)
VPHK is a member of the same group of GF Securities 
(Hong Kong) Brokerage
Discretionary
N
105,200
0.14%
0.01%
7.
GF Securities 
AM Note (7)
GF Securities AM is a member of the same group of 
companies as GF Securities (Hong Kong) Brokerage
Non-discretionary
N
381,400
0.52%
0.04%
8.
GF 
International Note (8)
GF International is a member of the same group of 
companies as GF Securities (Hong Kong) Brokerage
Discretionary
Y Note (8)
168,300
0.23%
0.02%
9.
CICCHKS
CICC acting as 
the asset manager 
for ICBC (ASIA) 
LTD Note (9)
CICC is a member of the same group of CICCHKS
Discretionary
Y Note (9)
33,700
0.05%
0.003%

<<<PAGE 21>>>
21
Notes:
(1) 
CSI
CSI will hold the Offer Shares as a placee under the International Offering on behalf of its ultimate clients 
(the “CSI Ultimate Clients”), on a non-discretionary basis, pursuant to which: (i) CSI will act as the single 
counterparty of the CSI Back-to-back TRS (the “CSI Back-to-back TRS”) to be entered into by it in connection 
with a total return swap order (the “CSI Client TRS”) placed and fully funded by the CSI Ultimate Clients, by 
which CSI will pass the full economic exposure of the Offer Shares placed to CSI to the CSI Ultimate Clients; 
(ii) as confirmed by CSI and CLSA, CSI will hold the legal title and beneficial interest in the Offer Shares, 
but will contractually agree to pass on the full economic exposure and return of the Offer Shares to the CSI 
Ultimate Clients, on a non-discretionary basis. The CSI Ultimate Clients may exercise their early termination 
rights to terminate the Client TRS at any time from the trade date of the Client TRS which should be on or after 
the date on which the Offer Shares are listed on the Stock Exchange; (iii) upon the final maturity or termination 
of the Client TRS by the CSI Ultimate Clients, CSI will dispose of the Offer Shares on the secondary market 
and the CSI Ultimate Clients will receive a final termination amount of the CSI Back-to-back TRS which will 
have taken into account all the economic returns or economic loss in relation to the Offer Shares and the fixed 
amount of transaction fees of the CSI Back-to-back TRS and the Client TRS. Due to its internal policy, CSI will 
not exercise the voting right of the Offer Shares during the terms of the CSI Back-to-back TRS; and (iv) CSI is 
not a collective investment scheme which is not authorized by the SFC, nor is expected to hold the Offer Shares 
on behalf of such scheme.
The details of the CSI Ultimate Clients are as follows:
Name of the CSI Ultimate Clients
Fund Manager
UBO(s) holding 
30% or more 
interest in Fund 
Manager (if 
applicable)
UBO(s) holding 
30% or more 
interest in the 
CSI Ultimate 
Clients (if 
applicable)
Beevest Investment Fund SPC – 
Global Multi Alpha Fund SP
Beevest Capital Management 
Limited
KANG Lan
NIE Fanqi
Sun Qianru
N/A
N/A
N/A
To the best of knowledge of CSI and having made all reasonable inquiries, each of the CSI Ultimate Clients and 
its UBOs is an independent third party of the Company, its subsidiaries, its substantial shareholders, CSI, CLSA 
and the companies which are members of the same group of companies as CLSA.
(2) 
CITIC Asset Management
CITIC Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager managing 
the funds on behalf of their investors (the “CITIC Asset Management Ultimate Clients”), each of which is, to 
the best knowledge of CITIC Asset Management, (i) an independent third party of the Company, its subsidiaries, 
its substantial shareholders, CITIC Asset Management, CLSA and the companies which are members of the 
same group of companies as CLSA; and (ii) a collective investment scheme which is not authorized by the SFC. 
No ultimate beneficial owner holds 30% or more interest in the funds.

<<<PAGE 22>>>
22
The details of the CITIC Asset Management Ultimate Clients are as follows:
Name of the CITIC Asset 
Management Ultimate Clients
Fund Manager
UBO of Fund 
Manager (if 
applicable)
UBO holding 30% 
or more interest 
in the CITIC 
Asset Management 
Ultimate Client (if 
applicable)
CITIC SECURITIES COMPANY
LIMITED XINHANG ZHIYUAN NO.1 (中信證券信航致遠 1 
號集合資產管理計劃)
CITIC Asset 
Management
CITIC Securities 
Company Limited
N/A
CITIC SECURITIES COMPANY
LIMITED XINHANG ZHIYUAN NO.3 (中信證券信航致遠 3 
號集合資產管理計劃)
CITIC Asset 
Management
CITIC Securities 
Company Limited
N/A
To the best of knowledge of CITIC Asset Management and after making all reasonable enquiries, (i) CITIC 
Asset Management Ultimate Clients, together with each of their ultimate beneficial owners, is an independent 
third party of the Company, its subsidiaries, its substantial shareholders, CITIC Asset Management, CLSA and 
the companies which are members of the same group of companies as CLSA, and (ii) none of CLSA and any 
companies which are members of the same group of companies as CLSA that hold any beneficial interest in any 
of CITIC Asset Management Ultimate Clients.
(3) 
CITIC AM HK
CITIC AM HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the fund 
on behalf of its underlying clients, namely (a) Meta Chance Limited, of which the ultimate beneficial owner 
holding 30% interest or more is natural person Song Ke (CHN Passport E57964565); and (b) BSCOMC Limited, 
of which the ultimate beneficial owners holding 30% or more interest therein is State-owned Assets Supervision 
and Administration Commission of People’s Government of Beijing Municipality, and of which are, to the 
best knowledge of CITIC AM HK, independent third parties of the Company, its subsidiaries, its substantial 
shareholders, CITIC AM HK, CLSA and the companies which are members of the same group companies as 
CLSA.
The ultimate beneficial owner of CITIC AM HK is CITIC Securities Company Limited (中信證券股份有限公
司, 6030.HK)
(4) 
E Fund Management
E Fund Management will hold the Offer Shares in its capacity as the discretionary fund manager managing the 
funds on behalf of its investors, each of which is, to the best knowledge of E Fund Management, an independent 
third party of E Fund Management, GF Securities (Hong Kong) Brokerage and the companies which are 
members of the same group of GF Securities (Hong Kong) Brokerage.
The shareholders of E Fund Management include (1) Guangdong Finance Trust Co., Ltd. (廣東粵財信託有限
公司), which is ultimately owned by The People’s Government of Guangdong Province (廣東省人民政府), (2) 
GF Securities Co., Ltd. (廣發証券股份有限公司), which is listed on the Stock Exchange (stock code: 1776) and 
the Shenzhen Stock Exchange (stock code: 000776), and (3) Infore Group Co., Ltd (盈峰集團有限公司), which 
is ultimately owned by He Jianfeng (何劍鋒), each holding 22.65% in E Fund Management and an Independent 
Third Party. None of the remaining shareholders of E Fund Management owns 30% or more equity interest 
therein.

<<<PAGE 23>>>
23
(5) 
E Fund HK
E Fund HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on 
behalf of its investors, each of which is, to the best knowledge of E Fund HK, an independent third party of E 
Fund HK, GF Securities (Hong Kong) Brokerage and the companies which are members of the same group of 
GF Securities (Hong Kong) Brokerage.
In addition, E Fund HK is expected to hold the Offer Shares on behalf of the following collective investment 
schemes which are not authorised by the SFC:
Name of the 
collective 
investment 
schemes
Types and 
values of 
assets under 
management 
(“AUM”)
Establishment 
date
Whether 
the scheme 
is publicly 
marketed
Identities of the 
general partners 
and the 20 
largest limited 
partners of the 
scheme where 
applicable
Identity of 
the Scheme 
Administrator
Whether any 
investor holds 
30% or more 
interests in the 
sub-fund (Y/N)
The relationships 
among the scheme, 
the ultimate 
beneficial owners of 
the limited partners, 
the controlling 
shareholders of the 
applicant, and the 
applicant
E Fund (HK) Neo 
Horizon Fund SP
AUM of 
approximately 
HKD100 million
August 2026
No
Not applicable 
as the scheme 
is not a limited 
partnership 
structure
E Fund HK
Save as Mr. 
YANG Runji 
(楊潤基), an 
Independent 
Third Party, no 
other investor 
holds 30% or 
more interest.
The scheme 
and ultimate 
beneficial owners 
are independent 
third parties of GF 
Securities (Hong 
Kong) Brokerage, 
the Company and 
the Controlling 
Shareholders of the 
Company.
E Fund (HK) Neo 
Opportunity SP II
AUM of 
approximately 
HKD500 million
June 2026
No
Not applicable 
as the scheme 
is not a limited 
partnership 
structure
E Fund HK
N
The scheme 
and ultimate 
beneficial owners 
are independent 
third parties of GF 
Securities (Hong 
Kong) Brokerage, 
the Company and 
the Controlling 
Shareholders of the 
Company.

<<<PAGE 24>>>
24
(6) 
Value Partners
Value Partners will hold the Offer Shares in its capacity as the discretionary fund manager managing assets on 
behalf of its underlying clients. Value Partners is a member of the same group of GF Securities (Hong Kong) 
Brokerage and therefore is a “connected client” of GF Securities (Hong Kong) Brokerage as defined under the 
Listing Rules.
Each of the underlying clients of Value Partners is an independent third party of Value Partners and GF 
Securities (Hong Kong) Brokerage and the companies which are members of the same group of companies as 
GF Securities (Hong Kong) Brokerage.
To the best knowledge, information and belief of Value Partners after due enquiry, the ultimate beneficial 
owners holding 30% or more interest of the ultimate clients of Value Partners are set out in the table below.
Value Partners has confirmed that, to the best of their knowledge, each of the ultimate client is an independent 
third party of Value Partners, GF Securities (Hong Kong) Brokerage and the companies which are members of 
the same group of companies as GF Securities (Hong Kong) Brokerage.
The details of the Value Partners Ultimate Clients are as follows:
Name of the funds to which the Offer  
Shares will be allocated
Fund Manager
Whether any 
investor holds 
30% or more 
interest in the 
fund
Ultimate 
Beneficial 
Owner with 
30% or more 
interests and 
Shareholding 
(%)
Value Partners Intelligent Funds – Chinese 
Mainland Focus Fund
Value Partners 
Limited
Yes
AIA 
International 
Limited
Value Partners Intelligent Funds – China 
Convergence Fund
Value Partners 
Limited
No
N/A
Value Partners High Dividend Stock Fund
Value Partners 
Hong Kong 
Limited
Yes
AIA 
International 
Limited

<<<PAGE 25>>>
25
(7) 
GF Securities AM
Each of the ultimate clients of GF Securities AM (the “GF Securities AM Ultimate Clients”) have engaged 
GF Securities AM, an asset manager that is qualified domestic institutional investor as approved by the relevant 
PRC authority to subscribe for and hold the Offer Shares as a placee under the International Offering on behalf 
of the GF Securities AM Ultimate Client on a non-discretionary basis.
Details of the GF Securities AM Ultimate Clients are set out as below:
Name of the funds to which 
the Offer Shares will be 
allocated
Fund Manager
Whether any 
investor holds 
30% or more 
interest in the 
fund
Ultimate Beneficial Owner 
with 30% or more interests 
and Shareholding (%)
GFAM ZYJXCL NO.1 
ASSET MANAGEMENT AC
GF Securities AM
Yes
Postal Savings Bank of China 
Co., Ltd. (stock code: 1658.
HK)
GFAM ZYJXCL NO.2 
ASSET MANAGEMENT AC
GF Securities AM
Yes
Postal Savings Bank of China 
Co., Ltd. (stock code: 1658.
HK)
GFAM ZHONGYOU NO.9 
ASSET MANAGEMENT 
ACCOUNT (QDII)
GF Securities AM
Yes
Postal Savings Bank of China 
Co., Ltd. (stock code: 1658.
HK)
ICBC(ASIA)LTD-ICBC LTD-
GFAM GYGGCL NO.2 AMA
GF Securities AM
Yes
Industrial and Commercial 
Bank of China Limited (stock 
code: 1398.HK, 601398.SH)
ICBC(ASIA)LTD-ICBC LTD-
GFAM GYGGCL NO.3 AMA
GF Securities AM
Yes
Industrial and Commercial 
Bank of China Limited (stock 
code: 1398.HK, 601398.SH)
As confirmed by GF Securities AM, (i) the Offer Shares to be placed to GF Securities AM are to be held on a 
non-discretionary basis on behalf of independent third parties; and (ii) each of the GF Securities AM Ultimate 
Clients and its ultimate beneficial owners (if applicable) is an independent third party of the Company, its 
subsidiaries, its Controlling Shareholders, its substantial shareholders, GF Securities AM, GF Securities (Hong 
Kong) Brokerage and the companies which are members of the same group of companies as GF Securities (Hong 
Kong) Brokerage.

<<<PAGE 26>>>
26
(8) 
GF International
GF International will hold the Offer Shares in its capacity as the discretionary fund manager managing the 
funds for and on behalf of its underlying clients, each of which is, to the best knowledge and belief and after 
due enquiry of GF International, an independent third party of the Company, its subsidiaries, its Controlling 
Shareholders, its substantial shareholders, GF International, GF Securities (Hong Kong) Brokerage and the 
companies which are members of the same group of GF Securities (Hong Kong) Brokerage. Save as disclosed 
below, no ultimate beneficial owner holds 30% or more interest in the funds.
GF International is investing on behalf of certain collective investment schemes which are not authorized by the 
SFC, details of which are as follow:
Name
Types and values 
of assets under 
management
Whether
the
scheme is
publicly
marketed
Scheme
establishment
date
Identity of 
the scheme 
administrator
Whether
any
investor
holds
30%
or more
interest
in
the fund
The relationships 
among the 
scheme, the 
ultimate 
beneficial owners, 
the controlling 
shareholders of 
the applicant, and 
the applicant
Golden Fortune 
Opportunity Fund
Private Fund, AUM 
approximately 
HK$190 million as 
of Aug 2026
No
19/11/2013
GF International
Yes, 
ZHUCHENG 
GARMENT 
& KNITTING 
IMP.EXP.CO., 
LIMITED, 
of which the 
UBO is ZHAO 
HAIYUE
The scheme 
and ultimate 
beneficial owners 
are independent 
third parties of GF 
Securities (Hong 
Kong) Brokerage, 
the Company and 
the Controlling 
Shareholders of the 
Company.
FrontLine 
Investment 
Master SPC-GF 
Luminous Fund 
SP
Private Fund, AUM 
approximately 
HK$500 million as 
of Aug 2026
No
7/11/2025
GF International
No
FrontLine 
Investment Master 
SPC-GF Vision 
Fund SP
Private Fund, AUM 
approximately 
HK$150 million as 
of Aug 2026
No
10/3/2026
GF International
No
FrontLine 
Investment Master 
SPC-GF Bonanza 
Fund SP
Private Fund, AUM 
approximately 
HK$180 million as 
of Aug 2026
No
8/4/2026
GF International
No
FrontLine 
Investment Master 
SPC-GF Curation 
Equity Fund SP
Private Fund, AUM 
approximately 
HK$75 million as of 
Aug 2026
No
4/5/2026
GF International
No
FrontLine 
Investment Master 
SPC – Golden 
Stone Fund SP
Private Fund, AUM 
approximately 
HK$50 million as of 
Aug 2026
No
3/11/2025
GF International
No
In addition to the funds disclosed above, GF International is also expected to hold the Offer Shares on behalf of 
one SFC authorized fund, namely GFI Global Select Equity Fund.

<<<PAGE 27>>>
27
(9) 
CICC
CICCHKS is a wholly owned subsidiary of CICC, and therefore a member of the same group of companies as 
CICC. Accordingly, CICC is a connected client of CICCHKS.
As confirmed by CICC, (i) ICBC Wealth Wisdom Joy Minimum Holding Period 180 Days Fixed Income Open 
End Net Value Wealth Management Product (工銀理財智悅最短持有 180 天固定收益類開放式淨值型理財
產品) (“ICBC Wealth Wisdom Joy”) owns 30% or more interest in CICC Gong Yin as an investor and there 
are no ultimate beneficial owners who hold 30% or more interest in ICBC Wealth Wisdom Joy; (ii) there are 
no ultimate beneficial owners who hold 30% or more interest in CICC Gong Yin; and (iii) each of the ultimate 
beneficial owners is an independent third party of the Company, its subsidiaries, CICC, CICCHKS and the 
companies which are members of the same group of companies as CICCHKS.
CICC is investing on behalf of a collective investment scheme which is not authorized by the SFC, the details 
of which are as follows:
Name
Types and values 
of assets under 
management
Whether 
the 
scheme is 
publicly 
marketed
Scheme 
establishment 
date
Identity of 
the scheme 
administrator
Whether 
any 
investor 
holds 30% 
or more 
interest in 
the fund
The relationships among 
the scheme, the ultimate 
beneficial owners, the 
controlling shareholders 
of the applicant, and the 
applicant
ICBC (ASIA) LTD-ICBC LTD-CICC Gong Yin 
JXCL NO.1 CIS (“CICC Gong Yin”)
Collective Asset 
Management Plan
Value: RMB93,000,000
No
26/6/2026
CICC
No
The scheme and ultimate 
beneficial owners are 
independent third parties of 
CICCHKS, the Company and 
the Controlling Shareholders 
of the Company.

<<<PAGE 28>>>
28
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or 
any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer or 
solicitation to purchase or subscribe for securities in the United States. The securities mentioned 
herein have not been, and will not be, registered under the United States Securities Act of 1933, 
as amended (the “U.S. Securities Act”). The securities may not be offered or sold in the United 
States except pursuant to an exemption from the registration requirements of the U.S. Securities 
Act and in compliance with any applicable state securities laws, or outside the United States 
unless in compliance with Regulation S under the U.S. Securities Act. There will be no public 
offer of securities in the United States.
The Offer Shares are being offered and sold (1) solely to qualified institutional buyers as defined 
in Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under 
the U.S. Securities Act and (2) outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated September 21, 2026 issued by Shenzhen Kinwong 
Electronic Co., Ltd. for detailed information about the Global Offering described below before 
deciding whether or not to invest in the H Shares thereby being offered.
* 
Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations 
under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the 
events set out in the section headed “Underwriting — Underwriting Agreements — Hong Kong Underwriting 
Agreement — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) 
on the Listing Date (which is currently expected to be on September 29, 2026).

<<<PAGE 29>>>
29
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, the total market value of the 
H Shares expected to be held by the public is expected to be approximately HK$5.10 billion, 
calculated based on the final Offer Price of HK$69.88 per H Share, which is higher than the 
prescribed expected market value of H Shares required to be held in public hands of not less 
than HK$3,000,000,000 under Rule 19A.13A(2)(b) of the Listing Rules, thereby satisfying Rule 
19A.13A(2) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the H Shares of the Company at the time of Listing. Based on 
the final Offer Price of HK$69.88 per H Share, the free float of the Company has a market value 
at the time of Listing of approximately HK$2,666.33 million. The Company satisfies the free float 
requirement under Rule 19A.13C(2)(b) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering: (i) no placee 
will, individually, be placed more than 10% of the enlarged issued share capital of the Company 
immediately after the Global Offering; (ii) there will not be any new substantial Shareholder under 
the Listing Rules immediately after the Global Offering; (iii) the three largest public shareholders 
of the Company do not hold more than 50% of the H shares in public hands at the time of the 
Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at 
least 300 Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing 
Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, 
September 29, 2026 (Hong Kong time), provided that the Global Offering has become 
unconditional and the right of termination described in the section headed “Underwriting – 
Underwriting Agreements – Hong Kong Underwriting Agreement – Grounds for Termination” in 
the Prospectus has not been exercised. Investors who trade the H Shares on the basis of publicly 
available allocation details prior to the receipt of H Share certificates or prior to the H Share 
certificates becoming valid evidence of title do so entirely at their own risk.

<<<PAGE 30>>>
30
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Tuesday, 
September 29, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Tuesday, September 29, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 100 H Shares each, and the stock code of the H Shares will 
be 3228.
By order of the Board
Shenzhen Kinwong Electronic Co., Ltd.
Mr. Liu Shaobai
Chairman of the Board
Hong Kong, September 28, 2026
As at the date of this announcement, the Board comprises: (i) Mr. Liu Yu, Mr. Deng Li, as 
Executive Directors; (ii) Mr. Liu Shaobai (Chairman of the Board), Mr. Cheuk Yung, Ms. Huang 
Xiaofen, Ms. Cheuk Kwan as Non-executive Directors; and (iii) Dr. Zhou Guoyun, Dr. Xin 
Guosheng, Dr. Cao Chunfang as Independent non-executive Directors.
