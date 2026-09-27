# 配发结果公告抽取任务：1641.HK Hongxing Coldchain (Hunan) Co., Ltd.- H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**12/01/2026 21:30**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0112/2026011201301.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1641.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for 
securities in the United States or in any other jurisdictions. The securities mentioned herein have not been, 
and will not be, registered under the United States Securities Act of 1933 as amended from time to time (the 
“U.S. Securities Act”) or any state securities law of the United States. The securities may not be offered, 
sold, pledged or transferred within the United States or to, or for the account or benefit of U.S. persons (as 
defined in Regulation S under the U.S. Securities Act (“Regulation S”)), except in transactions exempt from, 
or not subject to, the registration requirements of the U.S. Securities Act. The Offer Shares may be offered, 
sold or delivered outside the United States to non-U.S. persons in offshore transactions in accordance with 
Regulation S.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. This announcement is not a prospectus. Potential investors should 
read the prospectus dated December 31, 2025 (the “Prospectus”) issued by Hongxing Coldchain (Hunan) 
Co., Ltd. (紅星冷鏈（湖南）股份有限公司) (the “Company”) for detailed information about the Global 
Offering described below before deciding whether or not to invest in the H Shares thereby being offered. Any 
investment decision in relation to the Offer Shares should be taken solely in reliance on the information in the 
Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings 
as those defined in the Prospectus.
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and on 
behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong 
Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in 
the paragraph headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public 
Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on 
the Listing Date (which is currently expected to be on Tuesday, January 13, 2026).

<<<PAGE 2>>>
– 2 –
Hongxing Coldchain (Hunan) Co., Ltd.
紅星冷鏈（湖南）股份有限公司
(a joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under 
the Global Offering
:
23,263,000 H Shares
Number of Hong Kong Offer Shares
:
2,326,500 H Shares (subject to 
reallocation)
Number of International Offer Shares
:
20,936,500 H Shares (subject to reallocation)
Offer Price
:
HK$12.26 per H Share, plus brokerage of 
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
01641
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers
(in alphabetical order)
Ruibang

<<<PAGE 3>>>
– 3 –
HONGXING COLDCHAIN (HUNAN) CO., LTD.
ANNOUNCEMENT OF FINAL OFFER PRICE AND 
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have 
the same meanings as those defined in the prospectus dated December 31, 2025 (the 
“Prospectus”) issued by Hongxing Coldchain (Hunan) Co., Ltd. (紅星冷鏈（湖南）股份
有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of H 
Shareholders, H Shareholders and prospective investors should be aware that the 
price of the H Shares could move substantially even with a small number of H Shares 
traded and should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
1641
Stock short name
HX COLDCHAIN
Dealings commencement date
January 13, 2026*
*see note at the end of the announcement
Price Information
Offer Price
HK$12.26
Offer Shares and Share Capital
Number of Offer Shares
23,263,000 H Shares
Final Number of Offer Shares in Hong Kong Public 
Offering
2,326,500 H Shares
Final Number of Offer Shares in International 
Offering
20,936,500 H Shares
Number of issued Shares upon Listing
98,263,000 Shares

<<<PAGE 4>>>
– 4 –
Proceeds
Gross proceeds (Note)
HK$285.20 million
Less: Estimated listing expenses payable based on 
Offer Price
HK$(32.87) million
Net proceeds
HK$252.33 million
Note: Gross proceeds refers to the amount to which the Company is entitled receive. For details of the use 
of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.

<<<PAGE 5>>>
– 5 –
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
103,102
No. of successful applications
4,653
Subscription level
2,309.25 times
Claw-back triggered
No
No. of Offer Shares initially available under the Hong 
Kong Public Offering
2,326,500
H Shares
No. of Offer Shares reallocated from the International 
Offering (claw-back)
N/A
Final no. of Offer Shares under the Hong Kong Public 
Offering
2,326,500 
H Shares
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering
10%
Note: For details of the final allocation of the H Shares to the Hong Kong Public Offering, investors 
can refer to https://www.hkeipo.hk/iporesult to perform a search by identification number or 
https://www.hkeipo.hk/iporesult for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
106
Subscription level
1.65 times
No. of Offer Shares initially available under the 
International Offering
20,936,500 H Shares
No. of Offer Shares reallocated to the Hong Kong Public 
Offering (claw-back)
No
Final no. of Offer Shares under the International Offering
20,936,500 
H Shares
% of Offer Shares under the International Offering to the 
Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, (i) none 
of the Offer Shares subscribed by the placees and the public have been financed directly or 
indirectly by the Company, any of the Directors, chief executive of the Company, Controlling 
Shareholders, substantial Shareholders, existing Shareholders of the Company or any of 
its subsidiaries or their respective close associates; and (ii) none of the placees and the 
public who have purchased the Offer Shares are accustomed to taking instructions from the 

<<<PAGE 6>>>
– 6 –
Company, any of the Directors, chief executive of the Company, Controlling Shareholders, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries 
or their respective close associates in relation to the acquisition, disposal, voting or other 
disposition of H Shares registered in his/her/its name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investor
Investor Note 1
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
Existing 
shareholders 
or their close 
associates
FUHUIDA (HK) LIMITED  
(“FUHUIDA HK”)
1,781,000
7.66%
7.25%
1.81%
No
Total
1,781,000
7.66%
7.25%
1.81%
Note:
(1)	
For further details of the Cornerstone Investor, please refer to the section headed “Cornerstone 
Investors” in the Prospectus.
Allottee with Consent Obtained
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
Allottee with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Listing Guide in relation to 
allocations to connected client Note 1
Orient Asset Management 
(Hong Kong) Limited (“Orient 
AM”)
4,359,000
18.74%
17.74%
4.44%
A connected 
client
Note:
(1)	
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 
of the Listing Guide in relation to allocations to a connected client, please refer to the section 
headed “Others/Additional Information — Placing to a connected client with prior consent under 
paragraph 1C(1) of the Placing Guidelines” in this announcement.

<<<PAGE 7>>>
– 7 –
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
Unlisted 
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
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings Note 1
Hongxing Shiye Industrial 
Group Co., Ltd. (紅星實業
集團有限公司)
43,690,535
—
—
44.46%
January 12, 2027
Changsha Hongri Jingming 
Equity Investment 
Partnership (Limited 
Partnership) (長沙紅日景明
股權投資合夥企業(有限 
合夥))
6,045,039
—
—
6.15%
January 12, 2027
Changsha Hongri Mingsheng 
Enterprise Management 
Partnership (Limited 
Partnership) 長沙紅日明升
企業管理合夥企業(有限 
合夥)
3,491,905
—
—
3.56%
January 12, 2027
Changsha Hongxing 
Investment Management 
Center (長沙紅星投資經營
管理中心) Note 2
53,227,479
—
—
54.17%
January 12, 2027
Subtotal
53,227,479
—
—
54.17%
Note:
(1)	
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Laws. The required lock-up for the Controlling 
Shareholders ends on January 12, 2027, being 12 months following the Listing Date.
(2)	
For illustrative purposes only, this subsection lists only those members of the Controlling Shareholders who hold Shares directly in the 
Company. Pursuant to Rule 10.07 of the Listing Rules, each of the Controlling Shareholders (namely, Hongxing Shiye, Hongri Jingming, 
Hongri Mingsheng and Hongxing Center) has undertaken to the Company and the Stock Exchange that it shall, and shall procure that the 
relevant registered holders of the Shares in which it is beneficially interested shall, comply with the applicable lock-up requirements. For 
further details, please refer to the section headed “Underwriting — Underwriting Arrangements and Expenses -Undertakings to the Stock 
Exchange pursuant to the Listing Rules” in the Prospectus.

<<<PAGE 8>>>
– 8 –
Cornerstone Investor
Investor Note 1
Number of 
Unlisted 
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
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertaking Note 1
FUHUIDA HK
—
1,781,000
7.25%
1.81%
July 12, 2026
Subtotal
—
1,781,000
7.25%
1.81%
Note:
1.	
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on 
July 12, 2026, being six months following the Listing Date. The Cornerstone Investor will cease to 
be prohibited from disposing of or transferring H Shares subscribed for pursuant to the relevant 
cornerstone investment agreement after the indicated date.

<<<PAGE 9>>>
– 9 –
Other Existing Shareholders
Name
Number of 
Unlisted 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-
up undertakings 
upon Listing
% of shareholding 
in the Company 
subject to lock-
up undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings Note 1
Hunan Food Industry Co. Ltd.  
(湖南省食品產業有限公司)
3,637,401
—
—
3.7%
January 12, 2027
Xie Longgui (謝龍貴)
1,813,512
—
—
1.85%
January 12, 2027
Chen Ai (陳愛)
1,360,134
—
—
1.38%
January 12, 2027
Huang Fusheng (黃福生)
1,020,100
340,034
1.38%
1.38%
January 12, 2027
Dai Mingzhi (戴明智)
906,756
—
—
0.92%
January 12, 2027
Wu Ruiqi (吳瑞棋)
906,756
—
—
0.92%
January 12, 2027
Li Wenjing (黎雯靜)
906,756
—
—
0.92%
January 12, 2027
Luo Qinli (羅勤立)
906,756
—
—
0.92%
January 12, 2027
Song Deying (宋德映)
906,756
—
—
0.92%
January 12, 2027
Chen Xinglong (陳興隆)
634,729
—
—
0.65%
January 12, 2027
Cheng Yan (成燕)
340,033
113,345
0.46%
0.46%
January 12, 2027
Lu Yuanhong (呂元紅)
453,378
—
—
0.46%
January 12, 2027
Wu Jun (吳軍)
453,378
—
—
0.46%
January 12, 2027
Peng Wenzhao (彭文釗)
453,378
—
—
0.46%
January 12, 2027
Luo Tiexing (羅鐵興)
340,033
113,345
0.46%
0.46%
January 12, 2027
Yi Guangyue (易光躍)
453,378
—
—
0.46%
January 12, 2027
Zeng Wei (曾維)
453,378
—
—
0.46%
January 12, 2027
Zeng Ya (曾亞)
453,378
—
—
0.46%
January 12, 2027
Li Changxiao (李昌孝)
340,033
113,345
0.46%
0.46%
January 12, 2027
Kong Yu (孔昱)
340,033
113,345
0.46%
0.46%
January 12, 2027
Song Liwen (宋利文)
453,378
—
—
0.46%
January 12, 2027
Zou Songqiu (鄒松球)
226,689
226,689
0.92%
0.46%
January 12, 2027
Sun Ping (孫萍)
453,378
—
—
0.46%
January 12, 2027
Li Zhenbin (李振斌)
340,033
113,345
0.46%
0.46%
January 12, 2027
Li Gang (李剛)
453,378
—
—
0.46%
January 12, 2027
Liu Xinming (柳新明)
272,027
—
—
0.28%
January 12, 2027
Wu Yong (吳勇)
241,802
—
—
0.25%
January 12, 2027
Zhang Mingsheng (張明生)
226,689
—
—
0.23%
January 12, 2027
Li Zhenwu (李振武)
170,017
56,672
0.23%
0.23%
January 12, 2027
Li Dengyun (李登雲)
170,017
56,672
0.23%
0.23%
January 12, 2027
Zhang Ying (張穎)
170,017
56,672
0.23%
0.23%
January 12, 2027
Liu Xiaolian (劉小連)
211,576
—
—
0.22%
January 12, 2027
Subtotal
20,469,057
1,303,464
5.29%
22.13%
Note:
(1)	
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company 
Laws. The required lock-up for existing Shareholders ends on January 12, 2027 being 12 months 
following the Listing Date.

<<<PAGE 10>>>
– 10 –
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
4,359,000
20.8%
18.7%
4,359,000
4.4%
Top 5
15,465,000
73.9%
66.5%
15,465,000
15.7%
Top 10
20,229,500
96.6%
87.0%
20,229,500
20.6%
Top 25
20,888,000
99.8%
89.8%
20,888,000
21.3%
Note:
* Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares 
allotted
Allotment as % 
of International 
Offering
Allotment 
as % of total 
Offer Shares
Number of 
H Shares held 
upon Listing
% of total 
issued H Shares 
capital upon 
Listing
Number of 
Shares held 
upon Listing
Top 1
4,359,000
20.8%
18.7%
4,359,000
17.7%
4,359,000
Top 5
15,465,000
73.9%
66.5%
15,465,000
63.0%
15,465,000
Top 10
20,229,500
96.6%
87.0%
20,229,500
82.3%
20,229,500
Top 25
20,806,000
99.4%
89.4%
22,109,464
90.0%
25,566,469
Note:
* Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 11>>>
– 11 –
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders
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
Number of H 
Shares held 
upon Listing
Number of 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing
Top 1
–
N/A
N/A
–
53,227,479
54.2%
Top 5
11,946,000
57.1%
51.4%
11,946,000
68,810,880
70.0%
Top 10
15,465,000
73.9%
66.5%
15,805,034
76,863,660
78.2%
Top 25
20,229,500
96.6%
87.0%
21,136,258
88,610,181
90.2%
Note:
* Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon 
Listing.

<<<PAGE 12>>>
– 12 –
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications 
made by the public will be conditionally allocated on the basis set out below:
NO. OF SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT 
POOL A
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
500
65,757
658 out of 65,757 applicants to receive 500 H Shares
1.00%
1,000
5,105
71 out of 5,105 applicants to receive 500 H Shares
0.70%
1,500
2,063
35 out of 2,063 applicants to receive 500 H Shares
0.57%
2,000
1,413
27 out of 1,413 applicants to receive 500 H Shares
0.48%
2,500
1,360
29 out of 1,360 applicants to receive 500 H Shares
0.43%
3,000
751
17 out of 751 applicants to receive 500 H Shares
0.38%
3,500
575
14 out of 575 applicants to receive 500 H Shares
0.35%
4,000
2,102
55 out of 2,102 applicants to receive 500 H Shares
0.33%
4,500
597
17 out of 597 applicants to receive 500 H Shares
0.32%
5,000
2,783
80 out of 2,783 applicants to receive 500 H Shares
0.29%
6,000
719
23 out of 719 applicants to receive 500 H Shares
0.27%
7,000
503
17 out of 503 applicants to receive 500 H Shares
0.24%
8,000
805
29 out of 805 applicants to receive 500 H Shares
0.23%
9,000
719
27 out of 719 applicants to receive 500 H Shares
0.21%
10,000
1,819
72 out of 1,819 applicants to receive 500 H Shares
0.20%
15,000
1,029
49 out of 1,029 applicants to receive 500 H Shares
0.16%
20,000
767
42 out of 767 applicants to receive 500 H Shares
0.14%
25,000
689
42 out of 689 applicants to receive 500 H Shares
0.12%
30,000
439
29 out of 439 applicants to receive 500 H Shares
0.11%
35,000
358
25 out of 358 applicants to receive 500 H Shares
0.10%
40,000
414
31 out of 414 applicants to receive 500 H Shares
0.09%
45,000
256
20 out of 256 applicants to receive 500 H Shares
0.09%
50,000
787
65 out of 787 applicants to receive 500 H Shares
0.08%
60,000
476
43 out of 476 applicants to receive 500 H Shares
0.08%
70,000
375
36 out of 375 applicants to receive 500 H Shares
0.07%
80,000
450
46 out of 450 applicants to receive 500 H Shares
0.06%
90,000
395
43 out of 395 applicants to receive 500 H Shares
0.06%
100,000
1,931
217 out of 1,931 applicants to receive 500 H Shares
0.06%
200,000
987
152 out of 987 applicants to receive 500 H Shares
0.04%
300,000
690
128 out of 690 applicants to receive 500 H Shares
0.03%
400,000
891
188 out of 891 applicants to receive 500 H Shares
0.03%
 
98,005
Total number of Pool A successful applicants: 2,327
 
NO. OF SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT 
POOL B
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR
500,000
1,982
793 out of 1,982 applicants to receive 500 H Shares
0.04%
600,000
425
181 out of 425 applicants to receive 500 H Shares
0.04%
700,000
296
132 out of 296 applicants to receive 500 H Shares
0.03%
800,000
264
123 out of 264 applicants to receive 500 H Shares
0.03%
900,000
242
117 out of 242 applicants to receive 500 H Shares
0.03%
1,000,000
260
130 out of 260 applicants to receive 500 H Shares
0.03%
1,163,000
1,628
850 out of 1,628 applicants to receive 500 H Shares
0.02%
 
5,097
Total number of Pool B successful applicants: 2,326
 

<<<PAGE 13>>>
– 13 –
As of the date of this announcement, the relevant subscription monies previously deposited 
in the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/
or in respect of which consent has been obtained, the Company has complied with the 
Listing Rules and guidance materials in relation to the placing, allotment and listing of the 
Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by 
the placees or the public (as the case may be) directly or indirectly for each Offer Share 
subscribed for or purchased by them was the same as the Offer Price in addition to any 
brokerage, AFRC transaction levy, SFC transaction levy and trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Placing to a connected client with prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to a connected client of 
a connected distributor pursuant to the Placing Guidelines. Details of the placement to this 
connected client are set out below.

<<<PAGE 14>>>
– 14 –
Connected client
Connected distributor
Relationship with the connected distributor
Whether the connected client will 
hold beneficial interests of Offer 
Shares on a non-discretionary 
or discretionary basis for 
independent third parties
Number of Offer 
Shares to be 
allocated to the 
connected client
Approximate 
percentage of 
total number of 
Offer Shares
Approximate 
percentage 
of total H 
Shares in issue 
immediately 
following the 
completion of 
Global Offering
Orient AM Note 1
Orient Securities (Hong Kong) 
Limited (“Orient Securities”)
Orient AM and Orient Securities are members of the same 
group of companies.
Orient AM is therefore considered a connected client of 
Orient Securities pursuant to paragraph 1B(7) of Appendix 
F1 to the Listing Rules.
Discretionary basis
4,359,000
18.74%
4.44%
Note:
1.	
Orient AM will hold the Offer Shares on a discretionary basis on behalf of the scheme (i.e., Orient Asset Mgt (HK) Ltd-OSR Navigator No.13). The 
only shareholder in the fund is Invincible Investment SPC-Invincible Stable Growth Segregated Portfolio (the “Portfolio”). There is no general partner 
of limited partner in the Portfolio. The Portfolio is an investment fund controlled as to 59% by XSP Capital Limited, 29% by Haixiangyun Consulting 
Services (HK) Ltd and 12% by MM24 Management Consulting Limited. The shareholders of the Porfolio are independent from each other. XPS Capital 
Limited is wholly owned by Mr. Hu Xiangjuan, who is, the ultimate beneficial owner of the Portfolio.
To the best knowledge of Orient AM after due enquiry, (i) Orient AM has confirmed that, each of the underlying clients and the ultimate beneficial 
owner of the scheme is an independent third party of Orient AM and Orient Securities and the companies which are members of the same group of 
companies as Orient Securities; and (ii) Orient AM is a collective investment scheme which is not authorized by the SFC.

<<<PAGE 15>>>
– 15 –
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate 
such Offer Shares in the International Offering to the connected client listed above. The 
allocation of Offer Shares to such connected client is in compliance with all the conditions 
under the consent granted by the Stock Exchange.
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong 
Limited (the “Stock Exchange”) and Hong Kong Securities Clearing Company Limited 
(“HKSCC”) take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part 
of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in 
or into the United States (including its territories and possessions, any state of the United 
States and the District of Columbia). This announcement does not constitute or form 
a part of any offer or solicitation to purchase or subscribe for securities in the United 
States. The securities mentioned herein have not been, and will not be, registered under 
the United States Securities Act of 1933, as amended (the “U.S. Securities Act”). The 
securities may not be offered or sold in the United States except pursuant to an exemption 
from the registration requirements of the U.S. Securities Act and in compliance with any 
applicable state securities laws, or outside the United States unless in compliance with 
Regulation S under the U.S. Securities Act. There will be no public offer of securities in 
the United States.
The Offer Shares are being offered and sold solely outside the United States in offshore 
transactions in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation 
or offer to acquire, purchase or subscribe for securities. This announcement is not a 
prospectus. Potential investors should read the Prospectus dated December 31, 2025 
issued by Hongxing Coldchain (Hunan) Co., Ltd. (紅星冷鏈(湖南)股份有限公司) for 
detailed information about the Global Offering described below before deciding whether 
or not to invest in the H Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate 
their obligations under the Hong Kong Underwriting Agreement with immediate effect 
upon the occurrence of any of the events set out in the paragraph headed “Underwriting 
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Hong 
Kong Underwriting Agreement — Grounds for Termination” in the Prospectus at any 
time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected 
to be on January 13, 2026).

<<<PAGE 16>>>
– 16 –
PUBLIC FLOAT AND FREE FLOAT
Upon Listing, 24,566,464 H Shares, equivalent to 25.00% of the total number of issued 
Shares of the Company, will be counted towards the public float. Under Rule 19A.13A(1) 
of the Listing Rules, in the event the expected market value of the Company’s H Shares 
upon Listing does not exceed HK$6 billion, at least 25% of the total issued H Shares must 
be held by the public upon Listing. Therefore, the number of H Shares held in public hands 
fulfill the prescribed percentage of H Shares required to be held in public hands under Rule 
19A.13A(1) of the Listing Rules.
Excluding the Offer Shares to be allocated to the cornerstone investor that are subject to a 
lock-up period of six months following the Listing Date and the H Shares to be converted 
from Unlisted Shares that are subjected to a lockup period of 12 months following the 
Listing Date, the Company’s H Shares to be counted towards the free float upon Listing will 
be 21,482,000 Shares. Based on the Offer Price of HK$12.26 per H Share, the Company 
will satisfy the free float requirement under Rule 19A.13C(1)(a) of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering, 
(i) no placee will, individually, be placed more than 10% of the enlarged issued share 
capital of the Company immediately after the Global Offering; (ii) there will not be any new 
substantial Shareholder immediately after the Global Offering; (iii) the three largest public 
shareholders of the Company do not hold more than 50% of the H Shares in public hands at 
the time of the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and 
(iv) there will be at least 300 Shareholders at the time of the Listing in compliance with Rule 
8.08(2) of the Listing Rules.

<<<PAGE 17>>>
– 17 –
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, 
January 13, 2026 (Hong Kong time), provided that the Global Offering has become 
unconditional and the right of termination described in the section headed “Underwriting — 
Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus has not been exercised. Investors who trade the H Shares on 
the basis of publicly available allocation details prior to the receipt of H Share certificates or 
prior to the H Share certificates becoming valid evidence of title do so entirely at their own 
risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on 
Tuesday, January 13, 2026 (Hong Kong time), it is expected that dealings in the H Shares on 
the Stock Exchange will commence at 9:00 a.m. on Tuesday, January 13, 2026 (Hong Kong 
time). The H Shares will be traded in board lots of 500 H Shares each, and the stock code of 
the H Shares will be 01641.
By order of the Board
Hongxing Coldchain (Hunan) Co., Ltd.
紅星冷鏈（湖南）股份有限公司
LUO Yue
Chairman of the Board and non-executive director
Hong Kong, January 12, 2026
As of the date of this announcement, the board of directors of the Company comprises: (i) Mr. ZHANG 
Mingsheng and Ms. XU Qunying as executive directors; (ii) Mr. LUO Yue, Mr. LI Jun, Ms. LU Fenfang and 
Mr. ZHANG Zhong as non-executive directors; and (iii) Ms. LI Zhenzhu, Ms. CAI Yanping and Mr. HOW Sze 
Ming as independent non-executive directors.
