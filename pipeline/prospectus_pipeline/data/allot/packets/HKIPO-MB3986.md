# 配发结果公告抽取任务：3986.HK GigaDevice Semiconductor Inc. - H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**12/01/2026 22:30**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0112/2026011201539.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3986.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
1
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) 
and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for the Offer 
Shares in the United States or in any other jurisdictions. The Offer Shares have not been, and will not be, registered 
under the United States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or securities 
law of any state or other jurisdiction of the United States. The Offer Shares may not be offered, sold, pledged or 
otherwise transferred within the United States, except pursuant to an exemption from the registration requirements 
of the U.S. Securities Act, and in compliance with any applicable state securities laws. The Offer Shares are being 
offered and sold outside the United States to investors that are not U.S. persons nor persons acquiring for the account 
or benefit of U.S. persons in reliance on Regulation S under the U.S. Securities Act. There will be no public offer of 
the Offer Shares in the United States.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
December 31, 2025 (the “Prospectus”) issued by GigaDevice Semiconductor Inc. (兆易創新科技集團股份有限公
司) (the “Company”) for detailed information about the Global Offering described below before deciding whether or 
not to invest in the H Shares thereby being offered. Any investment decision in relation to the Offer Shares should be 
taken solely in reliance on the information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
In connection with the Global Offering, Huatai Financial Holdings (Hong Kong) Limited, as stabilizing manager 
(the “Stabilizing Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, the extent 
permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect 
transactions with a view to stabilizing or supporting the market price of the H Shares at such price, in such amounts 
and in such manners as the Stabilizing Manager, its affiliates or any person acting for it may determine and at a 
level higher than that which might otherwise prevail for a limited period after the Listing Date. However, there is 
no obligation on the Stabilizing Manager (or its affiliates or any person acting for it) to conduct any such stabilizing 
action. Such stabilizing action, if taken, (a) will be conducted at the absolute discretion of the Stabilization Manager 
(or its affiliates or any person acting for it) and in what the Stabilizing Manager reasonably regards as the best interest 
of our Company, (b) may be discontinued at any time and (c) is required to be brought to an end within 30 days of 
the last day for lodging applications under the Hong Kong Public Offering (which is Saturday, February 7, 2026). 
Such stabilizing action, if taken, may be effected in all jurisdictions where it is permissible to do so, in each case in 
compliance with all applicable laws, rules and regulatory requirements, including the Securities and Futures (Price 
Stabilizing) Rules (Chapter 571 W of the Laws of Hong Kong), as amended, made under the Securities and Futures 
Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Saturday, February 7, 2026). 
After this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of 
the H Shares, could fall.
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on behalf of 
the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
Tuesday, January 13, 2026).

<<<PAGE 2>>>
2
GigaDevice Semiconductor Inc.
兆易創新科技集團股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the 
Global Offering
:
28,915,800 H Shares (subject to the 
 Over-allotment Option)
Number of Hong Kong Offer Shares
:
2,891,600 H Shares
Number of International Offer Shares
:
26,024,200 H Shares (subject to 
 the Over-allotment Option)
Final Offer Price
:
HK$162.00 per H Share plus brokerage 
 of 1.0%, SFC transaction levy of 
 0.0027%, Stock Exchange trading fee of 
 0.00565% and AFRC transaction levy of 
 0.00015% (payable in full on application 
 in Hong Kong dollars and 
 subject to refund)
Nominal value :
RMB1.00 per H Share 
Stock Code
:
3986
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
1
 
GIGADEVICE SEMICONDUCTOR INC. 
兆易創新科技集團股份有限公司 
ANNOUNCEMENT OF FINAL OFFER PRICE AND  
ALLOTMENT RESULTS 
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same meanings as 
those defined in the prospectus dated December 31, 2025 (the “Prospectus”) issued by GigaDevice 
Semiconductor Inc. (the “Company”). 
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could move 
substantially even with a small number of H Shares traded and should exercise extreme caution when 
dealing in the H Shares. 
SUMMARY 
Company Information 
Stock Code 
3986
Stock short name 
GIGADEVICE
Dealings commencement date 
January 13, 2026
*see note at the end of the announcement 
Price Information 
Final Offer Price 
HK$162.00
Offer Shares and Share Capital 
Number of Offer Shares 
28,915,800
Number of Offer Shares in Hong Kong Public Offering 
2,891,600
Number of Offer Shares in International Offering 
26,024,200
Number of issued Shares upon Listing (before exercise of the 
Over-allotment Option) 
696,765,151 
Number of issued Shares upon Listing include 603,020 A Shares held by the Company as treasury shares. 
 
Offer Size Adjustment Option (Upsize option)
Number of additional shares issued under the option 
0
- Public Offer 
- 
- International Offer 
-
Note: The Offer Size Adjustment Option has not been exercised. 
Over-allocation
No. of Offer Shares over-allocated 
4,337,300
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases in 
the secondary market at prices that do not exceed the Offer Price or through deferred delivery or a 
combination of these means. In the event the Over-allotment Option is exercised, an announcement will be 
made on the Stock Exchange’s website.
 

<<<PAGE 4>>>
2
 
Proceeds
Gross proceeds (Note) 
HK$4,684.4 million
Less: Estimated listing expenses payable based on Final 
Offer Price 
HK$73.5 million 
Net proceeds 
HK$4,610.9 million
 
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. 
The Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis. 
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING 
No. of valid applications 
148,419
No. of successful applications 
25,871
Subscription level  
542.22 times 
Claw-back triggered 
N/A
No. of Offer Shares initially available under the Hong Kong Public 
Offering 
2,891,600 
Final no. of Offer Shares under the Hong Kong Public Offering 
2,891,600 
% of Offer Shares under the Hong Kong Public Offering to the Global 
Offering 
10% 
% of final no. of Offer Shares under the Hong Kong Public Offering to 
the Global Offering (after overallocation) 
8.70% 
 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
https://www.hkeipo.hk/iporesult to perform a search by name or identification document number or 
https://www.hkeipo.hk/iporesult for the full list of allottees. 
INTERNATIONAL OFFERING 
No. of placees 
177
Subscription Level  
18.52 times 
No. of Offer Shares initially available under the International Offering
26,024,200 
Final no. of Offer Shares under the International Offering  
26,024,200 
% of Offer Shares under the International Offering to the Global 
Offering  
90% 
% of final no. of Offer Shares under the International Offering to the 
Global Offering (after over-allocation) 
91.30% 

<<<PAGE 5>>>
3
 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a waiver from 
strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) of Appendix F1 to 
the Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange to permit the Company to allocate 
certain Offer Shares in the International Offering to certain Existing Minority Shareholders and/or their close 
associates; and (b) a consent under Chapter 4.15 of the Guide for New Listing Applicants to permit the Company 
to, among other things, allocate further H Shares in the International Offering to the Cornerstone Investors, (i) 
none of the Offer Shares subscribed by the placees and the public have been financed directly or indirectly by 
the Company, any of the Directors, Supervisors, chief executive of the Company, substantial Shareholders, 
existing Shareholders of the Company or any of its subsidiaries or their respective close associates; and (ii) none 
of the placees and the public who have purchased the Offer Shares are accustomed to taking instructions from 
the Company, any of the Directors, Supervisors, chief executive of the Company, substantial Shareholders, 
existing Shareholders of the Company or any of its subsidiaries or their respective close associates in relation to 
the acquisition, disposal, voting or other disposition of H Shares registered in his/her/its name or otherwise held 
by him/her/it. 
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
% of total issued share 
capital in the Company 
after the Global Offering 
(assuming the Over-
allotment Option is not 
exercised and no 
additional Shares are 
issued pursuant to the 
Share Incentive Plans) 
Existing 
shareholders or 
their close 
associates 
Beijing Yuanfeng Asset 
Management L.L.P. (北
京源峰私募基金管理
合夥企業(有限合夥)) 
(“Yuanfeng Asset 
Management”) and 
Huatai Capital 
Investment Limited 
(“HTCI”) (in 
connection with the 
Yuanfeng Asset 
Management OTC 
Swaps) (as defined in 
the Prospectus)
           886,100 
3.06% 
0.13% 
No 
China Pinnacle Equity 
Management Limited 
(“CPE”)
        1,035,000 
3.58% 
0.15% 
No 
Shanghai Greenwoods 
Asset Management Co., 
Ltd. (上海景林資產管
理有限公司) 
(“Shanghai 
Greenwoods”) and 
        1,426,500 
4.93% 
0.20% 
No 

<<<PAGE 6>>>
4
 
Huatai Capital 
Investment Limited 
(“HTCI”) (in 
connection with the 
Greenwoods OTC 
Swaps) (as defined in 
the Prospectus)
New Alternative 
Limited 
        1,200,700 
4.15% 
0.17% 
No 
New Golden Future 
Limited
        1,200,700 
4.15% 
0.17% 
No 
Dymon Asia Multi-
Strategy Investment 
Master Fund 
(“DAMSIMF”)
        1,200,700 
4.15% 
0.17% 
Yes 
CloudAlpha Capital 
Management Limited 
(“CloudAlpha 
Capital”)
           960,600 
3.32% 
0.14% 
No 
3W Fund Management 
Limited (“3W Fund”)
           480,300 
1.66% 
0.07% 
No 
HUAQIN TELECOM 
HONG KONG 
LIMITED (華勤通訊香
港有限公司) 
        1,440,900 
4.98% 
0.21% 
No 
Metazone Link (HK) 
Limited (“Metazone”)
           960,600 
3.32% 
0.14% 
No 
Sky Royal Trading 
Limited
           480,300 
1.66% 
0.07% 
No 
Green Better Limited 
(“Green Better”)
           480,300 
1.66% 
0.07% 
No 
New China Asset 
Management (Hong 
Kong) Limited (“New 
China Asset 
Management”)
           480,300 
1.66% 
0.07% 
No 
Taikang Life Insurance 
Co., Ltd (“Taikang 
Life”)
           480,300 
1.66% 
0.07% 
Yes 
Summit Ridge Capital 
SP (“Summit Ridge”)
           480,300 
1.66% 
0.07% 
No 
ICBC Wealth 
Management Co., Ltd. 
(“ICBC Wealth”)
           480,300 
1.66% 
0.07% 
No 
Greater Bay Area 
Development Fund 
Management Limited 
(大灣區發展基金管理
有限公司) (“GBAD 
Fund Management”)
           480,300 
1.66% 
0.07% 
No 

<<<PAGE 7>>>
5
 
Wind Sabre Fund SPC 
on behalf of Wind 
Sabre Opportunities 
Fund SP (“Wind 
Sabre”)
           240,100 
0.83% 
0.03% 
No 
Total 
      14,394,300 
49.78% 
2.07% 
 
Notes: 
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering (assuming the Over-allotment Option is not 
exercised).  
2. 
In addition to the Offer Shares subscribed for as Cornerstone Investors, DAMSIMF, Taikang Life, 
HTCI, CPE, New Alternative Limited, New Golden Future Limited, CloudAlpha Capital, 3W Fund, 
, Sky Royal Trading Limited, New China Asset Management, ICBC Wealth, GBAD Fund 
Management and Wind Sabre were allocated further Offer Shares as placees in the International 
Offering. Please refer to the section headed “Allotment Results Details – International Offering – 
Allotees with Waivers/Consents Obtained” in this announcement for details. Only the Offer Shares 
subscribed for as Cornerstone Investors are subject to lock-up as indicated below. For details, 
please refer to the section headed “Lock-up Undertakings – Cornerstone Investors” in this 
announcement. 
 
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
not exercised) Note 3 
% of total issued share 
capital in the Company
after the Global 
Offering (assuming the
Over-allotment Option 
is not exercised and no 
additional Shares are 
issued pursuant to the 
Share Incentive Plans) 
Note 4
Relationship 
Allotees with consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations 
of further H Shares to Cornerstone Investors Note 1  Note 5 
DAMSIMF 
240,000
0.83%
0.03%
DAMSIMF is a 
Cornerstone Investor
Taikang Life 
96,000
0.33%
0.01%
Taikang Life is a 
Cornerstone Investor
Yuanfeng Asset 
Management and 
HTCI (in connection 
with the Yuanfeng 
Asset Management 
OTC Swaps)
472,600
1.63%
0.07%
HTCI (in connection 
with the Yuanfeng 
Asset Management 
OTC Swaps) is a 
Cornerstone Investor

<<<PAGE 8>>>
6
 
CPE 
488,000
1.69%
0.07%
CPE is a Cornerstone 
Investor
Shanghai Greenwoods 
and HTCI (in 
connection with the 
Greenwoods OTC 
Swaps)
676,000
2.34%
0.10%
HTCI (in connection 
with the Greenwoods 
OTC Swaps) is a 
Cornerstone Investor
Greenwoods Asset 
Management Hong 
Kong Limited  
284,600
0.98%
0.04%
Greenwoods Asset 
Management Hong 
Kong Limited holding 
24.9% of the 
registered share 
capital of Shanghai 
Greenwoods, and is 
therefore a close 
associate of the 
Cornerstone Investor, 
Shanghai 
Greenwoods
New Alternative 
Limited 
220,000
0.76%
0.03%
New Alternative 
Limited is a 
Cornerstone Investor
New Golden Future 
Limited 
1,230,600
4.26%
0.18%
New Golden Future 
Limited is a 
Cornerstone Investor
STRONG MEDIA 
LIMITED 
950,900
3.29%
0.14%
Each of  New 
Alternative Limited 
and New Golden 
Future Limited is 
wholly-owned by 
Yunfeng Capital 
Limited, a wholly-
owned subsidiary of 
Yunfeng Investments 
Limited (“Yunfeng 
Capital”). Yunfeng 
Capital is majority-
owned and controlled 
by Mr. Yu Feng. 
STRONG MEDIA 
LIMITED is 
ultimately wholly 
owned by Mr. Yu 
Feng, and is therefore 
a close associate of 
the Cornerstone 
Investors, New 
Alternative Limited 
and New Golden 

<<<PAGE 9>>>
7
 
Future Limited. 
CloudAlpha Capital  
192,000
0.66%
0.03%
CloudAlpha Capital is 
a Cornerstone 
Investor
3W Fund  
96,000
0.33%
0.01%
3W Fund is a 
Cornerstone Investor
LI Dongsheng 
476,600
1.65%
0.07%
LI Dongsheng is a 
close associate of a 
Cornerstone Investor, 
Metazone. Metazone 
is a wholly owned 
subsidiary of TCL 
Industries Holdings 
Co., Ltd ("TCL"), 
and Mr. Li 
Dongsheng is the 
Chairman and the 
ultimate beneficial 
owner of TCL.
Sky Royal Trading 
Limited 
144,000
0.50%
0.02%
Sky Royal Trading 
Limited is a 
Cornerstone Investor
New China Asset 
Management 
96,000
0.33%
0.01%
New China Asset 
Management is a 
Cornerstone Investor
Summit Nova Capital 
SP 
192,000
0.66%
0.03%
Summit Nova Capital 
SP is a close associate 
of a Cornerstone 
Investor, Summit 
Ridge. Both of 
Summit Nova Capital 
SP and Summit Ridge 
are segregated 
portfolios managed 
by the same 
investment manager, 
S Harmony Asset 
Management Limited.
ICBC Wealth  
96,000
0.33%
0.01%
ICBC Wealth is a 
Cornerstone Investor
GBAD Fund 
Management 
96,000
0.33%
0.01%
GBAD Fund 
Management is a 
Cornerstone Investor

<<<PAGE 10>>>
8
 
Wind Sabre  
48,000
0.17%
0.01%
Wind Sabre is a 
Cornerstone Investor
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for 
New Listing Applicants in relation to allocations to connected clients Note 2 
CICC Financial 
Trading Limited 
("CICC FT") 
242,800
0.84%
0.04%
Connected client 
HTCI (in connection 
with the Yuanfeng 
Asset Management 
OTC Swaps)
886,100
3.06%
0.13%
Connected client as a 
Cornerstone Investor 
HTCI (in connection 
with the Greenwoods 
OTC Swaps) 
1,426,500
4.93%
0.20%
Connected client as a 
Cornerstone Investor 
HTCI 
1,187,600
4.11%
0.17%
Connected client as a 
placee 
CITIC Securities 
International Capital 
Management Limited 
(CSICM)
28,800
0.10%
0.00%
Connected client 
China Asset 
Management Co. Ltd. 
(China AMC)  
13,000
0.04%
0.00%
Connected client 
China Asset 
Management (Hong 
Kong) Limited 
(China AMC HK)
8,000
0.03%
0.00%
Connected client 
Bosera Asset 
Management 
(International) Co., 
Ltd (Bosera AM) 
2,000
0.01%
0.00%
Connected client 
ICBC UBS Asset 
Management 
(International) 
Company Limited 
(ICBC UBS 
International) 
1,500
0.01%
0.00%
Connected client 
ICBC UBS Asset 
Management Co., Ltd. 
(ICBC UBS)  
6,500
0.02%
0.00%
Connected client 

<<<PAGE 11>>>
9
 
Notes: 
1. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents 
the number of Offer Shares allocated to the investors as placees in the International Offering. For 
allocations of Offer Shares to the relevant investors as Cornerstone Investors, please refer to the 
section headed “Allotment Results Details – International Offering – Cornerstone Investors” in this 
announcement. For details of the consent under Chapter 4.15 of the Guide for New Listing Applicants 
in relation to allocations of further H Shares to the existing Shareholders and/or their close associates 
and Cornerstone Investors, please refer to the section headed “Others/Additional Information – 
Allotees with consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocations of further H Shares to Cornerstone Investors” in this announcement. 
2. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations to connected clients, please refer to the 
section headed “Others / Additional Information – Placing to connected clients with a prior consent 
under paragraph 1C(1) of the Placing Guidelines” in this announcement. 
3. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering (assuming the Over-allotment Option is not exercised). 
4. 
Not taking into account any A Shares held by the relevant investors. 
5. 
Except for DAMSIMF and Taikang Life, none of the allotees with consent under Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations of further H Shares to Cornerstone 
Investors is an existing Shareholder of the Company. 
 
 
 

<<<PAGE 12>>>
10
 
LOCK-UP UNDERTAKINGS 
Cornerstone Investors  
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
exercised and no 
additional Shares are 
issued pursuant to the 
Share Incentive 
Plans) 
Last day subject to 
the lock-up 
undertakingsNote 2 
Yuanfeng Asset 
Management and 
HTCI (in connection 
with the Yuanfeng 
Asset Management 
OTC Swaps)
           886,100 
3.06% 
0.13% 
July 12, 2026 
CPE 
        1,035,000 
3.58% 
0.15% 
July 12, 2026 
Shanghai 
Greenwoods and 
HTCI (in connection 
with the Greenwoods 
OTC Swaps) 
        1,426,500 
4.93% 
0.20% 
July 12, 2026 
New Alternative 
Limited 
        1,200,700 
4.15% 
0.17% 
July 12, 2026 
New Golden Future 
Limited 
        1,200,700 
4.15% 
0.17% 
July 12, 2026 
DAMSIMF 
        1,200,700 
4.15% 
0.17% 
July 12, 2026 
CloudAlpha Capital 
           960,600 
3.32% 
0.14% 
July 12, 2026 
3W Fund  
           480,300 
1.66% 
0.07% 
July 12, 2026 
HUAQIN 
TELECOM HONG 
KONG LIMITED 
(華勤通訊香港有限
公司) 
        1,440,900 
4.98% 
0.21% 
July 12, 2026 

<<<PAGE 13>>>
11
 
Metazone  
           960,600 
3.32% 
0.14% 
July 12, 2026 
Sky Royal Trading 
Limited 
           480,300 
1.66% 
0.07% 
July 12, 2026 
Green Better  
           480,300 
1.66% 
0.07% 
July 12, 2026 
New China Asset 
Management 
           480,300 
1.66% 
0.07% 
July 12, 2026 
Taikang Life  
           480,300 
1.66% 
0.07% 
July 12, 2026 
Summit Ridge  
           480,300 
1.66% 
0.07% 
July 12, 2026 
ICBC Wealth 
           480,300 
1.66% 
0.07% 
July 12, 2026 
GBAD Fund 
Management 
           480,300 
1.66% 
0.07% 
July 12, 2026 
Wind Sabre  
           240,100 
0.83% 
0.03% 
July 12, 2026 
Total 
      14,394,300 
49.78% 
2.07% 
 
Notes: 
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering. 
2. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on 
July 12, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or transferring 
H Shares subscribed pursuant to the relevant cornerstone investment agreements after the indicated 
date. 
 
 

<<<PAGE 14>>>
12
 
PLACEE CONCENTRATION ANALYSIS 
Placees* 
Number of H 
Shares allotted
Allotment as 
% of 
International 
Offering 
(assuming no 
exercise of the 
Over-
allotment 
Option) 
Allotment as 
% of 
International 
Offering 
(assuming the 
Over- 
allotment 
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
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over- 
allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
Number of H 
Shares held 
upon Listing 
% of total 
issued H share 
capital upon 
Listing 
(assuming no 
exercise of the 
Over-
allotment 
Option) 
% of total 
issued H share 
capital upon 
Listing 
(assuming the 
Over-
allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
% of total 
issued share 
capital upon 
Listing 
(assuming no 
exercise of the 
Over-
allotment 
Option and no 
additional 
Shares are 
issued 
pursuant to 
the Share 
Incentive 
Plans) 
% of total 
issued share 
capital upon 
Listing 
(assuming the 
Over-
allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
Top 1 
4,802,900 
18.46% 
15.82% 
16.61% 
14.44% 
4,802,900 
16.61% 
14.44% 
0.69% 
0.69% 
Top 5 
11,594,600 
44.55% 
38.19% 
40.10% 
34.87% 
11,594,600 
40.10% 
34.87% 
1.66% 
1.65% 
Top 10 
17,467,900 
67.12% 
57.53% 
60.41% 
52.53% 
17,467,900 
60.41% 
52.53% 
2.51% 
2.49% 
Top 25 
25,716,500 
98.82% 
84.70% 
88.94% 
77.34% 
25,716,500 
88.94% 
77.34% 
3.69% 
3.67% 
 
Note: 
* 
Ranking of placees is based on the number of H Shares allotted to the placees. 
 
 

<<<PAGE 15>>>
13
 
H SHAREHOLDER CONCENTRATION ANALYSIS 
H 
Sharehol
ders 
* 
Number of H 
Shares allotted
Allotment as 
% of 
International 
Offering 
(assuming no 
exercise of the 
Over-
allotment 
Option) 
Allotment as 
% of 
International 
Offering 
(assuming the 
Over- 
allotment 
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
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over- 
allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
Number of H 
Shares held 
upon Listing
% of total 
issued H share 
capital upon 
Listing 
(assuming no 
exercise of the 
Over-
allotment 
Option) 
% of total 
issued H share 
capital upon 
Listing 
(assuming the 
Over-
allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
% of total 
issued share 
capital upon 
Listing 
(assuming no 
exercise of the 
Over-
allotment 
Option and no 
additional 
Shares are 
issued 
pursuant to 
the Share 
Incentive 
Plans) 
% of total 
issued share 
capital upon 
Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
no additional 
Shares are 
issued pursuant 
to the Share 
Incentive 
Plans) 
Top 1 
4,802,900 
18.46% 
15.82% 
16.61% 
14.44% 
4,802,900 
16.61% 
14.44% 
0.69% 
0.69% 
Top 5 
11,594,600 
44.55% 
38.19% 
40.10% 
34.87% 
11,594,600 
40.10% 
34.87% 
1.66% 
1.65% 
Top 10 
17,467,900 
67.12% 
57.53% 
60.41% 
52.53% 
17,467,900 
60.41% 
52.53% 
2.51% 
2.49% 
Top 25 
25,716,500 
98.82% 
84.70% 
88.94% 
77.34% 
25,716,500 
88.94% 
77.34% 
3.69% 
3.67% 
 
Note: 
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing. 
 
 

<<<PAGE 16>>>
14
 
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
Option and no 
additional Shares 
are issued pursuant 
to the Share 
Incentive Plans) 
% of total issued 
share capital upon 
Listing (assuming 
the Over-allotment 
Option is fully 
exercised and no 
additional Shares 
are issued pursuant 
to the Share 
Incentive Plans) 
Top 1 
0 
0.00% 
0.00% 
0.00% 
0.00% 
0 
58,811,513 
8.44% 
8.39% 
Top 5 
0 
0.00% 
0.00% 
0.00% 
0.00% 
0 
136,149,214 
19.54% 
19.42% 
Top 10 
0 
0.00% 
0.00% 
0.00% 
0.00% 
0 
169,209,743 
24.29% 
24.13% 
Top 25 
7,190,000 
27.63% 
23.68% 
24.87% 
21.62% 
7,190,000 
216,762,305 
31.11% 
30.92% 
 
Note: 
* 
Ranking of Shareholders is based on the aggregate of, where applicable, the number of H Shares held by the Shareholders upon Listing and the A Shares held by the Shareholders as 
of December 31, 2025, which is the latest shareholding of A Shares available to the Company. 
# 
Among the top 25 placees, certain placees are also existing Shareholders. To the best knowledge, information and belief of the Company after due enquiry, no allocation has been 
made to the Existing Minority Shareholders holding more than 1% of the issued share capital of the Company immediately prior to the completion of the Global Offering. As the top 
25 placees who are also existing shareholders held less than 1% of the issued share capital of the Company immediately prior to the completion of the Global Offering, the number 
of A Shares held by them are not counted into the number of Shares held upon Listing. 
 

<<<PAGE 17>>>
15
 
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
applications
Basis of allocation/ballot
for
100
48,658
974 out of 48,658 applicants to receive 100 H Shares
2.00%
200
8,274
249 out of 8,274 applicants to receive 100 H Shares
1.50%
300
15,497
596 out of 15,497 applicants to receive 100 H Shares
1.28%
400
2,758
127 out of 2,758 applicants to receive 100 H Shares
1.15%
500
3,235
171 out of 3,235 applicants to receive 100 H Shares
1.06%
600
3,654
216 out of 3,654 applicants to receive 100 H Shares
0.99%
700
1,898
123 out of 1,898 applicants to receive 100 H Shares
0.93%
800
1,546
109 out of 1,546 applicants to receive 100 H Shares
0.88%
900
1,312
99 out of 1,312 applicants to receive 100 H Shares
0.84%
1,000
8,663
694 out of 8,663 applicants to receive 100 H Shares
0.80%
1,500
4,161
425 out of 4,161 applicants to receive 100 H Shares
0.68%
2,000
3,487
419 out of 3,487 applicants to receive 100 H Shares
0.60%
2,500
2,206
304 out of 2,206 applicants to receive 100 H Shares
0.55%
3,000
2,520
386 out of 2,520 applicants to receive 100 H Shares
0.51%
3,500
1,814
305 out of 1,814 applicants to receive 100 H Shares
0.48%
4,000
1,648
297 out of 1,648 applicants to receive 100 H Shares
0.45%
4,500
1,275
253 out of 1,275 applicants to receive 100 H Shares
0.44%
5,000
2,667
561 out of 2,667 applicants to receive 100 H Shares
0.42%
6,000
2,112
482 out of 2,112 applicants to receive 100 H Shares
0.38%
7,000
1,643
415 out of 1,643 applicants to receive 100 H Shares
0.36%
8,000
1,260
353 out of 1,260 applicants to receive 100 H Shares
0.35%
9,000
1,116
342 out of 1,116 applicants to receive 100 H Shares
0.34%
10,000
6,372
2,040 out of 6,372 applicants to receive 100 H Shares
0.32%
20,000
4,056
1,947 out of 4,056 applicants to receive 100 H Shares
0.24%
30,000
3,895
2,571 out of 3,895 applicants to receive 100 H Shares
0.22%
Total
135,727
Total number of Pool A successful applicants: 14,458
 
 

<<<PAGE 18>>>
16
 
 
 
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
40,000
5,709 4,568 out of 5,709 applicants to receive 100 H Shares
0.20%
50,000
1,573
1,435 out of 1,573 applicants to receive 100 H Shares
0.18%
60,000
1,013
100 H Shares
0.17%
70,000
760
100 H Shares plus 74 out of 760 applicants to receive an additional 100 H Shares
0.16%
80,000
504
100 H Shares plus 101 out of 504 applicants to receive an additional 100 H Shares
0.15%
90,000
356
100 H Shares plus 100 out of 356 applicants to receive an additional 100 H Shares
0.14%
100,000
1,574
100 H Shares plus 536 out of 1,574 applicants to receive an additional 100 H Shares
0.13%
200,000
538
200 H Shares
0.10%
300,000
236
200 H Shares plus 130 out of 236 applicants to receive an additional 100 H Shares
0.09%
400,000
93
200 H Shares plus 86 out of 93 applicants to receive an additional 100 H Shares
0.07%
500,000
69
300 H Shares
0.06%
600,000
50
300 H Shares plus 34 out of 50 applicants to receive an additional 100 H Shares
0.06%
700,000
26
400 H Shares
0.06%
800,000
34
400 H Shares plus 11 out of 34 applicants to receive an additional 100 H Shares
0.05%
900,000
15
400 H Shares plus 6 out of 15 applicants to receive an additional 100 H Shares
0.05%
1,000,000
26
400 H Shares plus 13 out of 26 applicants to receive an additional 100 H Shares
0.05%
1,200,000
34
500 H Shares
0.04%
1,445,800
82 600 H Shares
0.04%
Total
12,692
Total number of Pool B successful applicants: 11,413 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries. 
 

<<<PAGE 19>>>
17
 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of which 
consent has been obtained, the Company has complied with the Listing Rules and guidance materials in 
relation to the placing, allotment and listing of the Company’s H Shares. 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the 
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by 
them was the same as the final Offer Price in addition to any brokerage, AFRC transaction levy, SFC 
transaction levy and trading fee payable. 
OTHERS / ADDITIONAL INFORMATION 
Offer Size Adjustment Option  
The Offer Size Adjustment Option has not been exercised. As a result, the final number of Offer Shares 
under the International Offering has not been adjusted. 
Allocations of Offer Shares to the existing Shareholders and/or their close associates and 
Cornerstone Investors with a consent under Chapter 4.15 of the Guide for New Listing Applicants 
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 of the 
Guide for New Listing Applicants to permit the Company to allocate further Offer Shares in the 
International Offering to certain Cornerstone Investors as placees, subject to the following conditions 
(“Allocation to Size-based Exemption Participants”): 
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
each Director, chief executive and Supervisor of the Company confirms that no securities have 
been allocated to them or their respective close associates under the Size-based Exemption; and 
(e) 
details of the allocation to existing Shareholders and/or their close associates and Cornerstone 
Investors under the Size-based Exemption will be disclosed in this announcement. 
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted by 
the Stock Exchange. 
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates and 
Cornerstone Investors, please refer to the section headed “Allotment Results Details – International 
Offering – Allotees with Waivers/Consents Obtained” in this announcement. 
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines 

<<<PAGE 20>>>
18
 
Under the International Offering, certain Offer Shares were placed to connected clients of their connected 
distributors pursuant to the Placing Guidelines. Details of the placement to connected clients are set out 
below. The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, 
consents under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such Offer 
Shares in the International Offering to the connected clients. The allocation of Offer Shares to such 
connected clients is in compliance with all the conditions under the consent granted by the Stock 
Exchange. 
 

<<<PAGE 21>>>
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
ultimate 
beneficial 
owners of the 
Offer Shares or, 
where 
applicable, 
details of the 
structured 
products under 
which the 
subscription by 
the Connected 
Client was made 
(e.g. OTC total 
return swaps)  
 
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which is 
not authorised 
by the SFC or is 
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
Percentage of 
total number of 
Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised and 
no additional 
Shares are 
issued pursuant 
to the Share 
Incentive Plans)
Approximate 
percentage of total 
Shares in issue 
immediately 
following the 
completion of 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised and no 
additional Shares 
are issued 
pursuant to the 
Share Incentive 
Plans) 
1. 
China 
International 
Capital 
Corporation 
Hong Kong 
Securities 
Limited 
(CICCHKS)  
CICC 
Financial 
Trading 
Limited 
(CICC FT) 
(Note 1) 
 
CICC FT is a 
member of the 
same group of 
CICCHKS.  
 
Please refer to 
Note (1).  
 
N  
Pinpoint: 
1,800 
0.01% 
0.00% 
Hengde 
Funds: 49,000 
0.17% 
0.01% 
Jindan No.6: 
192,000 
0.66% 
0.03% 
2.  
Huatai 
Financial 
Holdings 
(Hong Kong) 
Huatai 
Capital 
Investment 
HTCI is a 
member of the 
same group of 
HTFH. 
Please refer to 
Note (3).  
N 
Greenwoods 
Funds: 
676,000 
2.34% 
0.10% 

<<<PAGE 22>>>
20
 
Limited 
(HTFH) 
Limited 
(HTCI) 
(Note 2) 
Yuanfeng 
Funds: 
472,600 
1.63% 
0.07% 
Gaoyi Funds: 
39,000 
0.13% 
0.01% 
3. 
CITIC 
Securities 
Brokerage 
(HK) Limited 
(CSB) 
CITIC 
Securities 
International 
Capital 
Management 
Limited 
(CSICM)
CSICM is a 
member of the 
same group of 
CSB. 
Please refer to 
Note (4).  
N 
Beevest: 
24,000 
0.08% 
0.00% 
HY Capital: 
4,800 
0.02% 
0.00% 
 
 
 

<<<PAGE 23>>>
21
 
Part B - Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties 
 
No. 
Connected 
Distributor 
Connected Client 
Relationship 
with the 
Connected 
Distributor 
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
Number of 
Offer Shares 
allocated to the 
connected 
client 
Approximate 
Percentage of total 
number of Offer 
Shares (assuming 
the Over-allotment 
Option is not 
exercised and no 
additional Shares 
are issued pursuant 
to the Share 
Incentive Plans) 
Approximate 
percentage of total 
Shares in issue 
immediately following 
the completion of 
Global Offering 
(assuming the Over-
allotment Option is not 
exercised and no 
additional Shares are 
issued pursuant to the 
Share Incentive Plans) 
1.  
CSB 
China Asset 
Management Co. Ltd. 
(China AMC) (Note 5)
CSB is a wholly 
owned 
subsidiary of 
CITIC Securities 
Company 
Limited (a 
company listed 
on the Stock 
Exchange, stock 
code: 6030.HK, 
the "CITIC 
Securities"), 
China AMC is 
controlled as to 
62.2% by 
CITICS 
Securities, and 
China AMC HK 
is a wholly 
N 
13,000 
0.04% 
0.00% 
2.  
China Asset 
Management (Hong 
Kong) Limited (China 
AMC HK) (Note 6) 
N 
8,000 
0.03% 
0.00% 

<<<PAGE 24>>>
22
 
owned 
subsidiary of 
China AMC. 
Therefore, CSB, 
China AMC HK 
and China AMC 
are members of 
the same group. 
3.  
CMB 
International 
Securities 
Limited 
(CMBI) and 
CMB 
International 
Global Markets 
Limited (CMBI 
GM) 
Bosera Asset 
Management 
(International) Co., 
Ltd  
(Bosera AM) (Note 7) 
Bosera AM is 
controlled as to 
45% by China 
Merchants Fund 
(招商基金) and 
55% by Bosera 
Asset 
Management, 
which is held as 
to 49% by China 
Merchants 
Securities. Each 
of CMBI and 
CMBI GM is a 
subsidiary of 
China Merchants 
Securities. 
Bosera AM is 
therefore a 
member of the 
same group of 
CMBI and 
CMBI GM
N 
2,000 
0.01% 
0.00% 
4.  
UBS AG 
Singapore 
ICBC UBS Asset 
Management 
UBS AG and 
UBS HK are 
N 
1,500 
0.01% 
0.00% 

<<<PAGE 25>>>
23
 
Branch Wealth 
Management 
(UBS AG) and 
UBS AG Hong 
Kong Branch 
Wealth 
Management 
(UBS HK) 
(International) 
Company Limited 
(ICBC UBS 
International) (Note 
8)
wholly owned 
subsidiaries of 
UBS Group AG,  
ICBC UBS is 
owned as to 20% 
by UBS Group 
AG, and ICBC 
UBS 
(International) is 
the wholly 
owned 
subsidiary of 
ICBC UBS. 
Therefore, UBS 
AG, UBS HK, 
ICBC UBS and 
ICBC UBS 
(International) 
are members of 
the same group.
5.  
ICBC UBS Asset 
Management Co., Ltd. 
(ICBC UBS) (Note 9) 
N 
6,500 
0.02% 
0.00% 
 
 
Notes: 
 
(1) CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one OTC swap transactions (the “OTC Swaps”) with each 
other and the ultimate clients (the “CICC FT Ultimate Clients”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the OTC 
Swaps while the economic risks and returns of the underlying Offer Shares are passed to the CICC FT Ultimate Clients, subject to customary fees and commissions. The 
OTC Swaps will be fully funded by the CICC FT Ultimate Clients. During the terms of the OTC Swaps, all economic returns of the Offer Shares subscribed by CICC FT 
will be passed to the CICC FT Ultimate Clients and all economic loss shall be borne by the CICC FT Ultimate Clients through the OTC Swaps, and CICC FT will not 
take part in any economic return or bear any economic loss in relation to the Offer Shares. The OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate 
Clients may request CICC FT to redeem it at their own discretions, upon which CICC FT shall dispose of the Offer Shares and settle OTC Swaps in cash in accordance 
with the terms and conditions of the OTC Swap. Despite that CICC FT will hold the legal title of the Offer Shares by itself, it will not exercise the voting rights attaching 
to the relevant Offer Shares during the terms of the OTC Swaps according to its internal policy. The CICC FT Ultimate Clients for purpose of this placee subscription 
include (i) 保銀多空穩健1 號 ("Pinpoint No.1"), 保銀多空穩健2 號 ("Pinpoint No.2") and 保銀進取1 號私募證券投資基金 ("Pinpoint Aggressive", collectively, 
"Pinpoint"), which are managed by Shanghai Pinpoint Private Equity Fund Management Co., Ltd. (上海保銀私募基金管理有限公司) ("Shanghai Pinpoint"); (ii) 恒

<<<PAGE 26>>>
24
 
德遠征添利3 號私募證券投資基金 and 恒德遠征添利7 號私募證券投資基金 (collectively, "Hengde Funds")"), which are managed by Beijing Hengde Times 
Private Equity Fund Management Co., Ltd. (北京恒德時代私募基金管理有限公司) ("Beijing Hengde"); and (iii) 金澹遠洋6 號私募證券投資基金 ("Jindan No.6"), 
which are managed by Shanghai Jindan Asset Management Co., Ltd. (上海金澹資產管理有限公司) ("Shanghai Jindan"). None of the single shareholders hold 30% 
or more interest in Pinpoint Aggressive, Hengde Funds or Beijing Hengde. Mr. Wang Qiang (王強) is the only single ultimate beneficial owner holding 30% or more 
interest in both Pinpoint No. 1 and Pinpoint No. 2. The only ultimate beneficial owner holding 30% or more interest of Shanghai Pinpoint includes Li Mo (李墨). Zhang 
Yan (張焱) is the only single ultimate beneficial owner holding 30% or more interest in Shanghai Jindan, and Ding Hai (丁海) is the only single ultimate beneficial owner 
holding 30% or more interest in Jindan No.6. 
 
To the best of CICC FT’s knowledge having made all reasonable inquiries, each of the CICC FT Ultimate Clients is an independent third party of CICC FT, CICCHKS 
and the companies which are members of the same group of companies as each of the Underwriters. 
 
 
The Overall Coordinators confirm that the Offer Shares to be placed to CICC FT are to be held on behalf of independent third parties. 
 
 
(2) Huatai Securities Co., Ltd. ("Huatai Securities"), the shares of which are listed on both the Shanghai Stock Exchange (stock code: 601688) and the Stock Exchange 
(stock code: 6886), is one of the domestic securities firms licensed to undertake cross-border derivatives trading activities. Huatai Securities entered into an ISDA 
agreement (the "ISDA Agreement") with its indirectly wholly-owned subsidiary, HTCI, to set out the principal terms of any future total return swap between Huatai 
Securities and HTCI. 
 
HTFH is an Overall Coordinator in connection with the Global Offering. Pursuant to the ISDA Agreement, HTCI, which intends to participate in the Global Offering as 
a placee, will hold the beneficial interest of the Offer Shares on a non-discretionary basis as the single underlying holder under a back-to-back total return swap (the 
"Back-to-back TRS") to be entered by HTCI in connection with a Client TRS (as defined below) placed by and fully funded (i.e. with no financing provided by HTCI) 
by the Huatai Ultimate Clients (as defined below), by which, HTCI will, subject to customary fees and commissions, pass the full economic exposure of the Offer Shares 
to the Huatai Ultimate Clients (as defined below), which in effect, HTCI will hold the beneficial interest of the Offer Shares on behalf of the Huatai Ultimate Clients (as 
defined below). HTFH, the Overall Coordinator, and HTCI are indirectly wholly-owned subsidiaries of Huatai Securities. Accordingly, HTCI is considered as a "connected 
client" of HTFH pursuant to paragraph 1B(7) of the Placing Guidelines. 
 
(3) PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public offerings ("IPOs") in Hong Kong. However, PRC investors 
are permitted to invest in products issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. In connection with 
such products, the licensed domestic securities firms, through their Hong Kong affiliates, may participate in Hong Kong IPOs either as placees or cornerstone investors 
(the "Cross-border Derivatives Trading Regime").  
 
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the "Huatai Ultimate Clients") cannot directly subscribe for the Offer Shares but may 
invest in derivative products issued by domestic securities firms licenced to undertake cross-border derivatives trading activities, such as Huatai Securities, with the Offer 
Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, the Huatai Ultimate Clients , through their respective investment managers (as 
applicable), will place a total return swap order (the "Client TRS") with Huatai Securities in connection with the Company's IPO and Huatai Securities will place a Back-

<<<PAGE 27>>>
25
 
to-back TRS order to HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the Back-to-back TRS, HTCI participates in the Company’s IPO 
and subscribes the Offer Shares through placing order with HTFH during the International Offering. 
 
The Huatai Ultimate Clients  for purpose of this place subscription include (i) 景林景泰全球私募證券投資基金, 景林全球基金, 景林致遠私募基金, 景林景泰豐收
私募證券投資基金, 景林豐收3 號私募基金, 景林豐收2 號基金 and 景林豐收6 號私募證券投資基金 (collectively, the "Greenwoods Funds"), which are managed 
by Shanghai Greenwoods Asset Management Co., Ltd. (上海景林資產管理有限公司) (“Shanghai Greenwoods”); (ii) 源峰價值私募證券投資基金、源峰穩健私募
證券投資基金 (collectively, the "Yuanfeng Funds"), which are managed by Beijing Yuanfeng Asset Management L.L.P. (北京源峰私募基金管理合夥企業(有限合
夥)) (“Yuanfeng Asset Management”); (iii) 金太陽高毅國鷺1 號崇遠基金, 高毅國鷺信遠私募證券投資基金, 高毅任昊臻選春和私募證券投資基金, 高毅任昊
長期價值朗潤私募證券投資基金, 高毅任昊優選致福私募證券投資基金, 高毅慶瑞6 號瑞行基金, 高毅慶瑞臻選灃源私募證券投資基金 and 高毅利偉精選唯實
基金 (collectively, the "Gaoyi Funds"), which are managed by Perseverance Asset Management L.l.p. (上海高毅資產管理合夥企業(有限合夥)) (“Gaoyi Asset 
Management”). Mr. Jiang Jinzhi is the chairman and an ultimate beneficial owner of Shanghai Greenwoods. No other shareholder holds 30% or more 
interest in Shanghai Greenwoods. The only ultimate beneficial owner holding 30% or more interest of Gaoyi Asset Management is Zhang Haiyan (张海燕). None of 
the single shareholders hold 30% or more interest in Greenwoods Funds, Yuanfeng Funds, Yuanfeng Asset Management and Gaoyi Funds. 
 
To the best of knowledge of HTCI and after making all reasonable enquiries, each of the Huatai Ultimate Clients  is an independent third party of HTCI, HTFH and the 
companies which are members of the same group of companies as each of the Underwriters. 
 
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in connection with the Client TRS order placed by the Huatai Ultimate 
Clients . Pursuant to the terms of the contracts of the Back-to-back TRS and the Client TRS, during the tenor of the Back-to-back TRS and the Client TRS, subject to 
customary fees and commissions, all economic returns of the Offer Shares will be ultimately passed to the Huatai Ultimate Clients  through the Back-to-back TRS and 
the Client TRS and all economic loss shall be ultimately borne by the Huatai Ultimate Clients . HTCI will not take any economic return or bear any economic loss in 
relation to the Offer Shares. 
 
Investment in the Back-to-back TRS and the Client TRS is similar to the investment in a qualified domestic institutional investor fund ("QDII") in the way that the Huatai 
Ultimate Clients  would reap all the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through the exchange rate exposure on both 
the notional value of the investment and the profit and loss of the investment. In contrast, the profit and loss of the Back-to-back TRS and the Client TRS factor into 
account the fluctuation in RMB exchange rate upon termination of the Client TRS by converting the profit and loss using the current exchange rate at the time of 
termination. As such, the Huatai Ultimate Clients  would bear the exchange rate exposure of the profit and loss on settlement date. 
 
The Huatai Ultimate Clients  may exercise an early termination right to terminate the Client TRS at any time from the issue date of the Client TRS which should be on 
or after the date on which the Offer Shares are listed on the Stock Exchange at their own discretion. Upon the termination upon maturity or early termination of the Client 
TRS by the Huatai Ultimate Clients , HTCI will dispose the Offer Shares on the secondary market and the Huatai Ultimate Clients  will receive a final settlement amount 
in cash in accordance with the terms and conditions of the Back-to-back TRS and the Client TRS which should have taken into account all the economic returns or 
economic loss in relation to the Offer Shares. If upon the maturity of the Client TRS, the Huatai Ultimate Clients  intend to extend the investment period, subject to further 
agreement between Huatai Securities and the relevant Huatai Ultimate Clients , the term of the Client TRS could be extended by way of a new issuance or a tenor 
extension. Accordingly, Huatai Securities will extend the term of the Back-to-back TRS by way of a new issuance or a tenor extension. 

<<<PAGE 28>>>
26
 
 
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through the economic exposure to the Huatai Ultimate Clients , 
each being an onshore client who places a Client TRS order with Huatai Securities in connection with the IPO of the Company. HTCI will not exercise the voting right 
of the Offer Shares during the tenor of the Back-to-back TRS. 
 
During the life of the Client TRS and Back-to-back TRS, HTCI may continue to hold the Offer Shares in its custodian account, or to hold some or all of the Offer Shares 
in a prime brokerage account for stock borrowing purposes, where HTCI will lend out its holding of underlying Offer Shares in the form of stock borrowing loans 
consistent with market practice to lower its finance costs, provided that HTCI has the ability to call back the Offer Shares on loan at any time in order to satisfy its 
obligations under the Back-to-back TRS to ensure the economic interests are ultimately passed to the Huatai Ultimate Clients . 
 
(4) CSICM will hold the allocated Offer Shares for its end clients on a non-discretionary basis, and all the economic exposure will be passed to its end clients through OTC 
total return swaps (TRS). The end clients of CSICM ("CSICM Ultimate Clients") and their ultimate beneficial owners include: (i) Beevest Capital Management Limited 
("Beevest") and Zeng Shuzhen is the only ultimate beneficial owner who holds 30% or more interests in Beevest; and (ii) HY Capital Company Limited ("HY Capital"), 
and the ultimate beneficial owners holding 30% or more interest of HY Capital include Xia Hui and Lu Ang. 
 
To best of knowledge of CSICM and after making all reasonable enquiries, the CSICM Ultimate Clients are independent third parties of CSICM, CSB and the companies 
which are members of the same group of companies as each of the Underwriters. 
 
(5) CSB is a distributor of the Global Offering. China AMC will hold the Offer Shares in its capacity as the discretionary fund manager managing assets on behalf of its 
underlying client, which is an independent third party. There is no ultimate beneficial owner holding 30% interest or more in such underlying client. To the best knowledge 
of China AMC after due enquiry, the underlying client of China AMC is an independent third party of China AMC and CSB, and the companies which are members of 
the same group of companies as each of the Underwriters. 
 
(6) CSB is a distributor of the Global Offering. China AMC HK will hold the Offer Shares in its capacity as the discretionary fund manager managing assets on behalf of its 
underlying clients or mandates, which are independent third parties. To the best knowledge of China AMC HK after due enquiry, each of the underlying clients or 
mandates of China AMC HK and their respective ultimate beneficial owner holding 30% or more interest is an independent third party of China AMC HK and CSB, and 
the companies which are members of the same group of companies as each of the Underwriters. 
 
(7) Each of CMBI and CMBI GM is distributor of the Global Offering. Bosera AM intends to subscribe and hold the Offer Shares in its capacity as the discretionary fund 
manager on behalf of its sub-funds, Navigator Technology Limited IPO Mandate, Bosera Hong Kong Equity Plus Fund (SFC authorized fund, CE: BRK536), and Bosera 
Global Select Equity Fund SP (collectively, the "Bosera Funds"). To the best knowledge of Bosera AM after due enquiry, each of the Bosera Funds and their respective 
ultimate beneficial owner holding 30% or more interest is an independent third party of Bosera AM and each of CMBI and CMBI GM, and the companies which are 
members of the same group of companies as each of the Underwriters. 
 
(8) Each of UBS AG and UBS HK is a distributor of the Global Offering. ICBC UBS (International) will hold the Offer Shares in its capacity as the discretionary fund 
manager on behalf of its underlying client, who, and its ultimate beneficial owner holding 30% interest or more, is an independent third party of the Company, its 
subsidiaries, its substantial shareholders, ICBC UBS (International), UBS AG, UBS HK and the companies which are members of the same group of each of the 
Underwriters. 

<<<PAGE 29>>>
27
 
 
(9) ICBC UBS will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their investors (the “ICBC UBS Ultimate 
Clients”), each of which is an independent third party. None of the ICBC UBS Ultimate Clients holds more than 30% ultimate beneficial interest in the relevant funds. 
ICBC UBS has confirmed that, to the best of their knowledge, each of the ICBC UBS Ultimate Clients is an independent party of ICBC UBS, UBS AG, UBS HK and 
the companies which are members of the same group of companies as each of the Underwriters. 
 

<<<PAGE 30>>>
28
 
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
The Offer Shares are being offered and sold outside the United States to investors that are not U.S. persons 
nor persons acquiring for the account or benefit of U.S. persons in reliance on Regulation S under the U.S. 
Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. This announcement is not a prospectus. Potential investors should 
read the Prospectus dated December 31, 2025 issued by GigaDevice Semiconductor Inc. for detailed 
information about the Global Offering described below before deciding whether or not to invest in the H 
Shares thereby being offered.
*Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators 
(for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence 
of any of the events set out in the section headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Hong Kong Underwriting Agreement – Grounds for Termination” 
in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently 
expected to be on January 13, 2026). 
 
 

<<<PAGE 31>>>
29 
 
PUBLIC FLOAT AND FREE FLOAT 
Immediately after the completion of the Global Offering (before any exercise of the Overallotment Option), 
the total market value of the H Shares to be held by the public is expected to be approximately HK$4,684.4 
million, calculated based on the final Offer Price of HK$162.00, which is higher than the prescribed expected 
market value of H Shares required to be held in public hands of not less than HK$3,000,000,000 under Rule 
19A.13A(2)(b) of the Listing Rules, thereby satisfying Rule 19A.13A(2) of the Listing Rules. 
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the Listing Date. As 
such, H Shares held by the Cornerstone Investors upon the Listing shall not be counted towards the free float 
of the H Shares of the Company at the time of Listing. Based on the Offer Price of HK$162.00 per H Share, 
the Company confirmed that it complies with the free float requirement under Rule 19A.13C(2)(b) of the 
Listing Rules.  
The Directors confirm that, immediately following completion of the Global Offering (before any exercise of 
the Over-allotment Option): (i) the Shares will be held by at least 300 Shareholders at the time of Listing, in 
compliance with Rule 8.08(2) of the Listing Rules; (ii) the three largest public Shareholders will not hold more 
than 50% of the H Shares held in public hands at the time of Listing, in compliance with Rules 8.08(3) and 
8.24 of the Listing Rules; (iii) no place will, individually, be placed more than 10% of the enlarged issued 
share capital of the Company immediately after the Global Offering; and (iv) there will not be any new 
substantial Shareholder (as defined in the Listing Rules) immediately after the Global Offering. 
COMMENCEMENT OF DEALINGS 
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, January 13, 
2026 (Hong Kong time), provided that the Global Offering has become unconditional and the right of 
termination described in the section headed “Underwriting – Underwriting Arrangements and Expenses 
– Hong Kong Public Offering – Grounds for Termination” in the Prospectus has not been exercised. 
Investors who trade the H Shares on the basis of publicly available allocation details prior to the receipt 
of H Share certificates or prior to the H Share certificates becoming valid evidence of title do so entirely 
at their own risk. 
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Tuesday, 
January 13, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange will 
commence at 9:00 a.m. on Tuesday, January 13, 2026 (Hong Kong time). The H Shares will be traded 
in board lots of 100 H Shares each, and the stock code of the H Shares will be 3986. 
By order of the Board  
GigaDevice Semiconductor Inc. 
Mr. Zhu Yiming 
Chairman of the Board and Executive Director 
Beijing, the PRC, January 12, 2026  
As at the date of this announcement, the Board comprises: (i) Mr. Zhu Yiming, Mr. He Wei and Mr. Hu Hong 
as executive Directors; (ii) Ms. Wen Tian as a non-executive Director; and (iii) Mr. Zhou Haitao, Dr. Qian 
He, Ms. Yeung Siuman Shirley, Dr. Chen Jie and Mr. Zheng Xiaodong as independent non-executive Directors. 
