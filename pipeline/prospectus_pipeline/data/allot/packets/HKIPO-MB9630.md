# 配发结果公告抽取任务：9630.HK Circuit Fabology Microelectronics Equipment Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**25/06/2026 22:42**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0625/2026062502296.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"9630.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
CIRCUIT FABOLOGY MICROELECTRONICS EQUIPMENT CO., LTD.
合肥芯碁微電子裝備股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated June 17, 2026 (the “Prospectus”) 
issued by Circuit Fabology Microelectronics Equipment Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, Shareholders and prospective investors should be aware that the price 
of the H Shares could move substantially even with a small number of H Shares 
traded and should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
9630
Stock short name
CFMEE
Dealings commencement date
June 26, 2026*
*  see note at the end of the announcement
Price Information
Final Offer Price
252.73
Offer Shares and Share Capital
Number of Offer Shares (Before exercise of the Over-
allotment Option)
12,838,650
Final Number of Offer Shares in Hong Kong Public 
Offering
1,283,900
Final Number of Offer Shares in International 
Offering (excluding Employee Reserved Shares 
under the Employee Preferential Offering and before 
exercise of the Over-allotment Option)
11,241,150
Number of Employee Reserved Shares in Employee 
Preferential Offering
313,600
Number of issued shares upon Listing (before exercise 
of the Over-allotment Option)
144,579,366

<<<PAGE 2>>>
– 2 –
Over-allocation
No. of Offer Shares over-allocated
1,925,750
Such over-allocation may be covered by exercising the Over-allotment Option or by 
making purchases in the secondary market at prices that do not exceed the Offer Price 
or through deferred delivery or a combination of these means. In the event the Over-
allotment Option is exercised, an announcement will be made on the Stock Exchange’s 
website.
Proceeds
Gross proceeds (Note)
HK$3,244.7 million
Less: Estimated listing expenses payable based on 
Final Offer Price
HK$91.7 million
Net proceeds
HK$3,153.1 million
Note:	Gross proceeds refers to the amount to which the Company is entitled to receive. For details of 
the use of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the 
Prospectus. The Company will adjust the allocation of the net proceeds from the exercise of the 
Over-allotment Option (if any) for the purposes as set out in the section headed “Future Plans and 
Use of Proceeds” of the Prospectus on a pro rata basis. We did not incur any listing expenses in 
2023 and 2024. In 2025, we incurred listing expenses of RMB16.2 million, of which RMB0.6 million 
was expensed in our consolidated statements of profit or loss.

<<<PAGE 3>>>
– 3 –
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
207,986
No. of successful applications
24,412
Subscription level
1,007.22 times
Reallocation
N/A
No. of Offer Shares initially available under the Hong 
Kong Public Offering
1,283,900
No. of Offer Shares reallocated from the International 
Offering
0
Final no. of Offer Shares under the Hong Kong Public 
Offering
1,283,900
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering
10%
Note:	For details of the results of allocations of the H Shares in the Hong Kong Public Offering, 
investors can refer to the “Allotment Results” page at https://www.hkeipo.hk/IPOResult or 
https://www.hkeipo.hk/IPOResult with a “search by ID” function.
INTERNATIONAL OFFERING
No. of placees
200
Subscription Level (excluding Employee Reserved 
Shares under the Employee Preferential Offering)
27.22 times
No. of Offer Shares initially available under the 
International Offering (excluding Employee Reserved 
Shares under the Employee Preferential Offering)
11,241,150
Final no. of Offer Shares under the International 
Offering (excluding Employee Reserved Shares under 
the Employee Preferential Offering) (before exercise of 
the Over-allotment Option)
11,241,150
% of Offer Shares under the International Offering 
to the Global Offering (including Employee Reserved 
Shares under the Employee Preferential Offering)
90%

<<<PAGE 4>>>
– 4 –
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) 
a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted 
by the Stock Exchange to permit H Shares in the International Offering to be placed to 
certain existing minority Shareholders and/or their close associates, and (b) a consent under 
Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to, among 
other things, allocate further H Shares in the International Offering to certain existing 
Shareholders and/or their close associates and Cornerstone Investors (i) none of the Offer 
Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, Controlling 
Shareholders, substantial Shareholders, existing Shareholders of the Company or any of 
its subsidiaries or their respective close associates; and (ii) none of the placees and the 
public who have purchased the Offer Shares are accustomed to taking instructions from the 
Company, any of the Directors, chief executive of the Company, Controlling Shareholders, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries 
or their respective close associates in relation to the acquisition, disposal, voting or other 
disposition of H Shares registered in his/her/its name or otherwise held by him/her/it.
PREFERENTIAL OFFERING
Employee preferential offering
No. of valid applications
1*
Subscription level
1 times
No. of Employee Reserved Shares initially available 
under the Employee Preferential Offering
313,600 International Offer 
Shares
Final no. of Employee Reserved Shares under the 
Employee Preferential Offering
313,600
Under-subscription of shares and made available to the 
International Offering
—
Under-subscription of shares and made available to the 
Hong Kong Public Offering
—
*  The number of Eligible Employee participated in the Employee Preferential Offering is 11.

<<<PAGE 5>>>
– 5 –
For details of the Employee Preferential Offering, please refer to the section headed 
“Structure of the Global Offering — The International Offering — Employee Preferential 
Offering” of the Prospectus and the section headed “Others/Additional Information — 
Allocations under the Employee Preferential Offering” in this announcement.
The placees in the International Offering include the following:
Cornerstone Investors
Investor Note 1
No. of Offer Shares 
allocated Note 2
% of total issued 
H Shares after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 3
% of total issued 
share capital 
after the Global 
Offering (assuming 
the Over-allotment 
Option is not 
exercised)
Existing 
Shareholders 
or their close 
associates
Entities under the control of Hefei SASAC
Hefei Jianhui Zhanxin Cornerstone 
Investment Company Limited 
(“Hefei Jianhui”)
340,950
2.66%
0.24%
No
Hong Kong Xinyao Investment 
Limited (“Xinyao Investment”)
309,950
2.41%
0.21%
No
Nexchip Semiconductor Hong 
Kong Corporation Limited 
(“Nexchip Semiconductor HK”)
247,950
1.93%
0.17%
No
JPMorgan Asset Management (Asia 
Pacific) Limited (“JPMAMAPL”)
619,950
4.83%
0.43%
No
Victory Giant Technology Holdings 
(Hong Kong) Limited (“Victory 
Giant HK”)
619,950
4.83%
0.43%
No
CPE Chestnut Investment Limited 
(“CPE Chestnut”)
557,950
4.35%
0.39%
No
Lion Global Investors Limited (“Lion 
Global”)
557,950
4.35%
0.39%
No
CICC Financial Trading Limited in 
connection with Greenwoods OTC 
Swaps (“CICC FT (in connection 
with Greenwoods OTC Swaps)”)
371,950
2.90%
0.26%
No
HHLR Advisors, Ltd. (“HHLR”)
371,950
2.90%
0.26%
No
Huadeng Victorious Way Limited 
(“Huadeng Victorious”)
325,450
2.53%
0.23%
No

<<<PAGE 6>>>
– 6 –
Investor Note 1
No. of Offer Shares 
allocated Note 2
% of total issued 
H Shares after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 3
% of total issued 
share capital 
after the Global 
Offering (assuming 
the Over-allotment 
Option is not 
exercised)
Existing 
Shareholders 
or their close 
associates
Montage Hong Kong Holdings 
Company Limited (“Montage HK”)
309,950
2.41%
0.21%
No
HK Yonglian Investment 
Development Co., Limited (“Yonglian 
Investment”)
309,950
2.41%
0.21%
No
Monterey Park Finance Limited 
(“Monterey Park”)
294,750
2.30%
0.20%
Yes
Bosera Asset Management 
(International) Co., Limited (“Bosera 
International”)
216,950
1.69%
0.15%
Yes
China Universal Asset Management 
(Hong Kong) Company Limited 
(“China Universal (HK)”)
216,950
1.69%
0.15%
Yes
Fullgoal Asset Management 
(HK) Limited and Fullgoal Fund 
Management Co., Ltd. (“Fullgoal HK 
and Fullgoal Fund”)
216,950
1.69%
0.15%
Yes
GF Fund Management Co., Ltd. 
and GF International Investment 
Management Limited (“GF Fund”)
216,950
1.69%
0.15%
No
Ocean Fine Industrial Limited 
(“Ocean Fine Industrial”)
154,950
1.21%
0.11%
No
Sungrow Power (Hong Kong) Co., 
Limited (“Sungrow Power HK”)
154,950
1.21%
0.11%
No
Total
6,416,350
49.98%
4.44%
Notes:
1.	
For further details of the cornerstone investors, please refer to the section headed “Cornerstone Investors” of the Prospectus; excluding Offer Shares 
allotted to Cornerstone Investors and/or their close associates with consent under Chapter 4.15 of the Guide for New Listing Applicants (if any).
2.	
Subject to rounding down to the nearest whole board lot of 50 Offer Shares. Calculated based on the exchange rate set out in the section headed 
“Information about this Prospectus and the Global Offering — Currency Translations”.
3.	
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the Global Offering.

<<<PAGE 7>>>
– 7 –
Allottees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after the 
Global Offering 
(Assuming Over-
allotment Option 
is not exercised) 
Note 7
% of total 
issued share 
capital after the 
Global Offering 
(Assuming Over-
allotment Option 
is not exercised) 
Note 8
Relationship*
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the 
Placing Guidelines in relation to subscription for H Shares by existing minority Shareholders holding more than 1% of the 
issued share capital of the Company immediately prior to the completion of the Global Offering and/or their close associates 
Notes 1,2 and 3
Monterey Park
294,750
2.30%
0.20%
A Cornerstone Investor and 
an existing Shareholder or 
close associate of an existing 
Shareholder
Bosera International
216,950
1.69%
0.15%
A Cornerstone Investor and 
an existing Shareholder or 
close associate of an existing 
Shareholder
China Universal (HK)
216,950
1.69%
0.15%
A Cornerstone Investor and 
an existing Shareholder or 
close associate of an existing 
Shareholder
Fullgoal HK and Fullgoal 
Fund
216,950
1.69%
0.15%
A Cornerstone Investor and 
an existing Shareholder or 
close associate of an existing 
Shareholder

<<<PAGE 8>>>
– 8 –
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after the 
Global Offering 
(Assuming Over-
allotment Option 
is not exercised) 
Note 7
% of total 
issued share 
capital after the 
Global Offering 
(Assuming Over-
allotment Option 
is not exercised) 
Note 8
Relationship*
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations 
of further H Shares to the existing Shareholders and/or their close associates and Cornerstone Investors Note 4
Fullgoal HK
11,350
0.0884%
0.0079%
Fullgoal HK is a wholly 
owned subsidiary of Fullgoal 
Fund Management Co., 
Ltd., who is an existing 
Shareholder of the Company.
Fullgoal Fund
19,650
0.1531%
0.0136%
Fullgoal Fund is an existing 
Shareholder of the Company.
Bosera International
31,000
0.2415%
0.0214%
Bosera International is an 
existing shareholder and 
a cornerstone investor.
JF Asset Management 
Ltd.
31,000
0.2415%
0.0214%
JF Asset Management Ltd. 
is a member of same group 
of companies as JPMorgan 
Asset Management (Asia 
Pacific) Limited, who is a 
cornerstone investor.
J.P.Morgan Securities 
(Asia Pacific) Limited
300
0.0023%
0.0002%
J.P.Morgan Securities (Asia 
Pacific) Limited is a member 
of same group of companies 
as JPMorgan Asset 
Management (Asia Pacific) 
Limited, who is a cornerstone 
investor.
Lion Global Investors
31,000
0.2415%
0.0214%
Lion Global is a cornerstone 
investor.
Oversea-Chinese Banking 
Corporation Limited 
(TRS)
45,000
0.3505%
0.0311%
Oversea-Chinese Banking 
Corporation Limited is a 
member of same group of 
companies as Lion Global 
Investors Limited, who is a 
cornerstone investor.

<<<PAGE 9>>>
– 9 –
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after the 
Global Offering 
(Assuming Over-
allotment Option 
is not exercised) 
Note 7
% of total 
issued share 
capital after the 
Global Offering 
(Assuming Over-
allotment Option 
is not exercised) 
Note 8
Relationship*
Oversea-Chinese Banking 
Corporation Limited
（TRS）
502,700
3.9155%
0.3477%
Oversea-Chinese Banking 
Corporation Limited is a 
member of same group of 
companies as Lion Global 
Investors Limited, who is a 
cornerstone investor.
China Universal (HK)
62,000
0.4829%
0.0429%
China Universal (HK) is a 
cornerstone investor.
Yonglian Investment
155,000
1.2073%
0.1072%
Yonglian Investment is a 
cornerstone investor.
GF Fund Management 
Co., Ltd. (“GF Fund 
Management”)
39,200
0.3053%
0.0271%
GF Fund Management Co., 
Ltd. is a cornerstone investor.
GF International 
Investment Management 
Limited (“GF Fund 
HK”, together with GF 
Fund Management, “GF 
Fund”)
53,800
0.4190%
0.0372%
GF International Investment 
Management Limited is a 
cornerstone investor.
GF Securities 
Asset Management 
(Guangdong) Co., Ltd
1,850
0.0144%
0.0013%
GF Securities Asset 
Management (Guangdong) 
Co., Ltd is a member of same 
group of companies as GF 
Fund, who are cornerstone 
investors.
Value Partners Hong 
Kong Limited
9,300
0.0724%
0.0064%
Value Partners Hong Kong 
Limited is a member of same 
group of companies as GF 
Fund.
E Fund Management 
(Hong Kong) Co., Limited
1,250
0.0097%
0.0009%
E Fund Management (Hong 
Kong) Co., Limited is a 
member of same group of 
companies as GF Fund.

<<<PAGE 10>>>
– 10 –
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after the 
Global Offering 
(Assuming Over-
allotment Option 
is not exercised) 
Note 7
% of total 
issued share 
capital after the 
Global Offering 
(Assuming Over-
allotment Option 
is not exercised) 
Note 8
Relationship*
E Fund Management 
Company Limited
8,050
0.0627%
0.0056%
E Fund Management 
Company Limited is a 
member of same group of 
companies as GF Fund.
Greenwoods Asset 
Management Hong Kong 
Limited
20,450
0.1593%
0.0141%
Greenwoods Asset 
Management Hong Kong 
Limited is a close associate 
of Shanghai Greenwoods 
Asset Management Co., Ltd., 
who is the ultimate clients of 
the Greenwoods OTC Swaps 
as defined in the Prospectus.
Greenwoods through 
Huatai Capital Investment 
Limited
10,550
0.0822%
0.0073%
Greenwoods is the ultimate 
clients of the Greenwoods 
OTC Swaps as defined in the 
Prospectus.
HHLR
31,000
0.2415%
0.0214%
HHLR is a cornerstone 
investor.
Huadeng Victorious
93,000
0.7244%
0.0643%
Huadeng is a cornerstone 
investor.
Montage HK
62,000
0.4829%
0.0429%
Montage HK is a cornerstone 
investor.
BAO Qin via CITIC 
Securities Brokerage 
(Hong Kong) Limited 
(in connection with OTC 
Swaps)
118,700
0.9246%
0.0821%
BAO Qin is a close associate 
of Tongfu Microelectronics 
Co., Ltd., which wholly 
owns Ocean Fine Industrial 
Limited, a cornerstone 
investor.

<<<PAGE 11>>>
– 11 –
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after the 
Global Offering 
(Assuming Over-
allotment Option 
is not exercised) 
Note 7
% of total 
issued share 
capital after the 
Global Offering 
(Assuming Over-
allotment Option 
is not exercised) 
Note 8
Relationship*
Qingdao Roadshow 
Investment Mangement 
Co.,Ltd-Reindeer No.89 
via Huatai Capital 
Investment Limited (TRS)
775,000
6.0365%
0.5360%
Qingdao Roadshow 
Investment Mangement 
Co.,Ltd-Reindeer No.89 is 
a close associate of Ms. Liu 
Chunlan, who is a director 
of Victory Giant Technology 
Holdings (Hong Kong) 
Limited, a cornerstone 
investor.
Sungrow Power HK
31,000
0.2415%
0.0214%
Sungrow Power HK is a 
cornerstone investor.
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the 
Placing Guidelines in relation to allocations to Existing Shareholder Employee Participants under the Employee Preferential 
Offering Note 5
Existing Shareholder 
Employee Participants
313,600
2.44%
0.22%
Eligible Employees
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations to connected clients Note 6
CICC FT (in connection 
with the Greenwoods 
OTC Swaps)
371,950
2.90%
0.26%
Connected client as a 
cornerstone investor
CICC FT in connection 
with the Pinpoint OTC 
Swaps
550
0.0043%
0.0004%
Connected client as a placee
CICC FT in connection 
with the Longrising OTC 
Swaps
3,100
0.0241%
0.0021%
Connected client as a placee
CICC FT in connection 
with the Gaoyi OTC 
Swaps
9,200
0.0717%
0.0064%
Connected client as a placee
Huatai Capital Investment 
Limited (“HTCI”)
864,550
6.7340%
0.5980%
Connected client as placee

<<<PAGE 12>>>
– 12 –
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after the 
Global Offering 
(Assuming Over-
allotment Option 
is not exercised) 
Note 7
% of total 
issued share 
capital after the 
Global Offering 
(Assuming Over-
allotment Option 
is not exercised) 
Note 8
Relationship*
Bosera Asset Management 
(International) Co., Ltd 
(博時基金(國際)有限公
司) (“Bosera AM”)
31,000
0.2415%
0.0214%
Connected client as placee
China Universal Asset 
Management (Hong 
Kong) Company Limited 
(“China Universal 
(HK)”)
62,000
0.4829%
0.0429%
Connected client as placee
China Asset Management 
(Hong Kong) Limited  
(華夏基金(香港)有限公
司) (“China AMC HK”)
3,100
0.0241%
0.0021%
Connected client as placee
Fullgoal Fund 
Management Co., Ltd  
(富國基金管理有限 
公司) (“Fullgoal Fund”)
19,650
0.1531%
0.0136%
Connected client as placee
Fullgoal Asset 
Management (HK) 
Limited (“Fullgoal AM”)
11,350
0.0884%
0.0079%
Connected client as placee
Notes:
1.	
Among the Cornerstone Investors, Monterey Park, Bosera International, China Universal (HK), 
Fullgoal HK, Fullgoal Fund are either existing minority Shareholders of the Company holding more 
than 1% of the issued share capital of the Company immediately prior to the completion of the Global 
Offering or their close associates. The Stock Exchange has granted a waiver from strict compliance 
with the requirements under Rule 10.04 of the Listing Rules and consent under Paragraph 1C(2) of the 
Placing Guidelines to permit H Shares in the International Offering to be placed to certain existing 
minority Shareholders and/or their close associates. Please refer to the section headed “Waivers from 
Strict Compliance with the Listing Rules — Allocation of H Shares to Existing Minority Shareholders 
and/or Their Close Associates” of the Prospectus for details.
The Stock Exchange granted the waiver on the condition that, among others, details of the allocation 
to the existing minority Shareholders holding more than 1% of the issued share capital of the Company 
immediately prior to the completion of the Global Offering will be disclosed in the Prospectus and/or 
allotment results announcement.

<<<PAGE 13>>>
– 13 –
2.	
For details of the waiver from strict compliance with Rule 10.04 of the Listing Rules and prior consent 
under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by existing 
minority Shareholders and/or close associates of existing Shareholders, please refer to the section 
headed “Others/Additional Information” in this announcement.
3.	
The number of Offer Shares allocated to Monterey Park, Bosera International, China Universal (HK), 
Fullgoal HK and Fullgoal Fund listed in this subsection only represents the number of Offer Shares 
allocated to Monterey Park, Bosera International, China Universal (HK), Fullgoal HK and Fullgoal 
Fund as cornerstone investors (excluding the Offer Shares allocated to Monterey Park, Bosera 
International, China Universal (HK), Fullgoal HK and Fullgoal Fund and/or their close associates 
in the placing tranche). For details of the consent under paragraph 18 of Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations of further H Shares to the existing Shareholders 
and/or their close associates and Cornerstone investors, please refer to the section headed “Others/
Additional Information — Allocations of Offer Shares to the existing Shareholders and/or their close 
associates and Cornerstone investors with a consent under paragraph 18 of Chapter 4.15 of the Guide 
for New Listing Applicants” in this announcement.
4.	
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents 
the number of Offer Shares allocated to the investors as placees in the International Offering. For 
allocations of Offer Shares to the relevant investors as Cornerstone Investors, please refer to the 
section headed “Allotment Results Details — International Offer — Cornerstone Investors” in this 
announcement. For details of the consent under paragraph 18 of Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations of further H Shares to the existing Shareholders and/or 
their close associates and Cornerstone investors, please refer to the section headed “Others/Additional 
Information — Allocations of Offer Shares to the existing Shareholders and/or their close associates 
and Cornerstone investors with a consent under paragraph 18 of Chapter 4.15 of the Guide for New 
Listing Applicants” in this announcement.
5.	
For details of the waiver from strict compliance with Rule 10.04 of the Listing Rules and consent 
under Paragraph 1C(2) of the Placing Guidelines in relation to allocations to Existing Shareholder 
Employee Participants and the Employee Preferential Offering, please refer to the sections headed 
“Waivers and Exemptions — Waiver and Consent in Respect of Allocations to Existing Shareholder 
Employee Participants” and “Structure of the Global Offering — Employee Preferential Offering” of 
the Prospectus. For details of the allocations under the Employee Preferential Offering, please refer 
to the section headed “Others/Additional Information — Allocations under the Employee Preferential 
Offering” in this announcement.
6.	
For details of the consents under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations to connected clients, please refer to the 
section headed “Others/Additional Information — Placing to connected clients with a prior consent 
under paragraph 1C(1) of the Placing Guidelines” in this announcement.
7.	
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering.
8.	
Only taking into account the H Shares allocated to the relevant investors under the Global Offering.

<<<PAGE 14>>>
– 14 –
Allottees who are customer(s) and/or supplier(s) of the Company
Investor
No. of Offer 
Shares allocated
% of H Shares 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised) Note 2
% of total issued 
share capital 
after the Global 
Offering (after 
taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised)
Relationship
Victory Giant HK Note 1
1,394,950
4.83%
0.43%
Shareholder of a customer of 
the Group
Monterey Park Note 1
294,750
2.30%
0.20%
Subsidiary of a customer of 
the Group
Ocean Fine Industrial Note 1
273,650
1.21%
0.11%
Subsidiary of a customer of 
the Group
Dynamic Holding Co., 
Ltd. Note 1
43,300
0.34%
0.03%
Shareholder of a customer of 
the Group
Note:
1.	
The number of Offer Shares allocated to Victory Giant HK, Monterey Park and Ocean Fine Industrial listed in this 
subsection only represents the number of Offer Shares allocated to Victory Giant HK, Monterey Park and Ocean Fine 
Industrial as cornerstone investors and as placees in the International Offering (as the case may be).
2.	
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued 
under the Global Offering

<<<PAGE 15>>>
– 15 –
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
immediately upon 
Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
% of shareholding 
in the Company 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject to the lock-
up undertakings Note 2
Ms. Cheng Zhuo Note 3
34,152,677
—
23.62%
December 25, 2026 (First 
Six-Month Period) Note 1
June 25, 2027 (Second Six-
Month Period) Note 2
Yage Venture Capital Note 3
9,450,000
—
6.54%
December 25, 2026 (First Six 
Month Period) Note 1
June 25, 2027 (Second Six 
Month Period) Note 2
Na Photolithography Note 3
746,625
—
0.52%
December 25, 2026 (First Six 
Month Period) Note 1 
June 25, 2027 (Second Six 
Month Period) Note 2
He Photolithography Note 3
618,375
—
0.43%
December 25, 2026 (First Six 
Month Period) Note 1
June 25, 2027 (Second Six 
Month Period) Note 2
Notes:
1.	
The Controlling Shareholders may dispose of or transfer Share after the indicated date subject to 
that the Controlling Shareholders will not cease to be a Controlling Shareholder.
2.	
The Controlling Shareholders will cease to be prohibited from disposing or transferring Shares after 
the indicated date.
3.	
As of the Latest Practicable Date, Yage Venture Capital, Na Photolithography and He 
Photolithography were controlled by Ms. Cheng as general partner and held 9,450,000, 746,625 
and 618,375 A Shares, respectively. As such, Ms. Cheng was deemed to be interested in the A shares 
held by the three entities for the purpose of Part XV of the SFO.

<<<PAGE 16>>>
– 16 –
Cornerstone Investors
Name
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 1
% of shareholding 
in the Company 
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
Hefei Jianhui
340,950
2.66%
0.24%
December 25, 2026
Xinyao Investment
309,950
2.41%
0.21%
December 25, 2026
Nexchip Semiconductor HK
247,950
1.93%
0.17%
December 25, 2026
JPMAMAPL
619,950
4.83%
0.43%
December 25, 2026
Victory Giant HK
619,950
4.83%
0.43%
December 25, 2026
CPE Chestnut
557,950
4.35%
0.39%
December 25, 2026
Lion Global
557,950
4.35%
0.39%
December 25, 2026
CICC FT (in connection with 
Greenwoods OTC Swaps)
371,950
2.90%
0.26%
December 25, 2026
HHLR
371,950
2.90%
0.26%
December 25, 2026
Huadeng Victorious
325,450
2.53%
0.23%
December 25, 2026
Montage HK
309,950
2.41%
0.21%
December 25, 2026
Yonglian Investment
309,950
2.41%
0.21%
December 25, 2026
Monterey Park
294,750
2.30%
0.20%
December 25, 2026
Bosera International
216,950
1.69%
0.15%
December 25, 2026
China Universal (HK)
216,950
1.69%
0.15%
December 25, 2026
Fullgoal HK and Fullgoal Fund
216,950
1.69%
0.15%
December 25, 2026
GF Fund
216,950
1.69%
0.15%
December 25, 2026
Ocean Fine Industrial
154,950
1.21%
0.11%
December 25, 2026
Sungrow Power HK
154,950
1.21%
0.11%
December 25, 2026
Notes:
1.	
The number of H Shares immediately after the Global Offering is the same as the number of Offer 
Shares to be issued under the Global Offering.
2.	
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on 
December 25, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or 
transferring H Shares subscribed for pursuant to the relevant cornerstone investment agreements 
after the indicated date.

<<<PAGE 17>>>
– 17 –
PLACEE CONCENTRATION ANALYSIS
Placees
Number of H 
Shares allotted
Allotment as % 
of International 
Offering (assuming 
the Over-allotment 
Option is not 
exercised)
Allotment as % 
of International 
Offering 
(assuming the 
Over-allotment 
Option is 
exercised)
Allotment as % of 
total Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
Allotment as % 
of total Offer 
Shares (assuming 
the Over-
allotment Option is 
exercised)
Number of Shares 
held upon Listing
Approximate % 
of total issued 
share capital upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Approximate % 
of total issued 
share capital upon 
Listing (assuming 
the Over-
allotment Option is 
exercised)
Top1
1,394,950
12.07%
10.35%
10.87%
9.45%
1,394,950
0.96%
0.95%
Top5
4,639,650
40.15%
34.42%
36.14%
31.42%
4,639,650
3.21%
3.17%
Top10
6,935,650
60.02%
51.45%
54.02%
46.98%
6,935,650
4.80%
4.73%
Top25
10,872,900
94.10%
80.66%
84.69%
73.64%
19,390,125
13.41%
13.24%
Note:
*	
Ranking of placees is based on the number of H Shares allotted to the placees.
**	
The International Offering includes the PRC Employee Preferential Offering.
H SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders
Number of H 
Shares allotted
Allotment as % 
of International 
Offering (assuming 
the Over-allotment 
Option is not 
exercised)
Allotment as % 
of International 
Offering 
(assuming the 
Over-allotment 
Option is 
exercised)
Allotment as % of 
total Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
Allotment as % 
of total Offer 
Shares (assuming 
the Over-
allotment Option is 
exercised)
Number of 
Shares held  
upon Listing
Approximate % 
of total issued 
share capital upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Approximate % 
of total issued 
share capital upon 
Listing (assuming 
the Over-
allotment Option is 
exercised)
Number of Shares 
held upon Listing
Top1
1,394,950
12.07%
10.35%
10.87%
9.45%
1,394,950
0.96%
0.95%
1,394,950
Top5
4,639,650
40.15%
34.42%
36.14%
31.42%
4,639,650
3.21%
3.17%
4,639,650
Top10
6,935,650
60.02%
51.45%
54.02%
46.98%
6,935,650
4.80%
4.73%
6,935,650
Top25
10,872,900
94.10%
80.66%
84.69%
73.64%
19,390,125
13.41%
13.24%
19,390,125
Note:
*	
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon 
Listing.
**	
The International Offering includes the PRC Employee Preferential Offering.

<<<PAGE 18>>>
– 18 –
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
Number of 
Shares allotted
Allotment as % 
of International 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Allotment as % 
of International 
Offering 
(assuming the 
Over-allotment 
Option is 
exercised)
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over-allotment 
Option is 
exercised)
Number of H 
Shares held 
upon Listing 
Number of 
Shares (all 
class) held upon 
Listing 
Approximate % 
of total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Approximate % 
of total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is 
exercised)
Top1
0
0.00%
0.00%
0.00%
0.00%
NA
 44,967,677 
31.10%
30.69%
Top5
1,069,600
9.26%
7.93%
8.33%
7.24%
1,069,600
 59,037,857 
40.83%
40.30%
Top10
2,464,550
21.33%
18.28%
19.20%
16.69%
2,464,550
 66,694,196 
46.13%
45.52%
Top25
5,160,900
44.66%
38.28%
40.20%
34.96%
5,160,900
 75,603,123 
52.29%
51.60%
Note:
*	
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder 
upon Listing.
**	
The International Offering includes the PRC Employee Preferential Offering. 

<<<PAGE 19>>>
– 19 –
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications 
made by the public will be conditionally allocated on the basis set out below:
BASIS OF ALLOTMENT FOR PRESS ANNOUNCEMENT
NO. OF SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL
NO. OF SHARES
APPLIED FOR
POOL A
50
74,911
2,248 out of 74,911 applicants to receive 50 H Shares
3.00%
100
11,402
443 out of 11,402 applicants to receive 50 H Shares
1.94%
150
24,260
1,093 out of 24,260 applicants to receive 50 H Shares
1.50%
200
4,711
237 out of 4,711 applicants to receive 50 H Shares
1.26%
250
3,468
189 out of 3,468 applicants to receive 50 H Shares
1.09%
300
2,142
125 out of 2,142 applicants to receive 50 H Shares
0.97%
350
5,301
327 out of 5,301 applicants to receive 50 H Shares
0.88%
400
1,796
117 out of 1,796 applicants to receive 50 H Shares
0.81%
450
961
66 out of 961 applicants to receive 50 H Shares
0.76%
500
6,954
490 out of 6,954 applicants to receive 50 H Shares
0.70%
600
2,011
152 out of 2,011 applicants to receive 50 H Shares
0.63%
700
1,510
121 out of 1,510 applicants to receive 50 H Shares
0.57%
800
1,837
154 out of 1,837 applicants to receive 50 H Shares
0.52%
900
1,193
105 out of 1,193 applicants to receive 50 H Shares
0.49%
1,000
5,813
529 out of 5,813 applicants to receive 50 H Shares
0.46%
1,500
4,303
455 out of 4,303 applicants to receive 50 H Shares
0.35%
2,000
3,979
468 out of 3,979 applicants to receive 50 H Shares
0.29%
2,500
2,566
328 out of 2,566 applicants to receive 50 H Shares
0.26%
3,000
2,095
286 out of 2,095 applicants to receive 50 H Shares
0.23%
3,500
1,716
249 out of 1,716 applicants to receive 50 H Shares
0.21%
4,000
2,206
335 out of 2,206 applicants to receive 50 H Shares
0.19%
4,500
1,133
180 out of 1,133 applicants to receive 50 H Shares
0.18%
5,000
3,281
542 out of 3,281 applicants to receive 50 H Shares
0.17%
6,000
1,949
344 out of 1,949 applicants to receive 50 H Shares
0.15%
7,000
1,532
287 out of 1,532 applicants to receive 50 H Shares
0.13%
8,000
1,707
336 out of 1,707 applicants to receive 50 H Shares
0.12%
9,000
1,123
231 out of 1,123 applicants to receive 50 H Shares
0.11%
10,000
11,267
2,402 out of 11,267 applicants to receive 50 H Shares
0.11%
 
Total
187,127
Total number of Pool A successful applicants: 12,839
 

<<<PAGE 20>>>
– 20 –
NO. OF SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL
NO. OF SHARES 
APPLIED FOR
POOL B
20,000
11,096
4,439 out of 11,096 applicants to receive 50 H Shares
0.10%
30,000
2,749
1,405 out of 2,749 applicants to receive 50 H Shares
0.09%
40,000
1,651
1,004 out of 1,651 applicants to receive 50 H Shares
0.08%
50,000
1,217
847 out of 1,217 applicants to receive 50 H Shares
0.07%
60,000
717
557 out of 717 applicants to receive 50 H Shares
0.06%
70,000
486
415 out of 486 applicants to receive 50 H Shares
0.06%
80,000
494
457 out of 494 applicants to receive 50 H Shares
0.06%
90,000
273
50 H Shares
0.06%
100,000
1,187
50 H Shares plus 68 out of 1,187 applicants to receive an 
additional 50 H Shares
0.05%
200,000
432
50 H Shares plus 262 out of 432 applicants to receive an additional 
50 H Shares
0.04%
300,000
164
100 H Shares
0.03%
400,000
81
100 H Shares plus 36 out of 81 applicants to receive an additional 
50 H Shares
0.03%
500,000
117
100 H Shares plus 93 out of 117 applicants to receive an additional 
50 H Shares
0.03%
641,950
195
150 H Shares plus 55 out of 195 applicants to receive an additional 
50 H Shares
0.03%
 
Total
20,859
Total number of Pool B successful applicants: 11,573
 
As of the date of this announcement, the relevant subscription monies previously deposited 
in the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/
or in respect of which consent has been obtained, the Company has complied with the 
Listing Rules and guidance materials in relation to the placing, allotment and listing of the 
Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by 
the placees or the public (as the case may be) directly or indirectly for each Offer Share 
subscribed for or purchased by them was the same as the final Offer Price in addition to any 
brokerage, AFRC transaction levy, SFC transaction levy and Stock Exchange trading fee 
payable.

<<<PAGE 21>>>
– 21 –
OTHERS/ADDITIONAL INFORMATION
Allocations to connected client under the Employee Preferential Offering with consent 
under paragraph 1C(1) of the Placing Guidelines
The Company has applied for, and the Stock Exchange has granted, a consent under 
paragraph 1C(1) of the Placing Guidelines to permit CICC Financial Trading Limited to 
participate in the Global Offering as a placee in connection with the Employee Preferential 
Offering, subject to the conditions set out in the Prospectus.
Allocations of Offer Shares to existing Shareholders and Cornerstone Investors and/or 
their close associates with a consent under Chapter 4.15 of the Guide for New Listing 
Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 
4.15 of the Guide for New Listing Applicants to permit the Company to allocate further 
Offer Shares in the International Offering to certain existing Shareholders and Cornerstone 
Investors and/or their close associates as placees, subject to the following conditions (the 
“Allocation to Size-based Exemption Participants”):
(a)	
the final offering size of the Global Offering, excluding any over-allocation, will be of 
a total value of at least HK$1 billion;
(b)	 the Offer Shares allocated to all existing Shareholders (whether as Cornerstone 
Investors and/or as placees) as permitted under this exemption do not exceed 30% of 
the total number of Offer Shares offered under the Global Offering;
(c)	
the Allocation to Size-based Exemption Participants will not affect the Company’s 
ability to satisfy its public float requirement under Rule 8.08(1) (as amended and 
replaced by Rule 19A.13A) of the Listing Rules;
(d)	 each of the Directors and chief executive of the Company confirms that no securities 
have been allocated to them or their respective close associates under this exemption; 
and
(e)	
details of the Cornerstone Investors and/or their close associates under this exemption 
will be disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to Cornerstone Investors, please refer to the 
section headed “Allotment Results Details — International Offering — Allottees with 
Waivers/Consents Obtained” in this announcement.

<<<PAGE 22>>>
– 22 –
Placing to connected clients with a prior consent under Paragraph 1C(1) of the Placing 
Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit CICC FT (in connection 
with Greenwoods OTC Swaps) to participate in the Global Offering as a Cornerstone 
Investor. For details of the allocations to CICC FT (in connection with Greenwoods OTC 
Swaps), please refer to the section headed “Allotment Results Details — International 
Offering — Cornerstone Investors” in this announcement.
In addition, under the International Offering, certain Offer Shares were placed to connected 
clients of their connected distributors pursuant to the Placing Guidelines as placees. Please 
refer to the section headed “Allotment Results Details — International Offering — Allottees 
with Waivers/Consents Obtained” in this announcement for details. The Company has 
applied to the Stock Exchange for, and the Stock Exchange has granted, a consent under 
paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such Offer 
Shares in the International Offering to the connected clients as placees. The allocation of 
Offer Shares to such connected clients is in compliance with all the conditions under the 
consent granted by the Stock Exchange. Details of the placement to connected clients as 
placees are set out below.

<<<PAGE 23>>>
– 23 –
No.
Connected Distributor
Connected Client
Relationship with 
the Connected 
Distributor
Whether the connected clients 
will hold the beneficial interests 
of the Offer Shares on a 
non-discretionary basis or 
discretionary basis for 
independent third parties
Number of 
Offer Shares 
to be allocated 
to the connected 
client
Approximate 
percentage of 
Offer Shares 
allocated to the 
connected client 
(assuming the 
Over-allotment 
Option is not 
exercised)
Approximate 
percentage of 
total issued 
share capital 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
1
CICCHKS
CICC FT in connection with  
the Pinpoint OTC Swaps Note 1
See Note 1
Non-discretionary basis
550
0.0043%
0.0004%
2
CICCHKS
CICC FT in connection with the 
Longrising OTC Swaps Note 2
See Note 2
Non-discretionary basis
3,100
0.0241%
0.0021%
3
CICCHKS
CICC FT in connection with  
the Gaoyi OTC Swaps Note 3
See Note 3
Non-discretionary basis
9,200
0.0717%
0.0064%
4
Huatai Financial Holdings (Hong Kong) Limited 
(“HTFH”)
HTCI Note 4
See Note 4
Non-discretionary basis
864,550
6.7340%
0.5980%
5
CMB International Securities Limited (招銀國際證券有
限公司) (“CMBI”) and China Merchants Securities 
(HK) Co., Limited (招商證券(香港)有限公司) 
(“CMS”)
Bosera AM Note 5
See Note 5
Discretionary basis
31,000
0.2415%
0.0214%
6
Orient Securities (Hong Kong) Limited (東方證券(香港)
有限公司) (“Orient Securities”)
China Universal (HK) Note 6
See Note 6
Discretionary basis
62,000
0.4829%
0.0429%
7
CITIC Securities Brokerage (HK) Limited (中信証券經
紀(香港)有限公司) (“CITIC Brokerage”)
China AMC HK Note 7
See Note 7
Discretionary basis
3,100
0.0241%
0.0021%
8
Guotai Junan Securities (Hong Kong) Limited (國泰君
安證券(香港)有限公司) (“GTJAS”) and Haitong 
International Securities Company Limited (海通國際
證券有限公司) (“Haitong Securities”)
Fullgoal Fund Note 8
See Note 8
Discretionary basis
19,650
0.1531%
0.0136%
9
GTJAS and Haitong Securities
Fullgoal AM Note 9
See Note 9
Discretionary basis
11,350
0.0884%
0.0079%

<<<PAGE 24>>>
– 24 –
Notes:
1.	
CICC FT and CICCL will enter into a series of cross border delta-one OTC swap transactions 
(collectively, the “Pinpoint OTC Swaps”) with each other and the ultimate clients (the “CICC FT 
Ultimate Clients (Pinpoint)”), pursuant to which CICC FT will hold the Offer Shares on a non-
discretionary basis to hedge the Pinpoint OTC Swaps while the economic risks and returns of the 
underlying Offer Shares are passed to the CICC FT Ultimate Clients (Pinpoint), subject to customary 
fees and commissions. The Pinpoint OTC Swaps will be fully funded by the CICC FT Ultimate 
Clients (Pinpoint). To the best of CICC FT’s knowledge having made all reasonable inquiries, each of 
the CICC FT Ultimate Clients (Pinpoint) is an independent third party of CICC FT, CICCHKS and 
the companies which are members of the same group of CICCHKS. The CICC FT Ultimate Clients 
(Pinpoint) are certain domestic private funds (including a total of no more than three funds, each 
being an Independent Third Party) managed by Shanghai Pinpoint Private Fund Management Co., 
Ltd. (上海保銀私募基金管理有限公司) (“Shanghai Pinpoint”). Li Mo holds 30% or more interest 
in Shanghai Pinpoint. Wang Qiang holds 30% or more interest in Pinpoint Multi-Strategy Stable No. 
1 Private Securities Investment Fund (保銀多空穩健1號私募證券投資基金) and Pinpoint Multi-
Strategy Stable No. 2 Private Securities Investment Fund (保銀多空穩健2號私募證券投資基金). 
No single ultimate beneficial owner holds 30% or more interest in Pinpoint Aggressive No. 1 (保銀進
取1號). To the best knowledge of CICC FT after due enquiry, each of the CICC FT Ultimate Clients 
(Pinpoint), their ultimate beneficial owners and the ultimate beneficial owners of Shanghai Pinpoint 
are independent third parties of the Company, its subsidiaries, CICC FT, CICCHKS and the companies 
which are members of the same group as CICC FT and CICCHKS.
2.	
CICC FT and CICCL will enter into a series of cross border delta-one OTC swap transactions 
(collectively, the “Longrising OTC Swaps”) with each other and the ultimate clients (the “CICC 
FT Ultimate Clients (Longrising)”), pursuant to which CICC FT will hold the Offer Shares on a 
non-discretionary basis to hedge the Longrising OTC Swaps while the economic risks and returns 
of the underlying Offer Shares are passed to the CICC FT Ultimate Clients (Longrising), subject 
to customary fees and commissions. The Longrising OTC Swaps will be fully funded by the CICC 
FT Ultimate Clients (Longrising). To the best of CICC FT’s knowledge having made all reasonable 
inquiries, each of the CICC FT Ultimate Clients (Longrising) is an independent third party of CICC 
FT, CICCHKS and the companies which are members of the same group of CICCHKS. The CICC FT 
Ultimate Clients (Longrising) for purpose of this placee subscription include (i) Yuanlesheng Qiangye 
Private Securities Investment Fund (源樂晟強業私募證券投資基金), whose fund manager is Tibet 
Yuanlesheng Asset Management Company Ltd. (“Tibet Longrising”, 西藏源樂晟資產管理有限公
司) and ultimate beneficial owners holding 30% or more interest are Zeng Xiaojie and Hu Caiyang, (ii) 
Yuanlesheng Qiangshu Private Securities Investment Fund (源樂晟強樹私募證券投資基金), whose 
fund manager is Tibet Longrising and ultimate beneficial owner holding 30% or more interest is Zeng 
Xiaojie, (iii) Yuanlesheng Qiangshi Private Securities Investment Fund (源樂晟強勢私募證券投資
基金), whose fund manager is Tibet Longrising and ultimate beneficial owner holding 30% or more 
interest is Zeng Xiaojie. To the best knowledge of CICC FT after due enquiry, each of the CICC FT 
Ultimate Clients (Longrising) and their ultimate beneficial owners are independent third parties of the 
Company, its subsidiaries, CICC FT, CICCHKS and the companies which are members of the same 
group as CICC FT and CICCHKS.

<<<PAGE 25>>>
– 25 –
3.	
CICC FT and CICCL will enter into a series of cross border delta-one OTC swap transactions 
(collectively, the “Gaoyi OTC Swaps”) with each other and the ultimate clients (the “CICC FT 
Ultimate Clients (Gaoyi)”), pursuant to which CICC FT will hold the Offer Shares on a non-
discretionary basis to hedge the Gaoyi OTC Swaps while the economic risks and returns of the 
underlying Offer Shares are passed to the CICC FT Ultimate Clients (Gaoyi), subject to customary 
fees and commissions. The Gaoyi OTC Swaps will be fully funded by the CICC FT Ultimate Clients 
(Gaoyi). During the terms of the Gaoyi OTC Swaps, all economic returns of the Offer Shares 
subscribed by CICC FT will be passed to the CICC FT Ultimate Clients (Gaoyi) and all economic loss 
shall be borne by the CICC FT Ultimate Clients (Gaoyi) through the Gaoyi OTC Swaps, and CICC 
FT will not take part in any economic return or bear any economic loss in relation to the Offer Shares. 
The Gaoyi OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate Clients (Gaoyi) may, 
after expiration of the lock-up period beginning from the date of the cornerstone agreement entered 
into between CICC FT and the Company and ending on the date which is six months from the Listing 
Date, request to early terminate the Gaoyi OTC Swaps at their own discretions, upon which CICC FT 
may dispose of the Offer Shares and settle the Gaoyi OTC Swaps in cash in accordance with the terms 
and conditions of the Gaoyi OTC Swaps. Despite that CICC FT will hold the legal title of the Offer 
Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares during the 
terms of the Gaoyi OTC Swaps according to its internal policy. To the best of CICC FT’s knowledge 
having made all reasonable inquiries, each of the CICC FT Ultimate Clients (Gaoyi) is an independent 
third party of CICC FT, China International Capital Corporation Hong Kong Securities Limited 
(“CICCHKS”) and the companies which are members of the same group of CICCHKS, and no 
single ultimate beneficial owner holds 30% or more interests in each of the CICC FT Ultimate Clients 
(Gaoyi).
The CICC FT Ultimate Clients (Gaoyi) are certain investment funds (including a total of no more than 
seven funds) managed by Shanghai Gaoyi Asset Management Partnership (Limited Partnership) (上海
高毅資產管理合夥企業(有限合夥)) (“Shanghai Gaoyi”). Shanghai Gaoyi is a limited partnership 
established in the PRC, which is engaged in asset management and investment management with 
a primary focus on investments in secondary market. Shanghai Gaoyi holds the Qualification of 
Private Investment Fund Manager (私募投資基金管理人資格) accredited by the Asset Management 
Association of China (中國證券投資基金業協會). The managing partner of Shanghai Gaoyi 
is Shanghai Gaoyi Investment Management Co., Ltd. (上海高毅投資管理有限公司) (“Gaoyi 
Investment”). Perseverance Asset Management is an affiliate of Shanghai Gaoyi.
4.	
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial 
public offerings (“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products 
issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading 
activities. In connection with such products, the licensed domestic securities firms, through their Hong 
Kong affiliates, may participate in Hong Kong IPOs either as placees or cornerstone investors (the 
“Cross-border Derivatives Trading Regime”).
Huatai Securities Co., Ltd. (“Huatai Securities”), the shares of which are listed on both the Shanghai 
Stock Exchange (stock code: 601688) and the Stock Exchange (stock code: 6886), is one of the 
domestic securities firms licensed to undertake cross-border derivatives trading activities. Huatai 
Securities entered into an ISDA agreement (the “ISDA Agreement”) with its indirectly wholly-owned 
subsidiary, Huatai Capital Investment Limited (“HTCI”) to set out the principal terms of any future 
total return swap between Huatai Securities and HTCI.

<<<PAGE 26>>>
– 26 –
HTFH is a sub-broker in connection with the Global Offering. Pursuant to the ISDA Agreement, 
HTCI, which intends to participate in the Global Offering as a placee, will hold the beneficial interest 
of the Offer Shares on a non-discretionary basis as the single underlying holder under a back-to-back 
total return swap (the “Back-to-back TRS”) to be entered by HTCI in connection with a Client TRS 
(as defined below) placed by and fully funded (i.e. with no financing provided by HTCI) by the Huatai 
Ultimate Clients (as defined below), by which, HTCI will, subject to customary fees and commissions, 
pass the full economic exposure of the Offer Shares ultimately to the Huatai Ultimate Clients, which 
in effect, HTCI will hold the beneficial interest of the Offer Shares on behalf of the Huatai Ultimate 
Clients. HTFH and HTCI are indirectly wholly-owned subsidiaries of Huatai Securities. Accordingly, 
HTCI is considered as a “connected client” of HTFH pursuant to paragraph 13(7) of the Placing 
Guidelines.
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the “Huatai Ultimate 
Clients”) cannot directly subscribe for the Offer Shares but may invest in derivative products issued 
by domestic securities firms licenced to undertake cross-border derivatives trading activities, such as 
Huatai Securities, with the Offer Shares as the underlying assets. Instead of directly subscribing for the 
Offer Shares, the Huatai Ultimate Clients, through their investment manager, will place a total return 
swap order (the “Client TRS”) with Huatai Securities in connection with the Company’s IPO and 
Huatai Securities will place a Back-to-back TRS order to HTCI on the terms of the ISDA Agreement. 
In order to hedge its exposure under the Back-to-back TRS, HTCI participates in the Company’s IPO 
and subscribes the Offer Shares through placing order with HTFH during the International Offering. 
The Huatai Ultimate Clients for purpose of this placing subscription include (i) Shanghai Greenwoods 
Asset Management Co., Ltd. (上海景林資產管理有限公司) (“Shanghai Greenwoods”) in its 
capacity as the fund manager of Greenwoods Harvest No. 2 Private Securities Investment Fund (景林
豐收2號私募證券投資基金), Greenwoods Harvest No. 3 Private Investment Fund (景林豐收3號私
募基金), Greenwoods Harvest No. 6 Private Securities Investment Fund (景林豐收6號私募證券投資
基金), Greenwoods Jingtai Harvest Private Securities Investment Fund (景林景泰豐收私募證券投資
基金), Greenwoods Zhiyuan Private Investment Fund (景林致遠私募基金), Greenwoods Global Fund 
(景林全球基金), and Greenwoods Jingtai Global Private Securities Investment Fund (景林景泰全球
私募證券投資基金); and (ii) Yikun Ruijian No.1 Private Securities Investment Fund (懿坤睿見1號
私募證券投資基金) (“Yikun Ruijian Fund”), a discretionary fund managed by Mr. Gao Yi (高懿). 
Mr. Jiang Jinzhi (蔣錦志) is the Chairman and an ultimate beneficial owner of Shanghai Greenwoods, 
holding 30% or more of the equity interest in Shanghai Greenwoods. As confirmed by Shanghai 
Greenwoods, no single investor holds 30% or more interests in any of the individual funds managed 
by Shanghai Greenwoods. As for the Yikun Ruijian Fund, Mr. Ma Fuquan (馬福泉), Mr. Ma Hanyong 
(馬漢永) and Mr. Ma Hanxi (馬漢喜), all being natural persons, each hold 30% or more of the equity 
interest in the Yikun Ruijian Fund.
To the best of our knowledge and after making all reasonable enquiries, each of the Huatai Ultimate 
Clients is an independent third party of (i) the Company, the connected person or the associates 
thereof, and (ii) HTCI, HTFH and the companies which are members of the same group of HTCI.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in 
connection with the Client TRS order placed by the Huatai Ultimate Clients. Pursuant to the terms of 
the contracts of the Back-to-back TRS and the Client TRS, during the tenor of the Back-to-back TRS 
and the Client TRS, subject to customary fees and commissions, all economic returns of the Offer 
Shares will be ultimately passed to the Huatai Ultimate Clients through the Back-to-back TRS and the 
Client TRS and all economic loss shall be ultimately borne by the Huatai Ultimate Clients. HTCI will 
not take any economic return or bear any economic loss in relation to the Offer Shares.

<<<PAGE 27>>>
– 27 –
Investment in the Back-to-back TRS and the Client TRS is similar to the investment in a qualified 
domestic institutional investor fund (“QDII”) in the way that the Huatai Ultimate Clients would reap 
all the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through 
the exchange rate exposure on both the notional value of the investment and the profit and loss of the 
investment. In contrast, the profit and loss of the Back-to-back TRS and the Client TRS factor into 
account the fluctuation in RMB exchange rate upon termination of the Client TRS by converting the 
profit and loss using the current exchange rate at the time of termination. As such, the Huatai Ultimate 
Clients would bear the exchange rate exposure of the profit and loss on settlement date.
The Huatai Ultimate Clients may exercise an early termination right to terminate the Client TRS at 
any time from the issue date of the Client TRS which should be on or after the date on which the 
Offer Shares are listed on the Stock Exchange at their own discretions. Upon the termination upon 
maturity or early termination of the Client TRS by the Huatai Ultimate Clients, HTCI will dispose the 
Offer Shares on the secondary market and the Huatai Ultimate Clients will receive a final settlement 
amount in cash in accordance with the terms and conditions of the Back-to-back TRS and the Client 
TRS which should have taken into account all the economic returns or economic loss in relation to 
the Offer Shares. If upon the maturity of the Client TRS, the Huatai Ultimate Clients intend to extend 
the investment period, subject to further agreement between Huatai Securities and the relevant Huatai 
Ultimate Clients, the term of the Client TRS could be extended by way of a new issuance or a tenor 
extension. Accordingly, Huatai Securities will extend the term of the Back-to-back TRS by way of a 
new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and 
pass through the economic exposure to the Huatai Ultimate Clients, each being an onshore client who 
places a Client TRS order with Huatai Securities in connection with the IPO of the Company. HTCI 
will not exercise the voting right of the Offer Shares during the tenor of the Back-to-back TRS.
During the life of the Client TRS and Back-to-back TRS, HTCI may continue to hold the Offer Shares 
in its custodian account, or to hold some or all of the Offer Shares in a prime brokerage account for 
stock borrowing purposes, where HTCI will lend out its holding of underlying Offer Shares in the form 
of stock borrowing loans consistent with market practice to lower its finance costs, provided that HTCI 
has the ability to call back the Offer Shares on loan at any time in order to satisfy its obligations under 
the Back-to-back TRS to ensure the economic interests are ultimately passed to the Huatai Ultimate 
Clients.
5.	
Each of CMBI and CMS is distributor of the Global Offering.
Bosera AM is held as to 55% by Bosera Asset Management Co., Ltd. and 45% by China Merchants 
Fund Management Co., Limited. China Merchants Securities Co., Ltd. (“CMSC”) currently holds 
49% of the equity interest of Bosera Asset Management Co., Ltd. and 45% of the equity interest of 
China Merchants Fund. CMS is a wholly-owned subsidiary of CMSC. Therefore, Bosera AM is a 
member of same group of companies as CMS and CMSC. Bosera AM intends to subscribe and hold 
the Offer Shares in its capacity as the discretionary fund manager on behalf of its sub-funds (namely, 
Bosera China New Opportunities Fund SP, Bosera Growth Premium Global Equity Strategy Fund SP, 
KB China Mainland FD Bosera, Bosera Growth Premium Global Equity Strategy Fund SP2, Bosera 
Growth Premium Global Equity Strategy Fund SP3, Bosera Growth Premium Global Equity Strategy 
Fund SP4), which are all independent third parties. To the best knowledge of Bosera AM after due 
enquiry, each of the sub-funds is an independent third party of Bosera AM and each of CMBI and 
CMS, and the companies which are members of the same group of companies as each of CMBI 

<<<PAGE 28>>>
– 28 –
and CMS. No single ultimate beneficial owner holds 30% or more interest in Bosera China New 
Opportunities Fund SP or KB China Mainland FD Bosera. The ultimate beneficial owner holding 
30% or more interest in (i) Bosera Growth Premium Global Equity Strategy Fund SP is Guo Feng 
(郭峰), holding approximately 48.9951%; (ii) Bosera Growth Premium Global Equity Strategy Fund 
SP2 is Guangdong Dongfang Precision Science & Technology Co., Ltd (Ticker: 002611 CH), holding 
approximately 47.42%; (iii) Bosera Growth Premium Global Equity Strategy Fund SP3 is HUANG 
Liya (黃麗亞), holding 100%; and (iv) Bosera Growth Premium Global Equity Strategy Fund SP4 is 
Guangdong Dongfang Precision Science & Technology Co., Ltd (Ticker: 002611 CH), holding 100%. 
Each such ultimate beneficial owner is an independent third party of Bosera AM and each of CMBI 
and CMS, and the companies which are members of the same group of companies as each of CMBI 
and CMS.
6.	
China Universal (HK) is a member of the same group of companies as Orient Securities.
China Universal (HK) is a wholly owned subsidiary of China Universal Asset Management Co., Ltd. 
(匯添富基金管理股份有限公司). China Universal (HK) is among the first group of Chinese fund 
management company subsidiaries established outside of Chinese Mainland. China Universal (HK) 
is licensed by the Securities and Futures Commission of Hong Kong to carry on Type 1 (Dealing in 
Securities), Type 4 (Advising on Securities) and Type 9 (Asset Management) regulated activities under 
Part V of the Securities and Futures Ordinance.
China Universal (HK) manages investment funds, provides investment advisory services, and manages 
discretionary accounts. The subscription of the Offer Shares as a cornerstone investor will be made 
by China Universal (HK) in its capacity as the investment manager on a discretionary basis for and on 
behalf of following fund(s) and/or discretionary account(s): (i) Better Supply Chain (HK) Holdings 
Co., Limited; (ii) LC Logistics, Inc; (iii) Poly Legend International Limited; (iv) Excellent Tide 
Securities Limited for and on behalf of Excellent Tide Eurasia OFC — Excellent Tide Eurasia No.1 
Fund; and (v) China Universal Special Situation Fund SPC — CUAM Flexible Strategy Fund SP.
To the best knowledge and belief of China Universal (HK), PENG Zimei holds 30% or more interest 
in Better Supply Chain (HK) Holdings Co., Limited; XU Xin and LI Yan hold 30% or more interest in 
LC Logistics, Inc; Yang Peilin holds 30% or more interest in Poly Legend International Limited; HUA 
Zhongjie and ZHANG Ping hold 30% or more interest in Excellent Tide Eurasia OFC — Excellent 
Tide Eurasia No.1 Fund; and no single ultimate beneficial owner holds 30% or more interest in China 
Universal Special Situation Fund SPC — CUAM Flexible Strategy Fund SP. To the best knowledge 
and belief of China Universal (HK), they are third parties independent of the Company.
7.	
China Asset Management is owned as to 62.2% by CITIC Securities Company Limited, which is 
holding company of CITIC Brokerage. China Asset Management is a member of the same group of 
companies as CITICS Brokerage.
China Asset Management is, on a discretionary basis, an investment advisor and a delegate of the 
investment manager of its underlying clients (“China Asset Management Ultimate Clients”) and 
manages assets (in its capacity as an investment advisor of the China Asset Management Ultimate 
Clients) and executes trades (in its capacity as a delegate of the investment manager of China 
Asset Management Ultimate Clients) for on behalf of China Asset Management Ultimate Clients, 
namely CHINAAMC CHINA FOCUS FUND, the ultimate beneficial owner of which is Manulife 
(International) Limited, holding 72.20% interest therein.

<<<PAGE 29>>>
– 29 –
To the best knowledge of China Asset Management HK after making all reasonable enquiries, (i) each 
of the China Asset Management HK Ultimate Clients is an independent third party of the Company, 
its subsidiaries, its substantial shareholders, CITIC Brokerage, China Asset Management and the 
companies which are members of the same group of companies as CITIC Brokerage; and (ii) China 
Asset Management is not a collective investment scheme which is not authorised by the SFC.
8.	
GTJAS and Haitong Securities are distributors in connection with of the Global Offering. Fullgoal 
HK is a wholly owned subsidiary of Fullgoal Fund, which is owned by Guotai Haitong Securities 
Co., Ltd. (stock code: 2611.HK/601211.SH) (“Guotai Haitong”) as to 27.775%. GTJAS, one of the 
distributors of the Global Offering, is a subsidiary of Guotai Haitong. Haitong Securities, a distributor 
in connection with the Global Offering, is also a subsidiary of Guotai Haitong. As advised by Fullgoal 
HK and Fullgoal Fund, each of Fullgoal HK and Fullgoal Fund is considered as a member of the same 
group of companies as GTJAS and Haitong Securities and therefore is a “connected client” of GTJAS 
and Haitong Securities for the purpose of paragraph 1B of the Placing Guidelines.
To the best of its knowledge after due enquiry, save as the internal funds from Fullgoal in China 
Merchants Bank-Fullgoal Hong Kong Equity Select Hybrid Fund (QDII) (“Fullgoal HK Equity 
Select”), with the proprietary capital contribution not exceeding 0.05% of the total fund size of 
Fullgoal HK Equity Select, each of the other underlying clients and their respective ultimate beneficial 
owners is an independent third party of Fullgoal Fund, HTI and their respective group companies. 
Fullgoal Fund will hold the Offer Shares in its capacity as discretionary investment manager on behalf 
of the underlying clients includes Fullgoal Hong Kong Equity Select, Fullgoal HK Equity Select, 
CMB-Fullgoal Blue Chip Selected Equity Fund (QDII) and ICBC Fullgoal Global Technology & 
Internet Fund. To the best knowledge of Fullgoal Fund after due enquiry, no investor holds 30% or 
more interest in any of such underlying clients.
9.	
Please refer to Note 5 above for the relationship among GTJAS, Haitong Securities and Fullgoal AM.
Fullgoal AMHK is a member of the same group of companies as HTI. To the best of its knowledge 
after due enquiry, each of its underlying clients and their respective ultimate beneficial owners is 
an independent third party of Fullgoal AMHK, HTI and their respective group companies. Fullgoal 
AMHK will hold the Offer Shares in its capacity as discretionary investment manager on behalf of 
such underlying clients, details of which are set out below:
(i)	
Fullgoal Asset Management (HK) Limited SUB A/C HI-Aktien China 1-Sfonds — Save for 
A European pension fund, no other ultimate beneficial owner holds more than 30% of interest 
therein.
(ii)	
Fullgoal Hong Kong and China Equity Fund — Save for The University of Hong Kong, no other 
ultimate beneficial owner holds more than 30% of interest therein.
(iii)	
Fullgoal China Growth Select Fund — Save for Zhao Xueming, no other ultimate beneficial 
owner holds more than 30% of interest therein.
(iv)	
Fullgoal China Opportunities Fund Fund — Save for China Everbright Fortune Investment 
Limited, L Industries Limited and Orient Sun Rise Fund Series SPC-Orient Sun Rise Enhanced 
Balanced Fund Segregated Portfolio, no other ultimate beneficial owner holds more than 30% of 
interest therein.

<<<PAGE 30>>>
– 30 –
(v)	
Fullgoal China Small-Mid Cap Growth Fund is a SFC authorized fund (CE no.: BNY686) — 
No investor holds 30% or more interest therein.
(vi)	
BMO Greater China Fund — No investor holds 30% or more interest therein.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate 
such Offer Shares in the International Offering to the connected clients listed above. The 
allocation of Offer Shares to such connected clients is in compliance with all the conditions 
under the consent granted by the Stock Exchange.
Allocations under the Employee Preferential Offering
Of the 11,554,750 Offer Shares initially being offered under the International Offering, 
313,600 Offer Shares, representing approximately 2.71% of the Offer Shares initially 
available for subscription under the International Offering, are available for subscription 
as Employee Reserved Shares by the Eligible Employees on a preferential basis under the 
Employee Preferential Offering according to Rule 10.01 of the Listing Rules. For details, 
please refer to the section headed “Structure of the Global Offering — The International 
Offering — Employee Preferential Offering” of the Prospectus.
313,600 Offer Shares have been placed to 11 Eligible Employees pursuant to the Employee 
Preferential Offering, representing approximately 2.44% of the total number of Offer Shares 
initially available under the Global Offering (before exercise of the Over-allotment Option). 
Each Eligible Employee confirms that he/she is and remains as an employee as of the date 
of the Prospectus and is not a core connected person of the Company.
Allocation of H Shares to existing minority Shareholders and their close associates
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted 
to the Company, a waiver from strict compliance with the requirements under Rule 10.04 
and consent under Paragraph 1C(2) of Appendix F1 to the Listing Rules to permit H Shares 
in the International Offering to be placed to certain existing minority Shareholders (together, 
the “Permitted Existing Shareholders”) and/or their close associates, on the conditions 
that each of them:
(a)	
holds less than 5% of the voting rights in our Company prior to the completion of the 
Global Offering;
(b)	 is not and will not be, a core connected person of our Company or any close associate 
of any such core connected person immediately prior to or following the Global 
Offering;

<<<PAGE 31>>>
– 31 –
(c)	
does not have the power to appoint any Director and/or have any other special rights;
(d)	 allocation to the Permitted Existing Shareholders and their close associates will 
not affect our Company’s ability to satisfy the public float requirement under Rule 
19A.13A of the Listing Rules; and
(e)	
that no preferential treatment has been, nor will be, given to any of the Permitted 
Existing Shareholders or their close associates by virtue of their relationship with our 
Company in any allocation in the International Offering.
Please refer to the section headed “Waivers from Strict Compliance with the Listing Rules 
— Allocation of H Shares to Existing Minority Shareholders and/or Their Close Associates” 
in the Prospectus for further details of the waiver and consent.
Each of the Sole Sponsor and the Company has provided the required confirmations as 
elaborated in the Prospectus. In particular, as the Company’s A Shares are listed on the 
STAR Market of Shanghai Stock Exchange since April 2021, the Company has a highly 
extensive base of existing Shareholders and disclosure of details of allocations to all 
existing minority Shareholders will not be meaningful to investors, the proposed disclosure 
threshold, i.e. details of the allocation to the existing minority Shareholders holding more 
than 1% of the issued share capital of the Company immediately prior to the completion of 
the Global Offering will be disclosed in this announcement, is appropriate.
All allocations of Offer Shares to the existing minority Shareholders are in compliance with 
all the conditions under the waiver and consent granted by the Stock Exchange.

<<<PAGE 32>>>
– 32 –
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong 
Limited (the “Stock Exchange”) and Hong Kong Securities Clearing Company Limited 
(“HKSCC”) take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part 
of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in 
or into the United States (including its territories and possessions, any state of the United 
States and the District of Columbia). This announcement does not constitute or form 
a part of any offer or solicitation to purchase or subscribe for securities in the United 
States. The securities mentioned herein have not been, and will not be, registered under 
the United States Securities Act of 1933, as amended (the “U.S. Securities Act”). The 
securities may not be offered or sold in the United States except pursuant to an exemption 
from the registration requirements of the U.S. Securities Act and in compliance with any 
applicable state securities laws, or outside the United States unless in compliance with 
Regulation S under the U.S. Securities Act. There will be no public offer of securities in 
the United States.
The Offer Shares may only be offered and sold outside the United States in offshore 
transactions in reliance on Regulation S under the U.S. Securities Act. No public offering 
of the Offer Shares will be made in the United States.
This announcement is for information purposes only and does not constitute an invitation 
or offer to acquire, purchase or subscribe for securities. This announcement is not a 
prospectus. Potential investors should read the Prospectus dated June 17, 2026 issued by 
Circuit Fabology Microelectronics Equipment Co., Ltd. for detailed information about the 
Global Offering described below before deciding whether or not to invest in the H Shares 
thereby being offered. Any investment decision in relation to the Offer Shares should be 
taken solely in reliance on the information in the Prospectus.
*  Potential investors of the Offer Shares should note that the Sole Sponsor and the 
Sponsor-OC (for itself and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate the Hong Kong Underwriting Agreement with immediate effect upon 
the occurrence of any of the events set out in the section headed “Underwriting — 
Underwriting Arrangements and Expenses — The Hong Kong Public Offering — Grounds 
for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on 
the Listing Date (which is currently expected to be on June 26, 2026).

<<<PAGE 33>>>
– 33 –
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering (before any exercise of the 
Over-allotment Option), the total market value of the H Shares to be held by the public is 
expected to be approximately HK$3,244.7 million, calculated based on the final Offer Price 
of HK$252.73 per H Share, which is higher than the prescribed expected market value of H 
Shares required to be held in public hands of not less than HK$3,000,000,000 under Rule 
19A.13A(2)(b) of the Listing Rules, thereby satisfying Rule 19A.13A(2) of the Listing 
Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following 
the Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall 
not be counted towards the free float of the H Shares of the Company at the time of Listing. 
Based on the final Offer Price of HK$252.73 per H Share, the Company confirms the free 
float requirement under Rule 19A.13C(2)(b) of the Listing Rules is satisfied.
The Directors confirm that, immediately following completion of the Global Offering (before 
any exercise of the Over-allotment Option): (i) no placee will, individually, be placed 
more than 10% of the enlarged issued share capital of the Company immediately after the 
Global Offering; (ii) there will not be any new substantial Shareholder under the Listing 
Rules immediately after the Global Offering; (iii) the three largest public shareholders of 
the Company do not hold more than 50% of the H Shares in public hands at the time of the 
Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will 
be at least 300 Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the 
Listing Rules.

<<<PAGE 34>>>
– 34 –
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, 
June 26, 2026 (Hong Kong time), provided that the Global Offering has become 
unconditional and the right of termination described in the section headed “Underwriting — 
Underwriting Arrangements and Expenses — The Hong Kong Public Offering — Grounds 
for Termination” in the Prospectus has not been exercised. Investors who trade the H Shares 
on the basis of publicly available allocation details prior to the receipt of H Share certificates 
or prior to the H Share certificates becoming valid evidence of title do so entirely at their 
own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on June 26, 
2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on June 26, 2026 (Hong Kong time). The H Shares will be 
traded in board lots of 50 H Shares each, and the stock code of the H Shares will be 9630.
By order of the Board
CIRCUIT FABOLOGY
MICROELECTRONICS EQUIPMENT CO., LTD.
Ms. Cheng Zhuo
Chairman of the Board and Executive Director
Hong Kong, June 25, 2026
As at the date of this announcement, the Board comprises: (i) Ms. Cheng Zhuo, Mr. Fang Lin and Ms. Wei 
Yongzhen as executive Directors; (ii) Mr. Zhao Lingyun, Mr. Zhou Chijun and Mr. Liu Feng as non-executive 
Directors; and Ms. Zhou Yana, Mr. Zhong Qi and Mr. Wong Lok Tak as independent non-executive Directors.
