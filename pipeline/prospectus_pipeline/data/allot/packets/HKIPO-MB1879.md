# 配发结果公告抽取任务：1879.HK Shanghai Xizhi Technology Co., Ltd. - P - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**27/04/2026 22:58**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0427/2026042703526.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1879.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) 
and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as 
those defined in the prospectus dated Monday, April 20, 2026 (the “Prospectus”) of Shanghai Xizhi Technology 
Co., Ltd. (上海曦智科技股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an offer or an invitation to induce an 
offer by any person to acquire, purchase or subscribe for any of the securities of the Company. This announcement 
is not a prospectus. Potential investors should read the Prospectus for detailed information about the Global 
Offering described below before deciding whether or not to invest in the Offer Shares. Any investment decision in 
relation to the Offer Shares should be taken solely in reliance on the information provided in the Prospectus.
This announcement does not constitute an offer to sell or the solicitation of an offer to buy nor shall there be 
any sale of Offer Shares in any jurisdiction in which such offer, solicitation or sales would be unlawful. This 
announcement is not for release, publication or distribution, directly or indirectly, in or into the United States or 
any other jurisdiction where such distribution is prohibited by law, nor is this announcement an offer for sale or 
solicitation to purchase or subscribe for securities in the United States or any other jurisdictions. The Offer Shares 
have not been and will not be registered under the U.S. Securities Act or any state securities laws in the United 
States and may not be offered, sold, pledged or transferred within the United States or to, or for the account or 
benefit of U.S. persons (as defined in Regulation S under the U.S. Securities Act), except in transactions exempt 
from, or not subject to, the registration requirements of the U.S. Securities Act. The Offer Shares are being offered 
and sold (1) solely to qualified institutional buyers as defined in Rule 144A in reliance on Rule 144A or another 
exemption from, or in a transaction not subject to, registration under the U.S. Securities Act and (2) outside the 
United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities 
Limited, as the stabilizing manager (the “Stabilizing Manager”) (or any person acting for it), on behalf of the 
Underwriters, may over-allocate or effect transactions with a view to stabilizing or supporting the market price 
of the Shares at a level higher than that which might otherwise prevail for a limited period after the Listing 
Date. However, there is no obligation on the Stabilizing Manager (or any person acting for it) to conduct any 
such stabilizing action. Such stabilizing action, if taken, (a) will be conducted at the absolute discretion of the 
Stabilizing Manager (or any person acting for it) and in what the Stabilizing Manager (or any person acting for 
it) reasonably regards as the best interest of our Company, (b) may be discontinued at any time, and (c) is required 
to be brought to an end within 30 days after the last day for lodging applications under the Hong Kong Public 
Offering (which is Saturday, May 23, 2026). Such stabilization action, if taken, may be effected in all jurisdictions 
where it is permissible to do so, in each case in compliance with all applicable laws, rules and regulatory 
requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong 
Kong), as amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the Shares for 
longer than the stabilization period which begins on the Listing Date, and is expected to expire on Saturday, May 
23, 2026, the 30th day after the last day for the lodging of applications under the Hong Kong Public Offering. 
After this date, when no further stabilizing action may be taken, demand for the Shares, and therefore the price of 
the Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out 
in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/
or not resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint Sponsors and the 
Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate 
their obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any 
of the events set out in the section headed “Underwriting — Underwriting Arrangements and Expenses — Hong 
Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong 
time) on the Listing Date (which is currently expected to be on Tuesday, April 28, 2026).

<<<PAGE 2>>>
– 2 –
Shanghai Xizhi Technology Co., Ltd.
上海曦智科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under
the Global Offering
:
13,795,215 H Shares (subject to the Over-
allotment Option)
Number of Hong Kong Offer Shares
:
2,759,055 H Shares (taking into account 
reallocation)
Number of International Offer Shares
:
11,036,160 H Shares (taking into account 
reallocation and subject to the Over-allotment 
Option)
Final Offer Price
:
HK$183.2 per H Share, plus brokerage of 1%, 
SFC transaction levy of 0.0027%, Stock 
Exchange trading fee of 0.00565% and AFRC 
transaction levy of 0.00015% (payable in full 
on application in Hong Kong dollars, subject 
to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
01879
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Overall Coordinator, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners

<<<PAGE 3>>>
– 3 –
SHANGHAI XIZHI TECHNOLOGY CO., LTD.
上海曦智科技股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall 
have the same meanings as those defined in the prospectus dated April 20, 2026 (the 
“Prospectus”) issued by Shanghai Xizhi Technology Co., Ltd. (上海曦智科技股份
有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, Shareholders and prospective investors should be aware that the price 
of the H Shares could move substantially even with a small number of H Shares 
traded and should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
01879
Stock short name
XIZHI TECH-P
Dealings commencement date
28 April 2026*
*  see note at the end of the announcement
Price Information
Final Offer Price
HK$183.2
Offer Price range
HK$166.60 - HK$183.20
Offer Price adjustment exercised
N/A
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the Over-
allotment Option)
13,795,215
Final Number of Offer Shares in Hong Kong Public 
Offering (after reallocation)
2,759,055
Final Number of Offer Shares in International 
Offering (after reallocation and before exercise of the 
Over-allotment Option)
11,036,160
Number of issued shares upon Listing (before exercise 
of the Over-allotment Option)
91,968,097

<<<PAGE 4>>>
– 4 –
Over-allocation
No. of Offer Shares over-allocated
2,069,280
Such over-allocation may be covered by exercising the Over-allotment Option or by 
making purchases in the secondary market at prices that do not exceed the Offer Price 
or through deferred delivery or a combination of these means. In the event the Over-
allotment Option is exercised, an announcement will be made on the Stock Exchange’s 
website.
Proceeds
Gross proceeds (Note)
HK$2,527.3 million
Less: Estimated listing expenses payable based on 
Final Offer Price
HK$(150.4) million
Net proceeds
HK$2,376.9 million
Note: Gross proceeds refer to the amount to which the issuer is entitled receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if any) 
for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus on a 
pro rata basis.

<<<PAGE 5>>>
– 5 –
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
378,085
No. of successful applications
134,609
Subscription level
5,784.70 times
Claw-back triggered
Yes
No. of Offer Shares initially available under the Hong 
Kong Public Offering
689,775
No. of Offer Shares reallocated from the International 
Offering (claw-back)
2,069,280
Final no. of Offer Shares under the Hong Kong Public 
Offering (after reallocation)
2,759,055
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering
20.00%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by name or identification number or www.hkeipo.hk/IPOResult for 
the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
327
Subscription Level
53.83 times
No. of Offer Shares initially available under the 
International Offering
13,105,440
No. of Offer Shares reallocated to the Hong Kong Public 
Offering (claw-back)
2,069,280
Final no. of Offer Shares under the International 
Offering (after reallocation)
11,036,160
% of Offer Shares under the International Offering to the 
Global Offering
80.00%
The Directors confirm that, to the best of their knowledge, information and belief, save for 
a waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted 
by the Stock Exchange to permit the Company to allocate certain Offer Shares in the 
International Offering to close associates of existing shareholders as a cornerstone investor 
and a placee, (i) none of the Offer Shares subscribed by the placees and the public have 
been financed directly or indirectly by the Company, any of the Directors, chief executive of 
the Company, Single Largest Shareholders, substantial shareholders, existing shareholders 
of the Company or any of its subsidiaries or their respective close associates; and (ii) none 
of the placees and the public who have purchased the Offer Shares are accustomed to taking 
instructions from the Company, any of the Directors, chief executive of the Company, Single 
Largest Shareholders, substantial shareholders, existing shareholders of the Company or 
any of its subsidiaries or their respective close associates in relation to the acquisition, 
disposal, voting or other disposition of Shares registered in his/her/its name or otherwise 
held by him/her/it.

<<<PAGE 6>>>
– 6 –
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of Offer 
Shares allocated
% of Offer 
Shares  
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing 
shareholders 
or their close 
associates
Alibaba Investment
1,111,680
8.06%
1.49%
1.21%
No
GIC
855,135
6.20%
1.14%
0.93%
No
Baillie Gifford
641,355
4.65%
0.86%
0.70%
No
BlackRock
641,355
4.65%
0.86%
0.70%
No
Fidelity International
641,355
4.65%
0.86%
0.70%
No
Schroders
641,355
4.65%
0.86%
0.70%
No
Temasek
641,355
4.65%
0.86%
0.70%
No
CM Shanghai Fund
624,240
4.53%
0.83%
0.68%
Yes
HHLRA FUNDS
427,560
3.10%
0.57%
0.46%
No
UBS AM
427,560
3.10%
0.57%
0.46%
No
3W Fund
427,560
3.10%
0.57%
0.46%
No
Aspex
427,560
3.10%
0.57%
0.46%
No
CPE Fir
213,780
1.55%
0.29%
0.23%
No
Greenwoods
213,765
1.55%
0.29%
0.23%
No — HK 
Greenwoods 
Yes — Shanghai 
Greenwoods and 
CICC FT (in 
connection with 
Greenwoods 
OTC Swaps)
GF Fund
213,765
1.55%
0.29%
0.23%
No
Lenovo
213,780
1.55%
0.29%
0.23%
No
Mirae Asset Securities HK
213,780
1.55%
0.29%
0.23%
No
ZTE HK
183,855
1.33%
0.25%
0.20%
No
ICBC Wealth
106,890
0.77%
0.14%
0.12%
No
Ping An AM
106,890
0.77%
0.14%
0.12%
No
Total
8,974,575
65.06%
12.00%
9.76%
Notes:
1.	
For further details of the cornerstone investors, please refer to the section headed “Cornerstone Investors” 
of the Prospectus.

<<<PAGE 7>>>
– 7 –
Allottees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares allocated
% of Offer 
Shares 
(assuming the  
Over-allotment 
Option is not 
exercised)
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Relationship
Allotees with waiver from strict compliance with the requirements under Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by existing minority shareholders(Note1)
Cornerstone Investors
CM Shanghai Fund
624,240
4.53%
0.83%
0.68%
A cornerstone 
investor and an 
existing minority 
shareholder
CICC FT (in connection with 
Greenwoods OTC Swaps)
179,505
1.30%
0.24%
0.20%
A cornerstone 
investor, a close 
associate of an 
existing minority 
shareholder and 
a connected 
client
Placees
Tembusu Limited
5,445
0.04%
0.01%
0.01%
A placee and a 
close associate 
of an existing 
minority 
shareholder
HCEP Master Fund and HCEP 
Long Only Master Fund
1,275
0.01%
0.002%
0.001%
A placee and a 
close associate 
of an existing 
minority 
shareholder
China Venture Capital 
Innovation Private Fund 
Management Co., Ltd. (國風投
創新私募基金管理有限公司)
272,925
1.98%
0.36%
0.30%
A placee and a 
close associate 
of an existing 
minority 
shareholder

<<<PAGE 8>>>
– 8 –
Investor
No. of Offer 
Shares allocated
% of Offer 
Shares 
(assuming the  
Over-allotment 
Option is not 
exercised)
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Relationship
Fortera International (Hong 
Kong) Limited (孚騰國際(香港)
有限公司)
27,285
0.20%
0.04%
0.03%
A placee and a 
close associate 
of an existing 
minority 
shareholder
VVC Technology Fund Ltd.
1,275
0.01%
0.002%
0.001%
A placee and a 
close associate 
of an existing 
minority 
shareholder
Daohe Chengguang Private 
Securities Investment Fund  
(道合承光私募證券投資基金)
42,750
0.31%
0.06%
0.05%
A placee and a 
close associate 
of an existing 
minority 
shareholder
Casstar Technology Venture 
Capital Co., Ltd. (中科創星科技
投資有限公司)
1,275
0.01%
0.002%
0.001%
A placee and a 
close associate 
of an existing 
minority 
shareholder
Red Earth Innovation 
International Company Limited
1,275
0.01%
0.002%
0.001%
A placee and a 
close associate 
of an existing 
minority 
shareholder
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants 
in relation to allocations to connected clients(Note2)
CICC Financial Trading Limited 
(“CICC FT”)
9,120
0.07%
0.01%
0.01%
Connected client 
as each of a 
cornerstone (in 
connection with 
Greenwoods 
OTC Swaps) and 
a placee
Also a close 
associate of an 
existing minority 
shareholder

<<<PAGE 9>>>
– 9 –
Investor
No. of Offer 
Shares allocated
% of Offer 
Shares 
(assuming the  
Over-allotment 
Option is not 
exercised)
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Relationship
Guotai Junan Investments (Hong 
Kong) Limited (“GTJAI”)
2,115
0.02%
0.003%
0.003%
Connected client 
as a placee
CITIC Securities International 
Capital Management Limited 
(“CSI Capital”)
105
0.0008%
0.0001%
0.0001%
Connected client 
as a placee
Huatai Capital Investment 
Limited (“HTCI”)
42,750
0.31%
0.06%
0.05%
Connected client 
as a placee
China Galaxy International 
Investment Company Limited 
(“CGII”)
210
0.002%
0.0003%
0.0002%
Connected client 
as a placee
Fullgoal Fund Management Co., 
Ltd. (“Fullgoal Fund”)
9,885
0.07%
0.01%
0.01%
Connected client 
as a placee
Fullgoal Asset Management 
(HK) Limited (“Fullgoal AM”)
2,940
0.02%
0.004%
0.003%
Connected client 
as a placee
Haitong International Asset 
Management (HK) Limited 
(“Haitong AM”)
60
0.0004%
0.00008%
0.00007%
Connected client 
as a placee
China Asset Management (Hong 
Kong) Limited (“China AMC 
HK”)
10,680
0.08%
0.01%
0.01%
Connected client 
as a placee
CITIC Securities Asset 
Management (HK) Limited 
(“CITIC AM”)
210
0.002%
0.0003%
0.0002%
Connected client 
as a placee
ICBC UBS Asset Management 
Co., Ltd. (“ICBC UBS”)
9,195
0.07%
0.01%
0.01%
Connected client 
as a placee
ICBC UBS Asset Management 
(International) Company Limited 
(“ICBC UBS International”)
3,630
0.03%
0.005%
0.004%
Connected client 
as a placee
UBS Asset Management 
(Singapore) Ltd. (“UBS AM”)
427,560
3.10%
0.57%
0.46%
Connected client 
as a placee
ICBC Wealth Management Co., 
Ltd. (“ICBC Wealth”)
106,890
0.77%
0.14%
0.12%
Connected client 
as a placee

<<<PAGE 10>>>
– 10 –
Investor
No. of Offer 
Shares allocated
% of Offer 
Shares 
(assuming the  
Over-allotment 
Option is not 
exercised)
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total 
issued share 
capital after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Relationship
China Merchants Fund 
Management Co., Ltd. (“China 
Merchants Fund”)
2,130
0.02%
0.003%
0.002%
Connected client 
as a placee
Bosera Asset Management 
(International) Co Ltd. (“Bosera 
AM”)
10,680
0.08%
0.01%
0.01%
Connected client 
as a placee
China Southern Asset 
Management Co., Ltd. (“China 
Southern”)
10,680
0.08%
0.01%
0.01%
Connected client 
as a placee
HSBC Global Asset Management 
(Hong Kong) Limited (“HSBC 
AM”)
14,955
0.11%
0.02%
0.02%
Connected client 
as a placee
Notes:
1.	
See “Waivers — Waiver Under Rule 10.04 and Consent under Paragraph 1C(2) of Appendix F1 to the Listing Rules in respect of Subscriptions of Offer 
Shares by Existing Shareholders and/or its Close Associates as Cornerstone Investors” of the Prospectus and the section headed “Others/Additional 
Information — Placing to the existing shareholders and/or their close associates with a prior waiver under Rule 10.04 of the Listing Rules and consent 
under paragraph 1C(2) of the Placing Guidelines” in this announcement for further details.
2.	
See “Waivers — Consent in respect of the Proposed Subscription of the Offer Shares by a Connected Client” of the Prospectus and the section headed 
“Others/Additional Information — Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines” in this 
announcement for further details.

<<<PAGE 11>>>
– 11 –
LOCK-UP UNDERTAKINGS
Key Persons (as Defined under Rule 18C.14 of the Listing Rules)
Name
Capacity
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
listing
% of total issued 
Shares after the 
Global Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings (Note 6)
Dr. Shen
Founder, executive 
Director, senior 
management, Key R&D 
Staff and a Single Largest 
Shareholder
5,918,128
6.43%
April 27, 2028
LightAI EIP
A Single Largest 
Shareholder
4,350,056
4.73%
April 27, 2028
— Mr. Wang Long (Note 1)
Our executive Director, 
a member of the senior 
management and Key R&D 
Staff
—
—
April 27, 2028
— Dr. Ben Chen (Note 2)
A Key R&D Staff
—
—
April 27, 2028
Mach C
A Single Largest 
Shareholder
3,540,391
3.85%
April 27, 2028
— Mr. Wang Long (Note 3)
Our executive Director, 
a member of the senior 
management and Key R&D 
Staff
—
—
April 27, 2028
Youguang Yihui
Close associate of Dr. 
Shen and a Single Largest 
Shareholder
8,583,458
9.33%
April 27, 2028
— Dr. Shen (Note 4)
Founder, executive 
Director, senior 
management, Key R&D 
Staff and a Single Largest 
Shareholder
—
—
April 27, 2028
— Dr. Meng Huaiyu (Note 4)
Our executive Directors, 
a member of the senior 
management and Key R&D 
Staff
—
—
April 27, 2028
— Mr. Zhang Hong (Note 4)
Our executive Director, 
senior management and a 
Single Largest Shareholder
—
—
April 27, 2028

<<<PAGE 12>>>
– 12 –
Name
Capacity
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
listing
% of total issued 
Shares after the 
Global Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings (Note 6)
Youguang Zhiyuan
Close associate of Mr. 
Zhang Hong, one of our 
executive Directors and 
senior management and a 
Single Largest Shareholder
4,780,789
5.20%
April 27, 2028
— Dr. Shen (Note 5)
Founder, executive 
Director, senior 
management, Key R&D 
Staff and a Single Largest 
Shareholder
—
—
April 27, 2028
— Mr. Peng Bo (Note 5)
A Key R&D Staff
—
—
April 27, 2028
— Dr. Meng Huaiyu (Note 5)
Our executive Directors, 
a member of the senior 
management and Key R&D 
Staff
—
—
April 27, 2028
— Mr. Zhang Hong (Note 5)
Our executive Director, 
senior management and a 
Single Largest Shareholder
—
—
April 27, 2028
Notes:
1.	
Mr. Wang Long is a limited partner with interest of 28.24% in LightAI EIP.
2.	
Dr. Ben Chen is a limited partner with interest of 0.51% in LightAI EIP.
3.	
Mr. Wang Long is a limited partner with interest of 9.68% in Mach C.
4.	
Dr. Shen, Dr. Meng Huaiyu and Mr. Zhang Hong are limited partners with interest of 32.87%, 24.50% and 15.68%, respectively. Youguang Shuoran 
is the general partner of Youguang Yihui with a partnership interest of 0.001% and is held by Dr. Shen, Dr. Meng Huaiyu and Mr. Zhang Hong as to 
80%, 10% and 10%, respectively.
5.	
For details of relevant interests in Youguang Zhiyuan, please refer to the section headed “History, Development and Corporate Structure — Share 
Incentive Platforms” in the Prospectus.
6.	
The lock-up period commences on the date by reference to which disclosure of its shareholding is made in the Prospectus and ends on the date which 
is 24 months from the Listing Date, i.e. April 27, 2028. In the event that upon the notification by the Stock Exchange that the Company will no longer 
be regarded as a Pre-Commercial Company after the Listing, the lock-up period will expire on the later of: (i) the date on which such lock-up periods 
would have ended if the Company had applied for listing as a Commercial Company; and (ii) the date falling on the 30th day after the announcement 
on the removal of designation as a Pre-Commercial Company as required under Rule 18C.24 of the Listing Rules.

<<<PAGE 13>>>
– 13 –
Pathfinder SIIs
Name Note 1
Capacity
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
% of total issued 
Shares after the 
Global Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings (Note 1)
MPC V L.P.
Pathfinder SIIs
3,532,177
3.84%
April 27, 2027
MPC V-A L.P.
Pathfinder SIIs
367,334
0.40%
April 27, 2027
Tencent Mobility Limited
Pathfinder SIIs
3,272,298
3.56%
April 27, 2027
Shanghai CM Digital 
Transformation Investment 
Fund, L.P.
Pathfinder SIIs
2,995,570
3.26%
April 27, 2027
Hangzhou Yihong Equity 
Investment Partnership 
(Limited Partnership)
Pathfinder SIIs
2,410,263
2.62%
April 27, 2027
Note:
1.	
In accordance with Rule 18C.14 of the Listing Rules, the required lock-up period commences on the date 
by reference to which disclosure of its shareholding is made in the Prospectus and ends on the date which 
is 12 months from the Listing Date, i.e. April 27, 2027. In the event that upon the notification by the 
Stock Exchange that the Company will no longer be regarded as a Pre-Commercial Company after the 
Listing, the lock-up period will expire on the later of: (i) the date on which such lock-up periods would 
have ended if the Company had applied for listing as a Commercial Company; and (ii) the date falling 
on the 30th day after the announcement on the removal of designation as a Pre-Commercial Company as 
required under Rule 18C.24 of the Listing Rules.

<<<PAGE 14>>>
– 14 –
Single Largest Shareholders
Name Note 1
Capacity
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
% of total issued 
Shares after the 
Global Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings (Note 1)
Dr. Shen
Beneficial Interest
5,918,128
6.43%
April 27, 2028
Youguang Yihui
Beneficial Interest
8,583,458
9.33%
April 27, 2028
Youguang Zhiyuan
Beneficial Interest
4,780,789
5.20%
April 27, 2028
LightAI EIP
Beneficial Interest
4,350,056
4.73%
April 27, 2028
Mach C
Beneficial Interest
3,540,391
3.85%
April 27, 2028
Notes:
1.	
The lock-up period commences on the date by reference to which disclosure of its shareholding is made in the Prospectus and ends on the date which 
is 24 months from the Listing Date, i.e. April 27, 2028. In the event that upon the notification by the Stock Exchange that the Company will no longer 
be regarded as a Pre-Commercial Company after the Listing, the lock-up period will expire on the later of: (i) the date on which such lock-up periods 
would have ended if the Company had applied for listing as a Commercial Company; and (ii) the date falling on the 30th day after the announcement 
on the removal of designation as a Pre-Commercial Company as required under Rule 18C.24 of the Listing Rules.
2.	
For illustrative purposes only, this subsection lists only those members of the Single Largest Shareholders who hold Shares directly in the Company. 
Pursuant to Rule 10.07 of the Listing Rules, each member of the Single Largest Shareholders (namely, Dr. Shen, Youguang Yihui, Youguang Shuoran 
Youguang Zhiyuan, Youguang Yuning, Mr. Zhang Hong, LightAI EIP, Deep Harbor Limited, Foong Jun Zhe and Mach C) has undertaken to the Stock 
Exchange and the Company that, except in connection with the Global Offering (including the Over-allotment Option), he, she or it shall, and shall 
procure that the relevant registered holders of the Shares in which he, she or it is beneficially interested shall, comply with the applicable lock-up 
requirements. For further details, please refer to the section headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong 
Public Offering — Undertakings given to the Stock Exchange pursuant to the Listing Rules — By Our Single Largest Shareholders” in the Prospectus.

<<<PAGE 15>>>
– 15 –
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
issued Shares 
after the Global 
Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total 
issued H shares 
after the Global 
Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings
Dr. Shen
5,918,128
2,959,064
6.43%
7.91%
April 27, 2028
Youguang Yihui
8,583,458
4,291,729
9.33%
11.48%
April 27, 2028
Youguang Zhiyuan
4,780,789
2,390,395
5.20%
6.39%
April 27, 2028
LightAI EIP Holdings LP
4,350,056
4,350,056
4.73%
5.82%
April 27, 2028
Mach C
3,540,391
3,540,391
3.85%
4.73%
April 27, 2028
Ha Wai Kwan Benjamin
3,045,519
913,656
3.31%
4.07%
April 27, 2027
Photon Technology Investment 
VI LPF
1,188,185
1,188,185
1.29%
1.59%
April 27, 2027
MPC V L.P.
3,532,177
3,532,177
3.84%
4.72%
April 27, 2027
MPC V-A L.P.
367,334
367,334
0.40%
0.49%
April 27, 2027
Tencent Mobility Limited
3,272,298
3,272,298
3.56%
4.38%
April 27, 2027
Shanghai CM Digital 
Transformation Investment 
Fund, L.P. (上海中移數字轉型
產業私募基金合夥企業(有限
合夥))
2,995,570
2,995,570
3.26%
4.01%
April 27, 2027
Global Bridge Capital USD 
Fund I, L.P.
2,833,712
2,833,712
3.08%
3.79%
April 27, 2027
Huzhou Jingxin Equity 
Investment Partnership 
Enterprise (Limited 
Partnership) (湖州景鑫股權投
資合夥企業(有限合夥))
2,579,630
2,579,630
2.80%
3.45%
April 27, 2027
Hangzhou Yihong Equity 
Investment Partnership 
(Limited Partnership) (杭州毅
鴻股權投資合夥企業(有限合
夥))
2,410,263
2,410,263
2.62%
3.22%
April 27, 2027
Lumina Orbis (HK) Limited
1,197,448
1,197,448
1.30%
1.60%
April 27, 2027
Lumistar VI, L.P.
399,149
399,149
0.43%
0.53%
April 27, 2027

<<<PAGE 16>>>
– 16 –
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
issued Shares 
after the Global 
Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total 
issued H shares 
after the Global 
Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings
Xiamen Yaheng Venture 
Capital Fund Partnership 
(Limited Partnership) (廈門雅
恒創業投資基金合夥企業(有
限合夥))
766,930
766,930
0.83%
1.03%
April 27, 2027
Beijing Casstar Key & Core 
Technology Venture Capital 
Investment L.P. (北京中科創
星硬科技創業投資合夥企業 
(有限合夥))
1,240,590
0
1.35%
1.66%
April 27, 2027
Shaanxi Advanced OEIC 
Technologies L.P. (陝西先導
光電集成科技投資合夥企業 
(有限合夥))
971,559
0
1.06%
1.30%
April 27, 2027
Shanghai Guofu Linghang 
Investment Partnership 
(Limited Partnership) (上海國
孚領航投資合夥企業)
2,004,433
1,002,217
2.18%
2.68%
April 27, 2027
Hangzhou Yuanli Phase 
III Equity Investment 
Partnership Enterprise (Limited 
Partnership) (杭州元利三期股
權投資合夥企業(有限合夥))
1,341,046
1,341,046
1.46%
1.79%
April 27, 2027
Chongqing Yuanhong Private 
Equity Investment Fund 
Partnership Enterprise (Limited 
Partnership) (重慶元弘私募股
權投資基金合夥企業(有限合
夥))
590,692
590,692
0.64%
0.79%
April 27, 2027
Nanjing Jiangbei Jiakang 
Technology Venture Capital 
Partnership (Limited 
Partnership) (南京江北佳康科
技創業投資合夥企業)
1,860,674
1,860,674
2.02%
2.49%
April 27, 2027

<<<PAGE 17>>>
– 17 –
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
issued Shares 
after the Global 
Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total 
issued H shares 
after the Global 
Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings
CICC Culture and Consumption 
Industry Equity Investment 
Fund (Xiamen) Partnership 
(Limited Partnership) (中金文
化消費產業股權投資基金(廈
門)合夥企業)
1,686,673
1,686,673
1.83%
2.26%
April 27, 2027
Nanjing Heli Guoxin 
Zhixin Equity Investment 
Partnership Enterprise (Limited 
Partnership) (南京和利國信智
芯股權投資合夥企業)
1,676,817
1,676,817
1.82%
2.24%
April 27, 2027
Vertex Ventures China IV, L.P.
1,619,264
1,619,264
1.76%
2.17%
April 27, 2027
Guanzi Equity Investment 
(Lishui) Partnership Enterprise 
(Limited Partnership) (關子股
權投資(麗水)合夥企業)
1,596,598
1,596,598
1.74%
2.14%
April 27, 2027
P7 China Holdings PCC 
Limited (acting solely in 
respect of the P7CH Direct P7 I 
cell)
1,596,598
1,596,598
1.74%
2.14%
April 27, 2027
Gongqingcheng Yachang 
Chenning Equity Investment 
Partnership Enterprise (Limited 
Partnership) (共青城亞昌辰檸
股權投資合夥企業(有限合夥))
344,880
0
0.37%
0.46%
April 27, 2027
Gongqingcheng Yachang 
Hongshuo Equity Investment 
Partnership Enterprise (Limited 
Partnership) (共青城亞昌宏
碩股權投資合夥企業(有限合
夥))
344,880
0
0.37%
0.46%
April 27, 2027

<<<PAGE 18>>>
– 18 –
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
issued Shares 
after the Global 
Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total 
issued H shares 
after the Global 
Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings
Jiangsu Qianquan Yuanhe 
Origin Intelligence No. 3 
Venture Capital Partnership 
Enterprise (Limited 
Partnership) (江蘇疌泉元禾原
點智能三號創業投資合夥企
業(有限合夥))
1,195,098
1,195,098
1.30%
1.60%
April 27, 2027
Shanghai Sci-Tech 
Innovation Center Capital 
Fund I Partnership (Limited 
Partnership) (上海科創中心壹
號股權投資基金合夥企業(有
限合夥))
1,089,826
544,913
1.19%
1.46%
April 27, 2027
Shanghai Pudong Pilot Zone 
Investment Fund (Limited 
Partnership) (上海浦東引領區
投資中心(有限合夥))
1,002,216
1,002,216
1.09%
1.34%
April 27, 2027
FreeS International Holdings 
(Hong Kong) Limited
812,609
812,609
0.88%
1.09%
April 27, 2027
Beijing Biwei Original 
Innovation Consulting Center 
(L.P.) (北京百度畢威企業管
理中心(有限合夥))
791,028
791,028
0.86%
1.06%
April 27, 2027
Wuhan Changfei Science 
and Technology Innovation 
Industry Fund Partnership 
Enterprise (Limited 
Partnership) (武漢長飛科創產
業基金合夥企業(有限合夥))
706,954
141,390
0.77%
0.95%
April 27, 2027
Pi Holdings Limited
607,223
607,223
0.66%
0.81%
April 27, 2027
Zhen Partners IV (HK) Limited
485,821
485,821
0.53%
0.65%
April 27, 2027
Ginkgo Capital Global Fund 
SPC-XtalPi AI Fund SP
286,196
286,196
0.31%
0.38%
April 27, 2027

<<<PAGE 19>>>
– 19 –
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
issued Shares 
after the Global 
Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total 
issued H shares 
after the Global 
Offering 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings
Shenzhen Shengxingyu 
Investment Partnership 
Enterprise (Limited Partnership 
(深圳盛杏鈺投資合夥企業(有
限合夥)
198,016
198,016
0.22%
0.26%
April 27, 2027
Morningside TMT Holding IV 
Limited
434,223
434,223
0.47%
0.58%
April 27, 2027
JIANGSU HOTLAND 
INTELLIGENT VENTURE 
INVESTMENT FUND (L.P.) 
(江蘇疌泉紅土智能創業投資
基金(有限合夥))
210,551
210,551
0.23%
0.28%
April 27, 2027
Shenzhen Capital Group Co., 
Ltd (深圳市創新投資集團有
限公司)
210,551
210,551
0.23%
0.28%
April 27, 2027
China Merchants Venture 
Capital Fund, L.P. (招商局創
新投資基金有限合夥)
404,816
404,816
0.44%
0.54%
April 27, 2027
Shaanxi Chuangfa Chuangxing 
Photon Venture Capital 
Partnership Enterprise (Limited 
Partnership) (陝西川發創星光
子創業投資合夥企業(有限合
夥))
399,149
0
0.43%
0.53%
Newlight Fund I LP
117,701
117,701
0.13%
0.16%
April 27, 2027
Shenzhen Dezhixi Information 
Consulting Co., LTD (深圳市
德之曦信息諮詢有限公司)
334,379
334,379
0.36%
0.45%
April 27, 2027
Tai You Fund I, LP
250,784
250,784
0.27%
0.34%
April 27, 2027

<<<PAGE 20>>>
– 20 –
Cornerstone Investors
Name
Number of Shares held in 
the Company subject to 
lock-up undertakings 
upon Listing
% of total issued Shares 
after the Global Offering 
upon Listing (assuming 
the Over-allotment 
Option is not exercised)
Last day subject  
to the lock-up  
undertakings (Note 1)
Alibaba Investment
1,111,680
1.21%
October 27, 2026
GIC
855,135
0.93%
October 27, 2026
Baillie Gifford
641,355
0.70%
October 27, 2026
BlackRock
641,355
0.70%
October 27, 2026
Fidelity International
641,355
0.70%
October 27, 2026
Schroders
641,355
0.70%
October 27, 2026
Temasek
641,355
0.70%
October 27, 2026
CM Shanghai Fund
624,240
0.68%
October 27, 2026
HHLRA FUNDS
427,560
0.46%
October 27, 2026
UBS AM
427,560
0.46%
October 27, 2026
3W Fund
427,560
0.46%
October 27, 2026
Aspex
427,560
0.46%
October 27, 2026
CPE Fir
213,780
0.23%
October 27, 2026
Greenwoods
213,765
0.23%
October 27, 2026
GF Fund
213,765
0.23%
October 27, 2026
Lenovo
213,780
0.23%
October 27, 2026
Mirae Asset Securities HK
213,780
0.23%
October 27, 2026
ZTE HK
183,855
0.20%
October 27, 2026
ICBC Wealth
106,890
0.12%
October 27, 2026
Ping An AM
106,890
0.12%
October 27, 2026
Note:
1.	
In accordance with the relevant cornerstone investment agreements, the required lock-up periods will 
end on October 27, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or 
transferring the H Shares subscribed for pursuant to the relevant cornerstone investment agreements 
after the indicated date.  

<<<PAGE 21>>>
– 21 –
PLACEE CONCENTRATION ANALYSIS
Shareholders
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
Allotment as % of 
total Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
Allotment as % of 
total Offer Shares 
(assuming the 
Over-allotment 
Option is fully 
exercised)
Number of Shares 
held upon Listing
% of total issued 
share capital upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
% of total issued 
share capital upon 
Listing (assuming 
the Over-allotment 
Option is fully 
exercised)
Top 1
1,111,680
10.07%
8.48%
8.06%
7.01%
1,111,680
1.21%
1.18%
Top 5
4,146,795
37.57%
31.64%
30.06%
26.14%
9,552,628
10.39%
10.16%
Top 10
6,925,980
62.76%
52.85%
50.21%
43.66%
12,331,813
13.41%
13.11%
Top 25
10,716,825
97.11%
81.77%
77.69%
67.55%
17,809,331
19.36%
18.94%
Notes
*	
Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 22>>>
– 22 –
H SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders
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
% of total issued 
H share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
H share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised)
% of total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised)
Top 1
897,270
8.13%
6.85%
6.50%
5.66%
6,303,103
8.43%
8.20%
6.85%
6.70%
Top 5
902,715
8.18%
6.89%
6.54%
5.69%
22,390,235
29.94%
29.13%
24.35%
23.81%
Top 10
930,000
8.43%
7.10%
6.74%
5.86%
36,611,570
48.96%
47.64%
39.81%
38.93%
Top 25
3,165,000
28.68%
24.15%
22.94%
19.95%
60,469,430
80.86%
78.68%
65.75%
64.30%
Notes
*	
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 23>>>
– 23 –
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
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
4,291,729
8,583,458
9.33%
9.13%
Top 5
897,270
8.13%
6.85%
6.50%
5.66%
20,294,347
29,935,534
32.55%
31.83%
Top 10
930,000
8.43%
7.10%
6.74%
5.86%
35,690,464
49,010,643
53.29%
52.12%
Top 25
3,166,275
28.69%
24.16%
22.95%
19.96%
59,679,677
75,212,005
81.78%
79.98%
Notes
*	
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 24>>>
– 24 –
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications 
made by the public will be conditionally allocated on the basis set out below:
Pool A
 Number  
 of H Shares 
 applied for 
 Number 
 of valid 
 applications Basis of allocation/ballot
Approximate
percentage
allotted of the
total number of
H Shares applied
for
15
82,860
4,972 out of 82,860 applicants to receive 15 H Shares
6.00%
30
12,417
980 out of 12,417 applicants to receive 15 H Shares
3.95%
45
16,761
1,553 out of 16,761 applicants to receive 15 H Shares
3.09%
60
7,852
815 out of 7,852 applicants to receive 15 H Shares
2.59%
75
6,697
759 out of 6,697 applicants to receive 15 H Shares
2.27%
90
4,552
555 out of 4,552 applicants to receive 15 H Shares
2.03%
105
5,048
654 out of 5,048 applicants to receive 15 H Shares
1.85%
120
4,379
598 out of 4,379 applicants to receive 15 H Shares
1.71%
135
5,773
826 out of 5,773 applicants to receive 15 H Shares
1.59%
150
31,668
4,719 out of 31,668 applicants to receive 15 H Shares
1.49%
300
17,279
3,386 out of 17,279 applicants to receive 15 H Shares
0.98%
450
14,545
3,345 out of 14,545 applicants to receive 15 H Shares
0.77%
600
8,675
2,235 out of 8,675 applicants to receive 15 H Shares
0.64%
750
6,109
1,719 out of 6,109 applicants to receive 15 H Shares
0.56%
900
5,050
1,528 out of 5,050 applicants to receive 15 H Shares
0.50%
1,050
5,423
1,743 out of 5,423 applicants to receive 15 H Shares
0.46%
1,200
4,399
1,491 out of 4,399 applicants to receive 15 H Shares
0.42%
1,350
3,595
1,276 out of 3,595 applicants to receive 15 H Shares
0.39%
1,500
21,700
8,030 out of 21,700 applicants to receive 15 H Shares
0.37%
3,000
14,021
6,822 out of 14,021 applicants to receive 15 H Shares
0.24%
4,500
9,899
5,653 out of 9,899 applicants to receive 15 H Shares
0.19%
6,000
7,080
4,530 out of 7,080 applicants to receive 15 H Shares
0.16%
7,500
5,212
3,642 out of 5,212 applicants to receive 15 H Shares
0.14%
9,000
4,245
3,188 out of 4,245 applicants to receive 15 H Shares
0.13%
10,500
3,752
2,995 out of 3,752 applicants to receive 15 H Shares
0.11%
12,000
3,342
2,812 out of 3,342 applicants to receive 15 H Shares
0.11%
13,500
2,528
2,229 out of 2,528 applicants to receive 15 H Shares
0.10%
15,000
20,584
18,914 out of 20,584 applicants to receive 15 H Shares
0.09%
 
Total
 335,445
Total number of Pool A successful applicants: 91,969
 

<<<PAGE 25>>>
– 25 –
Pool B
 Number  
 of H Shares 
 applied for
 Number 
 of valid 
 applications Basis of allocation/ballot
Approximate
percentage
allotted of the
total number of
H Shares applied
for
30,000
17,593
15 H Shares plus 10,556 out of 17,593 applicants to receive an additional 15 H Shares
0.08%
45,000
6,630
15 H Shares plus 5,854 out of 6,630 applicants to receive an additional 15 H Shares
0.06%
60,000
4,064
30 H Shares
0.05%
75,000
2,732
30 H Shares plus 852 out of 2,732 applicants to receive an additional 15 H Shares
0.05%
90,000
2,039
30 H Shares plus 1,130 out of 2,039 applicants to receive an additional 15 H Shares
0.04%
105,000
1,493
30 H Shares plus 1,090 out of 1,493 applicants to receive an additional 15 H Shares
0.04%
120,000
1,211
30 H Shares plus 1,066 out of 1,211 applicants to receive an additional 15 H Shares
0.04%
135,000
804
30 H Shares plus 746 out of 804 applicants to receive an additional 15 H Shares
0.03%
150,000
3,367
45 H Shares
0.03%
300,000
692
60 H Shares
0.02%
344,880
2,015
60 H Shares plus 836 out of 2,015 applicants to receive an additional 15 H Shares
0.02%
 
Total
42,640
Total number of Pool B successful applicants: 42,640
 

<<<PAGE 26>>>
– 26 –
As of the date of this announcement, the relevant subscription monies previously deposited 
in the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in 
respect of which consent has been obtained, the Company has complied with the Listing 
Rules and guidance materials in relation to the placing, allotment and listing of the H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by 
the placees or the public (as the case may be) directly or indirectly for each Offer Share 
subscribed for or purchased by them was the same as the final Offer Price in addition to any 
brokerage, AFRC transaction levy, SFC transaction levy and trading fee payable.
The Directors and the Overall Coordinators confirm that at least 50% of the total number of 
the Offer Shares have been allocated to and taken up by independent price setting investors 
in compliance with Rule 18C.08 of the Listing Rules.
The Directors further confirm that at least 20% of the issued share capital of the Company 
will be held by sophisticated independent investors at the time of Listing in compliance with 
Chapter 2.5 of the Guide for New Listing Applicants.
OTHERS/ADDITIONAL INFORMATION
Reallocation
As the Hong Kong Public Offering has been oversubscribed 50 times or more, the 
reallocation as described in the section headed “Structure of the Global Offering — The 
Hong Kong Public Offering — Reallocation” of the Prospectus has been applied.
As a result of the above, the final number of Offer Shares under the Hong Kong Public 
Offering is adjusted to 2,759,055 Shares, representing approximately 20.00% of the total 
number of Offer Shares available under the Global Offering (assuming the Over-allotment 
Option is not exercised), and the final number of Offer Shares under the International 
Offering is adjusted to 11,036,160 Shares, representing approximately 80.00% of the total 
number of Offer Shares under the Global Offering (assuming the Over-allotment Option is 
not exercised).

<<<PAGE 27>>>
– 27 –
Placing to the existing shareholders and/or their close associates with a prior waiver 
under Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the 
Placing Guidelines
The Company has applied for a waiver under Rule 10.04 of the Listing Rules and a 
consent under paragraph 1C(2) of Appendix F1 to the Listing Rules, to permit the existing 
shareholders and/or its close associates to participate as either cornerstone investors or 
placees in the Global Offering to subscribe for the Offer Shares to be issued by the Company 
under the International Offering (together, the “Existing Shareholder Participants”). 
The Stock Exchange has agreed to grant the requested waiver and consent subject to the 
conditions that:
(a)	
the allocation to the Existing Shareholder Participants will not affect the Company’s 
ability to satisfy its public float requirement under Rule 8.08(1) (as amended and 
replaced by Rule 19A.13A) and 18C.08 of the Listing Rules;
(b)	 the Company and the Joint Sponsors confirm that no preferential treatment has been, 
nor will be directly or indirectly, given to the Existing Shareholder Participants as 
cornerstone investors or placees by virtue of their relationship with the Company in 
any allocation in the Global Offering, other than the preferential treatment of assured 
entitlement under the cornerstone investment at the Offer Price and the terms are 
substantially the same as other cornerstone investors; and
(c)	
details of the subscription of the Offer Shares by the Existing Shareholder Participants 
as cornerstone investors or placees under the Global Offering have been disclosed 
in the Prospectus, and details of the allocation are disclosed in this allotment results 
announcement of the Company.
For details of the allocations of Offer Shares to such Existing Shareholder Participants, 
please refer to the section headed “Allotment Results Details — International Offering — 
Allotees with Waivers/Consents Obtained” in this announcement.
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of 
their connected distributors pursuant to the Placing Guidelines.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate 
such Offer Shares in the International Offering to the connected clients. The allocation of 
Offer Shares to such connected clients is in compliance with all the conditions under the 
consent granted by the Stock Exchange. Details of the placement to connected clients are set 
out below:

<<<PAGE 28>>>
– 28 –
No.
Connected Distributor
Connected Client
Relationship with the 
Connected Distributor
Identities of the 
ultimate beneficial 
owners of the Offer 
Shares or, where 
applicable, details 
of the structured 
products under which 
the subscription by 
the Connected Client 
was made (e.g. OTC 
total return swaps)
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
Number of Offer 
Shares allocated to the 
connected client
Approximate 
percentage of total 
number of Offer Shares 
under the Global 
Offering (assuming no 
exercise of the Over-
allotment Option)
Approximate 
percentage of total 
issued share capital 
after the Global 
Offering (assuming no 
exercise of the Over-
allotment Option)
Part A — Connected Client holding the beneficial interest of the Offer Shares on a non-discretionary basis on behalf of independent third parties
1.
China International Capital 
Corporation Hong Kong Securities 
Limited (“CICCHKS”)
CICC Financial Trading 
Limited (“CICC FT”)
CICC FT is a member 
of the same group of 
companies as CICCHKS
Please refer to Note 1
No
9,120
0.07%
0.01%
2.
Haitong International Securities 
Company Limited (“HTI”) and 
Guotai Junan Securities (Hong 
Kong) Limited (“GTJAS”)
Guotai Junan Investments 
(Hong Kong) Limited 
(“GTJAI”)
GTJAI is a member of the 
same group of companies 
as HTI and GTJAS
Please refer to Note 2
No
2,115
0.02%
0.002%
3.
CITIC Brokerage HK
CITIC Securities 
International Capital 
Management Limited 
(“CSI Capital”)
CSI Capital is a member 
of the same group of 
companies as CITIC 
Brokerage HK
Please refer to Note 3
No
105
0.0008%
0.0001%
4.
Huatai Financial Holdings (Hong 
Kong) Limited (“HTFH”)
Huatai Capital Investment 
Limited (“HTCI”)
HTCI is a member of the 
same group of companies 
as HTFH.
Please refer to Note 4
No
42,750
0.31%
0.05%
5.
China Galaxy International 
Securities (Hong Kong) Co., 
Limited (“CGIS”)
China Galaxy International 
Investment Company 
Limited (“CGII”)
CGII is a member of the 
same group of companies 
as CGIS
Please refer to Note 5
No
210
0.002%
0.0002%

<<<PAGE 29>>>
– 29 –
Notes:
1.	
CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one OTC swap transactions (the “OTC Swaps”) 
with each other and the ultimate clients (the “CICC FT Ultimate Clients”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary 
basis to hedge the OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed to the CICC FT Ultimate Clients, subject to 
customary fees and commissions. The OTC Swaps will be fully funded by the CICC FT Ultimate Clients. During the terms of the OTC Swaps, all economic 
returns of the Offer Shares subscribed by CICC FT will be passed to the CICC FT Ultimate Clients and all economic loss shall be borne by the CICC FT 
Ultimate Clients through the OTC Swaps, and CICC FT will not take part in any economic return or bear any economic loss in relation to the Offer Shares. 
The OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate Clients may request CICC FT to redeem it at their own discretion, upon which 
CICC FT shall dispose of the Offer Shares and settle OTC Swaps in cash in accordance with the terms and conditions of the OTC Swap. Despite that CICC 
FT will hold the legal title of the Offer Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares during the terms of the OTC 
Swaps according to its internal policy. To the best knowledge, information and belief of CICC FT after due enquiry, the CICC FT Ultimate Clients for purpose 
of this placee subscription include: (i) Wangzheng Gongying No. 17 Private Equity Investment Fund (望正共贏17號私募證券投資基金), managed by 
Shenzhen Wangzheng Asset Management Co., Ltd. (深圳望正資產管理有限公司), whose ultimate beneficial owner holding 30% or more interest is Qu Qin; 
(ii) Wangzheng Jingqi Hanye Jingxuan Private Equity Investment Fund (望正景氣行業精選私募證券投資基金), whose ultimate beneficial owner holding 
30% or more interest is Qu Qin; (iii) Yuanle Chengqiangye Private Equity Investment Fund (源樂晟強業私募證券投資基金), whose ultimate beneficial 
owners holding 30% or more interest are Zeng Xiaojie and Hu Caiyang; (iv) Hengde Yuanzhi Tianli No.3 Private Equity Investment Fund (恒德遠征添利3號
私募證券投資基金), Hengde Jinze No. E49 Private Equity Investment Fund (恒德金澤E49號私募證券投資基金) and Hengde Yuanzhi Tianli No.7 Private 
Equity Investment Fund (恒德遠征添利7號私募證券投資基金), for each of which no ultimate beneficial owner holds 30% or more interest; (v) Pinpoint 
Multi-Strategy Master Fund, whose ultimate beneficial owner holding 30% or more interest is Wang Qiang; (vi) Pinpoint China Fund, whose ultimate 
beneficial owner holding 30% or more interest is Wang Qiang; (vii) Yiyuan Zhizhen No.1 Private Equity Investment Fund (釔遠致臻1號私募證券投資基金), 
whose ultimate beneficial owner holding 30% or more interest is Yang Yucheng; (viii) Yiyuan Canghai No.1 Private Equity Investment Fund (釔遠滄海1號私
募證券投資基金), for which no ultimate beneficial owner holds 30% or more interest; and (ix) Gaoyi Renhao Jingxuan Chengze Private Equity Investment 
Fund (高毅任昊精選承澤私募證券投資基金), Gaoyi Qingrui No.6 Ruixing Fund (高毅慶瑞6號瑞行基金), Gaoyi Qingrui Zhenxuan Fengyuan Private 
Equity Fund (高毅慶瑞臻選灃源私募證券基金) Gaoyi Qingrui Jingxuan Ruixiang Convertible Multi-strategy Private Fund (高毅慶瑞精選瑞祥可轉債多策
略私募基金) and Gaoyi Liwei Selected Weishi Fund (高毅利偉精選唯實基金), for each of which no ultimate beneficial owner holds 30% or more interest.
To the best of CICC FT’s knowledge having made all reasonable inquiries, each of the CICC FT Ultimate Clients is an independent third party of CICC FT, 
CICCHKS and the companies which are members of the same group of companies as CICCHKS.

<<<PAGE 30>>>
– 30 –
2.	
HTI is the Sponsor-Overall Coordinator and GTJAS is a distributor in connection with the Global Offering. GTJAI shall hold the Offer Shares for hedging 
purpose as the single underlying asset of several sets of back-to-back total return swap transaction (the “GTHT Back-to-back TRS”) to be entered into 
between GTJAI and Guotai Haitong Securities Co., Ltd. (the “GTHT Onshore Parent”) in connection with several total return swap orders (the “GTHT 
Client TRS”) to be entered into by GTHT Onshore Parent and several ultimate clients (the “GTHT Onshore Ultimate Clients”), respectively. Such GTHT 
Client TRS is to be fully funded by the GTHT Onshore Ultimate Clients. GTJAI will hold the Offer Shares on a non-discretionary basis for the purpose of 
hedging the economic exposure under the GTHT Back-to-back TRS and GTHT Client TRS only, During the tenor of the GTHT Client TRS, all economic 
returns of the Offer Shares will be passed to the GTHT Onshore Ultimate Clients and all economic losses shall be borne by the GTHT Onshore Ultimate 
Clients, subject to the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS, and GTJAI will not take part in any economic return or 
bear any economic loss in relation to the price of the Offer Shares. The GTHT Onshore Ultimate Clients may request to redeem the Offer Shares at their own 
discretion, upon which GTJAI shall dispose of the Offer Shares and settle the GTHT Back-to-back TRS and GTHT Client TRS in cash in accordance with the 
terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS documents. Due to its internal policy, GTJAI will not exercise the voting right 
attaching to the Offer Shares during the tenor of the GTHT Back-to-back TRS and GTHT Client TRS.
To the best knowledge, information and belief of GTJAI after due enquiry, the GTHT Onshore Ultimate Clients for purpose of this placee subscription include, 
to the best knowledge, information and belief of GTJAI after due enquiry: (i) Lingding No.3 Private Securities Investment Fund (凌頂三號私募證券投資基
金), whose ultimate beneficial owner holding 30% or more interest is Xiong Nawei; (ii) Shidaigongying1 Private Equity Investment Fund (時代共贏1號私
募證券投資基金), whose ultimate beneficial owner holding 30% or more interest is Han Guangyong; (iii) Casstar Technology Venture Capital Co., Ltd. (中
科創星科技投資有限公司), whose ultimate beneficial owner holding 30% or more interest is Mi Lei; (iv) Zhonghe Capital Cultivation 8 Private Securities 
Investment Fund (中和資本耕耘8號私募證券投資基金) and Zhonghe Capital Cultivation 810 Private Securities Investment Fund (中和資本耕耘810號私
募證券投資基金), whose ultimate beneficial owner holding 30% or more interest in each of them is Zhang Jingting; (v) Weining Jujiao Private Securities 
Investment Fund (衛寧聚焦私募證券投資基金), whose ultimate beneficial owner holding 30% or more interest is Wang Zhangyi; (vi) Weining Qihang No. 
3 Private Securities Investment Fund (衛寧啟航3號私募證券投資基金), whose ultimate beneficial owner holding 30% or more interest is Ling Chao; (vii) 
Tongyi Anxin No.2 Private Securities Investment Fund (通怡安鑫2號私募證券投資基金), whose ultimate beneficial owner holding 30% or more interest is 
Huang Shilin; (viii) Tongyi Taoli No.1 Private Securities Investment Fund (通怡桃李1號私募證券投資基金), whose ultimate beneficial owner holding 30% 
or more interest is Wang Jing; and (ix) Tongyi Taoli No.10 Private Securities Investment Fund (通怡桃李10號私募證券投資基金), for which no ultimate 
beneficial owner holds 30% or more interest.

<<<PAGE 31>>>
– 31 –
To the best knowledge of GTJAI and after making all reasonable enquiries, (i) GTJAI has confirmed that, to the best of their knowledge, each of the 
GTHT Onshore Ultimate Clients and the ultimate beneficial owners holding 30% or more interest of the GTHT Onshore Ultimate Clients listed above is 
an independent third party of GTJAI, HTI, GTJAS and the companies which are members of the same group of companies as HTI, and (ii) GTJAI is not a 
collective investment scheme which is not authorised by the SFC nor is expected to hold the Offer Shares on behalf of such scheme.
3.	
CSI Capital proposes to subscribe for and hold the Offer Shares as a placee under the International Offering on behalf of CSI Ultimate Clients, each of them is 
an independent third party, on a non-discretionary basis, pursuant to which:
(i)	
CSI Capital will act as the single counterparty of a back-to-back total return swap transaction (the “CSI Capital Back-to-back TRS”) to be entered 
into by it in connection with a total return swap order (the “CSI Capital Client TRS”) placed and fully funded by the CSI Capital Ultimate Clients, by 
which CSI Capital will pass the full economic exposure of the Offer Shares placed to CSI Capital to the CSI Capital Ultimate Clients.
(ii)	
As confirmed by CSI Capital and CITIC Brokerage HK, CSI Capital will hold the legal title and beneficial interest in the Offer Shares, but will 
contractually agree to pass on the full economic exposure and return of the Offer Shares to the CSI Capital Ultimate Clients, on a non-discretionary 
basis. The CSI Capital Ultimate Clients may exercise their early termination rights to terminate the CSI Capital Client TRS at any time.
(iii)	
Upon the final maturity or termination of the CSI Capital Client TRS by the CSI Capital Ultimate Clients, CSI Capital will dispose of the Offer Shares 
on the secondary market and the CSI Capital Ultimate Clients will receive a final termination amount of the CSI Capital Back-to-back TRS which will 
have taken into account all the economic returns or economic loss in relation to the Offer Shares and the fixed amount of transaction fees of the CSI 
Capital Back-to-back TRS and the CSI Capital Client TRS. Due to its internal policy, CSI Capital will not exercise the voting right of the Offer Shares 
during the terms of the CSI Capital Back-to-back TRS.
To the best knowledge, information and belief of CSI Capital after due enquiry, the CSI Capital Ultimate Clients for purpose of this placee subscription 
include, to the best knowledge, information and belief of CSI Capital after due enquiry: (i) HY Capital Company Limited, whose ultimate beneficial owners 
holding 30% or more interest are Xia Hui and Lu Ang; and (ii) Shanghai Panjing Investment Management Centre (Limited Partnership) (上海盤京投資管理
中心(有限合夥)), whose ultimate beneficial owner holding 30% or more interest is Zhuang Tao.
CSI Capital has confirmed that, to the best of their knowledge and after making all reasonable enquiries, each of the CSI Capital Ultimate Clients and the 
respective ultimate beneficial owners is an independent third party of CSI Capital, CITIC Brokerage HK and the companies which are members of the same 
group of companies as CITIC Brokerage HK.

<<<PAGE 32>>>
– 32 –
4.	
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public offerings (“IPOs”) in Hong Kong. However, PRC 
investors are permitted to invest in products issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. 
In connection with such products, the licensed domestic securities firms, through their Hong Kong affiliates, may participate in Hong Kong IPOs either as 
placees or cornerstone investors (the “Cross-border Derivatives Trading Regime”).
Huatai Securities Co., Ltd. (“Huatai Securities”), the shares of which are listed on both the Shanghai Stock Exchange (stock code: 601688) and the Stock 
Exchange (stock code: 6886), is one of the domestic securities firms licensed to undertake cross-border derivatives trading activities. Huatai Securities entered 
into an ISDA agreement (the “ISDA Agreement”) with its indirectly wholly-owned subsidiary, HTCI to set out the principal terms of any future total return 
swap between Huatai Securities and HTCI.
HTFH is a distributor in connection with the Global Offering. Pursuant to the ISDA Agreement, HTCI, which intends to participate in the Global Offering 
as a placee, will hold the beneficial interest of the Offer Shares on a non-discretionary basis as the single underlying holder under a back-to-back total return 
swap (the “Back-to-back TRS”) to be entered by HTCI in connection with a Client TRS (as defined below) placed by and fully funded (i.e. with no financing 
provided by HTCI) by the Huatai Onshore Ultimate Client (as defined below), by which, HTCI will, subject to customary fees and commissions, pass the full 
economic exposure of the Offer Shares ultimately to the Huatai Onshore Ultimate Client, which in effect, HTCI will hold the beneficial interest of the Offer 
Shares on behalf of the Huatai Onshore Ultimate Client. HTFH and HTCI are indirectly wholly-owned subsidiaries of Huatai Securities. Accordingly, HTCI is 
considered as a “connected client” of HTFH pursuant to paragraph 1B(7) of the Placing Guidelines.
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investor (the “Huatai Onshore Ultimate Client”) cannot directly subscribe for the 
Offer Shares but may invest in derivative products issued by domestic securities firms licenced to undertake cross-border derivatives trading activities, such 
as Huatai Securities, with the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, each of the Huatai Onshore Ultimate 
Client, through its investment manager, will place a total return swap order (the “Client TRS”) with Huatai Securities in connection with the Company’s IPO 
and Huatai Securities will place a Back-to-back TRS order to HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the Back-to-
back TRS, HTCI participates in the Company’s IPO and subscribes the Offer Shares through placing order with HTFH during the International Offering. The 
Huatai Onshore Ultimate Client for purpose of this placee subscription include the investment fund.
To the best of HTCI’s knowledge and after making all reasonable enquiries, the Huatai Onshore Ultimate Client is an independent third party of HTCI, HTFH 
and the companies which are members of the same group of HTCI.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in connection with the Client TRS order placed by the Huatai 
Onshore Ultimate Client. Pursuant to the terms of the contracts of the Back-to-back TRS and the Client TRS, during the tenor of the Back-to-back TRS and 
the Client TRS, subject to customary fees and commissions, all economic returns of the Offer Shares will be ultimately passed to the Huatai Onshore Ultimate 
Client through the Back-to-back TRS and the Client TRS and all economic loss shall be ultimately borne by the Huatai Onshore Ultimate Client. HTCI will 
not take any economic return or bear any economic loss in relation to the Offer Shares.

<<<PAGE 33>>>
– 33 –
Investment in the Back-to-back TRS and the Client TRS is similar to the investment in a qualified domestic institutional investor fund (“QDII”) in the way 
that the Huatai Onshore Ultimate Client would reap all the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through the 
exchange rate exposure on both the notional value of the investment and the profit and loss of the investment. In contrast, the profit and loss of the Back-to-
back TRS and the Client TRS factor into account the fluctuation in RMB exchange rate upon termination of the Client TRS by converting the profit and loss 
using the current exchange rate at the time of termination. As such, the Huatai Onshore Ultimate Client would bear the exchange rate exposure of the profit 
and loss on settlement date.
The Huatai Onshore Ultimate Client may exercise an early termination right to terminate the Client TRS at any time from the issue date of the Client TRS 
which should be on or after the date on which the Offer Shares are listed on the Stock Exchange at its own discretion. Upon the termination upon maturity 
or early termination of the Client TRS by the Huatai Onshore Ultimate Client, HTCI will dispose the Offer Shares on the secondary market and the Huatai 
Onshore Ultimate Client will receive a final settlement amount in cash in accordance with the terms and conditions of the Back-to-back TRS and the Client 
TRS which should have taken into account all the economic returns or economic loss in relation to the Offer Shares. If upon the maturity of the Client TRS, 
the Huatai Onshore Ultimate Client intends to extend the investment period, subject to further agreement between Huatai Securities and the relevant Huatai 
Onshore Ultimate Client, the term of the Client TRS could be extended by way of a new issuance or a tenor extension. Accordingly, Huatai Securities will 
extend the term of the Back-to-back TRS by way of a new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through the economic exposure to the Huatai 
Onshore Ultimate Client, each being an onshore client who places a Client TRS order with Huatai Securities in connection with the IPO of the Company. 
HTCI will not exercise the voting right of the Offer Shares during the tenor of the Back-to-back TRS.
During the life of the Client TRS and Back-to-back TRS, HTCI may continue to hold the Offer Shares in its custodian account, or to hold some or all of the 
Offer Shares in a prime brokerage account for stock borrowing purposes, where HTCI will lend out its holding of underlying Offer Shares in the form of stock 
borrowing loans consistent with market practice to lower its finance costs, provided that HTCI has the ability to call back the Offer Shares on loan at any time 
in order to satisfy its obligations under the Back-to-back TRS to ensure the economic interests are ultimately passed to the Huatai Onshore Ultimate Client.
The Huatai Onshore Ultimate Client for purpose of this placing subscription includes Daohe Chengguang Private Securities Investment Fund (道合承光私募
証券投資基金), whose ultimate beneficial owner holding 30% or more interest is Zhong Shanshan.

<<<PAGE 34>>>
– 34 –
5.	
CGII and China Galaxy Securities (“CGS”) will enter into a series of cross border total return swap (TRS) transactions (collectively, the “CGII TRS”) with 
each other and the ultimate clients (“CGII Ultimate Clients”), pursuant to which CGII will hold the Offer Shares on a non-discretionary basis to hedge the 
CGII TRS while the economic risks and returns of the underlying Offer Shares are ultimately borne by the CGII Ultimate Clients, subject to customary fees 
and commissions. The CGII TRS will be fully funded by the CGII Ultimate Clients. During the terms of the CGII TRS, all economic returns of the Offer 
Shares subscribed by CGII will be passed to CGII Ultimate Clients and all economic loss shall be borne by CGII Ultimate Clients through the CGII TRS, 
and CGII will not take part in any economic return or bear any economic loss in relation to the Offer Shares. The CGII TRS are linked to the Offer Shares 
and CGII Ultimate Clients may, after expiration of the lock-up period beginning from the date of the relevant cornerstone agreements and ending on the date 
which is six months from the Listing Date, request to early terminate the CGII TRS at its own discretion, upon which CGII may dispose of the Offer Shares on 
the secondary market and CGII Ultimate Clients will receive a final settlement amount of the CGII TRS in cash in accordance with the terms and conditions 
of the CGII TRS.
To the best of CGII’s knowledge after having made all reasonable inquiries, each of the CGII Ultimate Clients is an independent third party of CGII, CGIS 
and the companies which are members of the same group of CGIS.
The CGII Ultimate Clients for purpose of this placing subscription include: (i) Yuanxin New Opportunity Private Securities Investment Fund (遠信新機遇
私募證券投資基金), for which no ultimate beneficial owner holds 30% or more interest; and (ii) Yuanxin China Value Return Selected Private Securities 
Investment Fund (遠信中國價值回報精選私募證券投資基金), whose ultimate beneficial owner holding 30% or more interest is Xie Zhendong.

<<<PAGE 35>>>
– 35 –
No.
Connected Distributor
Connected Client
Relationship with the 
Connected Distributor
Identities of the 
ultimate beneficial 
owners of the Offer 
Shares or, where 
applicable, details 
of the structured 
products under which 
the subscription by 
the Connected Client 
was made (e.g. OTC 
total return swaps)
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
Number of Offer 
Shares allocated to the 
connected client
Approximate 
percentage of total 
number of Offer Shares 
under the Global 
Offering (assuming no 
exercise of the Over-
allotment Option)
Approximate 
percentage of total 
issued share capital 
after the Global 
Offering (assuming no 
exercise of the Over-
allotment Option)
Part B — Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties
1.
HTI and GTJAS
Fullgoal Fund 
Management Co., Ltd. 
(“Fullgoal Fund”)
Fullgoal Fund is a member 
of the same group of 
companies as HTI and 
GTJAS
Please refer to Note 1
No
9,885
0.07%
0.01%
2.
HTI and GTJAS
Fullgoal Asset 
Management (HK) 
Limited (“Fullgoal AM”)
Fullgoal AM is a member 
of the same group of 
companies as HTI and 
GTJAS
Please refer to Note 2
No
2,940
0.02%
0.003%
3.
HTI and GTJAS
Haitong International 
Asset Management (HK) 
Limited (“Haitong AM”)
Haitong AM is a member 
of the same group of 
companies as HTI
Please refer to Note 3
No
60
0.0004%
0.00007%
4.
CITIC Securities Brokerage (HK) 
Limited (“CITIC Brokerage HK”)
China Asset Management 
(Hong Kong) Limited 
(“China AMC HK”)
China AMC HK is a 
member of the same group 
of companies as CITIC 
Brokerage HK
Please refer to Note 4
No
10,680
0.08%
0.01%
5.
CITIC Brokerage HK
CITIC Securities Asset 
Management (HK) 
Limited (“CITIC AM”)
CITIC AM is a member 
of the same group of 
companies as CITIC 
Brokerage HK
Please refer to Note 5
No
210
0.002%
0.0002%

<<<PAGE 36>>>
– 36 –
No.
Connected Distributor
Connected Client
Relationship with the 
Connected Distributor
Identities of the 
ultimate beneficial 
owners of the Offer 
Shares or, where 
applicable, details 
of the structured 
products under which 
the subscription by 
the Connected Client 
was made (e.g. OTC 
total return swaps)
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
Number of Offer 
Shares allocated to the 
connected client
Approximate 
percentage of total 
number of Offer Shares 
under the Global 
Offering (assuming no 
exercise of the Over-
allotment Option)
Approximate 
percentage of total 
issued share capital 
after the Global 
Offering (assuming no 
exercise of the Over-
allotment Option)
Part B — Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties
6.
UBS AG Singapore Branch Wealth 
Management (“UBS AG SG”), 
UBS AG Hong Kong Branch 
Wealth Management (“UBS 
AG HK”), ICBC International 
Securities Limited (“ICBCI”)
ICBC UBS Asset 
Management Co., Ltd. 
(“ICBC UBS”)
ICBC UBS is a member 
of the same group of 
companies as UBS AG SG 
and UBS AG HK
ICBC UBS is a member 
of the same group of 
companies as ICBCI
Please refer to Note 6
No
9,195
0.07%
0.01%
7.
UBS AG SG, UBS AG HK and 
ICBCI
ICBC UBS Asset 
Management 
(International) Company 
Limited (“ICBC UBS 
International”)
ICBC UBS International 
is a member of the same 
group of companies as 
UBS AG SG and UBS AG 
HK
ICBC UBS International 
is a member of the same 
group of companies as 
ICBCI
Please refer to Note 6
No
3,630
0.03%
0.004%
8.
UBS AG SG and UBS AG HK
UBS Asset Management 
(Singapore) Ltd. (“UBS 
AM”) (Note 6)
UBS AM is a member 
of the same group of 
companies as UBS AG SG 
and UBS AG HK
Please refer to Note 7
No
427,560
3.10%
0.46%

<<<PAGE 37>>>
– 37 –
No.
Connected Distributor
Connected Client
Relationship with the 
Connected Distributor
Identities of the 
ultimate beneficial 
owners of the Offer 
Shares or, where 
applicable, details 
of the structured 
products under which 
the subscription by 
the Connected Client 
was made (e.g. OTC 
total return swaps)
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
Number of Offer 
Shares allocated to the 
connected client
Approximate 
percentage of total 
number of Offer Shares 
under the Global 
Offering (assuming no 
exercise of the Over-
allotment Option)
Approximate 
percentage of total 
issued share capital 
after the Global 
Offering (assuming no 
exercise of the Over-
allotment Option)
Part B — Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties
9.
ICBCI
ICBC Wealth Management 
Co., Ltd. (“ICBC 
Wealth”)
ICBC Wealth is a member 
of the same group of 
companies as ICBCI
Please refer to Note 8
No
106,890
0.77%
0.12%
10.
CMB International Securities 
Limited (“CMBI”) and China 
Merchants Securities (HK) Co., 
Limited (“CMS”)
China Merchants Fund 
Management Co., Ltd. 
(“China Merchants 
Fund”)
China Merchants Fund is 
a member of the group of 
companies as CMBI and 
CMS.
Please refer to Note 9
No
2,130
0.02%
0.002%
11.
CMBI and CMS
Bosera Asset Management 
(International) Co Ltd. 
(“Bosera AM”)
Bosera AM is a member 
of the same group of 
companies as CMBI and 
CMS.
Please refer to Note 10
Please refer to Note 
10
10,680
0.08%
0.01%
12.
HTFH
China Southern Asset 
Management Co., Ltd. 
(“China Southern”)
China Southern is held 
by Huatai Securities Co., 
Ltd. as to 41.16%, which 
wholly owns HTFH. 
As such, China Southern 
and HTFH is a member 
of the same group of 
companies.
Please refer to Note 11
No
10,680
0.08%
0.01%

<<<PAGE 38>>>
– 38 –
No.
Connected Distributor
Connected Client
Relationship with the 
Connected Distributor
Identities of the 
ultimate beneficial 
owners of the Offer 
Shares or, where 
applicable, details 
of the structured 
products under which 
the subscription by 
the Connected Client 
was made (e.g. OTC 
total return swaps)
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
Number of Offer 
Shares allocated to the 
connected client
Approximate 
percentage of total 
number of Offer Shares 
under the Global 
Offering (assuming no 
exercise of the Over-
allotment Option)
Approximate 
percentage of total 
issued share capital 
after the Global 
Offering (assuming no 
exercise of the Over-
allotment Option)
Part B — Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties
13.
The Hongkong and Shanghai 
Banking Corporation Limited 
(“HSBC”) and HSBC Broking 
Securities (Asia) Limited (“HSBC 
Broking Securities”)
HSBC Global Asset 
Management (Hong Kong) 
Limited (“HSBC AM”)
HSBC AM is a member 
of the same group of 
companies as HSBC and 
HSBC Broking Securities.
Please refer to Note 12
No
14,955
0.11%
0.02%
Notes:
1.	
HTI is the Sponsor-Overall Coordinator and GTJAS is a distributor in connection with of the Global Offering. Fullgoal Fund will hold the Offer Shares in 
its capacity as the discretionary fund manager on behalf of its investors, each of which is an independent third party of the Company, its subsidiaries, its 
substantial shareholders, Fullgoal Fund, HTI, GTJAS and the companies which are members of the same group of HTI and GTJAS.
The Fullgoal Fund Ultimate Clients for purpose of this placing subscription include ICBC Fullgoal China Small & Mid Cap (HK listed) Equity Fund, ICBC 
Fullgoal Global Technology & Internet Fund, CMB-Fullgoal Blue Chip Selected Equity Fund (QDII), Fullgoal Dividend Selected Hybrid Fund, Fullgoal 
Global Consumption Selected Hybrid, Fullgoal Healthcare Select Hybrid Fund (QDII) and China Merchants Bank-Fullgoal Hong Kong Equity Select Hybrid 
Fund (QDII), for each of which no ultimate beneficial owner holds 30% or more interest.
2.	
HTI is the Sponsor-Overall Coordinator and GTJAS is a distributor in connection with of the Global Offering. Fullgoal AM will hold the Offer Shares in its 
capacity as the discretionary fund manager managing the funds on behalf of their underlying investors, each of which is an independent third party of the 
Company, its subsidiaries, its substantial shareholders, Fullgoal AM, HTI and the companies which are members of the same group of HTI and GTJAS.

<<<PAGE 39>>>
– 39 –
The Fullgoal AM Ultimate Clients for purpose of this placing subscription include: (i) HI-Aktien China 1-SFonds, whose ultimate beneficial owner holding 
30% or more interest is a European pension; (ii) Fullgoal China Growth Select Fund, whose ultimate beneficial owner holding 30% or more interest is Zhao 
Xueming; (iii) Fullgoal China Small-Mid Cap Growth Fund, for which no ultimate beneficial owner holds 30% or more interest; and (iv) Fullgoal China 
Opportunities Fund, whose ultimate beneficial owners holding 30% or more interest are China Everbright Fortune Investment Limited, L Industries Limited 
and Orient Sun Rise Fund Series SPC-Orient Sun Rise Enhanced Balanced Fund Segregated Portfolio.
3.	
HTI is the Sponsor-Overall Coordinator and GTJAS is a distributor in connection with the Global Offering. Haitong AM will hold the Offer Shares in its 
capacity as the discretionary investment manager managing assets on behalf of its underlying clients, each of which is an independent third party of Haitong 
AM, HTI, GTJAS and the companies which are members of the same group of HTI and GTJAS.
The Haitong AM Ultimate Clients for purpose of this placing subscription include Haitong Opportunity Fund II S.P., for which no ultimate beneficial owner 
holds 30% or more interest.
4.	
CITIC Brokerage HK is a distributor of the Global Offering. China AMC HK is a member of the same group of companies as CITIC Brokerage HK and China 
AMC HK is therefore considered as a connected client of CITIC Brokerage HK pursuant to paragraph 1B(7) of Appendix F1 to the Listing Rules. China AMC 
HK will hold the Offer Shares in its capacity as the discretionary fund manager managing on behalf of its underlying clients, each of which is an independent 
third party of the Company, its subsidiaries, its substantial shareholders, China AMC HK, CITIC Brokerage HK and the companies which are members of the 
same group of CITIC Brokerage HK.
The China AMC HK Ultimate Clients for purpose of this placing subscription include: (i) ChinaAMC Select Greater China Technology Fund, whose ultimate 
beneficial owner holding 30% or more interest is Futu Securities International (Hong Kong) Limited-client account, holding approximately 51.34%; (ii) 
ChinaAMC Fund — China AMC China Opportunities Fund, for which no ultimate beneficial owner holds 30% or more interest; (iii) China AMC China Focus 
Fund, whose ultimate beneficial owner holding 30% or more interest is Manulife (International) Limited, holding approximately 73.13%; (iv) China AMC 
China Growth Fund (SICAV), whose ultimate beneficial owner holding 30% or more interest is Yuanta Securities (HK) Company LTD, holding approximately 
72.71%; and (v) C215, whose ultimate beneficial owner holding 30% or more interest is Hong Kong Monetary Authority, holding 100%.

<<<PAGE 40>>>
– 40 –
5.	
CITIC Brokerage HK is a distributor of the Global Offering. CITIC AM will hold the Offer Shares in its capacity as the discretionary fund manager on behalf 
of its underlying client, which is an independent third party. There is no ultimate beneficial owner holding 30% interest or more in such underlying client. To 
the best knowledge of CITIC AM after due enquiry, the underlying client of CITIC AM is an independent third party of CITIC AM and CITIC Brokerage HK, 
and the companies which are members of the same group of companies as CITIC Brokerage HK.
The CITIC AM Ultimate Client for purpose of this placing subscription includes Meta Chance 2, whose ultimate beneficial owner holding 30% or more 
interest is Song Ke.
6.	
Each of UBS AG SG, UBS AG HK and ICBCI is a distributor in connection with the Global Offering. ICBC UBS will hold the Offer Shares in its capacity 
as the discretionary fund manager managing the funds on behalf of a discretionary account, each of whom (and each of whose respective underlying clients) 
is, to the best knowledge of ICBC UBS, an independent third party of the Company, its subsidiaries, its substantial shareholders, ICBC UBS, ICBC UBS 
International, UBS AG SG, UBS AG HK, ICBCI and the companies which are members of the same group of UBS AG SG, UBS AG HK and/or ICBCI. 
There is no ultimate beneficial owner holding 30% interest or more in such underlying client.
The ICBC UBS Ultimate Clients for purpose of this placing subscription include ICBC Credit Suisse New Economy Flexible Allocation Mixed Securities 
Investment Fund (QDII) (工銀瑞信新經濟靈活配置混合型證券投資基金(QDII)) and ICBC CS Hong Kong Small and Mid Cap Equity Securities 
Investment Fund (QDII) (工銀瑞信香港中小盤股票型證券投資基金(QDII)), for each of which no ultimate beneficial owner holds 30% or more interest.
ICBC UBS International will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of a discretionary account, 
each of whom (and each of whose respective underlying clients) is, to the best knowledge of ICBC UBS International who is an independent third party of the 
Company, its subsidiaries, its substantial shareholders, ICBC UBS, ICBC UBS International, UBS AG SG, UBS AG HK, ICBCI and the companies which are 
members of the same group of UBS AG SG, UBS AG HK and/or ICBCI.
The ICBC UBS International Ultimate Clients for purpose of this placing subscription include: (i) RUIHONG NO1, whose ultimate beneficial owner holding 
30% or more interest is Qiao Weibing; and (ii) RUIHONG NO3, whose ultimate beneficial owner holding 30% or more interest is Alpaca Capital Management 
Limited.
7.	
Each of UBS AG SG and UBS AG HK is a distributor of the Global Offering, of which its role is confirmed only after the publication of the Prospectus. 
UBS AM is a cornerstone investor of the Company and is included in this waiver application by virtue of its relationship with UBS AG SG and UBS AG 
HK for completeness. UBS AM will hold the Offer Shares in its capacity as investment manager for and on behalf of the following funds: (i) UBS (Lux) 
Equity Fund — Greater China (USD); (ii) UBS (Lux) Equity Fund — China Opportunity (USD); (iii) UBS (HK) Fund Series — China Opportunity Equity 
(USD); (iv) UBS (Lux) Equity SICAV — All China (USD); (v) UBS (CAY) China A Opportunity; and (vi) certain other segregated accounts and mandates. 
No single ultimate beneficial owner holds 30% or more interest in each of the abovementioned funds. UBS AM is a wholly owned subsidiary of UBS Asset 
Management AG, an investment management company, which is wholly ultimately owned by UBS Group AG, which is a company organized under Swiss law 
as a corporation that has issued shares of common stock to investors. UBS Group AG’s shares are listed on the SIX Swiss Exchange (stock code: UBSG) and 
the New York Stock Exchange (stock code: UBS).

<<<PAGE 41>>>
– 41 –
8.	
ICBCI is a distributor of the Global Offering, of which its role is confirmed only after the publication of the Prospectus. ICBC Wealth is a cornerstone investor 
of the Company and is included in this waiver application by virtue of its relationship with ICBCI for completeness. ICBC Wealth will hold the Offer Shares 
in its capacity as the investment manager of certain wealth management products under its discretionary management, and no single ultimate beneficial owner 
holds 30% or more interests in such products.
9.	
Each of CMBI and CMS is a distributor of the Global Offering. China Merchants Fund will hold the Offer Shares in its capacity as the discretionary fund 
manager managing the Pusheng Global Allocation Fund (the “China Merchants Fund Ultimate Client”) (a mutual fund) on behalf of their investors, of 
which all underlying investors of China Merchants Fund are independent third parties of the Company, its subsidiaries, China Merchants Fund, CMBI and the 
companies which are members of the same group of CMB International Securities Limited. No ultimate beneficial owner holds 30% or more interest therein. 
China Merchants Bank Co., Ltd. and China Merchants Securities Co., Ltd. (“CMSC”) are the ultimate beneficial owners holding 30% or more interest in 
China Merchants Fund.
10.	
Each of CMBI and CMS is distributor of the Global Offering. Bosera AM is held as to 55% by Bosera Asset Management Co., Ltd. and 45% by China 
Merchants Fund. CMSC currently holds 49% of the equity interest of Bosera Asset Management Co., Ltd. and 45% of the equity interest of China Merchants 
Fund. CMS is a wholly-owned subsidiary of CMSC. Therefore, Bosera AM is a member of same group of companies as CMS and CMSC. Bosera AM intends 
to subscribe and hold the Offer Shares in its capacity as the discretionary fund manager on behalf of its sub-funds (namely, Bosera Hong Kong Equity Plus 
Fund (SFC Authorised Fund), Bosera Global Select Equity Fund SP, Navigator Technology Limited IPO Mandate, Bosera China New Opportunities Fund 
SP, Bosera Growth Premium Global Equity Strategy Fund SP, KB China Mainland FD Bosera, Bosera Growth Premium Global Equity Strategy Fund SP2, 
Bosera Growth Premium Global Equity Strategy Fund SP3, Fortuna Capital Management IPO Mandate), which are all independent third parties. To the 
best knowledge of Bosera AM after due enquiry, each of the sub-funds and their respective ultimate beneficial owner holding 30% or more interest is an 
independent third party of Bosera AM and each of CMBI and CMS, and the companies which are members of the same group of companies as each of CMBI 
and CMS.
The Bosera AM Ultimate Clients for purpose of this placing subscription include: (i) Bosera Hong Kong Equity Plus Fund, for which no ultimate beneficial 
owner holds 30% or more interest; (ii) Bosera Global Select Equity Fund SP, whose ultimate beneficial owner holding 30% or more interest is Zhang Lei, 
holding approximately 53.67%; (iii) Navigator Technology Limited IPO Mandate, whose ultimate beneficial owner holding 30% or more interest is Fuhua 
Zheng, holding 100%; (iv) Bosera China New Opportunities Fund SP, for which no ultimate beneficial owner holds 30% or more interest; (v) Bosera Growth 
Premium Global Equity Strategy Fund SP, whose ultimate beneficial owner holding 30% or more interest is Guo Feng, holding approximately 49.00%; (vi) 
KB China Mainland FD Bosera, for which no ultimate beneficial owner holds 30% or more interest; (vii) Bosera Growth Premium Global Equity Strategy 
Fund SP2, whose ultimate beneficial owner holding 30% or more interest is Guangdong Dongfang Precision Science & Technology Co., Ltd (Ticker: 002611 
CH), holding approximately 47.42%; (viii) Bosera Growth Premium Global Equity Strategy Fund SP3, whose ultimate beneficial owner holding 30% or more 
interest is Huang Liya, holding 100%; and (ix) Fortuna Capital Management Limited IPO Mandate, whose ultimate beneficial owner holding 30% or more 
interest is Yang Dehui, holding 100%.

<<<PAGE 42>>>
– 42 –
11.	
HTFH is a distributor in connection with the Global Offering. China Southern, a qualified domestic institutional investor as approved by the relevant PRC 
authority to conduct asset management business, will hold the Offer Shares as the independent agent and discretionary manager of certain QDII funds. China 
Southern has confirmed that, to the best of their knowledge, each of such underlying clients are independent third parties of China Southern, HTFH and 
the companies which are members of the same group of companies as HTFH. There is no ultimate beneficial owner holding 30% interest or more in such 
underlying client.
The China Southern Ultimate Clients for purpose of this placing subscription include China Southern Hong Kong Growth Dynamic Allocation Hybrid Fund 
(南方香港成長靈活配置混合), China Southern Hong Kong Digital Economy Hybrid Initiating Fund (QDII) (南方港股數字經濟混合發起(QDII)), China 
Southern Hong Kong Select Equity Fund (南方香港LOF) and China Southern China New Economy (南方中國新興經濟), for each of which no ultimate 
beneficial owner holds 30% or more interest.
12.	
HSBC is an overall coordinator in connection with the Global Offering and HSBC Broker Services is a distributor in connection with the Global Offering. 
HSBC AM will hold the Offer Shares in its capacity as the discretionary fund manager managing assets on behalf of its underlying clients. Each of the 
underlying clients of HSBC AM is an independent third party of HSBC AM, HSBC and HSBC Broker Services and the companies which are members of the 
same group of HSBC and HSBC Broker Services. There is no ultimate beneficial owner holding 30% interest or more in such underlying client.
The HSBC AM Ultimate Clients for purpose of this placing subscription include HGIF Asia EXJ EQ Smal (HH), HSHK Asian Small Cap (EQ), HGIF Asia 
Ex Japan EQ (HH), HSBC APXJ EQ Vol FOC (HH), HSBC Pooled AP EXJ EQ (AC), HSBC RAIF AES Angel (HH), HSBC RAIF AES (HH), HGIF Chinese 
Equity (HH), HSBC China Growth FD (HH), HSBC China Momentum (HH), HSBC China Mult-A EQ-OFF and HSBC Pooled Chinese (HH), for each of 
which no ultimate beneficial owner holds 30% or more interest.
HSBC AM has confirmed that, to the best of their knowledge, each of such underlying clients are independent third parties of HSBC, HSBC AM and the 
companies which are members of the same group of companies as HSBC.

<<<PAGE 43>>>
– 43 –
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong 
Limited (the “Stock Exchange”) and Hong Kong Securities Clearing Company Limited 
(“HKSCC”) take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part 
of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in 
or into the United States (including its territories and possessions, any state of the United 
States and the District of Columbia). This announcement does not constitute or form 
a part of any offer or solicitation to purchase or subscribe for securities in the United 
States. The securities mentioned herein have not been, and will not be, registered under 
the United States Securities Act of 1933, as amended (the “U.S. Securities Act”). The 
securities may not be offered or sold in the United States except pursuant to an exemption 
from the registration requirements of the U.S. Securities Act and in compliance with any 
applicable state securities laws, or outside the United States unless in compliance with 
Regulation S under the U.S. Securities Act. There will be no public offer of securities in 
the United States.
The Offer Shares are being offered and sold (1) solely to qualified institutional buyers 
as defined in Rule 144A under the U.S. Securities Act pursuant to an exemption from 
registration under the U.S. Securities Act and (2) outside the United States in offshore 
transactions in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation 
or offer to acquire, purchase or subscribe for securities. This announcement is not a 
prospectus. Potential investors should read the Prospectus dated April 20, 2026 issued 
by Shanghai Xizhi Technology Co., Ltd. (上海曦智科技股份有限公司) for detailed 
information about the Global Offering described below before deciding whether or not to 
invest in the Shares thereby being offered.
*	
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and 
on behalf of the Hong Kong Underwriters), may, in their sole and absolute discretion, upon giving 
notice in writing to the Company, terminate the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the paragraph headed “Underwriting — 
Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” 
in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is 
currently expected to be on April 28, 2026).

<<<PAGE 44>>>
– 44 –
PUBLIC FLOAT AND FREE FLOAT
Pursuant to Rule 19A.13A of the Listing Rules, assuming that the Over-allotment Option is 
not exercised, based on the Offer Price of HK$183.2 per Offer Share, the expected market 
capitalization of the Company upon the Listing is HK$16,849 million, and the minimum 
prescribed public float percentage applicable to our Shares is 15%. Immediately after the 
completion of the Global Offering, 57,249,661 H Shares, representing approximately 62.25% of 
the issued share capital of our Company, will count towards the public float, thereby satisfying 
the minimum percentage requirement in compliance with Rule 19A.13A(1) of the Listing Rules.
Based on the final Offer Price of HK$183.2 per H Share, the Company satisfies the free 
float requirement under Rule 19A.13C of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering: (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of the 
Company; (ii) there will not be any new substantial Shareholder (as defined in the Listing Rules) 
of the Company; (iii) the three largest public shareholders of the Company do not hold more than 
50% of the H Shares in public hands at the time of the Listing in compliance with Rules 8.08(3) 
and 8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at the time of the 
Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, 
April 28, 2026 (Hong Kong time), provided that the Global Offering has become 
unconditional and the right of termination described in the section headed “Underwriting — 
Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus has not been exercised. Investors who trade the H Shares on 
the basis of publicly available allocation details prior to the receipt of H Share certificates or 
prior to the H Share certificates becoming valid evidence of title do so entirely at their own 
risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on 
Tuesday, April 28, 2026 (Hong Kong time), it is expected that dealings in the H Shares on 
the Stock Exchange will commence at 9:00 a.m. on Tuesday, April 28, 2026 (Hong Kong 
time). The H Shares will be traded in board lots of 15 H Shares each, and the stock code of 
the H Shares will be 01879.
By order of the Board
Shanghai Xizhi Technology Co., Ltd.
上海曦智科技股份有限公司
Dr. Shen Yichen
Founder, Chairman of the Board, 
Executive Director and Chief Executive Officer
Hong Kong, April 27, 2026
The Board comprises Dr. Shen Yichen, Dr. Meng Huaiyu, Mr. Wang Long and Mr. Zhang Hong as executive 
directors, Mr. Yu Ze and Mr. Zhang Kun as non-executive directors, and Dr. Huang Weiping, Dr. Zhao Hang 
and Ms. Xu Lili as independent non-executive directors (to be effective upon Listing).
