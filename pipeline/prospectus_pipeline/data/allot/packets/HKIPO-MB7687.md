# 配发结果公告抽取任务：7687.HK EACON Group Co., Ltd - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**07/07/2026 22:48**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0707/2026070702043.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"7687.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Hong Kong Stock 
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents 
of this announcement, make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute, and is not intended to constitute, or form a part of any offer or solicitation to 
purchase or subscribe for securities in the United States or in any other jurisdictions. The securities mentioned herein 
have not been, and will not be, registered under the United States Securities Act of 1933 as amended from time to time 
(the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the United States. The securities may 
not be offered, sold, pledged or otherwise transferred within the United States except pursuant to an exemption from 
the registration requirements of the U.S. Securities Act and in compliance with any applicable state securities laws. 
There will be no public offer of the Offer Shares in the United States. The Offer Shares are being offered and sold 
solely outside the United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act and 
applicable laws of each jurisdiction where those offers and sales occur.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
June 29, 2026 (the “Prospectus”) issued by EACON Group Co., Ltd (易控智駕科技股份有限公司) (the “Company”) 
for detailed information about the Global Offering described below before deciding whether or not to invest in the H 
Shares thereby being offered. Any investment decision in relation to the Offer Shares should be taken solely in reliance 
on the information in the Prospectus. The Company has not been and will not be registered under the U.S. Investment 
Company Act of 1940, as amended.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
In connection with the Global Offering, Haitong International Securities Company Limited, as stabilizing manager 
(the “Stabilizing Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, the extent 
permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect 
transactions with a view to stabilizing or supporting the market price of the H Shares at such price, in such amounts 
and in such manners as the Stabilizing Manager, its affiliates or any person acting for it may determine and at a 
level higher than that which might otherwise prevail for a limited period after the Listing Date. However, there is 
no obligation on the Stabilizing Manager (or its affiliates or any person acting for it) to conduct any such stabilizing 
action. Such stabilizing action, if taken, (a) will be conducted at the absolute discretion of the Stabilizing Manager (or 
its affiliates or any person acting for it) and in what the Stabilizing Manager reasonably regards as the best interest 
of our Company, (b) may be discontinued at any time and (c) is required to be brought to an end within 30 days 
of the last day for lodging applications under the Hong Kong Public Offering (which is Sunday, August 2, 2026). 
Such Stabilizing action, if taken, may be effected in all jurisdictions where it is permissible to do so, in each case in 
compliance with all applicable laws, rules and regulatory requirements, including the Securities and Futures (Price 
Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures 
Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Sunday, August 2, 2026). 
After this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of 
the H Shares, could fall.
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinator (for itself and on behalf of the 
Hong Kong Underwriters) shall be entitled to terminate its obligations under the Hong Kong Underwriting Agreement 
with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting – 
Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus 
at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Wednesday, 
July 8, 2026).

<<<PAGE 2>>>
2
EACON Group Co., Ltd
易控智駕科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares 
under the Global Offering
:
26,132,000 H Shares (subject to the Over-
Allotment Option)
Number of Hong Kong Offer Shares
:
2,613,200 H Shares
Number of International Offer Shares
:
23,518,800 H Shares (subject to the Over-
Allotment Option)
Final Offer Price
:
HK$87.92 per H Share, plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
Hong Kong Stock Exchange trading fee 
of 0.00565% and AFRC transaction levy 
of 0.00015%
Nominal value
:
RMB1.00 per H Share
Stock code
:
7687
Sole Sponsor, Overall Coordinator, Joint Global Coordinator,
Joint Bookrunner and Joint Lead Manager
Overall Coordinator, Joint Global Coordinator, 
Joint Bookrunner and Joint Lead Manager
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
EACON Group Co., Ltd
易控智駕科技股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated June 29, 2026 (the “Prospectus”) issued by 
EACON Group Co., Ltd (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
7687
Stock short name
EACON
Dealings commencement date
July 8, 2026*
* see note in the section headed “Disclaimers” in this announcement
Price Information
Final Offer Price
HK$87.92
Offer Price Range
HK$81.16-HK$87.92
Offer Price Adjustment
N/A
Offer Shares and Share Capital
Number of Offer Shares
26,132,000
Final Number of Offer Shares in Hong Kong Public Offering
2,613,200
Final Number of Offer Shares in International Offering (before 
exercise of the Over-Allotment Option)
23,518,800
Number of issued Shares upon Listing (before exercise of the 
Over-Allotment Option)
147,869,769
Over-allocation
Number of Offer Shares over-allocated(Note)
3,919,800
– International Offering
3,919,800
Note: Such over-allocation may be covered by exercising the Over-Allotment Option or by making purchases in the 
secondary market at prices that do not exceed the Offer Price or through deferred delivery or a combination of these 
means. In the event the Over-Allotment Option is exercised, an announcement will be made on the Stock Exchange’s 
website.

<<<PAGE 4>>>
4
Proceeds
Gross proceeds(Note)
HK$2,297.53 million
  Less: Estimated listing expenses payable based on Final Offer 
Price
HK$122.72 million
Net proceeds
HK$2,174.81 million
Note: Gross proceeds refer to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The Company 
will adjust the allocation of the net proceeds from the exercise of the Over-Allotment Option (if any) for the 
purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus on a pro rata basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
110,386
No. of successful applications
24,377
Subscription level
157.82 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong 
Public Offering
2,613,200
Final no. of Offer Shares under the Hong Kong Public Offering
2,613,200
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering
10.00%
Note: For details of the final allocation of H Shares to the Public Offer, investors can refer to 
www.eipo.com.hk/eIPOAllotment to perform a search by identification number or www.eipo.com.hk/eIPOAllotment 
for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
74
Subscription Level
10.50 times
No. of Offer Shares initially available under the International 
Offering
23,518,800
Final no. of Offer Shares under the International Offering
23,518,800
% of Offer Shares under the International Offering to the Global 
Offering
90.00%

<<<PAGE 5>>>
5
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a 
consent under Rule 10.04 under the Listing Rules and/or paragraph 1C(2) of Appendix F1 to the 
Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange to permit the Company 
to allocate certain Offer Shares in the International Offering to certain existing Shareholders and/
or their close associates, and (b) a consent under Rule 9.09(b) under the Listing Rules and/or 
paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to, 
among other things, allocate further Offer Shares in the International Offering to certain existing 
Shareholders and Cornerstone Investors and/or their close associates, (i) none of the Offer Shares 
subscribed by the placees and the public have been financed directly or indirectly by the Company, 
any of the Directors, chief executive of the Company, Controlling Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates; and (ii) none of the placees and the public who have purchased the Offer Shares 
are accustomed to taking instructions from the Company, any of its Directors, Supervisors, 
chief executive, Controlling Shareholders, substantial Shareholders, existing Shareholders of the 
Company or any of its subsidiaries or their respective close associates in relation to the acquisition, 
disposal, voting or other disposition of H Shares registered in his/her/its name or otherwise held by 
him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
Cornerstone Investors
No. of Offer 
Shares 
allocated(1)
Approximate 
% of Offer 
Shares(2)
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering(2)
Approximately 
% of total 
issued share 
capital after 
the Global 
Offering(2)
Existing
Shareholders 
or their close 
associates
ZIJINNING Limited Partnership 
(“ZIJINNING”)
1,782,450
6.82%
1.21%
1.21%
Yes(3)
Aurora SF (in connection with 
the Arrangement)
1,336,800
5.12%
0.90%
0.90%
No
FIL Investment Management 
(Hong Kong) Limited
(“Fidelity International”)
2,673,650
10.23%
1.81%
1.81%
Yes(4)
JPMorgan Asset Management 
(Asia Pacific) Limited
(“JPMAMAPL”)
2,228,050
8.53%
1.51%
1.51%
No
Baring Asset Management 
(Asia) Limited (“Barings”)
1,336,800
5.12%
0.90%
0.90%
No
Indus Select Master Fund, Ltd. 
and Vitruvius SICAV-Asian 
Equity (“Indus Fund”)
891,200
3.41%
0.60%
0.60%
No
Jain Global Master Fund Ltd
891,200
3.41%
0.60%
0.60%
No
Regal Partners Holdings Pty 
Limited and Regal Tactical 
Opportunities (Offshore) Master 
Fund (“REGAL”)
712,950
2.73%
0.48%
0.48%
No

<<<PAGE 6>>>
6
Cornerstone Investors
No. of Offer 
Shares 
allocated(1)
Approximate 
% of Offer 
Shares(2)
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering(2)
Approximately 
% of total 
issued share 
capital after 
the Global 
Offering(2)
Existing
Shareholders 
or their close 
associates
GF Fund Management Co., Ltd. 
and GF International Investment 
Management Limited (“GF 
Fund”)
445,600
1.71%
0.30%
0.30%
No
CDH Golden River L.P. 
(“CDH”)
445,600
1.71%
0.30%
0.30%
No
Seven Grand Managers, LLC 
(“Seven Grand”)
267,350
1.02%
0.18%
0.18%
No
Total
13,011,650
49.79%
8.80%
8.80%
Notes:
(1) 
The number of Offer Shares allocated to such investors only represents the number of Offer Shares allocated 
to the investors as cornerstone investors in the International Offering. For allocations of Offer Shares to 
the relevant investors as placees (if any), please refer to the section headed “Allotment Results Details – 
International Offering – Allottees with Waivers/Consents Obtained” in this announcement.
(2) 
Assuming the Over-Allotment Option is not exercised.
(3) 
ZIJINNING is a limited partnership established in BVI, which is ultimately wholly owned by Zijin Mining, 
which is in turn a subsidiary of Minxi Xinghang. Upon completion of the Global Offering (assuming the 
Over-Allotment Option is not exercised), Minxi Xinghang and its controlled entities (including Xinghang 
Chaozhi, Xinghang Chaoguang, Xinghang Qiguang, Xinghang Chaofeng and Xinghang Qixin) will in aggregate 
hold approximately 10.06% of the total issued share capital of the Company, and Minxi Xinghang will be a 
substantial Shareholder of the Company as defined under the Listing Rules. ZIJINNING is, accordingly, a 
core connected person of the Company and a close associate of an existing Shareholder of the Company. See 
“History, Development and Corporate Structure – Pre-IPO Investments – 5. Information about the Pre-IPO 
Investors” in the Prospectus for further details.
(4) 
Eight Roads (Tianjin) Equity Investment Partnership Enterprise (Limited Partnership) (斯道(天津)股權投資合
夥企業(有限合夥)) (“Tianjin Eight Roads”) is an existing Shareholder with approximately 1.54% shareholding 
and voting rights in the Company as of the date of this announcement. The general partner of Tianjin Eight 
Roads is Fidelity Growth (Shanghai) Equity Investment Management Co., Ltd. (富達成長(上海)股權投資管理
有限公司), which is wholly owned by Eight Roads Capital Advisors (Hong Kong) Limited (斯道資本(香港)有
限公司), a wholly owned subsidiary of Eight Roads GP. Eight Roads GP is indirectly wholly owned by Eight 
Roads Management Limited, which is in turn owned as to more than one-third by each of Cliff Trail LLC and 
Crow Lane Limited. Among the three limited partners of Tianjin Eight Roads, only Asia Ventures II QF L.P. 
holds 30% or more partnership interest thereof. See “History, Development and Corporate Structure – Pre-IPO 
Investments – 5. Information about the Pre-IPO Investors” in the Prospectus for further details.
(5) 
In addition to the Offer Shares subscribed for as Cornerstone Investors, all Cornerstone Investors except for 
CDH, were allocated further Offer Shares as placees in the International Offering. Please refer to the section 
headed “Allotment Results Details – International Offering – Allottees with Waivers/Consents Obtained” in this 
announcement for details. Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-
up as indicated below. For details, please refer to the section headed “Lock-up Undertakings – Cornerstone 
Investors” in this announcement.

<<<PAGE 7>>>
7
Allottees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of Offer 
Shares(2)
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering(1)
Approximately 
% of total 
issued share 
capital after 
the Global 
Offering(1)
Relationship
Part A Allottees as Cornerstone Investors
Allottees with a waiver from strict compliance with the requirements under Rule 9.09(b) under the Listing 
Rules and consent under Paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to 
subscription for H Shares by close associates of existing Shareholders as Cornerstone Investors(2)
ZIJINNING
1,782,450
6.82%
1.21%
1.21%
A cornerstone 
investor, a placee and 
a close associate of an 
existing Shareholder
Allottees with consent under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by 
close associates of existing Shareholders as Cornerstone Investors(2)
Fidelity International
2,673,650
10.23%
1.81%
1.81%
A cornerstone 
investor, a placee and 
a close associate of an 
existing Shareholder
Part B Allottees as placees other than Cornerstone Investors
Allottees with consent under Rule 9.09(b) under the Listing Rules and paragraph 18 of Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations of further H Shares to existing Shareholders and/or their close 
associates and Cornerstone Investors and/or their close associates(3)
ZIJINNING
445,600
1.71%
0.30%
0.30%
Same entity as the 
Cornerstone Investor 
and a close associate 
of a substantial 
shareholder
Guotai Junan Investments 
(Hong Kong) Limited (in 
connection with Chentao 
Xinnuo Swaps)(4)
789,850
3.02%
0.53%
0.53%
A placee, a connected 
client and the ultimate 
client of which is 
Chentao Xinnuo, a 
close associate of a 
substantial shareholder
Aurora SF (in connection 
with the Arrangement)(5)
712,950
2.73%
0.48%
0.48%
Same entity as the 
Cornerstone Investor 
and the ultimate 
client of which is 
Shanghai Jingshi, a 
close associate of an 
existing Shareholder

<<<PAGE 8>>>
8
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of Offer 
Shares(2)
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering(1)
Approximately 
% of total 
issued share 
capital after 
the Global 
Offering(1)
Relationship
Guotai Junan
Investments (Hong Kong)
Limited (in connection
with Shanghai Jingshi 
Swaps)(4)
712,950
2.73%
0.48%
0.48%
A placee, a connected 
client and the ultimate 
client of which is 
Shanghai Jingshi, a 
close associate of an 
existing Shareholder
Fidelity International
26,750
0.10%
0.02%
0.02%
Same entity as the 
Cornerstone Investor
JPMAMAPL
935,750
3.58%
0.63%
0.63%
Same entity as the 
Cornerstone Investor
Barings
623,850
2.39%
0.42%
0.42%
Same entity as the 
Cornerstone Investor
Indus Fund
891,200
3.41%
0.60%
0.60%
Same entity as the 
Cornerstone Investor
Jain Global Master Fund 
Ltd
623,850
2.39%
0.42%
0.42%
Same entity as the 
Cornerstone Investor
Regal Funds Management 
Asia Pte Ltd
267,350
1.02%
0.18%
0.18%
A close associate 
of REGAL, a 
Cornerstone Investor
GF Fund
891,150
3.41%
0.60%
0.60%
Same entity as the 
Cornerstone Investor
Seven Grand
133,650
0.51%
0.09%
0.09%
Same entity as the 
Cornerstone Investor
Allottees with consent under Rule 10.04 under the Listing Rules and/or paragraph 1C(2) of the Placing Guidelines 
in relation to allocations of further H Shares to existing Shareholders and/or their close associates as placees(6)
CHINA SPECIAL 
OPPORTUNITY FUND 
SPC (“CSO FUND”) 
ACTING FOR AND IN 
RESPECT OF CSOF-
PILOT SP (“CSOF-PILOT 
SP”)
178,200
0.68%
0.12%
0.12%
A placee, an existing 
Shareholder
Chaos Investment Co., Ltd. 
(“Chaos Investment”)
534,700
2.05%
0.36%
0.36%
A placee, a close 
associate of an 
existing Shareholder

<<<PAGE 9>>>
9
Investor
No. of Offer 
Shares 
allocated
Approximate 
% of Offer 
Shares(2)
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering(1)
Approximately 
% of total 
issued share 
capital after 
the Global 
Offering(1)
Relationship
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients(7)
Guotai Junan Investments 
(Hong Kong) Limited (the 
“GTINV”)
1,765,500
6.76%
1.19%
1.19%
Connected client as a 
placee
Fullgoal Asset 
Management (HK) Limited 
(“Fullgoal HK”)
4,750
0.02%
0.0032%
0.0032%
Connected client as a 
placee
(1) 
Assuming the Over-Allotment Option is not exercised.
(2) 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as Cornerstone Investors in the International Offering. The 
Stock Exchange has granted a consent under Rule 10.04 under the Listing Rules and/or paragraph 1C(2) of 
the Placing Guidelines and Rule 9.09(b) under the Listing Rules and/or paragraph 18 of Chapter 4.15 of the 
Guide for New Listing Applicants to permit H Shares in the International Offering to be placed to such existing 
Shareholders. Please refer to the section headed “Waivers – Waiver under Rule 9.09(b) of, and consent under 
Paragraph 1C(2) of Appendix F1 to, the Listing Rules and paragraph 18 of chapter 4.15 of the Guide for New 
Listing Applicants in respect of subscriptions for Offer Shares by close associates of existing Shareholders as 
cornerstone investors” of the Prospectus for details.
The Stock Exchange has granted the waiver on the condition that, among others, details of the allocation to the 
existing Shareholders will be disclosed in the Prospectus and/or allotment results announcement.
(3) 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details – International Offering – Cornerstone Investors” in this announcement. For details of the 
consent under Rule 9.09(b) under the Listing Rules and/or paragraph 18 of Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations of further H Shares to the Cornerstone Investors, please refer to the 
section headed “Others/Additional Information – Allocations of Offer Shares to certain existing Shareholders 
and Cornerstone Investors and/or their close associates with a consent under Rule 9.09(b) under the Listing 
Rules and/or paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants” in this announcement.

<<<PAGE 10>>>
10
(4) 
Guotai Junan Investments (Hong Kong) Limited (“GTINV”) shall hold the Offer Shares for hedging purpose as 
the single underlying asset of several sets of back-to-back total return swap transaction (the “GTHT Back-to-
back TRS”) to be entered into between GTINV and Guotai Haitong Securities Co., Ltd. (the “GTHT Onshore 
Parent”) in connection with several total return swap orders (the “GTHT Client TRS”) to be entered into by 
GTHT Onshore Parent and several ultimate clients (the “GTHT Onshore Ultimate Clients”), respectively. 
Such GTHT Client TRS is to be fully funded by the GTHT Onshore Ultimate Clients. GTINV will hold the 
Offer Shares on a non-discretionary basis for the purpose of hedging the economic exposure under the GTHT 
Back-to-back TRS and GTHT Client TRS only. During the tenor of the GTHT Client TRS, all economic returns 
of the Offer Shares will be passed to the GTHT Onshore Ultimate Clients and all economic losses shall be 
borne by the GTHT Onshore Ultimate Clients, subject to the terms and conditions of the GTHT Back-to-back 
TRS and GTHT Client TRS, and GTINV will not take part in any economic return or bear any economic loss in 
relation to the price of the Offer Shares. The GTHT Onshore Ultimate Clients may request to redeem the Offer 
Shares at their own discretion, upon which GTINV shall dispose of the Offer Shares and settle the GTHT Back-
to-back TRS and GTHT Client TRS in cash in accordance with the terms and conditions of the GTHT Back-
to-back TRS and GTHT Client TRS documents. Due to its internal policy, GTINV will not exercise the voting 
right attaching to the Offer Shares during the tenor of the GTHT Back-to-back TRS and GTHT Client TRS. To 
the best knowledge of GTINV and after making all reasonable enquiries, (i) GTINV has confirmed that, to the 
best of its knowledge, each of the GTHT Onshore Ultimate Clients and the ultimate beneficial owners holding 
30% or more interest of the GTHT Onshore Ultimate Clients is an independent third party of GTINV, Haitong 
Securities, and the companies which are members of the same group of companies as Haitong Securities and 
(ii) GTINV is not a collective investment scheme which is not authorized by the SFC nor is expected to hold 
the Offer Shares on behalf of such scheme. For details, please refer to the section headed “Others/Additional 
Information – Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines 
as placees” in this announcement.
(5) 
Aurora SF is a Singapore variable capital company. Oversea-Chinese Banking Corporation Limited (“OCBC 
Singapore”) and OCBC Bank Limited (“OCBC China”) will enter into cross-border total return swap (“Swap”) 
and Shanghai Jingshi Investment Management Center (Limited Partnership) (上海經石投資管理中心(有限合
夥)) (the “Ultimate Client”) will invest in structured deposit products issued by OCBC China (collectively, 
the “Arrangement”), pursuant to which Aurora SF will hold the legal title to the Offer Shares on a non-
discretionary basis to hedge the Swap while the economic risks and returns of the underlying Offer Shares are 
ultimately passed to the Ultimate Client, subject to customary fees and commissions. Aurora SF’s subscription 
of the Offer Shares will be fully funded by OCBC Singapore, and the Arrangement will be fully funded by the 
Ultimate Client.
(6) 
For allocations of Offer Shares to the relevant investors as placees, please refer to the section headed “Others/
Additional Information – Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines” and “Others/Additional Information – Allocations of Offer Shares to certain existing Shareholders 
and/or their close associates with a consent under paragraph 1C(2) of the Placing Guidelines pursuant to the 
fulfillment of Existing Shareholders Conditions and grounds as placees” in this announcement.
(7) 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients, please refer to the sections headed 
“Others/Additional Information – Placing to connected clients with a prior consent under paragraph 1C(1) of 
the Placing Guidelines” and “Others/Additional Information – Allocations of Offer Shares to certain existing 
Shareholders and Cornerstone Investors and/or their close associates with a consent under Rule 9.09(b) under 
the Listing Rules and/or paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants” in this 
announcement.

<<<PAGE 11>>>
11
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of H 
shares held in 
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
in Company 
subject to 
lock-up 
undertakings 
upon Listing(1)
Last day 
subject to 
the lock-up 
undertakings(2)
Mr. Lan(3)
32,000,000
32,000,000
21.64%
21.64%
July 7, 2029(3)(4)
Mr. Zhang(3)
7,492,858
7,492,858
5.07%
5.07%
July 7, 2029(3)(4)
Ms. Liu
2,803,628
2,803,628
1.90%
1.90%
July 7, 2027(4)
Jiaxing Zhitao
8,823,529
8,823,529
5.97%
5.97%
July 7, 2027(4)
Ningbo Yuying
487,990
487,990
0.33%
0.33%
July 7, 2027(4)
Ningbo Zhongying
433,233
433,233
0.29%
0.29%
July 7, 2027(4)
Sub-total
52,041,238
35.19%
35.19%
Notes:
(1) 
Assuming the Over-Allotment Option is not exercised.
(2) 
All existing Shareholders (including the Controlling Shareholders) shall not dispose of any of the Shares held 
by them within the 12 months following the Listing Date as required under the applicable PRC laws.
(3) 
Pursuant to the voluntary lock-up undertakings provided by each of Mr. Lan and Mr. Zhang, in addition to any 
restriction under applicable laws and regulations, the Shares directly held by them would be subject to a three-
year lock-up period upon Listing, with one-third of such Shares to be released at the end of each anniversary 
following the Listing Date. For details, please refer to the section headed “Relationship with Our Controlling 
Shareholders – Our Controlling Shareholders – Voluntary Lock-up Undertakings by Mr. Lan and Mr. Zhang” in 
the Prospectus.
(4) 
Pursuant to Rule 10.07 of the Listing Rules, each of Controlling Shareholders has undertaken to the Stock 
Exchange and the Company that he/she/it shall not dispose of or transfer any Shares in the period commencing 
on the date by reference to which disclosure of its shareholdings is made in the Prospectus and ending on the 
date which is six months from the Listing Date (the “First Six-month Period”), and in the following six months 
commencing from the expiry of the First Six-month Period, he/she/it may dispose of or transfer Shares subject 
to that any member of Controlling Shareholders will not cease to be a controlling shareholder (as defined 
in the Listing Rules). For further details, please refer to the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Undertakings to the Stock Exchange pursuant to 
the Listing Rules – (B) Undertakings by the Controlling Shareholders” in the Prospectus.

<<<PAGE 12>>>
12
Existing Shareholders (other than Controlling Shareholders)
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of H 
shares held in 
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
in Company 
subject to 
lock- up 
undertakings 
upon Listing(2)
Last day 
subject to 
the lock-up 
undertakings(2)
Minxi Xinghang 
State-Owned 
Asset Investment 
Management Co., Ltd. 
(閩西興杭國有資產
投資經營有限公司) 
(“Minxi Xinghang”)
5,232,980
5,232,980
3.54%
3.54%
July 7, 2027
Shanghang County 
Xinghang Chaozhi 
Venture Capital 
Partnership Enterprise 
(Limited Partnership) 
(上杭縣興杭朝智創
業投資合夥企業(有
限合夥)) (“Xinghang 
Chaozhi”)
4,278,075
4,278,075
2.89%
2.89%
July 7, 2027
Shanghang Xinghang 
Chaoguang Venture 
Capital Partnership 
(Limited Partnership) 
(上杭興杭朝光創業
投資合夥企業(有限
合夥)) (“Xinghang 
Chaoguang”)
1,024,123
1,024,123
0.69%
0.69%
July 7, 2027
Shanghang Xinghang 
Qiguang Venture 
Capital Partnership 
(Limited Partnership) 
(上杭興杭啟光創業
投資合夥企業(有限
合夥)) (“Xinghang 
Qiguang”)
1,004,129
1,004,129
0.68%
0.68%
July 7, 2027

<<<PAGE 13>>>
13
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of H 
shares held in 
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
in Company 
subject to 
lock- up 
undertakings 
upon Listing(2)
Last day 
subject to 
the lock-up 
undertakings(2)
Shanghang Xinghang 
Chaofeng Venture 
Capital Partnership 
(Limited Partnership) 
(上杭興杭朝風創業
投資合夥企業(有限
合夥)) (“Xinghang 
Chaofeng”)
604,987
604,987
0.41%
0.41%
July 7, 2027
Shanghang Xinghang 
Qixin Venture Capital 
Partnership (Limited 
Partnership) (上杭興
杭啓信創業投資合
夥企業(有限合夥)) 
(“Xinghang Qixin”)
2,730,010
2,730,010
1.85%
1.85%
July 7, 2027
Huzhou Yuecheng 
Equity Investment 
Partnership Enterprise 
(Limited Partnership) 
(湖州越誠股權投資
合夥企業(有限合夥)) 
(“Huzhou Yuecheng”)
1,185,827
1,185,827
0.80%
0.80%
July 7, 2027
Jiaxing Kelong 
Venture Capital 
Partnership (Limited 
Partnership) (嘉興科
隆創業投資合夥企業
(有限合夥)) (“Jiaxing 
Kelong”)
1,009,027
1,009,027
0.68%
0.68%
July 7, 2027
Jiaxing Chenzhi 
Venture Capital 
Partnership (Limited 
Partnership) (嘉興辰
智創業投資合夥企業
(有限合夥)) (“Jiaxing 
Chenzhi”)
612,274
612,274
0.41%
0.41%
July 7, 2027

<<<PAGE 14>>>
14
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of H 
shares held in 
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
in Company 
subject to 
lock- up 
undertakings 
upon Listing(2)
Last day 
subject to 
the lock-up 
undertakings(2)
Pingtan Jiayi Venture 
Capital Partnership 
(Limited Partnership) 
(平潭嘉翼創業投資
合夥企業(有限合夥)) 
(“Pingtan Jiayi”)
604,987
604,987
0.41%
0.41%
July 7, 2027
Jiaxing Chenyi Venture 
Capital Partnership 
Enterprise (Limited 
Partnership) (嘉興辰
易創業投資合夥企業
(有限合夥)) (“Jiaxing 
Chenyi”)
507,141
507,141
0.34%
0.34%
July 7, 2027
Shanghai Chentao 
Chuangxiang 
Chuangye Venture 
Capital Partnership 
Enterprise (Limited 
Partnership) (上海
辰韜創享創業投資
合夥企業(有限合
夥)) (“Chuangxiang 
Chuangye”)
422,425
422,425
0.29%
0.29%
July 7, 2027
Shanghang Yitao 
Venture Capital 
Partnership (Limited 
Partnership) (上杭易
韜創業投資合夥企業
(有限合夥)) (“Yitao 
Chuangye”)
636,172
636,172
0.43%
0.43%
July 7, 2027
Zijin Mining Zidi 
(Xiamen) Investment 
Partnership Enterprise 
(Limited Partnership) 
(紫金礦業紫地(廈
門)投資合夥企業
(有限合夥)) (“Zidi 
Investment”)
3,183,823
3,183,823
2.15%
2.15%
July 7, 2027

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
shares held in 
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
in Company 
subject to 
lock- up 
undertakings 
upon Listing(2)
Last day 
subject to 
the lock-up 
undertakings(2)
Zijin Mining Ziniu 
(Xiamen) Industrial 
Investment Fund 
Partnership (Limited 
Partnership) (紫金礦
業紫牛(廈門)產業
投資基金合夥企業
(有限合夥)) (“Ziniu 
Investment”)
1,134,352
1,134,352
0.77%
0.77%
July 7, 2027
Zijin Mining Zixing 
(Xiamen) Investment 
Partnership (Limited 
Partnership) (紫金礦
業紫興(廈門)投資合
夥企業(有限合夥)) 
(“Zixing Investment”)
179,457
179,457
0.12%
0.12%
July 7, 2027
Zijin Mining 
Investment Haixia 
Qihang (Fuzhou) 
Equity Investment 
Partnership (Limited 
Partnership) (紫金礦
業產投海峽啟航(福
州)股權投資合夥企業
(有限合夥)) (“Qihang 
Investment”)
211,212
211,212
0.14%
0.14%
July 7, 2027
Ningbo Nanying
9,078,777
9,078,777
6.14%
6.14%
July 7, 2027
Shanghang Chentao 
Xinghang Venture 
Capital Partnership 
(Limited Partnership) 
(上杭辰韜興杭創業
投資合夥企業(有限
合夥)) (“Chentao 
Xinghang”)
1,885,803
1,885,803
1.28%
1.28%
July 7, 2027
Magic Academy 
Limited
3,917,214
3,917,214
2.65%
2.65%
July 7, 2027

<<<PAGE 16>>>
16
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of H 
shares held in 
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
in Company 
subject to 
lock- up 
undertakings 
upon Listing(2)
Last day 
subject to 
the lock-up 
undertakings(2)
Eight Roads (Tianjin) 
Equity Investment 
Partnership Enterprise 
(Limited Partnership) 
(斯道(天津)股權投
資合夥企業(有限合
夥)) (“Tianjin Eight 
Roads”)
1,872,750
1,872,750
1.27%
1.27%
July 7, 2027
Suzhou Zhongxin 
Xingfu Digital 
Intelligence Venture 
Capital Partnership 
Enterprise (Limited 
Partnership) (蘇州中
新興富數智創業投
資合夥企業(有限合
夥)) (“Xingfu Digital 
Intelligence”)
1,224,547
1,224,547
0.83%
0.83%
July 7, 2027
Ma Zheng (馬徵)
537,665
537,665
0.36%
0.36%
July 7, 2027
Zhengzhou Tianjian 
Talent Venture Capital 
Fund Partnership 
(Limited Partnership) 
(鄭州天健人才創業投
資基金合夥企業(有限
合夥)) (“Zhengzhou 
Hi-Tech Fund”)
489,819
489,819
0.33%
0.33%
July 7, 2027
Ningbo Yunji 
Chuangyuan Enterprise 
Management 
Consulting Partnership 
(Limited Partnership) 
(寧波雲際創遠企業
管理諮詢合夥企業
(有限合夥)) (“Yunji 
Chuangyuan”)
1,377,752
1,377,752
0.93%
0.93%
July 7, 2027

<<<PAGE 17>>>
17
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of H 
shares held in 
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
in Company 
subject to 
lock- up 
undertakings 
upon Listing(2)
Last day 
subject to 
the lock-up 
undertakings(2)
Wuxi Xingqi Yuzheng 
Venture Capital 
Partnership (Limited 
Partnership) (無錫星奇
昱正創業投資合夥企
業(有限合夥)) (“Wuxi 
Xingqi”)
646,991
646,991
0.44%
0.44%
July 7, 2027
Ningbo Xihe 
Investment 
Management 
Partnership (Limited 
Partnership) (寧波熙
禾投資管理合夥企業
(有限合夥)) (“Xihe 
Investment”)
691,815
691,815
0.47%
0.47%
July 7, 2027
Ningbo Meishan 
Bonded Port Area 
Wending Investment 
Co., Ltd. (寧波梅山
保稅港區問鼎投資
有限公司) (“Ningbo 
Wending”)
682,633
682,633
0.46%
0.46%
July 7, 2027
Shenzhen 
Lvshuichangqing 
Venture Capital 
Investment Partnership 
(Limited Partnership) 
(深圳市綠水長青創
業投資合夥企業(有
限合夥)) (“Lvshui 
Changqing”)
76,600
76,600
0.05%
0.05%
July 7, 2027
Fujian Shidai Zeyuan 
Equity Investment 
Fund Partnership 
(Limited Partnership) 
(福建時代澤遠股權
投資基金合夥企業
(有限合夥)) (“Shidai 
Zeyuan”)
4,026,975
4,026,975
2.72%
2.72%
July 7, 2027

<<<PAGE 18>>>
18
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of H 
shares held in 
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
in Company 
subject to 
lock- up 
undertakings 
upon Listing(2)
Last day 
subject to 
the lock-up 
undertakings(2)
Zhao Dapeng (趙大鵬)
862,655
862,655
0.58%
0.58%
July 7, 2027
Ocean EW15 Limited
232,917
232,917
0.16%
0.16%
July 7, 2027
Tonly
646,991
646,991
0.44%
0.44%
July 7, 2027
Wang Xiaoshen (王曉
申)
107,832
107,832
0.07%
0.07%
July 7, 2027
Li Chenglin (李承霖)
323,496
323,496
0.22%
0.22%
July 7, 2027
Small and Medium-
Sized Fangguang 
(Shanghai) Private 
Fund Partnership 
(Limited Partnership) 
(中小方廣(上海)私
募基金合夥企業(有
限合夥)) (“Shanghai 
Fangguang”)
988,364
988,364
0.67%
0.67%
July 7, 2027
Changzhou Fangguang 
Phase IV Venture 
Capital Partnership 
(Limited Partnership) 
(常州方廣四期創業
投資合夥企業(有限
合夥)) (“Changzhou 
Fangguang”)
1,342,589
1,342,589
0.91%
0.91%
July 7, 2027
Shandong Green New 
Energy Industry Equity 
Investment Fund 
Partnership (Limited 
Partnership) (山東省
綠色新能源產業股權
投資基金合夥企業(有
限合夥)) (“Shangdong 
New Energy”)
1,078,319
1,078,319
0.73%
0.73%
July 7, 2027

<<<PAGE 19>>>
19
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of H 
shares held in 
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
in Company 
subject to 
lock- up 
undertakings 
upon Listing(2)
Last day 
subject to 
the lock-up 
undertakings(2)
Fuzhou Economic 
and Technological 
Development 
Zone Shengchuang 
Investment Partnership 
(Limited Partnership) 
(福州經濟技術開發
區盛創投資合夥企業
(有限合夥)) (“Fuzhou 
Shengchuang”)
53,094
53,094
0.04%
0.04%
July 7, 2027
China Special 
Opportunity Fund SPC 
(“CSO FUND”)
1,375,786
1,375,786
0.93%
0.93%
July 7, 2027
Hainan Daoyi 
Zhongxin Investment 
Partnership (Limited 
Partnership) (海南道
翼中芯投資合夥企業
(有限合夥)) (“Hainan 
Daoyi”)
211,212
211,212
0.14%
0.14%
July 7, 2027
Luoyang Industrial 
Development Fund 
Partnership (Limited 
Partnership) (洛陽
市產業發展基金合
夥企業(有限合夥)) 
(“Luoyang Fund”)
1,056,062
1,056,062
0.71%
0.71%
July 7, 2027
Fuyan Hi-Tech 
(Longyan) Private 
Equity Venture Capital 
Partnership (Limited 
Partnership) (福岩高新
(龍岩)私募創業投資
合夥企業(有限合夥)) 
(“Fuyan Gaoxin”)
380,182
380,182
0.26%
0.26%
July 7, 2027
Huafu Growth 
Investment Co., Ltd. 
(華福成長投資有
限公司) (“Huafu 
Investment”)
211,212
211,212
0.14%
0.14%
July 7, 2027

<<<PAGE 20>>>
20
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of H 
shares held in 
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
in Company 
subject to 
lock- up 
undertakings 
upon Listing(2)
Last day 
subject to 
the lock-up 
undertakings(2)
Longyan Ruitou Equity 
Investment Partnership 
(Limited Partnership) 
(龍岩睿投股權投資
合夥企業(有限合夥)) 
(“Longyan Ruitou”)
1,056,062
1,056,062
0.71%
0.71%
July 7, 2027
Shanghai Xingfu 
Young Eagle Private 
Equity Investment 
Fund Partnership 
(Limited Partnership) 
(上海興富雛鷹私募投
資基金合夥企業(有
限合夥)) (“Shanghai 
Xingfu”)
211,212
211,212
0.14%
0.14%
July 7, 2027
Qingdao Huixin 
Investment Partnership 
(Limited Partnership) 
(青島惠鑫投資合
夥企業(有限合夥)) 
(“Qingdao Huixin”)
1,056,062
1,056,062
0.71%
0.71%
July 7, 2027
Gongqingcheng TAM 
No. 1 Venture Capital 
Partnership (Limited 
Partnership) (共青城
天岸馬一號創業投資
合夥企業(有限合夥)) 
(“TAM No. 1 Venture 
Capital”)
673,345
673,345
0.46%
0.46%
July 7, 2027
Ge Weidong (葛衛東)
2,112,124
2,112,124
1.43%
1.43%
July 7, 2027
Shenzhen Desay SV 
Capital Co., Ltd. (深
圳市德賽西威產業
投資有限公司) (“SV 
Capital”)
1,267,275
1,267,275
0.86%
0.86%
July 7, 2027

<<<PAGE 21>>>
21
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of H 
shares held in 
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
in Company 
subject to 
lock- up 
undertakings 
upon Listing(2)
Last day 
subject to 
the lock-up 
undertakings(2)
Hongxing Green 
Venture Capital 
Industry Fund (Anhui) 
(Limited Partnership) 
(弘興綠色創業投資
產業基金(安徽)(有
限合夥)) (“Anhui 
Hongxing”)
1,478,487
1,478,487
1.00%
1.00%
July 7, 2027
Hunan Bofu Cultural 
Industry Investment 
Fund Enterprise 
(Limited Partnership) 
(湖南泊富文化產業投
資基金企業(有限合
夥)) (“Hunan Bofu”)
211,212
211,212
0.14%
0.14%
July 7, 2027
Tianjin Gaocheng Deyi 
Investment Partnership 
(Limited Partnership) 
(天津高成德億投資
合夥企業(有限合夥)) 
(“Gaocheng Deyi”)
1,056,062
1,056,062
0.71%
0.71%
July 7, 2027
Fujian Provincial 
Government 
Investment Fund Co., 
Ltd. (福建省省級政府
投資基金有限公司) 
(“Fujian Provincial 
Fund”)
633,637
633,637
0.43%
0.43%
July 7, 2027
Total
69,696,531
69,696,531
47.13%
47.13%
Notes:
(1) 
Assuming the Over-Allotment Option is not exercised.
(2) 
All existing Shareholders (including the Controlling Shareholders) shall not dispose of any of the Shares held 
by them within the 12 months following the Listing Date as required under the applicable PRC laws.

<<<PAGE 22>>>
22
Cornerstone Investors
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of H 
shares held in 
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
in Company 
subject to 
lock- up 
undertakings 
upon Listing(1)
Last day 
subject to 
the lock-up 
undertakings(2)
ZIJINNING
1,782,450
1,782,450
1.21%
1.21%
January 7, 2027
Aurora SF (in 
connection with the 
Arrangement)
1,336,800
1,336,800
0.90%
0.90%
January 7, 2027
Fidelity International
2,673,650
2,673,650
1.81%
1.81%
January 7, 2027
JPMAMAPL
2,228,050
2,228,050
1.51%
1.51%
January 7, 2027
Barings
1,336,800
1,336,800
0.90%
0.90%
January 7, 2027
Indus Fund
891,200
891,200
0.60%
0.60%
January 7, 2027
Jain Global Master 
Fund Ltd
891,200
891,200
0.60%
0.60%
January 7, 2027
REGAL
712,950
712,950
0.48%
0.48%
January 7, 2027
GF Fund
445,600
445,600
0.30%
0.30%
January 7, 2027
CDH
445,600
445,600
0.30%
0.30%
January 7, 2027
Seven Grand
267,350
267,350
0.18%
0.18%
January 7, 2027
Sub-total
13,011,650
13,011,650
8.80%
8.80%
Notes:
(1) 
Assuming the Over-Allotment Option is not exercised.
(2) 
In accordance with the respective cornerstone investment agreements, the required lock-up periods will end on 
January 7, 2027. The Cornerstone Investors will cease to be prohibited from disposing of or transferring the 
Shares subscribed for pursuant to their respective cornerstone investment agreements after the indicated date.

<<<PAGE 23>>>
23
PLACEE CONCENTRATION ANALYSIS
Placees
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
Allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
Allotment 
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
Allotment
Option)
Allotment as 
% of total 
Offer Shares 
(assuming 
the Over-
Allotment 
Option is 
exercised and 
new H Shares 
are issued)
Number of H 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing 
(assuming 
no exercise 
of the Over-
Allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
Allotment 
Option is 
exercised and 
new H Shares 
are issued)
Top 1
3,163,800
13.45%
11.53%
12.11%
10.53%
3,163,800
2.14%
2.08%
Top 5
12,815,600
54.49%
46.71%
49.04%
42.65%
17,524,444
11.85%
11.55%
Top 10
19,232,200
81.77%
70.09%
73.60%
64.00%
23,941,044
16.19%
15.77%
Top 25
25,224,150
107.25%
91.93%
96.53%
83.94%
38,398,757
25.97%
25.30%
Notes
* Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDER CONCENTRATION ANALYSIS
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
Allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
Allotment 
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
Allotment
Option)
Allotment as 
% of total 
Offer Shares 
(assuming 
the Over-
Allotment 
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
Allotment 
Option)
% of total 
issued H 
Shares 
capital upon 
Listing 
(assuming 
the Over-
Allotment 
Option is 
exercised and 
new H Shares 
are issued)
Number of 
Shares held 
upon Listing
Top 1
–
–
–
–
0.00%
52,041,238
35.19%
34.29%
52,041,238
Top 5
3,017,900
12.83%
11.00%
11.55%
10.04%
88,698,916
59.98%
58.44%
88,698,916
Top 10
11,644,800
49.51%
42.44%
44.56%
38.75%
106,029,238
71.70%
69.85%
106,029,238
Top 25
18,952,550
80.58%
69.07%
72.53%
63.07%
130,777,027
88.44%
86.16%
130,777,027
Notes
* Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 24>>>
24
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
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
Allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
Allotment 
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
Allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming 
the Over-
Allotment 
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
Allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
Allotment 
Option is 
exercised and 
new H Shares 
are issued)
Top 1
–
–
–
–
–
52,041,238
52,041,238
35.19%
34.29%
Top 5
3,017,900
12.83%
11.00%
11.55%
10.04%
88,698,916
88,698,916
59.98%
58.44%
Top 10
11,644,800
49.51%
42.44%
44.56%
38.75%
106,029,238
106,029,238
71.70%
69.85%
Top 25
18,952,550
80.58%
69.07%
72.53%
63.07%
130,777,027
130,777,027
88.44%
86.16%
Notes
* Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
NO. OF 
SHARES 
APPLIED 
FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
PERCENTAGE 
ALLOTTED 
OF THE 
TOTAL NO. 
OF SHARES 
APPLIED FOR
POOL A
50
45,741 4,574 out of 45,741 to receive 50 Shares
10.00%
100
23,813 2,858 out of 23,813 to receive 50 Shares
6.00%
150
3,244 487 out of 3,244 to receive 50 Shares
5.00%
200
1,489 238 out of 1,489 to receive 50 Shares
4.00%
250
1,567 274 out of 1,567 to receive 50 Shares
3.50%
300
991 178 out of 991 to receive 50 Shares
2.99%
350
619 113 out of 619 to receive 50 Shares
2.61%
400
581 107 out of 581 to receive 50 Shares
2.30%
450
422 80 out of 422 to receive 50 Shares
2.11%
500
11,210 2,130 out of 11,210 to receive 50 Shares
1.90%
600
1,005 205 out of 1,005 to receive 50 Shares
1.70%
700
524 117 out of 524 to receive 50 Shares
1.59%

<<<PAGE 25>>>
25
NO. OF 
SHARES 
APPLIED 
FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
PERCENTAGE 
ALLOTTED 
OF THE 
TOTAL NO. 
OF SHARES 
APPLIED FOR
800
487 117 out of 487 to receive 50 Shares
1.50%
900
324 82 out of 324 to receive 50 Shares
1.41%
1,000
3,456 899 out of 3,456 to receive 50 Shares
1.30%
1,500
1,372 486 out of 1,372 to receive 50 Shares
1.18%
2,000
1,188 513 out of 1,188 to receive 50 Shares
1.08%
2,500
1,115 569 out of 1,115 to receive 50 Shares
1.02%
3,000
609 358 out of 609 to receive 50 Shares
0.98%
3,500
455 293 out of 455 to receive 50 Shares
0.92%
4,000
371 261 out of 371 to receive 50 Shares
0.88%
4,500
297 227 out of 297 to receive 50 Shares
0.85%
5,000
1,147 918 out of 1,147 to receive 50 Shares
0.80%
6,000
724 669 out of 724 to receive 50 Shares
0.77%
7,000
408 400 out of 408 to receive 50 Shares
0.70%
8,000
313 310 out of 313 to receive 50 Shares
0.62%
9,000
233 50 Shares
0.56%
10,000
1,805 50 Shares plus 72 out of 1,805 to receive additional 50 Shares
0.52%
20,000
1,217 50 Shares plus 487 out of 1,217 to receive additional 50 Shares
0.35%
30,000
756 50 Shares plus 605 out of 756 to receive additional 50 Shares
0.30%
40,000
426 50 Shares plus 392 out of 426 to receive additional 50 Shares
0.24%
50,000
1,338 100 Shares
0.20%
Total
109,247 Total number of Pool A successful applicants: 23,238
POOL B
100,000
756 800 Shares
0.80%
150,000
106 900 Shares
0.60%
200,000
161 1,000 Shares
0.50%
400,000
42 2,000 Shares
0.50%
600,000
21 3,000 Shares
0.50%
800,000
5 4,000 Shares
0.50%
1,000,000
16 5,000 Shares
0.50%
1,306,600
32 6,200 Shares
0.47%
Total
1,139 Total number of Pool B successful applicants: 1,139

<<<PAGE 26>>>
26
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Allocations of Offer Shares to certain existing Shareholders and/or their close associates with 
a waiver from strict compliance with the requirements under Rule 9.09(b) and consent under 
paragraph 18 of Chapter 4.15 of the Guide as Cornerstone Investors
The Company has applied to, and the Stock Exchange has granted, a waiver from strict compliance 
with the requirements under Rule 9.09(b) and consent under paragraph 18 of Chapter 4.15 of 
the Guide for New Listing Applicants to permit the Company to allocate further Offer Shares to 
ZIJINNING, a close associate of an existing Shareholder, in the International Offering subject to 
the following conditions:
(1) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;
(2) 
the Offer Shares allocated to existing Shareholders and/or their close associates (whether 
as cornerstone investors and/or as placees) as permitted under the exemption granted by 
the Stock Exchange will not exceed 30% of the total number of H Shares offered under the 
Global Offering;
(3) 
the allocation to ZIJINNING and other existing Shareholders and/or their close associates 
(whether as cornerstone investors and/or as placees) will not affect the Company’s ability 
to satisfy its public float requirement as prescribed by the Stock Exchange under the waiver 
from strict compliance with the requirement of Rule 19A.13A(1) under the Listing Rules;
(4) 
each of the Directors, Supervisor, chief executives and Controlling Shareholders of the 
Company has confirmed that no Offer Shares will be allocated to any of them or their 
respective close associates under this exemption; and
(5) 
the details of allocation to ZIJINNING under the size-based exemption will be disclosed in 
this announcement.

<<<PAGE 27>>>
27
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
Please refer to the section headed “Waivers – Waiver under Rule 9.09(b) of, and consent under 
paragraph 1C(2) of Appendix F1 to, the Listing Rules and Paragraph 18 of Chapter 4.15 of 
the Guide for New Listing Applicants in respect of subscriptions for Offer Shares by close 
associates of existing Shareholders as Cornerstone Investors – (1) Subscription of Offer Shares 
by ZIJINNING as a Cornerstone Investor” in the Prospectus for further details of the waiver and 
consent.
Allocation of Offer Shares to certain existing Shareholders and/or their close associates with 
a waiver from strict compliance with the requirements under Rule 10.04 under the Listing 
Rules and/or consent under paragraph 1C(2) of the Placing Guidelines as Cornerstone 
Investors
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted to the 
Company, a consent under Rule 10.04 under the Listing Rules and/or Paragraph 1C(2) of Appendix 
F1 to the Listing Rules to permit Offer Shares in the International Offering to be placed to Fidelity 
International, a close associate of an existing Shareholder, in the International Offering on the 
conditions that:
(1) 
the cornerstone investment agreement with Fidelity International does not contain any 
material term which is more favourable to the existing Shareholder or its close associate than 
those in other cornerstone investment agreements;
(2) 
no preference in allocation was given to Fidelity International other than the assured 
entitlement for a Cornerstone Investor. The Company, the Sole Sponsor and the Overall 
Coordinators confirm that no preferential treatment has been, nor will be, given to Fidelity 
International by virtue of its relationships with the Company other than the assured 
entitlement for a Cornerstone Investor;
(3) 
the existing Shareholder, namely Tianjin Eight Roads, (i) has less than 5% voting rights in 
the Company before the Global Offering; (ii) is not a core connected person of the Company 
or its close associate; (iii) does not have the power to appoint directors or any other special 
rights;
(4) 
the proposed allocation to Fidelity International, a close associate of the existing Shareholder, 
will not affect the Company’s ability to satisfy its public float requirement as prescribed by 
the Stock Exchange under Rule 19A.13A(1) of the Listing Rules;
(5) 
each of the Company, the Sole Sponsor and the Overall Coordinators has provided the Stock 
Exchange with written confirmations in accordance with Chapter 4.15 of the Guide for New 
Listing Applicants; and
(6) 
the details of the allocations to Fidelity International will be disclosed in the Prospectus and/
or this announcement.
The allocation of Offer Shares to Fidelity International is in compliance with all the conditions 
under the waiver/consent granted by the Stock Exchange.

<<<PAGE 28>>>
28
Please refer to the section headed “Waivers – Waiver under Rule 9.09(b) of, and consent under 
paragraph 1C(2) of Appendix F1 to, the Listing Rules and Paragraph 18 of Chapter 4.15 of the 
Guide for New Listing Applicants in respect of subscriptions for Offer Shares by close associates 
of existing Shareholders as Cornerstone Investors – (2) Subscription of Offer Shares by Fidelity 
International as a Cornerstone Investor” in the Prospectus for further details of the waiver and 
consent.
Allocations of Offer Shares to certain existing Shareholders and Cornerstone Investors and/
or their close associates with a consent under Rule 9.09(b) under the Listing Rules and/or 
paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants as placees
The Company has applied to, and the Stock Exchange has granted, a consent under Rule 9.09(b) 
under the Listing Rules and/or paragraph 18 of Chapter 4.15 of the Guide for New Listing 
Applicants to permit the Company to allocate further Offer Shares in the International Offering to 
certain existing Shareholders and Cornerstone Investors and/or their close associates, subject to the 
following conditions (the “Allocation to Size-based Exemption Participants”):
(1) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;
(2) 
the Offer Shares allocated to all existing Shareholders and their close associates (whether 
as cornerstone investors and/or as placees) as permitted under the exemption granted by 
the Stock Exchange will not exceed 30% of the total number of H Shares offered under the 
Global Offering;
(3) 
the allocation to Size-based Exemption Participants will not affect the Company’s ability to 
satisfy its public float requirement as prescribed by the Stock Exchange under the waiver 
from strict compliance with the requirement of Rule 19A.13A(1) under the Listing Rules;
(4) 
each of the Directors, Supervisor, chief executives and Controlling Shareholders of the 
Company has confirmed that no Offer Shares will be allocated to any of them or their 
respective close associates under this exemption; and
(5) 
the details of allocation to the existing Shareholders and/or Cornerstone Investors and/or their 
close associates under the size-based exemption will be disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to existing Shareholders and Cornerstone Investors 
and/or their close associates, please refer to the section headed “Allotment Results Details – 
International Offering – Allottees with Waivers/Consents Obtained” in this announcement.

<<<PAGE 29>>>
29
Allocations of Offer Shares to certain existing Shareholders and/or their close associates with 
a consent under Rule 10.04 under the Listing Rules and/or paragraph 1C(2) of the Placing 
Guidelines pursuant to the fulfillment of Existing Shareholders Conditions and grounds as 
placees
The Company has applied to, and the Stock Exchange has granted, a consent under Rule 10.04 
under the Listing Rules and/or paragraph 1C(2) of the Placing Guidelines pursuant to the 
fulfillment of Existing Shareholders Conditions and grounds as follows:
(1) 
no preference in allocation was given to the existing Shareholders and/or their close 
associates. The Company, the Sole Sponsor and the Overall Coordinators confirm that no 
preferential treatment has been, nor will be, given to the existing Shareholder or its close 
associate by virtue of their relationships with the Company;
(2) 
each of the relevant existing Shareholders (i) has less than 5% voting rights in the Company 
before the Global Offering; (ii) is not a core connected person of the Company or its close 
associate; (iii) does not have the power to appoint directors or any other special rights;
(3) 
the proposed allocation to the existing Shareholders and/or their close associates will not 
affect the Company’s ability to satisfy its public float requirement as prescribed by the Stock 
Exchange under Rule 19A.13A(1) of the Listing Rules;
(4) 
each of the Company, the Sole Sponsor and the Overall Coordinators has provided the Stock 
Exchange with written confirmations in accordance with Chapter 4.15 of the Guide for New 
Listing Applicants; and
(5) 
the details of allocation to such existing Shareholders and/or their close associates will be 
disclosed in the allotment results announcement of the Company.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates, 
please refer to the section headed “Allotment Results Details – International Offering – Allottees 
with Waivers/Consents Obtained” in this announcement.
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines as placees
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines as placees. Please refer to the section 
headed “Allotment Results Details – International Offering – Allottees with Waivers/Consents 
Obtained” in this announcement for details.

<<<PAGE 30>>>
30
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such 
Offer Shares in the International Offering to the connected clients as placees. The allocation of 
Offer Shares to such connected clients is in compliance with all the conditions under the consent 
granted by the Stock Exchange. Details of the placement to connected clients as placees are set out 
below:
No.
Connected
Distributor
Connected
Client
Relationship
Identities of the 
ultimate beneficial 
owners of the 
Offer Shares or, 
where applicable, 
details of the 
structured products 
under which the 
subscription by the 
Connected Client 
was made (e.g. OTC 
total return swaps)
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
on behalf of such 
scheme
Amount 
of Offer 
Shares to 
be allocated 
to the 
Connected 
Client
Approximate 
percentage 
of total 
number of 
Offer Shares 
under the 
Global 
Offering
Approximate 
percentage 
of total 
issued share 
capital after 
the Global
Offering
Part A – Connected Client holding the beneficial interest of the Offer Shares on a non-discretionary basis on behalf of independent third parties
1.
Haitong International 
Securities Company 
Limited (“Haitong 
Securities”)
GTINV(1)
GTINV is a member 
of the same group of 
Haitong Securities
Note (1) below
N
1,765,000
6.76%
1.19%
Part B – Connected Client holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties
1.
Haitong Securities
Fullgoal HK(2)
Fullgoal HK is a member 
of the same group 
companies as Haitong 
Securities
Note (2) below
N
4,750
0.02%
0.0032%
Notes:
(1). 
Haitong Securities is the Sponsor-Overall Coordinator in connection with the Global Offering. GTINV shall 
hold the Offer Shares for hedging purpose as the single underlying asset of several sets of back-to-back total 
return swap transaction (the “GTHT Back-to-back TRS”) to be entered into between GTINV and Guotai 
Haitong Securities Co., Ltd. (the “GTHT Onshore Parent”) in connection with several total return swap 
orders (the “GTHT Client TRS”) to be entered into by GTHT Onshore Parent and several ultimate clients (the 
“GTHT Onshore Ultimate Clients”), respectively. Such GTHT Client TRS is to be fully funded by the GTHT 
Onshore Ultimate Clients. GTINV will hold the Offer Shares on a non-discretionary basis for the purpose of 
hedging the economic exposure under the GTHT Back-to-back TRS and GTHT Client TRS only. During the 
tenor of the GTHT Client TRS, all economic returns of the Offer Shares will be passed to the GTHT Onshore 
Ultimate Clients and all economic losses shall be borne by the GTHT Onshore Ultimate Clients, subject to the 
terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS, and GTINV will not take part in 
any economic return or bear any economic loss in relation to the price of the Offer Shares. The GTHT Onshore 
Ultimate Clients may request to redeem the Offer Shares at their own discretion, upon which GTINV shall 
dispose of the Offer Shares and settle the GTHT Back-to-back TRS and GTHT Client TRS in cash in accordance 
with the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS documents. Due to its 
internal policy, GTINV will not exercise the voting right attaching to the Offer Shares during the tenor of the 
GTHT Back-to-back TRS and GTHT Client TRS.

<<<PAGE 31>>>
31
Identities of the ultimate beneficial owners of the H Shares allotted to GTINV are set forth below
Applicant 
name
Beneficial owner
Number of
H Shares
Allocated
Ultimate Beneficial owner(s)
GTINV
Chentao Xinnuo Private Securities 
Investment Fund (辰韜信諾私募證券
投資基金) (“Chentao Xinnuo”)(a)
789,850
No entity holds 30% or more of the 
interests in Chentao Xinnuo, nor does 
it have any general partners or limited 
partners
Shanghai Jingshi Investment 
Management Center (Limited 
Partnership) (上海經石投資管理中心
(有限合夥))(b)
712,950
Zhang Guansheng (張冠生) 
XCMG Construction Machinery Co., 
Ltd. (000425.SZ)
Zhongcheng Runzhi Hexing No. 3 
Private Securities Investment Fund 
(中鋮潤智合興 3 號私募證券投資基
金) (“Zhongcheng Runzhi”)(c)
262,700
No entity holds 30% or more of the 
interests in Zhongcheng Runzhi, nor 
does it have any general partners or 
limited partners
(a) 
Chentao Xinnuo is a private securities investment fund registered under the Asset Management 
Association of China (私募證券投資基金(受託管理)), which is a segregated account under the 
discretionary management of its fund manager, Hangzhou Chentao Asset Management Co., Ltd. (杭州
辰韜資產管理有限公司) (“Hangzhou Chentao”). Hangzhou Chentao is a wholly-owned subsidiary of 
Shanghai Chentao Asset Management Co., Ltd. (上海辰韜資產管理有限公司) (“Shanghai Chentao”), 
a substantial shareholder of the Company as defined under the Listing Rules, which is held by Xu 
Haiying (徐海英) and Lin Xinzheng (林新正) as to 51.2% and 48.8%, respectively. Chentao Xinnuo is, 
accordingly, a core connected person of the Company and a close associate of an existing Shareholder of 
the Company.
The Stock Exchange has also granted the consent under paragraph 18 of Chapter 4.15 of the Guide in 
relation to allocations of H Shares to Chentao Xinnuo, a close associate of an existing Shareholder. For 
details, see “International Offering — Allottees with Waivers/ Consents Obtained” in this announcement.
(b) 
Shanghai Jingshi Investment Management Center (Limited Partnership) (上海經石投資管理中心(有限
合夥)) (“Shanghai Jingshi”) is held by Xuzhou XCMG Industrial Investment Partnership Enterprise 
(Limited Partnership) (徐州徐工產業投資合夥企業(有限合夥)) (“Xuzhou XCMG IM”) as to 99.9652% 
as its sole limited partner and by Mr. Zhang Guansheng (張冠生), an Independent Third Party, as to 
0.0348% as its general partner. Xuzhou XCMG IM is held by the listed company XCMG Construction 
Machinery Co., Ltd. (000425.SZ) as to 99.99% as its sole limited partner. No other entity ultimately 
holds 30% or more interest in Shanghai Jingshi.
(c) 
Zhongcheng Runzhi is a private securities investment fund registered under the Asset Management 
Association of China (私募證券投資基金(受託管理)), which is a segregated account under the 
discretionary management of its fund manager, Zhongcheng Runzhi Asset Management (Shanghai) 
Co., Ltd. (中鋮潤智資產管理(上海)有限公司), which is held by Chen Zongyan (陳宗彥) and Zhang 
Shanliang (張珊涼) as to 51% and 49%, respectively. Both of Chen Zongyan and Zhang Shanliang are 
Independent Third Parties.
To the best knowledge of GTINV and after making all reasonable enquiries, (i) GTINV has confirmed that, 
to the best of its knowledge, each of the GTHT Onshore Ultimate Clients and the ultimate beneficial owners 
holding 30% or more interest of the GTHT Onshore Ultimate Clients is an independent third party of GTINV, 
Haitong Securities and the companies which are members of the same group of companies as Haitong Securities 
and (ii) GTINV is not a collective investment scheme which is not authorized by the SFC nor is expected to 
hold the Offer Shares on behalf of such scheme.
(2). 
Fullgoal HK will hold the Offer Shares in its capacity as the discretionary fund manager on behalf of its 
investors, each of which is an independent third party of the Company, its subsidiaries, its Controlling 
Shareholders, its substantial Shareholders, Fullgoal HK, Haitong Securities and the companies which are 
members of the same group of Haitong Securities. No ultimate beneficial owner holds 30% or more interest in 
the underlying investors. None of the shareholder holds 30% or more interest in Fullgoal HK.

<<<PAGE 32>>>
32
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
(the “Hong Kong Stock Exchange”) and Hong Kong Securities Clearing Company Limited 
(“HKSCC”) take no responsibility for the contents of this announcement, make no representation 
as to its accuracy or completeness and expressly disclaim any liability whatsoever for any 
loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and the 
District of Columbia). This announcement does not constitute, and is not intended to constitute, 
or form a part of any offer or solicitation to purchase or subscribe for securities in the United 
States or in any other jurisdictions. The securities mentioned herein have not been, and will not 
be, registered under the United States Securities Act of 1933, as amended from time to time (the 
“U.S. Securities Act”) or securities law of any state or other jurisdiction of the United States. 
The securities may not be offered, sold, pledged or otherwise transferred within the United States 
except pursuant to an exemption from the registration requirements of the U.S. Securities Act 
and in compliance with any applicable state securities laws. There will be no public offer of the 
Offer Shares in the United States. The Offer Shares are being offered and sold solely outside the 
United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act 
and applicable laws of each jurisdiction where those offers and sales occur.
The Offer Shares are being offered and sold outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated June 29, 2026 (the “Prospectus”) issued by EACON 
Group Co., Ltd (易控智駕科技股份有限公司) (the “Company”) for detailed information about 
the Global Offering described below before deciding whether or not to invest in the H Shares 
thereby being offered. Any investment decision in relation to the Offer Shares should be taken 
solely in reliance on the information in the Prospectus. The Company has not been and will not 
be registered under the U.S. Investment Company Act of 1940, as amended.
* Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinator (for 
itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate its obligations 
under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of 
any of the events set out in the section headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus at any 
time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be 
on Wednesday, July 8, 2026).

<<<PAGE 33>>>
33
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering (assuming no exercise of the 
Over-Allotment Option), the number of the H Shares to be held by the public represents 
approximately 44.88% of the total issued share capital of our Company. Based on the final Offer 
Price of HK$87.92 per H Share, the expected market capitalization of the Company upon Listing 
would be approximately HK$13.0 billion, and the percentage that would result in the expected 
market value of H Shares held by the public to be HK$1.5 billion at the time of Listing is 
approximately 11.54%. Accordingly, the minimum prescribed public float percentage applicable to 
our H Shares under Rule 19A.13A(1) of the Listing Rules is 15%. Therefore, the Company satisfies 
the minimum public float requirement under Rule 19A.13A of the Listing Rules as over 15% of the 
Company’s total issued Shares will be held by the public upon completion of the Global Offering.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the H Shares of the Company at the time of Listing. Based on the 
final Offer Price of HK$87.92 per H Share, the Company satisfies the free float requirement under 
Rule 8.08A (as amended and replaced by Rule 19A.13C(1)(b) of the Listing Rules).
The Directors confirm that, immediately following completion of the Global Offering (before any 
exercise of the Over-Allotment Option): (i) the Shares will be held by at least 300 Shareholders at 
the time of Listing, in compliance with Rule 8.08(2) under the Listing Rules; (ii) the three largest 
public Shareholders will not hold more than 50% of the H Shares held in public hands at the time 
of Listing, in compliance with Rules 8.08(3) and 8.24 under the Listing Rules; (iii) no placee 
will, individually, be placed more than 10% of the enlarged issued share capital of the Company 
immediately after the Global Offering; and (iv) there will not be any new substantial Shareholder 
(as defined in the Listing Rules) immediately after the Global Offering.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, July 
8, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting” in the Prospectus has not been 
exercised. Investors who trade H Shares prior to the receipt of H Share certificates or the H Share 
certificates becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. in Hong Kong on 
Wednesday, July 8, 2026, it is expected that dealings in the H Shares on the Stock Exchange will 
commence at 9:00 a.m. on Wednesday, July 8, 2026. The H Shares will be traded in board lots of 
50 H Shares each and the stock code of the H Shares will be 7687.

<<<PAGE 34>>>
34
This announcement is available for viewing on the website of the Company at www.eacon.com 
and the website of the Hong Kong Stock Exchange at www.hkexnews.hk.
By order of the Board
EACON Group Co., Ltd
Lan Shuisheng
Co-chairman of the Board, executive Director, 
general manager and chief executive officer
Hong Kong, July 7, 2026
As of the date of this announcement, the Board comprises: (i) Mr. Lan Shuisheng, Mr. Zhang 
Lei, Dr. Lin Qiao, Dr. Chen Huiyong and Ms. Qu Xiaoyan as executive Directors; (ii) Mr. Lai 
Shengmin as a non-executive Director; and (iii) Dr. Gong Yan, Dr. Han Jian and Mr. Wong Yu 
Shan Eugene as proposed independent non-executive Directors.
