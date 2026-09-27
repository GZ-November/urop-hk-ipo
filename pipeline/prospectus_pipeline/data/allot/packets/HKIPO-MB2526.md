# 配发结果公告抽取任务：2526.HK Hangzhou Diagens Biotechnology Co., Ltd. - B - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**27/03/2026 20:11**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0327/2026032702330.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2526.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Hong Kong Stock 
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents 
of this announcement, make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the prospectus dated March 20, 2026 (the “Prospectus”) issued by Hangzhou Diagens Biotechnology Co., 
Ltd. (杭州德適生物科技股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an offer or an invitation to induce an offer 
by any person to acquire, purchase or subscribe for any of the securities of the Company. This announcement is not a 
prospectus. Potential investors should read the Prospectus for detailed information about the Global Offering described 
below before deciding whether or not to invest in the Offer Shares. Any investment decision in relation to the Offer 
Shares should be taken solely in reliance on the information provided in the Prospectus.
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
No stabilizing manager will be appointed, and it is anticipated that no stabilization activities will be carried out in 
relation to the Global Offering.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out 
in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or 
not resident in Hong Kong. Potential investors of the Offer Shares should note that the Sponsor-overall Coordinator 
(for itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate its obligations under the 
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the 
paragraph headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds 
for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is 
currently expected to be on Monday, March 30, 2026).

<<<PAGE 2>>>
2
Hangzhou Diagens Biotechnology Co., Ltd.
杭州德適生物科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under 
the Global Offering
:
7,999,200 H Shares
Number of Hong Kong Offer Shares
:
799,950 H Shares
Number of International Offer Shares
:
7,199,250 H Shares
Final Offer Price
:
HK$99.0 per H Share, plus brokerage of 
 1.0%, SFC transaction levy of 0.0027%, 
 AFRC transaction levy of 0.00015% and 
 Hong Kong Stock Exchange trading fee of 
 0.00565%
Nominal value
:
RMB1.00 per H Share
Stock code
:
2526
Sole Sponsor, Sponsor-overall Coordinator, Overall Coordinator, 
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Overall Coordinator, Joint Global Coordinator, 
Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
Hangzhou Diagens Biotechnology Co., Ltd.
杭州德適生物科技股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated March 20, 2026 (the “Prospectus”) issued by 
Hangzhou Diagens Biotechnology Co., Ltd. (杭州德適生物科技股份有限公司) (the “Company”).
SUMMARY
Warning: In view of high concentration of shareholding in a small number of H 
Shareholders, H Shareholders and prospective investors should be aware that the price of 
the H Shares could move substantially even with a small number of H Shares traded and 
should exercise extreme caution when dealing in the H Shares.
Company information
Stock code
2526
Stock short name
DIAGENS-B
Dealings commencement date
March 30, 2026*
* see note at the end of the announcement
Price Information
Final Offer Price
HK$99.0
Offer Price Range
HK$95.6 - HK$112.5
Offer Price Adjustment exercised
N/A
Offer Shares and Share Capital
Number of Offer Shares
7,999,200
Number of Offer Shares in the Hong Kong Public Offering
799,950
Number of Offer Shares in the International Offering
7,199,250
Number of issued shares upon Listing
88,879,200

<<<PAGE 4>>>
4
Proceeds
Gross proceedsNote
HK$791.9 million
Less: Estimated listing expenses payable based on Final Offer 
Price
HK$72.11 million
Net proceeds
HK$719.8 million
Note: Gross proceeds refers to the amount to which the issuer is entitled receive. For details of the use of proceeds, 
please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
115,017
No. of successful applications
14,278
Subscription level
1,073.37 times
Reallocation
No
No. of Offer Shares initially available under the Hong Kong Public 
Offering
799,950
No. of Offer Shares reallocated from the International Offering
0
Final no. of Offer Shares under the Hong Kong Public Offering
799,950
% of Offer Shares under the Hong Kong Public Offering to the Global 
Offering
10%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can refer to 
www.eipo.com.hk/eIPOAllotment to perform a search by identification number or www.eipo.com.hk/eIPOAllotment 
for the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
120
Subscription level
3.45 times
No. of Offer Shares initially available under the International Offering
7,199,250
No. of Offer Shares reallocated to the Hong Kong Public Offering
0
Final no. of Offer Shares under the International Offering
7,199,250
% of Offer Shares under the International Offering to the Global 
Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, supervisors, chief executive of the Company, controlling 
shareholders, substantial shareholders, existing shareholders of the Company or any of its 
subsidiaries or their respective close associates; and (ii) none of the placees and the public who 
have purchased the Offer Shares are accustomed to taking instructions from the Company, any of 
the Directors, supervisors, chief executive of the Company, controlling shareholders, substantial 
shareholders, existing shareholders of the Company or any of its subsidiaries or their respective 
close associates in relation to the acquisition, disposal, voting or other disposition of Shares 
registered in his/her/its name or otherwise held by him/her/it.

<<<PAGE 6>>>
6
The placees in the International Offering include the following:
Allotees with Consent Obtained
Investor
Number of Offer 
Shares allocated
% of total number
of Offer Shares
% of total issued 
share capital after 
the Global Offering
Relationship
Allottees with consent under paragraph 1C(1) of Appendix F1 to the Listing Rules (“Placing Guidelines ”) in relation to allocations to a 
connected client(1)
Huatai Capital Investment Limited 
(“HTCI”)
31,350
0.39%
0.04%
HTCI and Huatai 
Financial 
Holdings (Hong 
Kong) Limited 
(“Huatai”) are 
group companies 
within the same 
group
Notes:
(1) 
For details of the consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to a 
connected client, please refer to the section headed “Others/Additional Information – Placing to a connected 
client with a prior consent under paragraph 1C(1) of the Placing Guidelines” in this announcement.

<<<PAGE 7>>>
7
LOCK-UP UNDERTAKINGS
Controlling Shareholders(As Defined in the Prospectus)
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon listingNote (7)
Number of H 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon listing Note (7)
% of total 
issued H Shares 
after the Global 
Offering subject 
to lock-up 
undertakings 
upon listing
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon listing
Last day subject 
to the lock-up 
undertakings
Dr. Song Ning  
(“Dr. Song”)Note (1), (2), (3), (4) and (5)
24,293,507
24,293,507
27.33%
27.33%
March 30, 2027Note (6)
Hangzhou Diagens Nuohui 
Investment Management 
Partnership Enterprise 
(Limited Partnership) (杭州德
適諾輝投資管理合夥企業 
(有限合夥))(“Diagens 
Nuohui”)Note (2)
7,614,901
7,614,901
8.57%
8.57%
March 30, 2027Note (6)
Hangzhou Diagens Nuoda 
Technology Management 
Partnership Enterprise 
(Limited Partnership) (杭州德
適諾達科技管理合夥企業 
(有限合夥))(“Diagens 
Nuoda”)Note (3)
4,759,247
4,759,247
5.35%
5.35%
March 30, 2027Note (6)
Hangzhou Deqian Technology 
Management Partnership 
Enterprise (Limited 
Partnership) (杭州德仟科技
管理合夥企業(有限合夥)) 
(“Deqian Technology”)
3,530,834
3,530,834
3.97%
3.97%
March 30, 2027Note (6)
Hangzhou Diagens Nuoxin 
Investment Management 
Partnership Enterprise 
(Limited Partnership) (杭州德
適諾鑫投資管理合夥企業 
(有限合夥))(“Diagens 
Nuoxin”)
1,903,668
1,903,668
2.14%
2.14%
March 30, 2027Note (6)
Subtotal
42,102,157
42,102,157
47.37%
47.37%

<<<PAGE 8>>>
8
Notes:
(1) 
Dr. Song beneficially holds 24,293,507 Shares.
(2) 
Diagens Nuohui, being an ESOP Platform, is managed and controlled by its general partner, Dr. Song. 
Diagens Nuohui is owned as to approximately 61.35% by Hangzhou Defeng Acceleration Technology 
Management Partnership (Limited Partnership) (杭州德灃加速科技管理合夥企業(有限合夥)) (“Defeng 
Acceleration”) as its limited partner, which is in turn owned as to approximately 99.84% by Dr. Song as 
its general partner. Diagens Nuohui is owned as to approximately 36.61% by Hangzhou Defeng Origin 
Technology Management Partnership (Limited Partnership) (杭州德灃起源科技管理合夥企業(有限合夥)) 
(“Defeng Origin”) as its limited partner, which is in turn managed by Dr. Song as its general partner and 
not owned as to more than 30% by any of its limited partners. Diagens Nuohui is owned as to approximately 
1.94% by Hangzhou Defeng Rise Technology Limited Partnership (杭州德灃升騰科技管理合夥企業(有限合
夥)), which is in turn managed by Dr. Song as its general partner and not owned as to more than 30% by any 
of its limited partners.
As such, under the SFO, each of Dr. Song, Defeng Acceleration and Defeng Origin is deemed to be interested 
in the 7,614,901 Shares held by Diagens Nuohui.
(3) 
Diagens Nuoda is managed by its general partner, Dr. Song. None of the limited partners (not including Dr. 
Song who is the general partner) of Diagens Nuoda owns more than 30% of limited partnership interests 
therein. As such, under the SFO, Dr. Song is deemed to be interested in the 4,759,247 Shares held by Diagens 
Nuoda.
(4) 
Deqian Technology is managed by its general partner, Dr. Song. And Deqian Technology is owned as to 
approximately 99.90% by Hangzhou Dezhi Technology Management Partnership (Limited Partnership) (杭州
德智科技管理合夥企業(有限合夥)) as the sole limited partner, which is in turn owned as to approximately 
76.71% by Dr. Song as its general partner.
As such, under the SFO, each of Dr. Song and Hangzhou Dezhi Technology Management Partnership (Limited 
Partnership) is deemed to be interested in the 3,530,834 Shares held by Deqian Technology.
(5) 
Diagens Nuoxin is managed by its general partner, Dr. Song. And Diagens Nuoxin is owned as to 
approximately 62.50% by Mr. GUO Jian (郭健) as its limited partner. None of other limited partners of 
Diagens Nuoxin owns more than 30% of partnership interests therein. 
As such, under the SFO, each of Dr. Song and Mr. GUO Jian is deemed to be interested in the 1,903,668 
Shares held by Diagens Nuoxin.
(6) 
According to the PRC Company Law, all the Shares held by the existing Shareholders prior to the Global 
Offering are subject to a lock-up period of 12 months following the Listing Date.
(7) 
Calculated based on the assumption that all 80,880,000 Unlisted Shares will be converted into H Shares upon 
listing.

<<<PAGE 9>>>
9
Other Existing Shareholders (including the Pre-IPO Investors as defined in the “History, 
Development and Corporate Structure” section of the Prospectus)
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon listingNote (3)
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon listingNote (3)
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon listing
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon listing
Last day subject 
to the lock-up 
undertakings
Hangzhou Zicheng Investment 
Management Limited 
Partnership (Limited 
Partnership)  
(杭州紫城投資管理合夥企
業(有限合夥))Note (1)
2,539,107
2,539,107
2.86%
2.86%
30 March  
2027 Note (2)
Hangzhou Zizhou Investment 
Management Limited 
Partnership (Limited 
Partnership)  
(杭州紫洲投資管理合夥企
業(有限合夥))Note (1)
4,694,039
4,694,039
5.28%
5.28%
30 March  
2027 Note (2)
Hangzhou Zizheng Investment 
Management Limited 
partnership (Limited 
Partnership)  
(杭州紫正投資管理合夥企
業(有限合夥)Note (1)
1,546,877
1,546,877
1.74%
1.74%
30 March  
2027 Note (2)
Ningbo Jiayuan Venture Capital 
Limited Partnership (Limited 
Partnership)  
(寧波嘉緣創業投資合夥企
業(有限合夥))Note (1)
3,498,695
3,498,695
3.94%
3.94%
30 March  
2027 Note (2)

<<<PAGE 10>>>
10
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon listingNote (3)
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon listingNote (3)
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon listing
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon listing
Last day subject 
to the lock-up 
undertakings
Guozhong Private Equity 
Investment Fund (Xi’an) 
Limited Partnership (Limited 
Partnership)  
(國中私募股權投資基金 
(西安)合夥企業(有限 
合夥))Note (1)
2,959,964
2,959,964
3.33%
3.33%
30 March  
2027 Note (2)
Hunan Xiangjiang Liyuan 
Jiankun Venture Capital 
Limited Partnership (Limited 
Partnership)  
(湖南湘江力遠健鯤創業投
資合夥企業(有限合夥))Note (1)
2,959,964
2,959,964
3.33%
3.33%
30 March  
2027 Note (2)
Nanjing Huarui Ruichuang 
Venture Capital Center 
(Limited Partnership)  
(南京華睿睿創創業投資中
心(有限合夥))Note (1)
986,655
986,655
1.11%
1.11%
30 March  
2027 Note (2)
Jiaxing Weixin No. 1 Equity 
Investment Limited 
Partnership (Limited 
Partnership) 
(嘉興惟馨壹號股權投資合
夥企業(有限合夥))Note (1)
986,655
986,655
1.11%
1.11%
30 March  
2027 Note (2)
Qingdao Juancheng Equity 
Investment Limited 
Partnership (Limited 
Partnership)  
(青島雋誠股權投資合夥企
業(有限合夥))Note (1)
986,655
986,655
1.11%
1.11%
30 March  
2027 Note (2)
Lishui Jingen Private Equity 
Limited Partnership (Limited 
Partnership)  
(麗水金亘股權投資合夥企
業(有限合夥))Note (1)
986,655
986,655
1.11%
1.11%
30 March  
2027 Note (2)
Hangzhou Huayun Equity 
Investment Limited 
Partnership (Limited 
Partnership)  
(杭州花雲股權投資合夥企
業(有限合夥))Note (1)
197,330
197,330
0.22%
0.22%
30 March  
2027 Note (2)

<<<PAGE 11>>>
11
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon listingNote (3)
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon listingNote (3)
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon listing
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon listing
Last day subject 
to the lock-up 
undertakings
Hangzhou Yuxijin Equity 
Investment Limited 
Partnership (Limited 
Partnership)  
(杭州餘汐金股權投資合夥
企業(有限合夥))Note (1)
1,479,975
1,479,975
1.67%
1.67%
30 March  
2027 Note (2)
Tianjin Binhai Yuanyi Jimao 
Private Equity Limited 
Partnership (Limited 
Partnership) 
(天津濱海遠翼吉茂股權投
資合夥企業(有限合夥))Note (1)
1,945,119
1,945,119
2.19%
2.19%
30 March  
2027 Note (2)
Tianjin Yuanyi Yongxuan 
Enterprise Management 
Center (Limited Partnership) 
(天津遠翼永宣企業管理中
心(有限合夥))Note (1)
1,945,119
1,945,119
2.19%
2.19%
30 March  
2027 Note (2)
Tianjin Yongqian Enterprise 
Management Center (Limited 
Partnership)  
(天津永乾企業管理中心(有
限合夥))Note (1)
194,512
194,512
0.22%
0.22%
30 March  
2027 Note (2)
Hangzhou Hetu No. 6 Private 
Equity Limited Partnership 
(Limited Partnership)  
(杭州和途六號股權投資合
夥企業(有限合夥))Note (1)
4,491,905
4,491,905
5.05%
5.05%
30 March  
2027 Note (2)
Hangzhou Yuhang Jingkai 
Private Equity Limited 
Partnership (Limited 
Partnership) 
(杭州餘杭經開股權投資基
金合夥企業(有限合夥))Note (1)
1,296,745
1,296,745
1.46%
1.46%
30 March  
2027 Note (2)
Hunan Xiangjiang Liyuan 
Jianxiao Venture Capital 
Limited Partnership (Limited 
Partnership)  
(湖南湘江力遠健瀟創業投
資合夥企業(有限合夥))Note (1)
648,374
648,374
0.73%
0.73%
30 March  
2027 Note (2)

<<<PAGE 12>>>
12
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon listingNote (3)
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon listingNote (3)
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon listing
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon listing
Last day subject 
to the lock-up 
undertakings
Jiaxing Qingyulan No. 1 
Venture Capital Limited 
Partnership (Limited 
Partnership) 
(嘉興青於藍壹號創業投資
合夥企業(有限合夥))Note (1)
383,419
383,419
0.43%
0.43%
30 March  
2027 Note (2)
Hangzhou Hefu Private Equity 
Limited Partnership (Limited 
Partnership) 
(杭州和馥股權投資合夥企
業(有限合夥))Note (1)
2,154,451
2,154,451
2.42%
2.42%
30 March  
2027 Note (2)
Hangzhou Huarui Ruiyin 
Venture Capital Partnership 
(Limited Partnership)  
(杭州華睿睿銀創業投資合
夥企業(有限合夥))Note (1)
947,814
947,814
1.07%
1.07%
30 March  
2027 Note (2)
Zhejiang Hongshiliang Group 
Jigongjia Wine Co., Ltd.  
(浙江紅石樑集團濟公家酒
坊有限公司)Note (1)
947,814
947,814
1.07%
1.07%
30 March  
2027 Note (2)
Subtotal
38,777,843
38,777,843
43.64%
43.64%
Notes:
(1) 
Please refer to the section headed “History, Development and Corporate Structure — Principal Terms of the 
Pre-IPO Investments” in the Prospectus for details of the Pre-IPO Investors
(2) 
According to the PRC Company Law, all the Shares held by the existing Shareholders prior to the Global 
Offering are subject to a lock-up period of 12 months following the Listing Date.
(3) 
Calculated based on the assumption that all 80,880,000 Unlisted Shares will be converted into H Shares upon 
listing.

<<<PAGE 13>>>
13
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
% of total 
issued share 
capital upon 
Listing
Top 1
879,150
12.21%
10.99%
879,150
0.99%
Top 5
2,545,700
35.36%
31.82%
2,545,700
2.86%
Top 10
3,894,600
54.10%
48.69%
3,894,600
4.38%
Top 25
5,491,350
76.28%
68.65%
5,491,350
6.18%
Notes
* 
Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 14>>>
14
H SHAREHOLDERS CONCENTRATION ANALYSIS
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
issued H
Share
capital upon
Listing
Number of 
Shares held 
upon Listing
Top 1
0
0.00%
0.00%
42,102,157
47.37%
42,102,157
Top 5
0
0.00%
0.00%
65,143,308
73.29%
65,143,308
Top 10
0
0.00%
0.00%
78,170,270
87.95%
78,170,270
Top 25
4,093,500
56.86%
51.17%
84,778,988
95.39%
84,778,988
Notes
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing

<<<PAGE 15>>>
15
SHAREHOLDERS CONCENTRATION ANALYSIS
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
0
0.00%
0.00%
42,102,157
42,102,157
47.37%
Top 5
0
0.00%
0.00%
65,143,308
65,143,308
73.29%
Top 10
0
0.00%
0.00%
78,170,270
78,170,270
87.95%
Top 25
4,093,500
56.86%
51.17%
84,778,988
84,778,988
95.39%
Notes
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing

<<<PAGE 16>>>
16
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
NO. OF SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT
APPROXIMATE
PERCENTAGE 
ALLOTTED
OF THE TOTAL 
NO. OF SHARES 
APPLIED FOR
POOL A
50
62,439
1,873 out of 62,439 to receive 50 Shares
3.00%
100
5,013
167 out of 5,013 to receive 50 Shares
1.67%
150
1,687
58 out of 1,687 to receive 50 Shares
1.15%
200
1,570
57 out of 1,570 to receive 50 Shares
0.91%
250
1,569
58 out of 1,569 to receive 50 Shares
0.74%
300
1,058
41 out of 1,058 to receive 50 Shares
0.65%
350
752
30 out of 752 to receive 50 Shares
0.57%
400
5,549
224 out of 5,549 to receive 50 Shares
0.50%
450
1,008
42 out of 1,008 to receive 50 Shares
0.46%
500
3,247
140 out of 3,247 to receive 50 Shares
0.43%
600
858
39 out of 858 to receive 50 Shares
0.38%
700
628
31 out of 628 to receive 50 Shares
0.35%
800
1,708
87 out of 1,708 to receive 50 Shares
0.32%
900
1,193
63 out of 1,193 to receive 50 Shares
0.29%
1,000
2,389
133 out of 2,389 to receive 50 Shares
0.28%
1,500
1,444
97 out of 1,444 to receive 50 Shares
0.22%
2,000
1,239
98 out of 1,239 to receive 50 Shares
0.20%
2,500
1,041
95 out of 1,041 to receive 50 Shares
0.18%
3,000
828
85 out of 828 to receive 50 Shares
0.17%
3,500
652
74 out of 652 to receive 50 Shares
0.16%
4,000
649
82 out of 649 to receive 50 Shares
0.16%
4,500
547
75 out of 547 to receive 50 Shares
0.15%
5,000
1,356
204 out of 1,356 to receive 50 Shares
0.15%
6,000
757
131 out of 757 to receive 50 Shares
0.14%
7,000
713
141 out of 713 to receive 50 Shares
0.14%
8,000
597
132 out of 597 to receive 50 Shares
0.14%
9,000
651
159 out of 651 to receive 50 Shares
0.14%
10,000
3,031
812 out of 3,031 to receive 50 Shares
0.13%
20,000
1,660
829 out of 1,660 to receive 50 Shares
0.12%
30,000
1,020
746 out of 1,020 to receive 50 Shares
0.12%
40,000
1,244
1,197 out of 1,244 to receive 50 Shares
0.12%
108,097
Total number of Pool A successful applicants: 8,000

<<<PAGE 17>>>
17
NO. OF SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT / BALLOT
APPROXIMATE
PERCENTAGE 
ALLOTTED
OF THE TOTAL 
NO. OF SHARES 
APPLIED FOR
POOL B
50,000
3,420
2,848 out of 3,420 to receive 50 Shares
0.08%
60,000
730
660 out of 730 to receive 50 Shares
0.08%
70,000
476
50 Shares
0.07%
80,000
301
50 Shares plus 15 out of  301 to receive additional 50 
Shares
0.07%
90,000
227
50 Shares plus 28 out of  227 to receive additional 50 
Shares
0.06%
100,000
614
50 Shares plus 120 out of  614 to receive additional 50 
Shares
0.06%
150,000
369
50 Shares plus 205 out of  369 to receive additional 50 
Shares
0.05%
200,000
194
100 Shares
0.05%
250,000
107
100 Shares plus 30 out of  107 to receive additional 50 
Shares
0.05%
300,000
122
150 Shares
0.05%
399,950
360
150 Shares plus 58 out of  360 to receive additional 50 
Shares
0.04%
6,920
Total number of Pool B successful applicants: 6,278

<<<PAGE 18>>>
18
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that consent has been obtained, the 
Company has complied with the Listing Rules and guidance materials in relation to the placing, 
allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and Hong Kong Stock Exchange trading fee payable.

<<<PAGE 19>>>
19
OTHERS/ADDITIONAL INFORMATION
Placing to a connected client with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
The Company has applied to the Hong Kong Stock Exchange for, and the Hong Kong Stock 
Exchange has granted, a consent under paragraph 1C of the Placing Guidelines to permit the 
Company to allocate the Offer Shares in the International Offering to a connected client. The 
allocation of Offer Shares to such a connected client is in compliance with all the conditions 
under the consent granted by the Hong Kong Stock Exchange. Details of the placement to a 
connected client are set out below:
No.
Connected 
Client
Connected 
Distributor
Relationship 
with 
the Connected 
Distributor
Basis of holding 
securities
Number of 
Offer Shares 
(rounded 
down 
to nearest 
whole board 
lots of 50 
Shares) to be 
allocated to the 
connected 
client
Appropriate 
percentage of 
total number 
of 
Offer Shares
Approximate 
percentage of 
total Shares 
in issue 
immediately 
following the 
completion of 
Global 
Offering
1.
Huatai Capital 
Investment 
Limited 
(“HTCI”)(1)
Huatai Financial 
Holdings 
(Hong Kong) 
Limited 
(“Huatai”)
HTCI and Huatai 
are group 
companies 
within the 
same group
Non-
discretionary
31,350
0.39%
0.04%
Notes:
1. 
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public 
offerings (“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products issued by 
appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. In 
connection with such products, the licensed domestic securities firms, through their Hong Kong affiliates, 
may participate in Hong Kong IPOs either as placees or cornerstone investors (the “Cross-border 
Derivatives Trading Regime”).
Huatai Securities Co., Ltd. (“Huatai Securities”), the shares of which are listed on both the Shanghai Stock 
Exchange (stock code: 601688) and the Hong Kong Stock Exchange (stock code: 6886), is one of the domestic 
securities firms licensed to undertake cross-border derivatives trading activities. Huatai Securities entered 
into an ISDA agreement (the “ISDA Agreement”) with its indirectly wholly-owned subsidiary, HTCI, to set 
out the principal terms of any future total return swap between Huatai Securities and HTCI.
Huatai is the Sole Sponsor and one of the Overall Coordinators and Underwriters in connection with the 
Global Offering. Pursuant to an ISDA agreement entered into between Huatai Securities and HTCI, HTCI 
will hold the beneficial interest of the Offer Shares on a non-discretionary basis as the single underlying 
holding under a back-to-back total return swap (“Huatai Back-to-back TRS”) to be entered by HTCI in 
connection with a Client TRS (as defined below) placed by and fully funded (i.e. with no financing provided 
by HTCI) by Huatai Ultimate Clients (as defined below), by which, HTCI will, subject to customary fees and 
commissions, pass the full economic exposure of the Offer Shares ultimately to the Huatai Ultimate Clients, 
which in effect, HTCI will hold the beneficial interest of the Offer Shares on behalf of the Huatai Ultimate 
Clients.

<<<PAGE 20>>>
20
HTCI and Huatai are both indirectly wholly-owned subsidiaries of Huatai Securities. Accordingly, HTCI is 
considered as a “connected client” of Huatai pursuant to paragraph 1B(7) of the Placing Guidelines.
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (“Huatai Ultimate Clients”) 
cannot directly subscribe for the Offer Shares but may invest in derivative products issued by domestic 
securities firms licenced to undertake cross-border derivatives trading activities, such as Huatai Securities, 
with the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, the Huatai 
Ultimate Clients, through their investment managers, will place a total return swap order (“Client TRS”) 
with Huatai Securities in connection with the Company’s IPO and Huatai Securities will place a Huatai Back-
to-back TRS order to HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the 
Huatai Backto-back TRS, HTCI participates in the Company’s IPO and subscribes the Offer Shares through 
placing order with Huatai during the International Offering.
To the best of HTCI’s knowledge and after making all reasonable enquiries, each of the Huatai Ultimate 
Clients is an independent third party of (i) the Company, the connected person and/or their respective 
associates thereof, and (ii) HTCI, Huatai and the companies which are members of the same group of HTCI.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Huatai Back-to-back TRS in 
connection with the Client TRS order placed by the Huatai Ultimate Clients. Pursuant to the terms of the 
contracts of the Huatai Back-to-back TRS and the Client TRS, during the tenor of the Huatai Back-to-back 
TRS and the Client TRS, subject to customary fees and commissions, all economic returns of the Offer Shares 
will be ultimately passed to the Huatai Ultimate Clients through the Huatai Back-to-back TRS and the Client 
TRS and all economic loss shall be ultimately borne by the Huatai Ultimate Clients. HTCI will not take any 
economic return or bear any economic loss in relation to the Offer Shares.
Investment in the Huatai Back-to-back TRS and the Client TRS is similar to the investment in a qualified 
domestic institutional investor fund (“QDII”) in the way that the Huatai Ultimate Clients would reap all the 
economic benefits of the underlying Offer Shares, except that a QDII fund would pass through the exchange 
rate exposure on both the notional value of the investment and the profit and loss of the investment. In 
contrast, the profit and loss of the Huatai Back-to-back TRS and the Client TRS factor into account the 
fluctuation in RMB exchange rate upon termination of the Client TRS by converting the profit and loss using 
the current exchange rate at the time of termination. As such, the Huatai Ultimate Clients would bear the 
exchange rate exposure of the profit and loss on settlement date.
The Huatai Ultimate Clients may exercise an early termination right to terminate the Client TRS at any 
time from the issue date of the Client TRS which should be on or after the date on which the Offer Shares 
are listed on the Hong Kong Stock Exchange at their own discretions. Upon the termination upon maturity 
or early termination of the Client TRS by the Huatai Ultimate Clients, HTCI will dispose the Offer Shares 
on the secondary market and the Huatai Ultimate Clients will receive a final settlement amount in cash in 
accordance with the terms and conditions of the Huatai Back-to-back TRS and the Client TRS which should 
have taken into account all the economic returns or economic loss in relation to the Offer Shares. If upon the 
maturity of the Client TRS, the Huatai Ultimate Clients intend to extend the investment period, subject to 
further agreement between Huatai Securities and the relevant Huatai Ultimate Clients, the term of the Client 
TRS could be extended by way of a new issuance or a tenor extension. Accordingly, Huatai Securities will 
extend the term of the Huatai Back-toback TRS by way of a new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass 
through the economic exposure to the Huatai Ultimate Clients, each being an onshore client who places a 
Client TRS order with Huatai Securities in connection with the IPO of the Company. HTCI will not exercise 
the voting right of the Offer Shares during the tenor of the Huatai Back-to-back TRS.
During the life of the Client TRS and Huatai Back-to-back TRS, HTCI may continue to hold the Offer 
Shares in its custodian account, or to hold some or all of the Offer Shares in a prime brokerage account for 
stock borrowing purposes, HTCI will lend out its holding of underlying Offer Shares in the form of stock 
borrowing loans consistent with market practice to lower its finance costs, provided that HTCI has the ability 
to call back the Offer Shares on loan at any time in order to satisfy its obligations under the Huatai Back-to-
back TRS to ensure the economic interests are ultimately passed to the Huatai Ultimate Clients.

<<<PAGE 21>>>
21
2. 
The details of the ultimate beneficial owners of Huatai Ultimate Clients are as follows:
(1) 
Guangzhou Haizhu Digital Economy Industrial Investment Management Co., Limited (廣州市海珠數
字經濟創業投資管理有限公司) (“Guangzhou Haizhu”) is limited liability company established in the 
PRC. As of the date hereof, the sole ultimate beneficial owner of Guangzhou Haizhu is Haizhu District 
Bureau of Science, Industry, Commerce and Information Technology of Guangzhou Municipality (廣
州市海珠區科技工業商務和信息化局) (“Haizhu District Bureau”). Haizhu District Bureau is a 
government body under the Guangdong Provincial Government.
(2) 
Shanghai Yongjin Investment Management Co., Ltd. (上海涌津投資管理有限公司) is a limited 
liability company established in the PRC. It acts as the fund manager of Yongjin Yongxin No.52 
Private Securities Investment Fund (涌津涌鑫52號私募證券投資基金) (“Yongxin No.52 Fund”). As 
of the date hereof, Yongxin No.52 Fund has 14 limited partners and none of them holds 30% or more 
limited partnership interests.
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
(the “Hong Kong Stock Exchange”) and Hong Kong Securities Clearing Company Limited 
(“HKSCC”) take no responsibility for the contents of this announcement, make no representation 
as to its accuracy or completeness and expressly disclaim any liability whatsoever for any 
loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
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
Potential investors should read the Prospectus dated March 20, 2026 issued by Hangzhou 
Diagens Biotechnology Co., Ltd. for detailed information about the Global Offering described 
below before deciding whether or not to invest in the Shares thereby being offered.

<<<PAGE 22>>>
22
Potential investors of the Offer Shares should note that the Sponsor-overall Coordinator 
(for itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the 
occurrence of any of the events set out in the paragraph headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Hong Kong Underwriting 
Agreement — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong 
Kong time) on the Listing Date (which is currently expected to be on Monday, March 30, 2026).
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering and the conversion of Unlisted 
Shares into H Shares, an aggregate of 46,777,043 H Shares, representing approximately 52.63% 
of the total issued share capital of the Company will be held in the public hands for the purpose 
of Rule 8.08 of the Listing Rules, which is higher than the prescribed percentage of H Shares 
required to be held in public hands of 15% with the expected market value at the time of listing 
over HK$6,000,000,000 but not exceeding HK$30,000,000,000 under the Rule 8.08(1), calculated 
based on the final Offer Price of HK$99.0 per H Share, thereby satisfying Rule 19A.13A(1) of the 
Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public Shareholders 
do not hold more than 50% of the Shares held in the public hands at the time of the Listing in 
compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 
Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Monday, 
March 30, 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the paragraph headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” in the 
Prospectus has not been exercised. Investors who trade the H Shares on the basis of publicly 
available allocation details prior to the receipt of H Share certificates or prior to the H Share 
certificates becoming valid evidence of title do so entirely at their own risk.

<<<PAGE 23>>>
23
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. Monday, March 
30, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Hong Kong Stock 
Exchange will commence at 9:00 a.m. on Monday, March 30, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 50 H Shares each, and the stock code of the H Shares will be 
2526.
By order of our Board
Hangzhou Diagens Biotechnology Co., Ltd.
Song Ning
Chairman of the Board and Executive Director
Hong Kong, March 27, 2026
As of the date of this announcement, the Board comprises: (i) Dr. Song Ning and Mr. Weng 
Chih-Hsin (alias Robin Weng) as executive Directors; (ii) Dr. Xu Chen, Dr. Wu Lingqian and Mr. 
Yang Zehao as non-executive Directors; and (iii) Mr. Cha Yang (alias Stanley Cha), Ms. Zhang 
Jing and Mr. Wang Kaifeng as independent non-executive Directors.
