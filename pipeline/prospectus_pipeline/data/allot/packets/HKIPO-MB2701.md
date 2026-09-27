# 配发结果公告抽取任务：2701.HK Nsing Technologies Inc. - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**20/03/2026 21:01**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0320/2026032001594.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2701.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Hong Kong Stock 
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents 
of this announcement, make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement. This announcement is not for release, publication, distribution, directly or indirectly, in or into the 
United States (including its territories and possessions, any state of the United States and the District of Columbia).
This announcement does not constitute or form a part of any offer to sell or solicitation to purchase or subscribe for 
securities in the United States or in any other jurisdictions in which such offer or solicitation would be unlawful. The 
securities mentioned herein have not been, and will not be, registered under the United States Securities Act of 1933 as 
amended from time to time (the “U.S. Securities Act”) or any state securities law of the United States. The securities 
may not be offered, sold, pledged or transferred within the United States or to, or for the account or benefit of U.S. 
persons (as defined in Regulation S under the U.S. Securities Act (“Regulation S”)), except in transactions exempt 
from, or not subject to, the registration requirements of the U.S. Securities Act. The Offer Shares may be offered, sold 
or delivered outside the United States to non-U.S. persons in offshore transactions in accordance with Regulation S.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
March 13, 2026 (the “Prospectus”) issued by Nsing Technologies Inc. (國民技術股份有限公司) (the “Company”) 
for detailed information about the Global Offering described below before deciding whether or not to invest in the H 
Shares thereby being offered. Any investment decision in relation to the Offer Shares should be taken solely in reliance 
on the information in the Prospectus. The Company has not been and will not be registered under the U.S. Investment 
Company Act of 1940, as amended.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
Potential investors of the Offer Shares should note that the Sole Sponsor and the Sponsor-Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the 
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the 
section headed “Underwriting – Underwriting Arrangements – Hong Kong Public Offering – Grounds for Termination” 
in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to 
be on March 23, 2026).

<<<PAGE 2>>>
2
NSING TECHNOLOGIES INC.
國民技術股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the 
Global Offering
:
95,000,000 H Shares
Number of Hong Kong Offer Shares
:
9,500,000 H Shares
Number of International Offer Shares
:
85,500,000 H Shares
Final Offer Price
:
HK$10.80 per H Share, plus brokerage of
 1.0%, SFC transaction levy of 0.0027%,
 Stock Exchange trading fee of 0.00565%
 and AFRC transaction levy of 0.00015%
 (payable in full on application in Hong
 Kong Dollars and subject to refund)
Nominal value
:
RMB 1.00 per H Share
Stock Code
:
2701
Sole Sponsor, Overall Coordinator, Joint Global Coordinator,
Joint Bookrunner and Joint Lead Manager
Overall Coordinator, Joint Global Coordinator,
Joint Bookrunner and Joint Lead Manager
Joint Bookrunner and Joint Lead Manager

<<<PAGE 3>>>
NSING TECHNOLOGIES INC. 
國民技術股份有限公司 
ANNOUNCEMENT OF ALLOTMENT RESULTS 
 
Unless otherwise defined herein, capitalized terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated March 13, 2026 (the “Prospectus”) 
issued by NSING TECHNOLOGIES INC. (國民技術股份有限公司) (the “Company”).  
 
 
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, Shareholders and prospective investors should be aware that the price 
of the H Shares could move substantially even with a small number of H Shares traded 
and should exercise extreme caution when dealing in the H Shares. 
SUMMARY 
 
Company Information 
Stock Code 
2701 
Stock Short Name 
NSING TECH 
Dealings commencement date 
March 23, 2026* 
* see note at the end of the announcement 
 
Price Information 
Final Offer Price 
HK$10.80 
Maximum Offer Price 
HK$10.80 
Offer Price Adjustment exercised 
N/A 
 
Offer Shares and Share Capital 
Number of Offer Shares 
95,000,000 
Number of Offer Shares in Hong Kong 
Public Offering  
9,500,000 
Number of Offer Shares in International 
Offering  
85,500,000 
Number of issued Shares upon Listing  
678,126,700 
 
Proceeds 
Gross proceeds (Note) 
HK$1,026.0 million 
Less: Estimated 
listing 
expenses 
payable based on Final Offer 
Price 
HK$82.1 million 
Net Proceeds 
HK$943.9 million 
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For 
details of the use of proceeds, please refer to the section headed “Future Plans and Use of 
Proceeds” of the Prospectus.  

<<<PAGE 4>>>
 
ALLOTMENT RESULTS DETAILS 
 
HONG KONG PUBLIC OFFERING 
 
 
No. of valid applications 
56,547 
No. of successful applications 
24,399 
Subscription level 
131.83 times 
Claw-back triggered 
No 
No. of Offer Shares initially available under the Hong Kong 
Public Offering 
9,500,000 
Number of Offer Shares reallocated from the International 
Offering 
0 
Final no. of Offer Shares under the Hong Kong Public 
Offering 
9,500,000 
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering  
10% 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, 
investors can refer to the “Allotment Results” page at the designated results of allocation at 
www.hkeipo.hk/IPOResult or www.hkeipo.hk/IPOResult with a “search by ID” function. 
 
INTERNATIONAL OFFERING  
 
 
No. of placees 
59 
Subscription Level  
2.51 times 
No. of Offer Shares initially available under the International Offering 85,500,000 
Number of Offer Shares reallocated to the Hong Kong Public Offering 0 
Final no. of Offer Shares under the International Offering 
85,500,000 
% of Offer Shares under the International Offering to the Global 
Offering  
90% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) 
a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by 
the Stock Exchange to permit H Shares in the International Offering to be placed to certain 
Existing Minority Shareholders and/or their close associates, and (b) a consent under Chapter 
4.15 of the Guide for New Listing Applicants to permit the Company to, among other things, 
allocate further H Shares in the International Offering to certain Cornerstone Investors and/or 
their respective close associates, (i) none of the Offer Shares subscribed by the placees and the 
public have been financed directly or indirectly by the Company, any of the Directors, chief 
executive of the Company, substantial Shareholders, existing Shareholders of the Company or 
any of its subsidiaries or their respective close associates; and (ii) none of the placees and the 

<<<PAGE 5>>>
public who have purchased the Offer Shares are accustomed to taking instructions from the 
Company, any of the Directors, chief executive of the Company, substantial Shareholders, 
existing Shareholders of the Company or any of its subsidiaries or their respective close 
associates in relation to the acquisition, disposal, voting or other disposition of H Shares 
registered in his/her/its name or otherwise held by him/her/it. 
 
The placees in the International Offering include the following: 
 
Cornerstone Investors  
 
Investor 
No. of Offer 
Shares 
allocated 
% of total 
issued H Shares 
immediately 
after the Global 
Offering Note 1 
% of total issued 
share capital of 
the Company 
immediately after 
the Global 
Offering  
Existing 
shareholders or 
their close 
associates Note 2 
Guohua Life 
Insurance Co., 
Ltd. 
(“Guohua 
Life 
Insurance”) 
4,629,600 
4.9% 
0.68% 
Yes 
Harvest 
Oriental II SP 
(“Harvest 
Oriental II”) 
Note 3 
3,703,600 
3.9% 
0.55% 
No 
Ms. Christine 
Tai (戴婉琴) 
(“Ms. Tai”)  
2,777,600 
2.9% 
0.41% 
No 
Mr. An 
Jiangbo(安江
波) (“Mr. 
An”) 
925,800 
1.0% 
0.14% 
No 
Sunwoda 
Treasury 
(Hong Kong) 
Limited (欣旺
達財資(香港)
925,800 
1.0% 
0.14% 
No 

<<<PAGE 6>>>
有限公司) 
(“Sunwoda 
Treasury”) 
Total 
12,962,400 
13.6% 
1.91% 
- 
Notes: 
 
(1) The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering. 
 
(2) In addition to the Offer Shares subscribed for as Cornerstone Investors, a close associate of Harvest Oriental 
II was allocated further Offer Shares as placees in the International Offering. Please refer to the section headed 
“Allotment Results Details – International Offering – Allotees with Waivers/Consents Obtained” in this 
announcement for details. Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-up 
as indicated below. For details, please refer to the section headed “Lock-up Undertakings – Cornerstone 
Investors” in this announcement.  
 
(3) The number of Offer Shares allocated to such investor only represents the number of Offer Shares allocated 
to the investors as cornerstone investors in the International Offering. For allocations of Offer Shares to the 
relevant investor and/or its close associates as placee, please refer to the section headed “Allotment Results 
Details — International Offering — Allotees with waivers/ consents obtained” in this announcement. 
 
 
Allottee with waivers/consents obtained 
 
Investor 
No. of Offer 
Shares allocated 
Note 3 
% of Offer 
Shares 
immediately 
after the 
Global 
Offering 
% of total 
issued share 
capital 
immediately 
after the 
Global 
Offering Note 
4 
Relationship 
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and 
consent under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H 
Shares by Existing Minority Shareholders holding more than 1% of the issued share 
capital of the Company immediately prior to the completion of the Global Offering and/or 
their close associates Note 1 
Nil Note 1 
Nil 
Nil 
Nil 
Nil 
Allotees with consent under Chapter 4.15 of the Guide for New Listing Applicants in 
relation to allocations of further H Shares to investors who will participate in the Proposed 
Listing both as (i) a cornerstone investor and (ii) a placee in the International Offering Note 
1 

<<<PAGE 7>>>
Harvest Global 
Capital 
Investments 
Limited 
2,000,000 
2.11% 
0.29% 
A close associate of a 
Cornerstone Investor 
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 
of the Guide for New Listing Applicants in relation to allocations to connected clients Note 
1 
CITIC Securities 
International 
Capital 
Management 
Limited (“CSI”) 
7,020,000 
7.39% 
1.04% 
Connected client as a 
placee 
CITIC Securities 
Asset 
Management 
Company 
Limited 
(“CITIC AM”) 
20,000 
0.02% 
0.0029% 
Connected client as a 
placee 
Huatai Capital 
Investment 
Limited 
(“HTCI”) 
6,000,000 
6.32% 
0.88% 
Connected client as a 
placee 
Private wealth 
management 
division of Huatai 
Financial 
Holdings (Hong 
Kong) Limited 
(“HTFH PWM”) 
Note 2 
5,555,400 
5.85% 
0.82% 
Connected client as a 
placee, with a 
cornerstone investor 
as one of its ultimate 
clients  
Notes: 
 
1. For details of (a) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of the Placing Guidelines granted by the Stock Exchange to permit the Company to 
allocate certain Offer Shares in the International Offering to existing minority shareholders and their close 
associates as cornerstone investor; (b) a consent under paragraph 18 of Chapter 4.15 of the Guide for New 
Listing Applicants to permit the Company to allocate certain Offer Shares in the International Offering to 
certain Cornerstone Investors and/or their close associates; and (c) a consent under paragraph 1C(1) of 
the Placing Guidelines to permit the Company to allocate certain Offer Shares in the International Offering 
to connected clients, please refer to the sub-section relating to section headed “Others/Additional 
Information” in this announcement. 
 
2. Sunwoda Treasury, a Cornerstone Investor of the Company, is one of the ultimate clients of HTFH PWM, 
please refer to the section headed “Others/Additional Information – Placing to connected clients with prior 

<<<PAGE 8>>>
consents under paragraph 1C(1) of the Placing Guidelines” in this announcement for details.  
 
3. For allocations of Offer Shares to the relevant investors as Cornerstone Investors, please refer to the 
section headed “Allotment Results Details – International Offering – Cornerstone Investors” in this 
announcement.  
 
4. Only taking into account the H Shares allocated to the relevant investors under the Global Offering. 
 

<<<PAGE 9>>>
 
 
LOCK-UP UNDERTAKINGS  
 
Cornerstone Investors  
 
Name 
Number of 
shares held in 
the Company 
subject to lock 
up undertaking 
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing 
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing 
Note 1 
% of total 
issued share 
capital of the 
Company 
subject to 
lock-up 
undertakings 
upon Listing  
Last day 
subject to the 
lock-up 
undertakings 
Note 2 
Guohua 
Life 
Insurance 
4,629,600 
4,629,600 
4.9% 
0.68% 
September 
22, 2026 
Harvest 
Oriental 
II 
3,703,600 
3,703,600 
3.9% 
0.55% 
September 
22, 2026 
Ms. Tai 
2,777,600 
2,777,600 
2.9% 
0.41% 
September 
22, 2026 
Mr. An 
925,800 
925,800 
1.0% 
0.14% 
September 
22, 2026 
Sunwoda 
Treasury 
925,800 
925,800 
1.0% 
0.14% 
September 
22, 2026 
Notes: 
 
1. The number of H Shares immediately after the Global Offering is the same as the number 
of Offer Shares to be issued under the Global Offering. 
 
2. In accordance with the relevant cornerstone investment agreements, the required lock-
up ends on six months after the Listing Date, i.e. September 22, 2026. The Cornerstone 
Investors will cease to be prohibited from disposing of or transferring H Shares 
subscribed for pursuant to the relevant cornerstone investment agreements after the 
indicated date. 
 
PLACEE CONCENTRATION ANALYSIS 
 
Placees* 
Number of H 
Shares allotted 
Allotment 
as % of 
International 
Offering  
Allotment 
as % of total 
Offer Shares  
Number of  
Shares held 
upon Listing 
% of total 
issued share 
capital upon 
Listing 
Top 1 
7,020,000 
8.21% 
7.39% 
7,020,000 
1.04% 

<<<PAGE 10>>>
 
 
Top 5 
27,982,800 
32.73% 
29.46% 
30,982,100 
4.57% 
Top 10 
48,232,800 
56.41% 
50.77% 
51,232,100 
7.55% 
Top 25 
76,182,600 
89.10% 
80.19% 
79,181,900 
11.68% 
 
Note 
* Ranking of placees is based on the number of H Shares allotted to the placees. 
 
H SHAREHOLDERS CONCENTRATION ANALYSIS 
 
H 
Shareholde
rs * 
Number of 
H Shares 
allotted 
Allotment 
as % of 
Internatio
nal 
Offering  
Allotment 
as % of 
total Offer 
Shares  
% of total 
issued H 
share 
capital 
upon 
Listing 
Number of 
Shares 
held upon 
Listing 
% of total 
issued 
share 
capital 
upon 
Listing  
Top 1 
7,020,000 
8.21% 
7.39% 
7.39% 
7,020,000 
1.04% 
Top 5 
27,982,800 
32.73% 
29.46% 
29.46% 
30,982,100 
4.57% 
Top 10 
48,232,800 
56.41% 
50.77% 
50.77% 
51,232,100 
7.55% 
Top 25 
76,182,600 
89.10% 
80.19% 
80.19% 
79,181,900 
11.68% 
 
Note 
* Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders 
upon Listing. 
 
SHAREHOLDER CONCENTRATION ANALYSIS  
 
Shareholder 
s* 
Number 
of H 
Shares 
allotted 
Allotment 
as % of 
International 
Offering  
Allotment 
as % of 
total 
Offer 
Shares  
Number 
of H 
Shares 
held upon 
Listing 
Number of 
Shares 
held upon 
Listing 
% of total 
issued 
share 
capital 
upon 
Listing  
Top 1 
0 
0.00% 
0.00% 
0 
15,453,300 
2.28% 
Top 5 
23,353,200 27.31% 
24.58% 
23,353,200 41,805,800 
6.16% 
Top 10 
41,702,800 48.78% 
43.90% 
41,702,800 64,398,583 
9.50% 
Top 25 
68,442,200 80.05% 
72.04% 
68,442,200 102,118,383 15.06% 
 
Note 
* Ranking of Shareholders is based on the number of Shares (of all classes) held by the 

<<<PAGE 11>>>
 
 
Shareholder upon Listing. 
 

<<<PAGE 12>>>
 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
 
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made 
by the public will be conditionally allocated on the basis set out below: 
 
NO. OF SHARES 
APPLIED FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF 
ALLOTMENT / 
BALLOT 
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL NO. 
OF H SHARES 
APPLIED FOR 
POOL A 
200 
24,237 
7,272 out of 24,237 
applicants to receive 
200 H Shares 
30.00% 
400 
3,180 
1,104 out of 3,180 
applicants to receive 
200 H Shares 
17.36% 
600 
9,007 
3,403 out of 9,007 
applicants to receive 
200 H Shares 
12.59% 
800 
1,353 
543 out of 1,353 
applicants to receive 
200 H Shares 
10.03% 
1,000 
1,735 
730 out of 1,735 
applicants to receive 
200 H Shares 
8.41% 
1,200 
414 
181 out of 414 
applicants to receive 
200 H Shares 
7.29% 
1,400 
370 
167 out of 370 
applicants to receive 
200 H Shares 
6.45% 
1,600 
336 
156 out of 336 
applicants to receive 
200 H Shares 
5.80% 
1,800 
554 
264 out of 554 
applicants to receive 
200 H Shares 
5.29% 
2,000 
2,738 
1,332 out of 2,738 
applicants to receive 
200 H Shares 
4.86% 
3,000 
1,279 
678 out of 1,279 
applicants to receive 
3.53% 

<<<PAGE 13>>>
 
 
200 H Shares 
4,000 
1,498 
843 out of 1,498 
applicants to receive 
200 H Shares 
2.81% 
5,000 
816 
481 out of 816 
applicants to receive 
200 H Shares 
2.36% 
6,000 
604 
370 out of 604 
applicants to receive 
200 H Shares 
2.04% 
7,000 
232 
147 out of 232 
applicants to receive 
200 H Shares 
1.81% 
8,000 
210 
137 out of 210 
applicants to receive 
200 H Shares 
1.63% 
9,000 
1,406 
938 out of 1,406 
applicants to receive 
200 H Shares 
1.48% 
10,000 
1,883 
1,284 out of 1,883 
applicants to receive 
200 H Shares 
1.36% 
20,000 
1,063 
839 out of 1,063 
applicants to receive 
200 H Shares 
0.79% 
30,000 
456 
392 out of 456 
applicants to receive 
200 H Shares 
0.57% 
40,000 
296 
270 out of 296 
applicants to receive 
200 H Shares 
0.46% 
50,000 
262 
251 out of 262 
applicants to receive 
200 H Shares 
0.38% 
60,000 
174 
173 out of 174 
applicants to receive 
200 H Shares 
0.33% 
70,000 
124 
200 H Shares 
0.29% 
80,000 
110 200 H Shares plus 7 out 
of 110 applicants to 
receive an additional 
200 H Shares 
0.27% 
90,000 
100 200 H Shares plus 9 out 
of 100 applicants to 
0.24% 

<<<PAGE 14>>>
 
 
receive an additional 
200 H Shares 
100,000 
495 
200 H Shares plus 53 
out of 495 applicants to 
receive an additional 
200 H Shares 
0.22% 
200,000 
336 
200 H Shares plus 94 
out of 336 applicants to 
receive an additional 
200 H Shares 
0.13% 
300,000 
171 
200 H Shares plus 67 
out of 171 applicants to 
receive an additional 
200 H Shares 
0.09% 
400,000 
152 
200 H Shares plus 77 
out of 152 applicants to 
receive an additional 
200 H Shares 
0.08% 
 
55,591 
Total number of 
Pool A successful 
applicants: 23,443 
 
POOL B 
500,000 
520 
3,000 H Shares plus 
231 out of 520 
applicants to receive an 
additional 200 H Shares 
0.62% 
600,000 
65 
3,600 H Shares plus 10 
out of 65 applicants to 
receive an additional 
200 H Shares 
0.61% 
700,000 
50 
4,200 H Shares 
0.60% 
800,000 
48 
4,600 H Shares 
0.58% 
900,000 
23 
5,000 H Shares 
0.56% 
1,000,000 
147 
5,400 H Shares 
0.54% 
2,000,000 
54 
10,600 H Shares 
0.53% 
3,000,000 
13 
15,000 H Shares 
0.50% 
4,000,000 
8 
19,600 H Shares 
0.49% 
4,750,000 
28 
23,000 H Shares 
0.48% 
 
956 
Total number of 
Pool B successful 
applicants: 956 
 
 
As of the date of this announcement, the relevant subscription monies previously deposited in 
the designated nominee accounts have been remitted back to the accounts of all HKSCC 

<<<PAGE 15>>>
 
 
participants. Investors should contact their relevant brokers for any inquiries. 
 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect 
of which consent has been obtained, the Company has complied with the Listing Rules and 
guidance materials in relation to the placing, allotment and listing of the Company’s H Shares.  
 
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or 
indirectly, provided by the Company, the Single Largest Shareholder, Directors or syndicate 
members to any placees or the public (as the case may be) and the consideration payable by 
them for each Share of the Company subscribed for or purchased by them is the same as the 
final Offer Price determined by agreement between the Company and the Overall Coordinators 
(for themselves and on behalf of the Underwriters), in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and trading fee payable.  
 
OTHERS / ADDITIONAL INFORMATION 
 
Allocation of H Shares to existing minority Shareholders and their close associates with a 
waiver from the strict compliance with Rule 10.04 of the Listing Rules and a prior consent 
under paragraph 1C(2) of the Placing Guidelines 
 
The Company applied to the Stock Exchange for, and the Stock Exchange has granted, a waiver 
from strict compliance with the requirements under Rule 10.04 and consent under Paragraph 
1C(2) of Appendix F1 to the Listing Rules to permit H Shares in the International Offering to 
be placed to certain existing minority Shareholders who (i) hold less than 5% of the voting 
rights of the Company prior to the completion of the Global Offering and (ii) are not and will 
not become (upon the completion of the Global Offering) core connected persons of the 
Company or the close associates of any such core connected person (together, the “Existing 
Minority Shareholders”), subject to the conditions as follows: 
 
(a) each Existing Minority Shareholder to whom the Company may allocate the H Shares 
under the International Offering holds less than 5% of the voting rights in the Company 
prior to the completion of the Global Offering; 
 
(b) each Existing Minority Shareholder is not, and will not be, a core connected person of the 
Company or any close associate of any such core connected person immediately prior to 
or following the Global Offering;  
 
(c) none of the Existing Minority Shareholders has the power to appoint any Directors nor 
have any other special rights in the Company;  
 
(d) allocation to the existing minority shareholders and their close associates will not affect 
our company’s ability to satisfy the public float requirements of Rule 8.08 (1) (as amended 

<<<PAGE 16>>>
 
 
by Rule 9A 13A(2) of the Listing Rules) or otherwise approved by the Stock Exchange;  
 
(e) each of our Company, the Sole Sponsor and the Overall Coordinators shall confirm to the 
Stock Exchange in writing that, to the best of its knowledge and belief, it has no reason to 
believe that the Existing Minority Shareholders or their close associates received any 
preferential treatment in any allocation in the International Offering by virtue of their 
relationship with our Company; and 
 
(f) details of the allocation to the Existing Minority Shareholders holding more than 1% of 
the issued share capital of our Company immediately prior to the completion of the Global 
Offering will be disclosed in the Prospectus and/or this announcement, as the case may be. 
Nonetheless, as no allocation has been made to any such Existing Minority Shareholders 
holding more than 1% of the issued share capital of the Company, no disclosure has been 
made in this announcement. 
 
Please refer to the section headed “Waivers from strict compliance with the Listing Rules and 
Exemptions from The Companies (Winding Up And Miscellaneous Provisions) Ordinance – 
Allocation of H Shares to Existing Minority Shareholders and their Close Associates” in the 
Prospectus for further details of the waiver and consent.  
 
All allocation of Offer Shares to the Existing Minority Shareholders are in compliance with all 
the conditions under the wavier and consent granted by the Stock Exchange. 
 
Allocation of Offer Shares to Investors Who Will Participate in the Proposed Listing both as 
(i) a Cornerstone Investor and (ii) a Placee in the International Offering with consents under 
Chapter 4.15 of the Guide for New Listing Applicants 
 
The Company has applied for, and the Stock Exchange has granted, a waiver/consent under 
paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants with respect to possible 
allocations to investors who will participate in the Proposed Listing both as (i) a cornerstone 
investor and (ii) a placee in the International Offering (the “Double-Dipping Participants”), 
subject to the following conditions: 
 
(a) the final offering size of the Proposed Listing, will be of a total value of at least HK$1 
billion; 
 
(b) the Offer Shares allocated to all existing shareholders and/or their close associates (as 
cornerstone investors and placees in the International Offering) as permitted under this 
exemption do not exceed 30% of the total number of the H Shares offered; 
 
(c) each Director and chief executive of the Company has confirmed that no securities have 
been allocated to them or their respective close associates under the exemption as required 
by paragraph 18(iii) of Chapter 4.15 of the Guide for New Listing Applicants; 
 

<<<PAGE 17>>>
 
 
(d) allocation to the Double-Dipping Participants and/or their respective close associates will 
not affect the Company’s ability to satisfy the public float requirement under Rule 19A. 
13(2) of the Listing Rules; and 
 
(e) details of the allocation to the Double-Dipping Participants and/or their respective close 
associates under the exemption will be disclosed in the allotment results announcement. 
 
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange. 
 
For details of the allocations of Offer Shares to investors who will participate in the Proposed 
Listing both as (i) a cornerstone investor and (ii) a placee in the International Offering 
Cornerstone Investors, please refer to the section headed “Allotment Results Details – 
International Offering – Allotees with Waivers/Consents Obtained” in this announcement. 
 
Placing to connected clients with prior consents under paragraph 1C(1) of the Placing 
Guidelines 
 
The Company has applied for, and the Stock Exchange has granted, consents under paragraph 
1C of the Placing Guidelines to permit allocation to connected clients pursuant to the Placing 
Guidelines. The allocation of Offer Shares to such connected clients is in compliance with all 
the conditions under the consents granted by the Stock Exchange. Details of the placement to 
connected clients (including the cornerstone tranche and placing tranche) are set out below.  

<<<PAGE 18>>>
 
 
 
No. 
Connected Distributor 
Connected 
Client 
Relationship 
Whether the 
Connected 
Client will 
hold the 
beneficial 
interests of the 
Offer Shares 
on a non-
discretionary 
basis or 
discretionary 
basis for 
independent 
third partis 
Whether 
the 
Connected 
Client is a 
collective 
investment 
scheme 
which is 
not 
authorised 
by the SFC 
or is 
expected to 
hold the 
Offer 
Shares on 
behalf of 
such 
scheme 
Number of 
Offer 
Shares to 
be allocated 
to the 
connected 
client 
Approximate 
percentage 
of Offer 
Shares  
Approximate 
percentage 
of total 
issued share 
capital 
immediately 
after the 
Global 
Offering  
1. 
 CLSA Limited (“CLSA”) 
CSI Note 1 
CSI is a member of the same group 
of companies as CLSA. 
Non-
discretionary 
basis 
No 
7,020,000 
7.3895% 
1.0352% 
2. 
 CLSA 
CITIC AM Note 
2 
CITIC Asset Management is a 
member of the same group of 
companies as CLSA. 
Discretionary 
basis 
CITIC AM 
is expected 
to hold the 
Offer 
Shares on 
20,000 
0.0211% 
0.0029% 

<<<PAGE 19>>>
 
 
behalf of 
such 
scheme. 
3. 
 
Huatai Financial Holdings 
(Hong 
Kong) 
Limited 
(“HTFH”) 
HTCI Note 3 
HTCI is a member of the same 
group as HTFH 
Non-
discretionary 
basis 
HTCI is 
expected to 
hold the 
Offer 
Shares on 
behalf of 
such 
scheme. 
6,000,000 
6.3158% 
0.8848% 
4. 
 HTFH 
HTFH PWM 
Note 4 
Private 
wealth 
management 
division of HTFH is a division of 
HTFH and will place the order as 
a placee under the International 
Offering on behalf of the HTFH 
Ultimate Clients 
Non-
discretionary 
basis 
No 
5,555,400 
5.8478% 
0.8192% 
 
Notes: 
 
(1) CSI  
 
CSI will hold the Offer Shares as a placee under the International Offering on behalf of CSI Ultimate Clients, on a non-discretionary basis, pursuant to which: (i) CSI will act 
as the single counterparty of a back-to-back total return swap transaction (the “CSI Back-to-back TRS”) to be entered into by it in connection with a total return swap order 
(the “CSI Client TRS”) placed and fully funded by its ultimate clients (“CSI Ultimate Clients”), by which CSI will pass the full economic exposure of the Offer Shares placed 
to CSI to the CSI Ultimate Clients; and (ii) as confirmed by CSI and CLSA, CSI will hold the legal title and beneficial interest in the Offer Shares, but will contractually agree 
to pass on the full economic exposure and return of the Offer Shares to the CSI Ultimate Clients, on a non-discretionary basis. The CSI Ultimate Clients may exercise their 

<<<PAGE 20>>>
 
 
early termination rights to terminate the CSI Client TRS at any time from the trade date of the CSI Client TRS which should be on or after the date on which the Offer Shares 
are listed on the Stock Exchange; (iii) upon the final maturity or termination of the CSI Client TRS by the CSI Ultimate Clients, CSI will dispose of the Offer Shares on the 
secondary market and the CSI Ultimate Clients will receive a final termination amount of the CSI Back-to-back TRS which will have taken into account all the economic returns 
or economic loss in relation to the Offer Shares and the fixed amount of transaction fees of the CSI Back- to-back TRS and the CSI Client TRS. Due to its internal policy, CSI 
will not exercise the voting right of the Offer Shares during the terms of the CSI Back-to-back TRS; and (iv) CSI is not a collective investment schemes which is not authorized 
by the SFC, nor is expected to hold the Offer Shares on behalf of such scheme. The details of the CSI Ultimate Clients are as follow: 
 
Name  
Fund Manager 
  
UBO of Fund Manager 
Limited 
Partner/Shareholding 
holding 30% or more in the CSI 
Ultimate Clients 
HY Capital Company Limited 
Not applicable 
 
Not applicable 
 
Xia Hui  
Lu Ang 
Black Crystal Capital Management Co., Ltd. 
(黑晶資本管理有限公司) 
 
Not applicable 
Not applicable 
Li Chuxin (李出新) 
Shao Yukai (邵宇開) 
 
To the best of knowledge of CSI and after making all reasonable enquiries, the CSI Ultimate Clients, together with each of their ultimate beneficial owners, is an independent 
third party of the Company, its subsidiaries, its substantial shareholders, CSI, CLSA and the companies which are members of the same group of CLSA. 
 
(2) CITIC Asset Management 
 
CITIC Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their investors (the “CITIC Asset 
Management Ultimate Clients”), each of which is, to the best knowledge of CITIC Asset Management, an independent third party of the Company, its subsidiaries, its substantial 
shareholders, CITIC Asset Management, CLSA and the companies which are members of the same group of CLSA. No ultimate beneficial owner holds 30% or more interest in 
the funds. 
 
The details of the CITIC Asset Management Ultimate Clients are as follow: 

<<<PAGE 21>>>
 
 
 
Fund Name 
Fund Manager 
 
UBO of Fund Manager 
Limited 
Partner/Shareholding 
holding 30% or more in the CITIC 
Asset Management Ultimate Clients 
CITIC SECURITIES COMPANY LIMITED-
XINHANG ZHIYUAN NO.1(中信证券信航
致远1 号集合资产管理计划 ) 
CITIC Asset Management 
CITIC Securities Company Limited 
N/A 
CITIC SECURITIES COMPANY LIMITED-
XINHANG ZHIYUAN NO.3(中信证券信航
致远3 号集合资产管理计划 ) 
CITIC Asset Management 
CITIC Securities Company Limited 
N/A 
CITIC 
Securities 
AM-Guibinfengyuan 
No.118 QDII（中信证券资管贵宾丰元118
号QDII 集合资产管理计划） 
CITIC Asset Management 
CITIC Securities Company Limited 
N/A 
 
To the best of knowledge of CITIC Asset Management and after making all reasonable enquiries, CITIC Asset Management Ultimate Client, together with each of their ultimate 
beneficial owners, is an independent third party of the Company, its subsidiaries, its substantial shareholders, CITIC Asset Management, CLSA and the companies which are 
members of the same group of CLSA.  
 
(3) HTCI 
 
HTFH is a distributor in connection with the Global Offering. Pursuant to an ISDA Agreement (the “ISDA Agreement”), HTCI, which intends to participate in the Global 
Offering as a placee, will hold the beneficial interest of the Shares on a non-discretionary basis as the single underlying holder under a back-to-back total return swap (the 
“Back-to-back TRS”) to be entered by HTCI in connection with a Client TRS (as defined below) placed by and fully funded (i.e. with no financing provided by HTCI) by the 
Huatai Ultimate Client (as defined below), by which, HTCI will, subject to customary fees and commissions, pass the full economic exposure of the Shares to the Huatai 
Ultimate Client, which in effect, HTCI will hold the beneficial interest of the Shares on behalf of the Huatai Ultimate Client. Accordingly, HTCI is considered as a “connected 
client” of HTFH pursuant to paragraph 13(7) of the Placing Guidelines. 
 
The offshore investor (the “Huatai Ultimate Client”), through its investment manager, will place a total return swap order (the “Client TRS”) with HTCI in connection with 

<<<PAGE 22>>>
 
 
the Company’s IPO. In order to hedge its exposure under the Client TRS, HTCI participates in the Company’s IPO and subscribes the Shares through placing order with HTFH 
during the International Offering. 
 
The purpose of HTCI to subscribe for the Shares is for hedging the Client TRS order placed by the Huatai Ultimate Client. Pursuant to the terms of the Client TRS, during the 
tenor of the Client TRS, subject to customary fees and commissions, all economic returns of the Shares will be passed to the Huatai Ultimate Client through the Client TRS and 
all economic loss shall be borne by the Huatai Ultimate Client. HTCI will not take any economic return or bear any economic loss in relation to the Shares.  
 
The Huatai Ultimate Client may exercise an early termination right to terminate the Client TRS at any time from the issue date of the Client TRS which should be on or after 
the date on which the Shares are listed on the Stock Exchange at its own discretion. Upon the termination upon maturity or early termination of the Client TRS by the Huatai 
Ultimate Client, HTCI will dispose the Shares on the secondary market and the Huatai Ultimate Client will receive a final settlement amount of the Client TRS in cash in 
accordance with the terms and conditions of the Client TRS which should have taken into account all the economic returns or economic loss in relation to the Shares. If upon 
the maturity of the Client TRS, the Huatai Ultimate Client intends to extend the investment period, subject to further agreement between HTCI and the relevant Huatai Ultimate 
Client, the term of the Client TRS could be extended by way of a new issuance or a tenor extension.  
 
It is proposed that HTCI will hold the legal title and the voting right of the Shares by itself, and pass through the economic exposure to the Huatai Ultimate Client, being a 
client who places a Client TRS order with HTCI in connection with the IPO of the Company. HTCI will not exercise the voting right of the Shares during the tenor of the Client 
TRS. 
 
During the life of the Client TRS, HTCI may continue to hold the Shares in its custodian account, or to hold some or all of the Shares in a prime brokerage account for stock 
borrowing purposes, where HTCI will lend out its holding of underlying Shares in the form of stock borrowing loans consistent with market practice to lower its finance costs, 
provided that HTCI has the ability to call back the Shares on loan at any time in order to satisfy its obligations under the Client TRS to ensure the economic interests are 
ultimately passed to the Huatai Ultimate Client. 
 
The details of the HTCI Ultimate Client are as follow: 
 
Name of HTCI Ultimate Client 
Fund Manager 
UBO of Fund Manager 
Limited 
Partner/Shareholding 
holding 30% or more in the HTCI 
Ultimate Client 

<<<PAGE 23>>>
 
 
Jing Lin Capital VCC Sub A/C Vista 
Global Capital Fund 
Vista 
Global 
Asset 
Management Pte Ltd 
ZHANG Wei  
N/A 
 
To the best of the knowledge of HTCI and after making all reasonable enquiries, the Huatai Ultimate Client is an independent third party of (i) the Company, the connected 
person or the associates thereof, and (ii) HTCI, HTFH and the companies which are members of the same group of HTCI. 
 
(4) HTFH PWM 
 
Private wealth management division of HTFH will place the order as a placee under the International Offering on behalf of its ultimate clients (“HTFH Ultimate Clients”) 
on a non-discretionary basis.  
 
The details of the HTFH Ultimate Clients are as follow: 
 
Name  
Fund Manager 
UBO of Fund Manager 
Limited 
Partner/Shareholding 
holding 30% or more in the HTFH 
Ultimate Clients 
Foresight Vanguard Investment Limited
 
 
 
 
N/A 
N/A 
CUI SHUAI 
Sunwoda 
Treasury, 
a 
Cornerstone 
Investor of the Company 
N/A 
N/A 
Sunwoda Treasury is wholly owned by 
Sunwoda Electronic Co., Ltd. (欣旺達
電 子股份有限公司) (“Sunwoda 
Electronic”), a company established 
in the PRC in 1997, shares of which 
have been listed on the Shenzhen Stock 
Exchange (stock code: 300207) since 
2011 and the GDRs of which have been 
listed on the SIX Swiss Exchange 
(Symbol: SWD) since 2022. As of the 

<<<PAGE 24>>>
 
 
Latest Practicable Date, there was no 
single 
shareholder 
who 
has 
a 
beneficial ownership interest of 30% 
or more in Sunwoda Electronic. 
 
To the best of knowledge of HTFH and after making all reasonable enquiries, HTFH Ultimate Clients, together with each of their ultimate beneficial owners, is an independent 
third party of the Company, its subsidiaries, its substantial shareholders, HTFH and the companies which are members of the same group of HTFH.  

<<<PAGE 25>>>
 
 
 
DISCLAIMERS 
 
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
and Hong Kong Securities Clearing Company Limited take no responsibility for the contents 
of this announcement, make no representation as to its accuracy or completeness and 
expressly disclaim any liability whatsoever for any loss howsoever arising from or in reliance 
upon the whole or any part of the contents of this announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or 
into the United States (including its territories and possessions, any state of the United States 
and the District of Columbia). This announcement does not constitute or form a part of any 
offer to sell or solicitation to purchase or subscribe for securities in the United States or in 
any other jurisdictions in which such offer or solicitation would be unlawful. The securities 
mentioned herein have not been, and will not be, registered under the United States 
Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or any state 
securities law of the United States. The securities may not be offered, sold, pledged or 
transferred within the United States or to, or for the account or benefit of U.S. persons (as 
defined in Regulation S under the U.S. Securities Act (“Regulation S”)), except in 
transactions exempt from, or not subject to, the registration requirements of the U.S. 
Securities Act. The Offer Shares may be offered, sold or delivered outside the United States 
to non-U.S. persons in offshore transactions in accordance with Regulation S. 
The Offer Shares are being offered and sold outside the United States in offshore transactions 
in reliance on Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated March 13, 2026 issued by NSING 
TECHNOLOGIES INC. for detailed information about the Global Offering described below 
before deciding whether or not to invest in the H Shares thereby being offered. 
*Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements – Hong Kong Public Offering – Hong Kong Underwriting 
Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. 
(Hong Kong time) on the Listing Date (which is currently expected to be on March 23, 2026). 
 
 
 

<<<PAGE 26>>>
 
 
PUBLIC FLOAT AND FREE FLOAT 
 
Rule 19A.13A(2) of the Listing Rules provides that, where a new applicant is a PRC issuer 
with other listed shares at the time of Listing, this will normally mean that the portion of H 
shares for which Listing is sought that are held by the public, at the time of Listing, must (a) 
represent at least 10% of the issuer’s total number of issued shares in the class to which H 
shares belong (excluding treasury shares); or (b) have an expected market value of not less than 
HK$3,000,000,000. The A Shares of the Company are listed on the ChiNext Market of the 
Shenzhen Stock Exchange. So far as the Directors are aware, all 95,000,000 H Shares to be 
issued pursuant to the Global Offering, representing approximately 14.01% of the total issued 
share capital immediately upon Listing (excluding the treasury shares), are expected to be held 
by the public, which is higher than the prescribed percentage of H Shares required to be held 
in public hands of 10% under Rule 19A.13A(2)(a) of the Listing Rules, thereby satisfying Rule 
19A.13A(2) of the Listing Rules. 
 
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not 
be counted towards the free float of the H Shares of the Company at the time of Listing. Based 
on the final Offer Price of HK$10.80 per H Share, the Company satisfies the free float 
requirement under Rule 19A.13C(2) of the Listing Rules. 
 
The Directors confirm that, immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public shareholders 
of the Company do not hold more than 50% of the H shares in public hands at the time of the 
Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be 
at least 300 Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the 
Listing Rules.  
 
COMMENCEMENT OF DEALINGS 
 
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Monday, 
March 23, 2026 (Hong Kong time), provided that the Global Offering has become 
unconditional and the right of termination described in the section headed “Underwriting – 
Underwriting Arrangements – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus has not been exercised. Investors who trade the H Shares on the basis of publicly 
available allocation details prior to the receipt of H Share certificates or prior to the H Share 
certificates becoming valid evidence of title do so entirely at their own risk. 
 
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Monday, 
March 23, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Monday, March 23, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 200 H Shares each, and the stock code of the H Shares 
will be 2701.  
 
By order of the Board  
Nsing Technologies Inc.  
Mr. Sun Yingtong 
Chairman of the Board and executive director 

<<<PAGE 27>>>
 
 
 
Hong Kong, March 20, 2026 
 
As at the date of this announcement, the Board comprises: (i) Mr. Sun Yingtong, Mr. 
Kan Yulun and Ms. Ye Yantao as executive directors; (ii) Mr. Zhou Bin as the non-
executive director and (iii) Mr. Chen Weiwu, Ms. Hao Dan and Ms. Ji Xingdan as 
independent non-executive directors. 
