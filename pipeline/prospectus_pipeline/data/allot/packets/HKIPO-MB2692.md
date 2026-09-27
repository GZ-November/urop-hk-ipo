# 配发结果公告抽取任务：2692.HK Shenzhen Zhaowei Machinery & Electronics Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**06/03/2026 22:41**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0306/2026030601575.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2692.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
This announcement does not constitute an offer to sell or the solicitation of an offer to buy nor shall there be any sale 
of Offer Shares in any jurisdiction in which such offer, solicitation or sales would be unlawful. This announcement is 
not for release, publication or distribution, directly or indirectly, in or into the United States or any other jurisdiction 
where such distribution is prohibited by law, nor is this announcement an offer for sale or solicitation to purchase or 
subscribe for securities in the United States or any other jurisdictions. The Offer Shares have not been, and will not 
be, registered under the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities 
Act”), or any applicable state securities laws, and may not be offered, sold, pledged or transferred within the United 
States or to, or for the account or benefit of, U.S. persons (as defined in Regulation S under the U.S. Securities Act 
(the “Regulation S”)) except in transactions exempt from, or not subject to, the registration requirements of the 
U.S. Securities Act. The Offer Shares are being offered and sold outside the United States in offshore transactions in 
accordance with Regulation S. There will be no public offering of the Offer Shares in the United States.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
February 27, 2026 (the “Prospectus”) issued by Shenzhen Zhaowei Machinery & Electronics Co., Ltd. (深圳市兆
威機電股份有限公司) (the “Company”) for detailed information about the Global Offering described below before 
deciding whether or not to invest in the H Shares thereby being offered. Any investment decision in relation to the 
Offer Shares should be taken solely in reliance on the information in the Prospectus. The Company has not been and 
will not be registered under the U.S. Investment Company Act of 1940, as amended.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on behalf of 
the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
Monday, March 9, 2026).

<<<PAGE 2>>>
2
Shenzhen Zhaowei Machinery & Electronics Co., Ltd.
深圳市兆威機電股份有限公司
(a joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under the 
Global Offering
:
26,748,300 H Shares
Number of Hong Kong Offer Shares
:
2,674,900 H Shares (subject to reallocation)
Number of International Offer Shares
:
24,073,400 H Shares (subject to 
reallocation)
Final Offer Price
:
HK$71.28 per H Share, plus brokerage of 
1%, SFC transaction levy of 0.0027%, 
AFRC transaction levy of 0.00015% and 
Stock Exchange trading fee of 0.00565% 
(payable in full on application and subject 
to refund)
Nominal value
:
RMB1.0 per H Share
Stock code
:
2692
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators,
Joint Global Coordinators and Joint Bookrunners
Overall Coordinators, Joint Global Coordinators and Joint Bookrunners
Joint Bookrunners

<<<PAGE 3>>>
3
SHENZHEN ZHAOWEI MACHINERY & ELECTRONICS CO., LTD.
深圳市兆威機電股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated February 27, 2026 (the “Prospectus”) issued by 
Shenzhen Zhaowei Machinery & Electronics Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
2692
Stock short name
ZHAOWEI
Dealings commencement date
March 9, 2026*
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$71.28
Maximum Offer Price
HK$73.68
Offer Price Adjustment exercised
N/A
Offer Shares and Share Capital
Number of Offer Shares
26,748,300
Number of Offer Shares in Hong Kong Public Offering
2,674,900
Number of Offer Shares in International Offering
24,073,400
Number of issued Shares upon Listing
267,482,700
Proceeds
Gross proceeds (Note)
HK$1,906.62 million
 Less: Estimated listing expenses payable based on Final 
Offer Price
HK$ (78.89) million
Net proceeds
HK$1,827.73 million
Note: Gross proceeds refer to the amount to which the issuer is entitled receive. For details of the use of proceeds, 
please refer to the Prospectus dated February 27, 2026.

<<<PAGE 4>>>
4
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERRING
No. of valid applications
180,292
No. of successful applications
23,940
Subscription level
1,536.76 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong 
Public Offering
2,674,900
Final no. of Offer Shares under the Hong Kong Public 
Offering
2,674,900
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering
10.00%
Note: For details of the final allocation of H Shares to the Public Offer, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by name or identification number or www.hkeipo.hk/IPOResult 
for the full list of allottees.
INTERNATIONAL OFFER
No. of placees
75
Subscription Level
13.40 times
No. of Offer Shares initially available under the International 
Offering
24,073,400
% of Offer Shares under the International Offer to the Global 
Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, controlling shareholders, 
substantial shareholders, existing shareholders of the Company or any of its subsidiaries or their 
respective close associates; and (ii) none of the placees and the public who have purchased the 
Offer Shares are accustomed to taking instructions from the Company, any of the Directors, chief 
executive of the Company, controlling shareholders, substantial shareholders, existing shareholders 
of the Company or any of its subsidiaries or their respective close associates in relation to the 
acquisition, disposal, voting or other disposition of Shares registered in his/her/its name or 
otherwise held by him/her/it.

<<<PAGE 5>>>
5
The placees in the International Offer include the following:
Cornerstone Investors
Investor
No. of 
Offer Shares 
Allocated
% of 
Offer Shares 
(Note 1)
% of total
issued share
capital after 
the Global 
Offering 
(Note 2)
Existing
shareholders 
or their close 
associates
HHLRA
1,644,800
6.15%
0.61%
No
Mirae Asset Securities HK
548,200
2.05%
0.20%
No
Perseverance Asset Management
657,900
2.46%
0.25%
No
Da Cheng International
383,700
1.43%
0.14%
No
GF Fund HK
328,900
1.23%
0.12%
No
Oakwise Growth Fund
548,200
2.05%
0.20%
No
Jump Trading
328,900
1.23%
0.12%
No
VVC Technology
219,300
0.82%
0.08%
No
FMF
219,300
0.82%
0.08%
No
Taihu Golden Valley
548,200
2.05%
0.20%
No
Topstar Worldwide
474,000
1.77%
0.18%
No
Virtues Capital and China Securities (International) 
Investment Company Limited (in connection with 
the OTC Swaps)
438,600
1.64%
0.16%
No
Hengbang and China Galaxy International 
Investment Company Limited (in connection  
with the Hengbang OTC Swaps)
312,800
1.17%
0.12%
No
W Investment
394,700
1.48%
0.15%
No
BeingBoom Capital
328,900
1.23%
0.12%
No
Mr. He Maoling
328,900
1.23%
0.12%
No
Mr. Luo Jie
328,900
1.23%
0.12%
No
Bridge Zone Group
271,400
1.01%
0.10%
No
CMBC International
274,100
1.02%
0.10%
No
RIME
280,500
1.05%
0.10%
No
Main Source Capital
280,500
1.05%
0.10%
No
Total
9,140,700
34.17%
3.42%
Notes:
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be 
issued under the Global Offering.
2. 
The total issued share capital after the Global Offering includes 240,734,400 A Shares listed on the Shenzhen 
Stock Exchange as of the Latest Practicable Date.

<<<PAGE 6>>>
6
Allottees with Waivers/Consents Obtained
Investor
No. of 
shares 
allocated
% of 
offer shares 
(Note 1)
% of total 
issued share 
capital after 
the Global 
Offering 
(Note 2)
Relationship*
Allotees with consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of 
further H Shares to certain Cornerstone Investors and/or their close associates(Note 3 and 4)
HHLRA
1,644,800
6.15%
0.61%
Same entity as 
Cornerstone Investor
Mirae Asset Securities HK
1,206,200
4.51%
0.45%
Same entity as 
Cornerstone Investor
Perseverance Asset Management
625,000
2.34%
0.23%
Same entity as 
Cornerstone Investor
Da Cheng International
307,000
1.15%
0.11%
Same entity as 
Cornerstone Investor
GF Fund HK
657,900
2.46%
0.25%
Same entity as 
Cornerstone Investor
Oakwise Growth Fund
548,200
2.05%
0.20%
Same entity as 
Cornerstone Investor
Jump Trading
328,900
1.23%
0.12%
Same entity as 
Cornerstone Investor
VVC Technology
263,100
0.98%
0.10%
Same entity as 
Cornerstone Investor
FMF
219,300
0.82%
0.08%
Same entity as 
Cornerstone Investor
Virtues Capital and China Securities 
(International) Investment Company 
Limited (in connection with the OTC 
Swaps)
347,300
1.30%
0.13%
Same entity as 
Cornerstone Investor
Hengbang and China Galaxy International 
Investment Company Limited (in 
connection with the Hengbang OTC 
Swaps)
312,800
1.17%
0.12%
Same entity as 
Cornerstone Investor
Shenzhen Qianhai Hanrong Private Equity 
Securities Fund Management Co., Ltd.  
(深圳市前海瀚融私募證券基金管理有限
公司) (“Qianhai Hanrong”) (Note 5)
383,700
1.43%
0.14%
A close associate of a 
Cornerstone Investor,
W Investment

<<<PAGE 7>>>
7
Investor
No. of 
shares 
allocated
% of 
offer shares 
(Note 1)
% of total 
issued share 
capital after 
the Global 
Offering 
(Note 2)
Relationship*
BeingBoom Capital
285,100
1.07%
0.11%
Same entity as 
Cornerstone Investor
Mr. He Maoling
328,900
1.23%
0.12%
Same entity as 
Cornerstone Investor
Mr. Luo Jie
164,400
0.61%
0.06%
Same entity as 
Cornerstone Investor
Bridge Zone Group
271,400
1.01%
0.10%
Same entity as 
Cornerstone Investor
CMBC International
274,100
1.02%
0.10%
Same entity as 
Cornerstone Investor
Rime
224,400
0.84%
0.08%
Same entity as 
Cornerstone Investor
Mr. Xue Shouguang (薛守光)
280,500
1.05%
0.10%
A close associate of 
a Cornerstone 
Investor, 
Main Source 
Capital
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients(Note 6)
Bosera Asset Management (International) 
Co., Limited (“Bosera Asset 
Management”)
110,000
0.41%
0.04%
Connected client 
as a placee
Huatai Capital Investment Limited (“HTCI”)
187,500
0.70%
0.07%
Connected client as a 
placee
Guotai Junan Investments (Hong Kong) 
Limited (“GTJA Investments”)
383,700
1.43%
0.14%
Connected client 
as a placee

<<<PAGE 8>>>
8
Investor
No. of 
shares 
allocated
% of 
offer shares 
(Note 1)
% of total 
issued share 
capital after 
the Global 
Offering 
(Note 2)
Relationship*
Notes:
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
2. 
The total issued share capital after the Global Offering includes 240,734,400 A Shares listed on the Shenzhen 
Stock Exchange as of the Latest Practicable Date.
3. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details – International Offering – Cornerstone Investors” in this announcement. For details of the 
consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations 
of further H Shares to the Cornerstone Investors, please refer to the section headed “Others/Additional 
Information – Allocations of Offer Shares to Cornerstone Investors and/or their close associates with a 
consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants” in this announcement.
4. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details — International Offering — Cornerstone Investors” in this announcement.
5. 
Qianhai Hanrong and Guotai Haitong Securities Co., Ltd. will enter into cross border delta-one OTC equity 
swap transaction for the purpose of subscription of the Offer Shares in the amount of USD3,500,000. For the 
details of GTHT Client TRS, please refer to the section headed “Others/Additional Information — Placing to 
connected clients with a consent under paragraph 1C(1) of the Placing Guidelines”.
6. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients, please refer to the section headed 
“Others/Additional Information — Placing to connected clients with a consent under paragraph 1C(1) of the 
Placing Guidelines” in this announcement.

<<<PAGE 9>>>
9
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Number of 
H Shares held in 
the Company 
subject to lock-up 
undertakings 
upon Listing
% of total 
issued H Shares 
after the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing(Note 1)
% of 
shareholding 
in the Company 
subject to lockup 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings
Controlling Shareholders (Note 2)
150,217,600 
A Shares
0
0
62.40%
September 8, 2026 
(First Six-Month 
Period) (Note 3)
March 8, 2026 
(Second Six-Month 
Period) (Note 4)
Notes:
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
2. 
Mr. Li, Ms. Xie, Zhaowei Investment and Qingmo Partnership held in aggregate 150,217,600 A Shares, 
which are subject to lock-up undertakings upon Listing.
3. 
The Controlling Shareholders may dispose of or transfer Shares after the indicated date subject to that the 
Controlling Shareholders will not cease to be a Controlling Shareholders.
4. 
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after the 
indicated date.

<<<PAGE 10>>>
10
Cornerstone Investors
Name
Number of 
H Shares held in 
the Company 
subject to lock-up 
undertakings 
upon Listing
% of total 
issued H Shares 
after the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing(Note 1)
% of 
shareholding 
in the Company 
subject to lockup 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings
HHLRA
1,644,800 
6.15%
0.61%
September 8, 2026
Mirae Asset Securities HK
548,200 
2.05%
0.20%
September 8, 2026
Perseverance Asset Management
657,900 
2.46%
0.25%
September 8, 2026
Da Cheng International
383,700 
1.43%
0.14%
September 8, 2026
GF Fund HK
328,900 
1.23%
0.12%
September 8, 2026
Oakwise Growth Fund
548,200 
2.05%
0.20%
September 8, 2026
Jump Trading
328,900 
1.23%
0.12%
September 8, 2026
VVC Technology
219,300 
0.82%
0.08%
September 8, 2026
FMF
219,300 
0.82%
0.08%
September 8, 2026
Taihu Golden Valley
548,200 
2.05%
0.20%
September 8, 2026
Topstar Worldwide
474,000 
1.77%
0.18%
September 8, 2026
Virtues Capital and China Securities 
(International) Investment Company 
Limited (in connection with the OTC 
Swaps)
438,600 
1.64%
0.16%
September 8, 2026
Hengbang and China Galaxy International 
Investment Company Limited (in 
connection with the Hengbang OTC 
Swaps)
312,800 
1.17%
0.12%
September 8, 2026
W Investment
394,700 
1.48%
0.15%
September 8, 2026
BeingBoom Capital
328,900 
1.23%
0.12%
September 8, 2026
Mr. He Maoling
328,900 
1.23%
0.12%
September 8, 2026
Mr. Luo Jie
328,900 
1.23%
0.12%
September 8, 2026
Bridge Zone Group
271,400 
1.01%
0.10%
September 8, 2026
CMBC International
274,100 
1.02%
0.10%
September 8, 2026
RIME
280,500 
1.05%
0.10%
September 8, 2026
Main Source Capital
280,500 
1.05%
0.10%
September 8, 2026
Total
9,140,700 
34.17%
3.42%

<<<PAGE 11>>>
11
PLACEE CONCENTRATION ANALYSIS
Placees
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering
Allotment 
as % of total 
Offer Shares
Number of
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing
Top 1
3,289,600
13.66%
12.30%
3,289,600
1.23%
Top 5
8,410,100
34.94%
31.44%
8,410,100
3.14%
Top 10
12,479,400
51.84%
46.65%
12,479,400
4.67%
Top 25
20,760,100
86.24%
77.61%
20,760,100
7.76%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDER CONCENTRATION ANALYSIS
Number of
H Shares
allotted
Allotment
as % of
International
Offering
Allotment
as % of total
Offer Shares
Number of
H Shares held
upon Listing
% of
total issued
H Shares
capital upon
Listing
Number of
Shares held
upon Listing
Top 1
3,289,600
13.66%
12.30%
3,289,600
12.30%
3,289,600
Top 5
8,410,100
34.94%
31.44%
8,410,100
31.44%
8,410,100
Top 10
12,479,400
51.84%
46.65%
12,479,400
46.65%
12,479,400
Top 25
20,760,100
86.24%
77.61%
20,760,100
77.61%
20,760,100
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
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
Top1
–
0.00%
0.00%
–
150,217,600
56.16%
Top5
3,289,600
13.66%
12.30%
3,289,600 
165,576,566
61.90%
Top10
5,044,000
20.95%
18.86%
5,044,000 
175,888,583
65.76%
Top25
15,111,300
62.77%
56.49%
15,111,300
188,134,994
70.34%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 12>>>
12
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
Number of 
H Shares 
applied for
Number of 
valid 
applications
Basis of allocation/ballot
Approximate 
percentage allotted of 
the total number 
of H Shares 
applied for
POOL A
100
64,785
2,592 out of 64,785 applicants to receive 100 H Shares
4.00%
200
7,953
331 out of 7,953 applicants to receive 100 H Shares
2.08%
300
6,262
267 out of 6,262 applicants to receive 100 H Shares
1.42%
400
3,509
167 out of 3,509 applicants to receive 100 H Shares
1.19%
500
3,748
193 out of 3,748 applicants to receive 100 H Shares
1.03%
600
7,930
437 out of 7,930 applicants to receive 100 H Shares
0.92%
700
1,592
93 out of 1,592 applicants to receive 100 H Shares
0.83%
800
1,308
81 out of 1,308 applicants to receive 100 H Shares
0.77%
900
1,618
104 out of 1,618 applicants to receive 100 H Shares
0.71%
1,000
8,934
594 out of 8,934 applicants to receive 100 H Shares
0.66%
1,500
3,841
297 out of 3,841 applicants to receive 100 H Shares
0.52%
2,000
3,540
305 out of 3,540 applicants to receive 100 H Shares
0.43%
2,500
2,552
239 out of 2,552 applicants to receive 100 H Shares
0.37%
3,000
2,475
248 out of 2,475 applicants to receive 100 H Shares
0.33%
3,500
1,651
175 out of 1,651 applicants to receive 100 H Shares
0.30%
4,000
1,751
195 out of 1,751 applicants to receive 100 H Shares
0.28%
4,500
1,442
168 out of 1,442 applicants to receive 100 H Shares
0.26%
5,000
2,786
337 out of 2,786 applicants to receive 100 H Shares
0.24%
6,000
2,210
286 out of 2,210 applicants to receive 100 H Shares
0.22%
7,000
1,946
266 out of 1,946 applicants to receive 100 H Shares
0.20%
8,000
1,700
245 out of 1,700 applicants to receive 100 H Shares
0.18%
9,000
1,414
213 out of 1,414 applicants to receive 100 H Shares
0.17%
10,000
9,240
1,441 out of 9,240 applicants to receive 100 H Shares
0.16%
20,000
5,132
1,035 out of 5,132 applicants to receive 100 H Shares
0.10%
30,000
3,421
802 out of 3,421 applicants to receive 100 H Shares
0.08%
40,000
2,440
636 out of 2,440 applicants to receive 100 H Shares
0.07%
50,000
2,127
603 out of 2,127 applicants to receive 100 H Shares
0.06%
60,000
3,382
1,025 out of 3,382 applicants to receive 100 H Shares
0.05%
Total
160,689
Total number of Pool A successful applicants: 13,375

<<<PAGE 13>>>
13
Number of 
H Shares 
applied for
Number of 
valid 
applications
Basis of allocation/ballot
Approximate 
percentage allotted of 
the total number 
of H Shares 
applied for
POOL B
70,000
5,795
2,029 out of 5,795 applicants to receive 100 H Shares
0.05%
80,000
2,298
900 out of 2,298 applicants to receive 100 H Shares
0.05%
90,000
1,559
674 out of 1,559 applicants to receive 100 H Shares
0.05%
100,000
5,035
2,377 out of 5,035 applicants to receive 100 H Shares
0.05%
200,000
2,129
1,798 out of 2,129 applicants to receive 100 H Shares
0.04%
300,000
1,003
100 H Shares plus 187 out of 1,003 applicants to 
receive an additional 100 H Shares
0.04%
400,000
483
100 H Shares plus 247 out of 483 applicants to receive 
an additional 100 H Shares
0.04%
500,000
305
100 H Shares plus 251 out of 305 applicants to receive 
an additional 100 H Shares
0.04%
600,000
230
200 H Shares plus 29 out of 230 applicants to receive 
an additional 100 H Shares
0.04%
700,000
132
200 H Shares plus 55 out of 132 applicants to receive 
an additional 100 H Shares
0.03%
800,000
104
200 H Shares plus 73 out of 104 applicants to receive 
an additional 100 H Shares
0.03%
900,000
57
200 H Shares plus 56 out of 57 applicants to receive 
an additional 100 H Shares
0.03%
1,000,000
78
300 H Shares plus 21 out of 78 applicants to receive 
an additional 100 H Shares
0.03%
1,100,000
36
300 H Shares plus 20 out of 36 applicants to receive 
an additional 100 H Shares
0.03%
1,200,000
42
300 H Shares plus 34 out of 42 applicants to receive 
an additional 100 H Shares
0.03%
1,337,400
317
400 H Shares plus 50 out of 317 applicants to receive 
an additional 100 H Shares
0.03%
Total
19,603
Total number of Pool B successful applicants: 10,565
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 14>>>
14
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and trading fee payable.
OTHERS/ADDITIONAL INFORMATION

<<<PAGE 15>>>
15
Allocations of Offer Shares to Cornerstone Investors and/or their close associates with a 
consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph 
18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to allocate 
further Offer Shares in the International Offering to certain Cornerstone Investors and/or their 
close associates as placees, subject to the following conditions (the “Allocation to Size-based 
Exemption Participants”):
(a) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;
(b) 
the Offer Shares allocated to all existing shareholders and their close associates (whether as 
Cornerstone Investors and/or as placees) as permitted under this exemption will not exceed 
30% of the total number of Shares offered under the Global Offering;
(c) 
the Allocation to Size-based Exemption Participants will not affect the Company’s ability 
to satisfy its public float requirement as prescribed by the Stock Exchange under the waiver 
from strict compliance with the requirements of Rule 19A.13A(2) of the Listing Rules;
(d) 
each of the Directors, chief executive of the Company and the Controlling Shareholders has 
confirmed that no securities have been allocated to them or their respective close associates 
under this exemption; and
(e) 
details of the Allocation to Size-based Exemption Participants under the Size-based 
Exemption will be disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to Cornerstone Investors and/or their close associates, 
please refer to the section headed “Allotment Results Details – International Offering – Allotees 
with Waivers/Consents Obtained” in this announcement.

<<<PAGE 16>>>
16
Placing to connected clients with consent under paragraph 1C(1) of the Placing Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines as placees. Please refer to the section 
headed “Allotment Results Details – International Offering – Allottees with Waivers/Consents 
Obtained” in this announcement for details. The Company has applied to the Stock Exchange for, 
and the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing Guidelines 
to permit the Company to allocate such Offer Shares in the International Offering to the connected 
clients as placees. The allocation of Offer Shares to such connected clients is in compliance with 
all the conditions under the consent granted by the Stock Exchange. Details of the placement to 
connected clients as placees are set out below.
No.
Connected 
Distributor
Connected Client
Relationship
Whether the 
Connected Client 
is a collective 
investment scheme 
which is not 
authorised by the 
SFC or is expected 
to hold the Offer 
Shares on behalf 
of such scheme
Number of 
Offer Shares to 
be allocated to 
the Connected 
Client(Note 1)
Approximate 
percentage of 
total number 
of Offer Shares 
under the Global 
Offering(Note 1)
Approximate 
percentage of 
total issued 
share capital 
after the Global 
Offering(Note 1)
Part A – Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties
1.
China Merchants 
Securities (HK) 
Co., Limited 
(“CMS”)
Bosera Asset 
Management(Note 2)
Bosera Asset 
Management is a 
member of the same 
group of companies as 
CMS
Yes
110,000
0.41%
0.04%

<<<PAGE 17>>>
17
No.
Connected 
Distributor
Connected Client
Relationship
Whether the 
Connected Client 
is a collective 
investment scheme 
which is not 
authorised by the 
SFC or is expected 
to hold the Offer 
Shares on behalf 
of such scheme
Number of 
Offer Shares to 
be allocated to 
the Connected 
Client(Note 1)
Approximate 
percentage of 
total number 
of Offer Shares 
under the Global 
Offering(Note 1)
Approximate 
percentage of 
total issued 
share capital 
after the Global 
Offering(Note 1)
Part B – Connected Clients holding the beneficial interest of the Offer Shares on a non-discretionary basis on behalf of independent third parties
1.
Huatai Financial 
Holdings (Hong 
Kong) Limited 
(“HTFH”)
HTCI(Note 3)
HTCI is a member of 
the same group of 
companies as HTFH
No
187,500
0.70%
0.07%
2.
Guotai Junan 
Securities 
(Hong Kong) 
Limited (“GTJA 
Securities”)
GTJA 
Investments(Note 4)
GTJA Investments is a 
member of same group 
of companies as GTJA 
Securities
No
383,700
1.43%
0.14%
Notes:
1. 
The total issued share capital after the Global Offering includes 240,734,400 A Shares listed on the Shenzhen 
Stock Exchange as of the Latest Practicable Date.
2. 
Bosera Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager 
managing the sub-funds on behalf of its following clients, each of which is an independent third party of the 
Company, its subsidiaries, its substantial shareholders, CMS and the companies which are members of the 
same group of CMS to the best knowledge and belief of Bosera Asset Management.
Name of the sub-funds to 
which the Offer Shares will be 
allocated
Whether any investor holds 30% 
or more interests in the sub-fund 
(Y/N)
Ultimate Beneficiay 
Owner
Shareholding %
Bosera Hong Kong Equity Plus 
Fund (SFC authorised collective 
investment schemes)
N
N/A
N/A
Bosera Global Select Equity Fund 
SP (not SFC-authorised collective 
investment schemes)
Y
Zhang Lei (張雷)
53.67%

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
investment scheme 
which is not 
authorised by the 
SFC or is expected 
to hold the Offer 
Shares on behalf 
of such scheme
Number of 
Offer Shares to 
be allocated to 
the Connected 
Client(Note 1)
Approximate 
percentage of 
total number 
of Offer Shares 
under the Global 
Offering(Note 1)
Approximate 
percentage of 
total issued 
share capital 
after the Global 
Offering(Note 1)
3. 
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public 
offerings (“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products issued by 
appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. In 
connection with such products, the licensed domestic securities firms, through their Hong Kong affiliates, 
may participate in Hong Kong IPOs either as placees or cornerstone investors (the “Cross-border 
Derivatives Trading Regime”).
Huatai Securities Co., Ltd. (“HTSC”), the A shares of which are listed on the Shanghai Stock Exchange 
(stock code: 601688), the H shares of which are listed on the Stock Exchange (stock code: 6886), and the 
global depositary receipts of which are listed on the London Stock Exchange (LON: HTSC), is one of the 
domestic securities firms licensed to undertake cross-border derivatives trading activities. HTSC entered into 
an ISDA agreement (the “ISDA Agreement”) with its indirectly wholly-owned subsidiary, HTCI, to set out 
the principal terms of any future total return swap between HTSC and HTCI.
HTFH is a non-syndicate distributor and the Connected Distributor. Pursuant to the ISDA Agreement, HTCI, 
which intends to participate in the International Offering as a placee, will hold the beneficial interest of the 
Offer Shares on a nondiscretionary basis as the single underlying holder under a back-to-back total return 
swap (the “HT Back-to-back TRS”) to be entered by HTCI in connection with Huatai TRS (as defined 
below) order placed by and fully funded (i.e. with no financing provided by HTCI) by the Huatai Ultimate 
Clients (as defined below), by which, HTCI will, subject to customary fees and commissions, pass the full 
economic exposure of the Offer Shares ultimately to the Huatai Ultimate Clients, which in effect, HTCI will 
hold the beneficial interest of the Offer Shares on behalf of the Huatai Ultimate Clients. HTFH and HTCI are 
indirectly wholly-owned subsidiaries of HTSC. Accordingly, HTCI is considered as a “connected clients” of 
Huatai pursuant to paragraph 1B(7) of the Placing Guidelines.

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
investment scheme 
which is not 
authorised by the 
SFC or is expected 
to hold the Offer 
Shares on behalf 
of such scheme
Number of 
Offer Shares to 
be allocated to 
the Connected 
Client(Note 1)
Approximate 
percentage of 
total number 
of Offer Shares 
under the Global 
Offering(Note 1)
Approximate 
percentage of 
total issued 
share capital 
after the Global 
Offering(Note 1)
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investor (the “Huatai Ultimate 
Clients”) cannot directly subscribe for the Offer Shares but may invest in derivative products issued by 
domestic securities firms licenced to undertake cross-border derivatives trading activities, such as HTSC, 
with the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, the Huatai 
Ultimate Clients will, through its investment manager, place a total return swap order (the “Huatai TRS”) 
with HTSC in connection with the Company’s IPO and HTSC will place a HT Back-to-back TRS order to 
HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the HT Back-to-back TRS, 
HTCI participates in the Company’s IPO and subscribes for the Offer Shares through placing order with 
HTFH during the International Offering.
The Huatai Ultimate Clients for purpose of this placing subscription are certain investment funds managed by 
Shanghai Gaoyi Asset Management Partnership (Limited Partnership) (上海高毅資產管理合夥企業(有限合
夥)) on a discretionary basis, as follows:
Name of the Huatai Ultimate Clients
Ultimate beneficial 
owner(s) holding 30% 
or more interest in 
the fund managers 
and limited partnerships 
(if any)
高毅國鷺信遠私募證券投資基金(Gaoyi Guolu Xinyuan Private Equity 
Investment Fund)
NA
金太陽高毅國鷺 1 號崇遠基金(Jintaiyang Gaoyi Guolu No. 1 Chongyuan 
Fund)
NA
高毅利偉精選唯實基金(Gaoyi Liwei Selected Weishi Fund)
NA
To the best of knowledge of HTCI and after making all reasonable enquiries, the Huatai Ultimate Clients are 
independent third parties of (i) the Company, its connected person or the associates thereof, and (ii) HTCI, 
and the companies which are members of the same group of HTCI.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the HT Back-to-back TRS in 
connection with the Huatai TRS order placed by the Huatai Ultimate Clients. Pursuant to the terms of the 
contracts of the HT Back-to-back TRS and the Huatai TRS, during the tenor of the HT Back-to-back TRS and 
the Huatai TRS, subject to customary fees and commissions, all economic returns of the Offer Shares will be 
ultimately passed to the Huatai Ultimate Clients through the HT Back-to-back TRS and the Huatai TRS and 
all economic loss shall be ultimately borne by the Huatai Ultimate Clients. HTCI will not take any economic 
return or bear any economic loss in relation to the Offer Shares, save as customary fees and commissions.

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
investment scheme 
which is not 
authorised by the 
SFC or is expected 
to hold the Offer 
Shares on behalf 
of such scheme
Number of 
Offer Shares to 
be allocated to 
the Connected 
Client(Note 1)
Approximate 
percentage of 
total number 
of Offer Shares 
under the Global 
Offering(Note 1)
Approximate 
percentage of 
total issued 
share capital 
after the Global 
Offering(Note 1)
Investment in the HT Back-to-back TRS and the Huatai TRS is similar to the investment in a qualified 
domestic institutional investor fund (“QDII”) in the way that the Huatai Ultimate Clients would reap all 
the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through the 
exchange rate exposure on both the notional value of the investment and the profit and loss of the investment. 
In contrast, the profit and loss of the HT Back-to-back TRS and the Huatai TRS factor into account the 
fluctuation in RMB exchange rate upon termination of the Huatai TRS by converting the profit and loss using 
the current exchange rate at the time of termination. As such, the Huatai Ultimate Clients would bear the 
exchange rate exposure of the profit and loss on settlement date.
The Huatai Ultimate Clients may exercise an early termination right to terminate the Huatai TRS at any 
time from the issue date of the Huatai TRS which should be on or after the date on which the Offer Shares 
are listed on the Stock Exchange at their own discretions. Upon the termination upon maturity or early 
termination of the Huatai TRS by the Huatai Ultimate Clients, HTCI will dispose of the Offer Shares on the 
secondary market and the Huatai Ultimate Clients will receive a final settlement amount in cash in accordance 
with the terms and conditions of the HT Back-to-back TRS and the Huatai TRS which should have taken into 
account all the economic returns or economic loss in relation to the Offer Shares. If upon the maturity of the 
Huatai TRS, the Huatai Ultimate Clients intend to extend the investment period, subject to further agreement 
between HTSC and the relevant Huatai Ultimate Clients, the term of the Huatai TRS could be extended by 
way of a new issuance or a tenor extension. Accordingly, HTSC will extend the term of the HT Back-to-back 
TRS by way of a new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass 
through the economic exposure to the Huatai Ultimate Clients, being an onshore clients who places Huatai 
TRS orders with HTSC in connection with the IPO of the Company. HTCI will not exercise the voting rights 
of the Offer Shares during the tenor of the HT Back-to-back TRS.
During the life of the Huatai TRS and HT Back-to-back TRS, HTCI may continue to hold the Offer Shares 
in its custodian account, or to hold some or all of the Offer Shares in a prime brokerage account for stock 
borrowing purposes, where HTCI will lend out its holding of underlying Offer Shares in the form of stock 
borrowing loans consistent with market practice to lower its finance costs, provided that HTCI has the ability 
to call back the Offer Shares on loan at any time in order to satisfy its obligations under the HT Back-to-back 
TRS to ensure the economic interests are ultimately passed to the Huatai Ultimate Clients.

<<<PAGE 21>>>
21
No.
Connected 
Distributor
Connected Client
Relationship
Whether the 
Connected Client 
is a collective 
investment scheme 
which is not 
authorised by the 
SFC or is expected 
to hold the Offer 
Shares on behalf 
of such scheme
Number of 
Offer Shares to 
be allocated to 
the Connected 
Client(Note 1)
Approximate 
percentage of 
total number 
of Offer Shares 
under the Global 
Offering(Note 1)
Approximate 
percentage of 
total issued 
share capital 
after the Global 
Offering(Note 1)
4. 
It is proposed that GTJA Investments participates as placee to subscribe for the Offer Shares under the 
International Offering (the “GTJAI Subscription”). GTJA Investments is a member of the same group of 
companies as GTJA Securities, a non-syndicate broker, and is considered as a connected client of GTJA 
Securities pursuant to paragraph 1B(7) of the Placing Guidelines. In relation to the GTJAI Subscription, 
GTJA Investments shall hold the Offer Shares for hedging purpose as the single underlying asset of several 
sets of back-to-back total return swap transaction (the “GTHT Back-to-back TRS”) to be entered into 
between GTJA Investments and Guotai Haitong Securities Co., Ltd. (the “GTHT Onshore Parent”) in 
connection with several total return swap orders (the “GTHT Client TRS”) to be entered into by GTHT 
Onshore Parent and several ultimate clients (the “GTHT Onshore Ultimate Clients”), respectively. Such 
GTHT Client TRS is to be fully funded by the GTHT Onshore Ultimate Clients. GTJA Investments will 
hold the Offer Shares on a non-discretionary basis for the purpose of hedging the economic exposure under 
the GTHT Back-to-back TRS and GTHT Client TRS only. During the tenor of the GTHT Client TRS, all 
economic returns of the Offer Shares will be passed to the GTHT Onshore Ultimate Clients and all economic 
losses shall be borne by the GTHT Onshore Ultimate Clients, subject to the terms and conditions of the 
GTHT Back-to-back TRS and GTHT Client TRS, and GTJA Investments will not take part in any economic 
return or bear any economic loss in relation to the price of the Offer Shares. The GTHT Onshore Ultimate 
Clients may request to redeem the Offer Shares at their own discretion, upon which GTJA Investments 
shall dispose of the Offer Shares and settle the GTHT Back-to-back TRS and GTHT Client TRS in cash in 
accordance with the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS documents. 
Due to its internal policy, GTJA Investments will not exercise the voting right attaching to the Offer Shares 
during the tenor of the GTHT Back-to-back TRS and GTHT Client TRS.
To the best knowledge, information and belief of GTJA Investments after due enquiry, the GTHT Onshore 
Ultimate Clients and their respective ultimate beneficial owners holding 30% or more interest include:
Name of GTHT Onshore Ultimate Clients
Limited Partner/
Shareholders holding 
30% or more in the 
GTHT Onshore 
Ultimate Clients
深圳市前海瀚融私募證券基金管理有限公司(Shenzhen Qianhai Hanrong 
Private Equity Securities Fund Management Co., Ltd.), whose capacity is an 
investor, instead of a fund manager
林光亮(Lin Guangliang)
衛寧啟航 1 號私募證券投資基金
(Weining Qihang No. 1 Private Securities Investment Fund)
劉育濤(Liu Yutao)
衛寧聚焦私募證券投資基金
(Weining Jujiao Private Securities Investment Fund)
NA
衛寧聚焦私募證券投資基金
(Weining Jujiao Private Securities Investment Fund)
NA
中金金嘉 1 號集合資產管理計劃
(CICC Jinjia No.1 Collective Asset Management Plan)
NA
鹿秀馴鹿 25 號私募證券投資基金
(Roadshow Xunlu No.25 Private Equity Investment Fund)
王孟榮(Wang Mengrong)
銀萬全盈 70 號私募證券投資基金
(Yinwan Quanying No.70 Private Securities Investment Fund)
陳淩(Ling Chen)
銀萬全盈 70 號私募證券投資基金
(Yinwan Quanying No.70 Private Securities Investment Fund)
費斌(Bin Fei)

<<<PAGE 22>>>
22
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
Potential investors should read the Prospectus dated February 27, 2026 issued by Shenzhen 
Zhaowei Machinery & Electronics Co., Ltd. for detailed information about the Global Offering 
described below before deciding whether or not to invest in the Shares thereby being offered.
* 
Potential investors of the Offer Shares should note that the Joint Sponsors, the Sponsor-Overall Coordinators 
(for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations 
under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the 
events set out in the paragraph headed “Underwriting – Underwriting Arrangements and Expenses – Hong 
Kong Public Offering – Hong Kong Underwriting Agreement – Grounds for Termination” in the Prospectus 
at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
March 9, 2026).
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering, the number of the H Shares to be held 
by the public represents approximately 10% of the total issued share capital of the Company, the 
Company will therefore satisfy the public float requirement as required under Rule 19A.13A(2)(a) 
of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the H Shares of the Company at the time of Listing. Based on the 
final Offer Price of HK$71.28 per H Share, the Company satisfies the free float requirement under 
Rule 8.08A (as amended and replaced by Rule 19A.13C) of the Listing Rules.

<<<PAGE 23>>>
23
The Directors confirm that, immediately following completion of the Global Offering: (i) the 
Shares will be held by at least 300 Shareholders at the time of Listing, in compliance with Rule 
8.08(2) of the Listing Rules; (ii) the three largest public Shareholders will not hold more than 
50% of the H Shares held in public hands at the time of Listing, in compliance with Rules 8.08(3) 
and 8.24 of the Listing Rules; (iii) no placee will, individually, be placed more than 10% of the 
enlarged issued share capital of the Company immediately after the Global Offering; and (iv) there 
will not be any new substantial Shareholder (as defined in the Listing Rules) immediately after the 
Global Offering.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Monday, March 9, 
2026 (Hong Kong time), provided that the Global Offering has become unconditional and the right 
of termination described in the section headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has not been 
exercised. Investors who trade the H Shares on the basis of publicly available allocation details 
prior to the receipt of H Share certificates or prior to the H Share certificates becoming valid 
evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Monday, 
March 9, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Monday, March 9, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 100 H Shares each, and the stock code of the H Shares will 
be 2692.
By Order of the Board
Shenzhen Zhaowei Machinery & Electronics Co., Ltd.
Mr. Li Haizhou
Chairman of the Board and Executive Director
Hong Kong, March 6, 2026
As of the date of this announcement, the Board comprises (i) Mr. Li Haizhou, Ms. Xie Yanling, 
Mr. Ye Shubing and Mr. Li Ping as executive directors, (ii) Mr. Lu Zhiqiang as an employee 
representative director and (iii) Ms. Guo Xinmei, Dr. Zhou Changjiang and Mr. Lin Sen as 
independent non-executive directors.
