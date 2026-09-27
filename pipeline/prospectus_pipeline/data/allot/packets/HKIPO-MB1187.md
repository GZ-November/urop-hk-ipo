# 配发结果公告抽取任务：1187.HK Cofoe Medical Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**05/05/2026 22:12**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0505/2026050501942.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1187.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
in the United States or in any other jurisdictions. The securities mentioned herein have not been, and will not be, 
registered under the United States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or 
securities law of any state or other jurisdiction of the United States. The securities may not be offered, sold, pledged 
or otherwise transferred within the United States except pursuant to an exemption from the registration requirements 
of the U.S. Securities Act and in compliance with any applicable state securities laws. The securities are being offered 
and sold outside the United States in offshore transactions in accordance with Regulation S under the U.S. Securities 
Act. There will be no public offer of securities in the United States.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
April 27, 2026 (the “Prospectus”) issued by Cofoe Medical Technology Co., Ltd. (可孚醫療科技股份有限公司) (the 
“Company”) for detailed information about the Global Offering described below before deciding whether or not to 
invest in the H Shares thereby being offered. Any investment decision in relation to the Offer Shares should be taken 
solely in reliance on the information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinators (for themselves and on behalf 
of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting 
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
Wednesday, May 6, 2026).

<<<PAGE 2>>>
2
Cofoe Medical Technology Co., Ltd.*
可孚醫療科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
27,000,000 H Shares
Number of Hong Kong Offer Shares
:
2,700,000 H Shares
Number of International Offer Shares
:
24,300,000 H Shares
Final Offer Price
:
HK$39.33 per H Share, plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
AFRC transaction levy of 0.00015% and 
Hong Kong Stock Exchange trading fee of 
0.00565%
Nominal value
:
RMB1.00 per H Share
Stock code
:
1187
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators, 
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Other Overall Coordinator, Joint Global Coordinator, 
Joint Bookrunner and Joint Lead Manager
* 
for identification purpose only

<<<PAGE 3>>>
3
Cofoe Medical Technology Co., Ltd.*
可孚醫療科技股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated April 27, 2026 (the “Prospectus”) issued by 
Cofoe Medical Technology Co., Ltd. (可孚醫療科技股份有限公司) (the “Company”).
SUMMARY
Company information
Stock code
1187
Stock short name
COFOE
Dealings commencement date
May 6, 2026*
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$39.33
Maximum Offer Price
HK$39.33
Offer Shares and Share Capital
Number of Offer Shares
27,000,000
Final Number of Offer Shares in Hong Kong Public Offering
2,700,000
Final Number of Offer Shares in International Offering
24,300,000
Number of issued Shares upon Listing
235,897,000
Number of Offer Shares over-allocated (Note)
0
Note: There is no over-allotment option in the International Offering, and no stabilization activities will be carried out 
in relation to the Global Offering.

<<<PAGE 4>>>
4
Proceeds
Gross proceeds (Note)
HK$1,062.0 million
Less: Estimated listing expenses payable based on 
   Final Offer Price
HK$54.9 million
Net proceeds
HK$1,007.1 million
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of proceeds, 
please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
105,939
No. of successful applications
15,008
Subscription level
399.08 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong 
 Public Offering
2,700,000
Number of Offer Shares reallocated from the International 
 Offering
0
Final no. of Offer Shares under the Hong Kong Public Offering
2,700,000
% of Offer Shares under the Hong Kong Public Offering to 
 the Global Offering
10.00%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by identification number or www.hkeipo.hk/IPOResult for the 
full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
129
Subscription Level
3.4 times
No. of Offer Shares initially available under the International 
 Offering
24,300,000
Number of Offer Shares reallocated to the Hong Kong Public 
 Offering
0
Final no. of Offer Shares under the International Offering
24,300,000
% of Offer Shares under the International Offering to 
 the Global Offering
90.00%
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a 
waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit the Company to allocate certain Offer Shares in the International Offering 
to certain Existing Minority Shareholders, (b) a consent under paragraph 18 of Chapter 4.15 of 
the Guide for New Listing Applicants to permit the Company to, among other things, allocate 
further H Shares in the International Offering to certain cornerstone investors, and (c) a consent 
under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate certain Offer 
Shares in the International Offering to connected clients, (i) none of the Offer Shares subscribed 
by the placees and the public have been financed directly or indirectly by the Company, any of 
the Directors, chief executive of the Company, Controlling Shareholders, substantial Shareholders, 
existing Shareholders of the Company or any of its subsidiaries or their respective close associates; 
and (ii) none of the placees and the public who have purchased the Offer Shares are accustomed 
to taking instructions from the Company, any of the Directors, chief executive of the Company, 
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company or any 
of its subsidiaries or their respective close associates in relation to the acquisition, disposal, voting 
or other disposition of H Shares registered in his/her/its name or otherwise held by him/her/it.

<<<PAGE 6>>>
6
The placees in the International Offering include the following:
Cornerstone Investors
Cornerstone Investors
No. of 
Offer Shares 
allocatedNote 1
% of 
Offer Shares
% of total issued 
share capital 
after the Global 
Offering(Note 4)
Existing 
shareholders 
or their close 
associates
Lens Technology (HK) Co. Limited (藍思科技(香港)有限公司)
(“Lens Technology (HK)”)
1,990,900
7.37%
0.84%
No
Changsha Yufeng Technology Co., Ltd. (長沙雨豐科技有限公
司)(“Changsha Yufeng”)
1,390,700
5.15%
0.59%
Yes (Note 2)
Vision Capital Management Co., Ltd. (遠信(珠海)私募基
金管理有限公司) (“Vision Capital”) and China Galaxy 
International Investment Company Limited (“CGII”) (in 
connection with Vision Capital OTC Swaps)
1,296,000
4.80%
0.55%
Yes (Note 2)
Panjing Harbourview Investment Fund (盤京港景投資基金) 
(“Panjing Fund”)
995,400
3.69%
0.42%
No
FR M CONSULTING CO., LTD (“FR M CONSULTING”)
597,200
2.21%
0.25%
No
HongKong HQD Industry Limited (香港漢清達實業有限公司) 
(“HQD Industry”)
497,700
1.84%
0.21%
No
Da Cheng International Asset Management Company Limited 
(大成國際資產管理有限公司) (“Da Cheng International”)
398,100
1.47%
0.17%
No
Sinohealth Technology Holdings Limited (中康科技控股有限公
司) (“Sinohealth Technology”)
398,100
1.47%
0.17%
No
ODI TRUST LIMITED (“ODI TRUST”)
199,000
0.74%
0.08%
No
Huang Xuelin (黃雪林) (“Mr. Huang”)
995,400
3.69%
0.42%
No
Dai Jun’an (戴鈞安) (“Mr. Dai”)
497,700
1.84%
0.21%
No
Lu Qinchao (陸勤超) (“Ms. Lu”)
398,100
1.47%
0.17%
No
Total
9,654,300
35.76%
4.09%
Notes:
(1) 
The number of Offer Shares allocated to such investors only represents the number of Offer Shares allocated 
to the investors as cornerstone investors in the International Offering. For allocations of Offer Shares to 
the relevant investors as placees (if any), please refer to the section headed “Allotment Results Details – 
International Offering – Allottees with Waiver/Consents obtained” in this announcement.
(2) 
For details of a consent under paragraph 1C(2) of the Placing Guidelines granted by the Stock Exchange to 
permit the Company to allocate certain Offer Shares in the International Offering to certain Existing Minority 
Shareholders as cornerstone investor, please refer to the section headed “Others/Additional Information” in this 
announcement.
(3) 
In addition to the Offer Shares subscribed for as Cornerstone Investors, Lens Technology (HK), FR M 
CONSULTING, HQD Industry, Da Cheng International, ODI TRUST, Mr. Huang, Mr. Dai and Ms. Lu were 
allocated further Offer Shares as placees in the International Offering. Please refer to the section headed 
“Allotment Results Details – International Offering – Allottees with Waivers/Consents Obtained” in this 
announcement for details. Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-
up as indicated below. For details, please refer to the section headed “Lock-up Undertakings – Cornerstone 
Investors” in this announcement.
(4) 
Not taking into account any A Shares held by the relevant investor(s).

<<<PAGE 7>>>
7
Allottees with Waivers/Consents Obtained
Investor
No. of 
Offer Shares 
allocated
% of 
Offer Shares
% of total 
issued share 
capital after 
the Global 
OfferingNote 1, 3
Relationship
Allottees with waiver from strict compliance with the requirements under Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by Existing Minority Shareholders holding 1% 
or more of the issued share capital of the Company immediately prior to the completion of the Global Offering and/or their close 
associatesNote 1,3
Vision Capital Management Co., Ltd. (遠信(珠
海)私募基金管理有限公司)
1,296,000
4.8%
0.55%
An Existing Minority 
 Shareholder
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of 
further H Shares to certain Cornerstone InvestorsNote 1
Lens Technology (HK) Co. Limited (藍思科技
(香港)有限公司) (“Lens Technology (HK)”)
1,951,000
7.23%
0.83%
A Cornerstone Investor disclosed 
 in the Prospectus.
FR M CONSULTING CO., LTD (“FR M 
CONSULTING”)
199,000
0.74%
0.08%
A Cornerstone Investor disclosed 
 in the Prospectus.
HongKong HQD Industry Limited (香港漢清達
實業有限公司) (“HQD Industry”)
497,700
1.84%
0.21%
A Cornerstone Investor disclosed 
 in the Prospectus.
Da Cheng International Asset Management 
Company Limited (大成國際資產管理有限公
司) (“Da Cheng International”)
318,500
1.18%
0.14%
A Cornerstone Investor disclosed 
 in the Prospectus.
ODI TRUST LIMITED (“ODI TRUST”)
152,500
0.56%
0.06%
A Cornerstone Investor disclosed 
 in the Prospectus.
Huang Xuelin (黃雪林) (“Mr. Huang”)
975,000
3.61%
0.41%
A Cornerstone Investor disclosed 
 in the Prospectus.
Dai Jun’an (戴鈞安) (“Mr. Dai”)
488,000
1.81%
0.21%
A Cornerstone Investor disclosed 
 in the Prospectus.
Lu Qinchao (陸勤超) (“Ms. Lu”)
97,500
0.36%
0.04%
A Cornerstone Investor disclosed 
 in the Prospectus.
Subtotal
4,679,200
17.33%
1.98%

<<<PAGE 8>>>
8
Investor
No. of 
Offer Shares 
allocated
% of 
Offer Shares
% of total 
issued share 
capital after 
the Global 
OfferingNote 1, 3 Relationship
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in 
relation to allocations to connected clientsNote 1
Huatai Capital Investment Limited (“HTCI”)
119,000
0.44%
0.05% Connected client 
 investing as a placee
China Southern Asset Management Co., Ltd. 
(“CSAM”)
995,400
3.69%
0.42% Connected client 
 investing as a placee
Guotai Junan Investments (Hong Kong) Limited 
(“GTJAI”)
199,000
0.74%
0.08% Connected client 
 investing as a placee
Fullgoal Fund Management Co., Ltd. (“Fullgoal 
Fund”)
187,500
0.69%
0.08% Connected client 
 investing as a placee
Fullgoal Asset Management (HK) Limited 
(“Fullgoal HK”)
210,500
0.78%
0.09% Connected client 
 investing as a placee
CITIC Securities International Capital 
Management Limited (“CSICM”)
20,000
0.07%
0.01% Connected client 
 investing as a placee
Shanxi Securities International Asset Management 
Limited (“SSIAM”)
20,000
0.07%
0.01% Connected client 
 investing as a 
 placee
Valuable Investment Limited (“VIL”)
59,500
0.22%
0.03% Connected client 
 investing as a placee
Notes:
(1) 
For details of (a) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of the Placing Guidelines granted by the Stock Exchange to permit the Company to allocate 
certain Offer Shares in the International Offering to Existing Minority Shareholders; (b) a consent under 
paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to allocate certain 
Offer Shares in the International Offering to certain Cornerstone Investors; and (c) a consent under paragraph 
1C(1) of the Placing Guidelines to permit the Company to allocate certain Offer Shares in the International 
Offering to connected clients and details of ultimate clients adopting TRS arrangements, please refer to the sub-
section relating to section headed “Others/Additional Information” in this announcement.
(2) 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details – International Offering – Cornerstone Investors” in this announcement.
(3) 
Among the Cornerstone Investors, Vision Capital and Changsha Yufeng are Existing Minority Shareholders, 
and Vision Capital holds more than 1% of the issued share capital of the Company immediately prior to the 
completion of the Global Offering. The Stock Exchange has granted a waiver from strict compliance with the 
requirements under Rule 10.04 of the Listing Rules and consent under Paragraph 1C(2) of the Placing Guidelines 
to permit H Shares in the International Offering to be placed to certain Existing Minority Shareholders. Please 
refer to the section headed “Waivers from Strict Compliance with the Listing Rules – Allocation of H Shares to 
Existing Minority Shareholders and Their Close Associates” of the Prospectus for details.

<<<PAGE 9>>>
9
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number 
of Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing
Number 
of H Shares 
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
% of 
total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakingsNote 1
Zhang Min (張敏) (“Mr. Zhang”)
12,114,881
0
5.14%
0%
November 5, 2026 (First 
Sixth-Month Period)Note 1
May 5, 2027 (Second 
Sixth-Month Period)Note 2
Nie Juan (聶娟) (“Ms. Nie”)
3,485,739
0
1.48%
0%
November 5, 2026 (First 
Sixth-Month Period)Note 1
May 5, 2027 (Second 
Sixth-Month Period)Note 2
Changsha Keyuan Tongchuang Enterprise  
Management Center (Limited Partnership)  
(長沙科源同創創業投資合夥企業(有限合
夥)) (“Changsha Keyuan”)
12,114,881
0
5.14%
0%
November 5, 2026 (First 
Sixth-Month Period)Note 1 
May 5, 2027 (Second 
Sixth-Month Period)Note 2
Changsha Xiezihao Medical Investment Co., 
Ltd. (長沙械字號醫療投資有限公司)  
(“Changsha Xiezihao”)
85,079,923
0
36.07%
0%
November 5, 2026 (First 
Sixth-Month Period)Note 1
May 5, 2027 (Second 
Sixth-Month Period)Note 2
Notes:
(1) 
The Controlling Shareholders will cease to be prohibited from disposing of or transferring H Shares after the 
indicated date.
(2) 
In accordance with the relevant Listing Rule/guidance materials, the required lock-up for the first six-month 
period ends on November 5, 2026, and for the second six-month period, on May 5, 2027.
(3) 
For illustrative purposes only, this subsection lists only those members of the Controlling Shareholders who 
hold Shares directly in the Company. Immediately upon completion of the Global Offering (without taking into 
account any A Shares to be issued upon exercise of the share options granted under the Employee Incentive 
Schemes), Mr. Zhang, Ms. Nie, Changsha Xiezihao and Changsha Keyuan are expected to be entitled to exercise 
an aggregate of approximately 47.82% voting rights in our Company. Upon Listing, each of Mr. Zhang, Ms. 
Nie, Changsha Xiezihao and Changsha Keyuan will constitute a group of the Controlling Shareholders and each 
of them is subject to the same lock-up as disclosed above.

<<<PAGE 10>>>
10
Cornerstone Investors
NameNote 1
Number of Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing
Number 
of H Shares 
held in the 
Company subject
 to lock-up 
undertakings 
upon Listing
% of total 
issued H Shares 
after the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing
% of 
shareholding in 
Company subject 
to lock-up
 undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakingsNote 2
Lens Technology (HK)
1,990,900
1,990,900
7.37%
0.84%
November 5, 2026
Changsha Yufeng
1,390,700
1,390,700
5.15%
0.59%
November 5, 2026
Vision Capital and CGII (in connection with 
Vision Capital OTC Swaps)
1,296,000
1,296,000
4.80%
0.55%
November 5, 2026
Panjing Fund
995,400
995,400
3.69%
0.42%
November 5, 2026
FR M CONSULTING
597,200
597,200
2.21%
0.25%
November 5, 2026
HQD Industry
497,700
497,700
1.84%
0.21%
November 5, 2026
Da Cheng International
398,100
398,100
1.47%
0.17%
November 5, 2026
Sinohealth Technology
398,100
398,100
1.47%
0.17%
November 5, 2026
ODI TRUST 
199,000
199,000
0.74%
0.08%
November 5, 2026
Mr. Huang
995,400
995,400
3.69%
0.42%
November 5, 2026
Mr. Dai
497,700
497,700
1.84%
0.21%
November 5, 2026
Ms. Lu
398,100
398,100
1.47%
0.17%
November 5, 2026
Sub-total
9,654,300
9,654,300
35.76%
4.09%
Notes:
(1) 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in 
the Prospectus.
(2) 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on November 
5, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or transferring H Shares 
subscribed for pursuant to the relevant cornerstone investment agreements after the indicated date.
PLACEE CONCENTRATION ANALYSIS
Placees*
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
Number
of H Shares
held upon
Listing
% of total
issued share
capital upon
Listing
Top 1
3,941,900
16.22%
14.60%
3,941,900
1.67%
Top 5
9,594,400
39.48%
35.53%
9,594,400
4.07%
Top 10
14,357,100
59.08%
53.17%
14,357,100
6.09%
Top 25
20,011,200
82.35%
74.12%
20,011,200
8.48%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 11>>>
11
H SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders*
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
Number
of H Shares
held upon
Listing
% of total
issued
H Shares
capital upon
Listing
Number of
Shares
held upon
Listing
Top 1
3,941,900
16.22%
14.60%
3,941,900
14.60%
3,941,900
Top 5
9,594,400
39.48%
35.53%
9,594,400
35.53%
20,276,798
Top 10
14,357,100
59.08%
53.17%
14,357,100
53.17%
25,039,498
Top 25
20,011,200
82.35%
74.12%
20,011,200
74.12%
30,693,598
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
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
% of
total issued
share capital
upon Listing
Top 1
0
0.00%
0.00%
0
112,795,424
47.82%
Top 5
1,296,000
5.33%
4.80%
1,296,000
142,463,743
60.39%
Top 10
5,237,900
21.56%
19.40%
5,237,900
159,958,622
67.81%
Top 25
14,357,100
59.08%
53.17%
14,357,100
177,779,947
75.36%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 12>>>
12
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
Pool A
Approximate
percentage
allotted of the
Number
Number
total number of
of H Shares
of valid
H Shares
applied for
applications
Basis of allocation/ballot
applied for
100
36,115
1,806 out of 36,115 applicants to receive 100 H Shares
5.00%
200
23,947
1,592 out of 23,947 applicants to receive 100 H Shares
3.32%
300
4,338
341 out of 4,338 applicants to receive 100 H Shares
2.62%
400
2,377
210 out of 2,377 applicants to receive 100 H Shares
2.21%
500
3,566
346 out of 3,566 applicants to receive 100 H Shares
1.94%
600
1,613
169 out of 1,613 applicants to receive 100 H Shares
1.75%
700
1,122
125 out of 1,122 applicants to receive 100 H Shares
1.59%
800
1,239
146 out of 1,239 applicants to receive 100 H Shares
1.47%
900
882
109 out of 882 applicants to receive 100 H Shares
1.37%
1,000
7,327
943 out of 7,327 applicants to receive 100 H Shares
1.29%
1,500
2,064
314 out of 2,064 applicants to receive 100 H Shares
1.01%
2,000
1,745
299 out of 1,745 applicants to receive 100 H Shares
0.86%
2,500
1,517
285 out of 1,517 applicants to receive 100 H Shares
0.75%
3,000
1,246
252 out of 1,246 applicants to receive 100 H Shares
0.67%
3,500
602
130 out of 602 applicants to receive 100 H Shares
0.62%
4,000
663
151 out of 663 applicants to receive 100 H Shares
0.57%
4,500
446
107 out of 446 applicants to receive 100 H Shares
0.53%
5,000
1,393
347 out of 1,393 applicants to receive 100 H Shares
0.50%
6,000
793
213 out of 793 applicants to receive 100 H Shares
0.45%
7,000
678
194 out of 678 applicants to receive 100 H Shares
0.41%
8,000
653
198 out of 653 applicants to receive 100 H Shares
0.38%
9,000
590
187 out of 590 applicants to receive 100 H Shares
0.35%
10,000
3,384
1,120 out of 3,384 applicants to receive 100 H Shares
0.33%
20,000
1,439
633 out of 1,439 applicants to receive 100 H Shares
0.22%
30,000
940
488 out of 940 applicants to receive 100 H Shares
0.17%
40,000
573
335 out of 573 applicants to receive 100 H Shares
0.15%
50,000
521
334 out of 521 applicants to receive 100 H Shares
0.13%
60,000
406
281 out of 406 applicants to receive 100 H Shares
0.12%
70,000
332
244 out of 332 applicants to receive 100 H Shares
0.10%
80,000
331
257 out of 331 applicants to receive 100 H Shares
0.10%
90,000
225
184 out of 225 applicants to receive 100 H Shares
0.09%
100,000
1,364
1,160 out of 1,364 applicants to receive 100 H Shares
0.09%
Total
104,431
Total number of Pool A successful applicants: 13,500

<<<PAGE 13>>>
13
Pool B
Approximate
percentage
allotted of the
Number
Number
total number of
of H Shares
of valid
H Shares 
applied for
applications
Basis of allocation/ballot
applied for
200,000
798
600 H Shares
0.30%
300,000
176
700 H Shares plus 126 out of 176 applicants to receive 
 an additional 100 H Shares
0.26%
400,000
104
800 H Shares plus 84 out of 104 applicants to receive 
 an additional 100 H Shares
0.22%
500,000
91
1,000 H Shares
0.20%
600,000
69
1,100 H Shares plus 60 out of 69 applicants to receive 
 an additional 100 H Shares
0.20%
700,000
39
1,300 H Shares plus 2 out of 39 applicants to receive 
 an additional 100 H Shares
0.19%
800,000
23
1,400 H Shares
0.18%
900,000
15
1,500 H Shares plus 4 out of 15 applicants to receive 
 an additional 100 H Shares
0.17%
1,000,000
71
1,600 H Shares plus 20 out of 71 applicants to receive 
 an additional 100 H Shares
0.16%
1,350,000
122
2,000 H Shares plus 53 out of 122 applicants to receive 
 an additional 100 H Shares
0.15%
Total
1,508
Total number of Pool B successful applicants: 1,508

<<<PAGE 14>>>
14
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or 
indirectly, provided by the Company, its Controlling Shareholders, Directors or syndicate members 
to any placees or the public (as the case may be) and the consideration payable by them for each 
Offer Share of the Company subscribed for or purchased by them is the same as the final Offer 
Price determined by agreement between the Company and the Sponsor-Overall Coordinators (for 
themselves and on behalf of the Underwriters), in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Allocation of H Shares to Existing Minority Shareholders with a waiver from the strict 
compliance with Rule 10.04 of the Listing Rules and a prior consent under paragraph 1C(2) 
of the Placing Guidelines
The Company has applied for, and the Stock Exchange has granted, a waiver from strict 
compliance with the requirements under Rule 10.04 of the Listing Rules and consent under 
Paragraph 1C(2) of the Placing Guidelines to permit H Shares in the International Offering to be 
placed to certain Existing Minority Shareholders.
Please refer to the section headed “Waiver from Strict Compliance with the Listing Rules and 
Exemption from Compliance with the Companies (Winding up and Miscellaneous Provisions) 
Ordinance – Allocation of H Shares to Existing Minority Shareholders and Their Close Associates” 
in the Prospectus for further details of the waiver and consent. The allocation of Offer Shares to 
such Existing Minority Shareholders is in compliance with all the conditions under the waiver/
consent granted by the Stock Exchange.

<<<PAGE 15>>>
15
Allocations of Offer Shares to certain Cornerstone Investors with a consent under paragraph 
18 of Chapter 4.15 of the Guide
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 
of the Guide for New Listing Applicants to permit the Company to allocate further Offer Shares 
in the International Offering to certain Cornerstone Investors as placees, subject to the following 
conditions (the “Size-based Exemption”):
(a) 
the final offering size of the Global Offering will be of a total value of at least HK$1 billion;
(b) 
each Director, chief executive and Controlling Shareholder of the Company confirms that no 
Offer Shares have been allocated to them or their respective close associates under the Size-
based Exemption;
(c) 
the allocation to certain Cornerstone Investors and/or their close associates will not affect 
the Company’s ability to satisfy the public float requirement under Rule 19A.13A(2) of the 
Listing Rules; and
(d) 
disclosure of details of the allocation to the Cornerstone Investors and/or their close 
associates under the Size-based Exemption.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to Cornerstone Investors, please refer to the section 
headed “Allotment Results Details – International Offering – Allottees with Waivers/Consents 
Obtained” in this announcement.
Placing to connected clients with a consent under paragraph 1C(1) of the Placing Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit each of HTCI, CSAM, GTJAI, 
Fullgoal Fund, Fullgoal HK, CSICM, SSIAM and VIL (the “Connected Clients”) to participate in 
the Global Offering as connected client and to participate in the Global Offering as a placee. The 
allocation of Offer Shares to such connected clients is in compliance with all the conditions under 
the consent granted by the Stock Exchange.
For details of the consents under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of 
the Guide for New Listing Applicants in relation to allocations to connected clients, please refer to 
the section headed “Others/Additional Information – Placing to connected clients with a consent 
under paragraph 1C(1) of the Placing Guidelines” in this announcement.

<<<PAGE 16>>>
16
Details of the placement to connected clients are set out below:
No.
Connected 
Distributor
Connected Client
Relationship
Whether the
Connected
Client is a
collective
investment
scheme
which is not
authorised by
the SFC or
is expected to
hold the Offer
Shares on
behalf of
such scheme
Number
of Offer
Shares to
be allocated
to the
Connected
Client
Approximate
percentage of
total number
of Offer
Shares under
the Global
Offering
Approximate
percentage of
total issued
share capital
after the
Global
Offering
Part A – Connected Clients holding the beneficial interest of the Offer Shares on a non-discretionary basis on behalf of independent third parties
1
Huatai Financial Holdings 
(Hong Kong) Limited 
(“HTFH”)
Huatai Capital 
Investment 
Limited 
(“HTCI”)
HTFH is one of the Sponsor-Overall Coordinators, 
Overall Coordinators, Joint Sponsors, Joint Global 
Coordinators, Joint Bookrunners and Joint Lead 
Managers and Capital Market Intermediaries in 
connection with the Global Offering. HTFH and 
HTCI are indirectly wholly-owned subsidiaries of 
Huatai Securities Co. Ltd., the shares of which are 
listed on both the Shanghai Stock Exchange (stock 
code: 601688) and the Stock Exchange (stock code: 
6886) (“Huatai Securities”). Accordingly, HTCI 
is considered as a “connected client” of HTFH 
pursuant to paragraph 1B of the Appendix F1 to the 
Listing Rules. 
(1)
No
119,000
0.44%
0.05%

<<<PAGE 17>>>
17
No.
Connected 
Distributor
Connected Client
Relationship
Whether the
Connected
Client is a
collective
investment
scheme
which is not
authorised by
the SFC or
is expected to
hold the Offer
Shares on
behalf of
such scheme
Number
of Offer
Shares to
be allocated
to the
Connected
Client
Approximate
percentage of
total number
of Offer
Shares under
the Global
Offering
Approximate
percentage of
total issued
share capital
after the
Global
Offering
2
Guotai Junan Securities (Hong 
Kong) Limited (“GTJAS”)
Guotai Junan 
Investments 
(Hong Kong) 
Limited 
(“GTJAI”)
GTJAS is a syndicate member  
who places securities of the Company in relation 
to the Global Offering. GTJAI is a member of the 
same group of companies as GTJAS. Accordingly, 
GTJAI is considered as a “connected client” of 
GTJAS pursuant to paragraph 1B of the Appendix 
F1 to the Listing Rules.
(3)
No
199,000
0.74%
0.08%
3
CITIC Securities Brokerage 
(HK) Limited (“CSB”)
CITIC Securities 
International 
Capital 
Management 
Limited 
(“CSICM”)
CSB is syndicate member who places securities of 
the Company in relation to the Global Offering. 
CSICM is a member of the same group of 
companies as CSB. Accordingly, CSICM is 
considered as a “connected client” of CSB pursuant 
to paragraph 1B of the Appendix F1 to the Listing 
Rules.
(6)
No
20,000
0.07%
0.01%
4
Valuable Capital Limited 
(“VCL”)
Valuable 
Investment 
Limited (“VIL”)
VCL is a syndicate member who places securities of 
the Company in relation to the Global Offering. 
VIL is the same group of companies as VCL. 
Accordingly, VIL is considered as a “connected 
client” of VCL pursuant to paragraph 1B of the 
Appendix F1 to the Listing Rules.
(8)
No
59,500
0.22%
0.03%

<<<PAGE 18>>>
18
No.
Connected 
Distributor
Connected Client
Relationship
Whether the
Connected Client
is a collective
investment
scheme which
is not authorised
by the SFC or
is expected
to hold the
Offer Shares on
behalf of
such scheme
Number of
Offer Shares
to be 
allocated to 
the Connected
Client
Approximate
percentage 
of total 
number of
Offer Shares
under the
Global 
Offering
Approximate
percentage 
of total 
issued share
capital after
the Global
Offering
Part B – Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties
1
HTFH
China Southern Asset 
Management Co., 
Ltd. (“CSAM”)
HTFH is one of the 
Sponsor-Overall 
Coordinators, Overall 
Coordinators, Joint 
Sponsors, Joint Global 
Coordinators, Joint 
Bookrunners and 
Joint Lead Managers 
and Capital Market 
Intermediaries in 
connection the Global 
Offering. CSAM is held 
by Huatai Securities 
as to 41.16%, which 
wholly owns HTFH. 
As such, CSAM and 
HTFH is a member 
of the same group of 
companies. Accordingly, 
CSAM is considered 
as a “connected client” 
of HTFH pursuant to 
paragraph 1B of the 
Appendix F1 to the 
Listing Rules.(2)
No
995,400
3.69%
0.42%

<<<PAGE 19>>>
19
No.
Connected 
Distributor
Connected Client
Relationship
Whether the
Connected Client
is a collective
investment
scheme which
is not authorised
by the SFC or
is expected
to hold the
Offer Shares on
behalf of
such scheme
Number of
Offer Shares
to be 
allocated to 
the Connected
Client
Approximate
percentage 
of total 
number of
Offer Shares
under the
Global 
Offering
Approximate
percentage 
of total 
issued share
capital after
the Global
Offering
2
Shanxi Securities 
International 
Limited (“SSI”)
Shanxi Securities 
International Asset 
Management 
Limited (“SSIAM”)
SSI is syndicate member 
who places securities of 
the Company in relation 
to the Global Offering. 
Both SSI and SSIAM 
are ultimately controlled 
by Shanxi Securities 
International Financial 
Holdings (“SSIFH”). 
Accordingly, SSIAM 
is considered as a 
“connected client” of SSI 
pursuant to paragraph 1B 
of the Appendix F1 to the 
Listing Rules.(7)
No
20,000
0.07%
0.01%
3
GTJAS and Haitong 
International 
Securities Company 
Limited (“Haitong”)
Fullgoal Fund 
Management Co., 
Ltd. (“Fullgoal 
Fund”)
GTJAS and Haitong are 
syndicate members 
who place securities 
of the Company in 
relation to the Global 
Offering. Fullgoal 
Fund is a member of 
the same group of 
companies as GTJAS and 
Haitong, respectively. 
Accordingly, Fullgoal 
Fund is considered as 
a “connected client” 
of GTJAS and Haitong 
pursuant to paragraph 1B 
of the Appendix F1 to the 
Listing Rules.(4)
Yes
187,500
0.69%
0.08%

<<<PAGE 20>>>
20
No.
Connected 
Distributor
Connected Client
Relationship
Whether the
Connected Client
is a collective
investment
scheme which
is not authorised
by the SFC or
is expected
to hold the
Offer Shares on
behalf of
such scheme
Number of
Offer Shares
to be 
allocated to 
the Connected
Client
Approximate
percentage 
of total 
number of
Offer Shares
under the
Global 
Offering
Approximate
percentage 
of total 
issued share
capital after
the Global
Offering
4
GTJAS and Haitong
Fullgoal Asset 
Management (HK) 
Limited (“Fullgoal 
HK”)
GTJAS and Haitong are 
syndicate members who 
place securities of the 
Company in relation 
to the Global Offering. 
Fullgoal HK is a member 
of the same group of 
companies as GTJAS and 
Haitong, respectively. 
Accordingly, Fullgoal 
HK is considered as a 
“connected client” of 
GTJAS and Haitong 
pursuant to paragraph 1B 
of the Appendix F1 to the 
Listing Rules.(5)
Yes
210,500
0.78%
0.09%
Notes:
(1) 
Huatai Capital Investment Limited (“HTCI”) is a member of the same group of Huatai Financial Holdings (Hong 
Kong) Limited (“HTFH”).
HTFH is one of the Overall Coordinators, Joint Sponsors, Sponsor-Overall Coordinators, Joint Global 
Coordinators, Joint Bookrunners, Joint Lead Managers and Capital Market Intermediaries in connection with the 
Global Offering. Pursuant to an ISDA Agreement (the “ISDA Agreement”), HTCI, which intends to participate 
in the Global Offering as a placee, will hold the beneficial interest of the H Shares, on a non-discretionary basis 
as the single underlying holder under a back-to-back total return swap (the “Back-to-back TRS”) to be entered 
by HTCI in connection with a Client TRS (as defined below) placed by and fully funded (i.e. with no financing 
provided by HTCI) by the Huatai Ultimate Client (as defined below), by which, HTCI will, subject to customary 
fees and commissions, pass the full economic exposure of the Shares to the Huatai Ultimate Client, which in 
effect, HTCI will hold the beneficial interest of the Shares on behalf of the Huatai Ultimate Client. Accordingly, 
HTCI is considered as a “connected client” of HTFH pursuant to paragraph 1B of the Placing Guidelines.
The offshore investor (the “Huatai Ultimate Client”), through its investment manager, will place a total 
return swap order (the “Client TRS”) with HTCI in connection with the Company’s IPO. In order to hedge its 
exposure under the Client TRS, HTCI participates in the Company’s IPO and subscribes the Shares through 
placing order with HTFH during the International Offering.

<<<PAGE 21>>>
21
The purpose of HTCI to subscribe for the H Shares is for hedging the Client TRS order placed by the Huatai 
Ultimate Client. Pursuant to the terms of the Client TRS, during the tenor of the Client TRS, subject to 
customary fees and commissions, all economic returns of the H Shares will be passed to the Huatai Ultimate 
Client through the Client TRS and all economic loss shall be borne by the Huatai Ultimate Client. HTCI will 
not take any economic return or bear any economic loss in relation to the H Shares.
The Huatai Ultimate Client may exercise an early termination right to terminate the Client TRS at any time 
from the issue date of the Client TRS which should be on or after the date on which the H Shares are listed on 
the Stock Exchange at its own discretion. Upon the termination upon maturity or early termination of the Client 
TRS by the Huatai Ultimate Client, HTCI will dispose the H Shares on the secondary market and the Huatai 
Ultimate Client will receive a final settlement amount of the Client TRS in cash in accordance with the terms 
and conditions of the Client TRS which should have taken into account all the economic returns or economic 
loss in relation to the Shares. If upon the maturity of the Client TRS, the Huatai Ultimate Client intends to 
extend the investment period, subject to further agreement between HTCI and the relevant Huatai Ultimate 
Client, the term of the Client TRS could be extended by way of a new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the H Shares by itself, and pass through 
the economic exposure to the Huatai Ultimate Client, being a client who places a Client TRS order with HTCI 
in connection with the IPO of the Company. HTCI will not exercise the voting right of the H Shares during the 
tenor of the Client TRS.
During the life of the Client TRS, HTCI may continue to hold the H Shares in its custodian account, or to hold 
some or all of the H Shares in a prime brokerage account for stock borrowing purposes, where HTCI will lend 
out its holding of underlying H Shares in the form of stock borrowing loans consistent with market practice to 
lower its finance costs, provided that HTCI has the ability to call back the Shares on loan at any time in order to 
satisfy its obligations under the Client TRS to ensure the economic interests are ultimately passed to the Huatai 
Ultimate Client.
The Huatai Ultimate Client and its respective ultimate beneficial owner holding 30% or more interest include:
Huatai Ultimate Client
UBO with 30% or more interests
PRIME GAIN OFC SUB AC PRIME GAIN FUND II
Wu Bing
The general partner of the Huatai Ultimate Client is Jinluo Securities Limited, whose ultimate beneficial owner 
is Wu Bing.
HTCI has confirmed that, to the best of their knowledge, (i) each of the Huatai Ultimate Client and the ultimate 
beneficial owner holding 30% or more interest of the Huatai Ultimate Client listed above is an independent 
third party of (a) the Company, the connected person or the associates thereof; and (b) HTCI, HTFH and the 
companies which are members of the same group of companies as HTFH, and (ii) HTCI is not a collective 
investment scheme which is not authorised by the SFC nor is expected to hold the Offer Shares on behalf of 
such scheme.

<<<PAGE 22>>>
22
(2) 
CSAM, a qualified domestic institutional investor as approved by the relevant PRC authority to conduct asset 
management business, will hold the Offer Shares as the independent agent and discretionary manager of certain 
QDII funds for each of its funds (the “CSAM Ultimate Clients”).
The CSAM Ultimate Clients and their respective ultimate beneficial owners include:
CSAM Ultimate Clients
UBO with 30% or more interests
China Southern Hong Kong Growth Fund  
(南方香港成長靈活配置混合)
No single UBO with 30% or more interest
China Southern China New Economy 9-Month Holding Period 
Hybrid Fund (QDII) (南方中國新興經濟 9 個月持有期混合
(QDII))
No single UBO with 30% or more interest
China Southern Global Dynamic Allocation Fund  
(南方全球精選配置股票(QDI1-FOF))
No single UBO with 30% or more interest
CSAM has confirmed that, to the best of their knowledge, (i) the CSAM Ultimate Clients and the ultimate 
beneficial owners holding 30% or more interest of the CSAM Ultimate Clients listed above is an independent 
third party of (a) the Company, the connected person or the associates thereof; and (b) CSAM, HTFH and the 
companies which are members of the same group of companies as HTFH, and (ii) CSAM is not a collective 
investment scheme which is not authorised by the SFC nor is expected to hold the Offer Shares on behalf of 
such scheme.
(3) 
It is proposed that GTJAI participates as placee to subscribe for the Offer Shares under the International 
Offering (the “GTJAI Subscription”).
In relation to the GTJAI Subscription, GTJAI shall hold the Offer Shares for hedging purpose as the single 
underlying asset of a back-to-back total return swap transaction (the “GTHT Back-to-back TRS”) to be entered 
into between GTJAI and Guotai Haitong Securities Co., Ltd. (the “GTHT Onshore Parent”) in connection 
with a total return swap order (the “GTHT Client TRS”) to be entered into by GTHT Onshore Parent and 
ultimate client (the “GTHT Onshore Ultimate Client”), respectively. Such GTHT Client TRS is to be fully 
funded by the GTHT Onshore Ultimate Client. GTJAI will hold the Offer Shares on a non-discretionary basis 
for the purpose of hedging the economic exposure under the GTHT Back-to-back TRS and GTHT Client TRS 
only. During the tenor of the GTHT Client TRS, all economic returns of the Offer Shares will be passed to the 
GTHT Onshore Ultimate Client and all economic losses shall be borne by the GTHT Onshore Ultimate Client, 
subject to the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS, and GTJAI will 
not take part in any economic return or bear any economic loss in relation to the price of the Offer Shares. The 
GTHT Onshore Ultimate Client may request to redeem the Offer Shares at their own discretion, upon which 
GTJAI shall dispose of the Offer Shares and settle the GTHT Back-to-back TRS and GTHT Client TRS in cash 
in accordance with the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS documents. 
Due to its internal policy, GTJAI will not exercise the voting right attaching to the Offer Shares during the tenor 
of the GTHT Back-to-back TRS and GTHT Client TRS.
The GTHT Onshore Ultimate Client and their respective ultimate beneficial owners include:
GTHT Onshore Ultimate Client
UBO with 30% or more interests
CICC JINJIA No.1 Collective Asset Management Plan  
(中金金嘉 1 號集合資產管理計劃)
No single UBO with 30% or more interest
The fund manager of the GTHT Onshore Ultimate Clients is China International Capital Corporation Limited (中
國國際金融股份有限公司), whose ultimate controller is the State Council of the PRC, whereas its investment 
managers are Wang Chen (王琛) and Wang Ning (王寧).
GTJAI has confirmed that, to the best of their knowledge, (i) the GTJA Onshore Ultimate Client and the 
ultimate beneficial owners holding 30% or more interest of the GTJA Onshore Ultimate Client listed above is 
an independent third party of (a) the Company, the connected person or the associates thereof; and (b) GTJAI, 
GTJAS and the companies which are members of the same group of companies as GTJAS, and (ii) GTJAI is not 
a collective investment scheme which is not authorised by the SFC nor is expected to hold the Offer Shares on 
behalf of such scheme.

<<<PAGE 23>>>
23
(4) 
It is proposed that Fullgoal Fund participates as placee to subscribe for the Offer Shares under the International 
Offering (the “Fullgoal Subscription”).
In relation to the Fullgoal Subscription, Fullgoal Fund will hold the Offer Shares in its capacity as the 
discretionary fund manager on behalf of its funds (the “Fullgoal Ultimate Clients”).
The Fullgoal Ultimate Clients and their respective ultimate beneficial owners include:
Fullgoal Ultimate Clients
Whether the Fund 
is a Collective 
Investment 
Scheme
Whether the 
Scheme is 
Publicly Marketed
Fund 
Manager
UBO of Fund 
Manager with 
30% or more 
interests
UBO of Fullgoal 
HK Ultimate 
Clients with 30% 
or more interest
ICBC Fullgoal global technology & internet fund  
(ICBC Global Tech)
Yes
Yes
Fullgoal Fund
N/A
No single UBO with 30% or more 
interest
ICBC Fullgoal China Small & Mid Cap (HK listed)  
Equity Fund (ICBC China SMC)
Yes
Yes
Fullgoal Fund
N/A
No single UBO with 30% or more 
interest
Fullgoal Fund has confirmed that, to the best of their knowledge, (i) the Fullgoal Ultimate Clients and the 
ultimate beneficial owners holding 30% or more interest of the Fullgoal Ultimate Clients listed above is an 
independent third party of (a) the Company, the connected person or the associates thereof; and (b) Fullgoal 
Fund, GTJAS, Haitong and the companies which are members of the same group of companies as GTJAS and 
Haitong, respectively, and (ii) each of ICBC Global Tech and ICBC China SMC is a collective investment 
scheme which is not authorised by the SFC.
(5) 
It is proposed that Fullgoal HK participates as placee to subscribe for the Offer Shares under the International 
Offering (the “Fullgoal HK Subscription”).
In relation to the Fullgoal HK Subscription, Fullgoal HK will hold the Offer Shares in its capacity as the 
discretionary fund manager on behalf of its funds (the “Fullgoal HK Ultimate Clients”). Each of FCOF, BMO 
and FCGSF (as defined below) is a collective investment scheme which is not authorised by the SFC, whereas 
FHKCEF (as defined below) is not a collective investment scheme which is not authorised by the SFC nor is 
expected to hold the Offer Shares on behalf of such scheme
Fullgoal HK Ultimate Clients and their respective ultimate beneficial owners include:
Fullgoal HK Ultimate Clients
Whether the 
Fund is a 
Collective 
Investment Scheme
Whether the 
Scheme is 
Publicly Marketed
Fund Manager
UBO of Fund 
Manager with 
30% or more 
interests
UBO of the Fullgoal 
HK Ultimate Clients
Fullgoal China Opportunities Fund (FCOF)
Yes
Not publicly marketed Fullgoal HK
Fullgoal Fund
The ultimate beneficial owners are 
three investors which are entities 
and funds, namely (1) China 
Everbright Fortune Investment 
Limited; (2) L Industries Limited; 
and (3) Orient Sun Rise Fund Series 
SPC – Orient Sun Rise Enhanced 
Balanced Fund Segregated 
Portfolio, each with 30% or more 
interest therein. None of the 
aforesaid entities has a single UBO 
with 30% or more interest.
BMO Greater China Fund (BMO)
Yes
Yes
Fullgoal HK
Fullgoal Fund
No single UBO with 30% or more 
interest.

<<<PAGE 24>>>
24
Fullgoal HK Ultimate Clients
Whether the 
Fund is a 
Collective 
Investment Scheme
Whether the 
Scheme is 
Publicly Marketed
Fund Manager
UBO of Fund 
Manager with 
30% or more 
interests
UBO of the Fullgoal 
HK Ultimate Clients
Fullgoal China Growth Select Fund (FCGSF)
Yes
Not publicly marketed Fullgoal HK
Fullgoal Fund
The ultimate beneficial owner with 
30% or more interest is Zhao Xue 
Ming.
The University of Hong Kong-Hong Kong and China 
Equity Fund (FHKCEF)
No
Not publicly marketed Fullgoal HK
Fullgoal Fund
The ultimate beneficial owner with 
30% or more interest is The 
University of Hong Kong.
Fullgoal HK has confirmed that, to the best of their knowledge, the Fullgoal HK Ultimate Clients and the 
ultimate beneficial owners holding 30% or more interest of the Fullgoal HK Ultimate Clients listed above is 
an independent third party of (a) the Company, the connected person or the associates thereof; and (b) Fullgoal 
HK, GTJAS, Haitong and the companies which are members of the same group of companies as GTJAS and 
Haitong, respectively.
(6) 
It is proposed that CSICM participates as placee to subscribe for the Offer Shares under the International 
Offering (the “CSICM Subscription”).
In relation to the CSICM Subscription, CSICM will act as the single counterparty of several back-to-back total 
return swap transactions (the “CSICM Back-to-back TRS”) to be entered into by it in connection with total 
return swap orders (the “CSICM Client TRS”) placed and fully funded by its investors (the “CSICM Ultimate 
Clients”), by which CSICM will pass the full economic exposure of the Offer Shares placed to the CSICM 
Ultimate Clients. As confirmed by CSICM, CSICM will hold the legal title and beneficial interest in the Offer 
Shares, but will contractually agree to pass on the full economic exposure and return of the Offer Shares to the 
CSICM Ultimate Clients, on a non-discretionary basis. The CSICM Ultimate Clients may exercise their early 
termination rights to terminate the CSICM Client TRS at any time from the trade date of the CSICM Client TRS 
which should be on or after the date on which the Offer Shares are listed on the Stock Exchange. Upon the final 
maturity or termination of the CSICM Client TRS by the CSICM Ultimate Clients, CSICM will dispose of the 
Offer Shares on the secondary market and the CSICM Ultimate Clients will receive a final termination amount 
of the CSICM Back-to-back TRS which will have taken into account all the economic returns or economic loss 
in relation to the Offer Shares and the fixed amount of transaction fees of the CSICM Back-to-back TRS and 
the CSICM Client TRS. Due to its internal policy, CSICM will not exercise the voting right of the Offer Shares 
during the terms of the CSICM Back-to-back TRS.
The CSICM Ultimate Clients and their respective ultimate beneficial owners include:
CSICM Ultimate Clients
UBO with 30% or more interests
LW Investment II
Xu Chong
LW Investment III
N/A
The general partner of the LW Investment II and LW Investment III are Red Dot Asset Management Pte. Ltd., 
whose ultimate beneficial owners are Chan Hock Eng and Xie Dahong.
CSICM has confirmed that, to the best of their knowledge, (i) the CSICM Ultimate Clients and the ultimate 
beneficial owners holding 30% or more interest of the CSICM Ultimate Clients listed above is an independent 
third party of CSICM, CSB and the companies which are members of the same group of companies as CSB, and 
(ii) CSICM is not a collective investment scheme which is not authorised by the SFC nor is expected to hold the 
Offer Shares on behalf of such scheme.

<<<PAGE 25>>>
25
(7) 
It is proposed that SSIAM participates as placee to subscribe for the Offer Shares under the International 
Offering (the “SSIAM Subscription”).
In relation to the SSIAM Subscription, SSIAM will hold the Offer Shares in its capacity as the discretionary 
fund manager on behalf of its investors.
The ultimate client of SSIAM is Chen Jun (陳俊), who is also the ultimate beneficial owner of SSIAM with 
30% or more interest therein.
SSIAM has confirmed that, to the best of their knowledge, (i) the ultimate client of SSIAM and the ultimate 
beneficial owner holding 30% or more interest of the ultimate client of SSIAM listed above is an independent 
third party of (a) the Company, the connected person or the associates thereof; and (b) SSIAM, SSI, SSIFH and 
the companies which are members of the same group of companies as SSIFH, and (ii) SSIAM is not a collective 
investment scheme which is not authorised by the SFC nor is expected to hold the Offer Shares on behalf of 
such scheme.
(8) 
It is proposed that VIL participates as placee to subscribe for the Offer Shares under the International Offering 
(the “VIL Subscription”).
In relation to the VIL Subscription, VIL and its investor, who is also the ultimate beneficial owner (the “VIL 
Ultimate Client”), have entered into a series of cross border over-the-counter swap transactions (collectively, 
the “VIL Client TRS”) with each other pursuant to which VIL will hold the Offer Shares on a non-discretionary 
basis to hedge the VIL Client TRS while the economic risks and returns of the underlying Offer Shares are 
passed to the VIL Ultimate Client, subject to customary fees and commission.
The VIL Ultimate Client and ultimate beneficial owner are Guo Jing, who holds 30% or more interest therein.
VIL has confirmed that, to the best of their knowledge, (i) the VIL Ultimate Client and the ultimate beneficial 
owner holding 30% or more interest of the VIL Ultimate Client listed above is an independent third party of (a) 
the Company, the connected person or the associates thereof; and (b) VCL, VIL and the companies which are 
members of the same group of companies as VCL, and (ii) VIL is not a collective investment scheme which is 
not authorised by the SFC nor is expected to hold the Offer Shares on behalf of such scheme.

<<<PAGE 26>>>
26
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) 
and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities 
in the United States or in any other jurisdictions. The securities mentioned herein have not been, and will not be, 
registered under the United States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or 
securities law of any state or other jurisdiction of the United States. The securities may not be offered, sold, pledged 
or otherwise transferred within the United States except pursuant to an exemption from the registration requirements 
of the U.S. Securities Act and in compliance with any applicable state securities laws. The securities are being offered 
and sold outside the United States in offshore transactions in accordance with Regulation S under the U.S. Securities 
Act. There will be no public offer of securities in the United States.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
April 27, 2026 (the “Prospectus”) issued by Cofoe Medical Technology Co., Ltd. (可孚醫療科技股份有限公司) (the 
“Company”) for detailed information about the Global Offering described below before deciding whether or not to 
invest in the H Shares thereby being offered. Any investment decision in relation to the Offer Shares should be taken 
solely in reliance on the information in the Prospectus. The Company has not been and will not be registered under the 
U.S. Investment Company Act of 1940, as amended.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinators (for themselves and on behalf 
of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting 
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
Wednesday, May 6, 2026).

<<<PAGE 27>>>
27
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, the total number of the 27,000,000 
H Shares expected to be held by the public represents approximately 11.67% of the total issued 
share capital of our Company (excluding 4,496,131 A Shares repurchased by our Company 
as treasury shares as of the date of this announcement), which is higher than the prescribed 
percentage of H Shares required to be held in public hands of 10.00% under Rule 19A.13A(2)(a) of 
the Listing Rules. Based on the above, it is expected that our Company will satisfy the public float 
requirements as required under Rule 19A.13A(2) of the Listing Rules.
Considering that the final Offer Price is fixed at the Offer Price of HK$39.33 per Offer Share, save 
for 9,654,300 H Shares (representing approximately 4.17% of our total issued Shares immediately 
upon completion of the Global Offering, excluding 4,496,131 A Shares repurchased by our 
Company as treasury shares as of the date of this announcement) to be issued to the cornerstone 
investors that are subject to disposal restrictions for a period of six months from the Listing Date, 
the remaining 17,345,700 H Shares, representing approximately 7.50% of the total issued share 
capital of our Company (excluding 4,496,131 A Shares repurchased by our Company as treasury 
shares as of the date of this announcement), with an expected market value of approximately 
HK$682 million, which is higher than HK$600 million under Rule 19A.13C of the Listing 
Rules, will not be subject to any disposal restrictions (whether under contract, the Listing Rules, 
applicable laws or otherwise) at the time of the Listing. Our Company will satisfy the free float 
requirement under Rule 19A.13C of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public shareholders of 
the Company do not hold more than 50% of the H shares in public hands at the time of the Listing 
in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 
Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.

<<<PAGE 28>>>
28
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, May 
6, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting – Underwriting Arrangements 
and Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade the H Shares on the basis of publicly available allocation 
details prior to the receipt of H Share certificates or prior to the H Share certificates becoming 
valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Wednesday, 
May 6, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Wednesday, May 6, 2026 (Hong Kong time). The H Shares will be 
traded in board lots of 100 H Shares each, and the stock code of the H Shares will be 1187.
By order of the Board
Cofoe Medical Technology Co., Ltd.
Mr. ZHANG Min
Executive Director and Chairman of the Board
Hong Kong, May 5, 2026
As of the date of this announcement, the board of directors of the Company comprises: (i) Mr. 
ZHANG Min, Mr. ZHANG Zhiming, Mr. XUE Xiaoqiao and Mr. HE Bangjie as executive 
directors; and (ii) Mr. NING Huabo, Ms. SHEN Nan and Mr. Zhou Rong as independent non-
executive directors.
