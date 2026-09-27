# 配发结果公告抽取任务：2041.HK Medcaptain Medical Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**04/09/2026 18:47**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0904/2026090401842.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2041.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated August 28, 2026 (the “Prospectus”) of Medcaptain Medical Technology Co., Ltd. (深
圳麥科田生物醫療技術股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the Prospectus for 
detailed information about the Global Offering described below before deciding whether or not to invest in the Offer 
Shares. Any investment decision in relation to the Offer Shares should be taken solely in reliance on the information 
provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities in 
the United States. The securities mentioned herein have not been, and will not be, registered under the United States 
Securities Act of 1933, as amended (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of 
the United States and may not be offered, sold, pledged or otherwise transferred within the United States, except in 
transactions exempt from, or not subject to, the registration requirements of the U.S. Securities Act and in compliance 
with any applicable state securities laws. There will be no public offer of the Offer Shares in the United States. The 
Offer Shares are being offered and sold only (a) in the United States to “Qualified Institutional Buyers” in reliance on 
Rule 144A under the U.S. Securities Act or another exemption from, or in a transaction not subject to, the registration 
requirements under the U.S. Securities Act; and (b) outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act and applicable laws of each jurisdiction where those offers and sales occur.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to terms and conditions set out in 
the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not 
resident in Hong Kong.
Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall, in their sole and absolute discretion, be entitled to 
terminate their obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence 
of any of the events set out in the paragraph headed “Underwriting — Underwriting Arrangements and Expenses — 
The Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong 
Kong time) on the Listing Date.

<<<PAGE 2>>>
2
Medcaptain Medical Technology Co., Ltd.
深圳麥科田生物醫療技術股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the Global 
Offering
:
38,910,600 H Shares
Number of Hong Kong Offer Shares
:
3,891,100 H Shares
Number of International Offer Shares
:
35,019,500 H Shares
Offer Price
:
HK$15.42 per H Share, plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
Hong Kong Stock Exchange trading fee of 
0.00565% and AFRC transaction levy of 
0.00015%
Nominal value
:
RMB1.00 per H Share
Stock code
:
2041
Joint Sponsors, Overall Coordinators,
Joint Global Coordinators, Joint Bookrunners, Joint Lead Managers
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
Medcaptain Medical Technology Co., Ltd.
深圳麥科田生物醫療技術股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated August 28, 2026 (the “Prospectus”) 
of Medcaptain Medical Technology Co., Ltd. (深圳麥科田生物醫療技術股份有限公司) (the 
“Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company Information
Stock code
2041
Stock short name
MEDCAPTAIN
Dealings commencement date
September 7, 2026*
* see note at the end of the announcement
Price Information
Offer Price
HK$15.42
Offer Shares and Share Capital
Number of Offer Shares
38,910,600
Number of Offer Shares in Hong Kong Public Offering
3,891,100
Number of Offer Shares in International Offering
35,019,500
Number of issued Shares upon Listing
538,626,686
Proceeds
Gross proceeds (Note)
HK$600.0 million
 Less:  Estimated listing expenses payable based on Offer  
 Price
HK$103.8 million
Net proceeds
HK$496.2 million
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.

<<<PAGE 4>>>
4
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
57,305
No. of successful applications
15,492
Subscription level
436.37 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong 
 Public Offering
3,891,100
No. of Offer Shares reallocated from the International 
 Offering
N/A
Final no. of Offer Shares under the Hong Kong Public 
 Offering
3,891,100
% of Offer Shares under the Hong Kong Public Offering 
 to the Global Offering
10.00%
Note:  For details of the final allocation of Shares to the Hong Kong Public Offering, investors can refer to the 
designated results of allocations website at www.hkeipo.hk/IPOResult to perform a search by identification 
number or the “Allotment Results” page of the HK eIPO White Form service at www.hkeipo.hk/IPOResult for 
the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
95
Subscription Level
2.35 times
No. of Offer Shares initially available under the 
 International Offering
35,019,500
No. of Offer Shares reallocated to the Hong Kong 
 Public Offering
N/A
Final no. of Offer Shares under the International Offering
35,019,500
% of Offer Shares under the International Offering to the 
 Global Offering
90.00%
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, substantial shareholders, 
existing shareholders of the Company or any of its subsidiaries or their respective close associates; 
and (ii) none of the placees and the public who have purchased the Offer Shares are accustomed 
to taking instructions from the Company, any of the Directors, chief executive of the Company, 
substantial shareholders, existing shareholders of the Company or any of its subsidiaries or their 
respective close associates in relation to the acquisition, disposal, voting or other disposition of 
Shares registered in his/her/its name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Allottee with waiver/consent obtained
Investor
No. of Offer 
Shares allocated
% of 
Offer Shares
% of total 
Issued share 
capital after 
the Global 
Offering
Relationship
Allottee with consent under paragraph 1C(1) of the Placing Guidelines in relation to allocation to connected client (Note 1)
Wang On Asset Management Limited  
 (“Wang On AM”)
503,300
1.29%
0.09%
A connected client of 
Wang On Securities 
Limited (“Wang On 
Securities”) (Note 1)
Note:
1. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines in relation to allocation to connected 
client, please refer to the section headed “Additional Information – Placing to connected client with a prior 
consent under paragraph 1C(1) of the Placing Guidelines” in this announcement.

<<<PAGE 6>>>
6
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
H Shares 
held in the 
Company subject 
to lock-up
undertakings 
upon Listing
% of total
issued Shares in
the Company 
upon Listing
Last day
subject to the 
lock-up
undertakings (Note 1)
LIU Jie (Note 2)
54,450,000
10.11%
September 6, 2027
ZHONG Yaoqi/鍾要齊 (“Mr. Zhong”) (Note 2)
28,600,000
5.31%
September 6, 2027
LI Hui/李輝 (“Ms. Li”) (Note 2)
22,286,000
4.14%
September 6, 2027
Shenzhen Juxian Kangzhong Enterprise Management 
 Partnership (Limited Partnership)/
 深圳聚賢康眾企業管理合夥企業(有限合夥) (Note 2)
63,685,000
11.82%
September 6, 2027
Shenzhen Ruisen Kangzhong Investment Enterprise (Limited 
 Partnership)/深圳瑞森康眾投資企業(有限合夥) (Note 2)
8,950,000
1.66%
September 6, 2027
Zhuhai Ruikun Kangzhong Investment Enterprise (Limited 
 Partnership)/珠海瑞坤康眾投資企業(有限合夥) (Note 2)
5,650,000
1.05%
September 6, 2027
Zhuhai Jucai Kangzhong Investment Enterprise (Limited 
 Partnership)/珠海聚才康眾投資企業(有限合夥) (Note 2)
4,400,000
0.82%
September 6, 2027
Zhuhai Ruiqian Kangzhong Investment Enterprise (Limited 
 Partnership)/珠海瑞乾康眾投資企業(有限合夥) (Note 2)
4,400,000
0.82%
September 6, 2027
Zhuhai Ruiyu Kangzhong Investment Enterprise (Limited 
 Partnership)/珠海瑞鈺康眾投資企業(有限合夥) (Note 2)
3,300,000
0.61%
September 6, 2027
Shenzhen Ruixin Kangzhong Investment Enterprise (Limited 
 Partnership)/深圳瑞鑫康眾投資企業(有限合夥) (Note 2)
1,928,812
0.36%
September 6, 2027
Subtotal
197,649,812
36.70%
Notes:
1. 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. The 
required lock-up for the Controlling Shareholders ends on September 6, 2027, being 12 months following the 
Listing Date.
2. 
Ms. Li is the general partner of certain of our Employees Incentive Platforms, namely Juxian Kangzhong 
LP, Ruisen Kangzhong LP, Jucai Kangzhong LP, Ruiyu Kangzhong LP, Ruiqian Kangzhong LP and Ruikun 
Kangzhong LP, on behalf of which Ms. Li will exercise their voting powers at Shareholders’ meetings. Mr. 
Zhong is the general partner of Ruixin Kangzhong LP, on behalf of which Mr. Zhong will exercise its voting 
rights at Shareholders’ meetings. Mr. Liu, Mr. Zhong and Ms. Li have entered into the currently effective 
Concert Party Agreement. For further details, see “History, Development and Corporate Structure— Concert 
Party Arrangement” in the Prospectus.

<<<PAGE 7>>>
7
Pre-IPO Investors (as defined in the Prospectus)
Name
Number of 
H Shares 
held in the 
Company subject 
to lock-up
undertakings 
upon Listing
% of total 
issued Shares in 
the Company 
upon Listing
Last day 
subject to the 
lock-up
undertakings (Note 1)
Zhuhai Gao Ling Tiancheng Equity Investment Fund (Limited 
 Partnership)/珠海高瓴天成股權投資基金(有限合夥)
23,375,000
4.34%
September 6, 2027
Tianjin Zhenying Enterprise Management Consultancy Limited 
 Partnership (Limited Partnership)/
 天津振盈企業管理諮詢合夥企業(有限合夥)
23,100,000
4.29%
September 6, 2027
Zhuhai Aiheng Equity Investment Partnership (Limited 
 Partnership)/珠海艾恆股權投資合夥企業(有限合夥)
3,987,500
0.74%
September 6, 2027
Suzhou Gao Ling Qirui Medical Health Industry Investment 
 Partnership Enterprise (Limited Partnership)/
 蘇州高瓴祈睿醫療健康產業投資合夥企業(有限合夥)
1,487,500
0.28%
September 6, 2027
Shenzhen Hongtu Healthcare Industry Equity Investment 
 Partnership (Limited Partnership)/
 深圳紅土醫療健康產業股權投資基金合夥企業(有限合夥)
15,939,944
2.96%
September 6, 2027
Shenzhen Capital Group Co., Ltd./
 深圳市創新投資集團有限公司
10,544,885
1.96%
September 6, 2027
Guangdong Hongtu Entrepreneurship Investment Limited 
 Company/廣東紅土創業投資有限公司
5,395,057
1.00%
September 6, 2027
Shenzhen Hongtu Peacock Entrepreneurship Investment 
 Limited Company/深圳市紅土孔雀創業投資有限公司
5,395,057
1.00%
September 6, 2027
Shenzhen Pingshan Area Hongtu Entrepreneurship 
 Investment Limited Company/
 深圳市坪山區紅土創新發展創業投資有限公司
5,395,057
1.00%
September 6, 2027
Wuhu Xinshi Xinyao Equity Investment Partnership (Limited 
 Partnership)/蕪湖信石信耀股權投資合夥企業(有限合夥)
3,299,894
0.61%
September 6, 2027
Shenzhen Xinshi Xinxing Industry M&A Equity Investment 
 Fund Partnership (Limited Partnership)/
 深圳信石信興產業併購股權投資基金合夥企業(有限合夥)
13,199,582
2.45%
September 6, 2027
ZHUANG Xiaojin/莊小金
34,664,062
6.44%
September 6, 2027
Zhuhai Hualong Kangzhong Investment Partnership 
 Enterprise (Limited Partnership)/
 珠海華隆康眾投資合夥企業(有限合夥)
23,512,645
4.37%
September 6, 2027
Suzhou Lirui Equity Investment Center (Limited Partnership)/
 蘇州禮瑞股權投資中心(有限合夥)
13,750,000
2.55%
September 6, 2027

<<<PAGE 8>>>
8
Name
Number of 
H Shares 
held in the 
Company subject 
to lock-up
undertakings 
upon Listing
% of total 
issued Shares in 
the Company 
upon Listing
Last day 
subject to the 
lock-up
undertakings (Note 1)
MIAO Donglin/繆東林
11,554,687
2.15%
September 6, 2027
LI Dongcen/李冬岑
8,679,000
1.61%
September 6, 2027
Ningbo Kangjun Zhongyuan Equity Investment 
 Partnership (Limited Partnership)/
 寧波康君仲元股權投資合夥企業(有限合夥)
6,666,666
1.24%
September 6, 2027
Shenzhen Guozhong SME Development Private Equity 
 Investment Fund Partnership (limited partnership)/
 深圳國中中小企業發展私募股權投資基金合夥企業
 (有限合夥)
5,500,000
1.02%
September 6, 2027
Changzhou Zixi Venture Capital Partnership (Limited 
 Partnership)/常州梓熙創業投資合夥企業(有限合夥)
3,453,125
0.64%
September 6, 2027
Changzhou Zijing Venture Capital Partnership (Limited 
 Partnership)/常州梓瀞創業投資合夥企業(有限合夥)
3,453,125
0.64%
September 6, 2027
LV Caishu/呂才樹
1,943,475
0.36%
September 6, 2027
Shenzhen Junji Management Consulting Partnership (Limited 
 Partnership)/深圳市君濟管理諮詢合夥企業(有限合夥)
2,588,625
0.48%
September 6, 2027
Shenzhen Kanghong Consulting Management Enterprise 
 (Limited Partnership)/深圳市康泓諮詢管理企業(有限合夥)
1,500,000
0.28%
September 6, 2027
MAO Peihua/茅培華
1,401,639
0.26%
September 6, 2027
Shenzhen Boxin Shengke Venture Capital Partnership (Limited 
 Partnership)/深圳博信生科創業投資合夥企業(有限合夥)
1,250,000
0.23%
September 6, 2027
Shenzhen Share Zeshan Precision Medical Venture Capital 
 Partnership (Limited Partnership)/深圳市分享擇善精準醫療
 創業投資合夥企業(有限合夥)
1,250,000
0.23%
September 6, 2027
Shenzhen Nanshan SBCVC Equity Investment Fund Partnership 
 (Limited Partnership)/深圳市南山軟銀股權投資基金合夥
 企業(有限合夥)
1,250,000
0.23%
September 6, 2027
Shenzhen Grandway Capital Management Co., Ltd./
 深圳市嘉遠資本管理有限公司
1,250,000
0.23%
September 6, 2027
Shenzhen Gaotejia Ruixin Investment Partnership (Limited 
 Partnership)/深圳市高特佳睿信投資合夥企業(有限合夥)
1,250,000
0.23%
September 6, 2027
LI Ying/李穎
1,026,405
0.19%
September 6, 2027
Ningbo Jiazhu Enterprise Management Partnership (Limited 
 Partnership)/寧波嘉竹企業管理合夥企業(有限合夥)
1,000,000
0.19%
September 6, 2027

<<<PAGE 9>>>
9
Name
Number of 
H Shares 
held in the 
Company subject 
to lock-up
undertakings 
upon Listing
% of total 
issued Shares in 
the Company 
upon Listing
Last day 
subject to the 
lock-up
undertakings (Note 1)
Dongguan Xintai No. 18 Equity Investment Partnership 
 (Limited Partnership)/東莞鑫泰十八號股權投資合夥企業
 (有限合夥)
500,000
0.09%
September 6, 2027
Gongqingcheng Jiayin Ruihe Investment Management 
 Partnership (Limited Partnership)/
 共青城佳銀瑞禾投資管理合夥企業(有限合夥)
1,000,000
0.19%
September 6, 2027
Shenzhen High-Tech Venture Capital Co., Ltd./
 深圳市高新投創業投資有限公司
875,000
0.16%
September 6, 2027
Ningbo Zhixun Venture Capital Partnership (Limited 
 Partnership)/寧波市智尋創業投資合夥企業(有限合夥)
875,000
0.16%
September 6, 2027
Gongqingcheng Daohe Venture Capital Partnership (Limited 
 Partnership)/共青城道合創業投資合夥企業(有限合夥)
625,000
0.12%
September 6, 2027
Shenzhen Talent Innovation and Entrepreneurship No. 2 Equity 
 Investment Fund Partnership (Limited Partnership)/深圳市
 人才創新創業二號股權投資基金合夥企業(有限合夥)
531,250
0.10%
September 6, 2027
DOU Wenxiang/竇文祥
98,344
0.02%
September 6, 2027
Shenzhen Xiaohe Venture Capital Partnership (Limited 
 Partnership)/深圳市小禾創業投資合夥企業(有限合夥)
93,750
0.02%
September 6, 2027
Subtotal
242,661,274
45.05%
Notes:
1. 
Please see “History, Development and Corporate Structure — Information about our Pre-IPO Investors” in 
the Prospectus for the identities of the Pre-IPO Investors.
2. 
Pursuant to the applicable PRC law, within the 12 months following the Listing Date, all existing 
Shareholders (including the Pre-IPO Investors) are prohibited from disposing of any of the Shares held by 
them.

<<<PAGE 10>>>
10
PLACEE CONCENTRATION ANALYSIS
Placees
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering
Allotment as 
% of total 
Offer Shares 
Number of 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing
Top 1
4,067,400
11.61%
10.45%
4,067,400
0.76%
Top 5
13,900,400
39.69%
35.72%
13,900,400
2.58%
Top 10
19,379,500
55.34%
49.81%
19,379,500
3.60%
Top 25
28,141,100
80.36%
72.32%
28,141,100
5.22%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHARE SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering
Allotment as 
% of total 
Offer Shares
Number of 
H Shares 
held upon 
Listing
% of total 
issued 
H Share 
capital upon 
Listing
Number of
Shares
held upon
Listing
Top 1
0
0.00%
0.00%
197,649,812
41.24%
197,649,812
Top 5
0
0.00%
0.00%
360,009,019
75.12%
411,959,019
Top 10
0
0.00%
0.00%
417,158,848
87.05%
469,108,848
Top 25
16,513,800
47.16%
42.44%
450,356,387
93.98%
503,306,387
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
Allotment as 
% of total 
Offer Shares
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
0
0.00%
0.00%
197,649,812
197,649,812
36.70%
Top 5
0
0.00%
0.00%
360,009,019
411,959,019
76.48%
Top 10
0
0.00%
0.00%
417,158,848
469,108,848
87.09%
Top 25
16,513,800
47.16%
42.44%
449,106,387
507,181,387
94.16%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by Shareholders upon Listing.

<<<PAGE 11>>>
11
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
total number of
H Shares 
applied for
100
15,632
782 out of 15,632 applicants to receive 100 H Shares
5.00%
200
3,761
273 out of 3,761 applicants to receive 100 H Shares
3.63%
300
4,976
448 out of 4,976 applicants to receive 100 H Shares
3.00%
400
1,272
134 out of 1,272 applicants to receive 100 H Shares
2.63%
500
2,441
289 out of 2,441 applicants to receive 100 H Shares
2.37%
600
1,929
252 out of 1,929 applicants to receive 100 H Shares
2.18%
700
1,371
195 out of 1,371 applicants to receive 100 H Shares
2.03%
800
744
114 out of 744 applicants to receive 100 H Shares
1.92%
900
507
83 out of 507 applicants to receive 100 H Shares
1.82%
1,000
4,490
769 out of 4,490 applicants to receive 100 H Shares
1.71%
1,500
1,486
317 out of 1,486 applicants to receive 100 H Shares
1.42%
2,000
1,567
389 out of 1,567 applicants to receive 100 H Shares
1.24%
2,500
721
202 out of 721 applicants to receive 100 H Shares
1.12%
3,000
1,707
526 out of 1,707 applicants to receive 100 H Shares
1.03%
3,500
879
295 out of 879 applicants to receive 100 H Shares
0.96%
4,000
488
176 out of 488 applicants to receive 100 H Shares
0.90%
4,500
345
133 out of 345 applicants to receive 100 H Shares
0.86%
5,000
990
401 out of 990 applicants to receive 100 H Shares
0.81%
6,000
1,022
457 out of 1,022 applicants to receive 100 H Shares
0.75%
7,000
593
288 out of 593 applicants to receive 100 H Shares
0.69%
8,000
364
190 out of 364 applicants to receive 100 H Shares
0.65%
9,000
260
145 out of 260 applicants to receive 100 H Shares
0.62%
10,000
2,330
1,367 out of 2,330 applicants to receive 100 H Shares
0.59%
20,000
1,090
927 out of 1,090 applicants to receive 100 H Shares
0.43%
30,000
685
100 H Shares
0.33%
40,000
418
100 H Shares plus 97 out of 418 applicants to receive an 
additional 100 H Shares
0.31%
50,000
443
100 H Shares plus 172 out of 443 applicants to receive an 
additional 100 H Shares
0.28%
60,000
293
100 H Shares plus 155 out of 293 applicants to receive an 
additional 100 H Shares
0.25%
70,000
260
100 H Shares plus 172 out of 260 applicants to receive an 
additional 100 H Shares
0.24%

<<<PAGE 12>>>
12
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
total number of
H Shares 
applied for
80,000
195
100 H Shares plus 153 out of 195 applicants to receive an 
additional 100 H Shares
0.22%
90,000
159
100 H Shares plus 143 out of 159 applicants to receive an 
additional 100 H Shares
0.21%
100,000
1,133
200 H Shares
0.20%
200,000
664
200 H Shares plus 605 out of 664 applicants to receive an 
additional 100 H Shares
0.15%
300,000
750
300 H Shares plus 510 out of 750 applicants to receive an 
additional 100 H Shares
0.12%
Total
55,965
Total number of Pool A successful applicants: 14,152
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
total number of
H Shares 
applied for
400,000
583
900 H Shares plus 117 out of 583 applicants to receive an 
additional 100 H Shares
0.23%
500,000
158
1,000 H Shares plus 149 out of 158 applicants to receive an 
additional 100 H Shares
0.22%
600,000
82
1,200 H Shares plus 50 out of 82 applicants to receive an 
additional 100 H Shares
0.21%
700,000
95
1,400 H Shares plus 21 out of 95 applicants to receive an 
additional 100 H Shares
0.20%
800,000
60
1,500 H Shares plus 46 out of 60 applicants to receive an 
additional 100 H Shares
0.20%
900,000
25
1,700 H Shares plus 7 out of 25 applicants to receive an 
additional 100 H Shares
0.19%
1,000,000
135
1,800 H Shares plus 102 out of 135 applicants to receive an 
additional 100 H Shares
0.19%
1,500,000
50
2,500 H Shares plus 35 out of 50 applicants to receive an 
additional 100 H Shares
0.17%
1,945,500
152
3,100 H Shares plus 70 out of 152 applicants to receive an 
additional 100 H Shares
0.16%
Total
1,340
Total number of Pool B successful applicants: 1,340

<<<PAGE 13>>>
13
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
ADDITIONAL INFORMATION
Placing to connected client with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected client of certain 
distributor pursuant to the Placing Guidelines. Details of the placement to connected client are set 
out below.
Connected client
Connected 
distributor
Relationship
Whether the 
connected client 
will hold beneficial 
interests of Offer 
Shares on a non- 
discretionary or 
discretionary basis  
for independent  
third parties
No. of Offer 
Shares 
allocated 
to the 
connected 
client
% of 
Offer Shares
% of total 
issued share 
capital after 
the Global 
Offering
Wang On AM
Wang On Securities
See Note 1
Discretionary basis
503,300
1.29%
0.09%
Note:
1. 
Wang On Securities is a non-syndicate distributor in connection with the Global Offering. Wang On AM is a 
member of the same group of companies as Wang On Securities. Wang On AM will hold the Offer Shares in its 
capacity as discretionary fund manager managing the discretionary portfolio on behalf of its underlying clients 
(the “Wang On AM Ultimate Clients”). The ultimate beneficial owner holding 30% interests or more in the 
Wang On AM Ultimate Clients is LIU Ying. To the best of Wang On AM’s knowledge and belief after due 
enquiry, each of the Wang On AM Ultimate Clients and LIU Ying is an independent third party of the Company, 
its subsidiaries, its Controlling Shareholders (as defined in the Prospectus) and its substantial shareholders, 
Wang On AM, Wang On Securities and the companies which are members of the same group of companies as 
Wang On Securities, respectively.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraphs 1C(1) of the Placing Guidelines to permit the Company to allocate such 
Offer Shares in the International Offering to the connected client listed above. The allocation of 
Offer Shares to such connected client is in compliance with all the conditions under the consent 
granted by the Stock Exchange.

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
as amended (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the 
United States and may not be offered, sold, pledged or otherwise transferred within the United 
States, except in transactions exempt from, or not subject to, the registration requirements of the 
U.S. Securities Act and in compliance with any applicable state securities laws. There will be no 
public offer of the Offer Shares in the United States.
The Offer Shares are being offered and sold only (a) in the United States to “Qualified 
Institutional Buyers” in reliance on Rule 144A under the U.S. Securities Act or another 
exemption from, or in a transaction not subject to, the registration requirements under the 
U.S. Securities Act; and (b) outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act and applicable laws of each jurisdiction where those 
offers and sales occur.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated August 28, 2026 issued by Medcaptain Medical 
Technology Co., Ltd. (深圳麥科田生物醫療技術股份有限公司) for detailed information about 
the Global Offering described herein before deciding whether or not to invest in the Shares 
thereby being offered.
* 
Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-
Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall, 
in their sole and absolute discretion, be entitled to terminate their obligations under the 
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of 
the events set out in the paragraph headed “Underwriting — Underwriting Arrangements 
and Expenses — The Hong Kong Public Offering — Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date.

<<<PAGE 15>>>
15
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, (i) a total of 229,621,874 H Shares, 
representing approximately 42.63% of the total number of issued Shares will be regarded as public 
float and the Company will satisfy the minimum percentage as prescribed under Rule 19A.13A(1) 
of the Listing Rules; (ii) the three largest public Shareholders do not hold more than 50% of the 
H Shares in public hands at the time of Listing in compliance with Rules 8.08(3) and 8.24 of the 
Listing Rules; (iii) there will not be any new substantial shareholder (as defined in the Listing 
Rules) of the Company immediately after the Global Offering; (iv) no placee will, individually, 
be placed more than 10% of the enlarged issued share capital of the Company immediately after 
the Global Offering; and (v) there will be at least 300 Shareholders at the time of Listing in 
compliance with Rule 8.08(2) of the Listing Rules.
Based on the final Offer Price of HK$15.42 per H Share, the expected market value of the 
H Shares held by the public and not subject to any disposal restrictions will not be less than 
HK$600,000,000. Therefore, the Company is expected to satisfy the free float requirement under 
Rule 19A.13C of the Listing Rules at the time of Listing.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. (Hong Kong time) on 
Monday, September 7, 2026, provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting — Underwriting Arrangements 
and Expenses — The Hong Kong Public Offering — Grounds for Termination” in the Prospectus 
has not been exercised. Investors who trade H Shares prior to the receipt of H Share certificates or 
the H Share certificates becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong Kong time) 
on Monday, September 7, 2026, it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Monday, September 7, 2026. The H Shares will be traded in board 
lots of 100 H Shares each. The stock code of the Shares is 2041.
By order of the Board
Medcaptain Medical Technology Co., Ltd.
Mr. LIU Jie
Chairman of the Board and executive director
Hong Kong, September 4, 2026
As at the date of this announcement, the Board comprises: (i) Mr. LIU Jie, Mr. ZHONG Yaoqi and 
Mr. YAN Renzhong as executive Directors, (ii) Ms. LI Hui, Mr. ZHANG Jiecheng and Dr. ZHOU 
Yi as non-executive Directors, and (iii) Dr. SHAO Liyang, Mr. ZHANG Hanbin and Mr. TAM 
Man Hong as independent non-executive Directors.
