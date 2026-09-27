# 配发结果公告抽取任务：2475.HK Luxshare Precision Industry Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**08/07/2026 22:31**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0708/2026070801342.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2475.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock 
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for 
the contents of this announcement, make no representation as to its accuracy or completeness and expressly 
disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not, and is not intended to, constitute or form a part of any offer to sell or 
solicitation to purchase or subscribe for any securities in the United States or in any other jurisdiction. The 
Offer Shares have not been, and will not be, registered under the U.S. Securities Act of 1933, as amended 
from time to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the 
United States. The Offer Shares may not be offered, sold, pledged or otherwise transferred within the United 
States, except pursuant to an available exemption from, or in a transaction not subject to, the registration 
requirements of the U.S. Securities Act and in compliance with any applicable state securities laws. There 
will be no public offer of the Offer Shares in the United States. The Offer Shares are being offered and sold 
solely outside the United States in offshore transactions in reliance on Regulation S under the U.S. Securities 
Act.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for any securities. This announcement is not a prospectus. Potential investors should 
read the prospectus dated June 30, 2026 (the “Prospectus”) issued by Luxshare Precision Industry Co., 
Ltd. (立訊精密工業股份有限公司) (the “Company”) for detailed information about the Company and the 
Global Offering described below before deciding whether or not to invest in the Offer Shares.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings 
as those defined in the Prospectus.
In connection with the Global Offering, Goldman Sachs (Asia) L.L.C., as stabilizing manager (the 
“Stabilizing Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, to 
the extent permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, may 
over-allocate or effect transactions with a view to stabilizing or maintaining the market price of the H Shares 
at such price, in such amounts and in such manners as the Stabilizing Manager, its affiliates or any person 
acting for it may determine and at a level higher than that which might otherwise prevail for a limited 
period after the Listing Date. However, there is no obligation on the Stabilizing Manager (or its affiliates 
or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will 
be conducted at the absolute discretion of the Stabilizing Manager (or its affiliates or any person acting 
for it) and in what the Stabilizing Manager reasonably regards as the best interest of the Company, (b) may 
be discontinued at any time and (c) is required to be brought to an end within 30 days of the last day for 
lodging applications under the Hong Kong Public Offering (which is Wednesday, August 5, 2026). Such 
stabilizing action, if taken, may be effected in all jurisdictions where it is permissible to do so, in each case in 
compliance with all applicable laws, rules and regulatory requirements, including the Securities and Futures 
(Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities 
and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
- 1 -

<<<PAGE 2>>>
Potential investors should be aware that no stabilizing action can be taken to support the price of the H 
Shares for longer than the stabilization period, which will begin on the Listing Date, and is expected to expire 
on the 30th day after the last day for lodging applications under the Hong Kong Public Offering (which is 
Wednesday, August 5, 2026). After this date, when no further stabilizing action may be taken, demand for the 
H Shares, and therefore the price of the H Shares, could fall.
Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators 
(for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section 
headed “Underwriting — Underwriting Agreements — Hong Kong Underwriting Agreement — Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which 
is currently expected to be on Thursday, July 9, 2026).
- 2 -

<<<PAGE 3>>>
Luxshare Precision Industry Co., Ltd.
立訊精密工業股份有限公司
(a joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
383,472,800 H Shares (subject to 
the Over-allotment Option)
Number of Hong Kong Offer Shares
:
38,347,300 H Shares
Number of International Offer Shares
:
345,125,500 H Shares (subject to the 
Over-allotment Option)
Final Offer Price
:
HK$63.28 per H Share, plus brokerage 
of 1.0%, SFC transaction levy of 
0.0027%, AFRC transaction levy of 
0.00015% and Stock Exchange trading 
fee of 0.00565% (payable in full on 
application in Hong Kong dollars and 
subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
2475
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
- 3 -

<<<PAGE 4>>>
LUXSHARE PRECISION INDUSTRY CO., LTD. 
立訊精密工業股份有限公司 
ANNOUNCEMENT OF FINAL OFFER PRICE AND 
ALLOTMENT RESULTS 
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings 
as those defined in the prospectus dated June 30, 2026 (the “Prospectus”) issued by Luxshare Precision 
Industry Co., Ltd. (the “Company”).  
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could move 
substantially even with a small number of H Shares traded and should exercise extreme caution when 
dealing in the H Shares. 
SUMMARY 
Company information 
Stock code 
2475 
Stock short name 
LUXSHARE ICT 
Dealings commencement date 
July 9, 2026* 
*see note at the end of the announcement
Price Information 
Final Offer Price 
HK$63.28 
Maximum Offer Price 
HK$63.28 
Offer Shares and Share Capital 
Number of Offer Shares 
383,472,800 
Final Number of Offer Shares in Hong Kong Public Offering 38,347,300 
Final Number of Offer Shares in International Offering 
345,125,500 
Number of issued shares upon Listing (before exercise of the 
Over-allotment Option) 
7,701,730,624 
Over-allocation 
No. of Offer Shares over-allocated 
57,520,900 
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases 
in the secondary market at prices that do not exceed the Offer Price or through deferred delivery or a 
combination of these means. In the event the Over-allotment Option is exercised, an announcement will 
be made on the Stock Exchange’s website. 
Proceeds 
Gross proceeds (Note) 
HK$24,266.2 million 
Less: Estimated listing expenses payable based on Final 
Offer Price  
HK$(227.1) million 
Net proceeds 
HK$24,039.1 million 
Note: Gross proceeds refer to the amount to which the Company is entitled to receive. For details of the use 
of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis. 
- 4 -

<<<PAGE 5>>>
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING 
No. of valid applications 
47,308 
No. of successful applications 
47,308 
Subscription level 
3.78 times 
Claw-back triggered 
N/A 
No. of Offer Shares initially available under the Hong Kong Public 
Offering 
38,347,300 
Final no. of Offer Shares under the Hong Kong Public Offering 
38,347,300 
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering 
10.00% 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by name or identification number or www.hkeipo.hk/IPOResult 
for the full list of allottees. 
INTERNATIONAL OFFERING 
No. of placees 
294 
Subscription Level 
9.46 times 
No. of Offer Shares initially available under the International 
Offering 
345,125,500 
Final no. of Offer Shares under the International Offering (before 
exercise of the Over-allotment Option) 
345,125,500 
% of Offer Shares under the International Offering to the Global 
Offering 
90.00% 
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a waiver from 
strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) of Appendix F1 
to the Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange to permit H Shares in the 
International Offering to be placed to certain existing minority Shareholders and/or their close associates, 
who (i) hold less than 5% of the voting rights in the Company prior to the completion of the Global Offering 
and (ii) are not and will not become (upon the completion of the Global Offering) core connected persons of 
the  Company or the close associates of any such core connected person; and (b) a consent under paragraph 
18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to, among other things, 
allocate further H Shares in the International Offering to certain existing Shareholders, Cornerstone Investors 
and/or their close associates, (i) none of the Offer Shares subscribed by the placees and the public have been 
financed directly or indirectly by the Company, any of the Directors, chief executive of the Company, 
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company or any of its 
subsidiaries or their respective close associates; and (ii) none of the placees and the public who have 
purchased the Offer Shares are accustomed to taking instructions from the Company, any of the Directors, 
chief executive of the Company, Controlling Shareholders, substantial Shareholders, existing Shareholders of 
the Company or any of its subsidiaries or their respective close associates in relation to the acquisition, 
disposal, voting or other disposition of H Shares registered in his/her/its name or otherwise held by him/her/it. 
The placees in the International Offering include the following: 
- 5 -

<<<PAGE 6>>>
Cornerstone Investors 
Investor Note 1 
No. of 
Offer 
Shares 
allocated 
Approximate % of total 
issued H Shares after 
the Global 
Offering (assuming 
that the Over-allotment 
Option is not 
exercised) Notes 2,3 
Approximate % of 
total 
issued share 
capital after the 
Global Offering 
(assuming that the 
Over-allotment 
Option is not 
exercised) 
Existing 
shareholders or 
their close 
associates 
Taibai Investments 
Pte. Ltd. (太白投資
有
限
公
司
) 
(“Taibai”)  
19,812,100 
5.17% 
0.26% 
Yes 
True 
Light 
Investments H Pte. 
Ltd (“True Light”) 
4,953,000 
1.29% 
0.06% 
Yes 
HHLR 
Advisors, 
Ltd. (“HHLRA”) 
24,765,100 
6.46% 
0.32% 
Yes 
HHLRA 
(as 
the 
investment 
manager 
of 
a 
segregated 
management 
account 
(“SMA”) 
for 
CPP 
Investments) 
1,857,300 
0.48% 
0.02% 
Yes 
GIC 
Private 
Limited (“GIC”) 
18,573,800 
4.84% 
0.24% 
Yes 
CPE 
Neem 
Investment Limited 
(“CPE Neem”)  
9,286,900 
2.42% 
0.12% 
No 
Greenwoods Asset 
Management Hong 
Kong Limited ( 景
林資產管理香港
有限公司) (“HK 
Greenwoods”)  
8,667,800 
2.26% 
0.11% 
Yes 
Foresight 
Global 
Superior 
Choice 
SPC—Global 
Superior 
Choice 
Fund 1 SP (“GSC 
Fund 
1”), 
Foresight 
Global 
Superior 
Choice 
SPC—Vision Fund 
1 
SP 
(“Vision 
Fund 
1”), 
Foresight 
Global 
8,667,800 
2.26% 
0.11% 
Yes 
- 6 -

<<<PAGE 7>>>
Investor Note 1 
No. of 
Offer 
Shares 
allocated 
Approximate % of total 
issued H Shares after 
the Global 
Offering (assuming 
that the Over-allotment 
Option is not 
exercised) Notes 2,3 
Approximate % of 
total 
issued share 
capital after the 
Global Offering 
(assuming that the 
Over-allotment 
Option is not 
exercised) 
Existing 
shareholders or 
their close 
associates 
Superior 
Choice 
SPC—Horizon 
Fund 
1 
SP 
(“Horizon 
Fund 
1”) and Foresight 
Global 
Superior 
Choice 
SPC—
Horizon Next Fund 
SP (“Horizon Next 
Fund”), Foresight 
China Equity Fund 
(“FSCEF”, 
together with GSC 
Fund 
1, 
Vision 
Fund 1, Horizon 
Fund 1 and Horizon 
Next 
Fund, 
the 
“Foresight 
Funds”) 
Abu 
Dhabi 
Investment 
Authority (阿布扎
比
投
資
局
) 
(“ADIA”) 
5,572,100 
1.45% 
0.07% 
Yes 
UBS 
Asset 
Management 
(Singapore) 
Ltd. 
(“UBS 
AM 
Singapore”)  
5,572,100 
1.45% 
0.07% 
Yes 
Oaktree 
Capital 
Management, L.P. 
(“Oaktree”)  
5,572,100 
1.45% 
0.07% 
Yes 
Eastspring 
Investments 
(Singapore) 
Limited 
(“Eastspring SG”) 
4,643,400 
1.21% 
0.06% 
Yes 
Eastspring 
Investments (Hong 
Kong) Limited (瀚
亞投資（香港）
928,600 
0.24% 
0.01% 
Yes 
- 7 -

<<<PAGE 8>>>
Investor Note 1 
No. of 
Offer 
Shares 
allocated 
Approximate % of total 
issued H Shares after 
the Global 
Offering (assuming 
that the Over-allotment 
Option is not 
exercised) Notes 2,3 
Approximate % of 
total 
issued share 
capital after the 
Global Offering 
(assuming that the 
Over-allotment 
Option is not 
exercised) 
Existing 
shareholders or 
their close 
associates 
有
限
公
司
) 
(“Eastspring HK”) 
First 
Sentier 
Investors 
(Hong 
Kong) 
Limited 
(“First 
Sentier 
Investors HK”) 
5,434,300 
1.42% 
0.07% 
Yes 
First 
Sentier 
Investors 
(Singapore) (“First 
Sentier Investors 
SG”) 
137,800 
0.04% 
0.002% 
Yes 
GF 
Fund 
Management 
Co., 
Ltd. (廣發基金管
理有限公司) (“GF 
Fund 
Management”) 
3,095,600 
0.81% 
0.04% 
Yes 
GF 
International 
Investment 
Management 
Limited (廣發國際
資產管理有限公
司) (“GF Fund 
HK”)  
2,476,500 
0.64% 
0.03% 
Yes 
China 
Universal 
Asset Management 
(Hong 
Kong) 
Company Limited 
(匯添富資產管理
（香港）有限公
司
) 
(“China 
Universal (HK)”)  
5,572,100 
1.45% 
0.07% 
Yes 
Bosera 
Asset 
Management 
(International) Co., 
Limited (博時基金
（國際）有限公
司
) 
(“Bosera 
International”)  
5,572,100 
1.45% 
0.07% 
Yes 
- 8 -

<<<PAGE 9>>>
Investor Note 1 
No. of 
Offer 
Shares 
allocated 
Approximate % of total 
issued H Shares after 
the Global 
Offering (assuming 
that the Over-allotment 
Option is not 
exercised) Notes 2,3 
Approximate % of 
total 
issued share 
capital after the 
Global Offering 
(assuming that the 
Over-allotment 
Option is not 
exercised) 
Existing 
shareholders or 
their close 
associates 
FIL 
Investment 
Management 
(Hong 
Kong) 
Limited (富達基金
（香港）有限公
司
) 
(“Fidelity 
International”)  
3,714,700 
0.97% 
0.05% 
Yes 
Value 
Partners 
Hong 
Kong 
Limited (惠理基金
管理香港有限公
司) (“VPHKL”)  
3,231,800 
0.84% 
0.04% 
Yes 
Value 
Partners 
Limited (惠理基金
管
理
公
司
) 
(“VPL”)  
482,900 
0.13% 
0.01% 
Yes 
Taikang 
Life 
Insurance Co., Ltd 
(泰康人壽保險股
份有限責任公司) 
(“Taikang Life”)  
3,714,700 
0.97% 
0.05% 
Yes 
Huang 
River 
Investment Limited 
(“Huang River”)  
2,971,800 
0.77% 
0.04% 
No 
Prosper 
High 
Holding 
Limited 
(“Prosper High”) 
742,900 
0.19% 
0.01% 
No 
Mirae 
Asset 
Securities Co., Ltd 
(“Mirae 
Securities”)   
619,100 
0.16% 
0.01% 
Yes 
Mirae Asset Global 
Investments 
Co., 
Ltd. 
(“Mirae 
Asset”) 
3,095,600 
0.81% 
0.04% 
Yes 
Perseverance Asset 
Management 
International 
(Singapore) 
Pte. 
Ltd. 
(“Perseverance 
3,714,700 
0.97% 
0.05% 
Yes 
- 9 -

<<<PAGE 10>>>
Investor Note 1 
No. of 
Offer 
Shares 
allocated 
Approximate % of total 
issued H Shares after 
the Global 
Offering (assuming 
that the Over-allotment 
Option is not 
exercised) Notes 2,3 
Approximate % of 
total 
issued share 
capital after the 
Global Offering 
(assuming that the 
Over-allotment 
Option is not 
exercised) 
Existing 
shareholders or 
their close 
associates 
Asset 
Management”) 
Harvest 
Global 
Investments 
Limited (嘉實國際
資產管理有限公
司) (“HGI”)  
3,714,700 
0.97% 
0.05% 
Yes 
Integrated 
Core 
Strategies 
(Asia) 
Pte. 
Ltd. 
(“Millennium”) 
3,714,700 
0.97% 
0.05% 
No 
Jane Street Asia 
Trading 
Limited 
(“Jane Street”)  
3,714,700 
0.97% 
0.05% 
No 
WT 
Asset 
Management 
Limited 
(“WT 
Asset 
Management”) 
3,714,700 
0.97% 
0.05% 
Yes 
MY 
Asian 
Opportunities 
Master Fund, L.P. 
(“MY.Alpha”)  
3,714,700 
0.97% 
0.05% 
No 
Polymer Asia Fund 
LP (“Polymer”)  
3,714,700 
0.97% 
0.05% 
No 
Total 
185,736,900 
48.44% 
2.41% 
Notes: 
1. For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone
Investors” in the Prospectus.
2. The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares
to be issued under the Global Offering.
3.
In addition to the Offer Shares subscribed for as Cornerstone Investors, certain Cornerstone Investors
and/or their close associates were allocated further Offer Shares as placees in the International
Offering. Please refer to the section headed “Allotment Results Details – International Offering –
Allottees with Waivers/Consents Obtained” in this announcement for details. Only the Offer Shares
subscribed for as Cornerstone Investors are subject to lock-up restrictions as indicated below. For
details, please refer to the section headed “Lock-up Undertakings – Cornerstone Investors” in this
announcement.
- 10 -

<<<PAGE 11>>>
Allottees with Waivers/Consents Obtained 
Investor 
No. of Offer 
Shares 
allocated 
Approximate % of total 
issued H Shares after 
the Global Offering 
(assuming that the 
Over-allotment Option 
is not exercised) Note 5 
Approximate % of 
total issued share 
capital after the 
Global Offering 
(assuming that the 
Over-allotment 
Option is not 
exercised) Note 6 
Relationship 
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by certain existing 
minority Shareholders and/or their close associates holding more than 1% of the issued share capital of 
the Company immediately prior to the completion of the Global Offering  Note 1 and 2 
Foresight Funds 
8,667,800 
2.26% 
0.11% 
A Cornerstone 
Investor and an 
existing 
Shareholder 
and/or its close 
associates 
Taikang Life 
3,714,700 
0.97% 
0.05% 
A Cornerstone 
Investor and an 
existing 
Shareholder 
and/or its close 
associates 
HGI 
3,714,700 
0.97% 
0.05% 
A Cornerstone 
Investor and an 
existing 
Shareholder 
and/or its close 
associates 
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in 
relation to allocations of further H Shares to existing Shareholders and Cornerstone Investors and/or 
their close associates Note 3  
Taibai 
7,429,500 
1.94% 
0.10% 
A Cornerstone 
Investor  
HHLRA 
7,429,500 
1.94% 
0.10% 
A Cornerstone 
Investor  
GIC 
5,572,100 
1.45% 
0.07% 
A Cornerstone 
Investor  
CPE Neem 
3,095,600 
0.81% 
0.04% 
A Cornerstone 
Investor 
ADIA 
3,095,600 
0.81% 
0.04% 
A Cornerstone 
Investor  
Huang River 
990,600 
0.26% 
0.01% 
A Cornerstone 
Investor  
Prosper High 
247,600 
0.06% 
0.003% 
A Cornerstone 
Investor  
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients Note 4 
- 11 -

<<<PAGE 12>>>
Investor 
No. of Offer 
Shares 
allocated 
Approximate % of total 
issued H Shares after 
the Global Offering 
(assuming that the 
Over-allotment Option 
is not exercised) Note 5 
Approximate % of 
total issued share 
capital after the 
Global Offering 
(assuming that the 
Over-allotment 
Option is not 
exercised) Note 6 
Relationship 
CITIC Securities 
International 
Capital 
Management 
Limited (“CSI”) 
61,900 
0.02% 
0.001% 
Connected client 
as placee 
CITIC Securities  
Asset Management 
(HK) Limited  
(“CITIC AM 
HK”) 
24,700 
0.01% 
0.0003% 
Connected client 
as placee 
CITIC Securities  
Asset Management 
Company Limited  
(“CITIC AM”) 
185,700 
0.05% 
0.002% 
Connected client 
as placee 
GF Fund 
Management 
3,095,600 
0.81% 
0.04% 
Connected client 
as Cornerstone 
Investor 
GF Fund HK 
2,476,500 
0.64% 
0.03% 
Connected client 
as Cornerstone 
Investor 
GF Securities 
Asset Management 
(Guangdong) Co., 
Ltd. (“GF 
Securities AM”) 
1,609,700 
0.42% 
0.02% 
Connected client 
as placee 
VPHKL 
3,231,800 
0.84% 
0.04% 
Connected client 
as Cornerstone 
Investor 
VPL 
482,900 
0.13% 
0.01% 
Connected client 
as Cornerstone 
Investor 
HSBC Global 
Asset Management 
(Hong Kong) 
Limited (“HSBC 
AM HK”) 
4,953,000 
1.29% 
0.06% 
Connected client 
as placee 
UBS AM 
Singapore 
5,572,100 
1.45% 
0.07% 
Connected client 
as Cornerstone 
Investor 
China Southern 
Asset Management 
Co., Ltd (“China 
Southern”) 
619,100 
0.16% 
0.01% 
Connected client 
as placee 
- 12 -

<<<PAGE 13>>>
Notes: 
1.
The Company has applied for, and the Stock Exchange has granted, a waiver from strict compliance
with the requirements under Rule 10.04 of the Listing Rules and consent under Paragraph 1C(2) of
the Placing Guidelines to permit H Shares in the International Offering to be placed to certain
existing minority Shareholders and/or their close associates. Please refer to the section headed
“Waivers and Exemptions — Waiver in respect of Allocation of H Shares to Existing Minority
Shareholders and their Close Associates” of the Prospectus for details. The Stock Exchange granted
the waiver on the condition that, among others, details of allocations to certain existing minority
Shareholders and/or their close associates holding more than 1% of the issued share capital of the
Company immediately prior to the completion of the Global Offering will be disclosed in the
Prospectus (for cornerstone investors) and allotment results announcement (for both cornerstone
investors and placees) of the Company.
2.
For details of the waiver from strict compliance with Rule 10.04 of the Listing Rules and prior consent
under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by existing
minority Shareholders and/or close associates of existing Shareholders, please refer to the section
headed “Others/Additional Information” in this announcement.
3.
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents
the number of Offer Shares allocated to the investors as placees in the International Offering. For
allocations of Offer Shares to the relevant investors as Cornerstone Investors, please refer to the
section headed “Allotment Results Details – International Offering – Cornerstone Investors” in this
announcement. For details of the consent under paragraph 18 of Chapter 4.15 of the Guide for New
Listing Applicants in relation to allocations of further H Shares to existing Shareholders, Cornerstone
Investors and/or their close associates, please refer to the section headed “Others/Additional
Investor 
No. of Offer 
Shares 
allocated 
Approximate % of total 
issued H Shares after 
the Global Offering 
(assuming that the 
Over-allotment Option 
is not exercised) Note 5 
Approximate % of 
total issued share 
capital after the 
Global Offering 
(assuming that the 
Over-allotment 
Option is not 
exercised) Note 6 
Relationship 
Fullgoal Asset 
Management (HK) 
Limited (“Fullgoal 
HK”) 
1,857,300 
0.48% 
0.02% 
Connected client 
as placee 
Fullgoal Fund 
Management Co., 
Ltd. (“Fullgoal 
Fund”) 
2,476,500 
0.65% 
0.03% 
Connected client 
as placee 
- 13 -

<<<PAGE 14>>>
Information – Allocations of H Shares to the certain existing minority Shareholders and/or their close 
associates with a consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing 
Applicants” in this announcement. 
4.
For details of the consents under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the
Guide for New Listing Applicants in relation to allocations to connected clients, please refer to the
section headed “Others/Additional Information — Placing to connected clients with a prior consent
under paragraph 1C(1) of the Placing Guidelines” in this announcement.
5.
The number of H Shares immediately after the Global Offering is the same as the number of Offer
Shares to be issued under the Global Offering.
6.
Only taking into account the H Shares allocated to the relevant investors under the Global Offering.
LOCK-UP UNDERTAKINGS 
Controlling Shareholders 
Name 
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
immediately 
upon Listing 
Approximate % of 
total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing (assuming 
that the Over-
allotment Option is 
not exercised) Note 3 
Approximate % of 
shareholding 
in the Company 
subject to lock-up 
undertakings 
upon Listing 
(assuming that the 
Over-allotment 
Option is not 
exercised) 
Last day subject to 
the lock-up 
undertakings 
Luxshare 
Limited 
2,731,537,636 
Note 5
- 
35.47% 
January 8, 2027 
(First Six-Month 
Period) Note 1 
July 8, 2027 
(Second Six-Month 
Period) Note 2 
Ms. Wang Note 4 
2,731,537,636 
Note 5
- 
35.47% 
January 8, 2027 
(First Six-Month 
Period) Note 1 
July 8, 2027 
(Second Six-Month 
Period) Note 2 
- 14 -

<<<PAGE 15>>>
Mr. Wang Note 4 
2,751,391,783 
Note 5
- 
35.73% 
January 8, 2027 
(First Six-Month 
Period) Note 1 
July 8, 2027 
(Second Six-Month 
Period) Note 2 
Notes: 
1.
The Controlling Shareholders may dispose of or transfer Shares after the indicated date subject to that
the Controlling Shareholders will not cease to be a Controlling Shareholder.
2.
The Controlling Shareholders will cease to be prohibited from disposing or transferring Shares after
the indicated date.
3.
The number of H Shares immediately after the Global Offering is the same as the number of Offer
Shares to be issued under the Global Offering.
4.
Luxshare Limited is owned as to 50% by Ms. Wang and 50% by Mr. Wang. By virtue of the SFO, each
of Ms. Wang and Mr. Wang is deemed to be interested in the Shares in which Luxshare Limited is
interested.
5.
As of the Latest Practicable Date, out of the 2,731,537,636 A Shares beneficially owned by Luxshare
Limited, an aggregate of 1,033,292,000 A Shares were subject to pledges granted under certain loan
facilities in favor of certain licensed commercial banks. For further details of the share pledges granted
by Luxshare Limited, see section headed “Substantial Shareholders — Share Pledges by Luxshare
Limited” of the Prospectus.
Cornerstone Investors 
Name 
Number of H 
Shares held in 
the Company 
subject to lock-
up 
undertakings 
upon Listing 
Approximate % of 
total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised) Note 1 
Approximate % of 
shareholding in the 
Company subject to 
lock-up undertakings 
upon Listing 
(assuming the Over-
allotment Option is 
not exercised) 
Last day subject to 
the lock-up 
undertakings Note 2 
Taibai 
19,812,100 
5.17% 
0.26% 
January 8, 2027 
True Light 
4,953,000 
1.29% 
0.06% 
January 8, 2027 
HHLRA 
24,765,100 
6.46% 
0.32% 
January 8, 2027 
- 15 -

<<<PAGE 16>>>
Name 
Number of H 
Shares held in 
the Company 
subject to lock-
up 
undertakings 
upon Listing 
Approximate % of 
total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised) Note 1 
Approximate % of 
shareholding in the 
Company subject to 
lock-up undertakings 
upon Listing 
(assuming the Over-
allotment Option is 
not exercised) 
Last day subject to 
the lock-up 
undertakings Note 2 
HHLRA (as the 
investment 
Manager of an 
SMA managed 
for CPP 
Investments) 
1,857,300 
0.48% 
0.02% 
January 8, 2027 
GIC 
18,573,800 
4.84% 
0.24% 
January 8, 2027 
CPE Neem 
9,286,900 
2.42% 
0.12% 
January 8, 2027 
HK 
Greenwoods 
8,667,800 
2.26% 
0.11% 
January 8, 2027 
Foresight Funds 
8,667,800 
2.26% 
0.11% 
January 8, 2027 
ADIA 
5,572,100 
1.45% 
0.07% 
January 8, 2027 
UBS AM 
Singapore 
5,572,100 
1.45% 
0.07% 
January 8, 2027 
Oaktree 
5,572,100 
1.45% 
0.07% 
January 8, 2027 
Eastspring SG 
4,643,400 
1.21% 
0.06% 
January 8, 2027 
Eastspring HK 
928,600 
0.24% 
0.01% 
January 8, 2027 
First Sentier 
Investors HK 
5,434,300 
1.42% 
0.07% 
January 8, 2027 
First Sentier 
Investors SG 
137,800 
0.04% 
0.002% 
January 8, 2027 
GF Fund 
Management 
3,095,600 
0.81% 
0.04% 
January 8, 2027 
GF Fund HK 
2,476,500 
0.64% 
0.03% 
January 8, 2027 
- 16 -

<<<PAGE 17>>>
Name 
Number of H 
Shares held in 
the Company 
subject to lock-
up 
undertakings 
upon Listing 
Approximate % of 
total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised) Note 1 
Approximate % of 
shareholding in the 
Company subject to 
lock-up undertakings 
upon Listing 
(assuming the Over-
allotment Option is 
not exercised) 
Last day subject to 
the lock-up 
undertakings Note 2 
China Universal 
(HK)  
5,572,100 
1.45% 
0.07% 
January 8, 2027 
Bosera 
International 
5,572,100 
1.45% 
0.07% 
January 8, 2027 
Fidelity 
International 
3,714,700 
0.97% 
0.05% 
January 8, 2027 
VPHKL 
3,231,800 
0.84% 
0.04% 
January 8, 2027 
VPL 
482,900 
0.13% 
0.01% 
January 8, 2027 
Taikang Life 
3,714,700 
0.97% 
0.05% 
January 8, 2027 
Huang River 
2,971,800 
0.77% 
0.04% 
January 8, 2027 
Prosper High 
742,900 
0.19% 
0.01% 
January 8, 2027 
Mirae Securities 
619,100 
0.16% 
0.01% 
January 8, 2027 
Mirae Asset 
3,095,600 
0.81% 
0.04% 
January 8, 2027 
Perseverance 
Asset 
Management 
3,714,700 
0.97% 
0.05% 
January 8, 2027 
HGI 
3,714,700 
0.97% 
0.05% 
January 8, 2027 
Millennium 
3,714,700 
0.97% 
0.05% 
January 8, 2027 
Jane Street 
3,714,700 
0.97% 
0.05% 
January 8, 2027 
WT Asset 
Management 
3,714,700 
0.97% 
0.05% 
January 8, 2027 
MY.Alpha 
3,714,700 
0.97% 
0.05% 
January 8, 2027 
- 17 -

<<<PAGE 18>>>
Name 
Number of H 
Shares held in 
the Company 
subject to lock-
up 
undertakings 
upon Listing 
Approximate % of 
total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised) Note 1 
Approximate % of 
shareholding in the 
Company subject to 
lock-up undertakings 
upon Listing 
(assuming the Over-
allotment Option is 
not exercised) 
Last day subject to 
the lock-up 
undertakings Note 2 
Polymer 
3,714,700 
0.97% 
0.05% 
January 8, 2027 
Notes: 
1.
The number of H Shares immediately after the Global Offering is the same as the number of Offer
Shares to be issued under the Global Offering.
2.
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on
January 8, 2027. The Cornerstone Investors will cease to be prohibited from disposing of or
transferring H Shares subscribed for pursuant to the relevant cornerstone investment agreements after
the indicated date.
- 18 -

<<<PAGE 19>>>
PLACEE CONCENTRATION ANALYSIS 
Placees* 
Number of 
H Shares 
Allotted 
Allotment as 
% of 
International 
Offering 
(assuming the 
Over-
allotment 
Option is not 
exercised) 
Allotment as 
% of 
International 
Offering 
(assuming the 
Over-
allotment 
Option is fully 
exercised) 
Allotment as 
% of 
total Offer 
Shares 
(assuming the 
Over-
allotment 
Option is not 
exercised) 
Allotment as 
% of 
total Offer 
Shares 
(assuming the 
Over-
allotment 
Option is fully 
exercised) 
Number of H 
Shares held 
upon Listing 
% of total 
issued share 
capital upon 
Listing 
(assuming the 
Over-
allotment 
Option is not 
exercised) 
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over 
allotment 
Option is 
fully 
exercised) 
Top 1 
 56,340,500 
16.32% 
13.99% 
14.69% 
12.78% 
 56,340,500 
0.73% 
0.73% 
Top 5 
 120,172,400 
34.82% 
29.85% 
31.34% 
27.25% 
 120,172,400 
1.56% 
1.55% 
Top 10 
 161,034,700 
46.66% 
39.99% 
41.99% 
36.52% 
 161,034,700 
2.09% 
2.08% 
Top 25 
 235,700,500 
68.29% 
58.54% 
61.46% 
53.45% 
 235,700,500 
3.06% 
3.04% 
Note 
* Ranking of placees is based on the number of H Shares allotted to the placees.
- 19 -

<<<PAGE 20>>>
H SHAREHOLDERS CONCENTRATION ANALYSIS 
H 
Shareholders* 
Number of 
H Shares 
Allotted 
Allotment as 
% of 
International 
Offering 
(assuming the 
Over-
allotment 
Option is not 
exercised) 
Allotment as 
% of 
International 
Offering 
(assuming the 
Over-
allotment 
Option is fully 
exercised) 
Allotment as 
% of 
total Offer 
Shares 
(assuming the 
Over-
allotment 
Option is not 
exercised) 
Allotment as 
% of 
total Offer 
Shares 
(assuming the 
Over-
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
(assuming the 
Over-
allotment 
Option is not 
exercised) 
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over 
allotment 
Option is 
fully 
exercised) 
Top 1 
 56,340,500 
16.32% 
13.99% 
14.69% 
12.78% 
 56,340,500 
0.73% 
0.73% 
Top 5 
120,172,400 
34.82% 
29.85% 
31.34% 
27.25% 
 120,172,400 
1.56% 
1.55% 
Top 10 
161,034,700 
46.66% 
39.99% 
41.99% 
36.52% 
 161,034,700 
2.09% 
2.08% 
Top 25 
235,700,500 
68.29% 
58.54% 
61.46% 
53.45% 
 235,700,500 
3.06% 
3.04% 
Note 
* Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
- 20 -

<<<PAGE 21>>>
SHAREHOLDER CONCENTRATION  ANALYSIS 
Shareholders* 
Number of 
H Shares 
Allotted 
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
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
Option is 
fully 
exercised) 
Allotment 
as % of 
total Offer 
Shares 
(assuming 
the Over-
allotment 
Option is 
not 
exercised) 
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
Number of 
H Shares 
held upon 
Listing 
Number of 
Shares held 
upon Listing# 
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
not 
exercised) 
% of total 
issued 
share 
capital 
upon 
Listing 
(assuming 
the Over 
allotment 
Option is 
fully 
exercised) 
Top 1 
 -   
0.00% 
0.00% 
0.00% 
0.00% 
 -   2,751,391,783 
35.72% 
35.46% 
Top 5 
 -   
0.00% 
0.00% 
0.00% 
0.00% 
 -   3,792,287,327 
49.24% 
48.87% 
Top 10 
 65,008,300 
18.84% 
16.15% 
16.95% 
14.74% 
 65,008,300  4,208,055,423 
54.64% 
54.23% 
Top 25 
132,926,200 
38.52% 
33.01% 
34.66% 
30.14% 
132,926,200  4,651,749,245 
60.40% 
59.95% 
Note 
* Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.
# Among the top 25 placees, certain placees are also existing Shareholders. To the best knowledge, information and belief of the Company after due enquiry, 
details of the allocations to the Existing Minority Shareholder holding more than 1% of the issued share capital of the Company immediately prior to the 
completion of the Global Offering have been disclosed in this announcement. Please refer to the section headed “Allottees with Waivers/Consents Obtained - 
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the Placing Guidelines in relation to 
subscription for H Shares by certain existing minority Shareholders and/or their close associates holding more than 1% of the issued share capital of the Company 
immediately prior to the completion of the Global Offering” in this announcement. For the top 25 placees who are also existing shareholders held less than 
0.05% of the issued share capital of the Company immediately prior to the completion of the Global Offering, the number of A Shares held by them is not counted 
into the number of Shares held upon Listing. 
- 21 -

<<<PAGE 22>>>
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by the 
public will be conditionally allocated on the basis set out below:  
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL NO. 
OF H SHARES 
APPLIED FOR 
NO. OF 
H 
SHARES 
APPLIE
D FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF ALLOCATION/BALLOT 
POOL A 
100 
26,463 
100 H Shares 
100.00% 
200 
3,403 
100 H Shares plus 2,122 out of 3,403 
applicants to receive an additional 100 H 
Shares 
81.18% 
300 
1,641 
200 H Shares plus 256 out of 1,641 
applicants to receive an additional 100 H 
Shares 
71.87% 
400 
1,300 
200 H Shares plus 827 out of 1,300 
applicants to receive an additional 100 H 
Shares 
65.90% 
500 
2,346 
300 H Shares plus 190 out of 2,346 
applicants to receive an additional 100 H 
Shares 
61.62% 
600 
481 
300 H Shares plus 241 out of 481 applicants 
to receive an additional 100 H Shares 
58.35% 
700 
2,086 
300 H Shares plus 1,873 out of 2,086 
applicants to receive an additional 100 H 
Shares 
55.68% 
800 
390 
400 H Shares plus 109 out of 390 applicants 
to receive an additional 100 H Shares 
53.49% 
900 
206 
400 H Shares plus 134 out of 206 applicants 
to receive an additional 100 H Shares 
51.67% 
1,000 
2,376 
500 H Shares plus 4 out of 2,376 applicants 
to receive an additional 100 H Shares 
50.02% 
1,500 
1,201 
600 H Shares plus 770 out of 1,201 
applicants to receive an additional 100 H 
Shares 
44.27% 
2,000 
812 
800 H Shares plus 98 out of 812 applicants 
to receive an additional 100 H Shares 
40.60% 
2,500 
317 
900 H Shares plus 156 out of 317 applicants 
to receive an additional 100 H Shares 
37.97% 
3,000 
494 
1,000 H Shares plus 387 out of 494 
applicants to receive an additional 100 H 
Shares 
35.94% 
3,500 
174 
1,200 H Shares plus 2 out of 174 applicants 
to receive an additional 100 H Shares 
34.32% 
4,000 
210 
1,300 H Shares plus 39 out of 210 applicants 
to receive an additional 100 H Shares 
32.96% 
4,500 
135 
1,400 H Shares plus 43 out of 135 applicants 
to receive an additional 100 H Shares 
31.82% 
- 22 -

<<<PAGE 23>>>
5,000 
467 
1,500 H Shares plus 192 out of 467 
applicants to receive an additional 100 H 
Shares 
30.82% 
6,000 
336 
1,700 H Shares plus 170 out of 336 
applicants to receive an additional 100 H 
Shares 
29.18% 
7,000 
192 
1,900 H Shares plus 96 out of 192 applicants 
to receive an additional 100 H Shares 
27.86% 
8,000 
173 
2,100 H Shares plus 70 out of 173 applicants 
to receive an additional 100 H Shares 
26.76% 
9,000 
110 
2,300 H Shares plus 27 out of 110 applicants 
to receive an additional 100 H Shares 
25.83% 
10,000 
798 
2,500 H Shares plus 14 out of 798 applicants 
to receive an additional 100 H Shares 
25.02% 
20,000 
382 
4,000 H Shares plus 235 out of 382 
applicants to receive an additional 100 H 
Shares 
20.31% 
30,000 
184 
5,300 H Shares plus 171 out of 184 
applicants to receive an additional 100 H 
Shares 
17.98% 
40,000 
89 
6,500 H Shares plus 84 out of 89 applicants 
to receive an additional 100 H Shares 
16.49% 
50,000 
90 
7,700 H Shares plus 7 out of 90 applicants to 
receive an additional 100 H Shares 
15.42% 
60,000 
39 
8,700 H Shares plus 22 out of 39 
applicants to receive an additional 100 
H Shares 
14.59% 
70,000 
70 
9,700 H Shares plus 36 out of 70 
applicants to receive an additional 100 
H Shares 
13.93% 
 Total  
46,965 
Total number of Pool A successful 
applicants: 46,965 
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL NO. 
OF H SHARES 
APPLIED FOR 
NO. OF 
H 
SHARES 
APPLIE
D FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF ALLOCATION/BALLOT 
POOL B 
80,000 
127 
20,000 H Shares 
25.00% 
90,000 
20 
22,400 H Shares 
24.89% 
100,000 
89 
24,800 H Shares 
24.80% 
200,000 
37 
48,000 H Shares 
24.00% 
300,000 
20 
71,000 H Shares 
23.67% 
400,000 
12 
93,600 H Shares 
23.40% 
500,000 
6 
115,900 H Shares 
23.18% 
600,000 
2 
138,000 H Shares 
23.00% 
700,000 
4 
160,000 H Shares 
22.86% 
800,000 
6 
181,900 H Shares 
22.74% 
900,000 
3 
203,600 H Shares 
22.62% 
1,000,000 
11 
225,300 H Shares 
22.53% 
2,000,000 
3 
437,800 H Shares 
21.89% 
- 23 -

<<<PAGE 24>>>
3,000,000 
1 
645,900 H Shares 
21.53% 
4,000,000 
1 
851,000 H Shares 
21.28% 
5,000,000 
1 
1,057,000 H Shares 
21.14% 
 Total  
343 
Total number of Pool B successful 
applicants: 343 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries. 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of which 
consent has been obtained, the Company has complied with the Listing Rules and guidance materials 
in relation to the placing, allotment and listing of the Company’s H Shares. 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the 
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by 
them was the same as the final Offer Price in addition to any brokerage, SFC transaction levy, AFRC 
transaction levy, and Stock Exchange trading fee payable. 
OTHERS / ADDITIONAL INFORMATION 
Allocations of H Shares to the certain existing minority Shareholders and/or their close 
associates with a consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing 
Applicants 
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph 18 of 
Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to allocate further Offer 
Shares in the International Offering to certain existing Shareholders and Cornerstone Investors and/or 
their close associates as placees, subject to the following conditions (“Allocation to Size-based 
Exemption Participants”): 
(a)
the final offering size of the Global Offering, excluding any over-allocation, will be of a total
value of at least HK$1 billion;
(b)
the Offer Shares allocated to all existing Shareholders and their close associates (whether as
cornerstone investors and/or as placees) as permitted under the Size-based Exemption (as defined
in the Guide for New Listing Applicants) do not exceed 30% of the total number of the H Shares
offered under the Global Offering;
(c)
each Director, chief executive and Controlling Shareholder confirms that no securities have been
allocated to them or their respective close associates under the Size-based Exemption;
(d)
the Allocation to Size-based Exemption Participants will not affect the Company’s ability to
satisfy its public float requirement; and
(e)
details of the allocation to existing Shareholders and/or their close associates and Cornerstone
Investors under the Size-based Exemption will be disclosed in this announcement.
- 24 -

<<<PAGE 25>>>
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted 
by the Stock Exchange. 
For details of the allocations of Offer Shares to existing Shareholders, Cornerstone Investors and/or 
their close associates, please refer to the section headed “Allotment Results Details – International 
Offering – Allottees with Waivers/Consents Obtained” in this announcement. 
Allocation of H Shares to existing minority Shareholders and their close associates 
The Company has applied for, and the Stock Exchange has granted, a waiver from strict compliance 
with Rule 10.04 of, and a consent under paragraph 1C(2) of Appendix F1 to the Listing Rules to permit 
H Shares in the International Offering to be placed to certain existing minority Shareholders who will 
participate only as either cornerstone investors or placees (but not both) in the International Offering 
(together, the “Permitted Existing Shareholders”) on the conditions that each of them: 
(a)
together with their close associates, holds less than 5% of the voting rights in our Company prior
to the completion of the Global Offering;
(b)
is not and will not be, a core connected person of our Company or any close associate of any
such core connected person immediately prior to or following the Global Offering;
(c)
does not have the power to appoint any Director and/or have any other special rights;
(d)
allocation to the Permitted Existing Shareholders and their close associates will not affect the
Company’s ability to satisfy the public float requirement; and
(e)
that no preferential treatment has been, nor will be, given to any of the Permitted Existing
Shareholders or their close associates by virtue of their relationship with our Company in any
allocation in the International Offering.
Please refer to the section headed “Waivers and Exemptions — Waiver in respect of Allocation of H 
Shares to Existing Minority Shareholders and their Close Associates” in the Prospectus for further 
details of the waiver and consent. 
Each of the Joint Sponsors and the Company has provided the required confirmations as elaborated in 
the Prospectus. In particular, as the Company’s A Shares are listed on the Shenzhen Stock Exchange 
since September 2010, the Company has a highly extensive base of existing Shareholders and 
disclosure of details of allocations to all existing minority Shareholders will not be meaningful to 
investors, the proposed disclosure threshold, i.e. details of the allocation to the existing minority 
Shareholders holding more than 1% of the issued share capital of the Company immediately prior to 
the completion of the Global Offering will be disclosed in this announcement, is appropriate.  
All allocations of Offer Shares to the existing minority Shareholders are in compliance with all the 
conditions under the waiver and consent granted by the Stock Exchange. 
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines 
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, consents under 
paragraph 1C(1) of the Placing Guidelines to permit each of GF Fund Management, GF Fund HK, VPHKL 
and VPL to participate in the Global Offering as a Cornerstone Investor. For details of the consent granted, 
- 25 -

<<<PAGE 26>>>
please refer to “Waivers and Exemptions – Consent in respect of Proposed Subscription of Shares by 
certain Cornerstone Investors who are Connected Clients” in the Prospectus. 
In addition, under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines as placees. Please refer to the section headed 
“Allotment Results Details — International Offering — Allottees with Waivers/Consents Obtained” in this 
announcement for details. The Company has applied to the Stock Exchange for, and the Stock Exchange 
has granted, a consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate 
such Offer Shares in the International Offering to the connected clients as placees. The allocation of Offer 
Shares to such connected clients is in compliance with all the conditions under the consent granted by the 
Stock Exchange. Details of the placement to connected clients as placees are set out below.  
- 26 -

<<<PAGE 27>>>
No 
Connected 
Distributor 
Connected Client 
Relationship with the 
Connected Distributor 
Whether the connected 
client will hold the 
beneficial interests of the 
Offer Shares on a non-
discretionary basis or 
discretionary basis for 
independent third parties 
Whether the 
Connected Client is a 
collective investment 
scheme which is not 
authorised by the 
SFC or is expected to 
hold the Offer Shares 
on behalf of such 
scheme 
Number of Offer 
Shares to be allocated 
to the connected 
client 
Approximate 
percentage of 
total number of 
Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) 
Approximate 
percentage of total 
Shares in issue 
immediately following 
the completion of 
Global Offering 
(assuming the Over-
allotment Option is not 
exercised) 
1. 
CLSA Limited 
(“CLSA”) 
CITIC Securities 
International Capital 
Management Limited 
(“CSI”) Note 1 
CSI is a member of the same 
group of companies as CLSA. 
Non-discretionary basis 
N 
61,900 
0.02% 
0.001% 
2. 
CITIC Securities Asset 
Management (HK) Limited 
(“CITIC AM HK”) Note 2 
CITIC AM HK is a member of 
the same group of companies as 
CLSA. 
Discretionary basis 
N 
24,700 
0.02% 
0.0003% 
3. 
CITIC Securities Asset 
Management Company 
Limited (“CITIC AM”) Note
3
CITIC AM is a member of the 
same group of companies as 
CLSA. 
Discretionary basis 
Y 
Please refer to note 11 
for background and 
details of such 
schemes. 
185,700 
0.05% 
0.002% 
4. 
GF Securities 
(Hong Kong) 
Brokerage Limited 
(“GF Securities 
(Hong Kong) 
Brokerage”) 
GF Fund Management Co., 
Ltd. (“GF Fund 
Management”) Note 4 
GF Fund Management is a 
member of the same group of 
companies as GF Securities 
(Hong Kong) Brokerage. 
Discretionary basis 
N 
3,095,600 
0.81% 
0.04% 
5. 
GF International 
Investment Management 
Limited (“GF Fund HK”) 
Note 5
GF Fund HK is a member of the 
same group of companies as GF 
Securities (Hong Kong) 
Brokerage. 
Discretionary basis 
N 
2,476,500 
0.64% 
0.03% 
6. 
GF Securities Asset 
Management (Guangdong) 
Co., Ltd. (“GF Securities 
AM”) Note 6 
GF Securities AM is a member 
of the same group of companies 
as GF Securities (Hong Kong) 
Brokerage. 
Non-discretionary basis 
N 
1,609,700 
0.42% 
0.02% 
7. 
The Hongkong 
and Shanghai 
Banking 
Corporation 
Limited (“HSBC 
Bank”) 
HSBC Global Asset 
Management (Hong Kong) 
Limited (“HSBC AM 
HK”) Note 7 
HSBC AM HK is a member of 
the same group of companies as 
HSBC Bank. 
Discretionary basis 
N 
4,953,000 
1.29% 
0.06% 
8. 
UBS AG 
Singapore Branch 
(“UBS AG 
Singapore”) 
UBS Asset Management 
(Singapore) Ltd. (“UBS 
AM Singapore”) Note 8 
UBS AM Singapore is a 
member of the same group of 
companies as UBS AG 
Singapore. 
Discretionary basis 
N 
5,572,100 
1.45% 
0.07% 
- 27 -

<<<PAGE 28>>>
9. 
Huatai Financial 
Holdings (Hong 
Kong) Limited 
(“HTFH”) 
China Southern Asset 
Management Co., Ltd 
(“China Southern”) Note 9 
China Southern is a member of 
the same group of companies as 
HTFH.  
Discretionary basis 
N 
619,100 
0.16% 
0.01% 
10. 
Guotai Junan 
Securities (Hong 
Kong) Limited 
(“GTJA 
Securities”) and 
Haitong 
International 
Securities 
Company Limited 
(“HTIS”) 
Fullgoal Asset Management 
(HK) Limited (“Fullgoal 
HK”) Note 10 
Each of Fullgoal HK and 
Fullgoal Fund is a member of 
the same group of companies as 
GTJA Securities and HTIS.  
Discretionary basis 
N 
1,857,300 
0.48% 
0.02% 
11. 
Fullgoal Fund Management 
Co., Ltd. (“Fullgoal 
Fund”) Note 10 
Discretionary basis 
N 
2,476,500 
0.65% 
0.03% 
Notes: 
1.
CSI proposes to subscribe for and hold the Offer Shares as a placee under the International Offering for and on behalf of its underlying client (the “CSI Ultimate Client”), on a non-discretionary basis, pursuant to which CSI 
will act as the single counterparty of a back-to-back total return swap transaction (the “CSI Back-to-back TRS”) to be entered into by it in connection with a total return swap order (the “CSI Client TRS”) placed and fully 
funded by the CSI Ultimate Client, by which CSI will pass the full economic exposure of the Offer Shares placed to CSI to the CSI Ultimate Client. As confirmed by CSI and CLSA, CSI will hold the legal title and beneficial 
interest in the Offer Shares, but will contractually agree to pass on the full economic exposure and return of the Offer Shares to the CSI Ultimate Client, on a non-discretionary basis. The CSI Ultimate Client may exercise its 
early termination rights to terminate the CSI Client TRS at any time from the trade date of the CSI Client TRS which should be on or after the date on which the Offer Shares are listed on the Stock Exchange.
The CSI Ultimate Client is Hover4pi Fund I OFC, of which shareholder holding 30% or more interest is He Hui. Hover4pi Fund I OFC is managed by Hover4pi Capital Management. None of the shareholders hold 30% or more 
interest in Hover4pi Capital Management.
2.
CITIC AM HK is a member of the same group of companies as CLSA. CITIC AM HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds for and on behalf of its investors. To the 
best knowledge of CITIC AM HK after due enquiry, each of the funds is an independent third party of the Company, its subsidiaries, its substantial shareholders, CITIC AM HK, CLSA and the companies which are members 
of the same group of companies as CLSA.
3.
CITIC AM is a member of the same group of companies as CLSA. CITIC AM will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds for and on behalf of their investors (the “CITICS 
AM Ultimate Clients”). Each of the CITICS AM Ultimate Clients is, to the best knowledge of CITIC AM, (i) an independent third party of the Company, its subsidiaries, its substantial shareholders, CITIC AM, CLSA and the 
companies which are members of the same group of companies as CLSA; and (ii) a collective investment scheme which is not authorized by the SFC. Please refer to note 11 below for background and details of such schemes.
4.
GF Fund Management will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds for and on behalf of its underlying clients, each of which is, to the best knowledge and belief and after due 
enquiry of GF Fund HK, an independent third party of the Company, its subsidiaries, GF Fund Management, GF Securities (Hong Kong) Brokerage and the companies which are members of the same group of GF Securities
(Hong Kong) Brokerage. 
5.
GF Fund HK will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds for and on behalf of its underlying clients, each of which is, to the best knowledge and belief and after due enquiry
of GF Fund HK, an independent third party of the Company, its subsidiaries, GF Fund HK, GF Securities (Hong Kong) Brokerage and the companies which are members of the same group of GF Securities (Hong Kong) 
Brokerage. 
6.
GF Securities AM will hold the Offer Shares on a non-discretionary basis for and on behalf of its underlying clients (the “GF AM Ultimate Clients”), each of which is, to the best knowledge and belief and after due enquiry of 
GF Securities AM, an independent third party of the Company, its subsidiaries, GF Securities AM, GF Securities (Hong Kong) Brokerage and the companies which are members of the same group of GF Securities (Hong Kong) 
Brokerage. 
The GF AM Ultimate Clients include (i) PSBC Wealth Management Co., Ltd. (中郵理財有限責任公司), of which the shareholder holding 30% or more interest is Postal Savings Bank of China Co., Ltd. (中國郵政儲蓄銀行
股份有限公司), a company listed on the Stock Exchange (stock code: 01658); and (ii) CMB Wealth Management Co., Ltd. (招銀理財有限責任公司), of which the shareholder holding 30% or more interest is China Merchants 
Bank Co., Ltd. (招商銀行股份有限公司) , a company listed on the Stock Exchange (stock code: 03968). 
- 28 -

<<<PAGE 29>>>
7.
HSBC AM HK will hold the Offer Shares in its capacity as discretionary fund manager managing the funds for and on behalf of its investors, each of which is an independent third party of the Company, its subsidiaries, HSBC
AM HK and HSBC Bank and the companies which are members of the same group of HSBC Bank. 
8.
UBS AM Singapore will hold the Offer Shares in its capacity as the delegate of the investment manager on a discretionary basis for and on behalf of the following fund(s): (i) UBS (Lux) Equity Fund—Greater China (USD); 
(ii) UBS (Lux) Equity Fund—China Opportunity (USD); (iii) UBS (HK) Fund Series—China Opportunity Equity (USD); (iv) UBS (Lux) Equity SICAV—All China (USD); and (v) certain other segregated accounts and 
mandates, each of which is an independent third party of the Company, its subsidiaries, UBS AG Singapore, UBS AM Singapore and the companies which are members of the same group of companies as UBS AG Singapore. 
9.
China Southern will hold the Offer Shares in its capacity as the discretionary fund manager for and on behalf of its underlying clients, each of which is an independent third party of the Company, its subsidiaries, China Southern, 
HTFH and the companies which are members of the same group of companies as HTFH. 
10.
Fullgoal HK is a wholly-owned subsidiary of Fullgoal Fund. Guotai Haitong Securities Co., Ltd. (stock codes: 2611.HK and 601211.SH) (“Guotai Haitong”) is a shareholder of Fullgoal Fund, holding a 27.775% equity interest
therein. GTJA Securities and HTIS are both subsidiaries of Guotai Haitong. Each of Fullgoal HK and Fullgoal Fund will hold the Offer Shares in its capacity as the discretionary fund manager managing assets for and on behalf 
of its underlying investors, each of which is an independent third party of the Company, its subsidiaries, Fullgoal HK, Fullgoal Fund, GTJA Securities, HTIS and the companies which are members of the same group of GTJA 
Securities and HTIS.
11.
Details of the collective investment schemes which are not authorized by the SFC are as follows: 
No. 
Fund name 
Types and values of assets 
under management 
Whether the 
scheme is publicly 
marketed 
Identities of the general partners 
and the 20 largest limited partners 
of the scheme where applicable 
Identity of the scheme 
administrator 
Relationships among the scheme, the ultimate 
beneficial owner(s) of the limited partner(s), the 
largest group of the shareholders/ controlling 
shareholders of the Company, and the 
Company 
1. 
CITIC 
Securities 
AM-
Guibinfengyuan 
No.118 
QDII (中信證券資管貴賓豐
元118 號QDII 集合資產管
理計劃) 
Collective asset management plan 
AUM:  
approximately RMB228 million* 
No 
Not applicable as it is not in 
partnership structure and does not 
have any general partner or limited 
partner 
CITIC AM 
The scheme and ultimate beneficial owners are 
independent third parties of CLSA, the Company 
and the Controlling Shareholders.  
2. 
CITIC 
SECURITIES 
COMPANY 
LIMITED-
XINHANG 
ZHIYUAN 
NO.1 (中信證券信航致遠1
號集合資產管理計劃) 
Collective asset management plan 
AUM:  
approximately RMB24 million* 
No 
Not applicable as it is not in 
partnership structure and does not 
have any general partner or limited 
partner 
CITIC AM 
The scheme and ultimate beneficial owners are 
independent third parties of CLSA, the Company 
and the Controlling Shareholders. 
3. 
CITIC 
SECURITIES 
COMPANY 
LIMITED-
XINHANG 
ZHIYUAN 
NO.3 (中信證券信航致遠3
號集合資產管理計劃) 
Collective asset management plan 
AUM:  
approximately RMB56 million* 
No 
Not applicable as it is not in 
partnership structure and does not 
have any general partner or limited 
partner 
CITIC AM 
The scheme and ultimate beneficial owners are 
independent third parties of CLSA, the Company 
and the Controlling Shareholders. 
4. 
CITIC SECURITIES AM-
GUIBINFENGYUAN 
NO.108 QDII (中信證券資
管貴賓豐元108 號QDII 集
合資產管理計劃) 
Collective asset management plan 
AUM:  
approximately RMB155 million* 
No 
Not applicable as it is not in 
partnership structure and does not 
have any general partner or limited 
partner 
CITIC AM 
The scheme and ultimate beneficial owners are 
independent third parties of CLSA, the Company 
and the Controlling Shareholders. 
* This AUM figure is as of 18 June 2026. 
- 29 -

<<<PAGE 30>>>
DISCLAIMERS 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or into the 
United States (including its territories and possessions, any state of the United States and the 
District of Columbia). This announcement does not, and is not intended to, constitute or form a 
part of any offer to sell or solicitation to purchase or subscribe for any securities in the United 
States or in any other jurisdiction. The Offer Shares have not been, and will not be, registered 
under the U.S. Securities Act of 1933, as amended from time to time (the “U.S. Securities Act”) or 
securities law of any state or other jurisdiction of the United States. The Offer Shares may not be 
offered, sold, pledged or otherwise transferred within the United States, except pursuant to an 
available exemption from, or in a transaction not subject to, the registration requirements of the 
U.S. Securities Act and in compliance with any applicable state securities laws. There will be no 
public offer of the Offer Shares in the United States.  
The Offer Shares are being offered and sold solely outside the United States in offshore transactions 
in reliance on Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for any securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated June 30, 2026 issued by Luxshare Precision 
Industry Co., Ltd. (立訊精密工業股份有限公司 ) for detailed information about the Company 
and the Global Offering described below before deciding whether or not to invest in the H Shares 
thereby being offered. Any investment decision in relation to the Offer Shares should be taken solely 
in reliance on the information provided in the Prospectus. 
* Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to
terminate the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of
any of the events set out in the section headed “Underwriting — Underwriting Agreements — Hong
Kong Underwriting Agreement — Grounds for Termination” in the Prospectus at any time prior
to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Thursday,
July 9, 2026).
- 30 -

<<<PAGE 31>>>
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering (before any exercise of the 
Over-allotment Option, and assuming that the options granted under the Share Option 
Incentive Plans and the conversion rights for the outstanding Convertible Bonds are not 
exercised), the total market value of the H Shares expected to be held by the public is 
expected to be approximately HK$24.27 billion, calculated based on the final Offer Price 
of HK$63.28 per H Share, which is higher than the prescribed expected market value of H 
Shares required to be held in public hands of not less than HK$3,000,000,000 under Rule 
19A.13A(2)(b) of the Listing Rules, thereby satisfying Rule 19A.13A(2) of the Listing 
Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following 
the Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall 
not be counted towards the free float of the H Shares of the Company at the time of Listing. 
Based on the final Offer Price of HK$63.28 per H Share, the Company satisfies the free 
float requirement under Rule 19A.13C of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering (before 
any exercise of the Over-allotment Option): (i) no placee will, individually, be placed 
more than 10% of the enlarged issued share capital of the Company immediately after the 
Global Offering; (ii) there will not be any new substantial Shareholder immediately after the 
Global Offering; (iii) the three largest public Shareholders do not hold more than 50% of 
the H shares in public hands at the time of the Listing in compliance with Rules 8.08(3) and 
8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at the time of the 
Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Thursday, 
July 9, 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting — Underwriting 
Agreements — Hong Kong Underwriting Agreement — Grounds for Termination” in the 
Prospectus has not been exercised. Investors who trade the H Shares on the basis of publicly 
available allocation details prior to the receipt of H Share certificates or prior to the H Share 
certificates becoming valid evidence of title do so entirely at their own risk.
- 31 -

<<<PAGE 32>>>
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on 
Thursday, July 9, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the 
Stock Exchange will commence at 9:00 a.m. on Thursday, July 9, 2026 (Hong Kong time). 
The H Shares will be traded in board lots of 100 H Shares each, and the stock code of the H 
Shares will be 2475.
By order of the Board
Luxshare Precision Industry Co., Ltd.
立訊精密工業股份有限公司
Ms. Wang Laichun
Chairlady and Executive Director
People’s Republic of China, July 8, 2026
As at the date of this announcement, (i) Ms. Wang Laichun, Mr. Wang Laisheng, Mr. Qian Jiwen, Mr. Hao 
Jie and Mr. Chen Weihang are the executive Directors; and (ii) Dr. Hou Lingling, Mr. Liu Zhonghua and Ms. 
Song Yuhong are the independent non-executive Directors.
- 32 -
