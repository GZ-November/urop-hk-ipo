# 配发结果公告抽取任务：6067.HK Shenzhen Senior Technology Material Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**22/06/2026 22:58**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0622/2026062202141.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6067.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined herein, capitalized terms used in this announcement shall have the
same meanings as those defined in the prospectus dated 12 June 2026 (the “Prospectus”)
issued by Shenzhen Senior Technology Material Co., Ltd. (深圳市星源材質科技股份有限
公司) (the “Company”).
This announcement is for information purposes only and does not constitute an offer or an
invitation to induce an offer by any person to acquire, purchase or subscribe for any
securities of the Company. This announcement is not a prospectus. Potential investors
should read the Prospectus for detailed information about the Company and the Global
Offering described below before deciding whether or not to invest in the Offer Shares. Any
investment decision in relation to the Offer Shares should be taken solely in reliance on the
information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or
into the United States (including its territories and possessions, any state of the United
States and the District of Columbia). This announcement does not, and is not intended to,
constitute or form a part of any offer to sell or solicitation to purchase or subscribe for any
securities in the United States or in any other jurisdiction. The Offer Shares have not been,
and will not be, registered under the United States Securities Act of 1933, as amended from
time to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction
of the United States and may not be offered, sold, pledged or otherwise transferred within
the United States, except pursuant to an available exemption from, or in a transaction not
subject to, the registration requirements of the U.S. Securities Act and in compliance with
any applicable state securities laws. The Offer Shares are being offered and sold solely
outside the United States in offshore transactions in reliance on Regulation S under the U.S.
Securities Act. There will be no public offer of the Offer Shares in the United States.
Potential investors of the Offer Shares should note that the Sole Sponsor and the
Sponsor-OC (for itself and on behalf of the other Hong Kong Underwriters) shall be
entitled to terminate their obligations under the Hong Kong Underwriting Agreement with
immediate effect upon the occurrence of any of the events set out in the paragraph headed
“Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering
— Hong Kong Underwriting Agreement — Grounds for Termination” in the Prospectus at
any time prior to 8: 00 a.m. (Hong Kong time) on the Listing Date (which is currently
expected to be on Tuesday, 23 June 2026).
– 1 –

<<<PAGE 2>>>
Shenzhen Senior Technology Material Co., Ltd.
深圳市星源材質科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the
Global Offering
:
149,523,500 H Shares
Number of Hong Kong Offer Shares
:
14,952,500 H Shares
Number of International Offer Shares
:
134,571,000 H Shares
Final Offer Price
:
HK$8.98 per Offer Share, plus brokerage
of 1.0%, SFC transaction levy of
0.0027%, Stock Exchange trading fee of
0.00565%, and AFRC transaction levy of
0.00015%
Nominal Value
:
RMB1.00 per Share
Stock Code
:
6067
Sole Sponsor, Sponsor-Overall Coordinator, Joint Global Coordinator,
Joint Bookrunner and Joint Lead Manager
Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers
– 2 –

<<<PAGE 3>>>
SHENZHEN SENIOR TECHNOLOGY MATERIAL CO., LTD.
深圳市星源材質科技股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the
same meanings as those defined in the Prospectus issued by the Company.
SUMMARY
Company information
Stock code
6067
Stock short name
SENIOR MATERIAL
Dealings commencement date
23 June 2026*
*
see note at the end of the announcement
Price Information
Final Offer Price
HK$8.98
Maximum Offer Price
HK$8.98
Offer Shares and Share Capital
Number of Offer Shares
149,523,500 H Shares
Final Number of Offer Shares in Hong Kong Public
Offering
14,952,500 H Shares
Final Number of Offer Shares in International
Offering
134,571,000 H Shares
Number of issued shares upon Listing
1,495,234,139
Proceeds
Gross proceeds (Note)
HK$1,342.7 million
Less: Estimated listing expenses payable based on
Final Offer Price
HK$61.7 million
Net proceeds
HK$1,281.0 million
Note: Gross proceeds refers to the amount to which the issuer is entitled receive. For details of the use of
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” in the Prospectus.
– 3 –

<<<PAGE 4>>>
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
209,580
No. of successful applications
22,263
Subscription level
1,563.16 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong
Public Offering
14,952,500
No. of Offer Shares reallocated from the International Offering
0
Final no. of Offer Shares under the Hong Kong Public Offering
14,952,500
% of Offer Shares under the Hong Kong Public Offering to the
Global Offering
10%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can refer to
www.eipo.com.hk/eIPOAllotment
to
perform
a
search
by
identification
number
or
www.eipo.com.hk/eIPOAllotment for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
104
Subscription Level
14.34 times
No. of Offer Shares initially available under the International
Offering
134,571,000
No. of Offer Shares reallocated to the Hong Kong Public Offering
0
Final no. of Offer Shares under the International Offering
134,571,000
% of Offer Shares under the International Offering to the Global
Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for
(a) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent
under paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”)
granted by the Stock Exchange to permit H Shares in the International Offering to be
placed to certain Permitted Existing Shareholders, (b) a consent under paragraph 18 of
Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to, among
other things, allocate further H Shares in the International Offering to certain minority
existing shareholders and/or their close associates and certain Cornerstone Investors and
their close associates as disclosed in this announcement, and (c) a consent under paragraph
1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide to New Listing Applicants
(the “Guide”) granted by the Stock Exchange to permit H Shares in the International
Offering to be placed to certain connected clients as disclosed in this announcement, (i)
none of the Offer Shares subscribed by the placees and the public have been financed
directly or indirectly by the Company, any of the Directors, chief executive of the Company,
substantial shareholders, existing shareholders of the Company or any of its subsidiaries or
– 4 –

<<<PAGE 5>>>
their respective close associates; and (ii) none of the placees and the public who have
purchased the Offer Shares are accustomed to taking instructions from the Company, any of
the
Directors,
chief
executive
of
the
Company,
substantial
shareholders,
existing
shareholders of the Company or any of its subsidiaries or their respective close associates
in relation to the acquisition, disposal, voting or other disposition of H Shares registered in
his/her/its name or otherwise held by him/her/it.
The placees in the International Offer include the following:
Cornerstone Investors (Note 1)
Name
No. of Offer
Shares
allocated
% of Offer
Shares
% of total
issued H
Shares after
the Global
Offering
% of total
issued Shares
after the
Global
Offering
(Note 3)
Existing
shareholders
or their close
associates
Fullgoal Fund
Management Co., Ltd.
(“Fullgoal”)
6,720,500
4.49%
4.49%
0.45%
Yes
GF Fund Management
Co., Ltd. and GF
International Investment
Management Limited
(together, “GF Fund”)
(Note 2)
5,673,000
3.79%
3.79%
0.38%
Yes
TAIKANG LIFE
INSURANCE CO., LTD
(“Taikang Life”)
(Note 2)
5,673,000
3.79%
3.79%
0.38%
Yes
HARVEST
INTERNATIONAL
PREMIUM VALUE
(SECONDARY
MARKET) FUND SPC
acting on behalf of and
for HARVEST
SYNERGY SP (“Harvest
Synergy”) (Note 2)
4,922,500
3.29%
3.29%
0.33%
No
SPRINGS CAPITAL
(HONG KONG)
LIMITED (“Springs
Capital”)
5,567,500
3.72%
3.72%
0.37%
No
– 5 –

<<<PAGE 6>>>
Name
No. of Offer
Shares
allocated
% of Offer
Shares
% of total
issued H
Shares after
the Global
Offering
% of total
issued Shares
after the
Global
Offering
(Note 3)
Existing
shareholders
or their close
associates
Gaoteng Enterprise
Management Co., Ltd.
(“Gaoteng Enterprise
Management”) and
CICC FINANCIAL
TRADING LIMITED
(“CICC FT”) (in
connection with OTC
Swaps) (Notes 2 and 4)
2,618,000
1.75%
1.75%
0.18%
No
Sunwoda Treasury
(Hong Kong) Limited
(“Sunwoda Treasury”)
2,560,000
1.71%
1.71%
0.17%
No
JINKOSOLAR
INVESTMENT
LIMITED (“Jinkosolar”)
4,454,000
2.98%
2.98%
0.30%
No
Mondeomax Limited
(“Mondeomax”)
11,024,500
7.37%
7.37%
0.74%
No
Bona Star Consultant
Limited (“Bona Star”)
(Note 2)
8,351,500
5.59%
5.59%
0.56%
No
SINSANWA
HOLDINGS (H.K.)
CO., LIMITED
(“Sinsanwa”)
5,567,500
3.72%
3.72%
0.37%
No
SHEEN NATION
HOLDINGS LIMITED
(“Sheen Nation”)
2,618,000
1.75%
1.75%
0.18%
No
Chen Feng
1,745,500
1.17%
1.17%
0.12%
No
Total
67,495,500
45.14%
45.14%
4.51%
Notes:
1.
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone
Investors” in the Prospectus.
– 6 –

<<<PAGE 7>>>
2.
In addition to the Offer Shares subscribed for as Cornerstone Investors, GF Fund, Taikang Life,
Harvest Synergy, Bona Star, Gaoteng Enterprise Management, Fullgoal, Chen Feng and Sheen
Nation and/or their respective close associates, where applicable, were allocated further Offer Shares
as placees in the International Offering. Please refer to the section headed “Allotment Results Details
— International Offering — Allotees with waivers/consents obtained” in this announcement for
details. Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-up as
indicated below. For details, please refer to the section headed “Lock-up Undertakings —
Cornerstone Investors” in this announcement.
3.
Not taking into account any A Shares held by the relevant investors and including the 19,855,640 A
Shares being held as treasury shares as at the date of this announcement.
4.
CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the OTC Swaps (as defined
in the Prospectus), while the economic risks and returns of the underlying Offer Shares are passed to
the CICC FT Ultimate Client, i.e. Gaoteng Enterprise Management. Gortune Investment Co., Ltd.
(廣東民營投資股份有限公司) (“Gortune Investment”) is the controlling shareholder of Gaoteng
Enterprise Management, holding 99.94% of its issued shares. To the best of CICC FT’s knowledge
having made all reasonable inquiries, the CICC FT Ultimate Client is an independent third party of
CICC FT, CICCHKS and the companies which are members of the same group of CICCHKS, and
there is no single shareholder who holds more 30% or more interests in Gortune Investment. For
details, please refer to the section headed “Cornerstone Investors” of the Prospectus.
Allotees with waivers/consents obtained
Name
No. of Offer
Shares allocated
% of Offer
Shares
% of total
issued H Shares
after the Global
Offering
% of total
issued Shares
after the Global
Offering (Note
4)
Relationship
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the
Placing Guidelines in relation to subscription for H Shares by Permitted Existing Shareholders holding more than 1% of the
issued share capital of the Company immediately prior to the completion of the Global Offering and/or their close associates
(Note 1)
Fullgoal
7,349,000
4.91%
4.91%
0.49%
Fullgoal also manages
other fund products,
each holding less than
1% of the issued share
capital but in aggregate
holding more than 1%
of the issued share
capital of the Company
Fullgoal Asset
Management (HK)
Limited
206,500
0.14%
0.14%
0.01%
Fullgoal Asset
Management (HK)
Limited is
wholly-owned by
Fullgoal
– 7 –

<<<PAGE 8>>>
Name
No. of Offer
Shares allocated
% of Offer
Shares
% of total
issued H Shares
after the Global
Offering
% of total
issued Shares
after the Global
Offering (Note
4)
Relationship
Allotees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of
further H Shares to existing shareholders and Cornerstone Investors and/or their close associates (Note 2)
GF Fund
1,112,000
0.74%
0.74%
0.07%
Cornerstone Investor
Taikang Life
724,000
0.48%
0.48%
0.05%
Cornerstone Investor
Harvest Global
Capital Investments
Limited
1,782,000
1.19%
1.19%
0.12%
The fund manager of a
Cornerstone Investor,
namely Harvest Synergy
SP
Bona Star
4,409,000
2.95%
2.95%
0.29%
Cornerstone Investor
SEA2SEA
International Pte Ltd
3,087,000
2.06%
2.06%
0.21%
Wholly-owned by the
spouse of the sole
shareholder of, and
thus a close associate
of, a Cornerstone
Investor, namely Bona
Star
Yuemintou New
Opportunity No. 1
Private Securities
Investment Fund and
SHENWAN
HONGYUAN
(INTERNATIONAL)
HOLDINGS
LIMITED (in
connection with OTC
Swaps)
110,000
0.07%
0.07%
0.01%
A fund managed by
Yuemin Investment
Private Securities Fund
Management
(Shenzhen) Company
Limited (“Yuemin
Investment”). Yuemin
Investment is the GP
Of Yuemintou Private
Securities Management
Co., Ltd, which shares
the same controlling
shareholder as a
Cornerstone Investor,
namely Gaoteng
Enterprise Management
Fullgoal
628,500
0.42%
0.42%
0.04%
Cornerstone Investor
Fullgoal Asset
Management (HK)
Limited
206,500
0.14%
0.14%
0.01%
Wholly-owned by a
Cornerstone Investor,
namely Fullgoal
Chen Feng
20,000
0.01%
0.01%
0.00%
Cornerstone Investor
ICBCUBSI
2,000
0.00%
0.00%
0.00%
ICBCUBSI shares the
same ultimate beneficial
owner as a cornerstone
investor, namely Sheen
Nation
– 8 –

<<<PAGE 9>>>
Name
No. of Offer
Shares allocated
% of Offer
Shares
% of total
issued H Shares
after the Global
Offering
% of total
issued Shares
after the Global
Offering (Note
4)
Relationship
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide in relation to
allocations to connected clients (Note 3)
CICC FT
(in connection with
the OTC Swaps)
(Note 5)
25,500
0.02%
0.02%
0.00%
CICC FT is a member
of the same group as
China International
Capital Corporation
Hong Kong Securities
Limited (“CICCHKS”)
CICC FT (in
connection the OTC
swaps) (Note 12)
2,618,000
1.75%
1.75%
0.18%
CICC FT is a member
of the same group as
China International
Capital Corporation
Hong Kong Securities
Limited
Huatai Capital
Investment Limited
(“HTCI”) (Note 6)
11,024,000
7.37%
7.37%
0.74%
Huatai Capital
Investment Limited is a
member of the same
group as Huatai
Financial Holdings
(Hong Kong) Limited
(“HTFH”)
China Asset
Management (Hong
Kong) Limited
(“China AMC HK”)
(Note 7)
25,500
0.02%
0.02%
0.00%
China Asset
Management (Hong
Kong) Limited is a
member of the same
group as CITIC
Securities Brokerage
(HK) Limited (a
distributor of the
Global Offering)
(“CSB”)
ICBC UBS Asset
Management Co.,
(International) Ltd.
(“ICBCUBSI”)
(Note 8)
2,000
0.00%
0.00%
0.00%
ICBC UBS Asset
Management Co.,
(International) Ltd. is a
member of the same
group as ICBC
International Securities
Limited (“ICBCI”)
– 9 –

<<<PAGE 10>>>
Name
No. of Offer
Shares allocated
% of Offer
Shares
% of total
issued H Shares
after the Global
Offering
% of total
issued Shares
after the Global
Offering (Note
4)
Relationship
ICBC International
Fund Management
Limited (“ICBC
International”)
(Note 9)
2,000
0.00%
0.00%
0.00%
ICBC International
Fund Management is a
member of the same
group as ICBC
International Securities
Limited
AEGON-Industrial
Fund Management
Co., Ltd.
(“AEGON”)
(Note 10)
9,000
0.01%
0.01%
0.00%
China Industrial
Securities International
Capital Limited
(“CISI”) (a distributor
of the Global Offering)
is the controlling
shareholder of
AEGON-Industrial
Fund Management Co.,
Ltd.
Red South OFC-Red
South Mining
Technology Fund
(“Red South”)
(Note 11)
4,652,000
3.11%
3.11%
0.31%
VHS is wholly-owned
by Vast Harbour
Financial International
Holding Limited, which
holds 25% interest in
Red South
Notes:
1.
Among the Cornerstone Investors, GF Fund, GF International, Fullgoal and Taikang Life are
Permitted Existing Shareholders. The Stock Exchange has granted a waiver from strict compliance
with the requirements under Rule 10.04 of the Listing Rules and consent under Paragraph 1C(2) of
the Placing Guidelines to permit H Shares in the International Offering to be placed to certain
Permitted Existing Shareholders. Please refer to the section headed “Waivers — Allocation of H
Shares to Existing Minority Shareholders and Their Close Associates” of the Prospectus for details.
The Stock Exchange granted the waiver and consent on the condition that, among others, details of
the allocation to the Permitted Existing Shareholders holding more than 1% of the issued share
capital of the Company and/or their close associates immediately prior to the completion of the
Global Offering will be disclosed in the Prospectus and/or allotment results announcement.
2.
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents
the number of Offer Shares allocated to the investors as placees in the International Offering. For
allocations of Offer Shares to the relevant investors as Cornerstone Investors, please refer to the
section headed “Allotment Results Details — International Offering — Cornerstone Investors” in this
announcement. For details of the consent under paragraph 18 of Chapter 4.15 of the Guide for New
Listing Applicants in relation to allocations of further H Shares to the existing Shareholders and
cornerstone
investors
and/or
their
close
associates,
please
refer
to
the
section
headed
“Others/Additional Information — Allocation of Offer Shares to existing Shareholders and
cornerstone investors and/or their close associates with a consent under paragraph 18 of Chapter
4.15 of the Guide for New Listing Applicants” in this announcement.
– 10 –

<<<PAGE 11>>>
3.
For details of the consent under paragraphs 1C(1) of the Placing Guidelines in relation to allocations
to connected clients, please refer to the section headed “Others/Additional Information — Placing to
connected clients with prior consent under paragraph 1C(1) of the Placing Guidelines” in this
announcement.
4.
Not taking into account any A Shares held by the relevant investors.
5.
CICC FT will hold the Offer Shares on a non-discretionary basis for and on behalf the ultimate
clients (the “CICC FT Ultimate Clients”). CICC FT and CICCL will enter into a series of cross border
delta-one OTC swap transactions (collectively, the “OTC Swaps”) with each other and the CICC FT
Ultimate Clients, pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis
to hedge the OTC Swaps while the economic risks and returns of the underlying Offer Shares are
passed to the CICC FT Ultimate Clients, subject to customary fees and commissions. The OTC Swaps
will be fully funded by the CICC FT Ultimate Clients. During the terms of the OTC Swaps, all
economic returns of the Offer Shares subscribed by CICC FT will be passed to the CICC FT Ultimate
Clients and all economic loss shall be borne by the CICC FT Ultimate Clients through the OTC
Swaps, and CICC FT and CICCL will not take part in any economic return or bear any economic loss
in relation to the Offer Shares. The OTC Swaps are linked to the Offer Shares and the CICC FT
Ultimate Clients may request to early terminate the OTC Swaps at their own discretions, upon which
CICC FT may dispose of the Offer Shares and settle the OTC Swaps in cash in accordance with the
terms and conditions of the OTC Swaps. Despite that CICC FT will hold the legal title of the Offer
Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares during the
terms of the OTC Swaps according to its internal policy.
The CICC FT Ultimate Clients for purpose of this placee subscription include (i) Yuanlesheng
Qiangye Private Securities Investment Fund (源樂晟強業私募證券投資基金), whose fund manager is
Tibet Yuanlesheng Asset Management Company Ltd. (“Tibet Longrising”, 西藏源樂晟資產管理有限
公司) and ultimate beneficial owners holding 30% or more interest are Zeng Xiaojie and Hu Caiyang,
(ii) Yuanlesheng Qiangshu Private Securities Investment Fund (源樂晟強樹私募證券投資基金), whose
fund manager is Tibet Longrising and ultimate beneficial owner holding 30% or more interest is Zeng
Xiaojie, (iii) Yuanlesheng Qiangshi Private Securities Investment Fund (源樂晟強勢私募證券投資基
金), whose fund manager is Tibet Longrising and ultimate beneficial owner holding 30% or more
interest is Zeng Xiaojie.
To the best knowledge of CICC FT after due enquiry, each of the CICC FT Ultimate Clients and their
ultimate beneficial owners are independent third parties of the Company, its subsidiaries, CICC FT,
CICCHKS and the companies which are members of the same group as CICC FT and CICCHKS.
6.
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial
public offerings (“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products
issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading
activities. In connection with such products, the licensed domestic securities firms, through their
Hong Kong affiliates, may participate in Hong Kong IPOs either as placees or cornerstone investors
(the “Cross-border Derivatives Trading Regime”).
Huatai Securities Co., Ltd. (“Huatai Securities”), the shares of which are listed on both the Shanghai
Stock Exchange (stock code: 601688) and the Stock Exchange (stock code: 6886), is licensed to
undertake cross-border derivatives trading activities. Huatai Securities has entered into an ISDA
agreement (the “ISDA Agreement”) with its indirectly wholly-owned subsidiary, HTCI, to set out the
principal terms of any future total return swap between Huatai Securities and HTCI.
– 11 –

<<<PAGE 12>>>
Pursuant to the ISDA Agreement, HTCI, which intends to participate as a placee to subscribe for the
Offer Shares under the International Offering (the “Proposed Subscription”), will hold the beneficial
interest of the Offer Shares on a non-discretionary basis as the single underlying holder under a
back-to-back total return swap (the “Back-to-back TRS”) to be entered by HTCI in connection with a
total return swap order (the “Client TRS”) placed by and fully funded (i.e. with no financing provided
by HTCI) by an onshore investor (the “Huatai Ultimate Client”), by which HTCI will, subject to
customary fees and commissions, pass the full economic exposure of the Offer Shares ultimately to the
Huatai Ultimate Client. In effect, HTCI will hold the beneficial interest of the Offer Shares on behalf
of the Huatai Ultimate Client. HTFH and HTCI are indirectly wholly-owned subsidiaries of Huatai
Securities.
Pursuant to the Cross-border Derivatives Trading Regime, the Huatai Ultimate Client cannot directly
subscribe for the Offer Shares but may invest in derivative products issued by domestic securities
firms licenced to undertake cross-border derivatives trading activities, such as Huatai Securities, with
the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, the
Huatai Ultimate Client, through its investment manager, will place the Client TRS with Huatai
Securities in connection with the Company’s IPO and Huatai Securities will place a Back-to-back
TRS order to HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the
Back-to-back TRS, HTCI intends to participate in the Company’s IPO and subscribe to the Offer
Shares through placing an order with HTFH during the International Offering.
The Huatai Ultimate Client for purpose of the Proposed Subscription is Wanli No. 3 Private Equity
Investment Fund (萬利3號私募證券投資基金). To the best of HTCI’s knowledge having made all
reasonable inquiries, the Huatai Ultimate Client is an independent third party of HTCI, HTFH and
the companies which are members of the same group of HTFH.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in
connection with the Client TRS order placed by the Huatai Ultimate Client. Pursuant to the terms of
the contracts of the Back-to-back TRS and the Client TRS, during the tenor of the Back-to-back TRS
and the Client TRS, subject to customary fees and commissions, all economic returns of the Offer
Shares will be ultimately passed to the Huatai Ultimate Client through the Back-to-back TRS and the
Client TRS and all economic loss shall be ultimately borne by the Huatai Ultimate Client. HTCI will
not take any economic return or bear any economic loss in relation to the Offer Shares.
Investment in the Back-to-back TRS and the Client TRS is similar to the investment in a qualified
domestic institutional investor fund (“QDII”) in the way that the Huatai Ultimate Client would reap
all the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through
the exchange rate exposure on both the notional value of the investment and the profit and loss of the
investment. In contrast, the profit and loss of the Back-to-back TRS and the Client TRS factor into
account the fluctuation in RMB exchange rate upon termination of the Client TRS by converting the
profit and loss using the current exchange rate at the time of termination. As such, the Huatai
Ultimate Client would bear the exchange rate exposure of the profit and loss on settlement date.
The Huatai Ultimate Client may, ending on the date which is six months from the Listing Date,
exercise an early termination right to terminate the Client TRS at any time from the issue date of the
Client TRS which should be on or after the date on which the Offer Shares are listed on the Stock
Exchange at its own discretion. Upon the termination upon maturity or early termination of the
Client TRS by the Huatai Ultimate Client, HTCI will dispose the Offer Shares on the secondary
market and the Huatai Ultimate Client will receive a final settlement amount in cash in accordance
with the terms and conditions of the Back-to-back TRS and the Client TRS which should have taken
into account all the economic returns or economic loss in relation to the Offer Shares. If upon the
maturity of the Client TRS, the Huatai Ultimate Client intend to extend the investment period,
subject to further agreement between Huatai Securities and the Huatai Ultimate Client, the term of
the Client TRS could be extended by way of a new issuance or a tenor extension. Accordingly, Huatai
Securities will extend the term of the Back-to-back TRS by way of a new issuance or a tenor extension
– 12 –

<<<PAGE 13>>>
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and
pass through the economic exposure to the Huatai Ultimate Client, being an onshore client who
places a Client TRS order with Huatai Securities in connection with the IPO of the Company. HTCI
will not exercise the voting right of the Offer Shares during the tenor of the Back-to-back TRS.
During the life of the Client TRS and Back-to-back TRS, HTCI may continue to hold the Offer
Shares in its custodian account, or to hold some or all of the Offer Shares in a prime brokerage
account for stock borrowing purposes, where HTCI will lend out its holding of underlying Offer
Shares in the form of stock borrowing loans consistent with market practice to lower its finance costs,
provided that HTCI has the ability to call back the Offer Shares on loan at any time in order to satisfy
its obligations under the Back-to-back TRS to ensure the economic interests are ultimately passed to
the Huatai Ultimate Client.
To the best knowledge of HTCI after due enquiry, the Huatai Ultimate Client and its ultimate
beneficial owner(s) are independent third parties of the Company, its subsidiaries, HTCI, HTFH and
the companies which are members of the same group as HTCI and HTFH.
7.
China AMC HK will hold the Offer Shares in its capacity as the discretionary fund manager
managing assets on behalf of its underlying clients or mandates, which are independent third parties.
To the best knowledge of China AMC HK after due enquiry, each of the underlying clients or
mandates of China AMC HK and their respective ultimate beneficial owner holding 30% or more
interest is an independent third party of China AMC HK and CSB, and the companies which are
members of the same group of companies as CSB.
8.
ICBC UBS will hold the Offer Shares in its capacity as the discretionary fund manager managing the
funds on behalf of a discretionary account, who is an independent third party of ICBC UBS and
ICBCI, and the companies which are members of the same group of companies as ICBCI.
9.
ICBC International will hold the Offer Shares in its capacity as the discretionary fund manager
managing the funds on behalf of a discretionary account, who is an independent third party of ICBC
International and ICBCI, and the companies which are members of the same group of companies as
ICBCI.
10.
AEGON will hold the Offer Shares in its capacity as the discretionary fund manager managing assets
on behalf of its underlying clients or mandates, which are independent third parties. To the best
knowledge of AEGON after due enquiry, each of the underlying clients or mandates of AEGON and
their respective ultimate beneficial owners is an independent third party of AEGON and CISI, and
the companies which are members of the same group of companies as AEGON and CISI.
11.
Red South will hold the Offer Shares in its capacity as the discretionary fund manager managing
assets on behalf of its underlying clients or mandates, which are independent third parties. To the best
knowledge of Red South after due enquiry, each of the underlying clients or mandates of Red South
and their respective ultimate beneficial owners is an independent third party of Red South and VHS,
and the companies which are members of the same group of companies as Red South and VHS.
12.
CICC will hold the Offer Shares on non-discretionary basis on behalf of the ultimate clients (the
“Gaoteng CICC FT Ultimate Client”). CICC FT and CICCL will enter into a series of OTC Swaps
with each other and the Gaoteng CICC FT Ultimate Client, pursuant to which CICC FT will hold the
Offer Shares on a non-discretionary basis to hedge the OTC Swaps while the economic risks and
returns of the underlying Offer Shares are passed to the Gaoteng CICC FT Ultimate Client, subject to
customary fees and commissions. The OTC Swaps will be fully funded by the Gaoteng CICC FT
Ultimate Client. During the terms of the OTC Swaps, all economic returns of the Offer Shares
subscribed by CICC FT will be passed to the Gaoteng CICC FT Ultimate Client and all economic loss
shall be borne by the Gaoteng CICC FT Ultimate Client through the OTC Swaps, and CICC FT will
not take part in any economic return or bear any economic loss in relation to the Offer Shares. The
OTC Swaps are linked to the Offer Shares and the Gaoteng CICC FT Ultimate Client may, after
expiration of the lock-up period beginning from the date of the Cornerstone Investment Agreement
entered into between CICC FT and the Company and ending on the date which is six months from the
– 13 –

<<<PAGE 14>>>
Listing Date, request to early terminate the OTC Swaps at their own discretions, upon which CICC
FT may dispose of the Offer Shares and settle the OTC Swaps in cash in accordance with the terms
and conditions of the OTC Swaps. Despite that CICC FT will hold the legal title of the Offer Shares
by itself, it will not exercise the voting rights attaching to the relevant Offer Shares during the terms
of the OTC Swaps according to its internal policy. To the best of CICC FT’s knowledge having made
all reasonable inquiries, CICC FT Ultimate Client is an independent third party of CICC FT,
CICCHKS and the companies which are members of the same group of CICCHK.
The Gaoteng CICC FT Ultimate Client is Gaoteng Enterprise Management. Gaoteng Enterprise
Management is a joint stock company limited by shares incorporated in Zhuhai, Guangdong, the
PRC, with principal activities comprising investment holding, business management, investment in
self-owned
assets,
economic
and
information
consulting,
and
financial
consulting.
Gorgone
Investment is the controlling shareholder of Gaoteng Enterprise Management, holding 99.94% of
its issued shares. To the best knowledge of CICC FT, there is no single shareholder who holds 30% or
more interests in Gortune Investment.
LOCK-UP UNDERTAKINGS
Cornerstone Investors
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
% of total
issued H
Shares after
the Global
Offering
subject to
lock-up
undertakings
upon listing
% of
shareholding
in the
Company
subject to
lock-up
undertakings
upon listing
Last day subject
to the lock-up
undertakingsNote 1
Fullgoal
6,720,500
6,720,500
4.49%
0.45%
22 December 2026
GF Fund
5,673,000
5,673,000
3.79%
0.38%
22 December 2026
Taikang Life
5,673,000
5,673,000
3.79%
0.38%
22 December 2026
HARVEST
INTERNATIONAL
PREMIUM VALUE
(SECONDARY
MARKET) FUND
SPC acting on
behalf of and for
HARVEST
SYNERGY SP
4,922,500
4,922,500
3.29%
0.33%
22 December 2026
Springs Capital
5,567,500
5,567,500
3.72%
0.37%
22 December 2026
Gaoteng Enterprise
Management and
CICC FT (in
connection with
OTC Swaps)
2,618,000
2,618,000
1.75%
0.18%
22 December 2026
Sunwoda Treasury
2,560,000
2,560,000
1.71%
0.17%
22 December 2026
Jinkosolar
4,454,000
4,454,000
2.98%
0.30%
22 December 2026
Mondeomax
11,024,500
11,024,500
7.37%
0.74%
22 December 2026
– 14 –

<<<PAGE 15>>>
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
% of total
issued H
Shares after
the Global
Offering
subject to
lock-up
undertakings
upon listing
% of
shareholding
in the
Company
subject to
lock-up
undertakings
upon listing
Last day subject
to the lock-up
undertakingsNote 1
Bona Star
8,351,500
8,351,500
5.59%
0.56%
22 December 2026
Sinsanwa
5,567,500
5,567,500
3.72%
0.37%
22 December 2026
Sheen Nation
2,618,000
2,618,000
1.75%
0.18%
22 December 2026
Chen Feng
1,745,500
1,745,500
1.17%
0.12%
22 December 2026
Total
67,495,500
67,495,500
45.14%
4.51%
Note:
1.
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on 22
December 2026. The Cornerstone Investors will cease to be prohibited from disposing of or
transferring H Shares subscribed for pursuant to the relevant cornerstone investment agreements after
the indicated date.
PLACEE CONCENTRATION ANALYSIS
Placees
Number of H
Shares
allotted
Allotment as
% of
International
Offering
Allotment as
% of total
Offer Shares
Number of
H Shares
held upon
Listing
% of total
issued share
capital upon
Listing
Top 1
15,847,500
11.78%
10.60%
15,847,500
1.06%
Top 5
56,542,500
42.02%
37.82%
56,542,500
3.78%
Top 10
89,552,000
66.55%
59.89%
89,552,000
7.23%
Top 25
129,770,000
96.43%
86.79%
129,770,000
9.92%
Notes
*
Ranking of placees is based on the number of H Shares allotted to the placees.
– 15 –

<<<PAGE 16>>>
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number of
H Shares
allotted
Allotment as %
of International
Offering
Allotment as %
of total Offer
Shares
Number of
H Shares held
upon Listing
% of total
issued
H Shares
capital upon
Listing
Number of
Shares held
upon Listing
Top 1
15,847,500
11.78%
10.60%
15,847,500
10.60%
15,847,500
Top 5
56,542,500
42.02%
37.82%
56,542,500
37.82%
56,542,500
Top 10
89,552,000
66.55%
59.89%
89,552,000
59.89%
108,113,590
Top 25
129,770,000
96.43%
86.79%
129,770,000
86.79%
148,331,590
Notes
*
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
Number of H
Shares allotted
Allotment as %
of International
Offering
Allotment as %
of total Offer
Shares
Number of
H Shares held
upon Listing
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
0
170,836,191
11.43%
Top 5
7,555,500
5.61%
5.05%
7,555,500
278,768,440
18.64%
Top 10
34,427,500
25.58%
23.02%
34,427,500
364,185,335
24.36%
Top 25
77,358,000
57.48%
51.74%
77,358,000
492,465,959
32.94%
Notes
*
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon
Listing.
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by the public
will be conditionally allocated on the basis set out below:
NO. OF SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED OF THE
TOTAL NO. OF
SHARES APPLIED
FOR
POOL A
500
75,878
74 out of 75,878 to receive 500 Shares
0.10%
1,000
28,497
55 out of 28,497 to receive 500 Shares
0.10%
1,500
5,421
16 out of 5,421 to receive 500 Shares
0.10%
2,000
3,408
13 out of 3,408 to receive 500 Shares
0.10%
2,500
3,334
16 out of 3,334 to receive 500 Shares
0.10%
3,000
2,608
15 out of 2,608 to receive 500 Shares
0.10%
3,500
1,774
12 out of 1,774 to receive 500 Shares
0.10%
4,000
1,864
15 out of 1,864 to receive 500 Shares
0.10%
4,500
1,343
12 out of 1,343 to receive 500 Shares
0.10%
5,000
18,211
177 out of 18,211 to receive 500 Shares
0.10%
– 16 –

<<<PAGE 17>>>
NO. OF SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED OF THE
TOTAL NO. OF
SHARES APPLIED
FOR
6,000
2,263
26 out of 2,263 to receive 500 Shares
0.10%
7,000
1,454
20 out of 1,454 to receive 500 Shares
0.10%
8,000
1,320
21 out of 1,320 to receive 500 Shares
0.10%
9,000
1,285
22 out of 1,285 to receive 500 Shares
0.10%
10,000
9,725
189 out of 9,725 to receive 500 Shares
0.10%
20,000
5,201
202 out of 5,201 to receive 500 Shares
0.10%
30,000
3,558
207 out of 3,558 to receive 500 Shares
0.10%
40,000
2,952
229 out of 2,952 to receive 500 Shares
0.10%
50,000
3,352
325 out of 3,352 to receive 500 Shares
0.10%
60,000
2,190
255 out of 2,190 to receive 500 Shares
0.10%
70,000
1,806
246 out of 1,806 to receive 500 Shares
0.10%
80,000
1,389
216 out of 1,389 to receive 500 Shares
0.10%
90,000
1,267
221 out of 1,267 to receive 500 Shares
0.10%
100,000
6,531
1,268 out of 6,531 to receive 500 Shares
0.10%
200,000
4,223
1,640 out of 4,223 to receive 500 Shares
0.10%
300,000
2,754
1,605 out of 2,754 to receive 500 Shares
0.10%
400,000
1,909
1,483 out of 1,909 to receive 500 Shares
0.10%
500,000
6,562
6,373 out of 6,562 to receive 500 Shares
0.10%
202,079
Total number of Pool A successful applicants: 14,953
POOL B
1,000,000
4,151
3,960 out of 4,151 to receive 500 Shares
0.05%
1,500,000
940
500 Shares plus 404 out of 940 to receive additional 500 Shares
0.05%
2,000,000
585
500 Shares plus 530 out of 585 to receive additional 500 Shares
0.05%
2,500,000
403
1,000 Shares plus 155 out of 403 to receive additional 500
Shares
0.05%
3,000,000
226
1,000 Shares plus 195 out of 226 to receive additional 500
Shares
0.05%
3,500,000
135
1,500 Shares plus 46 out of 135 to receive additional 500
Shares
0.05%
4,000,000
122
1,500 Shares plus 100 out of 122 to receive additional 500
Shares
0.05%
4,500,000
82
2,000 Shares plus 24 out of 82 to receive additional 500 Shares
0.05%
5,000,000
89
2,000 Shares plus 69 out of 89 to receive additional 500 Shares
0.05%
5,500,000
60
2,500 Shares plus 15 out of 60 to receive additional 500 Shares
0.05%
6,000,000
95
2,500 Shares plus 69 out of 95 to receive additional 500 Shares
0.05%
7,476,000
613
3,500 Shares plus 81 out of 613 to receive additional 500
Shares
0.05%
7,501
Total number of Pool B successful applicants: 7,310
As of the date of this announcement, the relevant subscription monies previously deposited
in the designated nominee accounts have been remitted back to the accounts of all HKSCC
participants. Investors should contact their relevant brokers for any inquiries.
– 17 –

<<<PAGE 18>>>
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in
respect of which consent has been obtained, the Company has complied with the Listing
Rules and guidance materials in relation to the placing, allotment and listing of the
Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the
placees or the public (as the case may be) directly or indirectly for each Offer Share
subscribed for or purchased by them was the same as the final Offer Price in additional to
any brokerage, AFRC transaction levy, SFC transaction levy and Stock Exchange
trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Allocation of H Shares to existing minority Shareholders and/or their close associates
The Company has applied for, and the Stock Exchange has granted, a waiver from strict
compliance with Rule 10.04, and a consent under paragraph 1C(2) of Appendix F1 to the
Listing Rules to permit H Shares in the International Offering to be placed to certain
existing minority Shareholders and/or their close associates who (i) hold less than 5% of
the voting rights in the Company prior to the completion of the Global Offering and (ii)
are not and will not become (upon the completion of the Global Offering) core connected
persons of the Company or the close associates of any such core connected person
(together, the “Permitted Existing Shareholders”), on the following conditions:
(a) each Permitted Existing Shareholder to whom the Company may allocate the H
Shares under the International Offering, together with their close associates, holds
less than 5% of the voting rights in the Company prior to the completion of the
Global Offering;
(b) each Permitted Existing Shareholder is not, and will not be, a core connected person
of the Company or any close associate of any such core connected person
immediately prior to or following the Global Offering;
(c)
none of the Permitted Existing Shareholders has the power to appoint any Directors
nor have any other special rights in the Company;
(d) allocation to the Permitted Existing Shareholders and/or their close associates will
not affect the Company’s ability to satisfy the public float requirement under Rule
19A.13A(2) of the Listing Rules;
– 18 –

<<<PAGE 19>>>
(e)
based on discussions between the Company and the Overall Coordinators and
confirmations required to be submitted to the Stock Exchange by the Sole Sponsor
and the Overall Coordinators, the Company will confirm to the Stock Exchange
that:
a.
in case of participation as Cornerstone Investors, no preferential treatment has
been, nor will be, given to the Permitted Existing Shareholders and/or their close
associates by virtue of their relationship with the Company, other than the
preferential treatment of assured entitlement under a cornerstone investment
following the principles set out in Chapter 4.15 of the Guide, and the
cornerstone
investment
agreements
entered
into
between
the
Permitted
Existing Shareholder and/or their close associates do not contain any material
terms which are more favourable to the Permitted Existing Shareholders and/or
their close associates than those in other cornerstone investment agreements; or
b.
in case of participation as placees, no preferential treatment will be given to the
Permitted Existing Shareholders and/or their close associates in the allocation
process by virtue of their relationship with the Company;
(f)
in the case of participation as placees, the Overall Coordinators will confirm to the
Stock Exchange that, to the best of their knowledge and belief, no preferential
treatment has been, nor will be, given to any of the Permitted Existing Shareholders
or their close associates by virtue of their relationship with the Company in any
allocation in the International Offering; and
(g) the Sole Sponsor will confirm to the Stock Exchange that based on (a) its discussions
with the Company and the Overall Coordinators; and (b) the confirmations provided
to the Stock Exchange by the Company and the Overall Coordinators (confirmations
(e) and (f) mentioned above), and to the best of their knowledge and belief, it has no
reason to believe that the Permitted Existing Shareholders and/or their close
associates received any preferential treatment in the allocation process either as
cornerstone investors or as placees by virtue of their relationship with the Company,
other than, in the case of participation as cornerstone investors, the preferential
treatment of assured entitlement under a cornerstone investment following the
principles set out in Chapter 4.15 of the Guide, and details of allocation to the
Permitted Existing Shareholders holding more than 1% of the issued share capital of
the Company and/or their close associates immediately prior to the completion of
the Global Offering will be disclosed in this prospectus (for cornerstone investors)
and allotment results announcement (for both cornerstone investors and placees) of
the Company.
Please refer to the section headed “Waivers — Allocation of H Shares to Existing
Minority Shareholders and their close associates” in the Prospectus for further details of
the waiver and consent.
Among the Cornerstone Investors, GF Fund, Fullgoal and Taikang Life are Permitted
Existing Shareholders. Such allocations of Offer Shares to the Permitted Existing
Shareholders are in compliance with all the conditions under the waiver and consent
granted by the Stock Exchange.
– 19 –

<<<PAGE 20>>>
Allocation of Offer Shares to existing Shareholders and Cornerstone Investors and/or their
close associates with a consent under paragraph 18 of Chapter 4.15 of the Guide for New
Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under
paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the
Company to allocate further Offer Shares in the International Offering to certain existing
Shareholders and Cornerstone Investors and/or their close associates as placees, subject
to the following conditions:
(a) the final offering size of the Global Offering will be of a total value of at least HK$1
billion;
(b) the Offer Shares allocated to all existing Shareholders and their close associates
(whether as cornerstone investors and/or as placees) as permitted under the
Size-based Exemption (as defined in the Guide for New Listing Applicants) do not
exceed 30% of the total number of the H Shares offered under the Global Offering;
(c)
each Director and chief executive of the Company confirms that no securities have
been allocated to them or their respective close associates under this exemption;
(d) the Company will comply with the public float requirement under Rule 8.08(1) of the
Listing Rules; and
(e)
details of the allocation to such existing shareholders and Cornerstone Investors
under the Size-based Exemption will be disclosed in this announcement.
Such allocations of Offer Shares to the existing Shareholders and Cornerstone Investors
and/or their close associates are in compliance with all the conditions under the consent
granted by the Stock Exchange. For details of the placing to connected clients, please see
“Allotees with waivers/consents obtained — Allotees with consent under paragraph 18 of
Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further
H Shares to existing shareholders and Cornerstone Investors and/or their close
associates” in this announcement.
Placing to connected clients with prior consent under paragraph 1C(1) of the Placing
Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has
granted, a consent under paragraph 1(C)(1) of the Placing Guidelines to permit CICC FT
to participate in the Global Offering as a Cornerstone Investor. For details of the consent
granted, please refer to the section headed “Allotment Results Details — International
Offering — Cornerstone Investors” in this announcement.
In addition, under the International Offering, certain Offer Shares were placed to
connected clients of their connected distributors pursuant to the Placing Guidelines.
Please refer to the section headed “Allotment Results Details — International Offering —
Allotees with waivers/consents obtained” in this announcement for details. The
Company has applied to the Stock Exchange for, and the Stock Exchange has granted,
a consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to
– 20 –

<<<PAGE 21>>>
allocate such Offer Shares in the International Offering to the connected clients. The
allocation of Offer Shares to such connected clients is in compliance with all the
conditions under the consent granted by the Stock Exchange.
For details of the placing to connected clients, please see “Allotees with waivers/consents
obtained — Allotees with consent under paragraph 1C(1) of the Placing Guidelines and
Chapter 4.15 of the Guide in relation to allocations to connected clients” in this
announcement.
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong
Limited (the “Stock Exchange”) and Hong Kong Securities Clearing Company Limited
(“HKSCC”) take no responsibility for the contents of this announcement, make no
representation as to its accuracy or completeness and expressly disclaim any liability
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part
of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or
into the United States (including its territories and possessions, any state of the United
States and the District of Columbia). This announcement does not constitute or form a
part of any offer or solicitation to purchase or subscribe for securities in the United
States. The securities mentioned herein have not been, and will not be, registered under
the United States Securities Act of 1933, as amended (the “U.S. Securities Act”). The
securities may not be offered or sold in the United States except pursuant to an exemption
from the registration requirements of the U.S. Securities Act and in compliance with any
applicable state securities laws, or outside the United States unless in compliance with
Regulation S under the U.S. Securities Act. There will be no public offer of securities in
the United States.
The Offer Shares are being offered and sold outside the United States in offshore
transactions in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation
or offer to acquire, purchase or subscribe for securities. This announcement is not a
prospectus. Potential investors should read the Prospectus dated 12 June 2026 issued by
Shenzhen Senior Technology Material Co., Ltd. for detailed information about the Global
Offering described below before deciding whether or not to invest in the Shares thereby
being offered.
*Potential investors of the Offer Shares should note that the Sole Sponsor and the
Sponsor-OC (for itself and on behalf of the other Hong Kong Underwriters) shall be
entitled to terminate their obligations under the Hong Kong Underwriting Agreement with
immediate effect upon the occurrence of any of the events set out in the paragraph headed
“Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public
Offering — Hong Kong Underwriting Agreement — Grounds for Termination” in the
Prospectus at any time prior to 8: 00 a.m. (Hong Kong time) on the Listing Date (which
is currently expected to be on Tuesday, 23 June 2026).
– 21 –

<<<PAGE 22>>>
PUBLIC FLOAT AND FREE FLOAT
Under Rule 19A.13A(2) of the Listing Rules, the portion of H Shares held by the public,
at the time of Listing, must (a) represent at least 10% of the Company’s total number of
issued Shares (excluding treasury shares); or (b) have an expected market value of not
less than HK$3,000,000,000. Immediately following the completion of the Global
Offering, the total number of the H Shares issued pursuant to the Global Offering
represents 10.13% of the total issued share capital of our Company (excluding treasury
shares), which satisfy the minimum public float requirement under Rule 19A.13A(2)(a) of
the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following
the Listing Date. Based on an Offer Price of HK$8.98 per H Share, the Company will
satisfy the free float requirement under Rule 19A.13C(2) of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global
Offering, (i) no placee will, individually, be placed more than 10% of the enlarged issued
share capital of the Company immediately after the Global Offering; (ii) there will not be
any new substantial Shareholder immediately after the Global Offering; (iii) the three
largest public shareholders of the Company do not hold more than 50% of the shares in
public hands at the time of the Listing in compliance with Rules 8.08(3) and 8.24 of the
Listing Rules; and (iv) there will be at least 300 Shareholders at the time of the Listing in
compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8: 00 a.m. on Tuesday,
23 June 2026 (Hong Kong time), provided that the Global Offering has become
unconditional and the right of termination described in the section headed “Underwriting
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds
for Termination” in the Prospectus has not been exercised. Investors who trade the H
Shares on the basis of publicly available allocation details prior to the receipt of H Share
certificates or prior to the H Share certificates becoming valid evidence of title do so
entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8: 00 a.m. on
Tuesday, 23 June 2026 (Hong Kong time), it is expected that dealings in the H Shares on
the Stock Exchange will commence at 9: 00 a.m. on Tuesday, 23 June 2026 (Hong Kong
time). The H Shares will be traded in board lots of 500 H Shares each, and the stock code
of the H Shares will be 6067.
By order of the Board
Shenzhen Senior Technology Material Co., Ltd.
深圳市星源材質科技股份有限公司
Prof. Chen Xiufeng
Chairman and Executive Director
Hong Kong, 22 June 2026
– 22 –

<<<PAGE 23>>>
As at the date of this announcement, the Board comprises: Prof. Chen Xiufeng, Dr. Zhang
Xiaomin and Mr. Xu Liqiang as executive directors, Mr. Zhu Bide as a non-executive
director and Mr. Tang Changjiang, Dr. Lin Zhiwei and Ms. Sun Zhenzhen as independent
non-executive directors.
– 23 –
