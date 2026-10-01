# 配发结果公告抽取任务：6802.HK Shenzhen Camsense Technologies Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**29/09/2026 21:31**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0929/2026092901927.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6802.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock 
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the 
contents of this announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the 
contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings 
as those defined in the prospectus dated September 22, 2026 (the “Prospectus”) of Shenzhen Camsense 
Technologies Co., Ltd. (深圳市歡創科技股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for any securities. This announcement is not a prospectus. Potential investors should read 
the Prospectus for detailed information about the Global Offering before deciding whether or not to invest in the 
Offer Shares. Any investment decision in relation to the Offer Shares should be taken solely in reliance on the 
information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not, and is not intended to, constitute or form a part of any offer or solicitation to purchase 
or subscribe for securities in the United States or in any other jurisdictions. The Offer Shares have not been, and 
will not be, registered under the United States Securities Act of 1933, as amended from time to time (the “U.S. 
Securities Act”), or securities law of any state or other jurisdiction of the United States. The Offer Shares may 
not be offered, sold, pledged or otherwise transferred within the United States or to, or for the account or benefit 
of U.S. persons (as defined in Regulation S under the U.S. Securities Act), except pursuant to an available 
exemption from, or in a transaction not subject to, the registration requirements of the U.S. Securities Act. There 
will be no public offer of the Offer Shares in the United States. The Offer Shares are being offered and sold 
solely outside the United States in offshore transactions in reliance on Regulation S under the U.S. Securities 
Act.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited, 
as stabilizing manager (the “Stabilizing Manager”) (or any person acting for it), on behalf of the Underwriters, 
may over-allocate or effect transactions with a view to stabilizing or supporting the market price of the H Shares 
at a level higher than that which might otherwise prevail for a limited period after the Listing Date. However, 
there is no obligation on the Stabilizing Manager (or any person acting for it) to conduct any such stabilizing 
action. Such stabilizing action, if taken, (a) will be conducted at the absolute discretion of the Stabilizing 
Manager (or any person acting for it) and in what the Stabilizing Manager reasonably regards as the best 
interest of the Company, (b) may be discontinued at any time and (c) is required to be brought to an end within 
30 days from the last day for lodging applications under the Hong Kong Public Offering. Such stabilizing action, 
if taken, may be effected in all jurisdictions where it is permissible to do so, in each case in compliance with 
all applicable laws, rules and regulatory requirements, including the Securities and Futures (Price Stabilizing) 
Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance 
(Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that stabilizing action cannot be taken to support the price of the H Shares 
for longer than the stabilization period, which will begin on the Listing Date and is expected to expire on the 
30th day after the last day for lodging applications under the Hong Kong Public Offering. After this date, no 
further stabilizing action may be taken, and demand for the H Shares and the price of the H Shares could fall.
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on 
behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong Underwriting Agreement 
with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting – 
Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the day that trading in the H Shares commences 
on the Stock Exchange.

<<<PAGE 2>>>
– 2 –
Shenzhen Camsense Technologies Co., Ltd.
深圳市歡創科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the 
Global Offering
:
11,588,800 H Shares (subject to the 
Over-allotment Option)
Number of Hong Kong Offer Shares
:
1,158,900 H Shares
Number of International Offer Shares
:
10,429,900 H Shares (subject to the 
Over-allotment Option)
Offer Price
:
HK$58.85 per H Share, plus brokerage 
of 1.0%, SFC transaction levy of 
0.0027%, AFRC transaction levy of 
0.00015% and Stock Exchange trading 
fee of 0.00565% (payable in full on 
application in Hong Kong dollars and 
subject to refund)
Nominal Value
:
RMB1.00 per H Share
Stock Code
:
6802
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators, Joint Global Coordinators
and Joint Bookrunners
Overall Coordinator, Joint Global Coordinator and Joint Bookrunner
Joint Bookrunners

<<<PAGE 3>>>
– 3 –
Shenzhen Camsense Technologies Co., Ltd.
深圳市歡創科技股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have 
the same meanings as those defined in the prospectus dated September 22, 2026 (the 
“Prospectus”) issued by Shenzhen Camsense Technologies Co., Ltd. (深圳市歡創科技股份
有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, Shareholders and prospective investors should be aware that the price of 
the H Shares could move substantially even with a small number of H Shares traded and 
should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company Information
Stock code
6802
Stock short name
CAMSENSE
Dealings commencement date
September 30, 2026*
* See note at the end of this announcement.
Price Information
Offer Price
HK$58.85
Offer Shares and Share Capital
Number of Offer Shares before exercise of 
the Over-allotment Option
11,588,800 H Shares
Number of Offer Shares in the Hong Kong 
Public Offering
1,158,900 H Shares
Number of Offer Shares in the International 
Offering (before exercise of the Over-allotment Option)
10,429,900 H Shares
Number of issued Shares upon Listing before 
exercise of the Over-allotment Option
96,573,639
Over-allocation
No. of Offer Shares over-allocated
1,738,300 H Shares
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.

<<<PAGE 4>>>
– 4 –
Proceeds
Gross proceeds (Note 1)
HK$682.0 million
Less: Estimated listing expenses payable based 
on Offer Price (Note 2)
HK$(66.6) million
Net proceeds (Note 3)
HK$615.4 million
Notes:
(1) 
Gross proceeds refer to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
(2) 
This amount excludes the effect of the Special Bonus. Taking into account the Special Bonus, based on the 
Offer Price of HK$58.85, assuming no exercise of the Over-allotment Option, the total estimated listing 
expenses in relation to the Global Offering will be approximately HK$72.6 million. For details of the 
Special Bonus, please refer to the section headed “Additional Special Bonus” of this announcement.
(3) 
This amount excludes the effect of the Special Bonus. Taking into account the Special Bonus, based on the 
Offer Price of HK$58.85, assuming no exercise of the Over-allotment Option, the net proceeds in relation 
to the Global Offering will be approximately HK$609.4 million. For details of the Special Bonus, please 
refer to the section headed “Additional Special Bonus” of this announcement.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
157,315
No. of successful applications
11,589
Subscription level
3,546.91 times
Claw-back triggered
N/A
No. of Offer Shares initially available under 
the Hong Kong Public Offering
1,158,900 H Shares
No. of Offer Shares reallocated from the International 
Offering
0
Final no. of Offer Shares under the Hong Kong Public 
Offering
1,158,900 H Shares
% of Offer Shares under the Hong Kong Public 
Offering to the Global Offering
10%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can 
refer to https://www.hkeipo.hk/iporesult to perform a search by name or identification number or 
https://www.hkeipo.hk/iporesult for the full list of allottees.

<<<PAGE 5>>>
– 5 –
INTERNATIONAL OFFERING
No. of placees
130
Subscription level
5.53 times
No. of Offer Shares initially available under 
the International Offering
10,429,900 H Shares
No. of Offer Shares reallocated to the Hong Kong Public 
Offering
0
Final no. of Offer Shares under the International Offering 
(before exercise of the Over-allotment Option)
10,429,900 H Shares
% of Offer Shares under the International Offering to 
the Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for a waiver from strict 
compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) of Appendix F1 to the 
Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange to permit the Company to allocate 
certain Offer Shares in the International Offering to a close associate of an existing minority Shareholder 
(“Existing Minority Shareholder(s)”), (i) none of the Offer Shares subscribed by the placees and the public offer 
subscribers have been financed directly or indirectly by the Company, any of the Directors, chief executive of 
the Company, the Single Largest Group of Shareholders, substantial Shareholders, existing Shareholders or any 
of its subsidiaries or their respective close associates; (ii) none of the placees and the public offer subscribers 
who have subscribed for or purchased the Offer Shares are accustomed to taking instructions from the Company, 
any of the Directors, chief executive of the Company, the Single Largest Group of Shareholders, substantial 
Shareholders, existing Shareholders or any of its subsidiaries or their respective close associates in relation 
to the acquisition, disposal, voting or other disposition of H Shares registered in his/her/its name or otherwise 
held by him/her/it; (iii) there is no side agreement or arrangement between the Company, any of the Directors, 
chief executive of the Company, the Single Largest Group of Shareholders, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates, on one hand, and 
the public offer subscribers or the placees who have subscribed for or purchased the Offer Shares, on the other 
hand; (iv) there is no side agreement or arrangement between the Company, any of the Directors, chief executive 
of the Company, the Single Largest Group of Shareholders, substantial Shareholders, existing Shareholders of 
the Company or any of its subsidiaries or their respective close associates, on one hand, and any other parties, 
on the other hand, in connection with the subscription, purchase, disposal, turnover, or valuation of the Shares 
(which, for the avoidance of doubt, does not include agreements entered into with the Stabilizing Manager); and 
(v) no rebate has been, directly or indirectly, provided by the Company, any of the Directors, chief executive 
of the Company, the Single Largest Group of Shareholders, substantial Shareholders, existing Shareholders of 
the Company or any of its subsidiaries or their respective close associates, or syndicate members, or any other 
brokers involved in the Global Offering, to any investors in the Hong Kong Public Offering or placees in the 
International Offering.

<<<PAGE 6>>>
– 6 –
The placees in the International Offering include the following:
Cornerstone Investors
Cornerstone 
Investor(1)
No. of Offer 
Shares allocated
Approximate % 
of total number 
of Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
Approximate % 
of total issued H 
Shares after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Approximate % 
of total issued 
share capital in 
the Company 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing 
shareholders 
or their close 
associates
Golden Link
1,699,200
14.66%
1.76%
1.76%
No
Taiwan ZMAX
170,000
1.47%
0.18%
0.18%
No
Total
1,869,200
16.13%
1.94%
1.94%
–
Note:
(1) 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” 
in the Prospectus.

<<<PAGE 7>>>
– 7 –
Allottees with Waivers/Consents Obtained
Investors
No. of Offer 
Shares 
allocated
Approximate % 
of total number 
of Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
Approximate % 
of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Approximate % 
of total issued 
share capital in 
the Company 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the 
Placing Guidelines in relation to subscription for H Shares by Existing Minority Shareholder(s) and/or their close associate(s)(1)
Mr. Liang Jianhong 
(梁建宏)
20,400
0.18%
0.02%
0.02%
Spouse of Ms. Zheng Beibei (鄭
蓓蓓), an existing Shareholder 
holding approximately 1.30% 
of the Company’s issued share 
capital immediately before the 
Global Offering.
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations to connected clients(2)
GF Securities 
Asset Management 
(Guangdong) Co., Ltd. 
(“GF Securities AM”)
5,400
0.05%
0.01%
0.01%
GF Securities AM is a member
of the same group of companies 
as GF Securities (Hong Kong) 
Brokerage Limited (“GF 
Securities (Hong Kong) 
Brokerage”).
China International 
Capital Corporation 
Limited (“CICC”)
3,000
0.03%
0.003%
0.003%
CICC is a member of the same 
group of companies as China 
International Capital Corporation 
Hong Kong Securities Limited 
(“CICCHKS”).
Value Partners 
Hong Kong Limited 
(“VPHK”)
1,300
0.01%
0.001%
0.001%
VPHK is a member of the same 
group of companies as GF 
Securities (Hong Kong) Brokerage
Value Partners Limited 
(“VPL”)
100
0.0009%
0.0001%
0.0001%
VPL is a member of the same 
group of companies as GF 
Securities (Hong Kong) Brokerage

<<<PAGE 8>>>
– 8 –
Notes:
(1) 
The Stock Exchange has granted a waiver from strict compliance with Rule 10.04 of the Listing Rules and 
a consent under paragraph 1C(2) of the Placing Guidelines to permit the Offer Shares in the International 
Offering to be placed to a close associate of an Existing Minority Shareholder. Details of allocations to 
Existing Minority Shareholder(s) and/or their close associate(s) are disclosed in the section headed “Others/
Additional Information – Allocation of H Shares to Existing Minority Shareholder(s) and their close 
associate(s)” of this announcement, as applicable.
(2) 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients, please refer to the section 
headed “Others/Additional Information – Placing to connected clients with consent under paragraph 1C(1) 
of the Placing Guidelines” in this announcement.

<<<PAGE 9>>>
– 9 –
LOCK-UP UNDERTAKINGS
Single Largest Group of Shareholders
Name(1)
Number of Shares 
held subject to lock-
up undertakings 
upon Listing
Approximate % 
of total issued H 
Shares after the 
Global Offering 
subject to lock–up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Approximate % of 
total issued share 
capital in the 
Company after the 
Global Offering 
subject to lock–up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings(2)(3)
Wang Jian
10,641,212
11.02%
11.02%
September 29, 2027
Zhou Kun
8,763,889
9.07%
9.07%
September 29, 2027
Liu Yi
1,580,986
1.64%
1.64%
September 29, 2027
Camsense Investment
2,636,840
2.73%
2.73%
September 29, 2027
Xinle Management
1,261,649
1.31%
1.31%
September 29, 2027
Camsense Era
1,627,890
1.69%
1.69%
September 29, 2027
Subtotal
26,512,466
27.45%
27.45%
–
Notes:
(1) 
For further details of the Single Largest Group of Shareholders, please refer to the section headed 
“Relationship with Our Single Largest Group of Shareholders” in the Prospectus.
(2) 
Pursuant to Rule 10.07 of the Listing Rules, the Single Largest Group of Shareholders has undertaken to 
the Stock Exchange and the Company that, except in connection with the Global Offering (or the Over-
allotment Option), they will not, and will procure that the relevant registered holder(s) will not, without 
the prior written consent of the Stock Exchange and unless otherwise in compliance with the applicable 
requirements of the Listing Rules: in the period commencing on the date of the Prospectus and ending 
on the date which is six months from the Listing Date, either directly or indirectly, dispose of, nor enter 
into any agreement to dispose of or otherwise create any options, rights, interests or encumbrances in 
respect of, any of the securities of the Company that he/it is shown to beneficially own in the Prospectus. 
For further details, please refer to the section headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Undertakings to the Stock Exchange pursuant to the Listing 
Rules – By our Single Largest Group of Shareholders” in the Prospectus.
(3) 
According to the PRC Company Law, all existing Shareholders (including the Single Largest Group of 
Shareholders) are subject to a lock-up period of 12 months following the Listing Date.

<<<PAGE 10>>>
– 10 –
Cornerstone Investors
Name(1)
Number of Shares 
held subject to lock-
up undertakings 
upon Listing
Approximate % 
of total issued H 
Shares after the 
Global Offering 
subject to lock–up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Approximate % of 
total issued share 
capital in the 
Company after the 
Global Offering 
subject to lock–up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings(2)
Golden Link
1,699,200
1.76%
1.76%
March 29, 2027
Taiwan ZMAX
170,000
0.18%
0.18%
March 29, 2027
Total
1,869,200
1.94%
1.94%
–
Notes:
(1) 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” 
in the Prospectus.
(2) 
Each of the Cornerstone Investors has agreed to a lock-up period of six months from and including 
the Listing Date. The lock-up period is expected to end on March 29, 2027, being six months after the 
expected Listing Date.

<<<PAGE 11>>>
– 11 –
Pre-IPO Investors/Other Existing Shareholders (other than the Single Largest Group of 
Shareholders)
Name(1)
Number of Shares 
held subject to lock-
up undertakings 
upon Listing
Approximate % 
of total issued H 
Shares after the 
Global Offering 
subject to lock–up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Approximate % of 
total issued share 
capital in the 
Company after the 
Global Offering 
subject to lock–up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings(2)
Fuhai Shenwan
5,083,496
5.26%
5.26%
September 29, 2027
Nanshan Fuhai
4,964,457
5.14%
5.14%
September 29, 2027
Fuhai Jiuqian
1,505,697
1.56%
1.56%
September 29, 2027
Smart Internet
4,864,567
5.04%
5.04%
September 29, 2027
Shenzhen Qianhai
1,051,798
1.09%
1.09%
September 29, 2027
Zhongyuan Qianhai
657,374
0.68%
0.68%
September 29, 2027
Lingrui Keystone
3,853,815
3.99%
3.99%
September 29, 2027
Hangzhou Puhua Yuchen
2,764,034
2.86%
2.86%
September 29, 2027
Shanghai Puyang
1,129,250
1.17%
1.17%
September 29, 2027
Changzhou Xiyang
1,807,575
1.87%
1.87%
September 29, 2027
Dongguan Xiyang
1,041,976
1.08%
1.08%
September 29, 2027
Changzhou Xiyang Puxin
1,254,778
1.30%
1.30%
September 29, 2027
Changsha Xiyang
690,986
0.72%
0.72%
September 29, 2027
Yang Xi
138,188
0.14%
0.14%
September 29, 2027
Shanghai Xuanjian
1,254,778
1.30%
1.30%
September 29, 2027
Pingshan Kaisheng
3,840,388
3.98%
3.98%
September 29, 2027
Kaisheng No.5
829,219
0.86%
0.86%
September 29, 2027
Wuxi Yicun Juncheng
1,505,697
1.56%
1.56%
September 29, 2027
Shanghai Puruan
1,756,617
1.82%
1.82%
September 29, 2027
Jiaxing Zhongdian Aijia
752,849
0.78%
0.78%
September 29, 2027
Shanghai Baichen
690,986
0.72%
0.72%
September 29, 2027
Peng Peng
2,704,740
2.80%
2.80%
September 29, 2027
Qingdao Resonance
2,704,425
2.80%
2.80%
September 29, 2027
New Fuguo
925,602
0.96%
0.96%
September 29, 2027

<<<PAGE 12>>>
– 12 –
Name(1)
Number of Shares 
held subject to lock-
up undertakings 
upon Listing
Approximate % 
of total issued H 
Shares after the 
Global Offering 
subject to lock–up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Approximate % of 
total issued share 
capital in the 
Company after the 
Global Offering 
subject to lock–up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings(2)
Shenzhen Haojun
77,092
0.08%
0.08%
September 29, 2027
Qingdao 
Microelectronics
1,620,000
1.68%
1.68%
September 29, 2027
Guosen Capital
1,541,517
1.60%
1.60%
September 29, 2027
Zheng Beibei
1,105,596
1.14%
1.14%
September 29, 2027
Nanshan Shanghua 
Hongtu
1,081,761
1.12%
1.12%
September 29, 2027
Nanling Huiye
752,849
0.78%
0.78%
September 29, 2027
Zhicheng Shuzhi No. 10
540,903
0.56%
0.56%
September 29, 2027
Qingdao Guotou
486,000
0.50%
0.50%
September 29, 2027
Roborock Innovation
1,554,223
1.61%
1.61%
September 29, 2027
Zhongshan 
Entrepreneurship
554,040
0.57%
0.57%
September 29, 2027
Zhongshan Torch
554,040
0.57%
0.57%
September 29, 2027
Hefei High-Tech
831,060
0.86%
0.86%
September 29, 2027
Subtotal
58,472,373
60.55%
60.55%
–
Notes:
(1) 
For details of the background of each of the Pre-IPO Investors, please refer to the section headed “History, 
Development and Corporate Structure – Pre-IPO Investments” in the Prospectus.
(2) 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. 
According to the PRC Company Law, all existing Shareholders are subject to a lock-up period of 12 
months following the Listing Date.

<<<PAGE 13>>>
– 13 –
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
H Shares
allotted
Allotment
as % of 
International
Offering 
(assuming the
Over-
allotment 
Option is not
exercised)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option is fully 
exercised)
Allotment 
as % of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Allotment 
as % of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
Number of 
H Shares 
held upon
Listing
Approximate 
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
Top 1
3,398,400
32.58%
27.93%
29.32%
25.50%
3,398,400
3.52%
3.46%
Top 5
6,633,500
63.60%
54.52%
57.24%
49.77%
6,633,500
6.87%
6.75%
Top 10
8,138,700
78.03%
66.88%
70.23%
61.07%
8,138,700
8.43%
8.28%
Top 25
10,519,300
100.86%
86.45%
90.77%
78.93%
10,519,300
10.89%
10.70%
Note: *Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 14>>>
– 14 –
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares
allotted
Allotment
as % of 
International
Offering 
(assuming the
Over-
allotment 
Option is not
exercised)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option is fully 
exercised)
Allotment 
as % of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Allotment 
as % of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
Number of 
H Shares 
held upon
Listing
Approximate 
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
Top 1
0
0.00%
0.00%
0.00%
0.00%
26,512,466
27.45%
26.97%
Top 5
0
0.00%
0.00%
0.00%
0.00%
55,372,215
57.34%
56.32%
Top 10
3,398,400
32.58%
27.93%
29.32%
25.50%
71,779,416
74.33%
73.01%
Top 25
6,653,900
63.80%
54.68%
57.42%
49.93%
91,638,739
94.89%
93.21%
Note: *Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 15>>>
– 15 –
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders*
Number of 
H Shares
allotted
Allotment
as % of 
International
Offering 
(assuming the
Over-
allotment 
Option is not
exercised)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option is fully 
exercised)
Allotment 
as % of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Allotment 
as % of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
Number of 
H Shares 
held upon
Listing
Approximate 
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
Top 1
0
0.00%
0.00%
0.00%
0.00%
26,512,466
27.45%
26.97%
Top 5
0
0.00%
0.00%
0.00%
0.00%
55,372,215
57.34%
56.32%
Top 10
3,398,400
32.58%
27.93%
29.32%
25.50%
71,779,416
74.33%
73.01%
Top 25
6,653,900
63.80%
54.68%
57.42%
49.93%
91,638,739
94.89%
93.21%
Note: *Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon 
Listing.

<<<PAGE 16>>>
– 16 –
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made 
by the public will be conditionally allocated on the basis set out below:
Number of 
H Shares 
applied for
Number 
of valid 
applications
Pool A
Approximate 
percentage 
allotted of 
the total 
number of 
H Shares 
applied for
Basis of allocation/ballot
100
57,110
1,143 out of 57,110 applicants to receive 100 H Shares
2.00%
200
7,842
190 out of 7,842 applicants to receive 100 H Shares
1.21%
300
4,537
123 out of 4,537 applicants to receive 100 H Shares
0.90%
400
2,682
78 out of 2,682 applicants to receive 100 H Shares
0.73%
500
2,694
84 out of 2,694 applicants to receive 100 H Shares
0.62%
600
2,120
69 out of 2,120 applicants to receive 100 H Shares
0.54%
700
1,762
60 out of 1,762 applicants to receive 100 H Shares
0.49%
800
5,249
185 out of 5,249 applicants to receive 100 H Shares
0.44%
900
1,196
44 out of 1,196 applicants to receive 100 H Shares
0.41%
1,000
5,850
218 out of 5,850 applicants to receive 100 H Shares
0.37%
1,500
6,008
250 out of 6,008 applicants to receive 100 H Shares
0.28%
2,000
2,989
135 out of 2,989 applicants to receive 100 H Shares
0.23%
2,500
2,139
103 out of 2,139 applicants to receive 100 H Shares
0.19%
3,000
2,162
109 out of 2,162 applicants to receive 100 H Shares
0.17%
3,500
1,566
82 out of 1,566 applicants to receive 100 H Shares
0.15%
4,000
1,306
71 out of 1,306 applicants to receive 100 H Shares
0.14%
4,500
1,055
59 out of 1,055 applicants to receive 100 H Shares
0.12%

<<<PAGE 17>>>
– 17 –
Number of 
H Shares 
applied for
Number 
of valid 
applications
Pool A
Approximate 
percentage 
allotted of 
the total 
number of 
H Shares 
applied for
Basis of allocation/ballot
5,000
2,219
128 out of 2,219 applicants to receive 100 H Shares
0.12%
6,000
1,691
103 out of 1,691 applicants to receive 100 H Shares
0.10%
7,000
1,567
99 out of 1,567 applicants to receive 100 H Shares
0.09%
8,000
1,534
101 out of 1,534 applicants to receive 100 H Shares
0.08%
9,000
1,213
82 out of 1,213 applicants to receive 100 H Shares
0.08%
10,000
6,982
485 out of 6,982 applicants to receive 100 H Shares
0.07%
20,000
3,897
327 out of 3,897 applicants to receive 100 H Shares
0.04%
30,000
3,287
307 out of 3,287 applicants to receive 100 H Shares
0.03%
40,000
1,862
188 out of 1,862 applicants to receive 100 H Shares
0.03%
50,000
1,978
212 out of 1,978 applicants to receive 100 H Shares
0.02%
60,000
1,594
180 out of 1,594 applicants to receive 100 H Shares
0.02%
70,000
1,423
167 out of 1,423 applicants to receive 100 H Shares
0.02%
80,000
3,391
413 out of 3,391 applicants to receive 100 H Shares
0.02%
Total
140,905
Total number of Pool A successful applicants: 5,795
Number of 
H Shares 
applied for
Number 
of valid 
applications
Pool B
Approximate 
percentage 
allotted of 
the total 
number of 
H Shares 
applied for
Basis of allocation/ballot
90,000
3,345
904 out of 3,345 applicants to receive 100 H Shares
0.03%
100,000
7,040
1,992 out of 7,040 applicants to receive 100 H Shares
0.03%
200,000
2,417
931 out of 2,417 applicants to receive 100 H Shares
0.02%
300,000
1,208
557 out of 1,208 applicants to receive 100 H Shares
0.02%
400,000
638
334 out of 638 applicants to receive 100 H Shares
0.01%
500,000
316
183 out of 316 applicants to receive 100 H Shares
0.01%
579,400
1,446
893 out of 1,446 applicants to receive 100 H Shares
0.01%
Total
16,410
Total number of Pool B successful applicants: 5,794

<<<PAGE 18>>>
– 18 –
As of the date of this announcement, the relevant subscription monies previously deposited 
in the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers for any inquiries.
OTHERS/ADDITIONAL INFORMATION
Additional Special Bonus
Taking into consideration the contributions made by CICCHKS to the success of the Global 
Offering, in addition to the underwriting commission and incentive fee disclosed in the section 
headed “Underwriting — Underwriting Arrangements and Expenses — The International 
Offering — Total Commission and Expenses” in the Prospectus, the Company agrees to 
pay an additional incentive fee of HK$6 million (the “Special Bonus”) to CICCHKS upon 
the Listing. Taking into account the Special Bonus, based on the Offer Price of HK$58.85, 
assuming no exercise of the Over-allotment Option, the total estimated listing expenses 
in relation to the Global Offering will be approximately HK$72.6 million. The Company 
proposed the Additional Special Bonus on September 23, 2026 and it was not discussed 
between the Company and CICCHKS prior to September 23, 2026. 
The Company and the Joint Sponsors are of view that the adjustments to the listing expenses 
and use of proceeds as a result of the Special Bonus are not material to the business operations, 
financial positions and prospect of the Company, and that the Special Bonus arrangement does 
not constitute a significant change or a significant new matter for the purposes of Rule 11.13 
of the Listing Rules, for the following reasons: (i) changes of amount of the net proceeds to 
be used for each purpose disclosed in the Prospectus are less than 10%; (ii) the Company will 
continue to have sufficient funding for each intended purpose disclosed in the Prospectus with 
its available financial resources; and (iii) the intended purposes and proportional allocations 
of the net proceeds will remain unchanged, details of which are as follows: 
Taking into account the Special Bonus, assuming the Over-allotment Option is not exercised, 
based on the Offer Price of HK$58.85, the net proceeds from the Global Offering to be 
received by the Company, after deduction of the underwriting commissions, fees and estimated 
expenses payable by the Company in connection with the Global Offering, are estimated to 
be approximately HK$609.4 million. The Company intends to use the net proceeds for the 
following purposes:
• 
approximately HK$396.1 million (representing 65.0% of the net proceeds) will be 
allocated to enhance the Company’s R&D capabilities to strengthen its core technologies 
and the research and development of sensor products;
• 
approximately HK$152.4 million (representing 25.0% of the net proceeds) will be 
allocated to enhance its manufacturing capabilities; and
• 
approximately HK$60.9 million (representing 10.0% of the net proceeds) will be used 
for its working capital and general corporate purposes.

<<<PAGE 19>>>
– 19 –
Allocation of H Shares to Existing Minority Shareholder(s) and their close associate(s)
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, 
a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of the Placing Guidelines to permit the Offer Shares in the International 
Offering to be placed to a close associate (“Relevant Placee”) of an Existing Minority 
Shareholder (“Relevant Existing Shareholder”), subject to the conditions as follows:
(i) 
the Relevant Existing Shareholder holds less than 5% of the total voting rights in the 
Company prior to the completion of the Global Offering;
(ii) the Relevant Existing Shareholder is not, and will not be, a core connected person of the 
Company or any close associate of any such core connected person immediately prior to 
or following the Global Offering;
(iii) the Relevant Existing Shareholder does not have the power to appoint any Directors nor 
have any other special rights in the Company;
(iv) allocation to such Relevant Existing Shareholder or her close associate will not affect 
the Company’s ability to satisfy the public float requirement under Rule 8.08(1) (as 
amended and replaced by Rule 19A.13A) of the Listing Rules;
(v) 
no preferential treatment has been, nor will be, given to the Relevant Existing 
Shareholder or the Relevant Placee by virtue of their relationship with the Company in 
any allocation in the International Offering; and
(vi) the relevant information in respect of the allocation to the Relevant Existing Shareholder 
and/or her close associate will be disclosed in this announcement.
For details, please refer to the section headed “Allotment Results Details – International 
Offering – Allottees with Waivers/Consents Obtained” in this announcement.

<<<PAGE 20>>>
– 20 –
Placing to connected clients with consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of 
their connected distributors pursuant to the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants. The Company has applied to the Stock Exchange for, and the 
Stock Exchange has granted the relevant consent(s) under paragraph 1C(1) of the Placing 
Guidelines to permit the Company to allocate such Offer Shares in the International Offering 
to the connected clients. The allocation of Offer Shares to such connected clients is in 
compliance with all the conditions under the consents granted by the Stock Exchange. Details 
of the placement to connected clients are set out below.
No.
Connected 
Distributor
Connected 
Client
Relationship 
with the 
Connected 
Distributor
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
on behalf of 
such scheme
No. of Offer 
Shares to be 
allocated
Approx.% 
of total 
Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
Approx.% of 
total issued 
Shares upon 
Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Part A – Connected Clients holding beneficial interest in the Offer Shares on a non-discretionary basis on behalf of 
independent third parties
1
GF Securities 
(Hong Kong) 
Brokerage
GF Securities 
AM(1)
GF Securities 
AM is a 
member of the 
same group of 
companies as 
GF Securities 
(Hong Kong) 
Brokerage.
No
5,400
0.05%
0.01%

<<<PAGE 21>>>
– 21 –
No.
Connected 
Distributor
Connected 
Client
Relationship 
with the 
Connected 
Distributor
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
on behalf of 
such scheme
No. of Offer 
Shares to be 
allocated
Approx.% 
of total 
Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
Approx.% of 
total issued 
Shares upon 
Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Part B – Connected Clients holding beneficial interest in the Offer Shares on a discretionary basis on behalf of independent 
third-party investors
2
CICCHKS
CICC(2)
CICC is a 
member of the 
same group of 
companies as 
CICCHKS.
Yes(2)
3,000
0.03%
0.003%
3
GF Securities
(Hong Kong)
Brokerage
VPHK(3)
VPHK is a 
member of the 
same group of 
companies as 
GF Securities 
(Hong Kong) 
Brokerage
Yes(3)
1,300
0.01%
0.001%
4
GF Securities
(Hong Kong)
Brokerage
VPL(3)
VPL is a 
member of the 
same group of 
companies as 
GF Securities 
(Hong Kong) 
Brokerage
Yes(3)
100
0.0009%
0.0001%

<<<PAGE 22>>>
– 22 –
Notes:
1. 
GF Securities AM will hold the Offer Shares in its capacity as the fund manager managing the funds on 
behalf of its investors (the “GF Securities AM Ultimate Clients”). GF Securities AM is a direct wholly-
owned subsidiary of GF Securities Co., Ltd. (Stock Code: 1776) (“GF Securities”) and GF Securities 
(Hong Kong) Brokerage is an indirect wholly-owned subsidiary of GF Securities, therefore GF Securities 
AM is a member of the same group of companies as GF Securities (Hong Kong) Brokerage. GF Securities 
AM is therefore considered as a connected client of GF Securities (Hong Kong) Brokerage pursuant to 
paragraph 1B(7) of the Placing Guidelines.
GF Securities AM is to invest on a non-discretionary basis on behalf of the GF Securities AM Ultimate 
Clients, each of which is, to the best knowledge and belief and after due enquiry of GF Securities AM, 
an independent third party of the Company, the Single Largest Group of Shareholders, its substantial 
shareholders, its subsidiaries, GF Securities AM, GF Securities (Hong Kong) Brokerage and the 
companies which are members of the same group of companies as GF Securities (Hong Kong) Brokerage, 
and no proprietary money is used for the subscription of Offer Shares. The details of the GF Securities 
AM Ultimate Clients are as follows:
Name of the funds to which the 
Offer Shares will be allocated
Whether any investor holds 
30% or more interest in the fund
Ultimate beneficial owner with 30% or 
more interests and shareholding (%)
CIB-GFAM CHINA HK STOCKS 
MULTISTRATEGY AMA NO.7
Yes
Zhonghe Capital Cultivation 920 Private 
Securities Investment Fund 
中和資本耕耘920號私募證券投資基金, 
whose ultimate beneficial owner 
is Zhang Jingting (張敬庭)
SPDB – GF SECURITIES ASSET 
MANAGEMENT (GUANGDONG) 
CO., LTD. CHKMS AMA NO.12
Yes
Zhonghe Capital Cultivation 810 Private 
Securities Investment Fund 
中和資本耕耘810號私募證券投資基金, 
whose ultimate beneficial owner 
is Zhang Jingting (張敬庭)
2. 
CICCHKS is a wholly-owned subsidiary of CICC, and therefore a member of the same group of companies 
as CICC. Accordingly, CICC is a connected client of CICCHKS.
CICC is investing on behalf of a collective investment scheme which is not authorized by the SFC, the 
details of which are as follows:
Name
Types and 
values of 
assets under 
management 
Whether 
the scheme 
is publicly 
marketed
Scheme 
establishment 
date
Identities of the 
general partners 
and the 20 largest 
limited partners of 
the scheme where 
applicable
Identity of 
the scheme 
administrator
CICC229 
ICBC(ASIA)LTD-
ICBC LTD-CICC 
Gong Yin JXCL 
NO.1 CIS (“CICC 
Gong Yin”)
Collective asset 
management 
plan Value: 
RMB93,000,000
No
June 26, 2026
Not applicable as it 
is not in partnership 
structure and does 
not have any general 
partner or limited 
partner
CICC

<<<PAGE 23>>>
– 23 –
As confirmed by CICC, (i) ICBC Wealth Wisdom Joy Minimum Holding Period 180 Days Fixed Income 
Open End Net Value Wealth Management Product (工銀理財有限責任公司工銀理財智悅最短持有180
天固定收益類開放式淨值型理財產品) (“ICBC Wealth Wisdom Joy”) owns 30% or more interest in 
CICC Gong Yin as an investor and there are no ultimate beneficial owners who hold 30% or more interest 
in ICBC Wealth Wisdom Joy; (ii) there are no other ultimate beneficial owners who hold 30% or more 
interest in CICC Gong Yin; (iii) each of the ultimate beneficial owners is an independent third party of the 
Company, the Single Largest Group of Shareholders, its substantial shareholders, its subsidiaries, CICC, 
CICCHKS and the companies which are members of the same group of companies as CICCHKS. 
3. 
Each of VPHK and VPL is a member of the same group of companies as GF Securities (Hong Kong) 
Brokerage. GF Securities (Hong Kong) Brokerage is an indirect wholly-owned subsidiary of GF 
Securities. Each of VPHK and VPL is a wholly-owned subsidiary of Value Partners Group Limited (Stock 
Code: 806) (“VPGL”). GF Securities is interested in 20.04% shareholding in VPGL which renders each of 
VPHK and VPL an associate of GF Securities. Accordingly, each of VPHK and VPL is a member of the 
same group of companies as GF Securities (Hong Kong) Brokerage and is considered as a connected client 
of GF Securities (Hong Kong) Brokerage under paragraph 1B(7) of the Placing Guidelines. 
Each of VPHK and VPL will hold the Offer Shares in its capacity as the discretionary fund manager 
managing the funds on behalf of its investors (the “VP Ultimate Clients”). Each of VPHK and VPL is to 
invest on a discretionary basis on behalf of the VP Ultimate Clients which are independent third parties 
and no proprietary money is used for the subscription of Offer Shares. To the best knowledge of each of 
VPHK and VPL, each of the VP Ultimate Clients is an independent third party of the Company, the Single 
Largest Group of Shareholders, its substantial shareholders, its subsidiaries, VPHK, VPL, GF Securities 
(Hong Kong) Brokerage and the companies which are members of the same group of companies as GF 
Securities (Hong Kong) Brokerage. 
The details of the VP Ultimate Clients are as follows:
Name of the funds to which the Offer 
Shares will be allocated
Fund Manager
Whether any investor 
holds 30% or more 
interest in the fund
Ultimate beneficial owner 
with 30% or more interests 
and shareholding (%)
Value Partners Ireland Fund ICAV – 
Value Partners Asia Ex-Japan Equity 
Fund (“Value Partners Ireland Fund”)
VPHK
Yes
1. International Fund Services 
& Asset Management 
S.A.(Note 1)
2. Clearstream Banking 
S.A.(Note 1)
Value Partners Intelligent Funds – JA-
VP China New Century Fund (“Value 
Partners Intelligent Funds”)
VPL
Yes
Aizawa Securities Co. Ltd(Note 1)
Value Partners Multi-Asset Fund 
VPHK
Yes
AIA International Limited(Note 1)
Value Partners Funds SPC – Value 
Partners China A-Share Innovation Fund 
SP (“Value Partners Funds SPC”)
VPHK
Yes
Custody Bank of Japan, 
Ltd(Note 1)
Note 1: 
To the best knowledge of VPHK and VPL, there are no ultimate beneficial owners who hold 
30% or more interests in the entity(ies).

<<<PAGE 24>>>
– 24 –
Among the VP Ultimate Clients, Value Partners Ireland Fund, Value Partners Intelligent Funds and Value 
Partners Funds SPC are collective investment schemes which are not authorized by the SFC, details of 
which are as follows:
Fund name
Types and 
values of 
assets under 
management
Whether 
the scheme 
is publicly 
marketed
Scheme 
establishment 
date
Identities of the 
general partners 
and the 20 largest 
limited partners of 
the scheme where 
applicable
Identity of 
the scheme 
administrator
Value Partners 
Ireland Fund
ICAV fund, 
USD23 million as 
of Sep 2026 
Yes 
3 Sep 2018
Not applicable as it 
is not in partnership 
structure and does 
not have any general 
partner or limited 
partner
HSBC 
Securities 
Services 
(Ireland) DAC
Value Partners 
Intelligent Funds – 
Private fund, 
USD6 million as 
of Sep 2026
No 
 7 Mar 2002
Not applicable as it 
is not in partnership 
structure and does 
not have any general 
partner or limited 
partner
HSBC Trustee 
(Cayman) 
Limited 
Value Partners 
Funds SPC
Private fund, 
USD14 million as 
of Sep 2026
No 
 19 Nov 2018
Not applicable as it 
is not in partnership 
structure and does 
not have any general 
partner or limited 
partner
HSBC Trustee 
(Cayman) 
Limited 
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in 
respect of which consent has been obtained, the Company has complied with the Listing Rules 
and guidance materials in relation to the placing, allotment and listing of the Company’s H 
Shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or 
indirectly, provided by the Company, the Directors or syndicate members to any placees or the 
public (as the case may be) and the consideration payable by them for each H Share subscribed 
for or purchased by them is the same as the Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and trading fee payable.
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of 
this announcement, make no representation as to its accuracy or completeness and expressly 
disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the 
whole or any part of the contents of this announcement.
This announcement is for information purposes only and does not constitute an invitation 
or offer to acquire, purchase or subscribe for any securities. This announcement is not a 
prospectus. Potential investors should read the Prospectus dated September 22, 2026 for 
detailed information about the Global Offering before deciding whether or not to invest in the 
Offer Shares. Any investment decision in relation to the Offer Shares should be taken solely 
in reliance on the information provided in the Prospectus.

<<<PAGE 25>>>
– 25 –
This announcement is not for release, publication, distribution, directly or indirectly, in or 
into the United States (including its territories and possessions, any state of the United States 
and the District of Columbia). This announcement does not, and is not intended to, constitute 
or form a part of any offer or solicitation to purchase or subscribe for securities in the United 
States or in any other jurisdictions. The Offer Shares have not been, and will not be, registered 
under the United States Securities Act of 1933, as amended from time to time (the “U.S. 
Securities Act”), or securities law of any state or other jurisdiction of the United States. The 
Offer Shares may not be offered, sold, pledged or otherwise transferred within the United 
States or to, or for the account or benefit of U.S. persons (as defined in Regulation S under 
the U.S. Securities Act), except pursuant to an available exemption from, or in a transaction 
not subject to, the registration requirements of the U.S. Securities Act. There will be no public 
offer of the Offer Shares in the United States. The Offer Shares are being offered and sold 
solely outside the United States in offshore transactions in reliance on Regulation S under the 
U.S. Securities Act.
*Potential investors of the Offer Shares should note that the Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the 
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of 
the events set out in the section headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Grounds for termination” in the Prospectus at 
any time prior to 8:00 a.m. on the day that trading in the H Shares commences on the Stock 
Exchange.
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering and based on the Offer Price of 
HK$58.85 per H Share, assuming that the Over-allotment Option is not exercised:
(1) 
58,507,523 H Shares represent approximately 60.58% of the total issued share capital of 
the Company will be counted towards the public float for the purpose of Rule 19A.13A 
of the Listing Rules, which is higher than the prescribed percentage of H Shares required 
to be held in public hands of 25.00% under Rule 8.08(1) (as amended and replaced by 
Rule 19A.13A(1)) of the Listing Rules.
(2) 
excluding the Offer Shares to be allocated to the Cornerstone Investors that are subject 
to a lock-up period of six months following the Listing Date and the H Shares held 
by existing Shareholders to be converted from Unlisted Shares that are subjected to 
a lock-up period of 12 months following the Listing Date under the applicable PRC 
laws, the Company’s H Shares to be counted towards the free float upon Listing will be 
9,719,600 H Shares. Based on the Offer Price of HK$58.85 per H Share, the free float 
of the Company represents approximately 10.06% of the total issued share capital of the 
Company at the time of Listing with a market value of approximately HK$572.0 million. 
Accordingly, the Company will satisfy the free float requirement under Rule 19A.13C(1) 
of the Listing Rules.

<<<PAGE 26>>>
– 26 –
The Directors confirm that, immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public shareholders 
of the Company do not hold more than 50% of the H shares in public hands at the time of the 
Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will 
be at least 300 Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the 
Listing Rules.
COMMENCEMENT OF DEALINGS
H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, 
September 30, 2026 (Hong Kong time), provided that the Global Offering has become 
unconditional and the right of termination described in the section headed “Underwriting” in 
the Prospectus has not been exercised. Investors who trade H Shares prior to the receipt of H 
Share certificates or the H Share certificates becoming valid do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong Kong 
time) on Wednesday, September 30, 2026, it is expected that dealings in the H Shares on 
the Stock Exchange will commence at 9:00 a.m. on Wednesday, September 30, 2026. The H 
Shares will be traded in board lots of 100 H Shares each and the stock code of the H Shares 
will be 6802.
By Order of the Board
Shenzhen Camsense Technologies Co., Ltd.
Wang Jian
Executive Director and Chairman of the Board
Hong Kong, September 29, 2026
As at the date of this announcement, the Board comprises: (i) Mr. Wang Jian, Mr. Zhou Kun, 
Mr. Huang Shuguang and Ms. Qiu Lin as executive Directors; (ii) Ms. Li Shangran and 
Mr. Liu Xinpeng as non-executive Directors; and (iii) Mr. Dong Shengtang, Mr. Conrad Yan 
and Mr. Liang Wenzhao as independent non-executive Directors.
