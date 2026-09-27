# 配发结果公告抽取任务：2706.HK Beijing Haizhi Technology Group Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**12/02/2026 21:11**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0212/2026021201324.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2706.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for the Offer 
Shares in the United States or in any other jurisdictions. The Offer Shares have not been, and will not be, registered 
under the United States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or securities 
law of any state or other jurisdiction of the United States. The Offer Shares may not be offered, sold, pledged or 
otherwise transferred within the United States, except pursuant to an exemption from the registration requirements 
of the U.S. Securities Act, and in compliance with any applicable state securities laws. The Offer Shares are being 
offered and sold outside the United States to investors that are not U.S. persons nor persons acquiring for the account 
or benefit of U.S. persons in reliance on Regulation S under the U.S. Securities Act. There will be no public offer of 
the Offer Shares in the United States.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
February 5, 2026 (the “Prospectus”) issued by Beijing Haizhi Technology Group Co., Ltd. (北京海致科技集團股份有
限公司) (the “Company”) for detailed information about the Global Offering described below before deciding whether 
or not to invest in the H Shares thereby being offered. Any investment decision in relation to the Offer Shares should 
be taken solely in reliance on the information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
No stabilizing manager will be appointed, and it is anticipated that no stabilization activities will be carried out in 
relation to the Global Offering.
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on behalf of 
the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
Friday, February 13, 2026).

<<<PAGE 2>>>
2
Beijing Haizhi Technology Group Co., Ltd.
北京海致科技集團股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the
Global Offering
:
28,030,200 H Shares
Number of Hong Kong Offer Shares
:
2,803,200 H Shares
Number of International Offer Shares
:
25,227,000 H Shares
Final Offer Price
:
HK$27.06 per H Share, plus brokerage
 of 1.0%, SFC transaction levy of
 0.0027%, Hong Kong Stock Exchange
 trading fee of 0.00565% and AFRC
 transaction levy of 0.00015% (payable
 in full on application in Hong Kong
 dollars and subject to refund)
Nominal value
:
RMB0.1 per H Share
Stock code
:
2706
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
1 
 
BEIJING HAIZHI TECHNOLOGY GROUP CO., LTD. 
北京海致科技集團股份有限公司 
ANNOUNCEMENT OF FINAL OFFER PRICE AND  
ALLOTMENT RESULTS 
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same meanings as 
those defined in the prospectus dated February 5, 2026 (the “Prospectus”) issued by Beijing Haizhi Technology 
Group Co., Ltd. (the “Company”). 
 
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could move 
substantially even with a small number of H Shares traded and should exercise extreme caution when 
dealing in the H Shares. 
SUMMARY 
Company Information 
Stock Code 
2706 
Stock short name 
HAIZHI TECH GP 
Dealings commencement date 
February 13, 2026 
*see note at the end of the announcement 
Price Information 
Final Offer Price 
HK$27.06 
 
Offer Shares and Share Capital 
Number of Offer Shares 
28,030,200 
Number of Offer Shares in Hong Kong Public Offering 
2,803,200 
Number of Offer Shares in International Offering 
25,227,000 
Number of issued Shares upon Listing  
400,430,680 
Number of issued Shares upon Listing does not take into account any Shares to be issued under the Pre-
IPO Share Option Scheme. 
 
Proceeds 
Gross proceeds (Note) 
HK$758.5 million 
Less: Estimated listing expenses payable based on Final 
Offer Price 
HK$(103.1) million 
Net proceeds 
HK$655.4 million 
 
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. 
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING 
 
No. of valid applications 
232,258 

<<<PAGE 4>>>
2 
 
No. of successful applications 
14,016 
Subscription level  
5,065.06 times 
Claw-back triggered 
N/A 
No. of Offer Shares initially available under the Hong Kong Public 
Offering 
2,803,200 
Final no. of Offer Shares under the Hong Kong Public Offering 
2,803,200  
% of Offer Shares under the Hong Kong Public Offering to the Global 
Offering 
10% 
% of final no. of Offer Shares under the Hong Kong Public Offering to 
the Global Offering 
10% 
 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.eipo.com.hk to perform a search by identification document number or www.eipo.com.hk for the full list of 
allottees. 
INTERNATIONAL OFFERING 
 
No. of placees 
120 
Subscription Level  
8.39 times 
No. of Offer Shares initially available under the International Offering 25,227,000 
Final no. of Offer Shares under the International Offering  
25,227,000  
% of Offer Shares under the International Offering to the Global 
Offering  
90% 
% of final no. of Offer Shares under the International Offering to the 
Global Offering 
90% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange 
to permit the Company to allocate certain Offer Shares in the International Offering to a close associate of an 
existing Shareholder as a cornerstone investor, (i) none of the Offer Shares subscribed by the placees and the 
public have been financed directly or indirectly by the Company, any of the Directors, chief executive of the 
Company, substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or their 
respective close associates; and (ii) none of the placees and the public who have purchased the Offer Shares are 
accustomed to taking instructions from the Company, any of the Directors, chief executive of the Company, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates in relation to the acquisition, disposal, voting or other disposition of H Shares registered in 
his/her/its name or otherwise held by him/her/it. 
The placees in the International Offering include the following: 
Cornerstone Investors  

<<<PAGE 5>>>
3 
 
Investor 
No. of Offer 
Shares allocated 
% of offer shares 
(without taking into 
account any Shares to 
be issued under the Pre-
IPO Share Option 
Scheme) 
% of total issued share 
capital in the Company 
after the Global 
Offering (without taking 
into account any Shares 
to be issued under the 
Pre-IPO Share Option 
Scheme) 
Existing 
shareholders or 
their close 
associates 
JSC International 
Investment Fund SPC 
(acting for and on 
behalf of Etown SP) 
Note 1 
1,426,200 
5.09% 
0.36% 
Yes 
JINGSHENG 
HENGXING 
TECHNOLOGY PTE. 
LTD. 
1,152,400 
4.11% 
0.29% 
No 
Infini Global Master 
Fund 
864,400 
3.08% 
0.22% 
No 
Mega Prime 
Development Limited 
864,400 
3.08% 
0.22% 
No 
Total 
4,307,400 
15.37% 
1.08% 
 
Notes: 
1. As disclosed in the section headed "Cornerstone Investors" in the Prospectus, E-Town Capital is the
general partner of Industrial Upgrade Fund II, one of an existing Shareholders and Industrial Upgrade
Fund II is ultimately controlled and owned by Beijing Economic-Technological Development Area
Finance and State Owned Assets Supervision and Administration Bureau. Therefore, JSC Yizhi which is
the beneficial owner of Etown SP is a close associate of Industrial Upgrade Fund II pursuant to Rule
1.01 of the Listing Rules as it is a fellow subsidiary of the holding company of Industrial Upgrade Fund
II. For details of the prior consent under paragraph 1C(2) of the Placing Guidelines in relation to
subscription for H Shares by a close associate of an existing Shareholder, please refer to the section
headed “Others/ Additional Information — Placing to a close associate of an existing Shareholder as a
cornerstone investor” in this announcement. 
 
Allotees with Consents Obtained 
Investor 
No. of Offer 
Shares 
allocated 
% of offer shares 
(without taking into 
account any Shares 
to be issued under 
the Pre-IPO Share 
Option Scheme) 
% of total issued H Shares after the 
Global Offering (without taking into 
account any Shares to be issued under 
the Pre-IPO Share Option Scheme) Note 2 Relationship
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for 
New Listing Applicants in relation to allocations to connected clients Note 2 

<<<PAGE 6>>>
4 
 
CMBI (Singapore) 
Pte. Limited 
3,600 
0.013% 
0.00090% Connected 
client 
Bosera Asset 
Management 
(International) Co., 
Limited 
3,400 
0.012% 
0.00085% Connected 
client 
Funde Ivy OFC-
Funde Pioneers 
Equity Sub-Fund 
20,200 
0.072% 
0.00504% Connected 
client 
Haitong Global 
Investment SPC IV 
- Haitong 
Opportunity Fund II 
S.P. 
200 
0.001% 
0.00005% Connected 
client 
CITIC Securities 
Asset Management 
Company Limited 
200 
0.001% 
0.00005% Connected 
client 
CITIC Securities 
Asset management 
(HK) Limited 
200 
0.001% 
0.00005% Connected 
client 
CITIC Securities 
International Capital 
Management 
Limited 
200 
0.001% 
0.00005% Connected 
client 
Notes: 
1. For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations to connected clients, please refer to the 
section headed “Others / Additional Information – Placing to connected clients with a prior consent 
under paragraph 1C(1) of the Placing Guidelines” in this announcement. 
 
 
 

<<<PAGE 7>>>
5 
 
LOCK-UP UNDERTAKINGS 
Existing Shareholders 
Name 
Number of H Shares held 
in the Company subject to 
lock-up undertakings 
upon Listing 
% of total issued share 
capital in the Company 
subject to lock-up 
undertakings upon Listing 
(without taking into 
account any Shares to be 
issued under the Pre-IPO 
Share Option Scheme) 
Last day subject to the 
lock-up undertakingsNote 1 
Beijing Haikuo Fenxiang 
Business Consulting 
Partnership (Limited 
Partnership) (北京海闊分
享商務諮詢合夥企業(有
限合夥)) 
39,495,420 
9.86% 
February 12, 2027 
Beijing Haikuo 
Chengzhang Business 
Consulting Partnership 
(Limited Partnership) (北
京海闊成長商務諮詢合夥
企業(有限合夥)) 
30,829,450 
7.70% 
February 12, 2027 
Ren Xuyang (任旭陽) 
21,559,630 
5.38% 
February 12, 2027 
Yang Zaifei (楊再飛) 
17,794,530 
4.44% 
February 12, 2027 
LC ELITE LIMITED 
20,682,270 
5.17% 
February 12, 2027 
Suzhou Junlian Xiangdao 
Equity Investment 
Partnership (Limited 
Partnership) (蘇州君聯相
道股權投資合夥企業(有
限合夥)) 
22,696,270 
5.67% 
February 12, 2027 
Xiamen Junlian Yihe 
Venture Capital 
Partnership (Limited 
Partnership) (廈門君聯逸
禾創業投資合夥企業(有
限合夥)) 
3,693,260 
0.92% 
February 12, 2027 
Suzhou Junjunde Equity 
Investment Partnership 
(Limited Partnership) (蘇
州君駿德股權投資合夥企
業(有限合夥)) 
3,693,260 
0.92% 
February 12, 2027 

<<<PAGE 8>>>
6 
 
BAI GmbH 
24,224,340 
6.05% 
February 12, 2027 
SKY FINE LIMITED 
18,111,840 
4.52% 
February 12, 2027 
Yifang Technology Group, 
Ltd. 
15,036,110 
3.75% 
February 12, 2027 
China Internet Investment 
Fund (Limited Partnership) 
(中國互聯網投資基金(有
限合夥)) 
14,674,230 
3.66% 
February 12, 2027 
Shi Youcai (史有才) 
11,240,530 
2.81% 
February 12, 2027 
Beijing Information 
Industry Development 
Investment Fund (L.P.) (北
京信息產業發展投資基金
(有限合夥)) 
11,284,870 
2.82% 
February 12, 2027 
Hillhouse HZH HK 
Holdings Limited (高瓴海
致香港控股有限公司) 
9,479,370 
2.37% 
February 12, 2027 
Zhuhai Cheheng Equity 
Investment Partnership 
(Limited Partnership) (珠
海徹恒股權投資合夥企業
(有限合夥)) 
4,315,180 
1.08% 
February 12, 2027 
Beijing Weizhi Digital 
Investment Center 
(Limited Partnership) (北
京微智數科投資中心(有
限合夥)) 
6,771,780 
1.69% 
February 12, 2027 
Shanghai Artificial 
Intelligence Industry 
Equity Investment Fund 
Partnership (Limited 
Partnership) (上海人工智
能產業股權投資基金合夥
企業(有限合夥)) 
7,337,120 
1.83% 
February 12, 2027 
Yang Juan (楊娟) 
4,935,070 
1.23% 
February 12, 2027 
Xi’an Junlian Haiying 
Equity Investment 
Partnership (Limited 
Partnership) (西安君聯海
盈股權投資合夥企業(有
限合夥)) 
5,574,310 
1.39% 
February 12, 2027 

<<<PAGE 9>>>
7 
 
Wan Pengjiang (萬澎江) 
4,697,820 
1.17% 
February 12, 2027 
Jiaxing Chenyu Equity 
Investment Partnership 
(Limited Partnership) (嘉
興宸鈺股權投資合夥企業
(有限合夥)) 
4,308,810 
1.08% 
February 12, 2027 
Shanghai Guohe Phase III 
Modern Service Industry 
Equity Investment Fund 
Partnership (Limited 
Partnership) (上海國和三
期現代服務業股權投資基
金合夥企業(有限合夥)) 
5,642,590 
1.41% 
February 12, 2027 
Shanghai Fintech Equity 
Investment Fund (Limited 
Partnership) (上海金融科
技股權投資基金(有限合
夥)) 
2,821,300 
0.70% 
February 12, 2027 
Formation8 Partners Fund 
I, L.P. 
3,791,750 
0.95% 
February 12, 2027 
Hu Song (胡嵩) 
3,177,220 
0.79% 
February 12, 2027 
Wuxi Yicun Juancheng 
Investment Partnership 
(Limited Partnership) (無
錫一村雋澄投資合夥企業
(有限合夥)) 
3,385,890 
0.85% 
February 12, 2027 
TAL China Focus Master 
Fund 
3,668,550 
0.92% 
February 12, 2027 
TAL Global Opportunities 
Master Fund 
3,668,550 
0.92% 
February 12, 2027 
Magic Stone Hong Tao 
Alternative Fund, L.P. 
2,585,280 
0.65% 
February 12, 2027 
Foshan Datai Venture 
Investment Center 
(Limited Partnership) (佛
山達泰創業投資中心(有
限合夥)) 
2,505,130 
0.63% 
February 12, 2027 
Chen Liang (陳亮) 
2,179,040 
0.54% 
February 12, 2027 

<<<PAGE 10>>>
8 
 
Qu Ke (瞿珂) 
2,179,040 
0.54% 
February 12, 2027 
Hundsun Technologies Inc. 
(恒生電子股份有限公司) 
1,910,420 
0.48% 
February 12, 2027 
Wind Information (HK) 
Company Limited 
1,895,950 
0.47% 
February 12, 2027 
Shanghai Hehua Equity 
Investment Fund Co., Ltd. 
(上海荷花股權投資基金
有限公司) 
474,860 
0.12% 
February 12, 2027 
Shanghai Taomin 
Information Technology 
Co., Ltd. (上海濤敏信息
科技有限公司) 
1,128,630 
0.28% 
February 12, 2027 
Beijing Wandian Family 
Office Consulting Co., Ltd. 
(北京萬點家辦諮詢有限
公司) 
738,650 
0.18% 
February 12, 2027 
Beijing Economic and 
Technological 
Development Zone 
Industrial Upgrade Equity 
Investment Fund II 
(Limited Partnership) (北
京經濟技術開發區產業升
級股權投資基金二期(有
限合夥)) 
16,927,290 
4.23% 
February 12, 2027 
Beijing Artificial 
Intelligence Industry 
Investment Fund (Limited 
Partnership) (北京市人工
智能產業投資基金(有限
合夥)) 
11,284,870 
2.82% 
February 12, 2027 
Total 
372,400,480 
93.00% 
 
Notes: 
1. The expiry day of the lock-up period shown in the table above is pursuant to the PRC Company Law. 
2. For details on the background of other Pre-IPO Investors, please refer to the paragraphs headed 
“History, Development and Corporate Structure — Pre-IPO Investments — Information About Our 
Major Pre-IPO Investors” in the Prospectus. 
 
Cornerstone Investors 

<<<PAGE 11>>>
9 
 
Name 
Number of H Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing 
% of offer shares 
(without taking into 
account any Shares 
to be issued under the 
Pre-IPO Share 
Option Scheme) 
% of total issued 
share capital in the 
Company subject to 
lock-up undertakings 
upon Listing (without 
taking into account 
any Shares to be 
issued under the Pre-
IPO Share Option 
Scheme) 
Last day subject to 
the lock-up 
undertakingsNote 1 
JSC International 
Investment Fund 
SPC (acting for and 
on behalf of Etown 
SP) 
1,426,200 
5.09% 
0.36% 
January 12, 2027 
JINGSHENG 
HENGXING 
TECHNOLOGY 
PTE. LTD. 
1,152,400 
4.11% 
0.29% November 12, 2026 
Infini Global Master 
Fund 
864,400 
3.08% 
0.22% 
August 12, 2026 
Mega Prime 
Development 
Limited 
864,400 
3.08% 
0.22% 
August 12, 2026 
Total 
4,307,400 
15.37% 
1.08% 
 
Notes: 
1. In accordance with the relevant cornerstone investment agreements, the required lock-up ends on 
January 12, 2027, November 12, 2026 and August 12, 2026, respectively. The Cornerstone Investors 
will cease to be prohibited from disposing of or transferring H Shares subscribed pursuant to the 
relevant cornerstone investment agreements after the indicated date. 
 
 

<<<PAGE 12>>>
10 
 
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
% of total issued H 
share capital upon 
Listing 
% of total issued share 
capital upon Listing 
(without taking into 
account any Shares to 
be issued under the 
Pre-IPO Share Option 
Scheme) 
Top 1 
3,695,400 
14.65% 
13.18% 
3,695,400 
0.92% 
0.92% 
Top 5 
12,933,400 
51.27% 
46.14% 
12,933,400 
3.23% 
3.23% 
Top 10 
19,154,600 
75.93% 
68.34% 
36,081,890 
9.01% 
9.01% 
Top 25 
24,299,400 
96.32% 
86.69% 
41,226,690 
10.30% 
10.30% 
 
Note: 
* 
Ranking of placees is based on the number of H Shares allotted to the placees. 
 
 

<<<PAGE 13>>>
11 
 
H SHAREHOLDER CONCENTRATION ANALYSIS  
H 
Shareholders 
* 
Number of H Shares 
allotted 
Allotment as % of 
International Offering  
Allotment as % of total 
Offer Shares  
Number of H Shares 
held upon Listing 
% of total issued H 
share capital upon 
Listing 
% of total issued share 
capital upon Listing 
(without taking into 
account any Shares to 
be issued under the 
Pre-IPO Share Option 
Scheme) 
Top 1 
- 
0.00% 
0.00% 
39,495,420 
9.86% 
9.86% 
Top 5 
- 
0.00% 
0.00% 
138,805,110 
34.66% 
34.66% 
Top 10 
1,426,200 
5.65% 
5.09% 
228,783,350 
57.13% 
57.13% 
Top 25 
5,121,600 
20.30% 
18.27% 
337,817,050 
84.36% 
84.36% 
 
Note: 
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing. 
 
 

<<<PAGE 14>>>
12 
 
SHAREHOLDER CONCENTRATION ANALYSIS 
Shareholders* 
Number of H Shares 
allotted 
Allotment as % of 
International Offering  
Allotment as % of 
total Offer Shares 
Number of H 
Shares held upon 
Listing 
Number of Shares 
held upon Listing 
% of total issued share capital 
upon Listing (without taking 
into account any Shares to be 
issued under the Pre-IPO 
Share Option Scheme) 
Top 1 
- 
0.00% 
0.00% 
39,495,420 
9.86% 
9.86% 
Top 5 
- 
0.00% 
0.00% 
138,805,110 
34.66% 
34.66% 
Top 10 
1,426,200 
5.65% 
5.09% 
228,783,350 
57.13% 
57.13% 
Top 25 
5,121,600 
20.30% 
18.27% 
337,817,050 
84.36% 
84.36% 
 
Note: 
* 
Ranking of Shareholders is based on the aggregate of, where applicable, the number of H Shares held by the Shareholders upon Listing. 

<<<PAGE 15>>>
13 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 232,258 valid 
applications made by the public will be conditionally allocated on the basis set out below:  
 
 
Approximate 
 
 
Pool A 
percentage 
 
 
allotted of the 
Number of 
Number 
total number of 
H Shares 
of valid 
H Shares applied 
applied for 
applications 
Basis of allocation/ballot 
for 
200 
82,364 
50 out of 82,364 to receive 200 Shares 
0.06% 
400 
12,074 
14 out of 12,074 to receive 200 Shares 
0.06% 
600 
7,116 
13 out of 7,116 to receive 200 Shares 
0.06% 
800 
5,818 
14 out of 5,818 to receive 200 Shares 
0.06% 
1,000 
5,850 
17 out of 5,850 to receive 200 Shares 
0.06% 
1,200 
2,848 
10 out of 2,848 to receive 200 Shares 
0.06% 
1,400 
2,009 
8 out of 2,009 to receive 200 Shares 
0.06% 
1,600 
11,123 
53 out of 11,123 to receive 200 Shares 
0.06% 
1,800 
2,433 
13 out of 2,433 to receive 200 Shares 
0.06% 
2,000 
8,928 
53 out of 8,928 to receive 200 Shares 
0.06% 
3,000 
6,332 
57 out of 6,332 to receive 200 Shares 
0.06% 
4,000 
4,198 
50 out of 4,198 to receive 200 Shares 
0.06% 
5,000 
2,952 
44 out of 2,952 to receive 200 Shares 
0.06% 
6,000 
2,523 
45 out of 2,523 to receive 200 Shares 
0.06% 
7,000 
2,128 
44 out of 2,128 to receive 200 Shares 
0.06% 
8,000 
1,851 
44 out of 1,851 to receive 200 Shares 
0.06% 
9,000 
1,906 
51 out of 1,906 to receive 200 Shares 
0.06% 
10,000 
9,179 
274 out of 9,179 to receive 200 Shares 
0.06% 
20,000 
6,641 
396 out of 6,641 to receive 200 Shares 
0.06% 
30,000 
4,379 
392 out of 4,379 to receive 200 Shares 
0.06% 
40,000 
3,481 
415 out of 3,481 to receive 200 Shares 
0.06% 
50,000 
2,604 
388 out of 2,604 to receive 200 Shares 
0.06% 
60,000 
2,069 
370 out of 2,069 to receive 200 Shares 
0.06% 
70,000 
1,838 
384 out of 1,838 to receive 200 Shares 
0.06% 
80,000 
1,616 
385 out of 1,616 to receive 200 Shares 
0.06% 
90,000 
1,274 
342 out of 1,274 to receive 200 Shares 
0.06% 
100,000 
10,338 
3,082 out of 10,338 to receive 200 Shares 
0.06% 
 
205,872 
  
Total number of Pool A successful applicants: 7,008 
 
 
 
 

<<<PAGE 16>>>
14 
 
 
 
Pool B 
Approximate 
 
 
percentage 
 
 
allotted of the 
Number 
Number 
total number of 
of H Shares 
of valid 
H Shares applied 
applied for 
applications 
Basis of allocation/ballot 
for 
200,000 
11,891 
1,408 out of 11,891 to receive 200 Shares 
0.01% 
300,000 
3,920 
696 out of 3,920 to receive 200 Shares 
0.01% 
400,000 
2,626 
621 out of 2,626 to receive 200 Shares 
0.01% 
500,000 
1,464 
433 out of 1,464 to receive 200 Shares 
0.01% 
600,000 
1,170 
415 out of 1,170 to receive 200 Shares 
0.01% 
700,000 
869 
360 out of 869 to receive 200 Shares 
0.01% 
800,000 
765 
362 out of 765 to receive 200 Shares 
0.01% 
900,000 
446 
237 out of 446 to receive 200 Shares 
0.01% 
1,000,000 
479 
283 out of 479 to receive 200 Shares 
0.01% 
1,100,000 
267 
174 out of 267 to receive 200 Shares 
0.01% 
1,200,000 
257 
182 out of 257 to receive 200 Shares 
0.01% 
1,300,000 
219 
168 out of 219 to receive 200 Shares 
0.01% 
1,401,600 
2,013 
1,669 out of 2,013 to receive 200 Shares 
0.01% 
 
26,386 
 
360 out of 869 to receive 200 Shares 
 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries. 
 

<<<PAGE 17>>>
15 
 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of which 
consent has been obtained, the Company has complied with the Listing Rules and guidance materials in 
relation to the placing, allotment and listing of the Company’s H Shares. 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the 
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by 
them was the same as the final Offer Price in addition to any brokerage, AFRC transaction levy, SFC 
transaction levy and trading fee payable. 
OTHERS / ADDITIONAL INFORMATION 
Placing to a close associate of an existing Shareholder as a cornerstone investor 
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a consent 
under paragraph 1C(2) of Appendix F1 to the Listing Rules to allow the JSC International Investment 
Fund SPC (acting for and on behalf of Etown SP) to participate in the Global Offering as a cornerstone 
investor. For details, see the sections headed "Waivers and Exemptions – Placing to a close associate of 
an existing Shareholder as cornerstone investor" and "Cornerstone Investors" in the Prospectus. 
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted by 
the Stock Exchange. 
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates and 
Cornerstone Investors, please refer to the section headed “Allotment Results Details – International 
Offering – Cornerstone Investors” in this announcement. 
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines 
Under the International Offering, certain Offer Shares were placed to connected clients of their connected 
distributors pursuant to the Placing Guidelines. Details of the placement to connected clients are set out 
below. The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, 
consents under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such Offer 
Shares in the International Offering to the connected clients. The allocation of Offer Shares to such 
connected clients is in compliance with all the conditions under the consent granted by the Stock 
Exchange. 
 

<<<PAGE 18>>>
16 
 
Part A - Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties 
 
No. 
Connected 
Distributor 
Connected Client 
Relationship 
with the 
Connected 
Distributor 
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which is 
not authorised 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of 
such scheme  
Number of 
Offer Shares 
allocated to the 
connected 
client 
Approximate 
Percentage of total 
number of Offer 
Shares (without 
taking into account 
any Shares to be 
issued under the 
Pre-IPO Share 
Option Scheme) 
Approximate 
percentage of total 
Shares in issue 
immediately following 
the completion of 
Global Offering 
(without taking into 
account any Shares to 
be issued under the Pre-
IPO Share Option 
Scheme) 
1.  
(1) CMB 
International 
Capital Limited 
("CMB 
International") 
(2) CMB 
International 
Securities 
Limited 
("CMBI 
Securities")  
(3) CMB 
International 
Global Markets 
Limited 
("CMBI 
Global 
Markets", 
together with 
CMBI (Singapore) 
Pte. Limited ("CMBI 
SG")(1) 
CMBI SG is a 
member of the 
same group with 
the CMBI 
Connected 
Distributors and 
CMS. 
N 
3,600 
0.013% 
0.00090% 

<<<PAGE 19>>>
17 
 
CMB 
International 
and CMBI 
Securities, the 
"CMBI 
Connected 
Distributors") 
 
(4) China 
Merchants 
Securities (HK) 
Co., Limited 
("CMS") 
2.  
The CMBI 
Connected 
Distributors 
and CMS 
Bosera Asset 
Management 
(International) Co., 
Limited (“Bosera 
AM”)(2) 
Bosera AM is a 
member of the 
same group with 
the CMBI 
Connected 
Distributors and 
CMS. 
N 
3,400 
0.012% 
0.00085% 
3.  
Funde 
Securities 
Limited 
Funde Ivy OFC-Funde 
Pioneers Equity Sub-
Fund ("Funde 
Pioneers")(3) 
The investment 
manager of 
Funde Pioneers 
is Funde Asset 
Management 
(Hong Kong) 
Company 
Limited, which 
is a subsidiary of 
Funde Holdings 
(Group) Co., 
Ltd. Funde 
Securities 
Limited is also a 
N 
20,200 
0.072% 
0.00504% 

<<<PAGE 20>>>
18 
 
subsidiary of 
Funde Holdings 
(Group) Co., 
Ltd. Therefore, 
Funde Pioneers 
is a member of 
the same group 
with Funde 
Securities 
Limited. 
4.  
Haitong 
International 
Securities 
Company 
Limited 
("Haitong 
International") 
Haitong Global 
Investment SPC IV - 
Haitong Opportunity 
Fund II S.P. ("Haitong 
Opportunity Fund 
II")(4) 
Haitong 
Opportunity 
Fund II S.P. is 
managed by 
Haitong 
International 
Asset 
Management 
(HK) Limited, 
which is a 
member of the 
same group of 
Haitong 
International. 
N 
200 
0.001% 
0.00005% 
5.  
CITIC 
Securities 
Brokerage 
(HK) Limited 
("CSB") 
CITIC Securities Asset 
Management 
Company Limited 
("CITIC AM")(5) 
CITIC AM is a 
member of the 
same group of 
CSB. 
N 
200 
0.001% 
0.00005% 
6.  
CSB 
CITIC Securities Asset 
management (HK) 
Limited ("CITIC AM 
HK")(6) 
CITIC AM HK 
is a member of 
the same group 
of CSB. 
N 
200 
0.001% 
0.00005% 
 
 

<<<PAGE 21>>>
19 
 
Part B - Connected Client holding the beneficial interest of the Offer Shares on a non-discretionary basis on behalf of independent third parties 
No. 
Connected 
Distributor 
Connected Client 
Relationship 
with the 
Connected 
Distributor 
Identities of 
the ultimate 
beneficial 
owners of the 
Offer Shares 
or, where 
applicable, 
details of the 
structured 
products 
under which 
the 
subscription 
by the 
Connected 
Client was 
made (e.g. 
OTC total 
return swaps) 
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which 
is not 
authorised by 
the SFC or is 
expected to 
hold the Offer 
Shares on 
behalf of such 
scheme  
Number of 
Offer Shares 
allocated to 
the 
connected 
client 
Approximate 
Percentage of 
total number of 
Offer Shares 
(without taking 
into account any 
Shares to be 
issued under the 
Pre-IPO Share 
Option Scheme) 
Approximate 
percentage of total 
Shares in issue 
immediately 
following the 
completion of Global 
Offering (without 
taking into account 
any Shares to be 
issued under the Pre-
IPO Share Option 
Scheme) 
1.  
CSB  
CITIC Securities 
International 
Capital 
Management 
Limited ("CSI") 
CSI is a 
member of the 
same group of 
CSB.  
 
Please refer to 
Note (7).  
 
N  
200 
0.001% 
0.00005% 
 
Notes: 
 
(1) CMBI SG, a Singapore licensed fund manager, will hold the Offer Shares on behalf of Joy Dragon International Investment Limited (the "CMBI SG Ultimate Client") 
on a discretionary basis. To the best knowledge, information and belief of CMBI SG after making all reasonable enquiries, the only ultimate beneficial owner of the 
CMBI SG Ultimate Client with 30% or more interest is Huang, De'An Tony, an Independent Third Party. 
 

<<<PAGE 22>>>
20 
 
To the best knowledge, information and belief of CMBI SG after making all reasonable enquiries, the CMBI SG Ultimate Client and its ultimate beneficial owner is an 
independent third party of CMBI SG, the CMBI Connected Distributors, CMS and the companies which are members of the same group of companies as the CMBI 
Connected Distributors and CMS.  
 
(2) Bosera Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf of its underlying client. To the best 
knowledge, information and belief of Bosera AM after due enquiry, the underlying client of Bosera AM is an independent third party of Bosera AM, the CMBI Connected 
Distributors, CMS and the companies which are members of the same group of companies as the CMBI Connected Distributors and CMS. 
 
(3) Funde Pioneers will hold the Offer Shares on behalf of Huang, Jinghua ("Funde Pioneers Ultimate Client") on a discretionary basis. To the best knowledge, information 
and belief of Funde Pioneers after making all reasonable enquiries, the Funde Pioneers Ultimate Client is an independent third party of Funde Pioneers, Funde Securities 
Limited and the companies which are members of the same group of companies as Funde Securities Limited.  
 
(4) Haitong Opportunity Fund II will hold the Offer Shares on behalf of its underlying client on a discretionary basis. To the best knowledge, information and belief of 
Haitong Opportunity Fund II after making all reasonable enquiries, there is no ultimate beneficial owner holding 30% interest or more in such underlying client.  
 
To the best knowledge, information and belief of Haitong Opportunity Fund II after making all reasonable enquiries, its underlying client above is an independent third 
party of Haitong International Asset Management (HK) Limited, Haitong International and the companies which are members of the same group of companies as Haitong 
International.  
 
(5) CITIC AM will hold the Offer Shares on behalf of CITIC SECURITIES AM-GUIBINFENGYUAN NO. 118 QDII (中信证券资管贵宾丰元118 号QDII 集合资产管
理计划) on a discretionary basis. To the best knowledge, information and belief of CITIC AM after making all reasonable enquiries, there is no ultimate beneficial owner 
holding 30% interest or more in such underlying client. 
 
To the best knowledge, information and belief of CITIC AM after making all reasonable enquiries, its underlying client above and the ultimate beneficial owner of such 
underlying client are independent third parties of CITIC AM, CSB and the companies which are members of the same group of companies as CSB. 
 
(6) CITIC AM HK will hold the Offer Shares on behalf of CDNETWORKS HOLDINGS SINGAPORE PTE, LTD. (the "CITIC AM HK Ultimate Client") on a 
discretionary basis. To the best knowledge, information and belief of CITIC AM HK after making all reasonable enquiries, the only ultimate beneficial owner of the 
CITIC AM HK Ultimate Client with 30% or more interest is is Wangsu Science & Technology Co., Ltd. (a company listed on the Shenzhen Stock Exchange, stock code: 
300017). 
 
To the best knowledge, information and belief of CITIC AM HK after making all reasonable enquiries, its underlying client above and the ultimate beneficial owner of 
such underlying client are independent third parties of CITIC AM HK, CSB and the companies which are members of the same group of companies as CSB. 
 
(7) CSI will hold the Offer Shares on behalf of Panjing Hexiang No. 1 Private Equity Investment Fund (盘京贺想1 号私募证券投资基金) and Panjing Yuece No. 1 Private 
Equity Investment Fund (盘京悦策1 号私募证券投资基金) (the "CSI Ultimate Clients"), on a non-discretionary basis, pursuant to which: (i) CSI will act as the single 
counterparty of a back-to-back total return swap transaction (the “CSI Back-to-back TRS”) to be entered into by it in connection with a total return swap order (the “CSI 

<<<PAGE 23>>>
21 
 
Client TRS”) placed and fully funded by the CSI Ultimate Clients, by which CSI will pass the full economic exposure of the Offer Shares placed to CSI to the CSI 
Ultimate Clients; (ii) CSI will hold the legal title and beneficial interest in the Offer Shares, but will contractually agree to pass on the full economic exposure and return 
of the Offer Shares to the CSI Ultimate Clients, on a non-discretionary basis. To the best knowledge, information and belief of CSI after making all reasonable enquiries, 
there is no ultimate beneficial owner holding 30% interest or more in the CSI Ultimate Clients. The investment manager of the CSI Ultimate Clients is Shanghai Panjing 
Investment Management Center (Limited Partnership) (上海盘京投资管理中心（有限合伙）), whose only ultimate beneficial owner of the CMBI SG Ultimate Client 
with 30% or more interest is Zhuang Tao (庄涛), an Independent Third Party. 
 
To the best knowledge, information and belief of CSI after making all reasonable enquiries, the CSI Ultimate Clients and their ultimate beneficial owner are independent 
third parties of CSI, CSB and the companies which are members of the same group of companies as CSB. 
 

<<<PAGE 24>>>
22 
 
DISCLAIMERS 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong Kong 
Securities Clearing Company Limited take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability whatsoever for 
any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe 
for the Offer Shares in the United States or in any other jurisdictions. The Offer Shares have not been, and 
will not be, registered under the United States Securities Act of 1933 as amended from time to time (the 
“U.S. Securities Act”) or securities law of any state or other jurisdiction of the United States. The Offer 
Shares may not be offered, sold, pledged or otherwise transferred within the United States, except pursuant 
to an exemption from the registration requirements of the U.S. Securities Act and U.S. Investment Company 
Act of 1940, as amended (“U.S. Investment Company Act”), and in compliance with any applicable state 
securities laws. There will be no public offer of the Offer Shares in the United States. 
The Offer Shares are being offered and sold outside the United States to investors that are not U.S. persons 
nor persons acquiring for the account or benefit of U.S. persons in reliance on Regulation S under the U.S. 
Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. This announcement is not a prospectus. Potential investors should 
read the Prospectus dated February 5, 2026 issued by Beijing Haizhi Technology Group Co., Ltd. for 
detailed information about the Global Offering described below before deciding whether or not to invest in 
the H Shares thereby being offered. 
*Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators 
(for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence 
of any of the events set out in the section headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Hong Kong Underwriting Agreement – Grounds for Termination” 
in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently 
expected to be on February 13, 2026). 
 
 

<<<PAGE 25>>>
23 
 
PUBLIC FLOAT AND FREE FLOAT 
Immediately after the completion of the Global Offering, 230,353,700 H Shares, representing approximately 
57.53% of the total issued Shares upon Listing (without taking into account any Shares to be issued under the 
Pre-IPO Share Option Scheme), will be counted towards the public float of the Company in accordance with 
Rule 8.08 (as amended and replaced by Rule 19A.13A) of the Listing Rules, which is higher than the minimum 
prescribed percentage of shares in the class to which H shares belong must be H shares held by the public of 
15% under Rule 8.08 (as amended and replaced by Rule 19A.13A), thereby satisfying Rule 8.08 (as amended 
and replaced by Rule 19A.13A). 
Each of the Cornerstone Investors has agreed to a lock-up period of six months or longer following the Listing 
Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be counted towards the 
free float of the H Shares of the Company at the time of Listing. Based on the Offer Price of HK$27.06 per H 
Share, the Company confirmed that it complies with the free float requirement under Rule 19A.13C of the 
Listing Rules.  
The Directors confirm that, immediately following completion of the Global Offering: (i) the Shares will be 
held by at least 300 Shareholders at the time of Listing, in compliance with Rule 8.08(2) of the Listing Rules; 
(ii) the three largest public Shareholders will not hold more than 50% of the H Shares held in public hands at 
the time of Listing, in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; (iii) no place will, 
individually, be placed more than 10% of the enlarged issued share capital of the Company immediately after 
the Global Offering; and (iv) there will not be any new substantial Shareholder (as defined in the Listing 
Rules) immediately after the Global Offering. 
COMMENCEMENT OF DEALINGS 
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, February 13, 
2026 (Hong Kong time), provided that the Global Offering has become unconditional and the right of 
termination described in the section headed “Underwriting – Underwriting Arrangements and Expenses 
– Hong Kong Public Offering – Grounds for Termination” in the Prospectus has not been exercised. 
Investors who trade the H Shares on the basis of publicly available allocation details prior to the receipt 
of H Share certificates or prior to the H Share certificates becoming valid evidence of title do so entirely 
at their own risk. 
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Friday, February 
13, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange will 
commence at 9:00 a.m. on Friday, February 13, 2026 (Hong Kong time). The H Shares will be traded in 
board lots of 200 H Shares each, and the stock code of the H Shares will be 2706. 
By order of the Board  
Beijing Haizhi Technology Group Co., Ltd. 
Mr. Ren Xuyang 
Chairman of the Board and Executive Director 
Beijing, the PRC, February 12, 2026  
As at the date of this announcement, the Board comprises: (i) Mr. Ren Xuyang, Mr. Yang Zaifei, Ms. Yang 
Juan and Mr. Wan Pengjiang as executive Directors; (ii) Mr. Li Jiaqing, Ms. Long Yu and Mr. Li Hongtao as 
non-executive Directors; and (iii) Mr. Zhang Yifan, Mr. Jiang Tian, Mr. Li Shu Pai and Mr. Ma Yeming as 
proposed independent non-executive Directors. 
