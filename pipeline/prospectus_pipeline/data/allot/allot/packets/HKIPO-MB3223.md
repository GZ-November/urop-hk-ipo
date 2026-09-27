# 配发结果公告抽取任务：3223.HK Ingenic Semiconductor Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**24/08/2026 22:29**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0824/2026082401907.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3223.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
1
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) 
and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the prospectus dated August 17, 2026 (the “Prospectus”) issued by Ingenic Semiconductor Co., Ltd. (北京
君正集成電路股份有限公司) (the “Company”).
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
In connection with the Global Offering, Guotai Junan Securities (Hong Kong) Limited as stabilizing manager (the 
“Stabilizing Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, to the extent 
permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect 
transactions with a view to stabilizing or supporting the market price of the H Shares at such price, in such amounts 
and in such manners as the Stabilizing Manager, its affiliates or any person acting for it may determine and at a 
level higher than that which might otherwise prevail for a limited period after the Listing Date. However, there is 
no obligation on the Stabilizing Manager (or its affiliates or any person acting for it) to conduct any such stabilizing 
action. Such stabilizing action, if taken, (a) will be conducted at the absolute discretion of the Stabilizing Manager (or 
its affiliates or any person acting for it) and in what the Stabilizing Manager reasonably regards as the best interest 
of our Company, (b) may be discontinued at any time and (c) is required to be brought to an end within 30 days of 
the last day for lodging applications under the Hong Kong Public Offering (which is Saturday, September 19, 2026). 
Such stabilizing action, if taken, may be effected in all jurisdictions where it is permissible to do so, in each case in 
compliance with all applicable laws, rules and regulatory requirements, including the Securities and Futures (Price 
Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures 
Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Saturday, September 19, 
2026). After this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the 
price of the H Shares, could fall.
Potential investors of the Offer Shares should note that the Sole Sponsor and the Sponsor-Overall Coordinator (for 
itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong 
Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the paragraph 
headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently 
expected to be on or about Tuesday, August 25, 2026).

<<<PAGE 2>>>
2
Ingenic Semiconductor Co., Ltd.
北京君正集成電路股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under
the Global Offering
:
31,287,300 H Shares (subject to the
 Over-allotment Option)
Number of Hong Kong Offer Shares
:
3,128,800 Shares
Number of International Offer Shares
:
28,158,500 H Shares (subject to
 Over-allotment Option)
Final Offer Price
:
HK$100.00 per H Share plus brokerage
 of 1.0%, SFC transaction levy of
 0.0027%, Stock Exchange trading fee
 of 0.00565% and AFRC transaction
 levy of 0.00015%
Nominal value
:
RMB1.00 per H Share
Stock code
:
3223
Sole Sponsor, Sponsor-Overall Coordinator, Joint Global Coordinator,
Joint Bookrunner and Joint Lead Manager
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners
and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
INGENIC SEMICONDUCTOR CO., LTD.
北京君正集成電路股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND 
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated August 17, 2026 (the “Prospectus”) issued by 
Ingenic Semiconductor Co., Ltd. (北京君正集成電路股份有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
H Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company Information
Stock Code
3223
Stock short name
INGENIC
Dealings commencement date
August 25, 2026*
* see note at the end of the announcement
Price Information
Final Offer Price
HK$100.00
Maximum Offer Price
HK$102.80
Offer Shares and Share Capital
Number of Offer Shares (subject to the Over-allotment Option)
31,287,300
Number of Offer Shares in Hong Kong Public Offering
3,128,800
Number of Offer Shares in International Offering (subject to 
the Over-allotment Option)
28,158,500
Number of issued Shares upon Listing (before any exercise of 
the Over-allotment Option)
514,951,667
Over-allocation
No. of Offer Shares over-allocated
4,693,000
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.

<<<PAGE 4>>>
4
Proceeds
Gross proceeds (Note)
HK$3,128.7 million
Less: Estimated listing expenses payable based on Final Offer 
Price
HK$(74.1) million
Net proceeds
HK$3,054.6 million
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The Company 
will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if any) for the 
purposes as set out in the section headed “Future Plans and Use of Proceeds” in the Prospectus on a pro rata basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
141,851
No. of successful applications
25,349
Subscription level
927.37 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong Public 
Offering
3,128,800
Final no. of Offer Shares under the Hong Kong Public Offering
3,128,800
% of Offer Shares initially available under the Hong Kong Public 
Offering to the Global Offering
10%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
 www.eipo.com.hk/eIPOAllotment
 to perform a search by identification document number or 
 www.eipo.com.hk/eIPOAllotment
 for the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
101
Subscription Level
8.43 times
No. of Offer Shares initially available under the International Offering
28,158,500
Final no. of Offer Shares under the International Offering
28,158,500
% of Offer Shares initially available under the International Offering to 
the Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a 
waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit the Company to allocate certain Offer Shares in the International Offering 
to certain Permitted Existing Shareholders and/or their close associates and (b) a consent under 
Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to, among other 
things, allocate further H Shares in the International Offering to certain Cornerstone Investors and/
or their close associates, (i) none of the Offer Shares subscribed by the placees and the public have 
been financed directly or indirectly by the Company, any of the Directors, chief executive of the 
Company, existing Shareholders of the Company or any of its subsidiaries or their respective close 
associates; and (ii) none of the placees and the public who have purchased the Offer Shares are 
accustomed to taking instructions from the Company, any of the Directors, chief executive of the 
Company, existing Shareholders of the Company or any of its subsidiaries or their respective close 
associates in relation to the acquisition, disposal, voting or other disposition of H Shares registered 
in his/her/its name or otherwise held by him/her/it.

<<<PAGE 6>>>
6
The placees in the International Offering include the following:
Cornerstone Investors
Investor Note 1
No. of Offer  
Shares allocated Note 2
% of total issued 
H Shares after the 
Global Offering 
(assuming the Over-
allotment option is 
not exercised) Note 3
% of total issued 
share capital in the 
Company after the 
Global Offering 
(assuming the Over-
allotment option is 
not exercised)
Existing 
Shareholders or their 
close associates
Emerald Prime
4,706,800
15.04%
0.91%
No
GF Fund
2,353,400
7.52%
0.46%
Yes
Perseverance Asset Management
757,000
2.42%
0.15%
No
Shanghai Gaoyi and HTCI (in 
connection with the Huatai 
Back-to-back TRS and the 
Huatai Client TRS)
784,400
2.51%
0.15%
No
Huaqin Singapore
1,176,700
3.76%
0.23%
No
ICBC Wealth
1,176,700
3.76%
0.23%
Yes
Arrow Target
1,019,800
3.26%
0.20%
No
China Universal (HK)
941,300
3.01%
0.18%
Yes
CloudAlpha Capital
941,300
3.01%
0.18%
No
Heading Pioneer 10 Fund LPF
784,400
2.51%
0.15%
No
Dream’ee HK Fund
392,200
1.25%
0.08%
No
Total
15,034,000
48.05%
2.92%
Notes:
1. 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in 
the Prospectus.
2. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering (assuming the Over-allotment Option is not exercised).
3. 
Only taking into account the Shares allocated to the relevant investors as cornerstone investors under the 
Global Offering. In addition to the Offer Shares subscribed for as Cornerstone Investors, certain Cornerstone 
Investors were allocated further Offer Shares as placees in the International Offering. Please refer to the 
section headed “Allotment Results Details – International Offering – Allottees with Waivers/Consents 
Obtained” in this announcement for details. Only the Offer Shares subscribed for as Cornerstone Investors are 
subject to lock-up as indicated below. For details, please refer to the section headed “Lock-up Undertakings – 
Cornerstone Investors” in this announcement.

<<<PAGE 7>>>
7
Allottees with Waivers/Consents Obtained
Investor
No. of Offer  
Shares allocated
% of total issued 
H Shares after the 
Global Offering 
(assuming the Over-
allotment option is 
not exercised) Note 4
% of total issued 
share capital in the 
Company after the 
Global Offering 
(assuming the Over-
allotment option is 
not exercised)
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the 
Placing Guidelines in relation to subscription for H Shares by Permitted Existing Shareholders holding more than 1% of the 
issued share capital of the Company immediately prior to the completion of the Global Offering and/or their close associates Note 1
E Fund Management (Hong 
Kong) Co., Limited
78,400
0.25%
0.02%
Close associate of existing 
Shareholder
China Life Franklin Asset 
Management Co., Limited
156,800
0.50%
0.03%
Close associate of existing 
Shareholder
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of 
further H Shares to existing Shareholders and Cornerstone Investors and/or their close associates Note 2
GF Fund
1,239,400
3.96%
0.24%
A Cornerstone Investor and an 
existing Shareholder
GF International Investment 
Management Limited 
(“GF International”)
94,000
0.30%
0.02%
A close associate of GF Fund, 
a Cornerstone Investor and 
an existing Shareholder
China Universal (HK)
376,500
1.20%
0.07%
A Cornerstone Investor and an 
existing Shareholder
ICBC(ASIA)LTD-ICBC 
LTD-GFAM GYGGCL 
NO.2 AMA
39,200
0.13%
0.01%
A close associate of ICBC 
Wealth, a Cornerstone 
Investor, and a close 
associate of an existing 
Shareholder
ICBC(ASIA)LTD-
ICBC LTD-GFAM 
GYJXCL NO.1 ASSET 
MANAGEMENT AC
78,400
0.25%
0.02%
A close associate of ICBC 
Wealth, a Cornerstone 
Investor, and a close 
associate of an existing 
Shareholder
EPF GUANGYING 
OVERSEAS NO.38 QDII 
SMA
39,200
0.13%
0.01%
A close associate of ICBC 
Wealth, a Cornerstone 
Investor, and a close 
associate of an existing 
Shareholder

<<<PAGE 8>>>
8
Investor
No. of Offer  
Shares allocated
% of total issued 
H Shares after the 
Global Offering 
(assuming the Over-
allotment option is 
not exercised) Note 4
% of total issued 
share capital in the 
Company after the 
Global Offering 
(assuming the Over-
allotment option is 
not exercised)
Relationship
ICBC(ASIA)LTD-ICBC 
LTD-CICC Gong Yin 
JXCL No.1 CIS
235,100
0.75%
0.05%
A close associate of ICBC 
Wealth, a Cornerstone 
Investor, and a close 
associate of an existing 
Shareholder
SpreadCom Limited 
(“SpreadCom”)
392,200
1.25%
0.08%
A close associate of Arrow 
Target, a Cornerstone 
Investor
Huaqin Singapore
392,200
1.25%
0.08%
A Cornerstone Investor
Head Pioneer 10 Fund LPF
235,300
0.75%
0.05%
A Cornerstone Investor
Head Pioneer 8 Fund LPF
62,700
0.20%
0.01%
A close associate of Head 
Pioneer 10 Fund LPF, a 
Cornerstone Investor
Dream’ee JuneBeast Fund 
(“Dream’ee JuneBeast”)
78,400
0.25%
0.02%
A close associate of Dreem’ee 
HK Fund, a Cornerstone 
Investor
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants 
in relation to allocations to connected clients Note 3
Shanghai Gaoyi and HTCI 
(in connection with the 
Huatai Back-to-back TRS 
and the Huatai Client 
TRS)
784,400
2.51%
0.15%
Connected client as 
Cornerstone Investor
Shanghai GTHT
1,176,700
3.76%
0.23%
Connected client investing as 
an asset manager of ICBC 
Wealth as Cornerstone 
Investor and placee
China Universal (HK)
1,317,800
4.21%
0.26%
Connected client as 
Cornerstone Investor and 
placee
Fullgoal Fund Management 
Co., Ltd. (“Fullgoal 
Fund”)
235,200
0.75%
0.05%
Connected client as placee
China Southern Asset 
Management Co., Ltd. 
(“China Southern”)
313,700
1.00%
0.06%
Connected client as placee

<<<PAGE 9>>>
9
Investor
No. of Offer  
Shares allocated
% of total issued 
H Shares after the 
Global Offering 
(assuming the Over-
allotment option is 
not exercised) Note 4
% of total issued 
share capital in the 
Company after the 
Global Offering 
(assuming the Over-
allotment option is 
not exercised)
Relationship
China International Capital 
Corporation Limited 
(“CICC”)
235,100
0.75%
0.05%
Connected client as placee
Orient Asset Management 
(Hong Kong) Limited 
(“Orient AM”)
15,600
0.05%
0.003%
Connected client as placee
Notes:
1. 
The Stock Exchange has granted a waiver from strict compliance with the requirements under Rule 10.04 
of the Listing Rules and consent under Paragraph 1C(2) of the Placing Guidelines to permit H Shares in the 
International Offering to be placed to certain Permitted Existing Shareholders. Please refer to the section 
headed “Waivers, Consents and Exemption – Allocation of H Shares to Existing Minority Shareholders 
and Their Close Associates” in the Prospectus for details. To the best knowledge, information and belief 
of the Company after due enquiry, details of the allocations to the Permitted Existing Shareholders holding 
more than 1% of the issued share capital of the Company immediately prior to the completion of the Global 
Offering have been disclosed in this announcement.
2. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details – International Offering – Cornerstone Investors” in this announcement. For details of the 
consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further H 
Shares to the Cornerstone Investors, please refer to the section headed “Others/Additional Information – 
Allocations of Offer Shares to the Cornerstone Investors and their close associates as placees with a consent 
under Chapter 4.15 of the Guide for New Listing Applicants” in this announcement.
3. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients, please refer to the section headed 
“Others/Additional Information – Placing to connected clients with a prior consent under paragraph 1C(1) of 
the Placing Guidelines” in this announcement.
4. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering (assuming the Over-allotment Option is not exercised).

<<<PAGE 10>>>
10
LOCK-UP UNDERTAKINGS
Cornerstone Investors
Name
No. of H 
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
option is not 
exercised) Note 1
% of total issued 
share capital in 
the Company 
subject to lock-
up undertakings 
upon Listing 
(assuming the 
Over-allotment 
option is not 
exercised)
Last day subject 
to the lock-up 
undertakings Note 2
Emerald Prime
4,706,800
15.04%
0.91%
February 24, 2027
GF Fund
2,353,400
7.52%
0.46%
February 24, 2027
Perseverance Asset 
Management
757,000
2.42%
0.15%
February 24, 2027
Shanghai Gaoyi and 
HTCI (in connection 
with the Huatai Back-
to-back TRS and the 
Huatai Client TRS)
784,400
2.51%
0.15%
February 24, 2027
Huaqin Singapore
1,176,700
3.76%
0.23%
February 24, 2027
ICBC Wealth
1,176,700
3.76%
0.23%
February 24, 2027
Arrow Target
1,019,800
3.26%
0.20%
February 24, 2027
China Universal (HK)
941,300
3.01%
0.18%
February 24, 2027
CloudAlpha Capital
941,300
3.01%
0.18%
February 24, 2027
Heading Pioneer 10  
Fund LPF
784,400
2.51%
0.15%
February 24, 2027
Dream’ee HK Fund
392,200
1.25%
0.08%
February 24, 2027
Total
15,034,000
48.05%
2.92%
Notes:
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering (assuming the Over-allotment Option is not exercised).
2. 
In accordance with the relevant Cornerstone Investment Agreements, the required lock-up period commences 
from (and inclusive of) the Listing Date and ending on (and inclusive of) the date falling six (6) months 
after the Listing Date (being February 24, 2027). The Cornerstone Investors will cease to be prohibited from 
disposing of or transferring H Shares subscribed pursuant to the relevant Cornerstone Investment Agreements 
after the indicated date.

<<<PAGE 11>>>
11
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
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
the Over-
allotment 
Option is not 
exercised)
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
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)
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
4,706,800
16.72%
14.33%
15.04%
13.08%
4,706,800
0.91%
0.91%
Top 5
13,937,500
49.50%
42.43%
44.55%
38.74%
13,937,500
2.71%
2.68%
Top 10
21,165,700
75.17%
64.43%
67.65%
58.83%
21,165,700
4.11%
4.07%
Top 25
29,201,500
103.70%
88.89%
93.33%
81.16%
29,201,500
5.67%
5.62%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 12>>>
12
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
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
the Over-
allotment 
Option is not 
exercised)
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
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)
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
4,706,800
16.72%
14.33%
15.04%
13.08%
4,706,800
0.91%
0.91%
Top 5
13,937,500
49.50%
42.43%
44.55%
38.74%
13,937,500
2.71%
2.68%
Top 10
21,165,700
75.17%
64.43%
67.65%
58.83%
21,165,700
4.11%
4.07%
Top 25
29,201,500
103.70%
88.89%
93.33%
81.16%
29,201,500
5.67%
5.62%
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 13>>>
13
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
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
the Over-
allotment 
Option is not 
exercised)
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
Number of 
Shares held 
upon 
Listing
#
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)
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
–
0.00%
0.00%
0.00%
0.00%
–
58,411,378
11.34%
11.24%
Top 5
–
0.00%
0.00%
0.00%
0.00%
–
110,099,047
21.38%
21.19%
Top 10
3,765,200
13.37%
11.46%
12.03%
10.46%
3,765,200
150,846,152
29.29%
29.03%
Top 25
14,503,100
51.51%
44.15%
46.35%
40.31%
14,503,100
194,941,893
37.86%
37.51%
Note:
* 
Ranking of Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
# 
Among the top 25 placees, certain placees are also existing Shareholders. To the best knowledge, information 
and belief of the Company after due enquiry, details of the allocations to the Permitted Existing Shareholders 
holding more than 1% of the issued share capital of the Company immediately prior to the completion of the 
Global Offering have been disclosed in this announcement. Please refer to the section headed “Allottees with 
Waivers/Consents Obtained – Allottees with waiver from strict compliance with Rule 10.04 of the Listing 
Rules and consent under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by 
Permitted Existing Shareholders holding more than 1% of the issued share capital of the Company immediately 
prior to the completion of the Global Offering and/or their close associates” in this announcement. For the 
top 25 placees who are also existing shareholders holding less than 0.05% of the issued share capital of the 
Company immediately prior to the completion of the Global Offering, the number of A Shares held by them is 
not counted into the number of Shares held upon Listing.

<<<PAGE 14>>>
14
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
Number of  
H Shares  
applied for
Number of  
valid  
applications
Basis of allocation/ballot
Approximate  
% allotted of  
the total no. of  
H Shares  
applied for
POOL A
100
35,805
95 out of 35,805 to receive 100 Shares
0.27%
200
8,369
45 out of 8,369 to receive 100 Shares
0.27%
300
5,780
46 out of 5,780 to receive 100 Shares
0.27%
400
9,178
98 out of 9,178 to receive 100 Shares
0.27%
500
4,502
60 out of 4,502 to receive 100 Shares
0.27%
600
1,878
30 out of 1,878 to receive 100 Shares
0.27%
700
1,805
34 out of 1,805 to receive 100 Shares
0.27%
800
1,624
35 out of 1,624 to receive 100 Shares
0.27%
900
3,998
96 out of 3,998 to receive 100 Shares
0.27%
1,000
7,361
196 out of 7,361 to receive 100 Shares
0.27%
1,500
3,823
152 out of 3,823 to receive 100 Shares
0.27%
2,000
3,078
164 out of 3,078 to receive 100 Shares
0.27%
2,500
2,034
135 out of 2,034 to receive 100 Shares
0.27%
3,000
1,951
156 out of 1,951 to receive 100 Shares
0.27%
3,500
1,416
132 out of 1,416 to receive 100 Shares
0.27%
4,000
1,384
147 out of 1,384 to receive 100 Shares
0.27%
4,500
1,319
158 out of 1,319 to receive 100 Shares
0.27%
5,000
2,566
341 out of 2,566 to receive 100 Shares
0.27%
6,000
1,756
280 out of 1,756 to receive 100 Shares
0.27%
7,000
1,333
248 out of 1,333 to receive 100 Shares
0.27%
8,000
1,235
263 out of 1,235 to receive 100 Shares
0.27%
9,000
1,364
326 out of 1,364 to receive 100 Shares
0.27%
10,000
7,570
2,012 out of 7,570 to receive 100 Shares
0.27%
20,000
5,184
2,756 out of 5,184 to receive 100 Shares
0.27%
30,000
3,512
2,801 out of 3,512 to receive 100 Shares
0.27%
40,000
4,553
100 Shares plus 285 out of 4,553 to receive additional 100 Shares
0.27%
 
124,378
Total number of Pool A successful applicants: 15,359

<<<PAGE 15>>>
15
Number of  
H Shares  
applied for
Number of  
valid  
applications
Basis of allocation/ballot
Approximate  
% allotted of  
the total no. of  
H Shares  
applied for
POOL B
50,000
5,000
1,692 out of 5,000 to receive 100 Shares
0.07%
60,000
2,441
991 out of 2,441 to receive 100 Shares
0.07%
70,000
1,389
658 out of 1,389 to receive 100 Shares
0.07%
80,000
1,028
556 out of 1,028 to receive 100 Shares
0.07%
90,000
802
488 out of 802 to receive 100 Shares
0.07%
100,000
3,733
2,525 out of 3,733 to receive 100 Shares
0.07%
200,000
1,367
100 Shares plus 482 out of 1,367 to receive additional 100 Shares
0.07%
300,000
615
200 Shares plus 18 out of 615 to receive additional 100 Shares
0.07%
400,000
325
200 Shares plus 229 out of 325 to receive additional 100 Shares
0.07%
500,000
203
300 Shares plus 77 out of 203 to receive additional 100 Shares
0.07%
600,000
107
400 Shares plus 6 out of 107 to receive additional 100 Shares
0.07%
700,000
66
400 Shares plus 48 out of 66 to receive additional 100 Shares
0.07%
800,000
55
500 Shares plus 23 out of 55 to receive additional 100 Shares
0.07%
900,000
40
600 Shares plus 3 out of 40 to receive additional 100 Shares
0.07%
1,000,000
79
600 Shares plus 60 out of 79 to receive additional 100 Shares
0.07%
1,250,000
51
800 Shares plus 23 out of 51 to receive additional 100 Shares
0.07%
1,564,400
172
1,000 Shares plus 100 out of 172 to receive additional 100 Shares
0.07%
 
17,473
Total number of Pool B successful applicants: 9,990
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.

<<<PAGE 16>>>
16
OTHERS/ADDITIONAL INFORMATION
Allocations of Offer Shares to Permitted Existing Shareholders and/or their close associates
The Company has applied for, and the Stock Exchange has granted, a waiver from strict compliance 
with Rule 10.04 of, and a consent under paragraph 1C(2) of Appendix F1 to, the Listing Rules to 
permit H Shares in the International Offering to be placed to certain existing minority Shareholders 
who (i) hold less than 5% voting rights of the Company prior to the completion of the Global 
Offering and (ii) are not and will not become (upon the completion of the Global Offering) core 
connected persons of the Company or the close associates of any such core connected persons 
(together, the “Permitted Existing Shareholders”) and/or their close associates, subject to, among 
others, the following conditions:
(a) 
each of the Permitted Existing Shareholders to whom the Company may allocate H Shares in 
the International Offering is interested in less than 5% voting rights in the Company prior to 
the completion of the Global Offering;
(b) 
each of the Permitted Existing Shareholders is not, and will not be, a core connected person 
of the Company or any close associate of any such core connected person immediately prior 
to or following the Global Offering;
(c) 
none of the Permitted Existing Shareholders has the right to appoint any Director and/or has 
any other special rights in the Company;
(d) 
allocation to the Permitted Existing Shareholders or their close associates will not affect the 
Company’s ability to satisfy the public float requirement as prescribed under Rule 19A.13A 
of the Listing Rules;
(e) 
no preferential treatment is given to the Permitted Existing Shareholders or their respective 
close associates (other than the assured entitlement for a cornerstone investor); and
(f) 
details of the allocation to the Permitted Existing Shareholders and/or their respective close 
associates holding more than 1% of the issued share capital of the Company immediately 
prior to the completion of the Global Offering have been disclosed in this announcement.
Please refer to the section headed “Waivers, Consents and Exemption – Allocation of H Shares to 
Existing Minority Shareholders and Their Close Associates” in the Prospectus for further details of 
the waiver and consent.
Each of the Sole Sponsor and the Company has provided the required confirmations as elaborated 
in the Prospectus. In particular, as the Company’s A Shares are listed on the ChiNext of the 
Shenzhen Stock Exchange since 2011, the Company has a highly extensive base of existing 
Shareholders and disclosure of details of allocations to all Permitted Existing Shareholders will not 
be meaningful to investors, the proposed disclosure threshold, i.e. condition (f) of the waiver and 
consent which provides that details of the allocation to the Permitted Existing Shareholders holding 
more than 1% of the issued share capital of the Company immediately prior to the completion of 
the Global Offering will be disclosed in this announcement, is appropriate.

<<<PAGE 17>>>
17
Allocations of Offer Shares to the Cornerstone Investors and their close associates as placees 
with a consent under Chapter 4.15 of the Guide for New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 
of the Guide for New Listing Applicants to permit the Company to allocate further Offer Shares in 
the International Offering to certain existing Shareholders and Cornerstone Investors and/or their 
close associates (the “Size-based Exemption Participants”) as placees, subject to the following 
conditions (the “Size-based Exemption”):
(a) 
the final offering size of the Global Offering, assuming the Over-allotment Option is not 
exercised, will be of a total value of at least HK$1 billion;
(b) 
the Offer Shares allocated to all existing Shareholders (whether as cornerstone investors and/
or as placees) as permitted under the size-based exemption do not exceed 30% of the total 
number of the Offer Shares;
(c) 
each director and chief executive of the Company has confirmed that no Offer Shares 
have been allocated to them or their respective close associates pursuant to the size-based 
exemption;
(d) 
the allocation to the Size-based Exemption Participants will not affect the Company’s ability 
to satisfy the public float requirement under Rule 19A.13A of the Listing Rules; and
(e) 
details of the allocation to the relevant Size-based Exemption Participants under the 
size-based exemption will be disclosed in the allotment results announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange. For details of the allocation to Size-based Exemption Participants, 
please refer to the section headed “Allotment Results Details – International Offering – Allottees 
with Waivers/Consents Obtained” in this announcement.

<<<PAGE 18>>>
18
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit HTCI (in connection with the 
Huatai TRS) and ICBC Wealth (through Shanghai GTHT as the asset manager) to participate in 
the Global Offering as cornerstone investors. For details of the consent granted, please refer to 
“Waivers, Consents and Exemption – Consent in respect of the Proposed Subscription of H Shares 
by Connected Clients” in the Prospectus.
In addition, under the International Offering, certain Offer Shares were placed to connected clients 
of their connected distributors pursuant to the Placing Guidelines. Details of the placement to 
connected clients are set out below. The Company has applied to the Stock Exchange for, and the 
Stock Exchange has granted, consents under paragraph 1C(1) of the Placing Guidelines to permit 
the Company to allocate such Offer Shares in the International Offering to the connected clients. 
The allocation of Offer Shares to such connected clients is in compliance with all the conditions 
under the consent granted by the Stock Exchange.
No.
Connected 
Distributor
Connected Client
Relationship with 
the Connected 
Distributor
Whether the 
connected 
client will hold 
the beneficial 
interests of the 
Offer Shares 
on a non-
discretionary 
basis or 
discretionary 
basis for 
independent 
third parties
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which is 
not authorised 
by the SFC or 
is expected to 
hold the Offer 
Shares on 
behalf of such 
scheme
Number of 
Offer Shares 
allocated 
to the 
Connected 
Client
Approximate 
percentage 
of total 
number of 
Offer Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
percentage 
of total 
Shares 
in issue 
immediately 
following the 
completion 
of Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
1.
HTFH
HTCI Note 1
HTFH and HTCI are 
fellow subsidiaries 
of Huatai 
Securities.
Non-
discretionary 
basis
No
784,400
2.51%
0.15%
2.
The Sponsor-Overall 
Coordinator
Shanghai GTHT 
acting as a 
qualified domestic 
institutional 
investor for ICBC 
Wealth Note 2
Sponsor-Overall 
Coordinator 
and Shanghai 
GTHT are fellow 
subsidiaries of 
Guotai Haitong 
Securities Co., 
Ltd.
Non-
discretionary 
basis
No
392,300
1.25%
0.08%

<<<PAGE 19>>>
19
No.
Connected 
Distributor
Connected Client
Relationship with 
the Connected 
Distributor
Whether the 
connected 
client will hold 
the beneficial 
interests of the 
Offer Shares 
on a non-
discretionary 
basis or 
discretionary 
basis for 
independent 
third parties
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which is 
not authorised 
by the SFC or 
is expected to 
hold the Offer 
Shares on 
behalf of such 
scheme
Number of 
Offer Shares 
allocated 
to the 
Connected 
Client
Approximate 
percentage 
of total 
number of 
Offer Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Approximate 
percentage 
of total 
Shares 
in issue 
immediately 
following the 
completion 
of Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
3.
Orient Securities
China Universal 
(HK) 
Note 3
China Universal 
(HK) is a member 
of the same 
group of Orient 
Securities.
Discretionary
Yes
As 
Cornerstone 
Investor: 
941,300
3.01%
0.18%
As placee: 
376,500
1.02%
0.07%
4.
The Sponsor-Overall 
Coordinator 
and Haitong 
International 
Securities 
Company Limited 
(“Haitong 
International”)
Fullgoal  
Fund Note 4
Fullgoal fund is a 
member of the 
same group of 
companies as the 
Sponsor-Overall 
Coordinator 
and Haitong 
International.
Discretionary
Yes
235,200
0.75%
0.05%
5.
China International 
Capital 
Corporation 
Hong Kong 
Securities Limited 
(“CICCHKS”)
CICC acting as the 
asset manager for 
ICBC  
Wealth Note 5
CICCHKS is a 
member of the 
same group of 
companies as 
CICC.
Discretionary
Yes
235,100
0.75%
0.05%
6.
HTFH
China  
Southern Note 6
China Southern 
is a member of 
the same group 
of companies as 
HTFH.
Discretionary
No
313,700
1.00%
0.06%
7.
Orient Securities
Orient AM Note 7
Orient AM is a 
member of the 
same group of 
Orient Securities.
Discretionary
Yes
15,600
0.05%
0.003%

<<<PAGE 20>>>
20
Notes:
(1) 
HTCI will act as the single counterparty of a back-to-back total return swap transaction (the “Huatai Back-
to-back TRS”) to be entered into by HTCI and Huatai Securities in connection with a total return swap 
transaction (the “Huatai Client TRS”) fully funded by the ultimate clients (the “Ultimate Clients (Gaoyi)”), 
by which HTCI will ultimately pass the full economic return and loss of the Offer Shares allocated to HTCI to 
the Ultimate Clients (Gaoyi). HTCI will hold the Offer Shares on a non-discretionary basis to hedge the Huatai 
Back-to-back TRS in connection with the Huatai Client TRS, and will pass on the full economic return and 
loss of the Offer Shares ultimately to the Ultimate Clients (Gaoyi) through the Huatai Back-to-back TRS and 
the Huatai Client TRS, subject to customary fees and commissions. HTCI will not take part in any economic 
return or bear any economic loss in relation to the Offer Shares, save as customary fees and commission. The 
Ultimate Clients (Gaoyi) may, after expiration of the lock-up period beginning from the date of the Cornerstone 
Investment Agreement entered into among HTCI, the Company, the Sole Sponsor and the Sponsor-Overall 
Coordinator, and ending on the date which is six months from the Listing Date, request to early terminate the 
Huatai Client TRS at their own discretion. Upon the final maturity or early termination of the Huatai Client TRS 
by the Ultimate Clients (Gaoyi), HTCI will accordingly terminate the Huatai Back-to-back TRS and dispose 
of the Offer Shares on the secondary market and the Ultimate Clients (Gaoyi) will receive a final settlement 
amount of the Huatai Client TRS in cash in accordance with the terms and conditions of the Huatai Back-to-
back TRS and the Huatai Client TRS. It is proposed that HTCI will hold the legal title and the voting right 
of the Offer Shares by itself, and pass through the full economic return and loss ultimately to the Ultimate 
Clients (Gaoyi), each being an onshore client who places a Huatai Client TRS order with Huatai Securities in 
connection with the Global Offering. HTCI will not exercise the voting right of the Offer Shares during the 
tenor of the Huatai Back-to-back TRS. During the life of the Huatai Back-to-back TRS and the Huatai Client 
TRS, HTCI may continue to hold the Offer Shares in its custodian account, or to hold some or all of the Offer 
Shares in a prime brokerage account for stock borrowing purpose, which is consistent with market practice to 
lower its finance cost, provided that the economic interests are ultimately passed to the Ultimate Clients (Gaoyi).
The Ultimate Clients (Gaoyi) for the purpose of this place subscription are funds managed by Shanghai Gaoyi 
Asset Management Partnership (Limited Partnership) (上海高毅資產管理合夥企業(有限合夥)) (“Shanghai 
Gaoyi”) on a discretionary basis. Shanghai Gaoyi is a limited partnership established in the PRC, which is 
engaged in asset management and investment management with a primary focus on investments in secondary 
market. The managing partner of Shanghai Gaoyi is Shanghai Gaoyi Investment Management Co, Ltd. (上海
高毅投資管理有限公司). Perseverance Asset Management is an affiliate of Shanghai Gaoyi. As confirmed by 
Shanghai Gaoyi, there is no single ultimate beneficial owner holding 30% or more interests in respect of each 
of the Ultimate Clients (Gaoyi). To the best of HTCI’s knowledge after having made all reasonable inquiries, 
each of the Ultimate Clients (Gaoyi) is an independent third party of (i) the Company, the connected persons or 
associates thereof, and (ii) HTCI and the companies which are members of the same group of Huatai.
(2) 
ICBC Wealth has engaged Shanghai GTHT, a qualified domestic institutional investor as approved by the 
relevant PRC authority, to subscribe for and hold such Offer Shares on a non-discretionary basis on behalf of 
ICBC Wealth, in the name of Guotai Haitong Junxiang Wentuo QDII No.1 Collective Asset Management Plan 
Product (國泰海通君享穩拓QDII1號集合資產管理計劃). The Offer Shares to be placed to Shanghai GTHT 
are to be held on a non-discretionary basis on behalf of its underlying clients. Shanghai GTHT will hold the 
legal title and the voting right of the Offer Shares by itself, and pass through the full economic return and 
loss ultimately to ICBC Wealth. To the best of Shanghai GTHT’s knowledge after having made all reasonable 
inquiries, each of its underlying client and their ultimate beneficial owner(s) is an independent third party of the 
Company, the connected persons or associates thereof, Shanghai GTHT and the companies which are members 
of the same group of the Sponsor-Overall Coordinator.

<<<PAGE 21>>>
21
(3) 
China Universal (HK) is a wholly owned subsidiary of China Universal Asset Management Company Limited 
(“CUAM”). CUAM is owned by Orient Securities Co., Ltd, the group company of Orient Securities as to 
35.412%. As such, China Universal (HK) is a member of the same group of companies as Orient Securities 
and is therefore a connected client of Orient Securities. China Universal (HK) will hold the Offer Shares in 
its capacity as the discretionary fund manager for and on behalf of its underlying clients, each of which is 
an independent third party of the Company, its subsidiaries, China Universal (HK), Orient Securities and the 
companies which are members of the same group of companies as Orient Securities.
China Universal (HK) is investing on behalf of a collective investment scheme which is not authorized by the 
SFC, the details of which are as follows:
Name
Types and values 
of assets under 
management
Whether the 
scheme is publicly 
marketed
Scheme 
establishment date
Identities of the 
general partners 
and the 20 largest 
limited partners of 
the scheme where 
applicable
Identity of the scheme 
administrator
UBO of the scheme
China Universal 
Special Situation 
Fund SPC-CUAM 
Flexible Strategy 
Fund SP
Private Fund HK$1.3 
billion as of June 
2026
No
January 2026
Not applicable as it is 
not in partnership 
structure and does 
not have any general 
partner or limited 
partner
Maples Fund Services 
(Cayman) Limited
No single ultimate 
beneficial owner 
holds 30% or more 
interest
(4) 
Guotai Haitong is a shareholder of Fullgoal Fund, holding a 27.775% equity interest therein. The Sponsor-
Overall Coordinator and Haitong International, a non-syndicate distributor, is a subsidiary of Guotai Haitong. 
Accordingly, Fullgoal Fund is a connected client of the Sponsor-Overall Coordinator and Haitong International. 
Fullgoal Fund will hold the Offer Shares in its capacity as the discretionary fund manager managing assets 
for and on behalf of its underlying investors, each of which is an independent third party of the Company, its 
subsidiaries, the Fullgoal Fund, the Sponsor-Overall Coordinator, Haitong International and the companies 
which are members of the same group of the Sponsor-Overall Coordinator and Haitong International.

<<<PAGE 22>>>
22
Fullgoal Fund is investing on behalf of certain collective investment schemes which are not authorized by the 
SFC, the details of which are as follows:
Name
Whether the scheme in  
publicly marketed
Fund manager
UBO of fund manager
UBO of the scheme
ICBC Fullgoal global technology 
& internet fund
Publicly Marketed
Zhao Nianshen
N/A
No single ultimate beneficial 
owner holds 30% or more 
interest
ICBC Fullgoal China Small & 
Mid Cap (HK listed) Equity 
Fund
Publicly Marketed
Zhang Feng
N/A
No single ultimate beneficial 
owner holds 30% or more 
interest
CMB-FULLGOAL BLUE CHIP 
SELECTED EQUITY FUND 
(QDII)
Publicly Marketed
Wang Menghai
N/A
No single ultimate beneficial 
owner holds 30% or more 
interest
(5) 
CICCHKS is a non-syndicate distributor and a wholly owned subsidiary of CICC, and therefore a member of the 
same group of companies as CICC. Accordingly, CICC is a connected client of CICCHKS.
CICC is investing on behalf of a collective investment scheme which is not authorized by the SFC, the details 
of which are as follows:
Name
Types and values 
of assets under 
management
Whether the scheme 
is publicly marketed
Scheme  
establishment date
Identities of the general 
partners and the 20 largest 
limited partners of the scheme 
where applicable
Identity of the scheme 
administrator
CHINA INTERNATIONAL 
CAPITAL CORPORATION 
LTD – ICBC (ASIA)LTD-
ICBC LTD-CICC Gong Yin 
JXCL NO.1 CIS (中金工銀精
選策略1號QDII集合資產管理
計劃) (“CICC Gong Yin”)
Collective asset 
management plan
Value: RMB93,000,000
No
June 26, 2026
Not applicable as it is not in 
partnership structure and does 
not have any general partner 
or limited partner
CICC

<<<PAGE 23>>>
23
As confirmed by CICC, (i) ICBC Wealth Wisdom Joy Minimum Holding Period 180 Days Fixed Income Open-
End Net Value Wealth Management Product (工銀理財智悅最短持有180天固定收益類開放式淨值型理財產
品) (“ICBC Wealth Wisdom Joy”) owns 30% or more interest in CICC Gong Yin as an investor and there 
are no ultimate beneficial owners who hold 30% or more interest in ICBC Wealth Wisdom Joy; (ii) there are 
no ultimate beneficial owners who hold 30% or more interest in CICC Gong Yin; and (iii) each of the ultimate 
beneficial owners is an independent third party of the Company, its subsidiaries, CICC, CICCHKS and the 
companies which are members of the same group of companies as CICCHKS.
(6) 
China Southern is held by Huatai Securities Co., Ltd. as to 41.16%, which wholly owns HTFH. China Southern 
will hold the Offer Shares in its capacity as the discretionary fund manager for and on behalf of its underlying 
clients, each of which is an independent third party of the Company, its subsidiaries, China Southern, HTFH and 
the companies which are members of the same group of companies as HTFH.
(7) 
Orient Securities is a non-syndicate distributor and a wholly owned subsidiary of Orient Securities International 
Financial Group Limited (“Orient Securities International”). Since Orient AM is also a wholly-owned 
subsidiary of Orient Securities International, Orient AM is a member of the same group of Orient Securities and 
a connected client of Orient Securities. Orient AM will hold the Offer Shares in its capacity as the discretionary 
fund manager on behalf of its underlying clients, each of which is an independent third party of the Company, 
its subsidiaries, Orient Securities, Orient AM and the companies which are members of the same group of 
Orient Securities.
Orient AM is investing on behalf of a collective investment scheme which is not authorized by the SFC, the 
details of which are as follows:
Name
Types and 
values of 
assets under 
management
Whether 
the scheme 
is publicly 
marketed
Scheme 
establishment 
date
Identities of the 
general partners 
and the 20 
largest limited 
partners of the 
scheme where 
applicable
Identity of 
the scheme 
administrator
UBO of the 
scheme
Orient Asset Mgt 
(HK) Ltd-OSR 
Selective No.4
Discretionary 
account, 
US$30 million
No
August 22, 
2024
Not applicable 
as it is not in 
partnership 
structure and 
does not have 
any general 
partner or 
limited partner
Agricultural 
Bank of China, 
Hong Kong 
Branch
Zhang Ziyao 
holds 100% 
interest in 
Orient Asset 
Mgt (HK) Ltd-
OSR Selective 
No.4

<<<PAGE 24>>>
24
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or 
any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer 
or solicitation to purchase or subscribe for the Offer Shares in the United States or in any other 
jurisdictions. The Offer Shares have not been, and will not be, registered under the United States 
Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or securities 
law of any state or other jurisdiction of the United States. The Offer Shares may not be offered, 
sold, pledged or otherwise transferred within the United States, except pursuant to an exemption 
from the registration requirements of the U.S. Securities Act and U.S. Investment Company Act 
of 1940, as amended (“U.S. Investment Company Act”), and in compliance with any applicable 
state securities laws. There will be no public offer of the Offer Shares in the United States.
The Offer Shares are being offered and sold outside the United States to investors that are not 
U.S. persons nor persons acquiring for the account or benefit of U.S. persons in reliance on 
Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated August 17, 2026 issued by Ingenic Semiconductor 
Co., Ltd. (北京君正集成電路股份有限公司) for detailed information about the Global Offering 
described below before deciding whether or not to invest in the H Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Sole Sponsor and the Sponsor-
Overall Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting – 
Underwriting Arrangements and Expenses – Hong Kong Public Offering – Hong Kong 
Underwriting Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 
a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on August 25, 
2026).

<<<PAGE 25>>>
25
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering (before any exercise of the 
Over-allotment Option and assuming that no additional Shares are issued pursuant to the 2024 
Restricted Share Incentive Plan), the total market value of the H Shares to be held by the public 
is expected to be approximately HK$3.1 billion, calculated based on the final Offer Price of 
HK$100.00 per H Share, which is higher than the prescribed market value of the H Shares required 
to be held by the public of HK$3 billion under Rule 19A.13A(2)(b) of the Listing Rules, thereby 
satisfying Rule 8.08(1) (as amended and replaced by Rule 19A.13A(2)) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the H Shares of the Company at the time of Listing. Based on 
the final Offer Price of HK$100.00 per H Share, the Company satisfies the free float requirement 
under Rule 19A.13C of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering (before 
any exercise of the Over-allotment Option and assuming that no additional Shares are issued 
pursuant to the 2024 Restricted Share Incentive Plan): (i) the Shares will be held by at least 300 
Shareholders at the time of Listing, in compliance with Rule 8.08(2) of the Listing Rules; (ii) 
the three largest public Shareholders will not hold more than 50% of the H Shares held in public 
hands at the time of Listing, in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; (iii) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of the 
Company immediately after the Global Offering; and (iv) there will not be any new substantial 
Shareholder (as defined in the Listing Rules) immediately after the Global Offering.

<<<PAGE 26>>>
26
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, August 
25, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting – Underwriting Arrangements 
and Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade the H Shares on the basis of publicly available allocation 
details prior to the receipt of H Share certificates or prior to the H Share certificates becoming 
valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Tuesday, 
August 25, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Tuesday, August 25, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 100 H Shares each, and the stock code of the H Shares will 
be 3223.
By order of the Board
Ingenic Semiconductor Co., Ltd.
Dr. Liu Qiang
Executive Director, Chairman of the Board and General Manager
Beijing, PRC, August 24, 2026
As of the date of this announcement, the Board comprises (i) Dr. Liu Qiang, Mr. Zhang Jin, Mr. 
Xian Yonghui and Mr. Huang Lei as executive Directors; (ii) Mr. Li Jie, Mr. Zheng Hao and Ms. 
Zhang Yanxiang as non-executive Directors; and (iii) Mr. Ye Jinfu, Dr. Xiao Limin, Ms. Yu Ying 
and Mr. Xiang Zuo as independent non-executive Directors.
