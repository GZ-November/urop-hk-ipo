# 配发结果公告抽取任务：6915.HK Jiangxi Institute of Biological Products Inc. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**29/06/2026 21:13**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0629/2026062902075.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6915.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
same meanings as those defined in the prospectus dated June 22, 2026 (the “Prospectus”) of
Jiangxi Institute of Biological Products Inc. (江西生物製品研究所股份有限公司) (the
“Company”).
This announcement is for information purposes only and does not constitute an invitation or
offer to acquire, purchase or subscribe for any securities. This announcement is not a
prospectus. Potential investors should read the Prospectus for detailed information about
the Global Offering described below before deciding whether or not to invest in the Offer
Shares. Any investment decision in relation to the Offer Shares should be taken solely in
reliance on the information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or
into the United States (including its territories and possessions, any state of the United
States and the District of Columbia). This announcement does not constitute or form a part
of any offer or solicitation to purchase or subscribe for securities in the United States or in
any other jurisdictions. The securities mentioned herein have not been, and will not be,
registered under the United States Securities Act of 1933 as amended from time to time (the
“U.S. Securities Act”) or securities law of any state or other jurisdiction of the United
States. The securities may not be offered, sold, pledged or otherwise transferred within the
United States except pursuant to an exemption from the registration requirements of the
U.S. Securities Act and in compliance with any applicable state securities laws, or outside
the United States unless in compliance with Regulation S under the U.S. Securities Act.
There will be no public offer of securities in the United States.
– 1 –

<<<PAGE 2>>>
In connection with the Global Offering, China International Capital Corporation Hong
Kong Securities Limited as stabilizing manager (the “Stabilizing Manager”) (or its
affiliates or any person acting for it), on behalf of the Underwriters, to the extent permitted
by the applicable laws and regulatory requirements of Hong Kong or elsewhere, may
over-allocate or effect transactions with a view to stabilizing or supporting the market price
of the H Shares at such price, in such amounts and in such manners as the Stabilizing
Manager, its affiliates or any person acting for it may determine and at a level higher than
that which might otherwise prevail for a limited period after the Listing Date. However,
there is no obligation on the Stabilizing Manager (or its affiliates or any person acting for
it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will be
conducted at the absolute discretion of the Stabilizing Manager (or its affiliates or any
person acting for it) and in what the Stabilizing Manager reasonably regards as the best
interest of the Company, (b) may be discontinued at any time and (c) is required to be
brought to an end within 30 days of the last day for lodging applications under the Hong
Kong Public Offering (which is Saturday, July 25, 2026). Such stabilizing action, if taken,
may be effected in all jurisdictions where it is permissible to do so, in each case in
compliance with all applicable laws, rules and regulatory requirements, including the
Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong
Kong), as amended, made under the Securities and Futures Ordinance (Chapter 571 of the
Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the
price of the H Shares for longer than the stabilization period, which will begin on the Listing
Date, and is expected to expire on the 30th day after the last day for lodging applications
under the Hong Kong Public Offering (which is Saturday, July 25, 2026). After this date,
when no further stabilizing action may be taken, demand for the H Shares, and therefore the
price of the H Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms
and conditions set out in the Prospectus. The Hong Kong Offer Shares will not be offered to
any person who is outside Hong Kong and/or not resident in Hong Kong. Potential investors
of the Offer Shares should note that the Joint Overall Coordinators (for themselves and on
behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong
Underwriting Agreement with immediate effect upon the occurrence of any of the events set
out in the section headed “Underwriting — Underwriting Arrangements and Expenses —
Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time
prior to 8: 00 a.m. on the Listing Date.
– 2 –

<<<PAGE 3>>>
Jiangxi Institute of Biological Products Inc.
江西生物製品研究所股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under the
Global Offering
:
36,234,500 H Shares (subject to the
Over-allotment Option)
Number of Hong Kong Offer Shares
:
3,623,500 H Shares
Number of International Offer Shares
:
32,611,000 H Shares (subject to the
Over-allotment Option)
Final Offer Price
:
HK$11.20 per H Share, plus brokerage of
1.0%, SFC transaction levy of 0.0027%,
AFRC transaction levy of 0.00015% and
the Stock Exchange trading fee of
0.00565% (payable in full on application
in Hong Kong Dollars, subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
6915
Joint Sponsors, Sponsor-Overall Coordinators, Joint Overall Coordinators,
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and
Joint Lead Manager
Joint Bookrunners and Joint Lead Managers
– 3 –

<<<PAGE 4>>>
Jiangxi Institute of Biological Products Inc.
江西生物製品研究所股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the
same meanings as those defined in the prospectus dated June 22, 2026 (the “Prospectus”)
issued by Jiangxi Institute of Biological Products Inc. (江西生物製品研究所股份有限公
司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of H
Shareholders, Shareholders and prospective investors should be aware that the price of
the H Shares could move substantially even with a small number of H Shares traded and
should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock Code
6915
Stock Short Name
JIANGXI BIO
Dealings commencement date
June 30, 2026*
*
see note at the end of the announcement
Price Information
Final Offer Price
HK$11.20
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the
Over-allotment Option)
36,234,500 H Shares
Final Number of Offer Shares in Hong Kong Public
Offering
3,623,500 H Shares
Final Number of Offer Shares in International
Offering (before exercise of the Over-allotment
Option)
32,611,000 H Shares
Number of issued Shares upon Listing (before exercise
of the Over-allotment Option)
308,377,319
– 4 –

<<<PAGE 5>>>
Over-allocation
No. of Offer Shares over-allocated
5,435,000 H Shares
Such over-allocated Offer Shares may be covered by exercising the Over-allotment Option or by making
purchases in the secondary market at prices that do not exceed the Offer Price or by a combination of
these means. In the event the Over-allotment Option is exercised, an announcement will be made on the
Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$405.83 million
Less: Estimated listing expenses payable based on
Final Offer Price
HK$67.03 million
Net proceeds
HK$338.80 million
Note:
Gross proceeds refer to the amount which the Company is entitled to receive. For details of the use
of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the
Prospectus. The Company will adjust the allocation of the net proceeds from the exercise of the
Over-allotment Option (if any) for the purposes as set out in the section headed “Future Plans and
Use of Proceeds” of the Prospectus on a pro rata basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
78,433
No. of successful applications
5,152
Subscription level
476.56 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong
Kong Public Offering
3,623,500 H Shares
No. of Offer Shares reallocated from the International
Offering
0 H Shares
Final no. of Offer Shares under the Hong Kong Public
Offering
3,623,500 H Shares
% of Offer Shares under the Hong Kong Public
Offering to the Global Offering (before exercise of the
Over-allotment Option)
10%
– 5 –

<<<PAGE 6>>>
Note:
For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to
https://www.hkeipo.hk/iporesult
to
perform
a
search
by
identification
document
number
or
https://www.hkeipo.hk/iporesult for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
63
Subscription Level
4.25 times
No. of Offer Shares initially available under the
International Offering
32,611,000 H Shares
No. of Offer Shares reallocated to the Hong Kong
Public Offering
0 H Shares
Final no. of Offer Shares under the International
Offering (before exercise of the Over-allotment
Option)
32,611,000 H Shares
% of Offer Shares under the International Offering to
the Global Offering (before exercise of the
Over-allotment Option)
90%
The Directors confirm that, to the best of their knowledge, information and belief, (i) none
of the Offer Shares subscribed by the placees and the public have been financed directly or
indirectly by the Company, any of the Directors, chief executive of the Company,
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company
or any of its subsidiaries or their respective close associates; and (ii) none of the placees
and the public who have purchased the Offer Shares are accustomed to taking instructions
from the Company, any of the Directors, chief executive of the Company, Controlling
Shareholders, substantial Shareholders, existing Shareholders of the Company or any of its
subsidiaries or their respective close associates in relation to the acquisition, disposal,
voting or other disposition of H Shares registered in his/her/its name or otherwise held by
him/her/it.
– 6 –

<<<PAGE 7>>>
The placees in the International Offering include the following:
Cornerstone Investor
InvestorNote 1
No. of Offer
Shares allocated
% of Offer
Shares
(assuming the
Over-allotment
Option is not
exercised)
% of total
issued share
capital in the
Company after
the Global
Offering
(assuming the
Over-allotment
Option is not
exercised)
Existing
shareholders or
their close
associates
Wealth Strategy Holding
Limited
4,464,000
12.32%
1.45%
No
Total
4,464,000
12.32%
1.45%
Note:
1.
For further details of the Cornerstone Investor, please refer to the section headed “Cornerstone
Investor” in the Prospectus.
– 7 –

<<<PAGE 8>>>
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of Shares
held in the
Company subject
to lock-up
undertakings upon
Listing
% of total issued
share capital in the
Company subject
to lock-up
undertakings upon
Listing (assuming
the Over-allotment
Option is not
exercised)
Last day subject
to the lock-up
undertakingsNote 1
Shenzhen Qianhai Tianzheng
Biotechnology Co., Ltd.
203,687,250
H Shares
66.05%
June 29, 2027
Hainan Zhizheng Biotechnology
Development Co., Ltd.
4,875,000
H Shares
1.58%
June 29, 2027
Total
208,562,250
67.63%
Notes:
1.
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law.
The required lock-up for the Controlling Shareholders ends on June 29, 2027, being the date twelve
months following the Listing Date. For illustrative purposes only, this subsection lists only those
members of the Controlling Shareholders who hold Shares directly in the Company. Pursuant to Rule
10.07 of the Listing Rules, each Controlling Shareholder (namely, Ms. Jing Yue, Shenzhen Qianhai
Tianzheng Biotechnology Co., Ltd. and Hainan Zhizheng Biotechnology Development Co., Ltd.) has
undertaken to the Stock Exchange and the Company that she or it shall comply with the applicable
lock-up requirements. For further details, please refer to the section headed “Underwriting —
Underwriting Arrangements and Expenses — Hong Kong Public Offering — Undertakings to the
Stock Exchange Pursuant to the Listing Rules — Undertakings by the Controlling Shareholders” in
the Prospectus.
2.
Upon completion of the Global Offering, 270,855,819 Domestic Shares will be converted into H
Shares on a one-for-one basis.
– 8 –

<<<PAGE 9>>>
Cornerstone Investor
Name
Number of Shares
held in the
Company subject
to lock-up
undertakings upon
Listing
% of total issued
share capital in the
Company subject
to lock-up
undertakings upon
Listing (assuming
the Over-allotment
Option is not
exercised)
Last day subject
to the lock-up
undertakingsNote 1
Wealth Strategy Holding Limited
4,464,000
H Shares
1.45%
December 29, 2026
Total
4,464,000
1.45%
Note:
1.
In accordance with the relevant cornerstone investment agreement, the required lock-up ends on
December 29, 2026. The Cornerstone Investor will cease to be prohibited from disposing of or
transferring H Shares subscribed pursuant to the relevant cornerstone investment agreement after the
indicated date.
Pre-IPO Investors
Name
Number of Shares
held in the
Company subject
to lock-up
undertakings upon
Listing
% of total issued
share capital in the
Company subject
to lock-up
undertakings upon
Listing (assuming
the Over-allotment
Option is not
exercised)
Last day subject
to the lock-up
undertakingsNote 1
Chifeng Bo-en Jingtian Technology Co.,
Ltd.
5,070,000
H Shares
1.64%
June 29, 2027
Chongqing Hanyi Cultural Exchange
Co., Ltd.
12,675,000
H Shares
4.11%
June 29, 2027
Shenzhen Xiangyi Investment Guarantee
Co., Ltd.
6,337,500
H Shares
2.06%
June 29, 2027
YANG Kun
3,315,000
H Shares
1.07%
June 29, 2027
Hainan Ruiqingxiang Investment
Partnership (Limited Partnership)
2,125,090
H Shares
0.69%
June 29, 2027
– 9 –

<<<PAGE 10>>>
Name
Number of Shares
held in the
Company subject
to lock-up
undertakings upon
Listing
% of total issued
share capital in the
Company subject
to lock-up
undertakings upon
Listing (assuming
the Over-allotment
Option is not
exercised)
Last day subject
to the lock-up
undertakingsNote 1
Jiaxing Jiaci Erhuijing Equity
Investment Partnership (Limited
Partnership)
1,287,000
Domestic Shares
0.42%
June 29, 2027
LIN Lin
975,000 H Shares
0.32%
June 29, 2027
XU Qinhong
780,000 H Shares
0.25%
June 29, 2027
OUYANG Guishou
585,000 H Shares
0.19%
June 29, 2027
RONG Zhiyao
585,000 H Shares
0.19%
June 29, 2027
WANG Pengjie
585,000 H Shares
0.19%
June 29, 2027
Chongqing Hanxin Pharmaceutical Co.,
Ltd.
507,000 H Shares
0.16%
June 29, 2027
Jiangsu Hailei Pharmaceutical Co., Ltd.
507,000 H Shares
0.16%
June 29, 2027
Shenzhen Heli No. 7 Investment Center
(Limited Partnership)
507,000 H Shares
0.16%
June 29, 2027
ZHANG Yiyu
468,000 H Shares
0.15%
June 29, 2027
WEN Yejuan
429,000 H Shares
0.14%
June 29, 2027
CHEN Guangai
390,000 H Shares
0.13%
June 29, 2027
LU Changying
390,000 H Shares
0.13%
June 29, 2027
ZHANG Zhide
390,000 H Shares
0.13%
June 29, 2027
MA Ying
292,500 H Shares
0.09%
June 29, 2027
LI Yulun
195,000 H Shares
0.06%
June 29, 2027
ZHANG Ruoshi
195,000 H Shares
0.06%
June 29, 2027
LONG Yehong
195,000 H Shares
0.06%
June 29, 2027
DAI Yujian
195,000 H Shares
0.06%
June 29, 2027
Shenzhen Lingyao Investment
Partnership (Limited Partnership)
136,500 H Shares
0.04%
June 29, 2027
ZHU Luwen
117,000 H Shares
0.04%
June 29, 2027
LUO Qian
117,000 H Shares
0.04%
June 29, 2027
– 10 –

<<<PAGE 11>>>
Name
Number of Shares
held in the
Company subject
to lock-up
undertakings upon
Listing
% of total issued
share capital in the
Company subject
to lock-up
undertakings upon
Listing (assuming
the Over-allotment
Option is not
exercised)
Last day subject
to the lock-up
undertakingsNote 1
LI Xiaoying
97,500 H Shares
0.03%
June 29, 2027
LU Ruiheng
97,500 H Shares
0.03%
June 29, 2027
SONG Hongxia
97,500 H Shares
0.03%
June 29, 2027
WEN Anhua
97,500 H Shares
0.03%
June 29, 2027
WU Hao
97,500 H Shares
0.03%
June 29, 2027
WU Hong
97,500 H Shares
0.03%
June 29, 2027
WU Jianying
97,500 H Shares
0.03%
June 29, 2027
ZHU Guiju
97,500 H Shares
0.03%
June 29, 2027
XU Quanhua
39,000 H Shares
0.01%
June 29, 2027
GUO Lihong
39,000 H Shares
0.01%
June 29, 2027
HE Qunhua
39,000 H Shares
0.01%
June 29, 2027
WANG Weiling
29,250 H Shares
0.01%
June 29, 2027
YU Xiaoyan
19,500 H Shares
0.01%
June 29, 2027
Total
40,296,340
13.07%
Notes:
1.
Under the applicable PRC laws, all existing Shareholders are subject to a lock-up period of twelve
months following the Listing Date.
2.
Upon completion of the Global Offering, 270,855,819 Domestic Shares will be converted into H
Shares on a one-for-one basis.
– 11 –

<<<PAGE 12>>>
Other Existing Shareholders
Name
Number of Shares
held in the
Company subject
to lock-up
undertakings upon
Listing
% of total issued
share capital in the
Company subject
to lock-up
undertakings upon
Listing (assuming
the Over-allotment
Option is not
exercised)
Last day subject
to the lock-up
undertakingsNote 1
Hainan Huafengming Investment
Partnership (Limited Partnership)
3,597,419
H Shares
1.17%
June 29, 2027
ZENG Hong
760,500 H Shares
0.25%
June 29, 2027
Hainan Gangyuanhao Investment
Partnership (Limited Partnership)
674,310 H Shares
0.22%
June 29, 2027
Ji’an Aohai Industrial Development Co.,
Ltd.
12,675,000
H Shares
4.11%
June 29, 2027
Haikou Tianshun Industrial
Development Co., Ltd.
4,563,000
H Shares
1.48%
June 29, 2027
LIU Yurui
1,014,000
H Shares
0.33%
June 29, 2027
Total
23,284,229
7.55%
Notes:
1.
Under the applicable PRC laws, all existing Shareholders are subject to a lock-up period of twelve
months following the Listing Date.
2.
Upon completion of the Global Offering, 270,855,819 Domestic Shares will be converted into H
Shares on a one-for-one basis.
– 12 –

<<<PAGE 13>>>
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of
H Shares allotted
Allotment as % of
International
Offering (assuming
no exercise
of the
Over-allotment
Option)
Allotment as % of
International
Offering (assuming
the Over- allotment
Option is fully
exercised and new
H Shares are
issued)
Allotment as % of
total Offer Shares
(assuming no
exercise of the
Over-allotment
Option)
Allotment as % of
total Offer Shares
(assuming the
Over-allotment
Option is fully
exercised and new
H Shares are
issued)
Number of
H Shares held
upon Listing
% of total
H Shares upon
Listing (assuming
no exercise
of the Over-
allotment Option)
% of total
H Shares upon
Listing (assuming
the Over-allotment
Option is fully
exercised and new
H Shares are
issued)
% of total issued
share capital upon
Listing (assuming
no exercise of the
Over-allotment
Option)
% of total
issued share capital
upon Listing
(assuming the
Over-allotment
Option is fully
exercised and new
H Shares are
issued)
Top 1
4,464,000
13.69%
11.73%
12.32%
10.71%
4,464,000
1.45%
1.43%
1.45%
1.42%
Top 5
16,814,500
51.56%
44.20%
46.40%
40.35%
16,814,500
5.48%
5.38%
5.45%
5.36%
Top 10
22,906,500
70.24%
60.21%
63.22%
54.97%
22,906,500
7.46%
7.33%
7.43%
7.30%
Top 25
32,869,000
100.79%
86.39%
90.71%
78.88%
32,869,000
10.70%
10.52%
10.66%
10.47%
Note:
*
Ranking of placees is based on the number of H Shares allotted to the placees.
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
Over-
allotment Option
is fully exercised
and new
H Shares are
issued)
Allotment as %
of total Offer
Shares (assuming
no exercise of
the Over-
allotment Option)
Allotment as %
of total Offer
Shares (assuming
the Over-
allotment Option
is fully exercised
and new
H Shares are
issued)
Number of
H Shares held
upon Listing
% of total issued
H share capital
upon Listing
(assuming no
exercise of the
Over-allotment
Option)
% of total issued
H share capital
upon Listing
(assuming the
Over-allotment
Option is fully
exercised and
new H Shares
are issued)
% of total issued
share capital
upon Listing
(assuming no
exercise of the
Over-allotment
Option)
% of total issued
share capital
upon Listing
(assuming the
Over-allotment
Option is fully
exercised
and new
H Shares are
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
208,562,250
67.92%
66.73%
67.63%
66.46%
208,562,250
Top 5
0
0.00%
0.00%
0.00%
0.00%
245,319,750
79.89%
78.50%
79.55%
78.17%
245,319,750
Top 10
11,979,000
36.73%
31.49%
33.06%
28.75%
266,219,669
86.69%
85.18%
86.33%
84.83%
266,219,669
Top 25
26,467,500
81.16%
69.57%
73.05%
63.52%
288,176,259
93.84%
92.21%
93.45%
91.83%
288,176,259
Note:
*
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number of
H Shares allotted
Allotment as % of
International
Offering (assuming
no exercise of the
Over-allotment
Option)
Allotment as % of
International
Offering (assuming
the Over-allotment
Option is fully
exercised and new
H Shares are
issued)
Allotment as % of
total Offer Shares
(assuming no
exercise of the
Over-allotment
Option)
Allotment as % of
total Offer Shares
(assuming the
Over-allotment
Option is fully
exercised and new
H Shares are
issued)
Number of
H Shares held
upon Listing
Number of Shares
held upon Listing
% of total issued
share capital upon
Listing (assuming
no exercise of the
Over-allotment
Option)
% of total issued
share capital upon
Listing (assuming
the Over-allotment
Option is fully
exercised and new
H Shares are
issued)
Top 1
0
0.00%
0.00%
0.00%
0.00%
208,562,250
208,562,250
67.63%
66.46%
Top 5
0
0.00%
0.00%
0.00%
0.00%
245,319,750
245,319,750
79.55%
78.17%
Top 10
11,979,000
36.73%
31.49%
33.06%
28.75%
266,219,669
266,219,669
86.33%
84.83%
Top 25
25,584,000
78.45%
67.24%
70.61%
61.40%
287,292,759
288,579,759
93.58%
91.96%
Note:
*
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon
Listing.
– 13 –

<<<PAGE 14>>>
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 78,433
valid applications made by the public will be conditionally allocated on the basis set out
below:
Pool A
Number of
H Shares
applied for
Number
of valid
applications
Basis of allocations/ballot
Approximate
percentage
allotted of the
total number of
H Shares
applied for
500
51,007
1,021 out of 51,007 applicants to receive 500 H Shares
2.00%
1,000
4,827
138 out of 4,827 applicants to receive 500 H Shares
1.43%
1,500
1,490
53 out of 1,490 applicants to receive 500 H Shares
1.19%
2,000
1,140
47 out of 1,140 applicants to receive 500 H Shares
1.03%
2,500
1,011
47 out of 1,011 applicants to receive 500 H Shares
0.93%
3,000
607
31 out of 607 applicants to receive 500 H Shares
0.85%
3,500
3,343
182 out of 3,343 applicants to receive 500 H Shares
0.78%
4,000
553
33 out of 553 applicants to receive 500 H Shares
0.75%
4,500
268
17 out of 268 applicants to receive 500 H Shares
0.70%
5,000
3,122
204 out of 3,122 applicants to receive 500 H Shares
0.65%
6,000
554
40 out of 554 applicants to receive 500 H Shares
0.60%
7,000
831
65 out of 831 applicants to receive 500 H Shares
0.56%
8,000
470
39 out of 470 applicants to receive 500 H Shares
0.52%
9,000
284
25 out of 284 applicants to receive 500 H Shares
0.49%
10,000
1,064
99 out of 1,064 applicants to receive 500 H Shares
0.47%
15,000
594
68 out of 594 applicants to receive 500 H Shares
0.38%
20,000
429
57 out of 429 applicants to receive 500 H Shares
0.33%
25,000
432
65 out of 432 applicants to receive 500 H Shares
0.30%
30,000
369
61 out of 369 applicants to receive 500 H Shares
0.28%
35,000
262
47 out of 262 applicants to receive 500 H Shares
0.26%
40,000
298
57 out of 298 applicants to receive 500 H Shares
0.24%
45,000
249
51 out of 249 applicants to receive 500 H Shares
0.23%
50,000
594
126 out of 594 applicants to receive 500 H Shares
0.21%
60,000
267
63 out of 267 applicants to receive 500 H Shares
0.20%
70,000
203
52 out of 203 applicants to receive 500 H Shares
0.18%
80,000
292
79 out of 292 applicants to receive 500 H Shares
0.17%
90,000
178
51 out of 178 applicants to receive 500 H Shares
0.16%
100,000
1,315
398 out of 1,315 applicants to receive 500 H Shares
0.15%
200,000
449
194 out of 449 applicants to receive 500 H Shares
0.11%
300,000
403
214 out of 403 applicants to receive 500 H Shares
0.09%
Total
76,905
Total number of Pool A successful applicants: 3,624
– 14 –

<<<PAGE 15>>>
Pool B
Number of
H Shares
applied for
Number
of valid
applications
Basis of allocations/ballot
Approximate
percentage
allotted of the
total number of
H Shares
applied for
400,000
707
1,000 H Shares
0.25%
500,000
192
1,000 H Shares plus 34 out of 192 applicants to
receive an additional 500 H Shares
0.22%
600,000
99
1,000 H Shares plus 30 out of 99 applicants to receive
an additional 500 H Shares
0.19%
700,000
38
1,000 H Shares plus 17 out of 38 applicants to receive
an additional 500 H Shares
0.17%
800,000
70
1,000 H Shares plus 38 out of 70 applicants to receive
an additional 500 H Shares
0.16%
900,000
53
1,000 H Shares plus 35 out of 53 applicants to receive
an additional 500 H Shares
0.15%
1,000,000
78
1,000 H Shares plus 58 out of 78 applicants to receive
an additional 500 H Shares
0.14%
1,200,000
56
1,000 H Shares plus 52 out of 56 applicants to receive
an additional 500 H Shares
0.12%
1,400,000
37
1,500 H Shares
0.11%
1,600,000
31
1,500 H Shares plus 7 out of 31 applicants to receive
an additional 500 H Shares
0.10%
1,811,500
167
1,500 H Shares plus 61 out of 167 applicants to
receive an additional 500 H Shares
0.09%
Total
1,528
Total number of Pool B successful applicants: 1,528
As of the date of this announcement, the relevant subscription monies previously deposited
in the designated nominee accounts have been remitted back to the accounts of all HKSCC
participants. Investors should contact their relevant brokers for any inquiries.
– 15 –

<<<PAGE 16>>>
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, the Company has complied with the Listing Rules and
guidance materials in relation to the placing, allotment and listing of the Company’s H
Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the
placees or the public (as the case may be) directly or indirectly for each Offer Share
subscribed for or purchased by them was the same as the final Offer Price in addition to
any brokerage, AFRC transaction levy, SFC transaction levy and Stock Exchange
trading fee payable.
– 16 –

<<<PAGE 17>>>
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong
Limited and Hong Kong Securities Clearing Company Limited take no responsibility for
the contents of this announcement, make no representation as to its accuracy or
completeness and expressly disclaim any liability whatsoever for any loss howsoever
arising from or in reliance upon the whole or any part of the contents of this
announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or
into the United States (including its territories and possessions, any state of the United
States and the District of Columbia) or any other jurisdiction where such distribution is
prohibited by law. This announcement does not constitute or form a part of any offer to
sell or solicitation of an offer to buy, to purchase or subscribe for securities nor shall there
be any sale of Offer Shares in the United States or in any other jurisdictions in which such
offer or solicitation would be unlawful. The securities mentioned herein have not been, and
will not be, registered under the United States Securities Act or any state securities law of
the United States. The securities may not be offered, sold, pledged, or transferred within
the United States or to, or for the account or benefit of U.S. persons (as defined in
Regulation S) except pursuant to an exemption from, or in a transaction not subject to,
the registration requirements of the U.S. Securities Act and in compliance with any
applicable state securities laws.
This announcement is for information purposes only and does not constitute an invitation
or offer to acquire, purchase or subscribe for securities of the Company. This
announcement is not a prospectus. Potential investors should read the Prospectus dated
June 22, 2026 issued by Jiangxi Institute of Biological Products Inc. (江西生物製品研究
所股份有限公司) for detailed information about the Global Offering described below
before deciding whether or not to invest in the Offer Shares.
* Potential investors of the Offer Shares should note that the Joint Overall Coordinators
(for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to
terminate their obligations under the Hong Kong Underwriting Agreement upon the
occurrence of any of the events set out in the paragraph headed “Underwriting —
Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for
Termination” in the Prospectus at any time prior to 8: 00 a.m. (Hong Kong time) on the
Listing Date (which is currently expected to be Tuesday, June 30, 2026).
– 17 –

<<<PAGE 18>>>
PUBLIC FLOAT AND FREE FLOAT
Rule 19A.13A of the Listing Rules requires that where the expected market value of the
Shares at the time of Listing is less than HK$6,000,000,000, at least 25% of the total
number of the Shares must at the time of the Listing be held by the public.
Immediately after the completion of the Global Offering (before any exercise of the
Over-allotment
Option),
an
aggregate
of
88,425,840
H
Shares,
representing
approximately 28.67% of the total issued share capital of the Company will be
counted towards the public float. Therefore, the Company will be able to meet the public
float requirement under Rule 19A.13A(1) of the Listing Rules.
Rule 19A.13C(1) of the Listing Rules provides that, where a new applicant is a PRC
issuer with no other listed shares at the time of listing, the portion of H shares for which
listing is sought that are held by the public and not subject to any disposal restrictions at
the time of listing must normally (i) represent at least 10% of the total number of issued
shares in the class to which H shares belong at the time of listing (excluding treasury
shares), with an expected market value at the time of listing of not less than
HK$50,000,000; or (ii) have an expected market value at the time of listing of not less
than HK$600,000,000.
Immediately after the completion of the Global Offering (before any exercise of the
Over-allotment Option), based on the Offer Price of HK$11.20, except for (i) 272,142,819
Shares held by all existing Shareholders that are subject to a lock-up period of twelve
months following the Listing Date under applicable PRC law; and (ii) 4,464,000 Shares
held by Cornerstone Investor that are subject to a lock-up period of six months from and
including the Listing Date, all remaining 31,770,500 Shares, representing approximately
10.30% of the total Shares, will be counted toward the free float. Therefore, the
Company will be able to satisfy the free float requirement under Rule 19A.13C(1)(a) of
the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8: 00 a.m. on Tuesday,
June 30, 2026 (Hong Kong time), provided that the Global Offering has become
unconditional and the right of termination described in the section headed “Underwriting
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds
for Termination” in the Prospectus has not been exercised. Investors who trade the H
Shares on the basis of publicly available allocation details prior to the receipt of H Share
certificates or prior to the H Share certificates becoming valid evidence of title do so
entirely at their own risk.
– 18 –

<<<PAGE 19>>>
Assuming that the Global Offering becomes unconditional at or before 8: 00 a.m. on
Tuesday, June 30, 2026 (Hong Kong time), it is expected that dealings in the H Shares on
the Stock Exchange will commence at 9: 00 a.m. on Tuesday, June 30, 2026 (Hong Kong
time). The H Shares will be traded in board lots of 500 H Shares each, and the stock code
of the H Shares will be 6915.
By order of the Board
Jiangxi Institute of Biological Products Inc.
Ms. JING Yue
Chairperson of the Board
Hong Kong, June 29, 2026
As of the date of this announcement, the Board of Directors of the Company comprises: (i)
Ms. JING Yue, Mr. YAO Xiaodong, Mr. LI Changqing and Ms. JING Ruihua as executive
Directors; (ii) Ms. YU Ailian and Mr. XIAO Changqing as non-executive Directors; and
(iii) Dr. ZOU Pingxue, Dr. TSANG Hiu Leong and Mr. WU Di as independent
non-executive Directors.
– 19 –
