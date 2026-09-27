# 配发结果公告抽取任务：9637.HK Alebund Pharmaceuticals (Jiangsu) Limited - B - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**26/06/2026 22:44**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0626/2026062603033.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"9637.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities in 
the United States or in any other jurisdictions in which such offer or solicitation would be unlawful. The securities 
mentioned herein have not been, and will not be, registered under the United States Securities Act of 1933 as amended 
from time to time (the “U.S. Securities Act”) or any state securities law of the United States. The securities may not 
be offered, sold, pledged or transferred within the United States, except in transactions exempt from, or not subject 
to, the registration requirements of the U.S. Securities Act and in compliance with any applicable state securities 
laws. There will be no public offer of the Offer Shares in the United States. The Offer Shares are being offered and 
sold solely (1) to qualified institutional buyers as defined in Rule 144A under the U.S. Securities Act pursuant to an 
exemption from registration under the U.S. Securities Act; and (2) outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act and applicable laws of each jurisdiction where those offers and 
sales occur.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
June 18, 2026 (the “Prospectus”) issued by Alebund Pharmaceuticals (Jiangsu) Limited (禮邦醫藥(江蘇)股份有限公
司) (the “Company”) for detailed information about the Global Offering described below before deciding whether or 
not to invest in the H Shares thereby being offered. Any investment decision in relation to the Offer Shares should be 
taken solely in reliance on the information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
In connection with the Global Offering, Jefferies Hong Kong Limited, as the stabilization manager (the “Stabilization 
Manager”), or any person acting for it and on behalf of the Underwriters, may over-allocate or effect transactions with 
a view to stabilizing or supporting the market price of the Shares at a level higher than that which might otherwise 
prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilization Manager (or any 
person acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will be conducted at 
the absolute discretion of the Stabilization Manager (or any person acting for it) and in what the Stabilization Manager 
reasonably regards as the best interest of the Company, (b) may be discontinued at any time and (c) is required to be 
brought to an end within 30 days of the last day for lodging applications under the Hong Kong Public Offering. Such 
stabilization action, if commenced, may be effected in all jurisdictions where it is permissible to do so, in each case 
in compliance with all applicable laws, rules and regulatory requirements, including the Securities and Futures (Price 
Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures 
Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that stabilizing action cannot be taken to support the price of the Shares for longer 
than the stabilization period which begins on the Listing Date, and is expected to expire on the 30th day after the last 
day for the lodging of applications under the Hong Kong Public Offering. After this date, no further stabilizing action 
may be taken, demand for the Shares, and therefore the price of the Shares, could fall.
Potential investors of the Offer Shares should note that the Joint Representatives (for themselves and on behalf of 
the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
Monday, June 29, 2026).

<<<PAGE 2>>>
2
Alebund Pharmaceuticals (Jiangsu) Limited
禮邦醫藥( 江蘇) 股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the 
Global Offering
:
56,755,400 H Shares (subject to the  
Over-allotment Option)
Number of Hong Kong Offer Shares
:
5,675,600 H Shares
Number of International Offer Shares
:
51,079,800 H Shares (subject to the  
Over-allotment Option)
Offer Price
:
HK$22.60 per Offer Share, plus brokerage 
of 1.0%, AFRC transaction levy of 
0.00015%, SFC transaction levy of 
0.0027% and Stock Exchange trading 
fee of 0.00565% (payable in full on 
application in Hong Kong dollars and 
subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
09637
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators,
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Jefferies
BofA Securities
HTSC
(no particular order)
Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
CLSA Limited
BOCI

<<<PAGE 3>>>
3
Alebund Pharmaceuticals (Jiangsu) Limited
禮邦醫藥( 江蘇) 股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE
 AND ALLOTMENT RESULTS
Warning: In view of high concentration of shareholding in a small number of H Shareholders, H 
Shareholders and prospective investors should be aware that the price of the H Shares could move 
substantially even with a small number of H Shares traded and should exercise extreme caution 
when dealing in the H Shares.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated June 18, 2026 (the “Prospectus”) issued by 
Alebund Pharmaceuticals (Jiangsu) Limited (禮邦醫藥(江蘇)股份有限公司) (the “Company”).
SUMMARY
Company information
Stock code
09637
Stock short name
ALEBUND-B
Dealings commencement date
June 29, 2026*
* see note at the end of the announcement
Price Information
Final Offer Price
HK$22.60
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the Over-allotment Option)
56,755,400 
H Shares
Final Number of Offer Shares in Hong Kong Public Offering
5,675,600 
H Shares
Final Number of Offer Shares in International Offering (before 
exercise of the Over-allotment Option)
51,079,800 
H Shares
Number of issued Shares upon Listing (before exercise of the Over-
allotment Option)
339,852,231
Shares
Over-allocation
Number of Offer Shares over-allocated
8,513,300
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.

<<<PAGE 4>>>
4
Proceeds
Gross proceeds(Note)
HK$1,282.7 million
 Less: Estimated listing expenses payable based on 
     Offer Price
HK$101.9 million
Net proceeds
HK$1,180.8 million
Note: Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
145,729
No. of successful applications
35,131
Subscription level
963.56 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong Public 
Offering
5,675,600 H Shares
No. of Offer Shares reallocated from the International Offering 
(claw-back)
N/A
Final no. of Offer Shares under the Hong Kong Public Offering
5,675,600 H Shares
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering
10.00%
Note: For details of the final allocation of the H Shares to the Hong Kong Public Offering, investors 
can refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
93
Subscription level
19.77 times
No. of Offer Shares initially available under the International 
Offering
51,079,800 H Shares
No. of Offer Shares reallocated to the Hong Kong Public Offering 
(claw-back)
N/A
Final no. of Offer Shares under the International Offering
51,079,800 H Shares
% of Offer Shares under the International Offering to the Global 
Offering
90.00%

<<<PAGE 5>>>
5
The Directors confirm that, to the best of their knowledge, information and belief, save for 
consents under paragraphs 1C(1) and 1C(2) of Appendix F1 to the Listing Rules (the “Placing 
Guidelines”) and waivers from strict compliance with the requirements under Rules 9.09(b) (if 
applicable) and 10.04 of the Listing Rules pursuant to Chapters 2.3 and 4.15 of the Guide for 
New Listing Applicants (“Listing Guide”) granted by the Stock Exchange to permit the Company 
to, among other things, place certain H Shares in the International Offering to certain existing 
Shareholders and/or their close associates and certain connected clients, (i) none of the Offer 
Shares subscribed by the placees and the public have been financed directly or indirectly by the 
Company, any of the Directors, chief executive of the Company, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates; and (ii) 
none of the placees and the public who have purchased the Offer Shares are accustomed to taking 
instructions from the Company, any of the Directors, chief executive of the Company, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates in relation to the acquisition, disposal, voting or other disposition of H Shares 
registered in his/her/its name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
Investor (1)
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
issued share 
capital after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing
shareholders
or their close
associates(2)
GIC Private Limited (“GIC”)(2)(3)
7,627,200
13.44%
2.24%
Yes
Loomis, Sayles & Company, L.P. (“LSLP”)
3,266,000
5.75%
0.96%
No
Loomis Sayles Trust Company, LLC (“LSTC”)
1,067,600
1.88%
0.31%
No
RTW Master Fund, Ltd. (“RTW Master Fund”)
1,443,300
2.54%
0.42%
No
RTW Innovation Master Fund, Ltd. (“RTW Innovation 
Fund”)
1,198,400
2.11%
0.35%
No
RTW Biotech Opportunities Ltd. (“RTW Biotech”)
131,800
0.23%
0.04%
No
SymBiosis II, LLC (“SymBiosis”)(2)(4)
2,600,200
4.58%
0.77%
Yes
Huang River Investment Limited (“Huang River”)(2)(5)
1,386,700
2.44%
0.41%
Yes
Perfect Ten Holding Limited (“Perfect Ten”)(2)(5)
346,700
0.61%
0.10%
Yes
Cormorant Global Healthcare Master Fund, LP 
(“Cormorant”)
1,733,400
3.05%
0.51%
No
Dymon Asia Multi-Strategy Investment Master Fund 
(“DAMSIMF”)
1,733,400
3.05%
0.51%
No
GF Fund Management Co., Ltd. (“GF Fund 
Management”)
866,700
1.53%
0.26%
No

<<<PAGE 6>>>
6
Investor (1)
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
issued share 
capital after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing
shareholders
or their close
associates(2)
GF International Investment Management Limited (“GF 
Fund HK”)
866,700
1.53%
0.26%
No
China Universal Asset Management (Hong Kong) Company 
Limited (“China Universal (HK)”)
1,386,700
2.44%
0.41%
No
E Fund Management Co., Ltd. (“E Fund Management”)(6)
1,109,400
1.95%
0.33%
No
E Fund Management (Hong Kong) Co., Ltd. (“E Fund 
HK”)(6)
277,300
0.49%
0.08%
No
Golden Valley Value Select Master Fund (“Golden Valley 
Master”)(2)(7)
404,500
0.71%
0.12%
Yes
Golden Valley Global Limited (“Golden Valley Global”)(2)(7)
404,400
0.71%
0.12%
Yes
Loyal Valley Capital Advantage Fund III LP (“Loyal 
Valley Fund III”)(2)(7)
404,500
0.71%
0.12%
Yes
Total
28,254,900
49.78%
8.31%
Notes:
(1) 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in the Prospectus.
(2) 
Among the Cornerstone Investors, SymBiosis is an existing Shareholder. GIC is a close associate of Cliff Investment Pte. Ltd., an existing Shareholder. 
Huang River is a close associate of Guangxi Tencent Venture Investment Co., Ltd. (廣西騰訊創業投資有限公司) (“Guangxi Tencent”) and Perfect Ten, 
which are existing Shareholders. Each of Golden Valley Master and Golden Valley Global is a close associate of Loyal Valley Fund III, Shanghai Tanying 
Investment Partnership Enterprise (Limited Partnership) (上海檀英投資合夥企業(有限合夥)) (“Shanghai Tanying”) and Shanghai Jishi Lemei Private 
Equity Investment Fund Partnership (Limited Partnership) (上海濟世樂美私募投資基金合夥企業(有限合夥)) (“Shanghai Jishi Lemei”), each an existing 
Shareholder. The Stock Exchange has granted consents under paragraph 1C(2) of Appendix F1 of Placing Guidelines and Chapter 4.15 of the Listing Guide 
and a waiver from strict compliance from the requirements under Rule 9.09(b) and Rule 10.04 of the Listing Rules to permit each of GIC, SymBiosis, Huang 
River, Perfect Ten, Golden Valley Master, Golden Valley Global and Loyal Valley Fund III to participate in the International Offering as a cornerstone 
investor. Please refer to the section headed “Waivers and Exemptions – Consent and Waiver in respect of Allocation of H Shares to Certain Existing 
Shareholders and/or Their Close Associates” of the Prospectus for details.
(3) 
GIC, through Cliff Investment Pte. Ltd., owns approximately 4.48% of the total number of issued Shares of the Company before the Global Offering. Such 
shareholding is expected to be approximately 5.97% immediately following the completion of the Global Offering (and before any exercise of the Over-
allotment Option), after taking into account the Shares to be subscribed by GIC under the Cornerstone Investment.
(4) 
SymBiosis owns approximately 0.40% of the total issued Shares before the Global Offering. Such shareholding is expected to increase to approximately 
1.10% immediately following completion of the Global Offering (and before any exercise of the Over-allotment Option), after taking into account the Shares 
to be subscribed by it under the Cornerstone Investment.
(5) 
Guangxi Tencent and Perfect Ten collectively own approximately 11.73% of the total issued Shares before the Global Offering. Following completion of the 
Global Offering (and before any exercise of the Over-allotment Option), Guangxi Tencent, Perfect Ten and Huang River are expected to collectively hold 
10.28% of the total issued Shares after taking into account the Shares to be subscribed by Huang River and Perfect Ten under the Cornerstone Investment.
(6) 
The Company wishes to clarify that there was a clerical mistake in the Prospectus and the correct numbers of H Shares allocated to E Fund Management and 
E Fund HK are 1,109,400 and 277,300, respectively, as disclosed in this announcement.
(7) 
Loyal Valley Fund III, Shanghai Tanying and Shanghai Jishi Lemei collectively own approximately 6.40% of the total number of issued Shares before 
the Global Offering. Immediately following completion of the Global Offering (and before any exercise of the Over-allotment Option), Loyal Valley 
Fund III, Shanghai Tanying, Shanghai Jishi Lemei, Golden Valley Master and Golden Valley Global are expected to collectively hold 5.69% of the total 
issued Shares, after taking into account the Shares to be subscribed by Loyal Valley Fund III, Golden Valley Master and Golden Valley Global under the 
Cornerstone Investment.

<<<PAGE 7>>>
7
Allottees with Waivers/Consents Obtained
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
Allottees with consent under paragraph 1C(2) of the Placing Guidelines and waiver from strict 
compliance with the requirements under Rule 9.09(b) (where applicable) and Rule 10.04 of the Listing 
Rules pursuant to Chapters 2.3 and 4.15 of the Listing Guide in relation to subscription for Offer 
Shares by existing Shareholder and/or their close associates(1)
Cornerstone Investors
GIC
7,627,200
13.44%
2.24%
A cornerstone 
investor 
and a close 
associate of 
an existing 
Shareholder
SymBiosis
2,600,200
4.58%
0.77%
A cornerstone 
investor and 
an existing 
Shareholder
Huang River
1,386,700
2.44%
0.41%
A cornerstone 
investor 
and a close 
associate 
of existing 
Shareholders
Golden Valley Master
404,500
0.71%
0.12%
A cornerstone 
investor 
and a close 
associate 
of existing 
Shareholders 
Golden Valley Global
404,400
0.71%
0.12%
A cornerstone 
investor 
and a close 
associate 
of existing 
Shareholders

<<<PAGE 8>>>
8
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
Loyal Valley Fund III 
404,500
0.71%
0.12%
A cornerstone 
investor and 
an existing 
Shareholder
Perfect Ten
346,700
0.61%
0.10%
A cornerstone 
investor and 
an existing 
Shareholder
Placees
LAV Star Limited(2)
693,360
1.22%
0.20%
A placee and 
a close 
associate 
of existing 
Shareholders(2)
LAV Star Opportunity Limited(2)
693,360
1.22%
0.20%
A placee and 
a close 
associate 
of existing 
Shareholders(2)
Quan Venture Fund II, L.P.(3)
520,100
0.92%
0.15%
A placee 
and a close 
associate of 
an existing 
Shareholder(3)
LAV Public Equity Master 
Fund(2)
346,680
0.61%
0.10%
A placee and 
a close 
associate 
of existing 
Shareholders(2)

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
Worldwide Healthcare Partners 
LLC(4)
260,100
0.46%
0.08%
A placee 
and a close 
associate of 
an existing 
Shareholder(4)
Verition Multi-Strategy Master 
Fund Ltd. 
13,000
0.02%
0.00%
A placee and 
an existing 
Shareholder
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the 
Listing Guide in relation to allocations to connected clients(5)
Huatai Capital Investment Limited 
(“HTCI”) 
2,920,300
5.15%
0.86%
A connected 
client
China Asset Management (Hong 
Kong) Limited (“ChinaAMC 
(HK)”) 
4,000
0.0070%
0.0012%
A connected 
client
Orient Asset Management (Hong 
Kong) Limited (“Orient AM 
(Hong Kong)”) 
650,000
1.15%
0.19%
A connected 
client

<<<PAGE 10>>>
10
Notes:
1. 
The Stock Exchange has granted a consent under paragraph 1C(2) of the Placing Guidelines and a waiver 
from strict compliance with the requirements under Rule 9.09(b) (where applicable) and 10.04 of the Listing 
Rules pursuant to Chapters 2.3 and 4.15 of the Listing Guide to permit Offer Shares be placed the above 
placees who are existing Shareholders and/or their close associates. Please refer to the section headed 
“Others/Additional Information – Allocation of H Shares to Certain Existing Shareholders and/or Their Close 
Associates” in this announcement.
2. 
As of the Latest Practicable Date, LAV Delta Limited, LAV Orchid Limited and LAV Efficacy Limited 
are existing Shareholders ultimately beneficially owned by Dr. SHI Yi, which collectively held 8.34% of 
the total issued Shares. Each of LAV Star Limited, LAV Star Opportunity Limited and LAV Public Equity 
Master Fund (together with LAV Delta Limited, LAV Orchid Limited and LAV Efficacy Limited, the “LAV 
entities”) is an entity ultimately beneficially owned by Dr. SHI Yi and therefore a close associate of existing 
Shareholders. Immediately following completion of the Global Offering and before the exercise of the Over-
allotment Options, the LAV entities are expected to collectively hold 7.46% of the total issued Shares.
3. 
Quan Venture Fund II, L.P. is the sole shareholder of QC Six Limited (an existing Shareholder), and therefore 
a close associate of an existing Shareholder. As of the Latest Practicable Date, QC Six Limited held 6.64% 
of the total issued Shares. Immediately following completion of the Global Offering and before the exercise 
of the Over-allotment Options, QC Six Limited and Quan Venture Fund II, L.P. are expected to collectively 
hold 5.68% of the total issued Shares.
4. 
Worldwide Healthcare Partners LLC and Emerging Markets Healthcare Partners LLC (an existing 
Shareholder) are funds both managed under Exome Asset Management LLC, the investment adviser. Samuel 
D. Isaly is the ultimate beneficial owner of Exome Asset Management LLC. Therefore, Worldwide Healthcare 
Partners LLC is a close associate of an existing Shareholder. As of the Latest Practicable Date, Emerging 
Markets Healthcare Partners LLC held 0.40% of the total issued Shares. Immediately following completion 
of the Global Offering and before the exercise of the Over-allotment Options, Emerging Markets Healthcare 
Partners LLC and Worldwide Healthcare Partners LLC are expected to collectively hold 0.41% of the total 
issued Shares. 
5. 
The H Shares placed to such allottees are held on behalf of independent third parties (as defined in Chapter 
4.15 of the Listing Guide, and are in compliance with all the conditions under the consent granted by the 
Stock Exchange. For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 
of the Listing Guide in relation to allocations to connected clients, please refer to the section headed “Others/
Additional Information – Placing to connected clients with a prior consent under paragraph 1C(1) of the 
Placing Guidelines” in this announcement.

<<<PAGE 11>>>
11
LOCK-UP UNDERTAKINGS
Cornerstone Investors
Investor(1)
Number of H Shares 
held in the Company 
subject to lock-up 
undertakings 
upon Listing
% of shareholding
 in the Company 
subject to lock-up 
undertakings 
upon Listing 
(assuming the
Over-allotment
Option is not
exercised)
Last day subject to 
the lock-up 
undertaking(1)
GIC
7,627,200
2.24%
December 28, 2026
LSLP
3,266,000
0.96%
December 28, 2026
LSTC
1,067,600
0.31%
December 28, 2026
RTW Master Fund
1,443,300
0.42%
December 28, 2026
RTW Innovation Fund
1,198,400
0.35%
December 28, 2026
RTW Biotech
131,800
0.04%
December 28, 2026
SymBiosis
2,600,200
0.77%
December 28, 2026
Huang River
1,386,700
0.41%
December 28, 2026
Perfect Ten
346,700
0.10%
December 28, 2026
Cormorant
1,733,400
0.51%
December 28, 2026
DAMSIMF
1,733,400
0.51%
December 28, 2026
GF Fund Management
866,700
0.26%
December 28, 2026
GF Fund HK
866,700
0.26%
December 28, 2026
China Universal (HK)
1,386,700
0.41%
December 28, 2026
E Fund Management
1,109,400
0.33%
December 28, 2026
E Fund HK
277,300
0.08%
December 28, 2026
Golden Valley Master
404,500
0.12%
December 28, 2026
Golden Valley Global
404,400
0.12%
December 28, 2026
Loyal Valley Fund III
404,500
0.12%
December 28, 2026
Subtotal
28,254,900
8.31%
Note:
1. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on December 
28, 2026, being six months following the Listing Date. The Cornerstone Investors will cease to be prohibited 
from disposing of or transferring H Shares subscribed for pursuant to the relevant cornerstone investment 
agreements after the indicated date.

<<<PAGE 12>>>
12
Existing Shareholders (including the Pre-IPO Investors as defined in the “History, 
Development and Corporate Structure” section of the Prospectus)
Name
Number of Shares 
held in the
Company subject to 
lock-up undertakings 
upon Listing
% of
shareholding in the 
Company subject to 
lock-up 
undertakings upon 
Listing (assuming the 
Over-allotment Option 
is not exercised)
Last day subject to the 
lock-up undertakings(1)
Aleyuan Inc.
4,631,750
1.36%
June 28, 2027
Dr. Gavin Guoyao Xia
285
0.0001%
June 28, 2027
AleyuanGX Limited
11,866,156
3.49%
June 28, 2027
Jin Tian, M.D.
285
0.0001%
June 28, 2027
AleyuanJT Limited
6,844,123
2.01%
June 28, 2027
Aleyuan Limited
4,601,037
1.35%
June 28, 2027
Shanghai Chunyuan Pharmaceutical Technology Partnership (Limited 
Partnership) (上海純沅醫藥科技合夥企業(有限合夥))
1,815,215
0.53%
June 28, 2027
Yangzhou Liyue Consulting Management Partnership (Limited 
Partnership) (揚州禮悅諮詢管理合夥企業(有限合夥))
21,124,229
6.22%
June 28, 2027
Ms. Wang Yun
285
0.0001%
June 28, 2027
Dr. Zhang Huading
285
0.0001%
June 28, 2027
Shanghai Yuanyue Consulting Management Partnership (Limited 
Partnership) (上海沅悅諮詢管理合夥企業(有限合夥))
16,338,132
4.81%
June 28, 2027
Fortuna Limited 
1,517,931
0.45%
June 28, 2027
BCeGFR Limited 
623,742
0.18%
June 28, 2027
Guangxi Tencent(2)
30,965,311(2)
9.11%
June 28, 2027
Perfect Ten(2)
2,247,477(2)
0.66%
June 28, 2027
Yangzhou Guojin Libang Venture Capital Fund (Limited Partnership) 
(揚州國金禮邦創業投資基金(有限合夥))
24,722,321
7.27%
June 28, 2027
Yangzhou Guojin Emerging Industry Investment Fund (Limited 
Partnership) (揚州市國金新興產業投資基金合夥企業(有限合夥))
2,502,151
0.74%
June 28, 2027
LAV Delta Limited
18,068,978
5.32%
June 28, 2027
LAV Orchid Limited
5,162,925
1.52%
June 28, 2027
LAV Efficacy Limited
374,580
0.11%
June 28, 2027
Cliff Investment Pte. Ltd.(2)
12,668,524(2)
3.73%
June 28, 2027
Loyal Valley Fund III(2)
12,356,256(2)
3.64%
June 28, 2027
Shanghai Tanying(2)
2,884,284(2)
0.85%
June 28, 2027
Shanghai Jishi Lemei(2)
2,884,284(2)
0.85%
June 28, 2027

<<<PAGE 13>>>
13
Name
Number of Shares 
held in the
Company subject to 
lock-up undertakings 
upon Listing
% of
shareholding in the 
Company subject to 
lock-up 
undertakings upon 
Listing (assuming the 
Over-allotment Option 
is not exercised)
Last day subject to the 
lock-up undertakings(1)
QC Six Limited
18,790,247
5.53%
June 28, 2027
Suzhou Lirui Equity Investment Center (Limited Partnership) 
(蘇州禮瑞股權投資中心(有限合夥))
10,415,235
3.06%
June 28, 2027
Suzhou Lirun Equity Investment Centre (LP) (蘇州禮潤股權投資中心
(有限合夥))
5,802,840
1.71%
June 28, 2027
Dezhou Liangyi Mifang Health Venture Capital Partnership (Limited 
Partnership) (德州兩儀冪方康健創業投資合夥企業(有限合夥))
8,311,638
2.45%
June 28, 2027
Victory Eagle Group Limited
6,194,693
1.82%
June 28, 2027
Beijing Yuanqing Bencao Equity Investment Center, L.P. 
(北京元清本草股權投資中心(有限合夥))
6,001,766
1.77%
June 28, 2027
Shanghai Liyizhen Management Consulting Partnership Enterprise 
(Limited Partnership) (上海禮一臻管理諮詢合夥企業(有限合夥))
4,856,921
1.43%
June 28, 2027
Shanghai Liyuanzhen Management Consulting Partnership Enterprise 
(Limited Partnership) (上海禮元臻管理諮詢合夥企業(有限合夥))
766,442
0.23%
June 28, 2027
Beijing New Dynamic II Equity Investment Fund (Limited Partnership) 
(北京新動力二期股權投資基金(有限合夥))
5,081,814
1.50%
June 28, 2027
OCXPROURO Limited
2,624,360
0.77%
June 28, 2027
Rosy Lead Holding Limited
2,000,598
0.59%
June 28, 2027
Octagon Investments Master Fund LP
924,874
0.27%
June 28, 2027
Octagon Coinvest Opportunities Fund LP 
3,546,931
1.04%
June 28, 2027
Andorra Investment Limited
4,366,320
1.28%
June 28, 2027
SymBiosis(2)
1,123,739(2)
0.33%
June 28, 2027
YuanBio Venture Capital II L.P.
3,118,788
0.92%
June 28, 2027
Verition Multi-Strategy Master Fund Ltd.
3,011,571
0.89%
June 28, 2027

<<<PAGE 14>>>
14
Name
Number of Shares 
held in the
Company subject to 
lock-up undertakings 
upon Listing
% of
shareholding in the 
Company subject to 
lock-up 
undertakings upon 
Listing (assuming the 
Over-allotment Option 
is not exercised)
Last day subject to the 
lock-up undertakings(1)
Yangzhou Dingyi Start-up Investment Partnership (Limited Partnership) 
(揚州鼎毅創業投資合夥企業(有限合夥))
2,502,151
0.74%
June 28, 2027
Loyal Earn Hong Kong Limited
1,517,931
0.45%
June 28, 2027
Phoenix Aurora Limited
1,498,318
0.44%
June 28, 2027
Suzhou Luanbu Nuojin Investment Center (Limited Partnership) 
(蘇州欒布諾瑾投資中心(有限合夥))
1,454,186
0.43%
June 28, 2027
Xiamen Qianshan Qiyong Investment Partnership (Limited Partnership) 
(廈門千杉啟永投資合夥企業(有限合夥))
1,342,333
0.40%
June 28, 2027
Emerging Markets Healthcare Partners LLC
1,123,739
0.33%
June 28, 2027
Hongtao Investment-I Ltd.
935,637
0.28%
June 28, 2027
Yangzhou Longtou Chuanghai I Industry Fund Partnership 
(Limited Partnership) (揚州龍投創海壹號產業基金合夥企業(有限合夥))
834,054
0.25%
June 28, 2027
Hainan Renze Zhenji Venture Investment Fund Partnership Enterprise 
(Limited Partnership) (海南仁澤真寄創業投資基金合夥企業(有限合夥))
749,159
0.22%
June 28, 2027
Note:
1. 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. The 
required lock-up for existing Shareholders ends on June 28, 2027, being 12 months following the Listing 
Date.
2. 
The numbers of Shares held by Perfect Ten, Loyal Valley Fund III, Shanghai Tanying, Shanghai Jishi Lemei, 
SymBiosis, Guangxi Tencent and Cliff Investment Pte. Ltd. in the table above do not take into account the 
Shares to be subscribed by them and/or their respective close associates in the Global Offering. The Company 
has applied to the Stock Exchange for, and the Stock Exchange has granted to the Company, a consent under 
paragraph 1C(2) of Appendix F1 and a waiver from strict compliance with the requirements under Rule 
9.09(b) (where applicable) and Rule 10.04 of the Listing Rules to permit the Company to allocate such Offer 
Shares in the International Offering to themselves and/or their respective close associates. For details, please 
refer to the sections headed “Allottees with Waivers/Consents Obtained” and “Others/Additional Information” 
in this announcement.

<<<PAGE 15>>>
15
PLACEE CONCENTRATION ANALYSIS
Placees
* Numbers 
of H Shares 
allotted
Allotment as 
% of 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option
Allotment as 
% of 
International 
Offering 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued)
Allotment as 
% of total 
Offer Shares 
(assuming 
no exercise 
of the 
Over-allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued)
Number of 
H Shares held 
upon Listing
% of 
total issued 
share capital 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of 
total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued)
Top 1
7,627,200
14.93%
12.80%
13.44%
11.69%
15,228,314
5.97%
5.83%
Top 5
23,895,200
46.78%
40.10%
42.10%
36.61%
31,496,314
10.76%
10.50%
Top 10
34,816,200
68.16%
58.42%
61.34%
53.34%
43,541,053
14.30%
13.95%
Top 25
56,207,600
110.04%
94.32%
99.03%
86.12%
109,898,910
42.65%
41.61%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders
* Numbers 
of H Shares 
allotted
Allotment as 
% of 
International 
Offering 
(assuming no 
exercise 
of the Over-
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
and new 
H Shares 
are issued)
Allotment as 
% of 
total Offer 
Shares 
(assuming 
no exercise 
of the 
Over-allotment 
Option)
Allotment as 
% of 
total Offer 
Shares 
(assuming the 
Over-allotment 
Option is 
exercised 
and new 
H Shares 
are issued)
Number of 
H Shares 
held upon 
Listing
% of 
total issued 
H Shares 
capital upon 
Listing 
(assuming no 
exercise 
of the Over-
allotment 
Option)
% of 
total issued 
H Shares 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is 
exercised 
and new 
H Shares 
are issued)
Number 
of Shares 
held upon 
Listing
Top 1
0
0.00%
0.00%
0.00%
0.00%
27,870,950
12.27%
11.83%
69,363,455
Top 5
11,094,000
21.72%
18.62%
19.55%
17.00%
96,992,311
42.70%
41.16%
177,169,722
Top 10
19,068,100
37.33%
32.00%
33.60%
29.21%
143,040,991
62.98%
60.70%
244,471,661
Top 25
36,562,500
71.58%
61.35%
64.42%
56.02%
196,306,263
86.43%
83.31%
307,701,823
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 16>>>
16
SHAREHOLDERS CONCENTRATION ANALYSIS
All 
Shareholders
* Numbers
of H Shares
allotted
Allotment as
% of
International
Offering
(assuming no
exercise
of the Over-
allotment
Option)
Allotment as
% of
International
Offering
(assuming the 
Over-allotment
Option is
exercised and 
new H Shares
are issued)
Allotment as
% of total 
Offer Shares
(assuming
no exercise
of the
Over-allotment
Option)
Allotment as
% of
total Offer 
Shares
(assuming the
Over-allotment
Option is 
exercised 
and new
H Shares
are issued)
Number of
H Shares
held upon
Listing
Number
of Shares
held upon
Listing
% of
total issued
share
capital upon
Listing
(assuming no
exercise
of the Over-
allotment
Option)
% of
total issued
share capital 
upon Listing 
(assuming the 
Over- allotment 
Option is 
exercised and 
new H Shares
are issued)
Top 1
0
0.00%
0.00%
0.00%
0.00%
27,870,950
69,363,455
20.41%
19.91%
Top 5
11,094,000
21.72%
18.62%
19.55%
17.00%
96,992,311 177,169,722
52.13%
50.86%
Top 10
19,068,100
37.33%
32.00%
33.60%
29.21%
141,833,281 246,588,606
72.56%
70.78%
Top 25
34,135,600
66.83%
57.28%
60.15%
52.30%
195,380,654 307,777,074
90.65%
88.35%
Note:
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
ALLOTTED
OF THE TOTAL 
NO. OF SHARES 
APPLIED FOR
POOL A
100
49,764
2,986 out of 49,764 to receive 100 Shares
6.00%
200
7,452
715 out of 7,452 to receive 100 Shares
4.80%
300
19,076
2,003 out of 19,076 to receive 100 Shares
3.50%
400
7,727
884 out of 7,727 to receive 100 Shares
2.86%
500
2,649
315 out of 2,649 to receive 100 Shares
2.38%
600
1,067
132 out of 1,067 to receive 100 Shares
2.06%
700
834
110 out of 834 to receive 100 Shares
1.88%
800
795
111 out of 795 to receive 100 Shares
1.75%
900
854
125 out of 854 to receive 100 Shares
1.63%
1,000
5,897
898 out of 5,897 to receive 100 Shares
1.52%
1,500
2,182
392 out of 2,182 to receive 100 Shares
1.20%
2,000
8,754
1,765 out of 8,754 to receive 100 Shares
1.01%
2,500
1,498
331 out of 1,498 to receive 100 Shares
0.88%
3,000
1,166
277 out of 1,166 to receive 100 Shares
0.79%
3,500
822
208 out of 822 to receive 100 Shares
0.72%

<<<PAGE 17>>>
17
NO. OF 
SHARES
APPLIED FOR
NO. OF 
VALID
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT
APPROXIMATE
PERCENTAGE 
ALLOTTED
OF THE TOTAL 
NO. OF SHARES 
APPLIED FOR
4,000
2,594
693 out of 2,594 to receive 100 Shares
0.67%
4,500
952
267 out of 952 to receive 100 Shares
0.62%
5,000
1,488
435 out of 1,488 to receive 100 Shares
0.58%
6,000
847
266 out of 847 to receive 100 Shares
0.52%
7,000
733
245 out of 733 to receive 100 Shares
0.48%
8,000
725
256 out of 725 to receive 100 Shares
0.44%
9,000
715
265 out of 715 to receive 100 Shares
0.41%
10,000
4,188
1,620 out of 4,188 to receive 100 Shares
0.39%
20,000
3,081
1,849 out of 3,081 to receive 100 Shares
0.30%
30,000
1,900
1,146 out of 1,900 to receive 100 Shares
0.20%
40,000
1,511
1,024 out of 1,511 to receive 100 Shares
0.17%
50,000
1,372
1,098 out of 1,372 to receive 100 Shares
0.16%
60,000
767
644 out of 767 to receive 100 Shares
0.14%
70,000
617
525 out of 617 to receive 100 Shares
0.12%
80,000
619
555 out of 619 to receive 100 Shares
0.11%
90,000
664
625 out of 664 to receive 100 Shares
0.10%
100,000
2,985
2,932 out of 2,985 to receive 100 Shares
0.10%
200,000
2,681
100 Shares
0.05%
138,976
Total number of Pool A successful applicants: 28,378
POOL B
300,000
3,540
300 Shares
0.10%
400,000
783
300 Shares plus 705 out of 783 to receive additional 100 
 Shares
0.10%
500,000
1,240
400 Shares
0.08%
1,000,000
560
600 Shares
0.06%
1,500,000
136
800 Shares
0.05%
2,000,000
138
1,000 Shares
0.05%
2,837,800
356
1,100 Shares
0.04%
6,753
Total number of Pool B successful applicants: 6,753
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 18>>>
18
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and Stock Exchange trading fee payable.

<<<PAGE 19>>>
19
OTHERS/ADDITIONAL INFORMATION
Allocation of H Shares to Certain Existing Shareholders and/or Their Close Associates
As Cornerstone Investors
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted us, 
a consent under paragraph 1C(2) of Appendix F1 and a waiver from strict compliance from 
the requirements under Rules 9.09(b) and 10.04 of the Listing Rules, to permit H Shares in the 
International Offering to be placed to the Existing Shareholders and/or their respective close 
associates to participate in the Global Offering as cornerstone investors, on the basis set out in 
Paragraph 18 of Chapter 2.3 of the Listing Guide and subject to the following conditions:
(a) 
the Company will comply with the public float requirement under Rule 19A.13A of the 
Listing Rules and the free float requirement under Rule 19A.13C of the Listing Rules;
(b) 
no preference in allocation has been, nor will be, given to GIC, SymBiosis, Huang River, 
Golden Valley Master, Golden Valley Global, Loyal Valley Fund III and Perfect Ten and/
or their respective close associates by virtue of their relationship with the Company other 
than the preferential treatment of assured entitlement at the Offer Price under a cornerstone 
investment and the terms of the cornerstone investment agreement with the Cornerstone 
Investors are substantially the same as the other cornerstone investment agreements following 
the principles set out in Chapters 2.3 and 4.15 of the Listing Guide;
(c) 
the Shares to be subscribed by and allocated to the aforesaid investors under the Global 
Offering will be at the same Offer Price and on substantially the same terms, or no more 
favorable than, the terms of the other cornerstone investors (including being subject to a 
lock-up period of six months from the Listing Date) and each of the aforesaid cornerstone 
investors shall pay and settle in full the consideration for the relevant Offer Shares before 
dealings commence on the Listing Date;
(d) 
each of the Company, the Joint Sponsors and the Overall Coordinators has provided the Stock 
Exchange with written confirmations in accordance with Chapters 2.3 and 4.15 of the Listing 
Guide; and
(e) 
the relevant information in respect of the allocation to the Cornerstone Investors is disclosed 
in the Prospectus and will be disclosed in this announcement.
All allocations of Offer Shares to the Existing Shareholders and/or their close associates are in 
compliance with all the conditions under the waiver and consent granted by the Stock Exchange.
Please refer to the section headed “Waivers and Exemptions – Consent and Waiver in respect of 
Allocation of H Shares to Certain Existing Shareholders and/or Their Close Associates” in the 
Prospectus for further details of the waiver and consent.

<<<PAGE 20>>>
20
As Placees
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted the 
Company, a consent under paragraph 1C (2) of Appendix F1 and a waiver from strict compliance 
with the requirements under Rule 10.04 of the Listing Rules to permit H Shares in the International 
Offering to be placed to the Existing Shareholders and/or their close associates to participate in the 
Global Offering on the following basis as set out in Paragraph 18 of Chapter 2.3 and Chapter 4.15 
of the Listing Guide, subject to the conditions as follows:
(a) 
the Company will comply with the public float requirement under Rule 19A.13A of the 
Listing Rules and the free float requirement under Rule 19A.13C of the Listing Rules;
(b) 
no preference in allocation has been, nor will be, given to LAV Star Limited, LAV Star 
Opportunity Limited, LAV Public Equity Master Fund, Worldwide Healthcare Partners 
LLC, Verition Multi-Strategy Master Fund Ltd. and Quan Venture Fund II, L.P. and/ or their 
respective close associates by virtue of their relationship with the Company;
(c) 
each of the Company, the Joint Sponsors and the Overall Coordinators has provided the Stock 
Exchange with written confirmations in accordance with Chapters 2.3 and 4.15 of the Listing 
Guide; and
(d) 
the relevant information in respect of the allocation to the existing Shareholders and/or their 
close associates has been disclosed in this announcement.
For details of the allocations of Offer Shares to the existing Shareholders and/or their respective 
close associates, please refer to the section headed “Allotment Results Details – International 
Offering – Allottees with Waivers/Consents Obtained” in this announcement.

<<<PAGE 21>>>
21
Placing to connected clients with prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such 
Offer Shares in the International Offering to the connected clients. The allocation of Offer Shares 
to such connected clients is in compliance with all the conditions under the consent granted by the 
Stock Exchange. Details of the placement to connected clients are set out below:
Connected Client
Connected 
Distributor
Relationship 
with the 
Connected 
Distributor
Whether the 
Connected Client 
will hold the 
beneficial interests 
of the Offer 
Shares on a non-
discretionary basis 
or discretionary 
basis for 
independent third 
parties
Number of 
Offer Shares 
to be allocated
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering(1)
Approximate 
percentage of 
the total issued 
share capital 
immediately 
following 
completion 
of the Global 
Offering
(1)
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering
(2)
Approximate 
percentage of 
the total issued 
share capital 
immediately 
following 
completion 
of the Global 
Offering
(2)
Part A – Connected Client holding the beneficial interest of the Offer Shares on a non-discretionary basis on behalf of independent third party
Huatai Capital 
Investment Limited 
(“HTCI”)
(3)
Huatai 
Financial 
Holdings 
(Hong Kong) 
Limited 
(“HTFH”)
HTFH is a 
member of the 
same group of 
companies as 
HTCI.
Non-discretionary
2,920,300
5.15%
0.86%
4.47%
0.84%
Part B – Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties
China Asset 
Management (Hong 
Kong) Limited 
(“ChinaAMC 
(HK)”)
(4)
CLSA Limited 
(“CLSA”) 
and CITIC 
Securities 
Brokerage 
(HK) Limited 
(“CSB”)
ChinaAMC (HK) 
is a member of 
the same group 
of companies as 
CLSA and CSB.
Discretionary
4,000
0.0070%
0.0012%
0.0061%
0.0011%
Orient Asset 
Management (Hong 
Kong) Limited 
(“Orient AM 
(Hong Kong)”)(5)
Orient 
Securities 
(Hong Kong) 
Limited 
(“Orient HK”)
Orient AM 
(Hong Kong) 
is a member of 
the same group 
of companies as 
Orient HK.
Discretionary
650,000
1.15%
0.19%
1.00%
0.19%
Notes:
1. 
Assuming the Over-allotment Option is not exercised.
2. 
Assuming the Over-allotment Option is fully exercised.

<<<PAGE 22>>>
22
3. 
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public 
offerings (“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products issued by 
appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. In 
connection with such products, the licensed domestic securities firms, through their Hong Kong affiliates, 
may participate in Hong Kong IPOs either as placees or cornerstone investors (the “Cross-border 
Derivatives Trading Regime”).
Huatai Securities Co., Ltd. (“HTSC”), the A shares of which are listed on the Shanghai Stock Exchange 
(stock code: 601688), the H shares of which are listed on the Stock Exchange (stock code: 6886), and the 
global depositary receipts of which are listed on the London Stock Exchange (LON: HTSC), is one of the 
domestic securities firms licensed to undertake cross-border derivatives trading activities. HTSC entered into 
an ISDA agreement (the “ISDA Agreement”) with its indirectly wholly-owned subsidiary, HTCI, to set out 
the principal terms of any future total return swap between HTSC and HTCI.
HTFH is the Connected Distributor. Pursuant to the ISDA Agreement, HTCI, which intends to participate 
in the International Offering as a placee, will hold the beneficial interest of the Offer Shares on a 
non-discretionary basis as the single underlying holder under a back-to-back total return swap (the “HT 
Back-to-back TRS”) to be entered by HTCI in connection with Huatai TRS (as defined below) placed by and 
fully funded (i.e. with no financing provided by HTCI) by the Huatai Ultimate Client (as defined below), by 
which, HTCI will, subject to customary fees and commissions, pass the full economic exposure of the Offer 
Shares ultimately to the Huatai Ultimate Client, which in effect, HTCI will hold the beneficial interest of the 
Offer Shares on behalf of the Huatai Ultimate Client. Both HTFH and HTCI are indirectly wholly-owned 
subsidiaries of HTSC. Accordingly, HTCI is considered as a “connected client” of HTFH pursuant to 
paragraph 1B(7) of the Placing Guidelines.
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investor as shown in the table below 
(the “Huatai Ultimate Client”) cannot directly subscribe for the Offer Shares but may invest in derivative 
products issued by domestic securities firms licensed to undertake cross-border derivatives trading activities, 
such as HTSC, with the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer 
Shares, the Huatai Ultimate Client, through its investment manager will place a total return swap order (the 
“Huatai TRS”) with HTSC in connection with the Global Offering and HTSC will place a HT Back-to-back 
TRS order to HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the HT 
Back-to-back TRS, HTCI participates in the Global Offering and subscribes for the Offer Shares through 
placing order with HTFH during the International Offering.
To the best of HTCI’s knowledge after having made all reasonable inquiries, the Huatai Ultimate Client is 
an Independent Third Party of (i) the Company, and its connected persons, and (ii) HTCI and the companies 
which are members of the same group of HTCI.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the HT Back-to-back TRS in connection 
with the Huatai TRS order placed by the Huatai Ultimate Client. Pursuant to the terms of the contracts of 
the HT Back-to-back TRS and the Huatai TRS, during the tenor of the HT Back-to-back TRS and the Huatai 
TRS, subject to customary fees and commissions, all economic returns of the Offer Shares will be ultimately 
passed to the Huatai Ultimate Client through the HT Back-to-back TRS and the Huatai TRS and all economic 
loss shall be ultimately borne by the Huatai Ultimate Client. HTCI will not take any economic return or bear 
any economic loss in relation to the Offer Shares.
Investment in the HT Back-to-back TRS and the Huatai TRS is similar to the investment in a qualified 
domestic institutional investor fund (“QDII”) in the way that the Huatai Ultimate Client would reap all 
the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through the 
exchange rate exposure on both the notional value of the investment and the profit and loss of the investment. 
In contrast, the profit and loss of the HT Back-to-back TRS and the Huatai TRS factor into account the 
fluctuation in RMB exchange rate upon termination of the Huatai TRS by converting the profit and loss using 
the current exchange rate at the time of termination. As such, the Huatai Ultimate Client would bear the 
exchange rate exposure of the profit and loss on settlement date.

<<<PAGE 23>>>
23
The Huatai Ultimate Client may exercise an early termination right to terminate the Huatai TRS at any time 
from the issue date of the Huatai TRS which should be on or after the date on which the Offer Shares are 
listed on the Stock Exchange at its own discretion. Upon the termination upon maturity or early termination 
of the Huatai TRS by the Huatai Ultimate Client, HTCI will dispose of the Offer Shares on the secondary 
market and the Huatai Ultimate Client will receive a final settlement amount in cash in accordance with 
the terms and conditions of the HT Back-to-back TRS and the Huatai TRS which should have taken into 
account all the economic returns or economic loss in relation to the Offer Shares. If upon the maturity of the 
Huatai TRS, the Huatai Ultimate Client intends to extend the investment period, subject to further agreement 
between HTSC and the relevant Huatai Ultimate Client, the term of the Huatai TRS could be extended by 
way of a new issuance or a tenor extension. Accordingly, HTSC will extend the term of the HT Back-to-back 
TRS by way of a new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass 
through the economic exposure to the Huatai Ultimate Client, an onshore client who places a Huatai TRS 
order with HTSC in connection with the Global Offering of the Company. HTCI will not exercise the voting 
rights of the Offer Shares during the tenor of the HT Back-to-back TRS.
During the life of the Huatai TRS and HT Back-to-back TRS, HTCI may continue to hold the Offer Shares 
in its custodian account, or to hold some or all of the Offer Shares in a prime brokerage account for stock 
borrowing purposes, where HTCI will lend out its holding of underlying Offer Shares in the form of stock 
borrowing loans consistent with market practice to lower its finance costs, provided that HTCI has the ability 
to call back the Offer Shares on loan at any time in order to satisfy its obligations under the HT Back-to-back 
TRS to ensure the economic interests are ultimately passed to the Huatai Ultimate Client.
The details of the Huatai Ultimate Client are as follows:
Name of HTCI Ultimate 
Client
Fund manager
Ultimate 
beneficial owner 
(“UBO”) of fund 
manager
Limited Partner/
Shareholder holding 
30% or more in the 
HTCI Ultimate Client
Jiaqi Jinhai No. 1 Private 
Securities Investment Fund 
(佳祺金海1號私募證券投資
基金)
Hangzhou Jiaqi Asset Management 
Co., Ltd.(杭州佳祺資產管理有限公
司)
YANG Liu (楊柳)
No other shareholder 
holds 30% or more of 
equity interest in the fund 
manager.
4. 
It is proposed that ChinaAMC (HK) participates as placee to subscribe for Offer Shares as a placee under the 
International Offering (“ChinaAMC (HK) Subscription”). In relation to the ChinaAMC (HK) Subscription, 
ChinaAMC (HK) will hold the Offer Shares in its capacity as the discretionary fund manager on behalf 
of underlying investors, each of which is an independent third party of the Company, its subsidiaries, its 
substantial shareholders, ChinaAMC (HK), CLSA, CSB and the companies which are members of the same 
group of CLSA and CSB.
5. 
It is proposed that Orient AM (Hong Kong) participates as placee to subscribe for Offer Shares as a placee 
under the International Offering (“Orient AM (Hong Kong) Subscription”). In relation to the Orient 
AM (Hong Kong) Subscription, Orient AM (Hong Kong) will hold the Offer Shares in its capacity as the 
discretionary fund manager on behalf of underlying investors, each of which is an independent third party 
of the Company, its subsidiaries, its substantial shareholders, Orient AM (Hong Kong), Orient HK and the 
companies which are members of the same group of Orient HK.

<<<PAGE 24>>>
24
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or 
any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or 
into the United States (including its territories and possessions, any state of the United States 
and the District of Columbia). This announcement does not constitute or form a part of any 
offer to sell or solicitation to purchase or subscribe for securities in the United States or in any 
other jurisdictions in which such offer to sell or solicitation would be unlawful. The securities 
mentioned herein have not been, and will not be, registered under the United States Securities 
Act of 1933 as amended from time to time (the “U.S. Securities Act”) or any state securities law 
of the United States. The securities may not be offered, sold, pledged or transferred within the 
United States, except in transactions exempt from, or not subject to, the registration requirements 
of the U.S. Securities Act and in compliance with any applicable state securities laws. There will 
be no public offer of the Offer Shares in the United States. 
The Offer Shares are being offered and sold solely (1) to qualified institutional buyers as defined 
in Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under 
the U.S. Securities Act; and (2) outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act and applicable laws of each jurisdiction where those 
offers and sales occur.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated June 18, 2026 issued by Alebund Pharmaceuticals 
(Jiangsu) Limited (禮邦醫藥(江蘇)股份有限公司) for detailed information about the Global 
Offering described below before deciding whether or not to invest in the H Shares thereby being 
offered.
* Potential investors of the Offer Shares should note that the Joint Representatives (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the 
occurrence of any of the events set out in the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in 
the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is 
currently expected to be on June 29, 2026).

<<<PAGE 25>>>
25
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering (before any exercise of the 
Over-allotment Option), the expected market capitalization of the Company’s Shares would be 
approximately HK$7,680.66 million, calculated based on the Offer Price of HK$22.60 per Offer 
Share. Under Rule 19A.13A(1), the minimum prescribed public float percentage shall be 19.53%. 
The total number of listed H Shares held by the public (being 177,590,166 H Shares) represents 
approximately 52.26% of the total issued Shares of the Company upon Listing. For details of the 
Shares held by certain of our Shareholders which shall not be counted towards the public float, see 
“History, Development and Corporate Structure – Public Float and Free Float” in the Prospectus 
for details. Therefore, the Company will be able to meet the minimum public float requirement 
under Rule 19A.13A.
Immediately following the completion of the Global Offering (before any exercise of the 
Over-allotment Option) and based on the Offer Price of HK$22.60 per Offer Share, the expected 
market value of the H Shares held by the public and not subject to disposal restrictions will be 
approximately HK$644.1 million, representing approximately 8.39% of the total issued Shares of 
the Company upon Listing, As such, the Company will be able to satisfy the free float requirement 
under Rule 19A.13C of the Listing Rules.
The Directors confirm that immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public shareholders of 
the Company do not hold more than 50% of the H Shares in public hands at the time of the Listing 
in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 
Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Monday, June 29, 
2026 (Hong Kong time), provided that the Global Offering has become unconditional and the right 
of termination described in the section headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has not been 
exercised. Investors who trade the H Shares on the basis of publicly available allocation details 
prior to the receipt of H Share certificates or prior to the H Share certificates becoming valid 
evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Monday, June 
29, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Monday, June 29, 2026 (Hong Kong time). The H Shares will be 
traded in board lots of 100 H Shares each, and the stock code of the H Shares will be 09637.
By order of the Board
Alebund Pharmaceuticals (Jiangsu) Limited
Dr. Gavin Guoyao Xia
Chairman of the Board, executive Director and 
Chief Executive Officer
Hong Kong, June 26, 2026

<<<PAGE 26>>>
26
As of the date of this announcement, the Board comprises (i) Dr. Gavin Guoyao Xia, Jin Tian, 
M.D., Ms. Wang Yun and Dr. Zhang Huading as executive Directors; (ii) Dr. Lu An as a non-
executive Director; and (iii) Dr. Xu Runhong, Dr. Zhui Chen and Mr. Leung Chi Wai as 
independent non-executive Directors.
