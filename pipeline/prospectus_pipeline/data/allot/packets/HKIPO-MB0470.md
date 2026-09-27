# 配发结果公告抽取任务：0470.HK WUXI LEAD INTELLIGENT EQUIPMENT CO., LTD. - H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**10/02/2026 22:25**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0210/2026021001338.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"0470.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
announcement does not, and is not intended to, constitute or form a part of any offer or solicitation to purchase or 
subscribe for securities in the United States or in any other jurisdiction. The Offer Shares have not been and will not 
be registered under the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities 
Act”) or securities law of any state or other jurisdiction of the United States and may not be offered, sold, pledged or 
otherwise transferred within the United States, except in transactions exempt from, or not subject to, the registration 
requirements of the U.S. Securities Act and in compliance with any applicable state securities laws. The Offer Shares 
are being offered and sold (i) within the United States solely to “Qualified Institutional Buyers” as defined in Rule 
144A pursuant to an exemption from registration under the U.S. Securities Act and (ii) outside the United States in 
offshore transactions in accordance with Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. Potential investors should read the Prospectus for detailed information about the Company 
and the Global Offering described below before deciding whether or not to invest in the Offer Shares.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated February 3, 2026 (the “Prospectus”) issued by Wuxi Lead Intelligent Equipment Co., 
Ltd. (無錫先導智能裝備股份有限公司) (the “Company”).
In connection with the Global Offering, J.P. Morgan Securities (Asia Pacific) Limited as stabilizing manager (the 
“Stabilization Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, the extent 
permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect 
transactions with a view to stabilizing or supporting the market price of the Shares at such price, in such amounts 
and in such manners as the Stabilizing Manager, its affiliates or any person acting for it may determine and at a 
level higher than that which might otherwise prevail for a limited period after the Listing Date. However, there is 
no obligation on the Stabilizing Manager (or its affiliates or any person acting for it) to conduct any such stabilizing 
action. Such stabilizing action, if taken, (a) will be conducted at the absolute discretion of the Stabilization Manager 
(or its affiliates or any person acting for it) and in what the Stabilizing Manager reasonably regards as the best interest 
of our Company, (b) may be discontinued at any time and (c) is required to be brought to an end within 30 days of the 
last day for lodging applications under the Hong Kong Public Offering, being Sunday, March 8, 2026. Such stabilizing 
action, if taken, may be effected in all jurisdictions where it is permissible to do so, in each case in compliance with 
all applicable laws, rules and regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules 
(Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter 
571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering. After this date, when no further 
stabilizing action may be taken, demand for the H Shares, and therefore the price of the H Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out 
in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/
or not resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint Sponsors and the 
Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate 
their obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of 
the events set out in the section headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong 
Public Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the 
Listing Date.

<<<PAGE 2>>>
2
WUXI LEAD INTELLIGENT EQUIPMENT CO., LTD.
無錫先導智能裝備股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under the
Global Offering
:
107,658,400 H Shares (taking into account  
the full exercise of the Offer Size  
Adjustment Option and subject to the  
Over-allotment Option)
Number of Hong Kong Offer Shares
:
9,361,600 H Shares
Number of International Offer Shares
:
98,296,800 H Shares (taking into account  
the full exercise of the Offer Size  
Adjustment Option and subject to  
the Over-allotment Option)
Offer Price
:
HK$45.80 per H Share, plus brokerage 
of 1.0%, SFC transaction levy 
of 0.0027%, Hong Kong Stock 
Exchange trading fee of 0.00565% and 
AFRC transaction levy of 0.00015% 
(payable in full on application in Hong 
Kong dollars and subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
0470
Joint Sponsors, Sponsor-Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
(in alphabetical order)
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
WUXI LEAD INTELLIGENT EQUIPMENT CO., LTD. 
無錫先導智能裝備股份有限公司 
ANNOUNCEMENT OF ALLOTMENT RESULTS 
 
Unless otherwise defined herein, capitalized terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated February 3, 2026 (the “Prospectus”) 
issued by WUXI LEAD INTELLIGENT EQUIPMENT CO., LTD. (無錫先導智能裝備股份有
限公司) (the “Company”).  
 
 
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, Shareholders and prospective investors should be aware that the price 
of the H Shares could move substantially even with a small number of H Shares traded 
and should exercise extreme caution when dealing in the H Shares. 
SUMMARY 
 
Company Information 
Stock Code 
0470 
Stock Short Name 
WUXI LEAD 
Dealings commencement date 
February 11, 2026* 
* see note at the end of the announcement 
 
Price Information 
Final Offer Price 
HK$45.80 
Maximum Offer Price 
HK$45.80 
Offer Price Adjustment exercised 
N/A 
 
Offer Shares and Share Capital 
Number of Offer Shares 
107,658,400 
Number of Offer Shares in Hong Kong 
Public Offering  
9,361,600 
Number of Offer Shares in International 
Offering (taking into account the full 
exercise of the Offer Size Adjustment 
Option) 
98,296,800 
Number of issued Shares upon Listing 
(before exercise of the Over-allotment 
Option) 
1,673,821,434 
The number of Offer Shares above is determined after taking into account the additional 
Offer Shares issued under the following Offer Size Adjustment Option. 
 
Offer Size Adjustment Option (Upsize option) 
Number of additional shares issued 
under the option 
14,042,400 

<<<PAGE 4>>>
- Hong Kong Public Offering 
N/A 
- International Offering 
14,042,400 
The Offer Size Adjustment Option has been exercised in full, pursuant to which the Company 
is issuing and allotting 14,042,400 additional Offer Shares, representing approximately 
15.00% of the total number of Offer Shares initially available under the Global Offering, at 
the final Offer Price. 
 
Over-allocation 
No. of Offer Shares over-allocated 
16,148,700 
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option 
is exercised, an announcement will be made on the Stock Exchange’s website. 
 
Proceeds 
Gross proceeds (Note) 
HK$4,930.8 million 
Less: Estimated 
listing 
expenses 
payable based on Final Offer 
Price 
HK$134.4 million  
Net Proceeds 
HK$4,796.4 million 
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For 
details of the use of proceeds, please refer to the section headed “Future Plans and Use of 
Proceeds” of the Prospectus. The Company will adjust the allocation of the net proceeds 
from the exercise of the Over-allotment Option (if any) for the purposes as set out in the 
section headed “Future Plans and Use of Proceeds” of the Prospectus on a pro rata basis.  
 
ALLOTMENT RESULTS DETAILS 
 
HONG KONG PUBLIC OFFERING 
 
 
No. of valid applications 
57,322 
No. of successful applications 
28,577 
Subscription level 
79.54 times 
Claw-back triggered 
N/A 
No. of Offer Shares initially available under the Hong Kong 
Public Offering 
9,361,600 
Final no. of Offer Shares under the Hong Kong Public 
Offering 
9,361,600 
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering (after taking into account the full 
exercise of the Offer Size Adjustment Option) 
8.7% 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, 
investors can refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification 

<<<PAGE 5>>>
number or www.eipo.com.hk/eIPOAllotment for the full list of allottees. 
 
INTERNATIONAL OFFERING  
 
 
No. of placees 
127 
Subscription Level (before taking into account the Offer Size 
Adjustment Option) 
10.47x 
No. of Offer Shares initially available under the International Offering 84,254,400 
Final no. of Offer Shares under the International Offering (after taking 
into account the full exercise of the Offer Size Adjustment Option) 
98,296,800 
% of Offer Shares under the International Offering to the Global 
Offering (after taking into account the full exercise of the Offer Size 
Adjustment Option) 
91.3% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) 
a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the 
Stock Exchange to permit H Shares in the International Offering to be placed to certain 
Existing Minority Shareholders and/or their close associates, and (b) a consent under Chapter 
4.15 of the Guide for New Listing Applicants to permit the Company to, among other things, 
allocate further H Shares in the International Offering to certain Cornerstone Investors and/or 
their respective close associates, (i) none of the Offer Shares subscribed by the placees and the 
public have been financed directly or indirectly by the Company, any of the Directors, 
Supervisors, chief executive of the Company, substantial Shareholders, existing Shareholders 
of the Company or any of its subsidiaries or their respective close associates; and (ii) none of 
the placees and the public who have purchased the Offer Shares are accustomed to taking 
instructions from the Company, any of the Directors, Supervisors, chief executive of the 
Company, substantial Shareholders, existing Shareholders of the Company or any of its 
subsidiaries or their respective close associates in relation to the acquisition, disposal, voting 
or other disposition of H Shares registered in his/her/its name or otherwise held by him/her/it. 
 
The placees in the International Offering include the following: 
 
Cornerstone Investors  
 
Investor 
No. of Offer 
Shares 
allocated 
% of total 
issued H Shares 
after the Global 
Offering (after 
taking into 
account the full 
exercise of the 
Offer Size 
% of total issued 
share capital 
after the Global 
Offering (after 
taking into 
account the full 
exercise of the 
Offer Size 
Existing 
shareholders or 
their close 
associates Note 2 

<<<PAGE 6>>>
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised) Note 1 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised) 
Oaktree 
Capital 
Management
, L.P. 
(“Oaktree”) 
5,106,200 
4.74% 
0.31% 
No 
Pinpoint 
Asset 
Management 
Limited 
(“Pinpoint”) 
3,404,100 
3.16% 
0.20% 
No 
Aspex 
Master Fund 
(“AMF”) 
17,020,700 
15.81% 
1.02% 
No 
MY Asian 
Opportunities 
Master Fund, 
L.P. (“MY 
Asian”) 
5,106,200 
4.74% 
0.31% 
No 
Morgan 
Stanley & 
Co. 
International 
plc 
(“MSIP”) 
3,404,100 
3.16% 
0.20% 
Yes 
Ovata 
Capital 
Management 
Limited 
(“Ovata 
Capital”) 
3,404,100 
3.16% 
0.20% 
No 
Qube Master 
Fund Ltd 
(“QRT”) 
3,404,100 
3.16% 
0.20% 
No 
Wuxi Jinchou 
and GTHT 
(in 
connection 
with Wuxi 
2,553,100 
2.37% 
0.15% 
No 

<<<PAGE 7>>>
Jinchou OTC 
Swaps) (as 
defined in the 
Prospectus) 
Integrated 
Core 
Strategies 
(Asia) Pte. 
Ltd. 
(“Millenniu
m ICSA”) 
1,702,000 
1.58% 
0.10% 
No 
Rome 
Garden 
Holding 
Limited 
(“Rome 
Garden”) 
1,702,000 
1.58% 
0.10% 
No 
Total 
46,806,600 
43.48% 
2.80% 
- 
Notes: 
 
(1) The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering. 
 
(2) In addition to the Offer Shares subscribed for as Cornerstone Investors, Pinpoint, AMF, MY Asian, MSIP, 
Ovata Capital, QRT, Millennium ICSA and Rome Garden and/or their respective close associates, where 
applicable, were allocated further Offer Shares as placees in the International Offering. Please refer to the 
section headed “Allotment Results Details – International Offer – Allotees with Waivers/Consents Obtained” in 
this announcement for details. Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-
up as indicated below. For details, please refer to the section headed “Lock-up Undertakings – Cornerstone 
Investors” in this announcement.  
 
 
Allottee with waivers/consents obtained 
 
Investor 
No. of Offer 
Shares allocated 
% of total 
issued H 
Shares after 
the Global 
Offering 
(after 
taking into 
account the 
full exercise 
of the Offer 
% of total 
issued share 
capital after 
the Global 
Offering 
(after taking 
into account 
the full 
exercise of 
the Offer 
Relationship 

<<<PAGE 8>>>
Size 
Adjustment 
Option and 
assuming 
the Over-
allotment 
Option is 
not 
exercised 
Note 4 
Size 
Adjustment 
Option and 
assuming 
the Over-
allotment 
Option is 
not 
exercised 
Note 5 
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and 
consent under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H 
Shares by Existing Minority Shareholders and their close associates Note 1 
Nil Note 1 
Nil 
Nil 
Nil 
Nil 
Allotees with consent under Chapter 4.15 of the Guide for New Listing Applicants in 
relation to allocations of further H Shares to investors who will participate in the Proposed 
Listing both as (i) a cornerstone investor and (ii) a placee in the International Offering Note 
2 
Pinpoint 
1,727,900  
1.60% 
0.10% 
A Cornerstone 
Investor 
AMF 
8,510,000 
7.90% 
0.51% 
A Cornerstone 
Investor 
MY Asian 
1,079,300 
1.00% 
0.06% 
A Cornerstone 
Investor 
MY Total Return 
Offshore SP3 
112,500 
0.10% 
0.01% 
A close associate of 
a Cornerstone 
Investor 
MSIP 
1,159,700 
1.08% 
0.07% 
An Existing 
Minority 
Shareholder and a 
Cornerstone Investor 
Ovata Capital 
600,000 
0.56% 
0.04% 
A Cornerstone 
Investor 
QRT 
930,000  
0.86% 
0.06% 
A Cornerstone 
Investor 
Millennium 
ICSA 
900,000 
0.84% 
0.05% 
A Cornerstone 
Investor 
Rome Garden 
680,600 
0.63% 
0.04% 
A Cornerstone 
Investor 
Guotai Junan 
Investments 
(Hong Kong) 
Limited 
(“GTINV”) 
850,000 
0.79% 
0.05% 
For further informa
tion of GTINV, ple
ase refer to the sec
tion named “Corner
stone Investors” 

<<<PAGE 9>>>
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 
of the Guide for New Listing Applicants in relation to allocations to connected clients Note 
3 
Huatai Capital 
Investment 
Limited 
(“HTCI”) 
1,300,000 
1.21% 
0.08% 
Connected client 
CITIC Securities 
Asset 
Management 
Company 
Limited 
(“CITIC AM”) 
34,000 
0.03% 
0.00%*  
Connected client 
CITIC Securities 
Asset 
management 
(HK) Limited 
(“CITIC AM 
HK”) 
34,000 
0.03%  
0.00%*  
Connected client 
CITIC Securities 
International 
Capital 
Management 
Limited (“CSI”) 
8,500 
0.01%  
0.00%*  
Connected client 
Bosera Asset 
Management 
(International) 
Co. Limited 
(“Bosera AM”) 
68,000 
0.06% 
0.00%* 
Connected client 
China Southern 
Asset 
Management 
Co., Ltd. 
(“China 
Southern”) 
930,000 
0.86% 
0.06% 
Connected client 
Nomura Asset 
Management 
Taiwan Ltd. 
(“Nomura 
AM”) 
300,000 
0.28% 
0.02% 
Connected client 
Notes: 
* Percentage less than 0.01% 
 
1. Among the Cornerstone Investors, MSIP is an Existing Minority Shareholder of the Company. The Stock 

<<<PAGE 10>>>
Exchange has granted a waiver from strict compliance with the requirements under Rule 10.04 of the 
Listing Rules and consent under Paragraph 1(C)(2) of the Placing Guidelines to permit H Shares in the 
International Offering to be placed to Existing Minority Shareholders and their close associates. Please 
refer to the section headed “Waivers and Exemptions – Allocation of H Shares to Existing Minority 
Shareholders and Their Close Associates” of the Prospectus for details. 
 
The Stock Exchange granted the waiver on the condition that, among others, details of the allocation to the 
Existing Minority Shareholders holding more than 1% of the issued share capital of the Company 
immediately prior to the completion of the Global Offering will be disclosed in the Prospectus and/or the 
allotment results announcement. 
 
2. The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations 
of Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed 
“Allotment Results Details – International Offer – Cornerstone Investors” in this announcement. For 
details of the consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations 
of further H Shares to the investors who will participate in the Proposed Listing both as (i) a cornerstone 
investor and (ii) a placee in the International Offering, please refer to the section headed 
“Others/Additional Information – Allocation of H Shares to investors who will participate in the Proposed 
Listing both as (i) a cornerstone investor and (ii) a placee in the International Offering with consents under 
Chapter 4.15 of the Guide for New Listing Applicants ” in this announcement. 
 
3. For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients, please refer to the section headed 
“Others / Additional Information – Placing to connected clients with prior consents under paragraph 1C(1) 
of the Placing Guidelines” in this announcement. 
 
4. The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares 
to be issued under the Global Offering. 
 
5. Only taking into account the H Shares allocated to the relevant investors under the Global Offering. 
 

<<<PAGE 11>>>
 
 
LOCK-UP UNDERTAKINGS  
 
Controlling Shareholders 
 
Name 
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing 
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
(after taking 
into account 
the full 
exercise of 
the Offer 
Size 
Adjustment 
Option and 
assuming 
the Over-
allotment 
Option is not 
exercised Note 
1 
% of 
shareholding 
in the 
Company 
subject to lock-
up 
undertakings 
upon Listing 
(after taking 
into account 
the full 
exercise of the 
Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised 
Last day 
subject to the 
lock-up 
undertakings 
Controlling 
Shareholders 
Note 2 
506,331,703 
0 
0 
30.29% 
August 10, 
2026 (First 
Six-month 
Period) Note 3  
February 10, 
2027 
(Second Six-
month 
Period) Note 4 
Note: 
 
1. The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares 
to be issued under the Global Offering. 
 
2. Mr. Wang Yanqing (王燕清), Lhasa Xindao, Wuxi Yuxi and Shanghai Zhuoao held 8,836,057, 336,039,506, 
69,414,157 and 92,041,983 Shares subject to lock-up undertakings upon Listing, respectively. 
 

<<<PAGE 12>>>
 
 
3. The Controlling Shareholders may dispose of or transfer Shares after the indicated date subject to that the 
Controlling Shareholders will not cease to be a Controlling Shareholder. 
 
4. The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after 
the indicated date. 
 
Cornerstone Investors  
 
Name 
Number of H Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing 
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing 
(after taking 
into account 
the full 
exercise of 
the Offer 
Size 
Adjustment 
Option and 
assuming the 
Over-
allotment 
Option is not 
exercised Note 
1 
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing 
(after taking 
into account 
the full 
exercise of 
the Offer 
Size 
Adjustment 
Option and 
assuming 
the Over-
allotment 
Option is not 
exercised 
Last day 
subject to the 
lock-up 
undertakings 
Note 2 
Oaktree 
5,106,200 
4.74% 
0.31% 
August 10, 
2026 
Pinpoint 
3,404,100 
3.16% 
0.20% 
August 10, 
2026 
AMF 
17,020,700 
15.81% 
1.02% 
August 10, 
2026 
MY Asian 
5,106,200 
4.74% 
0.31% 
August 10, 
2026 
MSIP 
3,404,100 
3.16% 
0.20% 
August 10, 
2026 
Ovata Capital 
3,404,100 
3.16% 
0.20% 
August 10, 
2026 
QRT 
3,404,100 
3.16% 
0.20% 
August 10, 

<<<PAGE 13>>>
 
 
2026 
Wuxi Jinchou and 
GTHT (in 
connection with 
Wuxi Jinchou OTC 
Swaps) (as defined 
in the Prospectus) 
2,553,100 
2.37% 
0.15% 
August 10, 
2026 
Millennium ICSA 
1,702,000 
1.58% 
0.10% 
August 10, 
2026 
Rome Garden 
1,702,000 
1.58% 
0.10% 
August 10, 
2026 
Notes: 
 
1. The number of H Shares immediately after the Global Offering is the same as the number 
of Offer Shares to be issued under the Global Offering. 
 
2. In accordance with the relevant cornerstone investment agreements, the required lock-
up ends on August 10, 2026. The Cornerstone Investors will cease to be prohibited from 
disposing of or transferring H Shares subscribed for pursuant to the relevant cornerstone 
investment agreements after the indicated date. 
 
PLACEE CONCENTRATION ANALYSIS 
 
Placee
s* 
Numbe
r of H 
Shares 
allotted 
Allotment 
as % of 
Internatio
nal 
Offering 
(assuming 
no 
exercise 
of the 
Over-
allotment 
Option) 
Allotment 
as % of 
Internatio
nal 
Offering 
(assuming 
the Over- 
allotment 
Option is 
fully 
exercised 
and new 
H Shares 
are 
issued) 
Allotm
ent 
as % of 
total 
Offer 
Shares 
(assumi
ng no 
exercise 
of the 
Over-
allotme
nt 
Option) 
Allotm
ent 
as % of 
total 
Offer 
Shares 
(assumi
ng the 
Over-
allotme
nt 
Option 
is fully 
exercise
d and 
new H 
Shares 
are 
issued) 
Numbe
r of H 
Shares 
held 
upon 
Listing 
% of 
total 
issued 
share 
capital 
upon 
Listing 
(assumi
ng no 
exercise 
of the 
Over-
allotme
nt 
Option) 
% of 
total 
issued 
share 
capital 
upon 
Listing 
(assumi
ng the 
Over-
allotme
nt 
Option 
is fully 
exercise
d and 
new H 
Shares 
are 
issued) 
Top 1 
25,530,7
25.97% 
22.31% 
23.71% 
20.62% 
25,530,7
1.53% 
1.51% 

<<<PAGE 14>>>
 
 
00 
00 
Top 5 
51,936,7
00 
52.84% 
45.38% 
48.24% 
41.95% 
51,936,7
00 
3.10% 
3.07% 
Top 10 72,844,9
00 
74.11% 
63.65% 
67.66% 
58.84% 
72,844,9
00 
4.35% 
4.31% 
Top 25 96,900,2
00 
98.58% 
84.67% 
90.01% 
78.27% 
96,900,2
00 
5.79% 
5.73% 
 
Note 
* Ranking of placees is based on the number of H Shares allotted to the placees. 
 
H SHAREHOLDERS CONCENTRATION ANALYSIS 
 
H 
Sharehol
ders * 
Numbe
r of H 
Shares 
allotted 
Allotmen
t as % of 
Internati
onal 
Offering 
(assumin
g no 
exercise 
of the 
Over-
allotment 
Option) 
Allotmen
t as % of 
Internati
onal 
Offering 
(assumin
g the 
Over- 
allotment 
Option is 
fully 
exercised 
and new 
H Shares 
are 
issued) 
Allotm
ent 
as % 
of total 
Offer 
Shares 
(assum
ing no 
exercis
e of the 
Over- 
allotm
ent 
Option
) 
Allotm
ent 
as % 
of total 
Offer 
Shares 
(assum
ing the 
Over- 
allotme
nt 
Option 
is fully 
exercis
ed and 
new H 
Shares 
are 
issued) 
Numbe
r of H 
Shares 
held 
upon 
Listing 
% of 
total 
issued 
H 
share 
capital 
upon 
Listing 
(assum
ing no 
exercis
e of the 
Over-
allotme
nt 
Option
) 
% of 
total 
issued 
H 
share 
capital 
upon 
Listing 
(assum
ing the 
Over-
allotme
nt 
Option 
is fully 
exercis
ed and 
new H 
Shares 
are 
issued) 
Top 1 
25,530,
700 
25.97% 
22.31% 
23.71% 
20.62% 
25,530,
700 
23.71% 
20.62% 
Top 5 
51,936,
700 
52.84% 
45.38% 
48.24% 
41.95% 
51,936,
700 
48.24% 
41.95% 
Top 10 
72,844,
900 
74.11% 
63.65% 
67.66% 
58.84% 
72,844,
900 
67.66% 
58.84% 
Top 25 
96,900,
200 
98.58% 
84.67% 
90.01% 
78.27% 
96,900,
200 
90.01% 
78.27% 
 
Note 

<<<PAGE 15>>>
 
 
* Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders 
upon Listing. 
 
SHAREHOLDER CONCENTRATION ANALYSIS 
 
Shareh
older s* 
Nu
mbe
r of 
H 
Shar
es 
allot
ted 
Allotme
nt as % 
of 
Internat
ional 
Offering 
(assumi
ng no 
exercise 
of the 
Over-
allotmen
t 
Option) 
Allotme
nt as % 
of 
Internat
ional 
Offering 
(assumi
ng the 
Over-
allotmen
t Option 
is fully 
exercise
d and 
new H 
Shares 
are 
issued) 
Allot
ment 
as % 
of 
total 
Offer 
Share
s 
(assu
ming 
no 
exerci
se of 
the 
Over- 
allotm
ent 
Optio
n) 
Allot
ment 
as % 
of 
total 
Offer 
Share
s 
(assu
ming 
the 
Over-
allotm
ent 
Optio
n is 
fully 
exerci
sed 
and 
new H 
Share
s are 
issued
) 
Numb
er of 
H 
Share
s held 
upon 
Listin
g 
Numb
er of 
Shares 
held 
upon 
Listing 
% of 
total 
issued 
share 
capita
l upon 
Listin
g 
(assu
ming 
no 
exerci
se of 
the 
Over-
allotm
ent 
Optio
n) 
% of 
total 
issued 
share 
capita
l upon 
Listin
g 
(assu
ming 
the 
Over-
allotm
ent 
Optio
n is 
fully 
exerci
sed 
and 
new H 
Share
s are 
issued
) 
Top 1 
- 
0.0% 
0.0% 
0.0% 
0.0% 
- 
        
506,331
,703  
30.3% 
30.0% 
Top 5 
       
25,530
,700  
26.0% 
22.3% 
23.7% 
20.6% 
       
25,530
,700  
        
637,573
,535  
38.1% 
37.7% 
Top 10 
       
40,506
,700  
41.2% 
35.4% 
37.6% 
32.7% 
       
40,506
,700  
        
678,521
,125  
40.5% 
40.1% 
Top 25 
       
69,944
,900  
71.2% 
61.1% 
65.0% 
56.5% 
       
69,944
,900  
        
745,844
,836  
44.6% 
44.1% 
 
Note 

<<<PAGE 16>>>
 
 
* Ranking of Shareholders is based on the number of Shares (of all classes) held by the 
Shareholder upon Listing. 
 
 

<<<PAGE 17>>>
 
 
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
100 
17,015 
3,063 out of 17,015 to 
receive 100 Shares 
18.00% 
200 
8,294 
1,659 out of 8,294 to 
receive 100 Shares 
10.00% 
300 
1,911 
516 out of 1,911 to 
receive 100 Shares 
9.00% 
400 
1,355 
434 out of 1,355 to 
receive 100 Shares 
8.01% 
500 
1,685 
632 out of 1,685 to 
receive 100 Shares 
7.50% 
600 
696 
305 out of 696 to 
receive 100 Shares 
7.30% 
700 
666 
336 out of 666 to 
receive 100 Shares 
7.21% 
800 
614 
344 out of 614 to 
receive 100 Shares 
7.00% 
900 
622 
381 out of 622 to 
receive 100 Shares 
6.81% 
1,000 
7,322 
4,566 out of 7,322 to 
receive 100 Shares 
6.24% 
2,000 
3,187 
2,550 out of 3,187 to 
receive 100 Shares 
4.00% 
3,000 
1,645 
1,481 out of 1,645 to 
receive 100 Shares 
3.00% 
4,000 
1,072 
100 Shares 
2.50% 
5,000 
1,118 
100 Shares plus 56 out 
of 1,118 to receive 
additional 100 Shares 
2.10% 
6,000 
659 
100 Shares plus 53 out 
of 659 to receive 
additional 100 Shares 
1.80% 
7,000 
492 
100 Shares plus 59 out 
1.60% 

<<<PAGE 18>>>
 
 
of 492 to receive 
additional 100 Shares 
8,000 
456 
100 Shares plus 91 out 
of 456 to receive 
additional 100 Shares 
1.50% 
9,000 
372 
100 Shares plus 97 out 
of 372 to receive 
additional 100 Shares 
1.40% 
10,000 
2,417 
100 Shares plus 725 out 
of 2,417 to receive 
additional 100 Shares 
1.30% 
20,000 
1,309 
200 Shares 
1.00% 
30,000 
475 
300 Shares 
1.00% 
40,000 
477 
400 Shares 
1.00% 
50,000 
368 
500 Shares 
1.00% 
60,000 
251 
600 Shares 
1.00% 
70,000 
196 
700 Shares 
1.00% 
80,000 
152 
800 Shares 
1.00% 
90,000 
181 
900 Shares 
1.00% 
100,000 
936 
1,000 Shares 
1.00% 
 
55,943 
Total number of 
Pool A successful 
applicants: 27,198 
 
POOL B 
150,000 
715 
2,700 Shares plus 57 
out of 715 to receive 
additional 100 Shares 
1.81% 
200,000 
219 
2,900 Shares 
1.45% 
250,000 
90 
3,100 Shares 
1.24% 
300,000 
66 
3,300 Shares 
1.10% 
350,000 
20 
3,500 Shares 
1.00% 
400,000 
49 
3,700 Shares 
0.93% 
450,000 
38 
3,900 Shares 
0.87% 
500,000 
97 
4,100 Shares 
0.82% 
1,000,000 
47 
6,100 Shares 
0.61% 
1,500,000 
12 
8,100 Shares 
0.54% 
2,000,000 
5 
10,100 Shares 
0.51% 
2,500,000 
5 
12,100 Shares 
0.48% 
3,000,000 
3 
14,100 Shares 
0.47% 
4,000,000 
2 
18,700 Shares 
0.47% 
4,680,800 
11 
21,900 Shares 
0.47% 
 
1,379 
Total number of 
Pool B successful 
 

<<<PAGE 19>>>
 
 
applicants: 1,379 
 
As of the date of this announcement, the relevant subscription monies previously deposited in 
the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers for any inquiries. 
 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect 
of which consent has been obtained, the Company has complied with the Listing Rules and 
guidance materials in relation to the placing, allotment and listing of the Company’s H Shares.  
 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and trading fee payable.  
 
OTHERS / ADDITIONAL INFORMATION 
 
Offer Size Adjustment Option and reallocation 
 
The Offer Size Adjustment Option has been fully exercised by the Company, pursuant to which 
the Company is issuing and allotting 14,042,400 additional Offer Shares, representing 
approximately 15.0% of the total number of Offer Shares initially available under the Global 
Offering, at the final Offer Price. All of the additional Offer Shares that would be allotted and 
issued by the Company pursuant to the full exercise of the Offer Size Adjustment Option will 
be allocated to the International Offering. 
 
Accordingly, the total number of Offer Shares finally available under the Global Offering 
(taking into account the full exercise of the Offer Size Adjustment Option and before any 
exercise of the Over-allotment Option) that would be allotted and issued by the Company is 
107,658,400 Offer Shares and the total issued share capital of the Company upon Listing 
(taking into account the full exercise of the Offer Size Adjustment Option and before any 
exercise of the Over-allotment Option) will be 1,673,821,434 Shares. 
 
As a result of the above, the final number of Offer Shares under the Hong Kong Public Offering 
is 9,361,600 Shares, representing approximately 8.7% of the total number of Offer Shares 
available under the Global Offering (assuming the Over-allotment Option is not exercised), and 
the final number of Offer Shares under the International Offering is adjusted to 98,296,800 
Shares, representing approximately 91.3% of the total number of Offer Shares under the Global 
Offering (assuming the Over-allotment Option is not exercised). 
 
Allocation of H Shares to existing minority Shareholders and their close associates 
 

<<<PAGE 20>>>
 
 
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
waiver from strict compliance with the requirements under Rule 10.04 and consent under 
Paragraph 1(C)(2) of Appendix F1 to the Listing Rules to permit H Shares in the International 
Offering to be placed to certain existing minority Shareholders who (i) hold less than 5% of 
the voting rights in the Company prior to the completion of the Global Offering and (ii) are not 
and will not become (upon the completion of the Global Offering) core connected persons of 
the Company or the close associates of any such core connected person (together, the “Existing 
Minority Shareholders”) and/or their close associates, subject to the conditions, among others, 
as follows: 
 
(a) each Existing Minority Shareholder to whom the Company may allocate the H Shares 
under the International Offering holds less than 5% of the voting rights in the Company 
prior to the completion of the Global Offering; 
 
(b) each Existing Minority Shareholder is not, and will not be, a core connected person of the 
Company or any close associate of any core connected person immediately prior to or 
following the Global Offering; and 
 
(c) none of the Existing Minority Shareholders has the right to appoint any Directors nor have 
any other special rights in the Company. 
 
Please refer to the section headed “Waivers and Exemptions – Allocation of H Shares to 
Existing Minority Shareholders and their Close Associates” in the Prospectus for further details 
of the waiver and consent.  
 
Each of the Joint Sponsors, the Overall Coordinators and the Company has provided the 
required confirmations as elaborated in the Prospectus. In particular, as the Company’s A 
Shares are listed on the Shenzhen Stock Exchange since May 2015, the Company has a highly 
extensive base of existing Shareholders and disclosure of details of allocations to all Existing 
Minority Shareholders will not be meaningful to investors, the proposed disclosure threshold, 
i.e. condition (f) of the waiver and consent which provides that details of the allocation to the 
Existing Minority Shareholders holding more than 1% of the total issued share capital of the 
Company immediately prior to the completion of the Global Offering and/or their close 
associates will be disclosed in this announcement, is appropriate. Nonetheless, as no allocation 
has been made to any such Existing Minority Shareholders holding more than 1% of the issued 
share capital of the Company, no disclosure has been made in this announcement. 
 
All allocation of Offer Shares to the Existing Minority Shareholders are in compliance with all 
the conditions under the wavier and consent granted by the Stock Exchange. 
 
Allocation of Offer Shares to Investors Who Will Participate in the Proposed Listing both as 
(i) a Cornerstone Investor and (ii) a Placee in the International Offering with consents under 
Chapter 4.15 of the Guide for New Listing Applicants 
 

<<<PAGE 21>>>
 
 
The Company has applied for, and the Stock Exchange has granted, a waiver/consent under 
paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants with respect to possible 
allocations to investors who will participate in the Proposed Listing both as (i) a cornerstone 
investor and (ii) a placee in the International Offering (the “Double-Dipping Participants”), 
subject to the following conditions: 
 
(a) the final offering size of the Proposed Listing, excluding any over-allocation, will be of a 
total value of at least HK$1 billion; 
 
(b) the Offer Shares allocated to any Double-Dipping Participant who is also an existing 
Shareholder (“Double-Dipping Existing Shareholder Participant”) and the close 
associates of such Double-Dipping Existing Shareholder Participant (as cornerstone 
investors and placees in the International Offering) as permitted under this exemption 
(being Morgan Stanley & Co. International plc only) do not exceed 30% of the total 
number of the H Shares offered; 
 
(c) each Director, chief executive and Controlling Shareholder of the Company confirms that 
no securities have been allocated to them or their respective close associates under the 
exemption as required by paragraph 18(iii) of Chapter 4.15 of the Guide for New Listing 
Applicants; 
 
(d) allocation to the Double-Dipping Participants and/or their respective close associates will 
not affect the Company’s ability to satisfy the public float requirement; and 
 
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

<<<PAGE 22>>>
 
 
 
No. 
Connected Distributor 
Connected 
Client 
Relationship 
Whether the 
Connected 
Client will hold 
the beneficial 
interests of the 
Offer Shares on 
a non-
discretionary 
basis or 
discretionary 
basis for 
independent 
third partis 
Number of 
Offer Shares 
to be 
allocated to 
the connected 
client 
Approximate 
percentage 
of Offer 
Shares (after 
taking into 
account the 
full exercise 
of the Offer 
Size 
Adjustment 
Option and 
assuming no 
exercise of 
the Over-
allotment 
Option) 
Approximate 
percentage 
of total 
issued share 
capital after 
the Global 
Offering 
(after taking 
into account 
the full 
exercise of 
the Offer 
Size 
Adjustment 
Option and 
assuming no 
exercise of 
the Over-
allotment 
Option) 
1. 
 Huatai Financial Holdings 
(Hong 
Kong) 
Limited 
(“HTFH”) 
HTCI Note 1 
HTFH and HTCI are members of the 
same group. 
Non-discretionary 
basis 
1,300,000 
1.21% 
0.08% 
2. 
 CLSA Limited (“CLSA”) 
CITIC AM Note 2 
CITIC Asset Management is a member 
of the same group of companies as 
CLSA. 
Discretionary 
basis 
34,000 
0.03% 
0.00%*  

<<<PAGE 23>>>
 
 
3. 
 CLSA 
CITIC AM HK 
Note 3 
CITIC Asset Management HK is a 
member of the same group of 
companies as CLSA. 
Discretionary 
basis 
34,000 
0.03%  
0.00%*  
4. 
 CLSA 
CSI Note 4 
CSI is a member of the same group of 
companies as CLSA. 
Non-
discretionary 
basis 
8,500 
0.01%  
0.00%*  
5. 
 CMB International Capital 
Limited, CMB International 
Securities Limited and CMB 
International Global Markets 
Limited (“CMBI Connected 
Distributors”) 
Bosera AM Note 5  
Bosera AM is a member of the same 
group of companies as CMBI Connected 
Distributors. 
Discretionary 
basis 
68,000 
0.06% 
0.00%* 
6. 
 HTFH 
China Southern 
Note 6 
China Southern is a member of the 
same group of companies as HTFH. 
Discretionary 
basis  
930,000 
0.86% 
0.06% 
7. 
 Nomura Singapore Limited 
Nomura Asset 
Management 
Taiwan Ltd. 
(“Nomura 
AM”) 
Nomura AM is a member of the same 
group 
of 
companies 
as 
Nomura 
Singapore Limited 
Discretionary 
basis 
300,000 
0.28% 
0.02% 
 
Notes: 
 
* percentage less than 0.01% 
 
(1) HTCI 
 

<<<PAGE 24>>>
 
 
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public offerings (“IPOs”) in Hong Kong. However, PRC investors are 
permitted to invest in products issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. In connection with such products, 
the licensed domestic securities firms, through their Hong Kong affiliates, may participate in Hong Kong IPOs either as placees or cornerstone investors (the “Cross-border 
Derivatives Trading Regime”). 
 
Huatai Securities Co., Ltd. (“Huatai Securities”), the shares of which are listed on both the Shanghai Stock Exchange (stock code: 601688) and the Stock Exchange (stock 
code: 6886), is one of the domestic securities firms licensed to undertake cross-border derivatives trading activities. Huatai Securities entered into an ISDA agreement (the 
“ISDA Agreement”) with its indirectly wholly-owned subsidiary, Huatai Capital Investment Limited (“HTCI”) to set out the principal terms of any future total return swap 
between Huatai Securities and HTCI. 
 
HTFH is the Joint Global Coordinator, Joint Bookrunner, Joint Lead Manager and Capital Market Intermediary in connection with the Global Offering. Pursuant to the ISDA 
Agreement, HTCI, which intends to participate in the Global Offering as a placee, will hold the beneficial interest of the Offer Shares on a non-discretionary basis as the single 
underlying holder under a back-to-back total return swap (the “Back-to-back TRS”) to be entered by HTCI in connection with a Client TRS (as defined below) placed by and 
fully funded (i.e. with no financing provided by HTCI) by the Huatai Ultimate Clients (as defined below), by which, HTCI will, subject to customary fees and commissions, pass 
the full economic exposure of the Offer Shares ultimately to the Huatai Ultimate Clients, which in effect, HTCI will hold the beneficial interest of the Offer Shares on behalf of 
the Huatai Ultimate Clients. HTFH and HTCI are indirectly wholly-owned subsidiaries of Huatai Securities. Accordingly, HTCI is considered as a “connected client” of HTFH 
pursuant to paragraph 13(7) of the Placing Guidelines. 
 
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the “Huatai Ultimate Clients”) cannot directly subscribe for the Offer Shares but may invest 
in derivative products issued by domestic securities firms licenced to undertake cross-border derivatives trading activities, such as Huatai Securities, with the Offer Shares as 
the underlying assets. Instead of directly subscribing for the Offer Shares, the Huatai Ultimate Clients, through their investment manager, will place a total return swap order 
(the “Client TRS”) with Huatai Securities in connection with the Company’s IPO and Huatai Securities will place a Back-to-back TRS order to HTCI on the terms of the ISDA 
Agreement. In order to hedge its exposure under the Back-to-back TRS, HTCI participates in the Company’s IPO and subscribes the Offer Shares through placing order with 
HTFH during the International Offering.  
 
To the best of our knowledge and after making all reasonable enquiries, each of the Huatai Ultimate Clients is an independent third party of (i) the Company, the connected 
person or the associates thereof, and (ii) HTCI, HTFH and the companies which are members of the same group of HTCI. 
 
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in connection with the Client TRS order placed by the Huatai Ultimate Clients. 

<<<PAGE 25>>>
 
 
Pursuant to the terms of the contracts of the Back-to-back TRS and the Client TRS, during the tenor of the Back-to-back TRS and the Client TRS, subject to customary fees and 
commissions, all economic returns of the Offer Shares will be ultimately passed to the Huatai Ultimate Clients through the Back-to-back TRS and the Client TRS and all 
economic loss shall be ultimately borne by the Huatai Ultimate Clients. HTCI will not take any economic return or bear any economic loss in relation to the Offer Shares. 
 
Investment in the Back-to-back TRS and the Client TRS is similar to the investment in a qualified domestic institutional investor fund (“QDII”) in the way that the Huatai 
Ultimate Clients would reap all the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through the exchange rate exposure on both the 
notional value of the investment and the profit and loss of the investment. In contrast, the profit and loss of the Back-to-back TRS and the Client TRS factor into account the 
fluctuation in RMB exchange rate upon termination of the Client TRS by converting the profit and loss using the current exchange rate at the time of termination. As such, the 
Huatai Ultimate Clients would bear the exchange rate exposure of the profit and loss on settlement date. 
 
The Huatai Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time from the issue date of the Client TRS which should be on or after 
the date on which the Offer Shares are listed on the Stock Exchange at their own discretion. Upon the termination upon maturity or early termination of the Client TRS by the 
Huatai Ultimate Clients, HTCI will dispose the Offer Shares on the secondary market and the Huatai Ultimate Clients will receive a final settlement amount in cash in 
accordance with the terms and conditions of the Back-to-back TRS and the Client TRS which should have taken into account all the economic returns or economic loss in 
relation to the Offer Shares. If upon the maturity of the Client TRS, the Huatai Ultimate Clients intend to extend the investment period, subject to further agreement between 
Huatai Securities and the relevant Huatai Ultimate Clients, the term of the Client TRS could be extended by way of a new issuance or a tenor extension. Accordingly, Huatai 
Securities will extend the term of the Back-to-back TRS by way of a new issuance or a tenor extension. 
 
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through the economic exposure to the Huatai Ultimate Clients, each 
being an onshore client who places a Client TRS order with Huatai Securities in connection with the IPO of the Company. HTCI will not exercise the voting right of the Offer 
Shares during the tenor of the Back-to-back TRS. 
 
The Huatai Ultimate Clients are certain domestic private funds (each being an Independent Third Party) managed by Shanghai Greenwoods Asset Management Co., Ltd. (上
海景林资产管理有限公司), namely (i) Greenwoods Harvest Fund No.2 (景林丰收2 号基金), (ii) Greenwoods Harvest Fund No.3 (景林丰收3 号基金), (iii) Greenwoods 
Harvest No. 1 Private Securities Investment Fund (景林丰收6 号私募证券投资基金) and (iv) Greenwoods Jingtai Harvest Private Equity Investment Fund (景林景泰丰收
私募证券投资基金), of which no single ultimate beneficial owner holds 30% or more interest therein. The ultimate beneficial owner of Shanghai Greenwoods Asset 
Management Co., Ltd. is Jiang Jinzhi (蒋锦志). Each of the ultimate clients listed in (i) to (iv) above is entitled to economic returns of 42,200, 716,700, 56,200 and 484,900 
Offer Shares, respectively. 
 

<<<PAGE 26>>>
 
 
(2) CITIC Asset Management 
 
CITIC Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of its underlying clients, namely (i) CITIC 
SECURITIES COMPANY LIMITED-XINHANG ZHIYUAN NO.1 (中信證券信航致遠1 號集合資産管理計劃); (ii) CITIC SECURITIES COMPANY LIMITED-XINHANG 
ZHIYUAN NO.3 (中信證券信航致遠3 號集合資産管理計劃); and (iii) CITIC Securities AM-Guibinfengyuan No.118 QDII (中信證券資管貴賓豐元118 號QDII 集合資
産管理計劃), none of which has an ultimate beneficial owner holding 30% or more interest therein and each of which is, to the best knowledge of CITIC Asset Management, 
an independent third party of the Company, the connected person or the associates thereof, CITIC Asset Management, CLSA and the companies which are members of the same 
group of CLSA. CITIC Asset Management will hold 7,000, 16,200 and 10,800 Offer Shares on behalf of each of the ultimate clients listed in (i) to (iii) above, respectively. 
 
The ultimate beneficial owner of CITIC Asset Management is CITIC Securities Company Limited (中信證券股份有限公司, 6030.HK). 
 
(3) CITIC Asset Management HK  
 
CITIC Asset Management HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the fund on behalf of its underlying client, namely 
CDNETWORKS HOLDINGS SINGAPORE PTE, LTD., of which the ultimate beneficial owner holding 30% or more interest therein is Wangsu Science & Technology Co., Ltd. 
(300017.SZ), and of which is, to the best knowledge of CITIC Asset Management HK, an independent third party of the Company, the connected person or the associates thereof, 
CITIC Asset Management HK, CLSA and the companies which are members of the same group of CLSA. 
 
The ultimate beneficial owner of CITIC Asset Management HK is CITIC Securities Company Limited (中信證券股份有限公司, 6030.HK). 
 
(4) CSI  
 
CSI and CITIC Securities Company Limited will enter into a series of cross border OTC swap transactions (“OTC Swaps”) with Black Crystal Capital Management Co., Ltd. 
(黑晶資本管理有限公司), of which the ultimate beneficial owners holding 30% or more interest therein are Li Chuxin (李出新) and Shao Yukai (邵宇開), pursuant to which 
CSI will hold the Offer Shares to be subscribed for and on behalf of Black Crystal Capital Management Co., Ltd. on a non-discretionary basis to hedge the OTC Swaps while 
the economic risks and returns of the underlying Offer Shares are passed to the ultimate clients, subject to customary fees and commissions. CSI will not take part in any 
economic returns or bear any economic losses in relation to the Offer Shares. The OTC Swaps will be fully funded by Black Crystal Capital Management Co., Ltd.  
 
The ultimate beneficial owner of CSI is CITIC Securities Company Limited (中信證券股份有限公司, 6030.HK). 

<<<PAGE 27>>>
 
 
 
(5) Bosera AM 
 
Bosera AM will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of its underlying clients, namely (i) Bosera Global Select 
Equity Fund SP, of which the ultimate beneficial owner holding 30% or more therein is Zhang Lei (张雷); and (ii) Bosera Hong Kong Equity Plus Fund, of which there is no 
ultimate beneficial owner holding 30% or more interest therein, and each of which is, to the best knowledge of Bosera AM, an independent third party of the Company, the 
connected person or the associates thereof, Bosera AM, CMBI Connected Distributors and the companies which are members of the same group of CMBI. Bosera AM will hold 
3,900 and 64,100 Offer Shares on behalf of each of the ultimate clients listed in (i) to (ii) above, respectively. 
 
The ultimate beneficial owner of Bosera AM is China Merchants Group. 
 
(6) China Southern 
 
China Southern will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of its underlying clients, namely (i) China Southern 
Hong Kong Growth Dynamic Allocation Hybrid Fund (南方香港成长灵活配置混合), (ii) China Southern Hong Kong Digital Economy Hybrid Initiating Fund (QDII) (南方
港股数字经济混合发起(QDII)), (iii) China Southern China New Economy 9-Month Holding Period Hybrid Fund (QDII) (南方中国新兴经济9 个月持有期混合(QDII)), 
(iv) China Southern Hong Kong Select Equity Fund (南方香港LOF) and (v) China Southern Global Dynamic Allocation Fund (南方全球精选配置股票(QDII-FOF)), each 
of which there is no ultimate beneficial owner holding 30% or more interest therein, and each of which is, to the best knowledge of China Southern, an independent third party 
of the Company, the connected person or the associates thereof, China Southern, HTFH and the companies which are members of the same group of HTFH. China Southern 
will hold 431,800, 23,300, 265,700, 159,400 and 49,800 Offer Shares on behalf of each of the ultimate clients listed in (i) to (v) above, respectively. 
 
The ultimate beneficial owner of China Southern is Huatai Securities. 
 
(7) Nomura AM 
 
Nomura AM will hold the Offer Shares in its capacity as the discretionary fund manager managing the fund on behalf of its underlying client, namely GSAM Greater China 
Equity Fund, of which there is no ultimate beneficial owner holding 30% or more interest therein, and of which is, to the best knowledge of Nomura AM, an independent third 
party of the Company, the connected person or the associates thereof, Nomura AM, Nomura Singapore Limited and the companies which are members of the same group of 
Nomura Singapore Limited. 

<<<PAGE 28>>>
 
 
 
DISCLAIMERS 
 
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
and Hong Kong Securities Clearing Company Limited take no responsibility for the contents 
of this announcement, make no representation as to its accuracy or completeness and 
expressly disclaim any liability whatsoever for any loss howsoever arising from or in reliance 
upon the whole or any part of the contents of this announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or 
into the United States (including its territories and possessions, any state of the United States 
and the District of Columbia). This announcement does not constitute or form a part of any 
offer or solicitation to purchase or subscribe for securities in the United States. The 
securities mentioned herein have not been, and will not be, registered under the United States 
Securities Act of 1933, as amended (the “U.S. Securities Act”). The securities may not be 
offered or sold in the United States except pursuant to an exemption from the registration 
requirements of the U.S. Securities Act and in compliance with any applicable state securities 
laws, or outside the United States unless in compliance with Regulation S under the U.S. 
Securities Act. There will be no public offer of securities in the United States. 
The Offer Shares are being offered and sold outside the United States in offshore transactions 
in reliance on Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated February 3, 2026 issued by WUXI 
LEAD INTELLIGENT EQUIPMENT CO., LTD. for detailed information about the Global 
Offering described below before deciding whether or not to invest in the H Shares thereby 
being offered. 
*Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements – Hong Kong Public Offering – Hong Kong Underwriting 
Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. 
(Hong Kong time) on the Listing Date (which is currently expected to be on February 11, 
2026). 
 
 
 

<<<PAGE 29>>>
 
 
PUBLIC FLOAT 
 
Immediately after the completion of the Global Offering (after taking into account the full 
exercise of the Offer Size Adjustment Option and before any exercise of the Over-allotment 
Option), the total market value of the H Shares to be held by the public is expected to be above 
HK$4,930.8 million, calculated based on the final Offer Price of HK$45.80, which is higher 
than the prescribed expected market value of H Shares required to be held in public hands of 
not less than HK$3,000,000,000 under Rule 19A.13A(2)(b) of the Listing Rules, thereby 
satisfying Rule 19A.13A of the Listing Rules.  
 
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not 
be counted towards the free float of the H Shares of the Company at the time of Listing. Based 
on the final Offer Price of HK$45.80 per H Share, the Company satisfies the free float 
requirement under Rule 19A.13C(1)(b) of the Listing Rules. 
 
The Directors confirm that, immediately following the completion of the Global Offering (after 
taking into account the full exercise of the Offer Size Adjustment Option and before any 
exercise of the Over-allotment Option), (i) no placee will, individually, be placed more than 
10% of the enlarged issued share capital of the Company immediately after the Global Offering; 
(ii) there will not be any new substantial Shareholder immediately after the Global Offering; 
(iii) the three largest public shareholders of the Company do not hold more than 50% of the H 
shares in public hands at the time of the Listing in compliance with Rules 8.08(3) and 8.24 of 
the Listing Rules; and (iv) there will be at least 300 Shareholders at the time of the Listing in 
compliance with Rule 8.08(2) of the Listing Rules.  
 
COMMENCEMENT OF DEALINGS 
 
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, 
February 11, 2026 (Hong Kong time), provided that the Global Offering has become 
unconditional and the right of termination described in the section headed “Underwriting – 
Underwriting Arrangements – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus has not been exercised. Investors who trade the H Shares on the basis of publicly 
available allocation details prior to the receipt of H Share certificates or prior to the H Share 
certificates becoming valid evidence of title do so entirely at their own risk. 
 
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Wednesday, 
February 11, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Wednesday, February 11, 2026 (Hong Kong time). 
The H Shares will be traded in board lots of 100 H Shares each, and the stock code of the H 
Shares will be 0470.  
 
By order of the Board  
Wuxi Lead Intelligent Equipment Co., Ltd.  

<<<PAGE 30>>>
 
 
Mr. Wang Yanqing 
Chairman of the Board, Executive Director and 
Chief Executive Officer 
 
Hong Kong, February 10, 2026 
As at the date of this announcement, the Board comprises: (i) Mr. Wang Yanqing, Mr. 
Wang Jianxin, Mr. You Zhiliang and Mr. Wang Lei as executive directors; and (ii) Ms. 
Zhang Mingyan, Mr. Dai Jianjun and Ms. Wong Sze Wing as independent non-executive 
directors. 
 
 
 
