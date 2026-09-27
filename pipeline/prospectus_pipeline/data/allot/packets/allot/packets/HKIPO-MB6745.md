# 配发结果公告抽取任务：6745.HK Befar Group Co., Ltd - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**09/07/2026 21:39**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0709/2026070901273.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6745.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for any securities. This announcement is not a prospectus. Potential investors should read the Prospectus 
for detailed information about the Global Offering before deciding whether or not to invest in the Offer Shares. Any 
investment decision in relation to the Offer Shares should be taken solely in reliance on the information provided in 
the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities in 
the United States or in any other jurisdiction. The Offer Shares have not been, and will not be, registered under the 
United States Securities Act of 1933, as amended from time to time (the “U.S. Securities Act”) or securities law of 
any state or other jurisdiction of the United States. The Offer Shares may not be offered, sold, pledged or otherwise 
transferred within the United States or to, or for the account or benefit of US persons (as defined in Regulation S), 
except in transactions exempt from, or not subject to, the registration requirements of the U.S. Securities Act. There 
will be no public offer of the Offer Shares in the United States. The Offer Shares may be offered, sold or delivered 
outside the United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out in 
the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not 
resident in Hong Kong.
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on behalf of the 
Hong Kong Underwriters) shall be entitled to terminate the Hong Kong Underwriting Agreement with immediate effect 
upon the occurrence of any of the events set out in the section headed “Underwriting — Underwriting Arrangements 
and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 
a.m. on the day that trading in the H Shares commences on the Stock Exchange.
No stabilizing manager will be appointed in connection with the Global Offering and no stabilization activities will be 
carried out in relation to the Global Offering.

<<<PAGE 2>>>
2
Befar Group Co., Ltd
濱化集團股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under
the Global Offering
:
352,126,000 H Shares
Number of Hong Kong Offer Shares
:
35,213,000 H Shares
Number of International Offer Shares
:
316,913,000 H Shares
Final Offer Price
:
HK$3.48 per H Share, plus brokerage of 
 1.0%, SFC transaction levy of 0.0027%, 
 AFRC transaction levy of 0.00015% and 
 Stock Exchange trading fee of 0.00565%
Nominal Value
:
RMB1.00 per H Share
Stock Code
:
06745
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators, 
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and 
Joint Lead Manager
Зࡋ⳪暲
@:9)
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunner and Joint Lead Manager

<<<PAGE 3>>>
3
Befar Group Co., Ltd
濱化集團股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated June 30, 2026 (the “Prospectus”) issued by 
Befar Group Co., Ltd (濱化集團股份有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could 
move substantially even with a small number of H Shares traded and should exercise extreme 
caution when dealing in the H Shares.
SUMMARY
Company Information
Stock code
06745
Stock short name
BEFAR GROUP
Dealings commencement date
July 10, 2026*
* See note at the end of this announcement.
Price Information
Final Offer Price
Final Offer Price
HK$3.48
HK$3.48
Offer Price Range
Offer Price Range
HK$3.05 – HK$3.59
HK$3.05 – HK$3.59
Offer Shares and Share Capital
Number of Offer Shares
Number of Offer Shares
352,126,000
352,126,000
Number of Offer Shares in the Hong Kong Public Offering
Number of Offer Shares in the Hong Kong Public Offering
35,213,000
35,213,000
Number of Offer Shares in the International Offering
Number of Offer Shares in the International Offering
316,913,000
316,913,000
Number of issued Shares upon Listing 
Number of issued Shares upon Listing (Note)
(Note)
2,408,962,276
2,408,962,276
Note: Including 61,450,726 A Shares held by the Company as treasury Shares.
Proceeds
Gross proceeds (Note)
HK$1,225.40 million
 Less: Estimated listing expenses payable based on Final Offer 
   Price
HK$(65.03) million
Net proceeds
HK$1,160.37 million
Note: Gross proceeds refer to the amount which the Company is entitled to receive. For details of the use of proceeds, 
please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.

<<<PAGE 4>>>
4
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
88,855
No. of successful applications
17,358
Subscription level
227.58 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong Public 
Offering
35,213,000
No. of Offer Shares reallocated from the International Offering
Nil
Final no. of Offer Shares under the Hong Kong Public Offering
35,213,000
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering
10%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can 
refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
110
Subscription level
4.26 times
No. of Offer Shares initially available under the International 
Offering
316,913,000
No. of Offer Shares reallocated to the Hong Kong Public Offering
Nil
Final no. of Offer Shares under the International Offering
316,913,000
% of Offer Shares under the International Offering to the Global 
Offering
90%

<<<PAGE 5>>>
5
The Directors confirm that, to the best of their knowledge, information and belief, save for 
allocations under (a) the waiver from strict compliance with Rule 10.04 of the Listing Rules and 
consent under paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) 
granted by the Stock Exchange to permit the Company to allocate Offer Shares in the International 
Offering to certain Existing Minority Shareholders and/or their close associates, and (b) the waiver 
from strict compliance with Rule 10.04 of the Listing Rules and the consent under paragraph 1C(2) 
of the Placing Guidelines pursuant to paragraph 18 of Chapter 4.15 of the Guide to permit the 
Company to allocate further Offer Shares in the International Offering to, among others, existing 
Shareholder(s) and/or its close associates, (i) none of the Offer Shares subscribed by the placees 
and the public have been financed directly or indirectly by the Company, any of the Directors, the 
President of the Company, Single Largest Shareholder Group, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates; and (ii) 
none of the placees and the public who have purchased the Offer Shares are accustomed to taking 
instructions from the Company, any of the Directors, the President of the Company, Single Largest 
Shareholder Group, substantial Shareholders, existing Shareholders of the Company or any of its 
subsidiaries or their respective close associates in relation to the acquisition, disposal, voting or 
other disposition of H Shares registered in his/her/its name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
Cornerstone Investor
No. of Offer 
Shares allocated
Approximate % 
of total issued H 
Shares after the 
Global Offering (1)
Approximate % 
of total issued 
Shares(2) after the 
Global Offering
Existing shareholders 
or their close associates
Beijing Yian and HTCI (in 
connection with the Beijing Yian 
OTC Swaps)
33,774,000
9.59
1.44
Each of HTCI and Beijing 
Yian is a close associate 
of an Existing Minority 
Shareholder.
Luhua Daosheng and HTCI 
(in connection with the Luhua 
Daosheng OTC Swaps)
13,509,000
3.84
0.58
HTCI is a close associate 
of an Existing Minority 
S h a r e h o l d e r ; L u h u a 
Daosheng is an independent 
third party.
Aurora SF (in connection with 
Binzhou Guotou Arrangement)
13,219,000
3.75
0.56
Aurora SF is not an Existing 
Minority Shareholder; 
however its ultimate client, 
Binzhou Guotou, is a close 
associate of an Existing 
Minority Shareholder.
China Hongqiao
16,887,000
4.80
0.72
No
Hyperion Venture
6,609,000
1.88
0.28
No
Tianto
22,516,000
6.39
0.96
No
Safewell
5,747,000
1.63
0.24
No
Total
112,261,000
31.88
4.78
–

<<<PAGE 6>>>
6
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be 
issued under the Global Offering.
(2) 
Not taking into account of the 61,450,726 A Shares being held as treasury Shares.
(3) 
In addition to the Offer Shares subscribed for as Cornerstone Investors, certain Cornerstone Investors and/or 
their respective close associates may have allocated further Offer Shares as placees in the International Offering. 
The number of Offer Shares set out above only include the Offer Shares allocated to them as Cornerstone 
Investors. Please refer to the section headed “Allotment Results Details — International Offering — Allottees 
with Waivers/Consents Obtained” in this announcement for details. Only the Offer Shares subscribed for as 
Cornerstone Investors are subject to lock-up as indicated below in the section headed “Lock-up Undertakings — 
Cornerstone Investors”.
Allottees with Waivers/Consents Obtained
Investors
No. of Offer 
Shares allocated
Approximate % 
of total issued H 
Shares after the 
Global Offering (1)
Approximate % 
of total issued 
Shares(2) after the 
Global Offering
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the 
Placing Guidelines in relation to subscription for H Shares by Existing Minority Shareholders and/or their close associates (3)
Aurora SF (in connection with 
Binzhou Guotou Arrangement)
13,219,000
3.75
0.56
Binzhou Guotou is a close 
associate of Binzhou Antai 
Holding Group Co., Ltd. (濱州安
泰控股集團有限公司), which is 
an Existing Minority Shareholder, 
holding approximately 2.06% 
of A Shares as of the date of the 
Prospectus.
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide in relation to allocations to 
connected clients
HTCI (in connection with the 
Beijing Yian OTC Swaps)
33,774,000
9.59
1.44
Please refer to the section headed 
“Others/Additional Information 
— Placing to connected clients 
with consent under paragraph 
1C(1) of the Placing Guidelines” 
in this announcement.
HTCI (in connection with the 
Luhua Daosheng OTC Swaps)
13,509,000
3.84
0.58
SSIF Asset Management SPC-
SSI & Affluence Capital 
IPO Strategy Opportunity 
Segregated Portfolio (“SSIF 
AM Portfolio”)
22,000
0.01
<0.01

<<<PAGE 7>>>
7
Investors
No. of Offer 
Shares allocated
Approximate % 
of total issued H 
Shares after the 
Global Offering (1)
Approximate % 
of total issued 
Shares(2) after the 
Global Offering
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the 
Placing Guidelines pursuant to paragraph 18 of Chapter 4.15 of the Guide in relation to allocations of further H Shares to 
Cornerstone Investor(s) and/or existing Shareholder(s) and/or their respective close associates (4)(5)
China Hongqiao
16,887,000
4.80
0.72
Cornerstone Investor
Tianto
22,516,000
6.39
0.96
Cornerstone Investor
Safewell
8,908,000
2.53
0.38
Cornerstone Investor
Hyperion Venture
5,161,000
1.47
0.22
Cornerstone Investor
Aurora SF (in connection 
with the Arrangement with 
Jinan Junhua Changhong 
Investment Partnership (Limited 
Partnership)* (濟南君化長
鴻投資合夥企業(有限合夥)) 
(“Junhua Changhong”))
31,596,000
8.97
1.35
Aurora SF is a Cornerstone Investor, 
however such investment was in 
connection with a different ultimate 
client. Junhua Changhong, is an 
independent third party and not an 
existing Shareholder or Cornerstone 
Investor.
Oversea-Chinese Banking 
Corporation Limited (“OCBC 
Singapore”)
3,774,000
1.07
0.16
O C B C S i n g a p o r e i s t h e 
intermediate swap provider in 
relation to the investment by 
Aurora SF in connection with 
the arrangement with Binzhou 
Guotou and Junhua Changhong.
Yu Xinwei (於新偉)
10,344,000
2.94
0.44
Ultimate beneficial owner 
(holding approximately 68.42% 
of its interest) of Beijing Yian, 
which is the Beijing Yian OTC 
Swaps’ ultimate client.

<<<PAGE 8>>>
8
Investors
No. of Offer 
Shares allocated
Approximate % 
of total issued H 
Shares after the 
Global Offering (1)
Approximate % 
of total issued 
Shares(2) after the 
Global Offering
Relationship
SinoPro Securities Limited — 
Client’s Account
13,218,000
3.75
0.56
M a n a g e d b y S i n o P r o 
Securities Limited on behalf 
of independent third-party 
underlying clients. SinoPro 
Securities Limited is indirectly 
owned as to approximately 
32.35% by Yu Xinwei.
SinoPro Global Opportunities 
Open-Ended Fund Company — 
SinoPro Global Opportunities 
Fund III (“SinoPro Fund III”)
2,183,000
0.62
0.09
SinoPro Fund III, whose underlying 
investors are independent 
third parties, is managed by 
SinoPro Securities Limited, 
which is indirectly owned as to 
approximately 32.35% by Yu 
Xinwei.
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be 
issued under the Global Offering.
(2) 
Not taking into account of the 61,450,726 A Shares being held as treasury Shares.
(3) 
Only allocations to Existing Minority Shareholders holding more than 1% of the issued share capital of the 
Company immediately prior to completion of the Global Offering and/or their close associates are disclosed 
herein.

<<<PAGE 9>>>
9
(4) 
For details of the waiver from strict compliance with Rule 10.04 of the Listing Rules and the consent under 
paragraph 1C(2) of the Placing Guideline pursuant to paragraph 18 of Chapter 4.15 of the Guide in relation 
to allocations of further H Shares to Cornerstone Investors and/or existing Shareholder and/or their respective 
close associates, please refer to the section headed “Others/Additional Information — Size-based Exemption” in 
this announcement.
(5) 
The number of Offer Shares allocated to the relevant investors indicated herein only represents the number of 
Offer Shares allocated to them as placees (other than as Cornerstone Investors) in the International Offering. For 
allocation of Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed 
“Allotment Results Details — International Offering — Cornerstone Investors” in this announcement.

<<<PAGE 10>>>
10
LOCK-UP UNDERTAKINGS
Cornerstone Investors
Name
Number of H Shares 
held subject to lock-
up undertakings upon 
Listing
Approximate % of 
total issued H Shares 
subject to lock-up 
undertakings upon 
Listing (1)
Approximate % of 
total issued Shares(2) 
subject to lock-up 
undertakings upon 
Listing
Last day subject to the 
lock-up undertakings (3)
Beijing Yian and HTCI (in connection with the 
Beijing Yian OTC Swaps)
33,774,000
9.59
1.44
January 9, 2027
Luhua Daosheng and HTCI (in connection with 
the Luhua Daosheng OTC Swaps)
13,509,000
3.84
0.58
January 9, 2027
Aurora SF (in connection with Binzhou Guotou 
Arrangement)
13,219,000
3.75
0.56
January 9, 2027
China Hongqiao
16,887,000
4.80
0.72
January 9, 2027
Hyperion Venture
6,609,000
1.88
0.28
January 9, 2027
Tianto
22,516,000
6.39
0.96
January 9, 2027
Safewell
5,747,000
1.63
0.24
January 9, 2027
Total
112,261,000
31.88
4.78
–
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be 
issued under the Global Offering.
(2) 
Not taking into account of the 61,450,726 A Shares being held as treasury Shares.
(3) 
Each of the Cornerstone Investors has agreed to a lock-up period of six months from and including the 
Listing Date. The lock-up period is expected to end on January 9, 2027, being six months after the expected 
Listing Date of July 10, 2026. In addition to the Offer Shares subscribed for as Cornerstone Investors, certain 
Cornerstone Investors and/or their respective close associates may have allocated further Offer Shares as placees 
in the International Offering. The number of Offer Shares set out above only include the Offer Shares allocated 
to them as Cornerstone Investors. Please refer to the section headed “Allotment Results Details — International 
Offering — Allottees with Waivers/Consents Obtained” in this announcement for details. Only the Offer Shares 
subscribed for as Cornerstone Investors are subject to lock-up as indicated in the table.

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
Shares 
held upon 
Listing
% of total 
issued share 
capital upon 
Listing
Top 1
59,519,000
18.78%
16.90%
71,637,700
3.05%
Top 5
188,350,000
59.43%
53.49%
200,468,700
8.54%
Top 10
246,866,000
77.90%
70.11%
258,984,700
11.03%
Top 25
301,469,000
95.13%
85.61%
313,587,700
13.36%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
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
% of total 
issued 
H Shares 
upon Listing
Number of 
Shares held 
upon Listing
Top 1
59,519,000
18.78%
16.90%
59,519,000
16.90%
71,637,700
Top 5
188,350,000
59.43%
53.49%
188,350,000
53.49%
200,468,700
Top 10
246,866,000
77.90%
70.11%
246,866,000
70.11%
258,984,700
Top 25
301,469,000
95.13%
85.61%
301,469,000
85.61%
313,587,700
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
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
% of total 
issued share 
capital upon 
Listing
Top 1
–
0.00%
0.00%
–
231,686,772
9.87%
Top 5
117,770,000
37.16%
33.45%
117,770,000
456,327,574
19.44%
Top 10
186,914,000
58.98%
53.08%
186,914,000
633,557,974
26.99%
Top 25
238,342,000
75.21%
67.69%
238,342,000
849,387,298
36.18%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders, upon 
Listing.

<<<PAGE 12>>>
12
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
No. of 
Shares
applied for
No. of 
valid
applications
Basis of allotment/ballot
Approximate
percentage 
allotted
of the total 
no. of Shares 
applied for
POOL A
1,000
31,717
1,586 out of 31,717 to receive 1,000 Shares
5.00%
2,000
20,958
1,549 out of 20,958 to receive 1,000 Shares
3.70%
3,000
2,645
246 out of 2,645 to receive 1,000 Shares
3.10%
4,000
1,224
134 out of 1,224 to receive 1,000 Shares
2.74%
5,000
1,656
205 out of 1,656 to receive 1,000 Shares
2.48%
6,000
942
129 out of 942 to receive 1,000 Shares
2.28%
7,000
781
117 out of 781 to receive 1,000 Shares
2.14%
8,000
772
125 out of 772 to receive 1,000 Shares
2.02%
9,000
426
73 out of 426 to receive 1,000 Shares
1.90%
10,000
10,102
1,849 out of 10,102 to receive 1,000 Shares
1.83%
15,000
923
212 out of 923 to receive 1,000 Shares
1.53%
20,000
852
230 out of 852 to receive 1,000 Shares
1.35%
25,000
2,923
897 out of 2,923 to receive 1,000 Shares
1.23%
30,000
771
262 out of 771 to receive 1,000 Shares
1.13%
35,000
360
133 out of 360 to receive 1,000 Shares
1.06%
40,000
439
176 out of 439 to receive 1,000 Shares
1.00%
45,000
296
126 out of 296 to receive 1,000 Shares
0.95%
50,000
877
398 out of 877 to receive 1,000 Shares
0.91%
60,000
609
306 out of 609 to receive 1,000 Shares
0.84%
70,000
498
273 out of 498 to receive 1,000 Shares
0.78%
80,000
476
281 out of 476 to receive 1,000 Shares
0.74%
90,000
264
171 out of 264 to receive 1,000 Shares
0.72%
100,000
1,547
1,083 out of 1,547 to receive 1,000 Shares
0.70%
200,000
994
1,000 Shares
0.50%
300,000
759
1,000 Shares plus 18 out of 759 to receive additional 
1,000 Shares
0.34%

<<<PAGE 13>>>
13
No. of 
Shares
applied for
No. of 
valid
applications
Basis of allotment/ballot
Approximate
percentage 
allotted
of the total 
no. of Shares 
applied for
400,000
543
1,000 Shares plus 174 out of 543 to receive 
additional 1,000 Shares
0.33%
500,000
1,615
1,000 Shares plus 1,065 out of 1,615 to receive 
additional 1,000 Shares
0.33%
1,000,000
939
2,000 Shares
0.20%
86,908
Total number of Pool A successful applicants: 15,411
POOL B
1,500,000
1,118
7,000 Shares
0.47%
2,000,000
303
8,000 Shares
0.40%
2,500,000
136
9,000 Shares
0.36%
3,000,000
144
10,000 Shares
0.33%
4,000,000
67
12,000 Shares
0.30%
5,000,000
49
14,000 Shares
0.28%
6,000,000
22
16,000 Shares
0.27%
7,000,000
20
18,000 Shares
0.26%
8,000,000
17
21,000 Shares
0.26%
9,000,000
10
22,000 Shares
0.24%
10,000,000
31
23,000 Shares
0.23%
17,606,000
30
40,000 Shares
0.23%
1,947
Total number of Pool B successful applicants: 1,947
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
OTHERS/ADDITIONAL INFORMATION
Allocation of H Shares to Existing Minority Shareholders and their close associates
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 
1C(2) of the Placing Guidelines to permit the Company to allocate Offer Shares in the International 
Offering to Existing Minority Shareholders and/or their close associates. For details, please refer 
to the section headed “Waivers — Allocation of H Shares to Existing Minority Shareholders and 
Their Close Associates” in the Prospectus and the section headed “Allotment Results Details — 
International Offering — Allottees with Waivers/Consents Obtained” in this announcement.

<<<PAGE 14>>>
14
Placing to connected clients with consent under paragraph 1C(1) of the Placing Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of certain 
distributors. The Company has applied to the Stock Exchange for, and the Stock Exchange has 
granted, the consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to 
allocate such Offer Shares in the International Offering to such connected clients. Details of the 
placement to connected clients are set out below.
No.
Connected 
Distributor
Connected 
Client
Relationship with the 
Connected Distributor
Whether 
collective 
investment 
scheme not 
authorised by 
the SFC
No. of Offer 
Shares
allocated
Approx. 
% of total 
Offer 
Shares
Approx. 
% of total 
issued 
Shares(1)
upon 
Listing
Connected clients holding beneficial interest in the Offer Shares on a non-discretionary basis on behalf of independent third parties
1
Huatai Financial 
Holdings (Hong 
Kong) Limited 
(“HTFH”)
HTCI (in connection 
with the Beijing Yian 
OTC Swaps)
HTCI and HTFH are members of 
the same group of companies. HTCI 
will hold the H Shares on a non-
discretionary basis to hedge the 
Beijing Yian OTC Swaps. See details 
of the Beijing Yian OTC Swaps in 
the Prospectus.
No
33,774,000
9.59
1.44
2
HTFH
HTCI (in connection 
with the Luhua Daosheng 
OTC Swaps)
HTCI and HTFH are members of 
the same group of companies. HTCI 
will hold the H Shares on a non-
discretionary basis to hedge the 
Luhua Daosheng OTC Swaps. See 
details of the Luhua Daosheng OTC 
Swaps in the Prospectus.
No
13,509,000
3.84
0.58
Connected client holding beneficial interest in the Offer Shares on a discretionary basis on behalf of independent third parties
3
Shanxi Securities 
I n t e r n a t i o n a l 
Limited (“SSI”)
SSIF AM Portfolio
SSIF AM Portfolio is managed by 
SSIF Asset Management SPC, which 
is controlled by Shanxi Securities 
International Asset Management 
Limited, a member of the same group 
of SSI, a distributor of the Global 
Offering.
No
22,000
0.01
<0.01
Notes:
(1) 
Not taking into account of the 61,450,726 A Shares being held as treasury Shares.

<<<PAGE 15>>>
15
Size-based Exemption
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, 
the waiver from strict compliance with Rule 10.04 of the Listing Rules and the consent under 
paragraph 1C(2) of the Placing Guidelines pursuant to paragraph 18 of Chapter 4.15 of the 
Guide for New Listing Applicants to permit the Company to allocate further Offer Shares in 
the International Offering to certain Cornerstone Investors and/or existing Shareholders and/
or their respective close associates (the “Relevant Placees”) as placees, subject to the following 
conditions:
(a) 
the final offer size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;
(b) 
Offer Shares allocated to all existing Shareholders and/or their close associates (whether as 
Cornerstone Investors and/or as placees) as permitted under this exemption do not exceed 
30% of the total number of Offer Shares;
(c) 
each Director and the President of the Company has confirmed that no securities have been 
allocated to them or their respective close associates under this exemption;
(d) 
the allocation to the Relevant Placees will not affect the Company’s ability to satisfy its 
public float requirement under Rule 8.08(1) (as amended and replaced by Rule 19A.13A) of 
the Listing Rules; and
(e) 
details of the allocation to the Relevant Placees under this exemption will be disclosed in this 
announcement.
For details of such allocations, please refer to the section headed “Allotment Results Details – 
International Offering – Allottees with Waivers/Consents Obtained” in this announcement.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or 
indirectly, provided by the Company, the Directors or syndicate members to any placees or the 
public (as the case may be) and the consideration payable by them for each H Share subscribed 
for or purchased by them is the same as the Final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and trading fee payable.

<<<PAGE 16>>>
16
PUBLIC FLOAT AND FREE FLOAT
Rule 19A.13A(2) of the Listing Rules provides that, for a new PRC issuer with other listed 
shares, the H Shares held by the public must either (a) be at least 10% of the total number of 
issued shares in the class of securities to which H Shares belong, excluding treasury shares; or 
(b) have an expected market value at the time of Listing of not less than HK$3,000,000,000. The 
A Shares of the Company are listed on the Shanghai Stock Exchange. So far as the Directors are 
aware, immediately after completion of the Global Offering, all of the 352,126,000 H Shares to 
be issued pursuant to the Global Offering, representing approximately 15.00% of the total issued 
Shares immediately upon Listing (excluding the 61,450,726 A Shares held as treasury Shares), are 
expected to be held by the public. Accordingly, the Company is expected to satisfy the public float 
requirement under Rule 19A.13A(2) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon Listing shall not be 
counted towards the free float of the H Shares of the Company at the time of Listing. Based on 
the Final Offer Price of HK$3.48 per H Share, the Company is expected to satisfy the free float 
requirement under Rule 19A.13C of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public shareholders of 
the Company do not hold more than 50% of the H shares in public hands at the time of the Listing 
in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 
Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. (Hong Kong time) 
on Friday, July 10, 2026, provided that the Global Offering has become unconditional and the right 
of termination described in the section headed “Underwriting — Underwriting Arrangements and 
Expenses — Hong Kong Public Offering — Grounds for termination” in the Prospectus has not 
been exercised. Investors who trade H Shares prior to the receipt of H Share certificates or the H 
Share certificates becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong Kong 
time) on Friday, July 10, 2026, it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Friday, July 10, 2026. The H Shares will be traded in board lots of 
1,000 H Shares each. The stock code of the H Shares is 06745.

<<<PAGE 17>>>
17
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for any securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated June 30, 2026 for detailed information about 
the Global Offering before deciding whether or not to invest in the Offer Shares. Any investment 
decision in relation to the Offer Shares should be taken solely in reliance on the information 
provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer or 
solicitation to purchase or subscribe for securities in the United States or in any other jurisdictions. 
The Offer Shares have not been, and will not be, registered under the United States Securities Act 
of 1933 as amended from time to time (the “U.S. Securities Act”) or securities law of any state 
or other jurisdiction of the United States. The Offer Shares may not be offered, sold, pledged or 
otherwise transferred within the United States, except pursuant to an available exemption from, or 
in a transaction not subject to, the registration requirements of the U.S. Securities Act. There will 
be no public offer of the Offer Shares in the United States. The Offer Shares are being offered and 
sold solely outside the United States in offshore transactions in reliance on Regulation S under the 
U.S. Securities Act.
* Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves 
and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out 
in the section headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong 
Public Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. on 
the day that trading in the H Shares commences on the Stock Exchange. For the arrangement in 
case of severe weather, please refer to “How to Apply for Hong Kong Offer Shares” section of the 
Prospectus.
By Order of the Board
Befar Group Co., Ltd
Mr. Yu Jiang
Chairman of the Board and Executive Director
Hong Kong, July 9, 2026
As of the date of this announcement, the Board comprises: (i) Mr. Yu Jiang, Mr. Dong 
Hongbo, Mr. Ren Yuanbin and Dr. Liu Hongan as executive Directors; (ii) Mr. Song Shuhua 
as non-executive Director; and (iii) Mr. Hao Yinping, Ms. Li Haixia and Mr. Wang Qian as 
independent non-executive Directors. In addition, Mr. Cao Chunmeng is a proposed independent 
non-executive Director.
