# 配发结果公告抽取任务：2726.HK Epiworld International Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**27/03/2026 19:46**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0327/2026032702128.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2726.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same meanings as those 
defined in the Hong Kong prospectus dated March 20, 2026 (the “Prospectus”) of Epiworld International Co., Ltd. (瀚
天天成電子科技(廈門)股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for any securities. This announcement is not a prospectus. Potential investors should read the Prospectus 
for detailed information about the Global Offering described below before deciding whether or not to invest in 
the Offer Shares. Any investment decision in relation to the Offer Shares should be taken solely in reliance on the 
information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities 
in the United States or in any other jurisdictions. The securities mentioned herein have not been, and will not be, 
registered under the United States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) 
or securities law of any state or other jurisdiction of the United States. The securities may not be offered, sold, 
pledged or otherwise transferred within the United States or to, or for the account or benefit of US persons (as defined 
in Regulation S), except in transactions exempt from, or not subject to, the registration requirements of the U.S. 
Securities Act. The securities may be offered, sold or delivered only outside the United States in offshore transactions 
in reliance on Regulation S.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to term and conditions set out in 
the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not 
resident in Hong Kong. Potential investors of the Offer Shares should note that the Sole Sponsor and Sponsor-Overall 
Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting — Underwriting Arrangements and Expenses — The Hong Kong Public Offering — Hong Kong 
Underwriting Agreement — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. on the Listing 
Date (which is currently expected to be on Monday, March 30, 2026).

<<<PAGE 2>>>
2
Epiworld International Co., Ltd.
瀚天天成電子科技( 廈門) 股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the Global 
Offering
:
21,492,050 H Shares
Number of Hong Kong Offer Shares
:
2,149,250 H Shares
Number of International Offer Shares
:
19,342,800 H Shares
Final Offer Price
:
HK$76.26 per H Share, plus brokerage 
 of 1.0%, SFC transaction levy 
 of 0.0027%, AFRC transaction levy 
 of 0.00015% and Stock Exchange 
 trading fee of 0.00565%
Nominal Value
:
RMB1.00 per H Share
Stock Code
:
2726
Sole Sponsor, Sponsor-Overall Coordinator, Overall Coordinator,
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Joint Global Coordinators, Joint Bookrunners, Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
Epiworld International Co., Ltd.
瀚天天成電子科技( 廈門) 股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated March 20, 2026 (the “Prospectus”) issued by 
Epiworld International Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
H Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
2726
Stock short name
EPIWORLD
Dealings commencement date
March 30, 2026#
# 
see note at the end of the announcement
Price Information
Final Offer Price
HK$76.26
Maximum Offer Price
HK$76.26
Offer Shares and Share Capital
Number of Offer Shares
21,492,050
Final Number of Offer Shares in 
 Hong Kong Public Offering
2,149,250
Final Number of Offer Shares in 
 International Offering
19,342,800
Number of issued Shares upon Listing
425,584,810
Over-allocation
No. of Offer Shares over-allocated
0
Note: There is no over-allotment option in the International Offering, and no stabilization activities will be carried out 
in relation to the Global Offering.

<<<PAGE 4>>>
4
Proceeds
Gross proceeds (Note)
HK$1,640.0 million
Less: Estimated listing expenses 
 payable based on the Final Offer Price
HK$(80.5) million
Net proceeds
HK$1,559.5 million
Note: Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
45,084
No. of successful applications
13,260
Subscription level
50.66 times
Claw-back triggered
N/A
No. of Offer Shares initially available 
 under the Hong Kong Public Offering
2,149,250
Final no. of Offer Shares under 
 the Hong Kong Public Offering
2,149,250
Number of Offer Shares reallocated 
 from International Offering 
 to Hong Kong Public Offering
0
% of Offer Shares under the Hong Kong 
 Public Offering to the Global Offering
10%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can refer to www.eipo.
com.hk/eIPOAllotment to perform a search by identification number or www.eipo.com.hk/eIPOAllotment for 
the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
120
Subscription Level
1.95 times
No. of Offer Shares initially available 
 under the International Offering
19,342,800
Final no. of Offer Shares under 
 the International Offering
19,342,800
% of Offer Shares under the International 
 Offering to the Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for a 
consent under Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to 
allocate certain Offer Shares in the International Offering to close associate of certain existing 
minority Shareholders, (i) none of the Offer Shares subscribed by the placees and the public have 
been financed directly or indirectly by the Company, any of the Directors, Supervisors, chief 
executive of the Company, substantial shareholders, existing shareholders of the Company or any 
of its subsidiaries or their respective close associates; and (ii) none of the placees and the public 
who have purchased the Offer Shares are accustomed to taking instructions from the Company, any 
of the Directors, Supervisors, chief executive of the Company, substantial shareholders, existing 
shareholders of the Company or any of its subsidiaries or their respective close associates in 
relation to the acquisition, disposal, voting or other disposition of Shares registered in his/her/its 
name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investor
Investor
No. of
Offer 
Shares 
allocated
Approximate 
% of 
Offer Shares
Approximate 
% of total
 issued H 
Shares after
 the Global 
Offering
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering
Existing 
Shareholders 
or their close 
associates
Xiamen Advanced Intelligent Manufacturing Industry Investment 
 Limited (廈門先進智造產業投資有限公司)
10,058,500
46.80%
8.46%
2.36%
Yes

<<<PAGE 6>>>
6
Allotee with Waiver/Consent Obtained
Investor
No. of 
Offer 
Shares 
allocated
% of Offer 
Shares
% of total 
issued H 
Shares after 
the Global 
Offering
% of total 
issued share 
capital in the 
Company after 
the Global 
Offering
Relationship
Allotees with consent under paragraph 1C(2) of the Placing Guidelines in relation to allocations to close associate of certain existing shareholders as cornerstone 
investor Note 1
Xiamen Advanced Intelligent Manufacturing Industry Investment 
 Limited (廈門先進智造產業投資有限公司)
10,058,500
46.80%
8.46%
2.36%
A cornerstone 
investor and 
close associate 
of existing 
shareholders
Notes:
1. 
For details of the consent under paragraph 1C(2) of the Placing Guidelines in relation to allocations to existing 
shareholder, please refer to the section headed “Waiver and Consent in Relation to the Subscription for H Shares 
by Close Associates of Minority Existing Shareholders as Cornerstone Investor” in the Prospectus.
LOCK-UP UNDERTAKINGS
Single Largest Shareholder
Name
Number of 
shares held in 
the Company 
subject to lock-up 
undertakings 
upon Listing
% of 
shareholding 
in the Company 
subject to lock-up 
undertakings 
upon Listing
Last day 
subject to 
the lock-up 
undertakings
Dr. Zhao
116,560,399
27.39%
March 29, 2027 Note 1
Notes:
1. 
The expiry day of the lock-up period shown in the table above is pursuant to the PRC Company Law.

<<<PAGE 7>>>
7
Pre-IPO Investors
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding 
in the Company 
subject to 
lock-up 
undertakings 
upon Listing
Last day 
subject to 
the lock-up 
undertakings
Xike Zhongheng
56,749,358
13.33%
March 29, 
2027 Note 1
Li Qinghua (李慶華)
27,019,903
6.35%
March 29, 
2027 Note 1
Xincheng Zhongchuang
16,503,914
3.88%
March 29, 
2027 Note 1
Hubble Technology
16,292,350
3.83%
March 29, 
2027 Note 1
Xiamen Hongyuan
16,106,360
3.78%
March 29, 
2027 Note 1
Xiamen Spark
2,034,697
0.48%
March 29, 
2027 Note 1
Xiamen Hongxing
150,568
0.04%
March 29, 
2027 Note 1
Epiworld Core
15,968,888
3.75%
March 29, 
2027 Note 1
Hainan Zhentai
15,481,611
3.64%
March 29, 
2027 Note 1
China Resources Microelectronics
10,861,566
2.55%
March 29, 
2027 Note 1
Huangshan Saifu
10,225,966
2.40%
March 29, 
2027 Note 1
Puyuan Pengyuan
9,807,526
2.30%
March 29, 
2027 Note 1
Chen Yinfei (陳音飛)
9,527,146
2.24%
March 29, 
2027 Note 1
Ningbo Fuchi
9,503,871
2.23%
March 29, 
2027 Note 1
Xiamen Jushenghua
6,788,479
1.60%
March 29, 
2027 Note 1

<<<PAGE 8>>>
8
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding 
in the Company 
subject to 
lock-up 
undertakings 
upon Listing
Last day 
subject to 
the lock-up 
undertakings
Shanghai Tianli
6,787,150
1.59%
March 29, 
2027 Note 1
Zhang Minghua (張明華)
6,015,215
1.41%
March 29, 
2027 Note 1
Huiyou Chuangjia
5,430,783
1.28%
March 29, 
2027 Note 1
Dangfeng Technology
4,768,336
1.12%
March 29, 
2027 Note 1
Xiamen Hi-Tech Investment
3,810,858
0.90%
March 29, 
2027 Note 1
Torch Capital
2,381,872
0.56%
March 29, 
2027 Note 1
Chantou Juxiang Xinhan
2,778,751
0.65%
March 29, 
2027 Note 1
Xiamen Gongrong Industry
3,087,501
0.73%
March 29, 
2027 Note 1
Xiamen Chantou Gongrong
3,087,501
0.73%
March 29, 
2027 Note 1
ICBC Investment
6,946,878
1.63%
March 29, 
2027 Note 1
Wangrui Hancheng
2,424,557
0.57%
March 29, 
2027 Note 1
Ningbo Qiaowang
2,381,701
0.56%
March 29, 
2027 Note 1
Jiangyin Yinrun
980,736
0.23%
March 29, 
2027 Note 1
Huzhou Runxu
478,739
0.11%
March 29, 
2027 Note 1
Saifu Jinzuan
2,556,491
0.60%
March 29, 
2027 Note 1
Liaoning Haitong
1,887,453
0.44%
March 29, 
2027 Note 1

<<<PAGE 9>>>
9
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding 
in the Company 
subject to 
lock-up 
undertakings 
upon Listing
Last day 
subject to 
the lock-up 
undertakings
Hefei Tiancheng
1,800,000
0.42%
March 29, 
2027 Note 1
Qingda Runyu
1,282,501
0.30%
March 29, 
2027 Note 1
Qingda Xinsheng
1,005,114
0.24%
March 29, 
2027 Note 1
Shanghai Zhezhong
1,258,302
0.30%
March 29, 
2027 Note 1
Dongzheng Ruikun
840,630
0.20%
March 29, 
2027 Note 1
Qingyue Jingfu
794,500
0.19%
March 29,
2027 Note 1
Ningbo Fuwurong
476,357
0.11%
March 29, 
2027 Note 1
Jiadong Wuyuan
476,357
0.11%
March 29, 
2027 Note 1
Shanghai Minshenshi
463,125
0.11%
March 29, 
2027 Note 1
Huajin Mingjiade
154,375
0.04%
March 29, 
2027 Note 1
Huajin Yuxing
154,375
0.04%
March 29, 
2027 Note 1
Subtotal
287,532,361
67.57%
Notes:
1. 
The expiry day of the lock-up period shown in the table above is pursuant to the PRC Company Law.

<<<PAGE 10>>>
10
Cornerstone Investor
Name
Number of
 shares held in 
the Company 
subject to lock-up 
undertakings 
upon Listing
% of total 
Offer Shares
% of 
shareholding
 in the Company 
subject to 
lock-up 
undertakings 
upon Listing
Last day 
subject to 
the lock-up 
undertakings
Xiamen Advanced Intelligent Manufacturing Industry Investment Limited 
 (廈門先進智造產業投資有限公司)
10,058,500
46.80%
2.36%
September 29,
 2027 Note 1
Notes:
1. 
In accordance with the cornerstone investment agreement, the required lock-up period ends on September 
29, 2027. The Cornerstone Investor will cease to be prohibited from disposing of or transferring H Shares 
subscribed pursuant to the relevant cornerstone investment agreement after the indicated date.
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
Number of 
H Shares 
held upon 
Listing
Number of 
H Shares 
held upon 
Listing as % 
of total issued 
share capital 
upon Listing
Top 1
10,058,500
52.0013%
46.8010%
12,190,714
2.8645%
Top 5
12,224,050
63.1969%
56.8771%
14,356,264
3.3733%
Top 10
13,913,600
71.9317%
64.7384%
16,045,814
3.7703%
Top 25
16,878,450
87.2596%
78.5335%
19,010,664
4.4670%
* 
Ranking of placees is based on the number of Offer Shares allotted to the placees.
H SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares allotted
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
H Shares held 
upon Listing 
as % of total 
issued H share 
capital upon 
Listing
Number 
of Shares 
held upon 
Listing
Top 1
–
0.0000%
0.0000%
29,746,239 
25.0129%
116,560,399 
Top 5
10,058,500
52.0013%
46.8010%
71,578,154 
60.1883%
262,617,797 
Top 10
10,058,500
52.0013%
46.8010%
88,944,651 
74.7914%
331,448,178 
Top 25
11,838,550
61.2039%
55.0834%
108,187,523
90.9723%
407,088,732
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholder upon Listing.

<<<PAGE 11>>>
11
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number of 
H Shares allotted
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
Number of 
Shares held 
upon Listing 
as % of total 
issued share 
capital upon 
Listing
Top 1
–
0.0000%
0.0000%
29,746,239
116,560,399
27.3883%
Top 5
10,058,500
52.0013%
46.8010%
71,578,154
262,617,797
61.7075%
Top 10
10,058,500
52.0013%
46.8010%
88,944,651
331,448,178
77.8806%
Top 25
10,058,500
52.0013%
46.8010%
106,983,303
410,791,541
96.5240%
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 45,084 valid 
applications made by the public will be conditionally allocated on the basis set out below:
NO. OF 
SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE 
ALLOTTED
OF THE TOTAL 
NO. OF
SHARES 
APPLIED FOR
POOL A
50
19,798 3,960 out of 19,798 to receive 50 Shares
20.00%
100
11,582 2,432 out of 11,582 to receive 50 Shares
10.50%
150
856 187 out of 856 to receive 50 Shares
7.28%
200
1,241 273 out of 1,241 to receive 50 Shares
5.50%
250
690 152 out of 690 to receive 50 Shares
4.41%
300
375 84 out of 375 to receive 50 Shares
3.73%
350
215 51 out of 215 to receive 50 Shares
3.39%
400
275 73 out of 275 to receive 50 Shares
3.32%
450
220 65 out of 220 to receive 50 Shares
3.28%
500
1,583 507 out of 1,583 to receive 50 Shares
3.20%
600
2,408 910 out of 2,408 to receive 50 Shares
3.15%
700
289 125 out of 289 to receive 50 Shares
3.09%
800
291 135 out of 291 to receive 50 Shares
2.90%
900
617 312 out of 617 to receive 50 Shares
2.81%
1,000
1,163 629 out of 1,163 to receive 50 Shares
2.70%
1,500
529 413 out of 529 to receive 50 Shares
2.60%
2,000
295 50 Shares
2.50%
2,500
230 50 Shares plus 31 out of 230 to receive additional 50 Shares
2.27%
3,000
171 50 Shares plus 61 out of 171 to receive additional 50 Shares
2.26%

<<<PAGE 12>>>
12
3,500
103 50 Shares plus 59 out of 103 to receive additional 50 Shares
2.25%
4,000
122 50 Shares plus 96 out of 122 to receive additional 50 Shares
2.23%
4,500
81 100 Shares
2.22%
5,000
202 100 Shares plus 32 out of 202 to receive additional 50 Shares
2.16%
6,000
120 100 Shares plus 70 out of 120 to receive additional 50 Shares
2.15%
7,000
70 150 Shares
2.14%
8,000
65 150 Shares plus 15 out of 65 to receive additional 50 Shares
2.02%
9,000
82 150 Shares plus 51 out of 82 to receive additional 50 Shares
2.01%
10,000
441 200 Shares
2.00%
20,000
212 350 Shares
1.75%
30,000
107 500 Shares
1.67%
40,000
69 550 Shares
1.38%
50,000
255 650 Shares
1.30%
44,757 Total number of Pool A successful applicants: 12,933
POOL B
100,000
244 2,250 Shares
2.25%
200,000
27 3,250 Shares
1.63%
300,000
17 4,350 Shares
1.45%
400,000
9 5,250 Shares
1.31%
500,000
2 6,300 Shares
1.26%
600,000
4 7,200 Shares
1.20%
700,000
1 8,250 Shares
1.18%
800,000
1 9,200 Shares
1.15%
900,000
1 10,000 Shares
1.11%
1,074,600
21 11,800 Shares
1.10%
327 Total number of Pool B successful applicants: 327
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and Stock Exchange trading fee payable.

<<<PAGE 13>>>
13
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
States.
The Offer Shares are being offered and sold outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated March 20, 2026 issued by Epiworld International Co., 
Ltd. for detailed information about the Global Offering described below before deciding whether 
or not to invest in the H Shares thereby being offered.
* 
Potential investors of the Offer Shares should note that the Sole Sponsor and the Sponsor-
Overall Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing 
Date (which is currently expected to be on Monday, March 30, 2026).
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering, 64,109,097 H Shares, representing 
approximately 15.06% of the issued share capital of our Company will count towards the public 
float. Therefore, the number of H shares held in public hands is higher than the prescribed 
percentage of H Shares required to be held in public hands of 13.87% under Rule 19A.13A(1) 
of the Listing Rules, satisfying the minimum percentage requirement in compliance with Rule 
19A.13A(1) of the Listing Rules.
Pursuant to PRC Company Law, all of the Shares issued by our Company prior to the Global 
Offering will be subject to a lock-up period of one year from the Listing Date. Therefore, all 
Shares held by our existing Shareholders upon the Listing shall not be counted towards the free 
float. The Cornerstone Investor has agreed to a lock-up period of 18 months following the Listing 
Date. As such, H Shares held by the Cornerstone Investor upon the Listing shall not be counted 
towards the free float of the H Shares of the Company at the time of Listing. Based on the Offer 
Price of HK$76.26 per H Share, 11,433,550 H Shares with an expected market capitalization of 
approximately HK$871.9 million, which is higher than HK$600 million under Rule 19A.13C, will 
not be subject to any disposal restrictions (whether under contract, the Listing Rules, applicable 
laws or otherwise) at the time of the Listing. Therefore, the Company satisfies the free float 
requirement under Rule 19A.13C(1)(b) of the Listing Rules.

<<<PAGE 14>>>
14
The Directors confirm that, immediately following completion of the Global Offering: (i) the 
Shares will be held by at least 300 Shareholders at the time of Listing, in compliance with Rule 
8.08(2) of the Listing Rules; (ii) the three largest public Shareholders will not hold more than 
50% of the H Shares held in public hands at the time of Listing, in compliance with Rules 8.08(3) 
and 8.24 of the Listing Rules; (iii) no placee will, individually, be placed more than 10% of the 
enlarged issued share capital of the Company immediately after the Global Offering; and (iv) there 
will not be any new substantial Shareholder (as defined in the Listing Rules) immediately after the 
Global Offering.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. (Hong Kong time) 
on Monday, March 30, 2026, provided that (i) the Global Offering has become unconditional 
in all respects, and (ii) the right of termination described in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – The Hong Kong Public Offering – Hong Kong 
Underwriting Agreement – Grounds for termination” in the Prospectus has not been exercised. 
Investors who trade H Shares prior to the receipt of H Share certificates or the H Share certificates 
becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong Kong time) 
on Monday, March 30, 2026, it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. (Hong Kong time) on Monday, March 30, 2026. The H Shares will be 
traded in board lots of 50 H Shares each and the stock code of the H Shares will be 2726.
By order of the Board
Epiworld International Co., Ltd.
Dr. ZHAO Jianhui
Chairman of the Board and executive director
Hong Kong, March 27, 2026
As at the date of this announcement, Directors of the Company are: (i) Dr. ZHAO Jianhui, Ms. 
PAN Menghan and Ms. BAI Liting as executive directors; (ii) Mr. SU Ping, Mr. FANG Wei and 
Ms. XIE Jieping as non-executive directors; and (iii) Dr. KANG Junyong, Dr. SU Xinlong and Dr. 
LIAO Yi as independent non-executive directors.
