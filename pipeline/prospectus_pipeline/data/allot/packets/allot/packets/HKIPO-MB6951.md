# 配发结果公告抽取任务：6951.HK Chaozhou Three-Circle (Group) Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**08/07/2026 22:36**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0708/2026070801348.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6951.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not, and is not intended to, constitute or form a part of any offer or solicitation to 
purchase or subscribe for securities in the United States or in any other jurisdiction. The Offer Shares have 
not been and will not be registered under the United States Securities Act of 1933, as amended from time to 
time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the United States and 
may not be offered, sold, pledged or otherwise transferred within the United States, except in transactions 
exempt from, or not subject to, the registration requirements of the U.S. Securities Act and in compliance with 
any applicable state securities laws. The Offer Shares are being offered and sold outside the United States in 
offshore transactions in accordance with Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. Potential investors should read the Prospectus for detailed information 
about the Company and the Global Offering described below before deciding whether or not to invest in the 
Offer Shares.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings 
as those defined in the prospectus dated June 30, 2026 (the “Prospectus”) issued by Chaozhou Three-Circle 
(Group) Co., Ltd. (潮州三環（集團）股份有限公司) (the “Company”).
In connection with the Global Offering, China Galaxy International Securities (Hong Kong) Co., Limited as 
stabilizing manager (the “Stabilization Manager”) (or its affiliates or any person acting for it), on behalf of 
the Underwriters, to the extent permitted by the applicable laws and regulatory requirements of Hong Kong 
or elsewhere, may over-allocate or effect transactions with a view to stabilizing or supporting the market 
price of the H Shares at such price, in such amounts and in such manners as the Stabilizing Manager, its 
affiliates or any person acting for it may determine and at a level higher than that which might otherwise 
prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing Manager 
(or its affiliates or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, 
if taken, (a) will be conducted at the absolute discretion of the Stabilization Manager (or its affiliates or 
any person acting for it) and in what the Stabilizing Manager reasonably regards as the best interest of our 
Company, (b) may be discontinued at any time and (c) is required to be brought to an end within 30 days 
of the last day for lodging applications under the Hong Kong Public Offering (being Wednesday, August 5, 
2026). Such stabilizing action, if taken, may be effected in all jurisdictions where it is permissible to do so, in 
each case in compliance with all applicable laws, rules and regulatory requirements, including the Securities 
and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under 
the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H 
Shares for longer than the stabilization period, which will begin on the Listing Date, and is expected to expire 
on the 30th day after the last day for lodging applications under the Hong Kong Public Offering (being 
Wednesday, August 5, 2026). After this date, when no further stabilizing action may be taken, demand for the 
H Shares, and therefore the price of the H Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions 
set out in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside 
Hong Kong and/or not resident in Hong Kong. Potential investors of the Offer Shares should note that the 
Sole Sponsor and the Overall Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall 
be entitled to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus 
at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date.

<<<PAGE 2>>>
– 2 –
Chaozhou Three-Circle (Group) Co., Ltd.
潮州三環（集團）股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the 
Global Offering
:
71,364,300 H Shares (subject to the 
Over-allotment Option)
Number of Hong Kong Offer Shares
:
7,136,500 H Shares
Number of International Offer Shares :
64,227,800 H Shares (subject to the 
Over-allotment Option)
Final Offer Price
:
HK$100.30 per H Share, plus brokerage 
of 1.0%, SFC transaction levy of 
0.0027%, AFRC transaction levy of 
0.00015% and Stock Exchange trading 
fee of 0.00565%
Nominal value
:
RMB1.00 per H Share 
Stock code
:
6951
Sole Sponsor and Sole Overall Coordinator
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunner and Joint Lead Manager

<<<PAGE 3>>>
3 
 
 
Chaozhou Three-Circle (Group) Co., Ltd. 
潮州三環（集團）股份有限公司 
ANNOUNCEMENT OF ALLOTMENT RESULTS 
 
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could 
move substantially even with a small number of Shares traded and should exercise extreme 
caution when dealing in the H Shares. 
SUMMARY 
* 
see note at the end of the announcement 
* 
without taking into account any exercise of the Over-allotment Option. 
 
Company Information 
Stock Code 
6951 
Stock Short Name 
CCTC 
Dealings commencement date 
July 9, 2026* 
 
Price Information 
Final Offer Price 
HK$100.30 
Offer Shares and Share Capital 
Number of Offer Shares* 
71,364,300 
Final Number of Offer Shares in Hong 
Kong Public Offering 
7,136,500 
Final Number of Offer Shares in 
International Offering* 
64,227,800 
Number of issued Shares upon Listing 
(before exercise of the Over-allotment 
Option) 
1,987,861,671 
 

<<<PAGE 4>>>
4 
 
 
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website. 
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details 
of the use of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” 
of the Prospectus. The Company will adjust the allocation of the net proceeds from the exercise 
of the Over-allotment Option (if any) for the purposes as set out in the section headed “Future Plans 
and Use of Proceeds” of the Prospectus on a pro rata basis. 
 
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING 
 
No. of valid applications 
174,984 
No. of successful applications 
40,369 
Subscription level 
327.49 times 
Claw-back triggered 
N/A 
No. of Offer Shares initially available under the Hong Kong Public 
Offering 
7,136,500 
Final no. of Offer Shares under the Hong Kong Public Offering 
7,136,500 
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering 
10% 
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can 
refer to www.eipo.com.hk/eIPOAllotment to perform a search identification number or www.eipo. 
com.hk/eIPOAllotment for the full list of allottees. 
Over-allocation 
No. of Offer Shares over-allocated 
10,704,600 
Proceeds 
Gross proceeds (Note) 
HK$7,157.8 million 
Less: 
Estimated listing expenses payable 
based on Offer Price 
HK$111.9 million 
Net Proceeds 
HK$7,045.9 million 

<<<PAGE 5>>>
5 
 
 
INTERNATIONAL OFFERING 
 
No. of placees 
151 
Subscription Level 
16.24 times 
No. of Offer Shares initially available under 
the International Offering 
64,227,800 
Final no. of Offer Shares under the 
International Offering 
64,227,800 
% of Offer Shares under the International 
Offering to the Global Offering 
90% 
The Directors confirm that, to the best of their knowledge, information and belief, save for 
(a) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange 
to permit H Shares in the International Offering to be placed to certain Existing Minority Shareholders 
and/or their close associates, and (b) a consent under Chapter 4.15 of the Guide for New Listing 
Applicants to permit the Company to, among other things, allocate further H Shares in the 
International Offering to certain Cornerstone Investors and existing Shareholders (including those who 
are close associate(s) of an existing Shareholder) and/or their respective close associates, (i) none 
of the Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, Controlling Shareholders, 
substantial Shareholders, existing Shareholders or any of the Company’s subsidiaries or their 
respective close associates; and (ii) none of the placees and the public who have purchased the 
Offer Shares are accustomed to taking instructions from the Company, any of the Directors, chief 
executive of the Company, Controlling Shareholders, substantial Shareholders, existing Shareholders 
or any of the Company’s subsidiaries or their respective close associates in relation to the 
acquisition, disposal, voting or other disposition of H Shares registered in his/her/its name or otherwise 
held by him/her/it. 
The placees in the International Offering include the following: 
Cornerstone Investors 
 
Approximate 
% of total 
issued share 
Approximate 
capital after 
% of Offer 
the Global 
Shares 
Offering 
(assuming 
(assuming 
No. of 
the Over- 
the Over- 
Existing 
Offer 
allotment 
allotment 
Shareholders 
Shares 
Option is not 
Option is not 
or their close 
Investor 
allocated 
exercised) 
exercised) 
associates 
Taibai Investments Pte. Ltd. (“Temasek”) 
3,906,700 
5.47% 
0.20% 
Yes 

<<<PAGE 6>>>
6 
 
 
JPMorgan Asset Management (Asia Pacific) Limited 
(“JPMAMAPL”) 
3,906,700 
5.47% 
0.20% 
Yes 
CPE River Investment Limited (“CPE River”) 
3,906,700 
5.47% 
0.20% 
No 
Ninety One Asia Pte. Limited (“Ninety One Asia”) 
2,344,000 
3.28% 
0.12% 
Yes 
Alibaba Investment Limited (“Alibaba Investment”) 
2,344,000 
3.28% 
0.12% 
No 
Huang River Investment Limited (“Huang 
River”) 
1,953,300 
2.74% 
0.10% 
No 
Goldman Sachs Asset Management (Hong Kong) 
Limited (高盛資產管理(香港)有限公司) (“GSAM”) 
1,562,600 
2.19% 
0.08% 
Yes 
Manulife Investment Management (Hong Kong) Limited 
(宏利投資管理(香港)有限公司) (“Manulife 
Investment”), in its capacity as investment manager of 
the following entities: a sub-fund of Manulife Provident 
Funds Unit Trust Series: Manulife Hong Kong Equity 
Fund, and a sub-fund of Manulife Global Fund: Dragon 
Growth Fund (collectively, the “Manulife-managed 
Funds”) 
1,562,600 
2.19% 
0.08% 
No 
Taikang Life Insurance Co., Ltd (泰康人壽保險有限責
任公司) (“Taikang Life”) 
1,562,600 
2.19% 
0.08% 
Yes 
China Universal Asset Management Company Limited (
匯添富基金管理股份有限公司) (“CUAM”) and China 
Universal Asset Management (Hong Kong) Company 
Limited (匯添富資產管理(香港)有限公司) (“China 
Universal (HK)”, together with CUAM, “China 
Universal Investors”) 
1,562,600 
2.19% 
0.08% 
Yes 
Bosera Asset Management (International) Co., Limited  
(博時基金(國際)有限公司) (“Bosera International”) 
1,562,600 
2.19% 
0.08% 
Yes 
ICBC Wealth Management Co., Ltd. (工銀理財有限責任
公司) (“ICBC Wealth”) 
1,562,600 
2.19% 
0.08% 
Yes 
IvyRock Asset Management (HK) Limited (常春藤資產
管理(香港)有限公司) (“IvyRock”) 
1,562,600 
2.19% 
0.08% 
Yes 
Greater Bay Area Homeland Investments Limited (大灣
區共同家園投資有限公司) (“GBAHIL”) 
1,562,600 
2.19% 
0.08% 
No 
Metazone Link (HK) Limited (“Metazone”) 
1,562,600 
2.19% 
0.08% 
No 
Verition Multi-Strategy Master Fund Ltd. (“Verition 
Fund”) 
1,562,600 
2.19% 
0.08% 
No 
Schonfeld Global Master Fund L.P. (“GMF”) and 
Schonfeld IR Master Fund Pte. Ltd. (“IRMF”) 
1,562,600 
2.19% 
0.08% 
Yes 
Total 
35,550,000 
49.81% 
1.79% 
Note: 
1. In addition to the Offer Shares subscribed for as Cornerstone Investors, Temasek, JPMAMAPL, Ninety One Asia,
GSAM, Bosera International, CPE River, Alibaba Investment, Verition Fund, GBAHIL, Manulife Investment and 
Huang River and/or their respective close associates, where applicable, were allocated further Offer Shares as placees
in the International Offering. Please refer to the section headed “Allotment Results Details – International Offer –
Allottees with Waivers/Consents Obtained” in this announcement for details. Only the Offer Shares subscribed for as

<<<PAGE 7>>>
7 
 
 
Cornerstone Investors are subject to lock-up as indicated below. For details, please refer to the section headed “Lock-
up Undertakings – Cornerstone Investors” in this announcement. 

<<<PAGE 8>>>
8 
 
 
Allottees with waivers/consents obtained 
 
Investor 
No. of Offer 
Shares 
allocated 
Approximate 
% of Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised) 
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised) 
Relationship 
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by Existing 
Minority Shareholders holding more than 1% of the issued share capital of the Company immediately prior 
to the completion of the Global Offering and/or their close associates Note 1 
Invesco Great Wall Fund 
Management Company 
Limited 
39,000 
0.05% 
0.002% 
An existing Shareholder 
Allottees with consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocations of further Shares to existing Shareholders and Cornerstone Investors and/or their close 
associatesNote 2 
Temasek 
2,109,500 
2.96% 
0.11% 
An existing Shareholder and 
a Cornerstone Investor 
JPMAMAPL 
1,953,300 
2.74% 
0.10% 
An existing Shareholder and 
a Cornerstone Investor 
Ninety One Asia 
1,172,000 
1.64% 
0.06% 
An existing Shareholder and 
a Cornerstone Investor 
GSAM 
781,300 
1.09% 
0.04% 
An existing Shareholder and 
a Cornerstone Investor 
Bosera International 
625,000 
0.88% 
0.03% 
An existing Shareholder and 
a Cornerstone Investor 
CPE River 
1,953,300 
2.74% 
0.10% 
A Cornerstone Investor 
Alibaba Investment 
859,400 
1.20% 
0.04% 
A Cornerstone Investor 
Verition Fund 
273,400 
0.38% 
0.01% 
A Cornerstone Investor 
GBAHIL 
234,400 
 
0.32% 
0.02% 
A Cornerstone Investor 
Manulife Investment 
390,600 
0.55% 
0.02% 
A Cornerstone Investor 

<<<PAGE 9>>>
9 
 
 
Huang River 
859,400 
1.20% 
0.04% 
A Cornerstone Investor 
E Fund Management Co., 
Ltd. 
 
E Fund Management 
 (Hong Kong) Co, Limited 
94,000 
 
 
23,100 
0.13% 
 
 
0.03% 
0.004% 
 
 
0.001% 
An existing Shareholder 
 
 
An existing Shareholder 
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations to connected clientsNote 3 
ICBC UBS Asset 
Management Company 
Limited  
 
58,600 
0.08% 
0.003% 
Connected client as placee 
ICBC UBS Asset 
Management 
(International) Company 
Limited 
 
19,500 
0.03% 
0.001% 
Connected client as placee 
China Asset Management 
Co. Ltd 
39,000 
0.05% 
0.002% 
Connected client as placee 
China Asset Management 
(Hong Kong) Limited 
78,100 
0.11% 
0.004% 
Connected client as placee 
ICBC Wealth 
Management Co., Ltd 
1,562,600 
 
2.19% 
0.08% 
Connected Client as 
Cornerstone Investor 
 

<<<PAGE 10>>>
10 
 
 
Notes: 
1. 
The Stock Exchange has granted a waiver from strict compliance with the requirements under Rule 10.04 of the Listing 
Rules and consent under paragraph 1C(2) of the Placing Guidelines to permit H Shares in the International Offering to be 
placed to certain Existing Minority Shareholders and/or their close associates. Please refer to the section headed “Waivers 
from strict compliance with the Listing Rules — Waiver in relation to Allocation of H Shares to Existing Minority 
Shareholders and Their Close Associates” of the Prospectus for details. 
2. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the number of Offer 
Shares allocated to the investors as placees in the International Offering. For allocations of Offer Shares to the relevant 
investors as Cornerstone Investors, please refer to the section headed “Allotment Results Details – International Offer – 
Cornerstone Investors” in this announcement. For details of the consent under Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations of further Shares to the existing Shareholders and/or their close associates and 
Cornerstone Investors, please refer to the section headed “Others/Additional Information – Allocations of Offer Shares to 
existing Shareholders and Cornerstone Investors and/or their close associates with a consent under Chapter 4.15 of the 
Guide for New Listing Applicants” in this announcement. 
3. 
For details of the consent under paragraph 1C of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing 
Applicants in relation to allocations to connected clients, please refer to the section headed “Others/Additional 
Information – Placing to connected clients with prior consents under paragraph 1C of the Placing Guidelines” in this 
announcement. 

<<<PAGE 11>>>
11 
 
 
LOCK-UP UNDERTAKINGS 
Cornerstone Investors 
 
Name 
Number of 
Shares held 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing 
Approximate 
% of total 
issued 
H Shares 
after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised) 
Approximate 
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised) 
Last day 
subject to 
the lock-up 
undertakings 
Temasek  
3,906,700 
5.47% 
0.20% January 8, 2027 
JPMAMAPL 
3,906,700 
5.47% 
0.20% January 8, 2027 
CPE River 
3,906,700 
5.47% 
0.20% January 8, 2027 
Ninety One Asia 
2,344,000 
3.28% 
0.12% January 8, 2027 
Alibaba Investment 
2,344,000 
3.28% 
0.12% January 8, 2027 
Huang River 
1,953,300 
2.74% 
0.10% January 8, 2027 
GSAM 
1,562,600 
2.19% 
0.08% January 8, 2027 
Manulife-managed 
Funds 
1,562,600 
2.19% 
0.08% January 8, 2027 
Taikang Life 
1,562,600 
2.19% 
0.08% January 8, 2027 
China Universal 
Investors 
1,562,600 
2.19% 
0.08% January 8, 2027 
Bosera Internaitonal 
1,562,600 
2.19% 
0.08% January 8, 2027 
ICBC Wealth 
1,562,600 
2.19% 
0.08% January 8, 2027 
Ivy Rock 
1,562,600 
2.19% 
0.08% January 8, 2027 
GBAHIL 
1,562,600 
2.19% 
0.08% January 8, 2027 
Metazone 
1,562,600 
2.19% 
0.08% January 8, 2027 
Verition Fund 
1,562,600 
2.19% 
0.08% January 8, 2027 
GMF and IRMF 
1,562,600 
2.19% 
0.08% January 8, 2027 

<<<PAGE 12>>>
12 
 
 
Notes: 
1.  In accordance with the relevant cornerstone investment agreements, the required lock-up ends on January 8, 2027. The 
Cornerstone Investors will cease to be prohibited from disposing of or transferring Shares subscribed for pursuant to 
the relevant cornerstone investment agreements after the indicated date. 
 

<<<PAGE 13>>>
13 
 
 
Controlling Shareholders 
 
Name 
Number of 
Shares held 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing 
Approximate 
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised)Note 1 
Approximate 
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing 
(assuming 
the Over-
allotment 
Option is not 
exercised) 
Last day 
subject to 
the lock-up 
undertakings 
Zhang Wanzhen 
53,592,000 
-- 
2.70%  January 8, 2027 
(First Six-month 
Period)1 
July 8, 2027 
(Second Six-month 
Period)2 
Chaozhou Tririver  
Investment Co., Ltd. 
645,357,856 
 
-- 
32.46% January 8, 2027 
(First Six-month 
Period)1 
July 8, 2027 
(Second Six-month 
Period)2 
Notes: 
 
1. 
The Controlling Shareholders may dispose of or transfer Shares after the indicated date provided that each Controlling 
Shareholder will not cease to be a Controlling Shareholder. 
2. 
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after the indicated 
date. 
 

<<<PAGE 14>>>
14 
 
 
PLACEE CONCENTRATION ANALYSIS 
 
% of total 
issued 
Allotment 
Allotment 
share 
as % of 
as % of 
% of total 
capital 
International 
total Offer 
issued 
upon 
Offering 
Allotment 
Shares 
share 
Listing 
Allotment 
(assuming 
as % of 
(assuming 
capital 
(assuming 
as % of 
the Over- 
total Offer 
the Over- 
upon 
the Over- 
International 
allotment 
Shares 
allotment 
Listing 
allotment 
Offering 
Option 
(assuming 
Option 
(assuming 
Option 
(assuming 
is fully 
no exercise 
is fully 
no exercise 
is fully 
no exercise 
exercised 
of the 
exercised 
Number 
of the 
exercised 
Number of 
of the Over- 
and new 
Over- 
and new 
of H Shares 
Over- 
and new 
H Shares 
allotment 
Shares are 
allotment 
Shares are 
held upon 
allotment 
Shares 
Placees* 
allotted 
Option) 
issued) 
Option) 
issued) 
Listing 
Option) 
are issued) 
Top 1 
5,860,000 
9.1% 
7.8% 
8.2% 
7.1% 
5,860,000  
0.3% 
0.3% 
Top 5 
24,299,400 
37.8% 
32.4% 
34.0% 
29.6% 
24,299,400  
1.2% 
1.2% 
Top 10 
35,550,200 
55.4% 
47.4% 
49.8% 
43.3% 
35,550,200  
1.8% 
1.8% 
Top 25 
53,426,300 
83.2% 
71.3% 
74.9% 
65.1% 
53,426,300  
2.7% 
2.7% 
Note 
* 
Ranking of placees is based on the number of H Shares allotted to the placees. 
H SHAREHOLDERS CONCENTRATION ANALYSIS 
 
% of total 
issued 
Allotment 
share 
as % of 
Capital 
International 
Allotment 
% of total 
upon 
Offering 
as % of 
issued 
Listing 
(assuming 
total Offer 
share 
(assuming 
Allotment 
the Over- 
Allotment 
Shares 
capital 
the 
as % of 
allotment 
as % of 
(assuming the 
upon Over-allotment 
International 
Option is 
total Offer Over-allotment 
Listing 
Option 
Offering 
fully 
Shares 
Option 
(assuming 
is fully 
(assuming no 
exercised 
(assuming no 
is fully 
Number 
no exercise 
exercised 
Number of 
exercise of the 
and new 
exercise of the 
exercised and 
of H Shares 
of the 
and new 
H Shares Over-allotment 
H Shares are Over-allotment 
new H Shares 
held upon Over-allotment 
H Shares 
H Shareholders* 
allotted 
Option) 
issued) 
Option) 
are issued) 
Listing 
Option) 
are issued) 
Top 1 
5,860,000 
9.1% 
7.8% 
8.2% 
7.1% 
5,860,000 
0.3% 
0.3% 
Top 5 
24,299,400 
37.8% 
32.4% 
34.0% 
29.6% 
24,299,400 
1.2% 
1.2% 
Top 10 
35,550,200 
55.4% 
47.4% 
49.8% 
43.3% 
35,550,200 
1.8% 
1.8% 
Top 25 
53,426,300 
83.2% 
71.3% 
74.9% 
65.1% 
53,426,300 
2.7% 
2.7% 
Note 
* 
Ranking of H Shareholders is based on the number of H Shares held by the Shareholders upon Listing. 

<<<PAGE 15>>>
15 
 
 
SHAREHOLDER CONCENTRATION ANALYSIS 
 
% of total 
Allotment 
issued 
share 
as % of 
capital 
total Offer 
% of total 
upon 
Allotment 
Shares 
issued 
share 
Listing 
as % of 
Allotment 
(assuming 
capital (assuming 
Allotment 
International 
as % of 
the Over- 
upon 
the Over- 
as % of 
Offering 
total Offer 
allotment 
Listing allotment 
International 
(assuming the 
Shares 
Option 
(assuming 
Option 
Offering 
Over-allotment 
(assuming 
is fully 
no 
exercise 
is fully 
(assuming no 
Option is fully 
no exercise 
exercised 
Number 
of the exercised 
Number 
exercise of the 
exercised and 
of the Over- 
and new 
of Shares 
Over- 
and new 
of H Shares 
Over-allotment 
new Shares 
allotment 
Shares are 
held upon allotment Shares are 
Shareholders* 
allotted 
Option) 
are issued) 
Option) 
issued) 
Listing 
Option) 
issued) 
Top 1 
- 
0.0% 
0.0% 
0.0% 
0.0% 
698,949,856 
35.2% 
35.0% 
Top 5 
1,679,700 
2.6% 
2.2% 
2.4% 
2.0% 
978,014,487 
49.2% 
48.9% 
Top 10 
 
2,773,500 
4.3% 
3.7% 
3.9% 
3.4% 
1,072,127,764 
53.9% 
53.6% 
Top 25 
6,312,800 
 
9.8% 
8.4% 
8.8% 
7.7% 
1,226,204,892 
61.7% 
61.4% 
Note 
 
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing. 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below: 
 
NO. OF 
SHARES 
APPLIED FOR 
NO. OF 
VALID 
APPLICATIONS 
BASIS OF ALLOTMENT / BALLOT 
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR 
POOL A 
100 
62,183 429 out of 62,183 to receive 100 Shares 
0.69% 
200 
8,572 118 out of 8,572 to receive 100 Shares 
0.69% 
300 
6,795 141 out of 6,795 to receive 100 Shares 
0.69% 
400 
17,053 471 out of 17,053 to receive 100 Shares 
0.69% 

<<<PAGE 16>>>
16 
 
 
500 
3,523 122 out of 3,523 to receive 100 Shares 
0.69% 
600 
1,778 74 out of 1,778 to receive 100 Shares 
0.69% 
NO. OF 
SHARES 
APPLIED FOR 
NO. OF 
VALID 
APPLICATIONS 
BASIS OF ALLOTMENT / BALLOT 
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR 
700 
1,451 70 out of 1,451 to receive 100 Shares 
0.69% 
800 
1,499 83 out of 1,499 to receive 100 Shares 
0.69% 
900 
5,414 336 out of 5,414 to receive 100 Shares 
0.69% 
1,000 
7,519 519 out of 7,519 to receive 100 Shares 
0.69% 
1,500 
3,578 370 out of 3,578 to receive 100 Shares 
0.69% 
2,000 
4,087 564 out of 4,087 to receive 100 Shares 
0.69% 
2,500 
2,234 385 out of 2,234 to receive 100 Shares 
0.69% 
3,000 
2,589 536 out of 2,589 to receive 100 Shares 
0.69% 
3,500 
1,471 355 out of 1,471 to receive 100 Shares 
0.69% 
4,000 
1,814 501 out of 1,814 to receive 100 Shares 
0.69% 
4,500 
1,186 368 out of 1,186 to receive 100 Shares 
0.69% 
5,000 
2,893 998 out of 2,893 to receive 100 Shares 
0.69% 
6,000 
1,898 786 out of 1,898 to receive 100 Shares 
0.69% 
7,000 
1,438 695 out of 1,438 to receive 100 Shares 
0.69% 
8,000 
1,437 793 out of 1,437 to receive 100 Shares 
0.69% 
9,000 
1,211 752 out of 1,211 to receive 100 Shares 
0.69% 
10,000 
7,290 5,030 out of 7,290 to receive 100 Shares 
0.69% 
20,000 
4,809 
100 Shares plus 1,827 out of 4,809 to receive additional 100 Shares 
0.69% 
30,000 
2,674 
200 Shares plus 187 out of 2,674 to receive additional 100 Shares 
0.69% 
40,000 
3,267 
200 Shares plus 2,482 out of 3,267 to receive additional 100 Shares 
0.69% 
159,663 Total number of Pool A successful applicants: 25,246 
 

<<<PAGE 17>>>
17 
 
 
NO. OF 
SHARES 
APPLIED FOR 
NO. OF 
VALID 
APPLICATIONS 
BASIS OF ALLOTMENT / BALLOT 
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF SHARES 
APPLIED FOR 
POOL B 
50,000 
10,033 9,835 out of 10,033 to receive 100 Shares 
0.20%
100,000 
2,279 100 Shares plus 2,189 out of 2,279 to receive additional 100 Shares 
0.20% 
150,000 
968 200 Shares plus 911 out of 968 to receive additional 100 Shares 
0.20% 
200,000 
651 300 Shares plus 600 out of 651 to receive additional 100 Shares 
0.20% 
250,000 
759 400 Shares plus 684 out of 759 to receive additional 100 Shares 
0.20% 
500,000 
306 900 Shares plus 246 out of 306 to receive additional 100 Shares 
0.20% 
750,000 
98 1,400 Shares plus 69 out of 98 to receive additional 100 Shares 
0.20% 
1,000,000 
84 
1,900 Shares plus 51 out of 84 to receive additional 100 Shares 
0.20% 
1,250,000 
28 
2,400 Shares plus 14 out of 28 to receive additional 100 Shares 
0.20% 
1,500,000 
24 
2,900 Shares plus 10 out of 24 to receive additional 100 Shares 
0.20% 
2,000,000 
46 
3,900 Shares plus 10 out of 46 to receive additional 100 Shares 
0.20% 
2,500,000 
4 
4,900 Shares 
0.20% 
3,000,000 
8 
5,800 Shares plus 7 out of 8 to receive additional 100 Shares 
0.20% 
3,568,200 
33 
6,900 Shares plus 31 out of 33 to receive additional 100 Shares 
0.20% 
 
15,321 Total number of Pool B successful applicants: 15,123 
 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries. 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance materials 
in relation to the placing, allotment and listing of the Company’s H Shares. 
 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and Stock Exchange trading fee payable. 

<<<PAGE 18>>>
18 
 
 
OTHERS/ADDITIONAL INFORMATION 
 
Allocation of H Shares to Existing Minority Shareholders and their close associates 
 
The Company has applied for, and the Stock Exchange has granted, a waiver from strict compliance 
with the requirements under Rule 10.04 of and consent under paragraph 1C(2) of Appendix F1 to the 
Listing Rules to permit H Shares in the International Offering to be placed to certain existing minority 
Shareholders who (i) hold less than 5% of the voting rights in the Company prior to the completion of the 
Global Offering and (ii) are not and will not become (upon the completion of the Global Offering) core 
connected persons of the Company or the close associates of any such core connected person (together, 
the “Existing Minority Shareholders”) and/or their close associates, subject to the conditions as 
follows: 
 
(a) 
each Existing Minority Shareholder to whom the Company may allocate the H Shares in the 
International Offering holds less than 5% of the voting rights in the Company before Listing; 
 
(b) 
each Existing Minority Shareholder is not, and will not be, a core connected person of the Company 
or any close associate of any such core connected person immediately prior to or following the Global 
Offering; 
 
(c) 
none of the Existing Minority Shareholders has the right to appoint a Director and/or have any 
other special rights; 
 
(d) 
allocation to the Existing Minority Shareholders or its close associates will not affect the ability 
of the Company to satisfy the public float requirement as prescribed by the Stock Exchange 
under Rule 8.08 (as amended and replaced by Rule 19A.13A) of the Listing Rules or otherwise 
approved by the Stock Exchange; and 
 
(e) 
none of the Existing Minority Shareholders or its close associates receives any preferential treatment, 
or is in a position to exert influence on the Company to obtain actual or perceived preferential 
treatment in the allocation either as a placee by virtue of its relationship with the Company; 
Please refer to the section headed “Waivers from Strict Compliance with the Listing Rules — Waiver in 
relation to Allocation of H Shares to Existing Minority Shareholders and their Close Associates” in the 
Prospectus for further details of the waiver and consent. Given that (i) there is no requirement to disclose 
interests under PRC laws unless such person is an owner of more than 5% of the issued share capital of the 
Company, the Directors or senior management of the Company or top ten Shareholders, and (ii) The Hong 
Kong Securities Clearing Company Limited, as trustee, holds A Shares on behalf of investors in Hong 
Kong and overseas pursuant to the rules and limits of Shenzhen-Hong Kong Stock Connect and 
the Company is unable to identify Shareholders who hold A Shares through the Shenzhen-Hong Kong 
Stock Connect, allocation to the Existing Minority Shareholders and/or their close associates will not 
be disclosed in this announcement (other than to the extent that such Existing Minority Shareholders or 
close associates subscribe for H Shares as Cornerstone Investors or that such Existing Minority 
Shareholders shall hold more than 1% of the issued share capital of the Company immediately prior to the 
completion of the Global Offering). 

<<<PAGE 19>>>
19 
 
 
All allocations of Offer Shares to the Existing Minority Shareholders are in compliance with all 
the conditions under the waiver and consent granted by the Stock Exchange. 
 
Allocations of Offer Shares to existing Shareholders and Cornerstone Investors and/or their close 
associates with a consent under Chapter 4.15 of the Guide for New Listing Applicants 
 
The Company has applied to, and the Stock Exchange has granted, a consent under Chapter 4.15 
of the Guide for New Listing Applicants to permit the Company to allocate further Offer Shares 
in the International Offering to existing Shareholders and Cornerstone Investors and/or their close 
associates as placees, subject to the following conditions: 
 
(a) 
the final offering size of the Global Offering (excluding any additional Shares which may 
be issued upon exercise of the Over-allotment Option) will be of a total value of at least HK$1 
billion as required by paragraph 18(i) of Chapter 4.15 of the Guide for New Listing Applicants; 
 
(b) 
the Offer Shares allocated to all existing shareholders and their close associates (whether as 
cornerstone investors and/or as placees) as permitted under this exemption do not exceed 30% 
of the total number of the H Shares offered, which is in compliance with paragraph 18(ii) of Chapter 
4.15 of the Guide for New Listing Applicants; 
 
(c) 
each Director, chief executive and controlling shareholders of the Company has confirmed 
that no securities have been allocated to them or their respective close associates under the Size-
based Exemption as required by paragraph 18(iii) of Chapter 4.15 of the Guide for New Listing 
Applicants; 
 
(d) 
the Company will comply with the public float requirement under Rule 8.08(1) and Rule 19A.13A(2) 
of the Listing Rules; and 
 
(e) 
details of the allocation to such existing Shareholders and/or their close associates and Cornerstone 
Investors will be disclosed in this announcement. 
 
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted 
by the Stock Exchange. 
 
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates 
and Cornerstone Investors, please refer to the section headed “Allotment Results Details – International 
Offering – Allottees with Waivers/Consents Obtained” in this announcement. 

<<<PAGE 20>>>
20 
 
 
Placing to connected clients with prior consents under paragraph 1C of the Placing Guidelines 
 
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, consents under 
paragraph 1C of the Placing Guidelines to permit allocation to connected clients pursuant to the 
Placing Guidelines. The allocation of Offer Shares to such connected clients is in compliance with all 
the conditions under the consents granted by the Stock Exchange. Details of the placement to connected 
clients (including the cornerstone tranche and placing tranche) are set out below. 
 
No.      Connected Distributor 
 
Connected Client 
Relationship 
Whether the 
Connected 
Client will 
hold the 
beneficial 
interests of 
the Offer 
Shares on a 
non-
discretionary 
basis or 
discretionary 
basis for 
independent 
third parties 
Number of 
Offer 
Shares 
to be 
allocated to 
the 
connected 
client 
Approximate 
% of Offer 
Shares 
allocated 
to the 
connected 
client 
(assuming no 
exercise of 
the Over-
allotment 
Option) 
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering 
(assuming no 
exercise of 
the Over-
allotment 
Option) 
1. 
ICBC International 
Securities Limited 
(“ICBCI”)  
ICBC UBS Asset 
Management 
Company Limited  
(“ICBC UBS 
AM”)  
(Note 1) 
 
ICBC UBS AM 
is a member of 
the same group 
of companies as 
ICBCI  
Discretionary 
basis 
58,600 
 
0.08% 
0.003% 
2. 
ICBCI 
ICBC UBS Asset 
Management 
(International) 
Company Limited 
(“ICBC UBS AM 
International”) 
(Note 2)  
ICBC UBS 
AM 
International 
is a member 
of the same 
group of 
ICBCI 
Discretionary 
basis 
19,500 
 
0.03% 
0.001% 
3. 
CITIC Securities 
Brokerage (HK) 
Limited (“CSB”) 
China Asset 
Management Co. 
Ltd  
(“China AMC”) 
(Note 3) 
China AMC HK 
is wholly owned 
by China AMC. 
China AMC is 
owned 
as 
to 
62.2% by CITIC 
Securities 
Company 
Limited, which 
is 
holding 
company 
of 
CSB. Therefore, 
CSB, 
China 
AMC and China 
AMC HK are 
Discretionary 
basis 
39,000 
0.05% 
0.002% 
China Asset 
Management 
(Hong Kong) 
Limited 
(“China AMC 
HK”) (Note 4) 
78,100 
0.11% 
0.004% 

<<<PAGE 21>>>
21 
 
 
members of the 
same group. 
4. 
ICBC International 
Securities Limited 
(“ICBC Securities”) 
ICBC 
Wealth 
Management 
Co., Ltd (“ICBC 
Wealth 
Management”) 
(Note 5) 
ICBC 
Wealth 
Management is a 
member of the 
same group of 
ICBC Securities 
Discretionary 
basis 
1,562,600 
 
2.19% 
0.08% 
Notes: 
 
1. 
ICBC UBS AM will hold the Offer Shares in its capacity as the discretionary fund manager managing the funds on behalf 
of its investors. None of its investors holds 30% or more ultimate beneficial interest in the relevant funds. ICBC UBS AM 
has confirmed that, to the best of their knowledge, each of its investors is an independent third party of ICBC UBS AM, 
the companies, its subsidiaries, its substantial shareholders, ICBCI and the companies which are members of the same 
group of companies of ICBCI. 
 
2. 
ICBC UBS AM International will hold the Offer Shares in its capacity as the discretionary fund manager managing the 
funds on behalf of its investors, each of which is an independent third party. None of its investors holds 30% or more 
ultimate beneficial interest in the relevant funds. ICBC UBS AM International has confirmed that, to the best of their 
knowledge each of its investors is an independent third party of ICBC UBS AM International, the companies, its 
subsidiaries, its substantial shareholders, ICBCI and the companies which are members of the same group of companies 
of ICBCI. 
 
3. 
China AMC will hold the Offer Shares in its capacity as the discretionary fund manager managing assets on behalf of its 
underlying client, which is an independent third party. There is no ultimate beneficial owner holding 30% interest or more 
in such underlying client. To the best knowledge of China AMC after due enquiry, the underlying client of China AMC 
is an independent third party of China AMC and CSB, and the companies which are members of the same group of 
companies as each of the Underwriters.  
 
4. 
China AMC HK will hold the Offer Shares in its capacity as the discretionary fund manager managing assets on behalf 
of its underlying clients or mandates, which are independent third parties. To the best knowledge of China AMC HK after 
due enquiry, each of the underlying clients or mandates of China AMC HK and their respective ultimate beneficial owner 
holding 30% or more interest is an independent third party of China AMC HK and CSB, and the companies which are 
members of the same group of companies as each of the Underwriters. 
 
5. 
ICBC Wealth Management had entered into a cornerstone investment agreement with the Company to subscribe for the 
Offer Shares and will hold the Offer Shares on a discretionary basis for and on behalf of independent third-party 
underlying clients and/or accounts under the International Offering. ICBC Wealth Management is a wholly owned 
subsidiary of Industrial and Commercial Bank of China Limited. 

<<<PAGE 22>>>
22 
 
 
DISCLAIMERS 
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong 
Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or 
any part of the contents of this announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and the 
District of Columbia). This announcement does not, and is not intended to, constitute or form 
a part of any offer or solicitation to purchase or subscribe for securities in the United States 
or in any other jurisdiction. The Offer Shares have not been and will not be registered under 
the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities 
Act”) or securities law of any state or other jurisdiction of the United States and may not be offered, 
sold, pledged or otherwise transferred within the United States, except in transactions exempt from, 
or not subject to, the registration requirements of the U.S. Securities Act and in compliance with any 
applicable state securities laws. 
The Offer Shares are being offered and sold outside the United States in offshore transactions in 
accordance with Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to 
acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated June 30, 2026 issued by Chaozhou Three-Circle (Group) 
Co., Ltd. (潮州三環（集團）股份有限公司) for detailed information about the Global Offering 
described above before deciding whether or not to invest in the H Shares thereby being offered. 
* Potential investors of the Offer Shares should note that the Sole Sponsor and the Overall 
Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall be entitled to 
terminate their obligations under the Hong Kong Underwriting Agreement with immediate effect 
upon the occurrence of any of the events set out in the section headed “Underwriting – 
Underwriting Arrangements and Expenses – Hong Kong Public Offering – Hong Kong 
Underwriting Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 
a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Thursday, July 
9, 2026). 

<<<PAGE 23>>>
– 23 –
PUBLIC FLOAT
The total number of the H Shares to be issued pursuant to the Global Offering represents 
approximately 3.60% of the total issued share capital of the Company (assuming the 
Over-allotment Option is not exercised and excluding 5,133,800 A Shares repurchased 
by the Company as treasury shares). Immediately following the completion of the Global 
Offering (assuming the Over-allotment Option is not exercised), based on an Offer Price of 
HK$100.30 per Share, the market capitalization of the H Shares immediately upon Listing is 
expected to be HK$7,157.84 million, thereby satisfying the public float requirement under 
Rule 8.08(1) (as amended and replaced by Rule 19A.13A) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following 
the Listing Date. As such, Shares held by the Cornerstone Investors upon the Listing shall 
not be counted towards the free float of the H Shares of the Company at the time of Listing. 
Based on the Offer Price of HK$100.30 per Share, the Company satisfies the free float 
requirement under Rule 8.08A (as amended and replaced by Rule 19A.13C) of the Listing 
Rules.
The Directors confirm that, immediately following the completion of the Global Offering 
(before any exercise of the Over-allotment Option), (i) no placee will, individually, be 
placed more than 10% of the enlarged issued share capital of the Company immediately 
after the Global Offering; (ii) there will not be any new substantial Shareholder immediately 
after the Global Offering; (iii) the three largest public Shareholders do not hold more than 
50% of the H Shares held in public hands at the time of the Listing in compliance with Rules 
8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at the 
time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Thursday, 
July 9, 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” 
in the Prospectus has not been exercised. Investors who trade the H Shares on the basis of 
publicly available allocation details prior to the receipt of Share certificates or prior to the H 
Share certificates becoming valid evidence of title do so entirely at their own risk.

<<<PAGE 24>>>
– 24 –
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on 
Thursday, July 9, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the 
Stock Exchange will commence at 9:00 a.m. on Thursday, July 9, 2026 (Hong Kong time). 
The Shares will be traded in board lots of 100 Shares each, and the stock code of the H 
Shares will be 6951.
By order of the Board
Chaozhou Three-Circle (Group) Co., Ltd.
潮州三環（集團）股份有限公司
Mr. Li Gang
Chairman and Executive Director
Hong Kong, July 8, 2026
As at the date of this announcement, the Board comprises: (i) Mr. Zhang Wanzhen as non-executive Director; 
(ii) Mr. Li Gang, Mr. Ma Yanhong and Mr. Qiu Jihua as executive Directors; (iii) Mr. Jiang Lijun, Mr. Wen 
Xueli and Mr. Su Yanqi as independent non-executive Directors; and (iv) Ms. Wong Sze Wing as a proposed 
independent non-executive Director.
