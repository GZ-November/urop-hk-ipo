# 配发结果公告抽取任务：1021.HK Guangdong Huayan Robotics Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**27/03/2026 22:27**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0327/2026032703804.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1021.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the prospectus dated March 20, 2026 (the “Prospectus”) issued by Guangdong Huayan Robotics Co., Ltd. 
(廣東華沿機器人股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. Potential investors should read Prospectus for detailed information about the Company and 
the Global Offering described below before deciding whether or not to invest in the Offer Shares.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities 
in the United States or in any other jurisdictions. The securities mentioned herein have not been, and will not be, 
registered under the United States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or 
securities law of any state or other jurisdiction of the United States and may not be offered, sold, pledged or otherwise 
transferred within the United States except in transactions exempt from, or not subject to, the registration requirements 
of the U.S. Securities Act. There will be no public offer of securities in the United States. The Offer Shares are being 
offered and sold outside the United States in offshore transactions in reliance on Regulation S under the U.S. Securities 
Act.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited, as 
stabilizing manager (the “Stabilizing Manager”), or any person acting for it, on behalf of the Underwriters, may 
over-allocate or effect transactions with a view to stabilizing or supporting the market price of the Shares at a level 
higher than that which might otherwise prevail for a limited period after the Listing Date. However, there is no 
obligation on the Stabilizing Manager, or any person acting for it to conduct any such stabilizing action, which, if 
commenced, will be done at the sole and absolute discretion of the Stabilizing Manager, or any person acting for 
it, and may be discontinued at any time. Any such stabilizing action is required to be brought to an end on the 30th 
day after the last day for the lodging of applications under the Hong Kong Public Offering. Such stabilizing action, 
if taken, may be effected in all jurisdictions where it is permissible to do so, in each case in compliance with all 
applicable laws, rules and regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules 
(Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter 
571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the Shares for longer 
than the stabilization period, which begins on the Listing Date and is expected to expire on the 30th day after the last 
day for lodging applications under the Hong Kong Public Offering. After this date, when no further stabilizing action 
may be taken, demand for the Shares, and therefore the price of the Shares, could fall.
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinators (for themselves and on 
behalf of the Hong Kong Underwriters and Overall Coordinators) shall be entitled to terminate their obligations under 
the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the 
section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – Hong Kong 
Underwriting Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong 
time) on the Listing Date (which is currently expected to be on Monday, March 30, 2026).

<<<PAGE 2>>>
2
Guangdong Huayan Robotics Co., Ltd.
廣東華沿機器人股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under the
Global Offering
:
92,902,600 H Shares (taking into account 
the full exercise of the Offer Size 
Adjustment Option and subject to the 
Over-allotment Option)
Number of Hong Kong Offer Shares
:
16,157,000 H Shares (taking into account 
reallocation)
Number of International Offer Shares
:
76,745,600 H Shares (taking into account 
the full exercise of the Offer Size 
Adjustment Option, reallocation and 
subject to the Over-allotment Option)
Final Offer Price
:
HK$17.00 per H Share, plus brokerage 
of 1.0%, SFC transaction levy of 
0.0027%, Hong Kong Stock Exchange 
trading fee of 0.00565% and AFRC 
transaction levy of 0.00015%
Nominal Value
:
RMB 0.2 per H Share
Stock Code
:
1021
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
Guangdong Huayan Robotics Co., Ltd.
廣東華沿機器人股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated 20 March 2026 (the “Prospectus”) issued by 
Guangdong Huayan Robotics Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could 
move substantially even with a small number of H Shares traded and should exercise extreme 
caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
1021
Stock short name
HUAYAN ROBOTICS
Dealings commencement date
30 March 2026*
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$17.00
Offer Price Range
N/A
Offer Price Adjustment exercised
N/A
Offer Shares and Share Capital
Number of Offer Shares (taking into account the full exercise 
of the Offer Size Adjustment Option and before exercise of the 
Over-allotment Option)
92,902,600
Number of Offer Shares in Hong Kong Public Offering (after 
reallocation)
16,157,000
Number of offer shares in International Offering (after 
reallocation and taking into account the full exercise of the 
Offer Size Adjustment Option and before exercise of the Over-
allotment Option)
76,745,600
Number of issued shares upon Listing (before exercise of the 
Over-allotment Option)
543,597,580

<<<PAGE 4>>>
4
Offer Size Adjustment Option (Upsize option)
Number of additional shares issued under the option
12,117,600
– Hong Kong Public Offering
0
– International Offering
12,117,600
The Offer Size Adjustment Option has been exercised in full, pursuant to which the Company 
is issuing and allotting 12,117,600 additional Offer Shares, representing approximately 15% of 
the total number of Offer Shares initially available under the Global Offering, at the final Offer 
Price.
The additional Offer Shares issued pursuant to the Offer Size Adjustment Option will be 
allocated to the International Offering.
Over-allocation
No. of Offer Shares over-allocated
13,935,200
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$1,579.34 million
Less: Estimated listing expenses payable based on Final Offer 
Price
HK$(101.17) million
Net proceeds
HK$1,478.18 million
Note: Gross proceeds refers to the amount to which the issuer is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis.

<<<PAGE 5>>>
5
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
227,070
No. of successful applications
66,270
Subscription level (before taking into account the Offer Size 
Adjustment Option)
5,059.38 times
Claw-back triggered
Yes
No. of Offer Shares initially available under the Hong Kong 
Public Offering
4,039,400
No. of Offer Shares reallocated from the International Offering 
(claw-back)
12,117,600
Final no. of Offer Shares under the Hong Kong Public Offering 
(after reallocation)
16,157,000
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering (after taking into account the full exercise of the 
Offer Size Adjustment Option)
17.4%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can 
refer to https://www.hkeipo.hk/iporesult to perform a search by identification number or 
https://www.hkeipo.hk/iporesult for the full list of allottees.

<<<PAGE 6>>>
6
INTERNATIONAL OFFERING
No. of placees
151
Subscription Level (before taking into account the Offer Size 
Adjustment Option)
16.65 times
No. of Offer Shares initially available under the International 
Offering
76,745,600
Final no. of Offer Shares under the International Offering (after 
reallocation and taking into account the full exercise of the Offer 
Size Adjustment Option)
76,745,600
% of Offer Shares under the International Offering to the Global 
Offering (after taking into account the full exercise of the Offer 
Size Adjustment Option)
82.6%
The Directors confirm that, to the best of their knowledge, information and belief, save for a 
waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit the Company to allocate certain Offer Shares in the International Offering to 
close associates of existing shareholders as a cornerstone investor and a placee, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, controlling shareholders, 
substantial shareholders, existing shareholders of the Company or any of its subsidiaries or their 
respective close associates; and (ii) none of the placees and the public who have purchased the 
Offer Shares are accustomed to taking instructions from the Company, any of the Directors, chief 
executive of the Company, controlling shareholders, substantial shareholders, existing shareholders 
of the Company or any of its subsidiaries or their respective close associates in relation to the 
acquisition, disposal, voting or other disposition of Shares registered in his/her/its name or 
otherwise held by him/her/it.

<<<PAGE 7>>>
7
Cornerstone Investors
Name Note 1
No. of Offer 
Shares 
allocated
% of total 
issued H – 
shares after 
the Global 
Offering Note 2
% of total 
issued share 
capital after 
the Global 
Offering Note 2
Existing 
shareholders 
or their close 
associates
HHLR Advisors, Ltd.
13,802,400
2.63%
2.54%
No
GF Fund
13,802,200Note 3
2.63%
2.54%
No
Morgan Stanley & Co. 
International plc
4,600,800
0.88%
0.85%
No
Samson Group Limited/晟信集團
有限公司
2,941,000
0.56%
0.54%
No
Haojun Investment and HTCI 
(in connection with Haojun 
Investment OTC Swaps) Note 4
2,667,800
0.51%
0.49%
No
Eternal Summer Consulting 
Company Ltd.
2,300,400
0.44%
0.42%
No
Shrewd Pioneer Limited
2,300,400
0.44%
0.42%
No
Richfirm (Hong Kong) 
Development Limited/全順(香港)
發展有限公司
1,470,400
0.28%
0.27%
Yes
VVC Technology Fund Ltd.
1,380,200
0.26%
0.25%
No
Subtotal
45,265,600
8.61%
8.33%
Notes:
1. 
For further details of the cornerstone investors, please refer to the section headed “Cornerstone Investors” of the 
Prospectus.
2. 
After taking into account the full exercise of the Offer Size Adjustment Option and assuming the Over-allotment Option 
is not exercised.
3. 
The discrepancy between final number of allocated Offer Shares and disclosure in the Prospectus was due to rounding 
adjustments.
4. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations to connected clients, please refer to the section headed “Allottees with waivers/
consents obtained – International Offering – allotees with consent under paragraph 1C(1) of the Placing Guidelines 
and Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations to connected clients” of this 
announcement.

<<<PAGE 8>>>
8
Allotees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares
% of total 
issued 
H-shares after 
the Global 
Offering upon 
listing Note 1
% of 
shareholding in 
the Company 
listing Note 1
Relationship
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the Placing 
Guidelines in relation to subscription for H Shares by a close associate of existing shareholders Note 2
Cornerstone Investor
Richfirm (Hong Kong) 
Development Limited/全順(香
港)發展有限公司 (“Richfirm”)
1,470,400
1.58%
0.28%
0.27%
A cornerstone investor 
and close associate of 
existing shareholders
Placee
Yihe No. 22 Private Securities 
Investment Fund/頤和 22 期
私募證券投資基金(“Yihe No. 
22”)
4,236,200
4.56%
0.81%
0.78%
A placee and close 
associate of existing 
shareholders
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants 
in relation to allocations to connected clients
Huatai Capital Investment 
Limited (“HTCI”) Note 3
8,668,600
9.33%
1.65%
1.59%
connected client and 
a close associate of 
existing minority 
shareholder
CICC Financial Trading Limited 
(“CICC FT”) Note 3
35,200
0.04%
0.01%
0.01%
connected client
ICBC UBS Asset Management 
Co., (International) Ltd. 
(“ICBC UBS”) Note 3
311,000
0.33%
0.06%
0.06%
connected client
ICBC International Fund 
Management Limited (“ICBCI 
FM”) Note 3
13,800
0.01%
0.00%
0.00%
connected client
ICBC UBS Asset Management 
(International) Company 
Limited (“ICBC UBS 
International”) Note 3
100,600
0.11%
0.02%
0.02%
connected client
China Asset Management (Hong 
Kong) Limited (“China AMC 
HK”) Note 3
411,600
0.44%
0.08%
0.08%
connected client
Bosera Asset Management 
(International) Co., Limited 
(“Bosera Asset Management”) 
Note 3
345,000
0.37%
0.07%
0.06%
connected client

<<<PAGE 9>>>
9
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares
% of total 
issued 
H-shares after 
the Global 
Offering upon 
listing Note 1
% of 
shareholding in 
the Company 
listing Note 1
Relationship
Notes:
1. 
After taking into account the full exercise of the Offer Size Adjustment Option and assuming the Over-allotment Option is not exercised.
2. 
The Stock Exchange has granted a waiver from strict compliance with the requirements under Rule 10.04 of the Listing Rules and consent under Paragraph 
1C(2) of the Placing Guidelines to permit H Shares in the International Offering to be placed to close associates of existing shareholders as a cornerstone 
investor and a placee. For details of the consent under paragraph 1C(2) of the Placing Guidelines in relation to allocations to existing shareholder, please 
refer to the section headed “Waiver and Exemption – Waiver and consent in respect of subscriptions of offer shares by close associates of existing 
shareholder as cornerstone investor” in the Prospectus and the section headed “Allottees with waivers/consents obtained – International Offering – allotees 
with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations to 
connected clients” of this announcement.
To the best knowledge, information and belief of the Company after due enquiry, details of the allocation to a close associate of existing shareholders 
holding more than 1% of the issued share capital of the Company immediately prior to the completion of the Global Offering have been disclosed in this 
announcement.
3. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocations to connected clients, please refer to the section headed “Allottees with waivers/consents obtained – International Offering – allotees with consent 
under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations to connected clients” of 
this announcement.

<<<PAGE 10>>>
10
LOCK-UP UNDERTAKINGS
Shareholders of Unlisted Shares
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon listing
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon listing
% of total 
issued H-shares 
after the Global 
Offering subject 
to lock-up 
undertakings 
upon listing Note 1
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon listing Note 1
Last day 
subject to 
the lock-up 
undertakings 
Note 2
Shenzhen Zhirenxue 
Enterprise Management 
Partnership (Limited 
Partnership)/深圳市
智人學企業管理合
夥企業(有限合夥) 
(“Zhirenxue”)
8,617,800
–
–
1.59%
29 March 2027
Shenzhen Zhirenle 
Enterprise Management 
Partnership (Limited 
Partnership)/深圳市
智人樂企業管理合
夥企業(有限合夥) 
(“Zhirenle”)
5,000,000
–
–
0.92%
29 March 2027
Shenzhen Zhirenju 
Enterprise Management 
Partnership (Limited 
Partnership)/深圳市
智人聚企業管理合
夥企業(有限合夥) 
(“Zhirenju”)
2,500,000
–
–
0.46%
29 March 2027
Shenzhen Zhirenyun 
Enterprise Management 
Partnership (Limited 
Partnership)/深圳市
智人雲企業管理有
限合夥(有限合夥) 
(“Zhirenyun”)
1,910,000
–
–
0.35%
29 March 2027
Subtotal
18,027,800
–
–
3.32%
Notes:
1. 
After taking into account the full exercise of the Offer Size Adjustment Option and assuming the Over-
allotment Option is not exercised.
2. 
The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws and 
relevant lock-up undertakings as disclosed in the Prospectus.

<<<PAGE 11>>>
11
Controlling Shareholders
Name
Number of H – 
shares held in 
the Company 
subject to lock-
up undertakings 
upon listing
% of total issued 
H-shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon listing Note 1
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon listing Note 1
Last day subject 
to the lock-up 
undertakings Note 2
Mr. Wang Guangneng/王光能(“Mr. 
Wang”)
14,218,750
2.71%
2.62%
29 March 2027
Mr. Zhang Guoping/張國平(“Mr. 
Zhang”)
2,031,250
0.39%
0.37%
29 March 2027
Sichuan Zhirentuan Enterprise 
Management Partnership (Limited 
Partnership)/四川智人團企業管理合
夥企業(有限合夥) (“Zhirentuan”)
113,107,850
21.52%
20.81%
29 March 2027
Shenzhen Zhirenxing Enterprise 
Management Partnership (Limited 
Partnership)/深圳市智人行企業管理
合夥企業(有限合夥) (“Zhirenxing”)
18,950,440
3.61%
3.49%
29 March 2027
Shenzhen Xianzhikong Enterprise 
Management Partnership (Limited 
Partnership)/深圳市獻智控企
業管理合夥企業(有限合夥) 
(“Xianzhikong”)
7,774,540
1.48%
1.43%
29 March 2027
Foshan Zhirenying Enterprise 
Management Partnership (Limited 
Partnership)/佛山市智人營企業管理
有限合夥(有限合夥) (“Zhirenying”)
3,659,970
0.70%
0.67%
29 March 2027
Subtotal
159,742,800
30.39%
29.39%
Notes:
1. 
After taking into account the full exercise of the Offer Size Adjustment Option and assuming the Over-
allotment Option is not exercised.
2. 
The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws and 
relevant lock-up undertakings as disclosed in the Prospectus.

<<<PAGE 12>>>
12
Key Persons (as defined under Rule 18C.14 of the Listing Rules)
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon listing
Number of H – 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon listing
% of total issued 
H-shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon listing Note 1
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon listing Note 1
Last day 
subject to 
the lock-up 
undertakings 
Note 2
Mr. Wang
14,218,750
14,218,750
2.71%
2.62%
29 March 2027
Mr. Zhang
2,031,250
2,031,250
0.39%
0.37%
29 March 2027
Zhirentuan Note 3
113,107,850
113,107,850
21.52%
20.81%
29 March 2027
Zhirenxing Note 4/Note 7
18,950,440
18,950,440
3.61%
3.49%
29 March 2027
Xianzhikong Note 5
7,774,540
7,774,540
1.48%
1.43%
29 March 2027
Zhirenying Note 6
3,659,970
3,659,970
0.70%
0.67%
29 March 2027
Zhirenxue Note 4/Note 8
8,617,800
–
–
1.59%
29 March 2027
Zhirenle Note 4/Note 9
5,000,000
–
–
0.92%
29 March 2027
Zhirenju Note 4/Note 10
2,500,000
–
–
0.46%
29 March 2027
Zhirenyun Note 4/Note 11
1,910,000
–
–
0.35%
29 March 2027
Subtotal
159,742,800
30.39%
29.39%
Notes:
1. 
After taking into account the full exercise of the Offer Size Adjustment Option and assuming the Over-
allotment Option is not exercised.
2. 
Each of such core R&D members of the Company and/or Directors has undertaken that the partnership 
interests held by him/her in these partnerships are subject to a lock-up period of 12 months after the Listing 
Date (the “Partnership Lock-up Period”) pursuant to Rule 18C.14 of the Listing Rules. According to 
partnership agreements of these partnerships, transfer/disposal of partnership interests therein by the 
partners shall be subject to approval by the respective general partner of such partnerships (i.e. Zhirentuan). 
Zhirentuan has confirmed that it will not approve any transfer/disposal of such partnership interests by the 
core R&D members of the Company and/or Directors during the Partnership Lock-up Period.
3. 
As co-founders, Mr. Wang and Mr. Zhang decided to hold majority of their interest in the Company via 
a partnership (i.e. Zhirentuan) with both of them involved as partners, to enable the consolidation and 
stabilization of the founders’ voting rights, thereby enhancing corporate governance alignment. Mr. Wang 
and Mr. Zhang, as limited partners, hold approximately 81.14% and 11.73% partnership interests therein, 
respectively.

<<<PAGE 13>>>
13
4. 
In light of the requirement on number of partners of a partnership under PRC laws and regulations, each 
of Zhirenxing, Zhirenle, Zhirenju, Zhirenxue, and Zhirenyun was established as an Employee Incentive 
Platform with Zhirentuan (which is controlled by Mr. Wang) as the general partner. In addition, Mr. Wang 
and Mr. Zhang, as Directors and core R&D members, who have led and contributed to the development of the 
Company were granted batches of incentives in Employee Incentive Platforms. See “Appendix IV — Statutory 
and General Information — 5. Employee Incentive Schemes” in the Prospectus.
5. 
For purpose of further consolidating control over the Company by Mr. Wang, thereby further enhancing the 
decision-making efficiency at the general meetings of the Company and ensure the effective implementation 
of the strategy of the Group, Wang Xianli and Mr. Wang agreed for Zhirentuan to act as the general partner 
of Xianzhikong. Mr. Wang and Mr. Wang Xianli, as limited partners, hold approximately 0.78% and 76.91% 
partnership interests therein, respectively.
6. 
Zhirenying was established as an employee shareholding platform to provide employees opportunities to invest 
in the Company, with Zhirentuan as the general partner for further control consolidating by Mr. Wang. Du 
Weimin (one of our core R&D members), as a limited partner, holds approximately 1.07% partnership interests 
therein.
7. 
Among the limited partners, Zhang Yingtao (an executive Director), Hao Yu (one of our core R&D members), 
Gao Yuebo (one of our core R&D members), Zhang Peng (one of our core R&D members), Wang Xianli (our 
connected person), Zhao Yi (our connected person) hold approximately 19.77%, 3.6%, 3.28%, 2.44%, 12.59% 
and 12.53% partnership interests therein, respectively.
8. 
Among the limited partners, Mr. Wang (one of the Founders and Controlling Shareholders, an executive 
Director, the chairperson of the Board and the general manager of the Company), Zhang Yingtao (an executive 
Director), Hao Yu (one of our core R&D members), Gao Yuebo (one of our core R&D members), Zhang Peng 
(one of our core R&D members), Zhao Yi (our connected person) hold approximately 1.54%, 10.44%, 2.90%, 
3.48%, 3.83%, and 4.64% partnership interests therein, respectively.
9. 
Among the limited partners, Mr. Wang (one of the Founders and Controlling Shareholders, an executive 
Director, the chairperson of the Board and the general manager of the Company), Mr. Zhang (one of the 
Founders and Controlling Shareholders, an executive Director and the chief technology officer of the 
Company), Du Weimin (one of our core R&D members) hold approximately 4.20%, 10.00% and 5.00% 
partnership interests therein, respectively.
10. 
Among the limited partners, Mr. Wang (one of the Founders and Controlling Shareholders, an executive 
Director, the chairperson of the Board and the general manager of the Company) holds approximately 19.00% 
partnership interests therein.
11. 
Among the limited partners, Mr. Wang (one of the Founders and Controlling Shareholders, an executive 
Director, the chairperson of the Board and the general manager of the Company) holds approximately 42.30% 
partnership interests therein.

<<<PAGE 14>>>
14
Pathfinder SIIs
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon listing
Number of H 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon listing
% of total issued 
H-shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon listing Note 1
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon listing Note 1
Last day 
subject to 
the lock-up 
undertakings 
Note 2
Han’s Laser 
Technology Industry 
Group Co., Ltd./大族
激光科技產業集團股
份有限公司
75,586,735
75,586,735
14.38%
13.90%
29 March 2027
Shenzhen Zhongshen 
Xinchuang Equity 
Investment Partnership 
(Limited Partnership)/
深圳中深新創股權投
資合夥企業(有限合夥)
33,163,265
33,163,265
6.31%
6.10%
29 March 2027
Zhaoying (Zhucheng) 
Venture Capital 
Partnership (Limited 
Partnership)/招盈(諸
城)創業投資合夥企業
(有限合夥)
11,054,420
11,054,420
2.10%
2.03%
29 March 2027
Foshan Zhaoke 
Innovation Intelligent 
Industry Investment 
Fund Partnership 
(Limited Partnership)/
佛山市招科創新智能
產業投資基金合夥企
業(有限合夥)
11,054,420
11,054,420
2.10%
2.03%
29 March 2027
Subtotal
130,858,840
130,858,840
24.90%
24.07%
Notes:
1. 
Each of the Shareholders listed in the above table is a pathfinder SII of the Company as defined under 
Chapter.
2. 
2.5 of the Guide for New Listing Applicants. Please refer to the section headed “History, Development and 
Corporate Structure – Capitalization of our Company” in the Prospectus for further details.
3. 
All Pathfinder SIIs shall not dispose of any of the Shares held by them within the 12 months following the 
Listing Date as required under the applicable PRC laws and relevant lock-up undertakings as disclosed in the 
Prospectus. In accordance with Rule 18C.14(2) of the Listing Rules, the required lock-up period commences 
on the date by reference to which disclosure of its shareholding is made in the Prospectus and ends on the 
date which is six months from the Listing Date.

<<<PAGE 15>>>
15
Pre-IPO Investors
Name
Number of H – 
shares held in 
the Company 
subject to lock-
up undertakings 
upon listing
% of total issued 
H-shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon listing Note 1
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon listing Note 1
Last day subject 
to the lock-up 
undertakings Note 2
Beijing Guoke Ruihua Phase IV 
Equity Investment Fund Partnership 
Enterprise (Limited Partnership)/北
京國科瑞華四期股權投資基金合夥
企業(有限合夥)
9,735,015
1.85%
1.79%
29 March 2027
Shenzhen Baoshi Xinqiao Guoke 
Ruihua Private Equity Investment 
Fund Partnership Enterprise (Limited 
Partnership)/深圳市寶實新橋國科瑞
華私募股權投資基金合夥企業(有限
合夥)
9,735,015
1.85%
1.79%
29 March 2027
Mr. Liang Jianhong/梁建宏
18,804,660
3.58%
3.46%
29 March 2027
Fujian Min’an Tongfu Enterprise 
Management Partnership (Limited 
Partnership)/福建民安同富企業管理
合夥企業(有限合夥)
18,658,890
3.55%
3.43%
29 March 2027
Suzhou Tengxin Venture Capital 
Partnership (Limited Partnership)/蘇
州藤信創業投資合夥企業(有限合
夥)
11,661,810
2.22%
2.15%
29 March 2027
Yantai Xinzhen Tianying Equity 
Investment Center (Limited 
Partnership)/煙臺信貞添盈股權投資
中心(有限合夥)
11,054,420
2.10%
2.03%
29 March 2027
Shenzhen Zhongxiaodan Venture 
Capital Co., Ltd./深圳市中小擔創業
投資有限公司
3,887,270
0.74%
0.72%
29 March 2027

<<<PAGE 16>>>
16
Name
Number of H – 
shares held in 
the Company 
subject to lock-
up undertakings 
upon listing
% of total issued 
H-shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon listing Note 1
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon listing Note 1
Last day subject 
to the lock-up 
undertakings Note 2
Shenzhen Talent Innovation 
Entrepreneurship No. 3 Phase II 
Equity Investment Fund Partnership 
(Limited Partnership)/深圳市人才創
新創業三號二期股權投資基金合夥
企業(有限合夥)
3,887,270
0.74%
0.72%
29 March 2027
Shenzhen Toposcend Zhongxiaowei 
Venture Capital Enterprise (Limited 
Partnership)/深圳市投控東海中小微
創業投資企業(有限合夥)
6,632,655
1.26%
1.22%
29 March 2027
Guangdong Yuecai Industrial 
Investment Fund Partnership 
(Limited Partnership)/廣東粵財產業
投資基金合夥企業(有限合夥)
4,719,388
0.90%
0.87%
29 March 2027
Guangzhou Chuangying Jianke 
Investment Partnership (Limited 
Partnership)/廣州創盈健科投資合夥
企業(有限合夥)
28,317
0.01%
0.01%
29 March 2027
Foshan Pengxia Jufu Enterprise 
Management Partnership (Limited 
Partnership)/佛山市鵬廈聚富企業管
理合夥企業(有限合夥)
10,402,330
1.98%
1.91%
29 March 2027
Shenzhen Qielou Xingwen 
Management Partnership (Limited 
Partnership)/深圳鏤行穩管理合夥企
業(有限合夥)
9,438,775
1.80%
1.74%
29 March 2027
Shanghai Huaqi Investment 
Management Partnership (Limited 
Partnership)/上海畫琪投資管理合夥
企業(有限合夥)
4,737,610
0.90%
0.87%
29 March 2027

<<<PAGE 17>>>
17
Name
Number of H – 
shares held in 
the Company 
subject to lock-
up undertakings 
upon listing
% of total issued 
H-shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon listing Note 1
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon listing Note 1
Last day subject 
to the lock-up 
undertakings Note 2
Shenzhen Qunte Investment Co., 
Ltd./深圳市群特投資有限責任公司
4,413,988
0.84%
0.81%
29 March 2027
Wuxi High-tech Zone Xindongneng 
Industry Development Fund (Limited 
Partnership)/無錫高新區新動能產業
發展基金(有限合夥)
4,719,390
0.90%
0.87%
29 March 2027
Founder Securities Investment Co., 
Ltd./方正證券投資有限公司
4,421,770
0.84%
0.81%
29 March 2027
Shenzhen Shuohang Enterprise 
Management Partnership (Limited 
Partnership)/深圳市碩航企業管理合
夥(有限合夥)
3,178,760
0.60%
0.58%
29 March 2027
Ms. Liu Hong/劉宏
1,751,547
0.33%
0.32%
29 March 2027
Beijing CAS Zhengdao Investment 
Center (Limited Partnership)/北京國
科正道投資中心(有限合夥)
196,660
0.04%
0.04%
29 March 2027
Subtotal
142,065,540
27.03%
26.13%
Notes:
1. 
After taking into account the full exercise of the Offer Size Adjustment Option and assuming the Over-allotment Option is not exercised.
2. 
The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws.

<<<PAGE 18>>>
18
Cornerstone Investors
Name
Number of H – 
shares held in 
the Company 
subject to lock-
up undertakings 
upon listing
% of total issued 
H-shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon listing Note 1
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon listing Note 1
Last day subject 
to the lock-up 
undertakings Note 2
HHLR Advisors, Ltd.
13,802,400
2.63%
2.54%
29 September 2026
GF Fund
13,802,200 Note 3
2.63%
2.54%
29 September 2026
Morgan Stanley & Co. International 
plc
4,600,800
0.88%
0.85%
29 September 2026
Samson Group Limited/晟信集團有
限公司
2,941,000
0.56%
0.54%
29 September 2026
Haojun Investment and HTCI (in 
connection with Haojun Investment 
OTC Swaps)
2,667,800
0.51%
0.49%
29 September 2026
Eternal Summer Consulting 
Company Ltd.
2,300,400
0.44%
0.42%
29 September 2026
Shrewd Pioneer Limited
2,300,400
0.44%
0.42%
29 September 2026
Richfirm (Hong Kong) Development 
Limited/全順(香港)發展有限公司
1,470,400
0.28%
0.27%
29 September 2026
VVC Technology Fund Ltd.
1,380,200
0.26%
0.25%
29 September 2026
Subtotal
45,265,600
8.61%
8.33%
Notes:
1. 
After taking into account the full exercise of the Offer Size Adjustment Option and assuming the Over-
allotment Option is not exercised.
2. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on 29 
September 2026. The Cornerstone Investors will cease to be prohibited from disposing of or transferring H 
Shares subscribed for pursuant to the relevant cornerstone investment agreements after the indicated date.
3. 
The discrepancy between final number of allocated Offer Shares and disclosure in the Prospectus was due to 
rounding adjustments.

<<<PAGE 19>>>
19
PLACEE CONCENTRATION ANALYSIS**
Placees*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over – 
allotment 
Option 
is fully 
exercised and 
new H Shares 
are issued)
Allotment as 
% of total 
Offer Shares 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised and 
new H Shares 
are issued)
Number of H 
Shares held 
upon Listing
% of total 
issued H 
Share capital 
upon Listing 
(assuming no 
exercise of 
the Over – 
allotment 
Option)
% of total 
issued H 
share capital 
upon Listing 
(assuming 
the Over – 
allotment 
Option 
is fully 
exercised and 
new H Shares 
are issued)
% of total 
issued Share 
capital upon 
Listing 
(assuming no 
exercise of 
the Over – 
allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over – 
allotment 
Option 
is fully 
exercised and 
new H Shares 
are issued)
Top 1
13,802,400
17.98%
15.22%
14.86%
12.92%
13,802,400
2.63%
2.56%
2.54%
2.48%
Top 5
42,323,800
55.15%
46.67%
45.56%
39.62%
42,323,800
8.05%
7.84%
7.79%
7.59%
Top 10
54,651,000
71.21%
60.27%
58.83%
51.15%
54,651,000
10.40%
10.13%
10.05%
9.80%
Top 25
74,413,400
96.96%
82.06%
80.10%
69.65%
74,413,400
14.16%
13.79%
13.69%
13.35%
Notes
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
** 
Taking into account the full exercise of the Offer Size Adjustment Option.
H SHAREHOLDER CONCENTRATION ANALYSIS**
H Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming 
no exercise 
of the Over-
allotment
Option)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over – 
allotment 
Option 
is fully 
exercised and 
new
H Shares are 
issued)
Allotment as 
% of total 
Offer Shares 
(assuming no 
exercise of 
the Over-
allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised and 
new H Shares 
are issued)
Number of H 
Shares held 
upon Listing
% of total 
issued H 
Share capital 
upon Listing 
(assuming no
exercise of 
the Over – 
allotment 
Option)
% of total 
issued H 
Share capital 
upon Listing 
(assuming 
the Over – 
allotment 
Option 
is fully 
exercised and 
new H Shares 
are issued)
% of total 
issued Share 
capital upon 
Listing 
(assuming no
exercise of 
the Over – 
allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over – 
allotment 
Option 
is fully 
exercised and 
new H Shares 
are issued)
Top 1
–
0.00%
0.00%
0.00%
0.00%
159,742,800
30.39%
29.61%
29.39%
28.65%
Top 5
1,470,400
1.92%
1.62%
1.58%
1.38%
311,226,940
59.22%
57.69%
57.25%
55.82%
Top 10
29,075,000
37.88%
32.06%
31.30%
27.21%
395,765,120
75.30%
73.36%
72.80%
70.99%
Top 25
54,003,800
70.37%
59.55%
58.13%
50.55%
484,722,773
92.23%
89.85%
89.17%
86.94%
Notes
* 
Ranking of H Shareholders is based on the number of H Shares (of all classes) held by the H Shareholders upon 
Listing.
** 
Taking into account the full exercise of the Offer Size Adjustment Option.

<<<PAGE 20>>>
20
SHAREHOLDER CONCENTRATION ANALYSIS**
Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming 
no exercise 
of the Over-
allotment
Option)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over – 
allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Allotment as 
% of total 
Offer Shares 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Number of H 
Shares held 
upon Listing
Number of 
total shares 
held upon 
Listing
% of total 
issued Share 
capital upon 
Listing 
(assuming no 
exercise of 
the Over – 
allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over – 
allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Top 1
0
0.00%
0.00%
0.00%
0.00%
159,742,800
17,777,0600
32.70%
31.89%
Top 5
1,470,400
1.92%
1.62%
1.58%
1.38%
311,226,940
329,254,740
60.57%
59.06%
Top 10
29,075,000
37.88%
32.06%
31.30%
27.21%
395,765,120
413,792,920
76.12%
74.22%
Top 25
54,003,800
70.37%
59.55%
58.13%
50.55%
484,722,773
502,750,573
92.49%
90.17%
Notes
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.
** 
Taking into account the full exercise of the Offer Size Adjustment Option.
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 227,070 valid 
applications made by the public will be conditionally allocated on the basis set out below:
NO. OF H SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOCATION/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTED OF THE 
TOTAL NO. OF H 
SHARES APPLIED FOR
POOL A
200
46,102
2,306 out of 46,102 applicants to receive 200 H Shares
5.00%
400
39,888
3,192 out of 39,888 applicants to receive 200 H Shares
4.00%
600
7,784
818 out of 7,784 applicants to receive 200 H Shares
3.50%
800
3,614
434 out of 3,614 applicants to receive 200 H Shares
3.00%
1,000
5,085
712 out of 5,085 applicants to receive 200 H Shares
2.80%
1,200
2,948
425 out of 2,948 applicants to receive 200 H Shares
2.40%
1,400
2,384
368 out of 2,384 applicants to receive 200 H Shares
2.21%
1,600
2,225
356 out of 2,225 applicants to receive 200 H Shares
2.00%
1,800
1,340
225 out of 1,340 applicants to receive 200 H Shares
1.87%
2,000
14,358
2,513 out of 14,358 applicants to receive 200 H Shares
1.75%
3,000
3,669
695 out of 3,669 applicants to receive 200 H Shares
1.26%
4,000
3,341
649 out of 3,341 applicants to receive 200 H Shares
0.97%
5,000
5,349
1,070 out of 5,349 applicants to receive 200 H Shares
0.80%
6,000
2,907
594 out of 2,907 applicants to receive 200 H Shares
0.68%
7,000
1,552
326 out of 1,552 applicants to receive 200 H Shares
0.60%
8,000
1,503
325 out of 1,503 applicants to receive 200 H Shares
0.54%

<<<PAGE 21>>>
21
NO. OF H SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOCATION/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTED OF THE 
TOTAL NO. OF H 
SHARES APPLIED FOR
POOL A
9,000
1,275
287 out of 1,275 applicants to receive 200 H Shares
0.50%
10,000
9,596
2,208 out of 9,596 applicants to receive 200 H Shares
0.46%
20,000
7,340
2,056 out of 7,340 applicants to receive 200 H Shares
0.28%
30,000
5,167
1,628 out of 5,167 applicants to receive 200 H Shares
0.21%
40,000
3,820
1,331 out of 3,820 applicants to receive 200 H Shares
0.17%
50,000
3,266
1,199 out of 3,266 applicants to receive 200 H Shares
0.15%
60,000
3,282
1,379 out of 3,282 applicants to receive 200 H Shares
0.14%
70,000
1,789
814 out of 1,789 applicants to receive 200 H Shares
0.13%
80,000
1,835
881 out of 1,835 applicants to receive 200 H Shares
0.12%
90,000
1,510
748 out of 1,510 applicants to receive 200 H Shares
0.11%
100,000
9,067
4,534 out of 9,067 applicants to receive 200 H Shares
0.10%
200,000
9,197
8,320 out of 9,197 applicants to receive 200 H Shares
0.09%
Total:
201,193
Total number of Pool A successful applicants: 40,393
POOL B
300,000
11,350
200 H Shares plus 2,270 out of 11,350 applicants to receive an additional 200 H Shares
0.08%
400,000
3,426
200 H Shares plus 1,236 out of 3,426 applicants to receive an additional 200 H Shares
0.07%
500,000
2,170
200 H Shares plus 1,086 out of 2,170 applicants to receive an additional 200 H Shares
0.06%
600,000
1,612
200 H Shares plus 1,007 out of 1,612 applicants to receive an additional 200 H Shares
0.05%
700,000
960
200 H Shares plus 709 out of 960 applicants to receive an additional 200 H Shares
0.05%
800,000
870
200 H Shares plus 733 out of 870 applicants to receive an additional 200 H Shares
0.05%
900,000
674
200 H Shares plus 633 out of 674 applicants to receive an additional 200 H Shares
0.04%
1,000,000
1,767
400 H Shares
0.04%
1,500,000
1,030
400 H Shares plus 437 out of 1,030 applicants to receive an additional 200 H Shares
0.03%
2,019,600
2,018
400 H Shares plus 1,589 out of 2,018 applicants to receive an additional 200 H Shares
0.03%
Total:
25,877
Total number of Pool B successful applicants: 25,877
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 22>>>
22
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.
The Directors and the Overall Coordinators confirm that at least 50% of the total number of the 
Offer Shares (excluding any Shares issued and/or to be issued pursuant to the exercise of the Offer 
Size Adjustment Option and/or Over-allotment Option) have been allocated to and taken up by 
independent price setting investors in compliance with Rule 18C.08 of the Listing Rules.
The Directors further confirm that at least 20% of the issued share capital of the Company will be 
held by sophisticated independent investors at the time of Listing in compliance with Chapter 2.5 
of the Guide for New Listing Applicants.
OTHERS/ADDITIONAL INFORMATION
Offer Size Adjustment Option
The Offer Size Adjustment Option has been exercised by the Company in full, pursuant to which 
the Company is issuing and allotting 12,117,600 additional H Shares, representing approximately 
15.0% of the total number of H Shares initially available under the Global Offering, at the final 
Offer Price.
Accordingly, the total number of Offer Shares finally available under the Global Offering (after 
taking into account the full exercise of the Offer Size Adjustment Option and before any exercise 
of the Over-allotment Option) that would be allotted and issued by the Company is 92,902,600 
Offer Shares and the total issued share capital of the Company upon Listing (after taking into 
account the full exercise of the Offer Size Adjustment Option and before any exercise of the 
Over-allotment Option) will be 543,597,580 Shares.
The additional Offer Shares issued pursuant to the Offer Size Adjustment Option will be allocated 
to the International Offering.
Reallocation
As (i) the Hong Kong Public Offering is oversubscribed by more than 50 times and (ii) the 
reallocation pursuant to Chapter 4.14 of the Guide for New Listing Applicants as described 
in the section headed “Structure of the Global Offering – The Hong Kong Public Offering – 
Reallocation” of the Prospectus is exercised, the clawback arrangement is triggered and Offer 
Shares were reallocated to the Hong Kong Public Offering from the International Offering, so that 
the total number of Offer Shares available under the Hong Kong Public Offering is 16,157,000 
Offer Shares, representing 20% of the Offer Shares initially available under the Global Offering, 
assuming the Offer Size Adjustment Option is not exercised.

<<<PAGE 23>>>
23
Allocations of Further H Shares to close associates of existing shareholders as a cornerstone 
investor and a placee with a waiver from strict compliance with Rule 10.04 of the Listing 
Rules and consent under paragraph 1C(2) of the Placing Guidelines
The Company has applied to, and the Stock Exchange has granted, a waiver from strict compliance 
with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the Placing Guidelines 
to allocate further H Shares in the International Offering to a close associate of existing 
shareholder as cornerstone investor, subject to the following conditions:
(a) 
the Company will comply with the public float requirements of Rules 19A.13A and 18C.08 
of the Listing Rules and the free float requirements of Rule 19A.13C of the Listing Rules;
(b) 
the Company and the Joint Sponsors confirm that no preferential treatment has been, nor 
will be directly or indirectly, given to Richfirm as a cornerstone investor by virtue of its 
relationship with the Company in any allocation in the Global Offering, other than the 
preferential treatment of assured entitlement under the cornerstone investment at the Offer 
Price and the terms are substantially the same as other cornerstone investors; and;
(c) 
details of the subscription of the Offer Shares by Richfirm as Cornerstone Investor under the 
Global Offering are disclosed in the Prospectus, and details of the allocation will be disclosed 
in the allotment results announcement of our Company. For further information about the 
relevant cornerstone investments, please refer to the section headed “Cornerstone Investors” 
in the Prospectus.
The Company has applied to, and the Stock Exchange has granted, a waiver from strict compliance 
with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the Placing Guidelines 
to allocate further H Shares in the International Offering to a close associate of existing 
shareholder as placee, subject to the following conditions:
(a) 
the Company will comply with the public float requirements of Rules 19A.13A and 18C.08 
of the Listing Rules and the free float requirements of Rule 19A.13C of the Listing Rules; 
and
(b) 
the Company and the Joint Sponsors confirm that no preferential treatment has been, nor will 
be directly or indirectly, given to Yihe No. 22 as a placee by virtue of its relationship with 
the Company in any allocation in the Global Offering.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to close associates of existing shareholders as a 
cornerstone investor and a placee, please refer to the section headed “Allotment Results Details – 
International Offering – Allotees with Waivers/Consents Obtained” in this announcement.

<<<PAGE 24>>>
24
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines. Please refer to the section headed 
“Allotment Results Details – International Offering – Allotees with Waivers/Consents Obtained” in 
this announcement for details. The Company has applied to the Stock Exchange for, and the Stock 
Exchange has granted, a consent under paragraph 1C(1) of the Placing Guidelines to permit the 
Company to allocate such Offer Shares in the International Offering to the connected clients. The 
allocation of Offer Shares to such connected clients is in compliance with all the conditions under 
the consent granted by the Stock Exchange. Details of the placement to connected clients are set 
out below.
Part A – Connected Clients holding the beneficial interest of the Offer Shares on a 
non-discretionary basis on behalf of independent third parties
No.
Connected 
Distributor
Connected 
Client
Relationship 
with the 
Connected 
Distributor
Identities of 
the ultimate 
beneficial owners 
of the Offer 
Shares or, where 
applicable, details 
of the structured 
products under 
which the 
subscription by 
the Connected 
Client was made 
(e.g. OTC total 
return swaps)
Whether the 
Connected 
Client is a 
collective 
investment 
scheme 
which is not 
authorised by 
the SFC or 
is expected 
to hold the 
Offer Shares 
on behalf of 
such scheme
Number of 
Offer Shares 
allocated to 
the connected 
client
Approximate 
percentage 
of total 
number of 
Offer Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
percentage of 
total Shares 
in issue 
immediately 
following the 
completion 
of Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
1.
Huatai Financial 
Holdings (Hong 
Kong) Limited 
(“HTFH”)
Huatai Capital 
Investment 
Limited 
(“HTCI”)
Members 
of the same 
group
Please refer to 
Note 1
No
8,668,600
9.33%
1.59%
2.
China International 
Capital 
Corporation 
Hong Kong 
Securities Limited 
(“CICCHKS”)
CICC 
Financial 
Trading 
Limited 
(“CICC FT”)
Members 
of the same 
group
Please refer to 
Note 2
No
35,200
0.04%
0.01%

<<<PAGE 25>>>
25
Part B – Connected Clients holding the beneficial interest of the Offer Shares on a 
discretionary basis on behalf of independent third parties
No.
Connected 
Distributor
Connected Clients
Relationship 
with the 
Connected 
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
Maximum 
number of 
Offer Shares 
(rounded down 
to nearest 
whole board lot 
of 10 Shares) to 
be allocated to 
the connected 
client
Approximate 
percentage 
of total 
number of 
Offer Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
percentage of 
total Shares in 
issue immediately 
following the 
completion of Global 
Offering (assuming 
the Over-allotment 
Option is not 
exercised)
3.
ICBC International 
Securities Limited 
(“ICBCI”)
ICBC UBS Asset 
Management Co., 
(International) Ltd. 
(“ICBC UBS”) (Note 3)
Members of the 
same group
No
311,000
0.33%
0.06%
4.
ICBCI
ICBC International 
Fund Management 
Limited (“ICBCI 
FM”) (Note 4)
Members of the 
same group
No
13,800
0.01%
0.00%
5.
ICBCI
ICBC UBS Asset 
Management 
(International) 
Company Limited 
(“ICBC UBS 
International”) (Note 5)
Members of the 
same group
No
100,600
0.11%
0.02%
6.
Citic Securities 
Brokerage (HK) 
Limited (“CITIC 
Brokerage HK”)
China Asset 
Management (Hong 
Kong) Limited 
(“China AMC 
HK”) (Note 6)
Members of the 
same group
No
411,600
0.44%
0.08%
7.
China Merchants 
Securities (HK) 
Co., Limited 
(“CMS”)
Bosera Asset 
Management 
(International) 
Co., Limited 
(“Bosera Asset 
Management”) (Note 8)
Members of the 
same group
No
345,000
0.37%
0.06%

<<<PAGE 26>>>
26
Notes:
1. 
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public 
offerings (“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products issued by 
appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. In 
connection with such products, the licensed domestic securities firms, through their Hong Kong affiliates, may 
participate in Hong Kong IPOs either as placees or cornerstone investors (the “Cross-border Derivatives 
Trading Regime”).
Huatai Securities Co., Ltd. (“Huatai Securities”), the shares of which are listed on both the Shanghai Stock 
Exchange (stock code: 601688) and the Stock Exchange (stock code: 6886), is one of the domestic securities 
firms licensed to undertake cross-border derivatives trading activities. Huatai Securities entered into an ISDA 
agreement (the “ISDA Agreement”) with its indirectly wholly-owned subsidiary, HTCI, to set out the principal 
terms of any future total return swap between Huatai Securities and HTCI.
HTFH is a distributor of the Global Offering. Pursuant to the ISDA Agreement, HTCI, which intends 
to participate in the Global Offering as a placee, will hold the beneficial interest of the Offer Shares on 
a non-discretionary basis as the single underlying holder under a back-to-back total return swap (the 
“Back-to-back TRS”) to be entered by HTCI in connection with a Client TRS (as defined below) placed by 
and fully funded (i.e. with no financing provided by HTCI) by the Huatai Ultimate Clients (as defined below), 
by which, HTCI will, subject to customary fees and commissions, pass the full economic exposure of the 
Offer Shares ultimately to the Huatai Ultimate Clients, which in effect, HTCI will hold the beneficial interest 
of the Offer Shares on behalf of the Huatai Ultimate Clients. HTFH and HTCI are indirectly wholly-owned 
subsidiaries of Huatai Securities. Accordingly, HTCI is considered as a “connected client” of HTFH pursuant to 
paragraph 1B(7) of the Placing Guidelines.
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the “Huatai Ultimate 
Clients”) cannot directly subscribe for the Offer Shares but may invest in derivative products issued by domestic 
securities firms licenced to undertake cross-border derivatives trading activities, such as Huatai Securities, 
with the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, the Huatai 
Ultimate Clients, through its investment manager, will place a total return swap order (the “Client TRS”) with 
Huatai Securities in connection with the Company’s IPO and Huatai Securities will place a Back-to-back TRS 
order to HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the Back-to-back TRS, 
HTCI participates in the Company’s IPO and subscribes the Offer Shares through placing order with HTFH 
during the International Offering.
To the best of our knowledge and after making all reasonable enquiries, save for Yihe No. 22 Private Securities 
Investment Fund (頤和 22 期私募證券投資基金), each of the other Huatai Ultimate Clients is an independent 
third party of (i) the Company and their respective close associates thereof, and (ii) HTCI, HTFH and the 
companies which are members of the same group of HTCI.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in connection 
with the Client TRS order placed by the Huatai Ultimate Clients. Pursuant to the terms of the contracts of the 
Back-to-back TRS and the Client TRS, during the tenor of the Back-to-back TRS and the Client TRS, subject 
to customary fees and commissions, all economic returns of the Offer Shares will be ultimately passed to the 
Huatai Ultimate Clients through the Back-to-back TRS and the Client TRS and all economic loss shall be 
ultimately borne by the Huatai Ultimate Clients. HTCI will not take any economic return or bear any economic 
loss in relation to the Offer Shares.
Investment in the Back-to-back TRS and the Client TRS is similar to the investment in a qualified domestic 
institutional investor fund (“QDII”) in the way that the Huatai Ultimate Clients would reap all the economic 
benefits of the underlying Offer Shares, except that a QDII fund would pass through the exchange rate exposure 
on both the notional value of the investment and the profit and loss of the investment. In contrast, the profit and 
loss of the Back-to-back TRS and the Client TRS factor into account the fluctuation in RMB exchange rate upon 
termination of the Client TRS by converting the profit and loss using the current exchange rate at the time of 
termination. As such, the Huatai Ultimate Clients would bear the exchange rate exposure of the profit and loss 
on settlement date.

<<<PAGE 27>>>
27
The Huatai Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time 
from the issue date of the Client TRS which should be on or after the date on which the Offer Shares are listed 
on the Stock Exchange at their own discretion. Upon the termination upon maturity or early termination of the 
Client TRS by the Huatai Ultimate Clients, HTCI will dispose the Offer Shares on the secondary market and 
the Huatai Ultimate Clients will receive a final settlement amount in cash in accordance with the terms and 
conditions of the Back-to-back TRS and the Client TRS which should have taken into account all the economic 
returns or economic loss in relation to the Offer Shares. If upon the maturity of the Client TRS, the Huatai 
Ultimate Clients intend to extend the investment period, subject to further agreement between Huatai Securities 
and the relevant Huatai Ultimate Clients, the term of the Client TRS could be extended by way of a new 
issuance or a tenor extension. Accordingly, Huatai Securities will extend the term of the Back-to-back TRS by 
way of a new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass 
through the economic exposure to the Huatai Ultimate Clients, each being an onshore client who places a Client 
TRS order with Huatai Securities in connection with the IPO of the Company. HTCI will not exercise the voting 
right of the Offer Shares during the tenor of the Back-to-back TRS.
During the life of the Client TRS and Back-to-back TRS, HTCI may continue to hold the Offer Shares in its 
custodian account, or to hold some or all of the Offer Shares in a prime brokerage account for stock borrowing 
purposes, where HTCI will lend out its holding of underlying Offer Shares in the form of stock borrowing loans 
consistent with market practice to lower its finance costs, provided that HTCI has the ability to call back the 
Offer Shares on loan at any time in order to satisfy its obligations under the Back-to-back TRS to ensure the 
economic interests are ultimately passed to the Huatai Ultimate Clients.
The Huatai Ultimate Clients for purpose of this placing subscription are as follows:
(i) 
Ningbo Meishan Free Trade Port Zone Haojun Investment Management Co., Ltd. (寧波梅山保稅港區灝
浚投資管理有限公司) (“Haojun Investment”) and the ultimate beneficial owners are Shi Yu and Chen 
Chen, each holding as to 60% and 40% of the interests, respectively. Among the 8,668,600 Offer Shares 
allocated to HTCI, 2,667,800 Offer Shares will be beneficially owned by Haojun Investment.
Haojun Investment is one of the cornerstone investors of the Company. Haojun Investment will place a 
Back-to-back TRS order to HTCI on the terms of the ISDA Agreement. In order to hedge its exposure 
under the Back-to-back TRS, HTCI participates in the Company’s Global Offering and subscribes the 
Offer Shares through placing order with HTFH during the International Offering. For details of Haojun 
Investment and the cornerstone investment in the Company, please refer to the section headed “Haojun 
Investment and HTCI (in connection with Haojun Investment OTC Swaps) - Cornerstone Investors” of 
the Prospectus. After the issuance of the prospectus, HTFH became a distributor of the Global Offering 
and as result HTCI become a connected client of HTFH pursuant to paragraph 1B(7) of the Placing 
Guidelines.
(ii) 
Yihe No. 22 Private Securities Investment Fund (頤和22期私募證券投資基金)(“Yihe No. 22”), a fund 
management by Beijing Palace Asset Management Co., Ltd. (北京頤和久富投資管理有限公司) (“Palace 
AM”). The ultimate beneficial owner and controlling shareholder of Palace AM is Mr. Jiang Renfei (姜任
飛)(“Mr. Jiang”), holding as to 66.07 of the shareholdings interests in Palace AM. Among the 8,668,600 
Offer Shares allocated to HTCI, 4,236,200 Offer Shares will be beneficially owned by Yihe No. 22.
Shenzhen Qielou Xingwen Management Partnership (Limited Partnership) (深圳鍥鏤行穩管理合夥企業
(有限合夥)) (“Qielou Xingwen”) is an existing shareholder of the Company holding as to 2.09% of the 
interests in the Company. Mr. Jiang holds as to 58.1341% of the partnership interests in Qielou Xingwen. 
Accordingly, Palace AM, an entity controlled by Mr. Jiang, is a close associate of the Company’s existing 
shareholder Qielou Xingwen. The Company has applied for a waiver from strict compliance with Rule 
10.04 of the Listing Rules and a consent under paragraph 1C(2) of Appendix F1 to the Listing Rules, to 
permit Yihe No. 22 to participate in the Global Offering.
(iii) 
CSC Financial Co., Ltd., acting on behalf of the CSC “Juejin No. 1” Single Asset Management Plan (中
信建投証券股份有限公司代中信建投掘金 1 號單一資產管理計劃) (“Juejin No. 1”) and the ultimate 
beneficial owner is Kunlun-Western Securities Innovative Institutional Wealth Trust (昆侖西證創新法
人財富信託), which is a pooled funds trust plan established under the laws of the PRC and administered 
by Kunlun Trust Co., Ltd. (昆侖信託有限責任公司) as trustee. The sole settlor of the trust is Western 
Securities Innovation Investment Co., Ltd. (西證創新投資有限公司), which holds 100% of the trust 
benefits. For the avoidance of doubt, CSC Financial Co., Ltd. is an independent third party of CITIC 
Brokerage HK pursuant to paragraph 6 of Chapter 4.15 of the Guide. Among the 8,668,600 Offer Shares 
allocated to HTCI, 1,764,600 Offer Shares will be beneficially owned by Juejin No. 1.

<<<PAGE 28>>>
28
2. 
CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one 
OTC swap transactions (the “OTC Swaps”) with each other and the ultimate clients (the “CICC FT Ultimate 
Clients”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the OTC 
Swaps while the economic risks and returns of the underlying Offer Shares are passed to the CICC FT Ultimate 
Clients, subject to customary fees and commissions. The OTC Swaps will be fully funded by the CICC FT 
Ultimate Clients. During the terms of the OTC Swaps, all economic returns of the Offer Shares subscribed by 
CICC FT will be passed to the CICC FT Ultimate Clients and all economic loss shall be borne by the CICC FT 
Ultimate Clients through the OTC Swaps, and CICC FT will not take part in any economic return or bear any 
economic loss in relation to the Offer Shares. The OTC Swaps are linked to the Offer Shares and the CICC FT 
Ultimate Clients may request CICC FT to redeem it at their own discretion, upon which CICC FT shall dispose 
of the Offer Shares and settle OTC Swaps in cash in accordance with the terms and conditions of the OTC Swap. 
Despite that CICC FT will hold the legal title of the Offer Shares by itself, it will not exercise the voting rights 
attaching to the relevant Offer Shares during the terms of the OTC Swaps according to its internal policy. The 
CICC FT Ultimate Clients for purpose of this placee subscription include Lesheng Qiangye Private Securities 
Investment Fund (樂晟強業私募證券投資基金) and Yuanlesheng Qiangshu Private Securities Investment Fund 
(源樂晟強樹私募證券投資基金), which are funds managed by Tibet Yuanlesheng Asset Management Company 
Limited (西藏源樂晟資產管理有限公司).
To the best of CICC FT’s knowledge having made all reasonable inquiries, each of the CICC FT Ultimate 
Clients is an independent third party of CICC FT, CICCHKS and the companies which are members of the same 
group of companies as CICCHKS.
3. 
ICBCI is a distributor of the Global Offering. ICBC UBS will hold the Offer Shares in its capacity as the 
discretionary fund manager managing the funds on behalf of a discretionary account, who is an independent 
third party of the Company, its subsidiaries, its substantial shareholders, ICBC UBS, ICBCI and the companies 
which are members of the same group of ICBCI.
4. 
ICBCI is a distributor of the Global Offering. New Era Development Fund SPC (新時代發展基金 SPC) - 
Dynamic Allocation Equity Fund SP (“DAEF”) will hold the Offer Shares with ICBCI FM acting as the 
discretionary fund manager for the DAEF. Each of the end investors of DAEF is an independent third party 
of ICBCI FM and ICBCI (distributor of DAEF), both of which are wholly-owned subsidiaries of ICBC 
International Holdings Limited.
5. 
ICBCI is a distributor of the Global Offering. ICBC UBS (International) will hold the Offer Shares in its 
capacity as the discretionary fund manager on behalf of its underlying client, who, and its ultimate beneficial 
owner holding 30% interest or more, is an independent third party of the Company, its subsidiaries, its 
substantial shareholders, ICBC UBS (International), ICBCI and the companies which are members of the same 
group of ICBCI.
6. 
CITIC Brokerage HK is a distributor of the Global Offering. China AMC HK is a member of the same group of 
companies as CITIC Brokerage HK and China AMC HK is therefore considered as a connected client of CITIC 
Brokerage HK pursuant to paragraph 1B(7) of Appendix F1 to the Listing Rules. China AMC HK will hold the 
Offer Shares in its capacity as the discretionary fund manager managing on behalf of its underlying clients, each 
of which is an independent third party of the Company, its subsidiaries, its substantial shareholders, China AMC 
HK, CITIC Brokerage HK and the companies which are members of the same group of CITIC Brokerage HK.
CMS is a broker dealer of the Global Offering. Bosera Asset Management is held as to 55% by Bosera Asset 
Management Co., Ltd. and 45% by China Merchants Fund Management Co., Ltd. China Merchants Securities 
Co., Ltd. currently holds 49% of the equity interest of Bosera Asset Management Co., Ltd. and 45% of the 
equity interest of China Merchants Fund Management Co., Ltd. CMS is a wholly-owned subsidiary of China 
Merchants Securities Co., Ltd. Therefore, Bosera Asset Management is a member of same group of companies 
as CMS.
Bosera Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager managing 
four sub-funds (namely, Bosera Hong Kong Equity Plus Fund (SFC Authorised Fund), Bosera Global Select 
Equity Fund SP, Navigator Technology Limited IPO Mandate and Fortuna Capital Management Limited IPO 
Mandate) on behalf of its underlying client. There is no investor holding 30% or more interest in Bosera Hong 
Kong Equity Plus Fund (SFC Authorised Fund). The only investor holding 30% or more interest in Bosera 
Global Select Equity Fund SP is Zhang Lei (張雷), holding as to 53.67% of the interest. The ultimate beneficial 
owner of Navigator Technology Limited IPO Mandate is Zheng Fuhua (鄭複花). The ultimate beneficial owner 
of Fortuna Capital Management Limited IPO Mandate is Yang Dehui.

<<<PAGE 29>>>
29
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
The Offer Shares are being offered and sold (i) solely to qualified institutional buyers as defined 
in Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under 
the U.S. Securities Act and (ii) outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated 20 March 2026 issued by Guangdong 
Huayan Robotics Co., Ltd. for detailed information about the Global Offering described below 
before deciding whether or not to invest in the Shares thereby being offered.
* 
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and 
on behalf of the Hong Kong Underwriters and Overall Coordinators) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of 
any of the events set out in the paragraph headed “Underwriting – Underwriting Arrangements and Expenses 
– Hong Kong Public Offering – Hong Kong Underwriting Agreement – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected 
to be 30 March 2026).

<<<PAGE 30>>>
30
PUBLIC FLOAT
Pursuant to Rule 19A.13A of the Listing Rules, assuming that the Over-allotment Option is 
not exercised, based on the Offer Price of HK$17.00 per Offer Share, our expected market 
capitalization upon the Listing is HK$9,241 million, and the minimum prescribed public float 
percentage applicable to our Shares is 16.23%.
Immediately following the completion of the Global Offering (following full exercise of the Offer 
Size Adjustment Option and before any exercise of the Over-allotment Option) an aggregate 
of 290,240,245 H Shares, representing approximately 53.39% of the issued share capital of our 
Company will count towards the public float. Therefore, the number of H Shares held in public 
hands is higher than the prescribed percentage of H Shares required to be held in public hands of 
16.23% under Rule 19A.13A(1) of the Listing Rules.
Based on the final Offer Price of HK$17.00 per H Share, the Company satisfies the free float 
requirement under Rule 19A.13C of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering: (i) no 
placee will, individually, be placed more than 10% of the enlarged issued share capital of our 
Company; (ii) there will not be any new substantial Shareholder (as defined in the Listing Rules) 
of our Company; (iii) the three largest public shareholders of the Company do not hold more than 
50% of the H Shares in public hands at the time of the Listing in compliance with Rules 8.08(3) 
and 8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at the time of the 
Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Monday, March 
30, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting – Underwriting Arrangements 
and Expenses – Hong Kong Public Offering – Hong Kong Underwriting Agreement – Grounds for 
Termination” in the Prospectus has not been exercised. Investors who trade the H Shares on the 
basis of publicly available allocation details prior to the receipt of H Share certificates or prior to 
the H Share certificates becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Monday, 
March 30, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Monday, March 30, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 200 H Shares each, and the stock code of the H Shares will 
be 1021.
By order of the Board
Guangdong Huayan Robotics Co., Ltd.
Mr. Wang Guangneng
Executive Director and Chairman of the Board
Hong Kong, March 27, 2026
Directors of the Company named in the application to which this announcement relates are: (i) 
Mr. Wang Guangneng, Mr. Zhang Guoping and Mr. Zhang Yingtao as executive directors; (ii) Dr. 
Fang Bin as non-executive director; and (iii) Dr. Wang Yihua, Dr. Huang Kai and Ms. Gao Li as 
independent non-executive directors.
