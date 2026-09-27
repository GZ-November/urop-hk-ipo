# 配发结果公告抽取任务：9981.HK Shenzhen Woer Heat-Shrinkable Material Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**12/02/2026 22:56**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0212/2026021201492.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"9981.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) and Hong 
Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States (including its 
territories and possessions, any state of the United States and the District of Columbia). This announcement does not constitute 
or form a part of any offer or solicitation to purchase or subscribe for securities in the United States or in any other jurisdictions. 
The securities mentioned herein have not been, and will not be, registered under the United States Securities Act of 1933 as 
amended from time to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the United States. 
The securities may not be offered, sold, pledged or otherwise transferred within the United States except pursuant to an exemption 
from the registration requirements of the U.S. Securities Act and in compliance with any applicable state securities laws. The 
securities are being offered and sold outside the United States in offshore transactions in accordance with Regulation S under the 
U.S. Securities Act. There will be no public offer of securities in the United States.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase or 
subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated February 
5, 2026 (the “Prospectus”) issued by Shenzhen Woer Heat-Shrinkable Material Co., Ltd. (深圳市沃爾核材股份有限公司) (the 
“Company”) for detailed information about the Global Offering described below before deciding whether or not to invest in the 
H Shares thereby being offered. Any investment decision in relation to the Offer Shares should be taken solely in reliance on the 
information in the Prospectus. The Company has not been and will not be registered under the U.S. Investment Company Act of 
1940, as amended.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those defined in 
the Prospectus.
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinators (for themselves and on behalf of 
the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting Agreement 
with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to 
8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Friday, February 13, 2026).

<<<PAGE 2>>>
2
Shenzhen Woer Heat-Shrinkable Material Co., Ltd.
深圳市沃爾核材股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
139,988,800 H Shares
Number of Hong Kong Offer Shares
:
13,999,000 H Shares
Number of International Offer Shares
:
125,989,800 H Shares
Final Offer Price
:
HK$20.09 per Offer Share, plus brokerage 
of 1%, SFC transaction levy of 0.0027%, 
Stock Exchange trading fee of 0.00565% 
and AFRC transaction levy of 0.00015%
Nominal value
:
RMB1.00 per H Share
Stock code
:
9981
Joint Sponsors, Sponsor-overall Coordinators, Joint Global Coordinators, Joint Bookrunners 
and Joint Lead Managers
Overall Coordinator, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
Shenzhen Woer Heat-Shrinkable Material Co., Ltd.
深圳市沃爾核材股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND  
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated February 5, 2026 (the “Prospectus”) issued by 
Shenzhen Woer Heat-Shrinkable Material Co., Ltd. (the “Company”).
SUMMARY
Company information
Stock code
9981
Stock short name
WOER
Dealings commencement date
February 13, 2026*
*	
see note at the end of the announcement
Price Information
Final Offer Price
HK$20.09
Maximum Offer Price 
HK$20.09
Offer Price Adjustment
N/A
Offer Shares and Share Capital
Number of Offer Shares 
139,988,800
Final Number of Offer Shares in Hong Kong Public Offering
13,999,000
Final Number of Offer Shares in International Offering 
125,989,800
Number of issued Shares upon Listing
1,399,887,362
Proceeds
Gross proceeds (Note) 
HK$2,812.4 million
Less: Estimated listing expenses payable based on Final Offer 
Price
HK$(78.8) million
Net proceeds
HK$2,733.6 million
Note:	
Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of proceeds, please 
refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.

<<<PAGE 4>>>
4
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
141,463
No. of successful applications
31,654
Subscription level
569.58 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong Public 
Offering
13,999,000
Final no. of Offer Shares under the Hong Kong Public Offering
13,999,000
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering
10.00%
Note:	
For details of the final allocation of H Shares to the Public Offer, investors can refer to www.eipo.com.hk/eIPOAllotment 
to perform a search by identification number or www.eipo.com.hk/eIPOAllotment for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
116
Subscription Level
8.19 times
No. of Offer Shares initially available under the International 
Offering
125,989,800
Final no. of Offer Shares under the International Offering
125,989,800
% of Offer Shares under the International Offering to the Global 
Offering
90.00%

<<<PAGE 5>>>
5
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a 
waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit the Company to allocate certain Offer Shares in the International Offering 
to certain existing minority shareholders and/or their close associates, and (b) a consent under 
Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to, among other 
things, allocate further H Shares in the International Offering to an existing Shareholder and/or its 
close associates and Cornerstone Investors and/or its close associates, (i) none of the Offer Shares 
subscribed by the placees and the public have been financed directly or indirectly by the Company, 
any of the Directors, chief executive of the Company, group of single largest shareholder, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or their 
respective close associates; and (ii) none of the placees and the public who have purchased the 
Offer Shares are accustomed to taking instructions from the Company, any of the Directors, chief 
executive of the Company, group of single largest shareholder, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates in 
relation to the acquisition, disposal, voting or other disposition of H Shares registered in his/her/its 
name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
Cornerstone Investors
No. of Offer 
Shares 
allocated
 Note 1 % of Offer 
Shares
% of total issued 
share capital 
after the Global 
Offering
 Note 2 & 3
Existing 
shareholders 
or their 
close 
associates
HHLR Advisors, Ltd. (“HHLRA”)
9,703,000
6.93%
0.69% No
Shanghai Greenwoods and Huatai Capital 
Investment Limited (in connection with 
Greenwoods OTC Swaps)
6,986,000
4.99%
0.50% No
Jump Trading Pacific Pte. Ltd. (“Jump 
Trading”)
1,164,200
0.83%
0.08% No
Huizhou Huilian Investment Partnership 
(Limited Partnership) (“Huizhou 
Huilian”)
9,960,800
7.12%
0.71% No
JCC and Guotai Junan Investments (Hong 
Kong) Limited (in connection with JCC 
OTC Swaps)
1,164,200
0.83%
0.08% No
Shen Zhen New World Investment (H.K) 
Limited (“Shen Zhen New World”)
2,986,400
2.13%
0.21% Yes 
Note 2

<<<PAGE 6>>>
6
Cornerstone Investors
No. of Offer 
Shares 
allocated
 Note 1 % of Offer 
Shares
% of total issued 
share capital 
after the Global 
Offering
 Note 2 & 3
Existing 
shareholders 
or their 
close 
associates
BEST CHEER DEVELOPMENT 
LIMITED (“Best Cheer”)
1,692,200
1.21%
0.12% No
RIME Capital Limited (“RIME”)
398,200
0.28%
0.03% No
SCV Alpha LP (“SCV Alpha”)
1,344,800
0.96%
0.10% No
Yield Royal Investment Holding 
(Singapore) PTE. LTD. (“Yield Royal”)
1,164,200
0.83%
0.08% No
Guohui (HK) Holdings Co., Limited 
(“Guohui HK”)
1,943,600 
(Note 4)
1.39%
0.14% No
Pu Xin Guotai Junan Investments (Hong 
Kong) Limited (in connection with Pu Xin 
OTC Swaps)
1,941,200
1.39%
0.14% No
CAPCHEM (HONGKONG) CO., 
LIMITED (“Capchem Hong Kong”)
2,737,600
1.96%
0.20% No
Enhanced Investment Products Limited 
(“EIP”)
1,940,600
1.39%
0.14% No
Factorial Master Fund (“Factorial”)
776,200
0.55%
0.06% No
Qianhai Starlight Capital SPC (“Qianhai 
Starlight”)
2,328,600
1.66%
0.17% No
Total
48,231,800
34.45%
3.45%
Notes:
(1)	
The number of Offer Shares allocated to such investors only represents the number of Offer Shares allocated to the investors 
as cornerstone investors in the International Offering. For allocations of Offer Shares to the relevant investors as placees 
(if any), please refer to the section headed “Allotment Results Details — International Offering — Allotees with waiver/
consents obtained” in this announcement.
(2)	
For details of a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) 
of the Placing Guidelines granted by the Stock Exchange to permit the Company to allocate certain Offer Shares in the 
International Offering to certain existing minority shareholders and/or their close associates as cornerstone investor, please 
refer to the section headed “Others/Additional Information” in this announcement.
(3)	
Not taking into account any A Shares held by the relevant investors.
(4)	
The actual number of Offer Shares allocated to Guohui HK varies from the Prospectus disclosure due to the actual exchange 
rates determined pursuant to the terms of the cornerstone investment agreements.

<<<PAGE 7>>>
7
Allotees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares 
allocated 
Note 2
% of Offer 
Shares 
% of total 
issued share 
capital after 
the Global 
Offering
Relationship
Allotees with waiver from strict compliance with the requirements under Rule 10.04 of the Listing Rules 
and consent under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by 
existing minority shareholders 
(Note 1)
Shen Zhen New World
5,376,400
3.84%
0.38%
Nil
Allotees with consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocations of further H Shares to certain Cornerstone Investors and/or their close associates 
(Note 1)
HHLRA 
9,703,000
6.93%
0.69%
A Cornerstone 
Investor 
Note 2
Shanghai Greenwoods Asset 
Management Co., Ltd. and Huatai 
Capital Investment Limited (in 
connection with Greenwoods OTC 
Swaps)
3,103,000
2.22%
0.22%
A Cornerstone 
Investor 
Note 2
Greenwoods Asset Management 
Hong Kong Limited
776,200
0.55%
0.06%
A close associate 
of a Cornerstone 
Investor 
Note 2 & 3
Jump Trading 
1,164,200
0.83%
0.08%
A Cornerstone 
Investor 
Note 2
Huizhou Huilian 
1,106,600
0.79%
0.08%
A Cornerstone 
Investor 
Note 2
JCC and Guotai Junan Investments 
(Hong Kong) Limited (in connection 
with JCC OTC Swaps)
930,000
0.66%
0.07%
A Cornerstone 
Investor 
Note 2
Shen Zhen New World 
2,390,000
1.71%
0.17%
A Cornerstone 
Investor 
Note 2
BEST CHEER 
1,366,000
0.98%
0.10%
A Cornerstone 
Investor 
Note 2
RIME 
310,800
0.22%
0.02%
A Cornerstone 
Investor 
Note 2
Doo Financial HK Limited.
1,344,800
0.96%
0.10%
A close associate 
of a Cornerstone 
Investor 
Note 4

<<<PAGE 8>>>
8
Investor
No. of Offer 
Shares 
allocated 
Note 2
% of Offer 
Shares 
% of total 
issued share 
capital after 
the Global 
Offering
Relationship
Guohui HK
776,200
0.55%
0.06%
A Cornerstone 
Investor 
Note 2
Pu Xin Guotai Junan Investments 
(Hong Kong) Limited (in connection 
with Pu Xin GTHT OTC Swaps)
1,240,000 
0.89%
0.09%
A Cornerstone 
Investor 
Note 2
EIP
1,550,000 
1.11%
0.11%
A Cornerstone 
Investor 
Note 2
Qianhai Starlight
1,550,000 
1.11%
0.11%
A Cornerstone 
Investor 
Note 2
Factorial
620,000 
0.44%
0.04%
A Cornerstone 
Investor 
Note 2
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for 
New Listing Applicants in relation to allocations to connected clients 
(Note 1)
Fullgoal Fund Management Co., 
Ltd. 
192,200
0.14%
0.01%
Connected client 
as a placee
Fullgoal Asset Management (HK) 
Limited 
197,800
0.14%
0.01%
Connected client 
as a placee
Guotai Junan Investment (Hong 
Kong) Limited
4,074,600
2.91%
0.29%
Connected client 
as a placee
China Universal Asset Management 
(Hong Kong) Company Limited
390,000
0.28%
0.03%
Connected client 
as a placee
CHINA ASSET MANAGEMENT 
(HONG KONG) LIMITED
13,000
0.01%
0.001%
Connected client 
as a placee
CITIC Securities International 
Capital Management Limited
11,600
0.01%
0.001%
Connected client 
as a placee
(1)	
For details of (a) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of the Placing Guidelines granted by the Stock Exchange to permit the Company to allocate certain Offer Shares in 
the International Offering to existing minority shareholders and their close associates as cornerstone investor; (b) a consent 
under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to allocate certain 
Offer Shares in the International Offering to certain Cornerstone Investors and/or their close associates; and (c) a consent 
under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate certain Offer Shares in the International 
Offering to connected clients, please refer to the sub-section relating to section headed “Others/Additional Information” in 
this announcement.

<<<PAGE 9>>>
9
(2)	
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the number of Offer 
Shares allocated to the investors as placees in the International Offering. For allocations of Offer Shares to the relevant 
investors as Cornerstone Investors, please refer to the section headed “Allotment Results Details — International Offering 
— Cornerstone Investors” in this announcement.
(3)	
Greenwoods Asset Management Hong Kong Limited holds more than 30% of the registered share capital of Shanghai 
Greenwoods, and is therefore a close associate of the Cornerstone Investor, namely Shanghai Greenwoods.
(4)	
Doo Financial HK Limited is the only limited partner of SCV Alpha and is indirectly owned as to 100% by Mr. Chen Junjie, 
who is an Independent Third Party. Doo Financial Limited is therefore a close associate of SCV Alpha.
LOCK-UP UNDERTAKINGS
Cornerstone Investors
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon  
Listing 
Note 2
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding 
in Company 
subject to 
lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings 
Note 1
HHLR 
9,703,000
—
6.93%
0.69%
August 12, 2026
Shanghai Greenwoods 
Asset Management Co., 
Ltd. and Huatai Capital 
Investment Limited 
(in connection with 
Greenwoods OTC Swaps)
6,986,000
—
4.99%
0.50%
August 12, 2026
Jump Trading 
1,164,200
—
0.83%
0.08%
August 12, 2026
Huizhou Huilian 
9,960,800
—
7.12%
0.71%
August 12, 2026
JCC and Guotai Junan 
Investments (Hong 
Kong) Limited (in 
connection with JCC 
OTC Swaps)
1,164,200
—
0.83%
0.08%
August 12, 2026
Shen Zhen New World 
2,986,400
—
2.13%
0.21%
August 12, 2026
BEST CHEER 
1,692,200
—
1.21%
0.12%
August 12, 2026
RIME 
398,200
—
0.28%
0.03%
August 12, 2026
SCV Alpha 
1,344,800
—
0.96%
0.10%
August 12, 2026
Yield Royal 
1,164,200
—
0.83%
0.08%
August 12, 2026

<<<PAGE 10>>>
10
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon  
Listing 
Note 2
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding 
in Company 
subject to 
lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings 
Note 1
Guohui HK
1,943,600 
(Note 4)
—
1.39%
0.14%
August 12, 2026
Pu Xin Guotai Junan 
Investments (Hong 
Kong) Limited (in 
connection with Pu Xin 
GTHT OTC Swaps)
1,941,200
—
1.39%
0.14%
August 12, 2026
Capchem Hong Kong
2,737,600
—
1.96%
0.20%
August 12, 2026
EIP
1,943,600 
(Note 4)
—
1.39%
0.14%
August 12, 2026
Factorial 
776,200
—
0.55%
0.06%
August 12, 2026
Qianhai Starlight 
2,328,600
—
1.66%
0.17%
August 12, 2026
Sub-total
48,231,800
—
34.45%
3.45%
Notes:
(1)	
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on August 12, 2026. The 
Cornerstone Investors will cease to be prohibited from disposing of or transferring H Shares subscribed for pursuant to the 
relevant cornerstone investment agreements after the indicated date.
(2)	
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under 
the Global Offering.
(3)	
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in the Prospectus.

<<<PAGE 11>>>
11
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
H Shares allotted
Allotment as % of 
International Offering 
Allotment as % of 
total Offer Shares
Number of 
Shares held upon 
Listing
% of total issued share 
capital upon Listing
Top 1
19,406,000
15.40%
13.86%
19,406,000
1.39%
Top 5
56,092,400
44.52%
40.07%
59,971,600
4.28%
Top 10
77,452,200
61.47%
55.33%
81,331,400
5.81%
Top 25
110,222,800
87.49%
78.74%
111,889,800
7.99%
Notes
*	
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares allotted
Allotment 
as % of 
International 
Offering 
Allotment 
as % of 
total Offer Shares 
Number of 
H Shares held upon 
Listing
% of 
total issued 
H Shares 
capital upon 
Listing
Number of 
Shares held upon 
Listing
Top 1
19,406,000
15.40%
13.86%
19,406,000
13.86%
19,406,000
Top 5
59,971,600
47.60%
42.84%
59,971,600
42.84%
59,971,600
Top 10
81,331,400
64.55%
58.10%
81,331,400
58.10%
85,578,800
Top 25
111,889,800
88.81%
79.93%
111,889,800
79.93%
116,137,200
Notes
*	
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number of 
H Shares allotted
Allotment 
as % of 
International 
Offering 
Allotment 
as % of 
total Offer Shares 
Number of 
H Shares held 
upon Listing
Number of 
Shares held 
upon Listing
% of 
total issued share 
capital 
upon Listing
Top 1
0
0.00%
0.00%
0
189,563,801
13.54%
Top 5
19,406,000
15.40%
13.86%
19,406,000
370,616,126
26.47%
Top 10
56,418,000
44.78%
40.30%
56,418,000
421,632,434
30.12%
Top 25
102,389,200
81.27%
73.14%
102,389,200
481,879,925
34.42%
Notes
*	
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 12>>>
12
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by the 
public will be conditionally allocated on the basis set out below:
NO. OF SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
POOL A
200
38,921
128 out of 38,921 to receive 200 Shares
0.33%
400
20,769
135 out of 20,769 to receive 200 Shares
0.33%
600
4,999
49 out of 4,999 to receive 200 Shares
0.33%
800
3,201
42 out of 3,201 to receive 200 Shares
0.33%
1,000
4,333
71 out of 4,333 to receive 200 Shares
0.33%
1,200
1,731
34 out of 1,731 to receive 200 Shares
0.33%
1,400
1,077
25 out of 1,077 to receive 200 Shares
0.33%
1,600
1,160
31 out of 1,160 to receive 200 Shares
0.33%
1,800
848
25 out of 848 to receive 200 Shares
0.33%
2,000
10,801
356 out of 10,801 to receive 200 Shares
0.33%
3,000
2,452
121 out of 2,452 to receive 200 Shares
0.33%
4,000
3,289
217 out of 3,289 to receive 200 Shares
0.33%
5,000
2,212
182 out of 2,212 to receive 200 Shares
0.33%
6,000
1,646
163 out of 1,646 to receive 200 Shares
0.33%
7,000
1,184
137 out of 1,184 to receive 200 Shares
0.33%
8,000
1,290
170 out of 1,290 to receive 200 Shares
0.33%
9,000
1,155
169 out of 1,155 to receive 200 Shares
0.33%
10,000
6,748
1,095 out of 6,748 to receive 200 Shares
0.32%
20,000
4,026
1,306 out of 4,026 to receive 200 Shares
0.32%
30,000
2,379
1,158 out of 2,379 to receive 200 Shares
0.32%
40,000
2,242
1,455 out of 2,242 to receive 200 Shares
0.32%
50,000
1,980
1,606 out of 1,980 to receive 200 Shares
0.32%
60,000
1,538
1,497 out of 1,538 to receive 200 Shares
0.32%

<<<PAGE 13>>>
13
NO. OF SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
70,000
1,224
200 Shares plus 166 out of 1,224 to receive additional 200 Shares
0.32%
80,000
1,172
200 Shares plus 349 out of 1,172 to receive additional 200 Shares
0.32%
90,000
1,001
200 Shares plus 460 out of 1,001 to receive additional 200 Shares
0.32%
100,000
5,599
200 Shares plus 3,483 out of 5,599 to receive additional 200 Shares
0.32%
200,000
3,514
600 Shares plus 830 out of 3,514 to receive additional 200 Shares
0.32%
Total
132,491
Total number of Pool A successful applicants: 22,682
POOL B
300,000
4,904
200 Shares plus 3,949 out of 4,904 to receive additional 200 Shares
0.12%
400,000
977
400 Shares plus 398 out of 977 to receive additional 200 Shares
0.12%
500,000
692
600 Shares plus 6 out of 692 to receive additional 200 Shares
0.12%
600,000
451
600 Shares plus 275 out of 451 to receive additional 200 Shares
0.12%
700,000
245
800 Shares plus 52 out of 245 to receive additional 200 Shares
0.12%
800,000
246
800 Shares plus 200 out of 246 to receive additional 200 Shares
0.12%
900,000
159
1,000 Shares plus 66 out of 159 to receive additional 200 Shares
0.12%
1,000,000
718
1,200 Shares plus 13 out of 718 to receive additional 200 Shares
0.12%
2,000,000
262
2,400 Shares plus 9 out of 262 to receive additional 200 Shares
0.12%
3,000,000
92
3,600 Shares plus 5 out of 92 to receive additional 200 Shares
0.12%
4,000,000
52
4,800 Shares plus 4 out of 52 to receive additional 200 Shares
0.12%
5,000,000
48
6,000 Shares plus 4 out of 48 to receive additional 200 Shares
0.12%
6,000,000
22
7,200 Shares plus 2 out of 22 to receive additional 200 Shares
0.12%
6,999,400
104
8,400 Shares plus 12 out of 104 to receive additional 200 Shares
0.12%
Total
8,972
Total number of Pool B successful applicants: 8,972

<<<PAGE 14>>>
14
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or indirectly, 
provided by the Company, its group of single largest shareholder, Directors or syndicate members 
to any placees or the public (as the case may be) and the consideration payable by them for each 
Share of the Company subscribed for or purchased by them is the same as the final Offer Price 
determined by agreement between the Company and the Sponsor-Overall Coordinators (for 
themselves and on behalf of other Overall Coordinator and the Underwriters), in addition to any 
brokerage, AFRC transaction levy, SFC transaction levy and trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Allocation of H Shares to existing minority shareholders and their close associates with a 
waiver from the strict compliance with Rule 10.04 of the Listing Rules and a prior consent 
under paragraph 1C(2) of the Placing Guidelines
As disclosed in the Prospectus, the Company has applied to the Stock Exchange, and the Stock 
Exchange has granted, a waiver from the strict compliance with Rule 10.04 of the Listing Rules and 
a consent under paragraph 1C(2) of the Placing Guidelines to permit the Company to allocate such 
Offer Shares certain existing minority Shareholders who (i) hold less than 5% of the voting rights 
in our Company prior to the completion of the Global Offering and (ii) are not and will not become 
(upon the completion of the Global Offering) core connected persons of our Company or the close 
associates of any such core connected person (together, the “existing minority shareholder(s)”), 
on the following conditions:
(i)	
each of the existing minority shareholders to whom our Company may allocate the H Shares 
under the International Offering has less than 5% of the voting rights in our Company prior to 
the completion of the Global Offering;
(ii)	 each of the existing minority shareholders is not, and will not be, a core connected person of 
our Company or any close associate of any such core connected person immediately prior to or 
following the Global Offering;
(iii)	 each of the existing minority shareholders does not have the power to appoint Directors or 
have any other special rights in our Company;
(iv)	 allocation to the existing minority shareholders and their close associates will not affect our 
Company’s ability to satisfy the public float requirement as prescribed by the Stock Exchange 
under the waiver in respect of the strict compliance with the requirements of Rule 8.08 (as 
amended and replaced by Rule 19A.13A(2) when applied to PRC issuers with other listed 
shares) of the Listing Rules;

<<<PAGE 15>>>
15
(v)	 based on discussions between our Company and the Sponsor-overall Coordinators and 
confirmations required to be submitted to the Stock Exchange by the Joint Sponsors, the 
Company will confirm to the Stock Exchange that:
(a)	 in case of participation as cornerstone investors, no preferential treatment has been, nor 
will be, given to the existing minority shareholders and/or their close associates by virtue 
of their relationship with our Company, other than the preferential treatment of assured 
entitlement under a cornerstone investment following the principles set out in Chapter 
4.15 of the Guide, and the existing minority shareholders’ or their close associate’s 
cornerstone investment agreements do not contain any material terms which are more 
favorable to the existing minority shareholders or their close associate those in other 
cornerstone investment agreements; or
(b)	 in case of participation as placees, no preferential treatment will be given to the existing 
minority shareholders and/or their close associates by virtue of their relationship with our 
Company in any allocation in the placing tranche
(vi)	 in the case of participation as placees, the Overall Coordinators will confirm to the Stock 
Exchange that no preferential treatment has been, nor will be, given to any of the existing 
minority shareholders or their close associates by virtue of their relationship with our 
Company in any allocation in the International Offering; and
(vii)	the Joint Sponsors will confirm to the Stock Exchange that the confirmations provided to the 
Stock Exchange by our Company and the Sponsor-overall Coordinators and to the best of their 
knowledge and belief, they have no reason to believe that the existing minority shareholders 
and/or their close associates received any preferential treatment in any allocation in the placing 
tranche either as cornerstone investors or as placees by virtue of their relationship with our 
Company, other than, in the case of participation as cornerstone investors, the preferential 
treatment of assured entitlement under a cornerstone investment following the principles set 
out in Chapter 4.15 of the Guide, and details of allocation to the existing minority shareholders 
and/or their close associates will be disclosed in this prospectus (for cornerstone investors) and 
allotment results announcement (for both cornerstone investors and placees) of our Company.
Please refer to the section headed “Waivers from Strict Compliance with Listing Rules and 
Exemption from Compliance with the Companies (Winding Up and Miscellaneous Provisions) 
Ordinance — Allocation of H Shares to Existing Minority Shareholders and Their Close 
Associates” in the Prospectus for further details of the waiver and consent. The allocation of Offer 
Shares to such Existing Minority Shareholders is in compliance with all the conditions under the 
waiver/consent granted by the Stock Exchange.

<<<PAGE 16>>>
16
Allocations of Offer Shares to certain Cornerstone Investors and/or their close associates with 
a consent under paragraph 18 of Chapter 4.15 of the Guide
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 
of the Guide for New Listing Applicants to permit the Company to allocate further Offer Shares in 
the International Offering to certain Cornerstone Investors and/or their close associates as placees, 
subject to the following conditions (the “Size-based Exemption”):
(a)	 The final offering size of the Global Offering will exceed HK$1 billion;
(b)	 Offer Shares allocated to all existing shareholders and their close associates (whether as 
cornerstone investors and/or as placees) as permitted under the exemption granted by the Stock 
Exchange will not exceed 30% of the total number of Shares offered;
(c)	 Each of the Directors, chief executives and single largest shareholder group of the Company 
has confirmed that no Offer Shares will be allocated to any of the Directors, chief executives 
and single largest shareholder group of the Company or their respective close associates, and 
each of them will provide the confirmations upon the completion of the bookbuilding process;
(d)	 the allocation to size-based exemption participants will not affect the Company’s ability to 
satisfy its public float requirement as prescribed by the Stock Exchange under the waiver from 
strict compliance with the requirements of Rule 8.08(1) (as amended and replaced by Rule 
19A.13A) of the Listing Rules; and
(e)	 the details of allocation to the Size-based Exemption Participants under the size-based 
exemption will be disclosed in the allotment results announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted 
by the Stock Exchange.
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates 
and Cornerstone Investors, please refer to the section headed “Allotment Results Details — 
International Offering — Allotees with Waivers/Consents Obtained” in this announcement.
Placing to connected clients with consent under paragraph 1C(1) of the Placing Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines.

<<<PAGE 17>>>
17
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing 
Guidelines to permit the Company to allocate such Offer Shares in the International Offering to the connected clients. The allocation of 
Offer Shares to such connected clients is in compliance with all the conditions under the consent granted by the Stock Exchange. Details of 
the placement to connected clients are set out below:
No.
Connected Distributor
Connected Client
Relationship
Identities of the ultimate 
beneficial owners of the Offer 
Shares or, where applicable, 
details of the structured 
products under which the 
subscription by the Connected 
Client was made (e.g. OTC total 
return swaps)
Whether the Connected Client 
is a collective investment 
scheme which is not 
authorised by the SFC or is 
expected to hold the Offer 
Shares on behalf of such 
scheme
Maximum amount of Offer 
Shares to be allocated to the 
Connected Client 
Note 1
Approximate percentage of 
total number of Offer Shares 
under the Global Offering 
Note 1
Approximate percentage of 
total issued share capital after 
the Global Offering 
Note 1
Part A — Connected Clients holding the beneficial interest of the Offer Shares on a non-discretionary basis on behalf of independent third parties
1.
Guotai Junan Securities 
(Hong Kong) Limited 
(“GTJA Securities”)
Guotai Junan Investment 
(Hong Kong) Limited 
(“GTJA Investment”)
Note (3) below.
N/A
No
969,200
0.69%
0.07%
2.
Guotai Junan 
Investments 
(Hong Kong) Limited 
(“GTHT”)
Note (5) below
N/A
No
3,105,400
2.22%
0.22%
3.
CITIC Securities 
Brokerage (HK) Limited 
(“CITIC Brokerage”)
CITIC Securities 
International Capital 
Management Limited 
(1) 
(“CSICM”)
Note (2) below.
N/A
No
11,600
0.01%
0.001%

<<<PAGE 18>>>
18
No.
Connected Distributor
Connected Client
Relationship
Identities of the ultimate 
beneficial owners of the Offer 
Shares or, where applicable, 
details of the structured 
products under which the 
subscription by the Connected 
Client was made (e.g. OTC total 
return swaps)
Whether the Connected Client 
is a collective investment 
scheme which is not 
authorised by the SFC or is 
expected to hold the Offer 
Shares on behalf of such 
scheme
Maximum amount of Offer 
Shares to be allocated to the 
Connected Client 
Note 1
Approximate percentage of 
total number of Offer Shares 
under the Global Offering 
Note 1
Approximate percentage of 
total issued share capital after 
the Global Offering 
Note 1
Part A — Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties
3.
GTJA Securities
Fullgoal Fund 
Management Co., Ltd. 
(“Fullgoal Fund”)
Note (1) below.
N/A
No
192,200
0.14%
0.01%
Fullgoal Asset 
Management (HK) 
Limited (“Fullgoal 
HK”)
N/A
No
197,800
0.14%
0.01%
4.
Orient Securities (Hong 
Kong) Limited
China Universal Asset 
Management (Hong 
Kong) Company Limited 
(“China Universal 
(HK)”)
Note (4) below.
N/A
No
390,000
0.28%
0.03%
5
CITIC Securities 
Brokerage (HK) Limited 
(“CITIC Brokerage”)
CHINA ASSET 
MANAGEMENT 
(HONG KONG) 
LIMITED (“China 
Asset Management”)
Note (5) below.
N/A
No
13,000
0.01%
0.001%

<<<PAGE 19>>>
19
Notes:
(1)	
Fullgoal Fund and Fullgoal HK are members of the same group of GTJA Securities.
(2)	
CSICM is a member of the same group of companies as CITICS Brokerage.
(3)	
Both GTJA Investment and Guotai Junan Securities are indirect wholly-owned subsidiaries of Guotai Haitong Securities 
Co. Ltd., the A shares of which are listed on the Shanghai Stock Exchange (601211.SH) and the H shares are listed on the 
Hong Kong Stock Exchange (02611.HK). Therefore, GTJA Investment and Guotai Junan Securities are members of the 
same group of companies.
(4)	
China Universal (HK) is a wholly owned subsidiary of China Universal Asset Management Company Limited (“CUAM”). 
CUAM is owned by Orient Securities Co., Ltd, the group company of Orient Securities as to 35.412%.
(5)	
Both GTINV and Guotai Junan Securities are indirect wholly-owned subsidiaries of Guotai Haitong Securities Co. Ltd., 
the A shares of which are listed on the Shanghai Stock Exchange (601211.SH) and the H shares are listed on the Hong 
Kong Stock Exchange (02611.HK). Therefore, GTINV and Guotai Junan Securities are members of the same group of 
companies.
(6)	
China Asset Management is owned as to 62.2% by CITIC Securities Company Limited, which is holding company of CITIC 
Brokerage. China Asset Management is a member of the same group of companies as CITICS Brokerage

<<<PAGE 20>>>
20
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
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
investors should read the Prospectus dated February 5, 2026 issued by Shenzhen Woer Heat-
Shrinkable Material Co., Ltd. for detailed information about the Global Offering described below 
before deciding whether or not to invest in the H Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Sole Sponsor and the Sponsor-
Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall 
be entitled to terminate its obligations under the Hong Kong Underwriting Agreement with 
immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — 
Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on 
the Listing Date (which is currently expected to be on Friday, February 13, 2026).
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering, the number of the H Shares to be held by 
the public represents approximately 10.07% of the total issued share capital of our Company, the 
Company will therefore satisfy the public float requirement as required under Rule 19A.13A(2)(a) 
of the Listing Rules.

<<<PAGE 21>>>
21
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the H Shares of the Company at the time of Listing. Based on the 
final Offer Price of HK$20.09 per H Share, the Company satisfies the free float requirement under 
Rule 8.08A (as amended and replaced by Rule 19A.13C) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering: (i) the Shares 
will be held by at least 300 Shareholders at the time of Listing, in compliance with Rule 8.08(2) 
of the Listing Rules; (ii) the three largest public Shareholders will not hold more than 50% of the 
H Shares held in public hands at the time of Listing, in compliance with Rules 8.08(3) and 8.24 of 
the Listing Rules; (iii) no placee will, individually, be placed more than 10% of the enlarged issued 
share capital of the Company immediately after the Global Offering; and (iv) there will not be any 
new substantial Shareholder (as defined in the Listing Rules) immediately after the Global Offering.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, February 
13, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting — Underwriting Arrangements 
and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade the H Shares on the basis of publicly available allocation 
details prior to the receipt of H Share certificates or prior to the H Share certificates becoming valid 
evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Friday, 
February 13, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Friday, February 13, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 200 H Shares each, and the stock code of the H Shares will be 
9981.
By order of the Board
Shenzhen Woer Heat-Shrinkable Material Co., Ltd.
Mr. Zhou Heping
Executive Director and Chairperson of the Board
Hong Kong, February 12, 2026
As of the date of this announcement, the board of directors of the Company comprises: (i) Mr. Zhou Heping, Ms. Yi Huarong, 
Mr. Liu Zhanli, Mr. Xia Chunliang and Ms. Deng Yan as executive Directors; (ii) Dr. Li Wenyou as non-executive Director; and 
(iii) Mr. Zeng Fanyue, Ms. Dai Bingjie and Mr. Wang Dong as independent non-executive Directors.
