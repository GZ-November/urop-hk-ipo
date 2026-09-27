# 配发结果公告抽取任务：2715.HK ESTUN AUTOMATION CO., LTD - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**06/03/2026 21:18**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0306/2026030601391.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2715.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”, 
or the “Hong Kong Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy or completeness and 
expressly disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated February 27, 2026 (the “Prospectus”) of ESTUN AUTOMATION CO., LTD (南京
埃斯頓自動化股份有限公司) (the “Company”). This announcement is made by the order of the board (the “Board”) 
of directors (the “Directors”) of the Company. The Board collectively and individually accept responsibility for the 
accuracy of this announcement.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for any securities. This announcement is not a prospectus. Potential investors should read the Prospectus 
for detailed information about the Global Offering described below before deciding whether or not to invest in 
the Offer Shares. Any investment decision in relation to the Offer Shares should be taken solely in reliance on the 
information provided in the Prospectus.
This announcement is not for release, publication or distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia or any other 
jurisdiction where such distribution is prohibited by laws). This announcement does not constitute or form a part of 
any offer or solicitation to purchase or subscribe for securities in the United States or in any other jurisdictions. The 
securities mentioned herein have not been, and will not be, registered under the United States Securities Act of 1933 
as amended from time to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the 
United States. The securities may not be offered, sold, pledged or otherwise transferred within the United States except 
pursuant to an exemption from the registration requirements of the U.S. Securities Act and in compliance with any 
applicable state securities laws, or outside the United States unless in compliance with Regulation S under the U.S. 
Securities Act. There will be no public offer of securities in the United States.
In connection with the Global Offering, Huatai Financial Holdings (Hong Kong) Limited as stabilizing manager (the 
“Stabilizing Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, to the extent 
permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect 
transactions with a view to stabilizing or supporting the market price of the H Shares at such price, in such amounts 
and in such manners as the Stabilizing Manager, its affiliates or any person acting for it may determine and at a 
level higher than that which might otherwise prevail for a limited period after the Listing Date. However, there is 
no obligation on the Stabilizing Manager (or its affiliates or any person acting for it) to conduct any such stabilizing 
action. Such stabilizing action, if taken, (a) will be conducted at the absolute discretion of the Stabilizing Manager (or 
its affiliates or any person acting for it) and in what the Stabilizing Manager reasonably regards as the best interest of 
the Company, (b) may be discontinued at any time and (c) is required to be brought to an end within 30 days of the last 
day for lodging applications under the Hong Kong Public Offering (which is Friday, April 3, 2026). Such Stabilizing 
action, if taken, may be effected in all jurisdictions where it is permissible to do so, in each case in compliance with 
all applicable laws, rules and regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules 
(Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter 
571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Friday, April 3, 2026). After 
this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of the H 
Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to terms and conditions set out 
in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/
or not resident in Hong Kong. Potential investors of the Offer Shares should note that the Sole Sponsor and the 
Sponsor-Overall Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate 
the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the 
section headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds 
for Termination” in the Prospectus at any time prior to 8:00 a.m. on the Listing Date.

<<<PAGE 2>>>
2
ESTUN AUTOMATION CO., LTD
南京埃斯頓自動化股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the Global 
Offering
:
96,780,000 H Shares (subject to the Over-
allotment Option)
Number of Hong Kong Offer Shares
:
9,678,000 H Shares
Number of International Offer Shares
:
87,102,000 H Shares (subject to the Over-
allotment Option)
Final Offer Price
:
HK$15.36 per H Share, plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
Hong Kong Stock Exchange trading fee of 
0.00565% and AFRC transaction levy of 
0.00015%
Nominal value
:
RMB1.00 per H Share
Stock code
:
2715
Sole Sponsor, Sponsor-Overall Coordinator, Joint Global Coordinator, 
Joint Bookrunner and Joint Lead Manager
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunner and Joint Lead Manager

<<<PAGE 3>>>
3
ESTUN AUTOMATION CO., LTD
南京埃斯頓自動化股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated February 27, 2026 (the “Prospectus”) issued by 
ESTUN AUTOMATION CO., LTD (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
2715
Stock short name
ESTUN
Dealings commencement date
March 9, 2026*
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$15.36
Offer Price Range
HK$15.36-HK$17.00
Offer Price Adjustment
N/A
Offer Shares and Share Capital
Number of Offer Shares
96,780,000
Final Number of Offer Shares in Hong 
Kong Public Offering
9,678,000
Final Number of Offer Shares in 
International Offering (before exercise of 
the Over-allotment Option)
87,102,000
Number of issued Shares upon Listing 
(before exercise of the Over-allotment 
Option)
967,798,453

<<<PAGE 4>>>
4
Over-allocation
Number of Offer Shares over-allocated (Note)
14,517,000
Note: Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases in the 
secondary market at prices that do not exceed the Offer Price or through deferred delivery or a combination 
of these means. In the event the Over-allotment Option is exercised, an announcement will be made on the 
Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$1,486.54 million
 Less:  Estimated listing expenses payable 
based on Final Offer Price
HK$75.01 million
Net proceeds
HK$1,411.53 million
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
27,190
No. of successful applications
6,799
Subscription level
19.67 times
Claw-back triggered
N/A
No. of Offer Shares initially available under 
the Hong Kong Public Offering
9,678,000
Final no. of Offer Shares under the Hong 
Kong Public Offering
9,678,000
% of Offer Shares under the Hong Kong 
Public Offering to the Global Offering
10.00%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can 
refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
87
Subscription Level
3.34 times
No. of Offer Shares initially available under 
the International Offering
87,102,000
Final no. of Offer Shares under the 
International Offering
87,102,000
% of Offer Shares under the International 
Offering to the Global Offering
90.00%
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a 
waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit the Company to allocate certain Offer Shares in the International Offering 
to certain Existing Minority Shareholders and/or their close associates, and (b) a consent under 
paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company 
to, among other things, allocate further H Shares in the International Offering to certain existing 
Shareholders and/or their close associates and Cornerstone Investors, (i) none of the Offer Shares 
subscribed by the placees and the public have been financed directly or indirectly by the Company, 
any of the Directors, chief executive of the Company, Controlling Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates; and (ii) none of the placees and the public who have purchased the Offer Shares 
are accustomed to taking instructions from the Company, any of its Directors, chief executive, 
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company or any 
of its subsidiaries or their respective close associates in relation to the acquisition, disposal, voting 
or other disposition of H Shares registered in his/her/its name or otherwise held by him/her/it.
The placees in the International Offering include the following:

<<<PAGE 6>>>
6
Cornerstone Investors
Cornerstone Investors
No. of Offer 
Shares allocated(1)
Approximate % of 
total issued 
H Shares after the 
Global Offering(2)(3)
Approximate 
% of total issued 
share capital 
after the Global 
Offering(3)
Existing
shareholders 
or their close 
associates
Harvest International 
Premium Value (Secondary 
Market) Fund SPC acting 
on behalf of and for the 
account of Harvest Oriental 
SP (“Harvest Oriental”)
10,177,200
10.52%
1.05%
No
Hengtong Optic-electric 
International Co., Limited 
(“Hengtong Optic-electric 
International”)
7,633,000
7.89%
0.79%
No
Dream’ee (Hong Kong) 
Open-ended Fund Company 
(“Dream’ee HK Fund”)
5,208,200
5.38%
0.54%
No
Deep Source Holdings 
Limited  
(“Deep Source”)
5,088,600
5.26%
0.53%
No
Haitian Huayuan 
(Singapore) Pte. Ltd. 
(“Haitian Huayuan”)
2,481,400
2.56%
0.26%
No
New Fortune Holdings 
Group Limited (“New 
Fortune”)
1,933,600
2.00%
0.20%
No
Qianhai Hezhong 
Investment Holding 
Limited (“Qianhai 
Hezhong Investment”)
1,526,600
1.58%
0.16%
No
Total
34,048,600
35.18%
3.52%
Notes:
(1) 
The number of Offer Shares allocated to such investors only represents the number of Offer Shares allocated 
to the investors as cornerstone investors in the International Offering. For allocations of Offer Shares to 
the relevant investors as placees (if any), please refer to the section headed “Allotment Results Details – 
International Offering – Allottees with waiver/consents obtained” in this announcement.
(2) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
(3) 
Assuming the Over-allotment Option is not exercised.
(4) 
In addition to the Offer Shares subscribed for as Cornerstone Investors, Dream’ee HK Fund, Qianhai Hezhong 
Investment, a close associate of New Fortune, and a close associate of Harvest Oriental were allocated further 
Offer Shares as placees in the International Offering. Please refer to the section headed “Allotment Results 
Details — International Offering — Allottees with Waivers/Consents Obtained” in this announcement for 
details. Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-up as indicated 
below. For details, please refer to the section headed “Lock-up Undertakings — Cornerstone Investors” in 
this announcement.

<<<PAGE 7>>>
7
Allottees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares allocated
Approximate 
% of total issued 
H Shares after the 
Global Offering(1)(2)
Approximate % of 
total issued 
share capital 
after the Global 
Offering(2)
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the 
Placing Guidelines in relation to subscription for H Shares by Existing Minority Shareholders holding more than 1% of the issued 
share capital of the Company immediately prior to the completion of the Global Offering and/or their close associates(3)
Nil
Nil
Nil
Nil
Nil
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of 
further H Shares to Cornerstone Investors(4)
Dream’ee HK Fund
3,515,600
3.63%
0.36%
Same entity as the 
Cornerstone Investor
Qianhai Hezhong Investment
1,025,800
1.06%
0.11%
Same entity as the
Cornerstone Investor
Mr. Sang Kangqiao
1,442,800
1.49%
0.15%
A close associate 
of New Fortune, a 
Cornerstone Investor
Harvest Global Capital 
Investment Limited
10,684,600
11.04%
1.10%
A close associate of 
Harvest Oriental, a 
Cornerstone Investor
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants 
in relation to allocations to connected clients(5)

<<<PAGE 8>>>
8
Investor
No. of Offer 
Shares allocated
Approximate 
% of total issued 
H Shares after the 
Global Offering(1)(2)
Approximate % of 
total issued 
share capital 
after the Global 
Offering(2)
Relationship
GF Global Capital Limited 
(“GFGC”)
1,780,000
1.84%
0.18%
Connected client  
as a placee
CITIC Securities 
International Capital 
Management Limited (“CSI”)
1,272,000
1.31%
0.13%
Connected client  
as a placee
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the Global Offering.
(2) 
Assuming the Over-allotment Option is not exercised.
(3) 
The Stock Exchange has granted a waiver from strict compliance with the requirements under Rule 10.04 of the Listing Rules and consent under Paragraph 
1C(2) of the Placing Guidelines to permit H Shares in the International Offering to be placed to such Existing Minority Shareholders. Please refer to 
the section headed “Waivers from Strict Compliance With the Listing Rules and Exemption From Compliance with the Companies (Winding Up and 
Miscellaneous Provisions) Ordinance — Allocation of H Shares to Existing Minority Shareholders and Their Close Associates” of the Prospectus for details.
The Stock Exchange has granted the waiver on the condition that, among others, details of the allocation to the Existing Minority Shareholders holding 
more than 1% of the issued share capital of the Company (including the treasury Shares) immediately prior to the completion of the Global Offering will be 
disclosed in the Prospectus and/or allotment results announcement.
(4) 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the number of Offer Shares allocated to the investors 
as placees in the International Offering. For allocations of Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed 
“Allotment Results Details — International Offering — Cornerstone Investors” in this announcement. For details of the consent under paragraph 18 of Chapter 
4.15 of the Guide for New Listing Applicants in relation to allocations of further H Shares to the Cornerstone Investors, please refer to the section headed 
“Others/Additional Information — Allocations of Offer Shares to certain Cornerstone Investors and/or their close associates with a consent under paragraph 
18 of Chapter 4.15 of the Guide for New Listing Applicants” in this announcement.
(5) 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations 
to connected clients, please refer to the sections headed “Others/Additional Information — Placing to connected clients with a prior consent under paragraph 
1C(1) of the Placing Guidelines” in this announcement.

<<<PAGE 9>>>
9
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of Shares 
held in the Company 
subject to lock-up 
undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings 
upon Listing(1)(2)
% of shareholding 
in Company 
subject to lock-up 
undertakings 
upon Listing(2)
Last day subject 
to the lock-up 
undertakings(3)
Mr. Wu Bo
110,996,700
–
11.47%
September 8, 2026 
(First Six-Month 
Period)(4)
March 8, 2027 
(Second Six-Month 
Period)(5)
Mr. Wu Kan
1,263,033
–
0.13%
September 8, 2026 
(First Six-Month 
Period)(4)
March 8, 2027 
(Second Six-Month 
Period)(5)
Nanjing Primest Technology 
Co., Ltd. (南京派雷斯特科
技有限公司)
254,894,742
–
26.34%
September 8, 2026 
(First Six-Month 
Period)(4)
March 8, 2027 
(Second Six-Month 
Period)(5)
Sub-total
367,154,475
–
37.94%
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the Global Offering.
(2) 
Assuming the Over-allotment Option is not exercised.
(3) 
In accordance with the applicable Listing Rules, the required lock-up for the first six month period will end on September 8, 2026 and for the second 
six-month period will end on March 8, 2027.
(4) 
Each member of the Controlling Shareholders may dispose of or transfer Shares after the indicated date subject to that the any member of Controlling 
Shareholders will not cease to be a controlling shareholder (as defined in the Listing Rules).
(5) 
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after the indicated date.

<<<PAGE 10>>>
10
Cornerstone Investors
Name
Number of Shares 
held in the Company 
subject to lock-up 
undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings 
upon Listing(1)(2)
% of shareholding 
in Company 
subject to lock-up 
undertakings 
upon Listing(2)
Last day subject 
to the lock-up 
undertakings(3)
Harvest Oriental
10,177,200
10.52%
1.05%
September 8, 2026
Hengtong Optic-electric 
International
7,633,000
7.89%
0.79%
September 8, 2026
Dream’ee HK Fund
5,208,200
5.38%
0.54%
September 8, 2026
Deep Source
5,088,600
5.26%
0.53%
September 8, 2026
Haitian Huayuan
2,481,400
2.56%
0.26%
September 8, 2026
New Fortune
1,933,600
2.00%
0.20%
September 8, 2026
Qianhai Hezhong 
Investment
1,526,600
1.58%
0.16%
September 8, 2026
Sub-total
34,048,600
35.18%
3.52%
Notes:
(6) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the Global Offering.
(7) 
Assuming the Over-allotment Option is not exercised.
(8) 
In accordance with the respective cornerstone investment agreements, the required lock-up periods will end on September 8, 2026. The Cornerstone 
Investors will cease to be prohibited from disposing of or transferring the Shares subscribed for pursuant to their respective cornerstone investment 
agreements after the indicated date.

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
(assuming 
no exercise 
of the 
Over-
allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option is 
exercised 
and new 
H Shares 
are issued)
Allotment 
as % of 
total Offer 
Shares 
(assuming 
no exercise
 of the 
Over-
allotment 
Option
Allotment 
as % of 
total Offer 
Shares 
(assuming 
the Over-
allotment 
Option is 
exercised 
and new 
H Shares 
are issued)
Number of 
H Shares 
held upon 
Listing
% of total 
issued share 
capital upon 
Listing 
(assuming 
no exercise 
of the 
Over-
allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is 
exercised 
and new 
H Shares 
are issued)
Top 1
20,861,800
24.0%
20.5%
21.6%
18.7%
20,861,800
2.2%
2.1%
Top 5
46,877,200
53.8%
46.1%
48.4%
42.1%
46,877,200
4.8%
4.8%
Top 10
61,518,000
70.6%
60.5%
63.6%
55.3%
61,518,000
6.4%
6.3%
Top 25
82,324,600
94.5%
81.0%
85.1%
74.0%
82,324,600
8.5%
8.4%
Notes
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDER CONCENTRATION ANALYSIS
H 
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
of the
Over-
allotment
Option)
Allotment
as % of
International
Offering
(assuming 
the Over-
allotment
Option is
exercised
and new
H Shares
are issued)
Allotment
as % of
total Offer
Shares
(assuming
no exercise
of the
Over-
allotment
Option)
Allotment
as % of
total Offer
Shares
(assuming 
the Over-
allotment
Option is
exercised
and new
H Shares
are issued)
Number of 
H Shares 
held upon 
Listing
% of
total issued
H Shares
capital 
upon
Listing
(assuming
no exercise
of the
Over-
allotment
Option)
% of
total issued
H Shares
capital upon
Listing
(assuming 
the Over-
allotment
Option is
exercised
and new
H Shares
are issued)
Number of
Shares
held upon
Listing
Top 1
20,861,800
24.0%
20.5%
21.6%
18.7%
20,861,800
21.6%
18.7%
20,861,800
Top 5
46,877,200
53.8%
46.1%
48.4%
42.1%
46,877,200
48.4%
42.1%
46,877,200
Top 10
61,518,000
70.6%
60.5%
63.6%
55.3%
61,518,000
63.6%
55.3%
61,518,000
Top 25
82,324,600
94.5%
81.0%
85.1%
74.0%
82,324,600
85.1%
74.0%
82,324,600
Notes
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 12>>>
12
SHAREHOLDER CONCENTRATION ANALYSIS
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
of the
Over-
allotment
Option)
Allotment
as % of
International
Offering
(assuming
 the Over-
allotment
Option is
exercised
and new
H Shares
are issued)
Allotment
as % of
total Offer
Shares
(assuming
no exercise
of the
Over-
allotment
Option)
Allotment
as % of
total Offer
Shares
(assuming 
the Over-
allotment
Option is
exercised
and new
H Shares
are issued)
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
(assuming
no exercise
of the
Over-
allotment
Option)
% of
total issued
share capital
upon Listing
(assuming 
the Over-
allotment
Option is
exercised
and new
H Shares
are issued)
Top 1
0
0.0%
0.0%
0.0%
0.0%
0
367,154,475
37.9%
37.4%
Top 5
20,861,800
24.0%
20.5%
21.6%
18.7%
20,861,800
449,583,689
46.5%
45.8%
Top 10
42,307,200
48.6%
41.6%
43.7%
38.0%
42,307,200
483,809,363
50.0%
49.3%
Top 25
67,186,200
77.1%
66.1%
69.4%
60.4%
67,186,200
525,761,148
54.3%
53.5%
Notes
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 13>>>
13
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
NO. OF SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT
APPROXIMATE
PERCENTAGE 
ALLOTTED
OF THE TOTAL 
NO. OF
SHARES 
APPLIED FOR
POOL A
200
12,869
642 out of 12,869 to receive 200 
Shares
4.99%
400
4,206
420 out of 4,206 to receive 200 Shares
4.99%
600
1,471
220 out of 1,471 to receive 200 Shares
4.99%
800
593
118 out of 593 to receive 200 Shares
4.97%
1,000
1,093
271 out of 1,093 to receive 200 Shares
4.96%
1,200
384
114 out of 384 to receive 200 Shares
4.95%
1,400
200
69 out of 200 to receive 200 Shares
4.93%
1,600
197
77 out of 197 to receive 200 Shares
4.89%
1,800
207
90 out of 207 to receive 200 Shares
4.83%
2,000
1,966
943 out of 1,966 to receive 200 Shares
4.80%
3,000
553
398 out of 553 to receive 200 Shares
4.80%
4,000
348
334 out of 348 to receive 200 Shares
4.80%
5,000
375
200 Shares plus 74 out of  375 to 
receive additional 200 Shares
4.79%
6,000
359
200 Shares plus 157 out of  359 to 
receive additional 200 Shares
4.79%
7,000
122
200 Shares plus 82 out of  122 to 
receive additional 200 Shares
4.78%
8,000
115
200 Shares plus 105 out of  115 to 
receive additional 200 Shares
4.78%
9,000
89
400 Shares plus 13 out of  89 to 
receive additional 200 Shares
4.77%
10,000
639
400 Shares plus 245 out of  639 to 
receive additional 200 Shares
4.77%
20,000
380
800 Shares plus 293 out of  380 to 
receive additional 200 Shares
4.77%
30,000
213
1,400 Shares plus 34 out of  213 to 
receive additional 200 Shares
4.77%

<<<PAGE 14>>>
14
NO. OF SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT
APPROXIMATE
PERCENTAGE 
ALLOTTED
OF THE TOTAL 
NO. OF
SHARES 
APPLIED FOR
40,000
132
1,800 Shares plus 72 out of  132 to 
receive additional 200 Shares
4.77%
50,000
80
2,200 Shares plus 74 out of  80 to 
receive additional 200 Shares
4.77%
60,000
94
2,800 Shares plus 30 out of  94 to 
receive additional 200 Shares
4.77%
70,000
21
3,200 Shares plus 14 out of  21 to 
receive additional 200 Shares
4.76%
80,000
48
3,800 Shares plus 2 out of  48 to 
receive additional 200 Shares
4.76%
90,000
24
4,200 Shares plus 10 out of  24 to 
receive additional 200 Shares
4.76%
100,000
181
4,600 Shares plus 137 out of  181 to 
receive additional 200 Shares
4.75%
200,000
93
9,400 Shares plus 49 out of  93 to 
receive additional 200 Shares
4.75%
Total
27,052
Total number of Pool A successful 
applicants: 6,661
POOL B
300,000
71
16,200 Shares plus 28 out of  71 to 
receive additional 200 Shares
5.43%
400,000
16
21,600 Shares plus 8 out of  16 to 
receive additional 200 Shares
5.43%
500,000
7
27,000 Shares plus 5 out of  7 to 
receive additional 200 Shares
5.43%
600,000
8
32,400 Shares plus 6 out of  8 to 
receive additional 200 Shares
5.43%
700,000
3
38,000 Shares
5.43%
800,000
4
43,400 Shares
5.43%

<<<PAGE 15>>>
15
NO. OF SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT
APPROXIMATE
PERCENTAGE 
ALLOTTED
OF THE TOTAL 
NO. OF
SHARES 
APPLIED FOR
900,000
3
48,800 Shares plus 1 out of  3 to 
receive additional 200 Shares
5.43%
1,000,000
11
54,200 Shares plus 3 out of  11 to 
receive additional 200 Shares
5.43%
1,500,000
5
81,400 Shares
5.43%
2,000,000
7
108,400 Shares plus 4 out of  7 to 
receive additional 200 Shares
5.43%
3,000,000
1
162,800 Shares
5.43%
4,839,000
2
262,600 Shares
5.43%
Total
138
Total number of Pool B successful 
applicants: 138
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or 
indirectly, provided by the Company, its Controlling Shareholders, Directors or syndicate members 
to any placees or the public (as the case may be) and the consideration paid by the placees or the 
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased 
by them was the same as the final Offer Price in addition to any brokerage, AFRC transaction levy, 
SFC transaction levy and Stock Exchange trading fee payable.

<<<PAGE 16>>>
16
OTHERS/ADDITIONAL INFORMATION
Allocation of H Shares to existing minority shareholders and their close associates with a 
waiver from the strict compliance with Rule 10.04 of the Listing Rules and a prior consent 
under paragraph 1C(2) of the Placing Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted to the 
Company, a waiver from strict compliance with the requirements under Rule 10.04 and consent 
under Paragraph 1C(2) of Appendix F1 to the Listing Rules to permit H Shares in the International 
Offering to be placed to certain existing minority Shareholders and/or their close associates who 
will participate only as either cornerstone investors or placees (but not both) in the International 
Offering (together, the “Existing Minority Shareholders”) on the conditions that:
(i) 
each Existing Minority Shareholder to whom our Company may allocate the H Shares in the 
International Offering holds less than 5% of the total number of A Shares in issue of our 
Company before Listing;
(ii) each Existing Minority Shareholder is not, and will not be, a core connected person of our 
Company or any close associate of any such core connected person immediately prior to or 
following the Global Offering;
(iii) none of the Existing Minority Shareholders have the right to appoint a Director and/or have 
any other special rights;
(iv) allocation to the Existing Minority Shareholders or their close associates will not affect our 
ability to satisfy the public float requirement as prescribed by the Stock Exchange under Rule 
8.08 (as amended and replaced by Rule 19A.13A(2) when applied to PRC issuers with other 
listed shares) of the Listing Rules;
(v) 
the Sole Sponsor will confirm to the Stock Exchange in writing that based on (i) its 
discussions with our Company and the Sponsor-Overall Coordinator; and (ii) the 
confirmations provided to the Stock Exchange by our Company and the Sponsor-Overall 
Coordinator (confirmations (vi) and (vii) mentioned below), and to the best of its knowledge 
and belief, it has no reason to believe that any of the Existing Minority Shareholders or their 
close associates received any preferential treatment, or is in a position to exert influence 
on the Company to obtain actual or perceived preferential treatment in the allocation either 
as a cornerstone investor or as a placee by virtue of their relationship with our Company 
other than the preferential treatment of assured entitlement under a cornerstone investment 
following the principles set out in Chapter 4.15 of the Guide for New Listing Applicants, 
and details of the allocation to the Existing Minority Shareholders holding more than 1% of 
the issued share capital of the Company immediately prior to the completion of the Global 
Offering will be disclosed in this announcement;

<<<PAGE 17>>>
17
(vi) our Company will confirm to the Stock Exchange in writing that:
(a). in the case of participation as cornerstone investors, no preferential treatment has been, 
nor will be, given to the Existing Minority Shareholders or their close associates by 
virtue of their relationship with our Company, other than the preferential treatment of 
assured entitlement under a cornerstone investment following the principles set out in 
Chapter 4.15 of the Guide for New Listing Applicants, nor is the Existing Minority 
Shareholder in a position to exert influence on the Company to obtain actual or 
perceived preferential treatment, and the Existing Minority Shareholders or their close 
associates’ cornerstone investment agreements do not contain any material terms which 
are more favorable to the Existing Minority Shareholders or their close associates than 
those in other cornerstone investment agreements; or
(b). in the case of participation as placees, no preferential treatment has been, no will be, 
given to the Existing Minority Shareholders or their close associates, nor is the Existing 
Minority Shareholder in a position to exert influence on the Company to obtain actual 
or perceived preferential treatment, by virtue of their relationship with our Company in 
any allocation in the placing tranche;
(vii) in the case of participation as placees, the Sponsor-Overall Coordinator will confirm to the 
Stock Exchange that, to the best of its knowledge and belief, no preferential treatment has 
been, nor will be, given to the Existing Minority Shareholders or their close associates by 
virtue of their relationship with our Company in any allocation in the placing tranche.
Please refer to the section headed “Waivers from Strict Compliance with Listing Rules and 
Exemption from Compliance with the Companies (Winding Up and Miscellaneous Provisions) 
Ordinance – Allocation of H Shares to Existing Minority Shareholders and Their Close Associates” 
in the Prospectus for further details of the waiver and consent. The allocation of Offer Shares to 
such Existing Minority Shareholders is in compliance with all the conditions under the waiver/
consent granted by the Stock Exchange.
Allocations of Offer Shares to certain Cornerstone Investors and/or their close associates with 
a consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph 
18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to allocate 
further Offer Shares in the International Offering to certain Cornerstone Investors and/or their 
close associates as placees, subject to the following conditions (the “Allocation to Size-based 
Exemption Participants”):
(a) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;

<<<PAGE 18>>>
18
(b) 
the Allocation to Size-based Exemption Participants will not affect the Company’s ability 
to satisfy its public float requirement as prescribed by the Stock Exchange under the waiver 
from strict compliance with the requirement of Rule 19A.13A(2) of the Listing Rules;
(c) 
Each of the Directors, chief executives and Controlling Shareholders of the Company has 
confirmed that no Offer Shares will be allocated to any of them or their respective close 
associates under this exemption;
(d) 
the details of allocation to the Cornerstone Investors under the size-based exemption will be 
disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to Cornerstone Investors, please refer to the section 
headed “Allotment Results Details – International Offering – Allottees with Waivers/Consents 
Obtained” in this announcement.
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines as placees. Please refer to the section 
headed “Allotment Results Details — International Offering — Allottees with Waivers/Consents 
Obtained” in this announcement for details.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such 
Offer Shares in the International Offering to the connected clients as placees. The allocation of 
Offer Shares to such connected clients is in compliance with all the conditions under the consent 
granted by the Stock Exchange. Details of the placement to connected clients as placees are set out 
below:

<<<PAGE 19>>>
19
No.
Connected
Distributor
Connected
Client(3)
Relationship 
between the 
Connected 
Client and 
the Connected 
Distributor(s)
Whether the 
Connected 
Client will 
hold the 
beneficial 
interests of 
the Offer 
Shares 
on a 
nondiscretionary 
basis or 
discretionary 
basis for 
independent 
third parties
Number of 
H Shares 
to be
allocated
Approximate
% of the total
Offer Shares
in the Global
Offering
(assuming the 
Over-allotment 
Option is not 
exercised)
Approximate
% of the total
Offer Shares
in the Global
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised)
Approximate
%
of the total
issued share
capital
immediately
following
completion
of the Global
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Approximate
%
of the total
issued share
capital
immediately
following
completion
of the Global
Offering 
(assuming the 
Over-
allotment 
Option is fully 
exercised)
1.
GF Securities 
(Hong Kong) 
Brokerage 
Limited
GFGC(1)
GF Securities 
(Hong Kong) 
Brokerage 
Limited and 
GFGC are 
member of the 
same group of 
companies
Non-discretionary 
basis
1,780,000
1.84%
1.60%
0.18%
0.18%
2.
CITIC Securities 
Brokerage (HK) 
Limited (“CITIC 
Brokerage”)
CSI(2)
CITIC 
Brokerage 
and CSI are 
members of the 
same group of
companies.
Non-discretionary 
basis
1,272,000
1.31%
1.14%
0.13%
0.13%

<<<PAGE 20>>>
20
Notes:
(1). 
GFGC is to invest on non-discretionary basis. GFGC and GF Securities Co., Ltd. will enter into a series of cross 
border delta one OTC swap transactions (the “OTC Swaps”) with each other and the ultimate client (the “GFGC 
Ultimate Client”), pursuant to which GFGC will hold the Offer Shares on a non-discretionary basis to hedge 
the OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed to the GFGC 
Ultimate Client, subject to customary fees and commissions. The OTC swaps will be fully funded by the GFGC 
Ultimate Client. During the terms of the OTC Swaps, all economic returns of the Offer Shares subscribed by 
GFGC will be passed to the GFGC Ultimate Client and all economic loss shall be borne by the GFGC Ultimate 
Client through the OTC Swaps, and GFGC will not take part in any economic return or bear any economic loss 
in relation to the Offer Shares. The OTC Swaps are linked to the Offer Shares and the GFGC Ultimate Client 
may request GFGC to redeem it at their own discretions, upon which GFGC shall dispose of the Offer Shares 
and settle OTC Swaps in cash in accordance with the terms and conditions of the OTC Swap. Despite that 
GFGC will hold the legal title of the Offer Shares by itself, it will not exercise the voting rights attaching to the 
relevant Offer Shares during the terms of the OTC Swaps according to its internal policy.
GFGC will hold the Offer Shares for and on behalf of one ultimate client on non-discretionary basis, namely 
Jifu Venture Capital Co., Ltd. (吉富創業投資股份有限公司), where except for Dong Zhengqing, no ultimate 
beneficial owners hold 30% or more interest.
To the best of GFGC’s knowledge, the GFGC Ultimate Client is an Independent Third Party of GFGC, GF 
Securities (Hong Kong) Brokerage Limited and the companies which are members of the same group of GFGC 
and GF Securities (Hong Kong) Brokerage.
(2). 
CSI and CITIC Securities Company Limited will enter into a series of cross border OTC swap transactions 
(“OTC Swaps”) with the investment manager for and on behalf of its ultimate client (the “CSI Ultimate 
Client”). CSI will hold the Offer Shares to be subscribed for and on behalf of the CSI Ultimate Client to hedge 
the OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed to the CSI 
Ultimate Client, subject to customary fees and commissions. CSI will enter into the OTC Swaps on behalf of 
the CSI Ultimate Client on a non-discretionary basis. CSI will not take part in any economic returns or bear 
any economic losses in relation to the Offer Shares. The OTC Swaps will be fully funded by the CSI Ultimate 
Client.
CSI will hold the Offer Shares for and on behalf of one ultimate client on non-discretionary basis, namely HY 
Capital Company Limited, where except for Xia Hui and Lu Ang, no ultimate beneficial owners hold 30% or 
more interest.
CSI has confirmed that, to the best of their knowledge, each of the CSI Ultimate Client and its ultimate 
beneficial owners are independent third parties of CSI, CITIC Connected Distributors and the companies which 
are members of the same group of companies as CITIC Brokerage.
(3). 
Each of the Connected Client is not a collective investment scheme which is not authorized by the SFC, nor is it 
holding the Offer Shares on behalf of such schemes.

<<<PAGE 21>>>
21
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or 
any part of the contents of this announcement.
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
investors should read the Prospectus dated February 27, 2026 issued by ESTUN AUTOMATION 
CO., LTD for detailed information about the Global Offering described below before deciding 
whether or not to invest in the H Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Sole Sponsor and the Sponsor-
Overall Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate its obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing 
Date (which is currently expected to be on Monday, March 9, 2026).

<<<PAGE 22>>>
22
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering, the number of the H Shares to be held by 
the public represents approximately 10.00% of the total issued share capital of our Company, the 
Company will therefore satisfy the public float requirement as required under Rule 19A.13A(2)(a) 
of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the H Shares of the Company at the time of Listing. Based on the 
final Offer Price of HK$15.36 per H Share, the Company satisfies the free float requirement under 
Rule 8.08A (as amended and replaced by Rule 19A.13C) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering (before any 
exercise of the Over-allotment Option): (i) the Shares will be held by at least 300 Shareholders 
at the time of Listing, in compliance with Rule 8.08(2) of the Listing Rules; (ii) the three largest 
public Shareholders will not hold more than 50% of the H Shares held in public hands at the 
time of Listing, in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; (iii) no placee 
will, individually, be placed more than 10% of the enlarged issued share capital of the Company 
immediately after the Global Offering; and (iv) there will not be any new substantial Shareholder 
(as defined in the Listing Rules) immediately after the Global Offering.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Monday, March 9, 
2026 (Hong Kong time), provided that the Global Offering has become unconditional and the right 
of termination described in the section headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has not been 
exercised. Investors who trade the H Shares on the basis of publicly available allocation details 
prior to the receipt of H Share certificates or prior to the H Share certificates becoming valid 
evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Monday, 
March 9, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Monday, March 9, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 200 H Shares each, and the stock code of the H Shares will 
be 2715.
By order of the Board
ESTUN AUTOMATION CO., LTD
Mr. WU Bo
Chairman of the Board and executive Director
Hong Kong, March 6, 2026
As of the date of this announcement, the Board comprises: (i) Mr. WU Bo, Mr. WU Kan, Mr. ZHU 
Chunhua, Mr. ZHOU Ailin and Mr. HE Lingjun as executive Directors; (ii) Ms. CHEN Yinlan as 
non-executive Director; and (iii) Dr. TANG Wencheng, Dr. HAN Xiaofang and Mr. LIN Jinjun as 
independent non-executive Directors.
