# 配发结果公告抽取任务：3200.HK Shenzhen Han’s CNC Technology Co., Ltd. - H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**05/02/2026 20:55**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0205/2026020502290.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3200.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock 
Exchange”, or the “Hong Kong Stock Exchange”) and Hong Kong Securities Clearing Company Limited 
(“HKSCC”) take no responsibility for the contents of this announcement, make no representation as to its 
accuracy or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings 
as those defined in the prospectus dated January 29, 2026 (the “Prospectus”) of Shenzhen Han’s CNC 
Technology Co., Ltd. (深圳市大族數控科技股份有限公司) (the “Company”). This announcement is 
made by the order of the board (the “Board”) of directors (the “Directors”) of the Company. The Board 
collectively and individually accept responsibility for the accuracy of this announcement.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for any securities. This announcement is not a prospectus. Potential investors should 
read the Prospectus for detailed information about the Global Offering described below before deciding 
whether or not to invest in the Offer Shares. Any investment decision in relation to the Offer Shares should be 
taken solely in reliance on the information provided in the Prospectus.
This announcement is not for release, publication or distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia 
or any other jurisdiction where such distribution is prohibited by laws). This announcement does not 
constitute or form a part of any offer or solicitation to purchase or subscribe for securities in the United 
States or in any other jurisdictions. The securities mentioned herein have not been, and will not be, registered 
under the United States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) 
or securities law of any state or other jurisdiction of the United States. The securities may not be offered, 
sold, pledged or otherwise transferred within the United States except pursuant to an exemption from the 
registration requirements of the U.S. Securities Act and in compliance with any applicable state securities 
laws, or outside the United States unless in compliance with Regulation S under the U.S. Securities Act. 
There will be no public offer of securities in the United States.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities 
Limited as stabilizing manager (the “Stabilizing Manager”) (or its affiliates or any person acting for it), 
on behalf of the Underwriters, to the extent permitted by the applicable laws and regulatory requirements of 
Hong Kong or elsewhere, may over-allocate or effect transactions with a view to stabilizing or supporting the 
market price of the H Shares at such price, in such amounts and in such manners as the Stabilizing Manager, 
its affiliates or any person acting for it may determine and at a level higher than that which might otherwise 
prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing Manager 
(or its affiliates or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, 
if taken, (a) will be conducted at the absolute discretion of the Stabilizing Manager (or its affiliates or any 
person acting for it) and in what the Stabilizing Manager reasonably regards as the best interest of the 
Company, (b) may be discontinued at any time and (c) is required to be brought to an end within 30 days 
of the last day for lodging applications under the Hong Kong Public Offering (which is Thursday, March 5, 
2026). Such Stabilizing action, if taken, may be effected in all jurisdictions where it is permissible to do so, in 
each case in compliance with all applicable laws, rules and regulatory requirements, including the Securities 
and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under 
the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H 
Shares for longer than the stabilization period, which will begin on the Listing Date, and is expected to expire 
on the 30th day after the last day for lodging applications under the Hong Kong Public Offering (which is 
Thursday, March 5, 2026). After this date, when no further stabilizing action may be taken, demand for the H 
Shares, and therefore the price of the H Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to terms and conditions set 
out in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong 
Kong and/or not resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint 
Sponsors and the Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall 
be entitled to terminate the Hong Kong Underwriting Agreement with immediate effect upon the occurrence 
of any of the events set out in the section headed “Underwriting — Underwriting Arrangements and 
Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to 
8:00 a.m. on the Listing Date.

<<<PAGE 2>>>
– 2 –
SHENZHEN HAN’S CNC TECHNOLOGY CO., LTD.
深圳市大族數控科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under the
Global Offering
:
50,451,800 H Shares (subject to the  
Over-allotment Option)
Number of Hong Kong Offer Shares
:
5,045,200 H Shares
Number of International Offer Shares
:
45,406,600 H Shares (subject to the Over-
allotment Option)
Final Offer Price
:
HK$95.80 per H Share, plus brokerage of 1.0%, 
SFC transaction levy of 0.0027%, Hong Kong 
Stock Exchange trading fee of 0.00565% and 
AFRC transaction levy of 0.00015% (payable 
in full on application in Hong Kong dollars 
and subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
3200
Sole Sponsor, Sponsor-Overall Coordinator, Joint Global Coordinator,
Joint Bookrunner and Joint Lead Manager
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
 
3 
 
SHENZHEN HAN’S CNC TECHNOLOGY CO., LTD. / 深圳市大族數控科技股份有限
公司 
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS 
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could move 
substantially even with a small number of the H Shares traded and should exercise extreme caution 
when dealing in the H Shares. 
SUMMARY 
 
Company information 
Stock code  
3200
Stock short name  
HANS CNC
Dealings commencement date 
February 6, 2026*
*see note at the end of the announcement 
 
Price Information  
Final Offer Price 
HK$95.80
Maximum Offer Price 
HK$95.80
 
Offer Shares and Share Capital 
Number of Offer Shares 
50,451,800
Final Number of Offer Shares in Hong Kong Public Offering
5,045,200
Final Number of Offer Shares in International Offering 
45,406,600
Number of issued Shares upon Listing (before exercise of the 
Over-allotment Option) 
475,960,952 
 
Over-allocation 
No. of Offer Shares over-allocated 
7,567,700
- 
International Offering 
7,567,700
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases 
in the secondary market at prices that do not exceed the Offer Price or through deferred delivery or a 
combination of these means. In the event the Over-allotment Option is exercised, an announcement will 
be made on the Stock Exchange’s website.
 
Proceeds   
Gross proceeds (Note)  
HK$4,833.3 million
Less: Estimated listing expenses payable based on final 
Offer Price  
HK$202.6 million 
Net proceeds  
HK$4,630.7 million
 
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use 
of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis. 
 

<<<PAGE 4>>>
4 
 
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING 
 
No. of valid applications  
159,985
No. of successful applications  
38,958
Subscription level 
446.39 times
Claw-back triggered  
N/A
No. of Offer Shares initially available under the Hong Kong Public 
Offering  
5,045,200 
Final no. of Offer Shares under the Hong Kong Public Offering 
5,045,200
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering 
10% 
 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/iporesult to perform a search by name or identification number or www.hkeipo.hk/iporesult 
for the full list of allottees. 
INTERNATIONAL OFFERING 
 
No. of placees 
218
Subscription level 
21.07 times
No. of Offer Shares initially available under the International 
Offering  
45,406,600 
Final no. of Offer Shares under the International Offering 
45,406,600
% of Offer Shares under the International Offering to the Global 
Offering 
90% 
% of final no. of Offer Shares under the International Offering to 
the Global Offering (after over-allocation) 
91.30% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a waiver from 
strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) of Appendix F1 
to the Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange to permit H Shares in the 
International Offering to be placed to certain Existing Minority Shareholders and/or their close associates; 
and (b) a consent under Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to, 
among other things, allocate further H Shares in the International Offering to certain existing Shareholders 
and Cornerstone Investors and/or their respective close associates, (i) none of the Offer Shares subscribed by 
the placees and the public have been financed directly or indirectly by the Company, any of the Directors, 
chief executive of the Company, members of the Controlling Shareholders Group, substantial Shareholders, 
existing Shareholders of the Company or any of its subsidiaries or their respective close associates; and (ii) 
none of the placees and the public who have purchased the Offer Shares are accustomed to taking instructions 
from the Company, any of the Directors, chief executive of the Company, members of the Controlling 
Shareholders Group, substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries 
or their respective close associates in relation to the acquisition, disposal, voting or other disposition of the H 
Shares registered in his/her/its name or otherwise held by him/her/it.  
The placees in the International Offering include the following: 
Cornerstone Investors 

<<<PAGE 5>>>
5 
 
 
Investor 
No. of Offer 
Shares 
allocated 
% of H Shares 
(assuming 
the 
Over-allotment 
Option is not 
exercised) Note 1 
% of total issued 
share capital after 
the Global Offering 
(assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Existing 
shareholders or 
their 
close 
associates Note 2 
Hongxing International 
Technology Limited (宏興國
際科技有限公司) (“Hongxing 
International”)
4,884,200
9.68%
1.03%
No
GIC Private Limited
7,326,300
14.52%
1.54%
No
Schroder 
Investment 
Management (Singapore) Ltd 
and 
Schroder 
Investment 
Management 
(Hong 
Kong) 
Limited (“Schroders”)
6,105,200
12.10%
1.28%
No
HHLR 
Advisors, 
Ltd. 
(“HHLRA”)
2,035,000
4.03%
0.43%
No
Morgan 
Stanley 
& 
Co. 
International plc (“MSIP”)
814,000
1.61%
0.17%
Yes
Fullgoal
814,000
1.61%
0.17%
Fullgoal Asset Management 
(HK) Limited (“Fullgoal 
HK”) Note 3
244,200
0.48%
0.05%
No
Fullgoal Fund Management 
Co., Ltd. (“Fullgoal Fund”) 
Note 3
569,800
1.13%
0.12%
No
Tibet 
Longrising 
Asset 
Management Co., Ltd. (“Tibet 
Longrising”) Note 4 and CICC 
Financial 
Trading 
Limited 
(“CICC FT”) (in connection 
with the Tibet Longrising OTC 
Swaps)
814,000
1.61%
0.17%
Yes
ICBC Wealth Management 
Co., Ltd. (“ICBC Wealth”)
814,000
1.61%
0.17%
No
Wind Sabre Fund SPC on 
behalf 
of 
Wind 
Sabre 
Opportunities Fund SP (“Wind 
Sabre”)
814,000
1.61%
0.17%
No
WILL Semiconductor Limited 
(“OmniVision HK”)
797,700
1.58%
0.17%
No
Total 
25,218,400 
49.99% 
5.30% 
 
Notes: 
 
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the

<<<PAGE 6>>>
6 
 
 
Investor 
No. of Offer 
Shares 
allocated 
% of H Shares 
(assuming 
the 
Over-allotment 
Option is not 
exercised) Note 1 
% of total issued 
share capital after 
the Global Offering 
(assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Existing 
shareholders or 
their 
close 
associates Note 2 
Global Offering.  
 
2. 
In addition to the Offer Shares subscribed for as Cornerstone Investors, GIC Private Limited, Schroders, HHLRA, MSIP, Fullgoal 
HK, Fullgoal Fund, Tibet Longrising, IBCB Wealth, Wind Sabre, OmniVision HK and/or their close associates were allocated 
further Offer Shares as placees in the International Offering. Please refer to the section headed “Allotment Results Details — 
International Offering — Allottees with Waivers/Consents Obtained” in this announcement for details. Only the Offer Shares 
subscribed for as Cornerstone Investors are subject to lock-up restrictions as indicated below. For details, please refer to the 
section headed “Lock-up Undertakings — Cornerstone Investors” in this announcement. 
 
3. 
It was stated in the Prospectus (see page 315 thereof) that (i) Fullgoal HK will acquire 569,800 Offer Shares and which represent 
1.13% of the Offer Shares and 0.12% of the Company’s total issued share capital immediately upon completion of the Global 
Offering, assuming the Over-allotment Option is not exercised, and 0.98% of the Offer Shares and 0.12% of the Company’s total 
issued share capital, assuming the Over-allotment Option is exercised in full; and (ii) Fullgoal Fund will acquire 244,200 Offer 
Shares and which represent 0.48% of the Offer Shares and 0.05% of the Company’s total issued share capital immediately upon 
completion of the Global Offering, assuming the Over-allotment Option is not exercised, and 0.42% of the Offer Shares and 0.05% 
of the Company’s total issued share capital, assuming the Over-allotment Option is exercised in full. There were typos in respect 
of these figures stated in the Prospectus. The accurate figures regarding the number of Offer Shares to be acquired by Fullgoal HK 
and Fullgoal Fund as Cornerstone Investors, and their respective percentages of the Offer Shares and the Company’s total issued 
share capital are those stated in the above table of this announcement. Such amendments are not material and the total number of 
Offer Shares to be acquired by Fullgoal HK and Fullgoal Fund in aggregate as Cornerstone Investors stated in this announcement 
is the same as such number stated in the Prospectus. 
 
4. 
To the best of the knowledge, information and belief of the Company, one of the ultimate clients in connection with the Tibet 
Longrising OTC Swaps (the “CICC FT Ultimate Clients (Tibet Longrising)”) managed by Tibet Longrising is an existing minority 
Shareholder, holding not more than 1% of the issued share capital of the Company as of the date of this announcement. 
 
 

<<<PAGE 7>>>
7 
 
 
Allottees with Waivers/Consents Obtained 
 
 
Investor 
No. 
of 
Offer 
Shares allocated 
% of H Shares 
(assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) Note 1 
% of total issued 
share capital after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) 
Relationship 
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by Existing Minority 
Shareholders holding more than 1% of the issued share capital of the Company immediately prior to the 
completion of the Global Offering and/or their close associates 
Nil 
Nil 
Nil 
Nil 
Nil 
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in 
relation to allocations of further H Shares to existing Shareholders and Cornerstone Investors and/or 
their close associates Note 2 
GIC Private Limited 
975,000 
1.93% 
0.20% 
Same entity as the 
Cornerstone 
Investor 
Schroder Investment 
Management 
(Singapore) Ltd 
814,000 
1.61% 
0.17% 
Same entity as the 
Cornerstone 
Investor 
Hillhouse Investment 
Management Limited 81,400 
0.16% 
0.02% 
A close associate 
of the 
Cornerstone 
Investor 
MSIP
40,800 
0.08% 
0.01% 
Same entity as the 
Cornerstone 
Investor and 
existing 
Shareholder
Morgan Stanley 
Investment 
Management 
Company 
13,800 
0.03% 
0.00% 
A close associate 
of the 
Cornerstone 
Investor
Fullgoal
40,800 
0.08% 
0.01% 
Fullgoal HK 
15,200 
0.03% 
0.00% 
Same entity as the 
Cornerstone 
Investor
Fullgoal Fund 
25,600 
0.05% 
0.01% 
Same entity as the 
Cornerstone 
Investor
Tibet Longrising and 
CICC FT (in 
connection with the 
Tibet Longrising 
OTC Swaps)
30,600 
0.06% 
0.01% 
Same entity as the 
Cornerstone 
Investor and 
existing 
Shareholder

<<<PAGE 8>>>
8 
 
 
Investor 
No. 
of 
Offer 
Shares allocated 
% of H Shares 
(assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) Note 1 
% of total issued 
share capital after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) 
Relationship 
Longrising 
Prosperous China 
Fund
10,200 
0.02% 
0.00% 
A close associate 
of the 
Cornerstone 
Investor
ICBC Wealth
40,800 
0.08% 
0.01% 
Same entity as the 
Cornerstone 
Investor
Wind Sabre Capital 
Limited
40,800 
0.08% 
0.01% 
A close associate 
of the 
Cornerstone 
Investor
OmniVision HK
40,800 
0.08% 
0.01% 
Same entity as the 
Cornerstone 
Investor
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients Note 3 
CICC FT 
CICC FT Ultimate 
Clients (Tibet 
Longrising): 
814,000 
1.61% 
0.17% 
Connected client 
as a Cornerstone 
Investor 
CICC FT Ultimate 
Clients (Tibet 
Longrising): 
30,600 
0.06% 
0.01% 
Connected client 
as a placee 
Other ultimate 
clients (the 
“Other CICC FT 
Ultimate 
Clients”): 
9,371,200 
18.57% 
1.97% 
Connected client 
as a placee 
Bosera Asset 
Management 
(International) Co., 
Ltd (“Bosera AM”) 
40,800 
0.08% 
0.01% 
Connected client 
as a placee 
CITIC Securities 
International Capital 
Management Limited 
(“CSICM”) 
13,800 
0.03% 
0.00% 
Connected client 
as a placee 
China Asset 
Management (Hong 
Kong) Limited 
(“China AMC HK”) 24,500 
0.05% 
0.01% 
Connected client 
as a placee 

<<<PAGE 9>>>
9 
 
 
Investor 
No. 
of 
Offer 
Shares allocated 
% of H Shares 
(assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) Note 1 
% of total issued 
share capital after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) 
Relationship 
CITIC Securities 
Asset Management 
Co., Ltd. (“CITICS 
AM”) 
2,500 
0.00% 
0.00% 
Connected client 
as a placee 
ICBC UBS Asset 
Management Co., 
Ltd. (“ICBC UBS”) 
40,800 
0.08% 
0.01% 
Connected client 
as a placee 
UBS Asset 
Management 
(Singapore) Limited 
(“UBS AM 
Singapore”) 
81,400 
0.16% 
0.02% 
Connected client 
as a placee 
Huatai Capital 
Investment Limited 
(“HTCI”) 
89,300 
0.18% 
0.02% 
Connected client 
as a placee 
Notes: 
 
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the 
Global Offering. 
 
2. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the number of Offer Shares 
allocated to the investors as placees in the International Offering. For allocations of Offer Shares to the relevant investors and/or 
their close associates as Cornerstone Investors, please refer to the section headed “Allotment Results Details — International 
Offering — Cornerstone Investors” in this announcement. For details of the consent under paragraph 18 of Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations of further H Shares to the existing Shareholders and Cornerstone 
Investors and/or their close associates, please refer to the section headed “Others / Additional Information — Allocations of Offer 
Shares to the existing Shareholders and Cornerstone Investors and/or their close associates with a consent under paragraph 18 of 
Chapter 4.15 of the Guide for New Listing Applicants” in this announcement. 
 
3. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations to connected clients, please refer to the sections headed “Others / Additional Information — 
Placing to connected clients with a consent under paragraph 1C(1) of the Placing Guidelines” and “Others / Additional 
Information — Allocations of Offer Shares to the existing Shareholders and the Cornerstone Investors and/or their close associates 
with a consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants” in this announcement. 
 
LOCK-UP UNDERTAKINGS  
Controlling Shareholders Group 

<<<PAGE 10>>>
10 
 
Name Note 1 
Number 
and 
description 
of 
Shares held in 
the 
Company 
subject to lock-
up undertakings 
upon Listing  
% of total issued H 
Shares after the Global 
Offering 
subject 
to 
lock-up 
undertakings 
(assuming the Over-
allotment Option is not 
exercised) Note 2 
% of shareholding in 
the Company subject 
to 
lock-up 
undertakings 
(assuming the Over-
allotment Option is 
not exercised) 
Last day subject to 
the 
lock-up 
undertakings Note 3 
Han’s 
Laser 
355,868,100 
A 
Shares 
- 
74.77% 
August 5, 2026 (First 
Six-month 
Period) 
Note 4 
February 
5, 
2027 
(Second 
Six-month 
Period) Note 5 
Dazu 
Holdings 
3,231,900 
A 
Shares 
- 
0.68% 
August 5, 2026 (First 
Six-month 
Period) 
Note 4 
February 
5, 
2027 
(Second 
Six-month 
Period) Note 5
Notes: 
 
1. 
For illustrative purposes only, this subsection lists only those members of the Controlling Shareholders Group who hold Shares 
directly in the Company. Pursuant to Rule 10.07 of the Listing Rules, each member of the Controlling Shareholders Group 
(namely, Mr. Gao, Han’s Laser, Dazu Holdings and Han’s Global) has undertaken to the Stock Exchange and the Company 
that, except in connection with the Global Offering (including the Over-allotment Option), he or it shall, and shall procure that 
the relevant registered holders of the Shares in which he or it is beneficially interested shall, comply with the applicable lock-
up requirements. For further details, please refer to the section headed “Underwriting — Underwriting Arrangements and 
Expenses — Hong Kong Public Offering — Undertakings to the Stock Exchange pursuant to the Listing Rules — Undertakings 
by the Controlling Shareholders Group” in the Prospectus. 
 
2. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under 
the Global Offering. 
 
3. 
In accordance with the applicable Listing Rules, the required lock-up for the first six-month period will end on August 5, 2026 
and for the second six-month period will end on February 5, 2027. 
 
4. 
The Controlling Shareholders may dispose of or transfer Shares after the indicated date subject to that the Controlling 
Shareholders will not cease to be a Controlling Shareholder. 
 
5. 
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after the indicated date. 
 
Cornerstone Investors 
Name 
Number 
and 
description 
of 
Shares held in the 
Company subject to 
lock-up 
undertakings upon 
Listing  
% of total issued H 
Shares 
after 
the 
Global 
Offering 
subject to lock-up 
undertakings 
(assuming the Over-
allotment Option is 
not exercised) Note 1 
% of shareholding in 
the Company subject 
to 
lock-up 
undertakings 
(assuming the Over-
allotment Option is 
not exercised) 
Last 
day 
subject to the 
lock-up 
undertakings 
Note 2 
Hongxing 
International 
4,884,200 H Shares 
9.68% 
1.03% 
August 
5, 
2026 
GIC Private 
Limited 
7,326,300 H Shares 
14.52% 
1.54% 
August 
5, 
2026 

<<<PAGE 11>>>
11 
 
Name 
Number 
and 
description 
of 
Shares held in the 
Company subject to 
lock-up 
undertakings upon 
Listing  
% of total issued H 
Shares 
after 
the 
Global 
Offering 
subject to lock-up 
undertakings 
(assuming the Over-
allotment Option is 
not exercised) Note 1 
% of shareholding in 
the Company subject 
to 
lock-up 
undertakings 
(assuming the Over-
allotment Option is 
not exercised) 
Last 
day 
subject to the 
lock-up 
undertakings 
Note 2 
Schroders 
6,105,200 H Shares 
12.10% 
1.28% 
August 
5, 
2026 
HHLRA 
2,035,000 H Shares 
4.03% 
0.43% 
August 
5, 
2026 
MSIP 
814,000 H Shares 
1.61% 
0.17% 
August 
5, 
2026
Fullgoal 
814,000 H Shares 
1.61% 
0.17% 
August 
5, 
2026
Fullgoal HK 
244,200 H Shares
0.48%
0.05%
August 
5, 
2026
Fullgoal Fund 
569,800 H Shares
1.13%
0.12%
August 
5, 
2026
Tibet Longrising 
and CICC FT (in 
connection with 
the Tibet 
Longrising OTC 
Swaps)
814,000 H Shares 
1.61% 
0.17% 
August 
5, 
2026 
ICBC Wealth 
814,000 H Shares 
1.61% 
0.17% 
August 
5, 
2026
Wind Sabre 
814,000 H Shares 
1.61% 
0.17% 
August 
5, 
2026
OmniVision HK 
797,700 H Shares 
1.58% 
0.17% 
August 
5, 
2026
Notes: 
 
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the Global 
Offering. 
 
2. 
In accordance with the relevant cornerstone investment agreements, the required lock-up periods will end on August 5, 2026. The 
Cornerstone Investors will cease to be prohibited from disposing of or transferring the H Shares subscribed for pursuant to the relevant 
cornerstone investment agreements after the indicated date. 

<<<PAGE 12>>>
12 
 
PLACEE CONCENTRATION ANALYSIS 
Placees* 
Number of H Shares 
allotted 
Allotment as % 
of the 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option) 
Allotment as % 
of the 
International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised)
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
as % of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised)
Number of H 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing 
(assuming no 
exercise of the 
Over-
allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming the 
Over-
allotment 
Option is 
fully 
exercised)
Top 1
9,371,200
20.64%
17.69%
18.57%
16.15%
9,371,200
1.97%
1.94%
Top 5
34,156,600
75.22%
64.48%
67.70%
58.87%
34,156,600
7.18%
7.06%
Top 10
40,031,200
88.16%
75.57%
79.35%
69.00%
40,031,200
8.41%
8.28%
Top 25
47,974,500
105.66%
90.56%
95.09%
82.69%
47,974,500
10.08%
9.92%
 
Note: 
* Ranking of placees is based on the number of H Shares allotted to the placees. 
 
 

<<<PAGE 13>>>
 
13 
 
H SHAREHOLDERS CONCENTRATION ANALYSIS 
H 
Shareholders* 
Number of H 
Shares 
allotted 
Allotment as % 
of the 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option) 
Allotment as % 
of the 
International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised)
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
as % of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised)
Number of H 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing 
(assuming no 
exercise of the 
Over-
allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming the 
Over-
allotment 
Option is fully 
exercised)
Top 1
9,371,200
20.64%
17.69%
18.57%
16.15%
9,371,200
1.97%
1.94%
Top 5
34,156,600
75.22%
64.48%
67.70%
58.87%
34,156,600
7.18%
7.06%
Top 10
40,031,200
88.16%
75.57%
79.35%
69.00%
40,031,200
8.41%
8.28%
Top 25
47,974,500
105.66%
90.56%
95.09%
82.69%
47,974,500
10.08%
9.92%
 
Note: 
* Ranking of H Shareholders is based on the number of H Shares held by the Shareholders upon Listing. 
 
 

<<<PAGE 14>>>
 
14 
 
SHAREHOLDERS CONCENTRATION ANALYSIS 
Shareholders* 
Number of H Shares 
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
Option is 
fully 
exercised)
Allotment 
as % of total 
Offer Shares 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Allotment 
as % of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised)
Number of 
H Shares 
held upon 
Listing
Number of 
Shares held 
upon 
Listing
% of total 
issued 
share 
capital 
upon 
Listing 
(assuming 
no 
exercise 
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
Option is 
fully 
exercised)
Top 1
0
0
0
0
0
0 359,100,000
75.45%
74.27%
Top 5
24,591,700
54.16%
46.42%
48.74%
42.39% 24,591,700 390,344,249
82.01%
80.73%
Top 10
36,273,000
79.88%
68.47%
71.90%
62.52% 36,273,000 408,064,366
85.73%
84.39%
Top 25
45,021,300
99.15%
84.99%
89.24%
77.60% 45,021,300 421,912,428
88.64%
87.26%
 
Notes: 
* Ranking of Shareholders is based on the number of Shares held by the Shareholders upon Listing. 
 

<<<PAGE 15>>>
15 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below: 
 
NO. 
OF 
H 
SHARES 
APPLIED 
FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF ALLOTMENT / 
BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF THE 
TOTAL NO. OF H 
SHARES 
APPLIED 
FOR 
 
 
 
POOL A 
 
 
 
100
62,539
6,254 out of 62,539 applicants to 
receive 100 H Shares
10.00%
200
6,977
831 out of 6,977 applicants to 
receive 100 H Shares
5.96%
300
5,932
782 out of 5,932 applicants to 
receive 100 H Shares
4.39%
400
2,815
399 out of 2,815 applicants to 
receive 100 H Shares
3.54%
500
12,684
1,901 out of 12,684 applicants to 
receive 100 H Shares
3.00%
600
2,064
324 out of 2,064 applicants to 
receive 100 H Shares
2.62%
700
938
153 out of 938 applicants to 
receive 100 H Shares
2.33%
800
1,066
180 out of 1,066 applicants to 
receive 100 H Shares
2.11%
900
930
162 out of 930 applicants to 
receive 100 H Shares
1.94%
1,000
8,571
1,529 out of 8,571 applicants to 
receive 100 H Shares
1.78%
1,500
3,069
606 out of 3,069 applicants to 
receive 100 H Shares
1.32%
2,000
3,093
657 out of 3,093 applicants to 
receive 100 H Shares
1.06%
2,500
2,035
457 out of 2,035 applicants to 
receive 100 H Shares
0.90%
3,000
2,111
496 out of 2,111 applicants to 
receive 100 H Shares
0.78%
3,500
1,356
332 out of 1,356 applicants to 
receive 100 H Shares
0.70%
4,000
1,542
390 out of 1,542 applicants to 
receive 100 H Shares
0.63%
4,500
1,131
295 out of 1,131 applicants to 
receive 100 H Shares
0.58%
5,000
2,779
743 out of 2,779 applicants to 
receive 100 H Shares
0.53%

<<<PAGE 16>>>
16 
 
6,000
2,075
581 out of 2,075 applicants to 
receive 100 H Shares
0.47%
7,000
1,872
545 out of 1,872 applicants to 
receive 100 H Shares
0.42%
8,000
1,431
431 out of 1,431 applicants to 
receive 100 H Shares
0.38%
9,000
1,358
421 out of 1,358 applicants to 
receive 100 H Shares
0.34%
10,000
7,230
2,298 out of 7,230 applicants to 
receive 100 H Shares
0.32%
20,000
4,366
1,652 out of 4,366 applicants to 
receive 100 H Shares
0.19%
30,000
2,554
1,070 out of 2,554 applicants to 
receive 100 H Shares
0.14%
40,000
1,632
735 out of 1,632 applicants to 
receive 100 H Shares
0.11%
50,000
2,103
1,002 out of 2,103 applicants to 
receive 100 H Shares
0.10%
Total 
146,253
Total number of Pool A 
successful applicants: 25,226
POOL B 
60,000
6,272
100 H Shares plus 3,136 out of 
6,272 applicants to receive an 
additional 100 H Shares
0.25%
70,000
1,178
100 H Shares plus 703 out of 
1,178 applicants to receive an 
additional 100 H Shares
0.23%
80,000
847
100 H Shares plus 580 out of 847 
applicants 
to 
receive 
an 
additional 100 H Shares
0.21%
90,000
602
100 H Shares plus 462 out of 602 
applicants 
to 
receive 
an 
additional 100 H Shares
0.20%
100,000
2,684
100 H Shares plus 2,263 out of 
2,684 applicants to receive an 
additional 100 H Shares
0.18%
200,000
1,095
200 H Shares plus 480 out of 
1,095 applicants to receive an 
additional 100 H Shares
0.12%
300,000
401
200 H Shares plus 350 out of 401 
applicants 
to 
receive 
an 
additional 100 H Shares
0.10%
400,000
206
300 H Shares plus 47 out of 206 
applicants 
to 
receive 
an 
additional 100 H Shares
0.08%
500,000
107
300 H Shares plus 57 out of 107 
applicants 
to 
receive 
an 
additional 100 H Shares
0.07%

<<<PAGE 17>>>
17 
 
600,000
63
300 H Shares plus 51 out of 63 
applicants 
to 
receive 
an 
additional 100 H Shares
0.06%
700,000
38
400 H Shares plus 2 out of 38 
applicants 
to 
receive 
an 
additional 100 H Shares
0.06%
800,000
33
400 H Shares plus 9 out of 33 
applicants 
to 
receive 
an 
additional 100 H Shares
0.05%
900,000
25
400 H Shares plus 12 out of 25 
applicants 
to 
receive 
an 
additional 100 H Shares
0.05%
1,000,000
89
400 H Shares plus 60 out of 89 
applicants 
to 
receive 
an 
additional 100 H Shares
0.05%
1,500,000
35
500 H Shares plus 18 out of 35 
applicants 
to 
receive 
an 
additional 100 H Shares
0.04%
2,000,000
15
600 H Shares plus 3 out of 15 
applicants 
to 
receive 
an 
additional 100 H Shares
0.03%
2,522,600
42
600 H Shares plus 33 out of 42 
applicants 
to 
receive 
an 
additional 100 H Shares
0.03%
Total 
13,732
Total 
number of 
Pool 
B 
successful applicants: 13,732
 
COMPLIANCE WITH LISTING RULES AND GUIDANCE  
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the H Shares.  
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the 
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by 
them is the same as the final Offer Price in addition to any brokerage, AFRC transaction levy, SFC 
transaction levy and trading fee payable. 
OTHERS / ADDITIONAL INFORMATION 
 
Allocation of H Shares to Existing Minority Shareholders and their close associates 
 
The Company has applied for, and the Stock Exchange has granted, a waiver from strict compliance 
with Rule 10.04 of, and a consent under paragraph 1C(2) of Appendix F1 to, the Listing Rules to 
permit H Shares in the International Offering to be placed to certain existing minority Shareholders 
who (i) hold less than 5% of the total number of A Shares in issue of the Company prior to the 
completion of the Global Offering and (ii) are not and will not become (upon the completion of the 
Global Offering) core connected persons of the Company or the close associates of any such core 
connected person (together, the “Existing Minority Shareholders”), on the following conditions: 
 

<<<PAGE 18>>>
18 
 
(i) 
each Existing Minority Shareholder to whom the Company may allocate the H Shares in 
the International Offering holds less than 5% of the total number of A Shares in issue of 
the Company before Listing; 
 
(ii) 
each Existing Minority Shareholder is not, and will not be, a core connected person of the 
Company or any close associate of any such core connected person immediately prior to or 
following the Global Offering; 
 
(iii) 
none of the Existing Minority Shareholders has the right to appoint a Director and/or have 
any other special rights; 
 
(iv) 
allocation to the Existing Minority Shareholders or their close associates will not affect the 
Company’s ability to satisfy the public float requirement as prescribed by the Stock 
Exchange under Rule 8.08 (as amended and replaced by Rule 19A.13A) of the Listing 
Rules; 
 
(v) 
no preferential treatment is given to the Existing Minority Shareholders or their respective 
close associates (other than the assured entitlement for a cornerstone investor); and 
 
(vi) 
details of the allocation to the Existing Minority Shareholders and/or their respective close 
associates holding more than 1% of the issued share capital of the Company immediately 
prior to the completion of the Global Offering has been disclosed in this announcement. 
 
Please refer to the section headed “Waivers from Strict Compliance with the Listing Rules and 
Exemptions from the Companies (Winding Up and Miscellaneous Provisions) Ordinance — 
Allocation of H Shares to Existing Minority Shareholders and Their Close Associates” in the 
Prospectus for further details of the waiver and consent. As the A Shares are listed on the Shenzhen 
Stock Exchange since 2022, the Company has a highly extensive base of existing Shareholders and 
disclosure of details of allocations to all Existing Minority Shareholders and/or their respective close 
associates will not be meaningful to investors, the proposed disclosure threshold, i.e. condition (vi) of 
the waiver and consent which provides that details of the allocation to the Existing Minority 
Shareholders and/or their respective close associates holding more than 1% of the issued share capital 
of the Company immediately prior to the completion of the Global Offering will be disclosed in this 
announcement, is appropriate. 
 
Allocations of Offer Shares to existing Shareholders and Cornerstone Investors and/or their 
close associates with a consent under Chapter 4.15 of the Guide for New Listing Applicants 
 
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 of 
the Guide for New Listing Applicants to permit the Company to allocate further Offer Shares in the 
International Offering to certain existing Shareholders and Cornerstone Investors and/or their close 
associates as placees, subject to the following conditions (the “Allocation to Size-based Exemption 
Participants”): 
 
(a) the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion; 
 
(b)  the Offer Shares allocated to all existing Shareholders (whether as Cornerstone Investors and/or 
as placees) as permitted under this exemption do not exceed 30% of the total number of Offer 
Shares offered under the Global Offering; 

<<<PAGE 19>>>
19 
 
 
(c)  the Allocation to Size-based Exemption Participants will not affect the Company’s ability to 
satisfy its public float requirement under Rule 8.08(1) (as amended and replaced by Rule 
19A.13A) of the Listing Rules; 
 
(d) each of the Directors, chief executive of the Company and member of the Controlling 
Shareholders Group confirms that no securities have been allocated to them or their respective 
close associates under this exemption; and 
 
(e) details of the Cornerstone Investors and/or their close associates under this exemption will be 
disclosed in this announcement. 
 
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted 
by the Stock Exchange. 
 
For details of the allocations of Offer Shares to Cornerstone Investors, please refer to the section 
headed “Allotment Results Details – International Offering – Allottees with Waivers/Consents 
Obtained” in this announcement. 
 
Placing to connected clients with a consent under paragraph 1C(1) of the Placing Guidelines 
 
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a consent 
under paragraph 1C(1) of the Placing Guidelines to permit CICC FT (in connection with the Tibet 
Longrising OTC Swaps), as a connected client, to participate in the Global Offering as a Cornerstone 
Investor. For details of the consent granted, please refer to “Waivers from Strict Compliance with the 
Listing Rules and Exemptions from the Companies (Winding Up and Miscellaneous Provisions) 
Ordinance — Consent in respect of the Proposed Subscription of Offer Shares by a Cornerstone 
Investor Who Is a Connected Client” in the Prospectus. 
 
In addition, under the International Offering, certain Offer Shares were placed to connected clients of 
their connected distributors pursuant to the Placing Guidelines as placees. Please refer to the section 
headed “Allotment Results Details — International Offering — Allottees with Waivers/Consents 
Obtained” in this announcement for details. The Company has applied to the Stock Exchange for, and 
the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing Guidelines to permit 
the Company to allocate such Offer Shares in the International Offering to the connected clients as 
placees. The allocation of Offer Shares to such connected clients is in compliance with all the 
conditions under the consent granted by the Stock Exchange. Details of the placement to connected 
clients as placees are set out below: 

<<<PAGE 20>>>
20 
 
 
No. 
Connected 
Distributor 
Connected 
Client 
Relationship 
Whether the 
connected client 
is a collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Whether the 
connected client will 
hold the beneficial 
interests of the Offer 
Shares on a non-
discretionary basis 
or discretionary 
basis for 
independent third 
parties 
Number of Offer 
Shares to be 
allocated to the 
Connected Client 
Approximate percentage 
of total number of Offer 
Shares under the Global 
Offering (assuming no 
exercise of the Over-
allotment Option) 
Approximate percentage of 
total issued share capital 
immediately following the 
Global Offering (assuming 
the Over-allotment Option is 
not exercised) 
1.  
China 
International 
Capital 
Corporation 
Hong Kong 
Securities 
Limited 
(“CICCHKS”) 
CICC FT 
CICC FT is a 
member of the 
same group of 
CICCHKS. 
N 
Non-discretionary 
basis 
CICC FT Ultimate 
Clients 
(Tibet 
Longrising) 
Note 
1: 
30,600 
0.06%
0.01%
2.  
Other 
CICC 
FT 
Ultimate Clients Note 
2: 9,371,200 
18.57% 
1.97% 
3.  
CMB 
International 
Securities 
Limited 
(“CMBI”) and 
China Merchants 
Securities (HK) 
Co., Limited 
(“CMS HK”)
Bosera AM Note 3 
Bosera AM is a 
member of the 
same group of 
CMBI and CMS 
HK. 
N 
Discretionary basis 
40,800 
0.08% 
0.01% 
4.  
CITIC Securities 
Brokerage (Hong 
Kong) Limited 
(“CSB”) 
CSICM Note 4 
CSICM is a 
member of the 
same group of 
CSB.
N 
Non-discretionary 
basis 
13,800 
0.03% 
0.00% 
5.  
China AMC HK 
Note 5 
China AMC HK 
is a member of 
the same group 
of CSB.
N 
Discretionary basis 
24,500 
0.05% 
0.01% 

<<<PAGE 21>>>
21 
 
__________ 
Notes: 
1. CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one OTC swap transactions (the “OTC Swaps”) with each 
other and the CICC FT Ultimate Clients (Tibet Longrising), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the OTC Swaps 
while the economic risks and returns of the underlying Offer Shares are passed to the CICC FT Ultimate Clients (Tibet Longrising), subject to customary fees and 
commissions. The OTC Swaps will be fully funded by the CICC FT Ultimate Clients (Tibet Longrising). During the terms of the OTC Swaps, all economic returns of 
the Offer Shares subscribed by CICC FT will be passed to the CICC FT Ultimate Clients (Tibet Longrising) and all economic loss shall be borne by the CICC FT Ultimate 
Clients (Tibet Longrising) through the OTC Swaps, and CICC FT will not take part in any economic return or bear any economic loss in relation to the Offer Shares. The 
OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate Clients (Tibet Longrising) may request CICC FT to redeem it at their own discretions, upon which 
CICC FT shall dispose of the Offer Shares and settle OTC Swaps in cash in accordance with the terms and conditions of the OTC Swap. Despite that CICC FT will hold 
No. 
Connected 
Distributor 
Connected 
Client 
Relationship 
Whether the 
connected client 
is a collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Whether the 
connected client will 
hold the beneficial 
interests of the Offer 
Shares on a non-
discretionary basis 
or discretionary 
basis for 
independent third 
parties 
Number of Offer 
Shares to be 
allocated to the 
Connected Client 
Approximate percentage 
of total number of Offer 
Shares under the Global 
Offering (assuming no 
exercise of the Over-
allotment Option) 
Approximate percentage of 
total issued share capital 
immediately following the 
Global Offering (assuming 
the Over-allotment Option is 
not exercised) 
6.  
CITICS AM Note 
6 
CITICS AM is a 
member of the 
same group of 
CSB.
N 
Discretionary basis 
2,500 
0.00% 
0.00% 
7.  
UBS AG Hong 
Kong Branch 
(“UBS AG”) 
ICBC UBS Note 7 
ICBC UBS is a 
member of the 
same group of 
UBS AG.
N 
Discretionary basis 
40,800 
0.08% 
0.01% 
8.  
UBS AM 
Singapore Note 8 
UBS AM 
Singapore is a 
member of the 
same group of 
UBS AG.
N 
Discretionary basis 
81,400 
0.16% 
0.02% 
9.  
Huatai Financial 
Holdings (Hong 
Kong) Limited 
(“HTFH”)
HTCI Note 9 
HTCI is a 
member of the 
same group of 
HTFH.
N 
Non-discretionary 
basis 
89,300 
0.18% 
0.02% 

<<<PAGE 22>>>
22 
 
the legal title of the Offer Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares during the terms of the OTC Swaps according to its 
internal policy. 
 
Details of the CICC FT Ultimate Clients (Tibet Longrising) are set out as below: 
 
Name of the CICC FT Ultimate Clients (Tibet Longrising) 
Ultimate beneficial owner(s) holding 30% or more interest (if any) 
Longrising Shengshi No. 8 Private Securities Investment Fund (源樂晟晟世8 號私
募證券投資基金) 
Zeng Xiaojie (曾曉潔) 
Longrising Qiangshu Private Securities Investment Fund (源樂晟強樹私募證券投
資基金) 
Zeng Xiaojie (曾曉潔) 
Longrising Xinyun Private Securities Investment Fund (源乐晟新雲私募证券投资
基金) 
Yang Jianhai (楊建海) 
Longrising Xinsheng No.1 Private Securities Investment Fund (源樂晟新晟1 號私
募證券投資基金) 
N/A 
Longrising Xinhengsheng Private Securities Investment Fund (源乐晟新恒晟私募
证券投资基金) 
N/A 
 
To the best knowledge of CICC FT after making all reasonable enquiries, each of the CICC FT Ultimate Clients (Tibet Longrising) is an independent third party of CICC 
FT, CICCHKS, and the companies which are members of the same group of companies as CICCHKS. 
 
2. CICC FT and China International Capital Corporation Limited will enter into the OTC Swaps with each other and the Other CICC FT Ultimate Clients, pursuant to which 
CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed 
to the Other CICC FT Ultimate Clients, subject to customary fees and commissions. The OTC Swaps will be fully funded by the Other CICC FT Ultimate Clients. During 
the terms of the OTC Swaps, all economic returns of the Offer Shares subscribed by CICC FT will be passed to the Other CICC FT Ultimate Clients and all economic 
loss shall be borne by the Other CICC FT Ultimate Clients through the OTC Swaps, and CICC FT will not take part in any economic return or bear any economic loss 
in relation to the Offer Shares. The OTC Swaps are linked to the Offer Shares and the Other CICC FT Ultimate Clients may request CICC FT to redeem it at their own 
discretions, upon which CICC FT shall dispose of the Offer Shares and settle OTC Swaps in cash in accordance with the terms and conditions of the OTC Swap. Despite 
that CICC FT will hold the legal title of the Offer Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares during the terms of the OTC 
Swaps according to its internal policy. 
 
Details of the Other CICC FT Ultimate Clients are set out as below: 
 
Name of the Other CICC FT Ultimate Clients 
Ultimate beneficial owner(s) holding 30% or more interest (if any) 
Lingding Jiahe No. 2 Securities Private Investment Fund (凌頂嘉禾二號證券私募
投資基金) 
Zeng Yan (曾艷) 

<<<PAGE 23>>>
23 
 
Xiaoe Huisheng No. 1 Private Securities Investment Fund (小鱷慧昇1 號私募證券
投資基金) 
N/A 
Pinpoint Jinqu No. 1 Private Securities Investment Fund (保銀進取1 號私募證券
投資基金) 
N/A 
Pinpoint Long-Short Stable No. 2 Private Securities Investment Fund (保銀多空穩
健2 號私募證券投資基金) 
Wang Qiang (王強) 
Pinpoint Long-Short Stable No. 11 Private Securities Investment Fund (保銀多空
穩健1 號私募證券投資基金) 
Wang Qiang (王強) 
 
To the best knowledge of CICC FT after making all reasonable enquiries, each of the Other CICC FT Ultimate Clients is an independent third party of CICC FT, 
CICCHKS, and the companies which are members of the same group of companies as CICCHKS. 
 
3. Each of CMBI and CMS HK is a distributor of the Global Offering. Bosera AM intends to subscribe and hold the Offer Shares in its capacity as the discretionary fund 
manager on behalf of its sub-funds, which are all independent third parties. To the best knowledge of Bosera AM after due enquiry, each of the sub-funds and their 
respective ultimate beneficial owner holding 30% or more interest is an independent third party of Bosera AM, CMBI and CMS HK, and the companies which are 
members of the same group of CMBI and CMS HK. 
 
4. CSICM will enter into OTC total return swaps (TRS) with its end client (the “CSICM Ultimate Client”), pursuant to which CSICM will hold the allocated Offer Shares 
for the CSICM Ultimate Client on a non-discretionary basis, and all the economic exposure will be passed to the CSICM Ultimate Client through OTC total return swaps 
(TRS). The CSICM Ultimate Client is HY Capital Company Limited. Other than Xia Hui and Lu Ang, no single ultimate beneficial owner holds 30% or more interest in 
the CSICM Ultimate Client. To best of knowledge of CSICM and after making all reasonable enquiries, the CSICM Ultimate Client is an independent third party of 
CSICM, CSB and the companies which are members of the same group of CSB. 
 
5. China AMC HK will hold the Offer Shares in its capacity as the discretionary fund manager managing assets on behalf of its underlying clients or mandates, which are 
independent third parties. To the best knowledge of China AMC HK after due enquiry, each of the underlying clients or mandates of China AMC HK and their respective 
ultimate beneficial owner holding 30% or more interest is an independent third party of China AMC HK, CSB and the companies which are members of the same group 
of CSB. 
 
6. CITICS AM will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds (the “Funds”) on behalf of their respective investors. To the 
best knowledge of CITICS AM, each of the Funds above is an independent third party of CITICS AM, CSB and the companies which are members of the same group of 
CSB. 
 
7. ICBC UBS will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their investors (the “ICBC UBS Ultimate 
Clients”), each of which is an independent third party. None of the ICBC UBS Ultimate Clients holds more than 30% ultimate beneficial interest in the relevant funds. 
To the best of knowledge of ICBC UBS, each of the ICBC UBS Ultimate Clients is an independent party of ICBC UBS, UBS AG and the companies which are members 
of the same group of UBS AG. 
 

<<<PAGE 24>>>
24 
 
8. UBS AM Singapore will hold the beneficial interests of the Offer Shares on a discretionary basis for and on behalf of the underlying clients. To the best knowledge of 
UBS AM Singapore, each of the underlying clients is an independent third party of UBS AM Singapore, UBS AG and the companies which are members of the same 
group of UBS AG. 
 
9. PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public offerings (“IPOs”) in Hong Kong. However, PRC investors 
are permitted to invest in products issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. In connection with 
such products, the licensed domestic securities firms, through their Hong Kong affiliates, may participate in Hong Kong IPOs either as placees or cornerstone investors 
(the “Cross-border Derivatives Trading Regime”). 
 
Huatai Securities Co., Ltd. (“Huatai Securities”), the shares of which are listed on both the Shanghai Stock Exchange (stock code: 601688) and the Stock Exchange 
(stock code: 6886), is one of the domestic securities firms licensed to undertake cross-border derivatives trading activities. Huatai Securities entered into an ISDA 
agreement (the “ISDA Agreement”) with its indirectly wholly-owned subsidiary, HTCI to set out the principal terms of any future total return swap between Huatai 
Securities and HTCI. 
 
HTFH is a distributor in connection with the Global Offering. Pursuant to the ISDA Agreement, HTCI, which intends to participate in the Global Offering as a placee, 
will hold the beneficial interest of the Offer Shares on a non-discretionary basis as the single underlying holder under a back-to-back total return swap (the “Back-to-
back TRS”) to be entered by HTCI in connection with a Client TRS (as defined below) placed by and fully funded (i.e. with no financing provided by HTCI) by the 
Huatai Ultimate Clients (as defined below), by which, HTCI will, subject to customary fees and commissions, pass the full economic exposure of the Offer Shares 
ultimately to the Huatai Ultimate Clients, which in effect, HTCI will hold the beneficial interest of the Offer Shares on behalf of the Huatai Ultimate Clients. HTFH and 
HTCI are indirectly wholly-owned subsidiaries of Huatai Securities. Accordingly, HTCI is considered as a “connected client” of HTFH pursuant to paragraph 1B(7) of 
the Placing Guidelines. 
 
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the “Huatai Ultimate Clients”) cannot directly subscribe for the Offer Shares but may 
invest in derivative products issued by domestic securities firms licenced to undertake cross-border derivatives trading activities, such as Huatai Securities, with the Offer 
Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, each of the Huatai Ultimate Clients, through its investment manager, will place a 
total return swap order (the “Client TRS”) with Huatai Securities in connection with the Company’s IPO and Huatai Securities will place a Back-to-back TRS order to 
HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the Back-to-back TRS, HTCI participates in the Company’s IPO and subscribes the 
Offer Shares through placing order with HTFH during the International Offering. 
 
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in connection with the Client TRS order placed by the Huatai Ultimate 
Clients. Pursuant to the terms of the contracts of the Back-to-back TRS and the Client TRS, during the tenor of the Back-to-back TRS and the Client TRS, subject to 
customary fees and commissions, all economic returns of the Offer Shares will be ultimately passed to the Huatai Ultimate Clients through the Back-to-back TRS and 
the Client TRS and all economic loss shall be ultimately borne by the Huatai Ultimate Clients. HTCI will not take any economic return or bear any economic loss in 
relation to the Offer Shares. 
 
Investment in the Back-to-back TRS and the Client TRS is similar to the investment in a qualified domestic institutional investor fund (“QDII”) in the way that the Huatai 
Ultimate Clients would reap all the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through the exchange rate exposure on both 
the notional value of the investment and the profit and loss of the investment. In contrast, the profit and loss of the Back-to-back TRS and the Client TRS factor into 

<<<PAGE 25>>>
25 
 
account the fluctuation in RMB exchange rate upon termination of the Client TRS by converting the profit and loss using the current exchange rate at the time of 
termination. As such, the Huatai Ultimate Clients would bear the exchange rate exposure of the profit and loss on settlement date. 
 
The Huatai Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time from the issue date of the Client TRS which should be on or 
after the date on which the Offer Shares are listed on the Stock Exchange at their own discretion. Upon the termination upon maturity or early termination of the Client 
TRS by the Huatai Ultimate Clients, HTCI will dispose the Offer Shares on the secondary market and the Huatai Ultimate Clients will receive a final settlement amount 
in cash in accordance with the terms and conditions of the Back-to-back TRS and the Client TRS which should have taken into account all the economic returns or 
economic loss in relation to the Offer Shares. If upon the maturity of the Client TRS, the Huatai Ultimate Clients intend to extend the investment period, subject to further 
agreement between Huatai Securities and the relevant Huatai Ultimate Clients, the term of the Client TRS could be extended by way of a new issuance or a tenor extension. 
Accordingly, Huatai Securities will extend the term of the Back-to-back TRS by way of a new issuance or a tenor extension. 
 
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through the economic exposure to the Huatai Ultimate Clients, 
each being an onshore client who places a Client TRS order with Huatai Securities in connection with the IPO of the Company. HTCI will not exercise the voting right 
of the Offer Shares during the tenor of the Back-to-back TRS. 
 
During the life of the Client TRS and Back-to-back TRS, HTCI may continue to hold the Offer Shares in its custodian account, or to hold some or all of the Offer Shares 
in a prime brokerage account for stock borrowing purposes, where HTCI will lend out its holding of underlying Offer Shares in the form of stock borrowing loans 
consistent with market practice to lower its finance costs, provided that HTCI has the ability to call back the Offer Shares on loan at any time in order to satisfy its 
obligations under the Back-to-back TRS to ensure the economic interests are ultimately passed to the Huatai Ultimate Clients. 
 
Details of the Huatai Ultimate Clients are set out as below: 
 
Name of the Other CICC FT Ultimate Clients 
Ultimate beneficial owner(s) holding 30% or more interest (if any) 
Yuanfeng Stable Private Securities Investment Fund (源峰穩健私募證券投資基
金) 
N/A 
Yuanfeng Hongyu Private Securities Investment Fund (源峰泓聿私募證券投資基
金) 
Zhou Yong (周勇) 
Yuanfeng Value Private Securities Investment Fund (源峰價值私募證券投資基金) 
N/A 
Zhonghe Capital Cultivation No. 8 Private Securities Investment Fund (中和資本耕
耘8 號私募證券投資基金) 
Zhang Jingting (張敬庭) 
Greenwoods Harvest No. 2 Fund (景林豐收2 號基金) 
N/A 
Greenwoods Harvest No. 3 Private Fund (景林豐收3 號私募基金) 
N/A 
Greenwoods Harvest No. 6 Private Securities Investment Fund (景林豐收6 號私募
證券投資基金) 
N/A 

<<<PAGE 26>>>
26 
 
Greenwoods Jingtai Harvest Private Securities Investment Fund (景林景泰豐收私
募證券投資基金) 
N/A 
Greenwoods Shangyuan Private Securities Investment Fund (景林上元私募證券投
資基金) 
Lin Yanlei (林燕蕾) 
Shengquan Hengyuan Multi-Strategy Quantitative Hedge Fund No. 1 (盛泉恆元多
策略量化對沖1 號基金) 
N/A 
Shengquan Hengyuan Quantitative Arbitrage Specialised No. 48 Private Securities 
Investment Fund (盛泉恆元量化套利專項48 號私募證券投資基金) 
N/A 
Shengquan Hengyuan Multi-Strategy Vision No. 19 Private Securities Investment 
Fund (盛泉恆元多策略遠見19 號私募證券投資基金) 
N/A 
Shengquan Hengyuan Flexible Allocation Specialised No. 2 Private Securities 
Investment Fund (盛泉恆元靈活配置專項2 號私募證券投資基金) 
N/A 
Shengquan Hengyuan Quantitative Arbitrage Specialised No. 5 Private Securities 
Investment Fund (盛泉恆元量化套利專項5 號私募證券投資基金) 
N/A 
Shengquan Hengyuan Quantitative Arbitrage No. 1 Specialised Private Securities 
Investment Fund (盛泉恆元量化套利1 號專項私募證券投資基金) 
N/A 
Shengquan Hengyuan Quantitative Arbitrage Specialised No. 46 Private Securities 
Investment Fund (盛泉恆元量化套利專項46 號私募證券投資基金) 
N/A 
Shengquan Hengyuan Quantitative Arbitrage Specialised No. 29 Private Securities 
Investment Fund (盛泉恆元量化套利專項29 號私募證券投資基金) 
N/A 
Shengquan Hengyuan Quantitative Arbitrage Specialised No. 84 Private Securities 
Investment Fund (盛泉恆元量化套利專項84 號私募證券投資基金) 
N/A 
Tongyi Global Value No. 2 Private Securities Investment Fund (通怡全球價值2 號
私募證券投資基金) 
Liu Wei (劉偉) 
Tongyi Yuxin No. 2 Private Securities Investment Fund (通怡裕鑫2 號私募證券
投資基金) 
Huang Shilin (黃世霖) 
Tongyi Anxin No. 2 Private Securities Investment Fund (通怡安鑫2 號私募證券
投資基金) 
Huang Shilin (黃世霖) 
 
To the best of the knowledge of HTCI and after making all reasonable enquiries, each of the Huatai Ultimate Clients is an independent third party of (i) the Company, 
the connected person or the associates thereof, and (ii) HTCI, HTFH and the companies which are members of the same group of HTCI. 

<<<PAGE 27>>>
27 
 
DISCLAIMERS 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong 
Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement. 
This announcement is not for release, publication or distribution, directly or indirectly, in or into the 
United States (including its territories and possessions, any state of the United States and the District 
of Columbia or any other jurisdiction where such distribution is prohibited by laws). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe 
for securities in the United States or in any other jurisdictions. The securities mentioned herein have 
not been, and will not be, registered under the United States Securities Act of 1933 as amended from 
time to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the 
United States. The securities may not be offered, sold, pledged or otherwise transferred within the 
United States except pursuant to an exemption from the registration requirements of the U.S. Securities 
Act and in compliance with any applicable state securities laws. The Offer Shares are being offered 
and sold solely (a) to qualified institutional buyers as defined in Rule 144A under the U.S. Securities 
Act pursuant to Rule 144A or another available exemption from registration under the U.S. Securities 
Act and (2) outside the United States in offshore transactions in reliance on Regulation S under the 
U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer to 
acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated January 29, 2026 issued by Shenzhen Han’s CNC 
Technology Co., Ltd. for detailed information about the Global Offering described below before 
deciding whether or not to invest in the Offer Shares thereby being offered.
*Potential investors of the Offer Shares should note that the Sole Sponsor and the Sponsor-Overall 
Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate 
their obligations under the Hong Kong Underwriting Agreement with immediate effect upon the 
occurrence of any of the events set out in the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently 
expected to be on February 6, 2026).
 
 
 

<<<PAGE 28>>>
28 
 
PUBLIC FLOAT AND FREE FLOAT 
Immediately after the completion of the Global Offering (before any exercise of the Over-allotment 
Option), the total number of the H Shares expected to be held by the public represents approximately 
10.60% of the total issued share capital of the Company, which is higher than the prescribed percentage 
of H Shares required to be held in public hands of 10% under Rule 19A.13A(2)(a) of the Listing Rules, 
thereby satisfying Rule 8.08(1) (as amended and replaced by Rule 19A.13A) of the Listing Rules. 
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the Listing 
Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be counted 
towards the free float of the H Shares of the Company at the time of Listing. Based on the final Offer 
Price of HK$95.80 per H Share, the Company confirmed that it complies with the free float 
requirement under Rule 19A.13C(2)(b) of the Listing Rules. 
The Directors confirm that, immediately following completion of the Global Offering (before any 
exercise of the Over-allotment Option): (i) the Shares will be held by at least 300 Shareholders at the 
time of Listing, in compliance with Rule 8.08(2) of the Listing Rules; (ii) the three largest public 
Shareholders will not hold more than 50% of the H Shares held in public hands at the time of Listing, 
in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; (iii) no placee will, individually, be 
placed more than 10% of the enlarged issued share capital of the Company immediately after the 
Global Offering; and (iv) there will not be any new substantial Shareholder (as defined in the Listing 
Rules) immediately after the Global Offering. 
COMMENCEMENT OF DEALINGS 
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, February 6, 
2026 (Hong Kong time), provided that the Global Offering has become unconditional and the right of 
termination described in the section headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has not been 
exercised. Investors who trade the H Shares on the basis of publicly available allocation details prior 
to the receipt of H Share certificates or prior to the H Share certificates becoming valid evidence of 
title do so entirely at their own risk. 
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Friday, February 
6, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange will 
commence at 9:00 a.m. on Friday, February 6, 2026 (Hong Kong time). The H Shares will be traded 
in board lots of 100 H Shares each, and the stock code of the H Shares will be 3200. 
By order of the Board
Shenzhen Han’s CNC Technology Co., Ltd.
Mr. Yang Chaohui 
Chairman of the Board and Executive Director
 
Hong Kong, February 5, 2026 
As of the date of this announcement, the Board comprises: (i) Mr. Yang Chaohui as an executive 
Director; (ii) Mr. Zhang Jianqun, Mr. Zhou Huiqiang, Mr. Du Yonggang and Ms. Huang Linting as 
non-executive Directors; (iii) Mr. Qiu Yunliang, Ms. Li Weiwei and Dr. Xin Guosheng as independent 
non-executive Directors; and (iv) Ms. Xia Liya as a proposed independent non-executive Director. 
