# 配发结果公告抽取任务：2723.HK Beijing DeepZero Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**26/05/2026 22:49**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0526/2026052602298.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2723.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities 
in the United States or in any other jurisdictions. The securities mentioned herein have not been, and will not be, 
registered under the United States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or 
securities law of any state or other jurisdiction of the United States. The securities may not be offered, sold, pledged 
or otherwise transferred within the United States except pursuant to an exemption from the registration requirements 
of the U.S. Securities Act and in compliance with any applicable state securities laws. The securities are being offered 
and sold outside the United States in offshore transactions in accordance with Regulation S under the U.S. Securities 
Act. There will be no public offer of securities in the United States.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
May 18, 2026 (the “Prospectus”) issued by Beijing DeepZero Technology Co., Ltd. (北京深演智能科技股份有限公
司) (the “Company”) for detailed information about the Global Offering described below before deciding whether or 
not to invest in the H Shares thereby being offered. Any investment decision in relation to the Offer Shares should be 
taken solely in reliance on the information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinator (for itself and on behalf 
of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting – 
Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus 
at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Wednesday, 
May 27, 2026).

<<<PAGE 2>>>
2
Beijing DeepZero Technology Co., Ltd.
北京深演智能科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the Global
Offering
:
9,068,000 H Shares
Number of Hong Kong Offer Shares
:
906,800 H Shares
Number of International Offer Shares
:
8,161,200 H Shares
Final Offer Price
:
HK$55.50 per H Share, plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
Stock Exchange trading fee of 0.00565% and  
AFRC transaction levy of 0.00015%
Nominal Value
:
RMB1.00 per H Share
Stock Code
:
2723
Sole Sponsor, Sponsor-Overall Coordinator, Joint Global Coordinator,
Joint Bookrunner and Joint Lead Manager
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
Beijing DeepZero Technology Co., Ltd. 
北京深演智能科技股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated May 18, 2026 (the “Prospectus”) issued by 
Beijing DeepZero Technology Co., Ltd. (北京深演智能科技股份有限公司) (the “Company”).
SUMMARY
Company information
Stock code
2723
Stock short name
DEEPZERO
Dealings commencement date
May 27, 2026*
* see note at the end of the announcement
Price Information
Final Offer Price
HK$55.50
Offer Price Range
HK$43.50 - HK$55.50
Offer Shares and Share Capital
Number of Offer Shares
9,068,000
Number of Offer Shares in Hong Kong Public Offering
906,800
Number of Offer Shares in International Offering
8,161,200
Number of issued Shares upon Listing
90,679,175
Proceeds
Gross proceeds (Note)
HK$503.3 million
 Less: Estimated listing expenses payable based on Offer Price
HK$(38.2) million
Net proceeds
HK$465.1 million
Note: Gross proceeds refers to the amount to which the issuer is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.

<<<PAGE 4>>>
4
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
232,456
Number of successful applications
9,068
Subscription level
5,480.23 times
Number of Offer Shares initially available under the Hong Kong Public 
Offering
906,800
Final number of Offer Shares under the Hong Kong Public Offering
906,800
Reallocation
No
% of final number of Offer Shares under the Hong Kong Public Offering 
to the Global Offering
10.00%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can refer to 
www.eipo.com.hk/eIPOAllotment to perform a search by identification number or www.eipo.com.hk/eIPOAllotment 
for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
78
Subscription Level
3.41 times
No. of Offer Shares initially available under the International Offering
8,161,200
Final no. of Offer Shares under the International Offering
8,161,200
% of final number of Offer Shares under the International Offering to 
the Global Offering
90.00%
The Directors confirm that, to the best of their knowledge, information and belief, save for a 
consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide to permit 
the Company to allocate certain Offer Shares in the International Offering to a connected client, 
(i) none of the Offer Shares subscribed by the placees and the public have been financed directly 
or indirectly by the Company, any of the Directors, chief executive of the Company, Controlling 
Shareholders, substantial shareholders, existing shareholders of the Company or any of its 
subsidiaries or their respective close associates; and (ii) none of the placees and the public who 
have purchased the Offer Shares are accustomed to taking instructions from the Company, any of 
the Directors, chief executive of the Company, Controlling Shareholders, substantial shareholders, 
existing shareholders of the Company or any of its subsidiaries or their respective close associates 
in relation to the acquisition, disposal, voting or other disposition of Shares registered in his/her/its 
name or otherwise held by him/her/it.

<<<PAGE 5>>>
5
The placees in the International Offering include the following:
Allottee with waivers/consents obtained
Investor
No. of Offer 
Shares 
allocated
% of total 
Offer Share
% of total 
issued 
Shares after 
the Global 
Offering
Relationship
Allotee with consent under paragraph 1C(1) of the Appendix F1 to the Listing Rules (the 
“Placing Guidelines”) and Chapter 4.15 of the Guide in relation to allocation to connected 
client (Note)
CITIC Securities 
International Capital 
Management Limited 
(“CSICM”)
39,200
0.40%
0.00%
Connected client
Note: For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide in 
relation to allocation to connected client, please refer to the section headed “Others/Additional Information – Placing 
to connected client with a prior consent under paragraph 1C(1) of the Placing Guidelines” in this announcement.
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of H 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
% of total 
issued Shares 
in the Company 
subject to lock-up 
undertakings upon 
Listing
Last day subject 
to the lock-up 
undertakings (Note)
Huang Xiaonan
17,102,230
18.86%
May 26, 2027
Xie Peng
12,051,502
13.29%
May 26, 2027
Total
29,153,732
32.15%
Note:
1. 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. The 
required lock-up for the Controlling Shareholders ends on May 26, 2027, being one year following the Listing 
Date. Pursuant to Rule 10.07 of the Listing Rules, each of the Controlling Shareholders has undertaken to the 
Stock Exchange and the Company that, he or she shall comply with the applicable lock-up requirements. For 
further details, please refer to the section headed “Underwriting – Undertakings to the Stock Exchange Pursuant 
to the Listing Rules – Undertakings by our Controlling Shareholders” in the Prospectus.

<<<PAGE 6>>>
6
2. 
Pursuant to an acting-in-concert agreement dated July 13, 2016, entered into between Ms. Huang Xiaonan 
and Mr. Xie Peng (each a “Concert Party” and collectively, the “Concert Parties”), they have agreed to to, 
for so long as they are Shareholders of our Company, communicate thoroughly to reach a consensus as to 
how to exercise their voting rights in our Company and act in concert by aligning their votes at the relevant 
shareholders’ meetings. In the event that they could not reach a consensus as to how to exercise their voting 
rights, Mr. Xie agreed to follow the directions of Ms. Huang. (the “AIC Agreement”).
As a result of the AIC Agreement, immediately after the completion of the Global Offering, the Concert Parties 
will be collectively entitled to exercise control over approximately 32.15% of the voting rights in our Company, 
and therefore will remain as a group of Controlling Shareholders of our Company.
For details of the background of the Controlling Shareholders, please refer to the section headed “Relationship 
with our Controlling Shareholders – Our Controlling Shareholders” in the Prospectus.
Other existing Shareholders (including the Pre-IPO Investors as defined in the “History, 
Development and Corporate Structure” section of the Prospectus)
Name
Number of H 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued Shares 
after the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing
Last day 
subject to 
the lock-up 
undertakings 
(Note)
Beijing Heyin Investment Center 
(Limited Partnership) (北京合音投資
中心(有限合夥))
11,455,282
12.63%
May 26, 2027
China Mobile Innovative Business 
Fund (Shenzhen) Partnership (Limited 
Partnership) (中移創新產業基金(深
圳)合夥企業(有限合夥))
8,911,265
9.83%
May 26, 2027
Shanghai Forward Maoshang 
Investment Partnership (Limited 
Partnership) (上海富德懋賞投資合夥
企業(有限合夥))
8,372,938
9.23%
May 26, 2027
Shanghai Maoyao Investment 
Partnership (Limited Partnership) (上
海懋耀投資合夥企業(有限合夥))
7,405,007
8.17%
May 26, 2027
Shen Xuehua (沈學華)
3,536,423
3.90%
May 26, 2027

<<<PAGE 7>>>
7
Name
Number of H 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued Shares 
after the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing
Last day 
subject to 
the lock-up 
undertakings 
(Note)
Beijing BGWG Venture Capital Center 
(Limited Partnership) (北京市北廣文
資歌華創業投資中心(有限合夥))
2,817,549
3.11%
May 26, 2027
Beihai Qidian Yihao Venture Capital 
Partnership (Limited Partnership) (北
海起點壹號創業投資合夥企業(有限
合夥))
2,650,177
2.92%
May 26, 2027
Shanghai Zhencheng Investment 
Center (Limited Partnership) (上海振
誠投資中心(有限合夥))
2,253,889
2.49%
May 26, 2027
Huang Jicheng (黃繼承)
1,717,370
1.89%
May 26, 2027
Liu Chunru (劉春茹)
1,054,018
1.16%
May 26, 2027
Hongtu Chengzhang Venture Capital 
Co., Ltd. (紅土成長創業投資有限公
司)
918,018
1.01%
May 26, 2027
Shenzhen Capital Group Co., Ltd. (深
圳市創新投資集團有限公司)
918,018
1.01%
May 26, 2027
Zhang Wei (張煒)
263,504
0.29%
May 26, 2027
Qu Zhe (瞿哲)
183,985
0.20%
May 26, 2027
Total
52,457,443
57.85%
Note: The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. The 
required lock-up for all existing Shareholders ends on May 26, 2027, being one year following the Listing Date.

<<<PAGE 8>>>
8
PLACEE CONCENTRATION ANALYSIS
Placees(Note)
Number of 
H Shares 
Allocated
Allotment as 
to % of the 
International 
Offering
Allotment as to 
% of the total 
Offer Shares
Number of H 
Shares held 
upon Listing
Number of H Shares 
held upon Listing as 
% of total issued share 
capital upon Listing
Top 1
1,361,700
16.69%
15.02%
1,361,700
1.50%
Top 5
3,555,300
43.56%
39.21%
3,555,300
3.92%
Top 10
5,392,300
66.07%
59.47%
5,392,300
5.95%
Top 25
7,471,100
91.54%
82.39%
7,471,100
8.24%
Note: Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders(Note 1)
Number of 
H Shares 
Allocated
Allotment as 
to % of the 
International 
Offering
Allotment as to 
% of the total 
Offer Shares
Number of H 
Shares Held 
Upon Listing
Number of 
H Shares 
held upon 
Listing as % 
of total issued 
H share capital 
upon Listing
Number of 
Shares held 
upon Listing 
Top 1(Note 2)
0
0.00%
0.00%
29,153,732
32.15%
29,153,732
Top 5
0
0.00%
0.00%
71,915,700
79.31%
71,915,700
Top 10
1,361,700
16.69%
15.02%
81,734,872
90.14%
81,734,872
Top 25
6,373,000
78.09%
70.28%
87,800,190
96.83%
87,800,190
Notes: 
1. 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
2. 
Refers to the group of Controlling Shareholders. Please see lock-up undertakings of the Controlling Shareholders 
above for details.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders(note 1)
Number of 
H Shares 
Allocated
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
Number 
of Shares 
held upon 
Listing
% of total 
issued share 
capital upon 
Listing
Top 1(Note 2)
0
0.00%
0.00%
29,153,732
29,153,732
32.15%
Top 5
0
0.00%
0.00%
71,915,700
71,915,700
79.31%
Top 10
1,361,700
16.69%
15.02%
81,734,872
81,734,872
90.14%
Top 25
6,373,000
78.09%
70.28%
87,800,190
87,800,190
96.83%
Notes:
1. 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
2. 
Refers to the group of Controlling Shareholders. Please see lock-up undertakings of the Controlling Shareholders.

<<<PAGE 9>>>
9
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
NO. OF H 
SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL NO. OF 
H SHARES 
APPLIED FOR
POOL A
100
98,305
983 out of 98,305 to receive 100 H Shares
1.00%
200
12,852
131 out of 12,852 to receive 100 H Shares
0.51%
300
7,255
75 out of 7,255 to receive 100 H Shares
0.34%
400
4,562
48 out of 4,562 to receive 100 H Shares
0.26%
500
5,238
56 out of 5,238 to receive 100 H Shares
0.21%
600
2,968
32 out of 2,968 to receive 100 H Shares
0.18%
700
1,790
20 out of 1,790 to receive 100 H Shares
0.16%
800
10,104
113 out of 10,104 to receive 100 H Shares
0.14%
900
2,022
23 out of 2,022 to receive 100 H Shares
0.13%
1,000
10,499
121 out of 10,499 to receive 100 H Shares
0.12%
1,500
5,702
71 out of 5,702 to receive 100 H Shares
0.08%
2,000
4,404
59 out of 4,404 to receive 100 H Shares
0.07%
2,500
2,278
32 out of 2,278 to receive 100 H Shares
0.06%
3,000
2,631
40 out of 2,631 to receive 100 H Shares
0.05%
3,500
1,773
28 out of 1,773 to receive 100 H Shares
0.05%
4,000
1,751
29 out of 1,751 to receive 100 H Shares
0.04%
4,500
1,108
20 out of 1,108 to receive 100 H Shares
0.04%
5,000
2,662
49 out of 2,662 to receive 100 H Shares
0.04%
6,000
1,825
37 out of 1,825 to receive 100 H Shares
0.03%
7,000
1,394
31 out of 1,394 to receive 100 H Shares
0.03%
8,000
1,411
33 out of 1,411 to receive 100 H Shares
0.03%
9,000
1,267
32 out of 1,267 to receive 100 H Shares
0.03%
10,000
5,202
141 out of 5,202 to receive 100 H Shares
0.03%
15,000
3,445
123 out of 3,445 to receive 100 H Shares
0.02%
20,000
3,400
151 out of 3,400 to receive 100 H Shares
0.02%
25,000
2,146
114 out of 2,146 to receive 100 H Shares
0.02%
30,000
2,176
135 out of 2,176 to receive 100 H Shares
0.02%
35,000
1,645
116 out of 1,645 to receive 100 H Shares
0.02%
40,000
1,462
116 out of 1,462 to receive 100 H Shares
0.02%
45,000
994
87 out of 994 to receive 100 H Shares
0.02%
50,000
2,308
223 out of 2,308 to receive 100 H Shares
0.02%
60,000
1,685
192 out of 1,685 to receive 100 H Shares
0.02%
70,000
1,366
179 out of 1,366 to receive 100 H Shares
0.02%
80,000
1,603
238 out of 1,603 to receive 100 H Shares
0.02%
90,000
3,953
656 out of 3,953 to receive 100 H Shares
0.02%
Total
215,186
Total number of Pool A successful applicants: 4,534

<<<PAGE 10>>>
10
NO. OF H 
SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL NO. OF 
H SHARES 
APPLIED FOR
POOL B
100,000
8,071
1,957 out of 8,071 to receive 100 H Shares
0.02%
150,000
2,180
549 out of 2,180 to receive 100 H Shares
0.02%
200,000
1,492
390 out of 1,492 to receive 100 H Shares
0.01%
250,000
847
229 out of 847 to receive 100 H Shares
0.01%
300,000
758
212 out of 758 to receive 100 H Shares
0.01%
350,000
500
145 out of 500 to receive 100 H Shares
0.01%
400,000
460
137 out of 460 to receive 100 H Shares
0.01%
453,400
2,962
915 out of 2,962 to receive 100 H Shares
0.01%
17,270
Total number of Pool B successful applicants: 4,534
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the H Shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or 
indirectly, provided by the Company, its Controlling Shareholders, Directors or syndicate members 
to any placees or the public (as the case may be) and the consideration payable by them directly or 
indirectly for each Offer Share subscribed for or purchased by them is the same as the Offer Price 
in addition to any brokerage, AFRC transaction levy, SFC transaction levy and Stock Exchange 
trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Placing to connected client with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
The Company has applied to the Stock Exchange, and the Stock Exchange has granted, a consent 
under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate certain Offer 
Shares in the International Offering to a connected client. The allocation of Offer Shares to such 
connected client is in compliance with all the conditions under the consent granted by the Stock 
Exchange.

<<<PAGE 11>>>
11
Details of the placement to the connected client are set out below:
Connected 
distributor
Connected client
Relationship 
between connected 
distributor and 
connected client
Basis of holding 
securities
No. of Offer 
Shares 
subscribed
% to total 
Offer Shares 
under Global 
Offering
% to total 
issued Shares 
immediately 
upon completion 
of the Global 
Offering (Note 1)
CITIC Securities 
Brokerage (HK) 
Limited (“CITIC 
Brokerage”)
CITIC Securities 
International Capital 
Management 
Limited (“CSICM”)
CSICM is a member 
of the same group 
of companies as 
CITIC Brokerage
Non-discretionary
39,200
0.40%
0.00%
Note: CSICM will act as the single counterparty of a back-to-back total return swap transaction (the “CSICM Back-
to-back TRS”) to be entered into by CSICM in connection with a total return swap order (the “CSICM Client 
TRS”) placed by its ultimate client (the “CSICM Ultimate Client”), by which CSICM will pass the full 
economic exposure of the Offer Shares placed to CSICM to the CSICM Ultimate Client. CSICM will hold the 
beneficial interest of the Offer Shares on behalf of the CSICM Ultimate Client on a non-discretionary basis. 
The CSICM Ultimate Client may exercise an early termination right to early terminate the CSICM Client TRS 
at any time from the trade date of the CSICM Client TRS which should be on or after the date on which the 
Offer Shares are listed on the Stock Exchange. Upon the final maturity or termination of the CSICM Client 
TRS by the CSICM Ultimate Client, CSICM will dispose of the Offer Shares on the secondary market and the 
CSICM Ultimate Client will receive a final termination amount of the CSICM Back-to-back TRS which should 
have taken into account all the economic returns or economic loss in relation to the Offer Shares and the fixed 
amount of transaction fees of the CSICM Back-to-back TRS and the CSICM Client TRS. CSICM will not 
exercise the voting right of the Offer Shares during the terms of the CSICM Back-to-back TRS.
The CSICM Ultimate Client is Ningyong Fuchun No. 9 Private Equity Investment Fund (甯湧富春分9號私募證
券投資基金) (the “CSICM Ultimate Client”). The general partner of the CSICM Ultimate Client is Shanghai 
Ningyongfu Private Equity Fund Management Partnership (Limited Partnership) (上海甯湧富私募基金管理合
夥企業(有限合夥)) which is in turn held as to more than 30% by Mr. Weng Qiang (翁強). The limited partner 
holding 30% or more interest in the CSICM Ultimate Client is Lu Xuyang (陸徐楊)
CSICM has confirmed that, to the best of their knowledge, (i) each of the CSICM Ultimate Client and the 
ultimate beneficial owners holding 30% or more interest of the CSICM Ultimate Client listed above is an 
independent third party of (a) the Company, its subsidiaries, the connected persons or the associates thereof; and 
(b) CSICM, CITIC Brokerage and the companies which are members of the same group of companies as CITIC 
Brokerage.

<<<PAGE 12>>>
12
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the 
“Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy 
or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. Potential investors should read the Prospectus 
for detailed information about the Company and the Global Offering described below before 
deciding whether or not to invest in the Offer Shares.
This announcement is not for release, publication or distribution, directly or indirectly, in or 
into the United States (including its territories and possessions, any state of the United States 
and the District of Columbia). This announcement does not constitute or form a part of any 
offer or solicitation to purchase or subscribe for securities in the United States or in any other 
jurisdiction. The Offer Shares have not been and will not be registered under the United States 
Securities Act of 1933, as amended from time to time (the “U.S. Securities Act”) or securities 
law of any state or other jurisdiction of the United States and may not be offered, sold, pledged 
or transferred within the United States, except in transactions exempt from, or not subject to, the 
registration requirements of the U.S. Securities Act. There will be no public offer of the Offer 
Shares in the United States. The Offer Shares are being offered and sold outside the United 
States in offshore transactions in reliance on Regulation S under the U.S. Securities Act.
* Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinator (for itself and on behalf 
of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date.
PUBLIC FLOAT AND FREE FLOAT
As all of the Company’s Unlisted Shares will be converted into H Shares, immediately upon 
completion of the Global Offering and the Conversion of Unlisted Shares into H Shares, the 
Company will have 90,679,175 H Shares. Upon completion of the Global Offering and the 
Conversion of Unlisted Shares into H Shares, 63,004,435 H Shares (representing approximately 
69.48% of the total issued Shares upon Listing) to be converted from the Unlisted Shares are held 
by core connected persons of the Group and would not be considered as part of the public float. As 
a result of the foregoing, upon completion of the Global Offering and the Conversion of Unlisted 
Shares into H Shares, an aggregate of 27,674,740 H Shares, representing approximately 30.52% 
of the total issued share capital of the Company would be counted towards the public float upon 
Listing, which is higher than the prescribed percentage of H Shares required to be held in public 
hands of 25% under Rule 19A.13A(1) of the Listing Rules.
To the best knowledge of the Directors, the 9,068,000 H Shares to be issued pursuant to the Global 
Offering are expected to be held by the public and will not be subject to any disposal restrictions 
(whether under contract, the Listing Rules, applicable laws or otherwise). Based on the final Offer 
Price of HK$55.50 per H Share, the Company will satisfy the free float requirements under Rule 
19A.13C(1)(a) of the Listing Rules.

<<<PAGE 13>>>
13
The Directors confirm that, immediately following the completion of the Global Offering: (i) no 
placee will, individually, be placed more than 10% of the enlarged issued share capital of the 
Company; (ii) there will not be any new substantial Shareholder (as defined in the Listing Rules) 
of the Company; (iii) the three largest public shareholders of the Company do not hold more than 
50% of the H Shares in public hands at the time of the Listing in compliance with Rules 8.08(3) 
and 8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at the time of the 
Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, May 
27, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting – Underwriting Arrangements 
and Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade the H Shares on the basis of publicly available allocation 
details prior to the receipt of H Share certificates or prior to the H Share certificates becoming 
valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Wednesday, 
May 27, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Wednesday, May 27, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 100 H Shares each, and the stock code of the H Shares will 
be 2723.
By order of the Board
Beijing DeepZero Technology Co., Ltd.
Ms. HUANG Xiaonan
Chairwoman of the Board and executive Director
Hong Kong, May 26, 2026
As of the date of this announcement, the Board comprises: (i) Ms. Huang Xiaonan, Mr. Xie Peng 
and Mr. Yang Zhuo as executive Directors; (ii) Ms. Tian Tian, Mr. Huang Haibo and Mr. Huang 
Hao as non-executive Directors; and (iii) Ms. Li Juan, Mr. Xue Yansong and Mr. Guo Bing as 
independent non-executive Directors.
