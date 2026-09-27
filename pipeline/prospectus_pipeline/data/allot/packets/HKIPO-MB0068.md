# 配发结果公告抽取任务：0068.HK Manycore Tech Inc.

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**16/04/2026 20:59**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0416/2026041601684.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"0068.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
1
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) 
and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated April 9, 2026 (the “Prospectus”) issued by Manycore Tech Inc. (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities of the Company. This announcement is not a prospectus. Potential investors should read 
the Prospectus for detailed information about the Company and the Global Offering described below before deciding 
whether or not to invest in the Offer Shares. Any investment decision in relation to the Offer Shares should be taken 
solely in reliance on the information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not, and is not intended to, constitute or form a part of any offer to sell or solicitation to purchase 
or subscribe for any securities in the United States or in any other jurisdiction. The Offer Shares have not been, and 
will not be, registered under the U.S. Securities Act of 1933, as amended from time to time (the “U.S. Securities 
Act”) or securities law of any state or other jurisdiction of the United States and may not be offered, sold, pledged 
or otherwise transferred within the United States, except pursuant to an available exemption from, or in a transaction 
not subject to, the registration requirements of the U.S. Securities Act and in compliance with any applicable state 
securities laws. The Offer Shares are being offered and sold outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act, or in the United States to qualified institutional buyers in 
reliance on Rule 144A or any other available exemption from the registration requirements under the U.S. Securities 
Act.
In connection with the Global Offering, J.P. Morgan Securities (Asia Pacific) Limited, as stabilizing manager (the 
“Stabilizing Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, to the extent 
permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect 
transactions with a view to stabilizing or supporting the market price of the Shares at such price, in such amounts 
and in such manners as the Stabilizing Manager, its affiliates or any person acting for it may determine and at a 
level higher than that which might otherwise prevail for a limited period after the Listing Date. However, there is 
no obligation on the Stabilizing Manager (or its affiliates or any person acting for it) to conduct any such stabilizing 
action. Such stabilizing action, if taken, (a) will be conducted at the absolute discretion of the Stabilizing Manager (or 
its affiliates or any person acting for it) and in what the Stabilizing Manager reasonably regards as the best interest 
of the Company, (b) may be discontinued at any time and (c) is required to be brought to an end within 30 days 
of the last day for lodging applications under the Hong Kong Public Offering (which is Thursday, May 14, 2026). 
Such stabilizing action, if taken, may be effected in all jurisdictions where it is permissible to do so, in each case in 
compliance with all applicable laws, rules and regulatory requirements, including the Securities and Futures (Price 
Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures 
Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the Shares for longer 
than the stabilization period, which will begin on the Listing Date, and is expected to be brought to an end within 30 
days of the last day for lodging applications under the Hong Kong Public Offering (which is Thursday, May 14, 2026). 
After this date, when no further stabilizing action may be taken, demand for the Shares, and therefore the price of the 
Shares, could fall.
In connection with the Global Offering, J.P. Morgan Securities (Far East) Limited and CCB International Capital 
Limited act as the Joint Sponsors; and J.P. Morgan Securities (Asia Pacific) Limited and CCB International Capital 
Limited act as the Sponsor-Overall Coordinators and Overall Coordinators.
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on behalf of the 
Hong Kong Underwriters) shall be entitled to terminate the Hong Kong Underwriting Agreement with immediate effect 
upon the occurrence of any of the events set out in the section headed “Underwriting – Underwriting Arrangements 
and Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus at any time prior to 8:00 
a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Friday, April 17, 2026).

<<<PAGE 2>>>
2
Manycore Tech Inc.
(Incorporated in the Cayman Islands with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the Global 
Offering
:
160,619,000 Shares (subject to the Over-
allotment Option)
Number of Hong Kong Offer Shares
:
16,062,000 Shares
Number of International Offer Shares
:
144,557,000 Shares (subject to  
the Over-allotment Option)
Final Offer Price
:
HK$7.62 per Share plus brokerage of 1.0%, 
SFC transaction levy of  
0.0027%, AFRC transaction levy of  
0.00015% and the Stock Exchange  
trading fee of 0.00565% (payable in full  
on application in Hong Kong dollars,  
subject to refund)
Nominal value
:
US$0.000025 per Share
Stock code
:
00068
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
Manycore Tech Inc.
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated April 9, 2026 (the “Prospectus”) issued by 
Manycore Tech Inc. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the Shares could 
move substantially even with a small number of Shares traded and should exercise extreme 
caution when dealing in the Shares.
SUMMARY
Company information
Stock code
00068
Stock short name
MANYCORE TECH
Dealings commencement date
April 17, 2026*
*see note at the end of this announcement
Price Information
Final Offer Price
HK$7.62
Offer Price Range
HK$6.72 - HK$7.62
Offer Shares and Share Capital
Number of Offer Shares
160,619,000
Number of Offer Shares in Hong Kong Public Offering
16,062,000
Number of offer shares in International Offering
144,557,000
Number of issued shares upon Listing (before exercise of the 
Over-allotment Option)
1,700,106,840
Over-allocation
No. of Offer Shares over-allocated
24,092,500 Shares
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.

<<<PAGE 4>>>
4
Proceeds
Gross proceeds (before the exercise of the Over-allotment 
Option) (Note)
HK$1,223.9 million
Less: Estimated listing expenses payable based on final 
Offer Price
HK$131.9 million
Net proceeds
HK$1,092.0 million
Note: Gross proceeds refers to the amount to which the issuer is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” in the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
240,700
No. of successful applications
28,487
Subscription level
1,590.56 times
Reallocation
No
No. of Offer Shares initially available under the Hong Kong 
Public Offering
16,062,000
No. of Offer Shares reallocated from the International Offering
0
Final no. of Offer Shares under the Hong Kong Public Offering
16,062,000
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering (before the exercise of the Over-allotment 
Option)
10%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can 
refer to http://www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
http://www.eipo.com.hk/eIPOAllotment for the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
107
Subscription Level
14.46 times
No. of Offer Shares initially available under the International 
Offering
144,557,000
No. of Offer Shares reallocated to the Hong Kong Public Offering
0
Final No. of Offer Shares under the International Offering 
(before the exercise of the Over-allotment Option)
144,557,000
% of Offer Shares under the International Offering to the Global 
Offering (before the exercise of the Over-allotment Option)
90%

<<<PAGE 6>>>
6
The Directors confirm that, to the best of their knowledge, information and belief, save for a 
waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit the Company to allocate certain Offer Shares in the International Offering to an 
existing minority Shareholder and a close associate of existing minority Shareholders, (i) none of 
the Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, substantial shareholders, 
existing shareholders of the Company or any of its subsidiaries or their respective close associates; 
and (ii) none of the placees and the public who have purchased the Offer Shares are accustomed 
to taking instructions from the Company, any of the Directors, chief executive of the Company, 
substantial shareholders, existing shareholders of the Company or any of its subsidiaries or their 
respective close associates in relation to the acquisition, disposal, voting or other disposition of 
Shares registered in his/her/its name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
Investor(1)
No. of Offer 
Shares 
allocated as 
Cornerstone 
Investor(2)(3)
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing 
shareholders 
or their close 
associates
Taikang Life Insurance Co., 
Ltd (泰康人壽保險有限責
任公司) (“Taikang Life”)
13,369,500
8.32%
0.79%
No
Sunshine Life Insurance 
Corporation Limited 
(“Sunshine Life”)
10,284,000
6.40%
0.60%
No
GF Fund Management Co., 
Ltd. (廣發基金管理有限
公司) and GF International 
Investment Management 
Limited (廣發國際資產管
理有限公司) (together, “GF 
Fund”)
8,227,000
5.12%
0.48%
No
REDWOOD ELITE 
LIMITED (“Redwood”)
8,227,500
5.12%
0.48%
No
Mirae Asset Securities 
Co., Ltd. (“Mirae Asset 
Securities”)
5,142,000
3.20%
0.30%
No

<<<PAGE 7>>>
7
Investor(1)
No. of Offer 
Shares 
allocated as 
Cornerstone 
Investor(2)(3)
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing 
shareholders 
or their close 
associates
RIME Capital Limited 
(“RIME”)
5,142,000
3.20%
0.30%
No
Hesai Hong Kong Limited 
(“Hesai HK”)
3,085,000
1.92%
0.18%
No
Guohui (HK) Holdings Co., 
Limited (“Guohui HK”)
3,085,000
1.92%
0.18%
No
CR Construction Group 
Holdings Limited (“CR 
Construction”)
3,085,000
1.92%
0.18%
No
Total
59,647,000
37.14%
3.51%
Notes:
1. 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in 
the Prospectus.
2. 
Rounded down to the nearest whole board lot of 500 Shares, and is calculated based on the exchange rate 
set out in the section headed “Information about this Prospectus and the Global Offering – Exchange Rate 
Conversion” in the Prospectus.
3. 
In addition to the Offer Shares subscribed for as Cornerstone Investors, Taikang Life, Sunshine Life, 
GF Fund, Mirae Asset Securities, RIME, Hesai HK, Guohui HK as well as CR Construction and/or their 
respective close associates (collectively, the “Size-based Exemption Participants”), where applicable, were 
allocated further Offer Shares as placees in the International Offering. Please refer to the section headed 
“Allotment Results Details – International Offering – Allottees with Waiver/Consents Obtained” in this 
announcement for details. Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-
up as indicated below. For details, please refer to the section headed “Lock-up Undertakings – Cornerstone 
Investors” in this announcement.

<<<PAGE 8>>>
8
ALLOTTEES WITH WAIVER/CONSENTS OBTAINED
Investor
No. of Offer 
Shares 
allocated as 
placee
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total 
issued 
Shares after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Relationship
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations of further Shares to Cornerstone Investors and/or their close 
associate(Note 1)
Taikang Life
8,227,500
5.12%
0.48%
Cornerstone 
 Investor
Sunshine Life
6,125,000
3.81%
0.36%
Cornerstone 
 Investor
GF Fund
8,227,000
5.12%
0.48%
Cornerstone 
 Investor
Mirae Asset Securities
4,100,000
2.55%
0.24%
Cornerstone 
 Investor
RIME
970,000
0.60%
0.06%
Cornerstone 
 Investor
Hesai HK
2,020,000
1.26%
0.12%
Cornerstone 
 Investor
Guohui HK
2,020,000
1.26%
0.12%
Cornerstone 
 Investor
Zhejiang Construction 
International Limited 
(“Zhejiang 
Construction”) (Note 2)
3,085,000
1.92%
0.18%
Close 
 associate of 
 Cornerstone 
 Investor
Notes:
1. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details — Cornerstone Investors” in this announcement. For details of the consent under paragraph 
18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further Shares to 
the Cornerstone Investors and/or their respective close associates, please refer to the section headed “Others/
Additional Information – Allocations of Offer Shares to the Cornerstone Investors and/or their respective 
close associates with a consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants” 
in this announcement.
2. 
Zhejiang Construction is a close associate of CR Construction, a Cornerstone Investor.

<<<PAGE 9>>>
9
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total 
issued 
Shares after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Relationship
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations to connected clients(1)
ABCI Asset Management 
Limited (“ABCI AM”)
1,020,000
0.64%
0.06%
ABCI AM, 
ABCI Capital 
Limited and 
ABCI Securities 
Company 
Limited are 
group companies 
within the same 
group
Guotai Junan Investments 
(Hong Kong) Limited 
(“GTJA Investments”)
6,125,000
3.81%
0.36%
GTJA 
Investments 
is a member 
of the same 
group as Guotai 
Junan Securities 
(Hong Kong) 
Limited (“GTJA 
Securities”)
Note:
1. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to 
connected clients, please refer to the section headed “Others/Additional Information – Placing to connected 
clients with a prior consent under paragraph 1C(1) of the Placing Guidelines” in this announcement.

<<<PAGE 10>>>
10
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total 
issued 
Shares after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Relationship
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent 
under paragraph 1C(2) of the Placing Guidelines in relation to subscription for Shares by an 
existing minority Shareholder and a close associate of existing minority Shareholders(1)
Linear Venture, Ltd.
 (“Linear Venture”)
1,520,000
0.95%
0.09%
An existing 
shareholder
WONDER EDGE 
HOLDING LIMITED 
(“Wonder Edge”)(2)
1,020,000
0.64%
0.06%
A close associate 
of existing 
shareholders
Note:
1. 
The number of Offer Shares allocated to the relevant existing minority Shareholder and the relevant close 
associate of existing minority Shareholders listed in this subsection only represents the number of Offer 
Shares allocated to them as placees in the International Offering. For details of the consent under Rule 10.04 
of the Listing Rules and paragraph 1C(2) of the Placing Guidelines in relation to allocations of further Shares 
to an existing minority Shareholder and a close associate of existing minority Shareholders, please refer to 
the section headed “Others/Additional Information – Allocations of Offer Shares to an existing minority 
Shareholder and a close associate of existing minority Shareholders with a consent under Rule 10.04 of the 
Listing Rules and paragraph 1C(2) of the Placing Guidelines” in this announcement.
2. 
Planetree Partners I, L.P. (“Planetree Partners”), EXC Investment LLC (“EXC Investment”) and Planetree 
EXC Investment LLC (“Planetree EXC Investment”) are the existing shareholders of the Company, which 
hold approximately 1.05%, 0.45% and 0.62% of the total issued share capital of the Company immediately 
prior to the Global Offering respectively. Wonder Edge is ultimately controlled by Ng Yipin and therefore is 
a close associate of each of Planetree Partners, EXC Investment and Planetree EXC Investment.

<<<PAGE 11>>>
11
LOCK-UP UNDERTAKINGS
Warranting Shareholders
Name
Number of Shares 
held in the Company 
subject to lock-up 
undertaking upon 
Listing
% of Shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing (assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertaking(2)
Mr. Huang(1)
238,000,000
14.00%
October 16, 2026
Wintermatch 
International Limited 
(“Wintermatch”)(1)
238,000,000
14.00%
October 16, 2026
Notes:
1. 
Wintermatch is wholly-owned by Mr. Huang. Accordingly, Mr. Huang is deemed to be interested in the 
Shares held by Wintermatch.
2. 
The expiry date of the lock-up period shown in the table above is pursuant to voluntary undertaking made 
under the Hong Kong Underwriting Agreement.

<<<PAGE 12>>>
12
Pre-IPO Investors
Name
Number of Shares 
held in the 
Company 
subject to lock-up 
undertaking upon 
Listing
% of Shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-
allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertaking(1)
Mountain Glacier Investments 
Ltd.
17,000,000
1.00%
October 16, 2026
Aquanauts 3820 III L.P.
2,659,560
0.16%
October 16, 2026
IDG Technology Venture 
Investment IV, L.P.
120,000,000
7.06%
October 16, 2026
IDG Technology Venture 
Investment V, L.P.
78,589,226
4.62%
October 16, 2026
New Gultar Limited
17,892,733
1.05%
October 16, 2026
GGV Capital V L.P.
170,989,568
10.06%
October 16, 2026
GGV Capital V Entrepreneurs 
Fund L.P.
6,275,341
0.37%
October 16, 2026
MPC III L.P.
40,485,720
2.38%
October 16, 2026
MPC III-A L.P.
4,498,400
0.26%
October 16, 2026
Shanghai Yuanyan Enterprise 
Management Consulting 
Partnership (Limited 
Partnership)
15,718,514
0.92%
October 16, 2026
Shunwei Growth III Limited
133,307,402
7.84%
October 16, 2026
Astrend Opportunity III Alpha 
Limited
16,740,800
0.98%
October 16, 2026
HH SUM-I Holdings Limited
193,925,726
11.41%
October 16, 2026
HES VENTURES I, INC.
20,685,120
1.22%
October 16, 2026
HEARST VENTURES, INC.
13,888,371
0.82%
October 16, 2026
Planetree Partners I, L.P.
16,137,037
0.95%
October 16, 2026
EXC Investment LLC
6,972,018
0.41%
October 16, 2026
Planetree EXC Investment 
LLC
9,570,104
0.56%
October 16, 2026
Coatue PE Asia 36 LLC
53,678,200
3.16%
October 16, 2026

<<<PAGE 13>>>
13
Name
Number of Shares 
held in the 
Company 
subject to lock-up 
undertaking upon 
Listing
% of Shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-
allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertaking(1)
Coatue PE Asia 73 LLC
50,222,401
2.95%
October 16, 2026
QINGTING INVESTMENTS 
PTE. LTD.
19,207,311
1.13%
October 16, 2026
Linear Venture, Ltd.
1,477,485
0.09%
October 16, 2026
Total
1,009,921,037
59.40%
Notes:
1. 
The expiry date of the lock-up period shown in the table above is pursuant to voluntary undertaking.

<<<PAGE 14>>>
14
Existing Shareholders (other than the Warranting Shareholders and the Pre-IPO Investors)
Name
Number of Shares 
held in the 
Company 
subject to lock-up 
undertaking upon 
Listing
% of Shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-
allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertaking(1)
Ineffable International Limited
170,000,000
10.00%
October 16, 2026
Peekaboo International 
Limited
65,000,000
3.82%
October 16, 2026
Wide Future Group Limited
56,566,803
3.33%
October 16, 2026
Total
291,566,803
17.15%
Note:
1. 
The expiry date of the lock-up period shown in the table above is pursuant to voluntary undertaking.

<<<PAGE 15>>>
15
Cornerstone Investors
Name
Number of Shares 
held in the 
Company 
subject to lock-up 
undertaking upon 
Listing
% of Shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-
allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertaking(1)
Taikang Life
13,369,500
0.79%
October 16, 2026
Sunshine Life
10,284,000
0.60%
October 16, 2026
GF Fund
8,227,000
0.48%
October 16, 2026
Redwood
8,227,500
0.48%
October 16, 2026
Mirae Asset Securities
5,142,000
0.30%
October 16, 2026
RIME
5,142,000
0.30%
October 16, 2026
Hesai HK
3,085,000
0.18%
October 16, 2026
Guohui HK
3,085,000
0.18%
October 16, 2026
CR Construction
3,085,000
0.18%
October 16, 2026
Total
59,647,000
3.51%
Note:
1. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on October 
16, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or trading the Shares 
subscribed pursuant to the relevant cornerstone investment agreements after the indicated date.

<<<PAGE 16>>>
16
PLACEE CONCENTRATION ANALYSIS
Placees(1)
Number 
of Shares 
allotted
Allotment 
as % of 
International 
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
Option is 
exercised in full)
Allotment as % 
of total Offer 
Shares (assuming 
no exercise of the 
Over-allotment 
Option)
Allotment as % 
of total Offer 
Shares 
(assuming the 
Over-allotment 
Option is 
exercised in full)
Number 
of Shares 
held upon 
Listing
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
Option is 
exercised in full)
Top 1
21,597,000
14.94%
12.81%
13.45%
11.69%
21,597,000
1.27%
1.25%
Top 5
73,952,000
51.16%
43.85%
46.04%
40.04%
73,952,000
4.35%
4.29%
Top 10
106,286,500
73.53%
63.02%
66.17%
57.54%
106,286,500
6.25%
6.16%
Top 25
156,251,500
108.09%
92.65%
97.28%
84.59%
190,408,144
11.20%
11.04%
Note:
1. 
Ranking of placees is based on the number of Shares allotted to the places.
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders(1)
Number 
of Shares 
allotted
Allotment 
as % of 
International 
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
Option is 
exercised in full)
Allotment as % 
of total Offer 
Shares (assuming 
no exercise of the 
Over-allotment 
Option)
Allotment as % 
of total Offer 
Shares 
(assuming the 
Over-allotment 
Option is 
exercised in full)
Number 
of Shares 
held upon 
Listing
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
Option is 
exercised in full)
Top 1
0
0.00%
0.00%
0.00%
0.00%
238,000,000
14.00%
13.80%
Top 5
0
0.00%
0.00%
0.00%
0.00%
1,011,391,108
59.49%
58.66%
Top 10
0
0.00%
0.00%
0.00%
0.00%
1,431,890,834
84.22%
83.05%
Top 25
112,411,500
77.76%
66.65%
69.99%
60.86%
1,647,762,295
96.92%
95.57%
Note:
1. 
Ranking of Shareholders is based on the number of Shares held by the Shareholders upon Listing.

<<<PAGE 17>>>
17
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
Number 
of Shares 
applied for
Number 
of valid 
applications
Pool A
Approximate 
percentage 
allotted of the 
total number 
of Shares 
applied for
Basis of allocation/ballot
500
91,751
2,753 out of 91,751 to receive 500 Shares
3.00%
1,000
34,753
1,197 out of 34,753 to receive 500 Shares
1.72%
1,500
7,568
266 out of 7,568 to receive 500 Shares
1.17%
2,000
5,385
193 out of 5,385 to receive 500 Shares
0.90%
2,500
5,298
194 out of 5,298 to receive 500 Shares
0.73%
3,000
3,315
124 out of 3,315 to receive 500 Shares
0.62%
3,500
2,219
85 out of 2,219 to receive 500 Shares
0.55%
4,000
2,318
91 out of 2,318 to receive 500 Shares
0.49%
4,500
1,657
66 out of 1,657 to receive 500 Shares
0.44%
5,000
21,000
850 out of 21,000 to receive 500 Shares
0.40%
10,000
9,022
429 out of 9,022 to receive 500 Shares
0.24%
15,000
4,518
246 out of 4,518 to receive 500 Shares
0.18%
20,000
3,185
196 out of 3,185 to receive 500 Shares
0.15%
25,000
2,848
196 out of 2,848 to receive 500 Shares
0.14%
30,000
2,245
170 out of 2,245 to receive 500 Shares
0.13%
35,000
1,562
130 out of 1,562 to receive 500 Shares
0.12%
40,000
1,742
157 out of 1,742 to receive 500 Shares
0.11%
45,000
1,192
116 out of 1,192 to receive 500 Shares
0.11%
50,000
6,543
682 out of 6,543 to receive 500 Shares
0.10%
100,000
4,511
787 out of 4,511 to receive 500 Shares
0.09%
150,000
3,158
773 out of 3,158 to receive 500 Shares
0.08%
200,000
2,289
721 out of 2,289 to receive 500 Shares
0.08%
250,000
1,943
749 out of 1,943 to receive 500 Shares
0.08%
300,000
1,543
703 out of 1,543 to receive 500 Shares
0.08%
350,000
1,166
613 out of 1,166 to receive 500 Shares
0.08%
400,000
1,115
665 out of 1,115 to receive 500 Shares
0.07%
450,000
761
508 out of 761 to receive 500 Shares
0.07%
500,000
1,247
920 out of 1,247 to receive 500 Shares
0.07%
600,000
1,686
1,482 out of 1,686 to receive 500 Shares
0.07%
227,540
Total number of Pool A successful applicants: 16,062

<<<PAGE 18>>>
18
Number 
of Shares 
applied for
Number 
of valid 
applications
Pool B
Approximate 
percentage 
allotted of the 
total number 
of Shares 
applied for
Basis of allocation/ballot
700,000
4,684
4,076 out of 4,684 to receive 500 Shares
0.06%
800,000
1,513
1,386 out of 1,513 to receive 500 Shares
0.06%
900,000
908
500 Shares
0.06%
1,000,000
3,068
500 Shares plus 70 out of 3,068 to receive additional 500 Shares
0.05%
2,000,000
1,365
500 Shares plus 636 out of 1,365 to receive additional 500 Shares
0.04%
3,000,000
573
1,000 Shares
0.03%
4,000,000
283
1,000 Shares plus 108 out of 283 to receive additional 500 Shares
0.03%
5,000,000
187
1,000 Shares plus 158 out of 187 to receive additional 500 Shares
0.03%
6,000,000
96
1,500 Shares
0.03%
7,000,000
79
1,500 Shares plus 60 out of 79 to receive additional 500 Shares
0.03%
8,031,000
404
2,000 Shares
0.02%
13,160
Total number of Pool B successful applicants: 12,425
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Allocations of Offer Shares to the Cornerstone Investors and/or their respective close 
associates with a consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing 
Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph 
18 of Chapter 4.15 of the Guide to permit the Company to allocate further Offer Shares in the 
International Offering to the Size-based Exemption Participants as placees, subject to the following 
conditions:
(a) 
the final offering size of the Global Offering (assuming the Over-allotment Option is not 
exercised) exceeds the minimum offering size requirement of HK$1 billion in order for a 
size-based exemption to be granted;
(b) 
the Offer Shares allocated to all existing Shareholders and their close associates (whether 
as cornerstone investors and/or as placees) as permitted under this exemption do not exceed 
30% of the total number of Offer Shares offered under the Global Offering;

<<<PAGE 19>>>
19
(c) 
the Company does not have any controlling shareholder, and each Director and chief 
executive of the Company has confirmed that no Offer Shares in the Global Offering have 
been allocated to him/her or his/her respective close associates pursuant to the size-based 
exemption referred to in this submission;
(d) 
the allocation to the Size-based Exemption Participants will not affect the Company’s ability 
to satisfy the minimum public float requirement under Rule 8.08(1) of the Listing Rules; and
(e) 
the details of the allocation to the Size-based Exemption Participants will be disclosed in the 
allotment results announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange. For details of the allocations of Offer Shares to the Cornerstone 
Investors and/or their close associates, please refer to the section headed “Allotment Results 
Details – Allottees with Waiver/Consents Obtained” in this announcement.
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate the 
Offer Shares in the International Offering to the connected clients. The allocation of Offer Shares 
to such connected clients is in compliance with all the conditions under the consent granted by the 
Stock Exchange. Details of the placement to connected clients are set out below:
No.
Connected Distributor Connected Client
Relationship
Whether the 
connected client will 
hold the beneficial 
interests of the Offer 
Shares on a non-
discretionary basis or 
discretionary basis 
for independent third 
parties
Number of 
Offer Shares 
to be allocated 
to the 
connected 
client
Approximate 
percentage of 
Offer Shares 
allocated to the 
connected client 
(assuming the 
Over-allotment 
Option is not 
exercised)
Approximate 
percentage of 
total issued 
share capital 
after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
1.
ABCI Capital Limited 
(“ABCI Capital”) 
and ABCI Securities 
Company Limited 
(“ABCI Securities”)
ABCI Asset 
Management Limited 
(“ABCI AM”)(1)
ABCI AM, ABCI 
Capital and ABCI 
Securities are group 
companies within the 
same group
Discretionary basis
1,020,000
0.64%
0.06%
2.
Guotai Junan Securities 
(Hong Kong) Limited 
(“GTJA Securities”)
Guotai Junan 
Investments 
(Hong Kong) 
Limited (“GTJA 
Investments”)(2)
GTJA Investments is 
a member of the 
same group as GTJA 
Securities
Non-discretionary basis
6,125,000
3.81%
0.36%

<<<PAGE 20>>>
20
Notes:
1. 
ABCI AM is a member of the same group of companies as ABCI Capital and ABCI Securities, and ABCI AM is 
therefore a “connected client” of ABCI Capital and ABCI Securities.
ABCI AM intends to hold the Offer Shares in its capacity as manager managing investment portfolios on behalf 
of underlying investors (the “ABCI AM Ultimate Clients”) who are independent third parties on a discretionary 
basis.
To the best knowledge of ABCI AM, each of the ABCI AM Ultimate Clients is an independent third party of the 
Company, its subsidiaries, its substantial shareholders, ABCI Capital, ABCI Securities and the companies which 
are members of the same group of companies as ABCI Capital and ABCI Securities.
ABCI AM also confirms that it will not hold any Offer Shares placed to it on a proprietary basis for itself or for 
any group member of ABCI, and the Offer Shares will be held by it on behalf of independent third parties.
2. 
GTJA Investments shall hold the Offer Shares for hedging purpose as the single underlying asset of a 
back-to-back total return swap transaction (the “GTHT Back-to-back TRS”) to be entered into between GTJA 
Investments and Guotai Haitong Securities Co., Ltd. (the “GTHT Onshore Parent”) in connection with the 
total return swap order (the “GTHT Client TRS”) to be entered into by GTHT Onshore Parent and the ultimate 
client (the “GTHT Onshore Ultimate Client”), respectively. Such GTHT Client TRS is to be fully funded 
by the GTHT Onshore Ultimate Client. GTJA Investments will hold the Offer Shares on a non-discretionary 
basis for the purpose of hedging the economic exposure under the GTHT Back-to-back TRS and GTHT Client 
TRS only, During the tenor of the GTHT Client TRS, all economic returns of the Offer Shares will be passed 
to the GTHT Onshore Ultimate Client and all economic losses shall be borne by the GTHT Onshore Ultimate 
Client, subject to the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS, and GTJA 
Investments will not take part in any economic return or bear any economic loss in relation to the price of the 
Offer Shares. The GTHT Onshore Ultimate Client may request to redeem the Offer Shares at its own discretion, 
upon which GTJA Investments shall dispose of the Offer Shares and settle the GTHT Back-to-back TRS and 
GTHT Client TRS in cash in accordance with the terms and conditions of the GTHT Back-to-back TRS and 
GTHT Client TRS documents. Due to its internal policy, GTJA Investments will not exercise the voting right 
attaching to the Offer Shares during the tenor of the GTHT Back-to-back TRS and GTHT Client TRS.
To the best knowledge of GTJA Investments and after making all reasonable enquiries, (i) each of the GTHT 
Onshore Ultimate Client and the ultimate beneficial owner(s) holding 30% or more interest of the GTHT 
Onshore Ultimate Client is an independent third party of GTJA Investments, GTJA Securities and the companies 
which are members of the same group of companies as GTJA Securities, and (ii) GTJA Investments is not a 
collective investment scheme which is not authorised by the SFC nor is expected to hold the Offer Shares on 
behalf of such scheme. For the Stock Exchange’s information, the GTHT Onshore Ultimate Client is a domestic 
private fund, Duxi Bingtai Renaissance No. 18 Private Securities Investment Fund (篤熙稟泰文藝復興18號私
募證券投資基金), managed by Shanghai Duxi Bingtai Private Equity Fund Management Co., Ltd. (上海篤熙
稟泰私募基金管理有限公司) (“Shanghai Duxi Bingtai”) on a discretionary basis, with investment decisions 
independently made by Shanghai Duxi Bingtai’s fund managers. Shanghai Duxi Bingtai is held by Tang Fuquan 
(唐福全) and Liu Jie (劉潔) as to 99.00% and 1.00%, respectively.

<<<PAGE 21>>>
21
Allocations of Offer Shares to an existing minority Shareholder and a close associate of 
existing minority Shareholders with a consent under Rule 10.04 of the Listing Rules and 
paragraph 1C(2) of the Placing Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, consent 
under Rule 10.04 of the Listing Rules and paragraph 1C(2) of the Placing Guidelines to permit 
the Company to allocate the Offer Shares in the International Offering to an existing minority 
Shareholder and a close associate of existing minority Shareholders as placees, subject to the 
following conditions:
(a) 
each of (i) Linear Venture; and (ii) Planetree Partners, EXC Investment LLC and Planetree 
EXC Investment LLC (together, the “Permitted Existing Shareholders”) (on an aggregate 
basis), holds less than 5% of the Company’s voting rights prior to the Listing;
(b) 
each of the Permitted Existing Shareholders is not and will not be, a core connected person of 
our Company or any close associate of any such core connected person immediately prior to 
or following the Global Offering;
(c) 
each of the Permitted Existing Shareholders does not have the power to appoint any Director 
and/or have any other special rights;
(d) 
allocation to Linear Venture and Wonder Edge will not affect the Company’s ability to 
satisfy the public float requirement under Rule 8.08 of the Listing Rules;
(e) 
no preferential treatment has been, nor will be, given to Linear Venture or Wonder Edge by 
virtue of their relationship with the Company in any allocation in the International Offering; 
and
(f) 
each of the Company, the Joint Sponsors and the Overall Coordinators will provide the Stock 
Exchange with written confirmations in accordance with Chapter 4.15 of the Guide.
The allocation of Offer Shares to the existing Shareholders and/or their close associates as placees 
is in compliance with all the conditions under the consent granted by the Stock Exchange.
For details of the allocations of Offer Shares to the existing Shareholders and/or their close 
associates, please refer to the section headed “Allotment Results Details – Allottees with Waivers/
Consents Obtained” in this announcement.

<<<PAGE 22>>>
22
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the 
“Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy 
or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and the 
District of Columbia). This announcement does not, and is not intended to, constitute or form a 
part of any offer to sell or solicitation to purchase or subscribe for any securities in the United 
States or in any other jurisdiction. The Offer Shares have not been, and will not be, registered 
under the U.S. Securities Act of 1933, as amended from time to time (the “U.S. Securities Act”) 
or securities law of any state or other jurisdiction of the United States and may not be offered, 
sold, pledged or otherwise transferred within the United States, except pursuant to an available 
exemption from, or in a transaction not subject to, the registration requirements of the U.S. 
Securities Act and in compliance with any applicable state securities laws. There will be no 
public offer of the Offer Shares in the United States.
The Offer Shares are being offered and sold outside the United States in offshore transactions 
in reliance on Regulation S under the U.S. Securities Act, or in the United States to qualified 
institutional buyers in reliance on Rule 144A or any other available exemption from the 
registration requirements under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an offer or an 
invitation to induce an offer by any person to acquire, purchase or subscribe for any securities 
of the Company. This announcement is not a prospectus. Potential investors should read the 
Prospectus dated April 9, 2026 issued by the Company for detailed information about the 
Company and the Global Offering described below before deciding whether or not to invest in 
the Shares. Any investment decision in relation to the Offer Shares should be taken solely in 
reliance on the information provided in the Prospectus.
* Potential investors of the Offer Shares should note that the Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the 
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the 
events set out in the section headed “Underwriting — Underwriting Arrangements and Expenses 
— Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior 
to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Friday, 
April 17, 2026).

<<<PAGE 23>>>
23
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering, approximately 35.34% of our total issued 
Shares upon the completion of the Global Offering (before any exercise of the Over-allotment 
Option) will be counted towards public float, which is higher than the prescribed percentage of 
Shares required to be held in public hands of 15% which is the minimum prescribed public float 
percentage applicable to our Shares under Rule 8.08 of the Listing Rules, thereby satisfying Rule 
8.08(1) of the Listing Rules at the time of the Listing.
Based on the final Offer Price of HK$7.62 per Share, the Company satisfies the free float 
requirement under Rule 8.08A of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering: (i) no placee 
will, individually, be placed more than 10% of the enlarged issued share capital of the Company 
immediately after the Global Offering; (ii) there will not be any new substantial Shareholder under 
the Listing Rules immediately after the Global Offering; (iii) the three largest public shareholders 
of the Company do not hold more than 50% of the Shares in public hands at the time of the Listing 
in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 
Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
Share certificates will only become valid evidence of title at 8:00 a.m. (Hong Kong time) 
on Friday, April 17, 2026, provided that the Global Offering has become unconditional and 
the right of termination described in the section headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” in 
the Prospectus has not been exercised. Investors who trade Shares prior to the receipt of Share 
certificates or the Share certificates becoming valid evidence of title do so entirely at their own 
risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong Kong 
time) on Friday, April 17, 2026, it is expected that dealings in the Shares on the Stock Exchange 
will commence at 9:00 a.m. on Friday, April 17, 2026. The Shares will be traded in board lots of 
500 Shares each. The stock code of the Shares will be 00068.
By order of the Board
Manycore Tech Inc.
Mr. Huang Xiaohuang
Chairman of the Board and Executive Director
Hong Kong, April 16, 2026
Directors and proposed directors of the Company named in the application to which this 
announcement relates are: (i) Mr. Huang Xiaohuang, Mr. Chen Hang, Mr. Zhu Hao and Mr. Shen 
Bei as executive Directors; (ii) Mr. Foo Ji-xun and Mr. Tan Zhiqian as non-executive Directors; 
and (iii) Ms. Chen Lianqing, Mr. Ge Ke and Mr. Yeung Kwok On as proposed independent non-
executive Directors.
