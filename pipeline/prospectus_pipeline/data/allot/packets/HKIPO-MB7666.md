# 配发结果公告抽取任务：7666.HK Metis TechBio Co., Ltd. - P - H Shares

- 公告：Announcement of Allotment Results
- 刊发时间（港交所元数据）：**12/05/2026 22:43**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0512/2026051201482.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"7666.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
defined in the prospectus dated May 5, 2026 (the “Prospectus”) of Metis TechBio Co., Ltd. ( 劑泰科技(北京)股份有
限公司) (the “Company”).
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
requirements of the U.S. Securities Act. The Offer Shares are being offered and sold (1) solely to qualified institutional 
buyers as defined in Rule 144A in reliance on Rule 144A or another exemption from, or in a transaction not subject 
to, registration under the U.S. Securities Act and (2) outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act and applicable laws of each jurisdiction where those offers and sales occur.
In connection with the Global Offering, CLSA Limited, as the stabilizing manager (the “Stabilizing Manager”) 
(or any person acting for it), on behalf of the Underwriters, may over-allocate or effect transactions with a view to 
stabilizing or supporting the market price of the Shares at a level higher than that which might otherwise prevail for a 
limited period after the Listing Date. However, there is no obligation on the Stabilizing Manager (or any person acting 
for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will be conducted at the absolute 
discretion of the Stabilizing Manager (or any person acting for it) and in what the Stabilizing Manager (or any person 
acting for it) reasonably regards as the best interest of our Company, (b) may be discontinued at any time, and (c) is 
required to be brought to an end within 30 days after the last day for lodging applications under the Hong Kong Public 
Offering (which is Sunday, June 7, 2026). Such stabilization action, if taken, may be effected in all jurisdictions where 
it is permissible to do so, in each case in compliance with all applicable laws, rules and regulatory requirements, 
including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, 
made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the Shares for longer 
than the stabilization period which begins on the Listing Date, and is expected to expire on Sunday, June 7, 2026, the 
30th day after the last day for the lodging of applications under the Hong Kong Public Offering. After this date, when 
no further stabilizing action may be taken, demand for the Shares, and therefore the price of the Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out 
in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/
or not resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint Sponsors and the 
Sponsor-Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to 
terminate their obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence 
of any of the events set out in the section headed “Underwriting — Underwriting Arrangements and Expenses — Hong 
Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) 
on the Listing Date (which is currently expected to be on Wednesday, May 13, 2026).

<<<PAGE 2>>>
2
Metis TechBio Co., Ltd.
劑泰科技(北京)股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the Global 
Offering
:
201,229,000 H Shares (subject to the 
 Over-allotment Option)
Number of Hong Kong Offer Shares
:
40,246,000 H Shares (as adjusted after 
 reallocation)
Number of International Offer Shares
:
160,983,000 H Shares (as adjusted after 
 reallocation and subject to the 
 Over-allotment Option)
Offer Price
:
HK$10.50 per H Share, plus brokerage 
 of 1%, SFC transaction levy of 0.0027%, 
 Stock Exchange trading fee of 0.00565% 
 and Accounting and Financial Reporting 
 Council transaction levy of 0.00015%
Nominal value
:
RMB0.10 per H Share
Stock code
:
7666
Joint Sponsors
Overall Coordinators and Joint Global Coordinators
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
METIS TECHBIO CO., LTD.
劑泰科技(北京)股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated May 5, 2026 (the “Prospectus”) issued by Metis 
TechBio Co., Ltd. ( 劑泰科技(北京)股份有限公司) (the “Company”).
SUMMARY
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
Company information
Stock code
7666
Stock short name
METIS TECHBIO-P
Dealings commencement date
13 May 2026*
* 
see note at the end of the announcement
Price Information
Offer Price
HK$10.50
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the Over-
allotment Option)
201,229,000
Final Number of Offer Shares in Hong Kong Public Offering 
(after reallocation)
40,246,000
Final Number of Offer Shares in International Offering 
(after reallocation and before exercise of the Over-allotment 
Option)
160,983,000
Number of issued shares upon Listing (before exercise of the 
Over-allotment Option)
1,152,513,850

<<<PAGE 4>>>
4
Over-allocation
No. of Offer Shares over-allocated
30,184,000
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$2,112.9 million
Less: Estimated listing expenses payable based on Offer Price
HK$(120.2) million
Net proceeds
HK$1,992.7 million
Note: Gross proceeds refer to the amount to which the issuer is entitled receive. For details of the use of proceeds, 
please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The Company will 
adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if any) for the 
purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus on a pro rata 
basis.

<<<PAGE 5>>>
5
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
383,309
No. of successful applications
65,740
Subscription level
6910.96 times
Claw-back triggered
Yes
No. of Offer Shares initially available under the Hong Kong 
Public Offering
10,061,500
No. of Offer Shares reallocated from the International 
Offering (claw-back)
30,184,500
Final no. of Offer Shares under the Hong Kong Public 
Offering (after reallocation)
40,246,000
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering
20%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors 
can refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
208
Subscription Level
33.86 times
No. of Offer Shares initially available under the International 
Offering
191,167,500
No. of Offer Shares reallocated to the Hong Kong Public 
Offering (claw-back)
30,184,500
Final no. of Offer Shares under the International Offering 
(after reallocation)
160,983,000
% of Offer Shares under the International Offering to the 
Global Offering
80%

<<<PAGE 6>>>
6
The Directors confirm that, to the best of their knowledge, information and belief, save for 
consent under paragraphs 1C(1) and 1C(2) of Appendix F1 to the Listing Rules and Chapter 
2.5 and Chapter 4.15 of the Stock Exchange’s Guide for New Listing Applicants (the “Placing 
Guidelines”) granted by the Stock Exchange to permit the Company to allocate certain Offer 
Shares in the International Offering to existing Shareholder, close associates of existing 
Shareholders and connected clients of the overall coordinator(s), any syndicate member(s) 
(other than the overall coordinator(s)) or any distributor(s) (other than syndicate member(s)) 
as a cornerstone investor and a placee, (i) none of the Offer Shares subscribed by the placees 
and the public have been financed directly or indirectly by the Company, any of the Directors, 
chief executive of the Company, Single Largest Shareholders, substantial shareholders, existing 
shareholders of the Company or any of its subsidiaries or their respective close associates; and (ii) 
none of the placees and the public who have purchased the Offer Shares are accustomed to taking 
instructions from the Company, any of the Directors, chief executive of the Company, Single 
Largest Shareholders, substantial shareholders, existing shareholders of the Company or any of its 
subsidiaries or their respective close associates in relation to the acquisition, disposal, voting or 
other disposition of Shares registered in his/her/its name or otherwise held by him/her/it.

<<<PAGE 7>>>
7
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
BlackRock
37,304,500
18.54%
3.54%
3.24%
No
UBS AM Singapore
11,191,000
5.56%
1.06%
0.97%
No
China Venture Capital 
Innovation Investment Fund 
Co., Ltd.
7,460,500
3.71%
0.71%
0.65%
No
Mirae
5,968,500
2.97%
0.57%
0.52%
No
HHLRA
5,968,500
2.97%
0.57%
0.52%
No
Deerfield
3,730,000
1.85%
0.35%
0.32%
No
RTW Funds
3,730,000
1.85%
0.35%
0.32%
No
Arc Avenue
3,730,000
1.85%
0.35%
0.32%
No
Huadeng Technology
3,730,000
1.85%
0.35%
0.32%
No
Isometry Global
3,730,000
1.85%
0.35%
0.32%
No
GF Fund
3,730,000
1.85%
0.35%
0.32%
No
ICBCUBS Entities
3,730,000
1.85%
0.35%
0.32%
No
China AMC (HK)
3,730,000
1.85%
0.35%
0.32%
No
Fullgoal Fund
3,730,000
1.85%
0.35%
0.32%
No
Lake Bleu
2,984,000
1.48%
0.28%
0.26%
No
Sage Partners
2,984,000
1.48%
0.28%
0.26%
No
ICBC Wealth Management
1,492,000
0.74%
0.14%
0.13%
No
ORIX Asia AM
1,492,000
0.74%
0.14%
0.13%
No
Total
110,415,000
54.87%
10.49%
9.58 %
Note:
1. 
For further details of the cornerstone investors, please refer to the section headed “Cornerstone Investors” of the 
Prospectus.

<<<PAGE 8>>>
8
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
Allottees with waiver from strict compliance with the requirements under Rule 10.04 of the Listing Rules and 
consent under paragraph 1C(2) of the Placing Guidelines in relation to allocations to existing Shareholders and 
close associates of existing Shareholders(Note 1)
Placees
Martis Fund
3,730,500
1.85%
0.35%
0.32%
A placee, 
an existing 
shareholder 
and a close 
associate of 
an existing 
shareholder
Yael Capital Management 
Limited
4,477,000
2.22%
0.43%
0.39%
A placee and a 
close associate 
of an existing 
shareholder
Mr. Tse Eric S Y
746,500
0.37%
0.07%
0.06%
A placee and a 
close associate 
of an existing 
shareholder
China Life Franklin Asset 
Management Co., Limited
261,000
0.13%
0.02%
0.02%
A placee and a 
close associate 
of an existing 
shareholder
Subtotal
9,215,000
4.58%
0.88%
0.80%

<<<PAGE 9>>>
9
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
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients(Note2)
China AMC (HK)
3,730,000
1.85%
0.35%
0.32%
Connected 
client as a 
cornerstone
CITIC Securities Asset 
Management Company 
Limited (“CITIC Asset 
Management”)
1,500
0.0007%
0.0001%
0.0001%
Connected 
client as a 
placee
CITIC Securities Asset 
Management (HK) Limited 
(“CITIC Securities Asset”)
1,500
0.0007%
0.0001%
0.0001%
Connected 
client as a 
placee
Harvest Global Investments 
Limited (“Harvest”)
12,000
0.006%
0.001%
0.001%
Connected 
client as a 
placee
DWS Investments Hong 
Kong Limited (“DWS”)
12,000
0.006%
0.001%
0.001%
Connected 
client as a 
placee
HSBC Global Asset 
Management (Hong Kong) 
Limited (“HSBC AM”)
373,000
0.19%
0.04%
0.03%
Connected 
client as a 
placee
CITIC Securities 
International Capital 
Management Limited 
(“CSI”)
2,348,500
1.17%
0.22%
0.20%
Connected 
client as a 
placee
Subtotal
6,478,500
3.22%
0.62%
0.56%

<<<PAGE 10>>>
10
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
Notes:
1. 
See the section headed “Others/Additional Information — Placing to the existing shareholders and/or their 
close associates with a prior waiver under Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) 
of the Placing Guidelines” in this announcement for further details.
2. 
See “Waivers — Consent in respect of the Proposed Subscription of the Offer Shares by Connected Client” 
of the Prospectus and the section headed “Others/Additional Information — Placing to connected clients with 
a prior consent under paragraph 1C(1) of the Placing Guidelines” in this announcement for further details.
LOCK-UP UNDERTAKINGS
Key Persons(Note 1) (as Defined under Rule 18C.14 of the Listing Rules)
Name
Capacity
Number of 
Shares held in 
the Company 
subject to lock-
up
undertakings 
upon listing
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
undertakings (Note 2)
Dr. Lai
Co-founder, chairman 
of the Board, executive 
Director and chief 
executive officer
—
—
May 12, 2028
Scientia HK
Dr. Lai’s close associate
121,334,260
10.53%
May 12, 2028
Delos Holding
Dr. Lai’s close associate
16,000,000
1.39%
May 12, 2028
Dechi Holding
Dr. Lai’s close associate
10,232,590
0.89%
May 12, 2028
Dr. Chen
Co-founder, executive 
Director and chief
research and development 
officer
66,913,490
5.81%
May 12, 2028
Dr. Wang
Co-founder, executive 
Director and chief
operating officer
34,911,380
3.03%
May 12, 2028

<<<PAGE 11>>>
11
Name
Capacity
Number of 
Shares held in 
the Company 
subject to lock-
up
undertakings 
upon listing
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
undertakings (Note 2)
Nanjing Chengtai 
Yuxin
Dr. Wang’s close 
associate
25,857,170
2.24%
May 12, 2028
Hangzhou Shengtai
Dr. Wang’s close 
associate
16,524,730
1.43%
May 12, 2028
Subtotal
291,773,620
25.32%
Notes:
1. 
Dr. Lai, Dr. Chen and Dr. Wang are our Co-founders, executive Directors and senior management, each 
being our key persons responsible for our technical operations and/or the research and development of our 
Specialist Technology Products, who are subject to lock-up requirements pursuant to Rule 18C.14 of the 
Listing Rules. In addition, our key persons for the purpose of Rule 18C.14 of the Listing Rules also include 
(i) Dr. Alan Fu, Dr. Wei Xu and Mr. Mark Robert Herbert, each being a senior management member of the 
Company, and (ii) Dr. Andong Liu, our vice president and head of technology and one of our key personnel 
responsible for our Company’s technical operations and/or the research and development of our Specialist 
Technology Products (collectively, the “Other Key Persons”). As of the date of the Prospectus, the Other 
Key Persons held certain Equity Incentives under our Employee Incentive Schemes, for further details of the 
Employee Incentives, please refer to section headed “Appendix V — Statutory and General Information — 
Further Information about our Directors, Senior Management and Substantial Shareholders — 5. Employee 
Incentive Schemes.” in the Prospectus.
2. 
The lock-up period commences on the date by reference to which disclosure of its shareholding is made in 
the Prospectus and ends on the date which is 24 months from the Listing Date, i.e. May 12, 2028. In the 
event that upon the notification by the Stock Exchange that the Company will no longer be regarded as a Pre-
Commercial Company after the Listing, the lock-up period will expire on the later of: (i) the date on which 
such lock-up periods would have ended if the Company had applied for listing as a Commercial Company; 
and (ii) the date falling on the 30th day after the announcement on the removal of designation as a Pre-
Commercial Company as required under Rule 18C.24 of the Listing Rules.

<<<PAGE 12>>>
12
Pathfinder SIIs
Name Note 1
Capacity
Number 
of Shares 
held in the 
Company 
subject to 
lock-up
undertakings 
upon
Listing
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
Last day subject to 
the lock-up
undertakings (Note 1)
CICC
Pathfinder SIIs
108,800,000
9.44%
May 12, 2027
HSG
Pathfinder SIIs
65,558,660
5.69%
May 12, 2027
Beijing PICC Health 
and Pension Industry 
Investment Fund 
(Limited Partnership) 
(北京人保健康養老產
業投資基金(有限合
夥)) (“PICC Health 
& Pension Fund”)
Pathfinder SIIs
50,324,060
4.37%
May 12, 2027
5Y Capital
Pathfinder SIIs
45,463,970
3.94%
May 12, 2027
Jiangsu Jiequan 
Chengda Equity 
Investment Centre 
(Limited Partnership) 
(江蘇疌泉成達股權投
資中心(有限合夥))
Pathfinder SIIs
35,025,550
3.04%
May 12, 2027
Note:
1. 
In accordance with Rule 18C.14 of the Listing Rules, the required lock-up period commences on the date 
by reference to which disclosure of its shareholding is made in the Prospectus and ends on the date which 
is 12 months from the Listing Date, i.e. May 12, 2027. In the event that upon the notification by the Stock 
Exchange that the Company will no longer be regarded as a Pre-Commercial Company after the Listing, the 
lock-up period will expire on the later of: (i) the date on which such lock-up periods would have ended if the 
Company had applied for listing as a Commercial Company; and (ii) the date falling on the 30th day after the 
announcement on the removal of designation as a Pre-Commercial Company as required under Rule 18C.24 
of the Listing Rules.

<<<PAGE 13>>>
13
Single Largest Shareholders
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
Dr. Wang
Beneficial Interest
34,911,380
3.03%
May 12, 2028
Dr. Chen
Beneficial Interest
66,913,490
5.81%
May 12, 2028
Dr. Lai/Scientia 
 HK (Note 2)
Beneficial Interest
121,334,260
10.53%
May 12, 2028
Delos(Note 3)
Beneficial Interest
16,000,000
1.39%
May 12, 2028
Nanjing Chengtai 
Yuxin
Beneficial Interest
25,857,170
2.24%
May 12, 2028
Hangzhou Shengtai
Beneficial Interest
16,524,730
1.43%
May 12, 2028
Dechi Holding (Note 4)
Beneficial Interest
10,232,590
0.89%
May 12, 2028
Notes:
1. 
The lock-up period commences on the date by reference to which disclosure of its shareholding is made in 
the Prospectus and ends on the date which is 24 months from the Listing Date, i.e. May 12, 2028. In the 
event that upon the notification by the Stock Exchange that the Company will no longer be regarded as a Pre-
Commercial Company after the Listing, the lock-up period will expire on the later of: (i) the date on which 
such lock-up periods would have ended if the Company had applied for listing as a Commercial Company; 
and (ii) the date falling on the 30th day after the announcement on the removal of designation as a Pre-
Commercial Company as required under Rule 18C.24 of the Listing Rules.
2. 
Scientia HK Limited, a private company limited by shares incorporated on February 17, 2023, which is 
wholly owned by Dr. Lai.
3. 
As of the date of this announcement, Delos Holding was controlled by Dr. Lai as to approximately 38.57% 
and the remaining 61.43% equity interests were held by the relevant grantees under the 2023 Equity Incentive 
Plan, none of whom holds 30% or more of the equity interests therein.
4. 
As of the date of this announcement, Dechi Holding was owned as to (i) 3.91% by Dr. Lai; (ii) 44.82% by Dr. 
Alan Fu; (iii) 34.04% by Mr. Mark Robert Herbert; and (iv) 17.23% by three consultants of our Company. 
Dr. Lai controlled Dechi Holding through the only one management share he held and he is also responsible 
for the day-to-day decision making of Dechi Holding.

<<<PAGE 14>>>
14
Existing Shareholders
Name
Number of 
Shares held in 
the Company 
subject to
lock-up 
undertakings 
upon Listing
Number of H 
Shares held in 
the Company 
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
% of total 
issued H 
shares after 
the Global 
Offering
upon Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Last day 
subject to 
the lock-up 
undertakings
Dr. Wang
34,911,380
24,437,966
3.03%
2.32%
May 12, 2028
Dr. Chen
66,913,490
46,839,443
5.81%
4.45%
May 12, 2028
Dr. Lai/Scientia HK (Note 1)
121,334,260
84,933,982
10.53%
8.07%
May 12, 2028
Delos (Note 2)
16,000,000
16,000,000
1.39%
1.52%
May 12, 2028
Nanjing Chengtai Yuxin
25,857,170
25,857,170
2.24%
2.46%
May 12, 2028
Hangzhou Shengtai
16,524,730
16,524,730
1.43%
1.57%
May 12, 2028
Dechi Holding (Note 3)
10,232,590
10,232,590
0.89%
0.97%
May 12, 2028
Beijing Yuhetai
985,000
985,000
0.09%
0.09%
May 12, 2027
CICC Kangrui
72,533,330
50,773,331
6.29%
4.82%
May 12, 2027
PICC Health & Pension 
Fund
50,324,060
50,324,060
4.37%
4.78%
May 12, 2027
Evolution Holding
31,916,730
31,916,730
2.77%
3.03%
May 12, 2027
HSG Seed I
43,420,100
43,420,100
3.77%
4.12%
May 12, 2027
LS Metis
43,225,210
43,225,210
3.75%
4.11%
May 12, 2027
Martis Fund
42,616,430
42,616,430
3.70%
4.05%
May 12, 2027
XtalPi
32,146,460
32,146,460
2.79%
3.05%
May 12, 2027
CICC Healthcare
36,266,670
25,386,669
3.15%
2.41%
May 12, 2027
Jiequan Chengda
35,025,550
35,025,550
3.04%
3.33%
May 12, 2027
Matrice Capital
30,620,100
30,620,100
2.66%
2.91%
May 12, 2027
Duckling Fund
29,771,710
29,771,710
2.58%
2.83%
May 12, 2027
FreeS
27,235,920
27,235,920
2.36%
2.59%
May 12, 2027

<<<PAGE 15>>>
15
Name
Number of 
Shares held in 
the Company 
subject to
lock-up 
undertakings 
upon Listing
Number of H 
Shares held in 
the Company 
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
% of total 
issued H 
shares after 
the Global 
Offering
upon Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Last day 
subject to 
the lock-up 
undertakings
HSG Venture VIII
22,138,560
22,138,560
1.92%
2.10%
May 12, 2027
Guangzhou CMB
16,251,850
16,251,850
1.41%
1.54%
May 12, 2027
Vibrant Evolution
13,547,240
13,547,240
1.18%
1.29%
May 12, 2027
IMO Global
6,094,450
6,094,450
0.53%
0.58%
May 12, 2027
Chia Tai Pharmaceutical 
Group Investment Co., 
Limited
8,051,850
8,051,850
0.70%
0.76%
May 12, 2027
Kunshan Fengrui
7,734,860
7,734,860
0.67%
0.73%
May 12, 2027
YUAN BEN CHEN XING
7,236,680
7,236,680
0.63%
0.69%
May 12, 2027
Monolith
6,773,620
6,773,620
0.59%
0.64%
May 12, 2027
Chengdu Fengrui
5,366,960
5,366,960
0.47%
0.51%
May 12, 2027
Tianjin Taixi
4,064,170
4,064,170
0.35%
0.39%
May 12, 2027
Yael Capital
2,616,850
2,616,850
0.23%
0.25%
May 12, 2027
Taiping GBA
2,417,780
2,417,780
0.21%
0.23%
May 12, 2027
Yael Evergreen
2,415,560
2,415,560
0.21%
0.23%
May 12, 2027
Nanjing CMB
1,260,920
1,260,920
0.11%
0.12%
May 12, 2027
Shanghai Ziyuan
875,640
875,640
0.08%
0.08%
May 12, 2027
Alaya Capital Partners 
Limited
25,155,100
25,155,100
2.18%
2.39%
May 12, 2027
Beijing Medical and Health
25,734,780
25,734,780
2.23%
2.44%
May 12, 2027
Beijing Daxing
19,301,080
19,301,080
1.67%
1.83%
May 12, 2027
AHI Investment
6,386,010
6,386,010
0.55%
0.61%
May 12, 2027
Notes:
1. 
Scientia HK Limited, a private company limited by shares incorporated on February 17, 2023, which is 
wholly owned by Dr. Lai.
2. 
As of the date of this announcement, Delos Holding was controlled by Dr. Lai as to approximately 38.57% 
and the remaining 61.43% equity interests were held by the relevant grantees under the 2023 Equity Incentive 
Plan, none of whom holds 30% or more of the equity interests therein.
3. 
As of the date of this announcement, Dechi Holding was owned as to (i) 3.91% by Dr. Lai; (ii) 44.82% by Dr. 
Alan Fu; (iii) 34.04% by Mr. Mark Robert Herbert; and (iv) 17.23% by three consultants of our Company. 
Dr. Lai controlled Dechi Holding through the only one management share he held and he is also responsible 
for the day-to-day decision making of Dechi Holding.

<<<PAGE 16>>>
16
Cornerstone Investors
Name
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings
upon Listing
% of total issued 
Shares after the 
Global Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject to 
the lock-up
undertakings (Note 1)
BlackRock
37,304,500
3.24%
November 12, 2026
UBS AM Singapore
11,191,000
0.97%
November 12, 2026
China Venture Capital 
Innovation Investment Fund 
Co., Ltd.
7,460,500
0.65%
November 12, 2026
Mirae
5,968,500
0.52%
November 12, 2026
HHLRA
5,968,500
0.52%
November 12, 2026
Deerfield
3,730,000
0.32%
November 12, 2026
RTW Funds
3,730,000
0.32%
November 12, 2026
Arc Avenue
3,730,000
0.32%
November 12, 2026
Huadeng Technology
3,730,000
0.32%
November 12, 2026
Isometry Global
3,730,000
0.32%
November 12, 2026
GF Fund
3,730,000
0.32%
November 12, 2026
ICBCUBS Entities
3,730,000
0.32%
November 12, 2026
China AMC (HK)
3,730,000
0.32%
November 12, 2026
Fullgoal Fund
3,730,000
0.32%
November 12, 2026
Lake Bleu
2,984,000
0.26%
November 12, 2026
Sage Partners
2,984,000
0.26%
November 12, 2026
ICBC Wealth Management
1,492,000
0.13%
November 12, 2026
ORIX Asia AM
1,492,000
0.13%
November 12, 2026
Note:
1. 
In accordance with the relevant cornerstone investment agreements, the required lock-up periods will end on 
November 12, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or transferring 
the H Shares subscribed for pursuant to the relevant cornerstone investment agreements after the indicated 
date.

<<<PAGE 17>>>
17
PLACEE CONCENTRATION ANALYSIS
Placees
Number of H
Shares allotted
Allotment as %
of International
Offering
(assuming the
Over-allotment
Option is not
exercised)
Allotment as %
of International
Offering
(assuming the
Over-allotment
Option is fully
exercised)
Allotment as
% of total
Offer Shares
(assuming the
Over-allotment
Option is not
exercised)
Allotment as
% of total
Offer Shares
(assuming the
Over-allotment
Option is fully
exercised)
Number of 
Shares held
upon Listing
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
37,304,500
23.17%
19.51%
18.54%
16.12%
37,304,500
3.24%
3.15%
Top 5
67,893,000
42.17%
35.52%
33.74%
29.34%
67,893,000
5.89%
5.74%
Top 10
89,157,000
55.38%
46.64%
44.31%
38.53%
166,577,550
14.45%
14.08%
Top 25
136,903,500
85.04%
71.61%
68.03%
59.16%
214,324,050
18.60%
18.12%
Note
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
Allotment 
as % of 
total Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Allotment 
as % of 
total Offer 
Shares 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
Number 
of H Shares 
held upon 
Listing
% of total 
issued 
H share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total 
issued 
H share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
Top 1
0
0.00%
0.00%
0.00%
0.00%
224,825,881
21.35%
20.76%
19.51%
19.01%
Top 5
3,730,500
2.32%
1.95%
1.85%
1.61%
492,987,241
46.82%
45.52%
42.77%
41.68%
Top 10
41,035,000
25.49%
21.47%
20.39%
17.73%
705,230,161
66.98%
65.11%
61.19%
59.63%
Top 25
77,108,000
47.90%
40.34%
38.32%
33.32%
921,338,161
87.50%
85.06%
79.94%
77.90%
Note
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 18>>>
18
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
Number of 
H Shares 
allotted
Allotment 
as %of 
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
Allotment as
% of total
Offer Shares
(assuming the
Over-allotment
Option is fully
exercised)
Number of H
Shares held
upon Listing
Number of
Shares held
upon Listing
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
0
0.00%
0.00%
0.00%
0.00%
224,825,881
291,773,620
25.32%
24.67%
Top 5
3,730,500
2.32%
1.95%
1.85%
1.61%
492,987,241
592,574,980
51.42%
50.10%
Top 10
41,035,000
25.49%
21.47%
20.39%
17.73%
705,230,161
804,817,900
69.83%
68.05%
Top 25
77,108,000
47.90%
40.34%
38.32%
33.32%
921,338,161
1,020,925,900
88.58%
86.32%
Note
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 19>>>
19
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
METIS TECHBIO CO., LTD.
FINAL
BASIS OF ALLOTMENT FOR PRESS ANNOUNCEMENT
NO. OF SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE 
ALLOTTED OF THE 
TOTAL NO. OF
SHARES APPLIED FOR
POOL A
500
93,334
132 out of 93,334 to receive 500 Shares
0.14%
1,000
18,254
52 out of 18,254 to receive 500 Shares
0.14%
1,500
10,141
43 out of 10,141 to receive 500 Shares
0.14%
2,000
19,104
108 out of 19,104 to receive 500 Shares
0.14%
2,500
9,301
66 out of 9,301 to receive 500 Shares
0.14%
3,000
7,928
67 out of 7,928 to receive 500 Shares
0.14%
3,500
3,341
33 out of 3,341 to receive 500 Shares
0.14%
4,000
4,849
55 out of 4,849 to receive 500 Shares
0.14%
4,500
7,406
94 out of 7,406 to receive 500 Shares
0.14%
5,000
11,684
165 out of 11,684 to receive 500 Shares
0.14%
6,000
4,628
79 out of 4,628 to receive 500 Shares
0.14%
7,000
4,081
81 out of 4,081 to receive 500 Shares
0.14%
8,000
8,387
190 out of 8,387 to receive 500 Shares
0.14%
9,000
8,546
218 out of 8,546 to receive 500 Shares
0.14%
10,000
14,292
405 out of 14,292 to receive 500 Shares
0.14%
15,000
10,263
436 out of 10,263 to receive 500 Shares
0.14%
20,000
8,514
482 out of 8,514 to receive 500 Shares
0.14%
25,000
6,592
466 out of 6,592 to receive 500 Shares
0.14%
30,000
5,475
465 out of 5,475 to receive 500 Shares
0.14%
35,000
3,934
390 out of 3,934 to receive 500 Shares
0.14%
40,000
3,937
446 out of 3,937 to receive 500 Shares
0.14%
45,000
3,223
411 out of 3,223 to receive 500 Shares
0.14%
50,000
7,194
1,018 out of 7,194 to receive 500 Shares
0.14%
60,000
4,694
797 out of 4,694 to receive 500 Shares
0.14%
70,000
3,578
709 out of 3,578 to receive 500 Shares
0.14%
80,000
4,111
931 out of 4,111 to receive 500 Shares
0.14%
90,000
3,663
933 out of 3,663 to receive 500 Shares
0.14%
100,000
18,906
5,351 out of 18,906 to receive 500 Shares
0.14%
200,000
12,147
6,876 out of 12,147 to receive 500 Shares
0.14%
300,000
8,069
6,852 out of 8,069 to receive 500 Shares
0.14%
400,000
10,507
500 Shares plus 1,388 out of 10,507 to receive 
additional 500 Shares
0.14%
340,083
Total number of Pool A successful applicants: 38,858

<<<PAGE 20>>>
20
METIS TECHBIO CO., LTD.
FINAL
BASIS OF ALLOTMENT FOR PRESS ANNOUNCEMENT
NO. OF SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE 
ALLOTTED OF THE 
TOTAL NO. OF
SHARES APPLIED FOR
POOL B
500,000
22,231
8,087 out of 22,231 to receive 500 Shares
0.04%
1,000,000
8,076
5,876 out of 8,076 to receive 500 Shares
0.04%
1,500,000
3,977
500 Shares plus 363 out of 3,977 to receive additional 
500 Shares
0.04%
2,000,000
2,363
500 Shares plus 1,075 out of 2,363 to receive 
additional 500 Shares
0.04%
2,500,000
1,455
500 Shares plus 1,192 out of 1,455 to receive 
additional 500 Shares
0.04%
3,000,000
989
1,000 Shares plus 181 out of 989 to receive additional 
500 Shares
0.04%
3,500,000
650
1,000 Shares plus 355 out of 650 to receive additional 
500 Shares
0.04%
4,000,000
949
1,000 Shares plus 864 out of 949 to receive additional 
500 Shares
0.04%
5,030,500
2,536
1,500 Shares plus 1,674 out of 2,536 to receive 
additional 500 Shares
0.04%
43,226
Total number of Pool B successful applicants: 26,882

<<<PAGE 21>>>
21
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and Stock Exchange trading fee payable.
The Directors and the Overall Coordinators confirm that at least 50% of the total number of 
the Offer Shares have been allocated to and taken up by independent price setting investors in 
compliance with Rule 18C.08 of the Listing Rules.
The Directors further confirm that at least 25% of the issued share capital of the Company will be 
held by sophisticated independent investors at the time of Listing in compliance with Chapter 2.5 
of the Guide for New Listing Applicants.
OTHERS/ADDITIONAL INFORMATION
Reallocation
As the Hong Kong Public Offering has been oversubscribed 50 times or more, the reallocation 
as described in the section headed “Structure of the Global Offering — The Hong Kong Public 
Offering — Reallocation and Clawback” of the Prospectus has been applied. As a result of 
the above, the final number of Offer Shares under the Hong Kong Public Offering is adjusted 
to 40,246,000 Shares, representing approximately 20.00% of the total number of Offer Shares 
available under the Global Offering (assuming the Over-allotment Option is not exercised), and the 
final number of Offer Shares under the International Offering is adjusted to 160,983,000 Shares, 
representing approximately 80.00% of the total number of Offer Shares under the Global Offering 
(assuming the Over-allotment Option is not exercised).

<<<PAGE 22>>>
22
Placing to the existing shareholders and/or their close associates with a prior waiver under 
Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the Placing Guidelines
The Company has applied for a waiver under Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules, to permit the existing shareholders and/or its 
close associates to participate as placees in the Global Offering to subscribe for the Offer Shares to 
be issued by the Company under the International Offering (together, the “Existing Shareholder 
Participants”). The Stock Exchange has agreed to grant the requested waiver and consent subject 
to the conditions that:
(a) 
the allocation to the Existing Shareholder Participants will not affect the Company’s ability 
to satisfy its public float requirement under Rule 8.08(1) (as amended and replaced by Rule 
19A.13A) and 18C.08 of the Listing Rules;
(b) 
the Company and the Joint Sponsors confirm that no preferential treatment has been, nor will 
be directly or indirectly, given to the Existing Shareholder Participants as placees by virtue of 
their relationship with the Company in any allocation in the Global Offering, other than the 
preferential treatment of assured entitlement under the cornerstone investment at the Offer 
Price and the terms are substantially the same as other cornerstone investors; and
(c) 
details of the subscription of the Offer Shares by the Existing Shareholder Participants as 
placees under the Global Offering are disclosed in this allotment results announcement of the 
Company.

<<<PAGE 23>>>
23
For details of the allocations of Offer Shares to such Existing Shareholder Participants, please 
refer to the section headed “Allotment Results Details — International Offering — Allottees with 
Waivers/Consents Obtained” in this announcement.
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
Connected Distributor
Connected Client
Relationship with the Connected 
Distributor
Identities of 
the ultimate 
beneficial 
owners of the 
Offer Shares
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
(assuming no 
exercise of the 
Over-allotment 
Option)
Approximate 
percentage 
of total 
issued share 
capital after 
the Global 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Part A — Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties
1.
CLSA Limited 
(“CLSA”) 
CITIC Securities Asset 
Management Company 
Limited (“CITIC Asset 
Management”)
CLSA and CITIC Asset 
Management, are members of the 
same group of companies. 
Please refer to 
Note 1
Yes
1,500
0.0007%
0.0001%
2.
CLSA
CITIC Securities Asset 
Management (HK) Limited 
(“CITIC Securities 
Asset”)
CITIC Securities Asset is a member 
of the same group of companies as 
CLSA.
Please refer to 
Note 2
No
1,500
0.0007%
0.0001%

<<<PAGE 24>>>
24
No.
Connected Distributor
Connected Client
Relationship with the Connected 
Distributor
Identities of 
the ultimate 
beneficial 
owners of the 
Offer Shares
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
(assuming no 
exercise of the 
Over-allotment 
Option)
Approximate 
percentage 
of total 
issued share 
capital after 
the Global 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Part A — Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties
3.
Deutsche Bank AG, 
Hong Kong Branch 
(“DBHK”) 
Harvest Global Investments 
Limited (“Harvest”)
Harvest is a wholly-owned 
subsidiary of Harvest Financial 
Group Limited, which in turn is 
wholly owned by Harvest Fund 
Management Co., Ltd. Harvest 
Fund Management Co., Ltd. is 
30% owned by DWS Investments 
Singapore Limited. DWS 
Investments Singapore Limited 
is a wholly-owned subsidiary 
of DWS Group GmbH & Co. 
KGaA. DWS Group GmbH & 
Co. KGaA is partially owned by 
DB Beteiligungs-Holdings GmbH 
(79.49%), Nippon Life Insurance 
(5%) and outside shareholders 
(15.51 %) as at Dec 31, 2025. DB 
Beteiligungs-Holdings GmbH is 
wholly owned by Deutsche Bank 
AG. 
Please refer to 
Note 3
No
12,000
0.006%
0.001%
4.
DBHK 
DWS Investments Hong 
Kong Limited (“DWS”)
DWS is a wholly-owned subsidiary 
of DWS Group GmbH & Co. 
KGaA. DWS Group GmbH & 
Co. KGaA is partially owned by 
DB Beteiligungs-Holdings GmbH 
(79.49%), Nippon Life Insurance 
(5%) and outside shareholders 
(15.51%) as at December 31, 2025. 
DB Beteiligungs-Holdings GmbH 
is wholly owned by Deutsche Bank 
AG.
Please refer to 
Note 4
No
12,000
0.006%
0.001%

<<<PAGE 25>>>
25
No.
Connected Distributor
Connected Client
Relationship with the Connected 
Distributor
Identities of 
the ultimate 
beneficial 
owners of the 
Offer Shares
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
(assuming no 
exercise of the 
Over-allotment 
Option)
Approximate 
percentage 
of total 
issued share 
capital after 
the Global 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Part A — Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties
5.
The Hongkong And 
Shanghai Banking 
Corporation Limited 
(“HSBC”)
HSBC Global Asset 
Management (Hong Kong) 
Limited (“HSBC AM”)
HSBC AM is a fellow subsidiary of 
HSBC.
Please refer to 
Note 5
No
373,000
0.19%
0.03%
Notes:
1. 
CITIC Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager managing 
the funds on behalf of their investors, each of which is an independent third party.
The funds are as follows: (i) CITIC SECURITIES COMPANY LIMITED-XINHANG ZHIYUAN NO.3(中信証
券信航致遠 3 號集合資產管理計劃), and (ii) CITIC Securities AM-Guibinfengyuan No.118 QDII(中信証券資
管貴賓豐元 118 號 QDII 集合資產管理計劃).
None of the CITIC Asset Management Ultimate Clients holds more than 30% ultimate beneficial interest in the 
aforementioned funds, and all of them with discretionary management.
2. 
CITIC Securities Asset will hold the Offer Shares in its capacity as the discretionary fund manager managing 
the funds on behalf of their investors, each of which is an independent third party. 
The funds is as follows: CITIC Securities Asset Management (HK) Limited – CLSA CT Limited Sub Account 
26. Invested 100% by Roofer Securities Limited, of which UBO holding 30% or more interest is natural person 
Karen Liu.

<<<PAGE 26>>>
26
3. 
Harvest will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on 
behalf of their investors, each of which is an independent third party.
The funds are as follows: (i) HARVEST ESG CHINA A RESEARCH SELECT FUND, (ii) ASIA FRONTIER 
EQUITY FUND, (iii) Harvest BOCHK Diverse Income Fund, (iv) Harvest Total Return Fund, and (v) HGI IPO 
MANDATE NO.1.
No ultimate beneficial owner holds 30% or more interest in the funds.
4. 
DWS will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf 
of their investors, each of which is an independent third party.
The fund is as follows: DWS Invest Chinese Equities.
No ultimate beneficial owner holds 30% or more interest in the funds.
5. 
HSBC AM will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on 
behalf of their investors, each of which is an independent third party.
The funds are as follows: (i) HSBC Global Investment Funds Asia Ex Japan Equity Smaller Companies, (ii) 
HSBC Global Investment Funds Chinese Equity, (iii) HSBC Global Investment Funds Hong Kong Equity, (iv) 
HSBC China Growth Fund, (v) HSBC China Momentum Fund, (vi) HSBC Collective Investment Trust – HSBC 
China Multi-Asset Income Fund, (vii) HSBC China Mother Fund, (viii) HSBC Pooled Investment Fund-HSBC 
Pooled Chinese Equity Fund, (ix) HSBC Pooled Investment Fund – HK HSBC Pooled Hong Kong Equity Fund, 
(x) HSBC Global RAIF Discretionary Asia Equity Next Generation Leaders Portfolio, (xi) HSBC Global RAIF – 
Discretionary Asia Equity Portfolio, and (xii) HSHK Asian Small Caps.
No ultimate beneficial owner holds 30% or more interest in the funds.
No.
Connected 
Distributor
Connected 
Client
Relationship 
with the 
Connected 
Distributor
Identities of the ultimate 
beneficial owners of the Offer 
Shares or, where applicable, 
details of the structured products 
under which the subscription by 
the Connected Client was made 
(e.g. OTC total return swaps)
Whether the 
Connected Client 
is a collective 
investment scheme 
which is not 
authorised by the 
SFC or is expected 
to hold the Offer 
Shares on behalf of 
such scheme
Number of 
Offer Shares 
allocated 
to the 
connected 
client
Approximate 
percentage of total 
number of Offer 
Shares under the 
Global Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Approximate 
percentage of 
total issued share 
capital after the 
Global Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Part B — Connected Client holding the beneficial interest of the Offer Shares on a non-discretionary basis on behalf of independent third parties
1.
CLSA
CITIC Securities 
International Capital 
Management Limited 
(“CSI”)
CSI is a member of 
the same group of 
companies as CLSA.
Please refer to Note 1
No
2,348,500
1.17%
0.20%
Note:
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

<<<PAGE 27>>>
27
The details of the CSI Ultimate Clients are as follows:
Name (CSI Ultimate Client)
Asset Manager
UBO of Asset 
Manager
UBO of CSI 
Ultimate Client
Panjing Wenheng Private Securities Investment 
Fund (盤京聞恒私募證券投資基金)
Shanghai Panjing Investment Management 
Center (Limited Partnership) (上海盤京投資管
理中心(有限合夥))
Zhuang Tao (莊濤)
None
Panjing Wenheng Phase 2 Private Securities 
Investment Fund (盤京聞恒 2 期私募證券投資
基金)
Shanghai Panjing Investment Management 
Center (Limited Partnership) (上海盤京投資管
理中心(有限合夥))
Zhuang Tao (莊濤)
None
Lingding No.3 Private Securities Investment 
Fund (凌頂三號私募證券投資基金)
Ningbo Meishan Bonded Port Area Lingding 
Investment Management Co., Ltd. (寧波梅山
保稅港區凌頂投資管理有限公司)
Chen Youfang 
(陳有方), 
Deng Chunyan 
(鄧春燕)
Xiong Nawei 
(熊納微)
Yuanle Qiangye Private Securities Investment 
Fund (源樂晟強業私募證券投資基金)
Xizang Yuanle Asset Management Co., Ltd. 
(西藏源樂晟資產管理有限公司)
Zeng Xiaojie 
(曾曉潔)
Hu Caiyang 
(胡彩陽)
Canaan China Flagship Fund
Not applicable
Not applicable
Liang Hao
Hover4pi Fund I OFC
Hover4pi Capital Management
He Hui
None
Global Multi Alpha Fund SP
Beevest Capital Management Limited
Zeng Shuzhen
Zeng Shuzhen
Gaoyi Qingrui No.6 Ruixing Fund (高毅慶瑞 6 
號瑞行基金)
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥
企業(有限合夥))
None
None
Gaoyi Liwei Jingxuan Weishi Fund (高毅利偉
精選唯實基金)
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥
企業(有限合夥))
None
None
Gaoyi Renhao Long-term Value Langrun Private 
Securities Investment Fund (高毅任昊長期價值
朗潤私募證券投資基金)
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥
企業(有限合夥))
None
None
Jintaiyang Gaoyi Guolu No.1 Chongyuan Fund 
(金太陽高毅國鷺 1 號崇遠基金)
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥
企業(有限合夥))
None
None
Gaoyi Liwei Xinshi Private Fund (高毅利偉信
實私募基金)
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥
企業(有限合夥))
None
None
Gaoyi Guolu Xinyuan Private Securities 
Investment Fund (高毅國鷺信遠私募證券投資
基金)
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥
企業(有限合夥))
None
None

<<<PAGE 28>>>
28
Name (CSI Ultimate Client)
Asset Manager
UBO of Asset 
Manager
UBO of CSI 
Ultimate Client
Gaoyi Renhao Youxuan Zhifu Private Securities 
Investment Fund (高毅任昊優選致福私募證券
投資基金)
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥
企業(有限合夥))
None
None
Gaoyi Qingrui Youxuan Ruize Private Securities 
Investment Fund (高毅慶瑞優選瑞澤私募證券
投資基金)
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥
企業(有限合夥))
None
None
Gaoyi Qingrui Zhenxuan Fengyuan Private 
Securities Investment Fund (高毅慶瑞臻選灃源
私募證券投資基金)
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥
企業(有限合夥))
None
None
Gaoyi Renhao Jingxuan Chengze Private 
Securities Investment Fund (高毅任昊精選承澤
私募證券投資基金)
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥
企業(有限合夥))
None
None
Gaoyi Renhao Zhenxuan Chunhe Private 
Securities Investment Fund (高毅任昊臻選春和
私募證券投資基金)
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥
企業(有限合夥))
None
None
Gaoyi Qingrui Jingxuan Ruixiang Convertible 
Bond Multi-Strategy Private Fund (高毅慶瑞精
選瑞祥可轉債多策略私募基金)
Shanghai Gaoyi Asset Management Partnership 
(Limited Partnership) (上海高毅資產管理合夥
企業(有限合夥))
None
None
Evolution Darwin Shangshan No.3 Private 
Securities Investment Fund (進化論達爾文上善
三號私募證券投資基金)
Hainan Evolution Asset Management Co., Ltd. 
(海南進化論私募基金管理有限公司)
Wang Yiping 
(王一平)
None
To the best of knowledge of CSI and having made all reasonable inquiries, each of the CSI Ultimate Clients and 
its UBOs is an independent third party of the Company, its subsidiaries, its substantial shareholders, CSI, CLSA 
and the companies which are members of the same group of companies as CLSA.

<<<PAGE 29>>>
29
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
The Offer Shares are being offered and sold (1) solely to qualified institutional buyers as defined 
in Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under 
the U.S. Securities Act and (2) outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act and applicable laws of each jurisdiction where those 
offers and sales occur.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated May 5, 2026 issued by Metis TechBio Co., Ltd. ( 劑
泰科技(北京)股份有限公司) for detailed information about the Global Offering described below 
before deciding whether or not to invest in the Shares thereby being offered.
* 
Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-Overall Coordinators 
(for themselves and on behalf of the Hong Kong Underwriters), may, in their sole and absolute discretion, upon 
giving notice in writing to the Company, terminate the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus at 
any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on May 13, 
2026).

<<<PAGE 30>>>
30
PUBLIC FLOAT AND FREE FLOAT
Pursuant to Rule 19A.13A of the Listing Rules, assuming that the Over-allotment Option is 
not exercised, based on the Offer Price of HK$10.50 per Offer Share, the expected market 
capitalization of the Company upon the Listing is HK$12,101.4 million, and the minimum 
prescribed public float percentage applicable to our Shares is 15%. Immediately after the 
completion of the Global Offering, 828,100,230 H Shares, representing approximately 71.85% of 
the issued share capital of our Company, will count towards the public float, thereby satisfying the 
minimum percentage requirement in compliance with Rule 19A.13A(1) of the Listing Rules.
Based on the Offer Price of HK$10.50 per H Share, the Company satisfies the free float 
requirement under Rule 19A.13C(1)(b) of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering: (i) no 
placee will, individually, be placed more than 10% of the enlarged issued share capital of the 
Company; (ii) there will not be any new substantial Shareholder (as defined in the Listing Rules) 
of the Company; (iii) the three largest public shareholders of the Company do not hold more than 
50% of the H Shares in public hands at the time of the Listing in compliance with Rules 8.08(3) 
and 8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at the time of the 
Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, May 
13, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting — Underwriting Arrangements 
and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade the H Shares on the basis of publicly available allocation 
details prior to the receipt of H Share certificates or prior to the H Share certificates becoming 
valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Wednesday, 
May 13, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Wednesday, May 13, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 500 H Shares each, and the stock code of the H Shares will 
be 7666.
By order of the Board
Metis TechBio Co., Ltd.
Tsai-Ta Lai
Chairman of the Board, executive Director and chief executive officer
Hong Kong, May 12, 2026
Directors of the Company named in the application to which this announcement relates are: (i) Dr. 
Tsai-Ta Lai, Dr. Hongming Chen and Dr. Wenshou Wang as executive Directors; (ii) Mr. Hantao 
Huang and Ms. Yuan Gong as non-executive Directors; and (iii) Mr. Frank Yee Chon Lyn, Dr. Jin 
Li and Dr. Peter Edward Lobie as proposed independent non-executive Directors.
