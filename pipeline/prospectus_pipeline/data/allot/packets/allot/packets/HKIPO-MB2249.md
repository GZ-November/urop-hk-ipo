# 配发结果公告抽取任务：2249.HK NEXCHIP SEMICONDUCTOR (CHINA) LIMITED - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**09/07/2026 21:56**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0709/2026070901289.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2249.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for 
the Offer Shares in the United States or in any other jurisdictions. The Offer Shares have not been, and will not 
be, registered under the United States Securities Act of 1933 as amended from time to time (the “U.S. Securities 
Act”) or securities law of any state or other jurisdiction of the United States. The Offer Shares may not be 
offered, sold, pledged or otherwise transferred within the United States, except pursuant to an exemption from, 
or in a transaction not subject to, the registration requirements of the U.S. Securities Act, and in compliance 
with any applicable state securities laws. The Offer Shares are being offered and sold outside the United States 
in offshore transactions in reliance on Regulation S under the U.S. Securities Act. There will be no public offer 
of the Offer Shares in the United States.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. This announcement is not a prospectus. Potential investors should read 
the prospectus dated June 30, 2026 (the “Prospectus”) issued by Nexchip Semiconductor Corporation (合肥
晶合集成電路股份有限公司) (the “Company”) for detailed information about the Global Offering described 
below before deciding whether or not to invest in the H Shares thereby being offered. Any investment decision in 
relation to the Offer Shares should be taken solely in reliance on the information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as 
those defined in the Prospectus.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited, 
as stabilizing manager (the “Stabilizing Manager”) (or its affiliates or any person acting for it), on behalf of 
the Underwriters, to the extent permitted by the applicable laws and regulatory requirements of Hong Kong or 
elsewhere, may over-allocate or effect transactions with a view to stabilizing or supporting the market price 
of the H Shares at such price, in such amounts and in such manners as the Stabilizing Manager, its affiliates 
or any person acting for it may determine and at a level higher than that which might otherwise prevail for a 
limited period after the Listing Date. However, there is no obligation on the Stabilizing Manager (or its affiliates 
or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will be 
conducted at the absolute discretion of the Stabilizing Manager (or its affiliates or any person acting for it) and 
in what the Stabilizing Manager reasonably regards as the best interest of the Company, (b) may be discontinued 
at any time and (c) is required to be brought to an end within 30 days of the last day for lodging applications 
under the Hong Kong Public Offering (which is Thursday, August 6, 2026). Such stabilizing action, if taken, may 
be effected in all jurisdictions where it is permissible to do so, in each case in compliance with all applicable 
laws, rules and regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 
571 W of the Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter 571 
of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares 
for longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 
30th day after the last day for lodging applications under the Hong Kong Public Offering (which is Thursday, 
August 6, 2026). After this date, when no further stabilizing action may be taken, demand for the H Shares, and 
therefore the price of the H Shares, could fall.
Potential investors of the Offer Shares should note that the Sole Sponsor and Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under 
the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out 
in the section headed “Underwriting — Underwriting Agreements — Hong Kong Underwriting Agreement — 
Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date 
(which is currently expected to be on Friday, July 10, 2026).

<<<PAGE 2>>>
– 2 –
NEXCHIP SEMICONDUCTOR CORPORATION
合肥晶合集成電路股份有限公司
Global Offering
Number of Offer Shares under the 
Global Offering
:
216,167,000 H Shares (subject to the 
Over-allotment Option)
Number of Hong Kong Offer Shares
:
21,616,700 H Shares
Number of International Offer Shares
:
194,550,300 H Shares (subject to the 
Over-allotment Option)
Final Offer Price
:
HK$32.30 per H Share, plus brokerage 
of 1.0%, AFRC transaction levy of 
0.00015%, SFC transaction levy of 
0.0027% and Stock Exchange trading 
fee of 0.00565% (payable in full on 
application in Hong Kong dollars and 
subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
2249
Sole Sponsor, Sole Sponsor-Overall Coordinator, Joint Global Coordinator, 
Joint Bookrunner and Joint Lead Manager
Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
– 3 –
NEXCHIP SEMICONDUCTOR CORPORATION
合肥晶合集成電路股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND 
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated June 30, 2026 (the “Prospectus”) 
issued by Nexchip Semiconductor Corporation (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could 
move substantially even with a small number of H Shares traded and should exercise extreme 
caution when dealing in the H Shares.
SUMMARY
Company Information
Stock Code
2249
Stock short name
NEXCHIP
Dealings commencement date
July 10, 2026*
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$32.30
Offer Price Range
HK$30.00 – HK$32.30
Offer Shares and Share Capital
Number of Offer Shares
216,167,000
Number of Offer Shares in Hong Kong Public Offering
21,616,700
Number of Offer Shares in International Offering
194,550,300
Number of issued Shares upon Listing 
(before exercise of the Over-allotment Option)
2,223,758,697
Over-allocation
No. of Offer Shares over-allocated
32,425,000
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$6,982.19 million
Less: Es timated listing expenses payable based on 
Final Offer Price
HK$(203.47) million
Net proceeds
HK$6,778.73 million

<<<PAGE 4>>>
– 4 –
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of 
the use of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” 
of the Prospectus.
The Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment 
Option (if any) for the purposes as set out in the section headed “Future Plans and Use of 
Proceeds” of the Prospectus on a pro rata basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
195,505
No. of successful applications
84,096
Subscription level
344.26 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong 
Public Offering
21,616,700
Final no. of Offer Shares under the Hong Kong Public Offering
21,616,700
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering
10.00%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can 
refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification document number or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
170
Subscription Level
14.62 times
No. of Offer Shares initially available under the International 
Offering
194,550,300
Final no. of Offer Shares under the International Offering
194,550,300
% of Offer Shares under the International Offering to the Global 
Offering
90.00%
The Directors confirm that, to the best of their knowledge, information and belief, save 
for (a) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent 
under paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) 
granted by the Stock Exchange to permit the Company to allocate certain Offer Shares in 
the International Offering to certain Permitted Existing Shareholders and/or their close 
associates; and (b) a consent under Chapter 4.15 of the Guide for New Listing Applicants to 
permit the Company to, among other things, allocate further H Shares in the International 
Offering to certain existing Shareholders and/or their close associates, and the Cornerstone 
Investors, (i) none of the Offer Shares subscribed by the placees and the public have been 
financed directly or indirectly by the Company, any of the Directors, chief executive of the 

<<<PAGE 5>>>
– 5 –
Company, controlling shareholders, substantial Shareholders, existing Shareholders of the 
Company or any of its subsidiaries or their respective close associates; and (ii) none of 
the placees and the public who have purchased the Offer Shares are accustomed to taking 
instructions from the Company, any of the Directors, chief executive of the Company, 
controlling shareholders, substantial Shareholders, existing Shareholders of the Company 
or any of its subsidiaries or their respective close associates in relation to the acquisition, 
disposal, voting or other disposition of H Shares registered in his/her/its name or otherwise 
held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of Offer 
Shares 
allocatedNote 2
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 1
% of total issued 
share capital in 
the Company 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing 
shareholders 
or their close 
associates
Hefei Chipone (Hong Kong) Co., 
Limited (合肥集創（香港）有限公
司) and Chipone (Hong Kong) Co., 
Limited (集創北方（香港）有限公司) 
(collectively, “Chipone”)
12,460,800
5.76%
0.56%
No
Puxin Technology Limited (璞新科
技有限公司) (“Puxin Technology”)
12,213,000
5.65%
0.55%
Yes
Smartsens Technology (HK) Co., 
Limited (智感微電子科技（香港）
有限公司) (“Smartsens (HK)”)
12,010,400
5.56%
0.54%
No
Chery Automobile HongKong Trade 
Co., Limited (奇瑞汽車香港貿易有
限公司) (“Chery Automobile 
HongKong”) 
10,569,100
4.89%
0.48%
No
Goertek (HongKong) Co., Limited 
(香港歌爾泰克有限公司) (“Goertek 
(HongKong)”) 
7,278,900
3.37%
0.33%
No
Taikang Life Insurance Co., Ltd 
(泰康人壽保險有限責任公司) 
(“Taikang Life”)
8,734,700
4.04%
0.39%
Yes

<<<PAGE 6>>>
– 6 –
Investor
No. of Offer 
Shares 
allocatedNote 2
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 1
% of total issued 
share capital in 
the Company 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing 
shareholders 
or their close 
associates
GF Fund Management Co., Ltd. 
(廣發基金管理有限公司) (“GF 
Fund Management”) and 
GF International Investment 
Management Limited (廣發國際資
產管理有限公司) (“GF Fund HK”, 
together with GF Fund Management, 
“GF Fund”)
8,734,700
4.04%
0.39%
Yes
Shanghai Gaoyi Asset Management 
Partnership (Limited Partnership) 
(上海高毅資產管理合夥企業
（有限合夥） (“Shanghai Gaoyi”) 
and CICC Financial Trading Limited 
(“CICC FT”) (in connection with a 
series of cross border delta-one OTC 
equity swap transactions between 
CICC FT and China International 
Capital Corporation Limited 
(the “Gaoyi OTC Swaps”)
2,668,900
1.23%
0.12%
No
Perseverance Asset Management 
International (Singapore) Pte. 
Ltd. (“Perseverance Asset 
Management”)
1,698,400
0.79%
0.08%
No
China Universal Asset Management 
(Hong Kong) Company Limited 
(匯添富資產管理（香港）有限公司) 
(“China Universal (HK)”)Note 3
4,367,300
2.02%
0.20%
Yes  
NGS Super Pty Limited ( “NGS 
Super”), as trustee of NGS Super 
3,639,400
1.68%
0.16%
No
HHLR Advisors, Ltd. (“HHLRA”) 
3,639,400
1.68%
0.16%
No
WT Asset Management Limited 
(“WT Asset Management”)
3,639,400
1.68%
0.16%
No
IvyRock Asset Management (HK) 
Limited (常春藤資產管理（香港）
有限公司) (“IvyRock”)
3,639,400
1.68%
0.16%
Yes 

<<<PAGE 7>>>
– 7 –
Investor
No. of Offer 
Shares 
allocatedNote 2
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 1
% of total issued 
share capital in 
the Company 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing 
shareholders 
or their close 
associates
Verition Multi-Strategy Master Fund 
Ltd., managed by Verition Fund 
Management LLC (“Verition”)
3,396,800
1.57%
0.15%
No
Pinpoint Asset Management Limited 
(保銀資產管理有限公司) 
(“Pinpoint”)
3,396,800
1.57%
0.15%
Yes 
Da Cheng International Asset 
Management Company Limited 
(大成國際資產管理有限公司) 
(“Da Cheng International”) 
1,941,000
0.90%
0.09%
Yes 
ICBC Wealth Management Co., Ltd. 
(工銀理財有限責任公司) 
(“ICBC Wealth”)Note 3
1,941,000
0.90%
0.09%
No
PSBC Wealth Management Co., Ltd. 
(中郵理財有限責任公司) 
(“PSBC Wealth”) 
970,500
0.45%
0.04%
No
Harvest Global Investments Limited 
(嘉實國際資產管理有限公司) 
(“HGI”)
970,500
0.45%
0.04%
Yes 
Notes:
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the 
Global Offering (assuming the Over-allotment Option is not exercised).
2. 
Only taking into account the Shares allocated to the relevant investors as cornerstone investors under the Global Offering. In 
addition to the Offer Shares subscribed for as Cornerstone Investors, certain Cornerstone Investors (except Goertek (HongKong) 
and CICC FT) were allocated further Offer Shares as placees in the International Offering. Please refer to the section headed 
“Allotment Results Details — International Offering — Allottees with Waivers/Consents Obtained” in this announcement for 
details. Only the Offer Shares subscribed for as Cornerstone Investors are subject to lock-up as indicated below. For details, 
please refer to the section headed “Lock-up Undertakings — Cornerstone Investors” in this announcement.
3. 
Regarding Offer Shares allocated to China Universal (HK) and ICBC Wealth, please also refer to the consent under paragraph 
1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations to connected 
client for details.

<<<PAGE 8>>>
– 8 –
Allottees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares 
allocated
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 3
% of total issued 
share capital in 
the Company 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 4
Relationship
Allottees with consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of 
further H Shares to Cornerstone InvestorsNote 1 & 5
Chipone
5,393,800
2.50%
0.24%
Chipone is a Cornerstone 
Investor
Puxin Technology
532,200
0.25%
0.02%
Puxin Technology is a 
Cornerstone Investor and 
is a close associate of our 
existing Shareholders Note 6
Xu Chen
1,179,900
0.55%
0.05%
Xu Chen is the ultimate 
beneficial owner of 
Smartsens (HK), a 
Cornerstone Investor
Chery Automobile 
HongKong
3,238,400
1.50%
0.15%
Chery Automobile 
HongKong is a 
Cornerstone Investor
Taikang Life
2,038,000
0.94%
0.09%
Taikang Life is a 
Cornerstone Investor and 
is a close associate of our 
existing Shareholders Note 6
GF Fund
3,639,000
1.68%
0.16%
GF Fund is a Cornerstone 
Investor and a close 
associate of our existing 
Shareholders Note 6
Perseverance Asset 
Management
1,698,400
0.79%
0.08%
Perseverance Asset 
Management is a 
Cornerstone Investor
China Universal (HK)
1,698,400
0.79%
0.08%
China Universal (HK) is a 
Cornerstone Investor and 
is a close associate of our 
existing Shareholders Note 6
NGS Super
1,091,000
0.50%
0.05%
NGS Super is a 
Cornerstone Investor
HHLRA
1,091,000
0.50%
0.05%
HHLRA is a Cornerstone 
Investor
WT Asset Management
1,091,000
0.50%
0.05%
WT Asset Management is 
a Cornerstone Investor

<<<PAGE 9>>>
– 9 –
Investor
No. of Offer 
Shares 
allocated
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 3
% of total issued 
share capital in 
the Company 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 4
Relationship
IvyRock
1,045,700
0.48%
0.05%
IvyRock is a Cornerstone 
Investor and is a close 
associate of our existing 
Shareholders Note 6
Verition
970,500
0.45%
0.04%
Verition is a Cornerstone 
Investor
Pinpoint
970,500
0.45%
0.04%
Pinpoint is a Cornerstone 
Investor and is a close 
associate of our existing 
Shareholders Note 6
Da Cheng International
582,000
0.27%
0.03%
Da Cheng International is 
a Cornerstone Investor and 
is a close associate of our 
existing Shareholders Note 6
ICBC Wealth
582,000
0.27%
0.03%
ICBC Wealth is a 
Cornerstone Investor
PSBC Wealth
291,000
0.13%
0.01%
PSBC Wealth is a 
Cornerstone Investor
HGI
291,000
0.13%
0.01%
HGI is a Cornerstone 
Investor and is a close 
associate of our existing 
Shareholders Note 6
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clientsNote 2
CITIC Asset Management 
(as a placee)
2,400
0.001%
0.0001%
Connected client of CLSA 
and CSB
China AMC (as a placee)
242,600
0.11%
0.01%
China Southern (as a placee)
1,213,000
0.56%
0.05%
Connected client of HTFH
ICBC Wealth (as a 
cornerstone investor)
1,941,000
0.90%
0.09%
Connected client of ICBC 
ISL
ICBC Wealth (as a placee)
582,000
0.27%
0.03%

<<<PAGE 10>>>
– 10 –
Investor
No. of Offer 
Shares 
allocated
% of total issued 
H Shares after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 3
% of total issued 
share capital in 
the Company 
after the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)Note 4
Relationship
ICBC UBS (as a placee)
121,000
0.06%
0.01%
Connected client of ICBC 
ISL and UBS AG Hong 
Kong
UBS AM Singapore (as a 
placee)
4,367,000
2.02%
0.20%
Connected client of UBS 
AG Hong Kong
China Universal (HK) (as 
a cornerstone investor)
4,367,300
2.02%
0.20%
Connected client of Orient
China Universal (HK) (as 
a placee)
727,000
0.34%
0.03%
CUAM (as a placee)
971,400
0.45%
0.04%
Shanghai Gaoyi and CICC 
FT (in connection with 
Gaoyi OTC Swaps) (as a 
cornerstone investor)
2,668,900
1.23%
0.12%
Connected client of 
CICCHKS
Notes:
1. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the number of Offer 
Shares allocated to the investors as placees in the International Offering. For allocations of Offer Shares to the relevant investors 
as Cornerstone Investors, please refer to the section headed “Allotment Results Details — International Offering — Cornerstone 
Investors” in this announcement. For details of the consent under Chapter 4.15 of the Guide for New Listing Applicants in 
relation to allocations of further H Shares to the existing Shareholders and/or their close associates and Cornerstone Investors, 
please refer to the section headed “Others/Additional Information — Allocations of Offer Shares to the existing Shareholders 
and/or their close associates and Cornerstone Investors with a consent under Chapter 4.15 of the Guide for New Listing 
Applicants” in this announcement.
2. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations to connected clients, please refer to the section headed “Others/Additional Information — 
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines” in this announcement.
3. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the 
Global Offering (assuming the Over-allotment Option is not exercised).
4. 
Not taking into account any A Shares held by the relevant investors. The figures are based on assumption that the Over-allotment 
Option is not exercised.
5. 
Taking into account the number of Offer Shares further allocated to each of the Cornerstone Investors (and/or its close associates), 
the aggregate % of total issued share capital after the Global Offering (assuming the Over-allotment Option is not exercised) 
held by the respective investors are as follow:
Chipone holds 0.80%, Puxin Technology holds 0.57%, Xu Chen holds 0.59%, Chery Automobile Hongkong holds 0.63%, Taikang 
Life holds 0.48%, GF Fund holds 0.55%, Perseverance Asset Mgmt holds 0.16%, China Universal (HK) and CUAM holds 0.28%, 
NGS Super holds 0.21%, HHLRA holds 0.21%, WT Asset Management holds 0.21%, IvyRock holds 0.21%, Verition holds 0.19%, 
Pinpoint holds 0.19%, Da Cheng International holds 0.12%, ICBC Wealth holds 0.12%, PSBC Wealth holds 0.05% and HGI 
holds 0.05%.
6. 
All of these investors are Permitted Existing Shareholders, each of whom holds no more than 1% of the issued share capital of the 
Company immediately prior to the completion of the Global Offering.

<<<PAGE 11>>>
– 11 –
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
(assuming the 
Over-allotment 
Option is not 
exercised)
% of total issued 
share capital in 
the Company 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject to the 
lock-up undertakings
Hefei Construction 
Investment Holding 
(Group) Co., Ltd. 
(合肥市建設投資控
股（集團）有限公司) 
(“Hefei Construction 
Investment”)
468,474,592
–
21.07%
January 9, 2027 (First 
Six-Month Period)Note 1
July 9, 2027 (Second 
Six-Month Period)Note 2
Hefei Xinping Industrial 
Investment Fund (Limited 
Partnership) (合肥芯屏產
業投資基金（有限合夥）) 
(“Hefei Xinping”)
328,736,799
–
14.78%
January 9, 2027 (First 
Six-Month Period)Note 1
July 9, 2027 (Second 
Six-Month Period)Note 2
Notes:
1. 
The Controlling Shareholders may dispose of or transfer Shares after the indicated date subject to that 
the Controlling Shareholders will not cease to be a Controlling Shareholder.
2. 
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after 
the indicated date.
3. 
For illustrative purposes only, this subsection lists only those members of the Controlling Shareholders 
Group who hold Shares directly in the Company. Hefei Construction Investment is a direct beneficial 
owner of 468,474,592 Shares of the Company and controls 390,825,299 Shares of the Company 
(including repurchased shares of the Company) through Hefei Xinping, whose general partner is Hefei 
Jiantou Capital Management Co., Ltd. (“Jiantou Capital”), which is controlled by Hefei Construction 
Investment. 
Therefore, upon Listing, Hefei Construction Investment, Jiantou Capital and Hefei Xinping will constitute 
the Controlling Shareholders Group and each of them is subject to the same lock-up as disclosed above. For 
further details, please refer to “Relationship with our Controlling Shareholder Group” in the Prospectus.

<<<PAGE 12>>>
– 12 –
Cornerstone Investors
Name
Number of H 
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
(assuming the 
Over-allotment 
Option is not 
exercised)Note 1
% of total issued 
share capital in 
the Company 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject to the 
lock-up undertakingsNote 2
Chipone
12,460,800
5.76%
0.56%
January 9, 2027
Puxin Technology
12,213,000
5.65%
0.55%
January 9, 2027
Smartsens (HK)
12,010,400
5.56%
0.54%
January 9, 2027
Chery Automobile 
HongKong
10,569,100
4.89%
0.48%
January 9, 2027
Goertek (HongKong)
7,278,900
3.37%
0.33%
January 9, 2027
Taikang Life
8,734,700
4.04%
0.39%
January 9, 2027
GF Fund
8,734,700
4.04%
0.39%
January 9, 2027
Shanghai Gaoyi and CICC 
Financial Trading Limited 
(in connection with Gaoyi 
OTC Swaps)
2,668,900
1.23%
0.12%
January 9, 2027
Perseverance Asset 
Management
1,698,400
0.79%
0.08%
January 9, 2027
China Universal (HK)
4,367,300
2.02%
0.20%
January 9, 2027
NGS Super
3,639,400
1.68%
0.16%
January 9, 2027
HHLRA
3,639,400
1.68%
0.16%
January 9, 2027
WT Asset Management
3,639,400
1.68%
0.16%
January 9, 2027
IvyRock
3,639,400
1.68%
0.16%
January 9, 2027
Verition
3,396,800
1.57%
0.15%
January 9, 2027
Pinpoint
3,396,800
1.57%
0.15%
January 9, 2027
Da Cheng International
1,941,000
0.90%
0.09%
January 9, 2027

<<<PAGE 13>>>
– 13 –
Name
Number of H 
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
(assuming the 
Over-allotment 
Option is not 
exercised)Note 1
% of total issued 
share capital in 
the Company 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject to the 
lock-up undertakingsNote 2
ICBC Wealth
1,941,000
0.90%
0.09%
January 9, 2027
PSBC Wealth
970,500
0.45%
0.04%
January 9, 2027
HGI
970,500
0.45%
0.04%
January 9, 2027
Total
107,910,400
49.92%
4.85%
Notes:
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under the 
Global Offering.
2. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on January 9, 2027. The 
Cornerstone Investors will cease to be prohibited from disposing of or transferring H Shares subscribed pursuant to the relevant 
cornerstone investment agreements after the indicated date.
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Allotment 
as % of total 
Offer Shares 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment 
as % of total 
Offer Shares 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Number of 
H Shares held 
upon Listing
Approximate
% of 
total issued 
share capital 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
Approximate
% of 
total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Top1
17,854,600
9.18%
7.87%
8.26%
7.18%
17,854,600
0.80%
0.79%
Top5
69,971,300
35.97%
30.83%
32.37%
28.15%
69,971,300
3.15%
3.10%
Top10
106,219,300
54.60%
46.80%
49.14%
42.73%
106,219,300
4.78%
4.71%
Top25
177,500,200
91.24%
78.20%
82.11%
71.40%
177,500,200
7.98%
7.87%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 14>>>
– 14 –
H SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Allotment 
as % of total 
Offer Shares 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment 
as % of total 
Offer Shares 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Number of 
H Shares held 
upon Listing
Approximate
% of 
total issued 
share capital 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
Approximate
% of 
total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Top1
17,854,600
9.18%
7.87%
8.26%
7.18%
17,854,600
0.80%
0.79%
Top5
69,971,300
35.97%
30.83%
32.37%
28.15%
69,971,300
3.15%
3.10%
Top10
106,219,300
54.60%
46.80%
49.14%
42.73%
106,219,300
4.78%
4.71%
Top25
177,500,200
91.24%
78.20%
82.11%
71.40%
177,500,200
7.98%
7.87%
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Allotment 
as % of total 
Offer Shares 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment 
as % of total 
Offer Shares 
(assuming the 
Over-allotment
 Option is fully 
exercised and 
new H Shares 
are issued)
Number of 
H Shares held 
upon Listing 
(if applicable)
Number of 
Shares held 
upon Listing#
Approximate 
% of 
total issued 
share capital 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
Approximate 
% of 
total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Top1
0
0.00%
0.00%
0.00%
0.00%
0
797,211,391
35.85%
35.33%
Top5
0
0.00%
0.00%
0.00%
0.00%
0
1,250,403,880
56.23%
55.42%
Top10
29,212,100
15.02%
12.87%
13.51%
11.75%
29,212,100
1,359,437,114
61.13%
60.25%
Top25
116,409,300
59.84%
51.29%
53.85%
46.83%
116,409,300
1,523,385,097
68.50%
67.52%
Notes:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon 
Listing.
# 
Among the top 25 placees, certain placees are also existing Shareholders. To the best knowledge, 
information and belief of the Company after due enquiry, details of the allocations to the Permitted 
Existing Shareholder holding more than 1% of the issued share capital of the Company immediately 
prior to the completion of the Global Offering have been disclosed in this announcement. Please refer 
to the section headed “Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules 
and consent under paragraph 1C of the Placing Guidelines in relation to subscription for H Shares 
by Permitted Existing Shareholders holding more than 1% of the issued share capital of the Company 
immediately prior to the completion of the Global Offering and/or their close associates”. For the top 
25 placees who are also existing shareholders held less than 0.05% of the issued share capital of the 
Company immediately prior to the completion of the Global Offering, the number of A Shares held by them 
is not counted into the number of Shares held upon Listing.

<<<PAGE 15>>>
– 15 –
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made 
by the public will be conditionally allocated on the basis set out below:
NO. OF 
SHARES
APPLIED FOR
NO. OF 
VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED
OF THE TOTAL 
NO. OF SHARES 
APPLIED FOR
POOL A
100
44,149
3,532 out of 44,149 to receive 100 Shares
8.00%
200
7,729
773 out of 7,729 to receive 100 Shares
5.00%
300
17,609
2,007 out of 17,609 to receive 100 Shares
3.80%
400
3,413
491 out of 3,413 to receive 100 Shares
3.60%
500
4,555
752 out of 4,555 to receive 100 Shares
3.30%
600
2,861
532 out of 2,861 to receive 100 Shares
3.10%
700
2,183
472 out of 2,183 to receive 100 Shares
3.09%
800
2,191
507 out of 2,191 to receive 100 Shares
2.89%
900
1,910
476 out of 1,910 to receive 100 Shares
2.77%
1,000
21,502
5,573 out of 21,502 to receive 100 Shares
2.59%
2,000
8,011
2,958 out of 8,011 to receive 100 Shares
1.85%
3,000
8,682
3,943 out of 8,682 to receive 100 Shares
1.51%
4,000
3,493
1,837 out of 3,493 to receive 100 Shares
1.31%
5,000
3,498
2,062 out of 3,498 to receive 100 Shares
1.18%
6,000
2,626
1,699 out of 2,626 to receive 100 Shares
1.08%
7,000
2,072
1,378 out of 2,072 to receive 100 Shares
0.95%
8,000
1,912
1,361 out of 1,912 to receive 100 Shares
0.89%
9,000
1,817
1,308 out of 1,817 to receive 100 Shares
0.80%
10,000
10,205
7,348 out of 10,205 to receive 100 Shares
0.72%
20,000
5,896
100 Shares
0.50%
30,000
4,279
100 Shares plus 1,883 out of 4,279 to receive additional 100 Shares
0.48%
40,000
2,888
100 Shares plus 2,114 out of 2,888 to receive additional 100 Shares
0.43%
50,000
2,620
100 Shares plus 2,384 out of 2,620 to receive additional 100 Shares
0.38%
60,000
2,112
200 Shares
0.33%
70,000
1,587
200 Shares plus 381 out of 1,587 to receive additional 100 Shares
0.32%
80,000
1,560
200 Shares plus 672 out of 1,560 to receive additional 100 Shares
0.30%
90,000
1,760
200 Shares plus 1,248 out of 1,760 to receive additional 100 Shares
0.30%
100,000
10,224
300 Shares
0.30%
 
183,344
Total number of Pool A successful applicants: 71,935
 

<<<PAGE 16>>>
– 16 –
NO. OF 
SHARES
APPLIED FOR
NO. OF 
VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED
OF THE TOTAL 
NO. OF SHARES 
APPLIED FOR
POOL B
200,000
6,513
500 Shares
0.25%
300,000
1,947
600 Shares
0.20%
400,000
1,009
800 Shares
0.20%
500,000
1,612
1,000 Shares
0.20%
1,000,000
542
2,000 Shares
0.20%
1,500,000
201
3,000 Shares
0.20%
2,000,000
160
4,000 Shares
0.20%
3,000,000
77
6,000 Shares
0.20%
4,000,000
47
8,000 Shares
0.20%
6,000,000
17
11,000 Shares
0.18%
8,000,000
16
14,400 Shares
0.18%
10,808,300
20
19,100 Shares
0.18%
 
12,161
Total number of Pool B successful applicants: 12,161
 
As of the date of this announcement, the relevant subscription monies previously deposited 
in the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in 
respect of which consent has been obtained, the Company has complied with the Listing Rules 
and guidance materials in relation to the placing, allotment and listing of the Company’s H 
Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by 
the placees or the public (as the case may be) directly or indirectly for each Offer Share 
subscribed for or purchased by them was the same as the final Offer Price in addition to any 
brokerage, AFRC transaction levy, SFC transaction levy and trading fee payable.

<<<PAGE 17>>>
– 17 –
OTHERS/ADDITIONAL INFORMATION
Allocations of Offer Shares to the existing Shareholders and/or their close associates and 
Cornerstone Investors with a consent under Chapter 4.15 of the Guide for New Listing 
Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 
4.15 of the Guide for New Listing Applicants to permit the Company to allocate further 
Offer Shares in the International Offering to certain existing Shareholders and/or their 
close associates, and Cornerstone Investors as placees, subject to the following conditions 
(“Allocation to Size-based Exemption Participants”):
(a) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a 
total value of at least HK$1 billion;
(b) 
the Offer Shares allocated to all existing Shareholders and their close associates (whether 
as cornerstone investors and/or as placees) as permitted under the Size-based Exemption 
(as defined in the Guide for New Listing Applicants) do not exceed 30% of the total 
number of the H Shares offered under the Global Offering;
(c) 
the Allocation to Size-based Exemption Participants will not affect the Company’s 
ability to satisfy its public float requirement as prescribed by the Stock Exchange under 
the waiver from strict compliance with the requirements of Rule 8.08(1) and 19A.13A of 
the Listing Rules;
(d) 
each Director, chief executive and controlling shareholder of the Company confirms that 
no securities have been allocated to them or their respective close associates under the 
Size-based Exemption; and
(e) 
details of the allocation to existing Shareholders and/or their close associates and 
Cornerstone Investors under the Size-based Exemption will be disclosed in this 
announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of the allocations of Offer Shares to existing Shareholders and/or their close 
associates and Cornerstone Investors, please refer to the section headed “Allotment Results 
Details — International Offering — Allottees with Waivers/Consents Obtained” in this 
announcement.

<<<PAGE 18>>>
– 18 –
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of 
their connected distributors pursuant to the Placing Guidelines. Details of the placement to 
connected clients are set out below. The Company has applied to the Stock Exchange for, and 
the Stock Exchange has granted, consents under paragraph 1C(1) of the Placing Guidelines 
to permit the Company to allocate such Offer Shares in the International Offering to the 
connected clients. The allocation of Offer Shares to such connected clients is in compliance 
with all the conditions under the consent granted by the Stock Exchange.
Part A – Connected Clients holding the beneficial interest of the Offer Shares on a 
discretionary basis on behalf of independent third parties
No.
Connected 
Distributor
Connected Client
Relationship with the 
Connected Distributor
Whether the 
Connected Client 
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
allocated 
to the 
connected 
client
Approximate 
Percentage of 
total number 
of Offer Shares
Approximate 
percentage of 
total Shares 
in issue 
immediately 
following the 
completion of 
Global Offering
1.
CLSA Limited 
(“CLSA”) 
and CITIC 
Securities 
Brokerage 
(HK) Limited 
(“CSB”)
CITIC Securities 
Asset Management 
Company Limited 
(“CITIC Asset 
Management”) (1)
CITIC Asset Management 
is a member of the same 
group of companies as 
CLSA and CSB.
Yes
2,400 Less than 0.01% Less than 0.01%
China Asset 
Management 
Co., Ltd (“China 
AMC”) (2)
China AMC is a member 
of the same group of 
companies as CLSA and 
CSB.
No
242,600
0.11%
0.01%
2.
Huatai Financial 
Holdings (Hong 
Kong) Limited 
(“HTFH”)
China Southern 
Asset Management 
Co., Ltd. (“China 
Southern”) (3)
China Southern is held by 
Huatai Securities Co., 
Ltd. as to 41.16%, which 
wholly owns HTFH.
No
1,213,000
0.56%
0.05%
As such, China Southern is a 
member of the same group 
of companies as HTFH.

<<<PAGE 19>>>
– 19 –
No.
Connected 
Distributor
Connected Client
Relationship with the 
Connected Distributor
Whether the 
Connected Client 
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
allocated 
to the 
connected 
client
Approximate 
Percentage of 
total number 
of Offer Shares
Approximate 
percentage of 
total Shares 
in issue 
immediately 
following the 
completion of 
Global Offering
3.
ICBC 
International 
Securities 
Limited 
(“ICBC ISL”)
ICBC Wealth 
Management 
Co., Ltd. (“ICBC 
Wealth”)(4)
ICBC Wealth is a direct 
wholly-owned subsidiary 
of Industrial and 
Commercial Bank of China 
Limited (“ICBC”), the 
shares of which are listed 
on the Stock Exchange 
(stock code: 1398). ICBC 
Wealth and ICBC ISL 
are fellow subsidiaries of 
ICBC. ICBC Wealth is a 
member of the same group 
of companies as ICBC ISL.
No
As a cornerstone
investor:
1,941,000
As a placee: 
582,000
0.90%
0.27%
0.09%
0.03%
4.
UBS AG Hong 
Kong Branch 
Wealth 
Management 
(“UBS AG 
Hong Kong”)
ICBC UBS Asset 
Management 
(International) 
Company Limited 
(“ICBC UBS”)(5)
ICBC UBS is a member 
of the same group of 
companies as ICBC ISL 
and UBS AG Hong Kong.
No
121,000
0.06%
0.01%
UBS Asset 
Management 
(Singapore) 
Ltd. (“UBS AM 
Singapore”)(6)
UBS AM Singapore is a 
member of the same group 
of companies as UBS AG 
Hong Kong.
No
4,367,000
2.02%
0.20%

<<<PAGE 20>>>
– 20 –
No.
Connected 
Distributor
Connected Client
Relationship with the 
Connected Distributor
Whether the 
Connected Client 
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
allocated 
to the 
connected 
client
Approximate 
Percentage of 
total number 
of Offer Shares
Approximate 
percentage of 
total Shares 
in issue 
immediately 
following the 
completion of 
Global Offering
5.
Orient Securities 
(Hong Kong) 
Limited 
(“Orient”)
China Universal Asset 
Management (Hong 
Kong) Company 
Limited (“China 
Universal (HK)”)(7)
China Universal (HK) is a 
member of the same group 
of companies as Orient.
Yes
As a cornerstone 
investor: 
4,367,300
2.02%
0.20%
China Universal (HK) is 
therefore considered as a 
connected client of Orient 
pursuant to paragraph 
1B(7) of the Placing 
Guidelines.
As a placee: 
727,000
0.34%
0.03%
China Universal Asset 
Management Co. 
Ltd (“CUAM”)(8)
CUAM is the holding 
company of China 
Universal (HK). CUAM 
is a member of the same 
group of companies as 
Orient.
CUAM is therefore 
considered as a connected 
client of Orient pursuant 
to paragraph 1B(7) of the 
Placing Guidelines.
No
971,400
0.45%
0.04%

<<<PAGE 21>>>
– 21 –
Part B – Connected Clients holding the beneficial interest of the Offer Shares on a non-
discretionary basis on behalf of independent third parties
No.
Connected 
Distributor
Connected Client
Relationship with 
the Connected 
Distributor
Whether the 
Connected Client 
is a collective 
investment 
scheme which is 
not authorised 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme
Number of Offer 
Shares allocated 
to the connected 
client
Approximate 
Percentage of 
total number of 
Offer Shares
Approximate 
percentage of 
total Shares 
in issue 
immediately 
following the 
completion of 
Global Offering
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
with the Gaoyi 
OTC Swaps)(9)
CICC FT is a 
member of the 
same group with 
CICCHKS
No
2,668,900
1.23%
0.12%
Notes:
(1) 
CITIC Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager 
managing the funds on behalf of its investors, all of which are collective investment schemes not 
authorized by the Securities and Futures Commission (“SFC”), and each of which is an independent third 
party of the Company, its subsidiaries, its Controlling Shareholders, its substantial shareholders, CLSA, 
CSB, CITIC Asset Management and the companies which are members of the same group of CLSA and 
CSB. Details of the collective investment schemes are as follows:
No.
Fund name
Ultimate beneficial 
owner(s) holding 
30% of more 
interest (if any)
Types and values 
of assets under 
management
Whether 
the scheme 
is publicly 
marketed
Scheme 
establishment 
date
Identities of 
the general 
partners and 
the 20 largest 
limited partners 
of the scheme 
where applicable
Identity of 
the scheme 
administrator
Relationships among 
the scheme, 
the ultimate beneficial 
owner(s) of 
the limited partner(s), 
the controlling 
shareholders of 
the Company, and 
the Company
1.
CITIC Securities AM-
Guibinfengyuan 
No.118 QDII (中信
證券資管貴賓豐元
118號QDII集合資產
管理計劃)
Zhang Guofeng (張
國鋒) holds 30% 
or more interests
Collective asset 
management plan
AUM:
approximately RMB228 
million*
No
29 August 2025
Not applicable 
as it is not in 
partnership 
structure and 
does not have any 
general partner 
or limited partner
CITIC Asset 
Management
The scheme and ultimate 
beneficial owners are 
independent third 
parties of CLSA and 
CSB, the Company 
and the Controlling 
Shareholders.

<<<PAGE 22>>>
– 22 –
No.
Fund name
Ultimate beneficial 
owner(s) holding 
30% of more 
interest (if any)
Types and values 
of assets under 
management
Whether 
the scheme 
is publicly 
marketed
Scheme 
establishment 
date
Identities of 
the general 
partners and 
the 20 largest 
limited partners 
of the scheme 
where applicable
Identity of 
the scheme 
administrator
Relationships among 
the scheme, 
the ultimate beneficial 
owner(s) of 
the limited partner(s), 
the controlling 
shareholders of 
the Company, and 
the Company
2.
CITIC SECURITIES 
COMPANY 
LIMITED-XINHANG 
ZHIYUAN NO.1 (中
信證券信航致遠1號
集合資產管理計劃)
No single ultimate 
beneficial owner 
holds 30% or 
more interests
Collective asset 
management plan
AUM:
approximately RMB24 
million*
No
25 December 
2020
Not applicable 
as it is not in 
partnership 
structure and 
does not have any 
general partner 
or limited partner
CITIC Asset 
Management
The scheme and ultimate 
beneficial owners are 
independent third 
parties of CLSA and 
CSB, the Company 
and the Controlling 
Shareholders.
3.
CITIC SECURITIES 
COMPANY 
LIMITED-XINHANG 
ZHIYUAN NO.3 (中
信證券信航致遠3號
集合資產管理計劃)
No single ultimate 
beneficial owner 
holds 30% or 
more interests
Collective asset 
management plan
AUM:
approximately RMB56 
million*
No
4 March 2021
Not applicable 
as it is not in 
partnership 
structure and 
does not have any 
general partner 
or limited partner
CITIC Asset 
Management
The scheme and ultimate 
beneficial owners are 
independent third 
parties of CLSA and 
CSB, the Company 
and the Controlling 
Shareholders.
4.
CITIC SECURITIES 
AM-
GUIBINFENGYUAN 
NO.108 QDII (中信
證券資管貴賓豐元
108號QDII集合資產
管理計劃)
No single ultimate 
beneficial owner 
holds 30% or 
more interests
Collective asset 
management plan
AUM:
approximately RMB155 
million*
No
14 April 2026
Not applicable 
as it is not in 
partnership 
structure and 
does not have any 
general partner 
or limited partner
CITIC Asset 
Management
The scheme and ultimate 
beneficial owners are 
independent third 
parties of CLSA and 
CSB, the Company 
and the Controlling 
Shareholders.
* This AUM figure is as of 18 June 2026.
(2) 
China AMC will hold the Offer Shares in its capacity as the discretionary fund manager managing the 
funds on behalf of its underlying clients none of which is a collective investment scheme and each of which 
is an independent third party of the Company, its subsidiaries, its Controlling Shareholders, its substantial 
shareholders, CLSA, CSB, China AMC and the companies which are members of the same group of CLSA 
and CSB. Details of such underlying clients are as follows:
Name of underlying clients
Ultimate beneficial owner(s) holding 30% or 
more interest (if any)
ChinaAMC Global Selective Equity Fund
No single ultimate beneficial owner holds 30% or 
more interests
Mackenzie ChinaAMC all China Equity Fund
No single ultimate beneficial owner holds 30% or 
more interests
JSS All China Equity Fund
No single ultimate beneficial owner holds 
30% or more interests

<<<PAGE 23>>>
– 23 –
(3) 
China Southern, a qualified domestic institutional investor as approved by the relevant PRC authority 
to conduct asset management business, will hold the Offer Shares in its capacity as the independent 
agent and discretionary manager of certain QDII funds. None of such underlying clients is a collective 
investment scheme and each of them are independent third parties of the Company, its subsidiaries, its 
Controlling Shareholders, its substantial shareholders, HTFH, China Southern and the companies which 
are members of the same group of HTFH. Details of such underlying clients are as follows: 
Name of underlying clients
Ultimate beneficial owner(s) holding 30% or 
more interest (if any)
China Southern Hong Kong Growth Dynamic Allocation 
Hybrid Fund (南方香港成長靈活配置混合)
No single ultimate beneficial owner holds 30% 
or more interests
China New Economy 9-Month Holding Period Hybrid 
Fund (QDII) (南方中國新興經濟9個月持有期混合(QDII))
No single ultimate beneficial owner holds 30% 
or more interests
China Southern Global Dynamic Allocation Fund 
(南方全球精選配置股票(QDII-FOF))
No single ultimate beneficial owner holds 
30% or more interests
China Southern Hong Kong Stock Healthcare Industry 
Hybrid Initiated Securities Investment Fund (QDII) 
(南方港股醫藥行業混合發起（QDII）)
No single ultimate beneficial owner holds 
30% or more interests
China Southern Hong Kong Digital Economy Hybrid 
Initiating Fund (QDII) (南方港股數字經濟混合發起(QDII))
No single ultimate beneficial owner holds 
30% or more interests
China Southern Hong Kong Select Equity Fund 
(南方香港 LOF)
No single ultimate beneficial owner holds
30% or more interests
(4) 
ICBC Wealth will hold the beneficial interests of the Offer Shares on a discretionary basis for and on 
behalf of certain funds, segregated accounts and/or mandates, details of which are set out below. To the 
best knowledge of ICBC Wealth, and after making all reasonable enquiries none of their underlying clients 
is a collective investment scheme and  each of them is an independent third party of the Company, its 
subsidiaries and substantial shareholders, ICBC Wealth, ICBC ISL and the companies which are members 
of the same group of ICBC ISL. 
Name of underlying clients
Ultimate beneficial owner(s) holding 30% or 
more interest (if any)
工銀理財 • 智悅最短持有180天固定收益類開放式
凈值型理財產品
No single ultimate beneficial owner holds 30% 
or more interests
工銀理財 • 恒睿日升月恆30天持盈固收增強開放式
理財產品
No single ultimate beneficial owner holds 30% 
or more interests
工銀理財 • 恒睿日升月恆180天持盈固收增強開放式
理財產品
No single ultimate beneficial owner holds 
30% or more interests
(5) 
ICBC UBS will hold the Offer Shares in its capacity as the discretionary fund manager managing the 
funds on behalf of its underlying clients, none of which is a collective investment scheme and each of 
which is an independent third party of the Company, its subsidiaries, its Controlling Shareholders, its 
substantial shareholders, ICBC UBS, ICBC ISL and UBS AG Hong Kong and the companies which are 
members of the same group of ICBC ISL and UBS AG Hong Kong. Details of such underlying clients are as 
follows:
Name of underlying clients
Ultimate beneficial owner(s) holding 30% or 
more interest (if any)
RUIHONG NO3
Alpaca Capital Management Limited
RUIHONG NO4
Zhang Jiang

<<<PAGE 24>>>
– 24 –
(6) 
UBS AM Singapore will hold Offer Shares in its capacity as the discretionary fund manager managing 
assets on behalf of its underlying clients. None of such underlying clients is a collective investment 
scheme and each of them is an  independent third parties of the Company, its subsidiaries, its Controlling 
Shareholders, its substantial shareholders, UBS AM Singapore and UBS AG Hong Kong and the 
companies which are members of the same group of UBS AG Hong Kong. Details of such underlying 
clients are as follows:
Name of underlying clients
Ultimate beneficial owner(s) holding 30% or 
more interest (if any)
UBS (Lux) Equity Fund — Greater China
No single ultimate beneficial owner holds 30% 
or more interests
UBS (Lux) Equity Fund — China Opportunity
No single ultimate beneficial owner holds 30% 
or more interests
UBS (HK) Fund Series — China Opportunity Equity
No single ultimate beneficial owner holds 
30% or more interests
UBS (Lux) Equity SICAV — All China
No single ultimate beneficial owner holds 
30% or more interests
UBS (Lux) Investment SICAV — China A Opportunity
No single ultimate beneficial owner holds 
30% or more interests
UBS (Cay) — China A Opportunity
No single ultimate beneficial owner holds 
30% or more interests
UBS (Lux) Key Selection SICAV — China Allocation 
Opportunity
No single ultimate beneficial owner holds 
30% or more interests
UBS (JP) China Equity (Ex-A Share) Fund
No single ultimate beneficial owner holds 
30% or more interests
UBS HANA CHINA Equity Master Investment Trust
No single ultimate beneficial owner holds 
30% or more interests
Eskom Pension and Provident Fund China-A
No single ultimate beneficial owner holds 
30% or more interests
KIC_GAEQ-80 (EQA44) — Greater China Equity 
sponsored by MOEF
Korea Investment Corporation
KIC_CAEQ-35 (188492) — Greater China Equity 
sponsored by BOK
Korea Investment Corporation
Flourish — UBS — China Opportunity Equity
Flourish Investment Corporation
National Council for Social Security Fund
National Council for Social Security Fund
BORDER TO COAST EMERGING MARKETS EQUITY
Border to Coast Pensions Partnership 
Limited
BORDER TO COAST EMERGING MARKETS EQUITY 
ALPHA FUND
Border to Coast Pensions Partnership 
Limited
PIC China Opportunity Equity
Public Investment Corporation
(7) 
China Universal (HK) manages investment funds, provides investment advisory services, and manages 
discretionary accounts. The subscription of the Offer Shares as a cornerstone investor and placee will be 
made by China Universal (HK) in its capacity as the investment manager on a discretionary basis for and 
on behalf of following fund(s) and/or discretionary account(s): (i) LC Logistics, Inc; (ii) China Universal 
Special Situation Fund SPC — CUAM Flexible Strategy Fund SP; and (iii) Poly Legend Int Ltd. To the 
best knowledge and belief of China Universal (HK), XU Xin and LI Yan hold 30% or more interest in LC 
Logistics, Inc, and YANG Peilin holds 30% or more interest in Poly Legend Int Ltd; and no single ultimate 
beneficial owner holds 30% or more interest in China Universal Special Situation Fund SPC — CUAM 
Flexible Strategy Fund SP. Each of such underlying client is an independent third party of the Company, 
its subsidiaries, its Controlling Shareholders, its substantial shareholders, China Universal (HK) and 
Orient and the companies which are members of the same group of Orient.

<<<PAGE 25>>>
– 25 –
China Universal (HK) is investing on behalf of a collective investment scheme which is not authorized by 
the Securities and Futures Commission, details of which are as follows:
No. 
Fund name
Types and values 
of assets under 
management
Whether 
the scheme 
is publicly 
markets
Scheme 
establishment 
date
Identities of the 
general partners and 
the 20 largest limited 
partners of the scheme 
where applicable
Identity of 
the scheme 
administrator
Relationships among 
the scheme, the ultimate 
beneficial owner(s), China 
Universal (HK) and the 
Company
1.
China Universal 
Special Situation 
Fund SPC — 
CUAM Flexible 
Strategy Fund SP
Private fund 
HK$131 million 
as of March 2026
No
January 2026
Not applicable as it is 
not a partnership
Maples Fund 
Services 
(Cayman) 
Limited
The scheme and its ultimate 
beneficial owners are 
independent third parties 
of the Company, to the 
best of its knowledge.
(8) 
CUAM will hold Offer Shares in its capacity as the discretionary fund manager managing assets on behalf 
of its underlying clients. Each of such underlying clients is an independent third party of the Company, 
its subsidiaries, its Controlling Shareholders, its substantial shareholders, CUAM and Orient and the 
companies which are members of the same group of Orient. Details of such underlying clients are as 
follows:
Name of underlying clients
Ultimate beneficial owner(s) holding 30% or 
more interest (if any)
Global Mobile Internet Hybrid Fund 匯添富全球移動互聯
No single ultimate beneficial owner holds 30% or 
more interests
Global Consumer Industries 全球消費
No single ultimate beneficial owner holds 30% or 
more interests
SPDB China Universal Overseas fixed-income portfolio NO.1 
海外穩利一號
No single ultimate beneficial owner holds 30% or 
more interests
(9) 
CICC FT and China International Capital Corporation Limited will enter into a series of cross border 
delta-one OTC equity swap transactions (the “Gaoyi OTC Swaps”) with each other and the ultimate 
clients (the “CICC FT Ultimate Clients (Gaoyi)”), pursuant to which CICC FT will hold the Offer Shares 
on a non-discretionary basis to hedge the Gaoyi OTC Swaps while the economic risks and returns of 
the underlying Offer Shares are passed to the CICC FT Ultimate Clients (Gaoyi), subject to customary 
fees and commissions. The Gaoyi OTC Swaps will be fully funded by the CICC FT Ultimate Clients 
(Gaoyi). During the terms of the Gaoyi OTC Swaps, all economic returns of the Offer Shares subscribed 
by CICC FT will be passed to the CICC FT Ultimate Clients (Gaoyi) and all economic losses shall be 
borne by the CICC FT Ultimate Clients (Gaoyi) through the Gaoyi OTC Swaps, and CICC FT will not 
take part in any economic return or bear any economic loss in relation to the Offer Shares. The Gaoyi 
OTC Swaps are linked to the performance of the Offer Shares and the CICC FT Ultimate Clients (Gaoyi) 
may, after expiration of the lock-up period beginning from the date of the cornerstone agreement entered 
into between CICC FT and the Company and ending on the date which is six months from the Listing 
Date, request CICC FT to redeem it at their own discretions, upon which CICC FT shall dispose of the 
Offer Shares and settle Gaoyi OTC Swaps in cash in accordance with the terms and conditions of the 
Gaoyi OTC Swaps. Despite that CICC FT will hold the legal title of the Offer Shares by itself, it will not 
exercise the voting rights attaching to the relevant Offer Shares during the terms of the Gaoyi OTC Swaps 
according to its internal policy.

<<<PAGE 26>>>
– 26 –
The CICC FT Ultimate Clients (Gaoyi) are certain investment funds (the “Gaoyi Funds”) managed by 
Shanghai Gaoyi, including (i) Gaoyi Xiaofeng No. 1 Ruiyuan Securities Investment Fund (高毅－曉峰
1號睿遠證券投資基金), (ii) Gaoyi Xiaofeng No. 2 Zhixin Fund (高毅曉峰2號致信基金), (iii) Gaoyi 
Qingrui No.6 Ruixing Fund (高毅慶瑞6號瑞行基金), (iv) Gaoyi Qingrui Zhenxuan Fengyuan Private 
Securities Investment Fund (高毅慶瑞臻選灃源私募證券投資基金), (v) Gaoyi Qingrui Jingxuan Ruixiang 
Convertible Bond Multi-Strategy Private Fund (高毅慶瑞精選瑞祥可轉債多策略私募基金), (vi) Gaoyi 
Liwei Jingxuan Weishi Fund (高毅利偉精選唯實基金), (vii) Gaoyi Renhao Youxuan Zhifu Private 
Securities Investment Fund (高毅任昊優選致福私募證券投資基金), (viii) Gaoyi Renhao Long-term Value 
Langrun Private Securities Investment Fund (高毅任昊長期價值朗潤私募證券投資基金), (ix) Gaoyi 
Renhao Zhenxuan Chunhe Private Securities Investment Fund (高毅任昊臻選春和私募證券投資基金), 
and (x) Gaoyi Renhao Jingxuan Chengze Private Securities Investment Fund (高毅任昊精選承澤私募證
券投資基金), and none of the underlying clients of each of the Gaoyi Funds hold 30% or more interest 
in such fund. Shanghai Gaoyi is a limited partnership established in the PRC, which is engaged in asset 
management and investment management with a primary focus on investments in secondary market. The 
managing partner of Shanghai Gaoyi is Shanghai Gaoyi Investment Management Co., Ltd. (上海高毅投資
管理有限公司). Each of the CICC FT Ultimate Clients (Gaoyi) is an independent third party of CICC FT, 
CICCHKS and the companies which are members of the same group of CICCHKS.
DISCLAIMER
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
and Hong Kong Securities Clearing Company Limited take no responsibility for the 
contents of this announcement, make no representation as to its accuracy or completeness 
and expressly disclaim any liability whatsoever for any loss howsoever arising from or in 
reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in 
or into the United States (including its territories and possessions, any state of the United 
States and the District of Columbia). This announcement does not constitute or form a 
part of any offer or solicitation to purchase or subscribe for the Offer Shares in the United 
States or in any other jurisdictions. The Offer Shares have not been, and will not be, 
registered under the United States Securities Act of 1933 as amended from time to time (the 
“U.S. Securities Act”) or securities law of any state or other jurisdiction of the United 
States. The Offer Shares may not be offered, sold, pledged or otherwise transferred within 
the United States, except pursuant to an exemption from the registration requirements 
of the U.S. Securities Act and U.S. Investment Company Act of 1940, as amended (“U.S. 
Investment Company Act”), and in compliance with any applicable state securities laws. 
There will be no public offer of the Offer Shares in the United States.
The Offer Shares are being offered and sold outside the United States to investors that 
are not U.S. persons nor persons acquiring for the account or benefit of U.S. persons in 
reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation 
or offer to acquire, purchase or subscribe for securities. This announcement is not a 
prospectus. Potential investors should read the Prospectus dated June 30, 2026 issued by 
Nexchip Semiconductor Corporation for detailed information about the Global Offering 
described below before deciding whether or not to invest in the H Shares thereby being 
offered.

<<<PAGE 27>>>
– 27 –
*Potential investors of the Offer Shares should note that the Sole Sponsor and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be 
entitled to terminate their obligations under the Hong Kong Underwriting Agreement with 
immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting — Underwriting Agreements — Hong Kong Underwriting Agreement — 
Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong 
time) on the Listing Date (which is currently expected to be on July 10, 2026).
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering (before any exercise of the 
Over-allotment Option), the total market value of the H Shares to be held by the public is 
above HK$6,982 million, calculated on the Offer Price of HK$32.30 per H Share, representing 
approximately 10.0% of the total issued share capital of the Company (excluding 62,088,500 
A Shares repurchased by the Company as treasury shares), which is higher than the prescribed 
expected market value of H Shares required to be held in public hands of not less than 
HK$3,000,000,000 under Rule 19A.13A(2)(b) of the Listing Rules, thereby satisfying Rule 
19A.13A(2) of the Listing Rules at the time of the Listing.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not 
be counted towards the free float of the H Shares of the Company at the time of Listing. Based 
on the final Offer Price of HK$32.30 per H Share, the total market value of the H Shares 
counted towards free float is approximately HK$3,497 million the Company confirms it meets 
the free float requirement under Rule 19A.13C(2)(b) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering (before 
any exercise of the Over-allotment Option): (i) no placee will, individually, be placed more 
than 10% of the enlarged issued share capital of the Company immediately after the Global 
Offering; (ii) there will not be any new substantial Shareholder under the Listing Rules 
immediately after the Global Offering; (iii) the three largest public shareholders of the 
Company do not hold more than 50% of the H shares in public hands at the time of the Listing 
in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 
300 holders of H Shares at the time of the Listing in compliance with Rule 8.08(2) of the 
Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, July 
10, 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting — Underwriting 
Agreements — Hong Kong Underwriting Agreement — Grounds for Termination” in the 
Prospectus has not been exercised. Investors who trade the H Shares on the basis of publicly 
available allocation details prior to the receipt of H Share certificates or prior to the H Share 
certificates becoming valid evidence of title do so entirely at their own risk.

<<<PAGE 28>>>
– 28 –
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Friday, 
July 10, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Friday, July 10, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 100 H Shares each, and the stock code of the H Shares 
will be 2249.
By order of the Board
Nexchip Semiconductor Corporation
合肥晶合集成電路股份有限公司
Mr. Tsai Kuo-Chih
Executive Director and chairperson of the Board
Hong Kong, July 9, 2026
As at the date of this announcement, the Board comprises: (i) Mr. Tsai Kuo-Chih and Mr. Zhu 
Caiwei as Executive Directors; (ii) Mr. Lu Qinhang, Ms. Chen Xiaobei, Mr. Guo Zhaozhi and 
Mr. Qiu Wensheng as Non-executive Directors; and (iii) Prof. An Guangshi, Prof. Lin Zhiting 
and Mr. Chen Ting as Independent non-executive Directors.
