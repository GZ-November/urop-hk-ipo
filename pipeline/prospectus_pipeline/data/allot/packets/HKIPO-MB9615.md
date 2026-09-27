# 配发结果公告抽取任务：9615.HK Mech-Mind Robotics Technologies Co., Ltd. - H Shares

- 公告：Announcement of Final Offer Price and Allotment Results
- 刊发时间（港交所元数据）：**31/08/2026 21:54**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0831/2026083102433.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"9615.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated Monday, August 24, 2026 (the “Prospectus”) of Mech-Mind Robotics Technologies 
Co., Ltd. (梅卡曼德(雄安)機器人科技股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an offer or an invitation to induce an offer 
by any person to acquire, purchase or subscribe for any of the securities of the Company. This announcement is not a 
prospectus. Potential investors should read the Prospectus for detailed information about the Global Offering described 
below before deciding whether or not to invest in the Offer Shares. Any investment decision in relation to the Offer 
Shares should be taken solely in reliance on the information provided in the Prospectus.
This announcement does not constitute an offer to sell or the solicitation of an offer to buy nor shall there be any sale 
of Offer Shares in any jurisdiction in which such offer, solicitation or sales would be unlawful. This announcement is 
not for release, publication or distribution, directly or indirectly, in or into the United States or any other jurisdiction 
where such distribution is prohibited by law, nor is this announcement an offer for sale or solicitation to purchase or 
subscribe for securities in the United States or any other jurisdictions. The Offer Shares have not been and will not 
be registered under the U.S. Securities Act or any state securities laws in the United States and may not be offered, 
sold, pledged or transferred within the United States or to, or for the account or benefit of U.S. persons (as defined 
in Regulation S under the U.S. Securities Act), except in transactions exempt from, or not subject to, the registration 
requirements of the U.S. Securities Act. The Offer Shares are being offered and sold outside the United States in 
offshore transactions in reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, CLSA Limited as the stabilizing manager (the “Stabilizing Manager”) (or any 
person acting for it), on behalf of the Underwriters, may over-allocate or effect transactions with a view to stabilizing 
or supporting the market price of the Shares at a level higher than that which might otherwise prevail for a limited 
period after the Listing Date. However, there is no obligation on the Stabilizing Manager (or any person acting for it) 
to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will be conducted at the absolute discretion 
of the Stabilizing Manager (or any person acting for it) and in what the Stabilizing Manager (or any person acting for 
it) reasonably regards as the best interest of our Company, (b) may be discontinued at any time, and (c) is required to 
be brought to an end within 30 days after the last day for lodging applications under the Hong Kong Public Offering 
(which is Saturday, September 26, 2026). Such stabilization action, if taken, may be effected in all jurisdictions where 
it is permissible to do so, in each case in compliance with all applicable laws, rules and regulatory requirements, 
including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, 
made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should note that no stabilizing action can be taken to support the price of the H Shares for longer 
than the stabilization period, which will begin on the Listing Date and is expected to expire on Saturday, September 
26, 2026, being the 30th day after the last day for lodging applications under the Hong Kong Public Offering. After 
this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of the H 
Shares, could fall. The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and 
conditions set out in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside 
Hong Kong and/or not resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint 
Sponsors and the Sponsor-Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall 
be entitled to terminate their obligations under the Hong Kong Underwriting Agreement with immediate effect upon 
the occurrence of any of the events set out in the section headed “Underwriting — Underwriting Arrangements and 
Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. 
(Hong Kong time) on the Listing Date (which is currently expected to be on Tuesday, September 1, 2026).

<<<PAGE 2>>>
2
Mech-Mind Robotics Technologies Co., Ltd.
梅卡曼德(雄安)機器人科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
: 23,140,590 H Shares (subject to the 
 Over-allotment Option)
Number of Hong Kong Offer Shares : 1,157,040 H Shares (subject to reallocation)
Number of International Offer Shares : 21,983,550 H Shares (subject to reallocation 
 and the Over-allotment Option)
Final Offer Price : HK$101.70 per H Share, plus brokerage 
 of 1%, SFC transaction levy of 0.0027%, 
 AFRC transaction levy of 0.00015% and 
 Stock Exchange trading fee of 0.00565% 
 (payable in full on application in 
 Hong Kong dollars, subject to refund)
Nominal value : RMB0.05 per H Share
Stock code : 09615
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators,
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
(in alphabetical order)
Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
(in alphabetical order)
Joint Bookrunners
(in alphabetical order)

<<<PAGE 3>>>
3
MECH-MIND ROBOTICS TECHNOLOGIES CO., LTD.
梅卡曼德(雄安)機器人科技股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated August 24, 2026 (the “Prospectus”) issued by 
Mech-Mind Robotics Technologies Co., Ltd. (梅卡曼德(雄安)機器人科技股份有限公司) (the 
“Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
09615
Stock short name
MECH-MIND ROBOT
Dealings commencement date
1 September 2026*
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$101.70
Offer Price range
HK$95.30 – HK$101.70
Offer Price adjustment exercised
N/A
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the Over-
allotment Option)
23,140,590
Final Number of Offer Shares in Hong Kong Public 
Offering (after reallocation)
4,628,130
Final Number of Offer Shares in International 
Offering (after reallocation and before exercise of 
the Over-allotment Option)
18,512,460
Number of issued shares upon Listing (before 
exercise of the Over-allotment Option)
125,011,050

<<<PAGE 4>>>
4
Over-allocation
No. of Offer Shares over-allocated
3,471,060
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$2,353.4 million
Less: Estimated listing expenses payable based on 
Final Offer Price
HK$(153.2) million
Net proceeds
HK$2,200.2 million
Note: Gross proceeds refer to the amount to which the issuer is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis.

<<<PAGE 5>>>
5
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
252,461
No. of successful applications
89,083
Subscription level
3,835.36 times
Claw-back triggered
Yes
No. of Offer Shares initially available under the Hong 
Kong Public Offering
1,157,040
No. of Offer Shares reallocated from the International 
Offering (claw-back)
3,471,090
Final no. of Offer Shares under the Hong Kong Public 
Offering (after reallocation)
4,628,130
% of Offer Shares under the Hong Kong Public 
Offering to the Global Offering
20.00%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to www.
hkeipo.hk/IPOResult to perform a search by name or identification number or www.hkeipo.hk/IPOResult for the 
full list of allottees.
INTERNATIONAL OFFERING
No. of placees
130
Subscription Level
13.39 times
No. of Offer Shares initially available under the 
International Offering
21,983,550
No. of Offer Shares reallocated to the Hong Kong 
Public Offering (claw-back)
3,471,090
Final no. of Offer Shares under the International 
Offering (after reallocation)
18,512,460
% of Offer Shares under the International Offering to 
the Global Offering
80.00%

<<<PAGE 6>>>
6
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, Single Largest Group 
of Shareholders, substantial shareholders, existing shareholders of the Company or any of its 
subsidiaries or their respective close associates; and (ii) none of the placees and the public who 
have purchased the Offer Shares are accustomed to taking instructions from the Company, any of 
the Directors, chief executive of the Company, Single Largest Group of Shareholders, substantial 
shareholders, existing shareholders of the Company or any of its subsidiaries or their respective 
close associates in relation to the acquisition, disposal, voting or other disposition of Shares 
registered in his/her/its name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
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
issued H 
Shares after 
the Global 
Offering 
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
Existing 
shareholders 
or their close 
associates
Baillie Gifford
4,629,480
20.01%
4.09%
3.70%
No
Taikang Life
3,086,310
13.34%
2.73%
2.47%
No
Invus
1,157,370
5.00%
1.02%
0.93%
No
Jane Street
1,157,370
5.00%
1.02%
0.93%
No
Ghisallo
1,157,370
5.00%
1.02%
0.93%
No
Ruihua
1,157,370
5.00%
1.02%
0.93%
No
NGS Super Fund
771,570
3.33%
0.68%
0.62%
No
E Fund
771,540
3.33%
0.68%
0.62%
No
Golden Link
462,930
2.00%
0.41%
0.37%
No
Total
14,351,310
62.02%
12.69%
11.48%
Note:
1. 
For further details of the cornerstone investors, please refer to the section headed “Cornerstone Investors” of the 
Prospectus.

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
issued H 
Shares after 
the Global 
Offering 
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
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients(Note 1)
CITIC Securities Asset 
Management Company Limited 
(“CITIC AM”)
390
0.0017%
0.0003%
0.0003%
Connected client 
as a placee
CITIC Securities Asset 
management (HK) Limited 
(“CITIC AM HK”)
390
0.0017%
0.0003%
0.0003%
Connected client 
as a placee
China Asset Management 
(Hong Kong) Limited 
(“China AMC HK”)
7,680
0.0332%
0.0068%
0.0061%
Connected client 
as a placee
Bosera Asset Management 
(International) Co., Ltd 
(“Bosera AM”)
7,680
0.0332%
0.0068%
0.0061%
Connected client 
as a placee
CITIC Securities International 
Capital Management 
Limited(“CSI”)
780
0.0034%
0.0007%
0.0006%
Connected client 
as a placee
Note:
1. 
See the section headed “Others/Additional Information — Placing to connected clients with a prior consent 
under paragraph 1C(1) of the Placing Guidelines” in this announcement for further details.

<<<PAGE 8>>>
8
Allottee(s) who are customer(s) and/or supplier(s) of the Company
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
issued H 
Shares after 
the Global 
Offering 
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
Golden Link
462,930
2.00%
0.41%
0.37%
Subsidiary of a 
customer of the 
Group 
DAIDO Co., LTD.
229,980
0.99%
0.20%
0.18%
Shareholder of a 
customer of the 
Group 
LOCK-UP UNDERTAKINGS
Key Persons(Note 1) and their close associate(s)
Name
Capacity
Number 
of Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon listing
% of total 
issued 
Shares after 
the Global 
Offering 
upon Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings (Note 3)
Mr. Shao
Founder of our Group, an executive 
Director and Chief Executive 
Officer
8,600,220
6.88%
August 31, 2027
Mech-Mind 
 Management(Note 2)
Close associate of Mr. Shao
8,625,680
6.90%
August 31, 2027
Mr. Fu
Founder of our Group, an executive 
Director and vice president of 
business
4,000,000
3.20%
August 31, 2027
Dr. Ding
Founder of our Group, an executive 
Director and vice president of R&D 
management
2,666,660
2.13%
August 31, 2027

<<<PAGE 9>>>
9
Notes:
1. 
(i) Mr. Shao, being our founder, an executive Director and a member of our senior management, and (ii) Mr. 
Fu and Dr. Ding, each being our co-founder, an executive Director and a member of our senior management 
are our key persons responsible for our technical operations and/or the research and development of our 
Specialist Technology Products and are subject to lock-up requirements pursuant to Rule 18C.14 of the 
Listing Rules. In addition, our key persons for the purpose of Rule 18C.14 of the Listing Rules also include 
Ms. Yang Pei, being an executive Director and a member of our senior management. As of the date of the 
Prospectus, Ms. Yang Pei did not directly hold any Shares but held certain Employee Awards under the 
Pre-IPO Employee Incentive Scheme comprising of (A) vested Employee Awards representing 110,391 
underlying Shares, and (B) outstanding Employee Awards representing 1,052,443 underlying Shares, 
accounted for approximately 0.93% in aggregate of the total issued Shares of the Company immediately 
following completion of the Global Offering (assuming the Over-allotment Option is not exercised). The 
Shares underlying the Pre-IPO Employee Incentive Scheme will be subject to a 12-month lock-up period 
pursuant to the relevant PRC laws and regulations. For further details of the Employee Awards, please refer 
to section headed “Appendix IV — Statutory and General Information — Pre-IPO Employee Incentive 
Scheme” in the Prospectus.
2. 
Mech-Mind Management is our employee incentive platform. We had granted Employee Awards to selected 
participants under the Pre-IPO Employee Incentive Scheme for indirect limited partnership interests in Mech-
Mind Management (i.e. limited partnership interests in certain limited partners of Mech-Mind Management) 
corresponding to certain underlying Shares of the Company. As of the date of the Prospectus, Mech-Mind 
Management owned approximately 8.47% of the issued Shares of the Company.
3. 
The lock-up period commences on the date by reference to which disclosure of its shareholding is made in 
the Prospectus and ends on the date which is 12 months from the Listing Date, i.e. August 31, 2027.
Pathfinder SIIs
Name
Capacity
Number 
of Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued 
Shares after 
the Global 
Offering 
upon Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings (Note 1)
Hanchen
Pathfinder SIIs
13,886,680
11.11%
August 31, 2027
Qiming Rongke
Pathfinder SIIs
7,521,000
6.02%
August 31, 2027
Note:
1. 
All existing Shareholders shall not dispose of any of the Shares held by them within the 12 months following 
the Listing Date as required under the applicable PRC laws, i.e. ending on August 31, 2027. In accordance 
with Rule 18C.14(2) of the Listing Rules, the required lock-up period commences on the date by reference to 
which disclosure of its shareholding is made in the Prospectus and ends on the date which is six months from 
the Listing Date, i.e. February 28, 2027.

<<<PAGE 10>>>
10
Single Largest Group of Shareholders
Name Note 1
Capacity
Number 
of Shares 
held in the 
Company 
subject to 
lock-up
undertakings 
upon Listing
% of total 
issued 
Shares after 
the Global 
Offering 
upon Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings (Note 1)
Mr. Shao
Beneficial Interest
8,600,220
6.88%
August 31, 2027
Mech-Mind 
 Management(Note 2)
Beneficial Interest
8,625,680
6.90%
August 31, 2027
Mr. Fu
Beneficial Interest
4,000,000
3.20%
August 31, 2027
Dr. Ding
Beneficial Interest
2,666,660
2.13%
August 31, 2027
Notes:
1. 
The lock-up period commences on the date by reference to which disclosure of its shareholding is made in 
the Prospectus and ends on the date which is 12 months from the Listing Date, i.e. August 31, 2027.
2. 
For illustrative purposes only, this subsection lists only those members of the Single Largest Shareholders 
who hold Shares directly in the Company. Pursuant to Rule 10.07 of the Listing Rules, each member of the 
Single Largest Group of Shareholders (namely, Mr. Shao, Mr. Fu, Dr. Ding and Mech-Mind Management) 
has undertaken to the Stock Exchange and the Company that, except in connection with the Global Offering 
(including the Over-allotment Option), he, she or it shall, and shall procure that the relevant registered 
holders of the Shares in which he, she or it is beneficially interested shall, comply with the applicable lock-
up requirements. For further details, please refer to the section headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Undertakings pursuant to the Hong Kong 
Underwriting Agreement — Undertakings by our Single Largest Group of Shareholders” in the Prospectus.

<<<PAGE 11>>>
11
Existing Shareholders
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
Shares after the 
Global Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
H shares after the 
Global Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject to the 
lock-up undertakings
Mr. Shao
8,600,220
4,300,110
6.88%
3.80%
August 31, 2027
Mr. Fu
4,000,000
2,000,000
3.20%
1.77%
August 31, 2027
Dr. Ding
2,666,660
1,333,330
2.13%
1.18%
August 31, 2027
Mech-Mind Management
8,625,680
4,312,840
6.90%
3.81%
August 31, 2027
Qingdao Jianrui
4,677,460
4,677,460
3.74%
4.14%
August 31, 2027
Qingdao Blue Bay
1,179,520
1,179,520
0.94%
1.04%
August 31, 2027
Zibo Jiacheng
609,280
609,280
0.49%
0.54%
August 31, 2027
Gongqingcheng Shangqi
6,401,220
6,401,220
5.12%
5.66%
August 31, 2027
Nanjing Lvyong
1,599,900
1,599,900
1.28%
1.42%
August 31, 2027
Dawo Xingguo
212,440
212,440
0.17%
0.19%
August 31, 2027
Dawo Tongde
444,940
444,940
0.36%
0.39%
August 31, 2027
Gongqingcheng Yintaijiayi
390,500
390,500
0.31%
0.35%
August 31, 2027
Gongqingcheng Yintaijiayu
169,780
169,780
0.14%
0.15%
August 31, 2027
Qingdao Gaozhi
551,380
551,380
0.44%
0.49%
August 31, 2027
Mingzhe Huihua
1,102,760
1,102,760
0.88%
0.98%
August 31, 2027
Tibet Delian
4,096,200
4,096,200
3.28%
3.62%
August 31, 2027
Qiming Rongke
7,521,000
7,521,000
6.02%
6.65%
August 31, 2027
Intel Asia Pacific
3,899,540
3,899,540
3.12%
3.45%
August 31, 2027
Hanchen
13,886,680
13,886,680
11.11%
12.28%
August 31, 2027

<<<PAGE 12>>>
12
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
Shares after the 
Global Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
H shares after the 
Global Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject to the 
lock-up undertakings
Suzhou Yuanming
5,590,980
5,590,980
4.47%
4.94%
August 31, 2027
Beijing Kuxun Technology
8,679,200
8,679,200
6.94%
7.68%
August 31, 2027
Zhuhai Jinguang
5,938,620
5,938,620
4.75%
5.25%
August 31, 2027
Coatue
1,905,040
1,905,040
1.52%
1.68%
August 31, 2027
Cliff Investment
3,245,000
3,245,000
2.60%
2.87%
August 31, 2027
Xiong’an Fund
1,599,900
1,599,900
1.28%
1.42%
August 31, 2027
Shanghai Nanxiang
479,980
479,980
0.38%
0.42%
August 31, 2027
Hebei Structural
319,980
319,980
0.26%
0.28%
August 31, 2027
Broad-Ocean Motor
1,599,900
1,599,900
1.28%
1.42%
August 31, 2027
CICC Porsche
799,960
799,960
0.64%
0.71%
August 31, 2027
Jiaxing Shanghe
516,760
516,760
0.41%
0.46%
August 31, 2027
Tianjin Yongtai
399,980
399,980
0.32%
0.35%
August 31, 2027
Tianjin Tianchuang
160,000
160,000
0.13%
0.14%
August 31, 2027

<<<PAGE 13>>>
13
Cornerstone Investors
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued Shares 
after the 
Global Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings (Note 1)
Baillie Gifford
4,629,480
3.70%
February 28, 2027
Taikang Life
3,086,310
2.47%
February 28, 2027
Invus
1,157,370
0.93%
February 28, 2027
Jane Street
1,157,370
0.93%
February 28, 2027
Ghisallo
1,157,370
0.93%
February 28, 2027
Ruihua
1,157,370
0.93%
February 28, 2027
NGS Super Fund
771,570
0.62%
February 28, 2027
E Fund
771,540
0.62%
February 28, 2027
Golden Link
462,930
0.37%
February 28, 2027
Note:
1. 
In accordance with the relevant cornerstone investment agreements, the required lock-up periods will end on 
February 28, 2027. The Cornerstone Investors will cease to be prohibited from disposing of or transferring 
the H Shares subscribed for pursuant to the relevant cornerstone investment agreements after the indicated 
date.

<<<PAGE 14>>>
14
PLACEE CONCENTRATION ANALYSIS
Shareholders
Number of H
Shares allotted
Allotment 
as % of 
International
Offering
(assuming the
Over-allotment
Option is not
exercised)
Allotment 
as % of 
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
(assuming the
Over-allotment
Option is not
exercised)
Allotment 
as % of
total Offer 
Shares
(assuming the
Over-allotment
Option is fully
exercised)
Number of 
Shares
held upon 
Listing
% of total 
issued share 
capital upon
Listing 
(assuming the 
Over-allotment
Option is not
exercised)
% of total 
issued share 
capital upon
Listing 
(assuming the 
Over-allotment
Option is fully
exercised)
Top 1
4,629,480
25.01%
21.06%
20.01%
17.40%
4,629,480
3.70%
3.60%
Top 5
11,187,900
60.43%
50.89%
48.35%
42.04%
11,187,900
8.95%
8.71%
Top 10
15,979,320
86.32%
72.69%
69.05%
60.05%
15,979,320
12.78%
12.44%
Top 25
20,984,880
113.36%
95.46%
90.68%
78.86%
20,984,880
16.79%
16.33%
Notes
* 
Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 15>>>
15
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders
Number of H
Shares allotted
Allotment 
as % of 
International
Offering
(assuming the
Over-allotment
Option is not
exercised)
Allotment 
as % of 
International
Offering
(assuming the
Over-allotment
Option is fully
exercised)
Allotment
as % of total
Offer Shares
(assuming the
Over-allotment
Option is not
exercised)
Allotment
as % of total
Offer Shares
(assuming the
Over-allotment
Option is fully
exercised)
Number of H
Shares held
upon Listing
% of 
total issued 
H share capital
upon Listing
(assuming the
Over-allotment
Option is not
exercised)
% of 
total issued
H share capital
upon Listing
(assuming the
Over-allotment
Option is fully
exercised)
% of 
total issued
share capital
upon Listing
(assuming the
Over-allotment
Option is not
exercised)
% of 
total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised)
Top 1
0
0.00%
0.00%
0.00%
0.00%
13,886,680
12.28%
11.92%
11.11%
10.81%
Top 5
0
0.00%
0.00%
0.00%
0.00%
50,034,280
44.25%
42.93%
40.02%
38.94%
Top 10
4,629,480
25.01%
21.06%
20.01%
17.40%
76,755,820
67.89%
65.86%
61.40%
59.74%
Top 25
15,207,780
82.15%
69.18%
65.72%
57.15%
101,806,200
90.04%
87.36%
81.44%
79.24%
Notes
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
Number of 
H Shares 
allotted
Allotment 
as % of 
International
Offering
(assuming the
Over-
allotment
Option is not
exercised)
Allotment 
as % of 
International
Offering
(assuming the
Over-
allotment
Option is fully
exercised)
Allotment as
% of total
Offer Shares
(assuming the
Over-
allotment
Option is not
exercised)
Allotment as
% of total
Offer Shares
(assuming the
Over-
allotment
Option is fully
exercised)
Number of H
Shares held
upon Listing
Number of
Shares held
upon Listing
% of 
total issued 
share
capital upon
Listing
(assuming the
 Over-
allotment
Option is not
exercised)
% of 
total issued 
share
capital upon
Listing
(assuming the
Over-
allotment
Option is fully
exercised)
Top 1
0
0.00%
0.00%
0.00%
0.00%
11,946,280
23,892,560
19.11%
18.60%
Top 5
0
0.00%
0.00%
0.00%
0.00%
50,034,280
61,980,560
49.58%
48.24%
Top 10
4,629,480
25.01%
21.06%
20.01%
17.40%
76,755,820
88,702,100
70.96%
69.04%
Top 25
15,207,780
82.15%
69.18%
65.72%
57.15%
101,806,200
113,752,480
90.99%
88.54%
Notes
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 16>>>
16
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
Pool A
Number of 
H Shares 
applied for
Number 
of valid 
applications
Basis of allocation/ballot
Approximate 
percentage allotted 
of the total number 
of H Shares 
applied for
30
54,080
1,623 out of 54,080 applicants to receive  
30 H Shares
3.00%
60
7,128
317 out of 7,128 applicants to receive  
30 H Shares
2.22%
90
21,898
1,224 out of 21,898 applicants to receive  
30 H Shares
1.86%
120
5,818
383 out of 5,818 applicants to receive  
30 H Shares
1.65%
150
6,568
490 out of 6,568 applicants to receive  
30 H Shares
1.49%
180
3,753
311 out of 3,753 applicants to receive  
30 H Shares
1.38%
210
3,131
283 out of 3,131 applicants to receive  
30 H Shares
1.29%
240
2,215
216 out of 2,215 applicants to receive  
30 H Shares
1.22%
270
2,283
238 out of 2,283 applicants to receive  
30 H Shares
1.16%
300
10,630
1,174 out of 10,630 applicants to receive  
30 H Shares
1.10%
450
16,909
2,349 out of 16,909 applicants to receive  
30 H Shares
0.93%
600
4,228
691 out of 4,228 applicants to receive  
30 H Shares
0.82%
750
2,739
508 out of 2,739 applicants to receive  
30 H Shares
0.74%
900
7,127
1,466 out of 7,127 applicants to receive  
30 H Shares
0.69%
1,050
2,860
642 out of 2,860 applicants to receive  
30 H Shares
0.64%
1,200
1,905
461 out of 1,905 applicants to receive  
30 H Shares
0.60%
1,350
1,590
412 out of 1,590 applicants to receive  
30 H Shares
0.58%
1,500
12,747
3,499 out of 12,747 applicants to receive  
30 H Shares
0.55%

<<<PAGE 17>>>
17
Number of 
H Shares 
applied for
Number 
of valid 
applications
Basis of allocation/ballot
Approximate 
percentage allotted 
of the total number 
of H Shares 
applied for
3,000
7,937
3,225 out of 7,937 applicants to receive  
30 H Shares
0.41%
4,500
6,312
3,226 out of 6,312 applicants to receive  
30 H Shares
0.34%
6,000
4,051
2,437 out of 4,051 applicants to receive  
30 H Shares
0.30%
7,500
3,063
2,090 out of 3,063 applicants to receive  
30 H Shares
0.27%
9,000
3,584
2,712 out of 3,584 applicants to receive  
30 H Shares
0.25%
10,500
2,835
2,341 out of 2,835 applicants to receive  
30 H Shares
0.24%
12,000
2,030
1,808 out of 2,030 applicants to receive 30 H 
Shares
0.22%
13,500
1,716
1,633 out of 1,716 applicants to receive 30 H 
Shares
0.21%
15,000
11,001
30 H Shares plus 111 out of 11,001 
applicants to receive an additional 30 H 
Shares
0.20%
30,000
7,849
30 H Shares plus 3,886 out of 7,849 
applicants to receive an additional 30 H 
Shares
0.15%
45,000
9,853
30 H Shares plus 8,677 out of 9,853 
applicants to receive an additional 30 H 
Shares
0.13%
Total
227,840 Total number of Pool A successful 
applicants: 64,462

<<<PAGE 18>>>
18
Pool B
Number of 
H Shares 
applied for
Number 
of valid 
applications
Basis of allocation/ballot
Approximate 
percentage allotted 
of the total number 
of H Shares 
applied for
60,000
8,441
60 H Shares plus 5,065 out of 8,441 
applicants to receive an additional  
30 H Shares
0.13%
75,000
3,011
60 H Shares plus 2,560 out of 3,011 
applicants to receive an additional  
30 H Shares
0.11%
90,000
2,232
60 H Shares plus 2,099 out of 2,232 
applicants to receive an additional  
30 H Shares
0.10%
105,000
1,641
90 H Shares
0.09%
120,000
1,234
90 H Shares plus 346 out of 1,234 applicants 
to receive an additional 30 H Shares
0.08%
135,000
843
90 H Shares plus 317 out of 843 applicants 
to receive an additional 30 H Shares
0.08%
150,000
4,049
90 H Shares plus 1,848 out of 4,049 
applicants to receive an additional  
30 H Shares
0.07%
300,000
1,484
120 H Shares
0.04%
450,000
522
120 H Shares plus 387 out of 522 applicants 
to receive an additional 30 H Shares
0.03%
578,520
1,164
150 H Shares
0.03%
Total
24,621 Total number of Pool B successful 
applicants: 24,621

<<<PAGE 19>>>
19
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and trading fee payable.
The Directors and the Sponsor-Overall Coordinators confirm that at least 50% of the total number 
of the Offer Shares have been allocated to and taken up by independent price setting investors in 
compliance with Rule 18C.08 of the Listing Rules.
The Directors further confirm that at least 20% of the issued share capital of the Company will be 
held by sophisticated independent investors at the time of Listing in compliance with Chapter 2.5 
of the Guide for New Listing Applicants.
OTHERS/ADDITIONAL INFORMATION
Reallocation
As the Hong Kong Public Offering has been oversubscribed 50 times or more, the reallocation as 
described in the section headed “Structure of the Global Offering — Pricing and Allocation — 
Reallocation” of the Prospectus has been applied.
As a result of the above, the final number of Offer Shares under the Hong Kong Public Offering 
is adjusted to 4,628,130 Shares, representing approximately 20.00% of the total number of Offer 
Shares available under the Global Offering (assuming the Over-allotment Option is not exercised), 
and the final number of Offer Shares under the International Offering is adjusted to 18,512,460 
Shares, representing approximately 80.00% of the total number of Offer Shares under the Global 
Offering (assuming the Over-allotment Option is not exercised).

<<<PAGE 20>>>
20
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such 
Offer Shares in the International Offering to the connected clients. The allocation of Offer Shares 
to such connected clients is in compliance with all the conditions under the consent granted by the 
Stock Exchange. Details of the placement to connected clients are set out below:
No.
Connected 
Distributor
Connected 
Client
Relationship with 
the Connected 
Distributor
Identities of 
the ultimate 
beneficial 
owners of the 
Offer Shares 
or, where 
applicable, 
details of the 
structured 
products 
under 
which the 
subscription 
by the 
Connected 
Client was 
made (e.g. 
OTC total 
return swaps)
Whether the 
Connected 
Client is a 
collective 
investment 
scheme 
which is not 
authorised by 
the SFC or 
is expected 
to hold the 
Offer Shares 
on behalf of 
such scheme
Number of 
Offer Shares 
allocated to 
the connected 
client
Approximate 
percentage of 
total number 
of Offer 
Shares under 
the Global 
Offering 
(assuming 
no exercise 
of the Over-
allotment 
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
of the Over-
allotment 
Option)
Part A — Connected Client holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties
1.
CLSA Limited 
(“CLSA”)
CITIC AM
CLSA and CITIC 
AM, are members of 
the same group of 
companies.
Please refer to 
Note 2
Yes
390
0.0017%
0.0003%
2.
CLSA
CITIC AM 
HK
CITIC AM HK is a 
member of the same 
group of companies 
as CLSA.
Please refer to 
Note 3
No
390
0.0017%
0.0003%
3.
CLSA
China AMC 
HK
China AMC HK is a 
member of the same 
group of companies 
as CLSA.
Please refer to 
Note 4
No
7,680
0.0332%
0.0061%
4.
China Merchants 
Securities (HK) 
Co., Limited (Note 1) 
(“CMS”)
Bosera AM
Bosera AM is a 
member of the same 
group with CMS.
Please refer to 
Note 5
Yes
7,680
0.0332%
0.0061%

<<<PAGE 21>>>
21
Notes:
1. 
CMS is a sub-distributor in connection with the Global Offering.
2. 
CITIC AM will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on 
behalf of their investors (the “CITIC Asset Management Ultimate Clients”), each of which is an independent 
third party.
The details of the CITIC Asset Management Ultimate Clients are as follows:
Fund Name
Values of Assets 
under Management
Whether 
the Scheme 
is Publicly 
Marketed
Fund 
Manager
UBO Holding 
30% or More 
Interests in 
the Fund
UBO of 
Fund Manager
Number of 
the CITIC Asset 
Management 
Ultimate Clients
CITIC Securities AM-Guibinfengyuan No.118 
QDII (中信證券資管貴賓豐元 118 號 QDII  
集合資產管理計劃)
RMB231,609,106.16
Not publicly 
marketed
CITIC AM
Natural person 
Zhang Guofeng  
(張國鋒)
CITIC Securities 
Company 
Limited
7
CITIC SECURITIES COMPANY LIMITED-
XINHANG ZHIYUAN NO.1 (中信證券信航 
致遠 1 號集合資產管理計劃)
RMB21,139,210.99
Not publicly 
marketed
CITIC AM
No
CITIC Securities 
Company 
Limited
20
CITIC SECURITIES COMPANY LIMITED-
XINHANG ZHIYUAN NO.3 (中信證券信航 
致遠 3 號集合資產管理計劃)
RMB48,687,738.97
Not publicly 
marketed
CITIC AM
No
CITIC Securities 
Company 
Limited
35
CITIC SECURITIES AM-GUIBINFENGYUAN 
NO.108 QDII (中信證券資管貴賓豐元  
108 號 QDII 集合資產管理計劃)
RMB433,025,957.34
Not publicly 
marketed
CITIC AM
No
CITIC Securities 
Company 
Limited
43
3. 
CITIC AM HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds 
on behalf of their investors, each of which is an independent third party.
The funds are as follows:
(1) 
CITIC Securities Asset Management (HK) Limited – Meta Chance2, invested 100% by Meta Chance 
Limited, of which UBO holding 30% or more interest is natural person Song Ke;
(2) 
ICBC (ASIA) LTD-CITIC SECURITIES AM LTD-BSCOMC LTD, invested 100% by BSCOMC Limited, 
of which UBO holding 30% or more interest is State-owned Assets Supervision and Administration 
Commission of People’s Government of Beijing Municipality; and
(3) 
CITIC Securities Asset management (HK) Limited – CLSA CT LIMITED SUB ACCOUNT 29 – CGM, 
invested 100% by Wander Rise Assets Pte. Ltd., of which UBO holding 30% or more interest is natural 
person Sun Shigen.
4. 
China AMC HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds 
on behalf of their investors, each of which is an independent third party.
The funds are as follows:
(1) 
CHINAAMC SELECT GREATER CHINA TECHNOLOGY FUND, of which UBO holding 30% or more 
interest is Futu Securities International (Hong Kong) Limited – client account. No investor having 30% 
or more interest in Futu Securities International (Hong Kong) Limited – client account;
(2) 
CHINAAMC FUND – CHINAAMC CHINA OPPORTUNITIES FUND, of which no beneficial owner 
holds 30% or more interest;
(3) 
CHINAAMC CHINA FOCUS FUND, of which the only ultimate beneficial owner holding 30% or more 
interest is Manulife (International) Limited; and

<<<PAGE 22>>>
22
(4) 
ICBC (ASIA) LTD-CHINAAMC-BSCOMC LTD, invested 100% by BSCOMC Limited, of which the 
only ultimate beneficial owner holding 30% or more interest is State-owned Assets Supervision and 
Administration Commission of People’s Government of Beijing Municipality.
5. 
Bosera AM will hold the Offer Shares in its capacity as the discretionary fund manager managing the sub-funds 
on behalf of the following clients, each of which is an independent third party of the Company, its subsidiaries, 
its substantial shareholders, CMS and the companies which are members of the same group of companies as 
CMS.
Name of the sub-funds to 
which the Offer Shares 
will be allocated
Whether any investor 
holds 30% or more 
interests in the sub-fund 
(Y/N)
Name of UBO
Shareholding %
Fortuna Capital 
Management Limited IPO 
Mandate
Y
Yang Dehui 楊德會
100
Navigator Technology 
Limited IPO Mandate
Y
Fuhua Zheng 鄭複花
100
No.
Connected 
Distributor
Connected 
Client
Relationship with the 
Connected Distributor
Identities of 
the ultimate 
beneficial 
owners of the 
Offer Shares 
or, where 
applicable, 
details of the 
structured 
products 
under 
which the 
subscription 
by the 
Connected 
Client was 
made (e.g. 
OTC total 
return swaps)
Whether the 
Connected 
Client is a 
collective 
investment 
scheme 
which is not 
authorised by 
the SFC or 
is expected 
to hold the 
Offer Shares 
on behalf of 
such scheme
Number of 
Offer Shares 
allocated to 
the connected 
client
Approximate 
percentage of 
total number 
of Offer 
Shares under 
the Global 
Offering 
(assuming 
no exercise 
of the Over-
allotment 
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
of the Over-
allotment 
Option)
Part B — Connected Clients holding the beneficial interest of the Offer Shares on a non-discretionary basis on behalf of independent third parties
1.
CLSA
CSI
CSI is a member of 
the same group of 
companies as CLSA.
Please refer to 
Note 1
No
780
0.0034%
0.0006%

<<<PAGE 23>>>
23
Notes:
1. 
CSI will hold the Offer Shares as a placee under the International Offering on behalf of its ultimate clients 
(the “CSI Ultimate Clients”), on a non-discretionary basis, pursuant to which: (i) CSI will act as the single 
counterparty of the CSI Back-to-back TRS (the “CSI Back-to-back TRS”) to be entered into by it in connection 
with a total return swap order (the “CSI Client TRS”) placed and fully funded by the CSI Ultimate Clients, by 
which CSI will pass the full economic exposure of the Offer Shares placed to CSI to the CSI Ultimate Clients; 
(ii) as confirmed by CSI and CLSA, CSI will hold the legal title and beneficial interest in the Offer Shares, 
but will contractually agree to pass on the full economic exposure and return of the Offer Shares to the CSI 
Ultimate Clients, on a non-discretionary basis. The CSI Ultimate Clients may exercise their early termination 
rights to terminate the CSI Client TRS at any time from the trade date of the CSI Client TRS which should be 
on or after the date on which the Offer Shares are listed on the Stock Exchange; (iii) upon the final maturity 
or termination of the CSI Client TRS by the CSI Ultimate Clients, CSI will dispose of the Offer Shares on the 
secondary market and the CSI Ultimate Clients will receive a final termination amount of the CSI Back-to-
back TRS which will have taken into account all the economic returns or economic loss in relation to the Offer 
Shares and the fixed amount of transaction fees of the CSI Back-to-back TRS and the CSI Client TRS. Due to 
its internal policy, CSI will not exercise the voting right of the Offer Shares during the terms of the CSI Back-
to-back TRS; and (iv) CSI is not a collective investment scheme which is not authorized by the SFC, nor is 
expected to hold the Offer Shares on behalf of such scheme.
The details of the CSI Ultimate Clients are as follows:
Name (CSI Ultimate 
Client)
Asset Manager
UBO of Asset 
Manager
UBO of CSI Ultimate Client
Hover4pi Fund I OFC
Hover4pi Capital 
Management
He Hui
None
Hana Securities
N/A
N/A
HANA FINANCIAL GROUP 
(BBG ticker 086790 KS)
To the best of knowledge of CSI and having made all reasonable inquiries, each of the CSI Ultimate Clients and 
its UBOs is an independent third party of the Company, its subsidiaries, its substantial shareholders, CSI, CLSA 
and the companies which are members of the same group of companies as CLSA.

<<<PAGE 24>>>
24
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the 
“Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy 
or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer or 
solicitation to purchase or subscribe for securities in the United States. The securities mentioned 
herein have not been, and will not be, registered under the United States Securities Act of 1933, 
as amended (the “U.S. Securities Act”). The securities may not be offered or sold in the United 
States except pursuant to an exemption from the registration requirements of the U.S. Securities 
Act and in compliance with any applicable state securities laws, or outside the United States 
unless in compliance with Regulation S under the U.S. Securities Act. There will be no public 
offer of securities in the United States.
The Offer Shares are being offered and sold outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated August 24, 2026 issued by Mech-Mind Robotics 
Technologies Co., Ltd. (梅卡曼德(雄安)機器人科技股份有限公司) for detailed information 
about the Global Offering described below before deciding whether or not to invest in the Shares 
thereby being offered.
* 
Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-Overall Coordinators 
(for themselves and on behalf of the Hong Kong Underwriters), may, in their sole and absolute discretion, upon 
giving notice in writing to the Company, terminate the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the paragraph headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus 
at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
September 1, 2026).

<<<PAGE 25>>>
25
PUBLIC FLOAT AND FREE FLOAT
Pursuant to Rule 19A.13A of the Listing Rules, assuming that the Over-allotment Option is 
not exercised, based on the Offer Price of HK$101.70 per Offer Share, the expected market 
capitalization of the Company upon the Listing is HK$12,713.6 million, and the minimum 
prescribed public float percentage applicable to our Shares is 15%. Immediately after the 
completion of the Global Offering, 87,231,810 H Shares, representing approximately 69.78% of 
the issued share capital of our Company, will count towards the public float, thereby satisfying the 
minimum percentage requirement in compliance with Rule 19A.13A(1) of the Listing Rules.
Based on the final Offer Price of HK$101.70 per H Share, the Company satisfies the free float 
requirement under Rule 19A.13C of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering: (i) no 
placee will, individually, be placed more than 10% of the enlarged issued share capital of the 
Company; (ii) there will not be any new substantial Shareholder (as defined in the Listing Rules) 
of the Company; (iii) the three largest public shareholders of the Company do not hold more than 
50% of the H Shares in public hands at the time of the Listing in compliance with Rules 8.08(3) 
and 8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at the time of the 
Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, 
September 1, 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” in the 
Prospectus has not been exercised. Investors who trade the H Shares on the basis of publicly 
available allocation details prior to the receipt of H Share certificates or prior to the H Share 
certificates becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Tuesday, 
September 1, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Tuesday, September 1, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 30 H Shares each, and the stock code of the H Shares will be 
09615.
By order of the Board
Mech-Mind Robotics Technologies Co., Ltd.
梅卡曼德(雄安)機器人科技股份有限公司
Mr. Shao Tianlan
Chairperson of the Board, executive Director 
and chief executive officer
Hong Kong, August 31, 2026
Directors of the Company named in the application to which this announcement relates are: (i) 
Mr. Shao Tianlan, Mr. Fu Ao, Dr. Ding Youshuang and Ms. Yang Pei as executive Directors; (ii) 
Ms. Gong Yuan as non-executive Director; and (iii) Dr. Liu Ming, Dr. Tan Weijia and Dr. Zhang 
Qiusheng as independent non-executive Directors.
