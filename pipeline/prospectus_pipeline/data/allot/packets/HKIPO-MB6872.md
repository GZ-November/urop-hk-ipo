# 配发结果公告抽取任务：6872.HK TenNor Therapeutics (Suzhou) Limited - B - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**21/05/2026 19:43**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0521/2026052101298.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6872.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
transferred within the United States, except that the Offer Shares may be offered, sold or delivered (a) in the United 
States to a limited number of institutional “accredited investors” (as defined in Rule 501(a) under the U.S. Securities 
Act) in reliance on the Rule 506 safe harbor under the U.S. Securities Act; or (b) outside the United States in offshore 
transactions in reliance on Regulation S. There will be no public offer of the Offer Shares in the United States.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
May 14, 2026 (the “Prospectus”) issued by TenNor Therapeutics (Suzhou) Limited (丹諾醫藥(蘇州)股份有限公
司) (the “Company”) for detailed information about the Global Offering described below before deciding whether or 
not to invest in the H Shares thereby being offered. Any investment decision in relation to the Offer Shares should be 
taken solely in reliance on the information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
In connection with the Global Offering, CLSA Limited, as stabilizing manager (the “Stabilizing Manager”), or any 
person acting for it, on behalf of the Underwriters, may over-allocate or effect transactions with a view to stabilizing 
or supporting the market price of the H Shares at a level higher than that which might otherwise prevail for a limited 
period after the Listing Date. However, there is no obligation on the Stabilizing Manager (or any person acting for it) 
to conduct any such stabilizing action, which, if commenced, will be done at the sole and absolute discretion of the 
Stabilizing Manager (or any person acting for it) and may be discontinued at any time. Any such stabilizing action is 
required to be brought to an end on the 30th day after the last day for the lodging of applications under the Hong Kong 
Public Offering. Such stabilizing action, if taken, may be effected in all jurisdictions where it is permissible to do so, 
in each case in compliance with all applicable laws, rules and regulatory requirements, including the Securities and 
Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities 
and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that stabilizing action cannot be taken to support the price of the H Shares for 
longer than the stabilization period which begins on the Listing Date and is expected to expire on the 30th day after 
the last day for the lodging of applications under the Hong Kong Public Offering. After this date, no further stabilizing 
action may be taken, and demand for the H Shares and the price of the H Shares could fall.
The Overall Coordinators confirm that there has been no over-allocation of the H Shares under the International 
Offering, therefore, there will not be any delayed delivery arrangement and the Over-allotment Option will not be 
exercised. In view of the fact that there has been no over-allocation of the H Shares under the International Offering, 
no stabilising action as described in the Prospectus will be taken during the stabilisation period.
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on behalf of 
the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Underwriting Agreement – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
Friday, May 22, 2026).

<<<PAGE 2>>>
М੽Ԛ哦
TenNor Therapeutics (Suzhou) Limited
丹諾醫藥( 蘇州) 股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under
the Global Offering
:
8,856,000 H Shares (taking into account the 
 partial exercise of the Offer Size 
 Adjustment Option)
Number of Hong Kong Offer Shares
:
828,100 H Shares
Number of International Offer Shares
:
8,027,900 H Shares (taking into account the 
 partial exercise of the Offer Size 
 Adjustment Option)
Offer Price
:
HK$75.70 per H Share, plus brokerage of
 1.0%, SFC transaction levy of 0.0027%,
 AFRC transaction levy of 0.00015% and
 Hong Kong Stock Exchange trading fee of
 0.00565% (payable in full on application in
 Hong Kong dollars and subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
6872
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and 
Joint Lead Managers
Joint Bookrunners and/or Joint Lead Managers

<<<PAGE 3>>>
1 
 
TenNor Therapeutics (Suzhou) Limited 
丹諾醫藥(蘇州)股份有限公司 
ANNOUNCEMENT OF ALLOTMENT RESULTS 
Unless otherwise defined herein, capitalised terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated May 14, 2026 (the “Prospectus”) 
issued by TenNor Therapeutics (Suzhou) Limited (the “Company”). 
 
Warning: In view of high concentration of shareholding in a small number of Shareholders, Shareholders 
and prospective investors should be aware that the price of the H Shares could move substantially even with 
a small number of H Shares traded and should exercise extreme caution when dealing in the H Shares. 
SUMMARY 
Company Information 
Stock Code 
6872 
Stock short name 
TENNOR THERAP-B 
Dealings commencement date 
May 22, 2026* 
*see note at the end of the announcement 
Price Information 
Offer Price 
HK$75.70 
 
Offer Shares and Share Capital 
Number of Offer Shares (taking into account the partial 
exercise of the Offer Size Adjustment Option ) 
8,856,000 
Number of Offer Shares in Hong Kong Public Offering  
828,100 
Number of Offer Shares in International Offering (taking into 
account the partial exercise of the Offer Size Adjustment 
Option) 
8,027,900 
Number of issued Shares upon Listing 
52,328,926 
The number of Offer Shares above is determined after taking into account the additional Offer Shares issued 
under the following Offer Size Adjustment Option. 
 
Offer Size Adjustment Option (Upsize option) 
Number of additional Offer Shares issued under the option 
575,450 
-  Hong Kong Public Offering 
N/A 
-  International Offering 
575,450 
The Offer Size Adjustment Option has been partially exercised , pursuant to which the Company is issuing 
and allotting 575,450 additional Offer Shares, representing approximately 6.95% of the total number of 
Offer Shares initially available under the Global Offering, at the Offer Price. 
 
Over-allocation 
Number of Offer Shares over-allocated 
N/A 
There has been no over-allocation of Offer Shares in the International Offering. Therefore, the Over-
allotment Option will not be exercised. 

<<<PAGE 4>>>
2 
 
 
Proceeds  
Gross proceeds (Note) 
HK$670.4 million 
Less: Estimated listing expenses payable based on the Offer 
Price 
HK$(72.1) million 
Net proceeds 
HK$598.3 million 
 
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The 
Company intends to apply the additional net proceeds from the exercise of the Offer Size Adjustment Option 
for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus on a 
pro rata basis. 
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING 
 
No. of valid applications 
275,978 
No. of successful applications 
16,562 
Subscription level 
9,015.11 times 
Claw-back triggered 
N/A  
No. of Offer Shares initially available under the Hong Kong Public 
Offering 
828,100 
No. Offer Shares reallocated from the International Offering  
0 
Final no. of Offer Shares under the Hong Kong Public Offering 
828,100 
% of Offer Shares under the Hong Kong Public Offering to the Global 
Offering (taking into account the partial exercise of the Offer Size 
Adjustment Option) 
9.35% 
 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by name or identification document number or 
www.hkeipo.hk/IPOResult for the full list of allottees. 
INTERNATIONAL OFFERING 
 
No. of placees 
81 
Subscription Level 
9.24 times 
No. of Offer Shares initially available under the International Offering 7,452,450 
No. of Offer Shares reallocated to the Hong Kong Public Offering 
0 
Final no. of Offer Shares under the International Offering (taking into 
account the partial exercise of the Offer Size Adjustment Option) 
8,027,900 
% of Offer Shares under the International Offering to the Global 
Offering (taking into account the partial exercise of the Offer Size 
Adjustment Option) 
90.65% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for a waiver from strict 
compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) of Appendix F1 to the 
Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange to permit the Company to allocate 
certain Offer Shares in the International Offering to certain existing Shareholders and/or their close associates; 

<<<PAGE 5>>>
3 
 
(i) none of the Offer Shares subscribed by the placees and the public have been financed directly or indirectly by 
the Company, any of the Directors, chief executive of the Company, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates; and (ii) none of the 
placees and the public who have purchased the Offer Shares are accustomed to taking instructions from the 
Company, any of the Directors, chief executive of the Company, substantial Shareholders, existing Shareholders 
of the Company or any of its subsidiaries or their respective close associates in relation to the acquisition, 
disposal, voting or other disposition of H Shares registered in his/her/its name or otherwise held by him/her/it. 
The placees in the International Offering include the following: 
Cornerstone Investors  
Investor Note 1 
No. of Offer 
Shares allocated 
Approximate % of 
total number of 
Offer Shares (after 
taking into account 
the partial exercise 
of the Offer Size 
Adjustment Option) 
Approximate % of 
total issued share 
capital in the 
Company after the 
Global Offering (after 
taking into account 
the partial exercise of 
the Offer Size 
Adjustment Option) 
Existing shareholders 
or their close associates 
Note 2  
AMR Action Fund, L.P. 
(“AMR US”) 
1,520,000  
17.16% 
2.90% 
Yes 
AMR Action Fund, 
SCSp (“AMR 
Luxembourg”) 
527,600 
5.96% 
1.01% 
Yes 
Hua Yuan International 
Limited (華圓管理諮詢
(香港)有限公司) 
(“Hua Yuan”) 
620,850 
7.01% 
1.19% 
Yes 
Orient Asset 
Management (Hong 
Kong) Limited (東方資
產管理(香港)有限公
司) (“Orient Asset 
Management”) 
310,500 
3.51% 
0.59% 
No 
June Star Global 
Limited (駿昇環球有限
公司) (“June Star”) 
103,500 
1.17% 
0.20% 
No 
Total 
3,082,450 
34.81% 
5.89% 
 
Note:  
1. 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone 
Investors” in the Prospectus. 
2. 
Among the Cornerstone Investors, each of AMR US and AMR Luxembourg is an existing Shareholder 
of the Company, and Hua Yuan is a close associate of Suzhou Industrial Park Origin Ventures Co., 
Ltd. (蘇州工業園區原點創業投資有限公司), which is an existing Shareholder of the Company. The 
Stock Exchange has granted a waiver from strict compliance with the requirements under Rule 10.04 
of the Listing Rules and consent under Paragraph 1C(2) of the Placing Guidelines to permit 
subscription of the Offer Shares by existing Shareholders of the Company and/or their close associates 
as cornerstone investors. Please refer to the section headed “Waivers from Strict Compliance with 

<<<PAGE 6>>>
4 
 
Listing Rules – Cornerstone Subscription by Existing Shareholders or Close Associate of an Existing 
Shareholder” of the Prospectus for details. 
 
 
Allotees with Waivers/Consents Obtained 
Investor 
No. of Offer 
Shares 
allocated 
Approximate % of 
total number of 
Offer Shares (after 
taking into account the 
partial exercise of the 
Offer Size Adjustment 
Option) 
Approximate % of 
total issued share 
capital in the 
Company after the 
Global Offering (after 
taking into account the 
partial exercise of the 
Offer Size Adjustment 
Option) 
Relationship 
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by existing 
Shareholders and/or their close associates  
AMR US Note 1 
1,520,000  
17.16% 
2.90% 
An existing 
Shareholder and a 
Cornerstone Investor 
AMR Luxembourg 
Note 1 
527,600 
5.96% 
1.01% 
An existing 
Shareholder and a 
Cornerstone Investor 
Hua Yuan Note 1 
620,850 
7.01% 
1.19% 
A close associate of 
an existing 
Shareholder and a 
Cornerstone Investor 
Mr. Hu Zhibin Note 2 
155,350 
1.75% 
0.30% 
A close associate of 
an existing 
Shareholder 
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for 
New Listing Applicants in relation to allocations to connected clients Note3 
CITIC Securities 
International Capital 
Management Limited 
(“CSI”) 
6,000 
0.07% 
0.01% Connected client as a 
placee 
CITIC Securities 
Asset Management 
Company Limited 
(“CITIC Asset 
Management”)  
200 
0.00% 
0.00% Connected client as a 
placee 
CITIC Securities 
Asset Management 
(HK) Limited 
(“CITIC AM HK”) 
200 
0.00% 
0.00% Connected client as a 
placee 
China Asset 
Management (Hong 
Kong) Limited 
(“China AMC HK”) 
 
600 
0.01% 
0.00% Connected client as a 
placee 

<<<PAGE 7>>>
5 
 
Notes: 
1. 
The Stock Exchange has granted a waiver from strict compliance with the requirements under Rule 
10.04 of the Listing Rules and consent under Paragraph 1C(2) of the Placing Guidelines to permit 
subscription of the Offer Shares by existing Shareholders of the Company and/or their close associates 
as cornerstone investors. Please refer to the section headed “Waivers from Strict Compliance with 
Listing Rules – Cornerstone Subscription by Existing Shareholders or Close Associate of an Existing 
Shareholder” of the Prospectus for details. 
2. 
Mr. Hu Zhibin (“Mr. Hu”, disclosed as Mr. Hu Zhibing in the Prospectus) is a close associate of 
Changzhou Borun Mingdu Emerging Industry Private Equity Investment Fund Partnership (Limited 
Partnership)(常州博潤明都新興產業創業投資中心)(“Borun Mingdu”). Borun Mingdu holds 
approximately 0.50% of the total issued share capital of the Company immediately prior to the 
completion of the Global offering and are not and will not become (upon the completion of the Global 
Offering) a core connected person of the Company. As disclosed in the Prospectus, Borun Mingdu is 
a limited partnership established under the laws of the PRC and is managed by its general partner, 
Shanghai Broad Resources Investment Management Co., Ltd. (上海博潤投資管理有限公司), which 
is ultimately controlled by Mr. Hu as to 57.60%, an Independent Third Party. As such, Mr. Hu is a 
close associate of Borun Mingdu. For details, please refer to the section headed “Others / Additional 
Information – Placing to existing Shareholders and/or their close associates with prior consent under 
paragraph 1C(2) of the Placing Guidelines” in this announcement. 
3. 
For details of the consent under paragraph 1C of the Placing Guidelines and Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations to connected clients, please refer to the 
section headed “Others / Additional Information – Placing to connected clients with a prior 
consent under paragraph 1C(1) of the Placing Guidelines” in this announcement. 
 
LOCK-UP UNDERTAKINGS 
Cornerstone Investors  
Name 
Number of Shares held in 
the Company subject to 
lock-up undertakings 
upon Listing 
Approximate % of total 
issued share capital in the 
Company after the Global 
Offering subject to lock-up 
undertakings upon Listing 
Note 1 
Last day subject to the 
lock-up undertakingsNote 2  
AMR US 
1,520,000  
2.90% 
November 21, 2026 
AMR Luxembourg 
527,600 
1.01% 
November 21, 2026 
Hua Yuan 
620,850 
1.19% 
November 21, 2026 
Orient Asset Management 
310,500 
0.59% 
November 21, 2026 

<<<PAGE 8>>>
6 
 
June Star 
103,500 
0.20% 
November 21, 2026 
Total 
3,082,450 
5.89% 
 
Note: 
1. Taking into account the partial exercise of the Offer Size Adjustment Option. 
2. In accordance with the relevant cornerstone investment agreements, the required lock-up ends on 
November 21, 2026, being six months following the Listing Date. The Cornerstone Investors will 
cease to be prohibited from disposing of or transferring H Shares subscribed for pursuant to the 
relevant cornerstone investment agreements after the indicated date.  
 
Pre-IPO Investors  
NameNote 1 
Number of Shares held in 
the Company subject to 
lock-up undertakings 
upon Listing 
Approximate % of total 
issued share capital in the 
Company after the Global 
Offering subject to lock-up 
undertakings upon Listing 
Note 2
Last day subject to the 
lock-up undertakingsNote 3 
and Note 4
Cumbre 
6,153,028
11.76%
May 21, 2027 
Big Bend 77 
1,466,857
2.80%
May 21, 2027 
Big Bend 72 
448,108
0.86%
May 21, 2027 
Big Bend 73 
117,357
0.22%
May 21, 2027 
AMR US 
2,322,755
4.44%
May 21, 2027 
AMR Luxembourg 
805,956
1.54%
May 21, 2027 
WuXi Fund 
2,848,109
5.44%
May 21, 2027 
Suzhou Origin 
2,203,545
4.21%
May 21, 2027 
WuXi Guolian 
450,395
0.86%
May 21, 2027 
Immense Vantage 
2,450,497
4.68%
May 21, 2027 
Zhongshan Xiwan 
Industrial Development 
863,510
1.65%
May 21, 2027 
Zhongshan Venture Fund 
647,634
1.24%
May 21, 2027 
Zhongshan Cuiheng 
647,632
1.24%
May 21, 2027 
Zhongshan Xiwan 
Investment 
215,877
0.41%
May 21, 2027 
Ningbo Xiangshang 
600,527
1.15%
May 21, 2027 
Ningbo Yaoshang 
450,395
0.86%
May 21, 2027 
Ningbo Yanyuan 
450,395
0.86%
May 21, 2027 
Ningbo Borong 
300,263
0.57%
May 21, 2027 
Ningbo Rongshun 
140,319
0.27%
May 21, 2027 
MAL Investment 
773,134
1.48%
May 21, 2027 

<<<PAGE 9>>>
7 
 
Chao Interests 
773,134
1.48%
May 21, 2027 
Relativity Healthcare 
352,472
0.67%
May 21, 2027 
Suzhou GTJA 
723,385
1.38%
May 21, 2027 
Yantai GTJA 
600,527
1.15%
May 21, 2027 
Suzhou Chenghe 
477,668
0.91%
May 21, 2027 
Nongyin No. 2 
1,373,641
2.63%
May 21, 2027 
Susui Investment 
151,114
0.29%
May 21, 2027 
Beisen Dankang 
1,436,554
2.75%
May 21, 2027 
Hainan Century Star River 
1,351,186
2.58%
May 21, 2027 
Yuanjing Investment 
1,079,386
2.06%
May 21, 2027 
Kangnuo 
863,509
1.65%
May 21, 2027 
Ms. Frances McGary 
McKnight 
170,699
0.33%
May 21, 2027 
Ms. Grace Gillespie 
McKnight 
170,699
0.33%
May 21, 2027 
Mr. John Stevens 
McKnight 
170,699
0.33%
May 21, 2027 
Ms. Nell Lanier McKnight 
170,699
0.33%
May 21, 2027 
Mr. Steven Lanier 
McKnight 
77,313
0.15%
May 21, 2027 
Garcia – Bugge’ 
Enterprises, Inc. 
669,475
1.28%
May 21, 2027 
Huzhou Zhongnuo 
600,527
1.15%
May 21, 2027 
Mr. William J. Rieflin 
544,150
1.04%
May 21, 2027 
Qianrong Yingrun 
457,881
0.88%
May 21, 2027 
Yuankang Dingxiang 
366,305
0.70%
May 21, 2027 
Yangzhou Jinye 
327,445
0.63%
May 21, 2027 
Borun Mingdu 
215,877
0.41%
May 21, 2027 
Mr. Wang Xiaodong 
77,313
0.15%
May 21, 2027 
Beijing Jingguo Chuang 
2,159
0.00%
May 21, 2027 
Total 
37,560,110
71.78%
 
Notes: 
1. Please refer to the section headed “History, Development and Corporate Structure — Pre-IPO 
Investments — Information about Our Principal Pre-IPO Investors” in the Prospectus for details of 
the Pre-IPO Investors. 
2. Taking into account the partial exercise of the Offer Size Adjustment Option. 
3. The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company 
Law.  
4. The number of Shares held by AMR US, AMR Luxembourg, Suzhou Origin and Borun Mingdu in 
the table above does not take into account the Shares to be subscribed by them and/or their 

<<<PAGE 10>>>
8 
 
respective close associates in the Global Offering. The Company has applied to the Stock Exchange 
for, and the Stock Exchange has granted to the Company, a waiver from strict compliance with Rule 
10.04 of the Listing Rules and consent under paragraph 1C(2) of the Placing Guidelines to permit 
the Company to allocate such Offer Shares in the International Offering to themselves and/or their 
respective close associates. For details, please refer to the sections headed “Allottees with 
Waivers/Consents Obtained” in this announcement. 
 
 
Existing Shareholders (other than the Pre-IPO Investors as defined in the Prospectus) 
 
Name 
Number of Shares held in 
the Company subject to 
lock-up undertakings 
upon Listing 
Approximate % of total 
issued share capital in the 
Company after the Global 
Offering subject to lock-up 
undertakings upon Listing 
Note 1
Last day subject to the 
lock-up undertakingsNote 2 
Dr. Ma Zhenkun 
1,372,670
2.62%
May 21, 2027 
Danyuan Kangnuo 
2,180,237
4.17%
May 21, 2027 
Danyuan Aonuo 
1,780,987
3.40%
May 21, 2027 
Danyuan Nuokang 
578,922
1.11%
May 21, 2027 
Total 
5,912,816
11.30%
 
Notes: 
1. Taking into account the partial exercise of the Offer Size Adjustment Option. 
2. The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company 
Law. 
 
 

<<<PAGE 11>>>
9 
 
PLACEE CONCENTRATION ANALYSIS 
Placees* 
Number of H Shares 
allotted 
Allotment as % of 
International Offering 
(after taking into account 
the partial exercise of the 
Offer Size Adjustment 
Option) 
Allotment as % of total 
Offer Shares (after taking 
into account the partial 
exercise of the Offer Size 
Adjustment Option) 
Number of H Shares held 
upon Listing 
% of total issued share 
capital in the Company 
upon Listing 
(after taking into account 
the partial exercise of the 
Offer Size Adjustment 
Option) 
Top 1 
2,047,600 
25.51% 
23.12% 
5,176,311 
9.89% 
Top 5 
4,986,700 
62.12% 
56.31% 
10,769,351 
20.58% 
Top 10 
6,618,100 
82.44% 
74.73% 
12,400,751 
23.70% 
Top 25 
7,999,900 
99.65% 
90.33% 
13,782,551 
26.34% 
 
Note: 
* 
Ranking of placees is based on the number of H Shares allotted to the placees.  
 
 

<<<PAGE 12>>>
10 
 
H SHAREHOLDER CONCENTRATION ANALYSIS  
H 
Shareholders 
* 
Number of H Shares 
allotted 
Allotment as % of 
International Offering 
(after taking into 
account the partial 
exercise of the Offer 
Size Adjustment 
Option) 
Allotment as % of 
total Offer Shares 
(after taking into 
account the partial 
exercise of the Offer 
Size Adjustment 
Option) 
Number of H Shares 
held upon Listing 
% of total issued H 
share capital in the 
Company upon Listing 
(after taking into 
account the partial 
exercise of the Offer 
Size Adjustment 
Option) 
Number of Shares 
held upon Listing 
Top 1 
0 
0.00% 
0.00% 
8,185,350 
15.64% 
8,185,350 
Top 5 
2,668,450 
33.24% 
30.13% 
25,397,376 
48.53% 
25,397,376 
Top 10 
2,668,450 
33.24% 
30.13% 
35,864,745 
68.54% 
35,864,745 
Top 25 
5,564,750 
69.32% 
62.84% 
48,264,454 
92.23% 
48,264,454 
 
Note: 
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing. 
 
 

<<<PAGE 13>>>
11 
 
SHAREHOLDER CONCENTRATION ANALYSIS 
Shareholders* 
Number of H Shares 
allotted 
Allotment as % of 
International Offering 
(after taking into account 
the partial exercise of the 
Offer Size Adjustment 
Option) 
Allotment as % of total 
Offer Shares (after taking 
into account the partial 
exercise of the Offer Size 
Adjustment Option) 
Number of Shares held 
upon Listing# 
% of total issued share 
capital in the Company 
upon Listing 
(after taking into account 
the partial exercise of the 
Offer Size Adjustment 
Option) 
Top 1 
0 
0.00% 
0.00% 
8,185,350 
15.64% 
Top 5 
2,668,450 
33.24% 
30.13% 
25,397,376 
48.53% 
Top 10 
2,668,450 
33.24% 
30.13% 
35,864,745 
68.54% 
Top 25 
5,564,750 
69.32% 
62.84% 
48,264,454 
92.23% 
 
Note: 
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon Listing. 
 

<<<PAGE 14>>>
12 
 
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
 
 
 
50 
59,975
480 out of 59,975 applicants to receive 50 H Shares 
0.80% 
100 
32,644
345 out of 32,644 applicants to receive 50 H Shares 
0.53% 
150 
7,563
95 out of 7,563 applicants to receive 50 H Shares 
0.42% 
200 
5,301
74 out of 5,301 applicants to receive 50 H Shares 
0.35% 
250 
5,813
89 out of 5,813 applicants to receive 50 H Shares 
0.31% 
300 
3,762
62 out of 3,762 applicants to receive 50 H Shares 
0.27% 
350 
3,033
54 out of 3,033 applicants to receive 50 H Shares 
0.25% 
400 
2,994
56 out of 2,994 applicants to receive 50 H Shares 
0.23% 
450 
1,909
37 out of 1,909 applicants to receive 50 H Shares 
0.22% 
500 
7,162
145 out of 7,162 applicants to receive 50 H Shares 
0.20% 
600 
12,883
280 out of 12,883 applicants to receive 50 H Shares 
0.18% 
700 
2,272
53 out of 2,272 applicants to receive 50 H Shares 
0.17% 
800 
2,246
55 out of 2,246 applicants to receive 50 H Shares 
0.15% 
900 
1,739
45 out of 1,739 applicants to receive 50 H Shares 
0.14% 
1,000 
10,590
283 out of 10,590 applicants to receive 50 H Shares 
0.13% 
1,500 
5,044
159 out of 5,044 applicants to receive 50 H Shares 
0.11% 
2,000 
3,613
128 out of 3,613 applicants to receive 50 H Shares 
0.09% 
2,500 
3,632
140 out of 3,632 applicants to receive 50 H Shares 
0.08% 
3,000 
2,509
104 out of 2,509 applicants to receive 50 H Shares 
0.07% 
3,500 
2,294
102 out of 2,294 applicants to receive 50 H Shares 
0.06% 
4,000 
2,494
116 out of 2,494 applicants to receive 50 H Shares 
0.06% 
4,500 
1,550
76 out of 1,550 applicants to receive 50 H Shares 
0.05% 
5,000 
3,605
184 out of 3,605 applicants to receive 50 H Shares 
0.05% 
6,000 
2,907
160 out of 2,907 applicants to receive 50 H Shares 
0.05% 
7,000 
2,506
146 out of 2,506 applicants to receive 50 H Shares 
0.04% 
8,000 
2,513
155 out of 2,513 applicants to receive 50 H Shares 
0.04% 
9,000 
1,794
116 out of 1,794 applicants to receive 50 H Shares 
0.04% 
10,000 
13,114
881 out of 13,114 applicants to receive 50 H Shares 
0.03% 
20,000 
7,755
688 out of 7,755 applicants to receive 50 H Shares 
0.02% 
30,000 
6,132
641 out of 6,132 applicants to receive 50 H Shares 
0.02% 
40,000 
5,956
698 out of 5,956 applicants to receive 50 H Shares 
0.01% 
50,000 
4,203
539 out of 4,203 applicants to receive 50 H Shares 
0.01% 
60,000 
7,941
1,095 out of 7,941 applicants to receive 50 H Shares 
0.01% 
 
 
 
Total 
239,448 Total number of Pool A successful applicants: 8,281 
 
 
 
 
 

<<<PAGE 15>>>
13 
 
 
 
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
 
 
 
70,000 
5,706
799 out of 5,706 applicants to receive 50 H Shares 
0.01% 
80,000 
4,324
660 out of 4,324 applicants to receive 50 H Shares 
0.01% 
90,000 
2,652
436 out of 2,652 applicants to receive 50 H Shares 
0.01% 
100,000 
11,429
2,010 out of 11,429 applicants to receive 50 H Shares 
0.01% 
200,000 
5,062
1,386 out of 5,062 applicants to receive 50 H Shares 
0.01% 
300,000 
2,646
938 out of 2,646 applicants to receive 50 H Shares 
0.01% 
414,050 
4,711
2,052 out of 4,711 applicants to receive 50 H Shares 
0.01% 
 
 
 
Total 
36,530 
Total number of Pool B successful applicants: 8,281 
 
 
 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries. 
 

<<<PAGE 16>>>
14 
 
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
The Offer Size Adjustment Option has been partially exercised by the Overall Coordinators, pursuant to 
which the Company is issuing and allotting 575,450 additional H Shares, representing approximately 
6.95% of the total number of Offer Shares initially available under the Global Offering, at the Offer 
Price. All of the additional Offer Shares that would be allotted and issued by the Company pursuant to 
the partial exercise of the Offer Size Adjustment Option will be allocated to the International Offering. 
Accordingly, the total number of Offer Shares finally available under the Global Offering (taking into 
account the partial exercise of the Offer Size Adjustment Option) that would be allotted and issued by 
the Company is 8,856,000 H Shares and the total issued share capital of the Company upon Listing 
(taking into account the partial exercise of the Offer Size Adjustment Option) will be 52,328,926 H 
Shares. 
Placing to existing Shareholders and/or their close associates with prior consent under paragraph 
1C(2) of the Placing Guidelines  
The Company has applied to, and the Stock Exchange has granted, a waiver from the strict compliance 
with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) of the Placing Guidelines to 
permit the Company to allocate such Offer Shares in the International Offering to any existing Shareholder 
and/or close associate of existing Shareholders as listed above. Such allocations of Offer Shares are in 
compliance with all the conditions under the waiver/consent granted by the Stock Exchange. 
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates, please 
refer to the section headed “Allotment Results Details – International Offering – Allotees with 
Waivers/Consents Obtained” in this announcement. 
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines  
Under the International Offering, certain Offer Shares were placed to connected clients of their connected 
distributors pursuant to the Placing Guidelines. Details of the placement to connected clients are set out 
below. The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, 
consents under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such Offer 
Shares in the International Offering to the connected clients. The allocation of Offer Shares to such 
connected clients is in compliance with all the conditions under the consent granted by the Stock 
Exchange.  
 
 

<<<PAGE 17>>>
15 
 
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
under which 
the 
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
authorised 
by the SFC 
or is 
expected to 
hold the 
Offer Shares 
on behalf of 
such scheme  
Number of 
Offer Shares to 
be allocated to 
the connected 
client 
Appropriate 
percentage of total 
number of Offer 
Shares (taking into 
account the partial 
exercise of the Offer 
Size Adjustment 
Option) 
Approximate 
percentage of total 
issued share capital 
in the Company 
upon Listing (taking 
into account the 
partial exercise of 
the Offer Size 
Adjustment Option) 
1. 
CLSA 
Limited 
(“CLSA”)  
CITIC 
Securities 
International 
Capital 
Management 
Limited 
(“CSI”) 
CSI is a 
member of 
the same 
group of 
companies as 
CLSA 
Please refer to 
Note (1).  
N 
6,000 
0.0678% 
0.0115% 
 
 
 

<<<PAGE 18>>>
16 
 
Part B - Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties 
 
 
No. Connected 
Distributor 
Connected Client Relationship 
with the 
Connected 
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
Number of Offer 
Shares to be 
allocated to the 
connected client 
Appropriate 
percentage of total 
number of Offer 
Shares (taking into 
account the partial 
exercise of the Offer 
Size Adjustment 
Option) 
Approximate 
percentage of total 
issued share capital in 
the Company upon 
Listing (taking into 
account the partial 
exercise of the Offer 
Size Adjustment 
Option) 
1.  CLSA 
CITIC Securities 
Asset 
Management 
Company Limited 
(“CITIC Asset 
Management”)  
 
Please refer to 
Note (2). 
CITIC Asset 
Management is 
a member of 
the same group 
of companies as 
CLSA 
Y 
 
CITIC Asset 
Management is 
expected to 
hold the Offer 
Shares on 
behalf of 
collective 
investment 
schemes, please 
refer to Note 
(2). 
200 
0.0023% 
0.0004% 
2.  
CITIC 
Securities 
Asset 
CITIC AM HK 
is a member of 
the same group 
N 
200 
0.0023% 
0.0004% 

<<<PAGE 19>>>
17 
 
Management 
(HK) Limited 
(“CITIC AM 
HK”) 
 
Please refer to 
Note (3). 
of companies as 
CLSA 
3.  
China Asset 
Management (Hong
Kong) Limited 
(“China AMC 
HK”) 
 
Please refer to 
Note (4). 
China AMC 
HK is a 
member of the 
same group of 
companies as 
CLSA 
N 
600 
0.0068% 
0.0011% 
 

<<<PAGE 20>>>
18 
 
 
Notes:  
 
(1) CSI 
CSI will hold the Offer Shares as a placee under the International Offering on behalf of its ultimate clients (the “CSI Ultimate Clients”), on 
a non-discretionary basis, pursuant to which: (i) CSI will act as the single counterparty of the CSI Back-to-back TRS (the “CSI Back-to-back 
TRS”) to be entered into by it in connection with a total return swap order (the “CSI Client TRS”) placed and fully funded by the CSI 
Ultimate Clients, by which CSI will pass the full economic exposure of the Offer Shares placed to CSI to the CSI Ultimate Clients; (ii) as 
confirmed by CSI and CLSA, CSI will hold the legal title and beneficial interest in the Offer Shares, but will contractually agree to pass on 
the full economic exposure and return of the Offer Shares to the CSI Ultimate Clients, on a non-discretionary basis. The CSI Ultimate Clients 
may exercise their early termination rights to terminate the CSI Client TRS at any time from the trade date of the CSI Client TRS which should 
be on or after the date on which the Offer Shares are listed on the Stock Exchange; (iii) upon the final maturity or termination of the CSI 
Client TRS by the CSI Ultimate Clients, CSI will dispose of the Offer Shares on the secondary market and the CSI Ultimate Clients will receive 
a final termination amount of the CSI Back-to-back TRS which will have taken into account all the economic returns or economic loss in 
relation to the Offer Shares and the fixed amount of transaction fees of the CSI Back-to-back TRS and the CSI Client TRS. Due to its internal 
policy, CSI will not exercise the voting right of the Offer Shares during the terms of the CSI Back-to-back TRS; and (iv) CSI is not a collective 
investment scheme which is not authorized by the SFC, nor is it expected to hold the Offer Shares on behalf of such scheme. 
 
The details of the CSI Ultimate Clients are as follows: 
 
Name of the CSI Ultimate Clients Fund Manager 
UBO(s) holding 30% or more 
interest in Fund Manager (if 
applicable) 
UBO(s) holding 30% or more interest 
in the CSI Ultimate Clients 
(if applicable) 
Evolution Darwin Shangshan No. 3 
Private Equity Investment Fund* (
进化论达尔文上善三号私募证券
投资基金) 
Hainan Evolution Asset Management 
Co., Ltd.* (海南进化论私募基金管理有
限公司) 
Wang Yiping (王一平) 
N/A 
Tongyi Taoli No. 10 Private Equity 
Investment Fund* (通怡桃李 10号
私募证券投资基金) 
Shanghai Tongyi Investment 
Management Co., Ltd.* (上海通怡投资
管理有限公司) 
Chu Yibo (储贻波) 
N/A 
Liangpai Exclusive No. 43 Private 
Equity Investment Fund* (量派专
Shanghai QuantPi Investment Limited* (
上海量派投资管理有限公司) 
Sun Lin (孙林), Yu Hang (余航) 
Sun Lin (孙林) 

<<<PAGE 21>>>
19 
 
Name of the CSI Ultimate Clients Fund Manager 
UBO(s) holding 30% or more 
interest in Fund Manager (if 
applicable) 
UBO(s) holding 30% or more interest 
in the CSI Ultimate Clients 
(if applicable) 
享四十三号私募证券投资基金) 
Hesheng Macro Strategy No. 1 
Private Equity Investment Fund* (
合晟宏观策略1号私募证券投资
基金) 
Shanghai Hesheng Asset Management 
Co., Ltd.* (上海合晟资产管理股份有限
公司) 
N/A 
N/A 
Hesheng Qijia Hybrid No. 1 
Private Equity Investment Fund* (
合晟齐嘉混合1号私募证券投资
基金) 
Shanghai Hesheng Asset Management 
Co., Ltd.* (上海合晟资产管理股份有限
公司) 
N/A 
N/A 
Panjing Wenheng Phase 2 Private 
Equity Investment Fund* (盘京闻
恒2期私募证券投资基金) 
Shanghai Panjing Investment Center 
(Limited Partnership)* (上海盘京投资
管理中心(有限合伙)) 
Zhuang Tao (庄涛) 
N/A 
 
*For identification purposes only 
 
To the best knowledge of CSI and having made all reasonable inquiries, each of the CSI Ultimate Clients and its ultimate beneficial owners 
is an independent third party of the Company, its subsidiaries, its substantial shareholders, CSI, CLSA and the companies which are members 
of the same group of companies as CLSA. 
 
(2) CITIC Asset Management 
CITIC Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of their 
investors (the “CITIC Asset Management Ultimate Clients”), each of which is, to the best knowledge of CITIC Asset Management, (i) an 
independent third party of the Company, its subsidiaries, its substantial shareholders, CITIC Asset Management, CLSA and the companies 
which are members of the same group of companies as CLSA; and (ii) a collective investment scheme which is not authorized by the SFC. No 
ultimate beneficial owner holds 30% or more interest in the funds. 
 
The details of the CITIC Asset Management Ultimate Clients are as follows: 
 

<<<PAGE 22>>>
20 
 
Name of the CITIC 
Asset Management 
Ultimate Clients 
Scheme 
Establishment Date 
Values of Assets 
under Management 
Whether the Scheme 
is Publicly Marketed 
Fund Manager 
UBO of Fund 
Manager (if 
applicable) 
Limited Partner of 
the CITIC Asset 
Management 
Ultimate Clients 
UBO holding 30% or 
more interest in the 
CITIC Asset 
Management 
Ultimate Clients (if 
applicable) 
CITIC SECURITIES 
COMPANY LIMITED-
XINHANG ZHIYUAN 
NO.1* (中信证券信航致
远1号集合资产管理计划 
) 
December 25, 2020 
RMB26,274,974.36 
Not publicly 
marketed 
CITIC Asset 
Management 
CITIC Securities 
Company Limited (中
信證券股份有限公
司, 6030.HK) 
("CITIC 
SECURITIES") 
26 limited partners 
in total, all of which 
are individuals 
N/A 
CITIC SECURITIES 
COMPANY LIMITED-
XINHANG ZHIYUAN 
NO.3* (中信证券信航致
远3号集合资产管理计划 
) 
March 4, 2021 
RMB62,521,444.68 
Not publicly 
marketed 
CITIC Asset 
Management 
CITIC SECURITIES 
48 limited partners 
in total, all of which 
are individuals 
N/A 
 
*For identification purposes only  
 
To the best of knowledge of CITIC Asset Management and after making all reasonable enquiries, (i) CITIC Asset Management Ultimate 
Clients, together with each of their ultimate beneficial owners, is an independent third party of the Company, its subsidiaries, its substantial 
shareholders, CITIC Asset Management, CLSA and the companies which are members of the same group of companies as CLSA, and (ii) 
none of CLSA and any companies which are members of the same group of companies as CLSA hold any beneficial interest in any of CITIC 
Asset Management Ultimate Clients. 
 
(3) CITIC AM HK 
CITIC AM HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the fund on behalf of its underlying 
client, namely CITIC Securities Asset Management (HK) Limited – CLSA CT Limited Sub Account 33, which is 100% invested by Sino 
Biopharmaceutical Limited (中國生物製藥有限公司, 1177.HK) (“SBP GROUP”). SBP GROUP has no ultimate beneficial owner holding 
30% or more of its interests. To the best knowledge of CITIC AM HK, SBP GROUP is an independent third party of the Company, its 
subsidiaries, its substantial shareholders, CITIC AM HK, CLSA and the companies which are members of the same group of companies as 
CLSA. 
 
The ultimate beneficial owner of CITIC AM HK is CITIC SECURITIES. 

<<<PAGE 23>>>
21 
 
 
(4) China AMC HK 
China AMC HK will hold the Offer Shares in its capacity as the discretionary fund manager managing on behalf of its underlying client (the 
“China AMC HK Underlying Client”), which is an independent third party of the Company. To the best of knowledge of China AMC HK 
and after making all reasonable enquiries, (i) the China AMC HK Underlying Client is an independent third party of the Company, its 
subsidiaries, its substantial shareholders, China AMC HK, CLSA and the companies which are members of the same group of companies as 
CLSA, and (ii) none of CLSA or any companies which are members of the same group of companies as CLSA holds any beneficial interest in 
the China AMC HK Underlying Client. 
 
The details of the China AMC HK Underlying Client are as follow: 
 
Name of the China AMC HK 
Underlying Client 
Fund Manager 
UBO of Fund Manager (if 
applicable) 
UBO holding 30% or more interest 
in the China AMC HK Underlying 
Client (if applicable) 
CHINAAMC CHINA FOCUS FUND - 
254900G5YFZ5OTQS0G14 
China AMC HK 
CITIC SECURITIES 
Manulife Financial Corp 
(MFC.TO/0945.HK) 
 
 

<<<PAGE 24>>>
22 
 
 
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
Shares may not be offered, sold, pledged or transferred within the United States, except that the Offer Shares 
may be offered, sold or delivered (a) in the United States to a limited number of institutional “accredited 
investors” (as defined in Rule 501(a) under the U.S. Securities Act) in reliance on the Rule 506 safe harbor 
under the U.S. Securities Act; or (b) outside the United States in offshore transactions in reliance on 
Regulation S. There will be no public offer of the Offer Shares in the United States. 
The Offer Shares are being offered and sold outside the United States to investors that are not U.S. persons 
nor persons acquiring for the account or benefit of U.S. persons in reliance on Regulation S under the U.S. 
Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. This announcement is not a prospectus. Potential investors should 
read the Prospectus dated May 14, 2026 issued by TenNor Therapeutics (Suzhou) Limited for detailed 
information about the Global Offering described below before deciding whether or not to invest in the H 
Shares thereby being offered. 
*Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators 
(for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence 
of any of the events set out in the section headed “Underwriting – Underwriting Arrangements and 
Expenses –Hong Kong Underwriting Agreement – Grounds for Termination” in the Prospectus at any time 
prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on May 22, 
2026). 
 
 

<<<PAGE 25>>>
23 
 
PUBLIC FLOAT AND FREE FLOAT 
Immediately following the completion of the Global Offering (after taking into account the partial exercise of 
the Offer Size Adjustment Option), the total number of the H Shares held by the public represents 
approximately 73.06% of the total issued share capital of the Company, which is higher than the prescribed 
percentage of H Shares required to be held in public hands of 25% under Rule 19A.13A(1) of the Listing 
Rules, thereby satisfying Rule 19A.13A(1) of the Listing Rules at the time of the Listing.  
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the Listing Date. As 
such, H Shares held by the Cornerstone Investors upon the Listing shall not be counted towards the free float 
of the H Shares of the Company at the time of Listing. Based on the Offer Price of HK$75.70 per H Share, 
the Company confirms the free float requirement under Rule 19A.13C(1)(a) of the Listing Rules. 
The Directors confirm that, immediately following completion of the Global Offering (after taking into 
account the partial exercise of the Offer Size Adjustment Option): (i) no placee will, individually, be placed 
more than 10% of the enlarged issued share capital of the Company immediately after the Global Offering; 
(ii) there will not be any new substantial Shareholder under the Listing Rules immediately after the Global 
Offering; (iii) the three largest public shareholders of the Company do not hold more than 50% of the H shares 
in public hands at the time of the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and 
(iv) there will be at least 300 holders of H Shares at the time of the Listing in compliance with Rule 8.08(2) 
of the Listing Rules. 
COMMENCEMENT OF DEALINGS 
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, May 22, 2026 
(Hong Kong time), provided that the Global Offering has become unconditional and the right of 
termination described in the section headed “Underwriting – Underwriting Arrangements and Expenses 
– Hong Kong Underwriting Agreement – Grounds for Termination” in the Prospectus has not been 
exercised. Investors who trade the H Shares on the basis of publicly available allocation details prior to 
the receipt of H Share certificates or prior to the H Share certificates becoming valid evidence of title 
do so entirely at their own risk. 
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Friday, May 
22, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange will 
commence at 9:00 a.m. on Friday, May 22, 2026 (Hong Kong time). The H Shares will be traded in 
board lots of 50 H Shares each, and the stock code of the H Shares will be 6872. 
By order of the Board  
TenNor Therapeutics (Suzhou) Limited 
Dr. Ma Zhenkun 
Chairman of the Board, executive Director, 
chief executive officer and general manager 
Hong Kong, May 21, 2026  
As at the date of this announcement, the Board comprises: (i) Dr. Ma Zhenkun as the executive Director; (ii) 
Dr. Song Gaoguang and Mr. Michael James Bakes as non-executive Directors; and (iii) Mr. Lee Wai Kong, 
Albert, Dr. Ni Lin and Dr. Li Leping as independent non-executive Directors. 
