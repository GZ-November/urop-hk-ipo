# 配发结果公告抽取任务：2797.HK Jiangxi Qiyunshan Food Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**08/07/2026 21:13**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0708/2026070801132.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2797.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the ‘‘Stock
Exchange’’) and Hong Kong Securities Clearing Company Limited (‘‘HKSCC’’) take no responsibility for the
contents of this announcement, make no representation as to its accuracy or completeness and expressly
disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any part
of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as
those defined in the prospectus dated 30 June 2026 (the ‘‘Prospectus’’) issued by Jiangxi Qiyunshan Food Co.,
Ltd.（江西齊雲山食品股份有限公司）(the ‘‘Company’’).
This announcement is for information purposes only and does not constitute an offer or an invitation to induce
an offer by any person to acquire, purchase or subscribe for any securities of the Company. This announcement
is not a prospectus. Potential investors should read the Prospectus for detailed information about the Company
and the Global Offering described below before deciding whether or not to invest in the Offer Shares. Any
investment decision in relation to the Offer Shares should be taken solely in reliance on the information
provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United
States (including its territories and possessions, any state of the United States and the District of Columbia).
This announcement does not, and is not intended to, constitute or form a part of any offer to sell or solicitation
to purchase or subscribe for any securities in the United States. The Offer Shares have not been, and will not
be, registered under the United States Securities Act of 1933, as amended (the ‘‘U.S. Securities Act’’) or
securities law of any state or other jurisdiction of the United States. The Offer Shares may not be offered, sold,
pledged or otherwise transferred within the United States, except pursuant to an available exemption from, or
in a transaction not subject to, the registration requirements of the U.S. Securities Act. There will be no public
offer of the Offer Shares in the United States. The Offer Shares are being offered and sold solely outside the
United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, Zhongtai International Securities Limited as stabilising manager (the
‘‘Stabilising Manager’’), its affiliates or any person acting for it, on behalf of the Underwriters, may over-
allocate or effect transactions with a view to stabilising or supporting the market price of the Shares at a level
higher than that which might otherwise prevail for a limited period after the Listing Date. However, there is no
obligation on the Stabilising Manager, its affiliates or any person acting for it to conduct any such stabilising
action, which, if commenced, will be done at the sole and absolute discretion of the Stabilising Manager, its
affiliates or any person acting for it, and may be discontinued at any time. Any such stabilising action is
required to be brought to an end on the 30th day after the last day for the lodging of applications under the
Hong Kong Public Offering. Such stabilising action, if taken, may be effected in all jurisdictions where it is
permissible to do so, in each case in compliance with all applicable laws, rules and regulatory requirements,
including the Securities and Futures (Price Stabilising) Rules (Chapter 571W of the Laws of Hong Kong), as
amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that stabilising action cannot be taken to support the price of the Shares for
longer than the stabilisation period which begins on the Listing Date and is expected to expire on the 30th day
after the last day for the lodging of applications under the Hong Kong Public Offering. After this date, no
further stabilising action may be taken, and demand for the Shares and the price of the Shares could fall.
In connection with the Global Offering, Zhongtai International Capital Limited acts as the Sole Sponsor and
Zhongtai International Securities Limited act as the Sole Overall Coordinator.
The Sole Overall Coordinator confirm that there has been no over-allocation of the H Shares under the
International Offering, therefore, there will not be any delayed delivery arrangement and the Over-allotment
Option will not be exercised. In view of the fact that there has been no over-allocation of the H Shares under
the International Offering, no stabilising action as described in the Prospectus will be taken during the
stabilisation period.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions
set out in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong
Kong and/or not resident in Hong Kong. Potential investors of the Offer Shares should note that the Sole
Overall Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in
the section headed ‘‘Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering
— Grounds for Termination’’ in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing
Date.
1

<<<PAGE 2>>>
江西齊雲山食品股份有限公司
Jiangxi Qiyunshan Food Co., Ltd.
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the
Global Offering
:
25,000,000 H Shares
Number of Hong Kong Offer Shares
:
2,500,000 H Shares
Number of International Offer Shares
:
22,500,000 H Shares
Final Offer Price
:
HK$8.00 per H Share plus brokerage
of 1.0%, SFC transaction levy of
0.0027%, Stock Exchange trading fee
of 0.00565% and AFRC transaction
levy of 0.00015%
Nominal value
:
RMB1.00 per H Share
Stock Code
:
2797
Sole Sponsor
Зࡋ⳪暲
@:9)
Sole Overall Coordinator, Sole Global Coordinator,
Joint Bookrunner and Joint Lead Manager
Зࡋ⳪暲
@:9)
Joint Bookrunners and Joint Lead Managers
2

<<<PAGE 3>>>
JIANGXI QIYUNSHAN FOOD CO., LTD. / 江西齊雲山食品股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the
same meanings as those defined in the prospectus dated 30 June 2026 (the ‘‘Prospectus’’)
issued by Jiangxi Qiyunshan Food Co., Ltd. (the ‘‘Company’’).
Warning: In view of high concentration of shareholding in a small number of
Shareholders, Shareholders and prospective investors should be aware that the price
of the H Shares could move substantially even with a small number of H Shares
traded and should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
2797
Stock short name
QIYUNSHAN FOOD
Dealings commencement date
9 July 2026*
*
see note at the end of the announcement
Price Information
Final Offer Price
HK$8.00
Offer Price Range
HK$5.00 – HK$8.00
Offer Shares and Share Capital
Number of Offer Shares
25,000,000
Final Number of Offer Shares in Hong Kong Public Offering
2,500,000
Final Number of Offer Shares in International Offering
22,500,000
Number of issued shares upon Listing
100,000,000
Proceeds
Gross proceeds (Note)
HK$200.0 million
Less: Estimated listing expenses payable based on Final
Offer Price
HK$ (33.0) million
Net proceeds
HK$167.0 million
Note: Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the use
of proceeds, please refer to the section headed ‘‘Future Plans and Use of Proceeds’’ of the Prospectus.
3

<<<PAGE 4>>>
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
95,307
No. of successful applications
4,876
Subscription level
1,688.1
times
Reallocation
No
No. of Offer Shares initially available under the Hong Kong Public Offering
2,500,000
No. of Offer Shares reallocated from the International Offering
—
Final no. of Offer Shares under the Hong Kong Public Offering
2,500,000
% of Offer Shares under the Hong Kong Public Offering to the
Global Offering
10.00%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can
refer to www.unioniporesults.com.hk to perform a search by name or identification number or
www.unioniporesults.com.hk for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
85
Subscription Level
1.51 times
No. of Offer Shares initially available under the International Offering
22,500,000
Final no. of Offer Shares under the International Offering
22,500,000
% of Offer Shares under the International Offering to the Global
Offering
90.00%
4

<<<PAGE 5>>>
The Directors confirm that, to the best of their knowledge, information and belief, (i) none
of the Offer Shares subscribed by the placees and the public have been financed directly or
indirectly by the Company, any of the Directors, chief executive of the Company,
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company or
any of its subsidiaries or their respective close associates; and (ii) none of the placees and
the public who have purchased the Offer Shares are accustomed to taking instructions from
the
Company,
any
of
the
Directors,
chief
executive
of
the
Company,
Controlling
Shareholders, substantial Shareholders, existing Shareholders of the Company or any of its
subsidiaries or their respective close associates in relation to the acquisition, disposal, voting
or other disposition of H Shares registered in his/her/its name or otherwise held by
him/her/it.
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name Note 1
Number of
Shares held in
the Company
subject to
lock-up
undertakings
immediately
upon Listing
% of total
issued H Shares
after the
Global Offering
subject to
lock-up
undertakings
upon
Listing Note 3
% of
shareholding in
the Company
subject to
lock-up
undertakings
upon Listing
Last day subject
to the lock-up
undertakings Note 2
Chongyi Food Factory
Note 4
56,250,000
—
56.25%
8 July 2027
Yunzhishang LP Note 4
18,750,000
—
18.75%
8 July 2027
Total
75,000,000
—
75.00%
Notes:
1.
For illustrative purposes only, this subsection lists only those members of the Controlling Shareholders
who hold Shares directly in the Company.
2.
Pursuant to the applicable PRC law, the lock-up for existing Shareholders ends on 8 July 2027, being 12
months from the Listing Date. Pursuant to Rule 10.07 of the Listing Rules, each of the Controlling
Shareholders has undertaken to the Stock Exchange and the Company that, he/she/it shall comply with
the applicable lock-up requirements. For further details, please refer to the section headed ‘‘Underwriting
— Undertakings to the Stock Exchange pursuant to the Listing Rules — Undertaking by our Controlling
Shareholders’’ in the Prospectus.
5

<<<PAGE 6>>>
3.
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares
to be issued under the Global Offering.
4.
As at the date of this announcement, the Core Management Shareholders, namely Mr. Liu Zhigao, Mr.
Zhu Fangyong, Mr. Liu Jiyan, Ms. Yang Yulan, Mr. Huang Zhongming and Mr. Ling Huashan, who in
aggregate held over two-thirds of the equity interest in Chongyi Food Factory and over two-thirds of the
partnership interest in Yunzhishang LP, had entered into a concert party agreement. Due to their
collective shareholding control in Chongyi Food Factory and Yunzhishang LP, as well as their
management influence over the Company as the executive Directors, the Core Management Shareholders
are considered the Controlling Shareholders and each of them is deemed to be interested in the entire
shareholding of the Company held by Chongyi Food Factory and Yunzhishang LP. For details, please
refer to the section headed ‘‘Relationship with Our Controlling Shareholders’’ in the Prospectus.
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of
H Shares
allotted
Allotment as
% of
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
6,186,500
27.50%
24.75%
6,186,500
6.19%
Top 5
13,038,500
57.95%
52.15%
13,038,500
13.04%
Top 10
16,743,500
74.42%
66.97%
16,743,500
16.74%
Top 25
20,164,500
89.62%
80.66%
20,164,500
20.16%
Note
*
Ranking of placees is based on the number of H Shares allotted to the placees.
6

<<<PAGE 7>>>
H SHAREHOLDERS CONCENTRATION ANALYSIS
H
Shareholders*
Number of
H Shares
allotted
Allotment as
% of
International
Offering
Allotment as
% of total
Offer Shares
Number of
H Shares
held upon
Listing
% of total
issued H
Shares
capital upon
Listing
Number of
Shares held
upon Listing
% of total
issued share
capital upon
Listing
Top 1
6,186,500
27.50%
24.75%
6,186,500
24.75%
6,186,500
6.19%
Top 5
13,038,500
57.95%
52.15%
13,038,500
52.15%
13,038,500
13.04%
Top 10
16,743,500
74.42%
66.97%
16,743,500
66.97%
16,743,500
16.74%
Top 25
20,164,500
89.62%
80.66%
20,164,500
80.66%
20,164,500
20.16%
Note
*
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
Number of
H Shares
allotted
Allotment as
% of
International
Offering
Allotment as
% of total
Offer Shares
Number of
H Shares
held upon
Listing
Number of
Shares held
upon
Listing
% of total
issued share
capital upon
Listing
Top 1
–
0.00%
0.00%
–
56,250,000
56.25%
Top 5
10,564,500
46.95%
42.26%
10,564,500
85,564,500
85.56%
Top 10
15,512,500
68.94%
62.05%
15,512,500
90,512,500
90.51%
Top 25
19,868,500
88.30%
79.47%
19,868,500
94,868,500
94.87%
Note
*
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon
Listing.
7

<<<PAGE 8>>>
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications
made by the public will be conditionally allocated on the basis set out below:
Pool A
Number
of H Shares
applied for
Number
of valid
applications
Basis of allocation/ballot
Approximate
percentage
allotted of the
total number
of H Shares
applied for
500
47,933
43 out of 47,933 applications to receive 500 H shares
0.09%
1,000
21,291
42 out of 21,291 applications to receive 500 H shares
0.10%
1,500
2,384
8 out of 2,384 applications to receive 500 H shares
0.11%
2,000
827
3 out of 827 applications to receive 500 H shares
0.09%
2,500
949
5 out of 949 applications to receive 500 H shares
0.11%
3,000
479
3 out of 479 applications to receive 500 H shares
0.10%
3,500
350
3 out of 350 applications to receive 500 H shares
0.12%
4,000
385
3 out of 385 applications to receive 500 H shares
0.10%
4,500
281
3 out of 281 applications to receive 500 H shares
0.12%
5,000
6,260
56 out of 6,260 applications to receive 500 H shares
0.09%
7,500
1,129
15 out of 1,129 applications to receive 500 H shares
0.09%
10,000
1,369
25 out of 1,369 applications to receive 500 H shares
0.09%
12,500
589
13 out of 589 applications to receive 500 H shares
0.09%
15,000
421
11 out of 421 applications to receive 500 H shares
0.09%
17,500
247
8 out of 247 applications to receive 500 H shares
0.09%
20,000
295
11 out of 295 applications to receive 500 H shares
0.09%
22,500
236
10 out of 236 applications to receive 500 H shares
0.09%
25,000
540
24 out of 540 applications to receive 500 H shares
0.09%
30,000
331
18 out of 331 applications to receive 500 H shares
0.09%
35,000
256
16 out of 256 applications to receive 500 H shares
0.09%
40,000
266
19 out of 266 applications to receive 500 H shares
0.09%
45,000
192
16 out of 192 applications to receive 500 H shares
0.09%
50,000
1,289
116 out of 1,289 applications to receive 500 H shares
0.09%
100,000
850
153 out of 850 applications to receive 500 H shares
0.09%
150,000
573
155 out of 573 applications to receive 500 H shares
0.09%
200,000
347
125 out of 347 applications to receive 500 H shares
0.09%
250,000
825
371 out of 825 applications to receive 500 H shares
0.09%
300,000
249
134 out of 249 applications to receive 500 H shares
0.09%
350,000
213
134 out of 213 applications to receive 500 H shares
0.09%
400,000
206
148 out of 206 applications to receive 500 H shares
0.09%
450,000
153
124 out of 153 applications to receive 500 H shares
0.09%
500,000
761
685 out of 761 applications to receive 500 H shares
0.09%
Total
92,476
Total number of Pool A successful applicants: 2,500
8

<<<PAGE 9>>>
Pool B
Number
of H Shares
applied for
Number
of valid
applications
Basis of allocation/ballot
Approximate
percentage
allotted of the
total number
of H Shares
applied for
750,000
1,222
811 out of 1,222 applications to receive 500 H
Shares
0.04%
1,000,000
369
325 out of 369 applications to receive 500 H Shares
0.04%
1,250,000
1,240
500 H Shares plus 124 out of 1,240 applications to
receive an additional 500 H Shares
0.04%
Total
2,831
Total number of Pool B successful applicants: 2,376
As of the date of this announcement, the relevant subscription monies previously deposited
in the designated nominee accounts have been remitted back to the accounts of all HKSCC
participants. Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, the Company has complied with the Listing Rules and guidance
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the
placees or the public (as the case may be) directly or indirectly for each Offer Share
subscribed for or purchased by them was the same as the final Offer Price in addition to any
brokerage, AFRC transaction levy, SFC transaction levy and Stock Exchange trading fee
payable.
9

<<<PAGE 10>>>
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited
and Hong Kong Securities Clearing Company Limited take no responsibility for the
contents of this announcement, make no representation as to its accuracy or completeness
and expressly disclaim any liability whatsoever for any loss howsoever arising from or in
reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or
into the United States (including its territories and possessions, any state of the United
States and the District of Columbia) or any other jurisdiction where such distribution is
prohibited by law. This announcement does not constitute or form a part of any offer to
sell or solicitation of an offer to buy, to purchase or subscribe for securities nor shall
there be any sale of Offer Shares in the United States or in any other jurisdictions in
which such offer or solicitation would be unlawful. The securities mentioned herein have
not been, and will not be, registered under the United States Securities Act or any state
securities law of the United States. The securities may not be offered, sold, pledged, or
transferred within the United States or to, or for the account or benefit of U.S. persons (as
defined in Regulation S) except pursuant to an exemption from, or in a transaction not
subject to, the registration requirements of the U.S. Securities Act and in compliance with
any applicable state securities laws.
This announcement is for information purposes only and does not constitute an invitation
or offer to acquire, purchase or subscribe for securities. This announcement is not a
prospectus. Potential investors should read the Prospectus dated 30 June 2026 issued by
Jiangxi Qiyunshan Food Co., Ltd. for detailed information about the Global Offering
described below before deciding whether or not to invest in the H Shares thereby being
offered.
* Potential investors of the Offer Shares should note that the Sole Sponsor and the Sole
Overall Coordinator (for itself and on behalf of the Hong Kong Underwriters and the
Capital Market Intermediaries) shall be entitled to terminate their obligations under the
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of
the events set out in the section headed ‘‘Underwriting — Underwriting Arrangements and
Expenses — Hong Kong Public Offering — Hong Kong Underwriting Agreement —
Grounds for Termination’’ in the Prospectus at any time prior to 8:00 a.m. (Hong Kong
time) on the Listing Date (which is currently expected to be on 9 July 2026).
10

<<<PAGE 11>>>
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering, the total number of H Shares to be
held by the public is 25,000,000 H Shares, representing 25.00% of the total issued share
capital of the Company, will be counted towards the public float. Therefore, the Company
will be able to meet the public float requirement under Rule 19A.13A(1) of the Listing
Rules.
Rule 19A.13C(1) of the Listing Rules provides that, where a new applicant is a PRC issuer
with no other listed shares at the time of listing, the portion of H shares for which listing is
sought that are held by the public and not subject to any disposal restrictions at the time of
listing must normally (i) represent at least 10% of the total number of issued shares in the
class to which H shares belong at the time of listing (excluding treasury shares), with an
expected market value at the time of listing of not less than HK$50,000,000; or (ii) have an
expected market value at the time of listing of not less than HK$600,000,000.
Immediately after the completion of the Global Offering, based on the Offer Price of
HK$8.00, except for (i) 75,000,000 Shares held by all existing Shareholders that are subject
to a lock-up period of twelve months following the Listing Date under applicable PRC law,
all remaining 25,000,000 Shares, representing 25.00% of the total Shares, will be counted
toward the free float. Therefore, the Company will be able to satisfy the free float
requirement under Rule 19A.13C(1)(a) of the Listing Rules.
The Directors confirm that immediately following the completion of the Global Offering, (i)
no placee will, individually, be placed more than 10% of the enlarged issued share capital of
the Company immediately after the Global Offering; (ii) there will not be any new
substantial Shareholder immediately after the Global Offering; (iii) the three largest public
shareholders of the Company do not hold more than 50% of the H Shares in public hands at
the time of the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and
(iv) there will be at least 300 Shareholders at the time of the Listing in compliance with
Rule 8.08(2) of the Listing Rules.
11

<<<PAGE 12>>>
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Thursday, 9
July 2026 (Hong Kong time), provided that the Global Offering has become unconditional
and the right of termination described in the section headed ‘‘Underwriting — Underwriting
Arrangements and Expenses — Hong Kong Public Offering — Hong Kong Underwriting
Agreement — Grounds for Termination’’ in the Prospectus has not been exercised. Investors
who trade the H Shares on the basis of publicly available allocation details prior to the
receipt of H Share certificates or prior to the H Share certificates becoming valid evidence
of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on
Thursday, 9 July 2026 (Hong Kong time), it is expected that dealings in the H Shares on the
Stock Exchange will commence at 9:00 a.m. on Thursday, 9 July 2026 (Hong Kong time).
The H Shares will be traded in board lots of 500 H Shares each, and the stock code of the
H Shares will be 2797.
By order of the Board
Jiangxi Qiyunshan Food Co., Ltd.
Mr. Liu Zhigao
Chairman of the Board and Executive Director
Hong Kong, 8 July 2026
As at the date of this announcement, the Board comprises: (i) Mr. Liu Zhigao (Chairman),
Mr. Zhu Fangyong, Mr. Liu Jiyan, Ms. Yang Yulan, Mr. Huang Zhongming and Mr. Ling
Huashan as executive Directors; (ii) Mr. Wong Tsz Lun, Dr. Dai Taotao and Mr. Wong Sai
Hung as the independent non-executive Directors.
12
