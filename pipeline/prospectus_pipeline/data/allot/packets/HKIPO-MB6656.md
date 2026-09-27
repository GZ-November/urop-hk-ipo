# 配发结果公告抽取任务：6656.HK Sigenergy Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**15/04/2026 22:32**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0415/2026041501574.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6656.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
are being offered and sold outside the United States in offshore transactions in accordance with Regulation S under the 
U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. Potential investors should read the Prospectus for detailed information about the Company 
and the Global Offering described below before deciding whether or not to invest in the Offer Shares.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated April 8, 2026 (the “Prospectus”) issued by Sigenergy Technology Co., Ltd. (思格新能
源(上海)股份有限公司) (the “Company”).
In connection with the Global Offering, CLSA Limited as stabilizing manager (the “Stabilization Manager”) (or its 
affiliates or any person acting for it), on behalf of the Underwriters, the extent permitted by the applicable laws and 
regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect transactions with a view to stabilizing 
or supporting the market price of the H Shares at such price, in such amounts and in such manners as the Stabilizing 
Manager, its affiliates or any person acting for it may determine and at a level higher than that which might otherwise 
prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing Manager (or its 
affiliates or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will 
be conducted at the absolute discretion of the Stabilization Manager (or its affiliates or any person acting for it) and 
in what the Stabilizing Manager reasonably regards as the best interest of our Company, (b) may be discontinued at 
any time and (c) is required to be brought to an end within 30 days of the last day for lodging applications under the 
Hong Kong Public Offering, being Wednesday, May 13, 2026. Such stabilizing action, if taken, may be effected in all 
jurisdictions where it is permissible to do so, in each case in compliance with all applicable laws, rules and regulatory 
requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong 
Kong), as amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering. After this date, when no further 
stabilizing action may be taken, demand for the H Shares, and therefore the price of the H Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out in 
the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not 
resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-
Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the 
events set out in the section headed “Underwriting — Underwriting Arrangements — Hong Kong Public Offering — 
Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date.

<<<PAGE 2>>>
2
Sigenergy Technology Co., Ltd.
( 思格新能源( 上海) 股份有限公司)
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
13,573,900 H Shares (subject to the Over-
 allotment Option)
Number of Hong Kong Offer Shares
:
1,357,400 H Shares 
Number of International Offer Shares
:
12,216,500 H Shares (subject to 
 the Over-allotment Option)
Offer Price
:
HK$324.20 per H Share, plus brokerage 
 of 1.0%, SFC transaction levy 
 of 0.0027%, AFRC transaction levy of 
 0.00015% and Stock Exchange trading
 fee of 0.00565% (payable in full on 
 application in Hong Kong dollars and 
 subject to refund)
Nominal value
:
RMB0.1 per H Share
Stock code
:
6656
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators, Joint Global 
Coordinators, Joint Bookrunners and Joint Lead Managers
Other Overall Coordinator, Joint Global Coordinator, 
Joint Bookrunner and Joint Lead Manager

<<<PAGE 3>>>
Sigenergy Technology Co., Ltd. 
思格新能源(上海)股份有限公司 
 
ANNOUNCEMENT OF ALLOTMENT RESULTS 
 
Unless otherwise defined herein, capitalized terms used in this announcement shall have the 
same respective meanings as those defined in the prospectus dated April 8, 2026 (the 
“Prospectus”) issued by Sigenergy Technology Co., Ltd. (思格新能源(上海)股份有限公司) 
(the “Company”).  
 
 
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, Shareholders and prospective investors should be aware that the price 
of the H Shares could move substantially even with a small number of H Shares traded 
and should exercise extreme caution when dealing in the H Shares. 
SUMMARY 
 
Company Information 
Stock Code 
6656 
Stock Short Name 
SIGENERGY 
Dealings commencement date 
April 16, 2026* 
* see note at the end of the announcement 
 
Price Information 
Offer Price 
HK$324.20 
 
Offer Shares and Share Capital 
Number of Offer Shares (before exercise 
of the Over-allotment Option) 
13,573,900 
Final number of Offer Shares in Hong 
Kong Public Offering  
1,357,400 
Final number of Offer Shares in 
International Offering  
12,216,500 
Number of issued Shares upon Listing 
(before exercise of the Over-allotment 
Option) 
246,796,930 
 
Over-allocation 
No. of Offer Shares over-allocated 
2,036,000 
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option 
is exercised, an announcement will be made on the Stock Exchange’s website. 
 

<<<PAGE 4>>>
Proceeds  
Gross proceeds (Note) 
HK$4,400.7 million 
Less:
Estimated 
listing 
expenses 
payable based on Final Offer 
Price 
HK$210.8 million  
Net Proceeds 
HK$4,189.9 million  
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For 
details of the use of proceeds, please refer to the section headed “Future Plans and Use of 
Proceeds” of the Prospectus. The Company will adjust the allocation of the net proceeds 
from the exercise of the Over-allotment Option (if any) for the purposes as set out in the 
section headed “Future Plans and Use of Proceeds” of the Prospectus on a pro rata basis. 
 
ALLOTMENT RESULTS DETAILS 
 
HONG KONG PUBLIC OFFERING 
 
 
No. of valid applications 
202,730 
No. of successful applications 
13,517 
Subscription level 
1,102.05 times 
Claw-back triggered 
N/A 
No. of Offer Shares initially available under the Hong Kong 
Public Offering 
1,357,400 
Final no. of Offer Shares under the Hong Kong Public 
Offering  
1,357,400 
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering 
10.0% 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, 
investors can refer to www.hkeipo.hk/IPOResult to perform a search by name or identification 
number or www.hkeipo.hk/IPOResult for the full list of allottees. 
 
INTERNATIONAL OFFERING  
 
 
No. of placees 
428 
Subscription Level 
31.2 times 
No. of Offer Shares initially available under the International Offering
12,216,500 
Final no. of Offer Shares under the International Offering  
12,216,500 
% of Offer Shares under the International Offering to the Global 
Offering  
90.0% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) 
a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by 

<<<PAGE 5>>>
the Stock Exchange to permit H Shares in the International Offering to be placed to close 
associates of certain existing Shareholders, and (b) a consent under Chapter 4.15 of the Guide 
for New Listing Applicants to permit the Company to, among other things, allocate further H 
Shares in the International Offering to certain Cornerstone Investors and/or their respective 
close associates, (i) none of the Offer Shares subscribed by the placees and the public have 
been financed directly or indirectly by the Company, any of the Directors, Supervisors, chief 
executive of the Company, substantial Shareholders, existing Shareholders of the Company or 
any of its subsidiaries or their respective close associates; and (ii) none of the placees and the 
public who have purchased the Offer Shares are accustomed to taking instructions from the 
Company, any of the Directors, Supervisors, chief executive of the Company, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their 
respective close associates in relation to the acquisition, disposal, voting or other disposition 
of H Shares registered in his/her/its name or otherwise held by him/her/it. 
 
The placees in the International Offering include the following: 
 
Cornerstone Investors  
 
Investor 
No. of Offer 
Shares 
allocated Note 1 
% of total 
issued H Shares 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)  
% of total issued 
share capital 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) 
Existing 
shareholders or 
their close 
associates Note 2 
Aranda 
Investments 
Pte. Ltd 
(“Aranda”) 
797,200 
0.57% 
0.32% 
No
Shanghai 
Lujiazui 
(Group) Co., 
Ltd. 
(GUOTAI 
JUNAN 
INVESTMEN
TS (HONG 
KONG) 
LIMITED 
OTC Swap) 
697,900 
0.50% 
0.28% 
No
Goldman 
Sachs Asset 
Management 
507,300 
0.36% 
0.21% 
No

<<<PAGE 6>>>
(Hong Kong) 
Limited 
(“GSAM”) 
HHLR 
Advisors, Ltd. 
(“HHLRA”) 
338,200 
0.24% 
0.14% 
No
Hillhouse 
Investment 
Management, 
Ltd. (“HIM”) 
169,100 
0.12% 
0.07% 
No
UBS Asset 
Management 
(Singapore) 
Ltd. (“UBS 
AM 
Singapore”) 
507,300 
0.36% 
0.21% 
No
AXA 
Investment 
Managers UK 
Limited 
(“AXA IM”) 
362,300 
0.26% 
0.15% 
No
CPE Energy 
Investment 
Limited 
(“CPE 
Energy”) 
362,300 
0.26% 
0.15% 
No
Lazurite Hime 
L.P.  
362,300 
0.26% 
0.15% 
No
Baring Asset 
Management 
(Asia) Limited 
(“Barings”) 
241,500 
0.17% 
0.10% 
No
Charoen 
Pokphand 
Robot Limited 
(“Charoen 
Pokphand”) 
241,500 
0.17% 
0.10% 
No
CPIC 
Investment 
Management 
(H.K.) 
Company 
Limited 
(“CPIC 
241,500 
0.17% 
0.10% 
No

<<<PAGE 7>>>
IMHK”) 
Fullgoal Asset 
Management 
(HK) Limited 
(“Fullgoal 
HK”) 
72,500 
0.05% 
0.03% 
No
Fullgoal Fund 
Management 
Co., Ltd. 
(“Fullgoal 
Fund”) 
169,000 
0.12% 
0.07% 
No
Greenwoods 
Asset 
Management 
Hong Kong 
Limited (“HK 
Greenwoods”
) 
241,500 
0.17% 
0.10% 
No
Huadeng 
Technology 
Space 
Ventures Ltd 
(“Huadeng 
Technology”) 
241,500 
0.17% 
0.10% 
No
ICBC Wealth 
Management 
Co., Ltd. 
(“ICBC 
Wealth”) 
241,500 
0.17% 
0.10% 
No
Perseverance 
Asset 
Management 
International 
(Singapore) 
Pte. Ltd. 
(“Perseveranc
e Asset 
Management
”) 
241,500 
0.17% 
0.10% 
No
Scene Cloud 
Global 
Limited 
(“Scene 
Cloud”) 
241,500 
0.17% 
0.10% 
No

<<<PAGE 8>>>
Tropical 
Terrain 
Limited 
241,500 
0.17% 
0.10% 
No
3W Fund 
Management 
Limited (“3W 
Fund”) 
241,500 
0.17% 
0.10% 
No
Total 
6,760,400 
4.84% 
2.74% 
-
Notes:  
(1) The number of Offer Shares allocated to such investor only represents the number of Offer Shares 
allocated to the investors as cornerstone investors in the International Offering. For allocations of 
Offer Shares to the relevant investor and/or its close associates as placee, please refer to the section 
headed “Allotment Results Details — International Offering — Allotee with waivers/ consents 
obtained” in this announcement. 
(2) In addition to the Offer Shares subscribed for as Cornerstone Investors, Aranda, GSAM, HHLRA, 
UBS AM Singapore, AXA IM, CPE Energy, Lazurite Hime L.P., CPIC IMHK and/or their respective 
close associates, where applicable, were allocated further Offer Shares as placees in the 
International Offering. Please refer to the section headed “Allotment Results Details – International 
Offer – Allotee with waivers/consents obtained” in this announcement for details. Only the Offer 
Shares subscribed for as Cornerstone Investors are subject to lock-up as indicated below. For 
details, please refer to the section headed “Lock-up Undertakings – Cornerstone Investors” in this 
announcement.  
 
Allottee with waivers/consents obtained 
 
Investor 
No. of Offer 
Shares allocated 
% of total 
issued H 
Shares after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option is 
not 
exercised  
% of total 
issued share 
capital after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option is 
not 
exercised  
Relationship 
Allotees with a waiver from strict compliance with Rule 10.04 of the Listing Rules and a 
consent under Paragraph 1C of Appendix F1 to the Listing Rules  
Eastern Bell 
Capital VIII 
Investment 
Limited (“Eastern 
Bell Capital 
Investment”)Note 1 
36,000
0.03%
0.01%
Close associate 
of Jiaxing Dingyun

<<<PAGE 9>>>
Mr. Pan Jian (潘
健) Note 2 
24,000
0.02%
0.01%
Close associate 
of Andaman 
International
Allotees with consent under paragraph 1C(2) of the Placing Guidelines and paragraph 18
of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further 
H Shares to investors who will participate in the Global Offering both as (i) a cornerstone 
investor and (ii) a placee in the International Offering Note 3 
Temasek Group  
289,800
0.21%
0.12%
Close associate of a
Cornerstone Investor
Goldman Sachs 
Asset 
Management 
(Singapore) Pte. 
Ltd. 
96,400
0.07%
0.04%
Close associate of a
Cornerstone Investor
HHLRA 
168,400
0.12%
0.07%
Cornerstone Investor
UBS Global AM 
(SG) 
96,400
0.07%
0.04%
Close associate of a
Cornerstone Investor
AXA IM 
48,000
0.03%
0.02%
Cornerstone Investor
CPE GROWTH 
FUND #1; Guotai 
Junan Investments 
(Hong Kong) 
Limited -
Yuanfeng Asset 
Management 
L.L.P. 
96,500
0.07%
0.04%
Close associates of a
Cornerstone Investor
Lazurite Hime 
L.P. 
11,750
0.01%
0.00%*
Cornerstone Investor
CPIC IMHK 
11,750
0.01%
0.00%*
Cornerstone Investor
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and paragraph 6 of 
Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations to connected 
clients Note 4 
CITIC Securities 
International 
Capital 
Management 
Limited (“CSI”) 
68,300
0.05%
0.03%
CSI is a member of the 
same group of 
companies as CLSA
Limited (“CLSA”)
China Galaxy 
International 
Investment 
Company Limited 
(“CGII”) 
87,200
0.06%
0.04%
CGII is a member of the 
same group of 
companies as China 
China Galaxy
International 
Securities 

<<<PAGE 10>>>
(Hong Kong) Co., 
Limited (“CGIS”) 
AXA IM 
362,300
0.26%
0.15%
AXA IM is a member of 
the same group of
companies as BNP
Paribas Securities (Asia)
Limited (“BNPP”)
CITIC Securities 
Asset 
Management 
Company Limited 
(“CITIC Asset 
Management”) 
10,400
0.01%
0.00%*
CITIC Asset 
Management is a 
member of the same 
group of companies as 
CLSA
CITIC Securities 
Asset 
management (HK) 
Limited (“CITIC 
AM HK”) 
1,800
0.00%*
0.00%*
CITIC AM HK is a 
member of the same 
group of companies as 
CLSA
China Asset 
Management 
(Hong Kong) 
Limited (“China 
AMC HK”) 
24,000
0.02%
0.01% 
China AMC HK is a 
member of the same 
group of companies as 
CLSA
Notes: 
 
* Percentage less than 0.005% 
 
1. Eastern Bell Capital Investment is a fellow subsidiary of Jiaxing Dingyun, both of which are subject 
to the common ultimate statutory control of Yan Li (嚴力). Therefore, Eastern Bell Capital 
Investment is a close associate of Jiaxing Dingyun, an existing Shareholder. 
 
2. Mr. Pan Jian (潘健) wholly owns Andaman International. Therefore, Mr. Pan Jian (潘健) is a close 
associate of Andaman International, an existing Shareholder. 
 
3. The number of Offer Shares allocated to the relevant investors listed in this subsection only 
represents the number of Offer Shares allocated to the investors as placees in the International 
Offering. For allocations of Offer Shares to the relevant investors as Cornerstone Investors, please 
refer to the section headed “Allotment Results Details – International Offer – Cornerstone 
Investors” in this announcement. For details of the consent under Chapter 4.15 of the Guide for 
New Listing Applicants in relation to allocations of further H Shares to the cornerstone investors
and/or their close associates, please refer to the section headed “Others/Additional Information –
Allocation of Offer Shares to Investors Who Will Participate in the Global Offering both as (i) a 
Cornerstone Investor and (ii) a Placee in the International Offering with consents under Chapter 
4.15 of the Guide for New Listing Applicants” in this announcement. 

<<<PAGE 11>>>
 
4. For details of the consent under paragraph 1C(1) of the Placing Guidelines and paragraph 6 of 
Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations to connected clients, 
please refer to the section headed “Others / Additional Information – Placing to connected clients 
with prior consents under paragraph 1C(1) of the Placing Guidelines” in this announcement. 

<<<PAGE 12>>>
 
 
LOCK-UP UNDERTAKINGS  
 
Existing Shareholders (excluding Pre-IPO Investors) 
 
Name 
Number of 
Shares held in 
the Company 
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
issued H 
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
exercised) 
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
subject to the 
lock-up 
undertakings
Note 
Controlling Shareholders 
Mr. Xu 
Yingtong 
23,745,860
6,829,380
4.89%
9.62%
April 15, 2027 
Jiaxing 
Ouji 
15,000,000
6,710,000
4.80%
6.08%
April 15, 2027 
Jiaxing 
Gulin 
18,330,000
6,110,000
4.37%
7.43%
April 15, 2027
Jiaxing 
Mailin 
49,145,280
14,134,330
10.12%
19.91%
April 15, 2027
Jiaxing 
Maita 
8,725,150
8,725,150
6.24%
3.54%
April 15, 2027
Other Existing Shareholder 
Mr. Zhang 
Xianmiao 
2,915,290
2,915,290
2.09%
1.18%
April 15, 2027
Note: The expiry date of the lock-up period is pursuant to the PRC Company Law, which is longer 
than the lock-up period required for controlling shareholders under Rule 10.07 of the Listing Rules. 
 
Pre-IPO Investors 
 
Name 
Number of 
Shares held 
in the 
Company 
subject to 
lock-up 
undertaking
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up 
undertaking
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
% of 
shareholdin
g in the 
Company 
subject to 
lock-up 
undertaking
Last day 
subject to 
the lock-up 
undertaking
s Note 

<<<PAGE 13>>>
 
 
s upon 
Listing 
s upon 
Listing 
undertaking
s upon 
Listing 
(assuming 
the Over-
allotment 
Option is 
not 
exercised) 
s upon 
Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised) 
Jiaxing 
Qianzhusong 
17,311,370
5,740,400
4.11%
9.34%
April 15, 2027 
Zhuhai 
Meiheng 
13,894,736
20,842,104
14.92%
14.08%
April 15, 2027 
Guangzhou 
Huaxin 
19,078,950
19,078,950
13.65%
7.73%
April 15, 2027
Jiaxing 
Dingyun 
6,705,260
6,705,260
4.80%
2.72%
April 15, 2027
Andaman 
International 
3,421,053
1,710,527
1.22%
2.08%
April 15, 2027
Hangzhou 
Yiyun 
3,719,260
3,719,260
2.66%
1.51%
April 15, 2027
Shanghai 
Yusong 
3,684,210
3,684,210
2.64%
1.49%
April 15, 2027
Jiaxing Yuzai 
3,421,050
3,421,050
2.45%
1.39%
April 15, 2027
Xingxu New 
Energy 
3,187,940
3,187,940
2.28%
1.29%
April 15, 2027
Gonqingchen
g Yunteng 
2,905,610
2,905,610
2.08%
1.18%
April 15, 2027
Jinan V Fund 
2,235,090
2,235,090
1.60%
0.91%
April 15, 2027
Xiamen 
Xiaoyu 
2,235,090
2,235,090
1.60%
0.91%
April 15, 2027
TTGG 
Ventures 
1,593,970
1,593,970
1.14%
0.65%
April 15, 2027
Jiefeng 
Technology 
1,578,950
1,578,950
1.13%
0.64%
April 15, 2027
Suzhou V 
Fund 
1,564,560
1,564,560
1.12%
0.63%
April 15, 2027
Xingxu 
Yaoneng 
531,320
531,320
0.38%
0.22%
April 15, 2027
Note: The expiry date of the lock-up period is pursuant to the PRC Company Law. 
 
Cornerstone Investors  
 
Name 
Number of H 
% of total 
% of 
Last day 

<<<PAGE 14>>>
 
 
Shares held in the 
Company subject to 
lock-up 
undertakings upon 
Listing 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing 
(assuming the 
Over-
allotment 
Option is not 
exercised) 
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
subject to the 
lock-up 
undertakings
Note  
Aranda  
797,200
0.57%
0.32%
October 15, 
2026
Shanghai 
Lujiazui 
(Group) 
Co., 
Ltd.
(GUOTAI 
JUNAN 
INVESTMENTS 
(HONG 
KONG) 
LIMITED 
OTC
Swap) 
697,900
0.50%
0.28%
October 15, 
2026
GSAM 
507,300
0.36%
0.21%
October 15, 
2026
HHLRA 
338,200
0.24%
0.14%
October 15, 
2026
HIM 
169,100
0.12%
0.07%
October 15, 
2026
UBS AM Singapore 
507,300
0.36%
0.21%
October 15, 
2026
AXA IM 
362,300
0.26%
0.15%
October 15, 
2026
CPE Energy  
362,300
0.26%
0.15%
October 15, 
2026
Lazurite Hime L.P.  
362,300
0.26%
0.15%
October 15, 
2026
Barings 
241,500
0.17%
0.10%
October 15, 
2026
Charoen Pokphand  
241,500
0.17%
0.10%
October 15, 
2026
CPIC IMHK 
241,500
0.17%
0.10%
October 15, 
2026
Fullgoal HK 
72,500
0.05%
0.03%
October 15, 
2026

<<<PAGE 15>>>
 
 
Fullgoal Fund 
169,000
0.12%
0.07%
October 15, 
2026
HK Greenwoods 
241,500
0.17%
0.10%
October 15, 
2026
Huadeng Technology 
241,500
0.17%
0.10%
October 15, 
2026
ICBC Wealth  
241,500
0.17%
0.10%
October 15, 
2026
Perseverance 
Asset 
Management  
241,500
0.17%
0.10%
October 15, 
2026
Scene Cloud  
241,500
0.17%
0.10%
October 15, 
2026
Tropical 
Terrain 
Limited 
241,500
0.17%
0.10%
October 15, 
2026
3W Fund  
241,500
0.17%
0.10%
October 15, 
2026
Note: In accordance with the relevant cornerstone investment agreements, the required lock-up ends 
on October 15, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or 
transferring H Shares subscribed for pursuant to the relevant cornerstone investment agreements 
after the indicated date. 
 
PLACEE CONCENTRATION ANALYSIS  
 
Placee
s* 
Numbe
r of H 
Shares 
allotte
d 
Allotment 
as % of 
Internatio
nal 
Offering 
(assuming 
no 
exercise of 
the Over-
allotment 
Option) 
Allotment 
as % of 
Internatio
nal 
Offering 
(assuming 
the Over- 
allotment 
Option is 
fully 
exercised 
and new 
H Shares 
are 
issued) 
Allotme
nt as % 
of total 
Offer 
Shares 
(assumi
ng no 
exercise 
of the 
Over-
allotme
nt 
Option) 
Allotme
nt as % 
of total 
Offer 
Shares 
(assumi
ng the 
Over-
allotme
nt 
Option 
is fully 
exercise
d and 
new H 
Shares 
are 
issued) 
Numbe
r of H 
Shares 
held 
upon 
Listing 
% of 
total 
issued 
share 
capital 
upon 
Listing 
(assumi
ng no 
exercise 
of the 
Over-
allotme
nt 
Option) 
% of 
total 
issued 
share 
capital 
upon 
Listing 
(assumi
ng the 
Over-
allotme
nt 
Option 
is fully 
exercise
d and 
new H 
Shares 
are 
issued) 

<<<PAGE 16>>>
 
 
Top 1 
       
1,087,0
00  
8.90% 
7.63% 
8.01% 
6.96% 
       
1,087,0
00  
0.44% 
0.44% 
Top 5 
       
3,668,0
00  
30.02% 
25.74% 
27.02% 
23.50% 
       
3,668,0
00  
1.49% 
1.47% 
Top 10 
       
5,562,9
50  
45.54% 
39.03% 
40.98% 
35.64% 
       
5,562,9
50  
2.25% 
2.24% 
Top 25 
       
8,954,7
00  
73.30% 
62.83% 
65.97% 
57.37% 
       
8,954,7
00  
3.63% 
3.60% 
 
Note 
* Ranking of placees is based on the number of H Shares allotted to the placees. 
 
H SHAREHOLDERS CONCENTRATION ANALYSIS  
 
H 
Sharehol
ders * 
Numb
er of 
H 
Shares 
allotte
d 
Allotmen
t as % of 
Internati
onal 
Offering 
(assumin
g no 
exercise 
of the 
Over-
allotment 
Option) 
Allotmen
t as % of 
Internati
onal 
Offering 
(assumin
g the 
Over- 
allotment 
Option is 
fully 
exercised 
and new 
H Shares 
are 
issued) 
Allotm
ent 
as % 
of total 
Offer 
Shares 
(assum
ing no 
exercis
e of the 
Over- 
allotm
ent 
Option
) 
Allotm
ent 
as % 
of total 
Offer 
Shares 
(assum
ing the 
Over- 
allotme
nt 
Option 
is fully 
exercis
ed and 
new H 
Shares 
are 
issued) 
Numbe
r of H 
Shares 
held 
upon 
Listing 
% of 
total 
issued 
H 
share 
capital 
upon 
Listing 
(assum
ing no 
exercis
e of the 
Over-
allotme
nt 
Option
) 
% of 
total 
issued 
H 
share 
capital 
upon 
Listing 
(assum
ing the 
Over-
allotme
nt 
Option 
is fully 
exercis
ed and 
new H 
Shares 
are 
issued) 
Top 1 
- 
0.00% 
0.00% 
0.00% 
0.00% 
20,842,1
04 
14.92% 
14.70% 
Top 5 
- 
0.00% 
0.00% 
0.00% 
0.00% 
69,609,9
14  
49.82% 
49.10% 
Top 10 
36,000 
0.29% 
0.25% 
0.27% 
0.23% 
98,630,8
70.59% 
69.57% 

<<<PAGE 17>>>
 
 
34 
Top 25 
3,100,
300 
25.38% 
21.75% 
22.84% 
19.86% 
128,727,
421 
92.12% 
90.80% 
 
Note 
* Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders 
upon Listing. 
 
SHAREHOLDER CONCENTRATION ANALYSIS  
 
Shareh
older s* 
Nu
mbe
r of 
H 
Sha
res 
allot
ted 
Allotme
nt as % 
of 
Internat
ional 
Offerin
g 
(assumi
ng no 
exercise 
of the 
Over-
allotme
nt 
Option) 
Allotme
nt as % 
of 
Internat
ional 
Offerin
g 
(assumi
ng the 
Over-
allotme
nt 
Option 
is fully 
exercise
d and 
new H 
Shares 
are 
issued) 
Allot
ment 
as % 
of 
total 
Offer 
Share
s 
(assu
ming 
no 
exerci
se of 
the 
Over- 
allotm
ent 
Optio
n) 
Allot
ment 
as % 
of 
total 
Offer 
Share
s 
(assu
ming 
the 
Over-
allotm
ent 
Optio
n is 
fully 
exerci
sed 
and 
new H 
Share
s are 
issued
) 
Numb
er of H 
Shares 
held 
upon 
Listing 
Numbe
r of 
Shares 
held 
upon 
Listing 
% of 
total 
issued 
share 
capita
l upon 
Listin
g 
(assu
ming 
no 
exerci
se of 
the 
Over-
allotm
ent 
Optio
n) 
% of 
total 
issued 
share 
capita
l upon 
Listin
g 
(assu
ming 
the 
Over-
allotm
ent 
Optio
n is 
fully 
exerci
sed 
and 
new H 
Share
s are 
issued
) 
Top 1 
- 
0.00% 
0.00% 
0.00% 
0.00% 
14,134,
330  
49,145,
280  
19.91
% 
19.75
% 
Top 5 
- 
0.00% 
0.00% 
0.00% 
0.00% 
66,625,
164  
149,75
8,700  
60.68
% 
60.18
% 
Top 10 
60,000 0.49% 
0.42% 
0.44% 
0.38% 
96,646,
101  
203,71
0,690  
82.54
% 
81.87
% 
Top 25 
3,124,
300  
25.57% 
21.92% 
23.02
% 
20.01
% 
128,75
1,421  
235,81
6,010  
95.55
% 
94.77
% 
 

<<<PAGE 18>>>
 
 
Note 
* Ranking of Shareholders is based on the number of Shares (of all classes) held by the 
Shareholder upon Listing. 
 
 

<<<PAGE 19>>>
 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
 
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made 
by the public will be conditionally allocated on the basis set out below: 
 
NO. OF SHARES 
APPLIED FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF 
ALLOTMENT / 
BALLOT 
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL NO. 
OF H SHARES 
APPLIED FOR 
POOL A 
100
93,509
1,871 out of 93,509 
applicants to receive 
100 H Shares
2.00%
200
9,671
291 out of 9,671 
applicants to receive 
100 H Shares
1.50%
300
9,338
281 out of 9,338 
applicants to receive 
100 H Shares
1.00%
400
3,118
112 out of 3,118 
applicants to receive 
100 H Shares
0.90%
500
3,878
144 out of 3,878 
applicants to receive 
100 H Shares
0.74%
600
2,470
92 out of 2,470 
applicants to receive 
100 H Shares
0.62%
700
1,716
65 out of 1,716 
applicants to receive 
100 H Shares
0.54%
800
1,562
63 out of 1,562 
applicants to receive 
100 H Shares
0.50%
900
1,241
51 out of 1,241 
applicants to receive 
100 H Shares
0.46%
1,000
10,934
437 out of 10,934 
applicants to receive 
100 H Shares
0.40%
1,500
4,902
221 out of 4,902 
applicants to receive 
0.30%

<<<PAGE 20>>>
 
 
100 H Shares
2,000
4,339
200 out of 4,339 
applicants to receive 
100 H Shares
0.23%
2,500
2,597
137 out of 2,597 
applicants to receive 
100 H Shares
0.21%
3,000
2,985
180 out of 2,985 
applicants to receive 
100 H Shares
0.20%
3,500
2,056
137 out of 2,056 
applicants to receive 
100 H Shares
0.19%
4,000
1,701
123 out of 1,701 
applicants to receive 
100 H Shares
0.18%
4,500
1,288
99 out of 1,288 
applicants to receive 
100 H Shares
0.17%
5,000
2,688
216 out of 2,688 
applicants to receive 
100 H Shares
0.16%
6,000
2,218
200 out of 2,218 
applicants to receive 
100 H Shares
0.15%
7,000
1,817
179 out of 1,817 
applicants to receive 
100 H Shares
0.14%
8,000
1,452
152 out of 1,452 
applicants to receive 
100 H Shares
0.13%
9,000
1,233
134 out of 1,233 
applicants to receive 
100 H Shares
0.12%
10,000
12,739
1,402 out of 12,739 
applicants to receive 
100 H Shares
0.11%
 
179,452
Total number of 
Pool A successful 
applicants: 6,787 
POOL B 
20,000
11,585
2,317 out of 11,585 
applicants to receive 
100 H Shares
0.10%

<<<PAGE 21>>>
 
 
30,000
3,210
792 out of 3,210 
applicants to receive 
100 H Shares
0.08%
40,000
1,783
510 out of 1,783 
applicants to receive 
100 H Shares
0.07%
50,000
1,308
420 out of 1,308 
applicants to receive 
100 H Shares
0.06%
60,000
947
334 out of 947 
applicants to receive 
100 H Shares
0.06%
70,000
671
257 out of 671 
applicants to receive 
100 H Shares
0.05%
80,000
533
219 out of 533 
applicants to receive 
100 H Shares
0.05%
90,000
340
148 out of 340 
applicants to receive 
100 H Shares
0.05%
100,000
1,711
786 out of 1,711 
applicants to receive 
100 H Shares
0.05%
200,000
559
367 out of 559 
applicants to receive 
100 H Shares
0.03%
300,000
243
197 out of 243 
applicants to receive 
100 H Shares
0.03%
400,000
98
93 out of 98 applicants 
to receive 100 H 
Shares
0.02%
500,000
53
100 H Shares
0.02%
600,000
29
100 H Shares plus 5 
out of 29 applicants to 
receive an additional 
100 H Shares
0.02%
678,700
208
100 H Shares plus 52 
out of 208 applicants 
to receive an 
additional 100 H 
Shares
0.02%
 
23,278
Total number of 

<<<PAGE 22>>>
 
 
Pool B successful 
applicants: 6,730 
 
As of the date of this announcement, the relevant subscription monies previously deposited in 
the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers for any inquiries. 
 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect 
of which consent has been obtained, the Company has complied with the Listing Rules and 
guidance materials in relation to the placing, allotment and listing of the Company’s H Shares.  
 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and trading fee payable.  
 
OTHERS / ADDITIONAL INFORMATION 
 
Allocations of Offer Shares to close associates of existing Shareholders with a waiver from 
strict compliance with Rule 10.04 of the Listing Rules and a consent under Paragraph 1C of 
Appendix F1 to the Listing Rules  
 
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted to 
the Company, a waiver from strict compliance with the requirements under Rule 10.04 and a 
prior written consent under paragraph 1C of Appendix F1 to the Listing Rules to permit Offer 
Shares in the International Offering to be placed to each of Eastern Bell Capital Investment and 
Mr. Pan Jian (潘健), a close associate of Jiaxing Dingyun and Andaman International, 
respectively, each an existing Shareholder, on the conditions that each of Jiaxing Dingyun 
(together with Eastern Bell Capital Investment) and Andaman International (together with Mr. 
Pan Jian (潘健)):  
 
(a) holds less than 5% of the total number of Shares in issue of our Company prior to the 
completion of the Global Offering; 
 
(b) is not and will not become (upon the completion of the Global Offering) a core connected 
person of the Company or the close associate of any such core connected person; 
 
(c) does not have the right to appoint a Director and/or have any other special rights; 
 
(d) will not affect the Company’s ability to satisfy the public float requirement as prescribed 
by the Stock Exchange under Rule 8.08 of the Listing Rules upon being allocated with the 
relevant number of Offer Shares; and 

<<<PAGE 23>>>
 
 
 
(e) have not been given preferential treatment. 
 
For details of the allocations of Offer Shares to a close associate of an existing Shareholder, 
please refer to the section headed “Allotment Results Details – International Offer – Allotees 
with Waivers/Consents Obtained” in this announcement. 
 
Allocation of Offer Shares to investors who will participate in the Global Offering both as (i) 
a Cornerstone Investor and (ii) a placee in the International Offering with consents under 
Chapter 4.15 of the Guide for New Listing Applicants 
 
The Company has applied to, and the Stock Exchange has granted, a waiver/consent under 
paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company 
to allocate further Offer Shares in the International Offering to the relevant Cornerstone 
Investors and/or their close associates as placees, subject to the following conditions: 
 
(a) the final offering size of the Global Offering (excluding any additional H Shares which may 
be issued upon exercise of the Over-allotment Option) will be of a total value of at least 
HK$1 billion as required by paragraph 18(i) of Chapter 4.15 of the Guide for New Listing 
Applicants; 
 
(b) where relevant, the Offer Shares allocated to all existing shareholders and their close 
associates (whether as cornerstone investors and/or as placees) as permitted under this 
exemption do not exceed 30% of the total number of the H Shares offered, which is in 
compliance with paragraph 18(ii) of Chapter 4.15 of the Guide for New Listing Applicants; 
 
(c) each Director, chief executive, Controlling Shareholder and Supervisor of the Company 
has confirmed that no securities have been allocated to them or their respective close 
associates under the Size-based Exemption as required by paragraph 18(iii) of Chapter 4.15 
of the Guide for New Listing Applicants; 
 
(d) the Company will comply with the public float requirement under Rule 8.08(1) (as 
amended and replaced by Rule 19A.13A) of the Listing Rules; and 
 
(e) details of the allocation to such investors under the exemption will be disclosed in this 
announcement. 
 
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange. 
 
For details of the allocations of Offer Shares to investors who will participate in the Global 
Offering both as (i) a cornerstone investor and (ii) a placee in the International Offering, please 
refer to the section headed “Allotment Results Details – International Offer – Allotees with 
Waivers/Consents Obtained” in this announcement. 

<<<PAGE 24>>>
 
 
 
Placing to connected clients with prior consents under paragraph 1C(1) of the Placing 
Guidelines 
 
The Company has applied for, and the Stock Exchange has granted, consents under paragraph 
1C(1) of the Placing Guidelines to permit allocation to connected clients pursuant to the Placing 
Guidelines. The allocation of Offer Shares to such connected clients is in compliance with all 
the conditions under the consents granted by the Stock Exchange. Details of the placement to 
connected clients (including the cornerstone tranche and placing tranche) are set out below.  

<<<PAGE 25>>>
 
 
 
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
third partis 
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which is 
not authorised 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of 
such scheme 
Number of Offer 
Shares to be 
allocated to the 
connected client 
Approximate 
percentage 
of Offer 
Shares 
(assuming no 
exercise of 
the Over-
allotment 
Option) 
Approximate 
percentage 
of total 
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
CLSA  
CSI 
CSI 
is 
a 
member of the 
same group of 
companies as
CLSA 
Non-
discretionary 
basis 
No 
68,300 
0.50% 
0.03% 
2. 
CGIS 
CGII 
CGII 
is 
a 
member of the 
same group of 
companies as
CGIS 
Non-
discretionary 
basis 
No 
87,200 
0.64% 
0.04% 
3. 
BNPP 
AXA IM Note 
1 
AXA IM is a 
member of the 
same group of 
companies as 
Discretionary 
basis 
Yes 
362,300 
2.67% 
0.15% 

<<<PAGE 26>>>
 
 
BNPP. 
4. 
CLSA 
CITIC Asset 
Management 
CITIC Asset 
Management 
is a member of 
the same 
group of 
companies as 
CLSA 
Discretionary 
basis 
CITIC Asset 
Management is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
10,400 
0.08% 
0.00%*  
5. 
CLSA 
CITIC AM 
HK 
CITIC AM 
HK is a 
member of the 
same group of 
companies as 
CLSA 
Discretionary 
basis 
No 
1,800 
0.01% 
0.00%*  
6. 
CLSA 
China AMC 
HK 
China AMC 
HK is a 
member of the 
same group of 
companies as 
CLSA 
Discretionary 
basis 
No 
24,000 
0.18% 
0.01%  
 
Notes: 
 
* Percentage less than 0.005% 
 

<<<PAGE 27>>>
 
 
(1) CSI 
 
CSI will hold the Offer Shares as a placee under the International Offering on behalf of its ultimate clients (the “CSI Ultimate Clients”), on a non-discretionary 
basis, pursuant to which: (i) CSI will act as the single counterparty of a back-to-back total return swap transaction (the “CSI Back-to-back TRS”) to be entered 
into by it in connection with a total return swap order (the “CSI Client TRS”) placed and fully funded by the CSI Ultimate Clients, by which CSI will pass the 
full economic exposure of the Offer Shares placed to CSI to the CSI Ultimate Clients; and (ii) as confirmed by CSI and CLSA, CSI will hold the legal title and 
beneficial interest in the Offer Shares, but will contractually agree to pass on the full economic exposure and return of the Offer Shares to the CSI Ultimate 
Clients, on a non-discretionary basis. The CSI Ultimate Clients may exercise their early termination rights to terminate the CSI Client TRS at any time from the 
trade date of the CSI Client TRS which should be on or after the date on which the Offer Shares are listed on the Stock Exchange; (iii) upon the final maturity 
or termination of the CSI Client TRS by the CSI Ultimate Clients, CSI will dispose of the Offer Shares on the secondary market and the CSI Ultimate Clients 
will receive a final termination amount of the CSI Back-to-back TRS which will have taken into account all the economic returns or economic loss in relation 
to the Offer Shares and the fixed amount of transaction fees of the CSI Back- to-back TRS and the CSI Client TRS. Due to its internal policy, CSI will not 
exercise the voting right of the Offer Shares during the terms of the CSI Back-to-back TRS; and (iv) CSI is not a collective investment scheme which is not 
authorized by the SFC, nor is expected to hold the Offer Shares on behalf of such scheme.  
 
The details of the CSI Ultimate Clients are as follows: 
  
Name  
Fund Manager 
UBO of Fund Manager 
Limited Partner/Shareholding 
holding 30% or more in the CSI 
Ultimate Clients 
Tongyi Taoli No.1 Private 
Securities Investment Fund (通怡
桃李1 號私募證券投資基金) 
Shanghai Tongyi Investment Management 
Co., Ltd. (上海通怡投資管理有限公司) 
Chu Yibo (儲貽波) 
Wang Jing (王靜) 
Lingding Gaoshan No.11 Private 
Securities Investment Fund (淩頂
高山11 號私募證券投資基金) 
Ningbo Meishan Bonded Port Area Lingding 
Investment Management Co., Ltd. (寧波梅山
保稅港區淩頂投資管理有限公司) 
Chen Youfang (陳有方) 
Deng Chunyan (鄧春燕) 
Shao Rongxuan (邵榮炫) 
Zhu Xiao (朱曉) 
Evolution Darwin Shangshan No.3 
Private Securities Investment Fund 
Hainan Evolution Private Fund Management 
Co., Ltd. (海南進化論私募基金管理有限公
Wang Yiping (王一平) 
Wang Yiping (王一平) 

<<<PAGE 28>>>
 
 
(進化論達爾文上善三號私募證
券投資基金) 
司) 
Yue Min Tou New Selection 
Opportunity No.1 Private 
Securities Investment Fund (粵民
投新選機遇1 號私募證券投資基
金) 
Yue Min Tou Private Securities Fund 
Management (Shenzhen) Co., Ltd. (粵民投私
募證券基金管理（深圳）有限公司) 
Not applicable 
Liu Wei (劉偉) 
Yuanleshng Qiangye Private 
Securities Investment Fund (源樂
晟強業私募證券投資基金) 
Tibet Longrising Asset Management Co.,LTD 
(西藏源樂晟資產管理有限公司) 
Zeng Xiaojie (曾曉潔) 
Hu Caiyang (胡彩陽) 
Yuanleshng Qiangshi Private 
Securities Investment Fund (源樂
晟強勢私募證券投資基金) 
Tibet Longrising Asset Management Co.,LTD 
(西藏源樂晟資產管理有限公司) 
Zeng Xiaojie (曾曉潔) 
Not applicable 
Hover4pi Fund I OFC 
Hover4pi Capital Management 
He Hui 
Not applicable 
Canaan China Flagship Fund 
Not applicable 
Not applicable 
LIANG Hao 
LW Investment II 
LW INVESTMENT VCC 
Chan Hock Eng, Xie 
Dahong 
Xu Chong 
LW Investment III 
LW INVESTMENT VCC 
Chan Hock Eng, Xie 
Dahong 
Not applicable 
 
To the best of knowledge of CSI and after making all reasonable enquiries, the CSI Ultimate Clients, together with each of their ultimate beneficial owners, is 
an independent third party of the Company, its subsidiaries, its substantial shareholders, CSI, CLSA and the companies which are members of the same group 
of companies as CLSA. 
 
(2) CGII 
 
CGII and China Galaxy Securities (“CGS”) will enter into a series of cross border total return swap (TRS) transactions (collectively, the “CGII TRS”) with 
each other and the ultimate clients (“CGII Ultimate Clients”), pursuant to which CGII will hold the Offer Shares on a non-discretionary basis to hedge the 

<<<PAGE 29>>>
 
 
CGII TRS while the economic risks and returns of the underlying Offer Shares are ultimately borne by the CGII Ultimate Clients, subject to customary fees and 
commissions. The CGII TRS will be fully funded by the CGII Ultimate Clients. During the terms of the CGII TRS, all economic returns of the Offer Shares 
subscribed by CGII will be passed to CGII Ultimate Clients and all economic loss shall be borne by CGII Ultimate Clients through the CGII TRS, and CGII 
will not take part in any economic return or bear any economic loss in relation to the Offer Shares. The CGII TRS are linked to the Offer Shares and CGII 
Ultimate Clients may, after expiration of the lock-up period beginning from the date of the relevant cornerstone agreements and ending on the date which is six 
months from the Listing Date, request to early terminate the CGII TRS at its own discretion, upon which CGII may dispose of the Offer Shares on the secondary 
market and CGII Ultimate Clients will receive a final settlement amount of the CGII TRS in cash in accordance with the terms and conditions of the CGII TRS.  
The details of the CGII Ultimate Clients are as follow:  
 
Name  
Fund Manager 
UBO of Fund Manager 
Limited Partner/Shareholding holding 
30% or more in the CSI Ultimate 
Clients 
Lingding Gaoshan No. 11 Private 
Securities Investment Fund (淩頂
高山11 號私募證券投資基金) 
Ningbo Meishan Bonded Port Area Lingding 
Investment Management Co., Ltd. (寧波梅山
保稅港區淩頂投資管理有限公司) 
Deng Chunyan (鄧春燕) 
Chen Youfang (陳有方) 
Zhu Xiao (朱曉) 
Shao Rongxuan (邵榮炫)  
 
To the best of CGII’ s knowledge after having made all reasonable inquiries, each of the CGII Ultimate Clients is an independent third party of (i) the Company, 
its subsidiaries, its substantial shareholders, and (ii) CGII, CGIS and the companies which are members of the same group of CGIS. Both CGII and CGIS are 
indirect wholly-owned subsidiaries of CGS, the A shares of which are listed on the Shanghai Stock Exchange (stock code: 601881), the H shares of which are 
listed on the Stock Exchange (stock code: 6881). CGII is a connected client (as defined under Appendix F1 to the Listing Rules) of CGIS, holding securities on 
a non-discretionary basis on behalf of independent third parties. 
 
(3) AXA IM 
 
AXA IM, a wholly-owned subsidiary of BNPP Asset Management Holding (“BNPP AM”), will arrange the investment in the Offer Shares in its capacity as 
delegated investment manager on behalf of their investors (the “AXA IM Ultimate Clients”), each of which is, to the best knowledge of BNPP AM, an 
independent third party of the Company, its subsidiaries, its substantial shareholders, AXA IM, BNPP and the companies which are members of the same group 
of BNPP. No ultimate beneficial owner holds 30% or more interest in the funds, and none of BNPP and, to the best knowledge of BNPP AM, BNPP AM is not 

<<<PAGE 30>>>
 
 
aware of any companies which are members of the same group of BNPP that hold any beneficial interest in any of the funds. 
 
The details of the AXA IM Ultimate Clients are as follows: 
 
Fund Name 
Fund Manager 
UBO of Fund Manager 
Limited 
Partner/Shareholding 
holding 30% or more in the AXA IM 
Ultimate Clients 
BNP Paribas Clean Energy Solutions 
Fund 
AXA IM 
BNP Paribas SA 
N/A 
BNP Paribas Europe Environmental 
Solutions Fund 
AXA IM 
BNP Paribas SA 
N/A 
 
To the best of knowledge of BNPP AM and after making all reasonable enquiries, AXA IM Ultimate Clients, together with each of their ultimate beneficial 
owners, is an independent third party of the Company, its subsidiaries, its substantial shareholders, AXA IM, BNPP and the companies which are members of 
the same group of BNPP. 
 
(4) CITIC Asset Management 
 
CITIC Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their investors (the 
“CITIC Asset Management Ultimate Clients”), each of which is, to the best knowledge of CITIC Asset Management, (i) an independent third party of the 
Company, its subsidiaries, its substantial shareholders, CITIC Asset Management, CLSA and the companies which are members of the same group of companies 
as CLSA; and (ii) a collective investment scheme which is not authorized by the SFC. No ultimate beneficial owner holds 30% or more interest in the funds. 
The details of the CITIC Asset Management Ultimate Clients are as follows: 
 
Fund Name 
Values of Assets 
under Management 
Whether the 
Scheme is 
Publicly 
Marketed 
Fund Manager 
UBO of Fund 
Manager 
Limited Partner of the CITIC 
Asset Management Ultimate 
Clients 

<<<PAGE 31>>>
 
 
CITIC SECURITIES COMPANY 
LIMITED-XINHANG ZHIYUAN 
NO.1 (中信證券信航致遠1 號集
合資産管理計劃) 
RMB26,274,974.36 
Not publicly 
marketed 
CITIC Asset 
Management 
CITIC Securities 
Company Limited 
26 limited partners in total, all of 
which are individuals 
CITIC SECURITIES COMPANY 
LIMITED-XINHANG ZHIYUAN 
NO.3 (中信證券信航致遠3 號集
合資産管理計劃) 
RMB62,521,444.68 
Not publicly 
marketed 
CITIC Asset 
Management 
CITIC Securities 
Company Limited 
48 limited partners in total, all of 
which are individuals  
CITIC Securities AM-
Guibinfengyuan No.118 QDII (中
信證券資管貴賓豐元118 號
QDII 集合資産管理計劃) 
RMB226,629,029.61 
Not publicly 
marketed 
CITIC Asset 
Management 
CITIC Securities 
Company Limited 
Eight limited partners in total, 
each of which is either a single 
asset management scheme or a 
collective asset management 
scheme 
 
To the best of knowledge of CITIC Asset Management and after making all reasonable enquiries, (i) CITIC Asset Management Ultimate Clients, together with 
each of their ultimate beneficial owners, is an independent third party of the Company, its subsidiaries, its substantial shareholders, CITIC Asset Management, 
CLSA and the companies which are members of the same group of companies as CLSA, and (ii) none of CLSA and any companies which are members of the 
same group of companies as CLSA that hold any beneficial interest in any of CITIC Asset Management Ultimate Clients. 
 
(5) CITIC AM HK 
 
CITIC AM HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the fund on behalf of its underlying client, namely CLSA 
CT LIMITED SUB ACCOUNT 29 – CGM, of which the ultimate beneficial owner holding 30% or more interest therein is SUN Shigen, and of which is, to the 
best knowledge of CITIC AM HK, an independent third party of the Company, its subsidiaries, its substantial shareholders, CITIC AM HK, CLSA and the 
companies which are members of the same group companies as CLSA. 
 
The ultimate beneficial owner of CITIC AM HK is CITIC Securities Company Limited (中信證券股份有限公司, 6030.HK). 
 

<<<PAGE 32>>>
 
 
(6) China AMC HK 
 
China AMC HK is an investment advisor and a delegate of the investment manager of its underlying clients (“China AMC HK Ultimate Clients”) and manages 
assets (in its capacity as an investment advisor of the China AMC HK Ultimate Clients) and executes trades (in its capacity as a delegate of the investment 
manager of China AMC HK Ultimate Clients) for on behalf of China AMC HK Ultimate Clients, namely (i) CHINAAMC FUND - CHINAAMC CHINA 
OPPORTUNITIES FUND, with no ultimate beneficial owner holding 30% or more interest therein; (ii) CHINAAMC SELECT GREATER CHINA 
TECHNOLOGY FUND, the ultimate beneficial owner of which is Futu Securities19 International (Hong Kong) Limited, holding 51.87% interest therein; (iii) 
CHINAAMC CHINA FOCUS FUND, the ultimate beneficial owner of which is Manulife (International) Limited, holding 73.17% interest therein; and (iv) 
CHINAAMC CHINA GROWTH FUND (SICAV), the ultimate beneficial owner of which is Yuanta Securities (HK) Company LTD, holding 72.73% interest 
therein. To the best knowledge of China AMC HK after making all reasonable enquiries, (i) each of the China AMC HK Ultimate Clients is an independent third 
party of the Company, its subsidiaries, its substantial shareholders, CLSA, China AMC HK and the companies which are members of the same group of 
companies as CLSA; and (ii) China AMC HK is not a collective investment scheme which is not authorised by the SFC. 
 

<<<PAGE 33>>>
 
 
 
DISCLAIMERS 
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
and Hong Kong Securities Clearing Company Limited take no responsibility for the contents 
of this announcement, make no representation as to its accuracy or completeness and 
expressly disclaim any liability whatsoever for any loss howsoever arising from or in reliance 
upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or 
into the United States (including its territories and possessions, any state of the United States 
and the District of Columbia). This announcement does not constitute or form a part of any 
offer or solicitation to purchase or subscribe for securities in the United States. The 
securities mentioned herein have not been, and will not be, registered under the United States 
Securities Act of 1933, as amended (the “U.S. Securities Act”). The securities may not be 
offered or sold in the United States except pursuant to an exemption from the registration 
requirements of the U.S. Securities Act and in compliance with any applicable state securities 
laws, or outside the United States unless in compliance with Regulation S under the U.S. 
Securities Act. There will be no public offer of securities in the United States.
The Offer Shares are being offered and sold outside the United States in offshore transactions 
in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated April 8, 2026 issued by Sigenergy 
Technology Co., Ltd. for detailed information about the Global Offering described below 
before deciding whether or not to invest in the H Shares thereby being offered.
*Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-
Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall 
be entitled to terminate their obligations under the Hong Kong Underwriting Agreement with 
immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting – Underwriting Arrangements – Hong Kong Public Offering – Hong Kong 
Underwriting Agreement – Grounds for Termination” in the Prospectus at any time prior to 
8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on April 
16, 2026).
 
 
 

<<<PAGE 34>>>
 
 
PUBLIC FLOAT 
 
Immediately after the completion of the Global Offering (before any exercise of the Over-
allotment Option), the total number of H Shares held in public hands represents approximately 
27.44% of the total issued share capital of the Company, which is higher than the prescribed 
percentage of H Shares required to be held in public hands of 15% under Rule 19A.13A(1) of 
the Listing Rules calculated based on the final Offer Price of HK$324.20 per H Share, thereby 
satisfying Rule 19A.13A(1) of the Listing Rules. 
 
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors (excluding the Offer Shares 
subscribed for by them as placees) upon the Listing shall not be counted towards the free float 
of the H Shares of the Company at the time of Listing. Based on the final Offer Price of 
HK$324.20 per H Share, the Company satisfies the free float requirement under Rule 
19A.13C(1)(b) of the Listing Rules. 
 
The Directors confirm that, immediately following the completion of the Global Offering 
(before any exercise of the Over-allotment Option), (i) no placee will, individually, be placed 
more than 10% of the enlarged issued share capital of the Company immediately after the 
Global Offering; (ii) there will not be any new substantial Shareholder immediately after the 
Global Offering; (iii) the three largest public shareholders of the Company do not hold more 
than 50% of the H shares in public hands at the time of the Listing in compliance with Rules 
8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at the 
time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.  
 
COMMENCEMENT OF DEALINGS 
 
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Thursday, 
April 16, 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting – Underwriting 
Arrangements – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade the H Shares on the basis of publicly available 
allocation details prior to the receipt of H Share certificates or prior to the H Share certificates 
becoming valid evidence of title do so entirely at their own risk. 
 
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Thursday, 
April 16, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Thursday, April 16, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 100 H Shares each, and the stock code of the H Shares 
will be 6656.  
 
By order of the Board  
Sigenergy Technology Co., Ltd.  
Mr. Xu Yingtong 
Chairman of the Board, Executive Director and 
Chief Executive Officer
 
Hong Kong, April 15, 2026 
As at the date of this announcement, the Board comprises: (i) Mr. Xu Yingtong and Mr. 

<<<PAGE 35>>>
 
 
Zhang Xianmiao as executive directors; (ii) Mr. Sun Guoqing, Mr. Wang Lin and Ms. 
Yang Ting as non-executive directors and (iii) Ms. Ng Wing Yan Claudia, Mr. Lin Jinwu 
and Ms. Chen Jijin as proposed independent non-executive directors.  
 
