# 配发结果公告抽取任务：2729.HK Zhejiang Galaxis Technology Group Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**23/03/2026 20:38**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0323/2026032301408.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2729.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Zhejiang Galaxis Technology Group Co., Ltd. 
浙江凱樂士科技集團股份有限公司 
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT 
RESULTS 
Unless otherwise defined herein, capitalized terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated March 16, 2026 (the “Prospectus”) 
issued by Zhejiang Galaxis Technology Group Co., Ltd. (浙江凱樂士科技集團股份有限公
司) (the “Company”). 
 
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, Shareholders and prospective investors should be aware that the price 
of the H Shares could move substantially even with a small number of H Shares traded 
and should exercise extreme caution when dealing in the H Shares. 
SUMMARY 
 
Company Information 
Stock Code 
2729 
Stock Short Name 
GALAXIS TECH 
Dealings commencement date 
March 24, 2026* 
* see note at the end of the announcement 
 
Price Information 
Final Offer Price 
HK$16.66 
 
Offer Shares and Share Capital 
Number of Offer Shares 
36,798,000 
Number of Offer Shares in Hong Kong 
Public Offering 
3,679,800 
Number of Offer Shares in International 
Offering 
33,118,200 
Number of issued Shares upon Listing 
427,883,729 
Number of issued Shares upon Listing does not take into account any Shares to be issued 
under the Pre-IPO Share Option Scheme. 
 
 

<<<PAGE 2>>>
Proceeds 
Gross proceeds (Note) 
HK$613.0 million 
Less: Estimated listing expenses 
payable based on Final Offer Price 
HK$(57.3) million 
Net Proceeds 
HK$555.7 million 
Subject to rounding adjustment 
 
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For 
details of the use of proceeds, please refer to the section headed “Future Plans and Use of 
Proceeds” of the Prospectus. The Company will adjust the allocation of the net proceeds for 
the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the 
Prospectus on a pro rata basis.  
 
 

<<<PAGE 3>>>
ALLOTMENT RESULTS DETAILS 
 
HONGKONG PUBLIC OFFERING 
 
No. of valid applications 
107,253 
No. of successful applications 
17,382 
Subscription level  
2153.26 
times 
Reallocation 
N/A 
No. of Offer Shares initially available under the Hong Kong Public 
Offering 
3,679,800 
Final no. of Offer Shares under the Hong Kong Public Offering  
3,679,800 
% of final no. of Offer Shares under the Hong Kong Public Offering to 
the Global Offering  
10% 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, 
investors can refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification 
number or http://www.eipo.com.hk/eIPOAllotment for the full list of allottees. 
 
INTERNATIONAL OFFERING 
 
No. of Placees 
123 
Subscription Level  
3.37 times 
No. of Offer Shares initially available under the International Offering 
33,118,200 
Final no. of Offer Shares under the International Offering  
33,118,200 
% of final no. of Offer Shares under the International Offering to the 
Global Offering  
90% 
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of 
the Offer Shares subscribed by the placees and the public have been financed directly or 
indirectly by the Company, any of the Directors, chief executive of the Company, the Single 
Largest Group of Shareholders, substantial Shareholders, existing Shareholders or any of its 
subsidiaries or their respective close associates; and (ii) none of the placees and the public 
who have purchased the Offer Shares are accustomed to taking instructions from the 
Company, any of the Directors, chief executive of the Company, the Single Largest Group of 
Shareholders, substantial Shareholders, existing Shareholders or any of its subsidiaries or 
their respective close associates in relation to the acquisition, disposal, voting or other 
disposition of H Shares registered in his/her/its name or otherwise held by him/her/it. 
 
 

<<<PAGE 4>>>
LOCK-UP UNDERTAKINGS 
Pre-Listing Concert Parties 
Name 
Number of H 
Shares held in the 
Company subject 
to lock-up 
undertakings upon 
Listing 
% of shareholding in the 
Company subject to lock-
up undertakings upon 
Listing 
Last day subject 
to the lock-up 
undertakings Note1 
Dr. GU 
22,696,560 
5.30% 
March 23, 2027 
Ms. MA Lan 
558,000 
0.13% 
March 23, 2027 
Jiaxing Jiumai 
13,331,880 
3.12% 
March 23, 2027 
Jiaxing Huige 
22,053,960 
5.15% 
March 23, 2027 
Jiaxing Rongming 
33,081,120 
7.73% 
March 23, 2027 
Jiaxing Gaile 
24,935,040 
5.83% 
March 23, 2027 
Jointown 
Pharmaceutical 
15,622,560 
3.65% 
March 23, 2027 
China Merchants 
Advanced 
Technology 
25,328,160 
5.92% 
March 23, 2027 
Total 
157,607,280 
36.83% 
 
Notes:  
 
1. The expiry day of the lock-up period shown in the table above is pursuant to the PRC 
Company Law. In accordance with the relevant Listing Rules/guidance materials, the 
required lock-up for existing Shareholders ends on September 23, 2026, being 6 months 
following the Listing Date 
 
2. For details on the background of the Pre-Listing Concert Parties, please refer to the 
paragraphs headed “History, Development and Corporate Structure — Acting-in-
concert and Single Largest Group of Shareholders. 
 
 
 
 

<<<PAGE 5>>>
Pre-IPO Investors 
Name 
Number of H 
Shares held in the 
Company subject 
to lock-up 
undertakings 
upon Listing 
% of shareholding in the 
Company subject to lock-
up undertakings upon 
Listing 
Last day subject 
to the lock-up 
undertakings Note1 
Qijiang 
24,324,480 
5.68% 
March 23, 2027 
Qilu 
15,362,640 
3.59% 
March 23, 2027 
S.F. Technology 
33,081,120 
7.73% 
March 23, 2027 
Suzhou Huidao 
22,053,960 
5.15% 
March 23, 2027 
Suzhou Guyu 
3,088,800 
0.72% 
March 23, 2027 
TopView Innovation 
22,660,200 
5.30% 
March 23, 2027 
Oriza PE 
17,552,520 
4.10% 
March 23, 2027 
Anhui Cornerstone  
5,586,939 
1.31% 
March 23, 2027 
Linghui Cornerstone 
5,586,939 
1.31% 
March 23, 2027 
Huagai Tiantou 
10,212,480 
2.39% 
March 23, 2027 
Jiequan Xinnuo  
4,865,040 
1.14% 
March 23, 2027 
Xucun Investment 
4,410,720 
1.03% 
March 23, 2027 
Jiaxing Gencheng 
616,320 
0.14% 
March 23, 2027 
Nanhu Innovation 
Capital 
1,676,082 
1.16% 
March 23, 2027 
Science and 
Technology City 
High Tech 
1,676,082 
0.39% 
March 23, 2027 
Nanhu Jiaxing 
4,966,476 
0.39% 
March 23, 2027 
Beijing Mali 
7,735,320 
1.81% 
March 23, 2027 
Guangzhou Dashen 
7,258,680 
1.70% 
March 23, 2027 
Wuxi Industrial 
Development 
5,586,939 
1.31% 
March 23, 2027 
Yangtze River 
Pharmaceutical 
5,251,723 
1.23% 
March 23, 2027 
Xiamen Delta 
2,837,880 
0.66% 
March 23, 2027 
Suzhou Delta 
2,089,440 
0.49% 
March 23, 2027 
FG Venture 
4,410,720 
1.03% 
March 23, 2027 
Haiju Venture 
Capital 
3,709,727 
0.87% 
March 23, 2027 

<<<PAGE 6>>>
Name 
Number of H 
Shares held in the 
Company subject 
to lock-up 
undertakings 
upon Listing 
% of shareholding in the 
Company subject to lock-
up undertakings upon 
Listing 
Last day subject 
to the lock-up 
undertakings Note1 
Suzhou Jinxin  
1,676,082 
0.39% 
March 23, 2027 
Ningbo Qingkong 
1,621,800 
0.38% 
March 23, 2027 
Sumin Huixin 
3,243,240 
0.76% 
March 23, 2027 
Jiaxing Yukai 
3,141,804 
0.73% 
March 23, 2027 
Mr. HUANG Hong 
2,626,920 
0.61% 
March 23, 2027 
Wanlin International 
2,205,360 
0.52% 
March 23, 2027 
Shanghai 
Zhiyoumaite 
1,216,080 
0.28% 
March 23, 2027 
Xiamen Junshi 
810,720 
0.19% 
March 23, 2027 
Hainan Risinglink 
335,216 
0.08% 
March 23, 2027 
Total 
233,478,449 
54.57% 
 
Notes:  
 
1. The expiry day of the lock-up period shown in the table above is pursuant to the PRC 
Company Law.  
2. For details on the background of the Pre-IPO Investors, please refer to the paragraphs 
headed “History, Development and Corporate Structure — Pre-IPO Investments — 
Information Relating to Our Pre-IPO Investors” in the Prospectus. 
 
 
 
 
 
 

<<<PAGE 7>>>
PLACEE CONCENTRATION ANALYSIS 
Placees 
Number of H Shares 
allotted 
Allotment as % of 
International 
Offering  
Allotment as % of 
total Offer Shares  
Number of H Shares 
held upon Listing 
% of total issued 
share capital upon 
Listing  
Top 1 
2,100,800 
6.34% 
5.71% 
 2,100,800  
0.49% 
Top 5 
9,303,200 
28.09% 
25.28% 
 9,303,200  
2.17% 
Top 10 
17,537,600 
52.95% 
47.66% 
17,537,600  
4.10% 
Top 25 
27,409,800 
82.76% 
74.49% 
27,409,800  
6.41% 
Note 
* Ranking of placees is based on the number of H Shares allotted to the placees. 
H SHAREHOLDERS CONCENTRATION ANALYSIS 
H Shareholders 
Number of H Shares 
allotted 
Allotment as % of 
International 
Offering  
Allotment as % of 
total Offer Shares  
Number of H Shares 
held upon Listing 
% of total issued 
share capital upon 
Listing  
Top 1 
0 
0.00% 
0.00% 
116,656,560  
27.26% 
Top 5 
0 
0.00%  
0.00%  
259,467,120  
60.64% 
Top 10 
0 
0.00%  
0.00%  
323,920,638 
75.70% 
Top 25 
2,100,800 
6.34%  
5.71%  
390,824,513 
91.34% 
Note 
* Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing. 
 
 

<<<PAGE 8>>>
SHAREHOLDERS CONCENTRATION ANALYSIS  
Shareholders 
Number of H 
Shares allotted 
Allotment as % of 
International Offering  
Allotment as % of 
total Offer Shares  
Number of H 
Shares held upon 
Listing 
% of total issued share 
capital upon Listing  
Top 1 
0 
0.00% 
0.00% 
116,656,560  
27.26% 
Top 5 
0 
0.00%  
0.00%  
259,467,120  
60.64% 
Top 10 
0 
0.00%  
0.00%  
323,920,638 
75.70% 
Top 25 
2,100,800 
6.34%  
5.71%  
390,824,513 
91.34% 
Note 
* Ranking of Shareholders is based on the number of H Shares held by the H Shareholders upon Listing. 
 
 

<<<PAGE 9>>>
BASIS OF ALLOCATION UNDER THE HONGKONG PUBLIC OFFERING 
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 107,253 valid 
applications made by the public will be conditionally allocated on the basis set out below: 
 
NO. OF H 
SHARES 
APPLIED FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF 
ALLOTMENT/BALLOT 
APPROXIMATE 
PERCENTAGE 
OF ALLOTED 
SHARES OF 
THE TOTAL 
NO. OF H 
SHARES 
APPLIED FOR 
POOL A 
200 
24,885 
1,245 out of 24,885 to receive 
200 Shares 
5.00% 
400 
22,166 
1,126 out of 22,166 to receive 
200 Shares 
2.54% 
600 
2,881 
148 out of 2,881 to receive 200 
Shares 
1.71% 
800 
1,775 
92 out of 1,775 to receive 200 
Shares 
1.30% 
1,000 
2,538 
134 out of 2,538 to receive 200 
Shares 
1.06% 
1,200 
1,010 
54 out of 1,010 to receive 200 
Shares 
0.89% 
1,400 
1,081 
58 out of 1,081 to receive 200 
Shares 
0.77% 
1,600 
825 
45 out of 825 to receive 200 
Shares 
0.68% 
1,800 
747 
41 out of 747 to receive 200 
Shares 
0.61% 
2,000 
6,652 
374 out of 6,652 to receive 200 
Shares 
0.56% 
3,000 
2,354 
137 out of 2,354 to receive 200 
Shares 
0.39% 
4,000 
1,891 
115 out of 1,891 to receive 200 
Shares 
0.30% 
5,000 
1,234 
78 out of 1,234 to receive 200 
Shares 
0.25% 

<<<PAGE 10>>>
6,000 
811 
53 out of 811 to receive 200 
Shares 
0.22% 
7,000 
936 
64 out of 936 to receive 200 
Shares 
0.20% 
8,000 
696 
49 out of 696 to receive 200 
Shares 
0.18% 
9,000 
623 
45 out of 623 to receive 200 
Shares 
0.16% 
10,000 
4,172 
311 out of 4,172 to receive 200 
Shares 
0.15% 
20,000 
3,012 
284 out of 3,012 to receive 200 
Shares 
0.09% 
30,000 
2,620 
298 out of 2,620 to receive 200 
Shares 
0.08% 
40,000 
1,190 
159 out of 1,190 to receive 200 
Shares 
0.07% 
50,000 
732 
112 out of 732 to receive 200 
Shares 
0.06% 
60,000 
677 
118 out of 677 to receive 200 
Shares 
0.06% 
70,000 
1,280 
248 out of 1,280 to receive 200 
Shares 
0.06% 
80,000 
561 
120 out of 561 to receive 200 
Shares 
0.05% 
90,000 
325 
76 out of 325 to receive 200 
Shares 
0.05% 
100,000 
4,152 
1,056 out of 4,152 to receive 
200 Shares 
0.05% 
200,000 
5,675 
2,560 out of 5,675 to receive 
200 Shares 
0.05% 
 
97,501 
Total number of Pool A 
successful applicants: 9,200 
 
POOL B 
300,000 
4,602 
3,372 out of 4,602 to receive 
200 Shares 
0.05% 
400,000 
1,270 
1,019 out of 1,270 to receive 
200 Shares 
0.04% 

<<<PAGE 11>>>
500,000 
549 
480 out of 549 to receive 200 
Shares 
0.03% 
600,000 
364 
344 out of 364 to receive 200 
Shares 
0.03% 
700,000 
670 
200 Shares 
0.03% 
800,000 
353 
200 Shares plus 31 out of 353 
to receive additional 200 
Shares 
0.03% 
900,000 
139 
200 Shares plus 23 out of 139 
to receive additional 200 
Shares 
0.03% 
1,000,000 
600 
200 Shares plus 140 out of 600 
to receive additional 200 
Shares 
0.02% 
1,200,000 
202 
200 Shares plus 76 out of 202 
to receive additional 200 
Shares 
0.02% 
1,400,000 
203 
200 Shares plus 105 out of 203 
to receive additional 200 
Shares 
0.02% 
1,600,000 
141 
200 Shares plus 93 out of 141 
to receive additional 200 
Shares 
0.02% 
1,839,800 
659 
200 Shares plus 549 out of 659 
to receive additional 200 
Shares 
0.02% 
 
9,752 
Total number of Pool B 
successful applicants: 8,182 
 
As of the date of this announcement, the relevant subscription monies previously deposited in 
the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers  for any inquiries. 
 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect 
of which consent has been obtained, the Company has complied with the Listing Rules and 
guidance materials in relation to the placing, allotment and listing of the Company’s H Shares. 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable. 

<<<PAGE 12>>>
DISCLAIMERS 
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
and Hong Kong Securities Clearing Company Limited take no responsibility for the contents 
of this announcement, make no representation as to its accuracy or completeness and 
expressly disclaim any liability whatsoever for any loss howsoever arising from or in reliance 
upon the whole or any part of the contents of this announcement. 
 
This announcement is not for release, publication, distribution, directly or indirectly, in or 
into the United States (including its territories and possessions, any state of the United States 
and the District of Columbia). This announcement does not constitute or form a part of any 
offer or solicitation to purchase or subscribe for securities in the United States. The 
securities mentioned herein have not been, and will not be, registered under the United 
States Securities Act of 1933, as amended (the “U.S. Securities Act”). The securities may 
not be offered, sold, pledged or otherwise transferred in the United States except pursuant 
to an exemption from the registration requirements of the U.S. Securities Act and in 
compliance with any applicable state securities laws, or outside the United States unless in 
compliance with Regulation S under the U.S. Securities Act. There will be no public offer of 
securities in the United States. 
 
The Offer Shares are being offered and sold outside the United States in offshore 
transactions in reliance on Regulation S under the U.S. Securities Act. 
 
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated March 16, 2026 issued by Zhejiang 
Galaxis Technology Group Co., Ltd. (浙江凱樂士科技集團股份有限公司) for detailed 
information about the Global Offering before deciding whether or not to invest in the H 
Shares thereby being offered. 
 
*Potential investors of the Offer Shares should note that the Joint Sponsors and the Sponsor-
overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall 
be entitled to terminate their obligations under the Hong Kong Underwriting Agreement 
with immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting — Underwriting Arrangements — Hong Kong Public Offering — Hong Kong 
Underwriting Agreement — Grounds for Termination” in the Prospectus at any time prior 
to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
March 24, 2026). 
 
 
 

<<<PAGE 13>>>
PUBLIC FLOAT 
Immediately after the completion of the Global Offering, 256,092,089 H Shares, representing 
approximately 59.85% of the total issued Shares upon Listing (without taking into account any 
Shares to be issued under the Pre-IPO Share Option Scheme), will be counted towards the 
public float of the Company in accordance with Rule 8.08 (as amended and replaced by Rule 
19A.13A) of the Listing Rules, which is higher than the minimum prescribed percentage of 
21.04% of the shares in the relevant class (being H Shares) that must be held by the public 
under Rule 8.08 (as amended and replaced by Rule 19A.13A), thereby satisfying Rule 8.08 (as 
amended and replaced by Rule 19A.13A).  
The Directors confirm that, immediately following completion of the Global Offering: (i) the 
Shares will be held by at least 300 Shareholders at the time of Listing, in compliance with Rule 
8.08(2) of the Listing Rules; (ii) the three largest public Shareholders will not hold more than 
50% of the H Shares held in public hands at the time of Listing, in compliance with Rules 
8.08(3) and 8.24 of the Listing Rules; (iii) no placee will, individually, be placed more than 10% 
of the enlarged issued share capital of the Company immediately after the Global Offering; and 
(iv) there will not be any new substantial Shareholder (as defined in the Listing Rules) 
immediately after the Global Offering. 
Based on the Offer Price of HK$16.66 per H Share, the Company confirmed that it complies 
with the free float requirement under Rule 19A.13C of the Listing Rules.  
COMMENCEMENT OF DEALINGS 
The H Share certificates will only become valid evidence of title at 8:00 a.m. on March 24, 
2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting – Underwriting 
Arrangements – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade the H Shares on the basis of publicly available 
allocation details prior to the receipt of H Share certificates or prior to the H Share certificates 
becoming valid evidence of title do so entirely at their own risk. 
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on March 24, 
2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on March 24, 2026 (Hong Kong time). The H Shares will be 
traded in board lots of 200 H Shares each, and the stock code of the H Shares will be 2729. 
By order of the Board 
Zhejiang Galaxis Technology Group Co., Ltd.  
Dr. GU Chunguang 
Chairperson of the Board, Executive Director and Chief Executive Officer 
 
Hong Kong, March 23, 2026 
As at the date of this announcement, the Board comprises: (i) Dr.GU Chunguang, Dr. YANG 
Yan, Mr. SHEN Lu and Dr. BAI Hongxing as executive Directors; (ii) Mr. SHEN Qi and Mr. 
LI Qiuyu as non-executive directors; and (iii) Dr. HU Jianqiang, Mr. MO Rong and Mr. LAU 
Hak Lap as independent non-executive Directors. 
