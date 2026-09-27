# 配发结果公告抽取任务：6106.HK Shanghai Seer Intelligent Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**23/06/2026 22:57**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0623/2026062302143.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6106.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings 
as those defined in the prospectus dated June 15, 2026 (the “Prospectus”) issued by Shanghai Seer 
Intelligent Technology Co., Ltd. (上海仙工智能科技股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. Potential investors should read the Prospectus for detailed information 
about the Company and the Global Offering described below before deciding whether or not to invest in the 
Offer Shares.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe 
for securities in the United States or in any other jurisdictions. The securities mentioned herein have not 
been, and will not be, registered under the United States Securities Act of 1933 as amended from time to time 
(the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the United States and may 
not be offered, sold, pledged or otherwise transferred within the United States except in transactions exempt 
from, or not subject to, the registration requirements of the U.S. Securities Act. There will be no public offer 
of securities in the United States. The Offer Shares are being offered and sold outside the United States in 
offshore transactions in reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities 
Limited, as stabilizing manager (the “Stabilizing Manager”), or any person acting for it, on behalf of the 
Underwriters, may over-allocate or effect transactions with a view to stabilizing or supporting the market 
price of the Shares at a level higher than that which might otherwise prevail for a limited period after the 
Listing Date. However, there is no obligation on the Stabilizing Manager, or any person acting for it to 
conduct any such stabilizing action, which, if commenced, will be done at the sole and absolute discretion 
of the Stabilizing Manager, or any person acting for it, and may be discontinued at any time. Any such 
stabilizing action is required to be brought to an end on the 30th day after the last day for the lodging of 
applications under the Hong Kong Public Offering. Such stabilizing action, if taken, may be effected in all 
jurisdictions where it is permissible to do so, in each case in compliance with all applicable laws, rules and 
regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of 
the Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter 571 of the 
Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the Shares 
for longer than the stabilization period, which begins on the Listing Date and is expected to expire on the 
30th day after the last day for lodging applications under the Hong Kong Public Offering. After this date, 
when no further stabilizing action may be taken, demand for the Shares, and therefore the price of the Shares, 
could fall.
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinator (for itself and on 
behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section 
headed “Underwriting — Underwriting Arrangements and Expenses — The Hong Kong Public Offering — 
Hong Kong Underwriting Agreement — Grounds for Termination” in the Prospectus at any time prior to 
8:00 a.m. (Hong Kong time) on the Listing Date.

<<<PAGE 2>>>
– 2 –
Shanghai Seer Intelligent Technology Co., Ltd.
上海仙工智能科技股份有限公司
(A joint stock company established in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares 
under the Global Offering
:
10,497,300 H Shares (subject to the 
Over-allotment Option)
Number of Hong Kong Offer Shares
:
2,099,500 H Shares (as adjusted after 
reallocation)
Number of International Offer Shares
:
8,397,800 H Shares (as adjusted after 
allocation and subject to the Over-
allotment Option)
Offer Price
:
HK$101.60 per H Share, plus brokerage 
of 1.0%, AFRC transaction levy of 
0.00015%, SFC transaction levy of 
0.0027% and Stock Exchange trading 
fee of 0.00565%
Nominal value
:
RMB1.00 per H Share
Stock code
:
06106
Sole Sponsor, Sponsor-Overall Coordinator, Overall Coordinators,  
Joint Global Coordinators, Bookrunners and Joint Lead Managers
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and  
Joint Lead Managers
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
– 3 –
Shanghai Seer Intelligent Technology Co., Ltd.
上海仙工智能科技股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated June 15, 2026 (the “Prospectus”) 
issued by Shanghai Seer Intelligent Technology Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, Shareholders and prospective investors should be aware that the price 
of the H Shares could move substantially even with a small number of H Shares traded 
and should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
06106
Stock short name
SEER TECH
Dealings commencement date
June 24, 2026*
*  see note at the end of the announcement
Price Information
Final Offer Price
HK$101.60
Offer Price Range
N/A
Offer Price Adjustment exercised
N/A

<<<PAGE 4>>>
– 4 –
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the Over-
allotment Option)
10,497,300
Number of Offer Shares in Hong Kong Public 
Offering (after reallocation)
2,099,500
Number of Offer Shares in International Offering 
(after reallocation and before exercise of the Over-
allotment Option)
8,397,800
Number of issued Shares upon Listing (before 
exercise of the Over-allotment Option)
110,497,300
Offer Size Adjustment Option (Upsize option)
Number of additional shares issued under the option
0*
— Hong Kong Public Offering
—
— International Offering
—
*  The Offer Size Adjustment Option has not been exercised.
Over-allocation
No. of Offer Shares over-allocated
1,574,550
Such over-allocation may be covered by exercising the Over-allotment Option or by 
making purchases in the secondary market at prices that do not exceed the Offer Price 
or through deferred delivery or a combination of these means. In the event the Over-
allotment Option is exercised, an announcement will be made on the Stock Exchange’s 
website.

<<<PAGE 5>>>
– 5 –
Proceeds
Gross proceeds (Note)
HK$1,066.5 million
Less: Estimated listing expenses payable based on 
Final Offer Price
HK$(71.2) million
Net proceeds
HK$995.4 million
Note:	
1.	
Gross proceeds refers to the amount to which the issuer is entitled to receive. For details of 
the use of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of 
the Prospectus. The Company will adjust the allocation of the net proceeds from the exercise 
of the Over-allotment Option (if any) for the purposes as set out in the section headed “Future 
Plans and Use of Proceeds” of the Prospectus on a pro rata basis.
	
2.	
The discrepancy in the table between total and sums of amounts listed therein is due to 
rounding.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
222,966
No. of successful applications
38,687
Subscription level
5,934.56 times
Claw-back triggered
Yes
No. of Offer Shares initially available under the 
Hong Kong Public Offering
524,900
No. of Offer Shares reallocated from the 
International Offering (claw-back)
1,574,600
Final no. of Offer Shares under the Hong Kong 
Public Offering (after reallocation)
2,099,500
% of Offer Shares under the Hong Kong Public 
Offering to the Global Offering (before the exercise 
of the Over-allotment Option)
20.00%
Note:	For details of the final allocation of Shares to the Hong Kong Public Offering, investors 
can refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification number 
or  www.eipo.com.hk/eIPOAllotment for the full list of allottees.

<<<PAGE 6>>>
– 6 –
INTERNATIONAL OFFERING
No. of placees
134
Subscription Level
21.29 times
No. of Offer Shares initially available under the 
International Offering
9,972,400
Final no. of Offer Shares under the International 
Offering (after reallocation and before the exercise 
of the Over-allotment Option)
8,397,800
% of Offer Shares under the International Offering 
to the Global Offering before the exercise of the 
Over-allotment Option
80.00%
The Directors confirm that, to the best of their knowledge, information and belief, (i) none 
of the Offer Shares subscribed by the placees and the public have been financed directly or 
indirectly by the Company, any of the Directors, chief executive of the Company, controlling 
shareholders, substantial shareholders, existing shareholders of the Company or any of 
its subsidiaries or their respective close associates; and (ii) none of the placees and the 
public who have purchased the Offer Shares are accustomed to taking instructions from the 
Company, any of the Directors, chief executive of the Company, controlling shareholders, 
substantial shareholders, existing shareholders of the Company or any of its subsidiaries 
or their respective close associates in relation to the acquisition, disposal, voting or other 
disposition of Shares registered in his/her/its name or otherwise held by him/her/it.

<<<PAGE 7>>>
– 7 –
Cornerstone Investors
Name Note 1
No. of 
Offer Shares 
allocated
Approximate 
% of 
the Offer 
Shares Note 2
Approximate % 
of total issued 
share capital 
after the Global 
Offering Note 3
Existing 
shareholders 
or their close 
associates
HHLR Advisors, Ltd. (“HHLRA”)
1,156,650
11.02%
1.05%
No
Yuanbao Family Office Limited  
(“Yuanbao Family Office (元寶家辦)”)
1,156,650
11.02%
1.05%
No
3W Fund Management Limited (“3W Fund”)
771,100
7.35%
0.70%
No
GF Fund Management Co., Ltd.  
(廣發基金管理有限公司) (“GF Fund Management”)  
and GF International Investment Management Limited  
(廣發國際資產管理有限公司) (“GF Fund HK”,  
together with GF Fund Management, “GF Fund”)
462,650
4.41%
0.42%
No
Ruihua (International) Investment Limited  
(瑞華(國際)投資有限公司) (“Ruihua Investment”)
385,550
3.67%
0.35%
No
Zhonghe Capital (through GF Securities Asset Management 
(Guangdong) Co., Ltd (“GF Securities AM”) as the 
qualified domestic institutional investor)3
231,300
2.20%
0.21%
No
Yishao Capital Management (HK) Limited  
(“Yishao Capital”)
231,300
2.20%
0.21%
No
Nova Kerry Inc.
154,200
1.47%
0.14%
No
Subtotal
4,549,400
43.34%
4.12%
Notes:
1.	
For further details of the cornerstone investors, please refer to the section headed “Cornerstone Investors” of the Prospectus.
2.	
Assuming the Over-allotment Option is not exercised.
3.	
Splendid Zhonghe (Tianjin) Investment Management Co., Ltd. (錦繡中和(天津)投資管理有限公司) (“Splendid Zhonghe Investment”) has entered into Cornerstone 
Investment Agreement with the Company. Splendid Zhonghe Investment is a limited liability company incorporated in China on January 17, 2017. It is a wholly-owned 
subsidiary of Splendid Zhonghe (Beijing) Capital Co., Ltd. (錦繡中和(北京)資本管理有限公司) (“Zhonghe Capital”). Since the date of the prospectus, Zhonghe 
Capital has finalized its subscription arrangements. Splendid Zhonghe Investment has engaged GF Securities AM, an asset manager that is a qualified domestic 
institutional investor as approved by the relevant PRC authority, to subscribe for and hold such Offer Shares on a non-discretionary basis on behalf of Zhonghe 
Capital, in the name of: (1) CIB-GFAM CHINA HK STOCKS MULTISTRATEGY AMA NO.7 (廣發資管港股多元策略7號單一資產管理計劃(QDII))) and (ii) SPDB 
— GF SECURITIES ASSET MANAGEMENT (GUANGDONG) CO.,LTD. CHKMS AMA NO.12 (廣發資管港股多元策略12號單一資產管理計劃 (QDII)).

<<<PAGE 8>>>
– 8 –
Allottees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares Note 1
% of total 
issued 
H-shares after 
the Global 
Offering upon 
listing Note 1
% of 
shareholding 
in the 
Company upon 
listing Note 1
Relationship
Allottees with consent under paragraph 1C(1) of the Appendix F1 to the Listing Rules (the “Placing Guidelines”) and Chapter 4.15 of the Guide for 
New Listing Applicants in relation to allocations to connected clients
CICC Financial Trading Limited (“CICC FT”) 
(in connection with Hangzhou Zheshi OTC 
Swaps)
430,700
4.10%
0.39%
0.39%
Connected client
CICC FT (in connection with Aochuang 
Hangzhou OTC Swaps)
501,200
4.77%
0.45%
0.45%
Connected client
CICC FT (in connection with Tibet Longrising 
OTC Swaps)
3,700
0.04%
0.0033%
0.0033%
Connected client
CICC FT (in connection with Shanghai Tongyi 
OTC Swaps)
400
0.0038%
0.0036%
0.0036%
Connected client
China Asset Management (Hong Kong) Limited 
(“China AM”)
1,600
0.02%
0.0014%
0.0014%
Connected client
China Universal Asset Management (Hong Kong) 
Company Limited (“China UAM”)
7,700
0.07%
0.01%
0.01%
Connected client
Fullgoal Asset Management (HK) Limited 
(“Fullgoal AMHK”)
270,450
2.58%
0.24%
0.24%
Connected client
Fullgoal Fund Management Company Limited 
(“Fullgoal Fund”)
115,100
1.10%
0.10%
0.10%
Connected client
Notes:
1.	
Assuming the Over-allotment Option is not exercised.
2.	
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in 
relation to allocations to connected clients, please refer to the section headed “Allottees with waivers/consents obtained — International 
Offering — Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations to connected clients” of this announcement.

<<<PAGE 9>>>
– 9 –
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
listing
% of total issued 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
listing Note 1
Last day subject 
to the lock-up 
undertakings Note 2
Mr. Zhao Yue (“Mr. Zhao”)
17,050,617
15.43%
June 24, 2027
Shanghai Xianyi Enterprise Management Partnership 
(Limited Partnership) (上海仙一企業管理合夥企業(有限
合夥)) (“ Shanghai Xianyi”)
15,461,117
13.99%
June 24, 2027
Shanghai Xiansan Enterprise Management Partnership 
(Limited Partnership) (上海仙三企業管理合夥企業(有限
合夥)) (“Shanghai Xiansan”)
7,960,265
7.20%
June 24, 2027
Shanghai Xianwu Enterprise Management Partnership 
(Limited Partnership) (上海仙五企業管理合夥企業(有限
合夥)) (“Shanghai Xianwu”)
4,823,140
4.36%
June 24, 2027
Shanghai Xianliu Enterprise Management Partnership 
(Limited Partnership) (上海仙六企業管理合夥企業(有限
合夥)) (“Shanghai Xianliu”)
3,324,871
3.01%
June 24, 2027
Shanghai Xianqi Enterprise Management Partnership 
(Limited Partnership) (上海仙七企業管理合夥企業(有限
合夥)) (“Shanghai Xianqi”)
4,265,688
3.86%
June 24, 2027
Subtotal
52,885,698
47.86%
Notes:
1.	
Assuming the Over-allotment Option is not exercised.
2.	
The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws and relevant lock-up undertakings as 
disclosed in the Prospectus.

<<<PAGE 10>>>
– 10 –
Key Persons (as defined under Rule 18C.14 of the Listing Rules)
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon listing
% of total issued 
Shares after the 
Global Offering 
subject to lock-
up undertakings 
upon listing Note 1
Last day subject 
to the lock-up 
undertakings 
Note 2
Mr. Zhao
17,050,617
15.43%
June 24, 2027
Shanghai Xianyi
15,461,117
13.99%
June 24, 2027
Shanghai Xiansan
7,960,265
7.20%
June 24, 2027
Shanghai Xianwu
4,823,140
4.36%
June 24, 2027
Shanghai Xianliu
3,324,871
3.01%
June 24, 2027
Shanghai Xianqi
4,265,688
3.86%
June 24, 2027
Subtotal
52,885,698
47.86%
Notes:
1.	
Assuming the Over-allotment Option is not exercised.
2.	
Each of such core R&D members of the Company and/or Directors has undertaken that the partnership interests held by 
him/her in these partnerships are subject to a lock-up period of 12 months after the Listing Date (the “Partnership Lock-up 
Period”) pursuant to Rule 18C.14 of the Listing Rules.
3.	
The Company determined the key personnel, namely Mr. Zhao, Mr. Wang Qun, Mr. Ye Yangsheng, Dr. Huang Qiangsheng and 
Dr. Zhang Tengyu, based on their roles and expertise in leading the development of our core technologies in relation to the 
Specialist Technology Products and their seniority within the R&D department of the Company. These key personnel play 
critical roles in driving the Company’s product innovation and overall business development. Please refer to section headed 
“Business — Research and Development — R&D Team and Core Members” in the Prospectus for further details of their 
biographies. The key personnel directly or indirectly hold the Shares through Shanghai Xianyi, Shanghai Xiansan, Shanghai 
Xianwu, Shanghai Xianliu, Shanghai Xianqi, Suzhou Xianwu No. 1 and Suzhou Xianwu No. 2, and all the respective ultimate 
beneficial interests in these platforms held by the key personnel shall be subject to disposal restrictions pursuant to Rules 
18C.14 of the Listing Rules at the time of the Listing.

<<<PAGE 11>>>
– 11 –
Pathfinder SIIs
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon listing
% of total issued 
Shares after the 
Global Offering 
subject to lock-
up undertakings 
upon listing Note 1
Last day subject 
to the lock-up 
undertakings 
Note 2
Zhuhai Yinshan Modern Logistics Industry Equity 
Investment Fund (Limited Partnership) (珠海
隱山現代物流產業股權投資基金(有限合夥)) 
(“Zhuhai Yinshan”)
14,249,432
12.90%
June 24, 2027
Ecovacs (Hainan) Investment Co., Ltd. (科沃斯
(海南)投資有限公司) (“Ecovacs Investment 
Hainan”)
6,446,709
5.83%
June 24, 2027
Nanjing SAIF Equity Investment Fund (L.P.) (南京
賽富股權投資基金(有限合夥)) (“Nanjing SAIF”)
2,327,951
2.11%
June 24, 2027
Hangzhou Fuyang SAIF Yi’an Equity Investment 
Partnership (Limited Partnership) (杭州富陽賽
富億安股權投資合夥企業(有限合夥)) (“SAIF 
Yi’an”)
1,306,751
1.18%
June 24, 2027
Nanjing SAIF Yulin Equity Investment Partnership 
Enterprise (Limited Partnership) (南京賽富雨林股
權投資合夥企業(有限合夥)) (“SAIF Yulin”)
390,078
0.35%
June 24, 2027
Jiaxing Tengyuan Investment Partnership (Limited 
Partnership) (嘉興騰元投資合夥企業(有限合夥)) 
(“Jiaxing Tengyuan”)
234,042
0.21%
June 24, 2027
Subtotal
24,954,963
22.58%
Notes:
1.	
Each of the Shareholders listed in the above table is a pathfinder SII of the Company as defined under Chapter 2.5 of the 
Guide for New Listing Applicants. Please refer to the section headed “History, Development and Corporate Structure — 
Capitalization of the Company” in the Prospectus for further details.
2.	
All Pathfinder SIIs shall not dispose of any of the Shares held by them within the 12 months following the Listing Date as 
required under the applicable PRC laws and relevant lock-up undertakings as disclosed in the Prospectus. In accordance 
with Rule 18C.14(2) of the Listing Rules, the required lock-up period commences on the date by reference to which disclosure 
of its shareholding is made in the Prospectus and ends on the date which is six months from the Listing Date. In addition to 
the lock-up requirement under Rule 18C.14(2) of the Listing Rules, all existing Shareholders shall not dispose of any of the 
Shares held by them within the 12 months following the Listing Date, i.e. June 24, 2026, as required under the applicable 
PRC laws.

<<<PAGE 12>>>
– 12 –
Other Pre-IPO Investors
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon listing
% of total issued 
Shares after the 
Global Offering 
subject to lock-
up undertakings 
upon listing Note 1
Last day subject 
to the lock-up 
undertakings 
Note 2
Ningbo Meishan Bonded Port Area Huilidaoqin 
Investment Management Center (Limited 
Partnership) (寧波梅山保稅港區匯利道勤投資管
理中心(有限合夥)) (“Ningbo Huilidaoqin”)
9,654,483
8.74%
June 24, 2027
Tianjin Dehui Investment Management Partnership 
(Limited Partnership) (天津德輝投資管理合夥企
業(有限合夥)) (“Tianjin Dehui”)
5,349,599
4.84%
June 24, 2027
Hangzhou Yuanqiao Zhixing Venture Capital 
Partnership Enterprise (Limited Partnership) (杭
州遠橋智行創業投資合夥企業(有限合夥)) 
(“Hangzhou Yuanqiao”)
4,455,980
4.03%
June 24, 2027
Hangzhou Xiaoshan Haolan Equity Investment 
Fund Partnership Enterprise (Limited Partnership) 
杭州蕭山浩瀾股權投資基金合夥企業(有限合夥) 
(“Hangzhou Haolan”)
1,170,225
1.06%
June 24, 2027
Wuxi Liangxi Science and Technology City 
Hongtai Xinzhi Investment Partnership Enterprise 
(Limited Partnership) (無錫市梁溪科技城洪
泰新智投資合夥企業(有限合夥)) (“Hongtai 
Investment”)
1,529,052 
1.38%
June 24, 2027
Subtotal
22,159,339
20.05%
Notes:
1.	
Assuming the Over-allotment Option is not exercised.
2.	
The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws.

<<<PAGE 13>>>
– 13 –
Cornerstone Investors
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon listing
% of total issued 
Shares after the 
Global Offering 
subject to lock-
up undertakings 
upon listing Note 1
Last day subject 
to the lock-up 
undertakings 
Note 2
HHLRA
1,156,650
1.05%
December 24, 2026
Yuanbao Family Office (元寶家辦)
1,156,650
1.05%
December 24, 2026
3W Fund
771,100
0.70%
December 24, 2026
GF Fund
462,650
0.42%
December 24, 2026
Ruihua Investment
385,550
0.35%
December 24, 2026
Zhonghe Capital (through GF Securities AM as the 
qualified domestic institutional investor)
231,300
0.21%
December 24, 2026
Yishao Capital
231,300
0.21%
December 24, 2026
Nova Kerry Inc.
154,200
0.14%
December 24, 2026
Subtotal
4,549,400
4.12%
Notes:
1.	
Assuming the Over-allotment Option is not exercised.
2.	
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on December 24, 2026. The 
Cornerstone Investors will cease to be prohibited from disposing of or transferring H Shares subscribed for pursuant to the 
relevant cornerstone investment agreements after the indicated date.

<<<PAGE 14>>>
– 14 –
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of H 
Shares allotted
Allotment as % 
of International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as % 
of International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised)
Allotment as 
% of total 
Offer Shares 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over-allotment 
Option is fully 
exercised)
Number of 
Shares held 
upon Listing
% of total issued 
share capital 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised)
Top 1
1,156,650
13.7733
11.5986
11.0185
9.5814
1,156,650
1.0468
1.0321
Top 5
4,124,250
49.1112
41.3569
39.2886
34.1642
4,124,250
3.7325
3.68
Top 10
6,129,100
67.0166
56.4351
53.6125
46.6201
6,129,100
5.0932
5.0216
Top 25
9,136,350
102.8265
86.591
82.2603
71.5313
9,136,350
7.8151
7.7049
Note
*	
Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 15>>>
– 15 –
H SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
Allotment as 
% of total 
Offer Shares 
(assuming 
no exercise 
of the Over-
allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
Number of 
H Shares 
held upon 
Listing
% of total 
issued Share 
capital upon 
Listing 
(assuming 
no exercise 
of the Over-
allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option 
is fully 
exercised)
Top 1
0
N/A
N/A
0.0000
0.0000
17,050,617
15.4308
15.2140
Top 5
0
N/A
N/A
0.0000
0.0000
64,375,914
58.2601
57.4416
Top 10
0
N/A
N/A
0.0000
0.0000
89,717,030
81.1938
80.0531
Top 25
6,399,550
76.2053
64.1730
60.9635
53.0123
106,399,550
94.9385
94.0412
Note
*	
Ranking of H Shareholders is based on the number of H Shares (of all classes) held by the H 
Shareholders upon Listing.

<<<PAGE 16>>>
– 16 –
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 38,687 valid 
applications made by the public will be conditionally allocated on the basis set out below:
NO. OF 
H SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOCATION/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTED OF 
THE TOTAL NO. 
OF H SHARES 
APPLIED FOR
POOL A
50
70,566
3,528 out of 70,566 to receive 50 Shares
5.00%
100
10,449
627 out of 10,449 to receive 50 Shares
3.00%
150
5,530
373 out of 5,530 to receive 50 Shares
2.25%
200
4,371
314 out of 4,371 to receive 50 Shares
1.80%
250
3,763
287 out of 3,763 to receive 50 Shares
1.53%
300
3,298
264 out of 3,298 to receive 50 Shares
1.33%
350
3,045
254 out of 3,045 to receive 50 Shares
1.19%
400
2,617
226 out of 2,617 to receive 50 Shares
1.08%
450
14,742
1,312 out of 14,742 to receive 50 Shares
0.99%
500
7,310
669 out of 7,310 to receive 50 Shares
0.92%
600
3,410
327 out of 3,410 to receive 50 Shares
0.80%
700
2,370
237 out of 2,370 to receive 50 Shares
0.71%
800
1,765
183 out of 1,765 to receive 50 Shares
0.65%
900
3,854
411 out of 3,854 to receive 50 Shares
0.59%
1,000
6,394
701 out of 6,394 to receive 50 Shares
0.55%
1,500
4,303
525 out of 4,303 to receive 50 Shares
0.41%
2,000
3,327
438 out of 3,327 to receive 50 Shares
0.33%
2,500
2,527
352 out of 2,527 to receive 50 Shares
0.28%
3,000
2,395
350 out of 2,395 to receive 50 Shares
0.24%
3,500
1,832
279 out of 1,832 to receive 50 Shares
0.22%
4,000
1,780
281 out of 1,780 to receive 50 Shares
0.20%
4,500
1,450
236 out of 1,450 to receive 50 Shares
0.18%
5,000
3,436
575 out of 3,436 to receive 50 Shares
0.17%
6,000
2,496
438 out of 2,496 to receive 50 Shares
0.15%
7,000
3,053
558 out of 3,053 to receive 50 Shares
0.13%
8,000
1,672
316 out of 1,672 to receive 50 Shares
0.12%
9,000
1,424
278 out of 1,424 to receive 50 Shares
0.11%
10,000
8,958
1,797 out of 8,958 to receive 50 Shares
0.10%
20,000
6,846
1,648 out of 6,846 to receive 50 Shares
0.06%
30,000
4,268
1,143 out of 4,268 to receive 50 Shares
0.04%
40,000
7,179
2,068 out of 7,179 to receive 50 Shares
0.04%
 
Total
200,430
Total number of Pool A successful applicants: 20,995
 

<<<PAGE 17>>>
– 17 –
NO. OF 
H SHARES 
APPLIED FOR
NO. OF VALID 
APPLICATIONS
BASIS OF ALLOCATION/BALLOT
APPROXIMATE 
PERCENTAGE 
ALLOTED OF 
THE TOTAL NO. 
OF H SHARES 
APPLIED FOR
POOL B
50,000
7,560
4,443 out of 7,560 to receive 50 Shares
0.06%
60,000
2,376
1,583 out of 2,376 to receive 50 Shares
0.06%
70,000
2,373
1,759 out of 2,373 to receive 50 Shares
0.05%
80,000
1,249
1,015 out of 1,249 to receive 50 Shares
0.05%
90,000
725
639 out of 725 to receive 50 Shares
0.05%
100,000
2,713
50 Shares
0.05%
150,000
1,599
50 Shares plus 406 out of 1,599 to receive additional 50 Shares
0.04%
200,000
1,376
50 Shares plus 729 out of 1,376 to receive additional 50 Shares
0.04%
262,450
2,565
50 Shares plus 2,168 out of 2,565 to receive additional 50 
Shares
0.04%
 
Total:
22,536
Total number of Pool B successful applicants: 17,692
 
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
subscribed for or purchased by them was the same as the final Offer Price in addition to any 
brokerage, AFRC transaction levy, SFC transaction levy and Stock Exchange trading fee 
payable.
The Directors and the Overall Coordinators confirm that at least 50% of the total number of 
the Offer Shares (excluding any Shares issued and/or to be issued pursuant to the exercise 
of any offer Size Adjustment Option and/or Over-allotment Option) have been allocated to 
and taken up by independent price setting investors in compliance with Rule 18C.08 of the 
Listing Rules.

<<<PAGE 18>>>
– 18 –
The Directors further confirm that at least 20% of the issued share capital of the Company 
will be held by sophisticated independent investors at the time of Listing in compliance with 
Chapter 2.5 of the Guide for New Listing Applicants.
OTHERS/ADDITIONAL INFORMATION
Reallocation
As (i) the Hong Kong Public Offering is oversubscribed by more than 50 times and (ii) the 
reallocation pursuant to Paragraph 4.2 of Practice Note 18 of the Listing Rules (as modified 
by Rule 18C.09 of the Listing Rules) as described in the section headed “Structure of the 
Global Offering — The Hong Kong Public Offering — Reallocation” of the Prospectus 
is exercised, the clawback arrangement is triggered and Offer Shares were reallocated to 
the Hong Kong Public Offering from the International Offering, so that the total number 
of Offer Shares available under the Hong Kong Public Offering is 2,099,500 Offer Shares, 
representing 20% of the Offer Shares initially available under the Global Offering.
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of 
their connected distributors pursuant to the Placing Guidelines. Please refer to the section 
headed “Allotment Results Details — International Offering — Allottees with Waivers/
Consents Obtained” in this announcement for details. The Company has applied to the Stock 
Exchange for, and the Stock Exchange has granted, a consent under paragraph 1C(1) of the 
Placing Guidelines to permit the Company to allocate such Offer Shares in the International 
Offering to the connected clients. The allocation of Offer Shares to such connected clients 
is in compliance with all the conditions under the consent granted by the Stock Exchange. 
Details of the placement to connected clients are set out below.

<<<PAGE 19>>>
– 19 –
No.
Connected 
distributor
Connected client
Relationship with 
the connected 
distributor
Whether the 
connected 
clients will hold 
the beneficial 
interests of the 
Offer Shares on a 
non-discretionary 
basis or 
discretionary 
basis for 
independent third 
parties
Whether the 
connected client 
is a collective 
investment 
scheme which is 
not authorised 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme
Number of 
Offer Shares 
allocated to 
the connected 
client
Approximate 
percentage of 
total number of
 Offer Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
percentage of 
total Shares 
in issue 
immediately 
following the 
completion of 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
1.
China International 
Capital 
Corporation 
Hong Kong 
Securities 
Limited 
(“CICCHKS”)
CICC FT  
(in connection 
with Hangzhou 
Zheshi OTC 
Swaps)
1
CICC FT is a 
member of the 
same group of 
CICCHKS
Non-discretionary 
basis
No
430,700
4.10%
0.39%
CICC FT (in 
connection 
with Aochuang 
Hangzhou OTC 
Swaps)
2
CICC FT is a 
member of the 
same group of 
CICCHKS
Non-discretionary 
basis
No
501,200
4.77%
0.45%
CICC FT (in 
connection with 
Tibet Longrising 
OTC Swaps)
3
CICC FT is a 
member of the 
same group of 
CICCHKS
Non-discretionary 
basis
No
3,700
0.04%
0.0033%
CICC FT (in 
connection with 
Shanghai Tongyi 
OTC Swaps)
4
CICC FT is a 
member of the 
same group of 
CICCHKS
Non-discretionary 
basis
No
400
0.0038%
0.0036%
 
 
 
Sub Total
936,000
8.92%
0.85%
 
 
 

<<<PAGE 20>>>
– 20 –
No.
Connected 
distributor
Connected client
Relationship with 
the connected 
distributor
Whether the 
connected 
clients will hold 
the beneficial 
interests of the 
Offer Shares on a 
non-discretionary 
basis or 
discretionary 
basis for 
independent third 
parties
Whether the 
connected client 
is a collective 
investment 
scheme which is 
not authorised 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme
Number of 
Offer Shares 
allocated to 
the connected 
client
Approximate 
percentage of 
total number of
 Offer Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
percentage of 
total Shares 
in issue 
immediately 
following the 
completion of 
Global Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
1.
CITIC Securities 
Brokerage (HK) 
Limited (“CSB”)
China Asset 
Management 
(Hong Kong) 
Limited  
(“China AM”)
China AM is a 
member of the 
same group of 
companies as 
CSB
Discretionary basis No
1,600
0.02%
0.0014%
2.
Orient Securities 
(Hong Kong) 
Limited 
(“Orient”)
China Universal 
Asset 
Management 
(Hong Kong) 
Company 
Limited (“China 
UAM”)
China UAM is a 
member of the 
same group of 
companies as 
Orient
Discretionary basis No
7,700
0.07%
0.01%
3.
Haitong 
International 
Securities 
Company 
Limited (“HTI”)
Fullgoal Asset 
Management 
(HK) Limited 
(“Fullgoal 
AMHK”)
Fullgoal AMHK is 
a member of the 
same group of 
the companies 
as HTI
Discretionary basis No
270,450
2.58%
0.24%
Fullgoal Fund 
Management 
Company 
Limited 
(“Fullgoal 
Fund”)
Fullgoal Fund is a 
member of the 
same group of 
the companies 
as HTI
Discretionary basis No
115,100
1.10%
0.10%
Sub Total
394,850
3.76%
0.36%
 
 
 
Total
1,330,850
12.68%
1.20%
 
 
 

<<<PAGE 21>>>
– 21 –
Notes:
1.	
CICC Financial Trading Limited (“CICC FT”) is a wholly-owned subsidiary of China International 
Capital Corporation Limited, of which its shares are listed on the Shanghai Stock Exchange (stock 
code: 601995) and the Stock Exchange (stock code: 3908). CICC FT and China International 
Capital Corporation Limited will enter into a series of cross border delta-one OTC swap transactions 
(collectively, the “Hangzhou Zheshi OTC Swaps”) with each other and the ultimate clients (the “CICC 
FT Ultimate Clients (Hangzhou Zheshi)”), pursuant to which CICC FT will hold the Offer Shares 
on a non-discretionary basis to hedge the Hangzhou Zheshi OTC Swaps while the economic risks and 
returns of the underlying Offer Shares are passed to the CICC FT Ultimate Clients (Hangzhou Zheshi), 
subject to customary fees and commissions. The Hangzhou Zheshi OTC Swaps will be fully funded 
by the CICC FT Ultimate Clients (Hangzhou Zheshi). During the terms of the Hangzhou Zheshi OTC 
Swaps, all economic returns of the Offer Shares subscribed by CICC FT will be passed to the CICC 
FT Ultimate Clients (Hangzhou Zheshi) and all economic loss shall be borne by the CICC FT Ultimate 
Clients (Hangzhou Zheshi) through the Hangzhou Zheshi OTC Swaps, and CICC FT will not take part 
in any economic return or bear any economic loss in relation to the Offer Shares.
	
The Hangzhou Zheshi OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate Clients 
(Hangzhou Zheshi) may request CICC FT to redeem it at their own discretions, upon which CICC FT 
may dispose of the Offer Shares and settle the Hangzhou Zheshi OTC Swaps in cash in accordance 
with the terms and conditions of the OTC Swaps. Despite that CICC FT will hold the legal title of the 
Offer Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares during 
the terms of the Hangzhou Zheshi OTC Swaps according to its internal policy. The CICC FT Ultimate 
Clients (Hangzhou Zheshi) for purpose of this placee subscription comprise ZheShi Quanying Private 
Securities Investment Fund (哲石泉盈私募證券投資基金) (“Zheshi Quanying”) and ZheShi Puzhuo 
No. 1 Private Securities Investment Fund (哲石普卓壹號私募證券投資基金) (“ZheShi Puzhuo”), 
both of which are managed by Hangzhou Zheshi Private Fund Management Co., Ltd. (杭州哲石私募
基金管理有限公司) (“Hangzhou Zheshi”), in which Zhu Yin (朱寅), its legal representative, holds 
30.5% equity interest. Save for Huang Lu (黄露) (in respect of Zheshi Quanying) and Weng Jinjing 
(翁妗璟) (in respect of ZheShi Puzhuo), no investor holds 30% or more interest in either Zheshi 
Quanying or ZheShi Puzhuo. To the best knowledge of Hangzhou Zheshi after due enquiry, each of 
Zheshi Quanying, ZheShi Puzhuo, Hangzhou Zheshi and their respective ultimate beneficial owners is 
an independent third party of the Group, CICC FT, CICCHKS and the companies which are members 
of the same group of companies as each of the Underwriters.
2.	
CICC FT and China International Capital Corporation Limited will enter into a series of cross border 
delta-one OTC swap transactions (collectively, the “Aochuang Hangzhou OTC Swaps”) with each 
other and the ultimate client (the “CICC FT Ultimate Client (Aochuang Hangzhou)”), pursuant 
to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the Aochuang 
Hangzhou OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed 
to the CICC FT Ultimate Client (Aochuang Hangzhou), subject to customary fees and commissions. 
The Aochuang Hangzhou OTC Swaps will be fully funded by the CICC FT Ultimate Client (Aochuang 
Hangzhou). During the terms of the Aochuang Hangzhou OTC Swaps, all economic returns of the 
Offer Shares subscribed by CICC FT will be passed to the CICC FT Ultimate Client (Aochuang 
Hangzhou) and all economic loss shall be borne by the CICC FT Ultimate Client (Aochuang 
Hangzhou) through the Aochuang Hangzhou OTC Swaps, and CICC FT will not take part in any 
economic return or bear any economic loss in relation to the Offer Shares.

<<<PAGE 22>>>
– 22 –
	
The Aochuang Hangzhou OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate 
Client (Aochuang Hangzhou) may request CICC FT to redeem it at their own discretions, upon which 
CICC FT may dispose of the Offer Shares and settle the Aochuang Hangzhou OTC Swaps in cash in 
accordance with the terms and conditions of the OTC Swaps. Despite that CICC FT will hold the legal 
title of the Offer Shares by itself, it will not exercise the voting rights attaching to the relevant Offer 
Shares during the terms of the Aochuang Hangzhou OTC Swaps according to its internal policy. The 
CICC FT Ultimate Client (Aochuang Hangzhou) for purpose of this placee subscription comprises 
Aochuang Jinchentaihe No. 1 Private Securities Investment Fund (傲創金宸泰和1號私募證券投資基
金) (“Aochuang No.1”) which is managed by Aochuang (Hangzhou) Asset Management Co., Ltd. (傲
創(杭州)資產管理有限公司) (“Aochuang Hangzhou”). No investor holds 30% or more interest in 
Aochuang No.1. Aochuang Hangzhou is wholly owned by Chen Lingxi (陳泠希). To the best knowledge 
of Aochuang Hangzhou after due enquiry, each of Aochuang No.1, Aochuang Hangzhou and their 
respective ultimate beneficial owners is an independent third party of the Group, CICC FT, CICCHKS 
and the companies which are members of the same group of companies as each of the Underwriters.
3.	
CICC Financial Trading Limited (“CICC FT”) and China International Capital Corporation Limited 
will enter into a series of cross border delta-one OTC swap transactions (collectively, the “Tibet 
Longrising OTC Swaps”) with each other and the ultimate clients (the “CICC FT Ultimate Clients 
(Tibet Longrising)”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary 
basis to hedge the Tibet Longrising OTC Swaps while the economic risks and returns of the underlying 
Offer Shares are passed to the CICC FT Ultimate Clients (Tibet Longrising), subject to customary fees 
and commissions. The Tibet Longrising OTC Swaps will be fully funded by the CICC FT Ultimate 
Clients (Tibet Longrising). During the terms of the Tibet Longrising OTC Swaps, all economic returns 
of the Offer Shares subscribed by CICC FT will be passed to the CICC FT Ultimate Clients (Tibet 
Longrising) and all economic loss shall be borne by the CICC FT Ultimate Clients (Tibet Longrising) 
through the Tibet Longrising OTC Swaps, and CICC FT will not take part in any economic return or 
bear any economic loss in relation to the Offer Shares.
	
The Tibet Longrising OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate Clients 
(Tibet Longrising) may request CICC FT to redeem it at their own discretions, upon which CICC FT 
may dispose of the Offer Shares and settle the Tibet Longrising OTC Swaps in cash in accordance 
with the terms and conditions of the OTC Swaps. Despite that CICC FT will hold the legal title of 
the Offer Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares 
during the terms of the Tibet Longrising OTC Swaps according to its internal policy. The CICC FT 
Ultimate Clients (Tibet Longrising) for purpose of this placee subscription comprise Longrising 
Qiangshu Private Securities Investment Fund (源樂晟強樹私募證券投資基金) (“Longrising 
Qiangshu”), Longrising Qiangye Private Securities Investment Fund (源樂晟強業私募證券投資
基金) (“Longrising Qiangye”), Longrising Qiangshi Private Securities Investment Fund (源樂晟
強勢私募證券投資基金) (“Longrising Qiangshi”), all of which are managed by Tibet Longrising 
Asset Management Co., Ltd. (西藏源樂晟資產管理有限公司) (“Tibet Longrising”), in which Zeng 
Xiaojie (曾曉潔), its legal representative, holds 61.75% equity interest. Save for (i) Zeng Xiaojie who 
holds 30% or more interest in each of Longrising Qiangshu and Longrising Qiangshi, and (ii) Zeng 
Xiaojie and Hu Caiyang (胡彩陽), who each hold 30% or more interest in Longrising Qiangye, no 
investor holds 30% or more interest in the above entities. To the best knowledge of Tibet Longrising 
after due enquiry, each of Longrising Qiangshu, Longrising Qiangye, Longrising Qiangshi, Tibet 
Longrising and their respective ultimate beneficial owners is an independent third party of the Group, 
CICC FT, CICCHKS and the companies which are members of the same group of companies as each 
of the Underwriters.

<<<PAGE 23>>>
– 23 –
4.	
CICC Financial Trading Limited (“CICC FT”) and China International Capital Corporation Limited 
will enter into a series of cross border delta-one OTC swap transactions (collectively, the “Shanghai 
Tongyi OTC Swaps”) with each other and the ultimate clients (the “CICC FT Ultimate Clients 
(Shanghai Tongyi)”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary 
basis to hedge the Shanghai Tongyi OTC Swaps while the economic risks and returns of the underlying 
Offer Shares are passed to the CICC FT Ultimate Clients (Shanghai Tongyi), subject to customary fees 
and commissions. The Shanghai Tongyi OTC Swaps will be fully funded by the CICC FT Ultimate 
Clients (Shanghai Tongyi). During the terms of the Shanghai Tongyi OTC Swaps, all economic returns 
of the Offer Shares subscribed by CICC FT will be passed to the CICC FT Ultimate Clients (Shanghai 
Tongyi) and all economic loss shall be borne by the CICC FT Ultimate Clients (Shanghai Tongyi) 
through the Shanghai Tongyi OTC Swaps, and CICC FT will not take part in any economic return or 
bear any economic loss in relation to the Offer Shares.
	
The Shanghai Tongyi OTC Swaps are linked to the Offer Shares and the CICC FT Ultimate Clients 
(Shanghai Tongyi) may request CICC FT to redeem it at their own discretions, upon which CICC FT 
may dispose of the Offer Shares and settle the Shanghai Tongyi OTC Swaps in cash in accordance 
with the terms and conditions of the OTC Swaps. Despite that CICC FT will hold the legal title of the 
Offer Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares during 
the terms of the Shanghai Tongyi OTC Swaps according to its internal policy. The CICC FT Ultimate 
Clients (Shanghai Tongyi) for purpose of this placee subscription comprise Tongyi Taoli No.10 
Private Securities Investment Fund (通怡桃李10號私募證券投資基金) (“Tongyi Taoli No.10”), 
Tongyi Global Value No.5 Private Securities Investment Fund (通怡全球價值5號私募證券投資基
金) (“Tongyi Global Value No.5”) and Tongyi Active Equity Enhancement No.9 Private Securities 
Investment Fund (通怡主動股基增強9號私募證券投資基金) (“Tongyi Active No.9”), all of which 
are managed by Shanghai Tongyi Investment Management Co., Ltd. (上海通怡投資管理有限公
司) (“Shanghai Tongyi”) in which Chu Yibo (儲貽波), its legal representative, holds 40.48% equity 
interest. No investor holds 30% or more interest in Tongyi Taoli No.10, Tongyi Global Value No.5 and 
Tongyi Active No.9. To the best knowledge of Shanghai Tongyi after due enquiry, each of Tongyi Taoli 
No.10, Tongyi Global Value No.5, Tongyi Active No.9, Shanghai Tongyi and their respective ultimate 
beneficial owners is an independent third party of the Group, CICC FT, CICCHKS and the companies 
which are members of the same group of companies as each of the Underwriters.
5.	
China AM is a member of the same group of companies as CSB. To the best of its knowledge after due 
enquiry, each of its underlying clients and their respective ultimate beneficial owners is an independent 
third party of China AM, CSB and their respective group companies. China AM will hold the Offer 
Shares in its capacity as discretionary investment manager on behalf of such underlying clients, details 
of which are set out below:
(i)	
CHINAAMC SELECT GREATER CHINA TECHNOLOGY FUND — Save for Futu Securities 
International (Hong Kong) Limited-client account, no other ultimate beneficial owner holds 
more than 30% of interest therein. Futu Securities International (Hong Kong) Limited is a 
member of the underwriting syndicates, acts solely as a placing broker for its underlying 
clients on a non-discretionary basis and does not take any proprietary position in respect such 
subscription.
(ii)	
CHINAAMC FUND — CHINAAMC CHINA OPPORTUNITIES FUND — No investor holds 
30% or more interest therein.
(iii)	
CHINAAMC CHINA FOCUS FUND — Save for Manulife (International) Limited, no other 
ultimate beneficial owner holds more than 30% of interest therein.
(iv)	
CHINAAMC CHINA GROWTH FUND (SICAV) — Save for Yuanta Securities (HK) Company 
LTD, no other ultimate beneficial owner holds more than 30% of interest therein.

<<<PAGE 24>>>
– 24 –
6.	
China UAM is a member of the same group of companies as Orient. To the best of its knowledge 
after due enquiry, each of its underlying clients and their respective ultimate beneficial owners is an 
independent third party of China UAM, Orient and their respective group companies. China UAM will 
hold the Offer Shares in its capacity as discretionary investment manager on behalf of such underlying 
clients, details of which are set out below:
(i)	
China Universal Special Situation Fund SPC — CUAM Flexible Strategy Fund SP — No 
investor holds 30% or more interest therein.
(ii)	
China Universal Asset Management (Hong Kong) Company Limited — CLIENT’S A/C 
BETTER SUPPLY CHAIN (HK) HOLDINGS CO., LIMITED — Save for Peng Zimei, no 
other ultimate beneficial owner holds more than 30% of interest therein.
(iii)	
China Universal Asset Management (Hong Kong) Company Limited — CLIENT A/C 
EXCELLENT TIDE SECURITIES LIMITED — EXCELLENT TIDE EURASIA OFC — 
EXCELLENT TIDE EURASIA NO.1 FUND — Save for Hua Zhongjie and Zhang Ping, no 
other ultimate beneficial owner holds more than 30% of interest therein.
(iv)	
CHINA UNIVERSAL ASSET MANAGEMENT (HONG KONG) COMPANY LIMITED 
— CLIENT’S A/C LC LOGISTICS, INC — Save for Xu Xin and Li Yan, no other ultimate 
beneficial owner holds more than 30% of interest therein.
(v)	
CUAM China-Hong Kong Strategy Fund is a SFC authorized fund (CE no.: AZW731) — No 
investor holds 30% or more interest therein.

<<<PAGE 25>>>
– 25 –
7.	
Fullgoal AMHK is a member of the same group of companies as HTI. To the best of its knowledge 
after due enquiry, each of its underlying clients and their respective ultimate beneficial owners is 
an independent third party of Fullgoal AMHK, HTI and their respective group companies. Fullgoal 
AMHK will hold the Offer Shares in its capacity as discretionary investment manager on behalf of 
such underlying clients, details of which are set out below:
(i)	
Fullgoal Asset Management (HK) Limited SUB A/C HI-Aktien China 1-Sfonds — Save for 
A European pension fund, no other ultimate beneficial owner holds more than 30% of interest 
therein.
(ii)	
Fullgoal Hong Kong and China Equity Fund — Save for The University of Hong Kong, no other 
ultimate beneficial owner holds more than 30% of interest therein.
(iii)	
Fullgoal China Growth Select Fund — Save for Zhao Xueming, no other ultimate beneficial 
owner holds more than 30% of interest therein.
(iv)	
Fullgoal China Opportunities Fund — Save for China Everbright Fortune Investment Limited, 
L Industries Limited and Orient Sun Rise Fund Series SPC-Orient Sun Rise Enhanced Balanced 
Fund Segregated Portfolio, no other ultimate beneficial owner holds more than 30% of interest 
therein.
(v)	
Fullgoal China Small-Mid Cap Growth Fund is a SFC authorized fund (CE no.: BNY686) — 
No investor holds 30% or more interest therein.
(vi)	
BMO Greater China Fund — No investor holds 30% or more interest therein.
8.	
Fullgoal Fund is a member of the same group of companies as HTI. To the best of its knowledge after 
due enquiry, save as the internal funds from Fullgoal Fund in China Merchants Bank-Fullgoal Hong 
Kong Equity Select Hybrid Fund (QDII) (“Fullgoal HK Equity Select”), with the proprietary capital 
contribution not exceeding 0.05% of the total fund size of Fullgoal HK Equity Select, each of the 
other underlying clients and their respective ultimate beneficial owners is an independent third party of 
Fullgoal Fund, HTI and their respective group companies. Fullgoal Fund will hold the Offer Shares in 
its capacity as discretionary investment manager on behalf of the underlying clients includes Fullgoal 
HK Equity Select, CMB-Fullgoal Blue Chip Selected Equity Fund (QDII) and ICBC Fullgoal Global 
Technology & Internet Fund. To the best knowledge of Fullgoal Fund after due enquiry, no investor 
holds 30% or more interest in any of such underlying clients.

<<<PAGE 26>>>
– 26 –
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
(the “Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) 
take no responsibility for the contents of this announcement, make no representation as to 
its accuracy or completeness and expressly disclaim any liability whatsoever for any loss 
howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in 
or into the United States (including its territories and possessions, any state of the United 
States and the District of Columbia). This announcement does not constitute or form a part 
of any offer or solicitation to purchase or subscribe for securities in the United States. The 
securities mentioned herein have not been, and will not be, registered under the United 
States Securities Act of 1933, as amended (the “U.S. Securities Act”). The securities 
may not be offered or sold in the United States except pursuant to an exemption from the 
registration requirements of the U.S. Securities Act and in compliance with any applicable 
state securities laws, or outside the United States unless in compliance with Regulation S 
under the U.S. Securities Act. There will be no public offer of securities in the United States.
This announcement is for information purposes only and does not constitute an invitation 
or offer to acquire, purchase or subscribe for securities. This announcement is not a 
prospectus. Potential investors should read the Prospectus dated 15 June 2026 issued by 
Shanghai Seer Intelligent Technology Co., Ltd. for detailed information about the Global 
Offering described below before deciding whether or not to invest in the Shares thereby 
being offered.
*	
Potential investors of the Offer Shares should note that the Overall Coordinators (for themselves and 
on behalf of the Hong Kong Underwriters and Overall Coordinators) shall be entitled to terminate 
their obligations under the Hong Kong Underwriting Agreement with immediate effect upon the 
occurrence of any of the events set out in the paragraph headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Hong Kong Underwriting Agreement 
— Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the 
Listing Date.

<<<PAGE 27>>>
– 27 –
PUBLIC FLOAT
Pursuant to Rule 19A.13A(1) of the Listing Rules, assuming that the Over-allotment Option 
are not exercised, based on the Offer Price of HK$101.60 per Offer Share, our expected 
market capitalization upon the Listing is HK$11.23 billion, and the minimum prescribed 
public float percentage applicable to our Shares is 15.0%.
Immediately following the completion of the Global Offering (before any exercise of the 
Over-allotment Option) an aggregate of 43,362,170 H Shares, representing approximately 
39.24% of the issued share capital of our Company will count towards the public float. 
Therefore, the number of H Shares held in public hands is higher than the prescribed 
percentage of H Shares required to be held in public hands of 15% under Rule 19A.13A(1) 
of the Listing Rules.
Based on the final Offer Price of HK$101.60 per H Share, the Company satisfies the free 
float requirement under Rule 19A.13C of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering: 
(i) no placee will, individually, be placed more than 10% of the enlarged issued share capital 
of our Company; (ii) there will not be any new substantial Shareholder (as defined in the 
Listing Rules) of our Company; (iii) the three largest public shareholders of the Company 
do not hold more than 50% of the H Shares in public hands at the time of the Listing in 
compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 
300 Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing 
Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, 
June 24, 2026 (Hong Kong time), provided that the Global Offering has become 
unconditional and the right of termination described in the section headed “Underwriting 
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Hong 
Kong Underwriting Agreement — Grounds for Termination” in the Prospectus has not been 
exercised. Investors who trade the H Shares on the basis of publicly available allocation 
details prior to the receipt of H Share certificates or prior to the H Share certificates 
becoming valid evidence of title do so entirely at their own risk.

<<<PAGE 28>>>
– 28 –
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on 
Wednesday, June 24, 2026 (Hong Kong time), it is expected that dealings in the H Shares on 
the Stock Exchange will commence at 9:00 a.m. on Wednesday, June 24, 2026 (Hong Kong 
time). The H Shares will be traded in board lots of 50 H Shares each, and the stock code of 
the H Shares will be 06106.
By order of the Board
Shanghai Seer Intelligent Technology Co., Ltd.
Mr. Zhao Yue
Executive Director and Chairman of the Board
Hong Kong, June 23, 2026
Directors of the Company named in the application to which this announcement relates are: (i) Mr. Zhao Yue, 
Ms. Ding Xia, Mr. Ye Yangsheng and Mr. Wang Qun as executive directors, (ii) Dr. Cheng Lin, Dr. Liu Yong 
and Mr. Chen Fei as independent non-executive directors.
