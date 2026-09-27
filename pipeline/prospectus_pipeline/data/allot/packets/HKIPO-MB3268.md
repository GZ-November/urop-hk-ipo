# 配发结果公告抽取任务：3268.HK MeiG Smart Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**09/03/2026 22:31**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0309/2026030901426.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3268.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Hong Kong 
Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility 
for the contents of this announcement, make no representation as to its accuracy or completeness and 
expressly disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole 
or any part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings 
as those defined in the prospectus dated February 27, 2026 (the “Prospectus”) issued by MeiG Smart 
Technology Co., Ltd. (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities of the Company. This announcement is not a prospectus. Potential 
investors should read the Prospectus for detailed information about the Company and the Global Offering 
described below before deciding whether or not to invest in the Offer Shares. Any investment decision in 
relation to the Offer Shares should be taken solely in reliance on the information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not, and is not intended to, constitute or form a part of any offer to sell or 
solicitation to purchase or subscribe for any securities in the United States or in any other jurisdiction. The 
Offer Shares have not been, and will not be, registered under the U.S. Securities Act of 1933, as amended 
from time to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the 
United States and may not be offered, sold, pledged or otherwise transferred within the United States, except 
pursuant to an available exemption from, or in a transaction not subject to, the registration requirements 
of the U.S. Securities Act and in compliance with any applicable state securities laws. The Offer Shares are 
being offered and sold outside the United States in offshore transactions in reliance on Regulation S under 
the U.S. Securities Act.
Potential investors of the Offer Shares should note that the Sole Sponsor and Sponsor-Overall Coordinator 
(for itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section 
headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — 
Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing 
Date (which is currently expected to be on Tuesday, March 10, 2026).

<<<PAGE 2>>>
– 2 –
MeiG Smart Technology Co., Ltd.
美格智能技術股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the
Global Offering
:
40,250,000 H Shares (taking into account 
the full exercise of the Offer Size 
Adjustment Option)
Number of Hong Kong Offer Shares
:
3,500,000 H Shares
Number of International Offer Shares
:
36,750,000 H Shares (taking into account 
the full exercise of the Offer Size 
Adjustment Option)
Final Offer Price
:
HK$28.86 per H Share, plus brokerage 
of 1%, SFC transaction levy of 
0.0027%, Stock Exchange trading fee 
of 0.00565% and AFRC transaction 
levy of 0.00015% (payable in full on 
application in Hong Kong dollars and 
subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
3268
Sole Sponsor, Sponsor-Overall Coordinator, Joint Global Coordinator,  
Joint Bookrunner and Joint Lead Manager
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and  
Joint Lead Manager
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
– 3 –
MEIG SMART TECHNOLOGY CO., LTD.
美格智能技術股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE
AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have 
the same meanings as those defined in the prospectus dated February 27, 2026 (the 
“Prospectus”) issued by MeiG Smart Technology Co., Ltd. (the “Company”)
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, H Shareholders and prospective investors should be aware that the 
price of the H Shares could move substantially even with a small number of H Shares 
traded and should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
3268
Stock short name
MEIG
Dealings commencement date
March 10, 2026*
*  see note at the end of the announcement
Price information
Final offer price
HK$28.86
Maximum offer price
HK$28.86
Offer price adjustment exercised
N/A
Offer Shares and Share Capital
Number of Offer Shares (taking into account the full 
exercise of the Offer Size Adjustment Option)
40,250,000
Number of Offer Shares in Hong Kong Public Offering
3,500,000
Number of Offer Shares in International Offering 
(taking into account the full exercise of the Offer Size 
Adjustment Option)
36,750,000
Number of issued Shares upon Listing
302,006,700

<<<PAGE 4>>>
– 4 –
The number of Offer Shares above is determined after taking into account the additional Offer Shares 
issued under the following Offer Size Adjustment Option.
Offer Size Adjustment Option (Upsize option)
Number of additional shares issued under the option
5,250,000
— Hong Kong Public Offering
N/A
— International Offering
5,250,000
The Offer Size Adjustment Option has been exercised in full, pursuant to which the Company is issuing 
and allotting 5,250,000 additional Offer Shares, representing approximately 15.00% of the total number of 
Offer Shares initially available under the Global Offering, at the final Offer Price.
Proceeds
Gross proceeds (Note)
HK$1,161.6 million
Less: Estimated listing expenses payable based on Final 
Offer Price
HK$70.8 million
Net proceeds
HK$1,090.8 million
Note:	Gross proceeds refers to the amount to which the Company is entitled to receive. For details of 
the use of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the 
Prospectus.

<<<PAGE 5>>>
– 5 –
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
57,965
No. of successful applications
15,506
Subscription level
174.12 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong 
Kong Public Offering
3,500,000
No. of Offer Shares reallocated from the International 
Offering
N/A
Final no. of Offer Shares under the Hong Kong Public 
Offering
3,500,000
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering
8.70%
Note:	For details of the final allocation of H Shares to the Hong Kong Public Offering, investors 
can refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
69
Subscription Level
4.50 times
No. of Offer Shares initially available under the 
International Offering
31,500,000
No. of Offer Shares reallocated to the Hong Kong Public 
Offering
N/A
Final no. of Offer Shares under the International Offering 
(taking into account the full exercise of the Offer Size 
Adjustment Option)
36,750,000
% of Offer Shares under the International Offering to the 
Global Offering (taking into account the full exercise of 
the Offer Size Adjustment Option)
91.30%

<<<PAGE 6>>>
– 6 –
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) 
a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted 
by the Stock Exchange to permit Offer Shares in the International Offering to be placed to 
certain Existing Minority Shareholders and/or their close associates; (b) a consent under 
paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants to permit the Company to allocate certain Offer Shares in the International 
Offering to connected clients; and (c) a consent under paragraph 18 of Chapter 4.15 
of the Guide for New Listing Applicants to permit the Company to, among other things, 
allocate further Offer Shares in the International Offering to a Cornerstone Investor and/
or its close associates, (i) none of the Offer Shares subscribed by the placees and the 
public have been financed directly or indirectly by the Company, any of the Directors, 
supervisors of the Company, chief executive of the Company, controlling Shareholders, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries 
or their respective close associates; and (ii) none of the placees and the public who have 
purchased the Offer Shares are accustomed to taking instructions from the Company, any 
of the Directors, supervisors of the Company, chief executive of the Company, controlling 
Shareholders, substantial Shareholders, existing Shareholders of the Company or any of 
its subsidiaries or their respective close associates in relation to the acquisition, disposal, 
voting or other disposition of H Shares registered in his/her/its name or otherwise held by 
him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of Offer 
Shares 
allocated
% of total 
issued H Shares 
immediately 
following 
completion 
of the Global 
Offering(1)(2)(3)
% of total 
issued share 
capital 
immediately 
following 
completion 
of the Global 
Offering(1)(2)(3)
Existing shareholders or 
their close associates
Baoyue Lake Shenzhen Industrial 
Investment Win-Win Enterprise 
Management Limited (寶月湖深產
投共贏企業管理有限公司)  
(“Baoyue Win-Win”)
7,726,900
19.20%
2.56%
No
Meiko Elec. Hong Kong Co., Limited 
(“Meiko HK”)
1,354,100
3.36%
0.45%
No

<<<PAGE 7>>>
– 7 –
Investor
No. of Offer 
Shares 
allocated
% of total 
issued H Shares 
immediately 
following 
completion 
of the Global 
Offering(1)(2)(3)
% of total 
issued share 
capital 
immediately 
following 
completion 
of the Global 
Offering(1)(2)(3)
Existing shareholders or 
their close associates
Streamax Electronics Limited (銳
明電子有限公司) (“Streamax 
Electronics”)
1,083,300
2.69%
0.36%
No
Harvest International Premium Value 
(Secondary Market) Fund SPC 
on behalf of Harvest Oriental SP 
(“Harvest”)
1,732,500
4.30%
0.57%
No
Jinyi Capital Multi-Strategy Fund SPC 
Ltd. (“JinYi Capital”)
406,200
1.01%
0.13%
No
Open Wealth Management Limited  
(開盤財富管理有限公司)  
(“Open Wealth”)
1,039,500
2.58%
0.34%
No
China Winning Limited  
(“China Winning”)
812,400
2.02%
0.27%
No
Chau Tsang Cheong (周增昌)  
(“Mr. Chau”)
1,732,500
4.30%
0.57%
No
Subtotal
15,887,400
39.47%
5.26%
—
Notes:
(1)	
Taking into account the full exercise of the Offer Size Adjustment Option.
(2)	
Only taking into account the H Shares allocated to the relevant investors as cornerstone investors 
under the Global Offering. In addition to the Offer Shares subscribed for as Cornerstone Investors, 
a close associate of China Winning was allocated further Offer Shares as placee in the International 
Offering. Please refer to the section headed “Allotment Results Details — International Offering 
— Allotees with waivers/consents obtained” in this announcement for details. Only the Offer 
Shares subscribed for as Cornerstone Investors are subject to lock-up as indicated below. For 
details, please refer to the section headed “Lock-up Undertakings — Cornerstone Investors” in this 
announcement.
(3)	
Discrepancies in the above table between the sum of the percentage of Offer Shares allocated to 
each investor and the percentage of the total Offer Shares allocated to such investors are due to 
rounding.

<<<PAGE 8>>>
– 8 –
Allottees with waivers/consents obtained
Investor
No. of Offer 
Shares 
allocated
% of total 
issued 
H Shares 
immediately 
following 
completion 
of the Global 
Offering(1)(6)
% of total 
issued share 
capital 
immediately 
following 
completion 
of the Global 
Offering(1)
Relationship
Allotees with a consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to connected clients
CICC Financial Trading Limited 
(“CICC FT”)
762,000
1.89%
0.25%
A connected client of China 
International Capital 
Corporation Hong Kong 
Securities Limited 
(“CICC”)
Bosera Asset Management 
(International) Co., Ltd (“Bosera 
AM”)
1,291,500
3.21%
0.43%
A connected client of China 
Merchants Securities 
(HK) Co., Limited 
(“CMS”)
Huatai Capital Investment Limited 
(“HTCI”)
1,501,000
3.73%
0.50%
A connected client of 
Huatai Financial 
Holdings (Hong Kong) 
Limited (“HTFH”)
Allotees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocation of 
further H Shares to a Cornerstone Investor and/or its close associate(3)
China Winning Limited (“China 
Winning HK”)
804,000
2.00%
0.27%
A close associate of a 
Cornerstone Investor(4)
Notes:
(1)	
Taking into account the full exercise of the Offer Size Adjustment Option.
(2)	
For details of (i) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent 
under paragraph 1C(2) of the Placing Guidelines in relation to subscription for Offer Shares by an 
existing Shareholder or close associate of existing Shareholders, (ii) a consent under paragraph 
1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in 
relation to allocations to connected clients, and (iii) a consent under paragraph 18 of Chapter 4.15 
of the Guide for New Listing Applicants in relation to allocation of Offer Shares to a Cornerstone 
Investor and/or its close associates, please refer to the section headed “Others/Additional 
Information” in this announcement.

<<<PAGE 9>>>
– 9 –
(3)	
The number of Offer Shares allocated to the relevant investor listed in this subsection only represents 
the number of Offer Shares allocated to the relevant investor as placee in the International Offering. 
For allocation of Offer Shares to the relevant investor as Cornerstone Investor, please refer to the 
section headed “Allotment Results Details — International Offering — Cornerstone Investors” in 
this announcement.
(4)	
China Winning HK is a close associate of China Winning, which is a Cornerstone Investor.
(5)	
Only taking account the H Shares allocated to the relevant investors under the Global Offering.
(6)	
The number of H Shares immediately following the Global Offering is the same as the number of 
Offer Shares to be issued under the Global Offering.
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number and 
description 
of Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued H 
Shares 
immediately 
upon the 
Global 
Offering 
subject to 
lock-up 
undertakings 
upon 
Listing(1)(2)
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon 
Listing(1)
Last day subject to the 
lock-up undertakings (3)
Mr. WANG Ping
102,417,560 
A Shares
—
33.91%
September 9, 2026 (First 
Six-month Period) (3)
March 9, 2027 (Second 
Six-month Period) (4)
ZhaoGe Investment
26,248,240 
A Shares
—
8.69%
September 9, 2026 (First 
Six-month Period) (3)
March 9, 2027 (Second 
Six-month Period) (4)
Subtotal
128,665,800 
A Shares
—
42.60%
—

<<<PAGE 10>>>
– 10 –
Notes:
1.	
Taking into account the full exercise of the Offer Size Adjustment Option.
2.	
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering.
3.	
In accordance with the applicable Listing Rules, the required lock-up for the first six-month period 
will end on September 9, 2026 and for the second six-month period will end on March 9, 2027.
4.	
The Controlling Shareholders may dispose of or transfer Shares after the indicated date subject to 
that each of the Controlling Shareholders will not cease to be a Controlling Shareholder.
5.	
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares 
after the indicated date.
6.	
For illustrative purposes only, this subsection lists only those members of the Controlling 
Shareholders who hold Shares directly in the Company. Pursuant to Rule 10.07 of the Listing 
Rules, each of the Controlling Shareholders (namely, Mr. WANG Ping and ZhaoGe Investment) has 
undertaken to the Company and the Stock Exchange that, except pursuant to the Global Offering, 
he/it shall, and shall procure that the relevant registered holders of the Shares in which he/it is 
beneficially interested shall, comply with the applicable lock-up requirements. For further details, 
please refer to the section headed “Underwriting — Underwriting Arrangements and Expenses — 
Undertakings to the Hong Kong Stock Exchange pursuant to the Listing Rules” in the Prospectus.

<<<PAGE 11>>>
– 11 –
Cornerstone Investors
Name
Number and 
description of 
Shares held in 
the Company 
subject 
to lockup 
undertakings 
upon Listing
% of total 
issued H 
Shares after the 
Global Offering 
subject to 
lock-up 
undertakings 
upon 
Listing(1)(2)
% of 
shareholding in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing(1)
Last day subject to the lock-up 
undertakings(3)
Baoyue Win-Win
7,726,900 
H Shares
19.20%
2.56%
September 9, 2026
Meiko HK
1,354,100 
H Shares
3.36%
0.45%
September 9, 2026
Streamax Electronics
1,083,300 
H Shares
2.69%
0.36%
September 9, 2026
Harvest
1,732,500 
H Shares
4.30%
0.57%
September 9, 2026
JinYi Capital
406,200 
H Shares
1.01%
0.13%
September 9, 2026
Open Wealth
1,039,500 
H Shares
2.58%
0.34%
September 9, 2026
China Winning
812,400 
H Shares
2.02%
0.27%
September 9, 2026
Mr. Chau
1,732,500 
H Shares
4.30%
0.57%
September 9, 2026
Subtotal
15,887,400 
H Shares
39.47%
5.26%
—

<<<PAGE 12>>>
– 12 –
Notes:
1.	
Taking into account the full exercise of the Offer Size Adjustment Option.
2.	
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering.
3.	
In accordance with the relevant cornerstone investment agreements, the required lockup ends on 
September 9, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or 
transferring H Shares subscribed for pursuant to the relevant cornerstone investment agreements 
after the indicated date. For details, please refer to the section headed “Cornerstone Investors — 
Restrictions on the Cornerstone Investors” of the Prospectus.
4.	
Discrepancies in the above table between the sum of the percentage of Shares held by each investor 
and the percentage of the total Shares held by such investors are due to rounding.
PLACEE CONCENTRATION ANALYSIS1
Placees2
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
7,726,900
21.03%
19.20%
7,726,900
7,726,900
2.56%
Top 5
16,230,400
44.16%
40.32%
16,230,400
16,230,400
5.37%
Top 10
23,522,500
64.01%
58.44%
23,522,500
23,522,500
7.79%
Top 25
32,969,200
89.71%
81.91%
32,969,200
32,969,200
10.92%
Notes:
1.	
Taking into account the full exercise of the Offer Size Adjustment Option.
2.	
Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 13>>>
– 13 –
H SHAREHOLDERS CONCENTRATION ANALYSIS1
H Shareholders2
Number of 
H Shares 
allotted
Allotment 
as % of the 
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
capital 
upon 
Listing
Top 1
7,726,900
21.03%
19.20%
7,726,900
7,726,900
2.56%
Top 5
16,230,400
44.16%
40.32%
16,230,400
16,230,400
5.37%
Top 10
23,522,500
64.01%
58.44%
23,522,500
23,522,500
7.79%
Top 25
32,969,200
89.71%
81.91%
32,969,200
32,969,200
10.92%
Notes:
1.	
Taking into account the full exercise of the Offer Size Adjustment Option.
2.	
Ranking of H Shareholders is based on the number of H Shares held by H Shareholders upon Listing. 
SHAREHOLDER CONCENTRATION ANALYSIS1
Shareholders2
Number of 
H Shares 
allotted
Allotment 
as % of the 
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
capital 
upon 
Listing
Top 1
0
0.00%
0.00%
0
128,665,800
42.60%
Top 5
10,364,400
28.20%
25.75%
10,364,400
155,593,827
51.52%
Top 10
17,906,400
48.72%
44.49%
17,906,400
164,884,227
54.60%
Top 25
30,479,800
82.94%
75.73%
30,479,800
179,768,511
59.52%
Notes:
1.	
Taking into account the full exercise of the Offer Size Adjustment Option.
2.	
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders 
upon Listing.

<<<PAGE 14>>>
– 14 –
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications 
made by the public will be conditionally allocated on the basis set out below:
POOL A
NO. OF OFFER 
SHARES 
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
23,828
1,191 out of 23,828 to receive 100 Shares
5.00%
200
4,687
412 out of 4,687 to receive 100 Shares
4.40%
300
9,033
1,165 out of 9,033 to receive 100 Shares
4.30%
400
1,421
239 out of 1,421 to receive 100 Shares
4.20%
500
1,699
348 out of 1,699 to receive 100 Shares
4.10%
600
585
140 out of 585 to receive 100 Shares
3.99%
700
554
151 out of 554 to receive 100 Shares
3.89%
800
432
131 out of 432 to receive 100 Shares
3.79%
900
349
116 out of 349 to receive 100 Shares
3.69%
1,000
3,404
1,225 out of 3,404 to receive 100 Shares
3.60%
1,500
1,553
815 out of 1,553 to receive 100 Shares
3.50%
2,000
1,046
690 out of 1,046 to receive 100 Shares
3.30%
2,500
406
305 out of 406 to receive 100 Shares
3.00%
3,000
745
581 out of 745 to receive 100 Shares
2.60%
3,500
412
361 out of 412 to receive 100 Shares
2.50%
4,000
323
284 out of 323 to receive 100 Shares
2.20%
4,500
177
159 out of 177 to receive 100 Shares
2.00%
5,000
652
587 out of 652 to receive 100 Shares
1.80%
6,000
351
326 out of 351 to receive 100 Shares
1.55%
7,000
290
274 out of 290 to receive 100 Shares
1.35%
8,000
256
246 out of 256 to receive 100 Shares
1.20%
9,000
210
208 out of 210 to receive 100 Shares
1.10%
10,000
1,525
100 Shares
1.00%
20,000
844
100 Shares plus 188 out of 844 to receive additional 100 Shares
0.61%
30,000
424
100 Shares plus 212 out of 424 to receive additional 100 Shares
0.50%
40,000
297
100 Shares plus 178 out of 297 to receive additional 100 Shares
0.40%
50,000
263
100 Shares plus 175 out of 263 to receive additional 100 Shares
0.33%
60,000
173
200 Shares
0.33%
70,000
138
200 Shares plus 33 out of 138 to receive additional 100 Shares
0.32%
80,000
112
200 Shares plus 54 out of 112 to receive additional 100 Shares
0.31%
90,000
83
200 Shares plus 58 out of 83 to receive additional 100 Shares
0.30%
100,000
761
300 Shares
0.30%
 
Total
57,033
Total number of Pool A successful applicants:
14,574
 

<<<PAGE 15>>>
– 15 –
POOL B
NO. OF OFFER 
SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF OFFER 
SHARES 
APPLIED FOR
200,000
565
1,000 Shares plus 70 out of 565 to receive additional 100 Shares
0.51%
300,000
107
1,400 Shares
0.47%
400,000
61
1,800 Shares
0.45%
500,000
31
2,200 Shares
0.44%
600,000
15
2,600 Shares
0.43%
700,000
14
3,000 Shares
0.43%
800,000
18
3,400 Shares
0.43%
900,000
5
3,800 Shares
0.42%
1,000,000
36
4,200 Shares
0.42%
1,250,000
7
5,200 Shares
0.42%
1,500,000
12
6,200 Shares
0.41%
1,750,000
61
7,000 Shares
0.40%
 
Total
932
Total number of Pool B successful applicants:
932
 
As of the date of this announcement, the relevant subscription monies previously deposited 
in the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in 
respect of which consent has been obtained, the Company has complied with the Listing 
Rules and guidance materials in relation to the placing, allotment and listing of the H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by 
the placees or the public (as the case may be) directly or indirectly for each Offer Share 
subscribed for or purchased by them is the same as the Offer Price in addition to any 
brokerage, AFRC transaction levy, SFC transaction levy and Stock Exchange trading fee 
payable.

<<<PAGE 16>>>
– 16 –
OTHERS/ADDITIONAL INFORMATION
Offer Size Adjustment Option
The Offer Size Adjustment Option has been exercised by the Overall Coordinators in full, 
pursuant to which the Company is issuing and allotting 5,250,000 additional H Shares, 
representing approximately 15.00% of the total number of H Shares initially available 
under the Global Offering, at the Offer Price. All of the additional Offer Shares that would 
be allotted and issued by the Company pursuant to the full exercise of the Offer Size 
Adjustment Option will be allocated to the International Offering. Accordingly, the total 
number of Offer Shares finally available under the Global Offering (after taking into account 
the full exercise of the Offer Size Adjustment Option) that would be allotted and issued by 
the Company is 40,250,000 Offer Shares and the total issued share capital of the Company 
upon Listing (after taking into account the full exercise of the Offer Size Adjustment 
Option) will be 302,006,700 Shares.
Allocation of H Shares to Existing Minority Shareholders and/or their close associates
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted to 
the Company, a waiver from strict compliance with the requirements under Rule 10.04 and 
consent under Paragraph 1C(2) of Appendix F1 to the Listing Rules to permit H Shares in 
the International Offering to be placed to certain existing minority Shareholders who (i) hold 
less than 5% of the total voting rights in the Company prior to the completion of the Global 
Offering and (ii) are not and will not become (upon the completion of the Global Offering) 
core connected persons of the Company or the close associates of any such core connected 
person (together, the “Existing Minority Shareholders”) and/or their close associates, 
subject to the conditions as follows:
(a)	
each Existing Minority Shareholder to whom the Company may allocate the H 
Shares in the International Offering holds less than 5% of the total voting rights in the 
Company before Listing;
(b)	 each Existing Minority Shareholder is not, and will not be, a core connected person of 
the Company or any close associate of any such core connected person immediately 
prior to or following the Global Offering;
(c)	
none of the Existing Minority Shareholders has the right to appoint a Director and/or 
have any other special rights;
(d)	 allocation to the Existing Minority Shareholders or their close associates will not affect 
the Company’s ability to satisfy the public float requirement as prescribed by the Stock 
Exchange under Rule 19A.13A(2) of the Listing Rules or otherwise approved by the 
Stock Exchange;

<<<PAGE 17>>>
– 17 –
(e)	
the Sole Sponsor confirms the matters set out in (a) to (d) above and confirm to the 
Stock Exchange in writing that, to the best of their knowledge and belief, they have 
no reason to believe that any of the Existing Minority Shareholders or their close 
associates received any preferential treatment, or is in a position to exert influence 
on the Company to obtain actual or perceived preferential treatment in the allocation 
either as a cornerstone investor or as a placee by virtue of their relationship with 
the Company other than the preferential treatment of assured entitlement under a 
cornerstone investment following the principles set out in Chapter 4.15 of the Guide 
for New Listing Applicants, and details of the allocation to the Existing Minority 
Shareholders holding 1% or more of the issued share capital of the Company 
immediately prior to the completion of the Global Offering will be disclosed in the 
Prospectus and/or this announcement, as the case may be;
(f)	
the Company confirms to the Stock Exchange in writing that:
(i)	
in the case of participation as cornerstone investors, no preferential treatment 
has been, nor will be, given to the Existing Minority Shareholders or their close 
associates by virtue of their relationship with the Company, other than the 
preferential treatment of assured entitlement under a cornerstone investment 
following the principles set out in Chapter 4.15 of the Guide for New Listing 
Applicants, nor is the Existing Minority Shareholder in a position to exert 
influence on the Company to obtain actual or perceived preferential treatment, 
and the Existing Minority Shareholders or their close associates’ cornerstone 
investment agreements do not contain any material terms which are more 
favorable to the Existing Minority Shareholders or their close associates than 
those in other cornerstone investment agreements; or
(ii)	 in the case of participation as placees, no preferential treatment has been, nor 
will be, given to the Existing Minority Shareholders or their close associates, 
nor is the Existing Minority Shareholder in a position to exert influence on the 
Company to obtain actual or perceived preferential treatment, by virtue of their 
relationship with the Company in any allocation in the placing tranche;
(g)	 in the case of participation as placees, the Overall Coordinators will confirm to 
the Stock Exchange that, to the best of their knowledge and belief, no preferential 
treatment has been, nor will be, given to the Existing Minority Shareholders or their 
close associates by virtue of their relationship with the Company in any allocation 
in the placing tranche. Please refer to the section headed “Waivers and Exemptions 
— Allocation of H Shares to Existing Minority Shareholders and Their Close 
Associates” in the Prospectus for further details of the waiver and consent. Each 
of the Sole Sponsor and the Company has provided the required confirmations as 
elaborated in the Prospectus. In particular, as the Company’s A Shares are listed on 
the Shenzhen Stock Exchange since June 2017, the Company has a highly extensive 

<<<PAGE 18>>>
– 18 –
base of existing Shareholders and disclosure of details of allocations to all Existing 
Minority Shareholders and/or their respective close associates will not be meaningful 
to investors, the proposed disclosure threshold, i.e. condition (e) of the waiver 
and consent which provides that details of the allocation to the Existing Minority 
Shareholders and/or their respective close associates holding more than 1% of the 
issued share capital of the Company immediately prior to the completion of the Global 
Offering will be disclosed in this announcement, is appropriate. All allocations of 
Offer Shares to the Existing Minority Shareholders are in compliance with all the 
conditions under the waiver and consent granted by the Stock Exchange.
Placing to connected clients with prior consents under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of 
their connected distributors pursuant to the Placing Guidelines.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate 
such Offer Shares in the International Offering to certain connected clients of distributors. 
The allocation of Offer Shares to such connected clients is in compliance with all the 
conditions under the consent granted by the Stock Exchange. Details of the placement to 
connected clients are set out below:
No.
Connected  
distributor
Connected client
Relationship
Whether the 
connected 
clients will hold 
the beneficial 
interests of the 
Offer Shares on a 
non-discretionary 
basis or 
discretionary basis 
for independent 
third parties
Number 
of Offer 
Shares to 
be allocated 
to the 
connected 
client
Approximate 
% of Offer 
Shares 
allocated 
to the 
connected 
client(1)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering(1)
1.
CICC FT (2)
CICC
CICC FT is a member 
of the same group of 
companies as CICC.
Non-discretionary
762,000
1.89%
0.25%
2.
Bosera AM(3)
CMS
Bosera AM is a member 
of the same group of 
companies as CMS.
Discretionary
1,291,500
3.21%
0.43%
3.
HTCI(4)
HTFH
HTFH is a member of 
the same group of 
companies as HTCI.
Non-discretionary
1,501,000
3.73%
0.50%

<<<PAGE 19>>>
– 19 –
Notes:
(1)	
Taking into account the exercise of the Offer Size Adjustment Option.
(2)	
CICC FT and China International Capital Corporation Limited will enter into a series of cross border 
delta-one OTC swap transactions (the “OTC Swaps”) with each other and the ultimate clients (the 
“CICC FT Ultimate Clients”), pursuant to which CICC FT will hold the Offer Shares on a non-
discretionary basis to hedge the OTC Swaps while the economic risks and returns of the underlying 
Offer Shares are passed to the CICC FT Ultimate Clients, subject to customary fees and commissions. 
The OTC Swaps will be fully funded by the CICC FT Ultimate Clients. During the terms of the OTC 
Swaps, all economic returns of the Offer Shares subscribed by CICC FT will be passed to the CICC 
FT Ultimate Clients and all economic loss shall be borne by the CICC FT Ultimate Clients through 
the OTC Swaps, and CICC FT will not take part in any economic return or bear any economic loss in 
relation to the Offer Shares. The OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate 
Clients may request CICC FT to redeem it at their own discretions, upon which CICC FT shall dispose 
of the Offer Shares and settle OTC Swaps in cash in accordance with the terms and conditions of the 
OTC Swap. Despite that CICC FT will hold the legal title of the Offer Shares by itself, it will not 
exercise the voting rights attaching to the relevant Offer Shares during the terms of the OTC Swaps 
according to its internal policy. The CICC FT Ultimate Clients for purpose of this placee subscription 
include Hengde Yuanzheng Tianli No. 3 Private Equity Securities Investment Fund (恒德遠征添利3號
私募證券投資基金), Hengde Yuanzheng Jinxin No. 4 Private Equity Securities Investment Fund (恒
德遠征金信4號私募證券投資基金) and Hengde Jinze No. E49 Private Equity Securities Investment 
Fund (恒德金澤E49號私募證券投資基金) (collectively, “Hengde Funds”), which are managed by 
Beijing Hengde Times Private Equity Fund Management Co., Ltd. (北京恒德時代私募基金管理有
限公司) (“Beijing Hengde”), each of which is an independent third party of CICC FT, CICC and the 
companies which are members of the same group of companies as each of the Underwriters.
(3)	
Bosera AM will hold the Offer Shares in its capacity as the discretionary fund manager managing three 
sub-funds on behalf of its underlying clients (“Bosera AM Ultimate Clients”), namely:
(i)	
Bosera China New Opportunities Fund SP, with no ultimate beneficial owner holding 30% or 
more interest therein;
(ii)	
Bosera Growth Premium Global Equity Strategy Fund SP, the ultimate beneficial owner of 
which is Mr. Guo Feng (郭峰), holding 49.00% interest therein; and
(iii)	
Bosera Growth Premium Global Equity Strategy Fund SP 2, the ultimate beneficial owner of 
which is Guangdong Dongfang Precision Science & Technology Co., Ltd. (廣東東方精工科
技股份有限公司), the shares of which are listed on the Shenzhen Stock Exchange (stock code: 
2611), holding 47.42% therein.
To the best knowledge of Bosera AM after making all reasonable enquiries, no other ultimate 
beneficial owner holds 30% or more interest in each of the Bosera AM Ultimate Clients and each of 
Bosera AM Ultimate Clients is an independent third party of Bosera AM, CMS and the companies 
which are members of the same group of companies as each of the Underwriters.

<<<PAGE 20>>>
– 20 –
(4)	
HTCI proposes to subscribe for and hold the beneficial interest of the Offer Shares as a placee under 
the International Offering on behalf of its underlying onshore clients (“HTCI Ultimate Clients”), 
namely:
(i)	
Commando No. 003 Active Management Private Securities Investment Fund (康曼德003號主
動管理型私募證券投資基金), with no ultimate beneficial owner holding 30% or more interest 
therein;
(ii)	
Commando No. 111 Private Securities Investment Fund (康曼德111號私募證券投資基金), the 
ultimate beneficial owner holding 30% or more interest of which is Zhou Kun (周琨);
(iii)	
Commando Kangding No. 2 Active Management Private Securities Investment Fund (康曼德康
定2號主動管理型私募證券投資基金), with no ultimate beneficial owner holding 30% or more 
interest therein;
(iv)	
Xinhong Commando Ying Active Management Private Securities Investment Fund (信鴻康曼
楹德楹主動管理型私募證券投資基金), the ultimate beneficial owner holding 30% or more 
interest of which is Ding Ying (丁楹); and
(v)	
Commando Wagyu No. 1 Private Securities Investment Fund (康曼德和牛1號私募證券投資基
金), with no ultimate beneficial owner holding 30% or more interest therein.
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial 
public offerings (“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products 
issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading 
activities. In connection with such products, the licensed domestic securities firms, through their Hong 
Kong affiliates, may participate in Hong Kong IPOs either as placees or cornerstone investors (the 
“Cross-border Derivatives Trading Regime”).
Huatai Securities Co., Ltd. (“HTSC”), the A shares of which are listed on the Shanghai Stock 
Exchange (stock code: 601688), the H shares of which are listed on the Stock Exchange (stock 
code: 6886), and the global depositary receipts of which are listed on the London Stock Exchange 
(LON: HTSC), is one of the domestic securities firms licensed to undertake cross-border derivatives 
trading activities. HTSC entered into an ISDA agreement (the “ISDA Agreement”) with its indirectly 
wholly-owned subsidiary, HTCI, to set out the principal terms of any future total return swap between 
HTSC and HTCI.
HTFH is the Connected Distributor. Pursuant to the ISDA Agreement, HTCI, which intends to 
participate in the International Offering as a placee, will hold the beneficial interest of the Offer Shares 
on a non-discretionary basis as the single underlying holder under a back-to-back total return swap 
(the “HT Back-to-back TRS”) to be entered by HTCI in connection with Huatai TRS (as defined 
below) placed by and fully funded (i.e. with no financing provided by HTCI) by the HTCI Ultimate 
Clients, by which, HTCI will, subject to customary fees and commissions, pass the full economic 
exposure of the Offer Shares ultimately to the HTCI Ultimate Clients, which in effect, HTCI will hold 
the beneficial interest of the Offer Shares on behalf of the HTCI Ultimate Clients. HTFH and HTCI 
are indirectly wholly-owned subsidiaries of HTSC. Accordingly, HTCI is considered as a “connected 
clients” of Huatai pursuant to paragraph 1B(7) of the Placing Guidelines.

<<<PAGE 21>>>
– 21 –
Pursuant to the Cross-border Derivatives Trading Regime, the HTCI Ultimate Clients cannot directly 
subscribe for the Offer Shares but may invest in derivative products issued by domestic securities 
firms licenced to undertake cross-border derivatives trading activities, such as HTSC, with the Offer 
Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, the HTCI Ultimate 
Clients will, through its investment manager, place a total return swap order (the “Huatai TRS”) with 
HTSC in connection with the Company’s IPO and HTSC will place a HT Back-to-back TRS order to 
HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the HT Back-to-back 
TRS, HTCI participates in the Company’s IPO and subscribes for the Offer Shares through placing 
order with HTFH during the International Offering.
To the best knowledge of HTCI after making all reasonable enquiries, no other ultimate beneficial 
owner holds 30% or more interest in each of the HTCI Ultimate Clients and each of HTCI Ultimate 
Clients is an independent third party of HTCI, HTFH and the companies which are members of the 
same group of HTCI.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the HT Back-to-back TRS 
in connection with the Huatai TRS order placed by the HTCI Ultimate Clients. Pursuant to the 
terms of the contracts of the HT Back-to-back TRS and the Huatai TRS, during the tenor of the HT 
Back-to-back TRS and the Huatai TRS, subject to customary fees and commissions, all economic 
returns of the Offer Shares will be ultimately passed to the HTCI Ultimate Clients through the HT 
Back-to-back TRS and the Huatai TRS and all economic loss shall be ultimately borne by the HTCI 
Ultimate Clients. HTCI will not take any economic return or bear any economic loss in relation to the 
Offer Shares, save as customary fees and commissions.
Investment in the HT Back-to-back TRS and the Huatai TRS is similar to the investment in a qualified 
domestic institutional investor fund (“QDII”) in the way that the HTCI Ultimate Clients would reap 
all the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through 
the exchange rate exposure on both the notional value of the investment and the profit and loss of the 
investment. In contrast, the profit and loss of the HT Back-to-back TRS and the Huatai TRS factor into 
account the fluctuation in RMB exchange rate upon termination of the Huatai TRS by converting the 
profit and loss using the current exchange rate at the time of termination. As such, the HTCI Ultimate 
Clients would bear the exchange rate exposure of the profit and loss on settlement date.
The HTCI Ultimate Clients may exercise an early termination right to terminate the Huatai TRS at any 
time from the issue date of the Huatai TRS which should be on or after the date on which the Offer 
Shares are listed on the Stock Exchange at their own discretions. Upon the termination upon maturity 
or early termination of the Huatai TRS by the HTCI Ultimate Clients, HTCI will dispose the Offer 
Shares on the secondary market and the HTCI Ultimate Clients will receive a final settlement amount 
in cash in accordance with the terms and conditions of the HT Back-to-back TRS and the Huatai 
TRS which should have taken into account all the economic returns or economic loss in relation to 
the Offer Shares. If upon the maturity of the Huatai TRS, the HTCI Ultimate Clients intend to extend 
the investment period, subject to further agreement between HTSC and the relevant HTCI Ultimate 
Clients, the term of the Huatai TRS could be extended by way of a new issuance or a tenor extension. 
Accordingly, HTSC will extend the term of the HT Back-to-back TRS by way of a new issuance or a 
tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, 
and pass through the economic exposure to the HTCI Ultimate Clients, being onshore clients placing 
Huatai TRS orders with HTSC in connection with the IPO of the Company. HTCI will not exercise the 
voting rights of the Offer Shares during the tenor of the HT Back-to-back TRS.

<<<PAGE 22>>>
– 22 –
During the life of the Huatai TRS and HT Back-to-back TRS, HTCI may continue to hold the Offer 
Shares in its custodian account, or to hold some or all of the Offer Shares in a prime brokerage account 
for stock borrowing purposes, where HTCI will lend out its holding of underlying Offer Shares in the 
form of stock borrowing loans consistent with market practice to lower its finance costs, provided that 
HTCI has the ability to call back the Offer Shares on loan at any time in order to satisfy its obligations 
under the HT Back-to-back TRS to ensure the economic interests are ultimately passed to the HTCI 
Ultimate Clients.
Allocation of Offer Shares to a Cornerstone Investor and/or its close associates with a 
consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 
4.15 of the Guide for New Listing Applicants to permit the Company to allocate further 
Offer Shares in the International Offering to a Cornerstone Investor as placee, subject to the 
following conditions:
(a)	
the final offering size of the Global Offering will exceed the minimum offering size 
requirement of HK$1 billion;
(b)	 the Offer Shares allocated to all existing Shareholders (whether as Cornerstone 
Investors and/or as placees) as permitted under this exemption do not exceed 30% of 
the total number of Offer Shares;
(c)	
each of the Directors, chief executive of the Company and the Controlling Shareholders 
has confirmed that, no Offer Shares have been allocated to them or their respective 
close associates pursuant to the Size-based Exemption Conditions (as defined in the 
Guide for New Listing Applicants);
(d)	 allocation to the Size-based Exemption Participants will not affect the Company’s 
ability to satisfy the public float requirement under Rule 19A.13(2) of the Listing 
Rules; and
(e)	
the relevant information in respect of the Cornerstone Investor under the Size-based 
Exemption will be disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange. For details of the further allocations of Offer Shares to 
Cornerstone Investors, please refer to the section headed “Allotment Results Details — 
International Offering — Allotees with waivers/consents obtained” in this announcement.

<<<PAGE 23>>>
– 23 –
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
and Hong Kong Securities Clearing Company Limited take no responsibility for the 
contents of this announcement, make no representation as to its accuracy or completeness 
and expressly disclaim any liability whatsoever for any loss howsoever arising from or in 
reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in 
or into the United States (including its territories and possessions, any state of the United 
States and the District of Columbia). This announcement does not, and is not intended to, 
constitute or form a part of any offer to sell or solicitation to purchase or subscribe for 
any securities in the United States or in any other jurisdiction. The Offer Shares have not 
been, and will not be, registered under the U.S. Securities Act of 1933, as amended from 
time to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction 
of the United States and may not be offered, sold, pledged or otherwise transferred within 
the United States, except pursuant to an available exemption from, or in a transaction not 
subject to, the registration requirements of the U.S. Securities Act and in compliance with 
any applicable state securities laws. The Offer Shares are being offered and sold outside 
the United States in offshore transactions in reliance on Regulation S under the U.S. 
Securities Act.
This announcement is for information purposes only and does not constitute an 
invitation or offer to acquire, purchase or subscribe for securities of the Company. This 
announcement is not a prospectus. Potential investors should read the Prospectus for 
detailed information about the Company and the Global Offering described below before 
deciding whether or not to invest in the Offer Shares. Any investment decision in relation 
to the Offer Shares should be taken solely in reliance on the information provided in the 
Prospectus.
Potential investors of the Offer Shares should note that the Sole Sponsor and 
Sponsor-Overall Coordinator (for itself and on behalf of the Hong Kong Underwriters) 
shall be entitled to terminate the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting 
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds 
for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on 
the Listing Date (which is currently expected to be on Tuesday, March 10, 2026).

<<<PAGE 24>>>
– 24 –
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering (after taking into account the full 
exercise of the Offer Size Adjustment Option), the total number of the H Shares expected to 
be held by the public represents approximately 13.33% of the total issued share capital of the 
Company, which is higher than the prescribed percentage of H Shares required to be held in 
public hands of 10% under Rule 19A.13A(2)(a) of the Listing Rules, thereby satisfying Rule 
8.08(1) (as amended and replaced by Rule 19A.13A) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following 
the Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall 
not be counted towards the free float of the H Shares of the Company at the time of Listing. 
Based on the final Offer Price of HK$28.86 per H Share, the Company confirmed that it 
complies with the free float requirement under Rule 19A.13C(2)(b) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering: (i) 
the Shares will be held by at least 300 Shareholders at the time of Listing, in compliance 
with Rule 8.08(2) of the Listing Rules; (ii) the three largest public Shareholders will not hold 
more than 50% of the H Shares held in public hands at the time of Listing, in compliance 
with Rules 8.08(3) and 8.24 of the Listing Rules; (iii) no placee will, individually, be placed 
more than 10% of the enlarged issued share capital of the Company immediately after the 
Global Offering; and (iv) there will not be any new substantial Shareholder (as defined in 
the Listing Rules) immediately after the Global Offering.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, 
March 10, 2026 (Hong Kong time), provided that the Global Offering has become 
unconditional and the right of termination described in the section headed “Underwriting — 
Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus has not been exercised. Investors who trade the H Shares on 
the basis of publicly available allocation details prior to the receipt of H Share certificates or 
prior to the H Share certificates becoming valid evidence of title do so entirely at their own 
risk.

<<<PAGE 25>>>
– 25 –
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on 
Tuesday, March 10, 2026 (Hong Kong time), it is expected that dealings in the H Shares on 
the Stock Exchange will commence at 9:00 a.m. on Tuesday, March 10, 2026 (Hong Kong 
time). The H Shares will be traded in board lots of 100 H Shares each, and the stock code of 
the H Shares will be 3268.
By order of the Board
MeiG Smart Technology Co., Ltd.
Mr. WANG Ping
Chairman of the Board, Executive Director
and General Manager
Hong Kong, March 9, 2026
As of the date of this announcement, the directors and proposed directors of the Company: (i) Mr. WANG 
Ping, Mr. DU Guobin, Mr. XIA Youqing and Mr. HUANG Min as executive directors; and (ii) Mr. YANG 
Zheng, Dr. MA Lijun and Ms. LIU Jia as independent non-executive directors.
