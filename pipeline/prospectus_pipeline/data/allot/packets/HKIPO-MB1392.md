# 配发结果公告抽取任务：1392.HK Shenzhen HQVT Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**18/06/2026 22:24**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0618/2026061802066.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1392.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Exchange”, or the “Hong Kong Stock Exchange”) and Hong Kong Securities Clearing Company Limited 
(“HKSCC”) take no responsibility for the contents of this announcement, make no representation as to its 
accuracy or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings 
as those defined in the prospectus dated Thursday, 11 June 2026 (the “Prospectus”) of Shenzhen HQVT 
Technology Co., Ltd. (深圳海清智元科技股份有限公司) (the “Company”). This announcement is made by 
the order of the board (the “Board”) of directors (the “Directors”) of the Company. The Board collectively 
and individually accept responsibility for the accuracy of this announcement.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for any securities. This announcement is not a prospectus. Potential investors should 
read the Prospectus for detailed information about the Global Offering described below before deciding 
whether or not to invest in the Offer Shares. Any investment decision in relation to the Offer Shares should be 
taken solely in reliance on the information provided in the Prospectus.
This announcement is not for release, publication or distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia or 
any other jurisdiction where such distribution is prohibited by laws). This announcement does not constitute 
or form a part of any offer or solicitation to purchase or subscribe for securities in the United States or in 
any other jurisdictions. The securities mentioned herein have not been, and will not be, registered under the 
United States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or securities 
law of any state or other jurisdiction of the United States. The securities may not be offered, sold, pledged 
or otherwise transferred within the United States except pursuant to an exemption from the registration 
requirements of the U.S. Securities Act and in compliance with any applicable state securities laws, or (1) 
solely to qualified institutional buyers as defined in Rule 144A under the U.S. Securities Act pursuant to 
an exemption from registration under the U.S. Securities Act and (2) outside the United States unless in 
compliance with Regulation S under the U.S. Securities Act. There will be no public offer of securities in the 
United States.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to terms and conditions 
set out in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside 
Hong Kong and/or not resident in Hong Kong. Potential investors of the Offer Shares should note that the 
Joint Sponsors and the Sponsor-Overall Coordinators (for themselves and on behalf of the Hong Kong 
Underwriters) shall be entitled to terminate the Hong Kong Underwriting Agreement with immediate effect 
upon the occurrence of any of the events set out in the section headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus 
at any time prior to 8:00 a.m. on the Listing Date.

<<<PAGE 2>>>
– 2 –
Shenzhen HQVT Technology Co., Ltd.
深圳海清智元科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under 
the Global Offering:
85,162,500 H Shares
Number of Hong Kong Offer Shares:
8,516,500 H Shares 
Number of International Placing Shares:
76,646,000 H Shares
Final Offer Price:
HK$7.20 per Offer Share, plus brokerage 
of 1.0%, SFC transaction levy of 
0.0027%, Stock Exchange trading fee 
of 0.00565% and AFRC transaction 
levy of 0.00015%
Nominal value:
RMB0.0125 per H Share
Stock code:
1392
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators,  
Joint Global Coordinators, Joint Bookrunners, and Joint Lead Managers
Financial Adviser
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and  
Joint Lead Manager
Joint Bookrunners and Joint Lead Managers
SOMERLEY CAPITAL LIMITED

<<<PAGE 3>>>
 
-3-  
  
SHENZHEN HQVT TECHNOLOGY CO., LTD.  
深圳海清智元科技股份有限公司  
ANNOUNCEMENT OF ALLOTMENT RESULTS  
 
  
Warning: In view of high concentration of shareholding in a small number of H Shareholders, H 
Shareholders and prospective investors should be aware that the price of the H Shares could move 
substantially even with a small number of the H Shares traded and should exercise extreme caution 
when dealing in the H Shares.  
SUMMARY  
  
Company information  
 
Stock code   
1392 
Stock short name   
HQVT  
Dealings commencement date  
22 June 2026*  
*see note at the end of the announcement  
  
Price Information   
 
Offer Price  
HK$7.20  
  
Offer Shares and Share Capital  
Number of Offer Shares  
85,162,500 
Final Number of Offer Shares in Hong Kong Public Offering 8,516,500 
Final Number of Offer Shares in International Placing  
76,646,000 
Number of issued Shares upon Listing  
774,208,420 
 
 
Proceeds    
Gross proceeds (Note)   
HK$613.17 million  
Less: Estimated listing expenses payable based on Offer 
Price   
HK$76.34 million 
Net proceeds   
HK$536.83 million 
  
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use 
of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus dated 
11 June 2026. 
  
  
 
 

<<<PAGE 4>>>
 
-4-  
  
 
ALLOTMENT RESULTS DETAILS  
HONG KONG PUBLIC OFFERING  
  
 
No. of valid applications   
252,640 
No. of successful applications   
17,033 
Subscription level  
7,181.21 times 
Claw-back triggered   
N/A  
No. of Offer Shares initially available under the Hong Kong Public 
Offering   
8,516,500 H Shares 
No. of Offer Shares reallocated from the International Placing 
0 
Final no. of Offer Shares under the Hong Kong Public Offering 
8,516,500 H Shares  
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering  
10%  
  
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
https://www.hkeipo.hk/iporesult 
to 
perform 
a 
search 
by 
name 
or 
identification 
number 
or 
https://www.hkeipo.hk/iporesult for the full list of allottees.  
INTERNATIONAL PLACING  
  
 
No. of placees  
137 
Subscription level  
4.81 times  
No. of Offer Shares initially available under the International 
Placing   
76,646,000 H Shares 
No. of Offer Shares reallocated to the Hong Kong Public Offering 
0 
Final no. of Offer Shares under the International Placing  
76,646,000 H Shares 
% of final no. of Offer Shares under the International Placing to the 
Global Offering 
90%  
  
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the Offer Shares 
subscribed by the placees and the public have been financed directly or indirectly by the Company, any of the 
Directors, chief executive of the Company, Controlling Shareholders, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates; (ii) none of the 
placees and the public who have purchased the Offer Shares are accustomed to taking instructions from the 
Company, any of the Directors, chief executive of the Company, Controlling Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective close 
associates in relation to the acquisition, disposal, voting or other disposition of Shares registered in his/her/its 
name or otherwise held by him/her/it. 
 
 

<<<PAGE 5>>>
 
-5-  
  
   
LOCK-UP UNDERTAKINGS   
Controlling Shareholders  
Name 
Number of 
Shares held in 
the Company 
subject to 
lock-up  
undertakings 
upon 
Listing   
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up  
undertakings 
upon 
Listing  
% of total issued 
H Shares after 
the 
Global Offering 
subject to lock-up 
undertakings 
upon Listing 
% of 
shareholding in 
the 
Company subject 
to 
lock-up 
undertakings 
upon Listing  
Last day 
subject to 
the lock-up 
undertakings 
Note 1 
Zhou Bo 
(“Mr. Zhou”) 
(周波) Note3 
41,082,080 
41,082,080 
5.43% 
5.31% 21 
December 2026 
(First Six- 
Month Period)  
 
21 June 2027 
(Second Six- 
Month 
Period)Note2 
Shenzhen 
Zhongcheng 
Tianying 
Venture 
Capital 
Partnership 
(Limited 
Partnership)(“
Zhongcheng 
Tianying”) 
(深圳市眾誠
天盈創業投資
合夥企業(有
限合夥)) Note3 
264,150,960 
264,150,960 
34.93% 
34.12% 21 
December 2026 
(First Six- 
Month Period)  
 
21 June 2027 
(Second Six- 
Month 
Period)Note2 
Shenzhen 
Zhongzheng 
Tianying 
Venture 
Capital 
Partnership 
(Limited 
Partnership) 
(“Zhongzheng 
Tianying”) 
(深圳市眾正
19,200,000 
19,200,000 
2.54% 
2.48% 21 
December 2026 
(First Six- 
Month Period)  
 
21 June 2027 
(Second Six- 
Month 
Period)Note2 

<<<PAGE 6>>>
 
-6-  
  
Name 
Number of 
Shares held in 
the Company 
subject to 
lock-up  
undertakings 
upon 
Listing   
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up  
undertakings 
upon 
Listing  
% of total issued 
H Shares after 
the 
Global Offering 
subject to lock-up 
undertakings 
upon Listing 
% of 
shareholding in 
the 
Company subject 
to 
lock-up 
undertakings 
upon Listing  
Last day 
subject to 
the lock-up 
undertakings 
Note 1 
天盈創業投資
合夥企業(有
限合夥)) Note3 
Shenzhen 
Zhongzhi 
Tianying 
Venture 
Capital 
Partnership 
(Limited 
Partnership) 
(“Zhongzhi 
Tianying”) (深
圳市眾知天盈
創業投資合夥
企業(有限合
夥)) Note3 
12,329,040 
12,329,040 
1.63% 
1.59% 21 
December 2026 
(First Six- 
Month Period)  
 
21 June 2027 
(Second Six- 
Month 
Period)Note2 
Subtotal 
336,762,080 
336,762,080 
44.53% 
43.50%  
Notes:  
  
1. 
In accordance with the relevant Listing Rules/guidance materials, the required lock-up for the first six-month period ends on 21 December 
2026 and for the second six-month period, on 21 June 2027. In addition, pursuant to the applicable PRC law, within the 12 months 
following the Listing Date, all existing Shareholders (including the Controlling Shareholders) are prohibited from disposing of any of the 
Shares held by them. 
 
2. 
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after the indicated date.  
 
3. 
Upon Listing, Mr. Zhou, Zhongcheng Tianying, Zhongzheng Tianying and Zhongzhi Tianying will be, in aggregate, entitled to control the 
exercise of approximately 43.50% of the voting rights and therefore will remain as a group of Controlling Shareholders. For further 
details, please refer to “Relationship with Controlling Shareholders” in the Prospectus. This subsection illustrates their direct 
shareholding in the Company, and each of them is subject to the same lock-up as disclosed above. 
  
  
 
 

<<<PAGE 7>>>
 
-7-  
  
 
Other Existing Shareholders (including the Pre-IPO Investors as defined in the “History, Development 
and Corporate Structure” section of the Prospectus) 
 
Name  
Number of 
Shares held in 
the Company 
subject to lock-
up  
undertakings 
upon 
Listing 
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up  
undertakings 
upon 
Listing  
% of total issued 
H Shares after 
the 
Global Offering 
subject to lock-
up 
undertakings 
upon Listing Note  
% of 
shareholding in 
the 
Company 
subject to 
lock-up 
undertakings 
upon Listing Note 
Last day 
subject to 
the lock-up 
undertakings 
Note 
Shenzhen Langke 
Investment Co., 
Ltd. (深圳市朗科
投資有限公司) 
14,400,000 
14,400,000 
1.90% 
1.86% 21 June 2027 
Shenzhen Kaiying 
No. 8 
Venture Capital 
Partnership 
(Limited 
Partnership) (深圳
凱盈八號創業投資
合夥企業(有限合
夥)) 
8,722,560 
8,722,560 
1.15% 
1.13% 21 June 2027 
Shenzhen Kaiying 
No. 9 
Venture Capital 
Partnership(Limited 
Partnership) (深圳
凱盈九號創業投資
合夥企業(有限合
夥)) 
8,722,560 
8,722,560 
1.15% 
1.13% 21 June 2027 
Shenzhen Kaiying 
No.10 
Venture Capital 
Partnership 
Enterprise (Limited 
Partnership) (深圳
凱盈十號創業投資
合夥企業(有限合
夥)) 
13,530,320 
13,530,320 
1.80% 
1.75% 21 June 2027 
Shenzhen Taolue 
New Energy 
52,335,360 
52,335,360 
6.92% 
6.76% 21 June 2027 

<<<PAGE 8>>>
 
-8-  
  
Name  
Number of 
Shares held in 
the Company 
subject to lock-
up  
undertakings 
upon 
Listing 
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up  
undertakings 
upon 
Listing  
% of total issued 
H Shares after 
the 
Global Offering 
subject to lock-
up 
undertakings 
upon Listing Note  
% of 
shareholding in 
the 
Company 
subject to 
lock-up 
undertakings 
upon Listing Note 
Last day 
subject to 
the lock-up 
undertakings 
Note 
Equity Investment 
Fund 
Partnership 
Enterprise (Limited 
Partnership) (深圳
韜略新能源股權投
資基金合夥企業
(有限合夥)) 
Shenzhen Taolue 
Xinwang 
Venture Capital 
Partnership 
Enterprise (Limited 
Partnership) (深圳
韜略信旺創業投資
合夥企業(有限合
夥)) 
9,664,480 
9,664,480 
1.28% 
1.25% 21 June 2027 
Jinhua Jinlan 
Sunshine Strategy 
Venture Capital 
Partnership 
(Limited 
Partnership) (金華
市金蘭陽光韜略創
業投資合夥企業
(有限合夥)) 
40,356,880 
40,356,880 
5.34% 
5.21% 21 June 2027 
Shenzhen HTI 
Venture Capital 
Co., Ltd. (深圳市
高新投創業投資有
限公司) 
13,894,320 
13,894,320 
1.84% 
1.79% 21 June 2027 
Chengdu Shengao 
Investment 
Zhongxiaodan 
Entrepreneurship 
11,810,240 
11,810,240 
1.56% 
1.53% 21 June 2027 

<<<PAGE 9>>>
 
-9-  
  
Name  
Number of 
Shares held in 
the Company 
subject to lock-
up  
undertakings 
upon 
Listing 
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up  
undertakings 
upon 
Listing  
% of total issued 
H Shares after 
the 
Global Offering 
subject to lock-
up 
undertakings 
upon Listing Note  
% of 
shareholding in 
the 
Company 
subject to 
lock-up 
undertakings 
upon Listing Note 
Last day 
subject to 
the lock-up 
undertakings 
Note 
Equity Investment 
Fund Partnership 
Enterprise (Limited 
Partnership) (成都
深高投中小擔創業
股權投資基金合夥
企業(有限合夥)) 
Shenzhen City 
Talent Innovation 
Venture II Equity 
Investment Fund 
Partnership 
(Limited 
Partnership) (深圳
市人才創新創業二
號股權投資基金合
夥企業(有限合夥)) 
5,557,680 
5,557,680 
0.74% 
0.72% 21 June 2027 
Beward Invest 
Limited (畢沃德貿
易(深圳)有限公司) 
68,780,320 
68,780,320 
9.10% 
8.88% 21 June 2027 
Chen Yonggang (陳
永剛) 
23,774,800 
23,774,800 
3.14% 
3.07% 21 June 2027 
Xia Dong (夏東) 
23,040,000 
23,040,000 
3.05% 
2.98% 21 June 2027 
Zhu Zhenkui (朱振
奎) 
18,064,480 
— 
— 
2.33% 21 June 2027 
Shenzhen Shenrong 
Ruihe Venture 
Capital Partnership 
(Limited 
Partnership) (深圳
深蓉瑞合創業投資
合夥企業(有限合
夥)) 
2,084,080 
2,084,080 
0.28% 
0.27% 21 June 2027 
Shenzhen Xiaohe 
Investment 
1,389,440 
1,389,440 
0.18% 
0.18% 21 June 2027 

<<<PAGE 10>>>
 
-10-  
  
Name  
Number of 
Shares held in 
the Company 
subject to lock-
up  
undertakings 
upon 
Listing 
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up  
undertakings 
upon 
Listing  
% of total issued 
H Shares after 
the 
Global Offering 
subject to lock-
up 
undertakings 
upon Listing Note  
% of 
shareholding in 
the 
Company 
subject to 
lock-up 
undertakings 
upon Listing Note 
Last day 
subject to 
the lock-up 
undertakings 
Note 
Partnership 
(Limited 
Partnership) (深圳
市小禾創業投資合
夥企業(有限合夥)) 
Shenzhen Fuquan 
No.1 Investment 
Partnership 
Enterprise (Limited 
Partnership) (深圳
福泉壹號投資合夥
企業(有限合夥)) 
5,798,720 
5,798,720 
0.77% 
0.75% 21 June 2027 
Shenzhen Panhui 
Investment 
Development Co., 
Ltd. （深圳市攀輝
投資發展有限公
司） 
6,726,160 
6,726,160 
0.89% 
0.87% 21 June 2027 
Hainan Kezhihua 
Digital Technology 
Co., Ltd. (海南科
智華數字技術有限
公司) 
13,926,560 
13,926,560 
1.84% 
1.79% 21 June 2027 
Shanghai No. 9 
Private 
Investment Fund 
Partnership 
Enterprise (Limited 
Partnership) (上海
值得九號私募投資
基金合夥企業(有
限合夥)) 
9,704,880 
9,704,880 
1.28% 
1.25% 21 June 2027 
Subtotal 
352,283,840 
334,219,360 
44.21% 
45.50%  
Note: Pursuant to the applicable PRC law, within the 12 months following the Listing Date, all existing Shareholders 
(including the Pre-IPO Investors) are prohibited from disposing of any of the Shares held by them. 

<<<PAGE 11>>>
 
-11- 
 
PLACEE CONCENTRATION ANALYSIS 
Placees* 
Number of 
H Shares 
allotted 
Allotment 
as % of 
International 
Placing 
Allotment 
as % of total 
Offer Shares 
Number of 
Shares held 
upon 
Listing 
% of total 
issued share 
capital upon 
Listing 
Top 1 
10,095,000  
13.17% 
11.85% 
10,095,000 
1.30% 
Top 5 
28,338,500  
36.97% 
33.28% 
28,338,500 
3.66% 
Top 10 
39,170,000  
51.11% 
45.99% 
39,170,000 
5.06% 
Top 25 
53,622,500  
69.96% 
62.96% 
53,622,500 
6.93% 
 
Note: 
* Ranking of placees is based on the number of H Shares allotted to the placees. 
 
H SHAREHOLDERS CONCENTRATION ANALYSIS 
H 
Shareholders* 
Number 
of 
H Shares 
allotted 
Allotment 
as % of 
Internationa
l Placing 
Allotment 
as % of 
total 
Offer 
Shares 
Number of 
Shares held 
upon 
Listing 
% of 
total 
issued 
H 
Shares 
capital 
upon 
Listing 
Number of 
Shares held 
upon 
Listing 
Top 1 
0 
0.00% 
0.00% 336,762,080  44.54% 
336,762,080 
Top 5 
0  
0.00% 
0.00% 584,536,800  77.30% 
584,536,800 
Top 10 
10,095,000 
13.17% 
11.85% 665,078,040  87.96% 
665,078,040 
Top 25 
41,921,000  
54.69% 
49.22% 712,902,440  94.28% 
712,902,440 
 
Note: 
* Ranking of H Shareholders is based on the number of H Shares held by the Shareholders upon Listing.  
 
 

<<<PAGE 12>>>
 
-12- 
 
SHAREHOLDERS CONCENTRATION ANALYSIS 
Shareholders* 
Number 
of 
H Shares 
allotted 
Allotment 
as % of 
Internationa
l Placing 
Allotment 
as % of 
total 
Offer 
Shares 
Number of 
H Shares 
held upon 
Listing 
Number of 
Shares held 
upon 
Listing 
% of 
total 
issued 
share 
capital 
upon 
Listing 
Top 1 
0 
0.00% 
0.00% 336,762,080  336,762,080 
43.50% 
Top 5 
0  
0.00% 
0.00% 584,536,800  584,536,800 
75.50% 
Top 10 
10,095,000 
13.17% 
11.85% 655,373,160  673,437,640 
86.98% 
Top 25 
40,558,500  
52.92% 
47.62% 711,539,940  729,604,420 
94.24% 
 
Note: 
* Ranking of Shareholders is based on the number of Shares held by the Shareholders upon Listing.  
 
 

<<<PAGE 13>>>
 
-13- 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING  
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by the 
public will be conditionally allocated on the basis set out below:  
  
NO. OF H 
SHARES 
APPLIED FOR 
NO. OF VALID 
APPLICATION
S 
BASIS OF 
ALLOTMENT/BALLOT 
POOL A 
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE 
TOTAL NO. OF H 
SHARES APPLIED 
FOR 
500 
55,745 
1,115 out of 55,745 applicants to 
receive 500 H Shares 
2.00% 
1,000 
28,250 
655 out of 28,250 applicants to 
receive 500 H Shares 
1.16% 
1,500 
8,229 
208 out of 8,229 applicants to 
receive 500 H Shares 
0.84% 
2,000 
4,470 
121 out of 4,470 applicants to 
receive 500 H Shares 
0.68% 
2,500 
4,575 
129 out of 4,575 applicants to 
receive 500 H Shares 
0.56% 
3,000 
3,218 
95 out of 3,218 applicants to 
receive 500 H Shares 
0.49% 
3,500 
2,139 
65 out of 2,139 applicants to 
receive 500 H Shares 
0.43% 
4,000 
2,336 
73 out of 2,336 applicants to 
receive 500 H Shares 
0.39% 
4,500 
1,901 
61 out of 1,901 applicants to 
receive 500 H Shares 
0.36% 
5,000 
7,153 
234 out of 7,153 applicants to 
receive 500 H Shares 
0.33% 
6,000 
12,903 
438 out of 12,903 applicants to 
receive 500 H Shares 
0.28% 
7,000 
3,110 
109 out of 3,110 applicants to 
receive 500 H Shares 
0.25% 
8,000 
2,416 
88 out of 2,416 applicants to 
receive 500 H Shares 
0.23% 
9,000 
2,316 
86 out of 2,316 applicants to 
receive 500 H Shares 
0.21% 
10,000 
10,714 
406 out of 10,714 applicants to 
receive 500 H Shares 
0.19% 
15,000 
5,646 
233 out of 5,646 applicants to 
receive 500 H Shares 
0.14% 
20,000 
3,866 
170 out of 3,866 applicants to 
receive 500 H Shares 
0.11% 

<<<PAGE 14>>>
 
-14- 
 
NO. OF H 
SHARES 
APPLIED FOR 
NO. OF VALID 
APPLICATION
S 
BASIS OF 
ALLOTMENT/BALLOT 
POOL A 
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE 
TOTAL NO. OF H 
SHARES APPLIED 
FOR 
25,000 
3,500 
161 out of 3,500 applicants to 
receive 500 H Shares 
0.09% 
30,000 
2,766 
133 out of 2,766 applicants to 
receive 500 H Shares 
0.08% 
35,000 
1,953 
97 out of 1,953 applicants to 
receive 500 H Shares 
0.07% 
40,000 
2,077 
106 out of 2,077 applicants to 
receive 500 H Shares 
0.06% 
45,000 
1,687 
88 out of 1,687 applicants to 
receive 500 H Shares 
0.06% 
50,000 
3,570 
191 out of 3,570 applicants to 
receive 500 H Shares 
0.05% 
60,000 
2,840 
158 out of 2,840 applicants to 
receive 500 H Shares 
0.05% 
70,000 
2,494 
143 out of 2,494 applicants to 
receive 500 H Shares 
0.04% 
80,000 
2,126 
126 out of 2,126 applicants to 
receive 500 H Shares 
0.04% 
90,000 
1,598 
97 out of 1,598 applicants to 
receive 500 H Shares 
0.03% 
100,000 
11,217 
692 out of 11,217 applicants to 
receive 500 H Shares 
0.03% 
200,000 
7,156 
512 out of 7,156 applicants to 
receive 500 H Shares 
0.02% 
300,000 
5,384 
420 out of 5,384 applicants to 
receive 500 H Shares 
0.01% 
400,000 
3,917 
325 out of 3,917 applicants to 
receive 500 H Shares 
0.01% 
500,000 
4,073 
354 out of 4,073 applicants to 
receive 500 H Shares 
0.01% 
600,000 
6,952 
628 out of 6,952 applicants to 
receive 500 H Shares 
0.01% 
Total 
222,297 
Total number of Pool A 
successful applications: 8,517 
 
 
 
 

<<<PAGE 15>>>
 
-15- 
 
  
NO. OF H 
SHARES 
APPLIED FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF 
ALLOTMENT/BALLOT 
POOL B 
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE 
TOTAL NO. OF H 
SHARES APPLIED 
FOR 
700,000 
7,164 
1,003 out of 7,164 applicants to 
receive 500 H Shares 
0.01% 
800,000 
2,799 
442 out of 2,799 applicants to 
receive 500 H Shares 
0.01% 
900,000 
2,385 
418 out of 2,385 applicants to 
receive 500 H Shares 
0.01% 
1,000,000 
8,197 
1,579 out of 8,197 applicants to 
receive 500 H Shares 
0.01% 
2,000,000 
3,954 
1,415 out of 3,954 applicants to 
receive 500 H Shares 
0.01% 
3,000,000 
2,366 
1,216 out of 2,366 applicants to 
receive 500 H Shares 
0.01% 
4,258,000 
3,478 
2,443 out of 3,478 applicants to 
receive 500 H Shares 
0.01% 
Total 
30,343 
Total number of Pool B 
successful applications: 8,516 
 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries. 
 
 

<<<PAGE 16>>>
 
-16- 
 
COMPLIANCE WITH LISTING RULES AND GUIDANCE   
The Directors confirm that the Company has complied with the Listing Rules and guidance materials 
in relation to the placing, allotment and listing of the H Shares.   
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the 
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by 
them is the same as the Offer Price in addition to any brokerage, AFRC transaction levy, SFC 
transaction levy and trading fee payable.  
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or indirectly, 
provided by the Company, the Controlling Shareholders, the Directors or syndicate members to any 
placees or the public (as the case may be) and the consideration paid by the placees or the public (as 
the case may be) directly or indirectly for each Offer Share subscribed for or purchased by them was 
the same as the Offer Price in addition to any brokerage, AFRC transaction levy, SFC transaction levy 
and Stock Exchange trading fee payable. 
 
 

<<<PAGE 17>>>
 
-17- 
 
DISCLAIMERS  
  
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong 
Kong Securities Clearing Company Limited take no responsibility for the contents of this announcement, 
make no representation as to its accuracy or completeness and expressly disclaim any liability whatsoever 
for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.  
This announcement is not for release, publication or distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia 
or any other jurisdiction where such distribution is prohibited by laws). This announcement does not 
constitute or form a part of any offer or solicitation to purchase or subscribe for securities in the United 
States or in any other jurisdictions. The securities mentioned herein have not been, and will not be, 
registered under the United States Securities Act of 1933 as amended from time to time (the “U.S. 
Securities Act”) or securities law of any state or other jurisdiction of the United States. The securities may 
not be offered, sold, pledged or otherwise transferred within the United States except pursuant to an 
exemption from the registration requirements of the U.S. Securities Act and in compliance with any 
applicable state securities laws. The Offer Shares are being offered and sold solely (a) to qualified 
institutional buyers as defined in Rule 144A under the U.S. Securities Act pursuant to Rule 144A or another 
available exemption from registration under the U.S. Securities Act and (2) outside the United States in 
offshore transactions in reliance on Regulation S under the U.S. Securities Act.  
This announcement is for information purposes only and does not constitute an invitation or offer to 
acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential investors 
should read the Prospectus dated 11 June 2026 issued by Shenzhen HQVT Technology Co., Ltd. for detailed 
information about the Global Offering described below before deciding whether or not to invest in the 
Offer Shares thereby being offered.  
*Potential investors of the Offer Shares should note that the Overall Coordinators (for themself and on 
behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong 
Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in 
the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public 
Offering – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) 
on the Listing Date (which is currently expected to be on Monday, 22 June 2026).  
  
 
 

<<<PAGE 18>>>
– 18 –
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, an aggregate of 293,250,340 
H Shares, representing approximately 37.88% of the total number of shares in the class to 
which H Shares of our Company belong will be counted towards the public float. Therefore, 
the number of H Shares held in public hands is higher than the prescribed percentage of H 
Shares required to be held in public hands of 25% of the total number of shares in the class 
to which H Shares belong under Rule 19A.13A(1) of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering, 
(i) no placee will, individually, be placed more than 10% of the enlarged issued share 
capital of the Company immediately after the Global Offering; (ii) there will not be any new 
substantial Shareholder immediately after the Global Offering; (iii) the three largest public 
shareholders of the Company do not hold more than 50% of the H Shares in public hands at 
the time of the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and 
(iv) there will be at least 300 Shareholders at the time of the Listing in compliance with Rule 
8.08(2) of the Listing Rules.
Based on an Offer Price of HK$7.2 per Offer Share, the Company will satisfy the free float 
requirement under Rule 19A.13A(1) of the Listing Rules.
COMMENCEMENT OF DEALINGS
H Share certificates will only become valid at 8:00 a.m. on Monday, 22 June 2026 (Hong 
Kong time), provided that the Global Offering has become unconditional and the right of 
termination described in the section headed “Underwriting — Underwriting Arrangements 
and Expenses — Hong Kong Public Offering — Grounds for Termination” in the 
Prospectus has not been exercised. Investors who trade H Shares prior to the receipt of H 
Share certificates or the H Share certificates becoming valid do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on 
Monday, 22 June 2026 (Hong Kong time), it is expected that dealings in the H Shares on the 
Stock Exchange will commence at 9:00 a.m. on Monday, 22 June 2026 (Hong Kong time). 
The H Shares will be traded in board lots of 500 H Shares each. The stock code of the H 
Shares will be 1392.
By order of the Board
Shenzhen HQVT Technology Co., Ltd.
Mr. Zhou Bo
Chairman of the Board
Hong Kong, 18 June 2026
As of the date of this announcement, the Board comprises: (i) Mr. Zhou Bo, Mr. Miao Rui, Dr. Chai Jian, Mr. 
Zou Xiaogang and Mr. Chen Yonggang as executive Directors; (ii) Mr. Yu Lijie as non-executive Directors; 
(iii) Mr. Chen Haiping, Mr. Zhong Luhuan and Ms. Ho Ka Cin Verona as independent non-executive 
Directors.
