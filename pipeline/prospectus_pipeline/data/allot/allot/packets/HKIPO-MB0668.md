# 配发结果公告抽取任务：0668.HK Anker Innovations Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**30/06/2026 22:40**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0630/2026063003481.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"0668.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not, and is not intended to, constitute or form a part of any offer or solicitation to purchase or 
subscribe for securities in the United States or in any other jurisdiction. The Offer Shares have not been and will not 
be registered under the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities 
Act”) or securities law of any state or other jurisdiction of the United States and may not be offered, sold, pledged or 
otherwise transferred within the United States, except in transactions exempt from, or not subject to, the registration 
requirements of the U.S. Securities Act and in compliance with any applicable state securities laws. The Offer Shares 
are being offered and sold (i) within the United States solely to “Qualified Institutional Buyers” as defined in Rule 
144A pursuant to an exemption from registration under the U.S. Securities Act and (ii) outside the United States in 
offshore transactions in accordance with Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. Potential investors should read the Prospectus for detailed information about the Company 
and the Global Offering described below before deciding whether or not to invest in the Offer Shares.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated June 23, 2026 (the “Prospectus”) issued by Anker Innovations Technology Co., Ltd. 
(安克創新科技股份有限公司) (the “Company”).
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited as 
stabilizing manager (the “Stabilization Manager”) (or its affiliates or any person acting for it), on behalf of the 
Underwriters, to the extent permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, 
may over-allocate or effect transactions with a view to stabilizing or supporting the market price of the H Shares at 
such price, in such amounts and in such manners as the Stabilizing Manager, its affiliates or any person acting for it 
may determine and at a level higher than that which might otherwise prevail for a limited period after the Listing Date. 
However, there is no obligation on the Stabilizing Manager (or its affiliates or any person acting for it) to conduct 
any such stabilizing action. Such stabilizing action, if taken, (a) will be conducted at the absolute discretion of the 
Stabilization Manager (or its affiliates or any person acting for it) and in what the Stabilizing Manager reasonably 
regards as the best interest of our Company, (b) may be discontinued at any time and (c) is required to be brought to 
an end within 30 days of the last day for lodging applications under the Hong Kong Public Offering (being Sunday, 
July 26, 2026). Such stabilizing action, if taken, may be effected in all jurisdictions where it is permissible to do so, 
in each case in compliance with all applicable laws, rules and regulatory requirements, including the Securities and 
Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities 
and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (being Sunday, July 26, 2026). After 
this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of the H 
Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out 
in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/
or not resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint Sponsors and the 
Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate 
their obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of 
the events set out in the section headed “Underwriting – Underwriting Arrangements – Hong Kong Public Offering – 
Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date.

<<<PAGE 2>>>
2
Anker Innovations Technology Co., Ltd.
安克創新科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the 
Global Offering
:
46,632,800 H Shares (subject to 
 the Over-allotment Option)
Number of Hong Kong Offer Shares :
4,663,300 H Shares
Number of International Offer Shares :
41,969,500 H Shares (subject to 
 the Over-allotment Option)
Final Offer Price :
HK$99.32 per H Share, plus brokerage of 
 1.0%, SFC transaction levy of 0.0027%, 
 AFRC transaction levy of 0.00015% and 
 Stock Exchange trading fee of 0.00565%
Nominal value :
RMB1.00 per H Share 
Stock code :
00668
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers
(in alphabetical order)

<<<PAGE 3>>>
3
Anker Innovations Technology Co., Ltd.
安克創新科技股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company Information
Stock Code
00668
Stock Short Name
ANKER
Dealings commencement date
July 2, 2026*
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$99.32
Offer Shares and Share Capital
Number of Offer Shares*
46,632,800
Final Number of Offer Shares in Hong 
Kong Public Offering
4,663,300
Final Number of Offer Shares in 
International Offering*
41,969,500
Number of issued Shares upon Listing 
(before exercise of the Over-allotment 
Option)
582,909,162
* 
without taking into account any exercise of the Over-allotment Option.
Offer Size Adjustment Option (Upsize option)
Number of additional Shares issued under 
the option
N/A
– Hong Kong Public Offering
N/A
– International Offering
N/A
The Offer Size Adjustment Option was not exercised.

<<<PAGE 4>>>
4
Over-allocation
No. of Offer Shares over-allocated
6,994,900
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$4,631.6 million
Less: 
Estimated listing expenses payable 
based on Offer Price
HK$108.9 million
Net Proceeds
HK$4,522.7 million
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details 
of the use of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” 
of the Prospectus. The Company will adjust the allocation of the net proceeds from the exercise 
of the Over-allotment Option (if any) for the purposes as set out in the section headed “Future 
Plans and Use of Proceeds” of the Prospectus on a pro rata basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
36,424
No. of successful applications
18,453
Subscription level
27.57 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong Public 
Offering
4,663,300
Final no. of Offer Shares under the Hong Kong Public Offering
4,663,300
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering
10%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can 
refer to www.eipo.com.hk/eIPOAllotment to perform a search identification number or www.eipo.
com.hk/eIPOAllotment for the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
137
Subscription Level
10.24 times
No. of Offer Shares initially available under 
the International Offering
41,969,500
Final no. of Offer Shares under the 
International Offering
41,969,500
% of Offer Shares under the International 
Offering to the Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for 
(a) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the 
Stock Exchange to permit H Shares in the International Offering to be placed to certain Existing 
Minority Shareholders and/or their close associates, and (b) a consent under Chapter 4.15 of the 
Guide for New Listing Applicants to permit the Company to, among other things, allocate further 
H Shares in the International Offering to certain Cornerstone Investors (including those who are 
close associate(s) of an existing Shareholder) and/or their respective close associates, (i) none of 
the Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, Controlling Shareholders, 
substantial Shareholders, existing Shareholders or any of the Company’s subsidiaries or their 
respective close associates; and (ii) none of the placees and the public who have purchased the 
Offer Shares are accustomed to taking instructions from the Company, any of the Directors, 
chief executive of the Company, Controlling Shareholders, substantial Shareholders, existing 
Shareholders or any of the Company’s subsidiaries or their respective close associates in relation 
to the acquisition, disposal, voting or other disposition of H Shares registered in his/her/its name or 
otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of 
Offer 
Shares 
allocated
Approximate 
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Existing 
Shareholders 
or their close 
associates
Schroder Investment Management (Singapore) Ltd 
and Schroder Investment Management (Hong Kong) 
Limited (“Schroders”)
5,522,200
11.84%
0.95%
Yes
Aspex Master Fund (“Aspex”)
3,944,400
8.46%
0.68%
No

<<<PAGE 6>>>
6
Investor
No. of 
Offer 
Shares 
allocated
Approximate 
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Existing 
shareholders 
or their close 
associates
Principal Asset Management Company (Asia) 
Limited (“PAMAL”)
3,155,500
6.77%
0.54%
No
Greenwoods Asset Management Hong Kong Limited 
(“HK Greenwoods”)
1,186,800
2.54%
0.20%
No
Guotai Junan Investments (Hong Kong) Limited 
(“GTINV”) and Shanghai Greenwoods Asset 
Management Co., Ltd. (“Shanghai Greenwoods”) (in 
connection with the Greenwoods OTC Swaps) Note 2
785,400
1.68%
0.13%
No
HACF, L.P.
1,577,700
3.38%
0.27%
No
UBS Asset Management (Singapore) Ltd. (“UBS 
AM Singapore”)
1,577,700
3.38%
0.27%
Yes
Franklin Templeton Sealand Fund Management 
Co., Ltd. (國海富蘭克林基金管理有限公司) (“FT 
Sealand”)
1,183,300
2.54%
0.20%
Yes
Jane Street Asia Trading Limited (“Jane Street”)
1,183,300
2.54%
0.20%
No
Taikang Life Insurance Co., Ltd (泰康人壽保險有限
責任公司) (“Taikang Life”)
1,183,300
2.54%
0.20%
Yes
WT Asset Management Limited (“WT Asset 
Management”)
1,183,300
2.54%
0.20%
No
Value Partners Hong Kong Limited and Value 
Partners Limited (“Value Partners”)
788,800
1.69%
0.14%
Yes
Total
23,271,700
49.90%
3.99%
Notes:
1. 
In addition to the Offer Shares subscribed for as Cornerstone Investors, Schroders, Aspex, PAMAL, HK 
Greenwoods, Shanghai Greenwoods, FT Sealand, Jane Street, Taikang Life, WT Asset Management, Value 
Partners and/or their respective close associates, where applicable, were allocated further Offer Shares as placees 
in the International Offering. Please refer to the section headed “Allotment Results Details – International Offer 
– Allottees with Waivers/Consents Obtained” in this announcement for details. Only the Offer Shares subscribed 
for as Cornerstone Investors are subject to lock-up as indicated below. For details, please refer to the section 
headed “Lock-up Undertakings – Cornerstone Investors” in this announcement.
2. 
For the purpose of subscription of Offer Shares under the cornerstone tranche, GTINV and Guotai Haitong 
Securities Co., Ltd. will enter into a series of cross border delta-one OTC swap transactions with each 
other, and with Shanghai Greenwoods acting in its capacity as investment manager for and on behalf of its 
underlying funds. GTIVN is an existing shareholder of the Company.

<<<PAGE 7>>>
7
Allottees with waivers/consents obtained
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering 
(assuming 
the Over- 
allotment 
Option is not 
exercised)
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by Existing 
Minority Shareholders holding more than 1% of the issued share capital of the Company immediately 
prior to the completion of the Global Offering and/or their close associates Note 1
Schroders
8,835,200 Note 2
18.95%
1.52%
An existing Shareholder and 
a Cornerstone Investor
Allottees with consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocations of further Shares to existing Shareholders and Cornerstone Investors and/or their close 
associatesNote 2
Schroders
3,313,000
7.10%
0.57%
An existing Shareholder and 
a Cornerstone Investor
Aspex
2,090,000
4.48%
0.36%
A Cornerstone Investor
PAMAL
304,000
0.65%
0.05%
A Cornerstone Investor
HK Greenwoods
497,000
1.07%
0.09%
A Cornerstone Investor
Shanghai Greenwoods Note 3
449,000
0.96%
0.08%
A Cornerstone Investor
FT Sealand
181,000
0.39%
0.03%
A close associate of an 
existing Shareholder and a 
Cornerstone Investor
Franklin Templeton 
Investments (Asia) 
Limited Note 4
788,000
1.69%
0.14%
A close associate of an 
existing Shareholder and 
a close associate of a 
Cornerstone Investor
Jane Street Financial
Limited Note 5
118,000
0.25%
0.02%
A close associate of a
Cornerstone Investor
Taikang Life
236,600
0.51%
0.04%
An existing Shareholder and 
a Cornerstone Investor

<<<PAGE 8>>>
8
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering 
(assuming 
the Over- 
allotment 
Option is not 
exercised)
Relationship
WT Asset Management
181,000
0.39%
0.03%
A Cornerstone Investor
Value Partners
118,000
0.25%
0.02%
An existing Shareholder and 
a Cornerstone Investor
Shenzhen Capital 
Value Partners Greater 
Bay Area Opportunity 
Limited Partnership Fund 
Note 6
1,000
0.00%
0.00%
A close associate of an 
existing Shareholder and 
a close associate of a 
Cornerstone Investor
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations to connected clientsNote 7
CICC Financial Trading 
Limited (“CICC FT”)
552,000
1.18%
0.09%
Connected client
JP Morgan Asset
Management (Asia 
Pacific) Limited (“JPM 
AM”)
1,183,000
2.54%
0.20%
Connected client

<<<PAGE 9>>>
9
Notes:
1. 
Among the Cornerstone Investors, Schroders, FT Sealand, Taikang Life and Value Partners are either Existing Minority 
Shareholders of the Company or their close associates. The Stock Exchange has granted a waiver from strict compliance 
with the requirements under Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the Placing Guidelines 
to permit H Shares in the International Offering to be placed to certain Existing Minority Shareholders and/or their close 
associates. Please refer to the section headed “Waivers and Exemptions – Allocation of H Shares to Existing Minority 
Shareholders and Their Close Associates” of the Prospectus for details.
2. 
This number of Offer Shares allocated represents the Offer Shares allocated to Schroders in its capacity as both a 
cornerstone investor and a placee.
3. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the number of 
Offer Shares allocated to the investors as placees in the International Offering. For allocations of Offer Shares to the 
relevant investors as Cornerstone Investors, please refer to the section headed “Allotment Results Details – International 
Offer – Cornerstone Investors” in this announcement. For details of the consent under Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations of further Shares to the existing Shareholders and/or their close associates and 
Cornerstone Investors, please refer to the section headed “Others/Additional Information – Allocations of Offer Shares 
to existing Shareholders and Cornerstone Investors and/or their close associates with a consent under Chapter 4.15 of the 
Guide for New Listing Applicants” in this announcement.
4. 
For the purpose of subscription of Offer Shares under the placing tranche, Huatai Capital Investment Limited and Huatai 
Securities Company Limited will enter into a series of cross border delta-one OTC swap transactions with each other, and 
with Shanghai Greenwoods acting in its capacity as investment manager for and on behalf of its underlying funds.
5. 
FT Sealand is held as to 51% and 49% by Sealand Securities Co., Ltd. (國海證券股份有限公司) and Templeton 
International Inc., respectively. Each of Templeton International Inc. and Franklin Templeton Investments (Asia) Limited 
is a wholly-owned subsidiary of Franklin Resources, Inc.
6. 
Jane Street Financial Limited and Jane Street are close associates.
7. 
Each of Value Partners Hong Kong Limited (“VPHKL”) and Value Partners Limited (“VPL”) (together with other 
subsidiaries under Value Partners Group Limited), acts as investment manager or investment advisor to certain investment 
funds. Each of VPHKL and VPL is wholly owned by Value Partners Group Limited, a company listed on the Stock 
Exchange (stock code: 0806). Shenzhen Capital Value Partners Greater Bay Area Opportunity Limited Partnership Fund 
is held by VPL by more than 30%.
8. 
For details of the consent under paragraph 1C of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients, please refer to the section headed “Others/Additional 
Information – Placing to connected clients with prior consents under paragraph 1C(1) of the Placing Guidelines” in this 
announcement.

<<<PAGE 10>>>
10
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
Shares held 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
Approximate 
% of total 
issued  
H Shares 
after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings
 upon Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Last day 
subject to 
the lock-up 
undertakings
Yang Meng Note 3
233,433,108
–
40.04%
January 1, 2027 (First 
Six-month Period) Note 1
July 1, 2027 (Second  
Six-month Period) Note 2
He Li
19,535,100
–
3.35%
January 1, 2027 (First 
Six-month Period) Note 1
July 1, 2027 (Second  
Six-month Period) Note 2
Notes:
1. 
The Controlling Shareholders may dispose of or transfer Shares after the indicated date provided that each 
Controlling Shareholder will not cease to be a Controlling Shareholder.
2. 
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after the 
indicated date.
3. 
The total number of Shares, being 233,433,108, comprises 232,666,200 Shares held by Yang Meng (“Mr. 
Yang”) as beneficial owner and 766,908 Shares held by Mr. Yang by virtue of his interest in controlled 
corporations. Mr. Yang is a limited partner of each of Changsha Yuanxiu Enterprise Management Consulting 
Partnership (L.P.) (長沙遠修企業管理諮詢合夥企業(有限合夥)) (“Yuanxiu Consulting”) and Changsha 
Yuanqing Enterprise Management Consulting Partnership (L.P.) (長沙遠清企業管理諮詢合夥企業(有限合
夥)) (“Yuanqing Consulting”), holding 84.06% and 99.99% partnership interests therein respectively. As 
such, Mr. Yang is deemed to be interested in the 649,896 and 117,012 Shares held by Yuanxiu Consulting 
and Yuanqing Consulting respectively by virtue of the SFO. Nevertheless, the general partner of Yuanxiu 
Consulting and Yuanqing Consulting exercises sole discretion and control over the voting rights in Yuanxiu 
Consulting and Yuanqing Consulting respectively, and Mr. Yang as a limited partner does not take part in the 
management or control of Yuanxiu Consulting and Yuanqing Consulting.

<<<PAGE 11>>>
11
Cornerstone Investors
Name
Number of 
Shares held 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
Approximate 
% of total 
issued 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)Note 1
Approximate 
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing 
(assuming 
the Over-
allotment 
Option is not
 exercised)
Last day 
subject to 
the lock-up 
undertakings
Schroders
5,522,200
11.84%
0.95%
January 1, 2027
Aspex
3,944,400
8.46%
0.68%
January 1, 2027
PAMAL
3,155,500
6.77%
0.54%
January 1, 2027
HK Greenwoods
1,186,800
2.54%
0.20%
January 1, 2027
GTINV and Shanghai 
Greenwoods
785,400
1.68%
0.13%
January 1, 2027
HACF, L.P.
1,577,700
3.38%
0.27%
January 1, 2027
UBS AM Singapore
1,577,700
3.38%
0.27%
January 1, 2027
FT Sealand
1,183,300
2.54%
0.20%
January 1, 2027
Jane Street
1,183,300
2.54%
0.20%
January 1, 2027
Taikang Life
1,183,300
2.54%
0.20%
January 1, 2027
WT Asset Management
1,183,300
2.54%
0.20%
January 1, 2027
Value Partners
788,800
1.69%
0.14%
January 1, 2027
Notes:
1. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on January 1, 2027. 
The Cornerstone Investors will cease to be prohibited from disposing of or transferring Shares subscribed for 
pursuant to the relevant cornerstone investment agreements after the indicated date.

<<<PAGE 12>>>
12
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
of the Over-
allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised 
and new 
Shares are 
issued)
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
Option 
is fully 
exercised 
and new 
Shares are 
issued)
Number 
of H Shares 
held upon 
Listing
% of total 
issued 
share 
capital 
upon 
Listing 
(assuming 
no exercise 
of the 
Over-
allotment 
Option)
% of total 
issued 
share 
capital 
upon 
Listing 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised 
and new 
Shares 
are issued)
Top 1
8,835,200
21.05%
18.04%
18.95%
16.48%
8,835,200
1.52%
1.50%
Top 5
24,402,300
58.14%
49.84%
52.33%
45.50%
24,402,300
4.19%
4.14%
Top 10
32,864,000
78.30%
67.12%
70.47%
61.28%
32,864,000
5.64%
5.57%
Top 25
45,347,300
108.05%
92.61%
97.24%
84.56%
45,347,300
7.78%
7.69%
Note
* 
Ranking of placees is based on the number of Title Shares allotted to the placees.
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
exercise of the 
Overallotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised 
and new 
H Shares are 
issued)
Allotment 
as % of 
total Offer 
Shares
 (assuming no 
exercise of the 
Overallotment 
Option)
Allotment 
as % of 
total Offer 
Shares 
(assuming the 
Overallotment 
Option 
is fully 
exercised and 
new H Shares 
are issued)
Number 
of H Shares 
held upon 
Listing
% of total 
issued 
share 
capital 
upon 
Listing 
(assuming 
no exercise 
of the 
Overallotment 
Option)
% of total 
issued 
share 
Capital 
upon 
Listing 
(assuming 
the 
Overallotment 
Option 
is fully 
exercised 
and new 
H Shares 
are issued)
Top 1
8,835,200
21.05%
18.04%
18.95%
16.48%
8,835,200
1.52%
1.50%
Top 5
24,402,300
58.14%
49.84%
52.33%
45.50%
24,402,300
4.19%
4.14%
Top 10
32,864,000
78.30%
67.12%
70.47%
61.28%
32,864,000
5.64%
5.57%
Top 25
45,347,300
108.05%
92.61%
97.24%
84.56%
45,347,300
7.78%
7.69%
Note
* 
Ranking of H Shareholders is based on the number of H Shares held by the Shareholders upon Listing.

<<<PAGE 13>>>
13
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number 
of H Shares 
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
Option is fully 
exercised and 
new Shares 
are issued)
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
Option 
is fully 
exercised 
and new 
Shares are 
issued)
Number 
of Shares 
held upon 
Listing
% of total 
issued share 
capital 
upon 
Listing 
(assuming 
no exercise 
of the 
Over-
allotment 
Option)
% of total 
issued share 
capital 
upon 
Listing 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised 
and new 
Shares are 
issued)
Top 1
–
0.00%
0.00%
0.00%
0.00%
252,968,208
43.40%
42.88%
Top 5
–
0.00%
0.00%
0.00%
0.00%
404,702,882
69.43%
68.60%
Top 10
15,500,600
36.93%
31.66%
33.24%
28.90%
441,718,672
75.78%
74.88%
Top 25
28,763,300
68.53%
58.74%
61.68%
53.64%
487,285,074
83.60%
82.60%
Note
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
NO. OF 
SHARES
APPLIED FOR
NO. OF 
VALID
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT
APPROXIMATE
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
POOL A
100
16,474
4,942 out of 16,474 to receive 100 Shares
30.00%
200
3,319
1,460 out of 3,319 to receive 100 Shares
21.99%
300
1,584
760 out of 1,584 to receive 100 Shares
15.99%
400
2,359
1,227 out of 2,359 to receive 100 Shares
13.00%
500
1,355
745 out of 1,355 to receive 100 Shares
11.00%
600
551
314 out of 551 to receive 100 Shares
9.50%

<<<PAGE 14>>>
14
NO. OF 
SHARES
APPLIED FOR
NO. OF 
VALID
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT
APPROXIMATE
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
700
394
229 out of 394 to receive 100 Shares
8.30%
800
479
291 out of 479 to receive 100 Shares
7.59%
900
648
420 out of 648 to receive 100 Shares
7.20%
1,000
2,383
1,573 out of 2,383 to receive 100 Shares
6.60%
1,500
819
639 out of 819 to receive 100 Shares
5.20%
2,000
821
706 out of 821 to receive 100 Shares
4.30%
2,500
389
350 out of 389 to receive 100 Shares
3.60%
3,000
411
384 out of 411 to receive 100 Shares
3.11%
3,500
244
231 out of 244 to receive 100 Shares
2.70%
4,000
253
243 out of 253 to receive 100 Shares
2.40%
4,500
196
194 out of 196 to receive 100 Shares
2.20%
5,000
477
100 Shares
2.00%
6,000
273
100 Shares plus 22 out of 273 to receive additional 100 Shares
1.80%
7,000
214
100 Shares plus 41 out of 214 to receive additional 100 Shares
1.70%
8,000
184
100 Shares plus 59 out of 184 to receive additional 100 Shares
1.65%
9,000
168
100 Shares plus 74 out of 168 to receive additional 100 Shares
1.60%
10,000
907
100 Shares plus 499 out of 907 to receive additional 100 Shares
1.55%
20,000
433
300 Shares
1.50%
30,000
242
400 Shares
1.33%
40,000
158
500 Shares
1.25%
50,000
439
600 Shares
1.20%
36,174
Total number of Pool A successful applicants: 18,203

<<<PAGE 15>>>
15
NO. OF 
SHARES
APPLIED FOR
NO. OF 
VALID
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT
APPROXIMATE
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
POOL B
100,000
169
4,800 Shares plus 165 out of 169 to receive additional 100 Shares
4.90%
200,000
37
9,700 Shares
4.85%
300,000
14
14,400 Shares
4.80%
400,000
15
18,800 Shares
4.70%
500,000
2
23,000 Shares
4.60%
600,000
1
27,000 Shares
4.50%
700,000
4
30,800 Shares
4.40%
800,000
1
34,400 Shares
4.30%
900,000
1
37,800 Shares
4.20%
1,000,000
3
41,000 Shares
4.10%
2,331,600
3
90,000 Shares
3.86%
250
Total number of Pool B successful applicants: 250
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and Stock Exchange trading fee payable.

<<<PAGE 16>>>
16
OTHERS/ADDITIONAL INFORMATION
Offer Size Adjustment Option
The Offer Size Adjustment Option was not exercised and has lapsed.
Allocation of H Shares to Existing Minority Shareholders and their close associates
The Company has applied for, and the Stock Exchange has granted, a waiver from strict compliance 
with the requirements under Rule 10.04 of and consent under paragraph 1C(2) of Appendix F1 to 
the Listing Rules to permit H Shares in the International Offering to be placed to certain existing 
minority Shareholders who (i) hold less than 5% of the voting rights in the Company prior to the 
completion of the Global Offering and (ii) are not and will not become (upon the completion of the 
Global Offering) core connected persons of the Company or the close associates of any such core 
connected person (together, the “Existing Minority Shareholders”) and/or their close associates, 
subject to the conditions as follows:
(a) 
each Existing Minority Shareholder to whom the Company may allocate the H Shares in the 
International Offering holds less than 5% of the voting rights in the Company before Listing;
(b) 
each Existing Minority Shareholder is not, and will not be, a core connected person of the 
Company or any close associate of any such core connected person immediately prior to or 
following the Global Offering;
(c) 
none of the Existing Minority Shareholders has the right to appoint a Director and/or have 
any other special rights;
(d) 
allocation to the Existing Minority Shareholders or its close associates will not affect the 
ability of the Company to satisfy the public float requirement as prescribed by the Stock 
Exchange under Rule 8.08 (as amended and replaced by Rule 19A.13A) of the Listing Rules 
or otherwise approved by the Stock Exchange; and
(e) 
none of the Existing Minority Shareholders or its close associates receives any preferential 
treatment, or is in a position to exert influence on the Company to obtain actual or perceived 
preferential treatment in the allocation either as a placee by virtue of its relationship with the 
Company;
Please refer to the section headed “Waivers and Exemption – Allocation of H Shares to Existing 
Minority Shareholders and their Close Associates” in the Prospectus for further details of the 
waiver and consent. Given that (i) there is no requirement to disclose interests under PRC laws 
unless such person is an owner of more than 5% of the issued share capital of the Company, the 
Directors or senior management of the Company or top ten Shareholders, and (ii) The Hong Kong 
Securities Clearing Company Limited, as trustee, holds A Shares on behalf of investors in Hong 
Kong and overseas pursuant to the rules and limits of Shenzhen-Hong Kong Stock Connect and 
the Company is unable to identify Shareholders who hold A Shares through the Shenzhen-Hong 
Kong Stock Connect, allocation to the Existing Minority Shareholders and/or their close associates 
will not be disclosed in this announcement (other than to the extent that such Existing Minority 
Shareholders or close associates subscribe for H Shares as Cornerstone Investors or that such 
Existing Minority Shareholders shall hold more than 1% of the issued share capital of the Company 
immediately prior to the completion of the Global Offering).

<<<PAGE 17>>>
17
All allocations of Offer Shares to the Existing Minority Shareholders are in compliance with all 
the conditions under the waiver and consent granted by the Stock Exchange.
Allocations of Offer Shares to existing Shareholders and Cornerstone Investors and/or their 
close associates with a consent under Chapter 4.15 of the Guide for New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 
of the Guide for New Listing Applicants to permit the Company to allocate further Offer Shares 
in the International Offering to existing Shareholders and Cornerstone Investors and/or their close 
associates as placees, subject to the following conditions:
(a) 
the final offering size of the Global Offering (excluding any additional Shares which may 
be issued upon exercise of the Over-allotment Option) will be of a total value of at least 
HK$1 billion as required by paragraph 18(i) of Chapter 4.15 of the Guide for New Listing 
Applicants;
(b) 
the Offer Shares allocated to all existing shareholders and their close associates (whether as 
cornerstone investors and/or as placees) as permitted under this exemption do not exceed 30% 
of the total number of the H Shares offered, which is in compliance with paragraph 18(ii) of 
Chapter 4.15 of the Guide for New Listing Applicants;
(c) 
each Director and chief executive of the Company has confirmed that no securities have 
been allocated to them or their respective close associates under the Size-based Exemption as 
required by paragraph 18(iii) of Chapter 4.15 of the Guide for New Listing Applicants;
(d) 
the Company will comply with the public float requirement under Rule 8.08(1) and Rule 
19A.13A(2) of the Listing Rules; and
(e) 
details of the allocation to existing investors will be disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates 
and Cornerstone Investors, please refer to the section headed “Allotment Results Details – 
International Offering – Allottees with Waivers/Consents Obtained” in this announcement.

<<<PAGE 18>>>
18
Placing to connected clients with prior consents under paragraph 1C of the Placing 
Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, consents 
under paragraph 1C of the Placing Guidelines to permit allocation to connected clients pursuant to 
the Placing Guidelines. The allocation of Offer Shares to such connected clients is in compliance 
with all the conditions under the consents granted by the Stock Exchange. Details of the placement to 
connected clients (including the cornerstone tranche and placing tranche) are set out below.
No.
Connected Distributor
Connected 
Client
Relationship
Whether the 
Connected 
Client will hold 
the beneficial 
interests of the 
Offer Shares on 
a non-
discretionary 
basis or 
discretionary 
basis for 
independent 
third parties
Number of 
Offer 
Shares 
to be 
allocated to 
the 
connected 
client
Approximate 
% of Offer 
Shares 
allocated 
to the 
connected 
client 
(assuming no 
exercise of 
the Over-
allotment 
Option)
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering 
(assuming no 
exercise of 
the Over-
allotment 
Option)
1.
China International Capital 
Corporation Hong Kong 
Securities Limited (“CICCHKS”)
CICC FT Note 1
CICC FT is a member 
of the same group as 
CICCHKS.
Non-discretionary 
basis
552,000
1.18%
0.09%
2.
J.P. Morgan Securities (Asia 
Pacific) Limited (“JPM 
APAC”) and JPMorgan Chase 
Bank, N.A. (“JPM Chase”)
JPM AM Note 2
JPM APAC, JPM 
Chase and JPM AM 
are members of the 
same group.
Discretionary basis
1,183,000
2.54%
0.20%
Notes:
1. 
CICC FT and China International Capital Corporation Limited (“CICCL”) will enter into a cross border OTC 
swap transaction (the “Hongxin OTC Swap”) with Foshan Hongxin Private Fund Management Co., Ltd. (佛山
弘信私募基金管理有限公司) (“Foshan Hongxin”) as the fund manager acting on behalf of Hongxin Dongsheng 
No. 1 Private Securities Investment Fund (弘信東昇一號私募證券投資基金) (the “CICC FT Ultimate Client 
(Hongxin)”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the 
Hongxin OTC Swap while the economic risks and returns of the underlying Offer Shares are passed to the CICC 
FT Ultimate Client (Hongxin), subject to customary fees and commissions. The Hongxin OTC Swap will be fully 
funded by the CICC FT Ultimate Client (Hongxin). During the term of the Hongxin OTC Swap, all economic 
returns of the Offer Shares subscribed by CICC FT will be passed to the CICC FT Ultimate Client (Hongxin) and 
all economic loss shall be borne by the CICC FT Ultimate Client (Hongxin) through the Hongxin OTC Swap, and 
CICC FT will not take part in any economic return or bear any economic loss in relation to the Offer Shares. No 
investor in Hongxin Dongsheng No. 1 Private Securities Investment Fund holds 30% or more interest therein. Liu 
Guanglu (劉廣錄) is the ultimate beneficial owner holding 30% or more interest in Foshan Hongxin.
To the best of CICC FT’s knowledge having made all reasonable inquiries, the CICC FT Ultimate Client 
(Hongxin) is an independent third party of CICC FT, CICCHKS and the companies which are members of the 
same group of CICCHKS.
2. 
JPM AM will hold the Offer Shares in its capacity as the discretionary fund manager managing assets on behalf of 
its underlying clients. Each of the underlying clients of JPM AM is an independent third party of JPM AM, JPM 
APAC, JPM Chase and the companies which are members of the same group of JPM APAC and JPM Chase.

<<<PAGE 19>>>
19
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or 
any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and the 
District of Columbia). This announcement does not, and is not intended to, constitute or form 
a part of any offer or solicitation to purchase or subscribe for securities in the United States 
or in any other jurisdiction. The Offer Shares have not been and will not be registered under 
the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities 
Act”) or securities law of any state or other jurisdiction of the United States and may not be 
offered, sold, pledged or otherwise transferred within the United States, except in transactions 
exempt from, or not subject to, the registration requirements of the U.S. Securities Act and in 
compliance with any applicable state securities laws.
The Offer Shares are being offered and sold (i) within the United States solely to “Qualified 
Institutional Buyers” as defined in Rule 144A pursuant to an exemption from registration under 
the U.S. Securities Act and (ii) outside the United States in offshore transactions in accordance 
with Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated June 23, 2026 issued by by Anker Innovations 
Technology Co., Ltd. (安克創新科技股份有限公司) for detailed information about the Global 
Offering described below before deciding whether or not to invest in the H Shares thereby being 
offered.
* Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements – Hong Kong Public Offering – Hong Kong Underwriting 
Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong 
Kong time) on the Listing Date (which is currently expected to be on Thursday, July 2, 2026).

<<<PAGE 20>>>
20
PUBLIC FLOAT
Immediately following the completion of the Global Offering (before any exercise of the Over-
allotment Option assuming no new Shares are issued under the Restricted Share Incentive Plans, 
and excluding any A Shares issuable upon conversion of the outstanding 2025 Convertible Bonds), 
the total number of the H Shares expected to be held by the public represents approximately 8.00% 
of the total issued share capital of the Company, which is higher than the prescribed percentage of 
H Shares required to be held in public hands of 5.18% under Rule 19A.13A(2)(b) of the Listing 
Rules calculated based on the Offer Price of HK $99.32 per H Share, thereby satisfying Rule 
8.08(1) (as amended and replaced by Rule 19A.13A) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the H Shares of the Company at the time of Listing. Based on the 
Offer Price of HK$99.32 per Share, the Company satisfies the free float requirement under Rule 
8.08A (as amended and replaced by Rule 19A.13C) of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering (before 
any exercise of the Over-allotment Option), (i) no placee will, individually, be placed more than 
10% of the enlarged issued share capital of the Company immediately after the Global Offering; (ii) 
there will not be any new substantial Shareholder immediately after the Global Offering; (iii) the 
three largest public Shareholders do not hold more than 50% of the H Shares held in public hands 
at the time of the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) 
there will be at least 300 Shareholders at the time of the Listing in compliance with Rule 8.08(2) 
of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Thursday, July 
2, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting – Underwriting Arrangements – 
Hong Kong Public Offering – Grounds for Termination” in the Prospectus has not been exercised. 
Investors who trade the H Shares on the basis of publicly available allocation details prior to the 
receipt of Share certificates or prior to the H Share certificates becoming valid evidence of title do 
so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Thursday, July 
2, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange will 
commence at 9:00 a.m. on Thursday, July 2, 2026 (Hong Kong time). The Shares will be traded in 
board lots of 100 Shares each, and the stock code of the H Shares will be 00668.
By order of the Board
Anker Innovations Technology Co., Ltd.
Mr. Yang Meng
Chairman of the Board, Executive Director and Chief 
Executive Officer
Hong Kong, June 30, 2026
As at the date of this announcement, the Board comprises: (i) Mr. Yang Meng, Mr. Zhao 
Dongping, Mr. Zhu Fanghao and Mr. Xiong Kang as executive Directors; (ii) Mr. Zhang Shanfeng 
and Mr. Lian Meng as non-executive Directors; and (iii) Mr. Li Congliang, Ms. Yi Xuan and Mr. 
Han Xi as independent non-executive Directors.
