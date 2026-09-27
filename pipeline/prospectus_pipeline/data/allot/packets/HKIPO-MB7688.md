# 配发结果公告抽取任务：7688.HK Shanghai Top Numerical Control Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**19/05/2026 21:54**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0519/2026051901261.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"7688.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the 
contents of this announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the 
contents of this announcement.
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same meanings 
as those defined in the prospectus dated 12 May 2026 (the “Prospectus”) issued by Shanghai Top Numerical 
Control Technology Co., Ltd. (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. Potential investors should read the Prospectus for detailed information 
about the Company and the Global Offering described below before deciding whether or not to invest in the 
Offer Shares.
This announcement is not for release, publication or distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for 
securities in the United States or in any other jurisdiction. The Offer Shares have not been and will not be 
registered under the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities 
Act”) or securities law of any state or other jurisdiction of the United States and may not be offered, sold, 
pledged or transferred within the United States, except in transactions exempt from, or not subject to, the 
registration requirements of the U.S. Securities Act. There will be no public offer of the Offer Shares in the 
United States. The Offer Shares are being offered and sold outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, Guotai Junan Securities (Hong Kong) Limited, as stabilising manager 
(the “Stabilising Manager”), its affiliates or any person acting for it and on behalf of the Underwriters, may 
effect transactions with a view to stabilising or supporting the market price of the Shares at a level higher than 
that which might otherwise prevail for a limited period after the Listing Date. However, there is no obligation on 
the Stabilising Manager, its affiliates or any person acting for it, to conduct any such stabilising action, which, 
if commenced, will be done at the sole and absolute discretion of the Stabilising Manager, its affiliates or any 
person acting for it, and may be discontinued at any time. Any such stabilising activity is required to be brought 
to an end on the 30th day after the last day for the lodging of applications under the Hong Kong Public Offering. 
Such stabilisation action, if commenced, may be effected in all jurisdictions where it is permissible to do so, in 
each case in compliance with all applicable laws, rules and regulatory requirements, including the Securities 
and Futures (Price Stabilizing) Rules, as amended, made under the Securities and Futures Ordinance (Chapter 
571 of the Laws of Hong Kong).
Potential investors should be aware that stabilising action cannot be taken to support the price of the Shares for 
longer than the stabilisation period which begins on the Listing Date and is expected to expire on the 30th day 
after the last day for the lodging of applications under the Hong Kong Public Offering. After this date, no further 
stabilising action may be taken, and demand for the Shares and the price of the Shares could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set 
out in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong 
and/or not resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint Sponsors 
and the Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate effect upon the 
occurrence of any of the events set out in the section headed “Underwriting – Underwriting Arrangements and 
Expenses – Hong Kong Public Offering – Grounds of Termination” in the Prospectus at any time prior to 8:00 
a.m. (Hong Kong time) on the Listing Date.

<<<PAGE 2>>>
– 2 –
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
65,330,000 H Shares (subject to the 
Over-allotment Option)
Number of Hong Kong Offer Shares
:
6,533,000 H Shares (subject to 
reallocation)
Number of International Offer Shares
:
58,797,000 H Shares (subject to 
reallocation and the Over-allotment 
Option)
Offer Price
:
HK$26.39 per H Share, plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
Stock Exchange trading fee of 0.00565% 
and AFRC transaction levy of 0.00015% 
(payable in full on application in Hong 
Kong dollars and subject to refund)
Nominal value
:
RMB0.10 per H Share
Stock code
:
7688
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
– 3 –
Shanghai Top Numerical Control Technology Co., Ltd.
上海拓璞數控科技股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same meanings 
as those defined in the prospectus dated 12 May 2026 (the “Prospectus”) issued by Shanghai Top Numerical 
Control Technology Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, Shareholders 
and prospective investors should be aware that the price of the H Shares could move substantially even 
with a small number of H Shares traded and should exercise extreme caution when dealing in the H 
Shares.
SUMMARY
Company information
Stock code
7688
Stock short name
TOPNC
Dealings commencement date
20 May 2026*
*  see note at the end of this announcement
Price Information
Offer Price
HK$26.39
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the Over-allotment 
Option)
65,330,000
Number of Offer Shares in Hong Kong Public Offering
6,533,000
Number of Offer Shares in International Offering (before exercise of 
the Over-allotment Option)
58,797,000
Number of issued Shares upon Listing (before exercise of the Over-
allotment Option)
409,281,790
Over-allocation
No. of Offer Shares over-allocated
9,799,500
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases 
in the secondary market at prices that do not exceed the Offer Price or through deferred delivery or a 
combination of these means. In the event the Over-allotment Option is exercised, an announcement will be 
made on the Stock Exchange’s website.
Proceeds
Gross proceeds(Note)
HK$1,724.0 million
Less: Estimated listing expenses payable based on Offer Price
HK$(117.6) million
Net proceeds
HK$1,606.4 million
Note:	 Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the use 
of proceeds, please refer to the Prospectus. The Company will adjust the allocation of the net proceeds 
from the exercise of the Over-allotment Option (if any) for the purpose as set out in the section headed 
“Future Plans and Use of Proceeds” of the Prospectus on a pro rata basis.

<<<PAGE 4>>>
– 4 –
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
344,049
No. of successful applications
56,482
Subscription level
3,764.63 times
Reallocation
No
No. of Offer Shares initially available under the Hong Kong Public Offering
6,533,000
No. of Offer Shares reallocated from the International Offering
0
Final no. of Offer Shares under the Hong Kong Public Offering
6,533,000
% of Offer Shares under the Hong Kong Public Offering to the Global Offering 
(before exercise of Over-allotment Option)
10.00%
Note:	 For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by identification number or www.hkeipo.hk/IPOResult for 
the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
104
Subscription Level
30.46 times
No. of Offer Shares initially available under the International Offering
58,797,000
Final no. of Offer Shares under the International Offering
58,797,000
% of Offer Shares under the International Offering to the Global Offering (before 
the exercise of the Over-allotment Option)
90.00%
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the Offer Shares 
subscribed by the placees and the public have been financed directly or indirectly by the Company, any of 
the Directors, chief executive of the Company, Controlling Shareholders, substantial shareholders, existing 
shareholders of the Company or any of its subsidiaries or their respective close associates; and (ii) none of 
the placees and the public who have purchased the Offer Shares are accustomed to taking instructions from 
the Company, any of the Directors, chief executive of the Company, Controlling Shareholders, substantial 
shareholders, existing shareholders of the Company or any of its subsidiaries or their respective close associates 
in relation to the acquisition, disposal, voting or other disposition of Shares registered in his/her/its name or 
otherwise held by him/her/it.

<<<PAGE 5>>>
– 5 –
The placees in the International Offering include the following:
Cornerstone Investors
Investor(Note 1)
No. of Offer 
Shares allocated
% of Offer  
Shares(Note 2)
% of total 
issued Shares 
after the Global 
Offering(Note 2)
Existing 
Shareholders 
or their close 
associates
RBC Global Asset Management (Asia) Limited (“RBC”) (Note 3)
6,536,200
10.00%
1.60%
No
3W Fund Management Limited (“3W”) (Note 3)
5,938,500
9.09%
1.45%
No
Boyu Capital Management (Singapore) Pte. Ltd.  
(“Boyu”) (Notes 3 and 4)
4,453,900
6.82%
1.09%
No
HHLR Advisors, Ltd. (“HHLRA”) (Note 3)
2,969,200
4.54%
0.73%
No
UBS Asset Management (Singapore) Ltd.  
(“UBS AM Singapore”) (Note 3)
2,969,200
4.54%
0.73%
No
CDH Global Frontier Ventures Limited (“CDH”) (Note 3)
2,969,200
4.54%
0.73%
No
Cithara Global Multi-Strategy SPC – Disruptive Innovation 
Investment Fund SP (“Cithara Fund”)
1,484,600
2.27%
0.36%
No
Fullgoal Asset Management (HK) Limited  
(“Fullgoal HK”) (Note 5)
623,500
0.95%
0.15%
No
Fullgoal Fund Management Co., Ltd.  
(“Fullgoal Fund”) (Note 5)
267,200
0.41%
0.07%
No
China Asset Management Co., Ltd.  
(“China AMC”) (Note 6)
890,700
1.36%
0.22%
No
Shanghai Minhang Financial Investment Development Co., 
Ltd. (上海閔行金融投資發展有限公司)  
(“Shanghai Minhang”) (Notes 3 and 7)
890,700
1.36%
0.22%
No
TT International Asset Management Ltd  
(“TT International”) (Note 8)
890,700
1.36%
0.22%
No
Mirae Asset Securities (HK) Limited (“Mirae Asset”)
890,700
1.36%
0.22%
No
Goldman Sachs Asset Management (Hong Kong) Limited 
(“GSAM”)
890,700
1.36%
0.22%
No
Total
32,665,000
50.00%
7.98%
Notes:
1.	
For further details of the Cornerstone Investors, please refer to the section headed “The Cornerstone 
Investments – The Cornerstone Investors” of the Prospectus.
2.	
Assuming the Over-allotment Option is not exercised.
3.	
Only taking into account the Offer Shares allocated to the relevant investors as Cornerstone Investors 
under the Global Offering. In addition to the Offer Shares subscribed for as Cornerstone Investors, RBC, 
3W, Boyu, HHLRA, UBS AM Singapore, CDH and Shanghai Minhang and/or their respective close 
associates were allocated further Offer Shares as a placee in the International Offering. Please refer to the 
section headed “Allotment Results Details – International Offering – Allotees with Consents Obtained” in 
this announcement for details. Only the Offer Shares subscribed for as Cornerstone Investors are subject 
to lock-up as indicated below. For details, please refer to the section headed “Lock-up Undertakings – 
Cornerstone Investors” in this announcement.

<<<PAGE 6>>>
– 6 –
4.	
Aqua Ocean Limited, the entity entering into a Cornerstone Investment Agreement with the Company, the 
Joint Sponsors and the Overall Coordinators to subscribe for the Offer Shares, is a controlled subsidiary of 
Boyu Capital Opportunities Master Fund. Boyu Capital Opportunities Master Fund is an investment fund 
managed by Boyu.
5.	
Each of Fullgoal HK and Fullgoal Fund has entered into a Cornerstone Investment Agreement with the 
Company, the Joint Sponsors and the Overall Coordinators to subscribe for the Offer Shares. Fullgoal HK 
is a wholly owned subsidiary of Fullgoal Fund, which is owned by Guotai Haitong Securities Co., Ltd. 
(stock code: 2611.HK/601211.SH) (“Guotai Haitong”) as to 27.775%. Guotai Junan Securities (Hong 
Kong) Limited (“GTJA Securities”), one of the Overall Coordinators and Underwriters of the Global 
Offering, is a subsidiary of Guotai Haitong. Haitong International Securities Company Limited (“HTIS”), 
a non-syndicate sub-broker in connection with the Global Offering, is also a subsidiary of Guotai Haitong. 
As advised by Fullgoal HK and Fullgoal Fund, each of Fullgoal HK and Fullgoal Fund is considered as a 
member of the same group of companies as GTJA Securities and HTIS and therefore is a connected client 
of GTJA Securities and HTIS for the purpose of paragraph 1B of the Placing Guidelines. For the consent 
under paragraph 1C(1) of the Placing Guidelines granted by the Stock Exchange for the subscription of 
Offer Shares by a connected client of GTJA Securities, please refer to the section headed “Waivers from 
Strict Compliance with the Hong Kong Listing Rules – Consent in respect of the Proposed Subscription 
of Offer Shares by Connected Clients” of the Prospectus. The Company has also applied to the Stock 
Exchange, and the Stock Exchange has granted consent under paragraph 1C(1) of the Placing Guidelines 
in respect of the subscription of Offer Shares by a connected client of HTIS.
6.	
China Asset Management (Hong Kong) Limited (華夏基金(香港)有限公司), the entity entering into a 
Cornerstone Investment Agreement with the Company, the Joint Sponsors and the Overall Coordinators to 
subscribe for the Offer Shares, is a wholly-owned subsidiary of China AMC.
7.	
Shanghai Dalinghao Wan Xinzhi Linghang Private Equity Investment Fund Partnership Enterprise (Limited 
Partnership) (上海大零號灣心致領航私募投資基金合夥企業(有限合夥)), the entity entering into a 
Cornerstone Investment Agreement with the Company, the Joint Sponsors and the Overall Coordinators 
to subscribe for the Offer Shares, is a wholly-owned subsidiary of Shanghai Minhang. Shanghai Minhang 
will subscribe for Offer Shares from the International Offering as a Cornerstone Investor, through the 
subscription of a specific asset management plan, namely, Guotai Haitong Junde QDII 3677 Single 
Asset Management Plan (國泰海通君得QDII3677號單一資產管理計劃) (“Minhang QDII plan”) which 
Shanghai Guotai Haitong Securities Asset Management Co., Ltd. (“Shanghai Guotai”) is the investment 
manager, which is a connected client of GTJA Securities. For the consent under paragraph 1C(1) of the 
Placing Guidelines granted by the Stock Exchange for the subscription of Offer Shares by a connected 
client of GTJA Securities, please refer to the section headed “Waivers from Strict Compliance with the 
Hong Kong Listing Rules – Consent in respect of the Proposed Subscription of Offer Shares by Connected 
Clients” of the Prospectus.
8.	
TT International has entered into a Cornerstone Investment Agreement with the Company, the Joint 
Sponsors and the Overall Coordinators to subscribe for the Offer Shares in its capacity as the investment 
manager on a discretionary basis for and on behalf of its managed account clients, pursuant to the relevant 
investment management agreements, namely:
(i)	
TT Emerging Markets Opportunities Fund II Limited, the ultimate beneficial owner holding 30% or 
more interests of which is Contra Costa County Employees Retirement Association;
(ii)	
TT Emerging Markets Opportunities Fund Limited, the ultimate beneficial owner holding 30% or 
more interest of which is Cardinal AlternativeFocus TT Emerging Markets Fund, L.P.; and
(iii)	
TT Emerging Markets Equity Fund, with no ultimate beneficial owner holding 30% of more interest 
therein.
To the best of the knowledge of TT International, each of such clients are Independent Third Parties.

<<<PAGE 7>>>
– 7 –
Allotees with Consents Obtained
Investor
No. of Offer 
Shares allocated
% of total Offer 
Shares(Note 1)
% of total issued 
Shares after 
the Global 
Offering(Note 1)
Relationship
Allotees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants (the “Guide”) in relation to allocations of further H 
Shares to Cornerstone Investors and/or their close associates (the “Double-dipping Participants”) (Note 2)
RBC
3,919,400
6.00%
0.96%
Same entity as 
Cornerstone 
Investor
3W
3,563,100
5.45%
0.87%
Same entity as 
Cornerstone 
Investor
Boyu(Note 3)
2,375,400
3.64%
0.58%
Close associate of 
a Cornerstone 
Investor
HHLRA
1,484,600
2.27%
0.36%
Same entity as 
Cornerstone 
Investor
UBS AM Singapore
1,484,600
2.27%
0.36%
Same entity as 
Cornerstone 
Investor
CDH
1,484,600
2.27%
0.36%
Same entity as 
Cornerstone 
Investor
Shanghai Minhang
3,700
0.01%
0.001%
Same entity as 
Cornerstone 
Investor
Allotees with consent under paragraph 1C(1) of the Appendix F1 to the Listing Rules (the “Placing Guidelines”) and paragraph 18 of Chapter 4.15 of the 
Guide in relation to allocations to connected clients (Note 4)
Guotai Junan Investments (Hong Kong) Limited (“GTJAI” or 
“GTJA Investments”)
2,075,500
3.18%
0.51%
Connected client
Shanghai Minhang(Note 5)
3,700
0.01%
0.001%
Connected client

<<<PAGE 8>>>
– 8 –
Investor
No. of Offer 
Shares allocated
% of total Offer 
Shares(Note 1)
% of total issued 
Shares after 
the Global 
Offering(Note 1)
Relationship
China Galaxy International Investment Co., Limited (“CGII”)
742,300
1.14%
0.18%
Connected client
Bosera Asset Management (International) Co., Ltd  
(“Bosera AM”)
6,600
0.01%
0.002%
Connected client
Huatai Capital Investment Limited (“HTCI”)
7,500
0.01%
0.002%
Connected client
Notes:
1.	
Assuming the Over-allotment Option is not exercised.
2.	
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the number of Offer Shares allocated to the 
investors as placees in the International Offering. For allocations of Offer Shares to the relevant investors as Cornerstone Investors, please refer to the 
section headed “Allotment Results Details – International Offering – Cornerstone Investors” in this announcement. For details of the consent under 
Chapter 4.15 of the Guide in relation to allocations of further H Shares to the Cornerstone Investors and/or their close associates, please refer to the 
section headed “Others/Additional Information – Allocations of Offer Shares to certain Cornerstone Investors and/or their close associates with a 
consent under paragraph 18 of Chapter 4.15 of the Guide” in this announcement.
3.	
Boyu acts as a fund manager of Boyu Capital Opportunities Master Fund, which is the controlling entity of Aqua Ocean Limited, a Cornerstone 
Investor. Boyu is a close associate of Aqua Ocean Limited.
4.	
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide in relation to allocations to connected clients, 
please refer to the section headed “Others/Additional Information – Placing to connected clients with a prior consent under paragraph 1C(1) of the 
Placing Guidelines” in this announcement.
5.	
For the purpose of participating in the International Offering as a placee, Shanghai Minhang has subscribed for the Offer Shares through the subscription 
of a qualified domestic institutional investor fund (“QDII”) plan, which Shanghai Guotai is the investment manager of such QDII plan. Shanghai Guotai 
is a connected client of GTJA Securities (one of the Overall Coordinators and Underwriters of the Global Offering) and HTIS (a non-syndicate sub-
broker in connection with the Global Offering). In addition, the Stock Exchange has granted consent under paragraph 1C(1) of the Placing Guidelines in 
relation to the allocation of 890,700 H Shares to Shanghai Minhang as a Cornerstone Investor.

<<<PAGE 9>>>
– 9 –
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
Domestic 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
Number of H 
Shares held in 
the Company 
subject 
to lockup 
undertakings 
upon Listing
% of total 
issued Shares 
in the Company 
subject to  
lock-up  
undertakings 
upon  
Listing(Note 1)
Last day subject 
to the lock-up 
undertakings(Note 2)
Wang Yuhan (王宇晗)
12,663,677
113,973,093
30.94%
19 May 2027
Shanghai Tuoxian 
Technology Partnership 
(Limited Partnership) 
(上海拓賢科技合夥企業
(有限合夥))
0
6,624,610
1.62%
19 May 2027
Total
12,663,677
120,597,703
32.56%
Notes:
1.	
Assuming the Over-allotment Option is not exercised.
2.	
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. 
The required lock-up for the Controlling Shareholders ends on 19 May 2027, being one year following the 
Listing Date.

<<<PAGE 10>>>
– 10 –
Cornerstone Investors
Name
Number of H Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
% of total 
issued Shares after 
the Global Offering 
subject to lock-up 
undertakings upon  
Listing(Note 1)
Last day subject 
to the lock-up 
undertakings(Note 2)
RBC
6,536,200
1.60%
19 November 2026
3W
5,938,500
1.45%
19 November 2026
Boyu
4,453,900
1.09%
19 November 2026
HHLRA
2,969,200
0.73%
19 November 2026
UBS AM Singapore
2,969,200
0.73%
19 November 2026
CDH
2,969,200
0.73%
19 November 2026
Cithara Fund
1,484,600
0.36%
19 November 2026
Fullgoal HK
623,500
0.15%
19 November 2026
Fullgoal Fund
267,200
0.07%
19 November 2026
China AMC
890,700
0.22%
19 November 2026
Shanghai Minhang
890,700
0.22%
19 November 2026
TT International
890,700
0.22%
19 November 2026
Mirae Asset
890,700
0.22%
19 November 2026
GSAM
890,700
0.22%
19 November 2026
Total
32,665,000
7.98%
Notes:
1.	
Assuming the Over-allotment Option is not exercised.
2.	
In accordance with the relevant Cornerstone Investment Agreements, the required lock-up ends on 19 
November 2026, being six months following the Listing Date. The Cornerstone Investors will cease to be 
prohibited from disposing of or transferring H Shares subscribed for pursuant to the relevant Cornerstone 
Investment Agreements after the indicated date.

<<<PAGE 11>>>
– 11 –
Other existing Shareholders (including the Pre-IPO Investors as defined in the “History and Corporate 
Structure” section of the Prospectus)
Name
Number of 
Domestic 
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
Shares after the 
Global Offering 
subject to  
lock-up 
undertakings 
upon  
Listing(Note 1)
Last day subject 
to the lock-up 
undertakings(Note 2)
Li Yuhao (李宇昊)
6,491,640
25,966,560
7.93%
19 May 2027
Jiang Jinzhang (姜進章)
2,890,604
11,562,416
3.53%
19 May 2027
Ma Qun (馬群)
1,383,968
5,535,872
1.69%
19 May 2027
Shanghai Yiding Investment Management 
Centre (Limited Partnership) (上海誼鼎投資
管理中心(有限合夥))
4,119,814
23,345,616
6.71%
19 May 2027
Bi Qingzhen (畢慶貞)
618,798
5,569,182
1.51%
19 May 2027
Shenzhen Hehui Wealth Investment Enterprise 
(Limited Partnership) (深圳市和輝財富投資
企業(有限合夥))
0
11,390,880
2.78%
19 May 2027
Shenzhen Zhongyi Hehui Equity Investment 
Enterprise (Limited Partnership) (深圳市中藝
和輝股權投資企業(有限合夥))
0
7,385,140
1.80%
19 May 2027
Zhuhai Jiufeite Changsheng Equity Investment 
Fund Partnership (Limited Partnership)  
(珠海玖菲特長晟股權投資基金合夥企業(有
限合夥))
0
7,000,000
1.71%
19 May 2027
Zhuhai Jiufeite Jiufu Equity Investment Fund 
Partnership (Limited Partnership)  
(珠海玖菲特玖富股權投資基金合夥企業(有
限合夥))
0
5,000,000
1.22%
19 May 2027
Yang Lixuan (楊麗璇)
0
3,000,000
0.73%
19 May 2027
Shanghai Xixiao Technology Partnership 
(Limited Partnership)  
(上海璽霄科技合夥企業(有限合夥))
0
3,100,000
0.76%
19 May 2027
Hanzhong Zhonghe Advanced Manufacturing 
Industry Development Fund Partnership 
(Limited Partnership) (漢中眾合先進製造產
業發展基金合夥企業(有限合夥))
0
1,000,000
0.24%
19 May 2027
Gong Wen (龔雯)
105,000
595,000
0.17%
19 May 2027
Jiaxing CDH Geying Equity Investment 
Cooperation Enterprise (Limited Partnership) 
(嘉興鼎暉戈迎股權投資合夥企業 
(有限合夥))
0
19,118,750
4.67%
19 May 2027

<<<PAGE 12>>>
– 12 –
Name
Number of 
Domestic 
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
Shares after the 
Global Offering 
subject to  
lock-up 
undertakings 
upon  
Listing(Note 1)
Last day subject 
to the lock-up 
undertakings(Note 2)
Changzhou Yongyuan Venture Capital 
Investment Partnership (Limited Partnership) 
(常州永元創業投資合夥企業(有限合夥))
1,755,820
0
0.43%
19 May 2027
Yiwu Dongshun Real Estate Limited Company 
(義烏市東順置業有限公司)
764,750
0
0.19%
19 May 2027
Guangzhou Yujian Manufacturing Industry 
Equity Investment Fund LP (廣州煜健製造產
業股權投資基金合夥企業(有限合夥))
1,170,540
0
0.29%
19 May 2027
Shanghai Linsong Industrial Internet 
Venture Capital Fund Partnership (Limited 
Partnership) (上海臨松工業互聯網創業投資
基金合夥企業(有限合夥))
0
2,248,370
0.55%
19 May 2027
ShanghaiSongfanhui Enterprise Management 
Center (Limited Partnership) (上海松藩匯企
業管理中心(有限合夥))
0
45,880
0.01%
19 May 2027
Changzhou Xiangnong Industrial Investment 
Partnership (Limited Partnership)  
(常州祥檂實業投資合夥企業(有限合夥))
2,203,840
0
0.54%
19 May 2027
Xu Jie (徐傑)
0
1,826,720
0.45%
19 May 2027
Jiaxing Tengyin Equity Investment Partnership 
(Limited Partnership) (嘉興騰寅股權投資合
夥企業(有限合夥))
769,230
0
0.19%
19 May 2027
Gongqingcheng Xinzhou Venture Capital 
Partnership (Limited Partnership) (共青城芯
軸創業投資合夥企業(有限合夥))
0
4,700,000
1.15%
19 May 2027
Pan Jiaquan (潘家全)
0
2,146,650
0.52%
19 May 2027
Ningbo Yujun Equity Investment Partnership 
(Limited Partnership) (寧波與君股權投資合
夥企業(有限合夥))
0
2,000,000
0.49%
19 May 2027
Gongqingcheng Yuantuo Enterprise Investment 
Partnership (Limited Partnership) (共青城源
拓企業投資合夥企業(有限合夥))
0
6,380,000
1.56%
19 May 2027
Zhuhai Junlian Tuopu Venture Capital 
Enterprise (Limited Partnership) (珠海君聯拓
璞創業投資企業(有限合夥))
0
2,424,250
0.59%
19 May 2027
Zhuhai Jiufit Jiufu No.5 Equity Investment Fund 
Partnership (Limited Partnership) (珠海玖菲
特玖富五號股權投資基金合夥企業(有限合
夥))
0
2,315,150
0.57%
19 May 2027

<<<PAGE 13>>>
– 13 –
Name
Number of 
Domestic 
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
Shares after the 
Global Offering 
subject to  
lock-up 
undertakings 
upon  
Listing(Note 1)
Last day subject 
to the lock-up 
undertakings(Note 2)
Yangzhou Xinyuan Equity Investment 
Partnership (Limited Partnership) (揚州鑫元
股權投資合夥企業(有限合夥))
0
1,212,120
0.30%
19 May 2027
Pingtan Boda Hongye Equity Investment 
Partnership (Limited Partnership) (平潭博大
鴻業股權投資合夥企業(有限合夥))
303,030
1,212,120
0.37%
19 May 2027
Zhuhai Ruixin Zhaofeng Venture Capital Center 
(Limited Partnership) (珠海市瑞信兆豐創業
投資中心(有限合夥))
0
680,000
0.17%
19 May 2027
Foshan Zhaofeng Bona Equity Investment 
Center (Limited Partnership) (佛山市兆豐博
納股權投資中心(有限合夥))
0
680,000
0.17%
19 May 2027
Foshan Zhaofeng Tiancheng Equity Investment 
Center (Limited Partnership) (佛山市兆豐天
成股權投資中心(有限合夥))
0
748,000
0.18%
19 May 2027
Zhuhai Qingke Chenxi No. 1 Private Equity 
Investment Fund Partnership (Limited 
Partnership) (珠海青稞晨曦壹號私募股權投
資基金合夥企業(有限合夥))
0
680,270
0.17%
19 May 2027
Jiaxing Nanhu Keying Equity Investment 
Partnership (Limited Partnership) (嘉興南湖
科盈股權投資合夥企業(有限合夥))
1,818,182
7,272,728
2.22%
19 May 2027
Qingdao South China Dingye Yingwan 
Investment Partnership (Limited Partnership) 
(青島華南鼎業盈灣投資合夥企業 
(有限合夥))
239,795
719,385
0.23%
19 May 2027
Rizhao Muzhizhi Management Consulting 
Partnership (Limited Partnership) (日照市沐
之智股權投資基金中心(有限合夥))
510,198
1,190,462
0.42%
19 May 2027
Jiaxing Hongyang Huafu Jingqi Equity 
Investment Partnership (Limited Partnership) 
(嘉興泓陽華馥景祺股權投資合夥企業 
(有限合夥))
0
2,159,840
0.53%
19 May 2027
Qingdao Zhongjunqunxin Venture Capital Fund 
Partnership (Limited Partnership)  
(青島中駿群新創業投資基金合夥企業 
(有限合夥))
0
2,395,750
0.59%
19 May 2027
Tianjin Haisheng Fuyuan Investment 
Management Partnership (Limited 
Partnership) (天津海盛富遠投資管理合夥企
業(有限合夥))
0
472,410
0.12%
19 May 2027

<<<PAGE 14>>>
– 14 –
Name
Number of 
Domestic 
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
Shares after the 
Global Offering 
subject to  
lock-up 
undertakings 
upon  
Listing(Note 1)
Last day subject 
to the lock-up 
undertakings(Note 2)
China Post Life Insurance Co., Ltd. (中郵人壽
保險股份有限公司)
0
6,351,930
1.55%
19 May 2027
Beijing Yuanjing Investment Fund Center 
(Limited Partnership) (北京遠京投資基金中
心(有限合夥))
0
1,759,310
0.43%
19 May 2027
Beijing JGC Chuanghui Equity Investment 
Center (Limited Partnership) (北京京國創創
輝股權投資中心(有限合夥))
0
7,030
0.00%
19 May 2027
Jiaxing Zhiyou Venture Capital Partnership 
(Limited Partnership) (嘉興祉猷創業投資合
夥企業(有限合夥))
0
716,750
0.18%
19 May 2027
Xuchang Digital Economy Equity Investment 
Fund Partnership (Limited Partnership)  
(許昌數字經濟股權投資基金合夥企業 
(有限合夥))
0
1,303,180
0.32%
19 May 2027
Jiangsu Jianyin Investment Co., Ltd. (江蘇建銀
投資有限公司)
0
1,600,010
0.39%
19 May 2027
Tianjin Winfund Specialised No. 3 Venture 
Capital Partnership (Limited Partnership)  
(天津元藩專精叁號創業投資合夥企業(有限
合夥))
0
727,470
0.18%
19 May 2027
Total
25,145,209
185,545,201
51.48%
Notes:
1.	
Assuming the Over-allotment Option is not exercised.
2.	
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. The 
required lock-up for all existing Shareholders (including the Pre-IPO Investors) ends on 19 May 2027, 
being one year following the Listing Date.

<<<PAGE 15>>>
– 15 –
Placees with voluntary lock-up undertakings
Name
Number of H 
Shares held in 
the Company 
subject to lock-up 
undertakings 
upon Listing
% of total 
issued Shares 
after the Global 
Offering subject 
to lock-up 
undertakings upon 
Listing(Note 1)
Last day subject 
to the lock-up 
undertakings(Note 2)
Baring Asset Management 
(Asia) Limited
1,484,600
0.36%
19 November 2026
JUMP TRADING PACIFIC 
PTE. LTD.
890,700
0.22%
19 November 2026
Optimas Capital Limited
890,700
0.22%
19 November 2026
Total
3,266,000
0.80%
Notes:
1.	
Assuming the Over-allotment Option is not exercised.
2.	
Each of the placees has given a voluntary lock-up undertaking with the Company, pursuant to which such 
placee shall not dispose of the Shares placed with it under the International Offering within six months 
from the Listing Date.
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming the 
Over-
allotment 
Option is not 
exercised)
Allotment 
as % of 
International 
Offering 
(assuming the 
Over-
allotment 
Option is 
exercised)
Allotment 
as % of total 
Offer Shares 
(assuming the 
Over-
allotment 
Option is not 
exercised)
Allotment 
as % of total 
Offer Shares 
(assuming the 
Over-
allotment 
Option is 
exercised)
Number of 
Shares held 
upon Listing
% of total 
issued Shares 
upon Listing 
(assuming the 
Over-
allotment 
Option is not 
exercised)
% of total 
issued Shares 
upon Listing 
(assuming the 
Over-
allotment 
Option is 
exercised)
Top 1
10,455,600
17.78%
15.24%
16.00%
13.92%
10,455,600
2.55%
2.49%
Top 5
35,694,100
60.71%
52.03%
54.64%
47.51%
35,694,100
8.72%
8.52%
Top 10
46,828,600
79.64%
68.27%
71.68%
62.33%
46,828,600
11.44%
11.17%
Top 25
62,268,600
105.90%
90.78%
95.31%
82.88%
62,268,600
15.21%
14.86%
*	
Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 16>>>
– 16 –
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming the 
Over-
allotment 
Option is not 
exercised)
Allotment 
as % of 
International 
Offering 
(assuming the 
Over-
allotment 
Option is 
exercised)
Allotment 
as % of total 
Offer Shares 
(assuming the 
Over-
allotment 
Option is not 
exercised)
Allotment 
as % of total 
Offer Shares 
(assuming the 
Over-
allotment 
Option is 
exercised)
Number of 
H Shares 
held upon 
Listing
% of 
total issued 
H Shares 
upon Listing 
(assuming the 
Over-
allotment 
Option is not 
exercised)
% of 
total issued 
H Shares 
upon Listing 
(assuming the 
Over-
allotment 
Option is 
exercised)
Number of 
Shares held 
upon Listing
Top 1
0
0.00%
0.00%
0.00%
0.00%
120,597,703
32.46%
31.63%
133,261,380
Top 5
0
0.00%
0.00%
0.00%
0.00%
207,804,649
55.94%
54.50%
231,079,780
Top 10
19,957,200
33.94%
29.09%
30.55%
26.56%
260,912,143
70.24%
68.43%
288,896,060
Top 25
40,147,900
68.28%
58.53%
61.45%
53.44%
324,968,037
87.48%
85.23%
354,954,720
*	
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholder upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming the 
Over-
allotment 
Option is not 
exercised)
Allotment 
as % of 
International 
Offering 
(assuming the 
Over-
allotment 
Option is 
exercised)
Allotment 
as % of total 
Offer Shares 
(assuming the 
Over-
allotment 
Option is not 
exercised)
Allotment 
as % of total 
Offer Shares 
(assuming the 
Over-
allotment 
Option is 
exercised)
Number of 
H Shares 
held upon 
Listing
Number of 
Shares held 
upon Listing
% of total 
issued Shares 
upon Listing 
(assuming the 
Over-
allotment 
Option is not 
exercised)
% of total 
issued Shares 
upon Listing 
(assuming the 
Over-
allotment 
Option is 
exercised)
Top 1
0
0.00%
0.00%
0.00%
0.00%
120,597,703
133,261,380
32.56%
31.80%
Top 5
0
0.00%
0.00%
0.00%
0.00%
207,804,649
231,079,780
56.46%
55.14%
Top 10
19,957,200
33.94%
29.09%
30.55%
26.56%
260,912,143
288,896,060
70.59%
68.94%
Top 25
40,147,900
68.28%
58.53%
61.45%
53.44%
322,808,197
354,998,720
86.74%
84.71%
*	
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon 
Listing.

<<<PAGE 17>>>
– 17 –
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by the public will 
be conditionally allocated on the basis set out below:
Number of 
H Shares 
applied for
Number of 
valid 
applications
Basis of allocation/ballot
Approximate 
percentage 
allotted of the total 
number of H Shares 
applied for
Pool A
100
74,712
5,977 out of 74,712 applicants to receive 100 H Shares
8.00%
200
14,736
1,257 out of 14,736 applicants to receive 100 H Shares
4.27%
300
16,720
1,481 out of 16,720 applicants to receive 100 H Shares
2.95%
400
7,070
643 out of 7,070 applicants to receive 100 H Shares
2.27%
500
7,863
731 out of 7,863 applicants to receive 100 H Shares
1.86%
600
3,782
358 out of 3,782 applicants to receive 100 H Shares
1.58%
700
2,797
268 out of 2,797 applicants to receive 100 H Shares
1.37%
800
3,042
295 out of 3,042 applicants to receive 100 H Shares
1.21%
900
4,317
424 out of 4,317 applicants to receive 100 H Shares
1.09%
1,000
24,888
2,464 out of 24,888 applicants to receive 100 H Shares
0.99%
1,500
12,818
1,318 out of 12,818 applicants to receive 100 H Shares
0.69%
2,000
7,150
755 out of 7,150 applicants to receive 100 H Shares
0.53%
2,500
4,598
496 out of 4,598 applicants to receive 100 H Shares
0.43%
3,000
4,657
511 out of 4,657 applicants to receive 100 H Shares
0.37%
3,500
6,804
757 out of 6,804 applicants to receive 100 H Shares
0.32%
4,000
3,956
446 out of 3,956 applicants to receive 100 H Shares
0.28%
4,500
2,499
285 out of 2,499 applicants to receive 100 H Shares
0.25%
5,000
5,187
596 out of 5,187 applicants to receive 100 H Shares
0.23%
6,000
4,020
470 out of 4,020 applicants to receive 100 H Shares
0.19%
7,000
3,735
443 out of 3,735 applicants to receive 100 H Shares
0.17%
8,000
3,456
415 out of 3,456 applicants to receive 100 H Shares
0.15%
9,000
3,639
442 out of 3,639 applicants to receive 100 H Shares
0.13%
10,000
18,654
2,286 out of 18,654 applicants to receive 100 H Shares
0.12%
20,000
11,506
1,503 out of 11,506 applicants to receive 100 H Shares
0.07%
30,000
7,542
1,023 out of 7,542 applicants to receive 100 H Shares
0.05%
40,000
6,642
925 out of 6,642 applicants to receive 100 H Shares
0.03%
50,000
4,743
675 out of 4,743 applicants to receive 100 H Shares
0.03%
60,000
3,373
488 out of 3,373 applicants to receive 100 H Shares
0.02%
70,000
2,888
424 out of 2,888 applicants to receive 100 H Shares
0.02%
80,000
3,158
469 out of 3,158 applicants to receive 100 H Shares
0.02%
90,000
2,392
360 out of 2,392 applicants to receive 100 H Shares
0.02%
100,000
24,273
3,680 out of 24,273 applicants to receive 100 H Shares
0.02%
 
Total
307,617
Total number of Pool A successful applicants: 32,665
 

<<<PAGE 18>>>
– 18 –
Number of 
H Shares 
applied for
Number of 
valid 
applications
Basis of allocation/ballot
Approximate 
percentage 
allotted of the total 
number of H Shares 
applied for
Pool B
200,000
15,171
6,069 out of 15,171 applicants to receive 100 H Shares
0.02%
300,000
4,771
2,700 out of 4,771 applicants to receive 100 H Shares
0.02%
400,000
3,964
2,823 out of 3,964 applicants to receive 100 H Shares
0.02%
500,000
2,430
2,129 out of 2,430 applicants to receive 100 H Shares
0.02%
600,000
1,682
100 H Shares
0.02%
700,000
1,300
100 H Shares plus 202 out of 1,300 applicants to receive an 
additional 100 H Shares
0.02%
800,000
1,047
100 H Shares plus 319 out of 1,047 applicants to receive an 
additional 100 H Shares
0.02%
900,000
741
100 H Shares plus 333 out of 741 applicants to receive an 
additional 100 H Shares
0.02%
1,000,000
2,913
100 H Shares plus 1,690 out of 2,913 applicants to receive an 
additional 100 H Shares
0.02%
2,000,000
1,295
200 H Shares plus 1,114 out of 1,295 applicants to receive an 
additional 100 H Shares
0.01%
3,266,500
1,118
400 H Shares plus 541 out of 1,118 applicants to receive an 
additional 100 H Shares
0.01%
 
Total
36,432
Total number of Pool B successful applicants: 23,817
 
As of the date of this announcement, the relevant subscription monies previously deposited in the designated 
nominee accounts have been remitted back to the accounts of all HKSCC participants. Investors should contact 
their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of which consent 
has been obtained, the Company has complied with the Listing Rules and guidance materials in relation to the 
placing, allotment and listing of the H Shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or indirectly, provided by 
the Company, its Controlling Shareholders, Directors or syndicate members to any placees or the public (as the 
case may be) and the consideration payable by them directly or indirectly for each Offer Share subscribed for 
or purchased by them is the same as the Offer Price in addition to any brokerage, AFRC transaction levy, SFC 
transaction levy and trading fee payable.

<<<PAGE 19>>>
– 19 –
OTHERS/ADDITIONAL INFORMATION
Allocations of Offer Shares to certain Cornerstone Investors and/or their close associates with a consent 
under paragraph 18 of Chapter 4.15 of the Guide
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph 18 of Chapter 4.15 
of the Guide to permit the Company to allocate further Offer Shares in the International Offering to the Double-
dipping Participants as placees (the “Size-based Exemption”), subject to the following conditions:
(a)	
the final offering size of the Global Offering, excluding any over-allocation, will be of a total value of at 
least HK$1 billion;
(b)	
each Director, chief executive of the Company and Controlling Shareholder confirms that no securities 
have been allocated to them or their respective close associates under the Size-based Exemption;
(c)	
the allocation to the Double-dipping Participants will not affect the Company’s ability to satisfy the public 
float requirement; and
(d)	
details of the allocation to the Double-dipping Participants under the Size-based Exemption will be 
disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted by the Stock 
Exchange.
For details of the allocations of Offer Shares to the Double-dipping Participants, please refer to the section 
headed “Allotment Results Details – International Offering – Allotees with Consents Obtained” in this 
announcement.
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines
The Company has applied to the Stock Exchange, and the Stock Exchange has granted, a consent under paragraph 
1C(1) of the Placing Guidelines to permit the Company to allocate certain Offer Shares in the International 
Offering to connected clients. The allocation of Offer Shares to such connected clients is in compliance with all 
the conditions under the consent granted by the Stock Exchange.

<<<PAGE 20>>>
– 20 –
Details of the placement to the connected clients are set out below:
No.
Connected distributor
Connected 
client
Relationship 
between connected 
distributor and 
connected client
Basis of 
holding 
securities
No. of 
Offer Shares 
subscribed
% 
to total 
Offer Shares 
under Global 
Offering(Note 1)
% to total 
issued Shares 
immediately 
upon 
completion 
of the Global 
Offering(Note 1)
1
GTJA Securities and 
HTIS
Guotai Junan 
Investments (Hong 
Kong) Limited 
(“GTJAI” or “GTJA 
Investments”)
GTJA Investment is a 
member of the same group of 
companies as GTJA Securities 
and HTIS and is considered a 
connected client of GTJA  
Securities.(Note 2)
Non-
discretionary
2,075,500
3.18%
0.51%
2
Shanghai Guotai 
Haitong Securities 
Asset Management 
Co., Ltd. (“Shanghai 
Guotai”)
Shanghai Minhang will 
subscribe for Offer Shares 
from International Offering 
as a Cornerstone Investor, 
through the subscription of 
a specific asset management 
plan, namely, Minhang QDII 
plan which Shanghai Guotai is 
the investment manager, which 
is a connected client of GTJA 
Securities.
Discretionary
890,700
1.36%
0.22%
Shanghai Minhang will 
further subscribe for Offer 
Shares from International 
Offering as a placee, through 
the subscription of a specific 
asset management plan, 
namely Minhang QDII plan 
which Shanghai Guotai is the 
investment manager, which 
is a connected client of GTJA 
Securities and HTIS.
Discretionary
3,700
0.01%
0.001%

<<<PAGE 21>>>
– 21 –
No.
Connected distributor
Connected 
client
Relationship 
between connected 
distributor and 
connected client
Basis of 
holding 
securities
No. of 
Offer Shares 
subscribed
% 
to total 
Offer Shares 
under Global 
Offering(Note 1)
% to total 
issued Shares 
immediately 
upon 
completion 
of the Global 
Offering(Note 1)
3
China Galaxy 
International Securities 
(Hong Kong) Co., 
Limited (“CGIS”)
China Galaxy 
International 
Investment Co., 
Limited (“CGII”)
CGII is a member of the same 
group of companies as CGIS 
and CGII is considered a 
connected client of CGIS.(Note 3)
Non-
discretionary
742,300
1.14%
0.18%
4
(1)	 CMB International 
Capital Limited 
(“CMB 
International”)
(2)	 CMB International 
Securities 
Limited (“CMBI 
Securities”)
(3)	 CMB International 
Global Markets 
Limited (“CMBI 
Global Markets”, 
together with CMB 
International and 
CMBI Securities, 
the “CMBI 
Connected 
Distributors”)
Bosera Asset 
Management 
(International) Co., 
Ltd (“Bosera AM”)
Bosera AM is a member of the 
same group with the CMBI 
Connected Distributors.(Note 4)
Discretionary
6,600
0.01%
0.002%
5
Huatai Financial 
Holdings (Hong Kong) 
Limited (“HTFH”)
Huatai Capital 
Investment Limited 
(“HTCI”)
HTCI is a member of the same 
group of companies as HTFH.
(Note 5)
Non-
discretionary
7,500
0.01%
0.002%
Notes:
1.	
Assuming no exercise of the Over-allotment Option.
2.	
GTJAI will participate as placee to subscribe for the Offer Shares under the International Offering (the 
“GTJAI Subscription”).
In relation to the GTJAI Subscription, GTJAI shall hold the Offer Shares for hedging purpose as the single 
underlying asset of several sets of back-to-back total return swap transaction (the “GTHT Back-to-back 
TRS”) to be entered into between GTJAI and Guotai Haitong Securities Co., Ltd. (the “GTHT Onshore 
Parent”) in connection with several total return swap orders (the “GTHT Client TRS”) to be entered 
into by GTHT Onshore Parent and several ultimate clients (the “GTHT Onshore Ultimate Client”), 
respectively. Such GTHT Client TRS is to be fully funded by the GTHT Onshore Ultimate Client. GTJAI 
will hold the Offer Shares on a non-discretionary basis for the purpose of hedging the economic exposure 
under the GTHT Back-to-back TRS and GTHT Client TRS only.

<<<PAGE 22>>>
– 22 –
During the tenor of the GTHT Client TRS, all economic returns of the Offer Shares will be passed to the 
GTHT Onshore Ultimate Clients and all economic losses shall be borne by the GTHT Onshore Ultimate 
Client, subject to the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS, and 
GTJAI will not take part in any economic return or bear any economic loss in relation to the price of the 
Offer Shares. The GTHT Onshore Ultimate Client may request to redeem the Offer Shares at their own 
discretion, upon which GTJAI shall dispose of the Offer Shares and settle the GTHT Back-to-back TRS 
and GTHT Client TRS in cash in accordance with the terms and conditions of the GTHT Back-to-back 
TRS and GTHT Client TRS documents. Due to its internal policy, GTJAI will not exercise the voting right 
attaching to the Offer Shares during the tenor of the GTHT Back-to-back TRS and GTHT Client TRS.
To the best knowledge of GTJA Investments after making all reasonable enquiries, (i) each of the 
GTHT Onshore Ultimate Clients is an independent third party of GTJA Investments, GTJA Securities 
and the companies which are members of the same group of GTJA Securities; (ii) each of the ultimate 
beneficial owners holding 30% or more interests of GTHT Onshore Ultimate Clients is an independent 
third party of the Company, GTJA Investments, GTJA Securities and the companies which are members 
of the same group of GTJA Securities; and (iii) each of the GTHT Onshore Ultimate Clients and their 
respective ultimate beneficial owners (as set out below) is an independent third party of the Company, the 
subsidiaries, Controlling Shareholders, substantial shareholders, existing shareholders of the Company (the 
“Relevant Parties”), and respective subsidiaries and/or respective close associates of the Relevant Parties.
Such GTHT Client TRS is to be fully funded by the GTHT Onshore Ultimate Clients:
Swap Investor
Ultimate 
beneficial 
owner (“UBO”)
Remarks
Zhonghe (Tianjin) Investment Management Co. Ltd 
– Zhonghe Capital Cultivation 8 Private Securities 
Investment Fund (錦繡中和（天津）投資管理有
限公司－中和資本耕耘8號私募證券投資基金)
Zhang Jingting  
(張敬庭)
UBO with over 30% interest
Zhonghe (tianjin) Investment Management Co. Ltd – 
Zhonghe Capital Cultivation 810 Private Securities 
Investment Fund (錦繡中和（天津）投資管理有
限公司－中和資本耕耘810號私募證券投資基金)
Zhang Jingting  
(張敬庭)
UBO with over 30% interest
Zhonghe (Tianjin) Investment Management Co. 
Ltd – Zhonghe Capital Jinjun Private Securities 
Investment Fund (錦繡中和（天津）投資管理有
限公司－中和資本金君私募證券投資基金)
Zhang Shujun  
(張淑君)
UBO with over 30% interest
Shenzhen Commando Capital Management Co.,  
Ltd. – Commando No.003 Actively Managed  
Fund Private Securities Investment Fund (深圳市
康曼德資本管理有限公司－康曼德003號主動管
理型私募證券投資基金)
None
No UBO holding 30% or more 
interest
Shanghai Thunder Fund Management Co., Ltd. – 
Thunder Hengyi No.3 Private Securities Investment 
Fund (上海春雷私募基金管理有限公司－春雷恒
溢3號私募證券投資基金)
None
No UBO holding 30% or more 
interest

<<<PAGE 23>>>
– 23 –
To the best knowledge of GTJAI and after making all reasonable enquiries, (i) GTJA Investments has 
confirmed that, to the best of their knowledge, each of the GTHT Onshore Ultimate Clients and the 
ultimate beneficial owners holding 30% or more interest of the GTHT Onshore Ultimate Clients listed 
above is an independent third party of GTJA Investments, GTJA Securities and the companies which 
are members of the same group of companies as GTJA Securities, and (ii) GTJAI is not a collective 
investment scheme which is not authorised by the SFC nor is expected to hold the Offer Shares on behalf 
of such scheme.
3.	
CGII and China Galaxy Securities (“CGS”) will enter into a series of cross border total return swap (TRS) 
transactions (collectively, the “CGII TRS”) with each other and the ultimate client (“CGII Ultimate 
Client”), pursuant to which CGII will hold the Offer Shares on a non-discretionary basis to hedge the 
CGII TRS while the economic risks and returns of the underlying Offer Shares are ultimately borne by 
the CGII Ultimate Client, subject to customary fees and commissions. The CGII TRS will be fully funded 
by the CGII Ultimate Client. During the terms of the CGII TRS, all economic returns of the Offer Shares 
subscribed by CGII will be passed to CGII Ultimate Client and all economic loss shall be borne by CGII 
Ultimate Client through the CGII TRS, and CGII will not take part in any economic return or bear any 
economic loss in relation to the Offer Shares.
The CGII Ultimate Client may exercise an early termination right to terminate the CGII TRS at any time 
from the issue date of the CGII TRS which should be on or after the date on which the Offer Shares are 
listed on the Stock Exchange. Upon the termination upon maturity or early termination of the CGII TRS 
by the CGII Ultimate Client, CGII will dispose of the Offer Shares on the secondary market and the CGII 
Ultimate Client will receive final settlement amount of the back-to-back TRS which should have taken 
into account all the economic returns or economic loss in relation to the Offer Shares. If upon the maturity 
of the CGII TRS, the CGII Ultimate Client intends to extend the investment period, subject to further 
agreement between CGII and the CGII Ultimate Client, the term of the CGII TRS could be extended by 
way of a new issuance or a tenor extension. Accordingly, CGII will extend the term of the back-to-back 
TRS by way of a new issuance or a tenor extension.
CGII will hold the legal title and the voting right of the Offer Shares by itself, and pass through the 
economic exposure to the CGII Ultimate Client, which place CGII TRS orders through their asset manager 
with CGII in connection with the IPO of the Company. Due to its internal policy, CGII will not exercise 
the voting right of the Offer Shares during the tenor of the back-to-back TRS.
During the life of the CGII TRS and back-to-back TRS, CGII may continue to hold the Offer Shares in 
its custodian account, or to hold some or all of the Offer Shares in a prime brokerage account for stock 
borrowing purposes.
As permitted under the contractual arrangement with the CGII Ultimate Client, CGII will lend out its 
holding of underlying Offer Shares in the form of stock borrowing loans consistent with market practice to 
lower its finance costs, provided that CGII has the ability to call back the Offer Shares on loan at any time 
in order to satisfy its obligations under the back-to-back TRS to ensure the economic interests to be passed 
to the CGII Ultimate Client under the CGII TRS will remain unchanged.
To the best of CGII’s knowledge after having made all reasonable inquiries, the CGII Ultimate Client is an 
independent third party of CGII, and the companies which are members of the same group of CGIS.
Both CGII and CGIS are indirect wholly-owned subsidiaries of CGS, the A shares of which are listed 
on the Shanghai Stock Exchange (stock code: 601881), the H shares of which are listed on the Stock 
Exchange (stock code: 6881). CGII is a connected client (as defined under the Placing Guidelines) of 
CGIS, holding securities on a non-discretionary basis on behalf of independent third parties.

<<<PAGE 24>>>
– 24 –
Such CGII TRS is to be fully funded by the CGII Ultimate Client:
Swap Investor
UBO
Remarks
Commando No. 112 Private Securities Investment 
Fund (康曼德112號私募證券投資基金)
Liu Qiwei  
(劉奇偉)
UBO with over 30% interest
Commando No. 111 Private Securities Investment 
Fund (康曼德111號私募證券投資基金)
Zhou Kun (周琨)
UBO with over 30% interest
Xinhong Commando Ying Active Management  
Private Securities Investment Fund (信鴻康曼德
楹主動管理型私募證券投資基金)
Ding Ying (丁楹)
UBO with over 30% interest
Shenzhen Commando Capital Management  
Co., Ltd (深圳市康曼德資本管理有限公司)
Ding Ying (丁楹)
UBO with over 30% interest
4.	
Bosera AM will hold the Offer Shares in its capacity as the discretionary fund manager managing the 
funds on behalf of its underlying clients. To the best knowledge, information and belief of Bosera AM 
after due enquiry, the underlying clients of Bosera AM are independent third parties of Bosera AM, 
the CMBI Connected Distributors, CMS and the companies which are members of the same group of 
companies as the CMBI Connected Distributors and CMS.
5.	
HTCI will subscribe for and hold the beneficial interest of the Offer Shares as a placee under the 
International Offering on behalf of its underlying onshore client (“HTCI Ultimate Client”), namely, 
Shanghai Chuying Private Equity Fund Management Co., Ltd. – Chuying Yuanshan Steady No. 1 Private 
Equity Investment Fund (上海初櫻私募基金管理有限公司 – 初櫻遠山穩健1號私募證券投資基金), the 
ultimate beneficial owner holding 30% or more interest of which is Lu Hui.
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial 
public offerings (“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products issued 
by appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. 
In connection with such products, the licensed domestic securities firms, through their Hong Kong 
affiliates, may participate in Hong Kong IPOs either as placees or cornerstone investors (the “Cross-border 
Derivatives Trading Regime”).
Huatai Securities Co., Ltd. (“HTSC”), the A shares of which are listed on the Shanghai Stock Exchange 
(stock code: 601688), the H shares of which are listed on the Stock Exchange (stock code: 6886), and the 
global depositary receipts of which are listed on the London Stock Exchange (LON: HTSC), is one of the 
domestic securities firms licensed to undertake cross-border derivatives trading activities. HTSC entered 
into an ISDA agreement (the “ISDA Agreement”) with its indirectly wholly-owned subsidiary, HTCI, to 
set out the principal terms of any future total return swap between HTSC and HTCI.
HTFH is the connected distributor. Pursuant to the ISDA Agreement, HTCI, which intends to participate 
in the International Offering as a placee, will hold the beneficial interest of the Offer Shares on a non-
discretionary basis as the single underlying holder under a back-to-back total return swap (the “HT Back-
to-back TRS”) to be entered by HTCI in connection with Huatai TRS (as defined below) placed by and 
fully funded (i.e. with no financing provided by HTCI) by the HTCI Ultimate Client, by which, HTCI will, 
subject to customary fees and commissions, pass the full economic exposure of the Offer Shares ultimately 
to the HTCI Ultimate Client, which in effect, HTCI will hold the beneficial interest of the Offer Shares on 
behalf of the HTCI Ultimate Client. HTFH and HTCI are indirectly wholly-owned subsidiaries of HTSC. 
Accordingly, HTCI is considered as a connected clients of HTFH pursuant to paragraph 1B(7) of the 
Placing Guidelines.

<<<PAGE 25>>>
– 25 –
Pursuant to the Cross-border Derivatives Trading Regime, the HTCI Ultimate Client cannot directly 
subscribe for the Offer Shares but may invest in derivative products issued by domestic securities firms 
licenced to undertake cross-border derivatives trading activities, such as HTSC, with the Offer Shares 
as the underlying assets. Instead of directly subscribing for the Offer Shares, the HTCI Ultimate Client 
will, through its investment manager, place a total return swap order (the “Huatai TRS”) with HTSC in 
connection with the Company’s IPO and HTSC will place a HT Back-to-back TRS order to HTCI on the 
terms of the ISDA Agreement. In order to hedge its exposure under the HT Back-to-back TRS, HTCI 
participates in the Company’s IPO and subscribes for the Offer Shares through placing order with HTFH 
during the International Offering.
To the best knowledge of HTCI after making all reasonable enquiries, no other ultimate beneficial owner 
holds 30% or more interest in the HTCI Ultimate Client and the HTCI Ultimate Client is an independent 
third party of (i) the Company, the connected person or the associates thereof, and (ii) HTCI, HTFH and 
the companies which are members of the same group of HTCI.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the HT Back-to-back TRS in 
connection with the Huatai TRS order placed by the HTCI Ultimate Client. Pursuant to the terms of the 
contracts of the HT Back-to-back TRS and the Huatai TRS, during the tenor of the HT Back-to-back TRS 
and the Huatai TRS, subject to customary fees and commissions, all economic returns of the Offer Shares 
will be ultimately passed to the HTCI Ultimate Client through the HT Back-to-back TRS and the Huatai 
TRS and all economic loss shall be ultimately borne by the HTCI Ultimate Client. HTCI will not take any 
economic return or bear any economic loss in relation to the Offer Shares, save as customary fees and 
commissions.
Investment in the HT Back-to-back TRS and the Huatai TRS is similar to the investment in a QDII in the 
way that the HTCI Ultimate Client would reap all the economic benefits of the underlying Offer Shares, 
except that a QDII fund would pass through the exchange rate exposure on both the notional value of the 
investment and the profit and loss of the investment. In contrast, the profit and loss of the HT Back-to-
back TRS and the Huatai TRS factor into account the fluctuation in RMB exchange rate upon termination 
of the Huatai TRS by converting the profit and loss using the current exchange rate at the time of 
termination. As such, the HTCI Ultimate Client would bear the exchange rate exposure of the profit and 
loss on settlement date.
The HTCI Ultimate Client may exercise an early termination right to terminate the Huatai TRS at any 
time from the issue date of the Huatai TRS which should be on or after the date on which the Offer 
Shares are listed on the Stock Exchange at its own discretion. Upon the termination upon maturity or 
early termination of the Huatai TRS by the HTCI Ultimate Client, HTCI will dispose the Offer Shares 
on the secondary market and the HTCI Ultimate Client will receive a final settlement amount in cash in 
accordance with the terms and conditions of the HT Back-to-back TRS and the Huatai TRS which should 
have taken into account all the economic returns or economic loss in relation to the Offer Shares. If upon 
the maturity of the Huatai TRS, the HTCI Ultimate Client intends to extend the investment period, subject 
to further agreement between HTSC and the relevant HTCI Ultimate Client, the term of the Huatai TRS 
could be extended by way of a new issuance or a tenor extension. Accordingly, HTSC will extend the term 
of the HT Back-to-back TRS by way of a new issuance or a tenor extension.
HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through the 
economic exposure to the HTCI Ultimate Client, being onshore clients placing Huatai TRS orders with 
HTSC in connection with the IPO of the Company. HTCI will not exercise the voting rights of the Offer 
Shares during the tenor of the HT Back-to-back TRS.
During the life of the Huatai TRS and HT Back-to-back TRS, HTCI may continue to hold the Offer Shares 
in its custodian account, or to hold some or all of the Offer Shares in a prime brokerage account for stock 
borrowing purposes, where HTCI will lend out its holding of underlying Offer Shares in the form of stock 
borrowing loans consistent with market practice to lower its finance costs, provided that HTCI has the 
ability to call back the Offer Shares on loan at any time in order to satisfy its obligations under the HT 
Back-to-back TRS to ensure the economic interests are ultimately passed to the HTCI Ultimate Client.

<<<PAGE 26>>>
– 26 –
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock 
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for 
the contents of this announcement, make no representation as to its accuracy or completeness and expressly 
disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. Potential investors should read the Prospectus for detailed information 
about the Company and the Global Offering described below before deciding whether or not to invest in the 
Offer Shares.
This announcement is not for release, publication or distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for 
securities in the United States or in any other jurisdiction. The Offer Shares have not been and will not be 
registered under the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities 
Act”) or securities law of any state or other jurisdiction of the United States and may not be offered, sold, 
pledged or transferred within the United States, except in transactions exempt from, or not subject to, the 
registration requirements of the U.S. Securities Act. There will be no public offer of the Offer Shares in the 
United States. The Offer Shares are being offered and sold outside the United States in offshore transactions 
in reliance on Regulation S under the U.S. Securities Act.
*	
Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators 
(for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of 
any of the events set out in the section headed “Underwriting – Underwriting Arrangements and Expenses 
– Hong Kong Public Offering – Grounds of Termination” in the Prospectus at any time prior to 8:00 a.m. 
(Hong Kong time) on the Listing Date.
PUBLIC FLOAT AND FREE FLOAT
Pursuant to Rule 19A.13A of the Listing Rules, assuming that the Over-allotment Option is not exercised, based 
on the Offer Price of HK$26.39 per Offer Share, the expected market capitalisation of the Company upon the 
Listing is HK$10.8 billion, and the minimum prescribed public float percentage applicable to our Shares is 
15%. Immediately after the completion of the Global Offering, assuming that the Over-allotment Option is not 
exercised, 224,908,641 H Shares, representing approximately 54.95% of the issued share capital of our Company, 
will count towards the public float, thereby satisfying the minimum percentage requirement in compliance with 
Rule 19A.13A(1) of the Listing Rules.
Based on the Offer Price of HK$26.39 per H Share, the Company will satisfy the free float requirement under 
Rule 19A.13C(1) of the Listing Rules. 
The Directors confirm that, immediately following the completion of the Global Offering: (i) no placee will, 
individually, be placed more than 10% of the enlarged issued share capital of the Company; (ii) there will not 
be any new substantial Shareholder (as defined in the Listing Rules) of the Company; (iii) the three largest 
public shareholders of the Company do not hold more than 50% of the H Shares in public hands at the time of 
the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 
Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.

<<<PAGE 27>>>
– 27 –
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, 20 May 2026 (Hong 
Kong time), provided that the Global Offering has become unconditional and the right of termination described 
in the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering 
– Grounds of Termination” in the Prospectus has not been exercised. Investors who trade the H Shares on the 
basis of publicly available allocation details prior to the receipt of H Share certificates or prior to the H Share 
certificates becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Wednesday, 20 May 2026 
(Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange will commence at 9:00 a.m. 
on Wednesday, 20 May 2026 (Hong Kong time). The H Shares will be traded in board lots of 100 H Shares each, 
and the stock code of the H Shares will be 7688.
By order of the Board
Shanghai Top Numerical Control Technology Co., Ltd.
Dr. Wang Yuhan
Chairman and Executive Director
Hong Kong, 19 May 2026
Directors of the Company named in the application to which this announcement relates are: (i) Dr. Wang Yuhan, 
Mr. Li Yuhao and Mr. Yao Bin as executive directors of the Company; (ii) Mr. Li Qingfeng and Mr. Li Yonghao 
as non-executive directors of the Company; and (iii) Dr. Yang Jianguo, Dr. Feng Hutian and Ms. Liu Yueheng as 
independent non-executive directors of the Company.
