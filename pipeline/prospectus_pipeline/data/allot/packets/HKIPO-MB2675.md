# 配发结果公告抽取任务：2675.HK Shenzhen Edge Medical Co., Ltd.- B - H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**07/01/2026 22:47**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0107/2026010701900.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2675.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the Hong Kong prospectus dated December 30, 2025 (the “Prospectus”) of Shenzhen Edge Medical Co., 
Ltd. (深圳市精鋒醫療科技股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for any securities. This announcement is not a prospectus. Potential investors should read the Prospectus 
for detailed information about the Global Offering described below before deciding whether or not to invest in 
the Offer Shares. Any investment decision in relation to the Offer Shares should be taken solely in reliance on the 
information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities 
in the United States or in any other jurisdictions. The Offer Shares have not been and will not be registered under 
the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities Act”) or securities law 
of any state or other jurisdiction of the United States and may not be offered, sold, pledged or otherwise transferred 
within the United States, except in transactions exempt from, or not subject to, the registration requirements of the 
U.S. Securities Act and in compliance with any applicable state securities laws. There will be no public offer of the 
Offer Shares in the United States. The Offer Shares are being offered and sold solely (1) to qualified institutional 
buyers as defined in Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under the U.S. 
Securities Act; and (2) outside the United States in offshore transactions in reliance on Regulation S under the U.S. 
Securities Act and applicable laws of each jurisdiction where those offers and sales occur.
In connection with the Global Offering, Morgan Stanley Asia Limited as stabilizing manager (the “Stabilization 
Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, the extent permitted by the 
applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect transactions 
with a view to stabilizing or supporting the market price of the H Shares at such price, in such amounts and in such 
manners as the Stabilization Manager, its affiliates or any person acting for it may determine and at a level higher 
than that which might otherwise prevail for a limited period after the Listing Date. However, there is no obligation 
on the Stabilization Manager (or its affiliates or any person acting for it) to conduct any such stabilizing action. 
Such stabilizing action, if taken, (a) will be conducted at the absolute discretion of the Stabilization Manager (or its 
affiliates or any person acting for it) and in what the Stabilization Manager reasonably regards as the best interest 
of our Company, (b) may be discontinued at any time and (c) is required to be brought to an end within 30 days of 
the last day for lodging applications under the Hong Kong Public Offering. Such Stabilizing action, if taken, may be 
effected in all jurisdictions where it is permissible to do so, in each case in compliance with all applicable laws, rules 
and regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws 
of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong 
Kong). Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares 
for longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th 
day after the last day for lodging applications under the Hong Kong Public Offering. After this date, when no further 
stabilizing action may be taken, demand for the H Shares, and therefore the price of the H Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to term and conditions set out in 
the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or 
not resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint Sponsors and Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong 
Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section 
headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. on the Listing Date (which is currently expected to be on 
Thursday, January 8, 2026).

<<<PAGE 2>>>
2
Shenzhen Edge Medical Co., Ltd.
深圳市精鋒醫療科技股份有限公司
(A joint stock company established in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under
the Global Offering
:
27,722,200 H Shares (subject to
 the Over-allotment Option)
Number of Hong Kong Offer Shares
:
2,772,300 H Shares
Number of International Offer Shares
:
24,949,900 H Shares (subject to 
 the Over-allotment Option)
Offer Price
:
HK$43.24 per H Share, plus brokerage of
 1.0%, AFRC transaction levy of
 0.00015%, SFC transaction levy of
 0.0027% and Stock Exchange trading fee
 of 0.00565%
Nominal value
:
RMB1.00 per H Share
Stock code
:
2675
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Overall Coordinators, Joint Global Coordinators Joint Bookrunners
and Joint Lead Managers
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager

<<<PAGE 3>>>
3
Shenzhen Edge Medical Co., Ltd.
深圳市精鋒醫療科技股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated December 30, 2025 (the “Prospectus”) issued 
by Shenzhen Edge Medical Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the Shares could 
move substantially even with a small number of Shares traded and should exercise extreme 
caution when dealing in the Shares.
SUMMARY
Company information
Stock code
2675
Stock short name
EDGE MEDICAL-B
Dealings commencement date
January 8, 2026*
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$43.24
Offer Price Adjustment exercised
N/A
Offer Shares and Share Capital
Number of Offer Shares
27,722,200
Number of Offer Shares in Hong Kong Public Offering
2,772,300
Number of Offer Shares in International Offering
24,949,900
Number of issued Shares upon Listing
387,722,200
Over-allocation
No. of Offer Shares over-allocated
4,158,300
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.

<<<PAGE 4>>>
4
Proceeds
Gross proceeds (Note)
HK$1,198.7 million
 Less: Estimated listing expenses payable based on 
  Final Offer Price
HK$(82.1) million
Net proceeds
HK$1,116.6 million
Note: Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The 
Company intends to apply the additional net proceeds from the exercise of the Over-allotment Option (if any) 
for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus on a 
pro rata basis. During the Track Record Period, the Company incurred HK$20.2 million of listing expenses, 
among which, HK$18.5 million was charged to the consolidated statements of profit or loss of the Company.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
196,179
No. of successful applications
19,967
Subscription level
1,091.94 times
Claw-back triggered
No
No. of Offer Shares initially available under the Hong 
Kong Public Offering
2,772,300
% of Offer Shares under the Hong Kong Public 
Offering to the Global Offering
10%
Final no. of Offer Shares under the Hong Kong Public 
Offering (after over-allocation)
2,772,300
% of final no. of Offer Shares under the Hong Kong 
Public Offering to the Global Offering (after over-
allocation)
8.70%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can 
refer to http://www.hkeipo.hk/IPOResult to perform a search by identification number or 
http://www.tricor.com.hk/ipo/result for the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
175
Subscription Level
25.18 times
No. of Offer Shares initially available under the 
International Offering
24,949,900
% of Offer Shares under the International Offering to 
the Global Offering
90%
Final no. of Offer Shares under the International 
Offering (after over-allocation)
29,108,200
% of final no. of Offer Shares under the International 
Offering to the Global Offering (after over-allocation)
91.30%
The Directors confirm that, to the best of their knowledge, information and belief, save for consent 
to permit the Company to, among other things, allocate Shares in the International Offering to 
certain existing Shareholders and close associates of certain existing Shareholders, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, Supervisors, chief executive of the Company, controlling 
shareholders, substantial shareholders, existing shareholders of the Company or any of its 
subsidiaries or their respective close associates; and (ii) none of the placees and the public who 
have purchased the Offer Shares are accustomed to taking instructions from the Company, any of 
the Directors, Supervisors, chief executive of the Company, controlling shareholders, substantial 
shareholders, existing shareholders of the Company or any of its subsidiaries or their respective 
close associates in relation to the acquisition, disposal, voting or other disposition of Shares 
registered in his/her/its name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
Investor Note 1
No. of 
Offer Shares
allocated
Approximate % 
of Offer 
Shares Note 2
Approximate % 
of total issued 
share  capital 
after the 
Global
Offering Note 2
Existing 
Shareholders or 
their close 
associates
Abu Dhabi Investment Authority
2,699,000
9.74%
0.70%
No
UBS Asset Management 
 (Singapore) Ltd. Note 3
1,799,300
6.49%
0.46%
No
OrbiMed Genesis Master Fund, L.P. Note 4
1,799,300
6.49%
0.46%
Existing 
Shareholder
Huang River Investment Limited
899,600
3.25%
0.23%
No
LYFE Capital Fund IV (Dragon), L.P. Note 5
899,600
3.25%
0.23%
Close associate 
of an existing 
shareholder

<<<PAGE 6>>>
6
Investor Note 1
No. of 
Offer Shares
allocated
Approximate % 
of Offer 
Shares Note 2
Approximate % 
of total issued 
share  capital 
after the 
Global
Offering Note 2
Existing 
Shareholders or 
their close 
associates
Poly Platinum Enterprises Limited Note 6
539,800
1.95%
0.14%
Close associate 
of an existing 
shareholder
Mega Prime Development Limited Note 6
359,800
1.30%
0.09%
Close associate 
of an existing 
shareholder
China Asset Management (Hong Kong) 
Limited Note 7
899,600
3.25%
0.23%
No
China Alpha Fund Management (HK) Ltd
899,600
3.25%
0.23%
No
Tekful Limited
539,800
1.95%
0.14%
No
Integrated Core Strategies (Asia) Pte. Ltd.
539,800
1.95%
0.14%
No
Sage Partners Master Fund Note 8
539,800
1.95%
0.14%
Close associate 
of an existing 
shareholder
Panjing Harbourview Investment Fund
539,800
1.95%
0.14%
No
Infini Global Master Fund
539,800
1.95%
0.14%
No
Total
13,494,600
48.68%
3.48%
Note:
1. 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in 
the Prospectus.
2. 
Before any exercise of the Over-allotment Option.
3. 
UBS Asset Management (Singapore) Ltd. (“UBS AM Singapore”) is a connected client of UBS AG 
Singapore Branch (“UBS AG Singapore”). For details of consent under paragraph 1C(1) of Appendix F1 of 
the Listing Rules (the “Placing Guidelines”) in relation to allocations to connected clients as Cornerstone 
Investors, please refer to the section headed “Allotment Results Details – International Offering – Allottees 
with Waivers/Consents Obtained” in this announcement.
4. 
OrbiMed Genesis Master Fund, L.P. (“OrbiMed Genesis”) and its close associate, OrbiMed New Horizons 
Master Fund, L.P., are existing Shareholders of our Company, holding in aggregate approximately 0.33% of 
the equity interest in the Company immediately prior to the Global Offering. For details of consent under 
Rule 10.04 and paragraph 1C(2) of the Placing Guidelines for allocation of Offer Shares to a close associate 
of an existing shareholder as Cornerstone Investor, please refer to the section headed “Allotment Results 
Details – International Offering – Allottees with Waivers/Consents Obtained” in this announcement.

<<<PAGE 7>>>
7
Investor Note 1
No. of 
Offer Shares
allocated
Approximate % 
of Offer 
Shares Note 2
Approximate % 
of total issued 
share  capital 
after the 
Global
Offering Note 2
Existing 
Shareholders or 
their close 
associates
5. 
LYFE Capital Fund IV (Dragon), L.P. is a close associate of Guadalupe Peak Limited, which in turn holds 
approximately 5.27% equity interest in the Company immediately prior to the Global Offering. For details of 
consent under paragraph 1C(2) of the Placing Guidelines for allocation of Offer Shares to a close associate of 
an existing shareholder as Cornerstone Investor, please refer to the section headed “Allotment Results Details 
– International Offering – Allottees with Waivers/Consents Obtained” in this announcement.
6. 
Mega Prime Development Limited and Poly Platinum Enterprises Limited are close associates of GBA Fund 
Investment Limited (“GBA Fund”), with GBA Fund holding approximately 0.33% of the equity interest 
in the Company immediately prior to the Global Offering. For details of consent under paragraph 1C(2) 
of the Placing Guidelines for allocation of Offer Shares to a close associate of an existing shareholder as 
Cornerstone Investor, please refer to the section headed “Allotment Results Details – International Offering – 
Allottees with Waivers/Consents Obtained” in this announcement.
7. 
China Asset Management (Hong Kong) Limited (“ChinaAMC (HK)”) is a connected client of CLSA 
Limited. For details of consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to 
connected clients as Cornerstone Investors, please refer to the section headed “Allotment Results Details – 
International Offering – Allottees with Waivers/Consents Obtained” in this announcement.
8. 
Sage Partners Master Fund is a close associate of Sage Partners Alpha 1 L.P. (“Sage Partners”) with Sage 
Partners holding approximately 0.20% of the equity interest in the Company immediately prior to the Global 
Offering. For details of consent under paragraph 1C(2) of the Placing Guidelines for allocation Offer Shares 
to a close associate of an existing shareholder as Cornerstone Investor, please refer to the section headed 
“Allotment Results Details – International Offering – Allottees with Waivers/Consents Obtained” in this 
announcement.
Allottees with Waivers/Consents Obtained
Investor
No. of
Offer Shares
allocated
Approximate % 
of Offer 
Shares Note 1
Approximate % of 
total issued 
share capital after 
the Global
Offering Note 1
Relationship
Allottees with consent under Rule 10.04 of the Listing Rules and/or Paragraph 1C(2) of the Placing Guidelines – Allocation of 
Offer Shares to an existing shareholder and/or close associates of existing shareholders Note 2
OrbiMed Genesis
1,799,300
6.49%
0.46%
A Cornerstone 
Investor, an existing 
shareholder and a 
close associate of an 
existing shareholder
LYFE Capital Fund IV (Dragon), L.P.
899,600
3.25%
0.23%
A Cornerstone 
Investor and a close 
associate of an 
existing shareholder
Poly Platinum Enterprises Limited
539,800
1.95%
0.14%
A Cornerstone 
Investor and a close 
associate of an 
existing shareholder

<<<PAGE 8>>>
8
Investor
No. of
Offer Shares
allocated
Approximate % 
of Offer 
Shares Note 1
Approximate % of 
total issued 
share capital after 
the Global
Offering Note 1
Relationship
Mega Prime Development Limited
359,800
1.30%
0.09%
A Cornerstone 
Investor and a close 
associate of an 
existing shareholder
Sage Partners Master Fund
539,800
1.95%
0.14%
A Cornerstone 
Investor and a close 
associate of an 
existing shareholder
3H Health Investment Fund II, L.P.
540,000
1.95%
0.14%
A placee and a close 
associate of existing 
shareholders
Dragon Warrior Investments Limited
90,000
0.32%
0.02%
A placee and a close 
associate of existing 
shareholders
GF Securities Asset Management 
(Guangdong) Co., Ltd. (“GF Securities 
AM”)
1,800
0.01%
0.00%
A placee, a 
connected client of 
GF Securities (Hong 
Kong) Brokerage 
Limited (“GF 
Securities (Hong 
Kong) Brokerage”) 
and a close associate 
of an existing 
shareholder
GF International Investment Management 
Limited (“GF International”),
1,800
0.01%
0.00%
A placee, a 
connected client of 
GF Securities (Hong 
Kong) Brokerage 
and a close associate 
of an existing 
shareholder
E Fund Management Co., Ltd. (“E Fund”)
98,800
0.36%
0.03%
A placee, a 
connected client of 
GF Securities (Hong 
Kong) Brokerage 
and a close associate 
of an existing 
shareholder

<<<PAGE 9>>>
9
Investor
No. of
Offer Shares
allocated
Approximate % 
of Offer 
Shares Note 1
Approximate % of 
total issued 
share capital after 
the Global
Offering Note 1
Relationship
E Fund Management (Hong Kong) Co., Ltd. 
(“E Fund Hong Kong”)
9,200
0.03%
0.00%
A placee, a 
connected client of 
GF Securities (Hong 
Kong) Brokerage 
and a close associate 
of an existing 
shareholder
Value Partners Hong Kong Limited (“Value 
Partners”)
5,000
0.02%
0.00%
A placee, a 
connected client of 
GF Securities (Hong 
Kong) Brokerage 
and a close associate 
of an existing 
shareholder
Taibai Investments Pte. Ltd.
900,000
3.25%
0.23%
A placee and a close 
associate of existing 
shareholders
Mirae Asset Securities Co., Ltd.
3,500
0.01%
0.00%
A placee and a 
close associate of an 
existing shareholder
Mirae Asset Securities (HK) Limited
90,000
0.32%
0.02%
A placee and a 
close associate of an 
existing shareholder
CICC Financial Trading Limited
6,500
0.02%
0.00%
A placee, a 
connected client of 
China International 
Capital Corporation 
Hong Kong 
Securities Limited 
(“CICCHKS”) and 
a close associate 
of an existing 
shareholder
Note:
1. 
Before any exercise of the Over-allotment Option.
2. 
For details of the consent under Rule 10.04 of the Listing Rules and paragraph 1C(2) of the Placing 
Guidelines granted by the Stock Exchange to permit the Company to allocate certain Offer Shares in the 
International Offering to existing shareholders and/or close associates of existing Shareholders, please refer 
to the section headed “Waivers and Exemption” in the Prospectus and the section headed “Others/Additional 
Information” in this announcement.

<<<PAGE 10>>>
10
Investor
No. of
Offer Shares
allocated
Approximate % 
of Offer 
Shares Note 1
Approximate % of 
total issued 
share capital after 
the Global
Offering Note 1
Relationship
Allottees with consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to connected clients Note 2
ChinaAMC (HK)
899,600
3.25%
0.23%
A Cornerstone Investor 
and a connected client 
of CLSA Limited 
(“CLSA”)
GF International Investment Management Limited 
 (“GF International”)
1,800
0.01%
0.00%
A placee, a connected 
client of GF Securities 
(Hong Kong) 
Brokerage and a close 
associate of an existing 
shareholder
GF Securities Asset Management (Guangdong) 
 Co., Ltd. (“GF Securities AM”)
1,800
0.01%
0.00%
A placee, a connected 
client of GF Securities 
(Hong Kong) 
Brokerage and a close 
associate of an existing 
shareholder

<<<PAGE 11>>>
11
Investor
No. of
Offer Shares
allocated
Approximate % 
of Offer 
Shares Note 1
Approximate % of 
total issued 
share capital after 
the Global
Offering Note 1
Relationship
E Fund Management Co., Ltd. (“E Fund”)
98,800
0.36%
0.03%
A placee, a connected 
client of GF Securities 
(Hong Kong) 
Brokerage and a close 
associate of an existing 
shareholder
E Fund Management (Hong Kong) Limited 
 (“E Fund Hong Kong”)
9,200
0.03%
0.00%
A placee, a connected 
client of GF Securities 
(Hong Kong) 
Brokerage and a close 
associate of an existing 
shareholder
Value Partners Hong Kong Limited 
 (“Value Partners”)
5,000
0.02%
0.00%
A placee, a connected 
client of GF Securities 
(Hong Kong) 
Brokerage and a close 
associate of an existing 
shareholder
UBS Asset Management (Singapore) Ltd. 
 (“UBS AM Singapore”)
1,799,300
6.49%
0.46%
A placee and a 
connected client of 
UBS AG Singapore 
Branch (“UBS AG 
Singapore”)
ICBC UBS Asset Management Co., Ltd. 
 (“ICBC UBS”)
125,000
0.45%
0.03%
A placee and a 
connected client of 
UBS AG Singapore
CICC Financial Trading Limited 
 (“CICC FT”)
6,500
0.02%
0.00%
A placee, a connected 
client of CICCHKS and 
a close associate of an 
existing shareholder
CITIC Securities International Capital 
 Management Limited (“CSICM”)
741,400
2.67%
0.19%
A placee and a 
connected client of 
CLSA
Note:
1. 
Before any exercise of the Over-allotment Option.
2. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to 
connected clients, please refer to the section headed “Waivers and Exemption” in the Prospectus and the 
section headed “Others/Additional Information” in this announcement.

<<<PAGE 12>>>
12
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of shares 
held in the Company 
subject to lock-up
undertakings upon
Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings
upon Listing Note 1
Last day subject 
to the lock-up 
undertakings
Dr. Wang Note 2
31,368,798 Unlisted Shares 
73,193,861 H Shares
26.97%
January 8, 2027 Note 3
Dr. Gao Note 2
15,500,065 Unlisted Shares 
36,166,819 H Shares
13.33%
January 8, 2027 Note 3
Xieli Chuangfeng Note 2
10,708,126 H Shares
2.76%
January 8, 2027 Note 3
Subtotal
166,937,669
43.06%
Notes:
(1) 
Before any exercise of the Over-allotment Option.
(2) 
Dr. Wang is the sole general partner of Xieli Chuangfeng. By virtue of their spousal relationship, Dr. Wang 
and Dr. Gao, together with Xieli Chuangfeng (an entity controlled by Dr. Wang) form a group of Controlling 
Shareholders of our Company upon Listing.
(3) 
The expiry day of the lock-up period shown in the table above is pursuant to the PRC Company Law. In 
accordance with the relevant Listing Rule and guidance materials, the required lock-up for the First Six-
Month Period ends on July 8, 2026 and the Second Six-Month Period ends on January 8, 2027.
Pre-IPO Investors
Name
Number of shares 
held in the Company 
subject to lock-up
undertakings upon
Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings
upon Listing Note 1
Last day subject 
to the lock-up 
undertakings
Chengdu Mingsheng
17,504,640 H Shares
4.51%
January 8, 2027 Note 2
Zhongheng Huijin
16,359,120 H Shares
4.22%
January 8, 2027 Note 2
Suzhou Junlian
701,778 Unlisted Shares
11,787,990 H Shares
3.22%
January 8, 2027 Note 2
Sanzheng Zhengyun
11,691,424 H Shares
3.02%
January 8, 2027 Note 2
Social Security Fund
272,913 Unlisted Shares
4,584,216 H Shares
1.25%
January 8, 2027 Note 2

<<<PAGE 13>>>
13
Name
Number of shares 
held in the Company 
subject to lock-up
undertakings upon
Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings
upon Listing Note 1
Last day subject 
to the lock-up 
undertakings
Shenzhen Zhihui
4,473,922 H Shares
1.15%
January 8, 2027 Note 2
Khorgos Lianpan
4,892,760 H Shares
1.26%
January 8, 2027 Note 2
Beijing Xinghao
4,892,760 H Shares
1.26%
January 8, 2027 Note 2
HongShan Growth
1,290,060 Unlisted Shares
3,010,140 H Shares
1.11%
January 8, 2027 Note 2
Taijiashan Healthcare Fund
1,318,189 Unlisted Shares
3,075,775 H Shares
1.13%
January 8, 2027 Note 2
Shenzhen Hanchen
1,318,189 Unlisted Shares
3,075,775 H Shares
1.13%
January 8, 2027 Note 2
Guoce Green Technology
3,998,261 H Shares
1.03%
January 8, 2027 Note 2
Guoce Technology Manufacturing
2,817,275 H Shares
0.73%
January 8, 2027 Note 2
Jiaxing Siqi
333,586 H Shares
0.09%
January 8, 2027 Note 2
Jiaxing Yusheng
168,360 H Shares
0.04%
January 8, 2027 Note 2
Lingang Lanwan Fund I
2,388,960 H Shares
0.62%
January 8, 2027 Note 2
China State-owned Enterprise Mixed 
Ownership Reform Fund
1,911,240 H Shares
0.49%
January 8, 2027 Note 2
Vertex Investment
441,270 Unlisted Shares
1,323,810 H Shares
0.46%
January 8, 2027 Note 2
Beijing Yahui Jinlin
1,715,040 H Shares
0.44%
January 8, 2027 Note 2
Yu Anding (余安定)
1,476,720 H Shares
0.38%
January 8, 2027 Note 2
Hainan Yuanfeng
1,466,280 H Shares
0.38%
January 8, 2027 Note 2
Hangzhou Kangyin
1,466,280 H Shares
0.38%
January 8, 2027 Note 2
CICC Pucheng
1,466,280 H Shares
0.38%
January 8, 2027 Note 2
Chengdu Boyuan Jiayu
1,466,280 H Shares
0.38%
January 8, 2027 Note 2
Wuxi FirstLight
1,194,480 H Shares
0.31%
January 8, 2027 Note 2
Guangyuan Zhonghe
1,168,560 H Shares
0.30%
January 8, 2027 Note 2
Jiaxing Suizi
944,216 H Shares
0.24%
January 8, 2027 Note 2
Fan Xiaolin (范曉霖)
716,760 H Shares
0.18%
January 8, 2027 Note 2

<<<PAGE 14>>>
14
Name
Number of shares 
held in the Company 
subject to lock-up
undertakings upon
Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings
upon Listing Note 1
Last day subject 
to the lock-up 
undertakings
Qingdao Yizhou
716,760 H Shares
0.18%
January 8, 2027 Note 2
Hangzhou Xiangshu
477,720 H Shares
0.12%
January 8, 2027 Note 2
Guangzhou Jinyuan
422,071 H Shares
0.11%
January 8, 2027 Note 2
Jiang Hao (姜昊)
372,960 H Shares
0.10%
January 8, 2027 Note 2
Guadalupe Peak Limited
4,741,110 Unlisted 
Shares
14,223,330 H Shares
4.89%
January 8, 2027 Note 2
Intelligent Spark
4,300,128 Unlisted 
Shares
10,033,632 H Shares
3.70%
January 8, 2027 Note 2
Spark Plug
2,388,960 H Shares
0.62%
January 8, 2027 Note 2
Robust Edge Investments
10,563,551 H Shares
2.72%
January 8, 2027 Note 2
Centroid Investments
8,386,920 H Shares
2.16%
January 8, 2027 Note 2
Springleaf Investments
2,293,380 Unlisted 
Shares
5,351,220 H Shares
1.97%
January 8, 2027 Note 2
True Light
573,372 Unlisted Shares
1,337,868 H Shares
0.49%
January 8, 2027 Note 2
Kangji Medical
5,865,840 H Shares
1.51%
January 8, 2027 Note 2
GBA Fund
1,194,480 H Shares
0.31%
January 8, 2027 Note 2
Sage Partners
716,760 H Shares
0.18%
January 8, 2027 Note 2
Octagon Investments
716,760 H Shares
0.18%
January 8, 2027 Note 2
OrbiMed Genesis
597,240 H Shares
0.15%
January 8, 2027 Note 2
OrbiMed New Horizons
597,240 H Shares
0.15%
January 8, 2027 Note 2
Mirae Asset Global Investments
477,720 H Shares
0.12%
January 8, 2027 Note 2
Subtotal
193,062,331
49.79%
Notes:
(1) 
Before any exercise of the Over-allotment Option.
(2) 
The expiry day of the lock-up period shown in the table above is pursuant to the PRC Company Law.

<<<PAGE 15>>>
15
Cornerstone Investors
Name
Number of H Shares 
held in the Company 
subject to lock-up
undertakings upon
Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings
upon Listing Note 1
Last day subject 
to the lock-up 
undertakings
Abu Dhabi Investment Authority
2,699,000
0.70%
July 8, 2026Note 2
UBS Asset Management (Singapore) Ltd.
1,799,300
0.46%
July 8, 2026Note 2
OrbiMed Genesis Master Fund, L.P.
1,799,300
0.46%
July 8, 2026Note 2
Huang River Investment Limited
899,600
0.23%
July 8, 2026Note 2
China Asset Management (Hong Kong) Limited
899,600
0.23%
July 8, 2026Note 2
LYFE Capital Fund IV (Dragon), L.P.
899,600
0.23%
July 8, 2026Note 2
Poly Platinum Enterprises Limited
539,800
0.14%
July 8, 2026Note 2
Mega Prime Development Limited
359,800
0.09%
July 8, 2026Note 2
China Alpha Fund Management (HK) Ltd
899,600
0.23%
July 8, 2026Note 2
Tekful Limited
539,800
0.14%
July 8, 2026Note 2
Integrated Core Strategies (Asia) Pte. Ltd.
539,800
0.14%
July 8, 2026Note 2
Sage Partners Master Fund
539,800
0.14%
July 8, 2026Note 2
Panjing Harbourview Investment Fund
539,800
0.14%
July 8, 2026Note 2
Infini Global Master Fund
539,800
0.14%
July 8, 2026Note 2
Total
13,494,600
3.48%
Notes:
(1) 
Before any exercise of the Over-allotment Option.
(2) 
The expiry day of the lock-up period shown in the table above is pursuant to the relevant Cornerstone 
Investment Agreements.

<<<PAGE 16>>>
16
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
H Shares allotted
Allotment as % 
of International 
Offering (assuming 
no exercise of the 
Over-allotment 
Option)
Allotment as % 
of International 
Offering (assuming 
the Over-
allotment Option 
is fully 
exercised and new 
H Shares are 
issued)
Allotment as % of 
total Offer Shares 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as % 
of total Offer 
Shares (assuming 
the Over-
allotment 
Option is fully 
exercised and new 
H Shares are 
issued)
Number of 
Shares held 
upon Listing
Number of 
Shares held 
upon Listing as 
% of total issued 
share capital upon 
Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
Number of 
Shares held 
upon Listing as % 
of total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and new 
H Shares are 
issued)
Top 1
2,699,000
10.8%
9.3%
9.7%
8.5%
2,699,000
0.7%
0.7%
Top 5
8,963,600
35.9%
30.8%
32.3%
28.1%
10,158,080
2.6%
2.6%
Top 10
13,462,400
54.0%
46.2%
48.6%
42.2%
44,371,640
11.4%
11.3%
Top 25
22,392,700
89.8%
76.9%
80.8%
70.2%
83,943,835
21.7%
21.4%
Note:
* 
Ranking of placees is based on the number of Shares allotted to the placees.

<<<PAGE 17>>>
17
H SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares 
allotted
Allotment as % 
of International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as % 
of International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Allotment as % 
of total Offer 
Shares 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as % 
of total Offer 
Shares 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Number of 
H Shares held 
upon Listing
Number of 
H Shares held 
upon Listing as 
% of total issued 
H share capital 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
Number of 
H Shares held 
upon Listing as 
% of total 
issued H share 
capital upon 
Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Number of 
Shares held
upon Listing
Top 1
–
0.0%
0.0%
0.0%
0.0%
120,068,806
37.1%
36.6%
166,937,669
Top 5
746,600
3.0%
2.6%
2.7%
2.3%
202,861,827
62.7%
61.9%
250,705,381
Top 10
2,546,200
10.2%
8.7%
9.2%
8.0%
254,490,247
78.6%
77.6%
318,168,229
Top 25
11,515,900
46.2%
39.6%
41.5%
36.1%
299,316,631
92.5%
91.3%
362,994,613
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholder upon Listing.

<<<PAGE 18>>>
18
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number of 
H Shares allotted
Allotment as % 
of International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as % 
of International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised and new 
Shares are 
issued)
Allotment as % 
of total Offer 
Shares 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as % 
of total Offer 
Shares 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Shares 
are issued)
Number of 
Shares held 
upon Listing
Number of 
Shares held upon 
Listing as % 
of total issued 
share capital 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
Number of 
Shares held upon 
Listing as % 
of total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Shares 
are issued)
Top 1
–
0.0%
0.0%
0.0%
0.0%
166,937,669
43.1%
42.6%
Top 5
1,646,200
6.6%
5.7%
5.9%
5.2%
253,222,524
65.3%
64.6%
Top 10
2,546,200
10.2%
8.7%
9.2%
8.0%
318,168,229
82.1%
81.2%
Top 25
11,515,900
46.2%
39.6%
41.5%
36.1%
363,293,413
93.7%
92.7%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 19>>>
19
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, 19,967 valid applications 
made by the public will be conditionally allocated on the basis set out below:
Number of 
H Shares 
applied for
Number of 
valid applications
Basis of 
allocation/ballot
Approximate % 
allotted of the total 
no. of H Shares 
applied for
POOL A
100
91,082
456 out of 91,082 applicants to 
receive 100 H Shares
0.50%
200
28,073
242 out of 28,073 applicants to 
receive 100 H Shares
0.43%
300
3,955
47 out of 3,955 applicants to 
receive 100 H Shares
0.40%
400
1,934
29 out of 1,934 applicants to 
receive 100 H Shares
0.37%
500
2,746
49 out of 2,746 applicants to 
receive 100 H Shares
0.36%
600
1,206
25 out of 1,206 applicants to 
receive 100 H Shares
0.35%
700
957
22 out of 957 applicants to receive 
100 H Shares
0.33%
800
1,046
27 out of 1,046 applicants to 
receive 100 H Shares
0.32%
900
771
22 out of 771 applicants to receive 
100 H Shares
0.32%
1,000
17,714
532 out of 17,714 applicants to 
receive 100 H Shares
0.30%
1,500
2,607
108 out of 2,607 applicants to 
receive 100 H Shares
0.28%
2,000
4,622
238 out of 4,622 applicants to 
receive 100 H Shares
0.26%
2,500
2,431
149 out of 2,431 applicants to 
receive 100 H Shares
0.25%
3,000
1,627
115 out of 1,627 applicants to 
receive 100 H Shares
0.24%
3,500
894
72 out of 894 applicants to receive 
100 H Shares
0.23%
4,000
1,004
89 out of 1,004 applicants to 
receive 100 H Shares
0.22%
4,500
811
79 out of 811 applicants to receive 
100 H Shares
0.22%
5,000
1,853
195 out of 1,853 applicants to 
receive 100 H Shares
0.21%
6,000
1,167
142 out of 1,167 applicants to 
receive 100 H Shares
0.20%
7,000
947
130 out of 947 applicants to 
receive 100 H Shares
0.20%

<<<PAGE 20>>>
20
Number of 
H Shares 
applied for
Number of 
valid applications
Basis of 
allocation/ballot
Approximate % 
allotted of the total 
no. of H Shares 
applied for
POOL A
8,000
872
132 out of 872 applicants to 
receive 100 H Shares
0.19%
9,000
686
114 out of 686 applicants to 
receive 100 H Shares
0.18%
10,000
5,686
1,024 out of 5,686 applicants to 
receive 100 H Shares
0.18%
20,000
3,901
1,205 out of 3,901 applicants to 
receive 100 H Shares
0.15%
30,000
2,405
1,019 out of 2,405 applicants to 
receive 100 H Shares
0.14%
40,000
1,268
672 out of 1,268 applicants to 
receive 100 H Shares
0.13%
50,000
1,324
835 out of 1,324 applicants to 
receive 100 H Shares
0.13%
60,000
797
579 out of 797 applicants to 
receive 100 H Shares
0.12%
70,000
686
562 out of 686 applicants to 
receive 100 H Shares
0.12%
80,000
557
507 out of 557 applicants to 
receive 100 H Shares
0.11%
90,000
455
100 H Shares
0.11%
100,000
3,693
100 H Shares plus 297 out of 
3,693 applicants to receive an 
additional 100 H Shares
0.11%
Total
189,777 Total number of Pool A successful applicants: 13,565

<<<PAGE 21>>>
21
Number of 
H Shares 
applied for
Number of 
valid applications
Basis of 
allocation/ballot
Approximate % 
allotted of the total 
no. of H Shares 
applied for
POOL B
200,000
4,438
100 H Shares plus 3,551 out of 
4,438 applicants to receive an 
additional 100 H Shares
0.09%
300,000
769
200 H Shares plus 165 out of 
769 applicants to receive an 
additional 100 H Shares
0.07%
400,000
315
200 H Shares plus 178 out of 
315 applicants to receive an 
additional 100 H Shares
0.06%
500,000
209
200 H Shares plus 183 out of 
209 applicants to receive an 
additional 100 H Shares
0.06%
600,000
113
300 H Shares
0.05%
700,000
85
300 H Shares plus 26 out of 
85 applicants to receive an 
additional 100 H Shares
0.05%
800,000
66
300 H Shares plus 45 out of 
66 applicants to receive an 
additional 100 H Shares
0.05%
900,000
30
300 H Shares plus 25 out of 
30 applicants to receive an 
additional 100 H Shares
0.04%
1,000,000
92
400 H Shares
0.04%
1,386,100
285
400 H Shares plus 274 out of 
285 applicants to receive an 
additional 100 H Shares
0.04%
Total
6,402 Total number of Pool B successful applicants: 6,402
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.

<<<PAGE 22>>>
22
OTHER INFORMATION
Consent under Rule 10.04 and/or paragraph 1C(2) of the Placing Guidelines – Allocation of 
Offer Shares to an existing shareholder and/or close associates of existing shareholders as 
cornerstone investors
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted to 
the Company, consent under Rule 10.04 of the Listing Rules Paragraph 1C(2) of the Placing 
Guidelines for the allocation of Offer Shares to (i) OrbiMed Genesis, (ii) Mega Prime Development 
Limited and Poly Platinum Enterprises Limited, (iii) LYFE Capital Fund IV (Dragon), L.P. and (iv) 
Sage Partners Master Fund as Cornerstone Investors under the Global Offering. Please refer to the 
section headed “Waivers and Exemption – Waiver and consent under Rule 10.04 and Paragraph 
1C(2) of Appendix F1 to the Listing Rules in respect of subscriptions of Offer Shares by existing 
shareholder and close associates of existing shareholder as cornerstone investors” in the Prospectus 
for details.
Consent under paragraph 1C(2) of the Placing Guidelines – Allocation of Offer Shares to 
close associates of existing shareholders as placees
The Company has applied to the Stock Exchange, and the Stock Exchange has granted a consent 
under paragraph 1C(2) of the Placing Guidelines to permit the Company to allocate such Offer 
Shares in the International Offering to the close associates of existing shareholders as placees 
(together, the “Close Associates of Existing Shareholders as Placees”). Each of 3H Health 
Investment Fund II, L.P. and Dragon Warrior Investments Limited is a close associate of Robust 
Edge Investments Limited and Centroid Investments Limited. Each of GF Securities AM, GF 
International, E Fund, E Fund Hong Kong and Value Partners is a close associate of Guangfa 
Xinde Zhongheng Huijin (Longyan) Equity Investment Partnership (Limited Partnership) (廣
發信德中恒匯金(龍岩)股權投資合夥企業(有限合夥)). Taibai Investments Pte. Ltd. is a close 
associate of Springleaf Investments Pte. Ltd. and True Light Investments P Pte. Ltd.. Each of 
Mirae Asset Securities Co., Ltd. and Mirae Asset Securities (HK) Limited is a close associate of 
Mirae Asset Global Investments (Hong Kong) Limited. CICC FT is a close associate of CICC 
Pucheng Investment Co., Ltd. (中金浦成投資有限公司). The allocation of Offer Shares to the 
Close Associates of Existing Shareholders as Placees is in compliance with all the conditions under 
the consent granted by the Stock Exchange, including but not limited to (i) the Company complies 
with Rules 19A.13A and 19A.13C of the Listing Rules, and (ii) no preference in allocation was 
given to the Close Associates of Existing Shareholders as Placees.
For details of the allocations of Offer Shares to close associates of existing Shareholders, please 
refer to the section headed “Allotment Results Details — International Offering — Allotees with 
Waivers/Consents Obtained” in this announcement.
Placing to connected clients with prior consents under paragraph 1C(1) of the Placing 
Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, 
consents under paragraph 1C(1) of the Placing Guidelines to permit allocation to connected clients 
pursuant to the Placing Guidelines. The allocation of Offer Shares to such connected clients is in 
compliance with all the conditions under the consents granted by the Stock Exchange. Details of 
the placement to connected clients in placing tranche are set out below.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted a 
consent under paragraph 1C(1) of the Placing Guidelines to permit ChinaAMC (HK) to participate 
in the Global Offering as a Cornerstone Investor and connected client holding the Offer Shares 
on a discretionary basis. Please refer to the section headed “Waivers and Exemption – Consent in 
respect of the proposed subscription of Offer Shares by Connected Client” in the Prospectus for 
details.

<<<PAGE 23>>>
23
In addition, the Company has applied to the Stock Exchange, and the Stock Exchange has granted, a consent under paragraph 1C(1) of the 
Placing Guidelines to permit the Company to allocate certain Offer Shares in the International Offering to connected clients. The allocation 
of Offer Shares to such connected clients is in compliance with all the conditions under the consent granted by the Stock Exchange. Details 
of the placement to the connected clients are set out below.
No.
Name of connected 
client
Name of connected 
distributor
Relationship with the 
connected distributor
Basis of holding 
securities
Number of Offer 
Shares subscribed
Approximate 
percentage of 
the Offer Shares 
subscribed (assuming 
the Over-allotment 
Option is not 
exercised)
Approximate 
percentage of total 
issued share capital 
after the Global 
Offering (assuming no 
exercise of the Over-
allotment Option)
1.
GF International(1) 
(as placee)
GF Securities (Hong Kong) 
Brokerage, one of the 
Overall Coordinators
GF International is a 
member of the same 
group of companies as GF 
Securities (Hong Kong) 
Brokerage.
Discretionary
1,800
0.01%
0.00%
2.
GF Securities AM(2) 
(as placee)
GF Securities (Hong Kong) 
Brokerage, one of the 
Overall Coordinators
GF Securities AM is 
a member of the same 
group of companies as GF 
Securities (Hong Kong) 
Brokerage.
Non-discretionary
1,800
0.01%
0.00%
3.
E Fund(3) (as placee)
GF Securities (Hong Kong) 
Brokerage, one of the 
Overall Coordinators
E Fund is a member of the 
same group of companies as 
GF Securities (Hong Kong) 
Brokerage.
Discretionary
98,800
0.36%
0.03%
4.
E Fund Hong 
Kong(4) (as placee)
GF Securities (Hong Kong) 
Brokerage, one of the 
Overall Coordinators
E Fund Hong Kong is 
a member of the same 
group of companies as GF 
Securities (Hong Kong) 
Brokerage.
Discretionary
9,200
0.03%
0.00%
5.
Value Partners(5) (as 
placee)
GF Securities (Hong Kong) 
Brokerage, one of the 
Overall Coordinators
Value Partners is a member 
of the same group of 
companies as GF Securities 
(Hong Kong) Brokerage.
Discretionary
5,000
0.02%
0.00%

<<<PAGE 24>>>
24
No.
Name of connected 
client
Name of connected 
distributor
Relationship with the 
connected distributor
Basis of holding 
securities
Number of Offer 
Shares subscribed
Approximate 
percentage of 
the Offer Shares 
subscribed (assuming 
the Over-allotment 
Option is not 
exercised)
Approximate 
percentage of total 
issued share capital 
after the Global 
Offering (assuming no 
exercise of the Over-
allotment Option)
6.
UBS AM 
Singapore(6) 
(as cornerstone 
investor)
UBS AG Singapore, one 
of the distributors of the 
Global Offering
UBS AM Singapore is a 
member of the same group 
of companies as UBS AG 
Singapore.
Discretionary
1,799,300
6.49%
0.46%
7.
ICBC UBS(7) (as 
placee)
UBS AG Singapore, one 
of the distributors of the 
Global Offering
ICBC UBS is a member 
of the same group of 
companies as UBS AG 
Singapore.
Discretionary
125,000
0.45%
0.03%
8.
CICC FT(8) (as 
placee)
CICCHKS, one of the 
Overall Coordinators
CICC FT is a member of the 
same group of companies as 
CICCHKS.
Non-discretionary
6,500
0.02%
0.00%
9.
CSICM(9) (as 
placee)
CLSA, one of the Overall 
Coordinators
CSICM is a member of the 
same group of companies as 
CLSA.
Non-discretionary
741,400
Shenzhen Commando: 
36,000
Beevest: 
700,000
Perseverance AM: 
5,400
2.67%
Shenzhen Commando: 
0.13%
Beevest: 
2.53%
Perseverance AM: 
0.02%
0.19%
Shenzhen Commando: 
0.01%
Beevest: 
0.18%
Perseverance AM: 
0.00%
Notes:
(1) 
GF International will hold the Offer Shares in its capacity as the discretionary fund manager on behalf of their underlying clients (the “GF International 
Ultimate Clients”), each of which is an independent third party. Save for Ku Sen (顧晨), none of the GF International Ultimate Clients holds 30% or more 
ultimate beneficial interest in the relevant funds. GF International has confirmed that, to the best of their knowledge, each of the GF International Ultimate 
Clients is an independent party of GF International, GF Securities (Hong Kong) Brokerage and the companies which are members of the same group of companies 
as GF Securities (Hong Kong) Brokerage.
(2) 
GF Securities AM is an asset manager that is a QDII as approved by the relevant authority and will hold the Offer Shares as product manager on behalf of GF 
Asset Management Excellent Diversified Allocation No. 10 (QDII) Single Asset Management Plan (廣發資管卓越多元配置 10 號(QDII)單一資產管理計劃), 
with the ultimate client being Feng Tianhong (馮倩紅) (the “GF Securities AM Ultimate Client”). GF Securities AM has confirmed that, to the best of their 
knowledge, the GF Securities AM Ultimate Client is an independent party of GF Securities AM, GF Securities (Hong Kong) Brokerage and the companies which 
are members of the same group of companies as GF Securities (Hong Kong) Brokerage.

<<<PAGE 25>>>
25
(3) 
E Fund will hold the Offer Shares in its capacity as the discretionary fund manager on behalf of their underlying 
clients (the “E Fund Ultimate Clients”), each of which is an independent third party. None of the E Fund 
Ultimate Clients holds more than 30% ultimate beneficial interest in the relevant funds. E Fund has confirmed 
that, to the best of their knowledge, each of the E Fund Ultimate Clients is an independent party of E Fund, GF 
Securities (Hong Kong) Brokerage and the companies which are members of the same group of companies as 
GF Securities (Hong Kong) Brokerage.
(4) 
E Fund Hong Kong will hold the Offer Shares in its capacity as the discretionary fund manager on behalf of 
their underlying clients (the “E Fund Hong Kong Ultimate Clients”), each of which is an independent third 
party. None of the E Fund Hong Kong Ultimate Clients holds more than 30% ultimate beneficial interest in the 
relevant funds. E Fund Hong Kong has confirmed that, to the best of their knowledge, each of the E Fund Hong 
Kong Ultimate Clients is an independent party of E Fund Hong Kong, GF Securities (Hong Kong) Brokerage 
and the companies which are members of the same group of companies as GF Securities (Hong Kong) 
Brokerage.
(5) 
Value Partners will hold the Offer Shares in its capacity as the discretionary fund manager managing the 
SFC-authorized funds on behalf of their underlying clients (the “Value Partners Ultimate Clients”), each of 
which is an independent third party. The ultimate beneficial owners holding 30% or more interest in the SFC-
authorized collective authorized schemes are set out below:
(i) 
AIA International Limited
(ii) 
Bank of China (Hong Kong) Nominees Limited
(iii) 
The Master Trust Bank of Japan Limited.
Value Partners has confirmed that, to the best of their knowledge, each of the Value Partners Ultimate Clients 
is an independent party of Value Partners, GF Securities (Hong Kong) Brokerage and the companies which are 
members of the same group of companies as GF Securities (Hong Kong) Brokerage.
(6) 
UBS AM Singapore will hold the Offer Shares in its capacity as the discretionary fund manager managing 
the funds on behalf of their investors (the “UBS AM Singapore Ultimate Clients”), each of which is an 
independent third party. None of the UBS AM Singapore Ultimate Clients holds more than 30% ultimate 
beneficial interest in the relevant funds. UBS AM Singapore has confirmed that, to the best of their knowledge, 
each of the UBS AM Singapore Ultimate Clients is an independent party of UBS AM Singapore, UBS AG 
Singapore and the companies which are members of the same group of companies as UBS AG.
(7) 
ICBC UBS will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds 
on behalf of their investors (the “ICBC UBS Ultimate Clients”), each of which is an independent third party. 
None of the ICBC UBS Ultimate Clients holds more than 30% ultimate beneficial interest in the relevant funds. 
ICBC UBS has confirmed that, to the best of their knowledge, each of the ICBC UBS Ultimate Clients is an 
independent party of ICBC UBS, UBS AG Singapore and the companies which are members of the same group 
of companies as UBS AG.

<<<PAGE 26>>>
26
(8) 
CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one 
OTC swap transactions (collectively, the “CICC OTC Swaps”) with each other and the ultimate client (the 
“CICC FT Ultimate Client”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary 
basis to hedge the CICC OTC Swaps while the economic risks and returns of the underlying Offer Shares are 
passed to the CICC FT Ultimate Client, subject to customary fees and commissions. The CICC OTC Swaps 
will be fully funded by the CICC FT Ultimate Client. During the terms of the CICC OTC Swaps, all economic 
returns of the Offer Shares subscribed by CICC FT will be passed to the CICC FT Ultimate Client and all 
economic loss shall be borne by the CICC FT Ultimate Client through the CICC OTC Swaps, and CICC FT 
will not take part in any economic return or bear any economic loss in relation to the Offer Shares. Despite that 
CICC FT will hold the legal title of the Offer Shares by itself, it will not exercise the voting rights attaching 
to the relevant Offer Shares during the terms of the CICC OTC Swaps according to its internal policy. The 
CICC FT Ultimate Client is Shanghai Baoyin Private Equity Fund Management Co., Ltd. (上海保銀私募基金
管理有限公司) (“Pinpoint Fund”), which in turn manages the funds Baoyin Duokong Wenjian No. 1 Private 
Equity Investment Fund (保銀多空穩健1號私募證券投資基金) (“Duokong Wenjian No. 1”), Baoyin Duokong 
Wenjian No. 2 Private Equity Investment Fund (保銀多空穩健2號私募證券投資基金) (“Duokong Wenjian 
No. 2”) and Baoyin Jinqu No. 1 Private Equity Investment Fund (保銀進取1號私募證券投資基金)(“Jinqu 
No. 1”). The ultimate beneficial owner holding 30% or more interest in Duokong Wenjian No. 1 and Duokong 
Wenjian No. 2 is. Wang Qiang (王強), with no other ultimate beneficial owners holding 30% or more interest 
in Duokong Wenjian No.1, Duokong Wenjian No. 2 and Jinqu No.1. To the best of CICC FT’s knowledge, after 
making all reasonable inquiries, each of the CICC FT Ultimate Client and its ultimate beneficial owner is a third 
party independent from CICC FT and CICCHKS and the companies which are members of the same group of 
companies as CICCHKS.
(9) 
CSICM will act as the single counterparty of a back-to-back total return swap transaction (the “CSICM 
Back-to-back TRS”) to be entered into by CSICM in connection with a total return swap order (the “CSICM 
Client TRS”) placed by its ultimate clients (the “CSICM Ultimate Clients”), by which CSICM will pass the 
full economic exposure of the Offer Shares placed to CSICM (the “CSICM Offer Shares”) to the CSICM 
Ultimate Client, meaning in effect, CSICM will hold the beneficial interest of the CSICM Offer Shares on 
behalf of the CSICM Ultimate Clients on a non-discretionary basis. CSICM will hold the legal title and 
beneficial interest in the CSICM Offer Shares, but will contractually agree to pass on the full economic 
exposure and return of the CSICM Offer Shares to the CSICM Ultimate Clients. The CSICM Ultimate Clients 
may exercise an early termination right to early terminate the CSICM Client TRS at any time from the trade 
date of the CSICM Client TRS which should be on or after the date on which the CSICM Offer Shares are listed 
on the Stock Exchange. Upon the final maturity or early termination of the CSICM Client TRS by the CSICM 
Ultimate Clients, CSICM will dispose of the CSICM Offer Shares on the secondary market and the CSICM 
Ultimate Clients will receive a final termination amount of the CSICM Back-to-back TRS which should have 
taken into account all the economic returns or economic loss in relation to the CSICM Offer Shares and the 
fixed amount of transaction fees of the CSICM Back-to back TRS and the CSICM Client TRS. CSICM will not 
exercise the voting right of the CSICM Offer Shares during the tenor of the CSICM Back-to-back TRS. The 
CSICM Ultimate Clients are (i) Shenzhen Commando Capital Management Co., Ltd. (深圳市康曼德資本管理
有限公司) investing for and on behalf of nine different funds in the PRC, with the ultimate beneficial owners 
holding 30% or more interest in such funds being Ding Ying (丁楹), Huang Xiaolei (黃曉蕾) and Guo Hongqi 
(郭紅奇), with no other persons holding 30% or more interests therein; and (ii) Beevest Capital Management 
Limited, investing for and on behalf of Global Multi Alpha Fund SP, with the ultimate beneficial owner holding 
30% or more interest in such fund being Zeng Shuzhen and (iii) Perseverance Asset Management L.l.p. (上海
高毅資產管理合夥企業(有限合夥)), investing for and on behalf of five different funds in the PRC, with no 
ultimate beneficial owners holding 30% or more interest in such funds. To the best of CSICM’s knowledge, 
after making all reasonable inquiries, each of the CSICM Ultimate Clients and its ultimate beneficial owner 
is a third party independent from CSICM, CLSA and the companies which are members of the same group of 
companies as CLSA

<<<PAGE 27>>>
27
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
The Offer Shares are being offered and sold (1) solely to qualified institutional buyers as defined 
in Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under 
the U.S. Securities Act and (2) outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated December 30, 2025 issued by Shenzhen Edge Medical 
Co., Ltd.for detailed information about the Global Offering described below before deciding 
whether or not to invest in the H Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to 
terminate their obligations under the Hong Kong Underwriting Agreement with immediate effect 
upon the occurrence of any of the events set out in the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in 
the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is 
currently expected to be on Thursday, January 8, 2026).

<<<PAGE 28>>>
28
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering, 191,842,718 H Shares, representing 
approximately 49.48% of the issued share capital of our Company (before any exercise of the 
Over-allotment Option) will count towards the public float. Therefore, the number of H shares held 
in public hands is higher than the prescribed percentage of H Shares required to be held in public 
hands of 15% under Rule 19A.13A(1) of the Listing Rules, satisfying the minimum percentage 
requirement in compliance with Rule 19A.13A(1) of the Listing Rules calculated based on the 
Offer Price of HK$43.24 per Offer Share.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the Shares of the Company at the time of Listing. Based on the 
final Offer Price of HK$43.24 per H Share, the Company satisfies the free float requirement under 
Rule 19A.13C(1)(b) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering: (i) the 
Shares will be held by at least 300 Shareholders at the time of Listing, in compliance with Rule 
8.08(2) of the Listing Rules; (ii) the three largest public Shareholders will not hold more than 
50% of the H Shares held in public hands at the time of Listing, in compliance with Rules 8.08(3) 
and 8.24 of the Listing Rules; (iii) no placee will, individually, be placed more than 10% of the 
enlarged issued share capital of the Company immediately after the Global Offering; and (iv) there 
will not be any new substantial Shareholder (as defined in the Listing Rules) immediately after the 
Global Offering.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. (Hong Kong time) 
on Thursday, January 8, 2026, provided that (i) the Global Offering has become unconditional 
in all respects, and (ii) the right of termination described in the section headed “Underwriting – 
Underwriting Arrangements and Expenses – Hong Kong Underwriting Agreement – Grounds for 
termination” in the Prospectus has not been exercised. Investors who trade H Shares prior to the 
receipt of H Share certificates or the H Share certificates becoming valid evidence of title do so 
entirely at their own risk. Assuming that the Global Offering becomes unconditional at or before 
8:00 a.m. (Hong Kong time) on Thursday, January 8, 2026, it is expected that dealings in the H 
Shares on the Stock Exchange will commence at 9:00 a.m. on Thursday, January 8, 2026. The H 
Shares will be traded in board lots of 100 H Shares each and the stock code of the H Shares will be 
2675.
By order of the Board
Shenzhen Edge Medical Co., Ltd. 
(深圳市精鋒醫療科技股份有限公司)
Dr. Wang Jianchen
Chairman of the Board and Executive Director
Hong Kong, January 7, 2026
As of the date of this announcement, the board of directors of the Company comprises (i) Dr. 
Wang Jianchen, Dr. Gao Yuanqian and Ms. Wu Mengyuan as executive directors; (ii) Mr. Sheng 
Li, Mr. Chen Gang and Mr. Qiu Xiang as non-executive directors, and (iii) Mr. Yang Fan, Mr. 
Zhang Guoguang and Mr. Lau Ying Kit as independent non-executive directors.
