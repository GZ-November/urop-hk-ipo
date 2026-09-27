# 配发结果公告抽取任务：9611.HK Shanghai Longcheer Technology Co., Ltd.- H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**21/01/2026 22:27**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0121/2026012101145.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"9611.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) 
and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for any securities 
in the United States or in any other jurisdictions. The Offer Shares have not been, and will not be, registered under 
the United States Securities Act of 1933 as amended (the “U.S. Securities Act”) or securities law of any state or other 
jurisdiction of the United States. The Offer Shares may not be offered, sold, pledged, or otherwise transferred within 
the United States, except pursuant to an available exemption from, or in a transaction not subject to, the registration 
requirements of the U.S. Securities Act. There will be no public offer of the Offer Shares in the United States. The 
Offer Shares are being offered and sold solely (1) to qualified institutional buyers as defined in Rule 144A under the 
U.S. Securities Act pursuant to Rule 144A or another available exemption from registration under the U.S. Securities 
Act and (2) outside the United States in offshore transactions in reliance on Regulation S under the U.S. Securities 
Act.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
Wednesday, January 14, 2026 (the “Prospectus”) issued by SHANGHAI LONGCHEER TECHNOLOGY CO., LTD. 
(上海龍旗科技股份有限公司) (the “Company”) for detailed information about the Global Offering described below 
before deciding whether or not to invest in the H Shares thereby being offered. Any investment decision in relation to 
the Offer Shares should be taken solely in reliance on the information in the Prospectus.
Unless otherwise defined in this announcement, capitalised terms used herein shall have the same meanings as those 
defined in the Prospectus.
In connection with the Global Offering, Citigroup Global Markets Asia Limited, as stabilizing manager (the 
“Stabilizing Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, the extent 
permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect 
transactions with a view to stabilizing or supporting the market price of the H Shares at such price, in such amounts 
and in such manners as the Stabilizing Manager, its affiliates or any person acting for it may determine and at a 
level higher than that which might otherwise prevail for a limited period after the Listing Date. However, there is 
no obligation on the Stabilizing Manager (or its affiliates or any person acting for it) to conduct any such stabilizing 
action. Such stabilisation action, if taken, (a) will be conducted at the absolute discretion of the Stabilizing Manager 
(or its affiliates or any person acting for it) and in what the Stabilizing Manager reasonably regards as the best interest 
of our Company, (b) may be discontinued at any time and (c) is required to be brought to an end within 30 days of 
the last day for lodging applications under the Hong Kong Public Offering (which is Wednesday, February 18, 2026). 
Such stabilizing action, if taken, may be effected in all jurisdictions where it is permissible to do so, in each case in 
compliance with all applicable laws, rules and regulatory requirements, including the Securities and Futures (Price 
Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures 
Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilising action can be taken to support the price of the H Shares for 
longer than the stabilisation period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Wednesday, February 18, 
2026). After this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the 
price of the H Shares, could fall.
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on behalf of 
the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed Underwriting 
– Hong Kong Underwriting Arrangements – Hong Kong Public Offering –Grounds for Termination” in the Prospectus 
at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Thursday, 
January 22, 2026).

<<<PAGE 2>>>
2
SHANGHAI LONGCHEER TECHNOLOGY CO., LTD.
上海龍旗科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
52,259,100 H Shares (subject to the 
 Over-allotment Option)
Number of Hong Kong Offer Shares
:
5,226,000 H Shares
Number of International Offer Shares
:
47,033,100 H Shares (including 3,339,500 
 Employee Reserved Shares allocated 
 under the Employee Preferential 
 Offering, subject to the Over-allotment 
 Option)
Final Offer Price
:
HK$31.00 per H Share, plus brokerage of 
 1.0%, SFC transaction levy of 0.0027%, 
 Hong Kong Stock Exchange trading fee of 
 0.00565% and AFRC transaction levy 
 of 0.00015%
Nominal value
:
RMB1.00 per H Share
Stock code
:
9611
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Overall Coordinator, Joint Global Coordinator, 
Joint Bookrunner and Joint Lead Manager
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
SHANGHAI LONGCHEER TECHNOLOGY CO., LTD.
上海龍旗科技股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
9611
Stock short name
LONGCHEER
Dealings commencement date
January 22, 2026*
* see note at the end of the announcement
Price Information
Final Offer Price
HK$31.00
Maximum Offer Price
HK$31.00
Offer Shares and Share Capital
Number of Offer Shares
52,259,100
Number of Offer Shares in Hong Kong Public Offering
5,226,000
Number of Offer Shares in International Offering  
(excluding Reserved Shares under the Preferential Offering)
41,808,100
Number of Employee Reserved Shares in Employee 
Preferential Offering
No more than 5,225,000
Number of issued Shares upon Listing (before exercise of the 
Over-allotment Option)
522,590,644
Over-allocation
No. of Offer Shares over-allocated
7,838,800
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.

<<<PAGE 4>>>
4
Proceeds
Gross proceeds (Note)
HK$1,620.0 million
 Less: Estimated listing expenses payable based on 
 Final Offer Price
HK$100.1 million
Net proceeds
HK$1,519.9 million
Note: Gross proceeds refer to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
The Company will adjust the allocation of the net proceeds from the exercise of the Over-
allotment Option (if any) for the purposes as set out in the section headed “Future Plans and Use 
of Proceeds” of the Prospectus on a pro rata basis. During the Track Record Period, the listing 
expenses of RMB0.8 million has been charged to the consolidated statements of profit or loss of 
the Company, therefore the actual net proceeds received by the Company will be HK$1,520.7 
million.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
Number of valid applications
145,096
Number of successful applications
29,665
Subscription level
1,149.76 times
Reallocation
No
Number of Offer Shares initially available under the 
Hong Kong Public Offering
5,226,000
Number of Offer Shares reallocated from the International Offering
0
Final number of Offer Shares under the Hong Kong Public Offering
5,226,000
% of Offer Shares under the Hong Kong Public Offering 
to the Global Offering
10.00%
Note: For details of the final allocation of the Offer Shares to the Hong Kong Public Offering, investors can refer to 
www.eipo.com.hk/eIPOAllotment to perform a search by identification number or www.eipo.com.hk/eIPOAllotment 
for the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
Number of placees
172
Subscription Level (excluding Employee Reserved Shares under the 
Employee Preferential Offering)
9.02 times
Number of Offer Shares initially available under the International 
Offering (excluding Employee Reserved Shares under the Employee 
Preferential Offering)
41,808,100
Final number of Offer Shares under the International Offering 
(excluding final number of Employee Reserved Shares allocated under 
the Employee Preferential Offering) (before exercise of the Over-
allotment Option)
43,693,600
% of Offer Shares under the International Offering to 
the Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a 
waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit the Company to allocate certain Offer Shares in the International Offering 
to certain Existing Minority Shareholders and/or their close associates; and (b) a consent under 
paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company 
to, among other things, allocate further H Shares in the International Offering to the Cornerstone 
Investors and/or their close associates, (i) none of the Offer Shares subscribed by the placees 
and the public have been financed directly or indirectly by the Company, any of the Directors, 
chief executive of the Company, Controlling Shareholders, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates; and 
(ii) none of the placees and the public who have purchased the Offer Shares are accustomed to 
taking instructions from the Company, any of the Directors, chief executive of the Company, 
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company or any 
of its subsidiaries or their respective close associates in relation to the acquisition, disposal, voting 
or other disposition of H Shares registered in his/her/its name or otherwise held by him/her/it.

<<<PAGE 6>>>
6
Employee Preferential Offering
Number of valid applications 
222
Subscription Level 
0.64 times
Number of Employee Reserved Shares initially available under the 
Employee Preferential Offering
No more than 
5,225,000 
International 
Offer Shares
Final number of Employee Reserved Shares under the Employee 
Preferential Offering
3,339,500
Under-subscription of shares and made available to the International 
Offer
1,885,500
Under-subscription of shares and made available to the Public Offer
–
For details of the Employee Preferential Offering, please refer to the section headed “Structure of 
the Global Offering – Employee Preferential Offering” of the Prospectus and the section headed 
“Others/Additional Information – Allocations under the Employee Preferential Offering” in this 
announcement.

<<<PAGE 7>>>
7
The placees in the International Offering include the following: 
Cornerstone Investors
Investor
No. of Offer 
Shares Allocated(1)
% of total issued 
H Shares after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised)
% of total issued 
share capital in the 
Company after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised)
Existing 
shareholders 
or their close 
associates
Qualcomm Ventures LLC 
 (“Qualcomm”)
2,010,600
3.85%
0.38%
No
Jiangxi Guokong Private Equity 
 Fund Management Co., Ltd. 
 (江西國控私募基金管理有限公司)
 (“Jiangxi Guokong”)
3,896,700
7.46%
0.75%
No
WILL semiconductor Limited 
 (“OmniVision HK”)
2,513,200
4.81%
0.48%
No
Hong Kong Yuto Printing Company 
 Limited (“Hong Kong Yuto”)
2,513,200
4.81%
0.48%
No
Qingdao Guanlan and Guotai 
 Junan Investments (Hong Kong) 
 Limited (in connection with 
 Guanlan OTC Swaps)
2,010,600
3.85%
0.38%
No
Endless Growth NH Limited 
 (“Endless Growth”)
1,256,600
2.40%
0.24%
Yes
* For identification purposes only
Notes:
1. 
Excluding Offer Shares allotted to Cornerstone Investors and/or their close associates with consent under 
Chapter 4.15 of the Guide for New Listing Applicants (if any).
2. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering (assuming the Over-allotment Option is not exercised).
3. 
In addition to the Offer Shares subscribed for as Cornerstone Investors, Qingdao Guanlan and Guotai Junan 
Investments (Hong Kong) Limited (in connection with Guanlan OTC Swaps) and/or their close associates, 
where applicable, were allocated further Offer Shares as placees in the International Offering. Please refer 
to the section headed “Allotment Results Details – International Offering – Allotees with Waivers/Consents 
Obtained” in this announcement for details. Only the Offer Shares subscribed for as Cornerstone Investors are 
subject to lock-up as indicated below. For details, please refer to the section headed “Lock-up Undertakings – 
Cornerstone Investors” in this announcement.

<<<PAGE 8>>>
8
Allotees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares Allocated
% of total issued 
H Shares after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 4
% of total issued 
share capital in 
the Company 
after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 5
Relationship
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 
1C(2) of the Placing Guidelines in relation to subscription for H Shares by Existing Minority Shareholders and/
or their close associates holding more than 1% of the issued share capital of the Company immediately prior to the 
completion of the Global Offering Note 1
Endless Growth
1,256,600
2.40%
0.24%
The shareholders of 
Endless Growth are 
an existing minority 
Shareholder of our 
Company (holding less 
than 5% of our total 
issued Shares).
GTHT Onshore Ultimate 
Client under the 
Employee Preferential 
Offering
3,339,500
6.39%
0.64%
The ultimate client is a 
service trust subscribed 
by the Eligible 
Employees as ultimate 
beneficiaries pursuant 
to the Employee 
Preferential Offering.
Yuanxin Investments(1)
351,800
0.67%
0.07%
Close associates of existing 
shareholders of the 
Company 
Footnote:
(1) 
Yuanxin Investments consists of Yuanxin China Value Growth and Yuanxin Fund No.2 (as defined below). Each of Yuanxin Fund No.2 and 
Yuanxin China Value Growth is managed by the same fund manager, i.e. 遠信(珠海)私募基金管理有限公司, which is held by an ultimate 
beneficial owner named 劉岩 as to 42.49%, and therefore a close associate of 13 existing A-Share shareholders of the Company (each 
individually holding less than 0.2% of the total issued Shares as of the date of this announcement).

<<<PAGE 9>>>
9
Investor
No. of Offer 
Shares Allocated
% of total issued 
H Shares after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 4
% of total issued 
share capital in 
the Company 
after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 5
Relationship
Allotees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocations of further H Shares to Cornerstone Investors and/or their close associates Note 2
Qingdao Guanlan 
1,093,900
2.09%
0.21%
Same fund manager entity 
as set out in the Qingdao 
Guanlan and Guotai 
Junan Investments 
(Hong Kong) Limited 
(in connection with 
Guanlan OTC Swaps) 
in the section headed 
“Cornerstone Investors” 
of the Prospectus.
Guanlan Investment’s 
Linze Convertible Bond 
No. 1 Private Equity 
Investment Fund (觀
瀾投資霖澤轉債1號
私募證券投資基金) 
(“Guanlan Linze”)(2)
Close associate of Qingdao 
Guanlan
Gemming Capital 
Limited(3)
158,000
0.30%
0.03%
Close associate of Qingdao 
Guanlan
Footnote:
(2) 
Guanlan Linze is managed by Qingdao Guanlan.
(3) 
Gemming Capital Limited is ultimately controlled by Mr. Zhang Yanfeng, who is the actual controller of Qingdao Guanlan (as set out in 
the section headed “Cornerstone Investors” of the Prospectus).

<<<PAGE 10>>>
10
Investor
No. of Offer 
Shares Allocated
% of total issued 
H Shares after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 4
% of total issued 
share capital in 
the Company 
after the 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) Note 5
Relationship
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients Note 3
Guotai Junan Investments 
(Hong Kong) 
Limited (“GTJA 
Investments”)(4)
1,093,900
2.09%
0.21%
Connected Client as a 
placee
Fullgoal Fund 
Management Co., Ltd. 
(“Fullgoal Fund”)
493,300
0.94%
0.09%
Connected Client as a 
placee
Fullgoal Asset 
Management (HK) 
Limited (“Fullgoal 
HK”)
59,800
0.11%
0.01%
Connected Client as a 
placee
Huatai Capital 
Investment Limited 
(“HTCI”)
2,704,200
5.17%
0.52%
Connected Client as a 
placee
ABCI Asset Management 
Limited (“ABCI AM”)
25,100
0.05%
0.005%
Connected Client as a 
placee
GF Global Capital 
Limited (“GFGC”)
351,800
0.67%
0.07%
Connected Client
as a placee
E Fund Management 
Co., Ltd (“E Fund 
Management”)
514,400
0.98%
0.10%
Connected Client as a 
placee
E Fund Management 
(Hong Kong) Co., 
Limited (“E Fund 
HK”)
38,700
0.07%
0.01%
Connected Client as a 
placee
China Galaxy 
International 
Investment Company 
Limited (“CGII”)
578,100
1.11%
0.11%
Connected Client as a 
placee
(4) 
The number of Offer Shares allocated to GTJA Investments listed in this subsection only represents the number of Offer Shares allocated 
to GTJA Investments as a placee (excluding the final number of Shares allocated to Eligible Employees under the Employee Preferential 
Offering and Shares allocated to Qingdao Guanlan and Guotai Junan Investments (Hong Kong) Limited (in connection with Guanlan 
OTC Swaps) under the cornerstone investment.)

<<<PAGE 11>>>
11
Investor
No. of Offer 
Shares allocated
% of total issued 
H Shares after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised) Note 4
% of total issued 
share capital in the 
Company after the 
Global Offering 
(assuming the Over-
allotment Option is 
not exercised) Note 5
Relationship
Notes:
1. 
The Stock Exchange has granted a waiver from strict compliance with the requirements under Rule 10.04 
of the Listing Rules and consent under Paragraph 1C(2) of the Placing Guidelines to permit H Shares in the 
International Offering to be placed to certain Existing Minority Shareholders and/or their close associates. 
Please refer to the section headed “waivers and exemptions - waiver in respect of allocation of H shares to 
existing minority shareholders and their close associates” of the Prospectus for details.
To the best knowledge, information and belief of the Company after due enquiry, details of the allocations to 
the Existing Minority Shareholder and their close associates holding more than 1% of the issued share capital 
of the Company immediately prior to the completion of the Global Offering have been disclosed in this 
announcement.
2. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details – International Offering – Cornerstone Investors” in this announcement. For details of 
the consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocations of further H Shares to the Cornerstone Investors and/or their close associates, please refer to the 
section headed “Others/Additional Information – Allocations of Offer Shares to the Cornerstone Investors 
and their Close Associates with a Consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing 
Applicants” in this announcement.
3. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients, please refer to the section headed 
“Others/Additional Information – Placing to Connected Clients with a Consent under Paragraph 1C(1) of the 
Placing Guidelines” in this announcement.
4. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering (assuming the Over-allotment Option is not exercised).
5. 
Not taking into account any A Shares held by the relevant investors. The figures are based on assumption that 
the Over-allotment Option is not exercised.

<<<PAGE 12>>>
12
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
shares held 
in the Company 
subject to lock-up 
undertakings 
upon listing
% of total issued 
H shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
listing (assuming 
the Over-allotment
Option is not 
exercised)
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
listing (assuming 
the Over-allotment 
Option is not 
exercised)
Last day subject to the 
lock-up undertakings
Mr. Du Note 3,4,5
179,054,013
–
34.26%
July 21, 2026 (First Six-
Month Period) Note 1 
January 21, 2027 (Second 
Six-Month Period) Note 2
Mr. Ge Note 3,5,6
179,054,013
–
34.26%
July 21, 2026 (First Six-
Month Period) Note 1 
January 21, 2027 (Second 
Six-Month Period) Note 2
 Shanghai Xinhe Note 3
95,793,544
–
18.33%
July 21, 2026 (First Six-
Month Period) Note 1 
January 21, 2027 (Second 
Six-Month Period) Note 2
Kunshan Longcheer Note 3
95,793,544
–
18.33%
July 21, 2026 (First Six-
Month Period) Note 1 
January 21, 2027 (Second 
Six-Month Period) Note 2
Chengmai Qihe Note 4
45,845,019
–
8.77%
July 21, 2026 (First Six-
Month Period) Note 1 
January 21, 2027 (Second 
Six-Month Period) Note 2
Kunshan Qiyun Note 6
15,971,815
–
3.06%
July 21, 2026 (First Six-
Month Period) Note 1  
January 21, 2027 (Second 
Six-Month Period) Note 2

<<<PAGE 13>>>
13
Notes:
1. 
The Controlling Shareholders may dispose of or transfer Shares after the indicated date subject to that the Controlling Shareholders will not cease to be a 
Controlling Shareholder.
2. 
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after the indicated date.
3. 
As of the date of this announcement, Kunshan Longcheer is managed by its general partner, Shanghai Xinhe, which in turn is controlled by Mr. Du as to 
51.00% and Mr. Ge as to 49.00%. Save for Mr. Du who also holds 52.95% of the partnership interest in Kunshan Longcheer, none of the limited partners 
holds over one third of the partnership interest in Kunshan Longcheer. Therefore, each of Mr. Du, Mr. Ge and Shanghai Xinhe is deemed to be interested in 
the 95,793,544 Shares held by Kunshan Longcheer under the SFO.
4. 
As of the date of this announcement, Mr. Du is the general partner of Chengmai Qihe. Therefore, Mr. Du is deemed to be interested in the 45,845,019 
Shares held by Chengmai Qihe under the SFO.
5. 
As of the date of this announcement, pursuant to a concert party agreement dated November 1, 2021, Mr. Du and Mr. Ge agreed to act in concert by aligning 
the voting rights controlled by them at the Shareholders’ meetings of the Company. Therefore, they are deemed to be jointly interested in the aggregate 
number of Shares held by each other under the SFO.
6. 
As of the date of this announcement, Mr. Ge was the executive general partner of Kunshan Qiyun. Save for Mr. Ge, none of the other partners holds over 
one third of the partnership interest in Kunshan Qiyun. Therefore, Mr. Ge is also deemed to be interested in the 15,971,815 Shares held by Kunshan Qiyun 
under the SFO.

<<<PAGE 14>>>
14
Cornerstone Investors
Name
Number of 
H Shares held 
in the Company 
subject to lock-up 
undertakings
 upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over- allotment 
Option is not 
exercised) Note 1
% of total issued 
share capital in 
the Company 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over- allotment 
Option is not 
exercised)
Last day subject to the 
lock-up undertakings Note 2
Qualcomm
2,010,600
3.85%
0.38%
July 21, 2026
Jiangxi Guokong
3,896,700
7.46%
0.75%
July 21, 2026
OmniVision HK
2,513,200
4.81%
0.48%
July 21, 2026
Hong Kong Yuto
2,513,200
4.81%
0.48%
July 21, 2026
Qingdao Guanlan and 
 Guotai Junan Investments 
 (Hong Kong) Limited 
 (in connection with 
 Guanlan OTC Swaps)
2,010,600
3.85%
0.38%
July 21, 2026
Endless Growth
1,256,600
2.40%
0.24%
July 21, 2026
Total
14,200,900
27.18%
2.71%
Notes:
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
2. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on July 21, 
2026. The Cornerstone Investors will cease to be prohibited from disposing of or transferring H Shares 
subscribed pursuant to the relevant cornerstone investment agreements after the indicated date.

<<<PAGE 15>>>
15
H SHAREHOLDER CONCENTRATION ANALYSIS
H 
Shareholders
(1)
Number of 
H Shares 
allotted
Allotment as % 
of International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as % 
of International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
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
exercised and 
new H Shares 
are issued)
Number of 
H Shares 
held upon 
Listing
% of total 
issued H 
share capital 
upon Listing 
(assuming no 
exercise of the 
Overallotment 
Option)
% of total 
issued H 
share capital 
upon Listing 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised and 
new H Shares 
are issued)
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
exercised and 
new H Shares 
are issued)
Top 1
3,896,700
8.29%
7.10%
7.46%
6.48%
3,896,700
7.46%
6.48%
0.75%
0.73%
Top 5
15,745,400
33.48%
28.69%
30.13%
26.20%
15,745,400
30.13%
26.20%
3.01%
2.97%
Top 10
27,822,400
59.15%
50.70%
53.24%
46.30%
27,822,400
53.24%
46.30%
5.32%
5.25%
Top 25
43,210,900
91.87%
78.75%
82.69%
71.90%
43,210,900
82.69%
71.90%
8.27%
8.15%
Note:
1. 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 16>>>
16
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
(1)
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
exercised and 
new H Shares 
are issued)
Allotment 
as % of 
total Offer 
Shares 
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
exercised and 
new H Shares 
are issued)
Number of 
H Shares 
held upon 
Listing
Number of 
Shares held 
upon Listing
% of total issued 
share capital upon 
Listing (assuming 
no exercise of the 
Over-allotment 
Option)
% of total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares are 
issued)
Top 1
0
0.00%
0.00%
0.00%
0.00%
0
95,793,544
18.33%
18.06%
Top 5
0
0.00%
0.00%
0.00%
0.00%
0
202,275,406
38.71%
38.13%
Top 10
0
0.00%
0.00%
0.00%
0.00%
0
253,915,596
48.59%
47.87%
Top 25
20,785,400
44.19%
37.88%
39.77%
34.59%
20,785,400
315,691,663
60.41%
59.52%
Notes:
1. 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon 
Listing.
2. 
To the best knowledge, information and belief of the Company after due enquiry, details of the allocations 
to the Existing Minority Shareholder and/or their close associates holding more than 1% of the issued share 
capital of the Company immediately prior to the completion of the Global Offering have been disclosed in this 
announcement. Please refer to the section headed “Allotees with Waivers/Consents Obtained – Allotees with 
waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the 
Placing Guidelines in relation to subscription for H Shares by Existing Minority Shareholder and/or their close 
associates holding more than 1% of the issued share capital of the Company immediately prior to the completion 
of the Global Offering”.

<<<PAGE 17>>>
17
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
NO. OF 
SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT 
APPROXIMATE 
PERCENTAGE 
ALLOTTED 
OF THE 
TOTAL NO. OF 
SHARES 
APPLIED FOR
POOL A
100
28,372
58 out of 28,372 to receive 100 Shares
0.20%
200
8,452
34 out of 8,452 to receive 100 Shares
0.20%
300
16,441
100 out of 16,441 to receive 100 Shares
0.20%
400
3,649
29 out of 3,649 to receive 100 Shares
0.20%
500
4,847
49 out of 4,847 to receive 100 Shares
0.20%
600
2,821
34 out of 2,821 to receive 100 Shares
0.20%
700
3,463
49 out of 3,463 to receive 100 Shares
0.20%
800
1,935
31 out of 1,935 to receive 100 Shares
0.20%
900
1,615
29 out of 1,615 to receive 100 Shares
0.20%
1,000
15,942
323 out of 15,942 to receive 100 Shares
0.20%
2,000
5,893
239 out of 5,893 to receive 100 Shares
0.20%
3,000
4,800
292 out of 4,800 to receive 100 Shares
0.20%
4,000
2,815
228 out of 2,815 to receive 100 Shares
0.20%
5,000
2,645
268 out of 2,645 to receive 100 Shares
0.20%
6,000
1,763
214 out of 1,763 to receive 100 Shares
0.20%
7,000
1,311
186 out of 1,311 to receive 100 Shares
0.20%
8,000
1,223
198 out of 1,223 to receive 100 Shares
0.20%
9,000
996
182 out of 996 to receive 100 Shares
0.20%
10,000
6,779
1,373 out of 6,779 to receive 100 Shares
0.20%
20,000
3,759
1,523 out of 3,759 to receive 100 Shares
0.20%
30,000
2,628
1,597 out of 2,628 to receive 100 Shares
0.20%
40,000
1,679
1,361 out of 1,679 to receive 100 Shares
0.20%
50,000
1,467
100 Shares plus 19 out of 1,467 to receive additional 100 Shares
0.20%
60,000
1,084
100 Shares plus 234 out of 1,084 to receive additional 100 Shares
0.20%
70,000
949
100 Shares plus 397 out of 949 to receive additional 100 Shares
0.20%
80,000
766
100 Shares plus 476 out of 766 to receive additional 100 Shares
0.20%
90,000
699
100 Shares plus 576 out of 699 to receive additional 100 Shares
0.20%
100,000
5,462
200 Shares plus 142 out of 5,462 to receive additional 100 Shares
0.20%
134,255
Total number of Pool A successful applicants: 18,824

<<<PAGE 18>>>
18
NO. OF 
SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT 
APPROXIMATE 
PERCENTAGE 
ALLOTTED 
OF THE 
TOTAL NO. OF 
SHARES 
APPLIED FOR
POOL B
200,000
5,575
100 Shares plus 599 out of 5,575 to receive additional 100 Shares
0.06%
300,000
1,648
100 Shares plus 1,090 out of 1,648 to receive additional 100 Shares
0.06%
400,000
929
200 Shares plus 200 out of 929 to receive additional 100 Shares
0.06%
500,000
620
200 Shares plus 477 out of 620 to receive additional 100 Shares
0.06%
600,000
431
300 Shares plus 139 out of 431 to receive additional 100 Shares
0.06%
700,000
249
300 Shares plus 218 out of 249 to receive additional 100 Shares
0.06%
800,000
233
400 Shares plus 100 out of 233 to receive additional 100 Shares
0.06%
900,000
129
400 Shares plus 127 out of 129 to receive additional 100 Shares
0.06%
1,000,000
422
500 Shares plus 227 out of 422 to receive additional 100 Shares
0.06%
1,500,000
210
800 Shares plus 64 out of 210 to receive additional 100 Shares
0.06%
2,000,000
125
1,100 Shares plus 9 out of 125 to receive additional 100 Shares
0.06%
2,613,000
270
1,400 Shares plus 126 out of 270 to receive additional 100 Shares
0.06%
10,841
Total number of Pool B successful applicants: 10,841
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
Allocations of Offer Shares to the Cornerstone Investors and their Close Associates with a 
Consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph 
18 of Chapter 4.15 of the Guide to permit Cornerstone Investors and/or their close associates to 
subscribe for further Offer Shares as placees in the International Offering on the conditions as set 
out below:
(a) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;
(b) 
each Director (including the chief executive) of the Company and the Controlling 
Shareholders confirms that no securities have been allocated to them or their respective close 
associates under the Size-based Exemption;
(c) 
the allocation to the Cornerstone Investors and/or their close associates as permitted under 
the Size-based Exemption (as defined in the Guide) will not affect the Company’s ability to 
satisfy its public float requirement under 19A.13A(2) of the Listing Rules; and
(d) 
details of the allocation to Cornerstone Investors and/or their close associates under the 
Size-based Exemption will be disclosed in the allotment results announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to Cornerstone Investors, please refer to the section 
headed “Allotment Results Details – International Offering – Allotees with Waivers/Consents 
Obtained” in this announcement.

<<<PAGE 20>>>
20
Placing to Connected Clients with a Consent under Paragraph 1C(1) of the Placing Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines. Details of the placement to connected 
clients are set out below. The Company has applied to the Stock Exchange for, and the Stock 
Exchange has granted, consents under paragraph 1C(1) of the Placing Guidelines to permit 
Connected Clients to subscribe for Offer Shares as placees in the International Offering on the 
conditions set out below:
(a) 
any Offer Shares to be allocated to each of the Connected Clients will be held on behalf of 
independent third parties;
(b) 
no preferential treatment has been, nor will be, given to each of the Connected Clients by 
virtue of its relationship with the relevant distributor, namely HTI, GTJA Securities, HTFH 
or, ABCI, GF Securities or CGIS (collectively, the “Connected Distributors”) (as the case 
may be), in any allocation of Offer Shares in the International Offering;
(c) 
each of the Connected Clients confirms that to the best of its knowledge and belief, it has not 
received and will not receive preferential treatment in the allocation of Offer Shares in the 
Global Offering by virtue of its relationship with the Connected Clients (as the case may be);
(d) 
the Company, the Joint Overall Coordinators and each of the Connected Clients has provided 
the Stock Exchange with written confirmations in accordance with Chapter 4.15 of the Guide; 
and
(e) 
details of the allocations will be disclosed in the allotment results announcement.

<<<PAGE 21>>>
21
Details of the placement to a connected client are set out below:
No.
Connected Distributors
Connected Client
Relationship with the 
Connected Distributor (s)
Basis of holding 
securities
Number 
of Offer 
Shares 
subscribed 
(excluding 
Employee 
Reserved 
Shares 
allotted 
under the 
Employee 
Preferential 
Offering (if 
any))
Percentage 
to total 
Offer 
Shares 
under 
Global 
Offering
Percentage 
to total 
issued 
Shares 
immediately 
upon the 
completion 
of Global 
Offering
1.
Haitong International Securities 
 Company Limited (“HTI”)
Fullgoal Fund Management 
 Co., Ltd. 
 (“Fullgoal Fund”)
(1)
Fullgoal Asset Management 
 (HK) Limited 
 (“Fullgoal HK”)
(1)
Fullgoal HK, a wholly owned 
subsidiary of Fullgoal Fund, 
which is owned by Guotai 
Haitong Securities Co., Ltd.  
(SEHK: 2611) (“Guotai 
Haitong”) as to 27.775%. 
HTI and GTJA Securities 
are subsidiaries of Guotai 
Haitong. Therefore, Fullgoal 
Fund is a member of the 
same group of companies as 
HTI and GTJA Securities.
Discretionary
493,300
0.94%
0.09%
2.
Guotai Junan Securities 
 (Hong Kong) Limited 
 (“GTJA Securities”)
59,800
0.11%
0.01%
Guotai Junan Investments 
 (Hong Kong) Limited 
 (“GTJA Investments”)(2)
GTJA Investments is a member 
 of the same group of HTI and 
 GTJA Securities.
Non-discretionary
1,093,900
2.09%
0.21%
3.
Huatai Financial Holdings 
 (Hong Kong) Limited 
 (“HTFH”)
Huatai Capital Investment 
 Limited (“HTCI”)
(3)
HTCI is a member of the same 
 group of HTFH
Non-discretionary
2,704,200
5.17%
0.52%
4.
ABCI Securities Company 
 Limited (“ABCI”)
ABCI Asset Management 
 Limited (“ABCI AM”)
(4)
ABCI AM is a member of the 
 same group as ABCI
Discretionary
25,100
0.05%
0.005%
5.
GF Securities (Hong Kong) 
Brokerage Limited (“GF 
Securities”)
GF Global Capital Limited 
 (“GFGC”)
(5)
GFGC is a member of the same 
 group as GF Securities
Non-discretionary
351,800
0.67%
0.07%
E Fund Management Co., Ltd 
 (“E Fund Management”)
(6)
E Fund Management is 
 a member of the same group 
 with GF Securities
Discretionary
514,400
0.98%
0.10%
E Fund Management 
 (Hong Kong) Co., Limited 
 (“E Fund HK”)
(7)
E Fund HK is a member of the 
 same group with 
 GF Securities (Hong Kong) 
 Brokerage
Discretionary
38,700
0.07%
0.01%
6.
China Galaxy International 
Securities (Hong Kong) Co., 
Limited (“CGIS”)
China Galaxy International 
 Investment Company 
 Limited (“CGII”)
(8)
CGII is a wholly owned 
 subsidiary of CGIS
Non-discretionary
578,100
1.11%
0.11%

<<<PAGE 22>>>
22
Notes:
(1) 
Each of Fullgoal Fund and Fullgoal HK will hold the Offer Shares in their capacity as the discretionary 
fund manager on behalf of their investors, each of which is an independent third party of the Company, its 
subsidiaries, its Controlling Shareholders, its substantial shareholders, Fullgoal Fund, Fullgoal HK, HTI, GTJA 
Securities and the companies which are members of the same group of HTI and GTJA Securities. No ultimate 
beneficial owner holds 30% or more interest in the underlying investors.
(2) 
GTJA Investments shall hold the Offer Shares for hedging purpose as the single underlying asset of several 
sets of back-to-back total return swap transaction (the “GTHT Back-to-back TRS”) to be entered into between 
GTJA Investments and Guotai Haitong Securities Co., Ltd. (the “GTHT Onshore Parent”) in connection with 
several total return swap orders (the “GTHT Client TRS”) to be entered into by GTHT Onshore Parent and 
several ultimate clients (the “GTHT Onshore Ultimate Clients”), respectively. Such GTHT Client TRS is 
to be fully funded by the GTHT Onshore Ultimate Clients. GTJA Investments will hold the Offer Shares on a 
non-discretionary basis for the purpose of hedging the economic exposure under the GTHT Back-to-back TRS 
and GTHT Client TRS only. During the tenor of the GTHT Client TRS, all economic returns of the Offer Shares 
will be passed to the GTHT Onshore Ultimate Clients and all economic losses shall be borne by the GTHT 
Onshore Ultimate Clients, subject to the terms and conditions of the GTHT Back-to-back TRS and GTHT Client 
TRS, and GTJA Investments will not take part in any economic return or bear any economic loss in relation 
to the price of the Offer Shares. The GTHT Onshore Ultimate Clients may request to redeem the Offer Shares 
at their own discretion, upon which GTJA Investments shall dispose of the Offer Shares and settle the GTHT 
Back-to-back TRS and GTHT Client TRS in cash in accordance with the terms and conditions of the GTHT 
Back-to-back TRS and GTHT Client TRS documents. Due to its internal policy, GTJA Investments will not 
exercise the voting right attaching to the Offer Shares during the tenor of the GTHT Back-to-back TRS and 
GTHT Client TRS.
To the best knowledge of GTJA Investments after making all reasonable enquiries, (i) each of the GTHT 
Onshore Ultimate Clients is an independent third party of GTJA Investments, GTJA Securities and the 
companies which are members of the same group of GTJA Securities; (ii) each of the ultimate beneficial owners 
holding 30% or more interests of GTHT Onshore Ultimate Clients is an independent third party of the Company, 
GTJA Investments, GTJA Securities, HTI and the companies which are members of the same group of GTJA 
Securities and HTI; and (iii) each of the GTHT Onshore Ultimate Clients and their respective ultimate beneficial 
owners is an independent third party of the Company, the subsidiaries, Controlling Shareholders, substantial 
shareholders, existing shareholders of the Company (the “Relevant Parties”), and respective subsidiaries and/or 
respective close associates of the Relevant Parties.
To the best knowledge of GTJA Investments and after making all reasonable enquiries, (i) GTJA Investments 
has confirmed that, to the best of their knowledge, each of the GTHT Onshore Ultimate Clients and the ultimate 
beneficial owners holding 30% or more interest of the GTHT Onshore Ultimate Clients listed above is an 
independent third party of GTJA Investments, GTJA Securities, HTI and the companies which are members 
of the same group of companies as GTJA Securities and HTI, and (ii) GTJA Investments is not a collective 
investment scheme which is not authorised by the SFC nor is expected to hold the Offer Shares on behalf of 
such scheme.
(3) 
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public 
offerings (“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products issued by 
appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. In 
connection with such products, the licensed domestic securities firms, through their Hong Kong affiliates, may 
participate in Hong Kong IPOs either as placees or cornerstone investors (the “Cross-border Derivatives 
Trading Regime”).

<<<PAGE 23>>>
23
Huatai Securities Co., Ltd. (“Huatai Securities”), the shares of which are listed on both the Shanghai Stock 
Exchange (stock code: 601688) and the Stock Exchange (stock code: 6886), is one of the domestic securities 
firms licensed to undertake cross-border derivatives trading activities. Huatai Securities entered into an ISDA 
agreement (the “ISDA Agreement”) with its indirectly wholly-owned subsidiary, HTCI to set out the principal 
terms of any future total return swap between Huatai Securities and HTCI.
HTFH is the Overall Coordinator in connection with the Global Offering. Pursuant to the ISDA Agreement, 
HTCI, which intends to participate in the Global Offering as a placee, will hold the beneficial interest of the 
Offer Shares on a non-discretionary basis as the single underlying holder under a back-to-back total return swap 
(the “Back-to-back TRS”) to be entered by HTCI in connection with a Client TRS (as defined below) placed by 
and fully funded (i.e. with no financing provided by HTCI) by the Huatai Ultimate Clients (as defined below), 
by which, HTCI will, subject to customary fees and commissions, pass the full economic exposure of the 
Offer Shares ultimately to the Huatai Ultimate Clients, which in effect, HTCI will hold the beneficial interest 
of the Offer Shares on behalf of the Huatai Ultimate Clients. HTFH and HTCI are indirectly wholly-owned 
subsidiaries of Huatai Securities. Accordingly, HTCI is considered as a “connected client” of HTFH pursuant to 
paragraph 13(7) of the Placing Guidelines.
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the “Huatai Ultimate 
Clients”) cannot directly subscribe for the Offer Shares but may invest in derivative products issued by domestic 
securities firms licenced to undertake cross-border derivatives trading activities, such as Huatai Securities, 
with the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, the Huatai 
Ultimate Clients, through its investment manager, will place a total return swap order (the “Client TRS”) with 
Huatai Securities in connection with the Company’s IPO and Huatai Securities will place a Back-to-back TRS 
order to HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the Back-to-back TRS, 
HTCI participates in the Company’s IPO and subscribes the Offer Shares through placing order with HTFH 
during the International Offering.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in connection 
with the Client TRS order placed by the Huatai Ultimate Clients. Pursuant to the terms of the contracts of the 
Back-to-back TRS and the Client TRS, during the tenor of the Back-to-back TRS and the Client TRS, subject 
to customary fees and commissions, all economic returns of the Offer Shares will be ultimately passed to the 
Huatai Ultimate Clients through the Back-to-back TRS and the Client TRS and all economic loss shall be 
ultimately borne by the Huatai Ultimate Clients. HTCI will not take any economic return or bear any economic 
loss in relation to the Offer Shares.
Investment in the Back-to-back TRS and the Client TRS is similar to the investment in a qualified domestic 
institutional investor fund (“QDII”) in the way that the Huatai Ultimate Clients would reap all the economic 
benefits of the underlying Offer Shares, except that a QDII fund would pass through the exchange rate exposure 
on both the notional value of the investment and the profit and loss of the investment. In contrast, the profit and 
loss of the Back-to-back TRS and the Client TRS factor into account the fluctuation in RMB exchange rate upon 
termination of the Client TRS by converting the profit and loss using the current exchange rate at the time of 
termination. As such, the Huatai Ultimate Clients would bear the exchange rate exposure of the profit and loss 
on settlement date.
The Huatai Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time 
from the issue date of the Client TRS which should be on or after the date on which the Offer Shares are listed 
on the Stock Exchange at their own discretion. Upon the termination upon maturity or early termination of the 
Client TRS by the Huatai Ultimate Clients, HTCI will dispose the Offer Shares on the secondary market and 
the Huatai Ultimate Clients will receive a final settlement amount in cash in accordance with the terms and 
conditions of the Back-to-back TRS and the Client TRS which should have taken into account all the economic 
returns or economic loss in relation to the Offer Shares. If upon the maturity of the Client TRS, the Huatai 
Ultimate Clients intend to extend the investment period, subject to further agreement between Huatai Securities 
and the relevant Huatai Ultimate Clients, the term of the Client TRS could be extended by way of a new 
issuance or a tenor extension. Accordingly, Huatai Securities will extend the term of the Back-to-back TRS by 
way of a new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass 
through the economic exposure to the Huatai Ultimate Clients, each being an onshore client who places a Client 
TRS order with Huatai Securities in connection with the IPO of the Company. HTCI will not exercise the voting 
right of the Offer Shares during the tenor of the Back-to-back TRS.

<<<PAGE 24>>>
24
During the life of the Client TRS and Back-to-back TRS, HTCI may continue to hold the Offer Shares in its 
custodian account, or to hold some or all of the Offer Shares in a prime brokerage account for stock borrowing 
purposes, where HTCI will lend out its holding of underlying Offer Shares in the form of stock borrowing loans 
consistent with market practice to lower its finance costs, provided that HTCI has the ability to call back the 
Offer Shares on loan at any time in order to satisfy its obligations under the Back-to-back TRS to ensure the 
economic interests are ultimately passed to the Huatai Ultimate Clients.
To the best of the knowledge of HTCI and after making all reasonable enquiries, each of the Huatai Ultimate 
Clients is an independent third party of (i) the Company, the connected person or the associates thereof, and (ii) 
HTCI, HTFH and the companies which are members of the same group of HTCI.
Huatai Ultimate Clients
Ultimate Beneficial Owners 
(“UBO”)/Fund Manager
Remarks
Ruining Xinrong Qiande CSI 500 Index Enhanced 
Private Securities Investment Fund*(睿凝新榮乾德中
證500指數增強私募證券投資基金)
Beijing Ruining Private Equity Fund 
Management Co., Ltd* (北京睿凝私募
基金管理有限公司)
Fund Manager – 
with UBO with over 
30% interest being 
Wang Rui (王睿)
Wu Mao (吳茂)
UBO with over 30% 
interest
* For identification purposes only
(4) 
ABCI AM intends to hold the Offer Shares in its capacity as manager managing investment portfolios on behalf 
of underlying investors on a discretionary basis, each of which is an independent third party of the Company, 
its subsidiaries, its Controlling Shareholders, its substantial shareholders, ABCI AM, ABCI and the companies 
which are members of the same group of ABCI.
(5) 
GFGC is to invest on non-discretionary basis. GFGC and GF Securities Co., Ltd. will enter into a series of 
cross border delta-one OTC swap transactions (the “OTC Swaps”) with each other and the ultimate clients (the 
“GFGC Ultimate Clients”), pursuant to which GFGC will hold the Offer Shares on a non-discretionary basis 
to hedge the OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed to 
the GFGC Ultimate Clients, subject to customary fees and commissions. The OTC swaps will be fully funded 
by the GFGC Ultimate Clients. During the terms of the OTC Swaps, all economic returns of the Offer Shares 
subscribed by GFGC will be passed to the GFGC Ultimate Clients and all economic loss shall be borne by the 
GFGC Ultimate Clients through the OTC Swaps, and GFGC will not take part in any economic return or bear 
any economic loss in relation to the Offer Shares. The OTC Swaps are linked to the Offer Shares and the GFGC 
Ultimate Clients may request GFGC to redeem it at their own discretions, upon which GFGC shall dispose of 
the Offer Shares and settle OTC Swaps in cash in accordance with the terms and conditions of the OTC Swap. 
Despite that GFGC will hold the legal title of the Offer Shares by itself, it will not exercise the voting rights 
attaching to the relevant Offer Shares during the terms of the OTC Swaps according to its internal policy. 
GFGC will hold the Offer Shares on a non-discretionary basis for and on behalf of the following GF Ultimate 
Clients: (i) Yuanxin Private Securities Investment Fund No. 2 (Enhanced Private Placement Strategy) (“Yuanxin 
Fund No.2”) 遠信定增策略增強 2 號私募證券投資基金, whose UBO holding 30% or more interest is Weifeng 
Zhou; and (ii) Yuanxin China Value Growth Select Private Securities Investment Fund (“Yuanxin China Value 
Growth”) 遠信中國價值成長精選私募證券投資基金, whose UBO holding 30% or more interest is Weifeng 
Zhou.

<<<PAGE 25>>>
25
(6) 
E Fund Management will hold the Offer Shares for and on behalf of their underlying clients (the “E Fund 
Management Ultimate Clients”) on discretionary basis. To the best knowledge of E Fund Management and 
after making all reasonable enquiries, each of the E Fund Management Ultimate Clients is independent from 
the Company, its subsidiaries, its Controlling Shareholders, its substantial shareholders, GF Securities, E Fund 
Management and the companies which are members of the same group of companies as GF Securities.
(7) 
E Fund HK will hold the Offer Shares for and on behalf of their underlying clients (the “E Fund HK Ultimate 
Clients”) on discretionary basis. To the best knowledge of E Fund HK and after making all reasonable 
enquiries, each of the E Fund HK Ultimate Clients is independent from the Company, its subsidiaries, its 
Controlling Shareholders, its substantial shareholders, GF Securities, E Fund HK and the companies which are 
members of the same group of companies as GF Securities.
(8) 
CGII and China Galaxy Securities Co., Ltd. (“CGS”) will enter into a series of cross border total return swap 
(TRS) transactions (collectively, the “CGII TRS”) with each other and the ultimate clients (“CGII Ultimate 
Clients”), pursuant to which CGII will hold the Offer Shares on a non-discretionary basis to hedge the CGII 
TRS while the economic risks and returns of the underlying Offer Shares are ultimately borne by the CGII 
Ultimate Clients, subject to customary fees and commissions. The CGII TRS will be fully funded by the CGII 
Ultimate Clients. During the terms of the CGII TRS, all economic returns of the Offer Shares subscribed by 
CGII will be passed to CGII Ultimate Clients and all economic loss shall be borne by CGII Ultimate Clients 
through the CGII TRS, and CGII will not take part in any economic return or bear any economic loss in 
relation to the Offer Shares. The CGII TRS are linked to the Offer Shares and CGII Ultimate Clients may, 
after expiration of the lock-up period beginning from the date of the relevant cornerstone agreements and 
ending on the date which is six months from the Listing Date, request to early terminate the CGII TRS at its 
own discretion, upon which CGII may dispose of the Offer Shares on the secondary market and CGII Ultimate 
Clients will receive a final settlement amount of the CGII TRS in cash in accordance with the terms and 
conditions of the CGII TRS. To the best of CGII’ s knowledge after having made all reasonable inquiries, each 
of the CGII Ultimate Clients is an independent third party of (i) the Company, its subsidiaries, its Controlling 
Shareholders, its substantial shareholders, and (ii) CGII, and the companies which are members of the same 
group of CGIS. Both CGII and CGIS are indirect wholly-owned subsidiaries of CGS, the A shares of which 
are listed on the Shanghai Stock Exchange (stock code: 601881), the H shares of which are listed on the Stock 
Exchange (stock code: 6881). CGII is a connected client (as defined under Appendix F1 to the Listing Rules) of 
CGIS, holding securities on a non-discretionary basis on behalf of independent third parties.
CGII Ultimate Clients
Ultimate Beneficial Owners (“UBO”)/
Fund Manager
Remarks
Shenzhen Commando Capital Management Co., 
Ltd. (深圳市康曼德資本管理有限公司)
Ding Ying (丁楹)
UBO
Jindan Yuanyang No. 6 Private Securities 
Investment Fund (金澹遠洋6號私募證券投資 
基金)
Ding Hai (丁海)
UBO with over 30% 
interest
Shanghai Jindan Asset Management 
Co., Ltd. (上海金澹資產管理有限公司)
Fund Manager – with 
UBO with over 30% 
interest being Zhang Yan 
(張焱)

<<<PAGE 26>>>
26
Allocations under the Employee Preferential Offering
Of the 47,033,100 Offer Shares initially being offered under the International Offering, no more 
than 5,225,000 Offer Shares, representing approximately 11.11% of the Offer Shares initially 
available for subscription under the International Offering, are available for subscription as 
Employee Reserved Shares by the Eligible Employees on a preferential basis under the Employee 
Preferential Offering according to Rule 10.01 of the Listing Rules. For details, please refer to 
the section headed “Structure of the Global Offering – Employee Preferential Offering” of the 
Prospectus.
3,339,500 Offer Shares have been placed to 222 Eligible Employees pursuant to the Employee 
Preferential Offering, representing approximately 6.39% of the total number of Offer Shares 
initially available under the Global Offering (before exercise of the Over-allotment Option). 
Each Eligible Employees confirms that he/she is and remains an employee as of the date of the 
prospectus and is not a core connected person of the Company.
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or 
any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer 
or solicitation to purchase or subscribe for any securities in the United States or in any other 
jurisdictions. The Offer Shares have not been, and will not be, registered under the United States 
Securities Act of 1933, as amended (the “U.S. Securities Act”) or securities law of any state 
or other jurisdiction of the United States. The Offer Shares may not be offered, sold, pledged 
or otherwise transferred within the United States, except pursuant to an available exemption 
from, or in a transaction not subject to, the registration requirements of the U.S. Securities Act. 
There will be no public offer of the Offer Shares in the United States. The Offer Shares are 
being offered and sold solely (1) to qualified institutional buyers as defined in Rule 144A under 
the U.S. Securities Act pursuant to Rule 144A or another available exemption from registration 
under the U.S. Securities Act and (2) outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act.

<<<PAGE 27>>>
27
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the prospectus dated January 14, 2026 (the “Prospectus”) issued 
by Shanghai Longcheer Technology Co., Ltd. (上海龍旗科技股份有限公司) (the “Company”) 
for detailed information about the Global Offering described below before deciding whether or 
not to invest in the H Shares thereby being offered. Any investment decision in relation to the 
Offer Shares should be taken solely in reliance on the information in the Prospectus.
* Potential investors of the Offer Shares should note that the Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the 
occurrence of any of the events set out in the section headed “Underwriting – Hong Kong 
Underwriting Arrangements – Hong Kong Public Offering – Hong Kong Underwriting 
Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong 
Kong time) on the Listing Date (which is currently expected to be on Thursday, January 22, 
2026)
PUBLIC FLOAT AND FREE FLOAT
Immediately upon the completion of the Global Offering (before any exercise of the Over-allotment 
Option), the number of H Shares held in public hands represents approximately 10.02% of the 
total issued share capital of the Company (excluding treasury Shares), which is higher than the 
prescribed percentage of H Shares required to be held in public hands of 10.00% under Rule 
19A.13A(2)(a) of the Hong Kong Listing Rules.
The Directors confirm that, immediately upon the completion of the Global Offering (before any 
exercise of the Over-allotment Option), (i) no placee will, individually, be placed more than 10% 
of the enlarged issued share capital of the Company immediately after the Global Offering; (ii) 
there will not be any new substantial Shareholder immediately after the Global Offering; (iii) the 
three largest public shareholders of the Company do not hold more than 50% of the H shares in 
public hands at the time of the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing 
Rules; and (iv) there will be at least 300 Shareholders at the time of the Listing in compliance with 
Rule 8.08(2) of the Listing Rules.
Based on the final Offer Price of HK$31.00 per Offer Share and the total number of Offer Shares 
as subscribed by the Cornerstone Investors of 14,200,900 H Shares, representing approximately 
2.72% of the total issued share capital of our Company (excluding treasury Shares), the free 
float of our Company is 7.28% and with a market value at the time of Listing of approximately 
HK$1,179.8 million, which is substantially higher than the 5% threshold and an expected market 
value at the time of Listing of not less than HK$50,000,000 under Rule 19A.13C(2). The Company 
satisfies the free float requirement under Rule 19A.13C(2) of the Hong Kong Listing Rules.

<<<PAGE 28>>>
28
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Thursday, January 
22, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting – Underwriting Arrangements 
and Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade the H Shares on the basis of publicly available allocation 
details prior to the receipt of H Share certificates or prior to the H Share certificates becoming 
valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Thursday, 
January 22, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Thursday, January 22, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 100 H Shares each, and the stock code of the H Shares will 
be 9611.
By order of the Board
Shanghai Longcheer Technology Co., Ltd.
上海龍旗科技股份有限公司
Mr. DU Junhong
Chairman and Executive Director
Hong Kong, January 21, 2026
As at the date of this announcement, the Board comprises: (i) Mr. DU Junhong, Mr. GE Zhengang, 
Mr. GUAN Yadong and Ms. QIN Yanling as executive Directors; and (ii) Dr. SHEN Jianxin, 
Mr. YANG Chuan and Dr. NIU Shuangxia as independent non-executive Directors.
