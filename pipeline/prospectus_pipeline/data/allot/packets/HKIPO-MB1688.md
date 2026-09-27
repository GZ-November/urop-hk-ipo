# 配发结果公告抽取任务：1688.HK LINGYI iTECH (GUANGDONG) COMPANY - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**25/06/2026 22:41**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0625/2026062502292.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1688.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for the Offer 
Shares in the United States or in any other jurisdictions. The Offer Shares have not been, and will not be, registered 
under the United States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or securities 
law of any state or other jurisdiction of the United States. The Offer Shares may not be offered, sold, pledged or 
otherwise transferred within the United States, except pursuant to an exemption from the registration requirements 
of the U.S. Securities Act, and in compliance with any applicable state securities laws. The Offer Shares are being 
offered and sold outside the United States to investors that are not U.S. persons nor persons acquiring for the account 
or benefit of U.S. persons in reliance on Regulation S under the U.S. Securities Act. There will be no public offer of 
the Offer Shares in the United States.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
June 17, 2026 (the “Prospectus”) issued by LINGYI iTECH (GUANGDONG) COMPANY (廣東領益智造股份有限
公司) (the “Company”) for detailed information about the Global Offering described below before deciding whether 
or not to invest in the H Shares thereby being offered. Any investment decision in relation to the Offer Shares should 
be taken solely in reliance on the information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on behalf of 
the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
Friday, June 26, 2026).

<<<PAGE 2>>>
2
LINGYI iTECH (GUANGDONG) COMPANY
廣東領益智造股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the 
Global Offering
:
811,811,880 H Shares
Number of Hong Kong Offer Shares
:
81,181,320 H Shares
Number of International Offer Shares
:
730,630,560 H Shares
Final Offer Price
:
HK$10.18 per H Share, plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
AFRC transaction levy of 0.00015% and 
Stock Exchange trading fee of 0.00565% 
(payable in full on application in Hong 
Kong dollars and subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
1688
Sole Sponsor, Sole Sponsor-Overall Coordinator, Overall Coordinator,  
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and  
Joint Lead Managers
Joint Bookrunners and Joint Lead Managers 
(in alphabetical order)

<<<PAGE 3>>>
3
LINGYI iTECH (GUANGDONG) COMPANY
廣東領益智造股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated June 17, 2026 (the “Prospectus”) issued by 
Lingyi iTech (Guangdong) Company (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
H Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company Information
Stock Code
1688
Stock short name
LINGYI ITECH
Dealings commencement date
June 26, 2026
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$10.18
Maximum Offer Price
HK$10.18
Offer Shares and Share Capital
Number of Offer Shares
811,811,880
Final Number of Offer Shares in Hong Kong Public Offering
81,181,320
Final Number of Offer Shares in International Offering
730,630,560
Number of issued Shares upon Listing
8,120,010,560
Note: Including 34,031,200 A Shares repurchased by the Company pursuant to the repurchase mandates approved 
by the Board. The number of issued Shares upon Listing did not take into account any additional A Shares to 
be issued under the 2024 Share Option Scheme (if any).
Proceeds
Gross proceeds (Note)
HK$8,264.2 million
Less: Estimated listing expenses payable based on Final Offer Price
HK$112.6 million
Net proceeds
HK$8,151.7 million
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.

<<<PAGE 4>>>
4
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
162,822
No. of successful applications
33,279
Subscription level
96.16 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong Public Offering
81,181,320
Final no. of Offer Shares under the Hong Kong Public Offering
81,181,320
% of Offer Shares initially available under the Hong Kong 
Public Offering to the Global Offering
10%
% of final no. of Offer Shares under the Hong Kong 
Public Offering to the Global Offering
10%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer 
to www.eipo.com.hk/eIPOAllotment to perform a search by identification document number or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
152
Subscription Level
10.27
No. of Offer Shares initially available under the International Offering
730,630,560
Final no. of Offer Shares under the International Offering
730,630,560
% of Offer Shares initially available under the 
International Offering to the Global Offering
90%
% of final no. of Offer Shares under the International 
Offering to the Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for a 
waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit the Company to allocate certain Offer Shares in the International Offering to 
certain Existing Minority A Shareholders and/or their close associates, (i) none of the Offer Shares 
subscribed by the placees and the public have been financed directly or indirectly by the Company, 
any of the Directors, chief executive of the Company, Controlling Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates; and (ii) none of the placees and the public who have purchased the Offer Shares 
are accustomed to taking instructions from the Company, any of the Directors, chief executive of 
the Company, Controlling Shareholders, substantial Shareholders, existing Shareholders of the 
Company or any of its subsidiaries or their respective close associates in relation to the acquisition, 
disposal, voting or other disposition of H Shares registered in his/her/its name or otherwise held by 
him/her/it.

<<<PAGE 5>>>
5
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after 
the Global 
Offering Note 2
% of total issued 
share capital in 
the Company 
after the Global 
Offering (without 
taking into 
account any 
additional A 
Shares to be 
issued under 
the 2024 
Share Option 
Scheme) Note 3
Existing 
Minority A 
Shareholders 
or their close 
associates
GF Fund Management Co., Ltd. （廣發基金管理有限公司）  
(“GF Fund Management”)
24,634,500
3.03%
0.30%
Yes
GF International Investment Management Limited （廣發國際
資產管理有限公司） (“GF Fund HK”, together with GF Fund 
Management, “GF Fund”)
7,698,240
0.95%
0.09%
Kaide Global Investment Ltd (“Kaide Global Investment”)
24,634,500
3.03%
0.30%
No
Qube Master Fund Ltd, acting by its sub-investment manager 
Qube Research & Technologies Hong Kong Limited (“Qube”)
23,094,720
2.84%
0.28%
No
Ti-Capital (HK) Pioneer Fund III and Ti-Capital (HK) Pioneer 
Fund IV (collectively, “Ti-Capital Funds”)
23,094,720
2.84%
0.28%
No
Value Partners Hong Kong Limited
18,860,820
2.32%
0.23%
No
Value Partners Limited
4,233,900
0.52%
0.05%
No
Hongxing International Technology Limited （宏興國際科技有限
公司） (“Hongxing International”)
23,094,720
2.84%
0.28%
No
Morgan Stanley & Co. International plc (“MSIP”)
23,017,500
2.84%
0.28%
Yes
Greenwoods Asset Management Hong Kong Limited, as the 
investment manager of Golden China Master Fund (“HK 
Greenwoods”)
17,705,820
2.18%
0.22%
No
3W Fund Management Limited (“3W Fund”)
15,396,480
1.90%
0.19%
No
Deliante Holdings Co., Ltd. (“Deliante”)
15,396,480
1.90%
0.19%
No
Sunny Optical Capital Limited （舜宇資本有限公司）  
(“Sunny Optical Capital”)
15,396,480
1.90%
0.19%
No

<<<PAGE 6>>>
6
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after 
the Global 
Offering Note 2
% of total issued 
share capital in 
the Company 
after the Global 
Offering (without 
taking into 
account any 
additional A 
Shares to be 
issued under 
the 2024 
Share Option 
Scheme) Note 3
Existing 
Minority A 
Shareholders 
or their close 
associates
Honor Information Technology Co., Limited （榮耀信息 
技術有限公司） (“Honor”) Note 1
11,547,360
1.42%
0.14%
Yes
Jain Global Master Fund Ltd, acting through its investment 
manager Jain Global LLC (“Jain Global”)
11,547,360
1.42%
0.14%
No
Seven Grand Managers, LLC (“Seven Grand”)
11,547,360
1.42%
0.14%
No
Taikang Life Insurance Co., Ltd （泰康人壽保險 
有限責任公司） (“Taikang Life”)
11,547,360
1.42%
0.14%
Yes
Da Cheng International Asset Management Company Limited 
(“Da Cheng International”)
7,698,240
0.95%
0.09%
Yes
Everbright Wealth Management Co., Ltd. （光大理財有限 
責任公司） (“Everbright Wealth Management”)
7,698,240
0.95%
0.09%
No
GRANITE ASIA IX VCC (for the account of and on behalf of 
GX ACCESS, “GRANITE ASIA”)
7,698,240
0.95%
0.09%
No
Verition Multi-Strategy Master Fund Ltd., managed by  
Verition Fund Management LLC (“Verition”)
7,698,240
0.95%
0.09%
No
Total
313,241,280
38.59%
3.86%

<<<PAGE 7>>>
7
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after 
the Global 
Offering Note 2
% of total issued 
share capital in 
the Company 
after the Global 
Offering (without 
taking into 
account any 
additional A 
Shares to be 
issued under 
the 2024 
Share Option 
Scheme) Note 3
Existing 
Minority A 
Shareholders 
or their close 
associates
Notes:
1. 
Honor Information Technology Co., Limited is the official English name of Honor, which refers to the same 
entity as Honor Information Technology Limited (榮耀信息技術有限公司) as disclosed in the Prospectus. 
The difference of the English name was due to inadvertent translation error, which does not affect the validity 
of the relevant cornerstone investment agreement entered by Honor, nor will it affect the potential investors’ 
assessment of the identity of the cornerstone investor.
2. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be 
issued under the Global Offering.
3. 
Only taking into account the H Shares allocated to the relevant investors as cornerstone investors under the 
Global Offering. In addition to the Offer Shares subscribed for as Cornerstone Investors, certain Cornerstone 
Investors or their close associates, namely GF Fund Management, GF Fund HK, Kaide Global Investment, 
Qube, Ti-Capital Funds, Value Partners Limited, MSIP, HK Greenwoods, Shanghai Greenwoods Asset 
Management Co., Ltd. (“Shanghai Greenwoods”, a close associate of HK Greenwoods, one of the Cornerstone 
Investors), 3W Fund, Sunny Optical Capital, Honor, Jain Global, Seven Grand, Taikang Life, Da Cheng 
International, Everbright Wealth Management, GRANITE ASIA and Verition, were allocated further Offer 
Shares as placees in the International Offering. Please refer to the section headed “Allotment Results Details 
– International Offering – Allotees with Waivers/Consents Obtained” in this announcement for details. Only 
the Offer Shares subscribed for as Cornerstone Investors are subject to lock-up as indicated below. For details, 
please refer to the section headed “Lock-up Undertakings – Cornerstone Investors” in this announcement.

<<<PAGE 8>>>
8
Allotees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after 
the Global 
Offering Note 5
% of total issued 
share capital in 
the Company 
after the 
Global Offering 
(without taking 
into account 
any additional 
A Shares to be 
issued under 
the 2024 
Share Option 
Scheme) Note 1
Relationship
Allotees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further H 
Shares to existing Shareholders and Cornerstone Investors and/or their close associates Note 1
GF Fund Management
21,170,160
2.61%
0.26%
Same entity as the Cornerstone 
Investor, which is also an Existing 
Minority A Shareholder
GF Fund HK
11,161,920
1.37%
0.14%
Same entity as the Cornerstone 
Investor, which is also a close 
associate of Existing Minority A 
Shareholder
Kaide Global Investment
49,269,000
6.07%
0.61%
Same entity as the Cornerstone 
Investor
Qube
12,305,700 
1.52%
0.15%
Same entity as the Cornerstone 
Investor
Ti-Capital Funds
23,094,060
2.84%
0.28%
Same entity as the Cornerstone 
Investor
Value Partners Limited
12,305,040
1.52%
0.15%
Same entity as the Cornerstone 
Investor
MSIP
17,706,480
2.18%
0.22%
Same entity as the Cornerstone 
Investor, which is also an Existing 
Minority A Shareholder 
HK Greenwoods
17,707,800
2.18%
0.22%
Same entity as the Cornerstone 
Investor
Shanghai Greenwoods Asset Management 
Co., Ltd. (“Shanghai Greenwoods”) as 
one of the GTHT Onshore Ultimate Clients 
(as defined below)
4,614,720
0.57%
0.06%
Close associate of HK Greenwoods, 
one of the Cornerstone Investors
3W Fund
7,775,460
0.96%
0.10%
Same entity as the Cornerstone 
Investor

<<<PAGE 9>>>
9
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after 
the Global 
Offering Note 5
% of total issued 
share capital in 
the Company 
after the 
Global Offering 
(without taking 
into account 
any additional 
A Shares to be 
issued under 
the 2024 
Share Option 
Scheme) Note 1
Relationship
Want Power Holdings Limited
9,237,360
1.14%
0.11%
Close associate of Deliante, one of 
the Cornerstone Investors Note 2
Sunny Optical Capital
769,560
0.09%
0.01%
Same entity as the Cornerstone 
Investor
Honor
11,547,360
1.42%
0.14%
Same entity as the Cornerstone 
Investor, which is also a close 
associate of Existing Minority A 
Shareholder 
Jain Global
5,388,900
0.66%
0.07%
Same entity as the Cornerstone 
Investor
Seven Grand
5,388,900
0.66%
0.07%
Same entity as the Cornerstone 
Investor
Taikang Life
3,849,780
0.47%
0.05%
Same entity as the Cornerstone 
Investor, which is also an Existing 
Minority A Shareholder
Da Cheng International
2,309,340
0.28%
0.03%
Same entity as the Cornerstone 
Investor, which is also a close 
associate of Existing Minority A 
Shareholder
Everbright Wealth Management
2,309,340
0.28%
0.03%
Same entity as the Cornerstone 
Investor Note 3
GRANITE ASIA
2,309,340
0.28%
0.03%
Same entity as the Cornerstone 
Investor
Verition
2,309,340 
0.28%
0.03%
Same entity as the Cornerstone 
Investor

<<<PAGE 10>>>
10
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after 
the Global 
Offering Note 5
% of total issued 
share capital in 
the Company 
after the 
Global Offering 
(without taking 
into account 
any additional 
A Shares to be 
issued under 
the 2024 
Share Option 
Scheme) Note 1
Relationship
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation 
to allocations to connected clients as placees Note 4
Shanghai Guotai Haitong Securities 
Asset Management Co., Ltd. (“Shanghai 
Guotai”)
47,520
0.006%
0.0006%
Connected client
Fullgoal Fund Management Co., Ltd. 
(“Fullgoal Fund”)
192,060
0.02%
0.002%
Connected client
China Asset Management (Hong Kong) 
Limited (“China AMC HK”)
95,700
0.01%
0.001%
Connected client
CITIC Securities Asset Management 
Company Limited (“CITIC Asset 
Management”)
3,300
0.0004%
0.0000%
Connected client
CITIC Securities Asset management (HK) 
Limited (“CITIC Asset Management 
HK”)
3,300
0.0004%
0.0000%
Connected client
UBS Asset Management (Singapore) 
Limited (“UBS AM”)
384,780
0.05%
0.005%
Connected client
HSBC Global Asset Management (Hong 
Kong) Limited (“HSBC AM”)
18,480
0.002%
0.0002%
Connected client

<<<PAGE 11>>>
11
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after 
the Global 
Offering Note 5
% of total issued 
share capital in 
the Company 
after the 
Global Offering 
(without taking 
into account 
any additional 
A Shares to be 
issued under 
the 2024 
Share Option 
Scheme) Note 1
Relationship
Guotai Junan Investments (Hong Kong) 
Limited (“GTJAI”)
91,027,200
11.21%
1.12%
Connected client
CITIC Securities International Capital 
Management Limited (“CSI”)
4,518,360
0.56%
0.06%
Connected client
Notes:
1. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details – International Offering – Cornerstone Investors” in this announcement. For details of the 
consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further H 
Shares to the Cornerstone Investors, please refer to the section headed “Others/Additional Information – 
Allocations of Offer Shares to the Cornerstone Investors with a consent under Chapter 4.15 of the Guide for 
New Listing Applicants” in this announcement.
2. 
Deliante is non-discretionary investment holding company which is used to hold financial assets such as 
stocks and bonds for a family trust established by Mr. Tsai Eng-Meng (“Mr. Tsai”), as settlor for the benefit 
of Mr. Tsai and his family members. Mr. Tsai is also the ultimate beneficial owner of Want Power Holdings 
Limited. Therefore, Want Power Holdings Limited is a close associate of Deliante.
3. 
Everbright Wealth Management’s investment into the Company would be made and completed through 
QDII program in the PRC, of which it has engaged GF Securities Asset Management (Guangdong) Co., Ltd. 
(廣發証券資產管理(廣東)有限公司) (“GF Asset Management”). CEB-GFAM GSJXCL NO.1 ASSET 
MANAGEMENT AC (廣發資管光石精選策略 1 號集合資產管理計劃) is the QDII product account managed 
by GF Asset Management, through which the subscription of the Company’s shares would be executed on 
behalf of Everbright Wealth Management.
4. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients, please refer to the section headed 
“Others/Additional Information – Placing to connected clients with a prior consent under paragraph 1C(1) of 
the Placing Guidelines” in this announcement.
5. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.

<<<PAGE 12>>>
12
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
A Shares held 
in the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
share capital in 
the Company 
subject to lock-
up undertakings 
upon Listing 
(without taking 
into account 
any additional 
A Shares to be 
issued under 
the 2024 
Share Option 
Scheme) Note 1
Last day subject to the 
lock-up undertakings Note 2
Ms. Zeng Fangqin (曾芳勤) 
(“Ms. Zeng”)
108,536,846
1.34%
December 25, 2026 (First Six-month 
Period) Note 3 
June 25, 2027 (Second Six-month 
Period) Note 4
Lingsheng Investment (Jiangsu) Co., 
Ltd. (領勝投資(江蘇)有限公司) 
(“Lingsheng Investment”)
4,139,524,021
50.98%
December 25, 2026 (First Six-month 
Period) Note 3 
June 25, 2027 (Second Six-month 
Period) Note 4
Total
4,248,060,867
52.32%
Notes:
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
2. 
In accordance with the applicable Listing Rules, the required lock-up for the first six-month period will end 
on December 25, 2026 and for the second six-month period will end on June 25, 2027.
3. 
The Controlling Shareholders may dispose of or transfer Shares after the indicated date subject to that each of 
the Controlling Shareholders will not cease to be a Controlling Shareholder.
4. 
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after the 
indicated date.
5. 
For illustrative purposes only, this subsection lists only the Controlling Shareholders who hold Shares directly 
in the Company. Pursuant to Rule 10.07 of the Listing Rules and the Hong Kong Underwriting Agreement, 
the Controlling Shareholders (namely, Ms. Zeng and Lingsheng Investment) have undertaken to the Company 
and the Stock Exchange that, except pursuant to the Global Offering, they shall, and shall procure that 
the relevant registered holder(s) of the Shares in which they are beneficially interested shall, comply with 
the applicable lock-up requirements. For further details, please refer to the section headed “Underwriting 
— Underwriting Arrangements and Expenses – Undertakings to the Stock Exchange pursuant to the 
Listing Rules — (B) Undertakings by the Controlling Shareholders” and “Underwriting — Underwriting 
Arrangements and Expenses — Undertakings pursuant to the Hong Kong Underwriting Agreement — (B) 
Undertakings by the Controlling Shareholders” in the Prospectus.

<<<PAGE 13>>>
13
Cornerstone Investors
Name
Number of 
H Shares held in 
the Company 
subject to lock-up 
undertakings 
upon Listing
% of total issued 
share capital in 
the Company 
subject to lock-up 
undertakings upon 
Listing (without 
taking into account 
any additional A 
Shares to be issued 
under the 2024 Share 
Option Scheme) Note 1
Last day subject 
to the lock-up 
undertakings Note 2
GF Fund Management
24,634,500
0.30%
December 25, 2026
GF Fund HK
7,698,240
0.09%
December 25, 2026
Kaide Global Investment
24,634,500
0.30%
December 25, 2026
Qube
23,094,720
0.28%
December 25, 2026
Ti-Capital Funds
23,094,720
0.28%
December 25, 2026
Value Partners Hong Kong 
Limited
18,860,820
0.23%
December 25, 2026
Value Partners Limited
4,233,900
0.05%
December 25, 2026
Hongxing International
23,094,720
0.28%
December 25, 2026
MSIP
23,017,500
0.28%
December 25, 2026
HK Greenwoods
17,705,820
0.22%
December 25, 2026
3W Fund
15,396,480
0.19%
December 25, 2026
Deliante
15,396,480
0.19%
December 25, 2026
Sunny Optical Capital
15,396,480
0.19%
December 25, 2026
Honor
11,547,360
0.14%
December 25, 2026
Jain Global
11,547,360
0.14%
December 25, 2026
Seven Grand
11,547,360
0.14%
December 25, 2026
Taikang Life
11,547,360
0.14%
December 25, 2026
Da Cheng International
7,698,240
0.09%
December 25, 2026
Everbright Wealth 
Management
7,698,240
0.09%
December 25, 2026

<<<PAGE 14>>>
14
Name
Number of 
H Shares held in 
the Company 
subject to lock-up 
undertakings 
upon Listing
% of total issued 
share capital in 
the Company 
subject to lock-up 
undertakings upon 
Listing (without 
taking into account 
any additional A 
Shares to be issued 
under the 2024 Share 
Option Scheme) Note 1
Last day subject 
to the lock-up 
undertakings Note 2
GRANITE ASIA
7,698,240
0.09%
December 25, 2026
Verition
7,698,240
0.09%
December 25, 2026
Total
313,241,280
3.86%
Notes:
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
2. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on December 
25, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or transferring H Shares 
subscribed pursuant to the relevant cornerstone investment agreements after the indicated date.
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering
Allotment as % 
of total Offer 
Shares
Number of H 
Shares held 
upon Listing
% of total 
issued H share 
capital upon 
Listing
% of total 
issued share 
capital upon 
Listing 
(without taking 
into account 
any additional 
A Shares to 
be issued 
under the 2024 
Share Option 
Scheme)
Top 1
73,903,500
10.12
9.10
73,903,500
9.10
0.91
Top 5
274,694,640
37.60
33.84
274,694,640
33.84
3.38
Top 10
435,638,940
59.63
53.66
435,638,940
53.66
5.37
Top 25
657,860,940
90.04
81.04
657,860,940
81.04
8.10
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 15>>>
15
H SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders* 
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering
Allotment as % 
of total Offer 
Shares
Number of 
H Shares held 
upon Listing
% of total 
issued H share 
capital upon 
Listing
% of total 
issued share 
capital upon 
Listing 
(without taking 
into account 
any additional 
A Shares to 
be issued 
under the 2024 
Share Option 
Scheme)
Top 1
73,903,500
10.12
9.10
73,903,500
9.10
0.91
Top 5
274,694,640
37.60
33.84
274,694,640
33.84
3.38
Top 10
435,638,940
59.63
53.66
435,638,940
53.66
5.37
Top 25
657,860,940
90.04
81.04
657,860,940
81.04
8.10
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering
Allotment as % 
of total Offer 
Shares
Number of 
H Shares held 
upon Listing
Number of 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing 
(without taking 
into account 
any additional 
A Shares to 
be issued 
under the 2024 
Share Option 
Scheme)
Top 1
–
–
–
–
4,248,060,867
52.32
Top 5
74,017,680
10.13
9.12
74,017,680
4,677,657,478
57.61
Top 10
274,808,820
37.61
33.85
274,808,820
4,928,607,697
60.70
Top 25
535,834,860
73.34
66.00
543,532,440
5,326,838,148
65.60
Note:
* 
Ranking of Shareholders is based on the aggregate of, where applicable, the number of H Shares held by the 
Shareholders upon Listing.

<<<PAGE 16>>>
16
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
Pool A
Approximate
percentage
allotted of the
Number of
Number
total number of
H Shares
of valid
H Shares applied
applied for
applications
Basis of allocation/ballot
for
660
71,596
879 out of 71,596 to receive 660 Shares
1.23%
1,320
10,594
260 out of 10,594 to receive 660 Shares
1.23%
1,980
3,716
137 out of 3,716 to receive 660 Shares
1.23%
2,640
3,704
182 out of 3,704 to receive 660 Shares
1.23%
3,300
3,614
222 out of 3,614 to receive 660 Shares
1.23%
3,960
2,046
151 out of 2,046 to receive 660 Shares
1.23%
4,620
14,633
1,257 out of 14,633 to receive 660 Shares
1.23%
5,280
1,632
160 out of 1,632 to receive 660 Shares
1.23%
5,940
1,105
122 out of 1,105 to receive 660 Shares
1.23%
6,600
12,926
1,586 out of 12,926 to receive 660 Shares
1.23%
13,200
5,602
1,375 out of 5,602 to receive 660 Shares
1.23%
19,800
3,546
1,305 out of 3,546 to receive 660 Shares
1.23%
26,400
1,937
951 out of 1,937 to receive 660 Shares
1.23%
33,000
2,307
1,415 out of 2,307 to receive 660 Shares
1.23%
39,600
1,475
1,086 out of 1,475 to receive 660 Shares
1.23%
46,200
1,232
1,058 out of 1,232 to receive 660 Shares
1.23%
52,800
1,324
1,300 out of 1,324 to receive 660 Shares
1.23%
59,400
888
660 Shares plus 93 out of 888 to receive 
additional 660 Shares
1.23%
66,000
4,984
660 Shares plus 1,132 out of 4,984 to receive 
additional 660 Shares
1.23%
132,000
3,280
1,320 Shares plus 1,490 out of 3,280 to 
receive additional 660 Shares
1.23%
198,000
2,196
1,980 Shares plus 1,496 out of 2,196 to 
receive additional 660 Shares
1.23%
264,000
1,312
2,640 Shares plus 1,192 out of 1,312 to 
receive additional 660 Shares
1.23%
330,000
985
3,960 Shares plus 133 out of 985 to receive 
additional 660 Shares
1.23%
396,000
609
4,620 Shares plus 220 out of 609 to receive 
additional 660 Shares
1.23%
462,000
915
5,280 Shares plus 538 out of 915 to receive 
additional 660 Shares
1.23%
158,158
Total number of Pool A successful applicants: 28,615

<<<PAGE 17>>>
17
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
528,000
2,724
4,620 Shares plus 596 out of 2,724 to receive 
additional 660 Shares
0.90%
594,000
255
5,280 Shares plus 31 out of 255 to receive 
additional 660 Shares
0.90%
660,000
932
5,940 Shares plus 22 out of 932 to receive 
additional 660 Shares
0.90%
1,320,000
351
11,880 Shares plus 16 out of 351 to receive 
additional 660 Shares
0.90%
1,980,000
171
17,820 Shares plus 12 out of 171 to receive 
additional 660 Shares
0.90%
2,640,000
56
23,760 Shares plus 5 out of 56 to receive 
additional 660 Shares
0.90%
3,300,000
85
29,700 Shares plus 10 out of 85 to receive 
additional 660 Shares
0.90%
6,600,000
43
59,400 Shares plus 10 out of 43 to receive 
additional 660 Shares
0.90%
9,900,000
18
89,100 Shares plus 6 out of 18 to receive 
additional 660 Shares
0.90%
13,200,000
10
118,800 Shares plus 5 out of 10 to receive 
additional 660 Shares
0.90%
16,500,000
5
148,500 Shares plus 3 out of 5 to receive 
additional 660 Shares
0.90%
19,800,000
6
178,200 Shares plus 4 out of 6 to receive 
additional 660 Shares
0.90%
26,400,000
4
238,260 Shares
0.90%
40,590,660
4
366,300 Shares
0.90%
4,664
Total number of Pool B successful applicants: 4,664
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 18>>>
18
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Allocations of Offer Shares to Existing Minority A Shareholders and/or their close associates
The Company has applied for, and the Stock Exchange has granted, a waiver from strict 
compliance with Rule 10.04 of, and a consent under paragraph 1C(2) of Appendix F1 to, the 
Listing Rules to permit H Shares in the International Offering to be placed to certain existing 
minority Shareholders who (i) hold less than 5% voting rights of the Company prior to the 
completion of the Global Offering and (ii) are not and will not become (upon the completion of 
the Global Offering) core connected persons of the Company or the close associates of any such 
core connected persons (together, the “Existing Minority A Shareholders”) and/or their close 
associates, subject to, among others, the following conditions:
(a) 
each of the Existing Minority A Shareholders to whom the Company may allocate H Shares 
in the International Offering is interested in less than 5% voting rights in the Company prior 
to the completion of the Global Offering;
(b) 
each of the Existing Minority A Shareholders is not, and will not be, a core connected person 
of the Company or any close associate of any such core connected person immediately prior 
to or following the Global Offering;
(c) 
none of the Existing Minority A Shareholders has the right to appoint any Director and/or has 
any other special rights in the Company;
(d) 
allocation to the Existing Minority A Shareholders or their close associates will not affect the 
Company’s ability to satisfy the public float requirement as prescribed under Rule 19A.13A 
of the Listing Rules;
(e) 
no preferential treatment is given to the Existing Minority A Shareholders or their respective 
close associates (other than the assured entitlement for a cornerstone investor); and
(f) 
details of the allocation to the Existing Minority A Shareholders and/or their respective close 
associates holding more than 1% of the issued share capital of the Company immediately 
prior to the completion of the Global Offering have been disclosed in this announcement.

<<<PAGE 19>>>
19
Please refer to the section headed “Waivers and Exemptions – Allocation of Our H Shares to 
Existing Minority Shareholders and Their Close Associates under Rule 10.04 and Paragraph 1C(2) 
of Appendix F1 to the Hong Kong Listing Rules” in the Prospectus for further details of the waiver 
and consent.
Allocations of Offer Shares to the existing Shareholders and Cornerstone Investors and/
or their close associates as placees with a consent under Chapter 4.15 of the Guide for New 
Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 
of the Guide for New Listing Applicants to permit the Company to allocate further Offer Shares in 
the International Offering to certain existing Shareholders and Cornerstone Investors and/or their 
close associates (the “Size-based Exemption Participants”) as placees, subject to the following 
conditions (the “Size-based Exemption”):
(a) 
the final offering size of the Global Offering, will be of a total value of at least HK$1 billion;
(b) 
Offer Shares allocated to all existing Shareholders and their close associates (whether as 
Cornerstone Investors and/or as placees) as permitted under the Size-based Exemption do not 
exceed 30% of the total number of the Offer Shares;
(c) 
each of the Directors, chief executive and the Controlling Shareholders of the Company 
has confirmed that, no Offer Shares have been allocated to them or their respective close 
associates pursuant to the Size-based Exemption;
(d) 
the allocation to Size-based Exemption Participants under the Size-based Exemption will 
not affect the Company’s ability to satisfy the minimum public float requirement under Rule 
19A.13A of the Listing Rules; and
(e) 
the details of allocation to Size-based Exemption Participants under the Size-based Exemption 
will be disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange. For details of the allocation to Size-based Exemption Participants, 
please refer to the section headed “Allotment Results Details – International Offering – Allotees 
with Waivers/Consents Obtained” in this announcement.

<<<PAGE 20>>>
20
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines. Details of the placement to connected 
clients are set out below. The Company has applied to the Stock Exchange for, and the Stock 
Exchange has granted, consents under paragraph 1C(1) of the Placing Guidelines to permit the 
Company to allocate such Offer Shares in the International Offering to the connected clients. The 
allocation of Offer Shares to such connected clients is in compliance with all the conditions under 
the consent granted by the Stock Exchange.
Part A
Allocation of Offer Shares to Connected Client holding the beneficial interest of the Offer 
Shares on a discretionary basis on behalf of independent third parties
No.
Connected Distributor
Connected Client
Relationship with the 
Connected Distributor
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
Percentage of 
total number 
of Offer 
Shares
Approximate 
percentage of 
total Shares 
in issue 
immediately 
following the 
completion 
of Global 
Offering
1.
Guotai Junan Securities 
(Hong Kong) Limited 
(“GTJA Securities”)
S h a n g h a i G u o t a i 
Haitong Securities Asset 
Management Co., Ltd. 
(“Shanghai Guotai”) (1)
Shanghai Guotai is a 
member of the same 
group of companies as 
GTJA Securities.
N
47,520
0.006%
0.0006%
2.
GTJA Securities
F u l l g o a l F u n d 
Management Co., Ltd. 
(“Fullgoal Fund”) (2)
F u l l g o a l F u n d i s 
considered as a member 
of the same group of 
companies as GTJA 
Securities.
Y
Please refer 
to note (8) for 
background 
and details of 
such schemes.
192,060
0.02%
0.002%
3.
CLSA Limited 
(“CLSA”)
China Asset Management 
(Hong Kong) Limited 
(“China AMC HK”) (3)
China AMC HK is a 
member of the same 
group of companies as 
CLSA.
N
95,700
0.01%
0.001%

<<<PAGE 21>>>
21
No.
Connected Distributor
Connected Client
Relationship with the 
Connected Distributor
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
Percentage of 
total number 
of Offer 
Shares
Approximate 
percentage of 
total Shares 
in issue 
immediately 
following the 
completion 
of Global 
Offering
4.
CLSA
CITIC Securities Asset 
Management Company 
Limited (“CITIC Asset 
Management”) (4)
CITIC Asset Management 
is a member of the same 
group of companies as 
CLSA.
Y
Please refer 
to note (8) for 
background 
and details of 
such schemes.
3,300
0.0004%
0.0000%
5.
CLSA
CITIC Securities Asset 
M a n a g e m e n t ( H K ) 
Limited (“CITIC Asset 
Management HK”) (5)
CITIC Asset Management 
HK is a member of the 
same group of companies 
as CLSA.
N
3,300
0.0004%
0.0000%
6.
UBS AG Singapore 
Branch Wealth 
Management (“UBS 
AG Singapore”)
UBS Asset Management 
(Singapore) Limited 
(“UBS AM”) (6)
UBS AM is a member 
of the same group of 
companies as UBS AG 
Singapore.
N
384,780
0.05%
0.005%
7.
The Hongkong and 
Shanghai Banking 
Corporation Limited 
PB (“HSBC PB”) 
and HSBC Broking 
Securities (Asia) 
Limited (“HSBC”)
HSBC Global Asset 
Management (Hong 
Kong) Limited (“HSBC 
AM”) (7)
HSBC PB, HSBC and 
HSBC AM are members 
of the same group of 
companies.
N
18,480
0.002%
0.0002%
Notes:
(1) 
ICBC Wealth Management Co., Ltd. (“ICBC WM”) intends to subscribe for Offer Shares through the 
subscription of a specific asset management plan, namely “Guotai Haitong Junxiang Wentui QDII No. 1 
Collective Asset Management Plan” (國泰海通君享穩拓QDII1號集合資產管理計劃) (“ICBC QDII plan”), of 
which Shanghai Guotai is the investment manager.

<<<PAGE 22>>>
22
(2) 
Fullgoal Fund is owned by Guotai Haitong Securities Co., Ltd. (stock code: 2611.HK/601211.SH) (“Guotai 
Haitong”) as to 27.775%. GTJA Securities, the Sole Sponsor-Overall Coordinator is a subsidiary of Guotai 
Haitong. Fullgoal Fund is considered as a member of the same group of companies as GTJA Securities and 
therefore is a connected client of GTJA Securities for the purpose of paragraph 1B of the Placing Guidelines.
Fullgoal Fund, will subscribe for and hold the relevant number of Offer Shares through multiple funds, on 
behalf of its clients who are Independent Third Parties on a discretionary basis. No single client is the ultimate 
beneficial owner with more than 30% of interest of each of the funds.
The funds are as follows:
a. 
ICBC Fullgoal China Small & Mid Cap(HK listed) Equity Fund (富國中國中小盤（香港上市）混合型證
券投資基金), of which no ultimate beneficial owner holds 30% or more interest;
b. 
CMB-FULLGOAL BLUE CHIP SELECTED EQUITY FUND(QDII) (富國藍籌精選股票型證券投資基
金(QDII)), of which no ultimate beneficial owner holds 30% or more interest.
Fullgoal Fund is a QDII approved by the relevant PRC authority and is also the first fund management company 
with foreign equity participation among the first ten fund management companies in China. The relevant funds 
proposed to subscribe for the Offer Shares under the management of Fullgoal Fund are open-ended publicly 
raised securities investment funds registered with the CSRC.
The shareholders of Fullgoal Fund include (i) Guotai Haitong Securities Co., Ltd. (國泰海通證券股份有限公
司) holding 27.775% in Fullgoal Fund; (ii) Shenwan Hongyuan Securities Co., Ltd. (申萬宏源證券有限公司) 
holding 27.775% in Fullgoal Fund; (iii) Bank of Montreal holding 27.775% in Fullgoal Fund, and (iv) Shandong 
Financial Asset Management Co., Ltd. (山東省金融資產管理股份有限公司), holding 16.675% in Fullgoal 
Fund.
(3) 
China AMC HK will hold the Offer Shares in its capacity as the discretionary fund manager managing on behalf 
of its underlying clients. To the best knowledge of China AMC HK after due enquiry, each of the underlying 
clients is an independent third party.
The funds are as follows:
a. 
CHINAAMC SELECT GREATER CHINA TECHNOLOGY FUND, of which investor holding 30% 
or more interests is Futu Securities International (Hong Kong) Limited — client account, which was 
managed by Futu Securities International (Hong Kong) Limited on behalf of independent third parties;
b. 
CHINAAMC FUND – CHINAAMC CHINA OPPORTUNITIES FUND, of which no ultimate beneficial 
owner holds 30% or more interest;
c. 
CHINAAMC CHINA FOCUS FUND, of which investor holding 30% or more interests is Manulife 
(International) Limited (“Manulife Limited”). The ultimate beneficial owner holds 30% or more interest 
in Manulife Limited is MANULIFE FINANCIAL CORP, which is a listed entity on the Stock Exchange 
(stock code: 0945);
d. 
CHINAAMC CHINA GROWTH FUND (SICAV), of which investor holding 30% or more interests is 
Yuanta Securities (HK) Company LTD (“Yuanta Securities”). The ultimate beneficial owner holds 30% 
or more interest in Yuanta Securities is Yuanta Financial Holdings Co. Ltd, which is a listed entity on the 
Stock Exchange (stock code: 2885);
e. 
ICBC (ASIA) LTD-CHINAAMC-BSCOMC LTD, of which ultimate beneficial owner holding 30% or 
more interest is BSCOMC Limited. BSCOMC Limited is a government body controlled by the People’s 
Government of Beijing Municipality.

<<<PAGE 23>>>
23
(4) 
CITIC Asset Management is a member of the same group of companies as CLSA. CITIC Asset Management 
will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of 
their investors (the “CITICS AM Ultimate Clients”), together with each of their ultimate beneficial owners, 
is, to the best knowledge of CITIC Asset Management, (i) an independent third party of the Company, its 
subsidiaries, its substantial shareholders, CITIC Asset Management, CLSA and the companies which are 
members of the same group of companies as CLSA; and (ii) a collective investment scheme which is not 
authorized by the SFC.
The funds are as follows:
a. 
CITIC Securities AM-Guibinfengyuan No.118 QDII (中信證券資管貴賓豐元118號QDII集合資產管理計
劃), of which ultimate beneficial owner holds 30% or more interest is Zhang Guofeng (張國鋒);
b. 
CITIC SECURITIES COMPANY LIMITED-XINHANG ZHIYUAN NO.1 (中信證券信航致遠1號集合
資產管理計劃), of which no ultimate beneficial owner holds 30% or more interest;
c. 
CITIC SECURITIES COMPANY LIMITED-XINHANG ZHIYUAN NO.3 (中信證券信航致遠3號集合
資產管理計劃), of which no ultimate beneficial owner holds 30% or more interest;
d. 
CITIC SECURITIES AM-GUIBINFENGYUAN NO.108 QDII (中信證券資管貴賓豐元108號QDII集合
資產管理計劃), of which no ultimate beneficial owner holds 30% or more interest.
(5) 
CITIC Asset Management HK will hold the Offer Shares in its capacity as the discretionary fund manager 
managing the funds on behalf of their investors. To the best knowledge of CITIC Asset Management HK after 
due enquiry, each of the funds is an independent third party.
The funds are as follows:
a. 
CITIC Securities Asset Management (HK) Limited – Meta Chance2, of which ultimate beneficial owner 
holding 30% or more interest is Song Ke;
b. 
ICBC (ASIA) LTD-CITIC SECURITIES AM LTD-BSCOMC LTD, of which ultimate beneficial owner 
holding 30% or more interest is State-owned Assets Supervision and Administration Commission of the 
People’s Government of Beijing Municipality;
c. 
CITIC Securities Asset Management (HK) Limited – CLSA CT Limited Sub Account 33, of which no 
ultimate beneficial owner holds 30% or more interest.
(6) 
The ultimate beneficial owner of UBS AM is UBS Group AG, which is a listed entity in Switzerland (ID 
Number: 24476758).
(7) 
HSBC AM will hold the Offer Shares in its capacity as the discretionary fund manager managing assets on 
behalf of its underlying clients. Each of the underlying clients of HSBC AM is an independent third party of 
HSBC AM, HSBC PB, HSBC and the companies which are members of the same group of HSBC.
(8) 
Details of the collective investment schemes which is not authorized by the SFC are as follows.

<<<PAGE 24>>>
24
No.
Fund name
Types and values 
of asset under 
management 
(“AUM”)
Whether the 
scheme 
is publicly 
marketed
Scheme 
establishment 
date
Identities of the 
general partners 
and the 20 
largest limited 
partners of the 
scheme where 
applicable
Identity of 
the scheme 
administrator
Relationships 
among the 
scheme, the 
ultimate beneficial 
owner(s) of 
the limited 
partner(s), the 
largest group of 
the shareholders/
controlling 
shareholders of 
the Company, and 
the Company
1.
ICBC Fullgoal China 
Small & Mid Cap 
(HK listed) Equity 
Fund
Public Offering 
of Fund 3.55 
BILLION (First-
quarter reported 
data)
Publicly Marketed
September 4, 
2012
Not applicable 
as it is not in 
p a r t n e r s h i p 
structure and 
does not have 
a n y g e n e r a l 
partner or limited 
partner. 
No single client 
is the ultimate 
beneficial owner 
with more than 
30% of interest 
of each of the 
funds.
Fullgoal Fund
T h e s c h e m e 
a n d u l t i m a t e 
beneficial owners 
are independent 
third parties of 
GTJA Securities, 
the Company and 
the Controlling 
Shareholders of the 
Company.
2.
CMB-FULLGOAL 
BLUE CHIP 
SELECTED EQUITY 
FUND (QDII)
Public Offering 
of Fund 1.6 
BILLION (First-
quarter reported 
data)
Publicly Marketed
August 2, 
2019
Not applicable 
as it is not in 
p a r t n e r s h i p 
structure and 
does not have 
a n y g e n e r a l 
partner or limited 
partner.
No single client 
is the ultimate 
beneficial owner 
with more than 
30% of interest 
of each of the 
funds.
Fullgoal Fund
T h e s c h e m e 
a n d u l t i m a t e 
beneficial owners 
are independent 
third parties of 
GTJA Securities, 
the Company and 
the Controlling 
Shareholders of the 
Company.

<<<PAGE 25>>>
25
No.
Fund name
Types and values 
of asset under 
management 
(“AUM”)
Whether the 
scheme 
is publicly 
marketed
Scheme 
establishment 
date
Identities of the 
general partners 
and the 20 
largest limited 
partners of the 
scheme where 
applicable
Identity of 
the scheme 
administrator
Relationships 
among the 
scheme, the 
ultimate beneficial 
owner(s) of 
the limited 
partner(s), the 
largest group of 
the shareholders/
controlling 
shareholders of 
the Company, and 
the Company
3.
CITIC SECURITIES 
COMPANY 
LIMITED-XINHANG 
ZHIYUAN NO.1
Collective asset 
management plan
AUM: 
approximately 
RMB24 million*
No
December 25, 
2020
Not applicable 
as it is not in 
p a r t n e r s h i p 
structure and 
does not have 
a n y g e n e r a l 
partner or limited 
partner
CITIC Securities 
Asset Management 
Company Limited
T h e s c h e m e 
a n d u l t i m a t e 
beneficial owners 
are independent 
third parties of 
CLSA Limited, 
the Company and 
the Controlling 
Shareholders of the 
Company.
4.
CITIC SECURITIES 
COMPANY 
LIMITED-XINHANG 
ZHIYUAN NO.3
Collective asset 
management plan
AUM: 
approximately 
RMB56 million*
No
March 4, 2021
Not applicable 
as it is not in 
p a r t n e r s h i p 
structure and 
does not have 
a n y g e n e r a l 
partner or limited 
partner
CITIC Securities 
Asset Management 
Company Limited
T h e s c h e m e 
a n d u l t i m a t e 
beneficial owners 
are independent 
third parties of 
CLSA Limited, 
the Company and 
the Controlling 
Shareholders of the 
Company.
5.
CITIC Securities 
AM-Guibinfengyuan 
No.118 QDII
Collective asset 
management plan
AUM: 
approximately 
RMB228 million*
No
August 29, 
2025
Not applicable 
as it is not in 
p a r t n e r s h i p 
structure and 
does not have 
a n y g e n e r a l 
partner or limited 
partner
CITIC Securities 
Asset Management 
Company Limited
T h e s c h e m e 
a n d u l t i m a t e 
beneficial owners 
are independent 
third parties of 
CLSA Limited, 
the Company and 
the Controlling 
Shareholders of the 
Company.

<<<PAGE 26>>>
26
No.
Fund name
Types and values 
of asset under 
management 
(“AUM”)
Whether the 
scheme 
is publicly 
marketed
Scheme 
establishment 
date
Identities of the 
general partners 
and the 20 
largest limited 
partners of the 
scheme where 
applicable
Identity of 
the scheme 
administrator
Relationships 
among the 
scheme, the 
ultimate beneficial 
owner(s) of 
the limited 
partner(s), the 
largest group of 
the shareholders/
controlling 
shareholders of 
the Company, and 
the Company
6.
CITIC SECURITIES  
AM-
GUIBINFENGYUAN 
NO.108 QDII
Collective asset 
management plan
AUM: 
approximately 
RMB155 million*
No
April 14, 2026
Not applicable 
as it is not in 
p a r t n e r s h i p 
structure and 
does not have 
a n y g e n e r a l 
partner or limited 
partner
CITIC Securities 
Asset Management 
Company Limited
T h e s c h e m e 
a n d u l t i m a t e 
beneficial owners 
are independent 
third parties of 
CLSA Limited, 
the Company and 
the Controlling 
Shareholders of the 
Company.
* 
This AUM figure is as of June 18, 2026.

<<<PAGE 27>>>
27
Part B
Allocation of Offer Shares to Connected Client holding the beneficial interest of the Offer 
Shares on a non-discretionary basis on behalf of independent third parties
No.
Connected Distributor
Connected Client and 
its Ultimate Beneficial 
Owner
Relationship with the 
Connected Distributor
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
Percentage of 
total number 
of Offer 
Shares
Approximate 
percentage of 
total Shares 
in issue 
immediately 
following the 
completion 
of Global 
Offering
1.
Guotai Junan Securities 
(Hong Kong) Limited 
(“GTJA Securities”)
Guotai Junan Investments 
(Hong Kong) Limited 
(“GTJAI”) (1)
GTJAI is a member 
of the same group of 
companies as GTJA 
Securities.
N
91,027,200
11.21%
1.12%
2.
C L S A L i m i t e d 
(“CLSA”)
C I T I C S e c u r i t i e s 
International Capital 
Management Limited 
(“CSI”) (2)
CSI is a member of 
the same group of 
companies as CLSA.
N
4,518,360
0.56%
0.06%
Notes:
(1) 
It is proposed that GTJAI participates as placee to subscribe for the Offer Shares under the International 
Offering (the “GTJAI Subscription”).
In relation to the GTJAI Subscription, GTJAI shall hold the Offer Shares for hedging purpose as the single 
underlying asset of several sets of back-to-back total return swap transaction (the “GTHT Back-to-back TRS”) 
to be entered into between GTJAI and Guotai Haitong Securities Co., Ltd. (the “GTHT Onshore Parent”) 
in connection with several total return swap orders (the “GTHT Client TRS”) to be entered into by GTHT 
Onshore Parent and several ultimate clients (the “GTHT Onshore Ultimate Clients”), respectively. Such GTHT 
Client TRS is to be fully funded by the GTHT Onshore Ultimate Clients. GTJAI will hold the Offer Shares on 
a non-discretionary basis for the purpose of hedging the economic exposure under the GTHT Back-to-back TRS 
and GTHT Client TRS only.
During the tenor of the GTHT Client TRS, all economic returns of the Offer Shares will be passed to the GTHT 
Onshore Ultimate Clients and all economic losses shall be borne by the GTHT Onshore Ultimate Clients, 
subject to the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS, and GTJAI will 
not take part in any economic return or bear any economic loss in relation to the price of the Offer Shares. The 
GTHT Onshore Ultimate Clients may request to redeem the Offer Shares at their own discretion, upon which 
GTJAI shall dispose of the Offer Shares and settle the GTHT Back-to-back TRS and GTHT Client TRS in cash 
in accordance with the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS documents. 
Due to its internal policy, GTJAI will not exercise the voting right attaching to the Offer Shares during the tenor 
of the GTHT Back-to-back TRS and GTHT Client TRS.

<<<PAGE 28>>>
28
To the best knowledge of GTJAI after making all reasonable enquiries, (i) each of the GTHT Onshore Ultimate 
Clients is an independent third party of GTJAI, GTJA Securities and the companies which are members of the 
same group of GTJA Securities; (ii) each of the ultimate beneficial owners holding 30% or more interests of 
GTHT Onshore Ultimate Clients is an independent third party of the Company, GTJAI, GTJA Securities and 
the companies which are members of the same group of GTJA Securities; and (iii) each of the GTHT Onshore 
Ultimate Clients and their respective ultimate beneficial owners (as set out below) is an independent third party 
of the Company, the subsidiaries, the Controlling Shareholders, substantial shareholders, existing shareholders 
of the Company (the “Relevant Parties”), and respective subsidiaries and/or respective close associates of the 
Relevant Parties.
Such GTHT Client TRS is to be fully funded by the GTHT Onshore Ultimate Clients:
(a) 
Pingyang Ruihe Investment Management Co, Ltd – Ruihexinjian Private Securities Investment Fund (平
陽瑞和投資管理有限公司－瑞和信見私募證券投資基金), of which ultimate beneficial owner holds 
30% or more interest is YI JIANPING (易建萍);
(b) 
ZTCFFund Co., Ltd – Zhongtan Fuying 6 Hao Private Fund (中碳創富(北京)投資基金管理有限公司－
中碳富盈6號私募證券投資基金), of which no ultimate beneficial owner holds 30% or more interest;
(c) 
Zhuhai Zhuoshui Private Fund Management Co., Ltd – Zhuoshui No.1 Phase A Private Securities 
Investment Fund (珠海濁水私募基金管理有限公司－濁水1號A期私募證券投資基金) of which ultimate 
beneficial owner holds 30% or more interest is BI RAN （畢然）;
(d) 
Shanghai Greenwoods Asset Management Co., Ltd. – Greenwoods Harvest No.2 Fund (上海景林資產管
理有限公司－景林豐收2號基金), of which no ultimate beneficial owner holds 30% or more interest;
(e) 
Shanghai Greenwoods Asset Management Co., Ltd. – Greenwoods Harvest No.3 Private Securities 
Investment Fund (上海景林資產管理有限公司－景林豐收3號私募證券投資基金), of which no ultimate 
beneficial owner holds 30% or more interest;
(f) 
Shanghai Greenwoods Asset Management Co., Ltd. – Greenwoods Harvest No.6 Private Securities 
Investment Fund (上海景林資產管理有限公司－景林豐收6號私募證券投資基金), of which no ultimate 
beneficial owner holds 30% or more interest;
(g) 
Shanghai Greenwoods Asset Management Co., Ltd. – Greenwoods Jingtai Harvest Private Securities 
Investment Fund (上海景林資產管理有限公司－景林景泰豐收私募證券投資基金), of which no 
ultimate beneficial owner holds 30% or more interest.
To the best knowledge of GTJAI and after making all reasonable enquiries, (i) each of the GTJA Onshore 
Ultimate Clients and the ultimate beneficial owners holding 30% or more interest of the GTJA Onshore 
Ultimate Clients listed above is an independent third party of GTJAI, GTJA Securities and the companies which 
are members of the same group of companies as GTJA Securities, and (ii) GTJAI is not a collective investment 
scheme which is not authorised by the SFC nor is expected to hold the Offer Shares on behalf of such scheme.
(2) 
CSI proposes to subscribe for and hold the Offer Shares as a placee under the International Offering on behalf 
of CSI Ultimate Clients, on a non-discretionary basis, pursuant to which:
CSI will act as the single counterparty of a back-to-back total return swap transaction (the “CSI Back-to-back 
TRS”) to be entered into by it in connection with a total return swap order (the “CSI Client TRS”) placed and 
fully funded by the CSI Ultimate Clients, by which CSI will pass the full economic exposure of the Offer Shares 
placed to CSI to the CSI Ultimate Clients.
As confirmed by CSI and CLSA, CSI will hold the legal title and beneficial interest in the Offer Shares, but will 
contractually agree to pass on the full economic exposure and return of the Offer Shares to the CSI Ultimate 
Clients, on a non-discretionary basis. The CSI Ultimate Clients may exercise their early termination rights to 
terminate the CSI Client TRS at any time from the trade date of the CSI Client TRS which should be on or after 
the date on which the Offer Shares are listed on the Stock Exchange.

<<<PAGE 29>>>
29
The ultimate clients of CSI include:
(a) 
HY Capital Company Limited, of which two shareholders holding 30% or more interest are Xia Hui and 
Lu Ang;
(b) 
Heyi Xuehu No. 1 Private Securities Investment Fund (合易雪湖1號私募證券投資基金) is managed 
by Beijing Heyi Yingtong Asset Management Co., Ltd. (北京合易盈通資產管理有限公司).None of the 
single shareholders hold 30% or more interest in Heyi Xuehu No. 1 Private Securities Investment Fund. 
The single ultimate beneficial owner of Beijing Heyi Yingtong Asset Management Co., Ltd. (北京合易盈
通資產管理有限公司) includes Liu Zhe (劉喆) and Liu Yang (劉洋);
(c) 
Yuemintou Xinxuan Opportunity No. 1 Private Securities Investment Fund (粵民投新選機遇1號私募
證券投資基金), of which shareholder holding 30% or more interest is Liu Wei (劉偉), is managed by 
Yuemintou Private Securities Fund Management (Shenzhen) Co., Ltd. (粵民投私募證券基金管理(深圳)
有限公司). There is no ultimate beneficial owner for Yuemintou Private Securities Fund Management 
(Shenzhen) Co., Ltd.;
(d) 
Sun Qianru, an independent third-party individual (Singapore ID: S8755575E);
(e) 
Jin Dan Ocean Voyage No.6 Private Securities Investment Fund (金澹遠洋6號私募證券投資基金), of 
which shareholder holding 30% or more interest is Ding Hai (丁海), is managed by Shanghai Jindan 
Asset Management Co., Ltd. (上海金澹資產管理有限公司). The single ultimate beneficial owner of 
Shanghai Jindan Asset Management Co., Ltd. (上海金澹資產管理有限公司) is Zhang Yan (張焱).

<<<PAGE 30>>>
30
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or 
any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer 
or solicitation to purchase or subscribe for the Offer Shares in the United States or in any other 
jurisdictions. The Offer Shares have not been, and will not be, registered under the United States 
Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or securities 
law of any state or other jurisdiction of the United States. The Offer Shares may not be offered, 
sold, pledged or otherwise transferred within the United States, except pursuant to an exemption 
from the registration requirements of the U.S. Securities Act and U.S. Investment Company Act 
of 1940, as amended (“U.S. Investment Company Act”), and in compliance with any applicable 
state securities laws. There will be no public offer of the Offer Shares in the United States.
The Offer Shares are being offered and sold outside the United States to investors that are not 
U.S. persons nor persons acquiring for the account or benefit of U.S. persons in reliance on 
Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated June 17, 2026 issued by LINGYI iTECH 
(GUANGDONG) COMPANY for detailed information about the Global Offering described 
below before deciding whether or not to invest in the H Shares thereby being offered.
* 
Potential investors of the Offer Shares should note that the Sole Sponsor and the Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations 
under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the 
events set out in the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong 
Public Offering – Hong Kong Underwriting Agreement – Grounds for Termination” in the Prospectus at any 
time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on June 26, 
2026).

<<<PAGE 31>>>
31
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering (assuming no additional A Shares are 
issued under the 2024 Share Option Scheme), 811,811,880 H Shares, representing approximately 
10.04% of the total issued share capital of the Company upon Listing (excluding treasury Shares), 
which is higher than the prescribed percentage of H Shares required to be held in public hands of 
10% under Rule 19A.13A(2)(a) of the Listing Rules, thereby satisfying Rule 19A.13A(2) of the 
Listing Rules at the time of the Listing.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the H Shares of the Company at the time of Listing. Based on the 
final Offer Price of HK$10.18 per H Share, the Company confirmed that it complies with the free 
float requirement under Rule 19A.13C of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering (assuming 
no additional Shares are issued under the 2024 Share Option Scheme): (i) the Shares will be held 
by at least 300 Shareholders at the time of Listing, in compliance with Rule 8.08(2) of the Listing 
Rules; (ii) the three largest public Shareholders will not hold more than 50% of the H Shares held 
in public hands at the time of Listing, in compliance with Rules 8.08(3) and 8.24 of the Listing 
Rules; (iii) no placee will, individually, be placed more than 10% of the enlarged issued share 
capital of the Company immediately after the Global Offering; and (iv) there will not be any new 
substantial Shareholder (as defined in the Listing Rules) immediately after the Global Offering.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, June 26, 
2026 (Hong Kong time), provided that the Global Offering has become unconditional and the right 
of termination described in the section headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has not been 
exercised. Investors who trade the H Shares on the basis of publicly available allocation details 
prior to the receipt of H Share certificates or prior to the H Share certificates becoming valid 
evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Friday, June 
26, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Friday, June 26, 2026 (Hong Kong time). The H Shares will be 
traded in board lots of 660 H Shares each, and the stock code of the H Shares will be 1688.
By order of the Board
LINGYI iTECH (GUANGDONG) COMPANY
Ms. Zeng Fangqin
Chairwoman of the Board, Executive Director
and General Manager
Hong Kong, June 25, 2026
As at the date of this announcement, the Board comprises: (i) Ms. Zeng Fangqin, Mr. Jia Shuangyi 
and Ms. Huang Jinrong as executive Directors; (ii) Ms. Wei Zhenghui as non-executive Director; 
and (iii) Dr. Lau Kin Shing Charles, Dr. Cai Yuanqing and Mr. Ruan Chao as independent 
non-executive Directors.
