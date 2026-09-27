# 配发结果公告抽取任务：2261.HK NASN Intelligent Tech (Zhejiang) Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**06/08/2026 22:07**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0806/2026080602047.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2261.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for 
the contents of this announcement, make no representation as to its accuracy or completeness and expressly 
disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings 
as those defined in the prospectus dated July 30, 2026 (the “Prospectus”) issued by NASN Intelligent Tech 
(Zhejiang) Co., Ltd. (拿森智能科技(浙江)股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities of the Company. This announcement is not a prospectus. Potential 
investors should read the Prospectus for detailed information about the Company and the Global Offering 
described below before deciding whether or not to invest in the Offer Shares. Any investment decision in 
relation to the Offer Shares should be taken solely in reliance on the information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not, and is not intended to, constitute or form a part of any offer to sell or 
solicitation to purchase or subscribe for any securities in the United States or in any other jurisdiction. The 
Offer Shares have not been, and will not be, registered under the U.S. Securities Act of 1933, as amended 
from time to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the 
United States and may not be offered, sold, pledged or otherwise transferred within the United States, except 
pursuant to an available exemption from, or in a transaction not subject to, the registration requirements of 
the U.S. Securities Act and in compliance with any applicable state securities laws. There will be no public 
offer of the Offer Shares in the United States. The Offer Shares are being offered and sold solely outside the 
United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act.
It is anticipated that no stabilization activities will be carried out by the Stabilizing Manager in relation to 
the Global Offering.
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and 
on behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date.

<<<PAGE 2>>>
– 2 –
NASN Intelligent Tech (Zhejiang) Co., Ltd.
拿森智能科技（浙江）股份有限公司
(a joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under 
the Global Offering
:
57,594,500 H Shares
Number of Hong Kong Offer Shares
:
5,759,500 H Shares
Number of International Offer Shares
:
51,835,000 H Shares
Final Offer Price
:
HK$10.42 per H Share plus brokerage 
of 1.0%, SFC transaction levy of 
0.0027%, Hong Kong Stock Exchange 
trading fee of 0.00565% and AFRC 
transaction levy of 0.00015% (payable 
in full on application in Hong Kong 
dollars and subject to refund)
Nominal value
:
RMB0.0625 per H Share
Stock code
:
2261
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers
Joint Lead Manager

<<<PAGE 3>>>
 
NASN Intelligent Tech (Zhejiang) Co., Ltd. 
拿森智能科技（浙江）股份有限公司 
ANNOUNCEMENT OF ALLOTMENT RESULTS 
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings 
as those defined in the prospectus dated July 30, 2026 (the “Prospectus”) issued by NASN Intelligent Tech 
(Zhejiang) Co., Ltd. (the “Company”).  
 
Warning: In view of high concentration of shareholding in a small number of H Shareholders, H 
Shareholders and prospective investors should be aware that the price of the H Shares could move 
substantially even with a small number of H Shares traded and should exercise extreme caution when 
dealing in the H Shares. 
 
SUMMARY  
 
Company information 
Stock code  
2261
Stock short name  
NASN TECH
Dealings commencement date  
August 7, 2026*
*see note at the end of the announcement  
 
Price Information  
Final Offer Price  
HK$10.42
 
Offer Shares and Share Capital 
Number of Offer Shares  
57,594,500
Number of Offer Shares in the Hong Kong Public Offering 
5,759,500
Number of Offer Shares in International Offering 
51,835,000
Number of issued shares upon Listing 
594,984,292
 
Over-allocation 
No. of Offer Shares over-allocated  
0
 
The Overall Coordinators have confirmed that there has been no over-allocation of the Offer Shares in the 
International Offering. Therefore, it is expected that the Over-allotment Option will not be exercised. 
 
Proceeds
Gross proceeds (Note) 
HK$ 600.1 million
Less: Estimated listing expenses payable based on Final 
Offer Price  
HK$ (66.9) million 
Net proceeds  
HK$ 533.2 million
 
Note: Gross proceeds refer to the amount to which the Company is entitled to receive. For details of the use 
of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” in the Prospectus.  
 
ALLOTMENT RESULTS DETAILS 
3

<<<PAGE 4>>>
 
HONG KONG PUBLIC OFFERING  
 
No. of valid applications  
161,125
No. of successful applications  
40,339
Subscription level  
2,513.54 times
No. of Offer Shares initially available under the Hong Kong Public 
Offering 
5,759,500  
Final no. of Offer Shares under the Hong Kong Public Offering 
5,759,500
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering 
10% 
 
Note: For details of the final allocation of Offer Shares to the Hong Kong Public Offering, investors can 
refer to https://www.hkeipo.hk/IPOResult to perform a search by identification number or 
https://www.hkeipo.hk/IPOResult  for the full list of allottees. 
 
INTERNATIONAL OFFERING  
 
No. of placees  
133
Subscription level  
2.12 times
No. of Offer Shares initially available under the International 
Offering  
51,835,000  
Final no. of Offer Shares under the International Offering  
51,835,000
% of Offer Shares under the International Offering to the Global 
Offering 
90% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for a waiver from strict 
compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) of Appendix F1 to the 
Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange to permit the Company to allocate 
Offer Shares to a close associate of an existing shareholder, (i) none of the Offer Shares subscribed by the 
placees and the public have been financed directly or indirectly by the Company, any of the Directors, 
Supervisors, chief executive of the Company, substantial Shareholders, existing Shareholders of the Company 
or any of its subsidiaries or their respective close associates; and (ii) none of the placees and the public who 
have purchased the Offer Shares are accustomed to taking instructions from the Company, any of the Directors, 
Supervisors, chief executive of the Company, substantial Shareholders, existing Shareholders of the Company 
or any of its subsidiaries or their respective close associates in relation to the acquisition, disposal, voting or 
other disposition of H Shares registered in his/her/its name or otherwise held by him/her/it.  
 
The placees in the International Offering include the following: 
Allottees with waivers/consents obtained 
4

<<<PAGE 5>>>
 
 
Investor 
No. of 
Offer 
Shares 
allocated 
% of total 
number of 
Offer Shares 
under the 
Global 
Offering(1) 
% of total 
issued share 
capital after the 
Global Offering (1) 
Relationship 
Allottee with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to allocation to a close associate of an existing 
Shareholder (2)  
DeepStudy Limited
(“DeepStudy”) 
4,798,400
8.33%
0.81%
A close associate of 
an existing 
Shareholder
Allottee with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocation to a connected client (3) 
Orient Asset 
Management (Hong 
Kong) Limited 
(“Orient AM”)
9,000
0.02%
0.0015%
Connected client as a 
placee
 
Notes: 
 
(1) The Over-allotment Option has not been exercised and will not be exercised. 
 
(2) For details of the waiver from strict compliance with Rule 10.04 of the Listing Rules and consent 
under paragraph 1C(2) of the Placing Guidelines in relation to the allocation of Offer Shares 
to DeepStudy, please refer to the section headed “Others/Additional Information — Placing to 
a close associate of an existing Shareholder with a waiver from the strict compliance with Rule 
10.04 of the Listing Rules and a prior consent under paragraph 1C(2) of the Placing 
Guidelines” in this announcement. 
 
(3) For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 
of the Guide for New Listing Applicants in relation to allocation of Offer Shares to Orient AM, 
please refer to the section headed “Others/Additional Information – Placing to a connected 
client with a prior consent under paragraph 1C(1) of the Placing Guidelines” in this 
announcement. 
 
 
LOCK-UP UNDERTAKINGS  
Existing Shareholders 
 Name 
Number of H 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing 
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing  (1) 
% of total 
issued share 
capital after the 
Global Offering 
subject to lock-
up undertakings 
upon Listing (1) 
Last day subject 
to the lock-up 
undertakings 
Mr. Tao Zhe (“Mr. Tao”) (1)
83,869,328 
14.10% 
14.10% 
August 6, 2027 
(2)(3)
5

<<<PAGE 6>>>
 
 Name 
Number of H 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing 
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing  (1) 
% of total 
issued share 
capital after the 
Global Offering 
subject to lock-
up undertakings 
upon Listing (1) 
Last day subject 
to the lock-up 
undertakings 
Ms. Liu Qian (“Ms. Liu”) 
(1)
1,552,000 
0.26% 
0.26% 
August 6, 2027 
(2)(3)
Shanghai NASN Enterprise 
Management Partnership 
(Limited Partnership) 
(“NASN LP”) (1)
35,920,000 
6.04% 
6.04% 
August 6, 2027 (2)
Subtotal 
121,341,328  
20.39% 
20.39% 
Notes: 
 
(1) As of the date of this announcement, Mr. Tao acted as the general partner of NASN LP, and 
Shanghai Nazhi Business Consulting Partnership (Limited Partnership), Shanghai Naheng 
Business Consulting Partnership (Limited Partnership), Shanghai Narui Business Consulting 
Partnership (Limited Partnership) and Shanghai Nachen Business Consulting Partnership 
(Limited Partnership), the four limited partners of NASN LP. Mr. Tao and Ms. Liu are spouses. 
As such, Mr. Tao, Ms. Liu, NASN LP, Shanghai Nazhi, Shanghai Naheng, Shanghai Narui and 
Shanghai Nachen constitute the Single Largest Group of Shareholders. 
 
(2) Pursuant to PRC Company Law, the Shares held by all existing Shareholders (including the Pre-
IPO Investors) are subject to a lock-up period of 12 months after the Listing Date.  
 
(3) Each of Mr. Tao and Ms. Liu has given a lock-up undertaking pursuant to the Hong Kong 
Underwriting Agreement. For details, please refer to the section headed “Underwriting — 
Underwriting Arrangements and Expenses — Hong Kong Public Offering — Undertakings 
Pursuant to the Hong Kong Underwriting Agreement” in the Prospectus. 
 
 
 
Other Existing Shareholders  
Name 
Number of H 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing 
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing (1) 
% of total 
issued share 
capital after the 
Global Offering 
subject to lock-
up undertakings 
upon Listing (1) 
Last day subject 
to the lock-up 
undertakings 
Mr. Wang Jianming
60,240,880
10.12%
10.12%
August 6, 2027 (2)
Hangzhou Chuangqian 
Investment Partnership 
(Limited 
Partnership)
38,841,232 
6.53% 
6.53% 
August 6, 2027 (2)
Shanghai Yangtze River 
Delta BOC Capital Equity
35,636,816 
5.99% 
5.99% 
August 6, 2027 (2)
6

<<<PAGE 7>>>
 
Name 
Number of H 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing 
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing (1) 
% of total 
issued share 
capital after the 
Global Offering 
subject to lock-
up undertakings 
upon Listing (1) 
Last day subject 
to the lock-up 
undertakings 
Investment Fund 
Partnership (Limited 
Partnership)
Future Industry Investment 
Fund II (Limited 
Partnership)
33,623,296 
5.65% 
5.65% 
August 6, 2027 (2)
Suzhou Industrial Park 
Qiming Rongke Equity 
Investment Partnership 
(Limited Partnership)
32,400,016 
5.45% 
5.45% 
August 6, 2027 (2)
Chengdu Juli Zhongchan 
Equity Investment Fund 
Partnership (Limited 
Partnership)
17,587,952 
2.96% 
2.96% 
August 6, 2027 (2)
Hangzhou Juli No. 1 Equity 
Investment Partnership 
(Limited Partnership) 
7,961,328 
1.34% 
1.34% 
August 6, 2027 (2)
Juli Hangshi (Hangzhou) 
Equity Investment 
Partnership (Limited 
Partnership)
5,307,552 
0.89% 
0.89% 
August 6, 2027 (2)
Suzhou Sushang United 
Venture Capital Partnership 
(Limited Partnership)
25,098,992 
4.22% 
4.22% 
August 6, 2027 (2)
Ningbo Meishan Bonded 
Port Zone Wending 
Investment Co., Ltd.
21,378,784 
3.59% 
3.59% 
August 6, 2027 (2)
VNTR VI HK Holdings 
Limited
11,731,760 
1.97% 
1.97% 
August 6, 2027 (2)
MAUT IV HK Holdings 
Limited
7,821,184 
1.31% 
1.31% 
August 6, 2027 (2)
Ms. Hou Jiaqiao
17,817,408
2.99%
2.99%
August 6, 2027 (2)
Jiaxing Yunsen Equity 
Investment Partnership 
(Limited Partnership)
17,587,952 
2.96% 
2.96% 
August 6, 2027 (2)
Chongqing Changxin Zhiqi 
Private Equity Investment 
Fund Partnership (Limited 
Partnership)
13,676,224 
2.30% 
2.30% 
August 6, 2027 (2)
Sunpeak Asset Holdings 
(Hong Kong) Limited
13,036,768 
2.19% 
2.19% 
August 6, 2027 (2)
QM103 LIMITED
12,882,432
2.17%
2.17%
August 6, 2027 (2)
Suzhou Maison Zhiyuan 
Venture Capital Enterprise 
(Limited Partnership)
11,594,192 
1.95% 
1.95% 
August 6, 2027 (2)
7

<<<PAGE 8>>>
 
Name 
Number of H 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing 
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing (1) 
% of total 
issued share 
capital after the 
Global Offering 
subject to lock-
up undertakings 
upon Listing (1) 
Last day subject 
to the lock-up 
undertakings 
Shanghai Nasheng Business 
Consulting Partnership 
(Limited Partnership)
11,487,360 
1.93% 
1.93% 
August 6, 2027 (2)
Chongqing Kexing Sci-
Tech Innovation Equity  
Investment Fund 
Partnership (Limited 
Partnership)
5,276,384 
0.89% 
0.89% 
August 6, 2027 (2)
Shangrong Baoying 
(Ningbo) Investment Center 
(Limited Partnership)
1,675,104 
0.28% 
0.28% 
August 6, 2027 (2)
Shangrong Juxin (Ningbo) 
Venture Capital Center 
(Limited Partnership)
2,078,448 
0.35% 
0.35% 
August 6, 2027 (2)
Shanghai Shangrong Juyuan 
Equity Investment Center  
(Limited Partnership)
1,288,240 
0.22% 
0.22% 
August 6, 2027 (2)
Dongguan Qinhe Venture 
Capital Center (Limited 
Partnership)
4,832,832 
0.81% 
0.81% 
August 6, 2027 (2)
Chengdu Qigao Zhihe 
Venture Capital Partnership 
(Limited Partnership)
4,156,912 
0.70% 
0.70% 
August 6, 2027 (2)
Jiaxing Nasien Venture 
Capital Partnership (Limited 
Partnership)
1,028,416 
0.17% 
0.17% 
August 6, 2027 (2)
Subtotal 
416,048,464 
69.93% 
69.93% 
Notes: 
 
(1) The number of total issued H Shares immediately after the Global Offering is the same as the 
total number of issued shares of the Company after the Global Offering. 
 
(2) Pursuant to PRC Company Law, the Shares held by all existing Shareholders (including the Pre-
IPO Investors) are subject to a lock-up period of 12 months after the Listing Date. 
 
8

<<<PAGE 9>>>
 
PLACEE CONCENTRATION ANALYSIS  
Placees* 
Number of H Shares allotted 
Allotment as % of International 
Offering 
Allotment as % of total Offer Shares
Number of
H Shares held upon Listing
% of total issued share capital upon Listing
Top 1 
19,193,800
37.03%
33.33%
19,193,800
3.23%
Top 5 
46,009,200
88.76%
79.88%
47,037,616
7.91%
Top 10 
51,782,200
99.90%
89.91%
52,810,616
8.88%
Top 25 
51,822,000
99.97%
89.98%
52,850,416
8.88%
 
Note 
* Ranking of placees is based on the number of H Shares allotted to the placees. 
 # Among the top 25 placees, one of the placees, DeepStudy, is also a close associate of an existing Shareholder. To the best knowledge, information and belief of the Company after due 
enquiry, details of the allocations to DeepStudy have been disclosed in this announcement. Please refer to the section headed “Allottees with Waivers/ Consents Obtained – Allottee with 
waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the Placing Guidelines in relation to allocation to a close associate of an 
existing Shareholder” in this announcement. 
 
H SHAREHOLDERS CONCENTRATION ANALYSIS  
H Shareholders* 
Number of H Shares allotted 
Allotment as % of International 
Offering 
Allotment as % of total Offer Shares
Number of
H Shares held upon Listing
% of total issued share capital upon Listing
Top 1 
0
0.00%
0.00% 
121,341,328 
20.39%
Top 5 
0
0.00%
0.00% 
304,505,040 
51.18%
Top 10 
0
0.00%
0.00% 
436,559,072 
73.37%
Top 25 
50,807,600
98.02%
88.22% 
584,040,480 
98.16%
Note  
9

<<<PAGE 10>>>
 
* Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing. 
 
SHAREHOLDERS CONCENTRATION ANALYSIS  
Shareholders* 
Number of H Shares allotted 
Allotment as % of International 
Offering 
Allotment as % of total Offer Shares
Number of
H Shares held upon Listing
% of total issued share capital upon Listing
Top 1 
0
0.00% 
0.00%
121,341,328 
20.39%
Top 5 
0
0.00% 
0.00%
304,505,040 
51.18%
Top 10 
0
0.00% 
0.00%
436,559,072 
73.37%
Top 25 
50,807,600
98.02% 
88.22%
584,040,480 
98.16%
Note  
* Ranking of Shareholders is based on the number of Shares held by the Shareholders upon Listing. 
10

<<<PAGE 11>>>
 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING  
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:  
 
NO. OF H SHARES APPLIED 
FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF 
ALLOTMENT/BALLOT 
APPROXIMATE % 
ALLOTTED OF THE TOTAL 
NO. OF H SHARES APPLIED 
FOR  
 
POOL A 
 
100
40,644 
3,252 
out 
of 
40,644 
applicants to receive 100 H 
Shares 
8.00% 
200
3,245 
313 out of 3,245 applicants to 
receive 100 H Shares
4.82% 
300
16,882 
1,811 
out 
of 
16,882 
applicants to receive 100 H 
Shares 
3.58%
400
4,652 
539 out of 4,652 applicants to 
receive 100 H Shares
2.90% 
500
3,875 
477 out of 3,875 applicants to 
receive 100 H Shares
2.46% 
600
1,724 
223 out of 1,724 applicants to 
receive 100 H Shares
2.16%
700
1,778 
240 out of 1,778 applicants to 
receive 100 H Shares
1.93%
800
4,510 
629 out of 4,510 applicants to 
receive 100 H Shares
1.74%
900
2,839 
409 out of 2,839 applicants to 
receive 100 H Shares
1.60%
1,000
9,626 
1,424 out of 9,626 applicants 
to receive 100 H Shares 
1.48%
1,500
5,562 
917 out of 5,562 applicants to 
receive 100 H Shares
1.10%
2,000
4,180 
744 out of 4,180 applicants to 
receive 100 H Shares
0.89%
2,500
2,863 
541 out of 2,863 applicants to 
receive 100 H Shares
0.76%
3,000
2,703 
537 out of 2,703 applicants to 
receive 100 H Shares
0.66%
3,500
3,013 
623 out of 3,013 applicants to 
receive 100 H Shares
0.59%
4,000
3,384 
725 out of 3,384 applicants to 
receive 100 H Shares
0.54%
4,500
1,420 
314 out of 1,420 applicants to 
receive 100 H Shares
0.49%
5,000
2,491 
567 out of 2,491 applicants to 
receive 100 H Shares
0.46%
6,000
1,471 
351 out of 1,471 applicants to 
receive 100 H Shares
0.40%
7,000
1,237 
308 out of 1,237 applicants to 
receive 100 H Shares
0.36%
8,000
2,167 
559 out of 2,167 applicants to 
receive 100 H Shares
0.32%
9,000
1,199 
319 out of 1,199 applicants to 
0.30%
11

<<<PAGE 12>>>
 
 
receive 100 H Shares
10,000
5,597 
1,531 out of 5,597 applicants 
to receive 100 H Shares 
0.27%
20,000
2,890 
951 out of 2,890 applicants to 
receive 100 H Shares
0.16%
30,000
2,073 
761 out of 2,073 applicants to 
receive 100 H Shares
0.12%
40,000
1,755 
695 out of 1,755 applicants to 
receive 100 H Shares
0.10%
50,000
1,523 
640 out of 1,523 applicants to 
receive 100 H Shares
0.08%
60,000
816 
360 out of 816 applicants to 
receive 100 H Shares
0.07%
70,000
637 
293 out of 637 applicants to 
receive 100 H Shares
0.07%
80,000
738 
352 out of 738 applicants to 
receive 100 H Shares
0.06%
90,000
721 
355 out of 721 applicants to 
receive 100 H Shares
0.05%
100,000
3,677 
1,860 out of 3,677 applicants 
to receive 100 H Shares 
0.05%
200,000
2,799 
1,703 out of 2,799 applicants 
to receive 100 H Shares 
0.03%
300,000
1,988 
1,348 out of 1,988 applicants 
to receive 100 H Shares 
0.02%
400,000
2,905 
2,127 out of 2,905 applicants 
to receive 100 H Shares 
0.02%
Total
149,584
Total number of Pool A 
successful applicants: 28,798
 
 
POOL B 
500,000
3,884 
200 H Shares
0.04%
600,000
1,716 
200 H Shares plus 267 out of 
1,716 applicants to receive an 
additional 100 H Shares 
0.04%
700,000
938 
200 H Shares plus 278 out of 
938 applicants to receive an 
additional 100 H Shares 
0.03%
800,000
719 
200 H Shares plus 306 out of 
719 applicants to receive an 
additional 100 H Shares 
0.03%
900,000
527 
200 H Shares plus 288 out of 
527 applicants to receive an 
additional 100 H Shares 
0.03%
1,000,000
2,064 
200 H Shares plus 1,357 out 
of 2,064 applicants to receive 
an additional 100 H Shares 
0.03%
2,000,000
589 
300 H Shares plus 313 out of 
589 applicants to receive an 
additional 100 H Shares 
0.02%
2,879,700
1,104 
400 H Shares plus 109 out of 
1,104 applicants to receive an 
additional 100 H Shares 
0.01%
Total 
11,541
Total number of Pool B
successful applicants: 11,541
 
 
12

<<<PAGE 13>>>
 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries. 
  
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.  
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the 
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by 
them was the same as the final Offer Price in addition to any brokerage, the SFC transaction levy, the 
Hong Kong Stock Exchange trading fee and the AFRC transaction levy payable. 
 
OTHERS/ADDITIONAL INFORMATION 
Placing to a close associate of an existing Shareholder with a waiver from the strict compliance 
with Rule 10.04 of the Listing Rules and a prior consent under paragraph 1C(2) of the Placing 
Guidelines 
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a waiver 
from the strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) 
of the Placing Guidelines to permit the Company to allocate Offer Shares in the International Offering 
to DeepStudy, a close associate of an existing Shareholder, Jiaxing Nasien Venture Capital Partnership 
(Limited Partnership) (“Jiaxing Nasien”). The allocation of Offer Shares to DeepStudy is in 
compliance with all the conditions under the waiver/consent granted by the Stock Exchange, including 
but not limited to: 
(i) 
Jiaxing Nasien is interested in less than 5% of the voting rights of the Company before 
the Global Offering; 
 
(ii) 
Jiaxing Nasien is not, and will not become, a core connected person (as defined in the 
Listing Rules) of the Company or a close associate of any such core connected person 
upon completion of the Global Offering; 
 
(iii) 
Jiaxing Nasien does not have the right to appoint Directors or any other special rights in 
the Company which would influence the allocation process; 
 
(iv) 
each of the Company, the Joint Sponsors and the Overall Coordinators confirming that 
no preferential treatment is given to DeepStudy by virtue of it being a close associate of 
an existing Shareholder of the Company; and 
 
(v) 
allocation of Offer Shares to DeepStudy will not affect the Company's ability to satisfy 
the public float requirement under Rule 8.08(1) of the Listing Rules (as amended and 
replaced by Rule 19A.13A of the Listing Rules). 
 
13

<<<PAGE 14>>>
 
 
For details of the allocation of Offer Shares to DeepStudy, please refer to the section headed 
“Allotment Results Details — International Offering — Allottees with waivers/consents obtained” in 
this announcement.  
Placing to a connected client with a prior consent under paragraph 1C(1) of the Placing 
Guidelines  
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a consent 
under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate Offer Shares in 
the International Offering to Orient AM, a connected client. The allocation of Offer Shares to Orient 
AM is in compliance with all the conditions under the consent granted by the Stock Exchange. Details 
of the placement to Orient AM are set out below: 
14

<<<PAGE 15>>>
 
 
 
Connected 
Distributor 
Connected 
Client 
Relationship 
Whether the 
connected 
client 
will 
hold 
the 
beneficial 
interests 
of 
the 
Offer 
Shares on a 
non-
discretionary 
basis 
or 
discretionary 
basis 
for 
independent 
third parties 
Number 
of 
Offer Shares 
to be allocated 
to 
the 
Connected 
Client as a 
placee under 
the 
International 
Offering  
Approximate  % 
of total number 
of Offer Shares 
under the Global 
Offering  
Approximate % 
of total issued 
H Shares 
immediately 
following the 
completion of 
the Global 
Offering  
% of total 
issued share 
capital 
immediately 
following the 
completion 
of the Global 
Offering  
Orient 
Securities 
(Hong Kong) 
Limited 
(“Orient 
Securities”) 
(1) 
Orient AM 
Orient AM is 
a member of 
the same 
group of 
companies as 
Orient 
Securities 
Discretionary 
basis 
 
 
9,000 
0.02% 
0.0015% 
0.0015% 
 
Note: 
(1) Orient AM will hold the Offer Shares in its capacity as the discretionary fund manager on behalf of its underlying clients. Both Orient 
AM and Orient Securities are wholly-owned subsidiaries of Orient Securities International Financial Group Limited. Therefore, Orient 
AM is a member of the same group of companies as Orient Securities. Each of the underlying clients of Orient AM is an independent 
third party of the Company, its subsidiaries, its substantial shareholders, Orient AM, Orient Securities and the companies which are 
members of the same group of companies as Orient Securities.  
 
Orient AM is investing on behalf of certain collective investment schemes which are not authorized by the SFC, details of which are as 
15

<<<PAGE 16>>>
 
 
follows: 
 
Fund name 
Types and values of 
assets 
under 
management 
Whether the scheme 
is publicly marketed 
Scheme 
establishment date 
Identities 
of 
the 
general 
partners 
and the 20 largest 
limited partners of 
the scheme where 
applicable
Identity of the scheme 
administrator 
Orient 
Asset 
Mgt 
(HK) 
Ltd-OSR 
Global Macro Value 
Selective 
(“OSR 
Global 
Macro 
Value Selective”)
Discretionary 
account, 
US$10 
million 
 
No 
February 6, 2025 
Not applicable as it is 
not in partnership 
structure and does 
not have any general 
partner 
or 
limited 
partner
Agricultural Bank of 
China, Hong Kong 
Branch 
Orient 
Asset 
Mgt 
(HK) 
Ltd-OSR 
Selective 
No.4 
(“OSR 
Selective 
No.4”) 
Discretionary 
account, 
US$30 
million  
No 
August 22, 2024 
Not applicable as it is 
not in partnership 
structure and does 
not have any general 
partner 
or 
limited 
partner
Agricultural Bank of 
China, Hong Kong 
Branch 
ORIENT SUN RISE 
FUND SERIES SPC-
ORIENT SUN RISE 
OVERSEAS 
STABLE 
FUND 
SEGREGATED 
PORTFOLIO 
(“Orient Sun Rise 
Overseas 
Stable 
Fund 
Segregated 
Portfolio”)
Private fund, US$5 
million  
No 
November 18, 2025 
Not applicable as it is 
not in partnership 
structure and does 
not have any general 
partner 
or 
limited 
partner 
Agricultural Bank of 
China, Hong Kong 
Branch 
 
No ultimate beneficial owner holds 30% or more interest in Orient Sun Rise Overseas Stable Fund Segregated Portfolio. Each of OSR 
Global Macro Value Selective and OSR Selective No.4 is wholly-owned by individual investors, who are independent third parties. 
 
16

<<<PAGE 17>>>
 
 
DISCLAIMERS 
  
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong 
Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement. 
 
This announcement is not for release, publication, distribution, directly or indirectly, in or into the 
United States (including its territories and possessions, any state of the United States and the 
District of Columbia). This announcement does not, and is not intended to, constitute or form a part 
of any offer to sell or solicitation to purchase or subscribe for any securities in the United States or 
in any other jurisdiction. The Offer Shares have not been, and will not be, registered under the U.S. 
Securities Act of 1933, as amended from time to time (the “U.S. Securities Act”) or securities law 
of any state or other jurisdiction of the United States and may not be offered, sold, pledged or 
otherwise transferred within the United States, except pursuant to an available exemption from, or 
in a transaction not subject to, the registration requirements of the U.S. Securities Act and in 
compliance with any applicable state securities laws. There will be no public offer of the Offer 
Shares in the United States.  
 
The Offer Shares are being offered and sold solely outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to 
acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated July 30, 2026 issued by NASN Intelligent Tech (Zhejiang) 
Co., Ltd. for detailed information about the Global Offering described above before deciding whether 
or not to invest in the H Shares thereby being offered.  
* Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on 
behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds 
for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date. 
 
 
 
17

<<<PAGE 18>>>
– 18 –
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, based on the final Offer 
Price of HK$10.42 per Offer Share, the expected market capitalization upon the Listing 
is HK$6,199.7 million, and the minimum prescribed public float percentage applicable to 
the Shares is the higher of (i) the percentage that would result in the expected market value 
of H shares held by the public to be HK$1,500,000,000 at the time of Listing and (ii) 15% 
pursuant to Rule 8.08(1) (as amended and replaced by Rule 19A.13A(1)) of the Listing 
Rules.
Immediately following the completion of the Global Offering, an aggregate of 412,125,508 
H Shares, representing approximately 69.27% of the total issued share capital of the 
Company will be counted towards the public float. Therefore, the Company will be able to 
meet the public float requirement under Rule 19A.13A(1) of the Listing Rules.
Immediately following the completion of the Global Offering, based on the final Offer 
Price of HK$10.42 per Offer Share, the expected market value of the H Shares held by the 
public and not subject to any disposal restrictions will be HK$600.1 million. Therefore, the 
Company will be able to satisfy the free float requirement under Rule 19A.13C(1)(b) of the 
Listing Rules, which requires the portion of H shares held by the public and not subject to 
any disposal restrictions to have an expected market value at the time of listing of not less 
than HK$600,000,000.
The Directors confirm that, immediately following the completion of the Global Offering, 
(i) no placee will, individually, be placed more than 10% of the enlarged issued share 
capital of the Company immediately after the Global Offering; (ii) there will not be any 
new substantial Shareholder (as defined in the Listing Rules) immediately after the Global 
Offering; (iii) the three largest public shareholders of the Company do not hold more than 
50% of the H Shares in public hands at the time of the Listing in compliance with Rules 
8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at the 
time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.

<<<PAGE 19>>>
– 19 –
COMMENCEMENT OF DEALINGS
H Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, August 7, 
2026 (Hong Kong time), provided that the Global Offering has become unconditional in all 
respects and the right of termination described in the section headed “Underwriting” in the 
Prospectus has not been exercised. Investors who trade the H Shares prior to the receipt of H 
Share certificates or the H Share certificates becoming valid evidence of title do so entirely 
at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong 
Kong time) on Friday, August 7, 2026, dealings in the H Shares on the Stock Exchange will 
commence at 9:00 a.m. on Friday, August 7, 2026. The H Shares will be traded in board lots 
of 100 H Shares each. The stock code of the H Shares will be 2261.
By order of the Board
NASN Intelligent Tech (Zhejiang) Co., Ltd.
Mr. Tao Zhe
Executive Director, chairman of the Board and chief executive officer
Hong Kong, August 6, 2026
As at the date of this announcement, the Board of Directors of the Company comprises: (i) Mr. Tao Zhe, Ms. 
Liu Qian and Dr. Lin Yi as executive Directors; (ii) Ms. Liu Limei, Mr. Wang Jianming and Mr. Yeh Kuantai 
as non-executive Directors; and (iii) Mr. Fan Chi Chiu, Mr. Jiang Zhenyu and Dr. Wang Yao as independent 
non-executive Directors.
