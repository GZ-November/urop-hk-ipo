# 配发结果公告抽取任务：2476.HK Victory Giant Technology (HuiZhou) Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**20/04/2026 22:10**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0420/2026042001650.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2476.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”, 
or the “Hong Kong Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy or completeness and 
expressly disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated April 13, 2026 (the “Prospectus”) of Victory Giant Technology (HuiZhou) Co., 
Ltd. (勝宏科技(惠州)股份有限公司) (the “Company”). This announcement is made by the order of the board (the 
“Board”) of directors (the “Directors”) of the Company. The Board collectively and individually accept responsibility 
for the accuracy of this announcement.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for any securities. This announcement is not a prospectus. Potential investors should read the Prospectus 
for detailed information about the Global Offering described below before deciding whether or not to invest in 
the Offer Shares. Any investment decision in relation to the Offer Shares should be taken solely in reliance on the 
information provided in the Prospectus.
This announcement is not for release, publication or distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia or any other 
jurisdiction where such distribution is prohibited by laws). This announcement does not constitute or form a part of 
any offer or solicitation to purchase or subscribe for securities in the United States or in any other jurisdictions. The 
securities mentioned herein have not been, and will not be, registered under the United States Securities Act of 1933 
as amended from time to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the 
United States. The securities may not be offered, sold, pledged or otherwise transferred within the United States except 
pursuant to an exemption from the registration requirements of the U.S. Securities Act and in compliance with any 
applicable state securities laws, or outside the United States unless in compliance with Regulation S under the U.S. 
Securities Act. There will be no public offer of securities in the United States.
In connection with the Global Offering, J.P. Morgan Securities (Asia Pacific) Limited as stabilizing manager (the 
“Stabilizing Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, to the extent 
permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect 
transactions with a view to stabilizing or supporting the market price of the H Shares at such price, in such amounts 
and in such manners as the Stabilizing Manager, its affiliates or any person acting for it may determine and at a 
level higher than that which might otherwise prevail for a limited period after the Listing Date. However, there is 
no obligation on the Stabilizing Manager (or its affiliates or any person acting for it) to conduct any such stabilizing 
action. Such stabilizing action, if taken, (a) will be conducted at the absolute discretion of the Stabilizing Manager (or 
its affiliates or any person acting for it) and in what the Stabilizing Manager reasonably regards as the best interest 
of the Company, (b) may be discontinued at any time and (c) is required to be brought to an end within 30 days 
of the last day for lodging applications under the Hong Kong Public Offering (which is Saturday, May 16, 2026). 
Such Stabilizing action, if taken, may be effected in all jurisdictions where it is permissible to do so, in each case in 
compliance with all applicable laws, rules and regulatory requirements, including the Securities and Futures (Price 
Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures 
Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Saturday, May 16, 2026). 
After this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of 
the H Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to terms and conditions set out 
in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/
or not resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint Sponsors and the 
Sponsor-Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to 
terminate the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set 
out in the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – 
Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. on the Listing Date.

<<<PAGE 2>>>
2
Victory Giant Technology (HuiZhou) Co., Ltd.
勝宏科技( 惠州) 股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the 
Global Offering
:
95,850,000 H Shares (taking into account 
the full exercise of the Offer Size 
Adjustment Option and subject to the 
Over-allotment Option)
Number of Hong Kong Offer Shares
:
8,334,800 H Shares (including 482,000 
Overseas Employee Reserved Shares)
Number of International Offer Shares
:
87,515,200 H Shares (including 7,501,300 
PRC Employee Reserved Shares, taking 
into account the full exercise of the Offer 
Size Adjustment Option and subject to 
the Over-allotment Option)
Final Offer Price
:
HK$209.88 per H Share, plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
Stock Exchange trading fee of 0.00565% 
and AFRC transaction levy of 0.00015%
Nominal value
:
RMB1.00 per H Share
Stock code
:
2476
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators,
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and
Joint Lead Managers
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager

<<<PAGE 3>>>
3 
Victory Giant Technology (HuiZhou) Co., Ltd. / 勝宏科技（惠州）股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS 
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could move 
substantially even with a small number of the H Shares traded and should exercise extreme caution 
when dealing in the H Shares.
SUMMARY 
Company information 
Stock code  
2476
Stock short name  
VGT
Dealings commencement date 
April 21, 2026*
*see note at the end of the announcement 
Price Information  
Final Offer Price 
HK$209.88
Maximum Offer Price 
HK$209.88
Offer Shares and Share Capital 
Number of Offer Shares (after taking into account the full 
exercise of the Offer Size Adjustment Option) 
95,850,000 
Final Number of Offer Shares in Hong Kong Public Offering 
Note 1
8,334,800 
Final Number of Offer Shares in International Offering 
(after taking into account the full exercise of the Offer Size 
Adjustment Option) Note 2
87,515,200 
Number of issued Shares upon Listing (before exercise of the 
Over-allotment Option) Note 3
968,407,313 
Notes: 
1. Including 482,000 Overseas Employee Reserved Shares under the Overseas Employee Preferential 
Offering.  
2. Including 7,501,300 PRC Employee Reserved Shares under the PRC Employee Preferential Offering. 
3. Including 217,443 A Shares held by the Company as treasury shares. 
Offer Size Adjustment Option (Upsize option) 
Number of additional shares issued under the option 
12,502,000
-
Hong Kong Public Offering 
N/A
-
International Offering 
12,502,000
The Offer Size Adjustment Option has been exercised in full by the Sponsor-Overall Coordinators, 
pursuant to which the Company is issuing and allotting 12,502,000 additional Offer Shares, representing 
approximately 15.00% of the total number of Offer Shares initially available under the Global Offering, 
at the final Offer Price.
Over-allocation 

<<<PAGE 4>>>
4 
No. of Offer Shares over-allocated 
14,377,500
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases 
in the secondary market at prices that do not exceed the Offer Price or through deferred delivery or a 
combination of these means. In the event the Over-allotment Option is exercised, an announcement will 
be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)  
HK$20,117.00 million
Less: Estimated listing expenses payable based on final 
Offer Price  
HK$227.60 million 
Net proceeds  
HK$19,889.40 million
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use 
of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Offer Size Adjustment Option 
and the Over-allotment Option (if any) for the purposes as set out in the section headed “Future Plans and 
Use of Proceeds” of the Prospectus on a pro rata basis. 
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING (Excluding the Overseas Employee Preferential Offering) 
No. of valid applications  
250,606
No. of successful applications  
57,137
Subscription level 
431.15 times
Claw-back triggered  
N/A
No. of Offer Shares excluded Overseas Employee Reserved Shares 
initially available under the Hong Kong Public Offering 
7,501,400 
Final no. of Offer Shares excluded Overseas Employee Reserved 
Shares under the Hong Kong Public Offering (after reallocation 
from Overseas Employee Preferential Offering) 
7,852,800 
% of Offer Shares excluded Overseas Employee Reserved Shares 
under the Hong Kong Public Offering to the Global Offering (after 
taking into account the full exercise of the Offer Size Adjustment 
Option) 
8.19% 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.eipo.com.hk/eIPOAllotment 
to 
perform 
a 
search 
by 
identification 
number 
or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees. 
Overseas Employee Preferential Offering 
No. of valid applications  
46
Subscription level 
0.58 times
No. of Overseas Employee Reserved Shares initially available under 
the Overseas Employee Preferential Offering 
833,400 
Final no. of Overseas Employee Reserved Shares under the 
Overseas Employee Preferential Offering 
482,000 

<<<PAGE 5>>>
5 
Under-subscription of Overseas Employee Reserved Shares and 
made available to the Hong Kong Public Offering 
351,400 
Note: The 351,400 under-subscribed Overseas Employee Reserved Shares were reallocated to the Hong Kong 
Public Offering for subscription by the public in Hong Kong. For details of the final allocation of shares to 
the 
Overseas 
Employee 
Preferential 
Offering, 
Overseas 
Eligible 
Employees 
can 
refer 
to 
www.eipo.com.hk/eIPOAllotment 
to 
perform 
a 
search 
by 
identification 
number 
or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees. For details of the Overseas Employee Preferential 
Offering, please refer to the section headed “Structure of the Global Offering – The Overseas Employee 
Preferential Offering” of the Prospectus and the section headed “Others / Additional Information – 
Allocations under the Overseas Employee Preferential Offering” in this announcement. 
INTERNATIONAL OFFERING (Excluding the PRC Employee Preferential Offering) 
No. of placees (excluding the PRC Employee Preferential Offering)
341
Subscription level (excluding the PRC Employee Reserved Shares 
under the PRC Employee Preferential Offering) 
18.5 times 
No. of Offer Shares initially available under the International 
Offering (excluding the PRC Employee Reserved Shares under the 
PRC Employee Preferential Offering) 
67,511,900 
Final no. of Offer Shares under the International Offering 
(excluding the PRC Employee Reserved Shares under the PRC 
Employee Preferential Offering and after taking into account the 
full exercise of the Offer Size Adjustment Option) 
80,013,900 
% of Offer Shares under the International Offering to the Global 
Offering (excluding the PRC Employee Reserved Shares under the 
PRC Employee Preferential Offering and after taking into account 
the full exercise of the Offer Size Adjustment Option) 
83.48% 
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a waiver from 
strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) of Appendix F1 
to the Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange to permit H Shares in the 
International Offering to be placed to certain Existing Minority Shareholders and/or their close associates; 
(b) a consent under Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to, among 
other things, allocate further H Shares in the International Offering to certain existing Shareholders and 
Cornerstone Investors and/or their respective close associates; and (c) a waiver from strict compliance with 
Rules 10.03, 10.04 and 9.09(b) of the Listing Rules and a consent under paragraph 1C(2) of the Placing 
Guidelines granted by the Stock Exchange to permit the Company to allocate certain Offer Shares to the 
Eligible Core Connected Person Participants on a preferential basis under the PRC Employee Preferential 
Offering, (i) none of the Offer Shares subscribed by the placees and the public have been financed directly or 
indirectly by the Company, any of the Directors, chief executive of the Company, the Largest Group of 
Shareholders, substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or 
their respective close associates; and (ii) none of the placees and the public who have purchased the Offer 
Shares are accustomed to taking instructions from the Company, any of the Directors, chief executive of the 
Company, the Largest Group of Shareholders, substantial Shareholders, existing Shareholders of the Company 
or any of its subsidiaries or their respective close associates in relation to the acquisition, disposal, voting or 
other disposition of the H Shares registered in his/her/its name or otherwise held by him/her/it. 
PRC Employee Preferential Offering 

<<<PAGE 6>>>
6 
No. of valid applications  
1*
Subscription level 
1.00 time
No. of PRC Employee Reserved Shares initially available under the 
PRC Employee Preferential Offering 
7,501,300 
Final no. of PRC Employee Reserved Shares under the PRC 
Employee Preferential Offering 
7,501,300 
* The number of PRC Eligible Employees participated in the PRC Employee Preferential Offering is 145. 
For details of the PRC Employee Preferential Offering, please refer to the section headed “Structure of the 
Global Offering – The PRC Employee Preferential Offering” of the Prospectus and the section headed “Others 
/ Additional Information – Allocations under the PRC Employee Preferential Offering” in this announcement. 
The placees in the International Offering include the following: 
Cornerstone Investors
Investor 
No. of Offer 
Shares 
allocated 
% of H Shares 
(after 
taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(after taking into 
account 
the 
full 
exercise 
of 
the 
Offer 
Size 
Adjustment Option 
and assuming the 
Over-allotment 
Option 
is 
not 
exercised) 
Existing 
shareholders or 
their 
close 
associates Note 2
CPE Rosewood Investment 
Limited (“CPE Rosewood”)
2,800,700
2.92%
0.29%
No
Janchor Partners Pan-Asian 
Master Fund (“Janchor 
Fund”)
2,800,700
2.92%
0.29%
No
Yunfeng Capital
New Alternative Limited 
(“New Alternative”)
1,493,700
1.56%
0.15%
No
New Golden Future Limited
746,800
0.78%
0.08%
No
Deliante Holdings Co., Ltd. 
(“Deliante”)
1,979,200
2.06%
0.20%
No
Hong Kong Mason 
Electronics Co., Ltd. (香港麥
遜電子有限公司) (“Hong 
Kong Mason”)
1,867,100
1.95%
0.19%
No
Morgan Stanley & Co. 
International plc (“MSIP”)
1,307,000
1.36%
0.13%
Yes
Foresight Global Superior 
Choice SPC – Global Superior 
Choice Fund 1 SP, Foresight 
1,120,300
1.17%
0.12%
Yes

<<<PAGE 7>>>
7 
Investor 
No. of Offer 
Shares 
allocated 
% of H Shares 
(after 
taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(after taking into 
account 
the 
full 
exercise 
of 
the 
Offer 
Size 
Adjustment Option 
and assuming the 
Over-allotment 
Option 
is 
not 
exercised) 
Existing 
shareholders or 
their 
close 
associates Note 2
Global Superior Choice SPC – 
Vision Fund 1 SP, and 
Foresight Global Superior 
Choice SPC – Horizon Fund 1 
SP (“Foresight”)
HHLR Advisors, Ltd. 
(“HHLRA”)
1,120,300
1.17%
0.12%
No
Pinpoint Asset Management 
Limited (“Pinpoint”)
1,120,300
1.17%
0.12%
Yes
Sunshine Life Insurance 
Corporation Limited 
(“Sunshine Life”)
1,120,300
1.17%
0.12%
Yes
Tanwan Inc. (“Tanwan”)
1,120,300
1.17%
0.12%
No
Tropical Terrain Limited
1,120,300
1.17%
0.12%
No
Yong Rong (HK) Asset 
Management Limited (涌容
(香港)資產管理有限公司) 
(“YR Asset Management”)
1,120,300
1.17%
0.12%
No
Huizhou Huilian Investment 
Partnership (Limited 
Partnership) (惠州市惠聯投
資合夥企業(有限合夥)) 
(“Huizhou Huilian”)
1,073,500
1.12%
0.11%
No
Greenwoods Asset 
Management Hong Kong 
Limited (“HK Greenwoods”)
933,500
0.97%
0.10%
No
Bosera Asset Management 
(International) Co., Limited 
(“Bosera International”)
746,800
0.78%
0.08%
Yes
Cloudview Capital Limited 
(“Cloudview”)
746,800
0.78%
0.08%
No
CNCB (Hong Kong) 
Investment Limited (信銀(香
港)投資有限公司) (“CNCB 
Investment”)
746,800
0.78%
0.08%
No
Greater Bay Area Homeland Investments Limited (“GBAHIL”)
Mega Prime Development 
Limited (“Mega Prime”)
466,700
0.49%
0.05%
No

<<<PAGE 8>>>
8 
Investor 
No. of Offer 
Shares 
allocated 
% of H Shares 
(after 
taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(after taking into 
account 
the 
full 
exercise 
of 
the 
Offer 
Size 
Adjustment Option 
and assuming the 
Over-allotment 
Option 
is 
not 
exercised) 
Existing 
shareholders or 
their 
close 
associates Note 2
Poly Platinum Enterprises 
Limited (“Poly Platinum”)
280,000
0.29%
0.03%
No
Golden K2 Falcon Open-
ended Fund Company 
(“Golden K2 Falcon”)
746,800
0.78%
0.08%
No
Infore Funds Series 1 Open-
ended Fund Company 
(“Infore Capital”)
746,800
0.78%
0.08%
No
Metazone Link (HK) Limited 
(“Metazone”)
746,800
0.78%
0.08%
No
MY Asian Opportunities 
Master Fund, L.P. (“MY 
Asian”)
746,800
0.78%
0.08%
No
Ovata Capital Management 
Limited (“Ovata Capital”)
746,800
0.78%
0.08%
No
SR Wealth Securities Limited 
(“SR Wealth”)
746,800
0.78%
0.08%
No
Ruihua (International) 
Investment Limited (“Ruihua 
Investment”)
746,800
0.78%
0.08%
No
Tianhong Asset Management 
Co., Ltd. (天弘基金管理有限
公司) (“Tianhong Fund”) 
746,800
0.78%
0.08%
Yes
Ye Guofu (葉國富) 
746,800
0.78%
0.08%
No
CloudAlpha Capital 
Management Limited 
(“CloudAlpha Capital”)
560,100
0.58%
0.06%
No
Everbright Wealth 
Management Co., Ltd. 
(“Everbright Wealth 
Management”)
560,100
0.58%
0.06%
Yes
Jump Trading Pacific Pte. Ltd. 
(“Jump Trading”)
560,100
0.58%
0.06%
Yes
Luhua Daosheng (Beijing) 
Enterprise Management & 
Development Co., Ltd. (魯花
道生(北京)企業管理發展有
限公司) (“Luhua Daosheng”)
560,100
0.58%
0.06%
No

<<<PAGE 9>>>
9 
Investor 
No. of Offer 
Shares 
allocated 
% of H Shares 
(after 
taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(after taking into 
account 
the 
full 
exercise 
of 
the 
Offer 
Size 
Adjustment Option 
and assuming the 
Over-allotment 
Option 
is 
not 
exercised) 
Existing 
shareholders or 
their 
close 
associates Note 2
Mirae Asset Securities Co., 
Ltd. (“Mirae Asset”)
560,100
0.58%
0.06%
No
Panjing Harbourview 
Investment Fund (盤京港景投
資基金) (“Panjing Fund”) 
560,100
0.58%
0.06%
No
Wind Sabre Fund SPC 
(“WSOF”)
560,100
0.58%
0.06%
No
Black Dragon AP SPV1 
(“Black Dragon”)
373,400
0.39%
0.04%
No
HQ TELECOM SINGAPORE 
PTE. LTD. (“Huaqin 
Singapore”)
373,400
0.39%
0.04%
No
Total 
37,220,100 
38.83% 
3.84% 
Notes: 
1.
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the 
Global Offering.  
2.
In addition to the Offer Shares subscribed for as Cornerstone Investors, certain Cornerstone Investors and/or their close associates 
were allocated further Offer Shares as placees in the International Offering. Please refer to the section headed “Allotment Results 
Details – International Offering – Allottees with Waivers / Consents Obtained” in this announcement for details. Only the Offer 
Shares subscribed for as Cornerstone Investors are subject to lock-up restrictions as indicated below. For details, please refer to 
the section headed “Lock-up Undertakings – Cornerstone Investors” in this announcement.

<<<PAGE 10>>>
10 
Allottees with Waivers / Consents Obtained
Investor 
No. 
of 
Offer 
Shares 
allocated 
% of H Shares 
(after taking into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(after taking into 
account the full 
exercise 
of 
the 
Offer 
Size 
Adjustment Option 
and assuming the 
Over-allotment 
Option 
is 
not 
exercised) 
Relationship 
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by Existing Minority 
Shareholders holding more than 1% of the issued share capital of the Company immediately prior to the 
completion of the Global Offering and/or their close associates 
E Fund Management Co., 
Ltd. (“E Fund”) 
102,300 
0.11% 
0.01% 
E Fund also manages 
other fund products, 
each holding less than 
1% of the issued share 
capital but in 
aggregate holding 
more than 1% of the 
issued share capital of 
the Company. 
E Fund Management 
(Hong Kong) Co., Ltd. 
(“E Fund HK”) 
17,700 
0.02% 
0.002% 
E Fund HK is wholly 
owned by E Fund, 
which also manages 
other fund products, 
each holding less than 
1% of the issued share 
capital but in 
aggregate holding 
more than 1% of the 
issued share capital of 
the Company. 
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in 
relation to allocations of further H Shares to existing Shareholders and Cornerstone Investors and/or 
their close associates Note 2
Janchor Partners Limited 
2,800,700 
2.92% 
0.29% 
Close associate of 
Janchor Fund, one of 
the Cornerstone 
Investors 
New Golden Future 
Limited 
1,867,100 
1.95% 
0.19% 
Same entity as the 
Cornerstone Investor 
MSIP 
660,000 
0.69% 
0.07% 
Same entity as the 
Cornerstone Investor 

<<<PAGE 11>>>
11 
Investor 
No. 
of 
Offer 
Shares 
allocated 
% of H Shares 
(after taking into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(after taking into 
account the full 
exercise 
of 
the 
Offer 
Size 
Adjustment Option 
and assuming the 
Over-allotment 
Option 
is 
not 
exercised) 
Relationship 
Foresight Fund (Hong 
Kong) Limited 
500,000 
0.52% 
0.05% 
Close associate of 
Foresight, one of the 
Cornerstone Investors 
HHLRA 
522,800 
0.55% 
0.05% 
Same entity as the 
Cornerstone Investor 
Pinpoint 
522,800 
0.55% 
0.05% 
Same entity as the 
Cornerstone Investor 
Sunshine Life 
522,800 
0.55% 
0.05% 
Same entity as the 
Cornerstone Investor 
Boyu Capital 
Management (Singapore) 
Pte. Ltd. 
522,800 
0.55% 
0.05% 
Close associate of 
Tropical Terrain 
Limited, one of the 
Cornerstone Investors 
YR Asset Management 
522,800 
0.55% 
0.05% 
Same entity as the 
Cornerstone Investor 
HK Greenwoods 
396,600 
0.41% 
0.04% 
Same entity as the 
Cornerstone Investor 
Shanghai Greenwoods 
Asset Management Co., 
Ltd. (上海景林資產管理
有限公司, “Shanghai 
Greenwoods”) and 
Huatai Capital 
Investment Limited 
(“HTCI”) (in connection 
with the OTC swap) 
44,000 
0.05% 
0.005% 
Shanghai Greenwoods 
is a close associate of 
HK Greenwoods, one 
of the Cornerstone 
Investors 
Bosera International 
746,800 
0.78% 
0.08% 
Same entity as the 
Cornerstone Investor 
Cloudview 
351,000 
0.37% 
0.04% 
Same entity as the 
Cornerstone Investor 
CNCB Investment 
351,000 
0.37% 
0.04% 
Same entity as the 
Cornerstone Investor 
China Asset Management 
(Hong Kong) Limited 
120,000 
0.13% 
0.01% 
Close associate of 
CNCB Investment, 

<<<PAGE 12>>>
12 
Investor 
No. 
of 
Offer 
Shares 
allocated 
% of H Shares 
(after taking into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(after taking into 
account the full 
exercise 
of 
the 
Offer 
Size 
Adjustment Option 
and assuming the 
Over-allotment 
Option 
is 
not 
exercised) 
Relationship 
one of the Cornerstone 
Investors 
Mega Prime 
219,400 
0.23% 
0.02% 
Same entity as the 
Cornerstone Investor 
Poly Platinum 
131,600 
0.14% 
0.01% 
Same entity as the 
Cornerstone Investor 
Infore Capital 
133,600 
0.14% 
0.01% 
Same entity as the 
Cornerstone Investor 
Infore Capital 
Management Co., Ltd. 
(盈峰資本管理有限公
司, “Infore Capital 
Management”) and 
CITIC Securities Asset 
Management Company 
Limited (in connection 
with the OTC swap) 
70,000 
0.07% 
0.01% 
Infore Capital 
Management is a close 
associate of Infore 
Capital, one of the 
Cornerstone Investors 
Infore Capital 
Management and GF 
Global Capital Limited 
(“GFGC”) (in 
connection with the OTC 
swap) 
147,400 
0.15% 
0.02% 
Infore Capital 
Management is a close 
associate of Infore 
Capital, one of the 
Cornerstone Investors 
Li Dongsheng (李東生) 
351,000 
0.37% 
0.04% 
A close associate of 
Metazone, one of the 
Cornerstone Investors 
MY Asian 
351,000 
0.37% 
0.04% 
Same entity as the 
Cornerstone Investor
Ovata Equity Strategies 
Master Fund 
300,000 
0.31% 
0.03% 
A close associate of 
Ovata Capital, one of 
the Cornerstone 
Investors 
SR Wealth 
351,000 
0.37% 
0.04% 
Same entity as the 
Cornerstone Investor

<<<PAGE 13>>>
13 
Investor 
No. 
of 
Offer 
Shares 
allocated 
% of H Shares 
(after taking into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(after taking into 
account the full 
exercise 
of 
the 
Offer 
Size 
Adjustment Option 
and assuming the 
Over-allotment 
Option 
is 
not 
exercised) 
Relationship 
Ruihua Investment 
313,600 
0.33% 
0.03% 
Same entity as the 
Cornerstone Investor
CloudAlpha Capital 
186,700 
0.19% 
0.02% 
Same entity as the 
Cornerstone Investor
Everbright Wealth 
Management 
186,700 
0.19% 
0.02% 
Same entity as the 
Cornerstone Investor
ICBC Wealth 
Management Co., Ltd. 
(through EPF 
GUANGYING 
OVERSEAS NO.38 
QDII SMA as an asset 
manager) 
11,000 
0.01% 
0.001% 
The asset manager is a 
close associate of 
Everbright Wealth 
Management, one of 
the Cornerstone 
Investors
Jump Trading 
261,000 
0.27% 
0.03% 
Same entity as the 
Cornerstone Investor
Luhua Daosheng 
149,300 
0.16% 
0.02% 
Same entity as the 
Cornerstone Investor
Mirae Asset 
223,700 
0.23% 
0.02% 
Same entity as the 
Cornerstone Investor
Mirae Asset Securities 
(HK) Limited 
37,300 
0.04% 
0.004% 
A close associate of 
Mirae Asset, one of 
the Cornerstone 
Investors
Panjing Fund 
186,700 
0.19% 
0.02% 
Same entity as the 
Cornerstone Investor
WSOF 
186,700 
0.19% 
0.02% 
Same entity as the 
Cornerstone Investor
Black Dragon 
373,400 
0.39% 
0.04% 
Same entity as the 
Cornerstone Investor
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients Note 3
China Securities 
(International) 
Investment Company 
Limited (“CSII”) 
3,700 
0.004% 
0.0004% 
Connected client as a 
placee 
GF International 
Investment Management 
45,000 
0.05% 
0.005% 
Connected client as a 
placee 

<<<PAGE 14>>>
14 
Investor 
No. 
of 
Offer 
Shares 
allocated 
% of H Shares 
(after taking into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(after taking into 
account the full 
exercise 
of 
the 
Offer 
Size 
Adjustment Option 
and assuming the 
Over-allotment 
Option 
is 
not 
exercised) 
Relationship 
Limited (“GF 
International”) 
Value Partners Hong 
Kong Limited 
(“VPHKL”) 
38,800 
0.04% 
0.004% 
Connected client as a 
placee 
Value Partners Limited 
(“VPL”) 
6,200 
0.01% 
0.001% 
Connected client as a 
placee 
E Fund 
102,300 
0.11% 
0.01% 
Connected client as a 
placee 
E Fund HK 
17,700 
0.02% 
0.002% 
Connected client as a 
placee 
GF Securities Asset 
Management 
(Guangdong) Co., Ltd. 
(“GF Securities AM”) 
2,529,700 
2.64% 
0.26% 
Connected client 
investing as an asset 
manager of certain 
cornerstone investors 
(being Huizhou 
Huilian, Everbright 
Wealth Management 
and Luhua Daosheng) 
and placees 
GFGC 
166,100 
0.17% 
0.02% 
Connected client as a 
placee 
CICC Financial Trading 
Limited (“CICC FT”) 
3,651,000 
3.81% 
0.38% 
Connected client as a 
placee 
ABCI Asset Management 
Limited (“ABCI AM”) 
55,000 
0.06% 
0.01% 
Connected client as a 
placee 
HTCI  
4,428,000 
4.62% 
0.46% 
Connected client as a 
placee 
China Southern Asset 
Management Co., Ltd. 
(“China Southern”)  
45,000 
0.05% 
0.005% 
Connected client as a 
placee 
Bosera International 
1,493,600 
1.56% 
0.15% 
Connected client as a 
cornerstone investor 
and a placee 

<<<PAGE 15>>>
15 
Investor 
No. 
of 
Offer 
Shares 
allocated 
% of H Shares 
(after taking into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(after taking into 
account the full 
exercise 
of 
the 
Offer 
Size 
Adjustment Option 
and assuming the 
Over-allotment 
Option 
is 
not 
exercised) 
Relationship 
Guotai Junan Financial 
Products Limited 
(“GTJA FP”) 
9,405,800 
9.81% 
0.97% 
Connected client as a 
placee 
HuaAn Fund 
Management Co., Ltd 
(“HuaAn”) 
3,700 
0.004% 
0.0004% 
Connected client as a 
placee 
Fullgoal Fund 
Management Co., Ltd. 
(“Fullgoal Fund”) 
107,000 
0.11% 
0.01% 
Connected client as a 
placee 
Fullgoal Asset 
Management (HK) 
Limited (“Fullgoal HK”) 19,300 
0.02% 
0.002% 
Connected client as a 
placee 
ICBC UBS Asset 
Management Co., Ltd. 
(“ICBC UBS”) and 
ICBC UBS Asset 
Management 
(International) Company 
Limited (“ICBC UBS 
(International)”) 
20,000 
0.02% 
0.002% 
Connected client as a 
placee 
UBS Asset Management 
(Singapore) Limited 
(“UBS AM Singapore”) 
180,000 
0.19% 
0.02% 
Connected client as a 
placee 
BOCHK Asset 
Management Limited 
(“BOC AM”) 
25,000 
0.03% 
0.003% 
Connected client as a 
placee 
JPMorgan Asset 
Management (Asia 
Pacific) Limited (“JPM 
AM”) 
240,000 
0.25% 
0.02% 
Connected client as a 
placee 
SR Wealth 
1,097,800 
1.15% 
0.11% 
Connected client as a 
cornerstone investor 
and a placee 
China Galaxy 
International Investment 
1,317,800 
1.37% 
0.14% 
Connected client as a 
placee 

<<<PAGE 16>>>
16 
Investor 
No. 
of 
Offer 
Shares 
allocated 
% of H Shares 
(after taking into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(after taking into 
account the full 
exercise 
of 
the 
Offer 
Size 
Adjustment Option 
and assuming the 
Over-allotment 
Option 
is 
not 
exercised) 
Relationship 
Company Limited 
(“CGII”) 
Shenwan Hongyuan 
Group Co., Ltd. 
(“SWHY”) (through GF 
Securities AM as the 
asset manager) 
15,000 
0.02% 
0.002% 
Connected client as a 
placee 
Allottees with waiver from strict compliance with Rules 10.03, 10.04 and 9.09(b) of the Listing Rules and 
consent under paragraph 1C(2) of the Placing Guidelines in relation to allocations to the Eligible Core 
Connected Person Participants under the Employee Preferential Offering Note 4
Eligible Core Connected 
Person Participants 
445,032 
0.46% 
0.05% 
Eligible Employees 
who are directors, 
supervisors or chief 
executives of the 
Company’s 
subsidiaries and/or 
their close associates 
Notes: 
1.
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the 
Global Offering. 
2.
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the number of Offer Shares 
allocated to the investors as placees in the International Offering. For allocations of Offer Shares to the relevant investors and/or 
their close associates as Cornerstone Investors, please refer to the section headed “Allotment Results Details – International 
Offering – Cornerstone Investors” in this announcement. For details of the consent under paragraph 18 of Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations of further H Shares to the existing Shareholders and Cornerstone 
Investors and/or their close associates, please refer to the section headed “Others / Additional Information – Allocations of Offer 
Shares to the existing Shareholders and Cornerstone Investors and/or their close associates with a consent under paragraph 18 of 
Chapter 4.15 of the Guide for New Listing Applicants” in this announcement. 
3.
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations to connected clients, please refer to the sections headed “Others / Additional Information – 
Placing to connected clients with a consent under paragraph 1C(1) of the Placing Guidelines” and “Others / Additional 
Information – Allocations of Offer Shares to the existing Shareholders and the Cornerstone Investors and/or their close associates 
with a consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants” in this announcement. 
4.
For details of the waiver from strict compliance with Rules 10.03, 10.04 and 9.09(b) of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to allocations to Eligible Core Connected Person Participants and the 
Employee Preferential Offering, please refer to the sections headed “Waivers – Waiver in respect of Allocations to Eligible Director 
Participants, Existing Shareholder Employee Participants and Restrictions on Dealings in Securities by Core Connected Persons 
during the Listing Application Process”, “Structure of the Global Offering – The Overseas Employee Preferential Offering” and 
“Structure of the Global Offering – The PRC Employee Preferential Offering” of the Prospectus. For details of the allocations 
under the PRC Employee Preferential Offering, please refer to the section headed “Others / Additional Information – Allocations 
under the PRC Employee Preferential Offering” in this announcement.

<<<PAGE 17>>>
17 
Allottees who are customer(s) and/or supplier(s) of the Company
Investor 
No. of Offer 
Shares 
allocated 
% of H Shares 
(after 
taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) Note 1
% of total issued 
share capital after 
the Global Offering 
(after taking into 
account 
the 
full 
exercise 
of 
the 
Offer 
Size 
Adjustment Option 
and assuming the 
Over-allotment 
Option 
is 
not 
exercised) 
Relationship 
Hong Kong Mason
1,867,100
1.95%
0.19%
Subsidiary of a 
supplier of the 
Group
Huaqin Singapore
373,400
0.39%
0.04%
Subsidiary of a 
customer of the 
Group
Note: 
1.
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the 
Global Offering. 

<<<PAGE 18>>>
18 
LOCK-UP UNDERTAKINGS  
Largest Group of Shareholders 
Name Note 1
Number 
and 
description 
of 
Shares held in 
the 
Company 
subject to lock-
up undertakings 
upon Listing
% of total issued H 
Shares after the Global 
Offering 
subject 
to 
lock-up 
undertakings 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size Adjustment Option 
and assuming the Over-
allotment Option is not 
exercised) Note 2
% of shareholding in 
the Company subject 
to 
lock-up 
undertakings 
(after 
taking into account 
the full exercise of the 
Offer Size Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Last day subject to 
the 
lock-up 
undertakings Note 3
Shenghua 
Xinye
134,837,190 
A 
Shares
- 
13.92% 
October 20, 2026 Note 
4 
Hong Kong 
Victory 
Giant
131,432,001 
A 
Shares 
- 
13.57% 
October 20, 2026 Note 
4
Ms. 
Liu 
Chunlan
3,791,642 
A 
Shares
- 
0.39% 
October 20, 2026 Note 
4
Notes: 
1.
For illustrative purposes only, this subsection lists only those members of the Largest Group of Shareholders who hold Shares 
directly in the Company. Pursuant to Rule 10.07 of the Listing Rules, each member of the Largest Group of Shareholders 
(namely, Mr. Chen Tao, Ms. Liu Chunlan, Shenghua Xinye, Hongda Investment and Hong Kong Victory Giant) has undertaken 
to the Stock Exchange and the Company that, except in connection with the Global Offering (including the Offer Size Adjustment 
Option and the Over-allotment Option), he, she or it shall, and shall procure that the relevant registered holders of the Shares 
in which he, she or it is beneficially interested shall, comply with the applicable lock-up requirements. For further details, 
please refer to the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – 
Undertakings to the Stock Exchange pursuant to the Listing Rules – Undertakings by the Largest Group of Shareholders” in 
the Prospectus. 
2.
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under 
the Global Offering. 
3.
In accordance with the applicable Listing Rules, the required lock-up for the six-month period will end on October 20, 2026. 
4.
The Largest Group of Shareholders will cease to be prohibited from disposing of or transferring Shares after the indicated date. 

<<<PAGE 19>>>
19 
Cornerstone Investors 
Name 
Number 
and 
description 
of 
Shares held in the 
Company subject to 
lock-up 
undertakings upon 
Listing
% of total issued H 
Shares 
after 
the 
Global 
Offering 
subject to lock-up 
undertakings 
(after 
taking into account 
the full exercise of 
the 
Offer 
Size 
Adjustment 
Option 
and assuming the 
Over-allotment 
Option 
is 
not 
exercised) Note 1
% of shareholding in 
the Company subject 
to 
lock-up 
undertakings 
(after 
taking into account 
the full exercise of the 
Offer Size Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Last 
day 
subject to the 
lock-up 
undertakings 
Note 2
CPE Rosewood
2,800,700 H Shares
2.92%
0.29%
October 20, 
2026
Janchor Fund
2,800,700 H Shares
2.92%
0.29%
October 20, 
2026
Yunfeng Capital
New Alternative
1,493,700 H Shares
1.56%
0.15%
October 20, 
2026
New Golden 
Future Limited
746,800 H Shares
0.78%
0.08%
October 20, 
2026
Deliante
1,979,200 H Shares
2.06%
0.20%
October 20, 
2026
Hong Kong Mason
1,867,100 H Shares
1.95%
0.19%
October 20, 
2026
MSIP
1,307,000 H Shares
1.36%
0.13%
October 20, 
2026
Foresight
1,120,300 H Shares
1.17%
0.12%
October 20, 
2026
HHLRA
1,120,300 H Shares
1.17%
0.12%
October 20, 
2026
Pinpoint
1,120,300 H Shares
1.17%
0.12%
October 20, 
2026
Sunshine Life
1,120,300 H Shares
1.17%
0.12%
October 20, 
2026
Tanwan
1,120,300 H Shares
1.17%
0.12%
October 20, 
2026
Tropical Terrain 
Limited
1,120,300 H Shares
1.17%
0.12%
October 20, 
2026
YR Asset 
Management
1,120,300 H Shares
1.17%
0.12%
October 20, 
2026
Huizhou Huilian
1,073,500 H Shares
1.12%
0.11%
October 20, 
2026
HK Greenwoods
933,500 H Shares
0.97%
0.10%
October 20, 
2026
Bosera 
International
746,800 H Shares
0.78%
0.08%
October 20, 
2026

<<<PAGE 20>>>
20 
Name 
Number 
and 
description 
of 
Shares held in the 
Company subject to 
lock-up 
undertakings upon 
Listing
% of total issued H 
Shares 
after 
the 
Global 
Offering 
subject to lock-up 
undertakings 
(after 
taking into account 
the full exercise of 
the 
Offer 
Size 
Adjustment 
Option 
and assuming the 
Over-allotment 
Option 
is 
not 
exercised) Note 1
% of shareholding in 
the Company subject 
to 
lock-up 
undertakings 
(after 
taking into account 
the full exercise of the 
Offer Size Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Last 
day 
subject to the 
lock-up 
undertakings 
Note 2
Cloudview
746,800 H Shares
0.78%
0.08%
October 20, 
2026
CNCB Investment
746,800 H Shares
0.78%
0.08%
October 20, 
2026
GBAHIL
Mega Prime
466,700 H Shares
0.49%
0.05%
October 20, 
2026
Poly Platinum
280,000 H Shares
0.29%
0.03%
October 20, 
2026
Golden K2 Falcon
746,800 H Shares
0.78%
0.08%
October 20, 
2026
Infore Capital
746,800 H Shares
0.78%
0.08%
October 20, 
2026
Metazone
746,800 H Shares
0.78%
0.08%
October 20, 
2026
MY Asian
746,800 H Shares
0.78%
0.08%
October 20, 
2026
Ovata Capital
746,800 H Shares
0.78%
0.08%
October 20, 
2026
SR Wealth
746,800 H Shares
0.78%
0.08%
October 20, 
2026
Ruihua Investment
746,800 H Shares
0.78%
0.08%
October 20, 
2026
Tianhong Fund
746,800 H Shares
0.78%
0.08%
October 20, 
2026
Ye Guofu
746,800 H Shares
0.78%
0.08%
October 20, 
2026
CloudAlpha 
Capital
560,100 H Shares
0.58%
0.06%
October 20, 
2026
Everbright Wealth 
Management
560,100 H Shares
0.58%
0.06%
October 20, 
2026
Jump Trading 
Pacific
560,100 H Shares
0.58%
0.06%
October 20, 
2026
Luhua Daosheng
560,100 H Shares
0.58%
0.06%
October 20, 
2026
Mirae Asset
560,100 H Shares
0.58%
0.06%
October 20, 
2026

<<<PAGE 21>>>
21 
Name 
Number 
and 
description 
of 
Shares held in the 
Company subject to 
lock-up 
undertakings upon 
Listing
% of total issued H 
Shares 
after 
the 
Global 
Offering 
subject to lock-up 
undertakings 
(after 
taking into account 
the full exercise of 
the 
Offer 
Size 
Adjustment 
Option 
and assuming the 
Over-allotment 
Option 
is 
not 
exercised) Note 1
% of shareholding in 
the Company subject 
to 
lock-up 
undertakings 
(after 
taking into account 
the full exercise of the 
Offer Size Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Last 
day 
subject to the 
lock-up 
undertakings 
Note 2
Panjing Fund
560,100 H Shares
0.58%
0.06%
October 20, 
2026
WSOF
560,100 H Shares
0.58%
0.06%
October 20, 
2026
Black Dragon
373,400 H Shares
0.39%
0.04%
October 20, 
2026
Huaqin Singapore
373,400 H Shares
0.39%
0.04%
October 20, 
2026
Notes: 
1.
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the Global 
Offering. 
2.
In accordance with the relevant cornerstone investment agreements, the required lock-up periods will end on October 20, 2026. The 
Cornerstone Investors will cease to be prohibited from disposing of or transferring the H Shares subscribed for pursuant to the relevant 
cornerstone investment agreements after the indicated date. 

<<<PAGE 22>>>
22 
PLACEE CONCENTRATION ANALYSIS
Placees* 
Number of H 
Shares allotted 
Allotment 
as % of the 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)**
Allotment 
as % of the 
International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised)**
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
Option is 
fully 
exercised)
Number of H 
Shares held upon 
Listing
% of total 
issued share 
capital upon 
Listing 
(assuming no 
exercise of 
the Over-
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
fully 
exercised)
Top 1
5,601,400
6.40%
5.50%
5.84%
5.08%
5,601,400
0.58%
0.57%
Top 5
20,673,900
23.62%
20.29%
21.57%
18.76%
20,673,900
2.13%
2.10%
Top 10
31,192,400
35.64%
30.61%
32.54%
28.30%
31,192,400
3.22%
3.17%
Top 25
53,711,900
61.37%
52.71%
56.04%
48.73%
53,711,900
5.55%
5.47%
Notes: 
* Ranking of placees is based on the number of H Shares allotted to the placees. 
** The International Offering includes the PRC Employee Preferential Offering. 

<<<PAGE 23>>>
23 
H SHAREHOLDERS CONCENTRATION ANALYSIS
H 
Shareholders* 
Number of H 
Shares 
allotted 
Allotment as % 
of the 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)**
Allotment as % 
of the 
International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised)**
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
as % of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised)
Number of H 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing 
(assuming no 
exercise of the 
Over-
allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming the 
Over-
allotment 
Option is fully 
exercised)
Top 1
5,601,400
6.40%
5.50%
5.84%
5.08%
5,601,400
0.58%
0.57%
Top 5
20,673,900
23.62%
20.29%
21.57%
18.76%
20,673,900
2.13%
2.10%
Top 10
31,192,400
35.64%
30.61%
32.54%
28.30%
31,192,400
3.22%
3.17%
Top 25
53,711,900
61.37%
52.71%
56.04%
48.73%
53,711,900
5.55%
5.47%
Notes: 
* Ranking of H Shareholders is based on the number of H Shares held by the Shareholders upon Listing. 
** The International Offering includes the PRC Employee Preferential Offering. 

<<<PAGE 24>>>
24 
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders* 
Number of H 
Shares 
allotted 
Allotment 
as % of the 
International 
Offering 
(assuming no 
exercise of 
the Over-
allotment 
Option)**
Allotment 
as % of the 
International 
Offering 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised)**
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
Option is 
fully 
exercised)
Number of H 
Shares held 
upon Listing
Number of 
Shares held 
upon Listing
% of total 
issued 
share 
capital 
upon 
Listing 
(assuming 
no exercise 
of the 
Over-
allotment 
Option)
% of total 
issued 
share 
capital 
upon 
Listing 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised)
Top 1
0
0
0
0
0
0
270,060,833
27.89%
27.48%
Top 5
6,547,800
7.48%
6.43%
6.83%
5.94%
6,547,800
332,074,128
34.29%
33.79%
Top 10
15,800,200
18.05%
15.51%
16.48%
14.33%
15,800,200
365,977,549
37.79%
37.24%
Top 25
27,048,200
30.91%
26.55%
28.22%
24.54%
27,048,200
413,756,441
42.73%
42.10%
Notes: 
* Ranking of Shareholders is based on the number of Shares held by the Shareholders upon Listing. 
** The International Offering includes the PRC Employee Preferential Offering. 

<<<PAGE 25>>>
25 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below: 
NO. 
OF 
H 
SHARES 
APPLIED 
FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF ALLOTMENT / 
BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF THE 
TOTAL NO. OF H 
SHARES 
APPLIED 
FOR 
POOL A 
100
77,460
553 out of 77,460 to receive 100 
Shares
0.71%
200
22,437
320 out of 22,437 to receive 100 
Shares
0.71%
300
7,527
161 out of 7,527 to receive 100 
Shares
0.71%
400
9,223
263 out of 9,223 to receive 100 
Shares
0.71%
500
7,281
260 out of 7,281 to receive 100 
Shares
0.71%
600
3,720
159 out of 3,720 to receive 100 
Shares
0.71%
700
3,178
159 out of 3,178 to receive 100 
Shares
0.71%
800
2,839
162 out of 2,839 to receive 100 
Shares
0.71%
900
3,787
243 out of 3,787 to receive 100 
Shares
0.71%
1,000
14,124
1,008 out of 14,124 to receive 
100 Shares
0.71%
1,500
7,563
809 out of 7,563 to receive 100 
Shares
0.71%
2,000
6,427
917 out of 6,427 to receive 100 
Shares
0.71%
2,500
4,150
740 out of 4,150 to receive 100 
Shares
0.71%
3,000
4,046
866 out of 4,046 to receive 100 
Shares
0.71%
3,500
2,628
656 out of 2,628 to receive 100 
Shares
0.71%
4,000
2,867
818 out of 2,867 to receive 100 
Shares
0.71%
4,500
2,549
818 out of 2,549 to receive 100 
Shares
0.71%
5,000
4,691
1,673 out of 4,691 to receive 
100 Shares
0.71%

<<<PAGE 26>>>
26 
6,000
3,029
1,296 out of 3,029 to receive 
100 Shares
0.71%
7,000
2,679
1,338 out of 2,679 to receive 
100 Shares
0.71%
8,000
2,121
1,210 out of 2,121 to receive 
100 Shares
0.71%
9,000
2,177
1,398 out of 2,177 to receive 
100 Shares
0.71%
10,000
13,030
9,295 out of 13,030 to receive 
100 Shares
0.71%
20,000
9,913
100 Shares plus 4,229 out of 
9,913 to receive additional 100 
Shares
0.71%
Total 
219,446
Total number of Pool A 
successful applicants: 35,035
POOL B 
30,000
10,843
4,759 out of 10,843 to receive 
100 Shares
0.15%
40,000
4,543
2,659 out of 4,543 to receive 100 
Shares
0.15%
50,000
3,098
2,266 out of 3,098 to receive 100 
Shares
0.15%
60,000
2,114
1,856 out of 2,114 to receive 100 
Shares
0.15%
70,000
1,561
100 Shares plus 38 out of 1,561 
to receive additional 100 Shares
0.15%
80,000
1,247
100 Shares plus 212 out of 1,247 
to receive additional 100 Shares
0.15%
90,000
982
100 Shares plus 311 out of 982 to 
receive additional 100 Shares
0.15%
100,000
3,924
100 Shares plus 1,817 out of 
3,924 to receive additional 100 
Shares
0.15%
200,000
1,380
200 Shares plus 1,278 out of 
1,380 to receive additional 100 
Shares
0.15%
300,000
539
400 Shares plus 210 out of 539 to 
receive additional 100 Shares
0.15%
400,000
265
500 Shares plus 226 out of 265 to 
receive additional 100 Shares
0.15%
500,000
366
700 Shares plus 115 out of 366 to 
receive additional 100 Shares
0.15%
1,000,000
167
1,400 Shares plus 105 out of 167 
to receive additional 100 Shares
0.15%
1,500,000
41
2,100 Shares plus 39 out of 41 to 
receive additional 100 Shares
0.15%
2,000,000
50
2,900 Shares plus 13 out of 50 to 
receive additional 100 Shares
0.15%

<<<PAGE 27>>>
27 
3,750,700
40
5,400 Shares plus 34 out of 40 to 
receive additional 100 Shares
0.15%
Total 
31,160
Total 
number of 
Pool 
B 
successful applicants: 22,102
BASIS OF ALLOCATION UNDER THE OVERSEAS EMPLOYEE PREFERENTIAL 
OFFERING  
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 46 valid applications 
via Pink Form eIPO service will be conditionally allocated on the basis set out below. No preferential 
treatment was given to any of the Overseas Eligible Employees in the allocation of the Shares applied 
for by them under the Overseas Employee Preferential Offering and such allocation of Shares under 
the Overseas Employee Preferential Offering was made in accordance with the allocation basis 
described in the Prospectus. The 482,000 Overseas Employees Reserved Shares validly applied for 
will be allocated to Overseas Eligible Employees who have applied pursuant to the Overseas Employee 
Preferential Offering. The 351,400 under-subscribed Overseas Employee Reserved Shares were 
reallocated to the Hong Kong Public Offering for subscription by the public in Hong Kong. 
Number of 
Overseas 
Employee 
Reserved 
Shares 
Applied for 
Number of 
Valid 
Applications 
Basis of Allotment/Ballot 
Total 
Number 
of 
Overseas 
Employee 
Reserved 
Shares 
Allotted
Approximate 
Percentage 
Allocation 
Based on the 
Total 
Number of 
Employee 
Reserved 
Shares 
Applied for 
100
1
Allot Overseas Employee Reserved 
Shares applied for in full
100
100%
300
2
Allot Overseas Employee Reserved 
Shares applied for in full
600
100%
500
2
Allot Overseas Employee Reserved 
Shares applied for in full
1,000
100%
700
2
Allot Overseas Employee Reserved 
Shares applied for in full
1,400
100%
900
1
Allot Overseas Employee Reserved 
Shares applied for in full
900
100%
1,000
6
Allot Overseas Employee Reserved 
Shares applied for in full
6,000
100%
2,000
3
Allot Overseas Employee Reserved 
Shares applied for in full
6,000
100%
3,000
8
Allot Overseas Employee Reserved 
Shares applied for in full
24,000
100%
4,000
4
Allot Overseas Employee Reserved 
Shares applied for in full
16,000
100%
5,000
2
Allot Overseas Employee Reserved 
Shares applied for in full
10,000
100%

<<<PAGE 28>>>
28 
6,000
3
Allot Overseas Employee Reserved 
Shares applied for in full
18,000
100%
8,000
1
Allot Overseas Employee Reserved 
Shares applied for in full
8,000
100%
10,000
3
Allot Overseas Employee Reserved 
Shares applied for in full
30,000
100%
20,000
4
Allot Overseas Employee Reserved 
Shares applied for in full
80,000
100%
30,000
1
Allot Overseas Employee Reserved 
Shares applied for in full
30,000
100%
40,000
1
Allot Overseas Employee Reserved 
Shares applied for in full
40,000
100%
60,000
1
Allot Overseas Employee Reserved 
Shares applied for in full
60,000
100%
150,000
1
Allot Overseas Employee Reserved 
Shares applied for in full
150,000
100%
Total 
46
Total 
number 
of 
successful 
applicants: 46 
482,000
COMPLIANCE WITH LISTING RULES AND GUIDANCE  
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the H Shares.  
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the 
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by 
them is the same as the final Offer Price in addition to any brokerage, AFRC transaction levy, SFC 
transaction levy and trading fee payable. 
OTHERS / ADDITIONAL INFORMATION 
Offer Size Adjustment Option  
The Offer Size Adjustment Option has been exercised by the Sponsor-Overall Coordinators in full, 
pursuant to which the Company is issuing and allotting 12,502,000 additional H Shares, representing 
approximately 15.0% of the total number of H Shares initially available under the Global Offering, at 
the final Offer Price. All of the additional H Shares that would be allotted and issued by the Company 
pursuant to the full exercise of the Offer Size Adjustment Option will be allocated to the International 
Offering.  
Accordingly, the total number of Offer Shares finally available under the Global Offering (after taking 
into account the full exercise of the Offer Size Adjustment Option and before any exercise of the Over-
allotment Option) that would be allotted and issued by the Company is 95,850,000 H Shares and the 
total issued share capital of the Company upon Listing (after taking into account the full exercise of 
the Offer Size Adjustment Option and before any exercise of the Over-allotment Option) will be 
968,407,313 Shares. 
Allocation of H Shares to Existing Minority Shareholders and their close associates 

<<<PAGE 29>>>
29 
The Company has applied for, and the Stock Exchange has granted, a waiver from strict compliance 
with Rule 10.04 of, and a consent under paragraph 1C(2) of Appendix F1 to, the Listing Rules to 
permit H Shares in the International Offering to be placed to certain existing minority Shareholders 
who (i) hold less than 5% of the total number of A Shares in issue of the Company prior to the 
completion of the Global Offering and (ii) are not and will not become (upon the completion of the 
Global Offering) core connected persons of the Company or the close associates of any such core 
connected person (together, the “Existing Minority Shareholders”), on the following conditions: 
(i)
each Existing Minority Shareholder to whom the Company may allocate the H Shares in 
the International Offering holds less than 5% of the total number of A Shares in issue of 
the Company prior to the completion of the Global Offering; 
(ii)
each Existing Minority Shareholder is not, and will not be, a core connected person of the 
Company or any close associate of any such core connected person immediately prior to or 
following the Global Offering; 
(iii)
none of the Existing Minority Shareholders has the right to appoint a Director and/or have 
any other special rights; 
(iv)
allocation to the Existing Minority Shareholders or their close associates will not affect the 
Company’s ability to satisfy the public float requirement as prescribed under Rule 8.08 (as 
amended and replaced by Rule 19A.13A) of the Listing Rules; 
(v)
no preferential treatment is given to the Existing Minority Shareholders or their respective 
close associates (other than the assured entitlement for a cornerstone investor); and 
(vi)
details of the allocation to the Existing Minority Shareholders and/or their respective close 
associates holding more than 1% of the issued share capital of the Company immediately 
prior to the completion of the Global Offering have been disclosed in this announcement. 
Please refer to the section headed “Waivers – Allocation of H Shares to Existing Minority Shareholders 
and Their Close Associates” in the Prospectus for further details of the waiver and consent. As the A 
Shares are listed on the ChiNext Market of Shenzhen Stock Exchange since June 11, 2015, the 
Company has a highly extensive base of existing Shareholders and disclosure of details of allocations 
to all Existing Minority Shareholders and/or their respective close associates will not be meaningful 
to investors, the proposed disclosure threshold, i.e. condition (vi) of the waiver and consent which 
provides that details of the allocation to the Existing Minority Shareholders and/or their respective 
close associates holding more than 1% of the issued share capital of the Company immediately prior 
to the completion of the Global Offering will be disclosed in this announcement, is appropriate. 
Allocations of Offer Shares to existing Shareholders and Cornerstone Investors and/or their 
close associates with a consent under Chapter 4.15 of the Guide for New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 of 
the Guide for New Listing Applicants to permit the Company to allocate further Offer Shares in the 
International Offering to certain existing Shareholders and Cornerstone Investors and/or their close 
associates as placees, subject to the following conditions (the “Allocation to Size-based Exemption 
Participants”): 

<<<PAGE 30>>>
30 
(a) the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion; 
(b) the Offer Shares allocated to all existing Shareholders (whether as Cornerstone Investors and/or 
as placees) as permitted under this exemption do not exceed 30% of the total number of Offer 
Shares offered under the Global Offering; 
(c) the Allocation to Size-based Exemption Participants will not affect the Company’s ability to 
satisfy its public float requirement under Rule 8.08(1) (as amended and replaced by Rule 
19A.13A) of the Listing Rules; 
(d) each of the Directors and chief executive of the Company confirms that no securities have been 
allocated to them or their respective close associates under this exemption; and 
(e) details of the Cornerstone Investors and/or their close associates under this exemption will be 
disclosed in this announcement. 
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted 
by the Stock Exchange. 
For details of the allocations of Offer Shares to Cornerstone Investors, please refer to the section 
headed “Allotment Results Details – International Offering – Allottees with Waivers / Consents 
Obtained” in this announcement. 
Placing to connected clients with a consent under paragraph 1C(1) of the Placing Guidelines 
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a consent 
under paragraph 1C(1) of the Placing Guidelines to permit each of Huizhou Huilian, Everbright Wealth 
Management and Luhua Daosheng and Huizhou Huilian (through GF Securities AM as the asset 
manager) to participate in the Global Offering as a cornerstone investor. For details of the consent 
granted, please refer to “Waivers – Consent in respect of the Proposed Subscription of H Shares by 
Everbright Wealth Management, Luhua Daosheng and Huizhou Huilian through GF Securities AM” 
in the Prospectus.  
In addition, under the International Offering, certain Offer Shares were placed to connected clients of 
their connected distributors pursuant to the Placing Guidelines as placees. Please refer to the section 
headed “Allotment Results Details – International Offering – Allottees with Waivers / Consents 
Obtained” in this announcement for details. The Company has applied to the Stock Exchange for, and 
the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing Guidelines to permit 
the Company to allocate such Offer Shares in the International Offering to the connected clients as 
placees. The allocation of Offer Shares to such connected clients is in compliance with all the 
conditions under the consent granted by the Stock Exchange. Details of the placement to connected 
clients as placees are set out below: 

<<<PAGE 31>>>
31 
No.
Connected 
Distributor 
Connected 
Client 
Relationship 
Whether the 
connected client 
is a collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Whether the 
connected client will 
hold the beneficial 
interests of the Offer 
Shares on a non-
discretionary basis 
or discretionary 
basis for 
independent third 
parties 
Number of Offer 
Shares to be 
allocated to the 
Connected Client 
Approximate percentage 
of total number of Offer 
Shares under the Global 
Offering (after taking into 
account the full exercise of 
the Offer Size Adjustment 
Option and assuming no 
exercise of the Over-
allotment Option) 
Approximate percentage of 
total issued share capital 
immediately following the 
Global Offering (after taking 
into account the full exercise 
of the Offer Size Adjustment 
Option and assuming the 
Over-allotment Option is not 
exercised) 
1.
China Securities 
(International) 
Corporate 
Finance 
Company 
Limited 
(“CSCI”)
CSII Note 1
CSII is a member 
of the same 
group of CSCI. 
N
Non-discretionary 
basis
3,700 
0.004% 
0.0004% 
2.
GF Securities 
(Hong Kong) 
Brokerage 
Limited (“GF 
Securities 
(Hong Kong) 
Brokerage”) 
GF International 
Note 2
GF International 
is a member of 
the same group 
of companies as 
GF Securities 
(Hong Kong) 
Brokerage.
Y
Discretionary basis
45,000 
0.05% 
0.005% 
3.
VPHKL and 
VPL Note 3
GF Securities 
(Hong Kong) 
Brokerage is an 
indirect wholly-
owned subsidiary 
of GF Securities 
Co., Ltd. (“GF 
Securities”). 
Each of VPHKL 
and VPL is a 
wholly-owned 
subsidiary of 
Y
Discretionary basis
VPHKL: 38,800 
0.04% 
0.004% 
VPL: 6,200 
0.01% 
0.001% 

<<<PAGE 32>>>
32 
No.
Connected 
Distributor 
Connected 
Client 
Relationship 
Whether the 
connected client 
is a collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Whether the 
connected client will 
hold the beneficial 
interests of the Offer 
Shares on a non-
discretionary basis 
or discretionary 
basis for 
independent third 
parties 
Number of Offer 
Shares to be 
allocated to the 
Connected Client 
Approximate percentage 
of total number of Offer 
Shares under the Global 
Offering (after taking into 
account the full exercise of 
the Offer Size Adjustment 
Option and assuming no 
exercise of the Over-
allotment Option) 
Approximate percentage of 
total issued share capital 
immediately following the 
Global Offering (after taking 
into account the full exercise 
of the Offer Size Adjustment 
Option and assuming the 
Over-allotment Option is not 
exercised) 
Value Partners 
Group Limited, a 
company listed 
on the Stock 
Exchange (stock 
code: 806) 
(“Value 
Partners 
Group”). Since 
GF Securities is 
interested in 
20.04% of the 
issued share 
capital of Value 
Partners Group, 
it renders each of 
VPHKL and 
VPL an associate 
of GF Securities. 
Each of VPHKL 
and VPL is 
therefore a 
member of the 
same group 
companies as GF 
Securities (Hong 
Kong) 
Brokerage.

<<<PAGE 33>>>
33 
No.
Connected 
Distributor 
Connected 
Client 
Relationship 
Whether the 
connected client 
is a collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Whether the 
connected client will 
hold the beneficial 
interests of the Offer 
Shares on a non-
discretionary basis 
or discretionary 
basis for 
independent third 
parties 
Number of Offer 
Shares to be 
allocated to the 
Connected Client 
Approximate percentage 
of total number of Offer 
Shares under the Global 
Offering (after taking into 
account the full exercise of 
the Offer Size Adjustment 
Option and assuming no 
exercise of the Over-
allotment Option) 
Approximate percentage of 
total issued share capital 
immediately following the 
Global Offering (after taking 
into account the full exercise 
of the Offer Size Adjustment 
Option and assuming the 
Over-allotment Option is not 
exercised) 
4.
E Fund Note 4
E Fund is a 
member of the 
same group of 
companies as GF 
Securities (Hong 
Kong) 
Brokerage.
N
Discretionary basis
102,300 
0.11% 
0.01% 
5.
E Fund HK Note 5 
E Fund HK is a 
member of the 
same group of 
companies as GF 
Securities (Hong 
Kong) 
Brokerage.
N
Discretionary basis
17,700 
0.02% 
0.002% 
6.
GF Securities 
AM Note 6
GF Securities 
AM is a member 
of the same 
group of 
companies as GF 
Securities (Hong 
Kong) 
Brokerage.
N
Non-discretionary 
basis
2,529,700 
2.64% 
0.26% 
7.
GFGC Note 7
GFGC is a 
member of the 
same group of 
companies as GF 
Securities (Hong 
Kong) 
Brokerage.
N
Non-discretionary 
basis
166,100 
0.17% 
0.02% 

<<<PAGE 34>>>
34 
No.
Connected 
Distributor 
Connected 
Client 
Relationship 
Whether the 
connected client 
is a collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Whether the 
connected client will 
hold the beneficial 
interests of the Offer 
Shares on a non-
discretionary basis 
or discretionary 
basis for 
independent third 
parties 
Number of Offer 
Shares to be 
allocated to the 
Connected Client 
Approximate percentage 
of total number of Offer 
Shares under the Global 
Offering (after taking into 
account the full exercise of 
the Offer Size Adjustment 
Option and assuming no 
exercise of the Over-
allotment Option) 
Approximate percentage of 
total issued share capital 
immediately following the 
Global Offering (after taking 
into account the full exercise 
of the Offer Size Adjustment 
Option and assuming the 
Over-allotment Option is not 
exercised) 
8.
China 
International 
Capital 
Corporation 
Hong Kong 
Securities 
Limited 
(“CICC”)
CICC FT Note 8
CICC FT is a 
member of the 
same group of 
companies as 
CICC. 
N
Non-discretionary 
basis
3,651,000 
3.81% 
0.38% 
9.
ABCI Capital 
Limited and 
ABCI Securities 
Company 
Limited 
(collectively, 
“ABCI”)
ABCI AM Note 9
ABCI AM is a 
member of the 
same group as 
ABCI. 
N
Discretionary basis
55,000 
0.06% 
0.01% 
10.
Huatai Financial 
Holdings (Hong 
Kong) Limited 
(“HTFH”) 
HTCI 
HTCI is a 
member of the 
same group of 
HTFH. 
N
Non-discretionary 
basis
Huatai 
Offshore 
Ultimate Client Note 
10: 1,482,100 
1.55% 
0.15% 
11.
Huatai 
Onshore 
Ultimate Clients Note 
11: 2,945,900 
3.07% 
0.30% 
12.
China Southern 
Note 12
China Southern 
is held by Huatai 
Securities Co., 
Ltd. as to 
41.16%, which 
N
Discretionary basis
45,000 
0.05% 
0.005% 

<<<PAGE 35>>>
35 
No.
Connected 
Distributor 
Connected 
Client 
Relationship 
Whether the 
connected client 
is a collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Whether the 
connected client will 
hold the beneficial 
interests of the Offer 
Shares on a non-
discretionary basis 
or discretionary 
basis for 
independent third 
parties 
Number of Offer 
Shares to be 
allocated to the 
Connected Client 
Approximate percentage 
of total number of Offer 
Shares under the Global 
Offering (after taking into 
account the full exercise of 
the Offer Size Adjustment 
Option and assuming no 
exercise of the Over-
allotment Option) 
Approximate percentage of 
total issued share capital 
immediately following the 
Global Offering (after taking 
into account the full exercise 
of the Offer Size Adjustment 
Option and assuming the 
Over-allotment Option is not 
exercised) 
wholly owns 
HTFH. 
As such, China 
Southern and 
HTFH is a 
member of the 
same group of 
companies. 
13.
CMB 
International 
Securities 
Limited 
(“CMBI”) and 
China Merchants 
Securities (HK) 
Co., Limited 
(“CMS HK”)
Bosera 
International Note 
13
Bosera 
International is a 
member of the 
same group of 
CMBI and CMS 
HK. 
N
Discretionary basis
1,493,600 
1.56% 
0.15% 
14.
Guotai Junan 
Securities (Hong 
Kong) Limited 
(“GTJA HK”) 
and Haitong 
International 
Securities 
Company 
Limited (“HTI”)  
GTJA FP Note 14 
GTJA FP is a 
member of the 
same group as 
GTJA HK and 
HTI.
N
Non-discretionary 
basis
9,405,800 
9.81% 
0.97% 
15.
HuaAn Note 15
HuaAn is a 
member of the 
same group as 
GTJA HK and 
HTI.
N
Discretionary basis
3,700 
0.004% 
0.0004% 

<<<PAGE 36>>>
36 
No.
Connected 
Distributor 
Connected 
Client 
Relationship 
Whether the 
connected client 
is a collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Whether the 
connected client will 
hold the beneficial 
interests of the Offer 
Shares on a non-
discretionary basis 
or discretionary 
basis for 
independent third 
parties 
Number of Offer 
Shares to be 
allocated to the 
Connected Client 
Approximate percentage 
of total number of Offer 
Shares under the Global 
Offering (after taking into 
account the full exercise of 
the Offer Size Adjustment 
Option and assuming no 
exercise of the Over-
allotment Option) 
Approximate percentage of 
total issued share capital 
immediately following the 
Global Offering (after taking 
into account the full exercise 
of the Offer Size Adjustment 
Option and assuming the 
Over-allotment Option is not 
exercised) 
16.
GTJA HK, HTI 
and Shenwan 
Hongyuan 
Securities (H.K.) 
Limited 
(“SWHY HK”) 
Fullgoal Fund 
and Fullgoal HK 
Note 16
Fullgoal HK is a 
wholly owned 
subsidiary of 
Fullgoal Fund. 
Each of Guotai 
Haitong 
Securities Co., 
Ltd. and 
Shenwan 
Hongyuan 
Securities Co., 
Ltd. holds 
approximately 
27.775% in 
Fullgoal Fund. 
Accordingly, 
Fullgoal Fund 
and Fullgoal HK 
are members of 
the same group 
companies as 
GTJA HK, HTI 
and SWHY HK.
N
Discretionary basis
Fullgoal 
Fund: 
107,000 
0.11% 
0.01% 
Fullgoal HK: 19,300 
0.02% 
0.002% 
17.
UBS AG Hong 
Kong Branch 
(“UBS HK”) and 
UBS AG 
Singapore 
ICBC UBS and 
ICBC UBS 
(International) 
Note 17
ICBC UBS and 
ICBC UBS 
(International) 
are members of 
the same group 
N
Discretionary basis
ICBC UBS: 15,500 
0.02% 
0.002% 
ICBC 
UBS 
(International): 4,500 
0.005% 
0.0005% 

<<<PAGE 37>>>
37 
No.
Connected 
Distributor 
Connected 
Client 
Relationship 
Whether the 
connected client 
is a collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Whether the 
connected client will 
hold the beneficial 
interests of the Offer 
Shares on a non-
discretionary basis 
or discretionary 
basis for 
independent third 
parties 
Number of Offer 
Shares to be 
allocated to the 
Connected Client 
Approximate percentage 
of total number of Offer 
Shares under the Global 
Offering (after taking into 
account the full exercise of 
the Offer Size Adjustment 
Option and assuming no 
exercise of the Over-
allotment Option) 
Approximate percentage of 
total issued share capital 
immediately following the 
Global Offering (after taking 
into account the full exercise 
of the Offer Size Adjustment 
Option and assuming the 
Over-allotment Option is not 
exercised) 
Branch (“UBS 
SG”) 
of UBS HK and 
UBS SG.
18.
UBS AM 
Singapore Note 18
UBS AM 
Singapore is a 
member of the 
same group of 
UBS HK and 
UBS SG.
N
Discretionary basis
180,000 
0.19% 
0.02% 
19.
BOCI Securities 
Limited 
(“BOCI”) 
BOC AM Note 19 
BOC AM is a 
member of the 
same group of 
BOCI.
N
Discretionary basis
25,000 
0.03% 
0.003% 
20.
J.P. Morgan 
Securities (Asia 
Pacific) Limited 
(“JPM SAPL”) 
and JPMorgan 
Chase Bank, 
N.A. (“JPM 
Chase”)
JPM AM Note 20 
JPM AM is a 
member of the 
same group of 
companies as 
JPM SAPL and 
JPM Chase. 
N
Discretionary basis
240,000 
0.25% 
0.02% 
21.
SR Wealth (in 
the capacity of 
SFO Type 1 
license holder) 
SR Wealth (in 
the capacity of 
SFO Type 9 
license holder) 
Note 21
N/A 
N
Discretionary basis
1,097,800 
1.15% 
0.11% 
22.
China Galaxy 
International 
Securities (Hong 
CGII Note 22
CGII is a 
member of the 
N
Non-discretionary 
basis
1,317,800 
1.37% 
0.14% 

<<<PAGE 38>>>
38 
__________
Notes:
1.
CSII will enter into OTC total return swaps (TRS) with its end client (the “CSII Ultimate Client”), pursuant to which CSII will hold the allocated Offer Shares for the 
CSII Ultimate Client on a non-discretionary basis, and all the economic exposure will be passed to the CSII Ultimate Client through OTC total return swaps (TRS). 
Details of the CSII Ultimate Client are set out as below: 
Name of the CSII Ultimate Client 
Ultimate beneficial owner(s) holding 30% or more interest (if any) 
Shifeng Asset Daqiao No. 8 Private Securities Investment Fund (石鋒資產大巧
8 號私募證券投資基金) 
Guo Feng (郭鋒) 
To best of knowledge of CSII after making all reasonable enquiries, the CSII Ultimate Client is an independent third party of CSII, CSCI and the companies which are 
members of the same group of CSCI. 
2.
GF International will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of its investors, each of which is, to the best 
knowledge of GF International, an independent third party of GF International, GF Securities (Hong Kong) Brokerage and the companies which are members of the same 
group of GF Securities (Hong Kong) Brokerage. 
GF International is investing on behalf of certain collective investment schemes which are not authorized by the SFC, details of which are as follow: 
No.
Connected 
Distributor 
Connected 
Client 
Relationship 
Whether the 
connected client 
is a collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Whether the 
connected client will 
hold the beneficial 
interests of the Offer 
Shares on a non-
discretionary basis 
or discretionary 
basis for 
independent third 
parties 
Number of Offer 
Shares to be 
allocated to the 
Connected Client 
Approximate percentage 
of total number of Offer 
Shares under the Global 
Offering (after taking into 
account the full exercise of 
the Offer Size Adjustment 
Option and assuming no 
exercise of the Over-
allotment Option) 
Approximate percentage of 
total issued share capital 
immediately following the 
Global Offering (after taking 
into account the full exercise 
of the Offer Size Adjustment 
Option and assuming the 
Over-allotment Option is not 
exercised) 
Kong) Co., 
Limited 
(“CGIS”)
same group as 
CGIS. 
23.
SWHY HK 
SWHY (through 
GF Securities 
AM as the asset 
manager) Note 23
SWHY is a 
member of the 
same group as 
SWHY HK. 
N
Discretionary basis
15,000 
0.02% 
0.002% 

<<<PAGE 39>>>
39 
No. 
Fund name 
Types and values of 
assets under 
management 
Whether the 
scheme is 
publicly markets 
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
Identity of the 
scheme 
administrator 
Relationships 
among the 
scheme, the 
ultimate 
beneficial 
owner(s), GF 
Securities (Hong 
Kong) 
Brokerage and 
the Company 
1. 
GF Luminous Fund 
Private fund 
HK$229 million as of 
March 2026 
No 
November 2025 
Not applicable as 
it 
is 
not 
in 
partnership 
structure and does 
not 
have 
any 
general partner or 
limited partner 
NuBright Fund 
Services Limited
The scheme and 
ultimate 
beneficial owners 
are 
independent 
third parties of GF 
Securities (Hong 
Kong) Brokerage 
and the Company. 
2.  
GF Vision Fund 
Private fund 
HK$81 million as of 
March 2026 
No 
March 2026 
Not applicable as 
it 
is 
not 
in 
partnership 
structure and does 
not 
have 
any 
general partner or 
limited partner 
NuBright Fund 
Services Limited
The scheme and 
ultimate 
beneficial owners 
are 
independent 
third parties of GF 
Securities (Hong 
Kong) Brokerage 
and the Company. 
3. 
Golden Stone Fund 
Private fund 
HK$49 million as of 
March 2026 
No 
November 2025 
Not applicable as 
it 
is 
not 
in 
partnership 
structure and does 
not 
have 
any 
general partner or 
limited partner 
NuBright Fund 
Services Limited
The scheme and 
ultimate 
beneficial owners 
are 
independent 
third parties of GF 
Securities (Hong 
Kong) Brokerage 
and the Company. 
4. 
Golden 
Fortune 
Opportunity Fund 
Private fund 
US$5 million as of 
March 2026
No 
November 2013 
Not applicable as 
it 
is 
not 
in 
partnership 
structure and does 
ICBC 
(Asia) 
Trustee Company 
Limited 
The scheme and 
ultimate 
beneficial owners 
are 
independent 

<<<PAGE 40>>>
40 
not 
have 
any 
general partner or 
limited partner 
third parties of GF 
Securities (Hong 
Kong) Brokerage 
and the Company. 
5. 
GF Bonanza Fund 
Private fund 
HK$80 million as of 
April 2026 
No 
April 2026 
Not applicable as 
it 
is 
not 
in 
partnership 
structure and does 
not 
have 
any 
general partner or 
limited partner 
NuBright Fund 
Services Limited 
The scheme and 
ultimate 
beneficial owners 
are 
independent 
third parties of GF 
Securities (Hong 
Kong) Brokerage 
and the Company. 
3.
Each of VPHKL and VPL will hold the beneficial interests of the Offer Shares on a discretionary basis for and on behalf of its ultimate clients, each of whom is, to the 
best knowledge of VPHKL and VPL, an independent third party of VPHKL, VPL, GF Securities (Hong Kong) Brokerage and the companies which are members of the 
same group of GF Securities (Hong Kong) Brokerage. 
VPHKL and VPL are investing on behalf of certain collective investment schemes which are not authorized by the SFC, details of which are as follow: 
No. 
Fund name 
Types and values of 
assets under 
management 
Whether the 
scheme is 
publicly markets 
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
Identity of the 
scheme 
administrator 
Relationships 
among the 
scheme, the 
ultimate 
beneficial 
owner(s), GF 
Securities (Hong 
Kong) 
Brokerage and 
the Company 
1. 
Value Partners Funds 
SPC – Value Partners 
China 
A-Share 
Innovation Fund SP 
Private fund 
US$18 million as of 
December 31, 2025 
N 
March 2002 
Not applicable as 
it 
is 
not 
in 
partnership 
structure and does 
not 
have 
any 
general partner or 
limited partner 
HSBC 
Trustee 
(Cayman) Limited 
The scheme and 
ultimate 
beneficial owners 
are 
independent 
third parties of GF 
Securities (Hong 
Kong) Brokerage 
and the Company. 

<<<PAGE 41>>>
41 
2. 
Value Partners Ireland 
Fund ICAV – Value 
Partners Asia Ex-Japan 
Equity Fund 
ICAV public fund 
US$21 million as of 
December 31, 2025 
Y 
September 2018 
Not applicable as 
it 
is 
not 
in 
partnership 
structure and does 
not 
have 
any 
general partner or 
limited partner 
HSBC Securities 
Services (Ireland) 
DAC 
The scheme and 
ultimate 
beneficial owners 
are 
independent 
third parties of GF 
Securities (Hong 
Kong) Brokerage 
and the Company. 
3. 
Value 
Partners 
Intelligent Funds - JA-
VP China New Century 
Fund 
Private fund 
US$6 million as of 
December 31, 2025 
N 
March 2002 
Not applicable as 
it 
is 
not 
in 
partnership 
structure and does 
not 
have 
any 
general partner or 
limited partner 
HSBC Trustee 
(Cayman) 
Limited 
The scheme and 
ultimate 
beneficial owners 
are 
independent 
third parties of GF 
Securities (Hong 
Kong) Brokerage 
and the Company. 
4.
E Fund will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of its investors, each of which is, to the best knowledge 
of E Fund, an independent third party of E Fund, GF Securities (Hong Kong) Brokerage and the companies which are members of the same group of GF Securities (Hong 
Kong) Brokerage. 
5.
E Fund HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of its investors, each of which is, to the best 
knowledge of E Fund HK, an independent third party of E Fund HK, GF Securities (Hong Kong) Brokerage and the companies which are members of the same group of 
GF Securities (Hong Kong) Brokerage. 
6.
Each of the ultimate clients of GF Securities AM (the “GF Securities AM Ultimate Clients”) have engaged GF Securities AM, an asset manager that is qualified domestic 
institutional investor as approved by the relevant PRC authority to subscribe for and hold the Offer Shares as a placee under the International Offering on behalf of the 
GF Securities AM Ultimate Client on a non-discretionary basis. 
Details of the GF Securities AM Ultimate Clients are set out as below: 
Name of the GF Securities AM Ultimate Clients 
Name of the asset management plan 
Huizhou Huilian Investment Partnership (Limited Partnership) (惠州市惠聯投
資合夥企業(有限合夥)) 
GF Asset Management Hong Kong Equity Diversified Strategy No. 9 Single 
Asset Management Plan (廣發資管港股多元策略9 號單一資產管理計劃) 
Everbright Wealth Management Co., Ltd. 
GF Asset Management Guangshi Selective Strategy No. 1 Collective Asset 
Management Plan (廣發資管光石精選策略1 號集合資產管理計劃) 
Luhua Daosheng (Beijing) Enterprise Management & Development Co., Ltd. 
(魯花道生(北京)企業管理發展有限公司) 
GF Asset Management Hong Kong Equity Diversified Strategy No. 16 Single 
Asset Management Plan (廣發資管港股多元策略16 號單一資產管理計劃) 

<<<PAGE 42>>>
42 
Shenwan Hongyuan Group Co., Ltd. (申萬宏源集團股份有限公司) 
GF Asset Management Wanxiang No. 1 Single Asset Management Plan (廣發
資管萬享1 號單一資產管理計劃) 
ICBC WM 
GF Asset Management ICBC Selected Strategy No. 1 Collective Asset 
Management Plan (廣發資管工銀精選策略1 號集合資產管理計劃) 
7.
GFGC proposes to subscribe for and hold the Offer Shares as a placee under the International Offering on a non-discretionary basis. GFGC and GF Securities Co., Ltd. 
will enter into a series of cross border delta one OTC swap transactions (the “OTC Swaps”) with each other and the ultimate clients (the “GFGC Ultimate Clients”), 
pursuant to which GFGC will hold the Offer Shares on a non-discretionary basis to hedge the OTC Swaps while the economic risks and returns of the underlying Offer 
Shares are passed to the GFGC Ultimate Clients, subject to customary fees and commissions. The OTC swaps will be fully funded by the GFGC Ultimate Clients. During 
the terms of the OTC Swaps, all economic returns of the Offer Shares subscribed by GFGC will be passed to the GFGC Ultimate Clients and all economic loss shall be 
borne by the GFGC Ultimate Clients through the OTC Swaps, and GFGC will not take part in any economic return or bear any economic loss in relation to the Offer 
Shares. The OTC Swaps are linked to the Offer Shares and the GFGC Ultimate Clients may request GFGC to redeem it at their own discretions, upon which GFGC shall 
dispose of the Offer Shares and settle OTC Swaps in cash in accordance with the terms and conditions of the OTC Swap. Despite that GFGC will hold the legal title of 
the Offer Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares during the terms of the OTC Swaps according to its internal policy. 
Details of the GFGC Ultimate Clients are set out as below: 
Name of the GFGC Ultimate Clients 
Ultimate beneficial owner(s) holding 30% or more interest (if any) 
Yuemintou Xinxuan Opportunity No. 1 Private Securities Investment Fund (粵
民投新選機遇1 號私募證券投資基金) 
Liu Wei (劉偉) 
Infore Yingqi Private Securities Investment Fund (盈峰盈齊私募證券投資基
金) 
Xu Suying (許素英) and He Jianfeng (何劍鋒) 
Sichuan Puxin Industrial-Finance Investment Co., Ltd. (四川璞信產融投資有
限責任公司) 
Luzhou State-owned Assets Supervision and Administration Commission (瀘州
市國有資產監督管理委員會) 
To best of knowledge of GFGC after making all reasonable enquiries, each of the GFGC Ultimate Clients is an independent third party of GFGC, GF Securities (Hong 
Kong) Brokerage and the companies which are members of the same group of GF Securities (Hong Kong) Brokerage. 
8.
CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one OTC swap transactions (the “OTC Swaps”) with each 
other and the ultimate clients (the “CICC FT Ultimate Clients”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the OTC 
Swaps while the economic risks and returns of the underlying Offer Shares are passed to the CICC FT Ultimate Clients, subject to customary fees and commissions. The 
OTC Swaps will be fully funded by the CICC FT Ultimate Clients. During the terms of the OTC Swaps, all economic returns of the Offer Shares subscribed by CICC FT 
will be passed to the CICC FT Ultimate Clients and all economic loss shall be borne by the CICC FT Ultimate Clients through the OTC Swaps, and CICC FT will not 
take part in any economic return or bear any economic loss in relation to the Offer Shares. The OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate 
Clients may request CICC FT to redeem it at their own discretions, upon which CICC FT shall dispose of the Offer Shares and settle OTC Swaps in cash in accordance 
with the terms and conditions of the OTC Swap. Despite that CICC FT will hold the legal title of the Offer Shares by itself, it will not exercise the voting rights attaching 
to the relevant Offer Shares during the terms of the OTC Swaps according to its internal policy. The CICC FT Ultimate Clients for purpose of this placee subscription 
include Changjiang Jin (金長江), Chengyi Liu (劉承毅), Yashuang Chen (陳亞雙), Peiwu Shan (單佩武), Hongyun Lin (林紅雲) and Gangqiang Zhang (張剛強), each 
of which is an independent third party of CICC FT, CICC and the companies which are members of the same group of companies as each of the Underwriters. 

<<<PAGE 43>>>
43 
9.
ABCI AM intends to hold the Offer Shares in its capacity as manager managing investment portfolios on behalf of underlying investors on a discretionary basis. To best 
of knowledge of ABCI AM after making all reasonable enquiries, each of the underlying investors is an independent third party of ABCI AM, ABCI and the companies 
which are members of the same group of ABCI. 
10.
HTFH is an Underwriter in connection with the Global Offering. Pursuant to an ISDA Agreement (the “ISDA Agreement”), HTCI, which intends to participate in the 
Global Offering as a placee, will hold the beneficial interest of the Offer Shares on a non-discretionary basis as the single underlying holder under a back-to-back total 
return swap (the “Back-to-back TRS”) to be entered by HTCI in connection with a Client TRS (as defined below) placed by and fully funded (i.e. with no financing 
provided by HTCI) by the Huatai Offshore Ultimate Clients (as defined below), by which, HTCI will, subject to customary fees and commissions, pass the full 
economic exposure of the Offer Shares to the Huatai Offshore Ultimate Clients, which in effect, HTCI will hold the beneficial interest of the Offer Shares on behalf 
of the Huatai Offshore Ultimate Clients. Accordingly, HTCI is considered as a “connected client” of HTFH pursuant to paragraph 1B(7) of the Placing Guidelines. 
Each of the offshore investors (the “Huatai Offshore Ultimate Clients”), through its investment manager, will place a total return swap order (the “Client TRS”) 
with HTCI in connection with the Global Offering. In order to hedge its exposure under the Client TRS, HTCI participates in the Global Offering and subscribes the 
Offer Shares through placing order with HTFH during the International Offering. 
To the best of HTCI’s knowledge and after making all reasonable enquiries, each of the Huatai Offshore Ultimate Clients is an independent third party of HTCI, HTFH 
and the companies which are members of the same group of HTCI. 
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Client TRS order placed by the Huatai Offshore Ultimate Clients. Pursuant to the terms of 
the Client TRS, during the tenor of the Client TRS, subject to customary fees and commissions, all economic returns of the Offer Shares will be passed to the Huatai 
Offshore Ultimate Clients through the Client TRS and all economic loss shall be borne by the Huatai Offshore Ultimate Clients. HTCI will not take any economic 
return or bear any economic loss in relation to the Offer Shares.  
The Huatai Offshore Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time from the issue date of the Client TRS which 
should be on or after the date on which the Offer Shares are listed on the Stock Exchange at its own discretion. Upon the termination upon maturity or early termination 
of the Client TRS by the Huatai Offshore Ultimate Clients, HTCI will dispose the Offer Shares on the secondary market and the Huatai Offshore Ultimate Clients will 
receive a final settlement amount of the Client TRS in cash in accordance with the terms and conditions of the Client TRS which should have taken into account all 
the economic returns or economic loss in relation to the Offer Shares. If upon the maturity of the Client TRS, the Huatai Offshore Ultimate Clients intend to extend 
the investment period, subject to further agreement between HTCI and the relevant Huatai Offshore Ultimate Clients, the term of the Client TRS could be extended 
by way of a new issuance or a tenor extension.  
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through the economic exposure to each of the Huatai 
Offshore Ultimate Clients, being a client who places a Client TRS order with HTCI in connection with the Global Offering. HTCI will not exercise the voting right of 
the Offer Shares during the tenor of the Client TRS. 
During the life of the Client TRS, HTCI may continue to hold the Offer Shares in its custodian account, or to hold some or all of the Offer Shares in a prime brokerage 
account for stock borrowing purposes, where HTCI will lend out its holding of underlying Offer Shares in the form of stock borrowing loans consistent with market 
practice to lower its finance costs, provided that HTCI has the ability to call back the Offer Shares on loan at any time in order to satisfy its obligations under the Client 
TRS to ensure the economic interests are ultimately passed to the Huatai Offshore Ultimate Clients. 

<<<PAGE 44>>>
44 
Details of the Huatai Offshore Ultimate Clients are set out as below: 
Name of the Huatai Offshore Ultimate Clients 
Ultimate beneficial owner(s) holding 30% or more interest (if any) 
ZHONG HENG CAPITAL LIMITED 
Lan Dong (藍棟) 
KSICN SP2 
Zhu Lei (朱磊) 
CHEN HAN (陳晗) 
CHEN HAN (陳晗) 
Jindan Ocean No. 6 Private Securities Investment Fund (金澹遠洋6 號私募證
券投資基金) 
Ding Hai (丁海) 
11.
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public offerings (“IPOs”) in Hong Kong. However, PRC investors 
are permitted to invest in products issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. In connection with 
such products, the licensed domestic securities firms, through their Hong Kong affiliates, may participate in Hong Kong IPOs either as placees or cornerstone investors 
(the “Cross-border Derivatives Trading Regime”). 
Huatai Securities Co., Ltd. (“Huatai Securities”), the shares of which are listed on both the Shanghai Stock Exchange (stock code: 601688) and the Stock Exchange 
(stock code: 6886), is one of the domestic securities firms licensed to undertake cross-border derivatives trading activities. Huatai Securities entered into an ISDA 
agreement (the “ISDA Agreement”) with its indirectly wholly-owned subsidiary, HTCI to set out the principal terms of any future total return swap between Huatai 
Securities and HTCI. 
HTFH is an Underwriter in connection with the Global Offering. Pursuant to the ISDA Agreement, HTCI, which intends to participate in the Global Offering as a placee, 
will hold the beneficial interest of the Offer Shares on a non-discretionary basis as the single underlying holder under a back-to-back total return swap (the “Back-to-
back TRS”) to be entered by HTCI in connection with a Client TRS (as defined below) placed by and fully funded (i.e. with no financing provided by HTCI) by the 
Huatai Onshore Ultimate Clients (as defined below), by which, HTCI will, subject to customary fees and commissions, pass the full economic exposure of the Offer 
Shares ultimately to the Huatai Onshore Ultimate Clients, which in effect, HTCI will hold the beneficial interest of the Offer Shares on behalf of the Huatai Onshore 
Ultimate Clients. HTFH and HTCI are indirectly wholly-owned subsidiaries of Huatai Securities. Accordingly, HTCI is considered as a “connected client” of HTFH 
pursuant to paragraph 1B(7) of the Placing Guidelines. 
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the “Huatai Onshore Ultimate Clients”) cannot directly subscribe for the Offer Shares 
but may invest in derivative products issued by domestic securities firms licenced to undertake cross-border derivatives trading activities, such as Huatai Securities, with 
the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, each of the Huatai Onshore Ultimate Clients, through its investment manager, 
will place a total return swap order (the “Client TRS”) with Huatai Securities in connection with the Company’s IPO and Huatai Securities will place a Back-to-back 
TRS order to HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the Back-to-back TRS, HTCI participates in the Company’s IPO and 
subscribes the Offer Shares through placing order with HTFH during the International Offering. The Huatai Onshore Ultimate Clients for purpose of this placee 
subscription include the investment fund. 
To the best of HTCI’s knowledge and after making all reasonable enquiries, each of the Huatai Onshore Ultimate Clients is an independent third party of HTCI, HTFH 
and the companies which are members of the same group of HTCI. 
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in connection with the Client TRS order placed by the Huatai Onshore 
Ultimate Clients. Pursuant to the terms of the contracts of the Back-to-back TRS and the Client TRS, during the tenor of the Back-to-back TRS and the Client TRS, subject 

<<<PAGE 45>>>
45 
to customary fees and commissions, all economic returns of the Offer Shares will be ultimately passed to the Huatai Onshore Ultimate Clients through the Back-to-back 
TRS and the Client TRS and all economic loss shall be ultimately borne by the Huatai Onshore Ultimate Clients. HTCI will not take any economic return or bear any 
economic loss in relation to the Offer Shares. 
Investment in the Back-to-back TRS and the Client TRS is similar to the investment in a qualified domestic institutional investor fund (“QDII”) in the way that the Huatai 
Onshore Ultimate Clients would reap all the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through the exchange rate exposure 
on both the notional value of the investment and the profit and loss of the investment. In contrast, the profit and loss of the Back-to-back TRS and the Client TRS factor 
into account the fluctuation in RMB exchange rate upon termination of the Client TRS by converting the profit and loss using the current exchange rate at the time of 
termination. As such, the Huatai Onshore Ultimate Clients would bear the exchange rate exposure of the profit and loss on settlement date.  
The Huatai Onshore Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time from the issue date of the Client TRS which should 
be on or after the date on which the Offer Shares are listed on the Stock Exchange at their own discretion. Upon the termination upon maturity or early termination of the 
Client TRS by the Huatai Onshore Ultimate Clients, HTCI will dispose the Offer Shares on the secondary market and the Huatai Onshore Ultimate Clients will receive a 
final settlement amount in cash in accordance with the terms and conditions of the Back-to-back TRS and the Client TRS which should have taken into account all the 
economic returns or economic loss in relation to the Offer Shares. If upon the maturity of the Client TRS, the Huatai Onshore Ultimate Clients intend to extend the 
investment period, subject to further agreement between Huatai Securities and the relevant Huatai Onshore Ultimate Clients, the term of the Client TRS could be extended 
by way of a new issuance or a tenor extension. Accordingly, Huatai Securities will extend the term of the Back-to-back TRS by way of a new issuance or a tenor extension. 
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through the economic exposure to the Huatai Onshore Ultimate 
Clients, each being an onshore client who places a Client TRS order with Huatai Securities in connection with the IPO of the Company. HTCI will not exercise the voting 
right of the Offer Shares during the tenor of the Back-to-back TRS. 
During the life of the Client TRS and Back-to-back TRS, HTCI may continue to hold the Offer Shares in its custodian account, or to hold some or all of the Offer Shares 
in a prime brokerage account for stock borrowing purposes, where HTCI will lend out its holding of underlying Offer Shares in the form of stock borrowing loans 
consistent with market practice to lower its finance costs, provided that HTCI has the ability to call back the Offer Shares on loan at any time in order to satisfy its 
obligations under the Back-to-back TRS to ensure the economic interests are ultimately passed to the Huatai Onshore Ultimate Clients. 
Details of the Huatai Onshore Ultimate Clients are set out as below: 
Name of the Huatai Onshore Ultimate Clients 
Ultimate beneficial owner(s) holding 30% or more interest (if any) 
Greenwoods Harvest No. 2 Fund (景林豐收2 號基金) 
N/A 
Greenwoods Harvest No. 3 Private Equity Fund (景林豐收3 號私募基金) 
N/A 
Greenwoods Harvest No. 6 Private Securities Investment Fund (景林豐收6 號
私募證券投資基金) 
N/A 
Greenwoods Jingtai Harvest Private Securities Investment Fund (景林景泰豐收
私募證券投資基金) 
N/A 
Roadshow Red Deer No. 4 Private Securities Investment Fund (鹿秀馬鹿4 號
私募證券投資基金) 
N/A 

<<<PAGE 46>>>
46 
Gaoyi Guolu Xinyuan Private Securities Investment Fund (高毅國鷺信遠私募
證券投資基金) 
N/A 
Gaoyi Qingrui No. 6 Ruixing Fund (高毅慶瑞6 號瑞行基金) 
N/A 
Gaoyi Qingrui Selected Fengyuan Private Securities Investment Fund (高毅慶
瑞臻選灃源私募證券投資基金) 
N/A 
Gaoyi Renhao Premium Zhifu Private Securities Investment Fund (高毅任昊優
選致福私募證券投資基金) 
N/A 
Gaoyi Renhao Long-term Value Langrun Private Securities Investment Fund 
(高毅任昊長期價值朗潤私募證券投資基金) 
N/A 
Gaoyi Renhao Selected Chunhe Private Securities Investment Fund (高毅任昊
臻选春和私募证券投资基金) 
N/A 
Gaoyi Renhao Choice Chengze Private Securities Investment Fund (高毅任昊
精選承澤私募證券投資基金) 
N/A 
Gaoyi-Xiaofeng No. 1 Ruiyuan Securities Investment Fund (高毅-曉峰1 號睿
遠證券投資基金) 
N/A 
Gaoyi Xiaofeng No. 2 Zhixin Fund (高毅曉峰2 號致信基金) 
N/A 
Jintaiyang Gaoyi Guolu No. 1 Chongyuan Fund (金太陽高毅國鷺1 號崇遠基
金) 
N/A 
12.
China Southern, a qualified domestic institutional investor as approved by the relevant PRC authority to conduct asset management business, will hold the Offer Shares 
as the independent agent and discretionary manager of certain QDII funds. China Southern has confirmed that, to the best of their knowledge, each of such underlying 
clients are independent third parties of China Southern, HTFH and the companies which are members of the same group of companies as HTFH. 
13.
Each of CMBI and CMS HK is a distributor of the Global Offering. Bosera International intends to subscribe and hold the Offer Shares in its capacity as the discretionary 
fund manager on behalf of its sub-funds, which are all independent third parties. To the best knowledge of Bosera International after due enquiry, each of the sub-funds 
and their respective ultimate beneficial owner holding 30% or more interest is an independent third party of Bosera International, CMBI and CMS HK, and the companies 
which are members of the same group of CMBI and CMS HK. 
Details of the sub-funds are set out as below: 
Name of the sub-funds 
Ultimate beneficial owner(s) holding 30% or more interest (if any) 
Bosera Global Select Equity Fund SP 
Zhang Lei (張雷) 
Bosera China New Opportunities Fund SP
N/A
Bosera Growth Premium Global Equity Strategy Fund SP 
Guo Feng (郭峰) 
KB CHINA MAINLAND FD BOSERA
N/A
Bosera Growth Premium Global Equity Strategy Fund SP2
N/A
Bosera Growth Premium Global Equity Strategy Fund SP3
Huang Liya (黃麗亞) 

<<<PAGE 47>>>
47 
14.
GTJA FP shall hold the Offer Shares on a non-discretionary basis for hedging purposes as the single underlying asset of a delta one back-to-back total return swap 
transaction (the “GTJA Back-to-back TRS1”) to be entered into between GTJA FP and Guotai Junan Investments (Hong Kong) Limited (“GTJA INV”), and GTJA 
INV shall for hedging purposes enter into a cross-border delta one back-to-back total return swap transaction (the “GTJA Back-to-back TRS2”) with Guotai Haitong 
Securities Co., Ltd. (“GTHTS”), in connection with a total return swap order (the “GTHT Client TRS”) to be entered into by GTHTS and the GTHTS onshore clients 
(the “GTHT Onshore Clients”). Such GTHT Client TRS is to be fully funded by the GTHT Onshore Clients. The full economic exposure of the Offer Shares will be 
passed from GTJA FP to GTJA INV under the GTJA Back-to-back TRS1, from GTJA INV to GTHTS under the GTJA Back-to-back TRS2, and ultimately from GTHTS 
to the GTHT Onshore Clients under the GTHT Client TRS. The GTHT Onshore Clients may exercise an early termination right to early terminate the GTHT Client TRS 
at any time from the trade date of the GTHT Client TRS, which should be on or after the date on which the Offer Shares are listed on the Stock Exchange. Accordingly, 
(i) GTHTS may exercise an early termination right to early terminate the GTJA Back-to-back TRS2 at any time from the trade date of the GTJA Back-to-back TRS2, and 
(ii) GTJA INV may exercise an early termination right to early terminate the GTJA Back-to-back TRS1 at any time from the trade date of the GTJA Back-to-back TRS1, 
which in each case should be on or after the date on which the Offer Shares are listed on the Stock Exchange. Upon the final maturity or early termination of (i) the GTHT 
Client TRS by the GTHT Onshore Clients, (ii) the GTJA Back-to-back TRS2 by GTHTS, and (iii) the GTJA Back-to-back TRS1 by GTJA INV, GTJA FP will dispose 
the Offer Shares on the secondary market and the GTHT Onshore Clients ultimately will receive a final termination amount of the GTHT Client TRS, which should have 
taken into account all the economic returns or economic loss in relation to the Offer Shares, the fixed amount in relation to the GTJA Back-to-back TRS1, the GTJA Back-
to-back TRS2 and the GTHT Client TRS. GTJA FP will hold the legal title and the voting right of the Offer Shares by itself and pass through the economic exposure to 
GTJA INV, GTHTS and ultimately the GTHT Onshore Clients. Due to its internal policy, GTJA FP will not exercise the voting right of the Offer Shares during the tenor 
of the GTJA Back-to-back TRS1 and GTJA Back-to-back TRS2. To the best of GTJA FP’s knowledge having made all reasonable inquiries, each of the GTHT Onshore 
Clients is an independent third party of GTJA FP, GTJA INV and GTHTS and the companies which are members of the same group of each of them. 
Details of the GTHT Onshore Clients are set out as below: 
Name of the GTHT Onshore Clients 
Ultimate beneficial owner(s) holding 30% or more interest (if any) 
Roadshow Giraffe No. 5 Private Securities Investment Fund (鹿秀長頸鹿5 號
私募證券投資基金) 
N/A 
Roadshow Reindeer No. 15 Private Securities Investment Fund (鹿秀馴鹿15 號
私募證券投資基金) 
N/A 
Roadshow Reindeer No. 65 Private Securities Investment Fund (鹿秀馴鹿65 號
私募證券投資基金) 
N/A 
Yongguan Xinrui No. 1 Private Securities Investment Fund (永冠新瑞1 號私募
證券投資基金) 
Luo Chanfang (羅嬋芳) 
Among the GTHT Onshore Clients, the ultimate beneficial owners of Roadshow Giraffe No. 5 Private Securities Investment Fund, Roadshow Reindeer No. 15 Private 
Securities Investment Fund and Roadshow Reindeer No. 65 Private Securities Investment Fund are the 145 PRC Eligible Employees under the PRC Employee Preferential 
Offering. 7,501,300 Offer Shares have been placed to the PRC Eligible Employees pursuant to the PRC Employee Preferential Offering, and the maximum subscription 
amount of the Offer Shares that each individual PRC Eligible Employee applied for under the PRC Employee Preferential Offering is not more than RMB20 million 
(excluding the brokerage, SFC transaction levy, Stock Exchange trading fee and AFRC transaction levy). 
15.
HuaAn will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of its underlying client. The underlying client is an 
independent third party of HuaAn, GTJA HK, HTI and the companies which are members of the same group of companies as GTJA HK and HTI. 

<<<PAGE 48>>>
48 
16.
Fullgoal Fund and Fullgoal HK will hold the Offer Shares on a discretionary basis on behalf of its underlying clients. To the best of their knowledge, each of the underlying 
clients are independent third parties of Fullgoal Fund, Fullgoal HK, GTJA HK, HTI, SWHY HK and the companies which are members of the same group of companies 
as GTJA HK, HTI and SWHY HK. 
17.
ICBC UBS and ICBC UBS (International) will hold the Offer Shares in its capacity as the discretionary fund manager on behalf of certain funds, who are independent 
third parties of ICBC UBS, ICBC UBS (International), UBS HK, UBS SG and the companies which are members of the same group of UBS HK and UBS SG.  
18.
UBS AM Singapore will hold the beneficial interests of the Offer Shares on a discretionary basis for and on behalf of the underlying clients. To the best knowledge of 
UBS AM Singapore, each of the underlying clients is an independent third party of UBS AM Singapore, UBS HK, UBS SG and the companies which are members of the 
same group of UBS HK and UBS SG. 
19.
BOC AM proposed to subscribe for and hold the Offer Shares as a placee under the International Offering in its capacity as the investment manager for and on behalf of 
the underlying clients. To the best knowledge of BOC AM, each of the underlying clients is an independent third party of BOC AM, BOCI and the companies which are 
members of the same group of BOCI. 
20.
JPM AM will hold the Offer Shares in its capacity as the discretionary fund manager managing assets on behalf of its underlying clients. Each of the underlying clients 
of JPM AM is an independent third party of JPM AM, JPM SAPL, JPM Chase and the companies which are members of the same group of JPM SAPL and JPM Chase. 
21.
SR Wealth is a distributor of the Global Offering in the capacity of a licence holder of Type 1 (dealing in securities) regulated activities under the SFO. SR Wealth acts 
as the investment manager for and on behalf of retail clients and professional investors on discretionary basis in the capacity of a licence holder of Type 9 (asset 
management) regulated activities under the SFO. Each of the aforementioned retail clients and professional investors of SR Wealth is an independent third party of SR 
Wealth and the companies which are members of the same group of companies as SR Wealth. 
22.
CGII and China Galaxy Securities (“CGS”) will enter into a series of cross border total return swap (TRS) transactions (collectively, the “CGII TRS”) with each other 
and the ultimate clients (“CGII Ultimate Clients”), pursuant to which CGII will hold the Offer Shares on a non-discretionary basis to hedge the CGII TRS while the 
economic risks and returns of the underlying Offer Shares are ultimately borne by the CGII Ultimate Clients, subject to customary fees and commissions. The CGII TRS 
will be fully funded by the CGII Ultimate Clients. During the terms of the CGII TRS, all economic returns of the Offer Shares subscribed by CGII will be passed to CGII 
Ultimate Clients and all economic loss shall be borne by CGII Ultimate Clients through the CGII TRS, and CGII will not take part in any economic return or bear any 
economic loss in relation to the Offer Shares. The CGII TRS are linked to the Offer Shares and CGII Ultimate Clients may, after expiration of the lock-up period beginning 
from the date of the relevant cornerstone agreements and ending on the date which is six months from the Listing Date, request to early terminate the CGII TRS at its own 
discretion, upon which CGII may dispose of the Offer Shares on the secondary market and CGII Ultimate Clients will receive a final settlement amount of the CGII TRS 
in cash in accordance with the terms and conditions of the CGII TRS. 
To the best of CGII’ s knowledge after having made all reasonable inquiries, each of the CGII Ultimate Clients is an independent third party of CGII, CGIS and the 
companies which are members of the same group of CGIS. 
Details of the CGII Ultimate Clients are set out as below: 
Name of the CGII Ultimate Clients 
Ultimate beneficial owner(s) holding 30% or more interest (if any) 

<<<PAGE 49>>>
49 
Yuanfeng Value Private Securities Investment Fund (源峰價值私募證券投資
基金) 
N/A 
Yuanfeng Wenjian Private Securities Investment Fund (源峰穩健私募證券投
資基金) 
N/A 
Yuanfeng Hongyu Private Securities Investment Fund (源峰泓聿私募證券投資
基金) 
Zhou Yong (周勇) 
23.
SWHY will hold the Offer Shares on a discretionary basis on behalf of its underlying clients. To the best knowledge of SWHY after due enquiry, each of the underlying 
clients of SWHY is an independent third party of SWHY, SWHY HK and the companies which are members of the same group of companies as SWHY HK. 

<<<PAGE 50>>>
50 
Allocations under the Overseas Employee Preferential Offering 
Of the 8,334,800 Offer Shares initially being offered under the Hong Kong Public Offering, no more 
than 833,400 Offer Shares, representing approximately 10% of the Offer Shares initially available for 
subscription under the Hong Kong Public Offering, are available for subscription as Overseas 
Employee Reserved Shares by the Overseas Eligible Employees on a preferential basis under the 
Overseas Employee Preferential Offering according to Rule 10.01 of the Listing Rules. For details, 
please refer to the section headed “Structure of the Global Offering – The Overseas Employee 
Preferential Offering” of the Prospectus. 
482,000 Offer Shares have been allocated to 46 Overseas Eligible Employees pursuant to the Overseas 
Employee Preferential Offering, representing approximately 0.50% of the total number of Offer Shares 
available under the Global Offering (after taking into account the full exercise of the Offer Size 
Adjustment Option and before exercise of the Over-allotment Option). Of the 482,000 Offer Shares 
allocated to the Overseas Eligible Employees, 270,000 Offer Shares were placed to six Eligible Core 
Connected Person Participants, representing approximately 0.28% of the total number of Offer Shares 
available under the Global Offering (after taking into account the full exercise of the Offer Size 
Adjustment Option and before exercise of the Over-allotment Option). 
Allocations under the PRC Employee Preferential Offering 
Of the 75,013,200 Offer Shares initially being offered under the International Offering, no more than 
7,501,300 Offer Shares, representing approximately 10% of the Offer Shares initially available for 
subscription under the International Offering, are available for subscription as PRC Employee 
Reserved Shares by the PRC Eligible Employees on a preferential basis under the PRC Employee 
Preferential Offering according to Rule 10.01 of the Listing Rules. For details, please refer to the 
section headed “Structure of the Global Offering – The PRC Employee Preferential Offering” of the 
Prospectus. 
7,501,300 Offer Shares have been placed to 145 PRC Eligible Employees pursuant to the PRC 
Employee Preferential Offering, representing approximately 7.83% of the total number of Offer Shares 
available under the Global Offering (after taking into account the full exercise of the Offer Size 
Adjustment Option and before exercise of the Over-allotment Option). Of the 7,501,300 Offer Shares 
placed to the PRC Eligible Employees, 175,032 Offer Shares were placed to two Eligible Core 
Connected Person Participants, representing approximately 0.18% of the total number of Offer Shares 
available under the Global Offering (after taking into account the full exercise of the Offer Size 
Adjustment Option and before exercise of the Over-allotment Option), respectively. 

<<<PAGE 51>>>
51 
DISCLAIMERS 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong 
Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
This announcement is not for release, publication or distribution, directly or indirectly, in or into the 
United States (including its territories and possessions, any state of the United States and the District 
of Columbia or any other jurisdiction where such distribution is prohibited by laws). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe 
for securities in the United States or in any other jurisdictions. The securities mentioned herein have 
not been, and will not be, registered under the United States Securities Act of 1933 as amended from 
time to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the 
United States. The securities may not be offered, sold, pledged or otherwise transferred within the 
United States except pursuant to an exemption from the registration requirements of the U.S. Securities 
Act and in compliance with any applicable state securities laws. The Offer Shares may be offered, sold 
or delivered (a) in the United States solely to QIBs in reliance on Rule 144A or another exemption 
from, or in a transaction not subject to, the registration requirements of the U.S. Securities Act or (b) 
outside the United States in offshore transactions in reliance on Regulation S.
This announcement is for information purposes only and does not constitute an invitation or offer to 
acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated April 13, 2026 issued by Victory Giant Technology 
(HuiZhou) Co., Ltd. for detailed information about the Global Offering described below before 
deciding whether or not to invest in the Offer Shares thereby being offered.
*Potential investors of the Offer Shares should note that the Sole Sponsor and the Sponsor-Overall 
Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate 
their obligations under the Hong Kong Underwriting Agreement with immediate effect upon the 
occurrence of any of the events set out in the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently 
expected to be on April 21, 2026).

<<<PAGE 52>>>
52 
PUBLIC FLOAT AND FREE FLOAT 
Immediately after the completion of the Global Offering (after taking into account the full exercise of 
the Offer Size Adjustment Option and before any exercise of the Over-allotment Option), the total 
market value of the H Shares expected to be held by the public is expected to be approximately 
HK$20,023.59 million, calculated based on the final Offer Price of HK$209.88, which is higher than 
the prescribed expected market value of H Shares required to be held in public hands of not less than 
HK$3,000,000,000 under Rule 19A.13A(2)(b) of the Listing Rules, thereby satisfying Rule 
19A.13A(2) of the Listing Rules. 
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the Listing 
Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be counted 
towards the free float of the H Shares of the Company at the time of Listing. Based on the final Offer 
Price of HK$209.88 per H Share, the Company confirmed that it complies with the free float 
requirement under Rule 19A.13C(2)(b) of the Listing Rules. 
The Directors confirm that, immediately following completion of the Global Offering (after taking 
into account the full exercise of the Offer Size Adjustment Option and before any exercise of the Over-
allotment Option): (i) the Shares will be held by at least 300 Shareholders at the time of Listing, in 
compliance with Rule 8.08(2) of the Listing Rules; (ii) the three largest public Shareholders will not 
hold more than 50% of the H Shares held in public hands at the time of Listing, in compliance with 
Rules 8.08(3) and 8.24 of the Listing Rules; (iii) no placee will, individually, be placed more than 10% 
of the enlarged issued share capital of the Company immediately after the Global Offering; and (iv) 
there will not be any new substantial Shareholder (as defined in the Listing Rules) immediately after 
the Global Offering. 
COMMENCEMENT OF DEALINGS 
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, April 21, 
2026 (Hong Kong time), provided that the Global Offering has become unconditional and the right of 
termination described in the section headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has not been 
exercised. Investors who trade the H Shares on the basis of publicly available allocation details prior 
to the receipt of H Share certificates or prior to the H Share certificates becoming valid evidence of 
title do so entirely at their own risk. 
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Tuesday, April 
21, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange will 
commence at 9:00 a.m. on Tuesday, April 21, 2026 (Hong Kong time). The H Shares will be traded in 
board lots of 100 H Shares each, and the stock code of the H Shares will be 2476. 
By order of the Board
Victory Giant Technology (HuiZhou) Co., Ltd.
Mr. Chen Tao 
Chairman of the Board and Executive Director
Hong Kong, April 20, 2026 
As of the date of this announcement, the Board comprises: (i) Mr. Chen Tao, Mr. Zhao Qixiang, Mr. 
Chen Yong and Ms. Wang Haiyan as executive Directors; (ii) Ms. Liu Chunlan as a non-executive 

<<<PAGE 53>>>
53 
Director; (iii) Mr. Xie Lanjun, Dr. Xie Lingmin and Dr. Zhang Jihai as independent non-executive 
Directors; and (iv) Mr. Wong Ting Chung as a proposed independent non-executive Director. 
