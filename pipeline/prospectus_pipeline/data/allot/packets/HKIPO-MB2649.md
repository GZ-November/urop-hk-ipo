# 配发结果公告抽取任务：2649.HK ALSCO Pooling Service Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**06/03/2026 21:28**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0306/2026030601405.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2649.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
February 27, 2026 (the “Prospectus”) issued by ALSCO Pooling Service Co., Ltd. (蘇州優樂賽共享服務股份有限
公司) (the “Company”) for detailed information about the Global Offering described below before deciding whether 
or not to invest in the H Shares thereby being offered. Any investment decision in relation to the Offer Shares should 
be taken solely in reliance on the information in the Prospectus. The Company has not been and will not be registered 
under the U.S. Investment Company Act of 1940, as amended.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinators (for themselves and 
on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” 
in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to 
be on Monday, March 9, 2026).

<<<PAGE 2>>>
2
蘇州優樂賽共享服務股份有限公司
ALSCO Pooling Service Co., Ltd.
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
20,336,000 H Shares
Number of Hong Kong Offer Shares
:
2,034,000 H Shares
Number of International Offer Shares
:
18,302,000 H Shares
Final Offer Price
:
HK$11.0 per H Share, plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
Hong Kong Stock Exchange trading fee of 
0.00565% and AFRC transaction levy of 
0.00015%
Nominal value
:
RMB1.00 per H Share
Stock code
:
2649
Sole Sponsor, Overall Coordinator, Joint Global Coordinator, Joint Bookrunner
and Joint Lead Manager
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner, Joint Lead Manager
and Financial Adviser
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers
(in alphabetical order)

<<<PAGE 3>>>
3
ALSCO Pooling Service Co., Ltd.
蘇州優樂賽共享服務股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated February 27, 2026 (the “Prospectus”) issued by 
ALSCO Pooling Service Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of H 
Shareholders, H Shareholders and prospective investors should be aware that the price of 
the H Shares could move substantially even with a small number of H Shares traded and 
should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
2649
Stock short name
ALSCO POOLING
Dealings commencement date
March 9, 2026*
* see note at the end of the announcement
Price Information
Final Offer Price
HK$11.00
Offer Price Range
HK$11.00 – HK$14.00
Offer Price Adjustment exercised
No
Offer Shares and Share Capital
Number of Offer Shares
20,336,000
Number of Offer Shares in Hong Kong Public Offering
2,034,000
Number of Offer Shares in International Offering
18,302,000
Number of issued Shares upon Listing
90,336,000

<<<PAGE 4>>>
4
Proceeds
Gross proceeds (Note)
HK$223.70 million
Less: Estimated listing expenses payable based on final 
Offer Price
HK$(48.18) million
Net proceeds
HK$175.52 million
Note: Gross proceeds refer to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
162,571
No. of successful applications
4,068
Subscription level
5,297.23 times
Claw-back triggered
No
No. of Offer Shares initially available under the Hong Kong Public 
Offering
2,034,000
Final no. of Offer Shares under the Hong Kong Public Offering
2,034,000
% of Offer Shares under the Hong Kong Public Offering to the Global 
Offering
10%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.eipo.com.hk/eIPOAllotment to perform a search by name or identification number or www.eipo.com.hk/eIPOAllotment 
for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
162
Subscription level
4.20 times
No. of Offer Shares initially available under the International Offering
18,302,000
Final no. of Offer Shares under the International Offering
18,302,000
% of Offer Shares under the International Offering to the Global 
Offering
90%

<<<PAGE 5>>>
5
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, Supervisors, chief executive of the Company, Controlling 
Shareholders, substantial Shareholders, existing Shareholders of the Company or any of its 
subsidiaries or their respective close associates; and (ii) none of the placees and the public who 
have purchased the Offer Shares are accustomed to taking instructions from the Company, any of 
the Directors, Supervisors, chief executive of the Company, Controlling Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates in relation to the acquisition, disposal, voting or other disposition of H Shares 
registered in his/her/its name or otherwise held by him/her/it.
Furthermore, the Directors confirm that, to the best of their knowledge, no rebate has been, directly 
or indirectly, provided by the Company, the Controlling Shareholders, Directors or syndicate 
members to any placees or the public (as the case may be) and the consideration payable by them 
for each Offer Share subscribed for or purchased by them is the same as the final Offer Price 
determined by the Company, in addition to any brokerage, AFRC transaction levy, SFC transaction 
levy and Stock Exchange trading fee payable. There is also no side agreement or arrangement 
between the Company or any of its subsidiaries, their directors, chief executive, its Controlling 
Shareholders, substantial shareholders, existing Shareholders, or any of their respective close 
associates, on one hand, and the public subscribers or the placees who have subscribed for the 
Offer Shares, on the other hand. The International Offering is in compliance with Appendix F1 to 
the Listing Rules (the “Placing Guidelines”).
The placees in the International Offer include the following:

<<<PAGE 6>>>
6
Allotees with Waivers/Consents Obtained
Investor
No. of  
Offer Shares  
allocated
% of Offer  
Shares
% of total  
issued share  
capital after  
the Global  
Offering
Relationship
Allottees with consent under paragraph 5(1) of the Placing Guidelines in relation to subscription of 
shares by connected clients (Note 1)
Bosera Asset Management 
(International) Co., Limited
175,000
0.86%
0.19%
Connected client
CHINA ASSET 
MANAGEMENT (HONG 
KONG) LIMITED
175,000
0.86%
0.19%
Connected client
Value Partners Limited and 
Value Partners Hong Kong 
Limited
213,000
1.05%
0.24%
Connected client
Note:
1. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate certain 
Offer Shares in the International Offering to connected clients, please refer to the section headed “Other Information” in 
this announcement.

<<<PAGE 7>>>
7
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of  
Shares held  
in the Company  
subject to lock-up  
undertakings  
upon Listing
H Shares as %  
of total issued  
H Shares after  
the Global  
Offering subject  
to lock-up  
undertakings  
upon Listing
% of total  
issued share  
capital in the  
Company  
subject to  
lock-up  
undertakings 
upon Listing
Last day  
subject to  
the lock-up  
undertakings Note
Mr. Sun Yan’an
36,093,750 H Shares
41.18%
39.96%
March 9, 2027
Suzhou Anhua Investment  
Co., Ltd.
3,318,924 H Shares
3.79%
3.67%
March 9, 2027
Total
39,412,674 H Shares
44.96%
43.63%
Note: Under the applicable PRC laws, all existing Shareholders are subject to a lock-up period of twelve months 
following the Listing Date. The lock-up requirement under the applicable PRC laws is longer than the lock-up 
period required of Controlling Shareholders under Rule 10.07 of the Listing Rules.

<<<PAGE 8>>>
8
Pre-IPO Investors (as defined in the “History and Corporate Structure” section of the 
Prospectus)
Name
Number of  
Shares held  
in the Company  
subject to lock-up  
undertakings  
upon Listing
H Shares as %  
of total issued  
H Shares after  
the Global 
Offering subject  
to lock-up  
undertakings  
upon Listing
% of total  
issued share  
capital in the  
Company  
subject to  
lock-up 
undertakings  
upon Listing
Last day  
subject to  
the lock-up  
undertakings Note
Suzhou International  
Development Emerging  
Industry Venture  
Investment Enterprise  
(Limited Partnership)
3,645,833 H Shares
4.16%
4.04%
March 9, 2027
Suzhou Industrial Park  
Yuandian Zhengze No. 2  
Venture Capital Partnership  
(Limited Partnership)
2,604,163 H Shares
2.97%
2.88%
March 9, 2027
Suqian International  
Development Venture  
Capital Enterprise  
(Limited Partnership)
1,822,917 H Shares
2.08%
2.02%
March 9, 2027
Suzhou International  
Development Union Equity  
Investment Enterprise  
(Limited Partnership)
1,822,917 H Shares
2.08%
2.02%
March 9, 2027
Changzhou Shuguang  
Enterprise Management  
Consulting Partnership  
(Limited Partnership)
607,639 H Shares
0.69%
0.67%
March 9, 2027
Shanghai Qianjin Industrial  
Co., Ltd.
2,682,295 Shares
–
2.97%
March 9, 2027
Hangzhou Jintou Zhihe  
Venture Capital Partnership  
(Limited Partnership)
1,312,500 H Shares
1.50%
1.45%
March 9, 2027

<<<PAGE 9>>>
9
Name
Number of  
Shares held  
in the Company  
subject to lock-up  
undertakings  
upon Listing
H Shares as %  
of total issued  
H Shares after  
the Global 
Offering subject  
to lock-up  
undertakings  
upon Listing
% of total  
issued share  
capital in the  
Company  
subject to  
lock-up 
undertakings  
upon Listing
Last day  
subject to  
the lock-up  
undertakings Note
Fang Dianjun
492,188 H Shares
0.56%
0.54%
March 9, 2027
Yancheng Fusion Base  
Emerging Industry Fund  
(Limited Partnership)
1,750,000 H Shares
2.00%
1.94%
March 9, 2027
Suzhou Industrial Park  
Industry Investment Fund  
(Limited Partnership)
1,312,500 H Shares
1.50%
1.45%
March 9, 2027
Suzhou Shihu Minsheng  
Equity Investment 
Partnership  
(Limited Partnership)
875,000 H Shares
1.00%
0.97%
March 9, 2027
Suzhou Industrial Park Science  
and Technology Innovation  
Investment Partnership  
(Limited Partnership)
437,500 H Shares
0.50%
0.48%
March 9, 2027
Yu Yue
328,125 H Shares
0.37%
0.36%
March 9, 2027
Note: Under the applicable PRC laws, all existing Shareholders (including Pre-IPO Investors) are subject to a 
lockup period of twelve months following the Listing Date.

<<<PAGE 10>>>
10
Other Existing Shareholders
Name
Number of  
Shares held  
in the Company  
subject to lock-up  
undertakings  
upon Listing
H Shares as %  
of total issued  
H Shares after  
the Global  
Offering subject 
to lock-up  
undertakings  
upon Listing
% of total  
issued share  
capital in the  
Company 
subject to  
lock-up  
undertakings  
upon Listing
Last day  
subject to  
the lock-up  
undertakings Note 1
Wang Yue
4,921,875 H Shares
5.62%
5.45%
March 9, 2027
Zhu Zhizhou
2,460,937 H Shares
2.81%
2.72%
March 9, 2027
Sun Wenhong
2,460,937 H Shares
2.81%
2.72%
March 9, 2027
Suzhou Sailing Enterprise 
Management Partnership 
(Limited Partnership)
1,050,000 H Shares
1.20%
1.16%
March 9, 2027
Note: Under the applicable PRC laws, all existing Shareholders are subject to a lockup period of twelve months 
following the Listing Date.
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
H Shares 
allotted
Allotment 
as % of the 
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
3,600,000
19.67%
17.70%
3,600,000
3.99%
Top 5
7,227,000
39.49%
35.54%
7,227,000
8.00%
Top 10
10,588,500
57.85%
52.07%
10,588,500
11.72%
Top 25
15,332,000
83.77%
77.39%
15,332,000
16.97%
Notes:
* Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 11>>>
11
H SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholder*
Number of 
H Shares 
allotted
Allotment 
as % of the 
International 
Offering
Allotment  
as % of total 
Offer Shares
Number of  
H Shares 
held upon 
Listing
% of total 
issued  
H Shares 
capital upon 
Listing
Number of
Shares
held upon
Listing
Top 1
0
0.00%
0.00%
39,412,674
44.96%
39,412,674
Top 5
3,600,000
19.67%
17.70%
65,716,316
74.97%
65,716,316
Top 10
6,327,000
34.57%
31.11%
72,216,753
82.39%
72,216,753
Top 25
13,444,000
73.46%
66.11%
80,433,580
91.76%
80,433,580
Notes:
* Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholder*
Number of 
H Shares 
allotted
Allotment 
as % of the 
International 
Offering
Allotment  
as % of total 
Offer Shares
Number of  
H Shares 
held upon 
Listing
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
39,412,674
39,412,674
43.63%
Top 5
3,600,000
19.67%
17.70%
63,255,379
65,937,674
72.99%
Top 10
5,418,000
29.60%
26.64%
71,307,753
73,990,048
81.91%
Top 25
13,089,000
71.52%
64.36%
80,078,580
82,760,875
91.61%
Notes:
* Ranking of Shareholders is based on the number of Shares held by the Shareholders upon Listing.

<<<PAGE 12>>>
12
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
NO. OF  
H SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL NO. 
OF H SHARES 
APPLIED FOR
POOL A
500
91,248
34 out of 91,248 to receive 500 Shares
0.04%
1,000
8,071
6 out of 8,071 to receive 500 Shares
0.04%
1,500
4,772
6 out of 4,772 to receive 500 Shares
0.04%
2,000
3,056
5 out of 3,056 to receive 500 Shares
0.04%
2,500
2,617
5 out of 2,617 to receive 500 Shares
0.04%
3,000
1,845
4 out of 1,845 to receive 500 Shares
0.04%
3,500
3,518
9 out of 3,518 to receive 500 Shares
0.04%
4,000
1,754
5 out of 1,754 to receive 500 Shares
0.04%
4,500
916
3 out of 916 to receive 500 Shares
0.04%
5,000
4,197
16 out of 4,197 to receive 500 Shares
0.04%
6,000
1,076
5 out of 1,076 to receive 500 Shares
0.04%
7,000
1,730
9 out of 1,730 to receive 500 Shares
0.04%
8,000
986
6 out of 986 to receive 500 Shares
0.04%
9,000
636
5 out of 636 to receive 500 Shares
0.04%
10,000
2,708
22 out of 2,708 to receive 500 Shares
0.04%
15,000
1,865
21 out of 1,865 to receive 500 Shares
0.04%
20,000
1,424
22 out of 1,424 to receive 500 Shares
0.04%
25,000
1,343
25 out of 1,343 to receive 500 Shares
0.04%
30,000
1,038
24 out of 1,038 to receive 500 Shares
0.04%
35,000
931
25 out of 931 to receive 500 Shares
0.04%
40,000
938
28 out of 938 to receive 500 Shares
0.04%
45,000
669
23 out of 669 to receive 500 Shares
0.04%
50,000
1,428
54 out of 1,428 to receive 500 Shares
0.04%
60,000
795
36 out of 795 to receive 500 Shares
0.04%
70,000
800
42 out of 800 to receive 500 Shares
0.04%
80,000
707
43 out of 707 to receive 500 Shares
0.04%
90,000
558
38 out of 558 to receive 500 Shares
0.04%
100,000
2,156
163 out of 2,156 to receive 500 Shares
0.04%
150,000
1,723
195 out of 1,723 to receive 500 Shares
0.04%
200,000
1,312
198 out of 1,312 to receive 500 Shares
0.04%
250,000
1,069
201 out of 1,069 to receive 500 Shares
0.04%
300,000
881
200 out of 881 to receive 500 Shares
0.04%
350,000
2,107
556 out of 2,107 to receive 500 Shares
0.04%
Total
150,874
Total number of Pool A successful applicants: 2,034

<<<PAGE 13>>>
13
NO. OF  
H SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL NO. 
OF H SHARES 
APPLIED FOR
POOL B
400,000
3,412
343 out of 3,412 to receive 500 Shares
0.01%
450,000
791
90 out of 791 to receive 500 Shares
0.01%
500,000
1,164
146 out of 1,164 to receive 500 Shares
0.01%
600,000
733
111 out of 733 to receive 500 Shares
0.01%
700,000
625
110 out of 625 to receive 500 Shares
0.01%
800,000
485
98 out of 485 to receive 500 Shares
0.01%
900,000
412
93 out of 412 to receive 500 Shares
0.01%
1,017,000
4,075
1,043 out of 4,075 to receive 500 Shares
0.01%
Total
11,697
Total number of Pool B successful applicants: 2,034
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
OTHER INFORMATION
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
The Company has applied to the Stock Exchange, and the Stock Exchange has granted, a consent 
under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate certain Offer 
Shares in the International Offering to connected clients. The allocation of Offer Shares to such 
connected clients is in compliance with all the conditions under the consent granted by the Stock 
Exchange.

<<<PAGE 14>>>
14
Details of the placement to connected clients are set out below:
No.
Connected client
Connected distributor
Relationship with the
connected distributor
Basis of 
holding 
securities
Number
of Offer
Shares
Ultimate  
beneficial  
owner of the  
Offer Shares 
allocated to the 
connected client
Percentage 
of the 
Offer Shares
Percentage of 
total issued 
Shares of  
the Company 
immediately upon 
completion of the 
Global Offering
1.
Bosera Asset Management 
(International) Co., Ltd 
(“Bosera AM”)
CMB International Capital 
Limited (“CMBI”), CMB 
International Securities 
Limited (“CMBI Securities”), 
and CMB International 
Global Markets Limited 
(“CMBI Global Markets”, 
together with CMBI and 
CMBI Securities, the “CMBI 
Connected Distributors”)
Bosera AM is a member of the same 
group with CMBI, CMBI Securities 
and CMBI Global Markets.
Discretionary
175,000
Please refer to 
note 1 below.
0.86%
0.19%
2.
Value Partners Limited 
and Value Partners 
Hong Kong Limited 
(collectively, “Value 
Partners”)
GF Securities (Hong Kong) 
Brokerage Limited (“GF 
Securities (Hong Kong) 
Brokerage”)
GF Securities (Hong Kong) Brokerage is 
an indirect wholly-owned subsidiary 
of GF Securities Co., Ltd. (Stock 
Code: 1776) (“GF Securities”). Value 
Partners is a wholly-owned subsidiary 
of Value Partners Group Limited 
(Stock Code: 806) (“VPGL”).
GF Securities is interested in 20.04% 
shareholding in VPGL which renders 
VPGL and its subsidiaries “associates” 
of GF Securities, hence Value Partners 
and GF Securities (Hong Kong) 
Brokerage is a “member of the same 
group of companies”.
Discretionary
213,000
Please refer to 
note 2 below.
3.93%
0.89%

<<<PAGE 15>>>
15
No.
Connected client
Connected distributor
Relationship with the
connected distributor
Basis of 
holding 
securities
Number
of Offer
Shares
Ultimate  
beneficial  
owner of the  
Offer Shares 
allocated to the 
connected client
Percentage 
of the 
Offer Shares
Percentage of 
total issued 
Shares of  
the Company 
immediately upon 
completion of the 
Global Offering
3.
CHINA ASSET 
MANAGEMENT 
(HONG KONG) 
LIMITED (“China 
Asset Management”)
CITIC Securities Brokerage (HK) 
Limited (“CITIC Brokerage”)
China Asset Management is owned as to 
62.2% by CITIC Securities Company 
Limited, which is holding company 
of CITIC Brokerage. China Asset 
Management is a member of the 
same group of companies as CITICS 
Brokerage
Discretionary
175,000
Please refer to 
note 3 below.
0.86%
0.19%
Notes:
1) 
Bosera AM will hold the Offer Shares in its capacity as a discretionary fund manager managing assets on behalf of its underlying clients. To the best of 
knowledge of Bosera AM, the underlying clients of Bosera AM, together with its ultimate beneficial owners, is an independent third party of the Company, its 
subsidiaries, its Controlling Shareholders, its substantial shareholders, Bosera AM, the CMBI Connected Distributors and the companies which are members of 
the same group of the CMBI Connected Distributors.
2) 
Value Partners will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their investors, each of which is 
an independent third party of the Company, its subsidiaries, its Controlling Shareholders, its substantial shareholders, Value Partners, GF Securities and the 
companies which are members of the same group of GF Securities. To the best of knowledge of Value Partners, the underlying clients of Value Partners, together 
with its ultimate beneficial owners, is an independent third party of the Company, its subsidiaries, its Controlling Shareholders, its substantial shareholders, Value 
Partners, GF Securities (Hong Kong) Brokerage and the companies which are members of the same group of GF Securities (Hong Kong) Brokerage.
3) 
China Asset Management will subscribe for and hold the Offer Shares as a placee under the International Offering in accounts in its capacity as the discretionary 
fund manager managing assets on behalf of its underlying clients. To the best of knowledge of China Asset Management, the underlying clients of China Asset 
Management, together with its ultimate beneficial owners, is an independent third party of the Company, its subsidiaries, its Controlling Shareholders, its 
substantial shareholders, China Asset Management, CITIC Brokerage and the companies which are members of the same group of CITIC Brokerage.

<<<PAGE 16>>>
16
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or 
any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer or 
solicitation to purchase or subscribe for securities in the United States. The Offer Shares have 
not been and will not be registered under the United States Securities Act of 1933, as amended 
(the “U.S. Securities Act”) or any state securities laws in the United States and may not be 
offered, sold, pledged or transferred within the United States or to, or for the account or benefit 
of U.S. persons (as defined in Regulation S under the U.S. Securities Act), except in transactions 
exempt from, or not subject to, the registration requirements of the U.S. Securities Act. The 
Offer Shares are being offered and sold (1) solely to qualified institutional buyers as defined in 
Rule 144A in reliance on Rule 144A or another exemption from, or in a transaction not subject 
to, registration under the U.S. Securities Act and (2) outside the United States in offshore 
transactions in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated February 27, 2026 issued by ALSCO Pooling Service 
Co., Ltd. 蘇州優樂賽共享服務股份有限公司 for detailed information about the Global Offering 
described below before deciding whether or not to invest in the Offer Shares thereby being 
offered.
* Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing 
Date (which is currently expected to be on March 9, 2026).

<<<PAGE 17>>>
17
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, based on the Offer Price of 
HK$11.00 per H Share: (1) 27,506,138 H Shares, representing approximately 30.45% of the total 
number of issued Shares will be counted towards the public after Listing, which will satisfy the 
public float requirement under Rule 19A.13A of the Listing Rules; and (2) the Company satisfies 
the free float requirement pursuant to Rule 19A.13C(1) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering: (i) the 
Shares will be held by at least 300 Shareholders at the time of Listing, in compliance with Rule 
8.08(2) of the Listing Rules; (ii) the three largest public Shareholders will not hold more than 
50% of the H Shares held in public hands at the time of Listing, in compliance with Rules 8.08(3) 
and 8.24 of the Listing Rules; (iii) no placee will, individually, be placed more than 10% of the 
enlarged issued share capital of the Company immediately after the Global Offering; and (iv) there 
will not be any new substantial Shareholder (as defined in the Listing Rules) immediately after the 
Global Offering.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Monday, March 
9, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting — Underwriting Arrangements 
and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade the H Shares on the basis of publicly available allocation 
details prior to the receipt of H Share certificates or prior to the H Share certificates becoming 
valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Monday, 
March 9, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Monday, March 9, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 200 H Shares each, and the stock code of the H Shares will 
be 2649.
By order of the Board
ALSCO Pooling Service Co., Ltd.
Mr. Sun Yan’an
Chairman and Director
Hong Kong, March 6, 2026
As of the date of this announcement, the board of directors of the Company comprises: (i) 
Mr. Sun Yan’an, Mr. Wang Yue and Mr. Xiang Yang as executive Directors; (ii) Dr. Fang Dianjun, 
Mr. Ren Qingxiang and Dr. Dai Yuanyue as non-executive Directors; and (iii) Dr. Wang Rui, 
Dr. Liu Dacheng and Ms. Hong Ting as independent non-executive Directors.
