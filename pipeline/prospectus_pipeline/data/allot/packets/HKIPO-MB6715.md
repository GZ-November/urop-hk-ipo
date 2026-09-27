# 配发结果公告抽取任务：6715.HK Hangzhou Qiandaohu Xunlong Sci-tech Co., Ltd. - H Shares

- 公告：GLOBAL OFFERING
- 刊发时间（港交所元数据）：**29/06/2026 22:58**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0629/2026062902679.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6715.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the ‘‘Stock Exchange’’) and
Hong Kong Securities Clearing Company Limited (‘‘HKSCC’’) take no responsibility for the contents of this announcement,
make no representation as to its accuracy or completeness and expressly disclaim any liability whatsoever for any loss
howsoever arising from or in reliance upon the whole or any part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those
defined in the prospectus dated June 22, 2026 (the ‘‘Prospectus’’) of Hangzhou Qiandaohu Xunlong Sci-tech Co., Ltd. (杭
州千島湖鱘龍科技股份有限公司) (the ‘‘Company’’).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase or
subscribe for any securities. This announcement is not a prospectus. Potential investors should read the Prospectus for
detailed information about the Global Offering described below before deciding whether or not to invest in the Offer
Shares. Any investment decision in relation to the Offer Shares should be taken solely in reliance on the information
provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States (including
its territories and possessions, any state of the United States and the District of Columbia). This announcement does not,
and is not intended to, constitute or form a part of any offer to sell or solicitation to purchase or subscribe for any
securities in the United States or in any other jurisdiction. The Offer Shares have not been, and will not be, registered
under the U.S. Securities Act of 1933, as amended from time to time (the ‘‘U.S. Securities Act’’) or any securities law of
any state or other jurisdiction of the United States and may not be offered, sold, pledged, or otherwise transferred within
the United States, except pursuant to an exemption from, or in a transaction not subject to, the registration requirements of
the U.S. Securities Act and in compliance with any applicable state securities laws. There will be no public offer of the
Offer Shares in the United States. The Offer Shares are being offered and sold solely outside the United States in offshore
transactions in reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, CLSA Limited as stabilizing manager (the ‘‘Stabilizing Manager’’), its affiliates or
any person acting for it, on behalf of the Underwriters, may effect transactions with a view to stabilizing or supporting the
market price of the Shares at a level higher than that which might otherwise prevail for a limited period after the Listing
Date. However, there is no obligation on the Stabilizing Manager, its affiliates or any person acting for it to conduct any
such stabilizing action, which, if commenced, will be done at the sole and absolute discretion of the Stabilizing Manager,
its affiliates or any person acting for it and may be discontinued at any time. Any such stabilization activity is required to
be brought to an end on Saturday, July 25, 2026, being the 30th day after the last date for lodging of applications under
the Hong Kong Public Offering. Such stabilization action, if taken may be effected in all jurisdictions where it is
permissible to do so, in each case in compliance with all applicable laws, rules and regulatory requirements, including the
Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the
Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that stabilizing action cannot be taken to support the price of the H Shares for longer
than the stabilisation period which begins on the Listing Date, and is expected to expire on Saturday, July 25, 2026, the
30th day after the last day for the lodging of applications under the Hong Kong Public Offering. After this date, no further
stabilizing action may be taken, demand for the H Shares, and therefore the price of the H Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out in the
Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not resident
in Hong Kong. Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall-Coordinators
(for themselves and on behalf of the Hong Kong Underwriters) in their sole and absolute discretion may, by notice in
writing to the Company, terminate the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of
any of the events set out in ‘‘Underwriting — Underwriting Arrangements and Expenses — the Hong Kong Public Offering
— Grounds for Termination’’ in the Prospectus at any time at or prior to 8:00 a.m. on the Listing Date.
– 1 –

<<<PAGE 2>>>
Hangzhou Qiandaohu Xunlong Sci-tech Co., Ltd.
杭州千島湖鱘龍科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under
the Global Offering
:
16,332,900 H Shares (subject to the
Over-allotment Option)
Number of Hong Kong Offer Shares
:
1,633,300 H Shares
Number of International Offer Shares
:
14,699,600 H Shares (subject to the
Over-allotment Option)
Final Offer Price
:
HK$75.50 per H Share plus brokerage of
1.0%, SFC transaction levy of 0.0027%,
AFRC transaction levy of 0.00015% and
Hong Kong Stock Exchange trading fee of
0.00565% (payable in full on application in
Hong Kong dollars and subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
6715
Joint Sponsors, Sponsor-Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
– 2 –

<<<PAGE 3>>>
Hangzhou Qiandaohu Xunlong Sci-tech Co., Ltd.
杭州千島湖鱘龍科技股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same
meanings as those defined in the prospectus dated June 22, 2026 (the ‘‘Prospectus’’) issued by
Hangzhou Qiandaohu Xunlong Sci-tech Co., Ltd. (the ‘‘Company’’).
Warning: In view of high concentration of shareholding in a small number of H Shareholders,
H Shareholders and prospective investors should be aware that the price of the H Shares could
move substantially even with a small number of H Shares traded and should exercise extreme
caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
6715
Stock short name
XUNLONG SCITECH
Dealings commencement date
June 30, 2026*
*
see note at the end of the announcement
Price Information
Final Offer Price
HK$75.50
Fixed Offer Price
HK$75.50
Offer Shares and Share Capital
Number
of
Offer
Shares
(before
exercise
of
Over-
allotment Option)
16,332,900
Final Number of Offer Shares in Hong Kong Public
Offering
1,633,300
Final Number of Offer Shares in International Offering
(before exercise of the Over-allotment Option)
14,699,600
Number of issued Shares upon Listing (before exercise
of Over-allotment Option)
108,885,600
Over-allocation
No. of Offer Shares over-allocated
2,449,900
—
International Offer
2,449,900
Such over-allocation may be covered by exercising the Over-allotment Option or by making
purchases in the secondary market at prices that do not exceed the Offer Price or through
deferred delivery or a combination of these means. In the event the Over-allotment Option is
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$1,233.1 million
Less: Estimated listing expenses payable based on
Offer Price
HK$(86.9) million
Net proceeds
HK$1,146.3 million
Note:
Gross proceeds refers to the amount to which the Company is entitled receive assuming the Over-allotment
Option is not exercised. For details of the use of proceeds, please refer to the section headed ‘‘Future Plans
and Use of Proceeds’’ of the Prospectus.
The Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option
(if any) for the purposes as set out in the section headed ‘‘Future Plans and Use of Proceeds’’ of the
Prospectus on a pro rata basis.
– 3 –

<<<PAGE 4>>>
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
Number of valid applications
179,723
Number of successful applications
16,265
Subscription level
2,134.81 times
Claw-back triggered
No
No. of Offer Shares initially available under the Hong Kong Public Offering
1,633,300
Final number of Offer Shares under the Hong Kong Public Offering
1,633,300
% of Offer Shares under the Public Offering to the Global Offering
10.00%
Note:
For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to https://
www.hkeipo.hk/iporesult to perform a search by name or identification number or https://www.hkeipo.hk/iporesult
for the full list of allottees.
INTERNATIONAL OFFER
Number of placees
145
Subscription Level
19.87 times
Number of Offer Shares initially available under the International Offer
14,699,600
Final number of Offer Shares under the International Offer (before exercise
of the Over-allotment Option)
14,699,600
% of Offer Shares under the International Offering to the Global Offering
90.00%
The Directors confirm that, to the best of their knowledge, information and belief, save for consents
under paragraph 1C(1) of Appendix F1 to the Listing Rules (the ‘‘Placing Guidelines’’) and paragraph
18 of Chapter 4.15 of the Guide for New Listing Applicants granted by the Stock Exchange to permit
the Company to, among other things, place certain H Shares in the International Offering to
Cornerstone Investors and/or their close associates and connected clients, (i) none of the Offer Shares
subscribed by the placees and the public have been financed directly or indirectly by the Company, any
of
the
Directors,
chief
executive
of
the
Company,
Single
Largest
Shareholders,
substantial
shareholders, existing shareholders of the Company or any of its subsidiaries or their respective close
associates; and (ii) none of the placees and the public who have purchased the Offer Shares are
accustomed to taking instructions from the Company, any of the Directors, chief executive of the
Company, Single Largest Shareholders, substantial shareholders, existing shareholders of the Company
or any of its subsidiaries or their respective close associates in relation to the acquisition, disposal,
voting or other disposition of Shares registered in his/her/its name or otherwise held by him/her/it.
– 4 –

<<<PAGE 5>>>
The placees in the International Offering include the following:
Cornerstone Investors
InvestorNote 1
Number of
Offer
Shares
allocated
% of Offer
SharesNote 2
% of total
H Shares
after the
Global
Offering
Note 2
% of total
issued
share
capital
after the
Global
Offering
Note 2
Existing
shareholders
or their close
associates
BlackRock FundsNote 3
3,113,300
19.06%
2.86%
2.86%
No
BaringsNote 3
1,037,700
6.35%
0.95%
0.95%
No
Taikang LifeNote 3
1,037,700
6.35%
0.95%
0.95%
No
Shanghai Greenwoods and
GTINV (in connection with
Greenwoods OTC
Swaps)Note 4
778,300
4.77%
0.71%
0.71%
No
Dacheng Investors
726,400
4.45%
0.67%
0.67%
No
ICBC WealthNotes 3 and 5
518,800
3.18%
0.48%
0.48%
No
Nova Kerry Inc.Note 3
518,800
3.18%
0.48%
0.48%
No
Mirae Asset Securities
HKNote 3
415,100
2.54%
0.38%
0.38%
No
Subtotal
8,146,100
49.88%
7.48%
7.48%
Notes:
1.
For further details of the Cornerstone Investors, please refer to the section headed ‘‘Cornerstone Investments’’ of the
Prospectus.
2.
Assuming the Over-allotment Option is not exercised.
3.
Only taking into account the Offer Shares allocated to the relevant investors as cornerstone investors under the Global
Offering. In addition to the Offer Shares subscribed for as Cornerstone Investors, each of such investors and/or their
respective close associates was allocated further Offer Shares as a placee in the International Offering. Please refer to
the section headed ‘‘Allotment Results Details — International Offering Allotees with Waivers/Consents Obtained’’ in
this announcement for details. Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-up as
indicated below. For details, please refer to the section headed ‘‘Lock-up Undertakings — Cornerstone Investors’’ in
this announcement.
– 5 –

<<<PAGE 6>>>
4.
GTINV, a subsidiary of Guotai Haitong Securities Co. Ltd., has entered into a cornerstone investment agreement with
the Company, the Joint Sponsors, and the Sponsor-Overall Coordinators to subscribe for the Offer Shares in
connection with the Greenwoods OTC Swaps. Guotai Junan Securities (Hong Kong) Limited (‘‘GTJAS’’), a non-
syndicate sub-broker in connection with the Global Offering, is also a subsidiary of Guotai Haitong Securities Co.
Ltd., the A shares of which are listed on the Shanghai Stock Exchange (601211.SH) and the H shares are listed on the
Hong Kong Stock Exchange (02611.HK). GTINV is a member of the same group of companies as GTJAS, and
therefore is a ‘‘connected client’’ of GTJAS for the purpose of paragraph 1B of the Placing Guidelines. The Company
has applied to the Stock Exchange, and the Stock Exchange has granted consent under paragraph 1C(1) of the
Placing Guidelines.
5.
For the purpose of participation in the International Offering as a cornerstone investor, ICBC Wealth, a Cornerstone
Investor, has engaged various asset managers that are qualified domestic international investors as approved by the
relevant PRC authority, to subscribe for and hold such Offer Shares on a non-discretionary basis on behalf of ICBC
Wealth. Among all 518,800 Offer Shares subscribed for ICBC Wealth, (i) 415,100 Offer Shares were subscribed
through Shanghai Guotai Haitong Securities Asset Management Co., Ltd. (‘‘Shanghai GTHT Securities’’), and (ii)
103,700 Offer Shares were subscribed through GF SECURITIES ASSET MANAGEMENT (GUANGDONG) CO.,
LTD. Each of such asset managers is an independent third party of ICBC Wealth.
Among these asset managers which are qualified domestic international investors subscribing for Offer Shares for
ICBC Wealth, Shanghai GTHT Securities is a subsidiary of Guotai Haitong Securities Co. Ltd.. Therefore, Shanghai
GTHT Securities and GTJAS are members of the same group of companies and therefore is a ‘‘connected client’’ of
GTJAS for the purpose of paragraph 1B of the Placing Guidelines. The Company has applied to the Stock Exchange,
and the Stock Exchange has granted consent under paragraph 1C(1) of the Placing Guidelines.
– 6 –

<<<PAGE 7>>>
Allotees with Waivers/Consents Obtained
Investor
Number of
Offer Shares
allocated
% of Offer
SharesNote 1
% of total H
Shares after
the Global
Offering
Note 1
% of total
issued share
capital after
the Global
Offering
Note 1
Relationship
Allotees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to
allocation of further H Shares to Cornerstone Investors and/or their close associatesNote 2
BlackRock Funds
290,500
1.78%
0.27%
0.27%
A Cornerstone Investor
Barings
87,100
0.53%
0.08%
0.08%
A Cornerstone Investor
Taikang Life and its close associate
— Taikang Life
42,700
0.26%
0.04%
0.04%
A Cornerstone Investor
— SHANGHAI
EVERBRIGHT
SECURITIES
ASSET
MANAGEMENT
CO., LTD.
20,800
0.13%
0.02%
0.02%
To subscribe and hold
the Offer Shares for a
close associate of
a Cornerstone
InvestorNote 3
Subtotal:
63,500
0.39%
0.06%
0.06%
ICBC WealthNote 4
21,300
0.13%
0.02%
0.02%
A Cornerstone Investor
Nova Kerry Inc.
21,300
0.13%
0.02%
0.02%
A Cornerstone Investor
Mirae Asset Securities
HK
34,800
0.21%
0.03%
0.03%
A Cornerstone Investor
– 7 –

<<<PAGE 8>>>
Investor
Number of
Offer Shares
allocated
% of Offer
SharesNote 1
% of total H
Shares after
the Global
Offering
Note 1
% of total
issued share
capital after
the Global
Offering
Note 1
Relationship
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing
Applicants in relation to allocations to connected clientsNote 5
Part A — Connected Clients holding securities on a Discretionary Basis on behalf of Independent Third Parties
China Asset Management
(Hong Kong) Limited
(‘‘China AMC HK’’)
3,000
0.02%
0.00%
0.00%
A connected client of
CLSA Limited
(‘‘CLSA’’)
CITIC Securities Asset
Management (HK) Limited
(‘‘CITIC Asset
Management HK’’)
1,000
0.01%
0.00%
0.00%
A connected client of
CLSA
China Southern Asset
Management Co., Ltd.
(‘‘China Southern’’)
3,000
0.02%
0.00%
0.00%
A connected client of
Huatai Financial
Holdings (Hong
Kong) Limited
(‘‘HTFH’’)
Fullgoal Fund Management
Co., Ltd. (‘‘Fullgoal
Fund’’)
6,000
0.04%
0.01%
0.01%
A connected client of
GTJAS
Part B — Connected Clients holding securities on a Non-Discretionary Basis on behalf of Independent Third Parties
CSI Capital Management
Limited (‘‘CSI Capital’’)
74,000
0.45%
0.07%
0.07%
A connected client of
CLSA
Huatai Capital Investment
Limited (‘‘HTCI’’)
2,000
0.01%
0.00%
0.00%
A connected client of
HTFH
Shanghai Greenwoods and
GTINV (in connection with
Greenwoods OTC Swaps)
778,300Note 6
4.77%Note 6
0.71%Note 6
0.71%Note 6
GTINV is a member
of the same group of
companies as
GTJASNote 7
ICBC Wealth
518,800Note 6
3.18%Note 6
0.48%Note 6
0.48%Note 6
Shanghai GTHT
Securities and GTJAS
are members of the
same group of
companiesNote 8
– 8 –

<<<PAGE 9>>>
Notes:
1.
Assuming the Over-allotment Option is not exercised.
2.
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the number of
Offer Shares allocated to the investors as placees in the International Offering. For allocations of Offer Shares to the
relevant investors as Cornerstone Investors, please refer to the section headed ‘‘Allotment Results Details —
International Offering — Cornerstone Investors’’ in this announcement. For details of the consent under paragraph 18
of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further Shares to Cornerstone
investors and/or their close associates, please refer to the section headed ‘‘Others/Additional Information —
Allocations of Offer Shares to Cornerstone Investors and/or their close associates with consent under paragraph 18 of
Chapter 4.15 of the Guide for New Listing Applicants’’ in this announcement.
3.
SHANGHAI EVERBRIGHT SECURITIES ASSET MANAGEMENT CO., LTD. proposes to subscribe for and hold
the Offer Shares as a placee under the International Offering on behalf of SDIC Taikang Trust Co., Ltd. pursuant to its
discretionary investment management mandate. Taikang Insurance Group Inc. (the parent company of Taikang Life) is
interested (directly and indirectly through its wholly-owned subsidiary) in 30% or more equity interest in SDIC
Taikang Trust Co., Ltd. Therefore, SDIC Taikang Trust Co., Ltd. is a close associate of Taikang Life.
4.
For the purpose of participation in the International Offering as a placee, ICBC Wealth, has engaged various asset
managers that are qualified domestic international investors as approved by the relevant PRC authority, to subscribe
for and hold such Offer Shares on a non-discretionary basis on behalf of ICBC Wealth. Among all 21,300 Offer
Shares subscribed for ICBC Wealth, (i) 16,100 Offer Shares were subscribed through GREAT WALL FUND
MANAGEMENT CO., LTD, and (ii) 5,200 Offer Shares were subscribed through Everbright PGIM Fund Management
Co Ltd. Each of such asset managers is an independent third party of ICBC Wealth.
5.
For details of the consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to connected
clients, please refer to the section headed ‘‘Others/Additional Information — Placing to connected clients with a prior
consent under paragraph 1C(1) of the Placing Guidelines’’ in this announcement.
6.
Refer to Offer Shares subscribed for as a Cornerstone Investor.
7.
GTINV, a subsidiary of Guotai Haitong Securities Co. Ltd., has entered into a cornerstone investment agreement with
the Company, the Joint Sponsors, and the Sponsor-Overall Coordinators to subscribe for the Offer Shares in
connection with the Greenwoods OTC Swaps. GTJAS, a non-syndicate sub-broker in connection with the Global
Offering, is also a subsidiary of Guotai Haitong Securities Co. Ltd., the A shares of which are listed on the Shanghai
Stock Exchange (601211.SH) and the H shares are listed on the Hong Kong Stock Exchange (02611.HK). GTINV is a
member of the same group of companies as GTJAS, and therefore is a ‘‘connected client’’ of GTJAS for the purpose
of paragraph 1B of the Placing Guidelines.
8.
For the purpose of participation in the International Offering as a cornerstone investor, ICBC Wealth, a Cornerstone
Investor, has engaged various asset managers that are qualified domestic international investors as approved by the
relevant PRC authority, to subscribe for and hold such Offer Shares on a non-discretionary basis on behalf of ICBC
Wealth. Among all 518,800 Offer Shares subscribed for ICBC Wealth, (i) 415,100 Offer Shares were subscribed
through Shanghai GTHT Securities, and (ii) 103,700 Offer Shares were subscribed through GF SECURITIES ASSET
MANAGEMENT (GUANGDONG) CO., LTD. Each of such asset managers is an independent third party of ICBC
Wealth.
Among these asset managers which are qualified domestic international investors subscribing for Offer Shares for
ICBC Wealth, Shanghai GTHT Securities is a subsidiary of Guotai Haitong Securities Co. Ltd.. Therefore, Shanghai
GTHT Securities and GTJAS are members of the same group of companies and therefore is a ‘‘connected client’’ of
GTJAS for the purpose of paragraph 1B of the Placing Guidelines.
– 9 –

<<<PAGE 10>>>
LOCK-UP UNDERTAKINGS
Single Largest Shareholders
Name
Number of
Unlisted Shares
held in the
Company subject
to lock-up
undertakings
upon Listing
Number of H
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
upon Listing
(assuming the
Over-allotment
Option is not
exercised)
% of
shareholding in
the Company
subject to lock-
up undertakings
upon Listing
(assuming the
Over-allotment
Option is not
exercised)
Last day subject
to the lock-up
undertakings
Note 1
Mr. Wang
—
5,883,900
5.40%
5.40%
June 29, 2027
Chunan Kalujiaren
—
19,563,600
17.97%
17.97%
June 29, 2027
Hangzhou Kalujiaren
—
4,297,270
3.95%
3.95%
June 29, 2027
Hangzhou Xunlongren
—
2,310,000
2.12%
2.12%
June 29, 2027
Subtotal
—
32,054,770
29.44%
29.44%
Note:
1.
In accordance with the relevant Listing Rule/guidance materials, the required lock-up period ends on December 29,
2026. Pursuant to the PRC Company Law, shares issued by the Company prior to the Listing will be subject to a lock-
up period of one year from the Listing Date, which ends on June 29, 2027.
– 10 –

<<<PAGE 11>>>
Cornerstone Investors
Name
Number of H
Shares held in the
Company subject
to lock-up
undertakings upon
Listing
% of total issued
H Shares after the
Global Offering
subject to lock-up
undertakings upon
Listing (assuming
the Over-allotment
Option is not
exercised)
% of shareholding
in the Company
subject to lock-up
undertaking upon
Listing (assuming
the Over-allotment
Option is not
exercised)
Last day subject to
the lock-up
undertakings
Note 1
BlackRock Funds
3,113,300
2.86%
2.86%
December 29, 2026
Barings
1,037,700
0.95%
0.95%
December 29, 2026
Taikang Life
1,037,700
0.95%
0.95%
December 29, 2026
Shanghai Greenwoods and
GTINV (in connection with
Greenwoods OTC Swaps)
778,300
0.71%
0.71%
December 29, 2026
Dacheng Investors
726,400
0.67%
0.67%
December 29, 2026
ICBC Wealth
518,800
0.48%
0.48%
December 29, 2026
Nova Kerry Inc.
518,800
0.48%
0.48%
December 29, 2026
Mirae Asset Securities HK
415,100
0.38%
0.38%
December 29, 2026
Subtotal
8,146,100
7.48%
7.48%
Note:
1.
In accordance with each of the respective Cornerstone Investment Agreements, the required lock-up period of six
months from the Listing Date ends on December 29, 2026. The Cornerstone Investors will cease to be prohibited from
disposing of or transferring H Shares after the indicated date. For further details, please see ‘‘Cornerstone Investments
— Restrictions on the Cornerstone Investors’’ in the Prospectus.
– 11 –

<<<PAGE 12>>>
Other Existing Shareholders (including the Pre-IPO Investors as defined in the ‘‘History,
Development and Corporate Structure’’ section of the Prospectus)
Name
Number of
Unlisted Shares
held in the
Company
subject to lock-
up undertakings
upon Listing
Number of H
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
upon Listing
(assuming the
Over-allotment
Option is not
exercised)
% of
shareholding in
the Company
subject to lock-
up undertakings
upon Listing
(assuming the
Over-allotment
Option is not
exercised)
Last day subject
to the lock-up
undertakings
Note 1
Newline Media
—
4,234,750
3.89%
3.89%
June 29, 2027
Zhejiang Zhongye
—
1,194,400
1.10%
1.10%
June 29, 2027
Shiyue Venture
—
1,000,000
0.92%
0.92%
June 29, 2027
Qianfa Group
—
5,171,900
4.75%
4.75%
June 29, 2027
Jinshi Kunxiang
—
1,931,360
1.77%
1.77%
June 29, 2027
Qihui Runjin
—
2,450,250
2.25%
2.25%
June 29, 2027
CITIC Securities
Investment Co., Ltd.
(中信證券投資有限公司)
—
1,931,360
1.77%
1.77%
June 29, 2027
CHEN Xiaxin (陳夏鑫)
—
11,726,041
10.77%
10.77%
June 29, 2027
Fengshi Jinghe
—
7,336,200
6.74%
6.74%
June 29, 2027
ZHOU Junliang (周俊良)
—
4,763,719
4.37%
4.37%
June 29, 2027
Gaojing Luoke
—
3,415,600
3.14%
3.14%
June 29, 2027
Zixing Liangmei
—
2,665,000
2.45%
2.45%
June 29, 2027
QIU Shenlin (邱沈林)
—
2,228,200
2.05%
2.05%
June 29, 2027
Zhouyang Venture
—
2,184,900
2.01%
2.01%
June 29, 2027
LIU Yu (劉宇)
—
1,646,800
1.51%
1.51%
June 29, 2027
Tianchao Shuichan
—
1,252,610
1.15%
1.15%
June 29, 2027
GUO Quanqing (國全慶)
—
1,174,600
1.08%
1.08%
June 29, 2027
Yuansheng Jiahao
—
1,144,400
1.05%
1.05%
June 29, 2027
Fengshi Hechuang
—
855,600
0.79%
0.79%
June 29, 2027
RUAN Xinhong (阮新宏)
—
372,001
0.34%
0.34%
June 29, 2027
SHEN Huifeng (沈慧芬)
—
350,239
0.32%
0.32%
June 29, 2027
– 12 –

<<<PAGE 13>>>
Name
Number of
Unlisted Shares
held in the
Company
subject to lock-
up undertakings
upon Listing
Number of H
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
upon Listing
(assuming the
Over-allotment
Option is not
exercised)
% of
shareholding in
the Company
subject to lock-
up undertakings
upon Listing
(assuming the
Over-allotment
Option is not
exercised)
Last day subject
to the lock-up
undertakings
Note 1
Hangzhou Lingfeng
Cybernaut Venture
Capital Partnership
(Limited Partnership)
(杭州靈峰賽伯樂創業投
資合夥企業(有限合夥))
—
330,000
0.30%
0.30%
June 29, 2027
DONG Zhendong
(董振東)
—
280,175
0.26%
0.26%
June 29, 2027
QIAN Huilong (錢會龍)
—
280,175
0.26%
0.26%
June 29, 2027
CHEN Chunmei (陳春妹)
—
280,175
0.26%
0.26%
June 29, 2027
WU Nanping (吳南平)
—
280,175
0.26%
0.26%
June 29, 2027
FU Haiying (傅海英)
—
17,300
0.02%
0.02%
June 29, 2027
Subtotal
—
60,497,930
55.58%
55.58%
Note:
1.
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. The required
lock-up ends on June 29, 2027, being one year following the Listing Date.
– 13 –

<<<PAGE 14>>>
PLACEE CONCENTRATION ANALYSIS
Placees
Number
of H
Shares
allotted
Allotment as
% of
International
Offering
(assuming no
exercise of
the Over-
allotment
Option)
Allotment as
% of
International
Offering
(assuming
the Over-
allotment
Option is
exercised
and new H
Shares are
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
Option is
exercised
and new H
Shares are
issued)
Number of
Shares
held upon
Listing
% of total
issued share
capital upon
Listing
(assuming no
exercise of
the Over-
allotment
Option)
·% of total
issued share
capital upon
Listing
(assuming
the Over-
allotment
Option is
exercised
and new H
Shares are
issued)
Top 1
3,403,800
23.16%
19.85%
20.84%
18.12%
3,403,800
3.13%
3.06%
Top 5
7,342,000
49.95%
42.81%
44.95%
39.09%
7,342,000
6.74%
6.59%
Top 10
10,269,300
69.86%
59.88%
62.87%
54.67%
10,269,300
9.43%
9.22%
Top 25
15,129,100
102.92%
88.22%
92.63%
80.55%
15,129,100
13.89%
13.59%
Notes
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
(assuming no
exercise of
the Over-
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
and new H
Shares are
issued)
Allotment
as % of
total Offer
Shares
(assuming
no exercise
of the Over-
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
and new H
Shares are
issued)
Number of
H Shares
held upon
Listing
% of total
issued H
Shares
capital upon
Listing
(assuming
no exercise
of the Over-
allotment
Option)
% of total
issued H
Shares
capital upon
Listing
(assuming
the Over-
allotment
Option is
exercised
and new H
Shares are
issued)
Number of
Shares held
upon Listing
Top 1
0
0.00%
0.00%
0.00%
0.00%
32,054,770
29.44%
28.79%
32,054,770
Top 5
0
0.00%
0.00%
0.00%
0.00%
62,718,061
57.60%
56.33%
62,718,061
Top 10
3,403,800
23.16%
19.85%
20.84%
18.12%
79,416,430
72.94%
71.33%
79,416,430
Top 25
8,691,000
59.12%
50.68%
53.21%
46.27%
99,053,460
90.97%
88.97%
99,053,460
Notes
*
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
– 14 –

<<<PAGE 15>>>
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
Number of
H Shares
allotted
Allotment
as % of
International
Offering
(assuming no
exercise of
the Over-
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
and new H
Shares are
issued)
Allotment
as % of
total Offer
Shares
(assuming
no exercise
of the Over-
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
and new H
Shares are
issued)
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
of the Over-
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
and new H
Shares are
issued)
Top 1
0
0.00%
0.00%
0.00%
0.00%
32,054,770
32,054,770
29.44%
28.79%
Top 5
0
0.00%
0.00%
0.00%
0.00%
62,718,061
62,718,061
57.60%
56.33%
Top 10
3,403,800
23.16%
19.85%
20.84%
18.12%
79,416,430
79,416,430
72.94%
71.33%
Top 25
8,691,000
59.12%
50.68%
53.21%
46.27%
99,053,460
99,053,460
90.97%
88.97%
Notes
*
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.
– 15 –

<<<PAGE 16>>>
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, 179,723 valid applications made
by the public will be conditionally allocated on the basis set out below:
Pool A:
NO. OF
H SHARES
APPLIED
FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED OF
THE TOTAL NO.
OF H SHARES
APPLIED FOR
100
66,606
1,999 out of 66,606 applicants to receive 100 H Shares
3.00%
200
7,506
263 out of 7,506 applicants to receive 100 H Shares
1.75%
300
4,692
180 out of 4,692 applicants to receive 100 H Shares
1.28%
400
3,341
136 out of 3,341 applicants to receive 100 H Shares
1.02%
500
3,870
166 out of 3,870 applicants to receive 100 H Shares
0.86%
600
10,310
459 out of 10,310 applicants to receive 100 H Shares
0.74%
700
2,048
95 out of 2,048 applicants to receive 100 H Shares
0.66%
800
1,444
69 out of 1,444 applicants to receive 100 H Shares
0.60%
900
1,439
70 out of 1,439 applicants to receive 100 H Shares
0.54%
1,000
11,110
553 out of 11,110 applicants to receive 100 H Shares
0.50%
1,500
3,309
180 out of 3,309 applicants to receive 100 H Shares
0.36%
2,000
2,941
171 out of 2,941 applicants to receive 100 H Shares
0.29%
2,500
2,025
124 out of 2,025 applicants to receive 100 H Shares
0.24%
3,000
2,186
139 out of 2,186 applicants to receive 100 H Shares
0.21%
3,500
1,494
98 out of 1,494 applicants to receive 100 H Shares
0.19%
4,000
1,802
122 out of 1,802 applicants to receive 100 H Shares
0.17%
4,500
1,158
81 out of 1,158 applicants to receive 100 H Shares
0.16%
5,000
2,530
180 out of 2,530 applicants to receive 100 H Shares
0.14%
6,000
2,278
169 out of 2,278 applicants to receive 100 H Shares
0.12%
7,000
2,045
157 out of 2,045 applicants to receive 100 H Shares
0.11%
8,000
1,809
143 out of 1,809 applicants to receive 100 H Shares
0.10%
9,000
1,447
117 out of 1,447 applicants to receive 100 H Shares
0.09%
10,000
8,015
662 out of 8,015 applicants to receive 100 H Shares
0.08%
20,000
5,262
506 out of 5,262 applicants to receive 100 H Shares
0.05%
30,000
3,951
416 out of 3,951 applicants to receive 100 H Shares
0.04%
40,000
2,438
273 out of 2,438 applicants to receive 100 H Shares
0.03%
50,000
1,830
216 out of 1,830 applicants to receive 100 H Shares
0.02%
60,000
3,453
423 out of 3,453 applicants to receive 100 H Shares
0.02%
Total
162,339
Total number of Pool A successful applicants: 8,167
– 16 –

<<<PAGE 17>>>
Pool B:
NO. OF H
SHARES
APPLIED
FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED OF
THE TOTAL NO.
OF H SHARES
APPLIED FOR
70,000
5,983
2,095 out of 5,983 applicants to receive 100 H Shares
0.05%
80,000
1,634
610 out of 1,634 applicants to receive 100 H Shares
0.05%
90,000
974
385 out of 974 applicants to receive 100 H Shares
0.04%
100,000
4,206
1,747 out of 4,206 applicants to receive 100 H Shares
0.04%
200,000
2,252
1,303 out of 2,252 applicants to receive 100 H Shares
0.03%
300,000
965
691 out of 965 applicants to receive 100 H Shares
0.02%
400,000
357
286 out of 357 applicants to receive 100 H Shares
0.02%
500,000
230
205 out of 230 applicants to receive 100 H Shares
0.02%
600,000
176
169 out of 176 applicants to receive 100 H Shares
0.02%
700,000
106
100 H Shares
0.01%
816,600
501
100 H Shares plus 68 out of 501 applicants to receive an
additional 100 H Shares
0.01%
Total
17,384
Total number of Pool B successful applicants: 8,098
As of the date of this announcement, the relevant subscription monies previously deposited in the
designated nominee accounts have been remitted back to the accounts of all HKSCC participants.
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of
which consent has been obtained, the Company has complied with the Listing Rules and guidance
materials in relation to the placing, allotment and listing of the H shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or indirectly,
provided by the Company, the Single Largest Shareholders, the Company’s directors or syndicate
members to any placees or the public (as the case may be) and the consideration payable by them
directly or indirectly for each Offer Share subscribed for or purchased by them is the same as the Offer
Price in addition to any brokerage, AFRC transaction levy, SFC transaction levy and trading fee
payable.
– 17 –

<<<PAGE 18>>>
OTHERS/ADDITIONAL INFORMATION
Allocations of Offer Shares to Cornerstone Investors and/or their close associates with consent
under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph 18 of
Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to allocate further Offer
Shares in the International Offering to Cornerstone Investors and/or their close associates as placees,
subject to the following conditions (the ‘‘Size-based Exemption’’):
(a)
the offer (excluding any over-allocation) has a total value of at least HK$1 billion;
(b) Offer Shares allocated to all existing shareholders and their close associates (whether as
Cornerstone Investors and/or as placees) as permitted under the Size-based Exemption do not
exceed 30% of the total number of Offer Shares;
(c)
each Director, chief executive of the Company and the Single Largest Shareholders has confirmed
that no securities have been allocated to them or their respective close associates under the Size-
based Exemption;
(d) the Company will comply with the public float requirement under Rule 8.08(1) of the Listing
Rules (as amended and replaced by Rule 19A.13A(1) of the Listing Rules for PRC issuers with no
other listed shares); and
(e)
details of the allocation to Cornerstone Investors and/or their close associates under the Size-based
Exemption will be disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted by
the Stock Exchange. For details of the allocations of Offer Shares to the Cornerstone Investors and/or
their close associates, please refer to the section headed ‘‘Allotment Results Details — Allottees with
Waivers/Consents Obtained’’ in this announcement.
– 18 –

<<<PAGE 19>>>
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a consent
under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such Offer Shares
in the International Offering to the connected clients. The allocation of Offer Shares to such connected
clients is in compliance with all the conditions set out in paragraph 6 of Chapter 4.15 of the Guide for
New Listing Applicants under the consent granted by the Stock Exchange. Details of the placement to
connected clients are set out below:
No.
Connected
Distributor
Connected
Client
Relationship between the
Connected Distributor and
the Connected Client
Whether the
Connected
Client is a
collective
investment
scheme which is
not authorized
by the SFC or is
expected to hold
the Offer Shares
on behalf of
such scheme
Number of
Offer Shares
intended to
be allocated
to the
Connected
Client
Approximate
percentage of
Offer Shares
allocated to the
Connected
Client under the
Global
OfferingNote 1
Approximate
percentage of
the total share
capital of the
Company upon
completion of
the Global
OfferingNote 1
Part A — Connected Clients holding securities on a Discretionary Basis on behalf of Independent Third Parties
1
CLSA
China AMC
HK
China AMC HK is a member
of the same group of
companies as CLSANote 2
No
3,000
0.02%
0.00%
2
CITIC Asset
Management
HK
CITIC Asset Management HK
is a member of the same
group of companies as
CLSANote 2
No
1,000
0.01%
0.00%
3
HTFH
China
Southern
China Southern is a member
of the same group of
HTFHNote 3
No
3,000
0.02%
0.00%
4
GTJAS
Fullgoal Fund
Fullgoal Fund is a member of
the same group of companies
as GTJAS
Note
4
YesNote 5
6,000
0.04%
0.01%
Part B — Connected Clients holding securities on a Non-Discretionary Basis on behalf of Independent Third Parties
5
CLSA
CSI
CapitalNote 6
CSI Capital is a member of
the same group of companies
as CLSANote 2
No
74,000
0.45%
0.07%
6
HTFH
HTCINote 7
HTCI is a member of the
same group of HTFH
No
2,000
0.01%
0.00%
– 19 –

<<<PAGE 20>>>
No.
Connected
Distributor
Connected
Client
Relationship between the
Connected Distributor and
the Connected Client
Whether the
Connected
Client is a
collective
investment
scheme which is
not authorized
by the SFC or is
expected to hold
the Offer Shares
on behalf of
such scheme
Number of
Offer Shares
intended to
be allocated
to the
Connected
Client
Approximate
percentage of
Offer Shares
allocated to the
Connected
Client under the
Global
OfferingNote 1
Approximate
percentage of
the total share
capital of the
Company upon
completion of
the Global
OfferingNote 1
7
GTJAS
Shanghai
Greenwoods
and GTINV
(in
connection
with
Greenwoods
OTC Swaps)
GTINV is a member of the
same group of companies as
GTJASNote 8
No
778,300Note 9
4.77%Note 9
0.71%Note 9
8
ICBC Wealth
Shanghai GTHT Securities
and GTJAS are members of
the same group of
companiesNote 10
No
518,800Note 9
3.18%Note 9
0.48%Note 9
Notes:
1.
Before any exercise of the Over-allotment Option.
2.
China AMC HK, CITIC Asset Management HK, and CSI Capital are subsidiaries of CITIC Securities Company
Limited. Each of China AMC HK, CITIC Asset Management HK, and CSI Capital is a member of the same group of
companies as CLSA, and accordingly, is considered as a ‘‘connected client’’ of CLSA pursuant to paragraph 1B of the
Placing Guidelines.
3.
Huatai Securities Co., Ltd. is the controlling shareholder of China Southern. HTFH is an indirectly wholly owned
subsidiary of Huatai Securities Co., Ltd.. China Southern is a member of the same group of companies as HTFH, and
accordingly, is considered as a ‘‘connected client’’ of HTFH pursuant to paragraph 1B of the Placing Guidelines.
4.
Fullgoal Fund is owned by Guotai Haitong Securities Co., Ltd as to 27.775%. GTJAS is a subsidiary of Guotai
Haitong Securities Co., Ltd. Fullgoal Fund is considered as a member of the same group of companies as GTJAS and
therefore is a ‘‘connected client’’ of GTJAS for the purpose of paragraph 1B of the Placing Guidelines.
5.
It is proposed that Fullgoal Fund participates as placee to subscribe for the Offer Shares under the International
Offering (the ‘‘Fullgoal Subscription’’).
– 20 –

<<<PAGE 21>>>
In relation to the Fullgoal Subscription, Fullgoal Fund will hold the Offer Shares in its capacity as the discretionary
fund manager on behalf of its funds (the ‘‘Fullgoal Ultimate Clients’’). Details of the Fullgoal Ultimate Clients are as
follows:
No.
Name of
Fullgoal
Ultimate Clients
Types and
values of asset
under
management
Scheme
establishment
date
Whether the
scheme is
publicly
marketed
Identities of
the general
partners and
the 20
largest
limited
partners of
the scheme
where
applicable
Identity of the
scheme
administrator
Relationships among the
scheme, the ultimate
beneficial owner(s)
(‘‘UBO(s)’’) of the limited
partner(s), the largest
group of the shareholders/
controlling shareholders of
the Company, and the
Company
1.
ICBC Fullgoal
China Small &
Mid Cap(HK
listed) Equity
Fund
Public Offering
of Fund
RMB3.55 billion
(First-quarter
reported data)
September 4,
2012
Publicly
marketed
Not
applicable
Fullgoal Fund
The scheme and UBOs are
independent third parties of
GTJAS, the Company and
the Single Largest
Shareholders.
2.
CMB-
FULLGOAL
BLUE CHIP
SELECTED
EQUITY
FUND(QDII)
Public Offering
of Fund
RMB1.6 billion
(First-quarter
reported data)
August 2, 2019
Publicly
marketed
Not
applicable
Fullgoal Fund
The scheme and UBOs are
independent third parties of
GTJAS, the Company and
the Single Largest
Shareholders.
3.
Fullgoal Global
Consumption
Selected Hybrid
Fund
Public Offering
of Fund
RMB1.69 billion
(First-quarter
reported data)
July 30, 2021
Publicly
marketed
Not
applicable
Fullgoal Fund
The scheme and UBOs are
independent third parties of
GTJAS, the Company and
the Single Largest
Shareholders.
Fullgoal Fund has confirmed that, to the best of their knowledge, (i) each of the Fullgoal Ultimate Clients and their
respective UBOs is an independent third party of (a) the Company, the connected person or the associates thereof;
and (b) Fullgoal Fund, GTJAS and the companies which are members of the same group of companies as GTJAS, (ii)
each of the Fullgoal Ultimate Clients is a collective investment scheme which is not authorised by the SFC; and (iii)
no single UBO holds 30% or more interest in any of the Fullgoal Ultimate Clients.
6.
CSI Capital and CITIC Securities Company Limited will enter into a series of cross border OTC swap transactions
(the ‘‘OTC Swaps’’) with the investment managers, who act for and on behalf of certain ultimate clients (collectively,
the ‘‘CSI Capital Ultimate Clients’’), pursuant to which CSI Capital will hold the Offer Shares to be subscribed for
and on behalf of the investment managers on a non-discretionary basis to hedge the OTC Swaps while the economic
risks and returns of the underlying Offer Shares are passed to the CSI Capital Ultimate Clients, subject to customary
fees and commissions. CSI Capital will not take part in any economic returns or bear any economic losses in relation
to the Offer Shares. The OTC Swaps will be fully funded by the CSI Capital Ultimate Clients. Each of the investment
managers and their UBOs is independent from each of the Company, its subsidiaries and substantial shareholders.
– 21 –

<<<PAGE 22>>>
The UBO information of the CSI Capital Ultimate Clients for purpose of this placee subscription is set out below:
No.
Name of CSI
Capital Ultimate Clients
UBO holding 30%
or more interest
in CSI Capital
Ultimate Client
Name of Investment Manager
(if applicable)
UBO holding 30%
or more interest in
Investment
Manager (if
applicable)
1.
Tongyi Taoli No. 1 Private
Securities Investment Fund
通怡桃李1號私募證券投資基金
Wang Jing
王靜
Shanghai Tongyi Investment
Management Co., Ltd.
上海通怡投資管理有限公司
Chu Yibo
儲貽波
2.
Tongyi Anxin No. 2 Private
Securities Investment Fund
通怡安鑫2號私募證券投資基金
Huang Shilin
黃世霖
Shanghai Tongyi Investment
Management Co., Ltd.
上海通怡投資管理有限公司
Chu Yibo
儲貽波
3.
Tongyi Taoli No. 10 Private
Securities Investment Fund
通怡桃李10號私募證券投資基金
None
Shanghai Tongyi Investment
Management Co., Ltd.
上海通怡投資管理有限公司
Chu Yibo
儲貽波
4.
Yucheng Xiangjiang Qiming
Private Securities Investment Fund
宇誠香江啟明私募證券投資基金
Li Jianxue
李建學
Yucheng Private Fund
Management (Hainan)
Partnership (Limited
Partnership)
宇誠私募基金管理（海南）合
夥企業（有限合夥）
Ma Shuying
馬曙瑩
5.
Yuemin Investment New Selected
Opportunity No. 1 Private
Securities Investment Fund
粵民投新選機遇1號私募證券投資
基金
Liu Wei
劉偉
Yuemin Investment Private
Securities Fund Management
(Shenzhen) Co., Ltd.
粵民投私募證券基金管理（深
圳）有限公司
None
6.
Yuanlesheng Qiangye Private
Securities Investment Fund
源樂晟強業私募證券投資基金
Hu Caiyang
胡彩陽
Tibet Yuanlesheng Asset
Management Co., Ltd.
西藏源樂晟資產管理有限公司
Zeng Xiaojie
曾曉潔
7.
Hover4pi Fund I OFC
None
Hover4pi Capital Management
He Hui
7.
HTCI is a member of the same group of HTFH.
HTFH is a non-syndicate sub-broker in connection with the Global Offering. Pursuant to an ISDA Agreement (the
‘‘ISDA Agreement’’), HTCI, which intends to participate in the Global Offering as a placee, will hold the beneficial
interest of the Offer Shares on a non-discretionary basis as the single underlying holder under a back-to-back total
return swap (the ‘‘Back-to-back TRS’’) to be entered by HTCI in connection with a Client TRS (as defined below)
placed by and fully funded (i.e. with no financing provided by HTCI) by the Huatai Ultimate Client (as defined
below), by which, HTCI will, subject to customary fees and commissions, pass the full economic exposure of the Offer
Shares to the Huatai Ultimate Client, which in effect, HTCI will hold the beneficial interest of the Offer Shares on
behalf of the Huatai Ultimate Client. Accordingly, HTCI is considered as a ‘‘connected client’’ of HTFH pursuant to
paragraph 1B of the Placing Guidelines.
– 22 –

<<<PAGE 23>>>
The offshore investor, being Lu Liyang 魯黎陽(the ‘‘Huatai Ultimate Client’’) will place a total return swap order
(the ‘‘Client TRS’’) with HTCI in connection with the Company’s initial public offering (the ‘‘IPO’’). In order to
hedge its exposure under the Client TRS, HTCI participates in the Company’s IPO and subscribes the Offer Shares
through placing order with HTFH during the International Offering.
To the best of the Company’s knowledge and after making all reasonable enquiries, the Huatai Ultimate Client is an
independent third party of (i) the Company, the connected person or the associates thereof, and (ii) HTCI, HTFH and
the companies which are members of the same group of HTCI.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Client TRS order placed by the Huatai
Ultimate Client. Pursuant to the terms of the Client TRS, during the tenor of the Client TRS, subject to customary fees
and commissions, all economic returns of the Offer Shares will be passed to the Huatai Ultimate Client through the
Client TRS and all economic loss shall be borne by the Huatai Ultimate Client. HTCI will not take any economic
return or bear any economic loss in relation to the Offer Shares.
The Huatai Ultimate Client may exercise an early termination right to terminate the Client TRS at any time from the
issue date of the Client TRS which should be on or after the date on which the Offer Shares are listed on the Stock
Exchange at his own discretion. Upon the termination upon maturity or early termination of the Client TRS by the
Huatai Ultimate Client, HTCI will dispose the Offer Shares on the secondary market and the Huatai Ultimate Client
will receive a final settlement amount of the Client TRS in cash in accordance with the terms and conditions of the
Client TRS which should have taken into account all the economic returns or economic loss in relation to the Offer
Shares. If upon the maturity of the Client TRS, the Huatai Ultimate Client intends to extend the investment period,
subject to further agreement between HTCI and the relevant Huatai Ultimate Client, the term of the Client TRS could
be extended by way of a new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through
the economic exposure to the Huatai Ultimate Client, being a client who places a Client TRS order with HTCI in
connection with the IPO of the Company. HTCI will not exercise the voting right of the Offer Shares during the tenor
of the Client TRS.
During the life of the Client TRS, HTCI may continue to hold the Offer Shares in its custodian account, or to hold
some or all of the Offer Shares in a prime brokerage account for stock borrowing purposes, where HTCI will lend out
its holding of underlying Offer Shares in the form of stock borrowing loans consistent with market practice to lower
its finance costs, provided that HTCI has the ability to call back the Offer Shares on loan at any time in order to
satisfy its obligations under the Client TRS to ensure the economic interests are ultimately passed to the Huatai
Ultimate Client.
8.
For details, please refer to note 7 to the section headed ‘‘International Offer — Allotees with Waivers/Consent
Obtained’’ in this announcement.
9.
Refer to Offer Shares subscribed for as a Cornerstone Investor.
10.
For details, please refer to note 8 to the section headed ‘‘International Offer — Allotees with Waivers/Consent
Obtained’’ in this announcement.
– 23 –

<<<PAGE 24>>>
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the
‘‘Stock Exchange’’) and Hong Kong Securities Clearing Company Limited (‘‘HKSCC’’) take no
responsibility for the contents of this announcement, make no representation as to its accuracy or
completeness and expressly disclaim any liability whatsoever for any loss howsoever arising from
or in reliance upon the whole or any part of the contents of this announcement.
This announcement is for information purposes only and does not constitute an invitation or offer to
acquire, purchase or subscribe for any securities. This announcement is not a prospectus. Potential
investors should read the Prospectus for detailed information about the Global Offering described
below before deciding whether or not to invest in the Offer Shares. Any investment decision in
relation to the Offer Shares should be taken solely in reliance on the information provided in the
Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the
United States (including its territories and possessions, any state of the United States and the
District of Columbia). This announcement does not, and is not intended to, constitute or form a part
of any offer to sell or solicitation to purchase or subscribe for any securities in the United States or
in any other jurisdiction. The Offer Shares have not been, and will not be, registered under the U.S.
Securities Act of 1933, as amended from time to time (the ‘‘U.S. Securities Act’’) or any securities
law of any state or other jurisdiction of the United States and may not be offered, sold, pledged, or
otherwise transferred within the United States, except pursuant to an exemption from, or in a
transaction not subject to, the registration requirements of the U.S. Securities Act and in
compliance with any applicable state securities laws. There will be no public offer of the Offer
Shares in the United States. The Offer Shares are being offered and sold solely outside the United
States in offshore transactions in reliance on Regulation S under the U.S. Securities Act.
Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-Overall
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) in their sole and
absolute discretion may, by notice in writing to the Company, terminate the Hong Kong
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in
the paragraph headed ‘‘Underwriting — Underwriting Arrangements and Expenses — The Hong
Kong Public Offering — Grounds for Termination’’ in the Prospectus at any time prior to 8:00 a.m.
(Hong Kong time) on the Listing Date (which is currently expected to be on June 30, 2026).
PUBLIC FLOAT
Pursuant to Rule 19A.13A of the Listing Rules, assuming that the Over-allotment Option is not
exercised, based on the Offer Price of HK$75.50 per Offer Share, the expected market capitalization
upon the Listing is HK$8,220.9 million, and the minimum prescribed public float percentage applicable
to the Shares is 18.25%. Immediately following completion of the Global Offering (assuming the Over-
allotment Option is not exercised), an aggregate of 63,969,014 H Shares, representing approximately
– 24 –

<<<PAGE 25>>>
58.74% of the issued share capital of the Company will count towards the public float. Therefore, the
number of H Shares held in public hands is higher than the prescribed percentage of H Shares required
to be held in public hands of 18.25% under Rule 19A.13A(1) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the Listing
Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be counted
towards the free float of the H Shares of the Company at the time of Listing. Based on the Offer Price
of HK$75.50 per H Share, the Company satisfies the free float requirement under Rule 19A.13C of the
Listing Rules.
The Directors confirm that immediately after the completion of the Global Offering (assuming the
Over-allotment Option is not exercised), (i) no placee will, individually, be placed more than 10% of
the enlarged issued share capital of the Company; (ii) there will not be any new substantial shareholder
(as defined in the Listing Rules) of the Company; (iii) the three largest public shareholders of the
Company do not hold more than 50% of the H Shares in public hands at the time of the Listing in
compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 H
Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, June 30,
2026 (Hong Kong time), provided that the Global Offering has become unconditional and the right of
termination described in the section headed ‘‘Underwriting — Underwriting Arrangements and
Expenses — Hong Kong Public Offering — Grounds for Termination’’ in the Prospectus has not been
exercised. Investors who trade the H Shares on the basis of publicly available allocation details prior to
the receipt of H Share certificates or prior to the H Share certificates becoming valid evidence of title
do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Tuesday, June 30,
2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange will
commence at 9:00 a.m. on Tuesday, June 30, 2026 (Hong Kong time). The H Shares will be traded in
board lots of 100 H Shares each, and the stock code of the H Shares will be 6715.
By order of the Board
Hangzhou Qiandaohu Xunlong Sci-tech Co., Ltd.
Wang Bin
Chairman, Executive Director and General Manager
Hangzhou, PRC, June 29, 2026
Directors of the Company named in the application to which this announcement relates are: (i) Mr. Wang Bin, Mr. Xia
Yongtao, Mr. Han Lei and Mr. Wang Zhigang as executive Directors; (ii) Mr. Dong Zhendong and Mr. Kong Deren as non-
executive Directors; and (iii) Dr. Sun Song, Ms. Fan Xinpeng and Ms. Song Xiumei as independent non-executive Directors.
– 25 –
