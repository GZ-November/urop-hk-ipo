# 配发结果公告抽取任务：3625.HK Shanghai FourSemi Semiconductor Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**30/03/2026 22:33**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0330/2026033003564.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3625.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
– 1 –
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock 
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for 
the contents of this announcement, make no representation as to its accuracy or completeness and expressly 
disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings 
as those defined in the prospectus dated Monday, March 23, 2026 (the “Prospectus”) of Shanghai FourSemi 
Semiconductor Co., Ltd. (上海傅里葉半導體股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an offer or an invitation to 
induce an offer by any person to acquire, purchase or subscribe for any of the securities of the Company. This 
announcement is not a prospectus. Potential investors should read the Prospectus for detailed information 
about the Global Offering described below before deciding whether or not to invest in the Offer Shares. 
Any investment decision in relation to the Offer Shares should be taken solely in reliance on the information 
provided in the Prospectus.
This announcement does not constitute an offer to sell or the solicitation of an offer to buy nor shall there be 
any sale of Offer Shares in any jurisdiction in which such offer, solicitation or sales would be unlawful. This 
announcement is not for release, publication or distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia) or any 
other jurisdiction where such distribution is prohibited by law, nor is this announcement an offer for sale or 
solicitation to purchase or subscribe for securities in the United States or any other jurisdictions. The Offer 
Shares have not been, and will not be, registered under the United States Securities Act of 1933, as amended 
from time to time (the “U.S. Securities Act”), or any applicable state securities laws, and may not be offered, 
sold, pledged or transferred within the United States or to, or for the account or benefit of, U.S. persons (as 
defined in Regulation S under the U.S. Securities Act (the “Regulation S”)) except in transactions exempt 
from, or not subject to, the registration requirements of the U.S. Securities Act. The Offer Shares are being 
offered and sold outside the United States in offshore transactions in accordance with Regulation S. There 
will be no public offering of the Offer Shares in the United States.
No stabilizing manager will be appointed, and it is anticipated that no stabilization activities will be carried 
out in relation to the Global Offering. 
Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate 
their obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence 
of any of the events set out in the section headed “Underwriting — Underwriting Arrangements and Expenses 
— Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. 
(Hong Kong time) on the Listing Date (which is currently expected to be on Tuesday, March 31, 2026).

<<<PAGE 2>>>
– 2 –
Shanghai FourSemi Semiconductor Co., Ltd.
上海傅里葉半導體股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under
the Global Offering
:
12,000,000 H Shares
Number of Hong Kong Offer Shares
:
2,400,000 H Shares (as adjusted after 
reallocation)
Number of International Offer Shares
:
9,600,000 H Shares (as adjusted after 
reallocation)
Final Offer Price
:
HK$40 per H Share, plus brokerage 
of 1.0%, SFC transaction levy of 
0.0027%, AFRC transaction levy of 
0.00015% and Stock Exchange trading 
fee of 0.00565%
Nominal value
:
RMB1.00 per H Share
Stock code
:
3625
Joint Sponsors, Joint Sponsor-Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Joint Bookrunner and Joint Lead Manager
Joint Bookrunners

<<<PAGE 3>>>
– 3 –
SHANGHAI FOURSEMI SEMICONDUCTOR CO., LTD.
上海傅里葉半導體股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, Shareholders and prospective investors should be aware that the price 
of the H Shares could move substantially even with a small number of H Shares 
traded and should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
3625
Stock short name
FOURSEMI
Dealings commencement date
March 31, 2026*
*see note at the end of the announcement
Price Information
Final Offer Price
HK$40.00
Offer Price Range
HK$40.00–HK$50.00
Offer Shares and Share Capital
Number of Offer Shares
12,000,000
Final Number of Offer Shares in Public Offer (after 
reallocation)
2,400,000
Final Number of Offer Shares in International Offer 
(after reallocation)
9,600,000
Number of issued shares upon Listing
112,000,000

<<<PAGE 4>>>
– 4 –
Over-allocation
No. of Offer Shares over-allocated
0
Note: There has been no over-allocation of Offer Shares in the International Placing. Therefore, the 
Over-allotment Option will not be exercised.
Proceeds
Gross proceeds Note
HK$480.0 million
Less: Estimated listing expenses payable based on Final 
Offer Price
HK$(57.3) million
Net proceeds
HK$422.7 million
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of 
the use of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the 
Prospectus.
ALLOTMENT RESULTS DETAILS
PUBLIC OFFER
No. of valid applications
118,537
No. of successful applications
18,405
Subscription level
3,118.43 times
Claw-back triggered
Yes
No. of Offer Shares initially available under the Public Offer
600,000
No. of Offer Shares reallocated from the International Offer 
(clawback)
1,800,000
Final no. of Offer Shares under the Public Offer (after 
reallocation)
2,400,000
% of Offer Shares under the Public Offer to the Global 
Offering
20.00%
Note: For details of the final allocation of H Shares to the Public Offer, investors can refer to 
www.eipo.com.hk/eIPOAllotment to perform a search by identification number or www.eipo.com.hk/
eIPOAllotment for the full list of allottees.

<<<PAGE 5>>>
– 5 –
INTERNATIONAL OFFER
No. of placees
100
Subscription Level
2.93 times
No. of Offer Shares initially available under the International 
Offer
11,400,000
No. of Offer Shares reallocated to the Public Offer (claw-back)
1,800,000
Final no. of Offer Shares under the International Offer (after 
reallocation)
9,600,000
% of Offer Shares under the International Offer to the Global 
Offering
80.00%
The Directors confirm that, to the best of their knowledge, information and belief, (i) none 
of the Offer Shares subscribed by the placees and the public have been financed directly or 
indirectly by the Company, any of the Directors, chief executive of the Company, Controlling 
Shareholders, substantial Shareholders, existing Shareholders of the Company or any of 
its subsidiaries or their respective close associates; and (ii) none of the placees and the 
public who have purchased the Offer Shares are accustomed to taking instructions from the 
Company, any of the Directors, chief executive of the Company, Controlling Shareholders, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries 
or their respective close associates in relation to the acquisition, disposal, voting or other 
disposition of H Shares registered in his/her/its name or otherwise held by him/her/it.

<<<PAGE 6>>>
– 6 –
LOCK-UP UNDERTAKINGS
Key Persons (as defined under Rule 18C.14 of the Listing Rules)
Name
Capacity
Total number 
of Shares held 
in the Company 
subject to lock-
up undertakings 
upon Listing
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
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
the Company 
subject to lock-
up undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings 
Note 1
Xu Xiaolin (徐小林) 
(“Mr. Xu”)
Founder, chairman of the 
Board, executive Director and 
president
8,859,800
8,859,800
7.99%
7.91%
March 30, 2027
Liu Baoliang (劉保良) 
(“Mr. Liu”)
Co-founder, executive Director, 
vice president, director of 
algorithm applications and core 
R&D team member
2,518,500
2,518,500
2.27%
2.25%
March 30, 2027
S h a n g h a i F o u r S e m i 
Management Consulting 
Partnership (Limited 
Partnership) (上海傅里葉管
理諮詢合夥企業(有限合夥)) 
Note 2 (“Shanghai FourSemi 
Management”)
Employee shareholding 
platform controlled by Mr. Xu
12,617,800
12,617,800
11.38%
11.27%
March 30, 2027
X i a m e n F o u r S e m i 
Enterprise Management 
Consulting Partnership 
(Limited Partnership) 
(廈門傅里葉企業管理諮
詢合夥企業( 有限合夥) ) 
Note 2 (“Xiamen FourSemi 
Management”)
Employee shareholding 
platform controlled by Mr. Xu
7,073,700
7,073,700
6.38%
6.32%
March 30, 2027

<<<PAGE 7>>>
– 7 –
Name
Capacity
Total number 
of Shares held 
in the Company 
subject to lock-
up undertakings 
upon Listing
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
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
the Company 
subject to lock-
up undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings 
Note 1
Xiamen FourSemi Chuangke 
Enterprise Management 
Consulting Partnership 
(Limited Partnership) (廈
門傅里葉創科企業管理
諮詢合夥企業(有限合夥)) 
Note 2 (“Xiamen FourSemi 
Chuangke”)
Employee shareholding 
platform controlled by Mr. Xu
4,206,100
4,206,100
3.79%
3.76%
March 30, 2027
Subtotal
35,275,900
35,275,900
31.81%
31.50%
Notes:
1.	
The lock-up period commencing on the date by reference to which disclosure of its shareholding is 
made in the Prospectus and ending on the date which is 12 months from the Listing Date, i.e. March 
30, 2027.
2.	
As of the Latest Practicable Date, each of Shanghai FourSemi Management, Xiamen FourSemi 
Management and Xiamen FourSemi Chuangke was controlled by Mr. Xu as the general partner. 
Therefore, each of Shanghai FourSemi Management, Xiamen FourSemi Management and Xiamen 
FourSemi Chuangke is a close associate of Mr. Xu under the Listing Rules and is subject to the lock-
up requirements pursuant to Rule 18C.14 of the Listing Rules.
Certain limited partners of Shanghai FourSemi Management, Xiamen FourSemi Management and 
Xiamen FourSemi Chuangke, namely Mr. Qian Shun, Mr. Liu, Mr. Shi Hongxiao, Mr. He Xiuan, Mr. 
Yang Xiaoming, Mr. Liu Yanhai and Mr. Zhu Huaping, are also key persons under Rule 18C.14 of the 
Listing Rules and shall be subject to a lock-up period commencing from the date of the Prospectus 
and ending on expiry of 12 months from the Listing Date. They undertake that they will not dispose 
of their interests in the above partnerships within the aforementioned lock-up period. Except for Mr. 
Liu, being a member of the Controlling Shareholders, the abovementioned limited partners have no 
direct shareholding interests in the Company. 
Pursuant to the respective partnership agreement of Shanghai FourSemi Management, Xiamen 
FourSemi Management and Xiamen FourSemi Chuangke, any transfer of partnership interest by 
limited partners shall be approved by the general partner, Mr. Xu and the majority of the limited 
partners. Mr. Xu as the general partner of the aforementioned three employee shareholding 
platforms will ensure that the lock-up restriction will be effectively enforced in respect of the indirect 
interests held by these key persons as limited partners.

<<<PAGE 8>>>
– 8 –
Pathfinder SIIs
Name
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings
upon Listing
Number of 
H Shares held in
the Company 
subject to lock-up 
undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings 
upon Listing Note1
% of shareholding 
in the Company 
subject to lock-up 
undertakings 
upon Listing Note 1
Last day subject 
to the lock-up 
undertakings Note 2
Shanghai Moqin Intelligent 
Technology Co., Ltd. (上海摩勤智能
技術有限公司)
6,361,400
6,361,400
5.74%
5.68%
March 30, 2027
Shenzhen Fortune Chuanghong 
Private Equity Investment Enterprise 
(Limited Partnership) (深圳市達晨創
鴻私募股權投資企業(有限合夥))
4,696,800
4,696,800
4.24%
4.19%
March 30, 2027
Shenzhen Caizhi Chuangying Private 
Equity Investment Enterprise 
(Limited Partnership) (深圳市財智創
贏私募股權投資企業(有限合夥))
221,300
221,300
0.20%
0.20%
March 30, 2027
Shaoxing Gansheng Equity 
Investment Partnership (Limited 
Partnership) (紹興淦盛股權投資合夥
企業(有限合夥))
6,406,800
6,406,800
5.78%
5.72%
March 30, 2027
Wuxi Ark Investment Partnership 
(Limited Partnership) (無錫方舟投資
合夥企業(有限合夥)))
4,601,600
4,601,600
4.15%
4.11%
March 30, 2027
Subtotal
22,287,900
22,287,900
20.10%
19.90%
Note:
1.	
Each of the Shareholders listed in the above table is a pathfinder SII of the Company as 
defined under Chapter 2.5 of the Guide for New Listing Applicants. Please refer to the section 
headed“History and Corporate Structure – Capitalization of our Company” in the Prospectus for 
further details.
2.	
In accordance with Rule 18C.14(2) of the Listing Rules, the required lock–up period commences 
on the date by reference to which disclosure of its shareholding is made in the Prospectus and ends 
on the date which is six months from the Listing Date, i.e. September 30, 2026. In addition to the 
lock-up requirement under Rule 18C.14(2) of the Listing Rules, all existing Shareholders shall 
not dispose of any of the Shares held by them within the 12 months following the Listing Date, i.e. 
March 30, 2027, as required under the applicable PRC laws.

<<<PAGE 9>>>
– 9 –
Existing shareholders
Name Note 1
Number of 
Shares held in the 
Company subject to 
lock-up undertakings 
upon Listing
Number of 
H Shares held in the 
Company subject to 
lock-up undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings 
upon Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings Note 2
Shenzhen City Vinno Intelligent and 
Health Venture Investment Fund 
(Limited Partnership) (深圳市合創智
能及健康創業投資基金(有限合夥))
5,776,900
5,776,900
5.21%
5.16%
March 30, 2027
Xiamen Junyi Kaixiang Venture 
Capital Partnership (Limited 
Partnership) (廈門君翼凱翔創業投資
合夥企業 (有限合夥))
3,527,500
3,527,500
3.18%
3.15%
March 30, 2027
Shanghai Chaoyue Moore Equity 
Investment Fund Partnership 
(Limited Partnership) (上海超越摩爾
股權投資基金合夥企業 (有限合夥))
3,022,300
3,022,300
2.73%
2.70%
March 30, 2027
Jiaxing Junsheng Equity Investment 
Partnership (Limited Partnership) 
(嘉興君昇股權投資合夥企業 (有限合
夥))
2,921,500
2,921,500
2.63%
2.61%
March 30, 2027
Liu Changjiang (劉長江)
2,458,100
2,458,100
2.22%
2.19%
March 30, 2027
Shenzhen Zhanxiang Information 
Technology Co., Ltd. (深圳市展想信
息技術有限公司)
1,981,800
1,981,800
1.79%
1.77%
March 30, 2027
Beijing Xingtou Youxuan Venture 
Capital Fund (Limited Partnership) 
(北京興投優選創業投資基金 (有限合
夥))
1,850,300
1,850,300
1.67%
1.65%
March 30, 2027
Wentianxia Technological Group Co., 
Ltd. (聞天下科技集團有限公司)
1,687,300
1,687,300
1.52%
1.51%
March 30, 2027
Xiamen Weitai Shenghong Equity 
Investment Partnership (Limited 
Partnership) (廈門偉泰晟弘股權投資
合夥企業 (有限合夥))
1,680,000
1,680,000
1.52%
1.50%
March 30, 2027

<<<PAGE 10>>>
– 10 –
Name Note 1
Number of 
Shares held in the 
Company subject to 
lock-up undertakings 
upon Listing
Number of 
H Shares held in the 
Company subject to 
lock-up undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings 
upon Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings Note 2
Ningbo Junyi Borui Venture 
Investment Partnership (Limited 
Partnership)(寧波君翼博瑞創業投資
合夥企業 (有限合夥))
1,473,700
1,473,700
1.33%
1.32%
March 30, 2027
Xiamen Zhengchu Venture Capital 
Partnership (Limited Partnership) 
(廈門正儲創業投資合夥企業 (有限合
夥))
1,356,700
1,356,700
1.22%
1.21%
March 30, 2027
Shanghai Kuanlian Investment Co., 
Ltd. (上海寬聯投資有限公司)
1,322,800
1,322,800
1.19%
1.18%
March 30, 2027
Jiaxing Junqing Equity Investment 
Partnership (Limited Partnership) 
(嘉興君擎股權投資合夥企業 (有限合
夥))
1,302,300
1,302,300
1.17%
1.16%
March 30, 2027
Guangzhou Chufeng Equity 
Investment Partnership (Limited 
Partnership) (廣州初楓股權投資合夥
企業 (有限合夥))
1,222,700
1,222,700
1.10%
1.09%
March 30, 2027
H u z h o u Z h u o s h e n g E q u i t y 
Investment Partnership (Limited 
Partnership) (湖州卓昇股權投資合夥
企業 (有限合夥))
1,110,200
—
—
—
March 30, 2027
Tianjin Haihe Shunke Equity 
Investment Partnership (Limited 
Partnership) (天津海河順科股權投資
合夥企業 (有限合夥))
1,052,500
1,052,500
0.95%
0.94%
March 30, 2027
Jiang Yan (江燕)
950,000
950,000
0.86%
0.85%
March 30, 2027
S u z h o u Y a h e X i n g h u a 
Optoelectronics Industry Investment 
Partnership (Limited Partnership) 
(蘇州亞禾星華光電產業投資合夥 (有
限合夥))
906,700
906,700
0.82%
0.81%
March 30, 2027

<<<PAGE 11>>>
– 11 –
Name Note 1
Number of 
Shares held in the 
Company subject to 
lock-up undertakings 
upon Listing
Number of 
H Shares held in the 
Company subject to 
lock-up undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings 
upon Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings Note 2
Shenzhen Shunying Private Equity 
Investment Fund Partnership 
(Limited Partnership) (深圳順贏私募
股權投資基金合夥企業 (有限合夥))
747,100
747,100
0.67%
0.67%
March 30, 2027
Fujian Junxin Ruizhi Equity 
Investment Partnership (Limited 
Partnership) (福建珺信睿智股權投資
合夥企業 (有限合夥))
670,400
670,400
0.60%
0.60%
March 30, 2027
Suzhou Jicui Meibai Venture Capital 
Partnership (Limited Partnership) 
(蘇州集萃美柏創業投資合夥企業 (有
限合夥))
604,500
604,500
0.55%
0.54%
March 30, 2027
Shanghai Longcheer Smart 
Technology Co., Ltd. (上海龍旗智能
科技有限公司)
604,500
604,500
0.55%
0.54%
March 30, 2027
Suzhou Haisheng Xianting Industrial 
Investment Fund Partnership 
(Limited Partnership) (蘇州海晟閑庭
產業投資基金合夥企業(有限合夥))
576,900
576,900
0.52%
0.52%
March 30, 2027
Shanghai Fumiao Investment 
Management Partnership (Limited 
Partnership) (上海復淼投資管理合夥
企業(有限合夥))
560,500
560,500
0.51%
0.50%
March 30, 2027
Xiamen Innovation Xingke Equity 
Investment Partnership (Limited 
Partnership) (廈門創新興科股權投資
合夥企業(有限合夥))
555,100
555,100
0.50%
0.50%
March 30, 2027
Sanming Green Innovation 
Investment Partnership (Limited 
Partnership) (三明綠色創新投資合夥
企業 (有限合夥))
555,100
555,100
0.50%
0.50%
March 30, 2027

<<<PAGE 12>>>
– 12 –
Name Note 1
Number of 
Shares held in the 
Company subject to 
lock-up undertakings 
upon Listing
Number of 
H Shares held in the 
Company subject to 
lock-up undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings 
upon Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings Note 2
Quanzhou Huide Equity Investment 
Partnership (Limited Partnership) 
(泉州匯德股權投資合夥企業 (有限合
夥))
555,100
555,100
0.50%
0.50%
March 30, 2027
Jiaxing Shuimu Xinchi Venture 
Capital Partnership (Limited 
Partnership) (嘉興水沐芯馳創業投資
合夥企業 (有限合夥))
384,600
384,600
0.35%
0.34%
March 30, 2027
Furui Chuangxin (Xiamen) Emerging 
Industries Investment Partnership 
(Limited Partnership) (福睿創信（廈
門）新興產業投資合夥企業(有限合
夥))
383,900
383,900
0.35%
0.34%
March 30, 2027
Deng Tianshun (鄧天順)
336,000
336,000
0.30%
0.30%
March 30, 2027
N i n g b o Z h i y o u E n t e r p r i s e 
Management Partnership (Limited 
Partnership) (寧波志佑企業管理合夥
企業 (有限合夥))
181,300
181,300
0.16%
0.16%
March 30, 2027
Qingdao Xinda Venture Capital 
Center (Limited Partnership) (青島信
達普創投資中心(有限合夥))
117,900
117,900
0.11%
0.11%
March 30, 2027
Subtotal
42,436,200
41,326,000
37.27%
36.90%
Notes:
1.	
Please refer to the Prospectus for further details.
2.	
The expiry date of the lock–up period shown in the table above is pursuant to applicable PRC laws.

<<<PAGE 13>>>
– 13 –
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
as % of total 
Offer Shares
Number of 
Shares held 
upon Listing
% of 
total issued 
share capital 
upon Listing
Top 1
2,475,000
25.78%
20.63%
2,475,000
2.21%
Top 5
5,823,200
60.66%
48.53%
5,823,200
5.20%
Top 10
7,931,900
82.62%
66.10%
7,931,900
7.08%
Top 25
9,435,300
98.28%
78.63%
9,435,300
8.42%
Note:
*  Ranking of placees is based on the number of H Shares allotted to the placees.
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
% of total 
issued share 
capital upon 
Listing
Top 1
—
0.00%
0.00%
35,275,900
35,275,900
31.50%
Top 5
—
0.00%
0.00%
60,145,000
60,145,000
53.70%
Top 10
2,475,000
25.78%
20.63%
79,385,000
79,385,000
70.88%
Top 25
4,467,000
46.53%
37.23%
98,381,200
99,491,400
88.83%
Note:
*  Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon 
Listing.
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
Number of 
H Shares 
held upon 
Listing
% of total 
issued H Shares 
capital 
upon Listing
Number of 
Shares held 
upon Listing
Top 1
—
0.00%
0.00%
35,275,900
31.81%
35,275,900
Top 5
—
0.00%
0.00%
60,145,000
54.24%
60,145,000
Top 10
2,475,000
25.78%
20.63%
79,385,000
71.59%
79,385,000
Top 25
4,467,000
46.53%
37.23%
99,051,600
89.32%
99,051,600
Note:
*  Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 14>>>
– 14 –
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 118,537 valid 
applications made by the public will be conditionally allocated on the basis set out below:
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
100
62,321
3,116 out of 62,321 to receive 100 Shares
5.00%
200
5,937
332 out of 5,937 to receive 100 Shares
2.80%
300
2,579
148 out of 2,579 to receive 100 Shares
1.91%
400
1,812
106 out of 1,812 to receive 100 Shares
1.46%
500
1,890
113 out of 1,890 to receive 100 Shares
1.20%
600
1,150
70 out of 1,150 to receive 100 Shares
1.01%
700
749
47 out of 749 to receive 100 Shares
0.90%
800
1,325
86 out of 1,325 to receive 100 Shares
0.81%
900
6,820
452 out of 6,820 to receive 100 Shares
0.74%
1,000
4,254
287 out of 4,254 to receive 100 Shares
0.67%
1,500
2,315
170 out of 2,315 to receive 100 Shares
0.49%
2,000
1,596
127 out of 1,596 to receive 100 Shares
0.40%
2,500
866
74 out of 866 to receive 100 Shares
0.34%
3,000
857
79 out of 857 to receive 100 Shares
0.31%
3,500
595
58 out of 595 to receive 100 Shares
0.28%
4,000
677
70 out of 677 to receive 100 Shares
0.26%
4,500
446
49 out of 446 to receive 100 Shares
0.24%
5,000
1,011
118 out of 1,011 to receive 100 Shares
0.23%
6,000
744
96 out of 744 to receive 100 Shares
0.22%
7,000
611
86 out of 611 to receive 100 Shares
0.20%
8,000
589
90 out of 589 to receive 100 Shares
0.19%
9,000
553
91 out of 553 to receive 100 Shares
0.18%
10,000
3,491
617 out of 3,491 to receive 100 Shares
0.18%
20,000
2,473
726 out of 2,473 to receive 100 Shares
0.15%
30,000
1,348
553 out of 1,348 to receive 100 Shares
0.14%
40,000
927
489 out of 927 to receive 100 Shares
0.13%
50,000
732
471 out of 732 to receive 100 Shares
0.13%
60,000
547
416 out of 547 to receive 100 Shares
0.13%
70,000
445
391 out of 445 to receive 100 Shares
0.13%

<<<PAGE 15>>>
– 15 –
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
80,000
444
100 Shares plus 8 out of 444 to receive additional  
100 Shares
0.13%
90,000
406
100 Shares plus 44 out of 406 to receive additional  
100 Shares
0.12%
100,000
1,280
100 Shares plus 290 out of 1,280 to receive additional  
100 Shares
0.12%
 
111,790
Total number of Pool A successful applicants: 11,658
 
POOL B
125,000
2,480
100 Shares plus 1,077 out of 2,480 to receive additional  
100 Shares
0.11%
150,000
764
100 Shares plus 416 out of 764 to receive additional  
100 Shares
0.10%
175,000
436
100 Shares plus 285 out of 436 to receive additional  
100 Shares
0.09%
200,000
473
100 Shares plus 364 out of 473 to receive additional  
100 Shares
0.09%
225,000
198
200 Shares
0.09%
250,000
229
200 Shares plus 3 out of 229 to receive additional  
100 Shares
0.08%
275,000
123
200 Shares plus 16 out of 123 to receive additional  
100 Shares
0.08%
300,000
2,044
200 Shares plus 498 out of 2,044 to receive additional  
100 Shares
0.07%
 
6,747
Total number of Pool B successful applicants: 6,747
 
As of the date of this announcement, the relevant subscription monies previously deposited 
in the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers for any inquiries.

<<<PAGE 16>>>
– 16 –
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly 
or indirectly, provided by the issuer, its controlling shareholder(s), directors or syndicate 
members to any placees or the public (as the case may be) and the consideration payable by 
them for each share of the issuer subscribed for or purchased by them is the same as the final 
offer price determined by the issuer, in addition to any brokerage, AFRC transaction levy, 
SFC transaction levy and trading fee payable.
The Directors confirm that at least 50% of the total number of the Offer Shares have been 
allocated to and taken up by independent price setting investors in compliance with Rule 
18C.08 of the Listing Rules.
The Directors further confirm that at least 20% of the issued share capital of the Company 
will be held by sophisticated independent investors at the time of Listing in compliance with 
Chapter 2.5 of the Guide for New Listing Applicants.
OTHERS/ADDITIONAL INFORMATION
Reallocation
As the Hong Kong Public Offering has been over-subscribed by more than 100 times of the 
total number of Offer Shares initially available under the Hong Kong Public Offering, the 
reallocation procedure as disclosed in the section headed “Structure of the Global Offering 
— The Hong Kong Public Offering — Reallocation” in the Prospectus has been applied.
The number of Offer Shares initially available under the Hong Kong Public Offering is 
600,000 H Shares, representing approximately 5% of the total number of Offer Shares 
initially available under the Global Offering. As a result of such reallocation, the final 
number of Offer Shares under the Hong Kong Public Offering is adjusted to 2,400,000 
H Shares, representing approximately 20% of the total number of Offer Shares initially 
available under the Global Offering.

<<<PAGE 17>>>
– 17 –
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
and Hong Kong Securities Clearing Company Limited take no responsibility for the 
contents of this announcement, make no representation as to its accuracy or completeness 
and expressly disclaim any liability whatsoever for any loss howsoever arising from or in 
reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in 
or into the United States (including its territories and possessions, any state of the United 
States and the District of Columbia). This announcement does not constitute or form a part 
of any offer or solicitation to purchase or subscribe for securities in the United States. The 
Offer Shares have not been and will not be registered under the United States Securities 
Act of 1933, as amended (the “U.S. Securities Act”) or any state securities laws in the 
United States and may not be offered, sold, pledged or transferred within the United States 
or to, or for the account or benefit of U.S. persons (as defined in Regulation S under the 
U.S. Securities Act), except in transactions exempt from, or not subject to, the registration 
requirements of the U.S. Securities Act. The Offer Shares are being offered and sold 
outside the United States in offshore transactions in reliance on Regulation S under the U.S. 
Securities Act.
This announcement is for information purposes only and does not constitute an invitation 
or offer to acquire, purchase or subscribe for securities. This announcement is not a 
prospectus. Potential investors should read the Prospectus dated March 23, 2026 issued 
by Shanghai FourSemi Semiconductor Co., Ltd. for detailed information about the Global 
Offering described below before deciding whether or not to invest in the H Shares thereby 
being offered.
*Potential investors of the Offer Shares should note that the Joint Sponsors and the 
Sponsor-OCs (for themselves and on behalf of the Hong Kong Underwriters) shall be 
entitled to terminate their obligations under the Hong Kong Underwriting Agreement with 
immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering 
– Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong 
time) on the Listing Date (which is currently expected to be on March 31, 2026).

<<<PAGE 18>>>
– 18 –
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, the total number of the H 
Shares held by the public represents approximately 67.51% of the total issued share capital 
of the Company, which is higher than the prescribed percentage of H Shares required to 
be held in public hands of 25.00% under Rule 8.08(1) (as amended and replaced by Rule 
19A.13A(1)) of the Listing Rules calculated based on the final Offer Price of HK$40.00 per 
H Share, thereby satisfying the public float requirement under Rule 8.08(1) (as amended and 
replaced by Rule 19A.13A(1)) of the Listing Rules.
Based on the final Offer Price of HK$40.00 per H Share, the Company satisfies the free 
float requirement under Rule 19A.13C(1) of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering, 
(i) no placee will, individually, be placed more than 10% of the enlarged issued share 
capital of the Company immediately after the Global Offering; (ii) there will not be any new 
substantial Shareholder immediately after the Global Offering; (iii) the three largest public 
shareholders of the Company do not hold more than 50% of the shares in public hands at the 
time of the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) 
there will be at least 300 Shareholders at the time of the Listing in compliance with Rule 
8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, 
March 31, 2026 (Hong Kong time), provided that the Global Offering has become 
unconditional and the right of termination described in the section headed “Underwriting — 
Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus has not been exercised. Investors who trade the H Shares on 
the basis of publicly available allocation details prior to the receipt of Share certificates or 
prior to the Share certificates becoming valid evidence   of title do so entirely at their own 
risk.

<<<PAGE 19>>>
– 19 –
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m.  on 
Tuesday, March 31, 2026 (Hong Kong time), it is expected that dealings in the H Shares on 
the Stock Exchange will commence at 9:00 a.m. on Tuesday, March 31, 2026 (Hong Kong 
time). The H Shares will be traded in board lots of 100 Shares each, and the stock code of 
the H Shares will be 3625.
By order of the Board
Shanghai FourSemi Semiconductor Co., Ltd.
Xu Xiaolin
Chairman of the Board, Executive Director and president
Hong Kong, March 30, 2026
As of the date of this announcement, the Board comprises: (i) Mr. Xu Xiaolin, Mr. Liu Baoliang, Mr. Qian 
Shun and Ms. Yu Bingbing as executive Directors; (ii) Mr. Chen Binglin, Mr. Lin Enfeng as non-executive 
Directors; and (iii) Mr. Liu Hongcan, Ms. Liu Liping and Mr. Dai Xueguang as independent non executive 
Directors.
