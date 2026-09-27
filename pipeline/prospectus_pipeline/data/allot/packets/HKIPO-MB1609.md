# 配发结果公告抽取任务：1609.HK Star Sports Medicine Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**04/05/2026 22:50**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0504/2026050403728.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1609.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
defined in the prospectus dated April 24, 2026 (the “Prospectus”) of Star Sports Medicine Co., Ltd. (北京天星醫療股
份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the Prospectus for 
detailed information about the Global Offering described below before deciding whether or not to invest in the Offer 
Shares. Any investment decision in relation to the Offer Shares should be taken solely in reliance on the information 
provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities in 
the United States. The securities mentioned herein have not been, and will not be, registered under the United States 
Securities Act of 1933, as amended (the “U.S. Securities Act”). The securities may not be offered or sold in the 
United States except pursuant to an exemption from the registration requirements of the U.S. Securities Act and in 
compliance with any applicable state securities laws, or outside the United States unless in compliance with Regulation 
S under the U.S. Securities Act. There will be no public offer of securities in the United States. The Offer Shares are 
being offered and sold outside the United States in offshore transactions in reliance on Regulation S under the U.S. 
Securities Act.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to terms and conditions set out in 
the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not 
resident in Hong Kong.
Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall, in their sole and absolute discretion, be entitled to 
terminate their obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence 
of any of the events set out in the paragraph headed “Underwriting — Underwriting Arrangements and Expenses — 
The Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong 
Kong time) on the Listing Date (which is currently expected to be on Tuesday, May 5, 2026).

<<<PAGE 2>>>
2
STAR SPORTS MEDICINE CO., LTD.
北京天星醫療股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under the
Global Offering
:
8,421,850 H Shares
Number of Hong Kong Offer Shares:
:
842,200 H Shares
Number of International Offer Shares
:
7,579,650 H Shares
Offer Price
:
HK$98.50 per H Share, plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
Hong Kong Stock Exchange trading fee of 
0.00565% and AFRC transaction levy of 
0.00015%
Nominal value
:
RMB1.00 per H Share
Stock code
:
1609
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners
and Joint Lead Managers
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
STAR SPORTS MEDICINE CO., LTD.
北京天星醫療股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated April 24, 2026 (the “Prospectus”) of Star Sports 
Medicine Co., Ltd. (北京天星醫療股份有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company Information
Stock code
1609
Stock short name
STAR SPORTS 
 MED
Dealings commencement date
May 5, 2026*
* 
see note at the end of the announcement
Price Information
Offer Price
HK$98.50
Offer Shares and Share Capital
Number of Offer Shares
8,421,850
Number of Offer Shares in Hong Kong Public Offering
842,200
Number of Offer Shares in International Offering
7,579,650
Number of issued Shares upon Listing
54,831,344

<<<PAGE 4>>>
4
Proceeds
Gross proceeds (Note)
HK$829.6 million
Less: Estimated listing expenses payable based on Offer Price
HK$71.2 million
Net proceeds
HK$758.4 million
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of proceeds, 
please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
300,735
No. of successful applications
16,844
Subscription level
7,823.13 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong 
 Public Offering
842,200
No. of Offer Shares reallocated from the International Offering
N/A
Final no. of Offer Shares under the Hong Kong Public Offering
842,200
% of Offer Shares under the Hong Kong Public Offering to the 
 Global Offering
10.00%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can refer to the designated 
results of allocations website at www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
the “Allotment Results” page of the White Form eIPO service at www.eipo.com.hk/eIPOAllotment for the full list of 
allottees.
INTERNATIONAL OFFERING
No. of placees
71
Subscription Level
10.41 times
No. of Offer Shares initially available under the International Offering
7,579,650
No. of Offer Shares reallocated to the Hong Kong Public Offering
N/A
Final no. of Offer Shares under the International Offering
7,579,650
% of Offer Shares under the International Offering to the 
 Global Offering
90.00%

<<<PAGE 5>>>
5
The Directors confirm that, to the best of their knowledge, information and belief, save for a 
waiver from strict compliance with Rule 10.04 of the Listing Rules, consents under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) and Chapter 4.15 of the 
Guide for New Listing Applicants (“Listing Guide”) granted by the Stock Exchange to permit the 
Company to, among other things, place certain H Shares in the International Offering to existing 
Shareholders and/or their close associates, (i) none of the Offer Shares subscribed by the placees 
and the public have been financed directly or indirectly by the Company, any of the Directors, 
chief executive of the Company, substantial shareholders, existing shareholders of the Company or 
any of its subsidiaries or their respective close associates; (ii) none of the placees and the public 
who have purchased the Offer Shares are accustomed to taking instructions from the Company, any 
of the Directors, chief executive of the Company, substantial shareholders, existing shareholders 
of the Company or any of its subsidiaries or their respective close associates in relation to the 
acquisition, disposal, voting or other disposition of Shares registered in his/her/its name or 
otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of 
Offer 
Shares 
allocated
% of 
Offer 
Shares
% of total 
issued 
share 
capital 
after 
the Global 
Offering
Existing 
shareholders 
or their close 
associates
JSC International Investment Fund SPC 
 (“JSC International”) for and on behalf of JSC 
 International Investment Fund SPC-Shenghai SP 
 (“Shenghai SP”)
1,968,550
23.37%
3.59%
No
OAP IV (HK) Limited (奧博亞洲四期(香港)有限公司) 
 (“OAP IV”) (Note 1)
397,650
4.72%
0.73%
Yes
Greater Bay Area Development Fund Management 
 Limited (大灣區發展基金管理有限公司) 
 (“GBAD Fund Management”) for and on behalf of the 
 Managed Account of Mega Prime Development Limited 
 (“Mega Prime”)
318,100
3.78%
0.58%
No
GBAD Fund Management for and on behalf of the 
 Managed Account of Poly Platinum Enterprises Limited 
 (“Poly Platinum”)
238,600
2.83%
0.44%
No
Note:
1. 
OAP IV is our existing Shareholder. The Company has applied to the Stock Exchange, and the Stock Exchange 
has granted a waiver under Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) of the Placing 
Guidelines in relation to the subscription of the Offer Shares as Cornerstone Investor by OAP IV pursuant to 
the anti-dilution right. For further details, please refer to the section headed “Waiver from Strict Compliance 
with the Listing Rules — Waiver under Rule 10.04 and Consent under Paragraph 1C(2) of Appendix F1 to the 
Listing Rules in Respect of Subscriptions of Offer Shares by Existing Shareholders as Cornerstone Investors” 
in the Prospectus and the section headed “Allotment Results Details — International Offering — Allottees with 
waiver/consents obtained” in this announcement.

<<<PAGE 6>>>
6
Allottees with waiver/consents obtained
Investor
No. of 
Offer 
Shares 
allocated
% of 
Offer 
Shares
% of 
total 
issued 
share 
capital 
after the 
Global 
Offering
Relationship
Allottees with consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to 
connected clients(Note 1)
China Asset Management (Hong 
Kong) Limited  
(“China AMC”)
750
0.01%
0.00%
A connected client of CLSA Limited 
 (“CLSA”)
China Galaxy International 
Investment Co., Limited 
(“CGII”)
397,600
4.72%
0.73%
A connected client of China Galaxy 
 International Securities (Hong Kong) 
 Co., Limited (“CGIS”)
China Universal Asset 
Management (Hong Kong) 
Company Limited  
(“China Universal (HK)”)
500
0.01%
0.00%
A connected client of Orient Securities 
 (Hong Kong) Limited 
 (“Orient Securities”)
CITIC Securities International 
Capital Management Limited 
(“CSICM”)
1,200
0.01%
0.00%
A connected client of CLSA
Orient Asset Management  
(Hong Kong) Limited  
(“Orient AM”)
4,000
0.05%
0.01%
A connected client of Orient Securities
Hong Kong Haicheng Capital 
Limited (“Haicheng Capital”)
440,300
5.23%
0.80%
A connected client of Orient Securities
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to allocation to existing Shareholders and/or their 
close associates as Cornerstone Investors or placees (Note 2)
CGII
397,600
4.72%
0.73%
A close associate of the Existing 
 Shareholders (Note 3)
Haicheng Capital
440,300
5.23%
0.80%
A close associate of the Existing 
 Shareholders
OAP IV (Note 4)
397,650
4.72%
0.73%
A cornerstone investor and an 
 existing Shareholder

<<<PAGE 7>>>
7
Notes:
1. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to connected 
clients, please refer to the section headed “Additional Information – Placing to connected clients with a prior 
consent under paragraph 1C(1) of the Placing Guidelines” in this announcement.
2. 
The Stock Exchange has granted a waiver from the strict compliance with Rule 10.04 of the Listing Rules and 
a consent under paragraph 1C(2) of the Placing Guidelines to permit Offer Shares to be placed to the above 
placee who are close associate of certain existing Shareholders. Please refer to the section headed “Additional 
Information – Placing to close associates of existing Shareholders as placees with a waiver from the strict 
compliance with Rule 10.04 of the Listing Rules and a prior consent under paragraph 1C(2) of the Placing 
Guidelines” in this announcement.
3. 
As defined in Note 6 to the section headed “Additional Information – Placing to close associates of existing 
Shareholders as placees with a waiver from the strict compliance with Rule 10.04 of the Listing Rules and a 
prior consent under paragraph 1C(2) of the Placing Guidelines” in this announcement.”
4. 
As disclosed in the Prospectus, OAP IV, as one of the Pre-IPO Investors, has the right pursuant to the August 
2025 Supplemental Agreement to purchase up to the number of ordinary shares of the Company offered in the 
Global Offering at the Offer Price that enables it to maintain its ownership interest percentage in the Company 
immediately prior to a qualified IPO (the “OAP IV Entitled Shares”) (the “OAP IV Anti-Dilution Right”). 
In the Global Offering, OAP IV will exercise the OAP IV Anti-Dilution Right to subscribe for additional 
Offer Shares at the Offer Price as a cornerstone investor in the International Offering. Following the exercise 
of the OAP IV Anti-Dilution Right, OAP IV shall not own more than its percentage shareholding interest in 
the Company as at immediately before the Global Offering. The Stock Exchange has granted a waiver from 
strict compliance with Rule 10.04 of the Listing Rules, and a consent under paragraph 1C(2) of the Placing 
Guidelines, to allow OAP IV to subscribe for Offer Shares in the Global Offering as a cornerstone investor. 
Such waiver and consent were granted on the basis that, among other things, (a) the allocation to OAP IV 
is necessary in order to give effect to the OAP IV Anti-Dilution Right under the August 2025 Supplemental 
Agreement and such allocation will not affect the Company’s ability to satisfy the public float requirement 
under Rule 8.08 of the Listing Rules; (b) full disclosure of the OAP IV Anti-Dilution Right and the number 
of shares to be subscribed for by OAP IV will be made in the Prospectus, the allotment results announcement 
and the placee lists to be submitted to the Stock Exchange; (c) the OAP IV Entitled Shares will be subscribed 
for by OAP IV at the Offer Price and will not result in the percentage interest held by OAP IV in the Company 
increasing above the percentage interest held by OAP IV immediately prior to the Global Offering; and (d) 
the subscription of the OAP IV Entitled Shares by OAP IV will not have any impact on the Shares to be 
offered to the public investors in Hong Kong under the Hong Kong Public Offering, considering that OAP IV 
will subscribe for the OAP IV Entitled Shares in the International Offering at the same offer price and under 
substantially the same terms and conditions as other cornerstone investors in the Global Offering.

<<<PAGE 8>>>
8
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued 
Shares in 
the Company 
upon Listing
Last day 
subject to the 
lock-up 
undertakings (Note 1)
Mr. Dong Wenxing (Note 2)
15,382,400
28.05 %
May 4, 2027
Tianjin Yunkang Technology Center 
(Limited Partnership) (Note 2)
1,900,000
3.47%
May 4, 2027
Tianjin Puhe Enterprise Management 
Consulting Partnership (Limited 
Partnership) (Note 2)
1,094,401
1.99%
May 4, 2027
Tianjin Jikang Enterprise Management 
Consulting Partnership (Limited 
Partnership) (Note 2)
871,061
1.59%
May 4, 2027
Subtotal
19,247,862
35.10%
Notes:
1. 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Laws. The 
required lock-up for the Controlling Shareholders ends on May 4, 2026, being 12 months following the Listing 
Date.
2. 
The general partner of each of Tianjin Jikang, Tianjin Yunkang and Tianjin Puhe is Tianjin Bokang, which 
is held as to 99% by Mr. Dong and 1% by Ms. Zhang Di, our Non-Executive Director. Mr. Dong is the sole 
limited partner of both Tianjin Jikang and Tianjin Puhe. Tianjin Yunkang is an employee shareholding platform 
with 33 limited partners and Tianjin Bokang as its sole general partner, among which Mr. Dong held 64.77% 
partnership interest, our executive Director Mr. He Lu, our Supervisors Mr. Xu Jingtao, Mr. Yang Tengfei and 
Ms. Wang Yali, and our chief operating officer and deputy general manager Mr. Liu Shaobin, held 5.67%, 
1.13%, 1.13%, 0.57% and 2.27% partnership interest, respectively, with the remaining partnership interest held 
by our employees or former employees. None of the other limited partners hold 5% or more in Tianjin Yunkang 
or served as a Director, Supervisor or senior management of the Company. For further details, see “History, 
Development and Corporate Structure — OUR EMPLOYEE SHAREHOLDING PLATFORM.”

<<<PAGE 9>>>
9
Pre-IPO Investors (as defined in the Prospectus)
Name
Number 
of H Shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued Shares 
in the Company 
upon Listing
Last day subject 
to the lock-up 
undertakings
(Note 1)
Xiamen Defu Yuean Investment 
Partnership Enterprise (Limited 
Partnership)/廈門德福悅安投資合夥
企業(有限合夥)
4,938,004
9.01%
May 4, 2027
Suzhou Junlian Xinkang Venture 
Investment (Limited Partnership)/蘇州
君聯欣康創業投資合夥企業(有限合
夥)
4,504,897
8.22%
May 4, 2027
BEST ALIVE LIMITED/沛昕有限公司
2,503,228
4.57%
May 4, 2027
OAP IV (HK) Limited/奧博亞洲四期(香
港)有限公司
4,306,666
7.85%
May 4, 2027
Anji Jintian Dinghao Enterprise 
Management Consulting Partnership 
(Limited Partnership)/安吉錦天鼎昊
管理諮詢合夥企業(有限合夥)
2,276,333
4.15%
May 4, 2027
Ningbo Meishan Bonded Port Qianyi 
Equity Investment Partnership 
Enterprise (Limited Partnership)/寧波
梅山保稅港區乾怡股權投資合夥企業
(有限合夥)
2,057,501
3.75%
May 4, 2027
Beijing Yahui Jinlin Venture Capital 
Partnership (Limited Partnership)/北
京雅惠錦霖創業投資合夥企業(有限
合夥)
1,873,568
3.42%
May 4, 2027
Beijing Jianxing Healthcare Industry 
Equity Investment Partnership 
(Limited Partnership)/北京建興醫療
健康產業股權投資合夥企業(有限合
夥)
1,405,177
2.56%
May 4, 2027
Galaxy Yuanhui Investment Co., Ltd/銀
河源匯投資有限公司
1,170,980
2.14%
May 4, 2027

<<<PAGE 10>>>
10
Name
Number 
of H Shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued Shares 
in the Company 
upon Listing
Last day subject 
to the lock-up 
undertakings
(Note 1)
Ningbo Xianda Venture Investment 
Partnership Enterprise (Limited 
Partnership)/寧波先達創業投資合夥
企業(有限合夥)
702,588
1.28%
May 4, 2027
Taizhou Sida Venture Capital 
Partnership (Limited Partnership)/台
州思達創業投資合夥企業(有限合夥)
224,828
0.41%
May 4, 2027
Khorgos Dadao Venture Capital Co., 
Ltd./霍爾果斯達到創業投資有限公司
9,368
0.02%
May 4, 2027
Langma No. 61 (Shenzhen) 
Entrepreneurship Investment Center 
(Limited Partnership)/朗瑪六十一號
(深圳)創業投資中心(有限合夥)
351,294
0.64%
May 4, 2027
Langma No. 62 (Shenzhen) 
Entrepreneurship Investment Center 
(Limited Partnership)/朗瑪六十二號
(深圳)創業投資中心(有限合夥)
351,294
0.64%
May 4, 2027
3W Rivus Fund
485,906
0.89%
May 4, 2027
Subtotal
27,161,632
49.54%
Notes:
1. 
Please see “History, Development and Corporate Structure — Information about our Pre-IPO Investors” in the 
Prospectus for the identities of the Pre-IPO Investors.
2. 
Pursuant to the applicable PRC law, within the 12 months following the Listing Date, all existing Shareholders 
(including the Pre-IPO Investors) are prohibited from disposing of any of the Shares held by them.

<<<PAGE 11>>>
11
Cornerstone Investors
Name
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued 
Shares in 
the Company 
upon Listing
Last day subject 
to the lock-up 
undertakings
(Note 1)
JSC International for and on behalf of 
Shenghai SP
1,968,550
3.59%
November 4, 2026
OAP IV
397,650
0.73%
November 4, 2026
GBAD Fund Management for and on 
behalf of the Managed Account of 
Mega Prime
318,100
0.58%
November 4, 2026
GBAD Fund Management for and on 
behalf of the Managed Account of Poly 
Platinum
238,600
0.44%
November 4, 2026
Note:
1. 
Each of the Cornerstone Investors has agreed that it will not, whether directly or indirectly, at any time during 
the period of six months from and inclusive of the Listing Date (the “Lock-up Period”), dispose of any of the 
Offer Shares they have purchased pursuant to the relevant Cornerstone Investment Agreements, save for certain 
limited circumstances, such as transfers to any of its wholly-owned subsidiaries who will be bound by the same 
obligations of such Cornerstone Investor, including the Lock-up Period restriction.

<<<PAGE 12>>>
12
PLACEE CONCENTRATION ANALYSIS
Placees
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering
Allotment 
as % of total 
Offer Shares
Number of 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing
Top 1
1,968,550
25.97%
23.37%
1,968,550
3.59%
Top 5
4,408,650
58.16%
52.35%
5,345,434
9.75%
Top 10
6,021,800
79.45%
71.50%
11,265,250
20.55%
Top 25
7,550,850
99.62%
89.66%
12,794,300
23.33%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHARE SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering
Allotment 
as % of 
total Offer 
Shares
Number of 
H Shares 
held upon 
Listing
% of total 
issued H 
Share capital 
upon Listing
Top 1
–
0.00%
0.00%
19,247,862
35.10%
Top 5
397,650
5.25%
4.72%
38,174,640
69.62%
Top 10
3,204,100
42.27%
38.05%
47,254,120
86.18%
Top 25
7,033,800
92.80%
83.52%
53,443,294
97.47%
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering
Allotment 
as % of 
total Offer 
Shares
Number of 
H Shares 
held upon 
Listing
Number of 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing
Top 1
–
0.00%
0.00%
19,247,862
19,247,862
35.10%
Top 5
397,650
5.25%
4.72%
38,174,640
38,174,640
69.62%
Top 10
3,204,100
42.27%
38.05%
47,254,120
47,254,120
86.18%
Top 25
7,033,800
92.80%
83.52%
53,443,294
53,443,294
97.47%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by Shareholders upon Listing.

<<<PAGE 13>>>
13
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
percentage 
allotted of the 
total number 
of H Shares 
applied for
50
69,002
1,034 out of 69,002 to receive 50 Shares
1.50%
100
33,023
499 out of 33,023 to receive 50 Shares
0.76%
150
7,906
121 out of 7,906 to receive 50 Shares
0.51%
200
8,839
137 out of 8,839 to receive 50 Shares
0.39%
250
6,365
99 out of 6,365 to receive 50 Shares
0.31%
300
4,315
69 out of 4,315 to receive 50 Shares
0.27%
350
2,525
41 out of 2,525 to receive 50 Shares
0.23%
400
3,268
54 out of 3,268 to receive 50 Shares
0.21%
450
2,640
44 out of 2,640 to receive 50 Shares
0.19%
500
14,849
248 out of 14,849 to receive 50 Shares
0.17%
600
3,021
52 out of 3,021 to receive 50 Shares
0.14%
700
2,213
39 out of 2,213 to receive 50 Shares
0.13%
800
2,195
39 out of 2,195 to receive 50 Shares
0.11%
900
3,215
59 out of 3,215 to receive 50 Shares
0.10%
1,000
11,642
218 out of 11,642 to receive 50 Shares
0.09%
1,500
5,867
119 out of 5,867 to receive 50 Shares
0.07%
2,000
5,426
118 out of 5,426 to receive 50 Shares
0.05%
2,500
4,462
104 out of 4,462 to receive 50 Shares
0.05%
3,000
3,995
99 out of 3,995 to receive 50 Shares
0.04%
3,500
2,804
74 out of 2,804 to receive 50 Shares
0.04%
4,000
2,715
76 out of 2,715 to receive 50 Shares
0.03%
4,500
2,348
69 out of 2,348 to receive 50 Shares
0.03%
5,000
15,606
483 out of 15,606 to receive 50 Shares
0.03%
10,000
10,525
481 out of 10,525 to receive 50 Shares
0.02%
15,000
6,565
397 out of 6,565 to receive 50 Shares
0.02%
20,000
5,554
417 out of 5,554 to receive 50 Shares
0.02%
25,000
4,436
399 out of 4,436 to receive 50 Shares
0.02%
30,000
3,881
406 out of 3,881 to receive 50 Shares
0.02%
35,000
2,806
338 out of 2,806 to receive 50 Shares
0.02%
40,000
2,677
369 out of 2,677 to receive 50 Shares
0.02%
45,000
2,145
332 out of 2,145 to receive 50 Shares
0.02%
50,000
8,074
1,388 out of 8,074 to receive 50 Shares
0.02%
264,904
Total number of Pool A successful applicants: 8,422

<<<PAGE 14>>>
14
Pool B
Number of 
H Shares 
applied for
Number
of valid 
applications
Basis of allocation/ballot
Approximate 
percentage 
allotted of the 
total number 
of H Shares 
applied for
60,000
8,471
1,291 out of 8,471 to receive 50 Shares
0.01%
70,000
3,525
567 out of 3,525 to receive 50 Shares
0.01%
80,000
2,918
493 out of 2,918 to receive 50 Shares
0.01%
90,000
2,074
368 out of 2,074 to receive 50 Shares
0.01%
100,000
6,323
1,174 out of 6,323 to receive 50 Shares
0.01%
150,000
3,699
839 out of 3,699 to receive 50 Shares
0.01%
200,000
2,196
589 out of 2,196 to receive 50 Shares
0.01%
250,000
1,528
505 out of 1,528 to receive 50 Shares
0.01%
300,000
1,045
415 out of 1,045 to receive 50 Shares
0.01%
350,000
807
375 out of 807 to receive 50 Shares
0.01%
421,100
3,245
1,806 out of 3,245 to receive 50 Shares
0.01%
35,831
Total number of Pool B successful applicants: 8,422
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
ADDITIONAL INFORMATION
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of certain 
distributors pursuant to the Placing Guidelines. Details of the placement to connected clients are 
set out below.
Connected 
client
Connected distributor
Relationship
Whether the 
connected client will 
hold beneficial 
interests of Offer 
Shares on a non-
discretionary 
or discretionary 
basis for independent 
third parties
No. of Offer 
Shares 
allocated 
to the 
connected 
client
% of Offer 
Shares
% of total 
issued share 
capital after 
the Global 
Offering
China AMC
CLSA Limited (“CLSA”), 
Futu Securities International 
(Hong Kong) Limited 
(“Futu Securities”)
See Note 1
Discretionary basis
750
0.01%
0.00%
CGII
China Galaxy International 
Securities (Hong Kong) Co., 
Limited (“CGIS”)
See Note 2
Non-discretionary basis
397,600
4.72%
0.73%

<<<PAGE 15>>>
15
Connected 
client
Connected distributor
Relationship
Whether the 
connected client will 
hold beneficial 
interests of Offer 
Shares on a non-
discretionary 
or discretionary 
basis for independent 
third parties
No. of Offer 
Shares 
allocated 
to the 
connected 
client
% of Offer 
Shares
% of total 
issued share 
capital after 
the Global 
Offering
China Universal 
 (HK)
Orient Securities (Hong 
Kong) Limited (“Orient 
Securities”)
See Note 3
Discretionary basis
500
0.01%
0.00%
CSICM
CLSA
See Note 4
Non-discretionary basis
1,200
0.01%
0.00%
Orient AM
Orient Securities
See Note 5
Discretionary basis
4,000
0.05%
0.01%
Haicheng Capital
Orient Securities
See Note 6
Discretionary basis
440,300
5.23%
0.80%
Notes:
1. 
China AMC is a member of the same group of companies as CLSA, China AMC will hold the Offer Shares in 
its capacity as discretionary fund manager managing assets on behalf of its underlying clients. To the best of 
China AMC’s knowledge after due enquiry, each underlying client of China AMC is an independent third party 
of China AMC, CLSA and the companies which are members of the same group of CLSA; Futu Securities is an 
ultimate beneficial owner of a fund managed by China AMC.
2. 
CGII and China Galaxy Securities (“CGS”) will enter into a series of cross border total return swap (TRS) 
transactions (collectively, the “CGII TRS”) with each other and the ultimate client (“CGII Ultimate Client”), 
pursuant to which CGII will hold the Offer Shares on a non-discretionary basis to hedge the CGII TRS while 
the economic risks and returns of the underlying Offer Shares are ultimately borne by the CGII Ultimate Client, 
subject to customary fees and commissions. The CGII TRS will be fully funded by the CGII Ultimate Client. 
During the terms of the CGII TRS, all economic returns of the Offer Shares subscribed by CGII will be passed 
to CGII Ultimate Client and all economic loss shall be borne by CGII Ultimate Client through the CGII TRS, 
and CGII will not take part in any economic return or bear any economic loss in relation to the Offer Shares.
The CGII Ultimate Client may exercise an early termination right to terminate the CGII TRS at any time from 
the issue date of the CGII TRS which should be on or after the date on which the Offer Shares are listed on 
the Stock Exchange. Upon the termination upon maturity or early termination of the CGII TRS by the CGII 
Ultimate Client, CGII will dispose of the Offer Shares on the secondary market and the CGII Ultimate Client 
will receive final settlement amount of the back-to-back TRS which should have taken into account all the 
economic returns or economic loss in relation to the Offer Shares. If upon the maturity of the CGII TRS, the 
CGII Ultimate Client intends to extend the investment period, subject to further agreement between CGII and 
the CGII Ultimate Client, the term of the CGII TRS could be extended by way of a new issuance or a tenor 
extension. Accordingly, CGII will extend the term of the back-to-back TRS by way of a new issuance or a tenor 
extension.
It is proposed that CGII will hold the legal title and the voting right of the Offer Shares by itself, and pass 
through the economic exposure to the CGII Ultimate Client, which place CGII TRS orders through their asset 
manager with CGII in connection with the IPO of the Company. Due to its internal policy, CGII will not 
exercise the voting right of the Offer Shares during the tenor of the back-to-back TRS.
During the life of the CGII TRS and back-to-back TRS, CGII may continue to hold the Offer Shares in its 
custodian account, or to hold some or all of the Offer Shares in a prime brokerage account for stock borrowing 
purposes.

<<<PAGE 16>>>
16
As permitted under the contractual arrangement with the CGII Ultimate Client, CGII will lend out its holding 
of underlying Offer Shares in the form of stock borrowing loans consistent with market practice to lower its 
finance costs, provided that CGII has the ability to call back the Offer Shares on loan at any time in order to 
satisfy its obligations under the back-to-back TRS to ensure the economic interests to be passed to the CGII 
Ultimate Client under the CGII TRS will remain unchanged.
To the best of CGII’s knowledge after having made all reasonable inquiries, the CGII Ultimate Client is an 
independent third party of CGII, and the companies which are members of the same group of CGIS.
Both CGII and CGIS are indirect wholly-owned subsidiaries of CGS, the A shares of which are listed on the 
Shanghai Stock Exchange (stock code: 601881), the H shares of which are listed on the Stock Exchange (stock 
code: 6881). CGII is a connected client (as defined under Appendix F1 to the Listing Rules) of CGIS, holding 
securities on a non-discretionary basis on behalf of independent third parties.
The CGII Ultimate Client is Hangzhou Haida Bicheng Venture Capital Management Partnership(L.P.) (杭州海
達必成創業投資管理合夥企業(有限合夥)) (“Haida Bicheng”), a limited partnership established in the PRC, 
whose general partner is Wang Wengang (王文剛) (“Mr. Wang”), who owns 41% of the interest of Haida 
Bicheng.
3. 
China Universal (HK) is a member of the same group of companies as Orient Securities. China Universal 
(HK) will hold the Offer Shares in its capacity as discretionary fund manager managing assets on behalf of 
its underlying clients. To the best of China Universal (HK)’s knowledge after due enquiry, certain underlying 
clients of China Universal (HK) have ultimate beneficial owners holding 30% or more interest of the respective 
discretionary fund, however each underlying client of China Universal (HK) is an independent third party of 
China Universal (HK), Orient Securities and the companies which are members of the same group of Orient 
Securities.
4. 
CITIC Securities Company Limited (“CITIC Securities”), the shares of which are listed on both the Shanghai 
Stock Exchange (stock code: 600030) and the Stock Exchange (stock code: 6030), is one of the domestic 
securities firms licensed to undertake cross-border derivatives trading activities. CITIC Securities entered into 
an International Swaps and Derivatives Association agreement (the “ISDA Agreement”) with its indirectly 
wholly-owned subsidiary, CSICM to set out the principal terms of any future total return swap between CITIC 
Securities and CSICM.
CLSA is a sponsor-overall coordinator of the Global Offering. Pursuant to the ISDA Agreement, CSICM, which 
intends to participate in the Global Offering as a placee, will hold the Offer Shares on a non-discretionary basis 
as the single underlying holder under a back-to-back total return swap (the “Back-to-back TRS”) to be entered 
by CSICM with CITIC Securities in connection with Client TRS (as defined below) placed by and fully funded 
(i.e. with no financing provided by CSICM) by the CSICM Ultimate Clients (as defined below), pursuant to 
which CSICM will pass the full economic exposure of the Offer Shares to the CSICM Ultimate Clients, which 
in effect, CSICM will hold the beneficial interest of the Offer Shares on behalf of the CSICM Ultimate Clients.
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the “CSICM Ultimate 
Clients”) cannot directly subscribe for the Offer Shares but may invest in derivative products issued by domestic 
securities firms licenced to undertake cross-border derivatives trading activities, such as CITIC Securities, 
with the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, the CSICM 
Ultimate Clients will place a total return swap order (the “Client TRS”) with CITIC Securities in connection 
with the Company’s IPO and CITIC Securities will place Back-to-back TRS orders to CSICM on the terms of 
the ISDA Agreement. In order to hedge its exposure under the Back-to-back TRS, CSICM participates in the 
Company’s IPO and subscribes the Offer Shares through placing order with CLSA during the International 
Offering.

<<<PAGE 17>>>
17
The following table sets forth the ultimate beneficial owners of CSICM:
Name (CSICM Ultimate Client)
Asset Manager
UBO of Asset 
Manager
UBO of CSICM 
Ultimate Client
Yucheng Xiangjiang Qiming Private Securities Investment 
Fund* (宇誠香江啟明私募證券投資基金)
Yucheng Private Fund Management (Hainan) Partnership 
(Limited Partnership)* (宇誠私募基金管理(海南)合夥企業
(有限合夥)) (“Yucheng”)
Ma Shuying (馬曙瑩)
Li Jianxue (李建學)
Liangpai Exclusive Fund No. 43 Private Securities Investment 
Fund* (量派專享四十三號私募證券投資基金)
Shanghai QuantPi Investment Limited (上海量派投資管理有限
公司) (“Shanghai Liangpai”)
Sun Lin (孫林), Yu 
Hang (餘航)
Sun Lin (孫林)
Evolution Darwin Zenshan No. 3 Private Securities Investment 
Fund* (進化論達爾文上善三號私募證券投資基金)
Evolution Asset Management co., Ltd. (海南進化論私募基金管
理有限公司) (“Hainan Evolution”)
Wang Yiping (王一平)
N/A1
Tongyi Taoli No. 1 Private Securities Investment Fund* (通怡
桃李 1 號私募證券投資基金)
Shanghai Tongyi Investment Management Co., Ltd. (上海通怡投
資管理有限公司) (“Shanghai Tongyi”)
Chu Yibo (儲貽波)
Wang Jing (王靜)
Tongyi Taoli No. 10 Private Securities Investment Fund* (通
怡桃李 10 號私募證券投資基金)
Shanghai Tongyi Investment Management Co., Ltd. (上海通怡投
資管理有限公司)
Chu Yibo (儲貽波)
N/A2
To the best knowledge of CSICM after making all reasonable enquiries, the CSICM Ultimate Clients are 
independent third parties of CSICM and CLSA, the companies which are members of the same group of 
companies as CLSA and the Company.
Pursuant to the terms of the contracts of the Back-to-back TRS and the Client TRS, during the tenor of the 
Back-to-back TRS and the Client TRS, all economic returns of the Offer Shares will be passed to the CSICM 
Ultimate Clients through the Back-to-back TRS and the Client TRS and all economic loss shall be borne by the 
CSICM Ultimate Clients. CSICM and CITIC Securities will not take any economic return or bear any economic 
loss in relation to the Offer Shares.
The CSICM Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time 
from the issue date of the Client TRS which should be on or after the date on which the Offer Shares are listed 
on the Stock Exchange. Upon the termination upon maturity or early termination of the Client TRS by the 
CSICM Ultimate Clients, CSICM will dispose of the Offer Shares on the secondary market and the CSICM 
Ultimate Clients will receive final settlement amount of the Back-to-back TRS which should have taken into 
account all the economic returns or economic loss in relation to the Offer Shares. If upon the maturity of the 
Client TRS, the CSICM Ultimate Clients intend to extend the investment period, subject to further agreement 
between CSICM and the CSICM Ultimate Clients, the term of the Client TRS could be extended by way of a 
new issuance or a tenor extension. Accordingly, CSICM will extend the term of the Back-to-back TRS by way 
of a new issuance or a tenor extension.
It is proposed that CSICM will hold the legal title and the voting right of the Offer Shares by itself, and pass 
through the economic exposure to the CSICM Ultimate Clients, which place Client TRS orders through their 
asset manager with CITIC Securities in connection with the IPO of the Company. Due to its internal policy, 
CSICM will not exercise the voting right of the Offer Shares during the tenor of the Back-to-back TRS.
During the life of the Client TRS and Back-to-back TRS, CSICM may continue to hold the Offer Shares in its 
custodian account, or to hold some or all of the Offer Shares in a prime brokerage account for stock borrowing 
purposes.
As permitted under the contractual arrangement with the CSICM Ultimate Clients, CSICM will lend out its 
holding of underlying Offer Shares in the form of stock borrowing loans consistent with market practice to 
lower its finance costs, provided that CSICM has the ability to call back the Offer Shares on loan at any time in 
order to satisfy its obligations under the Back-to-back TRS to ensure the economic interests to be passed to the 
CSICM Ultimate Clients under the Client TRS will remain unchanged.
1 
No ultimate beneficial owners holding 30% or more interest
2 
No ultimate beneficial owners holding 30% or more interest

<<<PAGE 18>>>
18
5. 
Orient AM will hold the Offer Shares in its capacity as discretionary fund manager managing assets on behalf of 
its underlying clients under the sub-funds, namely OSR Selective No.4 and OSR Voyage No.16. Orient AM is a 
member of the same group of companies as Orient Securities. To the best of Orient AM’s knowledge after due 
enquiry, each underlying client of Orient AM is an independent third party of Orient AM, Orient Securities and 
the companies which are members of the same group of Orient Securities.
6. 
Haicheng Capital’s securities account has been fully entrusted to Orient AM for management, and Orient AM 
has been granted all investment and trading authority over Haicheng Capital’s account. Orient AM is a member 
of the same group of companies as Orient Securities. Haicheng Capital’s ultimate beneficiary owners are Chen 
Qiao (陳巧) and Wang Wengang (王文剛) (“Mr. Wang”), who owns 41% and 40% of the issued capital of 
Haicheng Capital as of the date of this application.
Ningbo Xianda Venture Investment Partnership Enterprise (Limited Partnership) (寧波先達創業投資合夥企業
(有限合夥)) (“Ningbo Xianda”) is a limited partnership incorporated in the PRC on June 29, 2021. Taizhou 
Sida Venture Capital Partnership (Limited Partnership) (台州思達創業投資合夥企業(有限合夥)) (“Taizhou 
Sida”) is a limited partnership incorporated in the PRC on March 2, 2022. Khorgos Dadao Venture Capital Co., 
Ltd. (霍爾果斯達到創業投資有限公司) (“Khorgos Dadao”) is a limited liability company established in the 
PRC on February 28, 2017. The general partner of Ningbo Xianda and the sole shareholder of Khorgos Dadao 
is Tianjin Haida Venture Capital Management Co., Ltd. (天津海達創業投資管理有限公司) (“Tianjin Haida”), 
which is ultimately controlled by Mr. Wang, an Independent Third Party of the Company. The general partner 
of Taizhou Sida is Hangzhou Haida Bicheng Venture Capital Management Partnership(L.P.) (杭州海達必成
創業投資管理合夥企業(有限合夥)) (“Haida Bicheng”), a limited partnership established in the PRC, whose 
general partner is Mr. Wang, who owns 41% of the interest of Haida Bicheng. Accordingly, each of Ningbo 
Xianda, Taizhou Sida and Khorgos Dadao is under the common control of Mr. Wang (together as the “Existing 
Shareholders”). Haida Bicheng, being a company of which Mr. Wang is an ultimate beneficiary owner holding 
40% of its issued capital, and Mr. Wang controlling each of the Existing Shareholders, is a close associate of 
the Existing Shareholders. None of the limited partners holds 30% or more of limited partnership interests in 
either of Ningbo Xianda, Taizhou Sida and Haida Bicheng.
As of the Latest Practicable Date (as defined in the Prospectus), Ningbo Xianda, Taizhou Sida and Khorgos 
Dadao held 1.51%, 0.48% and 0.02% of the total issued shares capital of the Company.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraphs 1C(1) of the Placing Guidelines to permit the Company to allocate such 
Offer Shares in the International Offering to the connected clients listed above. The allocation of 
Offer Shares to such connected clients is in compliance with all the conditions under the consent 
granted by the Stock Exchange.
Placing to close associates of existing Shareholders as placees with a waiver from the strict 
compliance with Rule 10.04 of the Listing Rules and a prior consent under paragraph 1C(2) 
of the Placing Guidelines
The Company has applied to the Stock Exchange, and the Stock Exchange has granted, the waivers 
from the strict compliance with Rule 10.04 of the Listing Rules and consents under paragraph 
1C(2) of the Placing Guidelines to permit the Company to allocate such Offer Shares in the 
International Offering to close associates (the “Placees”) of Existing Shareholders (as defined 
below) on the following grounds which are consistent with the conditions as set out in the Chapter 
4.15 of the Guide for New Listing Applicant:
(a) 
the Joint Sponsors confirm that:
(i) 
each of the Existing Shareholders is interested in less than 5% of the Company’s voting 
rights before the Listing;
(ii) none of the Existing Shareholders or their close associates is a core connected person of 
the Company or its close associate;

<<<PAGE 19>>>
19
(iii) none of the Existing Shareholders or their close associates has the power to appoint any 
Directors to the Board or any other special rights upon the Listing;
(iv) as none of the Existing Shareholders or their close associates is a core connected 
person of the Company or its close associate, allocation to the Placees will not affect 
the Company’s ability to satisfy the public float requirement under Rule 8.08(1) (as 
amended and replaced by 19A.13A(1) for PRC issuers with no other listed shares) of 
the Listing Rules; and
(v) 
to the best of their knowledge and belief, no preferential treatment has been, nor 
will be, given to the Existing Shareholders or their close associates by virtue of their 
relationship with the Company in any allocation in the placing tranche;
(b) 
the Company confirms that no preferential treatment has been, nor will be, given to the 
Existing Shareholders or their close associates by virtue of their relationship with the 
Company in any allocation of the placing tranche;
(c) 
the Overall Coordinators confirm that, to the best of their knowledge and belief, no 
preferential treatment has been, nor will be, given to the Existing Shareholders or their close 
associates by virtue of their relationship with the Company in any allocation in the placing 
tranche; and
(d) 
details of the allocation of H Shares to the Existing Shareholders and their close associates 
will be disclosed in this allotment results announcement.
The allocation of Offer Shares to such Existing Shareholders and/or close associates of the Existing 
Shareholders is in compliance with all the conditions under the waivers/consents granted by the 
Stock Exchange.
For details of the allocation of Offer Shares to a close associate of the Existing Shareholders, 
please refer to the section headed “Allotment Results Details — International Offering — Allottees 
with waiver/consents obtained” in this announcement.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and trading fee payable.

<<<PAGE 20>>>
20
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
investors should read the Prospectus dated April 24, 2026 issued by Star Sports Medicine Co., 
Ltd. (北京天星醫療股份有限公司) for detailed information about the Global Offering described 
herein before deciding whether or not to invest in the Shares thereby being offered.
* 
Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-
Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall, 
in their sole and absolute discretion, be entitled to terminate their obligations under the 
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of 
the events set out in the paragraph headed “Underwriting — Underwriting Arrangements 
and Expenses — The Hong Kong Public Offering — Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is 
currently expected to be on Tuesday, May 5, 2026).

<<<PAGE 21>>>
21
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, (i) approximately 52.12% of the 
total number of issued Shares will be regarded as public float and the Company will satisfy the 
minimum percentage as prescribed under Rule 19A.13A(1) of the Listing Rules; (ii) the three 
largest public Shareholders do not hold more than 50% of the H Shares in public hands at the time 
of Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; (iii) there will not be 
any new substantial shareholder (as defined in the Listing Rules) of the Company immediately after 
the Global Offering; (iv) no placee will, individually, be placed more than 10% of the enlarged 
issued share capital of the Company immediately after the Global Offering; and (v) there will be at 
least 300 Shareholders at the time of Listing in compliance with Rule 8.08(2) of the Listing Rules.
In consideration that the total number of H Shares in issue upon Listing that are held by the public 
and not subject to any disposal restrictions is expected to be at least 10% of the total issued share 
capital of the Company, the Company is expected to satisfy the free float requirement under Rule 
19A.13C of the Listing Rules at the time of Listing.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. (Hong Kong time) on 
Tuesday, May 5, 2026, provided that the Global Offering has become unconditional and the right 
of termination described in the section headed “Underwriting — Underwriting Arrangements and 
Expenses — The Hong Kong Public Offering — Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade H Shares prior to the receipt of H Share certificates or the 
H Share certificates becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong Kong 
time) on Tuesday, May 5, 2026, it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Tuesday, May 5, 2026. The H Shares will be traded in board lots of 
50 H Shares each. The stock code of the Shares is 1609.
By order of the Board
Star Sports Medicine Co., Ltd.
Mr. Dong Wenxing
Chairman of the Board and Executive Director
Hong Kong, May 4, 2026
As at the date of this announcement, the Board comprises: (i) Mr. Dong Wenxing and Mr. He Lu 
as executive directors; (ii) Ms. Zhang Di, Mr. Chang Xi, Mr. David Guowei Wang, Ms. Yi Lin and 
Mr. Zhou Quan as non-executive directors and (iii) Mr. Lyu Zhenlin, Mr. Deng Yu, Mr. Liu Baojie 
and Mr. Wang Chunfei as independent non-executive directors.
