# 配发结果公告抽取任务：0537.HK RIGOL Technologies Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**08/07/2026 22:29**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0708/2026070801336.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"0537.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
(the “Stock Exchange”, or the “Hong Kong Stock Exchange”) and Hong Kong Securities
Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this
announcement, make no representation as to its accuracy or completeness and expressly
disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the
whole or any part of the contents of this announcement.
Unless otherwise defined herein, capitalised terms used in this announcement shall have the
same meanings as those defined in the prospectus dated 30 June 2026 (the “Prospectus”) of
RIGOL Technologies Co., Ltd. (普源精電科技股份有限公司) (the “Company”). This
announcement is made by the order of the board (the “Board”) of directors (the
“Directors”) of the Company. The Board collectively and individually accept responsibility
for the accuracy of this announcement.
This announcement is for information purposes only and does not constitute an invitation or
offer to acquire, purchase or subscribe for any securities. This announcement is not a
prospectus. Potential investors should read the Prospectus for detailed information about
the Global Offering described below before deciding whether or not to invest in the Offer
Shares. Any investment decision in relation to the Offer Shares should be taken solely in
reliance on the information provided in the Prospectus.
This announcement is not for release, publication or distribution, directly or indirectly, in or
into the United States (including its territories and possessions, any state of the United
States and the District of Columbia or any other jurisdiction where such distribution is
prohibited by laws). This announcement does not constitute or form a part of any offer or
solicitation to purchase or subscribe for securities in the United States or in any other
jurisdictions. The securities mentioned herein have not been, and will not be, registered
under the United States Securities Act of 1933 as amended from time to time (the “U.S.
Securities Act”) or securities law of any state or other jurisdiction of the United States. The
securities may not be offered, sold, pledged or otherwise transferred within the United
States, except pursuant to an available exemption from, or in a transaction not subject to,
the registration requirements of the U.S. Securities Act and in accordance with any
applicable state securities laws in the United States. The Offer Shares may only be offered
and sold outside the United States in offshore transactions in reliance on Regulation S.
There will be no public offer of securities in the United States.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to terms
and conditions set out in the Prospectus. The Hong Kong Offer Shares will not be offered to
any person who is outside Hong Kong and/or not resident in Hong Kong. Potential investors
of the Offer Shares should note that the Sole Sponsor and the Sponsor-Overall Coordinator
(for itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of
the events set out in the section headed “Underwriting — Underwriting Arrangements and
Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus at
any time prior to 8: 00 a.m. on the Listing Date.
– 1 –

<<<PAGE 2>>>
RIGOL Technologies Co., Ltd.
普源精電科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under
the Global Offering
:
24,802,200 H Shares
Number of Hong Kong Offer Shares
:
2,480,300 H Shares
Number of International Offer Shares
:
22,321,900 H Shares
Final Offer Price
:
HK$45.98 per H Share plus brokerage of
1%, SFC transaction levy of 0.0027%,
Stock Exchange trading fee of 0.00565%
and AFRC transaction levy of 0.00015%
(payable in full on application in Hong
Kong dollars and subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
00537
Sole Sponsor, Sponsor-Overall Coordinator, Overall Coordinator, Joint Global Coordinator,
Joint Bookrunner and Joint Lead Manager
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
– 2 –

<<<PAGE 3>>>
RIGOL TECHNOLOGIES CO., LTD.
普源精電科技股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the
same meanings as those defined in the prospectus dated 30 June 2026 (the “Prospectus”)
issued by RIGOL Technologies Co., Ltd. (普源精電科技股份有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of
Shareholders, Shareholders and prospective investors should be aware that the price of
the H Shares could move substantially even with a small number of H Shares traded and
should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
00537
Stock short name
RIGOL
Dealings commencement date
9 July 2026*
*
see note at the end of the announcement
Price Information
Final Offer Price
HK$45.98
Maximum Offer Price
HK$45.98
Offer Shares and Share Capital
Number of Offer Shares
24,802,200
Number of Offer Shares in Hong Kong Public
Offering
2,480,300
Number of Offer Shares in International Offering
22,321,900
Number of issued shares upon Listing
218,676,617
Proceeds
Gross proceeds (Note)
HK$1,140.4 million
Less: Estimated listing expenses payable based on
Final Offer Price
HK$99.6 million
Net proceeds
HK$1,040.8 million
Note:
Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use
of proceeds, please refer to section headed “Future Plans and Use of Proceeds” of the Prospectus.
– 3 –

<<<PAGE 4>>>
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
Number of valid applications
92,738
Number of successful applications
13,851
Subscription level
356.86 times
Claw-back triggered
N/A
Number of Offer Shares initially available under the
Hong Kong Public Offering
2,480,300
Number of Offer Shares reallocated from the
International Offering (reallocation)
0
Final number of Offer Shares under the Hong Kong
Public Offering
2,480,300
% of final number of Offer Shares under the Hong
Kong Public Offering to the Global Offering
10.00%
Note:
For details of the final allocation of shares to the Hong Kong Public Offering, investors can refer to
https://www.hkeipo.hk/iporesult
to
perform
a
search
by
identification
number
or
https://www.hkeipo.hk/iporesult for the full list of allottees.
INTERNATIONAL OFFERING
Number of placees
91
Subscription Level
9.17 times
Number of Offer Shares initially available under the
International Offering
22,321,900
Number of Offer Shares reallocated to the Hong Kong
Public Offering
0
Final number of Offer Shares under the International
Offering
22,321,900
% of final number of Offer Shares under the
International Offering to the Global Offering
90.00%
The Directors confirm that, to the best of their knowledge, information and belief, save for
(a) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent
under paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”)
granted by the Stock Exchange to permit the Company to allocate certain Offer Shares in
the International Offering to certain permitted existing minority shareholders (the
“Existing Minority Shareholders”) and/or their close associates, and (b) a consent under
paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the
Company to, among other things, allocate further H Shares in the International Offering to
certain existing shareholders and Cornerstone Investors and/or their close associates, (i)
none of the Offer Shares subscribed by the placees and the public have been financed
directly or indirectly by the Company, any of its Directors, chief executive, Controlling
– 4 –

<<<PAGE 5>>>
Shareholders, substantial Shareholders, existing Shareholders of the Company or any of its
subsidiaries or their respective close associates; and (ii) none of the placees and the public
who have purchased the Offer Shares are accustomed to taking instructions from the
Company, any of the Directors, chief executive, substantial Shareholders, Controlling
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their
respective close associates in relation to the acquisition, disposal, voting or other disposition
of H Shares registered in his/her/its name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
Investor
Number of
Offer Shares
allocated
Approximate % of
total issued
H Shares after the
Global
Offering(1)(2)(3)
Approximate % of
total issued share
capital in the
Company after the
Global
Offering(1)(2)(3)(4)
Existing
shareholders or
their close
associates
HHLR Advisors, Ltd. (the
“HHLRA”)
4,261,300
17.18%
1.95%
No
CPE Hemlock Investment Limited
(the “CPE Hemlock”)
2,130,600
8.59%
0.97%
No
Suzhou Investors
.
Suzhou National High-tech
Industrial Development Zone
Management Committee (the
“Suzhou High-tech Zone”)
(consists of (a) Suzhou Taihu
Golden Valley Construction
and Development Co., Ltd.
(the “Taihu Golden Valley”)
and (b) Suzhou Science and
Technology City
Development Group Co.,
Ltd. (the “Kefa Group”))
1,704,500
6.87%
0.78%
No
.
Hua Yuan International
Limited (the “Hua Yuan”)
1,193,100
4.81%
0.55%
No
Subtotal
2,897,600
11.68%
1.33%
—
Sungrow Power (Hong Kong) Co.,
Limited (the “Sungrow Power HK”)
681,800
2.75%
0.31%
No
CITIC-Prudential Fund
Management Company Ltd. (the
“CITIC Prudential Fund”)
303,400
1.22%
0.14%
Yes
Purple Diamond Ltd (the “Panglin
Group”)
170,400
0.69%
0.08%
No
Total
10,445,100
42.11%
4.78%
—
– 5 –

<<<PAGE 6>>>
Investor
Number of
Offer Shares
allocated
Approximate % of
total issued
H Shares after the
Global
Offering(1)(2)(3)
Approximate % of
total issued share
capital in the
Company after the
Global
Offering(1)(2)(3)(4)
Existing
shareholders or
their close
associates
Notes:
(1)
The number of H Shares immediately after the Global Offering is the same as the number of Offer
Shares to be issued under the Global Offering.
(2)
In addition to the Offer Shares subscribed for as Cornerstone Investors, HHLRA, Sungrow Power
HK, Panglin Group and CITIC Prudential Fund were allocated further Offer Shares as placees in the
International Offering. Please refer to the section headed “Allotment Results Details — International
Offering — Allottees with Waivers/Consents Obtained” in this announcement for details. Only the
Offer Shares subscribed for as Cornerstone Investors are subject to lock-up as indicated below. For
details, please refer to the section headed “Lock-up Undertakings — Cornerstone Investors” in this
announcement.
(3)
For details of the waiver from strict compliance with Rule 10.04 of the Listing Rules and prior consent
under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by existing
minority Shareholders and/or their close associates, please refer to the section headed “Others/
Additional Information — Allocation of H Shares to Existing Minority Shareholders and/or their
close associates” in this announcement.
(4)
Not taking into account any A Shares held by the relevant Cornerstone Investors.
– 6 –

<<<PAGE 7>>>
Allottees with Waiver/Consent Obtained
Investor
Number of Offer
Shares allocated
Approximate %
of total issued H
Shares after the
Global
Offering(1)
Approximate %
of total issued
share capital in
the Company
after the Global
Offering(2)
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by Existing Minority
Shareholders holding 1% or more of the issued share capital of the Company immediately prior to the
completion of the Global Offering and/or their close associates(3)
CITIC Prudential Fund
610,200
2.46%
0.28%
An Existing
Minority
Shareholder, and
also acting as a
Cornerstone
Investor
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for
New Listing Applicants in relation to allocations to connected clients(4)
CITIC Prudential Fund
610,200
2.46%
0.28%
CITIC Prudential
Fund is a member
of the same group
of companies as
CLSA Limited who
is a distributor of
the Global Offering
CITIC Securities Asset
Management Company
Limited (the “CITIC
AM”)
5,200
0.02%
0.0024%
CITIC AM is a
member of the same
group of companies
as CLSA Limited
who is a distributor
of the Global
Offering
CITIC Securities Asset
Management (HK)
Limited (the “CITIC AM
HK”)
5,200
0.02%
0.0024%
CITIC AM HK is a
member of the same
group of companies
as CLSA Limited
who is a distributor
of the Global
Offering
China Asset Management
Co., Ltd. (the “China
AMC”)
852,200
3.44%
0.39%
China AMC is a
member of the same
group of companies
as CLSA Limited
who is a distributor
of the Global
Offering
– 7 –

<<<PAGE 8>>>
Investor
Number of Offer
Shares allocated
Approximate %
of total issued H
Shares after the
Global
Offering(1)
Approximate %
of total issued
share capital in
the Company
after the Global
Offering(2)
Relationship
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in
relation to allocations of further H Shares to existing Shareholders and Cornerstone Investors and/or their
close associates(5)
HHLRA
852,200
3.44%
0.39%
Cornerstone
Investor
Sungrow Power HK
594,800
2.40%
0.27%
Cornerstone
Investor
Panglin Group
169,600
0.68%
0.08%
Cornerstone
Investor
CITIC Prudential Fund
306,800
1.24%
0.14%
Cornerstone
Investor
Notes:
(1)
The number of H Shares immediately after the Global Offering is the same as the number of Offer
Shares to be issued under the Global Offering.
(2)
Not taking into account any A Shares held by the relevant Cornerstone Investors.
(3)
Among the Cornerstone Investors, CITIC Prudential Fund is an Existing Minority Shareholder who
does not hold 1% or more of the issued share capital of the Company (including the treasury Shares)
immediately prior to the completion of the Global Offering. The Stock Exchange has granted a waiver
from strict compliance with the requirements under Rule 10.04 of the Listing Rules and consent under
Paragraph 1C(2) of the Placing Guidelines to permit H Shares in the International Offering to be
placed to such Existing Minority Shareholders. Please refer to the section headed “Waivers — Waiver
in respect of Allocation of H Shares to Existing Minority Shareholders and Their Close Associates”
of the Prospectus for details.
The Stock Exchange has granted the waiver on the condition that, among others, details of the
allocation to the Existing Minority Shareholders and/or their close associates holding more than 1%
of the issued share capital of the Company immediately prior to the completion of the Global Offering
will be disclosed in the Prospectus and/or allotment results announcement.
(4)
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the
Guide for New Listing Applicants in relation to allocations to connected clients, please refer to the
sections headed “Others/Additional Information — Placing to connected clients with a consent under
paragraph 1C(1) of the Placing Guidelines” and “Others/Additional Information — Allocations of
Offer Shares to the existing Shareholders and Cornerstone Investors and/or their close associates with
a consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants” in this
announcement.
(5)
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents
the number of Offer Shares allocated to the investors as placees in the International Offering. For
allocations of Offer Shares to the relevant investors as Cornerstone Investors, please refer to the
section headed “Allotment Results Details — International Offering — Cornerstone Investors” in this
announcement. For details of the consent under paragraph 18 of Chapter 4.15 of the Guide for New
Listing Applicants in relation to allocations of further H Shares to the existing Shareholders and
Cornerstone Investors and/or their respective close associates, please refer to the section headed
“Others/Additional Information — Allocations of Offer Shares to the existing Shareholders and
Cornerstone Investors and/or their close associates with a consent under paragraph 18 of Chapter 4.15
of the Guide for New Listing Applicants” in this announcement.
– 8 –

<<<PAGE 9>>>
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name(1)
Number of Shares
held in the Company
subject to
lock-up undertakings
upon Listing
Approximate % of
shareholding in the
Company subject to
lock-up undertakings
upon listing
Last day subject to the
lock-up undertakings
Dr. Wang Yue
11,508,480
5.26%
8 January 2027 (First
Six-Month Period)(2)
8 July 2027 (Second
Six-Month Period)(3)
Suzhou RIGOL Investment Co.,
Ltd.
63,936,000
29.24%
8 January 2027 (First
Six-Month Period)(2)
8 July 2027 (Second
Six-Month Period)(3)
Suzhou Ruige Hezhong
Management Consulting
Partnership (Limited Partnership)
5,920,000
2.71%
8 January 2027 (First
Six-Month Period)(2)
8 July 2027 (Second
Six-Month Period)(3)
Suzhou Ruijin Hezhong
Management Consulting
Partnership (Limited Partnership)
5,920,000
2.71%
8 January 2027 (First
Six-Month Period)(2)
8 July 2027 (Second
Six-Month Period)(3)
Mr. Wang Tiejun
15,557,760
7.11%
8 January 2027 (First
Six-Month Period)(2)
8 July 2027 (Second
Six-Month Period)(3)
Mr. Li Weisen
15,557,760
7.11%
8 January 2027 (First
Six-Month Period)(2)
8 July 2027 (Second
Six-Month Period)(3)
Notes:
(1)
For further details, please refer to the section headed “Underwriting — Underwriting Arrangements
and Expenses — Undertakings to the Stock Exchange pursuant to the Listing Rules” in the
Prospectus.
(2)
Each member of the Controlling Shareholders may dispose of or transfer Shares after the indicated
date subject to that any member of the Controlling Shareholders will not cease to be a controlling
shareholder (as defined in the Listing Rules).
(3)
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after
the indicated date.
– 9 –

<<<PAGE 10>>>
Cornerstone Investors
Name
Number of Shares
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
Listing(1)
Approximate %
of shareholding in
the Company
subject to lock-up
undertakings upon
listing
Last day subject
to the lock-up
undertakings(2)
HHLRA
4,261,300
17.18%
1.95%
8 January 2027
CPE Hemlock
2,130,600
8.59%
0.97%
8 January 2027
Suzhou Investors
.
Suzhou High-tech
Zone
1,704,500
6.87%
0.78%
8 January 2027
.
Hua Yuan
1,193,100
4.81%
0.55%
8 January 2027
Subtotal
2,897,600
11.68%
1.33%
—
Sungrow Power HK
681,800
2.75%
0.31%
8 January 2027
CITIC Prudential Fund
303,400
1.22%
0.14%
8 January 2027
Panglin Group
170,400
0.69%
0.08%
8 January 2027
Total
10,445,100
42.11%
4.78%
—
Notes:
(1)
The number of H Shares immediately after the Global Offering is the same as the number of Offer
Shares to be issued under the Global Offering.
(2)
In accordance with the respective cornerstone investment agreements, the required lock-up periods will
end on 8 January 2027. The Cornerstone Investors will cease to be prohibited from disposing of or
transferring the Shares subscribed for pursuant to their respective cornerstone investment agreements
after the indicated date.
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of
H Shares
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
5,113,500
22.91%
20.62%
5,113,500
2.34%
Top 5
12,611,500
56.50%
50.85%
12,611,500
5.77%
Top 10
16,653,000
74.60%
67.14%
16,653,000
7.62%
Top 25
20,706,600
92.76%
83.49%
20,706,600
9.47%
Notes:
*
Ranking of placees is based on the number of H Shares allotted to the placees.
– 10 –

<<<PAGE 11>>>
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number of
H Shares
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
% of total H
Shares held
upon Listing
Number of
Shares held
upon Listing
% of total
issued share
capital upon
Listing
Top 1
5,113,500
22.91%
20.62%
5,113,500
20.62%
5,113,500
2.34%
Top 5
12,611,500
56.50%
50.85%
12,611,500
50.85%
12,611,500
5.77%
Top 10
16,653,000
74.60%
67.14%
16,653,000
67.14%
18,738,785
8.57%
Top 25
20,706,600
92.76%
83.49%
20,706,600
83.49%
23,047,975
10.54%
Notes:
*
Ranking of H Shareholders is based on the number of H Shares held by the Shareholders upon Listing.
– 11 –

<<<PAGE 12>>>
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders*
Number of
H Shares
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
Number of
Shares held
upon Listing#
% of total
issued share
capital upon
Listing
Top 1
0
0.00%
0
0
118,400,000
54.14%
Top 5
8,863,300
39.71%
35.74%
8,863,300
132,243,936
60.47%
Top 10
10,993,900
49.25%
44.33%
10,993,900
140,771,129
64.37%
Top 25
16,020,300
71.77%
64.59%
16,020,300
155,765,261
71.23%
Notes:
*
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon
Listing.
– 12 –

<<<PAGE 13>>>
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, 92,738 valid
applications made by the public will be conditionally allocated on the basis set out below:
Pool A
Number of
H Shares
applied for
Number
of valid
applications
Basis of allocation/ballot
Approximate
percentage
allotted of the
total number of
H Shares
applied for
100
43,966
3,518 out of 43,966 applicants to receive 100 H Shares
8.00%
200
18,926
1,872 out of 18,926 applicants to receive 100 H Shares
4.95%
300
2,658
298 out of 2,658 applicants to receive 100 H Shares
3.74%
400
938
115 out of 938 applicants to receive 100 H Shares
3.07%
500
1,148
151 out of 1,148 applicants to receive 100 H Shares
2.63%
600
589
82 out of 589 applicants to receive 100 H Shares
2.32%
700
446
65 out of 446 applicants to receive 100 H Shares
2.08%
800
477
73 out of 477 applicants to receive 100 H Shares
1.91%
900
424
67 out of 424 applicants to receive 100 H Shares
1.76%
1,000
7,728
1,250 out of 7,728 applicants to receive 100 H Shares
1.62%
1,500
1,229
225 out of 1,229 applicants to receive 100 H Shares
1.22%
2,000
1,951
390 out of 1,951 applicants to receive 100 H Shares
1.00%
2,500
650
140 out of 650 applicants to receive 100 H Shares
0.86%
3,000
626
142 out of 626 applicants to receive 100 H Shares
0.76%
3,500
351
84 out of 351 applicants to receive 100 H Shares
0.68%
4,000
497
123 out of 497 applicants to receive 100 H Shares
0.62%
4,500
413
106 out of 413 applicants to receive 100 H Shares
0.57%
5,000
733
194 out of 733 applicants to receive 100 H Shares
0.53%
6,000
457
128 out of 457 applicants to receive 100 H Shares
0.47%
7,000
322
95 out of 322 applicants to receive 100 H Shares
0.42%
8,000
306
94 out of 306 applicants to receive 100 H Shares
0.38%
9,000
232
74 out of 232 applicants to receive 100 H Shares
0.35%
10,000
1,565
512 out of 1,565 applicants to receive 100 H Shares
0.33%
20,000
911
369 out of 911 applicants to receive 100 H Shares
0.20%
30,000
500
229 out of 500 applicants to receive 100 H Shares
0.15%
40,000
428
214 out of 428 applicants to receive 100 H Shares
0.13%
50,000
246
132 out of 246 applicants to receive 100 H Shares
0.11%
60,000
220
125 out of 220 applicants to receive 100 H Shares
0.09%
70,000
166
99 out of 166 applicants to receive 100 H Shares
0.09%
80,000
164
102 out of 164 applicants to receive 100 H Shares
0.08%
90,000
129
83 out of 129 applicants to receive 100 H Shares
0.07%
100,000
1,893
1,251 out of 1,893 applicants to receive 100 H Shares
0.07%
Total
91,289
Total number of Pool A successful applicants: 12,402
– 13 –

<<<PAGE 14>>>
Pool B
Number of
H Shares
applied for
Number
of valid
applications
Basis of allocation/ballot
Approximate
percentage
allotted of the
total number of
H Shares
applied for
200,000
804
700 H Shares
0.35%
300,000
225
800 H Shares plus 72 out of 225 applicants to receive
an additional 100 H Shares
0.28%
400,000
107
900 H Shares plus 44 out of 107 applicants to receive
an additional 100 H Shares
0.24%
500,000
87
1,000 H Shares plus 30 out of 87 applicants to receive
an additional 100 H Shares
0.21%
600,000
56
1,100 H Shares plus 10 out of 56 applicants to receive
an additional 100 H Shares
0.19%
700,000
38
1,100 H Shares plus 36 out of 38 applicants to receive
an additional 100 H Shares
0.17%
800,000
14
1,200 H Shares plus 9 out of 14 applicants to receive
an additional 100 H Shares
0.16%
900,000
15
1,300 H Shares plus 5 out of 15 applicants to receive
an additional 100 H Shares
0.15%
1,000,000
11
1,300 H Shares plus 10 out of 11 applicants to receive
an additional 100 H Shares
0.14%
1,100,000
23
1,400 H Shares plus 11 out of 23 applicants to receive
an additional 100 H Shares
0.13%
1,240,100
69
1,500 H Shares plus 16 out of 69 applicants to receive
an additional 100 H Shares
0.12%
Total
1,449
Total number of Pool B successful applicants: 1,449
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
any brokerage, AFRC transaction levy, SFC transaction levy and Stock Exchange’s
trading fee payable.
– 14 –

<<<PAGE 15>>>
OTHERS/ADDITIONAL INFORMATION
Allocation of H Shares to Existing Minority Shareholders and/or their close associates
The Company has applied to, and the Stock Exchange has granted, a waiver from strict
compliance with the requirements under Rule 10.04 and consent under Paragraph 1C(2)
of Appendix F1 to the Listing Rules to permit H Shares in the International Offering to
be placed to certain existing minority Shareholders who (i) hold less than 5% of the total
number of issued Shares prior to the completion of the Global Offering and (ii) are not
and will not become (upon the completion of the Global Offering) core connected
persons of the Company or the close associates of any such core connected person
(together, the “Permitted Existing Shareholders”), subject to the conditions as follows:
(a) each Permitted Existing Shareholder to whom the Company may allocate the H
Shares under the International Offering holds less than 5% of the total number of
issued Shares prior to the completion of the Global Offering;
(b) each Permitted Existing Shareholder is not, and will not be, a core connected person
of the Company or any close associate of any such core connected person
immediately prior to or following the Global Offering;
(c)
none of the Permitted Existing Shareholders has the power to appoint any Directors
nor have any other special rights in the Company;
(d) allocation to the Permitted Existing Shareholders and their close associates will not
affect the Company’s ability to satisfy the public float requirement;
(e)
the Company will confirm to the Stock Exchange that:
(i)
in case of participation as cornerstone investors, no preferential treatment has
been, nor will be, given to the Permitted Existing Shareholders and/or their close
associates by virtue of their relationship with the Company, other than the
preferential treatment of assured entitlement under a cornerstone investment
following the principles set out in Chapter 4.15 of the Guide nor is the Permitted
Existing Shareholders in a position to exert influence on the Company to obtain
actual
or
perceived
preferential
treatment,
and
the
Permitted
Existing
Shareholders’ cornerstone investment agreements do not contain any material
terms which are more favorable to the Permitted Existing Shareholders than
those in other cornerstone investment agreements; or
(ii) in case of participation as placees, no preferential treatment has been, nor will
be, given to the Permitted Existing Shareholders and/or their close associates
nor is the Permitted Existing Shareholders in a position to exert influence on the
Company to obtain actual or perceived preferential treatment in the allocation
process by virtue of their relationship with the Company;
– 15 –

<<<PAGE 16>>>
(f)
in the case of participation as placees, the Overall Coordinators will confirm to the
Stock Exchange that, to the best of their knowledge and belief, no preferential
treatment has been, nor will be, given to any of the Permitted Existing Shareholders
or their close associates by virtue of their relationship with the Company in any
allocation in the International Offering; and
(g) the Sole Sponsor will confirm to the Stock Exchange that: (i) each Permitted Existing
Shareholder has less than 5% voting rights in the applicant before the Global
Offering; (ii) each Permitted Existing Shareholder is not a core connected person of
the Company or its close associate; (iii) each Permitted Existing Shareholder does
not have the power to appoint directors or any other special rights; (iv) allocation to
the Permitted Existing Shareholders or their close associates will not affect the
Company’s ability to satisfy the public float requirement; and (v) it has no reason to
believe that the Permitted Existing Shareholders or their close associates received
any preferential treatment in the IPO allocation as a placee or a cornerstone investor
by virtue of their relationship with the Company other than the preferential
treatment of assured entitlement under a cornerstone investment following the
principles set out in Chapter 4.15 of the Guide, and details of the allocation to the
Permitted Existing Shareholders holding more than 1% of the issued share capital of
the Company immediately prior to the completion of the Global Offering will be
disclosed in the Prospectus (for cornerstone investors) and/or allotment results
announcement (for both cornerstone investors and placees) of the Company.
Please refer to the section headed “Waivers — Waiver in respect of Allocation of H
Shares to Existing Minority Shareholders and Their Close Associates” in the Prospectus
for further details of the waiver and consent.
Each of the Sole Sponsor, the Overall Coordinators and the Company has provided the
required confirmations as elaborated in the Prospectus. In particular, as the Company’s
A Shares have been listed on the Shanghai Stock Exchange’s STAR Market with the
stock code of 688337 since 8 April 2022, the Company has a highly extensive base of
existing Shareholders and disclosure of details of allocations to all Permitted Existing
Shareholders and/or their respective close associates will not be meaningful to investors,
the proposed disclosure threshold, i.e. condition (g) of the waiver and consent which
provides that details of the allocation to the Permitted Existing Shareholders and/or their
respective close associates holding more than 1% of the issued share capital of the
Company immediately prior to the completion of the Global Offering will be disclosed in
this announcement, is appropriate.
All allocations of Offer Shares to the Permitted Existing Shareholders are in compliance
with all the conditions under the waiver and consent granted by the Stock Exchange.
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing
Guidelines
The Company has applied to, and the Stock Exchange has granted, a consent under
paragraph 1C(1) of the Placing Guidelines to permit CITIC Prudential Fund to
participate in the Global Offering as a connected client in its capacity as a Cornerstone
– 16 –

<<<PAGE 17>>>
Investor. For details of the consent granted, please refer to the section headed
“Allotment Results Details — International Offering — Cornerstone Investors” in this
announcement.
In addition, under the International Offering, certain Offer Shares were placed to
connected clients of their connected distributor pursuant to the Placing Guidelines as
placees. Please refer to the section headed “Allotment Results Details — International
Offering — Allottees with Waiver/Consent Obtained” in this announcement for details.
The Company has applied to the Stock Exchange for, and the Stock Exchange has
granted, a consent under paragraph 1C(1) of the Placing Guidelines to permit the
Company to allocate such Offer Shares in the International Offering to the connected
clients as placees. The allocation of Offer Shares to such connected clients is in
compliance with all the conditions under the consent granted by the Stock Exchange.
Details of the placement to connected clients as placees are set out below.
No.
Connected
Distributor
Connected Client
Relationship
Discretionary or
Non-Discretionary
Whether the
Connected Client is a
collective investment
scheme which is not
authorised by
the SFC or is
expected to hold the
Offer Shares on
behalf of
such scheme
Number of Offer
Shares to be
allocated to the
Connected Client
Approximate
percentage of
total number of
Offer Shares
under the
Global Offering
1.
CLSA Limited
CITIC Prudential Fund(1)
CITIC Prudential
Fund is a member
of the same group
of companies as
CLSA Limited
Discretionary
No
As Cornerstone
Investor: 303,400
As placee: 306,800
Total: 610,200
2.46%
2.
CLSA Limited
CITIC AM(2)
CITIC AM is a
member of the
same group of
companies as
CLSA Limited
Discretionary
Yes, CITIC AM is
expected to hold
the Offer Shares on
behalf of such
scheme. Please refer
to note 2 for
background and
details of these
schemes.
5,200
0.02%
3.
CLSA Limited
CITIC AM HK(3)
CITIC AM HK is a
member of the
same group of
companies as
CLSA Limited
Discretionary
No
5,200
0.02%
4.
CLSA Limited
China AMC(4)
China AMC is a
member of the
same group of
companies as
CLSA
Discretionary
Yes, China AMC is
expected to hold
the Offer Shares on
behalf of such
scheme. Please refer
to note 4 for
background and
details of these
schemes.
852,200
3.44%
– 17 –

<<<PAGE 18>>>
Notes:
1.
CITIC Prudential Fund will hold the Offer Shares in its capacity as the discretionary fund manager of
CITIC Prudential Global Macro-asset Allocation AMP 1 on behalf of the underlying clients which
are independent third parties. To the best knowledge of CITIC Prudential Fund, no single ultimate
beneficial owner holds 30% or more of the ultimate beneficial interest in CITIC Prudential Global
Macro-asset Allocation AMP 1. CLSA and CITIC Prudential Fund are members of the same group.
Therefore, CITIC Prudential Fund is a connected client of CLSA.
2.
CITIC AM will hold the Offer Shares in its capacity as the discretionary fund manager managing the
funds on behalf of their investors (the “CITIC Asset Management Ultimate Clients”), each of which is,
to the best knowledge of CITIC AM, an independent third party.
The details of the CITIC Asset Management Ultimate Clients are as follows:
Fund Name
Values of Assets
under Management
Whether the
Scheme is
Publicly
Marketed
Fund Manager
UBO Holding
30% or More
Interests in the
Fund
UBO of Fund
Manager
CITIC Securities AM-Guibinfengyuan No.118
QDII (中信證券資管貴賓豐元118號QDII集合資
產管理計劃)
RMB228.67 million
as of 3 July 2026
Not publicly
marketed
CITIC AM
Zhang Guofeng
(張國鋒)
CITIC Securities
Company Limited
CITIC SECURITIES COMPANY
LIMITED-XINHANG ZHIYUAN NO.1
(中信證券信航致遠1號集合資產管理計劃)
RMB24.05 million
as of 3 July 2026
Not publicly
marketed
CITIC AM
No
CITIC Securities
Company Limited
CITIC SECURITIES COMPANY
LIMITED-XINHANG ZHIYUAN NO.3
(中信證券信航致遠3號集合資產管理計劃)
RMB56.19 million
as of 3 July 2026
Not publicly
marketed
CITIC AM
No
CITIC Securities
Company Limited
CITIC SECURITIES
AM-GUIBINFENGYUAN NO.108 QDII
(中信證券資管貴賓豐元108號QDII集合資產管理
計劃)
RMB155.97 million
as of 3 July 2026
Not publicly
marketed
CITIC AM
No
CITIC Securities
Company Limited
3.
CITIC AM HK will hold the Offer Shares in its capacity as the discretionary fund manager managing
the funds on behalf of their investors, each of which is an independent third party.
The funds are as follows:
(i)
CITIC Securities Asset Management (HK) Limited — Meta Chance2, invested 100% by Meta
Chance Limited, of which the only ultimate beneficial owner holding 30% or more interest is
Song Ke, a natural person; and
(ii)
ICBC (ASIA) LTD-CITIC SECURITIES AM LTD-BSCOMC LTD, invested 100% by
BSCOMC Limited, of which the only ultimate beneficial owner holding 30% or more interest
is State-owned Assets Supervision and Administration Commission of People’s Government of
Beijing Municipality.
4.
China AMC will hold the Offer Shares in its capacity as the discretionary fund manager managing
assets on behalf of its underlying clients (the “China Asset Management Ultimate Clients”), each of
which is an independent third party of China AMC and CLSA and the companies which are members
of the same group of CLSA.
– 18 –

<<<PAGE 19>>>
The details of the China Asset Management Ultimate Clients are as follows:
Fund Name
Values of Assets
under Management
Whether the
Scheme is
Publicly
Marketed
Fund
Manager
UBO Holding
30% or More
Interests in
the Fund
UBO of Fund
Manager
ChinaAMC Global Selective
Equity Fund (華夏全球精選)
RMB2.83 million as
of 6 July 2026
Publicly
marketed
China AMC
No
CITIC Securities
Company
Limited
Mackenzie ChinaAMC all
China Equity Fund
RMB350 million as
of 6 July 2026
Publicly
marketed
China AMC
No
CITIC Securities
Company
Limited
JSS All China Equity Fund
RMB1.69 million as
of 6 July 2026
Publicly
marketed
China AMC
No
CITIC Securities
Company
Limited
Allocations of Offer Shares to the existing Shareholders and Cornerstone Investors and/or
their close associates with a consent under paragraph 18 of Chapter 4.15 of the Guide for
New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under
paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the
Company to allocate further Offer Shares in the International Offering to certain
Cornerstone Investors and/or their close associates as placees, subject to the following
conditions (“Allocation to Size-based Exemption Participants”):
(a) the final offering size of the Global Offering will be of a total value of at least HK$1
billion;
(b) the Offer Shares allocated to all existing Shareholders (whether as cornerstone
investors and/or as placees) as permitted under the size-based exemption do not
exceed 30% of the total number of the Offer Shares;
(c)
each Director, chief executive of the Company and Controlling Shareholder has
confirmed that no Offer Shares have been allocated to them or their respective close
associates under the size-based exemption;
(d) the Allocation to Size-based Exemption Participants will not affect the Company’s
ability to satisfy its public float requirement as prescribed by the Stock Exchange
under the waiver from strict compliance with the requirements of Rule 8.08(1) of the
Listing Rules (as amended and replaced by Rule 19A.13A(2) of the Listing Rules for
PRC issuers with other listed shares); and
(e)
the details of the Allocation to Size-based Exemption Participants under the
size-based exemption are disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the
consent granted by the Stock Exchange.
– 19 –

<<<PAGE 20>>>
For details of the allocations of Offer Shares to existing Shareholders and Cornerstone
Investors and/or their close associates, please refer to the section headed “Allotment
Results Details — International Offering — Allottees with Waiver/Consent Obtained” in
this announcement.
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong
Limited and Hong Kong Securities Clearing Company Limited take no responsibility for
the contents of this announcement, make no representation as to its accuracy or
completeness and expressly disclaim any liability whatsoever for any loss howsoever
arising from or in reliance upon the whole or any part of the contents of this
announcement.
This announcement is not for release, publication or distribution, directly or indirectly, in
or into the United States (including its territories and possessions, any state of the United
States and the District of Columbia). This announcement does not constitute or form a
part of any offer or solicitation to purchase or subscribe for securities in the United
States. The securities mentioned herein have not been, and will not be, registered under
the U.S. Securities Act. The securities may not be offered or sold in the United States
except pursuant to an available exemption from, or in a transaction not subject to, the
registration requirements of the U.S. Securities Act and in accordance with any
applicable state securities laws in the United States. The Offer Shares may only be
offered and sold outside the United States in offshore transactions in reliance on
Regulation S. There will be no public offer of securities in the United States.
This announcement is for information purposes only and does not constitute an invitation
or offer to acquire, purchase or subscribe for securities. This announcement is not a
prospectus. Potential investors should read the Prospectus dated 30 June 2026 issued by
the Company for detailed information about the Global Offering described above before
deciding whether or not to invest in the Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Sole Sponsor and the
Sponsor-Overall Coordinator (for itself and on behalf of the Hong Kong Underwriters)
shall be entitled to terminate their obligations under the Hong Kong Underwriting
Agreement with immediate effect upon the occurrence of any of the events set out in the
section headed “Underwriting — Underwriting Arrangements and Expenses — Hong
Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to
8: 00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 9
July 2026).
Public Float and Free Float
Immediately following the completion of the Global Offering, the 24,802,200 H Shares to
be issued thereunder are expected to represent approximately 11.34% of the Company’s
total issued share capital and will be counted towards the public float. This exceeds the
minimum public float requirement of at least 10% of the H Shares to be held in public
hands under Rule 19A.13A(2)(a) of the Listing Rules, and thereby satisfies Rule
19A.13A(2) of the Listing Rules.
– 20 –

<<<PAGE 21>>>
Each of the Cornerstone Investors has agreed to a lock-up period of six months following
and including the Listing Date. As such, H Shares held by the Cornerstone Investors
upon the Listing shall not be counted towards the free float of the H Shares of the
Company at the time of Listing. Based on the Final Offer Price of HK$45.98 per H Share,
the Company confirmed that it complies with the free float requirement under Rule
19A.13C(2)(b) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering: (i)
the Shares will be held by at least 300 Shareholders at the time of Listing, in compliance
with Rule 8.08(2) of the Listing Rules; (ii) the three largest public Shareholders will not
hold more than 50% of the H Shares held in public hands at the time of Listing, in
compliance with Rules 8.08(3) and 8.24 of the Listing Rules; (iii) no placee will,
individually, be placed more than 10% of the enlarged issued share capital of the
Company immediately after the Global Offering; and (iv) there will not be any new
substantial Shareholder (as defined in the Listing Rules) immediately after the Global
Offering.
Commencement of Dealings
The H Share certificates will only become valid evidence of title at 8: 00 a.m. on
Thursday, 9 July 2026 (Hong Kong time), provided that the Global Offering has become
unconditional and the right of termination described in the section headed “Underwriting
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds
for Termination” in the Prospectus has not been exercised. Investors who trade the H
Shares on the basis of publicly available allocation details prior to the receipt of H Share
certificates or prior to the H Share certificates becoming valid evidence of title do so
entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8: 00 a.m. on
Thursday, 9 July 2026 (Hong Kong time), it is expected that dealings in the H Shares on
the Stock Exchange will commence at 9: 00 a.m. on Thursday, 9 July 2026 (Hong Kong
time). The H Shares will be traded in board lots of 100 H Shares each, and the stock code
of the H Shares will be 00537.
By order of the Board
RIGOL Technologies Co., Ltd.
普源精電科技股份有限公司
Dr. Wang Yue
Chairman and Executive Director
Hong Kong, 8 July 2026
As of the date of this announcement, the executive Directors are Dr. Wang Yue, Mr. Wang
Ning, Dr. Sun Ningxiao and Mr. Cheng Jianchuan, and the independent non-executive
Directors are Dr. Qin Ce, Dr. Liu Liansheng and Ms. Xu Xu.
– 21 –
