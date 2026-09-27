# 配发结果公告抽取任务：6228.HK PT MERDEKA GOLD RESOURCES Tbk- DRS

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**25/06/2026 22:53**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0625/2026062502338.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6228.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the 
contents of this announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the 
contents of this announcement.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings 
as those defined in the prospectus dated June 17, 2026 (the “Prospectus”) issued by PT MERDEKA GOLD 
RESOURCES Tbk (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. This announcement is not a prospectus. Potential investors should read 
Prospectus for detailed information about the Company and the Global Offering described below before deciding 
whether or not to invest in the Offer HDRs.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for 
securities in the United States or in any other jurisdictions. The securities mentioned herein have not been, and 
will not be, registered under the United States Securities Act of 1933 as amended from time to time (the “U.S. 
Securities Act”) or securities law of any state or other jurisdiction of the United States and may not be offered, 
sold, pledged or otherwise transferred within the United States except in transactions exempt from, or not subject 
to, the registration requirements of the U.S. Securities Act. There will be no public offer of securities in the 
United States. The Offer HDRs are being offered and sold outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, CLSA Limited, as stabilizing manager (the “Stabilizing Manager”), or 
any person acting for it, on behalf of the Underwriters, may over-allocate or effect transactions with a view to 
stabilizing or supporting the market price of the HDRs at a level higher than that which might otherwise prevail 
for a limited period after the Listing Date. However, there is no obligation on the Stabilizing Manager, or any 
person acting for it to conduct any such stabilizing action, which, if commenced, will be done at the sole and 
absolute discretion of the Stabilizing Manager, or any person acting for it, and may be discontinued at any time. 
Any such stabilizing action is required to be brought to an end on the 30th day after the last day for the lodging 
of applications under the Hong Kong Public Offering. Such stabilizing action, if taken, may be effected in all 
jurisdictions where it is permissible to do so, in each case in compliance with all applicable laws, rules and 
regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the 
Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws 
of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the HDRs for 
longer than the stabilization period, which begins on the Listing Date and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering. After this date, when no further 
stabilizing action may be taken, demand for the HDRs, and therefore the price of the HDRs, could fall.
Potential investors of the Offer HDRs should note that the Overall Coordinators (for themselves and on 
behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section 
headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – Hong Kong 
Underwriting Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong 
Kong time) on the Listing Date (which is currently expected to be on Friday, June 26, 2026).

<<<PAGE 2>>>
– 2 –
PT MERDEKA GOLD RESOURCES Tbk
(Incorporated in Republic of Indonesia with limited liability)
GLOBAL OFFERING OF DEPOSITARY RECEIPTS
Number of Offer HDRs under the
Global Offering
:
89,668,600 Sale HDRs (subject to the 
Over-allotment Option)
Number of Hong Kong Offer HDRs
:
8,966,900 Sale HDRs
Number of International Offer HDRs
:
80,701,700 Sale HDRs (subject to the 
Over-allotment Option)
Final Offer Price
:
HK$26.60 per Offer HDR, plus brokerage 
of 1.0%, SFC transaction levy of 
0.0027%, Hong Kong Stock Exchange 
trading fee of 0.00565% and AFRC 
transaction levy of 0.00015%
Nominal Value
:
Nil 
Stock Code
:
6228
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers
Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers 
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
PT MERDEKA GOLD RESOURCES Tbk 
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS 
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated June 17, 2026 (the “Prospectus”) issued by PT Merdeka Gold Resources Tbk (the 
“Company”). 
Warning: In view of high concentration of shareholding in a small number of Shareholders, Shareholders and 
prospective investors should be aware that the price of the HDRs could move substantially even with a small 
number of HDRs traded and should exercise extreme caution when dealing in the HDRs. 
SUMMARY 
Company information 
Stock code 
6228 
Stock short name 
MERDEKAGOLD-DRS 
Dealings commencement date 
26 June 2026* 
*see note at the end of the announcement
Price Information 
Final Offer Price 
HK$26.60 
Maximum Offer Price 
HK$26.60 
Offer HDRs and Share Capital 
Number of Offer HDRs (before exercise of the Over-allotment 
Option) 
89,668,600 
Number of Offer HDRs in Hong Kong Public Offering 
8,966,900 
Number of Offer HDRs in International Offering (before exercise 
of the Over-allotment Option) 
80,701,700 
Number of issued HDRs upon Listing (before exercise of the 
Over-allotment Option) 
89,668,600 
No. of issued Shares upon Listing (before exercise of the Over-
allotment Option) 
14,731,366,060 
Over-allocation 
No. of Offer HDRs over-allocated 
13,450,200 
International Offering 
13,450,200 
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases in the 
secondary market at prices that do not exceed the Offer Price or through deferred delivery or a combination of 
these means. In the event the Over-allotment Option is exercised, an announcement will be made on the Stock 
Exchange’s website. 
Proceeds 
Gross proceeds (Note) 
HK$2,385.18 million 
Less: Estimated listing expenses payable based on Final Offer 
Price 
HK$(116.47) million 
Net proceeds 
HK$2,268.71 million 
Note: The Company will not receive any of the net proceeds from the Global Offering. The Selling Shareholders will
receive all the net proceeds from the Global Offering. In the event of exercise of the Over-allotment Option, the
Selling Shareholders will receive the additional net proceeds. 
– 3 –

<<<PAGE 4>>>
 
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING 
 
No. of valid applications 
22,329 
No. of successful applications 
22,329 
Subscription level  
4.42 times 
Clawback triggered 
N/A 
No. of Offer HDRs initially available under the Hong Kong Public 
Offering 
8,966,900 
No. of Offer HDRs reallocated from the International Offering  
N/A 
Final no. of Offer HDRs under the Hong Kong Public Offering  
8,966,900 
% of Offer HDRs under the Hong Kong Public Offering to the Global 
Offering 
10.00% 
Note: For details of the final allocation of HDRs to the Hong Kong Public Offering, investors can refer to
www.eipo.com.hk/eIPOAllotment to perform a search by identification number or www.eipo.com.hk/eIPOAllotment
for the full list of allottees.  
INTERNATIONAL OFFERING 
 
No. of placees 
98 
Subscription Level  
7.67 times 
No. of Offer HDRs initially available under the International Offering 
80,701,700  
Final no. of Offer HDRs under the International Offering (after 
reallocation) 
80,701,700  
% of Offer HDRs under the International Offering to the Global Offering 90.00% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save  for (a) a waiver from strict compliance 
with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) 
granted by the Stock Exchange to permit the Company to allocate certain Offer HDRs in the International Offering to Existing Minority 
Shareholder and/or their close associates; and (b) a consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants 
to permit the Company to, among other things, allocate further Offer HDRs in the International Offering to the Cornerstone Investors, 
existing shareholders and/or their close associates, (i) none of the Offer HDRs subscribed by the placees and the public have been 
financed directly or indirectly by the Company, any of the Directors, Commissioners, chief executive of the Company, 
controlling shareholders, substantial shareholders, existing shareholders of the Company or any of its subsidiaries or 
their respective close associates; and (ii) none of the placees and the public who have purchased the Offer HDRs are 
accustomed to taking instructions from the Company, any of the Directors, Commissioners, chief executive of the Company, 
controlling shareholders, substantial shareholders, existing shareholders of the Company or any of its subsidiaries or 
their respective close associates in relation to the acquisition, disposal, voting or other disposition of HDRs registered in 
his/her/its name or otherwise held by him/her/it. 
– 4 –

<<<PAGE 5>>>
Cornerstone Investors 
 
 
 
 
 
 
 
Investor 
No. of Offer 
HDRs 
allocated 
 
 
 
 
 
 
% of Offer 
HDRs Note 1 
 
 
 
 
% of total issued 
HDRs after the 
Global Offering Note 1  
 
 
 
 
% of total issued 
share capital 
after the Global 
Offering Note 1 
Existing 
shareholders 
or their close 
associates 
Ping An of China 
Asset Management 
(Hong Kong) 
Company Limited / 
(中國平安人壽保險
股份有限公司) 
(“Ping An AM”) 
8,838,200 
9.86% 
9.86% 
0.60% 
No 
Wanguo Gold Group 
Limited (“Wanguo”) 
5,892,100 
6.57% 
6.57% 
0.40% 
No 
Glencore 
International AG 
(“Glencore AG”) 
5,892,100 
6.57% 
6.57% 
0.40% 
No 
Mercuria Holdings 
(Singapore) Pte. Ltd. 
(“Mercuria”) 
5,892,100 
6.57% 
6.57% 
0.40% 
No 
Trafigura Pte. Ltd. 
(“Trafigura Group”) 
5,892,100 
6.57% 
6.57% 
0.40% 
No 
Intera Mining 
Investment Limited 
(“Intera Mining”) 
2,946,000 
3.29% 
3.29% 
0.20% 
No 
GF Fund 
Management Co., 
Ltd. and GF 
International 
Investment 
Management Limited 
(together, “GF 
Fund”) 
2,946,000 
3.29% 
3.29% 
0.20% 
No 
CNGR Hong Kong 
Material Science & 
Technology Co., 
Limited (“CNGR”) 
2,062,200 
2.30% 
2.30% 
0.14% 
Yes 
Eurus Holdings SPC 
(“ORIX”) 
1,473,000 
1.64% 
1.64% 
0.10% 
No 
Wind Sabre Fund 
SPC (“Wind Sabre”) 
1,473,000 
1.64% 
1.64% 
0.10% 
No 
Dymon Asia Multi-
Strategy Investment 
Master Fund 
(“DAMSIMF”) 
1,473,000 
1.64% 
1.64% 
0.10% 
No 
Subtotal 
44,779,800 
49.94% 
49.94% 
3.04% 
– 5 –

<<<PAGE 6>>>
Notes: 
1. 
Assuming the Over-allotment Option is not exercised. 
2. 
For further details of the cornerstone investors, please refer to the section headed “Cornerstone Investors” of 
the Prospectus. 
3. 
In addition to the Offer HDRs subscribed for as Cornerstone Investors, GF Fund, CNGR, Wind Sabre, ORIX 
and DAMSIMF were allocated further Offer HDRs as placees in the Internation Offering. Please refer to the 
section headed “Allotment Results Details – International Offering – Allottees with Waivers/Consents 
Obtained” in this announcement for details. Only the Offer HDRs subscribed for as Cornerstone Investors are 
subject to lock-up as indicated below. For details, please refer to the section headed “Lock-up Undertakings – 
Cornerstone Investors” in this announcement.  
 
– 6 –

<<<PAGE 7>>>
Allottees with Waivers/Consents Obtained 
 
 
 
 
 
 
 
 
 
Investor 
No. of 
Offer HDRs 
allocated 
 
 
 
 
 
 
 
% of Offer 
HDRs 
 
 
 
% of total 
issued HDRs 
after the 
Global 
Offering upon 
listing Note 2 
 
 
 
 
 
% of 
shareholding in 
the Company 
upon listing  
 
 
Relationship 
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under  paragraph 1C(2)
of the Placing Guidelines in relation to allocations to close associate of an existing shareholder as cornerstone investor 
Note 1 
CNGR 
2,062,200 
2.30% 
2.30% 
0.14% 
A Cornerstone 
Investor and a 
close associate of  
an Existing 
Minority 
Shareholder 
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocations of further HDRs to existing Shareholders and Cornerstone Investors and/or their respective close 
associates Note 3   
CNGR 
885,000 
0.99% 
0.99% 
0.06% 
A Cornerstone 
Investor and a 
close associate of  
an Existing 
Minority 
Shareholder 
GF Fund 
5,900,000 
6.58% 
6.58% 
0.40% 
A Cornerstone 
Investor  
Wind Sabre 
1,473,000 
1.64% 
1.64% 
0.10% 
A Cornerstone 
Investor  
Orix 
590,000 
0.66% 
0.66% 
0.04% 
A Cornerstone 
Investor  
DAMSIMF 
1,473,000 
1.64% 
1.64% 
0.10% 
A Cornerstone 
Investor  
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and  Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients  
CITIC Securities 
International Capital 
Management Limited 
(“CSI”)Note 4 
 
1,170,00 
1.30% 
1.30% 
0.01% 
Connected client 
CITIC Securities Asset 
Management Company
35,000 
0.04% 
0.04% 
0.002% 
Connected client 
– 7 –

<<<PAGE 8>>>
Limited (“CITIC 
AM”)Note 4 
 
CITIC Securities Asset 
management (HK) 
Limited (“CITIC AM 
HK”) Note 4 
 
112,000 
0.12% 
0.12% 
0.008% 
Connected client 
Bosera Asset 
Management 
(International) 
Co., Ltd. 
(“Bosera AM”) 
Note 4 
1,561,300 
1.74% 
1.74% 
0.11% 
Connected client 
China Asset 
Management (Hong 
Kong) Limited 
(“China AMC 
HK”) Note 4 
295,000 
0.33% 
0.33% 
0.02% 
Connected client 
AEGON-Industrial 
Fund Management 
Co., Ltd. (“AEGON”) 
Note 4 
 
29,400 
0.03% 
0.03% 
0.002% 
Connected client 
Notes: 
1. For details of the consent under paragraph 1C(2) of the Placing Guidelines in relation to allocations to 
existing shareholder, please refer to the section headed “Waivers and Exemptions – Allocation of the HDRs 
to existing shareholders and/or their close associates as cornerstone investors or placees” in the Prospectus. 
 
2. Assuming the Over-allotment Option is not exercised. 
 
3. The Stock Exchange has granted a consent under paragraph 18 of Chapter 4.15 of the Guide to permit HDRs 
in the International Offering to be placed to close associates of existing shareholders as a cornerstone 
investor and to cornerstone investors and/or their respective close associates as placees. For details of the 
consent under paragraph 18 of Chapter 4.15 of the Guide in relation to allocations to close associate of 
existing shareholders and cornerstone investors and/or their respective close associates, please refer to the 
section headed “Others/Additional Information – Allocations of Offer HDRs to cornerstone investors and/or 
their respective close associates as placees with a consent under Paragraph 18 of Chapter 4.15 of the Guide” 
of this announcement. 
 
4. For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients, please refer to the section headed 
“Others/Additional Information – Placing to connected clients with a prior consent under paragraph 1C(1) 
of the Placing Guidelines” of this announcement. 
 
– 8 –

<<<PAGE 9>>>
 
 
LOCK-UP UNDERTAKINGS 
 
Controlling Shareholder 
 
 
 
 
 
 
 
Name  Note 1 
 
 
 
 
 
 
 
Number of Shares 
held in the 
Company subject 
to lock-up 
undertakings upon 
listing 
 
 
 
 
 
 
 
% of total issued 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
listing  
 
 
 
 
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
listing  
 
 
 
 
 
 
Last day subject to 
the lock-up 
undertakings 
Note( 2)(3) 
PT Merdeka Copper 
Gold Tbk 
9,329,376,465 
63.33% 
63.33% 
25 June 2027 
Subtotal 
9,329,376,465 
63.33% 
63.33% 
Notes: 
1. Please refer to the section headed “History and Corporate Structure – Capitalization of our 
Company” in the Prospectus for further details. 
2. The required lock-up for the first six-month period ends on December 25, 2026 and for the second six-
month period ends on June 25, 2027. 
3. The expiry date of the lock-up period shown in the table above is pursuant to the relevant lock-up 
undertakings. 
 
 
  
  
  
– 9 –

<<<PAGE 10>>>
Selling Shareholders 
 
 
Name Note 1 
 
 
 
 
Number of Shares 
held in the 
Company subject to 
lock-up 
undertakings upon 
listing 
 
 
 
 
% of total 
issued Shares 
after the 
Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing 
Note 2 
 
 
 
 
Assuming full 
exercise of the 
Over-
allotment 
Option, 
number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon listing 
 
 
 
 
Assuming full 
exercise of the 
Over-allotment 
Option, % of total 
issued Shares 
after the Global 
Offering subject 
to lock-up 
undertakings 
upon listing Note 2 
 
 
 
 
 
Last day 
subject to the 
lock-up 
undertakings 
Note 3 
Continuum SPC (acting 
on behalf of and for the 
account of Infinity Fund 
SP) 
253,683,100 
1.72% 
225,601,100 
1.53% 
23 December 
2026 
Mr. Winato Kartono 
548,772,817 
3.73% 
472,429,817 
3.21% 
23 December 
2026 
PT Nugraha Eka 
Kencana 
148,791,665 
1.01% 
128,789,665 
0.87% 
23 December 
2026 
PT Unitras Kapital 
Indonesia 
74,949,360 
0.51% 
64,874,360 
0.44% 
23 December 
2026 
PT Nusantara Indah 
Cemerlang 
199,540,600 
1.35% 
199,540,600 
1.35% 
23 December 
2026 
Mr. Hardi Wijaya Liong 
202,470,351 
1.37% 
202,470,351 
1.37% 
23 December 
2026 
PT Bintang Delapan 
Harmoni 
168,441,300 
1.14% 
168,441,300 
1.14% 
23 December 
2026 
Mr. Edi Permadi 
79,926,165 
0.54% 
79,926,165 
0.54% 
23 December 
2026 
Mr. Alexander Ramlie 
72,234,000 
0.49% 
72,234,000 
0.49% 
23 December 
2026 
Sherman Mineral Trading 
Co., Limited 
79,315,200 
0.54% 
79,315,200 
0.54% 
23 December 
2026 
GEM Hong Kong 
International Co., 
Limited 
19,071,000 
0.13% 
19,071,000 
0.13% 
23 December 
2026 
PT Deze Trading 
Indonesia 
19,111,000 
0.13% 
19,111,000 
0.13% 
23 December 
2026 
Subtotal 
1,866,306,558 
12.67% 
1,731,804,558 
11.76% 
– 10 –

<<<PAGE 11>>>
Notes: 
1. Please refer to the section headed “Summary – Selling Shareholders and Over-Allotment Option Grantors” in 
the Prospectus for further details. 
2. The percentages are calculated based on the total issued and fully paid-up capital of 14,731,366,060 Shares as 
of the Latest Practicable Date. 
3. The expiry date of the lock-up period (180 days from the date of listing) shown in the table above is pursuant to 
the selling shareholder undertakings. 
 
 
– 11 –

<<<PAGE 12>>>
 
Cornerstone Investors 
 
Name 
Number of HDRs 
held in the 
Company subject 
to lock-up 
undertakings upon 
listing 
 
 
 
% of total issued 
HDRs after the 
Global Offering 
subject to lock-up 
undertakings upon 
listing Note 1 
 
 
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
listing  
 
Last day subject 
to the lock-up 
undertakings Note 2 
Ping An AM 
8,838,200 
9.86% 
0.60% 25 December 2026 
Wanguo 
5,892,100 
6.57% 
0.40% 25 December 2026 
Glencore AG 
5,892,100 
6.57% 
0.40% 25 December 2026 
Mercuria 
5,892,100 
6.57% 
0.40% 25 December 2026 
Trafigura Group 
5,892,100 
6.57% 
0.40% 25 December 2026 
Intera Mining 
2,946,000 
3.29% 
0.20% 25 December 2026 
GF Fund 
2,946,000 
3.29% 
0.20% 25 December 2026 
CNGR 
2,062,200 
2.30% 
0.14% 25 December 2026 
ORIX 
1,473,000 
1.64% 
0.10% 25 December 2026 
Wind Sabre 
1,473,000 
1.64% 
0.10% 25 December 2026 
DAMSIMF  
1,473,000 
1.64% 
0.10% 25 December 2026 
Subtotal 
44,779,800 
49.94% 
3.04% 
Notes: 
1. Assuming the Over-allotment Option is not exercised. 
2. In accordance with the relevant cornerstone investment agreement, the required lock-up ends on 25 
December 2026 (six months from the date of listing). The Cornerstone Investor will cease to be prohibited 
from disposing of or transferring HDRs subscribed for pursuant to the relevant cornerstone investment 
agreement after the indicated date. 
– 12 –

<<<PAGE 13>>>
PLACEE CONCENTRATION ANALYSIS** 
 
Placees 
Number of HDRs 
allotted 
 
Allotment as % of 
International Offering 
(assuming no exercise of the 
Over-allotment Option)  
Allotment as % of 
International Offering 
(assuming the Over-allotment 
Option is exercised) 
Allotment as % of total Offer 
HDRs (assuming no exercise of 
the Over- allotment Option) 
Allotment as % of total 
Offer HDRs (assuming the 
Over-allotment Option is 
exercised) 
Number of 
 HDRs held upon Listing 
 
% of total issued capital upon 
Listing (assuming no exercise of 
the Over-allotment Option) 
·% of total issued capital upo
n Listing (assuming the Over-
allotment Option is exercised)
  
Top 1 
8,846,000 
10.96% 
9.40% 
9.87% 
8.58% 
8,846,000 
0.60% 
0.60% 
Top 5 
35,368,400 
43.83% 
37.57% 
39.44% 
34.30% 
35,368,400 
2.40% 
2.40% 
Top 10 
55,998,800 
69.39% 
59.48% 
62.45% 
54.31% 
55,998,800 
3.80% 
3.80% 
Top 25 
81,185,800 
100.60% 
86.23% 
90.54% 
78.73% 
81,185,800 
5.51% 
5.51% 
 Notes 
* Ranking of placees is based on the number of HDRs allotted to the placees. 
HDR HOLDERS CONCENTRATION ANALYSIS** 
 
HDR 
Holders* 
Number of HDRs allotted 
Allotment as % of 
International Offering 
(assuming no exercise of the 
Over-allotment Option)  
Allotment as % of 
International Offering 
(assuming the Over-
allotment Option is 
exercised) 
Allotment as % of total 
Offer HDRs (assuming no 
exercise of the Over- 
allotment Option) 
Allotment as % of total 
Offer HDRs (assuming the 
Over-allotment Option is 
exercised) 
Number of HDRs held upon Listing 
% of total issued  
capital upon Listing 
(assuming no 
exercise of the Over-
allotment Option) 
% of total 
issued capital 
upon Listing 
(assuming the 
Over-allotment 
Option is 
exercised) 
Number of HDRs held upon Listing 
 
 Top 1 
   
8,846,000  
10.96% 
9.40% 
9.87% 
8.58% 
    
8,846,000 
0.60% 
0.60% 
    
8,846,000 
 Top 5 
   
35,368,400  
43.83% 
37.57% 
39.44% 
34.30% 
    
35,368,400 
2.40% 
2.40% 
    
35,368,400 
 Top 10 
   
55,998,800 
69.39% 
59.48% 
62.45% 
54.31% 
    
55,998,800 
3.80% 
3.80% 
    
55,998,800 
 Top 25 
   
81,400,900 
100.87% 
86.46% 
90.78% 
78.94% 
    
81,400,900 
5.53% 
5.53% 
    
81,400,900 
  
Notes 
– 13 –

<<<PAGE 14>>>
* Ranking of  Shareholders is based on the number of HDRs (of all classes) held by the HDR holders upon Listing. 
 
 
SHAREHOLDER CONCENTRATION ANALYSIS** 
 
Shareholders 
Number of HDRs 
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
exercised) 
Allotment as % of total 
Offer HDRs (assuming no 
exercise of the Over- 
allotment Option)  
Allotment as % of total 
Offer HDRs (assuming the 
Over-allotment Option is 
exercised)  
Number of HDRs held 
upon Listing (or 
equivalent Shares based 
on HDR conversion ratio) 
Number of HDRs held 
upon Listing (or 
equivalent Shares based 
on HDR conversion ratio) 
% of total issued capital 
upon Listing (assuming no 
exercise of the Over-
allotment Option) 
% of total issued capital 
upon Listing (assuming 
the Over-allotment 
Option is exercised)  
Top 1 
    
-    
0.00% 
0.00% 
0.00% 
0.00% 
    
932,937,646  
    
932,937,646  
63.33% 
63.33% 
Top 5 
    
-    
0.00% 
0.00% 
0.00% 
0.00% 
    
1,064,679,339  
    
1,064,679,339  
72.27% 
72.27% 
Top 10 
    
-    
0.00% 
0.00% 
0.00% 
0.00% 
    
1,157,323,893  
    
1,157,323,893  
78.56% 
78.56% 
Top 25 
    
41,260,500 
51.13% 
43.82% 
46.01% 
40.01% 
    
1,289,552,527  
    
1,289,552,527  
87.54% 
87.54% 
  
Notes 
* Ranking of Shareholders is based on the number of HDRs (of all classes) held by the Shareholder upon Listing. 
 
– 14 –

<<<PAGE 15>>>
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 22,329 valid applications 
made by the public will be conditionally allocated on the basis set out below: 
 
NO. OF 
HDRS 
APPLIED 
FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF ALLOTMENT/BALLOT 
APPROXIMATE 
PERCENTAGE 
ALLOTED OF 
THE TOTAL NO. 
OF HDRS 
APPLIED FOR 
POOL A 
100 
12,500 
100 HDRs 
100.00% 
200 
1,854 
100 HDRs plus 742 out of 1,854 to receive additional 100 HDRs 
70.01% 
300 
3,753 
100 HDRs plus 2,532 out of 3,753 to receive additional 100 HDRs 
55.82% 
400 
617 
200 HDRs 
50.00% 
500 
442 
200 HDRs plus 177 out of 442 to receive additional 100 HDRs 
48.01% 
600 
130 
200 HDRs plus 91 out of 130 to receive additional 100 HDRs 
45.00% 
700 
81 
200 HDRs plus 65 out of 81 to receive additional 100 HDRs 
40.04% 
800 
107 
200 HDRs plus 94 out of 107 to receive additional 100 HDRs 
35.98% 
900 
74 
200 HDRs plus 70 out of 74 to receive additional 100 HDRs 
32.73% 
1,000 
1,302 
300 HDRs 
30.00% 
2,000 
315 
400 HDRs 
20.00% 
3,000 
273 
500 HDRs 
16.67% 
4,000 
138 
600 HDRs 
15.00% 
5,000 
109 
700 HDRs 
14.00% 
6,000 
42 
800 HDRs 
13.33% 
7,000 
32 
900 HDRs 
12.86% 
8,000 
39 
1,000 HDRs 
12.50% 
9,000 
25 
1,100 HDRs 
12.22% 
10,000 
194 
1,200 HDRs 
12.00% 
20,000 
103 
1,800 HDRs 
9.00% 
30,000 
44 
2,400 HDRs 
8.00% 
40,000 
30 
3,000 HDRs 
7.50% 
50,000 
14 
3,600 HDRs 
7.20% 
60,000 
8 
4,200 HDRs 
7.00% 
70,000 
9 
4,800 HDRs 
6.86% 
80,000 
15 
5,400 HDRs 
6.75% 
90,000 
3 
6,000 HDRs 
6.67% 
100,000 
34 
6,600 HDRs 
6.60% 
Total: 
22,287 
Total number of Pool A successful applicants:22,287 
 
 
 
 
 
POOL B 
200,000 
25 
50,000 HDRs 
25.00% 
300,000 
8 
74,800 HDRs 
24.93% 
400,000 
3 
99,300 HDRs 
24.83% 
500,000 
2 
124,000 HDRs 
24.80% 
1,000,000 
2 
247,500 HDRs 
24.75% 
2,000,000 
1 
494,000 HDRs 
24.70% 
4,483,400 
1 
1,100,100 HDRs 
24.54% 
Total: 
42 
Total number of Pool B successful applicants: 42 
 
– 15 –

<<<PAGE 16>>>
As of the date of this announcement, the relevant subscription monies previously deposited in the designated nominee 
accounts have been remitted back to the accounts of all HKSCC participants. Investors should contact their 
relevant brokers for any inquiries. 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors and the Commissioners confirm that, except for the Listing Rules that have been waived and/or in 
respect of which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s HDRs. 
The Directors and the Commissioners confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer HDR purchased by them was the same as the 
final Offer Price in addition to any brokerage, AFRC transaction levy, SFC transaction levy and Stock Exchange 
trading fee payable. 
The Directors confirm that, immediately following completion of the Global Offering (before any exercise of the Over-
allotment Option): (i) the HDRs will be held by at least 300 HDR holders at the time of Listing, in compliance with 
Rule 8.08(2) of the Listing Rules; (ii) the three largest public HDR holders will not hold more than 50% of the HDRs 
held in public hands at the  time of Listing, in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; (iii) no 
placee will, individually, be placed more than 10% of the issued share capital of the Company  immediately after the 
Global Offering; and (iv) there will not be any new substantial HDR holder (as defined in the Listing Rules) 
immediately after the Global Offering. 
 
OTHERS / ADDITIONAL INFORMATION 
 
Allocations of Offer HDRs to cornerstone investors and/or their respective close associates as placees with a 
consent under Paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants  
 
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph  18 of Chapter 4.15 of the 
Guide for New Listing Applicants to permit the Company to allocate further Offer HDRs in the International Offering to 
certain existing Shareholders and Cornerstone  Investors and/or their close associates as placees, subject to the following 
conditions (“Allocation to Size-based Exemption Participants”): 
 
(a) the final offering size of the Global Offering, excluding any over-allocation will be of a total value of at least 
HK$1 billion; 
 
(b) the HDRs allocated to all existing Shareholders and their close associates (whether as Cornerstone Investors 
and/or as placees) as permitted under this exemption do not exceed 30% of the total number of HDRs offered 
under the Global Offering;  
 
(c) each of the Directors, commissioners, chief executives and the Controlling Shareholder of the Company has 
confirmed that no HDRs have been allocated to them or their respective close associates under this exemption; 
  
(d) details of the Allocation to the Size-based Exemption Participants will be disclosed in this announcement; and 
 
(e) each Size-based Exemption Participant is not a Selling Shareholder. 
 
Such allocations of Offer HDRs are in compliance with all the conditions under the consent granted by the Stock 
Exchange. 
 
For details of the allocations of Offer HDRs to Cornerstone Investors, please refer to the section headed “Allotment 
Results Details – International Offering – Allotees with Waivers/Consents Obtained” in this announcement. 
 
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines 
 
Under the International Offering, certain Offer HDRs were placed to connected clients of their connected distributors 
pursuant to the Placing Guidelines. Please refer to the section headed “Allotment Results Details – International Offering 
– 16 –

<<<PAGE 17>>>
– Allotees with Waivers/Consents Obtained” in this announcement for details. The Company has applied to the Stock 
Exchange for, and the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing Guidelines to permit 
the Company to allocate such Offer HDRs in the International Offering to the connected clients. The allocation of Offer 
HDRs to such connected clients is in compliance with all the conditions (pursuant to paragraph 6 of Chapter 4.15 of the 
Guide for New Listing Applicants) under the consent granted by the Stock Exchange. 
 Details of the placement to connected clients are set out below. 
– 17 –

<<<PAGE 18>>>
 
Part A – Connected Clients holding the beneficial interest of the Offer HDRs on a non-discretionary basis on behalf of independent third parties 
 
No. 
Connected 
Distributor 
Connected Client 
Relationship 
with the 
Connected 
Distributor 
Identities of the 
ultimate 
beneficial 
owners of the 
Offer HDRs or, 
where 
applicable, 
details of the 
structured 
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
scheme which 
is not 
authorised by 
the SFC or is 
expected to 
hold the Offer 
HDRs on 
behalf of such 
scheme  
 
Number of 
Offer HDRs 
allocated to the 
connected client 
Appropriate 
percentage of 
total number of 
Offer HDRs 
(assuming the 
Over-allotment 
Option is not 
exercised) 
Approximate 
percentage of total 
Shares in issue 
immediately 
following the 
completion of Global 
Offering  
1. 
CLSA Limited 
CITIC Securities 
International Capital 
Management Limited 
(“CSI”) 
CSI is a member 
of the same 
group of 
companies as 
CLSA. 
Please refer to 
Note 1 
No 
1,170,000 
1.30% 
0.08%  
 
– 18 –

<<<PAGE 19>>>
Part B – Connected Clients holding the beneficial interest of the Offer HDRs on a discretionary basis on behalf of independent third parties 
 
 
No. Connected Distributor 
Connected Client 
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
the Offer HDRs 
on behalf of such 
scheme  
Maximum 
number of Offer 
HDRs (rounded 
down to nearest 
whole board lot 
of 100 HDRs) to 
be allocate to the 
connected client 
Approximate 
percentage of 
total number of 
Offer HDRs 
(assuming the 
Over-allotment 
Option is not 
exercised) 
Approximate 
percentage of 
total Shares in 
issue immediately 
following the 
completion of 
Global Offering  
1.  CLSA Limited 
CITIC Securities Asset 
Management Company Limited 
(“CITIC AM”) 
 
CLSA and CITIC AM, 
are members of the 
same group of 
companies. 
Yes 
35,000 
0.04%  
0.002%  
2.  CLSA Limited 
CITIC Securities Asset 
management (HK) Limited 
(“CITIC AM HK”) 
 
CITIC AM HK is a 
member of the same 
group of companies as 
CLSA. 
No 
112,000 
0.12%  
0.008% 
3.  CMB International Securities 
Limited (“CMBI”) 
 
and 
 
China Merchants Securities 
(HK) Co., Limited (“CMS”) 
 
Bosera Asset Management 
(International) Co., Ltd 
(“Bosera AM”) 
Bosera AM is a 
member of the same 
group with CMBI and 
CMS. 
 
Yes 
1,561,300 
1.74%  
0.11% 
4.  CLSA Limited 
China Asset Management 
(Hong Kong) Limited (“China 
AMC HK”) 
 
China AMC HK is a 
member of the same 
group of companies as 
CLSA 
No 
295,000 
0.33%  
0.02%  
5.  China Industrial Securities 
International Brokerage Limited 
(“CISI”) 
 
AEGON-Industrial Fund 
Management Co., Ltd 
(“AEGON”) 
 
CISI is the controlling 
shareholder of 
AEGON 
Yes 
29,400 
0.03%  
0.002%  
 
 
 
– 19 –

<<<PAGE 20>>>
Notes: 
1. 
 
CSI will hold the Offer HDRs as a placee under the International Offering on behalf of its ultimate clients (the “CSI Ultimate Clients”), on a non-discretionary basis, pursuant 
to which: (i) CSI will act as the single counterparty of the CSI Back-to-back TRS (the “CSI Back-to-back TRS”) to be entered into by it in connection with a total return swap 
order (the “CSI Client TRS”) placed and fully funded by the CSI Ultimate Clients, by which CSI will pass the full economic exposure of the Offer HDRs placed to CSI to the 
CSI Ultimate Clients; (ii) as confirmed by CSI and CLSA, CSI will hold the legal title and beneficial interest in the Offer HDRs, but will contractually agree to pass on the full 
economic exposure and return of the Offer HDRs to the CSI Ultimate Clients, on a non-discretionary basis. The CSI Ultimate Clients may exercise their early termination rights 
to terminate the CSI Client TRS at any time from the trade date of the CSI Client TRS which should be on or after the date on which the Offer HDRs are listed on the Stock 
Exchange; (iii) upon the final maturity or termination of the CSI Client TRS by the CSI Ultimate Clients, CSI will dispose of the Offer HDRs on the secondary market and the 
CSI Ultimate Clients will receive a final termination amount of the CSI Back-to-back TRS which will have taken into account all the economic returns or economic loss in 
relation to the Offer HDRs and the fixed amount of transaction fees of the CSI Back-to-back TRS and the CSI Client TRS. Due to its internal policy, CSI will not exercise the 
voting right of the Offer HDRs during the terms of the CSI Back-to-back TRS; and (iv) CSI is not a collective investment scheme which is not authorized by the SFC, nor is 
expected to hold the Offer HDRs on behalf of such scheme. 
 
The details of the CSI Ultimate Clients are as follows:  
 
Name of CSI Ultimate Clients 
Fund Manager / General Partner 
Ultimate beneficial owners of Fund 
Manager / General Partner 
Limited partner / Shareholding 
holding 30% or more in the CSI 
Ultimate Clients 
Panshi 
Phase 
II 
Private 
Equity 
Investment Fund No. 1 
(盘世2期私募证劵投资基金1号) 
Shanghai 
Panjing 
Investment 
Management 
Center 
(Limited 
Partnership) 
(上海盘京投资管理中心(有限合伙)) 
Zhuang Tao (庄涛), a natural person 
None of the limited partners holds more 
than 30% interest in the respective CSI 
Ultimate Clients  
Panshi 
Phase 
II 
Private 
Equity 
Investment Fund No. 2 
(盘世2期私募证劵投资基金2号) 
Panshi 
Phase 
II 
Private 
Equity 
Investment Fund No. 3 
(盘世2期私募证劵投资基金3号) 
Panshi 
Phase 
II 
Private 
Equity 
Investment Fund No. 4 
(盘世2期私募证劵投资基金4号) 
Panshi 
Phase 
II 
Private 
Equity 
Investment Fund No. 5 
(盘世2期私募证劵投资基金5号) 
Panshi 
Phase 
II 
Private 
Equity 
Investment Fund No. 1 
(盘世2期私募证劵投资基金6号) 
Panshi 
Phase 
II 
Private 
Equity 
Investment Fund No. 1 
(盘世2期私募证劵投资基金7号) 
Panshi 
Phase 
II 
Private 
Equity 
Investment Fund No. 1 
(盘世2期私募证劵投资基金8号) 
 
To the best of knowledge of CSI and having made all reasonable inquiries, each of the CSI Ultimate Clients and its ultimate beneficial owners is an independent third party of 
the Company, its subsidiaries, its substantial shareholders, CSI, CLSA and the companies which are members of the same group of companies as CLSA. 
 
2. 
 
CITIC AM will hold the Offer HDRs in its capacity as the discretionary fund manager managing the funds on behalf of their investors, each of which is an independent third 
party. 
 
– 20 –

<<<PAGE 21>>>
The funds are as follows: (i) CITIC SECURITIES COMPANY LIMITED-XINHANG ZHIYUAN NO.1 (中信证券信航致远1号集合资产管理计划 ), and (ii) CITIC 
SECURITIES COMPANY LIMITED-XINHANG ZHIYUAN NO.3 (中信证券信航致远3号集合资产管理计划 ). 
 
None of the ultimate clients of CITIC AM holds more than 30% ultimate beneficial interest in the aforementioned funds, and all of them with discretionary management. 
 
3. 
 
CITIC AM HK will hold the Offer HDRs in its capacity as the discretionary fund manager managing the funds on behalf of their investors, each of which is an independent third 
party.  
 
The funds are as follows:  
(i) CITIC Securities Asset Management (HK) Limited – Meta Chance2, invested 100% by Meta Chance Limited, of which the only ultimate beneficial owner holding 30% or 
more interest is Song Ke, a natural person; 
(ii) CITIC Securities Asset Management (HK) Limited – CLSA CT Limited Sub Account 33, invested 100% by Sino Biopharmaceutical Limited (1177.HK), of which no 
beneficial owner holds 30% or more interest; and 
(iii) ICBC (ASIA) LTD-CITIC SECURITIES AM LTD-BSCOMC LTD, invested 100% by BSCOMC Limited, of which the only ultimate beneficial owner holding 30% or 
more interest is State-owned Assets Supervision and Administration Commission of People's Government of Beijing Municipality. 
 
4. 
 
Bosera AM will hold the Offer HDRs in its capacity as the discretionary fund manager managing the sub-funds on behalf of the following clients, each of which is an independent 
third party of the Company, its subsidiaries, its substantial shareholders, CMBI, CMS and the companies which are members of the same group of companies as CMBI and 
CMS.  
 
Name of the sub-funds to which the Offer 
HDRs will be allocated 
Whether any investor holds 30% or more 
interests in the sub-fund (Y/N) 
Name of ultimate beneficial owner 
Shareholding % 
Bosera China New Opportunities Fund SP 
N 
N/A 
N/A 
Bosera Growth Premium Global Equity 
Strategy Fund SP 
Y 
Guo Feng (郭峰) 
48.9951% 
Bosera Growth Premium Global Equity 
Strategy Fund SP2 
Y 
Guangdong Dongfang Precision Science & 
Technology Co., Ltd 
47.42% 
Bosera Growth Premium Global Equity 
Strategy Fund SP3 
Y 
HUANG Liya (黄丽亚) 
100% 
Bosera Growth Premium Global Equity 
Strategy Fund SP4 
Y 
Guangdong Dongfang Precision Science & 
Technology Co., Ltd 
100% 
5. 
 
China AMC HK is an investment advisor and a delegate of the investment manager of its underlying clients (“China AMC HK Ultimate Clients”) and manages assets (in its 
capacity as an investment advisor of the China AMC HK Ultimate Clients) and executes trades (in its capacity as a delegate of the investment manager of China AMC HK 
Ultimate Clients) for on behalf of: 
 
(i) CHINAAMC SELECT GREATER CHINA TECHNOLOGY FUND, of which the only limited partner holding 30% or more interest is Futu Securities International (Hong 
Kong) Limited-Client account, which is a distributor of this fund; 
(ii) CHINAAMC FUND - CHINAAMC CHINA OPPORTUNITIES FUND, of which no beneficial owner holds 30% or more interest; 
(iii) CHINAAMC CHINA GROWTH FUND (SICAV), of which the only ultimate beneficial owner holding 30% or more interest is Yuanta Financial Holdings Co. Ltd; and 
(iv) ICBC (ASIA) LTD-CHINAAMC-BSCOMC LTD, invested 100% by BSCOMC Limited, of which the only ultimate beneficial owner holding 30% or more interest is 
State-owned Assets Supervision and Administration Commission of People's Government of Beijing Municipality. 
 
To the best knowledge of China AMC HK after making all reasonable enquiries, (i) each of the China AMC HK Ultimate Clients is an independent third party of the Company, 
its subsidiaries, its substantial shareholders, CLSA, China AMC HK and the companies which are members of the same group of companies as CLSA; and (ii) China AMC HK 
is not a collective investment scheme which is not authorised by the SFC.  
 
6. 
 
AEGON will hold the Offer HDRs in its capacity as the discretionary fund manager managing the sub-funds on behalf of the following clients, each of which is an independent 
third party of the Company, its subsidiaries, its substantial shareholders, AEGON, CISI, and the companies which are members of the same group of companies as AEGON and 
CISI: 
 
(i) AIFMC ANYUE NO.1 QDII COLLECTIVE ASSET MANAGEMENT PLAN, of which no beneficial owner holds 30% or more interest; and 
– 21 –

<<<PAGE 22>>>
(ii) AEGON-INDUSTRIAL C017 SINGLE ASSET MANAGEMENT PLAN, invested 100% by Wangsu Science & Technology Co., Ltd. (网宿科技股份有限公司), of which 
no beneficial owner holds 30% or more interest.  
 
 
 
 
 
– 22 –

<<<PAGE 23>>>
 
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
The Offer HDRs are being offered and sold outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. This announcement is not a prospectus. Potential investors should read the 
Prospectus dated June 17, 2026  issued by PT Merdeka Gold Resources Tbk for detailed information about the 
Global Offering described below before deciding whether or not to invest in the HDRs thereby being offered. 
*Potential investors of the Offer HDRs should note that the Overall Coordinators (for themselves and on 
behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the 
paragraph headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering 
– Hong Kong Underwriting Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 
a.m. (Hong Kong time) on the Listing Date (which is currently expected to be June 26, 2026). 
 
 
 
– 23 –

<<<PAGE 24>>>
– 24 –
COMMENCEMENT OF DEALINGS
The HDR certificates will only become valid evidence of title at 8:00 a.m. on Friday, June 
26, 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Hong Kong Underwriting 
Agreement – Grounds for Termination” in the Prospectus has not been exercised. Investors 
who trade the HDRs on the basis of publicly available allocation details prior to the receipt 
of HDR certificates or prior to the HDR certificates becoming valid evidence of title do so 
entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Friday, 
June 26, 2026 (Hong Kong time), it is expected that dealings in the HDRs on the Stock 
Exchange will commence at 9:00 a.m. on Friday, June 26, 2026 (Hong Kong time). The HDRs 
will be traded in board lots of 100 HDRs each, and the stock code of the HDRs will be 6228.
By order of the Board
PT Merdeka Gold Resources Tbk
Mr. Boyke Poerbaya Abidin
President Director of the Board
Hong Kong, June 25, 2026
Directors and Commissioners of the Company named in the application to which this 
announcement relates are: (i) Mr. Boyke Poerbaya Abidin, Mr. Nicholas John Green, 
Mr. Barend Johannes Nicolaas Knoetze and Mr. Suryadinata Tanu as directors, (ii) 
Mr. Santoso Kartono, Mr. Winato Kartono and Mr. Xinyu Wang as commissioners, and (iii) 
Mr. Heri Sunaryadi, Dr. Jona Widhagdo Putri, Mr. Yu Gao and Mr. John Mackay McCulloch 
Williamson as independent commissioners.
