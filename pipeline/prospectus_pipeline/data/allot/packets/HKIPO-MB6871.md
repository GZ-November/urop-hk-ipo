# 配发结果公告抽取任务：6871.HK Robotphoenix Intelligent Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**15/05/2026 22:57**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0515/2026051502141.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6871.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
as those defined in the prospectus dated May 8, 2026 (the “Prospectus”) of Robotphoenix Intelligent 
Technology Co., Ltd. (浙江翼菲智能科技股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. This announcement is not a prospectus. Potential investors should read 
the Prospectus for detailed information about the Global Offering described below before deciding whether 
or not to invest in the Offer Shares. Any investment decision in relation to the Offer Shares should be taken 
solely in reliance on the information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe 
for securities in the United States. The securities mentioned herein have not been, and will not be, registered 
under the United States Securities Act of 1933, as amended (the “U.S. Securities Act”). The securities may 
not be offered or sold in the United States except pursuant to an exemption from the registration requirements 
of the U.S. Securities Act and in compliance with any applicable state securities laws, or outside the United 
States unless in compliance with Regulation S under the U.S. Securities Act. There will be no public offer 
of securities in the United States. The Offer Shares are being offered and sold outside the United States in 
offshore transactions in reliance on Regulation S under the U.S. Securities Act.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to term and conditions set 
out in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong 
Kong and/or not resident in Hong Kong.
Potential investors of the Offer Shares should note that the Sole Sponsor and Overall Coordinator (for itself 
and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the 
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out 
in the paragraph headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public 
Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on 
the Listing Date (which is currently expected to be on Monday, May 18, 2026).

<<<PAGE 2>>>
– 2 –
ROBOTPHOENIX INTELLIGENT TECHNOLOGY CO., LTD.
浙江翼菲智能科技股份有限公司
(A joint stock company established in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under the Global 
Offering
:
24,600,000 H Shares
Number of Hong Kong Offer Shares
:
4,920,000 H Shares (as adjusted after 
reallocation)
Number of International Offer Shares
:
19,680,000 H Shares (as adjusted after 
reallocation)
Offer Price
: 
HK$30.5 per H Share (payable in full in Hong 
Kong dollars on application plus brokerage 
of 1%, SFC transaction levy of 0.0027%, 
AFRC transaction levy of 0.00015% and the 
Stock Exchange trading fee of 0.00565% and 
subject to refund)
Nominal value
:
RMB0.25 per H Share
Stock code
:
6871
Sole Sponsor, Sponsor-OC, Overall Coordinator,
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
(in alphabetical order)
Joint Bookrunners and Joint Lead Managers
(in alphabetical order)
Joint Lead Managers
(in alphabetical order)

<<<PAGE 3>>>
– 3 – 
 
 
 
ANNOUNCEMENT OF ALLOTMENT RESULTS 
 
Unless otherwise defined herein, capitalized terms used in this announcement shall have the 
same meanings as those defined in prospectus dated May 8, 2026 (the “Prospectus”) of 
Robotphoenix Intelligent Technology Co., Ltd. (浙江翼菲智能科技股份有限公司) (the 
“Company”). 
 
SUMMARY 
 
Company Information 
Stock code 
6871 
Stock short name 
ROBOTPHOENIX 
Dealings commencement date 
May 18, 2026* 
* 
see note at the end of the announcement 
 
Price Information 
Offer Price 
HK$30.50 
 
Offer Shares and Share Capital 
Number of Offer Shares 
24,600,000 
Number of Offer Shares in Hong Kong Public Offering (after 
reallocation) 
4,920,000 
Number of Offer Shares in International Offering (after 
reallocation) 
19,680,000 
Number of issued Shares upon Listing 
244,953,968 
 
Proceeds 
Gross proceeds (Note) 
HK$750.3 million 
Less: Estimated listing expenses payable based on Offer Price 
HK$77.40 million 
Net proceeds 
HK$ 672.9  million 
 
Note:   Gross proceeds refers to the amount which the Company is entitled to receive. For details of the    use 
of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. 
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, Shareholders and prospective investors should be aware that the 
price   of the H Shares could move substantially even with a small number of H 
Shares traded and should exercise extreme caution when dealing in the H Shares. 

<<<PAGE 4>>>
– 13 – 
 
 
 
ALLOTMENT RESULTS DETAILS 
 
HONG KONG PUBLIC OFFERING 
 
 
No. of valid applications 
330,334 
No. of successful applications 
48,611 
Subscription level 
14,855.40 times 
Claw-back triggered 
Yes 
No. of Offer Shares initially available under the Hong 
Kong Public Offering 
1,230,000 
No. of Offer Shares reallocated from the International 
Offering (claw-back) 
3,690,000 
Final no. of Offer Shares under the Hong Kong Public 
Offering  
4,920,000 
% of Offer Shares under the Hong Kong Public 
Offering to the Global Offering 
20.0% 
 
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by identification number or www.hkeipo.hk/IPOResult 
for the full list of allottees. 
 
 
INTERNATIONAL OFFERING 
 
 
No. of placees 
133 
Subscription Level 
9.77 times 
No. of Offer Shares initially available under the 
International Offering 
23,370,000 
No. of Offer Shares reallocated to the Hong Kong 
Public Offering 
3,690,000 
Final no. of Offer Shares under the International 
Offering 
19,680,000 
% of Offer Shares under the International Offering to 
the Global Offering 
80.0% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for a waiver under Rule 
10.04 of the Listing Rules and consent under paragraph 1C(2) of Appendix F1 to the Listing Rules (the 
“Placing Guidelines”) granted by the Stock Exchange to permit the Company to allocate certain Offer Shares 

<<<PAGE 5>>>
– 14 – 
 
 
in the International Offering to certain existing minority shareholders and/or their close associates as placees, 
(i) none of the Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, Single Largest Group of Shareholders, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates; and (ii) none of the placees and the public who have purchased the Offer Shares are 
accustomed to taking instructions from the Company, any of the Directors, chief executive of the Company, 
Single Largest Group of Shareholders, substantial Shareholders, existing Shareholders of the Company or any 
of its subsidiaries or their respective close associates in relation to the acquisition, disposal, voting or other 
disposition of Shares registered in his/her/its name or otherwise held by him/her/it. 
  
The placees in the International Offering include the following: 
 
Allottees with waiver/consents obtained 
 
Investor 
No. of Offer 
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
capital after 
the Global 
Offering 
Relationship 
Allotees with consent under paragraph 1C(1) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) in relation to allocations to connected clients(Note 
1
CITIC Securities International Capital Management 
Limited (“CSI”)  
2,000 
0.0081% 
0.0008% 
0.0008% 
Connected client as a 
placee 
Grand China Global Master OFC-Grand China 
Investment Fund (“Grand China Global Master”) 
131,100 
0.5329% 
0.0535% 
0.0535% 
Connected client as a 
placee 
China Asset Management (Hong Kong) Limited 
(“China AMC HK”) 
1,200 
0.0049% 
0.0005% 
0.0005% 
Connected client as a 
placee 
Allotee with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the Placing Guidelines in relation to 
allocation to a close associate of existing Shareholders(Note 2) 
Mr. Lv Dalong (呂大龍) (Note 3)  
1,284,000 
5.2195% 
0.5242% 
0.5242% 
An existing Shareholder 
and a close associate of an 
existing Shareholder 
Chuxin Investment Management Limited (Note 4) 
4,800 
0.0195% 
0.0020% 
0.0020% 
A close associate of an 
existing Shareholder 
Notes: 
 
1. 
Saved as listed out, the H Shares placed to such allottees are held on behalf of independent third parties 
(as defined in Chapter 4.15 of the Guide for New Listing Applicants and are in compliance with all the 
conditions under the consent granted by the Stock Exchange. For details of the consent under paragraph 
1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation 
to allocations to connected clients, please refer to the section headed “Additional Information – Placing 
to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines” in this 
announcement. 
 
2. 
For details of the consents under paragraph 1C(2) of the Placing Guidelines and Chapter 4.15 of the 

<<<PAGE 6>>>
– 15 – 
 
 
Guide for New Listing Applicant in relation to allocations to connected clients, please refer to the section 
headed “Additional Information - Placing to existing shareholders and/or its close associates with a prior 
waiver under Rule 10.04 and consent under paragraph 1C(2) of the Placing Guidelines” in this 
announcement. 
 
3. 
Mr. Lv Dalong is an existing Shareholder. Further, the general partner of Qingkong Yinxing (an existing 
Shareholder) is Qingkong Yinxing Venture Investment Management (Beijing) Co., Ltd. (清控銀杏創
業投資管理(北京)有限公司), which is ultimately controlled by Mr. Lv Dalong (呂大龍). Mr. Lv 
Dalong is therefore a close associate of Qingkong Yinxing. 
 
4. 
Xizang Chuzhe Zhixin Equity Investment Partnership (Limited Partnership) (西藏初者之心股權投資
合夥企業(有限合夥)) (“Chuzhe Zhixin”) is an existing Shareholder. The general partner of Chuzhe 
Zhixin is Beijing Chuzhe Zhixin Investment Management Co., Ltd. (北京初心者投资管理有限公司), 
which is in turn ultimately controlled by Ms. Tian Jiangchuan ( 田江川). Chuxin Investment 
Management Limited is wholly owned by Ms. Tian Jiangchuan, and hence it is a close associate of 
Chuzhe Zhixin. 
 
LOCK-UP UNDERTAKINGS 
 
Key Persons (as defined under Rule 18C.14 of the Listing Rules) 
 
 
Name 
Number of H 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing 
% of total 
issued H 
Shares in the 
Company upon 
Listing 
% of total 
issued 
Shares in the 
Company upon 
Listing 
Last day subject 
to the lock-up 
undertakings (Note 1) 
Dr. Zhang Sai (“Dr. Zhang”) 
(Note 2)
24,611,704 
10.05% 
10.05% 
May 17, 2027 
Shaoxing Ziqiu Enterprise 
Management Partnership 
(Limited Partnership) (紹興梓
遒企業管理合夥企業(有限合
夥)) (“Shaoxing Ziqiu LP”) 
(Note 3)
19,310,376 
7.88% 
7.88% 
May 17, 2027 
Shaoxing Yuzhang Enterprise 
Management Partnership 
(Limited Partnership) (紹興宇
章企業管理合夥企業(有限合 
夥)) (“Shaoxing Yuzhang 
LP”) (Note 3) 
6,000,004 
2.45% 
2.45% 
May 17, 2027 
Shaoxing Zhiqiu Enterprise 
Management Partnership 
(Limited Partnership) (紹興知
秋企業管理合夥企業(有限合
夥)) (“Shaoxing Zhiqiu 
5,318,548 
2.17% 
2.17% 
May 17, 2027 

<<<PAGE 7>>>
– 16 – 
 
 
LP”) (Note 3) 
Subtotal 
55,240,632 
22.55% 
22.55% 
Notes: 
 
1. 
Pursuant to the applicable PRC law, within the 12 months following the Listing Date, all existing 
Shareholders (including the Pre-IPO Investors) are prohibited from disposing of any of the Shares held 
by them. Pursuant to Rule 18C.14(1) of the Listing Rules, the required lock-up period commences    on 
the date by reference to which disclosure of their shareholdings in the Company is made in the 
Prospectus and end on the date upon the expiry of 12 months from the Listing Date, being the same date 
on which the restriction against disposal of Shares under the applicable PRC laws ends. 
 
2. 
Dr. Zhang, the founder, chairman of our Board, executive Director and president, is a key person responsible 
for our technical operations and/or the research and development of our Specialist Technology Products who 
is subject to lock-up requirements pursuant to Rule 18C.14 of the Listing Rules. Except for Dr. Zhang, none 
of the other executive Directors, senior management members or core members of R&D beneficially owns 
any Shares of the Company and are therefore not subject to the lock-up requirements under the Rule 18C.14 
of the Listing Rules. 
 
3. 
Each of Shaoxing Ziqiu LP, Shaoxing Yuzhang LP and Shaoxing Zhiqiu LP was controlled by Dr. Zhang 
as the general partner. Therefore, each of Shaoxing Zhiqiu LP, Shaoxing Ziqiu LP and Shaoxing 
Yuzhang LP is a close associate of Dr. Zhang under the Listing Rules and is subject to the lock-up 
requirements pursuant to Rule 18C.14 of the Listing Rules. 
 
Pathfinder SIIs 
 
Name 
Number of H 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing 
% of total issued 
H Shares in the 
Company upon 
Listing 
% of total issued 
Shares in the 
Company upon 
Listing 
Last day subject to the 
lock-up undertakings 
(Note 1) 
Broadband Chengbai Yangtze 
River (Hubei) Investment Fund 
Partnership (Limited Partnership) 
(寬帶誠柏長江(湖北)投資基金合
夥企業(有限合夥))  
19,141,836 
7.81% 
7.81% 
May 17, 2027 
Qingkong Yinxing Nantong 
Venture Investment Fund 
Partnership (Limited 
Partnership) (清控銀杏南通創業
投資基金合夥企業(有限合夥)) 
(“Qingkong Yinxing”) 
11,352,060 
4.63% 
4.63% 
May 17, 2027 
Subtotal 
30,493,896 
12.44% 
12.44% 
 
Notes: 
 

<<<PAGE 8>>>
– 17 – 
 
 
1. 
Pursuant to the applicable PRC law, within the 12 months following the Listing Date, all existing 
Shareholders (including the Pre-IPO Investors) are prohibited from disposing of any of the Shares held 
by them. Pursuant to Rule 18C.14(2) of the Listing Rules, the required lock-up period commences on 
the date by reference to which disclosure of their respective shareholdings in the Company is made in 
the Prospectus and ends on the date upon the expiry of six months from the Listing Date i.e. November 
17, 2026. 
 
2. 
Each of the Shareholders listed in the above table is a Pathfinder SII of the Company as defined under 
Chapter 2.5 of the Guide for New Listing Applicants. 
 
Existing Shareholders (other than the Key Persons and the Pathfinder SIIs) 
 
Number of Shares 
held in the Company
subject to lock-up 
undertakings upon 
Name(Note 1) 
Listing 
% of total issued 
H Shares in the 
Company upon 
Listing 
% of total issued 
Shares in the 
Company upon 
Listing 
Last day subject 
to the lock-up 
undertakings 
(Note 2) 
Yuhuan City State-owned Assets 
Investment Operation Group 
Co., Ltd. (玉環市國有資產投資
經營集團有限公司) 
 21,344,380  
8.71% 
8.71% 
May 17, 
2027 
Shanghai Venture Capital Center 
(Limited Partnership) (上海峰
瑞創業投資中心(有限合夥)) 
 14,193,000  
5.79% 
5.79% 
May 17, 
2027 
Yuhuan City Equity Investment 
Fund Co., Ltd. (玉環市股權投
資基金有限公司) 
 14,000,000  
5.72% 
5.72% 
May 17, 
2027 
Jiaxing Runze Equity Investment 
Partnership Enterprise (Limited 
Partnership) (嘉興潤澤股權投
資合夥企業(有限合夥)) 
 9,085,312  
3.71% 
3.71% 
May 17, 
2027 
Rizhao Ivy Innovative Venture 
Capital Partnership (Limited 
Partnership) (日照常春藤創新
創業投資合夥企業(有限合夥)) 
 8,052,612  
3.29% 
3.29% 
May 17, 
2027 
Shenzhen Jasic Robotics 
Automation Equipment Co., 
Ltd. (深圳市佳士機器人自動
化設備有限公司)  
 5,632,836  
2.30% 
2.30% 
May 17, 
2027 
Jiaxing Feitu Xinyuan Venture 
Capital Partnership (Limited 
Partnership) (嘉興飛圖鑫元創
業投資合夥企業(有限合夥)) 
 5,114,328  
2.09% 
2.09% 
May 17, 
2027 

<<<PAGE 9>>>
– 18 – 
 
 
Ivory One Investment Ltd 
 4,763,232  
1.94% 
1.94% 
May 17, 
2027 
Suzhou ChinaEquity Chenxin 
Investment Center (Limited 
Partnership) (蘇州信中利晨信
投資中心(有限合夥)) 
 4,340,180  
1.77% 
1.77% 
May 17, 
2027 
Fengchi Qianhai Dianche No.2 
Investment Consulting 
Partnership (Limited 
Partnership) (深圳前海風馳電
掣貳號投資諮詢合夥企業(有
限合夥) 
 3,443,372  
1.41% 
1.41% 
May 17, 
2027 
Mr. Si Shaohua (司紹華) 
 3,409,540  
1.39% 
1.39% 
May 17, 
2027 
Chongtian Intelligence (Weifang) 
Enterprise Management 
Consulting Center (Limited 
Partnership) (沖天智能(濰坊)企
業管理諮詢中心(有限合夥)) 
 3,341,072  
1.36% 
1.36% 
May 17, 
2027 
Rizhao Ivy Venture Capital 
Partnership (Limited 
Partnership) (日照常春藤創業
投資 合夥企業(有限合夥)) 
 3,245,284  
1.32% 
1.32% 
May 17, 
2027 
Xizang Chuzhe Zhixin Equity 
Investment Partnership (Limited 
Partnership) (西藏初者之心股
權投資合夥企業(有限合夥)) 
 3,111,536  
1.27% 
1.27% 
May 17, 
2027 
Jianhu County Yuehu New 
Industry Fund Partnership 
(Limited Partnership) (建湖縣
悅湖新興產業基金合夥企業
(有限合夥)) 
 3,057,140  
1.25% 
1.25% 
May 17, 
2027 
Shanghai Qingwang Venture 
Investment Partnership (Limited 
Partnership) (上海青望創業投
資合夥企業(有限合夥) 
 3,038,132  
1.24% 
1.24% 
May 17, 
2027 
Hangzhou Guoke Infore Equity 
Investment Partnership (Limited 
Partnership) (杭州國科盈峰股
權投資合夥企業(有限合夥)) 
 2,700,208  
1.10% 
1.10% 
May 17, 
2027 
Hainan Ferry Growth No.3 Venture 
Investment Fund Partnership 
(Limited Partnership) (海南源
 2,557,156  
1.04% 
1.04% 
May 17, 
2027 

<<<PAGE 10>>>
– 19 – 
 
 
渡三期創業投資基金合夥企業
(有限合伙)) (formerly known as 
Suzhou Ferry Growth 
Investment Partnership (Limited 
Partnership) (蘇州源渡成長投
資合夥企業(有限合夥))) 
Smart Beauty Investment Limited 
 2,398,252  
0.98% 
0.98% 
May 17, 
2027 
Ms. Wu Xingtao (吳星陶) 
 2,354,996  
0.96% 
0.96% 
May 17, 
2027 
Mr. Yao Lisheng (姚立生) 
 1,704,764  
0.70% 
0.70% 
May 17, 
2027 
Mr. Wang Yanfeng (王彥峰) 
 1,704,764  
0.70% 
0.70% 
May 17, 
2027 
Mr. Tong Xinmiao (童新苗) 
 1,704,764  
0.70% 
0.70% 
May 17, 
2027 
Baotou Qidi Star Investment 
Center (Limited Partnership) (包
頭市啓迪之星投資中心(有限
合夥)) 
 1,649,280  
0.67% 
0.67% 
May 17, 
2027 
Jinan Yike No.1 Investment Center 
(Limited Partnership) (濟南翼
可一號投資中心) （有限合
伙） 
 1,425,000  
0.58% 
0.58% 
May 17, 
2027 
Ningbo Yiyi Equity Investment 
Fund Management Co., Ltd. (寧
波易一股權投資基金管理有限
公司) 
 1,302,052  
0.53% 
0.53% 
May 17, 
2027 
Fengchi Qianhai Dianche No.2 
Investment Consulting 
Partnership (Limited 
Partnership) (深圳前海風馳電
掣貳號投資諮詢合夥企業(有
限合夥)) 
 1,205,852  
0.49% 
0.49% 
May 17, 
2027 
Quanzhou Shenglian Equity 
Investment Fund Partnership 
(Limited Partnership) (泉州市
晟聯股權投資基金合夥企業
(有限合夥) 
 1,135,628  
0.46% 
0.46% 
May 17, 
2027 
Mr. Lv Dalong (呂大龍) 
 1,109,628  
0.45% 
0.45% 
May 17, 
2027 
Shaoxing City Shangyu District 
Wanxiang Holding Co., Ltd. (紹
 1,070,000  
0.44% 
0.44% 
May 17, 
2027 

<<<PAGE 11>>>
– 20 – 
 
 
興市上虞區萬象控股有限公
司) 
Shaoxing Shangyu Caoejiang 
Economic Development Zone 
Construction Development Co., 
Ltd (紹興市上虞曹娥江經濟開
發區建設發展有限公司) 
 1,070,000  
0.44% 
0.44% 
May 17, 
2027 
Mr. Zhang Kaifeng (張凱風) 
 355,140  
0.14% 
0.14% 
May 17, 
2027 
Subtotal 
134,619,440 
54.96% 
54.96% 
 
Notes: 
 
1. 
Please refer to the Prospectus for further details. 
 
2. 
The expiry date of the lock–up period shown in the table above is pursuant to applicable PRC laws 
 
 
PLACEE CONCENTRATION ANALYSIS 
 
 
 
 
 
Placees 
Top 1 
Top 5 
Top 10 
Top 25 
 
Note: 
 
* 
Ranking of placees is based on the number of H Shares allotted to the placees. 
 
 
 
Number 
Number of 
of Shares 
% of total issued 
H Shares 
Allotment as % of 
Allotment as % of 
held upon 
share capital 
allotted International Offering 
total Offer Shares 
Listing 
upon Listing 
3,147,500 
15.99% 
12.79% 
3,147,500 
1.28% 
11,465,800 
58.26% 
46.61% 
22,817,860 
9.32% 
15,707,700 
79.82% 
63.85% 
27,059,760 
11.05% 
18,361,400 
93.30% 
74.64% 
29,713,460 
12.13% 

<<<PAGE 12>>>
– 21 – 
 
 
H SHARE SHAREHOLDER CONCENTRATION ANALYSIS 
 
 
 
H Shareholders* 
Top 1 
Top 5 
Top 10 
Top 25 
 
Note: 
 
* 
Ranking of H Shareholders is based on the number of H Shares held by H Shareholders upon Listing. 
 
SHAREHOLDER CONCENTRATION ANALYSIS 
 
 
 
Shareholders 
Top 1 
Top 5 
Top 10 
Top 25 
 
Note: 
 
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by Shareholders upon 
Listing. 
 
 
 
Number of 
Number of 
Number of 
H Shares 
% of total issued 
Shares 
H Shares 
Allotment as % of 
Allotment as % of 
held upon 
H Share capital 
held upon 
allotted International Offering 
total Offer Shares 
Listing 
upon Listing 
Listing 
0 
0.00% 
0.00% 
55,240,632 
22.55% 
55,240,632 
1,284,000 
6.52% 
5.22% 
137,665,536 
56.20% 
137,665,536 
1,284,000 
6.52% 
5.22% 
175,505,036 
71.65% 
175,505,036 
10,185,400 
51.76% 
41.40% 
223,042,880 
91.06% 
223,042,880 
Number of 
Number of 
Number of 
H Shares 
Shares 
% of total issued 
H Shares 
Allotment as % of 
Allotment as % of 
held upon 
held upon 
share capital 
allotted International Offering 
total Offer Shares 
Listing 
Listing 
upon Listing 
0 
0.00% 
0.00% 
55,240,632 
55,240,632 
22.55% 
1,284,000 
6.52% 
5.22% 
137,665,536 
137,665,536 
56.20% 
1,284,000 
6.52% 
5.22% 
175,505,036 
175,505,036 
71.65% 
10,185,400 
51.76% 
41.40% 
223,042,880 
223,042,880 
91.06% 

<<<PAGE 13>>>
– 22 – 
 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
 
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications 
made by the public will be conditionally allocated on the basis set out below: 
 
Pool A 
Approximate 
percentage 
allotted of the 
total number 
Number 
Number 
of H Shares 
of H Shares 
of valid 
applied 
applied for 
applications 
Basis of allocation/ballot 
for 
100 
71,369 
2,142 out of 71,369 applicants to receive 100 H shares 
3.00% 
200 
13,996 
512 out of 13,996 applicants to receive 100 H shares 
1.83% 
300 
25,596 
1,050 out of 25,596 applicants to receive 100 H shares 
1.37% 
400 
6,360 
284 out of 6,360 applicants to receive 100 H shares 
1.12% 
500 
7,291 
346 out of 7,291 applicants to receive 100 H shares 
0.95% 
600 
4,556 
228 out of 4,556 applicants to receive 100 H shares 
0.83% 
700 
3,410 
178 out of 3,410 applicants to receive 100 H shares 
0.75% 
800 
3,201 
174 out of 3,201 applicants to receive 100 H shares 
0.68% 
900 
3,101 
174 out of 3,101 applicants to receive 100 H shares 
0.62% 
1,000 
15,770 
911 out of 15,770 applicants to receive 100 H shares 
0.58% 
1,500 
13,233 
858 out of 13,233 applicants to receive 100 H shares 
0.43% 
2,000 
6,351 
447 out of 6,351 applicants to receive 100 H shares 
0.35% 
2,500 
3,501 
263 out of 3,501 applicants to receive 100 H shares 
0.30% 
3,000 
7,852 
620 out of 7,852 applicants to receive 100 H shares 
0.26% 
3,500 
3,686 
305 out of 3,686 applicants to receive 100 H shares 
0.24% 
4,000 
2,716 
233 out of 2,716 applicants to receive 100 H shares 
0.21% 
4,500 
2,418 
215 out of 2,418 applicants to receive 100 H shares 
0.20% 
5,000 
4,470 
409 out of 4,470 applicants to receive 100 H shares 
0.18% 
6,000 
4,369 
421 out of 4,369 applicants to receive 100 H shares 
0.16% 
7,000 
3,177 
320 out of 3,177 applicants to receive 100 H shares 
0.14% 
8,000 
2,607 
273 out of 2,607 applicants to receive 100 H shares 
0.13% 
9,000 
3,692 
399 out of 3,692 applicants to receive 100 H shares 
0.12% 
10,000 
16,596 
1,846 out of 16,596 applicants to receive 100 H shares 
0.11% 
20,000 
9,981 
1,353 out of 9,981 applicants to receive 100 H shares 
0.07% 
30,000 
8,093 
1,231 out of 8,093 applicants to receive 100 H shares 
0.05% 
40,000 
5,482 
905 out of 5,482 applicants to receive 100 H shares 
0.04% 
50,000 
4,317 
759 out of 4,317 applicants to receive 100 H shares 
0.04% 
60,000 
3,510 
650 out of 3,510 applicants to receive 100 H shares 
0.03% 
70,000 
3,550 
687 out of 3,550 applicants to receive 100 H shares 
0.03% 
80,000 
2,839 
571 out of 2,839 applicants to receive 100 H shares 
0.03% 
90,000 
2,441 
508 out of 2,441 applicants to receive 100 H shares 
0.02% 

<<<PAGE 14>>>
– 23 – 
 
 
100,000 
24,882 
5,328 out of 24,882 applicants to receive 100 H shares 
0.02% 
 
Total 
 
294,413 
 
Total number of Pool A successful applicants: 
24,600 
 
 
 
Pool B 
Approximate 
Number 
Number 
percentage 
allotted of the 
total number 
of H Shares 
of H Shares 
applied for 
of valid 
applications 
Basis of allocation/ballot 
applied 
for 
200,000 13,567 
5,427 out of 13,567 applicants to receive 100 H shares 
0.02% 
300,000 5,768 
3,278 out of 5,768 applicants to receive 100 H shares 
0.02% 
400,000 3,481 
2,538 out of 3,481 applicants to receive 100 H shares 
0.02% 
500,000 2,919 
2,582 out of 2,919 applicants to receive 100 H shares 
0.02% 
615,000 10,186 
100 H shares plus 589 out of 10,186 applicants to 
receive an additional 100 H shares 
0.02% 
 
Total 
35,921 Total number of Pool B successful applicants: 24,011 
 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the designated 
nominee accounts have been remitted back to the accounts of all HKSCC participants. Investors should contact 
their relevant brokers for any inquiries. 

<<<PAGE 15>>>
– 14 – 
 
 
ADDITIONAL INFORMATION 
 
Reallocation 
 
As the Hong Kong Public Offering has been over-subscribed by more than 14,800 times of 
the total number of Offer Shares initially available under the Hong Kong Public Offering, the 
reallocation procedure as disclosed in the section headed “Structure and Conditions of the 
Global Offering – The Hong Kong Public Offering – Reallocation” in the Prospectus has been 
applied.  
 
The number of Offer Shares initially available under the Hong Kong Public Offering is 
1,230,000 Shares, representing approximately 5% of the total number of Offer Shares initially 
available under the Global Offering. As a result of such reallocation, the final number of Offer 
Shares under the Hong Kong Public Offering is adjusted to 4,920,000 Shares, representing 
approximately 20% of the total number of Offer Shares available under the Global Offering. 
 
Placing to connected clients with consents under paragraph 1C(1) of the Placing 
Guidelines 
 
Under the International Offering, certain Offer Shares were placed to connected clients of 
certain distributors pursuant to the Placing Guidelines. Details of the placement to connected 
clients are set out below. 
 
No. 
Connected 
Client 
Connected 
Distributor 
Relationship 
between the 
Connected 
Client 
and 
the 
Connected 
Distributor 
Informatio
n 
of 
the 
Connected 
Client 
Whether 
the 
connected 
client 
will 
hold 
beneficial 
interests of Offer 
Shares on a non-
discretionary or 
discretionary 
basis 
for 
independent third 
parties 
No. of Offer  
Shares 
allocated to 
the 
connected 
client 
% of Offer 
Shares 
% of total 
issued 
share 
capital 
after 
the Global 
Offering 
1. 
 
CSI 
CLSA 
CSI 
and 
CLSA 
are 
group 
companies. 
Accordingly, 
CSI 
is 
considered as 
a “connected 
client” 
of 
CLSA 
pursuant 
to 
paragraph 1B 
of 
the 
Appendix F1 
to the Listing 
Rules. 
Note 1 
Non-discretionary 
basis 
2,000 
0.0081% 
0.0008% 
2. 
 
Grand 
China 
Global Master 
Grand China Securities 
Limited 
Grand China 
Securities 
Limited is the 
Investment 
Manager 
of  
Grand China 
Global 
Master. Fund 
Accordingly, 
Grand China 
Global 
Master 
is 
considered as 
Note 2 
Discretionary basis 
131,100 
0.5329% 
0.0535% 

<<<PAGE 16>>>
– 15 – 
 
 
a “connected 
client” 
of 
Grand China 
Securities 
Limited 
pursuant 
to 
paragraph 1B 
of 
the 
Appendix F1 
to the Listing 
Rules. 
 
3. 
 
China AMC HK 
CLSA 
China AMC 
HK 
is 
a 
member 
of 
the 
same 
group 
of 
companies as 
CLSA. 
Accordingly, 
China AMC 
HK 
is 
considered as 
a “connected 
client” 
of 
CLSA 
pursuant 
to 
paragraph 1B 
of 
the 
Appendix F1 
to the Listing 
Rules. 
Note 3 
Discretionary basis 
1,200 
0.0049% 
0.0005% 
 
Notes: 
 
1. 
CSI will act as the single counterparty of a back-to-back total return swap transaction (the “CSI Back-
to-back TRS”) to be entered into by CSI in connection with a total return swap order (the “CSI Client 
TRS”) placed and fully funded by its ultimate clients (the “CSI Ultimate Clients”), by which CSI will 
pass the full economic exposure of the Offer Shares placed to CSI to the CSI Ultimate Clients.   
 
CSI will hold the Offer Shares but will contractually agree to pass on the full economic exposure to the 
CSI Ultimate Clients, on a non-discretionary basis. The CSI Ultimate Client may exercise an early 
termination right to early terminate the CSI Client TRS at any time from the trade date of the CSI Client 
TRS which should be on or after the date on which the Offer Shares are listed on the Stock Exchange. 
Upon the final maturity or termination of the CSI Client TRS by the CSI Ultimate Client, CSI will 
dispose of the Offer Shares on the secondary market and the CSI Ultimate Client will receive a final 
termination amount of the CSI Back-to-back TRS which will taken into account all the economic returns 
or economic loss in relation to the Offer Shares and the fixed amount of transaction fees of the CSI 
Back-to-back TRS and the CSI Client TRS. CSI will not exercise the voting right of the Offer Shares 
during the terms of the CSI Back-to-back TRS.  
 
To the best of CSI’s knowledge after having made all reasonable inquiries, each of the CSI Ultimate 
Clients is an independent third party of the Company its subsidiaries, CSI, CLSA and the companies 
which are members of the same group of CLSA.  
 
CSI is a wholly owned subsidiary of CITIC Securities Investment Limited (“CITIC Securities 
Investment”), which is wholly owned by CITIC Securities Company Limited (中信証券股份有限公
司) (“CITIC Securities”). CITIC Securities is the holding company of CLSA, one of the Overall 
Coordinators and Underwriters of the Global Offering.  
 
Therefore, CSI and CLSA are members of the same group of companies and CSI is a connected client 
of CLSA. The participation of CSI as placee in the International Offering would constitute an allocation 
to connected clients of the CLSA. 
 
2. 
Grand China Securities Limited will hold the Offer Shares in its capacity as the discretionary fund 

<<<PAGE 17>>>
– 16 – 
 
 
manager of Grand China Global Master on behalf of its investors, each of which is an independent third 
party of the Company, its subsidiaries, its substantial shareholders, Grand China Global Master, Grand 
China Securities Limited and the companies which are members of the same group of Grand China 
Securities Limited. Save for Mr. Ho Kin Kai who holds 31.25% interest in the Grand China Global 
Master, no other investor holds 30% or more interest in the Grand China Global Master. 
 
3. 
China AMC HK is an investment advisor and a delegate of the investment manager of its underlying 
clients (“China AMC HK Ultimate Clients”) and manages assets (in its capacity as an investment 
advisor of the China AMC HK Ultimate Clients) and executes trades (in its capacity as a delegate of the 
investment manager of China AMC HK Ultimate Clients) for on behalf of China AMC HK Ultimate 
Clients, namely CHINA AMC CHINA FOCUS FUND, the ultimate beneficial owner of which is 
Manulife (International) Limited, holding 72.20% interest therein. To the best knowledge of China AMC 
HK after making all reasonable enquiries, (i) each of the China AMC HK Ultimate Clients is an 
independent third party of the Company, its subsidiaries, its substantial shareholders, CLSA, China 
AMC HK and the companies which are members of the same group of companies as CLSA; and (ii) 
China AMC HK is not a collective investment scheme which is not authorised by the SFC. 

<<<PAGE 18>>>
– 15 – 
 
 
Placing to existing shareholders and/or its close associates with a prior waiver 
under Rule 10.04 and consent under paragraph 1C(2) of the Placing Guidelines 
 
The Company has applied for a waiver under Rule 10.04 of the Listing Rules and a 
consent under paragraph 1C(2) of Appendix F1 to the Listing Rules, to permit the 
existing shareholders and/or its close associates to participate as placees in the Global 
Offering to subscribe for the Offer Shares to be issued by the Company under the 
International Offering (together, the “Permitted Participants”). The Stock Exchange 
has agreed to grant the requested waiver and consent subject to the conditions that: 
 
(a) the allocation to the Permitted Participants will not affect the Company’s 
ability to satisfy its public float requirement under Rule 8.08(1) (as amended 
and replaced by Rule 19A.13A) of the Listing Rules; 
 
(b) the Company and the Sole Sponsor will confirm to the Stock Exchange that no 
preferential treatment has been, nor will be directly or indirectly, given to the 
Permitted Participants by virtue of their relationship with the Company or in 
any allocation in the International Offering; 
 
(c) the allocation to the Permitted Participants would not affect the Company’s 
compliance with the price discovery requirement under Rule 18.08C of the 
Listing Rules for the following reasons: 
 
a. sufficient number of Offer Shares will remain available for allocation to 
the independent price setting investors in the placing tranche in 
accordance with the requirements under paragraph 42 of Chapter 2.5 of 
the Guide; and 
 
b. it would not compromise the free float requirement under Rule 19A.13C 
of the Listing Rules, as there will remain sufficient H Shares held by the 
public and available for trading upon Listing; and 
 
(d) details of the allocation of the Offer Shares to the Permitted Participants as 
placees under the Global Offering will be disclosed in this allotment results 
announcement of the Company. 
 
For details of the allocations of Offer Shares to such Permitted Participants, please 
refer to the section headed “Allotment Results Details – International Offering – 
Allottees with waiver/consents obtained” in this announcement. 

<<<PAGE 19>>>
 
– 16 – 
 
 
 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
 
The Directors confirm that, except for the Listing Rules that have been waived and/    or 
in respect of which consent has been obtained, the Company has complied with the Listing 
Rules and guidance materials in relation to the placing, allotment and listing of the Company’s 
shares. 
 
The Directors confirm that, to the best of their knowledge, the consideration paid by  the 
placees or the public (as the case may be) directly or indirectly for each Offer Share subscribed 
for or purchased by them was the same as the final Offer Price in addition to any brokerage, 
AFRC transaction levy, SFC transaction levy and trading fee payable. 
 
The Directors and the Overall Coordinators confirm that at least 50% of the total number of 
the Offer Shares have been allocated to and taken up by independent price setting investors 
in compliance with Rule 18C.08 of the Listing Rules. 
 
The Directors further confirm that at least 20% of the issued share capital of the Company 
will be held by sophisticated independent investors at the time of Listing in compliance with 
Chapter 2.5 of the Guide for New Listing Applicants. 

<<<PAGE 20>>>
– 17 – 
 
 
DISCLAIMERS 
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
(the “Stock Exchange”) and Hong Kong Securities Clearing Company Limited 
(“HKSCC”) take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part 
of the contents of this announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in  or 
into the United States (including its territories and possessions, any state of the United 
States and the District of  Columbia). This announcement does not constitute or  form   a 
part of any offer or solicitation to purchase or subscribe for securities in the United States. 
The securities mentioned herein have not been, and will not be, registered under the United 
States Securities Act of 1933, as amended (the “U.S. Securities Act”). The securities may 
not be offered or sold in the United States except pursuant to an exemption from the 
registration requirements of the U.S. Securities Act and in compliance with any applicable 
state securities laws, or outside the United States unless in compliance with Regulation S 
under the U.S. Securities Act. There will be no public offer of securities in the United States. 
The Offer Shares are being offered and sold outside the United States in offshore 
transactions in reliance on Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation 
or offer to acquire, purchase or subscribe for securities. This announcement is not a 
prospectus. Potential investors should read the Prospectus dated May 8, 2026 issued by 
Robotphoenix Intelligent Technology Co., Ltd. (浙江翼菲智能科技股份有限公司) for 
detailed information about the Global Offering described herein before deciding whether 
or not to invest in the Shares thereby being offered. 
*   Potential investors of the Offer Shares should note that the Sole Sponsor and the Sponsor-OC   (for itself 
and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations 
under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of 
any of the events set out in the paragraph headed “Underwriting — Underwriting Arrangements 
and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any 
time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
Monday, May 18, 2026). 

<<<PAGE 21>>>
– 3 –
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, the total number of the H 
Shares held by the public represents approximately 63.02% of the total issued share capital 
of the Company, which is higher than the minimum prescribed percentage of H Shares 
required to be held in public hands of 20.08% under Rule 8.08(1) (as amended and replaced 
by Rule 19A.13A(1)) of the Listing Rules calculated based on the final Offer Price of 
HK$30.50 per H Share, thereby satisfying the public float requirement under Rule 8.08(1) (as 
amended and replaced by Rule 19A.13A(1)) of the Listing Rules.
In consideration that the total number of H Shares in issue upon Listing that are held by the 
public and not subject to any disposal restrictions is expected to be at least 10% of the total 
number of issued H Shares at the time of Listing, with an expected market value at the time 
of Listing of not less than HK$50,000,000, the Company is expected to satisfy the free float 
requirement under Rule 19A.13C of the Listing Rules at the time of the Listing.
The Directors confirm that, immediately following the completion of the Global Offering, 
(i) no placee will, individually, be placed more than 10% of the enlarged issued share 
capital of the Company immediately after the Global Offering; (ii) there will not be any new 
substantial Shareholder immediately after the Global Offering; (iii) the three largest public 
shareholders of the Company do not hold more than 50% of the shares in public hands at the 
time of the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) 
there will be at least 300 Shareholders at the time of the Listing in compliance with Rule 
8.08(2) of the Listing Rules.

<<<PAGE 22>>>
– 4 –
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. (Hong 
Kong time) on Monday, May 18, 2026, provided that the Global Offering has become 
unconditional and the right of termination described in the section headed “Underwriting — 
Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus has not been exercised. Investors who trade H Shares prior 
to the receipt of H Share certificates or the H Share certificates becoming valid evidence of 
title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong 
Kong time) on Monday, May 18, 2026, it is expected that dealings in the H Shares on the 
Stock Exchange will commence at 9:00 a.m. on Monday, May 18, 2026. The H Shares will 
be traded in board lots of 100 H Shares each. The stock code of the H Shares is 6871.
By order of the Board
Robotphoenix Intelligent Technology Co., Ltd.
Dr. Zhang Sai
Executive Director, Chairman of the Board and President
Hong Kong, May 15, 2026
As at the date of this announcement, the Board comprises (i) Dr. Zhang Sai, Mr. Zhang Zichao, Mr. Sun 
Tongliang and Mr. Dou Zhiyuan as executive directors; (ii) Mr. Wang Maike, Mr. Lee Shen Kai and Mr. Song 
Pengfei as non-executive directors; and (iii) Mr. Xiong Minghua, Ms. Zhou Shuang, Ms. Zhao Fengmei and 
Mr. Wu Qingyao as independent non-executive directors.
