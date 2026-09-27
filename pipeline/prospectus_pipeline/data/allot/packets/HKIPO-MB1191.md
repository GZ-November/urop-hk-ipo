# 配发结果公告抽取任务：1191.HK Crealights Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**26/06/2026 21:58**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0626/2026062602599.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1191.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
– 1 –
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock 
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for 
the contents of this announcement, make no representation as to its accuracy or completeness and expressly 
disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings 
as those defined in the prospectus dated June 18, 2026 (the “Prospectus”) issued by Crealights Technology 
Co., Ltd. (北京海光芯正科技股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. Potential investors should read Prospectus for detailed information 
about the Company and the Global Offering described below before deciding whether or not to invest in the 
Offer Shares.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe 
for securities in the United States or in any other jurisdictions. The securities mentioned herein have not 
been, and will not be, registered under the United States Securities Act of 1933 as amended from time to time 
(the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the United States and may 
not be offered, sold, pledged or otherwise transferred within the United States except in transactions exempt 
from, or not subject to, the registration requirements of the U.S. Securities Act. There will be no public offer 
of securities in the United States. The Offer Shares are being offered and sold outside the United States in 
offshore transactions in reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, Huatai Financial Holdings (Hong Kong) Limited, as stabilizing 
manager (the “Stabilizing Manager”), or any person acting for it, on behalf of the Underwriters, may 
over-allocate or effect transactions with a view to stabilizing or supporting the market price of the Shares at 
a level higher than that which might otherwise prevail for a limited period after the Listing Date. However, 
there is no obligation on the Stabilizing Manager, or any person acting for it to conduct any such stabilizing 
action, which, if commenced, will be done at the sole and absolute discretion of the Stabilizing Manager, or 
any person acting for it, and may be discontinued at any time. Any such stabilizing action is required to be 
brought to an end on the 30th day after the last day for the lodging of applications under the Hong Kong 
Public Offering. Such stabilizing action, if taken, may be effected in all jurisdictions where it is permissible 
to do so, in each case in compliance with all applicable laws, rules and regulatory requirements, including 
the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, 
made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the Shares 
for longer than the stabilization period, which begins on the Listing Date and is expected to expire on the 
30th day after the last day for lodging applications under the Hong Kong Public Offering. After this date, 
when no further stabilizing action may be taken, demand for the Shares, and therefore the price of the Shares, 
could fall.
Potential investors of the Offer Shares should note that the Overall Coordinator (for itself and on behalf 
of the Hong Kong Underwriter) shall be entitled to terminate their obligations under the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section 
headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Hong 
Kong Underwriting Agreement — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. 
(Hong Kong time) on the Listing Date (which is currently expected to be on Monday, June 29, 2026).

<<<PAGE 2>>>
– 2 –
Crealights Technology Co., Ltd.
北京海光芯正科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under 
the Global Offering
:
13,431,500 H Shares (subject to the 
Over-allotment Option)
Number of Hong Kong Offer Shares
:
1,343,150 H Shares
Number of International Offer Shares
:
12,088,350 H Shares (subject to the 
Over-allotment Option)
Offer Price
:
HK$114.00 per H Share, plus brokerage 
of 1.0%, SFC transaction levy of 
0.0027%, Hong Kong Stock Exchange 
trading fee of 0.00565% and AFRC 
transaction levy of 0.00015%
Nominal Value
:
RMB1.0 per H Share
Stock Code
:
1191
Sole Sponsor, Overall Coordinator, Sponsor-Overall Coordinator, 
Global Coordinator, Bookrunner and Lead Manager

<<<PAGE 3>>>
3 
 
Crealights Technology Co., Ltd. / 北京海光芯正科技股份有限公司 
ANNOUNCEMENT OF ALLOTMENT RESULTS 
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated 18 June 2026 (the “Prospectus”) issued by Crealights Technology Co., Ltd. (the 
“Company”). 
Warning: In view of high concentration of shareholding in a small number of Shareholders, Shareholders and 
prospective investors should be aware that the price of the H Shares could move substantially even with a small 
number of H Shares traded and should exercise extreme caution when dealing in the H Shares. 
SUMMARY 
 
Company information 
Stock code 
1191 
Stock short name 
CREALIGHTS 
Dealings commencement date 
29 June 2026* 
*see note at the end of the announcement 
 
Price Information 
Final Offer Price 
HK$114.00 
Offer Price Range 
N/A 
Offer Price Adjustment exercised 
N/A 
 
Offer Shares and Share Capital 
Number of Offer Shares (before exercise of the Over-allotment 
Option) 
13,431,500 
Number of Offer Shares in Hong Kong Public Offering (after 
reallocation) 
1,343,150 
Number of offer shares in International Offering (after 
reallocation) 
12,088,350 
Number of issued shares upon Listing (before exercise of the 
Over-allotment Option) 
89,542,045 
 
 
Over-allocation 
No. of Offer Shares over-allocated 
2,014,700 
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases in the 
secondary market at prices that do not exceed the Offer Price or through deferred delivery or a combination of 
these means. In the event the Over-allotment Option is exercised, an announcement will be made on the Stock 
Exchange’s website. 
 
Proceeds 
Gross proceeds (Note) 
HK$1,531.19 million 
Less: Estimated listing expenses payable based on Final Offer 
Price 
HK$(115.87) million 
Net proceeds 
HK$1,415.32 million 
Note: Gross proceeds refers to the amount to which the issuer is entitled to receive. For details of the use of proceeds,
please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The Company will adjust 
the allocation of the net proceeds from the exercise of the Over-allotment Option (if any) for the purposes as set out
in the section headed “Future Plans and Use of Proceeds” of the Prospectus on a pro rata basis.  
 

<<<PAGE 4>>>
4 
 
 
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING 
 
 
No. of valid applications 
185,373 
No. of successful applications 
23,975 
Subscription level  
1,296.89 times 
Claw-back triggered 
N/A 
No. of Offer Shares initially available under the Hong Kong Public 
Offering 
1,343,150 
No. of Offer Shares reallocated from the International Offering 
(claw-back) 
N/A 
Final no. of Offer Shares under the Hong Kong Public Offering 
(after reallocation) 
1,343,150 
% of Offer Shares under the Hong Kong Public Offering to the Global 
Offering  
10.00% 
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can refer to
www.eipo.com.hk/eIPOAllotment to perform a search by identification number or www.eipo.com.hk/eIPOAllotment
for the full list of allottees. 
INTERNATIONAL OFFERING 
 
 
No. of placees 
116 
Subscription Level 
15.51 times 
No. of Offer Shares initially available under the International Offering 
12,088,350 
Final no. of Offer Shares under the International Offering  
12,088,350 
% of Offer Shares under the International Offering to the Global Offering 90.00% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for a consent under paragraph 18 
of Chapter 4.15 of the Guide for New Listing Applicants (“the Guide”) granted by the Stock Exchange to permit the 
Company to, among other things, allocate further H Shares in the International Offering to certain existing Shareholders 
and/or their close associates and Cornerstone Investors and/or their close associates, (i) none of the Offer Shares 
subscribed by the placees and the public have been financed directly or indirectly by the Company, any of the Directors, 
chief executive of the Company, controlling shareholders, substantial shareholders, existing shareholders of the Company 
or any of its subsidiaries or their respective close associates; and (ii) none of the placees and the public who have 
purchased the Offer Shares are accustomed to taking instructions from the Company, any of the Directors, chief executive 
of the Company, substantial shareholders, existing shareholders of the Company or any of its subsidiaries or their 
respective close associates in relation to the acquisition, disposal, voting or other disposition of Shares registered in 
his/her/its name or otherwise held by him/her/it.

<<<PAGE 5>>>
5 
 
Cornerstone Investors 
 
 
 
 
 
 
 
 
Name Note 1 
 
 
 
 
 
 
No. of Offer 
Shares allocated 
 
 
 
 
 
 
% of total issued H- 
shares after the 
Global Offering Note 2 
 
 
 
 
% of total issued 
share capital after 
the Global Offering 
Note 2 
 
 
 
 
Existing 
shareholders or 
their close 
associates 
JSC International 
Investment Fund 
SPC (acting for 
and on behalf of 
Jingxin SP)Note 3 
2,192,950 
2.45% 
2.45% 
Yes 
Winwin Technology 
Investment Co., Limited 
/ 雙贏科技投資有限公
司 (“Winwin 
Technology”) 
1,754,350 
1.96% 
1.96% 
No 
Kingsoft Cloud Network 
Corporation Limited / 金
山雲網絡有限公司 
(“Kingsoft Cloud 
Network”) 
343,600 
0.38% 
0.38% 
No 
UBS Asset Management 
(Singapore) Ltd. (“UBS 
AM Singapore”) 
1,374,450 
1.53% 
1.53% 
No 
Perseverance Asset 
Management 
International (Singapore) 
Pte. Ltd. 
(“Perseverance Asset 
Management”) 
687,200 
0.77% 
0.77% 
No 
E Fund Note 4 
343,600 
0.38% 
0.38% 
No 
Subtotal 
6,696,150 
7.48% 
7.48%  
Notes: 
 
1. For further details of the cornerstone investors, please refer to the section headed “Cornerstone Investors” 
of the Prospectus. 
2. Assuming the Over-allotment Option is not exercised. 
3. For details of the consent under paragraph 18 of Chapter 4.15 of the Guide in relation to allocations to 
close associate of an existing shareholder, please refer to the section headed “Waivers from Strict 
Compliance with the Listing Rules – Allocation of Offer Shares to close associate of an existing shareholder 
as cornerstone investor” in the Prospectus. 
4. E Fund comprises of E Fund Management Co., Ltd. ( 易方達基金管理有限公司)(“E Fund 
Management”) and E Fund Management (Hong Kong) Co., Ltd. (易方達資產管理(香港)有限公司)(“E 
Fund HK”). 
 
 

<<<PAGE 6>>>
6 
 
 
Allotees with Waivers/Consents Obtained 
 
 
 
 
 
 
 
 
Investor 
 
 
 
 
 
No. 
of 
Offer 
Shares 
allocated 
 
 
 
 
 
% of 
Offer 
Shares 
 
 
 
% of total issued 
H-shares after 
the Global 
Offering upon 
listing Note 1 
 
 
% of 
shareholding in 
the Company 
upon listing Note 1 
 
 
 
 
 
 
 
Relationship 
Allotees with consent under paragraph 18 of Chapter 4.15 of the Guide in relation to subscription for H Shares by a close
associate of existing shareholders as cornerstone investor Note 2   
Cornerstone Investor 
JSC International 
Investment Fund SPC 
(acting for and on behalf 
of Jingxin SP)Note 3 
 
2,192,950 
16.33% 
2.45% 
2.45% 
A cornerstone 
investor and close 
associate of existing 
shareholder 
Allotees with consent under paragraph 18 of Chapter 4.15 of the Guide in relation to allocations of further H Shares to 
cornerstone investors and/or their respective close associates as placees Note 2 Note 3  
UBS AM Singapore 
825,000 
6.14% 
0.92% 
0.92% 
Cornerstone Investor 
Perseverance Asset 
Management 
156,150 
1.16% 
0.17% 
0.17% 
Cornerstone Investor 
CITIC Securities 
International Capital 
Management Limited 
(“CSI”) 
187,850 
1.40% 
0.21% 
0.21% 
Close associate of a 
Cornerstone Investor 
E Fund Management Co., 
Ltd. (易方達基金管理有
限公司) (“E Fund 
Management”) 
17,000 
0.13% 
0.02% 
0.02% 
Cornerstone Investor 
E Fund Management 
(Hong Kong) Co., Ltd. 
(易方達資產管理(香港)
有限公司) (“E Fund 
HK”) 
154,600 
1.15% 
0.17% 
0.17% 
Cornerstone Investor 
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and  Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations to connected clients Note 4 
China Galaxy 
International Investment 
Company Limited 
80,000 
0.60% 
0.09% 
0.09% 
Connected Client 

<<<PAGE 7>>>
7 
 
(“CGII”) Note 4  
Guotai Junan Investments 
(Hong Kong) Limited 
(“GTJAI”) Note 4 
156,000 
1.16% 
0.17% 
0.17% 
Connected Client 
Bosera Asset 
Management 
(International) Co., Ltd 
(“Bosera AM”) Note 4 
20,000 
0.15% 
0.02% 
0.02% 
Connected Client 
Fullgoal Fund 
Management Co., Ltd. 
(“Fullgoal Fund”) Note 4 
46,000 
0.34% 
0.05% 
0.05% 
Connected Client 
Fullgoal Asset 
Management (HK) 
Limited (“Fullgoal HK”) 
Note 4  
2,000 
0.01% 
0.00% 
0.00% 
Connected Client 
Notes: 
1. Assuming the Over-allotment Option is not exercised. 
 
2. The Stock Exchange has granted a waiver from strict compliance with the requirements under Rule 9.09(b) of the 
Listing Rules and consent under paragraph 18 of Chapter 4.15 of the Guide to permit H Shares in the International
Offering to be placed to close associates of existing shareholders as a cornerstone investor. For details of the consent 
under paragraph 18 of Chapter 4.15 of the Guide in relation to allocations to close associate of an existing shareholder,
please refer to the section headed “Waivers from Strict Compliance with the Listing Rules – Allocation of Offer Shares
to close associate of an existing shareholder as cornerstone investor” in the Prospectus and the section headed 
“Others/Additional Information – Allocations of Offer Shares to the existing shareholders and Cornerstone Investors
and/or their close associates with a consent under Paragraph 18 of Chapter 4.15 of the Guide” of this announcement.
 
3. The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the number 
of Offer Shares allocated to the investors as placees in the International Offering. For allocations of Offer Shares 
to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment Results Details – 
International Offering – Cornerstone Investors” in this announcement. For details of the consent under paragraph 
18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further H Shares to the 
Cornerstone Investors, please refer to the section headed “Others/Additional Information – Allocations of Offer 
Shares to the existing shareholders and Cornerstone Investors and/or their close associates with a consent under 
Paragraph 18 of Chapter 4.15 of the Guide” of this announcement. 
 
4. For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients, please refer to the section headed “Allottees with 
waivers/consents obtained – International Offering – allotees with consent under paragraph 1C(1) of the Placing 
Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations to connected 
clients” of this announcement. 
 
 
 
 

<<<PAGE 8>>>
8 
 
LOCK-UP UNDERTAKINGS 
 
Single Largest Group of Shareholders 
 
 
 
 
 
 
 
 
 
Name 
 
 
Number of H- 
shares held in the 
Company subject 
to lock-up 
undertakings upon 
listing 
 
 
 
% of total issued H-
shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
listing Note 1 
 
 
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
listing Note 1 
 
 
 
 
 
 
Last day subject 
to the lock-up 
undertakings Note 2 
Hu Zhaoyang /胡朝陽 
8,452,320 
9.44% 
9.44% 
28 June 2027 
Suzhou Haiyi 
Investment Management 
Partnership Enterprise 
(Limited Partnership) / 
蘇州海怡投資管理合夥
企業(有限合夥) 
4,743,660 
5.30% 
5.30% 
28 June 2027 
Suzhou Haixu 
Investment Management 
Partnership Enterprise 
(Limited Partnership) /
蘇州海旭投資管理合夥
企業(有限合 夥) 
2,872,380 
3.21% 
3.21% 
28 June 2027 
Subtotal 
16,068,360 
17.95% 
17.95% 
Notes: 
 
1. Assuming the Over-allotment Option is not exercised. 
2. The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws. 
 

<<<PAGE 9>>>
9 
 
Existing Shareholders and Pre-IPO Investors 
 
 
 
 
 
 
 
 
 
Name 
 
 
Number of H- 
shares held in 
the Company 
subject to lock-
up undertakings 
upon listing 
 
 
 
% of total issued H-
shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
listing Note 1 
 
 
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
listing Note 1 
 
 
 
 
 
 
Last day subject 
to the lock-up 
undertakings Note 2 
Suzhou Ronglian Venture 
Capital Partnership (L.P.) / 
蘇州融聯創業投資企業
(有限合夥) 
5,294,880 
5.91% 
5.91% 
28 June 2027 
Suzhou Huiqi Venture 
Capital Partnership 
(Limited Partnership) / 蘇
州匯琪創業投資合夥企業
(有限合夥) 
1,920,900 
2.15% 
2.15% 
28 June 2027 
Suzhou Jusheng 
Entrepreneurship 
Investment Co., Ltd. / 蘇州
聚昇創業投資有限公司 
344,880 
0.39% 
0.39% 
28 June 2027 
Suzhou Jingu Yuanxin 
Technology Venture 
Capital Partnership(Limited 
Partnership) / 蘇州金谷源
鑫科技創業投資合夥企業
(有限合夥) 
250,140 
0.28% 
0.28% 
28 June 2027 
Suzhou Xieli Venture 
Capital Co., Ltd./ 蘇州協
立創業投資有限公司 
3,547,440 
3.96% 
3.96% 
28 June 2027 
Suzhou Junshi Xieli 
Venture Investment Co., 
Ltd. / 蘇州君實協立創業
投資有限公司 
2,833,020 
3.16% 
3.16% 
28 June 2027 
Zhenjiang Junding Xieli 
Entrepreneurship 
Investment Co., Ltd. / 鎮江
君鼎協立創業投資有限公
司 
517,260 
0.58% 
0.58% 
28 June 2027 
Jiangsu Gaotou Bondshine 
Venture Capital Partnership 
(L.P.) / 江蘇高投邦盛創業
投資合夥企業(有限合夥) 
3,378,960 
3.77% 
3.77% 
28 June 2027 
Suzhou Bangsheng 
Yingxin Venture 
Investment 
Enterprises(L.P.) / 蘇州邦
盛贏新創業投資企業(有
限合夥) 
1,707,000 
1.91% 
1.91% 
28 June 2027 

<<<PAGE 10>>>
10 
 
Nanjing Bangsheng Juyuan 
Venture Capital Partnership 
(Limited Partnership)/ 南京
邦盛聚源創業投資合夥企
業(有限合夥) 
185,760 
0.21% 
0.21% 
28 June 2027 
Wuxi Yuli Venture Capital 
Partnership (L.P.) / 無錫毓
立創業投資合夥企業(有
限合夥) 
1,491,780 
1.67% 
1.67% 
28 June 2027 
Suzhou Association For 
Wide Band-Aid Venture 
Capital Center (L.P.) / 蘇州
協立寬禁帶創業投資中心
(有限合夥) 
863,700 
0.96% 
0.96% 
28 June 2027 
Suzhou Industrial Park 
Integrated Circuit Growth 
Fund Partnership (Limited 
Partnership) / 蘇州工業園
區集成電路成長基金合夥
企業(有限合夥) 
1,194,857 
1.33% 
1.33% 
28 June 2027 
Suzhou Industrial Park 
Zone Qina Venture Capital 
Co., Ltd. / 蘇州工業園區
啟納創業投資有限公司 
1,146,660 
1.28% 
1.28% 
28 June 2027 
Tianjin TEDA Venture 
Capital Group Corporation 
Limited / 天津泰達科技創
業投資集團股份有限公司 
5,025,180 
5.61% 
5.61% 
28 June 2027 
Jiangsu Bohua Equity 
Investment Partnership 
Enterprise (Limited 
Partnership) / 江蘇博華股
權投資合夥企業(有限合
夥) 
4,291,948 
4.79% 
4.79% 
28 June 2027 
Beijing Information 
Industry Development 
Investment Fund (Limited 
Partnership) / 北京信息產
業發展投資基金(有限合
夥) 
4,291,948 
4.79% 
4.79% 
28 June 2027 
Beijing Economic and 
Technological 
Development Zone 
Industrial Upgrading 
Equity Investment Fund 
Phase II (Limited 
Partnership) / 北京經濟技
術開發區產業升級股權投
資基金二期(有限合夥)) 
4,291,948 
4.79% 
4.79% 
28 June 2027 
Alibaba (China) 
Technology Co., Ltd. / 阿
里巴巴(中國)網絡技術有
限公司 
3,600,000 
4.02% 
4.02% 
28 June 2027 
Beijing Xiaomi Zhizao 
2,063,844 
2.30% 
2.30% 
28 June 2027 

<<<PAGE 11>>>
11 
 
Equity Investment Fund 
Partnership Enterprise 
(Limited Partnership) / 北
京小米智造股權投資基金
合夥企業(有限合夥) 
Beijing Haiju Assistance 
Entrepreneurship 
Investment Center (L.P.) /
北京海聚助力創業投資中
心(有限合夥) 
1,986,780 
2.22% 
2.22% 
28 June 2027 
Shanghai Handuo 
Investment Center (L.P.) /
上海漢鐸投資中心(有限
合夥) 
1,920,900 
2.15% 
2.15% 
28 June 2027 
Yiwu Huaxinyuanjing 
Venture Capital 
Center(L.P.) / 義烏華芯遠
景創業投資中心(有限合
夥) 
1,666,680 
1.86% 
1.86% 
28 June 2027 
Jiaxing Gaohe Venture 
Capital Partnership (L.P.) /
嘉興高和創業投資合夥企
業(有限合夥) 
1,440,660 
1.61% 
1.61% 
28 June 2027 
Suzhou Yinji Venture 
Capital Co., Ltd. / 蘇州銀
基創業投資有限 公司 
1,102,260 
1.23% 
1.23% 
28 June 2027 
Jiangsu Zhongtian 
Technology Co. Ltd. / 江蘇
中天科技股份有限公司 
1,000,020 
1.12% 
1.12% 
28 June 2027 
Nantong Jinyuan Huifu 
Entrepreneurship 
Investment Partnership 
Enterprise (Limited 
Partnership) /南通金源匯
富創業投資合夥企業(有
限合夥) 
886,860 
0.99% 
0.99% 
28 June 2027 
Suzhou Juyuan Casting 
Venture Capital Partnership 
(L.P.) /蘇州聚源鑄芯創業
投資合夥企業(有限合夥) 
666,660 
0.74% 
0.74% 
28 June 2027 
Jiang Wenhao / 蔣文昊 
612,000 
0.68% 
0.68% 
28 June 2027 
Zhong Junqi / 鐘俊奇 
517,260 
0.58% 
0.58% 
28 June 2027 
Subtotal 
60,042,185 
67.05% 
67.05% 
Notes: 
 
1. Assuming the Over-allotment Option is not exercised. 
2. The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws. 
 
 

<<<PAGE 12>>>
12 
 
Cornerstone Investors 
 
 
 
 
 
 
 
 
Name 
 
 
Number of H- 
shares held in the 
Company subject 
to lock-up 
undertakings upon 
listing 
 
 
 
% of total issued H-
shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
listing Note 1 
 
 
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
listing Note 1 
 
 
 
 
Last day subject 
to the lock-up 
undertakings Note 2 
JSC International 
Investment Fund 
SPC (acting for 
and on behalf of 
Jingxin SP)Note 3 
2,192,950 
2.45% 
2.45% 28 December 2026 
Winwin Technology 
Investment Co., Limited 
/ 雙贏科技投資有限公
司 (“Winwin 
Technology”) 
1,754,350 
1.96% 
1.96% 28 December 2026 
Kingsoft Cloud Network 
Corporation Limited / 金
山雲網絡有限公司 
(“Kingsoft Cloud 
Network”) 
343,600 
0.38% 
0.38% 28 December 2026 
UBS Asset Management 
(Singapore) Ltd. (“UBS 
AM Singapore”) 
1,374,450 
1.53% 
1.53% 28 December 2026 
Perseverance Asset 
Management 
International (Singapore) 
Pte. Ltd. 
(“Perseverance Asset 
Management”) 
687,200 
0.77% 
0.77% 28 December 2026 
E Fund 
343,600 
0.38% 
0.38% 28 December 2026 
Subtotal 
6,696,150 
7.48% 
7.48%  
Notes: 
 
1. Assuming the Over-allotment Option is not exercised. 
2. In accordance with the relevant cornerstone investment agreements, the required lock-up ends on 28 
December 2026. The Cornerstone Investors will cease to be prohibited from disposing of or transferring 
H Shares subscribed for pursuant to the relevant cornerstone investment agreements after the indicated 
date. 

<<<PAGE 13>>>
13 
 
PLACEE CONCENTRATION ANALYSIS 
 
 
 
 
 
 
 
 
Placees* 
Number of H Shares 
allotted
 
 
 
 
Allotment as % of 
International Offering 
(assuming no exercise of 
the Over-allotment 
Option) 
Allotment as % of
International Offering
(assuming the Over-
allotment Option is 
fully exercised and new
H Shares are issued)
 
 
 
 
 
Allotment as % of total 
Offer Shares (assuming no 
exercise of the Over- 
allotment Option) 
 
 
 
Allotment as % of total 
Offer Shares (assuming 
the Over-allotment 
Option is fully 
exercised and new H 
Shares are issued) 
Number of H Shares held
upon Listing
% of total issued H Share
capital upon Listing
(assuming no
exercise of the Over-
allotment Option)
 
 
 
% of total issued H share 
capital upon Listing 
(assuming the Over- 
allotment Option is 
fully exercised and new H 
Shares are issued) 
% of total issued Share
capital upon Listing
(assuming no
exercise of the Over-
allotment Option)
 
 
 
% of total issued share 
capital upon Listing 
(assuming the Over- 
allotment Option is 
fully exercised and new H 
Shares are issued) 
Top 1 
   
2,199,450  
18.19% 
15.60% 
16.38% 
14.24% 
   
2,199,450  
2.46% 
2.40% 
2.46% 
2.40% 
Top 5 
   
8,750,650  
72.39% 
62.05% 
65.15% 
56.65% 
   
8,750,650  
9.77% 
9.56% 
9.77% 
9.56% 
Top 10 
   
10,965,850  
90.71% 
77.76% 
81.64% 
70.99% 
   
10,965,850  
12.25% 
11.98% 
12.25% 
11.98% 
Top 25 
   
12,759,750  
105.55% 
90.48% 
95.00% 
82.61% 
   
12,759,750  
14.25% 
13.94% 
14.25% 
13.94% 
Notes 
* Ranking of placees is based on the number of H Shares allotted to the placees. 
 
 

<<<PAGE 14>>>
14 
 
H SHAREHOLDER CONCENTRATION ANALYSIS 
 
 
 
 
 
 
 
 
 
 
 
H Shareholders* 
 
 
 
 
 
 
 
 
 
 
Number of H Shares 
allotted 
 
 
 
 
 
 
 
 
Allotment as 
% of International 
Offering (assuming no 
exercise of the Over-
allotment 
Option) 
 
 
 
Allotment as % 
of International 
Offering (assuming 
the Over- allotment 
Option is fully 
exercised and new 
H Shares are issued) 
 
 
 
 
 
 
 
Allotment as % of total 
Offer Shares (assuming no 
exercise of the Over- 
allotment 
Option) 
 
 
 
Allotment as % of total 
Offer Shares (assuming 
the Over-allotment 
Option is fully 
exercised and new H 
Shares are issued) 
Number of H Shares
held upon Listing
 
 
 
 
 
 
 
% of total issued H 
Share capital upon 
Listing (assuming no 
exercise of the Over-
allotment Option)
 
 
 
 
% of total issued H Share 
capital upon Listing 
(assuming the Over- 
allotment Option is 
fully exercised and new H 
Shares are issued) 
 
 
 
 
 
% of total issued 
Share capital upon 
Listing (assuming no 
exercise of the Over- 
allotment 
Option) 
 
 
 
% of total issued share 
capital upon Listing 
(assuming the Over- 
allotment Option is 
fully exercised and new 
H Shares are issued) 
Top 1 
- 
0.00% 
0.00% 
0.00% 
0.00% 
   
16,068,360  
17.95% 
17.55% 
17.95% 
17.55% 
Top 5 
   
2,192,950  
18.14% 
15.55% 
16.33% 
14.20% 
   
46,825,446  
52.29% 
51.14% 
52.29% 
51.14% 
Top 10 
   
2,192,950  
18.14% 
15.55% 
16.33% 
14.20% 
   
64,439,571  
71.97% 
70.38% 
71.97% 
70.38% 
Top 25 
   
8,750,650  
72.39% 
62.05% 
65.15% 
56.65% 
   
84,861,195  
94.77% 
92.69% 
94.77% 
92.69% 
 
Notes 
* Ranking of H Shareholders is based on the number of H Shares (of all classes) held by the H Shareholders upon Listing. 
 
 

<<<PAGE 15>>>
15 
 
SHAREHOLDER CONCENTRATION ANALYSIS 
 
 
 
 
 
 
 
 
 
 
 
 
 
Shareholders* 
 
 
 
 
 
 
 
Number of H Shares 
allotted
Allotment as % of
International Offering
(assuming no exercise of
the Over-allotment
Option)
Allotment as % of
International Offering
(assuming the Over-
allotment Option is 
fully exercised and new
H Shares are issued)
Allotment as % of total
Offer Shares (assuming no
exercise of the Over-
allotment Option)
Allotment as % of total
Offer Shares (assuming
the Over-allotment 
Option is fully 
exercised and new H
Shares are issued)
Number of H Shares held
upon Listing
Number of total shares
held upon Listing
% of total issued Share
capital upon Listing
(assuming no
exercise of the Over-
allotment Option)
% of total issued share
capital upon Listing
(assuming the Over-
allotment Option is 
fully exercised and new H 
Shares are issued)
Top 1 
                      -   
- 
- 
- 
- 
   
16,068,360  
   
16,068,360  
17.95% 
17.55% 
Top 5 
   
2,192,950  
18.14% 
15.55% 
16.33% 
14.20% 
   
46,825,446  
   
46,825,446  
52.29% 
51.14% 
Top 10 
   
2,192,950  
18.14% 
15.55% 
16.33% 
14.20% 
   
64,439,571  
   
64,439,571  
71.97% 
70.38% 
Top 25 
8,750,650 
72.39% 
62.05% 
65.15% 
56.65% 
   
84,861,195  
   
84,861,195  
94.77% 
92.69% 
 
Notes 
* Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing. 
 

<<<PAGE 16>>>
16 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 185,373 valid applications 
made by the public will be conditionally allocated on the basis set out below: 
 
NO. OF H 
SHARES 
APPLIED 
FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF ALLOCATION/BALLOT 
APPROXIMATE 
PERCENTAGE 
ALLOTED OF 
THE TOTAL 
NO. OF H 
SHARES 
APPLIED FOR 
POOL A 
50 
81,051 
3,242 out of 81,051 to receive 50 Shares 
4.00% 
100 
10,376 
511 out of 10,376 to receive 50 Shares 
2.46% 
150 
4,366 
243 out of 4,366 to receive 50 Shares 
1.86% 
200 
3,510 
213 out of 3,510 to receive 50 Shares 
1.52% 
250 
3,089 
200 out of 3,089 to receive 50 Shares 
1.29% 
300 
2,286 
156 out of 2,286 to receive 50 Shares 
1.14% 
350 
1,731 
124 out of 1,731 to receive 50 Shares 
1.02% 
400 
11,092 
826 out of 11,092 to receive 50 Shares 
0.93% 
450 
1,949 
150 out of 1,949 to receive 50 Shares 
0.86% 
500 
6,367 
507 out of 6,367 to receive 50 Shares 
0.80% 
600 
1,893 
159 out of 1,893 to receive 50 Shares 
0.70% 
700 
1,341 
118 out of 1,341 to receive 50 Shares 
0.63% 
800 
4,015 
368 out of 4,015 to receive 50 Shares 
0.57% 
900 
1,498 
142 out of 1,498 to receive 50 Shares 
0.53% 
1,000 
6,809 
667 out of 6,809 to receive 50 Shares 
0.49% 
2,000 
4,543 
547 out of 4,543 to receive 50 Shares 
0.30% 
3,000 
3,002 
408 out of 3,002 to receive 50 Shares 
0.23% 
4,000 
2,487 
369 out of 2,487 to receive 50 Shares 
0.19% 
5,000 
2,688 
426 out of 2,688 to receive 50 Shares 
0.16% 
6,000 
1,456 
244 out of 1,456 to receive 50 Shares 
0.14% 
7,000 
1,170 
205 out of 1,170 to receive 50 Shares 
0.13% 
8,000 
1,129 
206 out of 1,129 to receive 50 Shares 
0.11% 
9,000 
1,247 
236 out of 1,247 to receive 50 Shares 
0.11% 
10,000 
3,799 
741 out of 3,799 to receive 50 Shares 
0.10% 

<<<PAGE 17>>>
17 
 
15,000 
2,607 
574 out of 2,607 to receive 50 Shares 
0.07% 
20,000 
1,823 
437 out of 1,823 to receive 50 Shares 
0.06% 
25,000 
1,255 
322 out of 1,255 to receive 50 Shares 
0.05% 
30,000 
1,065 
288 out of 1,065 to receive 50 Shares 
0.05% 
35,000 
866 
246 out of 866 to receive 50 Shares 
0.04% 
40,000 
1,888 
557 out of 1,888 to receive 50 Shares 
0.04% 
Total: 
172,398 
Total number of Pool A successful applicants: 13,432 
 
 
 
 
POOL B 
45,000 
3,928 
2,706 out of 3,928 to receive 50 Shares 
0.08% 
50,000 
4,575 
3,365 out of 4,575 to receive 50 Shares 
0.07% 
100,000 
1,935 
50 Shares 
0.05% 
150,000 
825 
50 Shares plus 377 out of  825 to receive additional 50 Shares 
0.05% 
200,000 
549 
50 Shares plus 408 out of  549 to receive additional 50 Shares 
0.04% 
250,000 
222 
100 Shares 
0.04% 
300,000 
262 
100 Shares plus 64 out of  262 to receive additional 50 Shares 
0.04% 
400,000 
180 
100 Shares plus 123 out of  180 to receive additional 50 Shares 
0.03% 
500,000 
138 
150 Shares 
0.03% 
671,550 
361 
150 Shares plus 254 out of  361 to receive additional 50 Shares 
0.03% 
Total: 
12,975 
Total number of Pool B successful applicants: 10,543 
 

<<<PAGE 18>>>
18 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the designated 
nominee accounts have been remitted back to the accounts of all HKSCC participants. Investors should contact 
their relevant brokers for any inquiries. 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of which consent 
has been obtained, the Company has complied with the Listing Rules and guidance materials in relation to the 
placing, allotment and listing of the Company’s H Shares. 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the public (as the 
case may be) directly or indirectly for each Offer Share subscribed for or purchased by them was the same as the final 
Offer Price in addition to any brokerage, AFRC transaction levy, SFC transaction levy and Stock Exchange trading fee 
payable. 
 
OTHERS / ADDITIONAL INFORMATION 
 
Allocations of Offer Shares to the existing shareholders and Cornerstone Investors and/or their close associates 
with a consent under Paragraph 18 of Chapter 4.15 of the Guide 
 
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph  18 of Chapter 4.15 of the 
Guide for New Listing Applicants to permit the Company to allocate  further Offer Shares in the International Offering 
to certain existing Shareholders and Cornerstone Investors and/or their close associates as placees, subject to the following 
conditions (“Allocation to Size-based Exemption Participants”): 
 
(a) the final offering size of the Global Offering, excluding any over-allocation will be of a total value of at least 
HK$1 billion; 
 
(b) the Offer Shares allocated to all existing Shareholders (whether as cornerstone investors or placees) as permitted 
under this exemption do not exceed 30% of the total number of the H Shares offered under the Global Offering;  
 
(c) each Director, supervisor and chief executive of the Company confirms that no Offer Shares have been allocated 
to them or their respective close associates under this exemption;  
 
(d) the Allocation to Size-based Exemption Participants will not affect the Company’s ability to satisfy its public 
float requirement as prescribed by the Stock Exchange under Rule 19A.13A(1) of the Listing Rules; and 
 
(e) details of the Allocation to Size-based Exemption Participants under this exemption has been disclosed in this 
announcement. 
 
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted by the Stock 
Exchange. 
 
For details of the allocations of Offer Shares to Cornerstone Investors, please refer to the section headed “Allotment 
Results Details – International Offering – Allotees with Waivers/Consents Obtained” in this announcement. 
 
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines 
 
Under the International Offering, certain Offer Shares were placed to connected clients of their connected distributors 
pursuant to the Placing Guidelines. Please refer to the section headed “Allotment Results Details – International Offering 
– Allotees with Waivers/Consents Obtained” in this announcement for details. The Company has applied to the Stock 
Exchange for, and the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing Guidelines to permit 
the Company to allocate such Offer Shares in the International Offering to the connected clients. The allocation of Offer 
Shares to such connected clients is in compliance with all the conditions under the consent granted by the Stock Exchange. 
Details of the placement to connected clients are set out below.

<<<PAGE 19>>>
19 
 
Part A - Connected Clients holding the beneficial interest of the Offer Shares on a non-discretionary basis on behalf of independent third parties 
No. 
Connected 
Distributor 
Connected 
Client 
Relationship 
with the 
Connected 
Distributor 
Identities of the 
ultimate beneficial 
owners of the 
Offer Shares or, 
where applicable, 
details of the 
structured 
products under 
which the 
subscription by the 
Connected Client 
was made (e.g. 
OTC total return 
swaps)  
 
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which 
is not 
authorised by 
the SFC or is 
expected to 
hold the Offer 
Shares on 
behalf of such 
scheme  
 
Number of 
Offer Shares 
allocated to 
the connected 
client 
Approximate 
percentage of 
total number 
of Offer 
Shares 
(assuming the 
Over-
allotment 
Option is not 
exercised) 
Approximate 
percentage of total 
Shares in issue 
immediately 
following the 
completion of Global 
Offering (assuming 
the Over-allotment 
Option is not 
exercised) 
1. 
China Galaxy 
International 
Securities (Hong 
Kong) Co., 
Limited (“CGIS”) 
China Galaxy 
International 
Investment 
Company 
Limited 
(“CGII”) Note(1) 
members of 
the same 
group 
Please refer to Note 
1 
No 
80,000  
0.60% 
0.09% 
2. 
Guotai Junan 
Securities (Hong 
Kong) Limited 
(“GTJAS”) and 
Haitong 
International 
Securities 
Company Limited 
(“Haitong”) 
Guotai Junan 
Investments 
(Hong Kong) 
Limited 
(“GTJAI”) 
Note(2) 
members of 
the same 
group 
Please refer to Note 
2 
No   
156,000 
1.16% 
0.17% 
 
 
 

<<<PAGE 20>>>
20 
 
Part B - Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties 
No. 
Connected 
Distributor 
Connected Clients 
Relationship with 
the Connected 
Distributor 
Whether the 
Connected Client 
is a collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme  
Maximum number 
of Offer Shares 
(rounded down to 
nearest whole 
board lot of 50 
Shares) to be 
allocated to the 
connected client 
Approximate 
percentage of 
total number 
of Offer 
Shares 
(assuming the 
Over-
allotment 
Option is not 
exercised) 
Approximate 
percentage of total 
Shares in issue 
immediately 
following the 
completion of 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised) 
1. CMB 
International 
Capital 
Limited 
(“CMBI”), 
CMB 
International 
Securities 
Limited 
(“CMBI 
Securities”), 
and CMB 
International 
Global 
Markets 
Limited 
(“CMBI 
Global 
Markets”)  
Bosera Asset 
Management 
(International) Co., 
Ltd (“Bosera 
AM”) Note(3) 
members of the 
same group 
No   
20,000 
0.15% 
0.02% 

<<<PAGE 21>>>
21 
 
2. GTJAS and 
Haitong  
Fullgoal Fund 
Management Co., 
Ltd. (“Fullgoal 
Fund”) Note(4) 
members of the 
same group 
Yes 
46,000 
0.34% 
0.05% 
Fullgoal Asset 
Management (HK) 
Limited (“Fullgoal 
HK”) Note(5) 
members of the 
same group 
Yes 
2,000 
0.01% 
0.00% 
Notes:  
1. CGII and China Galaxy Securities (“CGS”) will enter into a series of cross border total return swap (TRS)  transactions (collectively, the “CGII TRS”) with each 
other and the ultimate client (“CGII Ultimate Client”),  pursuant to which CGII will hold the Offer Shares on a non-discretionary basis to hedge the CGII TRS while  
the economic risks and returns of the underlying Offer Shares are ultimately borne by the CGII Ultimate Client,  subject to customary fees and commissions. The 
CGII TRS will be fully funded by the CGII Ultimate Client.  During the terms of the CGII TRS, all economic returns of the Offer Shares subscribed by CGII will be 

<<<PAGE 22>>>
22 
 
passed  to CGII Ultimate Client and all economic loss shall be borne by CGII Ultimate Client through the CGII TRS,  and CGII will not take part in any economic 
return or bear any economic loss in relation to the Offer Shares. 
The CGII Ultimate Client may exercise an early termination right to terminate the CGII TRS at any time from the issue date of the CGII TRS which should be on or 
after the date on which the Offer Shares are listed on the Stock Exchange. Upon the termination upon maturity or early termination of the CGII TRS by the CGII 
Ultimate Client, CGII will dispose of the Offer Shares on the secondary market and the CGII Ultimate Client will receive final settlement amount of the back-to-back 
TRS which should have taken into account all the economic returns or economic loss in relation to the Offer Shares. If upon the maturity of the CGII TRS, the CGII 
Ultimate Client intends to extend the investment period, subject to further agreement between CGII and the CGII Ultimate Client, the term of the CGII TRS could be 
extended by way of a new issuance or a tenor extension. Accordingly, CGII will extend the term of the back-to-back TRS by way of a new issuance or a tenor 
extension. 
It is proposed that CGII will hold the legal title and the voting right of the Offer Shares by itself, and pass through the economic exposure to the CGII Ultimate Client, 
which place CGII TRS orders through their asset manager with CGII in connection with the IPO of the Company. Due to its internal policy, CGII will not exercise 
the voting right of the Offer Shares during the tenor of the back-to-back TRS. 
During the life of the CGII TRS and back-to-back TRS, CGII may continue to hold the Offer Shares in its custodian account, or to hold some or all of the Offer Shares 
in a prime brokerage account for stock borrowing purposes.  
As permitted under the contractual arrangement with the CGII Ultimate Client, CGII will lend out its holding  of underlying Offer Shares in the form of stock 
borrowing loans consistent with market practice to lower its  finance costs, provided that CGII has the ability to call back the Offer Shares on loan at any time in order 
to  satisfy its obligations under the back-to-back TRS to ensure the economic interests to be passed to the CGII  Ultimate Client under the CGII TRS will remain 
unchanged. 
Both CGII and CGIS are indirect wholly owned subsidiaries of CGS, the A shares of which are listed on the Shanghai Stock Exchange (stock code: 601881), the H 
shares of which are listed on the Stock Exchange (stock code: 6881). CGII is a connected client (as defined under Appendix F1 to the Listing Rules) of CGIS, holding 
securities on a non-discretionary basis on behalf of independent third parties. 
The CGII Ultimate Client is Yuanfeng Yuanjing Growth Private Securities Investment Fund(源峰远景成长私募证券投资基金) (“Yuanfeng Yuanjing Fund”), a 
limited partnership established in the PRC, who is managed by Xiamen Yuanfeng Jiying Enterprise Management Partnership (LP). (厦门源峰集英企业管理合伙企
业（有限合伙）). No ultimate beneficial owner of Yuanfeng Yuanjing Fund is holding 30% or more interests in it.  
To the best of CGII’s knowledge after having made all reasonable inquiries, the CGII Ultimate Client is an independent third party of CGII, and the companies which 
are members of the same group of CGIS.  
2. It is proposed that GTJAI participates as placee to subscribe for the Offer Shares under the International Offering (the “GTJAI Subscription”). 
In relation to the GTJAI Subscription, GTJAI shall hold the Offer Shares for hedging purpose as the single  underlying asset of a back-to-back total return swap 
transaction (the “GTHT Back-to-back TRS”) to be entered  into between GTJAI and Guotai Haitong Securities Co., Ltd. (the “GTHT Onshore Parent”) in 

<<<PAGE 23>>>
23 
 
connection  with a total return swap order (the “GTHT Client TRS”) to be entered into by GTHT Onshore Parent and  ultimate client (the “GTHT Onshore Ultimate 
Client”), respectively. Such GTHT Client TRS is to be fully funded by the GTHT Onshore Ultimate Client. GTJAI will hold the Offer Shares on a non-discretionary 
basis for the purpose of hedging the economic exposure under the GTHT Back-to-back TRS and GTHT Client TRS only. During the tenor of the GTHT Client TRS, 
all economic returns of the Offer Shares will be passed to the  GTHT Onshore Ultimate Client and all economic losses shall be borne by the GTHT Onshore Ultimate 
Client,  subject to the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS, and GTJAI will  not take part in any economic return or bear any 
economic loss in relation to the price of the Offer Shares. The GTHT Onshore Ultimate Client may request to redeem the Offer Shares at their own discretion, upon 
which GTJAI shall dispose of the Offer Shares and settle the GTHT Back-to-back TRS and GTHT Client TRS in cash in accordance with the terms and conditions 
of the GTHT Back-to-back TRS and GTHT Client TRS documents.  Due to its internal policy, GTJAI will not exercise the voting right attaching to the Offer Shares 
during the tenor of the GTHT Back-to-back TRS and GTHT Client TRS. 
The GTHT Onshore Ultimate Client is Lingding Hengrui No.9 Private Securities Investment Fund (凌顶恒瑞九号私募证券投资基金) (“Lingding Hengrui No.9”), 
whose ultimate beneficial owner holding 30% or more interest is Zhu Dengjia (祝登甲). The fund manager of Lingding Hengrui No.9 is Ningbo Meishan Bonded 
Port Lingding Investment Management Co., Ltd. (宁波梅山保税港区凌顶投资管理有限公司), which is owned by Deng Chunyan (邓春燕) and Chen Youfang (陈
有方) as to 70% and 30%, respectively. 
To the best of GTJAI’s knowledge after having made all reasonable inquiries, the GTJA Onshore Ultimate Client and the ultimate beneficial owners holding 30% or 
more interest of the GTJA Onshore Ultimate Client listed above is an independent third party of GTJAI, GTJAS, Haitong and the companies which are members of 
the same group of companies as GTJAS and Haitong.  
3. Bosera AM will hold the Offer Shares in its capacity as a discretionary fund manager managing assets on behalf of its underlying clients. 
Name of the sub-funds to which the Offer Shares will be 
allocated 
Whether any investor holds 30% or 
more interests in the sub-fund (Y/N) 
Name of ultimate beneficial owner 
shareholding (%) 
Bosera China New Opportunities Fund SP 
N 
N/A 
N/A 
Bosera Growth Premium Global Equity Strategy Fund SP 
Y 
Guo Feng (郭峰) 
48.9951% 
KB CHINA MAINLAND FD BOSERA 
N 
N/A 
N/A 
Bosera Growth Premium Global Equity Strategy Fund SP2 
Y 
Guangdong Dongfang Precision Science & 
Technology Co.,Ltd  
47.42% 
Bosera Greater China Enhanced Return Bond Fund  (SFC 
Authorised Fund) 
N 
N/A 
N/A 
Bosera Growth Premium Global Equity Strategy Fund SP3 
Y 
HUANG Liya (黄丽亚) 
100% 

<<<PAGE 24>>>
24 
 
Bosera Growth Premium Global Equity Strategy Fund SP4 
Y 
Guangdong Dongfang Precision Science & 
Technology Co.,Ltd  
100% 
  
To the best of knowledge of Bosera AM, the underlying clients of Bosera AM, together with its ultimate beneficial owners, is an independent third party of the 
Company, its subsidiaries, its substantial shareholders, Bosera AM, CMBI and the companies which are members of the same group of CMBI. 
4. Fullgoal Fund is a fund management company established in China in April 1999, and is one of the first ten fund management companies authorized by the CSRC 
and other regulatory authorities to obtain full licenses to provide asset management services in the PRC. It is proposed that Fullgoal Fund participates as placee to 
subscribe for the Offer Shares under the International Offering (the “Fullgoal Subscription”). In relation to the Fullgoal Subscription, Fullgoal Fund will hold the 
Offer Shares in its capacity as the discretionary fund manager on behalf of its investors (the “Fullgoal Ultimate Clients”).  
Fullgoal Fund has confirmed that, to the best of their knowledge, (i) no ultimate beneficial owners of Fullgoal Ultimate Clients are holding 30% or more interests in 
it; (ii) each of the other Fullgoal Ultimate Client and the ultimate beneficial owners of the Fullgoal Ultimate Client is an independent third party of (a) the Company, 
the connected person or the associates thereof; and (b) Fullgoal Fund, GTJAS, Haitong and the companies which are members of the same group of companies as 
GTJAS and Haitong, respectively; and (iii) Fullgoal Fund is a collective investment scheme which is not authorised by the SFC and is expected to hold the Offer 
Shares on behalf of such scheme. 
5. Fullgoal HK is a wholly owned subsidiary of of Fullgoal Fund. Fullgoal HK was established in 2012 in Hong Kong and is licensed for Type 1 (Dealing in Securities), 
Type 4 (Advising on Securities) and Type 9 (Asset Management) regulated activities by the SFC. It is proposed that Fullgoal HK participates as placee to subscribe 
for the Offer Shares under the International Offering (the “Fullgoal HK Subscription”). In relation to the Fullgoal HK Subscription, Fullgoal HK will hold the Offer 
Shares in its capacity as the discretionary fund manager on behalf of its investors (the “Fullgoal HK Ultimate Clients”).  
Fullgoal HK has confirmed that, to the best of their knowledge, (i) no ultimate beneficial owners of Fullgoal HK Ultimate Clients are holding 30% or more interests 
in it; (ii) each of the other Fullgoal HK Ultimate Clients and the ultimate beneficial owners of the Fullgoal HK Ultimate Clients is an independent third party of (a) 
the Company, the connected person or the associates thereof; and (b) Fullgoal HK, GTJAS, Haitong and the companies which are members of the same group of 
companies as GTJAS and Haitong, respectively; and (iii) Fullgoal HK is a collective investment scheme which is not authorised by the SFC and is expected to hold 
the Offer Shares on behalf of such scheme. 
 
 

<<<PAGE 25>>>
25 
 
 
DISCLAIMERS 
 
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) 
and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of 
this announcement, make no representation as to its accuracy or completeness and expressly disclaim any 
liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the 
contents of this announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for 
securities in  the United States. The securities mentioned herein have not been, and will not be, registered 
under the United States Securities Act of 1933, as amended (the “U.S. Securities Act”). The securities may 
not be offered or sold in the United States except pursuant to an exemption from the registration requirements 
of the U.S. Securities Act and in compliance with any applicable state securities laws, or outside the United 
States unless in compliance with Regulation S under the U.S. Securities Act. There will be no public offer of 
securities in the United States. 
The Offer Shares are being offered and sold outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. This announcement is not a prospectus. Potential investors should read the 
Prospectus dated 18 June 2026  issued by Crealights Technology Co., Ltd. for detailed information about the 
Global Offering described below before deciding whether or not to invest in the Shares thereby being offered. 
*Potential investors of the Offer Shares should note that the Overall Coordinator (for itself and on behalf of 
the Hong Kong Underwriter) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the paragraph headed 
“Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – Hong Kong 
Underwriting Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong 
Kong time) on the Listing Date (which is currently expected to be 29 June 2026). 

<<<PAGE 26>>>
– 26 –
PUBLIC FLOAT
Pursuant to Rule 19A.13A of the Listing Rules, assuming that the Over-allotment Option is 
not exercised, based on the Offer Price of HK$114.00 per Offer Share, our expected market 
capitalization upon the Listing is HK$10,208 million, and the minimum prescribed public 
float percentage applicable to our Shares is 15%.
Immediately following the completion of the Global Offering (before any exercise of the 
Over-allotment Option) an aggregate of 45,646,802 H Shares, representing approximately 
50.98% of the issued share capital of our Company will count towards the public float. 
Therefore, the number of H Shares held in public hands is higher than the prescribed 
percentage of H Shares required to be held in public hands of 15% under Rule 19A.13A(1) 
of the Listing Rules.
Based on the Offer Price of HK$114.00 per H Share, the Company satisfies the free float 
requirement under Rule 19A.13C of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering: 
(i) no placee will, individually, be placed more than 10% of the enlarged issued share capital 
of our Company; (ii) there will not be any new substantial Shareholder (as defined in the 
Listing Rules) of our Company; (iii) the three largest public shareholders of the Company 
do not hold more than 50% of the H Shares in public hands at the time of the Listing in 
compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 
300 Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing 
Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Monday, 
June 29, 2026 (Hong Kong time), provided that the Global Offering has become 
unconditional and the right of termination described in the section headed “Underwriting 
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Hong 
Kong Underwriting Agreement — Grounds for Termination” in the Prospectus has not been 
exercised. Investors who trade the H Shares on the basis of publicly available allocation 
details prior to the receipt of H Share certificates or prior to the H Share certificates 
becoming valid evidence of title do so entirely at their own risk.

<<<PAGE 27>>>
– 27 –
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on 
Monday, June 29, 2026 (Hong Kong time), it is expected that dealings in the H Shares on 
the Stock Exchange will commence at 9:00 a.m. on Monday, June 29, 2026 (Hong Kong 
time). The H Shares will be traded in board lots of 50 H Shares each, and the stock code of 
the H Shares will be 1191.
By order of the Board
Crealights Technology Co., Ltd.
Dr. Hu Zhaoyang
Executive Director, Chairman of the Board and 
Chief Executive Officer
Hong Kong, June 26, 2026
Directors of the Company named in the application to which this announcement relates are: (i) Dr. Hu 
Zhaoyang, Mr. Hu Yong, Ms. Zhou Hong, Dr. Sun Xu and Mr. Guo Qingsong as executive directors; (ii) 
Mr. Ng Ho Nam as non-executive director; and (iii) Dr. Xu Haoping, Dr. Wang Fei and Mr. Zhang Wei as 
independent non-executive directors.
