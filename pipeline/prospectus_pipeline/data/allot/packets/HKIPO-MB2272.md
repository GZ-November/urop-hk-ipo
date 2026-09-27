# 配发结果公告抽取任务：2272.HK KEYTOP PARKING INC. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**25/06/2026 21:12**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0625/2026062501916.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2272.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for 
securities in the United States or in any other jurisdictions. The Offer Shares have not been and will not be 
registered under the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities 
Act”) or securities law of any state or other jurisdiction of the United States and may not be offered, sold, 
pledged or otherwise transferred within the United States, except in transactions exempt from, or not subject 
to, the registration requirements of the U.S. Securities Act and in compliance with any applicable state 
securities laws. There will be no public offer of the Offer Shares in the United States. The Offer Shares are 
being offered and sold outside the United States in offshore transactions in reliance on Regulation S under 
the U.S. Securities Act and applicable laws of each jurisdiction where those offers and sales occur.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. This announcement is not a prospectus. Potential investors should read 
the prospectus dated June 17, 2026 (the “Prospectus”) issued by Keytop Parking Inc. (廈門科拓通訊技術股
份有限公司) (the “Company”) for detailed information about the Global Offering described below before 
deciding whether or not to invest in the H Shares thereby being offered. Any investment decision in relation to 
the Offer Shares should be taken solely in reliance on the information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings 
as those defined in the Prospectus.
It is anticipated that no stabilization activities will be carried out by the Stabilizing Manager in relation to 
the Global Offering.
Potential investors of the Offer Shares should note that the Sponsor-OCs (for themselves and on behalf of the 
Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which 
is currently expected to be on Friday, June 26, 2026).

<<<PAGE 2>>>
– 2 –
KEYTOP PARKING INC.
廈門科拓通訊技術股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Total number of Offer Shares under the 
Global Offering
:
10,112,280 H Shares
Number of Hong Kong Offer Shares
:
1,011,240 H Shares
Number of International Offer Shares
:
9,101,040 H Shares
Offer Price
:
HK$39.55 per H Share, plus brokerage of 1%, SFC 
transaction levy of 0.0027%, Stock Exchange 
trading fee of 0.00565% and AFRC transaction 
levy of 0.00015%
Nominal value
:
RMB1.00 per H Share
Stock code
:
2272
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and 
Joint Lead Managers
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers
Joint Lead Managers

<<<PAGE 3>>>
 
 
3 
 
KEYTOP PARKING INC. 
廈門科拓通訊技術股份有限公司 
ANNOUNCEMENT OF ALLOTMENT RESULTS 
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated June 17, 2026 (the “Prospectus”) issued by 
Keytop Parking Inc. (廈門科拓通訊技術股份有限公司) (the “Company”). 
SUMMARY 
Company information 
Stock code 
2272 
Stock short name 
KEYTOP PARKING 
Dealings commencement date 
June 26, 2026* 
* 
see note at the end of the announcement 
Price Information 
Offer Price 
HK$39.55 
 
Offer Shares and Share Capital 
Number of Offer Shares 
10,112,280 
Final Number of Offer Shares in Hong Kong Public Offering 
1,011,240 
Final Number of Offer Shares in International Offering 
9,101,040 
Number of issued Shares upon Listing 
101,122,609 
 
Over-allocation 
No. of Offer Shares over-allocated 
0 
Note: There has been no over-allocation of Offer Shares in the International Offering. Therefore, the 
Over-allotment Option will not be exercised. 
Proceeds 
Gross proceeds (Note) 
HK$399.9 million 
Less: Estimated listing expenses payable based on the Offer Price 
HK$60.0 million 
Net proceeds 
HK$339.9 million 
Note: Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the 
use of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the 
Prospectus.  
 

<<<PAGE 4>>>
 
 
4 
 
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING 
 
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/iporesult to perform a search by identification number or www.hkeipo.hk/iporesult for the full list of 
allottees.  
 
 
 
No. of valid applications 
165,737 
No. of successful applications 
15,301 
Subscription level 
2,115.21 times 
Claw-back triggered 
N/A 
No. of Offer Shares initially available under the Hong Kong Public 
Offering 
1,011,240 
No. of Offer Shares reallocated from the International Offering 
0 
Final no. of Offer Shares under the Hong Kong Public Offering 
1,011,240 
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering  
10% 

<<<PAGE 5>>>
 
 
5 
 
INTERNATIONAL OFFERING  
 
No. of placees 
106 
Subscription level 
5.56 times 
No. of Offer Shares initially available under the International 
Offering 
9,101,040 
Final no. of Offer Shares under the International Offering 
9,101,040 
% of Offer Shares under the International Offering to the Global 
Offering  
90% 
 
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly by 
the Company, any of the directors, chief executive, Controlling Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates; and (ii) none of the placees and the public who have purchased the Offer Shares 
are accustomed to taking instructions from the Company, any of the directors, chief executive, 
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company or any 
of its subsidiaries or their respective close associates in relation to the acquisition, disposal, voting 
or other disposition of H Shares registered in his/her/its name or otherwise held by him/her/it. 
 
 

<<<PAGE 6>>>
 
 
6 
 
LOCK-UP UNDERTAKINGS 
Controlling Shareholders 
Name 
Number of Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing 
H Shares as % of 
total issued H 
Shares subject to 
lock-up 
undertakings 
upon Listing  
% of total issued 
share capital in 
the Company 
subject to lock-up 
undertakings 
upon Listing  
Last day subject to 
the lock-up 
undertakings Note 1 
Mr. Sun Longxi (孫龍喜) (“Mr. 
Sun”) Note 2 
 23,996,383 H 
Shares 
24.42% 
23.73% 
June 25, 2027 
Mr. Huang Jinlian (黃金練) (“Mr. 
Huang”) Note 2 
21,787,340 H 
Shares 
22.17% 
21.55% 
June 25, 2027 
Xiamen Hualong Electronics 
Technology Co., Ltd. (廈門鏵龍電
子科技有限公司) (“Hualong 
Electronics”) Note 2 
3,039,684 H 
Shares 
3.09% 
3.00% 
June 25, 2027 
Total 
48,823,407 H 
Shares  
49.68% 
48.28% 
 
 
Notes: 
1. The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws and relevant 
lock-up undertakings as disclosed in the Prospectus. 
2. Upon Listing, Mr. Sun, Mr. Huang, and Hualong Electronics will constitute a group of Controlling Shareholders. 
For further details, please refer to “Relationship with Our Controlling Shareholders” in the Prospectus. This 
subsection illustrates their direct shareholding in the Company, and each of them is subject to the same lock-up 
as disclosed above. 
 
 

<<<PAGE 7>>>
 
 
7 
 
Other Existing Shareholders (including the Pre-IPO Investors as defined in the “History, 
Development and Corporate Structure” section of the Prospectus) 
Name 
Number of Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing 
H Shares as % of 
total issued H 
Shares subject to 
lock-up 
undertakings 
upon Listing 
% of total issued 
share capital in 
the Company 
subject to lock-up 
undertakings 
upon Listing 
Last day subject to 
the lock-up 
undertakings Note 1 
Xiamen Juhua Enterprise 
Management Consulting Partnership 
(Limited Partnership) (廈門聚鏵企
業管理諮詢合夥企業(有限合夥))  
3,230,457 H 
Shares 
3.29% 
3.19% 
June 25, 2027 
Xiamen Tuojuxin Enterprise 
Management Consulting Partnership 
(Limited Partnership) (廈門 拓聚鑫
企業管理諮詢合夥企業(有限合夥
)) 
1,010,329 H 
Shares 
1.03% 
1.00% 
June 25, 2027 
Xiamen Tuojulian Enterprise 
Management Consulting Partnership 
(Limited Partnership) (廈門拓聚連
企業管理諮詢合夥企業(有限合夥
)) 
117,506 H Shares 
0.12% 
0.12% 
June 25, 2027 
Mr. Peng Jianhu (彭建虎) 
5,541,520 Shares 
(including 
2,684,480 H 
Shares and 
2,857,040 
Domestic Shares) 
2.73% 
5.48% 
June 25, 2027 
Chongqing Jiatuo Tiancheng 
Enterprise Management Partnership 
(Limited Partnership) (重慶加拓添
成企業管理合夥企業(有限合夥)) 
3,981,946 H 
Shares 
4.05% 
3.94% 
June 25, 2027 
Linzhi Lixin Information 
Technology Co., Ltd. (林芝利新信
息技術有限公司) 
5,603,521 H 
Shares 
5.70% 
5.54% 
June 25, 2027 
Suzhou Paiyi Venture Capital 
Partnership L.P. (蘇州湃益創業投
資合夥企業(有限合夥)) 
2,095,760 H 
Shares 
2.13% 
2.07% 
June 25, 2027 
Xiamen Zhengzhi Equity 
Investment Partnership (Limited 
Partnership) (廈門正志股權投資合
夥企業(有限合夥)) 
3,824,204 H 
Shares 
3.89% 
3.78% 
June 25, 2027 
Chongqing Hongtai Zhiying Equity 
Investment Center (Limited 
Partnership) (重慶洪泰致盈股權投
資中心(有限合夥)) 
3,381,345 H 
Shares 
3.44% 
3.34% 
June 25, 2027 
Yu Sheng (余盛) 
3,374,031 H 
Shares 
3.43% 
3.34% 
June 25, 2027 
Xiamen Suming Enterprise 
Management Consulting Partnership 
(Limited Partnership) (廈門速銘企
業管理諮詢合夥企業(有限合夥)) 
3,292,718 H 
Shares 
3.35% 
3.26% 
June 25, 2027 

<<<PAGE 8>>>
 
 
8 
 
Name 
Number of Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing 
H Shares as % of 
total issued H 
Shares subject to 
lock-up 
undertakings 
upon Listing 
% of total issued 
share capital in 
the Company 
subject to lock-up 
undertakings 
upon Listing 
Last day subject to 
the lock-up 
undertakings Note 1 
Xiamen Fulv Century Jinyuan 
Equity Investment Partnership 
(Limited Partnership) (廈門福旅世
紀金源股權投資合夥企業(有限合 
夥))  
2,711,573 H 
Shares 
2.76% 
2.68% 
June 25, 2027 
Yu Yunhui (余雲輝) 
2,129,288 H 
Shares 
2.17% 
2.11% 
June 25, 2027 
Yiwu Datuo Equity Investment 
Partnership (Limited Partnership) (
義烏大拓股權投資合夥企業(有限
合夥)) 
717,879 H Shares 
0.73% 
0.71% 
June 25, 2027 
Yu Li (余麗) 
574,305 H Shares 
0.58% 
0.57% 
June 25, 2027 
Fan Zijing (范子靖) 
358,941 H Shares 
0.37% 
0.35% 
June 25, 2027 
Xiamen Shan’erli Enterprise 
Management Partnership (Limited 
Partnership) (廈門善而利企業管理
合夥企業(有限合夥)) 
241,599 H Shares 
0.25% 
0.24% 
June 25, 2027 
Total 
42,186,922 Shares 
(including 
39,329,882 H 
Shares and 
2,857,040 
Domestic Shares) 
40.02% 
41.72% 
- 
 
Notes: 
1. Pursuant to the applicable PRC laws, all existing Shareholders are not permitted to dispose of any of the Shares 
held by them within 12 months following the Listing Date. 
 
PLACEE CONCENTRATION ANALYSIS  
Placees* 
Number of H Shares 
allotted 
Allotment as % of 
International Offering  
Allotment as % of total 
Offer Shares  
Number of H Shares 
held upon Listing 
% of total issued share 
capital upon Listing  
Top 1 
1,769,880 
19.45% 
17.50% 
1,769,880 
1.75% 
Top 5 
4,848,060 
53.27% 
47.94% 
4,848,060 
4.79% 
Top 10 
6,012,660 
66.07% 
59.46% 
6,012,660 
5.95% 
Top 25 
7,679,820 
84.38% 
75.95% 
7,679,820 
7.59% 
 
* 
Ranking of placees is based on the number of Offer Shares allotted to the placees. 
 
H SHAREHOLDER CONCENTRATION ANALYSIS  
H Shareholders* 
Number of H 
Shares allotted 
Allotment as % of 
International Offering  
Allotment as % of total 
Offer Shares 
Number of H Shares 
held upon Listing 
% of total issued share 
capital upon Listing  

<<<PAGE 9>>>
 
 
9 
 
Top 1 
0 
0.00% 
0.00% 
48,823,407 
48.28% 
Top 5 
0 
0.00% 
0.00% 
77,521,368 
76.66% 
Top 10 
1,769,880 
19.45% 
17.50% 
90,887,485 
89.88% 
Top 25 
6,341,280 
69.68% 
62.71% 
97,351,609 
96.27% 
 
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholder upon Listing. 
 
SHAREHOLDER CONCENTRATION ANALYSIS 
Shareholders* 
Number of H 
Shares allotted 
Allotment as % of 
International 
Offering  
Allotment as % of 
total Offer Shares  
Number of H 
Shares held upon 
Listing 
Number of Shares 
held upon Listing 
% of total issued 
share capital upon 
Listing  
Top 1 
0 
0.00% 
0.00% 
48,823,407 
  
48,823,407 
48.28% 
Top 5 
0 
0.00% 
0.00% 
74,664,328 
  
77,521,368 
76.66% 
Top 10 
1,769,880 
19.45% 
17.50% 
88,030,445 
  
90,887,485 
89.88% 
Top 25 
6,341,280 
69.68% 
62.71% 
94,494,569 
  
97,351,609 
96.27% 
 
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing. 
 
 

<<<PAGE 10>>>
 
 
10 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING  
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 165,737 valid 
applications made by the public will be conditionally allocated on the basis set out below: 
Pool A 
Number of 
H Shares 
applied for 
Number of 
valid 
applications 
Basis of allocation/ballot 
Approximate 
percentage allotted 
of the total number 
of H Shares 
applied for 
60 
69,554 
1,392 out of 69,554 applicants to receive 60 H Shares 
2.00% 
120 
8,618 
230 out of 8,618 applicants to receive 60 H Shares 
1.33% 
180 
24,472 
772 out of 24,472 applicants to receive 60 H Shares 
1.05% 
240 
9,964 
354 out of 9,964 applicants to receive 60 H Shares 
0.89% 
300 
2,988 
117 out of 2,988 applicants to receive 60 H Shares 
0.78% 
360 
959 
41 out of 959 applicants to receive 60 H Shares 
0.71% 
420 
651 
30 out of 651 applicants to receive 60 H Shares 
0.66% 
480 
755 
36 out of 755 applicants to receive 60 H Shares 
0.60% 
540 
736 
37 out of 736 applicants to receive 60 H Shares 
0.56% 
600 
6,486 
337 out of 6,486 applicants to receive 60 H Shares 
0.52% 
900 
1,933 
119 out of 1,933 applicants to receive 60 H Shares 
0.41% 
1,200 
8,050 
556 out of 8,050 applicants to receive 60 H Shares 
0.35% 
1,500 
1,661 
126 out of 1,661 applicants to receive 60 H Shares 
0.30% 
1,800 
959 
79 out of 959 applicants to receive 60 H Shares 
0.27% 
2,100 
709 
62 out of 709 applicants to receive 60 H Shares 
0.25% 
2,400 
2,044 
189 out of 2,044 applicants to receive 60 H Shares 
0.23% 
2,700 
806 
78 out of 806 applicants to receive 60 H Shares 
0.22% 
3,000 
1,944 
197 out of 1,944 applicants to receive 60 H Shares 
0.20% 
4,500 
1,243 
149 out of 1,243 applicants to receive 60 H Shares 
0.16% 
6,000 
1,616 
218 out of 1,616 applicants to receive 60 H Shares 
0.13% 
7,500 
775 
115 out of 775 applicants to receive 60 H Shares 
0.12% 
9,000 
718 
115 out of 718 applicants to receive 60 H Shares 
0.11% 
10,500 
533 
91 out of 533 applicants to receive 60 H Shares 
0.10% 
12,000 
880 
158 out of 880 applicants to receive 60 H Shares 
0.09% 
13,500 
515 
97 out of 515 applicants to receive 60 H Shares 
0.08% 
15,000 
2,230 
438 out of 2,230 applicants to receive 60 H Shares 
0.08% 
30,000 
2,155 
564 out of 2,155 applicants to receive 60 H Shares 
0.05% 
45,000 
1,115 
345 out of 1,115 applicants to receive 60 H Shares 
0.04% 
60,000 
1,039 
362 out of 1,039 applicants to receive 60 H Shares 
0.03% 
75,000 
513 
197 out of 513 applicants to receive 60 H Shares 
0.03% 
90,000 
496 
205 out of 496 applicants to receive 60 H Shares 
0.03% 
105,000 
434 
191 out of 434 applicants to receive 60 H Shares 
0.03% 
120,000 
925 
430 out of 925 applicants to receive 60 H Shares 
0.02% 
Total 
 158,476  Total number of Pool A successful applicants: 8,427 
 
 
 
 
 
 
 
 

<<<PAGE 11>>>
 
 
11 
 
Pool B 
Number of 
H Shares 
applied for 
Number of 
valid 
applications 
Basis of allocation/ballot 
Approximate 
percentage allotted 
of the total number 
of H Shares 
applied for 
135,000 
2,924 
2,632 out of 2,924 applicants to receive 60 H Shares 
0.04% 
150,000 
2,323 
2,228 out of 2,323 applicants to receive 60 H Shares 
0.04% 
300,000 
779 
60 shares plus 355 out of 779 applicants to receive an 
additional 60 H Shares 
0.03% 
450,000 
207 
60 shares plus 178 out of 207 applicants to receive an 
additional 60 H Shares 
0.02% 
505,620 
1,028 
60 shares plus 1,020 out of 1,028 applicants to receive an 
additional 60 H Shares 
0.02% 
Total 
7,261 
Total numbers of Pool B successful applicants: 6,874 
 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries. 
COMPLIANCE WITH LISTING RULES AND GUIDANCE  
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect 
of which consent has been obtained, the Company has complied with the Listing Rules and 
guidance materials in relation to the placing, allotment and listing of the H Shares. 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.

<<<PAGE 12>>>
 
 
12 
 
DISCLAIMERS 
 
* 
Potential investors of the Offer Shares should note that the Sponsor-OCs (for themselves and on behalf of the 
Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is 
currently expected to be on Friday, June 26, 2026). 
 
 
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly 
disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the 
whole or any part of the contents of this announcement. 
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
The Offer Shares are being offered and sold outside the United States in offshore transactions 
in reliance on Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated June 17, 2026 issued by Keytop Parking 
Inc. for detailed information about the Global Offering described below before deciding whether 
or not to invest in the H Shares thereby being offered. 

<<<PAGE 13>>>
– 13 –
PUBLIC FLOAT AND FREE FLOAT
Pursuant to Rule 19A.13A(1) of the Listing Rules, where the expected market value at the 
time of listing of the H Shares does not exceed HK$6 billion, 25.00% of the total number 
of H Shares must at the time of the Listing be held by the public. Based on an Offer Price 
of HK$39.55 per Offer Share, the market value of H Shares will be HK$3,886.4 million 
(on the basis that the Over-allotment Option is not exercised), and therefore the minimum 
prescribed public float applicable to the Company as required is 25.00%. Immediately upon 
completion of the Global Offering and the Conversion of Domestic Shares into H Shares, 
taking into account 10,112,280 H Shares offered pursuant to the Global Offering (on the 
basis that the Over-allotment Option will not be exercised), an aggregate of 41,791,152 H 
Shares will count towards the public float of the Company, representing 41.33% of the total 
issued share capital of the Company, which is in compliance with the requirement under 
Rule 19A.13A(1) of the Listing Rules.
The H Shares held by all existing Shareholders to be converted from Domestic Shares are 
subject to a lock-up period of 12 months following the Listing Date under the applicable 
PRC laws and shall not be counted towards the free float of the H Shares of the Company at 
the time of Listing. Based on the final Offer Price of HK$39.55 per Offer Share, 10,112,280 
H Shares representing 10.00% of the total number of issued Shares with an expected value 
of approximately HK$399.9 million, will count towards the free float of the Company. 
Therefore, the Company will be able to satisfy the requirement under Rule 19A.13C(1)(a) of 
the Listing Rules.
The Directors confirm that, immediately after the completion of the Global Offering, (i) no 
placee will, individually, be placed more than 10% of the enlarged issued share capital of the 
Company; (ii) there will not be any new substantial shareholder (as defined in the Listing 
Rules) of the Company; (iii) the three largest public shareholders of the Company do not 
hold more than 50% of the H Shares in public hands at the time of the Listing in compliance 
with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 holders 
of H Shares at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, June 
26, 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” 
in the Prospectus has not been exercised. Investors who trade the H Shares on the basis of 
publicly available allocation details prior to the receipt of H Share certificates or prior to the 
H Share certificates becoming valid evidence of title do so entirely at their own risk.

<<<PAGE 14>>>
– 14 –
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Friday, 
June 26, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Friday, June 26, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 60 H Shares each, and the stock code of the H Shares 
will be 2272.
By order of the Board
Keytop Parking Inc.
Sun Longxi
Chairman of the Board and Executive Director
Hong Kong, June 25, 2026
As at the date of this announcement, the Board comprises: (i) Mr. Sun Longxi and Mr. Huang Jinlian as 
executive directors; (ii) Mr. Wang Zhongsheng and Mr. Ye Hua as non-executive directors; and (iii) Dr. Li 
Xiaolin, Dr. Su Xinlong and Mr. Chen Linwei as independent non-executive directors.
