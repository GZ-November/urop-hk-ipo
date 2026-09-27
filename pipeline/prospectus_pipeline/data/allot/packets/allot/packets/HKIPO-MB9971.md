# 配发结果公告抽取任务：9971.HK BASiC Semiconductor Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**07/07/2026 21:55**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0707/2026070701913.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"9971.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
defined in the prospectus dated June 29, 2026 (the “Prospectus”) issued by BASiC Semiconductor Co., Ltd. (深圳基
本半導體股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. Potential investors should read the Prospectus for detailed information about the Company 
and the Global Offering described below before deciding whether or not to invest in the Offer Shares.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia) or to any person 
(as defined in Regulation S under the U.S. Securities Act of 1933, as amended from time to time, (the “U.S. Securities 
Act”)) or any other jurisdiction where such distribution is prohibited by law. This announcement does not constitute 
or form a part of any offer to sell or solicitation to purchase or subscribe for securities in the United States or in any 
other jurisdictions.
The Offer Shares have not been and will not be registered under the U.S. Securities Act or any state securities laws in 
the United States and may not be offered, sold, pledged or transferred within the United States or to, or for the account 
or benefit of U.S. persons (as defined in Regulation S under the U.S. Securities Act), except in transactions exempt 
from, or not subject to, the registration requirements of the U.S. Securities Act. The Offer Shares are being offered and 
sold outside the United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, it is anticipated that no stabilization activities will be carried out in relation to 
the Global Offering.
The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not resident in Hong 
Kong. Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the 
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the 
section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds 
for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date.

<<<PAGE 2>>>
2
BASiC Semiconductor Co., Ltd.
深圳基本半導體股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under
the Global Offering
:
27,386,200 H Shares
Number of Hong Kong Offer Shares
:
5,477,400 H Shares (taking into account 
 reallocation)
Number of International Offer Shares
:
21,908,800 H Shares (taking into account 
 reallocation)
Final Offer Price
:
HK$31.62 per H Share, plus brokerage of 
 1.0%, SFC transaction levy of 0.0027%, 
 AFRC transaction levy of 0.00015% and 
 Stock Exchange trading fee of 0.00565%
Nominal Value
:
RMB0.20 per H Share
Stock code
:
9971
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers
(in no particular order)
Joint Bookrunners and Joint Lead Managers
(in alphabetical order)

<<<PAGE 3>>>
3
BASiC Semiconductor Co., Ltd.
深圳基本半導體股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated June 29, 2026 (the “Prospectus”) issued by 
BASiC Semiconductor Co., Ltd. (深圳基本半導體股份有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
9971
Stock short name
BASICSEMI
Dealings commencement date
July 8, 2026*
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$31.62
Offer Price Range
HK$27.49 – HK$31.62
Offer Price Adjustment exercised
N/A
Offer Shares and Share Capital
Number of Offer Shares
27,386,200
Number of Offer Shares in Hong Kong Public Offering (as 
adjusted after reallocation)
5,477,400
Number of offer shares in International Offering (as adjusted 
after reallocation)
21,908,800
Number of issued shares upon Listing
304,289,725

<<<PAGE 4>>>
4
Over-allocation
No. of Offer Shares over-allocated
–
There has been no over-allocation of Offer Shares in the Placing. Therefore, the Over-allotment 
Option will not be exercised and will lapse upon Listing.
Proceeds to the Company
Gross proceeds to the Company (Note 1)
HK$865.95 million
Less: Estimated listing expenses payable based on the Offer 
Price
HK$(99.82) million
Net proceeds to the Company
HK$766.13 million
Note: Gross proceeds to the Company refer to the amount to which the issuer is entitled to receive. Net proceeds 
represent the estimated net proceeds calculated by the gross proceeds deducted by the estimated listing 
expenses payable based on Final Offer Price. For details of the use of proceeds, please refer to the section 
headed “Future Plans and Use of Proceeds” of the Prospectus.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
207,706
No. of successful applications
24,010
Subscription level
4,812.72 times
Claw-back triggered
Yes
No. of Offer Shares initially available under the Hong Kong 
Public Offering
1,369,400
No. of Offer Shares reallocated from the International Offering 
(claw-back)
4,108,000
Final no. of Offer Shares under the Hong Kong Public Offering 
(after reallocation)
5,477,400
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering
20.00%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can refer to www.eipo.
com.hk/eIPOAllotment to perform a search by identification number or www.eipo.com.hk/eIPOAllotment for 
the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
96
Subscription Level
2.98 times
No. of Offer Shares initially available under the International 
Offer
26,016,800
No. of Offer Shares reallocated to the Public Offer (claw-back)
4,108,000
Final no. of Offer Shares under the International Offer (as 
adjusted after reallocation)
21,908,800
% of Offer Shares under the International Offer to the Global 
Offering
80.00%
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, controlling shareholders, 
substantial shareholders, existing shareholders of the Company or any of its subsidiaries or their 
respective close associates; and (ii) none of the placees and the public who have purchased the 
Offer Shares are accustomed to taking instructions from the Company, any of the Directors, chief 
executive of the Company, controlling shareholders, substantial shareholders, existing shareholders 
of the Company or any of its subsidiaries or their respective close associates in relation to the 
acquisition, disposal, voting or other disposition of Shares registered in his/her/its name or 
otherwise held by him/her/it.

<<<PAGE 6>>>
6
Allottees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares 
allocated
% of total 
number of 
Offer Shares
% of total 
issued H 
Shares after 
the Global 
Offering
% of total 
issued share 
capital after 
the Global 
Offering
Relationship
Allotees with consent under paragraph 1C(1) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) and 
Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations to connected clients Note 1
CITIC Securities Asset 
Management Company 
Ltd (“CITIC Asset 
Management”)
1,400
0.0051%
0.00049%
0.00046%
Connected 
client
Note:
1. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in 
relation to allocations to connected clients, please refer to the section headed “Others/Additional Information” in this announcement.
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
Number of H 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
% of total 
issued 
shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
Last day 
subject to 
the lock-up 
undertakings
Bronze Group
54,154,890
54,154,890
18.83%
17.80%
July 7, 2027
BASiC Principle LP
18,404,300
18,404,300
6.40%
6.05%
July 7, 2027
BASiC Createnjoy LP
17,673,665
17,372,476
6.04%
5.81%
July 7, 2027
BASiC Innotech LP
12,000,000
12,000,000
4.17%
3.94%
July 7, 2027
BASiC Creation LP
11,491,475
11,352,989
3.95%
3.78%
July 7, 2027
BASiC Entrepreneur LP
9,750,000
9,750,000
3.39%
3.20%
July 7, 2027
BASiC Original LP
3,846,586
–
–
1.26%
July 7, 2027
Subtotal
127,320,916
123,034,655
42.79%
41.84%
Note:
The lock-up period shown in the table above is the requirement under the PRC Company Law. The lock-up requirement under the PRC Company 
Law is longer than the lock-up period required of controlling shareholders under Rule 10.07 of the Listing Rules.

<<<PAGE 7>>>
7
Key Persons (as defined under Rule 18C.14 of the Listing Rules)
Name
Number of 
shares held in 
the Company 
subject to lock-
up undertakings 
upon
listing
Number of H 
shares held in 
the Company 
subject to lock-
up undertakings 
upon
listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon listing
% of total issued 
shares after the 
Global Offering 
subject to lock-
up undertakings 
upon listing
Last day subject 
to the lock-up 
undertakings
Dr. Wang Zhihan  
(汪之涵) Note 1
N/A Note 1
N/A Note 1
N/A Note 1
N/A Note 1
July 7, 2027
Bronze Group Notes 2 and 8
54,154,890
54,154,890
18.83%
17.80%
July 7, 2027
BASiC Principle LP Notes 3 and 8
18,404,300
18,404,300
6.40%
6.05%
July 7, 2027
BASiC Original LP Note 1
3,846,586
–
–
1.26%
July 7, 2027
Dr. He Weiwei  
(和巍巍) Notes 2 and 8
N/A Note 9
N/A Note 9
N/A Note 9
N/A Note 9
July 7, 2027
Mr. Fu Junyin  
(傅俊寅) Notes 2 and 8
N/A Note 9
N/A Note 9
N/A Note 9
N/A Note 9
July 7, 2027
Ms. Yan Rui  
(閆瑞) Notes 2 and 8
N/A Note 9
N/A Note 9
N/A Note 9
N/A Note 9
July 7, 2027
Mr. Zhang Yu (張煜) Note 8
N/A Note 9
N/A Note 9
N/A Note 9
N/A Note 9
July 7, 2027
Mr. Zhang Yongkun  
(張永坤) Note 8
N/A Note 9
N/A Note 9
N/A Note 9
N/A Note 9
July 7, 2027
BASiC Createnjoy LP Notes 4 and 8
17,673,665
17,372,476
6.04%
5.81%
July 7, 2027
BASiC Innotech LP Notes 5 and 8
12,000,000
12,000,000
4.17%
3.94%
July 7, 2027
BASiC Creation LP Notes 6 and 8
11,491,475
11,352,989
3.95%
3.78%
July 7, 2027
BASiC Entrepreneur  
LP Notes 7 and 8
9,750,000
9,750,000
3.39%
3.20%
July 7, 2027
Subtotal
127,320,916
123,034,655
42.79%
41.84%
Notes:
1. 
Dr. Wang does not directly hold the Shares of the Company but he is deemed to be interested in all the interests of Bronze Group, taking into account his 
direct interests, the interests held by Bronze Holding LP (in which he serves as the general manager), his concert party arrangement with InteBridge Tech, 
and the interests of his mother, Ms. Wang Yongmiao (王永苗). See note 2 below for details. Moreover, Dr. Wang is the general partner of BASiC Principle 
LP, BASiC Createnjoy LP, BASiC Innotech LP, BASiC Creation LP, BASiC Entrepreneur LP and BASiC Original LP. Accordingly, under the SFO, Dr. 
Wang is deemed to be interested in the entire Shares held by Bronze Group, BASiC Principle LP, BASiC Createnjoy LP, BASiC Innotech LP, BASiC 
Creation LP, BASiC Entrepreneur LP and BASiC Original LP.

<<<PAGE 8>>>
8
2. 
Bronze Group is owned as to (a) 40.85% by Dr. Wang directly, (b) 27.35% by Bronze Holding LP, (c) 
19.57% by InteBridge Tech, and (d) 12.23% by Ms. Wang Yongmiao (王永苗) (“Ms. Wang”), Dr. Wang’s 
mother. In December 2021, Dr. Wang and InteBridge Tech entered into a concert party agreement pursuant to 
which they agreed to act in concert with respect to their shareholder rights in Bronze Group, including voting 
and proposing resolutions, with Dr. Wang’s decision prevailing in case of disagreement. InteBridge Tech 
was established as an investment platform for Bronze Group’s employees and has at all times been under 
the control and management of Dr. Wang as its sole director. The agreement was entered into to strengthen 
governance and provide clarity, simply reflecting and confirming the existing control arrangement on Bronze 
Group. Bronze Holding LP is controlled by Dr. Wang as its general partner holding a 90% interest, with Mr. 
Fu Junyin holding the remaining 10%. InteBridge Tech is owned as to 13%, 25%, 15%, 25%, 3% and 19% 
by Dr. Wang, Ms. Wang, Dr. He Weiwei, Mr. Fu Junyin, Ms. Yan Rui, and five employees of the Company 
or Bronze Group, respectively, and none of such employees holds more than 5% of the equity interest in 
InteBridge Tech.
3. 
BASiC Principle LP is controlled by Dr. Wang as its general partner with 1.87% partnership interests. BASiC 
Original LP is controlled by Dr. Wang as its general partner with 2.18% direct partnership interests and 
17.59% controlled through Bronze Group.
4. 
BASiC Createnjoy LP is an employee share incentive platform controlled by Dr. Wang as its general partner.
5. 
BASiC Innotech LP is an employee share platform controlled by Dr. Wang as its general partner.
6. 
BASiC Creation LP is an employee share incentive platform controlled by Dr. Wang as its general partner.
7. 
BASiC Entrepreneur LP is an employee share platform controlled by Dr. Wang as its general partner.
8. 
Apart from Dr. Wang, the executive Directors, senior management members and core R&D members who 
are subject to lock-up requirements pursuant to Rule 18C.14 of the Listing Rules and who indirectly hold 
Shares through (a) Bronze Group or (b) the employee shareholding platforms, namely BASiC Createnjoy LP, 
BASiC Innotech LP, BASiC Creation LP and BASiC Entrepreneur LP, include (i) Dr. He Weiwei, who is our 
executive Director, chief executive officer and a core R&D member; (ii) Mr. Fu Junyin, who is our executive 
Director and a core R&D member; (iii) Ms. Yan Rui, who is our executive Director; (iv) Mr. Zhang Yu, who 
is our Secretary of the Board and joint company secretary; and (v) Mr. Zhang Yongkun, who is our director 
of finance. See “Appendix V — Statutory and General Information — D. Employee Shareholding Platforms” 
of the Prospectus.
9. 
None of these individuals directly hold any Shares. See notes 2 and 8, as applicable.

<<<PAGE 9>>>
9
Pathfinder SIIs
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
Number of H 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
% of total 
issued 
shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
Last day 
subject to 
the lock-up 
undertakings
Leaguer SIIs
Shenzhen Leaguer Venture 
Capital Co., Ltd. (深圳市力
合創業投資有限公司)
11,001,225
11,001,225
3.83%
3.62%
July 7, 2027
Shenzhen Leaguer Yongjin 
Venture Capital Enterprise 
(Limited Partnership) (深圳
力合永金創業投資企業(有
限合夥))
5,021,125
5,021,125
1.75%
1.65%
July 7, 2027
Subtotal
16,022,350
16,022,350
5.57%
5.27%
Wingtech Technology Co., 
Ltd. (聞泰科技股份有限公
司)
10,162,360
10,162,360
3.53%
3.34%
July 7, 2027
Shenzhen InteBridge 
Technology Equity 
Investment Fund 
Partnership (Limited 
Partnership) (深圳英智科技
股權投資基金合夥企業(有
限合夥))
8,622,770
8,622,770
3.00%
2.83%
July 7, 2027
Subtotal
34,807,480
34,807,480
12.11%
11.44%
Notes:
1. 
Each of the Shareholders listed in the above table is a pathfinder SII of the Company as defined under Chapter 2.5 of the Guide for 
New Listing Applicants. Please refer to the section headed “History, Development and Corporate Structure – Lock-up Period” in the 
Prospectus for further details.
2. 
All Pathfinder SIIs shall not dispose of any of the Shares held by them within the 12 months following the Listing Date as required 
under the applicable PRC laws and relevant lock-up undertakings as disclosed in the Prospectus. In accordance with Rule 18C.14(2) of 
the Listing Rules, the required lock-up period commences on the date by reference to which disclosure of its shareholding is made in the 
Prospectus and ends on the date which is six months from the Listing Date.

<<<PAGE 10>>>
10
Pre-IPO Investors
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
Number of H 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
% of total 
issued 
shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
Last day 
subject to 
the lock-up 
undertakings
Shenzhen Lihe Hongxin 
Venture Capital Partnership 
(Limited Partnership) (深圳
力合泓鑫創業投資合夥企
業(有限合夥))
4,065,055
4,065,055
1.41%
1.34%
July 7, 2027
Guangdong Leaguer 
Kaiwu Venture Capital 
Fund Partnership (Limited 
Partnership) (廣東力合開物
創業投資基金合夥企業(有
限合夥))
3,963,895
3,963,895
1.38%
1.30%
July 7, 2027
Shenzhen Leaguer New 
Generation Information 
Technology Venture Capital 
Partnership (Limited 
Partnership) (深圳市力合新
一代信息技術創業投資合
夥企業(有限合夥))
3,726,745
3,726,745
1.30%
1.22%
July 7, 2027
Shenzhen Leaguer 
Rongtong Venture Capital 
Co., Ltd. (深圳力合融通創
業投資有限公司)
1,481,972
1,481,972
0.52%
0.49%
July 7, 2027
Zhangjiagang Leaguer 
Preferred Equity Investment 
Partnership (Limited 
Partnership) (張家港力合優
選股權投資合夥企業(有限
合夥))
883,685
883,685
0.31%
0.29%
July 7, 2027

<<<PAGE 11>>>
11
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
Number of H 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
% of total 
issued 
shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
Last day 
subject to 
the lock-up 
undertakings
Shenzhen Investment 
Control Chuangzhi 
Technology Private Venture 
Capital Fund Partnership 
(Limited Partnership) (深
圳投控創智科技私募創業
投資基金合夥企業(有限合
夥))
4,253,910
4,253,910
1.48%
1.40%
July 7, 2027
Guangdong Guangqi 
Zhixing Lu Equity 
Investment Partnership 
(Limited Partnership) (廣東
廣祺智行陸號股權投資合
夥企業(有限合夥))
4,165,935
4,165,935
1.45%
1.37%
July 7, 2027
Zhongshan Entrepreneur 
Development Fund of Funds 
(Limited Partnership) (中山
市創業發展母基金合夥企
業(有限合夥))
4,024,760
4,024,760
1.40%
1.32%
July 7, 2027
Shenzhen Songhe 
Chuangzhi Venture Capital 
Investment Enterprise 
(Limited Partnership) (深圳
松禾創智創業投資合夥企
業(有限合夥))
2,209,210
2,209,210
0.77%
0.73%
July 7, 2027
Zhuhai Cultural Industry 
Investment Fund (Limited 
Partnership) (珠海文化產業
投資基金(有限合夥))
2,082,965
2,082,965
0.72%
0.68%
July 7, 2027

<<<PAGE 12>>>
12
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
Number of H 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
% of total 
issued 
shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
Last day 
subject to 
the lock-up 
undertakings
Guangdong Yueke 
Jiangmen Innovation and 
Venture Capital Master 
Fund Co., Ltd. (廣東省粵科
江門創新創業投資母基金
有限公司)
1,999,650
1,999,650
0.70%
0.66%
July 7, 2027
Guangdong Kerui 
Investment Management 
Co., Ltd. (廣東科瑞投資管
理有限公司)
83,320
83,320
0.03%
0.03%
July 7, 2027
Zhongshan Torch High-
Tech Equity Investment 
Partnership (Limited 
Partnership) (中山火炬高新
股權投資合夥企業(有限合
夥))
2,951,490
2,951,490
1.03%
0.97%
July 7, 2027
Zhongshan Torch Huaying 
High-Tech Venture 
Investment Partnership 
(Limited Partnership) (中山
火炬華盈高新創業投資合
夥企業(有限合夥))
1,073,270
1,073,270
0.37%
0.35%
July 7, 2027
Qingdao Minxin Qiyuan 
Investment Center (Limited 
Partnership) (青島民芯啟元
投資中心(有限合夥))
3,387,455
3,387,455
1.18%
1.11%
July 7, 2027
Qingdao Truesino Haiping 
Equity Investment Fund 
Partnership (L.P.) (青島初
芯海屏股權投資基金合夥
企業(有限合夥))
1,666,375
1,666,375
0.58%
0.55%
July 7, 2027
Jinan Gaoxin Kexi Co-
Win One Venture Capital 
Partnership (Limited 
Partnership) (濟南高新珂璽
共贏壹號創業投資合夥企
業(有限合夥))
1,291,275
1,291,275
0.45%
0.42%
July 7, 2027

<<<PAGE 13>>>
13
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
Number of H 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
% of total 
issued 
shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
Last day 
subject to 
the lock-up 
undertakings
Bosch (Shanghai) Venture 
Capital Co., Ltd. (博世(上
海)創業投資有限公司)
6,038,505
6,038,505
2.10%
1.98%
July 7, 2027
Shenzhen BASIC Primary 
Colors Holding Partnership 
(Limited Partnership) (深圳
基本原色控股合夥企業(有
限合夥))
8,544,515
8,544,515
2.97%
2.81%
July 7, 2027
Shenzhen InteBridge 
Innovation Partnership 
(Limited Partnership) (深圳
英智創新合夥企業(有限合
夥))
6,899,410
4,199,410
1.46%
2.27%
July 7, 2027
Beijing E-town Changhou 
Display Chip Venture 
Capital Center (Limited 
Partnership) (北京屹唐長厚
顯示芯片創業投資中心(有
限合夥))
4,792,045
4,792,045
1.67%
1.57%
July 7, 2027
Guangdong Dezaihou 
Jiahang Equity Investment 
Partnership (Limited 
Partnership) (廣東德載厚嘉
航股權投資合夥企業(有限
合夥))
4,615,485
3,923,160
1.36%
1.52%
July 7, 2027
Wuxi New Peak Advanced 
Technology Investment 
Fund L.L.P. (無錫新高地高
精尖產業投資基金合夥企
業(有限合夥))
3,433,280
3,433,280
1.19%
1.13%
July 7, 2027
Jinpu Venture Capital 
Investment Co., Ltd. (津蒲
創業投資有限公司)
2,979,867
–
–
0.98%
July 7, 2027
Suzhou Tengxin Venture 
Capital Partnership (Limited 
Partnership) (蘇州藤信創業
投資合夥企業(有限合夥))
2,576,520
2,576,520
0.90%
0.85%
July 7, 2027

<<<PAGE 14>>>
14
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
Number of H 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
% of total 
issued 
shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
Last day 
subject to 
the lock-up 
undertakings
Shanghai Xiche Investment 
Management Center 
(Limited Partnership) (上海
喜車投資管理中心(有限合
夥))
2,540,590
2,540,590
0.88%
0.83%
July 7, 2027
Qianhai Renzhi 
Interconnection (Shenzhen) 
Equity Investment 
Enterprise (Limited 
Partnership) (前海仁智互聯
(深圳)股權投資企業(有限
合夥))
2,484,495
2,484,495
0.86%
0.82%
July 7, 2027
Zhuhai Changhou Zhiyuan 
Technology Management 
Center (Limited 
Partnership) (珠海長厚致遠
科技管理中心(有限合夥))
1,888,165
1,888,165
0.66%
0.62%
July 7, 2027
Gongqingcheng Jiayin 
Xiangfu No. 1 Equity 
Investment Partnership 
Enterprise (Limited 
Partnership) (共青城佳銀享
富壹號股權投資合夥企業
(有限合夥))
1,767,365
1,767,365
0.61%
0.58%
July 7, 2027
Ganzhou Sanxin Tengyi 
Equity Investment Center 
(Limited Partnership) (贛州
三新騰奕股權投資中心(有
限合夥))
1,688,595
1,688,595
0.59%
0.55%
July 7, 2027
Gongqingcheng Richland 
Semiconductor Industry 
Investment Management 
Partnership Enterprise 
(Limited Partnership) (共青
城厚土半導產業投資管理
合夥企業(有限合夥))
1,325,525
1,325,525
0.46%
0.44%
July 7, 2027

<<<PAGE 15>>>
15
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
Number of H 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
% of total 
issued 
shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
Last day 
subject to 
the lock-up 
undertakings
Gongqingcheng Helide 
Investment Partnership 
(Limited Partnership) (共青
城合利德投資合夥企業(有
限合夥))
1,325,525
1,325,525
0.46%
0.44%
July 7, 2027
Shenzhen BASIC Atom 
Management Partnership 
(Limited Partnership) (深圳
基本原子管理合夥企業(有
限合夥))
1,016,240
1,016,240
0.35%
0.33%
July 7, 2027
Shenzhen V&T 
Technologies Co., Ltd. (深
圳市藍海華騰技術股份有
限公司)
999,825
999,825
0.35%
0.33%
July 7, 2027
Shenzhen Kexi Basic 
Synergy Investment 
Partnership (Limited 
Partnership) (深圳珂璽基本
協同投資合夥企業(有限合
夥))
892,857
–
–
0.29%
July 7, 2027
Shenzhen Think Investment 
Management Co., Ltd. (深
圳市暢想投資管理有限公
司)
833,185
833,185
0.29%
0.27%
July 7, 2027
Guoxin Tiefa Venture 
Capital (Beijing) Co., Ltd. 
(國信鐵發創業投資(北京)
有限公司)
714,285
–
–
0.23%
July 7, 2027
Shenzhen Gongda Wujiang 
Investment Partnership 
(Limited Partnership) (深圳
市工大無疆投資合夥企業
(有限合夥))
267,858
–
–
0.09%
July 7, 2027

<<<PAGE 16>>>
16
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
Number of H 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
% of total 
issued 
shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
Last day 
subject to 
the lock-up 
undertakings
Shenzhen Kexi Gongying 
Industrial Investment 
Partnership (Limited 
Partnership) (深圳珂璽共贏
產業投資合夥企業(有限合
夥))
267,857
–
–
0.09%
July 7, 2027
Shenzhen Yiqi Investment 
Consulting Service 
Enterprise (Limited 
Partnership) (深圳市邑啟
投資諮詢服務企業(有限合
夥))
223,214
–
–
0.07%
July 7, 2027
Gongqingcheng Leaguer 
Huiying Venture Investment 
Management Partnership 
(Limited Partnership) (共青
城力合匯盈創業投資管理
合夥企業(有限合夥))
202,118
–
–
0.07%
July 7, 2027
China US Green Shenggu 
(Tianjin) Venture Capital 
Fund Partnership (Limited 
Partnership) (中美綠色盛谷
(天津)創業投資基金合夥企
業(有限合夥))
1,325,525
–
–
0.44%
July 7, 2027
Suzhou Longying No. 5 
Green Venture Capital 
Partnership (Limited 
Partnership) (蘇州龍鷹伍號
綠色創業投資合夥企業(有
限合夥))
595,973
–
–
0.20%
July 7, 2027
Runxia Zhaoying 
(Hubei) New Energy 
Industry Investment Fund 
Partnership (L.P.) (潤峽招
贏(湖北)新能源產業投資基
金合夥企業(有限合夥))
4,036,790
4,036,790
1.40%
1.33%
July 7, 2027

<<<PAGE 17>>>
17
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
Number of H 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon
listing
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
% of total 
issued 
shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing
Last day 
subject to 
the lock-up 
undertakings
Nanjing Zhaoyin Gongying 
Equity Investment 
Partnership (Limited 
Partnership) (南京市招銀共
贏股權投資合夥企業(有限
合夥))
129,145
129,145
0.04%
0.04%
July 7, 2027
Huayu (Qingdao) 
Manufacturing 
Transformation and 
Upgrade Private Equity 
Investment Fund 
Partnership (Limited 
Partnership) (華輿(青島)
製造業轉型升級私募股權
投資基金合夥企業(有限合
夥))
3,839,000
3,839,000
1.34%
1.26%
July 7, 2027
Hangzhou Times Dingfeng 
Venture Capital Partnership 
(Limited Partnership) (杭州
時代鼎豐創業投資合夥企
業(有限合夥))
1,162,970
1,162,970
0.40%
0.38%
July 7, 2027
Qingdao Taifu Huihong 
Jiuhao Private Equity 
Investment Fund 
Partnership (Limited 
Partnership) (青島泰富匯洪
玖號私募股權投資基金合
夥企業(有限合夥))
1,607,143
–
–
0.53%
July 7, 2027
Qingdao Taifu Hongying 
No. 1 Investment Center 
(Limited Partnership) (青島
泰富洪盈壹號投資中心(有
限合夥))
450,290
450,290
0.16%
0.15%
July 7, 2027
Subtotal
114,775,129
102,306,107
35.58%
37.72%
Note: 
The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws.

<<<PAGE 18>>>
18
PLACEE CONCENTRATION ANALYSIS
Placees
Number of 
H Shares allotted
Allotment as % of 
International Offering
Allotment as % of 
total Offer Shares
Number of Shares 
held upon Listing
% of total issued 
share capital upon Listing
Top 1
3,162,400
14.43%
11.55%
3,162,400
1.04%
Top 5
11,946,200
54.53%
43.62%
11,946,200
3.93%
Top 10
16,645,800
75.98%
60.78%
16,645,800
5.47%
Top 25
20,869,000
95.25%
76.20%
20,869,000
6.86%
Notes
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number of H 
Shares allotted
Allotment as % 
of International 
Offering
Allotment as 
% of total 
Offer Shares
Number of 
H Shares held 
upon Listing
% of total issued 
H Shares capital 
upon Listing
Number of 
Shares held 
upon Listing
Top 1
0
0.00%
0.00%
123,034,655
42.79%
127,320,916
Top 5
0
0.00%
0.00%
203,352,512
70.72%
207,638,773
Top 10
0
0.00%
0.00%
228,764,367
79.56%
235,750,628
Top 25
13,824,600
63.10%
50.48%
266,730,137
92.76%
274,408,723
Notes
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
Number of 
H Shares 
allotted
Allotment as % 
of International 
Offering
Allotment as 
% of total 
Offer Shares
Number of 
H Shares held 
upon Listing
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
123,034,655
127,320,916
41.84%
Top 5
0
0.00%
0.00%
203,352,512
207,638,773
68.24%
Top 10
0
0.00%
0.00%
228,650,737
236,329,323
77.67%
Top 25
11,946,200
54.53%
43.62%
261,846,067
276,033,161
90.71%
Notes
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 19>>>
19
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
No. of Shares
Applied For
No. of Valid
Applications
Basis of Allotment/Ballot
Approximate
Percentage 
Allotted 
of the Total 
No. of 
Shares 
Applied For
POOL A
200
99,878
169 out of 99,878 to receive 200 Shares
0.17%
400
11,148
38 out of 11,148 to receive 200 Shares
0.17%
600
6,025
31 out of 6,025 to receive 200 Shares
0.17%
800
2,744
19 out of 2,744 to receive 200 Shares
0.17%
1,000
3,948
33 out of 3,948 to receive 200 Shares
0.17%
1,200
1,607
16 out of 1,607 to receive 200 Shares
0.17%
1,400
11,136
132 out of 11,136 to receive 200 Shares
0.17%
1,600
2,395
32 out of 2,395 to receive 200 Shares
0.17%
1,800
927
14 out of 927 to receive 200 Shares
0.17%
2,000
9,404
159 out of 9,404 to receive 200 Shares
0.17%
3,000
5,426
137 out of 5,426 to receive 200 Shares
0.17%
4,000
2,776
94 out of 2,776 to receive 200 Shares
0.17%
5,000
1,684
71 out of 1,684 to receive 200 Shares
0.17%
6,000
1,809
92 out of 1,809 to receive 200 Shares
0.17%
7,000
1,073
63 out of 1,073 to receive 200 Shares
0.17%
8,000
1,145
77 out of 1,145 to receive 200 Shares
0.17%
9,000
792
60 out of 792 to receive 200 Shares
0.17%
10,000
5,619
474 out of 5,619 to receive 200 Shares
0.17%
20,000
4,636
783 out of 4,636 to receive 200 Shares
0.17%
30,000
2,938
744 out of 2,938 to receive 200 Shares
0.17%
40,000
2,492
842 out of 2,492 to receive 200 Shares
0.17%
50,000
1,584
669 out of 1,584 to receive 200 Shares
0.17%
60,000
1,670
846 out of 1,670 to receive 200 Shares
0.17%
70,000
1,117
660 out of 1,117 to receive 200 Shares
0.17%
80,000
1,016
686 out of 1,016 to receive 200 Shares
0.17%
90,000
885
672 out of 885 to receive 200 Shares
0.17%
100,000
1,623
1,370 out of 1,623 to receive 200 Shares
0.17%
120,000
1,193
200 Shares plus 16 out of 1,193 to receive additional 200 Shares
0.17%
140,000
2,963
200 Shares plus 539 out of 2,963 to receive additional 200 Shares
0.17%
191,653
Total number of Pool A successful applicants: 13,139

<<<PAGE 20>>>
20
No. of Shares
Applied For
No. of Valid
Applications
Basis of Allotment/Ballot
Approximate
Percentage 
Allotted 
of the Total 
No. of 
Shares 
Applied For
POOL B
160,000
5,404
2,383 out of 5,404 to receive 200 Shares
0.06%
180,000
1,165
578 out of 1,165 to receive 200 Shares
0.06%
200,000
2,239
1,234 out of 2,239 to receive 200 Shares
0.06%
250,000
1,174
809 out of 1,174 to receive 200 Shares
0.06%
300,000
1,056
873 out of 1,056 to receive 200 Shares
0.06%
350,000
596
575 out of 596 to receive 200 Shares
0.06%
400,000
659
200 Shares plus 67 out of 659 to receive additional 200 Shares
0.06%
450,000
347
200 Shares plus 83 out of 347 to receive additional 200 Shares
0.06%
500,000
372
200 Shares plus 141 out of 372 to receive additional 200 Shares
0.06%
550,000
212
200 Shares plus 109 out of 212 to receive additional 200 Shares
0.06%
600,000
310
200 Shares plus 203 out of 310 to receive additional 200 Shares
0.06%
650,000
155
200 Shares plus 123 out of 155 to receive additional 200 Shares
0.06%
684,600
2,364
200 Shares plus 2,096 out of 2,364 to receive additional 200 Shares
0.06%
16,053
Total number of Pool B successful applicants: 10,871
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 21>>>
21
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.
The Directors and the Overall Coordinators confirm that at least 50% of the total number of 
the Offer Shares have been allocated to and taken up by independent price setting investors in 
compliance with Rule 18C.08 of the Listing Rules.
The Directors further confirm that at least 20% of the issued share capital of the Company will be 
held by sophisticated independent investors at the time of Listing in compliance with Chapter 2.5 
of the Guide for New Listing Applicants.
OTHERS/ADDITIONAL INFORMATION
Reallocation
As (i) the Hong Kong Public Offering is oversubscribed by more than 50 times and (ii) the 
reallocation pursuant to Chapter 4.14 of the Guide for New Listing Applicants as described in the 
section headed “Structure of the Global Offering – The Hong Kong Public Offering – Reallocation” 
of the Prospectus is exercised, the clawback arrangement is triggered and Offer Shares were 
reallocated to the Hong Kong Public Offering from the International Offering, so that the total 
number of Offer Shares available under the Hong Kong Public Offering is 5,477,400 Offer Shares, 
representing 20% of the Offer Shares initially available under the Global Offering, assuming the 
Offer Size Adjustment Option is not exercised.
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit certain Offer Shares to be 
placed to a connected client of its connected distributor under the International Offering pursuant 
to the Placing Guidelines. Details of the placement to connected client are set out below. The 
allocation of Offer Shares to such connected client is in compliance with all the conditions under 
the consent granted by the Stock Exchange.

<<<PAGE 22>>>
22
No.
Connected 
Distributor
Connected
Client
Relationship
with the Connected 
Distributor
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
Maximum number 
of Offer Shares 
(rounded down 
to nearest whole 
board lot of 200 
Shares) to be 
allocated to the 
connected client
% of total number 
of Offer Shares
% of total issued 
H Shares after the 
Global Offering
% of total issued 
share capital 
after the Global 
Offering
1.
CITIC Securities 
Brokerage (HK) 
Limited (“CITIC 
Brokerage”)
CITIC Securities Asset 
Management Company 
Ltd (“CITIC Asset 
Management”)
See Note 1
No
1,400
0.0051%
0.00049%
0.00046%
Note:
1. 
CITIC Asset Management is a member of the same group of companies as CITIC Brokerage. CITIC Asset Management is therefore considered as a connected 
client of CITIC Brokerage pursuant to paragraph 1B(7) of Appendix F1 to the Listing Rules. CITIC Asset Management will hold the Offer Shares in its capacity 
as the discretionary fund manager managing on behalf of its underlying clients, each of which is an independent third party.
The underlying clients for purpose of this placing subscription include:
(A) 
CITIC SECURITIES AM-GUIBINFENGYUAN NO.118 QDII, the ultimate beneficial owner holding 30% interests or more in the fund is Zhang Guofeng 
(張國鋒), an independent third party of the Company and the connected person or the associates thereof, and CITIC Asset Management; and
(B) 
CITIC SECURITIES AM-GUIBINFENGYUAN NO.108 QDII, none of its ultimate beneficial owners hold 30% or more interest.
To the best of CITIC Brokerage’s knowledge and after making all reasonable enquiries, the underlying clients is an independent third party of (i) the Company, 
the connected person or the associates thereof, and (ii) CITIC Asset Management.

<<<PAGE 23>>>
23
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the 
“Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy 
or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
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
The Offer Shares are being offered and sold outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated June 29, 2026 issued by BASiC Semiconductor 
Co., Ltd. (深圳基本半導體股份有限公司) for detailed information about the Global Offering 
described below before deciding whether or not to invest in the Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the 
occurrence of any of the events set out in the section headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” in 
the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is 
currently expected to be on July 8, 2026).
PUBLIC FLOAT
Pursuant to Rule 19A.13A of the Listing Rules, assuming that the Over-allotment Option is 
not exercised, based on the Offer Price of HK$31.62 per Offer Share, our expected market 
capitalization upon the Listing is HK$9.62 billion, and the minimum prescribed public float 
percentage applicable to our Shares is 15.59%.
Immediately following the completion of the Global Offering and without taking into account the 
Over-allotment Option, an aggregate of 111,511,575 Shares or approximately 36.65% of the total 
issued share capital of the Company will be held in the public hands, satisfying the minimum 
percentage requirement in compliance with Rule 8.08(1) of the Listing Rules.

<<<PAGE 24>>>
24
The Directors confirm that, immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public Shareholders 
do not hold more than 50% of the Shares held in the public hands at the time of the Listing in 
compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 
Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, July 
8, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the paragraph headed “Underwriting – Underwriting Arrangements 
and Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has not 
been exercised. Investors who trade the Shares on the basis of publicly available allocation details 
prior to the receipt of Share certificates or prior to the Share certificates becoming valid evidence 
of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Wednesday, 
July 8, 2026 (Hong Kong time), it is expected that dealings in the Shares on the Stock Exchange 
will commence at 9:00 a.m. on Wednesday, July 8, 2026 (Hong Kong time). The Shares will be 
traded in board lots of 200 Shares each, and the stock code of the Shares will be 9971.
By order of the Board
BASiC Semiconductor Co., Ltd.
Dr. Wang Zhihan
Chairman
Hong Kong, July 7, 2026
Directors of the Company named in the application to which this announcement relates are: (i) Dr. 
Wang Zhihan, Dr. He Weiwei, Mr. Fu Junyin and Ms. Yan Rui as executive Directors; and (ii) Mr. 
Li Juping, Mr. Ye Xiang and Mr. Wang Susheng as independent non-executive Directors.
