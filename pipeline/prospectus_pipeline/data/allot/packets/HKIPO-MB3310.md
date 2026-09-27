# 配发结果公告抽取任务：3310.HK Viewtrix Technology Co., Ltd - H Shares

- 公告：Announcement of Allotment Results
- 刊发时间（港交所元数据）：**26/05/2026 22:05**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0526/2026052601908.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3310.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities 
in the United States or in any other jurisdictions. The securities mentioned herein have not been, and will not be, 
registered under the United States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or 
securities law of any state or other jurisdiction of the United States. The securities may not be offered, sold, pledged 
or otherwise transferred within the United States except pursuant to an exemption from the registration requirements of 
the U.S. Securities Act and in compliance with any applicable state securities laws, or outside the United States unless 
in compliance with Regulation S under the U.S. Securities Act. There will be no public offer of securities in the United 
States.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus 
dated May 18, 2026 (the “Prospectus”) issued by Viewtrix Technology Co., Ltd (雲英谷科技股份有限公司) (the 
“Company”) for detailed information about the Global Offering described below before deciding whether or not to 
invest in the H Shares thereby being offered. Any investment decision in relation to the Offer Shares should be taken 
solely in reliance on the information in the Prospectus. The Company has not been and will not be registered under the 
U.S. Investment Company Act of 1940, as amended.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited, as 
stabilizing manager (the “Stabilizing Manager”) (or any person acting for it), on behalf of the Underwriters, may 
over-allocate or effect transactions with a view to stabilizing or supporting the market price of the H Shares at a 
level higher than that which might otherwise prevail for a limited period after the Listing Date. However, there is 
no obligation on the Stabilizing Manager (or any person acting for it) to conduct any such stabilizing action. Such 
stabilizing action, if taken, (a) will be conducted at the absolute discretion of the Stabilizing Manager (or any person 
acting for it) and in what the Stabilizing Manager reasonably regards as the best interest of the Company, (b) may 
be discontinued at any time and (c) is required to be brought to an end within 30 days after the last day for lodging 
applications under the Hong Kong Public Offering (which is Saturday, June 20, 2026). Such stabilizing action, if taken, 
may be effected in all jurisdictions where it is permissible to do so, in each case in compliance with all applicable 
laws, rules and regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W 
of the Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws 
of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Saturday, June 20, 2026). 
After this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of 
the H Shares, could fall.
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinators (for themselves and on behalf 
of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting — 
Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus 
at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Wednesday, 
May 27, 2026).

<<<PAGE 2>>>
2
Viewtrix Technology Co., Ltd
雲英谷科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the Global 
Offering
:
52,859,200 H Shares (subject to the Over-
allotment Option)
Number of Hong Kong Offer Shares
:
5,286,000 H Shares
Number of International Offer Shares
:
47,573,200 H Shares (subject to the Over-
allotment Option)
Offer Price
:
HK$20.81 per H Share plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
Stock Exchange trading fee of 0.00565% 
and AFRC transaction levy of 0.00015% 
(payable in full on application in Hong 
Kong dollars and subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock Code
:
3310
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators, 
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
 
3 
 
VIEWTRIX TECHNOLOGY CO., LTD / 雲英谷科技股份有限公司 
ANNOUNCEMENT OF ALLOTMENT RESULTS 
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same meanings 
as those defined in the prospectus dated May 18, 2026 (the “Prospectus”) issued by Viewtrix Technology 
Co., Ltd (雲英谷科技股份有限公司) (the “Company”). 
 
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could move 
substantially even with a small number of the H Shares traded and should exercise extreme caution 
when dealing in the H Shares. 
SUMMARY 
 
Company information 
Stock code  
3310 
Stock short name  
VIEWTRIX TECH 
Dealings commencement date 
May 27, 2026* 
*see note at the end of the announcement 
 
Price Information  
Offer Price 
HK$20.81 
 
Offer Shares and Share Capital 
Number of Offer Shares 
52,859,200 
Final Number of Offer Shares in Hong Kong Public Offering 5,286,000 
Final Number of Offer Shares in International Offering 
47,573,200 
Number of issued Shares upon Listing (before exercise of the 
Over-allotment Option) 
427,778,950 
 
Over-allocation 
No. of Offer Shares over-allocated 
7,928,800 
- 
International Offering 
7,928,800 
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases 
in the secondary market at prices that do not exceed the Offer Price or through deferred delivery or a 
combination of these means. In the event the Over-allotment Option is exercised, an announcement will 
be made on the Stock Exchange’s website.  
 
Proceeds   
Gross proceeds Note 
HK$1,100.00 million 
Less: Estimated listing expenses payable based on the 
Offer Price  
HK$80.93 million 
Net proceeds  
HK$1,019.07 million 
 
Note: Gross proceeds refer to the amount which the Company is entitled to receive. For details of the use 
of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis. 

<<<PAGE 4>>>
4 
 
 
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING 
 
No. of valid applications  
242,444 
No. of successful applications  
25,707 
Subscription level 
3,559.68 times 
Claw-back triggered  
N/A 
No. of Offer Shares initially available under the Hong Kong Public 
Offering  
5,286,000 
Final no. of Offer Shares under the Hong Kong Public Offering 
5,286,000 
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering 
10% 
 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.eipo.com.hk/eIPOAllotment 
to 
perform 
a 
search 
by 
identification 
number 
or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees. 
INTERNATIONAL OFFERING 
 
No. of placees 
72 
Subscription level 
7.05 times 
No. of Offer Shares initially available under the International 
Offering  
47,573,200 
Final no. of Offer Shares under the International Offering 
47,573,200 
% of Offer Shares under the International Offering to the Global 
Offering 
90% 
% of final no. of Offer Shares under the International Offering to 
the Global Offering (after over-allocation) 
91.3% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit H Shares in the International Offering to be placed to Digital Vista, a close associate of 
an existing Shareholder as a Cornerstone Investor; and (b) a consent under Chapter 4.15 of the Guide for New 
Listing Applicants to permit the Company to, among other things, allocate further H Shares to Digital Vista 
as a placee in the International Offering, (i) none of the Offer Shares subscribed by the placees and the public 
have been financed directly or indirectly by the Company, any of the Directors, chief executive of the Company, 
members of the Single Largest Shareholder Group, substantial Shareholders, existing Shareholders of the 
Company or any of its subsidiaries or their respective close associates; and (ii) none of the placees and the 
public who have purchased the Offer Shares are accustomed to taking instructions from the Company, any of 
the Directors, chief executive of the Company, members of the Single Largest Shareholder Group, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective close 
associates in relation to the acquisition, disposal, voting or other disposition of the H Shares registered in 
his/her/its name or otherwise held by him/her/it. 
The placees in the International Offering include the following: 
Cornerstone Investors 

<<<PAGE 5>>>
5 
 
 
Investor 
No. of Offer 
Shares 
allocated 
Approximate % of the 
Offer Shares (assuming 
the 
Over-allotment 
Option is not exercised) 
Approximate % of total 
issued share capital after the 
Global Offering (assuming 
the Over-allotment Option is 
not exercised) 
Existing 
Shareholders or 
their 
close 
associates Note 2 
Digital 
Vista Note1 
16,818,800 
31.82% 
3.93% 
Yes Note2 
SpreadCom 
1,874,000 
3.55% 
0.44% 
No 
Total 
18,692,800 
35.37% 
4.37% 
 
Notes: 
 
1. 
In addition to the Offer Shares subscribed for as a Cornerstone Investor, Digital Vista was allocated further Offer Shares as a 
placee in the International Offering. Please refer to the section headed “Allotment Results Details — International Offering — 
Allottees with Consents Obtained” in this announcement for details. Only the Offer Shares subscribed for as a Cornerstone Investor 
are subject to lock-up restrictions as indicated below. For details, please refer to the section headed “Lock-up Undertakings — 
Cornerstone Investors” in this announcement. 
 
2. 
As disclosed in the section headed “Waiver and Consent” in the Prospectus, solely for the purpose of the Global Offering, Digital 
Vista is considered to be a close associate of an existing Shareholder (i.e., Guangdong Province Semiconductor and Integrated 
Circuit Industry Investment Fund Partnership (L.P.) (廣東省半導體及集成電路產業投資基金合夥企業（有限合夥）) holding 
less than 5% voting rights of the Company, which is ultimately controlled by the People’s Government of Guangdong Province (廣
東省人民政府). For details of the prior consent under paragraph 1C(2) of the Placing Guidelines in relation to subscription of H 
Shares by a close associate of an existing Shareholder as a Cornerstone Investor, please refer to the section headed “Others/ 
Additional Information — Placing to a close associate of an existing Shareholder as a Cornerstone Investor” in this announcement. 
 
 

<<<PAGE 6>>>
6 
 
 
Allottees with Consents Obtained 
 
 
Investor 
No. of Offer 
Shares 
allocated 
% of the Offer 
Shares (assuming 
the Over-allotment 
Option 
is 
not 
exercised) 
% of total issued share 
capital after the Global 
Offering (assuming the 
Over-allotment Option 
is not exercised) 
Relationship 
Allottees with consent under paragraphs 16 and 18 of Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations of further H Shares to a Cornerstone Investor Note 1 
Digital Vista 
7,640,800 
14.46% 
1.79% 
Cornerstone 
Investor and close 
associate of an 
existing 
Shareholder 
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients Note 2 
E Fund Management 
Co, Ltd. (“E Fund”) 8,600 
0.02% 
0.002% 
Connected client as 
a placee 
E Fund Management 
(Hong Kong) Co, 
Ltd. (“E Fund HK”) 8,600 
0.02% 
0.002% 
Connected client as 
a placee 
CITIC Securities 
International Capital 
Management 
Limited (“CSI”) 
4,000 
0.008% 
0.0008% 
Connected client as 
a placee 
Haitong 
International Asset 
Management (HK) 
Limited (“Haitong 
AM”) 
400 
0.0008% 
0.00008% 
Connected client as 
a placee 
Notes: 
 
1. 
The number of Offer Shares allocated to the relevant investor listed in this subsection only represents the number of Offer Shares 
allocated to such investor as a placee in the International Offering. For allocations of Offer Shares to such investor as a 
Cornerstone Investor, please refer to the section headed “Allotment Results Details — International Offering — Cornerstone 
Investors” in this announcement. For details of the consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations of further H Shares to the relevant Cornerstone Investor, please refer to the section headed 
“Others / Additional Information — Allocations of Offer Shares to a Cornerstone Investor with a consent under Chapter 4.15 of 
the Guide for New Listing Applicants” in this announcement. Solely for the purpose of the allocation of further H Shares to Digital 
Vista as a placee in the International Offering, Digital Vista is considered to be a close associate of an existing Shareholder who 
is deemed as a “PRC governmental body” under the Listing Rules and the Guide for New Listing Applicants. 
 
2. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations to connected clients, please refer to the sections headed “Others / Additional Information — 
Placing to connected clients with a consent under paragraph 1C(1) of the Placing Guidelines” in this announcement. 
 
 
LOCK-UP UNDERTAKINGS  
Single Largest Shareholder Group 

<<<PAGE 7>>>
7 
 
Name Note 1 
Number 
and 
description 
of 
Shares held in 
the 
Company 
subject to lock-up 
undertakings 
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
Shenzhen 
Yishi 
36,204,584 
H 
Shares 
8.46% 
8.46% 
May 26, 2027 
Yisheng 
No. 1 
23,843,783 
H 
Shares 
5.57% 
5.57% 
May 26, 2027 
Yisheng 
No. 2 
12,636,372 
H 
Shares 
2.95% 
2.95% 
May 26, 2027 
Notes: 
 
1. 
For illustrative purposes only, this subsection lists only those members of the Single Largest Shareholder Group who hold 
Shares directly in the Company. Pursuant to Rule 10.07 of the Listing Rules, each member of the Single Largest Shareholder 
Group (namely, Dr, Gu Jing, Shenzhen Yishi, Yisheng No. 1 and Yisheng No. 2) has undertaken to the Stock Exchange and the 
Company that, except pursuant to the Global Offering (including the Over-allotment Option), it/he will not, and shall procure 
that the relevant registered holder(s) will not, without the prior written consent of the Stock Exchange or unless otherwise 
permitted under the Listing Rules, at any time in the period commencing on the date by reference to which disclosure of its/his 
shareholding is made in the Prospectus and ending on the date which is six months from the Listing Date, either directly or 
indirectly, dispose of, nor enter into any agreement to dispose of or otherwise create any options, rights, interests or 
encumbrances in respect of, any of the securities of the Company in respect of which it/he is shown by the Prospectus to be the 
beneficial owner. For further details, please refer to the section headed “Underwriting — Underwriting Arrangements and 
Expenses — Hong Kong Public Offering — Undertakings to the Stock Exchange pursuant to the Listing Rules — Undertakings 
by the Single Largest Shareholder Group” in the Prospectus. 
 
2. 
Upon completion of the Global Offering, 374,919,750 Unlisted Shares are converted into H Shares on a one-for-one basis. 
 
3. 
The expiry day of the lock-up period shown in the table above is pursuant to the PRC Company Law. In accordance with the 
relevant Listing Rule, the required lock-up for the six-month period ends on November 26, 2026. 
 
 
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
% of total Offer 
Shares 
after 
the 
Global 
Offering 
subject to lock-up 
undertakings 
(assuming the Over-
allotment Option is 
not exercised) 
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
Note 1 
Digital Vista 
16,818,800 H 
Shares 
31.82% 
3.93% 
November 
26, 2026  
SpreadCom 
1,874,000 H Shares 
3.55% 
0.44% 
November 
26, 2026  
Note: 
 
1. 
In accordance with the relevant cornerstone investment agreements, the required lock-up periods will end on November 26, 2026. The 
Cornerstone Investors will cease to be prohibited from disposing of or transferring the H Shares subscribed for pursuant to the relevant 
cornerstone investment agreements after the indicated date. 
 
 
Pre-IPO Investors 

<<<PAGE 8>>>
8 
 
Name 
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
Shares 
after 
the 
Global 
Offering 
subject 
to 
lock-up 
undertakings 
(assuming the Over-
allotment Option is 
not exercised)Note 1 
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
undertakings Note 2 
HSG 
23,718,425 
H 
Shares 
5.54% 
5.54% 
May 26, 2027 
QM119 
Limited 
21,314,190 
H 
Shares 
4.98% 
4.98% 
May 26, 2027 
Qiming 
Rongke 
3,758,239 
H 
Shares 
0.88% 
0.88% 
May 26, 2027 
Qiming 
Rongying 
2,623,075 
H 
Shares 
0.61% 
0.61% 
May 26, 2027 
Qicheng 
Zhiyuan 
18,343,755 
H 
Shares 
4.29% 
4.29% 
May 26, 2027 
Ningbo 
Yuhang 
14,668,811 
H 
Shares 
3.43% 
3.43% 
May 26, 2027 
Xiamen Zhiyi 
6,044,157 
H 
Shares 
1.41% 
1.41% 
May 26, 2027 
Nanshan 
Hongtai 
17,426,566 
H 
Shares 
4.07% 
4.07% 
May 26, 2027 
Hongtai Zhiyun 2,225,785 
H 
Shares 
0.52% 
0.52% 
May 26, 2027 
Xiaomi 
Changjiang 
15,820,663 
H 
Shares 
3.70% 
3.70% 
May 26, 2027 
Tianjin Jinmi 
1,742,655 
H 
Shares 
0.41% 
0.41% 
May 26, 2027 
Hubble 
Technology 
15,820,663 
H 
Shares 
3.70% 
3.70% 
May 26, 2027 
Boe 
Technology 
15,507,357 
H 
Shares 
3.63% 
3.63% 
May 26, 2027 
Qualcomm 
China 
8,870,853 
H 
Shares 
2.07% 
2.07% 
May 26, 2027 
Jiaxing Haiyun 
8,697,610 
H 
Shares 
2.03% 
2.03% 
May 26, 2027 
Hefei Tianze 
8,632,034 
H 
Shares 
2.02% 
2.02% 
May 26, 2027 
Jichuang 
Yuyuan 
8,537,163 
H 
Shares 
2.00% 
2.00% 
May 26, 2027 
Vertex Legacy 
7,805,897 
H 
Shares 
1.82% 
1.82% 
May 26, 2027 
Xiangfeng 
Phase II 
4,500,000 
H 
Shares 
1.05% 
1.05% 
May 26, 2027 
Xiamen Qilu 
7,103,825 
H 
Shares 
1.66% 
1.66% 
May 26, 2027 
CICC Pucheng 
2,324,928 
H 
Shares 
0.54% 
0.54% 
May 26, 2027 

<<<PAGE 9>>>
9 
 
Name 
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
Shares 
after 
the 
Global 
Offering 
subject 
to 
lock-up 
undertakings 
(assuming the Over-
allotment Option is 
not exercised)Note 1 
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
undertakings Note 2 
Nanshan 
Zhonghang 
6,805,346 
H 
Shares 
1.59% 
1.59% 
May 26, 2027 
Shenzhen 
Pingshan 
400,168 
H 
Shares 
0.09% 
0.09% 
May 26, 2027 
White 
Cloud 
Valley 
6,407,569 
H 
Shares 
1.50% 
1.50% 
May 26, 2027 
Linghui 
Cornerstone 
4,848,488 
H 
Shares 
1.13% 
1.13% 
May 26, 2027 
Hangzhou 
Kunwei 
4,164,147 
H 
Shares 
0.97% 
0.97% 
May 26, 2027 
Shanghai 
Suishuo 
4,125,388 
H 
Shares 
0.96% 
0.96% 
May 26, 2027 
Yueke 
Xintai 
No. 25 
3,258,109 
H 
Shares 
0.76% 
0.76% 
May 26, 2027 
Yueke 
Xintai 
Industry 
1,313,762 
H 
Shares 
0.31% 
0.31% 
May 26, 2027 
Haitong 
New 
Energy 
3,188,193 
H 
Shares 
0.75% 
0.75% 
May 26, 2027 
Guokai 
Technology 
2,791,877 
H 
Shares 
0.65% 
0.65% 
May 26, 2027 
Semiconductor 
and IC Fund 
2,700,000 
H 
Shares 
0.63% 
0.63% 
May 26, 2027 
Wofu Ruixin 
2,582,812 
H 
Shares 
0.60% 
0.60% 
May 26, 2027 
Ceyuan 
Guangyi 
2,489,700 
H 
Shares 
0.58% 
0.58% 
May 26, 2027 
Shanghai 
Fuzhishuo 
2,412,907 
H 
Shares 
0.56% 
0.56% 
May 26, 2027 
Yu Huihui 
616,632 
H 
Shares 
0.14% 
0.14% 
May 26, 2027 
Bangsheng 
Yingxin 
2,366,646 
H 
Shares 
0.55% 
0.55% 
May 26, 2027 
Houwang 
Ruilian 
2,295,000 
H 
Shares 
0.54% 
0.54% 
May 26, 2027 
Zhicheng 
Shuzhi 
2,181,393 
H 
Shares 
0.51% 
0.51% 
May 26, 2027 
Shenzhen 
High-Tech 
Investment 
2,181,393 
H 
Shares 
0.51% 
0.51% 
May 26, 2027 
Shengao 
Investment 
1,090,696 
H 
Shares 
0.25% 
0.25% 
May 26, 2027 

<<<PAGE 10>>>
10 
 
Name 
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
Shares 
after 
the 
Global 
Offering 
subject 
to 
lock-up 
undertakings 
(assuming the Over-
allotment Option is 
not exercised)Note 1 
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
undertakings Note 2 
Shenzhen 
High-Tech 
Fuhai 
545,348 
H 
Shares 
0.13% 
0.13% 
May 26, 2027 
Jiaxing Xihao 
1,833,336 
H 
Shares 
0.43% 
0.43% 
May 26, 2027 
Qingyue 
Optoelectronics 
1,742,655 
H 
Shares 
0.41% 
0.41% 
May 26, 2027 
Guangdong 
Changtuoshi 
1,608,605 
H 
Shares 
0.38% 
0.38% 
May 26, 2027 
Wanchuang 
Shidai 
1,562,344 
H 
Shares 
0.37% 
0.37% 
May 26, 2027 
Nanjing Jintai 
1,118,664 
H 
Shares 
0.26% 
0.26% 
May 26, 2027 
Yuxin Taojin 
900,000 
H 
Shares 
0.21% 
0.21% 
May 26, 2027 
Shenzhen 
Addition No. 2 
545,348 
H 
Shares 
0.13% 
0.13% 
May 26, 2027 
Dinghong 
Growth 
450,000 
H 
Shares 
0.11% 
0.11% 
May 26, 2027 
Huahui Dianke 
450,000 
H 
Shares 
0.11% 
0.11% 
May 26, 2027 
Notes: 
 
1. 
Upon completion of the Global Offering, 374,919,750 Unlisted Shares are converted into H Shares on a one-for-one basis. 
 
2. 
The expiry day of the lock-up period shown in the table above is pursuant to the PRC Company Law. 
 
 
Existing Shareholders other than the Single Largest Shareholder Group and the Pre-IPO Investors as 
identified in the section headed “History, Development and Corporate Structure” in the Prospectus 
Name 
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
Shares 
after 
the 
Global 
Offering 
subject 
to 
lock-up 
undertakings 
(assuming the Over-
allotment Option is 
not exercised)Note 1 
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
undertakings Note 2 
Shenzhen 
Yizhen 
15,910,023 
H 
Shares 
3.72% 
3.72% 
May 26, 2027 
Beijing 
Chengda 
1,861,811 
H 
Shares 
0.44% 
0.44% 
May 26, 2027 
Notes: 
 

<<<PAGE 11>>>
11 
 
Name 
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
Shares 
after 
the 
Global 
Offering 
subject 
to 
lock-up 
undertakings 
(assuming the Over-
allotment Option is 
not exercised)Note 1 
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
undertakings Note 2 
1. 
Upon completion of the Global Offering, 374,919,750 Unlisted Shares are converted into H Shares on a one-for-one basis. 
 
2. 
The expiry day of the lock-up period shown in the table above is pursuant to the PRC Company Law. 
 
 
 

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
Option is 
fully 
exercised) 
 
 
 
 
 
 
 
 
 
Top 1 
24,459,600 
51.41% 
44.07% 
46.27% 
40.24% 
27,159,600 
6.35% 
6.23% 
Top 5 
40,592,200 
85.33% 
73.14% 
76.79% 
66.78% 
43,292,200 
10.12% 
9.94% 
Top 10 
49,566,200 
104.19% 
89.31% 
93.77% 
81.54% 
52,266,200 
12.22% 
12.00% 
Top 25 
55,432,400 
116.52% 
99.87% 
104.87% 
91.19% 
58,132,400 
13.59% 
13.34% 
 
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
- 
0.00% 
0.00% 
0.00% 
0.00% 
72,684,739 
16.99% 
16.68% 
Top 5 
24,459,600 
51.41% 
44.07% 
46.27% 
40.24% 
190,314,541 
44.49% 
43.68% 
Top 10 
24,459,600 
51.41% 
44.07% 
46.27% 
40.24% 
274,768,253 
64.23% 
63.06% 
Top 25 
35,212,200 
74.02% 
63.44% 
66.62% 
57.93% 
379,314,970 
88.67% 
87.06% 
 
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
as % of 
total Offer 
Shares 
(assuming 
no exercise 
of the Over- 
allotment 
Option) 
Allotment 
as % of 
total Offer 
Shares 
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
- 
0.00% 
0.00% 
0.00% 
0.00% 
72,684,739 
72,684,739 
16.99% 
16.68% 
Top 5 
24,459,600 
51.41% 
44.07% 
46.27% 
40.24% 190,314,541 190,314,541 
44.49% 
43.68% 
Top 10 
24,459,600 
51.41% 
44.07% 
46.27% 
40.24% 274,768,253 274,768,253 
64.23% 
63.06% 
Top 25 
35,212,200 
74.02% 
63.44% 
66.62% 
57.93% 379,314,970 379,314,970 
88.67% 
87.06% 
 
Notes: 
* Ranking of Shareholders is based on the number of Shares held by the Shareholders upon Listing. 
 

<<<PAGE 15>>>
15 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below: 
NO. OF H 
SHARES 
APPLIED 
FOR 
NO. 
OF 
VALID 
APPLICATIONS 
BASIS OF ALLOTMENT / BALLOT 
APPROXIMATE 
PERCENTAGE 
ALLOTTED 
OF 
THE TOTAL NO. 
OF 
H 
SHARES 
APPLIED FOR 
POOL A 
200 
65,446 1,963 out of 65,446 to receive 200 Shares 
3.00% 
400 
30,136 913 out of 30,136 to receive 200 Shares 
1.51% 
600 
7,223 221 out of 7,223 to receive 200 Shares 
1.02% 
800 
4,798 148 out of 4,798 to receive 200 Shares 
0.77% 
1,000 
6,323 197 out of 6,323 to receive 200 Shares 
0.62% 
1,200 
2,972 93 out of 2,972 to receive 200 Shares 
0.52% 
1,400 
2,190 69 out of 2,190 to receive 200 Shares 
0.45% 
1,600 
2,195 70 out of 2,195 to receive 200 Shares 
0.40% 
1,800 
3,217 104 out of 3,217 to receive 200 Shares 
0.36% 
2,000 
17,346 564 out of 17,346 to receive 200 Shares 
0.33% 
3,000 
5,182 176 out of 5,182 to receive 200 Shares 
0.23% 
4,000 
5,625 199 out of 5,625 to receive 200 Shares 
0.18% 
5,000 
3,654 134 out of 3,654 to receive 200 Shares 
0.15% 
6,000 
2,437 93 out of 2,437 to receive 200 Shares 
0.13% 
7,000 
1,781 70 out of 1,781 to receive 200 Shares 
0.11% 
8,000 
1,753 72 out of 1,753 to receive 200 Shares 
0.10% 
9,000 
2,513 106 out of 2,513 to receive 200 Shares 
0.09% 
10,000 
9,083 398 out of 9,083 to receive 200 Shares 
0.09% 
20,000 
6,544 378 out of 6,544 to receive 200 Shares 
0.06% 
30,000 
4,075 293 out of 4,075 to receive 200 Shares 
0.05% 
40,000 
3,657 314 out of 3,657 to receive 200 Shares 
0.04% 
50,000 
3,342 334 out of 3,342 to receive 200 Shares 
0.04% 
60,000 
2,399 273 out of 2,399 to receive 200 Shares 
0.04% 
70,000 
2,052 263 out of 2,052 to receive 200 Shares 
0.04% 
80,000 
1,938 275 out of 1,938 to receive 200 Shares 
0.04% 
90,000 
1,593 249 out of 1,593 to receive 200 Shares 
0.03% 
100,000 
11,284 1,920 out of 11,284 to receive 200 Shares 
0.03% 
200,000 
10,705 3,326 out of 10,705 to receive 200 Shares 
0.03% 
Total 
221,463 
Total number of Pool A successful 
applicants: 13,215 
POOL B 
300,000 
8,705 3,954 out of 8,705 to receive 200 Shares 
0.03% 

<<<PAGE 16>>>
16 
 
400,000 
2,530 1,262 out of 2,530 to receive 200 Shares 
0.02% 
500,000 
1,961 1,069 out of 1,961 to receive 200 Shares 
0.02% 
600,000 
1,300 767 out of 1,300 to receive 200 Shares 
0.02% 
700,000 
955 606 out of 955 to receive 200 Shares 
0.02% 
800,000 
858 584 out of 858 to receive 200 Shares 
0.02% 
900,000 
585 423 out of 585 to receive 200 Shares 
0.02% 
1,000,000 
1,167 907 out of 1,167 to receive 200 Shares 
0.02% 
1,250,000 
645 200 Shares 
0.02% 
1,500,000 
460 200 Shares plus 9 out of 460 to receive 
additional 200 Shares 
0.01% 
1,750,000 
708 200 Shares plus 97 out of 708 to receive 
additional 200 Shares 
0.01% 
2,643,000 
1,107 200 Shares plus 617 out of 1,107 to receive 
additional 200 Shares 
0.01% 
Total 
20,981 
Total number of Pool B successful 
applicants: 12,492 
 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors confirm that, except for the Listing Rules in respect of which consent has been obtained, 
the Company has complied with the Listing Rules and guidance materials in relation to the placing, 
allotment and listing of the H Shares.  
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the 
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by 
them is the same as the final Offer Price in addition to any brokerage, AFRC transaction levy, SFC 
transaction levy and Stock Exchange trading fee payable. 
OTHERS / ADDITIONAL INFORMATION 
 
Placing to a close associate of an existing Shareholder as a Cornerstone Investor 
 
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules to permit Digital Vista to participate in the Global Offering 
as a Cornerstone Investor. For details, see the sections headed “Waivers and Consent – Consent under Paragraph 
1C(2) of Appendix F1 to the Listing Rules in respect of Subscription of Offer Shares by a close associate of an 
existing Shareholder as a Cornerstone Investor” and “Cornerstone Investments” in the Prospectus.  
 
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted by the 
Stock Exchange. 
 
For details of further allocations of Offer Shares to such Cornerstone Investor as a placee in the International 
Offering, please refer to the section headed “Allotment Results Details – International Offering – Allottees with 
Consents Obtained” in this announcement. 
 
Allocations of Offer Shares to a Cornerstone Investor with a consent under Chapter 4.15 of the 
Guide for New Listing Applicants 
 
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 of 
the Guide for New Listing Applicants to permit the Company to allocate further Offer Shares in the 

<<<PAGE 17>>>
17 
 
International Offering to a Cornerstone Investor as a placee, subject to the following conditions (the 
“Allocation to Size-based Exemption Participant”): 
 
(a) the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion; 
 
(b)  the Allocation to Size-based Exemption Participant will not affect the Company’s ability to 
satisfy its public float requirement under Rule 8.08(1) (as amended and replaced by Rule 
19A.13A) of the Listing Rules; 
 
(c) each Director and chief executive confirms that no securities have been allocated to them or their 
respective close associates under this exemption; and 
 
(d) details of the allocation to such Cornerstone Investor under this exemption will be disclosed in 
this announcement. 
 
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted 
by the Stock Exchange. 
 
For details of the allocations of Offer Shares to Cornerstone Investors, please refer to the section 
headed “Allotment Results Details – International Offering – Allottees with Consents Obtained” in 
this announcement. 
 
Placing to connected clients with a consent under paragraph 1C(1) of the Placing Guidelines 
 
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines as placees. Please refer to the section headed 
“Allotment Results Details — International Offering — Allottees with Consents Obtained” in this 
announcement for details. The Company has applied to the Stock Exchange for, and the Stock 
Exchange has granted, a consent under paragraph 1C(1) of the Placing Guidelines to permit the 
Company to allocate such Offer Shares in the International Offering to the connected clients as placees. 
The allocations of Offer Shares to such connected clients are in compliance with all the conditions 
under the consent granted by the Stock Exchange. Details of the placement to connected clients as 
placees are set out below: 

<<<PAGE 18>>>
18 
 
 
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
not authorized 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
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
Number of 
Offer Shares 
to be 
allocated to 
the 
Connected 
Client 
Approximate 
percentage of total 
number of Offer 
Shares under the 
Global Offering 
(assuming no exercise 
of the Over-allotment 
Option) 
Approximate 
percentage of total 
issued share capital 
immediately following 
completion of the 
Global Offering 
(assuming no exercise 
of the Over-allotment 
Option) 
1. 
GF Securities 
(Hong Kong) 
Brokerage 
Limited 
(“GFSHK”) 
E Fund Note 1 
E Fund is a 
member of the 
same group of 
companies as 
GFSHK. 
No 
Discretionary 
basis 
8,600 
0.02% 
0.002% 
2. 
GFSHK 
E Fund HK 
Note 2 
E Fund HK is a 
member of the 
same group of 
companies as 
GFSHK. 
No 
Discretionary 
basis 
8,600 
0.02% 
0.002% 
3. 
CLSA 
CSI Note 3 
CSI is a member 
of the same 
group of 
companies as 
CLSA. 
No 
Non-
discretionary 
basis 
4,000 
0.008% 
0.0008% 
4. 
Guotai Junan 
Securities 
(Hong Kong) 
Limited 
Haitong AM 
Note 4 
Haitong AM is a 
member of the 
same group of 
companies as 
GTJA Securities 
No 
Discretionary 
basis 
400 
0.0008% 
0.00008% 

<<<PAGE 19>>>
19 
 
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
not authorized 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
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
Number of 
Offer Shares 
to be 
allocated to 
the 
Connected 
Client 
Approximate 
percentage of total 
number of Offer 
Shares under the 
Global Offering 
(assuming no exercise 
of the Over-allotment 
Option) 
Approximate 
percentage of total 
issued share capital 
immediately following 
completion of the 
Global Offering 
(assuming no exercise 
of the Over-allotment 
Option) 
(“GTJA 
Securities”) 
 
 
__________ 
 
Notes: 
1. E Fund will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of its investors, each of which is, to the 
best knowledge of E Fund, an independent third party of E Fund, GFSHK and the companies which are members of the same group of GFSHK. 
 
2. E Fund HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of its investors, each of which is, to 
the best knowledge of E Fund HK, an independent third party of E Fund HK, GFSHK and the companies which are members of the same group of GFSHK. 
 
3. CSI proposes to subscribe for and hold the Offer Shares as a placee under the International Offering on behalf of the ultimate client of CSI (the “CSI 
Ultimate Client”) on a non-discretionary basis, pursuant to which CSI will act as the single counterparty of a back-to-back total return swap transaction 
(the “CSI Back-to-back TRS”) to be entered into by it in connection with a total return swap order (the “CSI Client TRS”) placed and fully funded by the 
CSI Ultimate Client, by which CSI will pass the full economic exposure of the Offer Shares placed to CSI to the CSI Ultimate Client. As confirmed by CSI 
and CLSA, CSI will hold the legal title and beneficial interest in the Offer Shares, but will contractually agree to pass on the full economic exposure and 
return of the Offer Shares to the CSI Ultimate Client, on a non-discretionary basis. The CSI Ultimate Client may exercise its early termination rights to 
terminate the CSI Client TRS at any time from the trade date of the CSI Client TRS which should be on or after the date on which the Offer Shares are 
listed on the Stock Exchange. Upon the final maturity or termination of the CSI Client TRS by the CSI Ultimate Client, CSI will dispose of the Offer Shares 
on the secondary market and the CSI Ultimate Client will receive a final termination amount of the CSI Back-to-back TRS which will have taken into 

<<<PAGE 20>>>
20 
 
account all the economic returns or economic loss in relation to the Offer Shares and the fixed amount of transaction fees of the CSI Back-to-back TRS and 
the CSI Client TRS. Due to its internal policy, CSI will not exercise the voting right of the Offer Shares during the terms of the CSI Back-to-back TRS. 
 
Details of the CSI Ultimate Client are set out as below: 
 
Name of the CSI Ultimate Client 
Ultimate beneficial owner(s) holding 30% or more interest (if any) 
HY Capital Company Limited 
Xia Hui and Lu Ang 
 
To the best of knowledge of CSI after making all reasonable enquiries, the CSI Ultimate Client is an independent third party of CSI, CLSA and the 
companies which are members of the same group of CLSA. 
 
4. Haitong AM will hold the Offer Shares in its capacity as the discretionary fund manager managing the fund on behalf of its investors (the “Haitong AM 
Ultimate Client”), whose details are as follows: 
 
Name of the Haitong AM Ultimate Client 
Ultimate beneficial owner(s) holding 30% or more interest (if any) 
Haitong Opportunity Fund II S.P., a segregated portfolio of Haitong 
Global investment SPC lV 
N/A 
 
To the best of knowledge of Haitong AM after making all reasonable enquiries, the Haitong AM Ultimate Client is an independent third party of Haitong 
AM, GTJA Securities and the companies which are members of the same group of GTJA Securities. 
 

<<<PAGE 21>>>
21 
 
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
and sold solely outside the United States in offshore transactions in reliance on Regulation S under 
the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to 
acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated May 18, 2026 issued by Viewtrix Technology Co., Ltd (雲
英谷科技股份有限公司) for detailed information about the Global Offering described below before 
deciding whether or not to invest in the Offer Shares thereby being offered. 
*Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to 
terminate their obligations under the Hong Kong Underwriting Agreement with immediate effect upon 
the occurrence of any of the events set out in the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently 
expected to be on May 27, 2026). 
 
 
 

<<<PAGE 22>>>
22 
 
PUBLIC FLOAT AND FREE FLOAT 
Pursuant to Rule 8.08(1) (as amended and replaced by Rule 19A.13A) of the Listing Rules, assuming 
that the Over-Allotment Option is not exercised, based on the Offer Price of HK$20.81 per H Share, 
the market capitalization of the Company’s Shares upon the Listing is expected to be HK$8,902 
million and the minimum prescribed public float percentage applicable to the Company’s Shares is 
16.85%. 
So far as the Directors are aware and to the best knowledge of the Directors, following the conversion 
of the Unlisted Shares into H Shares and upon completion of the Global Offering (assuming that the 
Over-allotment Option is not exercised), an aggregate of 72,684,739 H Shares held by Shenzhen Yishi, 
Yisheng No. 1 and Yisheng No. 2, which are expected to be core connected persons (as defined under 
the Listing Rules) of the Company after the Listing will not be counted towards the public float. 
Except as stated above, all the 302,235,011 H Shares held by other Shareholders and the 52,859,200 
H Shares to be issued under the Global Offering will be counted towards the public float for the purpose 
of Rule 8.08 of the Listing Rules, representing approximately 83.01% of the enlarged share capital of 
the Company (assuming that the Over-allotment Option is not exercised) after the Listing, thereby 
satisfying Rule 8.08(1) (as amended and replaced by Rule 19A.13A) of the Listing Rules. 
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the Listing 
Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be counted 
towards the free float of the H Shares of the Company at the time of Listing. Based on an Offer Price 
of HK$20.81 per H Share, the Company will satisfy the free float requirement under Rule 8.08A (as 
amended and replaced by Rule 19A.13C) of the Listing Rules 
The Directors confirm that, immediately following completion of the Global Offering (before any 
exercise of the Over-allotment Option): (i) the Shares will be held by at least 300 Shareholders at the 
time of Listing, in compliance with Rule 8.08(2) of the Listing Rules; (ii) the three largest public 
Shareholders will not hold more than 50% of the H Shares held in public hands at the time of Listing, 
in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; (iii) no placee will, individually, be 
placed more than 10% of the enlarged issued share capital of the Company immediately after the 
Global Offering; and (iv) there will not be any new substantial Shareholder (as defined in the Listing 
Rules) immediately after the Global Offering. 
COMMENCEMENT OF DEALINGS 
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, May 27, 
2026 (Hong Kong time), provided that the Global Offering has become unconditional and the right of 
termination described in the section headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has not been 
exercised. Investors who trade the H Shares on the basis of publicly available allocation details prior 
to the receipt of H Share certificates or prior to the H Share certificates becoming valid evidence of 
title do so entirely at their own risk. 
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Wednesday, May 
27, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange will 
commence at 9:00 a.m. on Wednesday, May 27, 2026 (Hong Kong time). The H Shares will be traded 
in board lots of 200 H Shares each, and the stock code of the H Shares will be 3310. 
By order of the Board 

<<<PAGE 23>>>
23 
 
Viewtrix Technology Co., Ltd 
雲英谷科技股份有限公司 
Dr. Gu Jing 
Chairman of the Board and Chief Executive 
Officer 
 
Hong Kong, May 26, 2026 
As at the date of this announcement, the Board comprises (i) Dr. Gu Jing and Mr. Han Zhiyong as 
executive Directors; (ii) Ms. Zhan Jing and Mr. Zhou Zhifeng as non-executive Directors; and (iii) Dr. 
Jiang Yimin, Ms. Zhou Xinru and Mr. Chang Eric Jackson as independent non-executive Directors. 
