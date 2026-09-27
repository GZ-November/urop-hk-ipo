# 配发结果公告抽取任务：6810.HK Shanghai Sunmi Technology Co., Ltd. - W - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**28/04/2026 22:30**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0428/2026042804737.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6810.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) and Hong 
Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those defined in 
the prospectus dated April 21, 2026 (the “Prospectus”) issued by Shanghai Sunmi Technology Co., Ltd. (上海商米科技集團股份
有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase or 
subscribe for securities. Potential investors should read the Prospectus for detailed information about the Company and the 
Global Offering described below before deciding whether or not to invest in the Offer Shares.
This announcement is not for release, publication or distribution, directly or indirectly, in or into the United States (including its 
territories and possessions, any state of the United States and the District of Columbia). This announcement does not constitute 
or form a part of any offer or solicitation to purchase or subscribe for securities in the United States or in any other jurisdiction. 
The Offer Shares have not been and will not be registered under the United States Securities Act of 1933, as amended from time 
to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the United States and may not be offered, 
sold, pledged or transferred within the United States, except in transactions exempt from, or not subject to, the registration 
requirements of the U.S. Securities Act. The Offer Shares may only be offered and sold outside the United States in offshore 
transactions in reliance on Regulation S. There will be no public offer of the Offer Shares in the United States.
No stabilizing manager will be appointed, and it is anticipated that no stabilization activities will be carried out in relation to the 
Global Offering.
Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators (for themselves and 
on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting — 
Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any 
time prior to 8:00 a.m. (Hong Kong time) on the Listing Date.
The Company is controlled through weighted voting rights. Prospective investors should be aware of the potential risks of 
investing in a company with a WVR structure, in particular that the WVR Beneficiary, whose interests may not necessarily be 
aligned with those of our Shareholders as a whole, will be in a position to exert significant influence over the outcome of our 
Shareholders’ resolutions, irrespective of how other Shareholders vote. For further information about the risks associated with 
the WVR structure, see “Risk Factors — Risks Related to the WVR Structure” in the Prospectus. Prospective investors should 
make the decision to invest in the Company only after due and careful consideration.

<<<PAGE 2>>>
2
Shanghai Sunmi Technology Co., Ltd.
上海商米科技集團股份有限公司
(A joint stock company controlled through weighted voting rights and incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under the 
Global Offering
:
42,626,800 H Shares
Number of Hong Kong Offer Shares
:
4,262,700 H Shares
Number of International Offer Shares
:
38,364,100 H Shares
Offer Price
:
HK$24.86 per H Share, plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
AFRC transaction levy of 0.00015% and 
Stock Exchange trading fee of 0.00565%
Nominal value
:
RMB1.00 per H Share
Stock code
:
6810
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and 
Joint Lead Managers
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
Shanghai Sunmi Technology Co., Ltd.
上海商米科技集團股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
6810
Stock short name
SUNMI TECH-W
Dealings commencement date
April 29, 2026*
*  see note at the end of the announcement
Price Information
Offer Price
HK$24.86
Offer Shares and Share Capital
Number of Offer Shares
42,626,800
Number of Offer Shares in Hong Kong Public Offering 
4,262,700
Number of Offer Shares in International Offering
38,364,100
Number of issued Shares upon Listing
402,626,800
Proceeds
Gross proceeds
(Note)
HK$1,059.7 million
  Less: Estimated listing expenses payable based on 
  Offer Price
HK$(137.7) million
Net proceeds
HK$922.0 million
Note:	
Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the use of proceeds, 
please refer to section headed “Future Plans and Use of Proceeds” of the Prospectus. During the Track Record 
Period, the listing expenses charged to consolidated statement of profit or loss and comprehensive income were 
RMB26.2 million.

<<<PAGE 4>>>
4
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
204,939
No. of successful applications
32,542
Subscription level
2,003.16 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong Public 
Offering
4,262,700
No. of Offer Shares reallocated from the International Offering to 
Hong Kong Public Offering
N/A
Final no. of Offer Shares under the Hong Kong Public Offering 
4,262,700
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering
10.00%
Note:	 For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to www.eipo.com.
hk/eIPOAllotment to perform a search by identification number or www.eipo.com.hk/eIPOAllotment for the full list of 
allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
181
Subscription Level
7.91 times
No. of Offer Shares initially available under the International 
Offering
38,364,100
No. of Offer Shares reallocated to the Hong Kong Public Offering
N/A
Final no. of Offer Shares under the International Offering
38,364,100
% of Offer Shares under the International Offering to the Global 
Offering
90.00%
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a 
waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit the Company to allocate certain Offer Shares in the International Offering to 
a close associate of an existing minority Shareholder as a cornerstone investor and (b) a consent 
under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants to permit the Company to allocate certain Offer Shares in the International Offering to 
the connected clients, (i) none of the Offer Shares subscribed by the placees and the public have 
been financed directly or indirectly by the Company, any of the Directors, chief executive of the 
Company, Controlling Shareholders, substantial Shareholders, existing Shareholders or any of its 
subsidiaries or their respective close associates; and (ii) none of the placees and the public who 
have purchased the Offer Shares are accustomed to taking instructions from the Company, any of 
the Directors, chief executive of the Company, Controlling Shareholders, substantial Shareholders, 
existing Shareholders or any of its subsidiaries or their respective close associates in relation to 
the acquisition, disposal, voting or other disposition of H Shares registered in his/her/its name or 
otherwise held by him/her/it.

<<<PAGE 6>>>
6
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of 
Offer Shares 
allocated
Approximate 
% of Offer 
Shares
Approximate 
% of the total 
issued H Shares 
immediately 
following 
completion of the 
Global Offering
Approximate % 
of total issued 
share capital 
after the Global 
Offering
Existing 
Shareholders 
or their close 
associates
China Orient Enhanced Income Fund
1,575,100
3.70%
0.52%
0.39%
No
XINWUTANG CO., LIMITED
(1)
9,945,700
23.33%
3.27%
2.47%
Yes
Notes:
(1)	
As disclosed in the section headed “Cornerstone Investors” in the Prospectus, XINWUTANG CO., LIMITED is a close 
associate of Shanshang Investment, an existing minority Shareholder of our Company, and Jiashan Xinwutang Equity 
Investment Partnership Enterprise (Limited Partnership) (嘉善新武塘股權投資合夥企業（有限合夥）), which wholly 
owns XINWUTANG CO., LIMITED, has entered into a cornerstone investment agreement with the Company. For further 
details of the cornerstone investment, please refer to the sections headed “Cornerstone Investors” and “Waivers - 
Waiver from Strict Compliance with Rule 10.04 of and Consent under Paragraph 1C(2) of Appendix F1 to the Listing 
Rules in respect of Subscriptions of Offer Shares by a Close Associate of an Existing Shareholder as Cornerstone 
Investor” of the Prospectus.
Allotees with Waivers/Consents Obtained
Investor
No. of 
Offer Shares 
allocated
Approximate 
% of Offer 
Shares
Approximate 
% of the total 
issued H Shares 
immediately 
following 
completion of the 
Global Offering
Approximate % 
of the total issued 
share capital 
immediately 
following 
completion of the 
Global Offering
Relationship
Allotee with a consent under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by a 
close associate of an existing minority Shareholder
(1)
XINWUTANG CO., LIMITED
9,945,700
23.33%
3.27%
2.47% A cornerstone 
investor and a 
close associate 
of an existing 
minority 
Shareholder.
Allotees with a consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to connected clients
(2)

<<<PAGE 7>>>
7
Investor
No. of 
Offer Shares 
allocated
Approximate 
% of Offer 
Shares
Approximate 
% of the total 
issued H Shares 
immediately 
following 
completion of the 
Global Offering
Approximate % 
of the total issued 
share capital 
immediately 
following 
completion of the 
Global Offering
Relationship
CITIC Securities Asset Management 
Company Limited (“CITIC Asset 
Management”)
7,000
0.01642%
0.00230%
0.00174% A connected 
client of 
CLSA Limited 
(“CLSA”) as 
placee
China Asset Management (Hong 
Kong) Limited (“China AMC HK”)
2,000
0.00469%
0.00066%
0.00050% A connected 
client of CLSA 
as placee
ABCI Asset Management Limited 
(“ABCI AM”)
(3)
1,300
0.00305%
0.00043%
0.00032% ABCI AM, 
ABCI Capital 
Limited (“ABCI 
Capital”) and 
ABCI Securities 
Company 
Limited (“ABCI 
Securities”) are 
group companies 
within the same 
group.
ABCI AM
(3)
1,300
0.00305%
0.00043%
0.00032% ABCI AM, 
ABCI Capital 
and ABCI 
Securities are 
group companies 
within the same 
group.
Notes:
(1)	
For details of a consent under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by a close associate of an existing 
minority Shareholder, please refer to the section headed “Others/Additional Information — Placing to a close associate of an existing minority 
Shareholder as a cornerstone investor” in this announcement.
(2)	
For details of a consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocations to connected clients, please refer to the section headed “Others/Additional Information — Placing to connected clients with a prior consent 
under paragraph 1C(1) of the Placing Guidelines” in this announcement.
(3)	
The 1,300 Offer Shares to be allocated to ABCI AM as a connected client of each of ABCI Capital and ABCI Securities will be allotted solely through 
ABCI Securities as the connected distributor. For the avoidance of doubt, such allocation of 1,300 Offer Shares to ABCI AM is a single allocation and 
should not be double-counted by reason of ABCI AM being a connected client of both ABCI Capital and ABCI Securities.

<<<PAGE 8>>>
8
LOCK-UP UNDERTAKINGS
Controlling Shareholders and/or Shareholders of Unlisted Shares
Name
Number of 
H Shares held 
in the Company 
subject to lock-up 
undertakings upon 
Listing
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
Approximate 
% of the total 
issued H 
Shares subject 
to lock-up 
undertakings 
upon Listing
Approximate 
% of the total 
issued share 
capital subject 
to lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings
(2)
Mr. Lin
(1) 
—
(1)
98,584,276 
Class A Shares
—
24.49%
April 28, 2027
Subtotal
—
98,584,276
Class A Shares
—
24.49%
Woyou ESOP
28,877,670
Class B Ordinary 
Shares
(1)
28,877,670
Class B Ordinary 
Shares
9.50% 
7.17% 
April 28, 2027
Woyou Partnership
10,622,371
Class B Ordinary 
Shares
(1)
10,622,371
Class B Ordinary 
Shares
3.49% 
2.64% 
April 28, 2027
Ningbo Woyou 
1,751,241
Class B Ordinary 
Shares
(1)
1,751,241 
Class B Ordinary 
Shares
0.58% 
0.43% 
April 28, 2027
Subtotal
41,251,282
Class B Ordinary 
Shares
41,251,282
Class B Ordinary 
Shares
13.57%
10.25%
Total
41,251,282
Class B Ordinary 
Shares
98,584,276
Class A Shares
41,251,282
Class B Ordinary 
Shares
13.57%
34.73%

<<<PAGE 9>>>
9
Name
Number of 
H Shares held 
in the Company 
subject to lock-up 
undertakings upon 
Listing
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
Approximate 
% of the total 
issued H 
Shares subject 
to lock-up 
undertakings 
upon Listing
Approximate 
% of the total 
issued share 
capital subject 
to lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings
(2)
Notes:
(1)	
Mr. Lin will directly hold 98,584,276 Class A Shares (all being Unlisted Shares which will not be converted into H 
Shares upon Listing) and will control a total of 41,251,282 Class B Ordinary Shares (all of which will be converted into 
H Shares upon Listing) through Woyou ESOP, Woyou Partnership and Ningbo Woyou as their general partner.
(2)	
The expiry day of the lock-up period shown in the table above is pursuant to the PRC Company Law. In accordance with 
the relevant Listing Rules and guidance materials, the required lock-up for the First Six-Month Period ends on October 
28, 2026 and the Second Six-Month Period ends on April 28, 2027.
Pre-IPO Investors
Name
(1)
Number of 
H Shares held 
in the Company 
subject to lock-
up undertakings 
upon Listing
Approximate 
% of the total 
issued H Shares 
subject to lock-
up undertakings 
upon Listing
Approximate 
% of the total 
issued share 
capital subject 
to lock-up 
undertakings 
upon Listing
Last day subject to the 
lock-up undertakings
(2)
Yunxin Venture
98,182,427
32.29%
24.39%
April 28, 2027
Hantao Consulting
29,515,358 
9.71% 
7.33% 
April 28, 2027
Jinxing Venture
28,011,271
9.21% 
6.96% 
April 28, 2027
Shenzhen Capital Group
24,777,737 
8.15%
6.15% 
April 28, 2027
Shanshang Investment
14,832,000
(3)
4.88% 
3.68% 
April 28, 2027
Ding Di
9,444,524 
3.11% 
2.35% 
April 28, 2027
Jiang Nanchun
(4)
5,042,068
1.66% 
1.25% 
April 28, 2027
Nongyin Wenying
4,660,874 
1.53% 
1.16% 
April 28, 2027
Baolong Investment
3,559,097 
1.17% 
0.88% 
April 28, 2027
Guangyi Investment
2,139,086 
0.70%
0.53% 
April 28, 2027
Subtotal
220,164,442
72.41%
54.68%

<<<PAGE 10>>>
10
Name
(1)
Number of 
H Shares held 
in the Company 
subject to lock-
up undertakings 
upon Listing
Approximate 
% of the total 
issued H Shares 
subject to lock-
up undertakings 
upon Listing
Approximate 
% of the total 
issued share 
capital subject 
to lock-up 
undertakings 
upon Listing
Last day subject to the 
lock-up undertakings
(2)
Notes:
(1)	
For details on the background of the Pre-IPO Investors, please refer to the section headed “History, Development and 
Corporate Structure — Pre-IPO Investments — Information of the Pre-IPO Investors” in the Prospectus.
(2)	
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law.
(3)	
Only represents the number of H Shares held by Shanshang Investment as a Pre-IPO Investor. For the lock-up of the 
Offer Shares allocated to a close associate of Shanshang Investment as a Cornerstone Investor, please refer to the 
section headed “Allotment Results Details — Lock-up Undertakings — Cornerstone Investors” in this announcement.
(4)	
To the best knowledge of the Company, the Shares held by Mr. Jiang Weiqiang were transferred to Mr. Jiang Nanchun, 
the son of Mr. Jiang Weiqiang.
Cornerstone Investors
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of the total 
issued H Shares 
subject to lock-
up undertakings 
upon Listing
% of the total 
issued share 
capital subject 
to lock-up 
undertakings 
upon Listing
Last day subject to the 
lock-up undertakings
(1)
China Orient Enhanced Income 
Fund
1,575,100
0.52%
0.39%
March 28, 2027
XINWUTANG CO., LIMITED
9,945,700
3.27%
2.47%
October 28, 2026
Subtotal
11,520,800
3.79%
2.86%
Notes:
(1)	
Each Cornerstone Investor shall not dispose of any of the Offer Shares acquired in the Global Offering at any time 
during the respective periods as set out above pursuant to their respective Cornerstone Investment Agreement, save 
for certain limited circumstances, such as transfers to any of its wholly-owned subsidiaries who will be bound by the 
same obligations of such cornerstone investor, including the lock-up period restriction. For details, please refer to the 
section headed “Cornerstone Investors — Restrictions on the Cornerstone Investors” of the Prospectus.

<<<PAGE 11>>>
11
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering
Allotment 
as % of 
total Offer 
Shares
Number of 
H Shares 
held upon 
Listing
% of 
total issued 
H Share 
capital upon 
Listing
% of 
total issued 
share capital 
upon Listing**
Top 1
12,241,500
31.91%
28.72%
12,241,500
4.03%
3.04%
Top 5
25,302,300
65.95%
59.36%
40,134,300
13.20%
9.97%
Top 10
27,463,100
71.59%
64.43%
42,295,100
13.91%
10.50%
Top 25
32,941,500
85.87%
77.28%
47,773,500
15.71%
11.87%
Notes
*	
Ranking of placees is based on the number of H Shares allotted to the placees.
**	
Total issued share capital upon Listing includes Class A Shares (i.e. Shares with weighted voting rights which will not be converted into H Shares upon Listing). For details on 
the weighted voting rights structure of the Company, please refer to the section headed “Share Capital” of the Prospectus.

<<<PAGE 12>>>
12
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
Allotment 
as % of 
total Offer 
Shares 
Number of 
H Shares 
held upon 
Listing
% of 
total issued 
H Share 
capital upon 
Listing**
% of 
total issued 
Share capital 
upon Listing
Number of 
Shares held 
upon Listing
Top 1
0
0.00%
0.00%
98,182,427
32.29%
24.39%
98,182,427
Top 5
0
0.00%
0.00%
221,738,075
72.93%
55.07%
320,322,351
Top 10
22,187,200
57.83%
52.05%
277,904,741
91.40%
69.02%
376,489,017
Top 25
29,474,100
76.83%
69.14%
290,889,824
95.67%
72.25%
389,474,100
Notes
*	
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
**	
Total issued share capital upon Listing includes Class A Shares (i.e. Shares with weighted voting rights which will not be converted into H Shares upon Listing). For details on 
the weighted voting rights structure of the Company, please refer to the section headed “Share Capital” of the Prospectus.

<<<PAGE 13>>>
13
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
Allotment 
as % of 
total Offer 
Shares
Number of 
H Shares 
held upon 
Listing
Number of 
Shares held 
upon Listing
% of 
total issued 
Share capital 
upon Listing**
Top 1
0
0.00%
0.00%
41,251,282
139,835,558
34.73%
Top 5
0
0.00%
0.00%
221,738,075
320,322,351
79.56%
Top 10
22,187,200
57.83%
52.05%
277,904,741
376,489,017
93.51%
Top 25
29,474,100
76.83%
69.14%
290,889,824
389,474,100
96.73%
Notes
*	
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.
**	
Total issued share capital upon Listing includes Class A Shares (i.e. Shares with weighted voting rights which will not be converted into H Shares upon Listing). For details on 
the weighted voting rights structure of the Company, please refer to the section headed “Share Capital” of the Prospectus.

<<<PAGE 14>>>
14
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by the 
public will be conditionally allocated on the basis set out below:
POOL A
NO. OF SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
100
51,358
2,568 out of 51,358 to receive 100 H Shares
5.00%
200
9,702
494 out of 9,702 to receive 100 H Shares
2.55%
300
24,962
1,285 out of 24,962 to receive 100 H Shares
1.72%
400
5,399
281 out of 5,399 to receive 100 H Shares
1.30%
500
5,126
268 out of 5,126 to receive 100 H Shares
1.05%
600
3,367
177 out of 3,367 to receive 100 H Shares
0.88%
700
2,582
136 out of 2,582 to receive 100 H Shares
0.75%
800
2,874
152 out of 2,874 to receive 100 H Shares
0.66%
900
1,879
100 out of 1,879 to receive 100 H Shares
0.59%
1,000
10,233
550 out of 10,233 to receive 100 H Shares
0.54%
1,500
13,957
755 out of 13,957 to receive 100 H Shares
0.36%
2,000
3,817
207 out of 3,817 to receive 100 H Shares
0.27%
2,500
1,722
94 out of 1,722 to receive 100 H Shares
0.22%
3,000
2,186
130 out of 2,186 to receive 100 H Shares
0.20%
3,500
3,457
220 out of 3,457 to receive 100 H Shares
0.18%
4,000
2,363
155 out of 2,363 to receive 100 H Shares
0.16%
4,500
1,421
95 out of 1,421 to receive 100 H Shares
0.15%
5,000
2,970
205 out of 2,970 to receive 100 H Shares
0.14%
6,000
2,300
180 out of 2,300 to receive 100 H Shares
0.13%
7,000
2,119
175 out of 2,119 to receive 100 H Shares
0.12%
8,000
2,222
189 out of 2,222 to receive 100 H Shares
0.11%
9,000
1,804
160 out of 1,804 to receive 100 H Shares
0.10%
10,000
7,625
708 out of 7,625 to receive 100 H Shares
0.09%
20,000
4,790
735 out of 4,790 to receive 100 H Shares
0.08%
30,000
3,578
720 out of 3,578 to receive 100 H Shares
0.07%
40,000
2,798
728 out of 2,798 to receive 100 H Shares
0.07%
50,000
8,523
2,772 out of 8,523 to receive 100 H Shares
0.07%
100,000
4,322
2,820 out of 4,322 to receive 100 H Shares
0.07%
150,000
1,922
100 H Shares
0.07%
200,000
2,212
100 H Shares plus 121 out of 
  2,212 to receive additional 100 H Shares
0.05%
 
Total
193,590
Total number of Pool A successful 
  applicants: 21,193
 

<<<PAGE 15>>>
15
POOL B
NO. OF SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
250,000
3,990
100 H Shares plus 1,391 out of 3,990 to receive 
  additional 100 H Shares
0.05%
300,000
1,236
100 H Shares plus 532 out of 1,236 to receive 
  additional 100 H Shares
0.05%
350,000
860
100 H Shares plus 441 out of 860 to receive 
  additional 100 H Shares
0.04%
400,000
787
100 H Shares plus 470 out of 787 to receive 
  additional 100 H Shares
0.04%
450,000
545
100 H Shares plus 377 out of 545 to receive 
  additional 100 H Shares
0.04%
500,000
777
200 H Shares
0.04%
600,000
560
200 H Shares plus 10 out of 560 to receive 
  additional 100 H Shares
0.03%
700,000
370
200 H Shares plus 42 out of 370 to receive 
  additional 100 H Shares
0.03%
800,000
355
200 H Shares plus 100 out of 355 to receive 
  additional 100 H Shares
0.03%
900,000
218
200 H Shares plus 99 out of 218 to receive 
  additional 100 H Shares
0.03%
1,000,000
565
300 H Shares
0.03%
1,500,000
311
300 H Shares plus 145 out of 311 to receive 
  additional 100 H Shares
0.02%
2,131,300
775
400 H Shares
0.02%
 
Total
11,349
Total number of Pool B successful 
  applicants: 11,349
 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 16>>>
16
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consents have been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and Stock Exchange trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Placing to a close associate of an existing minority Shareholder as a cornerstone investor
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(2) of the Placing Guidelines to allow XINWUTANG CO., LIMITED 
to participate in the Global Offering as a cornerstone investor. For details, see the section headed 
“Waivers — Waiver from Strict Compliance with Rule 10.04 of and Consent Under Paragraph 
1C(2) of Appendix F1 to the Listing Rules in respect of Subscriptions of Offer Shares by a Close 
Associate of an Existing Shareholder as Cornerstone Investor” in the Prospectus. Such allocations 
of Offer Shares are in compliance with all the conditions under the consent granted by the Stock 
Exchange.
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates, 
please refer to the section headed “Allotment Results Details — International Offering — 
Cornerstone Investors” in this announcement.

<<<PAGE 17>>>
17
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their connected distributors pursuant to the 
Placing Guidelines.
The Company has applied to the Stock Exchange, and the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing 
Guidelines to permit the Company to allocate such Offer Shares in the International Offering to the connected clients listed below. The 
allocation of Offer Shares to such connected clients is in compliance with all the conditions under a consent granted by the Stock Exchange. 
Details of the placement to connected clients are set out below:
Connected 
Distributor
Connected Client
Relationship
Whether the 
connected 
clients will hold 
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
No. of Offer 
Shares allocated
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which is 
not authorized 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of 
such scheme
Approximate % 
of Offer Shares
Approximate %  
of the total 
issued H Shares 
immediately 
following 
completion of 
the
Global Offering
Approximate % 
of the total issued 
share capital 
immediately 
following 
completion of the 
Global Offering
CLSA
CITIC Asset 
Management
(1)
CITIC Asset
Management is 
a member of the 
same group of 
companies as 
CLSA. 
Discretionary 
basis
7,000 
Yes
0.01642%
0.00230%
0.00174% 

<<<PAGE 18>>>
18
Connected 
Distributor
Connected Client
Relationship
Whether the 
connected 
clients will hold 
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
No. of Offer 
Shares allocated
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which is 
not authorized 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of 
such scheme
Approximate % 
of Offer Shares
Approximate %  
of the total 
issued H Shares 
immediately 
following 
completion of 
the
Global Offering
Approximate % 
of the total issued 
share capital 
immediately 
following 
completion of the 
Global Offering
CLSA
China AMC 
HK
(2)
China
AMC HK is a 
member of the 
same group of 
companies as 
CLSA.
Discretionary 
basis
2,000 
No
0.00469%
0.00066%
0.00050%
ABCI 
Capital
ABCI AM
(3)
ABCI AM, 
ABCI Capital 
and ABCI 
Securities 
are  group 
companies 
within the same 
group.
Discretionary 
basis
1,300
Yes
(3)
0.00305%
0.00043%
0.00032%

<<<PAGE 19>>>
19
Connected 
Distributor
Connected Client
Relationship
Whether the 
connected 
clients will hold 
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
No. of Offer 
Shares allocated
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which is 
not authorized 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of 
such scheme
Approximate % 
of Offer Shares
Approximate %  
of the total 
issued H Shares 
immediately 
following 
completion of 
the
Global Offering
Approximate % 
of the total issued 
share capital 
immediately 
following 
completion of the 
Global Offering
ABCI 
Securities
ABCI AM
(3)
ABCI AM, 
ABCI Capital 
and ABCI 
Securities 
are  group 
companies 
within the same 
group.
Discretionary 
basis
1,300
Yes
(3)
0.00305%
0.00043%
0.00032%
Notes:
(1)	
CITIC Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their investors (the “CITIC Asset 
Management Ultimate Clients”), each of which is, to the best knowledge of CITIC Asset Management, (i) an independent third party of the Company, its subsidiaries, its 
substantial shareholders, CITIC Asset Management, CLSA and the companies which are members of the same group of companies as CLSA; and (ii) a collective investment 
scheme which is not authorized by the SFC. No ultimate beneficial owner holds 30% or more interest in the funds.

<<<PAGE 20>>>
20
Connected 
Distributor
Connected Client
Relationship
Whether the 
connected 
clients will hold 
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
No. of Offer 
Shares allocated
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which is 
not authorized 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of 
such scheme
Approximate % 
of Offer Shares
Approximate %  
of the total 
issued H Shares 
immediately 
following 
completion of 
the
Global Offering
Approximate % 
of the total issued 
share capital 
immediately 
following 
completion of the 
Global Offering
The details of the CITIC Asset Management Ultimate Clients, which are the collective investment schemes not authorized by the SFC, are as follow:
Fund Name
Values of Assets 
under Management
Whether the Scheme 
is Publicly Marketed
Fund Manager
UBO of Fund 
Manager
Limited Partner of the CITIC 
Asset Management Ultimate 
Clients
CITIC SECURITIES COMPANY LIMITED-
XINHANG ZHIYUAN NO.1
(中信證券信航致遠1號集合資產管理計劃)
RMB26,274,974.36
Not publicly marketed CITIC Asset 
Management
CITIC Securities 
Company Limited
26 limited partners in total, all of 
which are individuals
CITIC SECURITIES COMPANY LIMITED-
XINHANG ZHIYUAN NO.3
(中信證券信航致遠3號集合資產管理計劃)
RMB62,521,444.68
Not publicly marketed CITIC Asset 
Management
CITIC Securities 
Company Limited
48 limited partners in total, all of 
which are individuals
CITIC Securities AM-Guibinfengyuan 
No.118 QDII 
(中信證券資管貴賓豐元118號QDII
集合資產管理計劃) 
RMB226,629,029.61
Not publicly marketed CITIC Asset 
Management
CITIC Securities 
Company Limited
Eight limited partners in total, 
each of which is either a single 
asset management scheme or 
a collective asset management 
scheme
To the best of knowledge of CITIC Asset Management and after making all reasonable enquiries, (i) each of the CITIC Asset Management Ultimate Client, together with each of 
their ultimate beneficial owners, is an independent third party of the Company, its subsidiaries, its substantial shareholders, CITIC Asset Management, CLSA and the companies 
which are members of the same group of companies as CLSA, and (ii) none of CLSA and any companies which are members of the same group of companies as CLSA hold any 
beneficial interest in any of CITIC Asset Management Ultimate Clients.

<<<PAGE 21>>>
21
Connected 
Distributor
Connected Client
Relationship
Whether the 
connected 
clients will hold 
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
No. of Offer 
Shares allocated
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which is 
not authorized 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of 
such scheme
Approximate % 
of Offer Shares
Approximate %  
of the total 
issued H Shares 
immediately 
following 
completion of 
the
Global Offering
Approximate % 
of the total issued 
share capital 
immediately 
following 
completion of the 
Global Offering
(2)	
China AMC HK will hold the Offer Shares in its capacity as the discretionary fund manager managing on behalf of its underlying clients (the “China AMC HK Underlying 
Clients”), each of which is an independent third party. To the best of knowledge of China AMC HK and after making all reasonable enquiries, (i) the underlying clients is 
an independent third party of the Company, its subsidiaries, its substantial shareholders, China AMC HK, CLSA and the companies which are members of the same group 
of companies as CLSA, and (ii) none of CLSA and any companies which are members of the same group of companies as CLSA hold any beneficial interest in any of the 
underlying clients of China AMC HK.
The details of the China AMC HK Underlying Clients are as follow:
Fund Name
UBO/Shareholding holding 30% or more in the Fund
CHINAAMC SELECT GREATER CHINA TECHNOLOGY FUND
Futu Securities International (Hong Kong) Limited — client account
CHINAAMC FUND — CHINAAMC
CHINA OPPORTUNITIES FUND
N/A
CHINAAMC CHINA FOCUS FUND
Manulife (International) Limited
CHINAAMC CHINA GROWTH FUND (SICAV)
Yuanta Securities (HK) Company Limited

<<<PAGE 22>>>
22
Connected 
Distributor
Connected Client
Relationship
Whether the 
connected 
clients will hold 
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
No. of Offer 
Shares allocated
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which is 
not authorized 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of 
such scheme
Approximate % 
of Offer Shares
Approximate %  
of the total 
issued H Shares 
immediately 
following 
completion of 
the
Global Offering
Approximate % 
of the total issued 
share capital 
immediately 
following 
completion of the 
Global Offering
(3)	
ABCI AM intends to hold the Offer Shares in its capacity as manager managing investment portfolios on behalf of underlying investors (the “ABCI AM Ultimate Clients”) 
who are independent third parties on a discretionary basis. To the best of knowledge of ABCI AM and after making all reasonable enquiries, (i) each of the ABCI AM 
Ultimate Client, together with each of their ultimate beneficial owners, is an independent third party of the Company, its subsidiaries, its substantial shareholders, ABCI 
Capital, ABCI Securities and the companies which are members of the same group of companies as ABCI Capital and ABCI Securities, and (ii) none of ABCI Capital, ABCI 
Securities and the companies which are members of the same group of companies as ABCI Capital and ABCI Securities hold any beneficial interest in any of ABCI Asset AM 
Ultimate Clients.
	
The 1,300 Offer Shares proposed to be allocated to ABCI AM as a connected client of each of ABCI Capital and ABCI Securities will be placed solely through ABCI 
Securities as the connected distributor. For the avoidance of doubt, such allocation of 1,300 Offer Shares to ABCI AM is a single allocation and should not be double-counted 
by reason of ABCI AM being a connected client of both ABCI Capital and ABCI Securities.

<<<PAGE 23>>>
23
Connected 
Distributor
Connected Client
Relationship
Whether the 
connected 
clients will hold 
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
No. of Offer 
Shares allocated
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which is 
not authorized 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of 
such scheme
Approximate % 
of Offer Shares
Approximate %  
of the total 
issued H Shares 
immediately 
following 
completion of 
the
Global Offering
Approximate % 
of the total issued 
share capital 
immediately 
following 
completion of the 
Global Offering
The details of the ABCI AM Ultimate Clients are as follow:
Fund Name
Whether the Scheme 
is Publicly Marketed
Number of Offer 
Shares intended to be 
allocated to the Fund Fund Manager
UBO of Fund 
Manager
Limited Partner of the ABCI AM 
Ultimate Clients
ABCI Asset Management Limited — Client A/
C — ABCI Global Opportunities SPC — ABCI 
China Rising 6 SP
Not publicly marketed 700
ABCI Asset 
Management Limited
Agricultural Bank of 
China
3 limited partners in total, all of 
which are individuals, WEI Dezhi 
holds 55%, CHEN Dong holds 
30%.
ABCI Asset Management Limited — Client A/
C — E-Star
Not publicly marketed 600
ABCI Asset 
Management Limited
Agricultural Bank of 
China
1 limited partner in total, which 
is a HK listed company, E-Star 
Commercial Management 
Company Limited (6668HK).
ABCI Asset Management Limited — Client A/C — ABCI Global Opportunities SPC — ABCI China Rising 6 SP is a collective investment schemes not authorized by the SFC.

<<<PAGE 24>>>
24
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the 
“Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy or 
completeness and expressly disclaim any liability whatsoever for any loss howsoever arising from 
or in reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication or distribution, directly or indirectly, in or 
into the United States (including its territories and possessions, any state of the United States 
and the District of Columbia). This announcement does not constitute or form a part of any 
offer or solicitation to purchase or subscribe for securities in the United States or in any other 
jurisdiction. The Offer Shares have not been and will not be registered under the United States 
Securities Act of 1933, as amended from time to time (the “U.S. Securities Act”) or securities 
law of any state or other jurisdiction of the United States and may not be offered, sold, pledged 
or transferred within the United States, except in transactions exempt from, or not subject to, the 
registration requirements of the U.S. Securities Act. The Offer Shares may only be offered and 
sold outside the United States in offshore transactions in reliance on Regulation S. There will be 
no public offer of the Offer Shares in the United States.
The Offer Shares are being offered and sold outside the United States to investors that are not 
U.S. persons nor persons acquiring for the account or benefit of U.S. persons in reliance on 
Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated April 21, 2026 issued by Shanghai Sunmi Technology 
Co., Ltd. (上海商米科技集團股份有限公司) for detailed information about the Global Offering 
described above before deciding whether or not to invest in the H Shares thereby being offered.
Potential investors of the Offer Shares should note that the Joint Sponsors and Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the paragraph headed “Underwriting 
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Hong Kong 
Underwriting Agreement — Grounds for Termination” in the Prospectus at any time prior to 8:00 
a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on April 29, 2026).

<<<PAGE 25>>>
25
PUBLIC FLOAT AND FREE FLOAT
Based on the Offer Price, the minimum percentage of H Shares required to be held in public 
hands under Rule 8.08(1) (as amended and replaced by Rule 19A.13A(1)) of the Listing Rules 
is 15%, being the higher of (i) the percentage that would result in the expected market value of 
such securities in public hands to be HK$1.5 billion at the time of Listing, and (ii) 15%. Upon 
completion of the Global Offering, 164,608,815 H Shares, representing approximately 54.14% of 
the total number of H Shares of our Company, will be counted towards the public float, thereby 
satisfying the minimum public float requirements under Rule 8.08(1) (as amended and replaced by 
Rule 19A.13A(1)) of the Listing Rules.
Pursuant to the PRC Company Law, all Shares issued prior to the Listing shall not be transferred 
within one year from the Listing Date. In addition, each of the cornerstone investors has agreed to 
a lock-up period of six months or longer following the Listing Date. As such, H Shares held by the 
cornerstone investors upon the Listing shall not be counted towards the free float of the H Shares 
of the Company at the time of Listing. Immediately following completion of the Listing, a market 
capitalization of approximately HK$773 million of the H Shares listed on the Stock Exchange 
are not subject to such disposal restrictions at the time of the Listing (based on the Offer Price), 
representing 10.23% of our total number of H Shares, which will be counted as the free float. 
Accordingly, our Company will be able to satisfy the requirements under Rule 19A.13C(1)(b) of the 
Listing Rules.
The Directors also confirm that immediately following the completion of the Global Offering, 
(i) no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder upon Listing; and (iii) there will be at least 300 Shareholders at the time of the Listing 
in compliance with Rule 8.08(2) of the Listing Rules.

<<<PAGE 26>>>
26
COMMENCEMENT OF DEALINGS
Share certificates for the Offer Shares will only become valid evidence of title at 8:00 a.m. on 
Wednesday, April 29, 2026 (Hong Kong time), provided that (i) the Global Offering has become 
unconditional in all respects at or before that time, and (ii) the right of termination as described 
in the paragraph headed “Underwriting — Underwriting Arrangements and Expenses — Hong 
Kong Public Offering — Hong Kong Underwriting Agreement — Grounds for Termination” in the 
Prospectus has not been exercised. Investors who trade H Shares on the basis of publicly available 
allocation details before the receipt of H Share certificates or before the H Share certificates become 
valid evidence of title do so entirely at their own risk.
Assuming that the Hong Kong Public Offering becomes unconditional at or before 8:00 a.m. in 
Hong Kong on Wednesday, April 29, 2026, it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Wednesday, April 29, 2026. The H Shares will be traded 
in board lots of 100 H Shares each and the stock code of the H Shares will be 6810.
By order of the Board
Shanghai Sunmi Technology Co., Ltd.
Mr. Lin Zhe
Executive Director, Chairman of the 
Board and General Manager
Hong Kong, April 28, 2026
Directors of the Company named in the application to which this announcement relates are Mr. Lin Zhe, Mr. Chen Xiaojing, 
Mr. Zhang Jinpu and Mr. Chen Guihong as executive directors; Mr. Wang Huan and Ms. Zhang Yi as non-executive directors; 
Mr. Li Shihong, Ms. Wang Xia and Mr. Poon Wing Shing, Anthony as independent non-executive directors.
