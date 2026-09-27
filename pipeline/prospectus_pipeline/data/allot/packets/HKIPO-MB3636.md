# 配发结果公告抽取任务：3636.HK Yunnan Jinxun Resources Co., Ltd. - H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**08/01/2026 22:46**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0108/2026010801368.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3636.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
and Hong Kong Securities Clearing Company Limited (the “HKSCC”) take no responsibility for the contents of 
this announcement, make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
Unless otherwise defined herein, capitalized terms and expressions used in this announcement shall have the same 
meanings as those defined in the prospectus dated December 31, 2025 (the “Prospectus”) of Yunnan Jinxun Resources 
Co., Ltd. (雲南金潯資源股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an offer or an invitation to induce an 
offer by any person to acquire, purchase or subscribe for any securities of the Company. This announcement is not a 
prospectus. Potential investors should read the Prospectus carefully for detailed information about the Company and 
the Global Offering before deciding whether or not to invest in the Offer Shares. Any investment decision in relation 
to the Global Offering should be taken solely in reliance on the information provided in the Prospectus.
This announcement is not for release, publication or distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia) or to any 
person (as defined in Regulation S under the United States Securities Act of 1933, as amended from time to time, 
(the “U.S. Securities Act”)) (“U.S. Persons”) or any other jurisdiction where such distribution is prohibited by law. 
This announcement does not constitute or form a part of any offer to sell or solicitation to purchase or subscribe for 
securities in the United States or in any other jurisdiction. The Offer Shares have not been and will not be registered 
under the U.S. Securities Act or securities law any state or other jurisdiction of the United States and may not be 
offered, sold, pledged or transferred within the United States, except in transactions exempt from, or not subject to, the 
registration requirements of the U.S. Securities Act. There will not be and is not currently intended to be any public 
offer of the Offer Shares in the United States. The Offer Shares are being offered and sold outside the United States in 
offshore transactions in reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, Huatai Financial Holdings (Hong Kong) Limited, as the stabilizing manager 
(the “Stabilizing Manager”), its affiliates or any person acting for it, on behalf of the Underwriters, may over-allocate 
or effect transactions with a view to stabilizing or maintaining the market price of the H Shares at a level higher than 
that which might otherwise prevail in the open market for a limited period which begins on the Listing Date. However, 
there is no obligation on the Stabilizing Manager, its affiliates or any person acting for it to conduct any such 
stabilizing action, which, if commenced, will be done at the sole and absolute discretion of the Stabilizing Manager, 
its affiliates or any person acting for it, and may be discontinued at any time. Any such stabilizing activity is required 
to be brought to an end on Thursday, February 5, 2026, being the 30th day after the last day for lodging applications 
under the Hong Kong Public Offering. Such stabilizing action, if taken, may only be effected in all jurisdictions where 
it is permissible to do so, in each case in compliance with all applicable laws, rules and regulatory requirements, 
including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, 
made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that stabilizing action cannot be taken to support the price of the H Shares for 
longer than the stabilization period which begins on the Listing Date and is expected to expire on Thursday, February 
5, 2026, being the 30th day after the last day for lodging applications under the Hong Kong Public Offering. After this 
date, no further stabilizing action may be taken, and demand for the H Shares and the price of the H Shares could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions as set out 
in the Prospectus. Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves 
and on behalf of the Hong Kong Underwriters) and the Sole Sponsor shall be entitled to terminate the Hong 
Kong Underwriting Agreement upon the occurrence of any of the events set out in “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus at any time 
prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be Friday, January 9, 2026).

<<<PAGE 2>>>
2
Yunnan Jinxun Resources Co., Ltd.
雲南金潯資源股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the Global
:
36,765,600 H Shares (subject to the Over-
Offering allotment Option)
Number of Hong Kong Offer Shares
:
3,676,600 H Shares
Number of International Offer Shares
:
33,089,000 H Shares (subject to the Over-
allotment Option)
Offer Price
:
HK$30.00 per H Share, plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
AFRC transaction levy of 0.00015% and 
Stock Exchange trading fee of 0.00565%
Nominal value
:
RMB1.00 per H Share
Stock Code
:
3636
Sole Sponsor, Sponsor-Overall Coordinator, Overall Coordinator,
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers (in alphabetical order)
Joint Lead Managers (in alphabetical order)

<<<PAGE 3>>>
3
YUNNAN JINXUN RESOURCES CO., LTD./雲南金潯資源股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated 31 December 2025 (the “Prospectus”) issued by 
Yunnan Jinxun Resources Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of H 
Shareholders, H Shareholders and prospective investors should be aware that the price of 
the H Shares could move substantially even with a small number of H Shares traded and 
should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
3636
Stock short name
JINXUN RESOURCE
Dealings commencement date
9 January 2026*
* see note at the end of the announcement
Price Information
Final Offer Price
HK$30.00
Offer Shares and Share Capital
Number of Offer Shares
36,765,600
Final Number of Offer Shares in Hong Kong Public Offering
3,676,600
Final Number of Offer Shares in International Offering
33,089,000
Number of issued shares upon Listing (before exercise of 
Over-allotment Option)
147,062,243
Over-allocation
No. of Offer Shares over-allocated
5,514,800
 – International Offering
5,514,800
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.

<<<PAGE 4>>>
4
Proceeds
Gross proceeds (Note)
HK$1,102.97 million
 Less: Estimated listing expenses payable based on 
 Final Offer Price
HK$ (60.37) million
Net proceeds
HK$1,042.60 million
Note: Gross proceeds refers to the amount to which the issuer is entitled to receive. For details of the use of 
proceeds, please refer to the Prospectus.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
64,456
No. of successful applications
9,037
Subscription level
143.46 times
Claw-back triggered
No
No. of Offer Shares initially available under the Hong Kong Public 
Offering
3,676,600
Final no. of Offer Shares under the Hong Kong Public Offering
3,676,600
% of Offer Shares under the Hong Kong Public Offering to the Global 
Offering
10.00%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can refer to http://
www.eipo.com.hk/eIPOAllotment to perform a search by name or identification number or http://www.eipo.com.hk/
eIPOAllotment for the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
96
Subscription Level
12.78 times
No. of Offer Shares initially available under the International Offering
33,089,000
Final no. of Offer Shares under the International Offering
33,089,000
% of Offer Shares under the International Offering to the Global  
Offering (Note)
90.00%
Note: Assuming the Over-allotment Option is not exercised.
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, Controlling Shareholders, 
substantial shareholders, existing shareholders of the Company or any of its subsidiaries or their 
respective close associates; and (ii) none of the placees and the public who have purchased the 
Offer Shares are accustomed to taking instructions from the Company, any of the Directors, 
chief executive of the Company, Controlling Shareholders, substantial shareholders, existing 
shareholders of the Company or any of its subsidiaries or their respective close associates in 
relation to the acquisition, disposal, voting or other disposition of Shares registered in his/her/its 
name or otherwise held by him/her/it.

<<<PAGE 6>>>
6
The placees in the International Offering include the following:
Cornerstone Investors
Investor (1)
No. of Offer Shares 
allocated (2) (3)
% of Offer 
Shares (3)
% of total issued 
share capital 
after the Global 
Offering (3)
Existing 
shareholders 
or their close 
associates
Glencore International AG
7,780,800
21.16%
5.29%
No
Stoneylake Global Alpha Fund
2,593,600
7.05%
1.76%
No
NR 1 SP
2,074,800
5.64%
1.41%
No
China Asset Management (Hong Kong) 
Limited/
華夏基金管理(香港)有限公司
778,000
2.12%
0.53%
No
New Asia Ferrell Asset Management 
Limited/新亞洲富怡資產管理有限公司
778,000
2.12%
0.53%
No
Bridge Zone Group Limited/
聯域集團有限公司
770,200
2.09%
0.52%
No
Zhengxin Group Investment Limited
518,600
1.41%
0.35%
No
Sunwoda Treasury (Hong Kong) Limited/
欣旺達財資(香港)有限公司
333,200
0.91%
0.23%
No
Total
15,627,200
42.50%
10.63%
Notes:
1. 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in 
the Prospectus.
2. 
Excluding Offer Shares allotted to Cornerstone Investors and/or their close associates with consent under 
Chapter 4.15 of the Guide for New Listing Applicants (if any).
3. 
Before any exercise of the Over-allotment Option.

<<<PAGE 7>>>
7
ALLOTTEES WITH WAIVERS/CONSENTS OBTAINED
Investor
Number of Offer 
Shares allocated
% of Offer Shares 
(assuming no 
exercise of the 
Over-allotment)
% of total issued 
share capital 
after the Global 
Offering (assuming 
no exercise of the 
Over-allotment 
Option)
Allottees with consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further H Shares to 
Cornerstone Investors and/or their close associates (Note)
Stoneylake Global Alpha Fund
2,590,000
7.04%
1.76%
NR 1 SP
778,000
2.12%
0.53%
China Asset Management (Hong Kong) Limited
778,000
2.12%
0.53%
New Asia Ferrell Asset Management Limited
753,000
2.05%
0.51%
Bridge Zone Group Limited
750,000
2.04%
0.51%
Sunwoda Treasury (Hong Kong) Limited (欣旺達財資(香港)有限
公司)
333,000
0.91%
0.23%
Note: The number of Offer Shares allocated to the relevant investors listed in this subsection only represents 
the number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details – Cornerstone Investors” in this announcement. For details of the consent under Chapter 4.15 of 
the Guide for New Listing Applicants in relation to allocations of further Shares to Cornerstone investors and 
their close associates, please refer to the section headed “Others/Additional Information – Allocations of Offer 
Shares to Cornerstone Investor and/or their close associates with consent under Chapter 4.15 of the Guide” in this 
announcement.

<<<PAGE 8>>>
8
Investor
Number of Offer 
Shares allocated
% of Offer Shares 
(assuming no 
exercise of the 
Over-allotment)
% of total issued 
share capital 
after the Global 
Offering (assuming 
no exercise of the 
Over-allotment 
Option)
Relationship
Allottees with consent under paragraph 1C(1) Placing Guidelines for Equity Securities (Appendix F1 of the Main Board Listing 
Rules) in relation to allocations to connected clients (1)
Huatai Capital Investment 
Limited (“HTCI”)
403,600
1.10%
0.27%
HTCI and Huatai Financial 
Holdings (Hong Kong) 
Limited (“Huatai”) are group 
companies within the same 
group
CSOP Asset Management 
Limited (“CSOP AM”)
20,000
0.05%
0.01%
CSOP AM and Huatai are group 
companies within the same 
group
CITIC Securities International 
Capital Management Limited 
(“CSI”)
182,600
0.50%
0.12%
CSI and CLSA Limited 
(“CLSA”) are group 
companies within the same 
group
CITIC Securities Asset 
Management Company 
Limited (“CITIC SAMC”)
36,000
0.10%
0.02%
CITIC AMC and CLSA are 
group companies within the 
same group
China Asset Management (Hong 
Kong) Limited (“China AMC 
(HK)”)
1,556,000(2)
4.23%
1.06%
China AMC (HK) and CLSA 
are group companies within 
the same group.
One of the public funds 
managed by ChinaAMC 
(HK) is distributed by Futu 
Securities International (Hong 
Kong) Limited (“Futu”) and 
ultimately 74.29% held by 
Futu’s clients.
ABCI Asset Management 
Limited (“ABCI AM”)
1,000
0.003%
0.001%
ABCI AM, ABCI Capital 
Limited and ABCI Securities 
Company Limited are group 
companies within the same 
group
Notes:
1. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to 
connected clients, please refer to the section headed “Others/Additional Information – Placing to connected 
clients with a prior consent under paragraph 1C(1) of the Placing Guidelines” in this announcement.
2. 
Number of Offer Shares allocated to China AMC (HK) in this subsection included both Offer Shares allocated 
as cornerstone investor and as placee in the International Offering.

<<<PAGE 9>>>
9
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
Number of 
H Shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon listing
% of 
shareholding 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
Last day subject to 
the lock-up 
undertakings(Note)
Yuan Rong/袁榮
101,230,612
0
0.00%
68.84%
8 January 2027
Ji’an Heli Investment Management 
Center (Limited Partnership)/吉安縣
合勵投資管理中心(有限合夥)
8,973,467
0
0.00%
6.10%
8 January 2027
Subtotal
110,204,079
0
0.00%
74.94%
 
Note: The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Laws. The 
required lock-up for the Controlling Shareholders ends on 8 January 2027, being 12 months following the Listing 
Date.

<<<PAGE 10>>>
10
Existing Shareholders
Name
Number of 
shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
Number of 
H Shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon listing
% of 
shareholding 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
Last day subject to 
the lock-up 
undertakings(Note)
Yuan Rong/袁榮
101,230,612
0
0.00%
68.84%
8 January 2027
Ji’an Heli Investment Management 
Center (Limited Partnership)/吉安縣
合勵投資管理中心(有限合夥)
8,973,467
0
0.00%
6.10%
8 January 2027
Guo Lilei/郭利磊
27,299
0
0.00%
0.02%
8 January 2027
Wang Cuihua/王翠花
16,805
0
0.00%
0.01%
8 January 2027
Wu Jianli/吳建莉
14,820
0
0.00%
0.01%
8 January 2027
Song Tao/宋濤
14,000
0
0.00%
0.01%
8 January 2027
Zhu Xu/朱旭
10,283
0
0.00%
0.01%
8 January 2027
Liu Gang/劉剛
3,000
0
0.00%
0.00%
8 January 2027
Guo Lizhe/郭利哲
2,600
0
0.00%
0.00%
8 January 2027
Chen Shanyong/陳善勇
1,080
0
0.00%
0.00%
8 January 2027
Xiang Lili/向莉麗
750
0
0.00%
0.00%
8 January 2027
Bi Jiandong/畢建東
700
0
0.00%
0.00%
8 January 2027
Yu Hui/余慧
400
0
0.00%
0.00%
8 January 2027
Ye Xinyi/葉信益
200
0
0.00%
0.00%
8 January 2027
Peng Zhangyun/彭章運
200
0
0.00%
0.00%
8 January 2027
Xiong Wei/熊巍
100
0
0.00%
0.00%
8 January 2027
Han Xitang/韓錫堂
100
0
0.00%
0.00%
8 January 2027
Li Wenhai/李文海
100
0
0.00%
0.00%
8 January 2027
Zhou Jie/周杰
76
0
0.00%
0.00%
8 January 2027
Luo Jiegao/羅傑高
51
51
0.00%
0.00%
8 January 2027
Subtotal
110,296,643
51
0.00%
75.00%
Note: The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Laws. The required lock-up for the Controlling Shareholders ends on 8 January 2027, 
being 12 months following the Listing Date.

<<<PAGE 11>>>
11
Cornerstone Investors
Name
Number of 
shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
Number of 
H Shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon listing(Note 1)
% of 
shareholding 
in the Company 
subject to 
lock-up 
undertakings 
upon listing(Note 1)
Last day 
subject to the lock-up 
undertakings (Note 2)
Glencore International AG
2,593,600
2,593,600
7.05%
1.76%
9 July 2026
Glencore International AG
5,187,200
5,187,200
14.11%
3.53%
9 January 2029 (note 3)
Stoneylake Global Alpha Fund
2,593,600
2,593,600
7.05%
1.76%
9 July 2026
NR 1 SP
2,074,800
2,074,800
5.64%
1.41%
9 July 2026
China Asset Management (Hong Kong) 
Limited/華夏基金管理(香港)有限
公司
778,000
778,000
2.12%
0.53%
9 July 2026
New Asia Ferrell Asset Management 
Limited/新亞洲富怡資產管理有限
公司
778,000
778,000
2.12%
0.53%
9 July 2026
Bridge Zone Group Limited/聯域集團
有限公司
770,200
770,200
2.09%
0.52%
9 July 2026
Zhengxin Group Investment Limited
518,600
518,600
1.41%
0.35%
9 July 2026
Sunwoda Treasury (Hong Kong) 
Limited/欣旺達財資(香港) 
有限公司
333,200
333,200
0.91%
0.23%
9 July 2026
Subtotal
15,627,200
15,627,200
42.50%
10.63%
Notes:
1. 
Assuming the Over-allotment Option is not exercised.
2. 
The Cornerstone Investors will cease to be prohibited from disposing of or transferring H Shares after the indicated date.
3. 
Glencore International AG has agreed to an additional restriction of which the required lock-up ends on 9 January 2029, being 36 months following the Listing Date.

<<<PAGE 12>>>
12
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option is 
exercised and 
new H Shares 
are issued)
Allotment as 
% of total 
Offer Shares 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option is 
exercised and 
new H Shares 
are issued)
Number of H 
Shares held 
upon Listing
% of total 
issued H 
Shares 
capital upon 
Listing 
(assuming 
no exercise 
of the Over-
allotment 
Option)
% of total 
issued H 
Shares 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is 
exercised and 
new H Shares 
are issued)
Number of 
Shares held 
upon Listing
Top 1
7,780,800
23.51%
20.16%
21.16%
18.40%
7,780,800
21.16%
18.40%
7,780,800
Top 5
18,923,200
57.19%
49.02%
51.47%
44.76%
18,923,200
51.47%
44.76%
18,923,200
Top 10
26,564,400
80.28%
68.81%
72.25%
62.83%
26,564,400
72.25%
62.83%
26,564,400
Top 25
36,759,200
111.09%
95.22%
99.98%
86.94%
36,759,200
99.98%
86.94%
36,759,200
Note: Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing. This chart also presents the placee concentration 
analysis.

<<<PAGE 13>>>
13
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option is 
exercised and 
new H Shares 
are issued)
Allotment as 
% of total 
Offer Shares 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option is 
exercised and 
new H Shares 
are issued)
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
(assuming 
no exercise 
of the Over-
allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is 
exercised and 
new H Shares 
are issued)
Top 1
0
0.00%
0.00%
0.00%
0.00%
0
110,204,079
74.94%
72.23%
Top 5
17,373,200
52.50%
45.00%
47.25%
41.09%
17,373,200
127,577,279
86.75%
83.61%
Top 10
25,044,200
75.69%
64.87%
68.12%
59.23%
25,044,200
135,248,279
91.97%
88.64%
Top 25
36,633,200
110.71%
94.90%
99.64%
86.64%
36,633,200
146,837,279
99.85%
96.24%
Note: Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 14>>>
14
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
NO. OF 
H SHARES 
APPLIED FOR
NO. OF 
VALID 
APPLICATIONS BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL NO. 
OF H SHARES 
APPLIED FOR
200
36,519
0 H Shares
7.00%
200
2,749
200 H Shares
400
2,341
0 H Shares
4.37%
400
224
200 H Shares
600
1,019
0 H Shares
3.09%
600
104
200 H Shares
800
592
0 H Shares
2.34%
800
61
200 H Shares
1,000
3,235
0 H Shares
1.98%
1,000
356
200 H Shares
1,200
426
0 H Shares
1.66%
1,200
47
200 H Shares
1,400
343
0 H Shares
1.46%
1,400
39
200 H Shares
1,600
3,634
0 H Shares
1.32%
1,600
429
200 H Shares
1,800
222
0 H Shares
1.24%
1,800
28
200 H Shares
2,000
2,166
0 H Shares
1.13%
2,000
277
200 H Shares
3,000
1,022
0 H Shares
0.90%
3,000
159
200 H Shares
4,000
889
0 H Shares
0.78%
4,000
164
200 H Shares
5,000
408
0 H Shares
0.71%
5,000
88
200 H Shares
6,000
399
0 H Shares
0.66%
6,000
99
200 H Shares
7,000
189
0 H Shares
0.63%
7,000
53
200 H Shares
8,000
204
0 H Shares
0.60%
8,000
65
200 H Shares
9,000
138
0 H Shares
0.59%
9,000
50
200 H Shares
10,000
1,050
0 H Shares
0.57%
10,000
417
200 H Shares
20,000
491
0 H Shares
0.52%
20,000
531
200 H Shares

<<<PAGE 15>>>
15
NO. OF 
H SHARES 
APPLIED FOR
NO. OF 
VALID 
APPLICATIONS BASIS OF ALLOTMENT/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL NO. 
OF H SHARES 
APPLIED FOR
30,000
132
0 H Shares
0.51%
30,000
430
200 H Shares
40,000
478
200 H Shares
0.50%
50,000
180
200 H Shares
0.48%
50,000
45
400 H Shares
60,000
97
200 H Shares
0.47%
60,000
67
400 H Shares
70,000
57
200 H Shares
0.46%
70,000
90
400 H Shares
80,000
25
200 H Shares
0.45%
80,000
98
400 H Shares
90,000
58
400 H Shares
0.44%
100,000
501
400 H Shares
0.43%
100,000
89
600 H Shares
200,000
625
1,600 H Shares
0.80%
300,000
88
1,800 H Shares
0.60%
400,000
51
2,200 H Shares
0.55%
500,000
19
2,600 H Shares
0.52%
600,000
12
3,000 H Shares
0.50%
700,000
13
3,400 H Shares
0.49%
800,000
8
3,800 H Shares
0.48%
900,000
6
4,200 H Shares
0.47%
1,000,000
9
4,600 H Shares
0.46%
1,200,000
6
5,400 H Shares
0.45%
1,400,000
2
6,200 H Shares
0.44%
1,600,000
8
6,400 H Shares
0.40%
1,838,200
35
7,000 H Shares
0.38%
Total
64,456
3,676,600 H Shares
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 16>>>
16
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Allocations of Offer Shares to Cornerstone Investor and/or their close associates with consent 
under Chapter 4.15 of the Guide
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 of 
the Guide to permit the Company to allocate further Offer Shares in the International Offering to 
Cornerstone Investors and/or their close associates as placees, subject to the following conditions:
(a) 
the final offering size of the Global Offering (excluding any additional H Shares which may 
be issued upon exercise of the Over-allotment Option) will be of a total value of at least 
HK$1 billion;
(b) 
none of the Size-based Exemption Participants were existing shareholders of the Company;
(c) 
each of the Directors, chief executive and Controlling Shareholders of the Company has 
confirmed that no Offer Share have been allocated to them or their respective close associated 
under the Size-based Exemption;
(d) 
none of the Size-based Exemption Participants will become core connected person of the 
Company immediately upon the completion of the Global Offering; the Allocation to Size-
based Exemption Participants will not affect the Company’s ability to satisfy its public float 
requirement as prescribed by the Stock Exchange under the waiver from strict compliance 
with the requirements of Rule 8.08(1)(a) (as amended and replaced by Rule 19A.13A) of the 
Listing Rules
(e) 
details of the allocation to Cornerstone Investors and/or their close associates will be 
disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange. For details of the allocations of Offer Shares to the Cornerstone 
Investors and/or their close associates, please refer to the section headed “Allotment Results 
Details – Allottees with Waivers/Consents Obtained” in this announcement.

<<<PAGE 17>>>
17
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a consent under paragraph 1C of the Placing 
Guidelines to permit the Company to allocate the Offer Shares in the International Offering to the connected clients. The allocation of Offer 
Shares to such connected clients is in compliance with all the conditions under the consent granted by the Stock Exchange. Details of the 
placement to connected clients are set out below:
No.
Connected Clients
Connected Distributor
Relationship with 
the Connected Distributor
Basis of 
holding securities
Number of 
Offer Shares 
(rounded down to 
nearest whole 
board lots of 
200 Shares) 
to be allocated 
to the connected 
client
Appropriate 
percentage of 
total number 
of Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
Approximate 
percentage of 
total Shares 
in issue 
immediately 
following the 
completion of 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
1.
Huatai Capital Investment  
Limited (“HTCI”)(1)
Huatai Financial Holdings 
(Hong Kong) Limited 
(“Huatai”)
HTCI and Huatai are group companies 
within the same group
Non-discretionary
403,600
1.10%
0.27%
2.
CSOP Asset Management  
Limited (“CSOP AM”)(2)
Huatai
CSOP AM and Huatai are group 
companies within the same group
Discretionary
20,000
0.05%
0.01%
3.
CITIC Securities International Capital 
Management Limited (“CSI”)(3)
CLSA Limited (“CLSA”)
CSI and CLSA are group companies 
within the same group
Non-discretionary
182,600
0.50%
0.12%
4.
CITIC Securities Asset Management 
Company Limited (“CITIC 
SAMC”)(4)
CLSA
CITIC AMC and CLSA are group 
companies within the same group
Discretionary
36,000
0.10%
0.02%
5.
China Asset Management (Hong Kong) 
Limited (“China AMC (HK)”)(5)
CLSA
China AMC (HK) and CLSA are group 
companies within the same group
Discretionary
1,556,000
4.23%
1.06%
Futu Securities International 
(Hong Kong) Limited 
(“Futu”)
One of the public funds managed by 
ChinaAMC (HK) is distributed by 
Futu and ultimately 74.29% held by 
Futu’s clients.
6.
ABCI Asset Management Limited 
(“ABCI AM”)(6)
ABCI Capital Limited 
(“ABCI Capital”) 
and ABCI Securities 
Company Limited (“ABCI 
Securities”)
ABCI AM, ABCI Capital and ABCI 
Securities are group companies 
within the same group
Discretionary
1,000
0.003%
0.001%

<<<PAGE 18>>>
18
Notes:
1. 
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public 
offerings (“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products issued by 
appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. In 
connection with such products, the licensed domestic securities firms, through their Hong Kong affiliates, may 
participate in Hong Kong IPOs either as placees or cornerstone investors (the “Cross-border Derivatives 
Trading Regime”).
Huatai Securities Co., Ltd. (“Huatai Securities”), the shares of which are listed on both the Shanghai Stock 
Exchange (stock code: 601688) and the Stock Exchange (stock code: 6886), is one of the domestic securities 
firms licensed to undertake cross-border derivatives trading activities. Huatai Securities entered into an ISDA 
agreement (the “ISDA Agreement”) with its indirectly wholly-owned subsidiary, HTCI, to set out the principal 
terms of any future total return swap between Huatai Securities and HTCI.
Huatai is the Sole Sponsor and one of the Overall Coordinators and Underwriters in connection with the Global 
Offering. Pursuant to an ISDA agreement entered into between Huatai Securities and HTCI, HTCI will hold 
the beneficial interest of the Offer Shares on a non-discretionary basis as the single underlying holding under 
a back-to-back total return swap (“Huatai Back-to-back TRS”) to be entered by HTCI in connection with a 
Client TRS (as defined below) placed by and fully funded (i.e. with no financing provided by HTCI) by Huatai 
Ultimate Clients (as defined below), by which, HTCI will, subject to customary fees and commissions, pass the 
full economic exposure of the Offer Shares ultimately to the Huatai Ultimate Clients, which in effect, HTCI will 
hold the beneficial interest of the Offer Shares on behalf of the Huatai Ultimate Clients.
HTCI and Huatai are both indirectly wholly-owned subsidiaries of Huatai Securities. Accordingly, HTCI is 
considered as a “connected client” of Huatai pursuant to paragraph 1B(7) of the Placing Guidelines.
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (“Huatai Ultimate Clients”) 
cannot directly subscribe for the Offer Shares but may invest in derivative products issued by domestic 
securities firms licenced to undertake cross-border derivatives trading activities, such as Huatai Securities, 
with the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, the Huatai 
Ultimate Clients, through their investment managers, will place a total return swap order (“Client TRS”) with 
Huatai Securities in connection with the Company’s IPO and Huatai Securities will place a Huatai Back-to-back 
TRS order to HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the Huatai Back-
to-back TRS, HTCI participates in the Company’s IPO and subscribes the Offer Shares through placing order 
with Huatai during the International Offering.
To the best of HTCI’s knowledge and after making all reasonable enquiries, each of the Huatai Ultimate Clients 
is an independent third party of (i) the Company, the connected person and/or their respective associates thereof, 
and (ii) HTCI, Huatai and the companies which are members of the same group of HTCI.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Huatai Back-to-back TRS in 
connection with the Client TRS order placed by the Huatai Ultimate Clients. Pursuant to the terms of the 
contracts of the Huatai Back-to-back TRS and the Client TRS, during the tenor of the Huatai Back-to-back TRS 
and the Client TRS, subject to customary fees and commissions, all economic returns of the Offer Shares will be 
ultimately passed to the Huatai Ultimate Clients through the Huatai Back-to-back TRS and the Client TRS and 
all economic loss shall be ultimately borne by the Huatai Ultimate Clients. HTCI will not take any economic 
return or bear any economic loss in relation to the Offer Shares.

<<<PAGE 19>>>
19
Investment in the Huatai Back-to-back TRS and the Client TRS is similar to the investment in a qualified 
domestic institutional investor fund (“QDII”) in the way that the Huatai Ultimate Clients would reap all the 
economic benefits of the underlying Offer Shares, except that a QDII fund would pass through the exchange rate 
exposure on both the notional value of the investment and the profit and loss of the investment. In contrast, the 
profit and loss of the Huatai Back-to-back TRS and the Client TRS factor into account the fluctuation in RMB 
exchange rate upon termination of the Client TRS by converting the profit and loss using the current exchange 
rate at the time of termination. As such, the Huatai Ultimate Clients would bear the exchange rate exposure of 
the profit and loss on settlement date.
The Huatai Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time 
from the issue date of the Client TRS which should be on or after the date on which the Offer Shares are listed 
on the Stock Exchange at their own discretions. Upon the termination upon maturity or early termination of 
the Client TRS by the Huatai Ultimate Clients, HTCI will dispose the Offer Shares on the secondary market 
and the Huatai Ultimate Clients will receive a final settlement amount in cash in accordance with the terms and 
conditions of the Huatai Back-to-back TRS and the Client TRS which should have taken into account all the 
economic returns or economic loss in relation to the Offer Shares. If upon the maturity of the Client TRS, the 
Huatai Ultimate Clients intend to extend the investment period, subject to further agreement between Huatai 
Securities and the relevant Huatai Ultimate Clients, the term of the Client TRS could be extended by way of a 
new issuance or a tenor extension. Accordingly, Huatai Securities will extend the term of the Huatai Back-to-
back TRS by way of a new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass 
through the economic exposure to the Huatai Ultimate Clients, each being an onshore client who places a Client 
TRS order with Huatai Securities in connection with the IPO of the Company. HTCI will not exercise the voting 
right of the Offer Shares during the tenor of the Huatai Back-to-back TRS.
During the life of the Client TRS and Huatai Back-to-back TRS, HTCI may continue to hold the Offer Shares 
in its custodian account, or to hold some or all of the Offer Shares in a prime brokerage account for stock 
borrowing purposes, HTCI will lend out its holding of underlying Offer Shares in the form of stock borrowing 
loans consistent with market practice to lower its finance costs, provided that HTCI has the ability to call back 
the Offer Shares on loan at any time in order to satisfy its obligations under the Huatai Back-to-back TRS to 
ensure the economic interests are ultimately passed to the Huatai Ultimate Clients.
2. 
CSOP AM is the discretionary investment manager of China New Balance Opportunity Fund (the “CSOP AM 
Ultimate Client”) whose investors are, to the best of CSOP AM’s knowledge, independent third parties of 
the Connected Clients, Huatai and the companies which are members of the same group of Huatai. The only 
ultimate beneficial owner holding 30% or more interest of the CSOP AM Ultimate Client is CMB Wing Lung 
(Nominee) Ltd. CSOP AM makes investment decisions for CSOP AM Ultimate Client.
Huatai indirectly holds 21.609% shares of CSOP AM. CSOP AM is therefore considered as a connected client 
of Huatai pursuant to paragraph 1B(7) of the Placing Guidelines.

<<<PAGE 20>>>
20
3. 
CSI will act as the single counterparty of a back-to-back total return swap transaction (the “CSI Back-to-
back TRS”) to be entered into by CSI in connection with a total return swap order (the “CSI Client TRS”) 
placed and fully funded by its ultimate clients (the “CSI Ultimate Client(s)”), by which CSI will pass the full 
economic exposure of the Offer Shares placed to CSI to the CSI Ultimate Clients.
CSI will hold the Offer Shares but will contractually agree to pass on the full economic exposure to the CSI 
Ultimate Clients, on a non-discretionary basis. The CSI Ultimate Client may exercise an early termination right 
to early terminate the CSI Client TRS at any time from the trade date of the CSI Client TRS which should 
be on or after the date on which the Offer Shares are listed on the Stock Exchange. Upon the final maturity 
or termination of the CSI Client TRS by the CSI Ultimate Client, CSI will dispose of the Offer Shares on the 
secondary market and the CSI Ultimate Client will receive a final termination amount of the CSI Back-to-back 
TRS which will taken into account all the economic returns or economic loss in relation to the Offer Shares and 
the fixed amount of transaction fees of the CSI Back-to-back TRS and the CSI Client TRS. CSI will not exercise 
the voting right of the Offer Shares during the terms of the CSI Back-to-back TRS.
To the best of CSI’s knowledge after having made all reasonable inquiries, each of the CSI Ultimate Clients is 
an independent third party of the Company its subsidiaries, CSI, CLSA and the companies which are members 
of the same group of CLSA.
CSI is a wholly owned subsidiary of CITIC Securities Investment Limited (“CITIC Securities Investment”), 
which is wholly owned by CITIC Securities Company Limited (中信証券股份有限公司) (“CITIC Securities”). 
CITIC Securities is the holding company of CLSA, one of the Overall Coordinators and Underwriters of the 
Global Offering. Therefore, CSI and CLSA are members of the same group of companies and CSI is a connected 
client of CLSA. The participation of CSI as placee in the International Offering would constitute an allocation 
to connected clients of the CLSA.
4. 
CITIC SAMC is a wholly owned subsidiary of CITIC Securities Investment, which is wholly owned by CITIC 
Securities. CITIC Securities is the holding company of CLSA, one of the Overall Coordinators and Underwriters 
of the Global Offering. Therefore, CITIC SAMC and CLSA are members of the same group of companies and 
CITIC SAMC is a connected client of CLSA. The participation of CITIC SAMC as placee in the International 
Offering would constitute an allocation to connected clients of the CLSA.
CITIC SAMC will hold the Offer Shares on behalf of underlying funds who are independent third parties on 
a discretionary basis. To the best of CITIC SAMC’s knowledge, none of the ultimate beneficial owners holds 
more than 30% ultimate beneficial interest in the underlying funds.
5. 
ChinaAMC (HK) is a SFC licensed corporation carrying out types 1, 4 and 9 regulated activities in Hong 
Kong. As the discretionary fund manager of the fund which participates in the placing of the International 
Offering, ChinaAMC (HK) is fully responsible for the daily management and make investment decisions for the 
underlying investors. All participants in the placing are Hong Kong based public funds. One of the Hong Kong-
based public funds participating in the International Offering under the management of ChinaAMC (HK) is 
distributed by Futu and ultimately 74.29% held by clients of Futu.
6. 
ABCI AM is a member of the same group of companies as ABCI Capital and ABCI Securities, and ABCI AM is 
therefore a “connected client” of ABCI Capital and ABCI Securities.
ABCI AM intends to hold the Offer Shares in its capacity as manager managing investment portfolios on behalf 
of underlying investors (the “ABCI AM Ultimate Clients”) who are independent third parties on a discretionary 
basis.
To the best knowledge of ABCI AM, each of the ABCI AM Ultimate Clients is an independent third party of the 
Company, its subsidiaries, its substantial shareholders, ABCI Capital, ABCI Securities and the companies which 
are members of the same group of companies as ABCI Capital and ABCI Securities.
ABCI AM also confirms that it will not hold any Offer Shares placed to it on a proprietary basis for itself or for 
any group member of ABCI, and will be held by it on behalf of independent third parties.

<<<PAGE 21>>>
21
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
Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated 31 December 2025 issued by Yunnan Jinxun 
Resources Co., Ltd. for detailed information about the Global Offering described below before 
deciding whether or not to invest in the Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Joint Representatives (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the 
occurrence of any of the events set out in the paragraph headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Hong Kong Underwriting 
Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong 
Kong time) on the Listing Date (which is currently expected to be on 9 January 2026).

<<<PAGE 22>>>
22
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering (before any exercise of the Over-
allotment Option), based on the Offer Price of HK$30.00 per H Share:
(1) 
36,765,600 H Shares, representing approximately 25.0% of the total number of issued 
Shares will be counted towards the public after Listing, which will satisfy the public float 
requirement under Rule 19A.13A of the Listing Rules; and
(2) 
the Company satisfies the free float requirement pursuant to Rule 19A.13C(1) of the Listing 
Rules.
COMMENCEMENT OF DEALINGS
H Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, January 
9, 2026 (Hong Kong time), provided that the Global Offering has become unconditional in all 
respects and the right of termination described in the paragraph headed “Grounds for Termination” 
under the section headed “Underwriting” in the Prospectus has not been exercised and has lapsed. 
Investors who trade H Shares prior to the receipt of H Share certificates or the H Share certificates 
becoming valid evidence of title do so entirely at their own risk.
Assuming that the Hong Kong Public Offering becomes unconditional at or before 8:00 a.m. in 
Hong Kong on Friday, January 9, 2026, it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Friday, January 9, 2026. The H Shares will be traded in 
board lots of 200 Shares each. The stock code of the H Shares will be 3636.
By order of the Board
Yunnan Jinxun Resources Co., Ltd.
Mr. Yuan Rong
Chairman of the Board, Executive Director and Chief Executive Officer
Hong Kong, January 8, 2026
As at the date of this announcement, the Board comprises (i) Mr.Yuan Rong, Ms. Yuan Mei and 
Mr. Yang Yongchang as executive Directors; and (ii) Ms. Zheng Dongyu, Mr. Xia Hongying and 
Mr. Wong Hok Bun Mario as independent non-executive Directors.
