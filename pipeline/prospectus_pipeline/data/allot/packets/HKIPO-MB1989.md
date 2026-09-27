# 配发结果公告抽取任务：1989.HK Delton Technology (Guangzhou) Inc. - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**19/03/2026 22:09**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0319/2026031901556.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1989.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
  - 提示：最终基石股数 ÷ base offer（不含超额配售）。优先用公告基石表的 Total 行；若表内已给『假设超额配售权未行使』的百分比，可直接采用。

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
  - 提示：超额配售权实际行使并配发的股数；未行使填 0。另有 FULL EXERCISE OF THE OVER-ALLOTMENT OPTION 公告可交叉确认。
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
– 1 –
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) 
and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities 
in the United States or in any other jurisdictions. The securities mentioned herein have not been, and will not be, 
registered under the United States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) 
or securities law of any state or other jurisdiction of the United States. The securities may not be offered, sold, 
pledged or otherwise transferred within the United States except pursuant to an exemption from the registration 
requirements of the U.S. Securities Act and in compliance with any applicable state securities laws. The securities 
are being offered and sold outside the United States in offshore transactions in accordance with Regulation S 
under the U.S. Securities Act. There will be no public offer of securities in the United States.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. This announcement is not a prospectus. Potential investors should read the 
prospectus dated March 12, 2026 (the “Prospectus”) issued by Delton Technology (Guangzhou) Inc. (廣州廣合
科技股份有限公司) (the “Company”) for detailed information about the Global Offering described below before 
deciding whether or not to invest in the H Shares thereby being offered. Any investment decision in relation to the 
Offer Shares should be taken solely in reliance on the information in the Prospectus. The Company has not been 
and will not be registered under the U.S. Investment Company Act of 1940, as amended.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as 
those defined in the Prospectus.
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinators (for themselves and 
on behalf of the Overall Coordinators and the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the 
events set out in the section headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong 
Public Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) 
on the Listing Date (which is currently expected to be on Friday, March 20, 2026).

<<<PAGE 2>>>
– 2 –
Delton Technology (Guangzhou) Inc.
廣州廣合科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
46,000,000 H Shares
Number of Hong Kong Offer Shares
:
4,600,000 H Shares
Number of International Offer Shares
:
41,400,000 H Shares
Final Offer Price
:
HK$71.88 per H Share, plus brokerage of 
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
1989
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators, 
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners
and Joint Lead Managers
(in alphabetical order)
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager

<<<PAGE 3>>>
– 3 –
DELTON TECHNOLOGY (GUANGZHOU) INC.
廣州廣合科技股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND 
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated March 12, 2026 (the “Prospectus”) 
issued by Delton Technology (Guangzhou) Inc. (the “Company”).
SUMMARY
Company information
Stock code
1989
Stock short name
DELTON
Dealings commencement date
March 20, 2026*
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$71.88
Maximum Offer Price
HK$71.88
Offer Shares and Share Capital
Number of Offer Shares
46,000,000
Final Number of Offer Shares in Hong Kong Public Offering
4,600,000
Final Number of Offer Shares in International Offering
41,400,000
Number of issued Shares upon Listing
472,446,482
Number of Offer Shares over-allocated (Note)
0
Note: There is no over-allotment option in the International Offering, and no stabilization activities will be carried 
out in relation to the Global Offering.

<<<PAGE 4>>>
– 4 –
Proceeds
Gross proceeds (Note)
HK$3,306.48 million
Less: Estimated listing expenses payable based on 
Final Offer Price
HK$(121.22) million
Net proceeds
HK$3,185.26 million
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
202,417
No. of successful applications
39,425
Subscription level
1,070.72 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong 
Public Offering
4,600,000
Number of Offer Shares reallocated from the International 
Offering
0
Final no. of Offer Shares under the Hong Kong Public Offering
4,600,000
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering
10.00%
Note: For details of the final allocation of H Shares to the Public Offer, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by identification number or www.hkeipo.hk/IPOResult for 
the full list of allottees.

<<<PAGE 5>>>
– 5 –
INTERNATIONAL OFFERING
No. of placees
162
Subscription Level
14.64 times
No. of Offer Shares initially available under the International 
Offering
41,400,000
Number of Offer Shares reallocated to the Hong Kong Public 
Offering
0
Final no. of Offer Shares under the International Offering
41,400,000
% of Offer Shares under the International Offering to 
the Global Offering
90.00%
The Directors confirm that, to the best of their knowledge, information and belief, save for 
(a) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by 
the Stock Exchange to permit the Company to allocate certain Offer Shares in the International 
Offering to certain Existing Minority Shareholders and/or their close associates, (b) a consent 
under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the 
Company to, among other things, allocate further H Shares in the International Offering to an 
existing Shareholder and/or its close associates and a Cornerstone Investor and/or its close 
associates, and (c) a consent under paragraph 1C(1) of the Placing Guidelines to permit the 
Company to allocate certain Offer Shares in the International Offering to connected clients, (i) 
none of the Offer Shares subscribed by the placees and the public have been financed directly 
or indirectly by the Company, any of the Directors, chief executive of the Company, Controlling 
Shareholders, substantial Shareholders, existing Shareholders of the Company or any of its 
subsidiaries or their respective close associates; and (ii) none of the placees and the public 
who have purchased the Offer Shares are accustomed to taking instructions from the Company, 
any of the Directors, chief executive of the Company, Controlling Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their 
respective close associates in relation to the acquisition, disposal, voting or other disposition 
of H Shares registered in his/her/its name or otherwise held by him/her/it.

<<<PAGE 6>>>
– 6 –
The placees in the International Offering include the following:
Cornerstone Investors
Cornerstone Investors
No. of 
Offer Shares 
allocatedNote 1
% of 
Offer Shares
% of total 
issued share 
capital after 
the Global 
OfferingNote 3
Existing 
shareholders 
or their close 
associates
 
 
 
 
 
China Pinnacle Equity Management Limited 
(“CPE”)
1,730,100
3.76%
0.37%
No
Yuanfeng Asset Management and GTINV 
(in connection with the Yuanfeng OTC Swaps)
1,534,300
3.34%
0.32%
No
Shanghai Greenwoods and CITIC Securities 
International Capital Management Limited 
(in connection with CITICS Back-to-back TRS 
and CITICS Client TRS)
89,200
0.19%
0.02%
Yes Note 2
Greenwoods Asset Management Hong Kong 
Limited (“HK Greenwoods”)
3,175,200
6.90%
0.67%
No
UBS Asset Management (Singapore) Ltd. 
(“UBS AM Singapore”)
3,264,500
7.10%
0.69%
Yes Note 2
Value Partners Hong Kong Limited and Value 
Partners Limited (“Value Partners”)
3,264,500
7.10%
0.69%
No
Eastspring Investments (Singapore) Limited 
(“Eastspring”)
1,632,200
3.55%
0.35%
No
Greater Bay Area Development Fund Management 
Limited (“GBAHIL”)
1,632,100
3.55%
0.35%
No
MY Asian Opportunities Master Fund, L.P. 
(“MY Asian”)
1,088,100
2.37%
0.23%
No
Baring Asset Management (Asia) Limited 
(“Barings”)
1,088,100
2.37%
0.23%
No
Dajia Life Insurance Co., Ltd. (“Dajia Life”)
1,088,100
2.37%
0.23%
Yes Note 2
ICBC Wealth Management Co., Ltd. 
(“ICBC Wealth”)
1,088,100
2.37%
0.23%
No
 
 
 
Total
20,674,500Note 5
44.94%
4.38%
 
 
 

<<<PAGE 7>>>
– 7 –
Notes:
(1) 
The number of Offer Shares allocated to such investors only represents the number of Offer Shares allocated 
to the investors as cornerstone investors in the International Offering. For allocations of Offer Shares to 
the relevant investors as placees (if any), please refer to the section headed “Allotment Results Details – 
International Offering – Allotees with Waiver/Consents obtained” in this announcement.
(2) 
For details of a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of the Placing Guidelines granted by the Stock Exchange to permit the Company to allocate 
certain Offer Shares in the International Offering to certain Existing Minority Shareholders and/or their 
close associates as cornerstone investor, please refer to the section headed “Others/Additional Information” 
in this announcement.
(3) 
Not taking into account any A Shares held by the relevant investors.
(4) 
In addition to the Offer Shares subscribed for as Cornerstone Investors, CPE,  Yuanfeng Asset Management 
and GTINV (in connection with the Yuanfeng OTC Swaps), Shanghai Greenwoods and CITIC Securities 
International Capital Management Limited (in connection with CITICS Back-to-back TRS and CITICS 
Client TRS), HK Greenwoods, UBS AM Singapore, GBAHIL, MY Asian, Barings, Dajia Life and ICBC 
Wealth, and/or their close associates, were allocated further Offer Shares as placees in the International 
Offering. Please refer to the section headed “Allotment Results Details – International Offering – Allottees 
with Waivers/Consents Obtained” in this announcement for details. Only the Offer Shares subscribed for 
as Cornerstone Investors are subject to lock-up as indicated below. For details, please refer to the section 
headed “Lock-up Undertakings – Cornerstone Investors” in this announcement.
(5) 
The aggregate number of Offer Shares allocated to Cornerstone Investors is 300 less than that set out in the 
Prospectus due to rounding adjustments during the placing allocation for certain Cornerstone Investors.

<<<PAGE 8>>>
– 8 –
Allotees with Waivers/Consents Obtained
Investor
No. of 
Offer Shares 
allocated
% of 
Offer Shares
% of total 
issued share 
capital after 
the Global 
OfferingNote 1, 3
Relationship
 
 
 
 
 
Allotees with waiver from strict compliance with the requirements under Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by Existing Minority Shareholders 
holding 1% or more of the issued share capital of the Company immediately prior to the completion of the Global Offering 
and/or their close associates Note 1,3
E Fund Management Co., Ltd. 
(“E Fund”)
91,500
0.199%
0.019%
E Fund also manages other 
fund products, each 
holding less than 1% of 
the issued share capital but 
in aggregate holding more 
than 1% of the issued share 
capital of the Company.
E Fund Management (Hong Kong) 
Co., Ltd. (“E Fund HK”)
6,400
0.014%
0.001%
E Fund HK is wholly 
owned by E Fund, which 
also manages other fund 
products, each holding less 
than 1% of the issued share 
capital but in aggregate 
holding more than 1% of 
the issued share capital of 
the Company.

<<<PAGE 9>>>
– 9 –
Investor
No. of 
Offer Shares 
allocated
% of 
Offer Shares
% of total 
issued share 
capital after 
the Global 
OfferingNote 1, 3
Relationship
 
 
 
 
 
Allotees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations 
of further H Shares to certain Cornerstone Investors and/or their close associates Note 1
CSIWM – CPE Growth Fund #1
234,100
0.509%
0.050%
A close associate of 
a Cornerstone Investor, 
being CPE Note 2
Guotai Junan Investments 
(Hong Kong) Limited 
– Yuanfeng Wenjian Fund
310,100
0.674%
0.066%
A close associate of 
a Cornerstone Investor, 
being Yuanfeng Asset 
Management Note 2
Greenwood Entities
– Shanghai Greenwoods and 
CITIC Securities International 
Capital Management Limited (in 
connection with CITICS Back-to-
back TRS and CITICS Client TRS)
156,600
0.340%
0.033%
A Cornerstone Investor Note 2
– Greenwoods Asset Management 
Hong Kong Limited
387,600
0.843%
0.082%
A Cornerstone Investor Note 2
 
 
 
Subtotal
544,200
1.183%
0.115%
UBS AM Singapore
544,100
1.183%
0.115%
A Cornerstone Investor Note 2
Mega Prime Development Limited 
– Ruby24 and Poly Platinum 
Enterprises Limited 
272,100
0.592%
0.058%
A close associate of 
a Cornerstone Investor, 
being GBAHIL Note 2
MY Asian
181,300
0.394%
0.038%
A Cornerstone Investor Note 2
Barings
181,300
0.394%
0.038%
A Cornerstone Investor Note 2
Dajia Life
181,300
0.394%
0.038%
A Cornerstone Investor Note 2
ICBC Wealth
192,100
0.418%
0.041%
A Cornerstone Investor Note 2

<<<PAGE 10>>>
– 10 –
Investor
No. of 
Offer Shares 
allocated
% of 
Offer Shares
% of total 
issued share 
capital after 
the Global 
OfferingNote 1, 3
Relationship
 
 
 
 
 
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations to connected clients Note 1
CITIC Securities Asset Management 
Company Limited (“CITIC Asset 
Management”)
10,800
0.023%
0.002%
Connected client investing 
as a placee 
CITIC Securities Asset management 
(HK) Limited (“CITIC Asset 
Management HK”)
49,000
0.107%
0.010%
Connected client investing 
as a placee 
China Asset Management (Hong 
Kong) Limited (“China AMC HK”)
49,000
0.107%
0.010%
Connected client investing 
as a placee 
E Fund
91,500
0.199%
0.019%
Connected client investing 
as a placee 
E Fund HK
6,400
0.014%
0.001%
Connected client investing 
as a placee 
GF International Investment 
Management Limited (“GF 
International”)
97,900
0.213%
0.021%
Connected client investing 
as a placee 
CITIC Securities International Capital 
Management Limited (“CSI”)
675,800
1.469%
0.143%
Connected client investing 
as a cornerstone investor 
and a placee
GF Global Capital Limited (“GFGC”)
168,900
0.367%
0.036%
Connected client investing 
as a placee 
Huatai Capital Investment Limited 
(“HTCI”)
217,600
0.473%
0.046%
Connected client investing 
as a placee 
GF Securities Asset Management 
(Guangdong) Co., Ltd. 
(“GF Securities AM”)
345,800
0.752%
0.073%
Connected client investing 
as an asset manager of 
a cornerstone investor 
(being ICBC Wealth) and a 
placee 
Value Partners 
3,264,500
7.097%
0.691%
Connected client investing 
as a cornerstone investor

<<<PAGE 11>>>
– 11 –
Notes:
(1) 
For details of (a) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent 
under paragraph 1C(2) of the Placing Guidelines granted by the Stock Exchange to permit the Company to 
allocate certain Offer Shares in the International Offering to Existing Minority Shareholders and their close 
associates as cornerstone investor; (b) a consent under paragraph 18 of Chapter 4.15 of the Guide for New 
Listing Applicants to permit the Company to allocate certain Offer Shares in the International Offering to 
certain Cornerstone Investors and/or their close associates; and (c) a consent under paragraph 1C(1) of the 
Placing Guidelines to permit the Company to allocate certain Offer Shares in the International Offering to 
connected clients and details of ultimate clients adopting TRS arrangements, please refer to the sub-section 
relating to section headed “Others/Additional Information” in this announcement.
(2) 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations 
of Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed 
“Allotment Results Details – International Offering – Cornerstone Investors” in this announcement.
(3) 
Among the Cornerstone Investors, Dajia Life, CSICM and UBSAM Singapore are either Existing Minority 
Shareholders of the Company or their close associates. Among the other allotees, E Fund and E Fund HK 
are either Existing Minority Shareholders of the Company or their close associates. The Stock Exchange has 
granted a waiver from strict compliance with the requirements under Rule 10.04 of the Listing Rules and 
consent under Paragraph 1C(2) of the Placing Guidelines to permit H Shares in the International Offering 
to be placed to certain Existing Minority Shareholders and/or their close associates. Please refer to the 
section headed “Waivers from Strict Compliance with the Listing Rules – Allocation of H Shares to Existing 
Minority Shareholders and Their Close Associates” of the Prospectus for details.

<<<PAGE 12>>>
– 12 –
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
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued 
H Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon 
ListingNote 1
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon 
ListingNote 1
Last day subject to the lock-up 
undertakings Note 2
 
 
 
 
 
 
Guangzhou Zhenyun Investment Co., Ltd. 
(“Zhenyun Investment”)Note 4
171,142,853
0
0.00%
36.22%
September 19, 2026 
(First Sixth-Month Period)Note 1
March 19, 2027 
(Second Sixth-Month Period)Note 2
Shenzhen Guangcai Investment 
Partnership (Limited Partnership) 
(“Guangcai Investment”)Note 4
28,832,734
0
0.00%
6.10%
September 19, 2026 
(First Sixth-Month Period)Note 1
March 19, 2027 
(Second Sixth- Month Period)Note 2
Shenzhen Guangsheng Investment 
Partnership (Limited Partnership) 
(“Guangsheng Investment”) Note 4
28,832,734
0
0.00%
6.10%
September 19, 2026 
(First Sixth-Month Period)Note 1
March 19, 2027 
(Second Sixth-Month Period)Note 2
Notes:
(1) 
The Controlling Shareholders may dispose of or transfer H shares after the indicated date subject to that the 
Controlling Shareholders will not cease to be the Controlling Shareholders.
(2) 
The Controlling Shareholders will cease to be prohibited from disposing of or transferring H Shares after the 
indicated date.
(3) 
In accordance with the relevant Listing Rule/guidance materials, the required lock-up for the first six-month 
period ends on September 19, 2026, and for the second six-month period, on March 19, 2027.

<<<PAGE 13>>>
– 13 –
(4) 
For illustrative purposes only, this subsection lists only those members of the Controlling Shareholders 
who hold Shares directly in the Company. Immediately upon the completion of the Global Offering, the 
Company will be held as to (i) approximately 36.22% by Zhenyun Investment, which is owned as to 
99.90% by Mr. Xiao (the spouse of Ms. Liu) and 0.10% by Ms. Liu (the spouse of Mr. Xiao), respectively; 
(ii) approximately 6.10% by Guangsheng Investment, which is controlled by Mr. Xiao by virtue of his 
position as the sole general partner thereof; and (iii) approximately 6.10% by Guangcai Investment, which 
is controlled by Mr. Xiao by virtue of his position as the sole general partner thereof, respectively. Upon 
Listing, each of Mr. Xiao, Ms. Liu, Zhenyun Investment, Guangsheng Investment and Guangcai Investment 
will constitute a group of the Controlling Shareholders and each of them is subject to the same lock-up as 
disclosed above.
Cornerstone Investors
Name Note 1
Number of 
Shares held 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of 
H Shares held 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued 
H Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding 
in Company 
subject to 
lock-up 
undertakings 
upon Listing
Last day subject to the lock-up 
undertakings Note 2
 
 
 
 
 
 
CPE
1,730,100
1,730,100
3.76%
0.37%
September 19, 2026
Yuanfeng Asset Management and 
GTINV(in connection with the 
Yuanfeng OTC Swaps)
1,534,300
1,534,300
3.34%
0.32%
September 19, 2026
Greenwood Entities
– Shanghai Greenwoods and CSI (in 
connection with CITICS Back-to-
back TRS and CITICS Client TRS)
89,200
89,200
0.19%
0.02%
September 19, 2026
– HK Greenwoods
3,175,200
3,175,200
6.90%
0.67%
September 19, 2026
 
 
 
 
Sub-total
3,264,400
3,264,400
7.09%
0.69%
/
 
 
 
 
UBS AM Singapore
3,264,500
3,264,500
7.10%
0.69%
September 19, 2026
Value Partners
3,264,500
3,264,500
7.10%
0.69%
September 19, 2026
Eastspring
1,632,200
1,632,200
3.55%
0.35%
September 19, 2026
GBAHIL
1,632,100
1,632,100
3.55%
0.35%
September 19, 2026
MY Asian
1,088,100
1,088,100
2.37%
0.23%
September 19, 2026
Barings
1,088,100
1,088,100
2.37%
0.23%
September 19, 2026
Dajia Life
1,088,100
1,088,100
2.37%
0.23%
September 19, 2026
ICBC Wealth
1,088,100
1,088,100
2.37%
0.23%
September 19, 2026
 
 
 
 
Sub-total
20,674,500
20,674,500
44.94%
4.38%
 
 
 
 

<<<PAGE 14>>>
– 14 –
Notes:
(1) 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” 
in the Prospectus.
(2) 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on September 
19, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or transferring H Shares 
subscribed for pursuant to the relevant cornerstone investment agreements after the indicated date.
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering
Allotment 
as % of 
total Offer 
Shares
Number 
of H Shares 
held upon 
Listing
% of total 
issued share 
capital upon 
Listing
 
 
 
 
 
 
Top 1
3,808,600
9.20%
8.28%
3,808,600
0.81%
Top 5
15,212,500
36.75%
33.07%
15,212,500
3.22%
Top 10
24,407,300
58.95%
53.06%
24,407,300
5.17%
Top 25
33,902,200
81.89%
73.70%
33,902,200
7.18%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering
Allotment 
as % of 
total Offer 
Shares
Number 
of H Shares 
held upon 
Listing
% of total 
issued 
H Shares 
capital upon 
Listing
Number of 
Shares 
held upon 
Listing
 
 
 
 
 
 
 
Top 1
3,808,600
9.20%
8.28%
3,808,600
8.28%
4,149,301
Top 5
15,212,500
36.75%
33.07%
15,212,500
33.07%
15,553,201
Top 10
24,407,300
58.95%
53.06%
24,407,300
53.06%
24,748,001
Top 25
33,902,200
81.89%
73.70%
33,902,200
73.70%
34,324,301
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 15>>>
– 15 –
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering
Allotment 
as % of 
total Offer 
Shares
Number of 
H Shares 
held upon 
Listing
Number of 
Shares held 
upon Listing
% of 
total issued 
share capital 
upon Listing
 
 
 
 
 
 
 
Top 1
0
0.00%
0.00%
0
228,808,321
48.43%
Top 5
0
0.00%
0.00%
0
308,360,040
65.27%
Top 10
10,881,700
26.28%
23.66%
10,881,700
330,977,203
70.06%
Top 25
26,956,900
65.11%
58.60%
26,956,900
359,782,597
76.15%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon 
Listing.
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made 
by the public will be conditionally allocated on the basis set out below:
NO. OF SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT POOL A
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
 
 
 
 
100
69,175
3,459 out of 69,175 applicants to receive 100 shares
5.00%
200
12,543
797 out of 12,543 applicants to receive 100 shares
3.18%
300
6,634
485 out of 6,634 applicants to receive 100 shares
2.44%
400
3,057
247 out of 3,057 applicants to receive 100 shares
2.02%
500
4,377
382 out of 4,377 applicants to receive 100 shares
1.75%
600
12,684
1,178 out of 12,684 applicants to receive 100 shares
1.55%
700
1,845
181 out of 1,845 applicants to receive 100 shares
1.40%
800
1,647
169 out of 1,647 applicants to receive 100 shares
1.28%

<<<PAGE 16>>>
– 16 –
NO. OF SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT POOL A
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
 
 
 
 
900
1,082
116 out of 1,082 applicants to receive 100 shares
1.19%
1,000
9,302
1,031 out of 9,302 applicants to receive 100 shares
1.11%
1,500
4,075
520 out of 4,075 applicants to receive 100 shares
0.85%
2,000
3,724
525 out of 3,724 applicants to receive 100 shares
0.70%
2,500
2,603
396 out of 2,603 applicants to receive 100 shares
0.61%
3,000
2,770
449 out of 2,770 applicants to receive 100 shares
0.54%
3,500
1,658
284 out of 1,658 applicants to receive 100 shares
0.49%
4,000
1,862
333 out of 1,862 applicants to receive 100 shares
0.45%
4,500
1,285
240 out of 1,285 applicants to receive 100 shares
0.42%
5,000
2,870
555 out of 2,870 applicants to receive 100 shares
0.39%
6,000
2,297
473 out of 2,297 applicants to receive 100 shares
0.34%
7,000
1,971
428 out of 1,971 applicants to receive 100 shares
0.31%
8,000
1,750
398 out of 1,750 applicants to receive 100 shares
0.28%
9,000
1,413
335 out of 1,413 applicants to receive 100 shares
0.26%
10,000
9,432
2,315 out of 9,432 applicants to receive 100 shares
0.25%
20,000
5,928
1,849 out of 5,928 applicants to receive 100 shares
0.16%
30,000
4,183
1,501 out of 4,183 applicants to receive 100 shares
0.12%
40,000
2,868
1,136 out of 2,868 applicants to receive 100 shares
0.10%
50,000
2,523
1,080 out of 2,523 applicants to receive 100 shares
0.09%
60,000
4,692
2,138 out of 4,692 applicants to receive 100 shares
0.08%
 
180,250
Total number of Pool A successful applicants: 23,000
 

<<<PAGE 17>>>
– 17 –
NO. OF SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT POOL B
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
 
 
 
 
70,000
6,430
3,601 out of 6,430 applicants to receive 100 shares
0.08%
80,000
2,108
1,307 out of 2,108 applicants to receive 100 shares
0.08%
90,000
1,685
1,143 out of 1,685 applicants to receive 100 shares
0.08%
100,000
5,916
4,346 out of 5,916 applicants to receive 100 shares
0.07%
200,000
2,593
100 shares plus 634 out of 2,593 applicants to receive 
an additional 100 shares
0.06%
300,000
1,337
100 shares plus 928 out of 1,337 applicants to receive 
an additional 100 shares
0.06%
400,000
577
200 shares plus 63 out of 577 applicants to receive an additional 
100 shares
0.05%
500,000
450
200 shares plus 225 out of 450 applicants to receive 
an additional 100 shares
0.05%
600,000
238
200 shares plus 208 out of 238 applicants to receive 
an additional 100 shares
0.05%
700,000
146
300 shares plus 34 out of 146 applicants to receive an additional 
100 shares
0.05%
800,000
105
300 shares plus 61 out of 105 applicants to receive an additional 
100 shares
0.04%
900,000
68
300 shares plus 62 out of 68 applicants to receive an additional 
100 shares
0.04%
1,000,000
226
400 shares plus 53 out of 226 applicants to receive an additional 
100 shares
0.04%
1,500,000
114
500 shares plus 87 out of 114 applicants to receive an additional 
100 shares
0.04%
2,000,000
39
700 shares plus 7 out of 39 applicants to receive an additional 
100 shares
0.04%
2,300,000
135
700 shares plus 132 out of 135 applicants to receive 
an additional 100 shares
0.03%
 
22,167
Total number of Pool B successful applicants: 16,425
 
As of the date of this announcement, the relevant subscription monies previously deposited 
in the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers for any inquiries.

<<<PAGE 18>>>
– 18 –
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect 
of which consent has been obtained, the Company has complied with the Listing Rules and 
guidance materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or 
indirectly, provided by the Company, its Controlling Shareholders, Directors or syndicate 
members to any placees or the public (as the case may be) and the consideration payable 
by them for each Share of the Company subscribed for or purchased by them is the same 
as the final Offer Price determined by agreement between the Company and the Sponsor-
Overall Coordinators (for themselves and on behalf of other Overall Coordinators and the 
Underwriters), in addition to any brokerage, AFRC transaction levy, SFC transaction levy and 
trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Allocation of H Shares to Existing Minority Shareholders and their close associates with a 
waiver from the strict compliance with Rule 10.04 of the Listing Rules and a prior consent 
under paragraph 1C(2) of the Placing Guidelines
As disclosed in the Prospectus, the Company has applied to the Stock Exchange, and the Stock 
Exchange has granted, a waiver from the strict compliance with Rule 10.04 of the Listing 
Rules and a consent under paragraph 1C(2) of the Placing Guidelines to permit the Company to 
allocate such Offer Shares certain Existing Minority Shareholders and their close associates on 
the following conditions:
(i) 
the Joint Sponsors shall confirm to the Stock Exchange in writing that:
(a) 
each Existing Minority Shareholder to whom our Company may allocate the H 
Shares in the International Offering holds less than 5% of our Company’s voting 
rights prior to the completion of the Global Offering;
(b) 
each Existing Minority Shareholder is not, and will not be, a core connected 
person of our Company or any close associate of any such core connected person 
immediately prior to or following the Global Offering;
(c) 
none of the Existing Minority Shareholders has the right to appoint any Directors 
and/or any other special rights;

<<<PAGE 19>>>
– 19 –
(d) 
allocation to the Existing Minority Shareholders and/or their close associates will 
not affect our Company’s ability to satisfy the public float requirement as prescribed 
under Rule 19A.13A(2) of the Listing Rules, and details of the allocation to the 
Existing Minority Shareholders holding 1% or more of the issued share capital of 
our Company immediately prior to the completion of the Global Offering will be 
disclosed in this Prospectus and/or the allotment results announcement, as the case 
may be;
(e) 
to the best of their knowledge and belief, they have no reason to believe that any of 
the Existing Minority Shareholders received any preferential treatment, or is in a 
position to exert influence on our Company to obtain actual or perceived preferential 
treatment in the allocation either as a cornerstone investor or as a placee by virtue 
of their relationship with our Company other than the preferential treatment of 
assured entitlement under a cornerstone investment following the principles set out 
in Chapter 4.15 of the Guide for New Listing Applicants;
(ii) our Company shall confirm to the Stock Exchange in writing that:
(a) 
in the case of participation as cornerstone investors, no preferential treatment 
has been, nor will be, given to the Existing Minority Shareholders or their close 
associates by virtue of their relationship with our Company, other than the 
preferential treatment of assured entitlement under a cornerstone investment 
following the principles set out in Chapter 4.15 of the Guide for New Listing 
Applicants, nor is the Existing Minority Shareholder in a position to exert influence 
on our Company to obtain actual or perceived preferential treatment, and the 
Existing Minority Shareholders or their close associates’ cornerstone investment 
agreements do not contain any material terms which are more favorable to the 
Existing Minority Shareholders or their close associates than those in other 
cornerstone investment agreements; or
(b) 
in the case of participation as placees, no preferential treatment has been, nor will 
be, given to the Existing Minority Shareholders or their close associates, nor is the 
Existing Minority Shareholder in a position to exert influence on our Company to 
obtain actual or perceived preferential treatment, by virtue of their relationship with 
our Company in any allocation in the placing tranche; and

<<<PAGE 20>>>
– 20 –
(iii) in the case of participation as placees, the Overall Coordinators will confirm to the Stock 
Exchange that, to the best of their knowledge and belief, no preferential treatment has 
been, nor will be, given to the Existing Minority Shareholders or their close associates by 
virtue of their relationship with our Company in any allocation in the placing tranche.
Please refer to the section headed “Waivers from Strict Compliance with the Listing Rules 
– Allocation of H Shares to Existing Minority Shareholders and Their Close Associates” in 
the Prospectus for further details of the waiver and consent. The allocation of Offer Shares to 
such Existing Minority Shareholders is in compliance with all the conditions under the waiver/
consent granted by the Stock Exchange.
Allocations of Offer Shares to certain Cornerstone Investors and/or their close associates 
with a consent under paragraph 18 of Chapter 4.15 of the Guide
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 
of the Guide for New Listing Applicants to permit the Company to allocate further Offer Shares 
in the International Offering to certain Cornerstone Investors and/or their close associates as 
placees, subject to the following conditions (the “Size-based Exemption”):
(a) 
the final offering size of the Global Offering will be of a total value of at least HK$1 
billion;
(b) 
the Offer Shares allocated to all existing Shareholders and their close associates as 
permitted under the Size-based Exemption do not exceed 30% of the total number of the 
Shares offered under the Global Offering;
(c) 
each Director, chief executive and Controlling Shareholder of the Company confirms that 
no Offer Shares have been allocated to them or their respective close associates under the 
Size-based Exemption;
(d) 
the allocation to certain Cornerstone Investors and/or their close associates will not affect 
the Company’s ability to satisfy the public float requirement under Rule 19A.13A(2)) of 
the Listing Rules; and
(e) 
details of the allocation to the Cornerstone Investors and/or their close associates under 
the Size-based Exemption will be disclosed in this announcement.

<<<PAGE 21>>>
– 21 –
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to existing Shareholders and/or their close 
associates and Cornerstone Investors, please refer to the section headed “Allotment Results 
Details – International Offering – Allotees with Waivers/Consents Obtained” in this 
announcement.
Placing to connected clients with a consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, 
consent under paragraph 1C(1) of the Placing Guidelines to permit each of CSICM, VPHKL, 
VPL and ICBC Wealth to participate in the Global Offering as connected client to participate 
in the Global Offering as a Cornerstone Investor. For details of the consent granted, please 
refer to the section headed “Allotment Results Details – International Offering – Cornerstone 
Investors” in this announcement.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit each of CSI, GFGC, HTCI, 
GF Securities AM, CITIC Asset Management, CITIC Asset Management HK, China AMC 
HK, E Fund, E Fund HK and GF International (the “Connected Clients”) to participate in 
the Global Offering as connected client to participate in the Global Offering as a placee. The 
allocation of Offer Shares to such connected clients is in compliance with all the conditions 
under the consent granted by the Stock Exchange, including the following:
The Overall Coordinators shall confirm to the Stock Exchange in writing that:
(i) 
Based solely on the information and confirmation provided by the Connected Clients, the 
Shares to be allocated to the Connected Clients will be held by the Connected Clients on 
behalf of independent third parties upon completion of the Global Offering as placee, and 
details of the allocation to the Connected Clients are disclosed in the allotment results 
announcement of the Company;

<<<PAGE 22>>>
– 22 –
(ii) Based on the confirmation provided by CSI, to the best knowledge of CSI after making 
all reasonable enquiries, CSI Ultimate Clients is an independent third party of CSI, CLSA 
and the companies which are members of the same group of CLSA and the identities of the 
ultimate beneficial owners have been disclosed in the Consent Application;
(iii) Based on the confirmation provided by GFGC, to the best knowledge of GFGC after 
making all reasonable enquiries, GFGC Ultimate Clients is an independent third party 
of GFGC, GF Securities and the companies which are members of the same group of GF 
Securities and the identities of the ultimate beneficial owners have been disclosed in the 
Consent Application;
(iv) Based on the confirmation provided by GF Securities AM, to the best knowledge of GF 
Securities AM after making all reasonable enquiries, GF Securities AM Ultimate Clients 
is an independent third party of GF Securities AM, GF Securities and the companies 
which are members of the same group of GF Securities and the identities of the ultimate 
beneficial owners have been disclosed in the Consent Application;
(v) 
Based on the confirmation provided by HTCI, to the best knowledge of HTCI after 
making all reasonable enquiries, HTCI Ultimate Clients is an independent third party 
of HTCI, Huatai and the companies which are members of the same group of Huatai 
and the identities of the ultimate beneficial owners have been disclosed in the Consent 
Application;
(vi) To the best of our knowledge and belief, we have no reason to believe that the Connected 
Clients have received or will receive any preferential treatment in the allocation of 
the Offer Shares in the International Offering by virtue of their relationship with the 
respective connected distributor;
(vii) the background and details of certain collective investments schemes not authorized by 
the SFC, which GF International is investing on behalf of, are disclosed in the allotment 
results announcement of the Company; and
(viii) The respective connected distributor has not participated, and will not participate, in 
the decision-making process or relevant discussions among the Company, the Overall 
Coordinators and the Underwriters as to allocation of the Offer Shares to CITIC Asset 
Management, CITIC Asset Management HK, China AMC HK, E Fund, E Fund HK and 
GF International.

<<<PAGE 23>>>
– 23 –
The Company shall confirm to the Stock Exchange in writing that:
(i) 
No preferential treatment has been, nor will be, given to the Connected Clients in any 
allocation of the Offer Shares in the International Offering by virtue of their relationship 
with the Connected Distributor; and
(ii) The respective Connected Distributor has not participated, and will not participate, in the 
decision-making process or relevant discussions relating to allocation of the Offer Shares 
to CITIC Asset Management, CITIC Asset Management HK, China AMC HK, E Fund, E 
Fund HK and GF International.
Each of the Connected Clients shall confirm to the Stock Exchange in writing that in relation to 
the Shares to be allocated to the Connected Clients, to the best of their knowledge and belief, 
they have not received and will not receive any preferential treatment in the allocation of the 
Offer Shares in the International Offering by virtue of their relationship with the respective 
Connected Distributor.
In respect of Connected Clients holding the beneficial interest of the Offer Shares on a 
discretionary basis as disclosed below, the respective Connected Distributors shall confirm to 
the Stock Exchange in writing that:
(i) 
To the best of their knowledge and belief, no preferential treatment has been, nor will be, 
given to the Connected Clients in any allocation of the Offer Shares in the International 
Offering by virtue of their relationship with the Connected Distributor; and
(ii) The Connected Distributors have not participated, and will not participate, in the 
decision-making process or relevant discussions among the Company, the Overall 
Coordinators and the Underwriters as to whether the Offer Shares should be allocated to 
its respective Connected Clients.
In respect of Connected Clients holding the beneficial interest of the Offer Shares on a non-
discretionary basis as disclosed below, the respective Connected Distributors shall confirm to 
the Stock Exchange in writing that to the best of their knowledge and belief, no preferential 
treatment has been, nor will be, given to the Connected Clients in any allocation of the 
Offer Shares in the International Offering by virtue of their relationship with the respective 
Connected Distributor.

<<<PAGE 24>>>
– 24 –
Details of the placement to connected clients are set out below:
No.
Connected Distributor
Connected Client
Relationship
Identities of 
the ultimate 
beneficial 
owners of the 
Offer Shares 
or, where 
applicable, 
details of 
the structured 
products under 
which the 
subscription by 
the Connected 
Client was 
made (e.g. OTC 
total return 
swaps)
Whether the 
Connected 
Client is a
 collective 
investment 
scheme 
which is not 
authorised by 
the SFC or 
is expected to 
hold the Offer 
Shares on 
behalf of 
such scheme
Maximum 
amount 
of Offer 
Shares to 
be allocated 
to the 
Connected 
Client
Approximate 
percentage of 
total number 
of Offer 
Shares under 
the Global 
Offering
Approximate 
percentage of 
total issued 
share capital 
after the 
Global 
Offering
 
 
 
 
 
 
 
 
 
Part A – Connected Clients holding the beneficial interest of the Offer Shares on a non-discretionary basis on behalf of independent third parties
1.
CLSA Limited (“CLSA”)
CSI
CSI is a member of the 
same group of CLSA.
Please refer to 
Note (1) below.
No
586,600
1.275%
0.124%
2.
GF Securities (Hong Kong) 
Brokerage Limited 
(“GF Securities”)
GFGC
GFGC is a member of 
the same group of GF 
Securities.
Please refer to 
Note (2) below.
No
168,900
0.367%
0.036%
3.
Huatai Financial Holdings 
(Hong Kong) Limited 
(“HTFH”)
HTCI
HTCI is a member of 
the same group of 
companies as HTFH.
Please refer to 
Note (3) below.
No
217,600
0.473%
0.046%
4.
GF Securities 
GF Securities AM
GF Securities AM is a 
member of the same 
group of companies as 
GF Securities.
Please refer to 
Note (4) below.
No
19,400
0.042%
0.004%

<<<PAGE 25>>>
– 25 –
No.
Connected Distributor
Connected Client
Relationship
Whether the 
Connected Client 
is a collective 
investment 
scheme which 
is not authorised 
by the SFC or 
is expected 
to hold the 
Offer Shares on 
behalf of 
such scheme
Maximum 
amount of 
Offer Shares 
to be allocated 
to the Connected 
Client
Approximate 
percentage of 
total number of 
Offer Shares 
under the 
Global Offering
Approximate 
percentage of 
total issued share 
capital after 
the Global 
Offering
 
 
 
 
 
 
 
 
Part B – Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties
1.
CLSA Limited
CITIC Asset 
ManagementNote 5
CITIC Asset Management is 
a member of the same 
group of companies as 
CLSA.
No
10,800
0.023%
0.002%
2.
CLSA Limited
CITIC Asset 
Management 
HKNote 6
CITIC Asset Management HK 
is a member of the same 
group of companies as 
CLSA.
No
49,000
0.107%
0.010%
3.
CLSA Limited
China AMC HKNote 7
China AMC HK is a member 
of the same group of 
companies as CLSA.
No
49,000
0.107%
0.010%
4.
GF Securities
E FundNote 8
E Fund is a member of the 
same group of companies 
as GF Securities.
No
91,500
0.199%
0.019%
5.
GF Securities
E Fund HKNote 9
E Fund HK is a member of the 
same group of companies 
as GF Securities.
No
6,400
0.014%
0.001%
6.
GF Securities
GF InternationalNote 10
GF International is a member 
of the same group 
of companies as GF 
Securities
Yes, 
GF International is
 investing on behalf 
of certain collective 
investment schemes. 
Please refer to note 
(1) for background 
and details of such 
schemes. Note 11
97,900
0.213%
0.021%
Notes:
(1) 
CSI proposes to subscribe for and hold the Offer Shares as a placee under the International Offering on 
behalf of the ultimate clients of CSI (“CSI Ultimate Clients”), on a non-discretionary basis, pursuant to 
which:

<<<PAGE 26>>>
– 26 –
(i) 
CSI will act as the single counterparty of a back-to-back total return swap transaction (the “CSI 
Back-to-back TRS”) to be entered into by it in connection with a total return swap order (the “CSI 
Client TRS”) placed and fully funded by the CSI Ultimate Client, including Canaan China Flagship 
Fund and and the investment managers (Hover4pi Capital Management, Shenzhen Jingcong Asset 
Management Ltd. ( 深圳市景從資產管理有限公司), Shanghai Greenwoods Asset Management 
Ltd. (上海景林資產管理有限公司), Tibet Longrising Asset Management Co., Ltd. (西藏源樂晟
資產管理有限公司), Shanghai Panjing Investment Management Center (Limited Partnership) (上
海盤京投資管理中心（有限合夥）), Shanghai Tongyi Investment Management Co., Ltd. (上海通
怡投資管理有限公司), Shanghai Gaoyi Asset Management Partnership (Limited Partnership) (上
海高毅資產管理合夥企業（有限合夥）)) who act for and on behalf of certain ultimate clients, by 
which CSI will pass the full economic exposure of the Offer Shares placed to CSI to the CSI Ultimate 
Client.
(ii) 
As confirmed by CSI and CLSA, CSI will hold the legal title and beneficial interest in the Offer 
Shares, but will contractually agree to pass on the full economic exposure and return of the Offer 
Shares to the CSI Ultimate Client, on a non-discretionary basis. The CSI Ultimate Client may 
exercise their early termination rights to terminate the CSI Client TRS at any time from the trade date 
of the CSI Client TRS which should be on or after the date on which the Offer Shares are listed on 
the Stock Exchange.
(iii) 
Upon the final maturity or termination of the CSI Client TRS by the CSI Ultimate Client, CSI will 
dispose of the Offer Shares on the secondary market and the CSI Ultimate Client will receive a 
final termination amount of the CSI Back-to-back TRS which will have taken into account all the 
economic returns or economic loss in relation to the Offer Shares and the fixed amount of transaction 
fees of the CSI Back- to-back TRS and the CSI Client TRS. Due to its internal policy, CSI will not 
exercise the voting right of the Offer Shares during the terms of the CSI Back-to-back TRS.
(iv) 
CSI is not a collective investment schemes which is not authorized by the SFC, nor is expected to 
hold the Offer Shares on behalf of such scheme.
(v) 
To the best knowledge of CSI after making all reasonable enquiries, each of the investment managers 
and their ultimate beneficial owner is independent from each of the Company, its subsidiaries, 
substantial shareholders, CSI, CLSA and the companies which are members of the same group of 
CLSA.

<<<PAGE 27>>>
– 27 –
The details of the CSI Ultimate Client are as follows:
Investment Manager
UBOs holding 30% 
or more interest 
in Investment 
Manager
Name of CSI Ultimate ClientsNote
UBOs holding 
30% or more 
interest in CSI 
Ultimate Clients
Not applicable
Not applicable
Canaan China Flagship Fund
LIANG Hao
Hover4pi Capital Management
HE Hui
Hover4pi Fund I OFC
None
Shenzhen Jingcong Asset 
Management Ltd.
Zeng Huan (曾歡)
Jingcong Qingfeng 18th Private 
Securities Investment Fund 
(景從青鋒18號私募證券投資基金)
Fu Zhaoxia (付朝霞)
Shanghai Greenwoods Asset 
Management Co., Ltd.
Jiang Jinzhi (蔣錦志)
Jinglin Fengshou No. 3 Private Fund 
(景林豐收3號私募基金)
None
Shanghai Greenwoods Asset 
Management Co., Ltd.
Jiang Jinzhi (蔣錦志)
Jinglin Fengshou No. 6 Private Fund 
(景林豐收6號私募證券投資基金)
None
Shanghai Greenwoods Asset 
Management Co., Ltd.
Jiang Jinzhi (蔣錦志)
Jinglin Fengshou No. 7 Private Fund 
(景林豐收7號私募證券投資基金)
None
Shanghai Greenwoods Asset 
Management Co., Ltd.
Jiang Jinzhi (蔣錦志)
Jinglin Jingtai Fengshou Private 
Securities Investment Fund 
(景林景泰豐收私募證券投資基金)
None
Tibet Longrising Asset Management 
Co., Ltd.
Zeng Xiaojie
 (曾曉潔)
Longrising Qiangye Private Securities 
Investment Fund 
(源樂晟強業私募證券投資基金)
Hu Caiyang (胡彩陽)
Shanghai Panjing Investment 
Management Center (Limited 
Partnership)
Zhuang Tao (莊濤)
Panshi Private Securities Investment 
Fund (盤世私募證券投資基金)
None
Shanghai Panjing Investment 
Management Center (Limited 
Partnership)
Zhuang Tao (莊濤)
Panjing Xinghe No. 1 Private 
Securities Investment Fund 
(盤京興和1號私募證券投資基金)
Zhuang Tao (莊濤)
Shanghai Panjing Investment 
Management Center (Limited 
Partnership)
Zhuang Tao (莊濤)
Panjing Mingsheng Phase 1 Private 
Securities Investment Fund 
(盤京明晟1期私募證券投資基金)
Zhuang Tao (莊濤)
Shanghai Tongyi Investment 
Management Co., Ltd.
Chu Yibo (儲貽波)
Tongyi Anxin No. 2 Private Equity 
Securities Investment Fund 
(通怡安鑫2號私募證券投資基金)
Huang Shilin 
(黃世霖)
Shanghai Tongyi Investment 
Management Co., Ltd.
Chu Yibo (儲貽波)
Tongyi Taoli No. 10 Private Equity 
Securities Investment Fund 
(通怡桃李10號私募證券投資基金)
None

<<<PAGE 28>>>
– 28 –
Investment Manager
UBOs holding 30% 
or more interest 
in Investment 
Manager
Name of CSI Ultimate ClientsNote
UBOs holding 
30% or more 
interest in CSI 
Ultimate Clients
Shanghai Tongyi Investment 
Management Co., Ltd.
Chu Yibo (儲貽波)
Tongyi Taoli No. 1 Private Equity 
Securities Investment Fund 
(通怡桃李1號私募證券投資基金)
Wang Jing (王靜)
Shanghai Gaoyi Asset Management 
Partnership (Limited Partnership)
None
Golden Sun Gaoyi Guolu No. 1 
Chongyuan Fund (金太陽高毅國鷺
1號崇遠基金)
None
Shanghai Gaoyi Asset Management 
Partnership (Limited Partnership)
None
Gaoyi Ren Hao Youxuan Zhifu 
Private Securities Investment Fund 
(高毅任昊優選致福私募證券投資
基金)
None
Shanghai Gaoyi Asset Management 
Partnership (Limited Partnership)
None
Gaoyi Ren Hao Jingxuan Chengze 
Private Securities Investment Fund 
(高毅任昊精選承澤私募證券投資
基金)
None
Shanghai Gaoyi Asset Management 
Partnership (Limited Partnership)
None
Gaoyi Ren Hao Zhenxuan Chunhe 
Private Securities Investment Fund 
(高毅任昊臻選春和私募證券投資
基金)
None
Shanghai Gaoyi Asset Management 
Partnership (Limited Partnership)
None
Gaoyi Ren Hao Long-Term Value 
Langrun Private Securities 
Investment Fund (高毅任昊長期價
值朗潤私募證券投資基金)
None
Shanghai Gaoyi Asset Management 
Partnership (Limited Partnership)
None
Gaoyi Liwei Xinshi Private Fund 
(高毅利偉信實私募基金)
None
Shanghai Gaoyi Asset Management 
Partnership (Limited Partnership)
None
Gaoyi Liwei Jingxuan Weishi Fund 
(高毅利偉精選唯實基金)
None
Shanghai Gaoyi Asset Management 
Partnership (Limited Partnership)
None
Gaoyi Guolu Xinyuan Private 
Securities Investment Fund 
(高毅國鷺信遠私募證券投資基金)
None
Shanghai Gaoyi Asset Management 
Partnership (Limited Partnership)
None
Gaoyi Qingrui No. 6 Ruixing Fund 
(高毅慶瑞6號瑞行基金)
None

<<<PAGE 29>>>
– 29 –
Investment Manager
UBOs holding 30% 
or more interest 
in Investment 
Manager
Name of CSI Ultimate ClientsNote
UBOs holding 
30% or more 
interest in CSI 
Ultimate Clients
Shanghai Gaoyi Asset Management 
Partnership (Limited Partnership)
None
Gaoyi Qingrui Youxuan Ruize Private 
Securities Investment Fund (高毅慶
瑞優選瑞澤私募證券投資基金)
None
Shanghai Gaoyi Asset Management 
Partnership (Limited Partnership)
None
Gaoyi Qingrui Zhenxuan Fengyuan 
Private Securities Investment Fund 
(高毅慶瑞臻選灃源私募證券投資
基金)
None
Shanghai Gaoyi Asset Management 
Partnership (Limited Partnership)
None
Gaoyi – Xiaofeng No. 1 Ruiyuan 
Securities Investment Fund (高毅－
曉峰1號睿遠證券投資基金)
None
Shanghai Gaoyi Asset Management 
Partnership (Limited Partnership)
None
Gaoyi Xiaofeng No. 2 Zhixin Fund 
(高毅曉峰2號致信基金)
None
Note: The English names of the CSI Ultimate Clients are not their official names and they are listed for 
identification purpose only.
(2) 
GFGC proposes to subscribe for and hold the Offer Shares as a placee under the International Offering 
on a a non-discretionary basis. GFGC and GF Securities Co., Ltd. will enter into a series of cross border 
delta one OTC swap transactions (the “OTC Swaps”) with each other and the ultimate clients (the “GFGC 
Ultimate Clients”), pursuant to which GFGC will hold the Offer Shares on a non-discretionary basis to 
hedge the OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed to 
the GFGC Ultimate Clients being Jing Cong Qing Feng No.18 Private Securities Investment Fund (景從
青鋒18號私募證券投資基金), which is held as to 30% or more interest by Fu Zhaoxia (付朝霞), subject 
to customary fees and commissions. The OTC swaps will be fully funded by the GFGC Ultimate Clients. 
During the terms of the OTC Swaps, all economic returns of the Offer Shares subscribed by GFGC will be 
passed to the GFGC Ultimate Clients and all economic loss shall be borne by the GFGC Ultimate Clients 
through the OTC Swaps, and GFGC will not take part in any economic return or bear any economic loss 
in relation to the Offer Shares. The OTC Swaps are linked to the Offer Shares and the GFGC Ultimate 
Clients may request GFGC to redeem it at their own discretions, upon which GFGC shall dispose of the 
Offer Shares and settle OTC Swaps in cash in accordance with the terms and conditions of the OTC Swap. 
Despite that GFGC will hold the legal title of the Offer Shares by itself, it will not exercise the voting rights 
attaching to the relevant Offer Shares during the terms of the OTC Swaps according to its internal policy. 
GFGC is not a collective investment schemes which is not authorized by the SFC, nor is expected to hold 
the Offer Shares on behalf of such scheme.

<<<PAGE 30>>>
– 30 –
(3) 
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial 
public offerings (“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products 
issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading 
activities. In connection with such products, the licensed domestic securities firms, through their Hong 
Kong affiliates, may participate in Hong Kong IPOs either as placees or cornerstone investors (the “Cross-
border Derivatives Trading Regime”). Huatai Securities Co., Ltd. (“Huatai Securities”), the shares of 
which are listed on both the Shanghai Stock Exchange (stock code: 601688) and the Stock Exchange (stock 
code: 6886), is one of the domestic securities firms licensed to undertake cross-border derivatives trading 
activities. Huatai Securities entered into an ISDA agreement (the “ISDA Agreement”) with its indirectly 
wholly-owned subsidiary, HTCI, to set out the principal terms of any future total return swap between 
Huatai Securities and HTCI.
HTFH is one of the Overall Coordinators in connection with the Global Offering. Pursuant to the ISDA 
Agreement, HTCI, which intends to participate in the Global Offering as a placee, will hold the beneficial 
interest of Offer Shares on a non-discretionary basis as the single underlying holder under a back-to-back 
total return swap (the “Back-to-back TRS”) to be entered by HTCI in connection with a Client TRS (as 
defined below) placed by and fully funded (i.e. with no financing provided by HTCI) by the Huatai Ultimate 
Client (as defined below), by which, HTCI will, subject to customary fees and commissions, pass the full 
economic exposure of the Offer Shares ultimately to the Huatai Ultimate Client, which in effect, HTCI 
will hold the beneficial interest of the Offer Shares on behalf of the Huatai Ultimate Client. HTFH, being 
one of the Overall Coordinators in connection with the Global Offering, and HTCI are indirectly wholly-
owned subsidiaries of Huatai Securities. Accordingly, HTCI is considered as a “connected client” of HTFH 
pursuant to paragraph 13(7) of the Placing Guidelines.
Pursuant to the Cross-border Derivatives Trading Regime, Jiangxi Copper (Beijing) International 
Investment Co., Ltd. (the “Huatai Ultimate Client”) cannot directly subscribe for the Offer Shares but 
may invest in derivative products issued by domestic securities firms licenced to undertake cross-border 
derivatives trading activities, such as Huatai Securities, with the Offer Shares as the underlying assets. 
Instead of directly subscribing for the Offer Shares, the Huatai Ultimate Client will place a total return 
swap order (the “Client TRS”) with Huatai Securities in connection with the Company’s Global Offering 
and Huatai Securities will place a Back-to-back TRS order to HTCI on the terms of the ISDA Agreement. 
In order to hedge its exposure under the Back-to-back TRS, HTCI participates in the Company’s Global 
Offering and subscribes the Offer Shares through placing order with HTFH during the International 
Offering.
To the best of our knowledge and after making all reasonable enquiries, each of the Huatai Ultimate Client 
is an independent third party of the Company and their respective associates.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in connection 
with the Client TRS order placed by the Huatai Ultimate Client. Pursuant to the terms of the contracts of 
the Back-to-back TRS and the Client TRS, during the tenor of the Back-to-back TRS and the Client TRS, 
subject to customary fees and commissions, all economic returns of the Offer Shares will be ultimately 
passed to the Huatai Ultimate Client through the Back-to-back TRS and the Client TRS and all economic 
loss shall be ultimately borne by the Huatai Ultimate Client. HTCI will not take any economic return or bear 
any economic loss in relation to the Offer Shares.

<<<PAGE 31>>>
– 31 –
Investment in the Back-to-back TRS and the Client TRS is similar to the investment in a qualified domestic 
institutional investor fund (“QDII”) in the way that the Huatai Ultimate Client would reap all the economic 
benefits of the underlying Offer Shares, except that a QDII fund would pass through the exchange rate 
exposure on both the notional value of the investment and the profit and loss of the investment. In contrast, 
the profit and loss of the Back-to-back TRS and the Client TRS factor into account the fluctuation in 
RMB exchange rate upon termination of the Client TRS by converting the profit and loss using the current 
exchange rate at the time of termination. As such, the Huatai Ultimate Client would bear the exchange rate 
exposure of the profit and loss on settlement date.
The Huatai Ultimate Client may exercise an early termination right to terminate the Client TRS at any 
time from the issue date of the Client TRS which should be on or after the date on which the Offer 
Shares are listed on the Stock Exchange at their own discretion. Upon the termination upon maturity or 
early termination of the Client TRS by the Huatai Ultimate Client, HTCI will dispose the Offer Shares 
on the secondary market and the Huatai Ultimate Client will receive a final settlement amount in cash in 
accordance with the terms and conditions of the Back-to-back TRS and the Client TRS which should have 
taken into account all the economic returns or economic loss in relation to the Offer Shares. If upon the 
maturity of the Client TRS, the Huatai Ultimate Client intend to extend the investment period, subject to 
further agreement between Huatai Securities and the relevant Huatai Ultimate Client, the term of the Client 
TRS could be extended by way of a new issuance or a tenor extension. Accordingly, Huatai Securities will 
extend the term of the Back-to-back TRS by way of a new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass 
through the economic exposure to the Huatai Ultimate Client, each being an onshore client who places a 
Client TRS order with Huatai Securities in connection with the Global Offering of the Company. HTCI will 
not exercise the voting right of the Offer Shares during the tenor of the Back-to-back TRS.
During the life of the Client TRS and Back-to-back TRS, HTCI may continue to hold the Offer Shares in 
its custodian account, or to hold some or all of the Offer Shares in a prime brokerage account for stock 
borrowing purposes,where HTCI will lend out its holding of underlying Offer Shares in the form of stock 
borrowing loans consistent with market practice to lower its finance costs, provided that HTCI has the 
ability to call back the Offer Shares on loan at any time in order to satisfy its obligations under the Back-to-
back TRS to ensure the economic interests to are ultimately passed to the Huatai Ultimate Client.
HTCI is not a collective investment schemes which is not authorized by the SFC.
(4) 
The ultimate client of GF Securities AM (“GF Securities AM Ultimate Client”) has engaged GF Securities 
AM, an asset manager that is qualified domestic institutional investor as approved by the relevant PRC 
authority, in the name of CIB – GFAM WANXIANG NO.1 (廣發資管萬享1 號單一資產管理計劃
（QDII)), to subscribe for and hold the Offer Shares as a placee under the International Offering on behalf 
of the GF Securities AM Ultimate Client on a non-discretionary basis (the “GF Securities AM QDII 
Arrangement”).
(5) 
CITIC Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager 
managing the funds on behalf of its investors, each of which is, to the best knowledge of CITIC Asset 
Management, an independent third party of the Company, its subsidiaries, its substantial shareholders, 
CITIC Asset Management, CLSA and the companies which are members of the same group of CLSA.

<<<PAGE 32>>>
– 32 –
(6) 
CITIC Asset Management HK will hold the Offer Shares in its capacity as the discretionary fund manager 
managing the funds on behalf of its investors, each of which is, to the best knowledge of CITIC Asset 
Management HK, an independent third party of the Company, its subsidiaries, its substantial shareholders, 
CITIC Asset Management HK, CLSA and the companies which are members of the same group of CLSA.
(7) 
China AMC HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the 
funds on behalf of its investors, each of which is, to the best knowledge of China AMC HK, an independent 
third party of the Company, its subsidiaries, its substantial shareholders, China AMC HK, CLSA and the 
companies which are members of the same group of CLSA.
(8) 
E Fund will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on 
behalf of its investors, each of which is, to the best knowledge of E Fund, an independent third party of the 
Company, its subsidiaries, its substantial shareholders, E Fund, GF Securities and the companies which are 
members of the same group of GF Securities.
(9) 
E Fund HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds 
on behalf of its investors, each of which is, to the best knowledge of E Fund HK, an independent third party 
of the Company, its subsidiaries, its substantial shareholders, E Fund HK, GF Securities and the companies 
which are members of the same group of GF Securities.
(10) 
GF International will hold the Offer Shares in its capacity as the discretionary fund manager managing the 
funds on behalf of its investors, each of which is, to the best knowledge of GF International, an independent 
third party of the Company, its subsidiaries, its substantial shareholders, GF International, GF Securities 
and the companies which are members of the same group of GF Securities.
(11) 
Details of the collective investment schemes which is not authorized by the SFC are as follows:
No.
Fund name
Types and values 
of assets under 
management
Whether 
the scheme 
is publicly 
marketed
Scheme 
establishment 
date
Identities of 
the general 
partners and 
the 20 largest 
limited partners 
of the scheme 
where 
applicable
Identity of 
the scheme 
administrator
Relationships 
among the scheme, 
the ultimate beneficial 
owner(s) of the limited 
partner(s), the largest 
group of the shareholders/
controlling shareholders 
of the Company, 
and the Company
 
 
 
 
 
 
 
 
1.
GF Luminous Fund
Private Fund 
HKD 231 Million 
as of February 
2026
NO
November 
2025
Not applicable as 
it is a private 
fund
NuBright Fund 
Services 
Limited
The scheme and ultimate 
beneficial owners are 
independent third parties of 
GF Securities (Hong Kong) 
Brokerage, the Company and 
the Controlling Shareholders 
of the Company.

<<<PAGE 33>>>
– 33 –
No.
Fund name
Types and values 
of assets under 
management
Whether 
the scheme 
is publicly 
marketed
Scheme 
establishment 
date
Identities of 
the general 
partners and 
the 20 largest 
limited partners 
of the scheme 
where 
applicable
Identity of 
the scheme 
administrator
Relationships 
among the scheme, 
the ultimate beneficial 
owner(s) of the limited 
partner(s), the largest 
group of the shareholders/
controlling shareholders 
of the Company, 
and the Company
 
 
 
 
 
 
 
 
2.
GF Vision Fund
Private Fund 
HKD 81 Million 
as of March 2026
NO
March 2026
Not applicable as 
it is a private 
fund
NuBright Fund 
Services 
Limited
The scheme and ultimate 
beneficial owners are 
independent third parties of 
GF Securities (Hong Kong) 
Brokerage, the Company and 
the Controlling Shareholders 
of the Company.
3.
Golden Stone Fund
Private Fund 
HKD 49 Million 
as of February 
2026
NO
November 
2025
Not applicable as 
it is a private 
fund
NuBright Fund 
Services 
Limited
The scheme and ultimate 
beneficial owners are 
independent third parties of 
GF Securities (Hong Kong) 
Brokerage, the Company and 
the Controlling Shareholders 
of the Company.
4.
Golden Fortune 
Opportunity Fund
Private Fund 
HKD 45 Million 
as of February 
2026
NO
November 
2013
Not applicable as 
it is a private 
fund
ICBC (Aisa) 
Trustee 
Company 
Limited
The scheme and ultimate 
beneficial owners are 
independent third parties of 
GF Securities (Hong Kong) 
Brokerage, the Company and 
the Controlling Shareholders 
of the Company.
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of 
this announcement, make no representation as to its accuracy or completeness and expressly 
disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the 
whole or any part of the contents of this announcement.

<<<PAGE 34>>>
– 34 –
This announcement is not for release, publication, distribution, directly or indirectly, in or 
into the United States (including its territories and possessions, any state of the United States 
and the District of Columbia). This announcement does not constitute or form a part of any 
offer or solicitation to purchase or subscribe for securities in the United States. The securities 
mentioned herein have not been, and will not be, registered under the United States Securities 
Act of 1933, as amended (the “U.S. Securities Act”). The securities may not be offered or sold 
in the United States except pursuant to an exemption from the registration requirements of the 
U.S. Securities Act and in compliance with any applicable state securities laws, or outside the 
United States unless in compliance with Regulation S under the U.S. Securities Act. There will 
be no public offer of securities in the United States.
The Offer Shares are being offered and sold outside the United States in offshore transactions 
in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated March 12, 2026 issued by Delton 
Technology (Guangzhou) Inc. for detailed information about the Global Offering described 
below before deciding whether or not to invest in the H Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-
Overall Coordinators (for themselves and on behalf of the Overall Coordinators and the 
Hong Kong Underwriters) shall be entitled to terminate its obligations under the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out 
in the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong 
Public Offering – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. 
(Hong Kong time) on the Listing Date (which is currently expected to be on Friday, March 20, 
2026).
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, the H Shares expected to be held 
by the public have an expected value of approximately HK$3.31 billion (calculated based on the 
Offer Price of HK$71.88 per H Share), which is higher than the prescribed market value of the 
H Shares required to be held by the public of HK$3 billion under Rule 19A.13A(2). Based on 
the above, it is expected that our Company will satisfy the public float requirements as required 
under Rule 19A.13A(2) of the Listing Rules.

<<<PAGE 35>>>
– 35 –
Considering that the final Offer Price is fixed at the Offer Price of HK$71.88 per Offer Share, 
save for 20,674,500 H Shares (representing 4.38% of our total issued Shares immediately upon 
completion of the Global Offering) to be issued to the cornerstone investors that are subject to 
disposal restrictions for a period of six months from the Listing Date, the remaining 25,325,500 
H Shares with an expected market capitalization of approximately HK$1,820.40 million, 
which is higher than HK$600 million under Rule 19A.13C, will not be subject to any disposal 
restrictions (whether under contract, the Listing Rules, applicable laws or otherwise) at the time 
of the Listing. Our Company will satisfy the free float requirement under Rule 19A.13C of the 
Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public shareholders 
of the Company do not hold more than 50% of the H shares in public hands at the time of the 
Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at 
least 300 Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing 
Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, March 
20, 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus has not been exercised. Investors who trade the H Shares on the basis of publicly 
available allocation details prior to the receipt of H Share certificates or prior to the H Share 
certificates becoming valid evidence of title do so entirely at their own risk.

<<<PAGE 36>>>
– 36 –
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Friday, 
March 20, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Friday, March 20, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 100 H Shares each, and the stock code of the H Shares will 
be 1989.
By order of the Board
Delton Technology (Guangzhou) Inc.
Xiao Hongxing
Chairman of the Board
Hong Kong, March 19, 2026
As of the date of this announcement, the Board comprises Mr. Xiao Hongxing, Ms. Zeng Hong 
and Mr. Peng Jinghui as executive directors, Ms. Liu Jinchan as non-executive director, and 
Ms. Chen Limei, Ms. Li Ying and Dr. Shi Ling as independent non-executive directors.
