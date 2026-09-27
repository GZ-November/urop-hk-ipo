# 配发结果公告抽取任务：6938.HK Suzhou Ribo Life Science Co., Ltd. - B - H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**08/01/2026 22:43**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0108/2026010801352.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6938.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
announcement does not, and is not intended to, constitute or form a part of any offer or solicitation to purchase or 
subscribe for securities in the United States or in any other jurisdiction. The Offer Shares have not been and will not be 
registered under the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities Act”) or 
securities law of any state or other jurisdiction of the United States and may not be offered, sold, pledged or otherwise 
transferred within the United States, except in transactions exempt from, or not subject to, the registration requirements 
of the U.S. Securities Act and in compliance with any applicable state securities laws. There will be no public offer of 
the Offer Shares in the United States. The Offer Shares are being offered and sold solely (1) to qualified institutional 
buyers as defined in Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under the U.S. 
Securities Act; and (2) outside the United States in offshore transactions in reliance on Regulation S under the U.S. 
Securities Act and applicable laws of each jurisdiction where those offers and sales occur.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
December 31, 2025 (the “Prospectus”) issued by Suzhou Ribo Life Science Co., Ltd. (蘇州瑞博生物技術股份有限公
司) (the “Company”) for detailed information about the Global Offering described below before deciding whether or 
not to invest in the H Shares thereby being offered. The Company has not been and will not be registered under the U.S. 
Investment Company Act of 1940, as amended.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited 
as stabilizing manager (the “Stabilizing Manager”) (or its affiliates or any person acting for it) on behalf of the 
Underwriters, to the extent permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, 
may make purchases, over-allocate or effect transactions in the market or otherwise take such stabilizing action(s) with 
a view to stabilizing or supporting the market price of the H Shares at a level higher than that which might otherwise 
prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing Manager (or its 
affiliates or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will 
be conducted at the absolute discretion of the Stabilizing Manager (or its affiliates or any person acting for it) and in 
what the Stabilizing Manager reasonably regards as the best interest of the Company, (b) may be discontinued at any 
time and (c) is required to be brought to an end within 30 days after the last day for lodging applications under the 
Hong Kong Public Offering.
Potential investors should note that no stabilizing action can be taken to support the price of the H Shares for longer 
than the stabilization period, which will begin on the Listing Date and is expected to expire on Thursday, February 
5, 2026, being the 30th day after the last day for lodging applications under the Hong Kong Public Offering. After 
this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of the H 
Shares, could fall.
The obligations of the Hong Kong Underwriters under the Hong Kong Underwriting Agreement to subscribe for, and 
to procure subscribers for, the Hong Kong Offer Shares, are subject to termination by the Overall Coordinators (for 
themselves and on behalf of the Underwriters) if certain events shall occur prior to 8:00 a.m. on the Listing Date. Such 
grounds are set out in the section headed “Underwriting” in the Prospectus. It is important that you refer to that section 
for further details.

<<<PAGE 2>>>
2
Suzhou Ribo Life Science Co., Ltd.
蘇州瑞博生物技術股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
31,610,400 H Shares (taking into account 
 the full exercise of the Offer Size 
 Adjustment Option and subject to 
 the Over-allotment Option)
Number of Hong Kong Offer Shares
:
2,748,800 H Shares
Number of International Offer Shares
:
28,861,600 H Shares (taking into account 
 the full exercise of the Offer Size 
 Adjustment Option and subject to 
 the Over-allotment Option)
Offer Price
:
HK$57.97 per Offer Share, plus brokerage 
 of 1.0%, SFC transaction levy of 
 0.0027%, AFRC transaction levy 
 of 0.00015% and Hong Kong Stock 
 Exchange trading fee of 0.00565%
Nominal value
:
RMB1.00 per H Share
Stock code
:
6938
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, Joint Bookrunners, 
Joint Lead Managers
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners, Joint Lead Managers
Joint Global Coordinator, Joint Bookrunner, Joint Lead Manager
Joint Bookrunner, Joint Lead Manager

<<<PAGE 3>>>
3
SUZHOU RIBO LIFE SCIENCE CO., LTD.
蘇州瑞博生物技術股份有限公司 
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated December 31, 2025 (the “Prospectus”) issued 
by Suzhou Ribo Life Science Co., Ltd. (蘇州瑞博生物技術股份有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
6938
Stock short name
RIBOLIFE-B
Dealings commencement date
January 9, 2026*
* see note at the end of the announcement
Price Information
Fixed Offer Price
HK$57.97
Offer Shares and Share Capital
Number of Offer Shares
31,610,400 H Shares
Final Number of Offer Shares in Hong Kong Public 
 Offering
2,748,800 H Shares
Final Number of Offer Shares in International Offering 
 (taking into account the full exercise of the Offer Size 
 Adjustment Option and subject to the Over-allotment 
 Option)
28,861,600 H Shares
Number of issued shares upon Listing (before any exercise 
 of the Over-allotment Option)
165,813,510 Shares
The number of Offer Shares above is determined after taking into account the additional shares 
issued under the following Offer Size Adjustment Option.

<<<PAGE 4>>>
4
Offer Size Adjustment Option (Upsize option)
Number of additional shares issued under the option
4,123,000 H Shares
 – International Offering
4,123,000 H Shares
Over-allocation
No. of Offer Shares over-allocated
4,741,400 H Shares
 – International Offering
4,741,400 H Shares
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or a combination 
of these means. In the event the Over-allotment Option is exercised, an announcement will be 
made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$1,832.45 million
Less: Estimated listing expenses payable based on the 
 Offer Price
HK$130.65 million
Net proceeds
HK$1,701.80 million
Note: Gross proceeds refer to the amount to which the issuer is entitled to receive. For details of the use of 
proceeds, please refer to the Prospectus dated December 31, 2025.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
42,771
No. of successful applications
5,367
Subscription level
101.06 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the 
 Hong Kong Public Offering
2,748,800 H Shares
No. of Offer Shares reallocated from the International 
 Offering (claw-back)
0
Final no. of Offer Shares under the Hong Kong 
 Public Offering
2,748,800 H Shares
% of Offer Shares under the Hong Kong Public 
 Offering to the Global Offering
8.7%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can 
refer to https://www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
https://www.eipo.com.hk/eIPOAllotment for the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
177
Subscription Level
16.7 times
No. of Offer Shares initially available under the 
 International Offering
24,738,600 H Shares
No. of Offer Shares reallocated to the Hong Kong 
 Public Offering (claw-back)
0
Final no. of Offer Shares under the International 
 Offering (taking into account the full exercise of 
 the Offer Size Adjustment Option)
28,861,600 H Shares
% of Offer Shares under the International Offering 
 to the Global Offering
91.3%
The Directors confirm that, to the best of their knowledge, information and belief, save for a 
consent under paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) 
granted by the Stock Exchange to permit the Company to allocate certain Offer Shares in the 
International Offering to close associates of existing Shareholders of the Company, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, Supervisors, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates; and (ii) none of the placees and the public who have purchased the Offer Shares 
are accustomed to taking instructions from the Company, any of the Directors, chief executive 
of the Company, Supervisors, controlling Shareholders, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates in 
relation to the acquisition, disposal, voting or other disposition of Shares registered in his/her/its 
name or otherwise held by him/her/it.
Erik Selin Fastigheter Aktiebolag (“Erik Selin Fastigheter AB”) is a substantial shareholder 
of Ribocure AB, a subsidiary of the Company. Therefore, Erik Selin Fastigheter AB is a core 
connected person of the Company. The Company has applied for, and the Stock Exchange has 
granted, a waiver from strict compliance with Rule 9.09(b) of the Listing Rules to permit Erik 
Selin Fastigheter AB to participate as a cornerstone investor in the Global Offering. For details, 
please refer to the section headed “Waiver From Strict Compliance with the Listing Rules 
and Exemption From Strict Compliance with the Companies (Winding Up and Miscellaneous 
Provisions) Ordinance – Waiver From Strict Compliance with Rule 9.09(b) of the Listing Rules in 
relation to Cornerstone Subscription by a Core Connected Person” in the Prospectus.

<<<PAGE 6>>>
6
The placees in the International Offering include the following:
Cornerstone Investors
Investor(1)
Number 
of Offer 
Shares 
allocated
% of Offer 
Shares(2)
% of total 
issued H 
Shares 
after the 
Global 
Offering(2)
% of total 
issued 
share 
capital 
after the 
Global 
Offering(2)
Existing 
shareholders 
or their close 
associates
Arc Avenue Asset Management Pte. Ltd.
671,000
2.1%
0.4%
0.4%
No
Bright Stone Holdings Limited
536,800
1.7%
0.3%
0.3%
No
China Asset Management Co., Ltd.
2,013,200
6.4%
1.2%
1.2%
No
Da Cheng International Asset 
Management Company Limited and 
Dacheng Fund Management Company 
Limited
2,013,200
6.4%
1.2%
1.2%
No
Erik Selin Fastigheter Aktiebolag
1,342,000
4.2%
0.8%
0.8%
No(3)
Himension Fund
1,342,000
4.2%
0.8%
0.8%
No
IvyRock Asset Management (HK) 
Limited
536,800
1.7%
0.3%
0.3%
No
Mingxin Growth Ventures LS2 Limited
1,342,000
4.2%
0.8%
0.8%
No
Springs Capital (Hong Kong) Limited
1,342,000
4.2%
0.8%
0.8%
No
Taikang Life Insurance Co., Ltd.
1,610,400
5.1%
1.0%
1.0%
No
Tenbagger Capital Nengxin), LP. (上海拾
貝能信私募基金管理合夥企業(有限
合夥)), Tenbagger Capital (Shanghai, 
Ziran), LP. (上海自然拾貝投資管理合
夥企業(有限合夥)) and Huatai Capital 
Investment Limited
671,000
2.1%
0.4%
0.4%
No
Total
13,420,400
42.5%
8.1%
8.1%
Notes:
(1) 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in 
the Prospectus.
(2) 
Taking into account the full exercise of the Offer Size Adjustment Option and before any exercise of the 
Over-allotment Option.
(3) 
Erik Selin Fastigheter Aktiebolag (“Erik Selin Fastigheter AB”) is a substantial shareholder of Ribocure AB, 
a subsidiary of the Company. Therefore, Erik Selin Fastigheter AB is a core connected person of the Company. 
The Company has applied for, and the Stock Exchange has granted, a waiver from strict compliance with Rule 
9.09(b) of the Listing Rules to permit Erik Selin Fastigheter AB to participate as a cornerstone investor in the 
Global Offering. For details, please refer to the section headed “Waiver From Strict Compliance with the Listing 
Rules and Exemption From Strict Compliance with the Companies (Winding Up and Miscellaneous Provisions) 
Ordinance – Waiver From Strict Compliance with Rule 9.09(b) of the Listing Rules in relation to Cornerstone 
Subscription by a Core Connected Person” in the Prospectus.

<<<PAGE 7>>>
7
Allotees with Waivers/Consents Obtained
Investor
Number of 
Offer Shares 
allocated
% of Offer 
Shares(1)
% of total 
issued 
H Shares 
after 
the Global 
Offering(1)
% of total 
issued share 
capital after 
the Global 
Offering(1)
Relationship
Allotees with consent under paragraph 1C(2) of the Placing Guidelines in relation to subscription for Offer Shares by existing Shareholders 
and close associates of existing Shareholders (2)
William WONG (王興國)
402,600
1.27%
0.24%
0.24%
An existing Shareholder 
and a placee
Worldstar Global Holdings Limited
67,000
0.21%
0.04%
0.04%
An existing Shareholder 
and a placee
Blue Bay Healthcare Anchor Fund SPC
336,000
1.06%
0.20%
0.20%
A close associate of an 
existing Shareholder 
and a placee
Allotees with consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to connected clients (2)
CICC Financial Trading Limited (in 
connection with Zhonghe OTC 
Swaps) (3)
671,000
2.12%
0.40%
0.40%
Each is a connected client 
of China International 
Capital Corporation 
Hong Kong Securities 
Limited and a placee
CICC Financial Trading Limited (in 
connection with Yongjin OTC 
Swaps) (3)
40,000
0.13%
0.02%
0.02%
CICC Financial Trading Limited (in 
connection with Minghong OTC 
Swaps) (3)
13,400
0.04%
0.01%
0.01%
CICC Financial Trading Limited (in 
connection with Wangzheng OTC 
Swaps) (3)
1,200
0.00%
0.00%
0.00%
Notes:
(1) 
Taking into account the full exercise of the Offer Size Adjustment Option and before any exercise of the Over-
allotment Option.
(2) 
For details of (i) the consent under paragraph 1C(2) of the Placing Guidelines granted by the Stock Exchange to 
permit the Company to allocate certain Offer Shares in the International Offering to close associates of existing 
Shareholders, and (ii) the consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations 
to connected clients, please refer to the section headed “Waivers From Strict Compliance with the Listing 
Rules and exemption from Strict Compliance with the Companies (Winding Up and Miscellaneous Provisions) 
Ordinance” in the Prospectus and the section headed “Other Information” in this announcement.
(3) 
As defined in the section headed “Other Information – Placing to connected clients with prior consent under 
paragraph 1C(1) of the Placing Guidelines” in this announcement.

<<<PAGE 8>>>
8
Investor
Number of 
Offer Shares 
allocated
% of Offer 
Shares(1)
% of total 
issued 
H Shares 
after 
the Global 
Offering(1)
% of total 
issued share 
capital after 
the Global 
Offering(1)
Relationship
Guotai Junan Investments (Hong Kong) 
Limited
274,600
0.87%
0.17%
0.17%
A connected client 
of Guotai Junan 
Securities (Hong 
Kong) Limited 
and HAITONG 
INTERNATIONAL 
SECURITIES 
COMPANY 
LIMITED, and a 
placee
ABCI Asset Management Limited
5,800
0.02%
0.00%
0.00%
A connected client of 
ABCI Capital Limited 
and ABCI Securities 
Company Limited and 
a placee
ICBC UBS Asset Management Co., Ltd.
94,000
0.30%
0.06%
0.06%
Each is a connected client 
of ICBC International 
Securities Limited and 
a placee
Invesco Great Wall Fund Management 
Co., Ltd.
6,600
0.02%
0.00%
0.00%
Fullgoal Fund Management CO. LTD
100,600
0.32%
0.06%
0.06%
Each is a connected 
client of Guotai 
Junan Securities 
(Hong Kong) Limited 
and HAITONG 
INTERNATIONAL 
SECURITIES 
COMPANY 
LIMITED, and a 
placee
Fullgoal Asset management (HK) 
Limited
100,600
0.32%
0.06%
0.06%
HAITONG INTERNATIONAL ASSET 
MANAGEMENT (HK) LIMITED
6,600
0.02%
0.00%
0.00%

<<<PAGE 9>>>
9
LOCK-UP UNDERTAKINGS
Pre-IPO Investors (as defined in the “History and Corporate Structure” section of the 
Prospectus)
Name
Number of 
shares held in 
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
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing(1)
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing(1)
Last day subject 
to the lock-up 
undertakings(2)
Future Industry Investment Fund 
 (Limited Partnership)
 (先進製造產業投資基金(有限合夥))
11,430,002
11,430,002
6.89%
6.89%
January 8, 2027
Ningbo Panlin Qianyuan Equity Investment 
 Partnership (Limited Partnership)
 (寧波磐霖仟源股權投資合夥企業(有限合夥))
4,380,906
4,380,906
2.64%
2.64%
January 8, 2027
Hangzhou Panlin Xukang Venture Capital 
 Partnership (Limited Partnership)
 (杭州磐霖旭康創業投資合夥企業(有限合夥))
1,175,724
1,175,724
0.71%
0.71%
January 8, 2027
Jiaxing Panlin Guangci Venture Capital 
 Partnership (Limited Partnership) 
 (嘉興磐霖廣慈創業投資合夥企業(有限合夥))
1,004,334
1,004,334
0.61%
0.61%
January 8, 2027
Jiaxing Panlin Yuesheng Venture Capital 
 Partnership (Limited Partnership)
 (嘉興磐霖悅生創業投資合夥企業(有限合夥))
817,455
817,455
0.49%
0.49%
January 8, 2027
Shanghai Panlong Venture Capital Partnership 
 (Limited Partnership)
 (上海磐隴創業投資合夥企業(有限合夥))
817,455
817,455
0.49%
0.49%
January 8, 2027
Qingdao Panlin Hongyu Venture Capital 
 Partnership (Limited Partnership)
 (青島磐霖鴻裕創業投資企業(有限合夥))
782,695
782,695
0.47%
0.47%
January 8, 2027
Wise Vigour Limited
8,714,881
8,714,881
5.26%
5.26%
January 8, 2027
Kunshan Industrial Technology Research 
 Institute of Small Nucleic Acid Biotechnology 
 Research Institute Co. Ltd. 
 (昆山市工業技術研究院小核酸生物技術
 研究所有限責任公司)
3,224,973
3,224,973
1.94%
1.94%
January 8, 2027
Kunshan Hi-tech Venture Investment Co., Ltd.
 (昆山高新創業投資有限公司)
2,553,454
2,553,454
1.54%
1.54%
January 8, 2027

<<<PAGE 10>>>
10
Name
Number of 
shares held in 
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
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing(1)
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing(1)
Last day subject 
to the lock-up 
undertakings(2)
Kunshan Guoke Venture Capital Co., Ltd.
 (昆山市國科創業投資有限公司)
1,877,862
1,877,862
1.13%
1.13%
January 8, 2027
Kunshan Gongyan Venture Investment Co. Ltd.
 (昆山市工研創業投資有限公司)
816,246
816,246
0.49%
0.49%
January 8, 2027
Ionis Pharmaceuticals, Inc.
7,634,247
7,634,247
4.60%
4.60%
January 8, 2027
Shenzhen Yilong Venture Capital L.P.
 (深圳翼龍創業投資合夥企業(有限合夥))
6,297,338
6,297,338
3.80%
3.80%
January 8, 2027
Suzhou Jiyuan Yuanxing Equity Investment L.P.
 (蘇州紀源源星股權投資合夥企業(有限合夥))
5,239,889
5,239,889
3.16%
3.16%
January 8, 2027
Tianjin Haihe Asymchem Biopharmaceutical 
 Industry Innovation Investment L.P.
 (天津海河凱萊英生物醫藥產業創新投資基金
 (有限合夥))
1,949,716
1,949,716
1.18%
1.18%
January 8, 2027
Trinity Zhongzhi (Tianjin) Venture Capital 
 Center L.P.
 (三一眾志(天津)創業投資中心(有限合夥))
878,766
878,766
0.53%
0.53%
January 8, 2027
Trinity Zhongzhi II (Tianjin) Venture Capital 
 Center L.P.(三一眾志二期(天津)創業投資
 中心(有限合夥))
537,055
537,055
0.32%
0.32%
January 8, 2027
Trinity UCSF Limited
347,418
347,418
0.21%
0.21%
January 8, 2027
TIF Biomedical Fund II VCC
358,036
358,036
0.22%
0.22%
January 8, 2027
CICC Qide (Xiamen) Innovation Biomedical 
 Venture Capital Partnership (Limited 
 Partnership) (中金啟德(廈門)創新生物醫藥
 創業投資合夥企業(有限合夥))
2,091,741
2,091,741
1.26%
1.26%
January 8, 2027
Ningbo Meishan Bonded Port District Qirui 
 Equity Investment L.P.
 (寧波梅山保稅港區祺睿股權投資中心
 (有限合夥))
983,629
983,629
0.59%
0.59%
January 8, 2027
China Resources Venture Investment Co., Ltd.
 (華潤創業投資有限公司)
2,133,099
2,133,099
1.29%
1.29%
January 8, 2027

<<<PAGE 11>>>
11
Name
Number of 
shares held in 
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
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing(1)
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing(1)
Last day subject 
to the lock-up 
undertakings(2)
Shanghai Yangtze River Delta Industrial 
 Upgrading Equity Investment L.P.
 (上海長三角產業升級股權投資合夥企業
 (有限合夥))
1,969,908
1,969,908
1.19%
1.19%
January 8, 2027
Mr. LIU Guoping (劉國平)
1,899,525
1,899,525
1.15%
1.15%
January 8, 2027
Jiaxing Futong Investment L.P.
 (嘉興福通投資合夥企業(有限合夥))
1,881,880
1,881,880
1.13%
1.13%
January 8, 2027
Jinan Mingxin Industrial Investment Fund 
 Partnership (Limited Partnership)
 (濟南名信產業投資基金合夥企業(有限合夥))
1,864,127
1,864,127
1.12%
1.12%
January 8, 2027
Zhuhai Qiheng Equity Investment L.P.
 (珠海騏恒投資合夥企業(有限合夥))
1,852,159
1,852,159
1.12%
1.12%
January 8, 2027
Wenzhou Chouqin Borui Venture Investment L.P.
 (溫州酬勤博瑞創業投資合夥企業)
1,318,973
1,318,973
0.80%
0.80%
January 8, 2027
Tianjin Chouqin Tiancheng Venture 
 Investment L.P.
 (天津酬勤天成創業投資合夥企業)
338,302
338,302
0.20%
0.20%
January 8, 2027
Xizang Xingfan Enterprise Management Co., Ltd.
 (西藏星帆企業管理有限公司)
687,302
687,302
0.41%
0.41%
January 8, 2027
Wuxi Xingxi Venture Capital Partnership 
 (Limited Partnership)
 (無錫星錫創業投資合夥企業(有限合夥))
867,471
867,471
0.52%
0.52%
January 8, 2027
Jiaxing Co-way Yintian Venture Capital L.P.
 (嘉興眾匯銀田創業投資合夥企業(有限合夥))
1,045,869
1,045,869
0.63%
0.63%
January 8, 2027
Jiaxing Xiangtian Venture Capital L.P.
 (嘉興象田創業投資合夥企業(有限合夥))
367,026
367,026
0.22%
0.22%
January 8, 2027
Ningbo Daxie Yungong Jiajie Equity Investment 
 Partnership (Limited Partnership)
 (寧波大榭允公嘉傑股權投資合夥企業
 (有限合夥))
1,367,837
1,367,837
0.82%
0.82%
January 8, 2027

<<<PAGE 12>>>
12
Name
Number of 
shares held in 
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
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing(1)
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing(1)
Last day subject 
to the lock-up 
undertakings(2)
Shanghai Zhulu Enterprise Management 
 Consultation Center L.P.
 (上海築陸企業管理諮詢中心(有限合夥))
1,181,943
1,181,943
0.71%
0.71%
January 8, 2027
Zhuhai Qidi Rongchuang I Medical Industry 
 Investment L.P.(珠海啟迪融創一期醫療產業
 投資合夥企業(有限合夥))
1,026,853
1,026,853
0.62%
0.62%
January 8, 2027
Zhuhai Rongqian Equity Investment L.P. 
 (珠海融謙股權投資基金合夥企業(有限合夥))
138,764
138,764
0.08%
0.08%
January 8, 2027
Langma Twenty (Shenzhen) Venture Capital 
 Center L.P.(朗瑪二十號(深圳)
 創業投資中心(有限合夥))
197,573
197,573
0.12%
0.12%
January 8, 2027
Langma Thirty-Two (Shenzhen) Venture Capital 
 Center L.P.(朗瑪三十二號(深圳)
 創業投資中心(有限合夥))
136,075
136,075
0.08%
0.08%
January 8, 2027
Langma Ninety-Five (Shenzhen) Private Equity 
 Venture Investment Fund Partnership 
 (Limited Partnership)(朗瑪九十五號(深圳)
 私募創業投資基金合夥企業(有限合夥))
561,687
561,687
0.34%
0.34%
January 8, 2027
Langma Ninety-Six (Shenzhen) Private Equity 
 Venture Investment Fund Partnership 
 (Limited Partnership)(朗瑪九十六號(深圳)
 私募創業投資基金合夥企業(有限合夥))
240,723
240,723
0.15%
0.15%
January 8, 2027
Mr. William Wong (王興國)
895,091
895,091
0.54%
0.54%
January 8, 2027
Ningbo Boyuan Huizhi Enterprise Management 
 Partnership (Limited Partnership) 
 (寧波博遠匯智企業管理合夥企業(有限合夥))
848,299
848,299
0.51%
0.51%
January 8, 2027
Rixir Therapeutics, Limited
816,246
816,246
0.49%
0.49%
January 8, 2027
Zhuhai Hongtao Youxuan Equity Investment 
 Partnership (LP)(珠海弘陶優選股權投資
 合夥企業(有限合夥))
697,248
697,248
0.42%
0.42%
January 8, 2027
Shenzhen Hongtao Jiaxin Equity Investment L.P
 (深圳弘陶嘉信股權投資合夥企業(有限合夥))
90,716
90,716
0.05%
0.05%
January 8, 2027
Mr. Claes Robert Wahlestedt
712,500
712,500
0.43%
0.43%
January 8, 2027

<<<PAGE 13>>>
13
Name
Number of 
shares held in 
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
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing(1)
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing(1)
Last day subject 
to the lock-up 
undertakings(2)
Mr. Joseph Wade Collard
712,500
712,500
0.43%
0.43%
January 8, 2027
Xinsu Ronghe (Changezhou) Environment 
 Protection Investment Fund L.P.
 (新蘇融合(常州)環保投資基金(有限合夥))
613,092
613,092
0.37%
0.37%
January 8, 2027
Shenzhen Blue Ocean No. 1 Fund Management 
 Investment Center L.P.
 (深圳藍海壹號基金管理投資中心)
554,287
554,287
0.33%
0.33%
January 8, 2027
Kunshan Shuangyu Investment Enterprise L.P.
 (昆山雙禺投資企業(有限合夥))
541,674
541,674
0.33%
0.33%
January 8, 2027
Worldstar Global Holdings Limited
501,506
501,506
0.30%
0.30%
January 8, 2027
Shenzhen Xinchuang Medical Private Equity 
 Investment Fund Partnership (Limited 
 Partnership)(深圳欣創醫合私募股權投資基金
 合夥企業(有限合夥))
401,205
401,205
0.24%
0.24%
January 8, 2027
Shanghai Bluestone Investment Co., Ltd.
 (上海藍石投資有限公司)
389,151
389,151
0.23%
0.23%
January 8, 2027
Shanghai Chuang Yuan Yuan Investment 
 Management Co. Ltd.
 (上海創源垣投資管理有限公司)
382,268
382,268
0.23%
0.23%
January 8, 2027
Yantai Muxin Biopharmaceutical Health Industry 
 Development Partnership (Limited Partnership)
 (煙台牟信生物醫藥健康產業發展合夥企業
 (有限合夥))
300,904
300,904
0.18%
0.18%
January 8, 2027
Ms. CHEN Chi Nga (陳之雅)
268,527
268,527
0.16%
0.16%
January 8, 2027
Mr. LI Xiaofeng (李曉峰)
267,470
267,470
0.16%
0.16%
January 8, 2027
Mr. MI Zhongye (宓仲業)
80,241
80,241
0.05%
0.05%
January 8, 2027
Subtotal
94,063,843
94,063,843
56.73%
56.73%
Notes:
(1) 
Taking into account the full exercise of the Offer Size Adjustment Option and before any exercise of the Over-
allotment Option.
(2) 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law.

<<<PAGE 14>>>
14
Existing Shareholders (other than the Pre-IPO Investors as defined in the “History and 
Corporate Structure” section of the Prospectus)
Name
Number 
of shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon 
Listing(1)
% of 
shareholding 
in the 
Company 
subject to
lock-up 
undertakings 
upon 
Listing(1)
Last day 
subject to 
the lock-up 
undertakings(2)
Dr. LIANG Zicai (梁子才)
14,546,306
14,546,306
8.77%
8.77%
January 8, 2027
Kunshan Ruikong Enterprise Management 
 Consulting L.P.
 (昆山瑞控企業管理諮詢合夥企業(有限合夥))
10,842,204
10,842,204
6.54%
6.54%
January 8, 2027
Kunshan Ruiman Enterprise Management 
 Consulting L.P.
 (昆山瑞曼企業管理諮詢合夥企業(有限合夥))
5,539,551
5,539,551
3.34%
3.34%
January 8, 2027
Ms. MO Hua (莫華)
3,037,458
3,037,458
1.83%
1.83%
January 8, 2027
Prof. XI Zhen (席真)
2,847,150
2,847,150
1.72%
1.72%
January 8, 2027
Prof. ZHANG Lihe (張禮和)
1,898,100
1,898,100
1.14%
1.14%
January 8, 2027
Kunshan Ruiji Enterprise Management 
 Consulting L.P.
 (昆山瑞技企業管理諮詢合夥企業(有限合夥))
1,428,498
1,428,498
0.86%
0.86%
January 8, 2027
Subtotal
40,139,267
40,139,267
24.21%
24.21%
Notes:
(1) 
Taking into account the full exercise of the Offer Size Adjustment Option and before any exercise of the Over-
allotment Option.
(2) 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law.

<<<PAGE 15>>>
15
Cornerstone Investors
Name
Number 
of shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon 
Listing(1)
% of 
shareholding 
in the 
Company 
subject to
lock-up 
undertakings 
upon 
Listing(1)
Last day 
subject to 
the lock-up 
undertakings(2)
Arc Avenue Asset Management Pte. Ltd.
671,000
671,000
0.40%
0.40%
July 8, 2026
Bright Stone Holdings Limited
536,800
536,800
0.32%
0.32%
July 8, 2026
China Asset Management Co., Ltd.
2,013,200
2,013,200
1.21%
1.21%
July 8, 2026
Da Cheng International Asset Management 
 Company Limited and Dacheng Fund 
 Management Company Limited
2,013,200
2,013,200
1.21%
1.21%
July 8, 2026
Erik Selin Fastigheter Aktiebolag
1,342,000
1,342,000
0.81%
0.81%
July 8, 2026
Himension Fund
1,342,000
1,342,000
0.81%
0.81%
July 8, 2026
IvyRock Asset Management (HK) Limited
536,800
536,800
0.32%
0.32%
July 8, 2026
Mingxin Growth Ventures LS2 Limited
1,342,000
1,342,000
0.81%
0.81%
July 8, 2026
Springs Capital (Hong Kong) Limited
1,342,000
1,342,000
0.81%
0.81%
July 8, 2026
Taikang Life Insurance Co., Ltd.
1,610,400
1,610,400
0.97%
0.97%
July 8, 2026
Tenbagger Capital Nengxin), LP. 
 (上海拾貝能信私募基金管理合夥企業
 (有限合夥)), Tenbagger Capital 
 (Shanghai, Ziran), LP. (上海自然拾貝
 投資管理合夥企業(有限合夥)) 
 and Huatai Capital Investment Limited
671,000
671,000
0.40%
0.40%
July 8, 2026
Subtotal
13,420,400
13,420,400
8.09%
8.09%
Notes:
(1) 
Taking into account the full exercise of the Offer Size Adjustment Option and before any exercise of the Over-
allotment Option.
(2) 
Each Cornerstone Investor shall not dispose of any of the Offer Shares acquired in the Global Offering at 
any time during the period of six months following the Listing Date pursuant to their respective Cornerstone 
Investment Agreement, save for certain limited circumstances, such as transfers to any of its wholly-owned 
subsidiaries who will be bound by the same obligations of the relevant Cornerstone Investor, including the lock-
up period restriction. For details, please refer to the section headed “Cornerstone Investors – Restrictions on the 
Cornerstone Investors” of the Prospectus.

<<<PAGE 16>>>
16
PLACEE CONCENTRATION ANALYSIS
Placees
Number of 
H Shares 
Allocated
Allotment 
as % of 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
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
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued)
Number of 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued)
Top 1
2,013,200
6.98%
5.99%
6.37%
5.54%
2,013,200
1.21%
1.18%
Top 5
7,958,000
27.57%
23.68%
25.18%
21.89%
7,958,000
4.80%
4.67%
Top 10
14,507,200
50.26%
43.17%
45.89%
39.91%
14,507,200
8.75%
8.51%
Top 25
23,153,200
80.22%
68.90%
73.25%
63.69%
23,153,200
13.96%
13.58%
Notes
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
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
exercised 
and new H 
Shares are 
issued)
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
as % of 
total Offer 
Shares 
(assuming 
the Over-
allotment 
Option is 
exercised 
and new H 
Shares are 
issued)
Number of 
H Shares 
held upon 
Listing
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
assuming 
the Over-
allotment 
Option is 
exercised 
and new H 
Shares are 
issued)
Number of 
Shares held 
upon Listing
Top 1
0
0.00%
0.00%
0.00%
0.00%
40,139,267
24.21%
23.53%
40,139,267
Top 5
0
0.00%
0.00%
0.00%
0.00%
79,215,817
47.77%
46.45%
79,215,817
Top 10
0
0.00%
0.00%
0.00%
0.00%
105,533,652
63.65%
61.88%
105,533,652
Top 25
9,662,800
28.83%
24.76%
30.57%
26.58%
131,235,157
79.15%
76.95%
131,235,157
Notes
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 17>>>
17
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
exercised 
and new 
H Shares 
are issued)
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
as % of 
total Offer 
Shares 
(assuming 
the Over-
allotment 
Option is 
exercised 
and new 
H Shares 
are issued)
Number of 
H Shares 
held upon 
Listing
Number of 
Share held 
upon 
Listing
% of total 
issued share 
capital upon 
Listing 
(assuming 
no exercise 
of the 
Over-
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
exercised 
and new 
H Shares 
are issued)
Top 1
0
0.00%
0.00%
0.00%
0.00%
40,139,267
40,139,267
24.21%
23.53%
Top 5
0
0.00%
0.00%
0.00%
0.00%
79,215,817
79,215,817
47.77%
46.45%
Top 10
0
0.00%
0.00%
0.00%
0.00%
105,533,652
105,533,652
63.65%
61.88%
Top 25
9,662,800
28.83%
24.76%
30.57%
26.58%
131,235,157
131,235,157
79.15%
76.95%
Notes
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 18>>>
18
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 42,771 valid 
applications made by the public will be conditionally allocated on the basis set out below:
NO. OF 
SHARES 
APPLIED FOR
NO. OF 
VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
 PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES
 APPLIED FOR
POOL A
200
26,796
457 out of 26,796 to receive 200 Shares
1.71%
400
2,121
72 out of 2,121 to receive 200 Shares
1.70%
600
1,068
54 out of 1,068 to receive 200 Shares
1.69%
800
3,408
227 out of 3,408 to receive 200 Shares
1.67%
1,000
749
62 out of 749 to receive 200 Shares
1.66%
1,200
211
21 out of 211 to receive 200 Shares
1.66%
1,400
175
20 out of 175 to receive 200 Shares
1.63%
1,600
434
56 out of 434 to receive 200 Shares
1.61%
1,800
344
50 out of 344 to receive 200 Shares
1.61%
2,000
1,897
304 out of 1,897 to receive 200 Shares
1.60%
3,000
586
141 out of 586 to receive 200 Shares
1.60%
4,000
481
154 out of 481 to receive 200 Shares
1.60%

<<<PAGE 19>>>
19
NO. OF 
SHARES 
APPLIED FOR
NO. OF 
VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
 PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES
 APPLIED FOR
POOL A
5,000
319
127 out of 319 to receive 200 Shares
1.59%
6,000
304
145 out of 304 to receive 200 Shares
1.59%
7,000
180
100 out of 180 to receive 200 Shares
1.59%
8,000
212
135 out of 212 to receive 200 Shares
1.59%
9,000
142
101 out of 142 to receive 200 Shares
1.58%
10,000
978
775 out of 978 to receive 200 Shares
1.58%
20,000
680
200 Shares plus 397 out of 680 to receive 
additional 200 Shares
1.58%
30,000
234
400 Shares plus 88 out of 234 to receive 
additional 200 Shares
1.58%
40,000
156
600 Shares plus 21 out of 156 to receive 
additional 200 Shares
1.57%
50,000
120
600 Shares plus 110 out of 120 to receive 
additional 200 Shares
1.57%
60,000
93
800 Shares plus 65 out of 93 to receive 
additional 200 Shares
1.57%
70,000
53
1,000 Shares plus 26 out of 53 to receive 
additional 200 Shares
1.57%
80,000
88
1,200 Shares plus 23 out of 88 to receive 
additional 200 Shares
1.57%
41,829
Total number of Pool A successful 
applicants: 4,425
POOL B
90,000
466
600 Shares plus 106 out of 466 to receive 
additional 200 Shares
0.72%
100,000
151
600 Shares plus 89 out of 151 to receive 
additional 200 Shares
0.72%
150,000
87
1,000 Shares plus 33 out of 87 to receive 
additional 200 Shares
0.72%
200,000
73
1,400 Shares plus 13 out of 73 to receive 
additional 200 Shares
0.72%
250,000
34
1,600 Shares plus 33 out of 34 to receive 
additional 200 Shares
0.72%
300,000
18
2,000 Shares plus 14 out of 18 to receive 
additional 200 Shares
0.72%

<<<PAGE 20>>>
20
NO. OF 
SHARES 
APPLIED FOR
NO. OF 
VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
 PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES
 APPLIED FOR
POOL B
350,000
11
2,400 Shares plus 6 out of 11 to receive 
additional 200 Shares
0.72%
400,000
21
2,800 Shares plus 7 out of 21 to receive 
additional 200 Shares
0.72%
500,000
13
3,400 Shares plus 12 out of 13 to receive 
additional 200 Shares
0.72%
600,000
6
4,200 Shares plus 3 out of 6 to receive 
additional 200 Shares
0.72%
700,000
9
5,000 Shares plus 1 out of 9 to receive 
additional 200 Shares
0.72%
800,000
6
5,600 Shares plus 4 out of 6 to receive 
additional 200 Shares
0.72%
900,000
2
6,400 Shares plus 1 out of 2 to receive 
additional 200 Shares
0.72%
1,000,000
11
7,000 Shares plus 10 out of 11 to receive 
additional 200 Shares
0.72%
1,374,400
34
9,800 Shares plus 10 out of 34 to receive 
additional 200 Shares
0.72%
942
Total number of Pool B successful 
applicants: 942
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or 
indirectly, provided by the Company, its controlling shareholder(s), directors or syndicate members 
to any placees or the public (as the case may be) and the consideration payable by them for each 
Offer Share of the Company subscribed for or purchased by them is the same as the Offer Price 
determined by the Company, in addition to any brokerage, AFRC transaction levy, SFC transaction 
levy and trading fee payable.

<<<PAGE 21>>>
21
OTHER INFORMATION
Offer Size Adjustment Option
The Offer Size Adjustment Option has been fully exercised by the Overall Coordinators, pursuant 
to which the Company is issuing and allotting 4,123,000 additional Offer Shares, representing 
approximately 15% of the total number of Offer Shares initially available under the Global 
Offering, at the Offer Price. All of the additional Offer Shares that would be allotted and issued by 
the Company pursuant to the full exercise of the Offer Size Adjustment Option will be allocated 
to the International Offering. Accordingly, the total number of Offer Shares finally available under 
the Global Offering (taking into account the full exercise of the Offer Size Adjustment Option 
and before any exercise of the Over-allotment Option) that would be allotted and issued by the 
Company is 31,610,400 Offer Shares and the total issued share capital of the Company upon 
Listing (taking into account the full exercise of the Offer Size Adjustment Option and before any 
exercise of the Over-allotment Option) will be 165,813,510 Shares.
As a result of the above, the final number of Offer Shares under the International Offering is 
adjusted to 28,861,600 Shares, representing approximately 91.3% of the total number of Offer 
Shares under the Global Offering (assuming the Over-allotment Option is not exercised).
Placing to existing Shareholders and/or their close associates with prior consent under 
paragraph 1C(2) of the Placing Guidelines
Mr. Wong and Worldstar Global (collectively, the “Existing Shareholders as Placees”), and 
Blue Bay (the “Close Associate of Existing Shareholders as Placee”)
The Company has applied to the Stock Exchange, and the Stock Exchange has granted a consent 
under paragraph 1C(2) of the Placing Guidelines to permit the Company to allocate such Offer 
Shares in the International Offering to the Existing Shareholders as Placees and the Close 
Associate of Existing Shareholders as Placee set out below:
(1) 
Mr. William WONG (王興國) (“Mr. Wong”), an existing Shareholder of the Company.
(2) 
Worldstar Global Holdings Limited (“Worldstar Global”), an existing Shareholder of the 
Company.
(3) 
Blue Bay Healthcare Anchor Fund SPC (“Blue Bay”) is a close associate of Shenzhen Blue 
Ocean No. 1 Fund Management Investment Center L.P. (深圳藍海壹號基金管理投資中心(有
限合夥)) (“Blue Ocean Investment”), an existing Shareholder of the Company.
The allocation of Offer Shares to the Existing Shareholders as Placees and the Close Associate of 
Existing Shareholders as Placee is in compliance with all the conditions under the consent granted 
by the Stock Exchange, including but not limited to (i) the Company complies with Rules 19A.13A 
and 19A.13C of the Listing Rules, and (ii) no preference in allocation was given to the Existing 
Shareholders as Placees and the Close Associate of Existing Shareholders as Placee.
For details of the allocations of Offer Shares to close associates of existing Shareholders, please 
refer to the section headed “Allotment Results Details – International Offering – Allotees with 
Waivers/Consents Obtained” in this announcement.

<<<PAGE 22>>>
22
Placing to connected clients with prior consent under paragraph 1C(1) of the Placing 
Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted a 
consent under paragraph 1C(1) of the Placing Guidelines to permit Tenbagger Nengxin, Tenbagger 
Ziran and Huatai Capital Investment Limited (in connection with Huatai OTC Swaps) to participate 
in the Global Offering as a cornerstone investor.
In addition, the Company has applied to the Stock Exchange, and the Stock Exchange has granted, 
a consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate 
certain Offer Shares in the International Offering to connected clients as placees. The allocation of 
Offer Shares to such connected clients is in compliance with all the conditions under the consent 
granted by the Stock Exchange.

<<<PAGE 23>>>
23
Details of the placement to the connected clients above are set out below.
No.
Name of connected 
client
Name of connected 
distributor
Relationship with the 
connected distributor
Basis of 
holding 
securities
Number 
of Offer 
Shares 
subscribed
Ultimate 
beneficial 
owner of 
the Offer 
Shares 
allocated 
to the 
connected 
client
Percentage 
of the 
Offer 
Shares 
subscribed 
(assuming 
the Over-
allotment 
Option 
is not 
exercised 
and taking 
into 
account 
full 
exercise 
of the 
offer size 
adjustment 
option)
Percentage 
of the 
issued 
Shares 
of the 
Company 
immediately 
upon 
completion 
of the 
Global 
Offering 
(assuming 
the Over-
allotment 
Option 
is not 
exercised 
and taking 
into account 
full exercise 
of the 
offer size 
adjustment 
option)
1.
CICC Financial 
Trading Limited 
(“CICC FT”)
See Note 1 for further 
information of the 
ultimate clients of 
CICC FT.
China International 
Capital Corporation 
Hong Kong Securities 
Limited (“CICC”)
CICC FT is a member 
of the same group as 
CICC.
Non-
discretionary 
basis
725,600
See Note 1
2.30%
0.44%

<<<PAGE 24>>>
24
No.
Name of connected 
client
Name of connected 
distributor
Relationship with the 
connected distributor
Basis of 
holding 
securities
Number 
of Offer 
Shares 
subscribed
Ultimate 
beneficial 
owner of 
the Offer 
Shares 
allocated 
to the 
connected 
client
Percentage 
of the 
Offer 
Shares 
subscribed 
(assuming 
the Over-
allotment 
Option 
is not 
exercised 
and taking 
into 
account 
full 
exercise 
of the 
offer size 
adjustment 
option)
Percentage 
of the 
issued 
Shares 
of the 
Company 
immediately 
upon 
completion 
of the 
Global 
Offering 
(assuming 
the Over-
allotment 
Option 
is not 
exercised 
and taking 
into account 
full exercise 
of the 
offer size 
adjustment 
option)
2.
Guotai Junan 
Investments (Hong 
Kong) Limited 
(“GTJAI”)
* Fullgoal Fund, 
Fullgoal HK and 
Haitong IAM (each 
as defined below); 
for their allocation 
information, see 
No. 6, No. 7 and 
No. 8 in this table.
See Note 2 for further 
information of the 
ultimate clients of 
GTJAI.
Guotai Junan Securities 
(Hong Kong) Limited 
(“GTJAS”)
GTJAI, together with 
Fullgoal Fund and 
Fullgoal HK, are 
members of the same 
group as GTJAS and 
Haitong International 
(as defined below).
Non-
discretionary 
basis
274,600
See Note 2 
 and 
 Note 5
0.87%
0.17%
3.
ABCI Asset 
Management 
Limited (“ABCI 
AM”)
ABCI Capital Limited 
and ABCI Securities 
Company Limited 
(“ABCI”)
ABCI AM is a member 
of the same group as 
ABCI.
Discretionary 
basis
5,800
See Note 4
0.00%
0.00%

<<<PAGE 25>>>
25
No.
Name of connected 
client
Name of connected 
distributor
Relationship with the 
connected distributor
Basis of 
holding 
securities
Number 
of Offer 
Shares 
subscribed
Ultimate 
beneficial 
owner of 
the Offer 
Shares 
allocated 
to the 
connected 
client
Percentage 
of the 
Offer 
Shares 
subscribed 
(assuming 
the Over-
allotment 
Option 
is not 
exercised 
and taking 
into 
account 
full 
exercise 
of the 
offer size 
adjustment 
option)
Percentage 
of the 
issued 
Shares 
of the 
Company 
immediately 
upon 
completion 
of the 
Global 
Offering 
(assuming 
the Over-
allotment 
Option 
is not 
exercised 
and taking 
into account 
full exercise 
of the 
offer size 
adjustment 
option)
4.
ICBC UBS Asset 
Management 
Co., Ltd. (“ICBC 
UBS”)
ICBC International 
Securities Limited 
(“ICBCI”)
ICBC UBS and Invesco 
are members of 
the same group as 
ICBCI.
Discretionary 
basis
94,000
See Note 4
0.30%
0.06%
5.
Invesco Great Wall 
Fund Management 
Co., Ltd. 
(“Invesco”)
Discretionary 
basis
6,600
0.02%
0.00%
6.
Fullgoal Fund 
Management CO. 
LTD (“Fullgoal 
Fund”)
HAITONG 
INTERNATIONAL 
SECURITIES 
COMPANY 
LIMITED (“Haitong 
International”)
Fullgoal Fund, Fullgoal 
HK and Haitong 
IAM, together with 
GTJAI, are members 
of the same group as 
GTJAS and Haitong 
International.
Discretionary 
basis
100,600
See Note 2 
 and 
 Note 5
0.32%
0.06%
7.
Fullgoal Asset 
management (HK) 
Limited (“Fullgoal 
HK”)
Discretionary 
basis
100,600
0.32%
0.06%

<<<PAGE 26>>>
26
No.
Name of connected 
client
Name of connected 
distributor
Relationship with the 
connected distributor
Basis of 
holding 
securities
Number 
of Offer 
Shares 
subscribed
Ultimate 
beneficial 
owner of 
the Offer 
Shares 
allocated 
to the 
connected 
client
Percentage 
of the 
Offer 
Shares 
subscribed 
(assuming 
the Over-
allotment 
Option 
is not 
exercised 
and taking 
into 
account 
full 
exercise 
of the 
offer size 
adjustment 
option)
Percentage 
of the 
issued 
Shares 
of the 
Company 
immediately 
upon 
completion 
of the 
Global 
Offering 
(assuming 
the Over-
allotment 
Option 
is not 
exercised 
and taking 
into account 
full exercise 
of the 
offer size 
adjustment 
option)
8.
HAITONG 
INTERNATIONAL 
ASSET 
MANAGEMENT 
(HK) LIMITED 
(“Haitong IAM”)
* GTJAI; for 
its allocation 
information, see 
No. 2 in this table.
Discretionary 
basis
6,600
0.02%
0.00%
Notes:
1. 
CICC FT and China International Capital Corporation Limited (“CICCL”) will enter into a series of cross 
border delta-one OTC swap transactions (collectively, the “Zhonghe OTC Swaps”) with each other and the 
ultimate clients (the “CICC FT Ultimate Clients (Zhonghe)”), pursuant to which CICC FT will hold the Offer 
Shares on a non-discretionary basis to hedge the Zhonghe OTC Swaps while the economic risks and returns of 
the underlying Offer Shares are passed to the CICC FT Ultimate Clients (Zhonghe), subject to customary fees 
and commissions. The Zhonghe OTC Swaps will be fully funded by the CICC FT Ultimate Clients (Zhonghe). 
To the best of CICC FT’s knowledge having made all reasonable inquiries, each of the CICC FT Ultimate 
Clients (Zhonghe) is an independent third party of CICC FT, CICC and the companies which are members of 
the same group of CICC, and the ultimate beneficial owner holding 30% or more interests in the of the CICC 
FT Ultimate Clients (Zhonghe) is Zhang Jingting (張敬庭).

<<<PAGE 27>>>
27
CICC FT and CICCL will enter into a series of cross border delta-one OTC swap transactions (collectively, the 
“Yongjin OTC Swaps”) with each other and the ultimate clients (the “CICC FT Ultimate Client (Yongjin)”), 
pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the Yongjin OTC 
Swaps while the economic risks and returns of the underlying Offer Shares are passed to the CICC FT Ultimate 
Client (Yongjin), subject to customary fees and commissions. The Yongjin OTC Swaps will be fully funded 
by the CICC FT Ultimate Client (Yongjin). To the best of CICC FT’s knowledge having made all reasonable 
inquiries, the CICC FT Ultimate Client (Yongjin) is an independent third party of CICC FT, CICC and the 
companies which are members of the same group of CICC, and the ultimate beneficial owners holding 30% 
or more interests in each of the of the CICC FT Ultimate Clients (Yongjin) are Wu Jialin (吳家麒) and Xie 
Xiaoyong (謝小勇), respectively.
CICC FT and CICCL will enter into a series of cross border delta-one OTC swap transactions (collectively, 
the “Minghong OTC Swaps”) with each other and the ultimate clients (the “CICC FT Ultimate Client 
(Minghong)”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the 
Minghong OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed to the 
CICC FT Ultimate Client (Minghong), subject to customary fees and commissions. The Minghong OTC Swaps 
will be fully funded by the CICC FT Ultimate Client (Minghong). To the best of CICC FT’s knowledge having 
made all reasonable inquiries, the CICC FT Ultimate Client (Minghong) is an independent third party of CICC 
FT, CICC and the companies which are members of the same group of CICC, and no single ultimate beneficial 
owner holds 30% or more interest in each of the CICC FT Ultimate Client (Minghong).
CICC FT and CICCL will enter into a series of cross border delta-one OTC swap transactions (collectively, 
the “Wangzheng OTC Swaps”) with each other and the ultimate clients (the “CICC FT Ultimate Client 
(Wangzheng)”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge 
the Wangzheng OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed to 
the CICC FT Ultimate Client (Wangzheng), subject to customary fees and commissions. The Wangzheng OTC 
Swaps will be fully funded by the CICC FT Ultimate Client (Wangzheng). To the best of CICC FT’s knowledge 
having made all reasonable inquiries, the CICC FT Ultimate Client (Wangzheng) is an independent third 
party of CICC FT, CICC and the companies which are members of the same group of CICC, and the ultimate 
beneficial owner holding 30% or more interests in the of the CICC FT Ultimate Clients (Wangzheng) is Zhai 
Qin (瞿琴).
2. 
It is proposed that Guotai Junan Investments (Hong Kong) Limited (“GTJAI”) participates as placee to 
subscribe for the Offer Shares under the International Offering (the “GTJAI Subscription”). GTJAI is a 
member of the same group of companies as Guotai Junan Securities (Hong Kong) Limited (“GTJAS”) and is 
considered as a connected client of GTJAS pursuant to paragraph 1B(7) of the Placing Guidelines.
In relation to the GTJAI Subscription, GTJAI shall hold the Offer Shares for hedging purpose as the single 
underlying asset of several sets of back-to-back total return swap transaction (the “GTHT Back-to-back TRS”) 
to be entered into between GTJAI and Guotai Haitong Securities Co., Ltd. (the “GTHT Onshore Parent”) 
in connection with several total return swap orders (the “GTHT Client TRS”) to be entered into by GTHT 
Onshore Parent and several ultimate clients (the “GTHT Onshore Ultimate Client”), respectively. Such GTHT 
Client TRS is to be fully funded by the GTHT Onshore Ultimate Client. GTJAI will hold the Offer Shares on 
a non-discretionary basis for the purpose of hedging the economic exposure under the GTHT Back-to-back 
TRS and GTHT Client TRS only, During the tenor of the GTHT Client TRS, all economic returns of the Offer 
Shares will be passed to the GTHT Onshore Ultimate Clients and all economic losses shall be borne by the 
GTHT Onshore Ultimate Client, subject to the terms and conditions of the GTHT Back-to-back TRS and GTHT 
Client TRS, and GTJAI will not take part in any economic return or bear any economic loss in relation to the 
price of the Offer Shares. The GTHT Onshore Ultimate Client may request to redeem the Offer Shares at their 
own discretion, upon which GTJAI shall dispose of the Offer Shares and settle the GTHT Back-to-back TRS 
and GTHT Client TRS in cash in accordance with the terms and conditions of the GTHT Back-to-back TRS and 
GTHT Client TRS documents. Due to its internal policy, GTJAI will not exercise the voting right attaching to 
the Offer Shares during the tenor of the GTHT Back-to-back TRS and GTHT Client TRS.

<<<PAGE 28>>>
28
To the best knowledge, information and belief of GTJAI after due enquiry, the GTHT Onshore Ultimate Clients 
and their respective ultimate beneficial owners holding 30% or more interest include:
(i) 
Huang Shilin (黃世霖);
(ii) 
Wang Jing (王靜);
(iii) 
Sun Yuan (孫遠);
(iv) 
Chuxin Li (李出新);
(v) 
Yukai Shao (邵宇開);
(vi) 
Wu Jiaqi (吳家麒);
(vii) Xie Xiaoyong (謝小勇);
(viii) Zeng Xiaojie (曾曉潔);
(ix) 
ZHUANG TAO (莊濤);
(x) 
CHEN QIN;
(xi) 
CUI TONGKUI (崔同魁);
(xii) XIAO MING (肖明); and
(xiii) Guo Kai (郭鑥).
To the best knowledge of GTJAI after making all reasonable enquiries, (i) GTJAI has confirmed that, to the best 
of its knowledge, each of the GTHT Onshore Ultimate Clients and the ultimate beneficial owners holding 30% 
or more interest of the GTHT Onshore Ultimate Clients listed above is an independent third party of GTJAI, 
GTJAS and the companies which are members of the same group of companies as GTJAS, and (ii) GTJAI is not 
a collective investment scheme which is not authorised by the SFC nor is expected to hold the Offer Shares on 
behalf of such scheme.
3. 
ABCI AM intends to hold the Offer Shares in its capacity as manager managing investment portfolios on behalf 
of underlying investors who are independent third parties on a discretionary basis.
4. 
ICBC UBS intends to hold the Offer Shares in its capacity as manager managing investment portfolios on behalf 
of underlying investors who are independent third parties on a discretionary basis.
Invesco intends to hold the Offer Shares in its capacity as manager managing investment portfolios on behalf of 
underlying investors who are independent third parties on a discretionary basis.
5. 
Fullgoal Fund intends to hold the Offer Shares in its capacity as manager managing investment portfolios on 
behalf of underlying investors who are independent third parties on a discretionary basis.
Fullgoal HK intends to hold the Offer Shares in its capacity as manager managing investment portfolios on 
behalf of underlying investors who are independent third parties on a discretionary basis.
Haitong IAM intends to hold the Offer Shares in its capacity as manager managing investment portfolios on 
behalf of underlying investors who are independent third parties on a discretionary basis.

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
Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated December 31, 2025 issued by Suzhou Ribo 
Life Science Co., Ltd. for detailed information about the Global Offering described below before 
deciding whether or not to invest in the H Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the paragraph headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering –  Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing 
Date (which is currently expected to be on January 9, 2026).
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering, 110,900,415 H Shares, representing 
approximately 66.88% of the issued share capital of our Company (before any exercise of the 
Over-allotment Option) will count towards the public float. Therefore, the number of H shares held 
in public hands is higher than the prescribed percentage of H Shares required to be held in public 
hands under Rule 19A.13A(1) of the Listing Rules, satisfying the minimum percentage requirement 
in compliance with Rule 19A.13A(1) of the Listing Rules, representing 15.61% of H Shares to be 
held in public hands with the expected market value of HK$1.5 billion at the time of Listing, based 
on the Offer Price of HK$57.97 per H Share.

<<<PAGE 30>>>
30
All the existing shareholders of the Company are subject to a lock-up period of 12 months 
following the Listing Date pursuant to the applicable PRC laws and all the cornerstone investors 
are subject to a lock-up period of six months following the Listing Date. The Offer Shares to be 
subscribed by all the other investors participating in the Global Offering are not subject to any 
disposal restriction. Excluding the Offer Shares to be allocated to the cornerstone investors that 
are subject to a lock-up period of six months following the Listing Date, the Company’s H Shares 
to be counted towards the free float upon Listing will be 18,190,000 Shares. Based on the Offer 
Price of HK$57.97 per H Share, the Company will satisfy the free float requirement under Rule 
19A.13C(1)(b) of the Listing Rules
The Directors confirm that, immediately following completion of the Global Offering: (i) the 
Shares will be held by at least 300 Shareholders at the time of Listing, in compliance with Rule 
8.08(2) of the Listing Rules; (ii) the three largest public Shareholders will not hold more than 
50% of the H Shares held in public hands at the time of Listing, in compliance with Rules 8.08(3) 
and 8.24 of the Listing Rules; (iii) no placee will, individually, be placed more than 10% of the 
enlarged issued share capital of the Company immediately after the Global Offering; and (iv) there 
will not be any new substantial Shareholder (as defined in the Listing Rules) immediately after the 
Global Offering.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. (Hong Kong time) 
on Friday, January 9, 2026, provided that (i) the Global Offering has become unconditional in 
all respects, and (ii) the right of termination described in the section headed “Underwriting – 
Underwriting Arrangements and Expenses – Hong Kong Underwriting Agreement – Grounds for 
termination” in the Prospectus has not been exercised. Investors who trade H Shares prior to the 
receipt of H Share certificates or the H Share certificates becoming valid evidence of title do so 
entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong Kong time) 
on Friday, January 9, 2026,, it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Friday, January 9, 2026,. The H Shares will be traded in board lots 
of 200 H Shares each and the stock code of the H Shares will be 6938.
By order of the Board
Suzhou Ribo Life Science Co., Ltd.
Dr. LIANG Zicai
Chairman, Executive Director and Chief Executive Officer
Hong Kong, January 8, 2026
Directors of the Company named in the application to which this announcement relates are Dr. 
LIANG Zicai, Dr. GAN Liming and Dr. ZHANG Hongyan as executive directors, Dr. QI Fei, 
Mr. LI Dongfang and Mr. LI Yuhui as non-executive directors, and Dr. YU Xuefeng, Mr. MA 
Chaosong and Mr. WANG Ruiping as independent non-executive directors.
