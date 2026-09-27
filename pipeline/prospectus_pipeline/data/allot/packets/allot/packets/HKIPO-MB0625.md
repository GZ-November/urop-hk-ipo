# 配发结果公告抽取任务：0625.HK SHEIN Global Holdings Limited - W

- 公告：Announcement of Final Offer Price and Allotment Results
- 刊发时间（港交所元数据）：**31/08/2026 21:49**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0831/2026083102409.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"0625.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
defined in the prospectus dated 24 August 2026 (the “Prospectus”) issued by SHEIN Global Holdings Limited (the 
“Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. Potential investors should read the Prospectus for detailed information about the Company 
and the Global Offering described below before deciding whether or not to invest in the Offer Shares.
This announcement is not for release, publication or distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities 
in the United States or in any other jurisdiction. The Offer Shares have not been and will not be registered under the 
United States Securities Act of 1933, as amended from time to time (the “U.S. Securities Act”) or securities law of 
any state or other jurisdiction of the United States and may not be offered, sold, pledged or transferred within the 
United States, except in transactions exempt from, or not subject to, the registration requirements of the U.S. Securities 
Act. There will be no public offer of the Offer Shares in the United States. The Offer Shares are being offered and 
sold (1) solely to qualified institutional buyers as defined in Rule 144A under the U.S. Securities Act pursuant to an 
exemption from registration under the U.S. Securities Act and (2) outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, Goldman Sachs (Asia) L.L.C., as the stabilizing manager (the “Stabilizing 
Manager”), or its affiliates or any person acting for it, on behalf of the Underwriters, may over-allocate or effect 
transactions with a view to stabilizing or supporting the market price of the Class B Shares at a level higher than 
that which might otherwise prevail for a limited period after the Listing Date. However, there is no obligation on 
the Stabilizing Manager, its affiliates or any person acting for it, to conduct any such stabilizing action, which, if 
commenced, will be conducted at the absolute discretion of the Stabilizing Manager, its affiliates or any person 
acting for it, and may be discontinued at any time. Any such stabilizing activity is required to be brought to an end 
on Saturday, 26 September 2026, being the 30th day after the last day for lodging applications under the Hong Kong 
Public Offering. Such stabilization action, if taken, may be effected in all jurisdictions where it is permissible to do 
so, in each case in compliance with all applicable laws, rules and regulatory requirements, including the Securities and 
Futures (Price Stabilizing) Rules (Cap. 571W of the Laws of Hong Kong), as amended, made under the Securities and 
Futures Ordinance (Cap. 571 of the Laws of Hong Kong).
Potential investors should be aware that stabilizing action cannot be taken to support the price of the Class B Shares 
for longer than the stabilization period which begins on the Listing Date and is expected to expire on Saturday, 26 
September 2026, being the 30th day after the last day for the lodging of applications under the Hong Kong Public 
Offering. After this date, no further stabilizing action may be taken, and demand for the Class B Shares and the price 
of the Class B Shares could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out in 
the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not 
resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-
overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate, 
by giving notice in writing to the Company, their obligations under the Hong Kong Underwriting Agreement with 
immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Hong Kong Underwriting Agreement — Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date.
The Company is controlled through weighted voting rights. Prospective investors should be aware of the potential risks 
of investing in a company with a WVR structure, in particular that the WVR Beneficiaries, whose interests may not 
necessarily be aligned with those of our Shareholders as a whole, will be in a position to exert significant influence 
over the outcome of Shareholders’ resolutions, irrespective of how other Shareholders vote. For further information 
about the risks associated with the WVR structure, see “Risk Factors — J. Risks Related to our Class B Shares and 
the Global Offering” in the Prospectus. Prospective investors should make the decision to invest in the Company only 
after due and careful consideration.

<<<PAGE 2>>>
2
SHEIN Global Holdings Limited
希音國際控股有限公司
(A company controlled through weighted voting rights and incorporated in the Cayman Islands with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
279,992,500 Class B Shares (subject to the 
 Over-allotment Option)
Number of Hong Kong Offer 
Shares
:
27,999,300 Class B Shares
Number of International Offer 
Shares
:
251,993,200 Class B Shares (subject to the 
 Over-allotment Option)
Final Offer Price
:
HK$48.56 per Offer Share plus 
 brokerage of 1%, SFC transaction 
 levy of 0.0027%, AFRC transaction 
 levy of 0.00015% and the 
 Stock Exchange trading fee of 0.00565%
Nominal Value
:
US$0.000002 per Share
Stock Code
:
00625
Joint Sponsors, Sponsor-Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers
Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
SHEIN Global Holdings Limited
希音國際控股有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated 24 August 2026 (the “Prospectus”) issued by 
SHEIN Global Holdings Limited (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the Class B Shares 
could move substantially even with a small number of the Class B Shares traded and should 
exercise extreme caution when dealing in the Class B Shares.
SUMMARY
Company information
Stock code
Stock code
00625
00625
Stock short name
Stock short name
SHEIN-W
SHEIN-W
Dealings commencement date
Dealings commencement date
1 September 2026
1 September 2026#
#see note at the end of the announcement
Price Information
Final Offer Price
HK$48.56
Maximum Offer Price
HK$49.50
Offer Shares and Share Capital
Number of Offer Shares (before exercise of 
the Over-allotment Option)
279,992,500
Final Number of Offer Shares in Hong Kong 
Public Offering
27,999,300
Final Number of Offer Shares in 
International Offering (before exercise of 
the Over-allotment Option)
251,993,200
Number of issued Shares upon Listing 
(before exercise of the Over-allotment 
Option)
4,246,202,609

<<<PAGE 4>>>
4
Over-allocation
No. of Offer Shares over-allocated
41,998,500
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through stock 
borrowing arrangement or a combination of these means. In the event the Over-allotment Option 
is exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$13,596.4 million
Less: Estimated listing expenses payable 
 based on the Final Offer Price
HK$(382.3) million
Net proceeds
HK$13,214.1 million
Note: Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
The Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if any) 
for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus on a pro rata 
basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
35,751
No. of successful applications
18,673
Subscription level
5.63 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong 
 Kong Public Offering
27,999,300
No. of Offer Shares reallocated from the International 
 Offering (reallocation)
0
Final no. of Offer Shares under the Hong Kong Public 
 Offering
27,999,300
% of Offer Shares under the Hong Kong Public Offering 
 to the Global Offering (before the exercise of the 
 Over-allotment Option)
10%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can refer to 
www.eipo.com.hk/eIPOAllotment to perform a search by identification number or www.eipo.com.hk/eIPOAllotment 
for the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
106
Subscription Level
2.59 times
No. of Offer Shares initially available 
 under the International Offering
251,993,200
Final no. of Offer Shares under the 
 International Offering
251,993,200
% of Offer Shares under the International 
 Offering to the Global Offering (before 
 the exercise of the Over-allotment Option)
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) 
a waiver from strict compliance with Rule 10.04 of the Listing Rules and/or a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the 
Stock Exchange to permit Offer Shares in the International Offering to be placed to certain existing 
Shareholders and/or their close associates; and (b) a consent under paragraph 18 of Chapter 4.15 
of the Guide for New Listing Applicants to permit the Company to, among other things, allocate 
further Offer Shares in the International Offering to existing Shareholders and/or Cornerstone 
Investors and/or their close associates, (i) none of the Offer Shares subscribed by the placees 
and the public have been financed directly or indirectly by the Company, any of the Directors, 
chief executive of the Company, the Controlling Shareholders, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates; and 
(ii) none of the placees and the public who have purchased the Offer Shares are accustomed to 
taking instructions from the Company, any of the Directors, chief executive of the Company, the 
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company or any 
of its subsidiaries or their respective close associates in relation to the acquisition, disposal, voting 
or other disposition of the Class B Shares registered in his/her/its name or otherwise held by him/
her/it.

<<<PAGE 6>>>
6
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of Offer 
Shares allocated
% of Offer 
Shares (assuming 
the Over-
allotment Option 
is not exercised)
% of total 
issued Class 
B Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 1 Note 2
% of total 
issued share 
capital after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 1 Note 2
Existing 
Shareholders 
or their close
 associates
Exclusive Depot 
 Limited (“Exclusive 
 Depot”)
24,239,000
8.7%
0.9%
0.6%
Yes
Internet Fund IIIA Pte.
  Ltd. (“Internet 
 Fund IIIA”)
8,564,400
3.1%
0.3%
0.2%
Yes
General Atlantic 
 Singapore EDL 
 Pte. Ltd. (“General 
 Atlantic”)
8,079,600
2.9%
0.3%
0.2%
Yes
Huang River 
 Investment Limited 
 (“Huang River”)
8,079,600
2.9%
0.3%
0.2%
Yes
Greenwoods Asset 
 Management Hong 
 Kong Limited (“HK 
 Greenwoods”)
4,847,800
1.7%
0.2%
0.1%
Yes
Taikang Life Insurance 
 Co., Ltd (泰康人壽
 保險有限責任公司) 
 (“Taikang Life”)
4,847,800
1.7%
0.2%
0.1%
No
UBS Asset 
 Management 
 (Singapore) 
 Ltd. (“UBS AM 
 Singapore”)
3,231,800
1.2%
0.1%
0.1%
No
Total
61,890,000
22.1%
2.2%
1.5%

<<<PAGE 7>>>
7
Notes:
(1) 
In addition to the Offer Shares subscribed for as Cornerstone Investors, Exclusive Depot, General Atlantic, 
Huang River, Taikang Asset Management (Hong Kong) Company Limited, a close associate of Taikang Life, 
UBS AM Singapore and Boyu Capital Investment Management Co., Limited, a close associate of Boyu Entities, 
were allocated further Offer Shares as placees in the International Offering. Please refer to the section headed 
“Allotment Results Details — International Offering — Allottees with Waivers/Consents Obtained” in this 
announcement for details.
For Taikang Life and UBS AM Singapore, only the Offer Shares subscribed for as Cornerstone Investors are 
subject to lock-up as indicated below.
For Exclusive Depot, General Atlantic, Huang River and Boyu Capital Investment Management Co., Limited, 
the Offer Shares subscribed for as Cornerstone Investors and certain Offer Shares subscribed for as placees 
are subject to lock-up as indicated below.
For details, please refer to the sections headed “Lock-up Undertakings — Cornerstone Investors” and “Lock-
up Undertakings — Additional Lock-up Provided by Certain Placees who are Existing Shareholders or Their 
Close Associates” in this announcement.
(2) 
Only taking into account the Offer Shares allocated to the relevant investors as Cornerstone Investors under 
the Global Offering.
Allottees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares allocated
% of Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
Class B Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 1
Relationship
Allottees with consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further Offer 
Shares to existing Shareholders and Cornerstone Investors and/or their close associates Note 3
Placees Note 2
Boyu Entities
Exclusive Depot Limited
4,935,000 
1.8%
0.2%
0.1%
A Cornerstone 
Investor and 
an existing 
Shareholder
Boyu Capital Investment 
 Management Co., Limited
4,792,900 
1.7%
0.2%
0.1%
A close associate 
of Boyu Entities
Subtotal
9,727,900 
3.5%
0.3%
0.2%
/
IDG Entities
IDG China Capital Fund 
 III L.P.
769,000 
0.3%
0.03%
0.02%
An existing 
Shareholder
IDG China Capital III 
 Investors L.P.
38,000 
0.01%
0.001%
0.001%
An existing 
Shareholder

<<<PAGE 8>>>
8
Investor
No. of Offer 
Shares allocated
% of Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
Class B Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 1
Relationship
Subtotal
807,000
0.3%
0.03%
0.02%
/
Huang River
26,072,500
9.3%
0.9%
0.6%
A Cornerstone 
Investor and a 
close associate 
of Aonline 
Investment 
Limited (“Aonline 
Investment”), 
an existing 
Shareholder
General Atlantic
6,507,400
2.3%
0.2%
0.2%
A Cornerstone 
Investor and 
an existing 
Shareholder
Taikang Asset
 Management
 (Hong Kong)
 Company Limited
1,300,000
0.5%
0.05%
0.03% A close associate of
Taikang Life, 
a Cornerstone 
Investor
UBS AM Singapore
3,230,000
1.2%
0.1%
0.1%
A Cornerstone 
Investor
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the 
Placing Guidelines in relation to subscription for Offer Shares by existing Shareholders and/or their close associates Note 4
Cornerstone Investor
Exclusive Depot
24,239,000
8.7%
0.9%
0.6%
An existing 
Shareholder
Internet Fund IIIA
8,564,400
3.1%
0.3%
0.2%
A close associate 
of Internet Fund 
IV Pte. Ltd., 
an existing 
Shareholder
General Atlantic
8,079,600
2.9%
0.3%
0.2%
An existing 
Shareholder

<<<PAGE 9>>>
9
Investor
No. of Offer 
Shares allocated
% of Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
Class B Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 1
Relationship
Huang River
8,079,600
2.9%
0.3%
0.2%
A close associate 
of Aonline 
Investment, 
an existing 
Shareholder
HK Greenwoods
4,847,800
1.7%
0.2%
0.1%
A close associate 
of Greenwoods 
Entities, existing 
Shareholders of the 
Company
Placee Note 2
Hongshan Entities and HCEP
HongShan Capital 
 Advisors Limited
19,741,800
7.1%
0.7%
0.5%
A close associate 
of Hongshan 
Entities and HCEP, 
existing 
Shareholders 
of the Company
Ocean Prosperity 
 Holdings Limited
3,750,900 
1.3%
0.1%
0.1%
An existing 
Shareholder
HSG Growth VI Holdco E, 
 Ltd.
2,083,800 
0.7%
0.1%
0.05%
An existing 
Shareholder
HCEP Management Limited
1,041,900 
0.4%
0.04%
0.02%
A close associate 
of Hongshan 
Entities and 
HCEP, existing 
Shareholders of 
the Company
Subtotal
26,618,400 
9.5%
0.9%
0.6%
/
Willett Entities
Willett Advisors LLC
833,500
0.3%
0.03%
0.02%
A close associate 
of Willett Entities, 
existing 
Shareholders 
of the Company
Paragon
 Holdings I LLC
20,800
0.01%
0.001%
0.0005%
An existing 
Shareholder
Subtotal
854,300 
0.3%
0.03%
0.02%
/

<<<PAGE 10>>>
10
Investor
No. of Offer 
Shares allocated
% of Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
Class B Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 1
Relationship
Brookfield Entities
Runway Bermuda Holdco 1 
 Ltd.
4,167,700
1.5%
0.1%
0.1%
An existing 
Shareholder
Runway Bermuda Holdco 2 
 Ltd.
4,167,700
1.5%
0.1%
0.1%
An existing 
Shareholder
Subtotal
8,335,400 
3.0%
0.3%
0.2%
/
Alliance Lordon Limited
Enreal China Master Fund
2,383,100
0.9%
0.1%
0.1%
A close associate 
of Alliance 
Lordon Limited, 
an existing 
Shareholder
Forreal China Value Fund
1,784,600 
0.6%
0.1%
0.04%
A close associate 
of Alliance 
Lordon Limited, 
an existing 
Shareholder
Subtotal
4,167,700
1.5%
0.1%
0.1%
/
DST Asia IX
8,769,200 
3.1%
0.3%
0.2%
An existing 
Shareholder
Coppel Capital, 
 S.A. de C.V.
416,700 
0.1%
0.01%
0.01%
An existing 
Shareholder
D1 Capital Partners L.P.
6,251,600
2.2%
0.2%
0.1%
A close associate 
of D1 Master 
Holdco I LLC, 
an existing 
Shareholder
Reliance Retail Ventures 
 Limited
4,167,700
1.5%
0.1%
0.1%
An existing 
Shareholder
Preventive Healthcare LLC
2,083,800 
0.7%
0.1%
0.05%
An existing 
Shareholder

<<<PAGE 11>>>
11
Investor
No. of Offer 
Shares allocated
% of Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
Class B Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 1
Relationship
MIC Capital Management 
 81 RSC Ltd
6,251,600 
2.2%
0.2%
0.1%
An existing 
Shareholder
Sanabil Private Equity 
 Investments Company
4,384,600 
1.6%
0.2%
0.1%
An existing 
Shareholder
Xavier Bruno Herve Niel
41,600 
0.01%
0.001%
0.001%
A close associate 
of DAXN, Inc., 
an existing 
Shareholder
Claure Group LLC
5,001,300 
1.8%
0.2%
0.1%
An existing 
Shareholder
Mohawk River Holdings, 
 LLC
4,167,700 
1.5%
0.1%
0.1%
An existing 
Shareholder
Microsoft Corporation
1,041,900
0.4%
0.04%
0.02% A close associate of 
Microsoft Capital 
Group, LLC, 
an existing 
Shareholder
True Creative Limited
3,238,400 
1.2%
0.1%
0.1%
An existing 
Shareholder
Dragoneer Investment 
 Group, LLC
1,041,900 
0.4%
0.04%
0.02% A close associate of 
Shelf DF Holdings, 
LP, an existing 
Shareholder
SVF II APAC 
 AGGREGATOR (DE) 
 LLC
14,587,100 
5.2%
0.5%
0.3%
A close associate 
of Star Sphere 
Limited, 
an existing 
Shareholder
Coatue PE Asia 85 LLC
1,250,300 
0.4%
0.04%
0.03%
An existing 
Shareholder
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants 
in relation to allocations to connected clients Note 5
Cornerstone Investor
UBS AM Singapore
3,231,800
1.2%
0.1%
0.1%
A Cornerstone 
Investor and a 
connected client

<<<PAGE 12>>>
12
Investor
No. of Offer 
Shares allocated
% of Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
Class B Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 1
Relationship
PlaceeNote 2
UBS AM Singapore
3,230,000
1.2%
0.1%
0.1%
A Cornerstone 
Investor and a 
connected client
Fullgoal Asset Management 
 (HK) Limited 
 (“Fullgoal HK”)
898,000
0.3%
0.03%
0.02%
A connected 
client
Fullgoal Fund Management 
 Co., Ltd. 
 (“Fullgoal Fund”)
1,522,000
0.5%
0.1%
0.04%
A connected 
client
Notes:
1. 
Only taking into account the Offer Shares allocated to the relevant investors under the Global Offering.
2. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the bookbuilding placing tranche in the 
International Offering. For allocations of Offer Shares to the relevant investors as Cornerstone Investors, 
please refer to the section headed “Allotment Results Details — International Offering — Cornerstone 
Investors” in this announcement.
3. 
For details of the consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in 
relation to allocations of Offer Shares to certain existing Shareholders and Cornerstone Investors and/or their 
respective close associates, please refer to the section headed “Others/Additional Information — Allocations 
of Offer Shares to the existing Shareholders and/or Cornerstone Investors and/or their close associates with 
consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants” in this announcement.
4. 
For details of the waiver from strict compliance with Rule 10.04 of the Listing Rules and consent 
under paragraph 1C(2) of the Placing Guidelines in relation to subscription for Offer Shares by existing 
Shareholders and/or their close associates, please refer to the section headed “Waivers and Exemption — 
Waiver and Consent in Relation to the Subscription for Class B Shares By Existing Shareholders or their 
Close Associates as Cornerstone Investors” of the Prospectus, and the section headed “Others/Additional 
Information — Placing to existing Shareholders and/or their close associates with a waiver from the strict 
compliance with Rule 10.04 of the Listing Rules and a prior consent under paragraph 1C(2) of the Placing 
Guidelines” in this announcement.
5. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to 
connected clients, please refer to the section headed “Waivers and Exemption — Consent in Relation to the 
Proposed Subscription of Offer Shares by Certain Cornerstone Investor Who is Connected Client” of the 
Prospectus, and the section headed “Others/Additional Information — Placing to connected clients with a 
prior consent under paragraph 1C(1) of the Placing Guidelines” in this announcement.

<<<PAGE 13>>>
13
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name Note 1
Number of Shares held 
in the Company subject 
to lock-up undertakings 
upon Listing
Approximate
% of Shares held in
the Company
subject to lock-up
undertakings in 
total issued Shares 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject to
 the lock-up 
undertakings Note 2
Apex Sight 
 Holdings 
 Limited
798,973,148 Class A Shares
487,090,102 Class B Shares
30.3%
28 February 2027 
(First Six-Month 
Period)
31 August 2027 
(Second Six-Month 
Period)
Total
798,973,148 Class A Shares
487,090,102 Class B Shares
30.3%
Notes:
1. 
Mr. Yangtian Xu holds his interests in the Company through Apex Sight Holdings Limited. Mr. Yangtian Xu 
wholly owns Apex Sight Holdings Limited through XYT Holdings Limited and Top Plus Ventures Limited 
and is the sole director of Apex Sight Holdings Limited. All the Controlling Shareholders are subject to Rule 
10.07 undertaking under the Listing Rules.
2. 
In accordance with the relevant Listing Rules/guidance materials, the required lock-up for the first six-month 
period ends on 28 February 2027 (the “First Six-Month Period”) and for the second six-month period ends 
on 31 August 2027 (the “Second Six-Month Period”). The Controlling Shareholders may dispose of or 
transfer Shares after the First Six-Month Period subject to that the Controlling Shareholders will not cease to 
be a Controlling Shareholder. The Controlling Shareholders will cease to be prohibited from disposing of or 
transferring Shares after the Second Six-Month Period.

<<<PAGE 14>>>
14
Existing Shareholders
Name
Number of Shares held in the 
Company subject to lock-up 
undertakings upon Listing
Approximate
% of Class B
Shares subject to
lock-up
undertakings 
in total issued 
Class B Shares 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Approximate
% of Shares held
in the Company
subject to 
lock-up 
undertakings in 
total issued 
Shares after 
the Global 
Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day 
subject 
to the lock-up 
undertakings Note 1
Apex Sight 
 Holdings 
 Limited
798,973,148 Class A Shares
487,090,102 Class B Shares
17.2%
30.3%
31 August 
2028
Upright Victory 
 Holdings 
 Limited
205,579,906 Class A Shares
78,160,244 Class B Shares
2.8%
6.7%
31 August 
2028
Trendy Group 
 Holdings 
 Limited
393,169,450 Class B Shares
13.9%
9.3%
31 August 
2028
Floral Field 
 Holdings 
 Limited
205,579,906 Class A Shares
78,160,244 Class B Shares
2.8%
6.7%
31 August 
2028
Color Park 
 Holdings 
 Limited
205,579,906 Class A Shares
78,160,244 Class B Shares
2.8%
6.7%
31 August 
2028
All other existing 
 Shareholders as 
 of the date of 
 the Prospectus
1,435,756,959 Class B Shares
50.7%
33.8%
28 February 
2027
Note:
1. 
Each of the existing Shareholders as of the date of the Prospectus has entered into a deed of lock-up undertaking 
in favor of the Company, the Joint Sponsors and the Sponsor-overall Coordinators. Pursuant to such lock-
up undertakings, (i) each of Apex Sight Holdings Limited, Upright Victory Holdings Limited, Trendy Group 
Holdings Limited, Floral Field Holdings Limited and Color Park Holdings Limited has agreed to a lock-up in 
respect of the Shares they held immediately following completion of the Global Offering (except for Shares 
subscribed in the Global Offering, if any) during the period commencing the Listing Date and ending on 
(including) the date which is 24 months from the Listing Date, subject to customary exceptions; and (ii) each of 
the other existing Shareholders has agreed to a lock-up in respect of the Shares they held immediately following 
completion of the Global Offering (except for Shares subscribed in the Global Offering, if any) during the period 
commencing the Listing Date and ending on (including) the date which is six months from the Listing Date, 
subject to customary exceptions.

<<<PAGE 15>>>
15
Cornerstone Investors
Name
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings 
upon Listing
Approximate 
% of Class 
B Shares 
subject to 
lock-up 
undertakings 
in total 
issued Class 
B Shares 
upon Listing
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
% of Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
in total 
issued 
Shares after 
the Global 
Offering 
upon Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings Note 1
Exclusive Depot
24,239,000 
Class B Shares
0.9%
0.6%
28 February 2027
Internet Fund IIIA
8,564,400 
Class B Shares
0.3%
0.2%
28 February 2027
General Atlantic
8,079,600 
Class B Shares
0.3%
0.2%
28 February 2027
Huang River
8,079,600 
Class B Shares
0.3%
0.2%
28 February 2027
HK Greenwoods
4,847,800 
Class B Shares
0.2%
0.1%
28 February 2027
Taikang Life
4,847,800 
Class B Shares
0.2%
0.1%
28 February 2027
UBS AM Singapore
3,231,800 
Class B Shares
0.1%
0.1%
28 February 2027
Total
61,890,000 
Class B Shares
2.2%
1.5%
Notes:
1. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on 28 February 
2027. The Cornerstone Investors will cease to be prohibited from disposing of or transferring the Class B 
Shares subscribed for pursuant to the relevant cornerstone investment agreements after the indicated date.

<<<PAGE 16>>>
16
Additional Lock-up Provided by Certain Placees who are Existing Shareholders or Their 
Close Associates
Name
Number of Shares 
held in the 
Company subject 
to lock-up 
undertakings upon 
Listing
Approximate % 
of Class B Shares 
subject to lock-up 
undertakings in 
total issued 
Class B Shares 
upon Listing
(assuming the 
Over-allotment 
Option is not 
exercised)
Approximate % 
of Shares held 
in the Company 
subject to lock-up 
undertakings in 
total issued 
Shares after the 
Global Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings Note 1
Exclusive Depot 
Limited
4,935,000 
Class B Shares 
0.2%
0.1%
28 February 2027
Boyu Capital 
Investment 
Management Co., 
Limited
4,792,900 
Class B Shares
0.2%
0.1%
28 February 2027
Huang River
8,335,500 
Class B Shares
0.3%
0.2%
28 February 2027
General Atlantic
6,507,400 
Class B Shares
0.2%
0.2%
28 February 2027
HongShan Capital 
Advisors Limited
19,741,800 
Class B Shares
0.7%
0.5%
28 February 2027
Ocean Prosperity 
Holdings Limited
3,750,900 
Class B Shares
0.1%
0.1%
28 February 2027
HSG Growth VI 
Holdco E, Ltd.
2,083,800 
Class B Shares
0.1%
0.05%
28 February 2027
HCEP Management 
Limited
1,041,900 
Class B Shares
0.04%
0.02%
28 February 2027

<<<PAGE 17>>>
17
Name
Number of Shares 
held in the 
Company subject 
to lock-up 
undertakings upon 
Listing
Approximate % 
of Class B Shares 
subject to lock-up 
undertakings in 
total issued 
Class B Shares 
upon Listing
(assuming the 
Over-allotment 
Option is not 
exercised)
Approximate % 
of Shares held 
in the Company 
subject to lock-up 
undertakings in 
total issued 
Shares after the 
Global Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings Note 1
Willett Advisors LLC
833,500 
Class B Shares
0.03%
0.02%
28 February 2027
Paragon Holdings I 
LLC
20,800 
Class B Shares
0.001%
0.0005%
28 February 2027
Runway Bermuda 
Holdco 1 Ltd.
4,167,700 
Class B Shares
0.1%
0.1%
28 February 2027
Runway Bermuda 
Holdco 2 Ltd.
4,167,700 
Class B Shares
0.1%
0.1%
28 February 2027
Enreal China Master 
Fund
2,383,100 
Class B Shares
0.1%
0.1%
28 February 2027
Forreal China Value 
Fund
1,784,600 
Class B Shares
0.1%
0.04%
28 February 2027
DST Asia IX
4,167,700 
Class B Shares
0.1%
0.1%
28 February 2027
Coppel Capital, S.A. 
de C.V.
416,700 
Class B Shares
0.01%
0.01%
28 February 2027
D1 Capital Partners 
L.P.
6,251,600 
Class B Shares
0.2%
0.1%
28 February 2027
Reliance Retail 
Ventures Limited
4,167,700 
Class B Shares
0.1%
0.1%
28 February 2027
Preventive Healthcare 
LLC
2,083,800 
Class B Shares
0.1%
0.05%
28 February 2027
MIC Capital 
Management 81 RSC 
Ltd
6,251,600 
Class B Shares
0.2%
0.1%
28 February 2027

<<<PAGE 18>>>
18
Name
Number of Shares 
held in the 
Company subject 
to lock-up 
undertakings upon 
Listing
Approximate % 
of Class B Shares 
subject to lock-up 
undertakings in 
total issued 
Class B Shares 
upon Listing
(assuming the 
Over-allotment 
Option is not 
exercised)
Approximate % 
of Shares held 
in the Company 
subject to lock-up 
undertakings in 
total issued 
Shares after the 
Global Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings Note 1
Sanabil Private 
Equity Investments 
Company
2,083,900 
Class B Shares
0.1%
0.05%
28 February 2027
Xavier Bruno Herve 
Niel
41,600 
Class B Shares
0.001%
0.001%
28 February 2027
Claure Group LLC
5,001,300 
Class B Shares
0.2%
0.1%
28 February 2027
Mohawk River 
Holdings, LLC
4,167,700 
Class B Shares
0.1%
0.1%
28 February 2027
Microsoft Corporation
1,041,900 
Class B Shares
0.04%
0.02%
28 February 2027
True Creative Limited
3,238,400 
Class B Shares
0.1%
0.1%
28 February 2027
Dragoneer Investment 
Group, LLC
1,041,900 
Class B Shares
0.04%
0.02%
28 February 2027
SVF II APAC 
AGGREGATOR 
(DE) LLC
14,587,100 
Class B Shares
0.5%
0.3%
28 February 2027
Coatue PE Asia 85 
LLC
1,250,300 
Class B Shares
0.04%
0.03%
28 February 2027
Total
120,339,800 
Class B Shares 
4.3%
2.8%
Note:
1. 
Certain Placees which are existing Shareholders or their close associates have entered into lock-up 
undertakings in favor of the Company, the Joint Sponsors and the Sponsor-overall Coordinators. Pursuant 
to such lock-up undertakings, these certain existing Shareholders (or their close associates) have agreed to a 
lock-up in respect of the Shares they subscribed as placees in the Global Offering as specified above during 
the period commencing the Listing Date and ending on (including) the date which is six months from the 
Listing Date, subject to customary exceptions.

<<<PAGE 19>>>
19
PLACEE CONCENTRATION ANALYSIS
Placees*
Number 
of Class 
B Shares 
allotted
Allotment 
as % of the 
International 
Offering 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Allotment 
as % of the 
International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised 
and new 
Class B 
Shares are 
issued)
Allotment as 
% of total 
Offer Shares 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised and 
new Class B 
Shares are 
issued)
Number 
of Class B 
Shares held 
upon Listing
Number 
of Shares 
held upon 
Listing**
% of total 
issued Class 
B Shares 
upon Listing 
(assuming 
no exercise 
of the Over-
allotment 
Option)
% of total 
issued Class 
B Shares upon 
Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Class B 
Shares are 
issued)
% of total 
issued Shares 
upon Listing 
(assuming 
no exercise 
of the Over-
allotment 
Option)**
% of total 
issued Shares 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Class B 
Shares are 
issued)**
Top 1
34,152,100
13.6%
11.6%
12.2%
10.6%
48,477,993
48,477,993
1.7%
1.7%
1.1%
1.1%
Top 5
128,714,500
51.1%
43.8%
46.0%
40.0%
389,231,171
389,231,171
13.8%
13.6%
9.2%
9.1%
Top 10
176,720,500
70.1%
60.1%
63.1%
54.9%
605,931,914
605,931,914
21.4%
21.1%
14.3%
14.1%
Top 25
250,416,100
99.4%
85.2%
89.4%
77.8%
903,329,218
903,329,218
31.9%
31.4%
21.3%
21.1%
* 
Ranking of placees is based on the number of Offer Shares allotted to the placees.
** 
Total issued shares upon Listing include Class A Shares (i.e. Shares with weighted voting rights which will 
not be converted into Class B Shares upon Listing). For details on the weighted voting rights structure of the 
Company, please refer to the section headed “Share Capital” of the Prospectus.
Shareholders of Class B Shares Concentration Analysis
Class B 
Shareholders*
Number of 
Class B 
Shares allotted
Allotment 
as % of the 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment 
as % of the 
International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Class B 
Shares are 
issued)
Allotment as 
% of total 
Offer Shares 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Class B 
Shares are 
issued)
Number of 
Class B Shares 
held upon 
Listing
Number of 
Shares held 
upon Listing**
% of total 
issued Class 
B Shares 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total 
issued Class 
B Shares 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Class B 
Shares are 
issued)
% of total 
issued Shares 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)**
% of total 
issued Shares 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Class B 
Shares are 
issued)**
Top 1
–
–
–
–
–
487,090,102
1,286,063,250
17.2%
17.0%
30.3%
30.0%
Top 5
27,425,400
10.9%
9.3%
9.8%
8.5%
1,681,794,225
2,686,347,279
59.4%
58.5%
63.3%
62.6%
Top 10
74,804,500
29.7%
25.4%
26.7%
23.2%
2,232,889,771
3,648,602,637
78.9%
77.7%
85.9%
85.1%
Top 25
187,128,500
74.3%
63.7%
66.8%
58.1%
2,657,948,647
4,073,661,513
93.9%
92.5%
95.9%
95.0%
* 
Ranking of Shareholders of Class B Shares is based on the number of Class B Shares held by the Shareholders 
of Class B Shares upon Listing.
** 
Total issued shares upon Listing include Class A Shares (i.e. Shares with weighted voting rights which will 
not be converted into Class B Shares upon Listing). For details on the weighted voting rights structure of the 
Company, please refer to the section headed “Share Capital” of the Prospectus.

<<<PAGE 20>>>
20
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number 
of Class 
B Shares 
allotted
Allotment 
as % of the 
International 
Offering 
(assuming no 
exercise of 
the Over-
allotment 
Option)
Allotment 
as % of the 
International 
Offering 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised 
and new 
Class B 
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
Option 
is fully 
exercised 
and new 
Class 
B Shares 
are issued)
Number of 
Class B 
Shares held 
upon Listing
Number of 
Class A 
Shares held 
upon Listing
Number 
of Shares 
held upon 
Listing**
% of total 
issued Class 
B Shares 
upon Listing 
(assuming 
no exercise 
of the Over-
allotment 
Option)
% of total 
issued Class 
B Shares 
upon Listing 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised 
and new 
Class B 
Shares are 
issued)
% of total 
issued 
Shares upon 
Listing 
(assuming no 
exercise of 
the Over-
allotment 
Option)**
% of total 
issued 
Shares upon 
Listing 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised 
and new 
Class B 
Shares are 
issued)**
Top 1
–
–
–
–
–
487,090,102
798,973,148
1,286,063,250
17.2%
17.0%
30.3%
30.0%
Top 5
807,000
0.3%
0.3%
0.3%
0.3%
1,423,084,284
1,415,712,866
2,838,797,150
50.3%
49.5%
66.9%
66.2%
Top 10
74,804,500
29.7%
25.4%
26.7%
23.2%
2,232,889,771
1,415,712,866
3,648,602,637
78.9%
77.7%
85.9%
85.1%
Top 25
187,128,500
74.3%
63.7%
66.8%
58.1%
2,657,948,647
1,415,712,866
4,073,661,513
93.9%
92.5%
95.9%
95.0%
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon 
Listing.
** 
Total issued shares upon Listing include Class A Shares (i.e. Shares with weighted voting rights which will 
not be converted into Class B Shares upon Listing). For details on the weighted voting rights structure of the 
Company, please refer to the section headed “Share Capital” of the Prospectus.

<<<PAGE 21>>>
21
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 35,751 valid 
applications made by the public will be conditionally allocated on the basis set out below:
NO. OF 
SHARES
APPLIED 
FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
POOL A
100
15,312
2,820 out of 15,312 to receive 100 Shares
18.42%
200
5,341
1,967 out of 5,341 to receive 100 Shares
18.41%
300
1,628
899 out of 1,628 to receive 100 Shares
18.41%
400
1,333
981 out of 1,333 to receive 100 Shares
18.40%
500
1,637
1,506 out of 1,637 to receive 100 Shares
18.40%
600
561
100 Shares plus 58 out of 561 to receive additional 100 Shares
18.39%
700
277
100 Shares plus 79 out of 277 to receive additional 100 Shares
18.36%
800
344
100 Shares plus 161 out of 344 to receive additional 100 Shares
18.35%
900
246
100 Shares plus 160 out of 246 to receive additional 100 Shares
18.34%
1,000
3,401
100 Shares plus 2,836 out of 3,401 to receive additional 100 Shares
18.34%
2,000
1,576
300 Shares plus 1,052 out of 1,576 to receive additional 100 Shares
18.34%
3,000
611
500 Shares plus 306 out of 611 to receive additional 100 Shares
18.34%
4,000
367
700 Shares plus 123 out of 367 to receive additional 100 Shares
18.34%
5,000
387
900 Shares plus 65 out of 387 to receive additional 100 Shares
18.34%
6,000
204
1,100 Shares
18.33%
7,000
116
1,200 Shares plus 96 out of 116 to receive additional 100 Shares
18.33%
8,000
135
1,400 Shares plus 89 out of 135 to receive additional 100 Shares
18.32%
9,000
117
1,600 Shares plus 57 out of 117 to receive additional 100 Shares
18.32%
10,000
837
1,800 Shares plus 267 out of 837 to receive additional 100 Shares
18.32%
20,000
400
3,600 Shares plus 256 out of 400 to receive additional 100 Shares
18.32%
30,000
160
5,400 Shares plus 153 out of 160 to receive additional 100 Shares
18.32%
40,000
121
7,300 Shares plus 33 out of 121 to receive additional 100 Shares
18.32%
50,000
281
9,100 Shares plus 168 out of 281 to receive additional 100 Shares
18.32%
100,000
149
18,300 Shares plus 26 out of 149 to receive additional 100 Shares
18.32%
35,541
Total number of Pool A successful applicants: 18,463

<<<PAGE 22>>>
22
NO. OF 
SHARES
APPLIED 
FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
POOL B
150,000
92
25,800 Shares plus 28 out of 92 to receive additional 100 Shares
17.22%
200,000
35
34,400 Shares plus 14 out of 35 to receive additional 100 Shares
17.22%
250,000
47
43,000 Shares plus 23 out of 47 to receive additional 100 Shares
17.22%
500,000
15
86,100 Shares
17.22%
750,000
5
129,100 Shares plus 2 out of 5 to receive additional 100 Shares
17.22%
1,000,000
9
172,200 Shares
17.22%
1,500,000
1
258,300 Shares
17.22%
1,750,000
1
301,300 Shares
17.22%
2,250,000
1
387,400 Shares
17.22%
3,000,000
3
516,600 Shares
17.22%
13,999,600
1
2,410,700 Shares
17.22%
210
Total number of Pool B successful applicants: 210
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Class B Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them is the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and Stock Exchange trading fee payable.

<<<PAGE 23>>>
23
OTHERS/ADDITIONAL INFORMATION
Grant of Restricted Share Units under the PRE-IPO ESOP
Reference is made to the disclosure on the details of outstanding awards granted under the Pre-IPO 
ESOP in the section headed “Statutory and General Information – D. Share Incentive Plans – 1. 
Pre-IPO ESOP – Details of outstanding awards granted” in Appendix IV to the Prospectus.
The Company announces that on 25 August 2026, it has granted restricted share units (RSUs) to 
seven eligible participants under the Pre-IPO ESOP (who are consultants of the Group and not 
Directors, members of the senior management or connected persons of the Company) to receive an 
aggregate of 399,350 Class B Shares under the Pre-IPO ESOP, representing approximately 0.01% 
of the issued Shares immediately following the completion of the Global Offering (assuming the 
Assumptions). The grant of new RSUs since the Latest Practicable Date in the Prospectus is not 
material to the Company either on an individual basis and on an aggregate basis. For the avoidance 
of doubt, no further grant of options has been made since the Latest Practicable Date, and the 
disclosure in respect of outstanding options under the Pre-IPO ESOP in the Prospectus remains the 
same.
Taking into account the grant of RSUs on 25 August 2026, as of the date of this announcement, 
RSUs to receive a total of 15,949,700 Class B Shares had been granted and were outstanding 
under the Pre-IPO ESOP. Immediately following completion of the Global Offering (assuming the 
Assumptions), the aggregate number of Class B Shares underlying all options and RSUs granted 
represents approximately 4.07% of the issued Shares immediately following the completion of 
the Global Offering. Assuming full vesting and exercise of all options and RSUs granted under 
the Pre-IPO ESOP, the shareholding of the Shareholders immediately following completion of 
the Global Offering (assuming the Assumptions) will be diluted by approximately 4.07% and the 
Company’s earnings per Share will be diluted by approximately 4.07%.
Allocations of Offer Shares to the existing Shareholders and/or Cornerstone Investors and/or 
their close associates with consent under paragraph 18 of Chapter 4.15 of the Guide for New 
Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph 18 
of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to allocate further 
Offer Shares in the International Offering to certain existing Shareholders, Cornerstone Investors 
and/or their close associates as placees (the “Size-based Exemption Participants”), subject to the 
following conditions (the “Size-based Exemption”):
(a) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;
(b) 
the Offer Shares allocated to the Size-based Exemption Participants who are existing 
shareholders and/or their close associates (whether as Cornerstone Investors and/or as 
placees) as permitted under this exemption do not exceed 30% of the total number of Offer 
Shares offered under the Global Offering;

<<<PAGE 24>>>
24
(c) 
each Director, chief executive and Controlling Shareholder of the Company confirms that 
no securities have been allocated to them or their respective close associates under the 
Size-based Exemption;
(d) 
the allocation to Size-based Exemption Participants will not affect the Company’s ability to 
satisfy its public float requirement under Rule 8.08(1) of the Listing Rules; and
(e) 
details of the allocation to Size-based Exemption Participants under the Size-based Exemption 
will be disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to Cornerstone Investors, please refer to the section 
headed “Allotment Results Details — International Offering — Allottees with Waivers/Consents 
Obtained” in this announcement.
Placing to existing Shareholders and/or their close associates with a waiver from the strict 
compliance with Rule 10.04 of the Listing Rules and a prior consent under paragraph 1C(2) 
of the Placing Guidelines
The Company has applied to the Stock Exchange, and the Stock Exchange has granted, a 
waiver from the strict compliance with Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of the Placing Guidelines to permit the Company to allocate such Offer Shares 
in the International Offering to the relevant existing Shareholders (the “Minority Existing 
Shareholders”) and/or their close associates listed above, on the following grounds which are 
consistent with all applicable conditions under paragraph 14 of Chapter 4.15 of the Guide for New 
Listing Applicants:
(a) 
the Minority Existing Shareholders are interested in less than 5% of the Company’s voting 
rights prior to the completion of the Global Offering;
(b) 
each of the Minority Existing Shareholders is not a core connected person (as defined under 
the Listing Rules) of the Company or any close associate (as defined under the Listing Rules) 
of any such core connected person immediately prior to or following the Global Offering;
(c) 
each of the Minority Existing Shareholders has no right to appoint Directors (which, for the 
avoidance of doubt, does not include the director nomination right of a Shareholder under the 
Articles of Association) and does not have other special rights upon the Listing;
(d) 
the allocation to the Minority Existing Shareholders and/or their close associates will not 
affect the Company’s ability to satisfy the public float requirement of Rule 8.08 of the Listing 
Rules;
(e) 
the relevant information in respect of the allocation to each of the Minority Existing 
Shareholders and/or its close associates will be disclosed in this announcement;

<<<PAGE 25>>>
25
(f) 
the Joint Sponsors confirm to the Stock Exchange in writing that based on (i) their 
discussions with the Company and the Overall Coordinators; and (ii) the confirmations 
provided to the Stock Exchange by the Company and the Overall Coordinators (confirmations 
(g) and (h) mentioned below), and to the best of their knowledge and belief, it has no reason 
to believe that any of the Minority Existing Shareholders or its close associates received any 
preferential treatment by virtue of its relationship with the Company following the principles 
set out in Chapter 4.15 of the Guide for New Listing Applicants, and details of the allocation 
will be disclosed in this announcement;
(g) 
the Company confirms to the Stock Exchange in writing that no preferential treatment has 
been, nor will be, given to any of the Minority Existing Shareholders or its close associates 
by virtue of its relationship with the Company following the principles set out in Chapter 4.15 
of the Guide for New Listing Applicants; and
(h) 
the Overall Coordinators confirm, to the best of their knowledge and belief, to the Stock 
Exchange in writing that no preferential treatment has been, nor will be, given to any of 
the Minority Existing Shareholders or its close associates by virtue of its relationship with 
the Company following the principles set out in Chapter 4.15 of the Guide for New Listing 
Applicants, and details of the allocation will be disclosed in this announcement.
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates, 
please refer to the section headed “Allotment Results Details — International Offering — Allottees 
with Waivers/Consents Obtained” in this announcement.
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines.

<<<PAGE 26>>>
26
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing 
Guidelines to permit the Company to allocate such Offer Shares in the International Offering to the connected clients. The allocation of 
Offer Shares to such connected clients is in compliance with all the conditions under the consent granted by the Stock Exchange. Details of 
the placement to connected clients are set out below:
No.
Connected distributor
Connected client
Relationship
Discretionary 
or non-
discretionary
Whether the 
connected 
client is a 
collective 
investment 
scheme which 
is not 
authorized by 
the SFC or is 
expected to 
hold the 
Offer Shares 
on behalf of 
such scheme
Number of 
Offer Shares 
to be 
allocated 
to the 
connected 
client
Approximate 
% of total 
number of 
Offer Shares 
under the 
Global 
Offering 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Approximate 
% of total 
issued Class 
B Shares 
under the 
Global 
Offering 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Approximate 
% of total 
issued Shares 
immediately 
following the 
completion 
of the Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
1.
UBS AG Hong Kong Branch 
(“UBS AG”)
UBS Asset Management 
(Singapore) Ltd. (“UBS AM 
Singapore”) (1)
UBS AG, UBS WM HK, UBS WM 
SG and UBS AM Singapore are 
members of the same group
Discretionary
No
3,230,000
1.2%
0.1%
0.1%
Global Wealth Management 
division of UBS AG Hong 
Kong Branch (“UBS WM 
HK”)
Global Wealth Management 
division of UBS AG Singapore 
Branch (“UBS WM SG”)

<<<PAGE 27>>>
27
No.
Connected distributor
Connected client
Relationship
Discretionary 
or non-
discretionary
Whether the 
connected 
client is a 
collective 
investment 
scheme which 
is not 
authorized by 
the SFC or is 
expected to 
hold the 
Offer Shares 
on behalf of 
such scheme
Number of 
Offer Shares 
to be 
allocated 
to the 
connected 
client
Approximate 
% of total 
number of 
Offer Shares 
under the 
Global 
Offering 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Approximate 
% of total 
issued Class 
B Shares 
under the 
Global 
Offering 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Approximate 
% of total 
issued Shares 
immediately 
following the 
completion 
of the Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
2.
Guotai Junan Securities (Hong 
Kong) Limited (“GTJA 
Securities”)
Fullgoal Asset Management (HK) 
Limited (“Fullgoal HK”) (2)
Fullgoal Fund, Haitong Securities 
and GTJA Securities are members 
of the same group
Discretionary
Yes
898,000
0.3%
0.03%
0.02%
Haitong International Securities 
Company Limited (“Haitong 
Securities”)
Fullgoal Fund Management Co., 
Ltd. (“Fullgoal Fund”)(2)
Discretionary
Yes
1,522,000
0.5%
0.1%
0.04%

<<<PAGE 28>>>
28
Note:
1. 
UBS AG is an overall coordinator under the Global Offering. UBS WM HK and UBS WM SG are sub-brokers under the Global Offering. UBS AM Singapore 
is a member of the same group of companies as UBS AG, UBS WM HK and UBS WM SG. As a result, UBS AM Singapore is a connected client of UBS AG, 
UBS WM HK and UBS WM SG. UBS AM Singapore proposes to participate as a placee to subscribe for the Offer Shares for and on behalf of its underlying 
client under the Global Offering. UBS AM Singapore is a wholly owned subsidiary of UBS Asset Management AG, an investment management company, which 
is wholly ultimately owned by UBS Group AG, which is a company organized under Swiss law as a corporation that has issued shares of common stock to 
investors. UBS Group AG’s shares are listed on the SIX Swiss Exchange (stock code: UBSG) and the New York Stock Exchange (stock code: UBS).
UBS AM Singapore will hold the Offer Shares in its capacity as discretionary investment manager managing assets on behalf of each of UBS (LUX) EQUITY 
FUND — GREATER CHINA (USD), UBS (LUX) EQUITY FUND — CHINA OPPORTUNITY (USD), UBS (HK) FUND SERIES — CHINA OPPORTUNITY 
EQUITY (USD), UBS (LUX) EQUITY SICAV — ALL CHINA (USD) and certain other segregated accounts and mandates. The subscription will be fully funded 
by the personal assets of the underlying client. To the best knowledge of UBS AM Singapore after due enquiry, each of its underlying clients is an independent 
third party of UBS AM Singapore, UBS AG, UBS WM HK and UBS WM SG and the companies which are members of the same group of UBS AG, UBS WM 
HK and UBS WM SG and UBS AM Singapore.
2. 
Fullgoal HK is a wholly owned subsidiary of Fullgoal Fund, which is owned by Guotai Haitong as to 27.775%. Each of GTJA Securities and Haitong Securities 
is a subsidiary of Guotai Haitong. Each of Fullgoal HK and Fullgoal Fund is considered as a member of the same group of companies as GTJA Securities and 
Haitong Securities and therefore is a connected client of GTJA Securities and Haitong Securities.
Fullgoal HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their investors (the “Fullgoal HK 
Ultimate Clients”), each of which is, to the best knowledge of Fullgoal HK, (i) an independent third party of Fullgoal HK, GTJA Securities, Haitong Securities 
and the companies which are members of the same group of companies as Fullgoal HK, GTJA Securities and Haitong Securities; and (ii) a collective investment 
scheme which is not authorized by the SFC (save for Fullgoal China Small-Mid Cap Growth Fund, which is a SFC authorized fund (CE no.: BNY686)). Save as 
disclosed below, no ultimate beneficial owner holds 30% or more interest in the funds.

<<<PAGE 29>>>
29
The details of the Fullgoal HK Ultimate Clients are as follows:
Fund Name
Whether the Scheme is 
Publicly Marketed
Fund Manager
UBO of Fund 
Manager
UBO of the Fullgoal HK Ultimate Clients
The University of Hong 
Kong-Hong Kong and 
China Equity Fund
Not publicly marketed
Fullgoal HK
Fullgoal Fund
The ultimate beneficial owner is “The 
University of Hong Kong”
Fullgoal China Growth Select 
Fund
Not publicly marketed
Fullgoal HK
Fullgoal Fund
The ultimate beneficial owner is an 
individual, who is independent of the 
Company and its subsidiaries
Fullgoal China Opportunities 
Fund
Not publicly marketed
Fullgoal HK
Fullgoal Fund
The ultimate beneficial owners are three 
investors which are entities and funds 
and independent of the Company and its 
subsidiaries
Fullgoal China Small-Mid 
Cap Growth Fund
Yes
Fullgoal HK
Fullgoal Fund
No single ultimate beneficial owner holds 
30% or more interest
HI-Aktien China 1-SFonds
Not publicly marketed
Fullgoal HK
Fullgoal Fund
The ultimate beneficial owner is a 
European pension
BMO Greater China Fund
Yes
Fullgoal HK
Fullgoal Fund
No single ultimate beneficial owner holds 
30% or more interest
Fullgoal Fund will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their investors (the “Fullgoal 
Fund Ultimate Clients”), each of which is, to the best knowledge of Fullgoal Fund, (i) an independent third party of Fullgoal Fund, GTJA Securities, Haitong 
Securities and the companies which are members of the same group of companies as GTJA Securities, Haitong Securities and Fullgoal Fund; and (ii) a collective 
investment scheme which is not authorized by the SFC. No ultimate beneficial owner holds 30% or more interest in the funds.

<<<PAGE 30>>>
30
The details of the Fullgoal Fund Ultimate Clients are as follow:
Fund Name
Whether the Scheme is 
Publicly Marketed
Fund Manager
UBO of Fund 
Manager
UBO of the Fullgoal Fund Ultimate 
Clients
FULLGOAL DIVIDEND 
SELECTED HYBRID 
FUND
Yes
Fullgoal Fund
N/A
No single ultimate beneficial owner holds 
30% or more interest
CMB-FULLGOAL BLUE 
CHIP SELECTED EQUITY 
FUND (QDII)
Yes
Fullgoal Fund
N/A
No single ultimate beneficial owner holds 
30% or more interest
ICBC Fullgoal global 
technology & internet fund
Yes
Fullgoal Fund
N/A
No single ultimate beneficial owner holds 
30% or more interest
Fullgoal Global Consumption 
Selected Hybrid Fund
Yes
Fullgoal Fund
N/A
No single ultimate beneficial owner holds 
30% or more interest
ICBC Fullgoal China Small & 
Mid Cap (HK listed) Equity 
Fund
Yes
Fullgoal Fund
N/A
No single ultimate beneficial owner holds 
30% or more interest

<<<PAGE 31>>>
31
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
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated 24 August 2026 issued by SHEIN Global 
Holdings Limited for detailed information about the Global Offering described above before 
deciding whether or not to invest in the Offer Shares thereby being offered. Potential investors 
of the Offer Shares should note that the Joint Sponsors and the Sponsor-overall Coordinators 
(for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate 
their obligations under the Hong Kong Underwriting Agreement with immediate effect upon the 
occurrence of any of the events set out in the section headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Hong Kong Underwriting 
Agreement — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong 
Kong time) on the Listing Date (which is currently expected to be on 1 September 2026).
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering and before any exercise of the 
Over-allotment Option, the total number of the Class B Shares held by the public represents 
approximately 60.62% of the total number of issued Class B Shares of the Company, which is 
higher than the prescribed percentage of Class B Shares required to be held in public hands of 10% 
under Rule 8.08(1) of the Listing Rules calculated based on the Offer Price, thereby satisfying the 
public float requirement under Rule 8.08(1) of the Listing Rules.

<<<PAGE 32>>>
32
Based on the Offer Price of HK$48.56 per Offer Share, and taking into account the lock-up 
undertakings by the Controlling Shareholders, existing Shareholders, cornerstone investors and 
certain placees who are existing shareholders or their close associates as set out in “Lock-up 
Undertakings” above, the free float of the Company upon completion of the Global Offering is no 
less than HK$600 million, and therefore the Company satisfies the free float requirement under 
Rule 8.08A of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering and 
before any exercise of the Over-allotment Option, (i) no placee will, individually, be placed with 
more than 10% of the enlarged issued share capital of the Company immediately after the Global 
Offering; (ii) there will not be any new substantial Shareholder immediately after the Global 
Offering; (iii) the three largest public shareholders of the Company do not hold more than 50% of 
the Class B Shares in public hands at the time of the Listing in compliance with Rules 8.08(3) and 
8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at the time of the Listing 
in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, 1 
September 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Hong Kong Underwriting 
Agreement — Grounds for Termination” in the Prospectus has not been exercised. Investors who 
trade the Class B Shares on the basis of publicly available allocation details prior to the receipt of 
Share certificates or prior to the Share certificates becoming valid evidence of title do so entirely 
at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Tuesday, 1 
September 2026 (Hong Kong time), it is expected that dealings in the Class B Shares on the Stock 
Exchange will commence at 9:00 a.m. on Tuesday, 1 September 2026 (Hong Kong time). The 
Class B Shares will be traded in board lots of 100 Class B Shares each, and the stock code of the 
Class B Shares will be 00625.
By order of the Board
SHEIN Global Holdings Limited
Mr. Yangtian Xu
Chairman of the Board, Executive Director 
and Chief Executive Officer
Hong Kong, 31 August 2026
As at the date of this announcement, the board of directors of the Company comprises: (i) Mr. 
Yangtian Xu, Ms. Miao Miao, Ms. Xiaoqing Gu and Mr. Xiaoqing Ren as executive directors; and 
(ii) Mr. Denny Ting Bun Lee, Mr. Hongbin Cai and Mr. Ming Yan Lim as proposed independent 
non-executive directors (effective upon Listing).
