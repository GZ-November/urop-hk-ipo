# 配发结果公告抽取任务：3296.HK Huaqin Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**22/04/2026 22:21**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0422/2026042202072.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3296.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities 
in the United States or in any other jurisdictions. The Offer Shares have not been and will not be registered under 
the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities Act”) or securities law 
of any state or other jurisdiction of the United States and may not be offered, sold, pledged or otherwise transferred 
within the United States, except in transactions exempt from, or not subject to, the registration requirements of the 
U.S. Securities Act and in compliance with any applicable state securities laws. There will be no public offer of the 
Offer Shares in the United States. The Offer Shares are being offered and sold solely (1) to qualified institutional 
buyers as defined in Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under the U.S. 
Securities Act; and (2) outside the United States in offshore transactions in reliance on Regulation S under the U.S. 
Securities Act and applicable laws of each jurisdiction where those offers and sales occur.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
April 15, 2026 (the “Prospectus”) issued by Huaqin Co., Ltd. (華勤技術股份有限公司) (the “Company”) for detailed 
information about the Global Offering described below before deciding whether or not to invest in the H Shares 
thereby being offered. Any investment decision in relation to the Offer Shares should be taken solely in reliance on the 
information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited, 
as stabilizing manager (the “Stabilizing Manager”) (or its affiliates or any person acting for it), on behalf of the 
Underwriters, to the extent permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, 
may over-allocate or effect transactions with a view to stabilizing or supporting the market price of the H Shares at 
such price, in such amounts and in such manners as the Stabilizing Manager, its affiliates or any person acting for it 
may determine and at a level higher than that which might otherwise prevail for a limited period after the Listing Date. 
However, there is no obligation on the Stabilizing Manager (or its affiliates or any person acting for it) to conduct 
any such stabilizing action. Such stabilizing action, if taken, (a) will be conducted at the absolute discretion of the 
Stabilizing Manager (or its affiliates or any person acting for it) and in what the Stabilizing Manager reasonably 
regards as the best interest of our Company, (b) may be discontinued at any time and (c) is required to be brought to an 
end within 30 days of the last day for lodging applications under the Hong Kong Public Offering (which is Wednesday, 
May 20, 2026). Such stabilizing action, if taken, may be effected in all jurisdictions where it is permissible to do so, 
in each case in compliance with all applicable laws, rules and regulatory requirements, including the Securities and 
Futures (Price Stabilizing) Rules (Chapter 571 W of the Laws of Hong Kong), as amended, made under the Securities 
and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Wednesday, May 20, 2026). 
After this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of 
the H Shares, could fall.
Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) and the Overall Coordinators shall be entitled to terminate 
their obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any 
of the events set out in the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong 
Public Offering – Hong Kong Underwriting Agreement – Grounds for Termination” in the Prospectus at any time prior 
to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Thursday, April 23, 2026).

<<<PAGE 2>>>
2
Huaqin Co., Ltd.
華勤技術股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the Global 
Offering
:
58,548,200 H Shares (subject to the Over-
allotment Option)
Number of Hong Kong Offer Shares
:
5,854,900 H Shares
Number of International Offer Shares
:
52,693,300 H Shares (subject to the Over-
allotment Option)
Final Offer Price
:
HK$77.70 per H Share, plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
AFRC transaction levy of 0.00015% and 
Stock Exchange trading fee of 0.00565% 
(payable in full on application in Hong 
Kong dollars and subject to refund)
Nominal Value
:
RMB1.00 per H Share
Stock Code
:
3296
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators,
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
Huaqin Co., Ltd.
華勤技術股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated April 15, 2026 (the “Prospectus”) issued by 
Huaqin Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could 
move substantially even with a small number of H Shares traded and should exercise extreme 
caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
3296
Stock short name
HUAQIN
Dealings commencement date
April 23, 2026#
# 
see note at the end of the announcement
Price Information
Final Offer Price
HK$77.70
Maximum Offer Price
HK$77.70
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the Over-allotment 
Option)
58,548,200
Final Number of Offer Shares in Hong Kong Public Offering
5,854,900
Final Number of Offer Shares in International Offering (before 
exercise of the Over-allotment Option)
52,693,300
Number of issued Shares upon Listing (before exercise of the 
Over-allotment Option)
1,074,280,544

<<<PAGE 4>>>
4
Offer Size Adjustment Option (Upsize option)
Number of additional shares issued under the option
0*
– Hong Kong Public Offering
–
– International Offering
–
* 
The Offer Size Adjustment Option has not been exercised.
Over-allocation
No. of Offer Shares over-allocated
8,782,200
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$4,549.2 million
Less: Estimated listing expenses payable based on the Final Offer 
Price
HK$86.1 million
Net proceeds
HK$4,463.1 million
Note: Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
The Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if any) 
for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus on a pro rata 
basis.

<<<PAGE 5>>>
5
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
140,150
No. of successful applications
42,660
Subscription level
531.33 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong 
Public Offering
5,854,900
No. of Offer Shares reallocated from the International Offering 
(reallocation)
0
Final no. of Offer Shares under the Hong Kong Public Offering
5,854,900
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering (before the exercise of the Over-allotment 
Option)
10%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by identification number or www.hkeipo.hk/IPOResult for the full 
list of allottees.
INTERNATIONAL OFFERING
No. of placees
171
Subscription Level
13.34 times
No. of Offer Shares initially available under the International 
Offering
52,693,300
Final no. of Offer Shares under the International Offering
52,693,300
% of Offer Shares under the International Offering to the Global 
Offering (before the exercise of the Over-allotment Option)
90%

<<<PAGE 6>>>
6
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a 
waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit the Company to allocate certain Offer Shares in the International Offering to 
certain permitted existing shareholders (“Existing Minority Shareholders”) and/or their close 
associates; and (b) a consent under Chapter 4.15 of the Guide for New Listing Applicants to permit 
the Company to, among other things, allocate further H Shares in the International Offering to 
the Cornerstone Investors, existing shareholders and/or their close associates (i) none of the Offer 
Shares subscribed by the placees and the public have been financed directly or indirectly by the 
Company, any of the Directors, chief executive, substantial Shareholders, existing Shareholders 
of the Company or any of its subsidiaries or their respective close associates; and (ii) none of the 
placees and the public who have purchased the Offer Shares are accustomed to taking instructions 
from the Company, any of the Directors, chief executive, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates in 
relation to the acquisition, disposal, voting or other disposition of H Shares registered in his/her/its 
name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investor
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1/
Note 2
% of total issued 
share capital in 
the Company 
after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1/
Note 2
Existing 
Shareholders 
or their close 
associates
JPMAMAPL
6,858,800
11.71%
0.64%
Yes
UBS AM Singapore
1,008,600
1.72%
0.09%
Yes
Shanghai Gaoyi and CICC FT (in 
connection with Gaoyi OTC Swaps)
1,230,500
2.10%
0.11%
Yes
Perseverance Asset Management
786,700
1.34%
0.07%
Yes
Cloud Map
2,017,300
3.45%
0.19%
No
Taikang Life
2,017,300
3.45%
0.19%
Yes
3W Fund
1,512,900
2.58%
0.14%
No
New China Asset Management
1,008,600
1.72%
0.09%
No
Everbright Wealth
1,008,600
1.72%
0.09%
No
IvyRock
1,008,600
1.72%
0.09%
No
Aurora SF (in connection with the 
Arrangement)
2,521,600
4.31%
0.23%
No

<<<PAGE 7>>>
7
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1/
Note 2
% of total issued 
share capital in 
the Company 
after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1/
Note 2
Existing 
Shareholders 
or their close 
associates
KIL
2,521,600
4.31%
0.23%
No
OmniVision HK
1,512,900
2.58%
0.14%
No
Green Better
1,008,600
1.72%
0.09%
No
Hongxing International
1,008,600
1.72%
0.09%
No
Ingenic Semiconductor HK
1,008,600
1.72%
0.09%
No
Awinic Technology Limited
1,008,600
1.72%
0.09%
No
JinYi Capital (acting for and on behalf 
of Structured Credit SP Fund)
201,700
0.34%
0.02%
No
Total
29,250,100
49.96%
2.72%
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering (assuming the Over-allotment Option is not exercised).
(2) 
In addition to the Offer Shares subscribed for as Cornerstone Investors, Everbright Wealth, 3W Fund, 
IvyRock, Awinic Technology Limited, Perseverance Asset Management, Shanghai Gaoyi and CICC FT (in 
connection with Gaoyi OTC Swaps), Ingenic Semiconductor HK, Cloud Map, KIL, UBS AM Singapore, 
OmniVision HK, Taikang Life, New China Asset Management and JPMAMAPL, and/or their close 
associates, were allocated further Offer Shares as placees in the International Offering. Please refer to the 
section headed “Allotment Results Details – International Offering – Allottees with Waivers/Consents 
Obtained” in this announcement for details. Only the Offer Shares subscribed for as Cornerstone Investors are 
subject to lock-up as indicated below. For details, please refer to the section headed “Lock-up Undertakings – 
Cornerstone Investors” in this announcement.

<<<PAGE 8>>>
8
Allottee with Waiver/Consent Obtained
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 3
% of total issued 
share capital in 
the Company 
after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 4
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 
1C(2) of the Placing Guidelines in relation to subscription for H Shares by Existing Minority Shareholders holding 
more than 1% of the issued share capital of the Company immediately prior to the completion of the Global 
Offering and/or their close associates
JPMAMAPL
8,270,900
14.13%
0.77%
Existing Minority 
Shareholder and/or 
its close associates, 
and a Cornerstone 
Investor
Allottees with consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of 
further H Shares to existing Shareholders and Cornerstone Investors and/or their close associates Note 1
Everbright Wealth
201,700
0.34%
0.02%
A Cornerstone 
Investor
3W Fund
806,900
1.38%
0.08%
A Cornerstone 
Investor
IvyRock
201,700
0.34%
0.02%
A Cornerstone 
Investor
Awinic Technology Limited
201,700
0.34%
0.02%
A Cornerstone 
Investor
Perseverance Asset Management
217,700
0.37%
0.02%
A Cornerstone 
Investor and an 
existing shareholder
Shanghai Gaoyi and CICC FT 
(in connection with Gaoyi OTC 
Swaps)
286,600
0.49%
0.03%
A Cornerstone 
Investor and an 
existing shareholder
Ingenic Semiconductor HK
201,700
0.34%
0.02%
A Cornerstone 
Investor
Cloud Map
1,008,600
1.72%
0.09%
A Cornerstone 
Investor

<<<PAGE 9>>>
9
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 3
% of total issued 
share capital in 
the Company 
after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 4
Relationship
KIL
1,008,600
1.72%
0.09%
A Cornerstone 
Investor
UBS AM Singapore
1,008,600
1.72%
0.09%
A Cornerstone 
Investor and an 
existing shareholder
OmniVision HK
504,300
0.86%
0.05%
A Cornerstone 
Investor
Taikang Asset Management 
(Hong Kong) Company Limited 
(“Taikang AM”)
4,300
0.01%
0.00%
A close associate 
of Taikang Life, a 
Cornerstone Investor 
and an existing 
shareholder
Taikang Life
500,000
0.85%
0.05%
A Cornerstone 
Investor and an 
existing
shareholder
New China Asset Management
201,700
0.34%
0.02%
A Cornerstone 
Investor
JPMAMAPL
1,412,100
2.41%
0.13%
A Cornerstone 
Investor and an 
existing shareholder
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients Note 2
Shanghai Gaoyi and CICC FT 
(in connection with Gaoyi OTC 
Swaps)
286,600
0.49%
0.03%
CICC Financial 
Trading Limited 
(“CICC FT”) is 
a member of the 
same group as 
China International 
Capital Corporation 
Hong Kong 
Securities Limited 
(“CICCHKS”)
Beijing Hengde and CICC FT (in 
connection with Beijing Hengde 
OTC Swaps)
201,700
0.34%
0.02%
CICC FT is a 
member of the same 
group as CICCHKS
Longyan Huasheng and CICC 
FT (in connection with Longyan 
Huasheng OTC Swaps)
504,300
0.86%
0.05%
CICC FT is a 
member of the same 
group as CICCHKS

<<<PAGE 10>>>
10
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 3
% of total issued 
share capital in 
the Company 
after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 4
Relationship
Shenwan Hongyuan and CICC FT 
(in connection with SWHY OTC 
Swaps)
201,700
0.34%
0.02%
CICC FT is a 
member of the same 
group as CICCHKS
Yuanlesheng AM and CICC FT (in 
connection with Yuanlesheng OTC 
Swaps)
50,400
0.09%
0.00%
CICC FT is a 
member of the same 
group as CICCHKS
Guotai Junan Investments 
(Hong Kong) Limited (“GTJA 
Investments”)
348,100
0.59%
0.03%
GTJA Investments 
is a member of the 
same group as Guotai 
Junan Securities 
(Hong Kong) 
Limited (“GTJA 
Securities”) and 
Haitong International 
Securities Company 
Limited (“Haitong 
Securities”)
UBS AM Singapore
2,017,200
3.44%
0.18%
UBS AG Hong 
Kong Branch (“UBS 
AG”) and UBS 
AM Singapore are 
members of the same 
group
Fullgoal Asset Management (HK) 
Limited (“Fullgoal HK”)
200,000
0.34%
0.02%
Fullgoal HK, 
Fullgoal Fund, 
Haitong Securities 
and GTJA Securities 
are members of the 
same group
Fullgoal Fund Management Co., 
Ltd. (“Fullgoal Fund”)
606,900
1.04%
0.06%
HSBC Broking Securities (Asia) 
Limited (“HSBC Broking”)
253,200
0.43%
0.02%
The Hongkong and 
Shanghai Banking 
Corporation Limited 
PB (“HSBC”), 
HSBC GAM and 
HSBC Broking are 
members of the same 
group
HSBC Global Asset Management 
(Hong Kong) Limited (“HSBC 
GAM”)
806,900
1.38% 
0.08% 

<<<PAGE 11>>>
11
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 3
% of total issued 
share capital in 
the Company 
after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 4
Relationship
HuaAn Fund Management Co., Ltd 
(“HuaAn Fund”)
10,000
0.02%
0.00%
HuaAn Fund, 
Haitong Securities 
and GTJA Securities 
are members of the 
same group
CITIC-Prudential Fund 
Management Company Ltd. 
(“CITIC-Prudential Fund”)
151,200 
0.26% 
0.01% 
CITIC-Prudential 
Fund and CLSA 
Limited (“CLSA”) 
are members of the 
same group
Notes:
1. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details – International Offering – Cornerstone Investors” in this announcement. For details of the 
consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further H 
Shares to the existing Shareholders and/or their close associates and Cornerstone Investors, please refer to 
the section headed “Others/Additional Information – Allottees with consent under Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations of further H Shares to Cornerstone Investors” in this 
announcement.
2. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients, please refer to the section headed 
“Others/Additional Information – Placing to connected clients with a prior consent under paragraph 1C(1) of 
the Placing Guidelines” in this announcement.
3. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering (assuming the Over-allotment Option is not exercised).
4. 
Not taking into account any A Shares held by the relevant investors.

<<<PAGE 12>>>
12
LOCK-UP UNDERTAKINGS
Controlling Shareholders Group
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject to the 
lock-up undertakings
Qiu Wensheng Note 3
48,746,040
4.54%
October 22, 2026 (First Six 
Month Period) Note 1
April 22, 2027 (Second Six 
Month Period) Note 2
Shanghai Aoqin Note 3
321,300,000
29.91%
October 22, 2026 (First Six 
Month Period) Note 1
April 22, 2027 (Second Six 
Month Period) Note 2
Shanghai Haixian Note 3
56,700,000
5.28%
October 22, 2026 (First Six 
Month Period) Note 1
April 22, 2027 (Second Six 
Month Period) Note 2
Qiu Wenhui Note 3
18,060
0.00%
October 22, 2026 (First Six 
Month Period) Note 1
April 22, 2027 (Second Six 
Month Period) Note 2

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
% of 
shareholding in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject to the 
lock-up undertakings
Fujian Yuexiang Note 3
13,750,943
1.28%
October 22, 2026 (First Six 
Month Period) Note 1
April 22, 2027 (Second Six 
Month Period) Note 2
Total
440,515,043
41.01%
Notes:
1. 
The Controlling Shareholders Group may dispose of or transfer Shares after the indicated date subject to that 
each member of the Controlling Shareholders Group will not cease to be a Controlling Shareholders Group.
2. 
The Controlling Shareholders Group will cease to be prohibited from disposing or transferring Shares after 
the indicated date.
3. 
For illustrative purposes only, this subsection lists only those members of the Controlling Shareholders Group 
who hold Shares directly in the Company. Mr. Qiu Wensheng is a direct beneficial owner of 48,746,040 
Shares of the Company and controls 321,300,000 Shares of the Company through Shanghai Aoqin and 
56,700,000 Shares of the Company through Shanghai Haixian. Both Shanghai Aoqin and Shanghai Haixian 
are ultimately controlled by Mr. Qiu Wensheng. In addition, Mr. Qiu Wenhui, brother of Mr. Qiu Wensheng, 
is a direct beneficial owner of 18,060 Shares of the Company and controls 13,750,943 Shares of the Company 
through Fujian Yuexiang, which was held by Mr. Qiu Wenhui as to 90% as a limited partner and as to 10% 
by Ms. Lin Min (the spouse of Mr. Qiu Wenhui) as the general partner of Fujian Yuexiang. Ms. Lin Min has 
taken up the role as the general partner of Fujian Yuexiang purely based on the marital property arrangement 
between Mr. Qiu Wenhui and Ms. Lin Min. Shanghai Aoqin, Shanghai Haixian, Mr. Qiu Wenhui and Fujian 
Yuexiang are the parties acting in concert with Mr. Qiu Wensheng pursuant to applicable PRC laws. In 
addition, as advised by the PRC Legal Advisor of the Company, Ms. Lin Min is the general partner of Fujian 
Yuexiang, and Fujian Yuexiang is deemed to be controlled by Ms. Lin Min pursuant to the applicable PRC 
laws and the partnership agreement of Fujian Yuexiang.
Therefore, upon Listing, Mr. Qiu Wensheng, Shanghai Aoqin, Shanghai Haixian, Mr. Qiu Wenhui, Ms. Lin Min and 
Fujian Yuexiang will constitute the Controlling Shareholders Group and each of them is subject to the same lock-up 
as disclosed above. For further details, please refer to “Relationship with our Controlling Shareholder Group” in the 
Prospectus.

<<<PAGE 14>>>
14
Cornerstone Investors
Name
Number of 
shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 1
% of total issued 
share capital in 
the Company 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject to the 
lock-up undertakings 
Note 2
JPMAMAPL
6,858,800
11.71%
0.64%
October 22, 2026
UBS AM Singapore
1,008,600
1.72%
0.09%
October 22, 2026
Shanghai Gaoyi and CICC FT 
(in connection with Gaoyi OTC 
Swaps)
1,230,500
2.10%
0.11%
October 22, 2026
Perseverance Asset 
Management
786,700
1.34%
0.07%
October 22, 2026
Cloud Map
2,017,300
3.45%
0.19%
October 22, 2026
Taikang Life
2,017,300
3.45%
0.19%
October 22, 2026
3W Fund
1,512,900
2.58%
0.14%
October 22, 2026
New China Asset Management
1,008,600
1.72%
0.09%
October 22, 2026
Everbright Wealth
1,008,600
1.72%
0.09%
October 22, 2026
IvyRock
1,008,600
1.72%
0.09%
October 22, 2026
Aurora SF (in connection with 
the Arrangement)
2,521,600
4.31%
0.23%
October 22, 2026
KIL
2,521,600
4.31%
0.23%
October 22, 2026
OmniVision HK
1,512,900
2.58%
0.14%
October 22, 2026
Green Better
1,008,600
1.72%
0.09%
October 22, 2026
Hongxing International
1,008,600
1.72%
0.09%
October 22, 2026
Ingenic Semiconductor HK
1,008,600
1.72%
0.09%
October 22, 2026
Awinic Technology Limited
1,008,600
1.72%
0.09%
October 22, 2026

<<<PAGE 15>>>
15
Name
Number of 
shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 1
% of total issued 
share capital in 
the Company 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject to the 
lock-up undertakings 
Note 2
JinYi Capital (acting for and on 
behalf of Structured Credit SP 
Fund)
201,700
0.34%
0.02%
October 22, 2026
Total
29,250,100
49.96%
2.72%
Notes:
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
2. 
In accordance with the relevant cornerstone investment agreement, the required lock-up period ends on 
October 22, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or transferring H 
Shares subscribed pursuant to the relevant cornerstone investment agreement after the indicated date.
PLACEE CONCENTRATION ANALYSIS
Placees*
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
Option 
is fully 
exercised)
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
Option 
is fully 
exercised)
Number of 
H Shares 
held upon 
Listing
% of total 
issued 
H share 
capital upon 
Listing 
(assuming 
no exercise 
of the Over-
allotment 
Option)
% of total 
issued 
H share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
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
Option 
is fully 
exercised)
Top 1
8,270,900 
15.6963%
13.4540%
14.1267%
12.2840%
 8,270,900 
14.1267%
12.2840%
0.7699%
0.7637%
Top 5
19,870,200 
37.7092%
32.3221%
33.9382%
29.5115%
 19,870,200 
33.9382%
29.5115%
1.8496%
1.8346%
Top 10
30,763,300 
58.3818%
50.0416%
52.5435%
45.6901%
 30,763,300 
52.5435%
45.6901%
2.8636%
2.8404%
Top 25
46,396,600
88.0503%
75.4717%
79.2451%
68.9088%
46,396,600
79.2451%
68.9088%
4.3189%
4.2838%
* 
Ranking of placees is based on the number of Offer Shares allotted to the placees.

<<<PAGE 16>>>
16
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
allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
Allotment 
as % of 
total Offer 
Shares 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Allotment 
as % of 
total Offer 
Shares 
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
% of total 
issued 
H share 
capital upon 
Listing 
(assuming 
no exercise 
of the Over-
allotment 
Option)
% of total 
issued 
H share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
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
Option 
is fully 
exercised)
Top 1
8,270,900 
15.6963%
13.4540%
14.1267%
12.2840%
8,270,900 
14.1267%
12.2840%
0.7699%
0.7637%
Top 5
19,870,200 
37.7092%
32.3221%
33.9382%
29.5115%
19,870,200 
33.9382%
29.5115%
1.8496%
1.8346%
Top 10
30,763,300 
58.3818%
50.0416%
52.5435%
45.6901%
30,763,300 
52.5435%
45.6901%
2.8636%
2.8404%
Top 25
46,396,600
88.0503%
75.4717%
79.2451%
68.9088%
46,396,600
79.2451%
68.9088%
4.3189%
4.2838%
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholder upon Listing.
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
allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option is fully 
exercised)
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
Option is fully 
exercised)
Number of H 
Shares held 
upon Listing
Number of 
Shares held 
upon Listing#
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
Option is fully 
exercised)
Top 1
–
0.0000%
0.0000%
0.0000%
0.0000%
– 
440,515,043 
41.0056%
40.6731%
Top 5
–
0.0000%
0.0000%
0.0000%
0.0000%
–
685,068,283 
63.7700%
63.2529%
Top 10
8,270,900 
15.6963%
13.4540%
14.1267%
12.2840%
8,270,900 
800,770,299 
74.5401%
73.9357%
Top 25
28,746,000 
54.5534%
46.7601%
49.0980%
42.6939%
28,746,000 
847,560,562 
78.8956%
78.2559%
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.
# 
Among the top 25 placees, certain placees are also existing Shareholders. To the best knowledge, information 
and belief of the Company after due enquiry, details of the allocations to the Existing Minority Shareholders 
holding more than 1% of the issued share capital of the Company immediately prior to the completion of the 
Global Offering have been disclosed in this announcement.

<<<PAGE 17>>>
17
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 140,150 valid 
applications made by the public will be conditionally allocated on the basis set out below:
BASIS OF ALLOTMENT UNDER THE HONG KONG PUBLIC OFFERING
Pool A
Number
of H Shares
applied for
Number
of valid
applications
Basis of allocation/ballot
Approximate 
percentage 
allotted of 
the total 
number of 
H Shares 
applied for
100
45,182
5,422 out of 45,182 applicants to receive 100 H Shares
12.00%
200
11,686
1,693 out of 11,686 applicants to receive 100 H Shares
7.24%
300
7,167
1,159 out of 7,167 applicants to receive 100 H Shares
5.39%
400
4,704
823 out of 4,704 applicants to receive 100 H Shares
4.37%
500
6,229
1,157 out of 6,229 applicants to receive 100 H Shares
3.71%
600
4,420
863 out of 4,420 applicants to receive 100 H Shares
3.25%
700
1,311
267 out of 1,311 applicants to receive 100 H Shares
2.91%
800
1,122
237 out of 1,122 applicants to receive 100 H Shares
2.64%
900
857
187 out of 857 applicants to receive 100 H Shares
2.42%
1,000
7,412
1,661 out of 7,412 applicants to receive 100 H Shares
2.24%
1,500
2,908
728 out of 2,908 applicants to receive 100 H Shares
1.67%
2,000
2,366
640 out of 2,366 applicants to receive 100 H Shares
1.35%
2,500
1,786
514 out of 1,786 applicants to receive 100 H Shares
1.15%
3,000
1,491
450 out of 1,491 applicants to receive 100 H Shares
1.01%
3,500
971
306 out of 971 applicants to receive 100 H Shares
0.90%
4,000
1,099
359 out of 1,099 applicants to receive 100 H Shares
0.82%
4,500
831
280 out of 831 applicants to receive 100 H Shares
0.75%
5,000
1,960
680 out of 1,960 applicants to receive 100 H Shares
0.69%
6,000
1,505
549 out of 1,505 applicants to receive 100 H Shares
0.61%
7,000
1,081
411 out of 1,081 applicants to receive 100 H Shares
0.54%
8,000
1,110
438 out of 1,110 applicants to receive 100 H Shares
0.49%
9,000
775
316 out of 775 applicants to receive 100 H Shares
0.45%
10,000
5,854
2,449 out of 5,854 applicants to receive 100 H Shares
0.42%
20,000
3,734
1,886 out of 3,734 applicants to receive 100 H Shares
0.25%
30,000
2,357
1,329 out of 2,357 applicants to receive 100 H Shares
0.19%
40,000
1,763
1,075 out of 1,763 applicants to receive 100 H Shares
0.15%
50,000
1,904
1,233 out of 1,904 applicants to receive 100 H Shares
0.13%
60,000
3,180
2,163 out of 3,180 applicants to receive 100 H Shares
0.11%
Total
126,765
Total number of Pool A successful applicants: 29,275

<<<PAGE 18>>>
18
Pool B
Number
of H Shares
applied for
Number
of valid
applications
Basis of allocation/ballot
Approximate 
percentage 
allotted of 
the total 
number of 
H Shares 
applied for
70,000
3,570
100 H Shares plus 929 out of 3,570 applicants to receive an additional 
 100 H Shares
0.18%
80,000
1,445
100 H Shares plus 551 out of 1,445 applicants to receive an additional 
 100 H Shares
0.17%
90,000
819
100 H Shares plus 408 out of 819 applicants to receive an additional 
 100 H Shares
0.17%
100,000
3,929
100 H Shares plus 2,398 out of 3,929 applicants to receive an 
 additional 100 H Shares
0.16%
200,000
1,569
300 H Shares
0.15%
300,000
749
300 H Shares plus 675 out of 749 applicants to receive an additional 
 100 H Shares
0.13%
400,000
331
400 H Shares
0.10%
500,000
281
400 H Shares plus 202 out of 281 applicants to receive an additional 
 100 H Shares
0.09%
600,000
170
500 H Shares plus 63 out of 170 applicants to receive an additional 
 100 H Shares
0.09%
700,000
74
500 H Shares plus 45 out of 74 applicants to receive an additional 
 100 H Shares
0.08%
800,000
79
600 H Shares
0.08%
900,000
45
600 H Shares
0.07%
1,000,000
153
600 H Shares
0.06%
1,500,000
47
800 H Shares
0.05%
2,000,000
30
1,000 H Shares
0.05%
2,500,000
18
1,200 H Shares
0.05%
2,927,400
76
1,400 H Shares
0.05%
Total
13,385
Total number of Pool B successful applicants: 13,385
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 19>>>
19
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Allocations of Offer Shares to the existing Shareholders and/or their close associates and 
Cornerstone Investors with a consent under Chapter 4.15 of the Guide for New Listing 
Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 
of the Guide for New Listing Applicants to permit the Company to allocate further Offer Shares 
in the International Offering to certain Cornerstone Investors, existing shareholders and their close 
associates, as placees, subject to the following conditions (“Allocation to Size-based Exemption 
Participants”):
(a) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;
(b) 
the Offer Shares allocated to all existing Shareholders and their close associates (whether 
as cornerstone investors and/or as placees) as permitted under the Size-based Exemption (as 
defined in the Guide for New Listing Applicants) do not exceed 30% of the total number of 
the H Shares offered under the Global Offering;
(c) 
each Director and chief executive of the Company confirms that no securities have been 
allocated to them or their respective close associates under the Size-based Exemption; and
(d) 
details of the allocation to existing Shareholders and/or their close associates and Cornerstone 
Investors under the Size-based Exemption will be disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates 
and Cornerstone Investors, please refer to the section headed “Allotment Results Details – 
International Offering – Allottees with Waivers/Consents Obtained” in this announcement.

<<<PAGE 20>>>
20
Placing to connected clients with a prior consent under paragraph 1C of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines. Details of the placement to connected 
clients are set out below. The Company has applied to the Stock Exchange for, and the Stock 
Exchange has granted, consents under paragraph 1C(1) of the Placing Guidelines to permit the 
Company to allocate such Offer Shares in the International Offering to the connected clients. The 
allocation of Offer Shares to such connected clients is in compliance with all the conditions under 
the consent granted by the Stock Exchange.
No.
Connected 
Distributor
Connected Client
Relationship
Discretionary or 
non-discretionary
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
Number of Offer 
Shares to be 
allocated to the 
Connected Client
Approximate 
percentage of 
total number 
of Offer Shares 
under the Global 
Offering
1.
CICCHKS
CICC FT (in 
connection with 
Beijing Hengde 
OTC Swaps)
Same group entities
Non-discretionary
No
201,700
0.34%
2.
CICCHKS
CICC FT (in 
connection with 
Longyan Huasheng 
OTC Swaps)
Same group entities
Non-discretionary
No
504,300
0.86%
3.
CICCHKS
CICC FT (in 
connection with 
SWHY OTC 
Swaps)
Same group entities
Non-discretionary
No
201,700
0.34%
4.
CICCHKS
CICC FT (in 
connection with 
Gaoyi OTC Swaps)
Same group entities
Non-discretionary
No
286,600
0.49%
5.
CICCHKS
CICC FT (in 
connection with 
Yuanlesheng OTC 
Swaps)
Same group entities
Non-discretionary
No
50,400
0.09%
6.
GTJA 
Securities
GTJA Investments
Same group entities
Non-discretionary
No
348,100
0.59%
Haitong 
Securities

<<<PAGE 21>>>
21
No.
Connected 
Distributor
Connected Client
Relationship
Discretionary or 
non-discretionary
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
Number of Offer 
Shares to be 
allocated to the 
Connected Client
Approximate 
percentage of 
total number 
of Offer Shares 
under the Global 
Offering
7.
UBS AG
UBS AM 
Singapore
UBS AG and UBS 
AM Singapore are 
members of the same 
group
Discretionary
No
2,017,200
3.44%
8.
GTJA 
Securities
Fullgoal HK
Fullgoal HK, Fullgoal 
Fund, Haitong 
Securities and 
GTJA Securities are 
members of the same 
group
Discretionary
Yes
200,000
0.34%
Haitong 
Securities
Fullgoal Fund
Discretionary
Yes
606,900
1.04%
9.
HSBC
HSBC Broking
HSBC, HSBC GAM 
and HSBC Broking 
are members of the 
same group
Discretionary
No
253,200
0.43%
HSBC GAM
Discretionary
No
806,900
1.38%
10.
GTJA 
Securities
HuaAn Fund
HuaAn Fund, Haitong 
Securities and 
GTJA Securities are 
members of the same 
group
Discretionary
No
10,000
0.02%
Haitong 
Securities
11.
CLSA
CITIC-Prudential 
Fund
CITIC-Prudential 
Fund and CLSA are 
members of the same 
group
Discretionary
No
151,200
0.26% 

<<<PAGE 22>>>
22
Note:
1. 
CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one 
OTC swap transactions (the “Beijing Hengde OTC Swaps”) with each other and the ultimate clients (the 
“CICC FT Ultimate Clients (Beijing Hengde)”), pursuant to which CICC FT will hold the Offer Shares on a 
non-discretionary basis to hedge the Beijing Hengde OTC Swaps while the economic risks and returns of the 
underlying Offer Shares are passed to the CICC FT Ultimate Clients (Beijing Hengde), subject to customary 
fees and commissions. The Beijing Hengde OTC Swaps will be fully funded by the CICC FT Ultimate Clients 
(Beijing Hengde). During the terms of the Beijing Hengde OTC Swaps, all economic returns of the Offer Shares 
subscribed by CICC FT will be passed to the CICC FT Ultimate Clients (Beijing Hengde) and all economic loss 
shall be borne by the CICC FT Ultimate Clients (Beijing Hengde) through the Beijing Hengde OTC Swaps, and 
CICC FT will not take part in any economic return or bear any economic loss in relation to the Offer Shares. 
The Beijing Hengde OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate Clients (Beijing 
Hengde) may request CICC FT to redeem it at their own discretions, upon which CICC FT shall dispose of 
the Offer Shares and settle Beijing Hengde OTC Swaps in cash in accordance with the terms and conditions of 
the OTC Swap. Despite that CICC FT will hold the legal title of the Offer Shares by itself, it will not exercise 
the voting rights attaching to the relevant Offer Shares during the terms of the Beijing Hengde OTC Swaps 
according to its internal policy. The CICC FT Ultimate Clients (Beijing Hengde) for purpose of this placee 
subscription include Hengde Yuanzheng Tianli No. 3 Private Equity Securities Investment Fund (恒德遠征添
利 3 號私募證券投資基金), Hengde Yuanzheng Tianli No. 7 Private Equity Securities Investment Fund (恒德
遠征添利 7 號私募證券投資基金), Hengde Yuanzheng Jinxin No. 4 Private Equity Securities Investment Fund 
(恒德遠征金信 4 號私募證券投資基金) and Hengde Jinze No. E49 Private Equity Securities Investment Fund 
(恒德金澤 E49 號私募證券投資基金) (collectively, “Hengde Funds”), which are managed by Beijing Hengde 
Era Fund Management Co. Ltd (北京恒德時代私募基金管理有限公司) (“Beijing Hengde”), each of which is 
an independent third party of CICC FT, CICCHKS and the companies which are members of the same group of 
companies as each of the Underwriters.
2. 
CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one 
OTC swap transactions (the “Longyan Huasheng OTC Swaps”) with each other and the ultimate client (the 
“CICC FT Ultimate Client (Longyan Huasheng)”), pursuant to which CICC FT will hold the Offer Shares 
on a non-discretionary basis to hedge the Longyan Huasheng OTC Swaps while the economic risks and returns 
of the underlying Offer Shares are passed to the CICC FT Ultimate Client (Longyan Huasheng), subject to 
customary fees and commissions. The Longyan Huasheng OTC Swaps will be fully funded by the CICC FT 
Ultimate Client (Longyan Huasheng). During the terms of the Longyan Huasheng OTC Swaps, all economic 
returns of the Offer Shares subscribed by CICC FT will be passed to the CICC FT Ultimate Client (Longyan 
Huasheng) and all economic loss shall be borne by the CICC FT Ultimate Client (Longyan Huasheng) through 
the Longyan Huasheng OTC Swaps, and CICC FT will not take part in any economic return or bear any 
economic loss in relation to the Offer Shares. The Longyan Huasheng OTC Swaps are linked to the Offer 
Shares and the CICC FT Ultimate Client (Longyan Huasheng) may request CICC FT to redeem it at their own 
discretions, upon which CICC FT shall dispose of the Offer Shares and settle Longyan Huasheng OTC Swaps 
in cash in accordance with the terms and conditions of the OTC Swap. Despite that CICC FT will hold the legal 
title of the Offer Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares 
during the terms of the Longyan Huasheng OTC Swaps according to its internal policy. The CICC FT Ultimate 
Client (Longyan Huasheng) for purpose of this placee subscription is Longyan Huasheng Enterprise Investment 
Co., Ltd. (龍岩市華盛企業投資有限公司), a wholly owned subsidiary of Longyan Investment Development 
Group Co., Ltd. (龍岩投資發展集團有限公司) (“Longyan Investment”), which is an independent third party 
of CICC FT, CICCHKS and the companies which are members of the same group of companies as each of the 
Underwriters.
3. 
CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one 
OTC swap transactions (the “SWHY OTC Swaps”) with each other and the ultimate client (the “CICC FT 
Ultimate Client (SWHY)”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis 
to hedge the SWHY OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed 
to the CICC FT Ultimate Client (SWHY), subject to customary fees and commissions. The SWHY OTC Swaps 
will be fully funded by the CICC FT Ultimate Client (SWHY). During the terms of the SWHY OTC Swaps, all 
economic returns of the Offer Shares subscribed by CICC FT will be passed to the CICC FT Ultimate Client 
(SWHY) and all economic loss shall be borne by the CICC FT Ultimate Client (SWHY) through the SWHY 
OTC Swaps, and CICC FT will not take part in any economic return or bear any economic loss in relation to the 
Offer Shares. The SWHY OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate Client (SWHY) 
may request CICC FT to redeem it at their own discretions, upon which CICC FT shall dispose of the Offer 

<<<PAGE 23>>>
23
Shares and settle SWHY OTC Swaps in cash in accordance with the terms and conditions of the SWHY OTC 
Swap. Despite that CICC FT will hold the legal title of the Offer Shares by itself, it will not exercise the voting 
rights attaching to the relevant Offer Shares during the terms of the SWHY OTC Swaps according to its internal 
policy. The CICC FT Ultimate Client (SWHY) for purpose of this placee subscription is Shenwan Hongyuan 
Securities Co., Ltd. (申萬宏源證券有限公司), a wholly owned subsidiary of Shenwan Hongyuan Group Co., 
Ltd. (申萬宏源集團股份有限公司) (“Shenwan Hongyuan”) (000166.SZ; 6806.HK), which is an independent 
third party of CICC FT, CICCHKS and the companies which are members of the same group of companies as 
each of the Underwriters.
4. 
CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one 
OTC swap transactions (the “Gaoyi OTC Swaps”) with each other and the ultimate clients (the “CICC FT 
Ultimate Clients (Gaoyi)”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis 
to hedge the Gaoyi OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed 
to the CICC FT Ultimate Clients (Gaoyi), subject to customary fees and commissions. The Gaoyi OTC Swaps 
will be fully funded by the CICC FT Ultimate Clients (Gaoyi). During the terms of the Gaoyi OTC Swaps, all 
economic returns of the Offer Shares subscribed by CICC FT will be passed to the CICC FT Ultimate Clients 
(Gaoyi) and all economic loss shall be borne by the CICC FT Ultimate Clients (Gaoyi) through the Gaoyi OTC 
Swaps, and CICC FT will not take part in any economic return or bear any economic loss in relation to the 
Offer Shares. The Gaoyi OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate Clients (Gaoyi) 
may request CICC FT to redeem it at their own discretions, upon which CICC FT shall dispose of the Offer 
Shares and settle Gaoyi OTC Swaps in cash in accordance with the terms and conditions of the Gaoyi OTC 
Swaps. Despite that CICC FT will hold the legal title of the Offer Shares by itself, it will not exercise the voting 
rights attaching to the relevant Offer Shares during the terms of the Gaoyi OTC Swaps according to its internal 
policy. The CICC FT Ultimate Clients (Gaoyi) for purpose of this placee subscription are funds managed by 
Shanghai Gaoyi Asset Management Partnership (Limited Partnership) (上海高毅資產管理合夥企業(有限合
夥)) (“Shanghai Gaoyi”). Shanghai Gaoyi is a limited partnership established in the PRC, which is engaged in 
asset management and investment management with a primary focus on investments in secondary market. The 
managing partner of Shanghai Gaoyi is Shanghai Gaoyi Investment Management Co., Ltd. (上海高毅投資管理
有限公司). Each of the CICC FT Ultimate Clients (Gaoyi) is an independent third party of CICC FT, CICCHKS 
and the companies which are members of the same group of companies as each of the Underwriters.
5. 
CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one 
OTC swap transactions (the “Yuanlesheng OTC Swaps”) with each other and the ultimate clients (the 
“CICC FT Ultimate Clients (Yuanlesheng)”), pursuant to which CICC FT will hold the Offer Shares on a 
non-discretionary basis to hedge the Yuanlesheng OTC Swaps while the economic risks and returns of the 
underlying Offer Shares are passed to the CICC FT Ultimate Clients (Yuanlesheng), subject to customary 
fees and commissions. The Yuanlesheng OTC Swaps will be fully funded by the CICC FT Ultimate Clients 
(Yuanlesheng). During the terms of the Yuanlesheng OTC Swaps, all economic returns of the Offer Shares 
subscribed by CICC FT will be passed to the CICC FT Ultimate Clients (Yuanlesheng) and all economic loss 
shall be borne by the CICC FT Ultimate Clients (Yuanlesheng) through the Yuanlesheng OTC Swaps, and 
CICC FT will not take part in any economic return or bear any economic loss in relation to the Offer Shares. 
The Yuanlesheng OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate Clients (Yuanlesheng) 
may request CICC FT to redeem it at their own discretions, upon which CICC FT shall dispose of the Offer 
Shares and settle Yuanlesheng OTC Swaps in cash in accordance with the terms and conditions of the 
Yuanlesheng OTC Swaps. Despite that CICC FT will hold the legal title of the Offer Shares by itself, it will 
not exercise the voting rights attaching to the relevant Offer Shares during the terms of the Yuanlesheng OTC 
Swaps according to its internal policy. The CICC FT Ultimate Clients (Yuanlesheng) for purpose of this placee 
subscription include Yuanlesheng Qiangye Private Securities Investment Fund (源樂晟強業私募證券投資基
金) and Yuanlesheng Qiangshu Private Securities Investment Fund (源樂晟強樹私募證券投資基金), which are 
funds managed by Tibet Yuanlesheng Asset Management Company Limited (西藏源樂晟資產管理有限公司) 
(“Yuanlesheng AM”), each of which is an independent third party of CICC FT, CICCHKS and the companies 
which are members of the same group of companies as each of the Underwriters.

<<<PAGE 24>>>
24
6. 
In relation to the GTJA Investments’ Subscription, GTJA Investments shall hold the Offer Shares for hedging 
purpose as the single underlying asset of several sets of back-to-back total return swap transaction (the “GTHT 
Back-to-back TRS”) to be entered into between GTJA Investments and Guotai Haitong Securities Co., Ltd. (the 
“GTHT Onshore Parent”) in connection with several total return swap orders (the “GTHT Client TRS”) to 
be entered into by GTHT Onshore Parent and several ultimate clients (the “GTHT Onshore Ultimate Client”), 
respectively. Such GTHT Client TRS is to be fully funded by the GTHT Onshore Ultimate Client. GTJA 
Investments will hold the Offer Shares on a non-discretionary basis for the purpose of hedging the economic 
exposure under the GTHT Back-to-back TRS and GTHT Client TRS only, During the tenor of the GTHT Client 
TRS, all economic returns of the Offer Shares will be passed to the GTHT Onshore Ultimate Clients and all 
economic losses shall be borne by the GTHT Onshore Ultimate Client, subject to the terms and conditions of 
the GTHT Back-to-back TRS and GTHT Client TRS, and GTJA Investments will not take part in any economic 
return or bear any economic loss in relation to the price of the Offer Shares. The GTHT Onshore Ultimate Client 
may request to redeem the Offer Shares at their own discretion, upon which GTJA Investments shall dispose 
of the Offer Shares and settle the GTHT Back-to-back TRS and GTHT Client TRS in cash in accordance with 
the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS documents. Due to its internal 
policy, GTJA Investments will not exercise the voting right attaching to the Offer Shares during the tenor of the 
GTHT Back-to-back TRS and GTHT Client TRS.
To the best knowledge, information and belief of GTJA Investments after due enquiry, the GTHT Onshore 
Ultimate Clients and their respective ultimate beneficial owners holding 30% or more interest include:
a. 
The GTHT Onshore Ultimate Client (Jedi) for purpose of this placee subscription is Jedi Yuanyang No.6 
Private Securities Investment Fund (金淡遠洋 6 號私募證券投資基金), which is managed by Jedi Asset 
Management, LLC (上海金淡資產管理有限公司) (“Jedi AM”), each of which is an independent third 
party of GTJA Investments, GTJA Securities and the companies which are members of the same group of 
companies as each of the Underwriters;
b. 
The GTHT Onshore Ultimate Client (TSINGSTONE ASSET) for purpose of this placee subscription 
is TSINGSTONE ASSET MANAGEMENT GROUP LIMITED (清石資產管理(上海)有限公司) 
(“TSINGSTONE ASSET”), which is an independent third party of GTJA Investments, GTJA Securities 
and the companies which are members of the same group of companies as each of the Underwriters; and
c. 
The GTHT Onshore Ultimate Client (Shanghai Milestone) for purpose of this placee subscription is 
Lichen Scenery No. 66 Private Investment Fund (理成風景 66 號私募投資基金), which is managed by 
Shanghai Milestone Asset Management Co., Ltd. (上海理成資產管理有限公司) (“Shanghai Milestone”), 
each of which is an independent third party of GTJA Investments, GTJA Securities and the companies 
which are members of the same group of companies as each of the Underwriters.
7. 
UBS AG becomes a sub-broker under the International Offering during the application period. UBS AM 
Singapore is a member of the same group of companies as UBS AG. As a result, UBS AM Singapore is a 
connected client of UBS AG. UBS AM Singapore proposes to participate as placee to subscribe for the Offer 
Shares for and on behalf of its underlying client under the International Offering. UBS AM Singapore is a 
wholly owned subsidiary of UBS Asset Management AG, an investment management company, which is wholly 
ultimately owned by UBS Group AG, which is a company organised under Swiss law as a corporation that has 
issued shares of common stock to investors. UBS Group AG’s shares are listed on the SIX Swiss Exchange 
(stock code: UBSG) and the New York Stock Exchange (stock code: UBS).
The number of Offer Shares allocated to UBS AM Singapore comprises Offer Shares allocated to UBS AM 
Singapore in its capacity as a Cornerstone Investor and as a placee.
UBS AM Singapore will hold the Offer Shares in its capacity as discretionary investment manager managing 
assets on behalf of its underlying clients. The subscription will be fully funded by the personal assets of the 
underlying client. To the best knowledge of UBS AM Singapore after due enquiry, each of its underlying clients 
is an independent third party of the Company, its subsidiaries, UBS AM Singapore, UBS AG and the companies 
which are members of the same group of UBS AG and UBS AM Singapore.

<<<PAGE 25>>>
25
8. 
Fullgoal HK is a wholly owned subsidiary of Fullgoal Fund, which is owned by Guotai Haitong as to 27.775%. 
Each of GTJA Securities and Haitong Securities is a subsidiary of Guotai Haitong. Each of Fullgoal HK and 
Fullgoal Fund is considered as a member of the same group of companies as GTJA Securities and Haitong 
Securities and therefore is a connected client of GTJA Securities and Haitong Securities.
Fullgoal HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds 
on behalf of their investors (the “Fullgoal HK Ultimate Clients”), each of which is, to the best knowledge 
of Fullgoal HK, (i) an independent third party of the Company, its subsidiaries, its substantial shareholders, 
Fullgoal HK, GTJA Securities, Haitong Securities and the companies which are members of the same group 
of companies as Fullgoal HK, GTJA Securities and Haitong Securities; and (ii) Fullgoal China Small-Mid Cap 
Growth Fund, a collective investment scheme which is not authorized by the SFC. Save as disclosed below, no 
ultimate beneficial owner holds 30% or more interest in the funds.
The details of the Fullgoal HK Ultimate Clients are as follow:
Fund Name
Whether the Scheme 
is Publicly Marketed
Fund Manager
UBO of Fund 
Manager
UBO of the Fullgoal 
HK Ultimate Clients
The University of Hong Kong-
Hong Kong and China Equity 
Fund
Not publicly marketed
Fullgoal HK
Fullgoal Fund
The ultimate 
beneficial owner is 
“The University of 
Hong Kong”
Fullgoal China Growth Select 
Fund
Not publicly marketed
Fullgoal HK
Fullgoal Fund
The ultimate 
beneficial owner is an 
individual
Fullgoal China Opportunities Fund
Not publicly marketed
Fullgoal HK
Fullgoal Fund
The ultimate 
beneficial owners are 
three investors which 
are entities and funds
Fullgoal China Small-Mid Cap 
Growth Fund
Yes
Fullgoal HK
Fullgoal Fund
No single ultimate 
beneficial owner 
holds 30% or more 
interest
HI-Aktien China 1-SFonds
Not publicly marketed
Fullgoal HK
Fullgoal Fund
The ultimate 
beneficial owner is an 
European pension
BMO Greater China Fund
Yes
Fullgoal HK
Fullgoal Fund
No single ultimate 
beneficial owner 
holds 30% or more 
interest
Fullgoal Fund will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds 
on behalf of their investors (the “Fullgoal Fund Ultimate Clients”), each of which is, to the best knowledge 
of Fullgoal Fund, (i) an independent third party of the Company, its subsidiaries, its substantial shareholders, 
Fullgoal Fund, GTJA Securities, Haitong Securities and the companies which are members of the same group of 
companies as GTJA Securities, Haitong Securities and Fullgoal Fund; and (ii) a collective investment scheme 
which is not authorized by the SFC. No ultimate beneficial owner holds 30% or more interest in the funds.

<<<PAGE 26>>>
26
The details of the Fullgoal Fund Ultimate Clients are as follow:
Fund Name
Whether the Scheme 
is Publicly Marketed
Fund Manager
UBO of Fund 
Manager
UBO of the Fullgoal 
Fund Ultimate 
Clients
FULLGOAL DIVIDEND 
SELECTED HYBRID FUND
Yes
Fullgoal Fund
N/A
No single ultimate 
beneficial owner 
holds 30% or more 
interest
CMB-FULLGOAL BLUE CHIP 
SELECTED EQUITY FUND 
(QDII)
Yes
Fullgoal Fund
N/A
No single ultimate 
beneficial owner 
holds 30% or more 
interest
ICBC Fullgoal global technology 
& internet fund
Yes
Fullgoal Fund
N/A
No single ultimate 
beneficial owner 
holds 30% or more 
interest
Fullgoal Global Consumption 
Selected Hybrid Fund
Yes
Fullgoal Fund
N/A
No single ultimate 
beneficial owner 
holds 30% or more 
interest
ICBC Fullgoal China Small & Mid 
Cap (HK listed) Equity Fund
Yes
Fullgoal Fund
N/A
No single ultimate 
beneficial owner 
holds 30% or more 
interest
9. 
HSBC is a sub-broker under the International Offering. HSBC Broking will hold the Offer Shares in its capacity 
as the discretionary fund manager managing assets on behalf of its underlying clients. HSBC GAM will hold 
the Offer Shares in its capacity as the discretionary fund manager managing assets on behalf of its underlying 
clients. Each of HSBC Broking and HSBC GAM is a member of the same group of companies as HSBC. As a 
result, each of HSBC Broking and HSBC GAM is a connected client of HSBC. To the best knowledge of HSBC 
Broking and HSBC GAM after due enquiry, each of its underlying clients is an independent third party of the 
Company, its subsidiaries, HSBC, HSBC Broking, HSBC GAM and the companies which are members of the 
same group of HSBC, HSBC Broking and HSBC GAM
10. 
HuaAn Fund, Haitong Securities and GTJA Securities are members of the same group. Therefore, HuaAn Fund 
is a connected client of GTJA Securities and Haitong Securities.
11. 
CITIC-Prudential Fund will hold the Offer Shares in its capacity as the discretionary fund manager of Citic 
Prudential Global Macro-asset Allocation AMP 1. To the best knowledge of CITIC-Prudential Fund, none of the 
clients holds more than 30% ultimate beneficial interest in the relevant fund. CLSA and CITIC-Prudential Fund 
are members of the same group. Therefore, CITIC-Prudential Fund is a connected client of CLSA.

<<<PAGE 27>>>
27
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
The Offer Shares are being offered and sold solely (1) to qualified institutional buyers as defined 
in Rule 144A under the U.S. Securities Act pursuant to an exemption from registration under 
the U.S. Securities Act and (2) outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated April 15, 2026 issued by Huaqin Co., Ltd. 
for detailed information about the Global Offering described below before deciding whether or 
not to invest in the H Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-
Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) and the 
Overall Coordinators shall be entitled to terminate their obligations under the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set 
out in the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong 
Kong Public Offering – Hong Kong Underwriting Agreement – Grounds for Termination” in 
the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is 
currently expected to be on April 23, 2026).
PUBLIC FLOAT AND FREE FLOAT
Rule 8.08(1) (as amended and replaced by Rule 19A.13A) of the Listing Rules provides that, where 
a new applicant is a PRC issuer with other listed shares at the time of listing, this will normally 
mean that the portion of H shares for which listing is sought that are held by the public, at the time 
of listing, must (a) represent at least 10% of the issuer’s total number of issued shares in the class 
to which H shares belong (excluding treasury shares); or (b) have an expected market value of not 
less than HK$3,000,000,000. It is expected that upon Listing (assuming the Over-allotment Option 
is not exercised), based on the Offer Price of HK$77.70 per H Share, the market value of the H 
Shares that are held by the public is approximately HK$4,549.2 million, which is higher than the 
prescribed market value of the H Shares required to be held by the public of HK$3 billion under 
Rule 19A.13A(2) of the Listing Rules, thereby satisfying Rule 8.08(1) (as amended and replaced 
by Rule 19A.13A) of the Listing Rules.

<<<PAGE 28>>>
28
Rule 8.08A (as amended and replaced by Rule 19A.13C) of the Listing Rules provides that, where 
a new applicant is a PRC issuer with other listed shares at the time of listing, this will normally 
mean that the portion of H shares for which listing is sought that are held by the public and not 
subject to any disposal restrictions (whether under contract, the Listing Rules, applicable laws 
or otherwise), at the time of listing, must: (a) represent at least 5% of the total number of issued 
shares in the class to which H shares belong at the time of listing (excluding treasury shares), with 
an expected market value at the time of listing of not less than HK$50,000,000; or (b) have an 
expected market value at the time of listing of not less than HK$600,000,000. The Company will 
satisfy the free float requirement under Rule 8.08A (as amended and replaced by Rule 19A.13C) of 
the Listing Rules.
The Directors confirm that immediately after the completion of the Global Offering (assuming 
the Over-allotment Option is not exercised), (i) no placee will, individually, be placed more than 
10% of the enlarged issued share capital of the Company; (ii) there will not be any new substantial 
shareholder (as defined in the Listing Rules) of the Company; (iii) the three largest public 
shareholders of the Company do not hold more than 50% of the H Shares in public hands at the 
time of the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there 
will be at least 300 H Shareholders at the time of the Listing in compliance with Rule 8.08(2) of 
the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Thursday, April 
23, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting – Underwriting Arrangements 
and Expenses – Hong Kong Public Offering – Hong Kong Underwriting Agreement – Grounds for 
Termination” in the Prospectus has not been exercised. Investors who trade the H Shares on the 
basis of publicly available allocation details prior to the receipt of H Share certificates or prior to 
the H Share certificates becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Thursday, 
April 23, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Thursday, April 23, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 100 H Shares each, and the stock code of the H Shares will 
be 3296.
By order of the Board
Huaqin Co., Ltd.
QIU Wensheng
Chairman of the Board and Executive Director
Hong Kong, April 22, 2026
As at the date of this announcement, Directors of the Company are: (i) Mr. Qiu Wensheng, Mr. 
Cui Guopeng, Mr. Wu Zhenhai, Ms. Chen Xiaorong, Ms. Xi Pinghua and Mr. Deng Zhiguo as 
executive directors; and (ii) Mr. Hu Saixiong, Mr. Huang Zhiguo and Dr. Yu Fang as independent 
non-executive directors.
