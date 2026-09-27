# 配发结果公告抽取任务：3355.HK FS.COM Ltd. - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**20/03/2026 22:07**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0320/2026032001750.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3355.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
requirements of the U.S. Securities Act and in compliance with any applicable state securities laws. There will be no 
public offer of the Offer Shares in the United States. The Offer Shares are being offered and sold solely outside the 
United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act and applicable laws of 
each jurisdiction where those offers and sales occur.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. Potential investors should read the Prospectus for detailed information about the Company 
and the Global Offering described below before deciding whether or not to invest in the Offer Shares.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated 13 March 2026 (the “Prospectus”) issued by FS.COM Limited (the “Company”).
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
an end within 30 days of the last day for lodging applications under the Hong Kong Public Offering, being Friday, 
17 April 2026. Such stabilizing action, if taken, may be effected in all jurisdictions where it is permissible to do so, 
in each case in compliance with all applicable laws, rules and regulatory requirements, including the Securities and 
Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities 
and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering. After this date, when no further 
stabilizing action may be taken, demand for the H Shares, and therefore the price of the H Shares, could fall.
Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the 
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the 
section headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds 
for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date.
1

<<<PAGE 2>>>
FS.COM Limited
深圳市飛速創新科技股份有限公司
(a joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under the
Global Offering
:
40,000,000 H Shares (subject to the 
Over-allotment Option)
Number of Hong Kong Offer Shares
:
4,000,000 H Shares (subject to 
 reallocation)
Number of International Offer Shares
:
36,000,000 H Shares (subject to 
reallocation and the Over-allotment 
 Option)
Final Offer Price
:
HK$41.60 per H Share plus brokerage 
of 1.0%, SFC transaction levy of 
0.0027%, Hong Kong Stock Exchange 
trading fee of 0.00565% and AFRC 
transaction levy of 0.00015% (payable 
in full on application in Hong Kong 
dollars and subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
3355
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Joint Bookrunners
2

<<<PAGE 3>>>
FS.COM Limited / 深圳市飛速創新技術股份有限公司 
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS 
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated 13 March 2026 (the “Prospectus”) issued by FS.COM Limited (the “Company”).  
Warning: In view of high concentration of shareholding in a small number of Shareholders, Shareholders and 
prospective investors should be aware that the price of the H Shares could move substantially even with a small 
number of H Shares traded and should exercise extreme caution when dealing in the H Shares. 
SUMMARY 
Company information 
Stock code 
3355 
Stock short name 
FS.COM 
Dealings commencement date 
23 March 2026* 
*see note at the end of the announcement
Price Information 
Final Offer Price 
HK$41.60 
Maximum Offer Price 
HK$41.60 
Offer Shares and Share Capital 
Number of Offer Shares 
40,000,000 
Number of Offer Shares in the Hong Kong Public Offering (after 
reallocation) 
4,000,000 
Number of offer shares in International Offering (after 
reallocation) 
36,000,000 
Number of issued shares upon Listing 
400,000,000 
Over-allocation 
No. of Offer Shares over-allocated 
6,000,000 
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases in the 
secondary market at prices that do not exceed the Offer Price or through deferred delivery or a combination of 
these means. In the event the Over-allotment Option is exercised, an announcement will be made on the Stock 
Exchange’s website. 
Proceeds 
Gross proceeds (Note) 
HK$ 1,664.00 million 
Less: Estimated listing expenses payable based on Final Offer 
Price  
HK$ 104.97 million 
Net proceeds 
HK$ 1,559.03 million 
Note: Gross proceeds refer to the amount to which the Company is entitled to receive. For details of the use of proceeds, please 
refer to the Prospectus dated 13 March 2026. 
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING 
No. of valid applications 
196,756 
No. of successful applications 
31,492 
3

<<<PAGE 4>>>
 
Subscription level 
1,579.71 times 
Claw-back triggered 
N/A 
No. of Offer Shares initially available under the Public Offer 
4,000,000 
Final no. of Offer Shares under the Hong Kong Public Offering (after 
reallocation) 
4,000,000 
% of Offer Shares under the Hong Kong Public Offering to the Global 
Offering 
10% 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
https://www.hkeipo.hk/IPOResult to perform a search by name or identification number or 
https://www.hkeipo.hk/IPOResult  for the full list of allottees. 
INTERNATIONAL OFFERING 
No. of placees 
140 
Subscription Level 
10.92 times 
No. of Offer Shares initially available under the International Offering 
36,000,000 
Final no. of Offer Shares under the International Offering 
36,000,000 
% of Offer Shares under the International Offering to the Global 
Offering 
90% 
The Directors confirm that, to the best of their knowledge, information and belief, (a) save for waivers from strict 
compliance with Rule 10.04 of the Listing Rules and consents under paragraph 1C(2) of Appendix F1 to the Listing 
Rules (the “Placing Guidelines”) granted by the Stock Exchange to permit the Company to allocate certain Offer Shares 
in the International Offering to certain existing Shareholders and/or their close associates and (b) a consent under 
Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to, among other things, allocate further H 
Shares in the International Offering to certain Cornerstone Investors and/or their respective close associates, (i) none 
of the Offer Shares subscribed by the placees and the public have been financed directly or indirectly by the Company, 
any of the Directors, chief executive of the Company, controlling shareholders, substantial shareholders, existing 
shareholders of the Company or any of its subsidiaries or their respective close associates; and (ii) none of the placees 
and the public who have purchased the Offer Shares are accustomed to taking instructions from the Company, any of 
the Directors, chief executive of the Company, controlling shareholders, substantial shareholders, existing shareholders 
of the Company or any of its subsidiaries or their respective close associates in relation to the acquisition, disposal, 
voting or other disposition of Shares registered in his/her/its name or otherwise held by him/her/it.  
The placees in the International Offering include the following: 
Cornerstone Investors 
Investor(1) 
No. of 
Offer 
Shares 
allocated 
% of total issued H 
Shares after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised) 
% of total 
issued share 
capital after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised) 
Existing 
shareholders or 
their close 
associates 
Hao Great 
China Focus 
Fund (“Hao 
Fund”) 
3,751,900 
0.94% 
0.94% 
No 
Great Holding 
Development 
Limited (“Great 
Holding”) 
2,713,900 
0.68% 
0.68% 
No 
4

<<<PAGE 5>>>
 
Investor(1) 
No. of 
Offer 
Shares 
allocated 
% of total issued H 
Shares after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised) 
% of total 
issued share 
capital after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised) 
Existing 
shareholders or 
their close 
associates 
WT Asset 
Management 
Limited 
1,875,900 
0.47% 
0.47% 
No 
Caitong Funds 
SPC — 
Strategic Equity 
Fund III SP 
(“Caitong 
SEIII”) 
1,802,800 
0.45% 
0.45% 
No 
Shanghai 
Intewise Capital 
Investment 
Limited 
(“Shanghai 
Intewise”) 
ultimate clients 
and CICC 
Financial 
Trading Limited 
(“CICC FT”) 
(in connection 
with Shanghai 
Intewise OTC 
Swaps) 
1,346,100 
0.34% 
0.34% 
No 
Foresight 
Capital Steady 
Growth LPF 
(“Foresight”) 
1,201,900 
0.30% 
0.30% 
No 
SCGC Capital 
Holding 
Company 
Limited 
(“SCGC 
Capital”) 
1,201,900 
0.30% 
0.30% 
Yes 
Aether Wave 
Fund L.P. 
1,125,500 
0.28% 
0.28% 
Yes 
GF International 
Investment 
Management 
Limited (“GF 
Fund HK”) 
937,900 
0.23% 
0.23% 
No 
Shenzhen 
Kaifeng 
Investment 
Management 
Co., Ltd. 
(“Shenzhen 
Kaifeng”), 
Changdu 
Kaifeng 
Investment 
721,000 
0.18% 
0.18% 
No 
5

<<<PAGE 6>>>
 
Investor(1) 
No. of 
Offer 
Shares 
allocated 
% of total issued H 
Shares after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised) 
% of total 
issued share 
capital after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised) 
Existing 
shareholders or 
their close 
associates 
Management 
Co., Ltd. 
(“Changdu 
Kaifeng”) and 
CICC FT (in 
connection with 
the Kaifeng 
OTC Swaps (as 
defined below)) 
Wider Huge 
Group Limited 
(“Wider 
Huge”) 
244,100 
0.06% 
0.06% 
No 
Total 
16,922,900 
4.23% 
4.23% 
Note: 
1.
In addition to the Offer Shares subscribed for as Cornerstone Investors, CICC FT (in connection with the Shanghai
Intewise OTC Swaps and the Kaifeng OTC Swaps), Foresight, Aether Wave Fund L.P., SCGC Capital and Wider
Huge and/or their respective close associates, where applicable, were allocated further Offer Shares as placees
in the International Offering. Please refer to the section headed “Allotment Results Details – International Offer
– Allottees with waivers/consents obtained” in this announcement for details. Only the Offer Shares subscribed
for as Cornerstone Investors are subject to lock-up as indicated below. For details, please refer to the section
headed “Lock-up Undertakings – Cornerstone Investors” in this announcement.
Allottees with waivers/consents obtained 
Investor 
No. of 
Offer 
Shares allocated 
% of total issued H 
Shares after the 
Global Offering 
(assuming the over-
allotment Option is 
not exercised) 
% of total issued 
share capital after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) 
Relationship 
Allottees with consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of 
further H Shares to existing Shareholders and Cornerstone Investors and/or their close associates (1) 
Hao Fund 
1,743,500 
0.44% 
0.44% A Cornerstone 
Investor 
WT 
Asset 
Management Limited 
1,313,000 
0.33% 
0.33% A Cornerstone 
Investor 
Caitong SEIII 
1,257,000 
0.31% 
0.31% A Cornerstone 
Investor 
SCGC Capital 
1,200,000 
0.30% 
0.30% A close associate 
of an existing 
Shareholder and a 
Cornerstone 
Investor 
Aether Wave Fund 
L.P.
788,000 
0.20% 
0.20% A Cornerstone 
Investor 
Shanghai 
Intewise 
ultimate clients and 
CICC 
FT 
(in 
5,412,500 
1.35% 
1.35% A Cornerstone 
Investor 
6

<<<PAGE 7>>>
connection 
with 
Shanghai 
Intewise 
OTC Swaps) 
Shenzhen 
Kaifeng, 
Changdu 
Kaifeng 
and CICC FT (in 
connection with the 
Kaifeng OTC Swaps) 
318,500 
0.08% 
0.08% A Cornerstone 
Investor 
Longrising Ultimate 
Clients (as defined 
below) and CICC FT 
(in connection with 
the Longrising OTC 
Swaps (as defined 
below)) 
63,400 
0.16% 
0.16% A close associate 
of a Cornerstone 
Investor 
Wider Huge 
187,500 
0.05% 
0.05% A Cornerstone 
Investor 
Foresight 
825,500 
0.21% 
0.21% A Cornerstone 
Investor 
GF Fund HK 
656,500 
0.16% 
0.16% A close associate 
of a Cornerstone 
Investor 
GF Securities Asset 
Management 
(Guangdong) 
Co., 
Ltd. (“GF Securities 
AM”, acting as a 
qualified 
domestic 
institutional investor 
for PSBC Wealth 
Management 
Co., 
Ltd. 
(“PSBC 
Wealth”)) (2) 
5,000 
0.01% 
0.01% A close associate 
of a Cornerstone 
Investor 
GF Securities AM 
acting as a qualified 
domestic institutional 
investor 
for 
CIB-
GFAM 
WANXIANG NO.1 
(3)
2,000 
0.01% 
0.01% A close associate 
of a Cornerstone 
Investor 
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients (4) 
Shanghai Intewise 
ultimate clients and 
CICC FT (in 
connection with 
Shanghai Intewise 
OTC Swaps) 
5,412,500 
1.35% 
1.35% Connected client 
Shenzhen Kaifeng 
and CICC FT (in 
connection with the 
Kaifeng OTC 
Swaps) 
159,200 
0.04% 
0.04% Connected client 
Changdu Kaifeng 
and CICC FT (in 
connection with the 
Changdu OTC 
159,300 
0.04% 
0.04% Connected client 
7

<<<PAGE 8>>>
 
Swaps) (defined 
below) 
Longrising Ultimate 
Clients (as defined 
below) and CICC FT 
(in connection with 
the Longrising OTC 
Swaps (as defined 
below)) 
63,400 
0.02% 
0.02% Connected client 
Bosera Asset 
Management 
(International) Co., 
Ltd (“Bosera AM”) 
75,000 
0.02% 
0.02% Connected client 
China Asset 
Management (Hong 
Kong) Limited 
(“China AM HK”) 
75,000 
0.02% 
0.02% Connected client 
CSI Panjing 
Ultimate Clients 
(defined below) and 
CITIC Securities 
International Capital 
Management 
Limited (“CSI”) (in 
connection with CSI 
Panjing OTC Swaps) 
84,500 
0.02% 
0.02% Connected client 
CITIC Securities 
Asset Management 
Company Limited 
(“CITIC Asset 
Management”) 
10,000 
0.003% 
0.003% Connected client 
CSI HY Capital 
Ultimate Client (as 
defined below) and 
CSI (in connection 
with the CSI HY 
OTC Swaps (as 
defined below)) 
150,000 
0.04% 
0.04% Connected client 
Haitong Global 
Investment SPC IV - 
Haitong Opportunity 
Fund II S.P. 
(“Haitong 
Opportunity Fund 
II”) 
10,000 
0.003% 
0.003% Connected client 
Guotai Junan 
Investments (Hong 
Kong) Limited  
5,000 
0.001% 
0.001% Connected client 
Valuable Investment 
Limited 
37,500 
0.01% 
0.01% Connected client 
Notes: 
1.
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the number
of Offer Shares allocated to the investors as placees in the International Offering. For allocations of Offer Shares
to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment Results Details –
International Offer – Cornerstone Investors” in this announcement. For details of the consent under Chapter 4.15
of the Guide for New Listing Applicants in relation to allocations of further H Shares to the existing Shareholders
and/or their close associates and Cornerstone Investors, please refer to the section headed “Others/Additional
8

<<<PAGE 9>>>
 
Information – Allocations of further H Shares to a close associate of an existing Shareholders and Cornerstone 
Investors with consent under Chapter 4.15 of the Guide for New Listing Applicants” in this announcement.  
2.
GF Securities AM and GF Fund HK are members of the same group of companies. GF Securities AM is therefore
a close associate of GF Fund HK. PSBC Wealth has engaged GF Securities AM, an asset manager that is a qualified
domestic institutional investor as approved by the relevant PRC authority, to subscribe for and hold such Offer
Shares on a non-discretionary basis on behalf of PSBC Wealth, in the name of: (i) GFAM ZHONGYOU NO. 4
ASSET MANAGEMENT ACCOUNT (QDII) (廣發資管中郵理財港 股策略4號單一資產管理計劃) and (ii)
GFAM ZHONGYOU NO. 5 ASSET MANAGEMENT ACCOUNT (QDII) (廣發資管中郵理財港股策略5號單一
資產管理計劃). PSBC Wealth is wholly owned by Postal Savings Bank of China Co., Ltd. (SEHK: 1658) and is
ultimately controlled by China Post Group Corporation Limited.
3.
GF Securities AM will hold the Offer Shares as product manager on behalf of CIB- GFAM WANXIANG NO.1, with
the ultimate client being Shenwan Hongyuan Group Co., Ltd. (申萬宏源集團股份有限公司) (the “GF Securities
AM Ultimate Client AMS”). Shenwan Hongyuan Securities Co., Ltd. is a wholly-owned subsidiary of Shenwan
Hongyuan Group Co., Ltd. (Stock Code: 6806).
4.
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New
Listing Applicants in relation to allocations to connected clients, please refer to the section headed “Others /
Additional Information – Placing to connected clients with prior consent under paragraph 1C(1) of the Placing
Guidelines” in this announcement.
LOCK-UP UNDERTAKINGS 
Controlling Shareholders 
Name 
Number of 
shares held in 
the Company 
subject to lock-
up 
undertakings 
upon Listing 
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing 
% of total issued 
H Shares in the 
Company subject 
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
exercised 
Last day subject 
to the lock-up 
undertakings 
(1)(2)
Mr. Xiang Wei 
203,928,528 
203,928,528 
50.98% 
50.98% 
22 March 2027 
Shenzhen 
Yuxuan Prudence 
Technology 
Partnership 
(Limited 
Partnership) 
11,489,819 
11,489,819 
2.87% 
2.87% 
22 March 2027 
Shenzhen 
Yuxuan Progress 
Technology 
Partnership 
(Limited 
Partnership) 
2,650,548 
2,650,548 
0.66% 
0.66% 
22 March 2027 
Shenzhen 
Yuxuan Growth 
Technology 
Partnership 
(Limited 
Partnership) 
2,091,006 
2,091,006 
0.52% 
0.52% 
22 March 2027 
Total 
220,159,901 
220,159,901 
55.04% 
55.04% 
Note: 
9

<<<PAGE 10>>>
 
Name 
Number of 
shares held in 
the Company 
subject to lock-
up 
undertakings 
upon Listing 
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing 
% of total issued 
H Shares in the 
Company subject 
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
exercised 
Last day subject 
to the lock-up 
undertakings 
(1)(2)
1.
The expiry date of the lock-up period is pursuant to the PRC Company Law.
2.
In accordance with the relevant Listing Rule/guidance materials, the required lock-up for the first six-month period
ends on 22 September 2026 and for the second six-month period ends on 22 March 2027.
Cornerstone Investors 
 Name 
Number of H 
Shares held in the 
Company subject to 
lock-up 
undertakings upon 
Listing 
% of total issued H 
Shares subject to 
lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised) 
% of shareholding in 
the Company subject 
to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised) 
Last day subject to 
the lock-up 
undertakings (1) 
Hao Fund 
3,751,900 
0.94% 
0.94% 
22 September 2026 
Great Holding 
2,713,900 
0.68% 
0.68% 
22 September 2026 
WT Asset 
Management Limited 
1,875,900 
0.47% 
0.47% 
22 September 2026 
Caitong SEIII 
1,802,800 
0.45% 
0.45% 
22 September 2026 
Shanghai Intewise 
ultimate clients and 
CICC FT (in 
connection with 
Shanghai Intewise 
OTC Swaps) 
1,346,100 
0.34% 
0.34% 
22 September 2026 
Foresight 
1,201,900 
0.30% 
0.30% 
22 September 2026 
SCGC Capital 
1,201,900 
0.30% 
0.30% 
22 September 2026 
Aether Wave Fund 
L.P.
1,125,500 
0.28% 
0.28% 
22 September 2026 
GF Fund HK 
937,900 
0.23% 
0.23% 
22 September 2026 
Shenzhen Kaifeng, 
Changdu Kaifeng 
and CICC FT (in 
connection with the 
Kaifeng OTC Swaps) 
721,000 
0.18% 
0.18% 
22 September 2026 
Wider Huge 
244,100 
0.06% 
0.06% 
22 September 2026 
Total 
16,922,900 
4.23% 
4.23% 
Note: 
1.
In accordance with the respective Cornerstone Investment Agreement, the required lock-up ends on 22 September
2026. The Cornerstone Investors will cease to be prohibited from disposing of or transferring Shares after the
indicated date.
Existing Shareholders (other than the Controlling Shareholders) 
10

<<<PAGE 11>>>
 
 Name 
Number of shares held in 
the Company subject to 
lock-up undertakings 
upon Listing 
% of shareholding in the 
Company subject to lock-
up undertakings upon 
Listing (assuming the 
Over-allotment Option is 
not exercised) 
Last day subject to the 
lock-up undertakings (1) 
Gongqingcheng Fupeng 
Hongxiang No. 3 Venture 
Capital Partnership 
(Limited Partnership) 
39,405,738 
9.85% 
22 March 2027 
Ningbo Meishan Bonded 
Port Area Fupeng 
Hongxiang No. 8 Equity 
Investment 
Management Centre 
(Limited Partnership) 
17,514,646 
4.38% 
22 March 2027 
Haitong Innovation 
Securities Investment Co., 
Ltd. 
16,069,116 
4.02% 
22 March 2027 
Yang Jie 
15,850,897 
3.96% 
22 March 2027 
Shenzhen Hongtu No. 1 
Private Equity Investment 
Fund Partnership (Limited 
Partnership) 
8,181,818 
2.05% 
22 March 2027 
Shenzhen Chaoyue Future 
Venture Capital Partnership 
(Limited Partnership) 
6,860,832 
1.72% 
22 March 2027 
Hainan Orcas Private 
Equity Investment Fund 
Partnership (Limited 
Partnership) 
4,548,848 
1.14% 
22 March 2027 
Xiamen Taiya Phase I 
Venture Capital Partnership 
(Limited Partnership) 
3,892,093 
0.97% 
22 March 2027 
Guosen (Zhuhai) Energy 
Industry Private Equity 
Fund Partnership Enterprise 
(Limited Partnership) 
3,478,800 
0.87% 
22 March 2027 
Shenzhen Capital Group 
Co., Ltd. 
3,272,725 
0.82% 
22 March 2027 
Zhuhai Lafang Excellence 
No. 7 Investment Fund 
(Limited Partnership) 
3,083,880 
0.77% 
22 March 2027 
Jieyang Herun Investment 
Co., Ltd. 
3,083,880 
0.77% 
22 March 2027 
Shenzhen Nanshan Hongtu 
Equity Investment Fund 
Partnership (Limited 
Partnership) 
2,181,820 
0.55% 
22 March 2027 
Xuzhou Yongzheng 
Investment Partnership 
(Limited Partnership) 
1,785,335 
0.45% 
22 March 2027 
Xiamen Guosen Lianfa 
Intelligent Technology 
Industry Private Equity 
Investment Fund 
1,739,509 
0.43% 
22 March 2027 
11

<<<PAGE 12>>>
 Name 
Number of shares held in 
the Company subject to 
lock-up undertakings 
upon Listing 
% of shareholding in the 
Company subject to lock-
up undertakings upon 
Listing (assuming the 
Over-allotment Option is 
not exercised) 
Last day subject to the 
lock-up undertakings (1) 
Partnership Enterprise 
(Limited Partnership) 
Shenzhen Chiyu Enterprise 
Management 
Partnership (Limited 
Partnership) 
1,739,069 
0.43% 
22 March 2027 
Shenzhen Chaoyue No. 1 
Investment 
Partnership (Limited 
Partnership) 
1,636,362 
0.41% 
22 March 2027 
Gong Cuihua 
1,542,048 
0.39% 
22 March 2027 
Jinggangshan Mingcheng 
Feisu Equity Investment 
Partnership (Limited 
Partnership) 
1,090,910 
0.27% 
22 March 2027 
Jinggangshan Mingcheng 
Ruiying Equity Investment 
Partnership (Limited 
Partnership) 
1,090,910 
0.27% 
22 March 2027 
Shenzhen Sailvan Network 
Technology Co., Ltd. 
632,911 
0.16% 
22 March 2027 
Chen Shaofeng 
649,272 
0.16% 
22 March 2027 
Peng Chao 
508,680 
0.13% 
22 March 2027 
Total 
139,840,099 
38.85% 
Note: 
1.
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law.
12

<<<PAGE 13>>>
PLACEE CONCENTRATION ANALYSIS 
Placees* 
Number of H Shares 
allotted 
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
exercised and new H 
Shares are issued) 
Allotment as % of 
total Offer Shares 
(assuming no 
exercise of the Over-
allotment Option) 
Allotment as % of 
total Offer Shares 
(assuming the Over-
allotment Option is 
fully exercised and 
new H Shares are 
issued) 
Number of H Shares 
held upon Listing 
% of total issued 
share capital upon 
Listing (assuming no 
exercise of the Over-
allotment Option) 
% of total issued 
share capital upon 
Listing (assuming 
the Over-allotment 
Option is fully 
exercised and new H 
Shares are issued) 
Top 1 
6,758,600 
18.77% 
16.09% 
16.90% 
14.49% 
6,758,600 
1.69% 
1.66% 
Top 5 
21,216,600 
58.94% 
50.52% 
53.04% 
46.12% 
21,216,600 
5.30% 
5.23% 
Top 10 
30,976,800 
86.05% 
73.75% 
77.44% 
67.34% 
49,162,011 
12.29% 
12.11% 
Top 25 
37,927,400 
105.35% 
90.30% 
94.82% 
82.45% 
55,673,611 
13.92% 
13.71% 
Note 
* Ranking of placees is based on the number of Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS 
Placees* 
Number of H 
Shares allotted 
Allotment as % of 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option) 
Allotment as % of 
International 
Offering 
(assuming the 
Over-allotment 
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
Number of H 
Shares held upon 
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
Option is fully 
exercised and new 
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
220,159,901 
55.04% 
54.23% 
220,159,901 
Top 5 
2,401,900 
6.67% 
5.72% 
6.00% 
5.22% 
330,256,870 
82.56% 
81.34% 
330,256,870 
Top 10 
16,569,400 
46.03% 
39.45% 
41.42% 
36.02% 
361,871,185 
90.47% 
89.13% 
361,871,755 
Top 25 
34,238,300 
95.11% 
81.52% 
85.60% 
74.43% 
392,956,117 
98.24% 
96.79% 
392,956,117 
Note 
* Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
13

<<<PAGE 14>>>
SHAREHOLDERS CONCENTRATION ANALYSIS 
Placees* 
Number of H Shares 
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
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
Allotment as % 
of total Offer 
Shares 
(assuming no 
exercise of the 
Over-allotment 
Option) 
Allotment as % 
of total Offer 
Shares 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
Number of H 
Shares held 
upon Listing 
Number of Shares held upon 
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
Option is fully 
exercised and 
new H Shares are 
issued) 
Top 1 
0 
0.00% 
0.00% 
0.00% 
0.00% 
220,159,901 
220,159,901 
55.04% 
54.23% 
Top 5 
2,401,900 
6.67% 
5.72% 
6.00% 
5.22% 
330,256,870 
330,256,870 
82.56% 
81.34% 
Top 10 
16,569,400 
46.03% 
39.45% 
41.42% 
36.02% 
361,871,185 
361,871,185 
90.47% 
89.13% 
Top 25 
34,238,300 
95.11% 
81.52% 
85.60% 
74.43% 
392,956,117 
392,956,117 
98.24% 
96.79% 
Note 
* Ranking of Shareholders is based on the number of Shares held by the Shareholders upon Listing.
14

<<<PAGE 15>>>
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by the 
public will be conditionally allocated on the basis set out below: 
No. of H Shares 
Applied For 
No. of Valid 
Applications 
Basis of Allotment/Ballot 
Approximate 
Percentage allotted 
of the Total No. of H 
Shares applied for 
Pool A 
100 
64,962 
650 out of 64,962 to receive 100 Shares 
1.00% 
200 
25,942 
400 out of 25,942 to receive 100 Shares 
0.77% 
300 
4,603 
92 out of 4,603 to receive 100 Shares 
0.67% 
400 
3,172 
76 out of 3,172 to receive 100 Shares 
0.60% 
500 
4,154 
114 out of 4,154 to receive 100 Shares 
0.55% 
600 
2,222 
68 out of 2,222  to receive 100 Shares 
0.51% 
700 
1,985 
67 out of 1,985 to receive 100 Shares 
0.48% 
800 
2,100 
77 out of 2,100 to receive 100 Shares 
0.46% 
900 
1,341 
53 out of 1,341 to receive 100 Shares 
0.44% 
1,000 
16,443 
691 out of 16,443 to receive 100 Shares 
0.42% 
1,500 
3,520 
191 out of 3,520 to receive 100 Shares 
0.36% 
2,000 
4,367 
283 out of 4,367 to receive 100 Shares 
0.32% 
2,500 
2,056 
153 out of 2,056 to receive 100 Shares 
0.30% 
3,000 
1,726 
144 out of 1,726 to receive 100 Shares 
0.28% 
3,500 
1,242 
114 out of 1,242 to receive 100 Shares 
0.26% 
4,000 
1,228 
123 out of 1,228 to receive 100 Shares 
0.25% 
4,500 
1,101 
118 out of 1,101 to receive 100 Shares 
0.24% 
5,000 
2,308 
265 out of 2,308 to receive 100 Shares 
0.23% 
6,000 
1,596 
205 out of 1,596 to receive 100 Shares 
0.21% 
7,000 
1,378 
195 out of 1,378 to receive 100 Shares 
0.20% 
8,000 
1,328 
204 out of 1,328 to receive 100 Shares 
0.19% 
9,000 
1,158 
192 out of 1,158 to receive 100 Shares 
0.18% 
10,000 
9,058 
1,596 out of 9,058 to receive 100 Shares 
0.18% 
20,000 
4,848 
1,316 out of 4,848 to receive 100 Shares 
0.14% 
30,000 
3,255 
1,137 out of 3,255 to receive 100 Shares 
0.12% 
40,000 
2,379 
995 out of 2,379 to receive 100 Shares 
0.10% 
50,000 
2,179 
1,047 out of 2,179 to receive 100 Shares 
0.10% 
60,000 
1,453 
782 out of 1,453 to receive 100 Shares 
0.09% 
70,000 
1,248 
739 out of 1,248 to receive 100 Shares 
0.08% 
80,000 
1,160 
747 out of 1,160 to receive 100 Shares 
0.08% 
90,000 
993 
688 out of 993 to receive 100 Shares 
008% 
100,000 
8,759 
6,478 out of 8,759 to receive 100 Shares 
0.07% 
Total 
185,264 
Total number of Pool A successful applicants: 20,000 
No. of H Shares 
Applied For 
No. of Valid 
Applications 
Basis of Allotment/Ballot 
Approximate 
Percentage allotted 
of the Total No. of H 
Shares applied for 
15

<<<PAGE 16>>>
Pool B 
200,000 
6,055 
2,422 out of 6,055 to receive 100 Shares 
0.07% 
300,000 
1,822 
1,201 out of 1,822 to receive 100 Shares 
0.06% 
400,000 
1,031 
899 out of 1,031 to receive 100 Shares 
0.05% 
500,000 
717 
39 out of 717 to receive 100 Shares 
0.04% 
600,000 
341 
75 out of 341 to receive 100 Shares 
0.04% 
700,000 
273 
100 out of 273 to receive 100 Shares 
0.03% 
800,000 
212 
107 out of 212 to receive 100 Shares 
0.03% 
900,000 
157 
99 out of 157 to receive 100 Shares 
0.03% 
1,000,000 
535 
399 out of 535 to receive 100 Shares 
0.03% 
2,000,000 
349 
234 out of 349 to receive 100 Shares 
0.02% 
Total 
Total number of Pool B successful applicants: 11,492 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. Investors 
should contact their relevant brokers for any inquiries. 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of which 
consent has been obtained, the Company has complied with the Listing Rules and guidance materials in relation 
to the placing, allotment and listing of the Company’s H Shares.  
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the public 
(as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by them was the 
same as the final Offer Price in addition to any brokerage, AFRC transaction levy, SFC transaction levy and 
trading fee payable. 
OTHERS/ ADDITIONAL INFORMATION 
Allocations of further H Shares to a close associate of an existing Shareholders and Cornerstone Investors 
with consent under Chapter 4.15 of the Guide for New Listing Applicants 
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 of the Guide 
for New Listing Applicants to permit the Company to allocate further Offer Shares in the International Offering 
to a close associate of an existing Shareholder and Cornerstone Investors as placees, subject to the following 
conditions: 
(a)
the final offering size of the Global Offering (excluding any additional H Shares which may be issued
upon exercise of the Over-allotment Option) will be of a total value of at least HK$1 billion as required
by paragraph 18(i) of Chapter 4.15 of the Guide for New Listing Applicants;
(b)
the Offer Shares allocated to all existing shareholders and their close associates (whether as cornerstone
investors and/or as placees) as permitted under this exemption do not exceed 30% of the total number
of the H Shares offered, which is in compliance with paragraph 18(ii) of Chapter 4.15 of the Guide for
New Listing Applicants; and
(c)
each Director, chief executive and Supervisor of the Company has confirmed that no securities have
been allocated to them or their respective close associates under the Size-based Exemption as defined
in the Guide) as required by paragraph 18(iii) of Chapter 4.15 of the Guide for New Listing Applicants.
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted by the 
Stock Exchange. 
16

<<<PAGE 17>>>
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates and 
Cornerstone Investors, please refer to the section headed “Allotment Results Details – International Offer – 
Allottees with waivers/consents obtained” in this announcement. 
Placing to connected clients with prior consent under paragraph 1C(1) of the Placing Guidelines 
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, consents under 
paragraph 1C of the Placing Guidelines to permit allocation to connected clients pursuant to the Placing 
Guidelines. The allocation of Offer Shares to such connected clients is in compliance with all the conditions 
under the consents granted by the Stock Exchange. Details of the placement to connected clients (including the 
cornerstone tranche and placing tranche) are set out below. 
Connected 
Distributor 
Connected Client 
Relationship 
Whether the 
Connected Client 
will 
hold the 
beneficial 
interests of the 
Offer 
Shares on a non-
discretionary 
basis or 
discretionary 
basis 
for independent 
third 
parties 
Number 
of Offer 
Shares to 
be 
allocated to 
the 
connected 
client 
Approximate 
percentage of 
Offer Shares 
allocated to 
the connected 
client 
(assuming 
no exercise 
of the 
Overallotment 
Option) 
Approximate 
percentage 
of total 
issued share 
capital after 
the Global 
Offering 
(assuming 
no exercise 
of the 
Overallotment 
Option) 
China 
International 
Capital 
Corporation 
Hong Kong 
Securities 
Limited 
(“CICCHKS”) 
Shanghai Intewise 
ultimate clients and 
CICC FT (in 
connection with 
Shanghai Intewise 
OTC Swaps) (1) 
CICC FT is a 
member of the 
same group of 
CICCHKS 
Non-discretionary 
basis 
5,412,500 
13.53% 
1.35% 
Shenzhen Kaifeng 
and CICC FT (in 
connection with the 
Kaifeng OTC Swaps)
(2)
CICC FT is a 
member of the 
same group of 
CICCHKS 
Non-discretionary 
basis 
159,200 
0.40% 
0.04% 
Changdu Kaifeng and 
CICC FT (in 
connection with the 
Changdu OTC Swaps 
(defined below)) (3) 
CICC FT is a 
member of the 
same group of 
CICCHKS 
Non-discretionary 
basis 
159,300 
0.40% 
0.04% 
Longrising Ultimate 
Clients (as defined 
below) and CICC FT 
(in connection with 
the Longrising OTC 
Swaps (as defined 
below)) (4) 
CICC FT is a 
member of the 
same group of 
CICCHKS 
Non-discretionary 
basis 
63,400 
0.16% 
0.02% 
China Merchants 
Securities (HK) 
Co., Limited 
(“CMS”) 
Bosera AM (5) 
Bosera AM is a 
member of the 
same group of 
companies as 
CMS. 
Discretionary basis 
75,000 
0.19% 
0.02% 
CITIC Securities 
Brokerage (HK) 
Limited (“CSB”) 
China AM HK (6) 
CSB and China 
AM HK are 
members of the 
Discretionary basis 
75,000 
0.19% 
0.019% 
17

<<<PAGE 18>>>
same group of 
companies. 
CSI Panjing Ultimate 
Clients (defined 
below) and CSI (in 
connection with CSI 
Panjing OTC Swaps) 
(7)
CSI Capital is a 
member of the 
same group of 
companies as 
CSB. 
Non-discretionary 
basis 
84,500 
0.21% 
0.021% 
CITIC Securities 
Asset Management (8) 
CITIC Asset 
Management is a 
member of the 
same group of 
companies of 
CSB. 
Discretionary basis 
10,000 
0.03% 
0.003% 
CSI HY Capital 
Ultimate Client (as 
defined below) and 
CSI (in connection 
with the CSI HY 
OTC Swaps (as 
defined below)) (9) 
CSI is a member 
of the same 
group of 
companies of 
CSB. 
Non-discretionary 
basis 
150,000 
0.38% 
0.04% 
Guotai Junan 
Securities (Hong 
Kong) Limited 
(“GTJA 
Securities”) 
 Haitong Opportunity 
Fund II (10) 
Haitong 
Opportunity 
Fund II is 
managed by 
Haitong 
International 
Asset 
Management 
(HK) Limited, 
which is a 
member of the 
same group of 
GTJA Securities. 
Discretionary basis 
10,000 
0.03% 
0.003% 
GTJA Ultimate 
clients (defined 
below) and Guotai 
Junan Investments 
(Hong Kong) Limited 
(“GTJA 
Investments”) (in 
connection with the 
GTJA OTC Swaps 
(defined below)) (11) 
GTJA 
Investments is a 
member of the 
same group of 
GTJA Securities. 
Discretionary basis 
5,000 
0.01% 
0.001% 
Valuable Capital 
Limited 
Pan Haiguang (潘海
光) and Valuable 
Investment Limited 
(“Valuable 
Investment”) (in 
connection with the 
Valuable OTC Swaps 
(as defined below) (12) 
Valuable 
Investment is a 
member of the 
same group of 
companies as 
Valuable Capital 
Non-discretionary 
basis 
406,000 
1.02% 
0.10% 
Notes: 
(1)
CICC FT and China International Capital Corporation Limited (“CICCL”) has also entered into a series of cross border
over-the-counter swap transactions (collectively, the “Intewise OTC Swaps”) with each other, and with Shanghai Intewise
acting in its capacity as investment manager for and on behalf of Intewise Jinghong Electronic Technology Private
Securities Investment Fund (聚鳴景宏電子科 技私募證券投資基金) (“Intewise Jinghong”), Intewise Jiangchuan No. 3
18

<<<PAGE 19>>>
Private Securities Investment Fund (聚鳴匠傳3號私募證券投資基金) (“Intewise Jiangchuan No. 3”) and Intewise 
Jiangchuan No. 6 Private Securities Investment Fund (聚鳴匠傳6號私募證券投資基 金) (“Intewise Jiangchuan No. 6”, 
collectively with Intewise Jinghong and Interwise Jiangchuan No. 3, the “Intewise Ultimate Clients”).  
CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the Kaifeng OTC Swaps and Intewise OTC 
Swaps while the economic risks and returns of the underlying Offer Shares are passed to the Kaifeng Ultimate Clients and 
Intewise Ultimate Clients, subject to customary fees and commissions. CICC FT and CICCL are members of the same 
group of companies. 
(2)
CICC FT and CICCL has entered into a series of cross border over-the-counter swap transactions (collectively, the
“Shenzhen Kaifeng OTC Swaps”) with each other, and with Shenzhen Kaifeng acting in its capacity as investment
manager for and on behalf of Kaifeng Xingrui Equity Strategy No. 1 Securities Investment Private Fund (凱豐星睿股票
策略1號證券投資私募基金) (“Kaifeng Xingrui No. 1”) and Kaifeng Macro Strategy No. 10 Securities Investment
Private Fund (凱豐宏觀策略10號證券投資私募基金) (“Kaifeng Strategy No. 10”, collectively with Kaifeng Xingrui
No. 1, the “Shenzhen Kaifeng Ultimate Clients”), pursuant to which CICC FT will hold the Offer Shares on a non-
discretionary basis to hedge the Shenzhen Kaifeng OTC Swaps while the economic risks and returns of the underlying
Offer Shares are passed to the Shenzhen Kaifeng Ultimate Clients, subject to customary fees and commissions. The
Shenzhen Kaifeng OTC Swaps will be fully funded by the Shenzhen Kaifeng Ultimate Clients. To the best of CICC FT’s
knowledge having made all reasonable inquiries, each of the Shenzhen Kaifeng Ultimate Clients is an independent third
party of the Company and its associates, CICC FT, CICCL, CICCHKS and the companies which are members of the same
group of CICCHKS. Wu Xing (吳星) directly holds 32% interest in Shenzhen Kaifeng and 57.1% interest in Shanghai
Angyu Enterprise Management Consulting Partnership (Limited Partnership)* (上海昂毓企業管理諮詢合夥企業（有
限合夥）), which in turn holds 20% interest in Shenzhen Kaifeng. No other single ultimate beneficial owner holds 30%
or more interest in Shenzhen Kaifeng. Feng Wei (豐偉) and Wu Xing (吳星) holds 53.85% and 46.15% interest in Kaifeng
No. 1 Fund respectively. No single ultimate beneficial owner holds 30% or more interest in Kaifeng No. 10 Fund.
(3)
CICC FT and CICCL have also entered into a series of cross border over-the-counter swap transactions (collectively, the
“Changdu Kaifeng OTC Swaps”) with each other, and with Changdu Kaifeng acting in its capacity as investment
manager for and on behalf of Kaifeng Macro Hedge No.11 Private Fund (凱豐宏觀對沖11號私募基金) (the “Changdu
Kaifeng Ultimate Clients”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge
the Changdu Kaifeng OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed to the
Changdu Keifeng Ultimate Clients, subject to customary fees and commissions. The Changdu Kaifeng OTC Swaps will
be fully funded by the Changdu Kaifeng Ultimate Clients. To the best of CICC FT’s knowledge having made all reasonable
inquiries, each of the Changdu Kaifeng Ultimate Clients is an independent third party of the Company and its associates,
CICC FT, CICCL, CICCHKS and the companies which are members of the same group of CICCHKS. For completeness,
Changdu Kaifeng is a limited partner of and holds 33.3% partnership interest in Shenzhen Chaoyue Future Venture Capital
Partnership (Limited Partnership) (深圳市超越未來創業投資合夥企業(有限合夥)), an existing 1.91% Shareholder of
the Company. Wu Xing (吳星) holds 50% interest in Changdu Kaifeng. No other single ultimate beneficial owner holds
30% or more interest in Changdu Kaifeng. No single ultimate beneficial owner holds 30% or more interest in Kaifeng No.
11 Fund.
(4)
CICC FT and CICCL have entered into a series of cross border over-the-counter swap transactions (collectively, the
“Longrising OTC Swaps”) with each other, and with Yuanlesheng Asset Management Co., Ltd. (西藏源樂晟資產管理
有限公司) (“Longrising”) acting in its capacity as investment manager for and on behalf of Longrising Qiangshu Private
Securities Investment Fund (源樂晟強樹私募證券投資基金) (“Longrising Qiangshu”) and Longrising Qiangye Private
Securities Investment Fund (源樂晟強業私募證券投資基金) (“Longrising Qiangye”), collectively with Longrising
Qiangshu, the “Longrising Ultimate Clients”), pursuant to which CICC FT will hold the Offer Shares on a non-
discretionary basis to hedge the Longrising OTC Swaps while the economic risks and returns of the underlying Offer
Shares are passed to the Longrising Ultimate Clients, subject to customary fees and commissions. The Longrising OTC
Swaps will be fully funded by the Longrising Ultimate Clients. To the best of CICC FT’s knowledge having made all
reasonable inquiries, each of the Longrising Ultimate Clients is an independent third party of the Company and its
associates, CICC FT, CICCL, CICCHKS and the companies which are members of the same group of CICCHKS. Zeng
Xiaojie (曾曉潔) is the only beneficial owner with 30% interest or more in Longrising Qiangshu. Zeng Xiaojie (曾曉潔)
and Hu Caiyang (胡彩陽) are the only beneficial owners with 30% interest or more in Longrising Qiangye.
(5)
Bosera AM will hold the Offer Shares in its capacity as discretionary fund manager managing the sub-funds on behalf of
its following clients. Each of such clients, and their respective ultimate beneficial owner(s) with 30% interest or more, is,
to the best knowledge and belief of Bosera AM, an independent third party of the Company, its subsidiaries, its substantial
shareholders, CMS and the companies which are members of the same group of CMS:
Name of the sub-funds to which the Offer 
Shares will be allocated  
Whether any investor 
holds 
30% 
or 
more 
interests in the sub-fund 
Ultimate 
Beneficial 
Owner 
Shareholding % 
19

<<<PAGE 20>>>
Bosera Hong Kong Equity Plus Fund (SFC 
Authorised Fund) 
No 
N/A 
Bosera Global Select Equity Fund SP 
Yes 
Zhang Lei (張雷): 53.67% 
Bosera China New Opportunities Fund SP 
No 
N/A 
Bosera Growth Premium Global Equity 
Strategy Fund SP 
Yes 
Guo Feng (郭峰): 49.00% 
Bosera Growth Premium Global Equity 
Strategy Fund SP2 
Yes 
Guangdong Dongfang Precision 
Science & Technology Co., Ltd 
(Ticker: 002611 CH) 
(6)
China AM HK is an investment advisor and a delegate of the investment manager of the following underlying clients
(“China AM HK Ultimate Clients”) and manages assets (in its capacity as an investment advisor of the China AM HK
Ultimate Clients) and executes trades (in its capacity as delegate of the investment manager of China AM HK Ultimate
Clients) for and on behalf of China AM HK Ultimate Clients:
Name of the funds to which the Offer 
Shares will be allocated 
Whether any investor 
holds 30% or more 
interest in the fund 
Ultimate Beneficial Owner with 
30% or more interests and 
Shareholding (%) 
ChinaAMC Select Greater China 
Technology Fund 
Yes 
Futu Securities International 
(Hong Kong) Limited-client 
account: 52.96% 
ChinaAMC Fund - ChinaAMC China 
Opportunities Fund 
No 
N/A 
ChinaAMC China Focus Fund 
Yes 
Manulife (International) Limited: 
74.02% 
ChinaAMC China Growth Fund (SICAV) 
Yes 
Yuanta Securities (HK) Company 
LTD: 72.73% 
ChinaAMC Absolute Return Fund SP 
Yes 
Li Fung Ming: 79.16% 
To the best knowledge of China AM HK after making all reasonable enquiries, each of the China AM HK Ultimate Clients 
and the ultimate beneficial owners with 30% or more interest in the relevant China AM HK Ultimate Clients, is an 
independent third party of the Company, the Company’s subsidiaries and substantial shareholders, CSB, China AM HK 
and the companies which are members of the same group companies as CSB.  
(7)
CSI and CITIC Securities Company Limited (中信証券股份有限公司, 6030.HK) entered into a series of cross border
over-the-counter swap transactions (“CSI Panjing OTC Swaps”) with each other, and with Shanghai Panjing Investment
Management Centre (Limited Partnership)* (上海盤京投資管理中心（有限合夥）) acting in its capacity as investment
manager for and on behalf of PanShi Private Securities Investment Fund* (盤世私募證券投資基金) (“Panshi”), Panjing
MSCI Phase I Private Securities Investment Fund* (盤京明晟1期私募證券投資基金) (“Panjing MCSI”) and Panjing
Xinghe No. 1 Private Securities Investment Fund* (盤京興和1號私募證券投資基金) (“Panjing Xinghe”, together with
Panshi and Panjing MSCI as the “CSI Panjing Ultimate Clients”), pursuant to which CSI will hold the Offer Shares on
a non-discretionary basis to hedge the CSI OTC Swaps while the economic risks and returns of the underlying Offer Shares
are passed to the CSI Ultimate Clients, subject to customary fees and commissions. The CSI OTC Swaps will be fully
funded by the CSI Ultimate Clients.
To the best knowledge of CSI having made all reasonable inquiries, Shanghai Panjing is controlled by Zhuang Tao (莊濤
). Each of the CSI Ultimate Clients is an independent third party of the Company and its associates, CSI and the companies 
which are members of the same group of CITIC Securities Company Limited. No other single ultimate beneficial owner 
holds 30% or more interest in Panshi. Zhuang Tao (莊濤) is the only beneficial owner with 30% interest or more in Panjing 
MCSI and Panjing Xinghe. 
(8)
CITIC Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds
on behalf of following clients, each of which, to the best knowledge and belief of CITIC Asset Management, is an
independent third party of the Company, its subsidiaries, its substantial shareholders, CSB and the companies which are
members of the same group of CSB:
Name of the funds to which the Offer 
Shares will be allocated 
Whether any investor 
holds 30% or more 
interest in the fund 
Ultimate Beneficial Owner with 
30% or more interests and 
Shareholding (%) 
CITIC SECURITIES COMPANY 
LIMITED-XINHANG ZHIYUAN NO.1 
(中信証券信航致遠1號集合 資產管理
計劃) 
No 
N/A 
CITIC SECURITIES COMPANY 
No 
N/A 
20

<<<PAGE 21>>>
LIMITED-XINHANG ZHIYUAN NO.3 
(中信証券信航致遠3號集合 資產管理
計劃) 
CITIC Securities AM-Guibinfengyuan 
No.118 QDII (中信証券資管貴賓豐元
118號QDII集合資產 管理計劃) 
No 
N/A 
(9)
CSI and CITICS have entered into a series of cross border over-the-counter swap transactions (“CSI HY OTC Swaps”)
with each other, and with HY Capital Company Limited (“HY Capital” or “CSI HY Capital Ultimate Client”), as the
swap investor, pursuant to which CSI will hold the Offer Shares on a non-discretionary basis to hedge the CSI HY OTC
Swaps while the economic risks and returns of the underlying Offer Shares are passed to the CSI HY Capital Ultimate
Client, subject to customary fees and commissions. The CSI HY OTC Swaps will be fully funded by the CSI HY Capital
Ultimate Client. To the best of CSI’s knowledge having made all reasonable inquiries, Xia Hui and Lu Ang are ultimate
beneficial owners with 30% or more interest in HY Capital. Each of the CSI HY Capital Ultimate Client and its ultimate
beneficial owners with 30% or more interest, is an independent third party of the Company, its subsidiaries, its substantial
shareholders, CSB and the companies which are members of the same group of CSB and its associates.
(10)
Haitong Opportunity Fund II will hold the Offer Shares on behalf of its underlying client on a discretionary basis. To the
best knowledge, information and belief of Haitong Opportunity Fund II after making all reasonable enquiries, there is no
ultimate beneficial owner holding 30% interest or more in such underlying client.
To the best knowledge, information and belief of Haitong Opportunity Fund II after making all reasonable enquiries, its 
underlying client above is an independent third party of Haitong International Asset Management (HK) Limited, GTJA 
Securities] and the companies which are members of the same group of companies as GTJA Securities. 
(11)
GTJA Investments shall hold the Offer Shares for hedging purpose as the single underlying asset of several sets of back-
to-back total return swap transaction (the “GTHT Back-to-back TRS”) to be entered into between GTJA Investments and
Guotai Haitong Securities Co., Ltd. (the “GTHT Onshore Parent”) in connection with several total return swap orders
(the “GTHT Client TRS”) to be entered into by GTHT Onshore Parent and several ultimate clients (the “GTHT Onshore
Ultimate Client”), respectively. Such GTHT Client TRS is to be fully funded by the GTHT Onshore Ultimate Client.
GTJA Investments will hold the Offer Shares on a non-discretionary basis for the purpose of hedging the economic
exposure under the GTHT Back-to-back TRS and GTHT Client TRS only, During the tenor of the GTHT Client TRS, all
economic returns of the Offer Shares will be passed to the GTHT Onshore Ultimate Clients and all economic losses shall
be borne by the GTHT Onshore Ultimate Client, subject to the terms and conditions of the GTHT Back-to-back TRS and
GTHT Client TRS, and GTJA Investments will not take part in any economic return or bear any economic loss in relation
to the price of the Offer Shares. The GTHT Onshore Ultimate Client may request to redeem the Offer Shares at their own
discretion, upon which GTJA Investments shall dispose of the Offer Shares and settle the GTHT Back-to-back TRS and
GTHT Client TRS in cash in accordance with the terms and conditions of the GTHT Back-to-back TRS and GTHT Client
TRS documents. Due to its internal policy, GTJA Investments will not exercise the voting right attaching to the Offer
Shares during the tenor of the GTHT Back-to-back TRS and GTHT Client TRS.
To the best knowledge, information and belief of GTJA Investments after due enquiry, the GTHT Onshore Ultimate Clients 
and their respective ultimate beneficial owners holding 30% or more interest include: Shanghai Weining Investment 
Management Co, Ltd* (上海衛寧私募基金管理有限公司) (“Shanghai Weining”) acting in its capacity as investment 
manager for and on behalf of Weining Qihang No. 1 Private Securities Investment Fund* (衛甯啟航1號私募證券投資基
金) (“Weining Qihang”), and Shanghai Weining Investment Management Co ,Ltd-Weining Jujiao Private Securities 
Investment Fund* (衛寧聚焦私募證券投資基金) (“Weining Jujiao”, collectively with Weining Qihang, the “GTHT 
Onshore Ultimate Client”). Shanghai Weining is owned as to 45% by Fu Chengcheng (付誠成) and 35% by Lin Ran (
林然). Liu Yutao (劉育濤) is an ultimate beneficial owner with over 30% interest in Weining Qihang. Each of Lin Heming 
(林鶴鳴) and Wang Zhangyi (王張懿) is an ultimate beneficial owner with over 30% interest in Weining Jujiao. 
(12)
Valuable Investment and Pan Haiguang have entered into a series of cross border over-the-counter swap transactions
(collectively, the “Valuable OTC Swaps”) with each other, and with Pan Haiguang as the ultimate beneficial owner (the
“Valuable Ultimate Client”), pursuant to which Valuable Investment will hold the Offer Shares on a non-discretionary
basis to hedge the Valuable OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed to
the Valuable Ultimate Clients, subject to customary fees and commission. The Valuable OTC Swaps will be fully funded
by the Valuable Ultimate Clients. To the best of Valuable Investment’s knowledge having made all reasonable enquiries,
the Valuable Ultimate Client is an independent third party of the Company and its associates, Valuable Investment and the
companies which are members of the same group of Valuable Investment.
21

<<<PAGE 22>>>
DISCLAIMERS 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock 
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility 
for the contents of this announcement, make no representation as to its accuracy or completeness and 
expressly disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the 
whole or any part of the contents of this announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of 
Columbia). This announcement does not constitute or form a part of any offer or solicitation to purchase 
or subscribe for securities in the United States. The securities mentioned herein have not been, and will 
not be, registered under the United States Securities Act of 1933, as amended (the “U.S. Securities Act”). 
The securities may not be offered or sold in the United States except pursuant to an exemption from the 
registration requirements of the U.S. Securities Act and in compliance with any applicable state 
securities laws, or outside the United States unless in compliance with Regulation S under the U.S. 
Securities Act. There will be no public offer of securities in the United States. 
The Offer Shares are being offered and sold outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act. The Offer Shares have not been and will not be registered under 
the U.S. Securities Act and may not be offered or sold within the United States except pursuant to an exemption 
from the registration requirements of the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to 
acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential investors 
should read the Prospectus dated 13 March 2026 issued by FS.COM Limited for detailed information 
about the Global Offering described above before deciding whether or not to invest in the Shares thereby 
being offered.  
*Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on behalf
of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting
Agreement with immediate effect upon the occurrence of any of the events set out in the paragraph headed
“Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is
currently expected to be on 23 March 2026).
PUBLIC FLOAT 
Immediately following the completion of the Global Offering (before any exercise of the Over-allotment 
Option), 113,280,930 Shares, representing approximately 28.37% of the issued share capital of the Company 
will be held in the public hands, in compliance with Rule 8.08(1)(a) of the Listing Rules.  
The Directors confirm that, immediately following the completion of the Global Offering (i) no placee will, 
individually, be placed more than 10% of the enlarged issued share capital of the Company immediately after 
the Global Offering; (ii) there will not be any new substantial Shareholder (as defined in the Listing Rules) 
immediately after the Global Offering; (iii) the three largest public shareholders of the Company do not hold 
more than 50% of the H Shares in public hands at the time of the Listing in compliance with Rules 8.08(3) and 
8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at the time of the Listing in compliance 
with Rule 8.08(2) of the Listing Rules. 
COMMENCEMENT OF DEALINGS 
Share certificates will only become valid at 8:00 a.m. on Monday, 23 March 2026 provided that (i) the Global 
Offering has become unconditional in all respects at or before that time, and (ii) the right of termination as 
described in the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong 
Public Offering – Grounds for Termination” in the Prospectus has not been exercised. Investors who trade 
22

<<<PAGE 23>>>
Shares prior to the receipt of Share certificates or the Share certificates becoming valid evidence of title do so 
entirely at their own risk. 
Assuming that the Hong Kong Public Offering becomes unconditional at or before 8:00 a.m. in Hong Kong on 
Monday, 23 March 2026, it is expected that dealings in the Shares on the Stock Exchange will commence at 
9:00 a.m. on Monday, 23 March 2026. The Shares will be traded in board lots of 100 Shares each and the stock 
code of the Shares will be 3355. 
By order of the Board 
FS.COM Limited 
Mr. Xiang Wei 
Chairman and executive Director 
Hong Kong, 20 March 2026 
As at the date of this announcement, the board of directors of the Company comprises: Mr. Xiang Wei and Mr. 
Zeng Di as executive directors; Mr. Peng Chao and Mr. Zhao Pan as non-executive directors; and Mr. Ran 
Long, Dr. Guo Fei and Ms. Wang Jing as independent non-executive directors. 
*For identification purpose only
23
