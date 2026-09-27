# 配发结果公告抽取任务：0501.HK OmniVision Integrated Circuits Group, Inc. - H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**09/01/2026 22:49**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0109/2026010901581.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"0501.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”, or the “Hong 
Kong Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the 
contents of this announcement, make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those defined 
in the prospectus dated December 31, 2025 (the “Prospectus”) of OmniVision Integrated Circuits Group, Inc. (豪威集成電
路(集團)股份有限公司) (the “Company”). This announcement is made by the order of the board (the “Board”) of directors 
(the “Directors”) of the Company. The Board collectively and individually accept responsibility for the accuracy of this 
announcement.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase or 
subscribe for any securities. This announcement is not a prospectus. Potential investors should read the Prospectus for 
detailed information about the Global Offering described below before deciding whether or not to invest in the Offer Shares. 
Any investment decision in relation to the Offer Shares should be taken solely in reliance on the information provided in the 
Prospectus.
This announcement is not for release, publication or distribution, directly or indirectly, in or into the United States (including 
its territories and possessions, any state of the United States and the District of Columbia or any other jurisdiction where such 
distribution is prohibited by laws). This announcement does not constitute or form a part of any offer or solicitation to purchase 
or subscribe for securities in the United States or in any other jurisdictions. The securities mentioned herein have not been, and 
will not be, registered under the United States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or 
securities law of any state or other jurisdiction of the United States. The securities may not be offered, sold, pledged or otherwise 
transferred within the United States except pursuant to an exemption from the registration requirements of the U.S. Securities Act 
and in compliance with any applicable state securities laws, or outside the United States unless in compliance with Regulation S 
under the U.S. Securities Act. There will be no public offer of securities in the United States.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited as stabilizing 
manager (the “Stabilizing Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, to the 
extent permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect 
transactions with a view to stabilizing or supporting the market price of the H Shares at such price, in such amounts and in 
such manners as the Stabilizing Manager, its affiliates or any person acting for it may determine and at a level higher than that 
which might otherwise prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing 
Manager (or its affiliates or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) 
will be conducted at the absolute discretion of the Stabilizing Manager (or its affiliates or any person acting for it) and in what 
the Stabilizing Manager reasonably regards as the best interest of the Company, (b) may be discontinued at any time and (c) is 
required to be brought to an end within 30 days of the last day for lodging applications under the Hong Kong Public Offering 
(which is Friday, February 6, 2026). Such Stabilizing action, if taken, may be effected in all jurisdictions where it is permissible 
to do so, in each case in compliance with all applicable laws, rules and regulatory requirements, including the Securities and 
Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures 
Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for longer than 
the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day after the last day for 
lodging applications under the Hong Kong Public Offering (which is Friday, February 6, 2026). After this date, when no further 
stabilizing action may be taken, demand for the H Shares, and therefore the price of the H Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to terms and conditions set out in the Prospectus. 
The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not resident in Hong Kong. 
Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators (for themselves and on 
behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting — Underwriting Arrangements and 
Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. on the 
Listing Date.

<<<PAGE 2>>>
2
OmniVision Integrated Circuits Group, Inc.
豪威集成電路（集團）股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
45,800,000 H Shares (subject to the Over-
allotment Option)
Number of Hong Kong Offer Shares
:
4,580,000 H Shares
Number of International Offer Shares
:
41,220,000 H Shares (subject to the Over-
allotment Option)
Final Offer Price
:
HK$104.80 per H Share, plus brokerage 
of 1%, SFC transaction levy of 0.0027%, 
Stock Exchange trading fee of 0.00565% 
and AFRC transaction levy of 0.00015% 
(payable in full on application in Hong Kong
dollars and subject to refund)
Nominal value
:
RMB1.0 per H Share
Stock code
:
0501
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers
UBS  CICC  PASCHK  GF Securities
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and 
Joint Lead Managers
Haitong International  CITIC Securities
Joint Lead Manager
TMS

<<<PAGE 3>>>
3
OmniVision Integrated Circuits Group, Inc.
豪威集成電路( 集團) 股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated December 31, 2025 (the “Prospectus”) issued 
by OmniVision Integrated Circuits Group, Inc. (豪威集成電路（集團）股份有限公司) (the 
“Company”).
Warning: In view of high concentration of shareholding in a small number of H 
Shareholders, H Shareholders and prospective investors should be aware that the price of 
the H Shares could move substantially even with a small number of H Shares traded and 
should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
0501
Stock short name
OMNIVISION
Dealings commencement date
January 12, 2026*
*  see note at the end of the announcement
Price Information
Final Offer Price
HK$104.8
Offer Shares and Share Capital
Number of Offer Shares
45,800,000
Number of Offer Shares in Hong Kong Public Offering
4,580,000
Number of Offer Shares in International Offering (before exercise 
of the Over-allotment Option)
41,220,000
Number of issued Shares upon Listing (before exercise of the 
Over-allotment Option)
(1)
1,255,474,412
Note:
(1)	 The number of issued Shares upon Listing includes 3,921,163 repurchased A Shares which 
are held by the Company as treasury Shares

<<<PAGE 4>>>
4
Over-allocation
Number of Offer Shares over-allocated
6,870,000
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds
HK$4,799.8 million
Less: Estimated listing expenses payable based on Final
Offer Price
HK$106.7 million
Net proceeds
HK$4,693.2 million
Note: (1) Gross proceeds refers to the amount which the Company is entitled to receive. For 
details of the use of proceeds, please refer to the section headed “Future Plans and Use of 
Proceeds” of the Prospectus. The Company will adjust the allocation of the net proceeds from the 
exercise of the Over-allotment Option (if any) for the purposes as set out in the section headed 
“Future Plans and Use of Proceeds” of the Prospectus on a pro rata basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
Number of valid applications
14,551
Number of successful applications
14,551
Subscription level
9.28 times
Claw-back triggered
N/A
Number of Offer Shares initially available under the Hong Kong 
Public Offering
4,580,000
Final number of Offer Shares under the Hong Kong Public 
Offering
4,580,000
% of final number of Offer Shares under the Hong Kong Public 
Offering to the Global Offering
10%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors 
can refer to https://www.hkeipo.hk/iporesult to perform a search by identification number or 
https://www.hkeipo.hk/iporesult for the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
Number of placees
127
Subscription level
9.73 times
Number of Offer Shares initially available under the
International Offering
41,220,000
Final number of Offer Shares under the International Offering
41,220,000
% of final number of Offer Shares under the International 
Offering to the Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a 
waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit the Company to allocate certain Offer Shares in the International Offering 
to certain Existing Minority Shareholders and/or their close associates, and (b) a consent under 
paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company 
to, among other things, allocate further H Shares in the International Offering to certain existing 
Shareholders and/or their close associates and Cornerstone Investors, (i) none of the Offer Shares 
subscribed by the placees and the public have been financed directly or indirectly by the Company, 
any of its Directors, chief executive, Controlling Shareholders, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates; and (ii) 
none of the placees and the public who have purchased the Offer Shares are accustomed to taking 
instructions from the Company, any of its Directors, chief executive, substantial Shareholders, 
Controlling Shareholders, existing Shareholders of the Company or any of its subsidiaries or their 
respective close associates in relation to the acquisition, disposal, voting or other disposition of H 
Shares registered in his/her/its name or otherwise held by him/her/it.

<<<PAGE 6>>>
6
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering 
(1) (2)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering 
(2) (3)
Existing 
Shareholders 
or their close 
associates
Wildlife Willow Limited 
(“Wildlife”)
(4)
5,196,600
11.35%
0.41%
No
UBS Asset Management 
(Singapore) Ltd. (“UBS AM 
Singapore”)
(4)
2,969,500
6.48%
0.24%
Yes
Formosa Opportunity Limited
(“FOL”)
(4)
2,500,000
5.46%
0.20%
Yes
Huaqin Telecom Hong Kong 
Limited
2,227,100
4.86%
0.18%
No
SKY ROYAL TRADING 
LIMITED (“Sky Royal”)
(4)
1,908,300
4.17%
0.15%
No
Pudong Science and Technology 
(Cayman) Co., Ltd. (“PST”)
(4)
1,855,900
4.05%
0.15%
No
JSC International Investment Fund 
SPC (acting for and on behalf of 
Yongxin I SP)
1,484,700
3.24%
0.12%
No
Ghisallo Fund Master Ltd
(“Ghisallo”)
(4)
1,113,500
2.43%
0.09%
No
Dajia Life Insurance Co., Ltd.
(“Dajia Life”)
(4)
742,300
1.62%
0.06%
Yes
PSBC Wealth Management Co., 
Ltd. (“PSBC Wealth”) (through 
GF Securities Asset Management 
(Guangdong) Co., Ltd (“GF 
Securities AM”) as the qualified 
domestic institutional investor)
(4)
742,300
1.62%
0.06%
No
Total
20,740,200
45.28%
1.65%

<<<PAGE 7>>>
7
Notes:
(1)	 The number of H Shares immediately after the Global Offering is the same as the number of 
Offer Shares to be issued under the Global Offering.
(2)	 Assuming the Over-allotment Option is not exercised.
(3)	 The total issued share capital after the Global Offering includes 3,921,163 A Shares being 
held as treasury Shares as of the date of this announcement.
(4)	 In addition to the Offer Shares subscribed for as Cornerstone Investors, Wildlife, UBS 
AM Singapore, FOL, Sky Royal, PST, Ghisallo, Dajia Life and PSBC Wealth (through 
GF Securities AM as the qualified domestic institutional investor), were allocated further 
Offer Shares as placees in the International Offering. Please refer to the section headed 
“Allotment Results Details — International Offering — Allottees with Waivers/Consents 
Obtained” in this announcement for details. Only the Offer Shares subscribed for as 
Cornerstone Investors are subject to lock-up as indicated below. For details, please refer to 
the section headed “Lock-up Undertakings — Cornerstone Investors” in this announcement.

<<<PAGE 8>>>
8
Allottees with waivers/consents obtained
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering 
(1) (2)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering 
(2) (3)
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by Existing Minority 
Shareholders holding more than 1% of the issued share capital of the Company immediately prior to the 
completion of the Global Offering and/or their close associates
(4)
Nil
Nil
Nil
Nil
Nil
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in 
relation to allocations of further H Shares to Cornerstone Investors
(5)
Wildlife
2,128,000
4.65%
0.17%
Same entity as the 
Cornerstone Investor
UBS AM Singapore
2,128,000
4.65%
0.17%
Same entity as the 
Cornerstone Investor and an 
existing Shareholder
PST
558,000
1.22%
0.04%
Same entity as the 
Cornerstone Investor
FOL
758,000
1.66%
0.06%
Same entity as the 
Cornerstone Investor and an
existing Shareholder
Sky Royal
1,880,000
4.10%
0.15%
Same entity as the 
Cornerstone Investor
Ghisallo
333,800
0.73%
0.03%
Same entity as the 
Cornerstone Investor
Dajia Life
222,800
0.49%
0.02%
Same entity as the 
Cornerstone Investor and an
existing Shareholder
PSBC Wealth (through 
GF Securities AM as 
the qualified domestic 
institutional investor)
222,800
0.49%
0.02%
Same entity as the 
Cornerstone Investor
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for 
New Listing Applicants in relation to allocations to connected clients
(6)

<<<PAGE 9>>>
9
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering 
(1) (2)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering 
(2) (3)
Relationship
UBS AM Singapore
2,128,000
4.65%
0.17%
Connected client as a placee
2,969,500
6.48%
0.24%
Connected client as a
Cornerstone Investor
Fullgoal Asset 
Management (HK) 
Limited
9,700
0.02%
0.00%
Connected client as a placee
PSBC Wealth (through 
GF Securities AM as 
the qualified domestic 
institutional investor)
222,800
0.49%
0.02%
Connected client as a placee
742,300
1.62%
0.06%
Connected client as a
Cornerstone Investor
CITIC Securities Asset 
Management (HK) 
Limited
74,400
0.16%
0.01%
Connected client as a placee
Guotai Junan 
Investments (Hong 
Kong) Limited 
556,700
1.22%
0.04%
Connected client as a placee
Notes:
(1)	 The number of H Shares immediately after the Global Offering is the same as the number of 
Offer Shares to be issued under the Global Offering.
(2)	 Assuming the Over-allotment Option is not exercised.
(3)	 The total issued share capital after the Global Offering includes 3,921,163 A Shares being 
held as treasury Shares as of the date of this announcement.

<<<PAGE 10>>>
10
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering 
(1) (2)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering 
(2) (3)
Relationship
(4)	 Among the Cornerstone Investors, UBS AM Singapore, Formosa Opportunity Limited and 
Dajia Life Insurance Co., Ltd. are Existing Minority Shareholders or their close associate, 
none of which holds more than 1% of the issued share capital of the Company (including 
the treasury Shares) immediately prior to the completion of the Global Offering. The Stock 
Exchange has granted a waiver from strict compliance with the requirements under Rule 
10.04 of the Listing Rules and consent under Paragraph 1C(2) of the Placing Guidelines 
to permit H Shares in the International Offering to be placed to such Existing Minority 
Shareholders. Please refer to the section headed “Waivers and Exemptions — Allocation 
of H Shares to Existing Minority Shareholders and/or Their Close Associates” of the 
Prospectus for details.
The Stock Exchange has granted the waiver on the condition that, among others, details of 
the allocation to the Existing Minority Shareholders holding more than 1% of the issued 
share capital of the Company (including the treasury Shares) immediately prior to the 
completion of the Global Offering will be disclosed in the Prospectus and/or allotment 
results announcement.
(5)	 The number of Offer Shares allocated to the relevant investors listed in this subsection 
only represents the number of Offer Shares allocated to the investors as placees in 
the International Offering. For allocations of Offer Shares to the relevant investors as 
Cornerstone Investors, please refer to the section headed “Allotment Results Details — 
International Offering — Cornerstone Investors” in this announcement. For details of the 
consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in 
relation to allocations of further H Shares to the Cornerstone Investors, please refer to 
the section headed “Others/Additional Information — Allocations of Offer Shares to the 
Cornerstone Investors with a consent under paragraph 18 of Chapter 4.15 of the Guide for 
New Listing Applicants” in this announcement.
(6)	 For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 
4.15 of the Guide for New Listing Applicants in relation to allocations to connected clients, 
please refer to the sections headed “Others/Additional Information — Placing to connected 
clients with a consent under paragraph 1C(1) of the Placing Guidelines” and “Others/
Additional Information — Allocations of Offer Shares to the Cornerstone Investors with a 
consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants” in 
this announcement.

<<<PAGE 11>>>
11
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
(6)
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
total issued 
H Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon 
Listing 
(1)(2)
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon 
Listing 
(2)
Last day subject 
to the lock-up 
undertakings 
(3)
Mr. YU Renrong
303,472,250
—
24.17%
July 11, 2026 
(First Six-Month 
Period)
(4)
January 11, 2027 
(Second Six-Month 
Period)
(5)
Shaoxing Weihao Equity 
Investment Funds Management 
Partnership (Limited Partnership)
74,132,662
—
5.90%
July 11, 2026 
(First Six-Month 
Period)
(4) 
January 11, 2027 
(Second Six-Month 
Period)
(5)
Mr. YU Xiaorong
972,000
—
0.08%
July 11, 2026 
(First Six-Month 
Period)
(4) 
January 11, 2027 
(Second Six-Month 
Period)
(5)

<<<PAGE 12>>>
12
Name
(6)
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
total issued 
H Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon 
Listing 
(1)(2)
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon 
Listing 
(2)
Last day subject 
to the lock-up 
undertakings 
(3)
Notes:
(1)	 The number of H Shares immediately after the Global Offering is the same as the number of 
Offer Shares to be issued under the Global Offering.
(2)	 Assuming the Over-allotment Option is not exercised.
(3)	 In accordance with the applicable Listing Rules, the required lock-up for the first six month 
period will end on July 11, 2026 and for the second six-month period will end on January 
11, 2027.
(4)	 Each member of the Controlling Shareholders may dispose of or transfer Shares (which 
includes the Convertible Bonds held by Shaoxing Weihao Management and the underlying 
Shares that may be converted from such Convertible Bonds in the event of the exercise of its 
conversion rights, as applicable) after the indicated date subject to that the any member of 
Controlling Shareholders will not cease to be a controlling shareholder (as defined in the 
Listing Rules).
(5)	 The Controlling Shareholders will cease to be prohibited from disposing of or transferring 
Shares after the indicated date.
(6)	 For illustrative purposes only, this subsection lists only those members of the Controlling 
Shareholders who hold Shares directly in the Company. Pursuant to Rule 10.07 of the 
Listing Rules, each of the Controlling Shareholders (namely, Mr. Yu Renrong, Shaoxing 
Weihao Management, Shanghai Qingen, Qingdao Qingen and Mr. Yu Xiaorong) has 
undertaken to the Company and the Stock Exchange that, except in connection with the 
Global Offering (including the Over-allotment Option), he or it shall, and shall procure 
that the relevant registered holders of the Shares in which he or it is beneficially interested 
shall, comply with the applicable lock-up requirements. For further details, please refer 
to the section headed “Underwriting —  Underwriting Arrangements and Expenses — 
Undertakings to the Stock Exchange pursuant to the Listing Rules” in the Prospectus.

<<<PAGE 13>>>
13
Cornerstone Investors
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
total issued 
H Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon 
Listing 
(1)(2)
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon 
Listing 
(2) 
Last day subject 
to the lock-up 
undertakings 
(3)
Wildlife
5,196,600
11.35%
0.41%
July 11, 2026
UBS AM Singapore
2,969,500
6.48%
0.24%
July 11, 2026
Formosa Opportunity Limited
2,500,000
5.46%
0.20%
July 11, 2026
Huaqin Telecom 
  Hong Kong Limited
2,227,100
4.86%
0.18%
July 11, 2026
SKY ROYAL TRADING 
  LIMITED
1,908,300
4.17%
0.15%
July 11, 2026
PST
1,855,900
4.05%
0.15%
July 11, 2026
JSC International Investment 
  Fund SPC (acting for and 
  on behalf of Yongxin I SP)
1,484,700
3.24%
0.12%
July 11, 2026
Ghisallo Fund Master Ltd
1,113,500
2.43%
0.09%
July 11, 2026
Dajia Life Insurance Co., Ltd. 
742,300
1.62%
0.06%
July 11, 2026
PSBC Wealth (through GF 
  Securities AM as the qualified 
  domestic institutional investor)
742,300
1.62%
0.06%
July 11, 2026

<<<PAGE 14>>>
14
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
total issued 
H Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon 
Listing 
(1)(2)
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon 
Listing 
(2) 
Last day subject 
to the lock-up 
undertakings 
(3)
Notes:
(1)	 The number of H Shares immediately after the Global Offering is the same as the number of 
Offer Shares to be issued under the Global Offering.
(2)	 Assuming the Over-allotment Option is not exercised.
(3)	 In accordance with the respective cornerstone investment agreements, the required lock-
up periods will end on July 11, 2026. The Cornerstone Investors will cease to be prohibited 
from disposing of or transferring the Shares subscribed for pursuant to their respective 
cornerstone investment agreements after the indicated date.

<<<PAGE 15>>>
15
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment 
as % of 
International
Offering 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued)
Allotment 
as % of 
total Offer 
Shares 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment 
as % of 
total Offer 
Shares 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued)
Number of 
H Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued)
Top 1
7,324,600
17.77%
15.23%
15.99%
13.91%
7,324,600
0.58%
0.58%
Top 5
21,882,300
53.09%
45.50%
47.78%
41.55%
21,882,300
1.74%
1.73%
Top 10
32,621,400
79.14%
67.83%
71.23%
61.94%
32,621,400
2.60%
2.58%
Top 25
45,185,000
109.62%
93.96%
98.66%
85.79%
45,185,000
3.60%
3.58%
Note
*	
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS
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
Over-allotment
Option)
Allotment
as % of
International
Offering
(assuming the
Over-allotment
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
Over-allotment
Option)
Allotment
as % of
total Offer
Shares
(assuming the
Over-allotment
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
capital upon
Listing
(assuming
no exercise
of the
Over-allotment
Option)
% of
total issued
H Shares
capital upon
Listing
(assuming the
Over-allotment
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
7,324,600
17.77%
15.23%
15.99%
13.91%
7,324,600
0.58%
0.58%
7,324,600
Top 5
21,882,300
53.09%
45.50%
47.78%
41.55%
21,882,300
1.74%
1.73%
21,882,300
Top 10
32,621,400
79.14%
67.83%
71.23%
61.94%
32,621,400
2.60%
2.58%
32,621,400
Top 25
45,185,000
109.62%
93.96%
98.66%
85.79%
45,185,000
3.60%
3.58%
45,185,000
Note
*	
Ranking of H Shareholders is based on the number of H Shares held by the Shareholder upon Listing.

<<<PAGE 16>>>
16
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
Over-allotment
Option)
Allotment
as % of
International
Offering
(assuming the
Over-allotment
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
Over-allotment
Option)
Allotment
as % of
total Offer
Shares
(assuming the
Over-allotment
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
Over-allotment
Option)
% of
total issued
share capital
upon Listing
(assuming the
Over-allotment
Option is
exercised
and new
H Shares
are issued)
Top 1
0
0.00%
0.00%
0.00%
0.00%
0
378,576,912
30.15%
29.99%
Top 5
0
0.00%
0.00%
0.00%
0.00%
0
615,684,344
49.04%
48.77%
Top 10
3,258,000
7.90%
6.77%
7.11%
6.19%
3,258,000
671,561,816
53.49%
53.20%
Top 25
19,468,400
47.23%
40.48%
42.51%
36.96%
19,468,400
754,076,473
60.06%
59.74%
Note
*	
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 17>>>
17
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, 14,551 valid applications 
made by the public will be conditionally allocated on the basis set out below:
NO. OF 
H SHARES 
APPLIED FOR
NO. OF 
VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED OF
THE TOTAL NO.
OF H SHARES
APPLIED FOR
POOL A
100
7,028
100 H Shares
100.00%
200
1,230
100 H Shares plus 246 out of 1,230 applicants to receive an additional 
100 H Shares
60.00%
300
728
100 H Shares plus 255 out of 728 applicants to receive an additional 
100 H Shares
45.01%
400
1,146
100 H Shares plus 659 out of 1,146 applicants to receive an additional 
100 H Shares
39.38%
500
561
100 H Shares plus 392 out of 561 applicants to receive an additional 
100 H Shares
33.98%
600
160
100 H Shares plus 129 out of 160 applicants to receive an additional 
100 H Shares
30.10%
700
83
100 H Shares plus 75 out of 83 applicants to receive an additional 100 
H Shares
27.19%
800
122
100 H Shares plus 120 out of 122 applicants to receive an additional 
100 H Shares
24.80%
900
367
200 H Shares
22.22%
1,000
1,120
200 H Shares plus 150 out of 1,120 applicants to receive an additional 
100 H Shares
21.34%
1,500
403
200 H Shares plus 177 out of 403 applicants to receive an additional 
100 H Shares
16.26%
2,000
288
200 H Shares plus 196 out of 288 applicants to receive an additional 
100 H Shares
13.40%
2,500
92
200 H Shares plus 82 out of 92 applicants to receive an additional 100 
H Shares
11.57%
3,000
144
300 H Shares
10.00%
3,500
54
300 H Shares plus 12 out of 54 applicants to receive an additional 100 
H Shares
9.21%

<<<PAGE 18>>>
18
NO. OF 
H SHARES 
APPLIED FOR
NO. OF 
VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED OF
THE TOTAL NO.
OF H SHARES
APPLIED FOR
4,000
68
300 H Shares plus 25 out of 68 applicants to receive an additional 100 
H Shares
8.42%
4,500
39
300 H Shares plus 20 out of 39 applicants to receive an additional 100 
H Shares
7.81%
5,000
176
300 H Shares plus 110 out of 176 applicants to receive an additional 
100 H Shares
7.25%
6,000
63
300 H Shares plus 54 out of 63 applicants to receive an additional 100 
H Shares
6.43%
7,000
38
400 H Shares
5.71%
8,000
32
400 H Shares plus 4 out of 32 applicants to receive an additional 100 
H Shares
5.16%
9,000
36
400 H Shares plus 9 out of 36 applicants to receive an additional 100 
H Shares
4.72%
10,000
261
400 H Shares plus 105 out of 261 applicants to receive an additional 
100 H Shares
4.40%
20,000
89
600 H Shares
3.00%
30,000
51
800 H Shares
2.67%
40,000
44
1,000 H Shares
2.50%
Total
14,423
Total number of Pool A successful applicants: 14,423

<<<PAGE 19>>>
19
NUMBER OF 
H SHARES 
APPLIED FOR
NUMBER OF 
VALID 
APPLICATIONS
BASIS OF ALLOCATION/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NUMBER 
OF H SHARES 
APPLIED FOR
POOL B
50,000
59
4,300 H Shares plus 48 out of 59 applicants to receive an additional 
100 H Shares
8.76%
60,000
10
5,200 H Shares plus 4 out of 10 applicants to receive an additional 100 
H Shares
8.73%
70,000
4
6,100 H Shares
8.71%
80,000
6
6,900 H Shares plus 3 out of 6 applicants to receive an additional 100 
H Shares
8.69%
90,000
3
7,800 H Shares
8.67%
100,000
20
8,600 H Shares plus 12 out of 20 applicants to receive an additional 
100 H Shares
8.66%
200,000
8
17,300 H Shares
8.65%
300,000
3
25,900 H Shares
8.63%
400,000
1
34,400 H Shares
8.60%
500,000
4
42,900 H Shares plus 2 out of 4 applicants to receive an additional 100 
H Shares
8.59%
600,000
1
51,500 H Shares
8.58%
700,000
2
60,000 H Shares
8.57%
1,000,000
1
85,600 H Shares
8.56%
1,500,000
2
128,100 H Shares
8.54%
2,290,000
4
195,200 H Shares
8.52%
Total
128
Total number of Pool B successful applicants: 128

<<<PAGE 20>>>
20
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Allocation of H Shares to Existing Minority Shareholders and/or Their Close Associates
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted to the 
Company, a waiver from strict compliance with the requirements under Rule 10.04 and consent 
under Paragraph 1C(2) of Appendix F1 to the Listing Rules to permit H Shares in the International 
Offering to be placed to certain existing minority Shareholders (including holders of our GDRs) 
and/or their close associates who will participate only as either cornerstone investors or placees (but 
not both) in the International Offering (together, the “Existing Minority Shareholders”) on the 
conditions that each of them:
(a)	 together with their close associates, holds less than 5% of the voting rights in our Company 
prior to the completion of the Global Offering;
(b)	 is not and will not become a core connected person of the Company or the close associate of 
any such core connected person upon the completion of the Global Offering;
(c)	 does not have the right to appoint a Director and/or has any other special rights;
(d)	 allocation to the Existing Minority Shareholders or their close associates will not affect the 
Company’s ability to satisfy the public float requirement as prescribed by the Stock Exchange 
under Rule 19A.13A(2) of the Listing Rules;
(e)	 that no preferential treatment is given to the Existing Minority Shareholders or their respective 
close associates (other than the assured entitlement for a cornerstone investor); and
(f)	
details of the allocation to the Existing Minority Shareholders and/or their respective close 
associates holding more than 1% of the issued share capital of the Company immediately prior 
to the completion of the Global Offering has been disclosed in this announcement.
Please refer to the section headed “Waivers and Exemptions — Allocation of H Shares to Existing 
Minority Shareholders and/or Their Close Associates” in the Prospectus for further details of the 
waiver and consent.

<<<PAGE 21>>>
21
Each of the Joint Sponsors and the Company has provided the required confirmations as elaborated 
in the Prospectus. In particular, as the Company’s A Shares are listed on the Shanghai Stock 
Exchange since 2017, the Company has a highly extensive base of existing Shareholders and 
disclosure of details of allocations to all Existing Minority Shareholders and/or their respective 
close associates will not be meaningful to investors, the proposed disclosure threshold, i.e. 
condition (f) of the waiver and consent which provides that details of the allocation to the Existing 
Minority Shareholders and/or their respective close associates holding more than 1% of the issued 
share capital of the Company immediately prior to the completion of the Global Offering will be 
disclosed in this announcement, is appropriate.
All allocations of Offer Shares to the Existing Minority Shareholders are in compliance with all the 
conditions under the waiver and consent granted by the Stock Exchange.
Allocations of Offer Shares to the Cornerstone Investors with a consent under paragraph 18 of 
Chapter 4.15 of the Guide for New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph 18 
of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to allocate further 
Offer Shares in the International Offering to certain Cornerstone Investors as placees, subject to the 
following conditions (“Allocation to Size-based Exemption Participants”):
(a)	 the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;
(b)	 the Offer Shares allocated to all existing Shareholders (whether as cornerstone investors and 
as placees) as permitted under this exemption do not exceed 30% of the total number of the H 
Shares offered under the Global Offering;
(c)	 the Allocation to Size-based Exemption Participants will not affect the Company’s ability to 
satisfy its public float requirement as prescribed by the Stock Exchange under the waiver from 
strict compliance with the requirements of Rule 19A.13A(2) of the Listing Rules;
(d)	 each of the Directors, chief executive of the Company and the Controlling Shareholders 
confirms that no securities have been allocated to them or their respective close associates 
under this exemption; and
(e)	 details of the allocation to Cornerstone Investors under this exemption has been disclosed in 
this announcement.

<<<PAGE 22>>>
22
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted 
by the Stock Exchange.
For details of further allocations of Offer Shares to Cornerstone Investors, please refer to the section 
headed “Allotment Results Details — International Offering — Allottees with Waivers/Consents 
Obtained” in this announcement.
Placing to connected clients with a consent under paragraph 1C(1) of the Placing Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, 
consent under paragraph 1C(1) of the Placing Guidelines to permit UBS AM Singapore and GF 
Securities AM (acting as a qualified domestic institutional investor for and on behalf of PSBC 
Wealth) to participate in the Global Offering as connected clients to participate in the Global 
Offering as Cornerstone Investors. For details of the consent granted, please refer to the section 
headed “Allotment Results Details — International Offering — Cornerstone Investors” in this 
announcement.
In addition, under the International Offering, certain Offer Shares were placed to connected clients 
of their connected distributors pursuant to the Placing Guidelines as placees. Please refer to the 
section headed “Allotment Results Details — International Offering — Allottees with Waivers/
Consents Obtained” in this announcement for details. The Company has applied to the Stock 
Exchange for, and the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing 
Guidelines to permit the Company to allocate such Offer Shares in the International Offering to 
the connected clients as placees. The allocation of Offer Shares to such connected clients is in 
compliance with all the conditions under the consent granted by the Stock Exchange. Details of the 
placement to connected clients as placees are set out below.

<<<PAGE 23>>>
23
No.
Connected Client
 (9)
Connected 
Distributor(s)
Relationship between 
the Connected Client 
and the Connected 
Distributor(s)
Discretionary 
or non-
discretionary
Investment 
amount (US$)
Number of H 
Shares to be 
allocated 
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering
(1) 
Approximate 
percentage 
of the total 
issued share 
capital 
immediately 
following 
completion 
of the Global 
Offering
(1) (2) 
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering
(3) 
Approximate 
percentage 
of the total 
issued share 
capital 
immediately 
following 
completion 
of the Global 
Offering
(2) (3)
1.
UBS Asset Management 
(Singapore) Ltd. (“UBS 
AM Singapore”)
(4)
UBS AG Hong 
Kong Branch 
(“UBS HK”),
UBS AG Singapore 
Branch Wealth
Management
(“UBS SG WM”) 
and UBS AG
Hong Kong 
Branch Wealth 
Management
(“UBS HK WM”)
UBS AM Singapore is a 
member of the same group 
of companies as UBS HK, 
UBS SG WM and UBS HK 
WM.
Discretionary
28,664,722
2,128,000
4.65%
0.17%
4.04%
0.17%
2.
Fullgoal Asset 
Management (HK) Limited 
(“Fullgoal HK”) 
(5)
Haitong 
International 
Securities Company 
Limited (“HTI”)
Fullgoal HK is a member 
of the same group of 
companies as HTI.
Discretionary
130,662
9,700
0.02%
0.00%
0.02%
0.00%

<<<PAGE 24>>>
24
No.
Connected Client
 (9)
Connected 
Distributor(s)
Relationship between 
the Connected Client 
and the Connected 
Distributor(s)
Discretionary 
or non-
discretionary
Investment 
amount (US$)
Number of H 
Shares to be 
allocated 
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering
(1) 
Approximate 
percentage 
of the total 
issued share 
capital 
immediately 
following 
completion 
of the Global 
Offering
(1) (2) 
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering
(3) 
Approximate 
percentage 
of the total 
issued share 
capital 
immediately 
following 
completion 
of the Global 
Offering
(2) (3)
3.
GF Securities 
Asset Management 
(Guangdong) Co., Ltd. 
(“GF Securities AM”, 
acting as a qualified 
domestic institutional 
investor for PSBC Wealth 
Management Co., Ltd. 
(“PSBC Wealth”))
(6)
GF Securities 
(Hong Kong) 
Brokerage Limited 
(“GF Securities 
(Hong Kong) 
Brokerage”)
GF Securities AM is 
a member of the same 
group of companies as GF 
Securities (Hong Kong) 
Brokerage.
Non-
discretionary
3,001,175
222,800
0.49%
0.02%
0.42%
0.02%
4.
CITIC Securities Asset 
Management (HK) Limited 
(“CITICS AM”) 
(7) 
CLSA Limited 
(“CLSA”) and 
CITIC Securities 
Brokerage (HK) 
Limited (“CSB”)
CITICS AM is a member 
of the same group of 
companies as CLSA and 
CSB.
Discretionary
1,002,188
74,400
0.16%
0.01%
0.14%
0.01%
5.
Guotai Junan Investments 
(Hong Kong) Limited 
(“GTJAI”) 
(8)
HTI
GTJAI is a member of the 
same group of companies 
as HTI.
Non-
discretionary
7,498,896
556,700
1.22%
0.04%
1.06%
0.04%

<<<PAGE 25>>>
25
Notes:
(1)	
Assuming the Over-allotment Option is not exercised.
(2)	
Including 3,921,163 A Shares held by the Company in treasury as of the Latest Practicable Date.
(3)	
Assuming the Over-allotment Option is fully exercised.
(4)	
UBS AM Singapore will hold the beneficial interests of the Offer Shares on a discretionary basis for and on behalf of the underlying clients, each of whom is an independent third party of the Company, its subsidiaries, its Controlling Shareholders, its substantial 
shareholders, UBS AM Singapore, UBS HK, UBS HK WM, UBS SG WM and the companies which are members of the same group of UBS HK, UBS HK WM and UBS SG WM.
In addition to the Offer Shares subscribed for as a placee, UBS AM Singapore was allocated 2,969,500 Offer Shares as a Cornerstone Investor in the International Offering. UBS HK is an Overall Coordinator. UBS AM Singapore and UBS HK are members of the 
same group of companies. Accordingly, UBS AM Singapore is a connected client. The Company has, therefore, applied for, and the Stock Exchange has granted, a consent under paragraph 1C(1) of Appendix F1 to the Listing Rules to permit UBS AM Singapore 
to participate in the Global Offering as a Cornerstone Investor. For details, please refer to the section headed “Waivers and Exemptions — Consent in Respect of the Proposed Subscription of H Shares by a Cornerstone Investor Who is a Connected Client” in the 
Prospectus. With the appointment of UBS SG WM and UBS HK WM as additional sub-distributors in the Global Offering, the relationship among UBS AM Singapore, UBS HK, UBS SG WM and UBS HK WM also falls within the scope of the aforementioned waiver.
(5)	
Fullgoal HK will hold the Offer Shares in its capacity as the discretionary fund manager on behalf of its investors, each of which is an independent third party of the Company, its subsidiaries, its Controlling Shareholders, its substantial shareholders, Fullgoal HK, 
HTI and the companies which are members of the same group of HTI.
(6)	
PSBC Wealth has engaged GF Securities AM, an asset manager that is a qualified domestic institutional investor as approved by the relevant PRC authority, to subscribe for and hold such Offer Shares on a non-discretionary basis on behalf of PSBC Wealth, in the 
name of: (i) ICBC (ASIA) LTD-PAB-GFAM ZHONGYOU NO. 1 ASSET MANAGEMENT ACCOUNT (QDII) (廣發資管中郵理財港股策略1號單一資產管理計劃(QDII)), (ii) ICBC (ASIA) LTD-PAB-GFAM ZHONGYOU NO. 2 ASSET MANAGEMENT ACCOUNT 
(QDII) (廣發資管中郵理財港股策略2號單一資產管理計劃(QDII)), (iii) GFAM ZHONGYOU NO. 3 ASSET MANAGEMENT ACCOUNT (QDII) (廣發資管中郵理財港股策略3號單一資產管理計劃), (iv) GFAM ZHONGYOU NO. 4 ASSET MANAGEMENT 
ACCOUNT (QDII) (廣發資管中郵理財港股策略4號單一資產管理計劃) and (v) GFAM ZHONGYOU NO. 5 ASSET MANAGEMENT ACCOUNT (QDII) (廣發資管中郵理財港股策略5號單一資產管理計劃). PSBC Wealth is wholly owned by Postal Savings Bank of 
China Co., Ltd. (SEHK: 1658) and is ultimately controlled by China Post Group Corporation Limited.
As confirmed by GF Securities AM, (i) the Offer Shares to be placed to GF Securities AM are to be held on a non-discretionary basis on behalf of independent third parties; and (ii) each of PSBC Wealth and its ultimate beneficial owner is an independent third party 
of the Company, its subsidiaries, its Controlling Shareholders, its substantial shareholders, GF Securities AM, GF Securities (Hong Kong) Brokerage and the companies which are members of the same group of companies as GF Securities (Hong Kong) Brokerage.
(7)	
CITICS AM will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their investors, each of which is an independent third party of the Company, its subsidiaries, its Controlling Shareholders, its substantial 
shareholders, CITICS AM, CLSA, CSB and the companies which are members of the same group of CLSA and CSB.

<<<PAGE 26>>>
26
(8)	
GTJAI will hold the Offer Shares for hedging purpose as the single underlying asset of a back-to-back total return swap transaction (the “GTHT Back-to-back TRS”) to be entered into between GTJAI and Guotai Haitong Securities Co., Ltd. (the “GTHT Onshore 
Parent”) in connection with a total return swap order (the “GTHT Client TRS”) to be entered into by GTHT Onshore Parent and its ultimate client (the “GTHT Onshore Ultimate Client”). Such GTHT Client TRS is to be fully funded by the GTHT Onshore Ultimate 
Client. GTJAI will hold the H Shares on a non-discretionary basis for the purpose of hedging the economic exposure under the GTHT Back-to-back TRS and GTHT Client TRS only, and the economic exposure of the underlying Offer Shares will be passed to the GTHT 
Onshore Ultimate Client, subject to the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS documents. During the tenor of the GTHT Client TRS, all economic returns of the Offer Shares will be passed to the GTHT Onshore Ultimate Client 
and all economic losses shall be borne by the GTHT Onshore Ultimate Client, in accordance with the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS documents, and GTJAI will not take part in any economic return or bear any economic 
loss in relation to the price of the Offer Shares. The GTHT Onshore Ultimate Client may request to redeem the H Shares at their own discretion, upon which GTJAI shall dispose of the H Shares and settle the GTHT Back-to-back TRS and GTHT Client TRS in cash in 
accordance with the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS documents. Due to its internal policy, GTJAI will not exercise the voting right attaching to the Offer Shares during the tenor of the GTHT Back-to-back TRS and GTHT 
Client TRS documents.
The GTHT Onshore Ultimate Client for purpose of this placing subscription is Ze Tian Ai Pu Xi Long Steady No. 1 Private Securities Investment Fund (澤添艾普西隆穩健壹號私募證券投資基金), which is managed by Ningbo Ze Tian Investment 
Management Partnership (Limited Partnership) (寧波澤添投資管理合夥企業 (有限合夥)), a partnership ultimately beneficially owned by Zheng Jiao and Zhang Tuguo. There is no limited partner or shareholder holding a 30% or more interest in the 
GTHT Onshore Ultimate Client.
To the best of knowledge of GTJAI and after making all reasonable enquiries, the GTHT Onshore Ultimate Client is an independent third party of the Company, its subsidiaries, its Controlling Shareholders, its substantial shareholders, GTJAI, and the companies which 
are members of the same group of GTJAI.
(9)	
Each of the Connected Client is not a collective investment scheme which is not authorized by the SFC, nor is it holding the Offer Shares on behalf of such schemes.

<<<PAGE 27>>>
27
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
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
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated December 31, 2025 issued by the Company 
for detailed information about the Global Offering described above before deciding whether or 
not to invest in the Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the paragraph headed “Underwriting 
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing 
Date (which is currently expected to be on January 12, 2026).

<<<PAGE 28>>>
28
Public Float
Immediately after the completion of the Global Offering (before any exercise of the Over-
allotment Option), the total market value of the H Shares to be held by the public is expected to be 
approximately HK$4,799.8 million, calculated based on the final Offer Price of HK$104.8, which is 
higher than the prescribed expected market value of H Shares required to be held in public hands of 
not less than HK$3,000,000,000 under Rule 19A.13A(2)(b) of the Listing Rules, thereby satisfying 
Rule 19A.13A(2) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the H Shares of the Company at the time of Listing. Based on the 
Offer Price of HK$104.8 per H Share, the Company confirmed that it complies with the free float 
requirement under Rule 19A.13C(2)(b) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering (before any 
exercise of the Over-allotment Option): (i) the Shares will be held by at least 300 Shareholders 
at the time of Listing, in compliance with Rule 8.08(2) of the Listing Rules; (ii) the three largest 
public Shareholders will not hold more than 50% of the H Shares held in public hands at the 
time of Listing, in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; (iii) no placee 
will, individually, be placed more than 10% of the enlarged issued share capital of the Company 
immediately after the Global Offering; and (iv) there will not be any new substantial Shareholder 
(as defined in the Listing Rules) immediately after the Global Offering.
Commencement of Dealings
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Monday, January 
12, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting — Underwriting Arrangements 
and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade the H Shares on the basis of publicly available allocation 
details prior to the receipt of H Share certificates or prior to the H Share certificates becoming valid 
evidence of title do so entirely at their own risk.

<<<PAGE 29>>>
29
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Monday, 
January 12, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Monday, January 12, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 100 H Shares each, and the stock code of the H Shares will be 
0501.
By order of the Board
OmniVision Integrated Circuits Group, Inc.
Mr. YU Renrong
Chairman of the Board and Executive Director
Hong Kong, January 9, 2026
As of the date of this announcement, the Directors of the Company named in the application to which this announcement relates 
are: (i) Mr. YU Renrong, Mr. WU Xiaodong, Mr. JIA Yuan and Ms. QIU Huanping as executive Directors; (ii) Mr. LYU Dalong 
and Ms. CHEN Yu as non-executive Directors; and (iii) Mr. ZHU Liting, Ms. FAN Mingxi and Mr. MOU Lei as independent 
non-executive Directors.
