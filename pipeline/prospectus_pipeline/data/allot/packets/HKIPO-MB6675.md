# 配发结果公告抽取任务：6675.HK SENASIC Electronics Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**16/06/2026 21:59**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0616/2026061601760.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6675.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
defined in the prospectus dated 9 June 2026 (the “Prospectus”) issued by SENASIC Electronics Technology Co., Ltd. 
(琻捷電子科技(江蘇)股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the Prospectus for 
detailed information about the Company and the Global Offering described below before deciding whether or not to 
invest in the Offer Shares. Any investment decision in relation to the Offer Shares should be taken solely in reliance 
on the information in the Prospectus.
This announcement does not constitute an offer to sell or the solicitation of an offer to buy nor shall there be any sale 
of Offer Shares in any jurisdiction in which such offer, solicitation or sales would be unlawful. This announcement is 
not for release, publication or distribution, directly or indirectly, in or into the United States (including its territories 
and possessions, any state of the United States and the District of Columbia). This announcement does not constitute 
or form a part of any offer or solicitation to purchase or subscribe for securities in the United States or in any other 
jurisdiction. The Offer Shares have not been and will not be registered under the United States Securities Act of 1933, 
as amended from time to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the 
United States and may not be offered, sold, pledged or transferred within the United States, except in transactions 
exempt from, or not subject to, the registration requirements of the U.S. Securities Act. There will be no public offer 
of the Offer Shares in the United States. The Offer Shares are being offered and sold outside the United States in 
offshore transactions in reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited as 
stabilising manager (the “Stabilisation Manager”) (or its affiliates or any person acting for it), on behalf of the 
Underwriters, to the extent permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, 
may over-allocate or effect transactions with a view to stabilising or supporting the market price of the Shares at such 
price, in such amounts and in such manners as the Stabilising Manager, its affiliates or any person acting for it may 
determine and at a level higher than that which might otherwise prevail for a limited period after the Listing Date. 
However, there is no obligation on the Stabilising Manager (or its affiliates or any person acting for it) to conduct 
any such stabilising action. Such stabilising action, if taken, (a) will be conducted at the absolute discretion of the 
Stabilisation Manager (or its affiliates or any person acting for it) and in what the Stabilising Manager reasonably 
regards as the best interest of the Company, (b) may be discontinued at any time and (c) is required to be brought to 
an end within 30 days of the last day for lodging applications under the Hong Kong Public Offering. Such stabilising 
action, if taken, may be effected in all jurisdictions where it is permissible to do so, in each case in compliance with 
all applicable laws, rules and regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules 
(Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter 
571 of the Laws of Hong Kong).
Potential investors should be aware that stabilising action cannot be taken to support the price of the H Shares for 
longer than the stabilisation period which begins on the Listing Date and is expected to expire on the 30th day after 
the last day for the lodging of applications under the Hong Kong Public Offering. After this date, no further stabilising 
action may be taken, and demand for the H Shares and the price of the H Shares could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out in 
the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not 
resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint Sponsor-OCs (for themselves 
and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section 
headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date.

<<<PAGE 2>>>
2
䛺ܩ
SENASIC Electronics Technology Co., Ltd.
琻捷電子科技(江蘇)股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under 
the Global Offering
:
53,407,000 H shares (subject to 
 Over-allotment Option)
Number of Hong Kong Offer Shares
:
5,340,800 H Shares
Number of International Offer Shares
:
48,066,200 H Shares (subject to Over-allotment 
 Option)
Final Offer Price
:
HK$18.36 per H Share, plus brokerage of 
 1.0%, SFC transaction levy of 0.0027%, 
 AFRC transaction levy of 0.00015% and 
 Hong Kong Stock Exchange trading fee of 
 0.00565%
Nominal value
:
RMB0.05 per H Share
Stock code
:
6675
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers
Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
SENASIC ELECTRONICS TECHNOLOGY CO., LTD.
琻捷電子科技(江蘇)股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated 9 June 2026 (the “Prospectus”) issued 
by SENASIC Electronics Technology Co., Ltd.(琻捷電子科技(江蘇)股份有限公司) (the 
“Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company Information
Stock Code
6675
Stock Short Name
SENASIC
Dealings commencement date
17 June 2026*
* see note at the end of the announcement
Price Information
Offer Price
HK$18.36
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the Over-allotment Option)
53,407,000
Number of Offer Shares in Hong Kong Public Offering
5,340,800
Number of Offer Shares in International Offering (before exercise of the 
Over-allotment Option)
48,066,200
Number of issued Shares upon Listing (before exercise of the Over-
allotment Option and the options under the 2026 Pre-IPO Share Option 
Scheme)
379,041,820
Over-allocation
No. of Offer Shares over-allocated
2,855,800
- International Offering
2,855,800

<<<PAGE 4>>>
4
Proceeds
Gross proceeds(Note)
HK$980.55 million
 Less: Estimated listing expenses payable based on Offer Price
HK$68.03 million
Net Proceeds
HK$912.52 million
Note: Gross proceeds refer to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. In the event that 
the Over-allotment Option is exercised, the Company will adjust the allocation of the net proceeds on a pro rata 
basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFER
No. of valid applications
237,930
No. of successful applications
26,704
Subscription level
5,144.97 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong Public Offer
5,340,800
No. of Offer Shares reallocated from the International Offering
0
Final no. of Offer Shares under the Hong Kong Public Offering
5,340,800
% of Offer Shares under the Hong Kong Public Offer to the Global 
Offering
10%
Note: For details of the final allocation of H Shares to the Hon Kong Public Offering, investors can refer to 
www.hkeipo.hk/iporesult to perform a search by identification number or www.hkeipo.hk/iporesult for the full 
list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFER
No. of placees
105
Subscription Level
4.44 times
No. of Offer Shares initially available under the International Offer
48,066,200
No. of Offer Shares reallocated to the Hong Kong Public Offering
0
Final no. of Offer Shares under the International Offer (before exercise of 
the Over-allotment Option)
48,066,200
% of Offer Shares under the International Offer to the Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for a 
waiver under Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of Appendix 
F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange to permit 
the Company to allocate certain Offer Shares in the International Offering to a close associate 
of an existing shareholder as a cornerstone investor, (i) none of the Offer Shares subscribed by 
the placees and the public have been financed directly or indirectly by the Company, any of the 
Directors, chief executive of the Company, the Single Largest Group of Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates; and (ii) none of the placees and the public who have purchased the Offer Shares 
are accustomed to taking instructions from the Company, any of the Directors, chief executive 
of the Company, the Single Largest Group of Shareholders, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates in 
relation to the acquisition, disposal, voting or other disposition of H Shares registered in his/her/its 
name or otherwise held by him/her/it.

<<<PAGE 6>>>
6
The placees in the International Offering include the following:
Cornerstone Investors
Investor(1)
No. of Offer 
Shares 
allocated
% of Offer 
Shares(2)
% of total 
issued share 
capital after 
the Global 
Offering(2)
Existing 
shareholders 
or their 
close 
associates
Sunwoda Treasury (Hong 
Kong) Limited (欣旺達
財資(香港)有限公司)
2,156,800
4.04%
0.57%
No
Longwei Hong Kong 
Company Limited (香港
隆威國際貿易有限公司)
1,280,400
2.40%
0.34%
Yes
Oakwise Growth Fund  
SPC — Greater China 
Fund SP
4,007,600
7.50%
1.06%
No
Tembusu Limited
853,600
1.60%
0.23%
No
Andrew Y Yan (閻焱)
853,600
1.60%
0.23%
No
RIME Capital Limited  
(霧凇資本有限公司)
853,600
1.60%
0.23%
No
Thalassa Capital Dynamics 
SPC (acting for and 
on behalf of Thalassa 
Horizon SP)
2,685,000
5.03%
0.71%
No
Chample International 
Limited
1,633,800
3.06%
0.43%
No
Libra Stable Value and 
Fixed Income Segregated 
Portfolio Company 
acting for and on behalf 
of Libra Fixed Income 
One SP
1,089,200
2.04%
0.29%
No
Total
15,413,600
28.86%
4.07%

<<<PAGE 7>>>
7
Notes:
1. 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in 
the Prospectus.
2. 
Before any exercise of the Over-allotment Option or the options under the 2026 Pre-IPO Share Option 
Scheme.
Allottees with waiver/consents obtained
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares(1)
% of total 
issued share 
capital after 
the Global 
Offering(1)
Relationship
Allotees with consent under paragraph 1C(1) of Appendix F1 to the Listing Rules (the “Placing 
Guidelines”) in relation to allocations to connected clients(2)
SSIF Asset Management 
SPC-SSI & Affluence 
Capital IPO Strategy 
Opportunity Segregated 
Portfolio
54,400
0.10%
0.01%
Connected 
client as a 
placee
CITIC Securities 
International Capital 
Management Limited 
(“CSICM”)
400,000
0.75%
0.11%
Connected 
client as a 
placee
Guotai Junan Investments 
(Hong Kong) Limited 
(“GTJAI”)
544,600
1.02%
0.14%
Connected 
client as a 
placee
E Fund Management (Hong 
Kong) Co, Ltd. (“E 
Fund HK”)
3,400
0.01%
0.00%
Connected 
client as a 
placee
China Asset Management
 (Hong Kong) Limited
 (“China AM HK”)
3,400
0.01%
0.00%
Connected 
client as a 
placee
Huatai Capital Investment
 Limited (“HTCI”)
871,400
1.63%
0.23%
Connected 
client as a 
placee

<<<PAGE 8>>>
8
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares(1)
% of total 
issued share 
capital after 
the Global 
Offering(1)
Relationship
Allotee with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to allocation to a close associate of an existing 
shareholder as cornerstone investor (3)
Longwei Hong Kong 
Company Limited (香港隆
威國際貿易有限公司) (4)
1,280,400
2.40%
0.34%
A close 
associate of 
an existing 
shareholder 
as 
cornerstone 
investor
Notes:
1. 
Before any exercise of the Over-allotment Option or the options under the 2026 Pre-IPO Share Option Scheme.
2. 
Saved as listed out, the H Shares placed to such allottees are held on behalf of independent third parties (as 
defined in Chapter 4.15 of the Guide for New Listing Applicants) and are in compliance with all the conditions 
under the consent granted by the Stock Exchange. For details of the consent under paragraph 1C(1) of the 
Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations to 
connected clients, please refer to the section headed “Placing to connected clients with consents under paragraph 
1C(1) of the Placing Guidelines” in this announcement.
3. 
For details of the consents under paragraph 1C(2) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicant in relation to allocations to a close associate of an existing shareholder as 
cornerstone investor, please refer to the section headed “Placing to a close associate of an existing shareholder 
as cornerstone investor with a waiver under Rule 10.04 and consent under paragraph 1C(2) of the Placing 
Guidelines” in this announcement.
4. 
Longwei Hong Kong Company Limited (香港隆威國際貿易有限公司) (“Longwei HK”), a close associate (as 
defined in the Listing Rules) of Shanghai Baolong Automotive Corporation (上海保隆汽車科技股份有限公司) 
(“Baolong Automotive”), one of the Company’s existing shareholders and Pre-IPO Investors, has indicated to 
the Company its interest in participating in the Global Offering by making a cornerstone investment to subscribe 
for the Offer Shares. Further information of Baolong Automotive has been disclosed in the section headed 
“History, Development and Corporate Structure” of the Prospectus.

<<<PAGE 9>>>
9
LOCK-UP UNDERTAKINGS
Cornerstone Investors
Name
Number 
of Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option or the 
options under the 
2026 Pre-IPO 
Share Option 
Scheme is not 
exercised)
Last day subject 
to the lock-up 
undertakings
Sunwoda Treasury (Hong Kong) 
Limited (欣旺達財資(香港) 
有限公司)
2,156,800
0.57%
16 December 2026
Longwei Hong Kong Company 
Limited (香港隆威國際貿易 
有限公司)
1,280,400
0.34%
16 December 2026
Oakwise Growth Fund SPC — 
Greater China Fund SP
4,007,600
1.06%
16 December 2026
Tembusu Limited
853,600
0.23%
16 December 2026
Andrew Y Yan (閻焱)
853,600
0.23%
16 December 2026
RIME Capital Limited (霧凇資本
有限公司)
853,600
0.23%
16 December 2026
Thalassa Capital Dynamics SPC 
(acting for and on behalf of 
Thalassa Horizon SP)
2,685,000
0.71%
16 December 2026
Chample International Limited
1,633,800
0.43%
16 December 2026
Libra Stable Value and Fixed 
Income Segregated Portfolio 
Company acting for and on 
behalf of Libra Fixed Income 
One SP
1,089,200
0.29%
16 December 2026
Total
15,413,600
4.07%
In accordance with the respective Cornerstone Investment Agreement, the required lock-up ends on six 
months from the Listing Date, which is 16 December 2026. The Cornerstone Investors will cease to be 
prohibited from disposing of or transferring Shares after the indicated date.

<<<PAGE 10>>>
10
The Single Largest Group of Shareholders
Name(1)
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing 
Number of 
H Shares held 
in the Company 
subject to lock-
up undertakings 
upon Listing 
% of total issued 
H Shares after the 
Global Offering 
subject to lock-
up undertakings 
upon Listing (4)
% of shareholding
in the Company 
subject to lock – 
up undertakings 
upon Listing (4)
Last day subject 
to the lock-up
undertakings
Li Mengxiong (李夢雄) (2) 
(“Dr. Li”)
34,130,460
34,130,460
9.00%
9.00%
16 June 2027 (1) (3)
Li Shuguang (李曙光) (2) 
(“Mr. Li”)
13,586,460
13,586,460
3.58%
3.58%
16 June 2027 (1) (3)
Shanghai Chuangyingrui 
Enterprise Management 
Partnership (Limited 
Partnership) (上海創英銳企業
管理合夥企業(有限合夥)) (2) 
(“Shanghai Chuangyingrui”)
29,631,720
29,631,720
7.82%
7.82%
16 June 2027 (1) (3)
Shanghai Ruixinchuang Enterprise 
Management Partnership 
(Limited Partnership) (上海
銳芯創企業管理合夥企業
(有限合夥)) (2) (“Shanghai 
Ruixinchuang”)
24,838,700
24,838,700
6.55%
6.55%
16 June 2027 (1) (3)
Gongqingcheng SENASIC 
Investment Partnership (Limited 
Partnership) (共青城琻捷投
資合夥企業(有限合夥)) (2) 
(“Gongqingcheng SENASIC”)
2,830,980
2,830,980
0.75%
0.75%
16 June 2027 (1) (3)
Subtotal
105,018,320
105,018,320
27.71%
27.71%

<<<PAGE 11>>>
11
Notes:
1. 
For illustrative purposes only, this subsection lists only those members of the Single Largest Group of 
Shareholders who hold Shares directly in the Company. Pursuant to Rule 10.07 of the Listing Rules, each 
member of the Single Largest Group of Shareholders (namely, Dr. Li, Mr. Li, Shanghai Chuangyingrui, 
Shanghai Ruixinchuang, Shanghai Yaojun (as defined below) and Gongqingcheng SENASIC) has undertaken 
to the Stock Exchange and the Company that, except in connection with the Global Offering (including the 
Over-allotment Option), he/it will not, and will procure that the relevant registered holder(s) will not, without 
the prior written consent of the Joint Sponsor-OCs and unless otherwise in compliance with the applicable 
requirements of the Listing Rules: in the period commencing on the date by reference to which disclosure of its 
shareholdings in the Company is made in the Prospectus and ending on the date which is six months from the 
Listing Date, either directly or indirectly, dispose of, nor enter into any agreement to dispose of or otherwise 
create any options, rights, interests or encumbrances in respect of, any of the securities of the Company that 
he/it is shown to beneficially own in the Prospectus. For further details, please refer to the section headed 
“Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – Undertakings to 
the Stock Exchange pursuant to the Listing Rules – Undertakings by the Single Largest Group of Shareholders” 
in the Prospectus.
2. 
As of the date of this announcement, Dr. Li and Mr. Li, by virtue of the acting-in-concert arrangement, were 
collectively interested in approximately controlled 32.25% of the total issued share capital, comprising: (1) 
approximately 10.48% of the total issued share capital directly held by Dr. Li; (2) approximately 4.17% of the 
total issued share capital directly held by Mr. Li; (3) approximately 9.10% and 7.63% of the total issued share 
capital controlled by Dr. Li through Shanghai Chuangyingrui and Shanghai Ruixinchuang, respectively, both 
of which are the ESOP Platforms and controlled by Dr. Li; and (4) approximately 0.87% of the total issued 
share capital controlled by Dr. Li through Gongqingcheng SENASIC, being managed by Shanghai Yaojun 
Management Consulting Co., Ltd. (上海曜駿管理諮詢有限公司) (“Shanghai Yaojun”), a holding company 
wholly-owned by Dr. Li. Upon the Listing, without taking into account any Shares that may be issued upon 
exercise of the Over-allotment Option and under the 2026 Pre-IPO Share Option Scheme, Dr. Li and Mr. 
Li will be entitled to, directly and indirectly through Shanghai Chuangyingrui, Shanghai Ruixinchuang, 
Shanghai Yaojun and Gongqingcheng SENASIC, exercise 27.71% voting rights in the Company. Therefore, 
upon the Listing, Dr. Li, Mr. Li, Shanghai Chuangyingrui, Shanghai Ruixinchuang, Shanghai Yaojun and 
Gongqingcheng SENASIC will become the Single Largest Group of Shareholders.
3. 
According to the PRC Company Law, all existing Shareholders (including the Single Largest Group of 
Shareholders) are subject to a lock-up period of 12 months following the Listing Date.
4. 
The relevant number of shares and percentage are calculated without taking into account of any Shares that 
may be issued upon exercise of the Over-allotment Option or the options under the 2026 Pre-IPO Share Option 
Scheme.

<<<PAGE 12>>>
12
Other Existing Shareholders (other than the Single Largest Group of Shareholders and 
Cornerstone Investors)
Name
Number of 
Shares held 
in the Company 
subject to lock-up 
undertakings 
upon Listing
Number of 
H Shares held 
in the Company 
subject to lock-up 
undertakings 
upon Listing
% of total issued 
H Shares after 
the Global 
Offering subject
to lock-up 
undertakings 
upon Listing(1)
% of shareholding
in the Company 
subject to lock-up 
undertakings upon 
Listing(1)
Last day subject 
to the lock-up 
undertakings(2)
Gongqingcheng Yingruichuang Investment 
Partnership (Limited Partnership) (共
青城英銳創投資合夥企業(有限合夥)) 
(“Gongqingcheng Yingruichuang”)
6,388,320
6,388,320
1.69%
1.69%
16 June 2027
China State-Owned Enterprise Mixed-Ownership 
Reform Fund Co., Ltd. (中國國有企業混合所
有制改革基金有限公司)
19,701,600
19,701,600
5.20%
5.20%
16 June 2027
Hangzhou Chuangqian Investment Partnership 
(Limited Partnership) (杭州創乾投資合夥企
業(有限合夥))
19,547,160
19,547,160
5.16%
5.16%
16 June 2027
Changjiang Chendao (Hubei) New Energy 
Industry Investment Partnership (Limited 
Partnership) (長江晨道(湖北)新能源產業投
資合夥企業(有限合夥))
8,294,100
8,294,100
2.19%
2.19%
16 June 2027
Yibin Lvneng Equity Investment Partnership 
(Limited Partnership) (宜賓綠能股權投資合
夥企業(有限合夥))
5,182,380
5,182,380
1.37%
1.37%
16 June 2027
Yibin Chendao New Energy Industry Equity 
Investment Partnership (Limited Partnership) 
(宜賓晨道新能源產業股權投資合夥企業(有
限合夥))
2,421,600
2,421,600
0.64%
0.64%
16 June 2027
China Venture Capital Xinzhi Equity Investment 
Fund (Guangzhou) Partnership (Limited 
Partnership) (國風投新智股權投資基金(廣
州)合夥企業(有限合夥))
14,109,340
14,109,340
3.72%
3.72%
16 June 2027
Qingdao Huaxinchuangyuan Venture Capital 
Center (Limited Partnership) (青島華芯創原
創業投資中心(有限合夥))
12,039,300
12,039,300
3.18%
3.18%
16 June 2027
Xiamen Jianfa Emerging Industry Equity 
Investment No.16 Partnership Enterprise 
(Limited Partnership) (廈門建發新興產業股
權投資拾陸號合夥企業(有限合夥))
5,934,880
5,934,880
1.57%
1.57%
16 June 2027

<<<PAGE 13>>>
13
Name
Number of 
Shares held 
in the Company 
subject to lock-up 
undertakings 
upon Listing
Number of 
H Shares held 
in the Company 
subject to lock-up 
undertakings 
upon Listing
% of total issued 
H Shares after 
the Global 
Offering subject
to lock-up 
undertakings 
upon Listing(1)
% of shareholding
in the Company 
subject to lock-up 
undertakings upon 
Listing(1)
Last day subject 
to the lock-up 
undertakings(2)
Xiamen Jianfa Changrong No. 2 Equity 
Investment Partnership (Limited Partnership) 
(廈門建發長榕貳號股權投資合夥企業(有限
合夥))
1,978,300
1,978,300
0.52%
0.52%
16 June 2027
Qingdao Shangqi Huizhu Zhanxin Industry 
Investment Fund Partnership (Limited 
Partnership) (青島尚頎匯鑄戰新產業投資基
金合夥企業(有限合夥))
3,091,540
3,091,540
0.82%
0.82%
16 June 2027
Foshan Shangqi Delian Automotive Equity 
Investment Partnership (Limited Partnership) 
(佛山尚頎德聯汽車股權投資合夥企業(有限
合夥))
2,478,480
2,478,480
0.65%
0.65%
16 June 2027
Ningbo Meishan Bonded Port Zone Jiechuang 
Equity Investment Partnership (Limited 
Partnership) (寧波梅山保稅港區捷創股權投
資合夥企業(有限合夥))
1,239,240
1,239,240
0.33%
0.33%
16 June 2027
Geely Gongchuang No. 5 Investment (Tianjin) 
Partnership (Limited Partnership) (吉利共創
伍號投資(天津)合夥企業(有限合夥))
6,767,040
6,767,040
1.79%
1.79%
16 June 2027
Hai Feng Investment Holding Limited （海風投
資有限公司）
20,963,160
20,963,160
5.53%
5.53%
16 June 2027
Shenzhen Nanshan Hongtai Equity Investment 
Fund Partnership (Limited Partnership) (深圳
南山鴻泰股權投資基金合夥企業(有限合夥))
12,747,660
12,747,660
3.36%
3.36%
16 June 2027
Suzhou Jiyuan Haoyue Venture Capital 
Partnership (Limited Partnership) (蘇州紀源
皓月創業投資合夥企業(有限合夥))
5,656,320
5,656,320
1.49%
1.49%
16 June 2027
Suzhou Jiyuan Haoyuan Venture Capital 
Partnership (Limited Partnership) (蘇州紀源
皓元創業投資合夥企業(有限合夥))
4,194,480
4,194,480
1.11%
1.11%
16 June 2027
Zhuhai Gejin Guangfa Xinde Phase III 
Technology Venture Capital Fund (Limited 
Partnership) (珠海格金廣發信德三期科技創
業投資基金(有限合夥))
4,478,300
4,478,300
1.18%
1.18%
16 June 2027
Dongguan Guangfa Xinde Phase I Technology 
Venture Investment Partnership (Limited 
Partnership) (東莞廣發信德一期科技創業投
資合夥企業(有限合夥))
2,786,500
2,786,500
0.74%
0.74%
16 June 2027

<<<PAGE 14>>>
14
Name
Number of 
Shares held 
in the Company 
subject to lock-up 
undertakings 
upon Listing
Number of 
H Shares held 
in the Company 
subject to lock-up 
undertakings 
upon Listing
% of total issued 
H Shares after 
the Global 
Offering subject
to lock-up 
undertakings 
upon Listing(1)
% of shareholding
in the Company 
subject to lock-up 
undertakings upon 
Listing(1)
Last day subject 
to the lock-up 
undertakings(2)
Ningbo Meishan Bonded Port Area Cenyu 
Venture Capital Partnership (Limited 
Partnership) (寧波梅山保稅港區岑佑創業投
資合夥企業(有限合夥))
6,143,760
6,143,760
1.62%
1.62%
16 June 2027
Gongqingcheng Changshun Zhiying Venture 
Capital Partnership (Limited Partnership) (共
青城長舜智贏創業投資合夥企業(有限合夥))
5,260,260
5,260,260
1.39%
1.39%
16 June 2027
Shanghai Pudong Haiwang Integrated Circuit 
Industry Private Equity Fund Partnership 
Enterprise (Limited Partnership) (上海浦東海
望集成電路產業私募基金合夥企業(有限合
夥))
4,925,400
4,925,400
1.30%
1.30%
16 June 2027
Shanghai Baolong Automotive Corporation (上
海保隆汽車科技股份有限公司)
4,824,900
4,824,900
1.27%
1.27%
16 June 2027
Guangdong Guangqi Yuexiu Zhiyuan Industrial 
Investment Fund Partnership (Limited 
Partnership) (廣東廣祺越秀智源產業投資基
金合夥企業(有限合夥))
2,312,820
2,312,820
0.61%
0.61%
16 June 2027
Guangdong Guangqi Zhiyuan No. 6 Equity 
Investment Partnership (Limited Partnership) 
(廣東廣祺智源陸號股權投資合夥企業(有限
合夥))
2,312,820
2,312,820
0.61%
0.61%
16 June 2027
Mr. Zhou Yongsen (周永森)
4,625,580
4,625,580
1.22%
1.22%
16 June 2027
Mr. Ying Ting (應挺)
4,485,180
4,485,180
1.18%
1.18%
16 June 2027
Nanjing Jinti Venture Investment Partnership 
(Limited Partnership) (南京金體創業投資合
夥企業(有限合夥))
4,304,520
4,304,520
1.14%
1.14%
16 June 2027
Ma’anshan Huachun Baoxin Zhixin Equity 
Investment Partnership (Limited Partnership) 
(馬鞍山華淳保信智新股權投資合夥企業(有
限合夥))
3,135,420
3,135,420
0.83%
0.83%
16 June 2027
Zhuhai Huajin Lingyi Emerging Technology 
Industry Investment Fund (Limited 
Partnership) (珠海華金領翊新興科技產業投
資基金(有限合夥))
3,092,880
3,092,880
0.82%
0.82%
16 June 2027
Zhuhai Huajin Shangying No. 7 Equity 
Investment Fund Partnership (Limited 
Partnership) (珠海華金尚盈七號股權投資基
金合夥企業(有限合夥))
42,540
42,540
0.01%
0.01%
16 June 2027

<<<PAGE 15>>>
15
Name
Number of 
Shares held 
in the Company 
subject to lock-up 
undertakings 
upon Listing
Number of 
H Shares held 
in the Company 
subject to lock-up 
undertakings 
upon Listing
% of total issued 
H Shares after 
the Global 
Offering subject
to lock-up 
undertakings 
upon Listing(1)
% of shareholding
in the Company 
subject to lock-up 
undertakings upon 
Listing(1)
Last day subject 
to the lock-up 
undertakings(2)
Beijing Guoqi Intelligent Connected Vehicle 
Industry Investment Center (Limited 
Partnership) (北京國汽智能網聯汽車產業投
資中心(有限合夥))
2,955,240
2,955,240
0.78%
0.78%
16 June 2027
Shenzhen Huiyue Growth Investment Fund 
Enterprise (L.P.) (深圳市慧悅成長投資基金
企業(有限合夥))
2,220,360
2,220,360
0.59%
0.59%
16 June 2027
Shenzhen Tianhui Growth Investment Fund 
Enterprise (L.P.) (深圳市天慧成長投資基金
企業(有限合夥))
634,380
634,380
0.17%
0.17%
16 June 2027
Shihezi Mingzhao Equity Investment 
Management Co., Ltd. (石河子市明照股權投
資管理有限公司)
2,813,580
2,813,580
0.74%
0.74%
16 June 2027
Qufu Tianbo Investment Co., Ltd. (曲阜天博投
資有限公司)
2,577,780
2,577,780
0.68%
0.68%
16 June 2027
Hainan Shuangyi Hengrun Investment 
Partnership (Limited Partnership) (海南雙一
衡潤投資合夥企業(有限合夥))
2,421,600
2,421,600
0.64%
0.64%
16 June 2027
Ningbo Meishan Bonded Port Area Thriving 
Venture Capital Partnership (Limited 
Partnership) (寧波梅山保稅港區超興創業投
資合夥企業(有限合夥)
829,380
829,380
0.22%
0.22%
16 June 2027
Shanghai Changshun Jianye Consulting 
Management Co., Ltd. (上海長舜建業諮詢管
理有限公司)
486,840
486,840
0.13%
0.13%
16 June 2027
Ms. Xu Jianming (徐建明)
122,880
122,880
0.03%
0.03%
16 June 2027
Suzhou Junwang Chuangxin No. 2 Investment 
Partnership (Limited Partnership) (蘇州鋆望
創芯貳號投資合夥企業(有限合夥))
88,680
88,680
0.02%
0.02%
16 June 2027
Subtotal
220,616,500
220,616,500
58.20%
58.20%
Notes:
1. 
The relevant number of shares and percentage are calculated without taking into account of any Shares that 
may be issued upon exercise of the Over-allotment Option or the options under the 2026 Pre-IPO Share Option 
Scheme.
2. 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. 
According to the PRC Company Law, all existing Shareholders are subject to a lock-up period of 12 months 
following the Listing Date.

<<<PAGE 16>>>
16
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering**
Allotment 
as % of 
total Offer 
Shares**
Number of 
Shares held 
upon Listing
% of total 
issued share 
capital upon
Listing**
Top 1
23,980,000
49.89%
44.90%
23,980,000
6.33%
Top 5
34,626,600
72.04%
64.84%
34,626,600
9.14%
Top 10
42,197,200
87.79%
79.01%
42,197,200
11.13%
Top 25
50,202,800
104.45%
94.00%
55,027,700
14.52%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
** 
Before any exercise of the Over-allotment Option or the options under the 2026 Pre-IPO Share Option Scheme.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of
International 
Offering**
Allotment 
as % of total 
Offer Shares**
Number of 
H Shares held 
upon Listing
% of total 
issued H Shares 
capital upon 
Listing**
Number of 
Shares held 
upon Listing
Top 1
0
0.00%
0.00%
105,018,320
27.71%
105,018,320
Top 5
23,980,000
49.89%
44.90%
189,210,240
49.92%
189,210,240
Top 10
23,980,000
49.89%
44.90%
253,855,420
66.97%
253,855,420
Top 25
29,268,000
60.89%
54.80%
336,616,680
88.81%
336,616,680
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
** 
Before any exercise of the Over-allotment Option or the options under the 2026 Pre-IPO Share Option Scheme.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of
International 
Offering**
Allotment 
as % of total 
Offer Shares**
Number of 
H Shares held 
upon Listing
Number of 
Shares held 
upon Listing
% of total 
issued share 
capital upon
Listing**
Top 1
0
0.00%
0.00%
105,018,320
105,018,320
27.71%
Top 5
23,980,000
49.89%
44.90%
189,210,240
189,210,240
49.92%
Top 10
23,980,000
49.89%
44.90%
253,855,420
253,855,420
66.97%
Top 25
29,268,000
60.89%
54.80%
336,616,680
336,616,680
88.81%
Note
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.
** 
Before any exercise of the Over-allotment Option or the options under the 2026 Pre-IPO Share Option Scheme.

<<<PAGE 17>>>
17
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
Number of 
H Shares 
applied for
Number 
of valid 
applications
Pool A
Approximate 
percentage 
allotted of the 
total number 
of H Shares 
applied for
Basis of allocation/ballot
200
37,986
760 out of 37,986 applicants to receive 200 H Shares
2.00%
400
26,025
542 out of 26,025 applicants to receive 200 H Shares
1.04%
600
8,065
195 out of 8,065 applicants to receive 200 H Shares
0.81%
800
4,363
118 out of 4,363 applicants to receive 200 H Shares
0.68%
1,000
6,328
185 out of 6,328 applicants to receive 200 H Shares
0.58%
1,200
3,405
107 out of 3,405 applicants to receive 200 H Shares
0.52%
1,400
2,501
83 out of 2,501 applicants to receive 200 H Shares
0.47%
1,600
2,875
100 out of 2,875 applicants to receive 200 H Shares
0.43%
1,800
2,429
89 out of 2,429 applicants to receive 200 H Shares
0.41%
2,000
15,449
584 out of 15,449 applicants to receive 200 H Shares
0.38%
3,000
6,207
273 out of 6,207 applicants to receive 200 H Shares
0.29%
4,000
4,475
219 out of 4,475 applicants to receive 200 H Shares
0.24%
5,000
8,237
437 out of 8,237 applicants to receive 200 H Shares
0.21%
6,000
3,172
180 out of 3,172 applicants to receive 200 H Shares
0.19%
7,000
2,100
127 out of 2,100 applicants to receive 200 H Shares
0.17%
8,000
2,840
180 out of 2,840 applicants to receive 200 H Shares
0.16%
9,000
4,749
314 out of 4,749 applicants to receive 200 H Shares
0.15%
10,000
11,485
788 out of 11,485 applicants to receive 200 H Shares
0.14%
20,000
7,515
667 out of 7,515 applicants to receive 200 H Shares
0.09%
30,000
5,271
544 out of 5,271 applicants to receive 200 H Shares
0.07%
40,000
3,976
456 out of 3,976 applicants to receive 200 H Shares
0.06%
50,000
4,299
536 out of 4,299 applicants to receive 200 H Shares
0.05%
60,000
3,037
405 out of 3,037 applicants to receive 200 H Shares
0.04%
70,000
2,160
305 out of 2,160 applicants to receive 200 H Shares
0.04%
80,000
2,249
334 out of 2,249 applicants to receive 200 H Shares
0.04%
90,000
1,686
261 out of 1,686 applicants to receive 200 H Shares
0.03%
100,000
12,727
2,049 out of 12,727 applicants to receive 200 H Shares
0.03%
200,000
12,076
2,514 out of 12,076 applicants to receive 200 H Shares
0.02%
Total
207,687
Total number of Pool A successful applicants: 13,352

<<<PAGE 18>>>
18
Number of 
H Shares 
applied for
Number 
of valid 
applications
Pool B
Approximate 
percentage 
allotted of the 
total number 
of H Shares 
applied for
Basis of allocation/ballot
300,000
10,810
3,243 out of 10,810 applicants to receive 200 H Shares
0.02%
400,000
4,077
1,418 out of 4,077 applicants to receive 200 H Shares
0.02%
500,000
2,730
1,065 out of 2,730 applicants to receive 200 H Shares
0.02%
600,000
2,051
878 out of 2,051 applicants to receive 200 H Shares
0.01%
700,000
1,282
594 out of 1,282 applicants to receive 200 H Shares
0.01%
800,000
1,265
628 out of 1,265 applicants to receive 200 H Shares
0.01%
900,000
820
433 out of 820 applicants to receive 200 H Shares
0.01%
1,000,000
2,996
1,667 out of 2,996 applicants to receive 200 H Shares
0.01%
1,500,000
1,447
992 out of 1,447 applicants to receive 200 H Shares
0.01%
2,000,000
889
706 out of 889 applicants to receive 200 H Shares
0.01%
2,670,400
1,876
1,728 out of 1,876 applicants to receive 200 H Shares
0.01%
Total
30,243
Total number of Pool B successful applicants: 13,352
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
Placing to a close associate of an existing shareholder as cornerstone investor with a waiver 
under Rule 10.04 and consent under paragraph 1C(2) of the Placing Guidelines
The Company has applied for a waiver under Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules, to permit a close associate of an existing 
shareholder to participate as cornerstone investor in the Global Offering to subscribe for the Offer 
Shares to be issued by the Company under the International Offering. The Stock Exchange has 
agreed to grant the requested waiver and consent subject to the conditions that:
(i) 
Baolong Automotive has been a shareholder of the Company for more than five years. 
Longwei HK, being the wholly owned subsidiary of Baolong Automotive, is familiar with the 
Company’s business operations and development. Longwei HK’s proposed participation in 
the Global Offering reflects Baolong Automotive’s continued interest in the Company’s long-
term development;

<<<PAGE 19>>>
19
(ii) the Offer Shares to be subscribed by and allotted to Longwei HK under the Global Offering 
will be allotted at the Offer Price;
(iii) the Company and the Overall Coordinators have confirmed in writing that no preferential 
treatment has been, nor will be, given to Baolong Automotive or Longwei HK by virtue of 
their relationship with the Company in any allocation in the placing tranche of the Global 
Offering other than the preferential treatment of assured entitlement under a cornerstone 
investment following the principles set out in Chapter 4.15 of the Guide;
(iv) the Company has confirmed that the Longwei HK’s cornerstone investment agreement does 
not contain any material terms which are more favourable to Baolong Automative or Longwei 
HK than those in other cornerstone investment agreements;
(v) 
the Joint Sponsors have confirmed that to the best of their knowledge and belief, they have 
no reason to believe that Baolong Automotive or Longwei HK received any preferential 
treatment in any allocation in the placing tranche of the Global Offering as a cornerstone 
investor by virtue of their relationship with the Company other than the preferential treatment 
of assured entitlement under a cornerstone investment following the principles set out in 
Chapter 4.15 of the Guide, and details of the allocation will be disclosed in the Company’s 
allotment results announcement; and
(vi) the Joint Sponsors have further confirmed that based on their (a) discussions with the 
Company; (b) review of the Company’s latest shareholding chart; (c) review of the relevant 
corporate documents and agreements,
(a) 
Baolong Automotive (1) has less than 5% voting rights in the Company immediately 
before the Global Offering; (2) is not, and, together with Longwei HK, will not be, 
a core connected person of the Company or its close associate immediately prior to 
or following the Global Offering; and (3) does not have the power to appoint the 
Company’s directors or any other special rights upon the Listing; and
(b) 
the allocation to Longwei HK will not affect the Company’s ability to satisfy the public 
float requirement under Rule 19A.13A(1) of the Listing Rules.
Please refer to the section headed “Waivers and Exemptions – Subscriptions of offer shares by a 
close associate of an existing shareholder as cornerstone investor” in the Prospectus for further 
details of the waiver and consent.

<<<PAGE 20>>>
20
Placing to connected clients with consents under paragraph 1C(1) of the Placing Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of certain 
distributors pursuant to the Placing Guidelines. Details of the placement to connected clients are 
set out below:
No.
Connected 
Clients
Connected 
Distributor
Relationship 
between the 
Connected Client 
and the Connected 
Distributor
Whether the 
Connected Client 
will hold the 
beneficial interests 
of the Offer 
Shares on a non-
discretionary basis 
or discretionary 
basis for 
independent 
third parties
Number of 
H Shares to 
be allocated
Approximate 
percentage of 
Offer Shares in 
the Global 
Offering(7)
Approximate 
percentage of 
the total issued 
share capital 
immediately 
following 
completion of the 
Global 
Offering(7)
1
SSIF Asset 
Management 
SPC-SSI & 
Affluence Capital 
IPO Strategy 
Opportunity 
Segregated 
Portfolio (1)
Shanxi Securities 
International 
Limited (“SSI”)
SSI is a syndicate member 
who places securities of the 
Company in relation to the 
Global Offering; SSI and 
Shanxi Securities International 
Asset Management Limited 
(“SSIAM”) are both ultimately 
controlled by Shanxi Securities 
International Financial 
Holdings (“SSIFH”). The 
subscribing investor is SSIF 
Asset Management SPC-
SSI & Affluence Capital IPO 
Strategy Opportunity Segregated 
Portfolio, a segregated portfolio 
managed by SSIF ASSET 
MANAGEMENT SPC which 
is controlled by SSIAM. 
Accordingly, this segregated 
portfolio fund is considered 
as a “connected client” of SSI 
pursuant to paragraph 1B of 
the Appendix F1 to the Listing 
Rules.
Discretionary basis
54,400
0.10%
0.01%

<<<PAGE 21>>>
21
No.
Connected 
Clients
Connected 
Distributor
Relationship 
between the 
Connected Client 
and the Connected 
Distributor
Whether the 
Connected Client 
will hold the 
beneficial interests 
of the Offer 
Shares on a non-
discretionary basis 
or discretionary 
basis for 
independent 
third parties
Number of 
H Shares to 
be allocated
Approximate 
percentage of 
Offer Shares in 
the Global 
Offering(7)
Approximate 
percentage of 
the total issued 
share capital 
immediately 
following 
completion of the 
Global 
Offering(7)
2
CITIC Securities 
International 
Capital 
Management 
Limited 
(“CSICM”) (2)
CITIC Securities 
Brokerage (HK) 
Limited (“CITIC 
Brokerage”)
CSICM is a member of the same 
group of companies as CITIC 
Brokerage. Accordingly, CSICM 
is considered as a “connected 
client” of CITIC Brokerage 
pursuant to paragraph 1B of 
the Appendix F1 to the Listing 
Rules.
Non – discretionary 
basis
400,000
0.75%
0.11%
3
Guotai Junan 
Investments 
(Hong Kong) 
Limited 
(“GTJAI”) (3)
Guotai Junan 
Securities (Hong 
Kong) Limited 
(“GTJAS”)
GTJA Investment is a member 
of the same group of GTJAS. 
Accordingly, GTJAI is 
considered as a “connected 
client” of GTJAS pursuant to 
paragraph 1B of the Appendix 
F1 to the Listing Rules.
Non – discretionary 
basis
544,600
1.02%
0.14%
4
E Fund 
Management 
(Hong Kong) Co, 
Ltd. (“E Fund 
HK”) (4)
GF Securities 
(Hong Kong) 
Brokerage 
Limited 
(“GFSHK”)
E Fund HK is a member of 
the same group of companies 
as GFSHK. Accordingly, E 
Fund HK is considered as a 
“connected client” of GFSHK 
pursuant to paragraph 1B of 
the Appendix F1 to the Listing 
Rules.
Discretionary basis
3,400
0.01%
0.00%
5
China Asset 
Management 
(Hong Kong) 
Limited (“China 
AM HK”) (5)
CITIC Securities 
Brokerage (HK) 
Limited (“CITIC 
Brokerage”)
China AM HK is a member 
of the same group of CITIC 
Brokerage. Accordingly, China 
AM HK is considered as a 
“connected client” of CITIC 
Brokerage pursuant to paragraph 
1B of the Appendix F1 to the 
Listing Rules.
Discretionary basis
3,400
0.01%
0.00%
6
Huatai Capital 
Investment 
Limited  
(“HTCI”) (6)
Huatai Financial 
Holdings (Hong 
Kong) Limited 
(“HTFH”)
HTCI is a member of the same 
group of companies as HTFH. 
Accordingly, HTCI is considered 
as a “connected client” of HTFH 
pursuant to paragraph 1B of 
the Appendix F1 to the Listing 
Rules.
Non – discretionary 
basis
871,400
1.63%
0.23%

<<<PAGE 22>>>
22
Note: 
(1) SSIF Asset Management SPC-SSI & Affluence Capital IPO Strategy Opportunity Segregated Portfolio
It is proposed that SSIF Asset Management SPC-SSI & Affluence Capital IPO Strategy Opportunity Segregated 
Portfolio (the segregated portfolio established under SSIF ASSET MANAGEMENT SPC) participates as placee to 
subscribe for the Offer Shares under the International Offering (the “Fund Subscription”).
In relation to the Fund Subscription, SSIF Asset Management SPC-SSI & Affluence Capital IPO Strategy Opportunity 
Segregated Portfolio will hold the Offer Shares on a discretionary basis, with Shanxi Securities International Asset 
Management Limited (“SSIAM”) acting as its discretionary fund manager on behalf of numerous independent third-
party investors of the portfolio.
This segregated portfolio is a registered collective mutual fund; there is no single ultimate beneficial owner holding 
30% or more interest in the portfolio, and no natural person exercises sole control over the fund.
SSIF Asset Management SPC-SSI & Affluence Capital IPO Strategy Opportunity Segregated Portfolio has confirmed 
that, to the best of its knowledge, all underlying investors of the segregated portfolio fund are independent third parties 
of (a) the Company, the connected persons or the associates thereof; and (b) SSIF Asset Management SPC-SSI & 
Affluence Capital IPO Strategy Opportunity Segregated Portfolio, SSIAM, SSI, SSIFH and the companies which are 
members of the same group of companies as SSIFH.
(2) 
CSICM
CSICM will act as the single counterparty of a back-to-back total return swap transaction (the “CSICM Back-to-
back TRS”) to be entered into by CSICM in connection with a total return swap order (the “CSICM Client TRS”) 
placed by its ultimate client (the “CSICM Ultimate Client”), by which CSICM will pass the full economic exposure 
of the Offer Shares placed to CSICM to the CSICM Ultimate Client. CSICM will hold the beneficial interest of the 
Offer Shares on behalf of the CSICM Ultimate Client on a non-discretionary basis. The CSICM Ultimate Client may 
exercise an early termination right to early terminate the CSICM Client TRS at any time from the trade date of the 
CSICM Client TRS which should be on or after the date on which the Offer Shares are listed on the Stock Exchange. 
Upon the final maturity or termination of the CSICM Client TRS by the CSICM Ultimate Client, CSICM will dispose 
of the Offer Shares on the secondary market and the CSICM Ultimate Client will receive a final termination amount 
of the CSICM Back-to-back TRS which should have taken into account all the economic returns or economic loss in 
relation to the Offer Shares and the fixed amount of transaction fees of the CSICM Back-to-back TRS and the CSICM 
Client TRS. CSICM will not exercise the voting right of the Offer Shares during the terms of the CSICM Back-to-back 
TRS.
The CSICM Ultimate Client is Beevest Capital Management Limited – Global Multi Alpha Fund SP. The general 
partner of the CSICM Ultimate Client is Beevest Capital Management Limited which is in turn held as to more than 
30% by Zeng Shuzhen (曾淑珍). The limited partner holding 30% or more interest in the CSICM Ultimate Client is 
Zeng Shuzhen (曾淑珍).
CSICM has confirmed that, to the best of their knowledge, (i) each of the CSICM Ultimate Client and the ultimate 
beneficial owners holding 30% or more interest of the CSICM Ultimate Client listed above is an independent third 
party of (a) the Company, its subsidiaries, the connected persons or the associates thereof; and (b) CSICM, CITIC 
Brokerage and the companies which are members of the same group of companies as CITIC Brokerage.
(3) 
GTJAI
It is proposed that Guotai Junan Investments (Hong Kong) Limited (“GTJAI”) participates as placee to subscribe for 
the Offer Shares under the International Offering (the “GTJAI Subscription”). GTJAI is a member of the same group 
of companies as Guotai Junan Securities (Hong Kong) Limited (“GTJAS”) and is considered as a connected client of 
GTJAS pursuant to paragraph 1B(7) of the Placing Guidelines.

<<<PAGE 23>>>
23
In relation to the GTJAI Subscription, GTJAI shall hold the Offer Shares for hedging purpose as the single underlying 
asset of a set of back-to-back total return swap transaction (the “GTHT Back-to-back TRS”) to be entered into 
between GTJAI and Guotai Haitong Securities Co., Ltd. (the “GTHT Onshore Parent”) in connection with a total 
return swap order (the “GTHT Client TRS”) to be entered into by GTHT Onshore Parent and the ultimate client 
(the “GTHT Onshore Ultimate Client”), respectively. Such GTHT Client TRS is to be fully funded by the GTHT 
Onshore Ultimate Client. GTJAI will hold the Offer Shares on a non-discretionary basis for the purpose of hedging 
the economic exposure under the GTHT Back-to-back TRS and GTHT Client TRS only, During the tenor of the 
GTHT Client TRS, all economic returns of the Offer Shares will be passed to the GTHT Onshore Ultimate Client and 
all economic losses shall be borne by the GTHT Onshore Ultimate Client, subject to the terms and conditions of the 
GTHT Back-to-back TRS and GTHT Client TRS, and GTJAI will not take part in any economic return or bear any 
economic loss in relation to the price of the Offer Shares. The GTHT Onshore Ultimate Client may request to redeem 
the Offer Shares at their own discretion, upon which GTJAI shall dispose of the Offer Shares and settle the GTHT 
Back-to-back TRS and GTHT Client TRS in cash in accordance with the terms and conditions of the GTHT Back-
to-back TRS and GTHT Client TRS documents. Due to its internal policy, GTJAI will not exercise the voting right 
attaching to the Offer Shares during the tenor of the GTHT Back-to-back TRS and GTHT Client TRS.
To the best knowledge, information and belief of GTJA Investments after due enquiry, the GTHT Onshore Ultimate 
Clients and their respective ultimate beneficial owners holding 30% or more interest include:
GTHT Onshore 
Ultimate Clients
Ultimate Beneficial 
Owners (“UBO”)
Remarks
北京止於至善投資管理有限公司－
止於至善私募基金
Beijing Zhiyuzhishan Investment 
Management Co,Ltd-Zhiyuzhishan 
Private Fund
李豐 LI FENG (National ID: 
420102196104121450)
UBO with over 30% interest
To the best knowledge of GTJAI and after making all reasonable enquiries, (i) GTJA Investments has confirmed 
that, to the best of their knowledge, each of the GTJA Onshore Ultimate Clients and the ultimate beneficial owners 
holding 30% or more interest of the GTJA Onshore Ultimate Clients listed above is an independent third party of 
GTJA Investments, GTJAS and the companies which are members of the same group of companies as GTJAS., and 
(ii) GTJAI is not a collective investment scheme which is not authorised by the SFC nor is expected to hold the Offer 
Shares on behalf of such scheme.
(4) 
E Fund HK
E Fund HK will hold the Offer Shares for and on behalf of their underlying clients (the “E Fund HK Ultimate 
Clients”) on a discretionary basis. To the best knowledge of E Fund HK and after making all reasonable enquiries, 
each of the E Fund HK Ultimate Clients is independent from the Company, its subsidiaries, its substantial shareholders, 
GFSHK, E Fund HK and the companies which are members of the same group of companies as GFSHK. There is no 
single ultimate beneficial owner holding 30% or more interest in the portfolio, and no natural person exercises sole 
control over the fund.
(5) 
China Asset Management (Hong Kong) Limited
China AMC HK will hold the Offer Shares in its capacity as the discretionary fund manager managing on behalf of 
its underlying clients (the “China AMC HK Underlying Clients”), each of which is an independent third party of 
the Company. To the best of knowledge of China AMC HK and after making all reasonable enquiries, (i) each of 
the China AMC HK Underlying Clients is an independent third party of the Company, its subsidiaries, its substantial 
shareholders, China AMC HK, CLSA and the companies which are members of the same group of companies as 
CLSA, and (ii) none of CLSA and any companies which are members of the same group of companies as CLSA hold 
any beneficial interest in any of the China AMC HK Underlying Clients.

<<<PAGE 24>>>
24
The details of the China AMC HK Underlying Client(s) are as follow:
1. 
CHINAAMC SELECT GREATER CHINA TECHNOLOGY FUND – 213800N2TIGVZMBIDU43 – To our best 
knowledge, no others investor holds 30% or more interests in the portfolio, and no natural person exercises sole 
control over the fund
2. 
CHINAAMC FUND – CHINAAMC CHINA OPPORTUNITIES FUND – 213800LFHQWQ1J2I7875 – Confirm 
no others investor hold 30% or more interest in the same fund
3. 
CHINAAMC CHINA FOCUS FUND – 254900G5YFZ5OTQS0G14 – UBO – 72.04% – Manulife (International) 
Limited – 549300E1S6OED3RZ2B22
4. 
CHINAAMC CHINA GROWTH FUND (SICAV) – 213800OL1K8299ZA3F59 – UBO 72.71% – Yuanta 
Securities (HK) Company LTD – 3003006CJLCA4YV6DX47
5. 
ICBC (ASIA) LTD-CHINAAMC-BSCOMC LTD – 100% hold by BSCOMC Limited
(6) 
Huatai Capital Investment Limited
Huatai Financial Holdings (Hong Kong) Limited (“HTFH”) is a non-syndicate sub-broker in connection with the 
Global Offering. PRC investors are currently not permitted under applicable PRC laws to participate directly in initial 
public offerings (“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products issued by 
appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. In connection 
with such products, the licensed domestic securities firms, through their Hong Kong affiliates, may participate in Hong 
Kong IPOs either as placees or cornerstone investors (the “Cross-border Derivatives Trading Regime”).
Huatai Securities Co., Ltd. (“Huatai Securities”), the shares of which are listed on both the Shanghai Stock Exchange 
(stock code: 601688) and the Stock Exchange (stock code: 6886), is one of the domestic securities firms licensed to 
undertake cross-border derivatives trading activities. Huatai Securities entered into an ISDA agreement (the “ISDA 
Agreement”) with its indirectly wholly-owned subsidiary, HTCI, to set out the principal terms of any future total 
return swap between Huatai Securities and HTCI.
Pursuant to the ISDA Agreement, HTCI, which intends to participate in the Global Offering as a placee, will hold 
the beneficial interest of the Offer Shares on a non-discretionary basis as the single underlying holder under a 
back-to-back total return swap (the “Back-to-back TRS”) to be entered by HTCI in connection with a Client TRS (as 
defined below) placed by and fully funded (i.e. with no financing provided by HTCI) by the Huatai Ultimate Client 
(as defined below), by which, HTCI will, subject to customary fees and commissions, pass the full economic exposure 
of the Offer Shares ultimately to the Huatai Ultimate Client, which in effect, HTCI will hold the beneficial interest of 
the Offer Shares on behalf of the Huatai Ultimate Client. HTFH and HTCI are indirectly wholly-owned subsidiaries of 
Huatai Securities. Accordingly, HTCI is considered as a “connected client” of HTFH pursuant to paragraph 13(7) of 
the Placing Guidelines.
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investor (the “Huatai Ultimate Client”) cannot 
directly subscribe for the Offer Shares but may invest in derivative products issued by domestic securities firms 
licenced to undertake cross-border derivatives trading activities, such as Huatai Securities, with the Offer Shares as the 
underlying assets.

<<<PAGE 25>>>
25
Instead of directly subscribing for the Offer Shares, the Huatai Ultimate Client, through its investment manager, will 
place a total return swap order (the “Client TRS”) with Huatai Securities in connection with the Company’s IPO 
and Huatai Securities will place a Back-to-back TRS order to HTCI on the terms of the ISDA Agreement. In order to 
hedge its exposure under the Back-to-back TRS, HTCI participates in the Company’s IPO and subscribes the Offer 
Shares through placing order with HTFH during the International Offering. The Huatai Ultimate Client for purpose of 
this place subscription include the investment funds, details of which is set out below:
Name of Huatai Ultimate Client
Ultimate Beneficial 
Owners (“UBO”)
Remarks
北京止於至善投資管理有限公司－
止於至善私募基金
Beijing Zhiyuzhishan Investment 
Management Co,Ltd-Zhiyuzhishan 
Private Fund
李豐 LI FENG (National ID: 
420102196104121450)
UBO with over 30% interest
To the best of our knowledge and after making all reasonable enquiries, the Huatai Ultimate Client is an independent 
third party of (i) the Company, the connected person or the associates thereof, and (ii) HTCI, HTFH and the companies 
which are members of the same group of HTCI.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in connection with the 
Client TRS order placed by the Huatai Ultimate Client. Pursuant to the terms of the contracts of the Back-to-back 
TRS and the Client TRS, during the tenor of the Back-to-back TRS and the Client TRS, subject to customary fees and 
commissions, all economic returns of the Offer Shares will be ultimately passed to the Huatai Ultimate Client through 
the Back-to-back TRS and the Client TRS and all economic loss shall be ultimately borne by the Huatai Ultimate 
Client. HTCI will not take any economic return or bear any economic loss in relation to the Offer Shares.
Investment in the Back-to-back TRS and the Client TRS is similar to the investment in a qualified domestic 
institutional investor fund (“QDII”) in the way that the Huatai Ultimate Client would reap all the economic benefits 
of the underlying Offer Shares, except that a QDII fund would pass through the exchange rate exposure on both 
the notional value of the investment and the profit and loss of the investment. In contrast, the profit and loss of the 
Back-to-back TRS and the Client TRS factor into account the fluctuation in RMB exchange rate upon termination of 
the Client TRS by converting the profit and loss using the current exchange rate at the time of termination. As such, 
the Huatai Ultimate Client would bear the exchange rate exposure of the profit and loss on settlement date.
The Huatai Ultimate Client may exercise an early termination right to terminate the Client TRS at any time from the 
issue date of the Client TRS which should be on or after the date on which the Offer Shares are listed on the Stock 
Exchange at its own discretion. Upon the termination upon maturity or early termination of the Client TRS by the 
Huatai Ultimate Client, HTCI will dispose the Offer Shares on the secondary market and the Huatai Ultimate Client 
will receive a final settlement amount in cash in accordance with the terms and conditions of the Back-to-back TRS 
and the Client TRS which should have taken into account all the economic returns or economic loss in relation to 
the Offer Shares. If upon the maturity of the Client TRS, the Huatai Ultimate Client intend to extend the investment 
period, subject to further agreement between Huatai Securities and the relevant Huatai Ultimate Client, the term of 
the Client TRS could be extended by way of a new issuance or a tenor extension. Accordingly, Huatai Securities will 
extend the term of the Back-to-back TRS by way of a new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through 
the economic exposure to the Huatai Ultimate Client, each being an onshore client who places a Client TRS order with 
Huatai Securities in connection with the IPO of the Company. HTCI will not exercise the voting right of the Offer 
Shares during the tenor of the Back-to-back TRS.
During the life of the Client TRS and Back-to-back TRS, HTCI may continue to hold the Offer Shares in its custodian 
account, or to hold some or all of the Offer Shares in a prime brokerage account for stock borrowing purposes, where 
HTCI will lend out its holding of underlying Offer Shares in the form of stock borrowing loans consistent with market 
practice to lower its finance costs, provided that HTCI has the ability to call back the Offer Shares on loan at any time 
in order to satisfy its obligations under the Back-to-back TRS to ensure the economic interests are ultimately passed to 
the Huatai Ultimate Client.
(7) 
Before any exercise of the Over-allotment Option or the options under the 2026 Pre-IPO Share Option Scheme.

<<<PAGE 26>>>
26
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for 
or purchased by them is the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and trading fee payable.
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or 
any part of the contents of this announcement.
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
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated 9 June 2026 issued by SENASIC Electronics 
Technology Co., Ltd. (琻捷電子科技(江蘇)股份有限公司) for detailed information about 
the Global Offering described below before deciding whether or not to invest in the H Shares 
thereby being offered.
* 
Potential investors of the Offer Shares should note that the Joint Sponsors and Joint Sponsor-OCs (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations 
under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the 
events set out in the section headed “Underwriting — Underwriting Arrangements and Expenses — Hong 
Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong 
Kong time) on the Listing Date (which is currently expected to be on Wednesday, 17 June 2026).

<<<PAGE 27>>>
27
PUBLIC FLOAT AND FREE FLOAT
Immediately upon completion of the Global Offering and the Conversion of Unlisted Shares into 
H Shares, taking into account 53,407,000 H Shares to be offered pursuant to the Global Offering 
(without taking into account any Shares that may be issued upon exercise of the Over-allotment 
Option and under the 2026 Pre-IPO Share Option Scheme), an aggregate of 267,635,180 H Shares 
will count towards the public float of the Company under Rule 19A.13A(1) of the Listing Rules, 
representing 70.61% of the total issued Shares.
Based on (i) the Offer Price of HK$18.36, and (ii) 379,041,820 total H Shares which are expected 
to be in issue immediately upon completion of the Global Offering and the Conversion of Unlisted 
Shares into H Shares (without taking into account any Shares that may be issued upon exercise of 
the Over-allotment Option and under the 2026 Pre-IPO Share Option Scheme), it is expected that 
the market value of the H Shares at the time of Listing will be HK$6.96 billion. Accordingly, in 
the event that the expected market value of the Company is over HK$6.0 billion but not exceeding 
HK$30.0 billion, the higher of (a) the percentage that would result in the expected market value 
of H shares held by the public to be HK$1.5 billion at the time of listing; and (b) 15% of the total 
number of issued Shares must be held by the public at the time of Listing. Based on a public float 
of 70.61%, the Company will be able to meet the minimum public float requirements under Rule 
19A.13A(1) of the Listing Rules.
Rule 19A.13C(1) of the Listing Rules provides that, where a new applicant is a PRC issuer with 
no other listed shares at the time of listing, this will normally mean that the portion of H shares 
for which listing is sought that are held by the public and not subject to any disposal restrictions 
(whether under contract, the Listing Rules, applicable laws or otherwise), at the time of listing, 
must: (a) represent at least 10% of the total number of issued shares in the class to which H shares 
belong at the time of listing (excluding treasury shares), with an expected market value at the 
time of listing of not less than HK$50 million; or (b) have an expected market value at the time 
of listing of not less than HK$600 million. Shares held by all the existing shareholders of the 
Company (i.e. 325,634,820 Shares) are subject to a lock-up period of 12 months following the 
Listing Date pursuant to the applicable PRC laws and H Shares to be issued to the Cornerstone 
Investors pursuant to the cornerstone investments set forth in “Cornerstone Investors” of this 
prospectus (i.e. 15,413,600 H Shares) are subject to a lock-up period of six months following 
the Listing Date. The Offer Shares to be subscribed by all the other investors participating in the 
Global Offering are not subject to any disposal restriction. Based on the Offer Price of HK$18.36 
per H Share, the Company confirms that it complies with the free float requirement under Rule 
19A.13C(1) of the Listing Rules, with sufficient H Shares held by the public and available for 
trading.
The Directors confirm that, immediately following completion of the Global Offering: (i) no placee 
will, individually, be placed more than 10% of the enlarged issued share capital of the Company 
immediately after the Global Offering; (ii) there will not be any new substantial Shareholder under 
the Listing Rules immediately after the Global Offering; (iii) the three largest public shareholders 
of the Company do not hold more than 50% of the H shares in public hands at the time of the 
Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at 
least 300 Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing 
Rules.

<<<PAGE 28>>>
28
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, 17 
June 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting” in the Prospectus has not been 
exercised. Investors who trade the H Shares on the basis of publicly available allocation details 
prior to the receipt of H Share certificates or prior to the H Share certificates becoming valid 
evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. in Hong Kong on 
Wednesday, 17 June 2026, it is expected that dealings in the H Shares on the Stock Exchange will 
commence at 9:00 a.m. on Wednesday, 17 June 2026. The H Shares will be traded in board lots of 
200 H Shares each and the stock code of the H Shares will be 6675.
By order of the Board
SENASIC Electronics Technology Co., Ltd.
Li Mengxiong
Chairman of the Board, Executive Director and Chief Executive Officer
Hong Kong, 16 June 2026
As at the date of this announcement, the Board comprises: (i) Mr. Li Mengxiong, Mr. Zhu 
Shouteng, Mr. Li Shuguang and Ms. Xu Hongru as executive directors; (ii) Mr. Ju Hua and Mr. 
Sha Chongjiu as non-executive directors; and (iii) Mr. Chu Xiaowen, Mr. Jie Donghui and Ms. 
Cheung Suet Fong as independent non-executive directors.
