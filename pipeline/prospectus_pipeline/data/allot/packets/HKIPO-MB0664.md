# 配发结果公告抽取任务：0664.HK Hangzhou Tongshifu Cultural and Creative (Group) Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**30/03/2026 22:11**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0330/2026033003120.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"0664.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
This announcement is not for release, publication or distribution, directly or indirectly, in or into the United States 
or any other jurisdiction where such distribution is prohibited by law, nor is this announcement an offer for sale or 
solicitation to purchase or subscribe for securities in the United States or any other jurisdictions. The Offer Shares 
have not been, and will not be, registered under the United States Securities Act of 1933, as amended from time to 
time (the “U.S. Securities Act”), or any applicable securities laws of any state or other jurisdiction of the United 
States, and may not be offered, sold, pledged or transferred within the United States except in transactions exempt 
from, or not subject to, the registration requirements of the U.S. Securities Act. The Offer Shares are being offered 
and sold outside the United States in offshore transactions in accordance with Regulation S under the U.S. Securities 
Act and applicable laws of each jurisdiction where those offers and sales occur. There will be no public offering of the 
Offer Shares in the United States.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the prospectus dated March 23, 2026 (the “Prospectus”) issued by Hangzhou Tongshifu Cultural and 
Creative (Group) Co., Ltd. (杭州銅師傅文創(集團)股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an offer or an invitation to induce an offer 
by any person to acquire, purchase or subscribe for any of the securities of the Company. This announcement is not a 
prospectus. Potential investors should read the Prospectus for detailed information about the Global Offering described 
below before deciding whether or not to invest in the Offer Shares. Any investment decision in relation to the Offer 
Shares should be taken solely in reliance on the information provided in the Prospectus.
In connection with the Global Offering, CMB International Capital Limited (or its affiliates or any person acting for 
it), as the stabilizing manager (the “Stabilizing Manager”), on behalf of the Underwriters, to the extent permitted by 
the applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect transactions 
with a view to stabilizing or supporting the market price of the H Shares at such price, in such amounts and in such 
manners as the Stabilizing Manager, its affiliates or any person acting for it may determine and at a level higher than 
that which might otherwise prevail in the open market for a limited period after the Listing Date. However, there is 
no obligation on the Stabilizing Manager (or its affiliates or any person acting for it) to conduct any such stabilizing 
action. Such stabilizing actions, if taken, (a) will be conducted at the absolute discretion of the Stabilizing Manager 
(or its affiliates or any person acting for it) and in what the Stabilizing Manager (or its affiliates or any person acting 
for it) reasonably regards as the best interest of our Company, (b) may be discontinued at any time, and (c) is required 
to be brought to an end within 30 days of the last day for lodging applications under the Hong Kong Public Offering 
(which is Saturday, April 25, 2026). Such stabilization action, if taken, may be effected in all jurisdictions where it is 
permissible to do so, in each case in compliance with all applicable laws, rules and regulatory requirements, including 
the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made 
under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Saturday, April 25, 2026). 
After this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of 
the H Shares, could fall.
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on behalf of 
the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the paragraph headed 
“Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for termination” 
in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to 
be on Tuesday, March 31, 2026).

<<<PAGE 2>>>
2
HANGZHOU TONGSHIFU CULTURAL 
AND CREATIVE (GROUP) CO., LTD.
杭州銅師傅文創（集團）股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
7,406,800 H Shares
Number of Hong Kong Offer Shares
:
1,111,000 H Shares (after reallocation)
Number of International Offer Shares
:
6,295,800 H Shares (after reallocation)
Final Offer Price
:
HK$60.00 per H Share, plus brokerage of 
 1.0%, SFC transaction levy of 0.0027%, 
 Stock Exchange trading fee of 0.00565% 
 and the AFRC transaction levy of 
 0.00015%
Nominal value
:
RMB1.00 per H Share
Stock code
:
0664
Sole Sponsor, Sole Sponsor-Overall Coordinator, Joint Global Coordinator,
Joint Bookrunner and Joint Lead Manager
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
HANGZHOU TONGSHIFU CULTURAL 
AND CREATIVE (GROUP) CO., LTD.
杭州銅師傅文創（集團）股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE
AND ALLOTMENT RESULTS
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
0664
Stock short name
TONGSHIFU
Dealings commencement date
March 31, 2026*
* 
See note at the end of this announcement
Price Information
Final Offer Price
HK$60.00
Offer Price Range
HK$60.00 - 
HK$68.00
Offer Shares and Share Capital*
Number of Offer Shares
7,406,800
Final Number of Offer Shares in Hong Kong Public Offering 
 (after reallocation)
1,111,000
Final Number of Offer Shares in International Offering 
 (after reallocation)
6,295,800
Number of issued Shares upon Listing
64,406,800

<<<PAGE 4>>>
4
Over-allocation
No. of Offer Shares over-allocated
0
Note: There has been no over-allocation of Offer Shares in the International Offering. Therefore, the Over-allotment 
Option will not be exercised.
Proceeds
Gross proceeds (Note)
HK$444.41 million
Less: Estimated listing expenses payable based on Offer Price
HK$54.25 million
Net proceeds
HK$390.16 million
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
26,280
No. of successful applications
3,004
Subscription level
59.55 times
No. of Offer Shares initially available under the 
 Hong Kong Public Offering
740,700
No. of Offer Shares reallocated from the International Offering
370,300
Final no. of Offer Shares under the Hong Kong Public Offering 
 (after reallocation)
1,111,000
% of Offer Shares under the Hong Kong Public Offering 
 to the Global Offering
15.00%
Note: For details of the final allocation of Offer Shares to the Hong Kong Public Offering, investors 
can refer http://www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
http://www.eipo.com.hk/eIPOAllotment for the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
43
Subscription level
1.56 times
No. of Offer Shares initially available 
 under the International Offering
6,666,100
No. of Offer Shares reallocated to the Hong Kong Public Offering
370,300
Final no. of Offer Shares under the International Offering 
 (after reallocation)
6,295,800
% of Offer Shares under the International Offering 
 to the Global Offering
85.00%
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a 
consent under paragraph 1C(1) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) 
and Chapter 4.15 of the Guide for New Listing Applicants granted by the Stock Exchange to 
permit the Company to allocate certain Offer Shares to a connected client and (b) a consent under 
paragraph 1C(2) of the Placing Guidelines granted by the Stock Exchange to permit the Company 
to allocate certain Offer Shares to a close associate of an existing Shareholder, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly by 
the Company, any of the Directors, chief executive of the Company, the substantial shareholders, 
existing shareholders of the Company or any of its subsidiaries or their respective close associates; 
and (ii) none of the placees and the public who have purchased the Offer Shares are accustomed 
to taking instructions from the Company, any of the Directors, chief executive of the Company, 
substantial shareholders, existing shareholders of the Company or any of its subsidiaries or their 
respective close associates in relation to the acquisition, disposal, voting or other disposition of H 
Shares registered in his/her/its name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investor
Investor
No. of 
Offer Shares 
allocated
% of 
Offer Shares 
% of 
total issued 
share capital 
after the 
Global 
Offering 
Existing 
shareholders 
or their close 
associates
Jiantou International (Hong Kong) Co., 
Limited (“Jiantou International” or the 
“Cornerstone Investor”)
500,000
6.75%
0.78%
No

<<<PAGE 6>>>
6
Allottees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares allocated
% of Offer Shares 
% of total issued 
share capital after 
the Global 
Offering Note 3
Relationship
Allottees with consent under paragraph 1C(2) of the Placing Guidelines in relation to allocations to a close associate of an existing 
Shareholder Note 1
Wang Wenzhong (汪文忠) 
 (“Mr. Wang”) Note 2
1,543,600
20.84%
2.40%
A placee and a 
 close associate of 
 an existing 
 Shareholder
Allottee with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants 
in relation to allocations to a connected client Note 1
CITIC Securities 
 International Capital 
 Management Limited
100,000
1.35%
0.16%
A connected 
 client of CLSA 
 Limited 
 (“CLSA”)
Notes:
1. 
For details of the consent under (i) paragraph 1C(2) of the Placing Guidelines in relation to allocations to a close associate of an existing Shareholder, and (ii) 
paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations to a connected client, please 
refer to the section headed “Others/Additional Information” in this announcement.
2. 
Mr. Wang is a close associate of Beijing Hezhong Venture Capital Equity Investment Center (Limited Partnership), which is an existing Shareholder.
LOCK-UP UNDERTAKINGS
Directors
Name
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
Number of H 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing
Last day subject 
to the lock-up 
undertakingsNote
Yu Guang (俞光)
14,971,100
14,971,100
27.06%
26.04%
March 30, 2027
Xiao Feng (肖峰)
1,067,715
1,067,715
1.93%
1.86%
March 30, 2027
He Yun (何贇)
360,713
360,713
0.65%
0.63%
March 30, 2027
Luo Renxiang
 (羅仁祥)
288,571
288,571
0.52%
0.50%
March 30, 2027
Note:
Pursuant to the applicable PRC law, the lock-up for Directors ends on March 30, 2027, being 12 months from the Listing Date.

<<<PAGE 7>>>
7
Other Existing Shareholders (including the Pre-IPO Investors as defined in the section 
headed  “History, Development and Corporate Structure” of the Prospectus)
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of H 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued H 
Shares after 
the Global 
Offering 
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
Last day 
subject to 
the lock-up
undertakingsNote 2
Shunwei Ventures III (Hong Kong) 
Limited
7,631,981
7,631,981
13.80%
13.27%
March 30, 2027
Tianjin Jinmi Investment 
Partnership (Limited Partnership) 
5,451,418
5,451,418
9.85%
9.48%
March 30, 2027
Beijing GX Equity Investment Fund 
Partnership Enterprise (Limited 
Partnership)
3,453,413
3,453,413
6.24%
6.01%
March 30, 2027
Euro Master Limited
2,678,093
2,678,093
4.84%
4.66%
March 30, 2027
Guozhong Private Equity 
Investment Fund (Xi’an) 
Partnership (Limited Partnership)
2,158,766
2,158,766
3.90%
3.75%
March 30, 2027
Beijing Hezhong Venture Capital 
Equity Investment Center 
(Limited Partnership) (“Beijing 
Hezhong”）
2,008,599
–
3.63%
3.49%
March 30, 2027
CMG Media Convergence Industry 
Investment Fund (Limited 
Partnership)
1,781,250
1,781,250
3.22%
3.10%
March 30, 2027
Gongqingcheng Jinda Equity 
Investment Partnership (Limited 
Partnership)
1,744,459
1,744,459
3.15%
3.03%
March 30, 2027
Luo Wenjuan (羅文娟)
1,616,002
1,616,002
2.92%
2.81%
March 30, 2027
Changxing Jinyuan Hanfei 
Investment Management Center 
(Limited Partnership)
1,414,004
1,414,004
2.56%
2.46%
March 30, 2027
Qiu Dekang (裘德康)
1,154,287
1,154,287
2.09%
2.01%
March 30, 2027

<<<PAGE 8>>>
8
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of H 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued H 
Shares after 
the Global 
Offering 
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
Last day 
subject to 
the lock-up
undertakingsNote 2
Qingdao Yunzhi Investment 
Management Partnership (Limited 
Partnership)
1,096,577
1,096,577
1.98%
1.91%
March 30, 2027
Guangdong Bay Area No. 1 Digital 
Cultural Industry Investment 
Partnership (Limited Partnership)
712,500
712,500
1.29%
1.24%
March 30, 2027
Shenzhen Guolinfeng Asset 
Management Center (Limited 
Partnership)
621,875
621,875
1.12%
1.08%
March 30, 2027
Ruan Zhuoer (阮卓爾)
519,434
519,434
0.94%
0.90%
March 30, 2027
Yang Ke (楊軻)
490,571
490,571
0.89%
0.85%
March 30, 2027
Zhao Lei (趙磊)
481.817
481.817
0.87%
0.84%
March 30, 2027
Lv Lihan (呂立翰)
447,285
447,285
0.81%
0.78%
March 30, 2027
Zhang Lei (張磊)
431,071
431,071
0.78%
0.75%
March 30, 2027
Ningbo Meishan Bonded Port Area 
Fosun Weiying Equity Investment 
Fund Partnership (Limited 
Partnership)
298,737
298,737
0.54%
0.52%
March 30, 2027
Li Wanqiang (黎萬強)
288,571
288,571
0.52%
0.50%
March 30, 2027
Ding Pengfei (丁鵬飛)
288,571
288,571
0.52%
0.50%
March 30, 2027
Changxing Jinyuan Zhecheng 
Investment Management 
Partnership (Limited Partnership)
240,475
240,475
0.43%
0.42%
March 30, 2027
Chen Jingzhi (陳靜芝)
216,431
216,431
0.39%
0.38%
March 30, 2027
Yin Xuelong (殷雪龍)
202,000
202,000
0.37%
0.35%
March 30, 2027

<<<PAGE 9>>>
9
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of H 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued H 
Shares after 
the Global 
Offering 
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
Last day 
subject to 
the lock-up
undertakingsNote 2
Zhang Jianmei (張建梅)
178,914
178,914
0.32%
0.31%
March 30, 2027
Shanghai Ruma Youhua Enterprise 
Management Partnership (Limited 
Partnership)
171,000
–
–
0.30%
March 30, 2027
Jin Zeguang (金澤廣)
144,283
144,283
0.26%
0.25%
March 30, 2027
Lv Hangjun (呂杭軍)
144,282
144,282
0.26%
0.25%
March 30, 2027
Shentu Jiahui (申屠佳惠)
144,282
144,282
0.26%
0.25%
March 30, 2027
Yang Junjie (楊竣傑)
144,282
144,282
0.26%
0.25%
March 30, 2027
Jin Lihua (金麗華)
144,282
144,282
0.26%
0.25%
March 30, 2027
Zhang Weijiang (張衛江)
144,282
144,282
0.26%
0.25%
March 30, 2027
Qian Jiayang (錢家陽)
125,427
125,427
0.23%
0.22%
March 30, 2027
Yu Hong (俞宏)
124,089
124,089
0.22%
0.22%
March 30, 2027
Dong Shengfang (董聖芳)
115,429
115,429
0.21%
0.20%
March 30, 2027
Huang Dongsheng (黃東升)
115,427
115,427
0.21%
0.20%
March 30, 2027
Ren Bingzhang (任炳章)
109,658
109,658
0.20%
0.19%
March 30, 2027
Jin Hongwei (金宏偉)
106,875
106,875
0.19%
0.19%
March 30, 2027
Zhou Chengfeng (周乘風)
95,227
95,227
0.17%
0.17%
March 30, 2027
Shi Ziming (史子鳴)
92,342
92,342
0.17%
0.16%
March 30, 2027
An Hui (安輝)
92,342
92,342
0.17%
0.16%
March 30, 2027
Ren Liang (任亮)
89,457
89,457
0.16%
0.16%
March 30, 2027
Wang Yuezhen (王玥楨)
86,572
86,572
0.16%
0.15%
March 30, 2027
Lu Huahua (盧華華)
86,572
86,572
0.16%
0.15%
March 30, 2027
Ding Yi (丁屹)
57,717
57,717
0.10%
0.10%
March 30, 2027
Hu Wenping (胡文萍)
57,717
57,717
0.10%
0.10%
March 30, 2027
Zhang Jie (張傑)
57,717
57,717
0.10%
0.10%
March 30, 2027
Wang Qiuxia (王秋霞)
57,717
57,717
0.10%
0.10%
March 30, 2027
Liang Yu (梁鈺)
35,625
35,625
0.06%
0.06%
March 30, 2027

<<<PAGE 10>>>
10
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of H 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued H 
Shares after 
the Global 
Offering 
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
Last day 
subject to 
the lock-up
undertakingsNote 2
Chen Lisheng (陳理升)
35,625
35,625
0.06%
0.06%
March 30, 2027
Xu Danni (徐丹妮)
28,347
28,347
0.05%
0.05%
March 30, 2027
Huang Ningning (黃寧寧)
14,431
14,431
0.03%
0.03%
March 30, 2027
Jia Jinfu (賈金富)
14,431
14,431
0.03%
0.03%
March 30, 2027
Cui Yushu (崔玉舒)
11,546
11,546
0.02%
0.02%
March 30, 2027
Notes:
1. 
The lock-up applies to the Shares held immediately prior to the completion of the Global Offering.
2. 
Pursuant to the applicable PRC law, the lock-up for existing Shareholders ends on March 30, 2027, being 12 
months from the Listing Date.

<<<PAGE 11>>>
11
Cornerstone Investor
Name
Number of
Shares held in
the Company
subject to 
lock-up
undertakings
upon Listing
Number of H 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued
H Shares 
% of total 
issued Shares 
after the 
Global 
Offering upon 
Listing 
Last day 
subject to 
the lock-up
undertakingsNote
Jiantou International
500,000
500,000
0.80%
0.78%
September 30, 2026
Note:
In accordance with the cornerstone investment agreement, the required lock-up ends on September 30, 2026, being 
six months from and including the Listing Date. The Cornerstone Investor will cease to be prohibited from disposing 
of or transferring the H Shares subscribed for pursuant to the cornerstone investment agreement after the indicated 
date.

<<<PAGE 12>>>
12
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
of Shares 
held upon 
Listing 
% of total 
issued share 
capital upon 
Listing 
Top 1
1,543,600
24.52%
20.84%
1,543,600
2.40%
Top 5
3,486,600
55.38%
47.07%
3,486,600
5.41%
Top 10
4,637,100
73.65%
62.61%
4,637,100
7.20%
Top 25
6,042,900
95.98%
81.59%
6,042,900
9.38%
Note:
* 
Ranking of placees is based on the number of Offer Shares allotted to the placees.

<<<PAGE 13>>>
13
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number 
of H Shares 
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
% of total 
issued H Shares 
capital upon 
Listing 
Number 
of Shares 
held upon 
Listing 
Top 1
0
0.00%
0.00%
14,971,100
24.06%
14,971,100
Top 5
0
0.00%
0.00%
34,186,005
54.94%
34,186,005
Top 10
1,543,600
24.52%
20.84%
43,030,082
69.15%
43,030,082
Top 25
3,486,600
55.38%
47.07%
53,410,318
85.83%
53,410,318
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number 
of H Shares 
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
Number 
of Shares 
held upon 
Listing 
% of total 
issued share 
capital upon 
Listing 
Top 1
0
0.00%
0.00%
14,971,100
14,971,100
23.24%
Top 5
1,543,600
24.52%
20.84%
33,051,512
35,060,111
54.44%
Top 10
1,543,600
24.52%
20.84%
43,030,082
45,038,681
69.93%
Top 25
3,486,600
55.38%
47.07%
53,410,318
55,418,917
86.05%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon 
Listing.

<<<PAGE 14>>>
14
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 26,280 valid 
applications made by the public will be conditionally allocated on the basis set out below:
NO. OF 
SHARES 
APPLIED 
FOR
NO. OF 
VALID 
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
POOL A
100
19,181
533 out of 19,181 to receive 100 Shares
2.78%
200
1,423
79 out of 1,423 to receive 100 Shares
2.78%
300
567
47 out of 567 to receive 100 Shares
2.76%
400
267
29 out of 267 to receive 100 Shares
2.72%
500
464
62 out of 464 to receive 100 Shares
2.67%
600
205
32 out of 205 to receive 100 Shares
2.60%
700
468
85 out of 468 to receive 100 Shares
2.59%
800
154
31 out of 154 to receive 100 Shares
2.52%
900
72
16 out of 72 to receive 100 Shares
2.47%
1,000
1,228
290 out of 1,228 to receive 100 Shares
2.36%
1,500
320
113 out of 320 to receive 100 Shares
2.35%
2,000
238
112 out of 238 to receive 100 Shares
2.35%
2,500
120
70 out of 120 to receive 100 Shares
2.33%
3,000
160
112 out of 160 to receive 100 Shares
2.33%
3,500
76
62 out of 76 to receive 100 Shares
2.33%
4,000
79
73 out of 79 to receive 100 Shares
2.31%
4,500
62
100 Shares plus 2 out of 62 to receive additional 
100 Shares
2.29%
5,000
163
100 Shares plus 23 out of 163 to receive additional 
100 Shares
2.28%
6,000
97
100 Shares plus 35 out of 97 to receive additional 
100 Shares
2.27%
7,000
76
100 Shares plus 44 out of 76 to receive additional 
100 Shares
2.26%
8,000
51
100 Shares plus 39 out of 51 to receive additional 
100 Shares
2.21%
9,000
35
100 Shares plus 34 out of 35 to receive additional 
100 Shares
2.19%
10,000
301
200 Shares plus 58 out of 301 to receive additional 
100 Shares
2.19%
20,000
132
400 Shares plus 51 out of 132 to receive additional 
100 Shares
2.19%

<<<PAGE 15>>>
15
NO. OF 
SHARES 
APPLIED 
FOR
NO. OF 
VALID 
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
POOL A
30,000
79
600 Shares plus 46 out of 79 to receive additional 
100 Shares
2.19%
40,000
36
800 Shares plus 28 out of 36 to receive additional 
100 Shares
2.19%
50,000
25
1,000 Shares plus 24 out of 25 to receive additional 
100 Shares
2.19%
60,000
19
1,300 Shares plus 2 out of 19 to receive additional 
100 Shares
2.18%
70,000
36
1,500 Shares plus 10 out of 36 to receive additional 
100 Shares
2.18%
26,134
Total number of Pool A successful applicants: 2,858
POOL B
80,000
69
2,200 Shares plus 28 out of 69 to receive additional 
100 Shares
2.80%
90,000
6
2,500 Shares plus 1 out of 6 to receive additional 
100 Shares
2.80%
100,000
18
2,800 Shares
2.80%
120,000
8
3,300 Shares plus 5 out of 8 to receive additional 
100 Shares
2.80%
140,000
5
3,900 Shares plus 1 out of 5 to receive additional 
100 Shares
2.80%
160,000
8
4,400 Shares plus 7 out of 8 to receive additional 
100 Shares
2.80%
180,000
1
5,000 Shares
2.78%
200,000
12
5,500 Shares plus 8 out of 12 to receive additional 
100 Shares
2.78%
250,000
3
6,900 Shares plus 1 out of 3 to receive additional 
100 Shares
2.77%
300,000
2
8,300 Shares
2.77%
370,300
14
10,200 Shares plus 10 out of 14 to receive 
additional 100 Shares
2.77%
146
Total number of Pool B successful applicants: 146
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 16>>>
16
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the H Shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or 
indirectly, provided by the Company, its substantial shareholders, directors or syndicate members 
to any placees or the public (as the case may be) and the consideration paid by the placees or the 
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased 
by them is the same as the Offer Price in addition to any brokerage, AFRC transaction levy, SFC 
transaction levy and Stock Exchange trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Placing to a close associate of an existing Shareholder with prior consent under paragraph 
1C(2) of the Placing Guidelines
Under the International Offering, certain Offer Shares were placed to a close associate of an 
existing Shareholder pursuant to the Placing Guidelines.
The Company has applied to the Stock Exchange, and the Stock Exchange has granted, a consent 
under paragraph 1C(2) of the Placing Guidelines to permit the Company to allocate such Offer 
Shares in the International Offering to the close associate of the existing Shareholder. The 
allocation of Offer Shares to such close associate of the existing Shareholder is in compliance with 
all the conditions under the consent granted by the Stock Exchange as set out below:
(a) 
the Company and the Overall Coordinators have confirmed that no preferential treatment has 
been, nor will be, given to Beijing Hezhong or Mr. Wang by virtue of their relationship with 
the Company in any allocation in the placing tranche of the Global Offering;
(b) 
the Sole Sponsor has confirmed that to the best of its knowledge and belief, it has no reason 
to believe that Beijing Hezhong or Mr. Wang received any preferential treatment in any 
allocation in the placing tranche of the Global Offering by virtue of their relationship with 
the Company; and
(c) 
the Sole Sponsor has confirmed that (i) Beijing Hezhong (a) has less than 5% voting rights 
in the Company immediately before the Global Offering; (b) is not, and, together with Mr. 
Wang, will not be, a core connected person of the Company or its close associate immediately 
prior to or following the Global Offering; and (c) does not have the power to appoint the 
Company’s directors or any other special rights; (ii) allocation to Mr. Wang will not affect 
the Company’s ability to satisfy the public float requirement under Rule 19A.13A(1) of the 
Listing Rules; and (iii) details of the allocation will be disclosed in this announcement.
For details of the allocations of Offer Shares to the close associate of the existing Shareholder, 
please refer to the section headed “Allotment Results Details – International Offering – Allottees 
with Waivers/Consents Obtained” in this announcement.

<<<PAGE 17>>>
17
Placing to a connected client with prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to a connected client of its 
connected distributor pursuant to the Placing Guidelines.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such 
Offer Shares in the International Offering to the connected client. The allocation of Offer Shares 
to such connected client is in compliance with all the conditions under the consent granted by the 
Stock Exchange as set out below:
(a) 
each of the Overall Coordinators confirms that the Offer Shares allocated to CSICM will 
be held on behalf of independent third parties (as defined in Chapter 4.15 of Guide for New 
Listing Applicants);
(b) 
details of the investment by CSICM and details of the allocation will be disclosed in this 
announcement;
(c) 
each of the Company, CLSA (both as the connected distributor and an Overall Coordinator), 
the Sole Sponsor-Overall Coordinator and CSICM confirms that no preferential treatment has 
been, nor will be, given to CSICM by virtue of their relationship with CLSA in any allocation 
of Offer Shares in the International Offering; and
(d) 
the Overall Coordinators provide the identities of ultimate beneficial owners of the securities, 
or where applicable, details of the structured products under which the subscription by 
CSICM was made in their confirmations.
Details of the placement to the connected client are set out below:
No.
Connected 
Distributor
Connected 
Client
Relationship
Whether the 
connected 
clients 
will hold the 
beneficial 
interests of 
the Offer 
Shares on 
a non – 
discretionary 
basis or 
discretionary 
basis for 
independent 
third parties
Number of 
Offer 
Shares to 
be allocated 
to the 
Connected 
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
capital 
immediately 
following the 
completion 
of the 
Global 
Offering 
1.
CLSA 
Limited 
(“CLSA”)
CITIC Securities 
International 
Capital 
Management 
Limited 
(“CSICM”) 
Note
CSICM is a member of the same group of companies as 
CLSA. CSICM is therefore considered as a connected 
client of CLSA pursuant to paragraph 1B(7) of 
Appendix F1 to the Listing Rules.
Non-
discretionary 
basis
100,000
1.35%
0.16%

<<<PAGE 18>>>
18
Notes:
1. 
CSICM has subscribed for and will hold the Offer Shares as a placee under the International Offering on behalf 
of its ultimate client (the “CSICM Ultimate Client”), on a non-discretionary basis, pursuant to which:
(i) 
CSICM will act as the single counterparty of a back-to-back total return swap transaction (the “CSICM 
Back-to-back TRS”) to be entered into by it in connection with a total return swap order (the “CSICM 
Client TRS”) placed and fully funded by the CSICM Ultimate Client, by which CSICM will pass the full 
economic exposure of the Offer Shares placed to CSICM to the CSICM Ultimate Client. 
(ii) 
As confirmed by CSICM and CLSA, CSICM will hold the legal title and beneficial interest in the Offer 
Shares, but will contractually agree to pass on the full economic exposure and return of the Offer Shares 
to the CSICM Ultimate Client, on a non-discretionary basis. The CSICM Ultimate Client may exercise 
their early termination rights to terminate the CSICM Client TRS at any time from the trade date of the 
CSICM Client TRS which should be on or after the date on which the Offer Shares are listed on the Stock 
Exchange. 
(iii) 
Upon the final maturity or termination of the CSICM Client TRS by the CSICM Ultimate Client, CSICM 
will dispose of the Offer Shares on the secondary market and the CSICM Ultimate Client will receive 
a final termination amount of the CSICM Back-to-back TRS which will have taken into account all the 
economic returns or economic loss in relation to the Offer Shares and the fixed amount of transaction 
fees of the CSICM Back-to-back TRS and the CSICM Client TRS. Due to its internal policy, CSICM will 
not exercise the voting right of the Offer Shares during the terms of the CSICM Back-to-back TRS. 
(iv) 
CSICM is not a collective investment scheme which is not authorized by the SFC, nor is it expected to 
hold the Offer Shares on behalf of such scheme.
2. 
To the best of the knowledge of CSICM and after making all reasonable enquiries, each of the shareholders 
or limited partners holding 30% or more interest in the CSICM Ultimate Client and its fund managers is an 
independent third party of the Company, its subsidiaries, its substantial shareholders, CSICM, CLSA and the 
companies which are members of the same group of CLSA.
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer or 
solicitation to purchase or subscribe for securities in the United States. The securities mentioned 
herein have not been, and will not be, registered under the United States Securities Act of 1933, 
as amended (the “U.S. Securities Act”). The securities may not be offered or sold in the United 
States except pursuant to an exemption from the registration requirements of the U.S. Securities 
Act and in compliance with any applicable state securities laws, or outside the United States unless 
in compliance with Regulation S under the U.S. Securities Act. There will be no public offer of 
securities in the United States.
The Offer Shares are being offered and sold outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act and applicable laws of each jurisdiction 
where those offers and sales occur.

<<<PAGE 19>>>
19
This announcement is for information purposes only and does not constitute an offer or an 
invitation to induce an offer by any person to acquire, purchase or subscribe for any of the 
securities of the Company. This announcement is not a prospectus. Potential investors should read 
the Prospectus for detailed information about the Global Offering described above before deciding 
whether or not to invest in the Offer Shares.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus for detailed information about the Global Offering described 
below before deciding whether or not to invest in the Offer Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves 
and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations 
under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any 
of the events set out in the paragraph headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Grounds for termination” in the Prospectus at any time 
prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
Tuesday, March 31, 2026).
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering (before any exercise of the Over-
allotment Option), 37,546,402 H Shares, representing approximately 58.30% of the issued share 
capital of our Company will count towards the public float for the purpose of Rule 19A.13A(1) 
of the Listing Rules, which is higher than 25%, the minimum prescribed percentage of H Shares 
required to be held in public hands under Rule 19A.13A(1) of the Listing Rules applicable to the 
Company calculated based on the final Offer Price of HK$60.00 per Offer Share, thereby satisfying 
the public float requirement under Rule 19A.13A(1) of the Listing Rules.
All existing shareholders of the Company are subject to a lock-up period of 12 months following 
the Listing Date pursuant to the applicable PRC law. The Cornerstone Investor has agreed 
to a lock-up period of six months following the Listing Date. As such, H Shares held by the 
Cornerstone Investor upon the Listing shall not be counted towards the free float of the H Shares 
of the Company at the time of Listing. Based on the final Offer Price of HK$60.00 per Offer 
Share, the Company satisfies the free float requirement under Rule 19A.13C(1)(a) of the Listing 
Rules.
The Directors confirm that, immediately following the completion of the Global Offering (before 
any exercise of the Over-allotment Option), (i) no placee will, individually, be placed more than 
10% of the enlarged total issued share capital of the Company immediately after the Global 
Offering; (ii) there will not be any new substantial Shareholder immediately after the Global 
Offering; (iii) the three largest public Shareholders of the Company do not hold more than 50% of 
the H Shares in public hands at the time of the Listing in compliance with Rules 8.08(3) and 8.24 
of the Listing Rules; and (iv) there will be at least 300 Shareholders at the time of the Listing in 
compliance with Rule 8.08(2) of the Listing Rules.

<<<PAGE 20>>>
20
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. (Hong Kong time) 
on Tuesday, March 31, 2026, provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting – Underwriting Arrangements 
and Expenses – Hong Kong Public Offering – Grounds for termination” in the Prospectus has not 
been exercised. Investors who trade H Shares on the basis of publicly available allocation details 
prior to the receipt of H Share certificates or prior to the H Share certificates becoming valid 
evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong Kong time) 
on Tuesday, March 31, 2026, it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. (Hong Kong time) on Tuesday, March 31, 2026. The H Shares will be 
traded in board lots of 100 H Shares each, and the stock code of the H Shares will be 0664.
By order of the Board
Hangzhou Tongshifu Cultural and Creative (Group) Co., Ltd.
Yu Guang
Chairman of the Board and Executive Director
Hong Kong, March 30, 2026
As of the date of this announcement, the Board comprises: (i) Mr. Yu Guang, Mr. Luo Renxiang, 
Mr. He Yun, Ms. Wang Xiaoxia and Mr. Chen Ruiguang as executive Directors; (ii) Mr. Xiao Feng 
as a non-executive Director; and (iii) Mr. Tu Bisheng, Dr. Huang Wenli and Mr. Fong Chun Fai as 
independent non-executive Directors.
