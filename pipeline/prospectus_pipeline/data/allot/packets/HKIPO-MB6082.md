# 配发结果公告抽取任务：6082.HK Shanghai Biren Technology Co., Ltd.- H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**31/12/2025 22:50**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2025/1231/2025123102783.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6082.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated Monday, December 22, 2025 (the “Prospectus”) of Shanghai Biren Technology Co., 
Ltd. (上海壁仞科技股份有限公司) (the “Company”).
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
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited, as 
the stabilizing manager (the “Stabilizing Manager”) (or any person acting for it), on behalf of the Underwriters, 
may over-allocate or effect transactions with a view to stabilizing or supporting the market price of the Shares at a 
level higher than that which might otherwise prevail for a limited period after the Listing Date. However, there is 
no obligation on the Stabilizing Manager (or any person acting for it) to conduct any such stabilizing action. Such 
stabilizing action, if taken, (a) will be conducted at the absolute discretion of the Stabilizing Manager (or any person 
acting for it) and in what the Stabilizing Manager (or any person acting for it) reasonably regards as the best interest 
of our Company, (b) may be discontinued at any time, and (c) is required to be brought to an end within 30 days after 
the last day for lodging applications under the Hong Kong Public Offering (which is Wednesday, 28 January 2026). 
Such stabilization action, if taken, may be effected in all jurisdictions where it is permissible to do so, in each case 
in compliance with all applicable laws, rules and regulatory requirements, including the Securities and Futures (Price 
Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures 
Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the Shares for longer 
than the stabilization period which begins on the Listing Date, and is expected to expire on Wednesday, 28 January 
2026, the 30th day after the last day for the lodging of applications under the Hong Kong Public Offering. After this 
date, when no further stabilizing action may be taken, demand for the Shares, and therefore the price of the Shares, 
could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out in 
the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not 
resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-
Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the 
events set out in the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public 
Offering – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing 
Date (which is currently expected to be on Friday, January 2, 2026).

<<<PAGE 2>>>
2
Shanghai Biren Technology Co., Ltd.
上海壁仞科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
284,846,600 H Shares (taking into account 
the full exercise of the Offer Size 
Adjustment Option and subject to the 
Over-allotment Option)
Number of Hong Kong Offer Shares
:
49,538,600 H Shares (as adjusted after 
reallocation)
Number of International Offer Shares
:
235,308,000 H Shares (taking into account 
the full exercise of the Offer Size 
Adjustment Option, as adjusted after 
reallocation and subject to the Over-
allotment Option)
Final Offer Price
:
HK$19.60 per H Share, plus brokerage of  
1.0%, SFC transaction levy of 0.0027%,  
AFRC transaction levy of 0.00015% and  
Stock Exchange trading fee of 0.00565%  
(payable in full on application  
in Hong Kong dollars, subject to refund)
Nominal value
:
RMB0.02 per H Share
Stock code
:
6082
Joint Sponsors, Sponsor-OCs, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers
Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunner and Joint Lead Manager

<<<PAGE 3>>>
1 
 
SHANGHAI BIREN TECHNOLOGY CO., LTD. / 上海壁仞科技股份有限公司 
ANNOUNCEMENT 
OF 
FINAL 
OFFER 
PRICE 
AND  
ALLOTMENT RESULTS 
 
Warning:  In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could move 
substantially even with a small number of H Shares traded and should exercise extreme caution when 
dealing in the Shares. 
SUMMARY  
 
Company information 
Stock code  
6082 
Stock short name  
BIREN TECH 
Dealings commencement date  
January 2, 2026* 
*see note at the end of the announcement  
 
Price Information  
Final Offer Price  
HK$19.60 
Maximum Offer Price 
HK$19.60 
 
Offer Shares and Share Capital 
Number of Offer Shares (before exercise of the Over-
allotment Option) 
284,846,600 
Final Number of Offer Shares in Public Offer (after 
reallocation) 
49,538,600 
Final Number of Offer Shares in International Offer (after 
reallocation and the full exercise of the Offer Size 
Adjustment Option) * 
235,308,000  
Number of issued shares upon Listing (before exercise of the 
Over-allotment Option)  
2,396,131,700 
* The number of Offer Shares above is determined after taking into account the additional Offer Shares 
issued under the following Offer Size Adjustment Option. 
 
Offer Size Adjustment Option (Upsize option) 
Number of additional shares issued under the option 
37,153,800 
- 
Public Offer 
0 
- 
International Offer 
37,153,800 
The Offer Size Adjustment Option has been exercised in full, pursuant to which the Company is issuing 
and allotting 37,153,800 additional Offer Shares, representing approximately 15.0% of the total number 
of Offer Shares initially available under the Global Offering, at the final Offer Price. 
 
Over-allocation 
No. of Offer Shares over-allocated  
42,726,800 
- 
International Offer 
42,726,800 
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases 
in the secondary market at prices that do not exceed the Offer Price or through deferred delivery or a 
combination of these means. In the event the Over-allotment Option is exercised, an announcement will 
be made on the Stock Exchange’s website.  
 

<<<PAGE 4>>>
2 
 
Proceeds   
Gross proceeds (Note)  
HK$5,583.0 million 
Less: Estimated listing expenses payable based on Final 
Offer Price  
HK$(208.5) million 
Net proceeds  
HK$5,374.5 million 
 
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use 
of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Offer Size Adjustment Option 
and the exercise of the Over-allotment Option (if any) for the purposes as set out in the section headed 
“Future Plans and Use of Proceeds” of the Prospectus on a pro rata basis. 
 
 
ALLOTMENT RESULTS DETAILS 
PUBLIC OFFER  
 
No. of valid applications  
471,116 
No. of successful applications  
135,569 
Subscription level  
2,347.53 times 
Claw-back triggered  
Yes  
No. of Offer Shares initially available under the Public Offer  
12,384,800 
No. of Offer Shares reallocated from the International Offer (claw-
back) 
37,153,800 
Final no. of Offer Shares under the Public Offer (after reallocation) 49,538,600 
% of Offer Shares under the Public Offer to the Global Offering 
17.39 
 
Note: For details of the final allocation of Shares to the Public Offer, investors can refer to 
www.hkeipo.hk/iporesult to perform a search by identification number or www.hkeipo.hk/iporesult for the full 
list of allottees. 
INTERNATIONAL OFFER 
 
No. of placees  
359 
Subscription Level (before taking into account the Offer Size 
Adjustment Option) 
25.95 times  
No. of Offer Shares initially available under the International Offer  235,308,000 
No. of Offer Shares reallocated to the Public Offer (claw-back) 
37,153,800 
Final no. of Offer Shares under the International Offer (after 
reallocation and the full exercise of the Offer Size Adjustment 
Option) 
235,308,000 
% of Offer Shares under the International Offer to the Global 
Offering 
82.61% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for a waiver under Rule 
10.04 of the Listing Rules and consent under paragraph 1C(2) of Appendix F1 to the Listing Rules (the 
“Placing Guidelines”) granted by the Stock Exchange to permit the Company to allocate certain Offer Shares 
in the International Offering to certain existing minority shareholders and/or their close associates as 
cornerstone investors or placees, (i) none of the Offer Shares subscribed by the placees and the public have 

<<<PAGE 5>>>
3 
 
been financed directly or indirectly by the Company, any of the Directors, chief executive of the Company, 
Single Largest Group of Shareholders, substantial Shareholders, existing Shareholders of the Company or any 
of its subsidiaries or their respective close associates; and (ii) none of the placees and the public who have 
purchased the Offer Shares are accustomed to taking instructions from the Company, any of the Directors, 
chief executive of the Company, Single Largest Group of Shareholders, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates in relation to the 
acquisition, disposal, voting or other disposition of Shares registered in his/her/its name or otherwise held by 
him/her/it.  
The placees in the International Offer include the following: 
Cornerstone Investors 
 
Investor 
No. of Offer 
Shares 
allocated 
% of Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
share capital after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) 
Existing 
shareholders or 
their close 
associates 
3W Fund Management 
Limited (“3W Fund”) 
31,769,600 
11.15% 
1.33%  
Yes 
Qiming Venture Partners 
13,899,200  
4.88% 
0.58% 
 
- QM125 Limited 
7,942,400 
2.79% 
0.33% 
Yes 
- QM120 Limited 
5,956,800 
2.09% 
0.25% 
Yes 
Aspex Master Fund 
(“AMF”) 
11,913,600  
4.18% 
0.50% 
No 
WT Asset Management 
Limited (“WT Asset 
Management”) 
11,913,600  
4.18% 
0.50% 
No 
Hao Great China Focus 
Fund  
7,942,400  
2.79% 
0.33% 
No 
Ping An Life Insurance 
Company of China, Ltd. 
(“Ping An Life 
Insurance”) 
5,956,800 
2.09% 
0.25% 
Yes 
Huadeng Technology 
Peak Fortitude Ventures 
Ltd (“Huadeng 
Technology”) 
5,956,800 
2.09% 
0.25% 
No 
Lion Global Investors 
Limited (“Lion Global”) 
5,956,800 
2.09% 
0.25% 
No 
Shanghai Greenwoods 
and CICC Financial 
Trading Limited (“CICC 
FT”) (in connection with 
Greenwoods OTC 
Swaps) 
5,956,800 
2.09% 
0.25% 
No 
MY Asian Opportunities 
Master Fund, L.P. (“MY 
Asian”) 
4,765,400 
1.67% 
0.20% 
No 

<<<PAGE 6>>>
4 
 
 
Investor 
No. of Offer 
Shares 
allocated 
% of Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
share capital after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) 
Existing 
shareholders or 
their close 
associates 
Eastspring Investments 
(Singapore) Limited 
 (“Eastspring”) 
3,971,200 
1.39% 
0.17% 
No 
UBS Asset Management 
(Singapore) Ltd. (“UBS 
AM Singapore”) 
3,971,200 
1.39% 
0.17% 
No 
Taikang Life Insurance 
Co., Ltd (“Taikang 
Life”) 
3,971,200 
1.39% 
0.17% 
No 
Aspirational China 
Growth GP Limited 
(“Aspirational China 
Growth”) 
3,971,200 
1.39% 
0.17% 
Yes 
Charoen Pokphand 
Robot Limited 
(“Charoen Pokphand”) 
3,971,200 
1.39% 
0.17% 
No 
Digital China (HK) 
Limited (神州數碼(香
港)有限公司) (“Digital 
China”) 
3,971,200 
1.39% 
0.17% 
No 
Jinxiu 608 and GTJA HK 
(in connection with the 
GTJA Back-to-back TRS 
and Zhonghe 
OTC Swaps) 
3,176,800 
1.12% 
0.13% 
Yes 
China Southern Asset 
Management Co., Ltd. 
(南方基金管理有限公
司) (“China Southern”) 
3,176,800 
1.12% 
0.13% 
No 
Fullgoal Fund 
3,176,600 
1.12% 
0.13% 
 
Fullgoal Fund 
Management Co., 
Ltd. (富國基金管理
有限公司) 
(“Fullgoal Fund”) 
1,906,000 
0.67% 
0.08% 
No 
Fullgoal Asset 
Management (HK) 
Limited (“Fullgoal 
HK”) 
1,270,600 
0.45% 
0.05% 
No 
Yeebo Alpha Limited 
(“Yeebo”) 
2,581,200 
0.91% 
0.11% 
No 
Enhanced Investment 
Products Limited 
(“EIP”) 
1,985,600 
0.70% 
0.08% 
No 

<<<PAGE 7>>>
5 
 
 
Investor 
No. of Offer 
Shares 
allocated 
% of Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
share capital after 
the Global Offering 
(assuming the Over-
allotment Option is 
not exercised) 
Existing 
shareholders or 
their close 
associates 
Tessy Holding Limited 
1,985,600 
0.70% 
0.08% 
No 
New Opportunities SPC 
1,985,600 
0.70% 
0.08% 
Yes 
Total 
147,926,400 
51.93% 
6.17% 
 
 
 

<<<PAGE 8>>>
6 
 
 
Allotees with Waivers/Consents Obtained 
 
 
Investor 
No. 
of 
Offer 
Shares allocated 
% 
of 
Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) 
% 
of 
total 
issued 
share 
capital after the 
Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) 
Relationship 
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by existing 
minority shareholders and/or its close associates as cornerstone investors and placees Note 1 
Cornerstone Investors  
3W Fund 
31,769,600 
11.15% 
1.33% 
A 
cornerstone 
investor and a close 
associate 
of 
an 
existing 
minority 
shareholder 
QM120 
Limited 
and 
QM125 Limited 
13,899,200 
4.88% 
0.58% 
QM120 Limited is an 
existing 
minority 
shareholder. 
QM125 Limited is a 
close associate of 
QM120. 
Ping An Life Insurance 
5,956,800 
2.09% 
0.25% 
A 
cornerstone 
investor and a close 
associate 
of 
an 
existing 
minority 
shareholder 
Aspirational 
China 
Growth  
3,971,200 
1.39% 
0.17% 
A 
cornerstone 
investor 
and 
an 
existing 
minority 
shareholder 
New Opportunities SPC 
1,985,600 
0.70% 
0.08% 
A 
cornerstone 
investor and a close 
associate 
of 
an 
existing 
minority 
shareholder  
Guotai Junan Investments 
(Hong 
Kong) 
Limited 
(“GTJA 
Investments”) 
(in connection with the 
GTJA Back-to-back TRS 
and Zhonghe OTC Swaps) 3,176,800 
1.12% 
0.13% 
A 
cornerstone 
investor and a close 
associate of existing 
minority 
shareholders 

<<<PAGE 9>>>
7 
 
 
Investor 
No. 
of 
Offer 
Shares allocated 
% 
of 
Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) 
% 
of 
total 
issued 
share 
capital after the 
Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) 
Relationship 
Also 
a connected 
client 
Placees  
Black Dragon AP SPV1 
1,238,800 
0.43% 
0.05% 
A placee and an 
existing 
minority 
shareholder 
Sino 
Lion 
Ventures 
Limited (“Sino Lion”) 
198,400 
0.07% 
0.01% 
A placee and a close 
associate 
of 
an 
existing 
minority 
shareholder  
Haitong 
International 
Asset Management (HK) 
Limited (“Haitong AM”) 
19,800 
0.01% 
0.00% 
A placee and a close 
associate of existing 
minority 
shareholders 
Also 
a connected 
client 
Guotai Junan Investments 
(in connection with the 
GTHT 
Client 
TRS) 
(“GTJA Investments”) 
576,400 
0.20% 
0.02% 
A placee and a close 
associate of existing 
minority 
shareholders 
Also 
a connected 
client 
Xinyuan 
Tianxun 
Navigator 
Private 
Securities 
Investment 
Fund (芯源天循领航私
募证券投资基金) 
(“Xinyuan Tianxun”) (in 
connection 
with 
the 
Huatai Client TRS) 
99,200 
0.03% 
0.00% 
A placee and a close 
associate 
of 
an 
existing 
minority 
shareholder 
HTI Financial Solutions 
Limited (in connection 
with 
the 
HTI 
TRS) 
(“HTIFSL”) 
4,175,600 
1.47% 
0.18% 
A placee and a close 
associate 
of 
two 
existing 
minority 
shareholders 
Also 
a connected 
client 

<<<PAGE 10>>>
8 
 
 
Investor 
No. 
of 
Offer 
Shares allocated 
% 
of 
Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) 
% 
of 
total 
issued 
share 
capital after the 
Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) 
Relationship 
Dream'ee JuneBeast Fund 39,600 
0.01% 
0.00% 
A placee and a close 
associate 
of 
an 
existing 
minority 
shareholder  
Benchi Holding Limited 
39,600 
0.01% 
0.00% 
A placee and a close 
associate 
of 
an 
existing 
minority 
shareholder  
ZhuoLing 
International 
Limited 
397,000 
0.14% 
0.02% 
A placee and a close 
associate 
of 
an 
existing 
minority 
shareholder  
Li Wei (厲偉) 
198,400 
0.07% 
0.01% 
A placee and a close 
associate 
of 
an 
existing 
minority 
shareholder  
Shanghai Fame Limited 
252,000 
0.09% 
0.01% 
A placee and a close 
associate 
of 
an 
existing 
minority 
shareholder  
Autumn Thrive Limited 
3,971,200 
1.39% 
0.17% 
A placee and a close 
associate 
of 
an 
existing 
minority 
shareholder  
Shanghai 
Hua 
Hong 
International, Inc. 
2,959,000 
1.04% 
0.13% 
A placee and a close 
associate 
of 
an 
existing 
minority 
shareholder  
Lingang Wings Inc 
595,600 
0.21% 
0.03% 
A placee and a close 
associate 
of 
an 
existing 
minority 
shareholder 
Aquila Composite Fund 
SPC Ltd. - Aquila High 
Frequency Strategy SP 
39,600 
0.01% 
0.00% 
A placee and a close 
associate 
of 
an 
existing 
minority 
shareholder  
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations to connected clients Note 2 

<<<PAGE 11>>>
9 
 
 
Investor 
No. 
of 
Offer 
Shares allocated 
% 
of 
Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) 
% 
of 
total 
issued 
share 
capital after the 
Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) 
Relationship 
Ping An Life Insurance 
5,956,800 
2.09% 
0.25% 
Cornerstone investor 
and connected client 
CICC FT (in connection 
with Greenwoods OTC 
Swaps and the CICCFT 
OTC Swaps) 
5,956,800 
2.09% 
0.25% 
Cornerstone investor 
and connected client 
(in connection with 
Greenwoods OTC 
Swaps) 
587,200 
0.21% 
0.02% 
Connected client (in 
connection with the 
CICCFT OTC 
Swaps) 
CITIC 
Securities 
International 
Capital 
Management 
Limited 
(“CSI”)  
443,000 
0.16% 
0.02% 
Connected client 
GTJA 
Investments 
(in 
connection 
with 
the 
Zhonghe OTC Swaps and 
the GTJAI Subscription) 
3,176,800 
1.12% 
0.13% 
Cornerstone investor 
and connected client 
(in connection with 
Zhonghe OTC 
Swaps) 
576,400 
0.20% 
0.02% 
Connected client (in 
connection with the 
GTJAI Subscription) 
HTIFSL 
4,175,600 
1.47% 
0.18% 
Connected client 
Huatai Capital Investment 
Limited (“HTCI”) 
460,600 
0.16% 
0.02% 
Connected client 
CITIC Securities Asset 
Management 
Company 
Limited (“CITICS AM”) 
7,942,400  
2.79% 
0.34% 
Connected client 
China Asset Management 
(Hong 
Kong) 
Limited 
(“China AMC HK”) 
317,600 
0.11% 
0.01%   
Connected client 
China Universal Asset 
Management 
(Hong 
Kong) Company Limited 
(“China 
Universal 
(HK)”)  
317,600 
0.11% 
0.01% 
Connected client 

<<<PAGE 12>>>
10 
 
 
Investor 
No. 
of 
Offer 
Shares allocated 
% 
of 
Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) 
% 
of 
total 
issued 
share 
capital after the 
Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) 
Relationship 
Orient Asset Management 
(Hong 
Kong) 
Limited 
(“Orient AM”)  
8,000 
0.00% 
0.00% 
Connected client 
Guosen Securities (HK) 
Asset 
Management 
Company 
Limited 
(“Guosen HK AM”) 
79,400 
0.03% 
0.00% 
Connected client 
ICBC 
UBS 
Asset 
Management Co., Ltd. 
(“ICBC UBS”)  
37,000 
0.01% 
0.00% 
Connected client 
ICBC 
UBS 
Asset 
Management 
(International) Company 
Limited 
(“ICBC 
UBS 
(International)”) 
2,600 
0.00% 
0.00% 
Connected client 
UBS Asset Management 
(Singapore) Ltd. (“UBS 
AM Singapore”) 
3,971,200 
1.39% 
0.17% 
Cornerstone investor 
and connected client  
Haitong 
International 
Asset Management (HK) 
Limited (“Haitong AM”) 
19,800 
0.01% 
0.00% 
Connected client 
Haitong 
International 
Investment 
Managers 
Limited (“Haitong IIM”) 9,900 
0.00% 
0.00% 
Connected client 
Fullgoal Fund 
3,176,600 
1.12% 
0.13% 
Cornerstone investor 
and connected client 
China Southern 
3,176,600 
1.12% 
0.13% 
Cornerstone investor 
and connected client 
Notes: 
 
1. See “Waivers – Waiver Under Rule 10.04 and Consent under Paragraph 1C(2) of Appendix F1 to the 
Listing Rules in respect of Subscriptions of Offer Shares by Existing Shareholders and/or its Close 
Associates as Cornerstone Investors” of the Prospectus and the section headed “Others / Additional 
Information – Placing to existing shareholders and/or its close associates with a prior waiver under 
Rule 10.04 and consent under paragraph 1C(1) of the Placing Guidelines” in this announcement for 
further details. 
 
2. Saved as listed out, the H Shares placed to such allottees are held on behalf of independent third 

<<<PAGE 13>>>
11 
 
 
Investor 
No. 
of 
Offer 
Shares allocated 
% 
of 
Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) 
% 
of 
total 
issued 
share 
capital after the 
Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) 
Relationship 
parties (as defined in Chapter 4.15 of the Guide for New Listing Applicants and are in compliance 
with all the conditions under the consent granted by the Stock Exchange. For details of the consent 
under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations to connected clients, please refer to the section headed “Others 
/ Additional Information – Placing to connected clients with a prior consent under paragraph 1C(1) 
of the Placing Guidelines” in this announcement. 
 
 
LOCK-UP UNDERTAKINGS  
Key Persons (as defined under Rule 18C.14 of the Listing Rules) 
Name 
Capacity 
Total number 
of Shares 
held in the 
Company 
subject to 
lock–up 
undertakings 
upon Listing 
Number of 
H Shares 
held in the 
Company 
subject to 
lock–up 
undertakin
gs upon 
Listing 
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock–up 
undertaking
s upon 
Listing Note 1 
% of 
shareholdin
g in the 
Company 
subject to 
lock–up 
undertaking
s upon 
Listing 
Note 1 
Last day 
subject to 
the lock–
up 
undertakin
gs Note 2 
Wen ZHANG 
(“Mr. 
Zhang”) 
Founder of 
the Group, an 
executive 
Director and 
Chief 
Executive 
Officer 
183,174,800 
– 
– 
7.64% 
January 1, 
2027  
Shanghai 
Biliren 
Enterprise 
Management 
Consulting 
Partnership 
(Limited 
Partnership)* 
(上海壁立仞
企業管理諮
詢合夥企業
(有限合夥)) 
(“Shanghai 
Biliren”) Note 3 
Close 
associate of 
Mr. Zhang 
191,221,400 
– 
– 
7.98% 
January 1, 
2027  

<<<PAGE 14>>>
12 
 
 
Pathfinder SIIs 
 
Subtotal 
- 
374,396,200 
- 
- 
15.63% 
 
Notes: 
1. Assuming the Over–allotment Option is not exercised. 
2. The lock-up period commencing on the date by reference to which disclosure of its shareholding 
is made in the Prospectus and ending on the date which is 12 months from the Listing Date, i.e. 
January 1, 2027. 
3. Shanghai Biliren is the employee incentive platform of the Group. The Group had granted Share 
Options to selected participants under the Pre–IPO Employee Incentive Scheme for indirect 
limited partnership interests in 31 limited partners of Shanghai Biliren. Four of our Directors 
(including Mr. Zhou HONG, our Chief Technology Officer, and Mr. Linglan ZHANG, our Chief 
Operating Officer, who are also key management and core members of our R&D team) were 
limited partners of four of the limited partners of Shanghai Biliren, including (i) Limited 
Partnership 1 (a limited partner of Shanghai Biliren holding 46.54% of its partnership interests), 
whereby Mr. Zhou HONG, Mr. Linglan ZHANG and Mr. Luting PAN held 35.32%, 22.91% and 
1.28% of the partnership interests of Limited Partnership 1; (ii) Limited Partnership 2 (a limited 
partner of Shanghai Biliren holding approximately 9.08% of its partnership interests), whereby 
Mr. Xiao held 2.53% of the partnership interests of Limited Partnership 2; (iii) Limited 
Partnership 3 (a limited partner of Shanghai Biliren holding 1.95% of its partnership interests), 
whereby Mr. Xiao held 66.89% of the partnership interests of Limited Partnership 3; and (iv) 
Limited Partnership 31 (a limited partner of Shanghai Biliren holding 2.83% of its partnership 
interests), whereby Mr. Luting PAN held 17.23% of the partnership interests of Limited 
Partnership 31. Such partnership interests held by our four executive Directors in the limited 
partners of Shanghai Biliren will be subject to lock–up period ending on the expiry of 12 months 
from the Listing Date. Save as disclosed above, there is no other senior management or key 
management and core members of our R&D team who holds any interest in our Company. 
Name 
Number of 
Shares held in 
the Company 
subject to lock–
up undertakings 
upon Listing 
Number of H 
Shares held 
in the 
Company 
subject to 
lock–up 
undertakings 
upon Listing 
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock–up 
undertakings 
upon Listing Note 
1 
% of 
shareholding in 
the Company 
subject to lock–
up undertakings 
upon Listing 
Note 1 
Last day 
subject to the 
lock–up 
undertakings 
Note 2 
QM120 
Limited 
91,773,400 
45,886,700 
3.96% 
3.83% 
January 1, 
2027  
Country 
Garden Venture 
Capital  Note 3   
66,597,200 
– 
– 
2.78% 
January 1, 
2027  
Sky9 Capital 
Note 4 
55,270,450 
27,635,250 
2.39% 
2.31% 
January 1, 
2027  
Zhuhai Gree 
Venture Capital 
Investment Co., 
Ltd. (珠海格力
創業投資有限
公司) 
(“Zhuhai 
Gree”) 
45,904,650 
22,952,300 
1.98% 
1.92% 
January 1, 
2027  

<<<PAGE 15>>>
13 
 
 
Existing shareholders 
 
Shenzhen 
Songhe Growth 
Equity 
Investment 
Partnership 
(Limited 
Partnership) 
(深圳市松禾成
長股權投資合
夥企業(有限合
夥)) 
(“Shenzhen 
Songhe”) 
39,967,350 
39,967,350 
3.45% 
1.67% 
January 1, 
2027  
Subtotal 
299,513,050 
136,441,600 
11.78% 
12.50% 
 
Notes: 
 
1. Each of the Shareholders listed in the above table is a pathfinder SII of the Company as defined 
under Chapter 2.5 of the Guide for New Listing Applicants. Please refer to the section headed 
“History, Development and Corporate Structure – Capitalization of our Company” in the 
Prospectus for further details. 
2. In accordance with Rule 18C.14(2) of the Listing Rules, the required lock–up period commences 
on the date by reference to which disclosure of its shareholding is made in the Prospectus and 
ends on the date which is six months from the Listing Date, i.e. July 2, 2026. In addition to the 
lock-up requirement under Rule 18C.14(2) of the Listing Rules, all existing Shareholders shall 
not dispose of any of the Shares held by them within the 12 months following the Listing Date, i.e. 
January 2, 2027, as required under the applicable PRC laws. 
3. Includes 33,298,600 Shares held by Foshan Nanhai District Huibi No. 2 Equity Investment 
Partnership (Limited Partnership) (佛山市南海區匯碧二號股權投資合夥企業(有限合夥)) 
and 33,298,600 Shares held by Shenzhen Country Garden Innovation Investment Co., Ltd. (深圳
市碧桂園創新投資有限公司). 
4. Includes 29,194,700 Shares held by Sky9 Alpha Limited, 20,400,500 Shares held by Sky9 Capital 
MVP Fund II, L.P. and 5,675,250 Shares held by Shanghai Yunjiu No. 1 Venture Capital 
Investment Partnership (Limited Partnership) (上海雲玖一號創業投資合夥企業(有限合夥)) . 
Name Note 1 
Total number of 
Shares held in the 
Company subject to 
lock–up undertakings 
upon Listing 
Number of H 
Shares held in 
the Company 
subject to 
lock–up 
undertakings 
upon Listing 
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock–up 
undertakings 
upon Listing 
Note 2 
% of  
shareholding 
in the 
Company 
subject to 
lock–up 
undertakings 
upon listing 
Note 2 
Last day 
subject to the 
lock–up 
undertakings  
Note 3 
Shanghai 
Shanghe 
87,036,150 
43,131,824 
3.72% 
3.63% 
January 1, 
2027  

<<<PAGE 16>>>
14 
 
Guangzhou 
Industry 
Investment 
19,068,800 
9,534,400 
0.82% 
0.80% 
January 1, 
2027  
Knowledge 
City 
19,068,800 
9,534,400 
0.82% 
0.80% 
January 1, 
2027  
Zhuhai Da 
Heng Qin 
80,717,950 
– 
– 
3.37% 
January 1, 
2027 
Yuanqi Liqian 
60,446,300 
30,223,150 
2.61% 
2.52% 
January 1, 
2027  
Beijing Yurun 
9,401,100 
4,700,550 
0.41% 
0.39% 
January 1, 
2027  
Mr. Liang 
65,234,050 
– 
– 
2.72% 
January 1, 
2027 
Qingdao 
Huaxin Anchor 
62,299,150 
31,149,600 
2.69% 
2.60% 
January 1, 
2027  
Clear Affluent 
59,570,100 
42,283,800 
3.65% 
2.49% 
January 1, 
2027  
Linke Bixin 
56,752,400 
28,376,200 
2.45% 
2.37% 
January 1, 
2027  
Minsheng 
Tonghui 
50,472,950 
– 
– 
2.11% 
January 1, 
2027 
Gongqingcheng 
Yunren 
11,917,950 
848,650 
0.07% 
0.50% 
January 1, 
2027  
Ningbo 
Meishan 
Xingyinfeng 
8,076,500 
1,211,500 
0.10% 
0.34% 
January 1, 
2027  
Gongqingcheng 
Yunzhang 
5,958,950 
2,979,500 
0.26% 
0.25% 
January 1, 
2027  
Gongqingcheng 
Fengjue 
5,671,650 
1,985,100 
0.17% 
0.24% 
January 1, 
2027  
SME Huaying 
Fund 
29,219,700 
14,609,850 
1.26% 
1.22% 
January 1, 
2027  
Jiuyi Zhixin 
11,717,100 
11,031,350 
0.95% 
0.49% 
January 1, 
2027  
Hangzhou 
Unicorn 
25,114,150 
– 
– 
1.05% 
January 1, 
2027 
Turing Anqian 
11,350,500 
 
5,675,250 
0.49% 
0.47% 
January 1, 
2027  
Turing 
Anchang 
10,094,600 
– 
– 
0.42% 
January 1, 
2027  
Turing Anchi 
2,791,750 
– 
– 
0.12% 
January 1, 
2027  
Zhongtong 
Ruide 
22,952,300 
– 
– 
0.96% 
January 1, 
2027  
Jiaxing Yufeng 
12,153,600 
– 
– 
0.51% 
January 1, 
2027  
Jiaxing Yuzhen 9,651,750 
– 
– 
0.40% 
January 1, 
2027  
Gongqingcheng 
Shenghe 
16,295,200 
– 
– 
0.68% 
January 1, 
2027 

<<<PAGE 17>>>
15 
 
Suzhou Glory 
11,476,150 
5,738,100 
0.50% 
0.48% 
January 1, 
2027  
Shanghai Qi’an 
Jingjin Private 
Equity 
Fund 
Partnership 
(Limited 
Partnership) 
(上海奇安競進
私募基金合夥
企業(有限合
夥)) 
10,094,600 
– 
– 
0.42% 
January 1, 
2027  
Changsha 
Qi’an Qilin 
Venture 
Investment 
Fund 
Partnership 
(Limited 
Partnership) 
(長沙奇安麒麟
創業投資基金
合夥企業(有限
合夥)) 
1,009,450 
– 
– 
0.04% 
January 1, 
2027  
Hainan Nanbai 
Suan 
Technology 
Co., Ltd. (海南
南佰算科技有
限公司) 
10,094,600 
– 
– 
0.42% 
January 1, 
2027  
Xiaobin LIU 
(劉曉斌) 
10,094,600 
– 
– 
0.42% 
January 1, 
2027  
Qingdao Shuda 
Equity 
Investment 
Fund 
Partnership 
(Limited 
Partnership) 
(青島樹達股權
投資基金合夥
企業(有限合
夥)) 
 
9,400,000 
 
 
2,350,000 
0.20% 
0.39% 
January 1, 
2027  
Xiamen Tanren 8,394,600 
– 
– 
0.35% 
January 1, 
2027  
Puhua SME 
Phase II 
(Hangzhou) 
8,075,650 
– 
– 
0.34% 
January 1, 
2027  

<<<PAGE 18>>>
16 
 
Venture 
Investment 
Partnership 
(Limited 
Partnership) 
(普華中小二期 
(杭州)創業投
資合夥企業(有
限合夥)) 
Yancheng 
Huayao 
Zhisuan Phase 
II Venture 
Investment 
Partnership 
(Limited 
Partnership) 
(鹽城華耀智算
二期創業投資
合夥企業(有限
合夥)) 
2,220,800 
– 
– 
0.09% 
January 1, 
2027  
Jupiter Global 
Master Fund 
Ltd. 
7,611,800 
– 
– 
0.32% 
January 1, 
2027  
Aspirational 
China Growth 
GP Limited 
7,220,250 
– 
– 
0.30% 
January 1, 
2027  
Shenzhen 
Times 
Xinchuang No. 
16 Investment 
Partnership 
(Limited 
Partnership) 
(深圳時代信創
十六號投資合
夥企業(有限合
夥)) 
6,860,000 
– 
– 
0.29% 
January 1, 
2027  
Shenzhen 
Ganshen 
Wenhe Equity 
Investment 
Fund 
Partnership 
(Limited 
Partnership) 
(深圳市贛深文
合股權投資基
6,810,300 
– 
– 
0.28% 
January 1, 
2027  

<<<PAGE 19>>>
17 
 
金合夥企業 
(有限合 夥)) 
Yancheng 
Zhiping 
6,481,950 
– 
– 
0.27% 
January 1, 
2027  
Kun LAN (蘭
坤) 
6,056,750 
– 
– 
0.25% 
January 1, 
2027  
Quanzhou 
Wolun 
Hongshen 
Venture 
Capital 
Investment 
Partnership 
(Limited 
Partnership) 
(泉州沃侖紅燊
創業投資合夥
企業(有限合
夥)) 
5,675,250 
– 
– 
0.24% 
January 1, 
2027  
Jiantou 
Investment Co., 
Ltd. (建投投資
有限責任公司) 
 
5,675,250 
– 
– 
0.24% 
January 1, 
2027  
Jiangsu Jianyin 
Investment Co., 
Ltd. (江蘇建銀
投資有限公司) 5,197,850 
– 
– 
0.22% 
January 1, 
2027  
Li Song 
Foundation 
Company 
Limited (李‧宋
基金會有限公
司) 
5,047,300 
– 
– 
0.21% 
January 1, 
2027  
Shaanxi Jinzi 
Jinji Equity 
Investment 
Partnership 
(Limited 
Partnership) 
(陝西金資金濟
股權投資合夥
企業(有限合
夥)) 
 
5,047,300 
– 
– 
0.21% 
January 1, 
2027  
Shenzhen 
Jinshi 
Tiancheng 
Technology 
 
5,047,300 
– 
– 
0.21% 
January 1, 
2027  

<<<PAGE 20>>>
18 
 
Investment Co., 
Ltd. 
(深圳金石天成
科技投資有限
公司) 
YOUSU 
GmbH 
 
2,523,650 
– 
– 
0.11% 
January 1, 
2027  
Yousu Hong 
Kong Limited 
(游素香港有限
公司) 
2,523,650 
– 
– 
0.11% 
January 1, 
2027  
Huaxu 
(Guangzhou) 
Industrial 
Investment 
Fund 
Management 
Partnership 
(Limited 
Partnership) 
(華胥(廣州)產
業投資基金管
理合夥企業(有
限合夥)) 
3,028,400 
– 
– 
0.13% 
January 1, 
2027  
Chongqing 
Huaxu Private 
Equity 
Investment 
Fund 
Partnership 
(Limited 
Partnership) 
(重慶華胥私募
股權投資基金
合夥企業(有限
合夥)) 
2,018,900 
– 
– 
0.08% 
January 1, 
2027  
Gongqingcheng 
Fangwei Equity 
Investment 
Partnership 
(Limited 
Partnership) 
(共青城方維股
權投資合 夥企
業(有限合夥)) 
4,540,200 
 
908,050 
0.08% 
0.19% 
January 1, 
2027  
Gongqingcheng 
Chongtai Zhihe 
Venture 
Investment 
4,414,100 
– 
– 
0.18% 
January 1, 
2027  

<<<PAGE 21>>>
19 
 
Partnership 
(Limited 
Partnership) 
(共青城崇泰智
核創業投資合
夥企業(有限合
夥)) 
Julong Jingrun 
4,093,450 
– 
– 
0.17% 
January 1, 
2027  
Zhenchun 
FANG (方振
淳) 
4,037,850 
– 
– 
0.17% 
January 1, 
2027  
Wuhan Huashi 
Huitian Private 
Equity 
Investment 
Fund 
Partnership 
(Limited 
Partnership) 
(武漢華實匯添
私募股權投資
基金合夥企業
(有限合夥)) 
3,405,150 
– 
– 
0.14% 
January 1, 
2027  
Suzhou 
Xiangzhong 
Venture 
Investment 
Partnership 
(Limited 
Partnership) 
(蘇州祥仲創業
投資合夥企業
(有限合夥)) 
2,422,700 
– 
– 
0.10% 
January 1, 
2027  
Nanjing 
Xiangzhong 
Venture 
Investment 
Partnership 
(Limited 
Partnership) 
(南京祥仲創業
投資合夥企業
(有限合夥)) 
605,700 
– 
– 
0.03% 
January 1, 
2027  
Suzhou Weixin 
Taike Venture 
Investment 
Partnership 
(Limited 
2,018,900 
– 
– 
0.08% 
January 1, 
2027  

<<<PAGE 22>>>
20 
 
Partnership) 
(蘇州維新鈦氪
創業投資合夥
企業(有限合
夥)) 
Gongqingcheng 
Yintai Jiayi 
Investment 
Partnership 
(Limited 
Partnership) 
(共青城銀泰嘉
益投資合夥企
業(有限合夥)) 
3,028,400 
– 
– 
0.13% 
January 1, 
2027  
Fuzhou 
Innovation & 
Tech Venture 
Investment 
Partnership 
(Limited 
Partnership) 
(福州創新創科
投資合夥企業
(有限合夥)) 
3,028,400 
– 
– 
0.13% 
January 1, 
2027  
Ningbo Fengxi 
Venture 
Investment 
Partnership 
(Limited 
Partnership) 
(寧波豐曦創業
投資合夥企業
(有限合夥) 
3,028,400 
– 
– 
0.13% 
January 1, 
2027  
Zibo Pufeng 
Darun Equity 
Investment 
Fund 
Partnership 
(Limited 
Partnership) 
(淄博普豐達潤
股權投資基金
合夥企業(有限
合夥) 
2,577,350 
1,288,700 
0.11% 
0.11% 
January 1, 
2027  
Lighthouse 
Capital (HK) 
Financial 
2,166,100 
– 
– 
0.09% 
January 1, 
2027  

<<<PAGE 23>>>
21 
 
Limited (光源
資本(香港)金
融有限公司) 
Quanzhou 
Hongzhao 
Qiangxin 
Venture 
Investment 
Partnership 
(Limited 
Partnership) 
(泉州宏兆強芯
創業投資合夥
企業(有限合
夥) 
2,018,900 
– 
– 
0.08% 
January 1, 
2027  
Champ Earn 
49,850,450 
49,850,450 
4.30% 
2.08% 
January 1, 
2027  
PA GCC 
47,573,650 
47,573,650 
4.11% 
1.99% 
January 1, 
2027  
Huzhou Jingxin 36,217,700 
36,217,700 
3.13% 
1.51% 
January 1, 
2027  
Lobelia 
30,447,100 
30,447,100 
2.63% 
1.27% 
January 1, 
2027  
Jiaxin Zhizao 
29,049,500 
29,049,500 
2.51% 
1.21% 
January 1, 
2027  
Jiuyi Xinyuan 
 
14,755,650 
 
14,755,650 
1.27% 
0.62% 
January 1, 
2027  
Suzhou Yuanqi 
 
13,063,650 
 
13,063,650 
1.13% 
0.55% 
January 1, 
2027  
Matrice Capital 13,063,650 
13,063,650 
1.13% 
0.55% 
January 1, 
2027  
Tianjin Yuheng 23,280,200 
23,280,200 
2.01% 
0.97% 
January 1, 
2027  
3W Global 
20,397,000 
20,397,000 
1.76% 
0.85% 
January 1, 
2027  
MSA Growth 
19,029,450 
19,029,450 
1.64% 
0.79% 
January 1, 
2027  
Nantong 
Jianghai Fund  
18,882,200 
18,882,200 
1.63% 
0.79% 
January 1, 
2027  
Gaorong 
Kangteng 
15,495,850 
15,495,850 
1.34% 
0.65% 
January 1, 
2027  
Gaorong 
Kangyong 
2,734,550 
2,734,550 
0.24% 
0.11% 
January 1, 
2027  
Champion 
Forest 
17,015,050 
17,015,050 
1.47% 
0.71% 
January 1, 
2027  
Suzhou Juyuan 
16,394,500 
16,394,500 
1.42% 
0.68% 
January 1, 
2027  
Maxwise 
Investments 
15,223,550 
15,223,550 
1.31% 
0.64% 
January 1, 
2027  

<<<PAGE 24>>>
22 
 
Limited (萬慧
投資有限公司) 
Zhihui Unicorn  14,524,750 
14,524,750 
1.25% 
0.61% 
January 1, 
2027  
BAI GmbH 
14,490,850 
14,490,850 
1.25% 
0.60% 
January 1, 
2027  
Shanghai GP 
12,153,600 
12,153,600 
1.05% 
0.51% 
January 1, 
2027  
Shenzhen 
Qianhai 
9,722,900 
9,722,900 
0.84% 
0.41% 
January 1, 
2027  
Praise Fortune 
9,514,750 
9,514,750 
0.82% 
0.40% 
January 1, 
2027  
RCIF 
9,514,750 
9,514,750 
0.82% 
0.40% 
January 1, 
2027  
Yancheng 
Huayao 
Intelligent 
Computing 
Venture Capital 
Investment 
Partnership 
(Limited 
Partnership) 
(鹽城華耀智算
創業投資合夥
企業(有限合
夥)) 
 
5,675,250 
 
5,675,250 
0.49% 
0.24% 
January 1, 
2027  
Jiaxing 
Guangren 
7,721,450 
7,721,450 
0.67% 
0.32% 
January 1, 
2027  
China 
Insurance 
Investment Co., 
Ltd. 
(中保投資有限
責任公司) 
5,561,750 
5,561,750 
0.48% 
0.23% 
January 1, 
2027  
Nanchang 
Zhengtong 
Equity 
Investment 
Fund 
Partnership 
(Limited 
Partnership) 
(南昌政通股權
投資基金合夥
企業(有限合
夥)) 
5,277,950 
5,277,950 
0.46% 
0.22% 
January 1, 
2027  

<<<PAGE 25>>>
23 
 
 
 
Cornerstone Investors 
Shanghai 
Haitong Zhida 
Private 
Equity 
Investment 
Fund 
Partnership 
(Limited 
Partnership) 
(上海海通智達
私募投資基金
合夥企業(有限
合夥)) 
397,250 
397,250 
0.03% 
0.02% 
January 1, 
2027  
Jiaxing 
Benshuo 
Venture Capital 
Investment 
Partnership 
(Limited 
Partnership) 
(嘉興犇碩創業
投資合夥企業
(有限合夥)) 
 
4,937,450 
 
4,937,450 
0.43% 
0.21% 
January 1, 
2027  
Black Dragon 
AP SPV1 
4,125,900 
4,125,900 
0.36% 
0.17% 
January 1, 
2027  
Shaanxi 
Zhongtou 
Zhanlu Phase II 
Equity 
Investment 
Partnership 
(Limited 
Partnership) 
(陝西眾投湛盧
二期股權投資
合夥企業(有限
合夥)) 
2,043,100 
2,043,100 
0.18% 
0.09% 
January 1, 
2027  
Wimzie Zotac 
Limited 
1,135,050 
1,135,050 
0.10% 
0.05% 
January 1, 
2027  
Subtotal 
1,437,375,850 
736,830,424 
63.62% 
59.99% 
 
Notes: 
1. Please refer to the Prospectus for further details. 
2. Assuming the Over–allotment Option is not exercised. 
3. The expiry date of the lock–up period shown in the table above is pursuant to applicable PRC 
laws. 

<<<PAGE 26>>>
24 
 
Name 
Number of Shares held in 
the Company subject to lock-
up 
undertakings 
upon 
Listing 
% of total issued Shares after the 
Global Offering subject to lock-
up undertakings upon Listing 
(assuming the Over-allotment 
Option is not exercised) 
Last day subject to the 
lock-up undertakings 
Note 2 
3W Fund 
31,769,600 
1.33%  
July 1, 2026 
Qiming 
Venture 
Partners  
13,899,200  
0.58% 
July 1, 2026 
AMF 
11,913,600  
0.50% 
July 1, 2026 
WT Asset 
Management 
11,913,600  
0.50% 
July 1, 2026 
Hao Great 
China Focus 
Fund  
7,942,400  
0.33% 
July 1, 2026 
Ping An Life 
Insurance 
5,956,800 
0.25% 
July 1, 2026 
Huadeng 
Technology 
5,956,800 
0.25% 
July 1, 2026 
Lion Global 
5,956,800 
0.25% 
July 1, 2026 
CICC FT 
5,956,800 
0.25% 
July 1, 2026 
MY Asian 
4,765,400 
0.20% 
July 1, 2026 
Eastspring 
3,971,200 
0.17% 
July 1, 2026 
UBS 
AM 
Singapore 
3,971,200 
0.17% 
July 1, 2026 
Taikang Life 
3,971,200 
0.17% 
July 1, 2026 
Aspirational 
China 
Growth 
3,971,200 
0.17% 
July 1, 2026 
Charoen 
Pokphand 
3,971,200 
0.17% 
July 1, 2026 
Digital China 3,971,200 
0.17% 
July 1, 2026 
GTJA HK  
 
3,176,800 
0.13% 
July 1, 2026 
China 
Southern  
3,176,800 
0.13% 
July 1, 2026 
Fullgoal 
Fund  
3,176,600 
0.13% 
July 1, 2026 
Yeebo 
2,581,200 
0.11% 
July 1, 2026 
EIP 
1,985,600 
0.08% 
July 1, 2026 
Tessy 
Holding 
Limited 
1,985,600 
0.08% 
July 1, 2026 
New 
Opportunitie
s SPC 
1,985,600 
0.08% 
July 1, 2026 
Total 
147,926,400 
6.17% 
 

<<<PAGE 27>>>
25 
 
PLACEE CONCENTRATION ANALYSIS  
Placees* 
Number of Shares 
allotted 
Allotment as % of 
International Offering 
(assuming no exercise of 
the 
Over-allotment 
Option)  
Allotment as % of total 
Offer 
Shares 
(assuming no exercise 
of the Over- allotment 
Option) 
Allotment as % of total Offer 
Shares (assuming the Over-
allotment Option is fully 
exercised and new Shares are 
issued) 
Allotment 
as 
% 
of 
International 
Offering 
(assuming full exercise of the 
Over-allotment Option) 
Allotment as % of total Offer 
Shares 
(assuming 
full 
exercise 
of 
the 
Over- 
allotment Option) 
% of total issued share capital 
upon Listing (assuming the 
Over-allotment Option is fully 
exercised and new Shares are 
issued) 
Top 1 
31,769,600 
13.5013%  
11.1532%  
1.3259% 
11.4265% 
9.6985% 
1.3026% 
Top 5 
77,438,400  
32.9094%  
27.1860%  
3.2318%  
27.8521% 
23.6400% 
3.1752% 
Top 10 
111,098,000  
47.2139%  
39.0027%  
4.6366%  
39.9583% 
33.9155% 
4.5553% 
Top 25 
171,226,600  
72.7670%  
60.1119%  
7.1460%  
61.5846% 
52.2712% 
7.0208% 
 
Note 
* Ranking of placees is based on the number of Offer Shares allotted to the placees.  
 
SHAREHOLDER CONCENTRATION ANALYSIS  
H 
Shareholders
* 
Number 
of 
H 
Shares allotted 
Allotment as % of 
International Offering 
(assuming no exercise 
of the Over-allotment 
Option)  
 
Allotment as % of 
International Offering 
(assuming the Over-
allotment Option is 
fully exercised and 
new Shares are issued) 
Allotment as % of total 
Offer 
Shares 
(assuming no exercise 
of the Over- allotment 
Option) 
Allotment as % of total 
Offer Shares (assuming 
the 
Over-allotment 
Option is fully exercised 
and new Shares are 
issued) 
Number of H Shares held 
upon Listing 
% of total issued 
share capital upon 
Listing (assuming no 
exercise of the Over-
allotment Option) 
% of total issued share 
capital 
upon 
Listing 
(assuming 
the 
Over-
allotment Option is fully 
exercised and new Shares 
are issued) 
Number of Shares held 
upon Listing 
Top 1 
   
-   
0.0000% 
0.0000% 
0.0000% 
0.0000% 
   
-   
0.0000% 
0.0000% 
   
374,396,200  
Top 5 
   
13,904,800  
5.9092% 
4.2448% 
4.8815% 
4.2448% 
   
144,944,424  
6.0491% 
5.9431% 
   
731,870,750  
Top 10 
   
17,459,400  
7.4198% 
5.3299% 
6.1294% 
5.3299% 
   
255,102,124  
10.6464% 
10.4599% 
   
1,068,309,15
0  

<<<PAGE 28>>>
26 
 
Top 25 
   
59,454,600  
25.2667% 
18.1500% 
20.8725% 
18.1500% 
   
694,108,024  
28.9679% 
28.4604% 
   
1,667,719,55
0  
Note 
* Ranking of Shareholders is based on the number of Shares held by the Shareholders upon Listing.  
 
 
H SHAREHOLDER CONCENTRATION ANALYSIS  
H 
Shareholders* 
Number of H 
Shares allotted 
Allotment as % of 
International 
Offering 
(assuming no exercise of 
the 
Over-allotment 
Option)  
 
Allotment as % of 
International Offering 
(assuming the Over-
allotment Option is fully 
exercised 
and 
new  
Shares are issued) 
Allotment as % of total 
Offer Shares (assuming 
no exercise of the Over- 
allotment Option) 
Allotment as % of total Offer 
Shares (assuming the Over-
allotment 
Option 
is 
fully 
exercised and new Shares are 
issued) 
Number of 
Shares held upon Listing 
Number of 
Shares held upon Listing 
Top 1 
   
13,899,200  
5.9068% 
4.8795% 
   
59,785,900  
2.4951% 
   
105,632,600  
4.4085% 
Top 5 
   
59,151,400  
25.1379% 
20.7661% 
   
263,429,000  
10.9939% 
   
337,651,900  
14.0915% 
Top 10 
   
59,355,400  
25.2246% 
20.8377% 
   
467,254,774  
19.5004% 
   
644,689,450  
26.9054% 
Top 25 
   
63,828,600  
27.1256% 
22.4081% 
   
819,512,624  
34.2015% 
   
1,105,951,350  
46.1557% 
Note 
* Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.  
.  

<<<PAGE 29>>>
27 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING  
Subject to the satisfaction of the conditions set out in the Prospectus, 471,116 valid applications 
made by the public will be conditionally allocated on the basis set out below:  
 
NO. OF 
SHARES 
APPLIED 
FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF ALLOTMENT / BALLOT 
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF 
SHARES 
APPLIED FOR 
POOL A 
200 
174,816 
8,741 out of 174,816 applicants to 
receive 200 H Shares 
5.00% 
400 
25,420 
1,954 out of 25,420 applicants to receive 
200 H Shares 
3.84% 
600 
19,979 
1,996 out of 19,979 applicants to receive 
200 H Shares 
3.33% 
800 
9,280 
 
1,062 out of 9,280 applicants to receive 
200 H Shares 
2.86% 
1,000 
13,714 
 
1,716 out of 13,714 applicants to receive 
200 H Shares 
2.50% 
1,200 
6,869 
 
912 out of 6,869 applicants to receive 
200 H Shares 
2.21% 
1,400 
8,272 
 
1,194 out of 8,272 applicants to receive 
200 H Shares 
2.06% 
1,600 
6,977 
 
1,084 out of 6,977 applicants to receive 
200 H Shares 
1.94% 
1,800 
6,525 
 
1,110 out of 6,525 applicants to receive 
200 H Shares 
1.89% 
2,000 
35,199 
 
6,495 out of 35,199 applicants to receive 
200 H Shares 
1.85% 
3,000 
9,407 
 
2,341 out of 9,407 applicants to receive 
200 H Shares 
1.66% 
4,000 
9,206 
 
2,578 out of 9,206 applicants to receive 
200 H Shares 
1.40% 
5,000 
11,145 
 
3,357 out of 11,145 applicants to receive 
200 H Shares 
1.20% 
6,000 
9,328 
 
2,979 out of 9,328 applicants to receive 
200 H Shares 
1.06% 
7,000 
4,560 
 
1,585 out of 4,560 applicants to receive 
200 H Shares 
0.99% 
8,000 
4,554 
 
1,702 out of 4,554 applicants to receive 
200 H Shares 
0.93% 
9,000 
3,269 
 
1,303 out of 3,269 applicants to receive 
200 H Shares 
0.89% 
10,000 
21,045 
 
8,882 out of 21,045 applicants to receive 
200 H Shares 
0.84% 
20,000 
12,176 
 
7,502 out of 12,176 applicants to receive 
200 H Shares 
0.62% 

<<<PAGE 30>>>
28 
 
30,000 
7,587 
 
5,833 out of 7,587 applicants to receive 
200 H Shares 
0.51% 
40,000 
5,426 
 
4,881 out of 5,426 applicants to receive 
200 H Shares 
0.45% 
50,000 
4,914 
 
200 H Shares plus 78 out of 4,914 
applicants to receive an additional 200 H 
Shares 
0.41% 
60,000 
3,573 
 
200 H Shares plus 437 out of 3,573 
applicants to receive an additional 200 H 
Shares 
0.37% 
70,000 
2,717 
 
200 H Shares plus 600 out of 2,717 
applicants to receive an additional 200 H 
Shares 
0.35% 
80,000 
2,493 
 
200 H Shares plus 781 out of 2,493 
applicants to receive an additional 200 H 
Shares 
0.33% 
90,000 
1,926 
 
200 H Shares plus 771 out of 1,926 
applicants to receive an additional 200 H 
Shares 
0.31% 
100,000 
12,802 
 
200 H Shares plus 6,184 out of 12,802 
applicants to receive an additional 200 H 
Shares 
0.30% 
200,000 
8,682  400 H Shares 
0.20% 
 
   
 
Total   
441,861   
Total number of Pool A successful 
applicants: 106,314 
 
 
  
 
 
POOL B 
300,000 
9,925 
600 H Shares 
0.20% 
400,000 
4,148 
600 H Shares plus 1,695 out of 4,148 
applicants to receive an additional 200 H 
Shares 
0.17% 
500,000 
2,877  600 H Shares plus 2,197 out of 2,877 
applicants to receive an additional 200 H 
Shares 
0.15% 
600,000 
2,016  800 H Shares 
0.13% 
700,000 
1,369  800 H Shares plus 507 out of 1,369 
applicants to receive an additional 200 H 
Shares 
0.12% 
800,000 
1,140  800 H Shares plus 726 out of 1,140 
applicants to receive an additional 200 H 
Shares 
0.12% 
900,000 
910  1,000 H Shares 
0.11% 
1,000,000 
3,850  1,000 H Shares plus 459 out of 3,850 
applicants to receive an additional 200 H 
Shares 
0.10% 
2,000,000 
1,489  1,200 H Shares plus 1,225 out of 1,489 
applicants to receive an additional 200 H 
Shares 
0.07% 

<<<PAGE 31>>>
29 
 
3,000,000 
559  1,400 H Shares plus 280 out of 559 
applicants to receive an additional 200 H 
Shares 
0.05% 
4,000,000 
267  1,800 H Shares 
0.05% 
5,000,000 
204  2,200 H Shares 
0.04% 
6,192,400 
501  2,600 H Shares 
0.04% 
 
 
  
 
Total   
29,255   
Total number of Pool B successful 
applicants: 29,255 
 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries. 
  
COMPLIANCE WITH LISTING RULES AND GUIDANCE  
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s Shares.  
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or indirectly, 
provided by the issuer, its controlling shareholder(s), directors or syndicate members to any placees or 
the public (as the case may be) and the consideration payable by them for each share (or, where 
applicable, each unit of other equity securities or interests (which include equity securities, interests in 
a REIT, stapled securities and securities of an investment company (as defined in Rule 21.01)) of the 
issuer subscribed for or purchased by them is the same as the final offer price determined by the issuer, 
in addition to any brokerage, AFRC transaction levy, SFC transaction levy and trading fee payable. 
The Directors and the Overall Coordinators confirm that at least 50% of the total number of the Offer 
Shares have been allocated to and taken up by independent price setting investors in compliance with 
Rule 18C.08 of the Listing Rules.  
The Directors further confirm that at least 20% of the issued share capital of the Company will be held 
by sophisticated independent investors at the time of Listing in compliance with Chapter 2.5 of the 
Guide for New Listing Applicants.  
OTHERS / ADDITIONAL INFORMATION  
 
Offer Size Adjustment Option  
 
The Offer Size Adjustment Option has been exercised in full, pursuant to which the Company is issuing 
and allotting 37,153,800 additional Shares, representing approximately 15.0% of the total number of 
Shares initially available under the Global Offering, at the final Offer Price to increase the number of 
Offer Shares available under the International Offering. 
 
Accordingly, the total number of Offer Shares finally available under the Global Offering (after taking 
into account the full exercise of the Offer Size Adjustment Option and before any exercise of the Over-
allotment Option) that would be allotted and issued by the Company is 284,846,600 Offer Shares and 
the total issued share capital of the Company upon Listing (after taking into account the full exercise 

<<<PAGE 32>>>
30 
 
of the Offer Size Adjustment Option and before any exercise of the Over-allotment Option) will be  
2,396,131,700 Shares.  
 
Reallocation 
 
As the Hong Kong Public Offering has been over-subscribed by more than 100 times of the total 
number of Offer Shares initially available under the Hong Kong Public Offering, the reallocation 
procedure as disclosed in the section headed “Structure of the Global Offering – The Hong Kong 
Public Offering – Reallocation” in the Prospectus has been applied. 
 
The number of Offer Shares initially available under the Hong Kong Public Offering is 12,384,800 
Shares, representing approximately 5% of the total number of Offer Shares initially available under 
the Global Offering (assuming the Offer Size Adjustment Option and the Over-allotment Option are 
not exercised). As a result of such reallocation, the final number of Offer Shares under the Hong Kong 
Public Offering is adjusted to 49,538,600 Shares, representing approximately 20% of the total number 
of Offer Shares initially available under the Global Offering (assuming the Offer Size Adjustment 
Option and the Over-allotment Option are not exercised). 
 
Placing to existing shareholders and/or its close associates with a prior waiver under Rule 10.04 
and consent under paragraph 1C(1) of the Placing Guidelines 
 
The Company has applied for a waiver under Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules, to permit the existing shareholders and/or its 
close associates to participate as either cornerstone investors or placees in the Global Offering to 
subscribe for the Offer Shares to be issued by the Company under the International Offering (together, 
the “Existing Shareholder Participants”). The Stock Exchange has agreed to grant the requested 
waiver and consent subject to the conditions that: 
 
(a) 
the allocation to the Existing Shareholder Participants will not affect the Company’s ability to 
satisfy its public float requirement under Rule 8.08(1) (as amended and replaced by Rule 
19A.13A) of the Listing Rules;  
 
(b) 
the Company and the Joint Sponsors confirm that no preferential treatment has been, nor will 
be directly or indirectly, given to the Existing Shareholder Participants as cornerstone investors 
or placees by virtue of their relationship with the Company in any allocation in the Global 
Offering, other than the preferential treatment of assured entitlement under the cornerstone 
investment at the Offer Price and the terms are substantially the same as other cornerstone 
investors; and  
 
(c) 
details of the subscription of the Offer Shares by the Existing Shareholder Participants as 
cornerstone investors or placees under the Global Offering have been disclosed in the 
Prospectus, and details of the allocation are disclosed in this allotment results announcement 
of the Company. 
 
For details of the allocations of Offer Shares to such Existing Shareholder Participants, please refer to 
the section headed “Allotment Results Details – International Offering – Allotees with 
Waivers/Consents Obtained” in this announcement.  
 
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines 

<<<PAGE 33>>>
31 
 
 
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines.  
 
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a consent 
under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such Offer Shares 
in the International Offering to the connected clients. The allocation of Offer Shares to such connected 
clients is in compliance with all the conditions under the consent granted by the Stock Exchange. 
Details of the placement to connected clients are set out below: 

<<<PAGE 34>>>
32 
 
No. 
Connected 
Distributo
r 
Connected 
Client 
Relationship 
Identities of the ultimate 
beneficial owners of the 
Offer Shares or, where 
applicable, details of the 
structured products under 
which the subscription by 
the Connected Client was 
made (e.g. OTC total return 
swaps) 
Whether the 
Connected Client is 
a collective 
investment scheme 
which is not 
authorised by the 
SFC or is expected 
to hold the Offer 
Shares on behalf of 
such scheme 
Maximum 
amount of 
Offer Shares to 
be allocated to 
the Connected 
Client (based 
on the low end 
of the 
indicative Offer 
Price range) 
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
percentage of total 
issued share capital 
after the Global 
Offering (assuming 
no exercise of the 
Over-allotment 
Option) 
Part A - Connected Client holding the beneficial interest of the Offer Shares on a non-discretionary basis on behalf of independent third parties 
1. 
China 
Internation
al Capital 
Corporatio
n Hong 
Kong 
Securities 
Limited 
(CICCHKS
) 
CICC 
Financial 
Trading 
Limited 
(CICC FT) 
Note 1 and note 2 
 
CICC FT is a 
member of the 
same group of 
CICCHKS. 
Please refer to note (1). 
N 
5,956,800 
2.09% 
0.25% 
Please refer to note (2). 
N 
587,200 
 
0.21% 
0.02% 
2. 
CLSA 
CITIC 
Securities 
Internation
al Capital 
Manageme
nt Limited 
(CSI) Note 3 
CSI is a member 
of the same group 
of companies as 
CLSA. 
Please refer to note (3). 
No 
443,000 
0.16% 
 
0.02% 
3. 
Guotai 
Junan 
Securities 
(Hong 
Kong) 
Guotai 
Junan 
Investment
s (Hong 
Kong) 
GTJA Investment 
is a member of 
the same group as 
Please refer to note (4). 
No 
576,400 
0.20% 
0.02% 
Please refer to note (5). 
3,176,800 
1.12% 
0.13% 

<<<PAGE 35>>>
33 
 
Limited 
(GTJA 
HK) and 
Haitong 
Internation
al 
Securities 
Company 
Limited 
(HTI) 
Limited 
(GTJA 
Investment
s) Note 4 and 5 
GTJA HK and 
HTI. 
4. 
HTI 
Financial 
Solutions 
Limited 
(HTIFSL) 
Note 6 
HTIFSL is a 
member of the 
same group as 
GTJA HK and 
HTI. 
Please refer to note (6). 
No 
4,175,600 
1.47% 
0.17% 
5. 
Huatai 
Financial 
Holdings 
(Hong 
Kong) Ltd 
(HTFH) 
Huatai 
Capital 
Investment 
Limited 
(HTCI) Note 
7 
HTCI is a 
member of the 
same group of 
HTFH. 
Please refer to note (7). 
No 
460,600 
0.16% 
0.02% 
 
 
No. 
Connected 
Distributo
r 
Connected Client 
Relationship 
Whether the Connected 
Client is a collective 
investment scheme 
which is not authorised 
by the SFC or is 
expected to hold the 
Offer Shares on behalf 
of such scheme 
Maximum amount 
of Offer Shares to 
be allocated to the 
Connected Client 
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
after the Global 
Offering (assuming no 
exercise of the Over-
allotment Option) 
Part B - Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties 
1. 
C ITIC Securities 
Asset Management 
CITICS AM is a 
member of the same 
No 
7,942,400  
2.79% 
0.33% 

<<<PAGE 36>>>
34 
 
No. 
Connected 
Distributo
r 
Connected Client 
Relationship 
Whether the Connected 
Client is a collective 
investment scheme 
which is not authorised 
by the SFC or is 
expected to hold the 
Offer Shares on behalf 
of such scheme 
Maximum amount 
of Offer Shares to 
be allocated to the 
Connected Client 
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
after the Global 
Offering (assuming no 
exercise of the Over-
allotment Option) 
CLSA 
Limited 
(CLSA) 
 
Company Limited 
(CITICS AM) Note 8 
group of companies as 
CLSA. 
2. 
China Asset 
Management (Hong 
Kong) Limited (China 
AMC HK)Note 9 
China AMC HK is a 
member of the same 
group of companies 
as CLSA.   
N 
317,600 
0.11% 
0.01% 
3. 
Orient 
Securities 
(Hong 
Kong) 
Limited 
(Orient 
Securities) 
 
China Universal Asset 
Management (Hong 
Kong) Company 
Limited (China 
Universal (HK)) Note 10 
China Universal (HK) 
is a member of the 
same group of 
companies as Orient 
Securities. 
N 
317,600 
0.11% 
0.01% 
4. 
Orient Asset 
Management (Hong 
Kong) Limited (Orient 
AM) Note11 
Orient AM is a 
member of the same 
group of Orient 
Securities. 
Y 
8,000 
0.00% 
0.00% 
5. 
Guosen 
Securities 
(HK) 
Brokerage 
Company 
Limited 
(Guosen 
Guosen Securities 
(HK) Asset 
Management 
Company Limited 
(Guosen HK AM) Note 
12 
Guosen HK AM is a 
member of the same 
group of companies as 
Guosen HK 
Brokerage. 
N 
79,400 
0.03% 
0.00% 

<<<PAGE 37>>>
35 
 
No. 
Connected 
Distributo
r 
Connected Client 
Relationship 
Whether the Connected 
Client is a collective 
investment scheme 
which is not authorised 
by the SFC or is 
expected to hold the 
Offer Shares on behalf 
of such scheme 
Maximum amount 
of Offer Shares to 
be allocated to the 
Connected Client 
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
after the Global 
Offering (assuming no 
exercise of the Over-
allotment Option) 
HK 
Brokerage) 
6. 
UBS AG 
Hong Kong 
Branch and 
UBS AG 
Singapore 
Branch 
(UBS AG) 
ICBC UBS Asset 
Management Co., Ltd. 
(ICBC UBS) Note 13 
Both ICBC UBS and 
ICBC UBS 
(International) are 
members of the same 
group of companies as 
UBS AG. 
N 
37,000 
 
0.01% 
0.00% 
7. 
ICBC UBS Asset 
Management 
(International) 
Company Limited 
(ICBC UBS 
(International)) Note 13 
N 
2,600 
0.00% 
0.00% 
8. 
UBS Asset 
Management 
(Singapore) Ltd. (UBS 
AM Singapore) Note 14 
UBS AM Singapore is 
a member of the same 
group of companies as 
UBS AG. 
N 
3,971,200 
1.39% 
0.17% 
9. 
Guotai 
Junan 
Securities 
(Hong 
Kong) 
Limited 
(GTJA 
Haitong International 
Asset Management 
(HK) Limited 
(Haitong AM) Note 15 
Haitong AM is a 
member of the same 
group as GTJA HK 
and HTI. 
N 
19,800 
0.01% 
0.00% 
10.  
Management Co., Ltd. 
(富國基金管理 有限
Guotai Haitong 
Securities Co., Ltd. 
N 
1,906,000 
0.67% 
0.08% 

<<<PAGE 38>>>
36 
 
No. 
Connected 
Distributo
r 
Connected Client 
Relationship 
Whether the Connected 
Client is a collective 
investment scheme 
which is not authorised 
by the SFC or is 
expected to hold the 
Offer Shares on behalf 
of such scheme 
Maximum amount 
of Offer Shares to 
be allocated to the 
Connected Client 
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
after the Global 
Offering (assuming no 
exercise of the Over-
allotment Option) 
HK) and 
Haitong 
Internation
al 
Securities 
Company 
Limited 
(HTI) 
公司) (“Fullgoal 
Fund”) Note16 
(Guotai Haitong) 
holds approximately 
27.75% in the manager 
of Fullgoal Fund.  
Fullgoal Fund and 
Fullgoal HK (together, 
Fullgoal Fund) is a 
member of the same 
group as GTJA HK 
and HTI. 
11.  
Fullgoal Asset 
Management (HK) 
Limited (“Fullgoal 
HK”) Note 16 
N 
1,270,600 
0.45% 
0.05% 
12.  HTFH 
China Southern Asset 
Management Co., Ltd. 
(南方基金管理股份
有限公司) (China 
Southern) Note 17 
China Southern is held 
by Huatai Securities 
Co., Ltd. (華泰證券股
份有限公司) as to 
41.16%, which wholly 
owns HTFH. 
As such, China 
Southern and HTFH is 
a member of the same 
group of companies. 
N 
3,176,800 
1.12% 
0.13% 
 
 

<<<PAGE 39>>>
37 
 
Note: 
1. 
CICC FT has entered into cornerstone investment agreements with the Company, the Joint Sponsors and the Sponsor-OCs, to participate as a 
cornerstone investor in the Global Offering to subscribe for the Offer Shares to be issued by the Company under the International Offering. 
CICC FT and China International Capital Corporation Limited has entered into a series of cross border delta-one OTC swap transactions (collectively, 
the Greenwoods OTC Swaps) with each other and the ultimate clients (the CICC FT Ultimate Clients (Greenwoods)), pursuant to which CICC FT 
will hold the Offer Shares on a non-discretionary basis to hedge the Greenwoods OTC Swaps while the economic risks and returns of the underlying 
Offer Shares are passed to the CICC FT Ultimate Clients (Greenwoods), subject to customary fees and commissions. The Greenwoods OTC Swaps 
will be fully funded by the CICC FT Ultimate Clients (Greenwoods). During the terms of the Greenwoods OTC Swaps, all economic returns of the 
Offer Shares subscribed by CICC FT will be passed to the CICC FT Ultimate Clients (Greenwoods) and all economic loss shall be borne by the 
CICC FT Ultimate Clients (Greenwoods) through the Greenwoods OTC Swaps, and CICC FT will not take part in any economic return or bear any 
economic loss in relation to the Offer Shares. 
To the best of CICC FT’s knowledge having made all reasonable inquiries, each of the CICC FT Ultimate Clients (Greenwoods) is an Independent 
Third Party of CICC FT, CICCHKS and the companies which are members of the same group of CICCHKS, and no single ultimate beneficial owner 
holds 30% or more interests in each of the CICC FT Ultimate Clients (Greenwoods).  
2. 
CICC FT and China International Capital Corporation Limited (CICCL) will enter into a series of cross border delta-one OTC equity swap 
transactions (collectively, the “CICCFT OTC Swaps”) with each other and the ultimate clients (the “CICC FT Ultimate Clients”), pursuant to 
which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the CICCFT OTC Swaps  while the economic risks and returns of 
the underlying Offer Shares are passed to the CICC FT Ultimate Client, subject to customary fees and commissions. The CICCFT OTC Swaps will 
be fully funded by the CICC FT Ultimate Clients. During the term (which is one year although the CICC FT Ultimate Clients can terminate anytime) 
of the CICCFT OTC Swaps , all economic returns of the Offer Shares subscribed by CICC FT as Connected Client will be passed to the CICC FT 
Ultimate Clients and all economic losses shall be borne by the CICC FT Ultimate Clients through the CICCFT OTC Swaps , and CICC FT will not 
take part in any economic return or bear any economic loss in relation to the Offer Shares. The termination of the CICCFT OTC Swaps will not 
result CICC FT holding the Offer Shares in its proprietary account. Despite that CICC FT will hold the legal title of the Offer Shares by itself, it will 
not exercise the voting rights attaching to the relevant Offer Shares during the terms of the CICCFT OTC Swaps according to its internal policy. 
Consequently, CICC FT Ultimate Client is not entitled to any voting rights of the relevant Offer Shares.  
The CICC FT Ultimate Clients are (i) Wangzheng Gongying No. 17 Private Securities Investment Fund (望正共贏17 號私募證券投資基金), 
whose manager is Shenzhen Wangzheng Asset Management Co., Ltd (深圳望正資產管理有限公司). Other than Qu Qin (翟琴), no ultimate 
beneficial owner holds 30% or more interest in the fund; (ii) Longrising Qiangshu Private Equity Investment Fund (源樂晟強樹私募證券投資基
金) managed by Tibet Longrising Asset Management Co., Ltd (西藏源樂晟資產管理有限公司), the UBO of which is Zeng Xiaojie; and (iii) the 
following funds managed by Pinpoint Investment Management Limited (上海保銀私募基金管理有限公司): Pinpoint Jinqu No.1 Private Equity 
Investment Fund (保銀進取1 號私募證券投資基金) with no UBO of 30% or more interest, Pinpoint Duokong Stable No.1 Equity Investment 
Fund (保銀多空穩健1 號私募證券投資基金) whose UBO is Wang Qiang, and Pinpoint Duokong Stable No.2 Equity Investment Fund (保银多

<<<PAGE 40>>>
38 
 
空稳健2 号私募证券投资基金) whose UBO is Wang Qiang. To the best of CICC FT’s knowledge having made all reasonable inquiries, each of 
the CICC FT Ultimate Clients is an independent third party of CICC FT, CICCHKS and the companies which are members of the same group of 
CICCHKS. 
3. 
CSI proposes to subscribe for and hold the Offer Shares as a placee under the International Offering on behalf of CSI Ultimate Clients, each of them 
is an independent third party, on a non-discretionary basis, pursuant to which:  
(i) 
CSI will act as the single counterparty of a back-to-back total return swap transaction (the CSI Back-to-back TRS) to be entered into by it in 
connection with a total return swap order (the CSI Client TRS) placed and fully funded by the CSI Ultimate Client, by which CSI will pass 
the full economic exposure of the Offer Shares placed to CSI to the CSI Ultimate Client.  
(ii) 
As confirmed by CSI and CLSA, CSI will hold the legal title and beneficial interest in the Offer Shares, but will contractually agree to pass 
on the full economic exposure and return of the Offer Shares to the CSI Ultimate Client, on a non-discretionary basis. The CSI Ultimate 
Client may exercise their early termination rights to terminate the CSI Client TRS at any time from the trade date of the CSI Client TRS 
which should be on or after the date on which the Offer Shares are listed on the Stock Exchange. 
(iii) 
Upon the final maturity or termination of the CSI Client TRS by the CSI Ultimate Client, CSI will dispose of the Offer Shares on the secondary 
market and the CSI Ultimate Client will receive a final termination amount of the CSI Back-to-back TRS which will have taken into account 
all the economic returns or economic loss in relation to the Offer Shares and the fixed amount of transaction fees of the CSI Back- to-back 
TRS and the CSI Client TRS. Due to its internal policy, CSI will not exercise the voting right of the Offer Shares during the terms of the CSI 
Back-to-back TRS. 
Details of the CSI Ultimate Clients include (i) certain funds managed by Shanghai Panjing Investment Management Center (Limited Partnership) 
(上海盤京投資管理中心（有限合夥）); (ii) a private equity fund managed by Shanghai Jindan Asset Management Co., Ltd. (上海金澹資產管
理有限公司); (iii) a private equity fund managed by Hainan Langrun Lifang Private Fund Management Co., Ltd. (海南朗潤利方私募基金管理有
限公司); and (iv) HY Capital Company Limited. 
CSI has confirmed that, to the best of their knowledge and after making all reasonable enquiries, each of the CSI Ultimate Client and its ultimate 
beneficial owner is an independent third party of CSI, CLSA and the companies which are members of the same group of companies as CLSA. 
4. 
It is proposed that GTJA Investments participates as placee to subscribe for the Offer Shares under the International Offering (the GTJAI 
Subscription). In relation to the GTJAI Subscription, GTJA Investments shall hold the Offer Shares for hedging purpose as the single underlying 
asset of several sets of back-to-back total return swap transaction (the GTHT Back-to-back TRS) to be entered into between GTJA Investments and 
Guotai Haitong Securities Co., Ltd. (the GTHT Onshore Parent) in connection with several total return swap orders (the GTHT Client TRS) to be 
entered into by GTHT Onshore Parent and several ultimate clients (the GTHT Onshore Ultimate Clients), respectively. Such GTHT Client TRS is 
to be fully funded by the GTHT Onshore Ultimate Client. GTJA Investments will hold the Offer Shares on a non-discretionary basis for the purpose 
of hedging the economic exposure under the GTHT Back-to-back TRS and GTHT Client TRS only, During the tenor of the GTHT Client TRS, all 

<<<PAGE 41>>>
39 
 
economic returns of the Offer Shares will be passed to the GTHT Onshore Ultimate Clients and all economic losses shall be borne by the GTHT 
Onshore Ultimate Client, subject to the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS, and GTJA Investments will 
not take part in any economic return or bear any economic loss in relation to the price of the Offer Shares. The GTHT Onshore Ultimate Client may 
request to redeem the Offer Shares at their own discretion, upon which GTJA Investments shall dispose of the Offer Shares and settle the GTHT 
Back-to-back TRS and GTHT Client TRS in cash in accordance with the terms and conditions of the GTHT Back-to-back TRS and GTHT Client 
TRS documents.  
Due to its internal policy, GTJA Investments will not exercise the voting right attaching to the Offer Shares during the tenor of the GTHT Back-to-
back TRS and GTHT Client TRS.  
The GTHT Onshore Ultimate Client for purpose of this place subscription include (i) Beijing Yiyuanda Investment Management Co., Ltd. (北京逸
原達投資管理有限公司), with Huang Hui (黃輝) being its UBO; and (ii) Yucheng Private Equity Fund Management (Hainan) Partnership (Limited 
Partnership) (宇誠私募基金管理（海南）合夥企業（有限合夥）), with ZHANG Weihua (張衛華) and HONG Yan (洪燕) being its UBOs. 
GTJA Investments has confirmed that, to the best of their knowledge and after making all reasonable enquiries, each of the GTHT Onshore Ultimate 
Clients and its ultimate beneficial owner is an independent third party of GTJA Investments, HTI and the companies which are members of the same 
group of companies as HTI. 
5. 
In addition, as disclosed in the Prospectus, (i) GTJA Investments has entered into a cornerstone investment agreement with the Company, and (ii) 
GTJA Investments and, among others, Jinxiu No. 608 Private Investment Fund (Jinxiu 608) or (Guotai Haitong Ultimate Customer (Zhonghe)) 
managed by Jinxiu Zhonghe (Tianjin) Investment Management Co., Ltd. (錦繡中和(天津)投資管理有限公司) (Zhonghe Capital) will conduct a 
series of cross-border Delta-one over-the-counter swap transactions (Zhonghe OTC Swaps). Under these transaction arrangements, GTJA HK will 
hold the Offer Shares on a non-discretionary basis to hedge risks for Zhonghe OTC Swaps. After deducting customary fees and commissions, the 
economic risks and benefits associated with the underlying offered shares will be transferred to Guotai Haitong Ultimate Customer (Zhonghe).  
As far as GTJA Investments is aware, Guotai Haitong Ultimate Customer (Zhonghe) is an independent third party to GTJA Investments, HTI, and 
companies within the same group as HTI. 
6. 
HTIFSL has entered into a total return swap transaction trade (the HTI TRS) with each of (i) Shenzhen NewFoxon Investment Management CO., 
LTD. (深圳紐富斯投資管理有限公司), with ZHOU Cong (周聰) being its UBO; (ii) Lingding Investment Management Co., Ltd. (寧波梅山保稅
港區淩頂投資管理有限公司), with Xiong Nawei (熊納微) and Song Chen (宋辰) being its UBO; (iii) SMIC Juyuan Private Equity Fund 
Management (Shanghai) Co., Ltd (中芯聚源私募基金管理（上海）有限公司), which is a close associate of an existing shareholder; and (iv) 
Shanghai Weining Investment Mangement Co., Ltd (上海衛寧私募基金管理有限公司), with LIU YUTAO (劉育濤) being its UBO, (the HTI 
Ultimate Clients), pursuant to which HTIFSL will hold the Offering Shares on a non-discretionary basis as the single underlying holder under the 
HTI TRS. The full economic exposure of the Offer Shares will be passed to each of the HTI Ultimate Clients, while HTIFSL will hold the beneficial 
interest of the Offering Shares on behalf of each of the HTI Ultimate Clients. 

<<<PAGE 42>>>
40 
 
Due to its internal policy, HTIFSL will not exercise the voting rights of the Offer Shares during the term of HTI TRS. 
To the best of HTCI’s knowledge having made all reasonable inquiries, each of the HTI Ultimate Clients and their respective ultimate beneficial 
owners is an independent third party of HTIFSL, HTI and the companies which are members of the same group of HTI. 
7. 
Huatai Securities Co., Ltd. (“Huatai Securities”) is one of the domestic securities firms licensed to undertake cross-border derivatives trading 
activities. Huatai Securities entered into an ISDA agreement (the “ISDA Agreement”) with its indirectly wholly-owned subsidiary, HTCI, to set 
out the principal terms of any future total return swap between Huatai Securities and HTCI.  
HTCI is a member of the same group of HTFH. Pursuant to the ISDA Agreement, HTCI, which intends to participate in the Global Offering as a 
placee, will hold the beneficial interest of the Offer Shares on a non-discretionary basis as the single underlying holder under a back-to-back total 
return swap (the “Back-to-back TRS”) to be entered by HTCI in connection with a Client TRS (as defined below) placed by and fully funded (i.e. 
with no financing provided by HTCI) by the Huatai Ultimate Clients (as defined below), by which, HTCI will, subject to customary fees and 
commissions, pass the full economic exposure of the Offer Shares ultimately to the Huatai Ultimate Clients, which in effect, HTCI will hold the 
beneficial interest of the Offer Shares on behalf of the Huatai Ultimate Clients. HTFH and HTCI are indirectly wholly owned subsidiaries of Huatai 
Securities. Accordingly, HTCI is considered as a “connected client” of HTFH pursuant to paragraph 1B of the Placing Guidelines.  
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the “Huatai Ultimate Clients”) cannot directly subscribe for the 
Offer Shares but may invest in derivative products issued by domestic securities firms licenced to undertake cross-border derivatives trading activities, 
such as Huatai Securities, with the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, the Huatai Ultimate 
Clients, through its investment manager, will place a total return swap order (the “Client TRS”) with Huatai Securities in connection with the 
Company’s IPO and Huatai Securities will place a Back-to-back TRS order to HTCI on the terms of the ISDA Agreement. In order to hedge its 
exposure under the Back-to-back TRS, HTCI participates in the Company’s initial public offering and subscribes the Offer Shares through placing 
order with HTFH during the International Placing.  
To the best of our knowledge and after making all reasonable enquiries, each of the Huatai Ultimate Clients is an independent third party of HTCI, 
HTFH and the companies which are members of the same group of HTCI. 
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in connection with the Client TRS order placed by the 
Huatai Ultimate Clients. Pursuant to the terms of the contracts of the Back-to-back TRS and the Client TRS, during the tenor of the Back-to-back 
TRS and the Client TRS, subject to customary fees and commissions, all economic returns of the Offer Shares will be ultimately passed to the Huatai 
Ultimate Clients through the Back-to-back TRS and the Client TRS and all economic loss shall be ultimately borne by the Huatai Ultimate Clients. 
HTCI will not take any economic return or bear any economic loss in relation to the Offer Shares.  
Investment in the Back-to-back TRS and the Client TRS is similar to the investment in a qualified domestic institutional investor fund (“QDII”) in 
the way that the Huatai Ultimate Clients would reap all the economic benefits of the underlying Offer Shares, except that a QDII fund would pass 
through the exchange rate exposure on both the notional value of the investment and the profit and loss of the investment. In contrast, the profit and 
loss of the Back-to-back TRS and the Client TRS factor into account the fluctuation in RMB exchange rate upon termination of the Client TRS by 

<<<PAGE 43>>>
41 
 
converting the profit and loss using the current exchange rate at the time of termination. As such, the Huatai Ultimate Clients would bear the exchange 
rate exposure of the profit and loss on settlement date.  
The Huatai Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time from the issue date of the Client TRS 
which should be on or after the date on which the Offer Shares are listed on the Stock Exchange at its own discretion. Upon the termination upon 
maturity or early termination of the Client TRS by the Huatai Ultimate Clients, HTCI will dispose the Offer Shares on the secondary market and the 
Huatai Ultimate Clients will receive a final settlement amount in cash in accordance with the terms and conditions of the Back-to-back TRS and the 
Client TRS which should have taken into account all the economic returns or economic loss in relation to the Offer Shares. If upon the maturity of 
the Client TRS, the Huatai Ultimate Clients intends to extend the investment period, subject to further agreement between Huatai Securities and the 
relevant Huatai Ultimate Clients, the term of the Client TRS could be extended by way of a new issuance or a tenor extension. Accordingly, Huatai 
Securities will extend the term of the Back-to-back TRS by way of a new issuance or a tenor extension. 
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through the economic exposure to the 
Huatai Ultimate Clients, each being an onshore client who places a Client TRS order with Huatai Securities in connection with the IPO of the 
Company. HTCI will not exercise the voting right of the Offer Shares during the tenor of the Back-to-back TRS.  
During the life of the Client TRS and Back-to-back TRS, HTCI may continue to hold the Offer Shares in its custodian account, or to hold some or 
all of the Offer Shares in a prime brokerage account for stock borrowing purposes, where HTCI will lend out its holding of underlying Offer Shares 
in the form of stock borrowing loans consistent with market practice to lower its finance costs, provided that HTCI has the ability to call back the 
Offer Shares on loan at any time in order to satisfy its obligations under the Back-to-back TRS to ensure the economic interests are ultimately passed 
to the Huatai Ultimate Clients. 
The HTCI Ultimate Clients are (i) Xinyuan Tianxun Navigator Private Securities Investment Fund (芯源天循領航私募證券投資基金), whose 
manager is Shanghai Tianxun Jiuyi Private Equity Funds Management Co., Ltd. (上海天循久奕私募基金管理有限公司), which is a close associate 
of two existing shareholders (See the waiver and consent application submitted for allocation to existing shareholders or their close associates for 
details. Also see section headed “Allotment Results Details – International Offering – Allotees with Waivers/Consents Obtained” in this 
announcement); (ii) Liangke Dingan No.9 Private Equity Fund  (量客鼎安九号私募证券投资基金); (iii) Shanghai Daohe Equity Fund (道合承光
私募证券投资基金); (iv) Shenzhen Ruyuan Private Equity Fund Management Co., Ltd. (深圳如愿私募证券基金管理有限公司) ;  (v) 
Ruizeruoshui No.1 Private Equity Fund (锐泽若水1 号私募证券投资基金); (vi) Mingyi Haiying Private Equity Fund, Mingyi Yongtai Private 
Equity Fund (明毅海盈私募证券投资基金、明毅永泰私募证券投资基金).  
8. 
CITICS AM will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds (the Funds) on behalf of their respective 
investors. CITICS AM has confirmed that, to the best of their knowledge and after making all reasonable enquiries, no ultimate beneficial owner 
holds 30% or more interest in each of such Funds. 
CITICS AM has also confirmed that, to the best of their knowledge and after making all reasonable enquiries, each of the Funds above is an 
independent third party of CITICS AM, and the companies which are members of the same group of companies as CITICS AM and CLSA. 

<<<PAGE 44>>>
42 
 
9. 
China AMC HK will hold the Offer Shares in its capacity as the discretionary fund manager managing on behalf of its underlying clients, each of 
which is an independent third party (the China AM HK Ultimate Clients). China AMC HK is an investment advisor and a delegate of the investment 
manager of the China AM HK Ultimate Clients and manages assets (in its capacity as an investment advisor of China AM HK Ultimate Client) and 
executes trades (in its capacity as a delegate of the investment manager of China AM HK Ultimate Client) for and on behalf of China AM HK 
Ultimate Client. To the best of China AMC HK’s knowledge and after making all reasonable enquiries, the China AM HK Ultimate Client is an 
independent third party of the Company, its subsidiaries, and its substantial shareholders, China AMC HK, CLSA and the companies which are 
members of the same group of CLSA. 
10. 
The subscription will be made by China Universal (HK) in its capacity as the investment manager on a discretionary basis for and on behalf of its 
underlying clients. China Universal (HK) has confirmed that, to the best of their knowledge and after making all reasonable enquiries, each of its 
underlying clients and its UBO (if applicable) listed above is an independent third party of China Universal (HK), and the companies which are 
members of the same group of companies as Orient Securities. 
11. 
Orient AM will hold the Offer Shares on a discretionary basis on behalf of its underlying clients. To the best knowledge of Orient AM after due 
enquiry, there is no UBO holding 30% or more in each of its underlying clients, and each of the underlying clients of Orient AM is an independent 
third party of Orient AM and Orient Securities and the companies which are members of the same group of companies as Orient Securities.  
12. 
Guosen HK Brokerage is a sub-distributor in connection with the Global Offering. Guosen HK AM will participate as a placee and hold the Offer 
Shares in account in its capacity as the discretionary investment manager managing assets on behalf of its underlying client (the Guosen HK AM 
Client). Guosen HK AM is to invest on discretionary basis on behalf of the Guosen HK AM Client which is an independent third party and no 
proprietary money is used for the subscription. Guosen HK AM has confirmed that, to the best of their knowledge and after making all reasonable 
enquiries, each of the Guosen HK AM Client and its ultimate beneficial owner listed above is an independent third party of Guosen HK AM, and 
the companies which are members of the same group of companies as Guosen HK Brokerage. 
13. 
ICBC UBS and ICBC UBS (International) will hold the Offer Shares in its capacity as the discretionary fund manager on behalf of certain funds, 
who are independent third parties of the Company, its subsidiaries, its substantial shareholders, ICBC UBS, ICBC UBS (International), UBS AG 
and the companies which are members of the same group of UBS AG.  
14. 
UBS AM Singapore will hold the Offer Shares in its capacity as the discretionary fund manager on behalf of the following funds: (i) UBS (Lux) 
Equity Fund — Greater China (USD); (ii) UBS (Lux) Equity Fund — China Opportunity (USD); (iii) UBS (HK) Fund Series — China Opportunity 
Equity (USD); (iv) UBS (Lux) Equity SICAV — All China (USD); (v) UBS (Lux) Investment SICAV — China A Opportunity (USD); (vi) UBS 
(CAY) China A Opportunity; and (vii) certain other segregated accounts and mandates. There is no single ultimate beneficial owner holding 30% 
or more interests in such funds. 
UBS AM Singapore has confirmed that, to the best of its knowledge and after making all reasonable enquiries, each of the funds is an independent 
third party of UBS AM Singapore, UBS AG and the companies which are members of the same group of UBS AG. 

<<<PAGE 45>>>
43 
 
15. 
Haitong AM will hold the Offer Shares in its capacity as the discretionary fund manager of an independent third party, and no proprietary money is 
used for the subscription. Haitong AM has confirmed that, to the best of its knowledge and after making all reasonable enquiries, the ultimate client 
is an independent third party of Haitong AM, HTI and the companies which are members of the same group of HTI. 
16. 
Fullgoal Fund will hold the Offer Shares (on a discretionary basis) on behalf of its underlying clients. Each of the underlying clients is an independent 
third party of the Company, its subsidiaries, its substantial shareholders, and Fullgoal Fund. Fullgoal Fund has confirmed that, to the best of their 
knowledge, each of the underlying clients are independent third parties of Fullgoal Fund, HTI and the companies which are members of the same 
group of companies as HTI. 
17. 
China Southern, a qualified domestic institutional investor as approved by the relevant PRC authority to conduct asset management business, will 
hold the Offer Shares as the independent agent and discretionary manager of certain QDII funds. China Southern has confirmed that, to the best of 
their knowledge, each of such underlying clients are independent third parties of China Southern, HTFH and the companies which are members of 
the same group of companies as HTFH. 
 

<<<PAGE 46>>>
44 
 
DISCLAIMERS 
  
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong 
Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or into the 
United States (including its territories and possessions, any state of the United States and the District 
of Columbia). This announcement does not constitute or form a part of any offer or solicitation to 
purchase or subscribe for securities in the United States. The Offer Shares have not been and will not 
be registered under the United States Securities Act of 1933, as amended (the “U.S. Securities Act”) 
or any state securities laws in the United States and may not be offered, sold, pledged or transferred 
within the United States or to, or for the account or benefit of U.S. persons (as defined in Regulation 
S under the U.S. Securities Act), except in transactions exempt from, or not subject to, the registration 
requirements of the U.S. Securities Act. The Offer Shares are being offered and sold outside the United 
States in offshore transactions in reliance on Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to 
acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated December 22, 2025 issued by Shanghai Biren Technology 
Co., Ltd. for detailed information about the Global Offering described below before deciding whether 
or not to invest in the H Shares thereby being offered.  
*Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-OCs (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the 
occurrence of any of the events set out in the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on  the Listing Date (which is currently 
expected to be on January 2, 2026). 
 
 

<<<PAGE 47>>>
3
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering (after taking into account the full 
exercise of the Offer Size Adjustment Option and before any exercise of the Over-allotment 
Option), the total number of the H Shares held by the public represents approximately 48.33% of 
the total issued share capital of the Company, which is higher than the prescribed percentage of H 
Shares required to be held in public hands of 10.00% under Rule 8.08(1) (as amended and replaced 
by Rule 19A.13A(1)) of the Listing Rules calculated based on the final Offer Price of HK$19.60 
per H Share, thereby satisfying the public float requirement under Rule 8.08(1) (as amended and 
replaced by Rule 19A.13A(1)) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the Shares of the Company at the time of Listing. Based on the 
final Offer Price of HK$19.60 per H Share, the Company satisfies the free float requirement under 
Rule 19A.13C(1)(b) of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering (after 
taking into account the full exercise of the Offer Size Adjustment Option and before any exercise 
of the Over-allotment Option), (i) no placee will, individually, be placed more than 10% of the 
enlarged issued share capital of the Company immediately after the Global Offering; (ii) there 
will not be any new substantial Shareholder immediately after the Global Offering; (iii) the three 
largest public shareholders of the Company do not hold more than 50% of the shares in public 
hands at the time of the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; 
and (iv) there will be at least 300 Shareholders at the time of the Listing in compliance with Rule 
8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, January 2, 
2026 (Hong Kong time), provided that the Global Offering has become unconditional and the right 
of termination described in the section headed “Underwriting — Underwriting Arrangements and 
Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus has not 
been exercised. Investors who trade the Shares on the basis of publicly available allocation details 
prior to the receipt of Share certificates or prior to the Share certificates becoming valid evidence 
of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Friday, 
January 2, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Friday, January 2, 2026 (Hong Kong time). The H Shares 
will be traded in board lots of 200 Shares each, and the stock code of the H Shares will be 6082.
By order of the Board
Shanghai Biren Technology Co., Ltd.
上海壁仞科技股份有限公司
Mr. ZHANG WEN
Chairman of the Board, executive Director and Chief Executive Officer
Shanghai, December 31, 2025
As of the date of this announcement, the Board comprises: (i) Zhang Wen, Hong Zhou, Zhang 
Linglan, Xiao Bing and Pan Luting as executive Directors; (ii) Liu Jingguo as a non-executive 
Director; and (iii) Wang Yuan, Lam Siu Wing and Liu Jin as independent non-executive Directors.
