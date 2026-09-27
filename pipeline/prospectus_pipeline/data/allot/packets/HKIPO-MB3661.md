# 配发结果公告抽取任务：3661.HK SG Micro Corp - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**25/06/2026 22:21**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0625/2026062502076.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3661.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) and Hong 
Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States (including its 
territories and possessions, any state of the United States and the District of Columbia). This announcement does not constitute 
or form a part of any offer or solicitation to purchase or subscribe for the Offer Shares in the United States or in any other 
jurisdictions. The Offer Shares have not been, and will not be, registered under the United States Securities Act of 1933 as 
amended from time to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the United States. The 
Offer Shares may not be offered, sold, pledged or otherwise transferred within the United States, except pursuant to an exemption 
from the registration requirements of the U.S. Securities Act, and in compliance with any applicable state securities laws. The 
Offer Shares are being offered and sold outside the United States to investors that are not U.S. persons nor persons acquiring for 
the account or benefit of U.S. persons in reliance on Regulation S under the U.S. Securities Act. There will be no public offer of 
the Offer Shares in the United States.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase or 
subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated June 
17, 2026 (the “Prospectus”) issued by SG Micro Corp ( 聖邦微電子（北京）股份有限公司) (the “Company”) for detailed 
information about the Global Offering described below before deciding whether or not to invest in the H Shares thereby being 
offered. Any investment decision in relation to the Offer Shares should be taken solely in reliance on the information in the 
Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those defined in 
the Prospectus.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited, as stabilizing 
manager (the “Stabilizing Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, the extent 
permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect 
transactions with a view to stabilizing or supporting the market price of the H Shares at such price, in such amounts and in such 
manners as the Stabilizing Manager, its affiliates or any person acting for it may determine and at a level higher than that which 
might otherwise prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing Manager 
(or its affiliates or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will be 
conducted at the absolute discretion of the Stabilization Manager (or its affiliates or any person acting for it) and in what the 
Stabilizing Manager reasonably regards as the best interest of our Company, (b) may be discontinued at any time and (c) is 
required to be brought to an end within 30 days of the last day for lodging applications under the Hong Kong Public Offering 
(which is Thursday, July 23, 2026). Such stabilizing action, if taken, may be effected in all jurisdictions where it is permissible 
to do so, in each case in compliance with all applicable laws, rules and regulatory requirements, including the Securities and 
Futures (Price Stabilizing) Rules (Chapter 571 W of the Laws of Hong Kong), as amended, made under the Securities and Futures 
Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for longer than the 
stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day after the last day for lodging 
applications under the Hong Kong Public Offering (which is Thursday, July 23, 2026). After this date, when no further stabilizing 
action may be taken, demand for the H Shares, and therefore the price of the H Shares, could fall.
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on behalf of the Hong Kong 
Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting — Underwriting Arrangements and 
Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong 
Kong time) on the Listing Date (which is currently expected to be on Friday, June 26, 2026).

<<<PAGE 2>>>
2
SG Micro Corp
聖邦微電子（北京）股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under 
the Global Offering
:
54,001,200 H Shares (subject to  
the Over-allotment Option)
Number of Hong Kong Offer Shares
:
5,400,200 H Shares
Number of International Offer Shares
:
48,601,000 H Shares (subject to  
the Over-allotment Option)
Offer Price
:
HK$85.20 per H Share, plus brokerage of 
1.0%, AFRC transaction levy of 0.00015%, 
SFC transaction levy of 0.0027% and Stock 
Exchange trading fee of 0.00565% (payable 
in full on application in Hong Kong dollars 
and subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
3661
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
1 
 
SG MICRO CORP 
聖邦微電子(北京)股份有限公司 
ANNOUNCEMENT OF FINAL OFFER PRICE AND  
ALLOTMENT RESULTS 
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same meanings as 
those defined in the prospectus dated June 17, 2026 (the “Prospectus”) issued by SG Micro Corp (the 
“Company”). 
 
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could move 
substantially even with a small number of H Shares traded and should exercise extreme caution when 
dealing in the H Shares. 
SUMMARY 
Company Information 
Stock Code 
3661 
Stock short name 
SG MICRO 
Dealings commencement date 
June 26, 2026 
*see note at the end of the announcement 
Price Information 
Final Offer Price 
HK$85.20 
 
Offer Shares and Share Capital 
Number of Offer Shares 
54,001,200 
Number of Offer Shares in Hong Kong Public Offering 
5,400,200 
Number of Offer Shares in International Offering 
48,601,000 
Number of issued Shares upon Listing (before exercise of the 
Over-allotment Option) 
675,015,824 
 
 
Over-allocation 
No. of Offer Shares over-allocated 
8,100,100 
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases in 
the secondary market at prices that do not exceed the Offer Price or through deferred delivery or a 
combination of these means. In the event the Over-allotment Option is exercised, an announcement will be 
made on the Stock Exchange’s website. 
 
Proceeds 
Gross proceeds (Note) 
HK$4,600.9 million 
Less: Estimated listing expenses payable based on Final 
Offer Price 
HK$101.0 million 
Net proceeds 
HK$4,499.9 million 
 

<<<PAGE 4>>>
2 
 
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. 
The Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis.  
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING  
 
No. of valid applications 
153,878 
No. of successful applications 
34,304 
Subscription level  
251.73 times 
Claw-back triggered 
N/A 
No. of Offer Shares initially available under the Hong Kong Public 
Offering 
5,400,200 
Final no. of Offer Shares under the Hong Kong Public Offering 
5,400,200 
% of Offer Shares under the Hong Kong Public Offering to the Global 
Offering 
10% 
 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by name or identification document number or 
www.hkeipo.hk/IPOResult for the full list of allottees. 
INTERNATIONAL OFFERING 
 
No. of placees 
233 
Subscription Level  
23.5 times 
 
No. of Offer Shares initially available under the International Offering 48,601,000 
Final no. of Offer Shares under the International Offering  
48,601,000 
% of Offer Shares under the International Offering to the Global 
Offering  
90% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a waiver from 
strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) of Appendix F1 to 
the Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange to permit the Company to allocate 
certain Offer Shares in the International Offering to certain Existing Minority Shareholders and/or their close 
associates; and (b) a consent under Chapter 4.15 of the Guide for New Listing Applicants to permit the Company 
to, among other things, allocate further H Shares in the International Offering to certain existing Shareholders 
and/or their close associates, and the Cornerstone Investors, (i) none of the Offer Shares subscribed by the 
placees and the public have been financed directly or indirectly by the Company, any of the Directors, chief 

<<<PAGE 5>>>
3 
 
executive of the Company, controlling shareholders, substantial Shareholders, existing Shareholders of the 
Company or any of its subsidiaries or their respective close associates; and (ii) none of the placees and the public 
who have purchased the Offer Shares are accustomed to taking instructions from the Company, any of the 
Directors, chief executive of the Company, controlling shareholders, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates in relation to the 
acquisition, disposal, voting or other disposition of H Shares registered in his/her/its name or otherwise held by 
him/her/it. 
The placees in the International Offering include the following: 
Cornerstone Investors  
Investor 
No. of Offer 
Shares allocated 
% of total issued H 
Shares after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
share capital in the 
Company after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised) 
Existing shareholders 
or their close 
associates 
GIC Private Limited 
4,597,700 
8.51% 
0.68% 
Yes 
JPMorgan Asset 
Management (Asia 
Pacific) Limited 
(“JPMAMAPL”) 
4,505,700 
8.34% 
0.67% 
Yes 
CPE Ginkgo 
Investment Limited 
(“CPE Ginkgo”) 
3,494,200 
6.47% 
0.52% 
No 
Da Cheng International 
Asset Management 
Company Limited (“Da 
Cheng International”) 
275,800 
0.51% 
0.04% 
No 
Dajia Life Insurance 
Co., Ltd. (大家人壽保
險股份有限公司) 
(“Dajia Life”) 
275,800 
0.51% 
0.04% 
Yes 
Dymon Asia Multi-
Strategy Investment 
Master Fund 
(“DAMSIMF”) 
275,800 
0.51% 
0.04% 
No 
First Sentier Investors 
(Hong Kong) Limited 
(“First Sentier 
Investors”) 
1,839,000 
3.41% 
0.27% 
Yes 
GF Fund Management 
Co., Ltd. (廣發基金管
理有限公司) (“GF 
Fund Management”)  
919,500 
1.70% 
0.14% 
Yes 
GF International 
Investment 
Management Limited 
183,900 
0.34% 
0.03% 
Yes 

<<<PAGE 6>>>
4 
 
(廣發國際資產管理有
限公司) (“GF HK”) 
Golden Continent 
Global Vision Open-
ended Fund Company-
Value Opportunity 
Fund N0.2 (“Golden 
Continent”) 
275,800 
0.51% 
0.04% 
No 
Harvest Global 
Investments Limited 
(嘉實國際資產管理有
限公司) (“HGI”) 
275,800 
0.51% 
0.04% 
Yes 
HHLR Advisors, Ltd. 
(“HHLRA”) 
3,586,200 
6.64% 
0.53% 
No 
HHLRA (as the 
investment manager of 
an SMA managed for 
CPP Investments) 
919,500 
1.70% 
0.14% 
No 
Huadeng Tech Ace 
Investment Ltd 
(“Huadeng 
Technology”) 
459,700 
0.85% 
0.07% 
No 
HQ TELECOM 
SINGAPORE PTE. 
LTD. (“Huaqin 
Singapore”) 
643,600 
1.19% 
0.10% 
No 
Sungrow Power (Hong 
Kong) Co., Limited 
(“Sungrow Power”) 
367,800 
0.68% 
0.05% 
No 
ICBC Wealth 
Management Co., Ltd. 
(工銀理財有限責任公
司) (“ICBC Wealth”) 
275,800 
0.51% 
0.04% 
No 
iSoftStone Hong Kong 
Limited (“iSoftStone 
HK”) 
275,800 
0.51% 
0.04% 
No 
LMR Multi-Strategy 
Master Fund Limited 
(“LMR Master Fund”) 
275,800 
0.51% 
0.04% 
No 
Millennium Capital 
Management 
(Singapore) Pte. Ltd. 
(“Millennium 
Capital”) 
459,700 
0.85% 
0.07% 
No 
Ninety One Asia Pte. 
Limited (“Ninety One 
Asia”) 
275,800 
0.51% 
0.04% 
Yes 
Ocean Fine Industrial 
Limited (“Ocean Fine 
Industrial”) 
367,800 
0.68% 
0.05% 
No 

<<<PAGE 7>>>
5 
 
PSBC Wealth 
Management Co., Ltd. 
(中郵理財有限責任公
司) (“PSBC Wealth”) 
275,800 
0.51% 
0.04% 
No 
Taikang Life Insurance 
Co., Ltd (“Taikang 
Life”) 
735,600 
1.36% 
0.11% 
Yes 
Value Partners Hong 
Kong Limited  
928,700 
1.72% 
0.14% 
No 
Value Partners Limited  
174,700 
0.32% 
0.03% 
No 
Total 
26,941,300 
49.89% 
3.99% 
 
Notes: 
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering (assuming the Over-allotment Option is not 
exercised).  
2. 
In addition to the Offer Shares subscribed for as Cornerstone Investors, certain Cornerstone 
Investors were allocated further Offer Shares as placees in the International Offering. Please refer 
to the section headed “Allotment Results Details – International Offering – Allotees with 
Waivers/Consents Obtained” in this announcement for details. Only the Offer Shares subscribed for 
as Cornerstone Investors are subject to lock-up as indicated below. For details, please refer to the 
section headed “Lock-up Undertakings – Cornerstone Investors” in this announcement. 
 
Allotees with Waivers/Consents Obtained  
Investor 
No. of Offer 
Shares 
allocated 
% of total issued H 
Shares after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised) Note 5 
% of total issued 
share capital in 
the Company after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 6 
Relationship 
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C of the Placing Guidelines in relation to subscription for H Shares by Existing Minority 
Shareholders holding more than 1% of the issued share capital of the Company immediately prior to the 
completion of the Global Offering and/or their close associates Note 1 
GF Fund Management 
919,500 
1.70% 
0.14% 
GF Fund Management is a 
close associate of an 
existing Shareholder of the 
Company 
GF Fund HK 
183,900 
0.34% 
0.03% 
GF Fund HK is a close 
associate of an existing 
Shareholder of the 
Company 

<<<PAGE 8>>>
6 
 
Taikang Life 
735,600 
1.36% 
0.11% 
Taikang Life is a close 
associate of an existing 
Shareholder of the 
Company 
HGI Note 8 
349,300 
0.65% 
0.05% 
HGI is a close associate of 
an existing Shareholder of 
the Company 
Allotees with consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations 
of further H Shares to Cornerstone Investors Note 2 
GIC Private Limited 
1,380,000 
2.56% 
0.20% 
GIC Private Limited is a 
Cornerstone Investor and 
an existing shareholder of 
the Company  
JF Asset Management 
Ltd. ("JFAM") 
1,350,000 
2.50% 
0.20% 
JFAM is a close associate 
of JPMAMAPL 
J.P. Morgan Securities 
(Asia Pacific) Limited 
("JPMSAPL") 
2,800 
0.01% 
0.00% 
JPMSAPL is a close 
associate of JPMAMAPL 
Dajia Life 
73,500 
0.14% 
0.01% 
Dajia Life is a Cornerstone 
Investor and an existing 
shareholder of the 
Company  
First Sentier 
515,000 
0.95% 
0.08% 
First Sentier is a 
Cornerstone Investor and 
an existing shareholder of 
the Company  
HGI Note 8 
73,500  
0.14% 
0.01% 
HGI is a Cornerstone 
Investor and an existing 
shareholder of the 
Company  
Ninety One Asia 
73,500 
0.14% 
0.01% 
Ninety One Asia is a 
Cornerstone Investor and 
an existing shareholder of 
the Company  
Da Cheng 
International 
73,500 
0.14% 
0.01% Da Cheng International is a 
Cornerstone Investor 
DAMSIMF 
69,000 
0.13% 
0.01% 
DAMSIMF is a 
Cornerstone Investor 
Golden Continent 
69,000 
0.13% 
0.01% 
Golden Continent is a 
Cornerstone Investor 
HHLRA 
975,000 
1.81% 
0.14% 
HHLRA is a Cornerstone 
Investor 

<<<PAGE 9>>>
7 
 
Huadeng Technology 
124,000 
0.23% 
0.02% 
Huadeng Technology is a 
Cornerstone Investor 
ICBC Wealth Note 4 
91,900 
0.17% 
0.01% 
ICBC Wealth is a 
Cornerstone Investor 
ISoftStone HK 
183,900 
0.34% 
0.03% 
ISoftStone HK is a 
Cornerstone Investor 
LMR Master Fund 
69,000 
0.13% 
0.01% 
LMR Master Fund is a 
Cornerstone Investor 
Millennium Capital 
Management (Hong 
Kong) Limited 
("Millenium Capital 
HK") 
115,000 
0.21% 
0.02% 
Millennium Capital HK is 
a close associate of 
Millennium Capital, a 
Cornerstone Investor 
PSBC Wealth Note 5 
91,900 
0.17% 
0.01% 
PSBC Wealth is a 
Cornerstone Investor 
Value Partners 
Limited 
294,000 
0.54% 
0.04% 
Value Partners Limited is a 
Cornerstone Investor, as 
well as close associate of 
Value Partners Hong Kong 
Limited, another 
Cornerstone Investor 
HQ TELECOM 
SINGAPORE PTE. 
LTD. 
459,700 
0.85% 
0.07% 
HQ TELECOM 
SINGAPORE PTE. LTD. 
is a cloase associate of 
Huaqin Singapore, a 
Cornerstone Investor 
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for 
New Listing Applicants in relation to allocations to connected clients Note 3 
ICBC Wealth (as a 
cornerstone investor) 
275,800 
0.51% 
0.04% 
Connected client 
ICBC Wealth (as a 
placee) 
91,900 
0.17% 
0.01% 
Connected client 
China Asset 
Management (Hong 
Kong) Limited  
91,900 
0.17% 
0.01% 
Connected client 

<<<PAGE 10>>>
8 
 
Bosera Asset 
Management 
(International) Co., 
Limited  
91,900 
0.17% 
0.01% 
Connected client 
Fullgoal Asset 
Management (HK) 
Limited  
91,900 
0.17% 
0.01% 
Connected client 
UBS Asset 
Management 
(Singapore) Ltd. 
322,000 
0.60% 
0.05% 
Connected client 
HSBC Global Asset 
Management (Hong 
Kong) Limited 
322,000 
0.60% 
0.05% 
Connected client 
CICC Financial 
Trading Limited (in 
connection with the 
Gaoyi OTC Swaps) 
64,300 
0.12% 
0.01% 
Connected client 
CICC Financial 
Trading Limited (in 
connection with the 
Longrising OTC 
Swaps) 
18,000 
0.03% 
0.00% 
Connected client 
Huatai Capital 
Investment Limited 
(in connection with 
the Chonghu TRS) 
459,700 
0.85% 
0.07% 
Connected client 
Notes: 
1. 
The Stock Exchange has granted a waiver from strict compliance with the requirements under Rule 
10.04 of the Listing Rules and consent under Paragraph 1C of the Placing Guidelines to permit H 
Shares in the International Offering to be placed to certain Existing Minority Shareholders. Please 
refer to the section headed “Waivers and Exemptions – Allocation of H Shares to Existing Minority 
Shareholders and their Close Associates” of the Prospectus for details. 
To the best knowledge, information and belief of the Company after due enquiry, details of the 
allocations to the Existing Minority Shareholder holding more than 1% of the issued share capital of 
the Company immediately prior to the completion of the Global Offering have been disclosed in this 
announcement. 
2. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents 
the number of Offer Shares allocated to the investors as placees in the International Offering. For 
allocations of Offer Shares to the relevant investors as Cornerstone Investors, please refer to the 
section headed “Allotment Results Details – International Offering – Cornerstone Investors” in this 
announcement. For details of the consent under Chapter 4.15 of the Guide for New Listing Applicants 
in relation to allocations of further H Shares to the existing Shareholders and/or their close associates 
and Cornerstone Investors, please refer to the section headed “Others/Additional Information – 
Allocations of Offer Shares to the existing Shareholders and/or their close associates and Cornerstone 
Investors with a consent under Chapter 4.15 of the Guide for New Listing Applicants” in this 

<<<PAGE 11>>>
9 
 
announcement. 
3. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations to connected clients, please refer to the 
section headed “Others / Additional Information – Placing to connected clients with a prior consent 
under paragraph 1C(1) of the Placing Guidelines” in this announcement. 
4. 
For the purpose of participation in the International Offering as a placee, ICBC Wealth has engaged 
each of Everbright PGIM Fund and Great Wall Fund Management Co., Ltd., who is an asset manager 
that is a qualified domestic international investor as approved by the relevant PRC authority, to 
subscribe for and hold such Offer Shares on a non-discretionary basis on behalf of ICBC Wealth. Each 
of Everbright PGIM Fund and Great Wall Fund Management Co., Ltd.is an independent third party 
of ICBC Wealth. 
5. 
For the purpose of participation in the International Offering as a placee, PSBC Wealth has engaged 
GF SECURITIES ASSET MANAGEMENT (GUANGDONG) CO., LTD who is an asset manager that 
is a qualified domestic international investor as approved by the relevant PRC authority, to subscribe 
for and hold such Offer Shares on a non-discretionary basis on behalf of PSBC Wealth. GF 
SECURITIES ASSET MANAGEMENT (GUANGDONG) CO., LTD is an independent third party of 
PSBC Wealth. 
6. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering (assuming the Over-allotment Option is not exercised).  
7. 
Not taking into account any A Shares held by the relevant investors. The figures are based on 
assumption that the Over-allotment Option is not exercised. 
8. 
HGI is an existing Shareholder with 1% or more interest in the Company, and the 349,300 H Shares 
subscribed by HGI include 275,800 H Shares as a cornerstone investment and 73,500 under the placee 
tranche. 
 
LOCK-UP UNDERTAKINGS 
Controlling Shareholders  
Name 
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing 
% of total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing (assuming the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
share capital in the 
Company subject to 
lock-up undertakings 
upon Listing 
(assuming the Over-
allotment 
Option is not 
exercised) 
Last day subject to 
the lock-up 
undertakings 
Chongqing 
Hongshun Xiangtai 
Enterprise 
Management Co., 
Ltd. (重慶鴻順祥泰
企業管理有限公司) 
(“Hongshun 
Xiangtai”) 
221,512,150 
- 
32.82% 
December 25, 2026 
(First Six-Month 
Period)Note 1 
June 25, 2027 
(Second Six-Month 
Period)Note 2 

<<<PAGE 12>>>
10 
 
Chongqing Baoli 
Hongya Enterprise 
Management Co., 
Ltd. (重慶寶利弘雅
企業管理有限公司) 
(“Baoli Hongya”) 
221,512,150 
- 
32.82% 
December 25, 2026 
(First Six-Month 
Period)Note 1 
June 25, 2027 
(Second Six-Month 
Period)Note 2 
Power Trend 
International 
Development 
Limited (弘威國際 
發展有限公司) 
(“Power Trend”) 
221,512,150 
- 
32.82% 
December 25, 2026 
(First Six-Month 
Period)Note 1 
June 25, 2027 
(Second Six-Month 
Period)Note 2 
Dr. Zhang Shilong 
(張世龍) (“Dr. 
Zhang”) 
221,512,150 
- 
32.82% 
December 25, 2026 
(First Six-Month 
Period)Note 1 
June 25, 2027 
(Second Six-Month 
Period)Note 2 
Ms. Zhang Qin (張
勤) (“Ms. Zhang”) 
221,512,150 
- 
32.82% 
December 25, 2026 
(First Six-Month 
Period)Note 1 
June 25, 2027 
(Second Six-Month 
Period)Note 2 
Mr. Lin Lin (林林) 
221,512,150 
- 
32.82% 
December 25, 2026 
(First Six-Month 
Period)Note 1 
June 25, 2027 
(Second Six-Month 
Period)Note 2 
Ms. Wen Li 
221,512,150 
- 
32.82% 
December 25, 2026 
(First Six-Month 
Period)Note 1 
June 25, 2027 
(Second Six-Month 
Period)Note 2 
Notes: 
1. 
The Controlling Shareholders may dispose of or transfer Shares after the indicated date subject to 
that the Controlling Shareholders will not cease to be a Controlling Shareholder. 
2. 
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares 
after the indicated date. 
 
 
Cornerstone Investors  

<<<PAGE 13>>>
11 
 
Name 
Number of H Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing 
% of total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing (assuming the 
Over-allotment 
Option is not 
exercised)Note 1 
% of total issued 
share capital in the 
Company subject to 
lock-up undertakings 
upon Listing 
(assuming the Over-
allotment 
Option is not 
exercised) 
Last day subject to 
the lock-up 
undertakingsNote 2 
GIC Private Limited 
4,597,700 
8.51% 
0.68% December 25, 2026 
JPMAMAPL 
4,505,700 
8.34% 
0.67% December 25, 2026 
CPE Ginkgo 
3,494,200 
6.47% 
0.52% December 25, 2026 
Da Cheng 
International 
275,800 
0.51% 
0.04% December 25, 2026 
Dajia Life 
275,800 
0.51% 
0.04% December 25, 2026 
DAMSIMF 
275,800 
0.51% 
0.04% December 25, 2026 
First Sentier 
Investors 
1,839,000 
3.41% 
0.27% December 25, 2026 
GF Fund 
Management 
919,500 
1.70% 
0.14% December 25, 2026 
GF Fund HK 
183,900 
0.34% 
0.03% December 25, 2026 
Golden Continent 
275,800 
0.51% 
0.04% December 25, 2026 
HGI 
275,800 
0.51% 
0.04% December 25, 2026 
HHLRA 
3,586,200 
6.64% 
0.53% December 25, 2026 
HHLRA (as the 
investment manager 
of an SMA managed 
for CPP Investments) 
919,500 
1.70% 
0.14% December 25, 2026 
Huadeng Technology 
459,700 
0.85% 
0.07% December 25, 2026 

<<<PAGE 14>>>
12 
 
Huaqin Singapore 
643,600 
1.19% 
0.10% December 25, 2026 
Sungrow Power 
367,800 
0.68% 
0.05% December 25, 2026 
ICBC Wealth 
275,800 
0.51% 
0.04% December 25, 2026 
ISoftStone HK 
275,800 
0.51% 
0.04% December 25, 2026 
LMR Master Fund 
275,800 
0.51% 
0.04% December 25, 2026 
Millennium Capital 
459,700 
0.85% 
0.07% December 25, 2026 
Ninety One Asia 
275,800 
0.51% 
0.04% December 25, 2026 
Ocean Fine Industrial 
367,800 
0.68% 
0.05% December 25, 2026 
PSBC Wealth 
275,800 
0.51% 
0.04% December 25, 2026 
Taikang Life 
735,600 
1.36% 
0.11% December 25, 2026 
Value Partners Hong 
Kong Limited 
928,700 
1.72% 
0.14% December 25, 2026 
Value Partners 
Limited 
174,700 
0.32% 
0.03% December 25, 2026 
Total 
26,941,300 
49.89% 
3.99% 
 
Notes: 
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering. 
2. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on 
December 25, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or 
transferring H Shares subscribed pursuant to the relevant cornerstone investment agreements after 
the indicated date. 
 

<<<PAGE 15>>>
13 
 
PLACEE CONCENTRATION ANALYSIS  
Placees* 
Number of H 
Shares allotted 
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
Over- allotment 
Option is fully 
exercised and 
new H Shares are 
issued) 
Allotment as % 
of total Offer 
Shares (assuming 
no exercise of the 
Over-allotment 
Option) 
Allotment as % 
of total Offer 
Shares (assuming 
the Over-
allotment Option 
is fully exercised 
and new H 
Shares are 
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
exercised and 
new H Shares are 
issued) 
Top 1 
5,977,700 
12.30% 
10.54% 
11.07% 
9.63% 
5,977,700 
0.89% 
0.88% 
Top 5 
23,162,300 
47.66% 
40.85% 
42.89% 
37.30% 
23,162,300 
3.43% 
3.39% 
Top 10 
28,901,200 
59.47% 
50.97% 
53.52% 
46.54% 
28,901,200 
4.28% 
4.23% 
Top 25 
39,033,300 
80.31% 
68.84% 
72.28% 
62.85% 
39,033,300 
5.78% 
5.71% 
 
Note: 
* 
Ranking of placees is based on the number of H Shares allotted to the placees. 
 
 

<<<PAGE 16>>>
14 
 
H SHAREHOLDER CONCENTRATION ANALYSIS  
H 
Shareholde
rs 
* 
Number of H 
Shares allotted 
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
Over- allotment 
Option is fully 
exercised and 
new H Shares are 
issued) 
Allotment as % 
of total Offer 
Shares (assuming 
no exercise of the 
Over-allotment 
Option) 
Allotment as % 
of total Offer 
Shares (assuming 
the Over-
allotment Option 
is fully exercised 
and new H 
Shares are 
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
share capital upon 
Listing (assuming 
the Over-
allotment Option 
is fully exercised 
and new H Shares 
are issued) 
Top 1 
5,977,700 
12.30% 
10.54% 
11.07% 
9.63% 
5,977,700 
0.89% 
0.88% 
Top 5 
23,162,300 
47.66% 
40.85% 
42.89% 
37.30% 
23,162,300 
3.43% 
3.39% 
Top 10 
28,901,200 
59.47% 
50.97% 
53.52% 
46.54% 
28,901,200 
4.28% 
4.23% 
Top 25 
39,033,300 
80.31% 
68.84% 
72.28% 
62.85% 
39,033,300 
5.78% 
5.71% 
 
Note: 
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing. 
 
 

<<<PAGE 17>>>
15 
 
SHAREHOLDER CONCENTRATION ANALYSIS 
Shareholders
* 
Number of H 
Shares 
allotted 
Allotment as 
% of 
International 
Offering 
(assuming no 
exercise of the 
Over-
allotment 
Option) 
Allotment as % 
of International 
Offering 
(assuming the 
Over- allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
Allotment as 
% of total 
Offer Shares 
(assuming no 
exercise of the 
Over- 
allotment 
Option) 
Allotment as % 
of total Offer 
Shares 
(assuming the 
Over- allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
Number of 
H Shares 
held upon 
Listing 
Number of 
Shares held 
upon Listing# 
% of total issued 
share capital upon 
Listing 
(assuming no 
exercise of the 
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
0 
 221,512,150 32.82% 
32.43% 
Top 5 
1,930,900 
3.97% 
3.41% 
3.58% 
3.11% 
1,930,900  275,904,893 40.87% 
40.39% 
Top 10 
14,113,600 29.04% 
24.89% 
26.14% 
22.73% 
14,113,600  313,678,966 46.47% 
45.92% 
Top 25 
23,364,200 48.07% 
41.21% 
43.27% 
37.62% 
23,364,200  372,178,931 55.14% 
54.48% 
 
Note: 
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon Listing. 
# 
Among the top 25 placees, certain placees are also existing Shareholders. To the best knowledge, information and belief of the Company after due enquiry, details of the allocations 
to the Existing Minority Shareholder holding more than 1% of the issued share capital of the Company immediately prior to the completion of the Global Offering have been disclosed 
in this announcement. Please refer to the section headed “Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C of the 
Placing Guidelines in relation to subscription for H Shares by Existing Minority Shareholders holding more than 1% of the issued share capital of the Company immediately prior to 
the completion of the Global Offering and/or their close associates”. For the top 25 placees who are also existing shareholders held less than 0.05% of the issued share capital of the 
Company immediately prior to the completion of the Global Offering, the number of A Shares held by them is not counted into the number of Shares held upon Listing. 
 

<<<PAGE 18>>>
16 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING  
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by the 
public will be conditionally allocated on the basis set out below:  
 
 
Approximate 
 
 
Pool A 
percentage 
 
 
allotted of the 
Number of 
Number 
total number of 
H Shares 
of valid 
H Shares applied 
applied for 
applications Basis of allocation/ballot 
for 
100 
71,4607,146 out of 71,460 applicants to receive 100 H Shares 
10.00% 
200 
8,2361,017 out of 8,236 applicants to receive 100 H Shares 
6.17% 
300 
3,601503 out of 3,601 applicants to receive 100 H Shares 
4.66% 
400 
2,079317 out of 2,079 applicants to receive 100 H Shares 
3.81% 
500 
12,5512,045 out of 12,551 applicants to receive 100 H Shares 
3.26% 
600 
1,722297 out of 1,722 applicants to receive 100 H Shares 
2.87% 
700 
904164 out of 904 applicants to receive 100 H Shares 
2.59% 
800 
788148 out of 788 applicants to receive 100 H Shares 
2.35% 
900 
719140 out of 719 applicants to receive 100 H Shares 
2.16% 
1,000 
10,8162,174 out of 10,816 applicants to receive 100 H Shares 
2.01% 
1,500 
2,645602 out of 2,645 applicants to receive 100 H Shares 
1.52% 
2,000 
2,706671 out of 2,706 applicants to receive 100 H Shares 
1.24% 
2,500 
1,693450 out of 1,693 applicants to receive 100 H Shares 
1.06% 
3,000 
1,758493 out of 1,758 applicants to receive 100 H Shares 
0.93% 
3,500 
1,299382 out of 1,299 applicants to receive 100 H Shares 
0.84% 
4,000 
1,163356 out of 1,163 applicants to receive 100 H Shares 
0.77% 
4,500 
795253 out of 795 applicants to receive 100 H Shares 
0.71% 
5,000 
2,144702 out of 2,144 applicants to receive 100 H Shares 
0.65% 
6,000 
1,673579 out of 1,673 applicants to receive 100 H Shares 
0.58% 
7,000 
1,069388 out of 1,069 applicants to receive 100 H Shares 
0.52% 
8,000 
966365 out of 966 applicants to receive 100 H Shares 
0.47% 
9,000 
837328 out of 837 applicants to receive 100 H Shares 
0.44% 
10,000 
5,6442,280 out of 5,644 applicants to receive 100 H Shares 
0.40% 
20,000 
4,1822,084 out of 4,182 applicants to receive 100 H Shares 
0.25% 
30,000 
2,1731,225 out of 2,173 applicants to receive 100 H Shares 
0.19% 
40,000 
1,186 730 out of 1,186 applicants to receive 100 H Shares 
0.15% 
50,000 
1,766 1,162 out of 1,766 applicants to receive 100 H Shares 
0.13% 
Total 
146,575 Total number of Pool A successful applicants: 27,001 
 
 
 
 
 
 
 

<<<PAGE 19>>>
17 
 
 
 
Pool B 
Approximate 
 
 
percentage 
 
 
allotted of the 
Number 
Number 
total number of 
of H Shares 
of valid 
H Shares applied 
applied for 
applications 
Basis of allocation/ballot 
for 
60,000 
3,942 200 H Shares plus 3,469 out of 3,942 applicants to receive an additional 100 H Shares 
0.48% 
70,000 
615 300 H Shares plus 72 out of 615 applicants to receive an additional 100 H Shares 
0.45% 
80,000 
434 300 H Shares plus 147 out of 434 applicants to receive an additional 100 H Shares 
0.42% 
90,000 
242 300 H Shares plus 132 out of 242 applicants to receive an additional 100 H Shares 
0.39% 
100,000 
1,139 300 H Shares plus 844 out of 1,139 applicants to receive an additional 100 H Shares 
0.37% 
200,000 
453 500 H Shares plus 152 out of 453 applicants to receive an additional 100 H Shares 
0.27% 
300,000 
165 600 H Shares plus 70 out of 165 applicants to receive an additional 100 H Shares 
0.21% 
400,000 
54 700 H Shares plus 33 out of 54 applicants to receive an additional 100 H Shares 
0.19% 
500,000 
55 800 H Shares plus 22 out of 55 applicants to receive an additional 100 H Shares 
0.17% 
600,000 
25 900 H Shares plus 10 out of 25 applicants to receive an additional 100 H Shares 
0.16% 
700,000 
22 1,000 H Shares plus 4 out of 22 applicants to receive an additional 100 H Shares 
0.15% 
800,000 
24 1,000 H Shares plus 21 out of 24 applicants to receive an additional 100 H Shares 
0.14% 
900,000 
8 1,100 H Shares plus 4 out of 8 applicants to receive an additional 100 H Shares 
0.13% 
1,000,000 
52 1,200 H Shares 
0.12% 
1,500,000 
19 1,500 H Shares 
0.10% 
2,000,000 
14 1,800 H Shares 
0.09% 
2,700,100 
40 2,100 H Shares 
0.08% 
Total 
7,303 
Total number of Pool B successful applicants: 7,303 
 
 
 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries. 
 

<<<PAGE 20>>>
18 
 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of which 
consent has been obtained, the Company has complied with the Listing Rules and guidance materials in 
relation to the placing, allotment and listing of the Company’s H Shares. 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the 
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by 
them was the same as the final Offer Price in addition to any brokerage, AFRC transaction levy, SFC 
transaction levy and trading fee payable. 
OTHERS / ADDITIONAL INFORMATION 
Allocations of Offer Shares to the existing Shareholders and/or their close associates and 
Cornerstone Investors with a consent under paragraph 18 of Chapter 4.15 of the Guide for New 
Listing Applicants 
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 of the 
Guide for New Listing Applicants to permit the Company to allocate further Offer Shares in the 
International Offering to certain existing Shareholders and/or their close associates, and Cornerstone 
Investors as placees, subject to the following conditions (“Allocation to Size-based Exemption 
Participants”): 
(a) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion; 
(b) 
the Offer Shares allocated to all existing Shareholders and their close associates (whether as 
cornerstone investors and/or as placees) as permitted under the Size-based Exemption (as defined 
in the Guide for New Listing Applicants) do not exceed 30% of the total number of the H Shares 
offered under the Global Offering; 
(c) 
the Allocation to Size-based Exemption Participants will not affect the Company’s ability to 
satisfy its public float requirement as prescribed by the Stock Exchange under the waiver from 
strict compliance with the requirements of Rule 8.08(1) and 19A.13A of the Listing Rules;  
(d) 
each Director, chief executive and controlling shareholder of the Company confirms that no 
securities have been allocated to them or their respective close associates under the Size-based 
Exemption; and 
(e) 
details of the allocation to existing Shareholders and/or their close associates and Cornerstone 
Investors under the Size-based Exemption will be disclosed in this announcement. 
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted by 
the Stock Exchange. 
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates and 
Cornerstone Investors, please refer to the section headed “Allotment Results Details – International 
Offering – Allotees with Waivers/Consents Obtained” in this announcement. 
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines 
Under the International Offering, certain Offer Shares were placed to connected clients of their connected 
distributors pursuant to the Placing Guidelines. Details of the placement to connected clients are set out 

<<<PAGE 21>>>
19 
 
below. The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, 
consents under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such Offer 
Shares in the International Offering to the connected clients. The allocation of Offer Shares to such 
connected clients is in compliance with all the conditions under the consent granted by the Stock 
Exchange. 
 
 
Part A - Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on 
behalf of independent third parties 
 
N
o. 
Connected 
Distributo
r 
Connected Client 
Relationship with 
the Connected 
Distributor 
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
Numb
er of 
Offer 
Shares 
allocat
ed to 
the 
connec
ted 
client 
Approxi
mate 
Percenta
ge of 
total 
number 
of Offer 
Shares  
Approxi
mate 
percenta
ge of 
total 
Shares in 
issue 
immedia
tely 
following 
the 
completi
on of 
Global 
Offering  
1. 
ICBC 
Internation
al 
Securities 
Limited 
("ICBC") 
ICBC Wealth Management Co., 
Ltd. ("ICBC Wealth")(1) 
ICBC Wealth is a 
member of the 
same group with 
ICBC 
No 
As a 
corners
tone 
investo
r: 
275,80
0 
0.51% 
0.04% 
As a 
placee: 
91,900 
0.17% 
0.01% 
2. 
CITIC 
Securities 
Brokerage 
(HK) 
Limited 
("CSB") 
China Asset Management 
(Hong Kong) Limited (“China 
AM HK”)(2) 
China AM HK is a 
member of the 
same group with 
CSB 
No 
91,900 
0.17% 
0.01% 
3. 
China 
Merchants 
Securities 
(HK) Co., 
Limited 
("CMS") 
Bosera Asset Management 
(International) Co., Limited 
("Bosera")(3) 
Bosera is a member 
of the same group 
with CMS 
No 
91,900 
0.17% 
0.01% 
4. 
Haitong 
Internation
al 
Securities 
Company 
Limited 
Fullgoal Asset Management 
(HK) Limited ("Fullgoal AM 
HK")(4) 
Fullgoal AM HK is 
a member of the 
same group with 
Haitong 
No 
91,900 
0.17% 
0.01% 

<<<PAGE 22>>>
20 
 
("Haitong"
) 
5. 
UBS AG 
Hong 
Kong 
Branch and 
UBS AG 
Singapore 
Branch 
UBS Asset Management 
(Singapore) Ltd. ("UBS 
GAM")(5) 
UBS GAM is a 
member of the 
same group with 
UBS AG Hong 
Kong Branch and 
UBS AG Singapore 
Branch 
No 
322,00
0 
0.60% 
0.05% 
6. 
The 
Hongkong 
and 
Shanghai 
Banking 
Corporatio
n Limited 
("HSBC") 
HSBC Global Asset 
Management (Hong Kong) 
Limited ("HSBC GAM")(6) 
HSBC GAM is a 
member of the 
same group with 
HSBC 
No 
322,00
0 
0.60% 
0.05% 
 

<<<PAGE 23>>>
21 
 
Part B - Connected Clients holding the beneficial interest of the Offer Shares on a non-discretionary basis 
on behalf of independent third parties 
N
o. 
Connected 
Distributo
r 
Connected Client 
Relationship with 
the Connected 
Distributor 
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
Numb
er of 
Offer 
Shares 
allocat
ed to 
the 
connec
ted 
client 
Approxi
mate 
Percenta
ge of 
total 
number 
of Offer 
Shares  
Approxi
mate 
percenta
ge of 
total 
Shares in 
issue 
immedia
tely 
following 
the 
completi
on of 
Global 
Offering  
1. 
China 
Internation
al Capital 
Corporatio
n Hong 
Kong 
Securities 
Limited 
("CICCH
KS") 
CICC Financial Trading 
Limited ("CICC FT") (in 
connection with the Gaoyi OTC 
Swaps) (7) 
CICC FT is a 
member of the 
same group with 
CICCHKS 
No  
64,300 
0.12% 
0.01% 
2. 
CICCHKS 
CICC FT (in connection with 
the Longrising OTC Swaps)(8) 
CICC FT is a 
member of the 
same group with 
CICCHKS 
No  
18,000 
0.03% 
0.00% 
3. 
Huatai 
Financial 
Holdings 
(Hong 
Kong) 
Limited 
("HTFH") 
Huatai Capital Investment 
Limited ("HTCI") (in 
connection with the Chonghu 
TRS)(9)(10) 
HTCI is a member 
of the same group 
with HTFH 
No  
459,70
0 
0.85% 
0.07% 
 
Notes: 
 
(1) ICBC becomes a distributor of the Global Offering after issue of the Prospectus. ICBC Wealth Management Co., Ltd. ("ICBC 
Wealth"), a cornerstone investor, is considered as member of the same group with ICBC, and therefore constitutes a "connected 
client" of ICBC. In addition, ICBC Wealth also participates in the Global Offering as a placee. For the purpose of participation 
in the International Offering as a placee, ICBC Wealth has engaged each of Everbright PGIM Fund and Great Wall Fund 
Management Co., Ltd., who is an asset manager that is a qualified domestic international investor as approved by the relevant 
PRC authority, to subscribe for and hold such Offer Shares on a non-discretionary basis on behalf of ICBC Wealth. Each of 
Everbright PGIM Fund and Great Wall Fund Management Co., Ltd. is an independent third party of ICBC Wealth. ICBC Wealth 
will hold the Offer Shares in its capacity as the discretionary investment manager of certain wealth management products. To 
the best knowledge of ICBC Wealth and after making all reasonable enquiries, each of the underlying clients of ICBC Wealth 
together with their ultimate beneficial owners, is an independent third party of ICBC Wealth, ICBC and the companies which 
are members of the same group of ICBC. None of the underlying clients of ICBC Wealth hold 30% or more interest in such 
products. 
 
(2) CSB is a distributor of the Global Offering. China AM HK will hold the Offer Shares in its capacity as the discretionary fund 
manager managing assets on behalf of its underlying clients, and details of the funds managed are as follows: 

<<<PAGE 24>>>
22 
 
Name of the funds to which the Offer 
Shares will be allocated 
Whether any investor holds 30% or 
more interest in the fund 
Ultimate Beneficial Owner with 30% 
or more interests and Shareholding 
(%) 
CHINAAMC 
SELECT 
GREATER 
CHINA TECHNOLOGY FUND 
No 
N/A 
CHINAAMC FUND - CHINAAMC 
CHINA OPPORTUNITIES FUND 
No 
N/A 
CHINAAMC CHINA FOCUS FUND 
Yes 
Manulife Financial Corporation (a 
company listed on the Hong Kong Stock 
Exchange, stock code: 0945) 
CHINAAMC CHINA GROWTH FUND 
(SICAV) 
Yes 
Yuanta Financial Holdings Co., Ltd. (a 
company listed on the Taiwan Stock 
Exchange, ticker: 2885) 
ICBC 
(ASIA) 
LTD-CHINAAMC-
BSCOMC LTD 
Yes 
BSCOMC Limited (ultimately owned 
by State-owned Assets Supervision and 
Administration Commission of People's 
Government of Beijing Municipality) 
To the best knowledge of China AM HK, each of the underlying clients of China AM HK, together with their ultimate beneficial 
owners holding 30% or more interest, is an independent third party of China AM HK, CSB and the companies which are 
members of the same group of CSB.  
 
(3) CMS is a distributor of the Global Offering. Bosera will hold the Offer Shares in its capacity as the discretionary fund manager 
managing assets on behalf of its underlying clients, and details of the funds managed are as follows:  
Name of the funds to which the Offer 
Shares will be allocated 
Whether any investor holds 30% or 
more interest in the fund 
Ultimate Beneficial Owner with 30% 
or more interests and Shareholding 
(%) 
Bosera Hong Kong Equity Plus Fund 
(SFC Authorised Fund) 
No 
N/A 
Bosera Global Select Equity Fund SP 
Yes 
Zhang Lei (张雷) 
Navigator Technology Limited IPO 
Mandate  
Yes 
Zheng Fuhua (郑复花) 
Fortuna Capital Management Limited 
IPO  Mandate 
Yes 
Yang Dehui (杨德会) 
Bosera China New Opportunities Fund 
SP 
No 
N/A 
Bosera 
Growth 
Premium 
Global 
Equity Strategy Fund SP 
Yes 
Guo Feng (郭峰) 
KB CHINA MAINLAND FD BOSERA 
No 
N/A 
Bosera 
Growth 
Premium 
Global 
Equity Strategy Fund SP2 
Yes 
Guangdong 
Dongfang 
Precision 
Science 
& 
Technology 
Co., 
Ltd 
("Dongfang Precision Science", a 
company listed on the Shenzhen Stock 
Exchange, stock code: 002611) 
Bosera 
Greater 
China 
Enhanced 
Return Bond Fund  (SFC Authorised 
Fund) 
No 
N/A 
Bosera 
Growth 
Premium 
Global 
Equity Strategy Fund SP3 
Yes 
Huang Liya (黄丽亚) 
Bosera 
Growth 
Premium 
Global 
Equity Strategy Fund SP4 
Yes 
Dongfang Precision Science 
 
To the best knowledge of Bosera, each of the underlying client of Bosera, together with its ultimate beneficial owner holding 
30% or more interest, is an independent third party of Bosera, CMS and the companies which are members of the same group 
of CMS. 
 
(4) Haitong is a distributor of the Global Offering. Fullgoal AM HK will hold the Offer Shares in its capacity as the discretionary 
fund manager of Fullgoal China Circle Fund and HI-Aktien China 1-SFonds, managing assets on behalf of its underlying clients, 
and none of the investors hold 30% or more interest in the fund. To the best knowledge of Fullgoal AM HK, the underlying 
client of Fullgoal AM HK, together with its ultimate beneficial owner holding 30% or more interest, is an independent third 
party of Fullgoal AM HK, Haitong and the companies which are members of the same group of Haitong. 

<<<PAGE 25>>>
23 
 
 
(5) Each of UBS AG Hong Kong Branch and UBS AG Singapore Branch is a distributor of the Global Offering. UBS GAM will 
hold the Offer Shares in its capacity as the discretionary fund manager managing assets on behalf of its underlying clients. To 
the best knowledge of USB GAM, each of the underlying clients of UBS GAM, together with their ultimate beneficial owner 
holding 30% or more interest, is an independent third party of USB GAM, UBS AG Hong Kong Branch, UBS AG Singapore 
Branch and the companies which are members of the same group of UBS AG Hong Kong Branch and UBS AG Singapore 
Branch. 
 
(6) HSBC is a distributor of the Global Offering. HSBC GAM will hold the Offer Shares in its capacity as the discretionary fund 
manager managing assets on behalf of its underlying clients. To the best knowledge of HSBC GAM after due enquiry, each of 
its underlying clients is an independent third party of HSBC GAM, HSBC, and the companies which are members of the same 
group of HSBC. 
 
(7) CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one OTC swap 
transactions (the “Gaoyi OTC Swaps”) with each other and the ultimate clients (the “CICC FT Ultimate Clients (Gaoyi)”), 
pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the Gaoyi OTC Swaps while the 
economic risks and returns of the underlying Offer Shares are passed to the CICC FT Ultimate Clients (Gaoyi), subject to 
customary fees and commissions. The Gaoyi OTC Swaps will be fully funded by the CICC FT Ultimate Clients (Gaoyi). During 
the terms of the Gaoyi OTC Swaps, all economic returns of the Offer Shares subscribed by CICC FT will be passed to the CICC 
FT Ultimate Clients (Gaoyi) and all economic loss shall be borne by the CICC FT Ultimate Clients (Gaoyi) through the Gaoyi 
OTC Swaps, and CICC FT will not take part in any economic return or bear any economic loss in relation to the Offer Shares. 
The Gaoyi OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate Clients (Gaoyi) may request CICC FT to 
redeem it at their own discretions, upon which CICC FT shall dispose of the Offer Shares and settle Gaoyi OTC Swaps in cash 
in accordance with the terms and conditions of the Gaoyi OTC Swaps. Despite that CICC FT will hold the legal title of the Offer 
Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares during the terms of the Gaoyi OTC 
Swaps according to its internal policy. The CICC FT Ultimate Clients (Gaoyi) for purpose of this placee subscription are funds  
(the "Gaoyi Funds") managed by Shanghai Gaoyi Asset Management Partnership (Limited Partnership) (上海高毅資產管理
合夥企業(有限合 夥)) (“Shanghai Gaoyi”), including (i) Jintaiyang Gaoyi Guolu No.1 Chongyuan Fund (金太阳高毅国鹭1
号崇远基金), (ii) Gaoyi Guolu Xinyuan Private Securities Investment Fund (高毅国鹭信远私募证券投资基金), (iii) Gaoyi 
Renhao Long-term Value Langrun Private Securities Investment Fund (高毅任昊长期价值朗润私募证券投资基金), (iv) 
Gaoyi Renhao Zhenxuan Chunhe Private Securities Investment Fund (高毅任昊臻选春和私募证券投资基金), (v) Gaoyi 
Qingrui Jingxuan Ruixiang Convertible Bond Multi-Strategy Private Fund (高毅任昊精选承泽私募证券投资基金), (vi) Gaoyi 
Renhao Youxuan Zhifu Private Securities Investment Fund (高毅任昊优选致福私募证券投资基金), (vii) Gaoyi Qingrui No.6 
Ruixing Fund (高毅庆瑞6 号瑞行基金), (viii) Gaoyi Qingrui Zhenxuan Fengyuan Private Securities Investment Fund (高毅
庆瑞臻选沣源私募证券投资基金), and (ix) Gaoyi Qingrui Jingxuan Ruixiang Convertible Bond Multi-Strategy Private Fund 
(高毅庆瑞精选瑞祥可转债多策略私募基金), and none of the underlying clients of each of the Gaoyi Funds hold 30% or more 
interest in such fund. Shanghai Gaoyi is a limited partnership established in the PRC, which is engaged in asset management 
and investment management with a primary focus on investments in secondary market. The managing partner of Shanghai Gaoyi 
is Shanghai Gaoyi Investment Management Co., Ltd. (上海高毅投資管理 有限公司). Each of the CICC FT Ultimate Clients 
(Gaoyi) is an independent third party of CICC FT, CICCHKS and the companies which are members of the same group of 
CICCHKS 
 
(8) CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one OTC swap 
transactions (the “Longrising OTC Swaps”) with each other and the ultimate clients (the “CICC FT Ultimate Clients 
(Longrising)”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the Longrising 
OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed to the CICC FT Ultimate Clients 
(Longrising), subject to customary fees and commissions. The Longrising OTC Swaps will be fully funded by the CICC FT 
Ultimate Clients (Longrising). During the terms of the Longrising OTC Swaps, all economic returns of the Offer Shares 
subscribed by CICC FT will be passed to the CICC FT Ultimate Clients (Longrising) and all economic loss shall be borne by 
the CICC FT Ultimate Clients (Longrising) through the Longrising OTC Swaps, and CICC FT will not take part in any economic 
return or bear any economic loss in relation to the Offer Shares. The Longrising OTC Swaps are linked to the Offer Shares and 
the CICC FT Ultimate Clients (Longrising) may request CICC FT to redeem it at their own discretions, upon which CICC FT 
shall dispose of the Offer Shares and settle Longrising OTC Swaps in cash in accordance with the terms and conditions of the 
Longrising OTC Swaps. Despite that CICC FT will hold the legal title of the Offer Shares by itself, it will not exercise the voting 
rights attaching to the relevant Offer Shares during the terms of the Longrising OTC Swaps according to its internal policy. The 
CICC FT Ultimate Clients (Longrising) for purpose of this placee subscription are funds (the "Longrising Funds") managed 
by Tibet Longrising Asset Management Co., Ltd. (西藏源乐晟资产管理有限公司) (“Tibet Longrising”), including (i) 
Yuanlesheng Qiangye Private Equity Investment Fund (源乐晟强业私募证券投资基金); (ii) Yuanlesheng Qiangshu Private 
Equity Investment Fund (源乐晟强树私募证券投资基金); and (iii) Yuanlesheng Strong Private Equity Investment Fund (源乐

<<<PAGE 26>>>
24 
 
晟强势私募证券投资基金). The ultimate beneficial owners of the Longrising Funds are Zeng Xiaojie (曾晓洁) and Hu Caiyang 
(胡彩阳). Each of the CICC FT Ultimate Clients (Longrising) is an independent third party of CICC FT, CICCHKS and the 
companies which are members of the same group of CICCHKS. 
 
(9) Huatai Securities Co., Ltd. ("Huatai Securities"), the shares of which are listed on both the Shanghai Stock Exchange (stock 
code: 601688) and the Stock Exchange stock code: 6886), is one of the domestic securities firms licensed to undertake cross-
border derivatives trading activities. Huatai Securities entered into an ISDA agreement (the "ISDA Agreement") with its 
indirectly wholly-owned subsidiary, HTCI, to set out the principal terms of any future total return swap between Huatai 
Securities and HTCI. 
 
Pursuant to the ISDA Agreement, HTCI, which intends to participate in the Global Offering as a placee, will hold the beneficial 
interest of the Offer Shares on a non-discretionary basis as the single underlying holder under a back-to-back total return swap 
(the "Back-to-back TRS") to be entered by HTCI in connection with the a client TRS placed by and fully funded (i.e. with no 
financing provided by HTCI) by the Huatai ultimate clients, by which, HTCI will, subject to customary fees and commissions, 
pass the full economic exposure of the Offer Shares to the Huatai ultimate clients, which in effect, HTCI will hold the beneficial 
interest of the Offer Shares on behalf of the Huatai ultimate clients.  
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public offerings ("IPOs") 
in Hong Kong. However, PRC investors are permitted to invest in products issued by appropriate domestic securities firms 
licensed to undertake cross-border derivatives trading activities. In connection with such products, the licensed domestic 
securities firms, through their Hong Kong affiliates, may participate in Hong Kong IPOs either as placees or cornerstone 
investors (the "Cross-border Derivatives Trading Regime"). 
 
(10) Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the "Huatai Ultimate Clients (Chonghu)") 
cannot directly subscribe for the Offer Shares but may invest in derivative products issued by domestic securities firms licenced 
to undertake cross-border derivatives trading activities, such as Huatai Securities, with the Offer Shares as the underlying assets. 
Instead of directly subscribing for the Offer Shares, the Huatai Ultimate Clients (Chonghu), through its investment managers, 
will place a total return swap order (the "Chonghu TRS") with Huatai Securities in connection with the Company's IPO and 
Huatai Securities will place a Back-to-back TRS order to HTCI on the terms of the ISDA Agreement. In order to hedge its 
exposure under the Back-to-back TRS, HTCI participates in the Company’s IPO and subscribes the Offer Shares through placing 
order with HTFH during the International Offering. 
 
The Huatai Ultimate Clients (Chonghu) for purpose of this place subscription is Chonghu Xingcun No. 1 Private Equity 
Investment Fund (重湖星存1 号私募证券投资基金), whose discretionary fund manager is Hangzhou Chonghu Private Fund 
Management Co., Ltd. (杭州重湖私募基金管理有限公司). The ultimate beneficial owner of Huatai Ultimate Clients (Chonghu) 
with 30% or more interest is Xu Xin (徐昕). 
 
To the best of knowledge of HTCI and after making all reasonable enquiries, each of the Huatai Ultimate Clients (Chonghu) is 
an independent third party of HTCI, HTFH and the companies which are members of the same group of HTFH. 
 
DISCLAIMERS 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong Kong 
Securities Clearing Company Limited take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability whatsoever for 
any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe 
for the Offer Shares in the United States or in any other jurisdictions. The Offer Shares have not been, and 
will not be, registered under the United States Securities Act of 1933 as amended from time to time (the 
“U.S. Securities Act”) or securities law of any state or other jurisdiction of the United States. The Offer 
Shares may not be offered, sold, pledged or otherwise transferred within the United States, except pursuant 
to an exemption from the registration requirements of the U.S. Securities Act and U.S. Investment Company 
Act of 1940, as amended (“U.S. Investment Company Act”), and in compliance with any applicable state 
securities laws. There will be no public offer of the Offer Shares in the United States. 

<<<PAGE 27>>>
25 
 
The Offer Shares are being offered and sold outside the United States to investors that are not U.S. persons 
nor persons acquiring for the account or benefit of U.S. persons in reliance on Regulation S under the U.S. 
Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. This announcement is not a prospectus. Potential investors should 
read the Prospectus dated June 17, 2026 issued by SG Micro Corp for detailed information about the Global 
Offering described below before deciding whether or not to invest in the H Shares thereby being offered. 
*Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators 
(for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence 
of any of the events set out in the section headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Hong Kong Underwriting Agreement – Grounds for Termination” 
in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently 
expected to be on June 26, 2026). 
 
 

<<<PAGE 28>>>
26 
 
PUBLIC FLOAT AND FREE FLOAT 
Immediately following the completion of the Global Offering (before any exercise of the Over-allotment 
Option), the total market value of the H Shares to be held by the public is above HK$4,601 million, calculated 
on the Offer Price of HK$85.20 per H Share, representing approximately 8% of the total issued share capital 
of the Company, which is higher than the prescribed expected market value of H Shares required to be held 
in public hands of not less than HK$3,000,000,000 under Rule 19A.13A(2)(b) of the Listing Rules, thereby 
satisfying Rule 19A.13A(2) of the Listing Rules at the time of the Listing. 
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the Listing Date. As 
such, H Shares held by the Cornerstone Investors upon the Listing shall not be counted towards the free float 
of the H Shares of the Company at the time of Listing. Based on the final Offer Price of HK$85.20 per H 
Share, the Company confirms it meets the free float requirement under Rule 19A.13C(2)(b) of the Listing 
Rules. 
The Directors confirm that, immediately following completion of the Global Offering (before any exercise of 
the Over-allotment Option): (i) no placee will, individually, be placed more than 10% of the enlarged issued 
share capital of the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder under the Listing Rules immediately after the Global Offering; (iii) the three largest public 
shareholders of the Company do not hold more than 50% of the H shares in public hands at the time of the 
Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 
holders of H Shares at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.  
COMMENCEMENT OF DEALINGS 
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, June 26, 2026 
(Hong Kong time), provided that the Global Offering has become unconditional and the right of 
termination described in the section headed “Underwriting – Underwriting Arrangements and Expenses 
– Hong Kong Public Offering – Grounds for Termination” in the Prospectus has not been exercised. 
Investors who trade the H Shares on the basis of publicly available allocation details prior to the receipt 
of H Share certificates or prior to the H Share certificates becoming valid evidence of title do so entirely 
at their own risk. 
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Friday, June 
26, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange will 
commence at 9:00 a.m. on Friday, June 26, 2026 (Hong Kong time). The H Shares will be traded in 
board lots of 100 H Shares each, and the stock code of the H Shares will be 3661. 
By order of the Board  
SG Micro Corp 
Zhang Shilong 
Chairman of the Board, Executive Director and General 
Manager 
Beijing, the PRC, June 25, 2026  
As at the date of this announcement, the Board comprises: (i) Dr. Zhang Shilong and Ms. Zhang Qin as 
executive Directors; (ii) Mr. Lin Lin and Ms. Liu Ming as non-executive Directors; and (iii) Dr. Du Meijie, 
Ms. Tang Chunlin and Mr. Chan Yik Pun as independent non-executive Directors. 
