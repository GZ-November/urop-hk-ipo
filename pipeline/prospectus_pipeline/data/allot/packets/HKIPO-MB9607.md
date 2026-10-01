# 配发结果公告抽取任务：9607.HK Red Avenue New Materials Group Co., Ltd.

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**28/09/2026 20:39**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0928/2026092801809.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"9607.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited
(the
“Stock
Exchange”)
and
Hong
Kong
Securities
Clearing
Company
Limited
(“HKSCC”) take no responsibility for the contents of this announcement, make no
representation as to its accuracy or completeness and expressly disclaim any liability
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of
the contents of this announcement.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the
same meanings as those defined in the prospectus dated September 21, 2026 (the
“Prospectus”) issued by Red Avenue New Materials Group Co., Ltd. (彤程新材料集團股
份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an offer or an
invitation to induce an offer by any person to acquire, purchase or subscribe for any of the
securities of the Company. This announcement is not a prospectus. Potential investors
should read the Prospectus for detailed information about the Global Offering described
below before deciding whether or not to invest in the Offer Shares. Any investment decision
in relation to the Offer Shares should be taken solely in reliance on the information provided
in the Prospectus.
This announcement does not constitute an offer to sell or the solicitation of an offer to buy
nor shall there be any sale of Offer Shares in any jurisdiction in which such offer,
solicitation or sales would be unlawful. This announcement is not for release, publication or
distribution, directly or indirectly, in or into the United States or any other jurisdiction
where such distribution is prohibited by law, nor is this announcement an offer for sale or
solicitation to purchase or subscribe for securities in the United States or any other
jurisdictions. The Offer Shares have not been, and will not be, registered under the United
States Securities Act of 1933, as amended from time to time (the “U.S. Securities Act”), or
any applicable state securities laws, and may not be offered, sold, pledged or transferred
within the United States or to, or for the account or benefit of, U.S. persons (as defined in
Regulation S under the U.S. Securities Act (the “Regulation S”)) except in transactions
exempt from, or not subject to, the registration requirements of the U.S. Securities Act. The
Offer Shares are being offered and sold outside the United States in offshore transactions in
accordance with Regulation S. There will be no public offering of the Offer Shares in the
United States.
No stabilizing manager will be appointed, and it is anticipated that no stabilization
activities will be carried out in relation to the Global Offering.
Potential investors of the Offer Shares should note that the Sole Sponsor and the
Sponsor-Overall Coordinator (for itself and on behalf of the Hong Kong Underwriters)
shall be entitled to terminate their obligations under the Hong Kong Underwriting
Agreement with immediate effect upon the occurrence of any of the events set out in the
paragraph headed “Underwriting — Underwriting Arrangements and Expenses — Hong
Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to
8: 00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on or
about Tuesday, September 29, 2026).
– 1 –

<<<PAGE 2>>>
Red Avenue New Materials Group Co., Ltd.
彤程新材料集團股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under
the Global Offering
:
68,118,700 H Shares
Number of Hong Kong Offer Shares
:
6,811,900 H Shares
Number of International Offer Shares
:
61,306,800 H Shares
Final Offer Price
:
HK$44.00 per H Share plus brokerage of
1.0%, SFC transaction levy of 0.0027%,
Stock Exchange trading fee of 0.00565%
and AFRC transaction levy of 0.00015%
Nominal value
:
RMB1.00 per H Share
Stock code
:
9607
Sole Sponsor, Sponsor-Overall Coordinator, Joint Global Coordinator,
Joint Bookrunner and Joint Lead Manager
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and
Joint Lead Manager
Joint Bookrunners and Joint Lead Managers
– 2 –

<<<PAGE 3>>>
RED AVENUE NEW MATERIALS GROUP CO., LTD.
彤程新材料集團股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the
same meanings as those defined in the prospectus dated September 21, 2026 (the
“Prospectus”) issued by Red Avenue New Materials Group Co., Ltd. (彤程新材料集團股
份有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of
Shareholders, H Shareholders and prospective investors should be aware that the price
of the H Shares could move substantially even with a small number of H Shares traded
and should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company Information
Stock Code
9607
Stock short name
RA MATERIALS
Dealings commencement date
September 29, 2026*
*
see note at the end of the announcement
Price Information
Final Offer Price
HK$44.00
Maximum Offer Price
HK$44.00
Offer Shares and Share Capital
Number of Offer Shares
68,118,700
Number of Offer Shares in Hong Kong Public
Offering
6,811,900
Number of Offer Shares in International Offering
61,306,800
Number of issued Shares upon Listing
684,188,336
Proceeds
Gross proceeds(Note)
HK$2,997.22 million
Less: Estimated listing expenses payable based on
Final Offer Price
HK$(95.93) million
Net proceeds
HK$2,901.29 million
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use
of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” in the
Prospectus.
– 3 –

<<<PAGE 4>>>
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
12,645
No. of successful applications
12,645
Subscription level
3.39 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong
Kong Public Offering
6,811,900
Final no. of Offer Shares under the Hong Kong Public
Offering
6,811,900
% of Offer Shares initially available under the Hong
Kong Public Offering to the Global Offering
10%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to
www.hkeipo.hk/IPOResult to perform a search by identification document number or for the full list of
allottees.
INTERNATIONAL OFFERING
No. of placees
81
Subscription Level
2.75 times
No. of Offer Shares initially available under the
International Offering
61,306,800
Final no. of Offer Shares under the International
Offering
61,306,800
% of Offer Shares initially available under the
International Offering to the Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for a
waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under
paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted
by the Stock Exchange to permit the Company to allocate certain Offer Shares in the
International Offering to certain Permitted Existing Shareholders and/or their close
associates, (i) none of the Offer Shares subscribed by the placees and the public offer
subscribers have been financed directly or indirectly by the Company, any of the Directors,
chief executive of the Company, the Controlling Shareholders, substantial Shareholders,
existing Shareholders or any of its subsidiaries or their respective close associates; (ii) none
of the placees and the public offer subscribers who have subscribed for or purchased the
Offer Shares are accustomed to taking instructions from the Company, any of the
Directors, chief executive of the Company, the Controlling Shareholders, substantial
Shareholders, existing Shareholders or any of its subsidiaries or their respective close
associates in relation to the acquisition, disposal, voting or other disposition of H Shares
registered in his/her/its name or otherwise held by him/her/it; (iii) there is no side
agreement or arrangement between the Company, any of the Directors, chief executive of
the
Company,
the
Controlling
Shareholders,
substantial
Shareholders,
existing
Shareholders of the Company or any of its subsidiaries or their respective close
associates, on one hand, and the public offer subscribers or the placees who have
subscribed for or purchased the Offer Shares, on the other hand; (iv) there is no side
– 4 –

<<<PAGE 5>>>
agreement or arrangement between the Company, any of the Directors, chief executive of
the
Company,
the
Controlling
Shareholders,
substantial
Shareholders,
existing
Shareholders of the Company or any of its subsidiaries or their respective close
associates, on one hand, and any other parties, on the other hand, in connection with the
subscription, purchase, disposal, turnover, or valuation of the Shares; and (v) no rebate has
been, directly or indirectly, provided by the Company, any of the Directors, chief executive
of
the
Company,
the
Controlling
Shareholders,
substantial
Shareholders,
existing
Shareholders of the Company or any of its subsidiaries or their respective close
associates, or syndicate members, or any other brokers involved in the Global Offering,
to any investors in the Hong Kong Public Offering or placees in the International Offering.
The placees in the International Offering include the following:
Cornerstone Investors
InvestorNote 1
No. of Offer
Shares
allocatedNote 2
Approximate %
of total issued H
Shares after the
Global
OfferingNote 3
Approximate %
of total issued
share capital in
the Company
after the Global
OfferingNote 4
Existing
Shareholders or
their close
associates
CNCB Investment
3,208,100
4.7%
0.5%
No
Full Truck
3,564,500
5.2%
0.5%
No
Golden Valley Master
1,782,200
2.6%
0.3%
No
Goldshore
8,028,400
11.8%
1.2%
No
Happy Wisdom
2,676,100
3.9%
0.4%
Yes
Prinx Chengshan HK
1,000,000
1.5%
0.2%
No
Yang Quanhai
891,100
1.3%
0.1%
No
Zhou Bo
1,427,200
2.1%
0.2%
Yes
Total
22,577,600
33.1%
3.3%
Notes:
1.
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone
Investors” in the Prospectus.
2.
Only taking into account the Shares allocated to the relevant investors as cornerstone investors under
the Global Offering. In addition to the Offer Shares subscribed for as Cornerstone Investors, certain
Cornerstone Investors were allocated further Offer Shares as placees in the International Offering.
Please refer to the section headed “Allotment Results Details — International Offering — Allottees
with Waivers/Consents Obtained” in this announcement for details. Only the Offer Shares subscribed
for as Cornerstone Investors are subject to lock-up as indicated below. For details, please refer to the
section headed “Lock-up Undertakings — Cornerstone Investors” in this announcement.
3.
The number of total issued H Shares immediately after the Global Offering is the same as the number
of Offer Shares to be issued under the Global Offering.
4.
The calculation is based on (i) 616,069,636 A Shares in issue (including 3,001,917 treasury shares as
of the Latest Practicable Date); and (ii) 68,118,700 H Shares.
– 5 –

<<<PAGE 6>>>
Allottees with Waivers/Consents Obtained
Investor
No. of Offer
Shares allocated
Approximate %
of total issued H
Shares after the
Global
OfferingNote 3
Approximate %
of total issued
share capital in
the Company
after the Global
OfferingNote 4
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by Permitted Existing
Shareholders holding more than 1% of the issued share capital of the Company immediately prior to the
completion of the Global Offering and/or their close associatesNote 1
Nil
Nil
Nil
Nil
Nil
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in
relation to allocations of further H Shares to existing Shareholders and Cornerstone Investors and/or their
close associatesNote 2
CNCB Investment
2,138,700
3.14%
0.31%
A Cornerstone
Investor
Golden Valley Master
1,782,200
2.62%
0.26%
A Cornerstone
Investor
Goldshore
891,100
1.31%
0.13%
A Cornerstone
Investor
Happy Wisdom
2,723,300
4.00%
0.40%
A Cornerstone
Investor and a close
associate of existing
Shareholder
Zhou Bo
712,900
1.05%
0.10%
A Cornerstone
Investor and an
existing Shareholder
– 6 –

<<<PAGE 7>>>
Notes:
1.
The Stock Exchange has granted a waiver from strict compliance with the requirements under Rule
10.04 of the Listing Rules and consent under Paragraph 1C(2) of the Placing Guidelines to permit H
Shares in the International Offering to be placed to certain Permitted Existing Shareholders. Please
refer to the section headed “Waivers from Strict Compliance with the Listing Rules — Allocation of
H Shares to Existing Minority Shareholders and Their Close Associates” in the Prospectus for
details. To the best knowledge, information and belief of the Company after due enquiry, none of the
allottees who are Permitted Existing Shareholders holds more than 1% of the issued share capital of
the Company immediately prior to the completion of the Global Offering.
2.
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents
the number of Offer Shares allocated to the investors as placees in the International Offering. For
allocations of Offer Shares to the relevant investors as Cornerstone Investors, please refer to the
section headed “Allotment Results Details — International Offering — Cornerstone Investors” in this
announcement. For details of the consent under Chapter 4.15 of the Guide for New Listing Applicants
in relation to allocations of further H Shares to the Cornerstone Investors, please refer to the section
headed “Others/Additional Information — Allocations of Offer Shares to the existing Shareholders
and Cornerstone Investors and/or their close associates as placees with a consent under Chapter 4.15
of the Guide for New Listing Applicants” in this announcement.
3.
The number of total issued H Shares immediately after the Global Offering is the same as the number
of Offer Shares to be issued under the Global Offering.
4.
The calculation is based on (i) 616,069,636 A Shares in issue (including 3,001,917 treasury shares as
of the Latest Practicable Date); and (ii) 68,118,700 H Shares.
– 7 –

<<<PAGE 8>>>
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
No. of Shares held in
the Company subject
to lock-up
undertakings upon
Listing
Approximate % of
total issued share
capital in the
Company subject to
lock-up undertakings
upon ListingNote 4
Last day subject to the
lock-up undertakings
Ms. ZhangNote 1
375,570,200
54.89%
March 28, 2027
(First Six-Month
Period)Note 2
September 28, 2027
(Second Six-Month
Period)Note 3
Red Avenue InvestmentNote 1
294,570,000
43.05%
March 28, 2027
(First Six-Month
Period)Note 2
September 28, 2027
(Second Six-Month
Period)Note 3
Virgin HoldingsNote 1
80,162,700
11.72%
March 28, 2027
(First Six-Month
Period)Note 2
September 28, 2027
(Second Six-Month
Period)Note 3
Notes:
1.
As of the Latest Practicable Date, (i) Ms. Zhang is the legal and beneficial owner of 837,500 Shares;
(ii) Red Avenue Investment, which beneficially owns 294,570,000 Shares, is wholly owned by Ms.
Zhang; and (iii) Virgin Holdings, which beneficially owns 80,162,700 Shares, is owned as to 99.9%
by Ms. Zhang and 0.1% by Red Avenue Investment. By virtue of the SFO, Ms. Zhang is deemed to be
interested in the Shares held by Red Avenue Investment and Virgin Holdings. For further details,
please refer to “Relationship with Our Controlling Shareholders” in the Prospectus.
2.
The Controlling Shareholders may dispose of or transfer such Shares after the indicated date subject
to that the Controlling Shareholders will not cease to be a controlling shareholder (as defined in the
Listing Rules) of the Company.
3.
The Controlling Shareholders will cease to be prohibited from disposing of or transferring such Shares
after the indicated date.
4.
The calculation is based on (i) 616,069,636 A Shares in issue (including 3,001,917 treasury shares as
of the Latest Practicable Date); and (ii) 68,118,700 H Shares.
– 8 –

<<<PAGE 9>>>
Cornerstone Investors
Name
No. of H Shares
held in the
Company subject
to lock-up
undertakings upon
Listing
Approximate %
of total issued
H Shares after
the Global
Offering subject
to lock-up
undertakings upon
ListingNote 1
Approximate %
of total issued
share capital in
the Company
subject to
lock-up
undertakings upon
ListingNote 3
Last day subject
to the lock-up
undertakingsNote 2
CNCB Investment
3,208,100
4.7%
0.5%
March 28, 2027
Full Truck
3,564,500
5.2%
0.5%
March 28, 2027
Golden Valley Master
1,782,200
2.6%
0.3%
March 28, 2027
Goldshore
8,028,400
11.8%
1.2%
March 28, 2027
Happy Wisdom
2,676,100
3.9%
0.4%
March 28, 2027
Prinx Chengshan HK
1,000,000
1.5%
0.2%
March 28, 2027
Yang Quanhai
891,100
1.3%
0.1%
March 28, 2027
Zhou Bo
1,427,200
2.1%
0.2%
March 28, 2027
Total
22,577,600
33.1%
3.3%
Notes:
1.
The number of total issued H Shares immediately after the Global Offering is the same as the number
of Offer Shares to be issued under the Global Offering.
2.
In accordance with the relevant Cornerstone Investment Agreements, the required lock-up period
commences from (and inclusive of) the Listing Date and ending on (and inclusive of) the date falling
six (6) months after the Listing Date (being March 28, 2027). The Cornerstone Investors will cease
to be prohibited from disposing of or transferring H Shares subscribed pursuant to the relevant
Cornerstone Investment Agreements after the indicated date.
3.
The calculation is based on (i) 616,069,636 A Shares in issue (including 3,001,917 treasury shares as
of the Latest Practicable Date); and (ii) 68,118,700 H Shares.
– 9 –

<<<PAGE 10>>>
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of
H Shares allotted
Allotment as %
of International
Offering
Allotment as %
of total
Offer Shares
Number of
H Shares held
upon Listing
% of total issued
share capital
upon Listing#
Top 1
8,919,500
14.55%
13.09%
8,919,500
1.30%
Top 5
27,685,900
45.16%
40.64%
27,685,900
4.05%
Top 10
41,943,900
68.42%
61.57%
41,943,900
6.13%
Top 25
58,165,300
94.88%
85.39%
58,165,300
8.50%
Note:
*
Ranking of placees is based on the number of H Shares allotted to the placees.
#
The calculation is based on (i) 616,069,636 A Shares in issue (including 3,001,917 treasury shares as of
the Latest Practicable Date); and (ii) 68,118,700 H Shares.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number of
H Shares allotted
Allotment as %
of International
Offering
Allotment as %
of total
Offer Shares
Number of
H Shares held
upon Listing
% of total issued
share capital
upon Listing#
Top 1
8,919,500
14.55%
13.09%
8,919,500
1.30%
Top 5
27,685,900
45.16%
40.64%
27,685,900
4.05%
Top 10
41,943,900
68.42%
61.57%
41,943,900
6.13%
Top 25
58,165,300
94.88%
85.39%
58,165,300
8.50%
Note:
*
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
#
The calculation is based on (i) 616,069,636 A Shares in issue (including 3,001,917 treasury shares as of
the Latest Practicable Date); and (ii) 68,118,700 H Shares.
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders*
Number of
H Shares allotted
Allotment as %
of International
Offering
Allotment as %
of total
Offer Shares
Number of
H Shares held
upon Listing
Number of
Shares held
upon Listing#
% of total issued
share capital
upon Listing†
Top 1
0
0.00%
0.00%
0
375,570,200
54.89%
Top 5
8,919,500
14.55%
13.09%
8,919,500
424,853,818
62.10%
Top 10
27,687,600
45.16%
40.65%
27,687,600
449,992,119
65.77%
Top 25
51,571,100
84.12%
75.71%
51,571,100
484,649,933
70.84%
Notes:
*
Ranking of Shareholders is based on the number of Shares held by all Shareholders upon Listing.
#
Among the top 25 placees, certain placees are also existing Shareholders and/or their close associates. To
the best knowledge, information and belief of the Company after due enquiry, none of the allottees who are
Permitted Existing Shareholders holds more than 1% of the issued share capital of the Company
immediately prior to the completion of the Global Offering.
†
The calculation is based on (i) 616,069,636 A Shares in issue (including 3,001,917 treasury shares as of
the Latest Practicable Date); and (ii) 68,118,700 H Shares.
– 10 –

<<<PAGE 11>>>
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications
made by the public will be conditionally allocated on the basis set out below:
Number of
H Shares
applied for
Number of
valid
applications
Basis of allocation/ballot
Approximate percentage
allotted of the
total number of
H Shares applied for
Pool A
100
6,664
100 H Shares
100.00%
200
1,906
100 H Shares plus 948 out of 1,906 applicants to receive
an additional 100 H Shares
74.87%
300
571
100 H Shares plus 512 out of 571 applicants to receive
an additional 100 H Shares
63.22%
400
283
200 H Shares plus 69 out of 283 applicants to receive an
additional 100 H Shares
56.10%
500
552
200 H Shares plus 305 out of 552 applicants to receive
an additional 100 H Shares
51.05%
600
148
200 H Shares plus 124 out of 148 applicants to receive
an additional 100 H Shares
47.30%
700
85
300 H Shares plus 9 out of 85 applicants to receive an
additional 100 H Shares
44.37%
800
108
300 H Shares plus 39 out of 108 applicants to receive an
additional 100 H Shares
42.01%
900
68
300 H Shares plus 41 out of 68 applicants to receive an
additional 100 H Shares
40.03%
1,000
763
300 H Shares plus 625 out of 763 applicants to receive
an additional 100 H Shares
38.19%
1,500
201
400 H Shares plus 168 out of 201 applicants to receive
an additional 100 H Shares
32.24%
2,000
286
500 H Shares plus 206 out of 286 applicants to receive
an additional 100 H Shares
28.60%
2,500
123
600 H Shares plus 63 out of 123 applicants to receive an
additional 100 H Shares
26.05%
3,000
119
700 H Shares plus 29 out of 119 applicants to receive an
additional 100 H Shares
24.15%
3,500
43
700 H Shares plus 40 out of 43 applicants to receive an
additional 100 H Shares
22.66%
4,000
53
800 H Shares plus 30 out of 53 applicants to receive an
additional 100 H Shares
21.42%
4,500
46
900 H Shares plus 8 out of 46 applicants to receive an
additional 100 H Shares
20.39%
5,000
116
900 H Shares plus 87 out of 116 applicants to receive an
additional 100 H Shares
19.50%
6,000
40
1,000 H Shares plus 34 out of 40 applicants to receive an
additional 100 H Shares
18.08%
– 11 –

<<<PAGE 12>>>
Number of
H Shares
applied for
Number of
valid
applications
Basis of allocation/ballot
Approximate percentage
allotted of the
total number of
H Shares applied for
7,000
35
1,100 H Shares plus 30 out of 35 applicants to receive an
additional 100 H Shares
16.94%
8,000
28
1,200 H Shares plus 23 out of 28 applicants to receive an
additional 100 H Shares
16.03%
9,000
27
1,300 H Shares plus 20 out of 27 applicants to receive an
additional 100 H Shares
15.27%
10,000
165
1,400 H Shares plus 97 out of 165 applicants to receive
an additional 100 H Shares
14.59%
20,000
60
2,100 H Shares plus 50 out of 60 applicants to receive an
additional 100 H Shares
10.92%
30,000
41
2,700 H Shares plus 27 out of 41 applicants to receive an
additional 100 H Shares
9.22%
40,000
13
3,200 H Shares plus 9 out of 13 applicants to receive an
additional 100 H Shares
8.17%
50,000
19
3,700 H Shares plus 5 out of 19 applicants to receive an
additional 100 H Shares
7.45%
60,000
6
4,100 H Shares plus 3 out of 6 applicants to receive an
additional 100 H Shares
6.92%
70,000
7
4,500 H Shares plus 2 out of 7 applicants to receive an
additional 100 H Shares
6.47%
80,000
5
4,900 H Shares
6.13%
90,000
4
5,200 H Shares plus 2 out of 4 applicants to receive an
additional 100 H Shares
5.83%
100,000
36
5,500 H Shares plus 26 out of 36 applicants to receive an
additional 100 H Shares
5.57%
Total
12,621
Total number of Pool A successful applicants: 12,621
Number of
H Shares
applied for
Number of
valid
applications
Basis of allocation/ballot
Approximate percentage
allotted of the
total number of
H Shares applied for
Pool B
200,000
18
113,500 H Shares plus 10 out of 18 applicants to receive
an additional 100 H Shares
56.78%
300,000
2
170,300 H Shares
56.77%
400,000
3
227,000 H Shares
56.75%
600,000
1
340,300 H Shares
56.72%
Total
24
Total number of Pool B successful applicants: 24
– 12 –

<<<PAGE 13>>>
As of the date of this announcement, the relevant subscription monies previously deposited
in the designated nominee accounts have been remitted back to the accounts of all HKSCC
participants. Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in
respect of which consent has been obtained, the Company has complied with the Listing
Rules and guidance materials in relation to the placing, allotment and listing of the
Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the
placees or the public (as the case may be) directly or indirectly for each Offer Share
subscribed for or purchased by them was the same as the final Offer Price in addition to
any brokerage, AFRC transaction levy, SFC transaction levy and Stock Exchange
trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Allocations of Offer Shares to Permitted Existing Shareholders and/or their close
associates
The Company has applied for, and the Stock Exchange has granted, a waiver from strict
compliance with Rule 10.04 of, and a consent under paragraph 1C(2) of Appendix F1 to,
the Listing Rules to permit H Shares in the International Offering to be placed to certain
existing minority Shareholders who (i) hold less than 5% voting rights of the Company
prior to the completion of the Global Offering and (ii) are not and will not become (upon
the completion of the Global Offering) core connected persons of the Company or the
close associates of any such core connected persons (together, the “Permitted Existing
Shareholders”) and/or their close associates, subject to, among others, the following
conditions:
(a) each of the Permitted Existing Shareholders to whom the Company may allocate H
Shares under the International Offering holds less than 5% voting rights in the
Company prior to the completion of the Global Offering;
(b) each of the Permitted Existing Shareholders is not, and will not be, a core connected
person of the Company or any close associate of any such core connected person
immediately prior to or following the Global Offering;
(c)
none of the Permitted Existing Shareholders has the right to appoint any Directors
nor have any other special rights in the Company;
(d) allocation to the Permitted Existing Shareholders or their close associates will not
affect the Company’s ability to satisfy the public float requirement under Rule
8.08(1) (as amended and replaced by Rule 19A.13A(2)) of the Listing Rules;
– 13 –

<<<PAGE 14>>>
(e)
the Company providing a confirmation that:
(i)
in the case of participation as cornerstone investors, no preferential treatment
has been, nor will be, given to the Permitted Existing Shareholders or their close
associates by virtue of their relationship with the Company other than the
preferential treatment of assured entitlement under cornerstone investments
following the principles set out in Chapter 4.15 of the Guide for New Listing
Applicants, that the Permitted Existing Shareholders or their close associates’
cornerstone investment agreements do not contain any material terms which are
more favorable to the Permitted Existing Shareholders or their close associates
than those in other cornerstone investment agreements; and
(ii) in the case of participation as placees, no preferential treatment has been, nor
will be, given to the Permitted Existing Shareholders or their close associates by
virtue of their relationship with the Company in any allocation in the placing
tranche; and
(f)
in the case of participation as placees, the Overall Coordinators providing a
confirmation to the Stock Exchange that, to the best of its knowledge and belief, no
preferential treatment has been, nor will be, given to any of the Permitted Existing
Shareholders or their close associates by virtue of their relationship with the
Company in any allocation in the placing tranche; and
(g) the Sole Sponsor providing a confirmation to the Stock Exchange that based on (i)
their discussions with the Company and the Overall Coordinators; and (ii) the
confirmations provided to the Stock Exchange by the Company and the Overall
Coordinators, and to the best of its knowledge and belief, it has no reason to believe
that any of the Permitted Existing Shareholders or their close associates received any
preferential treatment or is in a position to exert influence on the Company to obtain
actual or perceived preferential treatment in the allocation either as a cornerstone
investor or as a placee by virtue of their relationship with the Company other than
the preferential treatment of assured entitlement under a cornerstone investment
following the principles set out in Chapter 4.15 of the Guide for New Listing
Applicants, and details of allocation to the Permitted Existing Shareholders holding
more than 1% of the total number of issued Shares immediately prior to the
completion of the Global Offering will be disclosed in the Prospectus and/or this
allotment results announcement, as the case may be.
Please refer to the section headed “Waivers from Strict Compliance with the Listing
Rules — Allocation of H Shares to Existing Minority Shareholders and Their Close
Associates” in the Prospectus for further details of the waiver and consent.
Each of the Sole Sponsor, the Overall Coordinators and the Company has provided the
required confirmations as elaborated above.
– 14 –

<<<PAGE 15>>>
Allocations of Offer Shares to the existing Shareholders and Cornerstone Investors and/or
their close associates as placees with a consent under Chapter 4.15 of the Guide for New
Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under
Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to allocate
further Offer Shares in the International Offering to certain existing Shareholders and
Cornerstone
Investors
and/or
their
close
associates
(the
“Size-based
Exemption
Participants”)
as
placees,
subject
to
the
following
conditions
(the
“Size-based
Exemption”):
(a) the final offering size of the Global Offering will be of a total value of at least HK$1
billion;
(b) the Offer Shares allocated to all existing Shareholders (whether as cornerstone
investors and/or as placees) as permitted under the size-based exemption do not
exceed 30% of the total number of the Offer Shares;
(c)
each director, chief executive and Controlling Shareholders of the Company has
confirmed that no Offer Shares have been allocated to them or their respective close
associates pursuant to the size-based exemption;
(d) the allocation to the
Size-based Exemption Participants will not affect the
Company’s ability to satisfy the public float requirement under Rule 19A.13A(2)
of the Listing Rules; and
(e)
details of the allocation to the relevant Size-based Exemption Participants under the
size-based exemption will be disclosed in the allotment results announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the
consent granted by the Stock Exchange. For details of the allocation to Size-based
Exemption Participants, please refer to the section headed “Allotment Results Details —
International
Offering
—
Allottees
with
Waivers/Consents
Obtained”
in
this
announcement.
– 15 –

<<<PAGE 16>>>
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong
Limited and Hong Kong Securities Clearing Company Limited take no responsibility for
the contents of this announcement, make no representation as to its accuracy or
completeness and expressly disclaim any liability whatsoever for any loss howsoever
arising from or in reliance upon the whole or any part of the contents of this
announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or
into the United States (including its territories and possessions, any state of the United
States and the District of Columbia). This announcement does not constitute or form a
part of any offer or solicitation to purchase or subscribe for the Offer Shares in the United
States or in any other jurisdictions. The Offer Shares have not been, and will not be,
registered under the United States Securities Act of 1933 as amended from time to time
(the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the
United States. The Offer Shares may not be offered, sold, pledged or otherwise
transferred within the United States, except pursuant to an exemption from the
registration requirements of the U.S. Securities Act and U.S. Investment Company Act
of 1940, as amended (“U.S. Investment Company Act”), and in compliance with any
applicable state securities laws. There will be no public offer of the Offer Shares in the
United States.
The Offer Shares are being offered and sold outside the United States to investors that are
not U.S. persons nor persons acquiring for the account or benefit of U.S. persons in
reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation
or offer to acquire, purchase or subscribe for securities. This announcement is not a
prospectus. Potential investors should read the Prospectus dated September 21, 2026
issued by Red Avenue New Materials Group Co., Ltd. (彤程新材料集團股份有限公司)
for detailed information about the Global Offering described below before deciding
whether or not to invest in the H Shares thereby being offered.
*
Potential investors of the Offer Shares should note that the Sole Sponsor and the
Sponsor-Overall
Coordinator
(for
itself
and
on
behalf
of
the
Hong
Kong
Underwriters) shall be entitled to terminate their obligations under the Hong Kong
Underwriting Agreement with immediate effect upon the occurrence of any of the
events set out in the section headed “Underwriting — Underwriting Arrangements and
Expenses — Hong Kong Public Offering — Hong Kong Underwriting Agreement —
Grounds for Termination” in the Prospectus at any time prior to 8: 00 a.m. (Hong
Kong time) on the Listing Date (which is currently expected to be on September 29,
2026).
– 16 –

<<<PAGE 17>>>
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, the total number of the H
Shares expected to be held by the public represents approximately 10.0% of the total
issued share capital of our Company (excluding treasury shares), which is higher than the
prescribed percentage of H Shares required to be held in public hands of 10% under Rule
19A.13A(2)(a) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following
the Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing
shall not be counted towards the free float of the H Shares of the Company at the time of
Listing. Based on the final Offer Price of HK$44.00 per H Share, the Company satisfies
the free float requirement under Rule 19A.13C of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering: (i)
the Shares will be held by at least 300 Shareholders at the time of Listing, in compliance
with Rule 8.08(2) of the Listing Rules; (ii) the three largest public Shareholders will not
hold more than 50% of the H Shares held in public hands at the time of Listing, in
compliance with Rules 8.08(3) and 8.24 of the Listing Rules; (iii) no placee will,
individually, be placed more than 10% of the enlarged issued share capital of the
Company immediately after the Global Offering; and (iv) there will not be any new
substantial Shareholder (as defined in the Listing Rules) immediately after the Global
Offering.
– 17 –

<<<PAGE 18>>>
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8: 00 a.m. on Tuesday,
September 29, 2026 (Hong Kong time), provided that the Global Offering has become
unconditional and the right of termination described in the section headed “Underwriting
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds
for Termination” in the Prospectus has not been exercised. Investors who trade the H
Shares on the basis of publicly available allocation details prior to the receipt of H Share
certificates or prior to the H Share certificates becoming valid evidence of title do so
entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8: 00 a.m. on
Tuesday, September 29, 2026 (Hong Kong time), it is expected that dealings in the H
Shares on the Stock Exchange will commence at 9: 00 a.m. on Tuesday, September 29,
2026 (Hong Kong time). The H Shares will be traded in board lots of 100 H Shares each,
and the stock code of the H Shares will be 9607.
By order of the Board
Red Avenue New Materials Group Co., Ltd.
Zhang Ning
Chairperson of the Board and Executive Director
Hong Kong, September 28, 2026
As of the date of this announcement, the Board comprises (i) Ms. Zhang Ning, Mr. Ding
Lin, Mr. Yuan Minjian, Mr. Yu Yaoming and Mr. Tang Jie as executive Directors; (ii)
Mr. Li Xiaoguang as non-executive Director; and (iii) Mr. Zhang Yun, Mr. Jiang
Changjian, Mr. Feng Yaoling and Mr. Chan Chi Fung Leo as independent non-executive
Directors.
– 18 –
