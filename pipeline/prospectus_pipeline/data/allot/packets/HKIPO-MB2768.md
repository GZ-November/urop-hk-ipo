# 配发结果公告抽取任务：2768.HK Qingdao Gon Technology Co., Ltd. - H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**03/02/2026 22:56**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0203/2026020302602.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2768.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined herein, capitalized terms in this announcement shall have the same meanings as those defined 
in the prospectus dated 27 January 2026 (“Prospectus”) issued by Qingdao Gon Technology Co., Ltd. (青島國恩科
技股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an offer or an invitation to induce an offer 
by any person to acquire, purchase or subscribe for securities of the Company. This announcement is not a prospectus. 
Potential investors should read the Prospectus for detailed information about the Company, the Hong Kong Public 
Offering and the International Offering described below before deciding whether or not to invest in the Offer Shares.
This announcement does not constitute an offer to sell or the solicitation of an offer to buy nor shall there be any sale 
of Offer Shares in any jurisdiction in which such offer, solicitation or sales would be unlawful. This announcement is 
not for release, publication or distribution, directly or indirectly, in or into the United States for sale or solicitation to 
purchase or subscribe for securities in the United States or any other jurisdictions. The Offer Shares have not been, 
and will not be, registered under the United States Securities Act 1933, as amended or supplemented from time to 
time (the “U.S. Securities Act”) or any state securities law of the United States and may not be offered, sold, pledged, 
transferred or delivered within the United States, except pursuant to an exemption from, or in a transaction not subject 
to, the registration requirements of the U.S. Securities Act and state securities laws of the United States. The Offer 
Shares are being offered and sold outside of the United States as offshore transactions in accordance with Regulation 
S under the U.S. Securities Act and the applicable laws of each jurisdiction where those offers and sales occur. There 
will not be and is not currently intended to be any public offering of securities of the Company in the United States.
Potential investors of the Offer Shares should note that the Sole Overall Coordinator (for itself and on behalf of the 
other Hong Kong Underwriters) shall be entitled to terminate the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in “Underwriting – Underwriting Arrangements and Expenses 
– Hong Kong Public Offering – Grounds for Termination” in the Prospectus at any time at or prior to 8:00 a.m. (Hong 
Kong time) on the Listing Date (which is currently expected to be on 4 February 2026).

<<<PAGE 2>>>
2
QINGDAO GON TECHNOLOGY CO., LTD.
青島國恩科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under
 the Global Offering
:
30,000,000 H Shares
Number of Hong Kong Offer Shares
:
 3,000,000 H Shares
Number of International Offer Shares
:
27,000,000 H Shares
Final Offer Price
:
 HK$36.00 per H Share plus brokerage 
 of 1%, SFC transaction levy of 
 0.0027%, Stock Exchange trading fee 
 of 0.00565% and AFRC transaction 
 levy of 0.00015% (payable in full on 
 application in Hong Kong dollars and 
 subject to refund)
Nominal value
:
 RMB1.00 per H Share
Stock code
: 2768
Sole Sponsor, Sponsor-Overall Coordinator, Joint Global Coordinator,
Joint Bookrunner and Joint Lead Manager
Joint Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
Qingdao Gon Technology Co., Ltd.
青島國恩科技股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated 27 January 2026 (the “Prospectus”) issued by 
Qingdao Gon Technology Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
2768
Stock short name
GON TECHNOLOGY
Dealings commencement date
4 February 2026*
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$36.00
Offer Price Range
HK$34.00 – HK$42.00
Offer Shares and Share Capital
Number of Offer Shares
30,000,000
Number of Offer Shares in Hong Kong Public Offering
3,000,000
Number of Offer Shares in International Offering
27,000,000
Number of issued Shares upon Listing
301,250,000
Proceeds
Gross proceeds (Note)
HK$1,080.0 million
Less: Estimated listing expenses payable based on final Offer Price
HK$(79.6) million
Net proceeds
HK$1,000.4 million
Note: Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus dated 27 
January 2026.

<<<PAGE 4>>>
4
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
171,047
No. of successful applications
14,819
Subscription level
2,251.85 times
Reallocation
No
No. of Offer Shares initially available under the Hong Kong Public 
Offering
3,000,000
No. of Offer Shares reallocated from the International Offering
0
Final no. of Offer Shares under the Hong Kong Public Offering
3,000,000
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering (Note)
10%
Note:
1. 
For details of the final allocation of Shares to the Hong Kong Public Offering, investors can 
refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
88
Subscription level
10.03 times
No. of Offer Shares initially available under the International 
Offering
27,000,000
No. of Offer Shares reallocated to the Hong Kong Public Offering
0
Final no. of Offer Shares under the International Offering
27,000,000
% of Offer Shares under the International Offering to the Global 
Offering
90%

<<<PAGE 5>>>
5
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) 
consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants (the “Guide”) 
to permit the Company to, among other things, allocate further H Shares in the International 
Offering to the Cornerstone Investors and/or their close associates and (b) a consent under 
paragraph 1C(1) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the 
Stock Exchange to permit H Shares in the International Offering to be placed to certain connected 
clients, (i) none of the Offer Shares subscribed by the placees and the public have been financed 
directly or indirectly by the Company, any of the Directors, chief executive of the Company, 
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company or any of 
its subsidiaries or their respective close associates; and (ii) none of the placees and the public who 
have purchased the Offer Shares are accustomed to taking instructions from the Company, any of 
the Directors, chief executive of the Company, Controlling Shareholders, substantial Shareholders, 
existing Shareholders of the Company or any of its subsidiaries or their respective close associates 
in relation to the acquisition, disposal, voting or other disposition of H Shares registered in his/her/
its name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of Offer 
Shares 
Allocated Note 1
% of total issued 
H Shares after 
the Global 
Offering Note 2 & 3
% of total issued 
share capital in 
the Company 
after the Global 
Offering Note 3
Existing 
shareholders 
or their close 
associates
Nice First Investments Limited 
 (“Nice First”)
1,072,000
3.57%
0.36%
No
SLD International Enterprises 
 Limited (“SLD”)
2,222,200
7.41%
0.75%
No
Cheng A International Co., Limited
498,000
1.66%
0.17%
No
Shenwan Hongyuan Securities 
 Co., Ltd.
216,400
0.72%
0.07%
No
First Seafront Fund Series SPC
3,055,400
10.18%
1.04%
No
New Harvest Wealth Securities 
 Company Limited
416,600
1.39%
0.14%
No
Luminous Horizon Limited
1,111,000
3.70%
0.38%
No
Fullgoal Asset Management (HK) 
 Limited (“Fullgoal HK”)
277,600
0.93%
0.09%
No

<<<PAGE 6>>>
6
Notes:
1. 
Excluding Offer Shares allotted to Cornerstone Investors and/or their close associates with consent under Chapter 4.15 of the Guide (if 
any).
2. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the Global 
Offering.
3. 
Not taking into account of the 6,250,000 treasury shares.
4. 
In addition to the Offer Shares subscribed for as Cornerstone Investors, Nice First Investment Limited, SLD International Enterprises 
Limited, Shenwan Hongyuan Securities Co., Ltd., New Harvest Wealth Securities Company Limited and Fullgoal HK and/or their close 
associates, where applicable, were allocated further Offer Shares as placees in the International Offering. Please refer to the section 
headed “Allotment Results Details – International Offering – Allotees with Waivers/Consents Obtained” in this announcement for further 
details. Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-up as indicated below. For details, please refer 
to the section headed “Lock-up Undertakings – Cornerstone Investors” in this announcement.

<<<PAGE 7>>>
7
Allottees with Waivers/Consents Obtained
Investor
No. of 
Offer Shares 
Allocated 
% of total issued 
H Shares after 
the Global 
Offering Notes 4 & 5
% of total issued 
share capital 
in the Company 
after the Global 
Offering Note 5
Relationship
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide in relation to allocations of further H 
Shares to Cornerstone Investors and/or their close associates
Nice First Investments Limited
1,063,000
3.54%
0.36%
Same entity as the 
 Cornerstone Investor
Zhou Wanyuan
2,361,000
7.87%
0.80%
Close associate of the 
 Cornerstone 
 Investor(3)
Shenwan Hongyuan 
 Securities Co., Ltd.
833,000
2.78%
0.28%
Same entity as the 
 Cornerstone Investor
New Harvest Wealth 
 Securities Company Limited
833,000
2.78%
0.28%
Same entity as the 
 Cornerstone Investor
Fullgoal HK
416,000
1.39%
0.14%
Same entity as the 
 Cornerstone Investor
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide in relation 
to allocations to connected clients Note 2
CITIC Securities International 
 Capital Management Limited
56,000
0.19%
0.02%
Connected Client as a 
placee
GF Securities Asset 
 Management (Guangdong) 
 Co., Ltd. Note 6
1,049,400
3.5%
0.36%
Connected Client 
as a placee and a 
Cornerstone Investor
GF Global Capital Limited
555,000
1.85%
0.19%
Connected Client as a 
placee
Bosera Asset Management 
 (International) Co., Limited
416,000
1.39%
0.14%
Connected Client as a 
placee
China Asset Management 
 (Hong Kong) Limited
13,600
0.05%
0.005%
Connected Client as a 
placee
CMBI (Singapore) Pte. Limited
2,200
0.01%
0.0007%
Connected Client as a 
placee
Fullgoal HK Note 7
693,600
2.31%
0.24%
Connected Client 
as a placee and a 
Cornerstone Investor
GF International Investment 
 Management Limited
750,000
2.50%
0.25%
Connected Client as a 
placee
E Fund Management Co., Ltd.
444,000
1.48%
0.15%
Connected Client as a 
placee
E Fund Management (Hong 
Kong) Co., Ltd.
111,000
0.37%
0.04%
Connected Client as a 
placee

<<<PAGE 8>>>
8
Notes:
1. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the number of Offer Shares 
allocated to the investors as placees in the International Offering. For allocations of Offer Shares to the relevant investors as Cornerstone 
Investors, please refer to the section headed “Allotment Results Details – International Offering – Cornerstone Investors” in this 
announcement. For details of the consent under paragraph 18 of Chapter 4.15 of the Guide in relation to allocations of further H Shares 
to the Cornerstone Investors and/or their close associates, please refer to the section headed “Others/Additional Information – Allocations 
of Offer Shares to the Cornerstone Investors and their Close Associates with a Consent under paragraph 18 of Chapter 4.15 of the Guide” 
in this announcement.
2. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide in relation to allocations to 
connected clients, please refer to the section headed “Others/Additional Information – Placing to Connected Clients with a Consent under 
Paragraph 1C(1) of the Placing Guidelines” in this announcement.
3. 
SLD International is a cornerstone investor. SLD International is owned as to Shen Zhenyu (“Ms. Shen”). Ms. Shen’s husband, Zhou 
Wanyuan (who is Ms. Shen’s close associate) is an anchor investor under the International Offering.
4. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the Global 
Offering.
5. 
Not taking into account of the 6,250,000 treasury shares.
6. 
Shenwan Hongyuan Securities Co., Ltd. (“SWHY Securities”) is a cornerstone investor of the Company. SWHY Securities’ investment 
into the Company was completed through QDII program in the PRC, of which it has engaged GF Securities Asset Management 
(Guangdong) Co., Ltd.
7. 
Fullgoal HK is also allocated with 277,600 Offer Shares (which amounts to approximately 0.72% of the Offer Shares and 0.073% of the 
issued share capital in the Company after the Global Offering, respectively), in its capacity as a cornerstone investor.

<<<PAGE 9>>>
9
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon 
Listing (Note 4)
Last day subject 
to the lock-up 
undertakings (Notes 1, 2)
Wang Aiguo
126,000,000
–
41.83%
3 February 2027
Xu Bo (Note 3) 
9,000,000
–
2.98%
3 February 2027
Xinghao Investment
18,000,000
–
5.98%
3 February 2027
Notes:
1. 
In accordance with the relevant Listing Rule/guidance materials, the required lock-up for the first six-month period ends on 3 August 
2026 and for the second six-month period ends on 3 February 2027.
2. 
According to the PRC Company Law, all the Shares held by existing Shareholders (including the Controlling Shareholders) prior to the 
Global Offering are subject to a lock-up period of one year from the Listing Date.
3. 
As of the Latest Practicable Date, Xinghao Investment directly held 18,000,000 A Shares and Xinghao Investment is controlled and held 
as to 83.30% by Ms. Xu. By virtue of the SFO, Ms. Xu is deemed to be interested in all the Shares held by Xinghao Investment.
4. 
Not taking into account of the 6,250,000 treasury shares.

<<<PAGE 10>>>
10
Cornerstone Investors
Name
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing Note 1 & 3
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings Note 2 & 3
Nice First Investments Limited
1,072,000
3.57%
0.36%
3 August 2026
SLD International Enterprises Limited
2,222,200
7.41%
0.75%
3 August 2026
Cheng A International Co., Limited
498,000
1.66%
0.17%
3 August 2026
Shenwan Hongyuan Securities  
Co., Ltd.
216,400
0.72%
0.07%
3 August 2026
First Seafront Fund Series SPC
3,055,400
10.18%
1.04%
3 August 2026
New Harvest Wealth Securities 
Company Limited
416,600
1.39%
0.14%
3 August 2026
Luminous Horizon
1,111,000
3.70%
0.38%
3 August 2026
Fullgoal Asset Management (HK) 
 Limited
277,600
0.93%
0.09%
3 August 2026
Subtotal
8,869,200
29.56%
3.01%
Notes:
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the Global Offering.
2. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on 3 August 2026. The Cornerstone Investors will 
cease to be prohibited from disposing of or transferring H Shares subscribed pursuant to the relevant cornerstone investment agreements after the 
indicated date.
3. 
Not taking into account of the 6,250,000 treasury shares.
PLACEE CONCENTRATION ANALYSIS
Placees
Number of 
H Shares 
allotted
Allotment as % 
of International 
Offering
Allotment as
% of total 
Offer Shares
Number of 
Shares held 
upon Listing
% of total issued 
share capital 
upon Listing
Top 1
4,583,200
16.97%
15.28%
4,583,200
15.28%
Top 5
14,772,600
54.71%
49.24%
14,772,600
49.24%
Top 10
20,958,600
77.62%
69.86%
20,958,600
69.86%
Top 25
26,451,400
97.97%
88.17%
26,451,400
88.17%
Note:
1. 
Ranking of placees is based on the number of H Shares allotted to the placees

<<<PAGE 11>>>
11
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders (1)
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
% of 
total issued 
H Shares 
capital upon
Listing
Number of 
Shares held 
upon Listing
Top 1
4,583,200
16.97%
15.28%
4,583,200
15.28%
4,583,200
Top 5
14,772,600
54.71%
49.24%
14,772,600
49.24%
14,772,600
Top 10
20,958,600
77.62%
69.86%
20,958,600
69.86%
20,958,600
Top 25
26,451,400
97.97%
88.17%
26,451,400
88.17%
26,451,400
Note:
1. 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders (1)
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
Number 
of H Shares 
held upon 
Listing
Number 
of Shares 
held upon 
Listing
% of total 
issued share 
capital upon
Listing
Top 1
0
0.00%
0.00%
0
126,000,000
42.71%
Top 5
0
0.00%
0.00%
0
166,890,754
55.57%
Top 10
6,805,200
25.20%
22.68%
6,805,200
192,074,904
65.11%
Top 25
17,548,600
64.99%
58.50%
17,548,600
230,214,397
78.04%
Notes:
1. 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 12>>>
12
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, 171,047 valid applications 
made by the public will be conditionally allocated on the basis set out below:
Approximate
percentage
allotted of the
Number of
total number of
H Shares Number of valid
H Shares
applied for
applications
Basis of allocation/ballot
applied for
Pool A
200
60,113
1,202 out of 60,113 to receive 200 Shares
2.00%
400
10,905
284 out of 10,905 to receive 200 Shares
1.30%
600
8,297
222 out of 8,297 to receive 200 Shares
0.89%
800
3,340
94 out of 3,340 to receive 200 Shares
0.70%
1,000
17,387
490 out of 17,387 to receive 200 Shares
0.56%
2,000
8,923
269 out of 8,923 to receive 200 Shares
0.30%
3,000
3,605
121 out of 3,605 to receive 200 Shares
0.22%
4,000
2,973
108 out of 2,973 to receive 200 Shares
0.18%
5,000
2,469
96 out of 2,469 to receive 200 Shares
0.16%
6,000
1,821
77 out of 1,821 to receive 200 Shares
0.14%
7,000
1,437
65 out of 1,437 to receive 200 Shares
0.13%
8,000
1,356
65 out of 1,356 to receive 200 Shares
0.12%
9,000
1,024
52 out of 1,024 to receive 200 Shares
0.11%
10,000
4,871
255 out of 4,871 to receive 200 Shares
0.10%
15,000
3,018
215 out of 3,018 to receive 200 Shares
0.09%
20,000
2,967
224 out of 2,967 to receive 200 Shares
0.08%
25,000
2,159
191 out of 2,159 to receive 200 Shares
0.07%
30,000
1,604
163 out of 1,604 to receive 200 Shares
0.07%
35,000
1,184
136 out of 1,184 to receive 200 Shares
0.07%
40,000
1,384
175 out of 1,384 to receive 200 Shares
0.06%
45,000
1,098
154 out of 1,098 to receive 200 Shares
0.06%
50,000
2,024
304 out of 2,024 to receive 200 Shares
0.06%
60,000
1,554
272 out of 1,554 to receive 200 Shares
0.06%
70,000
1,317
263 out of 1,317 to receive 200 Shares
0.06%
80,000
1,237
279 out of 1,237 to receive 200 Shares
0.06%
90,000
973
244 out of 973 to receive 200 Shares
0.06%
100,000
5,463
1,480 out of 5,463 to receive 200 Shares
0.05%
Total
154,503
Total number of Pool A successful applicants: 7,500

<<<PAGE 13>>>
13
Approximate
percentage
allotted of the
Number of
total number of
H Shares Number of valid
H Shares
applied for
applications
Basis of allocation/ballot
applied for
Pool B
150,000
7,258
2,417 out of 7,258 to receive 200 Shares
0.04%
200,000
2,390
882 out of 2,390 to receive 200 Shares
0.04%
250,000
1,520
616 out of 1,520 to receive 200 Shares
0.03%
300,000
1,039
459 out of 1,039 to receive 200 Shares
0.03%
350,000
614
294 out of 614 to receive 200 Shares
0.03%
400,000
548
282 out of 548 to receive 200 Shares
0.03%
450,000
468
258 out of 468 to receive 200 Shares
0.02%
500,000
677
398 out of 677 to receive 200 Shares
0.02%
600,000
503
332 out of 503 to receive 200 Shares
0.02%
700,000
285
209 out of 285 to receive 200 Shares
0.02%
800,000
234
189 out of 234 to receive 200 Shares
0.02%
900,000
152
134 out of 152 to receive 200 Shares
0.02%
1,000,000
153
146 out of 153 to receive 200 Shares
0.02%
1,100,000
109
200 Shares
0.02%
1,200,000
58
200 Shares plus 8 out of 58 to receive 
 additional 200 Shares
0.02%
1,300,000
49
200 Shares plus 9 out of 49 to receive 
 additional 200 Shares
0.02%
1,400,000
45
200 Shares plus 12 out of 45 to receive 
 additional 200 Shares
0.02%
1,500,000
442
200 Shares plus 152 out of 442 to receive 
 additional 200 Shares
0.02%
Total
16,544
Total number of Pool B successful applicants: 7,319
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.

<<<PAGE 14>>>
14
OTHERS/ADDITIONAL INFORMATION
Allocations of Offer Shares to the Cornerstone Investors and their Close Associates with a 
Consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph 
18 of Chapter 4.15 of the Guide to permit Cornerstone Investors and/or their close associates to 
subscribe for further Offer Shares as placees in the International Offering on the conditions as set 
out below:
(i) 
the final offering size of the proposed listing (excluding any over-allocation) will be of a 
total value of at least HK$1 billion;
(ii) each Director, chairman, and Controlling Shareholder has confirmed that no securities have 
been allocated to them or their respective close associates under the Size-based Exemption (as 
defined in the Guide);
(iii) the Company will comply with the public float requirement under Rule 19A.13A(2) and the 
free float requirement under Rule 8.08A of the Listing Rules; and
(iv) details of the allocation to such investors under the Size-based Exemption will be disclosed 
in the allotment results announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to Cornerstone Investors, please refer to the section 
headed “Allotment Results Details – International Offering – Allotees with Waivers/Consents 
Obtained” in this announcement.
Placing to Connected Clients with a Consent under Paragraph 1C(1) of the Placing Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines. Details of the placement to connected 
clients are set out below. The Company has applied to the Stock Exchange for, and the Stock 
Exchange has granted, consents under paragraph 1C(1) of the Placing Guidelines to permit 
Connected Clients to subscribe for Offer Shares as placees in the International Offering on the 
conditions set out below.

<<<PAGE 15>>>
15
In respect of the placing to the Connected Clients on a non-discretionary basis:
(i) 
no preferential treatment has been given, nor will be given, to each of the Connected Clients 
by virtue of its relationship with the relevant Connected Distributor in any allocation of Offer 
Shares in the International Offering;
(ii) the Offer Shares to be allocated to the Connected Clients will be held on behalf of 
independent third parties;
(iii) the details of the allocation (including the name and the relevant Connected Client’s 
relationship, the number of Shares allotted to and the percentage of Shares allocated) to the 
relevant Connected Clients will be disclosed in the allotment results announcement of the 
Company;
(iv) based on the discussions between the Company and the Joint Overall Coordinators and the 
confirmations provided to the Stock Exchange by the Company, the Connected Distributors 
and the Connected Clients, to the best of their knowledge and belief, they have no reasons to 
believe that preferential treatment has been given to each of the Connected Clients by virtue 
of its relationship with the relevant Connected Distributor in any allocation of Offer Shares 
in the International Offering;
(v) 
identities of ultimate beneficial owners of the securities, or where applicable, details of the 
structured products under which the subscription by the Connected Clients was made, would 
be confirmed to the Stock Exchange
(vi) the Connected Clients have agreed to furnish such information (to the extent relating to them) 
to the Stock Exchange and the Sole Sponsor as and when it is required for the purpose of 
facilitating the Stock Exchange’s vetting process, and consent to the disclosure of the details 
of the allocation in the allotment results announcement to be published by the Company
In respect of the placing to the Connected Clients on a discretionary basis:
no preferential treatment has been given, nor will be given, to each of the Connected Clients by 
virtue of its relationship with the relevant Connected Distributor in any allocation of Offer Shares 
in the International Offering
(i) 
the Offer Shares to be allocated to the Connected Clients will be held on behalf of 
independent third parties;
(ii) details of the allocation (including the name and the relevant Connected Client’s relationship, 
the number of Shares allotted to and the percentage of Shares allocated) to the relevant 
Connected Clients will be disclosed in the allotment results announcement of the Company;

<<<PAGE 16>>>
16
(iii) based on discussions between the Company and the Joint Overall Coordinators and the 
confirmations provided to the Stock Exchange by the Company, the Connected Distributors 
and the Connected Clients, to the best of their knowledge and belief, they have no reasons to 
believe that preferential treatment has been given to each of the Connected Clients by virtue 
of its relationship with the relevant Connected Distributor in any allocation of Offer Shares 
in the International Offering;
(iv) to the best of the Joint Overall Coordinators’ knowledge and belief, they have no reason 
to believe that the relevant Connected Client received any preferential treatment in the 
allocation of securities in the IPO as a cornerstone investor by virtue of its relationship with 
the relevant Connected Distributor other than the preferential treatment of assured entitlement 
under a cornerstone investment following the principles set out in Chapter 4.15 of the Guide, 
and details of the allocation will be disclosed in the prospectus and the allotment results 
announcement;
(v) 
the relevant Connected Distributor has not participated in, and will not participate in, the 
decision-making process or relevant discussions relating to allocation of securities to the 
relevant Connected Client among the Company, the Joint Overall Coordinators and the 
underwriters as to whether securities should be allocated to the relevant Connected Client;
(vi) for CMBI SG which is not a collective investment scheme authorised by the SFC or expected 
to hold the securities on behalf of such scheme, the background and details of such scheme 
has been provided to the Stock Exchange.
(vi) the cornerstone investment agreement with the relevant Connected Client does not contain 
any material terms which are more favourable to the relevant Connected Client than those 
in other cornerstone investment agreements and no preferential treatment has been, nor will 
be, given to the relevant Connected Client other than the preferential treatment of assured 
entitlement under a cornerstone investment following the principles set out in Chapter 4.15 of 
the Guide

<<<PAGE 17>>>
17
Details of the placement to the Connected Clients are set out below:
No.
Connected 
Distributors
Connected Client
Relationship 
with the 
Connected 
Distributor(s)
Basis of holding 
securities
Number 
of Offer 
Shares 
subscribed
Percentage 
to total 
Offer 
Shares 
under 
Global 
Offering (Note 11)
Percentage 
to total 
issued 
Shares 
immediately 
upon the 
completion 
of Global 
Offering (Note 11)
1.
CLSA
CITIC Securities 
International Capital 
Management Limited 
(“CSICM”)
See Note 1
Non-discretionary
56,000
0.19%
0.019%
2.
CLSA
China Asset Management 
(Hong Kong) Limited 
(“China AMC HK”)
See Note 2
Discretionary
13,600
0.05%
0.005%
3.
GF Securities (Hong 
Kong) Brokerage
GF Securities Asset 
Management 
(Guangdong) Co., Ltd. 
(“GF Securities Asset 
Management”)
See Note 3
Non-discretionary
27,000
0.09%
0.009%
4.
GF Securities (Hong 
Kong) Brokerage
GF Global Capital Limited 
(“GFGC”)
See Note 4
Non-discretionary
555,000
1.85%
0.188%
5.
GF Securities (Hong 
Kong) Brokerage
GF International 
Investment 
Management Limited 
(“GF International 
Investment”)
See Note 5
Discretionary
750,000
2.50%
0.254%
6.
CMS and CMBI 
Connected 
Distributors
Bosera Asset Management 
(International) Co., 
Limited (“Bosera Asset 
Management”)
See Note 6
Discretionary
416,000
1.39%
0.141%

<<<PAGE 18>>>
18
No.
Connected 
Distributors
Connected Client
Relationship 
with the 
Connected 
Distributor(s)
Basis of holding 
securities
Number 
of Offer 
Shares 
subscribed
Percentage 
to total 
Offer 
Shares 
under 
Global 
Offering (Note 11)
Percentage 
to total 
issued 
Shares 
immediately 
upon the 
completion 
of Global 
Offering (Note 11)
7.
CMB International 
Capital Limited 
(“CMBI”), CMB 
International 
Securities Limited 
(“CMBI Securities”) 
and CMB 
International Global 
Market Limited 
(“CMBI Global 
Markets”)
CMBI (Singapore) Pte. 
Limited (“CMBI SG”)
See Note 7
Discretionary
2,200
0.01%
0.001%
8.
GTJA
Fullgoal HK
See Note 8
Discretionary
416,000
1.39%
0.141%
9.
GF Securities 
(HongKong) 
Brokerage
E Fund Management 
Co., Ltd. (“E Fund 
Management”)
See Note 9
Discretionary
444,000
1.48%
0.15%
10.
GF Securities 
(HongKong) 
Brokerage
E Fund Management 
(Hong Kong) Co., Ltd. 
(“E Fund HK”)
See Note 10
Discretionary
111,000
0.37%
0.04%
Notes:
1. 
CSICM is a member of the same group of companies as CLSA. CSICM and CITIC Securities Company 
Limited will enter into a series of cross border OTC swap transactions (the “OTC Swaps”) with the 
investment managers (山東望水泉私募投資基金有限公司(Shandong Wangshui Private Equity Fund 
Company Limited*), 上海量派投資管理有限公司(Shanghai QuantPi Investment Limited)), who act for 
and on behalf of certain ultimate clients (collectively, the “CSICM Ultimate Clients”), pursuant to which 
CSICM will hold the Offer Shares to be subscribed for and on behalf of the investment managers on a non-
discretionary basis to hedge the OTC Swaps while the economic risks and returns of the underlying Offer 
Shares are passed to the CSICM Ultimate Clients, subject to customary fees and commissions. CSICM will 
not take part in any economic returns or bear any economic losses in relation to the Offer Shares. The OTC 
Swaps will be fully funded by the CSICM Ultimate Clients.
* For identification purpose only

<<<PAGE 19>>>
19
2. 
China AMC HK is a member of the same group of companies as CLSA and China AMC HK is therefore 
considered as a connected client of CLSA pursuant to paragraph 1B(7) of the Placing Guidelines. China AMC 
HK will hold the Offer Shares in its capacity as the discretionary fund manager managing on behalf of its 
underlying clients, each of which is an Independent Third Party.
3. 
GF Securities Asset Management is a direct wholly-owned subsidiary of GF Securities Co., Ltd. (Stock Code: 
1776) (“GF Securities”) and GF Securities (Hong Kong) Brokerage is an indirect wholly-owned subsidiary 
of GF Securities. Each of GF Securities Asset Management and GF Securities (Hong Kong) Brokerage is a 
member of the same group of companies.
GF Securities Asset Management will hold the Offer Shares as product manager on behalf of GF Asset 
Management WANXIANG No. 1 (QDII) Single Asset Management Plan (廣發資管萬享1號(QDII)單一資產
管理計劃), with the ultimate client being Shenwan Hongyuan Group Co., Ltd. (申萬宏源集團股份有限公司) 
(the “GF Securities AM Ultimate Client AMS”). Shenwan Hongyuan Securities Co., Ltd. as a cornerstone 
investor is a wholly-owned subsidiary of Shenwan Hongyuan Group Co., Ltd. (Stock Code: 6806).
4. 
Both GF Securities (Hong Kong) Brokerage and GFGC is an indirect wholly-owned subsidiary of GF 
Securities. Each of GF Securities (Hong Kong) Brokerage and GFGC is a member of the same group of 
companies.
GFGC is to invest on non-discretionary basis. GFGC and GF Securities will enter into a series of cross border 
delta one OTC swap transactions (the “OTC Swaps”) with each other and the ultimate clients (the “GFGC 
Ultimate Clients”), pursuant to which GFGC will hold the Offer Shares on a non-discretionary basis to 
hedge the OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed to the 
GFGC Ultimate Clients, subject to customary fees and commissions. The OTC swaps will be fully funded by 
the GFGC Ultimate Clients. During the terms of the OTC Swaps, all economic returns of the Offer Shares 
subscribed by GFGC will be passed to the GFGC Ultimate Clients and all economic loss shall be borne by 
the GFGC Ultimate Clients through the OTC Swaps, and GFGC will not take part in any economic return or 
bear any economic loss in relation to the Offer Shares. The OTC Swaps are linked to the Offer Shares and 
the GFGC Ultimate Clients may request GFGC to redeem it at their own discretions, upon which GFGC shall 
dispose of the Offer Shares and settle OTC Swaps in cash in accordance with the terms and conditions of 
the OTC Swap. Despite that GFGC will hold the legal title of the Offer Shares by itself, it will not exercise 
the voting rights attaching to the relevant Offer Shares during the terms of the OTC Swaps according to its 
internal policy.
GFGC will hold the Offer Shares for and on behalf of one ultimate client on non-discretionary basis, namely 
中金金嘉1號集合資產管理計劃(with no ultimate beneficial owner holding 30% or more of the interests).
5. 
GF Securities (Hong Kong) Brokerage is an indirect wholly-owned subsidiary of GF Securities and GF 
International Investment is an indirect non-wholly owned subsidiary of GF Securities. Each of GF Securities 
(Hong Kong) Brokerage and GF International Investment is a member of the same group of companies.

<<<PAGE 20>>>
20
6. 
Bosera Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager 
managing three sub-funds (namely, Bosera China New Opportunities Fund SP, Bosera Growth Premium 
Global Equity Strategy Fund SP and Bosera Global Select Equity Fund SP) on behalf of its underlying client.
Bosera Asset Management is held as to 55% by Bosera Asset Management Co., Ltd. and 45% by China 
Merchants Fund Management Co., Ltd.. China Merchants Securities Co., Ltd. currently holds 49% of the 
equity interest of Bosera Asset Management Co., Ltd. and 45% of the equity interest of China Merchants 
Fund Management Co., Ltd. CMS is a wholly-owned subsidiary of China Merchants Securities Co., Ltd.. 
China Merchants Bank Co., Ltd. currently holds 55% of the equity interest of China Merchants Fund 
Management Co., Ltd. Each of the CMBI Connected Distributors is a indirectly wholly-owned subsidiary 
of China Merchants Bank Co., Ltd. Therefore, Bosera Asset Management is a member of same group of 
companies as CMS and CMBI Connected Distributors.
7. 
CMBI is one of the Joint Bookrunners of the Proposed Listing. Each of CMBI Securities and CMBI Global 
Markets is a distributor of the Global Offering. CMBI, CMBI Securities and CMBI Global Markets are 
indirectly wholly-owned subsidiaries of CMB International Capital Holdings Corporation Limited. CMBI SG 
is a member of the same group with CMBI Connected Distributors. Accordingly, CMBI SG is considered as a 
“connected client” of CMBI Connected Distributors pursuant to paragraph 1B(7) of the Placing Guidelines.
8. 
Fullgoal HK and GTJA are indirectly owned by Guotai Haitong Securities Co., Ltd.
9. 
GF Securities (Hong Kong) Brokerage is an indirect wholly-owned subsidiary of GF Securities, which in 
turn holds 22.65% of the issued share capital of E Fund Management. As of the date of this submission, 
Accordingly, E Fund Management is a member of the same group of companies as GF Securities and 
therefore is a “connected client” of GF Securities (Hong Kong) Brokerage under paragraph 1B of the Placing 
Guidelines.
10. 
GF Securities (Hong Kong) Brokerage is an indirect wholly-owned subsidiary of GF Securities, which in turn 
holds 22.65% of the issued share capital of E Fund Management. As of the date of this submission, E Fund 
HK is a wholly-owned subsidiary of E Fund Management. Accordingly, E Fund Management and E Fund HK 
are members of the same group of companies as GF Securities and therefore is a “connected client” of GF 
Securities (Hong Kong) Brokerage under paragraph 1B of the Placing Guidelines.
11. 
Not taking into account of the 6,250,000 treasury shares.

<<<PAGE 21>>>
21
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
as amended (the “U.S. Securities Act”). The securities may not be offered or sold in the United 
States except pursuant to an exemption from the registration requirements of the U.S. Securities 
Act and in compliance with any applicable state securities laws, or outside the United States 
unless in compliance with Regulation S under the U.S. Securities Act. There will be no public 
offer of securities in the United States.
The Offer Shares are being offered and sold outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated 27 January 2026 issued by Qingdao Gon 
Technology Co., Ltd. for detailed information about the Global Offering described below before 
deciding whether or not to invest in the H Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Sole Overall Coordinator (for itself 
and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations 
under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of 
any of the events set out in the paragraph headed “Underwriting – Underwriting Arrangements 
and Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus at any 
time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be 
on 4 February 2026).

<<<PAGE 22>>>
22
PUBLIC FLOAT AND FREE FLOAT
Immediately upon the completion of the Global Offering, the number of H Shares held in public 
hands represent 10.17% of the total issued share capital of the Company (excluding treasury 
Shares), which is higher than the prescribed percentage of H Shares required to be held in public 
hands of 10.00% under Rule 19A.13A(2)(a) of the Listing Rules.
The Directors confirm that, immediately upon the completion of the Global Offering, (i) no placee 
will, individually, be placed more than 10% of the enlarged issued share capital of the Company 
immediately after the Global Offering; (ii) there will not be any new substantial Shareholder 
immediately after the Global Offering; (iii) the public hands at the time of the Listing is in 
compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 
Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the H Shares of the Company at the time of Listing. Based on the 
final Offer Price of HK$36.00 per H Share, the Company confirms the free float requirement under 
Rule 19A.13C(2)(a) of the Listing Rules.
COMMENCEMENT OF DEALINGS
H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, 4 
February 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus has not been exercised. Investors who trade H Shares prior to the receipt of H Share 
certificates or prior to the H Share certificates becoming valid evidence of title do so entirely at 
their own risk.
Assuming that the Hong Kong Public Offering becomes unconditional at or before 8:00 a.m. in 
Hong Kong on Wednesday, 4 February 2026, it is expected that dealings in the H Shares on the 
Stock Exchange will commence at 9:00 a.m. on Wednesday, 4 February 2026. The H Shares will 
be traded in board lots of 200 H Shares each and the stock code of the H Shares will be 2768.
By order of the Board
Qingdao Gon Technology Co., Ltd.
青島國恩科技股份有限公司
Mr. Wang Aiguo
Chairman and executive Director
Hong Kong, 3 February 2026
As of the date of this announcement, the board of directors of the Company comprises: (i) Mr. 
Wang Aiguo, Mr. Li Zonghao, Ms. Li Huiying and Mr. Han Bo as executive directors; and (ii) Mr. 
Wang Yaping, Mr. Sun Jianqiang and Ms. Hong Ting as independent non-executive directors.
