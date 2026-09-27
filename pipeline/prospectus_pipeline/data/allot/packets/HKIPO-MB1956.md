# 配发结果公告抽取任务：1956.HK Beijing Zhongke WengeAI Science and Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**25/06/2026 21:27**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0625/2026062501938.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1956.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as 
those defined in the prospectus dated June 17, 2026 (the “Prospectus”) of Beijing Zhongke WengeAI Science and 
Technology Co., Ltd.* (北京中科聞歌科技股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the Prospectus for 
detailed information about the Global Offering described below before deciding whether or not to invest in the Offer 
Shares. Any investment decision in relation to the Offer Shares should be taken solely in reliance on the information 
provided in the Prospectus.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited 
as stabilizing manager (the “Stabilizing Manager”), its affiliates or any person acting for it, on behalf of the 
Underwriters, may effect transactions with a view to stabilizing or supporting the market price of the Shares at a 
level higher than that which might otherwise prevail for a limited period after the Listing Date. However, there is no 
obligation on the Stabilizing Manager, its affiliates or any person acting for it to conduct any such stabilizing action, 
which, if commenced, will be done at the sole and absolute discretion of the Stabilizing Manager, its affiliates or any 
person acting for it and may be discontinued at any time. Any such stabilization activity is required to be brought to an 
end on Thursday, July 23, 2026, being the 30th day after the last date for lodging of applications under the Hong Kong 
Public Offering. Such stabilization action, if taken may be effected in all jurisdictions where it is permissible to do so, 
in each case in compliance with all applicable laws, rules and regulatory requirements, including the Securities and 
Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities 
and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
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
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to term and conditions set out in 
the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not 
resident in Hong Kong.
Potential investors of the Offer Shares should note that the Sole Sponsor and Overall Coordinator (for itself and 
on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the paragraph 
headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently 
expected to be on Friday, June 26, 2026).

<<<PAGE 2>>>
2
Beijing Zhongke WengeAI Science and Technology Co., Ltd.*
北京中科聞歌科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under the Global 
Offering
:
14,834,600 H Shares (subject to the Over-
 allotment Option)
Number of Hong Kong Offer Shares
:
2,967,000 H Shares (as adjusted after 
 reallocation)
Number of International Offer Shares
:
11,867,600 H Shares (as adjusted after 
 Reallocation and subject to the 
 Over-allotment Option)
Offer Price :
HK$60.70 per H Share (plus 
 brokerage of 1.0%, SFC transaction 
 levy of 0.0027%, AFRC transaction 
 levy of 0.00015% and the Stock 
 Exchange trading fee of 0.00565%)
Nominal value
:
RMB1.0 per H Share 
Stock code
:
1956
Sole Sponsor, Sponsor-Overall Coordinator, Overall Coordinator, Joint Global Coordinator, 
Joint Bookrunner and Joint Lead Manager
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Global Coordinators, Joint Bookrunners, Joint Lead Managers
Joint Bookrunners, Joint Lead Managers

<<<PAGE 3>>>
3
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in prospectus dated June 17, 2026 (the “Prospectus”) of Beijing Zhongke 
WengeAI Science and Technology Co., Ltd.* (北京中科聞歌科技股份有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company Information
Stock code
1956
Stock short name
WENGE AI
Dealings commencement date
June 26, 2026*
* 
see note at the end of the announcement
Price Information
Offer Price
HK$60.70
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the Over-allotment Option)
14,834,600
Number of Offer Shares in Hong Kong Public Offering (after reallocation)
2,967,000
Number of Offer Shares in International Offering 
 (after reallocation and before exercise of the Over-allotment Option)
11,867,600
Number of issued Shares upon Listing (before exercise of the Over-
 allotment Option)
173,101,207
Number of Shares over-allocated*
1,335,000
* 
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases in the 
secondary market at prices that do not exceed the Offer Price or through deferred delivery or a combination of 
these means. In the event the Over-allotment Option is exercised, an announcement will be made on the Stock 
Exchange’s website.
Proceeds
Gross proceeds Note 1
HK$900.5 million
Less: Estimated listing expenses payable based on Offer Price
HK$73.6 million
Net proceeds
HK$826.9 million Note 2
Note:(1) 
Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option 
(if any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the 
Prospectus on a pro rata basis.
(2) 
The amount included in this announcement has been subject to rounding adjustments.

<<<PAGE 4>>>
4
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
195,072
No. of successful applications
14,835
Subscription level
5,966.78 times
Claw-back triggered
Yes
No. of Offer Shares initially available under the Hong Kong Public 
 Offering
741,800
No. of Offer Shares reallocated from the International Offering 
 (claw-back)
2,225,200
Final no. of Offer Shares under the Hong Kong Public Offering
2,967,000
% of Offer Shares under the Hong Kong Public Offering to the 
 Global Offering
20.00%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can 
refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
147
Subscription Level
20.70 times
No. of Offer Shares initially available under the International Offering
14,092,800
No. of Offer Shares reallocated to the Hong Kong Public Offering  
(claw-back)
2,225,200
Final no. of Offer Shares under the International Offering (assuming 
the Over-allotment Option is not exercised)
11,867,600
% of Offer Shares under the International Offering to the Global 
 Offering
80.00%
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly by 
the Company, any of the Directors, chief executive, supervisors of the Company, Single Largest 
Group of Shareholders, substantial Shareholders, existing Shareholders of the Company or any of 
its subsidiaries or their respective close associates; and (ii) none of the placees and the public who 
have purchased the Offer Shares are accustomed to taking instructions from the Company, any of 
the Directors, chief executive, supervisors of the Company, Single Largest Group of Shareholders, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or their 
respective close associates in relation to the acquisition, disposal, voting or other disposition of 
Shares registered in his/her/its name or otherwise held by him/her/it.

<<<PAGE 5>>>
5
The Overall Coordinators and the Directors confirm that the allocation cap pursuant to paragraph 9 
of Chapter 4.14 of the Guide for New Listing Applicants has not been exceeded.
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of 
Offer Shares 
allocated
% of Offer 
Shares 
(assuming 
the Over 
allotment 
Option is not 
exercised)
% of total 
issued share 
capital after 
the Global 
Offering 
(assuming 
the Over 
allotment 
Option is not 
exercised)
Existing 
Shareholders 
or their close 
associates
China Orient Enhanced Income Fund
774,400
5.22%
0.45%
No
Harvest Global Investments Limited 
(嘉實國際資產管理有限公司)
774,400
5.22%
0.45%
No
First Seafront Asset Management 
Limited (前海國際基金管理有限公
司)
645,200
4.35%
0.37%
No
Guohui (HK) Holdings Co., Limited 
(國惠(香港)控股有限公司)
645,200
4.35%
0.37%
No
Huatai Capital Investment Limited (華
泰資本投資有限公司)
645,200
4.35%
0.37%
No
CMBC International Investment (HK) 
Limited (民銀國際投資(香港)有限
公司)
516,200
3.48%
0.30%
No
Total
4,000,600
26.97%
2.31%

<<<PAGE 6>>>
6
Allottees with waiver/consents obtained
Investor
No. of 
Offer 
Shares 
allocated
% of Offer 
Shares
% of total 
issued H 
Shares 
after the 
Global 
Offering 
(assuming 
the Over 
allotment 
Option 
is not 
exercised)
% of total 
issued 
share 
capital 
after the 
Global 
Offering 
(assuming 
the Over 
allotment 
Option 
is not 
exercised)
Relationship
Allotees with consent under paragraph 1C(1) of Appendix F1 to the Listing Rules (the 
“Placing Guidelines”) in relation to allocations to connected clients(Note 1)
ABCI Asset Management 
Limited (“ABCI AM”)
26,400
0.178%
0.015%
0.015%
Connected 
client 
investing as a 
placee
China Galaxy 
International 
Investment Co., Ltd 
(“CGII”)
3,200
0.022%
0.002%
0.002%
Connected 
client 
investing as a 
placee
CICC Financial Trading 
Limited (“CICC FT”)
5,600
0.038%
0.003%
0.003%
Connected 
client 
investing as a 
placee
Note:
1. 
Saved as listed out, the H Shares placed to such allottees are held on behalf of independent third parties (as 
defined in Chapter 4.15 of the Guide for New Listing Applicants and are in compliance with all the conditions 
under the consent granted by the Stock Exchange. For details of the consent under paragraph 1C(1) of the 
Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations to 
connected clients, please refer to the section headed “Additional Information – Placing to connected clients with 
a prior consent under paragraph 1C(1) of the Placing Guidelines” in this announcement.

<<<PAGE 7>>>
7
LOCK-UP UNDERTAKINGS
Key Persons (as defined under Rule 18C.14 of the Listing Rules)
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
issued H 
Shares in the 
Company 
upon 
Listing(Note 1)
% of total 
issued 
Shares in the 
Company 
upon 
Listing(Note 1)
Last day 
subject to 
the lock-up 
undertakings 
(Note 1)
Dr. Wang Lei (“Dr. Wang”) (Note 2)
2,816,151
1.63%
1.63%
June 25, 2027
Beijing Zhongke Sanshi Technology 
Development Co., Ltd. (北京中科三
石科技發展有限公司) (“Zhongke 
Sanshi”) (Note 3)
26,231,007
15.15%
15.15%
June 25, 2027
Hainan Xinyi Technology Center 
(Limited Partnership) (海南新移
科技中心(有限合夥)) (“Hainan 
Xinyi”) (Note 3)
1,055,893
0.61%
0.61%
June 25, 2027
Wenge Zhicai (Tianjin) Technology 
Center (Limited Partnership) (聞歌
智才(天津)科技中心(有限合夥)) 
(“Wenge Zhicai”) (Note 3)
6,268,709
3.62%
3.62%
June 25, 2027
Wenge Jiangcai (Tianjin) Technology 
Center (Limited Partnership) (聞歌
匠才(天津)科技中心(有限合夥)) 
(“Wenge Jiangcai”) (Note 3)
974,524
0.56%
0.56%
June 25, 2027
Dr. Luo Yin (“Dr. Luo”) (Note 4)
7,339,783
4.24%
4.24%
June 25, 2027
Mr. Qu Baoyu (“Mr. Qu”) (Note 5)
10,000
0.01%
0.01%
June 25, 2027
Mr. Ma Li (“Mr. Ma”) (Note 6)
200,000
0.12%
0.12%
June 25, 2027
Mr. Zheng Chaomin (“Mr. Zheng”) 
(Note 6)
100,000
0.06%
0.06%
June 25, 2027
Dr. Xu Nan (“Dr. Xu”) (Note 6)
25,000
0.01%
0.01%
June 25, 2027
Mr. Wang Yigang (“Mr. Wang”) (Note 6)
120,000
0.07%
0.07%
June 25, 2027
Beijing Zhongzi Investment 
Management Company Limited 
(北京中自投資管理有限公司) 
(“Zhongzi Investment”) (Note 7)
9,210,056
5.32%
5.32%
June 25, 2027
Prof. Zeng Dajun (“Prof. Zeng”) (Note 7)
3,837,523
2.22%
2.22%
June 25, 2027

<<<PAGE 8>>>
8
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
issued H 
Shares in the 
Company 
upon 
Listing(Note 1)
% of total 
issued 
Shares in the 
Company 
upon 
Listing(Note 1)
Last day 
subject to 
the lock-up 
undertakings 
(Note 1)
Wenge Hongcai (Beijing) Technology 
Center (Limited Partnership) (聞歌
鴻才(北京)科技中心(有限合夥)) 
(“Wenge Hongcai”) (Note 8)
671,991
0.39%
0.39%
June 25, 2027
Zhongke Youcai (Hainan) Science 
and Technology Center (Limited 
Partnership) (中科優才(海南)科
技中心(有限合夥)) (“Zhongke 
Youcai”) (Note 8)
9,181,182
5.30%
5.30%
June 25, 2027
Subtotal
68,041,819
39.31%
39.31%
Notes:
1. 
Pursuant to the applicable PRC law, within the 12 months following the Listing Date, all existing Shareholders 
(including the Pre-IPO Investors) are prohibited from disposing of any of the Shares held by them. Pursuant to 
Rule 18C.14(1) of the Listing Rules, the required lock-up period commences on the date by reference to which 
disclosure of their shareholdings in the Company is made in the Prospectus and end on the date upon the expiry 
of 12 months from the Listing Date, being the same date on which the restriction against disposal of Shares 
under the applicable PRC laws ends. And assuming the Over-allotment Option is not exercised.
2. 
Dr. Wang, the founder, chairman of our Board and executive Director, is a key person responsible for our 
technical operations and/or the research and development of our Specialist Technology Products who is subject 
to lock-up requirements pursuant to Rule 18C.14 of the Listing Rules.
3. 
Each of Zhongke Sanshi, Hainan Xinyi, Wenge Zhicai and Wenge Jiangcai is company or employee share 
platform controlled by Dr. Wang.
4. 
Dr. Luo, the founder, executive Director, chief executive officer, senior management and core R&D team 
member who is subject to lock-up requirements pursuant to Rule 18C.14 of the Listing Rules.
5. 
Mr. Qu, the executive Director and senior management and who is subject to lock-up requirements pursuant to 
Rule 18C.14 of the Listing Rules and the number of shares representing the underlying shares interested by Mr. 
Qu under the Pre-IPO Share Option Scheme.
6. 
Each of Mr. Ma, Mr. Zheng, Dr. Xu, Mr. Wang is the senior management or core R&D team members who 
is subject to lock-up requirements pursuant to Rule 18C.14 of the Listing Rules and the number of shares 
representing the underlying shares interested by Mr. Ma, Mr. Zheng, Dr. Xu, Mr. Wang under the Pre-IPO Share 
Option Scheme.
7. 
Prof. Zeng is the founder and one of the Single Largest Group of Shareholders and Zhongzi Investment is the 
founder, which is subject to the lock-up requirement to Rule 18C.14 of the Listing Rules.
8. 
Each of Wenge Hongcai and Zhongke Youcai is employee share platform where the Company’s executive 
Directors, senior management and core R&D team members hold partnership interests and which is subject to 
the lock-up requirements pursuant to Rule 18C.14 of the Listing Rules.

<<<PAGE 9>>>
9
Pathfinder SIIs
Name
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up
undertakings 
upon
Listing
% of total 
issued H 
Shares in the 
Company 
upon Listing 
(Note 1)
% of total 
issued 
Shares in the 
Company 
upon Listing 
(Note 1)
Last day 
subject to 
the lock-up 
undertakings
 (Note 1)
CDBC Manufacturing Industry 
Transformation and Upgrading Fund 
(Limited Partnership)國開製造業
轉型升級基金(有限合夥) (“CDBC 
MTU Fund”)
9,170,507
5.30%
5.30%
June 25, 2027
China Internet Investment Fund 
(Limited Partnership) (中國互聯
網投資基金(有限合夥) (“China 
Internet Investment”)
5,803,255
3.35%
3.35%
June 25, 2027
SCGC Investors
Shenzhen Capital Group Co., Ltd. 
(深圳市創新投資集團有限公司) 
(“SCGC”)
3,588,502
2.07%
2.07%
June 25, 2027
Beijing Hongtu Tech Technology 
Entrepreneurship Investment Center 
(Limited Partnership) (北京紅土
科技創業投資中心(有限合夥) 
(“Hongtu Tech”)
3,588,502
2.07%
2.07%
June 25, 2027
Subtotal
22,150,766
12.79%
12.79%
Notes:
1. 
Pursuant to the applicable PRC law, within the 12 months following the Listing Date, all existing Shareholders 
(including the Pre-IPO Investors) are prohibited from disposing of any of the Shares held by them. Pursuant to 
Rule 18C.14(2) of the Listing Rules, the required lock-up period commences on the date by reference to which 
disclosure of their respective shareholdings in the Company is made in the Prospectus and ends on the date 
upon the expiry of six months from the Listing Date i.e. December 26, 2026. And assuming the Over-allotment 
Option is not exercised.
2. 
Each of the Shareholders listed in the above table is a Pathfinder SII of the Company as defined under Chapter 
2.5 of the Guide for New Listing Applicants.

<<<PAGE 10>>>
10
Existing Shareholders (other than the Key Persons and the Pathfinder SIIs)
Name
Number of 
Shares
held in the 
Company
subject to 
lock-up
undertakings 
upon Listing 
(Note 1)
% of total 
issued H 
Shares in the 
Company 
upon Listing 
(Note 1)
% of total 
issued 
Shares in the 
Company 
upon Listing 
(Note 1)
Last day 
subject to 
the lock-up 
undertakings 
(Note 2)
Beijing Artificial Intelligence 
Industry Investment Fund (Limited 
Partnership) (北京市人工智能產業
投資基金(有限合夥))
6,428,571
3.7138%
3.7138%
June 25, 2027
Shenzhen Hengbang Zhiyuan No. 5 
Investment Partnership Enterprise 
(Limited Partnership) (深圳市恒邦
致遠五號投資合夥企業(有限合夥))
5,293,136
3.0578%
3.0578%
June 25, 2027
Infotech National Emerging Industry 
Venture Investment Guidance Fund 
(Limited Partnership) (盈富泰克國
家新興產業創業投資引導基金(有限
合夥))
4,514,932
2.6083%
2.6083%
June 25, 2027
Shenzhen Shenbao Yiben Cultural 
Industry Equity Investment Fund 
Partnership (Limited Partnership) 
(深圳市深報一本文化產業股權投資
基金合夥企業(有限合夥))
3,627,033
2.0953%
2.0953%
June 25, 2027
Beijing Zhongke Chuangxing Hard 
Technology Venture Capital 
Partnership (Limited Partnership) 
(北京中科創星硬科技創業投資合夥
企業(有限合夥))
3,315,885
1.9156%
1.9156%
June 25, 2027
Shenzhen Hengbang Zhiyuan No. 20 
Venture Capital Partnership (Limited 
Partnership) (深圳市恒邦致遠二十
號創業投資合夥企業(有限合夥))
3,080,500
1.7796%
1.7796%
June 25, 2027
Shenzhen Hengbang Growth  
No. 10 Venture Capital Partnership 
Enterprise (Limited Partnership) (深
圳市恒邦成長十號創業投資合夥企
業(有限合夥))
3,023,263
1.7465%
1.7465%
June 25, 2027

<<<PAGE 11>>>
11
Name
Number of 
Shares
held in the 
Company
subject to 
lock-up
undertakings 
upon Listing 
(Note 1)
% of total 
issued H 
Shares in the 
Company 
upon Listing 
(Note 1)
% of total 
issued 
Shares in the 
Company 
upon Listing 
(Note 1)
Last day 
subject to 
the lock-up 
undertakings 
(Note 2)
Beijing Jinke Huisheng Venture 
Capital Partnership (Limited 
Partnership) (北京金科匯晟創業投
資合夥企業(有限合夥))
2,815,624
1.6266%
1.6266%
June 25, 2027
Fuzhou Youbang Technology Center 
(General Partnership) (撫州市友邦
科技中心(普通合夥))
2,763,749
1.5966%
1.5966%
June 25, 2027
National Science and Technology 
Achievement Transformation 
Entrepreneurship Investment Fund 
(Wuhan) Partnership Enterprise 
(Limited Partnership) (國科科技成
果轉化創業投資基金(武漢)合夥企
業(有限合夥))
2,501,601
1.4452%
1.4452%
June 25, 2027
Qingdao Xinding Gnaw Ge Jinwu 
Private Equity Investment Fund 
Partnership (Limited Partnership) 
(青島新鼎啃哥錦伍私募股權投資基
金合夥企業(有限合夥))
2,450,000
1.4154%
1.4154%
June 25, 2027
CCTV Integrated Media Industry 
Investment Fund (Limited 
Partnership) (央視融媒體產業投資
基金(有限合夥))
2,304,148
1.3311%
1.3311%
June 25, 2027
Beijing Zhongguancun Science City 
Technology Growth Investment 
Partnership Enterprise (Limited 
Partnership) (北京中關村科學城科
技成長投資合夥企業(有限合夥))
2,304,148
1.3311%
1.3311%
June 25, 2027
Qingdao Xindinggnanggexin Third 
Investment Partnership (Limited 
Partnership) (青島新鼎啃哥欣叁投
資合夥企業(有限合夥))
2,085,407
1.2047%
1.2047%
June 25, 2027
Zhuhai Daye Shengde Technology 
Management Center (Limited 
Partnership) (珠海大業盛德科技管
理中心(有限合夥))
2,031,840
1.1738%
1.1738%
June 25, 2027

<<<PAGE 12>>>
12
Name
Number of 
Shares
held in the 
Company
subject to 
lock-up
undertakings 
upon Listing 
(Note 1)
% of total 
issued H 
Shares in the 
Company 
upon Listing 
(Note 1)
% of total 
issued 
Shares in the 
Company 
upon Listing 
(Note 1)
Last day 
subject to 
the lock-up 
undertakings 
(Note 2)
Beijing Shijingshan District Modern 
Innovation Industry Development 
Fund Co., Ltd. (北京市石景山區現
代創新產業發展基金有限公司)
1,875,039
1.0832%
1.0832%
June 25, 2027
Beijing Phase II Zhongke Chuangxing 
Hard Technology Venture Capital 
Partnership (Limited Partnership) 
(北京二期中科創星硬科技創業投資
合夥企業(有限合夥))
1,794,251
1.0365%
1.0365%
June 25, 2027
Zhongke Liandong Chuangxin Equity 
Investment Fund (Shaoxing) 
Partnership (Limited Partnership) 
(中科聯動創新股權投資基金(紹興)
合夥企業(有限合夥))
1,794,251
1.0365%
1.0365%
June 25, 2027
Ruide Huihuang Investment Co., Ltd. 
(瑞得輝煌投資有限公司)
1,764,379
1.0193%
1.0193%
June 25, 2027
Qingdao Lanhai Fangzhou Venture 
Capital Fund Partnership (Limited 
Partnership) (青島藍海方舟創業投
資基金合夥企業(有限合夥))
1,764,379
1.0193%
1.0193%
June 25, 2027
Guoke Dacheng Kechuang Equity 
Investment Fund (Tianjin) 
Partnership Enterprise (Limited 
Partnership) (國科大成科創股權投
資基金(天津)合夥企業(有限合夥))
1,583,127
0.9146%
0.9146%
June 25, 2027
Guoke Xinxing Kechuang Equity 
Investment Fund (Tianjin) 
Partnership Enterprise (Limited 
Partnership) (國科新興科創股權投
資基金(天津)合夥企業(有限合夥))
1,583,127
0.9146%
0.9146%
June 25, 2027
Gongqingcheng Ruisheng Equity 
Investment Partnership Enterprise 
(Limited Partnership) (共青城瑞晟
股權投資合夥企業(有限合夥))
1,043,667
0.6029%
0.6029%
June 25, 2027

<<<PAGE 13>>>
13
Name
Number of 
Shares
held in the 
Company
subject to 
lock-up
undertakings 
upon Listing 
(Note 1)
% of total 
issued H 
Shares in the 
Company 
upon Listing 
(Note 1)
% of total 
issued 
Shares in the 
Company 
upon Listing 
(Note 1)
Last day 
subject to 
the lock-up 
undertakings 
(Note 2)
Beijing Zhongzi Innovation Artificial 
Intelligence Venture Capital Phase I 
Fund (Limited Partnership) (北京中
自創新人工智能創投一期基金(有限
合夥))
897,126
0.5183%
0.5183%
June 25, 2027
Beijing Guoke Dingzhi Equity 
Investment Center (Limited 
Partnership) (北京國科鼎智股權投
資中心(有限合夥))
897,126
0.5183%
0.5183%
June 25, 2027
Guizhou Fenghou Zhiyuan Venture 
Capital Center (Limited Partnership) 
(貴州豐厚智源創業投資中心(有限
合夥))
897,126
0.5183%
0.5183%
June 25, 2027
Liaoning Xinxing Phase II Cultural 
Entrepreneurship Investment Fund 
Partnership Enterprise (Limited 
Partnership) (遼寧新興二期文化創
業投資基金合夥企業(有限合夥))
725,407
0.4191%
0.4191%
June 25, 2027
Shenzhen Hengbang Growth  
No. 5 Venture Capital Partnership 
Enterprise (Limited Partnership) (深
圳市恒邦成長五號創業投資合夥企
業(有限合夥))
725,407
0.4191%
0.4191%
June 25, 2027
Shenzhen Shengrunda Investment Co., 
Ltd. (深圳聖潤達投資有限公司)
725,407
0.4191%
0.4191%
June 25, 2027
Beijing Wendan Technology Co., Ltd. 
(Limited Partnership) (北京文丹科
技有限合夥企業(有限合夥))
510,687
0.2950%
0.2950%
June 25, 2027
Yuxin Digital Technology (Henan) 
Equity Investment Fund Partnership 
(Limited Partnership) (豫信數科(河
南)股權投資基金合夥企業(有限合
夥))
500,000
0.2888%
0.2888%
June 25, 2027

<<<PAGE 14>>>
14
Name
Number of 
Shares
held in the 
Company
subject to 
lock-up
undertakings 
upon Listing 
(Note 1)
% of total 
issued H 
Shares in the 
Company 
upon Listing 
(Note 1)
% of total 
issued 
Shares in the 
Company 
upon Listing 
(Note 1)
Last day 
subject to 
the lock-up 
undertakings 
(Note 2)
Shenzhen Hengbang Zhiyuan No. 23 
Venture Capital Partnership (Limited 
Partnership) (深圳市恒邦致遠二十
三號創業投資合夥企業(有限合夥))
499,999
0.2888%
0.2888%
June 25, 2027
Xiyue Xinmei (Zhuhai) Investment 
Partnership Enterprise (Limited 
Partnership) (喜悅馨美(珠海)投資
合夥企業(有限合夥)
408,680
0.2361%
0.2361%
June 25, 2027
Subtotal
68,529,022
39.5892%
39.5892%
Notes:
1. 
Assuming the Over-allotment Option is not exercised.
2. 
The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws.
Cornerstone Investors
Investor
Number of 
shares held
in the 
Company 
subject
to lock-up
undertakings 
upon
listing
% of 
shareholding 
in the
Company 
subject to
lock-up 
undertakings
upon listing 
(assuming 
the Over 
allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings
China Orient Enhanced Income Fund
774,400
0.45%
December 25, 2026
Harvest Global Investments Limited (嘉
實國際資產管理有限公司)
774,400
0.45%
December 25, 2026
First Seafront Asset Management Limited 
(前海國際基金管理有限公司)
645,200
0.37%
December 25, 2026
Guohui (HK) Holdings Co., Limited (國
惠(香港)控股有限公司)
645,200
0.37%
December 25, 2026

<<<PAGE 15>>>
15
Investor
Number of 
shares held
in the 
Company 
subject
to lock-up
undertakings 
upon
listing
% of 
shareholding 
in the
Company 
subject to
lock-up 
undertakings
upon listing 
(assuming 
the Over 
allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings
Huatai Capital Investment Limited (華泰
資本投資有限公司)
645,200
0.37%
December 25, 2026
CMBC International Investment (HK) 
Limited (民銀國際投資(香港)有限公
司)
516,200
0.30%
December 25, 2026
Subtotal
4,000,600
2.31%
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
allotment 
Option)
Allotment 
as % of total 
Offer Shares 
(assuming 
no exercise 
of the Over-
allotment 
Option)
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
allotment 
Option)
Top 1
3,771,800
31.78%
25.43%
3,771,800
2.18%
Top 5
7,411,000
62.45%
49.96%
7,411,000
4.28%
Top 10
10,195,200
85.91%
68.73%
10,195,200
5.89%
Top 25
12,513,200
105.44%
84.35%
12,513,200
7.23%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 16>>>
16
H SHARE SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(aassuming 
no exercise 
of the Over-
allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(aassuming 
no exercise 
of the Over-
allotment 
Option)
Number of 
H Shares 
held upon 
Listing
% of total 
issued H 
Share capital 
upon Listing 
(aassuming 
no exercise 
of the Over-
allotment 
Option)
Number of 
Shares held 
upon Listing
Top 1
-
0.00%
0.00%
48,523,590
28.03%
48,523,590
Top 5
-
0.00%
0.00%
89,379,631
51.63%
89,379,631
Top 10
-
0.00%
0.00%
118,859,102
68.66%
118,859,102
Top 25
5,217,000
43.96%
35.17%
157,922,048
91.23%
157,922,048
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
(assuming 
no exercise 
of the Over-
allotment 
Option)
Allotment 
as % of total 
Offer Shares 
(assuming 
no exercise 
of the Over-
allotment 
Option)
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
(assuming 
no exercise 
of the Over-
allotment 
Option)
Top 1
-
0.00%
0.00%
48,523,590
48,523,590
28.03%
Top 5
-
0.00%
0.00%
89,379,631
89,379,631
51.63%
Top 10
-
0.00%
0.00%
118,859,102
118,859,102
68.66%
Top 25
5,217,000
43.96%
35.17%
157,922,048
157,922,048
91.23%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by Shareholders upon Listing.

<<<PAGE 17>>>
17
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
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
allotted of the
total number
of H Shares
applied
for
200
83,904
122 out of 83,904 to receive 200 Shares
0.15%
400
10,268
30 out of 10,268 to receive 200 Shares
0.15%
600
5,331
24 out of 5,331 to receive 200 Shares
0.15%
800
19,656
115 out of 19,656 to receive 200 Shares
0.15%
1,000
4,537
33 out of 4,537 to receive 200 Shares
0.15%
1,200
1,346
12 out of 1,346 to receive 200 Shares
0.15%
1,400
1,115
12 out of 1,115 to receive 200 Shares
0.15%
1,600
3,912
46 out of 3,912 to receive 200 Shares
0.15%
1,800
1,189
16 out of 1,189 to receive 200 Shares
0.15%
2,000
8,691
127 out of 8,691 to receive 200 Shares
0.15%
3,000
2,861
63 out of 2,861 to receive 200 Shares
0.15%
4,000
2,524
74 out of 2,524 to receive 200 Shares
0.15%
5,000
1,909
70 out of 1,909 to receive 200 Shares
0.15%
6,000
1,589
70 out of 1,589 to receive 200 Shares
0.15%
7,000
1,176
60 out of 1,176 to receive 200 Shares
0.15%
8,000
1,398
82 out of 1,398 to receive 200 Shares
0.15%
9,000
1,053
69 out of 1,053 to receive 200 Shares
0.15%
10,000
3,949
287 out of 3,949 to receive 200 Shares
0.15%
15,000
2,842
310 out of 2,842 to receive 200 Shares
0.15%
20,000
3,285
477 out of 3,285 to receive 200 Shares
0.15%
25,000
1,564
284 out of 1,564 to receive 200 Shares
0.15%
30,000
1,687
367 out of 1,687 to receive 200 Shares
0.15%
35,000
1,284
326 out of 1,284 to receive 200 Shares
0.15%
40,000
1,434
416 out of 1,434 to receive 200 Shares
0.15%
45,000
858
280 out of 858 to receive 200 Shares
0.15%
50,000
1,646
597 out of 1,646 to receive 200 Shares
0.15%
60,000
1,454
633 out of 1,454 to receive 200 Shares
0.15%
70,000
1,171
595 out of 1,171 to receive 200 Shares
0.15%
80,000
3,135
1,821 out of 3,135 to receive 200 Shares
0.15%
Total
176,768
Total number of Pool A successful applicants: 7,418

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
allotted of the 
total number
of H Shares
applied
for
90,000
5,316
1,041 out of 5,316 to receive 200 Shares
0.04%
100,000
2,171
473 out of 2,171 to receive 200 Shares
0.04%
120,000
1,232
322 out of 1,232 to receive 200 Shares
0.04%
140,000
1,049
320 out of 1,049 to receive 200 Shares
0.04%
160,000
920
321 out of 920 to receive 200 Shares
0.04%
180,000
656
257 out of 656 to receive 200 Shares
0.04%
200,000
1,357
591 out of 1,357 to receive 200 Shares
0.04%
250,000
1,002
546 out of 1,002 to receive 200 Shares
0.04%
300,000
1,102
720 out of 1,102 to receive 200 Shares
0.04%
370,800
3,499
2,826 out of 3,499 to receive 200 Shares
0.04%
Total
18,304
Total number of Pool B successful applicants: 7,417
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 19>>>
19
ADDITIONAL INFORMATION
Reallocation
As the Hong Kong Public Offering has been over-subscribed by more than 50 times of the total 
number of Offer Shares initially available under the Hong Kong Public Offering, the reallocation 
procedure as disclosed in the section headed “Structure of the Global Offering – The Hong Kong 
Public Offering – Reallocation and Clawback” in the Prospectus has been applied.
The number of Offer Shares initially available under the Hong Kong Public Offering is 741,800 
Shares, representing approximately 5% of the total number of Offer Shares initially available under 
the Global Offering. As a result of such reallocation, the final number of Offer Shares under the 
Hong Kong Public Offering is adjusted to 2,967,000 Shares, representing approximately 20% of 
the total number of Offer Shares available under the Global Offering.
Placing to connected clients with consents under paragraph 1C(1) of the Placing Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of certain 
distributors pursuant to the Placing Guidelines. Details of the placement to connected clients are 
set out below.
No.
Connected Clients
Connected Distributor
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
independent third 
parties
Investment 
amount (HK$)
Number of 
H Shares to be 
allocated
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering
assuming no
exercise of 
Over-
allotment
Option
Approximate 
percentage of 
the total issued 
share capital 
immediately 
following 
completion 
of the Global 
Offering 
assuming no
exercise of 
Over-
allotment
Option
1.
ABCI Asset 
Management Limited 
(“ABCI AM”)
ABCI Capital Limited 
(“ABCI Capital”) 
and ABCI Securities 
Company Limited (“ABCI 
Securities”)
See Note 1
discretionary
1,602,480
26,400
0.178%
0.015%
2.
China Galaxy 
International 
Investment Co., Ltd 
(“CGII”)
China Galaxy International 
Securities (Hong Kong) 
Co., Limited (“CGIS”)
See Note 2
non-discretionary
194,240
3,200
0.022%
0.002%
3.
CICC Financial 
Trading Limited 
(“CICC FT”)
China International 
Capital Corporation Hong 
Kong Securities Limited 
(“CICC”)
See Note 3
non-discretionary
339,920
5,600
0.038%
0.003%

<<<PAGE 20>>>
20
Notes:
(1) 
ABCI AM intends to hold the Offer Shares in its capacity as manager managing investment portfolios on behalf 
of underlying investors (the “ABCI AM Ultimate Clients”) who are independent third parties on a discretionary 
basis. To the best knowledge of ABCI AM, each of the ABCI AM Ultimate Clients is an independent third party 
of the Company, its subsidiaries, its substantial shareholders, ABCI Capital, ABCI Securities and the companies 
which are members of the same group of companies as ABCI Capital and ABCI Securities, and ABCI AM is 
therefore a “connected client” of ABCI Capital and ABCI Securities. ABCI AM also confirms that it will not 
hold any Offer Shares placed to it on a proprietary basis for itself or for any group member of ABCI, and will 
be held by it on behalf of independent third parties.
(2) 
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
exercise the voting right of the Offer Shares during the tenor of the back-to-back TRS. During the life of the 
CGII TRS and back-to-back TRS, CGII may continue to hold the Offer Shares in its custodian account, or to 
hold some or all of the Offer Shares in a prime brokerage account for stock borrowing purposes.
As permitted under the contractual arrangement with the CGII Ultimate Client, CGII will lend out its holding 
of underlying Offer Shares in the form of stock borrowing loans consistent with market practice to lower its 
finance costs, provided that CGII has the ability to call back the Offer Shares on loan at any time in order to 
satisfy its obligations under the back-to-back TRS to ensure the economic interests to be passed to the CGII 
Ultimate Client under the CGII TRS will remain unchanged.
To the best of CGII’s knowledge after having made all reasonable inquiries, the CGII Ultimate Client is an 
independent third party of CGII, and the companies which are members of the same group of CGIS. Both CGII 
and CGIS are indirect wholly-owned subsidiaries of CGS, the A shares of which are listed on the Shanghai 
Stock Exchange (stock code: 601881), the H shares of which are listed on the Stock Exchange (stock code: 
6881). CGII is a connected client (as defined under Appendix F1 to the Listing Rules) of CGIS, holding 
securities on a non-discretionary basis on behalf of independent third parties.
The CGII Ultimate Client is Yuanfeng Vision Growth Private Equity Securities Investment Fund (源峰遠景成長
私募證券投資基金) (“Yuanfeng Vision Fund”), a registered private investment scheme in mainland China (No. 
SB2719), managed by CPE Asset Management Partnership (Limited Partnership) (北京源峰私募基金管理合夥
企業(有限合夥)) (“CPE Asset Management”). No single ultimate beneficial owner holds 30% or more interest 
in Yuanfeng Vision Fund.

<<<PAGE 21>>>
21
(3) 
CICC FT and China International Capital Corporation Limited will enter into a series of cross border delta-one 
OTC swap transactions (the “OTC Swaps”) with each other and the ultimate clients (the “CICC FT Ultimate 
Clients”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary to hedge the OTC 
Swaps while the economic risks and returns of the underlying Offer Shares are passed to the CICC FT Ultimate 
Clients, subject to customary fees and commissions. The OTC Swaps will be fully funded by the CICC FT 
Ultimate Clients. During the terms of the OTC Swaps, all economic returns of the Offer Shares subscribed by 
CICC FT will be passed to the CICC FT Ultimate Clients and all economic loss shall be borne by the CICC FT 
Ultimate Clients through the OTC Swaps, and CICC FT will not take part in any economic return or bear any 
economic loss in relation to the Offer Shares. The OTC Swaps are linked to the Offer Shares and the CICC FT 
Ultimate Clients may request CICC FT to redeem it at their own discretion, upon which CICC FT shall dispose 
of the Offer Shares and settle OTC Swaps in cash in accordance with the terms and conditions of the OTC 
Swap. Despite that CICC FT will hold the legal title of the Offer Shares by itself, it will not exercise the voting 
rights attaching to the relevant Offer Shares during the terms of the OTC Swaps according to its internal policy. 
CICC FT is a connected client (as defined under Appendix F1 to the Listing Rules) of CICC, holding securities 
on a non-discretionary basis on behalf of independent third parties.
To the best knowledge, information and belief of CICC FT after due enquiry, the CICC FT Ultimate Clients 
for purpose of this placee subscription include: (1) Little Croc No. 3 Private Securities Investment Fund (小鱷 
3 號私募證券投資基金) (“Little Croc No. 3”), which is managed by Shanghai Little Croc Asset Management 
Co., Ltd. (上海小鱷資產管理有限公司), a company controlled by Huang Hui (黃慧). Huang Hui holds 100% 
interests in Little Croc No. 3 and (ii) Yuanlesheng Qiangye Private Equity Securities Investment Fund (源樂晟
強業私募證券投資基金),which is managed by Tibet Longrising Asset Management Co., Ltd.(西藏源樂晟資產
管理有限公司) and ultimate beneficial owners holding 30% or more interest are Zeng Xiaojie and Hu Caiyang.

<<<PAGE 22>>>
22
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and trading fee payable.
The Directors and the Overall Coordinators confirm that at least 50% of the total number of 
the Offer Shares have been allocated to and taken up by independent price setting investors in 
compliance with Rule 18C.08 of the Listing Rules.
The Directors further confirm that at least 20% of the issued share capital of the Company will be 
held by sophisticated independent investors at the time of Listing in compliance with Chapter 2.5 
of the Guide for New Listing Applicants.

<<<PAGE 23>>>
23
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
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated June 17, 2026 issued by Beijing Zhongke 
WengeAI Science and Technology Co., Ltd.* (北京中科聞歌科技股份有限公司) for detailed 
information about the Global Offering described herein before deciding whether or not to invest 
in the Shares thereby being offered.
* 
Potential investors of the Offer Shares should note that the Sole Sponsor and the Sponsor-Overall Coordinator 
(for itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under 
the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events 
set out in the paragraph headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong 
Public Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong 
time) on the Listing Date (which is currently expected to be on Friday, June 26, 2026).

<<<PAGE 24>>>
24
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, the total number of the H Shares 
held by the public represents approximately 71.97% of the total issued share capital of the 
Company, which is higher than the prescribed percentage of H Shares required to be held in public 
hands of 15.00% under Rule 8.08(1) (as amended and replaced by Rule 19A.13A(1)) of the Listing 
Rules calculated based on the final Offer Price of HK$60.70 per H Share, thereby satisfying the 
public float requirement under Rule 8.08(1) (as amended and replaced by Rule 19A.13A(1)) of the 
Listing Rules.
In consideration that the total number of H Shares in issue upon Listing that are held by the 
public and not subject to any disposal restrictions is expected to have a market value at the time 
of the Listing of not less than HK$600,000,000, the Company is expected to satisfy the free float 
requirement under Rule 19A.13C of the Listing Rules at the time of the Listing.
The Directors confirm that, immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public shareholders of 
the Company do not hold more than 50% of the shares in public hands at the time of the Listing 
in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 
Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. (Hong Kong time) on 
Friday, June 26, 2026, provided that the Global Offering has become unconditional and the right 
of termination described in the section headed “Underwriting — Underwriting Arrangements and 
Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus has not 
been exercised. Investors who trade H Shares prior to the receipt of H Share certificates or the H 
Share certificates becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong Kong 
time) on Friday, June 26, 2026, it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Friday, June 26, 2026. The H Shares will be traded in board lots of 
200 H Shares each. The stock code of the Shares is 1956.
By order of the Board
Beijing Zhongke WengeAI Science and 
Technology Co., Ltd.
Dr. Wang Lei
Executive Director and Chairman of the Board
Hong Kong, June 25, 2026
As at the date of this announcement, the Board comprises (i) Dr. Wang Lei, Dr. Luo Yin, Mr. Qu 
Baoyu, Mr. Cao Jia and Ms. Zhang Xina as executive Directors; (ii) Mr. Zhou Jun as non-executive 
Director; and (iii) Mr. Xu Huansheng, Ms. Gu Fenling and Ms. Jiang Xianling as independent 
non-executive Directors.
