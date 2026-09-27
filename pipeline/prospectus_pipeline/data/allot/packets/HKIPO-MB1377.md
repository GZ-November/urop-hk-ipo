# 配发结果公告抽取任务：1377.HK Guangdong Dtech Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**08/07/2026 22:52**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0708/2026070801372.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1377.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the ‘‘Stock Exchange’’, or the
‘‘Hong Kong Stock Exchange’’) and Hong Kong Securities Clearing Company Limited (‘‘HKSCC’’) take no responsibility
for the contents of this announcement, make no representation as to its accuracy or completeness and expressly disclaim
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of
this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States (including
its territories and possessions, any state of the United States and the District of Columbia). This announcement does not
constitute or form a part of any offer or solicitation to purchase or subscribe for securities in the United States or in any
other jurisdictions. The securities mentioned herein have not been, and will not be, registered under the United States
Securities Act of 1933 as amended from time to time (the ‘‘U.S. Securities Act’’) or securities law of any state or other
jurisdiction of the United States. The securities may not be offered, sold, pledged or otherwise transferred within the United
States except pursuant to an exemption from the registration requirements of the U.S. Securities Act and in compliance with
any applicable state securities laws. The securities are being offered and sold outside the United States in offshore
transactions in accordance with Regulation S under the U.S. Securities Act. There will be no public offer of securities in the
United States.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase or
subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated June
30, 2026 (the ‘‘Prospectus’’) issued by Guangdong Dtech Technology Co., Ltd. (廣東鼎泰高科技術股份有限公司) (the
‘‘Company’’) for detailed information about the Global Offering described below before deciding whether or not to invest
in the H Shares thereby being offered. Any investment decision in relation to the Offer Shares should be taken solely in
reliance on the information in the Prospectus. The Company has not been and will not be registered under the U.S.
Investment Company Act of 1940, as amended.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those
defined in the Prospectus.
Potential investors of the Offer Shares should note that the Joint Sponsor-Overall Coordinators (for themselves and on
behalf of the Overall Coordinators and the Hong Kong Underwriters) shall be entitled to terminate their obligations under
the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the
section headed ‘‘Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for
Termination’’ in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently
expected to be on Thursday, July 9, 2026).
– 1 –

<<<PAGE 2>>>
Guangdong Dtech Technology Co., Ltd.
廣東鼎泰高科技術股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the
Global Offering
:
12,632,000 H Shares
Number of Hong Kong Offer Shares
:
1,263,200 H Shares (including 126,300
Overseas Employee Reserved Shares)
Number of International Offer Shares
:
11,368,800 H Shares (including 1,136,800 PRC
Employee Reserved Shares)
Final Offer Price
:
HK$380.00 per H Share, plus brokerage of
1.0%, SFC transaction levy of 0.0027%,
Stock Exchange trading fee of 0.00565% and
AFRC transaction levy of 0.00015%
Nominal value
:
RMB1.00 per H Share
Stock code
:
1377
Joint Sponsors, Joint Sponsor-Overall Coordinators, Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
– 2 –

<<<PAGE 3>>>
Guangdong Dtech Technology Co., Ltd.
廣東鼎泰高科技術股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Warning: In view of high concentration of shareholding in a small number of Shareholders,
Shareholders and prospective investors should be aware that the price of the H Shares could
move substantially even with a small number of the H Shares traded and should exercise
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
1377
Stock short name
DTECH
Dealings commencement date
July 9, 2026*
*
see note at the end of the announcement
Price Information
Final Offer Price
HK$380.00
Maximum Offer Price
HK$380.00
Offer Shares and Share Capital
Number of Offer Shares
12,632,000
Final Number of Offer Shares in Hong Kong Public
OfferingNote 1
1,263,200
Final
Number
of
Offer
Shares
in
International
OfferingNote 2
11,368,800
Number of issued Shares upon Listing
424,044,934
Notes:
1.
Including 60,300 Overseas Employee Reserved Shares under the Overseas Employee Preferential Offering.
2.
Including 911,300 PRC Employee Reserved Shares under the PRC Employee Preferential Offering.
Offer Size Adjustment Option (Upsize option)
Number of additional shares issued under the option
N/A
— Hong Kong Public Offering
N/A
— International Offering
N/A
The Offer Size Adjustment Option was not exercised and has lapsed.
Proceeds
Gross proceeds (Note)
HK$4,800.2 million
Less: Estimated listing expenses payable based on final
Offer Price
HK$135.4 million
Net proceeds
HK$4,664.8 million
Note:
Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of
proceeds, please refer to the section headed ‘‘Future Plans and Use of Proceeds’’ of the Prospectus.
– 3 –

<<<PAGE 4>>>
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING (Excluding the Overseas Employee Preferential Offering)
No. of valid applications
118,991
No. of successful applications
11,516
Subscription level
354.64 times
Claw-back triggered
N/A
No. of Offer Shares excluding Overseas Employee Reserved Shares initially
available under the Hong Kong Public Offering
1,136,900
Final no. of Offer Shares excluding Overseas Employee Reserved Shares
under the Hong Kong Public Offering
1,202,900
% of Offer Shares excluding Overseas Employee Reserved Shares under the
Hong Kong Public Offering to the Global Offering
9.52%
Note:
For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to http://
www.hkeipo.hk/IPOResult to perform a search by identification number or http://www.hkeipo.hk/IPOResult for the
full list of allottees.
Overseas Employee Preferential Offering
No. of valid applications
6
Subscription level
0.48 times
No. of Overseas Employee Reserved Shares initially available under the
Overseas Employee Preferential Offering
126,300
Final
no.
of
Overseas
Employee
Reserved
Shares
under
the
Overseas
Employee Preferential Offering
60,300
Under-subscription
of
Overseas
Employee
Reserved
Shares
and
made
available to the Hong Kong Public Offering
66,000
Note:
The 66,000 under-subscribed Overseas Employee Reserved Shares were reallocated to the Hong Kong Public
Offering for subscription by the public in Hong Kong. For details of the final allocation of shares to the Overseas
Employee Preferential Offering, Overseas Eligible Employees can refer to http://www.hkeipo.hk/IPOResult to
perform a search by identification number or http://www.hkeipo.hk/IPOResult for the full list of allottees. For details
of the Overseas Employee Preferential Offering, please refer to the section headed ‘‘Structure of the Global Offering
— The Overseas Employee Preferential Offering’’ of the Prospectus and the section headed ‘‘Others/Additional
Information — Allocations under the Overseas Employee Preferential Offering’’ in this announcement.
– 4 –

<<<PAGE 5>>>
INTERNATIONAL OFFERING (Excluding the PRC Employee Preferential Offering)
No. of placees (excluding the PRC Employee Preferential Offering)
227
Subscription level (excluding the PRC Employee Reserved Shares under the
PRC Employee Preferential Offering)
24.50 times
No. of Offer Shares initially available under the International Offering
(excluding the PRC Employee Reserved Shares under the PRC Employee
Preferential Offering)
10,232,000
Final no. of Offer Shares under the International Offering (excluding the
PRC Employee Reserved Shares under the PRC Employee Preferential
Offering)
10,457,500
% of Offer Shares under the International Offering to the Global Offering
(excluding the PRC Employee Reserved Shares under the PRC Employee
Preferential Offering)
82.79%
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a waiver
from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) of
Appendix F1 to the Listing Rules (the ‘‘Placing Guidelines’’) granted by the Stock Exchange to permit
H Shares in the International Offering to be placed to certain Existing Minority Shareholders and/or
their close associates; (b) a consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing
Applicants to permit the Company to, among other things, allocate further H Shares in the
International Offering to certain existing Shareholders and Cornerstone Investors and/or their
respective close associates; and (c) a waiver from strict compliance with Rules 10.04 of the Listing
Rules, a consent under paragraph 1C(2) of the Placing Guidelines granted by the Stock Exchange to
permit the Company to allocate certain Offer Shares to the Existing Shareholder Employee Participants
on a preferential basis under the PRC Employee Preferential Offering, (i) none of the Offer Shares
subscribed by the placees and the public have been financed directly or indirectly by the Company, any
of the Directors, chief executive of the Company, Controlling Shareholders, substantial Shareholders,
existing Shareholders of the Company or any of its subsidiaries or their respective close associates;
and (ii) none of the placees and the public who have purchased the Offer Shares are accustomed to
taking instructions from the Company, any of the Directors, chief executive of the Company,
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company or any of its
subsidiaries or their respective close associates in relation to the acquisition, disposal, voting or other
disposition of H Shares registered in his/her/its name or otherwise held by him/her/it.
– 5 –

<<<PAGE 6>>>
PRC Employee Preferential Offering
No. of valid applications
1*
Subscription level
0.80 times
No. of PRC Employee Reserved Shares initially available under the PRC
Employee Preferential Offering
1,136,800
Final no. of PRC Employee Reserved Shares under the PRC Employee
Preferential Offering
911,300
Under-subscription of PRC Employee Reserved Shares and made available to
the International Offering
225,500
*
The number of PRC Eligible Employees participated in the PRC Employee Preferential Offering is 116.
For details of the PRC Employee Preferential Offering, please refer to the section headed ‘‘Structure of
the Global Offering — The PRC Employee Preferential Offering’’ of the Prospectus and the section
headed ‘‘Others/Additional Information — Allocations under the PRC Employee Preferential Offering’’
in this announcement.
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of Offer
Shares
allocated
% of total
issued H
Shares after
the Global
Offering
Note 1
% of total
issued share
capital after
the Global
Offering
Existing
shareholders
or their close
associates
Note 2
VICTORY GIANT TECHNOLOGY
HOLDINGS (HONG KONG)
LIMITEDNote 4
618,600
4.90%
0.15%
No
HHLR ADVISORS, LTD.
618,600
4.90%
0.15%
No
ASPEX MASTER FUND
618,600
4.90%
0.15%
No
KINGBOARD INVESTMENTS
LIMITED
412,400
3.26%
0.10%
No
CPE INVESTMENT XV LIMITED
412,400
3.26%
0.10%
No
CloudAlpha Capital Management
Limited
412,400
3.26%
0.10%
No
– 6 –

<<<PAGE 7>>>
Investor
No. of Offer
Shares
allocated
% of total
issued H
Shares after
the Global
Offering
Note 1
% of total
issued share
capital after
the Global
Offering
Existing
shareholders
or their close
associates
Note 2
E FUND
E FUND MANAGEMENT CO., LTD.
(‘‘E Fund Management’’)
103,100
0.82%
0.02%
Yes
E FUND MANAGEMENT (HONG
KONG) CO., LTD. (‘‘E Fund HK’’)
206,200
1.63%
0.05%
Yes
VERITION MULTI-STRATEGY
MASTER FUND LTD.
309,300
2.45%
0.07%
No
TAIKANG LIFE INSURANCE CO.,
LTD
206,200
1.63%
0.05%
Yes
ATHOS CAPITAL LIMITED
206,200
1.63%
0.05%
No
HEL VED MASTER FUND
206,200
1.63%
0.05%
No
Integrated Core Strategies (Asia) Pte.
Ltd. (‘‘Millennium ICSA’’)
206,200
1.63%
0.05%
No
IFUND SPC — Vision IX SP
206,200
1.63%
0.05%
No
BARING ASSET MANAGEMENT
(ASIA) LIMITED
164,900
1.31%
0.04%
No
Martis Fund, L.P.
164,900
1.31%
0.04%
No
DYNAMIC HOLDING CO., LTD.
164,100
1.30%
0.04%
No
Total
5,236,500
41.45%
1.23%
Notes:
1.
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued
under the Global Offering.
2.
Not taking into account any A Shares held by the relevant investors.
3.
In addition to the Offer Shares subscribed for as Cornerstone Investors, certain Cornerstone Investors and/or their
close associates were allocated further Offer Shares as placees in the International Offering. Please refer to the section
headed ‘‘Allotment Results Details — International Offering — Allottees with Waivers/Consents Obtained’’ in this
announcement for details. Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-up
restrictions as indicated below. For details, please refer to the section headed ‘‘Lock-up Undertakings — Cornerstone
Investors’’ in this announcement.
4.
Reference is made to the section headed ‘‘Cornerstone Investors’’ on page 246 of the Prospectus. The Company would
like to clarify that the Chinese name of Mr. He Lianqi, one of the ultimate beneficial owners of VICTORY GIANT
TECHNOLOGY HOLDINGS (HONG KONG) LIMITED, is 何連琪.
– 7 –

<<<PAGE 8>>>
Allottees with Waivers/Consents Obtained
Investor
No. of
Offer
Shares
allocated
% of total
issued H
Shares after
the Global
Offering
Note 1
% of total
issued share
capital after
the Global
Offering
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by Existing Minority
Shareholders holding more than 1% of the issued share capital of the Company immediately prior to the
completion of the Global Offering and/or their close associates
E Fund HK
206,200
1.63%
0.05%
A cornerstone investor
and a close associate
of an existing
Shareholder
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in
relation to allocations of further H Shares to existing Shareholders and Cornerstone Investors and/or their
close associatesNote 2
TAIKANG LIFE INSURANCE CO.,
LTD
20,600
0.16%
0.005%
Same entity as the
Cornerstone Investor
E Fund Management
10,300
0.08%
0.002%
Same entity as the
Cornerstone Investor
E Fund HK
20,600
0.16%
0.005%
Same entity as the
Cornerstone Investor
Ms. Liu Chunlan
205,200
1.62%
0.05%
Ms. Liu Chunlan, who
is a director of
VICTORY GIANT
TECHNOLOGY
HOLDINGS (HONG
KONG) LIMITED, a
cornerstone investor.
HHLR Advisors, Ltd.
185,500
1.47%
0.04%
Same entity as the
Cornerstone Investor
Aspex Master Fund
185,500
1.47%
0.04%
Same entity as the
Cornerstone Investor
– 8 –

<<<PAGE 9>>>
Investor
No. of
Offer
Shares
allocated
% of total
issued H
Shares after
the Global
Offering
Note 1
% of total
issued share
capital after
the Global
Offering
Relationship
KINGBOARD INVESTMENTS
LIMITED
103,100
0.82%
0.02%
Same entity as the
Cornerstone Investor
CPE INVESTMENT XV LIMITED
123,700
0.98%
0.03%
Same entity as the
Cornerstone Investor
CloudAlpha Capital Management
Limited
103,100
0.82%
0.02%
Same entity as the
Cornerstone Investor
VERITION MULTI-STRATEGY
MASTER FUND LTD.
30,900
0.24%
0.01%
Same entity as the
Cornerstone Investor
HEL VED MASTER FUND
20,900
0.17%
0.005%
Same entity as the
Cornerstone Investor
Athos Capital Limited
20,900
0.17%
0.005%
Same entity as the
Cornerstone Investor
Millennium ICSA
20,900
0.17%
0.005%
Same entity as the
Cornerstone Investor
DYNAMIC HOLDING CO., LTD
20,800
0.16%
0.005%
Same entity as the
Cornerstone Investor
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for
New Listing Applicants in relation to allocations to connected clientsNote 3
CITIC Securities International Capital
Management Limited (‘‘CSICM’’)
400
0.003%
0.0001%
Connected client as a
placee
CITIC Securities Asset Management
Company Limited (‘‘CITICS AM’’)
400
0.003%
0.0001%
Connected client as a
placee
CITIC Securities Asset Management
(HK) Limited (‘‘CITICS AM HK’’)
400
0.003%
0.0001%
Connected client as a
placee
China Asset Management (Hong
Kong) Limited (‘‘China AMC HK’’)
400
0.003%
0.0001%
Connected client as a
placee
– 9 –

<<<PAGE 10>>>
Investor
No. of
Offer
Shares
allocated
% of total
issued H
Shares after
the Global
Offering
Note 1
% of total
issued share
capital after
the Global
Offering
Relationship
CITIC-Prudential Fund Management
Company Ltd.
(‘‘CITIC-Prudential’’)
1,000
0.008%
0.0002%
Connected client as a
placee
China Southern Asset Management
Co., Ltd. (‘‘CSAM’’)
400
0.003%
0.0001%
Connected client as a
placee
HSBC Global Asset Management
(Hong Kong) Limited
(‘‘HSBC AM’’)
1,000
0.008%
0.0002%
Connected client as a
placee
Huatai Capital Investment Limited
(‘‘HTCI’’)Note 5
303,100
2.40%
0.07%
Connected client as a
placee
E Fund Management
113,400
0.90%
0.03%
Connected client as a
cornerstone investor
and a placee
E Fund HK
226,800
1.80%
0.05%
Connected client as a
cornerstone investor
and a placee
Allottees with waiver from strict compliance with Rules 10.03, and 10.04 of the Listing Rules and consent
under paragraph 1C(2) of the Placing Guidelines in relation to allocations to the Existing Shareholder
Employee Participants under the Employee Preferential Offering Note 4
Existing Shareholder Employee
Participants
911,300
7.21%
0.21%
Eligible Employees
– 10 –

<<<PAGE 11>>>
Notes:
1.
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued
under the Global Offering.
2.
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the number of
Offer Shares allocated to the investors as placees in the International Offering. For allocations of Offer Shares to the
relevant investors and/or their close associates as Cornerstone Investors, please refer to the section headed ‘‘Allotment
Results Details — International Offering — Cornerstone Investors’’ in this announcement. For details of the consent
under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further H
Shares to the existing Shareholders and Cornerstone Investors and/or their close associates, please refer to the section
headed ‘‘Others/Additional Information — Allocations of Offer Shares to the existing Shareholders and Cornerstone
Investors and/or their close associates with a consent under paragraph 18 of Chapter 4.15 of the Guide for New
Listing Applicants’’ in this announcement.
3.
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New
Listing Applicants in relation to allocations to connected clients, please refer to the sections headed ‘‘Others/
Additional Information — Placing to connected clients with a consent under paragraph 1C(1) of the Placing
Guidelines’’ and ‘‘Others/Additional Information — Allocations of Offer Shares to the existing Shareholders and the
Cornerstone Investors and/or their close associates with a consent under paragraph 18 of Chapter 4.15 of the Guide for
New Listing Applicants’’ in this announcement.
4.
For details of the waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under Paragraph
1C(2) of the Placing Guidelines in relation to allocations to Existing Shareholder Employee Participants and the
Employee Preferential Offering, please refer to the sections headed ‘‘Waivers from strict compliance with the Listing
Rules — Waiver and Consent in Respect of Allocations to Existing Shareholder Employee Participants’’ and
‘‘Structure of the Global Offering — Employee Preferential Offering’’ of the Prospectus. For details of the allocations
under the Employee Preferential Offering, please refer to the section headed ‘‘Others/Additional Information —
Allocations under the Employee Preferential Offering’’ in this announcement.
5.
Under applicable PRC laws, PRC investors were not permitted to directly participate in initial public offerings (IPOs)
in Hong Kong. Instead, they invested through licensed domestic securities firms approved to undertake cross-border
derivatives trading under the Cross-border Derivatives Trading Regime. These securities firms, through their Hong
Kong affiliates, participated in Hong Kong IPOs as placees or cornerstone investors. Huatai Securities Co., Ltd.
(Huatai Securities), whose shares were listed on both the Shanghai Stock Exchange (601688) and the Hong Kong
Stock Exchange (6886), was one such licensed firm. Huatai Securities entered into an International Swaps and
Derivatives Association agreement (the ISDA Agreement) with its wholly owned Hong Kong subsidiary Huatai
International Company Limited (HTCI) to govern total return swap (TRS) transactions for the purpose of providing
investment exposure to its onshore clients.
In connection with the Global Offering, Huatai Financial Holdings (Hong Kong) Limited (HTFH), another wholly
owned subsidiary of Huatai Securities, acted as one of the Overall Coordinators and Underwriters. Pursuant to the
ISDA Agreement, HTCI subscribed for a total of 253,100 Offer Shares as a placee under a back-to-back total return
swap (Huatai Back-to-back TRS) entered into with Huatai Securities. This transaction corresponded to fully funded
Client TRS arrangements placed by Huatai’s onshore clients (the Huatai Onshore Ultimate Clients) with Huatai
Securities.
– 11 –

<<<PAGE 12>>>
All economic interests in the 253,100 Offer Shares were fully passed through by HTCI to the Huatai Onshore Ultimate
Clients, while HTCI bore no economic gain or loss. Each of the Huatai Onshore Ultimate Clients was, to the best of
HTCI’s knowledge after making all reasonable enquiries, an independent third party of (i) the Company and its
connected persons, and (ii) HTCI, HTFH, and their respective group companies. One of the participating onshore
clients was Roadshow Xunlu No. 90 Private Equity Investment Fund, managed by Qingdao Roadshow Investment
Management Co., Ltd., ultimately controlled by Yao Bo. No ultimate beneficial owner held 30 percent or more interest
in the fund.
The structure of the Huatai Back-to-back TRS and Client TRS operated similarly to a Qualified Domestic Institutional
Investor (QDII) arrangement, under which all economic returns and losses of the underlying Offer Shares were borne
solely by the Huatai Onshore Ultimate Clients, including the effect of foreign exchange fluctuations upon TRS
settlement. Separately, HTCI also subscribed for 50,000 H Shares under the International Offering corresponding to
Client TRS transactions placed directly by offshore clients (the Huatai Offshore Ultimate Clients). To hedge its
exposure under these offshore TRS arrangements, HTCI subscribed for and held the 50,000 H Shares through HTFH.
The full economic exposure, including all returns and losses, was passed to the Huatai Offshore Ultimate Clients,
while HTCI again assumed no economic exposure.
The Huatai Offshore Ultimate Clients were, to the best of HTCI’s knowledge, independent third parties to both the
Company and the Huatai group entities. During the life of the respective TRS agreements, HTCI held legal title and
voting rights to the Offer Shares and H Shares but did not exercise any voting rights. The shares were held in HTCI’s
custodian or prime brokerage accounts. In line with market practice, HTCI lent out part or all of its holdings as stock
borrowing loans to lower financing costs but retained the ability to recall the shares at any time to meet its TRS
settlement obligations.
A total of 303,100 Offer Shares, comprising 253,100 linked to the onshore TRS arrangements and 50,000 linked to the
offshore TRS arrangements, were allocated to HTCI as a connected client under the International Offering. These
shares were held solely for hedging purposes under the Huatai Back-to-back TRS and Client TRS structures, with all
economic exposure ultimately borne by the Huatai Onshore and Offshore Ultimate Clients.
– 12 –

<<<PAGE 13>>>
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number and
description of
Shares held in
the Company
subject to lock-
up undertakings
upon Listing
% of total issued
H Shares after
the Global
Offering subject
to lock-up
undertakings
Note 1
% of
shareholding in
the Company
subject to
lock-up
undertakings
Last day subject to the lock-
up undertakings
Ms. WANG Xin
328,690,677
A-Shares
—
77.51%
January 8, 2027 (First Six-
month Period)Note 2
July 8, 2027 (Second Six-
month Period)Note 3
Mr. WANG Junfeng
328,690,677
A-Shares
—
77.51%
January 8, 2027 (First Six-
month Period)Note 2
July 8, 2027 (Second Six-
month Period)Note 3
Mr. WANG Xuefeng
328,690,677
A-Shares
—
77.51%
January 8, 2027 (First Six-
month Period)Note 2
July 8, 2027 (Second Six-
month Period)Note 3
Mr. LIN Xia
328,690,677
A-Shares
—
77.51%
January 8, 2027 (First Six-
month Period)Note 2
July 8, 2027 (Second Six-
month Period)Note 3
Guangdong Taiding
Holdings Co., Ltd.
(‘‘Taiding Holdings’’)
312,552,000
A-Shares
—
73.71%
January 8, 2027 (First Six-
month Period)Note 2
July 8, 2027 (Second Six-
month Period)Note 3
Zhejiang Taiding Venture
Capital Partnership
Enterprise (Limited
Partnership) (‘‘Zhejiang
Taiding’’)
13,222,677
A-Shares
—
3.12%
January 8, 2027 (First Six-
month Period)Note 2
July 8, 2027 (Second Six-
month Period)Note 3
Taizhou Ruihe Electronic
Products Consulting
Center (Limited
Partnership) (‘‘Taizhou
Ruihe’’)
2,916,000
A-Shares
—
0.69%
January 8, 2027 (First Six-
month Period)Note 2
July 8, 2027 (Second Six-
month Period)Note 3
– 13 –

<<<PAGE 14>>>
Notes:
1.
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued
under the Global Offering.
2.
The Controlling Shareholders may dispose of or transfer Shares after the indicated date provided that each Controlling
Shareholder will not cease to be a Controlling Shareholder.
3.
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after the indicated
date.
– 14 –

<<<PAGE 15>>>
Cornerstone Investors
Name
Number and
description of
Shares held in
the Company
subject to lock-
up undertakings
upon Listing
% of total
issued H Shares
after the Global
Offering subject
to lock-up
undertakings
Note 1
% of
shareholding in
the Company
subject
to lock-up
undertakings
Last day subject
to the lock-up
undertakings
Note 2
VICTORY GIANT
TECHNOLOGY HOLDINGS
(HONG KONG) LIMITED
618,600
4.90%
0.15%
January 8, 2027
HHLR ADVISORS, LTD.
618,600
4.90%
0.15%
January 8, 2027
ASPEX MASTER FUND
618,600
4.90%
0.15%
January 8, 2027
KINGBOARD INVESTMENTS
LIMITED
412,400
3.26%
0.10%
January 8, 2027
CPE INVESTMENT XV
LIMITED
412,400
3.26%
0.10%
January 8, 2027
CloudAlpha Capital Management
Limited
412,400
3.26%
0.10%
January 8, 2027
E FUND
E FUND MANAGEMENT CO.,
LTD.
103,100
0.82%
0.02%
January 8, 2027
E FUND MANAGEMENT
(HONG KONG) CO., LTD.
206,200
1.63%
0.05%
January 8, 2027
VERITION MULTI-STRATEGY
MASTER FUND LTD.
309,300
2.45%
0.07%
January 8, 2027
TAIKANG LIFE INSURANCE
CO., LTD
206,200
1.63%
0.05%
January 8, 2027
ATHOS CAPITAL LIMITED
206,200
1.63%
0.05%
January 8, 2027
HEL VED MASTER FUND
206,200
1.63%
0.05%
January 8, 2027
Millennium ICSA
206,200
1.63%
0.05%
January 8, 2027
IFUND SPC — Vision IX SP
206,200
1.63%
0.05%
January 8, 2027
BARING ASSET MANAGEMENT
(ASIA) LIMITED
164,900
1.31%
0.04%
January 8, 2027
Martis Fund, L.P.
164,900
1.31%
0.04%
January 8, 2027
DYNAMIC HOLDING CO., LTD.
164,100
1.30%
0.04%
January 8, 2027
Total
5,236,500
41.45%
1.23%
– 15 –

<<<PAGE 16>>>
Notes:
1.
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued
under the Global Offering.
2.
In accordance with the relevant cornerstone investment agreements, the required lock-up periods will end on January
8, 2027. The Cornerstone Investors will cease to be prohibited from disposing of or transferring the H Shares
subscribed for pursuant to the relevant cornerstone investment agreements after the indicated date.
PLACEE CONCENTRATION ANALYSIS
Places*
Number of
H Shares
allotted
Allotment
as % of the
International
Offering**
Allotment
as % of total
Offer Shares
Number of
H Shares held
upon Listing
% of total
issued share
capital upon
Listing
Top 1
823,800
7.25%
6.52%
823,800
0.19%
Top 5
3,710,300
32.64%
29.37%
3,710,300
0.87%
Top 10
5,957,800
52.40%
47.16%
15,890,204
3.75%
Top 25
9,344,200
82.19%
73.97%
20,452,204
4.82%
Notes:
*
Ranking of placees is based on the number of H Shares allotted to the placees.
**
The International Offering includes the PRC Employee Preferential Offering.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number of
H Shares
allotted
Allotment
as % of the
International
Offering**
Allotment
as % of total
Offer Shares
Number of
H Shares held
upon Listing
% of total
issued share
capital upon
Listing
Top 1
823,800
7.25%
6.52%
823,800
0.19%
Top 5
3,710,300
32.64%
29.37%
3,710,300
0.87%
Top 10
5,957,800
52.40%
47.16%
15,890,204
3.75%
Top 25
9,344,200
82.19%
73.97%
20,452,204
4.82%
Notes:
*
Ranking of H Shareholders is based on the number of H Shares held by the Shareholders upon Listing.
**
The International Offering includes the PRC Employee Preferential Offering.
– 16 –

<<<PAGE 17>>>
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders*
Number of
H Shares
allotted
Allotment as
% of the
International
Offering**
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
0
0.00%
0.00%
0
328,690,677
77.51%
Top 5
340,200
2.99%
2.69%
340,200
355,844,358
83.92%
Top 10
342,600
3.01%
2.71%
342,600
368,681,847
86.94%
Top 25
4,818,400
42.38%
38.14%
4,818,400
381,116,237
89.88%
Notes:
*
Ranking of Shareholders is based on the number of Shares held by the Shareholders upon Listing.
**
The International Offering includes the PRC Employee Preferential Offering.
– 17 –

<<<PAGE 18>>>
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by the
public will be conditionally allocated on the basis set out below:
Number
of H Shares
applied for
Number of
valid applications
Basis of allocation/ballot
Approximate
percentage
allotted of the
total number of
H Shares
applied for
Pool A
100
69,534
2,087 out of 69,534 applicants to receive 100 H Shares
3.00%
200
9,557
380 out of 9,557 applicants to receive 100 H Shares
1.99%
300
2,315
109 out of 2,315 applicants to receive 100 H Shares
1.57%
400
1,304
69 out of 1,304 applicants to receive 100 H Shares
1.32%
500
1,508
87 out of 1,508 applicants to receive 100 H Shares
1.15%
600
892
56 out of 892 applicants to receive 100 H Shares
1.05%
700
580
39 out of 580 applicants to receive 100 H Shares
0.96%
800
715
50 out of 715 applicants to receive 100 H Shares
0.87%
900
544
40 out of 544 applicants to receive 100 H Shares
0.82%
1,000
6,467
495 out of 6,467 applicants to receive 100 H Shares
0.77%
1,500
2,169
196 out of 2,169 applicants to receive 100 H Shares
0.60%
2,000
1,964
200 out of 1,964 applicants to receive 100 H Shares
0.51%
2,500
1,305
145 out of 1,305 applicants to receive 100 H Shares
0.44%
3,000
1,477
177 out of 1,477 applicants to receive 100 H Shares
0.40%
3,500
803
103 out of 803 applicants to receive 100 H Shares
0.37%
4,000
928
125 out of 928 applicants to receive 100 H Shares
0.34%
4,500
517
73 out of 517 applicants to receive 100 H Shares
0.31%
5,000
1,335
197 out of 1,335 applicants to receive 100 H Shares
0.30%
6,000
801
127 out of 801 applicants to receive 100 H Shares
0.26%
7,000
683
116 out of 683 applicants to receive 100 H Shares
0.24%
8,000
750
134 out of 750 applicants to receive 100 H Shares
0.22%
9,000
449
84 out of 449 applicants to receive 100 H Shares
0.21%
10,000
4,748
926 out of 4,748 applicants to receive 100 H Shares
0.20%
Total
111,345
Total number of Pool A successful applicants: 6,015
– 18 –

<<<PAGE 19>>>
Number
of H Shares
applied for
Number of
valid applications
Basis of allocation/ballot
Approximate
percentage
allotted of the
total number of
H Shares
applied for
Pool B
20,000
4,583
2,750 out of 4,583 applicants to receive 100 H Shares
0.30%
30,000
1,106
863 out of 1,106 applicants to receive 100 H Shares
0.26%
40,000
601
532 out of 601 applicants to receive 100 H Shares
0.22%
50,000
381
100 H Shares
0.20%
60,000
216
100 H Shares plus 24 out of 216 applicants to receive an
additional 100 H Shares
0.19%
70,000
155
100 H Shares plus 33 out of 155 applicants to receive an
additional 100 H Shares
0.17%
80,000
109
100 H Shares plus 33 out of 109 applicants to receive an
additional 100 H Shares
0.16%
90,000
57
100 H Shares plus 23 out of 57 applicants to receive an
additional 100 H Shares
0.16%
100,000
268
100 H Shares plus 128 out of 268 applicants to receive an
additional 100 H Shares
0.15%
200,000
92
200 H Shares
0.10%
300,000
22
200 H Shares plus 17 out of 22 applicants to receive an
additional 100 H Shares
0.09%
400,000
10
300 H Shares
0.08%
500,000
17
300 H Shares plus 9 out of 17 applicants to receive an
additional 100 H Shares
0.07%
568,400
29
300 H Shares plus 20 out of 29 applicants to receive an
additional 100 H Shares
0.06%
Total
7,646
Total number of Pool B successful applicants: 5,501
– 19 –

<<<PAGE 20>>>
BASIS OF ALLOCATION UNDER THE OVERSEAS EMPLOYEE PREFERENTIAL OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 6 valid applications via
HK eIPO Pink Form service will be conditionally allocated on the basis set out below. No preferential
treatment was given to any of the Overseas Eligible Employees in the allocation of the Shares applied
for by them under the Overseas Employee Preferential Offering and such allocation of Shares under the
Overseas Employee Preferential Offering was made in accordance with the allocation basis described in
the Prospectus. The 60,300 Overseas Employees Reserved Shares validly applied for will be allocated
to Overseas Eligible Employees who have applied pursuant to the Overseas Employee Preferential
Offering. The 66,000 under-subscribed Overseas Employee Reserved Shares were reallocated to the
Hong Kong Public Offering for subscription by the public in Hong Kong.
Number of Overseas
Employee
Reserved Shares
Applied For
Number of
Valid
Overseas
Employee
Applications
Total Number
of Overseas
Employee
Reserved Shares
Applied For Basis of Allotment
Total Number
of Overseas
Employee
Reserved Shares
Allotted
Approximately
percentage of
allocation based on
the total number of
Overseas Employee
Reserved Shares
applied for in this
category
5,200
2
10,400 Allot Overseas Employee
Reserved Shares applied
for in full
10,400
100.00%
7,800
1
7,800 Allot Overseas Employee
Reserved Shares applied
for in full
7,800
100.00%
10,900
1
10,900 Allot Overseas Employee
Reserved Shares applied
for in full
10,900
100.00%
15,600
2
31,200 Allot Overseas Employee
Reserved Shares applied
for in full
31,200
100.00%
6
60,300
60,300
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of
which consent has been obtained, the Company has complied with the Listing Rules and guidance
materials in relation to the placing, allotment and listing of the H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by
them is the same as the final Offer Price in addition to any brokerage, AFRC transaction levy, SFC
transaction levy and trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Offer Size Adjustment Option
The Offer Size Adjustment Option was not exercised and has lapsed.
– 20 –

<<<PAGE 21>>>
Allocation of H Shares to Existing Minority Shareholders and their close associates
The Company has applied for, and the Stock Exchange has granted, a waiver from strict compliance
with Rule 10.04 of, and a consent under paragraph 1C(2) of Appendix F1 to, the Listing Rules to
permit H Shares in the International Offering to be placed to certain existing minority Shareholders
who (i) hold less than 5% of the total number of A Shares in issue of the Company prior to the
completion of the Global Offering and (ii) are not and will not become (upon the completion of the
Global Offering) core connected persons of the Company or the close associates of any such core
connected person (together, the ‘‘Existing Minority Shareholders’’), on the following conditions:
(i)
each Existing Minority Shareholder to whom the Company may allocate the H Shares in the
International Offering holds less than 5% of the total number of A Shares in issue of the Company
before Listing;
(ii) each Existing Minority Shareholder is not, and will not be, a core connected person of the
Company or any close associate of any such core connected person immediately prior to or
following the Global Offering;
(iii) none of the Existing Minority Shareholders have the right to appoint a Director and/or have any
other special rights;
(iv) allocation to the Existing Minority Shareholders or their close associates will not affect the ability
of the Company to satisfy the public float requirement as prescribed by the Stock Exchange under
Rule 8.08 of the Listing Rules or otherwise approved by the Stock Exchange;
(v) each of the Joint Sponsors confirms or will confirm to the Stock Exchange in writing that based on
(i) its discussions with the Company and the Overall Coordinators; and (ii) the confirmations
provided to the Stock Exchange by the Company and each of the Overall Coordinators
(confirmations (vi) and (vii) mentioned below), and to the best of its knowledge and belief, it has
no reason to believe that any of the Existing Minority Shareholders or their close associates
received any preferential treatment, or is in a position to exert influence on the Company to obtain
actual or perceived preferential treatment in the allocation either as a cornerstone investor or as a
placee by virtue of their relationship with the Company other than the preferential treatment of
assured entitlement under a cornerstone investment following the principles set out in Chapter 4.15
of the Guide and details of allocation to the Existing Minority Shareholders and/or their close
associates holding more than 1% of the issued share capital of the Company immediately prior to
the completion of the Global Offering will be disclosed in this prospectus (for cornerstone
investors) and/or allotment results announcement (for both cornerstone investors and placees) of
the Company;
– 21 –

<<<PAGE 22>>>
(vi) the Company confirms or will confirm to the Stock Exchange in writing that:
(a)
in the case of participation as cornerstone investors, no preferential treatment has been, nor
will be, given to the Existing Minority Shareholders or their close associates by virtue of their
relationship with the Company, other than the preferential treatment of assured entitlement
under a cornerstone investment following the principles set out in Chapter 4.15 of the Guide,
nor is the Existing Minority Shareholder in a position to exert influence on the Company to
obtain actual or perceived preferential treatment, and the Existing Minority Shareholders or
their close associates’ cornerstone investment agreements do not contain any material terms
which are more favorable to the Existing Minority Shareholders or their close associates than
those in other cornerstone investment agreements; or
(b) in the case of participation as placees, no preferential treatment has been, nor will be, given to
the Existing Minority Shareholders or their close associates, nor is the Existing Minority
Shareholder in a position to exert influence on the Company to obtain actual or perceived
preferential treatment, by virtue of their relationship with the Company in any allocation in
the placing tranche;
(vii) in the case of participation as placees, each of the Overall Coordinators will confirm to the Stock
Exchange that, to the best of its knowledge and belief, no preferential treatment has been, nor will
be, given to the Existing Minority Shareholders or their close associates by virtue of their
relationship with the Company in any allocation in the placing tranche.
Please refer to the section headed ‘‘Waivers from strict compliance with the Listing Rules — Allocation
of H Shares to Existing Minority Shareholders and Their Close Associates’’ in the Prospectus for
further details of the waiver and consent. The allocation of Offer Shares to such Existing Minority
Shareholders is in compliance with all the conditions under the waiver/ consent granted by the Stock
Exchange.
Allocations of Offer Shares to existing Shareholders and Cornerstone Investors and/or their close
associates with a consent under Chapter 4.15 of the Guide for New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 of the
Guide for New Listing Applicants to permit the Company to allocate further Offer Shares in the
International Offering to certain existing Shareholders and Cornerstone Investors and/or their close
associates as placees, subject to the following conditions (the ‘‘Allocation to Size-based Exemption
Participants’’):
(a)
the final offering size of the Global Offering, excluding any over-allocation, will be of a total
value of at least HK$1 billion;
(b) the Offer Shares allocated to all existing Shareholders (whether as Cornerstone Investors and/or as
placees) as permitted under this exemption do not exceed 30% of the total number of Offer Shares
offered under the Global Offering;
– 22 –

<<<PAGE 23>>>
(c)
the Allocation to Size-based Exemption Participants will not affect the Company’s ability to satisfy
its public float requirement under Rule 8.08(1) (as amended and replaced by Rule 19A.13A) of the
Listing Rules;
(d) each of the Directors and chief executive of the Company confirms that no securities have been
allocated to them or their respective close associates under this exemption; and
(e)
details of the Cornerstone Investors and/or their close associates under this exemption will be
disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted by
the Stock Exchange.
For details of the allocations of Offer Shares to Cornerstone Investors, please refer to the section
headed ‘‘Allotment Results Details — International Offering — Allottees with Waivers/Consents
Obtained’’ in this announcement.
Placing to connected clients with a consent under paragraph 1C(1) of the Placing Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a consent
under paragraph 1C(1) of the Placing Guidelines to permit each of E Fund HK and E Fund
Management to participate in the Global Offering as a cornerstone investor. For details of the consent
granted, please refer to ‘‘Waivers from strict compliance with the Listing Rules — Consent in respect
of the proposed subscription of H Shares by certain cornerstone investors who are connected clients’’ in
the Prospectus.
In addition, under the International Offering, certain Offer Shares were placed to connected clients of
their connected distributors pursuant to the Placing Guidelines as placees. Please refer to the section
headed ‘‘Allotment Results Details — International Offering — Allottees with Waivers/Consents
Obtained’’ in this announcement for details. The Company has applied to the Stock Exchange for, and
the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing Guidelines to permit
the Company to allocate such Offer Shares in the International Offering to the connected clients as
placees. The allocation of Offer Shares to such connected clients is in compliance with all the
conditions under the consent granted by the Stock Exchange. Details of the placement to connected
clients as placees are set out below:
– 23 –

<<<PAGE 24>>>
Part A – Connected Client Holding the Beneficial Interest of the Offer Shares on a Non-discretionary Basis on Behalf of Independent Third Parties 
No.  
Connected Distributor  
Connected Client  
Relationship  
Whether the Connected 
Client is a collective 
investment scheme 
which is not authorised 
by the SFC or is 
expected to hold the 
Offer Shares on behalf 
of such scheme  
Amount of Offer Shares 
to be allocated to the 
Connected Client  
Approximate percentage 
of total number of Offer 
Shares under the Global 
Offering  
Approximate percentage 
of total issued share 
capital after the Global 
Offering  
1. 
CLSA 
CSICM (Note 1) 
CSICM is a member 
of the same group of 
companies as CLSA. 
No 
400 
0.003% 
0.0001% 
2. 
HTFH 
HTCI 
HTCI and HTFH are 
group companies 
with the same group 
No 
Huatai Onshore 
Ultimate Clients: 
253,100 (Note 2) 
2.40% 
0.07% 
Huatai Offshore 
Ultimate Clients: 
50,000 (Note 3) 
Note: 
1.
CSICM  will  act  as  the  single  counterparty  of  a  back-to-back  total  return  swap  transaction  (the  “CSICM Back-to-back  TRS”)  to  be  entered  into  by
CSICM  in  connection  with  a  total  return  swap  order  (the  “CSICM Client  TRS”)  placed  by  its  ultimate  clients  (the  “CSICM  Ultimate  Clients”),  by
which  CSICM  will  pass  the full  economic  exposure  of  the  Offer  Shares  placed  to  CSICM  (the  “CSICM  Offer  Shares”)  to  the  CSICM Ultimate  Client,
meaning  in  effect,  CSICM  will  hold  the  beneficial  interest  of  the  CSICM  Offer  Shares  on behalf  of  the  CSICM  Ultimate  Clients  on  a  non-discretionary
basis.  CSICM  will  hold  the  legal  title  and beneficial  interest  in  the  CSICM  Offer  Shares,  but  will  contractually  agree  to  pass  on  the  full  economic
exposure  and  return  of  the  CSICM  Offer  Shares  to  the  CSICM  Ultimate  Clients.  The  CSICM  Ultimate  Clients may  exercise  an  early  termination  right
to  early  terminate  the  CSICM  Client  TRS  at  any  time  from  the  trade date of the CSICM Client TRS which should be on or after the date on which the CSICM
Offer Shares are listed on  the  Stock  Exchange.  Upon  the  final  maturity  or  early  termination  of  the  CSICM  Client  TRS  by  the  CSICM Ultimate  Clients,
CSICM  will  dispose  of  the  CSICM  Offer  Shares  on  the  secondary  market  and  the  CSICM Ultimate  Clients  will  receive  a  final  termination  amount  of
the  CSICM  Back-to-back  TRS  which  should  have taken  into  account  all  the  economic  returns  or  economic  loss  in  relation  to  the  CSICM  Offer  Shares
and  the fixed  amount  of  transaction  fees  of  the  CSICM  Back-to  back  TRS  and  the  CSICM  Client  TRS.  CSICM  will  not exercise  the  voting  right  of
24

<<<PAGE 25>>>
the  CSICM  Offer  Shares  during  the  tenor  of  the  CSICM  Back-to-back  TRS.   
 
 
The details of the CSI Ultimate Clients are as follows: 
 
 
Name of CSI Ultimate Client 
Limited Partner/ Shareholding 
holding 30% or more in the CSI 
Ultimate Clients 
Fund Manager/ General Partner 
Ultimate beneficial owners of 
Fund 
Manager 
/ 
General 
Partner 
Hover4pi Fund I OFC 
N/A 
Hover4pi Capital 
He Hui 
 
 
To  the  best  of  CSICM’s  knowledge, after  making  all  reasonable  inquiries,  each  of  the  CSICM  Ultimate  Clients  and  its  ultimate  beneficial  owner is  a  
third  party  independent  from  CSICM,  CLSA  and  the  companies  which  are  members  of  the  same  group  of companies as CLSA. 
 
2. 
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public offerings (“IPOs”) in Hong Kong. However, PRC investors 
are permitted to invest in products issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. In connection with 
such products, the licensed domestic securities firms, through their Hong Kong affiliates, may participate in Hong Kong IPOs either as placees or cornerstone investors 
(the “Cross-border Derivatives Trading Regime”). 
 
Huatai Securities Co., Ltd (“Huatai Securities”), the shares of which are listed on both the Shanghai Stock Exchange (stock code: 601688) and the Stock Exchange 
(stock code: 6886), is one of the domestic securities firms licensed to undertake cross-border derivatives trading activities. Huatai Securities entered into an 
International Swaps and Derivatives Association agreement (the “ISDA Agreement”) with its indirectly wholly-owned subsidiary, HTCI to set out the principal terms 
of any future total return swap between Huatai Securities and HTCI. 
 
HTFH is one of the Overall Coordinators and Underwriters in connection with the Global Offering. Pursuant to the ISDA agreement, HTCI, which intends to participate 
in the Global Offering as a placee, will hold the beneficial interest of the Offer Shares on a non-discretionary basis as the single underlying holding under a back-to-
back total return swap (“Huatai Back-to-back TRS”) to be entered by HTCI in connection with a Client TRS (as defined below) placed by and fully funded (i.e., 
with no financing provided by HTCI) by Huatai Onshore Ultimate Clients (as defined below), by which, HTCI will, subject to customary fees and commissions, pass 
the full economic exposure of the Offer Shares ultimately to the Huatai Onshore Ultimate Clients, which in effect, HTCI will hold the beneficial interest of the Offer 
Shares on behalf of the Huatai Onshore Ultimate Clients. 
 
HTCI and HTFH are both indirectly wholly-owned subsidiaries of Huatai Securities. Accordingly, HTCI is considered as a “connected client” of HTFH pursuant to 
paragraph 1B(7) of the Placing Guidelines. 
 
25

<<<PAGE 26>>>
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the “Huatai Onshore Ultimate Clients”) cannot directly subscribe for the Offer 
Shares but may invest in derivative products issued by domestic securities firms licenced to undertake cross-border derivatives trading activities, such as Huatai 
Securities, with the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, the Huatai Onshore Ultimate Clients, through their 
investment managers, will place a total return swap order (the “Client TRS”) with Huatai Securities in connection with the Global Offering and Huatai Securities will 
place a Huatai Back-to-back TRS order to HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the Huatai Back-to-back TRS, HTCI 
participates in the Global Offering and subscribes the Offer Shares through placing order with HTFH during the International Offering.  
 
To the best of HTCI’s knowledge and after making all reasonable enquiries, each of the Huatai Onshore Ultimate Clients is an independent third party of (i) the 
Company, the connected person and/or their respective associates thereof, and (ii) HTCI, HTFH and the companies which are members of the same group of HTCI.  
 
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Huatai Back-to-back TRS in connection with the Client TRS order placed by the Huatai 
Onshore Ultimate Clients. Pursuant to the terms of the contracts of the Huatai Back-to-back TRS and the Client TRS, during the tenor of the Huatai Back-to-back 
TRS and the Client TRS, subject to customary fees and commissions, all economic returns of the Offer Shares will be ultimately passed to the Huatai Onshore Ultimate 
Clients through the Huatai Back-to-back TRS and the Client TRS and all economic loss shall be ultimately borne by the Huatai Onshore Ultimate Clients. HTCI will 
not take any economic return or bear any economic loss in relation to the Offer Shares. 
 
Investment in the Huatai Back-to-back TRS and the Client TRS is similar to the investment in a qualified domestic institutional investor fund (“QDII”) in the way that 
the Huatai Onshore Ultimate Clients would reap all the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through the exchange 
rate exposure on both the notional value of the investment and the profit and loss of the investment. In contrast, the profit and loss of the Huatai Back-to-back TRS 
and the Client TRS factor into account the fluctuation in RMB exchange rate upon termination of the Client TRS by converting the profit and loss using the current 
exchange rate at the time of termination. As such, the Huatai Onshore Ultimate Clients would bear the exchange rate exposure of the profit and loss on settlement date. 
 
The Huatai Onshore Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time from the issue date of the Client TRS which 
should be on or after the date on which the Offer Shares are listed on the Stock Exchange at their own discretions. Upon the termination upon maturity or early 
termination of the Client TRS by the Huatai Onshore Ultimate Clients, HTCI will dispose the Offer Shares on the secondary market and the Huatai Onshore Ultimate 
Clients will receive a final settlement amount in cash in accordance with the terms and conditions of the Huatai Back-to-back TRS and the Client TRS which should 
have taken into account all the economic returns or economic loss in relation to the Offer Shares. If upon the maturity of the Client TRS, the Huatai Onshore Ultimate 
Clients intend to extend the investment period, subject to further agreement between Huatai Securities and the relevant Huatai Onshore Ultimate Clients, the term of 
the Client TRS could be extended by way of a new issuance or a tenor extension. Accordingly, Huatai Securities will extend the term of the Huatai Back-to-back TRS 
by way of a new issuance or a tenor extension.  
 
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through the economic exposure to the Huatai Onshore 
Ultimate Clients, each being an onshore client who places a Client TRS order with Huatai Securities in connection with the Global Offering. HTCI will not exercise 
the voting right of the Offer Shares during the tenor of the Huatai Back-to-back TRS.  
 
During the life of the Client TRS and Huatai Back-to-back TRS, HTCI may continue to hold the Offer Shares in its custodian account, or to hold some or all of the 
26

<<<PAGE 27>>>
Offer Shares in a prime brokerage account for stock borrowing purposes, HTCI will lend out its holding of underlying Offer Shares in the form of stock borrowing 
loans consistent with market practice to lower its finance costs, provided that HTCI has the ability to call back the Offer Shares on loan at any time in order to satisfy 
its obligations under the Huatai Back-to-back TRS to ensure the economic interests are ultimately passed to the Huatai Onshore Ultimate Clients. 
 
Huatai Ultimate Clients includes: Roadshow Xunlu No. 90 Private Equity Investment Fund (鹿秀馴鹿90號私募證券投資基金), whose manager is Qingdao 
Roadshow Investment Management Co., Ltd. (青島鹿秀投資管理有限公司) (“Qingdao Roadshow”). The ultimate beneficial owner of Qingdao Roadshow is 
Yao Bo (么博). No ultimate beneficial owner holds 30% or more interest in this fund. 
 
3. 
The offshore investors (the “Huatai Offshore Ultimate Clients”), through its investment manager, will place the Client TRS with HTCI in connection with the Global 
Offering. In order to hedge its exposure under the Client TRS, HTCI participates in the Global Offering and subscribes the H Shares through placing order with HTFH 
during the International Offering.  
 
To the best of our knowledge and after making all reasonable enquiries, the Huatai Offshore Ultimate Clients are an independent third party of (i) the Company, the 
connected person or the associates thereof, and (ii) HTCI, HTFH and the companies which are members of the same group of HTCI.  
 
The purpose of HTCI to subscribe for the H Shares is for hedging the Client TRS order placed by the Huatai Offshore Ultimate Clients. Pursuant to the terms of the 
Client TRS, during the tenor of the Client TRS, subject to customary fees and commissions, all economic returns of the H Shares will be passed to the Huatai Offshore 
Ultimate Clients through the Client TRS and all economic loss shall be borne by the Huatai Offshore Ultimate Clients. HTCI will not take any economic return or 
bear any economic loss in relation to the H Shares.  
 
The Huatai Offshore Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time from the issue date of the Client TRS which 
should be on or after the date on which the H Shares are listed on the Stock Exchange at their own discretion. Upon the termination upon maturity or early termination 
of the Client TRS by the Huatai Offshore Ultimate Clients, HTCI will dispose the H Shares on the secondary market and the Huatai Offshore Ultimate Clients will 
receive a final settlement amount of the Client TRS in cash in accordance with the terms and conditions of the Client TRS which should have taken into account all 
the economic returns or economic loss in relation to the H Shares. If upon the maturity of the Client TRS, the Huatai Offshore Ultimate Clients intends to extend the 
investment period, subject to further agreement between HTCI and the relevant Huatai Offshore Ultimate Client, the term of the Client TRS could be extended by 
way of a new issuance or a tenor extension.  
 
It is proposed that HTCI will hold the legal title and the voting right of the H Shares by itself, and pass through the economic exposure to the Huatai Offshore Ultimate 
Clients, being a client who places a Client TRS order with HTCI in connection with the Global Offering. HTCI will not exercise the voting right of the H Shares 
during the tenor of the Client TRS.  
 
During the life of the Client TRS, HTCI may continue to hold the H Shares in its custodian account, or to hold some or all of the H Shares in a prime brokerage 
account for stock borrowing purposes, where HTCI will lend out its holding of underlying H Shares in the form of stock borrowing loans consistent with market 
practice to lower its finance costs, provided that HTCI has the ability to call back the H Shares on loan at any time in order to satisfy its obligations under the Client 
27

<<<PAGE 28>>>
TRS to ensure the economic interests are ultimately passed to the Huatai Offshore Ultimate Clients. 
 
Huatai Offshore Ultimate Clients 
UBO 
Remarks 
Zhong Heng Capital Limited  
Lan Dong  
UBO with over 30% interest 
 
 
 
 
 
  
28

<<<PAGE 29>>>
Part B - Connected Client Holding the Beneficial Interest of the Offer Shares on a Discretionary Basis on Behalf of Independent Third Parties 
 
No.  
Connected 
Distributor  
Connected Client  
Relationship  
Whether the 
Connected Client is a 
collective investment 
scheme which is not 
authorised by the SFC 
or is expected to hold 
the Offer Shares on 
behalf of such scheme  
Amount of Offer 
Shares to be allocated 
to the Connected 
Client  
Approximate 
percentage of total 
number of Offer 
Shares under the 
Global Offering  
Approximate 
percentage of total 
issued share capital 
after the Global 
Offering  
1. 
CLSA 
CITICS AM (Note 1) 
CITICS AM is a member 
of the same group of 
companies as CLSA  
Yes 
400  
0.003%  
0.0001%  
2. 
CLSA 
CITICS AM HK (Note 
2) 
CITICS AM HK is a 
member of the same 
group of companies as 
CLSA  
No 
400 
0.003%   
0.0001%   
3.  
CLSA 
China AMC HK (Note 3) 
China AMC HK is a 
member of the same 
group of companies as 
CLSA. 
No 
400 
0.003% 
0.0001% 
4.  
CLSA 
CITIC-Prudential (Note 
4) 
CITIC-Prudential Fund 
and CLSA are members 
of the same group 
No 
1000 
0.008% 
0.0002% 
5. 
HSBC 
HSBC AM (Note 5) 
HSBC AM is a fellow 
subsidiary of HSBC. 
No 
1000 
0.008% 
0.0002%  
6. 
HTFH 
CSAM (Note 7) 
CSAM and HTFH are 
within the same group 
No 
400 
0.003% 
0.0001% 
 
29

<<<PAGE 30>>>
Notes: 
 
1. 
CITICS  AM is  a  member  of  the  same  group  of  companies  as  CLSA.  CITICS  AM will  hold  the  Offer  Shares  in  its  capacity  as  the  discretionary  
fund  manager  managing  the  funds  on  behalf  of their  investors  (the  “CITICS  AM  Ultimate  Clients”),  together  with  each  of  their  ultimate  beneficial  
owners, is,  to  the  best  knowledge  of  CITICS  AM,  (i)  an  independent  third  party  of  the  Company,  its subsidiaries,  its  substantial  shareholders,  CITICS  
AM,  CLSA  and  the  companies  which  are members  of  the  same  group  of  companies  as  CLSA;  and  (ii)  a  collective  investment  scheme  which  is  not 
authorized by the SFC. The funds are as follows: 
 
a. CITIC Securities AM-Guibinfengyuan No.118 QDII (中信證券資管貴賓豐元118 號QDII 集合資產管理計 劃), of which ultimate beneficial owner holds 
30% or more interest is Zhang Guofeng (張國鋒); 
 
b. CITIC  SECURITIES  COMPANY  LIMITED-XINHANG  ZHIYUAN  NO.1  (中信證券信航致遠1 號集合 資產管理計劃), of which no ultimate beneficial 
owner holds 30% or more interest; 
 
c. CITIC  SECURITIES  COMPANY  LIMITED-XINHANG  ZHIYUAN  NO.3  (中信證券信航致遠3 號集合 資產管理計劃), of which no ultimate beneficial 
owner holds 30% or more interest; 
 
d. CITIC  SECURITIES  AM-GUIBINFENGYUAN  NO.108  QDII  (中信證券資管貴賓豐元108 號QDII 集合 資產管理計劃), of which no ultimate beneficial 
owner holds 30% or more interest. 
 
 
 
2. CITICS AM HK will hold the Offer Shares in accounts as the investment manager managing assets on behalf of its underlying client Meta Chance Limited and 
BSCOMC Limited. (the "CITICS AM HK Client").  To the best knowledge of CITICS AM HK, the ultimate beneficial owner of Meta Chance Limited is natural 
person Song Ke, and the ultimate beneficial owner of BSCOMC Limited is State-owned Assets Supervision and Administration Commission of People's 
Government of Beijing Municipality. 
 
 
CITICS AM HK has confirmed that, to the best of their knowledge and after making all reasonable enquiries, each of the CITICS AM HK Client and its ultimate 
beneficial owners holding 30% or more therein listed above is an independent third party of all the underwriters and the companies which are members of the same 
group of companies as CLSA. 
 
 
3. China AMC HK will hold the Offer Shares in its capacity as the discretionary fund manager managing on behalf of its underlying clients, each  of  which is  an  
independent  third  party  (“China  AMC  Ultimate  Clients”). China AMC HK is an investment advisor and a delegate of the investment manager of the China 
AM HK Ultimate Clients and manages assets (in its capacity as an investment advisor of China AM HK Ultimate Client) and executes trades (in its capacity as a 
30

<<<PAGE 31>>>
delegate of the investment manager of China AM HK Ultimate Client) for and on behalf of China AM HK Ultimate Client.  
 
 
The details of the China AMC Ultimate Clients are as follows: 
 
(i) HKCINDAM – it is wholly held by China Cinda (HK) Asset Management CO., LTD. 
 
 
 To the best of China AMC HK’s knowledge and after making all reasonable enquiries, the China AM HK Ultimate Client is an independent third party of the 
Company, its subsidiaries, and its substantial shareholders, China AMC HK, CLSA and the companies which are members of the same group of CLSA. 
 
4. CITIC-Prudential Fund will  hold  the  Offer  Shares  in  its  capacity  as  the  discretionary  fund  manager  of CITIC Prudential Global Macro-asset Allocation 
AMP 1. To the best knowledge of CITIC-Prudential Fund, none of the clients holds  more  than  30%  ultimate  beneficial  interest  in  the  relevant  fund.  CLSA 
and  CITIC-Prudential  Fund are members of the same group. Therefore, CITIC-Prudential Fund is a connected client of CLSA. 
 
5.  HSBC is one of the Joint Sponsor-Overall Coordinator, the Overall Coordinators, Joint Sponsors, Joint Global Coordinators, Joint Bookrunners and Joint Lead 
Managers and Capital Market Intermediaries in connection  with  the  Global  Offering. HSBC AM will  hold  the  Offer  Shares  in  its  capacity  as  the  discretionary  
fund  manager  managing  assets  on  behalf  of  its  underlying  clients (“HSBC AM Ultimate Clients”).  There is no ultimate beneficial owner holding 30% 
interest or more in such underlying client.  
 
 
The HSBC AM Ultimate Clients for purpose of this placing subscription include HGIF CHINESE EQUITY (HH), HSBC CHINA GROWTH FD(HH), HSBC 
CHINA MOMENTUM (HH), HSBC CHINA MULT-A EQ-OFF, HSBC POOLED CHINESE (HH), FLOURISH INVEST CO(CN), HGIF HONG KONG 
EQUITY(HH), HSBC POOLED HK EQ (HH), HGIF ASIA EXJ EQ SMAL(HH), and HSHK ASIAN SMALL CAP(EQ),, for each of which no ultimate beneficial 
owner holds 30% or more interest. HSBC AM  has  confirmed  that,  to  the  best  of  their  knowledge and after making all reasonable enquires, each relevant fund 
managed by them is an independent third party of the Company and its subsidiaries.. 
 
 
6. 
HTFH is one of  the Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers and Capital Market Intermediaries in connection 
the Global Offering. CSAM is held by Huatai Securities as to 41.16%, which wholly owns HTFH. As such, CSAM and HTFH is a member of the same group of 
companies. Accordingly, CSAM is considered as a “connected client” of HTFH pursuant to paragraph 1B of the Appendix F1 to the Listing Rules. CSAM, a 
qualified domestic institutional  investor  as  approved  by  the  relevant  PRC  authority  to  conduct  asset management  business,  will  hold  the  Offer  Shares  as  
the  independent  agent  and  discretionary  manager of  certain QDII funds for each of its funds (the “CSAM Ultimate Clients”). 
 
 
 
 
 
 
31

<<<PAGE 32>>>
 
 The CSAM Ultimate Clients and their respective ultimate beneficial owners include: 
 
CSAM Ultimate Clients 
UBO with 30% or more interests 
China Southern Global Dynamic Allocation Fund 
No single UBO with 30% or more interest 
China Southern China New Economy 9-Month Holding Period Hybrid 
Fund (QDII) 
No single UBO with 30% or more interest 
China Southern Hong Kong Growth Fund 
No single UBO with 30% or more interest 
China Southern Digital Economy Hybrid Fund 
No single UBO with 30% or more interest 
China Southern Hong Kong Select Equity Fund 
No single UBO with 30% or more interest  
China Southern Hong Kong Healthcare Industry Hybrid Initiating Fund 
(QDII) 
No single UBO with 30% or more interest 
 
 
CSAM  has  confirmed  that,  to  the  best  of  their  knowledge,  (i)  the  CSAM  Ultimate  Clients  and  the  ultimate beneficial  owners  holding  30%  or  more  
interest  of  the  CSAM  Ultimate  Clients  listed  above  is  an  independent third  party  of  (a)  the  Company,  the  connected  person  or  the  associates  thereof;  
and  (b)  CSAM,  HTFH  and  the companies  which  are  members  of  the  same  group  of  companies  as  HTFH,  and  (ii)  CSAM  is  not  a  collective investment  
scheme  which  is  not  authorised  by  the  SFC  nor  is  expected  to  hold  the  Offer  Shares  on  behalf  of such scheme. 
 
. 
32

<<<PAGE 33>>>
Allocations under the Overseas Employee Preferential Offering
Of the 1,263,200 Offer Shares initially being offered under the Hong Kong Public Offering, no more
than 126,300 Offer Shares, representing approximately 10% of the Offer Shares initially available for
subscription under the Hong Kong Public Offering, are available for subscription as Overseas
Employee Reserved Shares by the Overseas Eligible Employees on a preferential basis under the
Overseas Employee Preferential Offering according to Rule 10.01 of the Listing Rules. For details,
please refer to the section headed ‘‘Structure of the Global Offering — The Overseas Employee
Preferential Offering’’ of the Prospectus.
60,300 Offer Shares have been allocated to 6 Overseas Eligible Employees pursuant to the Overseas
Employee Preferential Offering, representing approximately 0.48% of the total number of Offer Shares
available under the Global Offering.
Allocations under the PRC Employee Preferential Offering
Of the 11,368,800 Offer Shares initially being offered under the International Offering, no more than
1,136,800 Offer Shares, representing approximately 10% of the Offer Shares initially available for
subscription under the International Offering, are available for subscription as PRC Employee Reserved
Shares by the PRC Eligible Employees on a preferential basis under the PRC Employee Preferential
Offering according to Rule 10.01 of the Listing Rules. For details, please refer to the section headed
‘‘Structure of the Global Offering — The PRC Employee Preferential Offering’’ of the Prospectus.
911,300 Offer Shares have been placed to 116 PRC Eligible Employees pursuant to the PRC Employee
Preferential Offering, representing approximately 7.21% of the total number of Offer Shares available
under the Global Offering.
– 33 –

<<<PAGE 34>>>
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong
Kong Securities Clearing Company Limited take no responsibility for the contents of this
announcement, make no representation as to its accuracy or completeness and expressly disclaim
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any
part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the
United States (including its territories and possessions, any state of the United States and the
District of Columbia). This announcement does not constitute or form a part of any offer or
solicitation to purchase or subscribe for securities in the United States. The securities mentioned
herein have not been, and will not be, registered under the United States Securities Act of 1933, as
amended (the ‘‘U.S. Securities Act’’). The securities may not be offered or sold in the United States
except pursuant to an exemption from the registration requirements of the U.S. Securities Act and in
compliance with any applicable state securities laws, or outside the United States unless in
compliance with Regulation S under the U.S. Securities Act. There will be no public offer of
securities in the United States.
The Offer Shares may only be offered and sold outside the United States in offshore transactions in
reliance on Regulation S under the U.S. Securities Act. No public offering of the Offer Shares will
be made in the United States.
This announcement is for information purposes only and does not constitute an invitation or offer to
acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential
investors should read the Prospectus dated June 30, 2026 issued by Guangdong Dtech Technology
Co., Ltd. for detailed information about the Global Offering described below before deciding
whether or not to invest in the Offer Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Joint Sponsors and the Joint Sponsor-
Overall Coordinators (for itself and on behalf of the Hong Kong Underwriters) shall be entitled to
terminate their obligations under the Hong Kong Underwriting Agreement with immediate effect
upon the occurrence of any of the events set out in the section headed ‘‘Underwriting —
Underwriting
Arrangements
and
Expenses
—
Hong
Kong
Public
Offering
—
Grounds
for
Termination’’ in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing
Date (which is currently expected to be on July 9, 2026).
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering, the total market value of the H Shares
expected to be held by the public is expected to be approximately HK$4,800.16 million, calculated
based on the final Offer Price of HK$380.00, which is higher than the prescribed expected market
value of H Shares required to be held in public hands of not less than HK$3,000,000,000 under Rule
19A.13A(2)(b) of the Listing Rules, thereby satisfying Rule 19A.13A(2) of the Listing Rules.
– 34 –

<<<PAGE 35>>>
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the Listing
Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be counted
towards the free float of the H Shares of the Company at the time of Listing. Based on the final Offer
Price of HK$380.00 per H Share, the Company confirmed that it complies with the free float
requirement under Rule 19A.13C(2)(b) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering: (i) the Shares
will be held by at least 300 Shareholders at the time of Listing, in compliance with Rule 8.08(2) of the
Listing Rules; (ii) the three largest public Shareholders will not hold more than 50% of the H Shares
held in public hands at the time of Listing, in compliance with Rules 8.08(3) and 8.24 of the Listing
Rules; (iii) no placee will, individually, be placed more than 10% of the enlarged issued share capital
of the Company immediately after the Global Offering; and (iv) there will not be any new substantial
Shareholder (as defined in the Listing Rules) immediately after the Global Offering.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Thursday, July 9,
2026 (Hong Kong time), provided that the Global Offering has become unconditional and the right of
termination described in the section headed ‘‘Underwriting — Underwriting Arrangements and
Expenses — Hong Kong Public Offering — Grounds for Termination’’ in the Prospectus has not been
exercised. Investors who trade the H Shares on the basis of publicly available allocation details prior to
the receipt of H Share certificates or prior to the H Share certificates becoming valid evidence of title
do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Thursday, July 9,
2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange will
commence at 9:00 a.m. on Thursday, July 9, 2026 (Hong Kong time). The H Shares will be traded in
board lots of 100 H Shares each, and the stock code of the H Shares will be 1377.
By order of the Board
Guangdong Dtech Technology Co., Ltd.
廣東鼎泰高科技術股份有限公司
Wang Xin
Chairperson of the Board, Executive Director and General Manager
Hong Kong, July 8, 2026
As of the date of this announcement, the Board comprises: (i) Ms. Wang Xin, Mr. Wang Junfeng, Mr. Lin Xia, Mr. Wang
Xuefeng and Ms. Wang Yifei as executive Directors; and (ii) Ms. Li Xiaofei, Mr. Song Haihai, Dr. Xin Guosheng and Dr.
Huang Hui as independent non-executive Directors.
– 35 –
